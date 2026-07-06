# 이슈픽 수집 파이프라인

## 소스 3층 구조

| 층 | 소스 | 역할 | 저작권 |
|---|---|---|---|
| 주제 발굴 | 네이버 블로그 RSS (`rss.blog.naver.com/{ID}.xml`), 네이버 검색 API | "지금 뭘 쓸까" 신호 — 제목·타이밍만 사용 | 본문 재사용 금지 |
| 팩트 | 정부 부처 보도자료 RSS, 정부24, 복지로 | 금액·조건·기한의 근거 | 공공누리 — 출처 표기 후 자유 이용 |
| 작성 | Claude API | 상위글 구조 분석 + 공식 팩트로 새 글 생성 | 자체 콘텐츠 |

## 사용법

### ① 글감 발굴 (RSS 워치리스트)
```bash
pip install pyyaml
python watch_feeds.py        # 새 글감 후보 수집 → candidates/YYYY-MM-DD.json
```

### ② 본문 수집 (아로스100 10-32~34 방식)
키워드로 네이버 검색 API 상위 3개 블로그를 찾아 `m.blog.naver.com` 본문 전체를 수집:
```bash
pip install requests beautifulsoup4
export NAVER_CLIENT_ID=... NAVER_CLIENT_SECRET=...
python collect_bodies.py "청년도약계좌 조건"     # → briefs/청년도약계좌-조건.json
```

### ③ 초안 생성 (아로스100 10-34~35 방식, Claude 2단계)
1단계: 3개 본문에서 공통 정보·차별 정보·콘텐츠 갭 추출 → 2단계: 문장 재사용 없이 새 글 작성:
```bash
pip install anthropic
export ANTHROPIC_API_KEY=...
python generate_draft.py briefs/청년도약계좌-조건.json --section youth
# → ../content/youth/청년도약계좌-조건.md (draft: true)
# → briefs/*.analysis.md (검수용 분석 결과)
```

검수 후 `draft: true` 제거 → push → 자동 배포.

- `sources.yaml` — 워치리스트. 벤치마킹할 네이버 블로그는 `rss.blog.naver.com/블로그ID.xml` 형태로 추가
- `seen.json` — 중복 방지 (이미 본 글 URL)
- `candidates/` — 날짜별 글감 후보. 다음 단계(초안 생성)의 입력

## 다음 단계 (issue-pick 레포의 기존 파이프라인과 연결)

1. `candidates/*.json`에서 role=topic 후보 → 네이버 검색 API로 해당 키워드 상위 m.blog 글 수집·구조 분석
2. role=fact 후보(같은 주제의 보도자료)와 매칭 → Claude로 초안 생성
3. `../content/<section>/` 에 archetype 규격 마크다운으로 저장 (draft: true)
4. 검수 후 draft 해제 → push → 자동 배포

## 자동 실행 (GitHub Actions 예시)

```yaml
on:
  schedule:
    - cron: '0 22 * * *'   # 매일 아침 7시 KST
```
`watch_feeds.py` 실행 후 candidates/seen 변경분을 커밋하면 이력이 레포에 남는다.
