"""4~6번 초안 만들기(도구/세트_뽑기.py 를 고치지 않고 감싼 것).

세트_뽑기.py 는 문항 블록에서 ①~⑤ 로 시작하는 줄을 찾아 선지를 나누는데, 5번은 선지 번호가
쟁점 정리 상자 항목 끝(점선 뒤)에 붙어 있어 ① 로 시작하는 줄이 하나도 없다 → IndexError.
그래서 같은 함수(page_lines, join)를 쓰되, 선지 줄이 없는 문항은 블록 전체를 발문으로 두고
choices 를 빈 목록으로 남긴다(세트_4-6_만들기.py 에서 상자·선지로 나눈다).
"""
import json
import os
import re
import sys

import fitz

ROOT = r"D:\Work\블로그\리딩맵"
sys.path.insert(0, os.path.join(ROOT, "도구"))
import importlib.util

spec = importlib.util.spec_from_file_location("ppb", os.path.join(ROOT, "도구", "세트_뽑기.py"))
ppb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ppb)

pdf = os.path.join(ROOT, r"원본자료\ebsi-korean\pdf\20260324-go1-problem-kor_mun_16FRAZ68.pdf")
starts_file = os.path.join(ROOT, r"작업\20260324-go1\문단시작_4-6.txt")
out_path = os.path.join(ROOT, r"작업\20260324-go1\초안_4-6.json")
start, end = 4, 6

lines = ppb.page_lines(fitz.open(pdf))
gi = next(i for i, l in enumerate(lines) if re.match(rf"^\[{start}\s*[~～]\s*{end}\]", l.strip()))
q_re = lambda n: re.compile(rf"^{n}\.\s")
qi = {n: next(i for i, l in enumerate(lines) if i > gi and q_re(n).match(l)) for n in range(start, end + 1)}
nxt = next((i for i, l in enumerate(lines) if i > qi[end] and re.match(r"^\[\d+\s*[~～]\s*\d+\]", l.strip())), len(lines))

starts = [s.strip("\n") for s in open(starts_file, encoding="utf-8") if s.strip()]
paras, cur = [], None
for l in lines[gi + 1: qi[start]]:
    hit = next((s for s in starts if l.startswith(s)), None)
    if hit:
        if cur:
            paras.append(cur)
        cur = [l]
    elif cur is not None:
        cur.append(l)
if cur:
    paras.append(cur)
passage = [{"id": f"p{k}", "type": "para", "text": ppb.join(p), "underlines": []} for k, p in enumerate(paras, 1)]

questions = []
for n in range(start, end + 1):
    block = lines[qi[n]: (qi[n + 1] if n < end else nxt)]
    idx = [i for i, l in enumerate(block) if l[:1] and l[:1] in ppb.CIRCLED]
    stem = re.sub(rf"^{n}\.\s*", "", ppb.join(block[: idx[0]] if idx else block))
    choices = [ppb.join(block[i: (idx[j + 1] if j + 1 < len(idx) else len(block))])[1:].strip() for j, i in enumerate(idx)]
    questions.append({"no": n, "points": 3 if "[3점]" in stem else 2, "stem": stem, "bogi": None,
                      "choices": choices, "answer": None, "judgments": []})

json.dump({"guide": lines[gi].strip(), "range": [start, end], "passage": passage, "questions": questions},
          open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("passage", len(passage), "questions", len(questions))
