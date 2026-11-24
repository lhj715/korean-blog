"""2024-06 고2 43~45번(현대시: (가) 이성복 ｢꽃피는 시절｣, (나) 권정우 ｢저수지｣) 세트 → 세트_43-45.json
초안은 도구/세트_뽑기.py 로 뽑았다(_임시\\초안_43-45.json, 문단시작_43-45.txt). 지문은 raw_passage_lines 에서 다시 짠다. 쪽 그림(문제_16쪽_왼쪽·오른쪽)·texttrace·PDF 선으로 확인한 것:
- (가) 21행을 3행씩 7연(연 사이 빈 줄), 출처 줄 note. (나) 15행: 2행 / 4행 / 4행 / 3행 / 3행 5연, 출처 줄 note. (가)(나) 소제목은 label(굵음).
- 밑줄(PDF 선, 마크 뒤 그 행 끝까지): ㉠ 누군가의 입가에서 잔잔한 웃음이 되려 하셨지요 / ㉡ 당신은 나를 알지 못하고 / ㉢ 나는 울고 싶고, 웃고 싶고, 토하고 싶고 /
  ㉣ 부서지고 무너지며 당신을 보낼 일 아득합니다 / ㉤ 조막만 한 손으로 뻣센 내 가슴 쥐어뜯으며 발 구르는 당신. 발문 '않은' 밑줄: 44·45번.
- 굵은 글씨(texttrace type 0+1, 쪽 그림 확인; 45번 선지가 인용하는 말): (가) 추운 땅속을 헤매다 / 부르지 않아도 / 내 안(둘 중 첫 번째, 7행) / 뱉아 / 굳은 살가죽에 불 댕길 일.
  (나) 자기 안 / 모난 돌멩이 / 모난 파문 / 검은 돌멩이 / 검은 파문으로 / 들어가 / 하늘 / 넘치지 않. 선지·<보기>·발문에는 굵은 글씨 없음.
- 44번 발문의 '나'·'당신' 은 네모 테두리(stem_boxed). 45번 ⑤ 뒤 '＊확인 사항' 상자는 문항이 아니어서 뗌. 45번 선지는 쪽 그림대로 '에서 ‘' 띄어 씀.
- 해설지: 43번 ⑤ 정답 + 오답풀이 ①~④, 44번 ② 정답 + ①③④⑤, 45번 ① 정답 + ②~⑤ (모두 해설지 있음).
"""
import json
import re

HERE = r"D:\Work\블로그\리딩맵\작업\20240604-go2"
d = json.load(open(HERE + r"\_임시\초안_43-45.json", encoding="utf-8"))
R = [l.strip() for l in d.pop("raw_passage_lines")]
assert R[0] == "(가)" and R[22].startswith("- 이성복") and R[23] == "(나)" and R[40].startswith("- 권정우") and len(R) == 41


def stanzas(a, sizes):
    out, i = [], a
    for n in sizes:
        out.append("\n".join(R[i:i + n]))
        i += n
    return "\n\n".join(out), i


v1, e1 = stanzas(1, [3] * 7)
v2, e2 = stanzas(24, [2, 4, 4, 3, 3])
assert e1 == 22 and e2 == 40 and v2.endswith("바닥이 깊고도\n높다")
d["passage"] = [
    {"id": "l1", "type": "label", "text": "(가)", "underlines": [], "bold": ["(가)"]},
    {"id": "v1", "type": "verse", "text": v1,
     "underlines": [{"mark": "㉠", "text": "누군가의 입가에서 잔잔한 웃음이 되려 하셨지요"},
                    {"mark": "㉡", "text": "당신은 나를 알지 못하고"},
                    {"mark": "㉢", "text": "나는 울고 싶고, 웃고 싶고, 토하고 싶고"},
                    {"mark": "㉣", "text": "부서지고 무너지며 당신을 보낼 일 아득합니다"},
                    {"mark": "㉤", "text": "조막만 한 손으로 뻣센 내 가슴 쥐어뜯으며 발 구르는 당신"}],
     "bold": ["추운 땅속을 헤매다", "부르지 않아도", {"text": "내 안", "nth": 1}, "뱉아", "굳은 살가죽에 불 댕길 일"]},
    {"id": "n1", "type": "note", "text": R[22], "underlines": []},
    {"id": "l2", "type": "label", "text": "(나)", "underlines": [], "bold": ["(나)"]},
    {"id": "v2", "type": "verse", "text": v2, "underlines": [],
     "bold": ["자기 안", "모난 돌멩이", "모난 파문", "검은 돌멩이", "검은 파문으로", "들어가", "하늘", "넘치지 않"]},
    {"id": "n2", "type": "note", "text": R[40], "underlines": []},
]
P = {p["id"]: p for p in d["passage"]}
for _p in d["passage"]:
    for _b in _p.get("bold", []):
        _s = _b if isinstance(_b, str) else _b["text"]
        assert _s in _p["text"], _s
    for u in _p["underlines"]:
        assert u["text"] in _p["text"]
d["ranges"] = []
d["guide"] = "[43 ~ 45] 다음 글을 읽고 물음에 답하시오."
d["meta"] = {"exam": "2024학년도 6월 고2 전국연합학력평가 국어", "exam_id": "20240604-go2", "area": "문학(현대시)",
             "topic": "(가) 이성복 ｢꽃피는 시절｣ / (나) 권정우 ｢저수지｣",
             "problem_pdf": "20240604-go2-problem-kor_mun_22484VF6.pdf",
             "explanation_pdf": "20240604-go2-explanation-kor_hsj_K5T5L1W7.pdf"}

Q = {x["no"]: x for x in d["questions"]}
Q[44]["stem_underlines"] = ["않은"]
Q[45]["stem_underlines"] = ["않은"]
Q[44]["stem"] = Q[44]["stem"].replace("㉠~ ㉤", "㉠~㉤")
Q[44]["stem_boxed"] = ["나", "당신"]
c5 = Q[45]["choices"]
assert "확인" in c5[4] and c5[4].count("＊") + c5[4].count("*") <= 1
for k in ("＊확인 사항", "* 확인 사항"):
    if k in c5[4]:
        c5[4] = c5[4][: c5[4].index(k)].strip()
assert c5[4].endswith("있군."), c5[4]
for k, t in enumerate(c5):
    c5[k] = t.replace("에서저수지가", "에서 저수지가").replace("에서‘", "에서 ‘").replace("에서는‘", "에서는 ‘")
s = Q[45]["stem"]
i = s.index("<보 기>")
Q[45]["stem"] = s[:i].replace("[3점]", "").strip()
BG45 = s[i + len("<보 기>"):].strip()
assert BG45.startswith("(가)와 (나)는 모두")
Q[45]["bogi"] = {"label": "보 기", "paras": [BG45]}
for q in d["questions"]:
    assert len(q["choices"]) == 5 and q["stem"]

expl = open(HERE + r"\해설_글자.txt", encoding="utf-8").read()
base = expl.index("[43~45]")


def section(no):
    m = re.compile(rf"\n\s*{no}\.?\s*\[출제의도\]").search(expl, base)
    nm = re.compile(rf"\n\s*{no + 1}\.?\s*\[출제의도\]").search(expl, m.end()) if no != 45 else None
    return expl[m.start(): nm.start() if nm else len(expl)]


def X(no, a, b):
    sec = section(no)
    keep = [(i, c) for i, c in enumerate(sec) if not c.isspace()]
    comp = "".join(c for _, c in keep)
    ca, cb = re.sub(r"\s+", "", a), re.sub(r"\s+", "", b)
    ia = comp.index(ca)
    ib = comp.index(cb, ia) + len(cb)
    return sec[keep[ia][0]: keep[ib - 1][0] + 1].replace("\n", "")


def sq(t):
    return "".join(t.split())


def J(choice, verdict, ans, ev, reason, xq=None, bogi=None):
    out = {"choice": choice, "verdict": verdict, "is_answer": ans, "basis": "해설지" if xq else "자체", "reason": reason, "evidence": []}
    for pid, qt in ev:
        if pid == "bogi":
            assert sq(qt) in sq(bogi), qt
            out["evidence"].append({"source": "bogi", "para": None, "quote": qt})
        else:
            assert sq(qt) in sq(P[pid]["text"]), (choice, pid, qt)
            out["evidence"].append({"source": "passage", "para": pid, "quote": qt})
    if xq:
        out["explanation_quote"] = xq
    return out


# ---------- 43번 (적절한 것)
Q[43]["answer"] = 5
Q[43]["judgments"] = [
    J(1, "부적절", False, [("v1", "쥐어뜯으며 발 구르는 당신"), ("v2", "바닥이 깊고도")],
      "(가)는 명사 ‘당신’으로 끝나지만 (나)는 ‘높다’로 끝나 명사로 마무리하지 않는다.",
      X(43, "① (가)는 명사로", "그렇지 않다.")),
    J(2, "부적절", False, [("v1", "부르지 않아도 당신은 옵니다"), ("v2", "자기 안에 발 담그는 것들을")],
      "(가)는 ‘당신’을 청자로 두지만 (나)에는 구체적인 청자가 없다.",
      X(43, "② (가)는 ‘당신’을", "그렇지 않다.")),
    J(3, "부적절", False, [("v1", "나는 당신을 어떻게 보내드려야 할지 모르겠습니다"), ("v2", "하늘이 들어와도 넘치지 않는다")],
      "(가), (나) 모두 말뜻과 반대로 말하는 반어적 표현을 쓰지 않았다.",
      X(43, "③ (가), (나) 모두 반어적", "않았다.")),
    J(4, "부적절", False, [("v1", "당신이 올 때면 먼발치 마른 흙더미도 고개를 듭니다"), ("v2", "바닥이 깊고도")],
      "(가), (나) 모두 아래로 내려가는 하강적 이미지를 쓰지 않았다.",
      X(43, "④ (가), (나) 모두 하강적", "않았다.")),
    J(5, "적절", True, [("v1", "나는 울고 싶고, 웃고 싶고, 토하고 싶고"), ("v1", "부서지고 무너지며 당신을 보낼 일 아득합니다"),
                      ("v2", "모난 파문으로 대답하지 않는다"), ("v2", "검은 파문으로 대답하지 않는다")],
      "(가)는 ‘-고 싶고’와 ‘-ㄹ 일 -ㅂ니다’를, (나)는 ‘라고~ 대답하지 않는다’를 되풀이해 시적 상황을 강조한다.",
      X(43, "(가)는 ‘-고 싶고’", "강조하고 있다.")),
]

# ---------- 44번 (적절하지 않은 것)
Q[44]["answer"] = 2
Q[44]["judgments"] = [
    J(1, "적절", False, [("v1", "누군가의 입가에서 잔잔한 웃음이 되려 하셨지요")],
      "‘잔잔한 웃음이 되려 하셨’다는 표현에서 ‘나’가 ‘당신’을 긍정적으로 인식함이 드러난다.",
      X(44, "① ‘나’가 ‘당신’에 대해", "드러난다.")),
    J(2, "부적절", True, [("v1", "당신은 나를 알지 못하고")],
      "‘당신’이 ‘나’를 알지 못하는 상황은 나오지만 이에 대한 ‘당신’의 인식이나 안타까움은 드러나지 않는다.",
      X(44, "‘당신’이 ‘나’를 인지하지", "않는다.")),
    J(3, "적절", False, [("v1", "나는 울고 싶고, 웃고 싶고, 토하고 싶고")],
      "울고 싶고 웃고 싶고 토하고 싶다는 것은 ‘당신’을 보낼 때 ‘나’가 느낄 다양한 심정이다.",
      X(44, "③ ‘울고 싶고", "표현한 것이다.")),
    J(4, "적절", False, [("v1", "부서지고 무너지며 당신을 보낼 일 아득합니다")],
      "‘당신을 보낼 일 아득’하다는 것은 ‘나’의 막연한 마음을 표현한 것이다.",
      X(44, "④ ‘당신을 보낼 일", "표현한 것이다.")),
    J(5, "적절", False, [("v1", "조막만 한 손으로 뻣센 내 가슴 쥐어뜯으며 발 구르는 당신"), ("v1", "나를 벗고 싶어 몸부림하지만")],
      "‘내 가슴 쥐어뜯으며 발 구르는’ 모습은 ‘당신’이 ‘나’를 벗어나려고 애쓰는 모습이다.",
      X(44, "⑤ ‘당신’이 ‘내 가슴", "모습이다.")),
]

# ---------- 45번 (적절하지 않은 것)
Q[45]["answer"] = 1
Q[45]["judgments"] = [
    J(1, "부적절", True, [("v1", "귀먹고 눈먼 당신은 추운 땅속을 헤매다"), ("v1", "부르지 않아도 당신은 옵니다")],
      "‘추운 땅속을 헤매다’가 ‘부르지 않아도’ 오는 것은 자연의 섭리 때문이며 이 행위에 희생은 드러나지 않는다.",
      X(45, "‘추운 땅속을 헤매다’가", "드러나지 않는다."), BG45),
    J(2, "적절", False, [("v1", "굳은 살가죽에 불 댕길 일 막막합니다")],
      "‘굳은 살가죽에 불 댕길 일’은 꽃을 피울 때 ‘나’가 느낄 고통을 표현한 것이다.",
      X(45, "② ‘굳은 살가죽에", "표현한 것이다."), BG45),
    J(3, "적절", False, [("v2", "모난 돌멩이라고"), ("v2", "모난 파문으로 대답하지 않는다"), ("v2", "검은 파문으로 대답하지 않는다")],
      "‘모난’과 ‘검은’은 돌멩이가 상처를 주는 존재임을 드러내며, 저수지가 이에 파문으로 대답하지 않는 것은 상처를 준 존재마저 품는 모습이다.",
      X(45, "③ ‘모난’이나 ‘검은’은", "품는 모습이다."), BG45),
    J(4, "적절", False, [("v2", "하늘이 들어와도 넘치지 않는다")],
      "저수지 안에 하늘이 들어와도 넘치지 않는다는 것은 저수지의 넓은 포용력을 표현한 것이다.",
      X(45, "④ 저수지 안에", "표현한 것이다."), BG45),
    J(5, "적절", False, [("v1", "절편보다 희고 고운 당신을 잎잎이, 뱉아낼 테지만"), ("v2", "자기 안에 발 담그는 것들을"), ("v2", "겹쳐서 들어가도")],
      "(가)의 ‘내 안’에 있던 것이 밖으로 나오는 과정에서 인고와 희생을, (나)의 저수지 ‘안’으로 존재들이 ‘들어가’는 모습에서 포용을 파악할 수 있다.",
      X(45, "⑤ (가)의 ‘내 안’에", "파악할 수 있다."), BG45),
]
for x in d["questions"]:
    assert len(x["choices"]) == 5 and len(x["judgments"]) == 5

json.dump(d, open(HERE + r"\세트_43-45.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok")
