"""선지 줄이 '  ①' 꼴(앞 공백)이라 도구/세트_뽑기.py 가 선지를 못 찾는다. 도구는 고치지 않고 실행할 때만 선지 줄의 앞 공백을 뗀다."""
import sys, importlib
sys.path.insert(0, r"D:\Work\블로그\리딩맵\도구")
m = importlib.import_module("세트_뽑기")
_orig = m.page_lines
def patched(doc):
    return [l.lstrip() if l.lstrip()[:1] in m.CIRCLED and l.lstrip()[:1] else l for l in _orig(doc)]
m.page_lines = patched
sys.argv = ["세트_뽑기.py"] + sys.argv[1:]
m.main()
