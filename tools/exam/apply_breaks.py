# 사용: python3 apply_breaks.py <md> '<json>'
# json: {"지문번호(1부터)": ["문단시작문구", ...], ...}  문구 앞에 </p><p> 삽입
import re,sys,json
md=sys.argv[1]; spec=json.loads(sys.argv[2])
s=open(md,encoding='utf-8').read(); o=s
blocks=list(re.finditer(r'(<div class="passage"[^>]*>)(.*?)(</div>)',s,re.S))
def depth0_pos(block_start,body,phrase):
    # body 내 phrase 위치 중 span/a 밖이고 유일한 것
    idxs=[m.start() for m in re.finditer(re.escape(phrase),body)]
    ok=[]
    for i in idxs:
        pre=body[:i]
        if pre.count('<span')==pre.count('</span>') and pre.count('<a ')==pre.count('</a>'):
            ok.append(i)
    return ok
edits=[]; log=[]
for k,phrases in spec.items():
    bi=int(k)-1; bm=blocks[bi]
    head,body,tail=bm.group(1),bm.group(2),bm.group(3)
    bodybase=bm.start()+len(head)
    for ph in phrases:
        ok=depth0_pos(bm.start(),body,ph)
        if len(ok)!=1:
            log.append(f"지문{k} '{ph}' → 매칭 {len(ok)}개 (건너뜀)"); continue
        apos=bodybase+ok[0]
        if s[:apos].rstrip().endswith('<p>'): log.append(f"지문{k} '{ph}' 이미 문단경계"); continue
        edits.append(apos); log.append(f"지문{k} '{ph}' ✓")
for apos in sorted(set(edits),reverse=True): s=s[:apos]+'</p>\n  <p>'+s[apos:]
s=re.sub(r'<p>\s*</p>\s*','',s)
assert s.count('<span')==s.count('</span>'),"span 깨짐"
for tag in ['class="ev"','class="ev ans"','ev-tag','src-tag']: assert o.count(tag)==s.count(tag),tag
open(md,'w',encoding='utf-8').write(s)
print("\n".join(log)); print(f"\n삽입 {len(edits)}개")
