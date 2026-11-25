"""2026-10 고2 1~3번 세트(화법, 발표): 초안 + 쪽 그림 확인값 + 해설지 기반 판단 → 세트_1-3.json

초안: _임시/뽑기_1-3.py (세트_뽑기.py 를 선지 앞 공백·선지 줄 없는 2번만 고쳐 부르는 래퍼) → _임시/초안_1-3.json

쪽 그림·PDF 로 확인한 것(문제_1쪽.png, _임시/z_1-3_bogi.png, texttrace·선 좌표):
- 발표 지문은 상자 안 4문단(안녕하세요 / 정보성이란 / 이때 / 지금까지). 첫 줄 x=104, 이어지는 줄 x=93.5. 굵은 글씨 없음.
- 밑줄: ㉠ «담화의 정보성을 조절»(두 줄에 걸친 선, 기호는 선 밖). 2·3번 발문 '않은' 밑줄. 1번 발문 밑줄 없음.
- 2번: 발문 아래 계획 상자. [도입]·[전개]·[정리] 는 굵음(type 0+1), ◦ 항목은 보통. 항목 끝 점선 뒤 ①~⑤ → choices_in_box.
- 3번 <보 기>: «선생님:»·«학생:» 콜론까지 굵음(type 0+1). 안쪽 상자 «[추가 자료]»(굵음)와 «지온:»·«하준:»(콜론까지 굵음) → inbox.
  ⓐ~ⓔ 뒤 밑줄(기호는 선 밖, 그림의 기호 뒤 간격대로 한 칸 띄움). «학생:» 뒤 긴 밑줄 빈칸 위의 [A] → blank.
- 1~3번 배점 표시 없음.
"""
import json
import re

HERE = r"D:\Work\블로그\리딩맵\작업\20261020-go2"
d = json.load(open(HERE + r"\_임시\초안_1-3.json", encoding="utf-8"))
d.pop("raw_passage_lines", None)
d["meta"] = {"exam": "2026학년도 10월 고2 전국연합학력평가 국어", "exam_id": "20261020-go2", "area": "화법",
             "topic": "담화의 정보성에 대한 발표",
             "problem_pdf": "20261020-go2-problem-kor_mun_3R69236R.pdf",
             "explanation_pdf": "20261020-go2-explanation-kor_hsj_VAK354D2.pdf"}
d["guide"] = "[1 ~ 3] 다음은 수업 시간 중 학생의 발표이다. 물음에 답하시오."
P = {p["id"]: p for p in d["passage"]}
assert [P[k]["text"][:3] for k in ("p1", "p2", "p3", "p4")] == ["안녕하", "정보성", "이때 ", "지금까"]
U = "담화의 정보성을 조절"
assert "㉠" + U in P["p2"]["text"]
P["p2"]["underlines"] = [{"mark": "㉠", "text": U}]
Q = {q["no"]: q for q in d["questions"]}
Q[2]["stem_underlines"] = ["않은"]
Q[3]["stem_underlines"] = ["않은"]


def para(i, text, **kw):
    out = {"id": i, "type": "para", "text": text, "underlines": []}
    out.update(kw)
    return out


# 2번 계획 상자
s2 = Q[2]["stem"]
i = s2.index("[도입]")
Q[2]["stem"] = s2[:i].strip()
assert Q[2]["stem"].endswith("반영되지 않은 것은?")
parts = [x.strip() for x in re.split(r"(?=\[(?:도입|전개|정리)\]|◦)", s2[i:]) if x.strip()]
assert len(parts) == 8, parts
blocks, choices = [], []
for k, t in enumerate(parts, 1):
    if t.startswith("◦"):
        t = "◦ " + t[1:].strip()
        m = re.match(r"^◦ (.*?)\s*·{4,}\s*[①②③④⑤]$", t)
        assert m, t
        choices.append(m.group(1))
        blocks.append(para(f"b{k}", t))
    else:
        blocks.append(para(f"b{k}", t, bold=[t]))
assert len(choices) == 5
Q[2]["bogi"] = {"label": "", "blocks": blocks}
Q[2]["choices"] = choices
Q[2]["choices_in_box"] = True

# 3번 ⑤ 뒤에 붙은 쪽 머리글 제거
c5 = Q[3]["choices"][4]
Q[3]["choices"][4] = c5[: c5.index("2026학년도")].strip()
assert Q[3]["choices"][4].endswith("신정보를 제시하고 있습니다.")

# 3번 발문 / <보 기>
s3 = Q[3]["stem"]
i = s3.index("보 기선생님")
Q[3]["stem"] = s3[:i].strip()
assert Q[3]["stem"].endswith("적절하지 않은 것은?")
rest = s3[i + len("보 기"):].strip()
a = rest.index("학생: ")
b = rest.index("선생님: 네")
c = rest.index("[추가 자료]")
teacher1, student, teacher2, extra = rest[:a].strip(), rest[a:b].strip(), rest[b:c].strip(), rest[c:]
assert re.sub(r"\s+", " ", student) == "학생: [A]"
talk = [x.strip() for x in re.split(r"(?=(?:지온|하준): )", extra[len("[추가 자료]"):]) if x.strip()]
assert len(talk) == 9, talk
blocks = [para("t1", teacher1, dialogue=True, bold=["선생님:"]),
          para("x0", "[추가 자료]", bold=["[추가 자료]"], inbox="추가 자료")]
marks = []
for k, t in enumerate(talk, 1):
    name = t[:3]
    extra_kw = {}
    m = re.search(r"([ⓐⓑⓒⓓⓔ])\s*", t)
    if m:
        mark = m.group(1)
        t = t[: m.start()] + mark + " " + t[m.end():]
        body = t[t.index(mark) + 2:]
        if mark == "ⓒ":
            body = body[: body.index("부탁하려고.") + len("부탁하려고.")]
        extra_kw["underlines"] = [{"mark": mark, "text": body}]
        marks.append(mark)
    blocks.append(para(f"x{k}", t, dialogue=True, bold=[name], inbox="추가 자료", **extra_kw))
assert marks == list("ⓐⓑⓒⓓⓔ")
blocks.append(para("s1", "학생: [A]", dialogue=True, bold=["학생:"], blank="[A]"))
blocks.append(para("t2", teacher2, dialogue=True, bold=["선생님:"]))
Q[3]["bogi"] = {"label": "보 기", "blocks": blocks}

for n in (1, 2, 3):
    Q[n]["choices"] = [re.sub(r"\s+", " ", c).strip() for c in Q[n]["choices"]]
    assert len(Q[n]["choices"]) == 5


def J(choice, verdict, ans, ev, basis, reason, xq=None):
    out = {"choice": choice, "verdict": verdict, "is_answer": ans, "basis": basis, "reason": reason,
           "evidence": [{"source": s, "para": p, "quote": q} for s, p, q in ev]}
    if xq:
        out["explanation_quote"] = xq
    return out


def Pa(i, q):
    return ("passage", i, q)


def Bo(q):
    return ("bogi", None, q)


Q[1]["answer"] = 2
Q[1]["judgments"] = [
    J(1, "부적절", False, [Pa("p1", "오늘 저는 이러한 정보성에 대해 조사한 내용을 발표하겠습니다.")], "자체",
      "발표자는 조사한 내용을 발표한다고만 말한다. 그 내용을 어디에서 가져왔는지 자료의 출처는 발표 어디에서도 밝히지 않는다."),
    J(2, "적절", True, [Pa("p1", "그런데 이러한 생략은 담화의 요건 중 하나인 ‘정보성’과 관련된다는 사실, 알고 계셨나요? (대답을 듣고) 네, 생소하게 들리시죠?")], "해설지",
      "발표자는 청중에게 알고 있었는지 묻고, 대답을 들은 뒤 다시 질문을 던지며 청중과 주고받듯 발표를 이어 간다.",
      "청중과 상호 작용하고 있음을 확인할 수 있으므로 적절하다"),
    J(3, "부적절", False, [Pa("p1", "(대답을 듣고) 네, 생소하게 들리시죠?")], "자체",
      "발표자는 청중의 대답을 듣고 반응을 확인할 뿐이다. 청중이 무엇을 해 달라고 요청하거나 그에 따라 발표 내용을 바꾸는 장면은 없다."),
    J(4, "부적절", False, [Pa("p2", "정보성이란 담화의 내용이 수용자에게 정보로서의 가치가 있어야 함을 뜻합니다.")], "자체",
      "제재인 정보성은 뜻을 직접 풀어 설명한다. 친숙한 다른 대상에 빗대어 표현한 부분은 없다."),
    J(5, "부적절", False, [Pa("p4", "(목소리를 높여) 발표를 들은 여러분이 일상의 담화에서 정보성을 적절하게 조절함으로써 청자를 배려하며 원활하게 소통하는 사람이 되기를 바랍니다.")], "자체",
      "발표자는 청중에게 바라는 점을 말하며 발표를 마친다. 정보를 더 찾아볼 수 있는 방법은 안내하지 않는다."),
]

Q[2]["answer"] = 4
Q[2]["judgments"] = [
    J(1, "반영", False, [Pa("p1", "지난 시간에 담화의 요건 중 ‘응결성’에 대해 배웠습니다."),
                       Pa("p1", "오늘 저는 이러한 정보성에 대해 조사한 내용을 발표하겠습니다.")], "해설지",
      "1문단에서 지난 시간에 함께 배운 응결성을 떠올리게 한 뒤, 정보성에 대해 발표하겠다고 화제를 밝힌다.",
      "청중과 함께 공유한 경험을 환기하고 있고"),
    J(2, "반영", False, [Pa("p2", "정보성이란 담화의 내용이 수용자에게 정보로서의 가치가 있어야 함을 뜻합니다."),
                       Pa("p2", "따라서 화자는 효과적인 의사소통을 위해 청자가 이미 인식하고 있는 정보와 새로운 정보를 적절히 배치하여 ㉠담화의 정보성을 조절해야 합니다.")], "해설지",
      "2문단에서 정보성의 개념을 먼저 밝히고, 효과적인 의사소통을 위해 정보성을 조절해야 한다고 필요성을 말한다.",
      "정보성의 정도를 적절히 조절해야 할 필요성을 언급한 것을 확인할 수 있으므로 적절하다"),
    J(3, "반영", False, [Pa("p3", "이때 담화 상황 속에서 청자가 이미 인식하고 있는 것으로 전제된 정보를 ‘구정보’, 청자가 새롭게 알게 될 것이라고 판단되는 정보를 ‘신정보’라 합니다."),
                       Pa("p3", "예를 들어 “누가 강아지를 좋아해?”라는 질문에 대한 답으로 “동생이 강아지를 좋아해.”라고 말할 경우 신정보인 ‘동생’은 주격 조사 ‘이’가 표지로서 결합한 것임을 알 수 있습니다.")], "해설지",
      "3문단에서 정보를 구정보와 신정보로 나누고, 질문과 대답의 예를 들어 두 정보가 문장에서 어떻게 나타나는지 설명한다.",
      "예시를 들어 구정보와 신정보가 문장에서 실현되는 양상을 설명하고 있음을 확인할 수 있으므로 적절하다"),
    J(4, "미반영", True, [Pa("p3", "구정보와 신정보가 주어로 실현될 경우 구정보는 주로 보조사 ‘은/는’이 표지로 결합하고 신정보는 주격 조사 ‘이/가’가 표지로 결합하는 경우가 많습니다."),
                        Pa("p3", "이때 같은 질문에 대해 “강아지.”라고 답한다면 구정보인 ‘동생’과 ‘좋아해’를 생략함으로써 목적어에 나타난 신정보인 ‘강아지’에 초점을 맞춰 담화의 응결성을 높일 수도 있습니다.")], "해설지",
      "구정보와 신정보에 붙는 조사와 구정보를 생략한 예는 나오지만, 특징을 나열하고 각각의 정보를 생략했을 때의 장점을 분석해 강조하지는 않는다.",
      "그 특징을 나열하거나 각각의 정보를 생략했을 때의 장점을 분석해 언급한 부분은 확인할 수 없으므로 적절하지 않다"),
    J(5, "반영", False, [Pa("p4", "지금까지 담화의 정보성에 대해 구정보와 신정보의 측면으로 나누어 살펴보았습니다."),
                       Pa("p4", "청자를 배려하며 원활하게 소통하는 사람이 되기를 바랍니다.")], "해설지",
      "4문단에서 살펴본 내용을 정리한 다음, 청자를 배려하며 소통하는 사람이 되기를 바란다고 말한다.",
      "청중에게 기대하는 바를 언급하며 발표를 마무리하고 있음을 확인할 수 있으므로 적절하다"),
]

Q[3]["answer"] = 2
Q[3]["judgments"] = [
    J(1, "적절", False, [Bo("안녕, 너 점심은 먹고 왔어?"), Bo("응, 나 먹고 왔어.")], "해설지",
      "‘점심’은 앞의 질문에 이미 나온 구정보이다. ⓐ는 ‘먹고’의 목적어인 ‘점심을’을 빼고 대답한다.",
      "ⓐ는 구정보가 포함된 목적어 ‘점심을’을 생략하고 있으므로 적절하다"),
    J(2, "부적절", True, [Bo("시간이 없어서 점심을 못 먹고 올 줄 알았는데 다행히 먹고 왔네?"), Bo("어머니께서 데려다주셔서 점심은 먹고 왔지.")], "해설지",
      "ⓑ의 ‘점심은’은 이미 나온 정보를 생략하지 않고 보조사 ‘은’을 붙인 말이지만, ‘먹고’의 대상이 되는 목적어이다. 주어로 제시한 것이 아니다.",
      "ⓑ는 구정보인 ‘점심’을 생략하지 않고 보조사 ‘은’을 표지로 사용하여 목적어로 제시하고 있으므로 적절하지 않다"),
    J(3, "적절", False, [Bo("그런데 오늘 보자고 한 이유가 뭐야?"), Bo("시계가 멈춰서 부탁하려고.")], "해설지",
      "만나자고 한 이유를 묻는 말에 ‘시계가’라는 새 정보가 나온다. 격 조사 ‘가’가 붙은 이 말은 ‘멈춰서’의 주어이다.",
      "ⓒ는 격 조사 ‘가’를 결합하여 신정보 ‘시계’를 주어로 제시하고 있으므로 적절하다"),
    J(4, "적절", False, [Bo("시침 좀 한번 볼래?"), Bo("많이 휘어진 것 같아.")], "해설지",
      "휘어진 것은 바로 앞에서 말한 ‘시침’이다. ⓓ는 청자가 이미 알고 있는 이 주어를 드러내지 않는다.",
      "ⓓ는 구정보인 ‘시침’을 주어로 드러내지 않고 생략하였으므로 적절하다"),
    J(5, "적절", False, [Bo("그럼 어디에 가서 고쳐야 할까?"), Bo("학교 앞 수리점에 가서 고치면 될 거야.")], "해설지",
      "‘어디에’라고 물은 데 대한 새 정보가 ‘학교 앞 수리점에’라는 부사어에 담겨 있다.",
      "ⓔ는 부사어 ‘수리점에’에서 신정보를 제시하고 있으므로 적절하다"),
]

json.dump(d, open(HERE + r"\세트_1-3.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok")
