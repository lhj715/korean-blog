"""2024-04-30(PDF 표기 5월) 고3 언어와 매체(korB) 37~39번 세트(안내문 없는 단독 문항 묶음): 초안 + 쪽 그림 확인값 + 해설지 기반 판단 → 세트_37-39.json

확인한 것(2026-11-25, 문제_13쪽·14쪽 그림, PDF 텍스트층·선·글꼴, 600~1200dpi 확대):
- 37번 <보기>: 문단 1개(선생님: ...). «선생님:» 굵게(type 1, 콜론까지). 밑줄 ㉠안긴문장 ... 문장(두 줄에 걸친 선). 발문 밑줄 없음.
- 38번 <보기>: 첫 줄 «[예은, 세욱, 나라가 ...]»(굵지 않음) + 대화 9줄. 화자 이름과 콜론이 굵다(type 1). 밑줄 ㉠~㉨(기호 뒤 글자부터). 발문 밑줄 없음.
- 39번 <보기>: ⓐ~ⓔ 칸이 있는 표(옛한글 PUA 다수, 밑줄 10곳은 기호 없음). 표를 쪽에서 잘라 그림으로 넣고 글자는 pdf_text 에 둔다.
  선지 ①(-이-)·②(‘의’) 안에 PUA 글자가 하나씩 있어 choice_images 로 오려 낸 그림을 끼운다. 발문 «않은» 밑줄.
- 37번 ⑤ 뒤에 쪽 머리글('2024학년도 … 문제지', '제 1 교시', 쪽 번호)이 붙으므로 잘라 낸다.
- 38번 해설지는 ⑤ 만 설명한다. ①~④ 는 basis 자체.
"""
import json
import re

HERE = r"D:\Work\블로그\리딩맵\작업\20240430-go3-korB"
d = json.load(open(HERE + r"\초안_37-39.json", encoding="utf-8"))
d.pop("raw_passage_lines", None)
d["meta"] = {"exam": "2024학년도 5월 고3 전국연합학력평가 국어", "exam_id": "20240430-go3-korB",
             "area": "문법", "topic": "높임 표현·담화·중세 국어",
             "problem_pdf": "20240430-go3-problem-korB_mun_F32551Z1.pdf",
             "explanation_pdf": "20240430-go3-explanation-korB_hsj_2589O91H.pdf"}
d["guide"] = None
d["range"] = [37, 39]
d["passage"] = []
Q = {q["no"]: q for q in d["questions"]}

PUA = "[\ue000-\uf8ff]"


def sq(s):
    return re.sub(r"[\s\u200b]+", "", s)


# ---- 37번
s37 = Q[37]["stem"]
Q[37]["stem"] = s37[: s37.index("것은?") + 3]
b37 = s37[s37.index("것은?") + 3:]
assert b37.startswith("보 기선생님:"), b37[:10]
b37 = b37[len("보 기"):]
Q[37]["bogi"] = {"label": "보 기", "blocks": [{
    "id": "b1", "type": "para", "dialogue": True, "text": b37, "bold": ["선생님:"],
    "underlines": [{"mark": "㉠", "text": "안긴문장 내에서 특수 어휘를 통해 주체 높임을 표현하고 있는 문장"}]}]}
c5 = Q[37]["choices"][4]
Q[37]["choices"][4] = c5[: c5.index("드렸다.") + len("드렸다.")]

# ---- 38번
s38 = Q[38]["stem"]
Q[38]["stem"] = s38[: s38.index("것은?") + 3]
b38 = s38[s38.index("것은?") + 3:]
assert b38.startswith("보 기[예은")
b38 = b38[len("보 기"):]
title38 = "[예은, 세욱, 나라가 만나서 조별 과제를 하는 상황]"
assert b38.startswith(title38)
turns = [x.strip() for x in re.split(r"(?=(?:예은|나라|세욱): )", b38[len(title38):]) if x.strip()]
assert len(turns) == 9, turns
UL38 = {"㉠": "어제", "㉡": "우리", "㉢": "오늘", "㉣": "그거", "㉤": "너", "㉥": "지금", "㉦": "이거", "㉧": "너", "㉨": "우리"}
blocks38 = [{"id": "b1", "type": "para", "text": title38, "underlines": []}]
for k, t in enumerate(turns):
    sp = t.split(":")[0] + ":"
    uls = [{"mark": m, "text": UL38[m]} for m in UL38 if m in t]
    for u in uls:
        assert t.index(u["mark"]) + 1 == t.index(u["text"], t.index(u["mark"])), u
    blocks38.append({"id": f"b{k+2}", "type": "para", "dialogue": True, "text": t, "underlines": uls, "bold": [sp]})
assert sum(len(x["underlines"]) for x in blocks38) == 9
Q[38]["bogi"] = {"label": "보 기", "blocks": blocks38}

# ---- 39번
s39 = Q[39]["stem"]
Q[39]["stem"] = s39[: s39.index("것은?") + 3]
Q[39]["stem_underlines"] = ["않은"]
t39 = s39[s39.index("것은?") + 3:]
assert t39.startswith("보 기ⓐ")
t39 = t39[len("보 기"):]
assert re.search(PUA, t39)
Q[39]["bogi"] = {"label": "보 기", "figure": {
    "id": "bf1", "type": "figure", "caption": "", "image": "그림_37-39_39_보기표.png", "pdf_text": t39,
    "alt": "ⓐ~ⓔ 다섯 칸의 표. 칸마다 중세 국어 예문 두 개와 그 현대어 풀이가 있다. ⓐ 들의 새가 노래를 부른다 / 하늘의 사내아이가 있습니다, ⓑ 도적의 앞을 / 암탉이 아침에 울어, ⓒ 임금을 구하시고 / 종종 좋은 옷을 얻으며, ⓓ 마땅히 몸에 있느냐? / 구라제는 지금 어디 있느냐?, ⓔ 눈 먼 용이 눈을 뜨고 / 꿀같이 달고 빛이 희더니. 예문 속 일부 낱말에 밑줄이 있다."}}
c1, c2 = Q[39]["choices"][0], Q[39]["choices"][1]
assert [ch for ch in c1 if re.match(PUA, ch)] == ["\uf154"], c1
assert [ch for ch in c2 if re.match(PUA, ch)] == ["\ueea4"], c2
Q[39]["choice_images"] = {
    "1": [{"text": "\uf154", "image": "그림_37-39_39_선지1.png", "alt": "상대 높임 선어말 어미에 쓰인 옛 글자"}],
    "2": [{"text": "\ueea4", "image": "그림_37-39_39_선지2.png", "alt": "관형격 조사와 부사격 조사로 쓰인 옛 글자"}]}
for q in d["questions"]:
    assert len(q["choices"]) == 5, q["no"]

# ---- 해설지 인용 도우미
_all = open(HERE + r"\해설_글자.txt", encoding="utf-8").read().split("\n")
i0 = next(i for i, x in enumerate(_all) if x.startswith("37. [출제의도]"))
i1 = next(i for i, x in enumerate(_all) if x.startswith("40. [출제의도]"))
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


def E(start, end, lead=""):
    s, e = sq(start), sq(end)
    i = EXPL.index(s)
    assert EXPL[i - len(lead): i] == lead, (start, repr(EXPL[i - 3: i]))
    j = EXPL.index(e, i) + len(e)
    return EXPL[i - len(lead): j]


def J(choice, verdict, ans, ev, basis, reason, xq=None):
    out = {"choice": choice, "verdict": verdict, "is_answer": ans, "basis": basis, "reason": reason, "evidence": []}
    for e in ev:
        if e[0] == "figure":
            out["evidence"].append({"source": "figure", "fig": "bf1", "quote": e[1]})
        else:
            out["evidence"].append({"source": "bogi", "para": None, "quote": e[1]})
    if xq:
        out["explanation_quote"] = xq
    return out


def B(q):
    return ("bogi", q)


def F(q):
    return ("figure", q)


# ======== 37번 (정답 ③, 적절한 것)
Q[37]["answer"] = 3
Q[37]["judgments"] = [
    J(1, "부적절", False, [B("주체 높임과 객체 높임에서 특수 어휘로 높임 표현을 실현하는 방법에 대해 배웠습니다.")], "해설지",
      "안긴문장 ‘친척 어르신께 안부를 여쭙기’에는 특수 어휘 ‘여쭙다’가 쓰였지만, 높이는 대상이 객체인 ‘친척 어르신’이므로 주체 높임이 아니다.",
      E("안긴문장 ‘친척 어르신께 안부를 여쭙기’에서는", "적절하지 않다.")),
    J(2, "부적절", False, [B("안긴문장 내에서 특수 어휘를 통해 주체 높임을 표현하고 있는 문장")], "해설지",
      "안긴문장 ‘오랜만에 뵌’에는 특수 어휘 ‘뵈다’가 쓰였지만, 높이는 대상이 객체인 ‘은사님’이므로 주체 높임이 아니다.",
      E("안긴문장 ‘오랜만에 뵌’에서는", "적절하지 않다.")),
    J(3, "적절", True, [B("안긴문장 내에서 특수 어휘를 통해 주체 높임을 표현하고 있는 문장을 찾아봅시다.")], "해설지",
      "안긴문장 ‘고향에 계신’에서 특수 어휘 ‘계시다’로 주체인 ‘할머니’를 높이고 있으므로 조건에 맞다.",
      E("안긴문장 ‘고향에 계신’에서는", "적절하다.")),
    J(4, "부적절", False, [B("특수 어휘를 통해 주체 높임을 표현")], "해설지",
      "안긴문장 ‘머리가 하얗게 세신’은 주체인 ‘할아버지’를 높이지만, 특수 어휘가 아니라 선어말 어미 ‘-시-’를 썼다.",
      E("안긴문장 ‘머리가 하얗게 세신’에서는", "적절하지 않다.")),
    J(5, "부적절", False, [B("㉠안긴문장 내에서 특수 어휘를 통해")], "해설지",
      "안긴문장 ‘삼촌이 편하게 쉬시도록’은 주체인 ‘삼촌’을 높이지만, 특수 어휘가 아니라 선어말 어미 ‘-시-’를 썼다.",
      E("안긴문장 ‘삼촌이 편하게 쉬시도록’에서는", "적절하지 않다.")),
]

# ======== 38번 (정답 ⑤, 적절한 것) 해설지는 ⑤ 만 설명
Q[38]["answer"] = 5
Q[38]["judgments"] = [
    J(1, "부적절", False, [B("㉠어제 밤을 새웠더니"), B("나는 ㉢오늘까지 제출해야 할 과제가 더 있어서")], "자체",
      "㉠ ‘어제’와 ㉢ ‘오늘’은 둘 다 말하는 때에 따라 가리키는 날이 달라지는 말이므로, ㉠만 발화 시점과 관계없이 정해진다는 설명은 틀리다."),
    J(2, "부적절", False, [B("나는 ㉢오늘까지 제출해야 할 과제가 더 있어서 ㉣그거 준비하다가 못 잤어."), B("오늘은 자료 정리만 하면 되잖아."), B("예은이랑 내가 ㉦이거 마무리할게.")], "자체",
      "㉣ ‘그거’는 ㉢의 ‘오늘까지 제출해야 할 과제’를 가리키고, ㉦ ‘이거’는 ‘자료 정리’를 가리키므로 서로 다른 대상이다."),
    J(3, "부적절", False, [B("예은: 그랬구나. ㉤너 몸이 안 좋아 보이는데"), B("끝나고 연락할 테니까 ㉧너는 집에서 쉬고 있어.")], "자체",
      "㉤과 ㉧은 모두 몸이 안 좋아 보이는 나라를 가리키므로 같은 대상이다."),
    J(4, "부적절", False, [B("㉥지금 들어갈래?"), B("나라: ㉠어제 밤을 새웠더니")], "자체",
      "㉥ ‘지금’은 예은이 이 말을 하는 때를 가리키며, 나라가 말한 ㉠ ‘어제’를 기준으로 정해지지 않는다."),
    J(5, "적절", True, [B("예은: 당연하지. ㉨우리만 믿어."), B("㉡우리 다 같이 모여서 할걸.")], "해설지",
      "㉨은 예은, 세욱을 지시하고 ㉡은 예은, 세욱, 나라를 지시하므로 ㉨이 지시하는 대상은 ㉡이 지시하는 대상에 포함된다.",
      E("㉨은 예은, 세욱을 지시하고", "적절하다.")),
]

# ======== 39번 (정답 ②, 적절하지 않은 것)
Q[39]["answer"] = 2
Q[39]["judgments"] = [
    J(1, "적절", False, [F("◦\ue57b햇 새 놀애 브르\ue283다 [들의 새가 노래를 부른다]"),
                         F("◦하\ue28c童男이 잇\ue283\uf154다 [하늘의 사내아이가 있습니다]")], "해설지",
      "ⓐ에서 ‘브르다’와 달리 선어말 어미가 쓰인 ‘잇다’는 상대를 높이고 있다.",
      E("ⓐ에서", "적절하다.")),
    J(2, "부적절", True, [F("◦도\uf1fc\ue1cd 알\uf492[도적의 앞을]"),
                          F("◦암\uf440기 아\uf341\ue57b 우러 [암탉이 아침에 울어]")], "해설지",
      "ⓑ의 해당 글자는 ‘도적의’에 해당하는 말에서는 관형격 조사, ‘아침에’에 해당하는 말에서는 부사격 조사로 쓰였다. 주격 조사로도 쓰였다는 설명은 틀리다.",
      E("ⓑ에서", "적절하지 않다.")),
    J(3, "적절", False, [F("◦님그믈 救\uf537시고 [임금을 구하시고]"),
                         F("◦種種앳 됴\uf53a오\ue982 어드며 [종종 좋은 옷을 얻으며]")], "해설지",
      "음성 모음 체언 ‘님금’에는 목적격 조사 ‘을’이, 양성 모음 체언 ‘옷’에는 양성 모음의 목적격 조사가 결합하여 모음 조화가 지켜졌다.",
      E("ⓒ에서", "적절하다.")),
    J(4, "적절", False, [F("◦반\ue38a기 모매 잇\ue283녀 [마땅히 몸에 있느냐?]"),
                         F("◦究羅帝 이제 어듸 잇\ue283뇨 [구라제는 지금 어디 있느냐?]")], "해설지",
      "판정 의문문에는 종결 어미 ‘-녀’가, 의문사 ‘어듸’를 쓴 설명 의문문에는 ‘-뇨’가 쓰여 서로 달랐다.",
      E("ⓓ에서", "적절하다.")),
    J(5, "적절", False, [F("◦盲龍이 눈 \ue6d7고 [눈 먼 용이 눈을 뜨고]"),
                         F("◦\ue7a8\ue1a7티 \ue38f오 비치 \uf550더니 [꿀같이 달고 빛이 희더니]")], "해설지",
      "ⓔ의 낱말들에서 초성에 서로 다른 자음이 함께 쓰일 수 있었음을 알 수 있다.",
      E("ⓔ에서", "적절하다.")),
]

json.dump(d, open(HERE + r"\세트_37-39.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("세트_37-39.json 씀")
