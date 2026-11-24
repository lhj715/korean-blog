"""2024-03 고1 13~15번 세트(문법 단독 문항 묶음, 안내문 없음) → 세트_13-15.json
초안: _임시\\초안_13-15.json (도구/세트_뽑기.py 를 줄 앞 공백만 떼는 래퍼로 실행). 쪽 그림(문제_5쪽)·PDF 좌표로 확인한 것:
- guide null, passage []. 13번 발문 밑줄 없음, 14·15번 '않은' 밑줄.
- 13번 <보기>: 문단 하나(선생님: 굵음, 콜론은 보통) + 표 둘(벡터 선, 둘째 표의 «달님» 등은 래스터라 텍스트층에 없음) +
  [학습 활동](굵음) + 문단 + 점선 안쪽 상자(ㄱ ㄴ / ㄷ ㄹ 두 줄). 표 속 ㅂㄷㄱ 등은 그림 안이라 굵기 무시.
- 14번 <보기>: [탐구 과제](굵음) + 문단 + ㄱ~ㅁ 다섯 줄 + (오른쪽 단 위) 국어사전 화면 그림(래스터) + 각주 «* →:».
- 15번 <보기>: [학습 자료](굵음) 둘 + [학습 과제](굵음) + 문단 + ㄱ~ㅁ(각 항목 두 줄: 직접 인용, → 간접 인용).
  밑줄(300dpi 확대 확인): 폈구나, 폈다(고 제외), 갔어요, 갔다, 내일, 오늘, 이, 그, 너, 자기.
- 해설지 없는 선지: 없음(13~15번 모든 선지가 해설지에 있다).
"""
import json
import re

HERE = r"D:\Work\블로그\리딩맵\작업\20240328-go1"
d = json.load(open(HERE + r"\_임시\초안_13-15.json", encoding="utf-8"))
d.pop("raw_passage_lines", None)
d["meta"] = {"exam": "2024학년도 3월 고1 전국연합학력평가 국어", "exam_id": "20240328-go1", "area": "문법",
             "topic": "음운 변동·사전 활용·인용 표현",
             "problem_pdf": "20240328-go1-problem-kor_mun_7628232M.pdf",
             "explanation_pdf": "20240328-go1-explanation-kor_hsj_PVWAO87B.pdf"}
d["guide"] = None
d["passage"] = []
Q = {q["no"]: q for q in d["questions"]}

expl = open(HERE + r"\해설_글자.txt", encoding="utf-8").read()


def section(no):
    i = re.search(rf"\n{no}\. \[출제의도\]", expl).start()
    if no < 15:
        j = re.search(rf"\n{no + 1}\. \[출제의도\]", expl[i + 1:]).start() + i + 1
    else:
        j = expl.index("\n[16 ~ 20]", i)
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


def T(id_, type_, text, ul=(), **kw):
    o = {"id": id_, "type": type_, "text": text, "underlines": [{"mark": m, "text": t} for m, t in ul]}
    o.update(kw)
    return o


def J(choice, verdict, ans, ev, reason, xq):
    out = {"choice": choice, "verdict": verdict, "is_answer": ans, "basis": "해설지", "reason": reason,
           "evidence": [], "explanation_quote": xq}
    for e in ev:
        if e[0] == "fig":
            out["evidence"].append({"source": "figure", "fig": e[1], "quote": e[2]})
        else:
            out["evidence"].append({"source": "bogi", "para": None, "quote": e[1]})
    return out


def split_bogi(s, label="< 보 기 >"):
    i = s.index(label)
    return s[:i].strip(), s[i + len(label):]


# ================= 13번
st, B = split_bogi(Q[13]["stem"])
assert st == "<보기>는 수업의 일부이다. ‘학습 활동’의 결과로 가장 적절한 것은?", st
Q[13]["stem"] = st
iT1 = B.index("조음 위치조음 방법")
iT2 = B.index("영향의 방향")
iL = B.index("[학습 활동]")
iX = B.index("ㄱ. 난로")
P1 = B[:iT1].strip()
F1 = B[iT1:iT2]
F2 = B[iT2:iL]
LAB = "[학습 활동]"
P2 = B[iL + len(LAB):iX].strip()
LIST = B[iX:]
assert P1.startswith("선생님:") and P1.endswith("봅시다."), P1
assert P2.startswith("뒤 음운의") and P2.endswith("골라 보자."), P2
assert LIST == "ㄱ. 난로[날로]ㄷ. 실내[실래]ㄴ. 맏이[마지]ㄹ. 톱날[톰날]", LIST
SP = "\u3000"
Q[13]["bogi"] = {"label": "보 기", "blocks": [
    T("b1", "para", P1, dialogue=True, bold=["선생님"]),
    {"id": "f1", "type": "figure", "caption": "", "image": "그림_13-15_13_표1.png", "pdf_text": F1,
     "alt": "자음 체계표. 파열음은 입술소리 ㅂ, 잇몸소리 ㄷ, 여린입천장소리 ㄱ, 파찰음은 센입천장소리 ㅈ, 비음은 입술소리 ㅁ, 잇몸소리 ㄴ, 여린입천장소리 ㅇ, 유음은 잇몸소리 ㄹ이다."},
    {"id": "f2", "type": "figure", "caption": "", "image": "그림_13-15_13_표2.png", "pdf_text": F2,
     "alt": "음운 변동 양상표. 달님[달림]은 앞 음운의 영향으로 조음 방법이 변하고, 작문[장문]은 뒤 음운의 영향으로 조음 방법이 변하고, 해돋이[해도지]는 뒤 음운의 영향으로 조음 방법과 조음 위치가 변한다."},
    T("b2", "para", LAB, bold=[LAB]),
    T("b3", "para", P2),
    T("b4", "para", "ㄱ. 난로[날로]\nㄷ. 실내[실래]", inbox="list", inbox_line="dotted"),
    T("b4b", "para", "ㄴ. 맏이[마지]\nㄹ. 톱날[톰날]", inbox="list", inbox_line="dotted"),
]}
Q[13]["answer"] = 2
Q[13]["judgments"] = [
    J(1, "부적절", False, [("bogi", "ㄴ. 맏이[마지]"), ("fig", "f2", "조음 방법과 조음 위치의 변화")],
      "‘맏이[마지]’는 뒤 음운 ‘ㅣ’의 영향으로 앞 음운 ‘ㄷ’이 ‘ㅈ’으로 바뀌어 조음 방법과 조음 위치가 모두 바뀌므로 조음 방법만 바뀌는 단어가 아니다.",
      X(13, "① ㄴ은", "해당하지 않는다.")),
    J(2, "적절", True, [("bogi", "ㄱ. 난로[날로]"), ("bogi", "ㄹ. 톱날[톰날]"), ("fig", "f2", "조음 방법의 변화")],
      "‘난로[날로]’는 뒤 음운 ‘ㄹ’의 영향으로 앞 음운 ‘ㄴ’이, ‘톱날[톰날]’은 뒤 음운 ‘ㄴ’의 영향으로 앞 음운 ‘ㅂ’이 조음 방법만 바뀐다.",
      X(13, "‘ㄱ. 난로[날로]’는", "‘ㄹ. 톱날[톰날]’은 뒤의 음운 ‘ㄴ’의 영향으로 앞의 음운 ‘ㅂ’이 ‘ㅁ’으로 바뀌며, 조음 방법만 바뀌는 단어에 해당한다.")),
    J(3, "부적절", False, [("bogi", "ㄴ. 맏이[마지]"), ("bogi", "ㄷ. 실내[실래]")],
      "‘맏이[마지]’는 조음 방법만 바뀌는 경우가 아니고, ‘실내[실래]’는 앞 음운의 영향으로 뒤 음운이 바뀌므로 뒤 음운의 영향으로 앞 음운이 바뀌는 경우가 아니다.",
      X(13, "③ ㄴ은", "ㄷ은 조음 방법만 바뀌는 경우에는 해당하지만, 뒤 음운의 영향으로 앞 음운이 바뀌는 경우에는 해당하지 않는다.")),
    J(4, "부적절", False, [("bogi", "ㄴ. 맏이[마지]"), ("bogi", "ㄹ. 톱날[톰날]")],
      "‘ㄹ’은 조건에 맞지만 ‘맏이[마지]’는 앞 음운이 바뀌어도 조음 방법만 바뀌는 경우에 해당하지 않는다.",
      X(13, "④ ㄴ은", "해당하지 않는다.")),
    J(5, "부적절", False, [("bogi", "ㄷ. 실내[실래]"), ("bogi", "뒤 음운의 영향을 받아서 앞 음운이 조음 방법만 바뀌는")],
      "‘실내[실래]’는 조음 방법만 바뀌지만 앞 음운의 영향으로 뒤 음운이 바뀌므로 뒤 음운의 영향으로 앞 음운이 바뀌는 경우가 아니다.",
      X(13, "⑤ ㄷ은", "해당하지 않는다.")),
]

# ================= 14번
st, B = split_bogi(Q[14]["stem"])
assert st == "<보기>의 ‘탐구 과제’를 수행한 결과로 적절하지 않은 것은?", st
Q[14]["stem"] = st
Q[14]["stem_underlines"] = ["않은"]
iL = B.index("[탐구 과제]")
ik = B.index("ㄱ. 민수")
iN = B.index("* →:")
LAB14 = "[탐구 과제]"
INTRO = B[iL + len(LAB14):ik].strip()
items = re.split(r"(?=[ㄱ-ㅁ]\. )", B[ik:iN])
items = [x.strip() for x in items if x.strip()]
assert len(items) == 5 and items[0].startswith("ㄱ.") and items[4].startswith("ㅁ."), items
NOTE = B[iN:].strip()
assert INTRO.endswith("말해 보자.") and NOTE.endswith("나타냄."), (INTRO, NOTE)
RT = ("국어사전 작다1 「1」길이, 넓이, 부피 따위가 비교 대상이나 보통보다 덜하다. 「2」정하여진 크기에 모자라서 맞지 아니하다. "
      "「3」일의 규모, 범위, 정도, 중요성 따위가 비교 대상이나 보통 수준에 미치지 못하다. 「4」사람됨이나 생각 따위가 좁고 보잘것없다. "
      "작다2→적다 적다2 수효나 분량, 정도가 일정한 기준에 미치지 못하다.")
blocks = [T("b1", "para", LAB14, bold=[LAB14]), T("b2", "para", INTRO)]
for k, it in enumerate(items):
    blocks.append(T(f"b{3 + k}", "para", it))
blocks.append({"id": "f3", "type": "figure", "caption": "", "image": "그림_13-15_14_사전.png", "pdf_text": "", "raster_text": RT,
               "alt": "온라인 국어사전 화면. ‘작다1’의 뜻 「1」~「4」가 나열되어 있고, ‘작다2→적다’를 누르면 ‘적다2: 수효나 분량, 정도가 일정한 기준에 미치지 못하다.’가 나온다."})
blocks.append(T("b8", "note", NOTE))
Q[14]["bogi"] = {"label": "보 기", "blocks": blocks}
Q[14]["answer"] = 1
Q[14]["judgments"] = [
    J(1, "부적절", True, [("bogi", "ㄱ. 민수는 진서에 비해 말수가"), ("fig", "f3", "수효나 분량, 정도가 일정한 기준에 미치지 못하다.")],
      "‘말수가 적다’는 ‘수효나 분량, 정도가 일정한 기준에 미치지 못하다’는 뜻이어서 ‘작다2’에서 ‘적다2’로 이어지는 뜻을 보아 ‘적다’가 맞고, ‘작다1’의 「1」을 고려해 ‘작다’가 맞다고 한 것은 틀렸다.",
      X(14, "ㄱ은 ‘수효나", "‘적다’가 적절하다.")),
    J(2, "적절", False, [("bogi", "ㄴ. 키가 커서 작년에 구매한 옷이"), ("fig", "f3", "정하여진 크기에 모자라서 맞지 아니하다.")],
      "‘작년에 구매한 옷이 작다’는 ‘정하여진 크기에 모자라서 맞지 아니하다’는 뜻이므로 ‘작다1’의 「2」를 고려해 ‘작다’가 맞다.",
      X(14, "② ㄴ은", "적절하다.")),
    J(3, "적절", False, [("bogi", "ㄷ. 오늘 일은 지난번에 비해 규모가"), ("fig", "f3", "일의 규모, 범위, 정도, 중요성 따위가 비교 대상이나 보통 수준에 미치지 못하다.")],
      "‘규모가 작다’는 ‘일의 규모, 범위, 정도, 중요성 따위가 비교 대상이나 보통 수준에 미치지 못하다’는 뜻이므로 「3」을 고려해 ‘작다’가 맞다.",
      X(14, "③ ㄷ은", "적절하다.")),
    J(4, "적절", False, [("bogi", "ㄹ. 그는 큰일을 하기에는 그릇이 아직"), ("fig", "f3", "사람됨이나 생각 따위가 좁고 보잘것없다.")],
      "‘그릇이 작다’는 ‘사람됨이나 생각 따위가 좁고 보잘것없다’는 뜻이므로 「4」를 고려해 ‘작다’가 맞다.",
      X(14, "④ ㄹ은", "적절하다.")),
    J(5, "적절", False, [("bogi", "ㅁ. 백일장 대회의 신청 인원이 여전히"), ("bogi", "‘a →b’는 a를 b로 바꿔 써야 함을 나타냄.")],
      "‘신청 인원이 적다’는 ‘수효나 분량, 정도가 일정한 기준에 미치지 못하다’는 뜻이므로 ‘작다1’, ‘작다2’와 ‘적다2’를 고려해 ‘적다’가 맞다.",
      X(14, "⑤ ㅁ은", "적절하다.")),
]

# ================= 15번
st, B = split_bogi(Q[15]["stem"])
assert st == "<보기>의 ‘학습 자료’를 바탕으로 ‘학습 과제’를 수행한 결과로 적절하지 않은 것은?", st
Q[15]["stem"] = st
Q[15]["stem_underlines"] = ["않은"]
LA, LB = "[학습 자료]", "[학습 과제]"
iB = B.index(LB)
ik = B.index("ㄱ. 지아가")
D1 = B[B.index("◦직접인용"):B.index("◦간접인용")].strip()
D2 = B[B.index("◦간접인용"):iB].strip()
INTRO15 = B[iB + len(LB):ik].strip()
parts = re.split(r"(?=[ㄱ-ㅁ]\. )", B[ik:])
parts = [p.strip() for p in parts if p.strip()]
assert len(parts) == 5, parts
its = []
for p in parts:
    a, b = p.split("→")
    its.append(a.strip() + "\n→" + b)
assert INTRO15.endswith("바꾸어 보자.") and D1.endswith("사용함.") and D2.endswith("사용함."), (INTRO15, D1, D2)
ULS = [[("", "폈구나"), ("", "폈다")], [("", "갔어요"), ("", "갔다")], [("", "내일"), ("", "오늘")],
       [("", "이"), ("", "그")], [("", "너"), ("", "자기")]]
blocks = [T("b1", "para", LA, bold=[LA]), T("b2", "para", D1), T("b3", "para", D2),
          T("b4", "para", LB, bold=[LB]), T("b5", "para", INTRO15)]
for k, (it, ul) in enumerate(zip(its, ULS)):
    blocks.append(T(f"b{6 + k}", "para", it, ul))
Q[15]["bogi"] = {"label": "보 기", "blocks": blocks}
Q[15]["answer"] = 5
Q[15]["judgments"] = [
    J(1, "적절", False, [("bogi", "지아가 “꽃이 벌써 폈구나!”라고 했다."), ("bogi", "→ 지아가 꽃이 벌써 폈다고 했다.")],
      "문장 종결 표현 ‘폈구나’를 ‘폈다’로 적절히 바꿔 서술하였다.",
      X(15, "① ㄱ은", "서술하였다.")),
    J(2, "적절", False, [("bogi", "지아가 “버스가 벌써 갔어요.”라고 했다."), ("bogi", "→ 지아가 버스가 벌써 갔다고 했다.")],
      "높임 표현 ‘갔어요’를 ‘갔다’로 적절히 바꿔 서술하였다.",
      X(15, "② ㄴ은", "서술하였다.")),
    J(3, "적절", False, [("bogi", "나는 어제 지아에게 “내일 보자.”라고 했다."), ("bogi", "→ 나는 어제 지아에게 오늘 보자고 했다.")],
      "시간 표현 ‘내일’을 ‘오늘’로 적절히 바꿔 서술하였다.",
      X(15, "③ ㄷ은", "서술하였다.")),
    J(4, "적절", False, [("bogi", "전학을 간 지아는 “이 학교가 좋다.”라고 했다."), ("bogi", "→ 전학을 간 지아는 그 학교가 좋다고 했다.")],
      "지시 표현 ‘이’를 ‘그’로 적절히 바꿔 서술하였다.",
      X(15, "④ ㄹ은", "서술하였다.")),
    J(5, "부적절", True, [("bogi", "지아는 나에게 “민지가 너를 불렀다.”라고 했다."), ("bogi", "→ 지아는 나에게 민지가 자기를 불렀다고 했다.")],
      "민지가 부른 ‘너’는 ‘나’에 해당하므로 인칭 표현 ‘너’를 ‘나’로 바꾸어 ‘민지가 나를 불렀다고’로 써야 하는데 ‘자기를’로 바꾸어 적절하지 않다.",
      X(15, "ㅁ에서 ‘민지’가", "바꾸어야 한다.")),
]

for q in d["questions"]:
    assert q["stem"] and len(q["choices"]) == 5 and q["answer"]
json.dump(d, open(HERE + r"\세트_13-15.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok")
