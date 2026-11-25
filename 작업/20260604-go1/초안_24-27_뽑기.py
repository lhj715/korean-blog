"""24번 선지가 '◦질문 ····· ①' 꼴(◦ 로 시작, 번호는 줄 끝)이라 도구/세트_뽑기.py 가 선지를 못 찾아 멈춘다.
도구는 고치지 않고 실행할 때만 선지 기호 목록에 '◦' 를 더해 초안을 뽑는다. 24번은 세트_24-27_만들기.py 에서 다시 짠다."""
import sys, importlib
sys.path.insert(0, r"D:\Work\블로그\리딩맵\도구")
m = importlib.import_module("세트_뽑기")
m.CIRCLED = "①②③④⑤◦"
sys.argv = ["세트_뽑기.py"] + sys.argv[1:]
m.main()
