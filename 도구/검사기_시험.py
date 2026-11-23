"""세트_검사.py 가 오류를 정말 잡는지 시험한다. 합격한 세트에 일부러 오류를 하나씩 넣어 모두 불합격이 나와야 한다.

사용: py -X utf8 도구/검사기_시험.py <합격한 세트 JSON> <문제PDF> <해설PDF> <정답 bundle JSON>
검사기를 고치면 반드시 다시 돌린다. '놓침' 이 하나라도 있으면 종료 코드 1.
"""
import copy
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
set_path, *rest = sys.argv[1:5]
src = json.load(open(set_path, encoding="utf-8"))


def first(d, key):
    return next(x for x in d if key(x))


def q(d, i):
    return d["questions"][i]


def para_with_underline(d):
    return first(d["passage"], lambda p: p.get("underlines"))


def q_with_bogi(d):
    return first(d["questions"], lambda x: x.get("bogi"))


def q3(d):
    return first(d["questions"], lambda x: x["points"] == 3)


CASES = [
    ("정답 번호 바꿈", lambda d: q(d, 0).update(answer=q(d, 0)["answer"] % 5 + 1)),
    ("지문 글자 하나 바꿈", lambda d: d["passage"][0].update(text=d["passage"][0]["text"][:10] + "뷁" + d["passage"][0]["text"][11:])),
    ("선지 끝 잘라냄", lambda d: q(d, 1)["choices"].__setitem__(2, q(d, 1)["choices"][2][:-8])),
    ("근거 인용 지어냄", lambda d: q(d, 2)["judgments"][0]["evidence"][0].update(quote="지문에 없는 문장이다")),
    ("판단 말 뒤집음", lambda d: q(d, 0)["judgments"][0].update(verdict={"적절": "부적절", "부적절": "적절", "일치": "불일치", "불일치": "일치"}[q(d, 0)["judgments"][0]["verdict"]])),
    ("해설지 인용 지어냄", lambda d: first(q(d, 0)["judgments"], lambda j: j["basis"] == "해설지").update(explanation_quote="해설지에 없는 말")),
    ("밑줄 범위 한 글자 늘림", lambda d: para_with_underline(d)["underlines"][0].update(
        text=para_with_underline(d)["text"].split(para_with_underline(d)["underlines"][0]["mark"], 1)[1][: len(para_with_underline(d)["underlines"][0]["text"]) + 2])),
    ("3점 표시 빠뜨림", lambda d: q3(d).update(points=2) if any(x["points"] == 3 for x in d["questions"]) else q(d, 0).update(points=3)),
    ("그림 글자 섞음", lambda d: d["passage"][0].update(text=d["passage"][0]["text"] + "AB--------++++++++")),
    ("근거 없는 선지", lambda d: q(d, 1)["judgments"][3].update(evidence=[])),
    ("다른 문항 해설 인용", lambda d: first(q(d, 1)["judgments"], lambda j: j["basis"] == "해설지").update(
        explanation_quote=first(q(d, 0)["judgments"], lambda j: j["basis"] == "해설지")["explanation_quote"])),
    ("마지막 문단 뒷부분 잘라냄", lambda d: [p for p in d["passage"] if p["type"] == "para"][-1].update(
        text=[p for p in d["passage"] if p["type"] == "para"][-1]["text"][:-15])),
    ("발문 앞부분 잘라냄", lambda d: q(d, 0).update(stem=q(d, 0)["stem"][4:])),
]
if any(p["type"] == "figure" for p in src["passage"]):
    CASES.append(("그림 글자 기록 지움", lambda d: first(d["passage"], lambda p: p["type"] == "figure").update(pdf_text="")))
if any(x.get("bogi") for x in src["questions"]):
    CASES.append(("보기 글자 바꿈", lambda d: q_with_bogi(d)["bogi"]["paras"].__setitem__(0, "뷁" + q_with_bogi(d)["bogi"]["paras"][0][1:])))

missed = 0
tmp = os.path.join(tempfile.gettempdir(), "리딩맵_변조.json")
for name, f in CASES:
    d = copy.deepcopy(src)
    f(d)
    json.dump(d, open(tmp, "w", encoding="utf-8"), ensure_ascii=False)
    r = subprocess.run([sys.executable, "-X", "utf8", os.path.join(HERE, "세트_검사.py"), tmp, *rest],
                       capture_output=True, text=True, encoding="utf-8")
    codes = sorted({l.strip()[1:].split("]")[0] for l in r.stdout.splitlines() if l.strip().startswith("[")})
    if r.returncode:
        print(f"  잡음  {name:22s} {','.join(codes)}")
    else:
        missed += 1
        print(f"  놓침  {name}")
os.remove(tmp)
print(f"== {len(CASES)}가지 중 {len(CASES) - missed}가지 잡음")
sys.exit(1 if missed else 0)
