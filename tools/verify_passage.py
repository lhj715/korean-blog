#!/usr/bin/env python3
"""
리딩맵 지문 검증기 v2 — 블록 좌표 기반 문단 복원 후 JSON과 비교
사용법: python3 verify_passage.py <pdf파일> <json파일> <set_id>
"""

import sys, json, re, difflib
from pathlib import Path

try:
    import fitz
except ImportError:
    print("pip install pymupdf"); sys.exit(1)


# ── 텍스트 정규화 ──────────────────────────────────────
def normalize(text: str) -> str:
    """줄간 공백, 어절 사이 불필요 공백 제거"""
    text = re.sub(r'\s+', ' ', text).strip()
    # 행 끝 공백으로 분리된 어절 복원 (예: "전략 이다" → "전략이다")
    # 조사·어미로 시작하는 토큰 앞 공백 제거
    text = re.sub(r' (이다|이며|이고|이나|이라|이어|이지|이든|이든지)', r'\1', text)
    return text


# ── pymupdf 블록 기반 문단 추출 ────────────────────────
def extract_paragraphs_from_page(page, x_max=420, y_min=220, indent_x=107, tol=6):
    """
    x0 ≈ indent_x 이면 문단 첫 줄(들여쓰기).
    질문 번호(숫자.)가 나오면 지문 끝으로 간주.
    """
    blocks = page.get_text('blocks')
    lines = []
    for b in blocks:
        x0, y0, x1, y1, text = b[0], b[1], b[2], b[3], b[4]
        if x0 > x_max or y0 < y_min:
            continue
        text = text.replace('\n', ' ').strip()
        if not text:
            continue
        lines.append((y0, x0, text))

    lines.sort(key=lambda t: t[0])

    paragraphs = []
    current = []
    for y0, x0, text in lines:
        if re.match(r'^\d+[.．]', text):   # 문항 번호 시작 → 지문 끝
            break
        if re.match(r'^[①②③④⑤]', text):  # 선지 시작 → 지문 끝
            break
        is_indent = abs(x0 - indent_x) <= tol
        if is_indent and current:
            paragraphs.append(normalize(' '.join(current)))
            current = [text]
        else:
            current.append(text)
    if current:
        paragraphs.append(normalize(' '.join(current)))

    # 세트 헤더([1~3] ...) 제거
    paragraphs = [p for p in paragraphs if not re.match(r'^\[', p)]
    return paragraphs


def similarity(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, a, b).ratio()


def char_diff(a: str, b: str, context=15) -> list:
    """글자 단위 차이점 추출"""
    matcher = difflib.SequenceMatcher(None, a, b)
    diffs = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            continue
        ctx_a = a[max(0,i1-context):i2+context]
        ctx_b = b[max(0,j1-context):j2+context]
        diffs.append({
            'type': tag,
            'pdf': f'...{ctx_a}...',
            'json': f'...{ctx_b}...'
        })
    return diffs[:10]   # 최대 10개


# ── 메인 검증 ──────────────────────────────────────────
def verify(pdf_path: str, json_path: str, set_id: str):
    data = json.loads(Path(json_path).read_text(encoding='utf-8'))
    target_set = None
    for sec in data.get('sections', []):
        for s in sec.get('sets', []):
            if s['id'] == set_id:
                target_set = s; break

    if not target_set:
        print(f"❌ set_id '{set_id}' 없음"); sys.exit(1)

    doc = fitz.open(pdf_path)
    total_pages = len(doc)

    print(f"\n{'='*55}")
    print(f"세트: {set_id}")
    print(f"{'='*55}")

    for passage in target_set.get('passages', []):
        pid = passage.get('id') or '단일'
        json_paras = passage.get('paragraphs', [])

        print(f"\n▶ 지문 [{pid}]")

        # PDF 전체 문단 합치기 (복수 페이지 대응)
        pdf_paras = []
        for pg_idx in range(min(3, total_pages)):
            pdf_paras += extract_paragraphs_from_page(doc[pg_idx])

        # ── 1. 문단 수 비교 ────────────────────────────
        print(f"\n  [문단 수]")
        print(f"  JSON : {len(json_paras)}개")
        print(f"  PDF  : {len(pdf_paras)}개  {'✅' if len(json_paras) == len(pdf_paras) else '⚠️  불일치'}")

        # ── 2. 문단별 유사도 ───────────────────────────
        print(f"\n  [문단별 유사도]")
        all_pass = True
        for i, (jp, pp) in enumerate(zip(json_paras, pdf_paras), 1):
            sim = similarity(jp, pp)
            icon = '✅' if sim >= 0.97 else ('⚠️ ' if sim >= 0.90 else '❌')
            print(f"  {i}문단 {icon} {sim*100:.1f}%")
            if sim < 0.97:
                all_pass = False
                diffs = char_diff(pp, jp)
                for d in diffs[:3]:
                    print(f"       [{d['type']}]")
                    print(f"       PDF : {d['pdf']}")
                    print(f"       JSON: {d['json']}")

        # ── 3. JSON에만 있고 PDF에 없는 문단 ──────────
        if len(json_paras) > len(pdf_paras):
            print(f"\n  ❌ JSON 문단 {len(json_paras)-len(pdf_paras)}개가 PDF에서 추출 안 됨")
            for jp in json_paras[len(pdf_paras):]:
                print(f"     → {jp[:50]}...")

        # ── 4. 최종 판정 ───────────────────────────────
        print(f"\n  {'✅ 검증 통과' if all_pass and len(json_paras)==len(pdf_paras) else '⚠️  검수 필요'}")

    doc.close()
    print(f"\n{'='*55}\n")


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("사용법: python3 verify_passage.py <pdf> <json> <set_id>")
        sys.exit(1)
    verify(sys.argv[1], sys.argv[2], sys.argv[3])
