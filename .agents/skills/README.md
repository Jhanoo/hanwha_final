# 프로젝트 Agent 스킬

Codex 프로젝트 스킬 탐색 경로인 `.agents/skills/<name>/SKILL.md`에 필요한 스킬만 저장합니다. 현재 세션의 스킬 목록은 즉시 갱신되지 않을 수 있으므로 `AGENTS.md`에서도 파일을 직접 참조합니다.

| 스킬 | 용도 | 출처 | 기준 커밋 | 라이선스 |
| --- | --- | --- | --- | --- |
| frontend-design | UI 설계, 반응형·접근성·화면 문구 개선 | https://github.com/anthropics/skills/tree/main/skills/frontend-design | `683bc88e56f3e09ba94f7055977f3d3aa499f202` | Apache-2.0 |
| playwright | 실제 브라우저 조작, 스크린샷, 사용자 흐름 검증 | https://github.com/openai/skills/tree/main/skills/.curated/playwright | `49f948faa9258a0c61caceaf225e179651397431` | Apache-2.0 |

원본 LICENSE와 NOTICE(있는 경우), 참조 문서 및 스크립트를 보존합니다. Playwright의 SKILL.md에서 전역 설치 경로만 프로젝트 경로로 수정했습니다. 스킬은 AI 코딩 작업을 위한 지침이며 애플리케이션 런타임 의존성이 아닙니다.

## Playwright 사용

Node.js/npm의 `npx`가 필요합니다. 저장소 루트에서:

```bash
export PWCLI="$PWD/.agents/skills/playwright/scripts/playwright_cli.sh"
# 클라우드의 기본 홈 캐시가 쓰기 불가능할 때 사용
export npm_config_cache=/workspace/.cache/npm
bash "$PWCLI" --help
```

래퍼는 첫 실행 시 npm에서 `@playwright/cli`를 가져옵니다. 실제 브라우저 실행에는 브라우저 설치와 시스템 의존성이 추가로 필요할 수 있습니다. 스킬 파일 추가만으로 브라우저 런타임이 설치되지는 않습니다. 생성 결과는 `output/playwright/`에 저장하고 버전 관리에서 제외합니다.

업데이트는 위 출처에서 새 버전을 검토한 뒤 라이선스, 참조 파일, 로컬 경로 수정을 유지하며 기준 커밋을 갱신합니다. 원격 스크립트를 자동 업데이트하거나 임의 실행하지 않습니다.

## 프로젝트 진행 스킬 구성

작업별로 아래 스킬 하나를 먼저 읽고 필요한 보조 스킬만 추가합니다. 스킬 설치만으로 PRD·DB·테스트·배포가 실행되지는 않습니다. 새 Codex 세션에서 프로젝트 스킬을 탐색할 수 있으며, 현재 세션에서는 `AGENTS.md`의 경로로 직접 읽을 수 있습니다.

| 단계 | 스킬 | 주요 산출물 | 종류 |
| --- | --- | --- | --- |
| 제품 기획 | [project-prd](project-prd/SKILL.md) | `docs/prd.md` | 프로젝트 전용 |
| 요구사항 | [project-requirements](project-requirements/SKILL.md) | `docs/requirements.md`, `docs/traceability.md` | 프로젝트 전용 |
| 시스템 설계 | [project-architecture](project-architecture/SKILL.md) | `docs/architecture.md`, ADR, 구현 계획 | 프로젝트 전용 |
| DB 설계·생성 | [project-database](project-database/SKILL.md) | ERD, 데이터 사전, `db/` 생성·마이그레이션 SQL | 프로젝트 전용 |
| PostgreSQL | [supabase-postgres-best-practices](supabase-postgres-best-practices/SKILL.md) | 제약·인덱스·성능·RLS 검토 | Supabase 공개 스킬 |
| API·티켓 연동 | [project-api-contract](project-api-contract/SKILL.md) | API 명세, OpenAPI, TicketAdapter 계약 | 프로젝트 전용 |
| MCP 도구 | [mcp-builder](mcp-builder/SKILL.md) | 외부 API 도구 설계·구현·평가 | Anthropic 공개 스킬 |
| AI·지식 검색 평가 | [project-agent-evaluation](project-agent-evaluation/SKILL.md) | 평가 시나리오, 근거·도구 호출·이관 검증 | 프로젝트 전용 |
| UI | [frontend-design](frontend-design/SKILL.md) | 화면 설계·접근성·반응형 구현 | Anthropic 공개 스킬 |
| 브라우저 조작 | [playwright](playwright/SKILL.md) | 화면 점검·사용자 흐름 검증 | OpenAI 공개 스킬 |
| Python 웹 자동화 | [webapp-testing](webapp-testing/SKILL.md) | Python Playwright 테스트·서버 실행 보조 | Anthropic 공개 스킬 |
| 테스트·CI·전달 | [project-delivery](project-delivery/SKILL.md) | 테스트 계획, CI, 운영 문서, 발표 시나리오 | 프로젝트 전용 |

기본 순서: PRD → 요구사항 → 설계·DB·API → 구현 → 기능·AI 평가 → 데모·전달. 이미 확정되거나 구현된 단계는 재작성하지 않습니다. UI 검증은 Playwright CLI와 Python 자동화 중 하나를 선택합니다. PostgreSQL 스킬은 PostgreSQL 작업에만 적용하며 SQLite를 바꾸는 근거로 삼지 않습니다.

## 추가 공개 스킬 출처

| 스킬 | GitHub 출처 | 기준 커밋 | 라이선스 |
| --- | --- | --- | --- |
| mcp-builder | https://github.com/anthropics/skills/tree/main/skills/mcp-builder | `683bc88e56f3e09ba94f7055977f3d3aa499f202` | Apache-2.0 |
| webapp-testing | https://github.com/anthropics/skills/tree/main/skills/webapp-testing | `683bc88e56f3e09ba94f7055977f3d3aa499f202` | Apache-2.0 |
| supabase-postgres-best-practices | https://github.com/supabase/agent-skills/tree/main/skills/supabase-postgres-best-practices | `c9be0e931b7930f7d02126d04774d904c381e7d7` | MIT |

각 스킬의 참조·스크립트·라이선스 파일을 보존했습니다. PostgreSQL 스킬은 루트 MIT LICENSE도 함께 보존했습니다. 프로젝트 전용 스킬 7개는 이 저장소를 위해 작성한 지침과 템플릿이며 외부 스킬의 복사본으로 표시하지 않습니다. Anthropic의 `doc-coauthoring`은 문서 작성 후보로 검토했지만 해당 디렉터리에 명시적인 LICENSE가 없어 재배포하지 않았습니다. PRD·명세는 프로젝트 전용 지침으로 제공합니다.

## 실행 의존성

- 문서·ERD·API 명세 작성에는 추가 런타임 패키지가 필요 없습니다.
- SQLite 생성·검증은 `.venv/bin/python`의 표준 라이브러리를 사용합니다.
- Python 웹 자동화 실행 시 uv로 가상환경에 Playwright를 설치하고 브라우저도 준비해야 합니다. 이 변경에서는 패키지나 브라우저를 설치하지 않았습니다. 실제 테스트 작업 시 필요한 의존성을 선언·고정하세요.
- MCP 예제는 사용하는 SDK와 인증이 필요합니다. 스킬 폴더의 requirements를 애플리케이션 의존성에 무조건 합치지 않습니다.
- 실제 LLM 평가와 외부 티켓 테스트는 해당 인증이 있어야 실행할 수 있습니다.
- `openai/skills`는 deprecated 상태입니다. 기존 Playwright 복사본은 보존하되 후속 업데이트는 공식 `openai/plugins` 배포도 확인합니다.
