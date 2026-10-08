# Tobi-Bueck Customer Support Tickets

## 확인 정보

[원본 카드](https://huggingface.co/datasets/Tobi-Bueck/customer-support-tickets). 영어/독일어 합성 지원 티켓, 현재 default/train 뷰어 61,765행, CC-BY-NC-4.0 표기다. subject/body/answer/type/queue/priority/language/version/tag_1~tag_8을 관찰했다. 파일 버전별 규모와 언어가 다를 수 있다.

## 샘플과 용도

[발췌](샘플/08_Tobi_Bueck_발췌.json). 첫 행은 독일어 보안 사고 문의이며 Incident/Technical Support/high 라벨이다. 첫 100행에는 IT Support뿐 아니라 결제·반품 등도 섞여 있다. 이를 IT 업무 전체 정답으로 쓰지 않는다.

## 학습 방법 및 기대 효과

IT 관련 문의를 선별하고 한국어 검수·프로젝트 분류 재라벨링 후 category 및 support_queue 추천을 학습한다. queue는 팀 단위 라우팅 라벨이고 개인 assignee가 아니다. 우리 팀 목록과 배정 정책 없이는 실제 담당자 정답으로 매핑할 수 없다.

긴 문의를 짧은 티켓 초안으로 정리하는 SFT에 활용하려면 별도 정답 요약을 작성한다. answer를 그대로 초안으로 쓰면 상담원의 약속이나 원인 추측이 섞일 수 있다. 실제 대응 절차는 공식 문서로 검증한다.

분류·지원팀 추천의 개선을 기대한다. 사람이 검수한 한국어 holdout에서 class별 성능과 모호한 요청의 보류 행동을 평가한다.

## 제약

비상업 조건과 파생 이용 범위를 확인해야 한다. 우선순위 체계는 프로젝트와 다르며 라벨 품질은 전체 검증하지 않았다. 동일 템플릿·버전 중복을 그룹 분할한다. 첫 100행 관찰을 전체 품질 통계로 일반화하지 않는다.
