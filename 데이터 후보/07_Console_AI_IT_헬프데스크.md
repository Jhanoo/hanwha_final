# Console-AI IT Helpdesk Synthetic Tickets

## 확인 정보

[원본 카드 및 다운로드](https://huggingface.co/datasets/Console-AI/IT-helpdesk-synthetic-tickets). 2026-10-08 뷰어 기준 영어 합성 IT 문의 500행, MIT 표기, CSV다. subject/description/category/priority/id/createdAt/requesterEmail 필드를 확인했다. 첫 100행을 검사했으며 전체 품질 검수는 아니다.

## 실제 샘플

[발췌](샘플/07_Console_AI_발췌.json). 첫 문의 제목은 “Hey IT! Our network printer keeps disconnecting.”이다. 원본 라벨은 Network/Medium이다. 프린터 문의도 Network로 분류될 수 있어 현재 DeskMate의 장비 분류와 단순 동일시할 수 없다. 답변·담당자·해결 결과는 없다.

## 학습과 효과

subject+description에서 장애 분류와 사실 중심 요약을 생성하도록 SFT하거나 소형 분류기를 학습한다. 먼저 현재 네트워크/계정·권한/업무 도구/장비/기타에 대한 매핑 규칙을 정하고 애매한 사례를 사람이 재라벨링한다. 한국어 번역은 숫자·오류·제품명을 보존한다. 정답 요약은 새로 검수해야 하며 subject를 완벽한 요약으로 가정하지 않는다.

문의 표현 다양성과 분류·요약의 일관성 개선을 기대한다. 무작위 행 분할보다 동일 문의 변형/스레드 단위로 분할하고 macro-F1·요약 사실성을 평가한다.

## 제약

합성 priority를 회사 우선순위 정책으로 복제하지 않는다. requesterEmail 등은 학습 본문에서 제거한다. 원문에 포함된 링크나 담당자 지시는 승인 근거가 아니다. 증상 질문·분류용 1차 후보이며 해결 지식이나 개인 배정 정답은 아니다. 검증된 전체 학습셋은 아직 없다.
