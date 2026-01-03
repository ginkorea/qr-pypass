from __future__ import annotations

import json
import os
import time
from urllib.request import Request, urlopen
from urllib.parse import urlencode

BASE = os.environ.get("QRPYPASS_BASE", "http://127.0.0.1:5000")


def post_json(path: str, obj: dict) -> dict:
    data = json.dumps(obj).encode("utf-8")
    req = Request(BASE + path, data=data, headers={"Content-Type": "application/json"}, method="POST")
    with urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))


def get_json(path: str, params: dict | None = None) -> dict:
    url = BASE + path
    if params:
        url += "?" + urlencode(params)
    req = Request(url, method="GET")
    with urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))


def main():
    print("[health]", get_json("/health"))

    # 1) generate a TOTP provisioning URI + import it
    gen = post_json("/gen/payload", {
        "kind": "totp",
        "params": {
            "issuer": "QRPYPASS",
            "account_name": "verify-test@local",
            "digits": 6,
            "period": 30,
            "algorithm": "SHA1",
            "nbytes": 20
        },
        "import": True,
        "passphrase": None
    })
    print("[gen] kind:", gen["generated"]["kind"])
    print("[gen] uri (prefix):", gen["generated"]["payload"][:60] + "...")
    acc = gen.get("imported") or {}
    acc_id = acc.get("id")
    print("[import] id:", acc_id)

    # 2) list accounts
    lst = get_json("/auth/list")
    print("[list] count:", lst["count"])

    # 3) fetch current code
    code_resp = get_json("/auth/code", {"id": acc_id})
    code = code_resp["code"]
    remaining = code_resp["seconds_remaining"]
    print("[code] code:", code, "remaining:", remaining)

    # 4) verify the code
    ver = post_json("/auth/verify", {"id": acc_id, "code": code, "window": 1})
    print("[verify] ok:", ver["ok"], "matched_offset:", ver["matched_offset"])

    # 5) negative test: wrong code
    bad = post_json("/auth/verify", {"id": acc_id, "code": "000000", "window": 1})
    print("[verify-bad] ok:", bad["ok"], "matched_offset:", bad["matched_offset"])

    print("DONE")


if __name__ == "__main__":
    main()
