"""2024-03-28 고3 언어와 매체(korB) 35~36번 세트: 초안 + 쪽 그림 확인값 + 해설지 기반 판단 → 세트_35-36.json

확인한 것(문제_13쪽 그림·PDF 텍스트층·선·글꼴):
- [35 ~ 36] 안내문 + 글(문단 3개: 단어의 품사를 / 한 단어가 두 가지 / ⓐ중세 국어와). 글은 네모 상자 안(알려진 화면 한계).
- 지문 굵은 글씨 없음(type=1 은 문항 번호 35.·36. 뿐). 발문 밑줄 없음.
- 지문 밑줄 ⓐⓑⓒ(PDF 선 확인, 6줄). 세 번째 문단 p3 은 옛한글 PUA(ᄅᆞᆯ, ᄆᆞᆮ)가 있어 문단 그림을 display_image 로 쓴다.
- 35번 <보기> 밑줄 6개(이·크는·둘 / 큰·여러·반, PDF 선). 마크 ㉠~㉥ 는 밑줄 밖.
- 36번 <자료> 는 옛한글 PUA 가 많아 표 전체를 그림으로, 글자는 pdf_text 에 둔다. 선지 ③④ 안 PUA 는 choice_images.
- 36번 선지에는 PDF 밑줄 없음.
"""
import json
import re

HERE = r"D:\Work\블로그\리딩맵\작업\20240328-go3-korB"
d = json.load(open(HERE + r"\초안_35-36.json", encoding="utf-8"))
d.pop("raw_passage_lines", None)
d["meta"] = {"exam": "2024학년도 3월 고3 전국연합학력평가 국어(언어와 매체)", "exam_id": "20240328-go3-korB",
             "area": "문법", "topic": "품사 분류와 중세 국어의 품사",
             "problem_pdf": "20240328-go3-problem-korB_mun_HE53W32S.pdf",
             "explanation_pdf": "20240328-go3-explanation-korB_hsj_JP141445.pdf"}
Q = {q["no"]: q for q in d["questions"]}

# ---- 지문
P = {p["id"]: p for p in d["passage"]}
for p in d["passage"]:
    p.setdefault("underlines", [])
t3 = P["p3"]["text"]
for mark, txt in [("ⓐ", "중세 국어와 현대 국어에서 대응하는 단어의 품사가 같은 경우"),
                  ("ⓑ", "중세 국어와 현대 국어에서 대응하는 단어가 쓰일 수 있는 품사가 다른 경우"),
                  ("ⓒ", "중세 국어에서는 단어였지만 현대 국어에서는 품사 분류의 대상에서 제외되는 경우")]:
    assert mark + txt in t3, mark
    P["p3"]["underlines"].append({"mark": mark, "text": txt})
P["p3"]["display_image"] = "그림_35-36_p3.png"

# ---- 35번
s35 = Q[35]["stem"]
i = s35.index("< 보 기 >")
bt = s35[i + len("< 보 기 >"):]
Q[35]["stem"] = s35[:i].strip()
bl = [x for x in re.split(r"(?=◦)", bt) if x]
assert len(bl) == 2, bl
Q[35]["bogi"] = {"label": "보 기", "blocks": [
    {"id": "b1", "type": "para", "text": bl[0], "underlines": [
        {"mark": "㉠", "text": "이"}, {"mark": "㉡", "text": "크는"}, {"mark": "㉢", "text": "둘"}]},
    {"id": "b2", "type": "para", "text": bl[1], "underlines": [
        {"mark": "㉣", "text": "큰"}, {"mark": "㉤", "text": "여러"}, {"mark": "㉥", "text": "반"}]}]}

# ---- 36번
s36 = Q[36]["stem"]
j = s36.index("< 자 료 >")
jaryo = s36[j + len("< 자 료 >"):]
Q[36]["stem"] = s36[:j].replace("[3점]", "").strip()
Q[36]["bogi"] = {"label": "자 료", "figure": {
    "id": "bf1", "type": "figure", "caption": "", "image": "그림_35-36_36_자료.png", "pdf_text": jaryo,
    "alt": "자료 (가)~(마). 각 줄은 중세 국어 문장과 괄호 속 형태 분석, 이어서 현대어 풀이이다. (가) 어늬(어느+ㅣ) 解脫이 아니리오 / 어느 것이 해탈이 아니리오. (나) 기피(깊-+-이) 잇는 龍이 소리 업고 / 깊이 있는 용이 소리 없고. (다) 窓ᄋ로 여서(엿-+-어) / 창으로 엿보아. (라) ᄂᆞᄅᆞᆯ(ᄂᆞᆯ+ᄋᆞᆯ) 사흐라 / 날것을 썰어. (마) 니르고져 홇 배(바+ㅣ) 이셔도 / 이르고자 할 바가 있어도."}}
c5 = Q[36]["choices"][4]
Q[36]["choices"][4] = c5[: c5.index("명사로 분류할 수 있다.") + len("명사로 분류할 수 있다.")]
Q[36]["choices"] = Q[36]["choices"][:5]
for k, c in enumerate(Q[36]["choices"]):
    print(k + 1, [hex(ord(x)) for x in c if "\ue000" <= x <= "\uf8ff"])
Q[36]["choice_images"] = {
    "3": [{"text": "\uedf5", "image": "그림_35-36_36_선지3.png", "alt": "중세 국어 동사 어간 ‘엿-’(옛 글자 ㅿ 받침)"}],
    "4": [{"text": "\ue288", "image": "그림_35-36_36_선지4.png", "alt": "중세 국어 명사 ‘ᄂᆞᆯ’(날것)"}]}
for q in d["questions"]:
    assert len(q["choices"]) == 5, q["no"]


# ---- 해설지 인용 도우미(공백 무시)
def sq(s):
    return re.sub(r"[\s\u200b]+", "", s)


_all = open(HERE + r"\해설_글자.txt", encoding="utf-8").read().split("\n")
i0 = [i for i, x in enumerate(_all) if x.startswith("35. [출제의도]")][-1]
i1 = [i for i, x in enumerate(_all) if x.startswith("37. [출제의도]")][-1]
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
    s, e = sq(start), sq(end)
    i = EXPL.index(s)
    j = EXPL.index(e, i) + len(e)
    return EXPL[i:j]


def J(choice, verdict, ans, ev, basis, reason, xq=None):
    out = {"choice": choice, "verdict": verdict, "is_answer": ans, "basis": basis, "reason": reason, "evidence": []}
    for e in ev:
        if e[0] == "figure":
            out["evidence"].append({"source": "figure", "fig": e[1], "quote": e[2]})
        else:
            out["evidence"].append({"source": e[0], "para": e[1], "quote": e[2]})
    if xq:
        out["explanation_quote"] = xq
    return out


def Pp(para, quote):
    return ("passage", para, quote)


def F(quote):
    return ("figure", "bf1", quote)


# ======== 35번 (정답 ①, 적절한 것)
Q[35]["answer"] = 1
Q[35]["judgments"] = [
    J(1, "적절", True, [Pp("p2", "‘열 명이 왔다.’에서 ‘열’은 관형사인 ‘한’이나 ‘두’와 같이, 뒤에 오는 체언을 꾸며 주고 조사와 결합하지 않는다는 점에서 관형사로 분류하는 것이 일반적이다.")], "해설지",
      "㉠ ‘이’와 ㉤ ‘여러’는 모두 뒤에 오는 체언을 꾸며 주고 조사와 결합하지 않는 관형사이다.",
      E("㉠, ㉤은 관형사로서", "결합하지 않는다.")),
    J(2, "부적절", False, [Pp("p1", "하지만 ‘이것’은 대명사로서 말하는 이에게 가까이 있는 어떤 사물이든 대신할 수 있는 반면에, ‘나머지’는 명사로서 ‘어떤 한도에 차고 남은 부분’이라는 의미를 일정하게 가지고 있다.")], "해설지",
      "㉠ ‘이’는 관형사이고 ㉥ ‘반’은 명사이므로 같은 품사로 분류할 수 없다.",
      E("㉠은 관형사이고", "명사이다.")),
    J(3, "부적절", False, [Pp("p2", "하지만 ‘그는 약속 시간에 항상 늦는다.’에서는 어간 ‘늦-’에 어미 ‘-는-’이 결합하여 전형적인 동사의 특성이 나타난다.")], "해설지",
      "㉡ ‘크는’에는 어미 ‘-는’이, ㉣ ‘큰’에는 어미 ‘-ㄴ’이 결합하여 어미의 형태가 서로 다르다.",
      E("㉡은 어간에 어미", "결합하였다.")),
    J(4, "부적절", False, [Pp("p2", "다른 사례로 ‘열’은 조사와 결합할 수 있으며, 정확한 수량을 나타내므로 수사로만 분류하기 쉽다.")], "자체",
      "㉢ ‘둘’은 조사 ‘이’와 결합하며 수량을 나타내는 수사이지만, ㉥ ‘반’은 명사이므로 같은 품사로 분류할 수 없다."),
    J(5, "부적절", False, [Pp("p1", "하지만 ‘길게’는 ‘길-’에 어미 ‘-게’가 결합한 형용사의 활용형이고, ‘길이’는 ‘같이’, ‘깨끗이’처럼 ‘길-’에 부사 파생 접미사 ‘-이’가 결합하여 만들어진 부사이다.")], "자체",
      "㉣ ‘큰’은 어간에 어미 ‘-ㄴ’이 결합한 형용사의 활용형이고, ㉤ ‘여러’는 어미가 결합하지 않는 관형사이므로 같은 품사가 아니다."),
]

# ======== 36번 (정답 ④, 적절한 것)
Q[36]["answer"] = 4
Q[36]["judgments"] = [
    J(1, "부적절", False, [Pp("p2", "뒤에 오는 체언을 꾸며 주고 조사와 결합하지 않는다는 점에서 관형사로 분류하는 것이 일반적이다."),
                           F("[현대어 풀이: 어느 것이 해탈이 아니리오]")], "해설지",
      "중세 국어의 ‘어느’는 조사 ‘ㅣ’와 결합하므로 조사와 결합하지 않는 관형사가 아니다. 따라서 ⓐ의 사례가 아니다.",
      E("(가)에서 중세 국어의 ‘어느’는 조사", "알 수 있다.")),
    J(2, "부적절", False, [Pp("p1", "‘길이’는 ‘같이’, ‘깨끗이’처럼 ‘길-’에 부사 파생 접미사 ‘-이’가 결합하여 만들어진 부사이다."),
                           F("[현대어 풀이: 깊이 있는 용이 소리 없고]")], "해설지",
      "중세 국어의 ‘기피’는 ‘깊-’에 부사 파생 접미사 ‘-이’가 결합한 부사이다. 현대 국어의 ‘깊이’와 품사가 같으므로 ⓑ가 아니라 ⓐ의 사례이다.",
      E("(나)에서 중세 국어의 ‘기피’", "부사이다.")),
    J(3, "부적절", False, [Pp("p3", "이처럼 ⓑ중세 국어와 현대 국어에서 대응하는 단어가 쓰일 수 있는 품사가 다른 경우도 있다."),
                           F("[현대어 풀이: 창으로 엿보아]")], "자체",
      "현대 국어의 ‘엿-’은 접사라서 품사 분류의 대상에서 제외된다. 중세 국어에서는 단어였지만 현대 국어에서는 제외되는 경우이므로 ⓑ가 아니라 ⓒ의 사례이다."),
    J(4, "적절", True, [Pp("p3", "접사 ‘맏-’이 된 것처럼 ⓒ중세 국어에서는 단어였지만 현대 국어에서는 품사 분류의 대상에서 제외되는 경우도 있다."),
                        F("[현대어 풀이: 날것을 썰어]")], "해설지",
      "중세 국어의 ‘ᄂᆞᆯ’은 조사 ‘ᄋᆞᆯ’과 결합하고 ‘날것’이라는 의미를 지닌 명사이다. 현대 국어에서는 접사 ‘날-’이 되므로 ⓒ의 사례이다.",
      E("따라서 현대 국어의 접사 ‘날-’과", "알 수 있다.")),
    J(5, "부적절", False, [Pp("p3", "중세 국어와 현대 국어에서 대응하는 단어의 품사가 같은 경우가 많다."),
                           F("[현대어 풀이: 이르고자 할 바가 있어도]")], "자체",
      "중세 국어의 ‘바’는 조사 ‘ㅣ’와 결합하는 명사이고 현대 국어의 ‘바’도 명사이므로 품사가 같다. 따라서 ⓒ가 아니라 ⓐ의 사례이다."),
]

json.dump(d, open(HERE + r"\세트_35-36.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("세트_35-36.json 씀")
