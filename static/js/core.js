document.documentElement.classList.add("js-ready");

/* ============================================================
   消息提示自动关闭
   ============================================================ */
function dismissMessage(message) {
  if (!message || message.classList.contains("message--leaving")) return;
  message.classList.add("message--leaving");
  window.setTimeout(() => {
    const container = message.parentElement;
    message.remove();
    if (container && !container.querySelector("[data-message]")) container.remove();
  }, 220);
}

document.querySelectorAll("[data-message]").forEach((message) => {
  const closeButton = message.querySelector("[data-message-close]");
  closeButton?.addEventListener("click", () => dismissMessage(message));

  const timeout = Number.parseInt(message.dataset.autoDismiss || "", 10);
  if (Number.isFinite(timeout) && timeout > 0) {
    window.setTimeout(() => dismissMessage(message), timeout);
  }
});

/* ============================================================
   导航栏滚动效果（毛玻璃增强 + 阴影）
   ============================================================ */
(function initHeaderScroll() {
  const header = document.getElementById("site-header");
  if (!header) return;

  const scrollThreshold = 16;
  let ticking = false;

  function updateHeader() {
    const scrolled = window.scrollY > scrollThreshold;
    header.classList.toggle("site-header--scrolled", scrolled);
    ticking = false;
  }

  window.addEventListener("scroll", () => {
    if (!ticking) {
      window.requestAnimationFrame(updateHeader);
      ticking = true;
    }
  }, { passive: true });

  // 初始化一次
  updateHeader();
})();

/* ============================================================
   用户下拉菜单
   ============================================================ */
(function initUserDropdown() {
  const dropdown = document.getElementById("user-dropdown");
  if (!dropdown) return;

  const toggle = dropdown.querySelector(".user-dropdown__toggle");
  const menu = dropdown.querySelector(".user-dropdown__menu");
  if (!toggle || !menu) return;

  function openMenu() {
    toggle.setAttribute("aria-expanded", "true");
    menu.classList.add("is-open");
  }

  function closeMenu() {
    toggle.setAttribute("aria-expanded", "false");
    menu.classList.remove("is-open");
  }

  function isOpen() {
    return menu.classList.contains("is-open");
  }

  // 点击触发器：切换菜单
  toggle.addEventListener("click", (e) => {
    e.preventDefault();
    e.stopPropagation();
    isOpen() ? closeMenu() : openMenu();
  });

  // 点击外部：关闭菜单（但点击 dropdown 内部不关闭）
  document.addEventListener("click", (e) => {
    if (isOpen() && !dropdown.contains(e.target)) {
      closeMenu();
    }
  });

  // ESC 键关闭
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && isOpen()) closeMenu();
  });

  // 点击菜单项后关闭（延迟，让链接跳转/表单提交先执行）
  menu.querySelectorAll("a, button").forEach((item) => {
    item.addEventListener("click", () => {
      window.setTimeout(closeMenu, 50);
    });
  });
})();

/* ============================================================
   平滑滚动（锚点链接）
   ============================================================ */
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", (e) => {
    const targetId = anchor.getAttribute("href");
    if (targetId === "#") return;
    const target = document.querySelector(targetId);
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  });
});
