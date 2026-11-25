"""세트 JSON 통과 관문. 하나라도 어기면 불합격(종료 코드 1)이고, 불합격 세트는 사이트에 올리지 않는다.

사용: py -X utf8 도구/세트_검사.py <세트 JSON> <문제PDF> <해설PDF> <정답 bundle JSON>

검사 항목(번호는 보고서에 그대로 찍힌다)
 A1 문항 번호가 범위와 맞고 연속이다          A2 문항마다 선지 5개, 빈 선지 없음
 A3 배점 2/3, 3점 표시가 PDF 와 일치            A4 지문 항목 종류는 para/verse/label/note/omit/heading/figure 만
 B1 지문·발문·선지·상자 글자가 PDF 텍스트층과 일치(공백 무시)
 B2 그림 글자·보기 머리말·쪽 머리글·선지 기호가 지문·발문·선지에 섞이지 않음
 B3 빠짐 없음(선지 번호는 글 앞·뒤 어느 쪽이든, 마지막 문항 뒤 «확인 사항» 안내는 구역 밖): PDF 의 지문·문항 구역 글자가 등록한 조각으로 남김없이 설명된다
    (그림·표 속 글자는 그림 항목의 pdf_text, 구간 표시 [A] 등은 ranges 의 mark)
 C1 밑줄 범위가 항목 글 안에 그대로 있고 기호 바로 뒤에 온다
 C2 발문·선지에 나오는 ㉠·ⓐ·[A] 등 기호가 지문에서 밑줄·구간으로 등록됨(상자 안 기호·글 속 빈칸 [가] 는 예외)
 C3 등록한 밑줄 범위가 PDF 에 실제로 그어진 밑줄(선 그림)과 글자 단위로 같다(no_line 표시는 쪽 그림으로 확인한 경우만)
 C4 구간 표시([A] 등)가 가리키는 항목·글이 지문에 있다
 C5 굵은 글씨(bold: [글자 그대로])가 항목 글 안에 있다
 C6 선지 밑줄(choice_underlines: {"선지번호": [글자 그대로]})이 그 선지 글 안에 있다
 C7 display_image(쪽에서 잘라 낸 그림으로 대신 보여 주기)는 옛한글 PUA 글자가 든 항목에만
 C9 PDF 에 밑줄이 그어진 글자가 선지에만 있으면 choice_underlines 에 등록(같은 쪽만 봄). 발문 밑줄 빠짐은 알림
 (굵은 글씨는 PDF 에서 낱말 조각으로만 읽혀 자동 검사가 오탐투성이라 독립 검토자가 쪽 그림으로 확인한다)
 C8 choices_in_box(계획표처럼 선지가 상자 항목으로 찍힌 문항)면 선지 글과 번호가 상자 글 안에 있다
 D1 정답 = 정답표                              D2 판단 5개, 정답 표시 1개 = 정답
 D3 판단 말(적절/부적절, 일치/불일치)이 발문 방향과 맞다
 E1 모든 선지에 근거가 1개 이상
 E2 근거 인용이 글자 그대로 있다: passage(para=지문 항목 id) / bogi(그 문항 상자 글) / figure(fig=그림 id, 그 그림의 pdf_text)
 E3 해설지 기반 판단은 해설지 인용이 그 문항 해설 안에 글자 그대로 있다
 E4 이유가 비어 있지 않고 금지 문자(em dash)가 없다
 R  해설지에 없는 선지(근거=자체)는 별도 검토자 확인이 필요한 목록으로 보고한다(불합격 사유는 아님)

세트 데이터 구조는 CLAUDE.md 5절 «세트 데이터 구조».
"""
import json
import re
import sys

import fitz

HEADER = re.compile(r"^(\d+|국어\s*영역(?:\s*\([^)]*\))?|고[123]|홀수형|짝수형|\d{4}학년도 .*문제지\s*\d*|제\s*\d\s*교시\s*\d*|이 문제지에 관한 저작권은 한국교육과정평가원에 있습니다\.|\(화법과 작문\)|\(언어와 매체\)|<\s*>|━+|고[123]\s+\d+|\d+\s+고[123])$")
MARKS = "㉠㉡㉢㉣㉤㉥㉦㉧㉮㉯㉰㉱㉲ⓐⓑⓒⓓⓔⓕⓖ"
NEG = {"부적절", "불일치", "미반영", "틀림", "확인 불가"}
POS = {"적절", "일치", "반영", "맞음", "확인 가능"}
TEXT_TYPES = {"para", "verse", "label", "note", "omit", "heading"}
CIRS = "①②③④⑤"
COMMON_NEG = {"않은", "않는", "없는", "아닌", "않다"}  # 발문 강조 밑줄로 흔한 말: 같은 쪽 다른 발문과 헷갈려 선지 검사에서 뺀다


TEXTLAYER_SUBS = {}  # 세트 meta.textlayer_subs: PDF 텍스트층이 한자를 엉뚱한 한글로 읽은 곳({"靑": "복", "輸": "드"}). 데이터에는 쪽 그림대로 한자를 쓰고, 검사는 같게 본다


def squash(s):
    for _k, _v in TEXTLAYER_SUBS.items():
        s = s.replace(_k, _v)
    # 겹낫표 『 』 는 PDF 텍스트층에서 사용자 정의 글자(U+F000)로 나온다. 같게 본다. 폭 없는 공백(U+200B)은 공백으로 본다
    return re.sub(r"[\s​]+", "", s.replace("靑", "복").replace("뺷", "").replace("뺸", "").replace("『", "").replace("』", "").replace("∼", "~").replace("～", "~"))


def pdf_text(path):
    out = []
    for page in fitz.open(path):
        out += [l for l in page.get_text("text").split("\n") if not HEADER.match(l.strip())]
    return "\n".join(out)


def underlined_runs(path, with_page=False):
    """PDF 에 선으로 그려진 밑줄 위 글자를 읽는 순서(쪽 → 단 → 위아래 → 좌우)대로 돌려준다."""
    runs = []
    for pno, page in enumerate(fitz.open(path)):
        half = page.rect.width / 2
        segs = []
        for dr in page.get_drawings():
            for it in dr["items"]:
                if it[0] == "l" and abs(it[1].y - it[2].y) < 0.6 and abs(it[2].x - it[1].x) > 3:
                    segs.append((min(it[1].x, it[2].x), max(it[1].x, it[2].x), it[1].y))
                elif it[0] == "re" and it[1].height < 1.2 and it[1].width > 3:
                    segs.append((it[1].x0, it[1].x1, it[1].y1))
        # 쪽 가운데 아래 쪽번호 상자(윗변·아랫변 두 선, 쪽 가운데에 놓임)는 밑줄이 아니다
        mid = page.rect.width / 2
        segs = [s for s in segs
                if not (abs((s[0] + s[1]) / 2 - mid) < 3 and s[2] > page.rect.height * 0.88
                        and any(o is not s and abs(o[0] - s[0]) < 1 and abs(o[1] - s[1]) < 1 and 10 < abs(o[2] - s[2]) < 30 for o in segs))]
        chars = [(c["c"], fitz.Rect(c["bbox"])) for b in page.get_text("rawdict")["blocks"]
                 for l in b.get("lines", []) for sp in l["spans"] for c in sp["chars"]]
        seen = set()
        for x0, x1, y in segs:
            # 글자 가운데가 선 위에 있으면 밑줄 글자로 본다(선이 마지막 글자보다 1pt 남짓 짧게 끝나는 PDF 가 있다)
            # 선이 글자 아랫변보다 아주 조금(소수점) 위에 그어진 PDF 가 있고, 위첨자 '*'(각주 표시)는 아랫변이 선보다 훨씬 위다
            t = squash("".join(c for c, r in chars if x0 - 0.5 <= (r.x0 + r.x1) / 2 <= x1 + 0.5
                               and -1.2 <= y - r.y1 < (9 if c == "*" else 4)))
            key = (round(x0), round(y))
            if t and key not in seen:
                seen.add(key)
                runs.append(((pno, x0 >= half, round(y), x0), t))
    return [t for _, t in sorted(runs)] if not with_page else [(k[0], t) for k, t in sorted(runs)]


def boxes(q):
    """문항의 상자(<보기>·<자료>·계획표 등) 목록. bogi 는 dict 하나 또는 list."""
    b = q.get("bogi")
    if not b:
        return []
    return b if isinstance(b, list) else [b]


def box_items(box):
    """상자 안 항목: blocks 가 있으면 그대로, 없으면 paras + figure(s) 로 만든다."""
    if box.get("blocks"):
        return box["blocks"]
    items = [{"id": f"b{k+1}", "type": "para", "text": t} for k, t in enumerate(box.get("paras", []))]
    figs = box.get("figures") or ([box["figure"]] if box.get("figure") else [])
    items += [dict(f, type="figure", id=f.get("id", f"bf{k+1}")) for k, f in enumerate(figs)]
    return items


def main():
    set_path, prob_pdf, expl_pdf, bundle_path = sys.argv[1:5]
    s = json.load(open(set_path, encoding="utf-8"))
    TEXTLAYER_SUBS.update(s.get("meta", {}).get("textlayer_subs", {}))
    src = pdf_text(prob_pdf)
    src_sq = squash(src)
    expl = pdf_text(expl_pdf)
    answers = {int(a["qno"]): int(a["answer_number"]) for a in json.load(open(bundle_path, encoding="utf-8"))["answers"]}

    fails, review = [], []

    def fail(code, where, msg):
        fails.append(f"[{code}] {where}: {msg}")

    lo, hi = s["range"]
    qs = s["questions"]
    texts_p = {p["id"]: p for p in s["passage"] if p["type"] in TEXT_TYPES}
    figs_p = {p["id"]: p for p in s["passage"] if p["type"] == "figure"}
    for p in s["passage"]:
        if p["type"] not in TEXT_TYPES | {"figure"}:
            fail("A4", f"지문 {p.get('id')}", f"모르는 항목 종류 «{p['type']}»")
    ranges = s.get("ranges", [])

    # A
    if [q["no"] for q in qs] != list(range(lo, hi + 1)):
        fail("A1", "세트", f"문항 번호 {[q['no'] for q in qs]} != {lo}~{hi}")
    for q in qs:
        w = f"{q['no']}번"
        if len(q["choices"]) != 5 or any(not c.strip() for c in q["choices"]):
            fail("A2", w, f"선지 {len(q['choices'])}개 또는 빈 선지")
        if not q.get("stem", "").strip():
            fail("A2", w, "발문이 비어 있음")
        if q["points"] not in (2, 3):
            fail("A3", w, "배점이 2/3 이 아님")
        m = re.search(rf"(^|\n)　?{q['no']}\.\s(.{{0,3000}}?)(\n①|①|\n　?{q['no']+1}\.\s)", src, re.S)  # 선지가 그림뿐인 문항은 다음 문항 번호에서 끊는다(2025학년도 수능 39번)
        has3 = bool(m and "[3점]" in m.group(2))
        if has3 != (q["points"] == 3):
            fail("A3", w, f"3점 표시 불일치(PDF {'있음' if has3 else '없음'})")

    # 빈칸(blank) 글자 [가] 가 텍스트층에서 화자 줄과 떨어져 쪽 끝에 찍힌 PDF(2026-06 고2 6번): 글은 빈칸을 뺀 채 대조하고, 빈칸 글자는 구간 표시처럼 남은 글자에서 찾는다
    blank_marks, body = [], {}
    for p in texts_p.values():
        body[p["id"]] = p["text"]
        b = p.get("blank")
        if b and p["text"].rstrip().endswith(b) and squash(p["text"]) not in src_sq:
            body[p["id"]] = p["text"].rstrip()[:-len(b)]
            blank_marks.append({"mark": b})

    # B1·B2
    texts = [(f"지문 {p['id']}", body[p["id"]], True) for p in texts_p.values()]
    for q in qs:
        texts.append((f"{q['no']}번 발문", q["stem"], True))
        if q.get("sub_guide"):
            texts.append((f"{q['no']}번 작은 안내문", q["sub_guide"], False))
        if q.get("choices_raster"):
            # 선지가 PDF 에 글자 없이 그림(표)으로만 있는 문항: 선지 글은 그 문항 그림의 raster_text 에 글자 그대로 있어야 한다
            rt = squash(" ".join((it.get("pdf_text", "") + " " + it.get("raster_text", "")) for box in boxes(q) for it in box_items(box) if it["type"] == "figure"))
            for i, c in enumerate(q["choices"]):
                if squash(c) not in rt:
                    fail("B1", f"{q['no']}번 {CIRS[i]}", "choices_raster 인데 선지 글이 그림 raster_text 에 없음")
        else:
            texts += [(f"{q['no']}번 {CIRS[i]}", c, True) for i, c in enumerate(q["choices"])]
        for bi, box in enumerate(boxes(q)):
            texts += [(f"{q['no']}번 상자{bi+1} {it['id']}", it["text"], False) for it in box_items(box) if it["type"] in TEXT_TYPES]
    for where, t, strict in texts:
        if squash(t) not in src_sq:
            sq = squash(t)
            k = len(sq)
            while k > 0 and sq[:k] not in src_sq:
                k -= 10
            fail("B1", where, f"PDF 와 다름 — {max(k,0)}자째 근처: «{sq[max(k,0):max(k,0)+25]}»")
        if strict and re.search(r"<\s*그\s*림\s*>(?![가-힣])|<\s*보\s*기\s*>(?![가-힣]|\s*모두(?![가-힣]))|-{4,}|\+{4,}|===|[①②③④⑤]|확인\s*사항|답안지", t):
            fail("B2", where, "그림 글자·보기 머리말·쪽 머리글·선지 기호가 섞임")

    # B3 빠짐 없음
    deferred = []  # 그림 속 글자는 텍스트층에서 쪽 끝 등 다른 자리에 찍히기도 해서, 구역에 없으면 남은 글자 전체에서 찾는다

    def cut(region, pieces, where):
        for name, piece in pieces:
            sq = squash(piece)
            if not sq:
                continue
            k = region.find(sq)
            if k < 0:
                if sq.isdigit():  # 숫자만 있는 줄(연 번호 1·2·3)은 쪽 번호 필터(HEADER)가 지워 PDF 글자에 없다(2025-06 고3 31~34번)
                    continue
                if name.startswith("그림:") or name.startswith("상자"):  # 계획표 등 상자 글이 다음 문항 구역·쪽 끝에 찍히는 PDF(2025-10 고1 2번)
                    deferred.append((name, sq, where))
                elif name.startswith("선지") and len(sq) >= 12 and sq in src_sq:  # 선지 ①~⑤ 가 다음 세트 지문 뒤에 찍히는 PDF(2026-07 고3 17번): 번호+글이 PDF 에 이어져 있으면 인정
                    deferred.append((name, sq, where))
                else:
                    fail("B3", where, f"«{name}» 조각을 PDF 구역에서 찾지 못함")
                continue
            region = region[:k] + region[k + len(sq):]
        return region

    starts = []
    pos = 0
    g = -1
    if s.get("guide"):
        g = src_sq.find(squash(s["guide"]))
        if g < 0:
            fail("B3", "세트", "안내문을 PDF 에서 찾지 못함")
        pos = max(g, 0)
    for q in qs:
        if q.get("sub_guide"):
            # 문항 사이 작은 안내문([13 ~ 14] <보기>는 …)과 공용 상자는 그 문항 번호보다 앞에 찍힌다
            k = src_sq.find(squash(q["sub_guide"]), pos)
            starts.append(k)
            pos = max(k, pos)
            continue
        k = src_sq.find(f"{q['no']}." + squash(q["stem"])[:12], pos)
        starts.append(k)
        pos = max(k, pos)
    if min(starts) < 0:
        fail("B3", "세트", f"문항 시작 위치를 찾지 못함 {starts}")
    else:
        nxt = [m.start() for m in re.finditer(r"\[\d+~\d+\]", src_sq) if m.start() > starts[-1]]
        nq = [m.start() for m in re.finditer(rf"(?<!\d){hi+1}\.", src_sq) if m.start() > starts[-1]]
        notice = [m.start() for m in re.finditer(r"[*＊※]?확인사항", src_sq) if m.start() > starts[-1]]
        end = min(nxt[:1] + nq[:1] + notice[:1] + [len(src_sq)])
        leftovers = []
        if s.get("guide") and g >= 0:
            region = src_sq[g + len(squash(s["guide"])): starts[0]]
            # 텍스트층 순서가 «지문 → 문항 → * 확인 사항 → 지문 나머지(다음 쪽)» 로 뒤섞인 PDF: 확인 사항 문구 뒤 ~ 다음 안내문 앞을 지문 구역에 합친다
            if notice and end == notice[0]:  # 이 세트 끝에서 처음 만나는 게 확인 사항일 때만
                tail0 = src_sq.find("확인하시오.", notice[0])
                if tail0 >= 0:
                    tail0 += len("확인하시오.")
                    after = [m.start() for m in re.finditer(r"\[\d+~\d+\]", src_sq) if m.start() >= tail0]
                    tail = src_sq[tail0: after[0] if after else len(src_sq)]
                    # 다음 선택과목 안내문(「선택과목(…)」문제가제시되오니 …확인하시오.)은 지문이 아니다
                    tail = re.sub(r"이어서,?[「｢]선택과목\([^)]*\)[」｣]문제가제시되오니,?자신이선택한과목인지확인하시오\.", "", tail)
                    tail = re.sub(r"[*＊]?확인사항◦?답안지의해당란에필요한내용을정확히기입\(표기\)했는지확인하시오\.", "", tail)  # 마지막 쪽에 안내가 두 번 찍히는 PDF(2025-11 수능)
                    region += tail
            pieces = [(p["id"] if p["type"] in TEXT_TYPES else "그림:" + p["id"], body[p["id"]] if p["type"] in TEXT_TYPES else p.get("pdf_text", "")) for p in s["passage"]]
            leftovers.append(("지문 구역", cut(region, pieces, "지문 구역")))
        for i, q in enumerate(qs):
            region = src_sq[starts[i]: starts[i + 1] if i + 1 < len(qs) else end]
            pieces = [("작은 안내문", q.get("sub_guide", "")), ("번호", f"{q['no']}."), ("발문", q["stem"])]
            if q["points"] == 3:
                pieces.append(("[3점]", "[3점]"))
            for bi, box in enumerate(boxes(q)):
                pieces.append((f"상자{bi+1} 머리말", box.get("label", "")))
                for it in box_items(box):
                    pieces.append(((f"상자{bi+1} " if it["type"] in TEXT_TYPES else "그림:") + it["id"], it["text"] if it["type"] in TEXT_TYPES else it.get("pdf_text", "")))
            for k, c in enumerate(q["choices"] if not (q.get("choices_in_box") or q.get("choices_raster")) else []):
                before, after = CIRS[k] + squash(c), squash(c) + CIRS[k]
                pieces.append((f"선지 {CIRS[k]}", before if before in region or after not in region else after))
            leftovers.append((f"{q['no']}번 구역", cut(region, pieces, f"{q['no']}번 구역")))
        # 구간 표시([A] 등)는 PDF 에서 쪽 끝 등 엉뚱한 자리에 찍히므로 남은 글자에서 한 번씩 지운다
        rest = "".join(r for _, r in leftovers)
        for name, sq, where in deferred:
            k = rest.find(sq)
            if k < 0:
                # <보기> 상자 글이 이웃 세트 구역에 찍힌 PDF(2024-09 고2 9번 <보기> 가 11~12번 지문 한가운데에 찍힘)는 PDF 전체에서 찾는다
                if sq not in src_sq:
                    fail("B3", where, f"«{name[3:] if name.startswith('그림:') else name}» 글자를 PDF 구역에서 찾지 못함")
            else:
                rest = rest[:k] + rest[k + len(sq):]
        for rg in ranges + blank_marks:
            mk = squash(rg["mark"])
            k = rest.find(mk)
            if k < 0:
                # 구간 표시가 안내문 앞(쪽 머리 자리)에 찍히는 PDF(2025-09 고2 38~42번)는 이 세트 구역 밖에 있다
                if mk not in src_sq:  # 쪽 끝에 찍힌 [A] 가 이웃 세트 구역에 들어간 PDF(2025학년도 수능 35~36번)
                    fail("B3", "구간", f"구간 표시 «{rg['mark']}» 를 PDF 남은 글자에서 찾지 못함")
            else:
                rest = rest[:k] + rest[k + len(mk):]
        # 이웃 세트 지문의 구간 표시([A] 등)가 이 세트 구역 끝에 찍혀 나온 것은 빠진 글자가 아니다(2025-09 고2 12~15·34~37번)
        rest = re.sub(r"\[[A-E]\]", "", rest)
        if ranges:  # 구간 표시의 꺾쇠 선이 텍스트층에 «ㅣ» 조각으로 찍힌다(2025-03 고3 38~42번)
            rest = rest.replace("ㅣ", "")
        rest = rest.replace(CIRS, "", 1)  # 쪽 끝 선지 기호 한 벌(①②③④⑤)이 지문 구역 한가운데 찍힌 PDF(2024-09 고3 43~45번 3문단 «하고/싶어도» 사이)
        rest = rest.replace("◦", "").replace("<>", "")  # <보 기> 머리말의 꺾쇠(2025-11 수능 텍스트층은 꺾쇠째 찍힘)  # 메모·계획표의 글머리 기호는 장식이라 세지 않는다
        if rest and set(rest) == {"("}:  # 2025-04 평가원 텍스트층은 <보 기>·<학습 활동> 꺾쇠를 «(» 한 글자로 찍는다
            rest = ""
        if rest:  # 이웃 세트의 <보기> 글자가 이 세트 구역 안에 찍힌 것은 같은 폴더의 다른 세트 글자와 대조해 지운다(2024-09 고2 11~12번)
            import glob, os
            sib = ""
            for sp in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(set_path)), "세트_*.json"))):
                if os.path.abspath(sp) == os.path.abspath(set_path):
                    continue
                try:
                    sj = json.load(open(sp, encoding="utf-8"))
                except Exception:
                    continue
                parts = [(it.get("text", "") or it.get("pdf_text", "")) + it.get("raster_text", "") for it in sj.get("passage", [])]
                for sq_ in sj.get("questions", []):
                    parts.append(sq_.get("stem", ""))
                    for bx in boxes(sq_):
                        parts.append(bx.get("label", ""))
                        parts += [(it.get("text", "") or it.get("pdf_text", "")) + it.get("raster_text", "") for it in box_items(bx)]
                    parts += sq_.get("choices", [])
                    parts += [CIRS[ci] + c for ci, c in enumerate(sq_.get("choices", [])[:5])]  # 이웃 세트 선지가 번호째 이 세트 구역에 찍힌 PDF(2026-07 고3 17번 → 18~21번 지문)
                sib += squash("".join(parts)).replace("<", "").replace(">", "")
            rest = rest.replace("<", "").replace(">", "")
            while rest:
                n = len(rest)
                while n >= 8 and rest[:n] not in sib:
                    n -= 1
                if n < 8:
                    break
                rest = rest[n:]
        if rest:
            where = ", ".join(w for w, r in leftovers if r)
            fail("B3", where, f"등록되지 않은 PDF 글자가 남음: «{rest[:50]}»")

    # C 밑줄·구간
    marks = set()
    box_text_items = [it for q in qs for box in boxes(q) for it in box_items(box) if it["type"] in TEXT_TYPES]
    ul_items = list(texts_p.values()) + box_text_items
    for p in ul_items:
        for u in p.get("underlines", []):
            marks.add(u["mark"])
            # 기호와 밑줄 사이에 여는 따옴표가 선 없이 놓인 꼴(㉣“엄마 …, 2026-06 고1 35~38번)은 따옴표 하나를 건너뛴 것도 «바로 뒤» 로 본다
            seps = ("", " ", "“", "‘") if u["mark"] else ("", " ")
            if all((u["mark"] + sep + u["text"]) not in p["text"] for sep in seps):
                fail("C1", f"{p['id']}", f"밑줄 {u['mark']} «{u['text']}» 이 기호 바로 뒤에 없음")
    for p in ul_items:
        for key, word in (("bold", "굵은 글씨"), ("boxed", "네모 친 글자")):
            for bt in p.get(key, []):
                t, n = (bt, 1) if isinstance(bt, str) else (bt.get("text", ""), bt.get("nth", 1))
                if not t or p["text"].count(t) < n:
                    fail("C5", f"{p['id']}", f"{word} «{t[:20]}»({n}번째) 가 항목 글에 없음")
    for q in qs:
        if any(t not in q["stem"] for t in q.get("stem_underlines", []) + q.get("stem_boxed", [])):
            fail("C6", f"{q['no']}번", f"발문 밑줄·네모 {q.get('stem_underlines')} {q.get('stem_boxed')} 이 발문 글에 없음")
        if q.get("choices_in_box"):
            # 계획표처럼 선지가 상자 안 항목으로 찍힌 문항: 선지 글은 상자 글 안에 있어야 하고, 번호 ①~⑤ 도 상자 글에 있어야 한다
            bt = squash(" ".join(it["text"] for box in boxes(q) for it in box_items(box) if it["type"] in TEXT_TYPES))
            for k, c in enumerate(q["choices"]):
                if squash(c) not in bt or CIRS[k] not in bt:
                    fail("C8", f"{q['no']}번 {CIRS[k]}", "choices_in_box 인데 선지 글·번호가 상자 글에 없음")
        for k, lst in (q.get("choice_underlines") or {}).items():
            if not k.isdigit() or not 1 <= int(k) <= 5 or any(t not in q["choices"][int(k) - 1] for t in lst):
                fail("C6", f"{q['no']}번", f"선지 밑줄 {k}: {lst} 이 선지 글에 없음")
    for q in qs:
        for k, lst in (q.get("choice_images") or {}).items():
            for ci in lst:
                ok7 = k.isdigit() and 1 <= int(k) <= 5 and (len(ci.get("text", "")) == 1 or ci.get("text") == "‘ ’") and (("" <= ci["text"] <= "") or ci["text"] == "‘ ’") and ci["text"] in q["choices"][int(k) - 1]
                if not ok7 and ci.get("plain") and k.isdigit() and 1 <= int(k) <= 5 and len(ci.get("text", "")) == 1 and ci["text"] in q["choices"][int(k) - 1]:
                    ok7 = True  # plain: 텍스트층에서 일반 한글로 읽힌 옛한글(예: ㅿ 이 든 글자가 «틀»)을 그림으로 대신 보일 때(검토자가 쪽 그림 확인)
                if not ok7:
                    fail("C7", f"{q['no']}번 선지 {k}", "choice_images 의 text 는 그 선지에 든 옛한글 PUA 글자 하나여야 함")
    for p in ul_items:
        if p.get("display_image") and not re.search("[-]", p["text"]) and not re.search(r"‘\s+’", p["text"]) and not p.get("blank_hangul"):
            fail("C7", f"{p['id']}", "display_image 는 화면에서 깨지는 글자(옛한글 PUA)가 있는 항목에만 쓴다")
    for rg in ranges:
        marks.add(rg["mark"])
        if "paras" in rg:
            for pid in rg["paras"]:
                if pid not in texts_p:
                    fail("C4", "구간", f"{rg['mark']} 의 항목 {pid} 가 지문에 없음")
        elif rg.get("para") not in texts_p or not rg.get("text") or rg["text"] not in texts_p[rg["para"]]["text"]:
            fail("C4", "구간", f"{rg['mark']} «{rg.get('text', '')[:20]}» 이 {rg.get('para')} 에 없음")
    runs = underlined_runs(prob_pdf)
    for p in ul_items:
        for u in p.get("underlines", []):
            if u.get("no_line"):
                continue
            want = squash(u["text"])
            ok = False
            for i in range(len(runs)):
                acc = ""
                for r in runs[i:]:
                    acc += r
                    if acc == want:
                        ok = True
                    if len(acc) >= len(want):
                        break
                if ok:
                    break
            if not ok:
                fail("C3", f"{p['id']}", f"밑줄 {u['mark']} «{u['text']}» 이 PDF 에 그어진 밑줄 범위와 다름")
    stem_text = " ".join([q["stem"] for q in qs] + [c for q in qs for c in q["choices"]])
    used = set(re.findall(f"[{MARKS}]", stem_text)) | set(re.findall(r"\[[A-Z]\]", stem_text))
    # 그림 속 글자([A]·㉠ 꼬리표 등)도 기호가 있는 자리로 친다
    passage_text = " ".join([p["text"] for p in texts_p.values()] + [(f.get("pdf_text", "") + " " + f.get("raster_text", "")).strip() for f in figs_p.values()])
    box_text = " ".join([it["text"] for it in box_text_items] + [(it.get("pdf_text", "") + " " + it.get("raster_text", "")).strip() for q in qs for box in boxes(q) for it in box_items(box) if it["type"] == "figure"])
    # 발문 안에서 이름을 붙인 기호('화이트[A]'처럼 낱말 바로 뒤에 붙은 [A])는 지문 구간이 아니다
    defined = set(re.findall(r"[가-힣A-Za-z)](\[[A-Z]\])", " ".join(q["stem"] for q in qs)))
    for m in sorted(used - marks - defined):
        if m.startswith("["):
            ok = m in passage_text or m in box_text
        else:
            # 지문 글에는 없고(밑줄로 등록), 상자 안 또는 지문 그림 속 꼬리표로만 있는 기호는 예외
            plain_p = " ".join(p["text"] for p in texts_p.values())
            fig_p = " ".join((f.get("pdf_text", "") + " " + f.get("raster_text", "")).strip() for f in figs_p.values())
            ok = m not in plain_p and (m in box_text or m in fig_p)
        if not ok:
            fail("C2", "세트", f"{m} 이 발문·선지에 나오는데 지문의 밑줄·구간으로 등록되지 않음")

    # C9: PDF 에 밑줄이 그어진 글자가 선지에만 나오면(지문·상자에는 없음) choice_underlines 에 등록돼 있어야 한다
    #     발문 밑줄(예: '않은')이 빠진 것은 알림만 한다
    plain = squash(passage_text + box_text)
    notes = []
    page_runs = underlined_runs(prob_pdf, with_page=True)
    page_sq = [squash(pg.get_text("text")) for pg in fitz.open(prob_pdf)]
    # 같은 글자의 밑줄이 PDF 전체에서 등록된 선지 밑줄 수보다 많을 때만 «등록 빠짐» 으로 본다(같은 쪽 다른 문항의 밑줄과 헷갈리지 않게)
    from collections import Counter
    ul_total = Counter(t for _, t in page_runs)
    reg_total = Counter(squash(t) for q in qs for lst in (q.get("choice_underlines") or {}).values() for t in lst)
    # 같은 폴더의 다른 세트에 등록된 밑줄(같은 쪽에 두 세트가 걸칠 때 그쪽 밑줄을 이 세트 선지로 오인하지 않게)
    import glob as _glob, os as _os
    def _ul_texts(o, out):
        if isinstance(o, dict):
            for kk, vv in o.items():
                if kk == "underlines" and isinstance(vv, list):
                    out.update(squash(u.get("text", "")) for u in vv if isinstance(u, dict))
                elif kk in ("choice_underlines", "stem_underlines"):
                    vals = vv.values() if isinstance(vv, dict) else [vv]
                    for lst in vals:
                        out.update(squash(t) for t in lst)
                else:
                    _ul_texts(vv, out)
        elif isinstance(o, list):
            for vv in o:
                _ul_texts(vv, out)
    other_ul = set()
    for _sp in _glob.glob(_os.path.join(_os.path.dirname(_os.path.abspath(set_path)), "세트_*.json")):
        if _os.path.abspath(_sp) != _os.path.abspath(set_path):
            try:
                _ul_texts(json.load(open(_sp, encoding="utf-8")), other_ul)
            except Exception:
                pass
    for q in qs:
        cu = q.get("choice_underlines") or {}
        # 이 문항의 발문·선지가 찍힌 쪽의 밑줄만 본다(다른 쪽의 같은 글자 밑줄과 헷갈리지 않게)
        keys = [squash(q["stem"])[:12]] + [squash(c)[:12] for c in q["choices"]]
        pages = {i for i, t in enumerate(page_sq) for k in keys if k and k in t}
        q_runs = {t for pno, t in page_runs if pno in pages}
        for k, c in enumerate(q["choices"]):
            reg = "".join(squash(t) for t in cu.get(str(k + 1), []))
            for r in q_runs:
                if len(r) >= 2 and r not in COMMON_NEG and r in squash(c) and r not in plain and r not in reg and ul_total[r] > reg_total[r] and not (any(r in o for o in other_ul) and ul_total[r] <= reg_total[r] + 1) and not q.get("table_border"):  # table_border: 선지 표 칸 테두리가 밑줄로 읽히는 문항(검토자가 쪽 그림으로 확인)
                    fail("C9", f"{q['no']}번 {CIRS[k]}", f"PDF 에 밑줄이 그어진 «{r}» 가 선지에 있는데 choice_underlines 에 없음")
        su = "".join(squash(t) for t in q.get("stem_underlines", []))
        for r in q_runs:
            if len(r) >= 2 and r in squash(q["stem"]) and r not in plain and r not in su:
                notes.append(f"{q['no']}번 발문 «{r}»")
    if notes:
        review.append("(알림) 발문 밑줄 확인: " + ", ".join(sorted(set(notes))))

    # D, E
    for q in qs:
        w = f"{q['no']}번"
        ans = answers.get(q["no"])
        if q["answer"] != ans:
            fail("D1", w, f"정답 {q['answer']} != 정답표 {ans}")
        js = q["judgments"]
        if sorted(j["choice"] for j in js) != [1, 2, 3, 4, 5]:
            fail("D2", w, "판단이 선지 1~5 에 하나씩 있지 않음")
            continue
        picked = [j["choice"] for j in js if j["is_answer"]]
        if picked != [q["answer"]]:
            fail("D2", w, f"정답 표시 {picked} != 정답 {q['answer']}")
        negative = bool(re.search(r"(않은|않는|없는|틀린|적절하지|아닌)", q["stem"]))
        for j in js:
            v = j["verdict"]
            want = (NEG if negative else POS) if j["is_answer"] else (POS if negative else NEG)
            if v not in want:
                fail("D3", f"{w} {CIRS[j['choice']-1]}", f"판단 «{v}» 이 발문 방향과 안 맞음(기대: {'/'.join(sorted(want))})")
        # 선택과목 해설 PDF 는 화작·언매 해설이 같은 번호로 두 벌 들어 있다: 언어와 매체는 뒤의 것, 그 밖에는 앞의 것
        secs = list(re.finditer(rf"(^|\n)[ \t]*{q['no']}\.?\s*\[출제 ?의도\](.*?)(?=\n[ \t]*{q['no']+1}\.?\s*\[출제 ?의도\]|\n\[\d+\s*[~～∼]\s*\d+\]|\Z)", expl, re.S))
        if not secs:  # 2025-11 수능 해설지: «N. 제목» 다음 줄에 «정답해설 :» 이 오는 형식
            secs = list(re.finditer(rf"(^|\n){q['no']}\.\s*([가-힣 ·・,:.\-–\[\]]*\n.*?)(?=\n{q['no']+1}\.\s*[가-힣]|\n\[\d+\s*[~～∼]\s*\d+\]|\Z)", expl, re.S))
        sec = (secs[-1] if "언어와 매체" in s.get("meta", {}).get("exam", "") else secs[0]) if secs else None
        sec_sq = squash(sec.group(2)) if sec else ""
        if not sec:
            fail("E3", w, "해설지에서 이 문항 해설을 찾지 못함")
        q_texts = [it["text"] for box in boxes(q) for it in box_items(box) if it["type"] in TEXT_TYPES]
        q_figs = {it["id"]: (it.get("pdf_text", "") + " " + it.get("raster_text", "")).strip() for box in boxes(q) for it in box_items(box) if it["type"] == "figure"}
        q_figs.update({f["id"]: (f.get("pdf_text", "") + " " + f.get("raster_text", "")).strip() for f in figs_p.values()})
        for j in js:
            ww = f"{w} {CIRS[j['choice']-1]}"
            if not j.get("evidence"):
                fail("E1", ww, "근거 없음")
            for e in j.get("evidence", []):
                if e["source"] == "passage":
                    p = texts_p.get(e["para"])
                    if not p or e["quote"] not in p["text"]:
                        fail("E2", ww, f"인용 «{e['quote'][:30]}» 이 {e['para']} 에 글자 그대로 없음")
                elif e["source"] == "bogi":
                    if not any(e["quote"] in t for t in q_texts):
                        fail("E2", ww, f"인용 «{e['quote'][:30]}» 이 이 문항 상자 글에 글자 그대로 없음")
                elif e["source"] == "figure":
                    fig = q_figs.get(e.get("fig"))
                    if fig is None:
                        fail("E2", ww, f"그림 id «{e.get('fig')}» 가 지문 그림이나 이 문항 상자 그림에 없음")
                    elif not e["quote"].strip() or squash(e["quote"]) not in squash(fig):
                        fail("E2", ww, f"인용 «{e['quote'][:30]}» 이 그림 {e.get('fig')} 의 글자(pdf_text)에 없음")
                else:
                    fail("E2", ww, f"근거 출처 «{e['source']}» 는 passage/bogi/figure 만 허용")
            if j["basis"] == "해설지":
                if not j.get("explanation_quote") or squash(j["explanation_quote"]) not in sec_sq:
                    fail("E3", ww, "해설지 인용이 이 문항 해설에 글자 그대로 없음")
            elif j["basis"] == "자체":
                review.append(ww)
            else:
                fail("E3", ww, f"basis «{j['basis']}» 는 해설지/자체 만 허용")
            if not j.get("reason", "").strip() or "—" in j.get("reason", ""):
                fail("E4", ww, "이유가 비었거나 em dash 포함")

    print(f"== 세트 검사: {set_path}")
    if fails:
        print(f"불합격 {len(fails)}건")
        for f in fails:
            print("  " + f)
    else:
        print("합격 (프로그램 검사 전 항목 통과)")
    if review:
        print(f"해설지에 없는 선지 {len(review)}개: 별도 검토자 확인 필요 — " + ", ".join(review))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
