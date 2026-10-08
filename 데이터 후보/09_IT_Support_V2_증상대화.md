# IT_Support_V2 기술지원 질문 자료

## 확인 정보

[제작자 카드](https://huggingface.co/datasets/benjaminmacklin/IT_Support_V2). 영어 messages 기반 데이터, 현재 뷰어 103,226행, MIT 표기다. 제작자는 IT 지원 모델 Mack를 위해 생성한 자료라고 설명한다. 실제 운영 상담 로그로 확인한 자료는 아니다.

## 직접 확인한 품질 차이

[발췌](샘플/09_IT_Support_V2_발췌.json). 첫 user는 “Outlook cannot read emails from Exchange with large attachments.”이고 assistant는 outlook_issue다. 자연어 답변과 분류 라벨이 혼재한다.

이번 첫 100행 검사에서 모두 2턴이었다. _issue로 끝나는 답변은 9건, assistant에 Mack가 포함된 행은 24건이었다. 브랜드 문자열 포함 수치이며 정확한 자기소개 비율은 아니다. 이 표본을 전체 분포나 정답 품질로 일반화하지 않는다.

## 권장 사용 및 학습

전체 assistant 답변을 바로 SFT하지 않는다. VPN·계정·Outlook·프린터 관련 user 증상을 선별하고 실제 공식 문서 기반 추가 질문·답변으로 재작성한다. 분류 라벨 사례와 상담 사례를 분리하고 프로젝트 category를 검수한다. 다른 챗봇 자기소개와 관리자 전용·환경 미상 해결책은 제외한다.

문제 표현·오류 코드 다양성을 확보하는 보조 자료로 기대한다. 한국어 재작성과 학습에 드는 비용을 감안해 Console-AI 및 자체 대화 다음에 검토한다.

## 한계

다중 턴 증상 수집, 검색 근거, 사용자 승인, 실제 도구 호출, 담당자 배정 정답을 제공한다고 가정할 수 없다. 전체 답변의 기술적 정확성은 미검증이다. 공식 절차의 대체 자료로 쓰지 않는다.
