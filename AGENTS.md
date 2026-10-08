# 프로젝트 작업 지침

## 기본 규칙

- 사용자와의 설명 및 프로젝트 문서는 한국어로 작성한다. 기술명은 원문을 유지한다.
- 작업 시작 시 [.codex/commit-rules.md](.codex/commit-rules.md)를 읽고 모든 신규 커밋에 적용한다. 커밋 전 Diff와 메시지 규칙 준수 여부를 확인한다.
- 기존 변경과 티켓 데이터를 보존한다. API 키, 비밀번호, 개인정보, `.venv`, `.local` 데이터를 커밋하지 않는다.
- 기존 클라우드 체크아웃을 사용한다. 사용자의 명시적 요청 없이 Git worktree를 만들지 않는다.

## 프로젝트와 실행

- 핵심 결과물은 사내 IT 상담 → 해결 가이드 → 미해결 티켓 접수 → 상태 조회·변경 데모다.
- `server.py`는 Python HTTP API와 PostgreSQL 저장소다. 연결 정보는 `.env`에서 읽고 migration은 `scripts/migrate.py`로 적용한다. `web/`은 HTML, CSS, JavaScript UI다.
- Python 명령은 uv로 생성한 `.venv`에서 실행한다. 생성: `UV_CACHE_DIR=/workspace/.cache/uv uv venv --python python3 .venv`. 실행: `.venv/bin/python server.py`.
- 현재 상담은 규칙 기반이며 티켓은 PostgreSQL이다. 기존 SQLite 파일은 이관 후에도 원본으로 보존한다. 실제 LLM·Jira·ServiceNow 연동 여부를 사실대로 구분하고 데모 기능을 실서비스 기능으로 설명하지 않는다.
- 실행·발표 흐름은 `README.md`를 참고한다.

## 필요한 스킬만 사용

- 화면 신설 또는 UI 디자인 변경 시 [.agents/skills/frontend-design/SKILL.md](.agents/skills/frontend-design/SKILL.md)를 읽는다. 한국어 업무 환경, 명확한 안내, 키보드 접근성, 모바일 화면을 고려한다.
- 브라우저 상호작용 또는 UI 흐름 검증 시 [.agents/skills/playwright/SKILL.md](.agents/skills/playwright/SKILL.md)를 읽는다. 래퍼는 저장소의 `.agents/skills/playwright/scripts/playwright_cli.sh`를 사용한다. `CODEX_HOME`을 변경하지 않는다.
- 스킬의 제안보다 사용자 요구와 기존 프로젝트 제약을 우선한다. 관련 없는 작업에는 스킬을 강제로 적용하지 않는다.
- 출처, 라이선스, 실행 전제는 [.agents/skills/README.md](.agents/skills/README.md)를 참고한다.

## 프로젝트 단계별 스킬 선택

- 전체 목록과 출처는 [.agents/skills/README.md](.agents/skills/README.md)를 읽는다. 모든 스킬을 한 번에 로드하지 않고 현재 작업에 필요한 지침만 읽는다.
- PRD·MVP 기획: [.agents/skills/project-prd/SKILL.md](.agents/skills/project-prd/SKILL.md)
- 요구사항 명세·수용 기준·추적: [.agents/skills/project-requirements/SKILL.md](.agents/skills/project-requirements/SKILL.md)
- 아키텍처·ADR·구현 계획: [.agents/skills/project-architecture/SKILL.md](.agents/skills/project-architecture/SKILL.md)
- ERD·DB 생성·마이그레이션: [.agents/skills/project-database/SKILL.md](.agents/skills/project-database/SKILL.md). PostgreSQL 작업에만 [.agents/skills/supabase-postgres-best-practices/SKILL.md](.agents/skills/supabase-postgres-best-practices/SKILL.md)를 함께 적용한다.
- API 명세·티켓 어댑터: [.agents/skills/project-api-contract/SKILL.md](.agents/skills/project-api-contract/SKILL.md). MCP 도구를 만들 때만 [.agents/skills/mcp-builder/SKILL.md](.agents/skills/mcp-builder/SKILL.md)를 추가 사용한다.
- 실제 AI·RAG·도구 호출 평가: [.agents/skills/project-agent-evaluation/SKILL.md](.agents/skills/project-agent-evaluation/SKILL.md)
- 테스트·CI·배포·발표: [.agents/skills/project-delivery/SKILL.md](.agents/skills/project-delivery/SKILL.md). Python 브라우저 자동화에는 [.agents/skills/webapp-testing/SKILL.md](.agents/skills/webapp-testing/SKILL.md)를 읽는다.
- 공개 스킬의 Claude 전용 도구명은 사용 가능한 Codex 도구로 대응한다. uv, 기존 데이터 보존, 프로젝트 경로와 사용자 요구를 우선한다. 외부 패키지·서비스를 설치한 것으로 가정하지 않는다.

## 변경 검증

- API 변경 시 정상 요청, 잘못된 입력, 해당 티켓 생성·조회·상태 변경을 검증한다. 검증 데이터는 기존 사용자 데이터와 구분하고 검증 중 만든 데이터만 정리한다.
- UI 변경 시 `node --check web/app.js`와 변경된 사용자 흐름을 확인한다. 가능하면 Playwright로 실제 브라우저에서 검증한다.
- 커밋 전 `git diff --check`와 `git status --short`로 의도하지 않은 변경을 확인한다.
- 수행한 검사와 미실행·실패한 검사를 구분해 보고한다. 필요한 기능 검증 없이 준비 완료로 표현하지 않는다.

## 프로젝트 플러그인

- 설치 및 요구 사항은 [.agents/plugins/README.md](.agents/plugins/README.md)를 참고한다. 설치 명령은 `bash scripts/setup-codex-plugins.sh`이며, `.local/codex-plugins`의 공식 배포본을 사용한다.
- 실제 LLM·Agents SDK 개발에는 `openai-developers`, 코딩 스킬 품질 평가에는 `plugin-eval`을 사용한다.
- 플러그인 파일이 있다는 이유로 설치·인증·외부 시스템 연결이 완료되었다고 가정하지 않는다. 필요한 작업 전에 가용성을 확인한다.
- 외부 메시지 발송이나 티켓 변경은 사용자가 해당 작업을 요청한 범위에서만 수행한다. 단순 플러그인 설치는 외부 데이터 쓰기를 허용하지 않는다.
