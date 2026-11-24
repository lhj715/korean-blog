"""2024학년도 9월 고2 13~15번(문법 단독 문항 묶음, 안내문 없음) 세트: 초안 + 쪽 그림 확인값 + 해설지 기반 판단 → 세트_13-15.json

초안은 _임시\\뽑기래퍼.py(세트_뽑기.py 에서 선지·문단 첫 줄 앞 공백만 허용하게 고친 복사본)로 뽑았다(_임시\\초안_13-15.json, 문단시작 파일은 빈 파일).
쪽 그림(문제_5쪽_오른쪽, 문제_6쪽_왼쪽)과 PDF 좌표로 확인한 것:
- 13번: <보 기> 한 상자. 중세 국어 목적격 조사 문단은 옛한글(PUA)이 있어 문단 전체를 쪽에서 오려 낸 그림(display_image).
  예문 3줄(◦ + 옛한글 + 번역 줄)도 줄마다 PUA 가 있어 그림. 번역 줄 «[…]» 은 글. 굵은 글씨·밑줄 없음(발문 밑줄 없음).
  선지는 ㉠ ㉡ ㉢ 세 칸 표. 열 머리 ㉠㉡㉢ 는 밑줄(plain 상자). 선지 칸 안의 옛한글 PUA 4종(e288, e6d7, e38f, e470)은 choice_images.
- 14번: <보 기> 한 줄(㉠닭장[닥짱] ㉡끓는[끌른] ㉢홑이불[혼니불]). 굵은 글씨·밑줄 없음. 발문 밑줄 '않은'. [3점].
- 15번: <보 기> 문장 5줄(㉠~㉤). 밑줄·굵은 글씨 없음. 발문 밑줄 '않은'.
"""
import json
import re

HERE = r"D:\Work\블로그\리딩맵\작업\20240904-go2"
d = json.load(open(HERE + r"\_임시\초안_13-15.json", encoding="utf-8"))
d.pop("raw_passage_lines", None)
d["meta"] = {"exam": "2024학년도 9월 고2 전국연합학력평가 국어", "exam_id": "20240904-go2", "area": "문법",
             "topic": "중세 국어의 목적격 조사·음운 변동·안은문장", "problem_pdf": "20240904-go2-problem-kor_mun_M8138S5W.pdf",
             "explanation_pdf": "20240904-go2-explanation-kor_hsj_E91AW835.pdf"}
d["guide"] = None
d["passage"] = []
Q = {q["no"]: q for q in d["questions"]}
SP = "\u3000"

expl = open(HERE + r"\해설_글자.txt", encoding="utf-8").read()


def section(no):
    i = expl.index(f"\n{no}. [출제의도]")
    j = expl.index(f"\n{no + 1}. [출제의도]", i) if no < 15 else expl.index("** 현대 소설", i)
    return expl[i:j]


def X(no, a, b):
    sec = section(no)
    keep = [(i, c) for i, c in enumerate(sec) if not c.isspace()]
    comp = "".join(c for _, c in keep)
    ca, cb = re.sub(r"\s+", "", a), re.sub(r"\s+", "", b)
    ia = comp.index(ca)
    ib = comp.index(cb, ia) + len(cb)
    return sec[keep[ia][0]: keep[ib - 1][0] + 1].replace("\n", "")


def sub(text, a, b):
    i = text.index(a)
    return text[i: text.index(b, i) + len(b)]


def J(choice, verdict, ans, ev, basis, reason, xq=None):
    out = {"choice": choice, "verdict": verdict, "is_answer": ans, "basis": basis, "reason": reason,
           "evidence": [{"source": "bogi", "para": None, "quote": e} for e in ev]}
    if xq:
        out["explanation_quote"] = xq
    return out


# ================= 13번
s13 = Q[13]["stem"]
Q[13]["stem"] = s13[: s13.index("것은?") + 3]
body = s13[s13.index("<보 기>") + 5:]
j0 = body.index("◦")
B1 = body[:j0].strip()
rest = body[j0:]
assert rest.rstrip().endswith("㉠㉡㉢")
rest = rest.rstrip()[: -len("㉠㉡㉢")]
parts = [p for p in re.split(r"(?=◦)", rest) if p.strip()]
assert len(parts) == 3
EX, TR = [], []
for p in parts:
    k = p.index("[")
    EX.append(p[:k].strip())
    TR.append(p[k:].strip())
assert TR == ["[손을 손수 잡으시어]", "[세존께 내 뜻을 펴 아뢰십시오.]", "[왕이 부처를 청하십시오.]"], TR
Q[13]["bogi"] = [
    {"label": "보 기", "blocks": [
        {"id": "b1", "type": "para", "text": B1, "display_image": "그림_13-15_13_보기.png", "underlines": []},
        {"id": "e1", "type": "para", "text": EX[0], "display_image": "그림_13-15_13_예1.png", "underlines": []},
        {"id": "r1", "type": "para", "text": TR[0], "underlines": []},
        {"id": "e2", "type": "para", "text": EX[1], "display_image": "그림_13-15_13_예2.png", "underlines": []},
        {"id": "r2", "type": "para", "text": TR[1], "underlines": []},
        {"id": "e3", "type": "para", "text": EX[2], "display_image": "그림_13-15_13_예3.png", "underlines": []},
        {"id": "r3", "type": "para", "text": TR[2], "underlines": []}]},
    {"label": "", "plain": True, "blocks": [
        {"id": "th", "type": "heading", "text": "㉠" + SP * 8 + "㉡" + SP * 8 + "㉢",
         "underlines": [{"mark": "", "text": "㉠"}, {"mark": "", "text": "㉡"}, {"mark": "", "text": "㉢"}]}]},
]
CELLS = [("소\ue288", "\ue6d7들", "부텨를"), ("소\ue288", "\ue6d7\ue38f", "부텨를"),
         ("소\ue288", "\ue6d7들", "부텨\ue470"), ("소늘", "\ue6d7\ue38f", "부텨\ue470"), ("소늘", "\ue6d7들", "부텨를")]
for k, cells in enumerate(CELLS):
    assert "".join(cells) == Q[13]["choices"][k], (k, cells, Q[13]["choices"][k])
    Q[13]["choices"][k] = cells[0] + SP * 7 + cells[1] + SP * 6 + cells[2]
GL = {"\ue288": ("그림_13-15_13_선지_a.png", "ᄂᆞᆯ"), "\ue6d7": ("그림_13-15_13_선지_b.png", "ᄠᅳ"),
      "\ue38f": ("그림_13-15_13_선지_c.png", "ᄃᆞᆯ"), "\ue470": ("그림_13-15_13_선지_d.png", "ᄅᆞᆯ")}
Q[13]["choice_images"] = {}
for k, c in enumerate(Q[13]["choices"], 1):
    Q[13]["choice_images"][str(k)] = [{"text": g, "image": GL[g][0], "alt": GL[g][1]} for g in GL if g in c]

Q_FIRST = sub(B1, "먼저,", "실현되었는데,")
Q_BATCH = sub(B1, "앞말에 받침이 있을 때에는", "나타나기도 하였다.")
Q_YANG = sub(B1, "또한, 앞말의 모음이", "실현되었다.")
E1, E2, E3 = EX[0], EX[1], EX[2]
XA = X(13, "㉠은", "나타난 경우이다.")
XB = X(13, "㉡은", "나타난 경우이다.")
XC = X(13, "㉢은", "실현된 경우이다.")
Q[13]["answer"] = 1
Q[13]["judgments"] = [
    J(1, "적절", True, [Q_FIRST, Q_BATCH, Q_YANG, E1, E2, E3], "해설지",
      "㉠은 양성 모음 뒤라 ‘ᄋᆞᆯ’이 쓰이고 앞말의 받침이 이어 적혀 ‘소ᄂᆞᆯ’, ㉡은 음성 모음 뒤라 ‘을’이 쓰이고 받침이 이어 적혀 ‘ᄠᅳ들’, ㉢은 받침이 없는 음성 모음 뒤라 ‘를’이 쓰인 ‘부텨를’이다. 세 칸이 모두 맞다.",
      XA + " " + XB + " " + XC),
    J(2, "부적절", False, [Q_YANG, E2], "해설지",
      "㉡의 앞말은 음성 모음으로 끝나므로 ‘을’이 이어 적힌 ‘ᄠᅳ들’이 와야 한다. 양성 모음 뒤에 쓰는 ‘ᄋᆞᆯ’이 이어 적힌 ‘ᄠᅳᄃᆞᆯ’은 맞지 않는다.",
      XB),
    J(3, "부적절", False, [Q_FIRST, Q_YANG, E3], "해설지",
      "㉢은 앞말에 받침이 없고 음성 모음이므로 ‘를’이 쓰여 ‘부텨를’이 되어야 한다. 양성 모음 뒤에 쓰는 ‘ᄅᆞᆯ’은 맞지 않는다.",
      XC),
    J(4, "부적절", False, [Q_YANG, E1, E2, E3], "해설지",
      "㉠은 ‘소ᄂᆞᆯ’이어야 하고, ㉡은 ‘ᄠᅳ들’, ㉢은 ‘부텨를’이어야 한다. ‘소늘’, ‘ᄠᅳᄃᆞᆯ’, ‘부텨ᄅᆞᆯ’은 세 칸이 모두 맞지 않는다.",
      XA + " " + XB + " " + XC),
    J(5, "부적절", False, [Q_BATCH, E1], "해설지",
      "㉠은 양성 모음 ‘ㅗ’ 뒤에서 받침을 이어 적은 ‘소ᄂᆞᆯ’이어야 한다. ‘소늘’은 양성 모음 뒤에 음성 모음 형태의 조사를 쓴 것이라 맞지 않는다.",
      XA),
]

# ================= 14번
s14 = Q[14]["stem"]
Q[14]["points"] = 3
Q[14]["stem"] = s14[: s14.index("[3점]")].strip()
Q[14]["stem_underlines"] = ["않은"]
b14 = s14[s14.index("<보 기>") + 5:].strip()
assert b14 == "㉠닭장[닥짱]    ㉡끓는[끌른]    ㉢홑이불[혼니불]", repr(b14)
Q[14]["bogi"] = {"label": "보 기", "blocks": [{"id": "b1", "type": "para", "text": b14, "underlines": []}]}
Q[14]["answer"] = 2
K, N, H = "㉠닭장[닥짱]", "㉡끓는[끌른]", "㉢홑이불[혼니불]"
Q[14]["judgments"] = [
    J(1, "적절", False, [K, N], "해설지",
      "㉠은 겹받침 중 ‘ㄹ’이, ㉡은 겹받침 중 ‘ㅎ’이 탈락하는 자음군 단순화가 일어난다. 둘 다 음절 끝에 둘 이상의 자음이 오지 못하기 때문에 일어나는 변동이다.",
      X(14, "①㉠에서는", "음운 변동이다.")),
    J(2, "부적절", True, [N, H], "해설지",
      "㉡은 뒤의 ‘ㄴ’이 앞의 ‘ㄹ’에 동화되어 [끌른]이 되므로, 앞의 자음이 뒤의 자음에 동화된다는 설명은 틀리다.",
      X(14, "㉡의 ‘끓는’은", "음운 변동이 일어난다.")),
    J(3, "적절", False, [K, H], "해설지",
      "㉠에서 탈락한 음운은 ‘ㄹ’이고 ㉢에서 첨가된 음운은 ‘ㄴ’이어서 서로 다르다.",
      X(14, "③㉠에서 탈락된", "서로 다르다.")),
    J(4, "적절", False, [K, N, H], "해설지",
      "㉢은 음운 개수가 7개에서 8개로 하나 늘었고, ㉠과 ㉡은 7개에서 6개로 하나 줄었다.",
      X(14, "④㉢에서는", "줄었다.")),
    J(5, "적절", False, [N, H, K], "해설지",
      "㉡은 비음 ‘ㄴ’이 유음 ‘ㄹ’로, ㉢은 파열음 ‘ㄷ’이 비음으로 바뀌어 인접한 자음과 조음 방법이 같아졌다. ㉠은 ‘ㄱ’과 ‘ㅉ’의 조음 방법이 같지 않다.",
      X(14, "⑤㉡은", "같지 않다.")),
]

# ================= 15번
s15 = Q[15]["stem"]
Q[15]["stem"] = s15[: s15.index("것은?") + 3]
Q[15]["stem_underlines"] = ["않은"]
b15 = s15[s15.index("<보 기>") + 5:].strip()
S15 = [x for x in re.split(r"(?=[㉠㉡㉢㉣㉤])", b15) if x.strip()]
assert len(S15) == 5, S15
Q[15]["bogi"] = {"label": "보 기", "blocks": [
    {"id": f"b{k+1}", "type": "para", "text": t.strip(), "underlines": []} for k, t in enumerate(S15)]}
S = [t.strip() for t in S15]
Q[15]["answer"] = 1
Q[15]["judgments"] = [
    J(1, "부적절", True, [S[0]], "해설지",
      "㉠은 인용절을 가진 안은문장이다. 안은문장의 주어는 ‘그는’, 안긴문장의 주어는 ‘영수가’로 안긴문장의 주어가 생략되어 있지 않다.",
      X(15, "‘그는 영수가", "생략되어 있지 않다.")),
    J(2, "적절", False, [S[1]], "자체",
      "㉡은 ‘그녀가 산’이 ‘책’을 꾸미는 관형사절을 가진 안은문장이다. 안은문장의 주어는 ‘이것은’, 안긴문장의 주어는 ‘그녀가’이다."),
    J(3, "적절", False, [S[2]], "자체",
      "㉢은 ‘흐드러지게’가 서술어 ‘피었다’를 꾸미는 부사절을 가진 안은문장이다. 안긴문장의 주어는 안은문장의 주어 ‘개나리꽃이’와 같아 생략되어 있다."),
    J(4, "적절", False, [S[3]], "자체",
      "㉣은 ‘마음씨가 매우 착하다’가 서술어 역할을 하는 서술절을 가진 안은문장이다. 안은문장의 주어는 ‘영철이는’, 안긴문장의 주어는 ‘마음씨가’이다."),
    J(5, "적절", False, [S[4]], "자체",
      "㉤은 ‘아이들이 행복하기’가 목적어 역할을 하는 명사절을 가진 안은문장이다. 안은문장의 주어는 ‘나는’, 안긴문장의 주어는 ‘아이들이’이다."),
]

json.dump(d, open(HERE + r"\세트_13-15.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok")
