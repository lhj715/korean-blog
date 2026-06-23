#!/usr/bin/env python3
"""
PDF vs JSON 지문 원문 감사기 (지문 전용)
- 세트별 PDF (가)(나)(다) 라벨 수 vs JSON passages 수 비교
- 지문 텍스트 길이 비율
- 누락 후보 단어 (PDF에만 있는 4자 이상 한국어 단어)

선지 비교는 하지 않음 (2컬럼 오탐 문제로 신뢰도 낮음)
"""
import json, re, sys
from pathlib import Path

import fitz

PDF  = Path('/home/lhj715/teacher-materials/kice/2025/수능/문제지.pdf')
JSON = Path('/home/lhj715/korean-blog/data/exams/2025-수능.json')
PAGE_H   = 2000
COL_OFF  = 9
RATIO_LO = 0.80   # JSON 지문이 PDF의 80% 미만이면 경고
RATIO_HI = 1.40   # JSON 지문이 PDF의 140% 초과이면 경고
MISSING_THRESHOLD = 3  # 누락 후보 단어 이 이상이면 경고


def load_pdf_blocks():
    doc = fitz.open(str(PDF))
    blocks = []
    for pi, page in enumerate(doc):
        for b in page.get_text('blocks'):
            x0, y0, x1, y1, text = b[0], b[1], b[2], b[3], b[4]
            text = text.replace('\n', ' ').strip()
            if not text or y0 < 140 or y0 >= 1084:
                continue
            if re.match(r'^[*◦]', text) or text.rstrip() == '하시오.':
                continue
            col_off = COL_OFF if x0 >= 430 else 0
            vy = pi * PAGE_H + y0 + col_off
            blocks.append((vy, x0, text, pi))
    doc.close()
    return sorted(blocks)


def find_set_ranges(blocks):
    headers = []
    for vy, x0, text, pi in blocks:
        m = re.match(r'^\[(\d+)～(\d+)\]', text)
        if m:
            headers.append((int(m.group(1)), int(m.group(2)), vy))
    return headers


def get_set_blocks(blocks, headers, qs, qe):
    start_vy = end_vy = None
    for i, (s, e, vy) in enumerate(headers):
        if s == qs and e == qe:
            start_vy = vy
            end_vy = headers[i + 1][2] if i + 1 < len(headers) else 999999
            break
    if start_vy is None:
        return []
    return [(vy, x0, t) for vy, x0, t, pi in blocks if start_vy <= vy < end_vy]


def _label_has_content(set_blocks, label_idx, is_left, min_chars=60):
    """레이블 이후 같은 컬럼에 충분한 텍스트가 있으면 True (이미지 레이블 제외용)"""
    chars = 0
    for vy, x0, text in set_blocks[label_idx + 1:]:
        t = text.strip()
        if t in ('(가)', '(나)', '(다)'):
            break
        if re.match(r'^\d+[.．]\s', text):
            break
        if (x0 < 430) == is_left:
            chars += len(text)
    return chars >= min_chars


def count_pdf_labels(set_blocks):
    """
    PDF 세트 블록에서 지문 레벨 (가)(나)(다) 라벨과 위치 반환.
    2컬럼 레이아웃에서는 각 컬럼 독립적으로 첫 문항 번호를 추적.
    레이블 뒤에 같은 컬럼에 실제 텍스트가 없으면 이미지 레이블로 간주해 제외.
    """
    labels = {}
    q_started_L = False
    q_started_R = False
    blocks_list = list(set_blocks)  # 인덱싱용
    for idx, (vy, x0, text) in enumerate(blocks_list):
        is_left = x0 < 430
        if re.match(r'^\d+[.．]\s', text):
            if is_left:
                q_started_L = True
            else:
                q_started_R = True
        lbl = text.strip()
        if lbl in ('(가)', '(나)', '(다)') and lbl not in labels:
            if not _label_has_content(blocks_list, idx, is_left):
                continue  # 레이블 뒤 텍스트 없음 → 이미지 전용
            if is_left and not q_started_L:
                labels[lbl] = 'LEFT'
            elif not is_left and not q_started_R:
                labels[lbl] = 'RIGHT'
    return labels


def pdf_passage_text(set_blocks):
    """PDF 지문 영역 텍스트 (문항 시작 전까지 + 보기 제외)"""
    parts = []
    for vy, x0, text in set_blocks:
        if re.match(r'^\d+[.．]\s', text):
            break
        if re.match(r'^[①②③④⑤]', text):
            break
        if re.match(r'^<보', text):
            continue
        if re.match(r'^\[(\d+)～(\d+)\]', text):
            continue
        if text.strip() in ('(가)', '(나)', '(다)'):
            continue
        parts.append(text)
    return ' '.join(parts)


def norm_text(t):
    return re.sub(r'\s+', ' ', t).strip()


def json_passage_text(passages):
    return norm_text(' '.join(
        p for passage in passages
        for p in passage.get('paragraphs', [])
    ))


def missing_words(pdf_text, json_text, min_len=4):
    """PDF에만 있는 한국어 단어 후보"""
    pdf_words = set(re.findall(rf'[가-힣]{{{min_len},}}', pdf_text))
    return sorted([w for w in pdf_words if w not in json_text])


def audit_set(json_set, set_blocks, sec_id):
    issues = []
    warnings = []

    # 1. PDF 라벨 수 vs JSON passages 수
    pdf_labels = count_pdf_labels(set_blocks)
    json_pcount = len(json_set.get('passages', []))
    expected    = len(pdf_labels)

    if expected > 0 and json_pcount != expected:
        issues.append(
            f"지문 수 불일치: PDF {expected}개 {list(pdf_labels)} → JSON {json_pcount}개"
        )
    elif expected == 0 and json_pcount == 0 and sec_id not in ('화법과작문', '언어와매체'):
        issues.append("PDF·JSON 모두 passages 없음 (비선택과목)")

    # 2. 지문 길이 비율
    pdf_text  = pdf_passage_text(set_blocks)
    json_text = json_passage_text(json_set.get('passages', []))
    pdf_len   = len(pdf_text)
    json_len  = len(json_text)

    if pdf_len > 100:
        ratio = json_len / pdf_len
        if ratio < RATIO_LO:
            issues.append(f"지문 길이 부족: JSON {json_len}자 / PDF {pdf_len}자 (비율 {ratio:.2f})")
        elif ratio > RATIO_HI:
            warnings.append(f"지문 길이 초과: JSON {json_len}자 / PDF {pdf_len}자 (비율 {ratio:.2f})")

    # 3. 누락 후보 단어
    missing = missing_words(pdf_text, json_text)
    if len(missing) >= MISSING_THRESHOLD:
        warnings.append(f"누락 후보 단어 {len(missing)}개: {missing[:6]}")

    return issues, warnings


def main():
    print("PDF 로드 중...")
    all_blocks = load_pdf_blocks()
    headers    = find_set_ranges(all_blocks)
    print(f"세트 헤더 {len(headers)}개 발견\n")

    data    = json.loads(JSON.read_text(encoding='utf-8'))
    sec_map = {sec['id']: {s['id']: s for s in sec['sets']}
               for sec in data['sections']}
    sec_of  = {sid: sec['id']
               for sec in data['sections']
               for sid, s in sec_map[sec['id']].items()}

    total_err = total_warn = 0

    for sec in data['sections']:
        print(f"{'='*60}")
        print(f"[{sec['id']}]")
        for s in sec['sets']:
            set_id  = s['id']
            sec_id  = sec['id']
            m = re.match(r'set-(\d+)-(\d+)', set_id)
            qs, qe  = int(m.group(1)), int(m.group(2))

            pdf_blocks = get_set_blocks(all_blocks, headers, qs, qe)
            issues, warnings = audit_set(s, pdf_blocks, sec_id)

            status = '✅' if not issues else '❌'
            pdf_lbls = count_pdf_labels(pdf_blocks)
            json_pc  = len(s.get('passages', []))
            tag = f"PDF{list(pdf_lbls) or '단일'}→JSON{json_pc}개"

            print(f"  {status} {set_id}  Q{qs}~{qe}  [{tag}]")
            for iss in issues:
                print(f"       ❌ {iss}")
                total_err += 1
            for wrn in warnings:
                print(f"       ⚠️  {wrn}")
                total_warn += 1

    print(f"\n{'='*60}")
    print(f"오류: {total_err}개  경고: {total_warn}개")
    if total_err == 0:
        print("✅ 모든 세트 지문 원문 대조 통과")
    else:
        print("❌ 지문 누락/불일치 세트 있음")


if __name__ == '__main__':
    main()
