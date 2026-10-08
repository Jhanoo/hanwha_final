---
name: project-api-contract
description: HTTP API 명세, OpenAPI, 외부 티켓 시스템 인터페이스와 연동 구현에 사용한다.
---

# API 명세와 티켓 어댑터

프로젝트 루트 `AGENTS.md`와 커밋 규칙을 따른다. 사용자 요구와 기존 코드를 먼저 읽고, 현재 구현·계획·가정·검증 결과를 구분한다. 이 스킬은 현재 프로젝트를 위해 작성한 로컬 지침이다.

## 작업 순서

1. 현재 `/api/chat`, `/api/tickets`, `/api/tickets/{id}`와 요구사항을 확인한다.
2. `docs/api.md`에 method, path, 역할, 인증, 요청·응답, 필드 제약, HTTP 상태, 오류 예시를 기록한다.
3. OpenAPI가 필요한 경우 `docs/openapi.yaml`을 만들고 문서·코드·상태 코드의 일치 여부를 확인한다.
4. `TicketAdapter`는 create/list/get/update_status 등 필요한 계약만 정의한다. SQLite, Jira, ServiceNow 구현을 계약 뒤에 둔다.
5. 티켓 생성의 사용자 의도, 중복 방지, timeout, 재시도와 외부 오류 매핑을 정한다. 비멱등 POST를 무조건 재시도하지 않는다.
6. 구현 요청이면 정상·잘못된 입력·미존재 ID·외부 실패를 실제 호출로 검증한다. 인증 값이나 직원 데이터는 로그에 노출하지 않는다.
7. MCP로 노출할 때만 `mcp-builder`를 추가 사용한다. MCP가 단순 REST 연동의 필수 조건은 아니다.

## 산출물 템플릿

[템플릿](references/template.md)을 필요한 부분만 사용한다. 요청받은 작업을 실행하고 결과를 검증한다. 이 템플릿 자체는 완성된 제품 문서나 실행 결과가 아니다.
