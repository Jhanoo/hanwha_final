# ko-agentic-sft 한국어 행동 보조 자료

## 확인 정보

[제작자 카드](https://huggingface.co/datasets/waylake/ko-agentic-sft). 한국어 합성 2,369행, Apache-2.0 표기, messages/kind/has_action 구조다. 카드상 action 1,583건과 no-action 786건이 있으며 검색·연쇄 호출·계산·실패·직접 답변 등을 포함한다.

## 샘플 및 형식

[발췌](샘플/10_ko_agentic_구조요약.json). 첫 행은 문장 다듬기 direct 사례이며 has_action=false다. 처음 100행에서 여러 kind와 호출하지 않는 사례를 확인했다. 전체 행동 품질을 검증한 것은 아니다.

호출은 assistant content의 action/args JSON, 결과는 user 역할의 '[도구 결과]' 접두어 형태다. 외부 사실과 URL은 합성이므로 해결 지식으로 사용하지 않는다.

## 학습 방법과 효과

불필요한 호출 억제, 결과가 없을 때의 대응, 여러 단계 실행 형식 보조로 검토한다. 실제 tool 목록에 맞춰 역할을 변환하고 user로 포장된 결과를 tool result로 구분한다. 대화에 없는 schema를 임의로 덧붙이지 않는다. 현재 프로젝트에서 웹 검색이 구현됐다고 설명하지 않는다.

자체 IT SFT 사례와 소량 섞어 포함/제외 비교를 한다. 호출하지 말아야 할 요청의 과잉 호출률과 결과 밖 주장을 평가한다. generic direct 사례는 기존의 사용자 지원 범위와 맞는지 검수한다.

## 제약

사내 업무 전용이 아니며 teacher의 생성 조건도 확인해야 한다. 티켓 생성 승인·담당자 할당 데이터는 별도 제작한다. 카드의 형식 검증 설명은 우리 변환 결과나 학습 성능의 보장이 아니다.
