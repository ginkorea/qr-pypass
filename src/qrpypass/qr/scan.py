from __future__ import annotations

from typing import Dict, List, Optional, Tuple
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
)
from .models import QRResult


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
    Lower is better. Keep "cheap first" and "strong last".
    """
    m = (method or "").lower()
    if m.startswith("pyzbar"):
        return 0
    if m == "multi":
        return 1
    if m == "single":
        return 2
    if m == "curved":
        return 3
    if m.startswith("zxing"):
        return 4
    if m.startswith("tile_pyzbar"):
        return 5
    if m.startswith("tile_"):
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


def _tile_params(h: int, w: int) -> Tuple[int, int]:
    """
    Choose a tile size that is large enough for most QRs but not insane.
    """
    # Most phone photos: 3000x4000. QRs often 250-1200px wide.
    # 900 tiles are fine, but we can go a bit bigger to reduce loops.
    tile = 1100 if max(h, w) >= 3000 else 900
    overlap = 260
    return tile, overlap


def scan_qr_anywhere(image_path: str, *, max_results: int = 8) -> List[QRResult]:
    img = cv2.imread(image_path)
    if img is None:
        raise QRDecodeError(f"Image could not be read: {image_path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    H, W = gray.shape[:2]

    _dbg("scan: image_path=%s max_results=%d", image_path, max_results)
    _dbg("scan: loaded image shape=%s gray_shape=%s", getattr(img, "shape", None), getattr(gray, "shape", None))

    best: Dict[str, QRResult] = {}

    # ------------------------------------------------------------
    # Stage 1: pyzbar fast on full image (cheapest + often best)
    # ------------------------------------------------------------
    _dbg("stage 1: pyzbar_fast on full image")
    hits = decode_pyzbar_fast(gray)
    _dbg("stage 1: pyzbar_fast returned %d hit(s)", len(hits))
    for r in hits:
        _consider(best, r)
    if best:
        return _ordered(best, max_results)

    # ------------------------------------------------------------
    # Stage 2: OpenCV multi + single
    # ------------------------------------------------------------
    _dbg("stage 2: OpenCV detectAndDecodeMulti/single on full image")
    det = cv2.QRCodeDetector()

    hits = decode_multi(gray, det=det)
    _dbg("stage 2: OpenCV multi hit(s)=%d", len(hits))
    for r in hits:
        _consider(best, r)

    hits = decode_single(gray, det=det)
    _dbg("stage 2: OpenCV single hit(s)=%d", len(hits))
    for r in hits:
        _consider(best, r)

    if best:
        return _ordered(best, max_results)

    # ------------------------------------------------------------
    # Stage 3: OpenCV curved path (helps with perspective/warp)
    # ------------------------------------------------------------
    _dbg("stage 3: OpenCV curved decode on full image")
    hits = decode_curved(gray, det=det)
    _dbg("stage 3: OpenCV curved hit(s)=%d", len(hits))
    for r in hits:
        _consider(best, r)
    if best:
        return _ordered(best, max_results)

    # ------------------------------------------------------------
    # Stage 4: ZXing full image (strong C++ fallback)
    # ------------------------------------------------------------
    _dbg("stage 4: zxing on full image (if installed)")
    hits = decode_zxing(gray, method="zxing_full")
    _dbg("stage 4: zxing_full hit(s)=%d", len(hits))
    for r in hits:
        _consider(best, r)
    if best:
        return _ordered(best, max_results)

    # ------------------------------------------------------------
    # Stage 5: Tiling fallback (only now; this is the CPU-heavy step)
    #   Order per tile:
    #     - pyzbar_fast
    #     - OpenCV multi/single
    #     - zxing
    # ------------------------------------------------------------
    _dbg("stage 5: tiling fallback (no hits on full image)")
    tile, overlap = _tile_params(H, W)
    step = max(1, tile - overlap)

    _dbg("tiling: tile=%d overlap=%d step=%d", tile, overlap, step)

    for y in range(0, H, step):
        for x in range(0, W, step):
            crop = gray[y : y + tile, x : x + tile]
            if crop.size == 0:
                continue

            # pyzbar on crop
            for r in decode_pyzbar_fast(crop):
                mapped_bbox = None
                mapped_corners = None
                if r.bbox:
                    bx, by, bw, bh = r.bbox
                    mapped_bbox = (x + bx, y + by, bw, bh)
                if r.corners is not None:
                    mapped_corners = r.corners.copy()
                    mapped_corners[:, 0] += x
                    mapped_corners[:, 1] += y
                _consider(best, QRResult(payload=r.payload, bbox=mapped_bbox, corners=mapped_corners, method=f"tile_pyzbar"))

            # OpenCV on crop
            for r in decode_multi(crop, det=det):
                mapped_bbox = None
                mapped_corners = None
                if r.bbox:
                    bx, by, bw, bh = r.bbox
                    mapped_bbox = (x + bx, y + by, bw, bh)
                if r.corners is not None:
                    mapped_corners = r.corners.copy()
                    mapped_corners[:, 0] += x
                    mapped_corners[:, 1] += y
                _consider(best, QRResult(payload=r.payload, bbox=mapped_bbox, corners=mapped_corners, method="tile_multi"))

            for r in decode_single(crop, det=det):
                mapped_bbox = None
                mapped_corners = None
                if r.bbox:
                    bx, by, bw, bh = r.bbox
                    mapped_bbox = (x + bx, y + by, bw, bh)
                if r.corners is not None:
                    mapped_corners = r.corners.copy()
                    mapped_corners[:, 0] += x
                    mapped_corners[:, 1] += y
                _consider(best, QRResult(payload=r.payload, bbox=mapped_bbox, corners=mapped_corners, method="tile_single"))

            # ZXing on crop (last)
            for r in decode_zxing(crop, method="zxing_tile"):
                mapped_bbox = None
                mapped_corners = None
                if r.bbox:
                    bx, by, bw, bh = r.bbox
                    mapped_bbox = (x + bx, y + by, bw, bh)
                if r.corners is not None:
                    mapped_corners = r.corners.copy()
                    mapped_corners[:, 0] += x
                    mapped_corners[:, 1] += y
                _consider(best, QRResult(payload=r.payload, bbox=mapped_bbox, corners=mapped_corners, method="zxing_tile"))

            if len(best) >= max_results:
                return _ordered(best, max_results)

    if not best:
        _dbg("scan: FAILED - no QR decoded after all stages")

    return _ordered(best, max_results)


def decode_first(image_path: str) -> str:
    hits = scan_qr_anywhere(image_path, max_results=1)
    if not hits:
        raise QRDecodeError("No QR code found.")
    return hits[0].payload
