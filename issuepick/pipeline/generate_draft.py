#!/usr/bin/env python3
"""수집한 경쟁 블로그 본문 → 분석 → 이슈픽 마크다운 초안 생성.

아로스100 10-34~10-35 (Aggregator + 글 생성)의 파이썬 구현.
2단계 Claude 호출:
  1단계 분석: 상위 3개 본문에서 공통 정보(필수) / 차별 정보 / 빠진 정보 추출
  2단계 작성: 분석 결과를 소스로, 이슈픽 front matter 규격의 새 글 생성
             (본문 문장 재사용 금지 — 정보만 사용, 표현은 새로)

사용:
  export ANTHROPIC_API_KEY=...
  python generate_draft.py briefs/청년도약계좌-조건.json --section youth

의존성: pip install anthropic
"""
import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

import anthropic

BASE = Path(__file__).parent
CONTENT_DIR = BASE.parent / "content"

MODEL = "claude-sonnet-5"

ANALYZE_PROMPT = """다음은 네이버 검색 상위 {n}개 블로그의 본문이다. 분석해서 정리하라.

1. 공통 정보 — 모든 글이 다루는 핵심 사실 (신청 조건, 금액, 기한, 방법 등). 새 글에 반드시 포함.
2. 차별 정보 — 특정 글만 가진 유용한 정보 (꿀팁, 주의사항, 실제 후기 요점)
3. 콘텐츠 갭 — 세 글 모두 빠뜨린 것, 독자가 궁금해할 질문
4. 구조 패턴 — 공통적으로 쓰는 소제목 흐름

숫자(금액·날짜·기한)는 표기된 그대로 옮기되, 글마다 다르면 "확인 필요"로 표시하라.

{bodies}"""

WRITE_PROMPT = """너는 정부지원금·정책 전문 블로거다. 아래 분석 자료를 근거로 새 글을 한 편 써라.

키워드: {keyword} (제목에 반드시 포함, 변형 금지)

규칙:
- 경쟁 글의 문장·표현을 재사용하지 말 것. 정보만 취하고 문장은 전부 새로 쓸 것.
- 공통 정보는 모두 포함, 차별 정보 중 유용한 것 반영, 콘텐츠 갭을 채워 차별화.
- 분량: 본문 2,000~3,000자. 소제목(##) 3~5개. 마지막에 자주 묻는 질문 3개(### Q).
- 문체: 단정하고 실용적. 과장·이모지 금지. "~합니다" 체.
- 숫자가 "확인 필요"면 본문에 쓰지 말고 대신 공식 확인을 안내.
- 출력은 아래 형식 그대로. front matter 값을 분석 자료에서 추론해 채워라.

---
title: "(숫자를 포함한 20자 내외 제목)"
date: {today}
draft: true
summary: "(카드에 노출될 한 줄, 80자 이내)"
targets: []
regions: ["전국"]
topics: []
amount: "(핵심 금액 한 줄, 없으면 빈칸)"
deadline: ""
apply_url: ""
source: ""
keywords: [{keyword_json}]
---

(본문)

분석 자료:
{analysis}"""


def ask(client, prompt: str, max_tokens: int = 4000) -> str:
    msg = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("brief", help="collect_bodies.py가 만든 briefs/*.json")
    ap.add_argument("--section", required=True,
                    choices=["subsidy", "youth", "welfare", "money", "tax", "housing"])
    args = ap.parse_args()

    brief = json.loads(Path(args.brief).read_text(encoding="utf-8"))
    keyword = brief["keyword"]
    comps = [c for c in brief["competitors"] if c.get("chars", 0) > 300]
    if not comps:
        sys.exit("본문이 수집된 경쟁 글이 없습니다. collect_bodies.py를 다시 실행하세요.")

    client = anthropic.Anthropic()

    bodies = "\n\n".join(
        f"=== [{c['rank']}위] {c['title']} ===\n{c['body'][:6000]}" for c in comps
    )
    print("1/2 경쟁 글 분석 중…")
    analysis = ask(client, ANALYZE_PROMPT.format(n=len(comps), bodies=bodies))

    print("2/2 초안 작성 중…")
    article = ask(client, WRITE_PROMPT.format(
        keyword=keyword,
        today=date.today().isoformat(),
        keyword_json=json.dumps(keyword, ensure_ascii=False),
        analysis=analysis,
    ), max_tokens=6000)

    # 코드펜스로 감싸 나오면 벗기기
    article = re.sub(r"^```[a-z]*\n|```$", "", article.strip())
    if not article.startswith("---"):
        article = "---\n" + article.split("---", 1)[-1].lstrip()

    slug = re.sub(r"[^\w가-힣]+", "-", keyword).strip("-")
    out = CONTENT_DIR / args.section / f"{slug}.md"
    out.write_text(article + "\n", encoding="utf-8")

    # 분석 결과도 검수용으로 보존
    Path(str(args.brief)).with_suffix(".analysis.md").write_text(analysis, encoding="utf-8")
    print(f"완료: {out}  (draft: true — 검수 후 해제하세요)")


if __name__ == "__main__":
    main()
