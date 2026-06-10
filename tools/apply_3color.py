#!/usr/bin/env python3
# 기출 분석 파일을 2색(정답 녹/오답 파랑) → 3색으로 변환.
#   정답 근거 = 녹색(src-tag ans / ev ans)           그대로
#   지문 근거 = 파랑(맞는 진술)  : "부정형" 발문(적절하지 않은/일치하지 않는/반영되지 않은…)의 비정답 선지
#   오답 근거 = 빨강(틀린 진술)  : "긍정형" 발문(가장 적절한/일치하는…)의 비정답 선지  → class에 'wrong' 추가
# 정답(ans) 선지/배지/스팬은 건드리지 않음. recolor_evidence.py는 이 파일들에 돌리지 말 것(빨강이 사라짐).
import re, sys, glob

NEG = ["않은", "않는", "없는", "아닌", "어려운", "못한", "않다"]

def is_neg(stem_html):
    txt = re.sub(r'<[^>]+>', '', stem_html)
    return any(m in txt for m in NEG)

def process(path, apply):
    t = open(path, encoding='utf-8').read()

    # 1) 문항 번호 -> 발문 극성
    pol = {}
    for m in re.finditer(r'class="q-stem">\s*(\d+)\.(.*?)</p>', t, re.S):
        pol[int(m.group(1))] = 'neg' if is_neg(m.group(2)) else 'pos'

    # 1b) ev 스팬 -> 문항 번호 (따라오는 첫 배지 기준; <li> 밖 인라인 버튼 보정용)
    ev_q = {}
    for m in re.finditer(r'<span class="ev[^"]*" id="(ev[\w-]+)">.*?</span><a class="ev-tag[^"]*" href="#q(\d+)-', t, re.S):
        ev_q.setdefault(m.group(1), int(m.group(2)))

    # 2) 선지 id -> 유형 (ans / jimun / odab)
    ctype = {}
    for m in re.finditer(r'<li id="(q(\d+)-\d+)"[^>]*>(.*?)</li>', t, re.S):
        cid, n, body = m.group(1), int(m.group(2)), m.group(3)
        if 'class="src-tag ans"' in body:
            ctype[cid] = 'ans'
        elif 'class="src-tag"' in body:
            ctype[cid] = 'jimun' if pol.get(n) == 'neg' else 'odab'

    counts = {'jimun': 0, 'odab': 0, 'ans': 0, 'badge_wrong': 0, 'span_wrong': 0}

    # 3) 선지 버튼 변환 (li 단위)
    def repl_li(m):
        open_tag, cid, n, body, close = m.group(1), m.group(2), int(m.group(3)), m.group(4), m.group(5)
        ty = ctype.get(cid)
        if ty == 'jimun':
            # 라벨 '오답 근거'(+꼬리표) → '지문 근거'(+꼬리표), 클래스 유지(파랑)
            body, k = re.subn(r'(<a class="src-tag" href="#ev[\w-]+">)오답 근거([^<]*</a>)', r'\1지문 근거\2', body)
            counts['jimun'] += k
        elif ty == 'odab':
            # 클래스에 wrong 추가(빨강), 라벨 '오답 근거'(+꼬리표) 유지
            body, k = re.subn(r'<a class="src-tag" href="#(ev[\w-]+)">(오답 근거[^<]*)</a>',
                              r'<a class="src-tag wrong" href="#\1">\2</a>', body)
            counts['odab'] += k
        elif ty == 'ans':
            counts['ans'] += body.count('정답 근거')
        return f'{open_tag}{body}{close}'

    t = re.sub(r'(<li id="(q(\d+)-\d+)"[^>]*>)(.*?)(</li>)', repl_li, t, flags=re.S)

    # 3b) <li> 밖 인라인 선지(<b>①</b>) 버튼 보정: 스팬→문항 극성으로 분류
    def repl_btn_fb(m):
        evid, label = m.group(1), m.group(2)
        n = ev_q.get(evid)
        if n is None:
            return m.group(0)
        if pol.get(n) == 'pos':
            counts['odab'] += 1
            return f'<a class="src-tag wrong" href="#{evid}">{label}</a>'
        counts['jimun'] += 1
        return f'<a class="src-tag" href="#{evid}">{label.replace("오답 근거", "지문 근거", 1)}</a>'
    t = re.sub(r'<a class="src-tag" href="#(ev[\w-]+)">(오답 근거[^<]*)</a>', repl_btn_fb, t)

    # 4) 배지/스팬 색 (전역) — 겹침 우선순위: 정답(녹) > 지문(파랑) > 오답(빨강)
    # 4a) 비정답 배지(ev-tag)가 '긍정형' 문항을 가리키면 빨강. 초록·파랑 밑줄 위의 배지 모두 처리.
    #     (ev-tag ans 정답 배지는 건드리지 않음 → 정답 근거 우선)
    def badge_sub(m):
        n = int(m.group(1))
        if pol.get(n) == 'pos':
            counts['badge_wrong'] += 1
            return m.group(0).replace('class="ev-tag"', 'class="ev-tag wrong"', 1)
        return m.group(0)
    t = re.sub(r'<a class="ev-tag" href="#q(\d+)-\d+">[^<]*</a>', badge_sub, t)

    # 4b) 파란 스팬(ev): 가리키는 비정답 선지가 '전부 긍정형'일 때만 빨강.
    #     하나라도 부정형(지문 근거)이 겹치면 지문 우선 → 파랑 유지.
    #     초록 스팬(ev ans)은 정답 근거 우선이라 그대로 둠(이 정규식은 class="ev"만 매칭).
    def span_sub(m):
        span, badges = m.group(1), m.group(2)
        ns = [int(x) for x in re.findall(r'href="#q(\d+)-\d+"', badges)]
        pols = [pol[n] for n in ns if n in pol]
        if pols and all(p == 'pos' for p in pols):
            counts['span_wrong'] += 1
            return span.replace('class="ev"', 'class="ev wrong"', 1) + badges
        return m.group(0)
    t = re.sub(r'(<span class="ev" id="ev[\w-]+">.*?</span>)((?:<a class="ev-tag[^"]*" href="#q\d+-\d+">[^<]*</a>)+)',
               span_sub, t, flags=re.S)

    # 5) 범례 3색 — 형식 변형 모두 처리(긴 패턴 먼저)
    RED_B = '<b style="color:#c0392b;border-color:#c0392b">빨간 밑줄</b>'
    GREEN_B = '<b style="color:#1f7a3d;border-color:#1f7a3d">초록 밑줄</b>'
    legend_reps = [
        # (가) 초록 포함형 → 초록/파란(지문)/빨강(오답)
        ('<b style="color:#1f7a3d;border-color:#1f7a3d">초록 밑줄</b>은 정답 근거, <b>파란 밑줄</b>은 각 선지를 판단하는 오답 근거',
         f'{GREEN_B}은 정답 근거, <b>파란 밑줄</b>은 지문 근거(맞는 진술), {RED_B}은 오답 근거(틀린 진술)'),
        ('<b style="color:#1f7a3d;border-color:#1f7a3d">초록 밑줄</b>은 정답 근거, <b>파란 밑줄</b>은 오답 근거',
         f'{GREEN_B}은 정답 근거, <b>파란 밑줄</b>은 지문 근거(맞는 진술), {RED_B}은 오답 근거(틀린 진술)'),
        # (나) 초록 미포함형(2025/2026) → 초록 추가 + 파란(지문)/빨강(오답)
        ('<b>파란 밑줄</b>은 각 선지를 판단하는 오답 근거',
         f'{GREEN_B}은 정답 근거, <b>파란 밑줄</b>은 지문 근거(맞는 진술), {RED_B}은 오답 근거(틀린 진술)'),
        ('<b>파란 밑줄</b>은 오답 근거',
         f'{GREEN_B}은 정답 근거, <b>파란 밑줄</b>은 지문 근거(맞는 진술), {RED_B}은 오답 근거(틀린 진술)'),
    ]
    for old, new in legend_reps:
        t = t.replace(old, new)

    if apply:
        open(path, 'w', encoding='utf-8').write(t)

    pos_qs = sorted(n for n, p in pol.items() if p == 'pos')
    return counts, pos_qs, pol

if __name__ == '__main__':
    apply = '--apply' in sys.argv
    files = sorted(glob.glob('content/exams/2024/*go2*analysis.md') +
                   glob.glob('content/exams/2025/*go2*analysis.md') +
                   glob.glob('content/exams/2026/*go2*analysis.md'))
    for f in files:
        c, posqs, pol = process(f, apply)
        name = f.split('/')[-1]
        print(f"{name}: 지문(파랑) {c['jimun']} | 오답(빨강) {c['odab']} | 정답(녹) {c['ans']} | 빨강배지 {c['badge_wrong']} 빨강스팬 {c['span_wrong']}")
        print(f"   긍정형(빨강 대상) 문항: {posqs}")
    print("APPLY" if apply else "DRY-RUN (검토용)")
