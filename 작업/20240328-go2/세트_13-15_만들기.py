"""2024-03 고2 13~15번(문법 단독 문항, 안내문 없음) 세트 -> 세트_13-15.json
초안은 도구/세트_뽑기.py 로 뽑았다(_임시\초안_13-15.json, 문단시작 '-'). 쪽 그림·texttrace·PDF 선으로 확인한 것:
- 13번: <보기> 상자 하나, 굵은 글씨 없음(type 1 은 문항 번호뿐). 밑줄 ㉠ «어근의 품사를 바꾸는 접사가 붙어 이루어진 단어». 발문 밑줄 '않은'.
- 14번: <보기> 상자 = 학생·선생님 대화(말한 이만 굵게, 콜론은 보통) + 안쪽 상자 [자료](굵게, ㉠㉡ 항목) + [탐구 과정]·[탐구 결과](굵게).
  ⓐ ⓑ ⓒ 는 네모 빈칸(boxed). 선지는 ⓐ ⓑ ⓒ 표(머리는 plain 상자, 표 테두리 table_border).
- 15번: <보기 1>(밑줄 ㉠~㉢) <보기 2>(옛한글 PUA 본문은 쪽에서 오려 낸 그림 display_image, 밑줄 ⓐ~ⓔ) + [현대어 풀이](굵게).
  선지는 ㉠ ㉡ ㉢ 표.
"""
import json
import re

HERE = r"D:\Work\블로그\리딩맵\작업\20240328-go2"
d = json.load(open(HERE + r"\_임시\초안_13-15.json", encoding="utf-8"))
d.pop("raw_passage_lines", None)
d["meta"] = {"exam": "2024학년도 3월 고2 전국연합학력평가 국어", "exam_id": "20240328-go2", "area": "문법",
             "topic": "파생어, 자음군 단순화와 된소리되기, 중세 국어의 주격 조사",
             "problem_pdf": "20240328-go2-problem-kor_mun_28P1134K.pdf",
             "explanation_pdf": "20240328-go2-explanation-kor_hsj_WJ2WB32J.pdf"}
d["guide"] = None
d["passage"] = []
Q = {q["no"]: q for q in d["questions"]}
SP = "\u3000"
expl = open(HERE + r"\해설_글자.txt", encoding="utf-8").read()


def section(no):
    i = expl.index(f"\n{no}. [출제의도]")
    j = expl.index(f"\n{no + 1}. [출제의도]", i) if no < 15 else expl.index("[16", i)
    return expl[i:j]


def X(no, a, b):
    sec = section(no)
    keep = [(i, c) for i, c in enumerate(sec) if not c.isspace()]
    comp = "".join(c for _, c in keep)
    ca, cb = re.sub(r"\s+", "", a), re.sub(r"\s+", "", b)
    ia = comp.index(ca)
    ib = comp.index(cb, ia) + len(cb)
    return sec[keep[ia][0]: keep[ib - 1][0] + 1].replace("\n", "")


def J(choice, verdict, ans, ev, basis, reason, xq=None):
    out = {"choice": choice, "verdict": verdict, "is_answer": ans, "basis": basis, "reason": reason,
           "evidence": [{"source": "bogi", "para": None, "quote": e} for e in ev]}
    if xq:
        out["explanation_quote"] = xq
    return out


# ---------------- 13번
s = Q[13]["stem"]
Q[13]["stem"] = s[: s.index("것은?") + 3]
Q[13]["stem_underlines"] = ["않은"]
body = s[s.index("< 보 기 >") + len("< 보 기 >"):]
U13 = "어근의 품사를 바꾸는 접사가 붙어 이루어진 단어"
assert "㉠" + U13 in body and body.endswith("명사가 된 것이다."), body
Q[13]["bogi"] = {"label": "보 기", "blocks": [
    {"id": "b1", "type": "para", "text": body, "underlines": [{"mark": "㉠", "text": U13}]}]}
Q[13]["answer"] = 1
Q[13]["judgments"] = [
    J(1, "부적절", True, [U13, "예를 들어 명사 ‘웃음’은 동사 ‘웃다’의 어근 ‘웃-’에 접사 ‘-음’이 붙어 명사가 된 것이다."], "해설지",
      "‘일찍이’는 부사 어근 ‘일찍’에 접사 ‘-이’가 붙어 부사가 된 단어이므로, 접사가 어근의 품사를 바꾸지 않아 ㉠의 예로 적절하지 않다.",
      X(13, "‘일찍이’는", "적절하지 않다.")),
    J(2, "적절", False, [U13], "해설지",
      "‘마음껏’은 명사 어근 ‘마음’에 접사 ‘-껏’이 붙어 부사로 바뀐 단어이므로 ㉠의 예로 적절하다.",
      X(13, "②‘마음껏’은", "부사로 바뀌었다.")),
    J(3, "적절", False, ["또한 파생어 중에는 ㉠어근의 품사를 바꾸는 접사가 붙어"], "해설지",
      "‘가리개’는 동사 어근 ‘가리-’에 접사 ‘-개’가 붙어 명사로 바뀐 단어이므로 ㉠의 예로 적절하다.",
      X(13, "③‘가리개’는", "명사로 바뀌었다.")),
    J(4, "적절", False, ["명사 ‘웃음’은 동사 ‘웃다’의 어근 ‘웃-’에 접사 ‘-음’이 붙어 명사가 된 것이다."], "해설지",
      "‘높이다’는 형용사 어근 ‘높-’에 접사 ‘-이’가 붙어 동사로 바뀐 단어이므로 ㉠의 예로 적절하다.",
      X(13, "④‘높이다’는", "동사로 바뀌었다.")),
    J(5, "적절", False, ["파생어 중에는 ㉠어근의 품사를 바꾸는 접사가 붙어 이루어진 단어도 있다."], "해설지",
      "‘슬기롭다’는 명사 어근 ‘슬기’에 접사 ‘-롭-’이 붙어 형용사로 바뀐 단어이므로 ㉠의 예로 적절하다.",
      X(13, "⑤‘슬기롭다’는", "형용사로 바뀌었다.")),
]

# ---------------- 14번
s = Q[14]["stem"]
Q[14]["stem"] = s[: s.index("것은?") + 3]
body = s[s.index("< 보 기 >") + len("< 보 기 >"):]
assert body.endswith("발음된다.ⓐⓑⓒ"), body[-20:]
body = body[: -len("ⓐⓑⓒ")]
i_t = body.index("선생님:")
i_j = body.index("[자료]")
i_a = body.index("㉠ 자음군")
i_b = body.index("㉡ 된소리")
i_p = body.index("[탐구 과정]")
i_1 = body.index("1. ‘읽고’")
i_2 = body.index("2. ㉠이")
i_3 = body.index("3. ㉡이")
i_r = body.index("[탐구 결과]")
parts = {
    "st": body[:i_t].strip(), "te": body[i_t:i_j].strip(), "ja": body[i_j:i_a].strip(),
    "a": body[i_a:i_b].strip(), "b": body[i_b:i_p].strip(), "pg": body[i_p:i_1].strip(),
    "p1": body[i_1:i_2].strip(), "p2": body[i_2:i_3].strip(), "p3": body[i_3:i_r].strip(),
    "rh": body[i_r:i_r + len("[탐구 결과]")], "rt": body[i_r + len("[탐구 결과]"):].strip()}
assert parts["pg"] == "[탐구 과정]" and parts["ja"] == "[자료]"
assert parts["p2"].endswith("일어나는 ⓐ") and parts["p3"].endswith("설명할 수 ⓒ")
Q[14]["bogi"] = [
    {"label": "보 기", "blocks": [
        {"id": "b1", "type": "para", "dialogue": True, "text": parts["st"], "bold": ["학생"], "underlines": []},
        {"id": "b2", "type": "para", "dialogue": True, "text": parts["te"], "bold": ["선생님"], "underlines": []},
        {"id": "j0", "type": "para", "text": parts["ja"], "bold": ["[자료]"], "underlines": [], "inbox": "자료"},
        {"id": "j1", "type": "para", "text": parts["a"], "underlines": [], "inbox": "자료"},
        {"id": "j2", "type": "para", "text": parts["b"], "underlines": [], "inbox": "자료"},
        {"id": "g0", "type": "para", "text": parts["pg"], "bold": ["[탐구 과정]"], "underlines": []},
        {"id": "g1", "type": "para", "text": parts["p1"], "underlines": []},
        {"id": "g2", "type": "para", "text": parts["p2"], "underlines": [], "boxed": ["ⓐ"]},
        {"id": "g3", "type": "para", "text": parts["p3"], "underlines": [], "boxed": ["ⓑ", "ⓒ"]},
        {"id": "r0", "type": "para", "text": parts["rh"], "bold": ["[탐구 결과]"], "underlines": []},
        {"id": "r1", "type": "para", "text": parts["rt"], "underlines": []}]},
    {"label": "", "plain": True, "blocks": [
        {"id": "th", "type": "heading", "text": "ⓐ" + SP * 9 + "ⓑ" + SP * 9 + "ⓒ",
         "underlines": [{"mark": "", "text": t} for t in ("ⓐ", "ⓑ", "ⓒ")]}]},
]
Q[14]["table_border"] = True
for k, c in enumerate(Q[14]["choices"]):
    m = re.fullmatch(r"(조건이다\.|조건이 아니다\.)(\[ㄱ\]|\[ㄲ\])(없다\.|있다\.)", c)
    assert m, c
    Q[14]["choices"][k] = (SP * 2).join(m.groups())
A14 = "종성 [ㄹ] 뒤에 ‘ㄱ’이 연결된다는 것은 ㉡이 반드시 일어나는 ⓐ"
B14 = "둘째 음절의 초성이 ⓑ로 발음된다."
C14 = "그 후 ㉠이 일어난다고 하면 ‘읽고’의 발음을 설명할 수 ⓒ"
for q in (A14, B14, C14):
    assert re.sub(r"\s", "", q) in re.sub(r"\s", "", body), q
xa = X(14, "따라서 종성 [ㄹ] 뒤에", "들어간다.")
xb = X(14, "된소리되기가 일어나 둘째", "들어간다.")
xc = X(14, "그 후 첫째 음절 종성에서", "들어간다.")
Q[14]["answer"] = 4
Q[14]["judgments"] = [
    J(1, "부적절", False, [A14], "해설지",
      "ⓐ에는 ‘조건이 아니다’가 들어간다. 자음군 단순화가 먼저 일어나도 종성 [ㄹ] 뒤에서는 된소리되기가 일어나지 않으므로 ‘조건이다’는 맞지 않다.", xa),
    J(2, "부적절", False, [A14], "해설지",
      "ⓐ가 ‘조건이 아니다’여야 하므로 ‘조건이다’로 시작하는 짝은 맞지 않다.", xa),
    J(3, "부적절", False, [B14], "해설지",
      "된소리되기가 먼저 일어나면 둘째 음절의 초성은 [ㄱ]이 아니라 [ㄲ]로 발음되므로 ⓑ에 [ㄱ]은 맞지 않다.", xb),
    J(4, "적절", True, [A14, B14, C14], "해설지",
      "ⓐ에는 ‘조건이 아니다’, ⓑ에는 [ㄲ], ⓒ에는 ‘있다’가 들어가므로 바르게 짝지은 것이다.",
      X(14, "따라서 종성 [ㄹ] 뒤에", "ⓒ에는 ‘있다’가 들어간다.")),
    J(5, "부적절", False, [C14], "해설지",
      "된소리되기 뒤에 자음군 단순화가 일어나면 [일꼬]의 발음을 설명할 수 있으므로 ⓒ에는 ‘없다’가 아니라 ‘있다’가 들어간다.", xc),
]

# ---------------- 15번
s = Q[15]["stem"]
Q[15]["stem"] = s[: s.index("것은?") + 3]
body = s[s.index("< 보기 1 >") + len("< 보기 1 >"):]
assert body.endswith("㉠㉡㉢"), body[-10:]
body = body[:-3]
i2 = body.index("< 보기 2 >")
b1 = body[:i2].strip()
rest = body[i2 + len("< 보기 2 >"):]
ih = rest.index("[현대어 풀이]")
b2 = rest[:ih].strip()
b3 = rest[ih:].strip()
assert b2.startswith("孟宗(맹종)") and b2.endswith("\uf537더라"), ascii(b2)
Q[15]["bogi"] = [
    {"label": "보기 1", "blocks": [{"id": "b1", "type": "para", "text": b1, "underlines": [
        {"mark": "㉠", "text": "자음 다음에는 ‘이’가 나타났고"},
        {"mark": "㉡", "text": "모음 ‘이’나 반모음 ‘ㅣ’ 다음에는 나타나지 않았다"},
        {"mark": "㉢", "text": "모음 ‘이’도 반모음 ‘ㅣ’도 아닌 모음 다음에는 ‘ㅣ’가 나타났다"}]}]},
    {"label": "보기 2", "blocks": [
        {"id": "c1", "type": "para", "text": b2, "display_image": "그림_13-15_15_보기2본문.png", "underlines": [
            {"mark": "ⓐ", "text": "\ue560\ued8f미"}, {"mark": "ⓑ", "text": "어미"},
            {"mark": "ⓒ", "text": "겨\ued6b리"}, {"mark": "ⓓ", "text": "줄기"},
            {"mark": "ⓔ", "text": "孝道(효도)ㅣ"}]},
        {"id": "c2", "type": "para", "text": b3, "bold": ["[현대어 풀이]"], "underlines": []}]},
    {"label": "", "plain": True, "blocks": [
        {"id": "th", "type": "heading", "text": "㉠" + SP * 10 + "㉡" + SP * 10 + "㉢",
         "underlines": [{"mark": "", "text": t} for t in ("㉠", "㉡", "㉢")]}]},
]
Q[15]["table_border"] = True
CELLS = [("ⓐ", "ⓒ, ⓔ", "ⓑ, ⓓ"), ("ⓐ, ⓒ", "ⓓ", "ⓑ, ⓔ"), ("ⓐ, ⓒ", "ⓑ, ⓓ", "ⓔ"),
         ("ⓑ, ⓔ", "ⓒ, ⓓ", "ⓐ"), ("ⓔ", "ⓑ, ⓓ", "ⓐ, ⓒ")]
for k, cells in enumerate(CELLS):
    assert re.sub(r"\s", "", Q[15]["choices"][k]) == re.sub(r"\s", "", "".join(cells)), (k, Q[15]["choices"][k])
    Q[15]["choices"][k] = (SP * 3).join(cells)
R1 = "㉠자음 다음에는 ‘이’가 나타났고,"
R2 = "㉡모음 ‘이’나 반모음 ‘ㅣ’ 다음에는 나타나지 않았다."
R3 = "㉢모음 ‘이’도 반모음 ‘ㅣ’도 아닌 모음 다음에는 ‘ㅣ’가 나타났다."
ex1 = X(15, "나타났으므로 ⓐ와 ⓒ는", "㉠에 해당한다.")
ex2 = X(15, "ⓑ는 모음 ‘이’로 끝나는", "㉡에 해당한다.")
ex3 = X(15, "ⓔ는 모음 ‘이’도", "해당한다.")
Q[15]["answer"] = 3
Q[15]["judgments"] = [
    J(1, "부적절", False, [R1, "ⓒ겨\ued6b리"], "해설지",
      "ⓒ는 자음 ‘ㄹ’로 끝나는 체언 뒤에 주격 조사 ‘이’가 나타났으므로 ㉠에 들어가야 한다. ⓒ를 ㉡에 넣은 분류는 맞지 않다.", ex1),
    J(2, "부적절", False, [R2, "ⓑ어미"], "해설지",
      "ⓑ와 ⓓ는 모음 ‘이’로 끝나는 체언 뒤에 주격 조사가 나타나지 않았으므로 둘 다 ㉡에 해당한다. ⓓ만 ㉡에 넣은 분류는 맞지 않다.", ex2),
    J(3, "적절", True, [R1, R2, R3], "해설지",
      "ⓐ·ⓒ는 자음 뒤에 ‘이’가 나타나 ㉠, ⓑ·ⓓ는 모음 ‘이’ 뒤에 주격 조사가 나타나지 않아 ㉡, ⓔ는 ‘ㅗ’ 뒤에 ‘ㅣ’가 나타나 ㉢이므로 바른 분류이다.",
      X(15, "ⓐ와 ⓒ는 ㉠에 해당한다.", "해당한다.")),
    J(4, "부적절", False, [R3, "ⓔ孝道(효도)ㅣ"], "해설지",
      "ⓔ는 모음 ‘이’도 반모음 ‘ㅣ’도 아닌 모음 ‘ㅗ’ 뒤에 주격 조사 ‘ㅣ’가 나타났으므로 ㉢에 해당한다. ⓔ를 ㉠에 넣은 분류는 맞지 않다.", ex3),
    J(5, "부적절", False, [R1, "ⓔ孝道(효도)ㅣ"], "해설지",
      "ⓔ는 ㉠이 아니라 ㉢에 해당하고, ⓐ와 ⓒ는 ㉠에 들어가야 하므로 ㉠에 ⓔ만 넣은 분류는 맞지 않다.", ex1),
]
for q in d["questions"]:
    assert len(q["choices"]) == 5 and len(q["judgments"]) == 5 and q["stem"]
json.dump(d, open(HERE + r"\세트_13-15.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok")
