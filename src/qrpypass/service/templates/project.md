# Project Compilation: templates

## 🧾 Summary

| Metric | Value |
|:--|:--|
| Root Directory | `/home/gompert/data/workspace/qr-pypass/src/qrpypass/service/templates` |
| Total Directories | 0 |
| Total Indexed Files | 5 |
| Skipped Files | 0 |
| Indexed Size | 10.28 KB |
| Max File Size Limit | 2 MB |

## 📚 Table of Contents

- [gen.html](#gen-html)
- [index.html](#index-html)
- [login.html](#login-html)
- [register.html](#register-html)
- [vault.html](#vault-html)

## 📂 Project Structure

```
📄 gen.html
📄 index.html
📄 login.html
📄 register.html
📄 vault.html
```

## `gen.html`

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>qr-pypass generator</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
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

## `index.html`

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>qr-pypass</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
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

## `login.html`

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>qr-pypass login</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
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

## `register.html`

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>qr-pypass register</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
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

## `vault.html`

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>qr-pypass vault</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
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

<details>
<summary>📁 Final Project Structure</summary>

```
📄 gen.html
📄 index.html
📄 login.html
📄 register.html
📄 vault.html
```

</details>
