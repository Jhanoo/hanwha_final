---
name: project-database
description: ERD, 데이터 사전, SQLite 또는 PostgreSQL 스키마, DB 생성과 마이그레이션을 작업할 때 사용한다.
---

# DB 설계와 생성·마이그레이션

프로젝트 루트 `AGENTS.md`와 커밋 규칙을 따른다. 사용자 요구와 기존 코드를 먼저 읽고, 현재 구현·계획·가정·검증 결과를 구분한다. 이 스킬은 현재 프로젝트를 위해 작성한 로컬 지침이다.

## 작업 순서

1. 현재 티켓 앱 저장소는 PostgreSQL + pgvector다. `.local/tickets.db`는 보존용 legacy 소스이며 `docs/database.md`의 migration·이관 상태를 확인한다.
2. `docs/database.md`에 Mermaid ERD, 테이블·컬럼·키·관계·제약·인덱스·삭제 정책·시간대·보존 정책을 적는다.
3. 직원, 대화, 티켓, 티켓 이벤트, 지식 문서는 요구사항에 필요한 것만 설계한다. 스키마와 API의 ID·상태 타입을 맞춘다.
4. 생성 SQL과 버전 순서가 명확한 마이그레이션을 `db/`에 작성한다. 적용 이력, 재실행 정책, 데이터 전환 및 실패 시 복구를 정의한다.
5. DB 생성을 요청받았으면 새 임시 DB에서 실제 SQL을 실행하고 PK/FK/NOT NULL/CHECK/UNIQUE, CRUD와 롤백을 검증한다. SQLite는 연결별 `PRAGMA foreign_keys=ON`을 고려한다.
6. 변경은 기존 데이터에 대해 덮어쓰기·DROP·초기화를 기본값으로 삼지 않는다. 복구 가능한 백업과 검증 후 승인된 대상에 적용한다.
7. PostgreSQL 대상이면 `supabase-postgres-best-practices`도 읽고 SQLite 문법을 그대로 적용하지 않는다.
8. `.local/tickets.db`를 커밋하지 않는다. 가짜 데모 데이터만 seed로 만들고 변경 후 데이터 보존을 확인한다.
9. 수행한 DB 생성·마이그레이션·검증과 SQL만 작성한 상태를 구분해 보고한다.

## 산출물 템플릿

[템플릿](references/template.md)을 필요한 부분만 사용한다. 요청받은 작업을 실행하고 결과를 검증한다. 이 템플릿 자체는 완성된 제품 문서나 실행 결과가 아니다.
