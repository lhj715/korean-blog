"""2025-06 고2 13~15번(문법 단독 문항) 세트: 초안 + 쪽 그림 확인값 + 해설지 기반 판단 -> 세트_13-15.json

초안은 도구/세트_뽑기.py 로 뽑았다(_임시\초안_13-15.json, 안내문 없음). 쪽 그림(문제_5쪽_오른쪽, 문제_6쪽_왼쪽)으로 확인한 것:
- 안내문·지문 없음(guide null, passage []). 발문 밑줄 '않은'(13·15번).
- 13번: <보기> 상자 = 월인석보 인용(옛한글 PUA 다수 -> 문단 전체를 쪽에서 오려 낸 그림 display_image) + 출처 줄 + [현대어 풀이](굵게).
  밑줄 ㉠~㉤. 굵은 글씨는 «[현대어 풀이]» 만(type 0+1).
- 14번: <보기> 상자와 <조건> 상자(굵은 글씨 없음).
- 15번: <보기> 상자 = 학생·선생님 대화(말한 이와 콜론 굵게, Dotum 글꼴 type 0+1) + 안쪽 상자 [학습 과제](굵게)와 ㆍ 예문 5줄(밑줄 ㉠~㉤).
  선지는 «과제 / 적절성 판단 / 적절성 판단의 근거» 표(머리는 plain 상자, 표 테두리 table_border).
"""
import json
import re

HERE = r"D:\Work\블로그\리딩맵\작업\20250604-go2"
d = json.load(open(HERE + r"\_임시\초안_13-15.json", encoding="utf-8"))
d.pop("raw_passage_lines", None)
d["meta"] = {"exam": "2025년 6월 고2 전국연합학력평가 국어", "exam_id": "20250604-go2", "area": "문법",
             "topic": "중세 국어의 특징·관형사절의 시제·보조 용언의 띄어쓰기",
             "problem_pdf": "20250604-go2-problem-kor_mun_626F7113.pdf",
             "explanation_pdf": "20250604-go2-explanation-kor_hsj_1D4PC7B2.pdf"}
d["guide"] = None
d["passage"] = []
Q = {q["no"]: q for q in d["questions"]}
SP = "\u3000"
expl = open(HERE + r"\해설_글자.txt", encoding="utf-8").read()


def section(no):
    i = expl.index(f"\n{no}. [출제의도]")
    j = expl.index(f"\n{no + 1}. [출제의도]", i) if no < 15 else expl.index("[16~20]", i)
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
s13 = Q[13]["stem"]
Q[13]["stem"] = s13[: s13.index("것은?") + 3]
Q[13]["stem_underlines"] = ["않은"]
Q[13]["choices"][4] = Q[13]["choices"][4].split("━")[0]
t = s13[s13.index("보 기>") + 4:]
i_src = t.index("- \uf000월인석보")
i_hd = t.index("[현대어 풀이]")
main13 = t[:i_src]
src13 = t[i_src: i_hd]
mod13 = t[i_hd:]
assert main13.startswith("그\ue7b4") and main13.endswith("쇼셔") and src13 == "- \uf000월인석보\uf000(1449) -", (main13, src13)
ULS = [("㉠", "出家(출가)\uf537샤"), ("㉡", "\uea05믈"), ("㉢", "누\ue895며"), ("㉣", "\ue38a\ue470"), ("㉤", "니\ue46c쇼셔")]
for m, u in ULS:
    assert u in main13, (m, u)
Q[13]["bogi"] = {"label": "보 기", "blocks": [
    {"id": "b1", "type": "para", "text": main13, "display_image": "그림_13-15_13_보기본문.png",
     "underlines": [{"mark": m, "text": u} for m, u in ULS]},
    {"id": "n1", "type": "note", "text": src13.replace("월인석보", "『월인석보』"), "underlines": []},
    {"id": "b2", "type": "para", "text": mod13, "bold": ["[현대어 풀이]"], "underlines": []},
]}
x13 = X(13, "㉢의", "아니다")
Q[13]["answer"] = 3
Q[13]["judgments"] = [
    J(1, "적절", False, ["그때에 선혜가 부처님께 가서 출가하시어"], "해설지",
      "㉠은 현대어 ‘출가하시어’에 해당하며, 선어말 어미 ‘-샤-’가 주체인 ‘善慧(선혜)’를 높이고 있다.",
      X(13, "①㉠은", "높이고 있다")),
    J(2, "적절", False, ["다섯 가지 꿈을 꾸니", "㉡\uea05믈"], "해설지",
      "㉡은 현대어 ‘꿈을’에 해당하며, 어두자음군 ‘ㅺ’을 사용하고 있다. 초성에 서로 다른 두 자음이 함께 표기되었다.",
      X(13, "②㉡은", "사용하고 있다")),
    J(3, "부적절", True, ["하나는 바다에 누우며", "㉢누\ue895며"], "해설지",
      "㉢의 ‘누며’는 현대어 ‘누우며’에 해당하는 것으로, 높임의 의미를 나타내는 특수 어휘가 아니다.", x13),
    J(4, "적절", False, ["다섯은 손에 달을 잡으니", "㉣\ue38a\ue470"], "해설지",
      "㉣은 현대어 ‘달을’에 해당하며, 체언에 목적격 조사가 결합할 때 모음 조화가 지켜졌다.",
      X(13, "④㉣은", "지켜진 것이다")),
    J(5, "적절", False, ["나를 위하여 이르소서", "㉤니\ue46c쇼셔"], "해설지",
      "㉤은 현대어 ‘이르소서’에 해당하며, 단어의 첫머리에 ‘ㄴ’이 나타났으므로 두음법칙이 적용되지 않았다.",
      X(13, "⑤㉤은", "적용되지 않았다")),
]

# ---------------- 14번
s14 = Q[14]["stem"]
Q[14]["stem"] = s14[: s14.index("<보 기>")].strip()
assert Q[14]["stem"] == "<보기>를 참고할 때, <조건>에 맞는 문장으로 적절한 것은?", Q[14]["stem"]
b14 = s14[s14.index("<보 기>") + 5: s14.index("<조 건>")]
c14 = s14[s14.index("<조 건>") + 5:]
Q[14]["bogi"] = [
    {"label": "보 기", "blocks": [{"id": "b1", "type": "para", "text": b14, "underlines": []}]},
    {"label": "조 건", "blocks": [{"id": "c1", "type": "para", "text": c14, "underlines": []}]},
]
S_NOUN = "‘-(으)ㄴ, -던’으로 과거 시제를"
S_ADJ = "다만 형용사나 서술격 조사인 경우에는 ‘-(으)ㄴ’으로 현재 시제를 표현한다."
S_FUT = "‘-(으)ㄹ’로 미래 시제를"
COND = "과거 시제와 현재 시제를 표현하는 관형사절을 각각 한 번씩만 사용할 것."
Q[14]["answer"] = 1
Q[14]["judgments"] = [
    J(1, "적절", True, [S_NOUN, S_ADJ, COND], "해설지",
      "관형사절은 ‘언니가 만든’과 ‘은사이신’이다. ‘만든’은 과거 시제, ‘은사이신’은 서술격 조사의 현재 시제여서 조건에 맞는다.",
      X(14, "관형사절은 ‘언니가", "표현하고 있다")),
    J(2, "부적절", False, [S_ADJ, COND], "해설지",
      "관형사절은 형용사 ‘밝다’의 ‘밝은’ 하나뿐이고 현재 시제만 나타난다. 과거 시제 관형사절이 없다.",
      X(14, "②현재 시제를", "나타나 있다")),
    J(3, "부적절", False, [S_NOUN, COND], "해설지",
      "관형사절은 ‘내가 책을 사던’ 하나뿐이고 과거 시제만 나타난다. 현재 시제 관형사절이 없다.",
      X(14, "③과거 시제를", "나타나 있다")),
    J(4, "부적절", False, [S_NOUN, COND], "해설지",
      "‘집에 들어온’, ‘오빠가 한’, ‘내가 자주 듣던’ 세 관형사절이 모두 과거 시제이다. 각각 한 번씩만 쓴다는 조건에 맞지 않는다.",
      X(14, "④과거 시제를", "세 번 나타나 있다")),
    J(5, "부적절", False, [S_NOUN, S_FUT, COND], "해설지",
      "관형사절은 과거 시제의 ‘최근 출간된’과 미래 시제의 ‘검색할’이다. 현재 시제 관형사절이 없다.",
      X(14, "⑤과거 시제를", "나타나 있다")),
]

# ---------------- 15번
s15 = Q[15]["stem"]
Q[15]["stem"] = s15[: s15.index("것은?") + 3]
Q[15]["stem_underlines"] = ["않은"]
body = s15[s15.index("<보 기>") + 5:]
i2 = body.index("선생님:")
i_task = body.index("[학습 과제]", i2)
D1, D2 = body[:i2].strip(), body[i2:i_task].strip()
rest = body[i_task:]
i_tab = rest.index("과제적절성")
head15 = rest[:i_tab]
tab_head = rest[i_tab:]
assert tab_head == "과제적절성 판단적절성 판단의 근거", tab_head
parts = re.split(r"(?=ㆍ)", head15)
title15 = parts[0].strip()
bul = [p.strip() for p in parts[1:]]
assert len(bul) == 5 and title15.startswith("[학습 과제]"), (title15, bul)
BU = [("㉠", "읽어 주었다"), ("㉡", "주고갔다"), ("㉢", "덤벼들어보아라"), ("㉣", "읽어도보았으나"), ("㉤", "올 듯도 하다")]
blocks15 = [
    {"id": "b1", "type": "para", "dialogue": True, "text": D1, "bold": ["학생:"], "underlines": []},
    {"id": "b2", "type": "para", "dialogue": True, "text": D2, "bold": ["선생님:"], "underlines": []},
    {"id": "h1", "type": "para", "text": title15, "bold": ["[학습 과제]"], "underlines": [], "inbox": "학습과제"},
]
for k, (b, (m, u)) in enumerate(zip(bul, BU)):
    assert m in b and u in b, (b, m, u)
    blocks15.append({"id": f"e{k+1}", "type": "para", "text": b, "underlines": [{"mark": m, "text": u}], "inbox": "학습과제"})
Q[15]["bogi"] = [
    {"label": "보 기", "blocks": blocks15},
    {"label": "", "plain": True, "blocks": [
        {"id": "th", "type": "heading", "text": "과제" + SP * 4 + "적절성 판단" + SP * 8 + "적절성 판단의 근거", "underlines": []}]},
]
Q[15]["table_border"] = True
for k, c in enumerate(Q[15]["choices"]):
    m = c[0]
    judge = "적절함" if c[1:].startswith("적절함") else "적절하지 않음"
    ground = c[1 + len(judge):]
    Q[15]["choices"][k] = m + SP * 3 + judge + SP * 3 + ground
    assert m == "㉠㉡㉢㉣㉤"[k]
Q[15]["answer"] = 2
R_PRI = "보조 용언은 띄어 쓰는 것을 원칙으로 하되"
R_COMP = "앞말에 조사가 붙거나 앞말이 합성 용언인 경우에는 띄어 씁니다"
R_NOUN = "또한 의존 명사에 ‘-하다’가 결합한 보조 용언에서 의존 명사 뒤에 조사가 붙는 경우에도 띄어 씁니다"
R_MAIN = "본용언에 본용언이 이어진다면 띄어 씁니다"
Q[15]["judgments"] = [
    J(1, "적절", False, [R_PRI, "형이 나에게 책을 ㉠읽어 주었다."], "해설지",
      "㉠은 본용언 ‘읽어’ 뒤에 보조 용언 ‘주었다’가 이어진 경우이므로 띄어 쓰는 것이 원칙이다. 적절하다는 판단과 근거가 맞다.",
      X(15, "①㉠은", "원칙이다")),
    J(2, "부적절", True, [R_MAIN, "친구가 동생에게 선물을 ㉡주고갔다."], "해설지",
      "‘주고’와 ‘갔다’는 모두 본용언이므로 띄어 써야 한다. 보조 용언을 붙여 쓰는 것을 허용하는 경우가 아니어서 적절하다는 판단이 틀리다.",
      X(15, "‘주고’와", "써야 한다")),
    J(3, "적절", False, [R_COMP, "이번 기회에 한번 ㉢덤벼들어보아라."], "해설지",
      "㉢의 앞말 ‘덤벼들어’는 합성 용언이므로 보조 용언 ‘보아라’와 띄어 써야 한다. 적절하지 않다는 판단과 근거가 맞다.",
      X(15, "③㉢의", "띄어 써야 한다")),
    J(4, "적절", False, [R_COMP, "책을 ㉣읽어도보았으나"], "해설지",
      "㉣은 앞말 ‘읽어’에 조사 ‘도’가 붙은 경우이므로 보조 용언 ‘보았으나’와 띄어 써야 한다. 적절하지 않다는 판단과 근거가 맞다.",
      X(15, "④㉣은", "띄어 써야 한다")),
    J(5, "적절", False, [R_NOUN, "그가 보낸 메시지를 보니 그가 ㉤올 듯도 하다."], "해설지",
      "㉤은 보조 용언 ‘듯하다’에서 의존 명사 ‘듯’ 뒤에 조사 ‘도’가 붙은 경우이므로 띄어 써야 한다. 적절하다는 판단과 근거가 맞다.",
      X(15, "⑤㉤은", "띄어 써야 한다")),
]
json.dump(d, open(HERE + r"\세트_13-15.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok")
