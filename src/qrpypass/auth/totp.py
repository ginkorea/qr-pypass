from __future__ import annotations

import base64
import hashlib
import hmac
import struct
import time
from typing import Tuple

from .models import OTPAuthAccount


def _b32decode(secret_b32: str) -> bytes:
    # base64.b32decode is strict about padding; we can pad ourselves.
    s = secret_b32.strip().replace(" ", "").upper()
    pad = (-len(s)) % 8
    s += "=" * pad
    return base64.b32decode(s, casefold=True)


def _hash_for_alg(alg: str):
    alg = (alg or "SHA1").upper()
    if alg == "SHA1":
        return hashlib.sha1
    if alg == "SHA256":
        return hashlib.sha256
    if alg == "SHA512":
        return hashlib.sha512
    raise ValueError(f"Unsupported algorithm: {alg}")


def totp_now(account: OTPAuthAccount, *, now: int | None = None) -> Tuple[str, int]:
    """
    Returns (code, seconds_remaining).
    """
    if now is None:
        now = int(time.time())

    period = int(account.period)
    counter = now // period
    remaining = period - (now % period)

    key = _b32decode(account.secret_b32)
    msg = struct.pack(">Q", counter)
    digestmod = _hash_for_alg(account.algorithm)

    hm = hmac.new(key, msg, digestmod).digest()

    # dynamic truncation
    offset = hm[-1] & 0x0F
    part = hm[offset:offset + 4]
    dbc = struct.unpack(">I", part)[0] & 0x7FFFFFFF

    code_int = dbc % (10 ** int(account.digits))
    code = str(code_int).zfill(int(account.digits))
    return code, remaining
