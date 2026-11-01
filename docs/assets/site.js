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

// ヒーロー背景のマルチエージェント: 近くの仲間と群れを作り、メッセージを送り合って色(意見)を伝え合う
(() => {
  const canvas = document.querySelector(".agents");
  if (!canvas) return;
  const hero = canvas.parentElement;
  const ctx = canvas.getContext("2d");
  const COLORS = ["201, 169, 97", "95, 179, 189", "232, 228, 218"];
  const RANGE = 170;
  const SPACE = 36;
  const MAX_SPEED = 1;

  let width = 0;
  let height = 0;
  let agents = [];
  let messages = [];
  let sinceMessage = 0;
  let pointer = null;

  const spawn = () => ({
    x: Math.random() * width,
    y: Math.random() * height,
    vx: (Math.random() - 0.5) * MAX_SPEED,
    vy: (Math.random() - 0.5) * MAX_SPEED,
    team: Math.floor(Math.random() * COLORS.length),
    glow: 0,
  });

  const resize = () => {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    width = hero.clientWidth;
    height = hero.clientHeight;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const count = Math.max(30, Math.min(84, Math.round((width * height) / 15000)));
    while (agents.length < count) agents.push(spawn());
    agents.length = count;
    agents.forEach((a) => {
      a.x = Math.min(a.x, width);
      a.y = Math.min(a.y, height);
    });
    messages = [];
  };

  const step = (dt) => {
    const near = [];
    agents.forEach((a, i) => {
      let ax = (Math.random() - 0.5) * 0.02;
      let ay = (Math.random() - 0.5) * 0.02;
      agents.forEach((b, j) => {
        if (i === j) return;
        const dx = b.x - a.x;
        const dy = b.y - a.y;
        const d = Math.hypot(dx, dy) || 1;
        if (d > RANGE) return;
        if (i < j) near.push([i, j, d]);
        if (d < SPACE) {
          ax -= (dx / d) * 0.02;
          ay -= (dy / d) * 0.02;
        } else if (a.team === b.team) {
          // 同じ色どうしは寄り添い、向きをそろえる
          ax += (dx / d) * 0.0032 + (b.vx - a.vx) * 0.006;
          ay += (dy / d) * 0.0032 + (b.vy - a.vy) * 0.006;
        }
      });
      if (pointer) {
        const dx = pointer.x - a.x;
        const dy = pointer.y - a.y;
        const d = Math.hypot(dx, dy) || 1;
        if (d < 180) {
          ax += (dx / d) * 0.012;
          ay += (dy / d) * 0.012;
        }
      }
      // 画面の端では内側へ向きを変える
      const edge = 40;
      if (a.x < edge) ax += 0.02;
      if (a.x > width - edge) ax -= 0.02;
      if (a.y < edge) ay += 0.02;
      if (a.y > height - edge) ay -= 0.02;
      a.vx += ax * dt;
      a.vy += ay * dt;
      const speed = Math.hypot(a.vx, a.vy) || 1;
      const limit = speed > MAX_SPEED ? MAX_SPEED / speed : speed < 0.2 ? 0.2 / speed : 1;
      a.vx *= limit;
      a.vy *= limit;
      a.x += a.vx * dt;
      a.y += a.vy * dt;
      a.glow = Math.max(0, a.glow - 0.02 * dt);
    });

    // メッセージの送信と受信
    sinceMessage += dt;
    if (sinceMessage > 7 && near.length) {
      sinceMessage = 0;
      const [i, j] = near[Math.floor(Math.random() * near.length)];
      messages.push({ from: i, to: j, t: 0, team: agents[i].team });
    }
    messages = messages.filter((m) => {
      m.t += 0.018 * dt;
      if (m.t < 1) return true;
      const to = agents[m.to];
      to.glow = 1;
      if (Math.random() < 0.3) to.team = m.team;
      else if (Math.random() < 0.08) to.team = Math.floor(Math.random() * COLORS.length);
      return false;
    });
    return near;
  };

  const draw = (near) => {
    ctx.clearRect(0, 0, width, height);
    near.forEach(([i, j, d]) => {
      const a = agents[i];
      const b = agents[j];
      const alpha = (1 - d / RANGE) * 0.5;
      ctx.strokeStyle = `rgba(${a.team === b.team ? COLORS[a.team] : COLORS[2]}, ${a.team === b.team ? alpha : alpha * 0.45})`;
      ctx.lineWidth = 0.8;
      ctx.beginPath();
      ctx.moveTo(a.x, a.y);
      ctx.lineTo(b.x, b.y);
      ctx.stroke();
    });
    messages.forEach((m) => {
      const a = agents[m.from];
      const b = agents[m.to];
      ctx.fillStyle = `rgba(${COLORS[m.team]}, .95)`;
      ctx.beginPath();
      ctx.arc(a.x + (b.x - a.x) * m.t, a.y + (b.y - a.y) * m.t, 2.6, 0, Math.PI * 2);
      ctx.fill();
    });
    agents.forEach((a) => {
      if (a.glow > 0) {
        ctx.fillStyle = `rgba(${COLORS[a.team]}, ${a.glow * 0.22})`;
        ctx.beginPath();
        ctx.arc(a.x, a.y, 3 + (1 - a.glow) * 14, 0, Math.PI * 2);
        ctx.fill();
      }
      ctx.fillStyle = `rgba(${COLORS[a.team]}, .85)`;
      ctx.beginPath();
      ctx.arc(a.x, a.y, 2.8, 0, Math.PI * 2);
      ctx.fill();
    });
  };

  resize();
  window.addEventListener("resize", resize);

  // 動きを減らす設定では、静止した1枚だけを描く
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    draw(step(1));
    return;
  }

  hero.addEventListener("pointermove", (e) => {
    const r = hero.getBoundingClientRect();
    pointer = { x: e.clientX - r.left, y: e.clientY - r.top };
  });
  hero.addEventListener("pointerleave", () => {
    pointer = null;
  });

  let visible = true;
  let frame = 0;
  let last = 0;
  const loop = (now) => {
    const dt = Math.min((now - last) / 16.7 || 1, 3);
    last = now;
    draw(step(dt));
    frame = visible ? requestAnimationFrame(loop) : 0;
  };
  // ヒーローが画面外にあるときは計算を止める
  new IntersectionObserver(([entry]) => {
    visible = entry.isIntersecting;
    if (visible && !frame) {
      last = performance.now();
      frame = requestAnimationFrame(loop);
    }
  }).observe(hero);
})();
