"""문제 PDF 에서 그림·표·옛한글 조각을 잘라 낸다. 모든 조각은 이 도구로만 만든다.

사용: py -X utf8 도구/그림_자르기.py <회차ID>          예: py -X utf8 도구/그림_자르기.py 20260324-go2

- 위치는 작업/<회차ID>/그림_위치.json 에 적는다(쪽 그림을 보고 정한 값, PDF 좌표 pt):
    {"pdf": "<문제 PDF 파일 이름>", "그림": {"그림_7-10_7_사전.png": {"page": 3, "rect": [x0, y0, x1, y1]}, ...}}
- 해상도는 200dpi 로 고정하고 PNG 안에 dpi 를 적는다. 화면(기출_렌더.py)은 이 dpi 로
  원본 크기를 계산해 그림 속 글씨가 본문 글씨와 같은 크기로 보이게 한다. dpi 가 없는 그림은 게시가 멈춘다.
- 상자 테두리 선이 조각 가장자리에 걸리지 않게 rect 를 테두리 안쪽으로 잡는다.
"""
import json
import os
import sys

import fitz

DPI = 200
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    exam_id = sys.argv[1]
    work = os.path.join(ROOT, "작업", exam_id)
    pos = json.load(open(os.path.join(work, "그림_위치.json"), encoding="utf-8"))
    doc = fitz.open(os.path.join(ROOT, "원본자료", "ebsi-korean", "pdf", pos["pdf"]))
    for name, v in pos["그림"].items():
        pix = doc[v["page"] - 1].get_pixmap(dpi=DPI, clip=fitz.Rect(v["rect"]))
        pix.set_dpi(DPI, DPI)
        pix.save(os.path.join(work, name))
        print(name, pix.width, "x", pix.height)


if __name__ == "__main__":
    main()
