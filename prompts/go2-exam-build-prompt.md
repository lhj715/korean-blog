# 고2 기출 분석 페이지 제작 프롬프트

> 어느 채팅 세션에서 작업해도 동일한 결과가 나오도록 규칙을 정리한 기준 문서입니다.  
> 파일 위치: `~/korean-blog/prompts/go2-exam-build-prompt.md`  
> 스크립트: `/tmp/rebuild_2023.py` (세션 종료 시 사라짐 → 필요 시 재작성)

---

## 1. 파일 구조 기준

완성본 참조 파일: `content/exams/2024/2024-09-go2-korean-analysis.md`  
(이 파일을 항상 골든 포맷으로 삼아 비교 검증)

### frontmatter
```yaml
---
title: "{year}년 {month}월 고2 국어 기출 분석"
category: "학력평가"
date: {YYYY-MM-DD}
keywords: ["고2", "{year}년 {month}월", "학력평가", "국어", "기출 분석", "근거 표시"]
summary: "{year}년 {month}월 고2 전국연합학력평가 국어 기출 분석 — 지문에 선지 판단 근거를 표시한 풀이."
---
```

### 페이지 시작 (frontmatter 아래)
```html
<div class="exam-analysis">

<section class="exam-overview">
  <div class="exam-overview-item"><span>시행</span><strong>{YYYY-MM-DD}</strong></div>
  <div class="exam-overview-item"><span>대상</span><strong>고2</strong></div>
  <div class="exam-overview-item"><span>시험</span><strong>전국연합학력평가</strong></div>
  <div class="exam-overview-item"><span>분석 범위</span><strong>전체 45문항</strong></div>
</section>
```

---

## 2. 섹션 헤더 형식

```
## {시작}~{끝}번 {장르} · {핵심 주제}
```

### 장르 표기 규칙

| 지문 유형 | 표기 |
|---|---|
| 발표·강연 단독 | `화법` |
| 대화 + 작문 | `화법·작문` |
| 작문 단독 | `작문` |
| 언어·문법 문항 | `문법` |
| 현대소설 | `현대소설` |
| 고전소설 | `고전소설` |
| 현대시 | `현대시` |
| 고전시가 | `고전시가` |
| 고전시가 + 수필 | `고전시가·수필` |
| 비문학 인문 | `독서(인문)` |
| 비문학 과학·기술 | `독서(과학·기술)` |
| 비문학 사회 | `독서(사회)` |
| 시 + 소설 복합 | `갈래 복합` |

### 핵심 주제 표기 규칙

- **서술형 금지**: "~이다", "~다", "~임" 등 문장 끝맺음 절대 금지
- **명사구로만 끝낼 것**
- 화법·발표: 주제를 간결하게 → `조선 시대 전통 모자 흑립 발표`
- 소설·시: 작가명 + 「작품명」 → `오정희 「겨울 뜸부기」`
- 독서: 핵심 개념 명사구 → `니체의 힘에의 의지와 아곤`
- 복합 지문: 두 작품 나열 → `「금루사」 · 「회룡사관폭기」`

### 올바른 예시 (2026년 기준)

```
## 1~3번 화법 · 발표 속 의문문의 기능
## 4~6번 화법 · 폐전지 분리배출 토의
## 7~10번 문법 · 띄어쓰기·중세국어·피동·음운 변동
## 11~13번 독서 · 국제 물품 매매와 위험 부담(CISG)
## 27~30번 현대소설 · 오정희 「겨울 뜸부기」
## 38~42번 고전시가·수필 · 「금강별곡」과 「회룡사관폭기」
## 43~45번 현대시 · 조지훈 「향문」과 박성우 「두꺼비」
```

---

## 3. 지문(passage) 블록

```html
<div class="passage">
  <p class="passage-guide">[{시작} ~ {끝}] {안내문}<span class="passage-legend">
    <b style="color:#1f7a3d;border-color:#1f7a3d">초록 밑줄</b>은 정답 근거,
    <b>파란 밑줄</b>은 지문 근거입니다.</span></p>
  <p>지문 본문...</p>
  <p><span class="ev ans" id="ev{N}">정답 근거 문장</span>
     <a class="ev-tag ans" href="#q{N}-{정답인덱스}">{N}-{정답문자}</a></p>
</div>
```

### ev 스팬 규칙

- `id="ev{문항번호}"` — 문항 번호와 1:1 매칭
- ev 스팬이 없으면 정답 근거 버튼을 달지 않음 (링크 걸 곳이 없으면 버튼 불필요)
- 한 문항당 ev 스팬 1개 (가장 핵심적인 문장 1개만)
- 반드시 지문 원문에 실제로 존재하는 문장만 사용

---

## 4. 문항(q-block) 구조

```html
<div class="q-block" id="prob{N}">
  <p class="q-stem">{N}. {발문}</p>
  <ul class="q-opts">
    <li id="q{N}-1">① 선지 텍스트</li>
    <li id="q{N}-2">② 선지 텍스트<a class="src-tag ans" href="#ev{N}">정답 근거</a></li>
    <li id="q{N}-3">③ 선지 텍스트</li>
    <li id="q{N}-4">④ 선지 텍스트</li>
    <li id="q{N}-5">⑤ 선지 텍스트</li>
  </ul>
  <details class="solution">
    <summary>해설 보기</summary>
    <div class="solution-body">
      <div class="question-analysis">
        <div class="answer-line"><span>정답</span><strong>{정답문자}</strong></div>
        <p class="ask-read"><strong>발문 해석</strong> — 선지와 지문을 1:1로 대조한다.</p>
      </div>
      <table class="jt">
        <thead><tr><th>선지</th><th>판단</th><th>근거</th></tr></thead>
        <tbody>
          <tr class="correct"><td>②</td><td class="ok">정답</td><td>해설 참조.</td></tr>
          <tr><td>①</td><td>오답</td><td>해설 참조.</td></tr>
          ...
        </tbody>
      </table>
    </div>
  </details>
</div>
```

### q-block 규칙

- q-block 안에 문항 번호를 단독으로 쓰지 않음 (`<p class="q-stem">` 안에만)
- 선지는 ①②③④⑤ 순서 유지
- `id="q{N}-{인덱스}"` 형식 (①=1, ②=2, ③=3, ④=4, ⑤=5)
- 정답 선지에만 `src-tag ans` 버튼 부착 (ev 스팬 있을 때만)

---

## 5. 검증 체크리스트 (파일 완성 후 필수 실행)

```python
# 검증 항목
# 1. q-block 수가 45개인가?
# 2. ev 스팬 id="evN"이 있으면, 정답 선지에 href="#evN" 버튼이 있는가?
# 3. 정답 선지에 버튼이 있는데 ev 스팬이 없는 고아 버튼은 없는가?
# 4. jt 테이블에 5개 선지 행이 모두 있는가?
# 5. answer-line에 정답이 표시되어 있는가?
# 6. 섹션 헤더에 서술형 어미(이다/다/임)가 없는가?
# 7. 문항 번호가 q-block 안에 단독으로 있지 않은가?
```

---

## 6. PDF 소스 위치

```
문제지: /mnt/c/Users/관사/Documents/Codex/2026-05-27/goal/downloads/ebsi-korean/pdf/
패턴: YYYYMMDD-go2-problem-kor_mun_*.pdf
     YYYYMMDD-go2-explanation-kor_hsj_*.pdf
```

### 연도-월 → PDF 파일명 매핑

| 시험 | 문제 PDF |
|---|---|
| 2023-03 | 20230323-go2-problem-kor_mun_46J3446R.pdf |
| 2023-06 | 20230601-go2-problem-kor_mun_J9497Q75.pdf |
| 2023-09 | 20230906-go2-problem-kor_mun_P5SP1P3D.pdf |
| 2023-12 | 20231219-go2-problem-kor_mun_YE1S7AQC.pdf |

---

## 7. 주의사항

- `━━━━━` 등 PDF 구분선은 추출 시 반드시 제거
- 페이지 헤더("고2 국어영역", "제1교시" 등)도 제거
- 선지 텍스트의 `<` `>` 는 `&lt;` `&gt;` 로 이스케이프
- Hugo에서 `~`(물결)이 취소선으로 렌더링됨 → `〜`(전각) 또는 `-`로 대체
