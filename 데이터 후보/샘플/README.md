# 프로젝트 데이터 샘플 안내

2026-10-08 정리. 공개 데이터 발췌와 가상 설계 예시를 구분한다. 발췌는 완전한 학습 레코드가 아니다.

| 파일 | 목적 |
|---|---|
| [Console-AI](07_Console_AI_발췌.json) | IT 문의 제목과 분류 |
| [Tobi-Bueck](08_Tobi_Bueck_발췌.json) | 지원팀 라우팅 및 티켓 분류 |
| [IT_Support_V2](09_IT_Support_V2_발췌.json) | 기술지원 문의와 라벨 |
| [ko-agentic-sft](10_ko_agentic_구조요약.json) | 한국어 호출 억제 행동 |
| [FunctionChat-Bench](05_FunctionChat_발췌.json) | 독립 평가용 정답 호출 |
| [자체 IT 가상 사례](06_IT지원_가상예시.jsonl) | 추가 질문·상태 조회·담당자 할당 설계 예시 6건 |
| [검증 기록](재조사_검증기록.json) | 유지한 4개 공개 후보의 첫 100행 검사와 revision |

FunctionChat는 학습에서 제외한다. 가상 할당 도구는 현재 저장소에 없으며 실제 계약 확정 전 학습 입력으로 사용하지 않는다. 새 HF 샘플의 메타데이터 revision은 기록했지만 뷰어 조회는 revision 고정이 아니므로 학습용 원본 확보 시 고정 revision으로 다시 다운로드해야 한다. 라이선스 및 적용 범위는 각 상위 후보 문서를 따른다.
