"""새 회차 작업 준비: 작업 폴더·글자 덤프·쪽 그림·작업/검토 지시서·세트 경계를 한 번에 만든다.

사용: py -X utf8 도구/회차_준비.py <날짜>-<go1|go2|go3>      예) 20250903-go1, 20250710-go3
  go1·go2 → 작업\<날짜>-go1\ 한 곳.
  go3     → 작업\<날짜>-go3-korA\ (공통 1~34 + 화법과 작문 35~45), 작업\<날짜>-go3-korB\ (언어와 매체 35~45).
문제지가 홀수형(`_1_`)·짝수형(`_2_`) 둘이면 홀수형만 쓴다.
정답 bundle 이 없으면 알려 준다(공식 정답표 PDF 가 있으면 `도구/정답묶음_만들기.py` 로 만든다).
"""
import glob
import json
import os
import re
import sys

import fitz

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF = os.path.join(ROOT, "원본자료", "ebsi-korean", "pdf")
BUNDLES = os.path.join(ROOT, "원본자료", "ebsi-korean", "site-ready-dataset", "bundles")
GUIDE = re.compile(r"^\s*\[\s*(\d+)\s*[~～∼]\s*(\d+)\s*\]")


def pick(pattern):
    fs = sorted(f for f in glob.glob(os.path.join(PDF, pattern)) if "_2_" not in os.path.basename(f))
    return fs[0] if fs else None


def sets_of(txt_path, lo, hi):
    """문제 글자 덤프에서 안내문 [a~b] 와 안내문 없는 단독 문항 묶음의 범위를 찾는다."""
    lines = open(txt_path, encoding="utf-8").read().split("\n")
    guides = {}
    for l in lines:
        m = GUIDE.match(l)
        if m:
            a, b = int(m.group(1)), int(m.group(2))
            if lo <= a <= b <= hi and a not in guides:
                guides[a] = b
    covered = set()
    for a, b in guides.items():
        covered.update(range(a, b + 1))
    rng = [(a, b) for a, b in guides.items()]
    run = []
    for n in list(range(lo, hi + 1)) + [None]:
        if n is not None and n not in covered:
            run.append(n)
        elif run:
            rng.append((run[0], run[-1]))
            run = []
    return sorted(rng)


def render(prob, expl, folder):
    os.makedirs(folder, exist_ok=True)
    os.makedirs(os.path.join(folder, "_임시"), exist_ok=True)
    for src, name in ((prob, "문제"), (expl, "해설")):
        d = fitz.open(src)
        out = [f"=== {name} {i}쪽 ===\n" + pg.get_text() for i, pg in enumerate(d, 1)]
        open(os.path.join(folder, f"{name}_글자.txt"), "w", encoding="utf-8").write("\n".join(out))
    d = fitz.open(prob)
    for i, pg in enumerate(d, 1):
        r = pg.rect
        pg.get_pixmap(dpi=150).save(os.path.join(folder, f"문제_{i}쪽.png"))
        half = r.width / 2
        pg.get_pixmap(dpi=150, clip=fitz.Rect(0, 0, half, r.height)).save(os.path.join(folder, f"문제_{i}쪽_왼쪽.png"))
        pg.get_pixmap(dpi=150, clip=fitz.Rect(half, 0, r.width, r.height)).save(os.path.join(folder, f"문제_{i}쪽_오른쪽.png"))
    return len(d), d[0].rect


def briefs(folder, exam_id, prob, expl, bundle, kind):
    tpl = os.path.join(ROOT, "도구", "템플릿")
    rep = {"{EXAM}": exam_id, "{FOLDER}": folder, "{PROB}": prob, "{EXPL}": expl, "{BUNDLE}": bundle, "{KIND}": kind}
    for name in ("작업지시", "검토지시"):
        t = open(os.path.join(tpl, name + ".md"), encoding="utf-8").read()
        for k, v in rep.items():
            t = t.replace(k, v)
        open(os.path.join(folder, f"_{name}.md"), "w", encoding="utf-8").write(t)


def main(unit):
    m = re.fullmatch(r"(\d{8})-(go[123])", unit)
    if not m:
        sys.exit("형식: 20250903-go1 또는 20250710-go3")
    date, g = m.groups()
    jobs = []
    if g == "go3":
        for opt in ("korA", "korB"):
            jobs.append((f"{date}-go3-{opt}", pick(f"{date}-go3-problem-{opt}*mun*.pdf"), pick(f"{date}-go3-explanation-{opt}*hsj*.pdf"),
                         (1, 45) if opt == "korA" else (35, 45), "선택 화법과 작문" if opt == "korA" else "선택 언어와 매체"))
    else:
        jobs.append((f"{date}-{g}", pick(f"{date}-{g}-problem-kor_mun*.pdf"), pick(f"{date}-{g}-explanation-kor_hsj*.pdf"), (1, 45), g))
    for exam_id, prob, expl, (lo, hi), kind in jobs:
        bundle = os.path.join(BUNDLES, exam_id + ".json")
        if not (prob and expl):
            print(f"[{exam_id}] 문제/해설 PDF 를 찾지 못함: {prob} / {expl}")
            continue
        folder = os.path.join(ROOT, "작업", exam_id)
        n, size = render(prob, expl, folder)
        briefs(folder, exam_id, prob, expl, bundle, kind)
        print(f"[{exam_id}] 폴더 {folder}\n  문제 {os.path.basename(prob)} ({n}쪽 {size})\n  해설 {os.path.basename(expl)}\n  bundle {'있음' if os.path.exists(bundle) else '없음 ← 정답표부터 만들어야 함'}")
        sets = sets_of(os.path.join(folder, "문제_글자.txt"), lo, hi)
        print("  세트 범위:", ", ".join(f"{a}-{b}" for a, b in sets))
        got = {n for a, b in sets for n in range(a, b + 1)}
        miss = [n for n in range(lo, hi + 1) if n not in got]
        if miss:
            print("  ! 범위에 안 잡힌 문항:", miss)


if __name__ == "__main__":
    main(sys.argv[1])
