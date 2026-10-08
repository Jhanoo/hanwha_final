# DeskMate RAG 자료와 프로젝트 튜닝 데이터 제작 계획

## 기준선 먼저 구축

현재 저장소는 실제 LLM/RAG가 미구현이다. 먼저 현재 코드의 규칙 응답을 보존한 기준선과 모델+prompt+RAG 기준선을 비교한다. 데이터 후보 조사만으로 학습 효과나 모델 성능을 주장하지 않는다. 특정 모델 설치·외부 API 호출·학습은 이번 작업에서 수행하지 않았다.

## RAG로 쓸 공식 자료

| 현재 주제 | 공식 후보 | 적용과 제한 |
|---|---|---|
| VPN | [Windows VPN 연결](https://support.microsoft.com/ko-kr/windows/experience/connectivity-networking/connect-to-a-vpn-in-windows) | Windows 기본 VPN 일반 안내. 실제 회사 서버 주소·클라이언트 정책은 별도 승인 문서 필요 |
| 네트워크 | [Windows 프록시](https://support.microsoft.com/ko-kr/windows/experience/connectivity-networking/use-a-proxy-server-in-windows) | 설정 항목 이해. 회사 프록시 값을 임의로 만들지 않음 |
| 메일 | [Outlook 설정 문제 해결](https://support.microsoft.com/ko-kr/outlook/getstarted/troubleshoot-outlook-email-setup) | 새/클래식 Outlook과 계정 유형을 구분해 근거 선택 |
| 계정·권한 | 승인된 내부 계정 FAQ 및 Microsoft 계정 자료 | 사내 SSO와 개인 Microsoft 계정의 재설정 절차를 혼동하지 않음 |
| 프린터 | 실제 프린터 제조사·모델의 공식 매뉴얼 | 장비가 미정이므로 특정 제조사 문서를 정답으로 채택하지 않음 |

공개 링크 접근 가능성이 학습·재배포 허가를 의미하지 않는다. 원문 전체 복제 대신 허용된 범위와 이용 조건을 확인하고 출처·버전·제품 정보를 관리한다. RAG corpus는 아직 작성·색인하지 않았다.

## 권장 데이터 세트 분리

### A. 분류·티켓 초안

Console-AI에서 현재 4개 주제에 맞는 문의를 우선 선별한다. 부족한 표현은 Tobi의 IT 관련 행과 IT_Support_V2 user 문장에서 보완한다. 원문 답변을 정답으로 복사하지 않고 category, 사실 중심 summary, unknown 슬롯을 검수한다. source priority/queue는 우리 정책 정답으로 바로 사용하지 않는다.

### B. 한국어 상담과 도구 사용

실제 가이드에 근거해 문제 파악 → 추가 질문 → 검색 → 해결 여부 확인 → 초안 → 사용자 확인 → 생성 결과 설명 대화를 작성한다. 불필요한 호출·검색 실패·근거 부족은 ko-agentic-sft의 형식을 참고하되 source의 합성 사실은 가져오지 않는다.

### C. 담당자 할당 확장

사용자 요구는 담당자 할당이지만 현재 API/DB에 담당자 계약이 없다. 먼저 지원팀·담당자 목록, 처리 분야, 권한, 배정 정책과 재배정 흐름을 확정해야 한다. 공개 queue는 팀 라우팅 참고이고 개인 assignee 정답이 아니다. 기존 06번 가상 할당 도구는 설계 예시로 보존하며 현재 런타임 학습 계약에서 제외한다.

### D. 독립 평가

저장소 계획의 60개 synthetic 사례(개발용 40, holdout 20)를 우선 기준으로 삼는다. 기존 문서의 150~200개 평가 제안은 확장 단계다. FunctionChat-Bench는 외부 평가용으로 유지한다. 원본·번역·템플릿 그룹과 문서 질문 변형이 holdout에 누출되지 않도록 한다.

## 학습 형식과 서버 책임

학습 레코드에는 대화, 제공 도구, 검색 근거, 기대 출력과 provenance를 저장한다. ticket_draft.category/summary 등은 목표 annotation이며 현재 POST /api/tickets의 추가 필드가 아니다. 미확인 원인·영향·해결 조치는 null/unknown으로 두고 모델이 추측하지 않도록 한다.

현재 API priority는 보통/높음, DB enum은 normal/high 등으로 다르다. 학습 annotation과 실제 요청 변환을 명시적으로 분리한다. idempotency_key와 승인 증명은 앱/서버가 생성·검증하며 모델이 임의로 꾸미게 하지 않는다.

서버측 승인 경계는 현재 완성되지 않았다. 학습을 통해 구현 결함을 대신 해결할 수 없다. 미래 tool 명세 확정 전에는 create/assign 성공 데이터를 실제 계약으로 학습하지 않는다.

## 실험 단계와 효과

1. 사람이 검수한 100~200개 pilot으로 데이터 형식과 평가를 확인한다.
2. 반복되는 오류가 남으면 300~1,000건 규모로 검토한다. 수량은 제안이다.
3. API 모델 SFT와 공개 가중치 LoRA/QLoRA는 모델·비용·GPU 조건을 보고 선택한다. 현재 저장소의 API 모델 전략을 이번 조사만으로 변경하지 않는다.
4. 동일 문서·tool·평가 입력으로 prompt+RAG와 SFT+RAG를 비교한다.
5. category macro-F1, 슬롯 누락, 요약 환각, 승인 전 호출, 중복 생성, tool 실패 후 허위 성공, 지연을 평가한다.
6. 개선이 확인된 행동만 학습 효과로 보고한다. 담당자 배정 기능은 실제 구현 후 별도 검증한다.

## 샘플 상태

새 후보의 샘플은 공개 행의 일부 필드 발췌와 구조 요약이다. 완전한 원본 학습 레코드나 검수된 학습셋이 아니다. 새로 생성한 annotation 예시는 데모용 제안으로 표시한다. 원본과 변환 출처를 분리하고 변경 사실을 기록한다.
