#!/usr/bin/env python3
"""2025 수능 전체 JSON 재생성"""
import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from extract_all_sets import load_blocks, split_by_set, build_set, extract_questions

PDF  = Path('/home/lhj715/teacher-materials/kice/2025/수능/문제지.pdf')
OUT  = Path('/home/lhj715/korean-blog/data/exams/2025-수능.json')

# ── 정답표 ────────────────────────────────────────────────────
ANS_COMMON = {
    1:3, 2:4, 3:5,
    4:4, 5:5, 6:3, 7:2, 8:1, 9:2,
    10:3, 11:1, 12:5, 13:3,
    14:1, 15:2, 16:2, 17:3,
    18:2, 19:4, 20:1, 21:4,
    22:4, 23:5, 24:2, 25:2, 26:1, 27:1,
    28:4, 29:3, 30:5, 31:4,
    32:3, 33:5, 34:2,
}
ANS_HWA = {35:5, 36:4, 37:3, 38:4, 39:5, 40:4, 41:3, 42:5, 43:2, 44:1, 45:3}
ANS_ENM = {35:5, 36:4, 37:2, 38:4, 39:5, 40:4, 41:3, 42:5, 43:2, 44:1, 45:3}

# has_image: 선지가 이미지/표 안에 있어 텍스트 추출 불가
HAS_IMAGE_COMMON = {20}   # 문학 Q20 (표형 매칭)
HAS_IMAGE_HWA   = {39}   # 화작 Q39 (메모 표형)

def inject(q, ans_map):
    q['answer'] = ans_map.get(q['number'])


def postprocess_q20(q):
    """Q20 표형 매칭 문항: 질문 정리 + cells 파싱"""
    # 질문 텍스트에서 <학습 활동> 본문 제거
    stem = q['question']
    cut = stem.find('｢정을선전｣')
    if cut > 0:
        q['question'] = stem[:cut].strip()

    q['choice_format'] = 'table_matching'
    q['table_headers'] = ['인물A', '인물B', '소통의 내용']

    new_choices = []
    for c in q['choices']:
        raw = c['text'].strip()
        parts = raw.split()
        if len(parts) >= 3:
            cells = {
                '인물A': parts[0],
                '인물B': parts[1],
                '소통의 내용': ' '.join(parts[2:])
            }
        else:
            cells = {}
        new_choices.append({
            'no': c['no'],
            'text': raw,
            'cells': cells,
            'manual_verified': False
        })
    q['choices'] = new_choices

# ── 로드 ──────────────────────────────────────────────────────
blocks = load_blocks(str(PDF))
sets   = split_by_set(blocks)

# 전역 q_lookup (독서/문학용)
all_q   = extract_questions([(vy, x0, t) for vy, x0, t, pi, y0 in blocks])
q_lookup = {q['number']: q for q in all_q}

# ── 세트 ID → 섹션 매핑 ──────────────────────────────────────
# 세트 순서대로 번호 부여
# 독서 4개 / 문학 4개 / 화작 3개 / 언매 3개(+implicit)
SEC_MAP = [
    '독서', '독서', '독서', '독서',
    '문학', '문학', '문학', '문학',
    '화법과작문', '화법과작문', '화법과작문',
    '언어와매체', '언어와매체', '언어와매체',
]

section_data = {s: [] for s in ['독서', '문학', '화법과작문', '언어와매체']}

# ── 세트별 처리 ───────────────────────────────────────────────
for i, s in enumerate(sets):
    sec  = SEC_MAP[i]
    qr   = s['q_range']
    sid  = f"set-{qr[0]:02d}-{qr[1]:02d}"
    built = build_set(s, sid, q_lookup)

    # 정답 주입
    ans = ANS_HWA if sec == '화법과작문' else (ANS_ENM if sec == '언어와매체' else ANS_COMMON)
    for q in built['questions']:
        inject(q, ans)
        hi = HAS_IMAGE_COMMON.copy()
        if sec == '화법과작문':
            hi |= HAS_IMAGE_HWA
        if q['number'] in hi:
            q['has_image'] = True
        if q['number'] == 20 and sec == '문학':
            postprocess_q20(q)

    section_data[sec].append(built)

    # 언매 set-35-36: Q37-39 implicit set 추가
    if sec == '언어와매체' and qr == [35, 36]:
        extra_qs = extract_questions([(vy, x0, t) for vy, x0, t in s['blocks']])
        orphan = sorted([q for q in extra_qs if 37 <= q['number'] <= 39],
                        key=lambda q: q['number'])
        if orphan:
            for q in orphan:
                inject(q, ANS_ENM)
                if q['number'] in HAS_IMAGE_COMMON:
                    q['has_image'] = True
            implicit = dict(
                id='set-37-39', q_range=[37, 39],
                type='언어와매체', topic='', field='',
                passages=[], questions=orphan
            )
            section_data['언어와매체'].append(implicit)

# ── 최종 JSON 조립 ────────────────────────────────────────────
output = {
    "meta": {
        "id": "2025-수능",
        "year": 2025,
        "exam_type": "수능",
        "grade": 3,
        "month": 11,
        "subject": "국어",
        "form": "공통+선택",
        "source": "한국교육과정평가원",
        "total_questions": 45,
        "elective": True
    },
    "sections": [
        {
            "id": "독서",
            "label": "독서",
            "sets": section_data['독서']
        },
        {
            "id": "문학",
            "label": "문학",
            "sets": section_data['문학']
        },
        {
            "id": "화법과작문",
            "label": "화법과작문 (선택)",
            "sets": section_data['화법과작문']
        },
        {
            "id": "언어와매체",
            "label": "언어와매체 (선택)",
            "sets": section_data['언어와매체']
        },
    ]
}

OUT.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding='utf-8')
print(f"✅ 저장: {OUT}")

# ── 요약 출력 ─────────────────────────────────────────────────
for sec in output['sections']:
    print(f"\n[{sec['id']}]")
    for s in sec['sets']:
        qs = [q['number'] for q in s['questions']]
        print(f"  {s['id']}  Q{qs}")
