# 표준국어대사전 API로 추가 한자성어 뜻·한자 수집 (예문 제외)
import json, time, urllib.request, urllib.parse

API_KEY = "A2682A576B894322BF0BB381471AC12A"
URL = "https://stdict.korean.go.kr/api/search.do"

# 빈출 한자성어 후보 (현재 198개와 겹치는 건 자동 제외)
CAND = """
각골난망 가담항설 가렴주구 감언이설 강구연월 개과천선 거두절미 거안사위 견강부회 견문발검
경거망동 계구우후 고립무원 고장난명 곡학아세 골육상잔 교각살우 교언영색 구사일생 구우일모
권모술수 권선징악 권토중래 기고만장 기상천외 낙화유수 낭중지추 내우외환 노발대발 노심초사
다사다난 단도직입 단사표음 당랑거철 대기만성 대동소이 대의명분 도원결의 독불장군 동가홍상
동고동락 동상이몽 등용문 만사여의 망양보뢰 명경지수 무릉도원 박장대소 박학다식 발본색원
백년해로 백발백중 백척간두 백해무익 분골쇄신 불철주야 빈이낙도 사상누각 삼고초려 속수무책
수주대토 시기상조 식자우환 안분지족 양상군자 언중유골 오매불망 오십보백보 오월동주 온고지신
외유내강 유유자적 은인자중 이구동성 인과응보 인면수심 자가당착 자포자기 작심삼일 전광석화
절차탁마 점입가경 진퇴양난 천방지축 천재일우 청산유수 초지일관 파란만장 학수고대 후안무치
각자도생 개문납적 격화소양 경천동지 고군분투 과공비례 교토삼굴 군계일학 금과옥조 낙락장송
난신적자 남부여대 남존여비 노익장 논공행상 동족방뇨 면종복배 무위도식 미사여구 반신반의
배수진 백골난망 백아절현 부귀영화 불원천리 비분강개 상전벽해 석고대죄 소신공양 송구영신
승승장구 시종일관 약육강식 완물상지 용두사미 유명무실 이판사판 인산인해 자승자박 자화자찬
장삼이사 적자생존 전무후무 절세가인 정저지와 주경야독 중구난방 지성감천 진수성찬 차일피일
천의무봉 천인공노 청천벽력 초록동색 취생몽사 탁상공론 팔방미인 풍비박산 함흥차사 혈혈단신
호사다마 환골탈태 후생가외 가인박명 각양각색 공명정대 노마지지 다기망양 반목질시 백면서생
수렴청정 약방감초 양약고구 언어도단 오호통재 일기당천 임전무퇴 자고이래 자수성가 장유유서
재자가인 적재적소 전인미답 진충보국 천생연분 청풍명월 취사선택 포복절도 허심탄회 현모양처
호시탐탐 홍익인간 후회막급 양호유환 맹모삼천 서시빈목 백이숙제 와룡봉추 삼척동자 백년가약
독수공방 마부위침 망연자실 백문불여일견 신출귀몰 심기일전 양자택일 음참마속 의기양양 이전투구
일도양단 일사천리 자급자족 전전반측 절치부심 주객전도 중언부언 진인사대천명 촌철살인 추풍낙엽
의기소침 일언반구 거안제미 경세제민 공중누각 구화지문 단말마 대의멸친 만고강산 발분망식
배은망덕 사고무친 사생결단 산전수전 심사숙고 온유돈후 이합집산 천리안 흑백논리 감개무량
개선장군 경천애인 과대망상 금의야행 남가일몽 만수무강 무위자연 백락일고 백전백승 변화무쌍
사분오열 사통팔달 삼라만상 삼위일체 상명하복 생생지락 수수방관 수적천석 시종여일 십년감수
악전고투 오곡백과 완전무결 용호상박 우문현답 월하빙인 이해득실 익자삼우 정신일도 철두철미
청렴결백 태산준령 허장성세 혼정신성 각골통한 견리사의 극기복례 군신유의 도광양회 독서삼매
백가쟁명 보국안민 부귀공명 사기충천 생사고락 심모원려 암중모색 연전연승 요산요수 전심전력
천편일률 출장입상 패가망신 풍찬노숙 고목생화 괴력난신 국태민안 근검절약 금의환향 무사안일
반신불수 백수건달 백전노장 사리사욕 속전속결 기사회생 계란유골 함구무언 자업자득 견원지간
구곡간장 노류장화 단표누항 만경창파 백년대계 부지기수 사필귀정 삼순구식 어동육서 일벌백계
주지육림 천하태평 풍수지탄 형제투금 호구지책 십벌지목 안빈�낙도 연하고질 청운지지 호접지몽
""".split()

existing = {x["word"] for x in json.load(open("data/idioms.json", encoding="utf-8"))}
cands = []
seen = set()
for w in CAND:
    if w in existing or w in seen:
        continue
    seen.add(w); cands.append(w)
print(f"후보 {len(cands)}개 (198 제외 후)")

def fetch(word):
    params = urllib.parse.urlencode({"key": API_KEY, "q": word, "req_type": "json", "num": "5"})
    req = urllib.request.Request(f"{URL}?{params}")
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read().decode("utf-8"))
    items = data.get("channel", {}).get("item", [])
    if isinstance(items, dict):
        items = [items]
    for it in items:
        wd = it.get("word", "").replace("-", "").replace("^", "").strip()
        if wd != word:
            continue
        origin = it.get("origin", "").strip()
        sense = it.get("sense", {})
        if isinstance(sense, list):
            sense = sense[0] if sense else {}
        definition = sense.get("definition", "").strip()
        # 한자(origin)가 있고 글자수가 단어와 같으면 성어로 인정
        han = "".join(ch for ch in origin if "一" <= ch <= "鿿")
        if han and definition:
            return {"word": word, "hanja": han, "meaning": definition, "example": ""}
    return None

out = []
miss = []
for i, w in enumerate(cands):
    try:
        r = fetch(w)
        if r:
            out.append(r)
        else:
            miss.append(w)
    except Exception as e:
        miss.append(w + f"(ERR)")
    time.sleep(0.25)
    if (i + 1) % 50 == 0:
        print(f"  {i+1}/{len(cands)} ... 수집 {len(out)}")

json.dump(out, open("new_idioms_raw.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"\n수집 성공: {len(out)}개 → new_idioms_raw.json")
print(f"매칭 실패({len(miss)}): {' '.join(miss)}")
