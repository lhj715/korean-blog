"""세트 JSON → 확인용 HTML (이 컴퓨터에서만 보는 미리보기. 사이트 배포용 아님).

사용: py -X utf8 도구/미리보기.py <세트 JSON> <출력 HTML>
그림 파일은 세트 JSON 과 같은 폴더에 있어야 한다.
HTML 은 사람이 손으로 쓰지 않는다. 형식을 바꾸려면 이 파일을 고친다.
"""
import base64
import html
import json
import os
import sys

CIR = "①②③④⑤"


def spans(text, marks):
    """marks: [(start, end, kind, payload)] → 겹침을 고려해 조각으로 나눠 HTML 을 만든다."""
    cuts = sorted({0, len(text), *[m[0] for m in marks], *[m[1] for m in marks]})
    out = []
    for a, b in zip(cuts, cuts[1:]):
        cover = [m for m in marks if m[0] <= a and b <= m[1]]
        seg = html.escape(text[a:b])
        evs = [m[3] for m in cover if m[2] == "ev"]
        cls = []
        if any(m[2] == "ul" for m in cover):
            cls.append("ul")
        if evs:
            cls.append("ev")
            if any(e["ans"] for e in evs):
                cls.append("ans")
        if cls:
            ids = " ".join(e["id"] for e in evs)
            seg = f'<span class="{" ".join(cls)}" data-ev="{ids}">{seg}</span>'
        out.append(seg)
        # 근거가 끝나는 자리에 문항·선지 꼬리표
        for e in [m[3] for m in marks if m[2] == "ev" and m[1] == b]:
            out.append(f'<a class="tag{" ans" if e["ans"] else ""}" href="#{e["target"]}" data-pick="{e["choice"]}">{e["label"]}</a>')
    return "".join(out)


def main():
    src, dst = sys.argv[1:3]
    s = json.load(open(src, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(src))

    def img(name):
        data = base64.b64encode(open(os.path.join(base, name), "rb").read()).decode()
        return "data:image/png;base64," + data
    meta = s.get("meta", {})
    ev_by_para = {}
    ev_by_bogi = {}
    for q in s["questions"]:
        for j in q["judgments"]:
            for k, e in enumerate(j["evidence"]):
                item = {"id": f"e{q['no']}-{j['choice']}-{k}", "target": f"prob{q['no']}", "choice": f"q{q['no']}-{j['choice']}",
                        "label": f"{q['no']}-{CIR[j['choice']-1]}", "ans": j["is_answer"], "quote": e["quote"]}
                (ev_by_para.setdefault(e["para"], []) if e["source"] == "passage" else ev_by_bogi.setdefault(q["no"], [])).append(item)

    def marks_for(text, evs, uls=()):
        ms = []
        for e in evs:
            i = text.find(e["quote"])
            ms.append((i, i + len(e["quote"]), "ev", e))
        for u in uls:
            i = text.find(u["mark"] + u["text"])
            if i < 0:
                i = text.find(u["mark"] + " " + u["text"]) + 1
            start = i + len(u["mark"])
            ms.append((start, start + len(u["text"]), "ul", None))
        return ms

    h = []
    h.append(f"<h1>{html.escape(meta.get('exam', ''))} {s['range'][0]}~{s['range'][1]}번</h1>")
    h.append(f"<p class='sub'>{html.escape(meta.get('area', ''))} · {html.escape(meta.get('topic', ''))}</p>")
    h.append("<div class='passage'>")
    h.append(f"<p class='guide'>{html.escape(s['guide'])}</p>")
    h.append("<p class='legend'><span class='ev'>밑줄 친 곳</span>은 선지 판단의 근거, <span class='ev ans'>초록</span>은 정답의 근거입니다. 옆 번호를 누르면 그 문제로 돌아가고 해당 선지가 표시됩니다.</p>")
    for p in s["passage"]:
        if p["type"] == "para":
            h.append(f"<p id='{p['id']}'>{spans(p['text'], marks_for(p['text'], ev_by_para.get(p['id'], []), p.get('underlines', [])))}</p>")
        else:
            h.append(f"<figure><img src='{img(p['image'])}' alt='{html.escape(p.get('alt', ''))}'><figcaption>{html.escape(p.get('caption', ''))}</figcaption></figure>")
    h.append("</div>")

    for q in s["questions"]:
        h.append(f"<div class='q' id='prob{q['no']}'>")
        pt = " <span class='pt'>[3점]</span>" if q["points"] == 3 else ""
        h.append(f"<p class='stem'><b>{q['no']}.</b> {html.escape(q['stem'])}{pt}</p>")
        if q.get("bogi"):
            b = q["bogi"]
            h.append(f"<div class='bogi'><p class='bl'>{html.escape(b['label'])}</p>")
            if b.get("figure"):
                h.append(f"<img src='{img(b['figure']['image'])}' alt='{html.escape(b['figure'].get('alt', ''))}'>")
            for t in b["paras"]:
                h.append(f"<p>{spans(t, marks_for(t, ev_by_bogi.get(q['no'], [])))}</p>")
            h.append("</div>")
        h.append("<ol class='opts'>")
        J = {j["choice"]: j for j in q["judgments"]}
        for i, c in enumerate(q["choices"], 1):
            first = f"e{q['no']}-{i}-0"
            h.append(f"<li id='q{q['no']}-{i}'>{CIR[i-1]} {html.escape(c)} <a class='src{' ans' if J[i]['is_answer'] else ''}' href='#' data-go='{first}'>{'정답 근거' if J[i]['is_answer'] else '지문 근거'}</a></li>")
        h.append("</ol>")
        h.append(f"<details><summary>해설 보기</summary><p class='answer'>정답 <b>{CIR[q['answer']-1]}</b></p><table><tr><th>선지</th><th>판단</th><th>이유</th></tr>")
        for i in range(1, 6):
            j = J[i]
            mark = "" if j["basis"] == "해설지" else " <span class='own'>해설지에 없음</span>"
            h.append(f"<tr class='{'ok' if j['is_answer'] else ''}'><td>{CIR[i-1]}</td><td>{j['verdict']}</td><td>{html.escape(j['reason'])}{mark}</td></tr>")
        h.append("</table></details></div>")

    css = """
:root{--ink:#1d1d1b;--mid:#5a5a55;--line:#e4e0d6;--bg:#fbfaf6;--blue:#2457a6;--green:#1f7a3d}
@media (prefers-color-scheme:dark){:root{--ink:#ecebe6;--mid:#a9a8a1;--line:#3a3934;--bg:#1b1b19;--blue:#7fa8ff;--green:#5fc97f}}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.85 'Noto Serif KR',serif}
main{max-width:760px;margin:0 auto;padding:24px 16px 80vh}
h1{font-size:22px;margin:0}.sub{color:var(--mid);margin:4px 0 20px}
.passage{border:1px solid var(--line);padding:16px 18px;border-radius:6px}
.guide{font-weight:700}.legend{font-size:13px;color:var(--mid)}
.passage p{text-indent:1em;margin:0 0 6px}.passage p.guide,.passage p.legend{text-indent:0}
figure{margin:10px 0;text-align:center}figure img,.bogi img{max-width:100%;background:#fff;border-radius:4px}
figcaption{font-size:13px;color:var(--mid)}
.ul{text-decoration:underline;text-underline-offset:3px}
.ev{border-bottom:2px solid var(--blue)}.ev.ans{border-bottom-color:var(--green)}
.ev.hit{background:color-mix(in srgb,var(--blue) 18%,transparent)}.ev.ans.hit{background:color-mix(in srgb,var(--green) 20%,transparent)}
.tag{font:600 11px/1 sans-serif;color:var(--blue);text-decoration:none;vertical-align:super;margin:0 2px}.tag.ans{color:var(--green)}
.q{margin-top:28px;scroll-margin-top:12px}.opts li.pick{background:color-mix(in srgb,var(--blue) 14%,transparent);border-radius:4px}.stem{margin:0 0 8px}.pt{color:var(--mid)}
.bogi{border:1px solid var(--line);padding:10px 14px;margin:8px 0;border-radius:6px}.bl{text-align:center;margin:0}
.opts{list-style:none;padding:0;margin:0}.opts li{margin:4px 0;padding-left:1.2em;text-indent:-1.2em}
.src{font:600 12px sans-serif;color:var(--blue);margin-left:6px}.src.ans{color:var(--green)}
details{margin-top:10px;border-top:1px dashed var(--line);padding-top:8px}summary{cursor:pointer;color:var(--mid)}
table{border-collapse:collapse;width:100%;font-size:14px;margin-top:6px}th,td{border:1px solid var(--line);padding:6px 8px;vertical-align:top;text-align:left}
td:first-child,td:nth-child(2){white-space:nowrap}tr.ok td{color:var(--green);font-weight:600}
.own{font:600 11px sans-serif;color:#b0601b;margin-left:4px}.answer{margin:4px 0}
"""
    js = """
document.querySelectorAll('a.tag').forEach(a=>a.addEventListener('click',ev=>{ev.preventDefault();
 const q=document.querySelector(a.getAttribute('href')); if(q) q.scrollIntoView({behavior:'smooth',block:'start'});
 document.querySelectorAll('li.pick').forEach(x=>x.classList.remove('pick'));
 const li=document.getElementById(a.dataset.pick); if(li) li.classList.add('pick');}));
document.querySelectorAll('a.src').forEach(a=>a.addEventListener('click',ev=>{ev.preventDefault();
 const id=a.dataset.go; document.querySelectorAll('.hit').forEach(x=>x.classList.remove('hit'));
 const hits=[...document.querySelectorAll('[data-ev]')].filter(x=>x.dataset.ev.split(' ').some(e=>e.startsWith(id.slice(0,-2))));
 hits.forEach(x=>x.classList.add('hit')); if(hits[0]) hits[0].scrollIntoView({behavior:'smooth',block:'center'});}));
"""
    page = f"<!doctype html><html lang='ko'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>리딩맵 미리보기</title><style>{css}</style></head><body><main>{''.join(h)}</main><script>{js}</script></body></html>"
    open(dst, "w", encoding="utf-8").write(page)
    print("ok", dst)


if __name__ == "__main__":
    main()
