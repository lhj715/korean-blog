#!/usr/bin/env python3
"""
2025 수능 PDF vs JSON 샘플 대조기
사용법: python3 sample_compare.py
출력: 세트별 지문·선지 텍스트 차이 보고
"""
import json, re, sys
from pathlib import Path

import fitz

PDF  = Path('/home/lhj715/teacher-materials/kice/2025/수능/문제지.pdf')
JSON = Path('/home/lhj715/korean-blog/data/exams/2025-수능.json')
PAGE_H = 2000
COL_OFF = 9

# ── 검사할 세트 (독서2 문학2 화작1 언매1)
TARGETS = [
    ('독서',       'set-04-09'),
    ('독서',       'set-14-17'),
    ('문학',       'set-22-27'),
    ('문학',       'set-28-31'),
    ('화법과작문', 'set-38-42'),
    ('언어와매체', 'set-40-43'),
]


# ── PDF 원문 블록 로드 (y0 필터 동일하게 적용) ───────────────
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
            blocks.append((vy, x0, text, pi, y0))
    doc.close()
    return sorted(blocks)


# ── 세트 헤더 위치 파악 ────────────────────────────────────────
def find_set_ranges(blocks):
    headers = []
    for vy, x0, text, pi, y0 in blocks:
        m = re.match(r'^\[(\d+)～(\d+)\]', text)
        if m:
            headers.append((int(m.group(1)), int(m.group(2)), vy))
    return headers  # [(qs, qe, vy), ...]


def get_set_blocks(blocks, headers, qs, qe):
    """해당 세트의 vy 범위 블록 반환"""
    start_vy = None
    end_vy   = None
    for i, (s, e, vy) in enumerate(headers):
        if s == qs and e == qe:
            start_vy = vy
            end_vy = headers[i + 1][2] if i + 1 < len(headers) else 999999
            break
    if start_vy is None:
        return []
    return [(vy, x0, t) for vy, x0, t, pi, y0 in blocks
            if start_vy <= vy < end_vy]


# ── 텍스트 정규화 (비교용) ────────────────────────────────────
def norm(t):
    t = re.sub(r'\s+', ' ', t).strip()
    return t


# ── 지문 대조 ─────────────────────────────────────────────────
def compare_passages(json_passages, pdf_set_blocks):
    issues = []
    # JSON 지문 전체 텍스트 합산
    json_text = norm(' '.join(
        p for passage in json_passages for p in passage.get('paragraphs', [])
    ))

    # PDF 블록 중 지문 영역 텍스트 (세트 헤더 이후, 첫 문항 번호 이전)
    pdf_passage_parts = []
    for vy, x0, text in pdf_set_blocks:
        if re.match(r'^\d+[.．]', text):
            break
        if re.match(r'^\[', text) or re.match(r'^[①-⑤]', text):
            continue
        pdf_passage_parts.append(text)
    pdf_text = norm(' '.join(pdf_passage_parts))

    if not json_text and not pdf_text:
        return issues

    # 길이 비율
    ratio = len(json_text) / max(len(pdf_text), 1)
    if ratio < 0.85:
        issues.append(f"지문 길이 부족: JSON {len(json_text)}자 / PDF {len(pdf_text)}자 (ratio={ratio:.2f})")
    elif ratio > 1.15:
        issues.append(f"지문 길이 초과: JSON {len(json_text)}자 / PDF {len(pdf_text)}자 (ratio={ratio:.2f})")

    # 3글자 이상 PDF 단어가 JSON에 없으면 누락 후보
    pdf_words = set(re.findall(r'[가-힣]{4,}', pdf_text))
    missing = [w for w in pdf_words if w not in json_text]
    if missing:
        issues.append(f"지문 누락 단어 후보: {missing[:8]}")

    return issues


# ── 선지 대조 ─────────────────────────────────────────────────
def compare_choices(json_questions, pdf_set_blocks):
    issues = []

    # PDF에서 문항·선지 블록 수집
    pdf_q = {}   # {num: {'text': str, 'choices': {no: str}}}
    cur_num = None
    cur_c   = None
    for vy, x0, text in pdf_set_blocks:
        m = re.match(r'^(\d+)[.．]\s+(.*)', text)
        if m:
            cur_num = int(m.group(1))
            pdf_q.setdefault(cur_num, {'text': m.group(2).strip(), 'choices': {}})
            cur_c = None
            continue
        if cur_num is None:
            continue
        mc = re.match(r'^([①②③④⑤])(.*)', text)
        if mc:
            no = {'①':1,'②':2,'③':3,'④':4,'⑤':5}[mc.group(1)]
            cur_c = no
            pdf_q[cur_num]['choices'][no] = mc.group(2).strip()
            continue
        if cur_c and cur_num:
            existing = pdf_q[cur_num]['choices'].get(cur_c, '')
            # <보기>에서처럼 참조구가 이어질 때
            pdf_q[cur_num]['choices'][cur_c] = (existing + ' ' + text).strip()

    # JSON 문항과 대조
    for jq in json_questions:
        num = jq['number']
        pq  = pdf_q.get(num)
        if not pq:
            issues.append(f"Q{num:02d}: PDF에서 문항 블록 못 찾음")
            continue

        for jc in jq.get('choices', []):
            no = jc['no']
            jtext = norm(jc.get('text', ''))
            ptext = norm(pq['choices'].get(no, ''))
            if not ptext:
                continue  # PDF 선지 추출 안 된 경우 (이미지형 등)
            if not jtext:
                issues.append(f"Q{num:02d}-{no}: JSON 선지 비어 있음")
                continue

            # 핵심 단어 일치 확인
            p_words = set(re.findall(r'[가-힣]{3,}', ptext))
            j_words = set(re.findall(r'[가-힣]{3,}', jtext))
            only_pdf = p_words - j_words
            only_json = j_words - p_words
            if len(only_pdf) >= 3:
                issues.append(
                    f"Q{num:02d}-{no}: PDF에만 있는 단어 {list(only_pdf)[:4]}\n"
                    f"  JSON: {jtext[:60]}\n"
                    f"  PDF:  {ptext[:60]}"
                )

    return issues


# ── 메인 ──────────────────────────────────────────────────────
def main():
    print("PDF 로드 중...")
    all_blocks = load_pdf_blocks()
    headers    = find_set_ranges(all_blocks)
    print(f"세트 헤더 {len(headers)}개 발견\n")

    data = json.loads(JSON.read_text(encoding='utf-8'))
    sec_map = {sec['id']: {s['id']: s for s in sec['sets']}
               for sec in data['sections']}

    total_issues = 0

    for sec_id, set_id in TARGETS:
        m = re.match(r'set-(\d+)-(\d+)', set_id)
        qs, qe = int(m.group(1)), int(m.group(2))

        json_set = sec_map.get(sec_id, {}).get(set_id)
        if not json_set:
            print(f"[SKIP] {sec_id} {set_id} — JSON에 없음")
            continue

        pdf_blocks = get_set_blocks(all_blocks, headers, qs, qe)
        if not pdf_blocks:
            print(f"[SKIP] {sec_id} {set_id} Q{qs}~{qe} — PDF 블록 없음")
            continue

        print(f"{'='*60}")
        print(f"[{sec_id}] {set_id}  Q{qs}~{qe}  (PDF 블록 {len(pdf_blocks)}개)")

        issues = []
        issues += compare_passages(json_set.get('passages', []), pdf_blocks)
        issues += compare_choices(json_set.get('questions', []), pdf_blocks)

        if issues:
            total_issues += len(issues)
            for iss in issues:
                print(f"  ⚠️  {iss}")
        else:
            print(f"  ✅ 이상 없음")
        print()

    print(f"{'='*60}")
    print(f"총 발견 이슈: {total_issues}개")


if __name__ == '__main__':
    main()
