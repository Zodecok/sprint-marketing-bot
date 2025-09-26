// Usage: Define `window.SprintBot = { config: { origin, api, label } }` before including
// this script, then load it via <script src="./widget.js" defer></script>. The script mounts
// a floating launcher button that opens the Sprint chat UI inside an iframe sourced from
// `origin`, optionally appending `?api=...` when `config.api` is provided.
(function () {
  function onReady(fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn, { once: true });
    } else {
      fn();
    }
  }

  onReady(function initWidget() {
    const initial = window.SprintBot && window.SprintBot.config || {};
    const base = initial.origin || location.origin;
    const origin = base.endsWith("/") ? base : base + "/";

    const host = document.createElement("div");
    const shadow = host.attachShadow({ mode: "open" });

    const style = document.createElement("style");
    style.textContent = `
      .sb-btn{position:fixed;right:24px;bottom:24px;z-index:2147483647;display:flex;align-items:center;justify-content:center;width:56px;height:56px;border-radius:999px;border:none;background:#0f172a;color:#fff;cursor:pointer;box-shadow:0 24px 48px -18px rgba(15,23,42,.6);transition:transform .2s ease,box-shadow .2s ease}
      .sb-btn:hover{transform:scale(1.05);box-shadow:0 30px 64px -28px rgba(15,23,42,.6)}
      .sb-btn:focus-visible{outline:3px solid rgba(248,250,252,.95);outline-offset:3px}
      .sb-btn-icon{display:flex;width:24px;height:24px;align-items:center;justify-content:center}
      .sb-btn-text{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);border:0}
      .sb-iframe{position:fixed;right:24px;bottom:96px;z-index:2147483646;width:380px;max-width:92vw;height:560px;border:0;border-radius:28px;box-shadow:0 40px 90px -35px rgba(15,23,42,.6);border:1px solid rgba(148,163,184,.35);display:none;background:transparent}
      .sb-iframe.open{display:block}
    `;

    const btn = document.createElement("button");
    btn.className = "sb-btn";

    const labelText = initial.label || "Chat";
    btn.innerHTML = `
      <span class="sb-btn-icon" aria-hidden="true">
        <svg viewBox="0 0 24 24" fill="none" stroke="none" width="24" height="24">
          <path fill="currentColor" d="M5.5 4h13a2.5 2.5 0 0 1 2.5 2.5v8a2.5 2.5 0 0 1-2.5 2.5H12l-3.6 3.2A1 1 0 0 1 7 19.4V17H5.5A2.5 2.5 0 0 1 3 14.5v-8A2.5 2.5 0 0 1 5.5 4Z" />
        </svg>
      </span>
      <span class="sb-btn-text"></span>
    `;

    const btnText = btn.querySelector(".sb-btn-text");
    const setBtnLabel = (value) => {
      const next = typeof value === "string" && value.length ? value : "Chat";
      btn.setAttribute("aria-label", next);
      if (btnText) btnText.textContent = next;
    };

    setBtnLabel(labelText);

    const iframe = document.createElement("iframe");
    iframe.className = "sb-iframe";

    function buildSrc(srcOrigin, api) {
      if (typeof api === "string" && api.length > 0) {
        return srcOrigin + `?api=${encodeURIComponent(api)}`;
      }
      return srcOrigin;
    }

    iframe.src = buildSrc(origin, initial.api);

    const open = () => iframe.classList.add("open");
    const close = () => iframe.classList.remove("open");

    btn.addEventListener("click", () => {
      if (iframe.classList.contains("open")) close(); else open();
    });

    shadow.appendChild(style);
    shadow.appendChild(btn);
    shadow.appendChild(iframe);
    document.body.appendChild(host);

    window.SprintBot = {
      init: (opts) => {
        if (!opts) return;
        if (typeof opts.label === "string") setBtnLabel(opts.label);
        if (typeof opts.api === "string") iframe.src = buildSrc(origin, opts.api);
      },
      open,
      close
    };
  });
})();
