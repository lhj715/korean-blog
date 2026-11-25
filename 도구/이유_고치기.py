"""선지를 거의 되풀이하는 «이유» 를 골라 묶음으로 내고, 다시 쓴 결과를 세트에 반영한다.

사용:
  py -X utf8 도구/이유_고치기.py 목록 <묶음 크기>      → 작업\\_이유\\묶음_NN.json (고칠 대상과 맥락)
  py -X utf8 도구/이유_고치기.py 검사 <묶음 번호>      → 작업\\_이유\\결과_NN.json 형식·규칙 검사
  py -X utf8 도구/이유_고치기.py 반영                  → 검토 통과한 결과_NN.json 을 세트 JSON 에 반영(검토_NN.md 끝 «최종 판정: 통과» 필요)
결과 파일 형식: {"항목 id": "새 이유" 또는 null(지금 문장을 그대로 둠)}
반영하면 작업\\<회차>\\이유_수정.json 에도 남긴다. 세트 만들기 스크립트를 다시 돌리면 이유가 되돌아가므로 이 파일로 다시 반영한다(`반영` 은 몇 번 돌려도 같다).
"""
import difflib
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "작업", "_이유")


def sq(s):
    return re.sub(r"[\s\.,‘’“”'\"()ⓐ-ⓩ㉠-㉿]+", "", s or "")


def echo(choice, reason):
    return difflib.SequenceMatcher(None, sq(choice), sq(reason), autojunk=False).ratio()


def boxes(q):
    b = q.get("bogi")
    return [] if not b else (b if isinstance(b, list) else [b])


def box_text(q):
    out = []
    for b in boxes(q):
        for it in (b.get("blocks") or []):
            out.append(it.get("text") or it.get("raster_text") or it.get("pdf_text") or "")
        out += b.get("paras", [])
        f = b.get("figure")
        if f:
            out.append("[그림] " + (f.get("raster_text") or f.get("pdf_text") or f.get("alt", "")))
    return "\n".join(x for x in out if x)


def sets():
    return sorted(glob.glob(os.path.join(ROOT, "작업", "20*", "세트_*.json")))


def make_list(size):
    os.makedirs(OUT, exist_ok=True)
    items, contexts = [], {}
    for f in sets():
        d = json.load(open(f, encoding="utf-8"))
        rel = os.path.relpath(f, ROOT).replace("\\", "/")
        for q in d["questions"]:
            for j in q["judgments"]:
                c = q["choices"][j["choice"] - 1]
                if echo(c, j["reason"]) < 0.6:
                    continue
                if rel not in contexts:
                    contexts[rel] = [{"id": p["id"], "text": p.get("text") or "[그림] " + (p.get("raster_text") or p.get("pdf_text") or p.get("alt", ""))} for p in d["passage"]]
                items.append({"id": f"{rel}#{q['no']}-{j['choice']}", "set": rel, "no": q["no"], "choice_no": j["choice"], "stem": q["stem"], "bogi": box_text(q),
                              "choice": c, "verdict": j["verdict"], "is_answer": j["is_answer"], "reason": j["reason"],
                              "evidence": [{"where": e.get("para") or e.get("fig") or e["source"], "quote": e["quote"]} for e in j["evidence"]],
                              "explanation_quote": j.get("explanation_quote", "")})
    n = 0
    for i in range(0, len(items), size):
        n += 1
        chunk = items[i:i + size]
        data = {"passages": {k: contexts[k] for k in sorted({x["set"] for x in chunk})}, "items": chunk}
        json.dump(data, open(os.path.join(OUT, f"묶음_{n:02d}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("고칠 대상", len(items), "묶음", n)


def check(num):
    data = json.load(open(os.path.join(OUT, f"묶음_{num}.json"), encoding="utf-8"))
    res = json.load(open(os.path.join(OUT, f"결과_{num}.json"), encoding="utf-8"))
    bad = []
    changed = 0
    for it in data["items"]:
        if it["id"] not in res:
            bad.append((it["id"], "결과 없음"))
            continue
        r = res[it["id"]]
        if r is None:
            continue
        changed += 1
        if not r.strip():
            bad.append((it["id"], "빈 문장"))
        if "—" in r or "해설지" in r:
            bad.append((it["id"], "금지 글자(em dash·«해설지»)"))
        if re.search(r"(요|죠|습니다|합니다|입니다|됩니다|십니다)[.!?]?\s*$", r.strip()):
            bad.append((it["id"], "말투: 기존처럼 «~다» 로 끝낸다"))
        if len(r) > 220:
            bad.append((it["id"], f"너무 김({len(r)}자)"))
        if echo(it["choice"], r) >= 0.6:
            bad.append((it["id"], "여전히 선지를 되풀이"))
    extra = set(res) - {x["id"] for x in data["items"]}
    bad += [(e, "묶음에 없는 id") for e in extra]
    for b in bad:
        print(b[1], "|", b[0])
    print(f"대상 {len(data['items'])} 고침 {changed} 문제 {len(bad)}")


def apply():
    per_set = {}
    for rp in sorted(glob.glob(os.path.join(OUT, "결과_*.json"))):
        num = re.search(r"결과_(\d+)", rp).group(1)
        reviews = sorted(glob.glob(os.path.join(OUT, f"검토_{num}*.md")))
        if not reviews or not re.search(r"최종 판정:\s*\**\s*통과", open(reviews[-1], encoding="utf-8").read()):
            print("건너뜀(검토 통과 없음):", num)
            continue
        for k, v in json.load(open(rp, encoding="utf-8")).items():
            if v is None:
                continue
            rel, key = k.rsplit("#", 1)
            per_set.setdefault(rel, {})[key] = v
    total = 0
    for rel, changes in per_set.items():
        path = os.path.join(ROOT, rel)
        d = json.load(open(path, encoding="utf-8"))
        for q in d["questions"]:
            for j in q["judgments"]:
                key = f"{q['no']}-{j['choice']}"
                if key in changes:
                    j["reason"] = changes[key]
                    total += 1
        json.dump(d, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        log = os.path.join(os.path.dirname(path), "이유_수정.json")
        old = json.load(open(log, encoding="utf-8")) if os.path.exists(log) else {}
        old.setdefault(os.path.basename(path), {}).update(changes)
        json.dump(old, open(log, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("반영한 이유", total, "세트", len(per_set))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "목록":
        make_list(int(sys.argv[2]))
    elif cmd == "검사":
        check(sys.argv[2])
    elif cmd == "반영":
        apply()
