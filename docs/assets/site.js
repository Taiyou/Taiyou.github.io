// ナビの影と、スクロールに合わせたセクションのフェードイン
(() => {
  const nav = document.getElementById("site-nav");
  const onScroll = () => nav.classList.toggle("scrolled", window.scrollY > 16);
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  document.querySelectorAll(".nav-links a").forEach((a) => {
    a.addEventListener("click", () => {
      document.getElementById("nav-check").checked = false;
    });
  });

  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const targets = document.querySelectorAll(".reveal");
  if (reduce || !("IntersectionObserver" in window)) return;
  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) {
          e.target.classList.remove("is-hidden");
          io.unobserve(e.target);
        }
      });
    },
    { rootMargin: "0px 0px -8% 0px" }
  );
  targets.forEach((el) => {
    // すでに画面内にあるものは隠さない
    if (el.getBoundingClientRect().top > window.innerHeight) {
      el.classList.add("is-hidden");
      io.observe(el);
    }
  });
})();
