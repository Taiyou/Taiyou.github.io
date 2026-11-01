const TYPE_LABEL = {
  published_papers: "論文",
  misc: "MISC",
  books_etc: "書籍等",
  presentations: "講演",
  awards: "受賞",
  research_projects: "研究費",
};

const state = {
  researchers: [],
  publications: [],
  meta: null,
  config: null,
  filters: { q: "", type: "", yearFrom: null, yearTo: null },
  lang: "ja",
};

async function loadData() {
  const [researchers, publications, meta] = await Promise.all([
    fetch("./data/researchers.json").then((r) => r.json()),
    fetch("./data/publications.json").then((r) => r.json()),
    fetch("./data/meta.json").then((r) => r.json()),
  ]);
  return { researchers, publications, meta };
}

function pickLang(dict, lang) {
  if (!dict || typeof dict !== "object") return "";
  const other = lang === "ja" ? "en" : "ja";
  return dict[lang] || dict[other] || "";
}

function pickLangList(dict, lang) {
  if (!dict || typeof dict !== "object") return [];
  const other = lang === "ja" ? "en" : "ja";
  const v = dict[lang] || dict[other];
  return Array.isArray(v) ? v : [];
}

function applyFilters(publications, filters) {
  const q = (filters.q || "").trim().toLowerCase();
  const type = filters.type || "";
  const yf = Number.isFinite(filters.yearFrom) ? filters.yearFrom : null;
  const yt = Number.isFinite(filters.yearTo) ? filters.yearTo : null;

  return publications.filter((p) => {
    if (type && p.type !== type) return false;
    if (yf !== null && (p.year ?? -Infinity) < yf) return false;
    if (yt !== null && (p.year ?? Infinity) > yt) return false;
    if (q) {
      const title = [pickLang(p.title, "ja"), pickLang(p.title, "en")].join(" ");
      const venue = [pickLang(p.venue, "ja"), pickLang(p.venue, "en")].join(" ");
      const authors = [
        ...pickLangList(p.authors, "ja"),
        ...pickLangList(p.authors, "en"),
      ].join(" ");
      const hay = `${title} ${venue} ${authors}`.toLowerCase();
      if (!hay.includes(q)) return false;
    }
    return true;
  });
}

function sortByDateDesc(publications) {
  return [...publications].sort((a, b) => {
    const ay = a.year ?? -Infinity;
    const by = b.year ?? -Infinity;
    if (by !== ay) return by - ay;
    const ad = a.date || "";
    const bd = b.date || "";
    return bd.localeCompare(ad);
  });
}

function renderMeta(meta, root) {
  if (!meta) {
    root.textContent = "";
    return;
  }
  const d = meta.generated_at ? new Date(meta.generated_at) : null;
  const formatted = d && !Number.isNaN(d.getTime())
    ? d.toLocaleString("ja-JP", { hour12: false })
    : meta.generated_at;
  root.textContent = `最終更新: ${formatted}  /  研究者 ${meta.researchers_count} 名  /  業績 ${meta.publications_count} 件`;
}

function renderResearchers(researchers, root, lang) {
  root.innerHTML = "";
  for (const r of researchers) {
    const card = document.createElement("article");
    card.className = "researcher-card";

    const name = pickLang(r.name, lang) || r.permalink;
    const h = document.createElement("h3");
    const a = document.createElement("a");
    a.href = r.profile_url;
    a.target = "_blank";
    a.rel = "noopener noreferrer";
    a.textContent = name;
    h.appendChild(a);
    card.appendChild(h);

    const affil = pickLang(r.affiliation, lang);
    if (affil) {
      const p = document.createElement("p");
      p.className = "small muted";
      p.textContent = affil;
      card.appendChild(p);
    }
    const job = pickLang(r.job_title, lang);
    if (job) {
      const p = document.createElement("p");
      p.className = "small muted";
      p.textContent = job;
      card.appendChild(p);
    }
    root.appendChild(card);
  }
}

function renderPublications(publications, root, lang) {
  root.innerHTML = "";
  const frag = document.createDocumentFragment();
  for (const p of publications) {
    frag.appendChild(renderPubItem(p, lang));
  }
  root.appendChild(frag);
}

function renderPubItem(p, lang) {
  const li = document.createElement("li");
  li.className = "pub";

  const meta = document.createElement("div");
  meta.className = "pub-meta";

  const badge = document.createElement("span");
  badge.className = `badge badge-${p.type}`;
  badge.textContent = TYPE_LABEL[p.type] || p.type;
  meta.appendChild(badge);

  if (p.refereed === true) {
    const r = document.createElement("span");
    r.className = "badge badge-refereed";
    r.textContent = "査読";
    meta.appendChild(r);
  }
  if (p.invited === true) {
    const i = document.createElement("span");
    i.className = "badge badge-invited";
    i.textContent = "招待";
    meta.appendChild(i);
  }
  if (p.year || p.date) {
    const yr = document.createElement("span");
    yr.className = "year-pill";
    yr.textContent = p.date || String(p.year);
    meta.appendChild(yr);
  }
  li.appendChild(meta);

  const title = pickLang(p.title, lang) || "(無題)";
  const h = document.createElement("h3");
  h.className = "pub-title";
  if (p.url) {
    const a = document.createElement("a");
    a.href = p.url;
    a.target = "_blank";
    a.rel = "noopener noreferrer";
    a.textContent = title;
    h.appendChild(a);
  } else {
    h.textContent = title;
  }
  li.appendChild(h);

  const authors = pickLangList(p.authors, lang);
  if (authors.length) {
    const ap = document.createElement("p");
    ap.className = "pub-authors";
    ap.textContent = authors.join(", ");
    li.appendChild(ap);
  }

  const venue = pickLang(p.venue, lang);
  if (venue) {
    const vp = document.createElement("p");
    vp.className = "pub-venue";
    vp.textContent = venue;
    li.appendChild(vp);
  }

  const links = document.createElement("div");
  links.className = "pub-links";
  if (p.doi) {
    const a = document.createElement("a");
    a.href = `https://doi.org/${p.doi}`;
    a.target = "_blank";
    a.rel = "noopener noreferrer";
    a.textContent = `DOI: ${p.doi}`;
    links.appendChild(a);
  }
  if (p.id && /^https?:/.test(p.id)) {
    const a = document.createElement("a");
    a.href = p.id;
    a.target = "_blank";
    a.rel = "noopener noreferrer";
    a.textContent = "researchmap";
    links.appendChild(a);
  }
  if (links.childElementCount) li.appendChild(links);

  return li;
}

function debounce(fn, ms) {
  let t = null;
  return (...args) => {
    if (t) clearTimeout(t);
    t = setTimeout(() => fn(...args), ms);
  };
}

function readFilters() {
  const yf = parseInt(document.getElementById("year-from").value, 10);
  const yt = parseInt(document.getElementById("year-to").value, 10);
  return {
    q: document.getElementById("q").value,
    type: document.getElementById("type").value,
    yearFrom: Number.isFinite(yf) ? yf : null,
    yearTo: Number.isFinite(yt) ? yt : null,
  };
}

function update() {
  state.filters = readFilters();
  const filtered = sortByDateDesc(applyFilters(state.publications, state.filters));
  renderPublications(filtered, document.getElementById("list"), state.lang);

  const countEl = document.getElementById("result-count");
  countEl.textContent = `表示中: ${filtered.length} 件 / 全 ${state.publications.length} 件`;
  document.getElementById("empty").hidden = filtered.length !== 0;

  if (state.researchers.length) {
    renderResearchers(state.researchers, document.getElementById("researchers"), state.lang);
    document.getElementById("researchers-section").hidden = state.researchers.length < 2;
  }
}

function attachHandlers() {
  const debounced = debounce(update, 200);
  document.getElementById("q").addEventListener("input", debounced);
  document.getElementById("type").addEventListener("change", update);
  document.getElementById("year-from").addEventListener("input", debounced);
  document.getElementById("year-to").addEventListener("input", debounced);
  document.getElementById("lang").addEventListener("change", (e) => {
    state.lang = e.target.value === "en" ? "en" : "ja";
    document.documentElement.lang = state.lang;
    update();
  });
  document.getElementById("reset").addEventListener("click", () => {
    document.getElementById("q").value = "";
    document.getElementById("type").value = "";
    document.getElementById("year-from").value = "";
    document.getElementById("year-to").value = "";
    update();
  });
}

async function init() {
  try {
    const { researchers, publications, meta } = await loadData();
    state.researchers = Array.isArray(researchers) ? researchers : [];
    state.publications = Array.isArray(publications) ? publications : [];
    state.meta = meta || null;
  } catch (e) {
    document.getElementById("empty").hidden = false;
    document.getElementById("empty").textContent =
      "データを読み込めませんでした。GitHub Actions が初回実行されるまでお待ちください。";
    console.error(e);
    return;
  }

  renderMeta(state.meta, document.getElementById("meta"));
  document.getElementById("lang").value = state.lang;
  attachHandlers();
  update();
}

init();
