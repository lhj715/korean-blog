#!/usr/bin/env python3
"""
2024 수능 전체 JSON 재생성
특이사항: PDF가 40페이지 합본(화작버전+언매버전)
         → split_by_set()[:14] 상반부만 사용
"""
import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from extract_all_sets import load_blocks, split_by_set, build_set, extract_questions

PDF = Path('/home/lhj715/teacher-materials/kice/2024/수능/문제지.pdf')
OUT = Path('/home/lhj715/korean-blog/data/exams/2024-수능.json')

# ── 정답표 (홀수형) ───────────────────────────────────────────
ANS_COMMON = {
    1:5, 2:3, 3:1,
    4:5, 5:3, 6:2, 7:2,
    8:3, 9:1, 10:5, 11:2,
    12:3, 13:1, 14:4, 15:4, 16:5, 17:4,
    18:2, 19:1, 20:3, 21:5,
    22:2, 23:1, 24:3, 25:3, 26:2, 27:5,
    28:1, 29:4, 30:1, 31:2,
    32:2, 33:3, 34:4,
}
ANS_HWA = {35:4, 36:5, 37:4, 38:4, 39:5, 40:1, 41:3, 42:3, 43:2, 44:5, 45:1}
ANS_ENM = {35:4, 36:4, 37:1, 38:3, 39:4, 40:2, 41:1, 42:5, 43:3, 44:3, 45:5}

# ── 섹션 매핑 (상반부 14세트 순서) ───────────────────────────
# Q1~3, Q4~7, Q8~11, Q12~17 → 독서
# Q18~21, Q22~27, Q28~31, Q32~34 → 문학
# Q35~37, Q38~42, Q43~45 → 화작
# Q35~36, Q40~43, Q44~45 → 언매
SEC_MAP = [
    '독서', '독서', '독서', '독서',
    '문학', '문학', '문학', '문학',
    '화법과작문', '화법과작문', '화법과작문',
    '언어와매체', '언어와매체', '언어와매체',
]

def inject(q, ans_map):
    q['answer'] = ans_map.get(q['number'])


# ── 로드 (40페이지 합본 → 상반부 14세트만) ───────────────────
blocks = load_blocks(str(PDF))
all_sets = split_by_set(blocks)
sets = all_sets[:14]  # 화작 합본 기준 상반부만 (언매 14세트 이후는 중복)

# 전역 q_lookup (공통 독서/문학용)
all_q   = extract_questions([(vy, x0, t) for vy, x0, t, pi, y0 in blocks
                              if pi < 20])   # 상반부 페이지만
q_lookup = {q['number']: q for q in all_q}

section_data = {s: [] for s in ['독서', '문학', '화법과작문', '언어와매체']}

for i, s in enumerate(sets):
    sec = SEC_MAP[i]
    qr  = s['q_range']
    sid = f"set-{qr[0]:02d}-{qr[1]:02d}"
    built = build_set(s, sid, q_lookup)

    ans = ANS_HWA if sec == '화법과작문' else (ANS_ENM if sec == '언어와매체' else ANS_COMMON)
    for q in built['questions']:
        inject(q, ans)

    section_data[sec].append(built)

    # 언매 set-35-36: Q37~39 implicit set 추가
    if sec == '언어와매체' and qr == [35, 36]:
        extra_qs = extract_questions([(vy, x0, t) for vy, x0, t in s['blocks']])
        orphan = sorted([q for q in extra_qs if 37 <= q['number'] <= 39],
                        key=lambda q: q['number'])
        if orphan:
            for q in orphan:
                inject(q, ANS_ENM)
            implicit = dict(
                id='set-37-39', q_range=[37, 39],
                type='언어와매체', topic='', field='',
                passages=[], questions=orphan
            )
            section_data['언어와매체'].append(implicit)

# ── 최종 JSON 조립 ────────────────────────────────────────────
output = {
    "meta": {
        "id": "2024-수능",
        "year": 2024,
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
        {"id": "독서",       "label": "독서",           "sets": section_data['독서']},
        {"id": "문학",       "label": "문학",           "sets": section_data['문학']},
        {"id": "화법과작문", "label": "화법과작문 (선택)", "sets": section_data['화법과작문']},
        {"id": "언어와매체", "label": "언어와매체 (선택)", "sets": section_data['언어와매체']},
    ]
}

OUT.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding='utf-8')
print(f"✅ 저장: {OUT}")

for sec in output['sections']:
    print(f"\n[{sec['id']}]")
    for s in sec['sets']:
        qs = [q['number'] for q in s['questions']]
        np = len(s.get('passages', []))
        print(f"  {s['id']}  passages={np}  Q{qs}")
