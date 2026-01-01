from __future__ import annotations

import os
import tempfile
from typing import Any, Dict

from flask import Flask, jsonify, request

from qrpypass.qr import scan_and_classify


def create_app() -> Flask:
    app = Flask(__name__)

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

        # max_results (optional)
        max_results = request.form.get("max_results", "8")
        try:
            max_results_i = int(max_results)
            if max_results_i < 1 or max_results_i > 50:
                return jsonify({"error": "max_results must be between 1 and 50"}), 400
        except ValueError:
            return jsonify({"error": "max_results must be an integer"}), 400

        # Save to a temp file so OpenCV can reliably read it
        suffix = os.path.splitext(f.filename)[1].lower() or ".img"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp_path = tmp.name
            f.save(tmp_path)

        try:
            hits = scan_and_classify(tmp_path, max_results=max_results_i)
            return jsonify({
                "count": len(hits),
                "results": [h.to_dict() for h in hits],
            })
        except Exception as e:
            # Keep error message for dev; later we can gate with DEBUG flag
            return jsonify({"error": str(e)}), 500
        finally:
            try:
                os.remove(tmp_path)
            except Exception:
                pass

    return app
