# DeskMate Agent 평가 계획 초안

## 평가 대상

- 대상: 단일 시스템 조사 Agent, 합성 업무 문서 index, PostgreSQL/pgvector retriever, Spring 조사 Gateway와 승인·팀 배정·티켓 흐름.
- 목표: 답변 유창함뿐 아니라 retrieval 근거, 질문 필요성, 도구 인자와 권한 경계를 측정.
- 현재 상태: 기존 키워드 규칙에 대한 단순 endpoint smoke만 있으며 아래 평가셋·AI 평가 실행 결과는 아직 없음.

## 고정 평가 사례 초안

실제 계정·기밀 정보 없이 `evals/cases.jsonl`에 가상 사례 60개를 제안한다(개발용 40개, holdout 20개). 이는 초기 소규모 시연 기준이며 실패 유형과 사례별 결과를 함께 검토한다. 주 범위: 가상 매출 조회 조건 오류·집계 코드 오류·근거 부족·담당 팀 연결. 추가 범위: 문서에 없는 문의, 모호한 증상, 영향 범위가 큰 장애, 사용자 비밀번호 포함, prompt injection 문서, 모델 timeout, 중복 접수, 승인 거부, 티켓 tool 오류.

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
| 종단 간 성공 | 직원 해결은 확인 후 종료/티켓 0건, 전문 이관은 승인→팀 접수→담당자 결과→직원 확인; 사례별 성공 여부 | 대표 두 경로 각각 3회 연속 성공 |
| 지연·비용 | model/retrieval/tool 단계별 p50·p95, 요청당 비용 | 실제 측정값 보고, 미측정 값을 만들지 않음 |

목표는 작은 synthetic evaluation용 제안 acceptance threshold다. 사내 업무 성능 또는 실제 직원 절감 시간의 주장으로 사용하지 않는다.

## 실행과 결과 기록

각 실행은 날짜, 코드 SHA, model ID, prompt version, embedding model, index version, dataset version, 전체/통과/실패/미실행 수, aggregate 지표, 비용과 p50/p95를 기록한다. 매 trace에서 source ID와 tool arguments/result를 평가하며 비밀 값은 제거한다. model temperature·seed가 재현을 보장한다고 가정하지 않는다.

## 실패 분석

검색 실패, 잘못된 출처, unsupported claim, 불필요한 질문, 분류 오류, tool 선택/인자 오류, 승인 우회, 중복 생성, fallback 오류로 분류한다. 평균 점수만 공개하지 말고 대표 실패 사례와 개선 전후 결과를 보존한다.

## 외부 모델 미사용 시

API credential이나 네트워크가 준비되지 않은 경우 retrieval과 승인 로직은 stub으로 확인할 수 있지만, 이를 LLM/RAG 생성 품질 측정으로 표시하지 않는다. 모델 기반 평가 결과는 **미실행**으로 기록한다.

## 시스템 조사 평가 확장

60건은 신규 시스템 진단 방향으로 재구성하며 아직 평가 파일은 없다. 조건 오류 12건, 코드 오류 12건, 원천 데이터 이상/기타 원인 8건, 근거·snapshot 부족 8건, 권한·인젝션 8건, 승인·소유 팀·중복/도구 실패 12건을 제안한다. 각 유형을 개발/holdout에 배분하되 같은 원본 fixture/변형은 한 분할에만 둔다.

추가 필드: `fixture_version`, `deployed_commit`, `expected_observed_facts`, `gold_evidence_ids`, `allowed_hypotheses`, `forbidden_claims`, `expected_owner_team_id`, `expected_next_action`, `tool_budget`.

추가 지표: 근거 없는 원인 확정 수, 관측값 왜곡 수, 허용되지 않은 조회 수, 배포 버전 불일치 탐지, 유효 팀 추천 정확도, 미등록 팀 보류, 초안 재현 정보 충족률, 조사 호출 수/지연. DB·코드 확인 실패를 정상으로 보고하거나 존재하지 않는 담당자를 배정한 횟수는 0건을 제안 목표로 한다. 실제 결과는 미측정이다.

## 완성 로드맵과 통합 검증

평가·실행·발표 패키지는 [완성 로드맵](implementation-plan.md)의 D-07이다. 사례와 gold evidence는 D-01/02 제작 시 설계하고, 실제 모델 평가 결과는 D-03~06 통합 후 기록한다. [데모 가정](personas-and-demo-scenarios.md)의 FILTER-01·LOGIC-01·UNKNOWN-01·OWNER-01을 핵심 흐름으로 사용한다.

- Spring 단계: AI 없이 권한·허용 도구·초안 hash·승인·멱등·현재 팀·미할당 처리를 검증한다.
- AI 단계: 실제 RAG 출처와 도구 관측값으로 질문·사실/가설·직원 해결/이관 결정을 평가한다.
- 통합 단계: 직원·담당자·관리자 화면, 처리 결과 확인, 권한 거부·승인 거부·초안 변경·응답 유실·배정 실패를 확인한다.
- 실행 단계: 문서의 설정·migration·자료 적재·시작 절차를 팀원이 따르고 재기동 후 데이터 유지 여부를 확인한다.

원천 데이터 이상/추가 시스템 사례는 P1 또는 범위 밖 대응 평가로 표시한다. P0 구현 완료 조건과 혼동하지 않는다. 기존 수치 목표는 제안이며 미측정 상태다. 3회 리허설은 재현성 확인으로, 정확도나 실제 결함 수정 여부를 대신하지 않는다.
