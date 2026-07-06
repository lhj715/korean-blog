# 이슈픽 (issue-pick.com) — Hugo 재구조화

정부지원금·정책·혜택 정보를 자동 발행하는 수익형 블로그의 새 구조.

## 사이트 구조

```
issuepick/
├── hugo.toml            # 6개 섹션 + 3개 택소노미(targets/regions/topics)
├── content/
│   ├── subsidy/         # 지원금·보조금
│   ├── youth/           # 청년정책
│   ├── welfare/         # 복지혜택
│   ├── money/           # 금융·절약
│   ├── tax/             # 세금·연말정산
│   └── housing/         # 주거·부동산
├── layouts/             # 카드 그리드 + 마감임박(D-day) 위젯 + fact-box
├── assets/css/main.css
└── archetypes/default.md  # 자동 발행 파이프라인이 채우는 front matter 규격
```

### Front matter 규격 (자동화 파이프라인 계약)

```yaml
title, date, summary          # 필수
targets: []                   # 청년 / 신혼부부 / 소상공인 / 전국민 …
regions: [전국]
topics: []                    # 키워드 클러스터 (청년도약계좌 등)
amount: "월 최대 70만원"       # 카드·fact-box에 초록색 강조
deadline: "2026-07-18"        # D-14 이내면 홈 '마감 임박'에 자동 노출, 지나면 '마감' 처리
apply_url, source, keywords
```

## 자동 발행 파이프라인 (네이버 API 기반)

```
① 키워드 발굴     네이버 검색광고 API(연관검색어·검색량) + 데이터랩 트렌드
        ↓         → 검색량 급상승 + 경쟁 낮은 키워드 선별
② 상위글 수집     네이버 검색 API → blog.naver.com 결과의 m.blog.naver.com
        ↓         모바일 URL로 상위 10개 본문 크롤링
③ 분석            상위글 공통 소제목·자주 나오는 질문·빠진 정보(콘텐츠 갭) 추출
        ↓
④ 초안 생성       Claude API — 공식 출처(정부24·보도자료) 팩트 + 상위글 구조 분석을
        ↓         근거로 front matter 포함 마크다운 생성 (archetype 규격 준수)
⑤ 검수·발행       사람 검수(draft: true → false) 또는 자동 발행
        ↓         → git push → GitHub Actions가 Hugo 빌드·배포
⑥ 갱신            deadline 지난 글 자동 '마감' 배지, 정책 변경 시 lastmod 갱신
```

- 중복 발행 방지: 빌드 시 생성되는 `/index.json`(전 글 목록)을 파이프라인이 조회
- 파이프라인 코드는 별도 레포(`lhj715/issue-pick`)에서 운영, 이 레포는 콘텐츠+사이트만 관리

## 로컬 실행

```bash
cd issuepick && hugo server
```
