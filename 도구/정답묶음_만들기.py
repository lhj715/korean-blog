"""공식 정답표 PDF(텍스트층 있는 것)에서 go3 정답 bundle 두 개(korA·korB)를 만든다.

사용: py -X utf8 도구/정답묶음_만들기.py <날짜> [정답표 PDF 이름 일부]    예) 20250903
- 정답표 PDF: 원본자료\ebsi-korean\pdf\<날짜>-answer-live_main_answer_1_kor*.pdf (공통 1~34 + 화법과 작문 35~45 + 언어와 매체 35~45)
- 홀수형/짝수형이 둘 다 있는 시험(수능)은 문제지가 홀수형(`_1_`)이므로 홀수형 표를 쓴다.
- 이미지뿐인 정답표(텍스트층 없음)는 이 도구로 못 만든다(쪽 그림을 눈으로 읽어 직접 만든다).
만든 뒤 반드시 해설지의 정답 표기와 한 번 더 대조한다.
"""
import glob
import json
import os
import sys

import fitz

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF = os.path.join(ROOT, "원본자료", "ebsi-korean", "pdf")
BUNDLES = os.path.join(ROOT, "원본자료", "ebsi-korean", "site-ready-dataset", "bundles")
CIR = "①②③④⑤"


def main(date):
    fs = sorted(glob.glob(os.path.join(PDF, f"{date}-answer-live_main_answer_1_kor*.pdf")))
    if not fs:
        sys.exit("정답표 PDF 없음")
    t = fitz.open(fs[0])[0].get_text()
    if not t.strip():
        sys.exit("텍스트층이 없는 정답표(이미지)라 자동으로 못 만든다")
    toks = t[t.index("정답\n배점\n문항"):].split("\n") if "정답\n배점\n문항" in t else t.split("\n")
    trip = []
    i = 0
    while i < len(toks) - 2:
        if toks[i].isdigit() and toks[i + 1] and toks[i + 1] in CIR and toks[i + 2] in ("2", "3"):
            trip.append((int(toks[i]), toks[i + 1]))
            i += 3
        else:
            i += 1
    common = sorted((n, a) for n, a in trip if n <= 34)
    A, B = {}, {}
    for n, a in trip:
        if n >= 35:
            (A if n not in A else B)[n] = a
    if [n for n, _ in common] != list(range(1, 35)) or sorted(A) != list(range(35, 46)) or sorted(B) != list(range(35, 46)):
        sys.exit(f"정답표 파싱 이상: 공통 {len(common)} A {len(A)} B {len(B)}")
    ref = None
    for f in glob.glob(os.path.join(BUNDLES, "2026*-go3-korA.json")):
        ref = json.load(open(f, encoding="utf-8"))
        break
    for opt, label, S in (("korA", "화법과 작문", A), ("korB", "언어와 매체", B)):
        ans = [{"qno": n, "answer": a, "answer_number": str(CIR.index(a) + 1)} for n, a in common] + \
              [{"qno": n, "answer": S[n], "answer_number": str(CIR.index(S[n]) + 1)} for n in range(35, 46)]
        d = dict(ref)
        d.update(id=f"{date}-go3-{opt}", date=date, year=int(date[:4]), month=date[4:6], day=date[6:], option=opt, track_label=label,
                 answer_status="COMPLETE_BY_SOURCE_TABLE", answers=ans,
                 source_files={"answer": os.path.basename(fs[0]) + " (공식 정답표 PDF 텍스트층)"},
                 notes=["공식 정답표 PDF 텍스트층에서 도구/정답묶음_만들기.py 로 만듦. 해설지 정답 표기와 대조할 것."])
        out = os.path.join(BUNDLES, f"{date}-go3-{opt}.json")
        json.dump(d, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("만듦", out, len(ans))


if __name__ == "__main__":
    main(sys.argv[1])
