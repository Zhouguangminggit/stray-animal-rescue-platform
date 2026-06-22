document.addEventListener("DOMContentLoaded", () => {
  const elements = document.querySelectorAll(".reveal");
  const observer = new IntersectionObserver(
    (entries) => entries.forEach((entry) => entry.isIntersecting && entry.target.classList.add("is-visible")),
    { threshold: 0.15 },
  );
  elements.forEach((element) => observer.observe(element));
});
