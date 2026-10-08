# 요구사항 추적성 초안

| PRD | 요구사항 | 설계/API/화면/DB 산출물 | 테스트·평가 | 구현 상태 |
| --- | --- | --- | --- | --- |
| PRD-001 | FR-001 | Conversation API, 대화 화면 | 질문 슬롯 평가 | 목표 |
| PRD-002 | FR-002, FR-003 | Knowledge Retriever, 출처 UI, 문서 index | recall@3, 근거 일치 | 목표 |
| PRD-003 | FR-004 | Agent tools, 상담 요약 | schema·tool trace 평가 | 목표 |
| PRD-004 | FR-005, FR-006 | 승인 UI, TicketAdapter, idempotency key | 승인 없는 쓰기·중복 테스트 | 목표 |
| PRD-005 | FR-007 | 담당자 화면, ticket status/history | CRUD·상태 전이 테스트 | 일부 구현: ticket status |
| PRD-006 | FR-008, FR-010 | 오류 처리, 신뢰 경계 | provider/tool/prompt injection 평가 | 목표 |
| PRD-007 | FR-009 | evaluation harness, 결과 저장 | 고정 synthetic set | 미구현 |
| PRD-001~007 | NFR-001~006 | runbook, trace, UI, DB | 권한·개인정보·접근성·지연 검증 | 목표 |

요구사항이 변하면 이 표와 `docs/requirements.md`, `docs/agent-evaluation.md`를 함께 갱신한다. “일부 구현”은 새 AI 요구사항 완료를 뜻하지 않는다.

## 시스템 진단 확장 추적

| PRD | 요구사항 | 설계 산출물 | 평가 | 상태 |
|---|---|---|---|---|
| PRD-008 | FR-013, FR-014 | investigation-design.md 도구 Gateway·fixture | 조회 권한·관측값·배포 버전 | 목표 |
| PRD-009 | FR-015, FR-017 | 사실/가설 응답·직원 해결/이관 | 허위 확정·적절한 이관 | 목표 |
| PRD-010 | FR-016 | owner registry·Spring 배정 | 유효 팀·미등록 큐 | 목표 |
| PRD-004, PRD-008 | FR-018 | 조사 근거 포함 초안·승인 hash | 초안 완전성·승인 변경 | 목표 |
| PRD-006 | FR-019 | 도구 예산·거부/timeout | 권한 우회·반복 호출 | 목표 |

## 프로젝트 완성 산출물 추적

산출물과 구현 순서는 [완성 로드맵](implementation-plan.md)을 기준으로 한다. 아래 검증은 수행해야 할 계획이며 새 실행 결과가 아니다.

| 산출물 | 요구사항 | 산출물/검증 연결 | 구현 상태 |
|---|---|---|---|
| D-01 가상 업무 시스템 | FR-013, FR-014, FR-017 | sales-demo 화면/API; FILTER-01 80→100만 원, LOGIC-01 90만 원 재현 | 미구현 |
| D-02 조사 자료 | FR-002, FR-003, FR-014, FR-016 | 주문·문서·로그·코드·registry; snapshot/버전과 gold evidence 대조 | 문서 가정만 있음 |
| D-03 Spring 제품 백엔드 | FR-005~008, FR-012, FR-016, FR-018 | 사용자·권한·대화·승인·티켓·이력; hash/멱등/팀 배정 검증 | 미구현; 기존 Python 티켓 기능 이관 필요 |
| D-04 Spring Gateway | FR-013, FR-014, FR-016, FR-019 | 등록 읽기 도구; 권한/입력/예산/마스킹과 실패 응답 검증 | 미구현 |
| D-05 Python AI | FR-001~004, FR-008, FR-010, FR-011, FR-015, FR-017, FR-018 | RAG·Agent; 검색/도구 trace, 사실/가설, 안내/초안 평가 | 미구현; 지식 schema만 준비 |
| D-06 직원·담당자 화면 | FR-005, FR-007, FR-016~018, NFR-006 | 근거·승인·보드·미할당; 역할별 종단 간 및 키보드 검증 | 기존 규칙/티켓 UI만 있음 |
| D-07 평가·실행·발표 | FR-009, NFR-001~008 | 고정 평가·결과/trace·Compose·실행 안내; 리허설과 팀원 재현 | 기존 Python/DB 안내와 smoke만 있음 |
