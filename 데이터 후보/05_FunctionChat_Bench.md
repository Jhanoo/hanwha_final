# Kakao FunctionChat-Bench

## 성격과 확보 위치

한국어 대화에서 tool use/function calling을 평가하는 공개 벤치마크다. 학습 후보들과 함께 관리하지만 기본 용도는 평가다.

- [공식 저장소·데이터·평가 코드](https://github.com/kakao/functionchat-bench)
- [논문](https://arxiv.org/abs/2411.14054)
- [카카오 공개 안내](https://www.kakaocorp.com/page/detail/11415?lang=ENG)
- 이용 조건: 저장소의 `LICENSE`와 `NOTICE.md`를 함께 확인한다. 이번 조사에서는 라이선스 전문과 모든 하위 파일 조건을 확인하지 않아 특정 라이선스로 확정하지 않는다.

## 어떤 내용을 평가하는가

단일 호출과 여러 턴의 대화에서 함수 및 인자 선택, 함수 결과 전달, 정보 부족 시 추가 질문, 요청과 호출 가능한 기능의 관련성을 평가한다. SingleCall에는 25개 함수별 단일 턴 프롬프트가 포함된다. 상세 평가 건수는 사용할 revision에서 기록한다. 도구 목록 조건별 평가 수와 고유 대화 수를 혼동하지 않는다.

## 사용 방법

1. 저장소 revision과 데이터/평가 코드를 고정한다.
2. README가 요구하는 실행 환경과 모델 연결 방법을 확인한다.
3. 모델별 입력 및 출력 어댑터를 연결하고 작은 샘플로 파싱을 검사한다.
4. 모델마다 동일한 도구 목록, 질문, decoding 조건으로 평가한다.
5. 원본 평가 기준을 유지하고 출력 파싱 실패도 기록한다.
6. 학습 전후 결과와 자체 IT 시나리오 결과를 별도로 보고한다.

실행 명령은 사용할 revision의 README에 맞춘다. 이번에 저장소 다운로드나 평가 실행을 수행하지 않았으므로 실행 성공을 보장하는 명령을 제시하지 않는다.

## 학습시키지 않는 이유

원본 문항이나 번역·패러프레이즈를 학습에 넣으면 평가 누출이 발생한다. 독립 평가용으로 보존하고, 점수를 발표할 때 해당 자료로 학습/튜닝했는지 명시한다. 오류 유형을 자체 시나리오 설계에 참고하되 평가 문항 자체를 복제하지 않는다.

## 기대 효과

자료를 평가에 사용한다고 모델이 직접 개선되지는 않는다. 한국어 도구 사용의 전후 변화를 비교하고 실패 유형을 찾는 근거를 제공한다.

## 프로젝트 평가와의 차이

벤치마크 점수와 별도로 사내 IT 시나리오 완료율, 근거 충실성, 권한 거부 처리, 티켓 중복 처리 결과 설명, API 실패 대응을 평가한다. 벤치마크 고득점이 실제 서비스의 정확성과 안전성을 보장하지 않는다.

[공통 계획](README.md)을 따른다.

## 실제 평가 레코드 발췌

확인일: 2026-10-08. 공식 저장소의 다음 세 파일에서 첫 레코드의 필드와 구조를 조회했다. 전체 저장소를 복제하거나 평가를 실행하지 않았다.

- [Singlecall 원본](https://github.com/kakao/functionchat-bench/blob/main/data/FunctionChat-Singlecall.jsonl)
- [CallDecision 원본](https://github.com/kakao/functionchat-bench/blob/main/data/FunctionChat-CallDecision.jsonl)
- [Dialog 원본](https://github.com/kakao/functionchat-bench/blob/main/data/FunctionChat-Dialog.jsonl)

[Singlecall 발췌 JSON](샘플/05_FunctionChat_발췌.json)

```json
{
  "function_name": "getTodayBoxOfficeRanking",
  "query": {"serial_num":1,"content":"현재 박스오피스 순위가 궁금해요"},
  "ground_truth": {"name":"getTodayBoxOfficeRanking","arguments":"{}"}
}
```

원본 query/ground_truth는 목록이고 정답 content는 호출을 담은 문자열이다. 위 예시는 해당 항목만 꺼내 정답 content를 파싱한 발췌로 전체 원본 구조와 구분한다. 원본 tools에는 exact, 4_random, 4_close, 8_random, 8_close 조건이 있다.

CallDecision은 `input_messages`, `input_tools`, `type_of_output`, `ground_truth`, `acceptable_arguments`를 갖는다. Dialog는 `turns`별 질문 문맥과 정답을 보존하며 첫 레코드에서 slot/call/completion을 확인했다. Dialog의 계정 생성 예시에 비밀번호를 대화로 받는 흐름이 있어 우리 서비스 정책으로 복제하지 않는다.

학습용으로 가져오지 않는다. 정답 인자 값과 허용 대체 값, 도구 목록 조건을 평가 실행 시 보존한다.
