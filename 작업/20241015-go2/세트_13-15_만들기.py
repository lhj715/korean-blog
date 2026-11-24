"""2024년 10월 고2 13~15번(문법 단독 문항 묶음, 안내문 없음) 세트: 초안 + 쪽 그림 확인값 + 해설지 기반 판단 → 세트_13-15.json

초안은 도구/세트_뽑기.py 로 뽑았다(_임시\초안_13-15.json, 문단시작 파일은 빈 파일). 쪽 그림(문제_5쪽.png)으로 확인한 것:
- 13번 <보기> 한 상자(㉠㉡㉢ 세 줄, 밑줄 없음). 발문에 밑줄 없음.
- 14번 <보기>: «선생님» «학생» 이름만 굵음(콜론은 보통, texttrace type=1 은 이름 부분뿐). 발문 밑줄 '않은'.
  선지는 두 줄씩이고 줄마다 밑줄 낱말이 하나씩 있다(만큼·만큼, 다섯·다섯, 아무·아무, 모두·모두, 이·이).
- 15번 <보기> 본문 문단에 옛한글 PUA 글자가 있어 그 문단을 쪽에서 오려 낸 그림(display_image)으로 보인다.
  [탐구 자료] 상자(원본은 노트 모양 그림): 소제목 «[탐구 자료]»·«[현대어 풀이]» 굵음, 본문 첫 문단은 PUA 때문에 그림,
  굵은 말 王薦(왕천)의 아비 / 아ᄃᆞ리 / 하ᄂᆞᆯ / 너를. 노트 모양 테두리는 못 그림(한계).
  선지 ③④의 옛한글 PUA(U+E38A, U+E28C)는 choice_images.
"""
import json
import re

HERE = r"D:\Work\블로그\리딩맵\작업\20241015-go2"
d = json.load(open(HERE + r"\_임시\초안_13-15.json", encoding="utf-8"))
d.pop("raw_passage_lines", None)
d["meta"] = {"exam": "2024학년도 10월 고2 전국연합학력평가 국어", "exam_id": "20241015-go2", "area": "문법",
             "topic": "음운 변동·품사 통용·중세 국어의 격조사", "problem_pdf": "20241015-go2-problem-kor_mun_W63LRCEE.pdf",
             "explanation_pdf": "20241015-go2-explanation-kor_hsj_H2P1DE49.pdf"}
d["guide"] = None
d["passage"] = []
Q = {q["no"]: q for q in d["questions"]}

expl = open(HERE + r"\해설_글자.txt", encoding="utf-8").read()


def section(no):
    i = expl.index(f"\n{no}. [출제의도]")
    j = expl.index(f"\n{no + 1}. [출제의도]", i)
    return expl[i:j]


def X(no, a, b="적절하다"):
    sec = section(no)
    keep = [(i, c) for i, c in enumerate(sec) if not c.isspace()]
    comp = "".join(c for _, c in keep)
    ca = re.sub(r"\s+", "", a)
    cb = re.sub(r"\s+", "", b)
    ia = comp.index(ca)
    ib = comp.index(cb, ia) + len(cb)
    return sec[keep[ia][0]: keep[ib - 1][0] + 1].replace("\n", "")


def Xn(no, a, b):  # 적절하지 않다 까지
    return X(no, a, b)


def J(choice, verdict, ans, ev, basis, reason, xq=None):
    out = {"choice": choice, "verdict": verdict, "is_answer": ans, "basis": basis, "reason": reason,
           "evidence": [{"source": "bogi", "para": None, "quote": e} for e in ev]}
    if xq:
        out["explanation_quote"] = xq
    return out


# ---- 13번
s13 = Q[13]["stem"]
Q[13]["stem"] = s13[: s13.index("것은?") + 3]
Q[13]["bogi"] = {"label": "보 기", "blocks": [
    {"id": "b1", "type": "para", "text": "㉠ 흙장난[흑짱난]", "underlines": []},
    {"id": "b2", "type": "para", "text": "㉡ 부엌문[부엉문]", "underlines": []},
    {"id": "b3", "type": "para", "text": "㉢ 벼훑이[벼훌치]", "underlines": []}]}

# ---- 14번
s14 = Q[14]["stem"]
Q[14]["stem"] = s14[: s14.index("보 기")]
Q[14]["stem_underlines"] = ["않은"]
body14 = s14[s14.index("선생님:"):]
i2 = body14.index("학생:")
Q[14]["bogi"] = {"label": "보 기", "blocks": [
    {"id": "b1", "type": "para", "dialogue": True, "text": body14[:i2].strip(), "bold": ["선생님"], "underlines": []},
    {"id": "b2", "type": "para", "dialogue": True, "text": body14[i2:].strip(), "bold": ["학생"], "underlines": []}]}
Q[14]["choice_underlines"] = {"1": ["만큼", "만큼"], "2": ["다섯", "다섯"], "3": ["아무", "아무"],
                              "4": ["모두", "모두"], "5": ["이", "이"]}

# ---- 15번
s15 = Q[15]["stem"]
Q[15]["stem"] = s15[: s15.index("보 기")]
Q[15]["stem_underlines"] = ["않은"]
body = s15[s15.index("중세 국어에서는"):]
i_t = body.index("[탐구 자료]")
i_h = body.index("[현대어 풀이]")
b_main = body[:i_t].strip()
b_tam = body[i_t + len("[탐구 자료]"): i_h].strip()
b_hyun = body[i_h + len("[현대어 풀이]"):].strip()
assert b_tam.startswith("王薦(왕천)의 아비") and b_hyun.startswith("왕천의 아버지가")
BOLD_TAM = ["王薦(왕천)의 아비", "아\ue38a리", "하\ue28c", "너를"]
Q[15]["bogi"] = [
    {"label": "보 기", "blocks": [
        {"id": "b1", "type": "para", "text": b_main, "display_image": "그림_13-15_15_보기.png", "underlines": []}]},
    {"label": "", "blocks": [
        {"id": "b2", "type": "para", "text": "[탐구 자료]", "bold": ["[탐구 자료]"], "underlines": []},
        {"id": "b3", "type": "para", "text": b_tam, "display_image": "그림_13-15_15_탐구자료.png", "bold": BOLD_TAM,
         "underlines": []},
        {"id": "b4", "type": "para", "text": "[현대어 풀이]", "bold": ["[현대어 풀이]"], "underlines": []},
        {"id": "b5", "type": "para", "text": b_hyun, "underlines": []}]},
]
c3, c4 = Q[15]["choices"][2], Q[15]["choices"][3]
assert "\ue38a" in c3 and "\ue28c" in c4
Q[15]["choice_images"] = {
    "3": [{"text": "\ue38a", "image": "그림_13-15_15_선지_a.png", "alt": "ᄃᆞ"}],
    "4": [{"text": "\ue28c", "image": "그림_13-15_15_선지_b.png", "alt": "ᄂᆞᇙ"}]}

# ================= 판단
Q[13]["answer"] = 4
Q[13]["judgments"] = [
    J(1, "부적절", False, ["㉠ 흙장난[흑짱난]", "㉡ 부엌문[부엉문]", "㉢ 벼훑이[벼훌치]"], "해설지",
      "㉠은 자음군 단순화와 된소리되기로 2번, ㉡은 음절의 끝소리 규칙과 비음화로 2번, ㉢은 구개음화로 1번 일어나므로 횟수가 같지 않다.",
      X(13, "① 음운 변동이 ㉠에서", "적절하지 않다")),
    J(2, "부적절", False, ["㉠ 흙장난[흑짱난]", "㉡ 부엌문[부엉문]"], "해설지",
      "㉠에서는 자음군 단순화로 음운의 개수가 줄었지만, ㉡에서는 교체만 일어나 음운의 개수가 달라지지 않았다.",
      X(13, "② ㉠에서 자음군", "적절하지 않다")),
    J(3, "부적절", False, ["㉠ 흙장난[흑짱난]", "㉢ 벼훑이[벼훌치]"], "해설지",
      "㉠에서는 겹받침 중 ‘ㄹ’이 탈락했지만, ㉢에서는 탈락이 일어나지 않았다.",
      X(13, "③ ㉠에서는 흙", "적절하지 않다")),
    J(4, "적절", True, ["㉡ 부엌문[부엉문]", "㉢ 벼훑이[벼훌치]"], "해설지",
      "㉡의 음절의 끝소리 규칙과 비음화, ㉢의 구개음화는 모두 한 음운이 다른 음운으로 바뀌는 교체이므로 둘의 공통 변동은 교체다.",
      X(13, "㉡의 부엌문", "적절하다")),
    J(5, "부적절", False, ["㉢ 벼훑이[벼훌치]"], "해설지",
      "㉢에서는 구개음화만 일어나고 새로운 음운이 첨가되는 변동은 일어나지 않았다.",
      X(13, "⑤ ㉢에서는 새로운", "적절하지 않다")),
]

T14 = "동일한 형태의 한 단어가 체언과 수식언으로 사용되는 사례"
Q[14]["answer"] = 1
Q[14]["judgments"] = [
    J(1, "부적절", True, [T14], "해설지",
      "‘만큼’은 앞의 예에서는 의존 명사(체언)이지만 뒤의 예에서는 조사(관계언)로 쓰여, 체언과 수식언으로 쓰인 사례가 아니다.",
      X(14, "‘노력한 만큼", "적절하지 않다")),
    J(2, "적절", False, [T14], "해설지",
      "‘다섯’은 앞에서 관형사(수식언), 뒤에서 수사(체언)로 쓰였다.",
      X(14, "② ‘잘 익은", "적절하다")),
    J(3, "적절", False, [T14], "해설지",
      "‘아무’는 앞에서 대명사(체언), 뒤에서 관형사(수식언)로 쓰였다.",
      X(14, "③ ‘회의실에", "적절하다")),
    J(4, "적절", False, [T14], "해설지",
      "‘모두’는 앞에서 명사(체언), 뒤에서 부사(수식언)로 쓰였다.",
      X(14, "④ ‘그 일은", "적절하다")),
    J(5, "적절", False, [T14], "해설지",
      "‘이’는 앞에서 관형사(수식언), 뒤에서 대명사(체언)로 쓰였다.",
      X(14, "⑤ ‘이 나무는", "적절하다")),
]

JU = "주격 조사는 자음 뒤에서는 ‘이’, 모음 ‘이’나 반모음 ‘ㅣ’ 이외의 모음 뒤에서는 ‘ㅣ’, 모음 ‘이’나 반모음 ‘ㅣ’ 뒤에서는 ‘∅(영형태)’로 나타났다."
assert JU in b_main
GH = "관형격 조사는 유정 체언 뒤에서는 ‘\ueea4/의’, 무정 체언이나 높임의 유정 체언 뒤에서는 ‘ㅅ’으로 나타났다."
assert GH in b_main
GH_UNIT = "무정 체언이나 높임의 유정 체언 뒤에서는 ‘ㅅ’으로 나타났다."
MOK = "목적격 조사는 자음 뒤에서는"
MOK_FULL = b_main[b_main.index(MOK): b_main.index("나타났다.", b_main.index("음성 모음 뒤에서는")) + 5]
Q[15]["answer"] = 2
Q[15]["judgments"] = [
    J(1, "적절", False, [GH, "王薦(왕천)의 아비"], "해설지",
      "‘王薦(왕천)’은 유정 체언이고, 그 뒤에 관형격 조사 ‘의’가 쓰였다.",
      X(15, "① ‘王薦(왕천)의’는", "적절하다")),
    J(2, "부적절", True, [JU, "王薦(왕천)의 아비 "], "해설지",
      "‘아비’는 모음 ‘이’로 끝난 체언이므로 주격 조사가 ‘∅(영형태)’로 나타나야 한다. ‘ㅣ’가 실현된 것이 아니다.",
      X(15, "‘아비’는 모음", "적절하지 않다")),
    J(3, "적절", False, [JU, "아\ue38a리"], "해설지",
      "이 체언은 자음으로 끝났으므로 그 뒤에 주격 조사 ‘이’가 실현된다.",
      X(15, "③", "적절하다")),
    J(4, "적절", False, [GH_UNIT, "하\ue28c"], "해설지",
      "이 체언은 무정 체언이므로 그 뒤에 관형격 조사 ‘ㅅ’이 실현된다.",
      X(15, "④", "적절하다")),
    J(5, "적절", False, [MOK_FULL, "너를"], "해설지",
      "‘너를’은 음성 모음 ‘ㅓ’ 뒤에서 목적격 조사 ‘를’이 쓰였다.",
      X(15, "⑤ ‘너를’은", "적절하다")),
]
# 인용이 보기·탐구 자료 글에 글자 그대로 있어야 하므로, 아비 줄 인용은 탐구 자료에서 잘라 쓴다
for j in Q[15]["judgments"]:
    for e in j["evidence"]:
        e["quote"] = e["quote"].strip()

json.dump(d, open(HERE + r"\세트_13-15.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok")
