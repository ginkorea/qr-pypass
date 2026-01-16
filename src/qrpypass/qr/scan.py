from __future__ import annotations

from typing import Dict, List, Optional, Tuple, Iterable
import cv2
import numpy as np

from .decode import decode_multi, decode_single, QRDecodeError
from .models import QRResult


def _bbox_area(b: Optional[Tuple[int, int, int, int]]) -> int:
    if not b:
        return 10**18
    _, _, w, h = b
    return int(w) * int(h)


def _method_rank(method: str) -> int:
    """
    Lower is better.
    Prefer:
      - full-image multi
      - full-image multi with preprocessing
      - full-image single
      - full-image single with preprocessing
      - tiles (multi then single, then with preprocessing)
    """
    m = (method or "").lower()

    if m == "multi":
        return 0
    if m.startswith("multi:"):
        return 1
    if m == "single":
        return 2
    if m.startswith("single:"):
        return 3
    if m == "tile_multi":
        return 4
    if m.startswith("tile_multi:"):
        return 5
    if m == "tile":
        return 6
    if m.startswith("tile:"):
        return 7
    return 9


def _better(a: QRResult, b: QRResult) -> QRResult:
    """
    Return the better of two results for the same payload.
    Priority:
      1) method rank
      2) has bbox/corners
      3) smaller bbox area (tighter localization tends to be more accurate)
    """
    ra, rb = _method_rank(a.method), _method_rank(b.method)
    if ra != rb:
        return a if ra < rb else b

    a_has = (a.bbox is not None) + (a.corners is not None)
    b_has = (b.bbox is not None) + (b.corners is not None)
    if a_has != b_has:
        return a if a_has > b_has else b

    return a if _bbox_area(a.bbox) <= _bbox_area(b.bbox) else b


def _clahe(gray: np.ndarray) -> np.ndarray:
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    return clahe.apply(gray)


def _denoise(gray: np.ndarray) -> np.ndarray:
    # Helps with glossy noise / compression speckle
    return cv2.fastNlMeansDenoising(gray, None, h=12, templateWindowSize=7, searchWindowSize=21)


def _sharpen(gray: np.ndarray) -> np.ndarray:
    k = np.array([[0, -1, 0],
                  [-1, 5, -1],
                  [0, -1, 0]], dtype=np.float32)
    return cv2.filter2D(gray, -1, k)


def _adaptive_thresh(gray: np.ndarray, block: int = 31, c: int = 2) -> np.ndarray:
    block = int(block)
    if block % 2 == 0:
        block += 1
    block = max(9, min(block, 101))
    return cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        block, int(c)
    )


def _otsu(gray: np.ndarray) -> np.ndarray:
    _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th


def _morph_clean(bin_img: np.ndarray) -> np.ndarray:
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    closed = cv2.morphologyEx(bin_img, cv2.MORPH_CLOSE, k, iterations=1)
    opened = cv2.morphologyEx(closed, cv2.MORPH_OPEN, k, iterations=1)
    return opened


def _resize(gray: np.ndarray, scale: float) -> np.ndarray:
    if scale == 1.0:
        return gray
    h, w = gray.shape[:2]
    nh, nw = max(40, int(h * scale)), max(40, int(w * scale))
    interp = cv2.INTER_AREA if scale < 1.0 else cv2.INTER_CUBIC
    return cv2.resize(gray, (nw, nh), interpolation=interp)


def _variants(gray: np.ndarray) -> Iterable[Tuple[str, np.ndarray]]:
    """
    Preprocess variants ordered from cheap/natural to more aggressive.
    These materially improve decode rates for stylized / low-contrast / glossy signage QRs.
    """
    gray = gray.astype(np.uint8, copy=False)

    # baseline
    yield ("gray", gray)

    # contrast normalize
    g1 = _clahe(gray)
    yield ("clahe", g1)

    # denoise + clahe (often helps glossy signs)
    g2 = _clahe(_denoise(gray))
    yield ("dn_clahe", g2)

    # sharpen (recover slight blur)
    g3 = _sharpen(g1)
    yield ("sharpen", g3)

    # thresholding (big win for “not quite black” modules)
    ath = _morph_clean(_adaptive_thresh(g1, block=31, c=2))
    yield ("ath", ath)
    yield ("ath_inv", cv2.bitwise_not(ath))

    otsu = _morph_clean(_otsu(g1))
    yield ("otsu", otsu)
    yield ("otsu_inv", cv2.bitwise_not(otsu))

    # scale tricks
    yield ("up125", _resize(gray, 1.25))

    # downscale -> upscale (noise suppression)
    half = _resize(gray, 0.5)
    half_up = _resize(half, gray.shape[0] / max(1, half.shape[0]))
    yield ("dsus", half_up)


def _decode_on_variants(gray: np.ndarray, *, prefix: str) -> List[QRResult]:
    """
    Run OpenCV QR decoders across multiple preprocessing variants.
    """
    out: List[QRResult] = []

    for tag, v in _variants(gray):
        v2 = v
        if v2.ndim != 2:
            v2 = cv2.cvtColor(v2, cv2.COLOR_BGR2GRAY)
        if v2.dtype != np.uint8:
            v2 = v2.astype(np.uint8, copy=False)

        # multi first
        for r in decode_multi(v2):
            out.append(QRResult(payload=r.payload, corners=r.corners, bbox=r.bbox, method=f"{prefix}_multi:{tag}"))

        # then single
        for r in decode_single(v2):
            out.append(QRResult(payload=r.payload, corners=r.corners, bbox=r.bbox, method=f"{prefix}_single:{tag}"))

        # Early exit heuristic to keep runtime sane
        if out and tag in {"gray", "clahe", "ath", "otsu"}:
            break

    return out


def scan_qr_anywhere(image_path: str, *, max_results: int = 8) -> List[QRResult]:
    img = cv2.imread(image_path)
    if img is None:
        raise QRDecodeError(f"Image could not be read: {image_path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Collect best result per payload
    best: Dict[str, QRResult] = {}

    def consider(r: QRResult):
        if not r.payload:
            return
        cur = best.get(r.payload)
        best[r.payload] = r if cur is None else _better(cur, r)

    # 1) Try full image first (fast path)
    for r in decode_multi(gray):
        consider(r)
    for r in decode_single(gray):
        consider(r)

    # 1b) Try full-image preprocessing battery
    if not best:
        for r in _decode_on_variants(gray, prefix="full"):
            consider(r)

    if best:
        ordered = sorted(best.values(), key=lambda r: (_method_rank(r.method), _bbox_area(r.bbox)))
        return ordered[:max_results]

    # 2) Fallback tiling for large images / tough cases
    h, w = gray.shape
    tile = 900
    overlap = 220
    step = max(1, tile - overlap)

    for y in range(0, h, step):
        for x in range(0, w, step):
            crop = gray[y:y + tile, x:x + tile]
            if crop.size == 0:
                continue

            # tile raw first
            for r in decode_multi(crop):
                mapped_bbox = None
                mapped_corners = None

                if r.bbox:
                    bx, by, bw, bh = r.bbox
                    mapped_bbox = (x + bx, y + by, bw, bh)

                if r.corners is not None:
                    mapped_corners = r.corners.copy()
                    mapped_corners[:, 0] += x
                    mapped_corners[:, 1] += y

                consider(QRResult(payload=r.payload, corners=mapped_corners, bbox=mapped_bbox, method="tile_multi"))

            for r in decode_single(crop):
                mapped_bbox = None
                mapped_corners = None

                if r.bbox:
                    bx, by, bw, bh = r.bbox
                    mapped_bbox = (x + bx, y + by, bw, bh)

                if r.corners is not None:
                    mapped_corners = r.corners.copy()
                    mapped_corners[:, 0] += x
                    mapped_corners[:, 1] += y

                consider(QRResult(payload=r.payload, corners=mapped_corners, bbox=mapped_bbox, method="tile"))

            # If still nothing overall, try variants on tiles (expensive; do it only when needed)
            if not best:
                tile_var_hits = _decode_on_variants(crop, prefix="tile")
                for rr in tile_var_hits:
                    mapped_bbox = None
                    mapped_corners = None

                    if rr.bbox:
                        bx, by, bw, bh = rr.bbox
                        mapped_bbox = (x + bx, y + by, bw, bh)

                    if rr.corners is not None:
                        mapped_corners = rr.corners.copy()
                        mapped_corners[:, 0] += x
                        mapped_corners[:, 1] += y

                    consider(QRResult(payload=rr.payload, corners=mapped_corners, bbox=mapped_bbox, method=rr.method))

            if len(best) >= max_results:
                ordered = sorted(best.values(), key=lambda r: (_method_rank(r.method), _bbox_area(r.bbox)))
                return ordered[:max_results]

    ordered = sorted(best.values(), key=lambda r: (_method_rank(r.method), _bbox_area(r.bbox)))
    return ordered[:max_results]


def decode_first(image_path: str) -> str:
    hits = scan_qr_anywhere(image_path, max_results=1)
    if not hits:
        raise QRDecodeError("No QR code found.")
    return hits[0].payload
