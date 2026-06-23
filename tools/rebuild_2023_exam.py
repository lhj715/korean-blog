#!/usr/bin/env python3
"""
2023 수능 전체 JSON 재생성
특이사항: PDF 40페이지 합본 → split_by_set()[:14] 상반부만 사용
세트 차이: 문학 [22~26][27~30] (2025는 [22~27][28~31])
"""
import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from extract_all_sets import load_blocks, split_by_set, build_set, extract_questions

PDF = Path('/home/lhj715/teacher-materials/kice/2023/수능/문제지.pdf')
OUT = Path('/home/lhj715/korean-blog/data/exams/2023-수능.json')

# ── 정답표 (홀수형) ───────────────────────────────────────────
ANS_COMMON = {
    1:4, 2:5, 3:1,
    4:4, 5:5, 6:3, 7:2, 8:5, 9:2,
    10:4, 11:5, 12:2, 13:5,
    14:3, 15:4, 16:4, 17:1,
    18:4, 19:3, 20:3, 21:5,
    22:1, 23:5, 24:3, 25:3, 26:4,
    27:1, 28:5, 29:1, 30:2,
    31:1, 32:4, 33:2, 34:3,
}
ANS_HWA = {35:1, 36:5, 37:3, 38:4, 39:4, 40:3, 41:2, 42:4, 43:5, 44:2, 45:1}
ANS_ENM = {35:2, 36:4, 37:1, 38:4, 39:1, 40:2, 41:1, 42:3, 43:5, 44:4, 45:3}

# ── 섹션 매핑 (상반부 14세트 순서) ───────────────────────────
# 독서: [1~3][4~9][10~13][14~17]
# 문학: [18~21][22~26][27~30][31~34]
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
blocks = load_blocks(str(PDF))
all_sets = split_by_set(blocks)
sets = all_sets[:14]

all_q = extract_questions([(vy, x0, t) for vy, x0, t, pi, y0 in blocks if pi < 20])
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

    # ── 2023 전용 예외 처리 ────────────────────────────────────
    # set-40-43: (가)=이미지(누리집 화면), (나)=화상 회의 텍스트
    # extract_all_sets가 (가) RIGHT 이미지 레이블 뒤 LEFT 화상 회의 텍스트를 (가)로 오추출 → (가) 지문 제거
    if sec == '언어와매체' and qr == [40, 43]:
        built['passages'] = [p for p in built.get('passages', []) if p.get('label') != '(가)']

    # 화작 set-38-42 Q41: 선지가 이미지형(p15 y=761~1043 이미지)으로 텍스트 추출 불가
    if sec == '화법과작문' and qr == [38, 42]:
        for q in built['questions']:
            if q.get('number') == 41 and not q.get('choices'):
                q['processing_method'] = 'cropped_ocr_required'

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
        "id": "2023-수능",
        "year": 2023,
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
