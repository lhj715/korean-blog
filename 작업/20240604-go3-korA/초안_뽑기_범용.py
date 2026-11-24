"""번호 뒤에 줄바꿈이 오는 문항(19번 등)을 위해 q_re 를 완화한 초안 뽑기(도구는 고치지 않음)."""
import json
import re
import sys

import fitz

sys.path.insert(0, r"D:\Work\블로그\리딩맵\도구")
m = __import__("세트_뽑기")

pdf, start, end, starts_file, out_path = sys.argv[1:6]
start, end = int(start), int(end)
doc = fitz.open(pdf)
lines = m.page_lines(doc)
guide_re = re.compile(rf"^\[{start}\s*[~～∼]\s*{end}\]")
gi = next(i for i, l in enumerate(lines) if guide_re.match(l.strip()))
q_re = lambda n: re.compile(rf"^{n}\.(?:\s|$)")
qi = {n: next(i for i, l in enumerate(lines) if i > gi and q_re(n).match(l)) for n in range(start, end + 1)}
nxt = next((i for i, l in enumerate(lines) if i > qi[end] and re.match(r"^\[\d+\s*[~～∼]\s*\d+\]", l.strip())), len(lines))
starts = [s.strip("\n") for s in open(starts_file, encoding="utf-8") if s.strip()]
body = lines[gi + 1: qi[start]]
paras, cur = [], None
for l in body:
    hit = next((s for s in starts if l.startswith(s)), None)
    if hit:
        if cur:
            paras.append(cur)
        cur = [l]
    elif cur is not None:
        cur.append(l)
if cur:
    paras.append(cur)
passage = [{"id": f"p{k}", "type": "para", "text": m.join(p), "underlines": []} for k, p in enumerate(paras, 1)]
questions = []
for n in range(start, end + 1):
    block = lines[qi[n]: (qi[n + 1] if n < end else nxt)]
    idx = [i for i, l in enumerate(block) if l[:1] and l[:1] in m.CIRCLED]
    stem = re.sub(rf"^{n}\.\s*", "", m.join(block[: idx[0]] if idx else block))
    points = 3 if "[3점]" in stem else 2
    choices = []
    for j, i in enumerate(idx):
        seg = block[i: (idx[j + 1] if j + 1 < len(idx) else len(block))]
        choices.append(m.join(seg)[1:].strip())
    questions.append({"no": n, "points": points, "stem": stem, "bogi": None, "choices": choices, "answer": None, "judgments": []})
data = {"guide": lines[gi].strip(), "range": [start, end], "passage": passage, "questions": questions, "raw_passage_lines": body}
json.dump(data, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("passage", len(passage), "questions", len(questions))
