"""2026-09 고1 7~10번(문법 단독 문항) 세트 -> 세트_7-10.json

초안: _임시/뽑기_7-16.py(세트_뽑기.py 복사본, 선지 앞 공백 줄 인식만 고침)로 초안_7-10.json.
쪽 그림·PDF 좌표로 확인한 것(2026-11-25):
- 안내문·지문 없음(guide null, passage []).
- 7번: 설명 문단 + 글 속 네모 빈칸 ㉠(PDF 에서 '(' ')' 는 흰 글씨라 안 보이고 상자만 보임) + [자료](굵게) + ⓐ~ⓒ 세 줄(밑줄 없음).
- 8번: 옛한글 PUA 가 든 줄 3개는 그림(그림_7-10_8_보기1~3, display_image), 넷째 줄(耶輸ㅣ)은 글자.
  밑줄 ㉠ 하늘히 ㉡ 아들 ㉢ 뜯들 ㉣ 耶輸ㅣ(원문자는 밑줄 밖).
- 9번: ㄱ~ㄹ 네 줄. 발문 밑줄 '않은'.
- 10번: 선생님·학생 대화(말한 이만 굵게, 콜론은 type 0). 학생 줄은 빈칸 밑줄 위 [A]. [자료] 굵게.
- 발문 '않은' 밑줄은 8·9·10번.
"""
import json
import re

HERE = r"D:\Work\블로그\리딩맵\작업\20260902-go1"
d = json.load(open(HERE + r"\초안_7-10.json", encoding="utf-8"))
d.pop("raw_passage_lines", None)
d["meta"] = {"exam": "2026년 9월 고1 전국연합학력평가 국어", "exam_id": "20260902-go1", "area": "문법",
             "topic": "주체 높임·중세 국어의 특징·시제·음운 변동", "problem_pdf": "20260902-go1-problem-kor_mun_R6T8BQ7T.pdf",
             "explanation_pdf": "20260902-go1-explanation-kor_hsj_T9W3IK85.pdf"}
d["guide"] = None
d["passage"] = []
Q = {q["no"]: q for q in d["questions"]}

expl = open(HERE + r"\해설_글자.txt", encoding="utf-8").read()


def section(no):
    i = expl.index(f"\n{no}. [출제 의도]")
    cands = [expl.find(m, i + 5) for m in (f"\n{no + 1}. [출제 의도]", "\n** ")]
    j = min(c for c in cands if c > 0)
    return expl[i:j]


def X(no, a, b):
    """해설지 그 문항 해설에서 a 로 시작해 b 로 끝나는 글(줄바꿈만 이어 붙임)."""
    sec = section(no)
    keep = [(i, c) for i, c in enumerate(sec) if not c.isspace()]
    comp = "".join(c for _, c in keep)
    ca, cb = re.sub(r"\s+", "", a), re.sub(r"\s+", "", b)
    ia = comp.index(ca)
    ib = comp.index(cb, ia) + len(cb)
    return sec[keep[ia][0]: keep[ib - 1][0] + 1].replace("\n", "")


def between(s, a, b):
    i = s.index(a)
    return s[i: s.index(b, i) + len(b)]


def J(choice, verdict, ans, ev, basis, reason, xq=None):
    out = {"choice": choice, "verdict": verdict, "is_answer": ans, "basis": basis, "reason": reason,
           "evidence": [{"source": "bogi", "para": None, "quote": e} for e in ev]}
    if xq:
        out["explanation_quote"] = xq
    return out


# ---- 7번
s7 = Q[7]["stem"]
Q[7]["stem"] = s7[: s7.index("<보 기>")].strip()
b7 = s7[s7.index("<보 기>") + len("<보 기>"):]
t7a = b7[: b7.index("[자료]ⓐ")].strip()
assert "(   ㉠   )" in t7a
t7a = t7a.replace("(   ㉠   )", "㉠")  # PDF 의 괄호는 흰 글씨라 원본에 안 보인다
d["meta"]["textlayer_subs"] = {"(   ㉠   )": "㉠"}
L7 = [between(b7, "ⓐ", "아름다우시다."), between(b7, "ⓑ", "읽으신다."), between(b7, "ⓒ", "주무신다.")]
Q[7]["bogi"] = {"label": "< 보 기 >", "blocks": [
    {"id": "b1", "type": "para", "text": t7a, "underlines": [], "boxed": ["㉠"]},
    {"id": "b2", "type": "para", "text": "[자료]", "underlines": [], "bold": ["[자료]"]},
] + [{"id": f"e{k+1}", "type": "para", "text": t, "underlines": []} for k, t in enumerate(L7)]}

# ---- 8번
s8 = Q[8]["stem"]
Q[8]["stem"] = s8[: s8.index("<보 기>")].strip()
Q[8]["stem_underlines"] = ["않은"]
b8 = s8[s8.index("<보 기>") + len("<보 기>"):]
parts8 = re.split(r"∙", b8)[1:]
assert len(parts8) == 4
items8 = []
head8 = {}
imgs = {0: "그림_7-10_8_보기1.png", 1: "그림_7-10_8_보기2.png", 2: "그림_7-10_8_보기3.png"}
ULM = ["㉠", "㉡", "㉢", "㉣"]
for k, p in enumerate(parts8):
    p = p.strip()
    i = p.index("[")
    head, gloss = "∙" + p[:i].strip(), p[i:].strip()
    head8[k] = head
    mark = ULM[k]
    word = head[head.index(mark) + 1: head.index("(")]
    it = {"id": f"s{k+1}", "type": "para", "text": head, "underlines": [{"mark": mark, "text": word}]}
    if k in imgs:
        it["display_image"] = imgs[k]
    items8.append(it)
    items8.append({"id": f"g{k+1}", "type": "para", "text": gloss.replace("\u3000", " "), "underlines": []})
Q[8]["bogi"] = {"label": "< 보 기 >", "blocks": items8}

# ---- 9번
s9 = Q[9]["stem"]
Q[9]["stem"] = s9[: s9.index("<보 기>")].replace("[3점]", "").strip()
Q[9]["stem_underlines"] = ["않은"]
L9 = ["ㄱ. 내 친구가 맑은 하늘을 가리킨다.", "ㄴ. 그녀는 집에 가는 동생을 잡는다.", "ㄷ. 이것은 그가 아까 나에게 준 그림이다.",
      "ㄹ. 나는 동생이 심은 사과나무를 지금 본다."]
assert "".join(L9) == s9[s9.index("ㄱ."):]
Q[9]["bogi"] = {"label": "< 보 기 >", "blocks": [{"id": f"e{k+1}", "type": "para", "text": t, "underlines": []} for k, t in enumerate(L9)]}

# ---- 10번
s10 = Q[10]["stem"]
Q[10]["stem"] = s10[: s10.index("<보 기>")].strip()
Q[10]["stem_underlines"] = ["않은"]
b10 = s10[s10.index("<보 기>") + len("<보 기>"):]
t_t = between(b10, "음운 변동의 유형에는", "말해 볼까요?")
jar = b10[b10.index("[자료]  ") + len("[자료]"):].strip()
UL10 = {"㉠": "깊숙한[깁쑤칸]", "㉡": "가득히[가드키]", "㉢": "늦여름[는녀름]", "㉣": "붉게[불께]", "㉤": "단풍잎[단풍닙]",
        "㉥": "따뜻한[따뜨탄]", "㉦": "간지럽히던[간지러피던]"}
for m, t in UL10.items():
    assert m + t in jar, (m, t)
Q[10]["bogi"] = {"label": "< 보 기 >", "blocks": [
    {"id": "b1", "type": "para", "dialogue": True, "text": "선생님: " + t_t, "underlines": [], "bold": ["선생님"]},
    {"id": "b2", "type": "para", "dialogue": True, "text": "학생: [A]", "underlines": [], "bold": ["학생"], "blank": "[A]"},
    {"id": "b3", "type": "para", "dialogue": True, "text": "선생님: 네, 맞습니다.", "underlines": [], "bold": ["선생님"]},
    {"id": "b4", "type": "para", "text": "[자료]", "underlines": [], "bold": ["[자료]"]},
    {"id": "b5", "type": "para", "text": jar, "underlines": [{"mark": m, "text": t} for m, t in UL10.items()]},
]}

# ================= 판단
Q[7]["answer"] = 2
K7 = "점이 ‘아버지께서 산에 다녀오셨다.’와 같다."
assert K7 in b7
X7a = X(7, "[자료]의 ⓐ는", "사용했다.")
Q[7]["judgments"] = [
    J(1, "부적절", False, [L7[0], K7], "해설지",
      "ⓐ는 ‘눈이 아름다우시다’에서 선어말 어미로 주체 ‘어머니’를 간접적으로 높였다. ‘아버지께서 산에 다녀오셨다.’는 주체를 직접 높인 문장이므로 같은 점이 아니다.", X7a),
    J(2, "적절", True, [L7[1], K7], "해설지",
      "ⓑ의 ‘할머니께서는 … 읽으신다’는 주체 ‘할머니’를 직접 높이기 위해 주격 조사 ‘께서’와 선어말 어미를 쓴 문장이다. ‘아버지께서 산에 다녀오셨다.’도 같은 방식으로 주체를 직접 높였다.",
      X(7, "[자료]의 ⓑ는", "사용했고,")),
    J(3, "부적절", False, [L7[2], "주체 높임은 선어말 어미 ‘－(으)시－’, 주격 조사 ‘께서’, 특수 어휘 등을 통해 표현된다."], "해설지",
      "ⓒ의 ‘주무신다’는 특수 어휘이고 주체 ‘할아버지’를 직접 높인다. 그러나 ‘아버지께서 산에 다녀오셨다.’는 특수 어휘가 아니라 주격 조사와 선어말 어미로 높였으므로 같은 점이 아니다.",
      X(7, "[자료]의 ⓒ는", "사용했고,")),
    J(4, "부적절", False, [L7[0], L7[2]], "해설지",
      "ⓐ의 선어말 어미는 주체를 직접이 아니라 간접적으로 높인다. 그러므로 ⓐ와 ⓒ가 모두 직접 높인다는 말이 틀렸다.", X7a),
    J(5, "부적절", False, [L7[2], K7], "해설지",
      "ⓒ의 ‘아프셔서’는 주체를 간접적으로 높이지만, ‘아버지께서 산에 다녀오셨다.’는 주체를 직접 높인 문장이다. 간접 높임만으로는 같은 점이 되지 않는다.",
      X(7, "[자료]의 ⓒ는", "사용했다.")),
]

Q[8]["answer"] = 3
Q[8]["judgments"] = [
    J(1, "적절", False, [head8[0]], "해설지",
      "㉠의 ‘하ᄂᆞᆯ’은 ㅎ이 끝소리로 붙은 체언이다. ㅎ 뒤에 주격 조사가 이어진 ‘하ᄂᆞᆯ히’에서 ㅎ 종성 체언을 확인할 수 있다.",
      X(8, "①", "있다.")),
    J(2, "적절", False, [head8[2]], "해설지",
      "㉢의 ‘ᄠᅳᆮ’은 첫소리가 자음 둘 이상으로 이루어진 어두 자음군(ㅳ)을 보여 준다.",
      X(8, "②", "있다.")),
    J(3, "부적절", True, [head8[1], head8[2]], "해설지",
      "㉡ ‘아ᄃᆞᄅᆞᆯ’은 양성 모음끼리, ㉢ ‘ᄠᅳ들’은 음성 모음끼리 어울리는 모음 조화를 보여 준다. 두 곳 모두 모음 조화가 확인되므로 ㉡과 달리 ㉢에서만 확인한다는 말이 틀렸다.",
      X(8, "㉡에서는", "있다.")),
    J(4, "적절", False, [head8[0], head8[3]], "해설지",
      "㉠은 ㅎ 뒤에서 주격 조사 ‘이’가 쓰였고, ㉣은 ‘ㅣ’ 계열이 아닌 모음 뒤에서 주격 조사 ‘ㅣ’가 쓰였다. ㉣에서만 주격 조사 ‘ㅣ’를 확인한다는 말이 맞다.",
      X(8, "④", "있다.")),
    J(5, "적절", False, [head8[1], head8[2]], "해설지",
      "㉡은 ‘ㄹ’을, ㉢은 ‘ㄷ’을 다음 글자의 첫소리로 내려 적었다. 두 곳 모두 이어 적기를 확인할 수 있다.",
      X(8, "⑤", "있다.")),
]

Q[9]["answer"] = 1
Q[9]["judgments"] = [
    J(1, "부적절", True, [L9[0]], "해설지",
      "ㄱ의 ‘맑은’은 관형사형 어미 ‘-은’이 쓰여 현재 시제를 나타내고, ‘가리킨다’의 선어말 어미 ‘-ㄴ-’도 현재 시제를 나타낸다. 관형사형 어미로 과거 시제가 실현된다는 앞부분이 틀렸다.",
      X(9, "ㄱ에서 형용사", "실현된다.")),
    J(2, "적절", False, [L9[1]], "해설지",
      "ㄴ은 ‘가는’의 관형사형 어미 ‘-는’과 ‘잡는다’의 선어말 어미 ‘-는-’으로 현재 시제가 실현된다.",
      X(9, "②", "실현된다.")),
    J(3, "적절", False, [L9[2]], "해설지",
      "ㄷ은 시간 부사 ‘아까’와 ‘준’의 관형사형 어미 ‘-ㄴ’으로 과거 시제가 실현된다.",
      X(9, "③", "실현된다.")),
    J(4, "적절", False, ["동생이 심은 사과나무를"], "해설지",
      "ㄹ의 ‘심은’은 관형사형 어미 ‘-은’으로 과거 시제가 실현된다.",
      X(9, "④", "실현된다.")),
    J(5, "적절", False, ["사과나무를 지금 본다."], "해설지",
      "ㄹ은 시간 부사 ‘지금’과 ‘본다’의 선어말 어미 ‘-ㄴ-’으로 현재 시제가 실현된다.",
      X(9, "⑤", "실현된다.")),
]

Q[10]["answer"] = 5
Q[10]["judgments"] = [
    J(1, "적절", False, ["㉡가득히[가드키]"], "해설지",
      "㉡은 ‘득’의 ㄱ과 ‘히’의 ㅎ이 합쳐져 ㅋ이 되는 축약이 일어나 음운의 개수가 줄었다.",
      X(10, "①", "줄었다.")),
    J(2, "적절", False, ["㉢늦여름[는녀름]"], "해설지",
      "㉢은 ㅈ이 ㄷ으로, ㄷ이 ㄴ으로 바뀌는 교체와 ㄴ이 추가되는 첨가가 일어나 음운의 개수가 늘었다.",
      X(10, "②", "늘었다.")),
    J(3, "적절", False, ["㉣붉게[불께]"], "해설지",
      "㉣은 ㄱ이 ㄲ으로 바뀌는 교체와 ‘붉’의 ㄱ이 없어지는 탈락이 일어나 음운의 개수가 줄었다.",
      X(10, "③", "줄었다.")),
    J(4, "적절", False, ["㉠깊숙한[깁쑤칸]", "㉥따뜻한[따뜨탄]"], "해설지",
      "㉠은 ㅍ이 ㅂ으로, ㅅ이 ㅆ으로 바뀌는 교체와 ㄱ과 ㅎ이 합쳐져 ㅋ이 되는 축약이 일어났다. ㉥은 ㅅ이 ㄷ으로 바뀌는 교체가 일어난 뒤 ㄷ과 ㅎ이 합쳐져 ㅌ이 되는 축약이 일어났다. 둘 다 음운의 개수가 줄었다.",
      X(10, "④", "줄었다.")),
    J(5, "부적절", True, ["㉤단풍잎[단풍닙]", "㉦간지럽히던[간지러피던]"], "해설지",
      "㉤은 ㄴ이 추가되는 첨가와 ㅍ이 ㅂ으로 바뀌는 교체로 음운의 개수가 늘었고, ㉦은 축약으로 개수가 줄었다. 둘 다 개수가 변하지 않았다는 말이 틀렸다.",
      X(10, "㉤의", "줄었다.")),
]

json.dump(d, open(HERE + r"\세트_7-10.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok")
