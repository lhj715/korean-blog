"""세트 JSON → 기출 화면 HTML 조각. 사이트(게시.py)와 미리보기(미리보기.py)가 이 함수 하나를 같이 쓴다.
스타일은 assets/css/exam.css, 동작은 static/js/exam.js. HTML 을 손으로 쓰지 않는다.
"""
import html

CIR = "①②③④⑤"


def _spans(text, marks):
    cuts = sorted({0, len(text), *[m[0] for m in marks], *[m[1] for m in marks]})
    out = []
    for a, b in zip(cuts, cuts[1:]):
        cover = [m for m in marks if m[0] <= a and b <= m[1]]
        seg = html.escape(text[a:b])
        evs = [m[3] for m in cover if m[2] == "ev"]
        cls = []
        if any(m[2] == "ul" for m in cover):
            cls.append("xm-ul")
        if evs:
            cls.append("xm-ev")
            if any(e["ans"] for e in evs):
                cls.append("xm-ans")
        if cls:
            ids = " ".join(e["id"] for e in evs)
            attr = f' data-ev="{ids}"' if ids else ""
            seg = f'<span class="{" ".join(cls)}"{attr}>{seg}</span>'
        out.append(seg)
        for e in [m[3] for m in marks if m[2] == "ev" and m[1] == b]:
            out.append(f'<a class="xm-tag{" xm-ans" if e["ans"] else ""}" href="#prob{e["q"]}" data-pick="q{e["q"]}-{e["c"]}">{e["label"]}</a>')
    return "".join(out)


def _marks(text, evs, uls=()):
    ms = []
    for e in evs:
        i = text.find(e["quote"])
        if i < 0:
            raise ValueError(f"근거 인용이 본문에 없음: {e['quote'][:30]}")
        ms.append((i, i + len(e["quote"]), "ev", e))
    for u in uls:
        i = text.find(u["mark"] + u["text"])
        start = i + len(u["mark"]) if i >= 0 else text.find(u["mark"] + " " + u["text"]) + len(u["mark"]) + 1
        ms.append((start, start + len(u["text"]), "ul", None))
    return ms


def render_set(s, img):
    """img(파일명) → <img src> 에 넣을 주소."""
    meta = s.get("meta", {})
    by_para, by_bogi = {}, {}
    for q in s["questions"]:
        for j in q["judgments"]:
            for k, e in enumerate(j["evidence"]):
                item = {"id": f"e{q['no']}-{j['choice']}-{k}", "q": q["no"], "c": j["choice"],
                        "label": f"{q['no']}-{CIR[j['choice']-1]}", "ans": j["is_answer"], "quote": e["quote"]}
                (by_para.setdefault(e["para"], []) if e["source"] == "passage" else by_bogi.setdefault(q["no"], [])).append(item)

    lo, hi = s["range"]
    h = [f"<section class='xm-set' id='set{lo}-{hi}'>",
         f"<h2 class='xm-set-h'>{lo}~{hi}번 {html.escape(meta.get('area', ''))} · {html.escape(meta.get('topic', ''))}</h2>",
         "<div class='xm-passage'>",
         f"<p class='xm-guide'>{html.escape(s['guide'])}</p>",
         "<p class='xm-legend'><span class='xm-ev'>밑줄</span>은 선지 판단의 근거, <span class='xm-ev xm-ans'>초록 밑줄</span>은 정답의 근거입니다. "
         "옆 번호를 누르면 그 문제로 돌아가고, 선지의 '지문 근거'를 누르면 이 밑줄로 옵니다.</p>"]
    for p in s["passage"]:
        if p["type"] == "para":
            h.append(f"<p id='{lo}-{p['id']}'>{_spans(p['text'], _marks(p['text'], by_para.get(p['id'], []), p.get('underlines', [])))}</p>")
        else:
            h.append(f"<figure class='xm-fig'><img src='{img(p['image'])}' alt='{html.escape(p.get('alt', ''))}' loading='lazy'>"
                     f"<figcaption>{html.escape(p.get('caption', ''))}</figcaption></figure>")
    h.append("</div>")

    for q in s["questions"]:
        J = {j["choice"]: j for j in q["judgments"]}
        h.append(f"<div class='xm-q' id='prob{q['no']}'>")
        pt = " <span class='xm-pt'>[3점]</span>" if q["points"] == 3 else ""
        h.append(f"<p class='xm-stem'><b>{q['no']}.</b> {html.escape(q['stem'])}{pt}</p>")
        if q.get("bogi"):
            b = q["bogi"]
            h.append(f"<div class='xm-bogi'><p class='xm-bl'>{html.escape(b['label'])}</p>")
            if b.get("figure"):
                h.append(f"<img src='{img(b['figure']['image'])}' alt='{html.escape(b['figure'].get('alt', ''))}' loading='lazy'>")
            for t in b["paras"]:
                h.append(f"<p>{_spans(t, _marks(t, by_bogi.get(q['no'], [])))}</p>")
            h.append("</div>")
        h.append("<ul class='xm-opts'>")
        for i, c in enumerate(q["choices"], 1):
            a = J[i]["is_answer"]
            h.append(f"<li id='q{q['no']}-{i}'>{CIR[i-1]} {html.escape(c)}"
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
