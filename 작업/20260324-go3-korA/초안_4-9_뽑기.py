"""4~9번 초안 만들기(도구/세트_뽑기.py 를 고치지 않고 감싼 것).

세트_뽑기.py 는 줄 맨 앞이 «8.» 이어야 문항 시작으로 보는데, 8번 줄은 PDF 에서 전각 공백(U+3000)으로 시작한다
→ IndexError(StopIteration). 그래서 같은 함수(page_lines, join)를 쓰되 줄 앞 전각 공백만 떼고 뽑는다.
"""
import importlib.util
import json
import os
import re

import fitz

ROOT = r"D:\Work\블로그\리딩맵"
spec = importlib.util.spec_from_file_location("ppb", os.path.join(ROOT, "도구", "세트_뽑기.py"))
ppb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ppb)

pdf = os.path.join(ROOT, r"원본자료\ebsi-korean\pdf\20260324-go3-problem-korA_mun_95U73553.pdf")
starts_file = os.path.join(ROOT, r"작업\20260324-go3-korA\문단시작_4-9.txt")
out_path = os.path.join(ROOT, r"작업\20260324-go3-korA\초안_4-9.json")
start, end = 4, 9

lines = [l.lstrip("\u3000") for l in ppb.page_lines(fitz.open(pdf))]
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
