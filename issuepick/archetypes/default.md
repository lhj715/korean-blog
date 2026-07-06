---
title: "{{ replace .File.ContentBaseName "-" " " | title }}"
date: {{ .Date }}
draft: true
summary: ""            # 목록 카드·메타 설명에 노출되는 한 줄 요약
targets: []            # 예: ["청년", "전국민"]
regions: ["전국"]
topics: []             # 예: ["청년도약계좌"]
amount: ""             # 예: "월 최대 70만원" — 카드에 강조 표기
deadline: ""           # YYYY-MM-DD. 비우면 '상시'
apply_url: ""          # 신청 바로가기 링크
source: ""             # 근거 출처 (정부 보도자료 URL 등)
keywords: []           # 검색 노출용 키워드
---
