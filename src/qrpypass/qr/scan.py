# src/qrpypass/service/scan.py
from __future__ import annotations

from typing import Dict, List, Optional, Tuple, Iterable
import os
import logging

import cv2
import numpy as np

from .decode import (
    QRDecodeError,
    decode_multi,
    decode_single,
    decode_curved,
    decode_pyzbar_fast,
    decode_zxing,
    cleanup_variants,
)
from .models import QRResult

# Optional (but strongly recommended): PIL for EXIF orientation fix
try:
    from PIL import Image, ImageOps  # type: ignore
except Exception:  # pragma: no cover
    Image = None  # type: ignore
    ImageOps = None  # type: ignore


_LOG = logging.getLogger("qrpypass.qr")
_DEBUG = os.getenv("QRPYPASS_QR_DEBUG", "").strip().lower() in ("1", "true", "yes", "on")

if not _LOG.handlers:
    logging.basicConfig(level=logging.DEBUG if _DEBUG else logging.INFO)

if _DEBUG:
    _LOG.setLevel(logging.DEBUG)


def _dbg(msg: str, *args) -> None:
    if _DEBUG:
        _LOG.debug(msg, *args)


def _bbox_area(b: Optional[Tuple[int, int, int, int]]) -> int:
    if not b:
        return 10**18
    _, _, w, h = b
    return int(w) * int(h)


def _method_rank(method: str) -> int:
    """
    Lower is better. Prefer methods that are:
      - robust on real photos
      - likely to return correct payload early
      - (optionally) provide corners/bbox
    """
    m = (method or "").lower()

    # Best: WeChat (opencv-contrib) is often strongest on phone photos/stylized codes
    if m.startswith("wechat"):
        return 0

    # Then: pyzbar is fast + good on crisp, standard QRs
    if m.startswith("pyzbar"):
        return 1

    # Then: zxing on cleaned / warped variants
    if m.startswith("zxing_warp_clean"):
        return 2
    if m.startswith("zxing_clean"):
        return 3

    # Then: OpenCV decode paths
    if m == "multi":
        return 4
    if m == "single":
        return 5
    if m == "curved":
        return 6

    # Then: zxing on warped raw (still good)
    if m.startswith("zxing_warp_full"):
        return 7

    # Then: zxing on full raw image
    if m.startswith("zxing_full"):
        return 8

    # Last resort: tiles
    if m.startswith("zxing_tile"):
        return 9

    return 99


def _better(a: QRResult, b: QRResult) -> QRResult:
    ra, rb = _method_rank(a.method), _method_rank(b.method)
    if ra != rb:
        return a if ra < rb else b

    a_has = (a.bbox is not None) + (a.corners is not None)
    b_has = (b.bbox is not None) + (b.corners is not None)
    if a_has != b_has:
        return a if a_has > b_has else b

    return a if _bbox_area(a.bbox) <= _bbox_area(b.bbox) else b


def _consider(best: Dict[str, QRResult], r: QRResult) -> None:
    if not r.payload:
        return
    cur = best.get(r.payload)
    best[r.payload] = r if cur is None else _better(cur, r)


def _ordered(best: Dict[str, QRResult], max_results: int) -> List[QRResult]:
    ordered = sorted(best.values(), key=lambda r: (_method_rank(r.method), _bbox_area(r.bbox)))
    return ordered[:max_results]


def _tile_params(h: int, w: int) -> Tuple[int, int]:
    tile = 1100 if max(h, w) >= 3000 else 900
    overlap = 260
    return tile, overlap


def _imread_exif_fixed(image_path: str) -> np.ndarray:
    """
    OpenCV ignores EXIF Orientation. Modern phone images often rely on EXIF to
    represent rotation, so decode pipelines can fail if we don't apply it.

    Prefer PIL + ImageOps.exif_transpose when available; fall back to cv2.imread.
    """
    if Image is not None and ImageOps is not None:
        try:
            im = Image.open(image_path)
            im = ImageOps.exif_transpose(im)  # apply orientation properly
            im = im.convert("RGB")
            arr = np.array(im)  # RGB
            bgr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
            return bgr
        except Exception as e:  # pragma: no cover
            _dbg("imread_exif_fixed: PIL path failed, falling back to cv2.imread: %s", e)

    img = cv2.imread(image_path)
    if img is None:
        raise QRDecodeError(f"Image could not be read: {image_path}")
    return img


def _order_quad(pts: np.ndarray) -> np.ndarray:
    """
    Ensure quad points are ordered: [tl, tr, br, bl]
    pts: (4,2)
    """
    pts = np.asarray(pts, dtype=np.float32)
    s = pts.sum(axis=1)
    d = np.diff(pts, axis=1).reshape(-1)

    tl = pts[np.argmin(s)]
    br = pts[np.argmax(s)]
    tr = pts[np.argmin(d)]
    bl = pts[np.argmax(d)]

    return np.stack([tl, tr, br, bl], axis=0).astype(np.float32)


def _warp_quad(gray: np.ndarray, quad: np.ndarray, size: int = 768) -> np.ndarray:
    quad = _order_quad(quad)

    dst = np.array(
        [[0, 0], [size - 1, 0], [size - 1, size - 1], [0, size - 1]],
        dtype=np.float32,
    )

    M = cv2.getPerspectiveTransform(quad, dst)
    warped = cv2.warpPerspective(gray, M, (size, size), flags=cv2.INTER_LINEAR)
    return warped


def _quads_from_opencv_detector(gray: np.ndarray) -> List[np.ndarray]:
    """
    Use OpenCV's QRCodeDetector *detection* to get candidate quads even when decode fails.
    This is the "detect regardless of weird payload/styling" path.

    Returns list of (4,2) float32 quads in original image coordinates.
    """
    det = cv2.QRCodeDetector()
    quads: List[np.ndarray] = []

    # detectMulti exists in newer OpenCV versions; keep it optional
    try:
        ok, points = det.detectMulti(gray)  # type: ignore[attr-defined]
        if ok and points is not None:
            # points: (N,4,2)
            for q in np.asarray(points, dtype=np.float32):
                if q.shape == (4, 2):
                    quads.append(q)
    except Exception:
        pass

    # Single detect fallback
    try:
        ok, points = det.detect(gray)
        if ok and points is not None:
            q = np.asarray(points, dtype=np.float32).reshape(-1, 2)
            if q.shape == (4, 2):
                quads.append(q)
    except Exception:
        pass

    # Deduplicate roughly by centroid
    uniq: List[np.ndarray] = []
    seen: List[Tuple[int, int]] = []
    for q in quads:
        c = q.mean(axis=0)
        key = (int(c[0] // 20), int(c[1] // 20))
        if key not in seen:
            seen.append(key)
            uniq.append(q)

    return uniq


def _quads_from_contours(gray: np.ndarray) -> List[np.ndarray]:
    """
    Heuristic contour-based quad proposals:
    - adaptive threshold
    - find contours
    - keep convex 4-vertex polygons that are "square-ish"
    This helps when OpenCV's QR detector fails to detect any quad on stylized codes.

    This is intentionally bounded and heuristic, not exhaustive.
    """
    H, W = gray.shape[:2]
    quads: List[np.ndarray] = []

    # A few thresholding strategies
    variants: List[Tuple[str, np.ndarray]] = []

    try:
        den = cv2.bilateralFilter(gray, 7, 50, 50)
    except Exception:
        den = cv2.GaussianBlur(gray, (5, 5), 0)

    variants.append(("otsu", cv2.threshold(den, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]))
    variants.append(("otsu_inv", cv2.threshold(den, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]))
    variants.append(
        ("ath", cv2.adaptiveThreshold(den, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 41, 5))
    )
    variants.append(
        ("ath_inv", cv2.adaptiveThreshold(den, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 41, 5))
    )

    def is_squareish(quad: np.ndarray) -> bool:
        quad = _order_quad(quad)
        # side lengths
        sides = np.linalg.norm(np.roll(quad, -1, axis=0) - quad, axis=1)
        if np.any(sides < 10):
            return False
        ratio = float(sides.max() / sides.min())
        if ratio > 1.8:
            return False

        # area constraints: not too tiny, not too huge
        area = cv2.contourArea(quad.reshape(-1, 1, 2).astype(np.float32))
        if area < 0.002 * (H * W):
            return False
        if area > 0.95 * (H * W):
            return False

        return True

    for tag, bw in variants:
        # edge/contour extraction
        cnts, _hier = cv2.findContours(bw, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        # prefer larger contours first
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:200]

        for c in cnts:
            area = cv2.contourArea(c)
            if area < 2000:
                continue

            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            if len(approx) != 4:
                continue

            if not cv2.isContourConvex(approx):
                continue

            quad = approx.reshape(-1, 2).astype(np.float32)

            # Keep only square-ish quads
            if not is_squareish(quad):
                continue

            quads.append(quad)

        if quads:
            _dbg("contour_quads: tag=%s quads=%d", tag, len(quads))

    # Deduplicate by centroid
    uniq: List[np.ndarray] = []
    seen: set[Tuple[int, int]] = set()
    for q in quads:
        c = q.mean(axis=0)
        key = (int(c[0] // 25), int(c[1] // 25))
        if key in seen:
            continue
        seen.add(key)
        uniq.append(q)

    return uniq[:12]  # bound


def _try_wechat(gray: np.ndarray) -> List[QRResult]:
    """
    Try OpenCV WeChat QRCode detector if available (opencv-contrib).
    We keep this as best-effort: if not installed, returns [].

    Note: different OpenCV builds expose this under different symbols.
    """
    # Try a few possible constructors
    wc = None
    try:
        if hasattr(cv2, "wechat_qrcode_WeChatQRCode"):
            wc = cv2.wechat_qrcode_WeChatQRCode()  # type: ignore[attr-defined]
        elif hasattr(cv2, "wechat_qrcode") and hasattr(cv2.wechat_qrcode, "WeChatQRCode"):
            wc = cv2.wechat_qrcode.WeChatQRCode()  # type: ignore[attr-defined]
    except Exception as e:
        _dbg("wechat: init failed: %s", e)
        wc = None

    if wc is None:
        return []

    # detectAndDecode can return:
    # - list[str], points
    # - or a single string depending on version
    try:
        out = wc.detectAndDecode(gray)
    except Exception as e:
        _dbg("wechat: detectAndDecode failed: %s", e)
        return []

    payloads: List[str] = []
    points = None

    try:
        # Most common: (list[str], points)
        if isinstance(out, tuple) and len(out) >= 1:
            payloads = out[0] if isinstance(out[0], (list, tuple)) else [out[0]]
            points = out[1] if len(out) > 1 else None
        else:
            payloads = [str(out)]
    except Exception:
        payloads = []

    results: List[QRResult] = []
    if not payloads:
        return results

    # points is often (N,4,2)
    if points is not None:
        pts_arr = np.asarray(points, dtype=np.float32)
        if pts_arr.ndim == 3 and pts_arr.shape[1:] == (4, 2):
            for i, p in enumerate(payloads[: pts_arr.shape[0]]):
                q = pts_arr[i]
                xs = q[:, 0]
                ys = q[:, 1]
                x0, y0, x1, y1 = int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())
                bbox = (x0, y0, max(1, x1 - x0), max(1, y1 - y0))
                results.append(QRResult(payload=p, bbox=bbox, corners=q, method="wechat"))
            return results

    # If we have no points, still return payload(s)
    for p in payloads:
        if p:
            results.append(QRResult(payload=p, bbox=None, corners=None, method="wechat"))
    return results


def _run_decoders_on_patch(
    gray_patch: np.ndarray,
    *,
    best: Dict[str, QRResult],
    method_prefix: str,
    origin_xy: Optional[Tuple[int, int]] = None,
    quad_in_full: Optional[np.ndarray] = None,
) -> None:
    """
    Feed a patch through your strongest decoders:
      - ZXing on cleaned variants (usually best)
      - ZXing raw
      - pyzbar fast
      - OpenCV single/multi/curved
    Optionally map bbox/corners back to full image coordinates when origin_xy is provided.
    """
    ox, oy = origin_xy if origin_xy is not None else (0, 0)

    # 1) zxing on cleaned variants
    for tag, cleaned in cleanup_variants(gray_patch):
        zhits = decode_zxing(cleaned, method=f"{method_prefix}_clean_{tag}")
        for r in zhits:
            mapped_bbox = None
            mapped_corners = None

            if r.bbox:
                bx, by, bw, bh = r.bbox
                mapped_bbox = (ox + bx, oy + by, bw, bh)

            if r.corners is not None:
                mapped_corners = r.corners.copy()
                mapped_corners[:, 0] += ox
                mapped_corners[:, 1] += oy
            elif quad_in_full is not None:
                mapped_corners = quad_in_full.copy()

            _consider(
                best,
                QRResult(
                    payload=r.payload,
                    bbox=mapped_bbox,
                    corners=mapped_corners,
                    method=f"{method_prefix}_clean_{tag}",
                ),
            )

    # 2) zxing raw on patch
    zhits = decode_zxing(gray_patch, method=f"{method_prefix}_full")
    for r in zhits:
        mapped_bbox = None
        mapped_corners = None

        if r.bbox:
            bx, by, bw, bh = r.bbox
            mapped_bbox = (ox + bx, oy + by, bw, bh)

        if r.corners is not None:
            mapped_corners = r.corners.copy()
            mapped_corners[:, 0] += ox
            mapped_corners[:, 1] += oy
        elif quad_in_full is not None:
            mapped_corners = quad_in_full.copy()

        _consider(
            best,
            QRResult(
                payload=r.payload,
                bbox=mapped_bbox,
                corners=mapped_corners,
                method=f"{method_prefix}_full",
            ),
        )

    # 3) pyzbar fast on patch
    hits = decode_pyzbar_fast(gray_patch)
    for r in hits:
        mapped_bbox = None
        mapped_corners = None

        if r.bbox:
            bx, by, bw, bh = r.bbox
            mapped_bbox = (ox + bx, oy + by, bw, bh)

        if r.corners is not None:
            mapped_corners = r.corners.copy()
            mapped_corners[:, 0] += ox
            mapped_corners[:, 1] += oy
        elif quad_in_full is not None:
            mapped_corners = quad_in_full.copy()

        _consider(
            best,
            QRResult(
                payload=r.payload,
                bbox=mapped_bbox,
                corners=mapped_corners,
                method=f"{method_prefix}_pyzbar",
            ),
        )

    # 4) OpenCV decode on patch
    det = cv2.QRCodeDetector()
    for r in decode_multi(gray_patch, det=det):
        _consider(best, r)
    for r in decode_single(gray_patch, det=det):
        _consider(best, r)
    for r in decode_curved(gray_patch, det=det):
        _consider(best, r)


def scan_qr_anywhere(image_path: str, *, max_results: int = 8) -> List[QRResult]:
    """
    "State of the art" practical pipeline for real phone images, including:
      - EXIF orientation fix (critical for modern phone shots)
      - WeChatQRCode (opencv-contrib) if available
      - Detect-first localization → warp → decode (robust against stylized QRs / noisy backgrounds)
      - Your existing decode-first stages (pyzbar, zxing cleaned variants, OpenCV)
      - Tiling fallback

    This stays fully offline and uses best-available local detectors.
    """
    img = _imread_exif_fixed(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    H, W = gray.shape[:2]

    _dbg("scan: image_path=%s max_results=%d", image_path, max_results)
    _dbg("scan: loaded image shape=%s gray_shape=%s", getattr(img, "shape", None), getattr(gray, "shape", None))

    best: Dict[str, QRResult] = {}

    # ------------------------------------------------------------
    # 0) WeChat QR (opencv-contrib): often best on real-world photos
    # ------------------------------------------------------------
    _dbg("stage 0: wechat (opencv-contrib) on full image (if available)")
    whits = _try_wechat(gray)
    _dbg("stage 0: wechat hit(s)=%d", len(whits))
    for r in whits:
        _consider(best, r)
    if best:
        return _ordered(best, max_results)

    # ------------------------------------------------------------
    # 1) Detect-first: localize quad(s) → warp → decode
    #    This is the missing piece for stylized / low-quiet-zone / noisy backgrounds.
    # ------------------------------------------------------------
    _dbg("stage 1: detect-first quad localization (opencv detector)")
    quads = _quads_from_opencv_detector(gray)
    _dbg("stage 1: opencv quads=%d", len(quads))

    # If OpenCV didn't find any quads, fall back to contour proposals
    if not quads:
        _dbg("stage 1b: contour-based quad proposals")
        quads = _quads_from_contours(gray)
        _dbg("stage 1b: contour quads=%d", len(quads))

    # Try a few warp sizes; stylized codes sometimes decode better at larger size
    warp_sizes = (640, 768, 960)

    for qi, q in enumerate(quads[:10]):  # bound
        for sz in warp_sizes:
            try:
                warped = _warp_quad(gray, q, size=sz)
            except Exception as e:
                _dbg("warp failed (qi=%d sz=%d): %s", qi, sz, e)
                continue

            _dbg("stage 1: warped quad qi=%d size=%d", qi, sz)

            # Try WeChat on the warped patch too (often helps when full image fails)
            whits = _try_wechat(warped)
            _dbg("stage 1: wechat warped hit(s)=%d", len(whits))
            for r in whits:
                # WeChat points are in warped coords; but we still keep payload as high-quality signal
                _consider(best, QRResult(payload=r.payload, bbox=r.bbox, corners=r.corners, method="wechat_warp"))
            if best:
                return _ordered(best, max_results)

            # Now run strong decode suite on warped patch
            _run_decoders_on_patch(
                warped,
                best=best,
                method_prefix="zxing_warp",
                origin_xy=None,
                quad_in_full=q,
            )
            if best:
                return _ordered(best, max_results)

    # ------------------------------------------------------------
    # 2) pyzbar (fast + good on standard, crisp images)
    # ------------------------------------------------------------
    _dbg("stage 2: pyzbar_fast on full image")
    hits = decode_pyzbar_fast(gray)
    _dbg("stage 2: pyzbar_fast hit(s)=%d", len(hits))
    for r in hits:
        _consider(best, r)
    if best:
        return _ordered(best, max_results)

    # ------------------------------------------------------------
    # 3) ZXing on cleaned variants (remove junk / binarize / normalize)
    # ------------------------------------------------------------
    _dbg("stage 3: zxing on cleaned variants")
    for tag, cleaned in cleanup_variants(gray):
        zhits = decode_zxing(cleaned, method=f"zxing_clean_{tag}")
        _dbg("  zxing_clean_%s hit(s)=%d", tag, len(zhits))
        for r in zhits:
            _consider(best, r)
        if best:
            return _ordered(best, max_results)

    # ------------------------------------------------------------
    # 4) OpenCV full image paths
    # ------------------------------------------------------------
    _dbg("stage 4: OpenCV multi/single/curved")
    det = cv2.QRCodeDetector()

    for r in decode_multi(gray, det=det):
        _consider(best, r)
    for r in decode_single(gray, det=det):
        _consider(best, r)
    for r in decode_curved(gray, det=det):
        _consider(best, r)

    if best:
        return _ordered(best, max_results)

    # ------------------------------------------------------------
    # 5) ZXing on raw full image
    # ------------------------------------------------------------
    _dbg("stage 5: zxing on raw full image")
    zhits = decode_zxing(gray, method="zxing_full")
    _dbg("stage 5: zxing_full hit(s)=%d", len(zhits))
    for r in zhits:
        _consider(best, r)
    if best:
        return _ordered(best, max_results)

    # ------------------------------------------------------------
    # 6) Tiling fallback (last resort)
    # ------------------------------------------------------------
    _dbg("stage 6: tiling fallback")
    tile, overlap = _tile_params(H, W)
    step = max(1, tile - overlap)
    _dbg("tiling: tile=%d overlap=%d step=%d", tile, overlap, step)

    for y in range(0, H, step):
        for x in range(0, W, step):
            crop = gray[y : y + tile, x : x + tile]
            if crop.size == 0:
                continue

            # WeChat on tile (cheap-ish, and can surprise you)
            whits = _try_wechat(crop)
            for r in whits:
                _consider(best, QRResult(payload=r.payload, bbox=r.bbox, corners=r.corners, method="wechat_tile"))
            if best:
                return _ordered(best, max_results)

            # Try cleanup + ZXing on the tile (strong)
            for tag, cleaned in cleanup_variants(crop):
                for r in decode_zxing(cleaned, method=f"zxing_tile_{tag}"):
                    mapped_bbox = None
                    mapped_corners = None
                    if r.bbox:
                        bx, by, bw, bh = r.bbox
                        mapped_bbox = (x + bx, y + by, bw, bh)
                    if r.corners is not None:
                        mapped_corners = r.corners.copy()
                        mapped_corners[:, 0] += x
                        mapped_corners[:, 1] += y
                    _consider(
                        best,
                        QRResult(
                            payload=r.payload,
                            bbox=mapped_bbox,
                            corners=mapped_corners,
                            method=f"zxing_tile_{tag}",
                        ),
                    )

                if best:
                    return _ordered(best, max_results)

    _dbg("scan: FAILED - no QR decoded after all stages")
    return _ordered(best, max_results)


def decode_first(image_path: str) -> str:
    hits = scan_qr_anywhere(image_path, max_results=1)
    if not hits:
        raise QRDecodeError("No QR code found.")
    return hits[0].payload
