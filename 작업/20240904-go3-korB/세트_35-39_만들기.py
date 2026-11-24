"""2025학년도 9월 모의평가 고3 언어와 매체(korB) 35~39번 세트: 초안 + 쪽 그림 확인값 + 해설지 기반 판단 → 세트_35-39.json

쪽 그림(문제_13쪽.png, 문제_14쪽.png)과 PDF 텍스트층·선·글꼴로 확인한 것(2026-11-25):
- 구성: [35 ~ 36] 안내문 + 글(문단 3개) → 35·36번, 이어서 안내문 없는 단독 문항 37·38·39번. 하나의 세트(range [35,39]).
  세트_뽑기.py 는 안내문 [35 ~ 36] 을 범위 [35,39] 로 찾지 못하므로 35~36 초안(_임시\\d3536.json)과 37~39 초안(_임시\\d3739.json)을 합쳤다.
- 글은 네모 상자 안에 있다(알려진 화면 한계). 굵은 글씨 없음(get_texttrace type=1 없음, [자료]·[조건]·현대어 풀이는 중고딕 보통). 밑줄 ㉠㉡ 은 PDF 선(기호 바로 뒤부터 «경우» 까지).
- 36번 <보기>: 설명 줄 + 안쪽 테두리 상자(ⓐ~ⓔ 다섯 문장, 밑줄 단어 10개는 기호 없는 밑줄).
- 37번 <학습 활동>: 문단(밑줄 ㉠~㉤) + [자료] 표(쪽에서 잘라 그림, 표 속 글자는 pdf_text). 발문 '않은' 밑줄(PDF 선).
- 38번 <보기>: 옛한글 PUA 가 든 줄(체언·조사·자료 ◦ 줄)은 쪽에서 오려 낸 그림(display_image). 높임 표현 표는 그림. 자료의 밑줄 3곳은 기호 없는 밑줄.
  선지는 ㉠㉡㉢ 열 머리가 있는 표(PUA 포함)라서 choices_raster + 선지 표 그림(열 머리 ㉠㉡㉢ 밑줄은 그림 속).
- 39번: <보기> 상자 = [조건] + 글머리 3개.
"""
import json
import re

HERE = r"D:\Work\블로그\리딩맵\작업\20240904-go3-korB"
a = json.load(open(HERE + r"\_임시\d3536.json", encoding="utf-8"))
b = json.load(open(HERE + r"\_임시\d3739.json", encoding="utf-8"))
qa = {q["no"]: q for q in a["questions"]}
qb = {q["no"]: q for q in b["questions"]}
d = {"guide": "[35 ~ 36] 다음 글을 읽고 물음에 답하시오.", "range": [35, 39],
     "passage": a["passage"], "questions": [qa[35], qa[36], qb[37], qb[38], qb[39]]}
d["meta"] = {"exam": "2025학년도 9월 고3 모의평가 국어(언어와 매체)", "exam_id": "20240904-go3-korB",
             "area": "문법", "topic": "품사 통용·음운 변동 오류·중세 국어 높임·문장의 짜임과 시제",
             "problem_pdf": "20240904-go3-problem-korB_1_mun_4II3M1ST_1.pdf",
             "explanation_pdf": "20240904-go3-explanation-korB_1_hsj_1P5Q6LIA_1.pdf"}
Q = {q["no"]: q for q in d["questions"]}
for p in d["passage"]:
    p.setdefault("underlines", [])
P_ = {p["id"]: p for p in d["passage"]}
CIR = "①②③④⑤"
Z = "\u200b"


def sq(s):
    return re.sub(r"[\s\u200b]+", "", s)


# ---- 지문 밑줄 ㉠㉡
for m, t in [("㉠", "하나의 명사가 자립 명사와 의존 명사로 모두 쓰이는 경우"), ("㉡", "하나의 동사가 본동사와 보조 동사로 모두 쓰이는 경우")]:
    assert m + t in P_["p3"]["text"], m
P_["p3"]["underlines"] = [
    {"mark": "㉠", "text": "하나의 명사가 자립 명사와 의존 명사로 모두 쓰이는 경우"},
    {"mark": "㉡", "text": "하나의 동사가 본동사와 보조 동사로 모두 쓰이는 경우"}]

# ---- 36번
s36 = Q[36]["stem"]
i36 = s36.index("<보 기>")
body36 = s36[i36 + len("<보 기>"):]
Q[36]["stem"] = s36[:i36]
c5 = Q[36]["choices"][4]
Q[36]["choices"][4] = c5[: c5.index("37.")]
intro36 = "ⓐ～ⓔ의 밑줄 친 단어는 모두 둘 이상의 쓰임을 보인다."
assert body36.startswith(intro36), body36[:40]
lines36 = [x for x in re.split(r"(?=[ⓐⓑⓒⓓⓔ])", body36[len(intro36):]) if x]
assert len(lines36) == 5, lines36
UL36 = [["마당", "버렸다"], ["약간", "바퀴"], ["마당", "바퀴"], ["약간", "가지고"], ["가지고", "버렸다"]]
blocks36 = [{"id": "b1", "type": "para", "text": intro36, "underlines": []}]
for k, t in enumerate(lines36):
    for u in UL36[k]:
        assert u in t, (u, t)
    blocks36.append({"id": f"b{k+2}", "type": "para", "text": t, "underlines": [{"mark": "", "text": u} for u in UL36[k]], "inbox": "예문"})
Q[36]["bogi"] = {"label": "< 보 기 >", "blocks": blocks36}
Q[36]["choices"] = Q[36]["choices"][:5]

# ---- 37번
s37 = Q[37]["stem"]
i37 = s37.index("<학습 활동>", 1)
Q[37]["stem"] = s37[:i37]
Q[37]["stem_underlines"] = ["않은"]
body37 = s37[i37 + len("<학습 활동>"):]
j37 = body37.index("설명해 보자.") + len("설명해 보자.")
intro37 = body37[:j37]
rest37 = body37[j37:]
assert rest37.startswith("[자료]예표준 발음"), rest37[:20]
tab37 = rest37[len("[자료]"):]
UL37 = [("㉠", "유음화"), ("㉡", "‘ㄹ’의 비음화"), ("㉢", "구개음화"), ("㉣", "음절의 끝소리 규칙"), ("㉤", "ㄴ첨가")]
for m, t in UL37:
    assert m + t in intro37, m
Q[37]["bogi"] = {"label": "학습 활동", "blocks": [
    {"id": "b1", "type": "para", "text": intro37, "underlines": [{"mark": m, "text": t} for m, t in UL37]},
    {"id": "b2", "type": "para", "text": "[자료]", "underlines": []},
    {"id": "f1", "type": "figure", "caption": "", "image": "그림_35-39_37_자료표.png", "pdf_text": tab37, "raster_text": "",
     "alt": "3열 6행 표. 열 머리는 예, 표준 발음, 비표준 발음. ⓐ 인류가 [일류가] [인뉴가], ⓑ 순환론 [순환논] [순활론], ⓒ 코끝이 [코끄치] [코끄티], ⓓ 들녘을 [들녀클] [들녀글], ⓔ 봄여름 [봄녀름] [보며름]."}]}
c5 = Q[37]["choices"][4]
Q[37]["choices"][4] = c5[: c5.index("때문이다.") + 5]

# ---- 38번
s38 = Q[38]["stem"]
i38 = s38.index("<보 기>")
Q[38]["stem"] = s38[:i38]
body38 = s38[i38 + len("<보 기>"):]


def cut(s, x, y):
    i = s.index(x)
    j = s.index(y, i) if y else len(s)
    return s[i:j]


intro38 = cut(body38, "중세 국어에는", "[자료]에 나타난")
h38 = "[자료]에 나타난 체언과 조사"
t_chaeon = cut(body38, "∙체언:", "∙조사:")
t_josa = cut(body38, "∙조사:", "[자료]◦")
t_jaryo1 = cut(body38, "◦妙光이", "[현대어 풀이: 묘광이")
t_pul1 = cut(body38, "[현대어 풀이: 묘광이", "◦내 부텨")
t_jaryo2 = cut(body38, "◦내 부텨", "[현대어 풀이: 내가")
t_pul2 = cut(body38, "[현대어 풀이: 내가", "높임 표현")
tail = body38[body38.index("높임 표현높이는 대상"):]
assert tail.endswith("㉢㉠㉡㉢"), repr(tail[-10:])
tab38, hdr38 = tail[:-3], tail[-3:]
assert hdr38 == "㉠㉡㉢"
assert intro38.endswith("알아보자.") and t_pul2.endswith("드리되]") and t_pul1.endswith("이으시며]")
PUA = re.compile("[\ue000-\uf8ff]")
for t in (t_chaeon, t_josa, t_jaryo1, t_jaryo2):
    assert PUA.search(t)
for t in (intro38, t_pul1, t_pul2):
    assert not PUA.search(t)
u1 = "\ue38a" + Z + "외시고"
u2 = "니\ued6b" + Z + "시며"
u3 = "\uf537" + Z + "\ued8f" + Z + "\ue876" + Z + "\ue3a8" + Z
for u, t in ((u1, t_jaryo1), (u2, t_jaryo1), (u3, t_jaryo2)):
    assert u in t, repr(u)
blocks38 = [
    {"id": "b1", "type": "para", "text": intro38, "underlines": []},
    {"id": "b2", "type": "para", "text": h38, "underlines": []},
    {"id": "b3", "type": "para", "text": t_chaeon, "underlines": [], "display_image": "그림_35-39_38_체언.png"},
    {"id": "b4", "type": "para", "text": t_josa, "underlines": [], "display_image": "그림_35-39_38_조사.png"},
    {"id": "b5", "type": "para", "text": "[자료]", "underlines": []},
    {"id": "b6", "type": "para", "text": t_jaryo1, "underlines": [{"mark": "", "text": u1}, {"mark": "", "text": u2}], "display_image": "그림_35-39_38_자료1.png"},
    {"id": "b7", "type": "para", "text": t_pul1, "underlines": []},
    {"id": "b8", "type": "para", "text": t_jaryo2, "underlines": [{"mark": "", "text": u3}], "display_image": "그림_35-39_38_자료2.png"},
    {"id": "b9", "type": "para", "text": t_pul2, "underlines": []},
    {"id": "f1", "type": "figure", "caption": "", "image": "그림_35-39_38_높임표.png", "pdf_text": tab38, "raster_text": "",
     "alt": "2열 4행 표. 열 머리는 높임 표현, 높이는 대상. 첫 행은 옛 글자 ‘ᄃ외시고(ᄃ외-＋-시-＋-고)’와 ㉠, 둘째 행은 ‘니ᄉ시며(닝-＋-으시-＋-며)’와 ㉡, 셋째 행은 ‘호ᄉ보디(호-＋-ᄉᆞᆸ-＋-오디)’와 ㉢. 높이는 대상 칸의 ㉠㉡㉢은 빈칸 기호."}]
choice_txt = hdr38 + "".join(CIR[i] + c for i, c in enumerate(Q[38]["choices"]))
Q[38]["bogi"] = [
    {"label": "< 보 기 >", "blocks": blocks38},
    {"label": "", "plain": True, "figure": {
        "id": "cf", "type": "figure", "caption": "", "image": "그림_35-39_38_선지표.png", "pdf_text": choice_txt, "raster_text": "",
        "alt": "열 머리 ㉠ ㉡ ㉢(밑줄 있음), 5행 표. ① 妙光(묘광), 妙光(묘광), 부텨. ② 妙光(묘광), 妙光(묘광), 말씀. ③ 스승, 妙光(묘광), 부텨. ④ 스승, 스승, 말씀. ⑤ 스승, 스승, 부텨. ‘스승’의 ‘ᅌ’과 ‘말씀’의 ‘ᄊᆞ’는 옛 글자."}}]
Q[38]["choices_raster"] = True

# ---- 39번
s39 = Q[39]["stem"]
i39 = s39.index("<보 기>")
Q[39]["stem"] = s39[:i39].replace("[3점]", "").strip()
body39 = s39[i39 + len("<보 기>"):]
assert body39.startswith("[조건]"), body39[:10]
conds = [x for x in re.split(r"(?=◦)", body39[len("[조건]"):]) if x]
assert len(conds) == 3, conds
Q[39]["bogi"] = {"label": "< 보 기 >", "blocks": [{"id": "b1", "type": "para", "text": "[조건]", "underlines": []}] + [
    {"id": f"b{k+2}", "type": "para", "text": t, "underlines": []} for k, t in enumerate(conds)]}

for q in d["questions"]:
    assert len(q["choices"]) == 5, q["no"]

# ---- 해설지 인용 도우미
LINES = open(HERE + r"\해설_글자.txt", encoding="utf-8").read().split("\n")
ORIG = "".join(l for l in LINES[1081:1153] if not l.startswith("===") and not re.fullmatch(r"\d+", l.strip())).replace(Z, "")


def E(start, end):
    pat = lambda s: r"\s*".join(re.escape(c) for c in sq(s))
    ms = list(re.finditer(pat(start) + r".*?" + pat(end), ORIG, re.S))
    assert len(ms) == 1, (start, len(ms))
    return ms[0].group(0)


def J(choice, verdict, ans, ev, reason, xq, basis="해설지"):
    out = {"choice": choice, "verdict": verdict, "is_answer": ans, "basis": basis, "reason": reason, "evidence": []}
    for e in ev:
        if e[0] == "bogi":
            out["evidence"].append({"source": "bogi", "para": None, "quote": e[1]})
        elif e[0] == "fig":
            out["evidence"].append({"source": "figure", "fig": e[1], "quote": e[2]})
        else:
            out["evidence"].append({"source": "passage", "para": e[1], "quote": e[2]})
    if xq:
        out["explanation_quote"] = xq
    return out


def P(pid, quote):
    assert sq(quote) in sq(P_[pid]["text"]), quote
    return ("passage", pid, quote)


def B(no, quote):
    box = Q[no]["bogi"]
    box = box if isinstance(box, list) else [box]
    txt = "".join(it.get("text", "") for bx in box for it in bx.get("blocks", []))
    assert sq(quote) in sq(txt), quote
    return ("bogi", quote)


def F(no, fid, quote):
    box = Q[no]["bogi"]
    box = box if isinstance(box, list) else [box]
    figs = [it for bx in box for it in bx.get("blocks", [])] + [bx["figure"] for bx in box if "figure" in bx]
    f = next(x for x in figs if x.get("id") == fid)
    assert sq(quote) in sq(f["pdf_text"]), quote
    return ("fig", fid, quote)


# ======== 35번 (정답 ④, 적절한 것) ========
Q[35]["answer"] = 4
Q[35]["judgments"] = [
    J(1, "부적절", False, [P("p1", "‘그는 그저께 낮에 왔다.’와 ‘그는 그저께 왔다.’의 ‘그저께’는 각각 명사와 부사이므로"),
                        P("p2", "명사 ‘그저께’는 다양한 격 조사와 결합한다.")],
      "‘그저께가’의 ‘그저께’는 격 조사 ‘가’와 결합한 명사이고, ‘그저께 본’의 ‘그저께’는 용언을 수식하는 부사이다. 두 ‘그저께’의 품사가 같다는 설명은 틀리다.",
      E("‘내 생일은 그저께가 아니라", "부사이다.")),
    J(2, "부적절", False, [P("p1", "‘그는 세계적으로 유명하다.’의 ‘세계적’은 명사이므로"),
                        P("p1", "각각 명사와 부사이므로 ‘그저께’도 품사 통용을 보이는 단어이다.")],
      "‘세계적으로’의 ‘세계적’은 격 조사 ‘으로’와 결합한 명사이고, ‘서둘러’처럼 용언을 수식하는 ‘그저께’는 부사이다. 품사가 같다는 설명은 틀리다.",
      E("‘그는 세계적으로 매우 유명하다.’에 쓰인 ‘세계적’은 명사이다.", "‘그저께’는 부사이다.")),
    J(3, "부적절", False, [P("p2", "관형사 ‘세계적’은 조사와 결합할 수 없고 항상 관형어로 쓰인다."),
                        P("p1", "‘그는 그저께 왔다.’의 ‘그저께’는 각각 명사와 부사이므로")],
      "‘첫눈이 그저께 왔다.’의 ‘그저께’는 용언을 수식하는 부사로 부사어이고, ‘세계적 명성’의 ‘세계적’은 관형사로 관형어이다. 문장 성분이 서로 같다는 설명은 틀리다.",
      E("‘첫눈이 그저께 왔다.’에 쓰인", "문장 성분은 관형어이다.")),
    J(4, "적절", True, [P("p2", "그리고 명사 ‘그저께’는 격 조사와 결합해 다양한 문장 성분으로 쓰인다."),
                      P("p1", "‘그는 그저께 낮에 왔다.’와 ‘그는 그저께 왔다.’의 ‘그저께’는 각각 명사와 부사이므로")],
      "‘그저께 낮만큼’의 ‘그저께’는 명사로 관형어이고, ‘그저께 피었다’의 ‘그저께’는 부사로 부사어이다. 품사도 문장 성분도 서로 다르다.",
      E("‘여기는 그저께 낮만큼 더웠다.’에 쓰인", "문장 성분은 부사어이다.")),
    J(5, "부적절", False, [P("p2", "가령 명사 ‘세계적’은 ‘으로’와 ‘이다’ 등과 같은 격 조사와 결합하지만"),
                        P("p2", "가령 명사 ‘세계적’은 격 조사와 결합해 문장의 부사어와 서술어로 쓰일 수 있는데")],
      "‘세계적인’은 명사 ‘세계적’에 조사 ‘이-’와 어미 ‘-ㄴ’이 결합했지만, ‘세계적으로’는 명사에 조사 ‘으로’만 결합했다. 둘 다 조사와 어미가 결합했다는 설명은 틀리다.",
      E("‘그는 세계적인 선수이다.’에서의", "부사어로 쓰이고 있다.")),
]

# ======== 36번 (정답 ③, 적절한 것) ========
Q[36]["answer"] = 3
LA = "ⓐ나는 급한 마당에 실수로 결재 서류를 휴지통에 버렸다."
LB = "ⓑ나는 약간의 시간이 남아 자전거 바퀴를 깨끗이 닦았다."
LC = "ⓒ작고 귀여운 강아지가 넓은 마당을 일곱 바퀴나 돌았다."
LD = "ⓓ산꼭대기에 구름이 약간 껴 가지고 경치가 좋아 보였다."
LE = "ⓔ나는 모임을 가지고 난 후 아주 급히 집으로 와 버렸다."
Q[36]["judgments"] = [
    J(1, "부적절", False, [P("p3", "먼저 ㉠하나의 명사가 자립 명사와 의존 명사로 모두 쓰이는 경우가 있다."), B(36, LA)],
      "‘마당’은 자립 명사와 의존 명사로 모두 쓰여 ㉠에 해당하지만, ⓐ의 ‘급한 마당에’는 관형어 ‘급한’의 수식을 받아야만 쓰이는 의존 명사이다. 자립 명사라는 설명은 틀리다.",
      E("ⓐ의 ‘급한 마당에’에서는", "의존 명사로 사용되었다.")),
    J(2, "부적절", False, [P("p1", "이처럼 명사와 부사로 품사 통용을 보이는 단어에는 ‘약간’도 있다."), B(36, LB)],
      "‘약간’은 명사와 부사로 쓰이는 품사 통용 단어이므로 하나의 명사가 자립 명사와 의존 명사로 쓰이는 ㉠에 해당하지 않는다. ⓑ의 ‘약간의’는 명사로 쓰였다.",
      E("‘약간’은 ‘약간의 돈’처럼", "㉠에 해당하지 않는다.")),
    J(3, "적절", True, [P("p3", "‘그는 늦잠을 자는 바람에 회사에 지각했다.’의 ‘바람’은 관형어의 수식을 받아야만 문장에 쓰일 수 있는 의존 명사이다."), B(36, LC)],
      "‘바퀴’는 자립 명사와 의존 명사로 모두 쓰여 ㉠에 해당하고, ⓒ의 ‘일곱 바퀴나’는 관형어 ‘일곱’의 수식을 받아야만 쓰이는 의존 명사이다.",
      E("‘바퀴’는 자립 명사와 의존 명사로 모두 쓰이기 때문에 ㉠에 해당한다.", "의존 명사로 사용되었다.")),
    J(4, "부적절", False, [P("p3", "‘나는 고난을 견뎌 내었다.’의 ‘내다’는 본동사 없이는 문장에 쓰일 수 없는 보조 동사이다."), B(36, LD)],
      "‘가지다’는 본동사와 보조 동사로 모두 쓰여 ㉡에 해당하지만, ⓓ의 ‘껴 가지고’는 앞말이 뜻하는 행동의 결과나 상태가 유지됨을 나타내는 보조 동사이다. 본동사라는 설명은 틀리다.",
      E("‘가지다’는 본동사와 보조 동사로 모두 쓰이기 때문에 ㉡에 해당한다.", "보조 동사로 사용되었다.")),
    J(5, "부적절", False, [P("p3", "다음으로 ㉡하나의 동사가 본동사와 보조 동사로 모두 쓰이는 경우가 있다."), B(36, LE)],
      "‘버리다’는 본동사와 보조 동사로 모두 쓰여 ㉡에 해당하지만, ⓔ의 ‘와 버렸다’는 앞말이 나타내는 행동이 이미 끝났음을 나타내는 보조 동사이다. 본동사라는 설명은 틀리다.",
      E("‘버리다’는 본동사와 보조 동사로 모두 쓰이기 때문에 ㉡에 해당한다.", "보조 동사로 사용되었다.")),
]

# ======== 37번 (정답 ④, 적절하지 않은 것) ========
Q[37]["answer"] = 4
Q[37]["judgments"] = [
    J(1, "적절", False, [F(37, "f1", "ⓐ인류가[일류가][인뉴가]"), B(37, "㉠유음화, ㉡‘ㄹ’의 비음화")],
      "‘인류가’는 유음화가 적용되어 [일류가]로 발음해야 하는데, ‘ㄹ’의 비음화가 적용되어 [인뉴가]로 발음했다. 설명이 맞다.",
      E("‘인류가’는 유음화(㉠)를 적용하여", "적용하였기 때문이다.")),
    J(2, "적절", False, [F(37, "f1", "ⓑ순환론[순환논][순활론]"), B(37, "그런데 음운 변동이 잘못 적용되거나, 적용되지 않아 비표준 발음이 나타나기도 한다.")],
      "‘순환론’은 ‘ㄹ’의 비음화가 적용되어 [순환논]으로 발음해야 하는데, 유음화가 적용되어 [순활론]으로 발음했다. 설명이 맞다.",
      E("‘순환론’은 ‘ㄹ’의 비음화(㉡)를 적용하여", "적용하였기 때문이다.")),
    J(3, "적절", False, [F(37, "f1", "ⓒ코끝이[코끄치][코끄티]"), B(37, "㉢구개음화")],
      "‘코끝이’는 구개음화가 적용되어 [코끄치]로 발음해야 하는데, 구개음화가 적용되지 않아 [코끄티]로 발음했다. 설명이 맞다.",
      E("‘코끝이’는 구개음화(㉢)를 적용하여", "적용하지 않았기 때문이다.")),
    J(4, "부적절", True, [F(37, "f1", "ⓓ들녘을[들녀클][들녀글]"), B(37, "㉣음절의 끝소리 규칙")],
      "‘들녘을’의 ‘을’은 형식 형태소이므로 음절의 끝소리 규칙을 적용하지 않고 [들녀클]로 발음해야 한다. [들녀글]은 오히려 음절의 끝소리 규칙을 적용해서 생긴 발음이어서, 적용돼야 하는데 그렇지 않았다는 설명은 틀리다.",
      E("‘들녘을’의 ‘을’은 형식 형태소이기 때문에", "적용하였기 때문이다.")),
    J(5, "적절", False, [F(37, "f1", "ⓔ봄여름[봄녀름][보며름]"), B(37, "㉤ㄴ첨가")],
      "‘봄여름’은 ㄴ 첨가가 적용되어 [봄녀름]으로 발음해야 하는데, ㄴ 첨가가 적용되지 않아 [보며름]으로 발음했다. 설명이 맞다.",
      E("‘봄여름’은 ㄴ 첨가(㉤)를 적용하여", "적용하지 않았기 때문이다.")),
]

# ======== 38번 (정답 ①, 적절한 것) ========
Q[38]["answer"] = 1
XQ38 = E("주체 높임의 선어말 어미 ‘-시-’를 통해 문장의 주체인 ‘妙光(묘광)’을 높이고 있다.", "‘부텨(부처)’를 높이고 있다.")
R1 = "[현대어 풀이: 묘광이 옛적 등명을 도와 연등의 스승이 되시고 이제 석가를 도와 등명의 도를 이으시며]"
R2 = "[현대어 풀이: 내가 부처께 말씀을 드리되]"
Q[38]["judgments"] = [
    J(1, "적절", True, [B(38, R1), B(38, R2)],
      "㉠, ㉡의 ‘-시-’, ‘-으시-’는 문장의 주체 ‘妙光(묘광)’을 높이고, ㉢의 객체 높임 선어말 어미는 문장의 객체 ‘부텨(부처)’를 높인다.",
      XQ38),
    J(2, "부적절", False, [B(38, R2), B(38, "문장의 객체를 높이는 선어말 어미가 있었다.")],
      "㉠, ㉡이 높이는 대상은 ‘妙光(묘광)’으로 맞지만, ㉢의 객체 높임 선어말 어미가 높이는 대상은 객체인 ‘부텨(부처)’이다. ‘말씀’은 높이는 대상이 아니라 부처께 드리는 말이다.",
      None, "자체"),
    J(3, "부적절", False, [B(38, R1), B(38, "문장의 주체를 높이는 선어말 어미")],
      "㉠의 ‘-시-’는 문장의 주체를 높이므로 높이는 대상은 ‘妙光(묘광)’이다. ‘스승’은 풀이에서 묘광이 되는 자리일 뿐 높임의 주체가 아니다.",
      None, "자체"),
    J(4, "부적절", False, [B(38, R1), B(38, R2)],
      "㉠, ㉡이 높이는 대상은 주체 ‘妙光(묘광)’인데 ‘스승’이라 했고, ㉢이 높이는 대상은 객체 ‘부텨(부처)’인데 ‘말씀’이라 했다. 세 칸이 모두 틀리다.",
      None, "자체"),
    J(5, "부적절", False, [B(38, R1), B(38, "[자료]의 밑줄 친 높임 표현의 선어말 어미가 높이는 대상이 무엇인지 알아보자.")],
      "㉢의 ‘부텨(부처)’는 맞지만, ㉠, ㉡의 ‘-시-’, ‘-으시-’가 높이는 대상은 ‘스승’이 아니라 주체인 ‘妙光(묘광)’이다.",
      None, "자체"),
]

# ======== 39번 (정답 ⑤, 적절한 것) ========
Q[39]["answer"] = 5
C1, C2, C3 = "◦안긴절이 한 번만 나타날 것.", "◦안긴절에는 짧은 부정 표현이 나타날 것.", "◦안은문장은 사건시가 발화시보다 앞설 것."
Q[39]["judgments"] = [
    J(1, "부적절", False, [B(39, C2)],
      "‘차갑지 않은’은 관형사절로 안긴 절이고, 여기에는 긴 부정 표현 ‘-지 않다’가 쓰였다. 짧은 부정 표현이 나타나야 한다는 조건에 맞지 않는다.",
      E("관형사절 ‘차갑지 않은’이 안긴절로 쓰였으며", "앞서는 과거 시제이다.")),
    J(2, "부적절", False, [B(39, C1)],
      "관형사절 ‘바쁜’과 인용절 ‘바쁜 업무들이 안 끝났다고’가 모두 안긴절로 쓰였다. 안긴절이 한 번만 나타나야 한다는 조건에 맞지 않는다.",
      E("관형사절 ‘바쁜’과 인용절", "앞서는 과거 시제이다.")),
    J(3, "부적절", False, [B(39, C2)],
      "인용절 ‘결코 포기를 하지 않겠다고’에는 긴 부정 표현 ‘-지 않다’가 쓰였다. 짧은 부정 표현이 나타나야 한다는 조건에 맞지 않는다.",
      E("인용절 ‘결코 포기를 하지 않겠다고’가 안긴절로 쓰였으며", "앞서는 과거 시제이다.")),
    J(4, "부적절", False, [B(39, C3)],
      "‘예상한다’에서 보듯 안은문장은 사건시와 발화시가 일치하는 현재 시제이다. 사건시가 발화시보다 앞서야 한다는 조건에 맞지 않는다.",
      E("‘예상한다’에서 확인할 수 있듯이", "현재 시제이다.")),
    J(5, "적절", True, [B(39, C1), B(39, C2), B(39, C3)],
      "관형사절 ‘그가 못 읽은’이 안긴절로 한 번 쓰였고 여기에 짧은 부정 표현 ‘못’이 나타난다. ‘읽었다’에서 보듯 안은문장은 사건시가 발화시보다 앞서는 과거 시제여서 세 조건을 모두 충족한다.",
      E("관형사절 ‘그가 못 읽은’이 안긴절로 쓰였으며", "앞서는 과거 시제이다.")),
]

json.dump(d, open(HERE + r"\세트_35-39.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("세트_35-39.json 씀")
