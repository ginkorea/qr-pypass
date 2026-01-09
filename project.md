# Project Compilation: mysite

## 🧾 Summary

| Metric | Value |
|:--|:--|
| Root Directory | `/home/gompert/mysite` |
| Total Directories | 15 |
| Total Indexed Files | 43 |
| Skipped Files | 12 |
| Indexed Size | 146.72 KB |
| Max File Size Limit | 2 MB |

## 📚 Table of Contents

- [README.md](#readme-md)
- [_data/app.db](#data-app-db)
- [dist/qrpypass-0.1.2-py3-none-any.whl](#dist-qrpypass-0-1-2-py3-none-any-whl)
- [gitignore](#gitignore)
- [pyproject.toml](#pyproject-toml)
- [requirements.txt](#requirements-txt)
- [setup.py](#setup-py)
- [src/qrpypass.egg-info/PKG-INFO](#src-qrpypass-egg-info-pkg-info)
- [src/qrpypass.egg-info/SOURCES.txt](#src-qrpypass-egg-info-sources-txt)
- [src/qrpypass.egg-info/dependency_links.txt](#src-qrpypass-egg-info-dependency-links-txt)
- [src/qrpypass.egg-info/top_level.txt](#src-qrpypass-egg-info-top-level-txt)
- [src/qrpypass/__init__.py](#src-qrpypass-init-py)
- [src/qrpypass/auth/__init__.py](#src-qrpypass-auth-init-py)
- [src/qrpypass/auth/generate.py](#src-qrpypass-auth-generate-py)
- [src/qrpypass/auth/models.py](#src-qrpypass-auth-models-py)
- [src/qrpypass/auth/otpauth.py](#src-qrpypass-auth-otpauth-py)
- [src/qrpypass/auth/store.py](#src-qrpypass-auth-store-py)
- [src/qrpypass/auth/totp.py](#src-qrpypass-auth-totp-py)
- [src/qrpypass/classify/__init__.py](#src-qrpypass-classify-init-py)
- [src/qrpypass/classify/models.py](#src-qrpypass-classify-models-py)
- [src/qrpypass/classify/payload.py](#src-qrpypass-classify-payload-py)
- [src/qrpypass/generate/__init__.py](#src-qrpypass-generate-init-py)
- [src/qrpypass/generate/models.py](#src-qrpypass-generate-models-py)
- [src/qrpypass/generate/payloads.py](#src-qrpypass-generate-payloads-py)
- [src/qrpypass/qr/__init__.py](#src-qrpypass-qr-init-py)
- [src/qrpypass/qr/decode.py](#src-qrpypass-qr-decode-py)
- [src/qrpypass/qr/models.py](#src-qrpypass-qr-models-py)
- [src/qrpypass/qr/pipeline.py](#src-qrpypass-qr-pipeline-py)
- [src/qrpypass/qr/scan.py](#src-qrpypass-qr-scan-py)
- [src/qrpypass/service/app.py](#src-qrpypass-service-app-py)
- [src/qrpypass/service/db.py](#src-qrpypass-service-db-py)
- [src/qrpypass/service/run.py](#src-qrpypass-service-run-py)
- [src/qrpypass/service/static/app.js](#src-qrpypass-service-static-app-js)
- [src/qrpypass/service/static/gen.js](#src-qrpypass-service-static-gen-js)
- [src/qrpypass/service/static/style.css](#src-qrpypass-service-static-style-css)
- [src/qrpypass/service/templates/gen.html](#src-qrpypass-service-templates-gen-html)
- [src/qrpypass/service/templates/index.html](#src-qrpypass-service-templates-index-html)
- [src/qrpypass/service/templates/login.html](#src-qrpypass-service-templates-login-html)
- [src/qrpypass/service/templates/register.html](#src-qrpypass-service-templates-register-html)
- [src/qrpypass/service/templates/vault.html](#src-qrpypass-service-templates-vault-html)
- [test/api-test.py](#test-api-test-py)
- [test/full_api_smoke.py](#test-full-api-smoke-py)
- [test/test_totp_verify_flow.py](#test-test-totp-verify-flow-py)

## 📂 Project Structure

```
📁 _data/
    📄 app.db
📁 dist/
    📄 qrpypass-0.1.2-py3-none-any.whl
    📄 qrpypass-0.1.2.tar.gz
📁 images/
    📄 qr-logo.png
    📄 qr.png
📁 src/
    📁 qrpypass/
        📁 auth/
            📄 __init__.py
            📄 generate.py
            📄 models.py
            📄 otpauth.py
            📄 store.py
            📄 totp.py
        📁 classify/
            📄 __init__.py
            📄 models.py
            📄 payload.py
        📁 generate/
            📄 __init__.py
            📄 models.py
            📄 payloads.py
        📁 qr/
            📄 __init__.py
            📄 decode.py
            📄 models.py
            📄 pipeline.py
            📄 scan.py
        📁 service/
            📁 static/
                📄 app.js
                📄 apple-touch-icon-180.png
                📄 favicon-16.png
                📄 favicon-32.png
                📄 favicon-48.png
                📄 favicon.ico
                📄 gen.js
                📄 icon-512.png
                📄 style.css
            📁 templates/
                📄 gen.html
                📄 index.html
                📄 login.html
                📄 register.html
                📄 vault.html
            📄 app.py
            📄 db.py
            📄 run.py
        📄 __init__.py
    📁 qrpypass.egg-info/
        📄 dependency_links.txt
        📄 PKG-INFO
        📄 SOURCES.txt
        📄 top_level.txt
📁 test/
    📁 api_test_out/
        📄 text.png
        📄 totp.png
        📄 url.png
    📄 api-test.py
    📄 full_api_smoke.py
    📄 test_totp_verify_flow.py
📄 gitignore
📄 pyproject.toml
📄 README.md
📄 requirements.txt
📄 setup.py
```

## `README.md`

```markdown
![qr-pypass logo](images/qr-logo.png)

# qr-pypass

**qr-pypass** is a lightweight, headless QR decoding and TOTP authentication service built for **offline-first security workflows**.

It is designed for air-gapped labs, red-team and blue-team tooling, automation pipelines, and environments where QR codes and 2FA need to be processed **locally**, without mobile devices or cloud dependencies.

**Homepage:** [https://ginkorea.one](https://ginkorea.one)
**Source:** [https://github.com/ginkorea/qr-pypass](https://github.com/ginkorea/qr-pypass)
**PyPI:** [https://pypi.org/project/qrpypass/](https://pypi.org/project/qrpypass/)

---

## What It Does

With `qr-pypass`, you can:

* Decode QR codes from screenshots or images
* Detect and classify QR payloads (URL, text, otpauth)
* Generate QR codes programmatically
* Generate, import, store, and verify TOTP (RFC 6238) secrets
* Run everything locally with no outbound network access

The project exposes both:

* A **Python API** for direct integration
* A **Flask-based HTTP service** with a minimal web UI

---

## Core Features

### QR Decoding

* Detects **multiple QR codes anywhere in an image**
* Uses OpenCV with multi-pass detection and tiling fallback
* Returns bounding boxes, corner points, and decode method
* Robust against screenshots, partial QRs, and large images

### Payload Classification

Automatically classifies decoded payloads as:

* `url` (with normalization)
* `text`
* `otpauth` (TOTP provisioning URIs)

### TOTP / OTPAuth

* Generate RFC-compliant `otpauth://totp` URIs
* Import existing provisioning URIs
* Secure local storage (optional encryption at rest)
* Generate current TOTP codes
* Verify TOTP codes with configurable time window

### QR Generation

* Generate QR codes for:

  * URLs
  * Arbitrary text
  * TOTP provisioning URIs
* Control box size and border
* Outputs PNG images

### Service and Web UI

* Flask-based HTTP API
* Minimal web UI for:

  * Uploading screenshots or images
  * Viewing decoded QR payloads
  * Generating QR codes
  * Managing stored TOTP accounts

No JavaScript frameworks. No external assets.

---

## Installation

### From PyPI

```bash
pip install qrpypass
```

Python **3.9+** is required.

---

### From Source (Development)

```bash
git clone https://github.com/ginkorea/qr-pypass.git
cd qr-pypass

python -m venv .qr-env
source .qr-env/bin/activate

pip install -r requirements.txt
pip install -e .
```

---

## Running the Service

```bash
python -m qrpypass.service.run
```

By default, the service runs at:

```
http://127.0.0.1:5000
```

---

## Configuration

The service can be configured using environment variables:

| Variable             | Default       | Description                     |
| -------------------- | ------------- | ------------------------------- |
| `QRPYPASS_HOST`      | `127.0.0.1`   | Bind address                    |
| `QRPYPASS_PORT`      | `5000`        | Port                            |
| `QRPYPASS_DEBUG`     | `0`           | Enable Flask debug mode         |
| `QRPYPASS_STORE_DIR` | `~/.qrpypass` | Local account storage directory |

---

## Web UI Routes

* `/` – QR scan UI (upload screenshots or images)
* `/gen` – QR payload and TOTP generator
* `/vault` – Stored TOTP account management

---

## API Overview

### Health Check

```http
GET /health
```

---

### Scan QR Codes

```http
POST /scan
Content-Type: multipart/form-data
```

**Form fields**

* `file` (required) – image file
* `max_results` (optional, default: 8)

---

### Generate Payload

```http
POST /gen/payload
Content-Type: application/json
```

```json
{
  "kind": "url | text | totp",
  "params": { },
  "import": false,
  "passphrase": null
}
```

---

### Generate QR Image

```http
POST /gen/qr
Content-Type: application/json
```

```json
{
  "payload": "...",
  "box_size": 8,
  "border": 2
}
```

Returns `image/png`.

---

### TOTP Endpoints

| Endpoint            | Description           |
| ------------------- | --------------------- |
| `POST /auth/import` | Import otpauth URI    |
| `GET /auth/list`    | List stored accounts  |
| `GET /auth/code`    | Get current TOTP code |
| `POST /auth/verify` | Verify TOTP code      |

An optional `passphrase` encrypts the TOTP store at rest.

---

## Python API Example

```python
from qrpypass.qr import scan_and_classify

hits = scan_and_classify("screenshot.png")
for hit in hits:
    print(hit.classification.kind, hit.qr.payload)
```

---

## Testing

End-to-end tests are included:

```bash
python test/api-test.py
python test/full_api_smoke.py
python test/test_totp_verify_flow.py
```

These cover:

* QR generation → scan → classification
* TOTP generation, import, code generation, and verification

---

## Security Notes

* Secrets are never logged
* TOTP storage can be encrypted at rest
* No outbound network access
* Suitable for air-gapped or lab environments

---

## Common Use Cases

* QR extraction from screenshots (2FA enrollment, phishing analysis)
* Headless TOTP verification in security tooling
* Red-team and blue-team labs
* Offline QR decoding pipelines
* Local alternatives to mobile authenticator apps

---

## License

MIT

---

## Author

**Josh Gompert**
[https://ginkorea.one](https://ginkorea.one)


```

## `gitignore`

```text
# Environments
.qr-env/
.venv/
env/
venv/
*.env

# Python build artifacts
*.egg-info/
dist/
build/
*.whl
*.egg
MANIFEST

# Byte-compiled files & caches
__pycache__/
*.py[cod]
*.pyo
*.pyd
.pytest_cache/
.mypy_cache/
.ruff_cache/
*.cache

# OS files
.DS_Store
Thumbs.db

# Logs
*.log
logs/

```

## `pyproject.toml`

```toml
[project]
name = "qrpypass"
version = "0.1.2"
description = "Headless QR decoder + TOTP authenticator Flask mini-service"
readme = "README.md"
requires-python = ">=3.9"
license = { text = "MIT" }

authors = [
  { name = "Josh Gompert" }
]
[project.urls]
Homepage = "https://ginkorea.one"
Repository = "https://github.com/ginkorea/qr-pypass"
Issues = "https://github.com/ginkorea/qr-pypass/issues"


```

## `requirements.txt`

```text
opencv-python>=4.8.0
cryptography>=41.0.0
Flask>=3.0.0
qrcode[pil]>=7.4.2
Pillow>=10.0.0
Flask-Login>=0.6.3
Flask-Limiter>=3.7.0



```

## `setup.py`

```python
from setuptools import setup, find_packages

setup(
    name="qrpypass",
    version="0.1.2",
    description="Headless QR decoder + TOTP authenticator Flask mini-service",
    author="Josh Gompert",
    author_email="",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "opencv-python>=4.8.0",
        "cryptography>=41.0.0",
        "Flask>=3.0.0",
        "qrcode[pil]>=7.4.2",
        "Pillow>=10.0.0",
    ],
    python_requires=">=3.9",
)

```

## `src/qrpypass.egg-info/PKG-INFO`

```text
Metadata-Version: 2.4
Name: qrpypass
Version: 0.1.2
Summary: Headless QR decoder + TOTP authenticator Flask mini-service
Author: Josh Gompert
Author-email: 
License: MIT
Project-URL: Homepage, https://ginkorea.one
Project-URL: Repository, https://github.com/ginkorea/qr-pypass
Project-URL: Issues, https://github.com/ginkorea/qr-pypass/issues
Requires-Python: >=3.9
Description-Content-Type: text/markdown
Dynamic: requires-python

![qr-pypass logo](images/qr-logo.png)

# qr-pypass

**qr-pypass** is a lightweight, headless QR decoding and TOTP authentication service built for **offline-first security workflows**.

It is designed for air-gapped labs, red-team and blue-team tooling, automation pipelines, and environments where QR codes and 2FA need to be processed **locally**, without mobile devices or cloud dependencies.

**Homepage:** [https://ginkorea.one](https://ginkorea.one)
**Source:** [https://github.com/ginkorea/qr-pypass](https://github.com/ginkorea/qr-pypass)
**PyPI:** [https://pypi.org/project/qrpypass/](https://pypi.org/project/qrpypass/)

---

## What It Does

With `qr-pypass`, you can:

* Decode QR codes from screenshots or images
* Detect and classify QR payloads (URL, text, otpauth)
* Generate QR codes programmatically
* Generate, import, store, and verify TOTP (RFC 6238) secrets
* Run everything locally with no outbound network access

The project exposes both:

* A **Python API** for direct integration
* A **Flask-based HTTP service** with a minimal web UI

---

## Core Features

### QR Decoding

* Detects **multiple QR codes anywhere in an image**
* Uses OpenCV with multi-pass detection and tiling fallback
* Returns bounding boxes, corner points, and decode method
* Robust against screenshots, partial QRs, and large images

### Payload Classification

Automatically classifies decoded payloads as:

* `url` (with normalization)
* `text`
* `otpauth` (TOTP provisioning URIs)

### TOTP / OTPAuth

* Generate RFC-compliant `otpauth://totp` URIs
* Import existing provisioning URIs
* Secure local storage (optional encryption at rest)
* Generate current TOTP codes
* Verify TOTP codes with configurable time window

### QR Generation

* Generate QR codes for:

  * URLs
  * Arbitrary text
  * TOTP provisioning URIs
* Control box size and border
* Outputs PNG images

### Service and Web UI

* Flask-based HTTP API
* Minimal web UI for:

  * Uploading screenshots or images
  * Viewing decoded QR payloads
  * Generating QR codes
  * Managing stored TOTP accounts

No JavaScript frameworks. No external assets.

---

## Installation

### From PyPI

```bash
pip install qrpypass
```

Python **3.9+** is required.

---

### From Source (Development)

```bash
git clone https://github.com/ginkorea/qr-pypass.git
cd qr-pypass

python -m venv .qr-env
source .qr-env/bin/activate

pip install -r requirements.txt
pip install -e .
```

---

## Running the Service

```bash
python -m qrpypass.service.run
```

By default, the service runs at:

```
http://127.0.0.1:5000
```

---

## Configuration

The service can be configured using environment variables:

| Variable             | Default       | Description                     |
| -------------------- | ------------- | ------------------------------- |
| `QRPYPASS_HOST`      | `127.0.0.1`   | Bind address                    |
| `QRPYPASS_PORT`      | `5000`        | Port                            |
| `QRPYPASS_DEBUG`     | `0`           | Enable Flask debug mode         |
| `QRPYPASS_STORE_DIR` | `~/.qrpypass` | Local account storage directory |

---

## Web UI Routes

* `/` – QR scan UI (upload screenshots or images)
* `/gen` – QR payload and TOTP generator
* `/vault` – Stored TOTP account management

---

## API Overview

### Health Check

```http
GET /health
```

---

### Scan QR Codes

```http
POST /scan
Content-Type: multipart/form-data
```

**Form fields**

* `file` (required) – image file
* `max_results` (optional, default: 8)

---

### Generate Payload

```http
POST /gen/payload
Content-Type: application/json
```

```json
{
  "kind": "url | text | totp",
  "params": { },
  "import": false,
  "passphrase": null
}
```

---

### Generate QR Image

```http
POST /gen/qr
Content-Type: application/json
```

```json
{
  "payload": "...",
  "box_size": 8,
  "border": 2
}
```

Returns `image/png`.

---

### TOTP Endpoints

| Endpoint            | Description           |
| ------------------- | --------------------- |
| `POST /auth/import` | Import otpauth URI    |
| `GET /auth/list`    | List stored accounts  |
| `GET /auth/code`    | Get current TOTP code |
| `POST /auth/verify` | Verify TOTP code      |

An optional `passphrase` encrypts the TOTP store at rest.

---

## Python API Example

```python
from qrpypass.qr import scan_and_classify

hits = scan_and_classify("screenshot.png")
for hit in hits:
    print(hit.classification.kind, hit.qr.payload)
```

---

## Testing

End-to-end tests are included:

```bash
python test/api-test.py
python test/full_api_smoke.py
python test/test_totp_verify_flow.py
```

These cover:

* QR generation → scan → classification
* TOTP generation, import, code generation, and verification

---

## Security Notes

* Secrets are never logged
* TOTP storage can be encrypted at rest
* No outbound network access
* Suitable for air-gapped or lab environments

---

## Common Use Cases

* QR extraction from screenshots (2FA enrollment, phishing analysis)
* Headless TOTP verification in security tooling
* Red-team and blue-team labs
* Offline QR decoding pipelines
* Local alternatives to mobile authenticator apps

---

## License

MIT

---

## Author

**Josh Gompert**
[https://ginkorea.one](https://ginkorea.one)


```

## `src/qrpypass.egg-info/SOURCES.txt`

```text
README.md
pyproject.toml
setup.py
src/qrpypass/__init__.py
src/qrpypass.egg-info/PKG-INFO
src/qrpypass.egg-info/SOURCES.txt
src/qrpypass.egg-info/dependency_links.txt
src/qrpypass.egg-info/top_level.txt
src/qrpypass/auth/__init__.py
src/qrpypass/auth/generate.py
src/qrpypass/auth/models.py
src/qrpypass/auth/otpauth.py
src/qrpypass/auth/store.py
src/qrpypass/auth/totp.py
src/qrpypass/classify/__init__.py
src/qrpypass/classify/models.py
src/qrpypass/classify/payload.py
src/qrpypass/generate/__init__.py
src/qrpypass/generate/models.py
src/qrpypass/generate/payloads.py
src/qrpypass/qr/__init__.py
src/qrpypass/qr/decode.py
src/qrpypass/qr/models.py
src/qrpypass/qr/pipeline.py
src/qrpypass/qr/scan.py
test/test_totp_verify_flow.py
```

## `src/qrpypass.egg-info/dependency_links.txt`

```text


```

## `src/qrpypass.egg-info/top_level.txt`

```text
qrpypass

```

## `src/qrpypass/__init__.py`

```python
from .generate.models import GenKind, GeneratedPayload
from .generate.payloads import generate_payload, generate_text, generate_url, generate_totp

__all__ = ["GenKind", "GeneratedPayload", "generate_payload", "generate_text", "generate_url", "generate_totp"]

```

## `src/qrpypass/auth/__init__.py`

```python
from .models import OTPAuthAccount, OTPAccount
from .otpauth import OTPAuthError, parse_otpauth_uri
from .totp import totp_now, totp_verify
from .store import load_accounts, save_accounts, default_store_path, StoreError
from .generate import generate_totp_secret_b32, build_otpauth_uri

__all__ = [
    "OTPAuthAccount",
    "OTPAccount",
    "OTPAuthError",
    "parse_otpauth_uri",
    "totp_now",
    "totp_verify",
    "load_accounts",
    "save_accounts",
    "default_store_path",
    "StoreError",
    "generate_totp_secret_b32",
    "build_otpauth_uri",
]

```

## `src/qrpypass/auth/generate.py`

```python
from __future__ import annotations

import base64
import os
from urllib.parse import quote


def generate_totp_secret_b32(*, nbytes: int = 20) -> str:
    """
    Generate a random TOTP secret in Base32 (uppercase, no padding).
    Default: 20 bytes (160-bit), common for TOTP.
    """
    if not (10 <= nbytes <= 64):
        raise ValueError("nbytes must be between 10 and 64")

    raw = os.urandom(nbytes)
    # base32 includes '=', strip padding for otpauth URIs
    return base64.b32encode(raw).decode("ascii").rstrip("=").upper()


def build_otpauth_uri(
    *,
    issuer: str,
    account_name: str,
    secret_b32: str,
    digits: int = 6,
    period: int = 30,
    algorithm: str = "SHA1",
) -> str:
    """
    Build an otpauth://totp provisioning URI.

    Label: "Issuer:Account"
    Query: secret, issuer, algorithm, digits, period
    """
    issuer = (issuer or "").strip()
    account_name = (account_name or "").strip()
    secret_b32 = (secret_b32 or "").strip().replace(" ", "").upper()

    if not issuer:
        raise ValueError("issuer is required")
    if not account_name:
        raise ValueError("account_name is required")
    if not secret_b32:
        raise ValueError("secret_b32 is required")

    algorithm = (algorithm or "SHA1").upper()
    if algorithm not in {"SHA1", "SHA256", "SHA512"}:
        raise ValueError("algorithm must be SHA1, SHA256, or SHA512")

    if digits not in {6, 7, 8}:
        raise ValueError("digits must be 6, 7, or 8")
    if not (5 <= int(period) <= 300):
        raise ValueError("period must be between 5 and 300 seconds")

    # Label is commonly "Issuer:Account"
    label = f"{issuer}:{account_name}"
    label_enc = quote(label, safe="")

    return (
        f"otpauth://totp/{label_enc}"
        f"?secret={quote(secret_b32, safe='')}"
        f"&issuer={quote(issuer, safe='')}"
        f"&algorithm={quote(algorithm, safe='')}"
        f"&digits={int(digits)}"
        f"&period={int(period)}"
    )

```

## `src/qrpypass/auth/models.py`

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass(frozen=True)
class OTPAuthAccount:
    """
    Parsed representation of otpauth://totp/... provisioning.
    Secret is stored as base32 string (normalized) but should not be logged.
    """
    id: str                 # stable key for storage (derived from issuer+name)
    name: str               # account name (label right side)
    issuer: Optional[str]   # issuer if present
    secret_b32: str         # base32 (no spaces), normalized to uppercase
    algorithm: str = "SHA1" # SHA1/SHA256/SHA512
    digits: int = 6
    period: int = 30

    def safe_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "issuer": self.issuer,
            "algorithm": self.algorithm,
            "digits": self.digits,
            "period": self.period,
        }


# Backwards-compatible alias (your totp.py was importing OTPAccount)
OTPAccount = OTPAuthAccount

```

## `src/qrpypass/auth/otpauth.py`

```python
from __future__ import annotations

import hashlib
import re
import urllib.parse
from typing import Optional, Tuple, Dict

from .models import OTPAuthAccount


class OTPAuthError(ValueError):
    pass


_B32_RE = re.compile(r"^[A-Z2-7]+=*$")


def _norm_b32(s: str) -> str:
    s2 = s.strip().replace(" ", "").upper()
    if not s2:
        raise OTPAuthError("Missing secret")
    # allow lowercase + spaces in input, normalize to uppercase
    if not _B32_RE.match(s2):
        # We keep it strict-ish: otpauth secrets are base32 (A-Z2-7) with optional '=' padding.
        raise OTPAuthError("Secret does not look like base32")
    return s2


def _parse_label(label: str) -> Tuple[Optional[str], str]:
    """
    Label is usually 'Issuer:AccountName' or just 'AccountName'.
    """
    label = label.strip()
    if ":" in label:
        issuer_label, name = label.split(":", 1)
        issuer_label = issuer_label.strip() or None
        name = name.strip()
        return issuer_label, name
    return None, label


def _stable_id(issuer: Optional[str], name: str) -> str:
    base = f"{issuer or ''}|{name}".encode("utf-8", "ignore")
    return hashlib.sha256(base).hexdigest()[:16]


def parse_otpauth_uri(uri: str) -> OTPAuthAccount:
    """
    Supports otpauth://totp/... only. HOTP can be added later.
    """
    if not uri or not uri.lower().startswith("otpauth://"):
        raise OTPAuthError("Not an otpauth URI")

    p = urllib.parse.urlparse(uri)
    typ = (p.netloc or "").lower()
    if typ != "totp":
        raise OTPAuthError(f"Unsupported otpauth type: {typ!r} (only 'totp' supported)")

    label = urllib.parse.unquote((p.path or "").lstrip("/"))
    if not label:
        raise OTPAuthError("Missing label in otpauth URI")

    issuer_label, name = _parse_label(label)
    if not name:
        raise OTPAuthError("Missing account name in label")

    qs = urllib.parse.parse_qs(p.query)

    secret_raw = (qs.get("secret", [""])[0] or "").strip()
    secret_b32 = _norm_b32(secret_raw)

    issuer_q = (qs.get("issuer", [None])[0] or None)
    issuer = issuer_q or issuer_label

    algorithm = (qs.get("algorithm", ["SHA1"])[0] or "SHA1").upper()
    if algorithm not in {"SHA1", "SHA256", "SHA512"}:
        raise OTPAuthError(f"Unsupported algorithm: {algorithm}")

    digits_s = (qs.get("digits", ["6"])[0] or "6")
    try:
        digits = int(digits_s)
    except ValueError:
        raise OTPAuthError("digits must be an integer")
    if digits not in {6, 7, 8}:
        raise OTPAuthError("digits must be 6, 7, or 8")

    period_s = (qs.get("period", ["30"])[0] or "30")
    try:
        period = int(period_s)
    except ValueError:
        raise OTPAuthError("period must be an integer")
    if period < 5 or period > 300:
        raise OTPAuthError("period must be between 5 and 300 seconds")

    acc_id = _stable_id(issuer, name)

    return OTPAuthAccount(
        id=acc_id,
        name=name,
        issuer=issuer,
        secret_b32=secret_b32,
        algorithm=algorithm,
        digits=digits,
        period=period,
    )

```

## `src/qrpypass/auth/store.py`

```python
from __future__ import annotations

import json
import os
from dataclasses import asdict
from pathlib import Path
from typing import Dict, Optional, Any, List

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

from .models import OTPAuthAccount


class StoreError(RuntimeError):
    pass


def default_store_path() -> Path:
    base = Path(os.environ.get("QRPYPASS_STORE_DIR", Path.home() / ".qrpypass"))
    base.mkdir(parents=True, exist_ok=True)
    return base / "accounts.json"


def _kdf(passphrase: str, salt: bytes) -> bytes:
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    return kdf.derive(passphrase.encode("utf-8", "ignore"))


def _fernet_from_passphrase(passphrase: str, salt: bytes) -> Fernet:
    key = _kdf(passphrase, salt)
    return Fernet(base64_urlsafe(key))


def base64_urlsafe(raw32: bytes) -> bytes:
    import base64
    return base64.urlsafe_b64encode(raw32)


def _serialize_account(a: OTPAuthAccount) -> Dict[str, Any]:
    return {
        "id": a.id,
        "name": a.name,
        "issuer": a.issuer,
        "secret_b32": a.secret_b32,
        "algorithm": a.algorithm,
        "digits": a.digits,
        "period": a.period,
    }


def _deserialize_account(d: Dict[str, Any]) -> OTPAuthAccount:
    return OTPAuthAccount(
        id=d["id"],
        name=d["name"],
        issuer=d.get("issuer"),
        secret_b32=d["secret_b32"],
        algorithm=d.get("algorithm", "SHA1"),
        digits=int(d.get("digits", 6)),
        period=int(d.get("period", 30)),
    )


def load_accounts(path: Optional[Path] = None, *, passphrase: Optional[str] = None) -> Dict[str, OTPAuthAccount]:
    path = path or default_store_path()
    if not path.exists():
        return {}

    raw = path.read_bytes()

    try:
        doc = json.loads(raw.decode("utf-8"))
    except Exception as e:
        raise StoreError(f"Failed to parse store JSON: {e}")

    if doc.get("encrypted") is True:
        if not passphrase:
            raise StoreError("Store is encrypted. Passphrase required.")
        salt_b64 = doc.get("salt_b64")
        token = doc.get("token")
        if not salt_b64 or not token:
            raise StoreError("Encrypted store missing salt/token fields")

        import base64
        salt = base64.b64decode(salt_b64)
        f = _fernet_from_passphrase(passphrase, salt)
        try:
            plain = f.decrypt(token.encode("utf-8"))
        except InvalidToken:
            raise StoreError("Bad passphrase (cannot decrypt store)")
        payload = json.loads(plain.decode("utf-8"))
    else:
        payload = doc

    items = payload.get("accounts", [])
    out: Dict[str, OTPAuthAccount] = {}
    for d in items:
        a = _deserialize_account(d)
        out[a.id] = a
    return out


def save_accounts(accounts: Dict[str, OTPAuthAccount], path: Optional[Path] = None, *, passphrase: Optional[str] = None) -> None:
    path = path or default_store_path()
    payload = {"accounts": [_serialize_account(a) for a in accounts.values()]}

    if passphrase:
        # encrypt at rest
        import base64, os
        salt = os.urandom(16)
        f = _fernet_from_passphrase(passphrase, salt)
        token = f.encrypt(json.dumps(payload).encode("utf-8")).decode("utf-8")
        doc = {
            "encrypted": True,
            "salt_b64": base64.b64encode(salt).decode("utf-8"),
            "token": token,
        }
        path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    else:
        # plaintext store (still fine for airgapped labs; your call)
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

```

## `src/qrpypass/auth/totp.py`

```python
from __future__ import annotations

import base64
import binascii
import hmac
import hashlib
import time
from typing import Tuple

from .models import OTPAuthAccount  # canonical


def _b32_decode_nopad(secret_b32: str) -> bytes:
    s = (secret_b32 or "").strip().replace(" ", "").upper()
    pad = (-len(s)) % 8
    s += "=" * pad
    try:
        return base64.b32decode(s, casefold=True)
    except binascii.Error as e:
        raise ValueError("Invalid base32 secret") from e


def _hotp(key: bytes, counter: int, digits: int, algo: str) -> str:
    algo_u = (algo or "SHA1").upper()
    if algo_u == "SHA1":
        digestmod = hashlib.sha1
    elif algo_u == "SHA256":
        digestmod = hashlib.sha256
    elif algo_u == "SHA512":
        digestmod = hashlib.sha512
    else:
        raise ValueError("Unsupported algorithm (use SHA1/SHA256/SHA512)")

    msg = counter.to_bytes(8, "big")
    h = hmac.new(key, msg, digestmod).digest()
    off = h[-1] & 0x0F
    dbc = int.from_bytes(h[off:off + 4], "big") & 0x7FFFFFFF
    code = dbc % (10 ** digits)
    return str(code).zfill(digits)


def totp_at(acc: OTPAuthAccount, for_time: int) -> str:
    key = _b32_decode_nopad(acc.secret_b32)
    period = int(acc.period)
    counter = int(for_time) // period
    return _hotp(key, counter, int(acc.digits), acc.algorithm)


def totp_now(acc: OTPAuthAccount) -> Tuple[str, int]:
    now = int(time.time())
    code = totp_at(acc, now)
    period = int(acc.period)
    remaining = period - (now % period)
    return code, remaining


def totp_verify(
    acc: OTPAuthAccount,
    code: str,
    *,
    window: int = 1,
    at_time: int | None = None,
) -> Tuple[bool, int]:
    if at_time is None:
        at_time = int(time.time())

    code = (code or "").strip()
    if not code.isdigit():
        return False, 0

    if window < 0 or window > 10:
        raise ValueError("window must be between 0 and 10")

    period = int(acc.period)
    base = int(at_time)

    for offset in range(-window, window + 1):
        t = base + (offset * period)
        expected = totp_at(acc, t)
        if hmac.compare_digest(expected, code):
            return True, offset

    return False, 0

```

## `src/qrpypass/classify/__init__.py`

```python
from .models import PayloadKind, ClassifiedPayload
from .payload import classify_payload

__all__ = ["PayloadKind", "ClassifiedPayload", "classify_payload"]

```

## `src/qrpypass/classify/models.py`

```python
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict, Any


class PayloadKind(str, Enum):
    OTPAUTH = "otpauth"
    URL = "url"
    TEXT = "text"


@dataclass(frozen=True)
class ClassifiedPayload:
    kind: PayloadKind
    raw: str
    # For URL kind, normalized_url will include a scheme.
    normalized_url: Optional[str] = None
    # Extra extracted info (issuer/name for otpauth label, etc.)
    meta: Optional[Dict[str, Any]] = None

    def to_dict(self) -> dict:
        return {
            "kind": self.kind.value,
            "raw": self.raw,
            "normalized_url": self.normalized_url,
            "meta": self.meta or {},
        }

```

## `src/qrpypass/classify/payload.py`

```python
from __future__ import annotations

import re
import urllib.parse
from typing import Optional, Dict, Any

from .models import ClassifiedPayload, PayloadKind


_URL_SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*://")
_BARE_DOMAIN_RE = re.compile(r"^[A-Za-z0-9.-]+\.[A-Za-z]{2,}([/:?#].*)?$")


def classify_payload(raw: str) -> ClassifiedPayload:
    s = (raw or "").strip()

    if not s:
        return ClassifiedPayload(kind=PayloadKind.TEXT, raw="")

    # 1) otpauth provisioning
    if s.lower().startswith("otpauth://"):
        meta = _parse_otpauth_meta_best_effort(s)
        return ClassifiedPayload(kind=PayloadKind.OTPAUTH, raw=s, meta=meta)

    # 2) URL (http/https or bare domain)
    url = _normalize_url_if_possible(s)
    if url is not None:
        return ClassifiedPayload(kind=PayloadKind.URL, raw=s, normalized_url=url, meta=_url_meta(url))

    # 3) Anything else
    return ClassifiedPayload(kind=PayloadKind.TEXT, raw=s)


def _normalize_url_if_possible(s: str) -> Optional[str]:
    # Already has a scheme (http/https/etc.)
    if _URL_SCHEME_RE.match(s):
        return s

    # Looks like a domain.tld (optionally with path/query)
    if _BARE_DOMAIN_RE.match(s):
        return "https://" + s

    return None


def _url_meta(url: str) -> Dict[str, Any]:
    try:
        p = urllib.parse.urlparse(url)
        return {
            "scheme": p.scheme,
            "host": p.hostname or "",
            "path": p.path or "",
        }
    except Exception:
        return {}


def _parse_otpauth_meta_best_effort(uri: str) -> Dict[str, Any]:
    """
    Parse just enough for classification/UI without depending on the OTP module.
    Full parsing + validation belongs in the authenticator module later.
    """
    out: Dict[str, Any] = {}
    try:
        p = urllib.parse.urlparse(uri)
        out["type"] = p.netloc  # totp / hotp (we mainly support totp)
        label = urllib.parse.unquote(p.path.lstrip("/"))
        out["label"] = label

        if ":" in label:
            issuer_label, name = label.split(":", 1)
            out["issuer_label"] = issuer_label
            out["name"] = name
        else:
            out["name"] = label

        qs = urllib.parse.parse_qs(p.query)
        if "issuer" in qs:
            out["issuer"] = qs["issuer"][0]
        if "digits" in qs:
            out["digits"] = qs["digits"][0]
        if "period" in qs:
            out["period"] = qs["period"][0]
        if "algorithm" in qs:
            out["algorithm"] = qs["algorithm"][0]
        # do NOT include secret in meta by default (avoid accidental logging)
        out["has_secret"] = "secret" in qs and bool(qs["secret"][0])
    except Exception:
        # best-effort only
        pass
    return out

```

## `src/qrpypass/generate/__init__.py`

```python
from .models import GenKind, GeneratedPayload
from .payloads import generate_payload, generate_text, generate_url, generate_totp

__all__ = [
    "GenKind",
    "GeneratedPayload",
    "generate_payload",
    "generate_text",
    "generate_url",
    "generate_totp",
]

```

## `src/qrpypass/generate/models.py`

```python
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict, Any


class GenKind(str, Enum):
    URL = "url"
    TEXT = "text"
    OTPAUTH_TOTP = "otpauth_totp"


@dataclass(frozen=True)
class GeneratedPayload:
    kind: GenKind
    payload: str
    meta: Dict[str, Any]

    def to_dict(self) -> dict:
        return {"kind": self.kind.value, "payload": self.payload, "meta": self.meta}

```

## `src/qrpypass/generate/payloads.py`

```python
from __future__ import annotations

from typing import Dict, Any, Optional
from urllib.parse import urlencode, quote

from qrpypass.auth.generate import generate_totp_secret_b32, build_otpauth_uri
from .models import GenKind, GeneratedPayload


def generate_text(*, text: str) -> GeneratedPayload:
    text = (text or "").strip()
    if not text:
        raise ValueError("text is required")
    return GeneratedPayload(kind=GenKind.TEXT, payload=text, meta={})


def generate_url(*, url: str) -> GeneratedPayload:
    url = (url or "").strip()
    if not url:
        raise ValueError("url is required")
    # Do not over-normalize; generation should respect user intent.
    return GeneratedPayload(kind=GenKind.URL, payload=url, meta={})


def generate_totp(
    *,
    issuer: str,
    account_name: str,
    secret_b32: Optional[str] = None,
    digits: int = 6,
    period: int = 30,
    algorithm: str = "SHA1",
    nbytes: int = 20,
) -> GeneratedPayload:
    issuer = (issuer or "").strip()
    account_name = (account_name or "").strip()
    if not issuer:
        raise ValueError("issuer is required")
    if not account_name:
        raise ValueError("account_name is required")

    if secret_b32 is None:
        if nbytes < 10 or nbytes > 64:
            raise ValueError("nbytes must be between 10 and 64")
        secret_b32 = generate_totp_secret_b32(nbytes=nbytes)

    uri = build_otpauth_uri(
        issuer=issuer,
        account_name=account_name,
        secret_b32=secret_b32,
        digits=digits,
        period=period,
        algorithm=algorithm,
    )

    # meta includes secret because you are generating it; caller can choose to display/store
    return GeneratedPayload(
        kind=GenKind.OTPAUTH_TOTP,
        payload=uri,
        meta={
            "issuer": issuer,
            "account_name": account_name,
            "digits": digits,
            "period": period,
            "algorithm": algorithm.upper(),
            "secret_b32": secret_b32,
        },
    )


def generate_payload(kind: str, params: Dict[str, Any]) -> GeneratedPayload:
    k = (kind or "").strip().lower()
    if k == "text":
        return generate_text(text=params.get("text", ""))
    if k == "url":
        return generate_url(url=params.get("url", ""))
    if k in {"totp", "otpauth", "otpauth_totp"}:
        return generate_totp(
            issuer=params.get("issuer", ""),
            account_name=params.get("account_name", ""),
            secret_b32=params.get("secret_b32"),
            digits=int(params.get("digits", 6)),
            period=int(params.get("period", 30)),
            algorithm=params.get("algorithm", "SHA1"),
            nbytes=int(params.get("nbytes", 20)),
        )
    raise ValueError(f"Unsupported kind: {kind!r}")

```

## `src/qrpypass/qr/__init__.py`

```python
from .models import QRResult
from .scan import scan_qr_anywhere
from .pipeline import scan_and_classify, ScanHit

__all__ = ["QRResult", "scan_qr_anywhere", "ScanHit", "scan_and_classify"]

```

## `src/qrpypass/qr/decode.py`

```python
from __future__ import annotations
from typing import List, Tuple
import cv2
import numpy as np
from .models import QRResult

class QRDecodeError(RuntimeError):
    pass

def _bbox_from_corners(corners: np.ndarray) -> Tuple[int, int, int, int]:
    xs, ys = corners[:, 0], corners[:, 1]
    x0, y0 = int(xs.min()), int(ys.min())
    x1, y1 = int(xs.max()), int(ys.max())
    return x0, y0, max(1, x1-x0), max(1, y1-y0)

def decode_multi(img: np.ndarray) -> List[QRResult]:
    det = cv2.QRCodeDetector()
    try:
        ok, data_list, points, _ = det.detectAndDecodeMulti(img)
    except Exception:
        return []
    if not ok or not data_list:
        return []
    results = []
    for i, data in enumerate(data_list):
        if not data:
            continue
        corners = points[i].astype(np.float32) if points is not None else None
        bbox = _bbox_from_corners(corners) if corners is not None else None
        results.append(QRResult(payload=data, corners=corners, bbox=bbox, method="multi"))
    return results

def decode_single(img: np.ndarray) -> List[QRResult]:
    det = cv2.QRCodeDetector()
    data, pts, _ = det.detectAndDecode(img)
    if not data:
        return []
    corners = pts.astype(np.float32) if pts is not None else None
    bbox = _bbox_from_corners(corners) if corners is not None else None
    return [QRResult(payload=data, corners=corners, bbox=bbox, method="single")]

```

## `src/qrpypass/qr/models.py`

```python
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Tuple, List
import numpy as np

@dataclass(frozen=True)
class QRResult:
    payload: str
    corners: Optional[np.ndarray] = None
    bbox: Optional[Tuple[int, int, int, int]] = None
    method: str = "unknown"

    def to_dict(self) -> dict:
        d = {"payload": self.payload, "method": self.method}
        if self.bbox:
            x, y, w, h = self.bbox
            d["bbox"] = {"x": x, "y": y, "w": w, "h": h}
        if self.corners is not None:
            d["corners"] = self.corners.astype(float).tolist()
        return d

```

## `src/qrpypass/qr/pipeline.py`

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Dict, Any

from qrpypass.qr.models import QRResult
from qrpypass.qr.scan import scan_qr_anywhere
from qrpypass.classify import ClassifiedPayload, classify_payload


@dataclass(frozen=True)
class ScanHit:
    qr: QRResult
    classification: ClassifiedPayload

    def to_dict(self) -> Dict[str, Any]:
        return {
            "qr": self.qr.to_dict(),
            "classification": self.classification.to_dict(),
        }


def scan_and_classify(image_path: str, *, max_results: int = 8) -> List[ScanHit]:
    """
    High-level pipeline:
      - find/decode QR(s) anywhere in image
      - classify decoded payload(s)
      - return structured results
    """
    hits = scan_qr_anywhere(image_path, max_results=max_results)
    out: List[ScanHit] = []
    for h in hits:
        c = classify_payload(h.payload)
        out.append(ScanHit(qr=h, classification=c))
    return out

```

## `src/qrpypass/qr/scan.py`

```python
from __future__ import annotations

from typing import Dict, List, Optional, Tuple
import cv2
import numpy as np

from .decode import decode_multi, decode_single, QRDecodeError
from .models import QRResult


def _bbox_area(b: Optional[Tuple[int, int, int, int]]) -> int:
    if not b:
        return 10**18
    _, _, w, h = b
    return int(w) * int(h)


def _method_rank(method: str) -> int:
    """
    Lower is better.
    We prefer multi-detection on the full image, then tile, then single.
    """
    m = (method or "").lower()
    if m == "multi":
        return 0
    if m == "tile_multi":
        return 1
    if m == "tile":
        return 2
    if m == "single":
        return 3
    return 9


def _better(a: QRResult, b: QRResult) -> QRResult:
    """
    Return the better of two results for the same payload.
    Priority:
      1) method rank
      2) has bbox/corners
      3) smaller bbox area (tighter localization tends to be more accurate)
    """
    ra, rb = _method_rank(a.method), _method_rank(b.method)
    if ra != rb:
        return a if ra < rb else b

    a_has = (a.bbox is not None) + (a.corners is not None)
    b_has = (b.bbox is not None) + (b.corners is not None)
    if a_has != b_has:
        return a if a_has > b_has else b

    return a if _bbox_area(a.bbox) <= _bbox_area(b.bbox) else b


def scan_qr_anywhere(image_path: str, *, max_results: int = 8) -> List[QRResult]:
    img = cv2.imread(image_path)
    if img is None:
        raise QRDecodeError(f"Image could not be read: {image_path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Collect best result per payload
    best: Dict[str, QRResult] = {}

    def consider(r: QRResult):
        if not r.payload:
            return
        cur = best.get(r.payload)
        best[r.payload] = r if cur is None else _better(cur, r)

    # 1) Try full image first
    for r in decode_multi(gray):
        consider(r)
    for r in decode_single(gray):
        consider(r)

    if best:
        # Return best results sorted by quality, capped
        ordered = sorted(best.values(), key=lambda r: (_method_rank(r.method), _bbox_area(r.bbox)))
        return ordered[:max_results]

    # 2) Fallback tiling for large images
    h, w = gray.shape
    tile = 900
    overlap = 200
    step = max(1, tile - overlap)

    for y in range(0, h, step):
        for x in range(0, w, step):
            crop = gray[y:y + tile, x:x + tile]

            # Prefer multi on tile first
            tile_hits = decode_multi(crop)
            for r in tile_hits:
                mapped_bbox = None
                mapped_corners = None

                if r.bbox:
                    bx, by, bw, bh = r.bbox
                    mapped_bbox = (x + bx, y + by, bw, bh)

                if r.corners is not None:
                    mapped_corners = r.corners.copy()
                    mapped_corners[:, 0] += x
                    mapped_corners[:, 1] += y

                consider(QRResult(
                    payload=r.payload,
                    corners=mapped_corners,
                    bbox=mapped_bbox,
                    method="tile_multi"
                ))

            # Then single on tile
            tile_hits2 = decode_single(crop)
            for r in tile_hits2:
                mapped_bbox = None
                mapped_corners = None

                if r.bbox:
                    bx, by, bw, bh = r.bbox
                    mapped_bbox = (x + bx, y + by, bw, bh)

                if r.corners is not None:
                    mapped_corners = r.corners.copy()
                    mapped_corners[:, 0] += x
                    mapped_corners[:, 1] += y

                consider(QRResult(
                    payload=r.payload,
                    corners=mapped_corners,
                    bbox=mapped_bbox,
                    method="tile"
                ))

            if len(best) >= max_results:
                ordered = sorted(best.values(), key=lambda r: (_method_rank(r.method), _bbox_area(r.bbox)))
                return ordered[:max_results]

    ordered = sorted(best.values(), key=lambda r: (_method_rank(r.method), _bbox_area(r.bbox)))
    return ordered[:max_results]


def decode_first(image_path: str) -> str:
    hits = scan_qr_anywhere(image_path, max_results=1)
    if not hits:
        raise QRDecodeError("No QR code found.")
    return hits[0].payload

```

## `src/qrpypass/service/app.py`

```python
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

from .db import init_db, authenticate, create_user, get_user_by_id, upsert_totp_account, list_totp_accounts, get_totp_account


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
    app.config["MAX_CONTENT_LENGTH"] = int(os.environ.get("QRPYPASS_MAX_UPLOAD_BYTES", str(6 * 1024 * 1024)))

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

```

## `src/qrpypass/service/db.py`

```python
from __future__ import annotations

import os
import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List, Dict, Any

from cryptography.fernet import Fernet
from werkzeug.security import generate_password_hash, check_password_hash


def data_dir() -> Path:
    base = Path(os.environ.get("QRPYPASS_DATA_DIR", Path.home() / ".qrpypass"))
    base.mkdir(parents=True, exist_ok=True)
    return base


def db_path() -> Path:
    return data_dir() / "app.db"


def master_fernet() -> Fernet:
    key = os.environ.get("QRPYPASS_MASTER_KEY", "").strip()
    if not key:
        raise RuntimeError("Missing QRPYPASS_MASTER_KEY (required in multi-user mode)")
    # QRPYPASS_MASTER_KEY must be a Fernet key (urlsafe base64 32 bytes).
    return Fernet(key.encode("utf-8"))


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path()))
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with connect() as c:
        c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            pw_hash TEXT NOT NULL,
            created_at INTEGER NOT NULL
        )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS totp_accounts (
            id TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            issuer TEXT,
            secret_enc BLOB NOT NULL,
            algorithm TEXT NOT NULL,
            digits INTEGER NOT NULL,
            period INTEGER NOT NULL,
            created_at INTEGER NOT NULL,
            UNIQUE(user_id, id),
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """)


@dataclass
class User:
    id: int
    email: str

    # Flask-Login interface
    @property
    def is_authenticated(self) -> bool:  # pragma: no cover
        return True

    @property
    def is_active(self) -> bool:  # pragma: no cover
        return True

    @property
    def is_anonymous(self) -> bool:  # pragma: no cover
        return False

    def get_id(self) -> str:  # pragma: no cover
        return str(self.id)


def create_user(email: str, password: str) -> User:
    email = (email or "").strip().lower()
    if not email or "@" not in email:
        raise ValueError("Invalid email")
    if not password or len(password) < 10:
        raise ValueError("Password must be at least 10 characters")

    pw_hash = generate_password_hash(password)
    now = int(time.time())

    with connect() as c:
        try:
            cur = c.execute(
                "INSERT INTO users (email, pw_hash, created_at) VALUES (?, ?, ?)",
                (email, pw_hash, now),
            )
        except sqlite3.IntegrityError:
            raise ValueError("Email already registered")
        uid = int(cur.lastrowid)
    return User(id=uid, email=email)


def get_user_by_email(email: str) -> Optional[sqlite3.Row]:
    with connect() as c:
        r = c.execute("SELECT * FROM users WHERE email = ?", (email.strip().lower(),)).fetchone()
        return r


def get_user_by_id(user_id: int) -> Optional[User]:
    with connect() as c:
        r = c.execute("SELECT id, email FROM users WHERE id = ?", (int(user_id),)).fetchone()
        if not r:
            return None
        return User(id=int(r["id"]), email=str(r["email"]))


def authenticate(email: str, password: str) -> Optional[User]:
    r = get_user_by_email(email)
    if not r:
        return None
    if not check_password_hash(r["pw_hash"], password):
        return None
    return User(id=int(r["id"]), email=str(r["email"]))


def upsert_totp_account(
    *,
    user_id: int,
    acc_id: str,
    name: str,
    issuer: Optional[str],
    secret_b32: str,
    algorithm: str,
    digits: int,
    period: int,
) -> None:
    f = master_fernet()
    secret_enc = f.encrypt(secret_b32.encode("utf-8"))
    now = int(time.time())

    with connect() as c:
        c.execute(
            """
            INSERT INTO totp_accounts
              (id, user_id, name, issuer, secret_enc, algorithm, digits, period, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
              user_id=excluded.user_id,
              name=excluded.name,
              issuer=excluded.issuer,
              secret_enc=excluded.secret_enc,
              algorithm=excluded.algorithm,
              digits=excluded.digits,
              period=excluded.period
            """,
            (acc_id, int(user_id), name, issuer, secret_enc, algorithm, int(digits), int(period), now),
        )


def list_totp_accounts(user_id: int) -> List[Dict[str, Any]]:
    with connect() as c:
        rows = c.execute(
            "SELECT id, name, issuer, algorithm, digits, period, created_at FROM totp_accounts WHERE user_id = ? ORDER BY created_at DESC",
            (int(user_id),),
        ).fetchall()

    out = []
    for r in rows:
        out.append(
            {
                "id": r["id"],
                "name": r["name"],
                "issuer": r["issuer"],
                "algorithm": r["algorithm"],
                "digits": int(r["digits"]),
                "period": int(r["period"]),
                "created_at": int(r["created_at"]),
            }
        )
    return out


def get_totp_account(user_id: int, acc_id: str) -> Optional[Dict[str, Any]]:
    with connect() as c:
        r = c.execute(
            "SELECT * FROM totp_accounts WHERE user_id = ? AND id = ?",
            (int(user_id), acc_id),
        ).fetchone()
        if not r:
            return None

    f = master_fernet()
    secret_b32 = f.decrypt(r["secret_enc"]).decode("utf-8")

    return {
        "id": r["id"],
        "name": r["name"],
        "issuer": r["issuer"],
        "secret_b32": secret_b32,
        "algorithm": r["algorithm"],
        "digits": int(r["digits"]),
        "period": int(r["period"]),
    }

```

## `src/qrpypass/service/run.py`

```python
from __future__ import annotations

import os
from qrpypass.service.app import create_app

app = create_app()

if __name__ == "__main__":
    host = os.environ.get("QRPYPASS_HOST", "127.0.0.1")
    port = int(os.environ.get("QRPYPASS_PORT", "5000"))
    debug = os.environ.get("QRPYPASS_DEBUG", "0") == "1"
    app.run(host=host, port=port, debug=debug)

```

## `src/qrpypass/service/static/app.js`

```javascript
const form = document.getElementById("uploadForm");
const fileInput = document.getElementById("file");
const maxResults = document.getElementById("maxResults");
const statusEl = document.getElementById("status");
const resultsEl = document.getElementById("results");

const passEl = document.getElementById("passphrase");
const autoImportEl = document.getElementById("autoImportOtp");

// Track active timers so we can stop them on a new scan
const activeIntervals = new Set();

function escapeHtml(s) {
  return String(s)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function stopAllIntervals() {
  for (const id of activeIntervals) clearInterval(id);
  activeIntervals.clear();
}

async function postJson(url, body) {
  const r = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const d = await r.json().catch(() => ({}));
  return { ok: r.ok, status: r.status, data: d };
}

async function getJson(url) {
  const r = await fetch(url, { method: "GET" });
  const d = await r.json().catch(() => ({}));
  return { ok: r.ok, status: r.status, data: d };
}

function renderOtpAuthCard({ idx, rawUri }) {
  // Unique ids for DOM nodes
  const cardId = `otp-card-${idx}`;
  const codeId = `otp-code-${idx}`;
  const remId = `otp-rem-${idx}`;
  const msgId = `otp-msg-${idx}`;
  const btnId = `otp-btn-${idx}`;

  resultsEl.insertAdjacentHTML(
    "beforeend",
    `
    <div class="card" id="${cardId}">
      <div><b>#${idx + 1}</b></div>
      <div><b>kind:</b> otpauth</div>
      <div class="muted">Provisioning URI detected (secret not displayed in UI).</div>

      <div style="margin-top:12px;" class="row">
        <button type="button" id="${btnId}">Import &amp; Show Code</button>
        <span class="muted" id="${msgId}"></span>
      </div>

      <div style="margin-top:12px;">
        <div><b>code</b></div>
        <div style="font-size:28px; font-family: ui-monospace, monospace;" id="${codeId}">—</div>
        <div class="muted" id="${remId}"></div>
      </div>

      <div style="margin-top:12px;">
        <div><b>raw payload</b></div>
        <pre>${escapeHtml(rawUri)}</pre>
      </div>
    </div>
    `
  );

  const btn = document.getElementById(btnId);
  const msgEl = document.getElementById(msgId);
  const codeEl = document.getElementById(codeId);
  const remEl = document.getElementById(remId);

  let accId = null;

  async function refreshCodeOnce() {
    if (!accId) return;
    const passphrase = (passEl.value || "").trim();
    const qs = new URLSearchParams({ id: accId });
    if (passphrase) qs.set("passphrase", passphrase);

    const res = await getJson(`/auth/code?${qs.toString()}`);
    if (!res.ok) {
      msgEl.textContent = "Error: " + (res.data.error || ("HTTP " + res.status));
      return;
    }

    const code = res.data.code || "";
    const remaining = res.data.seconds_remaining;

    codeEl.textContent = code ? code : "—";
    remEl.textContent =
      (typeof remaining === "number")
        ? `refresh in ${remaining}s`
        : "";
  }

  function startLiveRefresh() {
    // Do one immediate fetch, then tick every second
    refreshCodeOnce();

    const intervalId = setInterval(async () => {
      // We intentionally re-fetch each second so countdown stays accurate
      // (and we avoid building a fragile local countdown that drifts).
      await refreshCodeOnce();
    }, 1000);

    activeIntervals.add(intervalId);
  }

  btn.addEventListener("click", async () => {
    msgEl.textContent = "Importing...";
    codeEl.textContent = "—";
    remEl.textContent = "";

    const passphrase = (passEl.value || "").trim();
    const res = await postJson("/auth/import", {
      otpauth_uri: rawUri,
      passphrase: passphrase || null,
    });

    if (!res.ok) {
      msgEl.textContent = "Error: " + (res.data.error || ("HTTP " + res.status));
      return;
    }

    const imported = res.data.imported || {};
    accId = imported.id || null;

    if (!accId) {
      msgEl.textContent = "Import failed (no id returned).";
      return;
    }

    msgEl.textContent = `Imported id: ${accId}`;
    startLiveRefresh();
  });

  // Optional: auto-import if enabled
  const autoImport = !!(autoImportEl && autoImportEl.checked);
  if (autoImport) {
    // Slight delay so DOM is ready, then click programmatically
    setTimeout(() => btn.click(), 0);
  }
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  stopAllIntervals();
  resultsEl.innerHTML = "";
  statusEl.textContent = "Scanning...";

  const f = fileInput.files[0];
  if (!f) {
    statusEl.textContent = "Pick a file first.";
    return;
  }

  const fd = new FormData();
  fd.append("file", f);
  fd.append("max_results", String(maxResults.value || 8));

  try {
    const resp = await fetch("/scan", { method: "POST", body: fd });
    const data = await resp.json();

    if (!resp.ok) {
      statusEl.textContent = "Error: " + (data.error || resp.statusText);
      return;
    }

    statusEl.textContent = `Found ${data.count} result(s).`;

    if (!data.results || data.results.length === 0) {
      resultsEl.innerHTML = `<div class="card"><b>No QR codes decoded.</b></div>`;
      return;
    }

    data.results.forEach((item, idx) => {
      const cls = item.classification || {};
      const qr = item.qr || {};
      const bbox = (qr.bbox) ? JSON.stringify(qr.bbox) : "null";

      // Special handling for otpauth: import + live code
      if (cls.kind === "otpauth" && cls.raw) {
        renderOtpAuthCard({ idx, rawUri: cls.raw });
        return;
      }

      // Default card behavior (URL/TEXT/etc.)
      let extra = "";
      if (cls.kind === "url" && cls.normalized_url) {
        const u = escapeHtml(cls.normalized_url);
        extra = `<div><b>Open:</b> <a href="${u}" target="_blank" rel="noreferrer">${u}</a></div>`;
      }

      resultsEl.insertAdjacentHTML("beforeend", `
        <div class="card">
          <div><b>#${idx + 1}</b></div>
          <div><b>kind:</b> ${escapeHtml(cls.kind || "unknown")}</div>
          <div><b>method:</b> ${escapeHtml(qr.method || "unknown")}</div>
          <div><b>bbox:</b> <span class="muted">${escapeHtml(bbox)}</span></div>
          ${extra}
          <div style="margin-top:10px;"><b>raw payload</b></div>
          <pre>${escapeHtml(cls.raw || "")}</pre>
        </div>
      `);
    });

  } catch (err) {
    statusEl.textContent = "Error: " + err;
  }
});

```

## `src/qrpypass/service/static/gen.js`

```javascript
// src/qrpypass/service/static/gen.js
(() => {
  const kindEl = document.getElementById("kind");
  const fieldsEl = document.getElementById("fields");
  const statusEl = document.getElementById("status");
  const outEl = document.getElementById("out");
  const btnGen = document.getElementById("btnGen");
  const importEl = document.getElementById("doImport");

  // Optional: recent UI removed this input, so it may be null.
  const passEl = document.getElementById("passphrase");

  // Track last blob URL so we can revoke it (avoid leaking memory)
  let lastObjUrl = null;

  function esc(s) {
    return String(s)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;");
  }

  function fieldRow(html) {
    return `<div class="row" style="margin-top:10px;">${html}</div>`;
  }

  function renderFields() {
    const k = kindEl.value;

    if (k === "url") {
      fieldsEl.innerHTML = fieldRow(`
        <input id="url" style="flex:1" placeholder="https://example.com" />
      `);
      return;
    }

    if (k === "text") {
      fieldsEl.innerHTML = `
        <textarea id="text" rows="4" style="width:100%; padding:10px;" placeholder="Any text payload."></textarea>
      `;
      return;
    }

    // totp (otpauth)
    fieldsEl.innerHTML = `
      ${fieldRow(`
        <input id="issuer" placeholder="issuer (e.g. ACME)" />
        <input id="account_name" placeholder="account (e.g. alice@example.com)" style="min-width:280px;" />
      `)}
      ${fieldRow(`
        <label>digits <input id="digits" type="number" min="6" max="8" value="6" /></label>
        <label>period <input id="period" type="number" min="5" max="300" value="30" /></label>
        <label>algorithm
          <select id="algorithm">
            <option value="SHA1">SHA1</option>
            <option value="SHA256">SHA256</option>
            <option value="SHA512">SHA512</option>
          </select>
        </label>
        <label>nbytes <input id="nbytes" type="number" min="10" max="64" value="20" /></label>
      `)}
      <div class="muted" style="margin-top:8px;">
        Secret is generated server-side unless you extend the UI to supply one.
      </div>
    `;
  }

  async function postJson(url, body) {
    const r = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const d = await r.json().catch(() => ({}));
    return { ok: r.ok, status: r.status, data: d };
  }

  function clearOldPreviewUrl() {
    if (lastObjUrl) {
      try {
        URL.revokeObjectURL(lastObjUrl);
      } catch (_) {}
      lastObjUrl = null;
    }
  }

  function buildParams(kind) {
    const params = {};

    if (kind === "url") {
      params.url = (document.getElementById("url")?.value || "").trim();
      return params;
    }

    if (kind === "text") {
      params.text = (document.getElementById("text")?.value || "").trim();
      return params;
    }

    // totp
    params.issuer = (document.getElementById("issuer")?.value || "").trim();
    params.account_name = (document.getElementById("account_name")?.value || "").trim();
    params.digits = Number(document.getElementById("digits")?.value || 6);
    params.period = Number(document.getElementById("period")?.value || 30);
    params.algorithm = (document.getElementById("algorithm")?.value || "SHA1").trim();
    params.nbytes = Number(document.getElementById("nbytes")?.value || 20);
    return params;
  }

  function suggestFilename(kind) {
    const ts = new Date().toISOString().replaceAll(":", "-").replaceAll(".", "-");
    if (kind === "url") return `qr-url-${ts}.png`;
    if (kind === "text") return `qr-text-${ts}.png`;
    return `qr-totp-${ts}.png`;
  }

  btnGen.addEventListener("click", async () => {
    outEl.innerHTML = "";
    statusEl.textContent = "Generating...";
    clearOldPreviewUrl();

    try {
      const k = kindEl.value;
      const params = buildParams(k);

      // Optional passphrase (safe if input removed)
      const passphrase = passEl ? (passEl.value || "").trim() : "";
      const doImport = !!(importEl && importEl.checked);

      // 1) Generate payload
      const res = await postJson("/gen/payload", {
        kind: k,
        params,
        import: doImport,
        passphrase: passphrase || null,
      });

      if (!res.ok) {
        statusEl.textContent = "Error: " + (res.data.error || ("HTTP " + res.status));
        return;
      }

      const gen = res.data.generated || {};
      const payload = gen.payload || "";

      // 2) Render QR png from payload
      const qrResp = await fetch("/gen/qr", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ payload, box_size: 8, border: 2 }),
      });

      let previewHtml = "";
      if (qrResp.ok) {
        const blob = await qrResp.blob();
        const objUrl = URL.createObjectURL(blob);
        lastObjUrl = objUrl;

        const filename = suggestFilename(k);

        previewHtml = `
          <div class="card">
            <div class="row" style="justify-content:space-between; align-items:center;">
              <div><b>QR preview</b></div>
              <a class="btn" href="${objUrl}" download="${esc(filename)}">Download PNG</a>
            </div>
            <div style="margin-top:10px;">
              <img src="${objUrl}" alt="qr" style="max-width:360px; width:100%; height:auto; border-radius:10px;" />
            </div>
          </div>
        `;
      } else {
        // Attempt to surface server error text if any
        let msg = "";
        try {
          msg = await qrResp.text();
        } catch (_) {}
        previewHtml = `
          <div class="card">
            <b>QR render failed</b>
            <div class="muted">HTTP ${qrResp.status}${msg ? " :: " + esc(msg.slice(0, 300)) : ""}</div>
          </div>
        `;
      }

      // 3) Show details
      const metaJson = esc(JSON.stringify(gen.meta || {}, null, 2));
      const payloadEsc = esc(payload);

      statusEl.textContent = "Generated.";

      outEl.innerHTML = `
        ${previewHtml}
        <div class="card">
          <div><b>kind:</b> ${esc(gen.kind || "")}</div>

          <div style="margin-top:10px;" class="row">
            <button type="button" id="btnCopyPayload">Copy payload</button>
            ${res.data.imported && res.data.imported.id
              ? `<span class="muted">Imported id: ${esc(res.data.imported.id)}</span>`
              : `<span class="muted">${doImport ? "Import requested (no id returned)." : ""}</span>`}
          </div>

          <div style="margin-top:10px;"><b>payload</b></div>
          <pre id="payloadPre">${payloadEsc}</pre>

          <div style="margin-top:10px;"><b>meta</b></div>
          <pre>${metaJson}</pre>
        </div>
      `;

      // Copy button handler
      const btnCopy = document.getElementById("btnCopyPayload");
      if (btnCopy) {
        btnCopy.addEventListener("click", async () => {
          try {
            await navigator.clipboard.writeText(payload);
            btnCopy.textContent = "Copied";
            setTimeout(() => (btnCopy.textContent = "Copy payload"), 900);
          } catch (e) {
            btnCopy.textContent = "Copy failed";
            setTimeout(() => (btnCopy.textContent = "Copy payload"), 1200);
          }
        });
      }
    } catch (err) {
      statusEl.textContent = "Error: " + (err?.message || String(err));
    }
  });

  kindEl.addEventListener("change", renderFields);
  renderFields();
})();

```

## `src/qrpypass/service/static/style.css`

```css
/* Modern dark theme (no framework) */
:root{
  color-scheme: dark;

  --bg: #0b0f17;
  --panel: rgba(255,255,255,0.06);
  --panel-2: rgba(255,255,255,0.04);
  --border: rgba(255,255,255,0.12);
  --border-2: rgba(255,255,255,0.08);
  --text: rgba(255,255,255,0.92);
  --muted: rgba(255,255,255,0.62);
  --accent: rgba(120, 180, 255, 0.95);
  --danger: rgba(255, 120, 140, 0.95);

  --radius: 14px;
  --shadow: 0 10px 30px rgba(0,0,0,0.35);
}

*{ box-sizing: border-box; }

html, body { height: 100%; }

body{
  margin: 0;
  font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
  background:
    radial-gradient(1000px 700px at 10% 0%, rgba(120,180,255,0.18), transparent 55%),
    radial-gradient(900px 600px at 90% 10%, rgba(255,120,140,0.10), transparent 55%),
    var(--bg);
  color: var(--text);
}

.container{
  max-width: 980px;
  margin: 0 auto;
  padding: 18px 20px 48px;
}

.topbar{
  position: sticky;
  top: 0;
  z-index: 10;
  backdrop-filter: blur(12px);
  background: linear-gradient(to bottom, rgba(11,15,23,0.86), rgba(11,15,23,0.65));
  border-bottom: 1px solid var(--border-2);
  padding: 14px 20px;
}

.topbar .brand{
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo{
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: grid;
  place-items: center;
  font-weight: 800;
  letter-spacing: 0.4px;
  background: linear-gradient(135deg, rgba(120,180,255,0.35), rgba(255,120,140,0.25));
  border: 1px solid var(--border);
  box-shadow: var(--shadow);
}

.title{
  font-size: 16px;
  font-weight: 750;
  line-height: 1.1;
}

.subtitle{
  font-size: 12px;
  color: var(--muted);
  line-height: 1.2;
}

.nav{
  margin-top: 10px;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.navlink{
  text-decoration: none;
  color: var(--muted);
  padding: 8px 10px;
  border-radius: 10px;
  border: 1px solid transparent;
  background: transparent;
}

.navlink:hover{
  color: var(--text);
  border-color: var(--border-2);
  background: rgba(255,255,255,0.03);
}

.navlink.active{
  color: var(--text);
  border-color: var(--border);
  background: rgba(255,255,255,0.05);
}

.navlink.danger{
  color: rgba(255,255,255,0.86);
}
.navlink.danger:hover{
  border-color: rgba(255,120,140,0.35);
  background: rgba(255,120,140,0.12);
}

h1{
  margin: 0;
  font-size: 18px;
}

.row{
  display:flex;
  gap: 14px;
  flex-wrap: wrap;
  align-items: center;
}

.card{
  background: var(--panel);
  border: 1px solid var(--border-2);
  border-radius: var(--radius);
  padding: 16px;
  box-shadow: var(--shadow);
  margin-top: 16px;
}

.card.subtle{
  background: var(--panel-2);
  box-shadow: none;
}

.muted{ color: var(--muted); }

pre{
  white-space: pre-wrap;
  word-break: break-word;
  padding: 12px;
  border-radius: 12px;
  border: 1px solid var(--border-2);
  background: rgba(0,0,0,0.18);
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  margin: 10px 0 0;
}

label{
  display:flex;
  gap: 8px;
  align-items: center;
  color: var(--muted);
}

select,
input[type="number"],
input[type="password"],
input[type="email"],
input[type="file"],
input[type="text"],
textarea{
  font-family: inherit;
  padding: 10px 12px;
  border-radius: 12px;
  border: 1px solid var(--border-2);
  background: rgba(0,0,0,0.20);
  color: var(--text);
  outline: none;
}

select:focus,
input:focus,
textarea:focus{
  border-color: rgba(120,180,255,0.45);
  box-shadow: 0 0 0 4px rgba(120,180,255,0.10);
}

button{
  padding: 10px 14px;
  border-radius: 12px;
  border: 1px solid var(--border);
  background: rgba(255,255,255,0.06);
  color: var(--text);
  font-family: inherit;
  cursor: pointer;
}

button:hover{
  background: rgba(255,255,255,0.10);
}

button:active{
  transform: translateY(1px);
}

a{ color: var(--accent); }

.otp{
  font-size: 26px;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  letter-spacing: 1.5px;
  padding: 6px 10px;
  border-radius: 12px;
  border: 1px solid var(--border-2);
  background: rgba(0,0,0,0.18);
  min-width: 120px;
  text-align: center;
}

```

## `src/qrpypass/service/templates/gen.html`

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>qr-pypass generator</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
<!-- qrpypass:favicons:begin -->
<link rel="icon" href="{{ url_for('static', filename='favicon.ico') }}?v=20260103071729">
<link rel="icon" type="image/png" sizes="32x32" href="{{ url_for('static', filename='favicon-32.png') }}?v=20260103071729">
<link rel="icon" type="image/png" sizes="16x16" href="{{ url_for('static', filename='favicon-16.png') }}?v=20260103071729">
<link rel="apple-touch-icon" sizes="180x180" href="{{ url_for('static', filename='apple-touch-icon-180.png') }}?v=20260103071729">
<link rel="icon" type="image/png" sizes="512x512" href="{{ url_for('static', filename='icon-512.png') }}?v=20260103071729">
<!-- qrpypass:favicons:end -->
</head>
<body>

  <!-- Header / Nav -->
  <header class="topbar">
    <div class="brand">
      <div class="logo">qp</div>
      <div>
        <div class="title">qr-pypass</div>
        <div class="subtitle">Generator</div>
      </div>
    </div>

    <nav class="nav">
      <a class="navlink" href="{{ url_for('index') }}">Scan</a>
      <a class="navlink active" href="{{ url_for('gen_page') }}">Generate</a>
      <a class="navlink" href="{{ url_for('vault') }}">Vault</a>
      <a class="navlink danger" href="{{ url_for('logout') }}">Logout</a>
    </nav>
  </header>

  <main class="container">
    <p class="muted">
      Generate payloads (URL/Text/TOTP) and render them as QR codes.
    </p>

    <section class="card">
      <div class="row">
        <label>type
          <select id="kind">
            <option value="url">URL</option>
            <option value="text">Text</option>
            <option value="totp">TOTP (otpauth)</option>
          </select>
        </label>

        <label class="row" style="gap:8px;">
          <input id="doImport" type="checkbox" />
          import (TOTP only)
        </label>

        <!-- passphrase removed (multi-user server-side encryption) -->

        <button id="btnGen" type="button">Generate</button>
      </div>

      <div id="fields" style="margin-top:12px;"></div>

      <p id="status" class="muted"></p>
    </section>

    <div id="out"></div>
  </main>

  <script src="{{ url_for('static', filename='gen.js') }}"></script>
</body>
</html>

```

## `src/qrpypass/service/templates/index.html`

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>qr-pypass</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
<!-- qrpypass:favicons:begin -->
<link rel="icon" href="{{ url_for('static', filename='favicon.ico') }}?v=20260103071729">
<link rel="icon" type="image/png" sizes="32x32" href="{{ url_for('static', filename='favicon-32.png') }}?v=20260103071729">
<link rel="icon" type="image/png" sizes="16x16" href="{{ url_for('static', filename='favicon-16.png') }}?v=20260103071729">
<link rel="apple-touch-icon" sizes="180x180" href="{{ url_for('static', filename='apple-touch-icon-180.png') }}?v=20260103071729">
<link rel="icon" type="image/png" sizes="512x512" href="{{ url_for('static', filename='icon-512.png') }}?v=20260103071729">
<!-- qrpypass:favicons:end -->
</head>
<body>

  <header class="topbar">
    <div class="brand">
      <div class="logo">qp</div>
      <div>
        <div class="title">qr-pypass</div>
        <div class="subtitle">Scanner</div>
      </div>
    </div>

    <nav class="nav">
      <a class="navlink active" href="{{ url_for('index') }}">Scan</a>
      <a class="navlink" href="{{ url_for('gen_page') }}">Generate</a>
      <a class="navlink" href="{{ url_for('vault') }}">Vault</a>
      <a class="navlink danger" href="{{ url_for('logout') }}">Logout</a>
    </nav>
  </header>

  <main class="container">
    <p class="muted">
      Upload a screenshot or photo containing QR codes. Authenticator (otpauth) QRs can be imported and will generate live codes.
    </p>

    <section class="card">
      <form id="uploadForm" class="row">
        <input id="file" type="file" accept="image/*" required />

        <label>max_results
          <input id="maxResults" type="number" min="1" max="50" value="8" />
        </label>

        <label class="row" style="gap:8px;">
          <input id="autoImportOtp" type="checkbox" checked />
          auto-import otpauth
        </label>

        <button type="submit">Scan</button>
      </form>

      <p id="status" class="muted"></p>
    </section>

    <div id="results"></div>
  </main>

  <script src="{{ url_for('static', filename='app.js') }}"></script>
</body>
</html>

```

## `src/qrpypass/service/templates/login.html`

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>qr-pypass login</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
<!-- qrpypass:favicons:begin -->
<link rel="icon" href="{{ url_for('static', filename='favicon.ico') }}?v=20260103071729">
<link rel="icon" type="image/png" sizes="32x32" href="{{ url_for('static', filename='favicon-32.png') }}?v=20260103071729">
<link rel="icon" type="image/png" sizes="16x16" href="{{ url_for('static', filename='favicon-16.png') }}?v=20260103071729">
<link rel="apple-touch-icon" sizes="180x180" href="{{ url_for('static', filename='apple-touch-icon-180.png') }}?v=20260103071729">
<link rel="icon" type="image/png" sizes="512x512" href="{{ url_for('static', filename='icon-512.png') }}?v=20260103071729">
<!-- qrpypass:favicons:end -->
</head>
<body>

  <header class="topbar">
    <div class="brand">
      <div class="logo">qp</div>
      <div>
        <div class="title">qr-pypass</div>
        <div class="subtitle">Sign in</div>
      </div>
    </div>

    <nav class="nav">
      <a class="navlink active" href="{{ url_for('login') }}">Login</a>
      <a class="navlink" href="{{ url_for('register') }}">Register</a>
    </nav>
  </header>

  <main class="container">
    <section class="card">
      <h1 style="margin-bottom:8px;">Login</h1>
      <p class="muted" style="margin-top:0;">
        Sign in to scan, import authenticators, and view your vault.
      </p>

      <form method="POST" class="row" style="margin-top:14px;">
        <label>
          email
          <input name="email" type="email" placeholder="you@example.com" required style="min-width:320px;" />
        </label>

        <label>
          password
          <input name="password" type="password" placeholder="••••••••••" required style="min-width:260px;" />
        </label>

        <button type="submit">Sign in</button>
      </form>

      {% if error %}
        <div class="card subtle" style="margin-top:14px; border-color: rgba(255,120,140,0.25);">
          <div><b>Login failed</b></div>
          <div class="muted">{{ error }}</div>
        </div>
      {% endif %}

      <p class="muted" style="margin-top:14px;">
        New here? <a href="{{ url_for('register') }}">Create an account</a>
      </p>
    </section>
  </main>

</body>
</html>

```

## `src/qrpypass/service/templates/register.html`

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>qr-pypass register</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
<!-- qrpypass:favicons:begin -->
<link rel="icon" href="{{ url_for('static', filename='favicon.ico') }}?v=20260103071729">
<link rel="icon" type="image/png" sizes="32x32" href="{{ url_for('static', filename='favicon-32.png') }}?v=20260103071729">
<link rel="icon" type="image/png" sizes="16x16" href="{{ url_for('static', filename='favicon-16.png') }}?v=20260103071729">
<link rel="apple-touch-icon" sizes="180x180" href="{{ url_for('static', filename='apple-touch-icon-180.png') }}?v=20260103071729">
<link rel="icon" type="image/png" sizes="512x512" href="{{ url_for('static', filename='icon-512.png') }}?v=20260103071729">
<!-- qrpypass:favicons:end -->
</head>
<body>

  <header class="topbar">
    <div class="brand">
      <div class="logo">qp</div>
      <div>
        <div class="title">qr-pypass</div>
        <div class="subtitle">Create account</div>
      </div>
    </div>

    <nav class="nav">
      <a class="navlink" href="{{ url_for('login') }}">Login</a>
      <a class="navlink active" href="{{ url_for('register') }}">Register</a>
    </nav>
  </header>

  <main class="container">
    <section class="card">
      <h1 style="margin-bottom:8px;">Register</h1>
      <p class="muted" style="margin-top:0;">
        Create an account. Use a strong password (10+ characters).
      </p>

      <form method="POST" class="row" style="margin-top:14px;">
        <label>
          email
          <input name="email" type="email" placeholder="you@example.com" required style="min-width:320px;" />
        </label>

        <label>
          password
          <input name="password" type="password" placeholder="10+ characters" required style="min-width:260px;" />
        </label>

        <button type="submit">Create</button>
      </form>

      <div class="card subtle" style="margin-top:14px;">
        <div><b>Password tips</b></div>
        <div class="muted">Use a long passphrase. Avoid reusing a password from other sites.</div>
      </div>

      {% if error %}
        <div class="card subtle" style="margin-top:14px; border-color: rgba(255,120,140,0.25);">
          <div><b>Registration failed</b></div>
          <div class="muted">{{ error }}</div>
        </div>
      {% endif %}

      <p class="muted" style="margin-top:14px;">
        Already have an account? <a href="{{ url_for('login') }}">Sign in</a>
      </p>
    </section>
  </main>

</body>
</html>

```

## `src/qrpypass/service/templates/vault.html`

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>qr-pypass vault</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
<!-- qrpypass:favicons:begin -->
<link rel="icon" href="{{ url_for('static', filename='favicon.ico') }}?v=20260103071729">
<link rel="icon" type="image/png" sizes="32x32" href="{{ url_for('static', filename='favicon-32.png') }}?v=20260103071729">
<link rel="icon" type="image/png" sizes="16x16" href="{{ url_for('static', filename='favicon-16.png') }}?v=20260103071729">
<link rel="apple-touch-icon" sizes="180x180" href="{{ url_for('static', filename='apple-touch-icon-180.png') }}?v=20260103071729">
<link rel="icon" type="image/png" sizes="512x512" href="{{ url_for('static', filename='icon-512.png') }}?v=20260103071729">
<!-- qrpypass:favicons:end -->
</head>
<body>

  <header class="topbar">
    <div class="brand">
      <div class="logo">qp</div>
      <div>
        <div class="title">qr-pypass</div>
        <div class="subtitle">Vault</div>
      </div>
    </div>

    <nav class="nav">
      <a class="navlink" href="{{ url_for('index') }}">Scan</a>
      <a class="navlink" href="{{ url_for('gen_page') }}">Generate</a>
      <a class="navlink active" href="{{ url_for('vault') }}">Vault</a>
      <a class="navlink danger" href="{{ url_for('logout') }}">Logout</a>
    </nav>
  </header>

  <main class="container">
    <p class="muted">Your stored authenticators. Click to show live code.</p>

    <section class="card">
      <div id="vault"></div>
      <p id="status" class="muted"></p>
    </section>
  </main>

  <script>
    async function getJson(url){
      const r = await fetch(url, {method:"GET"});
      const d = await r.json().catch(() => ({}));
      return {ok:r.ok, status:r.status, data:d};
    }

    const vaultEl = document.getElementById("vault");
    const statusEl = document.getElementById("status");
    const intervals = new Set();

    function stopAll(){ for (const i of intervals) clearInterval(i); intervals.clear(); }
    function esc(s){ return String(s).replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;"); }

    async function refreshOne(id){
      const res = await getJson(`/auth/code?id=${encodeURIComponent(id)}`);
      if (!res.ok) return null;
      return res.data;
    }

    async function load(){
      stopAll();
      statusEl.textContent = "Loading...";
      const res = await getJson("/auth/list");
      if (!res.ok){
        statusEl.textContent = "Error loading vault.";
        return;
      }
      const accts = res.data.accounts || [];
      statusEl.textContent = `Accounts: ${accts.length}`;

      vaultEl.innerHTML = accts.map(a => `
        <div class="card subtle">
          <div><b>${esc(a.issuer || "")}</b> ${esc(a.name || "")}</div>
          <div class="muted">id: ${esc(a.id)}</div>
          <div style="margin-top:10px;" class="row">
            <button type="button" data-id="${esc(a.id)}">Show code</button>
            <div class="otp" id="code-${esc(a.id)}">—</div>
            <div class="muted" id="rem-${esc(a.id)}"></div>
          </div>
        </div>
      `).join("");

      vaultEl.querySelectorAll("button[data-id]").forEach(btn => {
        btn.addEventListener("click", async () => {
          const id = btn.getAttribute("data-id");
          const codeEl = document.getElementById(`code-${id}`);
          const remEl  = document.getElementById(`rem-${id}`);

          async function tick(){
            const d = await refreshOne(id);
            if (!d) return;
            codeEl.textContent = d.code || "—";
            remEl.textContent = (typeof d.seconds_remaining === "number") ? `refresh in ${d.seconds_remaining}s` : "";
          }

          await tick();
          const intv = setInterval(tick, 1000);
          intervals.add(intv);
        });
      });
    }

    load();
  </script>
</body>
</html>

```

## `test/api-test.py`

```python
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

```

## `test/full_api_smoke.py`

```python
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

```

## `test/test_totp_verify_flow.py`

```python
#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from urllib.request import Request, urlopen

BASE = "http://127.0.0.1:5000"

def post_json(path: str, obj: dict) -> dict:
    url = BASE + path
    req = Request(url, data=json.dumps(obj).encode("utf-8"), headers={"Content-Type":"application/json"}, method="POST")
    with urlopen(req, timeout=20) as r:
        data = json.loads(r.read().decode("utf-8"))
        if r.status >= 400:
            raise RuntimeError(f"{path} -> HTTP {r.status}: {data}")
        return data

def get_json(path: str) -> dict:
    url = BASE + path
    req = Request(url, method="GET")
    with urlopen(req, timeout=20) as r:
        data = json.loads(r.read().decode("utf-8"))
        if r.status >= 400:
            raise RuntimeError(f"{path} -> HTTP {r.status}: {data}")
        return data

def main():
    # 1) generate a totp otpauth URI (no import)
    gen = post_json("/gen/payload", {
        "kind": "totp",
        "params": {"issuer":"QRPYPASS", "account_name":"verify-test@local", "digits":6, "period":30, "algorithm":"SHA1"},
        "import": False
    })
    uri = gen["generated"]["payload"]
    print("[gen] uri:", uri[:80] + "...")

    # 2) import it
    imp = post_json("/auth/import", {"otpauth_uri": uri})
    acc_id = imp["imported"]["id"]
    print("[import] id:", acc_id)

    # 3) get current code
    code_resp = get_json(f"/auth/code?id={acc_id}")
    code = code_resp["code"]
    print("[code] code:", code, "remaining:", code_resp["seconds_remaining"])

    # 4) verify the code
    ver = post_json("/auth/verify", {"id": acc_id, "code": code, "window": 1})
    print("[verify] ok:", ver["ok"], "offset:", ver["matched_offset"])
    if not ver["ok"]:
        raise RuntimeError("Expected verify to succeed")

    # 5) verify a bad code
    bad = post_json("/auth/verify", {"id": acc_id, "code": "000000", "window": 1})
    print("[verify-bad] ok:", bad["ok"])
    if bad["ok"]:
        raise RuntimeError("Expected verify to fail")

    print("All good.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("FAIL:", e, file=sys.stderr)
        raise

```

<details>
<summary>📁 Final Project Structure</summary>

```
📁 _data/
    📄 app.db
📁 dist/
    📄 qrpypass-0.1.2-py3-none-any.whl
    📄 qrpypass-0.1.2.tar.gz
📁 images/
    📄 qr-logo.png
    📄 qr.png
📁 src/
    📁 qrpypass/
        📁 auth/
            📄 __init__.py
            📄 generate.py
            📄 models.py
            📄 otpauth.py
            📄 store.py
            📄 totp.py
        📁 classify/
            📄 __init__.py
            📄 models.py
            📄 payload.py
        📁 generate/
            📄 __init__.py
            📄 models.py
            📄 payloads.py
        📁 qr/
            📄 __init__.py
            📄 decode.py
            📄 models.py
            📄 pipeline.py
            📄 scan.py
        📁 service/
            📁 static/
                📄 app.js
                📄 apple-touch-icon-180.png
                📄 favicon-16.png
                📄 favicon-32.png
                📄 favicon-48.png
                📄 favicon.ico
                📄 gen.js
                📄 icon-512.png
                📄 style.css
            📁 templates/
                📄 gen.html
                📄 index.html
                📄 login.html
                📄 register.html
                📄 vault.html
            📄 app.py
            📄 db.py
            📄 run.py
        📄 __init__.py
    📁 qrpypass.egg-info/
        📄 dependency_links.txt
        📄 PKG-INFO
        📄 SOURCES.txt
        📄 top_level.txt
📁 test/
    📁 api_test_out/
        📄 text.png
        📄 totp.png
        📄 url.png
    📄 api-test.py
    📄 full_api_smoke.py
    📄 test_totp_verify_flow.py
📄 gitignore
📄 pyproject.toml
📄 README.md
📄 requirements.txt
📄 setup.py
```

</details>
