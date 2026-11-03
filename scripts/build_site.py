"""site/ の原稿から docs/ に静的サイトを生成する(標準ライブラリのみ)。

    python3 scripts/build_site.py

docs/publications/ は researchmap の自動更新用なので触らない。
"""

from __future__ import annotations

import html
import json
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
        "cv_title": "CV",
        "cv_desc": "学歴・経験・受賞歴・研究費・スキル",
        "cv_open": "CVを開く",
        "cv_close": "閉じる",
        "cv_page": "CVのページで見る →",
    },
    "en": {
        "pages": PAGES_DIR / "en",
        "prefix": "en/",
        "labels": ["Research", "Persona Lab", "Projects", "Achievements", "Media", "DeSci", "Code", "CV", "Articles"],
        "switch": "日本語",
        "footer_db": "Publication database (updated daily from researchmap)",
        "menu": "Open menu",
        "toc": "On this page",
        "cv_title": "CV",
        "cv_desc": "Education, experience, honors, grants, and skills",
        "cv_open": "Open CV",
        "cv_close": "Close",
        "cv_page": "View the CV page →",
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


def render_markdown(text: str, root: str, prefix: str = "sec") -> tuple[str, list[tuple[str, str]]]:
    lines = text.strip("\n").split("\n")
    out: list[str] = []
    toc: list[tuple[str, str]] = []
    i = 0

    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            i += 1
        elif line.startswith("## "):
            anchor = f"{prefix}-{len(toc) + 1}"
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
            body, _ = render_markdown("\n".join(block), root, prefix) if any(s.strip() for s in block) else ("", [])
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


def render_nav(lang: str, active: str, root: str, switch_href: str | None = None) -> str:
    conf = LANGS[lang]
    links = "".join(
        f'<a href="{root}{conf["prefix"]}{slug}/"{" class=active" if slug == active else ""}>{label}</a>'
        for slug, label in zip(SLUGS, conf["labels"])
    )
    page = "" if active == "home" else f"{active}/"
    other = "ja" if lang == "en" else "en"
    href = switch_href or f"{root}{LANGS[other]['prefix']}{page}"
    switch = f'<a class="nav-lang" href="{html.escape(href)}" lang="{other}">{conf["switch"]}</a>'
    return links + switch


def wrap(
    template: str,
    meta: dict[str, str],
    body: str,
    root: str,
    lang: str,
    active: str,
    path: str | None = None,
    switch_href: str | None = None,
    langs: tuple[str, ...] | None = None,
) -> str:
    conf = LANGS[lang]
    if path is None:
        page = "" if active == "home" else f"{active}/"
        alternates = "\n  ".join(
            f'<link rel="alternate" hreflang="{code}" href="https://taiyou.github.io/{LANGS[code]["prefix"]}{page}">'
            for code in LANGS
        )
    else:
        # ブログ記事：自分自身を canonical にし、もう一方の言語版があれば hreflang で示す
        alternates = f'<link rel="canonical" href="https://taiyou.github.io/{conf["prefix"]}{path}">'
        for code in langs or ():
            alternates += f'\n  <link rel="alternate" hreflang="{code}" href="https://taiyou.github.io/{LANGS[code]["prefix"]}{path}">'

    return (
        template.replace("{{lang}}", lang)
        .replace("{{title}}", html.escape(meta["title"]))
        .replace("{{description}}", html.escape(meta["description"]))
        .replace("{{alternates}}", alternates)
        .replace("{{home}}", root + conf["prefix"])
        .replace("{{menu}}", conf["menu"])
        .replace("{{footer_db}}", conf["footer_db"])
        .replace("{{nav}}", render_nav(lang, active, root, switch_href))
        .replace("{{content}}", body)
        .replace("{{root}}", root)
    )


NOTE_MARKER = "<!--note-->"
NOTE_DATA = SITE_DIR / "data" / "note.json"


def load_note() -> list[dict[str, str]]:
    if not NOTE_DATA.exists():
        return []
    return json.loads(NOTE_DATA.read_text(encoding="utf-8")).get("items", [])


def render_note_list(items: list[dict[str, str]], limit: int | None = None) -> str:
    """note の記事を日付つきの一覧にする（scripts/fetch_note.py が毎日更新）。"""
    rows = "".join(
        f'<li><span class="note-date">{html.escape(x["date"].replace("-", "."))}</span>'
        f'<a href="{html.escape(x["url"])}" target="_blank" rel="noopener">{html.escape(x["title"])}</a></li>'
        for x in items[:limit]
    )
    return f'<ul class="note-list">{rows}</ul>'


BLOG_MARKER = "<!--blog-->"


def load_posts(lang: str) -> list[tuple[str, dict[str, str], str]]:
    """site/pages/<lang>/blog/*.md を新しい順に読む。ファイル名がそのまま URL になる。"""
    blog_dir = LANGS[lang]["pages"] / "blog"
    posts = [(p.stem, *read_page(p)) for p in blog_dir.glob("*.md")] if blog_dir.exists() else []
    return sorted(posts, key=lambda x: x[1].get("date", ""), reverse=True)


def render_blog_list(lang: str, root: str) -> str:
    rows = "".join(
        f'<li><span class="note-date">{html.escape(meta.get("date", "").replace("-", "."))}</span>'
        f'<a href="{root}{LANGS[lang]["prefix"]}blog/{slug}/">{html.escape(meta["heading"])}'
        + (f' <span class="post-status">{html.escape(meta["status"])}</span>' if meta.get("status") else "")
        + "</a></li>"
        for slug, meta, _ in load_posts(lang)
        if not meta.get("redirect")
    )
    return f'<ul class="note-list">{rows}</ul>'


def render_redirect(target: str, root: str) -> str:
    href, _ = link_attrs(target, root)
    canonical = "https://taiyou.github.io/" + target.lstrip("/")
    return (
        '<!DOCTYPE html><html><head><meta charset="UTF-8">'
        f'<meta http-equiv="refresh" content="0; url={href}">'
        f'<link rel="canonical" href="{canonical}"><title>Moved</title></head>'
        f'<body><p>This page has moved to <a href="{href}">{canonical}</a>.</p></body></html>'
    )


CV_MARKER = "<!--cv-->"


def render_cv_drawer(root: str, lang: str) -> str:
    """業績ページなどに、ボタンで開閉できる CV を埋め込む。"""
    conf = LANGS[lang]
    _, cv_text = read_page(conf["pages"] / "cv.md")
    cv_html, _ = render_markdown(cv_text, root, prefix="cv")
    return (
        '<details class="cv-drawer" id="cv">'
        '<summary>'
        f'<span class="cv-sum-text"><span class="cv-sum-title">{conf["cv_title"]}</span>'
        f'<span class="cv-sum-desc">{conf["cv_desc"]}</span></span>'
        f'<span class="cv-sum-btn"><span class="when-closed">{conf["cv_open"]}</span>'
        f'<span class="when-open">{conf["cv_close"]}</span></span>'
        '</summary>'
        '<div class="cv-drawer-body">'
        f'<p class="cv-drawer-link"><a href="{root}{conf["prefix"]}cv/">{conf["cv_page"]}</a></p>'
        f'<div class="timeline cv-embed">{cv_html}</div>'
        '</div></details>'
    )


def render_subpage(meta: dict[str, str], text: str, root: str, lang: str) -> str:
    content, toc = render_markdown(text, root)
    if NOTE_MARKER in content:
        content = content.replace(NOTE_MARKER, render_note_list(load_note()))
    if CV_MARKER in content:
        content = content.replace(CV_MARKER, render_cv_drawer(root, lang))
    if BLOG_MARKER in content:
        content = content.replace(BLOG_MARKER, render_blog_list(lang, root))
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
    posts = 0

    for lang, conf in LANGS.items():
        out_dir = OUT_DIR / conf["prefix"]
        out_dir.mkdir(parents=True, exist_ok=True)
        depth = conf["prefix"].count("/")

        # トップページ
        root = "../" * depth or "./"
        meta, body = read_page(conf["pages"] / "index.html")
        _, news_text = read_page(conf["pages"] / "_news.md")
        news, _ = render_markdown(news_text, root)
        body = body.replace("{{news}}", news).replace("{{note_latest}}", render_note_list(load_note(), 5))
        (out_dir / "index.html").write_text(wrap(template, meta, body, root, lang, "home"), encoding="utf-8")

        # 下層ページ
        root = "../" * (depth + 1)
        for slug in SLUGS:
            meta, text = read_page(conf["pages"] / f"{slug}.md")
            body = render_subpage(meta, text, root, lang)
            dest = out_dir / slug
            dest.mkdir(parents=True, exist_ok=True)
            (dest / "index.html").write_text(wrap(template, meta, body, root, lang, slug), encoding="utf-8")

        # ブログ記事（docs/<lang>/blog/<slug>/）。言語切替は原文（note など）があればそちらへ
        root = "../" * (depth + 2)
        for slug, meta, text in load_posts(lang):
            dest = out_dir / "blog" / slug
            dest.mkdir(parents=True, exist_ok=True)
            if meta.get("redirect"):
                # 統合した記事などは、古い URL から新しい記事へ転送する
                (dest / "index.html").write_text(render_redirect(meta["redirect"], root), encoding="utf-8")
                continue
            body = render_subpage(meta, text, root, lang)
            other = "ja" if lang == "en" else "en"
            if any(s == slug and not m.get("redirect") for s, m, _ in load_posts(other)):
                # もう一方の言語版があれば、言語切替はそちらへ
                switch, langs = f"{root}{LANGS[other]['prefix']}blog/{slug}/", (lang, other)
            else:
                switch, langs = meta.get("original"), None
            page = wrap(template, meta, body, root, lang, "articles", f"blog/{slug}/", switch, langs)
            (dest / "index.html").write_text(page, encoding="utf-8")
            posts += 1
    print(f"Built {(len(SLUGS) + 1) * len(LANGS) + posts} pages into {OUT_DIR}")


if __name__ == "__main__":
    build()
