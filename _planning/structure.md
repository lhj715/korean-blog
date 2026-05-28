# Phase 2 — 사이트 구조 설계 (readingmap.kr)

대상: 고1~고3. 세 기둥 = **문학 · 문법 · 기출 자료실** (추후 독서·화법과작문 확장 가능).

## 1. 최상위 메뉴
```
홈
├── 문학      작품 아카이브 (핵심, 다축 탐색)
├── 문법      언어 체계 + 어휘
├── 기출      수능/모평/학평 문제·해설·PDF 자료실
└── 검색
(향후 추가: 독서, 화법과작문)
```

## 2. 문학 (content/literature/works/)
작품 = 콘텐츠 파일 1개 + 정형 메타. 목록·연표·필터는 자동 생성.

### 다축 탐색 (Hugo taxonomy로 동시 태깅)
- **갈래(genre)**: 고전시가 / 현대시 / 고전산문 / 현대소설 / 극 / 수필
- **작가(author)**
- **시대(period)**: 고대 / 고려 / 조선 / 근대(개화~1945) / 현대(1945~)
- **출제연도(exam)**: "2016-수능" 등 출제 이력
- (학년 축은 사용하지 않기로 함 — 2026-05-28)

### 작품 front matter 스키마
```yaml
title: 자화상
slug: jahwasang
author: 윤동주
genre: 현대시
period: 근대
year_approx: 1939
form: 자유시·서정시
source: 하늘과 바람과 별과 시
exam: [2016-수능]          # 출제이력 (taxonomy)
themes: [자아성찰, 부끄러움]
keywords: [우물, 자아성찰]
copyright: public          # public(원문게재가능) | protected(발췌·해설만)
summary: 한 줄 요약
```
본문 섹션(템플릿 권장 순서): 원문 → 현대어 풀이(고전) → 해제 → 핵심정리(주제·특징) → 시어·구절 풀이 → 출제 이력 → 관련 작품.

## 3. 문법 (content/grammar/)
체계별 분류 (내신 + 언어와매체 '언어'):
```
음운       음운과 음운변동
단어       품사 / 단어형성 / 의미관계
문장       문장성분 / 문장구조 / 문법요소(높임·시제·피동사동·부정)
담화       담화의 개념과 표현
국어사     중세국어 / 국어의 변천
어문규정   한글맞춤법 / 표준어 / 띄어쓰기 / 외래어표기
어휘       한자성어 / 속담·관용어 / 고유어
```
문법 항목 front matter: title / category(위 7분류) / grade / keywords / 기출연계.

## 4. 기출 자료실 (content/exams/)
분류 축: **연도 × 시험종류**.
```
시험종류: 학력평가(3·4·6·7·9·10월) / 모의평가(6·9월) / 수능
연도: 2017 ~ 현재
항목별 제공: 문제지 PDF · 정답표 · (지문분석/해설) · 출제작품 → 문학DB 링크
```
- 평가원(수능·모평) PDF: `teacher-materials/kice/collect.py`가 자동 수집 → exams/로 편입.
- 출제 작품을 문학 작품 페이지와 상호 링크(이 작품이 나온 시험 ↔ 이 시험에 나온 작품).

## 5. 자동 수집 → 사이트 반영 파이프라인 (Phase 3에서 구현)
```
[출처: sources.yaml] → [collector(평가원PDF / m.blog 스크랩)] → [원자료 보관]
   → [가공·요약·메타태깅] → [content/*.md 생성] → [hugo build] → [git push] → 배포
```
priority 1(박전현 등)은 신규 글 주기 점검, kice는 시험 시즌 갱신.

## 6. 기술/배포
- Hugo(정적) + 커스텀 경량 레이아웃(블로그형 테마 대신 아카이브형).
- 디자인: Noto Serif KR(제목)+Noto Sans KR(본문), 한지/먹 톤.
- 배포: GitHub(SoT) → Cloudflare Pages (또는 카페24 분리 후 정적 호스팅).
- readingmap.kr DNS: 현재 WP(CF 프록시) → 새 정적사이트로 전환 (Phase 3, 사용자 확인 후).
```
content/
  _index.md
  literature/{_index.md, works/<slug>.md}
  grammar/{_index.md, <slug>.md}
  exams/{_index.md, <year>/<exam>.md}
layouts/  (baseof, home, list, single, taxonomy)
data/     (메뉴·상수)
assets/css/
```
