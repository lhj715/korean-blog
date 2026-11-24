"""2025-06 고3 모의평가 언어와 매체(korB) 37~39번 세트(안내문 없는 단독 문항 묶음): 초안 + 쪽 그림 확인값 + 해설지 기반 판단 → 세트_37-39.json

확인한 것(2026-11-25, 문제_13쪽·14쪽 그림, PDF 텍스트층·선·글꼴):
- 37번 <학습 활동> 상자: 선생님 말 문단 1개 + 안쪽 상자(㉠㉡㉢ 세 줄). 굵은 글씨는 «선생님» 만(get_texttrace type 0, 태고딕 글꼴. 콜론은 보통 글꼴).
  선지는 «제시 문장 / 수행 결과» 두 칸 표(머리 줄은 plain 상자, 표 테두리 선이 밑줄로 읽히므로 table_border). 밑줄 없음.
- 38번 <보기>: 문단 4개(첫 설명, (가), (나), (가)는 설명). 밑줄 ㉠㉡(PDF 선), 기호 없는 밑줄 «사실»(가)(나). 선지의 밑줄 낱말은 choice_underlines.
- 39번 수업 대화: 선생님·학생·선생님 세 줄 + «중세 국어 단어 / 목적격 조사 / 결합 단어» 표. 옛한글 PUA 가 든 1·3번째 말과 표는 쪽에서 오려 그림으로,
  선지 ① ③ 의 PUA 한 글자는 choice_images. 굵은 글씨는 말한 이 «선생님»·«학 생» 만(콜론은 보통).
- 발문 «않은» 밑줄은 37·38번(39번은 «적절한 것»).
"""
import json
import re

HERE = r"D:\Work\블로그\리딩맵\작업\20250604-go3-korB"
d = json.load(open(HERE + r"\_임시\d3739.json", encoding="utf-8"))
d.pop("raw_passage_lines", None)
d["meta"] = {"exam": "2026학년도 대학수학능력시험 6월 모의평가 국어(언어와 매체)", "exam_id": "20250604-go3-korB",
             "area": "문법", "topic": "문장의 짜임·관형사절·중세 국어 목적격 조사",
             "problem_pdf": "20250604-go3-problem-korB_1_mun_34L3Q845_1.pdf",
             "explanation_pdf": "20250604-go3-explanation-korB_1_hsj_TLN6OPB4_2.pdf"}
d["guide"] = None
d["range"] = [37, 39]
Q = {q["no"]: q for q in d["questions"]}
SP = "\u3000\u3000\u3000"

# ---- 37번
s37 = Q[37]["stem"]
Q[37]["stem"] = s37[: s37.index("[3점]")].strip()
Q[37]["stem_underlines"] = ["않은"]
body = s37[s37.index("<학습 활동>", 1) + len("<학습 활동>"):]
assert body.endswith("제시 문장수행 결과"), body[-20:]
t37 = body[: body.index("분석해 보세요.") + len("분석해 보세요.")]
items37 = re.split(r"(?=[㉠㉡㉢])", body[len(t37): body.index("제시 문장수행 결과")])
items37 = [x for x in items37 if x]
assert len(items37) == 3, items37
b37 = [{"id": "b1", "type": "para", "dialogue": True, "text": t37, "bold": ["선생님"], "underlines": []}]
for k, t in enumerate(items37):
    b37.append({"id": f"b{k+2}", "type": "para", "text": t, "underlines": [], "inbox": "분석"})
Q[37]["bogi"] = [
    {"label": "학습 활동", "blocks": b37},
    {"label": "", "plain": True, "blocks": [
        {"id": "th", "type": "heading", "text": "제시 문장" + SP * 5 + "수행 결과", "underlines": []}]},
]
Q[37]["table_border"] = True
c5 = Q[37]["choices"][4]
Q[37]["choices"][4] = c5[: c5.index("실현되지 않았다.") + len("실현되지 않았다.")]
newc = []
for c in Q[37]["choices"]:
    m = re.search(r"\s*(?=[㉠㉡㉢]은 실현되었지만)", c)
    a, b = c[: m.start()].strip(), c[m.end():].strip()
    newc.append(a + SP * 3 + b)
Q[37]["choices"] = newc

# ---- 38번
s38 = Q[38]["stem"]
Q[38]["stem"] = s38[: s38.index("<보 기>")]
Q[38]["stem_underlines"] = ["않은"]
bg = s38[s38.index("<보 기>") + len("<보 기>"):]
parts = [x for x in re.split(r"(?=\(가\) 나는|\(나\) 나는|\(가\)는)", bg) if x]
assert len(parts) == 4, parts
b38 = [{"id": f"b{k+1}", "type": "para", "text": t, "underlines": []} for k, t in enumerate(parts)]
b38[1]["underlines"] = [{"mark": "", "text": "사실"}]
b38[2]["underlines"] = [{"mark": "", "text": "사실"}]
b38[3]["underlines"] = [
    {"mark": "㉠", "text": "수식받는 명사가 관형사절의 문장 성분이 될 수 있는 경우이다"},
    {"mark": "㉡", "text": "수식받는 명사가 관형사절의 문장 성분이 될 수 없는 경우이다"},
]
Q[38]["bogi"] = {"label": "< 보 기 >", "blocks": b38}
Q[38]["choice_underlines"] = {"1": ["기억"], "2": ["사건"], "3": ["단점"], "4": ["가능성"], "5": ["경험"]}

# ---- 39번
s39 = Q[39]["stem"]
i39 = s39.index("것은?") + len("것은?")
Q[39]["stem"] = s39[:i39]
rest = s39[i39:]
it = rest.index("중세 국어 단어목적격")
tab_text = rest[it:]
turns = [x for x in re.split(r"(?=학\u3000생:|선생님: 그 경우에는)", rest[:it]) if x]
assert len(turns) == 3, turns
PUA = re.compile("[\ue000-\uf8ff]")
IMGS = ["그림_37-39_39_수업1.png", None, "그림_37-39_39_수업3.png"]
BOLD = [["선생님"], ["학\u3000생"], ["선생님"]]
b39 = []
for k, t in enumerate(turns):
    b = {"id": f"b{k+1}", "type": "para", "dialogue": True, "text": t, "bold": BOLD[k], "underlines": []}
    if IMGS[k]:
        assert PUA.search(t), k
        b["display_image"] = IMGS[k]
    else:
        assert not PUA.search(t), k
    b39.append(b)
b39.append({"id": "tf", "type": "figure", "caption": "", "image": "그림_37-39_39_표.png",
            "pdf_text": tab_text, "raster_text": "",
            "alt": "표. 열 머리는 ‘중세 국어 단어’, ‘목적격 조사’, ‘결합 단어’. 왼쪽 칸에는 중세 국어 단어 여섯 개(둡게(덮개), 바롤(바다), 염규(부추), 아바님(아버님), 꿈, 벼로(벼루))가 적혀 있다. 가운데 칸에는 위에서부터 아래아가 든 ‘올’, ‘롤’과 ‘을’, ‘를’이 있고, 오른쪽 칸에는 각각 ㉠, ㉡, ㉢, ㉣이 있다."})
Q[39]["bogi"] = {"label": "", "blocks": b39}
c1, c3 = Q[39]["choices"][0], Q[39]["choices"][2]
assert c1.count("\ue470") == 1 and c3.count("\uea0b") == 1
Q[39]["choice_images"] = {
    "1": [{"text": "\ue470", "image": "그림_37-39_39_선지1.png", "alt": "아래아가 든 옛 글자 ‘롤’(바롤의 끝 글자)"}],
    "3": [{"text": "\uea0b", "image": "그림_37-39_39_선지3.png", "alt": "옛 글자 ‘꿈’"}],
}
for q in d["questions"]:
    assert len(q["choices"]) == 5, q["no"]


# ---- 인용·해설 도우미
def sq(s):
    return re.sub(r"[\s\u200b]+", "", s)


lines = open(HERE + r"\해설_글자.txt", encoding="utf-8").read().split("\n")
region = lines[777:895]
region = region[:808 - 777] + region[822 - 777:]
txt, skip = [], False
for l in region:
    if re.match(r"^=== 해설 \d+쪽 ===$", l):
        skip = True
        continue
    if skip:
        skip = False
        continue
    txt.append(l)
EXPL = sq("\n".join(txt))


def E(start, end, lead=""):
    s, e = sq(start), sq(end)
    i = EXPL.index(s)
    assert EXPL[i - len(lead): i] == lead, (start, repr(EXPL[i - 3: i]))
    j = EXPL.index(e, i) + len(e)
    return EXPL[i - len(lead): j]


def bq(no, start, end):
    """그 문항 상자 글 항목에서 start~end 를 글자 그대로 잘라 온다."""
    boxes = Q[no]["bogi"] if isinstance(Q[no]["bogi"], list) else [Q[no]["bogi"]]
    for box in boxes:
        for it_ in box.get("blocks", []):
            t = it_.get("text", "")
            if start in t:
                i = t.index(start)
                return t[i: t.index(end, i) + len(end)]
    raise KeyError(start)


def fq(start, end):
    i = tab_text.index(start)
    return tab_text[i: tab_text.index(end, i) + len(end)]


def J(choice, verdict, ans, ev, basis, reason, xq=None):
    out = {"choice": choice, "verdict": verdict, "is_answer": ans, "basis": basis, "reason": reason, "evidence": []}
    for e in ev:
        if isinstance(e, tuple):
            out["evidence"].append({"source": "figure", "fig": "tf", "quote": e[1]})
        else:
            out["evidence"].append({"source": "bogi", "para": None, "quote": e})
    if xq:
        out["explanation_quote"] = xq
    return out


# ======== 37번 (정답 ⑤, 적절하지 않은 것)
A1 = bq(37, "㉠피동", "피동사")
A2 = bq(37, "㉡서술어", "안긴문장")
A3 = bq(37, "㉢본용언", "서술어")
Q[37]["answer"] = 5
Q[37]["judgments"] = [
    J(1, "적절", False, [A1, A2], "해설지",
      "‘손꼽히다’는 피동 접미사 ‘-히-’가 결합한 피동사여서 ㉠이 실현되었다. 이 문장에는 서술어로 기능하는 안긴문장이 없으므로 ㉡은 실현되지 않았다.",
      E("‘손꼽히다’는", "쓰이지 않았다.")),
    J(2, "적절", False, [A1, A3], "해설지",
      "‘담기다’는 피동 접미사 ‘-기-’가 결합한 피동사여서 ㉠이 실현되었다. ‘모아 왔다’의 ‘오다’는 보조 용언이 아니라 본용언이므로 ㉢은 실현되지 않았다.",
      E("‘담기다’는", "본용언이다.")),
    J(3, "적절", False, [A2, A1], "해설지",
      "‘마음이 여려서’가 서술어로 기능하는 안긴문장이어서 ㉡이 실현되었다. 이 문장에는 피동 접미사가 결합한 피동사가 없으므로 ㉠은 실현되지 않았다.",
      E("‘친구가 마음이 여려서’에서", "쓰이지 않았다.")),
    J(4, "적절", False, [A2, A3], "해설지",
      "‘값이 올랐다’가 서술어로 기능하는 안긴문장이어서 ㉡이 실현되었다. 이 문장에는 본용언과 보조 용언의 결합으로 이루어진 서술어가 없으므로 ㉢은 실현되지 않았다.",
      E("‘우표가 올해 들어 값이 올랐다.’에서", "안긴문장이다(㉡).")),
    J(5, "부적절", True, [A3, A1], "해설지",
      "‘걸려 버렸다’는 본용언과 보조 용언의 결합으로 이루어진 서술어여서 ㉢이 실현되었다. ‘보이다’도 피동 접미사 ‘-이-’가 결합한 피동사여서 ㉠도 실현되었으므로 ㉠이 실현되지 않았다는 설명은 틀리다.",
      E("‘걸려 버렸다’는", "결합한 피동사이기 때문에 ㉠이 실현되었다.")),
]

# ======== 38번 (정답 ①, 적절하지 않은 것)
D_A = bq(38, "㉠수식받는", "있는 경우이다.")
D_B = bq(38, "㉡수식받는", "없는 경우이다.")
E_GA = bq(38, "(가)는 ‘사실’이", "있는 경우이다.")
E_NA = bq(38, "(나)는 관형사절의", "없는 경우이다.")
Q[38]["answer"] = 1
Q[38]["judgments"] = [
    J(1, "부적절", True, [D_A, D_B], "해설지",
      "‘함께 어울렸던’의 원래 문장은 ‘(생략된 주어) 함께 어울렸다.’이고 이 문장이 ‘기억’의 내용에 해당한다. ‘기억’은 관형사절의 문장 성분이 될 수 없으므로 ㉠이 아니라 ㉡의 예이다.",
      E("관형사절의 원래 문장 ‘(생략된 주어) 함께", "예로 적절하다.")),
    J(2, "적절", False, [E_GA], "해설지",
      "‘사건’은 관형사절의 원래 문장 ‘(생략된 주어) 어제 박물관에서 일어났다.’의 주어에 해당한다. 수식받는 명사가 관형사절의 문장 성분이 될 수 있으므로 ㉠의 예이다.",
      E("‘사건’이 관형사절의", "경우이다.")),
    J(3, "적절", False, [D_B], "해설지",
      "관형사절의 원래 문장 ‘방수가 잘되지 않는다.’가 ‘단점’의 내용에 해당한다. ‘단점’은 관형사절의 문장 성분이 될 수 없으므로 ㉡의 예이다.",
      E("관형사절의 원래 문장 ‘방수가", "경우이다.")),
    J(4, "적절", False, [E_NA], "해설지",
      "관형사절의 원래 문장 ‘전쟁이 끝나다.’가 ‘가능성’의 내용에 해당한다. ‘가능성’은 관형사절의 문장 성분이 될 수 없으므로 ㉡의 예이다.",
      E("관형사절의 원래 문장 ‘전쟁이", "경우이다.")),
    J(5, "적절", False, [bq(38, "(나) 나는", "깨달았다."), D_B], "해설지",
      "관형사절의 원래 문장 ‘(생략된 주어) 새벽마다 운동을 했다.’가 ‘경험’의 내용에 해당한다. ‘경험’은 관형사절의 문장 성분이 될 수 없으므로 ㉡의 예이다.",
      E("관형사절의 원래 문장 ‘(생략된 주어) 새벽마다", "경우이다.")),
]

# ======== 39번 (정답 ③, 적절한 것)
T_HARM = bq(39, "그리고 중세 국어에서", "결합했어요.")
T_MID = bq(39, "특이한 것은", "점이에요.")
F = lambda q: ("f", q)
Q[39]["answer"] = 3
Q[39]["judgments"] = [
    J(1, "부적절", False, [F(fq("바", "(바다)")), F(fq("아바님(아버님)", "(아버님)")), T_MID], "해설지",
      "㉠(‘올’)에는 끝음절에 받침이 있고 양성 모음인 ‘바롤(바다)’이 들어간다. 그런데 끝음절이 중성 모음 ‘ㅣ’이고 받침이 있는 ‘아바님(아버님)’도 ‘올’과 결합할 수 있으므로 ‘바롤’뿐이라는 설명은 틀리다.",
      E("(바다)’과", "‘아바님(아버님)’이다.")),
    J(2, "부적절", False, [F(fq("염규(부추)", "(부추)")), F(fq("벼로(벼루)", "(벼루)")), T_HARM], "해설지",
      "㉡(‘롤’)에는 끝음절에 받침이 없고 양성 모음인 ‘벼로(벼루)’와 모음이 ‘ㅔ’인 ‘둡게(덮개)’가 들어간다. ‘염규(부추)’는 끝음절 모음이 음성 모음이라 ‘를’과 결합하므로 ㉡에 들어갈 수 없다.",
      E("단어(㉡)는", "‘벼로(벼루)’이다.")),
    J(3, "적절", True, [F(fq("아바님(아버님)", "(아버님)")), F(fq("(꿈)", "(꿈)")), T_MID, T_HARM], "해설지",
      "‘아바님’은 끝음절 모음이 중성 모음 ‘ㅣ’이고 받침이 있어 ‘을’과도 결합할 수 있고, ‘꿈’은 받침이 있고 음성 모음이어서 ‘을’과 결합한다. 따라서 ㉢에는 ‘아바님’과 ‘꿈’이 들어간다.",
      E("‘을’과 결합할 수 있는 단어(㉢)는", "(꿈)’이다.")),
    J(4, "부적절", False, [F(fq("둡게(덮개)", "(덮개)")), F(fq("염규(부추)", "(부추)")), T_MID], "해설지",
      "‘둡게(덮개)’는 끝음절에 받침이 없고 모음이 ‘ㅔ’여서 ‘를’과 결합하고, ‘염규(부추)’도 받침이 없고 음성 모음이어서 ‘를’과 결합한다. ㉣에는 ‘둡게’뿐 아니라 ‘염규’도 들어가므로 틀리다.",
      E("‘를’과 결합할 수 있는 단어(㉣)는", "‘염규(부추)’이다.")),
    J(5, "부적절", False, [F(fq("아바님(아버님)", "(아버님)")), F(fq("둡게(덮개)", "(덮개)")), T_MID], "해설지",
      "㉡(‘롤’)과 ㉣(‘를’)에 공통으로 들어가는 단어는 받침이 없는 ‘둡게(덮개)’이다. ‘아바님’은 받침이 있어 ㉠과 ㉢에 들어가므로 ㉡과 ㉣에는 들어가지 않는다.",
      E("단어(㉡)는", "‘염규(부추)’이다.")),
]

json.dump(d, open(HERE + r"\세트_37-39.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("세트_37-39.json 씀")
