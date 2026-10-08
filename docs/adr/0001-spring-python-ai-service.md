# ADR 0001: Spring 제품 백엔드와 Python AI 서비스 분리

- 상태: 제안됨
- 날짜: 2026-10-08

## 맥락

팀은 Java에 익숙하며 프로젝트는 티켓 업무 API와 AI 기술 시연을 함께 필요로 한다. 현재 저장소는 Python 규칙 기반 서버이며 PostgreSQL 티켓 저장은 구현됐지만 LLM과 RAG는 아직 구현되지 않았다.

## 제안 결정

Spring Boot가 외부 API, 인증·인가, 상담 흐름, 승인, 티켓, 담당자 할당과 업무 데이터 쓰기를 맡는다. Python 내부 서비스는 Agents SDK, LLM 호출, RAG, 지식 문서 ingestion과 검색을 맡는다. Web UI는 Spring만 호출하고 Spring이 Python에 내부 HTTP/JSON 요청을 보낸다.

Spring은 승인·권한·티켓 생성의 최종 책임자다. Python 모델 출력은 응답·근거·티켓 초안 제안으로만 취급하고 티켓 테이블에 직접 쓸 수 없다. 초기에는 PostgreSQL + pgvector 한 인스턴스를 공유하되 Spring 업무 테이블과 Python 지식 인덱스의 소유권, DB role을 분리한다.

## 대안

1. Python 단일 백엔드: 현재 코드 재사용이 쉽고 AI 통합이 빠르지만 팀의 Java 역량과 제품 API 주력 언어가 달라진다.
2. Spring 단일 백엔드: 배포·보안·업무 데이터 경계가 단순하지만 Python AI 생태계와 평가 도구를 사용할 때 통합 선택이 제한될 수 있다.
3. Spring + Python AI 서비스: 업무 API와 AI 실험의 책임을 분리할 수 있지만 서비스 간 계약·배포·관측·DB 권한 운영이 추가된다.

## 결과 및 검증 과제

- Spring↔Python 내부 API schema, 인증, timeout, 오류/재시도 규칙을 확정해야 한다.
- PostgreSQL 공유 계정이 아닌 최소 권한 서비스별 DB role과 migration 소유권을 설계해야 한다.
- Python AI 서비스 장애 시 Spring은 실패를 분명히 반환하고 티켓을 생성하지 않아야 한다.
- 현재 Python 티켓 API 이관은 기능·상태 매핑·데이터 보존을 검증한 뒤 진행한다.
- 모델 API 호출 비용·한국어 품질·민감 정보 처리와 다중 서비스 운영 부담을 통합 평가한다.
- 단일 모델 API 호출만 남고 Python 전용 RAG/평가 필요가 없다면 Python 서비스를 합치는 선택을 재검토한다.

이 ADR은 설계 방향 제안이며 구현 확정이나 서비스 이관 완료를 뜻하지 않는다.
