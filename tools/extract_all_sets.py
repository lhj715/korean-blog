#!/usr/bin/env python3
"""
리딩맵 기출 PDF → 전체 세트 JSON 초안 생성기
사용법: python3 extract_all_sets.py <pdf파일> [출력.json]
"""

import sys, json, re
from pathlib import Path

try:
    import fitz
except ImportError:
    print("pip install pymupdf"); sys.exit(1)

CHOICE_MAP = {'①': 1, '②': 2, '③': 3, '④': 4, '⑤': 5}
PAGE_H = 2000   # 가상 y 간격 (페이지 경계)
# 두 컬럼 정렬: 같은 y에서 LEFT가 RIGHT보다 먼저
COL_OFFSET = 9  # RIGHT 컬럼 y에 더해지는 정렬 가중치


def norm(t):
    t = re.sub(r'\s+', ' ', t).strip()
    t = re.sub(r' (이다|이며|이고|이나|이라|이어|이지|이든|이란|이자)', r'\1', t)
    return t


# ── 블록 수집 ────────────────────────────────────────────────
def load_blocks(pdf_path):
    doc = fitz.open(pdf_path)
    blocks = []
    for pi, page in enumerate(doc):
        for b in page.get_text('blocks'):
            x0, y0 = b[0], b[1]
            text = b[4].replace('\n', ' ').strip()
            if not text or y0 < 140 or y0 >= 1084:
                continue
            # 시험지 안내 문구 제거 (* 확인 사항, ◦답안지·◦이어서 등)
            if re.match(r'^[*◦]', text) or text.rstrip() == '하시오.':
                continue
            # LEFT 컬럼 우선: RIGHT 컬럼에 COL_OFFSET 추가
            col_off = 0 if x0 < 430 else COL_OFFSET
            vy = pi * PAGE_H + y0 + col_off
            blocks.append((vy, x0, text, pi, y0))
    doc.close()
    return sorted(blocks)


# ── 세트 경계 분할 ────────────────────────────────────────────
def split_by_set(blocks):
    """
    헤더 vy 기준으로 세트를 나누되, 헤더와 같은 페이지의 RIGHT 컬럼이
    헤더보다 낮은 vy에 있을 경우(=페이지 top → 이전 세트 범위에 잡힘)
    해당 블록을 새 세트에 포함시킨다.
    예) set-14-17 헤더: p4 LEFT y=665 / p4 RIGHT (y=159~563)에 지문 3·4문단
    """
    headers = []
    for vy, x0, text, pi, y0 in blocks:
        m = re.match(r'^\[(\d+)～(\d+)\]', text)
        if m:
            headers.append((int(m.group(1)), int(m.group(2)), vy, pi, x0))

    sets = []
    for i, (qs, qe, h_vy, h_pi, h_x0) in enumerate(headers):
        end_vy = headers[i+1][2] if i+1 < len(headers) else float('inf')

        sb = [(vy2, x0, text) for vy2, x0, text, pi2, y02 in blocks
              if h_vy <= vy2 < end_vy]

        # look-back: 헤더가 LEFT 컬럼일 때
        # 같은 페이지 RIGHT 컬럼이 헤더 vy보다 이른 경우 → 이 세트 지문 내용
        if h_x0 < 430:
            page_right_floor = h_pi * PAGE_H
            extra = [(vy2, x0, text) for vy2, x0, text, pi2, y02 in blocks
                     if x0 >= 430 and pi2 == h_pi and page_right_floor <= vy2 < h_vy]
            sb = sorted(sb + extra)

        # look-forward: 다음 세트 헤더가 RIGHT 컬럼일 때
        # 같은 페이지 LEFT 컬럼이 end_vy 이후에도 남아 있는 경우 → 이 세트 내용
        # (예: Q30 텍스트(LEFT y=701)와 [32-34] 헤더(RIGHT y=700)가 같은 y에 겹칠 때
        #  Q30 선지(LEFT y=727+)가 end_vy 밖으로 밀려나는 문제 방지)
        if i + 1 < len(headers):
            _, _, next_h_vy, next_h_pi, next_h_x0 = headers[i + 1]
            if next_h_x0 >= 430:
                page_end = (next_h_pi + 1) * PAGE_H
                extra_l = [(vy2, x0, text) for vy2, x0, text, pi2, y02 in blocks
                           if x0 < 430 and pi2 == next_h_pi and end_vy <= vy2 < page_end]
                if extra_l:
                    sb = sorted(sb + extra_l)

        sets.append({'q_range': [qs, qe], 'blocks': sb})
    return sets


# ── 단일/복합 판별 ────────────────────────────────────────────
def has_composite(blocks):
    for _, x0, text in blocks:
        if text.strip() in ('(가)', '(나)', '(다)'):
            return True
    return False


# ── 왼쪽 컬럼 지문 추출 ──────────────────────────────────────
def extract_passage_L(blocks, start_label=None):
    """
    start_label=None  → 단일지문 (바로 시작)
    start_label='(가)' → (가) 레이블 이후부터
    """
    paras, cur = [], []
    active = (start_label is None)

    for _, x0, text in blocks:
        if x0 >= 430:
            continue
        if re.match(r'^\[(\d+)～(\d+)\]', text):
            continue
        stripped = text.strip()
        if stripped == start_label:
            active = True; continue
        # (나) 레이블 만나면 왼쪽 지문 끝 (복합지문)
        if stripped in ('(나)', '(다)') and active:
            break
        if active and (re.match(r'^\d+[.．]\s', text) or re.match(r'^[①②③④⑤]', text)):
            break
        if not active:
            continue
        if 103 <= x0 <= 115:
            if cur: paras.append(norm(' '.join(cur)))
            cur = [text]
        elif 85 <= x0 <= 115:
            cur.append(text)

    if cur:
        paras.append(norm(' '.join(cur)))
    return paras


# ── 오른쪽 컬럼 지문 추출 ────────────────────────────────────
def extract_passage_R(blocks, label='(나)'):
    """오른쪽 컬럼에서 (나) 지문 추출"""
    paras, cur = [], []
    active = False

    def is_set_header(text):
        return bool(re.match(r'^\[(\d+)～(\d+)\]', text))

    def is_passage_label(text):
        return text.strip() in ('(가)', '(나)', '(다)')

    for _, x0, text in blocks:
        if x0 < 430:
            if text.strip() == label:
                active = True
            continue
        # 오른쪽 컬럼
        # 세트 헤더와 지문 레이블은 항상 skip
        if is_set_header(text) or is_passage_label(text):
            if text.strip() == label:
                active = True
            continue

        if not active:
            # 레이블 없이 오른쪽 컬럼 시작부터 (복합지문에서 (나) 맨 위부터)
            if 430 <= x0 <= 465 and not re.match(r'^\d+[.．]\s', text) and not re.match(r'^[①②③④⑤]', text):
                active = True

        if not active:
            continue
        # 오른쪽 문항 시작 → 지문 끝
        if re.match(r'^\d+[.．]\s', text) and 430 <= x0 <= 445:
            break
        if re.match(r'^[①②③④⑤]', text):
            break
        if re.match(r'^<보', text):
            break

        # 문단 구분 (x0≈455 들여쓰기, x0≈445 이어짐)
        if 450 <= x0 <= 465:
            if cur: paras.append(norm(' '.join(cur)))
            cur = [text]
        elif 430 <= x0 <= 452:
            cur.append(text)

    if cur:
        paras.append(norm(' '.join(cur)))
    return paras


# ── 단일 컬럼 상태기계 ────────────────────────────────────────
def _extract_col(col_blocks, is_right: bool):
    """
    col_blocks: 한 컬럼의 (vy, x0, text) 목록 (vy 순 정렬 상태)
    is_right: True → RIGHT컬럼 패턴 사용
    """
    Q_X_MAX = 445 if is_right else 430   # 문항 번호 x0 상한
    questions, cur_q, cur_c = [], None, None
    state = 'INIT'
    bogi_lines = []
    prev_vy = None   # 페이지 경계 감지용

    def flush_c():
        nonlocal cur_c
        if cur_c and cur_q:
            cur_q['choices'].append(dict(cur_c))
        cur_c = None

    def flush_q():
        flush_c()
        if cur_q:
            questions.append(dict(cur_q))

    for vy, x0, text in col_blocks:
        # 페이지를 넘어가는 선지 이어붙임 차단 (지문 텍스트 오염 방지)
        if (prev_vy is not None and vy - prev_vy > PAGE_H // 2
                and state == 'CHOICE'):
            flush_q(); cur_q = None; state = 'INIT'
        prev_vy = vy

        # 공통 skip / flush
        if re.match(r'^\[(\d+)～(\d+)\]', text):
            flush_q(); cur_q = None; state = 'INIT'   # 새 세트 → 이전 문항 마감
            continue
        if text.strip() in ('(가)', '(나)', '(다)'): continue
        if x0 > 500 and state != 'CHOICE': continue  # 중앙 정렬 제목 (선지 이어짐은 제외)

        # 새 문항 시작
        m_q = re.match(r'^(\d+)[.．]\s+(.*)', text)
        if m_q and x0 < Q_X_MAX:
            flush_q()
            num = int(m_q.group(1))
            q_text = m_q.group(2).strip()
            sm = re.search(r'\[(\d)점\]', q_text)
            score = int(sm.group(1)) if sm else 2
            q_text = re.sub(r'\s*\[\d점\]', '', q_text).strip()
            cur_q = dict(number=num, score=score, question=q_text,
                         type='', passage_ref=None, bogi=None,
                         choices=[], answer=None,
                         processing_method='normal_text_extraction',
                         confidence=0.99, needs_review=False,
                         explanation=None, keywords=[])
            cur_c = None; state = 'Q_TEXT'; bogi_lines = []
            continue

        if cur_q is None: continue

        # 보기 시작 — 독립 레이블만 (예: "<보 기>", "<보기>"). 선지 안 "<보기>에서..." 는 제외
        if re.match(r'^<보[^>]*>\s*$', text) and state in ('Q_TEXT', 'CHOICE'):
            state = 'BOGI'; bogi_lines = []; continue

        # 선지 시작 (한 블록에 여러 선지가 인라인으로 오는 경우 분리)
        if re.match(r'^[①②③④⑤]', text):
            if state == 'BOGI':
                cur_q['bogi'] = {'label': '보기',
                                 'content': ' '.join(bogi_lines),
                                 'has_image': False}
            # 블록 안에 ①② 같이 선지가 복수면 분리
            parts = re.split(r'(?<!\A)(?=[①②③④⑤])', text)
            for part in parts:
                part = part.strip()
                if not part: continue
                flush_c()
                no = CHOICE_MAP.get(part[0], 0)
                cur_c = {'no': no, 'text': part[1:].lstrip()}
            state = 'CHOICE'; continue

        if state == 'BOGI':
            bogi_lines.append(text); continue

        if state == 'Q_TEXT':
            sm = re.search(r'\[(\d)점\]', text)
            if sm:
                cur_q['score'] = int(sm.group(1))
                text = re.sub(r'\s*\[\d점\]', '', text).strip()
            if text: cur_q['question'] = (cur_q['question'] + ' ' + text).strip()
            continue

        if state == 'CHOICE' and cur_c:
            cur_c['text'] = (cur_c['text'] + ' ' + text).strip()
            continue

    flush_q()
    return questions


# ── 화작 초고 지문 추출 (RIGHT→LEFT 컬럼 넘김) ─────────────
def extract_hwa_passage(blocks):
    """
    화작 [학생의 초고] 형식: 지문이 오른쪽 컬럼에서 시작해
    다음 페이지 왼쪽 컬럼으로 이어지는 패턴 전용 추출.
    RIGHT 마지막 vy를 기준으로 LEFT 후반부만 이어붙임.
    """
    HWA_LABELS = {'[학생의 초고]', '[초고]'}

    right_blocks = [(vy, x0, t) for vy, x0, t in blocks if x0 >= 430]
    left_blocks  = [(vy, x0, t) for vy, x0, t in blocks if x0 <  430]

    # ① 오른쪽 컬럼 추출
    paras_r, cur, active, last_vy = [], [], False, -1
    for vy, x0, text in right_blocks:
        if re.match(r'^\[(\d+)～(\d+)\]', text): continue
        if text.strip() in HWA_LABELS:
            active = True; continue
        if not active: continue
        if re.match(r'^\d+[.．]\s', text) and x0 <= 445: break
        if re.match(r'^[①②③④⑤]', text): break
        last_vy = vy
        if 450 <= x0 <= 465:
            if cur: paras_r.append(norm(' '.join(cur)))
            cur = [text]
        elif 430 <= x0 <= 452:
            cur.append(text)
    if cur: paras_r.append(norm(' '.join(cur)))

    if last_vy < 0:
        return paras_r  # 화작 레이블 없음 → 빈 반환

    # ② 왼쪽 컬럼 이어짐: last_vy 이후 블록만 (다음 페이지)
    paras_l, cur = [], []
    for vy, x0, text in left_blocks:
        if vy <= last_vy: continue   # RIGHT 지문과 같은/이전 페이지 skip
        if re.match(r'^\[(\d+)～(\d+)\]', text): continue
        if re.match(r'^\d+[.．]\s', text): break   # 문항 시작
        if re.match(r'^[①②③④⑤]', text): break
        if 103 <= x0 <= 115:
            if cur: paras_l.append(norm(' '.join(cur)))
            cur = [text]
        elif 85 <= x0 <= 115:
            cur.append(text)
    if cur: paras_l.append(norm(' '.join(cur)))

    # 마지막 RIGHT 문단과 첫 LEFT 문단 연결 (페이지 넘김 연속 문단)
    if paras_r and paras_l:
        # 오른쪽 끝 문단이 마침표로 끝나지 않으면 이어붙임
        last_r = paras_r[-1]
        first_l = paras_l[0]
        if not re.search(r'[.。]$', last_r.rstrip()):
            paras_r[-1] = (last_r + ' ' + first_l).strip()
            paras_l = paras_l[1:]

    return paras_r + paras_l


# ── 문항 + 선지 추출 (컬럼 완전 분리) ───────────────────────
def extract_questions(blocks):
    """
    수능 2컬럼: LEFT·RIGHT 스트림을 완전히 분리 처리 후 번호로 병합.
    한 컬럼 내에서 다른 컬럼의 문항이 끊지 않으므로 선지 누락 없음.
    """
    left  = [(vy, x0, t) for vy, x0, t in blocks if x0 < 430]
    right = [(vy, x0, t) for vy, x0, t in blocks if x0 >= 430]
    qs_l = _extract_col(left,  is_right=False)
    qs_r = _extract_col(right, is_right=True)
    return sorted(qs_l + qs_r, key=lambda q: q['number'])


# ── 세트 → 구조체 변환 ───────────────────────────────────────
def build_set(set_info, set_id, q_lookup):
    """
    q_lookup: {번호: question_dict} — 전체 PDF에서 추출한 문항
    """
    blocks = set_info['blocks']
    q_range = set_info['q_range']

    composite = has_composite(blocks)
    passages = []

    if composite:
        paras_ga = extract_passage_L(blocks, start_label='(가)')
        if paras_ga:
            passages.append(dict(id='가', label='(가)', genre='독서',
                                 title=None, author=None,
                                 paragraphs=paras_ga, markers={}))
        paras_na = extract_passage_R(blocks, label='(나)')
        if paras_na:
            passages.append(dict(id='나', label='(나)', genre='독서',
                                 title=None, author=None,
                                 paragraphs=paras_na, markers={}))
    else:
        paras = extract_passage_L(blocks, start_label=None)

        # LEFT 마지막 문단이 마침표 없이 끊기면 RIGHT 컬럼에 이어짐
        if paras and not re.search(r'[.。？！]$', paras[-1].rstrip()):
            paras_r = extract_passage_R(blocks, label=None)
            if paras_r:
                paras[-1] = (paras[-1] + ' ' + paras_r[0]).strip()
                paras = paras + paras_r[1:]

        if not paras:
            # 화작 초고형: RIGHT컬럼 레이블 → 다음 페이지 LEFT 이어짐
            paras = extract_hwa_passage(blocks)
        if paras:
            passages.append(dict(id=None, label=None, genre='독서',
                                 title=None, author=None,
                                 paragraphs=paras, markers={}))

    # 문항: 선택과목(35-45)은 세트별 블록에서 직접 추출 (번호 중복 방지)
    qs, qe = q_range
    if qs >= 35:
        per_set_qs = extract_questions([(vy, x0, t) for vy, x0, t in blocks])
        questions = sorted([q for q in per_set_qs if qs <= q['number'] <= qe],
                           key=lambda q: q['number'])
    else:
        questions = [q_lookup[n] for n in range(qs, qe+1) if n in q_lookup]

    return dict(id=set_id, q_range=q_range,
                type='독서', topic='', field='',
                passages=passages, questions=questions)


# ── 메인 ─────────────────────────────────────────────────────
def main():
    if len(sys.argv) < 2:
        print("사용법: python3 extract_all_sets.py <pdf> [output.json]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else Path(pdf_path).stem + '_all_sets.json'

    blocks = load_blocks(pdf_path)

    # 1. 전체 문항 추출 (번호로 조회)
    all_q = extract_questions([(vy, x0, text) for vy, x0, text, pi, y0 in blocks])
    q_lookup = {q['number']: q for q in all_q}
    print(f"전체 문항 추출: {sorted(q_lookup.keys())}")

    # 2. 세트 경계 분할
    sets = split_by_set(blocks)

    print(f"\n세트 {len(sets)}개:")
    results = []
    for i, s in enumerate(sets):
        qr = s['q_range']
        set_id = f"set-{qr[0]:02d}-{qr[1]:02d}"
        built = build_set(s, set_id, q_lookup)
        results.append(built)
        p_count = sum(len(p['paragraphs']) for p in built['passages'])
        q_nums = [q['number'] for q in built['questions']]
        expected = list(range(qr[0], qr[1]+1))
        ok = '✅' if q_nums == expected else '❌'
        print(f"  {ok} {set_id}  지문{len(built['passages'])}개 ({p_count}문단)  문항{q_nums}")

    Path(out_path).write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"\n저장: {out_path}")


if __name__ == '__main__':
    main()
