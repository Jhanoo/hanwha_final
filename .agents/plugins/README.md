# IT Agent 프로젝트 플러그인

공식 출처: https://github.com/openai/plugins

검토·고정한 커밋: `5fd93af4cd0c623e020d0cc7e9ce178b4ac1f70f`

| 플러그인 | 버전 | 사용 목적 | 추가 요구 사항 |
| --- | --- | --- | --- |
| openai-developers | 1.2.3 | Agents SDK 구현, OpenAI API 문제 해결, ChatGPT Apps 개발 | 실제 모델 호출에는 API 인증 필요 |
| plugin-eval | 0.1.2 | 코딩 스킬·플러그인 구조 및 토큰 예산 평가 | Node.js 20 이상 |

이는 Codex 개발 도구다. 설치만으로 DeskMate 챗봇이 LLM 또는 Jira와 연동되지는 않는다. Plugin Eval은 스킬·플러그인 평가 도구이며 챗봇 답변 정확도 평가 도구가 아니다.

## Mac에서 설치

저장소 변경을 내려받고 저장소 루트에서 실행한다.

```bash
git pull
bash scripts/setup-codex-plugins.sh
```

스크립트는 공식 저장소를 `.local/codex-plugins`에 내려받아 고정한 버전으로 준비하고, `hanwha-it-agent` marketplace를 등록한 뒤 두 플러그인을 설치한다. Codex CLI에 `plugin add`와 `plugin marketplace add` 명령이 필요하다. 명령이 없다면 Codex를 업데이트한다. 기존 사용자 설정을 덮어쓰지 않고 Codex의 공식 등록 명령을 사용한다.

설치 후 Codex를 재시작하고 확인한다.

```bash
codex plugin list --marketplace hanwha-it-agent
```


## 다운로드만 준비하거나 평가 CLI 사용

```bash
bash scripts/setup-codex-plugins.sh --prepare-only
node .local/codex-plugins/plugins/plugin-eval/scripts/plugin-eval.js analyze .agents/skills/frontend-design --format markdown
```

클라우드에서는 다운로드, manifest 인식, Plugin Eval CLI 실행을 확인했다. Codex 전역 설정 디렉터리가 읽기 전용이어서 전역 설치·활성화는 완료하지 못했다. 실제 LLM 호출은 검증하지 않았다. Plugin Eval의 정적 평가에서는 frontend-design의 토큰 예산과 트리거 설명 개선을 제안했다. 이는 실제 작업 성능 측정 결과가 아니다.

배포본은 원본 라이선스를 유지한 `.local` 체크아웃에 보관하고 GitHub 프로젝트에는 복사하지 않는다. `openai-developers` manifest는 Proprietary, `plugin-eval`은 MIT로 선언되어 있으므로 각각 원본 조건을 따른다. 버전을 자동으로 최신화하지 않으며 업데이트 시 manifest, 실행 스크립트, 인증 및 라이선스를 다시 검토한다.

## 기존 로컬 설치 정리

이전에 프로젝트 marketplace에서 Rovo를 설치했다면 Mac에서 다음 명령으로 제거한다. 이번 변경은 다른 marketplace에서 설치한 플러그인을 자동 삭제하지 않는다.

```bash
codex plugin remove atlassian-rovo@hanwha-it-agent
```
