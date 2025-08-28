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
      .sb-btn{position:fixed;right:16px;bottom:16px;z-index:2147483647;background:rgb(var(--sb-accent,51,97,255));color:#fff;border:none;border-radius:999px;padding:10px 14px;box-shadow:0 6px 24px rgba(0,0,0,.15);font:500 14px/1.2 ui-sans-serif,system-ui;cursor:pointer}
      .sb-iframe{position:fixed;right:16px;bottom:72px;z-index:2147483646;width:360px;max-width:95vw;height:520px;border:0;border-radius:16px;box-shadow:0 12px 40px rgba(0,0,0,.2);display:none}
      .sb-iframe.open{display:block}
    `;

    const btn = document.createElement("button");
    btn.className = "sb-btn";
    btn.textContent = initial.label || "Chat";

    const iframe = document.createElement("iframe");
    iframe.className = "sb-iframe";
    iframe.src = origin + `?api=${encodeURIComponent(initial.api || "")}`;

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
        if (typeof opts.label === "string") btn.textContent = opts.label;
        if (typeof opts.api === "string") iframe.src = origin + `?api=${encodeURIComponent(opts.api)}`;
      },
      open,
      close
    };
  });
})();

