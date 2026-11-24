"""2024-10 고1 13~15번(문법 단독 문항: 높임 표현·시간 표현·중세 국어) 세트: 초안 + 쪽 그림 확인값 + 해설지 기반 판단 → 세트_13-15.json

초안은 도구/세트_뽑기.py 로 뽑았다(_임시\\초안_13-15.json, 인자 «13 15 -»). 쪽 그림(문제_5쪽_왼쪽·오른쪽.png)과 PDF 좌표로 확인한 것:
- 안내문·지문 없음(guide null, passage []). 문항마다 자기 상자가 있다.
- 13번: <보 기> 상자 = ㉠~㉤ 문장 5줄(밑줄 없음). 선지는 ①~⑤ 가 행인 표(문장 | 주체 높임(격조사·특수 어휘·선어말 어미) | 객체 높임(격조사·특수 어휘)):
  표 머리는 머리말 없는 plain 상자에 그림 한 장(그림_13-15_13_표머리.png, 선·글자가 벡터라 쪽에서 잘라 그림으로, 글자는 텍스트층에 있어 pdf_text),
  선지 글은 «㉠ + 전각 공백 + ○✕…» (칸마다 전각 공백 세 개). 발문 밑줄 없음('적절한').
- 14번: <보 기> = 선생님 말(«선생님:» 콜론까지 굵게, type=1) + 안쪽 테두리 상자(◦ 예문 5줄). 밑줄은 ㉠~㉤ 뒤 낱말(살·곧·한다·번졌다·간), 원문자는 밑줄 밖. 발문 밑줄 '않은'.
- 15번: <보 기> = 중세 국어 문단(옛한글 PUA 가 있어 쪽에서 오려 낸 그림 display_image, 문단 안 굵은 낱말 바미·조사·비저·醫員(의원)드려·뜨들은 그림에 들어 있다)
  + «[현대어 풀이]»(굵게) + 현대어 문단. 선지 ①④⑤ 의 옛한글 PUA 글자 3개는 choice_images 로 작은 그림을 낀다.
  발문 밑줄 '않은'.
- 텍스트층 전각 공백(생일　선물 등)은 그림대로 보통 공백으로 바꾼다.
"""
import json
import re

HERE = r"D:\Work\블로그\리딩맵\작업\20241015-go1"
d = json.load(open(HERE + r"\_임시\초안_13-15.json", encoding="utf-8"))
d.pop("raw_passage_lines", None)
d["meta"] = {"exam": "2024학년도 10월 고1 전국연합학력평가", "exam_id": "20241015-go1", "area": "문법",
             "topic": "높임 표현·시간 표현·중세 국어의 특징", "problem_pdf": "20241015-go1-problem-kor_mun_TV4C3674.pdf",
             "explanation_pdf": "20241015-go1-explanation-kor_hsj_M4258A7J.pdf"}
d["guide"] = None
d["passage"] = []
Q = {q["no"]: q for q in d["questions"]}
SP = "\u3000"

expl = open(HERE + r"\해설_글자.txt", encoding="utf-8").read()


def section(no):
    i = expl.index(f"\n{no}. [출제의도]")
    j = expl.index(f"\n{no + 1}. [출제의도]", i)
    return expl[i:j]


def X(no, a, b):
    """해설지 그 문항 해설에서 a 로 시작해 b 로 끝나는 글(줄바꿈만 이어 붙임)."""
    sec = section(no)
    keep = [(i, c) for i, c in enumerate(sec) if not c.isspace()]
    comp = "".join(c for _, c in keep)
    ca, cb = re.sub(r"\s+", "", a), re.sub(r"\s+", "", b)
    ia = comp.index(ca)
    ib = comp.index(cb, ia) + len(cb)
    return sec[keep[ia][0]: keep[ib - 1][0] + 1].replace("\n", "")


def J(choice, verdict, ans, ev, basis, reason, xq=None):
    out = {"choice": choice, "verdict": verdict, "is_answer": ans, "basis": basis, "reason": reason,
           "evidence": [{"source": "bogi", "para": None, "quote": e} for e in ev]}
    if xq:
        out["explanation_quote"] = xq
    return out


# ================= 13번
RAW13 = Q[13]["stem"]
s13 = RAW13.replace("　", " ")
Q[13]["stem"] = s13[: s13.index("것은?") + 3]
body13 = s13[s13.index("보 기") + 3:]
iH = body13.index("문장주체")
H13 = RAW13[RAW13.index("문장주체"):]  # 텍스트층 그대로(전각 공백 포함)
sent13 = [body13[: iH]]
parts = re.split(r"(?=㉠|㉡|㉢|㉣|㉤)", body13[:iH])
parts = [p for p in parts if p]
assert len(parts) == 5, parts
Q[13]["bogi"] = [
    {"label": "보 기", "blocks": [{"id": f"b{k+1}", "type": "para", "text": t, "underlines": []} for k, t in enumerate(parts)]},
    {"label": "", "plain": True, "blocks": [
        {"id": "f13", "type": "figure", "caption": "", "image": "그림_13-15_13_표머리.png", "pdf_text": H13,
         "alt": "표 머리: 문장 / 주체 높임(격조사, 특수 어휘, 선어말 어미) / 객체 높임(격조사, 특수 어휘)."}]},
]
Q[13]["table_border"] = True   # 표 칸 테두리가 밑줄로 읽힘(쪽 그림으로 선지 글자에 밑줄 없음 확인)
marks = "㉠㉡㉢㉣㉤"
for k, c in enumerate(Q[13]["choices"]):
    assert c[0] == marks[k] and len(c) == 6, c
    Q[13]["choices"][k] = c[0] + SP * 3 + (SP * 3).join(c[1:])

# ================= 14번
s14 = Q[14]["stem"]
Q[14]["stem"] = s14[: s14.index("보 기")]
Q[14]["stem_underlines"] = ["않은"]
body14 = s14[s14.index("선생님:"):]
iB = body14.index("◦")
T14 = body14[:iB].strip()
bul = [b.strip() for b in re.split(r"(?=◦)", body14[iB:]) if b.strip()]
assert len(bul) == 5, bul
UL = [("㉠", "살"), ("㉡", "곧"), ("㉢", "한다"), ("㉣", "번졌다"), ("㉤", "간")]
blocks14 = [{"id": "b1", "type": "para", "dialogue": True, "text": T14, "bold": ["선생님:"], "underlines": []}]
for k, (b, (m, u)) in enumerate(zip(bul, UL)):
    assert m in b and u in b, (b, m, u)
    blocks14.append({"id": f"e{k+1}", "type": "para", "text": b, "inbox": "예문", "underlines": [{"mark": m, "text": u}]})
Q[14]["bogi"] = {"label": "보 기", "blocks": blocks14}

# ================= 15번
s15 = Q[15]["stem"]
Q[15]["stem"] = s15[: s15.index("보 기")]
Q[15]["stem_underlines"] = ["않은"]
body15 = s15[s15.index("보 기") + 3:]
iM = body15.index("[현대어 풀이]")
OLD = body15[:iM].strip()
MOD = body15[iM + len("[현대어 풀이]"):].strip()
assert OLD.startswith("解叔謙") and OLD.endswith("니\ue46e대") and MOD.startswith("해 숙겸") and MOD.endswith("말하니까")
Q[15]["bogi"] = {"label": "보 기", "blocks": [
    {"id": "b1", "type": "para", "text": OLD, "underlines": [], "display_image": "그림_13-15_15_보기.png"},
    {"id": "b2", "type": "para", "text": "[현대어 풀이]", "underlines": [], "bold": ["[현대어 풀이]"]},
    {"id": "b3", "type": "para", "text": MOD, "underlines": []},
]}
Q[15]["choice_images"] = {
    "1": [{"text": "\ue57b", "image": "그림_13-15_15_선지1_a.png", "alt": "ᄆᆡ"}],
    "2": [{"text": "틀", "image": "그림_13-15_15_선지2_a.png", "alt": "ᅀᆞ", "plain": True}],
    "4": [{"text": "\ue38a", "image": "그림_13-15_15_선지4_a.png", "alt": "ᄃᆞ"}],
    "5": [{"text": "\ue6d7", "image": "그림_13-15_15_선지5_a.png", "alt": "ᄠᅳ"}],
}
for q in Q.values():
    assert len(q["choices"]) == 5

# ================= 판단
Q[13]["answer"] = 5
S13 = parts
Q[13]["judgments"] = [
    J(1, "부적절", False, [S13[0].strip()], "해설지",
      "㉠은 주체 ‘삼촌’을 높이는 격조사 ‘께서’와 특수 어휘 ‘계시다’를 쓰고 선어말 어미는 쓰지 않았다. 표의 주체 높임 중 격조사만 맞고 특수 어휘와 선어말 어미 칸은 틀렸다.",
      X(13, "㉠은 주체인", "적절하지 않다")),
    J(2, "부적절", False, [S13[1].strip()], "해설지",
      "㉡은 주체 ‘어머니’를 높이는 격조사 ‘께서’와 선어말 어미 ‘-시-’를 쓰고, 객체 높임은 쓰지 않았다. 표의 주체 높임 격조사 칸과 객체 높임 격조사 칸이 틀렸다.",
      X(13, "㉡은 주체인", "적절하지 않다")),
    J(3, "부적절", False, [S13[2].strip()], "해설지",
      "㉢은 객체 ‘할머니’를 높이는 특수 어휘 ‘모시다’를 쓰고, 객체 높임 격조사는 쓰지 않았다. 표의 객체 높임 격조사 칸이 틀렸다.",
      X(13, "㉢은 객체인", "적절하지 않다")),
    J(4, "부적절", False, [S13[3].strip()], "해설지",
      "㉣은 객체 ‘선생님’을 높이는 격조사 ‘께’와 특수 어휘 ‘여쭤보다’를 쓴다. 표는 객체 높임 격조사 칸을 쓰지 않은 것으로 적어 틀렸다.",
      X(13, "㉣은 객체인", "적절하지 않다")),
    J(5, "적절", True, [S13[4].strip()], "해설지",
      "㉤은 주체 ‘할아버지’를 높이는 격조사 ‘께서’와 특수 어휘 ‘주무시다’를 쓰고 선어말 어미와 객체 높임은 쓰지 않았다. 표의 모든 칸이 이와 맞다.",
      X(13, "㉤은 주체인", "또한 객체 높임의 경우 격조사, 특수 어휘 모두 사용하지 않는다는 분석은 적절하다.")),
]

E14 = [b[1:].strip() if b.startswith("◦") else b for b in bul]
Q[14]["answer"] = 5
Q[14]["judgments"] = [
    J(1, "적절", False, [E14[0]], "해설지",
      "㉠ ‘살’은 어간 ‘살-’에 관형사형 어미 ‘-ㄹ’이 결합해 발화시를 기준으로 사건시가 나중인 시제를 나타낸다.",
      X(14, "㉠은 어간", "나타내므로 적절하다")),
    J(2, "적절", False, [E14[1]], "해설지",
      "㉡ ‘곧’은 시간 부사어로, 발화시를 기준으로 사건시가 나중인 시제를 나타낸다.",
      X(14, "㉡은 시간 부사어로", "나타내므로 적절하다")),
    J(3, "적절", False, [E14[2]], "해설지",
      "㉢ ‘한다’는 어간 ‘하-’에 선어말 어미 ‘-ㄴ-’이 결합해 발화시와 사건시가 일치하는 시제를 나타낸다.",
      X(14, "㉢은 어간", "나타내므로 적절하다")),
    J(4, "적절", False, [E14[3]], "해설지",
      "㉣ ‘번졌다’는 어간 ‘번지-’에 선어말 어미 ‘-었-’이 결합해 발화시를 기준으로 사건시가 앞선 시제를 나타낸다.",
      X(14, "㉣은 어간", "나타내므로 적절하다")),
    J(5, "부적절", True, [E14[4]], "해설지",
      "㉤ ‘간’은 어간 ‘가-’에 관형사형 어미 ‘-ㄴ’이 결합해 발화시를 기준으로 사건시가 앞선 시제를 나타낸다. 발화시와 사건시가 일치한다는 말이 틀렸다.",
      X(14, "㉤은 어간", "적절하지 않다")),
]

sec15 = section(15).replace("\n", "")
i1 = sec15.index("[출제의도] 중세 국어의 특징 이해하기") + len("[출제의도] 중세 국어의 특징 이해하기")
XQ1 = sec15[i1: sec15.index("적절하지 않다.", i1) + len("적절하지 않다.")]
assert XQ1.startswith("‘바")
Q[15]["answer"] = 1


def sent15(mark, nxt=None):
    i = sec15.index(mark)
    return sec15[i + len(mark): sec15.index("적절하다.", i) + len("적절하다.")].strip()


Q[15]["judgments"] = [
    J(1, "부적절", True, ["바\ue57b", "밤에 뜰 가운데"], "해설지",
      "‘바’는 체언 ‘밤’에 부사격 조사가 결합한 것으로, 끝음절이 양성 모음인 체언에 양성 모음 조사가 쓰여 모음 조화를 따르고 있다. 따르지 않았다는 말이 틀렸다.",
      XQ1.rstrip(".")),
    J(2, "적절", False, ["조틀 비더니", "머리 조아려"], "해설지",
      "‘조’에는 현대 국어에 없는 글자 ‘ㅿ’이 표기에 쓰였다.",
      sent15("② ").rstrip(".")),
    J(3, "적절", False, ["비저 머그면", "술 빚어 먹으면"], "해설지",
      "‘비저’는 현대 국어에서 ‘빚어’로 끊어 적는 것과 달리 이어 적기를 하였다.",
      sent15("③ ").rstrip(".")),
    J(4, "적절", False, ["醫員(의원)\ue38a려", "의사한테 물으니"], "해설지",
      "‘醫員(의원)’ 뒤에 쓰인 부사격 조사는 현대 국어의 ‘한테’와 형태가 다르다.",
      sent15("④ ").rstrip(".")),
    J(5, "적절", False, ["\ue6d7들", "얻으러 다니는 뜻을"], "해설지",
      "‘뜻을’의 첫 글자는 현대 국어와 달리 어두 자음군이 쓰였다.",
      sent15("⑤ ").rstrip(".")),
]

json.dump(d, open(HERE + r"\세트_13-15.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok")
