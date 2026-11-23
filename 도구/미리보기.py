"""세트 JSON → 확인용 HTML 한 파일 (이 컴퓨터에서 보는 용도).

사용: py -X utf8 도구/미리보기.py <세트 JSON> <출력 HTML>
사이트와 같은 화면이 나오도록 기출_렌더.py · assets/css/exam.css · static/js/exam.js 를 그대로 쓴다.
"""
import base64
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from 기출_렌더 import render_set  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKENS = """:root{--ink:#1a1814;--ink-mid:#4a4640;--ink-soft:#8a8480;--paper:#f7f4ef;--paper-warm:#ede9e2;--paper-line:#d8d3cb;--ev:#1f5c9e}
body{margin:0;background:var(--paper);color:var(--ink);font-family:'Noto Sans KR',system-ui,sans-serif;line-height:1.75}
main{margin:0 auto;padding:24px 16px}h1{font-size:22px;margin:0 0 4px}"""


def main():
    src, dst = sys.argv[1:3]
    s = json.load(open(src, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(src))

    def img(name):
        return "data:image/png;base64," + base64.b64encode(open(os.path.join(base, name), "rb").read()).decode()

    css = open(os.path.join(ROOT, "assets", "css", "exam.css"), encoding="utf-8").read()
    js = open(os.path.join(ROOT, "static", "js", "exam.js"), encoding="utf-8").read()
    body = render_set(s, img)
    title = s.get("meta", {}).get("exam", "")
    page = (f"<!doctype html><html lang='ko'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
            f"<title>리딩맵 미리보기</title><style>{TOKENS}{css}</style></head><body><main class='xm-page'>"
            f"<h1>{title}</h1><p class='xm-meta'>미리보기</p>{body}<div class='xm-end'></div></main><script>{js}</script></body></html>")
    open(dst, "w", encoding="utf-8").write(page)
    print("ok", dst)


if __name__ == "__main__":
    main()
