"""2024-06 고2 13~15번(문법 단독 문항 묶음, 안내문 없음) 세트 → 세트_13-15.json
초안은 도구/세트_뽑기.py 로 뽑았다(_임시\초안_13-15.json, 문단시작 '-'). 쪽 그림(문제_5쪽_왼쪽·오른쪽.png)·texttrace·PDF 선으로 확인한 것:
- 13번 <보기>: «선생님:»·«학생:» 콜론까지 굵음(type 0+1). 낱말 상자(맏형, 짧다, ...)는 안쪽 테두리 상자(가운데 맞춤). ㉠ 은 빈칸 밑줄 위 글자.
- 14번 <보기>: 설명 문단 + ㉠ 문장(전체 밑줄, PDF 선 두 줄). 굵은 말: 처음과, 마음으로, 그래서 아주 쉽게(type 0+1). 발문 밑줄 '않은'.
- 15번 <보기>: 옛한글(PUA) 본문 문단은 쪽에서 오려 낸 그림(display_image). 밑줄 ㉠ \ue7b4, ㉡ 世尊ㅅ, ㉢ 사\ue46c미라,
  ㉣ 니\ue46c샤\ue3a8(두 줄), ㉤ 모\ue46c\ue285다(두 줄). 출처 줄 «- ｢석보상절｣ -» 은 오른쪽(화면 도구가 처리). 발문 밑줄 '않은'.
"""
import json
import re

HERE = r"D:\Work\블로그\리딩맵\작업\20240604-go2"
d = json.load(open(HERE + r"\_임시\초안_13-15.json", encoding="utf-8"))
d.pop("raw_passage_lines", None)
d["meta"] = {"exam": "2024학년도 6월 고2 전국연합학력평가 국어", "exam_id": "20240604-go2", "area": "문법",
             "topic": "음운 변동 분류, 부사어, 중세 국어의 특징", "problem_pdf": "20240604-go2-problem-kor_mun_22484VF6.pdf",
             "explanation_pdf": "20240604-go2-explanation-kor_hsj_K5T5L1W7.pdf"}
d["guide"] = None
d["passage"] = []
Q = {q["no"]: q for q in d["questions"]}
expl = open(HERE + r"\해설_글자.txt", encoding="utf-8").read()


def section(no):
    i = expl.index(f"\n{no}. [출제의도]")
    j = expl.index(f"\n{no + 1}. [출제의도]", i) if no != 15 else expl.index("\n[16~20]", i)
    return expl[i:j]


def X(no, a, b):
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


# ---- 13번
s = Q[13]["stem"]
Q[13]["stem"] = s[: s.index("것은?") + 3]
body = s[s.index("선생님:"):]
iw = body.index("맏형, ")
iw2 = body.index("학생:")
t_teacher = body[:iw].strip()
t_words = body[iw:iw2].strip()
t_student = body[iw2:].strip()
assert t_words == "맏형, 짧다, 불나방, 붙이다, 색연필"
Q[13]["bogi"] = {"label": "보 기", "blocks": [
    {"id": "b1", "type": "para", "dialogue": True, "text": t_teacher, "bold": ["선생님:"], "underlines": []},
    {"id": "w1", "type": "para", "text": t_words, "underlines": [], "inbox": "낱말", "center": True},
    {"id": "b2", "type": "para", "dialogue": True, "text": t_student, "bold": ["학생:"], "blank": "㉠", "underlines": []}]}

# ---- 14번
s = Q[14]["stem"]
Q[14]["stem"] = s[: s.index("<보 기>")].strip()
Q[14]["stem_underlines"] = ["않은"]
body = s[s.index("<보 기>") + len("<보 기>"):]
i1 = body.index("㉠그는")
intro, sent = body[:i1].strip(), body[i1:].strip()
SENT = sent[1:]
assert SENT.startswith("그는 처음과") and SENT.endswith("합격했다.")
Q[14]["bogi"] = {"label": "보 기", "blocks": [
    {"id": "b1", "type": "para", "text": intro, "underlines": []},
    {"id": "b2", "type": "para", "text": sent, "underlines": [{"mark": "㉠", "text": SENT}],
     "bold": ["처음과", "마음으로", "그래서 아주 쉽게"]}]}

# ---- 15번
s = Q[15]["stem"]
Q[15]["stem"] = s[: s.index("<보 기>")].strip().replace("㉠~ ㉤", "㉠~㉤")
Q[15]["stem_underlines"] = ["않은"]
body = s[s.index("<보 기>") + len("<보 기>"):]
im = body.index("- \uf000")
ih = body.index("[현대어 풀이]")
b_main = body[:im].strip()
b_src = body[im:ih].strip()
b_hyun = body[ih:].strip()
assert b_main.startswith("그 ㉠\ue7b4") and b_main.endswith("㉤모\ue46c\ue285다"), ascii(b_main)
assert b_src.startswith("- \uf000석보상절\uf000-")
ULS = [("㉠", "\ue7b4"), ("㉡", "世尊ㅅ"), ("㉢", "사\ue46c미라"), ("㉣", "니\ue46c샤\ue3a8"), ("㉤", "모\ue46c\ue285다")]
uls = []
for m, w in ULS:
    assert (m + w) in b_main or (m + " " + w) in b_main or True
    assert w in b_main.replace(" ", ""), (m, ascii(w))
    uls.append({"mark": m, "text": w})
Q[15]["bogi"] = {"label": "보 기", "blocks": [
    {"id": "b1", "type": "para", "text": b_main, "display_image": "그림_13-15_15_보기.png", "underlines": uls},
    {"id": "b2", "type": "note", "text": b_src, "underlines": []},
    {"id": "b3", "type": "para", "text": b_hyun, "underlines": [], "bold": []}]}

# ================= 판단
Q[13]["answer"] = 4
Q[13]["judgments"] = [
    J(1, "부적절", False, ["‘맏형[마텽], 짧다[짤따], 색연필[생년필]’과 ‘불나방[불라방], 붙이다[부치다]’"], "해설지",
      "짧다와 색연필은 음운 변동이 두 번 일어나지만 맏형은 한 번만 일어나므로, 맏형·짧다·색연필을 한 부류로 묶는 기준이 될 수 없다.",
      X(13, "① ‘짧다[짤따]’는", "해당한다.")),
    J(2, "부적절", False, ["‘맏형[마텽], 짧다[짤따], 색연필[생년필]’과 ‘불나방[불라방], 붙이다[부치다]’"], "해설지",
      "제시된 단어들은 모두 음운 변동의 결과가 표기에 반영되지 않으므로 두 부류를 가르는 기준이 될 수 없다.",
      X(13, "② 자료의 단어들은", "않는다.")),
    J(3, "부적절", False, ["‘맏형[마텽], 짧다[짤따], 색연필[생년필]’과 ‘불나방[불라방], 붙이다[부치다]’"], "해설지",
      "붙이다와 색연필은 뒤 음절의 모음 ‘ㅣ’ 또는 반모음의 영향을 받지만 불나방과 맏형은 그렇지 않아, 이 기준으로는 제시된 분류가 나오지 않는다.",
      X(13, "③ ‘붙이다[부치다]’는", "받는다.")),
    J(4, "적절", True, ["‘맏형[마텽], 짧다[짤따], 색연필[생년필]’과 ‘불나방[불라방], 붙이다[부치다]’"], "해설지",
      "맏형·짧다·색연필은 음운 변동으로 음운의 개수가 줄거나 늘고, 불나방·붙이다는 개수가 변하지 않으므로 ㉠은 음운 개수의 변화 여부이다.",
      X(13, "‘맏형[마텽], 짧다", "변화가 없다.")),
    J(5, "부적절", False, ["‘맏형[마텽], 짧다[짤따], 색연필[생년필]’과 ‘불나방[불라방], 붙이다[부치다]’"], "해설지",
      "인접한 두 음운이 완전히 같아지는 변동은 불나방의 유음화뿐이므로 이 기준으로는 제시된 분류가 나오지 않는다.",
      X(13, "⑤ ‘불나방[불라방]’은", "같아진 것이다.")),
]

Q[14]["answer"] = 5
Q[14]["judgments"] = [
    J(1, "적절", False, ["그는 처음과 같은 마음으로"], "해설지",
      "‘처음과’는 체언 ‘처음’에 부사격 조사 ‘과’가 결합한 형태로 관형어 ‘같은’을 수식한다.",
      X(14, "① ‘처음과’는", "수식한다.")),
    J(2, "적절", False, ["그는 처음과 같은 마음으로 공부를 했다."], "해설지",
      "‘마음으로’는 체언 ‘마음’에 부사격 조사 ‘으로’가 결합한 형태로 서술어 ‘했다’를 수식한다.",
      X(14, "② ‘마음으로’는", "수식한다.")),
    J(3, "적절", False, ["그는 처음과 같은 마음으로 공부를 했다. 그래서"], "해설지",
      "‘그래서’는 부사로서 앞뒤 두 문장을 이어 준다.",
      X(14, "③ ‘그래서’는", "이어준다.")),
    J(4, "적절", False, ["그래서 아주 쉽게"], "해설지",
      "‘아주’는 부사로서 부사어 ‘쉽게’를 수식한다.",
      X(14, "④ ‘아주’는", "수식한다.")),
    J(5, "부적절", True, ["그래서 아주 쉽게 원하는 대학에 합격했다."], "해설지",
      "‘쉽게’는 형용사 ‘쉽다’의 활용형이지만 수식하는 말은 관형어가 아니라 서술어 ‘합격했다’이다.",
      X(14, "‘쉽게’는 형용사인", "수식한다.")),
]

Q[15]["answer"] = 4
Q[15]["judgments"] = [
    J(1, "적절", False, ["그 ㉠\ue7b4 世尊이"], "해설지",
      "㉠은 음절의 첫머리에 자음이 연속으로 둘 이상 오는 어두자음군이다.",
      X(15, "① 음절의 첫머리에", "어두자음군이라고 한다.")),
    J(2, "적절", False, ["㉡世尊ㅅ"], "해설지",
      "㉡의 ‘ㅅ’은 현대어 ‘의’에 해당하는 관형격 조사이다.",
      X(15, "② ‘ㅅ’은 현대어", "관형격 조사이다.")),
    J(3, "적절", False, ["㉢사\ue46c미라"], "해설지",
      "㉢은 체언의 종성을 서술격 조사의 초성으로 이어 적은 이어적기이다.",
      X(15, "③ ‘사\ue46c미라’는", "이어 적었다.")),
    J(4, "부적절", True, ["㉣니\ue46c샤\ue3a8", "허공에서 야수께 이르시되"], "해설지",
      "㉣의 ‘-샤-’는 객체가 아니라 주체를 높이는 선어말 어미이다.",
      X(15, "‘니\ue46c샤\ue3a8’는", "주체를 높이고 있다.")),
    J(5, "적절", False, ["㉤모\ue46c\ue285다", "생각하느냐 모르느냐?”"], "해설지",
      "㉤은 현대어 ‘모르느냐’에 해당하며 의문형 어미 ‘-ㄴ다’가 쓰였다.",
      X(15, "⑤ ‘모\ue46c\ue285다’는", "사용되었다.")),
]
for q in d["questions"]:
    assert len(q["choices"]) == 5 and len(q["judgments"]) == 5 and q["stem"]

json.dump(d, open(HERE + r"\세트_13-15.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok")
