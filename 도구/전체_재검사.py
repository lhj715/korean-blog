"""작업\\ 아래 모든 회차의 모든 세트를 검사기로 다시 돌린다(도구를 고친 뒤 회귀 확인용).

사용: py -X utf8 도구/전체_재검사.py [회차ID 접두어 ...]   (인자 없으면 전부)
출력: 불합격만 자세히, 마지막에 «총 N개 불합격 M개».
"""
import glob
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF = os.path.join(ROOT, "원본자료", "ebsi-korean", "pdf")
BUNDLES = os.path.join(ROOT, "원본자료", "ebsi-korean", "site-ready-dataset", "bundles")


def pick(pattern):
    fs = sorted(f for f in glob.glob(os.path.join(PDF, pattern)) if "_2_" not in os.path.basename(f))
    return fs[0] if fs else None


def main():
    prefixes = sys.argv[1:]
    total = bad = 0
    for d in sorted(glob.glob(os.path.join(ROOT, "작업", "20*"))):
        exam = os.path.basename(d)
        if prefixes and not any(exam.startswith(p) for p in prefixes):
            continue
        m = re.fullmatch(r"(\d{8})-(go[12])", exam)
        m3 = re.fullmatch(r"(\d{8})-go3-(kor[AB])", exam)
        if m:
            prob = pick(f"{exam}-problem-kor_mun*.pdf")
            expl = pick(f"{exam}-explanation-kor_hsj*.pdf")
        elif m3:
            date, opt = m3.groups()
            prob = pick(f"{date}-go3-problem-{opt}*mun*.pdf")
            expl = pick(f"{date}-go3-explanation-{opt}*hsj*.pdf")
        else:
            continue
        bundle = os.path.join(BUNDLES, exam + ".json")
        for f in sorted(glob.glob(os.path.join(d, "세트_*.json"))):
            total += 1
            r = subprocess.run([sys.executable, "-X", "utf8", os.path.join(ROOT, "도구", "세트_검사.py"), f, prob, expl, bundle],
                               capture_output=True, text=True, encoding="utf-8")
            if not r.stdout.split("\n")[1:2] or not r.stdout.split("\n")[1].startswith("합격"):
                bad += 1
                print("불합격", f)
                print("\n".join(r.stdout.split("\n")[1:5]), r.stderr[-300:])
    print(f"총 {total}개 불합격 {bad}개")


if __name__ == "__main__":
    main()
