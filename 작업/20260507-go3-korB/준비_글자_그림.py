"""2026-03 2026-05 고3 언어와 매체(korB): 문제·해설 PDF 글자 덤프와 쪽 그림(dpi 150, 왼쪽·오른쪽 반쪽) 만들기."""
import pathlib, fitz
HERE = pathlib.Path(__file__).parent
PDF = HERE.parent.parent / "원본자료" / "ebsi-korean" / "pdf"
prob = PDF / "20260507-go3-problem-korB_mun_L475QB46.pdf"
expl = PDF / "20260507-go3-explanation-korB_hsj_746K9I7M_2.pdf"
for src, name in ((prob, "문제"), (expl, "해설")):
    d = fitz.open(src)
    out = []
    for i, pg in enumerate(d, 1):
        out.append(f"=== {name} {i}쪽 ===\n" + pg.get_text())
    (HERE / f"{name}_글자.txt").write_text("\n".join(out), encoding="utf-8")
d = fitz.open(prob)
for i, pg in enumerate(d, 1):
    r = pg.rect
    pg.get_pixmap(dpi=150).save(HERE / f"문제_{i}쪽.png")
    half = r.width / 2
    pg.get_pixmap(dpi=150, clip=fitz.Rect(0, 0, half, r.height)).save(HERE / f"문제_{i}쪽_왼쪽.png")
    pg.get_pixmap(dpi=150, clip=fitz.Rect(half, 0, r.width, r.height)).save(HERE / f"문제_{i}쪽_오른쪽.png")
print("쪽 수", len(d), "크기", d[0].rect)
