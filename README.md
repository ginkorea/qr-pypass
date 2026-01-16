# qr-pypass

![qr-pypass logo](images/qr-logo.png)

**qr-pypass** is a **local-first, headless QR decoding and TOTP service** designed for **security workflows, air-gapped environments, and automation pipelines**.

It is built to reliably decode *real-world QR codes* such as phone screenshots, camera photos, cropped images, and distorted captures — without cloud APIs, mobile devices, or external services.

The project now uses **state-of-the-art QR detection via OpenCV’s WeChat QR detector**, which significantly outperforms legacy ZXing-style decoders on modern smartphone imagery.

**Homepage:** [https://ginkorea.one](https://ginkorea.one)
**Source:** [https://github.com/ginkorea/qr-pypass](https://github.com/ginkorea/qr-pypass)
**PyPI:** [https://pypi.org/project/qrpypass/](https://pypi.org/project/qrpypass/)

---

## Why qr-pypass Exists

Most QR libraries work well only for:

• perfectly cropped QR codes
• synthetic QR images
• ideal lighting and contrast

They often fail on:

• phone screenshots
• camera photos
• skewed or rotated QRs
• partial codes
• high-resolution images

**qr-pypass is designed for the messiness of reality.**

It was built for red teams, blue teams, labs, SOC tooling, and automation where QR and 2FA artifacts need to be decoded **locally and reliably**.

---

## Core Capabilities

### QR Detection and Decoding

* **WeChat QR detector (OpenCV contrib)** — primary engine
* Detects **multiple QR codes per image**
* Handles:

  * screenshots
  * camera photos
  * large images
  * rotated or skewed QRs
* Returns:

  * decoded payload
  * bounding box
  * corner points
  * detection method used

WeChat QR is now the **first-pass detector** and succeeds on cases where older approaches fail.

---

### Payload Classification

Decoded payloads are automatically classified as:

* `url`
* `text`
* `otpauth` (RFC-compliant TOTP provisioning URIs)

This allows direct routing into downstream automation or security workflows.

---

### TOTP / OTPAuth Support

* Generate RFC-6238 compliant TOTP secrets
* Import existing `otpauth://totp` URIs
* Store secrets locally (optionally encrypted at rest)
* Generate current TOTP codes
* Verify TOTP codes with configurable time drift

This enables **headless authenticator workflows** without phones or apps.

---

### QR Generation

Generate QR codes for:

* URLs
* arbitrary text
* TOTP provisioning URIs

Options include:

* configurable box size
* configurable border
* PNG output

---

### HTTP Service + Minimal UI

`qr-pypass` exposes:

* a **Python API**
* a **Flask-based HTTP service**
* a **minimal web UI**

No JavaScript frameworks.
No external assets.
No cloud calls.

---

## Installation

### From PyPI

```bash
pip install qrpypass
```

Python **3.9+** required.

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

Default address:

```
http://127.0.0.1:5000
```

---

## Configuration

Environment variables:

| Variable             | Default       | Description                |
| -------------------- | ------------- | -------------------------- |
| `QRPYPASS_HOST`      | `127.0.0.1`   | Bind address               |
| `QRPYPASS_PORT`      | `5000`        | Port                       |
| `QRPYPASS_DEBUG`     | `0`           | Flask debug mode           |
| `QRPYPASS_QR_DEBUG`  | `0`           | QR detection debug logging |
| `QRPYPASS_STORE_DIR` | `~/.qrpypass` | Local TOTP storage         |

---

## Web UI Routes

* `/` — QR scan UI (upload screenshots or photos)
* `/gen` — payload and QR generator
* `/vault` — TOTP account management

---

## HTTP API Overview

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

* `file` (required)
* `max_results` (optional, default: 8)

Returns structured detection results including bounding boxes.

---

### Generate Payload

```http
POST /gen/payload
Content-Type: application/json
```

```json
{
  "kind": "url | text | totp",
  "params": {},
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

| Endpoint            | Description        |
| ------------------- | ------------------ |
| `POST /auth/import` | Import otpauth URI |
| `GET /auth/list`    | List accounts      |
| `GET /auth/code`    | Get current code   |
| `POST /auth/verify` | Verify code        |

Optional passphrase enables encryption at rest.

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

Included end-to-end tests:

```bash
python test/api-test.py
python test/full_api_smoke.py
python test/test_totp_verify_flow.py
```

Covers:

* QR generation → scan → classification
* TOTP generation, import, code, and verification

---

## Security Model

* No outbound network access
* Secrets never logged
* Optional encryption at rest
* Designed for offline and air-gapped use

---

## Common Use Cases

* Extract QR payloads from screenshots
* Analyze phishing or 2FA enrollment flows
* Headless TOTP verification
* Red-team and blue-team labs
* Offline QR decoding pipelines
* Mobile-free authenticator replacement

---

## License

MIT

---

## Author

**Josh Gompert**
[https://ginkorea.one](https://ginkorea.one)
