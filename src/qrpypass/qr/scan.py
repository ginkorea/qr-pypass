from __future__ import annotations
from typing import List, Optional
import cv2
import numpy as np
from .decode import decode_multi, decode_single, QRDecodeError
from .models import QRResult

def scan_qr_anywhere(image_path: str, *, max_results: int = 8) -> List[QRResult]:
    img = cv2.imread(image_path)
    if img is None:
        raise QRDecodeError("Image could not be read.")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    results = []
    # try full image first
    hits = decode_multi(gray) + decode_single(gray)
    if hits:
        return hits[:max_results]

    # fallback tiling for large images
    h, w = gray.shape
    tile = 900
    overlap = 200
    step = tile - overlap
    for y in range(0, h, step):
        for x in range(0, w, step):
            crop = gray[y:y+tile, x:x+tile]
            for r in decode_multi(crop) + decode_single(crop):
                # map bbox to original space
                if r.bbox:
                    bx, by, bw, bh = r.bbox
                    mapped_bbox = (x+bx, y+by, bw, bh)
                else:
                    mapped_bbox = None
                if r.corners is not None:
                    mapped_corners = r.corners.copy()
                    mapped_corners[:,0] += x
                    mapped_corners[:,1] += y
                else:
                    mapped_corners = None

                results.append(QRResult(
                    payload=r.payload,
                    corners=mapped_corners,
                    bbox=mapped_bbox,
                    method="tile"
                ))
                if len(results) >= max_results:
                    return results
    return results
