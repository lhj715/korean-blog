"""2025-09 고2 11번(문법 단독 문항, 안내문·지문 없음) 세트 → 세트_11.json

쪽 그림(문제_4쪽_오른쪽.png)·PDF 로 확인한 것:
- guide null, passage []. <보기> 상자 하나: 순서도 그림(마름모 두 개 + ⓐ ⓑ ⓒ 상자, 글자는 텍스트층에 있음 → pdf_text) +
  «[자료]»(굵게, type 0+1) + 안쪽 상자(ㄱ~ㄹ 문장 4개, 실선 → inbox "자료").
- 선지는 ⓐ ⓑ ⓒ 세 칸 표: 표 머리(ⓐ ⓑ ⓒ)는 머리말 없는 plain 상자. 발문 밑줄 없음.
- 순서도 그림 rect = 마름모·화살표·ⓐⓑⓒ 상자 범위(그림_위치_11.json). «<보 기>» 머리말·[자료] 는 그림 밖.
"""
import json
import re
import sys

import fitz

sys.path.insert(0, r"D:\Work\블로그\리딩맵\도구")
m = __import__("세트_뽑기")

HERE = r"D:\Work\블로그\리딩맵\작업\20250903-go2"
PDF = r"D:\Work\블로그\리딩맵\원본자료\ebsi-korean\pdf\20250903-go2-problem-kor_mun_8HG61RY3_1.pdf"
lines = m.page_lines(fitz.open(PDF))
a = next(i for i, l in enumerate(lines) if l.startswith("11. <보기>"))
b = next(i for i, l in enumerate(lines) if l.startswith("[12~13]"))
L = lines[a:b]
SP = "\u3000"

stem = re.sub(r"^11\.\s*", "", L[0]).strip()
assert stem == "<보기>의 ⓐ～ⓒ에 들어갈 문장을 바르게 분류한 것은?", stem
assert L[2] == "<보 기>" and L[15] == "[자료]" and L[16].startswith("ㄱ.") and L[19].startswith("ㄹ.")
# 순서도 속 글자는 텍스트층 순서 그대로(L[3:15] 와 같다)
assert " ".join(x.strip() for x in L[3:15]) == ("하나의 문장에 다른 문장이 문장 성분의 자격으로 들어가 있는가? 안긴문장이 안은문장에서 "
                                              "체언을 수식하고 있는가? ⓒ 아니요 아니요 예 예 ⓐ ⓑ")
PDF_TEXT = ("하나의 문장에 다른 문장이 문장 성분의 자격으로 들어가 있는가? 안긴문장이 안은문장에서 체언을 수식하고 있는가? "
            "ⓒ 아니요 아니요 예 예 ⓐ ⓑ")

# 선지: ① 줄 뒤 세 칸씩
idx = [k for k, l in enumerate(L) if l[:1] and l[:1] in m.CIRCLED]
assert len(idx) == 5
ch = []
for n, k in enumerate(idx):
    e = idx[n + 1] if n + 1 < len(idx) else len(L)
    cells = [x.strip() for x in L[k + 1:e] if x.strip()]
    assert len(cells) == 3, cells
    ch.append((SP * 3).join(cells))

ex = [L[16].strip(), L[17].strip(), L[18].strip(), L[19].strip()]
bogi = [
    {"label": "보 기", "blocks": [
        {"id": "f1", "type": "figure", "caption": "", "image": "그림_11_11_순서도.png", "pdf_text": PDF_TEXT,
         "alt": "순서도: ‘하나의 문장에 다른 문장이 문장 성분의 자격으로 들어가 있는가?’에 ‘아니요’이면 ⓐ, ‘예’이면 "
                "‘안긴문장이 안은문장에서 체언을 수식하고 있는가?’로 넘어가고, 여기서 ‘아니요’이면 ⓑ, ‘예’이면 ⓒ."},
        {"id": "b1", "type": "para", "text": "[자료]", "underlines": [], "bold": ["[자료]"]},
        {"id": "e1", "type": "para", "text": ex[0], "underlines": [], "inbox": "자료"},
        {"id": "e2", "type": "para", "text": ex[1], "underlines": [], "inbox": "자료"},
        {"id": "e3", "type": "para", "text": ex[2], "underlines": [], "inbox": "자료"},
        {"id": "e4", "type": "para", "text": ex[3], "underlines": [], "inbox": "자료"},
    ]},
    {"label": "", "plain": True, "blocks": [
        {"id": "h1", "type": "heading", "text": SP * 2 + "ⓐ" + SP * 3 + "ⓑ" + SP * 3 + "ⓒ",
         "underlines": [{"mark": "", "text": "ⓐ"}, {"mark": "", "text": "ⓑ"}, {"mark": "", "text": "ⓒ"}]}]},
]

q = {"no": 11, "points": 2, "stem": stem, "bogi": bogi, "choices": ch, "answer": 1}
Q1 = "하나의 문장에 다른 문장이 문장 성분의 자격으로 들어가 있는가?"
Q2 = "안긴문장이 안은문장에서 체언을 수식하고 있는가?"
G, N, D, R = ("동생이 돌아왔다는 이야기를 들었다.", "나는 어버이날에 부모님께 편지를 썼다.",
              "그녀는 누구보다도 마음 씀씀이가 크다.", "옆집에 사는 친구와 요즘 매일 학교에 같이 간다.")


def J(choice, verdict, ans, ev, basis, reason, xq=None):
    def one(e):
        s, p, t = e
        if s == "figure":
            return {"source": s, "fig": p, "para": None, "quote": t}
        return {"source": s, "para": p, "quote": t}
    out = {"choice": choice, "verdict": verdict, "is_answer": ans, "basis": basis, "reason": reason,
           "evidence": [one(e) for e in ev]}
    if xq:
        out["explanation_quote"] = xq
    return out


q["judgments"] = [
    J(1, "적절", True,
      [("bogi", None, N), ("bogi", None, D), ("bogi", None, G), ("bogi", None, R)], "해설지",
      "ㄴ은 다른 문장이 들어가 있지 않은 홑문장이라 ⓐ이다. ㄷ은 ‘마음 씀씀이가 크다’라는 서술절을 안은 문장으로 체언을 수식하는 안긴문장이 아니어서 ⓑ이다. "
      "ㄱ은 ‘동생이 돌아왔다는’, ㄹ은 ‘옆집에 사는’이라는 관형절이 체언을 꾸미므로 ⓒ이다.",
      "ㄱ은 ‘동생이 돌아왔다는’이라는 관형절을 가진 안은문장이고, ㄹ은 ‘옆집에 사는’이라는 관형절을 가진 안은문장이다. ㄴ은 홑문장이며 ㄷ은 ‘마음 씀씀이가 크다’라는 서술절을 가진 안은문장이다."),
    J(2, "부적절", False,
      [("bogi", None, "옆집에 사는 친구와 요즘 매일 학교에 같이 간다."), ("figure", "f1", Q2)], "자체",
      "ㄹ은 ‘옆집에 사는’이 체언 ‘친구’를 꾸미는 관형절이어서 ‘체언을 수식하고 있는가?’에 ‘예’이므로 ⓑ이 아니라 ⓒ에 들어가야 한다."),
    J(3, "부적절", False,
      [("bogi", None, "그녀는 누구보다도 마음 씀씀이가 크다."), ("figure", "f1", Q1)], "자체",
      "ㄷ은 ‘마음 씀씀이가 크다’라는 서술절이 문장 성분으로 들어 있어 첫 물음에 ‘예’이므로 ⓐ에 들어갈 수 없다. ⓐ에는 ㄴ이 들어간다."),
    J(4, "부적절", False,
      [("bogi", None, "동생이 돌아왔다는 이야기를 들었다."), ("figure", "f1", Q1)], "자체",
      "ㄱ은 ‘동생이 돌아왔다는’이라는 관형절이 문장 성분으로 들어 있어 첫 물음에 ‘예’이므로 ⓐ에 들어갈 수 없고, 체언을 수식하므로 ⓒ에 들어간다."),
    J(5, "부적절", False,
      [("bogi", None, "나는 어버이날에 부모님께 편지를 썼다."), ("figure", "f1", Q1)], "자체",
      "ㄴ은 다른 문장이 문장 성분으로 들어 있지 않은 홑문장이어서 첫 물음에 ‘아니요’이므로 ⓒ이 아니라 ⓐ에 들어가야 한다."),
]

data = {
    "meta": {"exam": "2025년 9월 고2 전국연합학력평가 국어", "exam_id": "20250903-go2", "area": "문법",
             "topic": "구조에 따른 문장의 종류",
             "problem_pdf": "20250903-go2-problem-kor_mun_8HG61RY3_1.pdf",
             "explanation_pdf": "20250903-go2-explanation-kor_hsj_ICT76N4K_1.pdf"},
    "guide": None, "range": [11, 11], "passage": [], "questions": [q],
}
json.dump(data, open(HERE + r"\세트_11.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", ch)
