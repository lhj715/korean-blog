# ruflo (claude-flow v3) 로컬 설치 가이드

[ruvnet/ruflo](https://github.com/ruvnet/ruflo)는 Claude Code용 에이전트 오케스트레이션
도구입니다(구 claude-flow). 100+ 전문 에이전트, 스웜 조율, 벡터 메모리(AgentDB) 등을
제공합니다.

이 저장소에는 ruflo 초기화로 생성된 **공유 설정**이 이미 커밋되어 있습니다:

| 경로 | 내용 |
|------|------|
| `CLAUDE.md` | ruflo 에이전트 조율 가이드 (Claude Code가 자동으로 읽음) |
| `.claude/` | 스킬 30개, 커맨드 16개, 에이전트 17개, 훅 설정(`settings.json`) |
| `.mcp.json` | claude-flow MCP 서버 등록 (`npx ruflo mcp start`) |

런타임 데이터(`.agents/`, `.swarm/`, `.claude-flow/`)는 용량이 크고 로컬에서
재생성되므로 `.gitignore`에 제외되어 있습니다.

## 사전 요구사항

- Node.js (v20 이상 권장, npm 포함)
- Claude Code CLI

## 로컬 설치 방법

저장소를 pull 받은 뒤, 프로젝트 루트에서 아래 명령 한 번이면 됩니다:

```bash
git pull
npx ruflo@latest init
```

이미 커밋된 `.claude/` 설정이 있으므로, 기존 설정을 덮어쓰고 최신으로 맞추려면:

```bash
npx ruflo@latest init --force
```

전역 설치를 원하면(선택):

```bash
npm install -g ruflo@latest
ruflo --version
```

## 설치 확인

```bash
npx ruflo@latest init check   # 초기화 상태 확인
npx ruflo@latest --version    # 버전 확인 (v3.32.x)
```

Claude Code를 프로젝트 루트에서 실행하면 `.mcp.json`의 claude-flow MCP 서버와
`.claude/` 스킬·에이전트가 자동으로 로드됩니다.

## 자주 쓰는 명령

```bash
ruflo daemon start    # 백그라운드 워커 시작
ruflo swarm init      # 스웜 초기화
ruflo init upgrade    # 데이터 보존하면서 헬퍼/statusline 업데이트
```

자세한 내용은 [공식 저장소](https://github.com/ruvnet/ruflo)를 참고하세요.
