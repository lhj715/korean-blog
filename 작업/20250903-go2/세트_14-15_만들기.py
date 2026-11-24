"""2025-09 고2 14~15번(문법 단독 문항: 합성 동사·본용언+본용언, 중세 국어 높임법) 세트 → 세트_14-15.json

쪽 그림·PDF 로 확인한 것(문제_5쪽.png, 문제_6쪽_왼쪽.png):
- 안내문·지문 없음(guide null, passage []). 문항마다 자기 <보기> 상자가 있다.
- 14번: <보기> = 학생 질문 + 선생님 설명(말한 이 «학생»·«선생님» 만 굵음: texttrace type=1 이 이름 글자에만 있고 콜론은 type=0)
  + «[학습 활동]»(굵음, 괄호 포함) + ◦ 안내 줄 + 표(합성 동사가 포함된 문장 ㉠ / 본용언+본용언이 포함된 문장 ㉡, 텍스트층 글자 있음 → 쪽에서 잘라 그림).
  발문 밑줄 '않은'. 선지는 «㉠: … ㉡: …» 두 줄(대괄호로 묶임). ⑤ 뒤 [A] 는 12~13번 지문 3문단의 구간 표시인데 텍스트층 순서상 여기 붙어 나온다 → 잘라 낸다.
- 15번: <보기>(문단 하나, 중세 국어 선어말 어미 3종에 옛한글 PUA 6자) + <자료>(ㄱㄴㄷ 3줄, 각각 아래 현대어 풀이 줄).
  PUA 가 든 보기 문단과 자료 ㄱ·ㄴ 줄은 쪽에서 잘라 낸 그림(display_image)으로 보인다. ㄷ 줄은 PUA 없음. 발문 밑줄 '않은', [3점].
  선지에는 PUA 가 없다.
- 굵은 글씨·네모 글자는 15번에 없음.
"""
import json

HERE = r"D:\Work\블로그\리딩맵\작업\20250903-go2"
d = json.load(open(HERE + r"\_임시\초안_14-15.json", encoding="utf-8"))
d.pop("raw_passage_lines", None)
d["meta"] = {"exam": "2025년 9월 고2 전국연합학력평가 국어", "exam_id": "20250903-go2", "area": "문법",
             "topic": "합성 동사와 본용언+본용언·중세 국어의 높임 표현", "problem_pdf": "20250903-go2-problem-kor_mun_8HG61RY3_1.pdf",
             "explanation_pdf": "20250903-go2-explanation-kor_hsj_ICT76N4K_1.pdf"}
d["guide"] = None
d["passage"] = []
Q = {q["no"]: q for q in d["questions"]}

# ---- 14번
s14 = Q[14]["stem"]
Q[14]["stem"] = s14[: s14.index("<보 기>")].strip()
Q[14]["stem_underlines"] = ["않은"]
body = s14[s14.index("<보 기>") + len("<보 기>"):]
i2 = body.index("선생님:")
i3 = body.index("[학습 활동]")
i4 = body.index("합성 동사가포함된")
D1, D2 = body[:i2].strip(), body[i2:i3].strip()
LEAD = body[i3 + len("[학습 활동]"): i4].strip()
TBL = body[i4:].strip()
assert D1.startswith("학생:") and D2.endswith("해 볼까요?") and LEAD.startswith("◦문장의") and TBL.endswith("㉠㉡"), (D1[:5], D2[-8:], LEAD[:5], TBL)
Q[14]["bogi"] = {"label": "보 기", "blocks": [
    {"id": "b1", "type": "para", "dialogue": True, "text": D1, "bold": ["학생"], "underlines": []},
    {"id": "b2", "type": "para", "dialogue": True, "text": D2, "bold": ["선생님"], "underlines": []},
    {"id": "b3", "type": "para", "text": "[학습 활동]", "bold": ["[학습 활동]"], "underlines": []},
    {"id": "b4", "type": "para", "text": LEAD, "underlines": []},
    {"id": "f1", "type": "figure", "caption": "", "image": "그림_14-15_14_표.png", "pdf_text": TBL, "raster_text": "",
     "alt": "표: 왼쪽 칸 ‘합성 동사가 포함된 문장’ 아래 ㉠, 오른쪽 칸 ‘본용언+본용언이 포함된 문장’ 아래 ㉡"}]}
Q[14]["choices"] = Q[14]["choices"][:5]
Q[14]["choices"][4] = Q[14]["choices"][4].replace("[A]", "").strip()
Q[14]["choices"] = [c.replace("㉡:", " ㉡:").strip() for c in Q[14]["choices"]]
assert all(c.startswith("㉠: ") and " ㉡: " in c for c in Q[14]["choices"])

# ---- 15번
s15 = Q[15]["stem"]
Q[15]["stem"] = s15[: s15.index("[3점]")].strip()
Q[15]["stem_underlines"] = ["않은"]
mk1, mk2 = "<보 기>", "<자 료>"
B15 = s15[s15.index(mk1) + len(mk1): s15.index(mk2)].strip()
R15 = s15[s15.index(mk2) + len(mk2):]
cuts = [R15.index(x) for x in ("ㄱ. ", "[문수가", "ㄴ. ", "[태자를", "ㄷ. ", "[야수가")] + [len(R15)]
parts = [R15[a:b].strip() for a, b in zip(cuts, cuts[1:])]
assert len(parts) == 6 and parts[5] == "[야수가 그 소식을 들으시고]", parts
assert B15.startswith("중세 국어에서") and B15.endswith("실현되었다.")
Q[15]["bogi"] = [
    {"label": "보 기", "blocks": [
        {"id": "b1", "type": "para", "text": B15, "display_image": "그림_14-15_15_보기.png", "underlines": []}]},
    {"label": "자 료", "blocks": [
        {"id": "e1", "type": "para", "text": parts[0], "display_image": "그림_14-15_15_자료ㄱ.png", "underlines": []},
        {"id": "t1", "type": "para", "text": parts[1], "underlines": []},
        {"id": "e2", "type": "para", "text": parts[2], "display_image": "그림_14-15_15_자료ㄴ.png", "underlines": []},
        {"id": "t2", "type": "para", "text": parts[3], "underlines": []},
        {"id": "e3", "type": "para", "text": parts[4], "underlines": []},
        {"id": "t3", "type": "para", "text": parts[5], "underlines": []}]},
]

# 해설지에서 문장 이어 따오기
expl = open(HERE + r"\해설_글자.txt", encoding="utf-8").read()
s_14 = expl[expl.index("14. [출제의도]"): expl.index("15. [출제의도]")].replace("\n", "")
s_15 = expl[expl.index("15. [출제의도]"): expl.index("** 인문 **")].replace("\n", "")


def cut(sec, a, b):
    i = sec.index(a)
    j = sec.index(b, i) + len(b)
    return sec[i:j]


def J(choice, verdict, ans, ev, basis, reason, xq=None):
    def one(e):
        return {"source": "bogi", "para": None, "quote": e}
    out = {"choice": choice, "verdict": verdict, "is_answer": ans, "basis": basis, "reason": reason,
           "evidence": [one(e) for e in ev]}
    if xq:
        out["explanation_quote"] = xq
    return out


Q[14]["answer"] = 1
Q[14]["judgments"] = [
    J(1, "부적절", True,
      ["‘직책을 집어 멀리 던졌다.’처럼 두 용언 사이에 다른 문장 성분이 들어갈 수 없어요."],
      "해설지",
      "㉠과 ㉡의 ‘건너뛰다’는 두 용언 사이에 다른 문장 성분이 들어갈 수 없는 합성 동사다. ㉡은 본용언+본용언 구성이 아니므로 ㉡의 예로 알맞지 않다.",
      cut(s_14, "㉠과 ㉡에 쓰인", "모두 합성 동사이다.")),
    J(2, "적절", False,
      ["‘집다’와 ‘던지다’의 의미를 단순히 합한 것과는 다르죠?"],
      "자체",
      "㉠의 ‘벗어던졌다’는 관습을 버렸다는 뜻이라 ‘벗다’와 ‘던지다’의 뜻을 단순히 합한 것과 다른 합성 동사다. ㉡의 ‘벗어 던졌다’는 모자를 벗은 뒤 던졌다는 뜻의 본용언+본용언이다."),
    J(3, "적절", False,
      ["합성 동사는 사전에 등재된 한 단어이기 때문에 띄어쓰기를 하지 않고"],
      "자체",
      "㉠의 ‘끌어내렸다’는 그를 회장직에서 물러나게 했다는 뜻으로 붙여 쓰는 한 단어, 곧 합성 동사다. ㉡의 ‘끌어 내렸다’는 썰매를 끌고 내렸다는 뜻의 본용언+본용언이다."),
    J(4, "적절", False,
      ["각각의 용언이 주어와 호응하기 때문에 본용언+ 본용언 구성으로 볼 수 있어요."],
      "자체",
      "㉠의 ‘뜯어먹어서’는 남의 것을 억지로 얻으려 한다는 뜻의 합성 동사다. ㉡의 ‘뜯어 먹는다’는 소가 풀을 뜯고 소가 먹는다는 뜻이어서 두 용언이 모두 주어와 호응하는 본용언+본용언이다."),
    J(5, "적절", False,
      ["이때의 두 용언은 반드시 띄어 써야 하며 두 용언 사이에 다른 문장 성분이 들어갈 수 있어요."],
      "자체",
      "㉠의 ‘집어먹었다’는 겁을 먹었다는 뜻이라 ‘집다’와 ‘먹다’의 뜻을 단순히 합한 것이 아닌 합성 동사다. ㉡의 ‘집어 먹었다’는 과자를 집어서 먹었다는 뜻으로 두 용언 사이에 다른 문장 성분이 들어갈 수 있는 본용언+본용언이다."),
]

Q[15]["answer"] = 4
Q[15]["judgments"] = [
    J(1, "적절", False,
      ["주체 높임은 주로 선어말 어미 ‘–시– / –샤–’", "[문수가 마야께 청하시되]"],
      "해설지",
      "ㄱ의 풀이 ‘청하시되’에서 주체 ‘文殊(문수)’를 높이는 데 선어말 어미 ‘–샤–’가 쓰였다.",
      cut(s_15, "ㄱ에서는 주체인", "‘–샤–’가 사용되었다.")),
    J(2, "적절", False,
      ["객체 높임은 선어말 어미", "ㄱ. 文殊(문수)ㅣ 摩耶(마야)"],
      "해설지",
      "ㄱ에서 객체 ‘摩耶(마야)’를 높이기 위해 조사와 객체 높임 선어말 어미가 함께 쓰였다. 풀이의 ‘마야께’가 이를 보여 준다.",
      cut(s_15, "②ㄱ에서는 객체인", "사용되었다.").lstrip("②")),
    J(3, "적절", False,
      ["특수 어휘, 조사에 의해 실현되었다", "ㄴ. 太子(태자)"],
      "해설지",
      "ㄴ에서 객체 ‘太子(태자)’를 높이는 데 특수 어휘 ‘모셔’가 쓰였다.",
      cut(s_15, "③ㄴ에서는 객체인", "사용되었다.").lstrip("③")),
    J(4, "부적절", True,
      ["夫人(부인)", "[태자를 싸 안아 부인께 모셔 오니]"],
      "해설지",
      "ㄴ에 쓰인 선어말 어미는 ‘夫人(부인)’이 아니라 ‘太子(태자)’를 높이기 위한 것이다. ‘夫人(부인)’ 뒤에는 어미가 아니라 조사가 붙어 ‘부인께’로 풀이되므로 선지는 틀리다.",
      cut(s_15, "ㄴ에 사용된 선어말 어미", "높이기 위해 사용되었다.")),
    J(5, "적절", False,
      ["ㄷ. 耶輸(야수)ㅣ 그 긔별 드르시고", "[야수가 그 소식을 들으시고]"],
      "해설지",
      "ㄷ의 ‘드르시고’에서 주체 ‘耶輸(야수)’를 높이는 데 선어말 어미 ‘–시–’가 쓰였다.",
      cut(s_15, "⑤ㄷ에서는 주체인", "사용되었다.").lstrip("⑤")),
]

json.dump(d, open(HERE + r"\세트_14-15.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok")
