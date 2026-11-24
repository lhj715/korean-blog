"""2025-10 고2 13~15번(문법 단독 문항) 세트: 초안 + 쪽 그림 확인값 + 해설지 기반 판단 → 세트_13-15.json

초안은 도구/세트_뽑기.py 로 뽑았다(_임시\초안_13-15.json). 쪽 그림(문제_5쪽_오른쪽.png, 문제_6쪽_왼쪽.png)으로 확인한 것:
- 안내문·지문 없음(guide null, passage []). 문항마다 자기 상자가 있다.
- 13번: <학습 활동> 상자 = 설명 문단 + 주머니 두 개 그림(래스터, 카드 글자는 텍스트층에 있음). 발문 밑줄 '않은'.
  선지는 «뽑은 카드 | 만들어진 문장» 두 칸 표: 표 머리는 머리말 없는 plain 상자, 선지 글은 '카드 + 전각 공백 + 문장'.
- 14번: <보기> = 선생님 말(말한 이 «선생님:» 굵게: type=1 로 «선생님» 과 «:» 모두 굵음). 발문 밑줄 '않은'.
- 15번: <보기> = 선생님/학생/선생님 대화(말한 이와 콜론 굵게) + «[학습 활동]»(굵게) + ◦ 예문 3줄(각각 아래 현대어 풀이 줄).
  예문 2·3 에 옛한글 PUA 글자(U+E46C, U+E64F)가 있어 그 줄을 쪽에서 오려 낸 그림(display_image)으로 보인다. 빈칸 ㉠ 은 텍스트 줄에서 밑줄 위 글자.
  선지는 ㉠·㉡·㉢ 세 칸 표: 표 머리(㉠ ㉡ ㉢ 밑줄 없음)는 plain 상자, 옛한글 PUA(U+E283 ᄂᆞ, U+F537 ᄒᆞ, U+E285 ᄂᆞᆫ)는 choice_images.
"""
import json
import re

HERE = r"D:\Work\블로그\리딩맵\작업\20251014-go2"
d = json.load(open(HERE + r"\_임시\초안_13-15.json", encoding="utf-8"))
d.pop("raw_passage_lines", None)
d["meta"] = {"exam": "2025년 10월 고2 전국연합학력평가 국어", "exam_id": "20251014-go2", "area": "문법",
             "topic": "문장의 짜임·음운 변동·중세 국어 의문문", "problem_pdf": "20251014-go2-problem-kor_mun_KX6R9ZC9.pdf",
             "explanation_pdf": "20251014-go2-explanation-kor_hsj_FJMJXZZL.pdf"}
d["guide"] = None
d["passage"] = []
Q = {q["no"]: q for q in d["questions"]}
SP = "\u3000"


def between(s, a, b, incl_b=True):
    i = s.index(a)
    j = s.index(b, i) + (len(b) if incl_b else 0)
    return s[i:j]


# ---- 13번
s13 = Q[13]["stem"]
Q[13]["stem"] = s13[: s13.index("것은?") + 3]
Q[13]["stem_underlines"] = ["않은"]
Q[13]["table_border"] = True   # 표 칸 아래 테두리가 밑줄로 읽힘(C9 건너뜀, 쪽 그림으로 밑줄 없음 확인)
b13 = between(s13, "각 주머니에서", "만들어 봅시다.")
F13 = s13[s13.index("㉠ 목적어"): s13.index("뽑은 카드")]
assert F13 == ("㉠ 목적어 역할을 하는 명사절을 안은 문장㉡ 간접 인용절을 안은 문장"
               "ⓐ 용언의 관형사형이 관형어로 쓰인 문장ⓑ 사동사에 의한 사동문ⓒ 능력 부정에 해당하는 긴 부정문"), F13
Q[13]["bogi"] = [
    {"label": "학습 활동", "blocks": [
        {"id": "b1", "type": "para", "text": b13, "underlines": []},
        {"id": "f13", "type": "figure", "caption": "", "image": "그림_13-15_13_주머니.png", "pdf_text": F13,
         "alt": "주머니 1에는 ㉠ 목적어 역할을 하는 명사절을 안은 문장, ㉡ 간접 인용절을 안은 문장 카드가, 주머니 2에는 ⓐ 용언의 관형사형이 관형어로 쓰인 문장, ⓑ 사동사에 의한 사동문, ⓒ 능력 부정에 해당하는 긴 부정문 카드가 들어 있다."},
    ]},
    {"label": "", "plain": True, "blocks": [
        {"id": "h1", "type": "heading", "text": "뽑은 카드" + SP * 6 + "만들어진 문장", "underlines": []}]},
]
cards = ["㉠, ⓐ", "㉠, ⓑ", "㉠, ⓒ", "㉡, ⓑ", "㉡, ⓒ"]
for k, c in enumerate(Q[13]["choices"]):
    assert c.startswith(cards[k]), c
    Q[13]["choices"][k] = cards[k] + SP * 2 + c[len(cards[k]):].strip()

# ---- 14번
s14 = Q[14]["stem"]
Q[14]["stem"] = s14[: s14.index("보 기")]
Q[14]["stem_underlines"] = ["않은"]
b14 = s14[s14.index("선생님:"):]
Q[14]["bogi"] = {"label": "보 기", "blocks": [
    {"id": "b1", "type": "para", "dialogue": True, "text": b14, "bold": ["선생님:"], "underlines": []}]}

# ---- 15번
s15 = Q[15]["stem"]
Q[15]["stem"] = s15[: s15.index("보 기")]
body = s15[s15.index("선생님:"):]
i2 = body.index("학생:")
i3 = body.index("선생님:", i2)
i4 = body.index("[학습 활동]◦")        # 선생님 말 안의 «[학습 활동]을 통해» 가 아니라 예문 머리의 것
D1, D2, D3 = body[:i2].strip(), body[i2:i3].strip(), body[i3:i4].strip()
rest = body[i4 + len("[학습 활동]"):]
assert rest.strip().endswith("㉠㉡㉢")
cuts = [rest.index(x) for x in ("◦太子", "(태자가", "◦내 니", "(내가 이르던", "◦네 엇던", "(네가 어떤", "㉠㉡㉢")]
parts = [rest[a:b].strip() for a, b in zip(cuts, cuts[1:])]
assert len(parts) == 6
blocks15 = [
    {"id": "b1", "type": "para", "dialogue": True, "text": D1, "bold": ["선생님:"], "underlines": []},
    {"id": "b2", "type": "para", "dialogue": True, "text": D2, "bold": ["학생:"], "underlines": []},
    {"id": "b3", "type": "para", "dialogue": True, "text": D3, "bold": ["선생님:"], "underlines": []},
    {"id": "b4", "type": "para", "text": "[학습 활동]", "bold": ["[학습 활동]"], "underlines": []},
    {"id": "e1", "type": "para", "text": parts[0], "blank": "㉠", "underlines": []},
    {"id": "t1", "type": "para", "text": parts[1], "underlines": []},
    {"id": "e2", "type": "para", "text": parts[2], "display_image": "그림_13-15_15_학습활동2.png", "underlines": []},
    {"id": "t2", "type": "para", "text": parts[3], "underlines": []},
    {"id": "e3", "type": "para", "text": parts[4], "display_image": "그림_13-15_15_학습활동3.png", "underlines": []},
    {"id": "t3", "type": "para", "text": parts[5], "underlines": []},
]
Q[15]["bogi"] = [
    {"label": "보 기", "blocks": blocks15},
    {"label": "", "plain": True, "blocks": [
        {"id": "h1", "type": "heading", "text": SP * 2 + "㉠" + SP * 6 + "㉡" + SP * 6 + "㉢", "underlines": []}]},
]
A, B, C = "\ue283", "\uf537", "\ue285"
img = {A: ("그림_13-15_15_선지_a.png", "ᄂᆞ"), B: ("그림_13-15_15_선지_b.png", "ᄒᆞ"), C: ("그림_13-15_15_선지_c.png", "ᄂᆞᆫ")}
cells = [
    ("잇" + A + "녀", "그러터녀", "求(구)" + B + C + "다"),
    ("잇" + A + "녀", "그러터뇨", "求(구)" + B + A + "뇨"),
    ("잇" + A + "뇨", "그러터녀", "求(구)" + B + C + "다"),
    ("잇" + A + "뇨", "그러터녀", "求(구)" + B + A + "뇨"),
    ("잇" + A + "뇨", "그러터뇨", "求(구)" + B + A + "뇨"),
]
for k, cs in enumerate(cells):
    assert "".join(cs) == Q[15]["choices"][k], (k, [hex(ord(c)) for c in Q[15]["choices"][k]])
    Q[15]["choices"][k] = (SP * 3).join(cs)
Q[15]["choice_images"] = {
    str(k + 1): [{"text": ch, "image": img[ch][0], "alt": img[ch][1]} for ch in "".join(cs) if ch in img]
    for k, cs in enumerate(cells)}

# 15번 해설지 원문(옛한글 PUA 포함)에서 ㉢ 문장과 이어 붙인 인용을 잘라 온다
expl = open(HERE + r"\해설_글자.txt", encoding="utf-8").read()
sec15 = expl[expl.index("15. [출제의도]"): expl.index("[인문]")].replace("\n", "")
def sent(m):
    i = sec15.index(m)
    return sec15[i: sec15.index("적절하다", i) + 4]


XQ_A = sent("㉠에는")
XQ_B = sent("㉡에는")
XQ_C = sent("㉢에는")
iA, iB, iC = sec15.index("㉠에는"), sec15.index("㉡에는"), sec15.index("㉢에는")
XQ_AB = sec15[iA: iB + len(XQ_B)]
XQ_BC = sec15[iB: iC + len(XQ_C)]
XQ_ALL = sec15[iA: iC + len(XQ_C)]


def J(choice, verdict, ans, ev, basis, reason, xq=None):
    out = {"choice": choice, "verdict": verdict, "is_answer": ans, "basis": basis, "reason": reason,
           "evidence": [({"source": "figure", "fig": e[1], "quote": e[2]} if e[0] == "figure"
                         else {"source": "bogi", "para": None, "quote": e[1]}) for e in ev]}
    if xq:
        out["explanation_quote"] = xq
    return out


CA = ("figure", "f13", "㉠ 목적어 역할을 하는 명사절을 안은 문장")
CB = ("figure", "f13", "㉡ 간접 인용절을 안은 문장")
Ca = ("figure", "f13", "ⓐ 용언의 관형사형이 관형어로 쓰인 문장")
Cb = ("figure", "f13", "ⓑ 사동사에 의한 사동문")
Cc = ("figure", "f13", "ⓒ 능력 부정에 해당하는 긴 부정문")
Q[13]["answer"] = 2
Q[13]["judgments"] = [
    J(1, "적절", False, [CA, Ca], "해설지",
      "‘내가 건강하기’는 목적어 역할을 하는 명사절이고, ‘바라는’은 용언의 관형사형이 ‘분’을 꾸미는 관형어다. ㉠과 ⓐ 조건을 모두 만족한다.",
      "‘내가 건강하기’는 목적어 역할을 하는 명사절이고, ‘바라는’은 용언의 관형사형이 ‘분’을 수식하는 관형어이므로 적절하다"),
    J(2, "부적절", True, [CA, Cb], "해설지",
      "‘이번 책이 독자들에게 많이 읽히기’는 목적어 역할을 하는 명사절이지만, ‘읽히기’는 ‘읽다’에 피동 접미사 ‘-히-’가 붙은 피동사다. 사동사에 의한 사동문이 아니므로 ⓑ 조건을 만족하지 못한다.",
      "‘이번 책이 독자들에게 많이 읽히기’는 목적어 역할을 하는 명사절이지만, ‘읽히기’는 ‘읽다’에 피동 접미사 ‘-히-’가 결합한 피동사이므로 적절하지 않다"),
    J(3, "적절", False, [CA, Cc], "해설지",
      "‘대회에 나가지 못했음’은 목적어 역할을 하는 명사절이고, ‘-지 못하다’ 꼴의 긴 부정이면서 능력 부정이다. ㉠과 ⓒ 조건을 모두 만족한다.",
      "‘대회에 나가지 못했음’은 목적어 역할을 하는 명사절이고, ‘나가지 못했음’은 ‘-지 못하다’라는 형태의 긴 부정이면서 능력 부정이므로 적절하다"),
    J(4, "적절", False, [CB, Cb], "해설지",
      "‘환자를 어서 눕히라고’에는 간접 인용절이 쓰였고, ‘눕히라’의 기본형 ‘눕히다’는 ‘눕다’에 사동 접미사 ‘-히-’가 붙은 사동사다. ㉡과 ⓑ 조건을 모두 만족한다.",
      "‘환자를 어서 눕히라고’에 간접 인용절이 사용되었고, ‘눕히라’의 기본형 ‘눕히다’는 ‘눕다’에 사동 접미사 ‘-히-’가 결합한 사동사이므로 적절하다"),
    J(5, "적절", False, [CB, Cc], "해설지",
      "‘이곳이 어디냐고’에는 간접 인용절이 쓰였고, ‘묻지 못했다’는 ‘-지 못하다’ 꼴의 긴 부정이면서 능력 부정이다. ㉡과 ⓒ 조건을 모두 만족한다.",
      "‘이곳이 어디냐고’에 간접 인용절이 사용되었고, ‘묻지 못했다’는 ‘-지 못하다’라는 형태의 긴 부정이면서 능력 부정이므로 적절하다"),
]

Q[14]["answer"] = 1
Q[14]["judgments"] = [
    J(1, "부적절", True, [("bogi", "음운 환경에 따라 교체, 탈락, 축약 등의 음운 변동을 겪기도 합니다")], "해설지",
      "‘많은’의 ‘ㅎ’은 모음으로 시작하는 어미 ‘-은’ 앞에서 탈락한다. 자음군 단순화로 탈락하는 것이 아니다.",
      "‘많은’의 ‘ㅎ’은 모음으로 시작하는 어미 ‘-은’ 앞에서 탈락하는 현상이 일어나므로 적절하지 않다"),
    J(2, "적절", False, [("bogi", "교체, 탈락, 축약 등의 음운 변동을 겪기도 합니다")], "해설지",
      "‘놓고’의 ‘ㅎ’은 뒤의 ‘ㄱ’을 만나 거센소리 ‘ㅋ’으로 축약된다.",
      "‘놓고’의 ‘ㅎ’은 뒤의 ‘ㄱ’을 만나 거센소리 ‘ㅋ’으로 축약되는 현상이 일어나므로 적절하다"),
    J(3, "적절", False, [("bogi", "‘ㅎ’은 음운 환경에 따라 교체, 탈락, 축약")], "해설지",
      "‘꽂히다’에서는 받침 ‘ㅈ’이 뒤 음절의 첫소리 ‘ㅎ’을 만나 거센소리 ‘ㅊ’으로 축약된다.",
      "‘꽂히다’에서는 받침 ‘ㅈ’이 뒤 음절의 첫소리 ‘ㅎ’과 만나 거센소리 ‘ㅊ’으로 축약되는 현상이 일어나므로 적절하다"),
    J(4, "적절", False, [("bogi", "음운 환경에 따라 교체, 탈락")], "해설지",
      "‘앓는’의 ‘ㅎ’은 자음군 단순화로 탈락하고, 뒤의 ‘ㄴ’이 앞의 ‘ㄹ’을 만나 유음 ‘ㄹ’로 교체된다.",
      "‘앓는’의 ‘ㅎ’은 자음군 단순화를 통해 탈락하고 뒤의 ‘ㄴ’이 앞의 ‘ㄹ’을 만나 유음 ‘ㄹ’로 교체되는 현상이 일어나므로 적절하다"),
    J(5, "적절", False, [("bogi", "‘ㅎ’의 발음에 대해 규정하고 있습니다. 이때 ‘ㅎ’은 음운 환경에 따라 교체")], "해설지",
      "‘쌓네’의 ‘ㅎ’은 음절의 끝소리 규칙으로 ‘ㄷ’이 되고, 이 ‘ㄷ’이 뒤의 ‘ㄴ’을 만나 비음 ‘ㄴ’으로 교체된다.",
      "‘쌓네’의 ‘ㅎ’은 음절의 끝소리 규칙에 따라 ‘ㄷ’이 된 후, 뒤의 ‘ㄴ’을 만나 비음 ‘ㄴ’으로 교체되는 현상이 일어나므로 적절하다"),
]

R_JEONG = "판정 의문문에서는 종결 어미 ‘-녀’가, 설명 의문문에서는 종결 어미 ‘-뇨’가 쓰였습니다"
R_2IN = "또 주어가 2인칭일 때는 의문문의 종류와 관계없이 종결 어미 ‘-ㄴ다’가 쓰였습니다"
Q[15]["answer"] = 3
Q[15]["judgments"] = [
    J(1, "부적절", False, [("bogi", R_JEONG), ("bogi", "(태자가 이제 어디 있느냐?)")], "해설지",
      "㉠은 ‘어디 있느냐’를 묻는 설명 의문문이므로 종결 어미 ‘-뇨’가 쓰인 ‘잇뇨’여야 한다. ‘잇녀’는 판정 의문문의 어미다.",
      XQ_A),
    J(2, "부적절", False, [("bogi", R_JEONG), ("bogi", "(내가 이르던 구라제가 진실로 그러하더냐?)")], "해설지",
      "㉠은 설명 의문문이므로 ‘잇뇨’여야 하고, ㉡은 긍정이나 부정을 묻는 판정 의문문이므로 ‘그러터녀’여야 한다. ‘잇녀’와 ‘그러터뇨’는 둘 다 어미가 거꾸로 쓰였다.",
      XQ_AB),
    J(3, "적절", True, [("bogi", "(태자가 이제 어디 있느냐?)"), ("bogi", "(내가 이르던 구라제가 진실로 그러하더냐?)"),
                       ("bogi", R_2IN)], "해설지",
      "㉠은 설명 의문문이라 ‘잇뇨’, ㉡은 판정 의문문이라 ‘그러터녀’다. ㉢은 주어가 2인칭인 의문문이므로 종류와 관계없이 ‘-ㄴ다’가 쓰인 ‘求(구)ᄒᆞᄂᆞᆫ다’가 맞다.",
      XQ_ALL),
    J(4, "부적절", False, [("bogi", R_2IN), ("bogi", "(네가 어떤 밥을 구하는가?)")], "해설지",
      "㉢의 주어는 2인칭 ‘네’이므로 의문문의 종류와 관계없이 종결 어미 ‘-ㄴ다’가 쓰여야 한다. 설명 의문문의 어미 ‘-뇨’를 쓴 ‘求(구)ᄒᆞᄂᆞ뇨’는 맞지 않다.",
      XQ_C),
    J(5, "부적절", False, [("bogi", R_JEONG), ("bogi", "(내가 이르던 구라제가 진실로 그러하더냐?)"), ("bogi", R_2IN)], "해설지",
      "㉡은 ‘그러하더냐’를 묻는 판정 의문문이므로 ‘그러터녀’여야 하고, ㉢도 ‘-ㄴ다’가 쓰여야 한다. ‘그러터뇨’와 ‘求(구)ᄒᆞᄂᆞ뇨’는 어미가 맞지 않다.",
      XQ_BC),
]

json.dump(d, open(HERE + r"\세트_13-15.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok")
