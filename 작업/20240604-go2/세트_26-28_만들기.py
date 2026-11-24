"""2024-06 고2 26~28번(현대소설, 문순태 ｢늙으신 어머니의 향기｣) 세트 -> 세트_26-28.json
초안은 도구/세트_뽑기.py 로 뽑았다(_임시\\초안_26-28.json, 문단시작 '-'). 지문은 raw_passage_lines 에서 다시 짠다.
쪽 그림(문제_9쪽, 10쪽)·texttrace·PDF 좌표로 확인한 것:
- 문단: 줄 시작 x=108(10쪽)/449(9쪽) 들여쓰기로 확인. 앞부분 4문단, [중략 부분 줄거리] 는 omit(굵은 글씨), 뒷부분은 대사 한 줄이 한 항목.
  쪽 경계(9쪽→10쪽)에서 [중략 부분 줄거리] 뒤 '예상했던 대로' 가 새 문단.
- 밑줄(PDF 선): ㉠ 노인네들이~듣지 않았다, ㉡ 몸살이~보았다, ㉢ 그 무렵부터~시작했다, ㉣ 아내가~있었다, ㉤ 쓰디쓴~팠다. 발문 '않은' 밑줄은 27·28번.
- 굵은 글씨(texttrace type 0+1, 쪽 그림 확인): 9쪽 생에 대한 집착 / 우리 집의 '집' / 밥이 없으면 / 까탈을 부리 / 어머니의 삶 / 궁핍과 땀과 희생과 인종 /
  특유한 어머니의 냄새 / 어머니의 냄새(첫 번째) / 역겹다고 느 / [중략 부분 줄거리]. 10쪽 냄새 때문에 숨을 쉴 수가 없 / 아주 심해요 / 절대로 내 몸에서 나는 냄새가 아녀.
  따옴표와 마침표, 조사는 보통. 발문·선지·<보기>는 굵은 글씨 없음.
- 지문 전체를 감싼 네모 상자는 도구가 그리지 못한다(한계).
"""
import json
import re

HERE = r"D:\Work\블로그\리딩맵\작업\20240604-go2"
d = json.load(open(HERE + r"\_임시\초안_26-28.json", encoding="utf-8"))
rawp = d.pop("raw_passage_lines")
R = lambda i: rawp[i].strip()


def joinp(a, b):
    return "".join(rawp[a:b + 1]).strip()


def T(id_, type_, text, ul=(), bold=None):
    p = {"id": id_, "type": type_, "text": text, "underlines": [{"mark": m, "text": t} for m, t in ul]}
    if bold:
        p["bold"] = bold
    return p


# 문단 경계 (raw 줄 번호 범위)
spans = [(0, 11), (12, 26), (27, 40), (41, 47)]
plist = [T(f"p{k + 1}", "para", joinp(a, b)) for k, (a, b) in enumerate(spans)]
assert R(0).startswith("어머니는 동물적") and R(12).startswith("어머니가 젊었을") and R(27).startswith("그러던") and R(41).startswith("나는 어머니의")
assert R(48).startswith("[중략 부분 줄거리]") and R(52).startswith("예상했던 대로")
omit = T("o1", "omit", joinp(48, 50), [], ["[중략 부분 줄거리]"])
after = [
    ("p5", 52, 55), ("q1", 56, 56), ("p6", 57, 63), ("q2", 64, 64), ("p7", 65, 66), ("q3", 67, 67), ("p8", 68, 68),
    ("q4", 69, 69), ("q5", 70, 70), ("q6", 71, 73), ("q7", 74, 74), ("q8", 75, 75), ("q9", 76, 76), ("q10", 77, 77),
    ("q11", 78, 78), ("q12", 79, 79), ("q13", 80, 80), ("p9", 81, 82), ("q14", 83, 83), ("p10", 84, 84), ("q15", 85, 85),
    ("p11", 86, 87), ("q16", 88, 89), ("p12", 90, 92),
]
alist = [T(i, "para", joinp(a, b)) for i, a, b in after]
note = T("n1", "note", R(93))
d["passage"] = plist + [omit] + alist + [note]
P = {p["id"]: p for p in d["passage"]}

# 밑줄
ul = {
    "p1": [("㉠", "노인네들이 항생제 주사를 많이 맞는 것이 좋지 않다는 말을 해도 듣지 않았다.")],
    "p2": [("㉡", "몸살이 나서 꿍꿍 앓으면서도 휘청거리며 호미를 들고 밭에 나가는 모습을 자주 보았다.")],
    "p3": [("㉢", "그 무렵부터 말로 형언할 수 없는 어머니의 냄새가 솔솔 풍기기 시작했다.")],
    "p6": [("㉣", "아내가 누워 있는 사이 어머니는 기세 좋게 주방에서 달그락거리며 저녁을 준비하고 있었다.")],
    "p12": [("㉤", "쓰디쓴 세월의 냄새라는 어머니의 말이 명치끝을 후벼 팠다.")],
}
for k, v in ul.items():
    P[k]["underlines"] = [{"mark": m, "text": t} for m, t in v]

# 굵은 글씨
t1 = P["p1"]["text"]
pos = t1.index("우리 집") + len("우리 ")
nth_jip = t1[:pos + 1].count("집")
assert t1[pos] == "집"
P["p1"]["bold"] = ["생에 대한 집착", {"text": "집", "nth": nth_jip}, "밥이 없으면", "까탈을 부리"]
P["p2"]["bold"] = ["어머니의 삶", "궁핍과 땀과 희생과 인종"]
P["p3"]["bold"] = ["특유한 어머니의 냄새"]
P["p4"]["bold"] = [{"text": "어머니의 냄새", "nth": 1}, "역겹다고 느"]
P["q1"]["bold"] = ["냄새 때문에 숨을 쉴 수가 없"]
P["q11"]["bold"] = ["아주 심해요"]
P["q14"]["bold"] = ["절대로 내 몸에서 나는 냄새가 아녀"]
for _p in d["passage"]:
    for b in _p.get("bold", []):
        t = b if isinstance(b, str) else b["text"]
        n = 1 if isinstance(b, str) else b["nth"]
        assert _p["text"].count(t) >= n, (_p["id"], t)
        if isinstance(b, str):
            assert _p["text"].count(t) == 1, (_p["id"], t, _p["text"].count(t))
    for u in _p["underlines"]:
        assert u["text"] in _p["text"], (_p["id"], u)
d["ranges"] = []
d["guide"] = "[26 ~ 28] 다음 글을 읽고 물음에 답하시오."
d["meta"] = {"exam": "2024학년도 6월 고2 전국연합학력평가 국어", "exam_id": "20240604-go2", "area": "문학(현대소설)",
             "topic": "문순태, ｢늙으신 어머니의 향기｣",
             "problem_pdf": "20240604-go2-problem-kor_mun_22484VF6.pdf",
             "explanation_pdf": "20240604-go2-explanation-kor_hsj_K5T5L1W7.pdf"}

Q = {x["no"]: x for x in d["questions"]}
for n in (27, 28):
    Q[n]["stem_underlines"] = ["않은"]
s = Q[28]["stem"]
i = s.index("<보 기>")
Q[28]["stem"] = s[:i].replace("[3점]", "").strip()
bg = s[i + len("<보 기>"):].strip()
assert bg.startswith("소설은 감각적") and bg.endswith("지적한다.")
Q[28]["bogi"] = {"label": "보 기", "paras": [bg]}
BG28 = bg
for q in Q.values():
    assert q["stem"].strip(), q["no"]

expl = open(HERE + r"\해설_글자.txt", encoding="utf-8").read()


def section(no):
    i = expl.index(f"\n{no}. [출제의도]")
    nxt = {28: "\n[29~33]"}.get(no, f"\n{no + 1}. [출제의도]")
    return expl[i: expl.index(nxt, i)]


def X(no, a, b):
    sec = section(no)
    keep = [(i, c) for i, c in enumerate(sec) if not c.isspace()]
    comp = "".join(c for _, c in keep)
    ca, cb = re.sub(r"\s+", "", a), re.sub(r"\s+", "", b)
    ia = comp.index(ca)
    ib = comp.index(cb, ia) + len(cb)
    return sec[keep[ia][0]: keep[ib - 1][0] + 1].replace("\n", "")


def sq(t):
    return "".join(t.split())


def J(choice, verdict, ans, ev, reason, xq=None, bogi=None):
    out = {"choice": choice, "verdict": verdict, "is_answer": ans, "basis": "해설지" if xq else "자체", "reason": reason,
           "evidence": []}
    for pid, qt in ev:
        if pid == "bogi":
            assert qt in bogi, qt
            out["evidence"].append({"source": "bogi", "para": None, "quote": qt})
        else:
            assert qt in P[pid]["text"], (choice, pid, qt)
            out["evidence"].append({"source": "passage", "para": pid, "quote": qt})
    if xq:
        out["explanation_quote"] = xq
    return out


Q[26]["answer"] = 2
Q[26]["judgments"] = [
    J(1, "부적절", False, [("p7", "식탁에 마주 앉아 저녁을 먹던 어머니가 마뜩찮은 표정으로 뚜벅 물었다."),
                         ("p11", "그러면서 어머니는 상반신을 내 앞으로 바짝 꺾으며 재촉했다.")],
      "‘나’와 어머니의 식탁 대화가 차례대로 이어질 뿐, 동시에 진행되는 두 사건이 번갈아 제시되는 곳은 없다.",
      X(26, "① 동시에", "않다.")),
    J(2, "적절", True, [("p1", "어머니는 동물적 본능에 가까울 정도로 생에 대한 집착이 강했다."),
                      ("p2", "어머니가 젊었을 적에는 그렇지가 않았다.")],
      "‘나’가 보고 느낀 대로 어머니가 지금은 생에 집착하고 젊을 적에는 희생적이었다고 서술하여, 한 인물의 삶의 모습을 보여 준다.",
      X(26, "윗글은 서술자인", "있다.")),
    J(3, "부적절", False, [("p4", "나는 어머니의 냄새가 역겹다고 느껴질 때마다 젊었을 때의 어머니를 떠올리곤 한다."),
                         ("p2", "어머니가 젊었을 적에는 그렇지가 않았다.")],
      "현재형 서술은 있으나, 젊은 시절의 일은 ‘않았다’처럼 과거 시제로 서술되어 과거의 사건을 현재 시제로 서술하지 않았다.",
      X(26, "③ 현재 시제로", "아니다.")),
    J(4, "부적절", False, [("p4", "나는 어머니의 냄새가 역겹다고 느껴질 때마다"),
                         ("p12", "어머니의 말이 명치끝을 후벼 팠다.")],
      "처음부터 끝까지 ‘나’가 직접 보고 느낀 것을 서술하며, 장면에 따라 서술자가 바뀌지 않는다.",
      X(26, "④ 이 작품은", "있다.")),
    J(5, "부적절", False, [("p6", "나는 우선 창문부터 열고 코끝이 아리도록 안방에 라벤더 향수를 듬뿍 뿌려댔다.")],
      "안방이 언급되지만 ‘나’의 행동에 곁들여 나올 뿐, 공간적 배경을 구체적으로 묘사한 대목은 없다.",
      X(26, "⑤ 공간적", "않다.")),
]

Q[27]["answer"] = 3
Q[27]["judgments"] = [
    J(1, "적절", False, [("p1", "㉠노인네들이 항생제 주사를 많이 맞는 것이 좋지 않다는 말을 해도 듣지 않았다.")],
      "항생제 주사가 좋지 않다는 주변의 말을 듣지 않는 데서 어머니의 완고함이 드러난다.",
      X(27, "① 주변의 말을", "있다.")),
    J(2, "적절", False, [("p2", "㉡몸살이 나서 꿍꿍 앓으면서도 휘청거리며 호미를 들고 밭에 나가는 모습을 자주 보았다."),
                       ("p2", "자신보다 가족을 위해서 희생하는 것을 삶의 보람으로 생각하는 것 같았다.")],
      "몸살이 나도 호미를 들고 밭에 나가는 모습에서 가족을 위해 헌신한 어머니가 드러난다.",
      X(27, "② 몸살이", "있다.")),
    J(3, "부적절", True, [("p3", "㉢그 무렵부터 말로 형언할 수 없는 어머니의 냄새가 솔솔 풍기기 시작했다."),
                        ("p4", "나는 어머니의 냄새가 역겹다고 느껴질 때마다")],
      "‘나’는 어머니의 냄새를 역겹다고 느껴 부정적으로 판단하고 있으므로 좋은지 나쁜지 판단하기 어려워한다고 볼 수 없다.",
      X(27, "‘나’는 어머니의", "있다.")),
    J(4, "적절", False, [("p6", "㉣아내가 누워 있는 사이 어머니는 기세 좋게 주방에서 달그락거리며 저녁을 준비하고 있었다.")],
      "며느리가 쓰러져 누워 있는데도 기세 좋게 저녁을 준비하는 모습에서 아내의 상황에 아랑곳하지 않는 어머니가 드러난다.",
      X(27, "④ 며느리가", "있다.")),
    J(5, "적절", False, [("p12", "㉤쓰디쓴 세월의 냄새라는 어머니의 말이 명치끝을 후벼 팠다.")],
      "어머니의 말이 명치끝을 후벼 팠다는 데서 그 말에 아픔을 느끼는 ‘나’가 드러난다.",
      X(27, "⑤ 어머니가", "있다.")),
]

Q[28]["answer"] = 2
Q[28]["judgments"] = [
    J(1, "적절", False, [("p1", "밥이 없으면 아무렇지 않은 일에도 까탈을 부리며 심하게 며느리를 닦달했다."),
                       ("p1", "어머니는 동물적 본능에 가까울 정도로 생에 대한 집착이 강했다."),
                       ("bogi", "부모 세대에 대한 그릇된 관념을 지적한다.")],
      "밥이 없다고 까탈을 부리는 어머니를 생에 대한 집착으로 보는 것은 부모 세대에 대한 그릇된 관념으로 볼 수 있다.",
      X(28, "① ‘나’가 밥이", "있다."), BG28),
    J(2, "부적절", True, [("p2", "어머니의 삶은 궁핍과 땀과 희생과 인종의 그것이었다."),
                        ("p2", "우리 식구의 생명줄을 머리에 이고 버둥거렸던 어머니의 모습은 내 가슴속에, 이 세상에서 가장 아름답고 강한 존재로 살아 있었다.")],
      "‘나’는 어머니의 삶을 궁핍과 희생으로 보면서도 어머니를 가장 아름답고 강한 존재로 기억하므로 어머니의 삶을 부정적으로 여긴다고 볼 수 없다.",
      X(28, "‘우리 식구의", "없다."), BG28),
    J(3, "적절", False, [("p3", "특유한 어머니의 냄새를 피우기 시작한 것 같다."),
                       ("bogi", "소설은 감각적 소재를 활용하여 현실의 문제를 드러내기도 한다.")],
      "어머니의 냄새는 가족 사이의 갈등을 일으키는 감각적 소재로 쓰여 현실의 문제를 드러낸다.",
      X(28, "③ ‘어머니의 냄새’라는", "있다."), BG28),
    J(4, "적절", False, [("p4", "나는 어머니의 냄새가 역겹다고 느껴질 때마다"),
                       ("q1", "“냄새 때문에 숨을 쉴 수가 없어요.”")],
      "어머니의 냄새를 역겹다고 느끼는 ‘나’와 숨을 쉴 수가 없다고 말하는 아내는 그 냄새를 문제로 여기는 자식의 모습이다.",
      X(28, "④ 어머니의 냄새를", "있다."), BG28),
    J(5, "적절", False, [("q11", "“아주 심해요.”"),
                       ("q14", "절대로 내 몸에서 나는 냄새가 아녀.”"),
                       ("bogi", "냄새에 대한 각기 다른 인식으로 형성된 갈등")],
      "냄새가 심하다는 ‘나’와 자기 몸의 냄새가 아니라고 부인하는 어머니의 말에서 서로 다른 인식에서 오는 갈등이 드러난다.",
      X(28, "⑤ 어머니의 냄새가", "있다."), BG28),
]
for x in d["questions"]:
    assert len(x["choices"]) == 5 and len(x["judgments"]) == 5

json.dump(d, open(HERE + r"\세트_26-28.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok")
