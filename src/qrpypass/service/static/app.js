const form = document.getElementById("uploadForm");
const fileInput = document.getElementById("file");
const maxResults = document.getElementById("maxResults");
const statusEl = document.getElementById("status");
const resultsEl = document.getElementById("results");

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
    const qs = new URLSearchParams({ id: accId });

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
    refreshCodeOnce();

    const intervalId = setInterval(async () => {
      await refreshCodeOnce();
    }, 1000);

    activeIntervals.add(intervalId);
  }

  btn.addEventListener("click", async () => {
    msgEl.textContent = "Importing...";
    codeEl.textContent = "—";
    remEl.textContent = "";

    const res = await postJson("/auth/import", {
      otpauth_uri: rawUri,
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
    const data = await resp.json().catch(() => ({}));

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
