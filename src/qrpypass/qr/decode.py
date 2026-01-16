from __future__ import annotations

"""
QR decoding backends.

Goal:
- Cheap first, heavy last.
- Add a robust C++ backend (ZXing) for cases where OpenCV + zbar miss entirely.

Backends:
  1) pyzbar/zbar (if installed)
  2) OpenCV QRCodeDetector: multi + single
  3) OpenCV detectAndDecodeCurved (often helps on perspective/warped photos)
  4) zxing-cpp (C++ ZXing) (very strong fallback)
"""

from typing import List, Optional, Tuple

import cv2
import numpy as np

from .models import QRResult


class QRDecodeError(RuntimeError):
    pass


# ---------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------
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


def _ensure_gray_u8(img: np.ndarray) -> np.ndarray:
    if img is None:
        return img
    if img.ndim == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if img.dtype != np.uint8:
        img = img.astype(np.uint8, copy=False)
    return img


# ---------------------------------------------------------------------
# Optional: pyzbar / zbar
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
        try:
            payload = data.decode("utf-8", errors="replace")
        except Exception:
            payload = str(data)

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


def decode_pyzbar_fast(gray: np.ndarray) -> List[QRResult]:
    """
    Fast, low-CPU pyzbar attempts.
    """
    if gray is None or not _HAS_PYZBAR:
        return []
    gray = _ensure_gray_u8(gray)

    hits = _decode_pyzbar(gray, method="pyzbar_gray")
    if hits:
        return hits

    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    hits = _decode_pyzbar(blur, method="pyzbar_blur3")
    if hits:
        return hits

    try:
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8)).apply(gray)
        hits = _decode_pyzbar(clahe, method="pyzbar_clahe")
        if hits:
            return hits
    except Exception:
        pass

    try:
        sharp = cv2.addWeighted(gray, 1.5, cv2.GaussianBlur(gray, (0, 0), 1.0), -0.5, 0)
        hits = _decode_pyzbar(sharp, method="pyzbar_sharp")
        if hits:
            return hits
    except Exception:
        pass

    return []


# ---------------------------------------------------------------------
# OpenCV detector (reused)
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
    """
    OpenCV curved decode path. Can help when the QR is perspective-warped or curved.
    Not all OpenCV builds expose this; we guard it safely.
    """
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
# Optional: ZXing C++ backend
# ---------------------------------------------------------------------
try:
    import zxingcpp  # type: ignore

    _HAS_ZXING = True
except Exception:
    zxingcpp = None
    _HAS_ZXING = False


def decode_zxing(gray: np.ndarray, *, max_symbols: int = 16, method: str = "zxing") -> List[QRResult]:
    """
    Robust C++ QR decode via zxing-cpp.
    Works well when OpenCV/zbar fail to even detect.
    """
    if not _HAS_ZXING or gray is None:
        return []

    gray = _ensure_gray_u8(gray)

    try:
        # returns list of Barcodes
        hits = zxingcpp.read_barcodes(gray)  # type: ignore[attr-defined]
    except Exception:
        return []

    out: List[QRResult] = []
    for h in hits[:max_symbols]:
        fmt = getattr(h, "format", None)
        if fmt is not None and str(fmt).lower().find("qr") == -1:
            # Keep it strict: only QR
            continue

        payload = getattr(h, "text", "") or ""
        if not payload:
            continue

        # position may exist; best-effort bbox/corners
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
