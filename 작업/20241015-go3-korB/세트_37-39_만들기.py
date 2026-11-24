"""2024-10 고3 언어와 매체(korB) 37~39번 세트(안내문 없는 단독 문항 묶음): 초안 + 쪽 그림 확인값 + 해설지 기반 판단 → 세트_37-39.json

확인한 것(2026-11-25, 문제_13쪽·14쪽 그림, PDF 텍스트층·선·글꼴, 400dpi 확대):
- 37번 <보기> 상자: ㄱ~ㅁ 다섯 줄, 밑줄·굵은 글씨 없음. 발문 «않은» 밑줄(PDF 선 확인).
- 38번 <보기> 상자: 문단 1개 + ◦ 줄 4개. 밑줄 ㉠놓친다 ㉡넘기면 ㉢되찾기 ㉣앞당겼다 ㉤뒤섞는 ㉥끝마치곤(PDF 선 6개). 굵은 글씨 없음.
- 39번 <보기> 상자: 선생님 말(굵은 글씨는 «선생님» 만, 콜론은 보통) + «[예문]»(굵음, 대괄호 포함) + ㄱ~ㄹ 예문 줄(옛한글 PUA 있음 → display_image)
  + 줄 아래 현대어 풀이 [ ] . 선지는 ㉠~㉣ 네 칸 표(머리 ㉠㉡㉢㉣ 에 밑줄 4개, 테두리 없음 → plain 상자).
  선지 안 옛한글 PUA 22글자는 choice_images(글자마다 쪽에서 오려 냄). 발문에 밑줄 없음.
- 37번 ⑤ 뒤에 쪽 머리글이 붙으므로 잘라 낸다.
"""
import json
import re

HERE = r"D:\Work\블로그\리딩맵\작업\20241015-go3-korB"
d = json.load(open(HERE + r"\초안_37-39.json", encoding="utf-8"))
d.pop("raw_passage_lines", None)
d["meta"] = {"exam": "2024학년도 10월 고3 전국연합학력평가", "exam_id": "20241015-go3-korB",
             "area": "문법", "topic": "안긴문장·단어의 구성·중세 국어",
             "problem_pdf": "20241015-go3-problem-korB_1_mun_6XCL7212.pdf",
             "explanation_pdf": "20241015-go3-explanation-korB_1_hsj_Z62463WQ.pdf"}
d["guide"] = None
d["range"] = [37, 39]
d["passage"] = []
Q = {q["no"]: q for q in d["questions"]}
PUA = re.compile("[\ue000-\uf8ff]")

# ---- 37번
s = Q[37]["stem"]
i = s.index("< 보 기 >")
Q[37]["stem"] = s[:i]
Q[37]["stem_underlines"] = ["않은"]
lines = [x for x in re.split(r"(?=[ㄱㄴㄷㄹㅁ]\. )", s[i + len("< 보 기 >"):]) if x]
assert len(lines) == 5, lines
Q[37]["bogi"] = {"label": "< 보 기 >", "blocks": [{"id": f"b{k+1}", "type": "para", "text": t, "underlines": []} for k, t in enumerate(lines)]}
c = Q[37]["choices"][4]
Q[37]["choices"][4] = c[: c.index("있다.") + 3]

# ---- 38번
s = Q[38]["stem"]
i = s.index("< 보 기 >")
Q[38]["stem"] = s[:i]
body = s[i + len("< 보 기 >"):]
intro = body[: body.index("◦")]
rest = body[len(intro):]
bul = ["◦" + x for x in rest.split("◦") if x]
assert len(bul) == 4, bul
UL38 = [[("㉠", "놓친다")], [("㉡", "넘기면"), ("㉢", "되찾기")], [("㉣", "앞당겼다")], [("㉤", "뒤섞는"), ("㉥", "끝마치곤")]]
b38 = [{"id": "b1", "type": "para", "text": intro, "underlines": []}]
for k, t in enumerate(bul):
    for m, u in UL38[k]:
        assert m + u in t, (m, u, t)
    b38.append({"id": f"b{k+2}", "type": "para", "text": t, "underlines": [{"mark": m, "text": u} for m, u in UL38[k]]})
Q[38]["bogi"] = {"label": "< 보 기 >", "blocks": b38}

# ---- 39번
s = Q[39]["stem"]
i = s.index("< 보 기 >")
Q[39]["stem"] = s[:i]
body = s[i + len("< 보 기 >"):]
assert body.endswith("㉠㉡㉢㉣")
body = body[: -len("㉠㉡㉢㉣")]
j = body.index("[예문]ㄱ.")
talk = body[:j].strip()
ex = body[j + len("[예문]"):]
assert talk.startswith("선생님:") and talk.endswith("나타날까요?")
parts = [x for x in re.split(r"(?=[ㄱㄴㄷㄹ]\. )", ex) if x]
assert len(parts) == 4, parts
blocks = [{"id": "b1", "type": "para", "dialogue": True, "text": talk, "bold": ["선생님"], "underlines": [], "display_image": "그림_37-39_39_보기본문.png"},
          {"id": "b2", "type": "para", "text": "[예문]", "bold": ["[예문]"], "underlines": []}]
n = 3
for k, t in enumerate(parts):
    a, b = t.split("[", 1)
    assert PUA.search(a) and not PUA.search(b)
    blocks.append({"id": f"b{n}", "type": "para", "text": a, "underlines": [], "display_image": f"그림_37-39_39_예문{k+1}.png"})
    blocks.append({"id": f"b{n+1}", "type": "para", "text": "[" + b, "underlines": []})
    n += 2
Q[39]["bogi"] = [
    {"label": "< 보 기 >", "blocks": blocks},
    {"label": "", "plain": True, "blocks": [
        {"id": "h1", "type": "heading", "text": "㉠　　　　㉡　　　　㉢　　　　㉣",
         "underlines": [{"mark": "", "text": m} for m in "㉠㉡㉢㉣"]}]},
]
# 선지 표: 칸마다 3칸 공백으로 잇는다
info = json.load(open(HERE + r"\_임시\선지그림_37-39.json", encoding="utf-8"))
SP = "\u3000\u3000\u3000"
ALT = {"0xf537": "아래아가 든 옛 글자 ‘ᄒᆞ’", "0xe46c": "아래아가 든 옛 글자 ‘ᄅᆞ’", "0xf53c": "아래아가 든 옛 글자 ‘ᄒᆞᆯ’",
       "0xe46e": "아래아가 든 옛 글자 ‘ᄅᆞᆫ’", "0xe20c": "옛 글자 ‘낡’(ᄂᆞᆰ)"}
ci = {}
for k in range(5):
    raw = Q[39]["choices"][k]
    m = re.fullmatch(r"(.*?마다)(나모와|남과)(.*?도)(.*)", raw)
    assert m, raw
    Q[39]["choices"][k] = SP.join(m.groups())
    lst = info[str(k + 1)]
    chars = [ch for ch in raw if PUA.match(ch)]
    assert [hex(ord(ch)) for ch in chars] == [h for h, _ in lst], (k, chars, lst)
    ci[str(k + 1)] = [{"text": ch, "image": nm, "alt": ALT[h]} for ch, (h, nm) in zip(chars, lst)]
Q[39]["choice_images"] = ci
for q in d["questions"]:
    assert len(q["choices"]) == 5 and q["stem"], q["no"]


def J(choice, verdict, ans, ev, basis, reason, xq=None):
    out = {"choice": choice, "verdict": verdict, "is_answer": ans, "basis": basis, "reason": reason,
           "evidence": [{"source": "bogi", "para": None, "quote": q} for q in ev]}
    if xq:
        out["explanation_quote"] = xq
    return out


# ======== 37번 (정답 ⑤, 적절하지 않은 것)
Q[37]["answer"] = 5
Q[37]["judgments"] = [
    J(1, "적절", False, ["ㄱ. 마을 사람들은 그가 가족과 만나기를 바란다.", "ㄷ. 어제 동생은 무역 회사에 다니는 사람을 만났다."], "자체",
      "ㄱ의 안긴문장 ‘그가 가족과 만나기’에는 ‘만나다’가 요구하는 필수적 부사어 ‘가족과’가 있고, ㄷ의 안긴문장 ‘무역 회사에 다니는’에는 ‘다니다’가 요구하는 필수적 부사어 ‘무역 회사에’가 있다."),
    J(2, "적절", False, ["ㄱ. 마을 사람들은 그가 가족과 만나기를 바란다.", "ㅁ. 뒷산에서 다리를 다친 언니는 병원에 입원하였다."], "자체",
      "ㄱ의 ‘그가 가족과 만나기’는 ‘를’이 붙어 ‘바란다’의 목적어로 쓰였고, ㅁ의 ‘뒷산에서 다리를 다친’은 뒤의 ‘언니’를 꾸미는 관형어로 쓰였다."),
    J(3, "적절", False, ["ㄴ. 그들은 옛 친구가 살던 동네에서 시간을 보냈다.", "ㄹ. 나는 문득 그가 나에게 호의를 가졌음을 느꼈다."], "자체",
      "ㄴ의 안긴문장 ‘옛 친구가 살던’에서 ‘살다’의 필수적 부사어(‘동네에서’)는 생략되어 있다. ㄹ의 안긴문장 ‘그가 나에게 호의를 가졌음’에는 주어 ‘그가’, 부사어 ‘나에게’, 목적어 ‘호의를’이 모두 있어 생략된 필수 성분이 없다."),
    J(4, "적절", False, ["ㄴ. 그들은 옛 친구가 살던 동네에서 시간을 보냈다.", "ㄷ. 어제 동생은 무역 회사에 다니는 사람을 만났다."], "자체",
      "ㄴ의 ‘옛 친구가 살던’은 체언 ‘동네’를, ㄷ의 ‘무역 회사에 다니는’은 체언 ‘사람’을 꾸미는 관형절이므로 둘 다 체언을 수식하는 기능을 한다."),
    J(5, "부적절", True, ["ㄹ. 나는 문득 그가 나에게 호의를 가졌음을 느꼈다.", "ㅁ. 뒷산에서 다리를 다친 언니는 병원에 입원하였다."], "해설지",
      "ㄹ의 안긴문장에는 목적어 ‘호의를’과 필수적 부사어 ‘나에게’가 있다. 그러나 ㅁ의 안긴문장 ‘뒷산에서 다리를 다친’에는 목적어 ‘다리를’만 있고 필수적 부사어는 없다. 따라서 둘 다 필수적 부사어와 목적어가 있다는 이해는 적절하지 않다.",
      "ㄹ의 안긴문장에는 목적어와 필수적 부사어가 포함되어 있지만 ㅁ의 안긴문장에는 필수적 부사어가 포함되어 있지 않다"),
]

# ======== 38번 (정답 ③, 적절한 것)
T = "용언은 활용을 하기 때문에 어간과 어미로 나눌 수 있으며 어미에는 어말 어미와 선어말 어미가 있다."
G = "합성어 용언의 어간은 ‘어근+어근’으로 구성되어 있고, 파생어 용언의 어간은 ‘접두사+어근’ 혹은 ‘어근+접미사’로 구성되어 있다."
l1, l2, l3, l4 = "뛰는 토끼 잡으려다 잡은 토끼 ㉠놓친다.", "치료 시기를 ㉡넘기면 건강을 ㉢되찾기 어렵다.", "책임자는 건물의 완공일을 일주일 정도 ㉣앞당겼다.", "그는 흙과 모래를 ㉤뒤섞는 일을 혼자 ㉥끝마치곤 했다."
Q[38]["answer"] = 3
Q[38]["judgments"] = [
    J(1, "부적절", False, [T, l1, l4], "자체",
      "㉠ ‘놓친다’에는 어말 어미 ‘-다’ 앞에 현재를 나타내는 선어말 어미 ‘-ㄴ-’이 쓰였지만, ㉥ ‘끝마치곤’에는 선어말 어미가 없다. 동일한 선어말 어미가 쓰였다는 설명은 틀리다."),
    J(2, "부적절", False, [l2, l3, G], "자체",
      "㉡ ‘넘기면’의 어간 ‘넘기-’는 어근에 접미사 ‘-기-’가 붙은 파생어 용언이다. 반면 ㉣ ‘앞당겼다’의 어간 ‘앞당기-’는 ‘앞’과 ‘당기-’ 두 어근으로 이루어진 합성어 용언이라 접사가 없다."),
    J(3, "적절", True, [G, l2, l4], "해설지",
      "㉢ ‘되찾기’와 ㉤ ‘뒤섞는’은 파생어 용언이고, 두 어간 모두 접두사 ‘되-’, ‘뒤-’에 어근 ‘찾-’, ‘섞-’이 붙은 ‘접두사+어근’ 구성이다.",
      "㉢과 ㉤은 파생어 용언으로 모두 어간이 접두사와 어근으로 구성되어 있다"),
    J(4, "부적절", False, [T, l3], "자체",
      "㉣ ‘앞당겼다’에는 선어말 어미 ‘-었-’ 하나와 어말 어미 ‘-다’ 하나가 쓰였다. 두 개의 선어말 어미가 쓰였다는 설명은 틀리다."),
    J(5, "부적절", False, [G, l4], "자체",
      "㉥ ‘끝마치곤’의 어간 ‘끝마치-’는 ‘끝’과 ‘마치-’ 두 어근이 합쳐진 합성어 용언의 어간이다. 어근과 접미사로 구성되었다는 설명은 틀리다."),
]

# ======== 39번 (정답 ③, 적절한 것)
R1 = "자음으로 시작하는 조사나 조사 ‘와’와 결합할 때 ‘나모’"
R2 = "‘와’를 제외한 모음으로 시작하는 조사와 결합할 때"
E1, E2, E3, E4 = "[원숭이가 나무마다 매달렸다 한다]", "[나무와 흙으로 하며]", "[하루도 벗 없이 하지 못하셨다]", "[하루는 조심하지 아니하셔]"
Q[39]["answer"] = 3
Q[39]["judgments"] = [
    J(1, "부적절", False, [R2, E4], "자체",
      "㉣은 ‘하루’가 모음으로 시작하는 조사 ‘은’과 결합한 자리이므로 모음 앞에서 쓰이는 형태가 와야 한다. 그런데 이 선지의 ㉣에는 자음 앞에서 쓰이는 형태가 놓였다."),
    J(2, "부적절", False, [R1, E2, E4], "자체",
      "㉡은 ‘나무’가 조사 ‘와’와 결합한 자리인데, ‘와’와 결합할 때는 ‘나모’ 형태가 쓰이므로 ‘나모와’가 와야 한다. 이 선지의 ㉡은 ‘남과’라서 맞지 않고, ㉢에도 모음 앞 형태가 놓여 있다."),
    J(3, "적절", True, [R1, R2, E1, E2, E3, E4], "해설지",
      "㉠은 자음으로 시작하는 조사 ‘마다’, ㉡은 조사 ‘와’와 결합하므로 모두 ‘나모’ 형태인 ‘나모마다’, ‘나모와’가 온다. ㉢은 자음으로 시작하는 조사 ‘도’와 결합하므로 자음 앞 형태의 ‘하루도’, ㉣은 모음으로 시작하는 조사 ‘은’과 결합하므로 모음 앞 형태의 ‘하루는’이 온다. 네 칸이 모두 맞는다.",
      "이 단어들은 자음으로 시작하는 조사나 조사 ‘와’와 결합할 때"),
    J(4, "부적절", False, [R1, E1, E2], "자체",
      "㉠은 ‘나무’가 자음으로 시작하는 조사 ‘마다’와 결합한 자리이므로 ‘나모마다’가 와야 한다. 이 선지의 ㉠에는 모음 앞에서 쓰이는 형태가 놓였고, ㉡의 ‘남과’도 ‘와’ 앞에는 맞지 않는다."),
    J(5, "부적절", False, [R1, E1, E3], "자체",
      "㉠에 모음 앞에서 쓰이는 형태가 놓였는데, ‘나무’는 자음으로 시작하는 조사 ‘마다’ 앞에서 ‘나모’ 형태가 되어야 하므로 틀리다. ㉢도 ‘도’ 앞에는 모음 앞 형태가 놓였다."),
]
json.dump(d, open(HERE + r"\세트_37-39.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("세트_37-39.json 씀")
