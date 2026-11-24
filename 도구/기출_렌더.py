"""세트 JSON → 기출 화면 HTML 조각. 사이트(게시.py)와 미리보기(미리보기.py)가 이 함수 하나를 같이 쓴다.
스타일은 assets/css/exam.css, 동작은 static/js/exam.js. HTML 을 손으로 쓰지 않는다.

지문·상자 항목 종류: para(문단, dialogue=true 면 대화 줄) / verse(시·시조, 줄은 \n, 연은 빈 줄) / label((가) 등)
 / note(각주·출처) / omit(중략 줄거리) / heading(초고의 제목·항목) / figure(그림·표 그림)
"""
import html
import re

from PIL import Image

CIR = "①②③④⑤"
# 원본 본문 글자 11.2pt ↔ 화면 본문 15px. 그림을 이 비율로 줄여 그림 속 글씨가 본문과 같은 크기로 보이게 한다.
PX_PER_PT = 15 / 11.2


def img_width(path):
    """그림_자르기.py 가 적어 둔 dpi 로 원본 크기를 구해 화면 너비(px)를 낸다."""
    im = Image.open(path)
    dpi = im.info.get("dpi")
    if not dpi:
        raise ValueError(f"그림에 dpi 가 없음(도구/그림_자르기.py 로 다시 자를 것): {path}")
    return round(im.width * 72 / dpi[0] * PX_PER_PT)
TEXT_TYPES = {"para", "verse", "label", "note", "omit", "heading"}


def _boxes(q):
    b = q.get("bogi")
    if not b:
        return []
    return b if isinstance(b, list) else [b]


def _box_items(box):
    if box.get("blocks"):
        return box["blocks"]
    items = [{"id": f"b{k+1}", "type": "para", "text": t} for k, t in enumerate(box.get("paras", []))]
    figs = box.get("figures") or ([box["figure"]] if box.get("figure") else [])
    items += [dict(f, type="figure", id=f.get("id", f"bf{k+1}")) for k, f in enumerate(figs)]
    return items


def _spans(text, marks):
    cuts = sorted({0, len(text), *[m[0] for m in marks], *[m[1] for m in marks]})
    out = []
    for a, b in zip(cuts, cuts[1:]):
        cover = [m for m in marks if m[0] <= a and b <= m[1]]
        seg = html.escape(text[a:b]).replace("\n", "<br>")
        evs = [m[3] for m in cover if m[2] == "ev"]
        cls = []
        if any(m[2] == "ul" for m in cover):
            cls.append("xm-ul")
        if any(m[2] == "rg" for m in cover):
            cls.append("xm-rgi")
        if any(m[2] == "b" for m in cover):
            cls.append("xm-b")
        if any(m[2] == "bx" for m in cover):
            cls.append("xm-bx")
            if re.fullmatch(r"\[[A-Z가-힣]\]|[ⓐ-ⓩ㉠-㉿]", text[a:b]):  # 글 속 네모 빈칸 [A]: 원본처럼 넓은 칸
                cls.append("xm-bxblank")
        if evs:
            cls.append("xm-ev")
            if any(e["ans"] for e in evs):
                cls.append("xm-ans")
        if cls:
            ids = " ".join(e["id"] for e in evs)
            attr = f' data-ev="{ids}"' if ids else ""
            seg = f'<span class="{" ".join(cls)}"{attr}>{seg}</span>'
        # 구간 표시(글 안 일부)는 시작 자리에 이름표
        for m in marks:
            if m[2] == "rg" and m[0] == a:
                seg = f'<span class="xm-rgl">{html.escape(m[3])}</span>' + seg
        out.append(seg)
        for e in [m[3] for m in marks if m[2] == "ev" and m[1] == b]:
            out.append(_tag(e))
    return "".join(out)


def _tag(e):
    return f'<a class="xm-tag{" xm-ans" if e["ans"] else ""}" href="#prob{e["q"]}" data-pick="q{e["q"]}-{e["c"]}">{e["label"]}</a>'


def _find_nth(text, bt):
    # 글자 그대로 또는 {"text": 글자, "nth": n} (n번째로 나오는 것, 1부터)
    t, n = (bt, 1) if isinstance(bt, str) else (bt["text"], bt.get("nth", 1))
    i = -1
    for _ in range(n):
        i = text.find(t, i + 1)
        if i < 0:
            break
    return i, len(t)


def _marks(text, evs, uls=(), rgs=(), bolds=(), boxed=()):
    ms = []
    for kind, lst in (("b", bolds), ("bx", boxed)):
        for bt in lst:
            i, n = _find_nth(text, bt)
            if i >= 0:
                ms.append((i, i + n, kind, None))
    for e in evs:
        i = text.find(e["quote"])
        if i < 0:
            raise ValueError(f"근거 인용이 본문에 없음: {e['quote'][:30]}")
        ms.append((i, i + len(e["quote"]), "ev", e))
    for u in uls:
        i = text.find(u["mark"] + u["text"])
        start = i + len(u["mark"]) if i >= 0 else text.find(u["mark"] + " " + u["text"]) + len(u["mark"]) + 1
        ms.append((start, start + len(u["text"]), "ul", None))
    for r in rgs:
        i = text.find(r["text"])
        ms.append((i, i + len(r["text"]), "rg", r["mark"]))
    return ms


def _item(p, evs, inline_rgs, anchor):
    t = p["type"]
    if t == "figure":
        tags = "".join(_tag(e) for e in evs)
        tagline = f"<div class='xm-figtags'>그림·표 근거 {tags}</div>" if tags else ""
        ids = " ".join(e["id"] for e in evs)
        dev = f" data-ev='{ids}'" if ids else ""
        return (f"<figure class='xm-fig' id='{anchor}'{dev}><img src='{p['_src']}' width='{p['_w']}' alt='{html.escape(p.get('alt', ''))}' loading='lazy'>"
                f"{'<figcaption>' + html.escape(p['caption']) + '</figcaption>' if p.get('caption') else ''}{tagline}</figure>")
    if p.get("display_image"):
        # 옛한글(PUA)처럼 글꼴로 못 보여 주는 항목: 쪽에서 잘라 낸 그림을 보인다(글은 alt 로 남긴다)
        tags = "".join(_tag(e) for e in evs)
        ids = " ".join(e["id"] for e in evs)
        dev = f" data-ev='{ids}'" if ids else ""
        return (f"<div class='xm-imgtext' id='{anchor}'{dev}><img src='{p['_src']}' width='{p['_w']}' alt='{html.escape(p['text'])}' loading='lazy'>"
                f"{'<div class=xm-figtags>근거 ' + tags + '</div>' if tags else ''}</div>")
    body = _spans(p["text"], _marks(p["text"], evs, p.get("underlines", []), inline_rgs, p.get("bold", []), p.get("boxed", [])))
    if p.get("blank"):  # 빈칸 밑줄 위의 글자(예: 학생: ____[가]____)
        b = html.escape(p["blank"])
        body = body.replace(b, f"<span class='xm-blank'>{b}</span>", 1)
    cls = {"para": "xm-dlg" if p.get("dialogue") else "", "verse": "xm-verse", "label": "xm-label",
           "note": "xm-note", "omit": "xm-omit", "heading": "xm-head"}[t]
    if p.get("center"):
        cls = (cls + " xm-center").strip()
    if t == "note" and re.match(r"^[-–] .+ [-–]$", p["text"]):  # 작품 출처 줄(- 작자, ｢제목｣ -)은 원본처럼 오른쪽
        cls += " xm-right"
    if t == "verse":  # 연시조의 <제1수> 같은 표시는 원본처럼 그 수 끝 오른쪽
        body = re.sub(r"(?:<br>)?(&lt;제\d+수&gt;)(?:<br>)?", r"<span class='xm-suno'>\1</span>", body)
    return f"<p class='{cls}' id='{anchor}'>{body}</p>" if cls else f"<p id='{anchor}'>{body}</p>"


def render_set(s, img, path):
    """img(파일명) → <img src> 에 넣을 주소, path(파일명) → 그 그림 파일 경로(크기 계산용)."""
    def pic(name):
        return {"_src": img(name), "_w": img_width(path(name))}

    meta = s.get("meta", {})
    lo, hi = s["range"]
    by_para, by_box, by_fig = {}, {}, {}
    for q in s["questions"]:
        for j in q["judgments"]:
            for k, e in enumerate(j["evidence"]):
                item = {"id": f"e{q['no']}-{j['choice']}-{k}", "q": q["no"], "c": j["choice"],
                        "label": f"{q['no']}-{CIR[j['choice']-1]}", "ans": j["is_answer"], "quote": e["quote"]}
                if e["source"] == "passage":
                    by_para.setdefault(e["para"], []).append(item)
                elif e["source"] == "bogi":
                    by_box.setdefault(q["no"], []).append(item)
                else:
                    by_fig.setdefault(e["fig"], []).append(item)

    ranges = s.get("ranges", [])
    block_rg = {}   # 항목 id → 구간 이름(여러 항목을 묶는 구간)
    inline_rg = {}  # 항목 id → [글 안 구간]
    for r in ranges:
        if "paras" in r:
            for pid in r["paras"]:
                block_rg[pid] = r["mark"]
        else:
            inline_rg.setdefault(r["para"], []).append(r)

    title = f"{lo}~{hi}번" + (f" {meta['area']}" if meta.get("area") else "") + (f" · {meta['topic']}" if meta.get("topic") else "")
    h = [f"<section class='xm-set' id='set{lo}-{hi}'>", f"<h2 class='xm-set-h'>{html.escape(title)}</h2>"]
    if s["passage"] or s.get("guide"):
        h.append("<div class='xm-passage'>")
        if s.get("guide"):
            h.append(f"<p class='xm-guide'>{html.escape(s['guide'])}</p>")
        h.append("<p class='xm-legend'><span class='xm-ev'>밑줄</span>은 선지 판단의 근거, <span class='xm-ev xm-ans'>초록 밑줄</span>은 정답의 근거입니다. "
                 "옆 번호를 누르면 그 문제로 돌아가고, 선지의 '지문 근거'를 누르면 이 밑줄로 옵니다.</p>")
        cur = None
        for p in s["passage"]:
            rg = block_rg.get(p["id"])
            if rg != cur:
                if cur:
                    h.append("</div>")
                if rg:
                    h.append(f"<div class='xm-rg'><span class='xm-rgl'>{html.escape(rg)}</span>")
                cur = rg
            if p.get("display_image"):
                p = dict(p, **pic(p["display_image"]))
            if p["type"] == "figure":
                p = dict(p, **pic(p["image"]))
                evs = by_fig.get(p["id"], [])
            else:
                evs = by_para.get(p["id"], [])
            x = _item(p, evs, inline_rg.get(p["id"], []), f"{lo}-{p['id']}")
            if p.get("cont") and h[-1].endswith("</p>") and x.startswith("<p"):
                # 쪽 경계에서 끊긴 문단: 앞 항목에 이어 한 문단으로 보인다("cont": true)
                # "cont": "join" 은 낱말 중간에서 끊긴 경우(공백 없이 잇는다), true 는 낱말 사이(공백 한 칸)
                h[-1] = h[-1][:-4] + ("" if p["cont"] == "join" else " ") + re.sub(r"^<p[^>]*>", "", x)
            else:
                h.append(x)
        if cur:
            h.append("</div>")
        h.append("</div>")

    for q in s["questions"]:
        J = {j["choice"]: j for j in q["judgments"]}
        h.append(f"<div class='xm-q' id='prob{q['no']}'>")
        pt = " <span class='xm-pt'>[3점]</span>" if q["points"] == 3 else ""
        st = q["stem"]
        stem_html = _spans(st, [(st.find(t), st.find(t) + len(t), "ul", None) for t in q.get("stem_underlines", []) if t in st]
                           + [(st.find(t), st.find(t) + len(t), "bx", None) for t in q.get("stem_boxed", []) if t in st])
        stem_p = f"<p class='xm-stem'><b>{q['no']}.</b> {stem_html}{pt}</p>"
        if q.get("sub_guide"):
            # 문항 사이 작은 안내문([13 ~ 14] <보기>는 …)과 두 문항 공용 상자는 원본처럼 발문보다 앞에 둔다
            h.append(f"<p class='xm-subguide'>{html.escape(q['sub_guide'])}</p>")
        else:
            h.append(stem_p)
        box_evs = list(by_box.get(q["no"], []))
        for box in _boxes(q):
            # plain: 원본에 테두리가 없는 묶음(선지 표의 열 머리 등)
            h.append("<div class='xm-bogi xm-plain'>" if box.get("plain") else "<div class='xm-bogi'>")
            if box.get("label"):
                h.append(f"<p class='xm-bl'>{html.escape(box['label'])}</p>")
            inbox = None  # 상자 안 상자: 이어진 항목의 "inbox" 값이 같으면 한 테두리로 묶는다
            for it in _box_items(box):
                if it.get("inbox") != inbox:
                    if inbox:
                        h.append("</div>")
                    if it.get("inbox"):
                        # "inbox_line": "dotted" 이면 원본처럼 점선 테두리
                        dot = " xm-dotted" if it.get("inbox_line") == "dotted" else ""
                        h.append(f"<div class='xm-inbox{dot}'>")
                    inbox = it.get("inbox")
                if it["type"] == "figure":
                    it = dict(it, **pic(it["image"]))
                    mine = by_fig.get(it["id"], [])
                    h.append(_item(it, mine, [], f"q{q['no']}-{it['id']}"))
                else:
                    if it.get("display_image"):
                        it = dict(it, **pic(it["display_image"]))
                    mine = [e for e in box_evs if e["quote"] in it["text"]]
                    for e in mine:
                        box_evs.remove(e)
                    h.append(_item(it, mine, [], f"q{q['no']}-{it['id']}"))
            if inbox:
                h.append("</div>")
            h.append("</div>")
        if q.get("sub_guide"):
            h.append(stem_p)
        h.append("<ul class='xm-opts'>")
        cu = q.get("choice_underlines") or {}
        for i, c in enumerate(q["choices"], 1):
            a = J[i]["is_answer"]
            ctext = _spans(c, [(c.find(t), c.find(t) + len(t), "ul", None) for t in cu.get(str(i), []) if t in c])
            for ci in (q.get("choice_images") or {}).get(str(i), []):
                # 옛한글(PUA) 글자 하나를 쪽에서 오려 낸 작은 그림으로 대신 보인다
                if ci["text"] in ctext:
                    ctext = ctext.replace(ci["text"], f"<img class='xm-inl' src='{img(ci['image'])}' alt='{html.escape(ci.get('alt', ''))}'>", 1)
            h.append(f"<li id='q{q['no']}-{i}'>{CIR[i-1]} {ctext}"
                     f"<a class='xm-src{' xm-ans' if a else ''}' href='#set{lo}-{hi}' data-ev='e{q['no']}-{i}-'>{'정답 근거' if a else '지문 근거'}</a></li>")
        h.append("</ul>")
        h.append(f"<details class='xm-sol'><summary>해설 보기</summary><p class='xm-answer'>정답 <b>{CIR[q['answer']-1]}</b></p>"
                 "<table class='xm-jt'><thead><tr><th>선지</th><th>판단</th><th>이유</th></tr></thead><tbody>")
        for i in range(1, 6):
            j = J[i]
            own = "" if j["basis"] == "해설지" else " <span class='xm-own'>해설지에 없는 선지</span>"
            h.append(f"<tr{' class=xm-ok' if j['is_answer'] else ''}><td>{CIR[i-1]}</td><td>{j['verdict']}</td><td>{html.escape(j['reason'])}{own}</td></tr>")
        h.append("</tbody></table></details></div>")
    h.append("</section>")
    return "\n".join(h)
