# DeskMate AI Agent 구현 계획 초안

## 0단계: 계약과 기준선

- PRD·요구사항·아키텍처를 검토하고 모델 접근, synthetic 자료, demo 환경을 확정.
- 기존 endpoint와 ticket DB의 동작을 고정한 baseline 시나리오 확보.
- 완료: FR/PRD traceability, 선택 기술 ADR, 비밀 없는 설정 예시.

## DB 우선 단계: PostgreSQL + pgvector

- Docker Compose에 고정한 PostgreSQL + pgvector image와 persistent local volume 구성.
- async 또는 sync Python PostgreSQL driver와 migration runner 선정, uv dependency에 고정.
- `db/migrations/001_initial_schema.sql`은 현재 초안이므로 새 로컬 DB에서 extension, migration, constraint, vector search를 검증한 뒤 확정.
- 현재 SQLite ticket DB를 지우지 않고 새 PostgreSQL DB로 import하고 count/상태를 비교.
- 완료: compose health, 확장·schema, CRUD, pgvector top-k 검색, 재기동 후 데이터 유지, rollback 절차 검증.

## 1단계: Agent runtime과 상담 API

- Python 앱 설정에 model provider, model ID, timeout, feature mode를 주입.
- 규칙 모드는 fallback으로 유지하고 Agent 호출 모드 상태를 UI에 분명히 표시.
- 대화 입력/출력 schema, request ID, 오류 분류 적용.
- 완료: 유효/잘못된 입력, provider timeout, API key 미설정 fallback이 검증됨.

## 2단계: synthetic 지식 corpus와 RAG

- source metadata/버전이 포함된 VPN·계정·메일 가이드 작성.
- 문서 분할, embedding 생성, index version을 재현 가능한 ingestion command로 구현.
- 검색 도구는 top-k 구절·source ID·score를 반환하고 답변에 출처 노출.
- 완료: gold source 평가, 검색 0건 fallback, 문서 prompt injection 테스트.

## 3단계: Agent 도구와 승인 경계

- 읽기 검색·요약과 쓰기 티켓 API 계약 정의.
- 사용자 검토 가능한 ticket draft, 서버 검증 approval ID, idempotency key 구현.
- TicketAdapter를 PostgreSQL에 연결하고 상태 전이와 변경 이력을 추가.
- 완료: 승인 없는 쓰기 0건, 반복 호출 중복 0건, 담당자 상태 변경 확인.

## 4단계: 평가 harness와 증거 UI

- `evals/cases.jsonl` synthetic 사례 최소 20건 생성 및 고정.
- retrieval, grounding, classification, tool, safety, latency/cost metric 산출.
- UI에 검색 근거, tool trace 요약, 티켓 draft, 결과를 보기 쉽게 표시.
- 완료: 실행 결과가 dataset/model/index/code version과 함께 저장되고 실패를 재현할 수 있음.

## 5단계: 통합 리허설과 발표

- happy path와 검색·모델·DB 오류 path 리허설.
- 모바일/키보드 접근, localhost 설정, 데모 DB reset 절차 점검.
- 발표 순서: 아키텍처 → RAG 근거 → tool trace → 승인 → 티켓 → 평가 실패 분석.
- 완료: 동일 환경에서 3회 연속 종단 간 시연, 미구현/미실행 범위 명시.

## 의존성과 위험

- 모델 호출을 위해 실제 credential 및 네트워크 access가 필요할 수 있음.
- embedding 비용, 한국어 검색 성능, 모델 비결정성이 평가 결과에 영향.
- SQLite ticket DB에서 PostgreSQL로 데이터 이관할 경우 backup·행 수·ID·상태 비교가 필요.
- 인증 없는 localhost 데모를 공용 네트워크에 공개하지 않음.
