"""2026년 7월 고3 언어와 매체 37~39번(안내문 없는 문법 단독 문항 묶음) 세트: 초안 + 쪽 그림 확인값 + 해설지 기반 판단 → 세트_37-39.json

초안: py -X utf8 _임시\\뽑기_래퍼_35-45.py <문제PDF> 37 39 - 초안_37-39.json   (선지 줄 앞 공백 때문에 래퍼 사용)
쪽 그림·텍스트층으로 확인한 것(문제_13쪽·14쪽, _임시 확대, texttrace):
- 굵은 글씨: 37 상자의 상황 줄 '[윤수, … 상황]' 전체, 말한 이 '윤수:' '설아:' '준호:'(콜론까지 type 0+1), 39 상자의 '[조건]'.
  38 상자는 굵은 글씨 없음.
- 밑줄: 37·38 발문 '않은'. 37 <보기> ㉠~㉦ 낱말, 38 <자료> 의 용언(기호 뒤가 아니므로 mark ""). 39 에는 밑줄 없음.
- 39 상자 아래에 0.7pt 크기의 보이지 않는 글자 'ㅠ' 가 텍스트층에 있다(쪽 그림에는 없음). meta.textlayer_subs 로 검사에서 뺀다.
- 1차 독립검토(독립검토_37-39.md) '반드시 고칠 것' 반영: 37②, 38②③④ 근거 인용 보강.
- 초안은 쪽 머리글·[A] 등을 37 ⑤ 뒤에 붙이므로 잘라 낸다.
"""
import json
import sys

ROOT = r"D:\Work\블로그\리딩맵"
HERE = ROOT + r"\작업\20260708-go3-korB"
sys.path.insert(0, ROOT + r"\도구")
import 세트_검사 as chk  # noqa: E402  (해설지 글자를 그대로 가져오기 위한 읽기 함수만 쓴다)

PROB = "20260708-go3-problem-korB_mun_NA5G12DA.pdf"
EXPL = "20260708-go3-explanation-korB_hsj_176HMBW2.pdf"
EX = chk.pdf_text(ROOT + r"\원본자료\ebsi-korean\pdf" + "\\" + EXPL).replace("\n", "")


def xq(no, a, b):
    s = EX.rindex(f"{no}. [출제 의도]")
    i = EX.index(a, s)
    j = EX.index(b, i) + len(b)
    return EX[i:j].strip()


d = json.load(open(HERE + r"\초안_37-39.json", encoding="utf-8"))
d.pop("raw_passage_lines", None)
d["meta"] = {"exam": "2026학년도 7월 고3 전국연합학력평가 국어영역(언어와 매체)", "exam_id": "20260708-go3-korB",
             "area": "문법", "topic": "지시 표현, 본용언과 보조 용언의 품사, 문장의 구조와 높임 표현",
             "problem_pdf": PROB, "explanation_pdf": EXPL,
             "textlayer_subs": {"ㅠ": ""}}
d["guide"] = None
d["range"] = [37, 39]
d["passage"] = []
Q = {q["no"]: q for q in d["questions"]}


def P(i, text, **kw):
    return dict({"id": i, "type": "para", "text": text, "underlines": []}, **kw)


def pieces(s, starts):
    """s 를 starts(각 조각의 첫 글자들) 자리에서 차례로 자른다."""
    idx, pos = [], 0
    for x in starts:
        pos = s.index(x, pos)
        idx.append(pos)
        pos += len(x)
    assert idx[0] == 0, s[:20]
    return [s[a:b].strip() for a, b in zip(idx, idx[1:] + [len(s)])]


def split_stem(no, end):
    s = Q[no]["stem"]
    i = s.index(end) + len(end)
    Q[no]["stem"] = s[:i]
    return s[i:].strip()


def U(mark, text):
    return {"mark": mark, "text": text}


# ---- 37번
rest = split_stem(37, "것은?")
Q[37]["stem_underlines"] = ["않은"]
assert rest.startswith("<보 기>")
rest = rest[len("<보 기>"):].strip()
parts = pieces(rest, ["[윤수", "윤수: 설아야", "설아: 시작", "준호: ㉢", "윤수: 그럼", "준호: 두", "설아: 어쩔"])
blocks = [P("b1", parts[0], type="heading", bold=[parts[0]])]
UL37 = [U("㉠", "여기"), U("㉡", "거기"), U("㉢", "여기"), U("㉣", "그건"), U("㉤", "이것들"), U("㉥", "저번"), U("㉦", "이번")]
for k, t in enumerate(parts[1:], 2):
    blocks.append(P(f"b{k}", t, dialogue=True, bold=[t[:t.index(":") + 1]],
                    underlines=[u for u in UL37 if u["mark"] in t]))
assert sum(len(b["underlines"]) for b in blocks) == 7
Q[37]["bogi"] = {"label": "<보 기>", "blocks": blocks}
c5 = Q[37]["choices"][4]
Q[37]["choices"][4] = c5[: c5.index("2023학년도")].strip()

# ---- 38번
Q[38]["stem"] = Q[38]["stem"].replace("[3점]", "")
rest = split_stem(38, "것은?")
Q[38]["stem_underlines"] = ["않은"]
assert rest.startswith("<보 기>"), rest[:20]
i = rest.index("<자 료>")
view = rest[len("<보 기>"):i].strip()
lines = pieces(rest[i + len("<자 료>"):].strip(), ["㉠그는", "㉡음식", "㉢그는", "㉣눈물", "㉤그가"])
UL38 = [["못하지", "않았다"], ["못하지", "않다"], ["않고"], ["못했다"], ["못했다"]]
Q[38]["bogi"] = [
    {"label": "<보 기>", "blocks": [P("b1", view)]},
    {"label": "<자 료>", "blocks": [P(f"c{k+1}", t, underlines=[U("", x) for x in UL38[k]]) for k, t in enumerate(lines)]},
]

# ---- 39번
rest = split_stem(39, "것은?")
assert rest.startswith("<보 기>")
rest = rest[len("<보 기>"):].replace("ㅠ", "").strip()
parts = pieces(rest, ["[조건]", "∘안은", "∘목적어", "∘안긴"])
Q[39]["bogi"] = {"label": "<보 기>", "blocks": [P("b1", parts[0], type="heading", bold=["[조건]"])]
                 + [P(f"b{k+2}", t) for k, t in enumerate(parts[1:])]}


def J(choice, verdict, ans, quotes, reason, x):
    return {"choice": choice, "verdict": verdict, "is_answer": ans, "basis": "해설지", "reason": reason,
            "explanation_quote": x, "evidence": [{"source": "bogi", "para": None, "quote": q} for q in quotes]}


# ======== 37번 (정답 ②, 적절하지 않은 것)
Q[37]["answer"] = 2
Q[37]["judgments"] = [
    J(1, "적절", False, ["2번 조명만 점등이 안 되고 있어. ㉠여기 좀 와 봐.", "㉢여기엔 아무것도 없어."],
      "㉠의 '여기'는 2번 조명만 점등이 안 되고 있는 곳이고, ㉢의 '여기'는 준호가 예비 조명이 없음을 확인한 곳이므로 서로 다른 위치이다.",
      xq(37, "①㉠의", "확인한 곳이다.")),
    J(2, "부적절", True, ["준호야, ㉡거기에 혹시 예비 조명이 있니? 있다면 좀 가져다줄래?", "㉢여기엔 아무것도 없어."],
      "㉡의 '거기'와 ㉢의 '여기'는 같은 곳을 가리킨다. 그러나 ㉡은 말하는 설아에게서 멀고 듣는 준호에게 가까운 곳을 가리키는 표현이므로, 지시하는 장소에 화자가 위치할 때 쓰는 표현이 아니다.",
      xq(37, "㉡의 ‘거기’와", "적절하지 않다.")),
    J(3, "적절", False, ["혹시 예비 조명이 있니?", "㉣그건 작년에 고장나서 폐기했대."],
      "㉣의 '그건'은 앞의 발화에서 언급된 예비 조명을 대신하고, ㉡의 '거기'는 준호가 있는 장소를 가리킨다.",
      xq(37, "③㉣의", "표현이다.")),
    J(4, "적절", False, ["작년에 고장나서 폐기했대.", "1번과 3번 조명 두 개뿐인데 ㉤이것들로 무대를 모두 비출 수 있을까?"],
      "㉣의 '그건'은 폐기되어 대화 상황에 없는 예비 조명을 가리키고, ㉤의 '이것들'은 대화 상황에 있는 1번과 3번 조명을 가리킨다.",
      xq(37, "④㉣의", "표현이다.")),
    J(5, "적절", False, ["㉥저번에도 조명 두 개로 행사를 진행한 적이 있었어.", "㉦이번에도 그렇게 하자."],
      "㉥의 '저번'은 과거의 특정 시점을 가리키지만, ㉦의 '이번'은 축제가 진행되는 때를 가리킨다.",
      xq(37, "⑤㉥의", "표현이다.")),
]

# ======== 38번 (정답 ⑤, 적절하지 않은 것)
RULE = view[view.index("본용언과 보조 용언의 품사는"): view.index("형용사는 그렇지 않다.") + len("형용사는 그렇지 않다.")]
DEF = view[view.index("문장의 주체를 주되게 서술하면서"): view.index("보조 용언이라고 하는데") + len("보조 용언이라고 하는데")]
Q[38]["answer"] = 5
Q[38]["judgments"] = [
    J(1, "적절", False, ["용언에는 본용언, 보조 용언으로 둘 다 쓰이는 것이 있다.", "㉠그는 노래를 못하지 않았다.", "㉣눈물 때문에 말을 잇지 못했다."],
      "㉠의 '못하다'는 본용언이고 ㉣의 '못하다'는 '잇다'에 연결된 보조 용언이므로, '못하다'는 본용언과 보조 용언으로 모두 쓰인다.",
      xq(38, "①㉠의", "알 수 있다.")),
    J(2, "적절", False, [RULE, "㉠그는 노래를 못하지 않았다.", "㉡음식 솜씨가 예전보다 못하지 않다."],
      "㉡은 '예전보다 못하지 않는다'처럼 쓸 수 없다. '않다'가 현재 시제 선어말 어미와 결합할 수 없으므로 보조 형용사이다. ㉠의 '않다'는 결합할 수 있어 보조 동사이다.",
      xq(38, "②㉡의", "보조 동사이다.")),
    J(3, "적절", False, [DEF, "㉡음식 솜씨가 예전보다 못하지 않다.", "㉢그는 사람들에게 말을 않고 떠났다."],
      "㉡의 '않다'는 본용언의 뜻을 보충하는 보조 용언이다. ㉢의 '않다'는 '어떤 행동을 안 하다'의 뜻으로 주체를 주되게 서술하는 본용언이다.",
      xq(38, "③㉡의", "본용언이다.")),
    J(4, "적절", False, [RULE, "말을 않고 떠났다.", "㉡음식 솜씨가 예전보다 못하지 않다."],
      "㉢의 '않다'는 '말을 않고 있다'처럼 '-고 있다'와 결합할 수 있으므로 동사이다. ㉡의 '못하다'는 '-고 있다'와 결합할 수 없으므로 형용사이다.",
      xq(38, "④㉢의", "형용사이다.")),
    J(5, "부적절", True, ["보조 용언의 품사는 본용언의 품사에 연동되어 결정되는 것도 있고", "말을 잇지 못했다.", "㉤그가 한 행동은 옳지 못했다."],
      "㉣의 '못하다'는 동사 '잇다'를 따라 보조 동사이고, ㉤의 '못하다'는 형용사 '옳다'를 따라 보조 형용사이다. 본용언의 품사와 다르지 않으며, '못하다'의 품사는 고정되지 않고 본용언의 품사에 연동되어 결정된다.",
      xq(38, "㉣의 ‘못하다’는 보조 동사이고", "알 수 있다.")),
]

# ======== 39번 (정답 ①, 적절한 것)
Q[39]["answer"] = 1
Q[39]["judgments"] = [
    J(1, "적절", True, ["∘안은문장의 서술어의 자릿수가 셋일 것.", "∘목적어나 부사어가 지시하는 대상을 높일 것.", "∘안긴절의 주체를 간접적으로 높이는 표현이 나타날 것."],
      "서술어 '여쭈어보다'는 주어, 부사어, 목적어를 필요로 하는 세 자리 서술어이고 부사어가 가리키는 '할아버지'를 높인다. 관형사절 '다리가 아프신'은 할아버지의 신체를 높여 할아버지를 간접적으로 높인다.",
      xq(39, "관형사절 ‘다리가", "서술어이다.")),
    J(2, "부적절", False, ["서술어의 자릿수가 셋일 것."],
      "'찾아가다'는 두 자리 서술어이므로 서술어의 자릿수가 셋이라는 조건에 맞지 않는다.",
      xq(39, "②‘찾아가다’는", "서술어이다.")),
    J(3, "부적절", False, ["안긴절의 주체를 간접적으로 높이는 표현"],
      "안긴절 '고향에서 올라오신'의 주체는 '부모님'이고, 이 표현은 주체를 직접 높이므로 간접적으로 높이는 표현이 아니다.",
      xq(39, "③‘고향에서", "높이고 있다.")),
    J(4, "부적절", False, ["목적어나 부사어가 지시하는 대상을 높일 것."],
      "부사어 '친척들에게'가 지시하는 대상인 '친척들'을 높이고 있지 않다.",
      xq(39, "④부사어가", "있지 않다.")),
    J(5, "부적절", False, ["안은문장의 서술어의 자릿수가 셋"],
      "'위로하다'는 두 자리 서술어이므로 서술어의 자릿수가 셋이라는 조건에 맞지 않는다.",
      xq(39, "⑤‘위로하다’는", "서술어이다.")),
]

json.dump(d, open(HERE + r"\세트_37-39.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("세트_37-39.json 씀")
