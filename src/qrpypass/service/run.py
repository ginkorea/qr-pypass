from __future__ import annotations

import os
from qrpypass.service.app import create_app

app = create_app()

if __name__ == "__main__":
    host = os.environ.get("QRPYPASS_HOST", "127.0.0.1")
    port = int(os.environ.get("QRPYPASS_PORT", "5000"))
    debug = os.environ.get("QRPYPASS_DEBUG", "0") == "1"
    app.run(host=host, port=port, debug=debug)
