const kindEl = document.getElementById("kind");
const fieldsEl = document.getElementById("fields");
const statusEl = document.getElementById("status");
const outEl = document.getElementById("out");
const btnGen = document.getElementById("btnGen");
const passEl = document.getElementById("passphrase");
const importEl = document.getElementById("doImport");

function esc(s){
  return String(s).replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;");
}

function fieldRow(html){
  return `<div class="row" style="margin-top:10px;">${html}</div>`;
}

function renderFields(){
  const k = kindEl.value;
  if (k === "url"){
    fieldsEl.innerHTML = fieldRow(`
      <input id="url" style="flex:1" placeholder="https://example.com" />
    `);
  } else if (k === "text"){
    fieldsEl.innerHTML = `
      <textarea id="text" rows="4" style="width:100%; padding:10px;" placeholder="Any text payload..."></textarea>
    `;
  } else {
    fieldsEl.innerHTML = `
      ${fieldRow(`
        <input id="issuer" placeholder="issuer (e.g., ACME)" />
        <input id="account_name" placeholder="account (e.g., alice@example.com)" style="min-width:280px;" />
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
}

async function postJson(url, body){
  const r = await fetch(url, {method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify(body)});
  const d = await r.json().catch(() => ({}));
  return {ok: r.ok, status: r.status, data: d};
}

btnGen.addEventListener("click", async () => {
  outEl.innerHTML = "";
  statusEl.textContent = "Generating...";

  const k = kindEl.value;
  const params = {};

  if (k === "url"){
    params.url = (document.getElementById("url").value || "").trim();
  } else if (k === "text"){
    params.text = (document.getElementById("text").value || "").trim();
  } else {
    params.issuer = (document.getElementById("issuer").value || "").trim();
    params.account_name = (document.getElementById("account_name").value || "").trim();
    params.digits = Number(document.getElementById("digits").value || 6);
    params.period = Number(document.getElementById("period").value || 30);
    params.algorithm = (document.getElementById("algorithm").value || "SHA1").trim();
    params.nbytes = Number(document.getElementById("nbytes").value || 20);
  }

  const passphrase = (passEl.value || "").trim();
  const doImport = !!importEl.checked;

  const res = await postJson("/gen/payload", {
    kind: k,
    params,
    import: doImport,
    passphrase: passphrase || null,
  });

  if (!res.ok){
    statusEl.textContent = "Error: " + (res.data.error || ("HTTP " + res.status));
    return;
  }

  const gen = res.data.generated || {};
  statusEl.textContent = "Generated.";

  // Render QR image
  const qrRes = await fetch("/gen/qr", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({payload: gen.payload, box_size: 8, border: 2})
  });

  let imgHtml = "";
  if (qrRes.ok){
    const blob = await qrRes.blob();
    const objUrl = URL.createObjectURL(blob);
    imgHtml = `<div class="card"><div><b>QR preview</b></div><img src="${objUrl}" alt="qr" style="margin-top:10px; max-width:360px;"></div>`;
  }

  const metaJson = esc(JSON.stringify(gen.meta || {}, null, 2));
  const payloadEsc = esc(gen.payload || "");

  outEl.innerHTML = `
    ${imgHtml}
    <div class="card">
      <div><b>kind:</b> ${esc(gen.kind || "")}</div>
      <div style="margin-top:10px;"><b>payload</b></div>
      <pre>${payloadEsc}</pre>
      <div style="margin-top:10px;"><b>meta</b></div>
      <pre>${metaJson}</pre>
      ${res.data.imported ? `<div class="muted">Imported id: ${esc(res.data.imported.id)}</div>` : ""}
    </div>
  `;
});

kindEl.addEventListener("change", renderFields);
renderFields();
