"""site/ の原稿から docs/ に静的サイトを生成する(標準ライブラリのみ)。

    python3 scripts/build_site.py

docs/publications/ は researchmap の自動更新用なので触らない。
"""

from __future__ import annotations

import html
import re
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SITE_DIR = REPO_ROOT / "site"
PAGES_DIR = SITE_DIR / "pages"
OUT_DIR = REPO_ROOT / "docs"

SLUGS = ["research", "persona", "projects", "achievements", "media", "desci", "code", "cv", "articles"]

LANGS = {
    "ja": {
        "pages": PAGES_DIR,
        "prefix": "",
        "labels": ["研究", "Persona Lab", "企画・運営", "業績", "メディア", "DeSci", "コード", "CV", "記事"],
        "switch": "EN",
        "footer_db": "業績データベース（researchmap から自動更新）",
        "menu": "メニューを開く",
        "toc": "ページ内目次",
    },
    "en": {
        "pages": PAGES_DIR / "en",
        "prefix": "en/",
        "labels": ["Research", "Persona Lab", "Projects", "Achievements", "Media", "DeSci", "Code", "CV", "Articles"],
        "switch": "日本語",
        "footer_db": "Publication database (updated daily from researchmap)",
        "menu": "Open menu",
        "toc": "On this page",
    },
}

IMG_LINK = r"\[!\[([^\]]*)\]\(([^)\s]+)\)\]\(([^)\s]+)\)"
IMG = r"!\[([^\]]*)\]\(([^)\s]+)\)"
ONLY_IMAGES = re.compile(rf"^(?:\s*(?:{IMG_LINK}|{IMG}))+\s*$")


def link_attrs(url: str, root: str) -> tuple[str, str]:
    """内部リンクを相対パスへ直し、外部リンクには新規タブの属性を付ける。"""
    if url.startswith("/"):
        return root + url[1:], ""
    if url.startswith("http"):
        return url, ' target="_blank" rel="noopener"'
    return url, ""


def image_src(src: str, root: str) -> str:
    return src if src.startswith("http") else f"{root}assets/img/{src}"


def inline(text: str, root: str) -> str:
    out = html.escape(text, quote=False)

    def anchor(label: str, url: str, cls: str = "") -> str:
        href, attrs = link_attrs(url, root)
        c = f' class="{cls}"' if cls else ""
        return f'<a{c} href="{href}"{attrs}>{label}</a>'

    def picture(alt: str, src: str) -> str:
        return f'<img src="{image_src(src, root)}" alt="{html.escape(alt)}" loading="lazy">'

    out = re.sub(IMG_LINK, lambda m: anchor(picture(m[1], m[2]), m[3]), out)
    out = re.sub(IMG, lambda m: picture(m[1], m[2]), out)
    # [[Preprint](url)] と [[Preprint]](url) はどちらも小さなタグにする
    out = re.sub(r"\[\[([^\[\]]+)\]\(([^)\s]+)\)\]", lambda m: anchor(m[1], m[2], "tag"), out)
    out = re.sub(r"\[\[([^\[\]]+)\]\]\(([^)\s]+)\)", lambda m: anchor(m[1], m[2], "tag"), out)
    out = re.sub(r"\[([^\[\]]+)\]\(([^)\s]+)\)", lambda m: anchor(m[1], m[2]), out)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)


def render_list(lines: list[str], root: str) -> str:
    """インデント 2 文字ごとに入れ子にしたリストを描画する。"""
    parts: list[str] = []
    stack: list[tuple[int, str]] = []
    for line in lines:
        m = re.match(r"^(\s*)(-|\d+\.)\s+(.*)$", line)
        depth = len(m[1]) // 2
        tag = "ol" if m[2] != "-" else "ul"
        while stack and stack[-1][0] > depth:
            parts.append(f"</li></{stack.pop()[1]}>")
        if stack and stack[-1][0] == depth:
            parts.append("</li>")
        else:
            start = f' reversed start="{m[2][:-1]}"' if tag == "ol" else ""
            parts.append(f"<{tag}{start}>")
            stack.append((depth, tag))
        parts.append(f"<li>{inline(m[3], root)}")
    while stack:
        parts.append(f"</li></{stack.pop()[1]}>")
    return "".join(parts)


def render_markdown(text: str, root: str) -> tuple[str, list[tuple[str, str]]]:
    lines = text.strip("\n").split("\n")
    out: list[str] = []
    toc: list[tuple[str, str]] = []
    i = 0

    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            i += 1
        elif line.startswith("## "):
            anchor = f"sec-{len(toc) + 1}"
            toc.append((anchor, line[3:].strip()))
            out.append(f'<h2 id="{anchor}">{inline(line[3:].strip(), root)}</h2>')
            i += 1
        elif line.startswith("### "):
            # entry は次の見出しまで続く
            i += 1
            block: list[str] = []
            while i < len(lines) and not re.match(r"^#{2,3} ", lines[i]):
                block.append(lines[i])
                i += 1
            body, _ = render_markdown("\n".join(block), root) if any(s.strip() for s in block) else ("", [])
            out.append(
                f'<div class="entry"><h3>{inline(line[4:].strip(), root)}</h3>'
                f'<div class="entry-body">{body}</div></div>'
            )
        elif line.startswith("@youtube "):
            cards = []
            while i < len(lines) and lines[i].startswith("@youtube "):
                _, vid, title = lines[i].split(" ", 2)
                cards.append(
                    f'<a class="video" href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noopener">'
                    f'<span class="video-thumb"><img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="" loading="lazy"></span>'
                    f'<span class="video-title">{inline(title, root)}</span></a>'
                )
                i += 1
            out.append(f'<div class="video-grid">{"".join(cards)}</div>')
        elif re.match(r"^\s*(-|\d+\.)\s+", line):
            block = []
            while i < len(lines) and re.match(r"^\s*(-|\d+\.)\s+", lines[i]):
                block.append(lines[i].rstrip())
                i += 1
            out.append(render_list(block, root))
        elif ONLY_IMAGES.match(line):
            count = len(re.findall(r"!\[", line))
            out.append(f'<figure class="figs figs-{min(count, 3)}">{inline(line.strip(), root)}</figure>')
            i += 1
        elif line.startswith("<"):
            out.append(line)
            i += 1
        else:
            out.append(f"<p>{inline(line.strip(), root)}</p>")
            i += 1
    return "\n".join(out), toc


def read_page(path: Path) -> tuple[dict[str, str], str]:
    raw = path.read_text(encoding="utf-8")
    meta: dict[str, str] = {}
    if raw.startswith("---\n"):
        head, raw = raw[4:].split("\n---\n", 1)
        for line in head.splitlines():
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()
    return meta, raw


def render_nav(lang: str, active: str, root: str) -> str:
    conf = LANGS[lang]
    links = "".join(
        f'<a href="{root}{conf["prefix"]}{slug}/"{" class=active" if slug == active else ""}>{label}</a>'
        for slug, label in zip(SLUGS, conf["labels"])
    )
    page = "" if active == "home" else f"{active}/"
    other = "ja" if lang == "en" else "en"
    switch = f'<a class="nav-lang" href="{root}{LANGS[other]["prefix"]}{page}" lang="{other}">{conf["switch"]}</a>'
    return links + switch


def wrap(template: str, meta: dict[str, str], body: str, root: str, lang: str, active: str) -> str:
    conf = LANGS[lang]
    page = "" if active == "home" else f"{active}/"
    alternates = "\n  ".join(
        f'<link rel="alternate" hreflang="{code}" href="https://taiyou.github.io/{LANGS[code]["prefix"]}{page}">'
        for code in LANGS
    )
    return (
        template.replace("{{lang}}", lang)
        .replace("{{title}}", html.escape(meta["title"]))
        .replace("{{description}}", html.escape(meta["description"]))
        .replace("{{alternates}}", alternates)
        .replace("{{home}}", root + conf["prefix"])
        .replace("{{menu}}", conf["menu"])
        .replace("{{footer_db}}", conf["footer_db"])
        .replace("{{nav}}", render_nav(lang, active, root))
        .replace("{{content}}", body)
        .replace("{{root}}", root)
    )


def render_subpage(meta: dict[str, str], text: str, root: str, lang: str) -> str:
    content, toc = render_markdown(text, root)
    lead = f'<p class="page-lead">{inline(meta["lead"], root)}</p>' if meta.get("lead") else ""
    side = ""
    if meta.get("toc") == "true" and toc:
        items = "".join(f'<a href="#{a}">{inline(t, root)}</a>' for a, t in toc)
        side = f'<nav class="toc" aria-label="{LANGS[lang]["toc"]}">{items}</nav>'
    layout = "page-grid" if side else "page-single"
    variant = meta.get("variant", "")
    return (
        '<header class="page-head"><div class="page-head-inner">'
        f'<p class="section-label">{meta.get("label", "")}</p>'
        f'<h1>{html.escape(meta["heading"])}</h1>{lead}</div></header>'
        f'<main class="{layout}">{side}<article class="prose {variant}">{content}</article></main>'
    )


def build() -> None:
    template = (SITE_DIR / "template.html").read_text(encoding="utf-8")

    (OUT_DIR / "assets").mkdir(parents=True, exist_ok=True)
    for name in ("site.css", "site.js"):
        shutil.copy(SITE_DIR / "assets" / name, OUT_DIR / "assets" / name)
    (OUT_DIR / ".nojekyll").touch()

    for lang, conf in LANGS.items():
        out_dir = OUT_DIR / conf["prefix"]
        out_dir.mkdir(parents=True, exist_ok=True)
        depth = conf["prefix"].count("/")

        # トップページ
        root = "../" * depth or "./"
        meta, body = read_page(conf["pages"] / "index.html")
        _, news_text = read_page(conf["pages"] / "_news.md")
        news, _ = render_markdown(news_text, root)
        body = body.replace("{{news}}", news)
        (out_dir / "index.html").write_text(wrap(template, meta, body, root, lang, "home"), encoding="utf-8")

        # 下層ページ
        root = "../" * (depth + 1)
        for slug in SLUGS:
            meta, text = read_page(conf["pages"] / f"{slug}.md")
            body = render_subpage(meta, text, root, lang)
            dest = out_dir / slug
            dest.mkdir(parents=True, exist_ok=True)
            (dest / "index.html").write_text(wrap(template, meta, body, root, lang, slug), encoding="utf-8")
    print(f"Built {(len(SLUGS) + 1) * len(LANGS)} pages into {OUT_DIR}")


if __name__ == "__main__":
    build()
