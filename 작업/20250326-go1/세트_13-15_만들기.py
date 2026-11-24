"""2025-03 고1 13~15번 세트(문법 단독 문항 묶음, 안내문 없음) → 세트_13-15.json
초안: 도구/세트_뽑기.py (_임시\초안_13-15.json). 쪽 그림(문제_5쪽, 왼쪽·오른쪽)과 PDF 좌표로 확인한 것:
- guide null, passage []. 13·14·15번 발문 '않은' 밑줄(PDF 선).
- 13번 <보기>: 문단 둘(들여쓰기 x 115.0 / 104.9) + 표(벡터 선, 쪽에서 잘라 그림). 표 머리 «단어»·«의미 자질» 은 type=1 이지만 그림 안.
- 14번 <보기>: 소개 문단 하나 + ㄱ~ㅁ 예문 다섯 줄(상자 안 상자 없음). 밑줄: 자기·저·저희·당신·스스로(PDF 선 5개).
- 15번 <보기>: «선생님» 굵음(type=1 + 확대 그림 확인, 콜론은 보통). 순서도(래스터, 텍스트층에 글자 없음 → pdf_text "" + raster_text),
  그 아래 <사이시옷을 표기하는 조건> 상자(테두리는 래스터, 글자는 텍스트층; 제목 가운데), «￭학습 과제»(type=1, 콜론 보통),
  안쪽 상자(PDF 선 사각형)의 예문 다섯 줄은 a~e 빈칸 밑줄 위 글자라 blank. 굵은 글씨는 이것뿐.
- 15번 순서도 그림은 쪽 오른쪽 단의 첫 번째 래스터(447.7,288.6~744.4,369.3).
"""
import json
import re

HERE = r"D:\Work\블로그\리딩맵\작업\20250326-go1"
d = json.load(open(HERE + r"\_임시\초안_13-15.json", encoding="utf-8"))
d.pop("raw_passage_lines", None)
d["meta"] = {"exam": "2025년 3월 고1 전국연합학력평가 국어", "exam_id": "20250326-go1", "area": "문법",
             "topic": "의미 자질·재귀 대명사·사이시옷 표기",
             "problem_pdf": "20250326-go1-problem-kor_mun_55A7H57F.pdf",
             "explanation_pdf": "20250326-go1-explanation-kor_hsj_1V99HKS3.pdf"}
d["guide"] = None
d["passage"] = []
Q = {q["no"]: q for q in d["questions"]}

expl = open(HERE + r"\해설_글자.txt", encoding="utf-8").read()


def section(no):
    i = re.search(rf"\n{no}\. \[", expl).start()
    j = re.search(rf"\n{no + 1}\. \[", expl[i + 1:]).start() + i + 1
    lines = [l for l in expl[i:j].split("\n") if not re.fullmatch(r"=== 해설 \d+쪽 ===|\d+|고[123]", l.strip())]
    return "\n".join(lines)


def X(no, a, b):
    sec = section(no)
    keep = [(i, c) for i, c in enumerate(sec) if not c.isspace()]
    comp = "".join(c for _, c in keep)
    ca, cb = re.sub(r"\s+", "", a), re.sub(r"\s+", "", b)
    ia = comp.index(ca)
    ib = comp.index(cb, ia) + len(cb)
    return sec[keep[ia][0]: keep[ib - 1][0] + 1].replace("\n", "")


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


def body_of(q):
    s = q["stem"]
    i = s.index("< 보 기 >")
    q["stem"] = s[:i].replace("[3점]", "").strip()
    return s[i + len("< 보 기 >"):].strip()


# ================= 13번
B = body_of(Q[13])
assert Q[13]["stem"] == "<보기>에서 제시된 단어의 의미 자질을 분석한 결과로 적절하지 않은 것은?"
Q[13]["stem_underlines"] = ["않은"]
i1 = B.index("상하 관계에서")
i2 = B.index("단어의미 자질")
P1, P2, FT = B[:i1].strip(), B[i1:i2].strip(), B[i2:].strip()
assert P1.endswith("가능하다.") and P2.endswith("동일하다.")
assert FT == "단어의미 자질사람[+인간]여자[+인간], [+여성]숙녀[+인간], [+여성], [+성숙]신사[+인간], [-여성], [+성숙]소녀[+인간], [+여성], [-성인]", FT
Q[13]["bogi"] = {"label": "보 기", "blocks": [
    {"id": "b1", "type": "para", "text": P1, "underlines": []},
    {"id": "b2", "type": "para", "text": P2, "underlines": []},
    {"id": "f13", "type": "figure", "caption": "", "image": "그림_13-15_13_표.png", "pdf_text": FT,
     "alt": "단어와 의미 자질 표. 사람: [+인간]. 여자: [+인간], [+여성]. 숙녀: [+인간], [+여성], [+성숙]. 신사: [+인간], [-여성], [+성숙]. 소녀: [+인간], [+여성], [-성인]."}]}
Q[13]["answer"] = 5
SANG = "상하 관계에서 하의어는 상의어보다 구체적인 의미를 가지므로, 상의어의 의미 자질을 모두 가지며 상의어보다 의미 자질이 하나 이상 많다."
BAN = "반의 관계에 있는 단어들은 하나의 의미 자질만 대립되고 나머지 의미 자질은 동일하다."
Q[13]["judgments"] = [
    J(1, "적절", False, [("bogi", SANG), ("fig", "f13", "사람[+인간]"), ("fig", "f13", "숙녀[+인간], [+여성], [+성숙]")], "해설지",
      "‘사람’의 의미 자질 [+인간]은 ‘숙녀’의 의미 자질에 모두 들어 있고, ‘숙녀’가 두 개 더 많으므로 ‘사람’은 상의어이다.",
      X(13, "‘사람’의 의미 자질은 ‘숙녀’", "‘숙녀’의 상의어이다.")),
    J(2, "적절", False, [("fig", "f13", "여자[+인간], [+여성]"), ("fig", "f13", "사람[+인간]")], "해설지",
      "‘여자’는 ‘사람’의 의미 자질 [+인간]에 [+여성]을 더 가지므로 하의어이다.",
      X(13, "‘여자’의 의미 자질은 ‘사람’의 의미 자질을 포함하고", "‘사람’의 하의어이다.")),
    J(3, "적절", False, [("fig", "f13", "소녀[+인간], [+여성], [-성인]"), ("fig", "f13", "여자[+인간], [+여성]")], "해설지",
      "‘소녀’는 ‘여자’의 의미 자질에 [-성인]을 더 가지므로 하의어이고, 의미 자질의 개수도 더 많다.",
      X(13, "‘소녀’의 의미 자질은 ‘여자’의 의미 자질을 포함하고", "구체적인 의미를 가진다.")),
    J(4, "적절", False, [("bogi", BAN), ("fig", "f13", "신사[+인간], [-여성], [+성숙]")], "해설지",
      "‘신사’는 [-여성], ‘숙녀’는 [+여성]만 다르고 나머지 의미 자질이 같으므로 반의 관계이다.",
      X(13, "[-여성]을 가진 ‘신사’와", "반의 관계에 있다.")),
    J(5, "부적절", True, [("bogi", SANG), ("fig", "f13", "소녀[+인간], [+여성], [-성인]")], "해설지",
      "‘소녀’와 ‘사람’은 두 의미 자질이 대립해서가 아니라, ‘소녀’가 ‘사람’의 의미 자질을 포함하고 [+여성]과 [-성인]을 더 가지기 때문에 상하 관계이다.",
      X(13, "‘소녀’와 ‘사람’은 상하 관계에 있는데", "더 갖고 있기 때문이다.")),
]

# ================= 14번
B = body_of(Q[14])
assert Q[14]["stem"] == "<보기>의 밑줄 친 단어에 대한 설명으로 적절하지 않은 것은?"
Q[14]["stem_underlines"] = ["않은"]
k = B.index("ㄱ. ")
INTRO = B[:k].strip()
assert INTRO.endswith("쓰이기도 한다.")
parts = re.split(r"(?=ㄱ\. |ㄴ\. |ㄷ\. |ㄹ\. |ㅁ\. )", B[k:])
parts = [p.strip() for p in parts if p.strip()]
assert len(parts) == 5, parts
ULW = ["자기", "저", "저희", "당신", "스스로"]
blocks = [{"id": "b1", "type": "para", "text": INTRO, "underlines": []}]
for n, (t, w) in enumerate(zip(parts, ULW)):
    assert w in t
    blocks.append({"id": f"b{n + 2}", "type": "para", "text": t, "underlines": [{"mark": "", "text": w}]})
Q[14]["bogi"] = {"label": "보 기", "blocks": blocks}
Q[14]["answer"] = 1
Q[14]["judgments"] = [
    J(1, "부적절", True, [("bogi", parts[0])], "해설지",
      "ㄱ의 ‘자기’는 문장의 의미상 ‘동생’이 아니라 ‘정우’를 나타내는 재귀 대명사이다.",
      X(14, "ㄱ의 ‘자기’는", "나타내고 있다.")),
    J(2, "적절", False, [("bogi", parts[1])], "해설지",
      "ㄴ의 ‘저’는 ‘엄마’가 아니라 주어 ‘막내’를 나타내는 재귀 대명사이다.",
      X(14, "‘저’는 ‘엄마’가 아니라", "재귀 대명사이다.")),
    J(3, "적절", False, [("bogi", parts[2])], "해설지",
      "ㄷ의 ‘저희’는 ‘선생님’이 아니라 ‘아이들’을 나타내는 재귀 대명사이다.",
      X(14, "‘저희’는 ‘선생님’이 아니라", "재귀 대명사이다.")),
    J(4, "적절", False, [("bogi", parts[3])], "해설지",
      "ㄹ의 ‘당신’은 ‘손님’이 아니라 ‘할머니’를 나타내는 재귀 대명사이다.",
      X(14, "‘당신’은 ‘손님’이 아니라", "재귀 대명사이다.")),
    J(5, "적절", False, [("bogi", "한편 명사 ‘스스로’, ‘서로’는 재귀 대명사처럼 쓰이기도 한다."), ("bogi", parts[4])], "해설지",
      "ㅁ의 ‘스스로’는 ‘신입생’이 아니라 ‘선배들’을 나타내는 재귀 대명사처럼 쓰인다.",
      X(14, "‘스스로’는 ‘신입생’이 아니라", "쓰이고 있다.")),
]

# ================= 15번
B = body_of(Q[15])
assert Q[15]["stem"] == "<보기>의 선생님이 제시한 ‘학습 과제’를 탐구한 내용으로 적절하지 않은 것은?", Q[15]["stem"]
Q[15]["points"] = 3
Q[15]["stem_underlines"] = ["않은"]
a = B.index("<사이시옷을 표기하는 조건>")
b = B.index("ㄱ. B의")
c = B.index("￭학습 과제")
e0 = B.index("◦비+")
TALK = B[:a].strip()
assert TALK.startswith("선생님: 고유어") and TALK.endswith("탐구해 봅시다.")
TITLE = B[a:b].strip()
conds = [x.strip() for x in re.split(r"(?=ㄴ\. A의 종성에 |ㄷ\. A의 종성과)", B[b:c]) if x.strip()]
assert len(conds) == 3, conds
TASK = B[c:e0].strip()
assert TASK == "￭학습 과제: a ~ e에 들어갈 올바른 표기를 탐구해 보자.", TASK
items = [x.strip() for x in re.split(r"(?=◦)", B[e0:]) if x.strip()]
assert len(items) == 5, items
FLOW_RT = "A + B ㄱ~ㄷ 중 하나의 음운 변동이 일어나는가? 예 아니요 A + ㅅ + B A + B"
bl = [{"id": "b1", "type": "para", "dialogue": True, "text": TALK, "bold": ["선생님"], "underlines": []},
      {"id": "f15", "type": "figure", "caption": "", "image": "그림_13-15_15_흐름도.png", "pdf_text": "", "raster_text": FLOW_RT,
       "alt": "순서도. A와 B를 더한 뒤 «ㄱ~ㄷ 중 하나의 음운 변동이 일어나는가?» 를 묻는다. «예» 이면 A+ㅅ+B, «아니요» 이면 A+B."},
      {"id": "b2", "type": "para", "text": TITLE, "inbox": "조건", "center": True, "underlines": []}]
for n, t in enumerate(conds):
    bl.append({"id": f"b{n + 3}", "type": "para", "text": t, "inbox": "조건", "underlines": []})
bl.append({"id": "b6", "type": "para", "text": TASK, "bold": ["￭학습 과제"], "underlines": []})
for n, (t, ch) in enumerate(zip(items, "abcde")):
    bl.append({"id": f"b{n + 7}", "type": "para", "text": t, "inbox": "과제", "blank": ch, "underlines": []})
Q[15]["bogi"] = {"label": "보 기", "blocks": bl}
Q[15]["answer"] = 2
Q[15]["judgments"] = [
    J(1, "적절", False, [("bogi", conds[0]), ("bogi", items[0])], "해설지",
      "‘길’의 초성이 [길]에서 [낄]로 예사소리에서 된소리로 바뀌므로 a는 ㄱ에 해당하고 ‘빗길’로 적는다.",
      X(15, "‘비’와 ‘길’이 합쳐진 단어의 발음은", "‘빗길’이라고 표기하는 것은 적절하다.")),
    J(2, "부적절", True, [("bogi", conds[0]), ("bogi", items[1])], "해설지",
      "‘쪽’의 초성은 합쳐지기 전에도 합쳐진 뒤에도 된소리 ‘ㅉ’이라 ㄱ~ㄷ 중 어떤 음운 변동도 일어나지 않으므로 ‘윗쪽’ 표기는 적절하지 않다.",
      X(15, "학습 과제에 제시된 대로, ‘위’와 ‘쪽’이", "‘윗쪽’이라고 표기하는 것은 적절하지 않다.")),
    J(3, "적절", False, [("bogi", conds[1]), ("bogi", items[2])], "해설지",
      "‘코’가 [콘]으로 발음되어 A의 종성에 ‘ㄴ’이 생기므로 c는 ㄴ에 해당하고 ‘콧날’로 적는다.",
      X(15, "‘코’와 ‘날’이 합쳐진 단어의 발음은", "‘콧날’이라고 표기하는 것은 적절하다.")),
    J(4, "적절", False, [("bogi", conds[1]), ("bogi", items[3])], "해설지",
      "‘이’가 [인]으로 발음되어 A의 종성에 ‘ㄴ’이 생기므로 d는 ㄴ에 해당하고 ‘잇몸’으로 적는다.",
      X(15, "‘이’와 ‘몸’이 합쳐진 단어의 발음은", "‘잇몸’이라고 표기하는 것은 적절하다.")),
    J(5, "적절", False, [("bogi", conds[2]), ("bogi", items[4])], "해설지",
      "‘배’가 [밴]으로, ‘일’이 [닐]로 발음되어 A의 종성과 B의 초성에 각각 ‘ㄴ’이 생기므로 e는 ㄷ에 해당하고 ‘뱃일’로 적는다.",
      X(15, "‘배’와 ‘일’이 합쳐진 단어의 발음은", "‘뱃일’이라고 표기하는 것은 적절하다.")),
]

for q in d["questions"]:
    assert q["stem"] and len(q["choices"]) == 5 and q["answer"]
json.dump(d, open(HERE + r"\세트_13-15.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok")
