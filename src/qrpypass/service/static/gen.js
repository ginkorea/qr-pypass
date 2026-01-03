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
