from __future__ import annotations

from typing import Dict, List, Optional, Tuple
import os
import logging

import cv2
import numpy as np
from PIL import Image, ImageOps

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

_LOG = logging.getLogger("qrpypass.qr")
_DEBUG = os.getenv("QRPYPASS_QR_DEBUG", "").strip().lower() in ("1", "true", "yes", "on")


def _init_logging() -> None:
    if not _LOG.handlers:
        logging.basicConfig(level=logging.DEBUG if _DEBUG else logging.INFO)
    if _DEBUG:
        _LOG.setLevel(logging.DEBUG)

    # Pillow is extremely noisy when root logger is DEBUG.
    logging.getLogger("PIL").setLevel(logging.WARNING)
    logging.getLogger("PIL.TiffImagePlugin").setLevel(logging.WARNING)


_init_logging()


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
    Lower is better. Order reflects practical “SOTA in the wild”:
    WeChatQRCode > ZXing(cleaned) > pyzbar > OpenCV > ZXing(raw) > warps/tiles.
    """
    m = (method or "").lower()

    if m.startswith("wechat"):
        return 0

    if m.startswith("zxing_clean"):
        return 1

    if m.startswith("pyzbar"):
        return 2

    if m in ("multi", "single", "curved"):
        return 3

    if m.startswith("zxing_full"):
        return 4

    if m.startswith("wechat_warp") or m.startswith("zxing_warp") or m.startswith("opencv_warp"):
        return 5

    if m.startswith("zxing_tile") or m.startswith("wechat_tile") or m.startswith("opencv_tile"):
        return 6

    return 9


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


def _load_image_bgr_exif(image_path: str) -> np.ndarray:
    """
    Always honor EXIF orientation. This matters for phone photos where
    Orientation=6 is common (90deg rotation).
    """
    try:
        im = Image.open(image_path)
    except Exception as e:
        raise QRDecodeError(f"Image could not be read: {image_path} ({e})")

    try:
        im = ImageOps.exif_transpose(im)
    except Exception:
        # If exif is broken or missing, just continue.
        pass

    im = im.convert("RGB")
    arr = np.array(im)  # RGB uint8
    bgr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
    return bgr


# ---------------------------------------------------------------------
# WeChat QRCode (OpenCV contrib)
# ---------------------------------------------------------------------
def _wechat_detector():
    ctor = getattr(cv2, "wechat_qrcode_WeChatQRCode", None)
    if ctor is None:
        return None
    try:
        # In opencv-contrib-python wheels this works without passing model paths.
        return ctor()
    except Exception:
        return None


def _decode_wechat(det, bgr: np.ndarray, *, method: str = "wechat") -> List[QRResult]:
    if det is None or bgr is None:
        return []
    try:
        texts, points = det.detectAndDecode(bgr)
    except Exception:
        return []

    if texts is None:
        return []
    if isinstance(texts, str):
        texts = [texts]

    out: List[QRResult] = []
    for i, payload in enumerate(texts):
        if not payload:
            continue

        pts_i = None
        if points is not None and len(points) > i:
            pts_i = points[i]

        corners = None
        bbox = None
        if pts_i is not None:
            corners = np.asarray(pts_i, dtype=float).reshape(-1, 2)
            x1 = float(np.min(corners[:, 0]))
            y1 = float(np.min(corners[:, 1]))
            x2 = float(np.max(corners[:, 0]))
            y2 = float(np.max(corners[:, 1]))
            bbox = (int(round(x1)), int(round(y1)), int(round(max(1.0, x2 - x1))), int(round(max(1.0, y2 - y1))))

        out.append(QRResult(payload=str(payload), corners=corners, bbox=bbox, method=method))
    return out


# ---------------------------------------------------------------------
# Quad warp fallback: find likely QR square and unskew it
# ---------------------------------------------------------------------
def _order_quad(pts: np.ndarray) -> np.ndarray:
    pts = np.asarray(pts, dtype=np.float32).reshape(4, 2)
    s = pts.sum(axis=1)
    d = np.diff(pts, axis=1).reshape(-1)
    tl = pts[np.argmin(s)]
    br = pts[np.argmax(s)]
    tr = pts[np.argmin(d)]
    bl = pts[np.argmax(d)]
    return np.stack([tl, tr, br, bl], axis=0)


def _warp_from_quad(gray: np.ndarray, quad: np.ndarray, size: int = 900) -> np.ndarray:
    quad = _order_quad(quad)
    dst = np.array([[0, 0], [size - 1, 0], [size - 1, size - 1], [0, size - 1]], dtype=np.float32)
    M = cv2.getPerspectiveTransform(quad.astype(np.float32), dst)
    return cv2.warpPerspective(gray, M, (size, size), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)


def _find_candidate_quads(gray: np.ndarray, *, max_quads: int = 6) -> List[np.ndarray]:
    """
    Heuristic: find large-ish 4-point contours that could be a QR boundary.
    This does not “decode”, it only finds a plausible square so we can warp.
    """
    g = gray
    if g.ndim == 3:
        g = cv2.cvtColor(g, cv2.COLOR_BGR2GRAY)

    # Edge emphasis
    blur = cv2.GaussianBlur(g, (5, 5), 0)
    edges = cv2.Canny(blur, 60, 160)
    edges = cv2.dilate(edges, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=1)

    cnts, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    H, W = g.shape[:2]
    img_area = float(H * W)

    quads: List[Tuple[float, np.ndarray]] = []
    for c in cnts:
        area = cv2.contourArea(c)
        if area < 0.01 * img_area:
            continue
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) != 4:
            continue
        if not cv2.isContourConvex(approx):
            continue

        pts = approx.reshape(4, 2).astype(np.float32)

        # Squareness check (loose)
        quad = _order_quad(pts)
        def _dist(a, b): return float(np.linalg.norm(a - b))
        w1 = _dist(quad[0], quad[1])
        w2 = _dist(quad[3], quad[2])
        h1 = _dist(quad[0], quad[3])
        h2 = _dist(quad[1], quad[2])
        w = (w1 + w2) / 2.0
        h = (h1 + h2) / 2.0
        if min(w, h) <= 0:
            continue
        aspect = max(w, h) / min(w, h)
        if aspect > 1.35:
            continue

        # Prefer bigger quads
        score = area
        quads.append((score, quad))

    quads.sort(key=lambda t: t[0], reverse=True)
    return [q for _, q in quads[:max_quads]]


def _tile_params(h: int, w: int) -> Tuple[int, int]:
    tile = 1100 if max(h, w) >= 3000 else 900
    overlap = 260
    return tile, overlap


def scan_qr_anywhere(image_path: str, *, max_results: int = 8) -> List[QRResult]:
    bgr = _load_image_bgr_exif(image_path)
    if bgr is None:
        raise QRDecodeError(f"Image could not be read: {image_path}")

    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    H, W = gray.shape[:2]

    _dbg("scan: image_path=%s max_results=%d", image_path, max_results)
    _dbg("scan: loaded image shape=%s gray_shape=%s", getattr(bgr, "shape", None), getattr(gray, "shape", None))

    best: Dict[str, QRResult] = {}

    # ------------------------------------------------------------
    # 0) WeChatQRCode on full image (SOTA for messy/stylized codes)
    # ------------------------------------------------------------
    wechat = _wechat_detector()
    if wechat is not None:
        _dbg("stage 0: wechat (opencv-contrib) on full image (if available)")
        hits = _decode_wechat(wechat, bgr, method="wechat")
        _dbg("stage 0: wechat hit(s)=%d", len(hits))
        for r in hits:
            _consider(best, r)
        if best:
            return _ordered(best, max_results)

    # ------------------------------------------------------------
    # 0.5) OpenCV QRCodeDetector (baseline)
    # ------------------------------------------------------------
    _dbg("stage 0.5: OpenCV QRCodeDetector on full image")
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
    # 1) ZXing on cleaned variants (junk removal)
    # ------------------------------------------------------------
    _dbg("stage 1: zxing on cleaned variants")
    for tag, cleaned in cleanup_variants(gray):
        zhits = decode_zxing(cleaned, method=f"zxing_clean_{tag}")
        _dbg("  zxing_clean_%s hit(s)=%d", tag, len(zhits))
        for r in zhits:
            _consider(best, r)
        if best:
            return _ordered(best, max_results)

    # ------------------------------------------------------------
    # 2) pyzbar fallback (fast; can hit some cases)
    # ------------------------------------------------------------
    _dbg("stage 2: pyzbar_fast on full image")
    hits = decode_pyzbar_fast(gray)
    _dbg("stage 2: pyzbar_fast hit(s)=%d", len(hits))
    for r in hits:
        _consider(best, r)
    if best:
        return _ordered(best, max_results)

    # ------------------------------------------------------------
    # 3) ZXing on raw full image
    # ------------------------------------------------------------
    _dbg("stage 3: zxing on raw full image")
    zhits = decode_zxing(gray, method="zxing_full")
    _dbg("stage 3: zxing_full hit(s)=%d", len(zhits))
    for r in zhits:
        _consider(best, r)
    if best:
        return _ordered(best, max_results)

    # ------------------------------------------------------------
    # 4) Quad warp fallback (try to detect the square and flatten it)
    # ------------------------------------------------------------
    _dbg("stage 4: quad-warp fallback")
    quads = _find_candidate_quads(gray, max_quads=6)
    _dbg("stage 4: quad candidates=%d", len(quads))

    for qi, quad in enumerate(quads):
        warped = _warp_from_quad(gray, quad, size=900)
        warped_bgr = cv2.cvtColor(warped, cv2.COLOR_GRAY2BGR)

        if wechat is not None:
            wh = _decode_wechat(wechat, warped_bgr, method=f"wechat_warp_{qi}")
            _dbg("  wechat_warp_%d hit(s)=%d", qi, len(wh))
            for r in wh:
                _consider(best, r)
            if best:
                return _ordered(best, max_results)

        # Run ZXing on cleaned warp (often very effective)
        for tag, cleaned in cleanup_variants(warped):
            zwh = decode_zxing(cleaned, method=f"zxing_warp_{qi}_{tag}")
            for r in zwh:
                _consider(best, r)
            if best:
                return _ordered(best, max_results)

        # OpenCV on warp as well
        for r in decode_multi(warped, det=det):
            _consider(best, QRResult(payload=r.payload, corners=r.corners, bbox=r.bbox, method=f"opencv_warp_{qi}_multi"))
        for r in decode_single(warped, det=det):
            _consider(best, QRResult(payload=r.payload, corners=r.corners, bbox=r.bbox, method=f"opencv_warp_{qi}_single"))
        for r in decode_curved(warped, det=det):
            _consider(best, QRResult(payload=r.payload, corners=r.corners, bbox=r.bbox, method=f"opencv_warp_{qi}_curved"))
        if best:
            return _ordered(best, max_results)

    # ------------------------------------------------------------
    # 5) Tiling fallback (last resort)
    # ------------------------------------------------------------
    _dbg("stage 5: tiling fallback")
    tile, overlap = _tile_params(H, W)
    step = max(1, tile - overlap)
    _dbg("tiling: tile=%d overlap=%d step=%d", tile, overlap, step)

    for y in range(0, H, step):
        for x in range(0, W, step):
            crop = gray[y : y + tile, x : x + tile]
            if crop.size == 0:
                continue

            # Strongest tile approach: cleaned ZXing
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
                    _consider(best, QRResult(payload=r.payload, bbox=mapped_bbox, corners=mapped_corners, method=f"zxing_tile_{tag}"))

                if best:
                    return _ordered(best, max_results)

            # Optional: tile OpenCV baseline
            for r in decode_multi(crop, det=det):
                if not r.payload:
                    continue
                bbox = None
                corners = None
                if r.bbox:
                    bx, by, bw, bh = r.bbox
                    bbox = (x + bx, y + by, bw, bh)
                if r.corners is not None:
                    corners = r.corners.copy()
                    corners[:, 0] += x
                    corners[:, 1] += y
                _consider(best, QRResult(payload=r.payload, bbox=bbox, corners=corners, method="opencv_tile_multi"))

            if best:
                return _ordered(best, max_results)

    _dbg("scan: FAILED - no QR decoded after all stages")
    return _ordered(best, max_results)


def decode_first(image_path: str) -> str:
    hits = scan_qr_anywhere(image_path, max_results=1)
    if not hits:
        raise QRDecodeError("No QR code found.")
    return hits[0].payload
