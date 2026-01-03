from __future__ import annotations

import io
import os
import tempfile

import qrcode
from flask import Flask, jsonify, request, render_template, send_file

from qrpypass.qr import scan_and_classify
from qrpypass.generate import generate_payload

from qrpypass.auth import (
    parse_otpauth_uri,
    totp_now,
    totp_verify,
    load_accounts,
    save_accounts,
    StoreError,
    OTPAuthError,
)


def create_app() -> Flask:
    # Ensure Flask can always locate templates/static in this package
    here = os.path.dirname(__file__)
    templates_dir = os.path.join(here, "templates")
    static_dir = os.path.join(here, "static")

    app = Flask(
        __name__,
        template_folder=templates_dir,
        static_folder=static_dir,
        static_url_path="/static",
    )

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/gen")
    def gen_page():
        return render_template("gen.html")

    @app.get("/health")
    def health():
        return jsonify({"ok": True})

    @app.post("/scan")
    def scan():
        """
        multipart/form-data:
          file: (image) required
          max_results: optional int
        """
        if "file" not in request.files:
            return jsonify({"error": "missing form file field 'file'"}), 400

        f = request.files["file"]
        if not f.filename:
            return jsonify({"error": "empty filename"}), 400

        max_results = request.form.get("max_results", "8")
        try:
            max_results_i = int(max_results)
            if not (1 <= max_results_i <= 50):
                return jsonify({"error": "max_results must be between 1 and 50"}), 400
        except ValueError:
            return jsonify({"error": "max_results must be an integer"}), 400

        suffix = os.path.splitext(f.filename)[1].lower() or ".img"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp_path = tmp.name
            f.save(tmp_path)

        try:
            hits = scan_and_classify(tmp_path, max_results=max_results_i)
            return jsonify({"count": len(hits), "results": [h.to_dict() for h in hits]})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            try:
                os.remove(tmp_path)
            except Exception:
                pass

    @app.get("/auth/list")
    def auth_list():
        passphrase = request.args.get("passphrase")  # optional
        try:
            accounts = load_accounts(passphrase=passphrase)
            return jsonify(
                {"count": len(accounts), "accounts": [a.safe_dict() for a in accounts.values()]}
            )
        except StoreError as e:
            return jsonify({"error": str(e)}), 400

    @app.post("/auth/import")
    def auth_import():
        """
        JSON:
          { "otpauth_uri": "...", "passphrase": "optional" }
        """
        data = request.get_json(silent=True) or {}
        uri = (data.get("otpauth_uri") or "").strip()
        passphrase = data.get("passphrase")

        if not uri:
            return jsonify({"error": "Missing otpauth_uri"}), 400

        try:
            acc = parse_otpauth_uri(uri)
        except OTPAuthError as e:
            return jsonify({"error": str(e)}), 400

        try:
            accounts = load_accounts(passphrase=passphrase)
            accounts[acc.id] = acc
            save_accounts(accounts, passphrase=passphrase)
        except StoreError as e:
            return jsonify({"error": str(e)}), 400

        return jsonify({"imported": acc.safe_dict()})

    @app.get("/auth/code")
    def auth_code():
        """
        Query:
          id=<account_id>&passphrase=optional
        """
        acc_id = (request.args.get("id") or "").strip()
        passphrase = request.args.get("passphrase")

        if not acc_id:
            return jsonify({"error": "Missing id"}), 400

        try:
            accounts = load_accounts(passphrase=passphrase)
        except StoreError as e:
            return jsonify({"error": str(e)}), 400

        acc = accounts.get(acc_id)
        if not acc:
            return jsonify({"error": "Unknown id"}), 404

        code, remaining = totp_now(acc)
        return jsonify({"account": acc.safe_dict(), "code": code, "seconds_remaining": remaining})

    @app.post("/auth/verify")
    def auth_verify():
        """
        JSON:
          { "id": "<account_id>", "code": "123456", "window": 1, "passphrase": "optional" }

        Returns:
          { ok: bool, matched_offset: int, account: {...} }
        """
        data = request.get_json(silent=True) or {}
        acc_id = (data.get("id") or "").strip()
        code = (data.get("code") or "").strip()
        passphrase = data.get("passphrase")

        try:
            window = int(data.get("window", 1))
        except Exception:
            return jsonify({"error": "window must be an integer"}), 400

        if not acc_id:
            return jsonify({"error": "Missing id"}), 400
        if not code:
            return jsonify({"error": "Missing code"}), 400

        try:
            accounts = load_accounts(passphrase=passphrase)
        except StoreError as e:
            return jsonify({"error": str(e)}), 400

        acc = accounts.get(acc_id)
        if not acc:
            return jsonify({"error": "Unknown id"}), 404

        try:
            ok, offset = totp_verify(acc, code, window=window)
        except Exception as e:
            return jsonify({"error": str(e)}), 400

        return jsonify({"ok": ok, "matched_offset": offset, "account": acc.safe_dict()})

    @app.post("/gen/payload")
    def gen_payload_api():
        """
        JSON:
          { "kind": "url|text|totp", "params": {...}, "import": false, "passphrase": "optional" }

        For totp: if import=true, store into authenticator store.
        """
        data = request.get_json(silent=True) or {}
        kind = (data.get("kind") or "").strip()
        params = data.get("params", {}) or {}

        do_import = bool(data.get("import", False))
        passphrase = data.get("passphrase")

        try:
            gp = generate_payload(kind, params)
        except Exception as e:
            return jsonify({"error": str(e)}), 400

        imported = None
        if do_import and gp.kind.value == "otpauth_totp":
            try:
                acc = parse_otpauth_uri(gp.payload)
                accounts = load_accounts(passphrase=passphrase)
                accounts[acc.id] = acc
                save_accounts(accounts, passphrase=passphrase)
                imported = acc.safe_dict()
            except (OTPAuthError, StoreError) as e:
                return jsonify({"error": str(e)}), 400

        return jsonify({"generated": gp.to_dict(), "imported": imported})

    @app.post("/gen/qr")
    def gen_qr():
        """
        JSON: { "payload": "string", "box_size": 8, "border": 2 }
        Returns: image/png
        """
        data = request.get_json(silent=True) or {}
        payload = (data.get("payload") or "").strip()
        if not payload:
            return jsonify({"error": "payload is required"}), 400

        try:
            box_size = int(data.get("box_size", 8))
            border = int(data.get("border", 2))
        except ValueError:
            return jsonify({"error": "box_size and border must be integers"}), 400

        if not (2 <= box_size <= 20):
            return jsonify({"error": "box_size must be between 2 and 20"}), 400
        if not (0 <= border <= 10):
            return jsonify({"error": "border must be between 0 and 10"}), 400

        qr = qrcode.QRCode(box_size=box_size, border=border)
        qr.add_data(payload)
        qr.make(fit=True)

        img = qr.make_image()
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        return send_file(buf, mimetype="image/png")

    return app
