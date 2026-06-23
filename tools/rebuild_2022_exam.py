#!/usr/bin/env python3
"""
2022 수능 전체 JSON 재생성
특이사항: 20p 단일 PDF (합본 아님) → split_by_set() 전체 14세트 사용
세트 차이: 문학 [18~23][24~27][28~31][32~34] (2023/2025와 크기 다름)
           헤더 위치: 독서 [14~17] RIGHT, 문학 [18~23][24~27][28~31] RIGHT
정답: TODO — 공식 정답 확인 후 채울 것 (현재 None → validate 경고)
"""
import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from extract_all_sets import load_blocks, split_by_set, build_set, extract_questions

PDF = Path('/home/lhj715/teacher-materials/kice/2022/수능/문제지.pdf')
OUT = Path('/home/lhj715/korean-blog/data/exams/2022-수능.json')

# ── 정답표 (홀수형) — TODO: 공식 정답 확인 후 채울 것 ─────────
ANS_COMMON = {}
ANS_HWA    = {}
ANS_ENM    = {}

# ── 섹션 매핑 (14세트 순서) ──────────────────────────────────
# 독서: [1~3][4~9][10~13][14~17]
# 문학: [18~23][24~27][28~31][32~34]
# 화작: [35~37][38~42][43~45]
# 언매: [35~36][40~43][44~45]
SEC_MAP = [
    '독서', '독서', '독서', '독서',
    '문학', '문학', '문학', '문학',
    '화법과작문', '화법과작문', '화법과작문',
    '언어와매체', '언어와매체', '언어와매체',
]


def inject(q, ans_map):
    q['answer'] = ans_map.get(q['number'])


# ── 로드 ──────────────────────────────────────────────────────
blocks  = load_blocks(str(PDF))
all_sets = split_by_set(blocks)
sets    = all_sets  # 20p 단일 PDF → 슬라이스 불필요

all_q   = extract_questions([(vy, x0, t) for vy, x0, t, pi, y0 in blocks])
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

    # 언매 set-35-36: Q37~39 implicit set
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
        "id": "2022-수능",
        "year": 2022,
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
        {"id": "독서",       "label": "독서",            "sets": section_data['독서']},
        {"id": "문학",       "label": "문학",            "sets": section_data['문학']},
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
