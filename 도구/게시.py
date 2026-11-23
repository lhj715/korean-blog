"""검사·검토를 통과한 세트만 사이트 페이지로 만든다.

사용: py -X utf8 도구/게시.py <회차ID>          예: py -X utf8 도구/게시.py 20260324-go2

관문(하나라도 걸리면 아무것도 쓰지 않고 멈춘다)
 1. 작업/<회차ID>/세트_*.json 마다 도구/세트_검사.py 합격
 2. 같은 범위의 가장 나중 독립검토 파일(독립검토_<범위>*.md)에 "최종 판정: 통과"
결과
 - static/images/exams/<회차ID>/  그림 복사
 - content/exams/<회차ID>.md      페이지 머리말(front matter)
 - data/exams/<회차ID>.json       화면 HTML (기출_렌더 출력). 두 파일 다 손으로 고치지 않는다.
"""
import glob
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from 기출_렌더 import render_set  # noqa: E402

GRADE = {"go1": "고1", "go2": "고2", "go3": "고3"}


def main():
    exam_id = sys.argv[1]
    work = os.path.join(ROOT, "작업", exam_id)
    sets = []
    for path in glob.glob(os.path.join(work, "세트_*.json")):
        s = json.load(open(path, encoding="utf-8"))
        sets.append((s["range"][0], path, s))
    if not sets:
        sys.exit(f"세트 파일이 없음: {work}")
    sets.sort()

    pdf = os.path.join(ROOT, "원본자료", "ebsi-korean", "pdf")
    bundle = os.path.join(ROOT, "원본자료", "ebsi-korean", "site-ready-dataset", "bundles", f"{exam_id}.json")
    bad = []
    for _, path, s in sets:
        m = s["meta"]
        r = subprocess.run([sys.executable, "-X", "utf8", os.path.join(HERE, "세트_검사.py"), path,
                            os.path.join(pdf, m["problem_pdf"]), os.path.join(pdf, m["explanation_pdf"]), bundle],
                           capture_output=True, text=True, encoding="utf-8")
        if r.returncode:
            bad.append(f"{os.path.basename(path)}: 프로그램 검사 불합격\n{r.stdout}")
        lo, hi = s["range"]
        reviews = sorted(glob.glob(os.path.join(work, f"독립검토_{lo}-{hi}*.md")))
        if not reviews or not re.search(r"최종 판정:\s*\**\s*통과", open(reviews[-1], encoding="utf-8").read()):
            bad.append(f"{os.path.basename(path)}: 독립 검토 통과 기록 없음 ({os.path.basename(reviews[-1]) if reviews else '파일 없음'})")
    if bad:
        print("게시 중단 — 관문 불합격:")
        print("\n".join(bad))
        sys.exit(1)

    img_dir = os.path.join(ROOT, "static", "images", "exams", exam_id)
    os.makedirs(img_dir, exist_ok=True)
    bodies = []
    for _, path, s in sets:
        names = []

        def walk(o):
            if isinstance(o, dict):
                for k, v in o.items():
                    if k in ("image", "display_image") and isinstance(v, str):
                        names.append(v)
                    else:
                        walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(s["passage"])
        walk([q.get("bogi") for q in s["questions"]])
        for n in names:
            shutil.copy2(os.path.join(os.path.dirname(path), n), os.path.join(img_dir, n))
        bodies.append(render_set(s, lambda n: f"/images/exams/{exam_id}/{n}", lambda n: os.path.join(img_dir, n)))

    m = sets[0][2]["meta"]
    date = f"{exam_id[:4]}-{exam_id[4:6]}-{exam_id[6:8]}"
    grade = GRADE.get(exam_id.split("-")[1], "")
    ranges = ", ".join(f"{s['range'][0]}~{s['range'][1]}번" for _, _, s in sets)
    fm = {
        "title": m["exam"],
        "date": date,
        "category": "학력평가" if "학력평가" in m["exam"] else ("수능" if "수능" in m["exam"] else "모의평가"),
        "grade": grade,
        "exam_id": exam_id,
        "sets": ranges,
        "summary": f"{m['exam']} 지문 근거 찾기. 선지마다 판단 근거를 지문에 표시했습니다.",
    }
    head = "---\n" + "\n".join(f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in fm.items()) + "\n---\n"
    out = os.path.join(ROOT, "content", "exams", f"{exam_id}.md")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(head)
    data = os.path.join(ROOT, "data", "exams", f"{exam_id}.json")
    os.makedirs(os.path.dirname(data), exist_ok=True)
    json.dump({"html": "\n".join(bodies)}, open(data, "w", encoding="utf-8"), ensure_ascii=False)
    print("게시 파일:", os.path.relpath(out, ROOT), "+", os.path.relpath(data, ROOT), "/ 세트", ranges, "/ 그림", len(os.listdir(img_dir)))


if __name__ == "__main__":
    main()
