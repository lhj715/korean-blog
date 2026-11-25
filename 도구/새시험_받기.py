"""EBSi 목록에서 아직 저장소에 없는 새 시험 파일(시험지·해설지·정답표)만 받는다.

사용: py -X utf8 도구/새시험_받기.py <연도> [시작 날짜 8자리 이상만]       예) py -X utf8 도구/새시험_받기.py 2026 20260501
- 목록 호출·파일 주소·저장 이름 규칙은 CLAUDE.md «시험지·해설지·정답표 받는 법» 참고.
- 저장 위치: 원본자료\\ebsi-korean\\pdf\\ (pdf), answer-images\\ (png). 이미 있는 파일은 건너뛴다.
- 호출 사이 0.2초 쉰다. 받은 파일 목록을 출력한다.
"""
import math
import re
import sys
import time
import urllib.parse
import urllib.request
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PDF_DIR = ROOT / "원본자료" / "ebsi-korean" / "pdf"
ANS_DIR = ROOT / "원본자료" / "ebsi-korean" / "answer-images"
API = "https://www.ebsi.co.kr/ebs/xip/xipc/previousPaperListAjax.ajax"
BASE = "https://wdown.ebsi.co.kr/W61001/01exam"
TARGETS = {
    "D100": ("go1", "17012", "03,04,05,06,08,09,10,11,12"),
    "D200": ("go2", "17022", "03,04,05,06,08,09,10,11,12"),
    "D300": ("go3", "140117,140118,korPast", "03,04,05,06,07,08,09,10,11,12"),
}


def clean(v):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", unescape(v))).strip()


def post(target, subj, months, years, page):
    data = {"targetCd": target, "yearList": years, "monthList": months, "arOrd": "1", "subjIdList": subj, "sort": "recent", "currentPage": str(page)}
    req = urllib.request.Request(API, data=urllib.parse.urlencode(data).encode(), headers={
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "User-Agent": "Mozilla/5.0",
        "Referer": f"https://www.ebsi.co.kr/ebs/xip/xipc/previousPaperList.ebs?targetCd={target}"})
    return urllib.request.urlopen(req, timeout=45).read().decode("utf-8", "replace")


def main(year, since="0"):
    got = []
    for target, (grade, subj, months) in TARGETS.items():
        first = post(target, subj, months, year, 1)
        m = re.search(r'<em class="tot">([^<]+)</em>', first)
        total = int(re.sub(r"\D", "", m.group(1))) if m else 0
        for page in range(1, max(1, math.ceil(total / 15)) + 1):
            html = first if page == 1 else post(target, subj, months, year, page)
            for block in re.findall(r'<div class="qus_box kor">(.*?)(?=<div class="qus_box kor">|<div class="pagination|$)', html, re.S):
                title = clean((re.search(r'<div class="qus_tit">(.*?)</div>', block, re.S) or [None, ""])[1])
                for onclick, label in re.findall(r'<button[^>]+onclick="([^"]+)"[^>]*>\s*<span>([^<]+)</span>', block, re.S):
                    a = re.search(r"\(\s*'([^']+)'", onclick)
                    if not a:
                        continue
                    url = unescape(a.group(1)).strip()
                    url = url if url.startswith("http") else BASE + ("" if url.startswith("/") else "/") + url
                    ext = Path(urllib.parse.urlparse(url).path).suffix.lower()
                    if ext not in (".pdf", ".png", ".jpg", ".jpeg"):
                        continue
                    lab = clean(label)
                    kind = "problem" if lab == "문제" else "explanation" if lab == "해설" else "answer" if ("정답" in lab or re.search(r"_scr(?:_[0-9]+)?\.pdf$", url)) else "other"
                    date = (re.search(r"/01exam/(\d{8})/", url) or [None, ""])[1]
                    if not date or date < since:
                        continue
                    name = re.sub(r"\s+", " ", re.sub(r'[\\/:*?"<>|]+', "-", f"{date}-{grade}-{kind}-{Path(urllib.parse.urlparse(url).path).name}")).strip()
                    dest = (PDF_DIR if ext == ".pdf" else ANS_DIR) / name
                    if dest.exists():
                        continue
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    data = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read()
                    dest.write_bytes(data)
                    ok = data.startswith(b"%PDF-") if ext == ".pdf" else data.startswith(b"\x89PNG") if ext == ".png" else True
                    got.append((name, len(data), ok, title))
                    time.sleep(0.2)
            time.sleep(0.2)
    for n, b, ok, t in got:
        print(("OK " if ok else "BAD"), n, b, t)
    print("받은 파일", len(got))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "0")
