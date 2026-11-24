"""2025-04-30(PDF 표기 5월) 고3 언어와 매체(korB) 37~39번 세트(안내문 없는 단독 문항 묶음): 초안 + 쪽 그림 확인값 + 해설지 기반 판단 → 세트_37-39.json

확인한 것(2026-11-25, 문제_13쪽·14쪽 그림, PDF 텍스트층·선·글꼴, 400dpi 확대):
- 37번 <학습 활동> 상자: 안내 문단 + «[게임 규칙]»(굵게: Haansoft Batang type 0+1, 이 줄만) + 규칙 문단 + 게임판 그림(래스터, 글자는 raster_text).
  선지는 ⓐ ⓑ ⓒ 세 칸 표(머리 ⓐⓑⓒ 는 밑줄 없음).
- 38번 <보기>: 문단 1개, 밑줄 ㉠이러한 표지가 없는 절 (기호 뒤 글자부터, 선은 «절» 까지). 굵은 글씨 없음.
- 39번 <보기>: 옛한글 PUA 가 많은 문단(쪽에서 오려 display_image) + «[현대어 풀이]» 줄(굵은 글씨 아님, type 0 전용) + 현대어 문단(첫 줄 들여씀).
  밑줄 ㉠지븨 ㉡도라와 ㉢(PUA) ㉣닙고 ㉤(PUA)들 ㉥닐어늘 ㉦六師(육사)(PUA) ㉧무리. 발문 «않은» 밑줄.
- 38·39번 보기 머리말 «보 기» 뒤와 37번 «학습 활동» 뒤에 텍스트층 글자 «(» 가 한 개씩 남는다(상자 머리 꺾쇠). 도구 한계로 보고.
- 37번 ⑤ 뒤에 쪽 머리글('2025학년도 … 문제지', '제 1 교시')이 붙으므로 잘라 낸다.
"""
import json
import re

HERE = r"D:\Work\블로그\리딩맵\작업\20250430-go3-korB"
d = json.load(open(HERE + r"\초안_37-39.json", encoding="utf-8"))
d.pop("raw_passage_lines", None)
d["meta"] = {"exam": "2025학년도 5월 고3 전국연합학력평가 국어(언어와 매체)", "exam_id": "20250430-go3-korB",
             "area": "문법", "topic": "음운 변동·안긴문장·중세 국어",
             "problem_pdf": "20250430-go3-problem-korB_mun_A9NKF76H_1.pdf",
             "explanation_pdf": "20250430-go3-explanation-korB_hsj_3547QJ99.pdf"}
d["guide"] = None
d["range"] = [37, 39]
d["passage"] = []
Q = {q["no"]: q for q in d["questions"]}

PUA = "[\ue000-\uf8ff]"


def sq(s):
    return re.sub(r"[\s\u200b]+", "", s)


# ---- 37번
s37 = Q[37]["stem"]
Q[37]["stem"] = s37[: s37.index("것은?") + 3]
body = s37[s37.index("것은?") + 3:]
body = body[body.index("다음은 음운"):]
assert body.endswith("ⓐⓑⓒ")
body = body[: -len("ⓐⓑⓒ")]
i_r = body.index("[게임 규칙]")
intro37 = body[:i_r].strip()
rule37 = body[i_r + len("[게임 규칙]"):].strip()
assert intro37.endswith("말해 보자.") and rule37.endswith("제시해야 한다."), (intro37[-10:], rule37[-10:])
F37 = "ⓐ 교체 1회 탈락 1회 ⓑ 교체 1회 축약 1회 ⓒ 교체 2회 첨가 1회 도착 지점"
Q[37]["bogi"] = [
    {"label": "학습 활동", "blocks": [
        {"id": "g1", "type": "para", "text": intro37, "underlines": []},
        {"id": "g2", "type": "para", "text": "[게임 규칙]", "underlines": [], "bold": ["[게임 규칙]"]},
        {"id": "g3", "type": "para", "text": rule37, "underlines": []},
        {"id": "f1", "type": "figure", "caption": "", "image": "그림_37-39_37_게임판.png", "pdf_text": "", "raster_text": F37,
         "alt": "게임판. 말이 왼쪽 첫 칸에서 출발해 화살표를 따라 이동한다. 첫 칸 ⓐ에는 교체 1회, 탈락 1회, 둘째 칸 ⓑ에는 교체 1회, 축약 1회, 셋째 칸 ⓒ에는 교체 2회, 첨가 1회가 적혀 있고, 마지막 칸이 도착 지점이다."},
    ]},
    {"label": "", "plain": True, "blocks": [
        {"id": "h1", "type": "heading", "text": "　　　　　　ⓐ　　　　　　　　　　　　ⓑ　　　　　　　　　　　　ⓒ", "underlines": []}]},
]
rows = [("굳이[구지]", "직행열차[지캥녈차]", "홑이불[혼니불]"),
        ("맑지[막찌]", "백합꽃[배캅꼳]", "짓이기다[진니기다]"),
        ("밟는[밤ː는]", "탓하다[타타다]", "옷맵시[온맵씨]"),
        ("칡뿌리[칙뿌리]", "밟히다[발피다]", "물약[물략]"),
        ("넓둥글다[넙뚱글다]", "커다랗다[커ː다라타]", "훗일[훈ː닐]")]
SP = "\u3000\u3000\u3000"
for k, r in enumerate(rows):
    raw = Q[37]["choices"][k]
    assert raw.startswith("".join(r)), (raw, r)
Q[37]["choices"] = [SP.join(r) for r in rows]

# ---- 38번
s38 = Q[38]["stem"]
Q[38]["stem"] = s38[: s38.index("것은?") + 3]
b38 = s38[s38.index("것은?") + 3:]
b38 = b38[b38.index("대부분의"):].strip()
assert "㉠이러한 표지가 없는 절도 있다." in b38
Q[38]["bogi"] = {"label": "보 기", "blocks": [{"id": "b1", "type": "para", "text": b38,
                 "underlines": [{"mark": "㉠", "text": "이러한 표지가 없는 절"}]}]}

# ---- 39번
s39 = Q[39]["stem"]
Q[39]["stem"] = s39[: s39.index("것은?") + 3]
Q[39]["stem_underlines"] = ["않은"]
b39 = s39[s39.index("것은?") + 3:]
b39 = b39[b39.index("須達"):]
i_h = b39.index("[현대어 풀이]")
main39 = b39[:i_h].strip()
mod = b39[i_h + len("[현대어 풀이]"):].strip()
assert re.search(PUA, main39)
assert not re.search(PUA, mod)
ULS = [("㉠", "지븨"), ("㉡", "도라와"), ("㉢", "\ue6f5"), ("㉣", "닙고"), ("㉤", "\ue6d7들"), ("㉥", "닐어늘"),
       ("㉦", "六師(육사)\ueea4"), ("㉧", "무리")]
for m, u in ULS:
    assert m + u in main39, (m, u)
Q[39]["bogi"] = {"label": "보 기", "blocks": [
    {"id": "b1", "type": "para", "text": main39, "display_image": "그림_37-39_39_보기본문.png",
     "underlines": [{"mark": m, "text": u} for m, u in ULS]},
    {"id": "b2", "type": "para", "text": "[현대어 풀이]", "underlines": []},
    {"id": "b3", "type": "para", "text": mod, "underlines": []},
]}
for q in d["questions"]:
    assert len(q["choices"]) == 5, q["no"]
    assert not re.search(PUA, "".join(q["choices"])), q["no"]

# ---- 해설지 인용 도우미
_ln = open(HERE + r"\해설_글자.txt", encoding="utf-8").read().split("\n")[1001:1061]
_cl, skip = [], False
for x in _ln:
    if x.startswith("=== 해설"):
        skip = True
        continue
    if skip:
        skip = False
        if re.fullmatch(r"\d+", x.strip()):
            continue
    _cl.append(x)
EXPL = sq("\n".join(_cl))
assert "40.[출제의도]" not in EXPL and EXPL.startswith("37.[출제의도]")


def E(start, end, lead=""):
    s, e = sq(start), sq(end)
    i = EXPL.index(s)
    assert EXPL[i - len(lead): i] == lead, (start, repr(EXPL[i - 3: i]))
    j = EXPL.index(e, i) + len(e)
    return EXPL[i - len(lead): j]


def J(choice, verdict, ans, ev, basis, reason, xq=None):
    out = {"choice": choice, "verdict": verdict, "is_answer": ans, "basis": basis, "reason": reason, "evidence": []}
    for e in ev:
        if e[0] == "figure":
            out["evidence"].append({"source": "figure", "fig": e[1], "quote": e[2]})
        else:
            out["evidence"].append({"source": "bogi", "para": None, "quote": e[2]})
    if xq:
        out["explanation_quote"] = xq
    return out


def B(q):
    return ("bogi", None, q)


def F(q):
    return ("figure", "f1", q)


CA, CB, CC = "ⓐ 교체 1회 탈락 1회", "ⓑ 교체 1회 축약 1회", "ⓒ 교체 2회 첨가 1회"
for c in (CA, CB, CC):
    assert c in F37

# ======== 37번 (정답 ②, 적절한 것)
Q[37]["answer"] = 2
Q[37]["judgments"] = [
    J(1, "부적절", False, [F(CA), F(CB)], "해설지",
      "‘홑이불[혼니불]’은 교체 2회, 첨가 1회가 일어나 ⓒ를 만족하지만, ‘굳이[구지]’는 구개음화로 교체 1회만 일어나 ⓐ를 만족하지 않고, ‘직행열차[지캥녈차]’는 축약 1회, 첨가 1회가 일어나 ⓑ를 만족하지 않는다.",
      E("‘홑이불[혼니불]’은 음절의", "적절하지 않다.")),
    J(2, "적절", True, [F(CA), F(CB), F(CC), B("말이 위치한 칸에 적힌 조건을 모두 만족하는 단어를 제시해야 한다.")], "해설지",
      "‘맑지[막찌]’는 교체 1회, 탈락 1회로 ⓐ를, ‘백합꽃[배캅꼳]’은 음절의 끝소리 규칙과 거센소리되기로 교체 1회, 축약 1회가 일어나 ⓑ를, ‘짓이기다[진니기다]’는 교체 2회, 첨가 1회로 ⓒ를 만족한다.",
      E("‘맑지[막찌]’는 된소리되기와", "적절하다.")),
    J(3, "부적절", False, [F(CC)], "해설지",
      "‘밟는[밤ː는]’은 ⓐ를, ‘탓하다[타타다]’는 ⓑ를 만족하지만, ‘옷맵시[온맵씨]’는 음절의 끝소리 규칙, 비음화, 된소리되기로 교체 3회가 일어나 ⓒ를 만족하지 않는다.",
      E("‘밟는[밤ː는]’은 비음화", "적절하지 않다.")),
    J(4, "부적절", False, [F(CA), F(CB), F(CC)], "해설지",
      "‘칡뿌리[칙뿌리]’는 탈락 1회만 일어나 ⓐ를, ‘밟히다[발피다]’는 축약 1회만 일어나 ⓑ를, ‘물약[물략]’은 교체 1회, 첨가 1회가 일어나 ⓒ를 만족하지 않는다.",
      E("‘칡뿌리[칙뿌리]’는 자음", "적절하지 않다.")),
    J(5, "부적절", False, [F(CB)], "해설지",
      "‘넓둥글다[넙뚱글다]’는 ⓐ를, ‘훗일[훈ː닐]’은 ⓒ를 만족하지만, ‘커다랗다[커ː다라타]’는 거센소리되기로 축약 1회만 일어나 ⓑ를 만족하지 않는다.",
      E("‘넓둥글다[넙뚱글다]’는 된소리되", "적절하지 않다.")),
]

# ======== 38번 (정답 ②, 적절한 것)
Q[38]["answer"] = 2
Q[38]["judgments"] = [
    J(1, "부적절", False, [B("안길 때 어미, 조사 등의 문법적 요소가 붙는데")], "해설지",
      "‘조심했다’ 앞의 ‘-도록’은 부사절을 만드는 어미가 붙은 경우라서 표지가 있는 절이다. ㉠에 해당하지 않는다.",
      E("어미 ‘-도록’이 붙은", "적절하지 않다.")),
    J(2, "적절", True, [B("그런데 ㉠이러한 표지가 없는 절도 있다.")], "해설지",
      "‘바람이 더 잘 통한다’는 어미나 조사 없이 다른 문장에 안겨 있는 서술절이므로, 표지가 없는 절(㉠)이 사용된 문장이다.",
      E("㉠은 이러한 어미나", "적절하다.")),
    J(3, "부적절", False, [B("이는 어떤 종류의 절인지를 나타내는 표지가 된다.")], "해설지",
      "‘있는 책’의 ‘-는’은 관형절을 만드는 어미가 붙은 경우라서 표지가 있는 절이다. ㉠에 해당하지 않는다.",
      E("어미 ‘-는’이 붙은 관형절이", "적절하지 않다.")),
    J(4, "부적절", False, [B("대부분의 안긴문장은 다른 문장 속에 안길 때")], "해설지",
      "‘건강하시기를’의 ‘-기’는 명사절을 만드는 어미가 붙은 경우라서 표지가 있는 절이다. ㉠에 해당하지 않는다.",
      E("어미 ‘-기’가 붙은 명사절이", "적절하지 않다.")),
    J(5, "부적절", False, [B("조사 등의 문법적 요소가 붙는데")], "해설지",
      "‘먹었다고 말했다’의 ‘고’는 인용절을 만드는 조사가 붙은 경우라서 표지가 있는 절이다. ㉠에 해당하지 않는다.",
      E("조사 ‘고’가 붙은 인용절이", "적절하지 않다.")),
]

# ======== 39번 (정답 ①, 적절하지 않은 것)
Q[39]["answer"] = 1
Q[39]["judgments"] = [
    J(1, "부적절", True, [B("㉠지븨"), B("㉦六師(육사)\ueea4"), B("수달이 집에 돌아와"), B("육사의 무리가")], "해설지",
      "㉦은 현대어 풀이 ‘육사의’에 해당하는 관형격 조사이지만, ㉠은 ‘집에’에 해당하는 부사격 조사이다. ㉠과 ㉦을 모두 모음 조화에 따라 달라지는 관형격 조사로 본 설명은 틀리다.",
      E("㉦의", "적절하지 않다.")),
    J(2, "적절", False, [B("㉡도라와"), B("수달이 집에 돌아와")], "해설지",
      "㉡ ‘도라와’는 현대어 ‘돌아와’에 해당한다. 앞 형태소 ‘돌-’의 끝소리 ‘ㄹ’을 다음 형태소의 첫소리로 옮겨 적은 이어적기가 쓰였다.",
      E("㉡은 앞 형태소", "적절하다.")),
    J(3, "적절", False, [B("㉢\ue6f5"), B("㉤\ue6d7들")], "해설지",
      "㉢과 ㉤은 초성이 ‘ㅳ’으로 적혀 있어 두 개 이상의 자음이 함께 쓰였음을 확인할 수 있다.",
      E("㉢과 ㉤의 초", "적절하다.")),
    J(4, "적절", False, [B("㉣닙고"), B("㉥닐어늘"), B("옷을 입고"), B("그 뜻을 이르거늘")], "해설지",
      "㉣의 ‘닙고’는 현대어 ‘입고’와, ㉥의 ‘닐어늘’은 현대어 ‘이르거늘’과 달리 첫소리가 ‘ㄴ’으로 적혀 있어 두음 법칙이 적용되지 않았다.",
      E("㉣의 ‘닙고’는", "적절하다.")),
    J(5, "적절", False, [B("㉧무리"), B("육사의 무리가")], "해설지",
      "㉧ ‘무리’는 모음 ‘이’로 끝난 주어인데 그 뒤에 주격 조사가 나타나지 않았다.",
      E("㉧은 ‘무리", "적절하다.")),
]

json.dump(d, open(HERE + r"\세트_37-39.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("세트_37-39.json 씀")
