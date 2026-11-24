"""2024-07 고3 화법과 작문 35~37번 세트(화법, 발표: 한옥의 기와): 초안 + 쪽 그림 확인값 + 해설지 기반 판단 → 세트_35-37.json

초안은 _임시/초안_뽑기_래퍼_35-45.py (점선 뒤 번호·줄 앞 공백 처리 래퍼)로 뽑았다. 36번은 래퍼가 잘못 나눠 PDF 줄에서 다시 짠다.
쪽 그림(문제_13쪽_왼쪽/오른쪽.png)·texttrace 로 확인한 것:
- 발표 지문은 상자 안 5문단(들여쓰기로 시작). 밑줄·굵은 글씨 없음.
- 35번 발문 밑줄 없음. 36·37번 발문 '않은' 밑줄.
- 36번 발문 뒤 메모 상자 하나(점선 지시선 + ①~⑤). 선지 글·번호가 상자 글 안에 있다(choices_in_box).
  '∙화제 선정'·'∙청중 분석'·'∙발표 구성' 은 Haansoft Batang type 0+1 겹침이라 굵은 글씨. '- ' 줄은 type 0 전용.
- 37번 <보 기> 상자: 대화 3줄. '학생N :' 은 Haansoft Dotum type 0+1 겹침(콜론 포함)이라 굵은 글씨.
  37번 ⑤ 뒤에 붙은 쪽 머리글(2024학년도 … 제1 교시)은 선지가 아니다 → 잘라 낸다.
"""
import json
import re
import sys

sys.path.insert(0, r"D:\Work\블로그\리딩맵\도구")
import importlib
import fitz

HERE = r"D:\Work\블로그\리딩맵\작업\20240711-go3-korA"
PDF = r"D:\Work\블로그\리딩맵\원본자료\ebsi-korean\pdf\20240711-go3-problem-korA_1_mun_RXG65M96.pdf"
d = json.load(open(HERE + r"\초안_35-37.json", encoding="utf-8"))
d.pop("raw_passage_lines", None)
d["guide"] = "[35 ~ 37] 다음은 학생의 발표이다. 물음에 답하시오."
d["meta"] = {"exam": "2024학년도 7월 고3 전국연합학력평가 국어", "exam_id": "20240711-go3-korA", "area": "화법",
             "topic": "한옥의 기와에 대한 학생 발표",
             "problem_pdf": "20240711-go3-problem-korA_1_mun_RXG65M96.pdf",
             "explanation_pdf": "20240711-go3-explanation-korA_1_hsj_1P42X9B5.pdf"}
for p in d["passage"]:
    p["text"] = p["text"].strip()
P = {p["id"]: p for p in d["passage"]}
Q = {q["no"]: q for q in d["questions"]}
Q[36]["stem_underlines"] = ["않은"]
Q[37]["stem_underlines"] = ["않은"]

# 36번: PDF 줄에서 다시 짠다
m = importlib.import_module("세트_뽑기")
L = m.page_lines(fitz.open(PDF))
i0 = next(k for k, l in enumerate(L) if l.startswith("36."))
i1 = next(k for k, l in enumerate(L) if l.startswith("37."))
lines = [l for l in L[i0 + 1:i1] if l.strip()]
Q[36]["stem"] = "다음은 발표자의 발표 계획이다. 발표에 반영되지 않은 것은?"
blocks, choices, k = [], [], 0
n = 0
while n < len(lines):
    l = lines[n]
    if l.startswith("∙"):
        blocks.append({"id": f"h{len(blocks)}", "type": "label", "text": l.strip(), "underlines": [], "bold": [l.strip()]})
        n += 1
    else:
        assert l.startswith("- ")
        two = (l + lines[n + 1]).strip()
        k += 1
        body = re.split(r"\s*·{3,}", two[2:])[0].strip()
        choices.append(body)
        blocks.append({"id": f"q{k}", "type": "para", "text": two, "underlines": []})
        n += 2
assert k == 5 and len(choices) == 5
Q[36]["bogi"] = {"label": "", "blocks": blocks}
Q[36]["choices"] = choices
Q[36]["choices_in_box"] = True

# 37번: 발문 / <보 기> 분리
s37 = Q[37]["stem"]
i = s37.index("<보 기>")
Q[37]["stem"] = s37[:i].strip()
body = s37[i + len("<보 기>"):]
parts = [x.strip() for x in re.split(r"(?=학생[123] :)", body) if x.strip()]
assert len(parts) == 3, parts
Q[37]["bogi"] = {"label": "보 기", "blocks": [
    {"id": f"s{k}", "type": "para", "text": t, "underlines": [], "dialogue": True, "bold": [t.split(":")[0] + ":"]} for k, t in enumerate(parts, 1)]}
c5 = Q[37]["choices"][4]
Q[37]["choices"][4] = c5[: c5.index("2024학년도")].strip()
assert Q[37]["choices"][4].endswith("지적하고 있다.")
for q in d["questions"]:
    q["choices"] = [c.replace("\u3000", " ").strip() for c in q["choices"]]


def J(choice, verdict, ans, ev, basis, reason, xq=None):
    out = {"choice": choice, "verdict": verdict, "is_answer": ans, "basis": basis, "reason": reason,
           "evidence": [({"source": s, "fig": p, "para": None, "quote": q} if s == "figure" else {"source": s, "para": p, "quote": q})
                        for s, p, q in ev]}
    if xq:
        out["explanation_quote"] = xq
    return out


Q[35]["answer"] = 5
Q[35]["judgments"] = [
    J(1, "부적절", False, [("passage", "p2", "여러분은 기와에 대해 잘 알고 계신가요?")], "자체",
      "2문단에서 청중에게 기와를 아는지 묻지만, 답을 듣고 반응을 확인하는 말 없이 곧바로 기와의 정의를 설명해 나간다."),
    J(2, "부적절", False, [("passage", "p4", "당시에 연꽃은 진정한 군자라는 의미를 담고 있었다고 합니다.")], "자체",
      "연꽃 무늬의 의미를 전하면서도 '~라고 합니다'라고 말할 뿐 어떤 자료에서 가져왔는지 출처를 밝히지 않는다."),
    J(3, "부적절", False, [("passage", "p3", "우리 조상들은 왜 기와로 지붕을 덮었을까요?")], "해설지",
      "3문단에서 청중에게 질문을 던지지만 스스로 답을 이어 가며, 청중이 던지는 질문을 받는 대목은 없다.",
      "청중의 질문을 받고 있지는 않다"),
    J(4, "부적절", False, [("passage", "p1", "오늘은 한옥의 기와에 대해 말씀드리겠습니다.")], "자체",
      "1문단에서 발표 주제만 밝힐 뿐, 이어질 내용의 차례를 미리 안내하는 말은 어디에도 없다."),
    J(5, "적절", True, [("passage", "p5", "다음 주에 방문할 한옥 마을에서 기와를 더욱 눈여겨보았으면 좋겠습니다.")], "해설지",
      "마지막 5문단에서 한옥 마을에서 기와를 더 눈여겨보았으면 좋겠다고 청중에게 바라는 바를 말한 뒤 발표를 마친다.",
      "청중에게 바라는 바를 언급하며 발표를 마무리하고 있다"),
]

Q[36]["answer"] = 3
Q[36]["judgments"] = [
    J(1, "반영", False, [("passage", "p1", "지난 시간에 한옥에 관해 배울 때 기와가 무엇인지 잘 모른다는 친구들이 많아서 오늘은 한옥의 기와에 대해 말씀드리겠습니다."),
                       ("bogi", None, "청중의 배경지식을 고려하여 발표 내용을 한옥의 기와로 선정해야겠어.")], "해설지",
      "1문단에서 기와가 무엇인지 모르는 친구들이 많아 한옥의 기와를 발표 주제로 골랐다고 밝히므로 계획이 반영되었다.",
      "청중의 배경지식을 고려하여 발표 내용을 한옥의 기와로 선정했음을 언급하고 있다"),
    J(2, "반영", False, [("passage", "p1", "그럼 먼저 동영상을 보시죠. (동영상 제시) 기와가 만든 곡선이 무척 아름답게 느껴지는데요, 다음 주에 방문할 한옥 마을에서 지금 본 기와들을 직접 볼 수 있을 것입니다."),
                       ("bogi", None, "청중의 관심을 끌기 위해 청중과 관련 있는 발표 대상을 찍은 동영상 자료를 제시해야겠어.")], "해설지",
      "1문단에서 청중이 다음 주에 방문할 한옥 마을의 기와를 보여 주는 동영상을 제시하므로 계획이 반영되었다.",
      "청중이 ‘다음 주에 방문할 한옥 마을’의 기와를 보여 주는 동영상 자료를 제시하고 있다"),
    J(3, "미반영", True, [("passage", "p2", "기와에는 대표적으로 암키와와 수키와, 암막새와 수막새가 있습니다."),
                        ("bogi", None, "기와의 제작 과정을 보여 주기 위해 기와의 종류를 유형별로 분류하여 설명해야겠어.")], "해설지",
      "2문단은 기와를 암키와와 수키와, 암막새와 수막새로 나누어 설명할 뿐, 기와를 만드는 과정을 보여 주지는 않는다.",
      "기와의 종류를 유형별로 분류하여 설명하고 있지만, 기와의 제작 과정을 보여 주고 있지는 않다"),
    J(4, "반영", False, [("passage", "p3", "점토를 가마에서 높은 온도로 구워 만들기 때문에 기와는 마치 화장실에 많이 쓰이는 타일같이 물을 흡수하지 않는 성질을 가지고 있습니다."),
                       ("bogi", None, "빗물을 막는 기와의 기능을 설명하기 위해 일상의 친숙한 대상을 활용해야겠어.")], "해설지",
      "3문단에서 기와가 빗물을 막는 까닭을 화장실에 많이 쓰이는 타일에 빗대어 설명하므로 계획이 반영되었다.",
      "기와의 기능을 설명하기 위해 일상의 친숙한 대상인 ‘타일’을 활용하고 있다"),
    J(5, "반영", False, [("passage", "p4", "여기 두 사진이 보이시죠? 왼쪽은 고구려의, 오른쪽은 백제의 연꽃무늬 수막새입니다."),
                       ("bogi", None, "고구려와 백제의 연꽃무늬 수막새를 비교하기 위해 두 사진을 나란히 제시해야겠어.")], "해설지",
      "4문단에서 왼쪽에 고구려, 오른쪽에 백제의 연꽃무늬 수막새 사진을 나란히 보여 주며 비교하므로 계획이 반영되었다.",
      "‘왼쪽’에는 고구려의, ‘오른쪽’에는 백제의 수막새 사진을 나란히 제시하여 비교하고 있다"),
]

Q[37]["answer"] = 5
Q[37]["judgments"] = [
    J(1, "적절", False, [("bogi", None, "기와는 같은 무늬가 시기와 지역에 따라 다른 모양으로 표현되었다는 것이 흥미로웠어.")], "해설지",
      "학생 1은 같은 무늬가 시기와 지역에 따라 달리 표현되었다는 것이 흥미로웠다고 하여 발표에서 알게 된 정보를 긍정적으로 평가한다.",
      "발표를 통해 알게 된 정보를 긍정적으로 평가하고 있다"),
    J(2, "적절", False, [("bogi", None, "점토를 높은 온도에서 굽기 때문에 기와가 물을 흡수하지 않는 성질을 가진다고 했는데, 그 원리는 뭘까?")], "해설지",
      "학생 2는 발표에서 원리를 말하지 않은 기와의 물을 흡수하지 않는 성질에 대해 그 원리가 무엇인지 궁금해한다.",
      "발표에 언급되지 않은 정보에 대해 궁금증을 드러내고 있다"),
    J(3, "적절", False, [("bogi", None, "빗물을 빠르게 배수하는 데 기와지붕의 곡선도 영향을 준다는 것을 선생님께 들었어.")], "해설지",
      "학생 3은 빗물을 빠르게 배수하는 데 기와지붕의 곡선도 영향을 준다고 선생님께 들었다며 발표와 관련된 자신의 경험을 떠올린다.",
      "발표 내용과 관련 있는 자신의 경험을 떠올리고 있다"),
    J(4, "적절", False, [("bogi", None, "다음 주에 한옥 마을에서 문화 해설사에게 기와의 무늬에 대해 질문해야겠어."),
                       ("bogi", None, "그 과학적 원리가 무엇인지 누리집에서 검색해 봐야지.")], "해설지",
      "학생 1은 문화 해설사에게 질문하겠다고, 학생 3은 누리집에서 검색하겠다고 하여 둘 다 발표와 관련된 정보를 더 찾아보려 한다.",
      "발표 내용과 관련하여 추가적인 정보를 탐색하려 하고 있다"),
    J(5, "부적절", True, [("bogi", None, "점토를 높은 온도에서 굽기 때문에 기와가 물을 흡수하지 않는 성질을 가진다고 했는데, 그 원리는 뭘까? 더 자세히 설명해 주면 좋았을 것 같아."),
                        ("bogi", None, "그 과학적 원리가 무엇인지 누리집에서 검색해 봐야지.")], "해설지",
      "발표에서 필요한 내용이 빠졌다고 지적하는 것은 학생 2뿐이다. 학생 3은 궁금한 원리를 스스로 검색해 보겠다고 할 뿐 발표의 부족한 점을 말하지 않는다.",
      "‘학생3’은 지적하고 있지 않다"),
]

d["range"] = [35, 37]
json.dump(d, open(HERE + r"\세트_35-37.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok")
