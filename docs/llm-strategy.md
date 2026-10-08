# DeskMate LLM 선택과 데이터 전략

## 결론

**목표 구성은 Spring Boot 제품 백엔드 + Python AI Service다. Python 서비스에서 OpenAI Agents SDK와 호스팅 LLM API를 사용하고 PostgreSQL + pgvector로 RAG를 구현한다.** `gpt-4.1-mini`는 첫 API 후보지만 계정·지역별 제공 여부, 가격, 최신 모델을 확인하기 전 미확정이다. Fine-tuning은 기준선과 오류 분석 전에는 하지 않는다.

- IT 해결 정보는 모델 파라미터보다 승인된 최신 가이드에 있어야 한다. 이를 RAG의 출처·인용으로 보여 주는 것이 주제에 더 직접적이다.
- MVP의 주된 AI 가치는 다중 턴 증상 파악, 근거 검색, tool 선택과 승인 경계다. SDK의 tool schema·서버 검증·trace로 시연한다.
- 한 모델만 보면 선택 근거가 약해지므로, API와 인증이 준비되면 더 작은/큰 사용 가능 모델을 같은 평가셋에서 비교한다. 외부 API 접근 전에는 소요 비용이나 성능을 단정하지 않는다.
- 현재 앱은 Python 규칙 기반 단일 서버이며, Spring 백엔드 이관과 Python AI Service 분리, 실제 모델 호출은 미구현이다. 이번 문서는 목표 설계이며 모델을 설치·호출하거나 API key를 설정한 것은 아니다.

## 모델 방식 비교

| 방식 | 예시 | 장점 | 부담·한계 | 권고 |
| --- | --- | --- | --- | --- |
| 호스팅 API | GPT-4.1 mini 후보 | 빠른 통합, 낮은 운영 부담, JSON/tool calling에 적합 | 요청당 비용, 외부 전송·개인정보 검토, 계정/지역별 모델 제공 확인 | MVP 주력 |
| 호스팅 소형/대형 대안 | OpenAI에서 실제 사용 가능한 작은/큰 모델 | 품질·비용 비교 근거 마련 | 같은 고정 평가셋과 schema가 필요 | 기준선 완성 후 비교 |
| 공개 가중치 자체 실행 | Qwen Instruct 8B 계열 후보 | 로컬 추론과 데이터 경계 제어 가능 | GPU/메모리, quantization, serving, 성능·라이선스 검토, 운영 복잡도 | API 사용 불가 또는 로컬 실행이 핵심 rubric일 때 비교 |
| 자체 사전학습 | 처음부터 가중치 학습 | 연구 자체가 핵심일 때 학습 과정을 제시 가능 | 큰 규모의 고품질 데이터, GPU 시간·비용, 평가 인프라 필요 | 이 프로젝트 범위에서 제외 |

공개 가중치 모델 이름·상업 사용 조건은 선택 시점의 공식 model card/license에서 다시 확인한다. “오픈소스”나 공개 다운로드가 곧 제한 없는 상업 사용을 뜻하지 않는다.

## RAG와 튜닝의 역할

- **RAG가 해결:** 최신 절차와 사내 고유 사실 제공, 근거 문서·구절 인용, 문서 변경·삭제 반영, 허용된 사용자 자료 범위 검색.
- **Fine-tuning이 해결할 수 있는 것:** 반복해서 나타나는 응답 형식·분류·질문 순서·도구 선택 패턴을 더 일관되게 만드는 것.
- **Fine-tuning으로 해결하면 안 되는 것:** VPN 암호, 현재 장애 상태 등 변하는 사실을 기억시키기, 출처 없는 사실 보충, 승인 없는 티켓 쓰기를 모델에 위임하기.
- 모델을 튜닝해도 서버 측 schema 검증, 승인 확인, idempotency는 항상 유지한다. RAG 근거는 대화 시점에 검색한다.

## 데이터는 어디서 구할 수 있나

| 데이터 | 구할 수 있는 방법 | 이 프로젝트 적합도 | 사용 전 확인 |
| --- | --- | --- | --- |
| 우리 회사 IT 절차·FAQ | 실제 소유 부서가 공유·사용을 승인한 비기밀 문서 | 답변 RAG에는 가장 적합. 현재는 제공되지 않음 | 소유자 승인, 최신 버전, 부서별 접근 범위, 비밀·개인정보 제거 |
| 공개 기술지원 대화 | Ubuntu Dialogue Corpus 같은 공개 커뮤니티 대화 | 언어·분포가 다르고, 개인 식별자·잡음·라이선스 검토 부담. 직접 fine-tune용으로 바로 쓰기엔 부적합 | 원 출처 이용약관/라이선스, 재배포·학습 허가, 사용자 식별정보와 보안 내용 정리 |
| 공개 의도 분류셋 | PolyAI Banking77 등 | 분류 평가 형식 참고에 유용. 은행 업무 의도는 사내 IT 해결 답변을 학습시키지 않음 | dataset card의 license, 출처와 허용 목적 확인 |
| 합성 IT 가이드·문의 | 승인된 제품 문서를 바탕으로 팀이 시나리오와 정답을 작성 | 데모용으로 가장 현실적인 시작점. 실제 사내 지식이라고 오인되지 않게 synthetic 표시 | 사실·절차를 사람 검토. 공개 배포할 때 원문 문서 저작권 확인 |
| 실제 티켓/상담 로그 | 회사 service desk export | 미래에 확보하면 가장 도메인에 맞을 수 있음. 지금은 접근 불가 | 개인정보, 직원·기기 식별자, credential, 보안 사건, 노사·규제, 내부 사용/학습 법적 근거와 승인 검토 |

공개 데이터는 형식·테스트 사례의 참고 자료이지 내부 대응 절차의 대체물이 아니다. 이 문서 작성 환경의 네트워크 정책으로 공식 model/dataset 페이지 접속을 확인하지 못했다. 따라서 실시간 가격, 현재 API 모델 목록, 데이터셋의 현 라이선스 문구를 검증했다고 주장하지 않는다. 도입 직전 공식 페이지를 확인한다.

참고할 공식 페이지:

- OpenAI models: https://platform.openai.com/docs/models
- OpenAI API pricing: https://openai.com/api/pricing/
- Agents SDK: https://openai.github.io/openai-agents-python/
- Banking77 dataset card: https://huggingface.co/datasets/PolyAI/banking77
- Bitext customer support dataset card: https://huggingface.co/datasets/bitext/Bitext-customer-support-llm-chatbot-training-dataset
- 공개 가중치 후보 예시 Qwen: https://huggingface.co/Qwen

각 dataset/model card의 라이선스와 사용 조건은 다운로드·학습 전에 다시 확인한다. 이 URL을 적었다고 이미 해당 자료를 프로젝트에 복사하거나 사용한 것은 아니다.

## 권장 데이터 생성 계획

### RAG corpus

- 먼저 VPN·계정·메일·프린터에 관해 **12~20개의 짧고 검토된 synthetic 가이드**를 만든다.
- 각 문서에 `source_id`, `title`, `category`, `version`, `owner`, `updated_at`, `allowed_audience`, `source_url` 또는 synthetic 표기를 포함한다.
- 문서를 절차/문제 해결 단위로 나누고 원문 문서 ID·버전을 chunk metadata에 남긴다.
- 인덱싱용 가이드와 평가용 질문·정답을 분리한다. 같은 문장 재사용으로 retrieval 점수를 부풀리지 않는다.

### Fine-tuning을 고려할 때

RAG·prompt·도구 schema·모델 후보를 비교한 뒤에도 반복되는 오류가 남을 때만 작은 supervised fine-tuning 실험을 설계한다. 공개 최소 샘플 수는 품질 기준이 아니며, 아래는 이 프로젝트의 실무 시작 제안이다.

- **Pilot:** 사람 검토한 100~200개의 다중 턴 사례로 유효성·학습 pipeline·format 안정성 확인.
- **비교 실험:** 일관된 오류 패턴을 대표하는 300~1,000개 고품질 사례를 목표로 데이터 수집 가능성 검토. 사례 수만 채우기보다 class/실패 모드를 균형 있게 포함.
- 대화 예시에는 필요한 입력 맥락, 검색된 근거, 기대 추가 질문 또는 구조화 응답을 넣는다. tool-call 학습을 하면 기대 도구명과 schema-valid arguments, 도구 결과 뒤 후속 응답을 함께 만든다.
- 편향, 과잉 이관, 위험한 해결 지침, 근거 밖 주장, 거부 사례를 포함하되 실제 credential·개인정보는 포함하지 않는다.
- DPO/preference 학습은 좋은 답과 더 나쁜 답의 쌍을 전문가가 선택할 수 있고 supervised 기준선이 충분히 안정된 다음 단계다. 처음부터 필요하지 않다.
- 문서 업데이트에 따라 바뀌는 정답은 fine-tuning target이 아니라 RAG 문서에 둔다.

수량은 법칙이나 모델 공급자 최소 요구치가 아니라 실험을 시작하기 위한 제안이며, 실제 학습 API의 최신 요구사항을 확인한다.

## 평가용 데이터 구성

먼저 **60개 synthetic 사례**를 제안한다: prompt·retrieval 개발용 40개, 마지막까지 동결할 holdout 20개. 범위는 정상 문의, 모호함과 추가 질문, 문서 내·외부 질문, 다중 장애, 한국어 표현 변화, 정보 부족, 프롬프트 인젝션, 금지 정보, ticket 승인·거부, idempotent retry, API/tool 오류다. 작은 holdout에서 수치가 불안정하므로 aggregate 점수와 사례별 실패를 모두 공개한다.

각 사례에는 기대 분류·필수 슬롯·gold source/chunk, 허용·금지 tool, 기대 이관, 개인정보·prompt injection 기대 동작을 적는다. 튜닝 데이터와 holdout은 사용자 표현/문서 단위로 분리해 유사한 문장 누출을 줄인다. 실측 전에 성공 기준을 확정하지 않고, 첫 baseline 결과를 보고 목표를 검토한다.

## Fine-tuning 의사결정 기준

다음 조건이 충족될 때 별도 실험으로 진행한다.

1. 고정 holdout에서 현재 API 모델 + RAG + prompt 기준선 결과를 기록했다.
2. 실패 분석 결과가 최신 지식 부재가 아니라 형식·분류·질문·도구 선택 같은 학습 가능한 반복 패턴으로 모인다.
3. 해당 오류를 대표하고 사람이 검토한 예시와, 학습에 사용하지 않을 독립 holdout을 확보했다.
4. 예상 품질 차이가 학습·유지·재검증 비용을 상쇄하는지 작은 pilot으로 비교한다.
5. 학습 데이터 이용 허가, 공급자 보존 정책, 민감 데이터 제거와 rollback 가능한 model version을 확인했다.

조건이 충족되지 않으면 RAG, tool schema, prompt, UI의 승인 흐름을 개선한다. Fine-tuning 전후의 retrieval 근거·tool 정확도·안전성·latency·총비용을 같은 평가셋으로 비교한다.

## 설정과 비밀 정보

`OPENAI_API_KEY`는 로컬 `.env` 또는 안전한 사용자 환경 설정에만 저장한다. `.env`는 Git에서 제외한다. 모델과 embedding model은 환경 변수로 선택 가능하게 하고 로그에는 key, 원문 민감 대화, chain-of-thought를 기록하지 않는다.
