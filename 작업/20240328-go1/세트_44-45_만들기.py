"""2024-03 고1 44~45번 세트(희곡 이미경 ｢그게 아닌데｣) → 세트_44-45.json
초안: _임시\\초안_44-45.json (줄 앞 공백만 떼는 래퍼로 뽑음, 문단시작_44-45.txt). 쪽 그림(문제_15·16쪽)·texttrace 로 확인한 것:
- [앞부분 줄거리] 상자(omit, 레이블 굵음). 대사 줄의 말한 이 이름(조련사·어머니·의사·형사·코끼리)만 굵고 콜론은 보통.
- (중략)은 가운데 줄. 마지막 문단은 쪽 단 경계(왼쪽 단 아래→오른쪽 단 위)에서 이어지지만 텍스트층에서 한 항목으로 합쳐졌다.
- 발문 ‘않은’ 밑줄 44·45번. 45번 <보기>는 문단 하나.
- 45번 선지 끝 «확인 사항» 안내는 초안에서 잘라 냈다.
- 해설지 없는 선지: 없음(44~45번 모든 선지가 해설지에 있다).
"""
import json
import re

HERE = r"D:\Work\블로그\리딩맵\작업\20240328-go1"
d = json.load(open(HERE + r"\_임시\초안_44-45.json", encoding="utf-8"))
d.pop("raw_passage_lines", None)
d["meta"] = {"exam": "2024학년도 3월 고1 전국연합학력평가 국어", "exam_id": "20240328-go1", "area": "문학(현대 희곡)",
             "topic": "그게 아닌데",
             "problem_pdf": "20240328-go1-problem-kor_mun_7628232M.pdf",
             "explanation_pdf": "20240328-go1-explanation-kor_hsj_PVWAO87B.pdf"}
d["guide"] = "[44 ~ 45] 다음 글을 읽고 물음에 답하시오."
ps = {p["id"]: p for p in d["passage"]}
assert ps["p1"]["text"].startswith("[앞부분 줄거리]")
ps["p1"]["type"] = "omit"
ps["p1"]["bold"] = ["[앞부분 줄거리]"]
assert ps["p15"]["text"] == "(중략)"
ps["p15"]["type"] = "omit"
ps["p15"]["center"] = True
assert ps["p29"]["text"].startswith("- 이미경")
ps["p29"]["type"] = "note"
for p in d["passage"]:
    m = re.match(r"(조련사|어머니|의사|형사|코끼리):", p["text"])
    if m:
        p["dialogue"] = True
        p["bold"] = [m.group(1)] if p["text"].count(m.group(1)) == 1 else [{"text": m.group(1), "nth": 1}]
d["ranges"] = []

Q = {q["no"]: q for q in d["questions"]}
c5 = Q[45]["choices"][4]
k = c5.index("* 확인 사항")
Q[45]["choices"][4] = c5[:k].strip()
for n in (44, 45):
    Q[n]["stem_underlines"] = ["않은"]
s45 = Q[45]["stem"]
k = s45.index("< 보 기 >")
st = s45[:k].replace("[3점]", "").strip()
assert st == "<보기>를 바탕으로 윗글을 감상한 내용으로 적절하지 않은 것은?", st
Q[45]["stem"] = st
Q[45]["points"] = 3
BG = s45[k + len("< 보 기 >"):].strip()
assert BG.startswith("이 작품은") and BG.endswith("의미한다."), BG
Q[45]["bogi"] = {"label": "보 기", "paras": [BG]}

expl = open(HERE + r"\해설_글자.txt", encoding="utf-8").read()


def section(no):
    i = re.search(rf"\n{no}\. \[출제의도\]", expl).start()
    if no < 45:
        j = re.search(rf"\n{no + 1}\. \[출제의도\]", expl[i + 1:]).start() + i + 1
    else:
        j = len(expl)
    lines = [l for l in expl[i:j].split("\n") if not re.fullmatch(r"=== 해설 \d+쪽 ===|\d+|고[123]", l.strip())]
    return "\n".join(lines)


def X(no, a, b):
    sec = section(no)
    keep = [(i, c) for i, c in enumerate(sec) if not c.isspace()]
    comp = "".join(c for _, c in keep)
    ca, cb = re.sub(r"\s+", "", a), re.sub(r"\s+", "", b)
    ia = comp.index(ca)
    ib = comp.index(cb, ia) + len(cb)
    return sec[keep[ia][0]: keep[ib - 1][0] + 1].replace("\n", "")


def J(choice, verdict, ans, ev, reason, xq):
    out = {"choice": choice, "verdict": verdict, "is_answer": ans, "basis": "해설지", "reason": reason,
           "evidence": [], "explanation_quote": xq}
    for e in ev:
        if e[0] == "bogi":
            out["evidence"].append({"source": "bogi", "para": None, "quote": e[1]})
        else:
            out["evidence"].append({"source": "passage", "para": e[0], "quote": e[1]})
    return out


# 44
Q[44]["answer"] = 5
Q[44]["judgments"] = [
    J(1, "적절", False, [("p2", "나도 코끼리랑 눈이 마주쳤지만 휘파람을 불었는데. 못 본 척 휘파람만 불었는데.")],
      "조련사는 코끼리들이 탈출하려는 낌새를 알았지만 휘파람만 불며 못 본 척했다고 말한다.",
      X(44, "① 조련사는", "말했다.")),
    J(2, "적절", False, [("p7", "시켜서 했다고. 그들이 널 1년 전부터 코끼리 조련에 투입했잖아.")],
      "형사는 ‘시켜서 했다’고 인정하라며 배후의 지시로 조련에 투입되었다고 다그친다.",
      X(44, "② 형사는", "다그쳤다.")),
    J(3, "적절", False, [("p9", "넌 그저 착한 마음에 코끼리들을 풀어주고 싶었잖아.")],
      "어머니는 코끼리를 풀어 준 까닭을 조련사의 착한 마음에서 찾는다.",
      X(44, "③ 어머니는", "찾았다.")),
    J(4, "적절", False, [("p25", "코끼리를 사랑할 순 있지만 그건 병이에요.")],
      "의사는 코끼리를 사랑하는 조련사의 마음을 ‘병’이라 부르며 병과 연관 지어 해석한다.",
      X(44, "④ 의사는", "해석했다.")),
    J(5, "부적절", True, [("p12", "(소리를 지른다) 가만히 앉아!"), ("p14", "얘야, 정신 차려.")],
      "형사, 의사, 어머니는 각자 자기 말만 할 뿐 서로 의견을 교환하는 장면이 없다.",
      X(44, "코끼리 탈출 사건에 대해", "나오지 않는다.")),
]

# 45
Q[45]["answer"] = 3
Q[45]["judgments"] = [
    J(1, "적절", False, [("p4", "조련사가 피한다."), ("bogi", "사람들 사이의 소통 단절의 문제를")],
      "조련사가 어머니의 손길을 피하고 의사와 형사의 말을 외면하는 것은 소통이 끊긴 상황을 보여 준다.",
      X(45, "① 조련사가 어머니의 손길을", "엿볼 수 있다.")),
    J(2, "적절", False, [("p16", "(꽤 지쳐 있다) 내가 했는데. 다 내가 했는데."), ("bogi", "결국 조련사는 자기 생각을 버리고")],
      "지친 조련사가 같은 말을 되풀이하는 것은 소통이 어려운 상황에서 자기 생각을 버리고 자포자기하는 모습이다.",
      X(45, "② 조련사가 꽤 지쳐", "볼 수 있다.")),
    J(3, "부적절", True, [("p24", "조련사가 편안한 미소를 지으며"), ("bogi", "회복 불가능한 단절 상황에 놓이게 되었음을 의미한다")],
      "조련사가 코끼리로 변해 가는 것은 단절이 깊어지는 과정이므로 미소를 짓는 모습을 단절에서 벗어난 것으로 볼 수 없다.",
      X(45, "조련사가 코끼리로 변해 가는 모습은", "보기 어렵다.")),
    J(4, "적절", False, [("p28", "형사, 의사, 어머니는 자신의 의지가 관철된 듯, 결의에 찬 박수를 친다."), ("bogi", "타인의 의지에 맞추어 순응하는")],
      "조련사가 타인의 의지에 순응해 코끼리가 된 뒤 세 사람이 박수를 치는 것은 자신들의 의지가 관철된 만족감을 드러낸다.",
      X(45, "④ 조련사가 코끼리가 되는 것은 소통의", "볼 수 있다.")),
    J(5, "적절", False, [("p28", "조련사와 코끼리는 형사, 의사, 어머니 사이를 돌며 쇼를 시작한다."), ("bogi", "수동적인 처지가 된다")],
      "코끼리가 되어 쇼를 하는 조련사는 동물원의 코끼리와 다를 바 없는 수동적인 처지로 전락한 모습이다.",
      X(45, "⑤ 조련사가 코끼리가 되는 것은 타인의", "볼 수 있다.")),
]

for q in d["questions"]:
    assert q["stem"] and len(q["choices"]) == 5 and q["answer"]
json.dump(d, open(HERE + r"\세트_44-45.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok")
