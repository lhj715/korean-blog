import fitz,re,sys,json
from collections import Counter
B="/mnt/c/Users/관사/Documents/Codex/2026-05-27/goal/downloads/ebsi-korean"
def norm(t):
    t=re.sub(r'\d{0,2}\s*국어\s*영역','',t); return re.sub(r'[^가-힣0-9]','',t)
pdf=sys.argv[2]; doc=fitz.open(pdf)
def lines_pc(pi,c):
    pg=doc[pi];w=pg.rect.width;d=pg.get_text("dict");out=[]
    for blk in d["blocks"]:
        for ln in blk.get("lines",[]):
            t="".join(s["text"] for s in ln["spans"])
            if not t.strip():continue
            if re.match(r'^\s*\d{0,2}\s*국어\s*영역',t):continue
            x0=round(ln["bbox"][0],1);cc=0 if x0<w/2 else 1
            if cc==c: out.append((ln["bbox"][1],x0,t))
    return sorted(out)
s=open(sys.argv[1],encoding='utf-8').read()
locs=json.loads(sys.argv[3])
passages=list(re.finditer(r'<div class="passage"[^>]*>(.*?)</div>',s,re.S))
allphr={}
for k,ls in locs.items():
    npl=norm(re.sub(r'<[^>]+>','',passages[int(k)-1].group(1)))
    phr=[]
    for pi,c in ls:
        L=lines_pc(pi,c)
        plines=[(y,x0,t) for (y,x0,t) in L if len(norm(t))>=6 and norm(t)[:9] in npl]
        if len(plines)<2: continue
        # 상위 2개 x0 군집 → 본문선/문단선, 중간값 기준
        cnt=Counter(round(x0) for y,x0,t in plines)
        top=[x for x,_ in cnt.most_common(4)]
        if len(top)<2:
            thr=min(top)+7
        else:
            a,b=sorted(top[:2]); 
            # 두 군집이 5~16 떨어져야 본문/문단; 아니면 다음 후보
            if not (5<=b-a<=18):
                # 본문선=최빈, 문단선=본문+10 근처 탐색
                base=cnt.most_common(1)[0][0]; b=base+10; a=base
            thr=(a+b)/2
        for i,(y,x0,t) in enumerate(plines):
            if x0>=thr:
                # 앞 지문줄이 문장종결부호로 끝나야 진짜 문단/대화 시작(이어지는 줄 제외)
                if i>0:
                    prev=plines[i-1][2].rstrip()
                    if prev and prev[-1] not in '.?!\u201d\u2019\u300d\u300f\u2026)\uff09':
                        continue
                ph=re.sub(r'^[㉠-㉿\[]','',t.strip())[:18].strip()
                if re.search('[가-힣]',ph): phr.append(ph)
    allphr[k]=phr
print(json.dumps(allphr,ensure_ascii=False))
