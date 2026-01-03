// was: const passEl = document.getElementById("passphrase");
const passEl = document.getElementById("passphrase"); // may be null now

btnGen.addEventListener("click", async () => {
  outEl.innerHTML = "";
  statusEl.textContent = "Generating...";

  try {
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

    // null-safe
    const passphrase = passEl ? (passEl.value || "").trim() : "";
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
    } else {
      statusEl.textContent = `Generated, but QR render failed (HTTP ${qrRes.status}).`;
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
  } catch (err) {
    statusEl.textContent = "Error: " + err;
  }
});
