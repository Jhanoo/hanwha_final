# DeskMate AI Agent 구현 계획 초안

## 0단계: 계약과 기준선

- PRD·요구사항·아키텍처를 검토하고 모델 접근, synthetic 자료, demo 환경을 확정.
- 기존 endpoint와 ticket DB의 동작을 고정한 baseline 시나리오 확보.
- 완료 기준: FR/PRD traceability, 선택 기술 ADR, 비밀 없는 설정 예시.

## 1단계: PostgreSQL + pgvector 전환

- 완료: Docker Compose PostgreSQL + pgvector image와 persistent local volume 구성.
- 완료: Psycopg driver, uv dependency, migration runner 구성.
- 완료: migration, pgvector extension, ticket CRUD와 cosine distance smoke 검증. embedding retrieval 및 운영 규모 index 성능은 미검증.
- 완료: SQLite 원본 보존. 기존 source DB 티켓 0건 확인 후 import 실행.
- 미완료: 재기동 후 persistent volume 확인과 migration rollback 검증.

## 2단계: 모델 기준선과 Agent runtime

- `docs/llm-strategy.md`의 후보가 API 계정에서 실제 제공되는지, 도구 호출·구조화 출력 지원과 최신 가격을 확인.
- 우선 API 모델 1종을 연결하고 모델/embedding model 이름을 환경 변수로 주입. API key는 안전한 환경 설정으로 관리.
- Holdout 사례를 동결한 뒤 동일 조건의 가용 모델 후보를 비교하고 지연·호출비용·실패 사례 기록.
- 현재 기준선에서 prompt/RAG/tool schema 수정으로 해결할 오류와 fine-tuning 대상 오류를 구분.
- 완료 기준: 선택 근거, model ID, SDK 버전, 비용 측정 방법과 미검증 항목 기록.

## 3단계: synthetic 지식 corpus와 RAG

- source metadata/버전이 포함된 VPN·계정·메일 가이드 작성.
- 문서 분할, embedding 생성, index version을 재현 가능한 ingestion command로 구현.
- 검색 도구는 top-k 구절·source ID·score를 반환하고 답변에 출처 노출.
- 완료 기준: gold source 평가, 검색 0건 fallback, 문서 prompt injection 테스트.

## 4단계: Agent 도구와 승인 경계

- 읽기 검색·요약과 쓰기 티켓 API 계약 정의.
- 사용자 검토 가능한 ticket draft, 서버 검증 approval ID, idempotency key 구현.
- TicketAdapter를 PostgreSQL에 연결하고 상태 전이와 변경 이력을 추가.
- 완료 기준: 승인 없는 쓰기 0건, 반복 호출 중복 0건, 담당자 상태 변경 확인.

- 튜닝은 holdout 기준선 및 데이터 이용 허가를 갖춘 후 별도 실험 승인/작업으로 진행.

## 5단계: 평가 harness와 증거 UI

- `evals/cases.jsonl` synthetic 사례 60건(개발용 40, holdout 20) 작성 후 고정.
- retrieval, grounding, classification, tool, safety, latency/cost metric 산출.
- UI에 검색 근거, tool trace 요약, 티켓 draft, 결과를 보기 쉽게 표시.
- 완료 기준: 실행 결과가 dataset/model/index/code version과 함께 저장되고 실패를 재현할 수 있음.

## 6단계: 통합 리허설과 발표

- happy path와 검색·모델·DB 오류 path 리허설.
- 모바일/키보드 접근, localhost 설정, 데모 DB reset 절차 점검.
- 발표 순서: 아키텍처 → RAG 근거 → tool trace → 승인 → 티켓 → 평가 실패 분석.
- 완료 기준: 동일 환경에서 3회 연속 종단 간 시연, 미구현/미실행 범위 명시.

## 의존성과 위험

- 모델 호출을 위해 실제 credential 및 네트워크 access가 필요할 수 있음.
- embedding 비용, 한국어 검색 성능, 모델 비결정성이 평가 결과에 영향.
- SQLite ticket DB에서 PostgreSQL로 데이터 이관할 경우 backup·행 수·ID·상태 비교가 필요.
- 인증 없는 localhost 데모를 공용 네트워크에 공개하지 않음.
