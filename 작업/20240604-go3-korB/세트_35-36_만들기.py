"""2024-06 고3 모의평가(2025학년도 6월) 언어와 매체(korB) 35~36번 세트: 초안 + 쪽 그림 확인값 + 해설지 기반 판단 → 세트_35-36.json

확인한 것(2026-11-25, 문제_13쪽.png, PDF 텍스트층·선·글꼴):
- 구성: [35 ~ 36] 안내문 + 글(문단 4개, 모두 첫 줄 들여쓰기 x 106.7). 글은 네모 상자 안(알려진 화면 한계). 굵은 글씨·옛한글 없음.
- 글 밑줄 ㉠~㉤은 PDF 선(기호 뒤 글자부터). ㉡은 «있다» 까지(마침표 제외), ㉤은 «있는데» 까지.
- 35번 <보기> 밑줄 ⓐ얼마 ⓑ무슨 ⓒ언제 ⓓ어떤. 발문에 밑줄 없음(적절한 것).
- 36번 발문 [3점], 발문에 밑줄 없음. 대화 상자: 말한 이 이름(아들·엄마·딸·아빠)은 태고딕 글꼴(굵음), 콜론은 신명조(보통).
  밑줄 ㉮엄마 ㉯이모 ㉰여보세요. ㉱김 선생님 ㉲김수진 님 ㉳이모님(PDF 선, 기호 뒤 글자부터).
"""
import json
import re

HERE = r"D:\Work\블로그\리딩맵\작업\20240604-go3-korB"
d = json.load(open(HERE + r"\초안_35-36.json", encoding="utf-8"))
d.pop("raw_passage_lines", None)
d["guide"] = "[35 ~ 36] 다음 글을 읽고 물음에 답하시오."
d["range"] = [35, 36]
d["meta"] = {"exam": "2025학년도 6월 고3 모의평가 국어", "exam_id": "20240604-go3-korB",
             "area": "문법", "topic": "지칭어와 호칭어",
             "problem_pdf": "20240604-go3-problem-korB_mun_BARMEM1B.pdf",
             "explanation_pdf": "20240604-go3-explanation-korB_hsj_PV487SE9_3.pdf"}
Q = {q["no"]: q for q in d["questions"]}
P = {p["id"]: p for p in d["passage"]}
for p in d["passage"]:
    p.setdefault("underlines", [])

# ---- 지문 밑줄
P["p1"]["underlines"] = [{"mark": "㉠", "text": "사람이나 사물 등을 가리켜 이를 때 사용되는 말은 지칭어, 그 대상을 부르는 말은 호칭어라고 한다."}]
P["p3"]["underlines"] = [
    {"mark": "㉡", "text": "‘홍길동’과 친족 관계에 있는 사람이라면 그를 ‘길동이, 삼촌, 아빠’ 등으로 이르거나 부를 수 있다"},
    {"mark": "㉢", "text": "공적 관계에 있고 격식적인 대화 상황이라면 그 대상을 공적인 직위나 지위 등을 사용하여 이르거나 부르는 것이 일반적이다."},
    {"mark": "㉣", "text": "앞서 언급한 ‘홍길동’이 ‘이사’란 직위에 있다면 그를 ‘홍 이사, 홍길동 이사님’ 등으로 이르거나 부를 수 있다."},
    {"mark": "㉤", "text": "특수한 의도를 가지고 지칭어나 호칭어를 사용하는 경우도 있는데"},
]

# ---- 35번
s35 = Q[35]["stem"]
Q[35]["stem"] = s35[: s35.index("?") + 1]
bg = s35[s35.index("<보 기>") + len("<보 기>"):]
items = [x for x in re.split(r"(?=◦)", bg) if x]
assert len(items) == 4, items
UL35 = ["얼마", "무슨", "언제", "어떤"]
MK = "ⓐⓑⓒⓓ"
Q[35]["bogi"] = {"label": "< 보 기 >", "blocks": [
    {"id": f"b{k+1}", "type": "para", "text": t, "underlines": [{"mark": MK[k], "text": UL35[k]}]} for k, t in enumerate(items)]}
for k, t in enumerate(items):
    assert (MK[k] + UL35[k]) in t

# ---- 36번
s36 = Q[36]["stem"]
j = s36.index("[3점]")
Q[36]["stem"] = s36[:j].strip()
turns = [x.strip() for x in re.split(r"(?=(?:아들|엄마|딸|아빠): )", s36[j + len("[3점]"):]) if x.strip()]
assert len(turns) == 7, turns
UL36 = {"㉮": "엄마", "㉯": "이모", "㉰": "여보세요.", "㉱": "김 선생님", "㉲": "김수진 님", "㉳": "이모님"}
b36 = []
for k, t in enumerate(turns):
    uls = [{"mark": m, "text": UL36[m]} for m in UL36 if m in t]
    for u in uls:
        assert (u["mark"] + u["text"]) in t, u
    b36.append({"id": f"b{k+1}", "type": "para", "dialogue": True, "text": t, "underlines": uls, "bold": [t.split(":")[0]]})
assert sum(len(b["underlines"]) for b in b36) == 6
Q[36]["bogi"] = {"label": "", "blocks": b36}
c5 = Q[36]["choices"][4]
Q[36]["choices"] = Q[36]["choices"][:4] + [c5[: c5.index("확인된다.") + len("확인된다.")]]
for q in d["questions"]:
    assert len(q["choices"]) == 5, q["no"]
    assert q["stem"], q["no"]


# ---- 해설지
def clean(lines):
    out, skip = [], False
    for l in lines:
        if re.match(r"^=== 해설 \d+쪽 ===$", l):
            skip = True
            continue
        if skip:
            skip = False
            continue
        out.append(l)
    return "".join(out)


LN = open(HERE + r"\해설_글자.txt", encoding="utf-8").read().split("\n")
i0 = next(i for i, l in enumerate(LN) if l.startswith("35. 품사의 특성"))
i1 = next(i for i, l in enumerate(LN) if l.startswith("37. 서술어의 자릿수"))
EXPL = clean(LN[i0:i1])
SQ = lambda s: re.sub(r"\s+", "", s)


def E(start, end):
    """해설지 글(공백 포함)에서 start~end 를 글자 그대로 잘라 온다."""
    i = EXPL.index(start)
    return EXPL[i: EXPL.index(end, i) + len(end)]


def J(choice, verdict, ans, ev, basis, reason, xq=None):
    out = {"choice": choice, "verdict": verdict, "is_answer": ans, "basis": basis, "reason": reason, "evidence": []}
    for e in ev:
        if e[0] == "bogi":
            out["evidence"].append({"source": "bogi", "para": None, "quote": e[1]})
        else:
            out["evidence"].append({"source": "passage", "para": e[1], "quote": e[2]})
    if xq:
        out["explanation_quote"] = xq
    return out


def B(q):
    return ("bogi", q)


def PQ(pid, q):
    assert q in P[pid]["text"], q
    return ("passage", pid, q)


bq35 = {k: items[i].lstrip("◦") for i, k in enumerate("abcd")}
BA, BB, BC, BD = (bq35[k] for k in "abcd")
S_MI = "이들은 다시, 대상을 알지 못하는 미지칭과 대상이 정해지지 않아 불분명한 부정칭으로 나뉜다."
S_EX = "‘너희 학교는 어디야?’의 ‘어디’는 전자에, ‘어디 좀 가자.’의 ‘어디’는 후자에 해당된다."
S_POS = "이러한 대명사 외에 명사, 관형사, 부사 등도 알지 못함이나 불분명함을 나타낼 수 있다."
S_BOTH = "‘어디 가?’의 ‘어디’는 맥락에 따라 전자와 후자 모두 가능하다."

Q[35]["answer"] = 4
Q[35]["judgments"] = [
    J(1, "부적절", False, [B(BA), B(BB), PQ("p4", S_MI)], "해설지",
      "ⓐ ‘얼마’는 대상을 알지 못함을 나타내는 명사이고, ⓑ ‘무슨’은 대상이 정해지지 않아 불분명함을 나타내는 관형사이다. ⓐ가 불분명함을 나타낸다는 설명이 틀리다.",
      E("ⓐ의 ‘얼마’는", "관형사이다.")),
    J(2, "부적절", False, [B(BA), B(BC), PQ("p4", S_EX)], "해설지",
      "ⓐ ‘얼마’는 알지 못함을 나타내는 명사이고, ⓒ ‘언제’는 불분명함을 나타내는 부사이다. 둘은 나타내는 것도 품사도 다르다.",
      E("ⓐ의 ‘얼마’는", "ⓒ의 ‘언제’는 대상이 정해지지 않아 불분명함을 나타내며 부사이다.")),
    J(3, "부적절", False, [B(BA), B(BD), PQ("p4", S_BOTH)], "해설지",
      "ⓐ ‘얼마’는 명사이고, ⓓ ‘어떤’은 맥락에 따라 알지 못함과 불분명함을 모두 나타내는 관형사이다. 품사가 동일하다는 설명이 틀리다.",
      E("ⓐ의 ‘얼마’는", "ⓓ의 ‘어떤’은 맥락에 따라 대상을 알지 못하거나 대상이 정해지지 않아 불분명함을 나타내며 관형사이다.")),
    J(4, "적절", True, [B(BB), B(BC), PQ("p4", S_POS)], "해설지",
      "ⓑ ‘무슨’은 불분명함을 나타내는 관형사이고, ⓒ ‘언제’는 불분명함을 나타내는 부사이다. 둘 다 불분명함을 나타내며 품사는 서로 다르다.",
      E("따라서 ⓑ, ⓒ는", "서로 다르다.")),
    J(5, "부적절", False, [B(BB), B(BD), PQ("p4", S_BOTH)], "해설지",
      "ⓑ ‘무슨’은 불분명함만 나타내고 알지 못함은 나타내지 않는다. 알지 못함과 불분명함을 모두 나타내는 것은 ⓓ뿐이다.",
      E("ⓑ의 ‘무슨’은", "관형사이다.")),
]

tb = {k: turns[i] for i, k in enumerate(["a1", "m1", "d", "a2", "f1", "m2", "f2"])}
Q[36]["answer"] = 5
Q[36]["judgments"] = [
    J(1, "부적절", False, [B("㉮엄마, 진로 선택을 어떻게 해야 할지 모르겠어요."), B("㉲김수진 님!"), PQ("p1", "사람이나 사물 등을 가리켜 이를 때 사용되는 말은 지칭어, 그 대상을 부르는 말은 호칭어라고 한다.")], "해설지",
      "㉮는 아들이 엄마를 부르는 호칭어이고 ㉲는 아빠가 아내를 부르는 호칭어이다. 둘 다 호칭어이므로 지칭어 ㉲라는 설명이 틀리고, 같은 대상에 대한 호칭어가 화자와의 관계에 따라 달라지는 사례이다.",
      E("① ㉮는 ‘아들’이", "사례이다.")),
    J(2, "부적절", False, [B("㉯이모도 주말에 쉬셔야 하는데 괜찮을까요?"), B("㉳이모님께 감사 인사 꼭 드리고"), PQ("p3", "‘홍길동’과 친족 관계에 있는 사람이라면 그를 ‘길동이, 삼촌, 아빠’ 등으로 이르거나 부를 수 있다")], "해설지",
      "㉯와 ㉳은 화자와 대상의 친족 관계가 달라도 같은 친족어를 쓴 사례이다. 그러나 ㉳은 ㉯에 접미사 ‘-님’이 결합한 복합적 형식이어서 같은 형식으로 보기 어렵다.",
      E("② ㉡은 사적 관계에", "어렵다.")),
    J(3, "부적절", False, [B("㉲김수진 님! 본인 아드님 진로 상담은 충분히 알아본 다음에 하는 것이 어떨까요?"), PQ("p3", "공적 관계에 있고 격식적인 대화 상황이라면 그 대상을 공적인 직위나 지위 등을 사용하여 이르거나 부르는 것이 일반적이다.")], "해설지",
      "제시된 상황은 가족 간의 대화 장면이므로 공적이고 격식적인 상황이라고 보기 어렵다. 따라서 ㉲를 ㉢의 사례로 볼 수 없다.",
      E("③ 제시된 상황은", "어렵다.")),
    J(4, "부적절", False, [B("㉱김 선생님의 사생활도 생각 좀 하시죠?"), PQ("p3", "앞서 언급한 ‘홍길동’이 ‘이사’란 직위에 있다면 그를 ‘홍 이사, 홍길동 이사님’ 등으로 이르거나 부를 수 있다.")], "해설지",
      "㉣은 공적 관계의 격식적인 대화 상황에서 직위를 쓰는 사례인데 제시된 상황은 가족 간의 대화이다. 또 ㉱는 호칭어가 아니라 지칭어이다.",
      E("④ ㉣은 공적 관계에", "지칭어이다.")),
    J(5, "적절", True, [B("㉰여보세요."), PQ("p3", "특수한 의도를 가지고 지칭어나 호칭어를 사용하는 경우도 있는데")], "해설지",
      "‘여보세요.’는 가족 사이에, 특히 아들에게 일반적으로 쓸 표현이 아니다. ㉰에서는 아들의 생각에 주의를 주려는 특수한 의도로 상황에 어울리지 않는 호칭어를 쓰고 있다.",
      E("정답해설 : ‘여보세요.’는", "쓰고 있다.")),
]

json.dump(d, open(HERE + r"\세트_35-36.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("세트_35-36.json 씀")
