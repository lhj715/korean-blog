"""세트 JSON 통과 관문. 하나라도 어기면 불합격(종료 코드 1)이고, 불합격 세트는 사이트에 올리지 않는다.

사용: py -X utf8 도구/세트_검사.py <세트 JSON> <문제PDF> <해설PDF> <정답 bundle JSON>

검사 항목(번호는 보고서에 그대로 찍힌다)
 A1 문항 번호가 범위와 맞고 연속이다          A2 문항마다 선지 5개, 빈 선지 없음
 A3 배점 2/3, 3점 표시가 PDF 와 일치            A4 지문 항목 종류는 para/verse/label/note/omit/heading/figure 만
 B1 지문·발문·선지·상자 글자가 PDF 텍스트층과 일치(공백 무시)
 B2 그림 글자·보기 머리말·쪽 머리글·선지 기호가 지문·발문·선지에 섞이지 않음
 B3 빠짐 없음: PDF 의 지문·문항 구역 글자가 등록한 조각으로 남김없이 설명된다
    (그림·표 속 글자는 그림 항목의 pdf_text, 구간 표시 [A] 등은 ranges 의 mark)
 C1 밑줄 범위가 항목 글 안에 그대로 있고 기호 바로 뒤에 온다
 C2 발문·선지에 나오는 ㉠·ⓐ·[A] 등 기호가 지문에서 밑줄·구간으로 등록됨(상자 안 기호·글 속 빈칸 [가] 는 예외)
 C3 등록한 밑줄 범위가 PDF 에 실제로 그어진 밑줄(선 그림)과 글자 단위로 같다(no_line 표시는 쪽 그림으로 확인한 경우만)
 C4 구간 표시([A] 등)가 가리키는 항목·글이 지문에 있다
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

HEADER = re.compile(r"^(\d+|국어영역|국어 영역|고[123]|홀수형|짝수형)$")
MARKS = "㉠㉡㉢㉣㉤㉥㉦㉧㉮㉯㉰㉱㉲ⓐⓑⓒⓓⓔⓕⓖ"
NEG = {"부적절", "불일치", "미반영", "틀림"}
POS = {"적절", "일치", "반영", "맞음"}
TEXT_TYPES = {"para", "verse", "label", "note", "omit", "heading"}
CIRS = "①②③④⑤"


def squash(s):
    return re.sub(r"\s+", "", s)


def pdf_text(path):
    out = []
    for page in fitz.open(path):
        out += [l for l in page.get_text("text").split("\n") if not HEADER.match(l.strip())]
    return "\n".join(out)


def underlined_runs(path):
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
        chars = [(c["c"], fitz.Rect(c["bbox"])) for b in page.get_text("rawdict")["blocks"]
                 for l in b.get("lines", []) for sp in l["spans"] for c in sp["chars"]]
        seen = set()
        for x0, x1, y in segs:
            t = squash("".join(c for c, r in chars if r.x0 >= x0 - 1 and r.x1 <= x1 + 1 and 0 <= y - r.y1 < 4))
            key = (round(x0), round(y))
            if t and key not in seen:
                seen.add(key)
                runs.append(((pno, x0 >= half, round(y), x0), t))
    return [t for _, t in sorted(runs)]


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
        if q["points"] not in (2, 3):
            fail("A3", w, "배점이 2/3 이 아님")
        m = re.search(rf"(^|\n){q['no']}\.\s(.{{0,400}}?)(\n①|①)", src, re.S)
        has3 = bool(m and "[3점]" in m.group(2))
        if has3 != (q["points"] == 3):
            fail("A3", w, f"3점 표시 불일치(PDF {'있음' if has3 else '없음'})")

    # B1·B2
    texts = [(f"지문 {p['id']}", p["text"], True) for p in texts_p.values()]
    for q in qs:
        texts.append((f"{q['no']}번 발문", q["stem"], True))
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
        if strict and re.search(r"<\s*그\s*림\s*>(?![가-힣])|<\s*보\s*기\s*>(?![가-힣])|-{4,}|\+{4,}|===|[①②③④⑤]", t):
            fail("B2", where, "그림 글자·보기 머리말·쪽 머리글·선지 기호가 섞임")

    # B3 빠짐 없음
    def cut(region, pieces, where):
        for name, piece in pieces:
            sq = squash(piece)
            if not sq:
                continue
            k = region.find(sq)
            if k < 0:
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
        k = src_sq.find(f"{q['no']}." + squash(q["stem"])[:12], pos)
        starts.append(k)
        pos = max(k, pos)
    if min(starts) < 0:
        fail("B3", "세트", f"문항 시작 위치를 찾지 못함 {starts}")
    else:
        nxt = [m.start() for m in re.finditer(r"\[\d+~\d+\]", src_sq) if m.start() > starts[-1]]
        nq = [m.start() for m in re.finditer(rf"(?<!\d){hi+1}\.", src_sq) if m.start() > starts[-1]]
        end = min(nxt[:1] + nq[:1] + [len(src_sq)])
        leftovers = []
        if s.get("guide") and g >= 0:
            region = src_sq[g + len(squash(s["guide"])): starts[0]]
            pieces = [(p["id"], p["text"] if p["type"] in TEXT_TYPES else p.get("pdf_text", "")) for p in s["passage"]]
            leftovers.append(("지문 구역", cut(region, pieces, "지문 구역")))
        for i, q in enumerate(qs):
            region = src_sq[starts[i]: starts[i + 1] if i + 1 < len(qs) else end]
            pieces = [("번호", f"{q['no']}."), ("발문", q["stem"])]
            if q["points"] == 3:
                pieces.append(("[3점]", "[3점]"))
            for bi, box in enumerate(boxes(q)):
                pieces.append((f"상자{bi+1} 머리말", box.get("label", "")))
                for it in box_items(box):
                    pieces.append((f"상자{bi+1} {it['id']}", it["text"] if it["type"] in TEXT_TYPES else it.get("pdf_text", "")))
            pieces += [(f"선지 {CIRS[k]}", CIRS[k] + c) for k, c in enumerate(q["choices"])]
            leftovers.append((f"{q['no']}번 구역", cut(region, pieces, f"{q['no']}번 구역")))
        # 구간 표시([A] 등)는 PDF 에서 쪽 끝 등 엉뚱한 자리에 찍히므로 남은 글자에서 한 번씩 지운다
        rest = "".join(r for _, r in leftovers)
        for rg in ranges:
            mk = squash(rg["mark"])
            k = rest.find(mk)
            if k < 0:
                fail("B3", "구간", f"구간 표시 «{rg['mark']}» 를 PDF 남은 글자에서 찾지 못함")
            else:
                rest = rest[:k] + rest[k + len(mk):]
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
            if (u["mark"] + u["text"]) not in p["text"] and (u["mark"] + " " + u["text"]) not in p["text"]:
                fail("C1", f"{p['id']}", f"밑줄 {u['mark']} «{u['text']}» 이 기호 바로 뒤에 없음")
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
    passage_text = " ".join(p["text"] for p in texts_p.values())
    box_text = " ".join(it["text"] for it in box_text_items)
    for m in sorted(used - marks):
        if m.startswith("["):
            ok = m in passage_text or m in box_text
        else:
            ok = m not in passage_text and m in box_text
        if not ok:
            fail("C2", "세트", f"{m} 이 발문·선지에 나오는데 지문의 밑줄·구간으로 등록되지 않음")

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
        negative = bool(re.search(r"(않은|않는|없는|틀린|적절하지)", q["stem"]))
        for j in js:
            v = j["verdict"]
            want = (NEG if negative else POS) if j["is_answer"] else (POS if negative else NEG)
            if v not in want:
                fail("D3", f"{w} {CIRS[j['choice']-1]}", f"판단 «{v}» 이 발문 방향과 안 맞음(기대: {'/'.join(sorted(want))})")
        sec = re.search(rf"(^|\n){q['no']}\.\s*\[출제의도\](.*?)(?=\n{q['no']+1}\.\s*\[출제의도\]|\n\[\d+\s*[~～]\s*\d+\]|\Z)", expl, re.S)
        sec_sq = squash(sec.group(2)) if sec else ""
        if not sec:
            fail("E3", w, "해설지에서 이 문항 해설을 찾지 못함")
        q_texts = [it["text"] for box in boxes(q) for it in box_items(box) if it["type"] in TEXT_TYPES]
        q_figs = {it["id"]: it.get("pdf_text", "") for box in boxes(q) for it in box_items(box) if it["type"] == "figure"}
        q_figs.update({f["id"]: f.get("pdf_text", "") for f in figs_p.values()})
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
