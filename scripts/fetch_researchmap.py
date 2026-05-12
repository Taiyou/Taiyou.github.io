"""researchmap API から研究者プロフィールと業績を取得し docs/data/*.json を生成する。"""

from __future__ import annotations

import json
import logging
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

import requests
import yaml

from normalize import normalize, normalize_profile

API_BASE = "https://api.researchmap.jp"
PAGE_LIMIT = 100
SLEEP_BETWEEN = 0.3
TIMEOUT = 30
MAX_RETRIES = 3

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = REPO_ROOT / "config.yml"
DATA_DIR = REPO_ROOT / "docs" / "data"

log = logging.getLogger("rmap")


def _user_agent() -> str:
    repo = os.environ.get("GITHUB_REPOSITORY", "local/dev")
    return f"rmap-site/0.1 (+https://github.com/{repo})"


def _session() -> requests.Session:
    s = requests.Session()
    s.headers.update(
        {
            "Accept": "application/ld+json",
            "User-Agent": _user_agent(),
        }
    )
    return s


SESSION = _session()


def load_config(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    if not isinstance(cfg, dict):
        raise ValueError(f"config must be a mapping, got {type(cfg).__name__}")
    if "researchers" not in cfg or not isinstance(cfg["researchers"], list):
        raise ValueError("config.researchers must be a list")
    if "achievement_types" not in cfg or not isinstance(cfg["achievement_types"], list):
        raise ValueError("config.achievement_types must be a list")
    return cfg


def fetch_with_retry(url: str, params: dict | None = None) -> dict:
    """5xx/429 は指数バックオフでリトライ。404 は例外を投げず空 dict を返す。"""
    backoff = 1.0
    last_exc: Exception | None = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            r = SESSION.get(url, params=params, timeout=TIMEOUT)
        except requests.RequestException as e:
            last_exc = e
            log.warning("Request failed (%s), retrying in %.0fs", e, backoff)
            time.sleep(backoff)
            backoff *= 2
            continue

        if r.status_code == 200:
            try:
                return r.json()
            except ValueError as e:
                raise RuntimeError(f"Invalid JSON from {url}: {e}") from e
        if r.status_code == 404:
            log.warning("404 Not Found: %s", url)
            return {}
        if r.status_code == 429 or 500 <= r.status_code < 600:
            log.warning(
                "HTTP %d from %s, retry %d/%d after %.0fs",
                r.status_code, url, attempt, MAX_RETRIES, backoff,
            )
            time.sleep(backoff)
            backoff *= 2
            continue
        # その他 4xx は致命
        raise RuntimeError(f"HTTP {r.status_code} from {url}: {r.text[:200]}")

    raise RuntimeError(f"Exhausted retries for {url}: {last_exc}")


def fetch_profile(permalink: str) -> dict:
    url = f"{API_BASE}/{permalink}"
    data = fetch_with_retry(url)
    time.sleep(SLEEP_BETWEEN)
    if not data:
        return {}
    return normalize_profile(data, permalink)


def fetch_achievement_pages(permalink: str, ach_type: str) -> Iterator[dict]:
    """ページネーションを辿って item を yield する。"""
    start = 1
    url = f"{API_BASE}/{permalink}/{ach_type}"
    while True:
        params = {
            "limit": PAGE_LIMIT,
            "start": start,
            "format": "json",
            "sort": "-date",
        }
        data = fetch_with_retry(url, params=params)
        time.sleep(SLEEP_BETWEEN)
        if not data:
            return
        items = data.get("items")
        if not isinstance(items, list) or not items:
            return
        for it in items:
            if isinstance(it, dict):
                yield it
        if len(items) < PAGE_LIMIT:
            return
        start += PAGE_LIMIT


def dedupe(pubs: list[dict]) -> list[dict]:
    """id をキーに重複統合。researcher_permalinks をマージ、他フィールドは先勝ち。"""
    seen: dict[str, dict] = {}
    no_id: list[dict] = []
    for p in pubs:
        pid = p.get("id")
        if not pid:
            no_id.append(p)
            continue
        if pid in seen:
            existing = seen[pid]
            for plink in p.get("researcher_permalinks", []):
                if plink not in existing["researcher_permalinks"]:
                    existing["researcher_permalinks"].append(plink)
        else:
            seen[pid] = dict(p)
    return list(seen.values()) + no_id


def _sort_key(p: dict) -> tuple:
    # date が無いものは末尾。新しい順なので降順 -> キー反転で昇順比較
    date = p.get("date") or ""
    year = p.get("year") or 0
    # date 文字列は YYYY-MM-DD / YYYY-MM / YYYY を想定。文字列比較で十分。
    return (-year, date)


def sort_publications(pubs: list[dict]) -> list[dict]:
    return sorted(pubs, key=lambda p: (p.get("year") or 0, p.get("date") or ""), reverse=True)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    if not CONFIG_PATH.exists():
        log.error("config.yml not found at %s", CONFIG_PATH)
        sys.exit(1)

    cfg = load_config(CONFIG_PATH)
    ach_types: list[str] = cfg["achievement_types"]

    researchers_out: list[dict] = []
    publications_all: list[dict] = []

    for r in cfg["researchers"]:
        if not isinstance(r, dict) or "permalink" not in r:
            log.warning("Skipping invalid researcher entry: %r", r)
            continue
        permalink = r["permalink"]
        log.info("Fetching profile: %s", permalink)
        profile = fetch_profile(permalink)
        if not profile:
            log.warning("  profile not found, skipping researcher")
            continue

        # 設定で display_name が指定されていれば name.ja を上書き
        display_name = r.get("display_name")
        if display_name:
            profile.setdefault("name", {})
            profile["name"].setdefault("ja", display_name)

        researchers_out.append(profile)

        for ach_type in ach_types:
            count = 0
            for item in fetch_achievement_pages(permalink, ach_type):
                publications_all.append(normalize(item, ach_type, permalink))
                count += 1
            log.info("  %s: %d items", ach_type, count)

    publications = sort_publications(dedupe(publications_all))

    log.info(
        "Total: %d researchers, %d publications",
        len(researchers_out),
        len(publications),
    )

    if not researchers_out:
        log.error(
            "No researchers fetched. Refusing to overwrite existing data/*.json."
        )
        sys.exit(2)

    write_json(DATA_DIR / "researchers.json", researchers_out)
    write_json(DATA_DIR / "publications.json", publications)
    write_json(
        DATA_DIR / "meta.json",
        {
            "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "researchers_count": len(researchers_out),
            "publications_count": len(publications),
            "source": "researchmap",
        },
    )

    log.info("Wrote docs/data/{researchers,publications,meta}.json")


if __name__ == "__main__":
    main()
