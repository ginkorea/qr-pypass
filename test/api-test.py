#!/usr/bin/env python3
"""
End-to-end API test for qr-pypass.

Tests:
  - /gen/payload (url, text, totp)
  - /gen/qr (render payload -> PNG)
  - /scan (decode PNG -> payload + classification)
  - /auth/import, /auth/list, /auth/code (TOTP store + code generation)

No third-party deps required (uses urllib).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Tuple
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote


# ----------------------------
# HTTP helpers (urllib only)
# ----------------------------

def http_json(method: str, url: str, payload: Dict[str, Any] | None = None, timeout: int = 20) -> Tuple[int, Dict[str, Any]]:
    data = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = Request(url, data=data, headers=headers, method=method.upper())
    try:
        with urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            status = resp.status
    except Exception as e:
        raise RuntimeError(f"HTTP error calling {method} {url}: {e}") from e

    try:
        return status, json.loads(raw.decode("utf-8", "ignore") or "{}")
    except Exception:
        return status, {"_raw": raw.decode("utf-8", "ignore")}


def http_get_bytes(url: str, timeout: int = 20) -> bytes:
    req = Request(url, headers={"Accept": "*/*"}, method="GET")
    with urlopen(req, timeout=timeout) as resp:
        return resp.read()


def http_post_bytes(url: str, body: bytes, content_type: str, timeout: int = 20) -> Tuple[int, bytes, Dict[str, str]]:
    req = Request(url, data=body, headers={"Content-Type": content_type}, method="POST")
    with urlopen(req, timeout=timeout) as resp:
        return resp.status, resp.read(), dict(resp.headers.items())


def multipart_form(fields: Dict[str, str], files: Dict[str, Tuple[str, bytes, str]]) -> Tuple[bytes, str]:
    """
    Build multipart/form-data body.

    fields: {"max_results": "8"}
    files: {"file": ("name.png", b"...", "image/png")}
    """
    boundary = "----qrpypass-" + uuid.uuid4().hex
    crlf = b"\r\n"
    parts = []

    for k, v in fields.items():
        parts.append(b"--" + boundary.encode("ascii"))
        parts.append(f'Content-Disposition: form-data; name="{k}"'.encode("utf-8"))
        parts.append(b"")
        parts.append(v.encode("utf-8"))

    for field_name, (filename, content, mime) in files.items():
        parts.append(b"--" + boundary.encode("ascii"))
        parts.append(
            f'Content-Disposition: form-data; name="{field_name}"; filename="{filename}"'.encode("utf-8")
        )
        parts.append(f"Content-Type: {mime}".encode("utf-8"))
        parts.append(b"")
        parts.append(content)

    parts.append(b"--" + boundary.encode("ascii") + b"--")
    parts.append(b"")

    body = crlf.join(parts)
    content_type = f"multipart/form-data; boundary={boundary}"
    return body, content_type


# ----------------------------
# Test logic
# ----------------------------

@dataclass
class Generated:
    kind: str
    payload: str
    meta: Dict[str, Any]


def assert_ok(status: int, data: Dict[str, Any], ctx: str) -> None:
    if not (200 <= status < 300):
        raise RuntimeError(f"{ctx} failed: HTTP {status} :: {data}")


def gen_payload(base: str, kind: str, params: Dict[str, Any], do_import: bool = False, passphrase: str | None = None) -> Tuple[Generated, Dict[str, Any] | None]:
    status, data = http_json(
        "POST",
        f"{base}/gen/payload",
        {"kind": kind, "params": params, "import": do_import, "passphrase": passphrase},
    )
    assert_ok(status, data, f"/gen/payload ({kind})")
    g = data.get("generated") or {}
    gp = Generated(kind=g.get("kind", ""), payload=g.get("payload", ""), meta=g.get("meta") or {})
    imported = data.get("imported")
    return gp, imported


def gen_qr_png(base: str, payload: str, box_size: int = 8, border: int = 2) -> bytes:
    status, raw, headers = http_post_bytes(
        f"{base}/gen/qr",
        body=json.dumps({"payload": payload, "box_size": box_size, "border": border}).encode("utf-8"),
        content_type="application/json",
    )
    if status < 200 or status >= 300:
        try:
            msg = raw.decode("utf-8", "ignore")
        except Exception:
            msg = str(raw[:200])
        raise RuntimeError(f"/gen/qr failed: HTTP {status} :: {msg}")
    ctype = headers.get("Content-Type", "")
    if "image/png" not in ctype:
        raise RuntimeError(f"/gen/qr expected image/png, got {ctype}")
    return raw


def scan_png(base: str, png_bytes: bytes, *, max_results: int = 8) -> Dict[str, Any]:
    body, ctype = multipart_form(
        fields={"max_results": str(max_results)},
        files={"file": ("generated.png", png_bytes, "image/png")},
    )
    status, raw, _headers = http_post_bytes(f"{base}/scan", body=body, content_type=ctype)
    try:
        data = json.loads(raw.decode("utf-8", "ignore") or "{}")
    except Exception:
        data = {"_raw": raw.decode("utf-8", "ignore")}
    assert_ok(status, data, "/scan")
    return data


def auth_import(base: str, otpauth_uri: str, passphrase: str | None = None) -> Dict[str, Any]:
    status, data = http_json("POST", f"{base}/auth/import", {"otpauth_uri": otpauth_uri, "passphrase": passphrase})
    assert_ok(status, data, "/auth/import")
    return data


def auth_list(base: str, passphrase: str | None = None) -> Dict[str, Any]:
    qs = ""
    if passphrase:
        qs = "?" + urlencode({"passphrase": passphrase})
    status, data = http_json("GET", f"{base}/auth/list{qs}", None)
    assert_ok(status, data, "/auth/list")
    return data


def auth_code(base: str, acc_id: str, passphrase: str | None = None) -> Dict[str, Any]:
    q = {"id": acc_id}
    if passphrase:
        q["passphrase"] = passphrase
    url = f"{base}/auth/code?{urlencode(q)}"
    status, data = http_json("GET", url, None)
    assert_ok(status, data, "/auth/code")
    return data


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="http://127.0.0.1:5000", help="Base URL, e.g. http://127.0.0.1:5000")
    ap.add_argument("--outdir", default="api_test_out", help="Where to write generated PNGs")
    ap.add_argument("--passphrase", default="", help="Optional store passphrase (encrypts store at rest)")
    ap.add_argument("--import-on-generate", action="store_true", help="Use /gen/payload import=true for TOTP instead of /auth/import")
    args = ap.parse_args()

    base = args.base.rstrip("/")
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    passphrase = args.passphrase.strip() or None

    # Health
    status, health = http_json("GET", f"{base}/health", None)
    assert_ok(status, health, "/health")
    print("[OK] health:", health)

    # ---------------- URL test ----------------
    url_target = "https://github.com/ginkorea/qr-pypass"
    gp_url, _ = gen_payload(base, "url", {"url": url_target})
    print("[OK] generated URL payload")
    png_url = gen_qr_png(base, gp_url.payload)
    (outdir / "url.png").write_bytes(png_url)
    scan_url = scan_png(base, png_url, max_results=5)
    decoded_url = (scan_url.get("results") or [{}])[0].get("classification", {}).get("raw", "")
    if decoded_url != gp_url.payload:
        raise RuntimeError(f"URL mismatch:\n  generated={gp_url.payload}\n  decoded={decoded_url}")
    print("[OK] url -> qr -> scan roundtrip")

    # ---------------- TEXT test ----------------
    text_target = f"hello from qr-pypass at {time.time()}"
    gp_text, _ = gen_payload(base, "text", {"text": text_target})
    print("[OK] generated TEXT payload")
    png_text = gen_qr_png(base, gp_text.payload)
    (outdir / "text.png").write_bytes(png_text)
    scan_text = scan_png(base, png_text, max_results=5)
    decoded_text = (scan_text.get("results") or [{}])[0].get("classification", {}).get("raw", "")
    if decoded_text != gp_text.payload:
        raise RuntimeError(f"TEXT mismatch:\n  generated={gp_text.payload}\n  decoded={decoded_text}")
    print("[OK] text -> qr -> scan roundtrip")

    # ---------------- TOTP test ----------------
    issuer = "QRPYPASS"
    account_name = f"test-{uuid.uuid4().hex[:8]}@local"
    do_import = bool(args.import_on_generate)

    gp_totp, imported = gen_payload(
        base,
        "totp",
        {"issuer": issuer, "account_name": account_name, "digits": 6, "period": 30, "algorithm": "SHA1", "nbytes": 20},
        do_import=do_import,
        passphrase=passphrase,
    )
    print("[OK] generated TOTP otpauth payload")

    png_totp = gen_qr_png(base, gp_totp.payload)
    (outdir / "totp.png").write_bytes(png_totp)

    scan_totp = scan_png(base, png_totp, max_results=5)
    decoded_totp = (scan_totp.get("results") or [{}])[0].get("classification", {}).get("raw", "")
    if decoded_totp != gp_totp.payload:
        raise RuntimeError(f"TOTP URI mismatch:\n  generated={gp_totp.payload}\n  decoded={decoded_totp}")
    print("[OK] totp -> qr -> scan roundtrip")

    if not do_import:
        # Import via auth endpoint
        imp = auth_import(base, gp_totp.payload, passphrase=passphrase)
        imported = imp.get("imported")
        print("[OK] imported TOTP via /auth/import")
    else:
        print("[OK] imported TOTP via /gen/payload import=true")

    if not imported or not imported.get("id"):
        raise RuntimeError(f"Import did not return an account id: {imported}")

    acc_id = imported["id"]

    # List accounts
    listing = auth_list(base, passphrase=passphrase)
    ids = [a.get("id") for a in (listing.get("accounts") or [])]
    if acc_id not in ids:
        raise RuntimeError(f"Imported account id not found in /auth/list. id={acc_id} ids={ids}")
    print("[OK] /auth/list contains imported account")

    # Get TOTP code
    code_resp = auth_code(base, acc_id, passphrase=passphrase)
    code = code_resp.get("code")
    rem = code_resp.get("seconds_remaining")
    if not code or not str(code).isdigit():
        raise RuntimeError(f"Bad TOTP code returned: {code_resp}")
    print(f"[OK] /auth/code => {code} (seconds_remaining={rem})")

    print("\nAll tests passed.")
    print(f"Artifacts written to: {outdir.resolve()}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise
    except Exception as e:
        print("\n[FAIL]", e, file=sys.stderr)
        raise SystemExit(2)
