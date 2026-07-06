#!/usr/bin/env python3
"""워치리스트 RSS를 폴링해서 '글감 후보'를 만든다.

흐름:
  sources.yaml의 피드 조회 → 키워드 필터 → 이미 본 글 제외(seen.json)
  → candidates/YYYY-MM-DD.json 으로 저장

이 스크립트는 수집·선별까지만 담당한다. 글 생성은 다음 단계
(generate_draft.py, Claude API)에서 후보 파일을 읽어 수행한다.
표준 라이브러리만 사용 (yaml 제외: pip install pyyaml).
"""
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

import yaml

BASE = Path(__file__).parent
SEEN_FILE = BASE / "seen.json"
CAND_DIR = BASE / "candidates"

UA = {"User-Agent": "Mozilla/5.0 (issuepick feed watcher)"}


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read()


def parse_rss(raw: bytes):
    """RSS 2.0 / Atom 모두에서 (title, link, pubdate, description) 추출."""
    root = ET.fromstring(raw)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    items = root.findall(".//item") or root.findall(".//atom:entry", ns)
    for it in items:
        def text(tag):
            el = it.find(tag) if it.find(tag) is not None else it.find(f"atom:{tag}", ns)
            return (el.text or "").strip() if el is not None and el.text else ""
        link = text("link")
        if not link:  # Atom은 link가 href 속성
            el = it.find("atom:link", ns)
            link = el.get("href", "") if el is not None else ""
        yield {
            "title": re.sub(r"<[^>]+>", "", text("title")),
            "link": link,
            "pub": text("pubDate") or text("updated"),
            "desc": re.sub(r"<[^>]+>", "", text("description"))[:300],
        }


def main():
    cfg = yaml.safe_load((BASE / "sources.yaml").read_text(encoding="utf-8"))
    inc = cfg.get("include_keywords", [])
    exc = cfg.get("exclude_keywords", [])
    seen = set(json.loads(SEEN_FILE.read_text()) if SEEN_FILE.exists() else [])

    candidates = []
    for feed in cfg["feeds"]:
        if not feed.get("enabled", True):
            continue
        try:
            raw = fetch(feed["url"])
        except Exception as e:
            print(f"[skip] {feed['id']}: {e}", file=sys.stderr)
            continue
        for item in parse_rss(raw):
            if item["link"] in seen or not item["title"]:
                continue
            title = item["title"]
            if inc and not any(k in title for k in inc):
                continue
            if any(k in title for k in exc):
                continue
            candidates.append({
                **item,
                "source_id": feed["id"],
                "source_name": feed["name"],
                "role": feed["role"],           # topic=주제 신호, fact=근거
                "sections": feed["sections"],
            })
            seen.add(item["link"])

    if candidates:
        CAND_DIR.mkdir(exist_ok=True)
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        out = CAND_DIR / f"{today}.json"
        existing = json.loads(out.read_text(encoding="utf-8")) if out.exists() else []
        out.write_text(
            json.dumps(existing + candidates, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"{len(candidates)}건 후보 추가 → {out}")
    else:
        print("새 후보 없음")

    SEEN_FILE.write_text(json.dumps(sorted(seen), ensure_ascii=False, indent=0))


if __name__ == "__main__":
    main()
