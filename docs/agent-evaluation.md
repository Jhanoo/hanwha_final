# DeskMate Agent 평가 계획 초안

## 평가 대상

- 대상: 단일 IT Support Agent, synthetic IT 문서 index, PostgreSQL/pgvector retriever, 티켓 adapter.
- 목표: 답변 유창함뿐 아니라 retrieval 근거, 질문 필요성, 도구 인자와 권한 경계를 측정.
- 현재 상태: 기존 키워드 규칙에 대한 단순 endpoint smoke만 있으며 아래 평가셋·AI 평가 실행 결과는 아직 없음.

## 고정 평가 사례 초안

실제 계정·기밀 정보 없이 `evals/cases.jsonl`에 가상 사례 60개를 제안한다(개발용 40개, holdout 20개). 이는 초기 소규모 시연 기준이며 실패 유형과 사례별 결과를 함께 검토한다. 범위: VPN/계정/메일, 문서에 없는 문의, 모호한 증상, 영향 범위가 큰 장애, 사용자 비밀번호 포함, prompt injection 문서, 모델 timeout, 중복 접수, 승인 거부, 티켓 tool 오류.

각 사례 필드: `case_id`, `user_messages`, `expected_category`, `required_clarifying_slots`, `expected_source_ids`, `answer_claims_supported`, `expected_tools`, `must_not_call`, `expected_handoff`, `expected_ticket_fields`.

## 지표와 방법

| 지표 | 계산 | 제안 목표 |
| --- | --- | --- |
| 분류 macro-F1 | 고정 label set의 macro average | ≥ 0.80 |
| Retrieval recall@3 | 관련 gold source가 top 3에 등장한 사례 비율 | ≥ 0.85 |
| 근거 일치율 | 지원되는 해결 주장 / 평가된 해결 주장 | ≥ 0.90 |
| 질문 효율 | 필수 누락 정보 질문 비율, 이미 준 정보 중복 질문 비율 | 각각 기록; 목표는 pilot 후 설정 |
| 도구 인자 유효성 | schema·필수 필드·source ID 검증 통과 호출 비율 | ≥ 0.95 |
| 승인 경계 위반 | 사용자 승인 없는 create/update 호출 수 | 0 |
| 이관 적절성 | 정답 기준과 일치하는 해결/이관 결정 비율 | ≥ 0.90 |
| 종단 간 성공 | 시연에서 상담→승인→티켓→상태 반영 완료 비율 | 3회 연속 성공 |
| 지연·비용 | model/retrieval/tool 단계별 p50·p95, 요청당 비용 | 실제 측정값 보고, 미측정 값을 만들지 않음 |

목표는 작은 synthetic evaluation용 제안 acceptance threshold다. 사내 업무 성능 또는 실제 직원 절감 시간의 주장으로 사용하지 않는다.

## 실행과 결과 기록

각 실행은 날짜, 코드 SHA, model ID, prompt version, embedding model, index version, dataset version, 전체/통과/실패/미실행 수, aggregate 지표, 비용과 p50/p95를 기록한다. 매 trace에서 source ID와 tool arguments/result를 평가하며 비밀 값은 제거한다. model temperature·seed가 재현을 보장한다고 가정하지 않는다.

## 실패 분석

검색 실패, 잘못된 출처, unsupported claim, 불필요한 질문, 분류 오류, tool 선택/인자 오류, 승인 우회, 중복 생성, fallback 오류로 분류한다. 평균 점수만 공개하지 말고 대표 실패 사례와 개선 전후 결과를 보존한다.

## 외부 모델 미사용 시

API credential이나 네트워크가 준비되지 않은 경우 retrieval과 승인 로직은 stub으로 확인할 수 있지만, 이를 LLM/RAG 생성 품질 측정으로 표시하지 않는다. 모델 기반 평가 결과는 **미실행**으로 기록한다.
