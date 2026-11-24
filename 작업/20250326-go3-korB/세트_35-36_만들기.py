"""2025-03 고3 언어와 매체(korB) 35~36번 세트: 초안 + 쪽 그림 확인값 + 해설지 기반 판단 → 세트_35-36.json

확인한 것(2026-11-25, 문제_13쪽.png, PDF 텍스트층·선·글꼴, 400dpi 확대):
- 구성: [35 ~ 36] 안내문 + 글(문단 3개, 모두 들여쓰기로 시작). 글은 네모 상자 안(알려진 화면 한계). 굵은 글씨·밑줄·옛한글 없음.
- 발문 «않은» 밑줄: 35번·36번 모두(PDF 선).
- 36번 <보기>: 굵은 글씨(Haansoft Batang type 0+1, 괄호까지) «[중세 국어의 예]», «[현대 국어의 예]» 두 줄만.
  밑줄 4곳(㉠롱담ᄒ다라, ㉡셜흔세히러시니, ㉢ᄒ던, ㉣오르던)은 줄 가운데 글자라 기호 없는 밑줄(mark "").
  옛한글 PUA 가 든 ㉠ 줄과 ㉢ 줄은 쪽에서 오려 낸 그림(display_image). ㉣ 줄 «*» 는 위첨자 모양이나 글자는 그대로.
  «※ ‘*’은 어법에 맞지 않음을 나타냄.» 는 note.
- 36번 ⑤ 뒤에 37~39번 글자가 딸려 와 잘라 낸다.
"""
import json
import re

HERE = r"D:\Work\블로그\리딩맵\작업\20250326-go3-korB"
d = json.load(open(HERE + r"\_임시\초안_35-36.json", encoding="utf-8"))
d.pop("raw_passage_lines", None)
d["guide"] = "[35 ~ 36] 다음 글을 읽고 물음에 답하시오."
d["range"] = [35, 36]
d["meta"] = {"exam": "2025학년도 3월 고3 전국연합학력평가 국어영역(언어와 매체)", "exam_id": "20250326-go3-korB",
             "area": "문법", "topic": "선어말 어미 ‘-더-’의 변화",
             "problem_pdf": "20250326-go3-problem-korB_mun_79OHAI8N.pdf",
             "explanation_pdf": "20250326-go3-explanation-korB_hsj_YA4UFFZA.pdf"}
Q = {q["no"]: q for q in d["questions"]}
P = {p["id"]: p for p in d["passage"]}
for p in d["passage"]:
    p.setdefault("underlines", [])

# ---- 발문·선지
Q[35]["stem_underlines"] = ["않은"]
Q[36]["stem_underlines"] = ["않은"]
Q[36]["choices"] = Q[36]["choices"][:5]
c5 = Q[36]["choices"][4]
Q[36]["choices"][4] = c5[: c5.index("보여 주는군.") + len("보여 주는군.")]
for q in d["questions"]:
    assert len(q["choices"]) == 5, q["no"]

# ---- 36번 <보기>
s36 = Q[36]["stem"]
bi = s36.index("< 보 기 >")
Q[36]["stem"] = s36[:bi].replace("[3점]", "").strip()
body = s36[bi + len("< 보 기 >"):]
parts = [x for x in re.split(r"(?=㉠ |㉡ |㉢ |㉣ |\(태자|\(부처|\(내가|\[현대 국어의 예\]|※)", body) if x]
H1 = "[중세 국어의 예]"
assert len(parts) == 10, parts
assert parts[0] == H1, parts[0]
assert parts[1].startswith("㉠ ") and parts[2].startswith("(태자") and parts[3].startswith("㉡ ")
assert parts[4].startswith("(부처") and parts[5].startswith("㉢ ") and parts[6].startswith("(내가")
assert parts[7] == "[현대 국어의 예]" and parts[8].startswith("㉣ ") and parts[9].startswith("※"), parts
PUA = "[\ue000-\uf8ff]"
UL36 = {1: "\ue42c담\uf537다라", 3: "셜흔세히러시니", 5: "\uf537던", 8: "오르던"}
blocks = []
for k, t in enumerate(parts):
    b = {"id": f"b{k+1}", "type": "note" if t.startswith("※") else "para", "text": t, "underlines": []}
    if k in UL36:
        assert UL36[k] in t, (k, t)
        b["underlines"] = [{"mark": "", "text": UL36[k]}]
    if t in (H1, "[현대 국어의 예]"):
        b["bold"] = [t]
    blocks.append(b)
blocks[1]["display_image"] = "그림_35-36_36_보기1.png"
blocks[5]["display_image"] = "그림_35-36_36_보기3.png"
for k, b in enumerate(blocks):
    has = bool(re.search(PUA, b["text"]))
    assert has == (k in (1, 5)), (k, b["text"])
Q[36]["bogi"] = {"label": "< 보 기 >", "blocks": blocks}


# ---- 인용 도우미
def pq(pid, start, end):
    t = P[pid]["text"]
    i = t.index(start)
    j = t.index(end, i) + len(end)
    return ("passage", pid, t[i:j])


def bq(q):
    assert any(q in b["text"] for b in blocks), q
    return ("bogi", None, q)


def sq(s):
    return re.sub(r"[\s\u200b]+", "", s)


lines = open(HERE + r"\해설_글자.txt", encoding="utf-8").read().split("\n")
region = lines[900:973]
assert region[0].startswith("35. [출제의도]") and lines[973].startswith("40. [출제의도]"), (region[0], lines[973])
EXPL = sq("\n".join(l for l in region if not re.match(r"^=== 해설 \d+쪽 ===$", l)))
EXPL = EXPL[: EXPL.index(sq("37. [출제의도]"))]


def E(start, end, lead=""):
    s, e = sq(start), sq(end)
    i = EXPL.index(s)
    assert EXPL[i - len(lead): i] == lead, (start, repr(EXPL[i - 3: i]))
    j = EXPL.index(e, i) + len(e)
    return EXPL[i - len(lead): j]


def J(choice, verdict, ans, ev, basis, reason, xq=None):
    out = {"choice": choice, "verdict": verdict, "is_answer": ans, "basis": basis, "reason": reason, "evidence": []}
    for e in ev:
        out["evidence"].append({"source": e[0], "para": e[1], "quote": e[2]})
    if xq:
        out["explanation_quote"] = xq
    return out


# ======== 35번 (정답 ②, 적절하지 않은 것)
Q[35]["answer"] = 2
Q[35]["judgments"] = [
    J(1, "적절", False, [pq("p2", "‘-더-’가 현대 국어의 ‘-더-’와 달리 단순히", "나타낼 뿐")], "해설지",
      "2문단은 중세 국어의 ‘-더-’가 단순히 사건이 과거에 발생한 것임을 나타냈다고 한다. 따라서 중세 국어에서는 과거 시제가 선어말 어미 ‘-더-’로 실현될 수 있었다.",
      E("중세 국어에서 과거 시제는", "실현될 수 있다.", lead="①")),
    J(2, "부적절", True, [pq("p3", "현대 국어에서 ‘-더-’가 표현하는 인식의 시점이", "때문이다."),
                        pq("p1", "즉 현대 국어의 ‘-더-’가 표현하는 과거는", "할 수 있다.")], "해설지",
      "현대 국어의 ‘-더-’가 표현하는 과거는 화자가 사건을 인식한 시점이고, 3문단은 이 인식의 시점이 과거에 국한된다고 한다. 그러므로 화자의 사건 인식 시점이 과거가 아닐 수 있다는 설명은 틀리다.",
      E("현대 국어에서 ‘-더-’가 표현하는 과거는", "적절하지 않다.")),
    J(3, "적절", False, [pq("p3", "중세 국어의 ‘-더-’가 나타냈던 의미가", "유지되고 있다.")], "해설지",
      "3문단은 중세 국어의 ‘-더-’가 나타냈던 의미가 과거 시제 관형사형 어미 ‘-던’에 남아 현대 국어까지 유지된다고 한다. 따라서 관형사절의 과거 시제를 ‘-던’으로 표현할 수 있다.",
      E("현대 국어에서 과거 시제 관형사형", "표현할 수 있다.", lead="③")),
    J(4, "적절", False, [pq("p1", "그러나 감정이나 감각을 표현하는 형용사가", "함께 쓰인다.")], "해설지",
      "‘춥다’는 감각을 표현하는 형용사이다. 서술어가 이런 형용사인 평서문에서는 1인칭 주어가 ‘-더-’와 함께 쓰일 수 있으므로 ‘나는 좀 춥더라.’는 적절한 예이다.",
      E("감각을 표현하는 형용사인", "함께 쓰인다.", lead="④")),
    J(5, "적절", False, [pq("p3", "과거 시제 선어말 어미 ‘-앗-/-엇-’이 근대 국어 시기에 확립되면서", "의미가 바뀌었다.")], "해설지",
      "근대 국어 시기에 과거 시제 선어말 어미 ‘-앗-/-엇-’이 확립되면서 ‘-더-’의 의미가 ‘어떤 사실을 지각을 통해 새로 알게 됨.’으로 바뀌었다. 그래서 현대 국어와 중세 국어에서 ‘-더-’의 의미가 서로 다르다.",
      E("근대 국어 시기에", "바뀌게 되었다.", lead="⑤")),
]

# ======== 36번 (정답 ④, 적절하지 않은 것)
Q[36]["answer"] = 4
Q[36]["judgments"] = [
    J(1, "적절", False, [pq("p1", "그러나 감정이나 감각을 표현하는 형용사가", "함께 쓰인다."),
                       bq("내 \ue42c담\uf537다라")], "해설지",
      "㉠의 ‘내 담다라’는 서술어가 감정이나 감각을 표현하는 형용사인 평서문이 아니다. 그런데도 1인칭 주어가 ‘-더-’와 함께 쓰였다.",
      E("감정이나 감각을 표현하는 형용사가 서술어인 평서문이 아님에도", "함께 쓰였다.")),
    J(2, "적절", False, [pq("p2", "또한 ‘-더-’와 주체 높임 선어말 어미", "차이가 있었다."),
                       bq("셜흔세히러시니")], "해설지",
      "중세 국어에서는 ‘-더-’와 ‘-시-’가 연이어 쓰일 때 ‘-더시-’(‘-러시-’)로 나타났다. ㉡은 이 순서를 보여 주며, ‘-시더-’의 순서로 나타나는 현대 국어와 차이가 있다.",
      E("중세 국어에서는 ‘-더-(-러-)’와", "차이가 있었다.", lead="②")),
    J(3, "적절", False, [pq("p2", "중세 국어의 ‘-더-’는 환경에 따라", "실현되었다."),
                       bq("내 \ue42c담\uf537다라"), bq("셜흔세히러시니")], "해설지",
      "㉠은 ‘-더-’가 ‘-오-’와 결합한 융합형 ‘-다-’로 실현된 것이고, ㉡은 ‘이다’의 ‘이-’ 뒤에서 ‘-러-’로 실현된 것이다. 두 예는 ‘-더-’가 환경에 따라 다양한 형태로 실현되었음을 보여 준다.",
      E("㉠은 ‘-더-’가", "실현된 것이다.", lead="③")),
    J(4, "부적절", True, [pq("p3", "중세 국어의 ‘-더-’가 나타냈던 의미가", "유지되고 있다."),
                        pq("p2", "주어의 인칭과 관련하여", "나타내지 않았다."),
                        bq("내 \uf537던 이리")], "해설지",
      "‘-던’이 쓰인 관형사절은 중세 국어와 현대 국어 모두에서 주어의 인칭과 관련한 현대 국어 ‘-더-’의 특징을 나타내지 않는다. 그러므로 중세 국어의 ‘-던’이 현대 국어의 ‘-던’과 차이가 있었다는 설명은 틀리다.",
      E("중세 국어와 현대 국어 모두에서", "나타내지 않는다.")),
    J(5, "적절", False, [pq("p3", "중세 국어의 ‘-더-’가 나타냈던 의미가", "유지되고 있다."),
                       bq("*내일부터 오르던 버스 요금은 첫차부터 적용된다.")], "해설지",
      "중세 국어의 ‘-더-’는 사건이 과거에 발생한 것임을 나타냈고 이 의미가 현대 국어의 ‘-던’에 남아 있다. 그래서 관형사절에서 미래의 사건에 ‘-던’을 쓸 수 없고, ㉣은 어법에 맞지 않는다.",
      E("중세 국어의 ‘-더-’는 사건이 과거에", "사용할 수 없다.", lead="⑤")),
]
for q in d["questions"]:
    for j in q["judgments"]:
        for e in j["evidence"]:
            if e["source"] == "bogi":
                e["para"] = None

json.dump(d, open(HERE + r"\세트_35-36.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("세트_35-36.json 씀")
