import re, glob, sys, difflib
CIRC='①②③④⑤'
APPLY='--apply' in sys.argv

def build(text):
    ia={}
    probs=[(mt.start(), mt.group(1)) for mt in re.finditer(r'id="prob(\d+)"',text)]
    probs.append((len(text),None))
    for i in range(len(probs)-1):
        s,_=probs[i]; e=probs[i+1][0]; blk=text[s:e]
        am=re.search(r'정답</span><strong>([①②③④⑤])',blk)
        if not am: continue
        ans=CIRC.index(am.group(1))+1
        for lm in re.finditer(r'<li id="([^"]+)">\s*([①②③④⑤])',blk):
            ia[lm.group(1)]=(CIRC.index(lm.group(2))+1==ans)
    return ia

def recolor(text):
    ia=build(text)
    def ans_of(t):
        t=t.lstrip('#')
        if t in ia: return ia[t]
        base=re.sub(r'[a-z]+$','',t)   # qN-Mb -> qN-M
        return ia.get(base,False)
    # 1) src-tags inside each li -> class+label per enclosing li answer (preserve attrs/id)
    def fix_li(lm):
        body=lm.group(0); ans=ia.get(lm.group(1),False)
        def srep(sm):
            pre,href,post,label=sm.group(1),sm.group(2),sm.group(3),sm.group(4)
            suf=re.sub(r'^(정답 근거|오답 근거)','',label)
            newlabel=('정답 근거' if ans else '오답 근거')+suf
            cls='src-tag ans' if ans else 'src-tag'
            return f'<a class="{cls}"{pre}href="{href}"{post}>{newlabel}</a>'
        return re.sub(r'<a class="src-tag(?: ans)?"(\s[^>]*?\s|\s)href="(#[^"]+)"([^>]*)>([^<]*)</a>',srep,body)
    text=re.sub(r'<li id="([^"]+)">.*?</li>',fix_li,text,flags=re.S)
    # 2) ev-tags -> class per target option answer (fallback strip suffix)
    def evrep(m):
        pre,href,post,label=m.group(1),m.group(2),m.group(3),m.group(4)
        cls='ev-tag ans' if ans_of(href) else 'ev-tag'
        return f'<a class="{cls}"{pre}href="{href}"{post}>{label}</a>'
    text=re.sub(r'<a class="ev-tag(?: ans)?"(\s[^>]*?\s|\s)href="(#[^"]+)"([^>]*)>([^<]*)</a>',evrep,text)
    # 3) src reference map for spans: span_id -> any-answer (using enclosing li)
    src_ans={}
    for lm in re.finditer(r'<li id="([^"]+)">.*?</li>',text,flags=re.S):
        ans=ia.get(lm.group(1),False)
        for sm in re.finditer(r'class="src-tag( ans)?"[^>]*href="#(ev[^"]+)"',lm.group(0)):
            src_ans[sm.group(2)]=src_ans.get(sm.group(2),False) or ans
    # 4) span class: green iff trailing ev-tag ans OR src-from-answer
    pat=re.compile(r'<span class="ev(?: ans)?" id="(ev[^"]+)">(.*?)</span>((?:<a class="ev-tag(?: ans)?" href="#[^"]+">[^<]*</a>)*)',re.S)
    def sp(m):
        sid,inner,tail=m.group(1),m.group(2),m.group(3)
        green=src_ans.get(sid,False) or ('ev-tag ans"' in tail)
        return f'<span class="{"ev ans" if green else "ev"}" id="{sid}">{inner}</span>{tail}'
    text=pat.sub(sp,text)
    return text

tot=0
for f in sorted(glob.glob('content/exams/**/*.md',recursive=True)):
    a=open(f,encoding='utf-8').read(); b=recolor(a)
    if a!=b:
        ch=sum(1 for x in difflib.unified_diff(a.splitlines(),b.splitlines()) if x.startswith('+') and not x.startswith('+++'))
        tot+=ch; print(f"{f.split('/')[-1]}: {ch}")
        if APPLY: open(f,'w',encoding='utf-8').write(b)
print(f"총 {tot} | APPLY={APPLY}")
