"""2025-09 고1 13~15번(문법 단독 문항) 세트: 초안 + 쪽 그림 확인값 + 해설지 기반 판단 → 세트_13-15.json

초안은 _임시\초안_뽑기_13-21.py(도구/세트_뽑기.py 의 줄 앞 공백 대응 래퍼)로 뽑았다(_임시\초안_13-15.json). 이 PDF 는 선지 줄이 «  ① …» 처럼 앞 공백이 있어 도구가 그대로는 멈춘다.
쪽 그림(문제_5쪽_오른쪽.png, 문제_6쪽_왼쪽.png)과 PDF 좌표(그림_위치_13-15.json)로 확인한 것:
- 안내문·지문 없음(guide null, passage []). 문항마다 자기 상자가 있다.
- 13번: <학습 활동> 상자 = 표(그림, 래스터 아님: 선·글자가 벡터라 쪽에서 잘라 그림으로) + 설명 문단 + «[자료]»(굵음) + 안쪽 상자(낱말 목록, 가운데 맞춤).
  발문 밑줄 '않은'. 선지는 «시제 | 문장» 두 칸 표: 표 머리(시제·문장, 밑줄 있음)는 머리말 없는 plain 상자, 선지 글은 '시제 + 전각 공백 + 문장',
  선지 안 밑줄 낱말(잔·푸르던·깨끗한·읽은·떠날)은 choice_underlines. 표 글자의 소프트 하이픈(U+00AD)은 PDF 글 그대로 둔다.
- 14번: <보기> = «[탐구 과정]»(굵음) + 순서도(그림, 마름모·화살표 도형 + 글자 ㉮㉯㉰, «아니요»·«예» 는 도형 그림이라 텍스트층에 없다). 발문 밑줄 '않은', [3점].
- 15번: <보기> = 예문 3개(각각 «∘예문 / [현대어 풀이] / －『출전』» 세 줄). 예문에 옛한글 PUA 글자가 있어(U+F1FC·E57B·E6D2…) 세 줄을 쪽에서 오려 낸 그림(display_image)으로 보이고
  (예문 안 굵은 글씨도 그림에 들어 있다), 글에는 PUA 를 그대로 둔다. 출전 줄 앞의 «－『 』» 세 글자는 텍스트층에서 U+F000 이라 글에는 『 』 만 둔다(검사기가 U+F000·『』 를 같게 본다).
  선지 ②③④ 안의 옛한글 PUA 글자 4개는 choice_images(쪽에서 오려 낸 작은 그림). 발문 밑줄 '않은'.
"""
import json
import re

HERE = r"D:\Work\블로그\리딩맵\작업\20250903-go1"
d = json.load(open(HERE + r"\_임시\초안_13-15.json", encoding="utf-8"))
d.pop("raw_passage_lines", None)
d["meta"] = {"exam": "2025년 9월 고1 전국연합학력평가 국어", "exam_id": "20250903-go1", "area": "문법",
             "topic": "관형사형 어미의 시제·높임 표현·중세 국어의 특징", "problem_pdf": "20250903-go1-problem-kor_mun_E77XJM41_1.pdf",
             "explanation_pdf": "20250903-go1-explanation-kor_hsj_YR115187_1.pdf"}
d["guide"] = None
d["passage"] = []
Q = {q["no"]: q for q in d["questions"]}
SP = "\u3000"
SH = "\u00ad"  # 소프트 하이픈(표 안 어미 앞)

expl = open(HERE + r"\해설_글자.txt", encoding="utf-8").read()


def section(no):
    i = expl.index(f"\n{no}. [출제의도]")
    j = expl.index(f"\n{no + 1}. [출제의도]", i)
    return expl[i:j]


def X(no, a, b, skip_marker=False):
    """해설지 그 문항 해설에서 a 로 시작해 b 로 끝나는 글(줄바꿈만 이어 붙임). skip_marker: a 앞의 원문자 한 글자는 뺀다."""
    sec = section(no)
    keep = [(i, c) for i, c in enumerate(sec) if not c.isspace()]
    comp = "".join(c for _, c in keep)
    ca, cb = re.sub(r"\s+", "", a), re.sub(r"\s+", "", b)
    ia = comp.index(ca)
    ib = comp.index(cb, ia) + len(cb)
    out = sec[keep[ia][0]: keep[ib - 1][0] + 1].replace("\n", "")
    return out[1:] if skip_marker else out


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
s13 = Q[13]["stem"]
Q[13]["stem"] = s13[: s13.index("것은?") + 3]
Q[13]["stem_underlines"] = ["않은"]
F13 = s13[s13.index("품사"): s13.index("위 표는")]
assert F13 == f"품사시제       동사형용사과거{SH}(으)ㄴ, {SH}던{SH}던현재{SH}는{SH}(으)ㄴ미래{SH}(으)ㄹ{SH}(으)ㄹ", repr(F13)
B13 = s13[s13.index("위 표는"): s13.rindex("[자료]")]
LIST13 = s13[s13.rindex("[자료]") + len("[자료]"): s13.rindex("시제")]
assert LIST13 == "자다, 푸르다, 깨끗하다, 읽다, 떠나다", LIST13
assert s13[s13.rindex("시제"):].replace(" ", "") == "시제문장"
Q[13]["bogi"] = [
    {"label": "학습 활동", "blocks": [
        {"id": "f13", "type": "figure", "caption": "", "image": "그림_13-15_13_표.png", "pdf_text": F13,
         "alt": "시제별 관형사형 어미 표. 동사: 과거 -(으)ㄴ, -던 / 현재 -는 / 미래 -(으)ㄹ. 형용사: 과거 -던 / 현재 -(으)ㄴ / 미래 -(으)ㄹ."},
        {"id": "b1", "type": "para", "text": B13.strip(), "underlines": []},
        {"id": "b2", "type": "para", "text": "[자료]", "bold": ["[자료]"], "underlines": []},
        {"id": "b3", "type": "para", "text": LIST13, "inbox": "자료", "center": True, "underlines": []},
    ]},
    {"label": "", "plain": True, "blocks": [
        {"id": "h1", "type": "heading", "text": "시제" + SP * 6 + "문장",
         "underlines": [{"mark": "", "text": "시제"}, {"mark": "", "text": "문장"}]}]},
]
tense = ["과거", "과거", "현재", "현재", "미래"]
for k, c in enumerate(Q[13]["choices"]):
    assert c.startswith(tense[k]), c
    Q[13]["choices"][k] = tense[k] + SP * 2 + c[len(tense[k]):].strip()
Q[13]["choice_underlines"] = {"1": ["잔"], "2": ["푸르던"], "3": ["깨끗한"], "4": ["읽은"], "5": ["떠날"]}

T = "f13"
Q[13]["answer"] = 4
Q[13]["judgments"] = [
    J(1, "적절", False, [("fig", T, f"과거{SH}(으)ㄴ, {SH}던")], "해설지",
      "‘잔’은 동사 ‘자다’의 어간에 관형사형 어미 ‘-ㄴ’이 결합한 과거 시제 표현이다. 표에서 동사의 과거는 ‘-(으)ㄴ, -던’이다.",
      X(13, "동사 ‘자다’의", "나타낸다.")),
    J(2, "적절", False, [("fig", T, f"(으)ㄴ, {SH}던{SH}던")], "해설지",
      "‘푸르던’은 형용사 ‘푸르다’의 어간에 어미 ‘-던’이 결합한 과거 시제 표현이다. 표에서 형용사의 과거는 ‘-던’이다.",
      X(13, "형용사 ‘푸르다’의", "나타낸다.")),
    J(3, "적절", False, [("fig", T, f"현재{SH}는{SH}(으)ㄴ")], "해설지",
      "‘깨끗한’은 형용사 ‘깨끗하다’의 어간에 어미 ‘-ㄴ’이 결합한 현재 시제 표현이다. 표에서 형용사의 현재는 ‘-(으)ㄴ’이다.",
      X(13, "형용사 ‘깨끗하다’의", "나타낸다.")),
    J(4, "부적절", True, [("fig", T, f"현재{SH}는")], "해설지",
      "‘읽은’은 동사 ‘읽다’의 어간에 어미 ‘-은’이 결합한 과거 시제 표현이어서 현재 시제 문장에 맞지 않는다. 표에서 동사의 현재는 ‘-는’이므로 ‘읽는’으로 써야 한다.",
      X(13, "‘읽은’은 동사", "활용해야 한다.")),
    J(5, "적절", False, [("fig", T, f"미래{SH}(으)ㄹ{SH}(으)ㄹ")], "해설지",
      "‘떠날’은 동사 ‘떠나다’의 어간에 어미 ‘-ㄹ’이 결합한 미래 시제 표현이다. 표에서 동사의 미래는 ‘-(으)ㄹ’이다.",
      X(13, "동사 ‘떠나다’의", "나타낸다.")),
]

# ================= 14번
s14 = Q[14]["stem"]
Q[14]["points"] = 3
Q[14]["stem"] = s14[: s14.index("[3점]")].strip()
Q[14]["stem_underlines"] = ["않은"]
F14 = s14[s14.index("문장에서 주체를높이기"):]
assert F14 == "문장에서 주체를높이기 위한 특수 어휘가문장에서 주체를 높이는 표현이㉰㉮㉯쓰이고 있는가?쓰이고 있는가?", repr(F14)
assert s14[s14.index("<보 기>"):].replace(" ", "").startswith("<보기>[탐구과정]문장에서")
Q[14]["bogi"] = {"label": "보 기", "blocks": [
    {"id": "b1", "type": "para", "text": "[탐구 과정]", "bold": ["[탐구 과정]"], "underlines": []},
    {"id": "f14", "type": "figure", "caption": "", "image": "그림_13-15_14_탐구과정.png", "pdf_text": F14,
     "alt": "탐구 과정 순서도. ‘문장에서 주체를 높이는 표현이 쓰이고 있는가?’에 ‘아니요’면 ㉮, ‘예’이면 ‘문장에서 주체를 높이기 위한 특수 어휘가 쓰이고 있는가?’로 간다. 여기서 ‘아니요’면 ㉯, ‘예’이면 ㉰."}]}
F = "f14"
Q[14]["answer"] = 4
Q[14]["judgments"] = [
    J(1, "적절", False, [("fig", F, "문장에서 주체를 높이는 표현이")], "해설지",
      "‘뵙고’는 ‘보다’의 높임말로 객체를 높이는 표현일 뿐, 주체를 높이는 표현은 쓰이지 않았다. 첫 물음에서 ‘아니요’로 가므로 ㉮에 들어간다.",
      X(14, "‘고모를 뵙고’에서", "사용되지 않았다.")),
    J(2, "적절", False, [("fig", F, "주체를 높이는 표현이")], "해설지",
      "‘께서’나 ‘-(으)시-’ 같은 주체를 높이는 표현이 쓰이지 않았으므로 첫 물음에서 ‘아니요’로 가 ㉮에 들어간다.",
      X(14, "‘께서’나", "사용되지 않았다.")),
    J(3, "적절", False, [("fig", F, "높이기 위한 특수 어휘가")], "해설지",
      "‘입으셔야’에는 주체 높임 선어말 어미 ‘-으시-’가 쓰여 주체를 높였지만 특수 어휘는 쓰이지 않았다. 둘째 물음에서 ‘아니요’로 가므로 ㉯에 들어간다.",
      X(14, "‘입으셔야’에서", "사용되지 않았다.")),
    J(4, "부적절", True, [("fig", F, "문장에서 주체를 높이는 표현이㉰㉮")], "해설지",
      "‘선생님께’의 ‘께’는 부사격 조사 ‘에게’의 높임으로 객체를 높이는 표현이다. 문장의 주체인 동생을 높이는 표현은 쓰이지 않았으므로 ㉯가 아니라 ㉮에 들어가야 한다.",
      X(14, "‘선생님께’에서", "적절하지 않다.")),
    J(5, "적절", False, [("fig", F, "특수 어휘가문장에서 주체를 높이는 표현이㉰")], "해설지",
      "‘할머니께서는’의 ‘께서’로 주체를 높이는 표현이 쓰였고, ‘주무시니’는 ‘자다’를 높인 특수 어휘이다. 두 물음에 모두 ‘예’이므로 ㉰에 들어간다.",
      X(14, "‘할머니께서는’의", "확인할 수 있다.")),
]

# ================= 15번
s15 = Q[15]["stem"]
Q[15]["stem"] = s15[: s15.index("<보 기>")]
Q[15]["stem_underlines"] = ["않은"]
body = s15[s15.index("<보 기>") + len("<보 기>"):]
ex = [e for e in body.split("∘") if e.strip()]
assert len(ex) == 3, len(ex)
texts15 = []
PUA = chr(0xF000)
for e in ex:
    t = re.sub(r"\s+", " ", "∘" + e).strip()
    # 출전 줄 «－『…』»: 텍스트층에서 세 글자(줄표·『·』)가 모두 U+F000. 검사기는 『 』 를 U+F000 으로 보므로 «U+F000『…』» 로 쓴다(앞의 U+F000 은 줄표, 화면은 그림이 보인다)
    t = re.sub(PUA + PUA + "([^" + PUA + "]+)" + PUA, PUA + r"『\1』", t)
    assert t.count(PUA) == 1 and "『" in t, repr(t)
    t = re.sub(r"(?<=\S)(?=\[)", " ", t)
    t = re.sub("(?<=\S)(?=" + PUA + ")", " ", t)
    texts15.append(t)
assert texts15[0].startswith("∘부톄 안\uf1fc시니 [부처가 앉으시니] " + PUA + "『월인천강지곡』"), repr(texts15[0])
assert texts15[1].endswith("[봄에 와 있는 만 리 밖의 나그네는] " + PUA + "『두시언해』"), repr(texts15[1])
assert texts15[2].endswith("[물고기 뛰노니 해가 산에 비치어 있도다] " + PUA + "『두시언해』"), repr(texts15[2])
Q[15]["bogi"] = {"label": "보 기", "blocks": [
    {"id": f"e{k+1}", "type": "para", "text": t, "display_image": f"그림_13-15_15_예문{k+1}.png", "underlines": []}
    for k, t in enumerate(texts15)]}
Q[15]["choice_images"] = {
    "2": [{"text": "\uf1fc", "image": "그림_13-15_15_선지_a.png", "alt": "ᄌᆞ"}],
    "3": [{"text": "\ue57b", "image": "그림_13-15_15_선지_b.png", "alt": "ᄆᆡ"},
          {"text": "\ueea4", "image": "그림_13-15_15_선지_c.png", "alt": "ᄋᆡ"}],
    "4": [{"text": "\ue6d2", "image": "그림_13-15_15_선지_d.png", "alt": "ᄠᅱ"}],
}
for k, lst in Q[15]["choice_images"].items():
    for ci in lst:
        assert ci["text"] in Q[15]["choices"][int(k) - 1]
Q[15]["answer"] = 3
Q[15]["judgments"] = [
    J(1, "적절", False, [("bogi", "부톄")], "해설지",
      "‘부톄’는 ‘부텨’에 주격 조사 ‘ㅣ’가 결합한 형태이므로 현대 국어와 달리 주격 조사 ‘ㅣ’가 쓰였음을 알 수 있다.",
      X(15, "‘부톄’는", "결합한 것이다.")),
    J(2, "적절", False, [("bogi", "안\uf1fc시니")], "해설지",
      "첫째 예문의 ‘앉으시니’에 해당하는 말은 어간 ‘앉-’에 어미가 결합한 것을 소리 나는 대로 이어 적은 것이므로 이어 적기를 했음을 알 수 있다.",
      X(15, "②", "이어 적기가 된 것이다.", True)),
    J(3, "부적절", True, [("bogi", "보\ue57b")], "해설지",
      "둘째 예문의 ‘봄에’에 해당하는 말은 ‘와 있는’과 호응하는 부사어이므로 그 끝의 조사는 관형격 조사가 아니라 부사격 조사이다. 중세 국어에서는 현대 국어와 달리 부사격 조사로 이 조사도 쓰였다.",
      X(15, "‘보", "쓰였다.")),
    J(4, "적절", False, [("bogi", "\ue6d2노니")], "해설지",
      "셋째 예문의 ‘뛰노니’에 해당하는 말은 첫머리에 ‘ㅳ’이 쓰여 어두자음군이 존재했음을 알 수 있다.",
      X(15, "④", "알 수 있다.", True)),
    J(5, "적절", False, [("bogi", "뫼헤")], "해설지",
      "‘뫼헤’는 ‘ㅎ’ 종성 체언인 ‘뫼ㅎ’에 부사격 조사 ‘에’가 결합한 것이므로 ‘ㅎ’ 종성 체언이 사용되었음을 알 수 있다.",
      X(15, "‘뫼헤’는", "결합한 것이다.")),
]

json.dump(d, open(HERE + r"\세트_13-15.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok")
