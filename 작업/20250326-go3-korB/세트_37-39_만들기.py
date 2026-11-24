"""2025-03 고3 언어와 매체(korB) 37~39번 세트(안내문 없는 단독 문항 묶음): 초안 + 쪽 그림 확인값 + 해설지 기반 판단 → 세트_37-39.json

확인한 것(2026-11-25, 문제_13쪽·14쪽 그림, PDF 텍스트층·선·글꼴, 400dpi 확대):
- 37번 <보기>: 글머리(◦) 2개. 밑줄 ㉠꽃잎에[꼰니페] ㉡맺힌[매친] ㉢읊조리며[읍쪼리며] ㉣끓는[끌른] ㉤구급약[구ː금냑] (기호 바로 뒤부터). 굵은 글씨 없음.
  발문 «않은» 밑줄(PDF 선). 줄 끝 «따라서 / 시를», «있는 / ㉤구급약» 은 줄바꿈이 낱말 경계라 공백을 둔다.
- 38번 <보기>: 글머리(◦) 2개, 굵은 글씨·밑줄 없음. [3점].
- 39번: 첫 상자(머리말 없음) = «[학습 활동]»(굵은 글씨, type 0+1) + 안내 문단 + 예문(밑줄 6곳, 기호 없음) + «[학습 자료]»(굵은 글씨) + 표(쪽에서 오려 그림, 표 글자는 pdf_text).
  둘째 상자 < 보 기 > = a~d 네 항목(밑줄·굵은 글씨 없음).
- 37번 ⑤ 뒤에 쪽 머리글('2025학년도 … 문제지', '제 1 교시')이 붙어 잘라 낸다.
"""
import json
import re

HERE = r"D:\Work\블로그\리딩맵\작업\20250326-go3-korB"
d = json.load(open(HERE + r"\_임시\초안_37-39.json", encoding="utf-8"))
d.pop("raw_passage_lines", None)
d["guide"] = None
d["range"] = [37, 39]
d["passage"] = []
d["meta"] = {"exam": "2025학년도 3월 고3 전국연합학력평가 국어영역(언어와 매체)", "exam_id": "20250326-go3-korB",
             "area": "문법", "topic": "음운 변동·안긴문장·형태소",
             "problem_pdf": "20250326-go3-problem-korB_mun_79OHAI8N.pdf",
             "explanation_pdf": "20250326-go3-explanation-korB_hsj_YA4UFFZA.pdf"}
Q = {q["no"]: q for q in d["questions"]}


def sq(s):
    return re.sub(r"[\s\u200b]+", "", s)


# ---- 선지 정리
c5 = Q[37]["choices"][4]
Q[37]["choices"][4] = c5[: c5.index("일어났군.") + len("일어났군.")]
for q in d["questions"]:
    assert len(q["choices"]) == 5, q["no"]

# ---- 37번
s37 = Q[37]["stem"]
bi = s37.index("< 보 기 >")
Q[37]["stem"] = s37[:bi].strip()
Q[37]["stem_underlines"] = ["않은"]
raw37 = s37[bi + len("< 보 기 >"):]
U37 = ["꽃잎에[꼰니페]", "맺힌[매친]", "읊조리며[읍쪼리며]", "끓는[끌른]", "구급약[구ː금냑]"]
T37 = ["◦㉠꽃잎에[꼰니페] 이슬이 ㉡맺힌[매친] 오솔길을 따라서 시를 ㉢읊조리며[읍쪼리며] 거닐었다.",
       "◦이마가 펄펄 ㉣끓는[끌른] 아기에게 급한 대로 집에 있는 ㉤구급약[구ː금냑]을 꺼내 먹였다."]
assert sq("".join(T37)) == sq(raw37), (sq("".join(T37)), sq(raw37))
b37 = []
for k, t in enumerate(T37):
    uls = [{"mark": m, "text": u} for m, u in zip("㉠㉡㉢㉣㉤", U37) if m + u in t]
    b37.append({"id": f"b{k+1}", "type": "para", "text": t, "underlines": uls})
assert sum(len(b["underlines"]) for b in b37) == 5
Q[37]["bogi"] = {"label": "< 보 기 >", "blocks": b37}

# ---- 38번
s38 = Q[38]["stem"]
bi = s38.index("< 보 기 >")
Q[38]["stem"] = s38[:bi].replace("[3점]", "").strip()
raw38 = s38[bi + len("< 보 기 >"):]
T38 = ["◦안은문장의 서술어는 서술어의 자릿수가 두 자리일 것.",
       "◦안은문장에서 부사어 기능을 하는 안긴문장에 보어가 포함될 것."]
assert sq("".join(T38)) == sq(raw38), (raw38,)
Q[38]["bogi"] = {"label": "< 보 기 >", "blocks": [
    {"id": f"b{k+1}", "type": "para", "text": t, "underlines": []} for k, t in enumerate(T38)]}

# ---- 39번
s39 = Q[39]["stem"]
i_h = s39.index("[학습 활동]")
Q[39]["stem"] = s39[:i_h].strip()
rest = s39[i_h:]
i_bogi = rest.index("< 보 기 >")
act, bogi_raw = rest[:i_bogi], rest[i_bogi + len("< 보 기 >"):]
H_ACT, H_DATA = "[학습 활동]", "[학습 자료]"
assert act.startswith(H_ACT)
intro = act[len(H_ACT): act.index("표시하시오.") + len("표시하시오.")]
sent = "막내딸이 삶은 햇감자가 설익어서 조금씩 깨물어 먹었다."
i_s = act.index(sent)
assert act[len(H_ACT) + len(intro): i_s] == "", repr(act[len(H_ACT) + len(intro): i_s])
after = act[i_s + len(sent):]
assert after.startswith(H_DATA)
table_text = after[len(H_DATA):]
assert table_text.startswith("분석 내용대답") and table_text.endswith("㉡㉢○㉣㉤"), table_text
ULS39 = ["막내딸", "삶은", "햇감자", "설익어서", "조금씩", "깨물어"]
for u in ULS39:
    assert u in sent
b39a = [
    {"id": "g1", "type": "para", "text": H_ACT, "underlines": [], "bold": [H_ACT]},
    {"id": "g2", "type": "para", "text": intro, "underlines": []},
    {"id": "g3", "type": "para", "text": sent, "underlines": [{"mark": "", "text": u} for u in ULS39]},
    {"id": "g4", "type": "para", "text": H_DATA, "underlines": [], "bold": [H_DATA]},
    {"id": "tf", "type": "figure", "caption": "", "image": "그림_37-39_39_표.png", "pdf_text": table_text,
     "alt": "표. 열 머리는 ‘분석 내용’과 ‘대답’. 첫째 줄: ‘삶은’, ‘설익어서’에는 모두 자립 형태소가 존재하지 않는다. 대답 ㉠. 둘째 줄: ‘햇감자’는 의존 형태소와 자립 형태소가 모두 포함된 말이다. 대답 ㉡. 셋째 줄: 분석 내용 칸에 ㉢, 대답은 ○. 넷째 줄: 분석 내용 칸에 ㉣, 대답 칸에 ㉤."},
]
T39 = ["a. ㉠과 ㉡에 들어갈 적절한 대답은 각각 ‘×’, ‘○’이다.",
       "b. ㉢이 ‘‘막내딸’은, 자립 형태소이면서 실질 형태소인 형태소 두 개로만 이루어진 말이다.’라면, ㉢에 대한 대답은 적절하다.",
       "c. ㉣이 ‘‘햇감자’에는 형식 형태소가 존재하고, ‘조금씩’에는 형식 형태소가 존재하지 않는다.’라면, ㉤에 들어갈 적절한 대답은 ‘×’이다.",
       "d. ㉣이 ‘‘삶은’은 실질 형태소가 한 개 포함된 말이고, ‘깨물어’는 실질 형태소가 두 개 포함된 말이다.’라면, ㉤에 들어갈 적절한 대답은 ‘○’이다."]
assert sq("".join(T39)) == sq(bogi_raw), (sq(bogi_raw),)
Q[39]["bogi"] = [
    {"label": "", "blocks": b39a},
    {"label": "< 보 기 >", "blocks": [{"id": f"b{k+1}", "type": "para", "text": t, "underlines": []} for k, t in enumerate(T39)]},
]


# ---- 해설지 인용 도우미
lines = open(HERE + r"\해설_글자.txt", encoding="utf-8").read().split("\n")
region = lines[900:973]
assert region[0].startswith("35. [출제의도]") and lines[973].startswith("40. [출제의도]")
full = sq("\n".join(l for l in region if not re.match(r"^=== 해설 \d+쪽 ===$", l)))
EXPL = full[full.index(sq("37. [출제의도]")):]


def E(start, end, lead=""):
    s, e = sq(start), sq(end)
    i = EXPL.index(s)
    assert EXPL[i - len(lead): i] == lead, (start, repr(EXPL[i - 3: i]))
    j = EXPL.index(e, i) + len(e)
    return EXPL[i - len(lead): j]


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


def B(q):
    return ("bogi", q)


def F(q):
    assert q in table_text, q
    return ("fig", "tf", q)


# ======== 37번 (정답 ④, 적절하지 않은 것)
for u in U37:
    assert any(u in b["text"] for b in b37)
Q[37]["answer"] = 4
Q[37]["judgments"] = [
    J(1, "적절", False, [B("㉠꽃잎에[꼰니페]"), B("㉢읊조리며[읍쪼리며]")], "해설지",
      "㉠은 ‘ㄴ’ 첨가, 음절의 끝소리 규칙, 비음화가 일어나 세 번이다. ㉢은 음절의 끝소리 규칙, 자음군 단순화, 된소리되기가 일어나 세 번이다.",
      E("㉠‘꽃잎에[꼰니페]’는", "세 번씩 일어났다.", lead="①")),
    J(2, "적절", False, [B("㉠꽃잎에[꼰니페]"), B("㉤구급약[구ː금냑]")], "해설지",
      "㉤은 ‘ㄴ’ 첨가와 비음화가 일어난다. ㉠, ㉤ 모두 첨가된 ‘ㄴ’ 때문에 비음화가 일어났고, 비음화는 조음 방법이 변하는 음운 변동이다.",
      E("㉤‘구급약", "변하게 된다.", lead="②")),
    J(3, "적절", False, [B("㉡맺힌[매친]"), B("㉢읊조리며[읍쪼리며]")], "해설지",
      "㉡은 거센소리되기가 일어나고 ㉢은 자음군 단순화가 일어난다. 두 변동의 결과 음운의 개수가 줄어든다.",
      E("㉡에서는 거센소리되기", "줄어들었다.", lead="③")),
    J(4, "부적절", True, [B("㉡맺힌[매친]"), B("㉣끓는[끌른]")], "해설지",
      "㉣은 자음군 단순화가 일어나 음절 끝에 올 수 있는 자음 개수의 제한으로 인한 변동이 맞다. 그러나 ㉡은 거센소리되기만 일어나므로 ㉡에 대한 설명은 적절하지 않다.",
      E("㉣‘끓는[끌른]’은", "적절하지 않다.")),
    J(5, "적절", False, [B("㉣끓는[끌른]"), B("㉤구급약[구ː금냑]")], "해설지",
      "㉣은 유음화가 일어나고 ㉤은 비음화가 일어난다. 유음화와 비음화는 모두 인접한 자음과 조음 방법이 같아지는 음운 변동이다.",
      E("㉣에서는 유음화", "같아지는 음운 변동이다.", lead="⑤")),
]

# ======== 38번 (정답 ③, 적절한 것)
C1, C2 = "안은문장의 서술어는 서술어의 자릿수가 두 자리일 것.", "안은문장에서 부사어 기능을 하는 안긴문장에 보어가 포함될 것."
Q[38]["answer"] = 3
Q[38]["judgments"] = [
    J(1, "부적절", False, [B(C2)], "자체",
      "안긴문장 ‘내가 국어 교사가 되기’는 조사 ‘를’과 결합해 목적어로 쓰였다. 부사어 기능을 하는 안긴문장이어야 한다는 둘째 조건에 맞지 않는다."),
    J(2, "부적절", False, [B(C2)], "자체",
      "안긴문장 ‘그곳은 범행 현장이 아니었음’은 조사 ‘이’와 결합해 주어로 쓰였다. 부사어 기능을 하는 안긴문장이어야 한다는 둘째 조건에 맞지 않는다."),
    J(3, "적절", True, [B(C1), B(C2)], "해설지",
      "안은문장의 서술어 ‘유리하다’는 두 자리 서술어이다. 명사절 ‘그가 차기 학생회장이 되기’는 조사와 결합해 부사어로 기능하고 보어 ‘학생회장이’를 포함하므로 두 조건을 모두 만족한다.",
      E("‘지금 상황은 그가 차기 학생회장이", "③이다.")),
    J(4, "부적절", False, [B(C2)], "자체",
      "안긴문장 ‘준희가 동생과 오랜만에 외갓집에 방문하기’는 조사 ‘로’와 결합해 부사어로 쓰이지만, 이 안긴문장에는 보어가 없다. 보어가 포함되어야 한다는 둘째 조건에 맞지 않는다."),
    J(5, "부적절", False, [B(C1), B(C2)], "자체",
      "‘알렸다’는 ‘나는’, ‘그에게’, 안긴문장 ‘교양 수업이 휴강되었음’을 요구하는 세 자리 서술어이다. 서술어가 두 자리여야 한다는 첫째 조건에 맞지 않고, 안긴문장도 목적어로 쓰였다."),
]

# ======== 39번 (정답 ⑤, 적절한 것)
La, Lb, Lc, Ld = T39
R1 = F("‘삶은’, ‘설익어서’에는 모두 자립 형태소가 존재하지 않는다.")
Q[39]["answer"] = 5
Q[39]["judgments"] = [
    J(1, "부적절", False, [B(La), R1], "해설지",
      "‘삶은’(삶-+-은)과 ‘설익어서’(설-+익-+-어서)는 모두 의존 형태소로만 이루어져 자립 형태소가 없으므로 ㉠의 대답은 ○이다. a는 ㉠을 ‘×’라고 하므로 적절하지 않다.",
      E("‘삶은’(삶-+-은),", "존재하지 않는다.", lead="a.")),
    J(2, "부적절", False, [B(Lb), B(Lc), B(Ld)], "해설지",
      "b, c는 적절하지만 d도 적절하다. ‘삶은’의 실질 형태소는 ‘삶-’ 하나이고 ‘깨물어’의 실질 형태소는 ‘깨-’와 ‘물-’ 둘이므로, d를 빼고 b, c만 고른 것은 ‘있는 대로’ 고른 것이 아니다.",
      E("‘삶은’에서 실질 형태소는", "‘물-’이다.", lead="d.")),
    J(3, "부적절", False, [B(Lb), B(Lc), B(Ld)], "해설지",
      "‘막내딸’(막내+딸)은 자립 형태소이면서 실질 형태소인 ‘막내’와 ‘딸’로만 이루어져 b도 적절하다. b를 빼고 c, d만 고른 것은 ‘있는 대로’ 고른 것이 아니다.",
      E("‘막내딸’(막내+딸)은", "이루어져 있다.", lead="b.")),
    J(4, "부적절", False, [B(La), B(Lb), B(Ld)], "해설지",
      "‘삶은’과 ‘설익어서’는 모두 의존 형태소로만 이루어져 ㉠의 대답이 ○이므로 a는 적절하지 않다. a를 포함한 선지는 틀리다.",
      E("‘삶은’(삶-+-은),", "존재하지 않는다.", lead="a.")),
    J(5, "적절", True, [B(Lb), B(Lc), B(Ld)], "해설지",
      "b의 ‘막내딸’은 ‘막내’와 ‘딸’로 이루어지고, c의 ‘햇-’과 ‘-씩’은 접사로 형식 형태소이며, d의 ‘삶은’과 ‘깨물어’의 실질 형태소는 각각 한 개와 두 개이다. 적절한 것은 b, c, d이다.",
      E("따라서 학습 자료에 대한 설명으로", "b, c, d이다.")),
]
for q in d["questions"]:
    assert len(q["choices"]) == 5, q["no"]

json.dump(d, open(HERE + r"\세트_37-39.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("세트_37-39.json 씀")
