#!/usr/bin/env python3
"""
리딩맵 기출 PDF → JSON 초안 자동 생성기
사용법: python3 extract_draft.py <pdf파일> [페이지번호(0부터)]
예시:  python3 extract_draft.py 문제지.pdf 0
"""

import sys, json, re
from pathlib import Path

try:
    import fitz
except ImportError:
    print("pip install pymupdf"); sys.exit(1)

CHOICE_MAP = {'①': 1, '②': 2, '③': 3, '④': 4, '⑤': 5}


# ── 정규화 ────────────────────────────────────────────
def norm(text: str) -> str:
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r' (이다|이며|이고|이나|이라|이어|이지)', r'\1', text)
    return text


# ── 블록 분류 ─────────────────────────────────────────
def classify(x0: float, text: str) -> str:
    if re.match(r'^\[\d+～\d+\]', text):   return 'SET_HEADER'
    if re.match(r'^\d+[.．]\s', text):
        return 'Q_LEFT' if x0 < 430 else 'Q_RIGHT'
    if re.match(r'^[①②③④⑤]', text):
        return 'C_LEFT' if x0 < 430 else 'C_RIGHT'
    if re.match(r'^<보', text):             return 'BOGI'
    if x0 < 430:
        if 103 <= x0 <= 115:               return 'PARA_START'
        if 88  <= x0 <= 102:               return 'PARA_CONT'
        if 105 <= x0 <= 115:               return 'C_CONT_LEFT'
    else:
        if 433 <= x0 <= 443:               return 'Q_RIGHT'
        if 443 <= x0 <= 456:               return 'Q_CONT_RIGHT'
        if 453 <= x0 <= 465:               return 'C_CONT_RIGHT'
    return 'IGNORE'


# ── 문단 추출 (왼쪽 컬럼) ────────────────────────────
def extract_paragraphs(left_blocks):
    paragraphs = []
    current = []
    for _, x0, text in left_blocks:
        tag = classify(x0, text)
        if tag in ('Q_LEFT', 'C_LEFT'):
            break
        if tag == 'SET_HEADER':
            continue
        if tag == 'PARA_START' and current:
            paragraphs.append(norm(' '.join(current)))
            current = [text]
        elif tag in ('PARA_START', 'PARA_CONT'):
            current.append(text)
    if current:
        paragraphs.append(norm(' '.join(current)))
    return paragraphs


# ── 문항 + 선지 추출 ──────────────────────────────────
def extract_questions(blocks, col='left'):
    """
    col='left'  → Q_LEFT, C_LEFT, C_CONT_LEFT
    col='right' → Q_RIGHT, Q_CONT_RIGHT, C_RIGHT, C_CONT_RIGHT
    """
    q_tag  = 'Q_LEFT'  if col == 'left'  else 'Q_RIGHT'
    qc_tag = None      if col == 'left'  else 'Q_CONT_RIGHT'
    c_tag  = 'C_LEFT'  if col == 'left'  else 'C_RIGHT'
    cc_tag = 'C_CONT_LEFT' if col == 'left' else 'C_CONT_RIGHT'

    questions = []
    cur_q = None
    cur_c = None
    bogi_active = False

    for _, x0, text in blocks:
        tag = classify(x0, text)

        # 보기 감지
        if tag == 'BOGI':
            bogi_active = True
            if cur_q:
                cur_q['bogi'] = {'label': '보기', 'content': '', 'has_image': False}
            continue

        # 새 문항 시작
        if tag == q_tag:
            if cur_q:
                if cur_c:
                    cur_q['choices'].append(cur_c); cur_c = None
                questions.append(cur_q)
            m = re.match(r'^(\d+)[.．]\s*(.*)', text)
            num = int(m.group(1))
            q_text = m.group(2).strip()
            score_m = re.search(r'\[(\d)점\]', q_text)
            score = int(score_m.group(1)) if score_m else 2
            q_text = re.sub(r'\s*\[\d점\]', '', q_text).strip()
            cur_q = {
                'number': num,
                'score': score,
                'question': q_text,
                'type': '',
                'passage_ref': None,
                'bogi': None,
                'choices': [],
                'answer': None,
                'has_image': False,
                'explanation': None,
                'keywords': []
            }
            bogi_active = False
            cur_c = None
            continue

        # 문항 이어짐 (오른쪽 컬럼만)
        if qc_tag and tag == qc_tag and cur_q and not cur_q['choices']:
            score_m = re.search(r'\[(\d)점\]', text)
            if score_m:
                cur_q['score'] = int(score_m.group(1))
                text = re.sub(r'\s*\[\d점\]', '', text).strip()
            cur_q['question'] = (cur_q['question'] + ' ' + text).strip()
            continue

        # 선지 시작
        if tag == c_tag and cur_q:
            if cur_c:
                cur_q['choices'].append(cur_c)
            no = CHOICE_MAP.get(text[0], 0)
            body = text[1:].strip()
            if ' ' in body[:2]:  # "① 본문" → "본문"
                body = body.lstrip()
            cur_c = {'no': no, 'text': body}
            continue

        # 선지 이어짐 (명시적 태그 or x0 애매한 경우 cur_c 있으면 이어붙임)
        if (tag == cc_tag or (cur_c and tag in ('PARA_START', 'PARA_CONT'))) and cur_c:
            cur_c['text'] = (cur_c['text'] + ' ' + text).strip()
            continue

    if cur_q:
        if cur_c:
            cur_q['choices'].append(cur_c)
        questions.append(cur_q)

    return questions


# ── 페이지 파싱 ───────────────────────────────────────
def parse_page(page):
    raw = page.get_text('blocks')
    blocks = sorted(
        [(b[1], b[0], b[4].replace('\n', ' ').strip()) for b in raw if b[4].strip()],
        key=lambda x: x[0]
    )

    # 헤더/푸터 제거 (y < 200 or y > 1070)
    blocks = [(y, x0, t) for y, x0, t in blocks if 200 <= y <= 1070]

    # 세트 헤더 찾기
    set_headers = []
    for y, x0, text in blocks:
        m = re.match(r'\[(\d+)～(\d+)\]', text)
        if m:
            set_headers.append({'q_range': [int(m.group(1)), int(m.group(2))], 'y': y})

    # 왼쪽 / 오른쪽 분리
    left  = [(y, x0, t) for y, x0, t in blocks if x0 < 430]
    right = [(y, x0, t) for y, x0, t in blocks if x0 >= 430]

    paragraphs = extract_paragraphs(left)

    # 왼쪽 문항 추출 (지문 이후 부분)
    left_after_passage = []
    in_q = False
    for y, x0, text in left:
        tag = classify(x0, text)
        if tag in ('Q_LEFT', 'C_LEFT', 'C_CONT_LEFT'):
            in_q = True
        if in_q:
            left_after_passage.append((y, x0, text))

    q_left  = extract_questions(left_after_passage, col='left')
    q_right = extract_questions(right, col='right')

    all_questions = sorted(q_left + q_right, key=lambda q: q['number'])

    return {
        'set_headers': set_headers,
        'paragraphs': paragraphs,
        'questions': all_questions
    }


# ── 메인 ─────────────────────────────────────────────
def main():
    if len(sys.argv) < 2:
        print("사용법: python3 extract_draft.py <pdf> [페이지(0부터)]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    page_idx = int(sys.argv[2]) if len(sys.argv) > 2 else 0

    doc = fitz.open(pdf_path)
    result = parse_page(doc[page_idx])
    doc.close()

    print(f"세트 헤더: {result['set_headers']}")
    print(f"문단 수: {len(result['paragraphs'])}")
    print(f"문항 수: {len(result['questions'])}")
    print()

    for i, p in enumerate(result['paragraphs'], 1):
        print(f"[{i}문단] {p[:80]}...")
    print()

    for q in result['questions']:
        print(f"Q{q['number']:02d} ({q['score']}점) {q['question'][:60]}")
        for c in q['choices']:
            print(f"  {c['no']}. {c['text'][:50]}")
        print()

    # JSON 초안 출력
    draft = {
        'paragraphs': result['paragraphs'],
        'questions': result['questions']
    }
    out_path = Path(pdf_path).stem + f'_p{page_idx}_draft.json'
    Path(out_path).write_text(json.dumps(draft, ensure_ascii=False, indent=2))
    print(f"초안 저장: {out_path}")


if __name__ == '__main__':
    main()
