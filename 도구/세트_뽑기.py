"""기출 PDF 에서 세트 하나(지문 + 문항)의 초안 JSON 을 만든다.

사용: py -X utf8 도구/세트_뽑기.py <문제PDF> <시작번호> <끝번호> <문단시작어 파일> <출력 JSON>

- 글자는 PDF 텍스트층 그대로 쓴다(OCR 아님). 줄 끝에 공백이 있으면 단어 경계, 없으면 단어 중간으로 보고 이어 붙인다.
- 문단 경계·밑줄 범위·그림 위치는 텍스트층에 없으므로, 쪽 그림을 보고 확인한 값을 <문단시작어 파일>(한 줄에 하나)로 넘긴다.
- 이 도구는 초안만 만든다. 판단·근거는 사람이(Claude 가) 채우고, 세트_검사.py 를 통과해야 한다.
"""
import json
import re
import sys

import fitz

HEADER = re.compile(r"^(\d+|국어영역|국어 영역|고[123]|홀수형|짝수형)$")
CIRCLED = "①②③④⑤"


def page_lines(doc):
    """쪽 머리글·쪽 번호를 뺀 줄 목록(줄 끝 공백 유지)."""
    out = []
    for page in doc:
        for line in page.get_text("text").split("\n"):
            if HEADER.match(line.strip()):
                continue
            out.append(line)
    return out


def join(lines):
    return "".join(lines).strip()


def main():
    pdf, start, end, starts_file, out_path = sys.argv[1:6]
    start, end = int(start), int(end)
    doc = fitz.open(pdf)
    lines = page_lines(doc)

    guide_re = re.compile(rf"^\[{start}\s*[~～]\s*{end}\]")
    gi = next(i for i, l in enumerate(lines) if guide_re.match(l.strip()))
    q_re = lambda n: re.compile(rf"^{n}\.\s")
    qi = {n: next(i for i, l in enumerate(lines) if i > gi and q_re(n).match(l)) for n in range(start, end + 1)}
    nxt = next((i for i, l in enumerate(lines) if i > qi[end] and re.match(r"^\[\d+\s*[~～]\s*\d+\]", l.strip())), len(lines))

    # 지문: 문단 시작어로 나눈다. 시작어 사이에 끼는 그림 글자(짧은 줄)는 버린다.
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
    paras.append(cur)
    passage = []
    for k, p in enumerate(paras, 1):
        # 그림 글자 제거: 문단 끝 문장부호 뒤에 붙은 짧은 줄들
        text = join(p)
        passage.append({"id": f"p{k}", "type": "para", "text": text, "underlines": []})

    questions = []
    for n in range(start, end + 1):
        block = lines[qi[n]: (qi[n + 1] if n < end else nxt)]
        idx = [i for i, l in enumerate(block) if l[:1] in CIRCLED]
        stem_lines = block[: idx[0]]
        stem = join(stem_lines)
        stem = re.sub(rf"^{n}\.\s*", "", stem)
        points = 3 if "[3점]" in stem else 2
        choices = []
        for j, i in enumerate(idx):
            seg = block[i: (idx[j + 1] if j + 1 < len(idx) else len(block))]
            choices.append(join(seg)[1:].strip())
        questions.append({"no": n, "points": points, "stem": stem, "bogi": None,
                          "choices": choices, "answer": None, "judgments": []})

    data = {"guide": lines[gi].strip(), "range": [start, end], "passage": passage, "questions": questions}
    json.dump(data, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("passage", len(passage), "questions", len(questions))


if __name__ == "__main__":
    main()
