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
