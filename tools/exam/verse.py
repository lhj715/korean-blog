import fitz,re,glob,sys,json
B="/mnt/c/Users/관사/Documents/Codex/2026-05-27/goal/downloads/ebsi-korean"
doc=fitz.open(glob.glob(B+"/pdf/20230601-go2-problem*.pdf")[0])
def col(pi,c):
    pg=doc[pi];w=pg.rect.width;d=pg.get_text("dict");out=[]
    for blk in d["blocks"]:
        for ln in blk.get("lines",[]):
            t="".join(s["text"] for s in ln["spans"])
            if not t.strip():continue
            x0=round(ln["bbox"][0],1);cc=0 if x0<w/2 else 1
            if cc==c: out.append((ln["bbox"][1],x0,t.strip()))
    return sorted(out)
cfg=json.loads(sys.argv[2]); idx=cfg['idx']; locs=cfg['locs']; startkey=cfg['start']; endre=cfg['endre']
lines=[]
for pi,c in locs:
    for y,x,t in col(pi,c):
        if re.match(endre,t): break
        if re.match(r'^\d+$',t) or '국어영역' in t or t.startswith('[') or t=='(가)' or t.startswith('━'): continue
        lines.append(t)
f=sys.argv[1]; s=open(f,encoding='utf-8').read(); o=s
b=list(re.finditer(r'<div class="passage"[^>]*>(.*?)</div>',s,re.S))[idx]
cur=s.find(startkey,b.start()); 
if cur<0: print("start 못찾음");sys.exit()
cur+=len(startkey)
ins=[]
for t in lines[1:]:
    key=re.sub(r'^[㉠-㉣ⓐ-ⓔ]','',t)[:13]
    j=s.find(key,cur)
    if j<0: continue
    p=j
    while p>0 and s[p-1] in '㉠㉡㉢㉣ⓐⓑⓒⓓⓔ': p-=1
    pre=s[:p]
    if pre.count('<span')!=pre.count('</span>'):
        sm=re.search(r'<span[^>]*>[^<]*$',pre); p=sm.start() if sm else p
    sep='</p>\n  <p>' if t.startswith('(나)') else '<br>'
    ins.append((p,sep)); cur=j+len(key)
for p,sep in sorted(ins,key=lambda x:-x[0]):
    if s[:p].rstrip().endswith(('<br>','<p>')): continue
    s=s[:p]+sep+s[p:]
s=re.sub(r'<p>\s*</p>\s*','',s)
assert s.count('<span')==o.count('<span')
open(f,'w',encoding='utf-8').write(s)
b2=re.findall(r'<div class="passage"[^>]*>(.*?)</div>',s,re.S)[idx]
print(f"지문{idx+1}: 삽입{len(ins)} <p>{b2.count('<p>')} <br>{b2.count('<br>')}")
