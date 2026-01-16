from __future__ import annotations

from typing import List, Optional, Tuple

import cv2
import numpy as np

from .models import QRResult


class QRDecodeError(RuntimeError):
    pass


def _ensure_gray_u8(img: np.ndarray) -> np.ndarray:
    if img is None:
        return img
    if img.ndim == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if img.dtype != np.uint8:
        # Clip if needed (e.g., float images)
        if np.issubdtype(img.dtype, np.floating):
            img = np.clip(img, 0, 255).astype(np.uint8)
        else:
            img = img.astype(np.uint8, copy=False)
    return img


def _points_to_bbox(points: Optional[np.ndarray]) -> Optional[Tuple[int, int, int, int]]:
    if points is None:
        return None
    pts = np.asarray(points, dtype=float).reshape(-1, 2)
    if pts.size == 0:
        return None
    x1 = float(np.min(pts[:, 0]))
    y1 = float(np.min(pts[:, 1]))
    x2 = float(np.max(pts[:, 0]))
    y2 = float(np.max(pts[:, 1]))
    return (
        int(round(x1)),
        int(round(y1)),
        int(round(max(1.0, x2 - x1))),
        int(round(max(1.0, y2 - y1))),
    )


# ---------------------------------------------------------------------
# pyzbar / zbar
# ---------------------------------------------------------------------
try:
    from pyzbar.pyzbar import decode as _zbar_decode  # type: ignore
    from pyzbar.pyzbar import ZBarSymbol  # type: ignore

    _HAS_PYZBAR = True
except Exception:
    _HAS_PYZBAR = False
    _zbar_decode = None
    ZBarSymbol = None


def _decode_pyzbar(gray: np.ndarray, *, method: str) -> List[QRResult]:
    if not _HAS_PYZBAR or gray is None:
        return []
    gray = _ensure_gray_u8(gray)

    try:
        symbols = [ZBarSymbol.QRCODE] if ZBarSymbol is not None else None
        results = _zbar_decode(gray, symbols=symbols)  # type: ignore[arg-type]
    except Exception:
        return []

    out: List[QRResult] = []
    for r in results or []:
        if getattr(r, "type", None) != "QRCODE":
            continue

        data = getattr(r, "data", b"") or b""
        payload = data.decode("utf-8", errors="replace") if isinstance(data, (bytes, bytearray)) else str(data)

        rect = getattr(r, "rect", None)
        bbox = None
        if rect is not None:
            bbox = (int(rect.left), int(rect.top), int(rect.width), int(rect.height))

        poly = getattr(r, "polygon", None)
        corners = None
        if poly:
            pts = [(float(p.x), float(p.y)) for p in poly]
            if len(pts) >= 4:
                corners = np.asarray(pts[:4], dtype=float)

        out.append(QRResult(payload=payload, corners=corners, bbox=bbox, method=method))

    return out


# ---------------------------------------------------------------------
# OpenCV QRCodeDetector
# ---------------------------------------------------------------------
_DETECTOR = cv2.QRCodeDetector()


def decode_multi(gray: np.ndarray, *, det: Optional[cv2.QRCodeDetector] = None) -> List[QRResult]:
    if gray is None:
        return []
    gray = _ensure_gray_u8(gray)
    detector = det or _DETECTOR

    try:
        ok, decoded_info, points, _ = detector.detectAndDecodeMulti(gray)
    except Exception:
        return []

    if not ok or not decoded_info:
        return []

    out: List[QRResult] = []
    for i, payload in enumerate(decoded_info):
        if not payload:
            continue
        pts_i = None
        if points is not None and len(points) > i:
            pts_i = points[i]
        corners = None
        if pts_i is not None:
            corners = np.asarray(pts_i, dtype=float).reshape(-1, 2)
        bbox = _points_to_bbox(pts_i)
        out.append(QRResult(payload=str(payload), corners=corners, bbox=bbox, method="multi"))
    return out


def decode_single(gray: np.ndarray, *, det: Optional[cv2.QRCodeDetector] = None) -> List[QRResult]:
    if gray is None:
        return []
    gray = _ensure_gray_u8(gray)
    detector = det or _DETECTOR

    try:
        data, points, _ = detector.detectAndDecode(gray)
    except Exception:
        return []

    if not data:
        return []

    corners = None
    if points is not None:
        corners = np.asarray(points, dtype=float).reshape(-1, 2)
    bbox = _points_to_bbox(points)
    return [QRResult(payload=str(data), corners=corners, bbox=bbox, method="single")]


def decode_curved(gray: np.ndarray, *, det: Optional[cv2.QRCodeDetector] = None) -> List[QRResult]:
    if gray is None:
        return []
    gray = _ensure_gray_u8(gray)
    detector = det or _DETECTOR
    fn = getattr(detector, "detectAndDecodeCurved", None)
    if fn is None:
        return []
    try:
        data, points, _ = fn(gray)
    except Exception:
        return []
    if not data:
        return []
    corners = None
    if points is not None:
        corners = np.asarray(points, dtype=float).reshape(-1, 2)
    bbox = _points_to_bbox(points)
    return [QRResult(payload=str(data), corners=corners, bbox=bbox, method="curved")]


# ---------------------------------------------------------------------
# ZXing C++ backend (strong fallback)
# ---------------------------------------------------------------------
try:
    import zxingcpp  # type: ignore

    _HAS_ZXING = True
except Exception:
    zxingcpp = None
    _HAS_ZXING = False


def decode_zxing(gray: np.ndarray, *, max_symbols: int = 16, method: str = "zxing") -> List[QRResult]:
    if not _HAS_ZXING or gray is None:
        return []
    gray = _ensure_gray_u8(gray)

    try:
        # Keep API-compatible: zxingcpp.read_barcodes(image) works across versions.
        hits = zxingcpp.read_barcodes(gray)  # type: ignore[attr-defined]
    except Exception:
        return []

    out: List[QRResult] = []
    for h in hits[:max_symbols]:
        fmt = getattr(h, "format", None)
        if fmt is not None and "qr" not in str(fmt).lower():
            continue
        payload = getattr(h, "text", "") or ""
        if not payload:
            continue

        bbox = None
        corners = None
        pos = getattr(h, "position", None)
        if pos is not None:
            pts = []
            for key in ("top_left", "top_right", "bottom_right", "bottom_left"):
                p = getattr(pos, key, None)
                if p is not None:
                    pts.append((float(p.x), float(p.y)))
            if len(pts) == 4:
                corners = np.asarray(pts, dtype=float)
                bbox = _points_to_bbox(corners)

        out.append(QRResult(payload=payload, corners=corners, bbox=bbox, method=method))
    return out


# ---------------------------------------------------------------------
# Junk removal / cleanup variants (generic)
# ---------------------------------------------------------------------
def cleanup_variants(gray: np.ndarray) -> List[Tuple[str, np.ndarray]]:
    """
    Produce a small, bounded set of cleaned images intended to remove
    stylization "junk" and make a QR look like a normal binary module grid.

    Keep this cheap: no big loops, no huge parameter sweeps.
    """
    g = _ensure_gray_u8(gray)
    out: List[Tuple[str, np.ndarray]] = []

    # A) slight denoise helps thresholding
    dn = cv2.fastNlMeansDenoising(g, None, h=10, templateWindowSize=7, searchWindowSize=21)
    out.append(("dn", dn))

    # B) Otsu binarize (and invert)
    _, th = cv2.threshold(dn, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    out.append(("otsu", th))
    out.append(("otsu_inv", cv2.bitwise_not(th)))

    # C) Adaptive threshold (and invert)
    ath = cv2.adaptiveThreshold(
        dn, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 2
    )
    out.append(("ath", ath))
    out.append(("ath_inv", cv2.bitwise_not(ath)))

    # D) Morphology to “square up” rounded modules / fill logos a bit
    k3 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    k5 = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

    # close fills gaps / suppresses logo holes
    out.append(("otsu_close3", cv2.morphologyEx(th, cv2.MORPH_CLOSE, k3, iterations=1)))
    out.append(("otsu_close5", cv2.morphologyEx(th, cv2.MORPH_CLOSE, k5, iterations=1)))

    # open removes speckle
    out.append(("ath_open3", cv2.morphologyEx(ath, cv2.MORPH_OPEN, k3, iterations=1)))

    # E) A “strong cleanup” variant: close then open on inverted binary
    inv = cv2.bitwise_not(th)
    strong = cv2.morphologyEx(inv, cv2.MORPH_CLOSE, k5, iterations=2)
    strong = cv2.morphologyEx(strong, cv2.MORPH_OPEN, k3, iterations=1)
    out.append(("strong_inv", strong))

    return out


# ---------------------------------------------------------------------
# High-level attempt helpers
# ---------------------------------------------------------------------
def decode_pyzbar_fast(gray: np.ndarray) -> List[QRResult]:
    if gray is None or not _HAS_PYZBAR:
        return []
    g = _ensure_gray_u8(gray)

    for tag, img in [("gray", g), ("blur3", cv2.GaussianBlur(g, (3, 3), 0))]:
        hits = _decode_pyzbar(img, method=f"pyzbar_{tag}")
        if hits:
            return hits

    # Try cleaned variants (bounded set)
    for tag, img in cleanup_variants(g):
        hits = _decode_pyzbar(img, method=f"pyzbar_clean_{tag}")
        if hits:
            return hits

    return []
