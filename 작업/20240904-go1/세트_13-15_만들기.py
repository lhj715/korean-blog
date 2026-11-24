"""2024-09 고1 13~15번 세트(문법 단독 문항 묶음, 안내문 없음) → 세트_13-15.json
초안: _임시\\뽑기_13-20.py (도구/세트_뽑기.py 사본: 선지 줄이 «  ①» 처럼 공백으로 시작해도 찾도록 strip 만 고침). 쪽 그림과 PDF 좌표로 확인한 것:
- guide null, passage []. 13번 발문 밑줄 없음, 14번 '않은' 밑줄(PDF 선 y184), 15번 발문 밑줄 없음('적절한').
- 13번 <보기>: 문단 둘(들여쓰기 «  » 로 시작) + [활동] + 그림(학생 1·2·3 래스터 위 글자는 텍스트층). 굵은 글씨 없음.
- 14번 <학습 활동>: 문단 하나 + ㄱ·ㄴ 예문 두 줄(안쪽 상자 없음). 굵은 글씨·밑줄 없음. 텍스트층 전각 공백은 보통 공백으로.
- 15번 <보기>: «선생님»·«학생» 굵음(type=1, 콜론은 보통). [자료1] 표(벡터 선, 글자는 텍스트층)·[자료2] 상자·학생 말은
  «예1»·«예2» 네모 낱말이 텍스트층에 없는 작은 그림이라 쪽에서 잘라 그림으로 넣고 pdf_text 에 텍스트층 글자를 둔다.
  선지는 ㉠·㉡ 두 칸 표: 표 머리(㉠ ㉡ 아래 밑줄)는 머리말 없는 plain 상자, 선지 글은 «㉠칸 + 전각 공백 + ㉡칸».
"""
import json
import re

HERE = r"D:\Work\블로그\리딩맵\작업\20240904-go1"
d = json.load(open(HERE + r"\_임시\초안_13-15.json", encoding="utf-8"))
d.pop("raw_passage_lines", None)
d["meta"] = {"exam": "2024학년도 9월 고1 전국연합학력평가", "exam_id": "20240904-go1", "area": "문법",
             "topic": "음운 변동·인용 표현·중세 국어 ‘ㅎ’ 종성 체언",
             "problem_pdf": "20240904-go1-problem-kor_mun_76DL7ZJ6.pdf",
             "explanation_pdf": "20240904-go1-explanation-kor_hsj_W74UM25M.pdf"}
d["guide"] = None
d["passage"] = []
Q = {q["no"]: q for q in d["questions"]}
SP = "\u3000"

expl = open(HERE + r"\해설_글자.txt", encoding="utf-8").read()


def section(no):
    i = re.search(rf"\n{no}\. \[출제의도\]", expl).start()
    j = re.search(rf"\n{no + 1}\. \[출제의도\]", expl[i + 1:]).start() + i + 1
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


def J(choice, verdict, ans, ev, basis, reason, xq=None):
    out = {"choice": choice, "verdict": verdict, "is_answer": ans, "basis": basis, "reason": reason, "evidence": []}
    for e in ev:
        if e[0] == "fig":
            out["evidence"].append({"source": "figure", "fig": e[1], "quote": e[2]})
        else:
            out["evidence"].append({"source": "bogi", "para": None, "quote": e[1]})
    if xq:
        out["explanation_quote"] = xq
    return out


# ================= 13번
s = Q[13]["stem"]
i = s.index("<보 기>")
st = s[:i].strip()
assert st == "<보기>의 활동을 모든 학생이 바르게 수행했을 때, ‘학생2’가 쓴 단어로 적절한 것은?", st
Q[13]["stem"] = st
B = s[i + len("<보 기>"):]
iA = B.index("[활동]")
iB = B.index("앞 학생이")
iF = B.index("학생1")
P1, LAB, P2, FT = B[:iA].strip(), "[활동]", B[iB:iF].strip(), B[iF:].strip()
assert P1.endswith("첨가가 있다.") and P2.endswith("쓰시오."), (P1, P2)
assert FT == "학생1   학생2 학생3솜이불[솜ː니불]밟히다[발피다]➜➜", FT
Q[13]["bogi"] = {"label": "보 기", "blocks": [
    {"id": "b1", "type": "para", "text": P1, "underlines": []},
    {"id": "b2", "type": "para", "text": LAB, "underlines": []},
    {"id": "b3", "type": "para", "text": P2, "underlines": []},
    {"id": "f13", "type": "figure", "caption": "", "image": "그림_13-15_13_활동.png", "pdf_text": FT,
     "alt": "학생 1, 학생 2, 학생 3이 차례로 화살표로 이어져 있다. 학생 1은 ‘솜이불[솜ː니불]’, 학생 3은 ‘밟히다[발피다]’ 판을 들고 있고 학생 2의 판은 비어 있다."}]}
Q[13]["answer"] = 2
CHUK = "두 음운이 합쳐져 새로운 하나의 음운으로 줄어드는 축약"
Q[13]["judgments"] = [
    J(1, "부적절", False, [("fig", "f13", "솜이불[솜ː니불]"), ("bogi", "없던 음운이 새로 생기는 첨가가 있다.")], "해설지",
      "‘삯일[상닐]’에는 탈락과 교체뿐 아니라 ‘솜이불’에서 일어난 첨가도 일어나므로 ‘학생2’가 쓸 수 없는 단어이다.",
      X(13, "① ‘삯일[상닐]’에서는", "탈락, 교체, 첨가가 일어난다.")),
    J(2, "적절", True, [("bogi", P2), ("fig", "f13", "솜이불[솜ː니불]밟히다[발피다]")], "해설지",
      "‘옷맵시[온맵씨]’는 다른 음운 변동 없이 교체만 일어나므로, 앞 학생들의 단어에서 일어난 첨가와 축약이 일어나지 않아 ‘학생2’의 단어로 적절하다.",
      X(13, "‘옷맵시[온맵씨]’에서는", "적절하다.")),
    J(3, "부적절", False, [("fig", "f13", "밟히다[발피다]"), ("bogi", CHUK)], "해설지",
      "‘겉핥기[거탈끼]’에는 교체, 탈락과 함께 ‘밟히다’에서 일어난 축약이 일어나므로 ‘학생2’가 쓸 수 없는 단어이다.",
      X(13, "③ ‘겉핥기[거탈끼]’에서는", "교체, 탈락, 축약이 일어난다.")),
    J(4, "부적절", False, [("fig", "f13", "솜이불[솜ː니불]"), ("bogi", "없던 음운이 새로 생기는 첨가")], "해설지",
      "‘색연필[생년필]’에는 교체와 함께 ‘솜이불’에서 일어난 첨가가 일어나므로 ‘학생2’가 쓸 수 없는 단어이다.",
      X(13, "④ ‘색연필[생년필]’에서는", "첨가, 교체가 일어난다.")),
    J(5, "부적절", False, [("fig", "f13", "밟히다[발피다]"), ("bogi", CHUK)], "해설지",
      "‘넓죽하다[넙쭈카다]’에는 탈락, 교체와 함께 ‘밟히다’에서 일어난 축약이 일어나므로 ‘학생2’가 쓸 수 없는 단어이다.",
      X(13, "⑤ ‘넓죽하다[넙쭈카다]’에서는", "탈락, 교체, 축약이 일어난다.")),
]

# ================= 14번
s = Q[14]["stem"]
i = s.index("<학습 활동>", 5)
st = s[:i].replace("[3점]", "").strip()
assert st == "<학습 활동>을 수행한 결과로 적절하지 않은 것은?", st
Q[14]["stem"] = st
Q[14]["stem_underlines"] = ["않은"]
B = s[i + len("<학습 활동>"):].strip()
ik = B.index("ㄱ. ")
il = B.index("ㄴ. ")
INTRO = B[:ik].strip().replace(SP, " ")
G = B[ik:il].strip()
N = B[il:].strip()
assert INTRO.startswith("직접 인용을") and INTRO.endswith("보자．"), INTRO
Q[14]["bogi"] = {"label": "학습 활동", "blocks": [
    {"id": "b1", "type": "para", "text": INTRO, "underlines": []},
    {"id": "b2", "type": "para", "text": G, "underlines": []},
    {"id": "b3", "type": "para", "text": N, "underlines": []}]}
Q[14]["choices"] = [c.replace(SP, " ") for c in Q[14]["choices"]]
Q[14]["answer"] = 4
Q[14]["judgments"] = [
    J(1, "적절", False, [("bogi", "당신은 제 책을 보셨습니까?”라고 물었다")], "해설지",
      "ㄱ은 직접 인용의 높임 표현 ‘보셨-’이 간접 인용에서 ‘보았냐고’로 바뀐다.",
      X(14, "ㄱ은 ‘그는", "높임 표현")),
    J(2, "적절", False, [("bogi", "그녀는 내일 도착합니다.”라고 말했다")], "해설지",
      "ㄴ은 직접 인용의 시간 표현 ‘내일’이 간접 인용에서 ‘오늘’로 바뀐다.",
      X(14, "ㄴ은 ‘나는 어제", "시간 표현(내일→오늘)")),
    J(3, "적절", False, [("bogi", "당신은 제 책을"), ("bogi", "그녀는 내일")], "해설지",
      "ㄱ은 ‘당신’과 ‘제’가 간접 인용에서 ‘내’와 ‘자기’로 바뀌지만, ㄴ의 ‘그녀’는 바뀌지 않는다.",
      X(14, "인용절의 대명사", "→자기(의)")),
    J(4, "부적절", True, [("bogi", "보셨습니까?”라고"), ("bogi", "도착합니다.”라고")], "해설지",
      "ㄱ의 ‘-습니까’도 ‘-냐’로, ㄴ의 ‘-ㅂ니다’도 ‘-ㄴ다’로 바뀌어 두 문장 모두 종결 어미가 바뀌므로 ㄴ만 바뀐다고 할 수 없다.",
      X(14, "ㄴ은 ‘나는 어제", "종결 어미")),
    J(5, "적절", False, [("bogi", "라고 물었다"), ("bogi", "라고 말했다")], "해설지",
      "ㄱ과 ㄴ 모두 직접 인용의 조사 ‘라고’가 간접 인용에서 ‘고’로 바뀐다.",
      X(14, "인용 조사(라고→고)", "인용 조사(라고→고)")),
]

# ================= 15번
s = Q[15]["stem"]
i = s.index("<보 기>")
st = s[:i].strip()
assert st == "<보기>의 ㉠, ㉡에 들어갈 내용으로 적절한 것은?", st
Q[15]["stem"] = st
B = s[i + len("<보 기>"):]
a1 = B.index("[자료1]", B.index("까요?"))
a2 = B.index("[자료2]", a1)
a3 = B.index("학생:")
a4 = B.index("선생님: 네")
b5 = B.index("㉠㉡", a4)
TALK = B[:a1].strip()
T1 = B[a1 + len("[자료1]"):a2].strip()
T2 = B[a2 + len("[자료2]"):a3].strip()
STU = B[a3:a4].strip()
ENDT = B[a4:b5].strip()
assert TALK.startswith("선생님: 중세국어") and TALK.endswith("까요?"), TALK
assert T1.startswith("결합하는 조사") and T1.endswith("나타난다."), T1
assert STU.startswith("학생: [자료1]을") and STU.endswith("합니다."), STU
assert ENDT == "선생님: 네, 맞아요.", ENDT
Q[15]["bogi"] = [
    {"label": "보 기", "blocks": [
        {"id": "b1", "type": "para", "dialogue": True, "text": TALK, "bold": ["선생님"], "underlines": []},
        {"id": "b2", "type": "para", "text": "[자료1]", "underlines": []},
        {"id": "f15a", "type": "figure", "caption": "", "image": "그림_13-15_15_자료1.png", "pdf_text": T1,
         "alt": "[자료1] 표. 관형격 조사 ‘ㅅ’: ‘ㅎ’은 나타나지 않는다. 모음으로 시작하는 조사: ‘ㅎ’은 뒤따르는 모음에 이어 적는다. ‘ㄱ’ 또는 ‘ㄷ’으로 시작하는 조사: ‘ㅎ’은 뒤따르는 ‘ㄱ’, ‘ㄷ’과 어울려 ‘ㅋ’, ‘ㅌ’으로 나타난다."},
        {"id": "b3", "type": "para", "text": "[자료2]", "underlines": []},
        {"id": "f15b", "type": "figure", "caption": "", "image": "그림_13-15_15_자료2.png", "pdf_text": T2,
         "alt": "[자료2] 예1 [내ㅎ+이] 이러 → [빈칸] 이러 (냇물이 이루어져). 예2 부텻 [우ㅎ+과] → 부텻 [빈칸] (부처의 위와)."},
        {"id": "f15c", "type": "figure", "caption": "", "image": "그림_13-15_15_학생.png", "pdf_text": STU,
         "alt": "학생: [자료1]을 보면 [자료2]의 예1은 (㉠)라고 써야 하고, 예2는 (㉡)라고 써야 합니다."},
        {"id": "b4", "type": "para", "dialogue": True, "text": ENDT, "bold": ["선생님"], "underlines": []}]},
    {"label": "", "plain": True, "blocks": [{"id": "h1", "type": "heading", "text": SP + "㉠" + SP * 5 + "㉡",
        "underlines": [{"mark": "", "text": "㉠"}, {"mark": "", "text": "㉡"}]}]},
]
Q[15]["choices"] = [c[:2] + SP * 3 + c[2:] for c in Q[15]["choices"]]
Q[15]["answer"] = 1
R1 = "‘ㅎ’은 뒤따르는 모음에 이어 적는다."
R2 = "‘ㅎ’은 뒤따르는 ‘ㄱ’, ‘ㄷ’과 어울려 ‘ㅋ’, ‘ㅌ’으로 나타난다."
XA = X(15, "‘내ㅎ’와 ‘이’가 결합할 때", "‘내히’라고 써야 한다.")
XB = X(15, "‘우ㅎ’와 ‘과’가 결합할 때", "‘우콰’라고 써야 한다.")
XC = X(15, "따라서 ㉠에는", "쓰는 것이 적절하다.")
Q[15]["judgments"] = [
    J(1, "적절", True, [("fig", "f15a", R1), ("fig", "f15a", R2)], "해설지",
      "‘이’는 모음으로 시작하는 조사라 ‘ㅎ’을 모음에 이어 적어 ㉠은 ‘내히’이고, ‘과’는 ‘ㄱ’으로 시작하는 조사라 ‘ㅎ’이 ‘ㅋ’으로 나타나 ㉡은 ‘우콰’이다.",
      XC),
    J(2, "부적절", False, [("fig", "f15a", R2)], "해설지",
      "㉠은 ‘내히’로 맞지만, ㉡은 ‘ㅎ’이 뒤따르는 ‘ㄱ’과 어울려 ‘ㅋ’으로 나타나야 하므로 ‘우과’가 아니라 ‘우콰’이다.",
      XB),
    J(3, "부적절", False, [("fig", "f15a", R1)], "해설지",
      "㉡은 ‘우콰’로 맞지만, ㉠은 ‘ㅎ’을 뒤따르는 모음에 이어 적어야 하므로 ‘내이’가 아니라 ‘내히’이다.",
      XA),
    J(4, "부적절", False, [("fig", "f15a", "‘ㅎ’은 뒤따르는 모음에 이어 적는다."), ("fig", "f15a", "‘ㅎ’은 뒤따르는 ‘ㄱ’, ‘ㄷ’과 어울려")], "해설지",
      "㉠은 ‘내이’가 아니라 ‘내히’이고, ㉡도 ‘우과’가 아니라 ‘우콰’이므로 둘 다 틀렸다.",
      XC),
    J(5, "부적절", False, [("fig", "f15a", "‘ㅋ’, ‘ㅌ’으로 나타난다.")], "해설지",
      "㉠은 ‘내히’로 맞지만, ㉡은 ‘ㅎ’이 ‘ㄱ’과 어울려 ‘ㅋ’으로 나타난 ‘우콰’여야 하므로 ‘웋과’는 적절하지 않다.",
      XB),
]

for q in d["questions"]:
    assert q["stem"] and len(q["choices"]) == 5 and q["answer"]
json.dump(d, open(HERE + r"\세트_13-15.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok")
