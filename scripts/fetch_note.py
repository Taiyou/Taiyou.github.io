"""note の RSS から記事一覧を取得し、site/data/note.json に保存する。

取得に失敗したときは既存のファイルを残す（サイトのビルドは古い一覧のまま続けられる）。
"""
from __future__ import annotations

import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from pathlib import Path

FEED_URL = "https://note.com/hirotaiyohamada/rss"
OUT = Path(__file__).resolve().parent.parent / "site" / "data" / "note.json"
MAX_ITEMS = 60


def parse(xml_text: str) -> list[dict[str, str]]:
    root = ET.fromstring(xml_text)
    items = []
    for item in root.iter("item"):
        title = (item.findtext("title") or "").strip()
        url = (item.findtext("link") or "").strip().split("?")[0]
        pub = item.findtext("pubDate") or ""
        try:
            date = parsedate_to_datetime(pub).date().isoformat()
        except (TypeError, ValueError):
            date = ""
        if title and url:
            items.append({"date": date, "title": title, "url": url})
    items.sort(key=lambda x: x["date"], reverse=True)
    return items


def merge(new: list[dict[str, str]], old: list[dict[str, str]]) -> list[dict[str, str]]:
    """RSS は最新の数十件しか返さないので、過去に取得した記事も残す。"""
    seen = {x["url"] for x in new}
    merged = new + [x for x in old if x["url"] not in seen]
    merged.sort(key=lambda x: x["date"], reverse=True)
    return merged[:MAX_ITEMS]


def main() -> int:
    old = []
    if OUT.exists():
        old = json.loads(OUT.read_text(encoding="utf-8")).get("items", [])
    try:
        req = urllib.request.Request(FEED_URL, headers={"User-Agent": "taiyou.github.io site builder"})
        with urllib.request.urlopen(req, timeout=30) as res:
            new = parse(res.read().decode("utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"note の取得に失敗しました（既存の一覧を使います）: {e}", file=sys.stderr)
        return 0
    if not new:
        print("note の記事が見つかりませんでした（既存の一覧を使います）", file=sys.stderr)
        return 0
    items = merge(new, old)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"source": FEED_URL, "items": items}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"note: {len(items)} 件")
    return 0


if __name__ == "__main__":
    sys.exit(main())
