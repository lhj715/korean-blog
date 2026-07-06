#!/usr/bin/env python3
"""키워드 → 네이버 검색 API 상위 블로그 → m.blog 본문 전체 수집.

아로스100 10-32~10-34 워크플로의 파이썬 구현:
  1. 네이버 검색 API(블로그)로 키워드 상위 N개(정확도순) 조회
  2. blog.naver.com URL을 m.blog.naver.com 으로 변환 (모바일은 차단 없음)
  3. 본문 셀렉터(se-main-container / postViewArea)에서 텍스트 추출
  4. briefs/<키워드>.json 으로 저장 → generate_draft.py 의 입력

사용:
  export NAVER_CLIENT_ID=... NAVER_CLIENT_SECRET=...
  python collect_bodies.py "청년도약계좌 조건" [--top 3]

의존성: pip install requests beautifulsoup4
"""
import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE = Path(__file__).parent
BRIEF_DIR = BASE / "briefs"

SEARCH_URL = "https://openapi.naver.com/v1/search/blog.json"
UA = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile Safari/604.1"
}


def naver_search(keyword: str, top: int) -> list[dict]:
    cid = os.environ.get("NAVER_CLIENT_ID")
    secret = os.environ.get("NAVER_CLIENT_SECRET")
    if not (cid and secret):
        sys.exit("NAVER_CLIENT_ID / NAVER_CLIENT_SECRET 환경변수를 설정하세요.")
    r = requests.get(
        SEARCH_URL,
        params={"query": keyword, "display": max(top * 3, 10), "sort": "sim"},
        headers={"X-Naver-Client-Id": cid, "X-Naver-Client-Secret": secret},
        timeout=15,
    )
    r.raise_for_status()
    items = r.json().get("items", [])
    # 네이버 블로그만 (티스토리 등 제외), 상위 top개
    naver_only = [i for i in items if "blog.naver.com" in i.get("link", "")]
    return naver_only[:top]


def to_mobile(url: str) -> str:
    return url.replace("https://blog.naver.com", "https://m.blog.naver.com")


def strip_tags(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def fetch_body(url: str) -> str:
    """m.blog 페이지에서 본문 텍스트를 추출한다."""
    r = requests.get(to_mobile(url), headers=UA, timeout=20)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    body = soup.select_one("div.se-main-container, div#postViewArea, div#viewTypeSelector")
    if body is None:
        return ""
    text = body.get_text("\n", strip=True)
    # 과도한 빈 줄 정리
    return re.sub(r"\n{3,}", "\n\n", text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("keyword")
    ap.add_argument("--top", type=int, default=3, help="수집할 상위 블로그 수")
    args = ap.parse_args()

    print(f"검색: {args.keyword} (상위 {args.top}개)")
    results = naver_search(args.keyword, args.top)
    if not results:
        sys.exit("검색 결과에 네이버 블로그가 없습니다.")

    competitors = []
    for rank, item in enumerate(results, 1):
        title = strip_tags(item["title"])
        url = item["link"]
        print(f"  [{rank}] {title}")
        try:
            body = fetch_body(url)
        except Exception as e:
            print(f"      수집 실패: {e}", file=sys.stderr)
            body = ""
        competitors.append({
            "rank": rank,
            "title": title,
            "url": url,
            "mobile_url": to_mobile(url),
            "postdate": item.get("postdate", ""),
            "body": body,
            "chars": len(body),
        })
        time.sleep(1.5)  # 매너 딜레이

    BRIEF_DIR.mkdir(exist_ok=True)
    safe = re.sub(r"[^\w가-힣]+", "-", args.keyword).strip("-")
    out = BRIEF_DIR / f"{safe}.json"
    out.write_text(
        json.dumps(
            {"keyword": args.keyword, "collected_at": time.strftime("%Y-%m-%d %H:%M"),
             "competitors": competitors},
            ensure_ascii=False, indent=2,
        ),
        encoding="utf-8",
    )
    ok = sum(1 for c in competitors if c["chars"] > 300)
    print(f"완료: {ok}/{len(competitors)}건 본문 수집 → {out}")


if __name__ == "__main__":
    main()
