import re,sys,json
f=sys.argv[1]; spec=json.loads(sys.argv[2])
s=open(f,encoding='utf-8').read(); o=s
# 지문 영역 범위
pranges=[(m.start(),m.end()) for m in re.finditer(r'<div class="passage"[^>]*>.*?</div>',s,re.S)]
def in_passage(i): return any(a<=i<b for a,b in pranges)
def wrap(txt,eid,qid,label,ans=False):
    global s
    pat=re.escape(txt).replace(r'\ ',r'\s*')
    hits=[m for m in re.finditer(pat,s) if in_passage(m.start()) and '<span' not in m.group(0) and '<a ' not in m.group(0) and s[:m.start()].count('<span')==s[:m.start()].count('</span>')]
    if len(hits)!=1:
        print(f"skip {label}: {len(hits)}건");return
    m=hits[0]; cls="ev ans" if ans else "ev"; tg="ev-tag ans" if ans else "ev-tag"
    s=s[:m.start()]+f'<span class="{cls}" id="{eid}">{m.group(0)}</span><a class="{tg}" href="#{qid}">{label}</a>'+s[m.end():]
    # 범위 갱신
    global pranges
    pranges=[(a,b+len(s)-len(o)) if a<=m.start() else (a,b) for a,b in pranges]
def btn(qid,eid,ans=False):
    global s
    m=re.search(r'(<li id="%s">.*?)</li>'%qid,s,re.S)
    if not m or 'src-tag' in m.group(1): return
    cls="src-tag ans" if ans else "src-tag"; lab="정답 근거" if ans else "오답 근거"
    s=s.replace(m.group(0),m.group(1)+f'<a class="{cls}" href="#{eid}">{lab}</a></li>')
for it in spec:
    wrap(it['t'],it['e'],it['q'],it['l'],it.get('a',False)); btn(it['q'],it['e'],it.get('a',False))
    pranges=[(m.start(),m.end()) for m in re.finditer(r'<div class="passage"[^>]*>.*?</div>',s,re.S)]
assert s.count('<span')==s.count('</span>')
open(f,'w',encoding='utf-8').write(s); print(f"적용 {len(spec)}개")
