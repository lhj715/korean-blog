# readingmap.kr 도메인 분리 + 새 사이트 연결 계획

## 현재 상태 (조사 결과)
- readingmap.kr → **A 183.111.161.147 (카페24 워드프레스)**, Cloudflare 프록시 경유
- www / *.readingmap.kr → apex로 CNAME (proxied)
- MX → mw-002.cafe24.com (카페24 메일), TXT SPF 존재
- CF zone ID: `fb2d0e9236f3538c592111be7b5fc7f3` (active, 토큰으로 DNS 제어 가능)

## 목표
워드프레스(카페24)를 떼어내고, 새 Hugo 정적 사이트(이 레포)를 readingmap.kr에 연결.

## 배포 방식 권고: **Cloudflare Pages**
이유: DNS가 이미 CF에 있음 + 무료 + GitHub 푸시하면 자동 빌드/배포 + 커스텀 도메인 추가 시 DNS 자동 설정.
- 빌드: `hugo` / 출력: `public` / 환경변수 `HUGO_VERSION=0.161.1`
- 대안: GitHub Pages(가능하나 CF Pages가 더 매끄러움), wrangler 직접 업로드(GitHub 연동 없이 토큰만으로).

## 단계 (안전 순서 — 라이브 컷오버는 마지막)
1. **[안전]** 새 사이트를 GitHub(lhj715/korean-blog)에 푸시. ※ 이 시점엔 readingmap.kr은 여전히 카페24를 가리키므로 라이브 영향 없음.
2. **[안전]** CF Pages 프로젝트 생성 → 레포 연결 → `*.pages.dev` 프리뷰 URL에서 새 사이트 검수.
3. **[라이브 컷오버 — 사용자 확인 필수]** Pages 프로젝트에 readingmap.kr 커스텀 도메인 추가
   → A 183.111.161.147 → Pages CNAME으로 교체. www도 동일.
4. **[보존]** MX(메일)·SPF TXT는 그대로 둔다 (이메일 계속 카페24 사용 시). 워드프레스 글/메일을 안 쓰면 추후 정리.

## 주의
- 컷오버 = 되돌릴 수 있으나(레코드 원복) 라이브 사이트가 바뀌므로 사용자 확인 후 실행.
- 기존 WP 콘텐츠 SEO가 중요하면 주요 URL 리다이렉트 매핑 검토 (현재는 "갈아엎기" 방침이라 생략 가능).
- GitHub OAuth 연동은 브라우저 1회 클릭 필요(비개발자 단계) → 또는 wrangler 토큰 업로드로 우회 가능.

## 백업
- 기존 PaperMod 블로그 = git 브랜치 `archive/papermod-blog` 에 보존됨.
- 기존 DNS 레코드 스냅샷: A=183.111.161.147 / www·* CNAME→apex / MX mw-002.cafe24.com / SPF.
