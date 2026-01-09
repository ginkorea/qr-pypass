from __future__ import annotations

import io
import os
import tempfile

import qrcode
from flask import Flask, jsonify, request, render_template, send_file, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from PIL import Image

from qrpypass.qr import scan_and_classify
from qrpypass.generate import generate_payload
from qrpypass.auth import (
    parse_otpauth_uri,
    totp_now,
    totp_verify,
    OTPAuthError,
)

from .db import (
    init_db,
    authenticate,
    create_user,
    get_user_by_id,
    upsert_totp_account,
    list_totp_accounts,
    get_totp_account,
    delete_totp_account,
)


def create_app() -> Flask:
    here = os.path.dirname(__file__)
    templates_dir = os.path.join(here, "templates")
    static_dir = os.path.join(here, "static")

    app = Flask(
        __name__,
        template_folder=templates_dir,
        static_folder=static_dir,
        static_url_path="/static",
    )

    # Required for sessions (set in env on PythonAnywhere / WSGI)
    app.secret_key = os.environ.get("QRPYPASS_SECRET_KEY", "dev-unsafe-change-me")

    # Upload size limit (e.g. 6 MB)
    app.config["MAX_CONTENT_LENGTH"] = int(
        os.environ.get("QRPYPASS_MAX_UPLOAD_BYTES", str(6 * 1024 * 1024))
    )

    # Rate limiting
    limiter = Limiter(get_remote_address, app=app, default_limits=["200 per hour"])

    # DB init
    init_db()

    # Login setup
    login_mgr = LoginManager()
    login_mgr.login_view = "login"
    login_mgr.init_app(app)

    @login_mgr.user_loader
    def load_user(user_id: str):
        try:
            return get_user_by_id(int(user_id))
        except Exception:
            return None

    @app.get("/login")
    def login():
        return render_template("login.html")

    @app.post("/login")
    @limiter.limit("10 per minute")
    def login_post():
        email = (request.form.get("email") or "").strip()
        password = (request.form.get("password") or "").strip()
        u = authenticate(email, password)
        if not u:
            return render_template("login.html", error="Invalid email/password"), 401
        login_user(u)
        return redirect(url_for("vault"))

    @app.get("/register")
    def register():
        return render_template("register.html")

    @app.post("/register")
    @limiter.limit("5 per minute")
    def register_post():
        email = (request.form.get("email") or "").strip()
        password = (request.form.get("password") or "").strip()
        try:
            u = create_user(email, password)
        except Exception as e:
            return render_template("register.html", error=str(e)), 400
        login_user(u)
        return redirect(url_for("vault"))

    @app.get("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("login"))

    @app.get("/")
    @login_required
    def index():
        return render_template("index.html")

    @app.get("/vault")
    @login_required
    def vault():
        return render_template("vault.html")

    @app.get("/gen")
    @login_required
    def gen_page():
        return render_template("gen.html")

    @app.get("/health")
    def health():
        return jsonify({"ok": True})

    # ---------- helpers ----------
    def _reject_huge_images(path: str) -> None:
        # Prevent decompression bomb / giant images
        with Image.open(path) as im:
            w, h = im.size
            max_dim = int(os.environ.get("QRPYPASS_MAX_IMAGE_DIM", "6000"))
            if w > max_dim or h > max_dim:
                raise ValueError(f"Image too large ({w}x{h}); max dimension is {max_dim}")

    # ---------- SCAN ----------
    @app.post("/scan")
    @login_required
    @limiter.limit("30 per minute")
    def scan():
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
            _reject_huge_images(tmp_path)
            hits = scan_and_classify(tmp_path, max_results=max_results_i)
            return jsonify({"count": len(hits), "results": [h.to_dict() for h in hits]})
        except Exception as e:
            return jsonify({"error": str(e)}), 400
        finally:
            try:
                os.remove(tmp_path)
            except Exception:
                pass

    # ---------- AUTH ----------
    @app.get("/auth/list")
    @login_required
    @limiter.limit("120 per minute")
    def auth_list():
        accounts = list_totp_accounts(current_user.id)
        return jsonify({"count": len(accounts), "accounts": accounts})

    @app.post("/auth/import")
    @login_required
    @limiter.limit("20 per minute")
    def auth_import():
        data = request.get_json(silent=True) or {}
        uri = (data.get("otpauth_uri") or "").strip()
        if not uri:
            return jsonify({"error": "Missing otpauth_uri"}), 400

        try:
            acc = parse_otpauth_uri(uri)
        except OTPAuthError as e:
            return jsonify({"error": str(e)}), 400

        upsert_totp_account(
            user_id=current_user.id,
            acc_id=acc.id,
            name=acc.name,
            issuer=acc.issuer,
            secret_b32=acc.secret_b32,
            algorithm=acc.algorithm,
            digits=acc.digits,
            period=acc.period,
        )
        return jsonify({"imported": acc.safe_dict()})

    @app.post("/auth/delete")
    @login_required
    @limiter.limit("60 per minute")
    def auth_delete():
        data = request.get_json(silent=True) or {}
        acc_id = (data.get("id") or "").strip()
        if not acc_id:
            return jsonify({"error": "Missing id"}), 400

        ok = delete_totp_account(current_user.id, acc_id)
        if not ok:
            return jsonify({"error": "Unknown id"}), 404

        return jsonify({"deleted": acc_id})

    @app.get("/auth/code")
    @login_required
    @limiter.limit("240 per minute")
    def auth_code():
        acc_id = (request.args.get("id") or "").strip()
        if not acc_id:
            return jsonify({"error": "Missing id"}), 400

        row = get_totp_account(current_user.id, acc_id)
        if not row:
            return jsonify({"error": "Unknown id"}), 404

        # Build a transient OTPAuthAccount for totp_now
        from qrpypass.auth.models import OTPAuthAccount

        acc = OTPAuthAccount(
            id=row["id"],
            name=row["name"],
            issuer=row["issuer"],
            secret_b32=row["secret_b32"],
            algorithm=row["algorithm"],
            digits=row["digits"],
            period=row["period"],
        )
        code, remaining = totp_now(acc)
        return jsonify({"account": acc.safe_dict(), "code": code, "seconds_remaining": remaining})

    @app.post("/auth/verify")
    @login_required
    @limiter.limit("60 per minute")
    def auth_verify():
        data = request.get_json(silent=True) or {}
        acc_id = (data.get("id") or "").strip()
        code = (data.get("code") or "").strip()

        try:
            window = int(data.get("window", 1))
        except Exception:
            return jsonify({"error": "window must be an integer"}), 400

        if not acc_id:
            return jsonify({"error": "Missing id"}), 400
        if not code:
            return jsonify({"error": "Missing code"}), 400

        row = get_totp_account(current_user.id, acc_id)
        if not row:
            return jsonify({"error": "Unknown id"}), 404

        from qrpypass.auth.models import OTPAuthAccount

        acc = OTPAuthAccount(
            id=row["id"],
            name=row["name"],
            issuer=row["issuer"],
            secret_b32=row["secret_b32"],
            algorithm=row["algorithm"],
            digits=row["digits"],
            period=row["period"],
        )

        try:
            ok, offset = totp_verify(acc, code, window=window)
        except Exception as e:
            return jsonify({"error": str(e)}), 400

        return jsonify({"ok": ok, "matched_offset": offset, "account": acc.safe_dict()})

    # ---------- GENERATE ----------
    @app.post("/gen/payload")
    @login_required
    @limiter.limit("60 per minute")
    def gen_payload_api():
        data = request.get_json(silent=True) or {}
        kind = (data.get("kind") or "").strip()
        params = data.get("params", {}) or {}
        do_import = bool(data.get("import", False))

        try:
            gp = generate_payload(kind, params)
        except Exception as e:
            return jsonify({"error": str(e)}), 400

        imported = None
        if do_import and gp.kind.value == "otpauth_totp":
            try:
                acc = parse_otpauth_uri(gp.payload)
                upsert_totp_account(
                    user_id=current_user.id,
                    acc_id=acc.id,
                    name=acc.name,
                    issuer=acc.issuer,
                    secret_b32=acc.secret_b32,
                    algorithm=acc.algorithm,
                    digits=acc.digits,
                    period=acc.period,
                )
                imported = acc.safe_dict()
            except OTPAuthError as e:
                return jsonify({"error": str(e)}), 400

        return jsonify({"generated": gp.to_dict(), "imported": imported})

    @app.post("/gen/qr")
    @login_required
    @limiter.limit("120 per minute")
    def gen_qr():
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
