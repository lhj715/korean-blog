# 기출 분석 파일 제작 기준

> **이 문서의 역할**: 리딩맵 기출 분석 파일을 처음부터 끝까지 일관되게 만들기 위한 단일 기준서.  
> 새 채팅창에서 작업을 시작할 때 이 파일을 먼저 읽고 따른다.  
> 기준 변경 시 이 파일만 수정하면 전 회차에 일괄 적용 가능.

---

## 목차

1. [작업 워크플로우](#1-작업-워크플로우)
2. [태깅 기준 (A)](#2-태깅-기준)
3. [콘텐츠 제작 기준 (B)](#3-콘텐츠-제작-기준)
4. [유형별 특이사항 (C)](#4-유형별-특이사항)
5. [PDF → HTML 변환 체크리스트 (D)](#5-pdf--html-변환-체크리스트)
6. [참조: CANONICAL 템플릿](#6-참조)

---

## 1. 작업 워크플로우

### 1.1 파일 작업 순서

```
1단계 (지문·문제 업로드)
  ├─ PDF 추출 → 각 세트 단락 구조 확인
  ├─ passage 블록 + ev span 없이 지문 텍스트만 올림
  ├─ q-block 구조 잡기 (발문 + 보기 + 선지)
  ├─ 정답표 대조 → correct 행·정답 번호 삽입
  └─ ★ 1단계 완료 = 파일 커밋 가능

2단계 (근거 표시)
  ├─ 지문에 ev span 삽입 (ev-qN-M id 부여)
  ├─ 선지에 src-tag 삽입 (정답/지문 근거 구분)
  └─ ★ 2단계 완료 = 파일 커밋 가능

3단계 (해설 달기)
  ├─ solution-body 작성 (answer-line + ask-read + 해설 문단)
  ├─ jt 테이블 작성 (모든 선지 판단·근거)
  └─ ★ 3단계 완료 = exam_index.json 등록 + 배포
```

**핵심 원칙: 해설(3단계)이 전부 완성되기 전에는 exam_index.json에 등록·배포하지 않는다.**  
1·2단계 완료 파일은 content/exams/ 폴더에 커밋해두되 인덱스 미등록 상태로 둔다.

### 1.2 새 채팅창에서 이어받을 때

새 채팅 시작 시 AI에게 전달할 사항:
```
- 이 파일(exam-production-standards.md) 먼저 읽을 것
- 작업 대상 파일 경로 알려줄 것
- 현재 어느 단계까지 완료됐는지 알려줄 것
- 참조 기준 파일: /home/lhj715/korean-blog/content/exams/2026/2026-03-go2-korean-analysis.md
  (완성된 고2 기출 기준 파일)
```

### 1.3 정답 검증

PDF 정답표 이미지 또는 다음 경로의 데이터로 대조:
```
/home/lhj715/downloads/ebsi-korean/site-ready-dataset/bundles/
```
올바른 정답 확인 없이 correct 행 지정 금지.

---

## 2. 태깅 기준

### 2.1 ev span ID 체계

**형식: `ev-qN-M`**
- N = 문항 번호
- M = 선지 번호 (①=1, ②=2, ③=3, ④=4, ⑤=5)

| 상황 | ID 형식 | 예시 |
|---|---|---|
| 단일 문항·선지 근거 | `ev-qN-M` | `ev-q5-2` (5번 ② 근거) |
| 같은 선지 근거가 2곳 | `ev-qN-Ma` / `ev-qN-Mb` | `ev-q5-2a`, `ev-q5-2b` |
| 여러 문항이 공유하는 span | 가장 낮은 문항 번호 기준 | Q4-②와 Q5-① 공유 → `ev-q4-2` |

**ev span 클래스:**
- 오답 근거: `class="ev"`
- 정답 근거: `class="ev ans"`

### 2.2 ev-tag (지문 → 문제 링크)

```html
<a class="ev-tag" href="#qN-M">N-②</a>
```
- href: `#qN-M` (선지 li의 id)
- 표시 텍스트: `N-②` (원문자)
- 정답 ev-tag: `class="ev-tag ans"`

### 2.3 src-tag (선지 → 지문 링크)

```html
<!-- 오답 선지 -->
<a class="src-tag" href="#ev-qN-M">지문 근거</a>

<!-- 정답 선지 -->
<a class="src-tag ans" href="#ev-qN-M">정답 근거</a>
```

### 2.4 ev span 배치 규칙

```html
<p>...앞 텍스트... <span class="ev" id="ev-q5-2">핵심 근거 문장.</span><a class="ev-tag" href="#q5-2">5-②</a> 뒤 텍스트...</p>
```

- span 닫는 태그 직후 ev-tag (공백 없음)
- 한 단락에 ev span 여러 개 → 연속 배치
- 가능한 짧게 감싸기 (핵심 문장 단위, 한 문장 이내 원칙)
- 하나의 span에 ev-tag 여러 개 붙는 것 허용 (여러 선지가 같은 근거를 공유할 때)

### 2.5 jt 테이블 판단값

`ok` class는 정답 행에만 사용.

| 발문 유형 | 정답 행 (`class="ok"`) | 오답 행 |
|---|---|---|
| 기본형 | `정답` | `오답` |
| 적절/부적절 | `부적절` (부적절이 정답일 때) 또는 `적절` | `적절` 또는 `부적절` |
| 일치/불일치 | `불일치` 또는 `일치` | 반대 |
| 반영/미반영 | `미반영` 또는 `반영` | 반대 |

### 2.6 bogi-label

PDF 원문 표기 그대로 사용. HTML 엔티티 필수.

```html
<p class="bogi-label">&lt; 보 기 &gt;</p>
<p class="bogi-label">&lt; 자 료 &gt;</p>
<p class="bogi-label">&lt; 학습 활동 &gt;</p>
<p class="bogi-label">&lt; 조건 &gt;</p>
```

---

## 3. 콘텐츠 제작 기준

### 3.1 파일 최상위 구조

```markdown
---
title: "YYYY년 M월 고2 국어 기출 분석"
category: "학력평가"
date: YYYY-MM-DD
keywords: ["고2", "YYYY년 M월", "학력평가", "국어", "기출 분석", "근거 표시", "혼자 공부"]
summary: "YYYY년 M월 고2 전국연합학력평가 국어 기출 분석 — 지문에 선지 판단 근거를 표시하고 발문 해석·선지 판단·오답 함정까지 담은 풀이."
---

<div class="exam-analysis">

<section class="exam-overview">
  <div class="exam-overview-item"><span>시행</span><strong>YYYY-MM-DD</strong></div>
  <div class="exam-overview-item"><span>대상</span><strong>고2</strong></div>
  <div class="exam-overview-item"><span>시험</span><strong>전국연합학력평가</strong></div>
  <div class="exam-overview-item"><span>분석 범위</span><strong>전체 45문항</strong></div>
</section>
<div id="set1" class="set-anchor"></div>

## 1~3번 화법 · 소제목
```

**금지**: `<nav class="set-nav">` 사용 안 함 (어떤 회차에도 없음)  
세트 앵커 `<div id="setN" class="set-anchor"></div>`는 h2 바로 앞에 배치.

### 3.2 세트 h2 제목 형식

```
## {시작번호}~{끝번호}번 {유형} · {지문 소제목}
```

유형 표기: `화법` / `문법` / `독서` / `문학` / `화법·작문` / `독서·작문`

### 3.3 read-guide 블록

모든 세트에 포함 (문법 단독 문항 세트 제외):

```html
<div class="read-guide">
  <div class="read-guide-head">이 지문, 이렇게 읽는다</div>
  <p>한 줄 요약.</p>
  <ul>
    <li><strong>핵심1</strong> — 설명.</li>
    <li><strong>핵심2</strong> — 설명.</li>
  </ul>
  <p class="read-guide-tip"><strong>출제 포인트 예고</strong> — N번·M번의 함정 예고.</p>
</div>
```

### 3.4 passage 블록

```html
<div class="passage">
  <p class="passage-guide">[N ~ M] 다음은 ...이다. 물음에 답하시오.<span class="passage-legend">LEGEND</span></p>
  <!-- 단락들 -->
</div>
```

**passage-legend 두 가지 중 선택:**

A. 지문 근거(파란)+정답 근거(초록) 모두 표시할 때:
```
<b>파란 밑줄</b>은 각 선지를 판단하는 지문 근거, 옆의 번호는 해당 문항·선지를 가리킵니다. <span class="click-hint">번호를 누르면 그 문제로, 선지의 '지문 근거'를 누르면 이 밑줄로 이동합니다.</span> (예: 1-④ = 1번 ④의 근거)
```

B. 정답 근거만 표시할 때:
```
<b style="color:#1f7a3d;border-color:#1f7a3d">초록 밑줄</b>은 정답 근거입니다. 옆 번호를 누르면 그 문제로 이동합니다.
```

### 3.5 지문 단락 유형별 태그

| 상황 | 태그 |
|---|---|
| 일반 단락 | `<p>내용</p>` |
| 대화 발화 | `<p class="dlg"><b>사회자:</b> 내용</p>` |
| [A][B] 구간 | `<div class="seg"><span class="seg-label">[ A ]</span>` + dlg들 + `</div>` |
| 시·운문 | `<pre class="verse">내용</pre>` |
| [중략] 줄거리 | `<p class="middle-omit">〔중략〕 줄거리 : 내용</p>` |
| 지문 출처·각주 | `<p class="footnote">* 출처 내용</p>` |
| (가)(나) 소지문 구분 | `<p class="src-label">(가)</p>` |

**단락 변환 원칙:**
- PDF 들여쓰기 또는 빈 줄로 구분된 단락 → `<p>` 1개
- `<p>` 태그 사이 빈 줄 없음
- 발표 지문(화자 1명)은 일반 `<p>` 사용 (dlg 불필요)

### 3.6 q-block 구조 (전체)

```html
<div class="q-block" id="probN">N
  <p class="q-stem">N. 발문 텍스트 <span class="q-rate">오답률 N.N%</span> <span class="q-pt-inline">[3점]</span></p>
  <!-- 보기가 있으면 여기 -->
  <ul class="q-opts">
    <li id="qN-1">① 선지 텍스트<a class="src-tag ans" href="#ev-qN-1">정답 근거</a></li>
    <li id="qN-2">② 선지 텍스트<a class="src-tag" href="#ev-qN-2">지문 근거</a></li>
    <li id="qN-3">③ 선지 텍스트</li>
    <li id="qN-4">④ 선지 텍스트</li>
    <li id="qN-5">⑤ 선지 텍스트</li>
  </ul>
  <details class="solution">
    <summary>해설 보기</summary>
    <div class="solution-body">
      <div class="question-analysis">
        <div class="answer-line"><span>정답</span><strong>①</strong></div>
        <p class="ask-read"><strong>발문 해석</strong> — 발문이 요구하는 것을 한 줄로.</p>
        <p>핵심 해설 문단. 정답 이유 중심.</p>
      </div>
      <table class="jt">
        <thead><tr><th>선지</th><th>판단</th><th>근거</th></tr></thead>
        <tbody>
          <tr class="correct"><td>①</td><td class="ok">정답</td><td>근거 한 줄.</td></tr>
          <tr><td>②</td><td>오답</td><td>근거 한 줄.</td></tr>
          <tr><td>③</td><td>오답</td><td>근거 한 줄.</td></tr>
          <tr><td>④</td><td>오답</td><td>근거 한 줄.</td></tr>
          <tr><td>⑤</td><td>오답</td><td>근거 한 줄.</td></tr>
        </tbody>
      </table>
    </div>
  </details>
</div>
```

**세부 규칙:**
- 선지 id: `qN-1` ~ `qN-5` (숫자, 원문자 아님)
- 3점 마커: `<span class="q-pt-inline">[3점]</span>` 발문 끝에 (PDF 확인 필수)
- 오답률: `<span class="q-rate">오답률 N.N%</span>` — EBSi 데이터 있을 때만
- src-tag: `</li>` 직전에 배치 (공백 없음)
- trap 블록: 자주 틀리는 이유가 있으면 jt 아래에 추가
  ```html
  <div class="trap">
    <div class="trap-head">조심할 점 — 제목</div>
    <p>함정 설명.</p>
  </div>
  ```

### 3.7 q-bogi 구조

```html
<div class="q-bogi">
  <p class="bogi-label">&lt; 보 기 &gt;</p>
  <p>텍스트 내용</p>
  <!-- 표 자료가 있으면: -->
  <div class="data-box">
    <p class="dt">[자료 1] 제목</p>
    <table class="data-tbl">
      <thead><tr><th>구분</th><th>A</th><th>B</th></tr></thead>
      <tbody><tr><td>항목</td><td>○</td><td>×</td></tr></tbody>
    </table>
  </div>
</div>
```

- 빈칸 [가]: `<span class="bogi-blank">[ 가 ]</span>`
- 보기 내 ①②③④⑤: `<b>①</b>` 굵게
- ⓐⓑⓒ 기호: HTML 특수문자 그대로 (`ⓐ`, `ⓑ`, `ⓒ`)
- ㉠㉡㉢ 기호: 그대로 (`㉠`, `㉡`)

### 3.8 해설 없는 상태 처리

**임시 placeholder 사용 금지.**  
해설이 없으면 `<details>` 블록 자체를 작성하지 않는다.  
1·2단계 작업 중에는 `</ul>` 뒤에서 바로 `</div>` 닫기.

```html
<!-- 1~2단계: 해설 없음 -->
<div class="q-block" id="probN">N
  <p class="q-stem">N. 발문</p>
  <ul class="q-opts">
    ...
  </ul>
</div>

<!-- 3단계: 해설 추가 후 -->
<div class="q-block" id="probN">N
  <p class="q-stem">N. 발문</p>
  <ul class="q-opts">
    ...
  </ul>
  <details class="solution">
    ...
  </details>
</div>
```

### 3.9 exam_index.json 등록 시점

파일 경로: `/home/lhj715/korean-blog/data/exam_index.json`

등록 조건: **3단계(해설) 전 회차 완료 후에만** 항목 추가.  
등록 후 배포(git push + deploy_hugo.sh).

```json
{
  "url": "/exams/YYYY/YYYY-MM-go2-korean-analysis/",
  "title": "YYYY년 M월 고2 국어 기출 분석",
  "year": YYYY,
  "month": M,
  "grade": 2,
  "type": "학력평가"
}
```

---

## 4. 유형별 특이사항

### 4.1 화법 지문

- 발표(화자 1명): 일반 `<p>` 단락
- 대화·토의·토론: `<p class="dlg"><b>이름:</b> 내용</p>`
- [A][B] 발화 구간:
  ```html
  <div class="seg"><span class="seg-label">[ A ]</span>
    <p class="dlg"><b>학생1:</b> ...</p>
    <p class="dlg"><b>학생2:</b> ...</p>
  </div>
  ```
- 학생 계획표(2번 유형): `<div class="q-plan">` 안에 `<p id="qN-M">◦ 계획 내용 <b>①</b><a class="src-tag" ...></a></p>`

### 4.2 문법 단독 문항

공유 지문 없음 → passage 블록 없음. 세트 안내문 사용:

```html
<p class="ask-read" style="margin:0 0 16px"><strong>안내</strong> — N~M번은 공유 지문 없이 각 〈보기〉만으로 푸는 문법 문항입니다.</p>
```

이후 각 q-block 안에 `<div class="q-bogi">` 직접 포함.

### 4.3 독서 지문

- 일반 단락: `<p>내용</p>`
- (가)(나) 복수 지문: `<p class="src-label">(가)</p>` 구분자 삽입
- 각주: `<p class="footnote">* 설명</p>`
- 도표/그래프: `<table class="data-tbl">` 또는 텍스트 설명으로 대체

### 4.4 문학 지문

**시·시조·가사:**
```html
<pre class="verse">첫째 연 / 첫 행
둘째 행
셋째 행

둘째 연 / 첫 행
</pre>
```
연 구분: 빈 줄 1개

**소설·수필:**
- 일반 `<p>` 단락
- `〔중략〕`: `<p class="middle-omit">〔중략〕 줄거리 : 줄거리 내용</p>`

**작품 제목·작가:**
- passage-guide 안에 명시하거나 h2 소제목에 포함
- 별도 라벨 필요 시: `<p class="src-label">「작품명」 — 작가</p>`

---

## 5. PDF → HTML 변환 체크리스트

### 5.1 지문 작업 (1단계)

```
☐ 세트별 passage-guide 문구 정확히 복사 ([N ~ M] 다음은 ...)
☐ 단락 경계: PDF 들여쓰기/빈줄 → <p> 1개씩
☐ 대화 지문: dlg 클래스 + <b>발화자:</b> 구분
☐ [A][B] 구간: seg 블록으로 묶음
☐ 시·운문: pre.verse 사용, 연 구분 빈 줄
☐ [중략]: middle-omit 클래스
☐ 각주·출처: footnote 클래스
```

### 5.2 문제 작업 (1단계)

```
☐ 문항 번호 id="probN" 정확히
☐ 3점 문항: q-pt-inline 추가 (PDF 3점 표기 확인)
☐ bogi-label: PDF 원문 그대로 (HTML 엔티티 &lt;&gt;)
☐ 선지 id: qN-1 ~ qN-5
☐ 선지 특수문자 유지: →, ≠, ≤, ㉠, ⓐ 등
☐ 표 자료: data-tbl로 구조화
☐ 이미지/그래프: 텍스트 설명 또는 [그림] 표기
☐ 정답 대조 → correct 행·ok 판단값 삽입
```

### 5.3 근거 표시 (2단계)

```
☐ ev-qN-M id 체계 준수
☐ ev id 파일 내 중복 없음 (grep "id=\"ev-" 확인)
☐ 정답 근거 span: class="ev ans"
☐ 모든 src-tag href → 실제 ev id와 1:1 매칭
☐ ev-tag 표시 텍스트: N-① 형식 (원문자)
☐ 정답 선지: src-tag ans
```

### 5.4 해설 작업 (3단계)

```
☐ 모든 문항 answer-line 정답 번호 확인
☐ ask-read 발문 해석 작성
☐ jt 테이블: 전 선지 판단·근거 작성
☐ 판단값 표준 준수 (정답/오답, 적절/부적절 등)
☐ 자주 틀리는 문항: trap 블록 추가
```

### 5.5 배포 전 최종 확인

```
☐ 해설 전 문항 완료
☐ exam_index.json 항목 추가
☐ set-anchor id 순서 확인 (set1~setN 빠짐 없음)
☐ git commit + push
☐ Lightsail deploy_hugo.sh 실행
```

---

## 6. 참조

### 기준 파일 경로

| 역할 | 경로 |
|---|---|
| 완성 기준 파일 (2026-03 고2) | `content/exams/2026/2026-03-go2-korean-analysis.md` |
| 완성 기준 파일 (2025-06 고2) | `content/exams/2025/2025-06-go2-korean-analysis.md` |
| CANONICAL HTML 템플릿 | `_templates/exam-analysis-CANONICAL.html` |
| 기출 원본 데이터 | `/home/lhj715/downloads/ebsi-korean/site-ready-dataset/bundles/` |
| 오답률 데이터 | `data/wrongrate/` |
| exam_index | `data/exam_index.json` |

### 파일 경로 규칙

```
content/exams/{연도}/{연도}-{월(2자리)}-go2-korean-analysis.md
```
예: `content/exams/2016/2016-06-go2-korean-analysis.md`

### 현재 완료된 회차 (2026-06-15 기준)

| 회차 | 단계 | 비고 |
|---|---|---|
| 2026-03 고2 | 3단계 완료 | CANONICAL 기준 파일 |
| 2025-03 고2 | 3단계 완료 | |
| 2025-06 고2 | 3단계 완료 | |
| 2025-09 고2 | 3단계 완료 | |
| 2025-10 고2 | 3단계 완료 | |
| 2016-06 고2 | 1단계 완료 | 2단계·3단계 미완 |
