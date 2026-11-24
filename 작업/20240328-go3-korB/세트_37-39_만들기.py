"""2024-03-28 고3 언어와 매체(korB) 37~39번 세트(안내문 없는 단독 문항 묶음): 초안 + 쪽 그림 확인값 + 해설지 기반 판단 → 세트_37-39.json

확인한 것(문제_13쪽·14쪽.png, PDF 텍스트층·선·글꼴):
- 37번: 발문 밑줄 없음, 굵은 글씨 없음(글꼴 전부 type 0). <학습 활동> 상자 = 문단 + 안쪽 상자(낱말 두 줄, 가운데 맞춤, 실선) + ◦ 줄 4개. 선지 밑줄 없음.
- 38번: 발문 «않은» 밑줄(PDF 선). <보기> 상자 = 문단 1개. 밑줄 ㉮(두 어근이 대등하게 결합하는 것), ㉯(한 어근이 다른 어근을 수식하는 것),
  ㉰(각각의 어근이 원래 지닌 의미와는 다른 새로운 의미를 가지는 것; 줄 바꿈 3줄). 마크 ㉮㉯㉰ 는 선 밖. ㄱ~ㅁ 예문 5줄. 굵은 글씨 없음.
- 39번: 발문 밑줄 없음. <보기> 상자 = «선생님:» 문단(말한 이 이름 «선생님» 만 굵음 type 1, 콜론은 보통) + 흐름도(그림, 글자는 pdf_text) +
  «[자료]»(굵음, type 1) + ㄱ~ㅂ 6줄. 선지는 (가)(나)(다) 열 머리 + 5행 표(PDF 에는 열 순서로 찍힘 → 쪽에서 오려 그림, choices_raster, 선지 글은 raster_text).
  열 머리 (가)(나)(다) 에 밑줄이 그림 속에 있다. 옛한글·PUA 없음.
"""
import json
import re

HERE = r"D:\Work\블로그\리딩맵\작업\20240328-go3-korB"
d = json.load(open(HERE + r"\초안_37-39.json", encoding="utf-8"))
d.pop("raw_passage_lines", None)
d["guide"] = None
d["range"] = [37, 39]
d["meta"] = {"exam": "2024학년도 3월 고3 전국연합학력평가 국어(언어와 매체)", "exam_id": "20240328-go3-korB",
             "area": "문법", "topic": "음운 변동·합성어의 의미 관계·관형사절",
             "problem_pdf": "20240328-go3-problem-korB_mun_HE53W32S.pdf",
             "explanation_pdf": "20240328-go3-explanation-korB_hsj_JP141445.pdf"}
Q = {q["no"]: q for q in d["questions"]}
CIR = "①②③④⑤"

# ---- 37번
s = Q[37]["stem"]
Q[37]["stem"] = s[: s.index("?") + 1]
assert Q[37]["stem"] == "<학습 활동>을 수행한 결과로 적절한 것은?"
bx = s[len(Q[37]["stem"]):]
assert bx.startswith("< 학습 활동 >")
bx = bx[len("< 학습 활동 >"):]
ta = bx[: bx.index("생각해 보자.") + len("생각해 보자.")]
rest = bx[len(ta):]
w1 = "흙화덕[흐콰덕], 드넓다[드널따]"
w2 = "끊겼다[끈켣따], 겉치레[걷치레]"
assert rest.startswith(w1 + w2), rest
rest = rest[len(w1 + w2):]
bul = [x for x in re.split(r"(?=◦)", rest) if x]
assert len(bul) == 4, bul
c5 = Q[37]["choices"][4]
Q[37]["choices"][4] = c5[: c5.index("단팥죽[단팓쭉]") + len("단팥죽[단팓쭉]")]
blocks = [{"id": "b1", "type": "para", "text": ta, "underlines": []},
          {"id": "w1", "type": "para", "text": w1, "underlines": [], "inbox": "낱말", "center": True},
          {"id": "w2", "type": "para", "text": w2, "underlines": [], "inbox": "낱말", "center": True}]
for k, b in enumerate(bul):
    blocks.append({"id": f"d{k+1}", "type": "para", "text": b, "underlines": []})
Q[37]["bogi"] = {"label": "학습 활동", "blocks": blocks}

# ---- 38번
s = Q[38]["stem"]
Q[38]["stem"] = s[: s.index("?") + 1]
assert Q[38]["stem"] == "<보기>를 읽고 이해한 내용으로 적절하지 않은 것은?"
Q[38]["stem_underlines"] = ["않은"]
bx = s[len(Q[38]["stem"]):]
assert bx.startswith("< 보 기 >")
bx = bx[len("< 보 기 >"):]
t1 = bx[: bx.index("있다.", bx.index("한편")) + len("있다.")]
ex = bx[len(t1):]
exs38 = [x for x in re.split(r"(?=[ㄱ-ㅁ]\. )", ex) if x]
assert len(exs38) == 5, exs38
UL38 = [("㉮", "두 어근이 대등하게 결합하는 것"), ("㉯", "한 어근이 다른 어근을 수식하는 것"),
        ("㉰", "각각의 어근이 원래 지닌 의미와는 다른 새로운 의미를 가지는 것")]
for m, t in UL38:
    assert (m + t) in t1, m
b38 = [{"id": "b1", "type": "para", "text": t1, "underlines": [{"mark": m, "text": t} for m, t in UL38]}]
for k, e in enumerate(exs38):
    b38.append({"id": f"e{k+1}", "type": "para", "text": e, "underlines": []})
Q[38]["bogi"] = {"label": "보 기", "blocks": b38}

# ---- 39번
s = Q[39]["stem"]
Q[39]["stem"] = s[: s.index("?") + 1]
bx = s[len(Q[39]["stem"]):]
assert bx.startswith("< 보 기 >")
bx = bx[len("< 보 기 >"):]
ta = bx[: bx.index("봅시다.") + len("봅시다.")]
assert ta.startswith("선생님: 관형사절은")
r = bx[len(ta):]
flow = r[: r.index("(다)") + 3]
assert flow == "안긴문장이 안은문장에서 관형어의 기능을 하는가?→아니요(가)↓예안긴문장에 생략된 성분이 있는가?→아니요(나)↓예(다)", flow
r = r[len(flow):]
assert r.startswith("[자료]")
r = r[len("[자료]"):]
ex = r[: r.index("몰랐다.") + len("몰랐다.")]
tail = r[len(ex):]
assert tail == "(가)(나)(다)", tail
exs39 = [x for x in re.split(r"(?=[ㄱ-ㅂ]\. )", ex) if x]
assert len(exs39) == 6, exs39
FLOW_ALT = ("흐름도. 첫째 칸 ‘안긴문장이 안은문장에서 관형어의 기능을 하는가?’에서 ‘아니요’ 쪽은 (가). ‘예’ 쪽은 둘째 칸 ‘안긴문장에 생략된 성분이 있는가?’. "
            "둘째 칸에서 ‘아니요’ 쪽은 (나), ‘예’ 쪽은 (다).")
b39 = [{"id": "b1", "type": "para", "dialogue": True, "text": ta, "bold": ["선생님"], "underlines": []},
       {"id": "ff", "type": "figure", "caption": "", "image": "그림_37-39_39_흐름도.png", "pdf_text": flow, "raster_text": "", "alt": FLOW_ALT},
       {"id": "b2", "type": "para", "text": "[자료]", "bold": ["[자료]"], "underlines": []}]
for k, e in enumerate(exs39):
    b39.append({"id": f"e{k+1}", "type": "para", "text": e, "underlines": []})
cc = Q[39]["choices"]
rows = ["ㄱ, ㄴ ㄹ, ㅂ ㄷ, ㅁ", "ㄱ, ㄷ ㄴ, ㅁ ㄹ, ㅂ", "ㄴ, ㅁ ㄹ, ㅂ ㄱ, ㄷ", "ㄴ, ㅂ ㄷ, ㄹ ㄱ, ㅁ", "ㄹ, ㅁ ㄴ, ㅂ ㄱ, ㄷ"]
for c, rw in zip(cc, rows):
    assert re.sub(r"\s", "", c) == re.sub(r"\s", "", rw), (c, rw)
RT = "(가) (나) (다) " + " ".join(f"{CIR[k]} {rw}" for k, rw in enumerate(rows))
Q[39]["bogi"] = [
    {"label": "보 기", "blocks": b39},
    {"label": "", "plain": True, "figure": {
        "id": "cf", "type": "figure", "caption": "", "image": "그림_37-39_39_선지표.png",
        "pdf_text": "(가)(나)(다)" + "".join(CIR[k] + cc[k] for k in range(5)), "raster_text": RT,
        "alt": "열 머리 (가) (나) (다), 5행 표. ① ㄱ, ㄴ / ㄹ, ㅂ / ㄷ, ㅁ. ② ㄱ, ㄷ / ㄴ, ㅁ / ㄹ, ㅂ. ③ ㄴ, ㅁ / ㄹ, ㅂ / ㄱ, ㄷ. ④ ㄴ, ㅂ / ㄷ, ㄹ / ㄱ, ㅁ. ⑤ ㄹ, ㅁ / ㄴ, ㅂ / ㄱ, ㄷ. 열 머리 (가) (나) (다)에 밑줄이 있다."}}]
Q[39]["choices"] = rows
Q[39]["choices_raster"] = True
Q[39]["table_border"] = True
for q in d["questions"]:
    assert len(q["choices"]) == 5, q["no"]


# ---- 해설지
def sq(s):
    return re.sub(r"[\s\u200b]+", "", s)


_all = open(HERE + r"\해설_글자.txt", encoding="utf-8").read().split("\n")
i0 = [i for i, x in enumerate(_all) if x.startswith("37. [출제의도]")][-1]
i1 = [i for i, x in enumerate(_all) if x.startswith("40. [출제의도]")][-1]
_cl, skip = [], False
for x in _all[i0:i1]:
    if x.startswith("=== 해설"):
        skip = True
        continue
    if skip:
        skip = False
        if re.fullmatch(r"\d+", x.strip()):
            continue
    _cl.append(x)
EXPL = sq("\n".join(_cl))


def E(start, end):
    a, b = sq(start), sq(end)
    i = EXPL.index(a)
    return EXPL[i: EXPL.index(b, i) + len(b)]


def J(choice, verdict, ans, ev, basis, reason, xq=None):
    out = {"choice": choice, "verdict": verdict, "is_answer": ans, "basis": basis, "reason": reason,
           "evidence": [{"source": "bogi", "para": None, "quote": q} for q in ev]}
    if xq:
        out["explanation_quote"] = xq
    return out


# ======== 37번 (정답 ④)
D1 = [b.lstrip("◦") for b in bul]
Q[37]["answer"] = 4
Q[37]["judgments"] = [
    J(1, "부적절", False, [D1[0], D1[1]], "자체",
      "㉠은 자음군 단순화, ㉡은 거센소리되기이다. ‘밝히다[발키다]’에는 거센소리되기(㉡)만 일어나고 자음군 단순화(㉠)는 일어나지 않는다."),
    J(2, "부적절", False, [D1[0], D1[2]], "자체",
      "㉠은 자음군 단순화, ㉢은 음절의 끝소리 규칙이다. ‘닭고기[닥꼬기]’에는 자음군 단순화(㉠)와 된소리되기(㉣)가 일어나므로 ㉠, ㉢의 예가 아니다."),
    J(3, "부적절", False, [D1[0], D1[3]], "자체",
      "㉠은 자음군 단순화, ㉣은 된소리되기이다. ‘깎고서[깍꼬서]’에는 음절의 끝소리 규칙(㉢)과 된소리되기(㉣)가 일어나므로 ㉠, ㉣의 예가 아니다."),
    J(4, "적절", True, [D1[1], D1[2]], "해설지",
      "‘숱하다[수타다]’는 음절의 끝소리 규칙(㉢)과 거센소리되기(㉡)가 일어나므로 ㉡, ㉢이 모두 일어난 예이다.",
      E("㉠은 자음군 단순화, ㉡은 거센소리되기", "예로 적절하다.")),
    J(5, "부적절", False, [D1[1], D1[3]], "자체",
      "㉡은 거센소리되기, ㉣은 된소리되기이다. ‘단팥죽[단팓쭉]’에는 음절의 끝소리 규칙(㉢)과 된소리되기(㉣)가 일어나므로 ㉡, ㉣의 예가 아니다."),
]

# ======== 38번 (정답 ②, 적절하지 않은 것)
X = [e.strip() for e in exs38]
Q[38]["answer"] = 2
Q[38]["judgments"] = [
    J(1, "적절", False, [X[0], "두 어근이 대등하게 결합하는 것이 있고"], "자체",
      "‘논밭’은 ‘논’과 ‘밭’이 대등하게 결합한 합성어이므로 ㉮에 해당한다."),
    J(2, "부적절", True, [X[1], "두 어근이 대등하게 결합하는 것이 있고"], "해설지",
      "‘보리밥’은 앞의 어근 ‘보리’가 뒤의 어근 ‘밥’을 수식하는 합성어이므로 ㉯에 해당한다. 두 어근이 대등하게 결합한 ㉮라는 이해는 적절하지 않다.",
      E("‘보리밥’은 앞의 어근", "적절하지 않다.")),
    J(3, "적절", False, [X[2], "한 어근이 다른 어근을 수식하는 것도 있다"], "자체",
      "‘돌다리’는 앞의 어근 ‘돌’이 뒤의 어근 ‘다리’를 수식하는 합성어이므로 ㉯에 해당한다."),
    J(4, "적절", False, [X[3], "한 어근이 다른 어근을 수식하는 것도 있다"], "자체",
      "‘길바닥’은 앞의 어근 ‘길’이 뒤의 어근 ‘바닥’을 수식하는 합성어이므로 ㉯에 해당한다."),
    J(5, "적절", False, [X[4], "각각의 어근이 원래 지닌 의미와는 다른 새로운 의미를 가지는 것도 있다"], "자체",
      "‘피땀’은 ‘피’와 ‘땀’의 의미와 다른 새로운 의미를 가지는 합성어이므로 ㉰에 해당한다."),
]

# ======== 39번 (정답 ③, 바르게 짝지은 것)
Y = [e.strip() for e in exs39]
Q[39]["answer"] = 3
Q[39]["judgments"] = [
    J(1, "부적절", False, [Y[0]], "자체",
      "(가)에 ㄱ을 넣을 수 없다. ㄱ은 관형사절을 안은 문장이므로 안긴문장이 관형어 기능을 하여 (가)가 아니다."),
    J(2, "부적절", False, [Y[2]], "자체",
      "(가)에 ㄷ을 넣을 수 없다. ㄷ은 관형사절을 안은 문장이므로 안긴문장이 관형어 기능을 하여 (가)가 아니다."),
    J(3, "적절", True, [Y[1], Y[4]], "해설지",
      "ㄴ은 명사절, ㅁ은 인용절을 안은 문장이라 (가)이고, ㄹ과 ㅂ은 생략된 성분이 없는 관형사절을 안은 문장이라 (나)이며, ㄱ과 ㄷ은 생략된 성분이 있는 관형사절을 안은 문장이라 (다)이다.",
      E("ㄴ은 명사절을 안은 문장", "분류할 수 있다.")),
    J(4, "부적절", False, [Y[5]], "자체",
      "(가)에 ㅂ을 넣을 수 없다. ㅂ은 관형사절을 안은 문장이므로 안긴문장이 관형어 기능을 하여 (가)가 아니다."),
    J(5, "부적절", False, [Y[3]], "자체",
      "(가)에 ㄹ을 넣을 수 없다. ㄹ은 관형사절을 안은 문장이므로 안긴문장이 관형어 기능을 하여 (가)가 아니다."),
]

json.dump(d, open(HERE + r"\세트_37-39.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("세트_37-39.json 씀")
