"""2025-03 고2 13~15번(문법 단독 문항) 세트: 초안 + 쪽 그림 확인값 + 해설지 기반 판단 -> 세트_13-15.json

초안: 도구/세트_뽑기.py (_임시\초안_13-15.json, 안내문 없음). 쪽 그림으로 확인한 것:
- 13번 <학습 활동> 상자: 안내 줄, [조건](굵게) ㄱ~ㄷ, 표(조건/실현된 예문)는 그림 조각. 발문 밑줄 없음.
- 14번 <보기> 상자: 선생님(굵게, 콜론은 보통) 대화, 안쪽 [자료] 상자([자료] 굵게), 순서도는 그림 조각. 선지는 [A][B][C] 3열 표.
- 15번 <보기> 상자: 설명 문단 + ◦ 예문 5줄(㉠~㉤ 밑줄). 발문 밑줄 '않은'.
- 굵은 글씨(type 0+1): [조건], 선생님, [자료] 만.
"""
import json
import re

HERE = r"D:\Work\블로그\리딩맵\작업\20250326-go2"
d = json.load(open(HERE + r"\_임시\초안_13-15.json", encoding="utf-8"))
raw_q = {q["no"]: {"stem": q["stem"]} for q in d["questions"]}
d.pop("raw_passage_lines", None)
d["meta"] = {"exam": "2025년 3월 고2 전국연합학력평가 국어", "exam_id": "20250326-go2", "area": "문법",
             "topic": "안은문장과 안긴문장·파생어의 분류·음운 변동",
             "problem_pdf": "20250326-go2-problem-kor_mun_4XZ5B8N3.pdf",
             "explanation_pdf": "20250326-go2-explanation-kor_hsj_E4P12771.pdf"}
d["guide"] = None
d["passage"] = []
Q = {q["no"]: q for q in d["questions"]}
SP = "\u3000"
expl = open(HERE + r"\해설_글자.txt", encoding="utf-8").read()


def section(no):
    i = expl.index(f"\n{no}. [출제의도]")
    j = expl.index(f"\n{no + 1}. [출제의도]", i) if no < 15 else expl.index("\n[16 ~ 21]", i)
    return expl[i:j]


def X(no, a, b):
    sec = section(no)
    keep = [(i, c) for i, c in enumerate(sec) if not c.isspace()]
    comp = "".join(c for _, c in keep)
    ca, cb = re.sub(r"\s+", "", a), re.sub(r"\s+", "", b)
    ia = comp.index(ca)
    ib = comp.index(cb, ia) + len(cb)
    return sec[keep[ia][0]: keep[ib - 1][0] + 1].replace("\n", "")


def J(choice, verdict, ans, ev, reason, xq):
    return {"choice": choice, "verdict": verdict, "is_answer": ans, "basis": "해설지", "reason": reason,
            "evidence": ev, "explanation_quote": xq}


def B(q):
    return {"source": "bogi", "para": None, "quote": q}


def F(fig, q):
    return {"source": "figure", "fig": fig, "quote": q}


# ---------------- 13번
Q[13]["stem"] = "<학습 활동>의 ⓐ~ ⓒ에 들어갈 예문으로 적절한 것은?"
C1 = "ㄱ. 안긴문장에 시간을 나타내는 부사어를 포함할 것."
C2 = "ㄴ. 안은문장의 서술어에 과거 시제 선어말 어미를 포함할 것."
C3 = "ㄷ. 안은문장의 사건이 안긴문장의 사건보다 나중에 일어날 것."
Q[13]["bogi"] = {"label": "학습 활동", "blocks": [
    {"id": "b1", "type": "para", "text": "※ 다음 [조건]이 실현된 예문을 만들어 보자.", "underlines": []},
    {"id": "b2", "type": "para", "text": "[조건]", "bold": ["[조건]"], "underlines": []},
    {"id": "b3", "type": "para", "text": C1, "underlines": []},
    {"id": "b4", "type": "para", "text": C2, "underlines": []},
    {"id": "b5", "type": "para", "text": C3, "underlines": []},
    {"id": "f1", "type": "figure", "caption": "", "image": "그림_13-15_13_조건표.png",
     "pdf_text": "조건실현된 예문ㄱ+ ㄴⓐㄱ+ ㄷⓑㄴ+ ㄷⓒ", "raster_text": "",
     "alt": "표: 조건 ㄱ+ㄴ은 예문 ⓐ, 조건 ㄱ+ㄷ은 예문 ⓑ, 조건 ㄴ+ㄷ은 예문 ⓒ에 해당한다."},
]}
Q[13]["answer"] = 1
Q[13]["judgments"] = [
    J(1, "적절", True, [B(C1), B(C2), F("f1", "ㄱ+ ㄴⓐ")],
      "‘내일’이 안긴문장의 시간 부사어이고, 안은문장의 서술어 ‘약속했다’에 과거 시제 선어말 어미가 있어 ⓐ의 조건 ㄱ과 ㄴ이 모두 실현된다.",
      X(13, "안긴문장에", "실현되었다.")),
    J(2, "부적절", False, [B(C2), F("f1", "ㄱ+ ㄴⓐ")],
      "안은문장의 서술어 ‘생각난다’에 과거 시제 선어말 어미가 없어 ⓐ의 조건 ㄴ이 실현되지 않았다.",
      X(13, "② 안은문장의", "포함되지 않았다")),
    J(3, "부적절", False, [B(C1), F("f1", "ㄱ+ ㄷⓑ")],
      "안긴문장 ‘자신이 대회에서 우승했음’에 시간 부사어가 없어 ⓑ의 조건 ㄱ이 실현되지 않았다.",
      X(13, "③ 안긴문장에", "포함되지 않았다")),
    J(4, "부적절", False, [B(C1), F("f1", "ㄱ+ ㄷⓑ")],
      "안긴문장 ‘동생이 읽을’에 시간 부사어가 없어 ⓑ의 조건 ㄱ이 실현되지 않았다.",
      X(13, "④ 안긴문장에", "포함되지 않았다")),
    J(5, "부적절", False, [B(C2), F("f1", "ㄴ+ ㄷⓒ")],
      "안은문장의 서술어 ‘좋아한다’에 과거 시제 선어말 어미가 없어 ⓒ의 조건 ㄴ이 실현되지 않았다.",
      X(13, "⑤ 안은문장의", "포함되지 않았다")),
]

# ---------------- 14번
Q[14]["stem"] = "<보기>의 [A] ~ [C]에 들어갈 내용을 바르게 짝지은 것은?"
ROWS = [("ㄱ, ㄴ", "ㄷ, ㅁ", "ㄹ, ㅂ"), ("ㄱ, ㄴ", "ㄹ, ㅁ", "ㄷ, ㅂ"), ("ㄴ, ㅂ", "ㄷ, ㄹ", "ㄱ, ㅁ"),
        ("ㄴ, ㅂ", "ㄷ, ㅁ", "ㄱ, ㄹ"), ("ㄷ, ㅁ", "ㄴ, ㅂ", "ㄱ, ㄹ")]
for k, r in enumerate(ROWS):
    assert "".join(r) == Q[14]["choices"][k].strip(), (k, Q[14]["choices"][k])
    Q[14]["choices"][k] = (SP * 4).join(r)
L1 = "ㄱ. 겁쟁이          ㄴ. 날고기          ㄷ. 넓히다"
L2 = "ㄹ. 맡기다          ㅁ. 지우개          ㅂ. 풋사랑"
FIGTXT = "접사가 어근 뒤에 결합하는가?→아니요[A] ↓예파생어의 품사가 어근의 품사와 동일한가?→아니요[B] ↓예[C]"
Q[14]["bogi"] = [
    {"label": "보 기", "blocks": [
        {"id": "b1", "type": "para", "dialogue": True,
         "text": "선생님: 파생어는 어근과 접사로 이루어진 단어를 말합니다. [자료]의 파생어를 분류해 봅시다.",
         "bold": ["선생님"], "underlines": []},
        {"id": "h1", "type": "para", "text": "[자료]", "bold": ["[자료]"], "underlines": [], "inbox": "자료"},
        {"id": "e1", "type": "para", "text": L1, "underlines": [], "inbox": "자료"},
        {"id": "e2", "type": "para", "text": L2, "underlines": [], "inbox": "자료"},
        {"id": "f1", "type": "figure", "caption": "", "image": "그림_13-15_14_순서도.png", "pdf_text": FIGTXT,
         "raster_text": "",
         "alt": "순서도: ‘접사가 어근 뒤에 결합하는가?’에 아니요면 [A], 예면 ‘파생어의 품사가 어근의 품사와 동일한가?’로 간다. 이 물음에 아니요면 [B], 예면 [C]이다."},
    ]},
    {"label": "", "plain": True, "blocks": [
        {"id": "th", "type": "heading", "text": "[A]" + SP * 6 + "[B]" + SP * 6 + "[C]",
         "underlines": [{"mark": "", "text": "[A]"}, {"mark": "", "text": "[B]"}, {"mark": "", "text": "[C]"}]}]},
]
Q[14]["answer"] = 4
QA = X(14, "ㄴ과 ㅂ은", "[A]에 해당한다")
QB = X(14, "ㄷ은 형용사", "[C]에 해당된다")
QALL = X(14, "ㄴ과 ㅂ은", "[C]에 해당된다")
Q[14]["judgments"] = [
    J(1, "부적절", False, [B("ㄱ. 겁쟁이"), F("f1", "접사가 어근 뒤에 결합하는가?")],
      "ㄱ ‘겁쟁이’는 접미사가 어근 뒤에 결합했으므로 [A]에 들어가지 않는다. [A]에는 접두사가 결합한 ㄴ, ㅂ이 들어간다.", QA),
    J(2, "부적절", False, [B("ㄱ. 겁쟁이"), F("f1", "아니요[A]")],
      "ㄱ ‘겁쟁이’는 어근 뒤에 접미사가 결합한 파생어이므로 [A]에 들어가지 않는다.", QA),
    J(3, "부적절", False, [B("ㅁ. 지우개"), B("ㄹ. 맡기다"), F("f1", "파생어의 품사가 어근의 품사와 동일한가?")],
      "ㅁ ‘지우개’는 동사 어근에 접미사가 결합해 명사가 되었으므로 품사가 달라 [B]에 해당한다. ㄹ ‘맡기다’는 품사가 같아 [C]에 해당한다. 그래서 ㄷ, ㄹ을 [B]에, ㄱ, ㅁ을 [C]에 둔 것은 틀렸다.", QB),
    J(4, "적절", True, [B("ㅁ. 지우개"), B("ㄹ. 맡기다"), F("f1", "아니요[B]")],
      "[A]는 접두사가 결합한 ㄴ, ㅂ, [B]는 접미사가 결합하고 품사가 바뀐 ㄷ, ㅁ, [C]는 접미사가 결합하고 품사가 같은 ㄱ, ㄹ이다.", QALL),
    J(5, "부적절", False, [B("ㄷ. 넓히다"), B("ㅁ. 지우개")],
      "ㄷ, ㅁ은 접사가 어근 뒤에 결합하므로 접사가 어근 뒤에 결합하지 않는 [A]에 들어갈 수 없다.", QA),
]

# ---------------- 15번
Q[15]["stem"] = "<보기>의 ㉠~ ㉤에 대한 이해로 적절하지 않은 것은?"
Q[15]["stem_underlines"] = ["않은"]
t = raw_q[15]["stem"]
body = t[t.index("< 보 기 >") + len("< 보 기 >"):]
i0 = body.index("◦")
intro = body[:i0].strip()
bul = [x.strip().lstrip("\u3000") for x in re.split(r"(?=◦)", body[i0:]) if x.strip()]
assert len(bul) == 5 and intro.endswith("달라지기도 한다."), (intro, bul)
BU = [("㉠", "첫해[처태]"), ("㉡", "넋두리[넉뚜리]"), ("㉢", "겉넓이[건널비]"), ("㉣", "낯익어[난니거]"), ("㉤", "물약[물략]")]
blocks = [{"id": "b1", "type": "para", "text": intro, "underlines": []}]
for k, (b, (m, u)) in enumerate(zip(bul, BU)):
    assert b.startswith("◦") and (m + u) in b, (b, m, u)
    blocks.append({"id": f"e{k+1}", "type": "para", "text": b, "underlines": [{"mark": m, "text": u}]})
Q[15]["bogi"] = {"label": "보 기", "blocks": blocks}
Q[15]["answer"] = 2
Q[15]["judgments"] = [
    J(1, "적절", False, [B("㉠첫해[처태]")],
      "‘첫해[처태]’는 ㅅ이 ㄷ으로 바뀌는 교체와 ㄷ과 ㅎ이 ㅌ으로 합쳐지는 축약이 한 번씩 일어나 음운이 하나 줄었다.",
      X(15, "①", "줄었다")),
    J(2, "부적절", True, [B("㉡넋두리[넉뚜리]")],
      "‘넋두리[넉뚜리]’는 첨가가 일어나지 않고 탈락과 교체가 일어나 음운의 개수가 하나 줄었다.",
      X(15, "㉡은 음운의", "줄었다")),
    J(3, "적절", False, [B("㉢겉넓이[건널비]")],
      "‘겉넓이[건널비]’는 교체만 일어나 음운의 개수에 변화가 없다.",
      X(15, "③ ㉢은", "없다")),
    J(4, "적절", False, [B("㉣낯익어[난니거]")],
      "‘낯익어[난니거]’는 교체와 첨가가 일어나 음운의 개수가 하나 늘었다.",
      X(15, "④ ㉣은", "늘었다")),
    J(5, "적절", False, [B("㉤물약[물략]")],
      "‘물약[물략]’은 첨가와 교체가 일어나 음운의 개수가 하나 늘었다.",
      X(15, "⑤ ㉤은", "늘었다")),
]
json.dump(d, open(HERE + r"\세트_13-15.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok")
