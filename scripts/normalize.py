"""researchmap API レスポンスを内部スキーマへ正規化する。"""

from __future__ import annotations

import re
from typing import Any, Callable


# 種別ごとのフィールドマッピング
# (内部キー, [候補となる API フィールド名 ...])
_FIELD_MAP: dict[str, dict[str, list[str]]] = {
    "published_papers": {
        "title": ["paper_title"],
        "venue": ["publication_name"],
        "date": ["publication_date"],
        "authors": ["authors"],
    },
    "misc": {
        "title": ["paper_title"],
        "venue": ["publication_name"],
        "date": ["publication_date"],
        "authors": ["authors"],
    },
    "books_etc": {
        "title": ["book_title"],
        "venue": ["publisher"],
        "date": ["publication_date"],
        "authors": ["authors"],
    },
    "presentations": {
        "title": ["presentation_title"],
        "venue": ["event"],
        "date": ["event_date", "from_date", "presentation_date"],
        "authors": ["authors"],
    },
    "awards": {
        "title": ["award_title"],
        "venue": ["awarding_organization"],
        "date": ["award_date"],
        "authors": ["winners", "authors"],
    },
    "research_projects": {
        "title": ["research_project_title"],
        "venue": ["funding_system"],
        "date": ["from_date"],
        "authors": ["investigators"],
    },
}

# 一般的なシングルトン値で言語辞書として扱いたいキー
_LANG_KEYS = ("ja", "en")


def extract_lang_dict(value: Any) -> dict[str, Any]:
    """API の {'ja': ..., 'en': ...} 形式を素直に dict 化。

    スカラのみの場合は ja に入れる。None は空辞書。
    """
    if value is None:
        return {}
    if isinstance(value, dict):
        out: dict[str, Any] = {}
        for k in _LANG_KEYS:
            if k in value and value[k] not in (None, "", []):
                out[k] = value[k]
        return out
    # スカラ
    return {"ja": value}


def extract_lang_list(value: Any) -> dict[str, list[Any]]:
    """著者などのリスト系を {'ja': [...], 'en': [...]} に正規化。"""
    if value is None:
        return {}
    if isinstance(value, dict):
        out: dict[str, list[Any]] = {}
        for k in _LANG_KEYS:
            v = value.get(k)
            if v is None:
                continue
            if isinstance(v, list):
                # 中身が dict（{name: ..., affiliation: ...}）の場合は name を抜く
                names = [_author_name(a) for a in v if a is not None]
                names = [n for n in names if n]
                if names:
                    out[k] = names
            elif isinstance(v, str) and v:
                out[k] = [v]
        return out
    if isinstance(value, list):
        names = [_author_name(a) for a in value if a is not None]
        names = [n for n in names if n]
        return {"ja": names} if names else {}
    if isinstance(value, str) and value:
        return {"ja": [value]}
    return {}


def _author_name(a: Any) -> str | None:
    if isinstance(a, str):
        return a.strip() or None
    if isinstance(a, dict):
        # researchmap の著者オブジェクトは name / family_name + given_name 等が混在
        for k in ("name", "full_name", "display_name"):
            v = a.get(k)
            if isinstance(v, str) and v.strip():
                return v.strip()
            if isinstance(v, dict):
                d = extract_lang_dict(v)
                if d:
                    return d.get("ja") or d.get("en")
        fam = a.get("family_name")
        giv = a.get("given_name")
        if isinstance(fam, dict):
            fam = fam.get("ja") or fam.get("en")
        if isinstance(giv, dict):
            giv = giv.get("ja") or giv.get("en")
        if fam or giv:
            return " ".join(p for p in (fam, giv) if p)
    return None


def extract_year(date_str: str | None) -> int | None:
    """'2024-03' や '2024' から 2024 を取り出す。失敗時 None。"""
    if not date_str or not isinstance(date_str, str):
        return None
    m = re.match(r"(\d{4})", date_str)
    return int(m.group(1)) if m else None


def _normalize_date(value: Any) -> str | None:
    """ISO8601 風の日付文字列に揃える。

    辞書 {"from": "...", "to": "..."} のケースは from を採用。
    """
    if value is None:
        return None
    if isinstance(value, str):
        return value.strip() or None
    if isinstance(value, dict):
        for k in ("from", "value", "start"):
            v = value.get(k)
            if isinstance(v, str) and v.strip():
                return v.strip()
    return None


def _first(item: dict, keys: list[str]) -> Any:
    for k in keys:
        if k in item and item[k] not in (None, "", [], {}):
            return item[k]
    return None


def _build_url(item: dict, doi: str | None, fallback_id: str | None) -> str | None:
    if doi:
        return f"https://doi.org/{doi}"
    # link や url フィールドを優先
    for k in ("link", "url"):
        v = item.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
        if isinstance(v, dict):
            d = extract_lang_dict(v)
            for lk in ("ja", "en"):
                if lk in d and isinstance(d[lk], str) and d[lk]:
                    return d[lk]
    return fallback_id


def normalize(item: dict, ach_type: str, researcher_permalink: str) -> dict:
    """1件の業績を内部スキーマに変換する。"""
    mapping = _FIELD_MAP.get(ach_type, _FIELD_MAP["published_papers"])

    title = extract_lang_dict(_first(item, mapping["title"]))
    venue = extract_lang_dict(_first(item, mapping["venue"]))
    authors = extract_lang_list(_first(item, mapping["authors"]))
    date_raw = _normalize_date(_first(item, mapping["date"]))

    doi = item.get("doi")
    if isinstance(doi, str):
        doi = doi.strip() or None
    else:
        doi = None

    refereed = item.get("refereed")
    if not isinstance(refereed, bool):
        refereed = None
    invited = item.get("invited")
    if not isinstance(invited, bool):
        invited = None

    pub_id = item.get("@id") or item.get("id") or ""

    # extra は既知キーを除く全フィールド
    consumed = {
        "@id",
        "id",
        "doi",
        "refereed",
        "invited",
    }
    for keys in mapping.values():
        consumed.update(keys)
    extra = {k: v for k, v in item.items() if k not in consumed}

    return {
        "id": pub_id,
        "type": ach_type,
        "title": title,
        "authors": authors,
        "venue": venue,
        "year": extract_year(date_raw),
        "date": date_raw,
        "doi": doi,
        "url": _build_url(item, doi, pub_id if isinstance(pub_id, str) else None),
        "refereed": refereed,
        "invited": invited,
        "researcher_permalinks": [researcher_permalink],
        "extra": extra,
    }


def normalize_profile(item: dict, permalink: str) -> dict:
    """プロフィール JSON-LD を Researcher スキーマに変換する。"""
    name = extract_lang_dict(item.get("name") or item.get("full_name"))
    if not name:
        # family_name + given_name のフォールバック
        fam = extract_lang_dict(item.get("family_name"))
        giv = extract_lang_dict(item.get("given_name"))
        merged: dict[str, str] = {}
        for k in _LANG_KEYS:
            parts = [p for p in (fam.get(k), giv.get(k)) if p]
            if parts:
                merged[k] = " ".join(parts)
        name = merged

    # affiliation は profile 直下 or affiliations[0] のいずれか
    affil_src = item.get("affiliation")
    if affil_src is None and isinstance(item.get("affiliations"), list) and item["affiliations"]:
        affil_src = item["affiliations"][0]
    affiliation = None
    job_title = None
    if isinstance(affil_src, dict):
        # researchmap は affiliation 内に organization, section, job_title などを持つ
        org = affil_src.get("organization") or affil_src.get("name")
        section = affil_src.get("section") or affil_src.get("department")
        org_d = extract_lang_dict(org) if org is not None else {}
        sec_d = extract_lang_dict(section) if section is not None else {}
        merged = {}
        for k in _LANG_KEYS:
            parts = [p for p in (org_d.get(k), sec_d.get(k)) if p]
            if parts:
                merged[k] = " / ".join(parts)
        if merged:
            affiliation = merged
        jt = affil_src.get("job_title") or affil_src.get("job")
        if jt is not None:
            jd = extract_lang_dict(jt)
            if jd:
                job_title = jd
    elif isinstance(affil_src, (str, list)):
        affiliation = extract_lang_dict(affil_src if not isinstance(affil_src, list) else (affil_src[0] if affil_src else None))

    researcher_id = item.get("researcher_id") or item.get("researcher_number")
    if isinstance(researcher_id, dict):
        researcher_id = researcher_id.get("ja") or researcher_id.get("en")
    if researcher_id is not None and not isinstance(researcher_id, str):
        researcher_id = str(researcher_id)

    orcid = item.get("orcid") or item.get("ORCID")
    if not isinstance(orcid, str):
        orcid = None

    return {
        "permalink": permalink,
        "name": name,
        "affiliation": affiliation,
        "job_title": job_title,
        "profile_url": f"https://researchmap.jp/{permalink}",
        "researcher_id": researcher_id,
        "orcid": orcid,
    }


# 後方互換: dict 経由でアクセスしたい場合
NORMALIZERS: dict[str, Callable[[dict, str], dict]] = {
    t: (lambda item, permalink, t=t: normalize(item, t, permalink))
    for t in _FIELD_MAP
}
