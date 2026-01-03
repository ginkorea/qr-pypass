# qr-pypass

**qr-pypass** is a lightweight, headless QR decoding and TOTP authentication service.  
It is designed for air-gapped labs, automation pipelines, and security tooling where you need to:

- Decode QR codes from screenshots or images
- Classify QR payloads (URL, text, otpauth)
- Generate QR codes programmatically
- Generate, import, store, and verify TOTP (RFC 6238) secrets
- Run everything locally with no cloud dependencies

The project exposes both a **Python API** and a **Flask-based HTTP service with a minimal web UI**.

---

## Features

### QR Decoding
- Detects **multiple QR codes anywhere in an image**
- Uses OpenCV with multi-pass detection and tiling fallback
- Returns bounding boxes, corners, and decode method
- Robust against screenshots, partial QRs, and large images

### Payload Classification
Automatically classifies decoded QR payloads as:
- `url` (with normalization)
- `text`
- `otpauth` (TOTP provisioning URIs)

### TOTP / OTPAuth
- Generate RFC-compliant `otpauth://totp` URIs
- Import existing provisioning URIs
- Secure local storage (optional encryption at rest)
- Generate current TOTP codes
- Verify TOTP codes with configurable window

### QR Generation
- Generate QR codes for:
  - URLs
  - Arbitrary text
  - TOTP provisioning URIs
- Control box size and border
- Returns PNG images

### Service + UI
- Flask API
- Minimal web UI for:
  - Uploading screenshots
  - Viewing decoded QR payloads
  - Generating QR codes
  - Managing TOTP accounts

---

## Installation

```bash
git clone https://github.com/ginkorea/qr-pypass.git
cd qr-pypass

python -m venv .qr-env
source .qr-env/bin/activate

pip install -r requirements.txt
pip install -e .
````

Python **3.9+** is required.

---

## Running the Service

```bash
python -m qrpypass.service.run
```

By default the service runs on:

```
http://127.0.0.1:5000
```

### Environment Variables

| Variable             | Default       | Description               |
| -------------------- | ------------- | ------------------------- |
| `QRPYPASS_HOST`      | `127.0.0.1`   | Bind address              |
| `QRPYPASS_PORT`      | `5000`        | Port                      |
| `QRPYPASS_DEBUG`     | `0`           | Enable Flask debug        |
| `QRPYPASS_STORE_DIR` | `~/.qrpypass` | Account storage directory |

---

## Web UI

* `/` – QR scan UI (upload screenshots/images)
* `/gen` – QR payload + TOTP generator

No JavaScript frameworks, no external assets.

---

## API Overview

### Health Check

```http
GET /health
```

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
  "params": { ... },
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

Optional `passphrase` encrypts the store at rest.

---

## Python API Example

```python
from qrpypass.qr import scan_and_classify

hits = scan_and_classify("screenshot.png")
for h in hits:
    print(h.classification.kind, h.qr.payload)
```

---

## Testing

End-to-end API tests are included:

```bash
python test/api-test.py
python test/full_api_smoke.py
python test/test_totp_verify_flow.py
```

These tests cover:

* QR generation → scan → classification
* TOTP generation, import, code generation, and verification

---

## Security Notes

* Secrets are never logged
* TOTP store can be encrypted using a passphrase
* No outbound network access
* Suitable for air-gapped or lab environments

---

## Use Cases

* QR extraction from screenshots (2FA enrollment, phishing analysis)
* Headless TOTP verification in security tooling
* Red-team / blue-team labs
* Offline QR decoding pipelines
* Lightweight local alternative to mobile authenticator apps

---

## License

MIT

---

## Author

**Josh Gompert**

---

