"""2025학년도 6월 모의평가 고3 언어와 매체(korB) 37~39번 세트(안내문 없는 단독 문항 묶음): 초안 + 쪽 그림 확인값 + 해설지 기반 판단 → 세트_37-39.json

확인한 것(2026-11-25, 문제_13쪽·14쪽.png, PDF 텍스트층·선·글꼴):
- 37번: 발문 밑줄 없음. 선지는 «①┌ 문장 / └ 문장» 꼴 짝 두 줄(상자 항목으로 찍힌 선지 → choices_in_box, 번호가 글 앞). 밑줄 낱말 10개(PDF 선):
  계신다·도착한 / 그칠·내리는 / 만들·새웠다 / 된·아니고 / 지나쳤다·지나치는. 굵은 글씨 없음.
- 38번: 발문 밑줄 없음. <보기> 상자 = 선생님 말(문단 1개, 밑줄 ⓐ자음군 단순화 ⓑ된소리되기 ⓒ비음화 ⓓ음절의 끝소리 규칙) + 안쪽 상자(㉠~㉤ 5줄:
  원본은 2열 3행이라 텍스트층은 ㉠㉢㉤㉡㉣ 순) + «학  생: ____[A]____»(빈칸 [A]) + «선생님: 네, 맞아요.». 말한 이 이름(선생님·학  생)은 태고딕(굵음), 콜론은 신명조(보통).
  발문 안 «[A]» 는 견고딕 글꼴이나 발문 굵은 글씨 필드가 없어 데이터에 싣지 않는다.
- 39번: 발문 «않은» 밑줄(PDF 선). <탐구 활동> 상자 = 문단 + 표(쪽에서 오려 그림, 표 속 글자는 pdf_text) + 문단 + 안쪽 상자(한자 5개) + 문단.
  선지는 ⓐ~ⓓ 열 머리와 5행 표(글자가 텍스트층에 열 순서로만 있음 → 쪽에서 오려 그림, choices_raster, 선지 글은 raster_text). ⓐ 열의 밑줄 낱말(불·흙·다·옷·을)과 열 머리 ⓐ~ⓓ 밑줄은 그림 속.
  옛한글·PUA 없음. 한자 텍스트층 정상.
"""
import json
import re

HERE = r"D:\Work\블로그\리딩맵\작업\20240604-go3-korB"
d = json.load(open(HERE + r"\초안_37-39.json", encoding="utf-8"))
d.pop("raw_passage_lines", None)
d["guide"] = None
d["range"] = [37, 39]
d["meta"] = {"exam": "2025학년도 6월 고3 모의평가 국어", "exam_id": "20240604-go3-korB",
             "area": "문법", "topic": "서술어의 자릿수·음운 변동의 순서·차자 표기",
             "problem_pdf": "20240604-go3-problem-korB_mun_BARMEM1B.pdf",
             "explanation_pdf": "20240604-go3-explanation-korB_hsj_PV487SE9_3.pdf"}
Q = {q["no"]: q for q in d["questions"]}

# ---- 37번
c5 = Q[37]["choices"][4]
c5 = c5[: c5.index("기차를 탔다.") + len("기차를 탔다.")]
pairs = [
    ("할아버지는 형님 댁에 계신다.", "여객선이 도착한 항구엔 안개가 꼈다.", ["계신다", "도착한"]),
    ("저 친구는 불평이 그칠 날이 없다.", "그는 배에서 내리는 장면을 상상했다.", ["그칠", "내리는"]),
    ("나는 이 호박을 죽으로 만들 것이다.", "아버지는 뜬눈으로 밤을 새웠다.", ["만들", "새웠다"]),
    ("얼음으로 된 성이 나타났다.", "그는 남이 아니고 가족이다.", ["된", "아니고"]),
    ("그의 신중함은 아무래도 지나쳤다.", "언니는 간이역만 지나치는 기차를 탔다.", ["지나쳤다", "지나치는"]),
]
old = Q[37]["choices"][:4] + [c5]
for (a, b, _), o in zip(pairs, old):
    assert o == a + b, (o, a + b)
CIR = "①②③④⑤"
Q[37]["choices"] = [a + "\n" + b for a, b, _ in pairs]
b37 = []
for k, (a, b, uls) in enumerate(pairs):
    t = CIR[k] + " " + a + "\n" + b
    for u in uls:
        assert t.count(u) == 1, (u, t)
    b37.append({"id": f"c{k+1}", "type": "para", "text": t, "underlines": [{"mark": "", "text": u} for u in uls]})
Q[37]["bogi"] = {"label": "", "plain": True, "blocks": b37}
Q[37]["choices_in_box"] = True

# ---- 38번
s38 = Q[38]["stem"]
Q[38]["stem"] = s38[: s38.index("?") + 1]
assert Q[38]["stem"] == "<보기>의 [A]에 들어갈 말로 적절한 것은?"
body = s38[s38.index("<보 기>") + len("<보 기>"):]
t1 = body[: body.index("봅시다.") + len("봅시다.")]
assert t1.startswith("선생님: 한 단어에서")
words = ["㉠ 실없네[시럼네]", "㉡ 깊숙이[깁쑤기]", "㉢ 짓밟지[짇빱찌]", "㉣ 꺾는[껑는]", "㉤ 훑고[훌꼬]"]
rest = body[len(t1):]
assert rest == "㉠ 실없네[시럼네]㉢ 짓밟지[짇빱찌]㉤ 훑고[훌꼬]㉡ 깊숙이[깁쑤기]㉣ 꺾는[껑는]학  생:[A]선생님: 네, 맞아요.", rest
UL38 = [("ⓐ", "자음군 단순화"), ("ⓑ", "된소리되기"), ("ⓒ", "비음화"), ("ⓓ", "음절의 끝소리 규칙")]
for m, t in UL38:
    assert (m + t) in t1
blocks38 = [{"id": "b1", "type": "para", "dialogue": True, "text": t1, "bold": ["선생님"],
             "underlines": [{"mark": m, "text": t} for m, t in UL38]}]
for k, w in enumerate(words):
    blocks38.append({"id": f"w{k+1}", "type": "para", "text": w, "underlines": [], "inbox": "낱말"})
blocks38.append({"id": "b2", "type": "para", "dialogue": True, "text": "학  생: [A]", "bold": ["학  생", "[A]"], "blank": "[A]", "underlines": []})
blocks38.append({"id": "b3", "type": "para", "dialogue": True, "text": "선생님: 네, 맞아요.", "bold": ["선생님"], "underlines": []})
Q[38]["bogi"] = {"label": "< 보 기 >", "blocks": blocks38}

# ---- 39번
s39 = Q[39]["stem"]
i = s39.index("?") + 1
Q[39]["stem"] = s39[:i]
Q[39]["stem_underlines"] = ["않은"]
bx = s39[i:]
assert bx.startswith("<탐구 활동>")
bx = bx[len("<탐구 활동>"):]
ta = bx[: bx.index("보인 것이다.") + len("보인 것이다.")]
tb = bx[len(ta): bx.index("㉢") + 1]
assert tb.startswith("훈으로 읽음음으로 읽음") and tb.endswith("읽음···· ㉢"), tb
r2 = bx[len(ta) + len(tb):]
tc = r2[: r2.index("설명해 보자.") + len("설명해 보자.")]
r3 = r2[len(tc):]
td = r3[: r3.index("乙(새-을)") + len("乙(새-을)")]
r4 = r3[len(td):]
te = r4[: r4.index("이용한 것이다.") + len("이용한 것이다.")]
assert r4[len(te):] == "ⓐⓑⓒⓓ", r4[len(te):]
assert td == "火(불-화), 土(흙-토), 多(많다-다), 衣(옷-의), 乙(새-을)", td
TB_ALT = ("2행 2열 표. 열 머리는 ‘훈으로 읽음’, ‘음으로 읽음’, 행 머리는 ‘본뜻 유지’, ‘본뜻 무시’. "
          "본뜻 유지·훈으로 읽음: ‘水’를 ‘물’의 뜻으로 ‘물’로 읽음 ㉠. 본뜻 유지·음으로 읽음: ‘水’를 ‘물’의 뜻으로 ‘수’로 읽음. "
          "본뜻 무시·훈으로 읽음: ‘水’를 ‘물’의 뜻과 상관없이 ‘물’로 읽음 ㉡. 본뜻 무시·음으로 읽음: ‘水’를 ‘물’의 뜻과 상관없이 ‘수’로 읽음 ㉢.")
Q[39]["bogi"] = [
    {"label": "< 탐구 활동 >", "blocks": [
        {"id": "b1", "type": "para", "text": ta, "underlines": []},
        {"id": "tf", "type": "figure", "caption": "", "image": "그림_37-39_39_표.png", "pdf_text": tb, "raster_text": "", "alt": TB_ALT},
        {"id": "b2", "type": "para", "text": tc, "underlines": []},
        {"id": "b3", "type": "para", "text": td, "underlines": [], "inbox": "한자", "center": True},
        {"id": "b4", "type": "para", "text": te, "underlines": []},
    ]},
]
rows = ["불빛이 일다 火 불 ㉠", "진흙이 굳다 土 흙 ㉠", "웃음이 많다 多 다 ㉡", "시옷을 적다 衣 옷 ㉡", "찬물을 담다 乙 을 ㉢"]
cc = Q[39]["choices"]
assert cc[:4] == ["", "", "", ""] and cc[4] == "불빛이 일다진흙이 굳다웃음이 많다시옷을 적다찬물을 담다火土多衣乙불흙다옷을㉠㉠㉡㉡㉢"
RT = "ⓐ ⓑ ⓒ ⓓ " + " ".join(f"{CIR[k]} {r}" for k, r in enumerate(rows))
Q[39]["bogi"].append({"label": "", "plain": True, "figure": {
    "id": "cf", "type": "figure", "caption": "", "image": "그림_37-39_39_선지표.png",
    "pdf_text": "ⓐⓑⓒⓓ" + CIR + cc[4], "raster_text": RT,
    "alt": "열 머리 ⓐ ⓑ ⓒ ⓓ, 5행 표. ① 불빛이 일다, 火, 불, ㉠. ② 진흙이 굳다, 土, 흙, ㉠. ③ 웃음이 많다, 多, 다, ㉡. ④ 시옷을 적다, 衣, 옷, ㉡. ⑤ 찬물을 담다, 乙, 을, ㉢. ⓐ 열의 ‘불’, ‘흙’, ‘다’, ‘옷’, ‘을’에 밑줄이 있다."}})
Q[39]["choices"] = rows
Q[39]["choices_raster"] = True
for q in d["questions"]:
    assert len(q["choices"]) == 5, q["no"]


# ---- 해설지
def clean(lines):
    out, skip = [], False
    for l in lines:
        if re.match(r"^=== 해설 \d+쪽 ===$", l):
            skip = True
            continue
        if skip:
            skip = False
            continue
        out.append(l)
    return "".join(out)


LN = open(HERE + r"\해설_글자.txt", encoding="utf-8").read().split("\n")
i0 = next(i for i, l in enumerate(LN) if l.startswith("37. 서술어의 자릿수"))
i1 = next(i for i, l in enumerate(LN) if l.startswith("[40~45] 매체"))
EXPL = clean(LN[i0:i1])


def E(start, end):
    i = EXPL.index(start)
    return EXPL[i: EXPL.index(end, i) + len(end)]


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


B = lambda q: ("bogi", q)

# ======== 37번 (정답 ①, 같은 것끼리)
Q[37]["answer"] = 1
Q[37]["judgments"] = [
    J(1, "적절", True, [B(pairs[0][0]), B(pairs[0][1])], "해설지",
      "‘계시다’는 주어와 부사어를 필수적으로 요구하는 서술어이고, ‘도착하다’도 주어와 부사어를 필수적으로 요구하는 서술어이다. 두 서술어의 필수 성분이 같다.",
      E("정답해설 : ‘계시다’는", "서술어이다.")),
    J(2, "부적절", False, [B(pairs[1][0]), B(pairs[1][1])], "해설지",
      "‘그치다’는 주어만 필수적으로 요구하고, ‘내리다’는 주어와 부사어를 필수적으로 요구한다. 필수 성분이 서로 다르다.",
      E("② ‘계속되던", "서술어이다.")),
    J(3, "부적절", False, [B(pairs[2][0]), B(pairs[2][1])], "해설지",
      "‘만들다’는 주어, 목적어, 부사어를 필수적으로 요구하고, ‘새우다’는 주어, 목적어를 필수적으로 요구한다. 필수 성분의 개수가 다르다.",
      E("③ ‘무엇이", "서술어이다.")),
    J(4, "부적절", False, [B(pairs[3][0]), B(pairs[3][1])], "해설지",
      "‘되다’는 주어와 부사어를 필수적으로 요구하고, ‘아니다’는 주어와 보어를 필수적으로 요구한다. 필수 성분의 종류가 다르다.",
      E("④ ‘어떤 재료나", "서술어이다.")),
    J(5, "부적절", False, [B(pairs[4][0]), B(pairs[4][1])], "해설지",
      "앞의 ‘지나치다’는 주어만 필수적으로 요구하고, 뒤의 ‘지나치다’는 주어와 목적어를 필수적으로 요구한다. 필수 성분의 개수가 다르다.",
      E("⑤ ‘일정한 한도를", "서술어이다.")),
]

# ======== 38번 (정답 ①)
W = {k + 1: words[k] for k in range(5)}
Q[38]["answer"] = 1
Q[38]["judgments"] = [
    J(1, "적절", True, [B(W[1]), B("ⓐ자음군 단순화, ⓑ된소리되기, ⓒ비음화")], "해설지",
      "‘실없네[시럼네]’는 ‘없’이 ‘업’이 되는 자음군 단순화(ⓐ)가 일어나, ‘ㅂ’이 ‘ㅁ’이 되는 비음화(ⓒ)가 일어날 조건이 마련된 것이다.",
      E("정답해설 : ㉠의", "조건이 마련된 것이다.")),
    J(2, "부적절", False, [B(W[2]), B("ⓓ음절의 끝소리 규칙을 활용해 설명해 봅시다.")], "해설지",
      "‘깊숙이[깁쑤기]’는 ‘깊’이 ‘깁’이 되는 음절의 끝소리 규칙(ⓓ)이 먼저 일어나 ‘ㅅ’이 ‘ㅆ’이 되는 된소리되기(ⓑ)가 일어날 조건이 마련된 것이다. ⓑ가 먼저라는 설명은 순서가 거꾸로이다.",
      E("② ㉡의", "조건이 마련된 것이다.")),
    J(3, "부적절", False, [B(W[3]), B("예컨대, ‘찾는’은 [찬는]으로 발음되는데, 음절의 끝소리 규칙이 일어나 비음화가 일어날 조건이 마련된 것이에요.")], "해설지",
      "‘짓밟지[짇빱찌]’는 ‘짓’이 ‘짇’이 되는 음절의 끝소리 규칙(ⓓ)이 일어나 ‘ㅂ’이 ‘ㅃ’이 되는 된소리되기(ⓑ)가 일어날 조건이 마련된 것이다. 자음군 단순화(ⓐ)는 일어나지 않는다.",
      E("③ ㉢의", "조건이 마련된 것이다.")),
    J(4, "부적절", False, [B(W[4])], "해설지",
      "‘꺾는[껑는]’은 ‘꺾’이 ‘꺽’이 되는 음절의 끝소리 규칙(ⓓ)이 먼저 일어나 ‘ㄱ’이 ‘ㅇ’이 되는 비음화(ⓒ)가 일어날 조건이 마련된 것이다. ⓒ가 먼저라는 설명은 순서가 거꾸로이다.",
      E("④ ㉣의", "조건이 마련된 것이다.")),
    J(5, "부적절", False, [B(W[5])], "해설지",
      "‘훑고[훌꼬]’는 음절의 끝소리 규칙(ⓓ)이 일어나 ‘ㄱ’이 ‘ㄲ’이 되는 된소리되기(ⓑ)가 일어날 조건이 마련된 것이다. 자음군 단순화(ⓐ)로 설명하는 것은 틀리다.",
      E("⑤ ㉤의", "조건이 마련된 것이다.")),
]

# ======== 39번 (정답 ③, 적절하지 않은 것)
T1 = "예) ‘水’를 ‘물’의 뜻으로 ‘물’로 읽음············· ㉠"
T2 = "예) ‘水’를 ‘물’의 뜻과 상관없이 ‘물’로 읽음···· ㉡"
T3 = "예) ‘水’를 ‘물’의 뜻과 상관없이 ‘수’로 읽음···· ㉢"
for t in (T1, T2, T3):
    assert t.replace(" ", "") in tb.replace(" ", ""), t
F = lambda q: ("fig", "tf", q)
Q[39]["answer"] = 3
Q[39]["judgments"] = [
    J(1, "적절", False, [B("火(불-화)"), F(T1)], "해설지",
      "‘불[火]’을 ‘火’로 표기하고 ‘불’로 읽는 방식은 한자의 본뜻을 유지하고 훈으로 읽은 경우이므로 ㉠에 해당한다.",
      E("① ‘불[火]’을", "㉠에 해당한다.")),
    J(2, "적절", False, [B("土(흙-토)"), F(T1)], "해설지",
      "‘흙[土]’을 ‘土’로 표기하고 ‘흙’으로 읽는 방식은 한자의 본뜻을 유지하고 훈으로 읽은 경우이므로 ㉠에 해당한다.",
      E("② ‘흙[土]’을", "㉠에 해당한다.")),
    J(3, "부적절", True, [B("多(많다-다)"), F(T3)], "해설지",
      "‘많다’의 ‘-다’를 ‘多’로 표기하고 ‘다’로 읽는 방식은 한자의 본뜻을 무시하고 음으로 읽은 경우이므로 ㉡이 아니라 ㉢에 해당한다.",
      E("정답해설 : ‘많다’의", "㉢에 해당한다.")),
    J(4, "적절", False, [B("衣(옷-의)"), F(T2)], "해설지",
      "‘시옷’의 ‘옷’을 ‘衣’로 표기하고 ‘옷’으로 읽는 방식은 한자의 본뜻을 무시하고 훈으로 읽은 경우이므로 ㉡에 해당한다.",
      E("④ ‘시옷’의", "㉡에 해당한다.")),
    J(5, "적절", False, [B("乙(새-을)"), F(T3)], "해설지",
      "‘찬물을’의 ‘을’을 ‘乙’로 표기하고 ‘을’로 읽는 방식은 한자의 본뜻을 무시하고 음으로 읽은 경우이므로 ㉢에 해당한다.",
      E("⑤ ‘찬물을’의", "㉢에 해당한다.")),
]

json.dump(d, open(HERE + r"\세트_37-39.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("세트_37-39.json 씀")
