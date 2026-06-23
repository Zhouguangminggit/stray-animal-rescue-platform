document.addEventListener("DOMContentLoaded", () => {
  // 滚动揭示动画
  const elements = document.querySelectorAll(".reveal, .reveal-left, .reveal-right");
  const observer = new IntersectionObserver(
    (entries) => entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
      }
    }),
    { threshold: 0.12, rootMargin: "0px 0px -30px 0px" }
  );
  elements.forEach((element) => observer.observe(element));
});
