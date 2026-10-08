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
