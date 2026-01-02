const form = document.getElementById("uploadForm");
const fileInput = document.getElementById("file");
const maxResults = document.getElementById("maxResults");
const statusEl = document.getElementById("status");
const resultsEl = document.getElementById("results");

function escapeHtml(s) {
  return String(s)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
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

      let extra = "";
      if (cls.kind === "url" && cls.normalized_url) {
        const u = escapeHtml(cls.normalized_url);
        extra = `<div><b>Open:</b> <a href="${u}" target="_blank" rel="noreferrer">${u}</a></div>`;
      } else if (cls.kind === "otpauth") {
        extra = `<div class="muted">Provisioning URI detected (secret not displayed).</div>`;
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
