# 기출 골격 회차 작업 도구

2015~2022 고2 골격 회차(해설 미작성·통짜 지문·옛한글 PUA) 완성용.
상세 방법: 메모리 project_readingmap_passage_paragraphs / project_readingmap_exam_analysis.

- `rescan_f2.py <md> <problem.pdf> '<{지문번호:[[page,col]...]}>'` — 좌표 상위2군집+종결부호로 문단시작 검출(JSON 출력)
- `apply_breaks.py <md> '<{지문번호:[문구...]}>' [--apply]` — 문구 앞에 </p><p> 삽입(지문한정·유일·depth0)
- `wrapbtn2.py <md> '<[{t,e,q,l,a}...]>'` — 지문에 근거 span+ev-tag, 선지에 src-tag(오답/정답). 실패스킵
- `verse.py <md> '<{idx,locs,start,endre}>'` — 운문 행별 <br>

소스 인덱스: data/exam_sources_index.json (159회차 PDF경로·정답표)
