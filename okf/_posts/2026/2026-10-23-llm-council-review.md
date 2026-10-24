---
type: "Repo Review"
title: "[Repo Review] LLM Council — 여러 모델의 답변과 상호 평가를 함께 읽는 방법"
description: "여러 LLM의 병렬 답변·익명 평가·의장 종합이 React 화면과 단계별 SSE, JSON 저장으로 이어지는 과정을 추적하고 순위와 대화 상태의 한계를 분석합니다."
date: "2026-10-23"
tags:
  - "Repo Review"
  - "AI Agent"
  - "Prompt Engineering"
  - "Python"
  - "Tools"
resource: "https://github.com/karpathy/llm-council/tree/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131"
generated:
  by: "process:blog-review"
  at: "2026-10-23T17:20:24+09:00"
sources:
  - id: "github:karpathy/llm-council"
    resource: "https://github.com/karpathy/llm-council/tree/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131"
    title: "LLM Council"
    author: "karpathy"
    last_modified: "2025-11-22T15:35:19-08:00"
status: "stable"
year: "2026"
analyzed_at: "2026-10-23T17:20:24+09:00"
source_id: "karpathy/llm-council"
source_revision: "92e1fccb1bdcf1bab7221aa9ed90f9dc72529131"
source_type: "repo"
source_url: "https://github.com/karpathy/llm-council/tree/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131"
visual_sources:
  - path: "/img/reviews/2026/llm-council-review/architecture.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/main.py#L126-L199"
    caption: "리뷰어 작성, 분석 커밋 기준. 로컬 UI·서버·저장소와 원격 OpenRouter의 경계."
    code_sources:
      - "https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/frontend/src/api.js#L5-L85"
      - "https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/main.py#L126-L199"
      - "https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/openrouter.py#L24-L49"
      - "https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/storage.py#L130-L156"
  - path: "/img/reviews/2026/llm-council-review/council-stages.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/council.py#L8-L174"
    caption: "리뷰어 작성, 분석 커밋 기준. 세 단계의 입력·출력과 집계 순위의 사용 범위."
    code_sources:
      - "https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/council.py#L8-L174"
      - "https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/council.py#L211-L255"
      - "https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/main.py#L150-L164"
---

## 한 모델의 답변보다, 답변들이 갈리는 지점을 읽는 도구입니다

같은 질문을 여러 LLM에 입력하면 서로 다른 설명과 근거를 얻을 수 있습니다. 그러나 답변을 탭마다 복사하고, 어느 부분이 겹치고 충돌하는지 비교하는 일은 사용자의 몫으로 남습니다. **LLM Council은 질문의 병렬 응답 수집 → 응답에 대한 상호 평가 → 의장 모델의 종합을 하나의 화면에 묶은 로컬 웹 앱**입니다. 저자 Karpathy는 여러 모델과 함께 책을 읽으며 답변을 나란히 살펴보기 위한 주말 실험으로 만들었다고 설명합니다. [README](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/README.md#L5-L15)

이 레포에서 흥미로운 부분은 최종 답변만 제공하지 않는다는 점입니다. 사용자는 각 모델의 첫 답변과 다른 응답에 대한 평가 원문, 파싱된 순위까지 볼 수 있습니다. 따라서 공부할 때에는 최종 결론뿐 아니라 **어떤 설명을 좋은 설명으로 평가했는지**를 함께 읽을 수 있습니다. 다만 모델 간 합의가 정확성을 보증하거나, 응답 수가 늘면 성능이 향상된다고 입증한 프로젝트는 아닙니다. 분석 커밋의 README와 코드에는 이를 검증하는 벤치마크가 없습니다.

이 글은 커밋 [`92e1fccb1bdcf1bab7221aa9ed90f9dc72529131`](https://github.com/karpathy/llm-council/tree/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131)을 고정해 정적으로 읽었습니다. 대상 앱의 의존성 설치, 실행, 모델 호출과 성능 측정은 하지 않았습니다. 아래 설치 명령은 같은 커밋의 문서를 소개한 것이며 실행 성공을 확인한 기록이 아닙니다.

## 무엇을 로컬에서 실행하고, 무엇을 API로 호출하나요?

화면과 Python 서버, 대화 JSON 파일은 사용자의 컴퓨터에 있습니다. 실제 LLM 추론은 서버가 **OpenRouter의 원격 API**로 요청합니다. 모델 가중치를 내려받아 로컬에서 추론하는 구조는 아닙니다. API 키는 Python 서버의 `.env`에서 읽고, OpenRouter 요청의 Bearer 인증 헤더에 넣습니다. 브라우저는 서버에 질문을 전달합니다. [설정](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/config.py#L3-L26), [API 요청 구성](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/openrouter.py#L24-L49)

분석 커밋의 기본 구성은 다음과 같습니다. 모델 이름은 **그 커밋에 기록된 설정값**이며, 현재 제공 여부나 가격을 확인한 목록은 아닙니다.

| 역할 | 설정값 |
|---|---|
| 초기 답변·상호 평가를 수행하는 네 모델 | `openai/gpt-5.1`, `google/gemini-3-pro-preview`, `anthropic/claude-sonnet-4.5`, `x-ai/grok-4` |
| 최종 답변을 작성하는 의장 | `google/gemini-3-pro-preview` |
| 새 대화 제목 생성 | `google/gemini-2.5-flash` |

출처: [기본 모델 설정](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/config.py#L11-L23), [제목 생성](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/council.py#L258-L293).

의장은 위원 중 한 모델과 같아도 되며 별도 모델로 바꿀 수도 있습니다. 다만 위원·의장 모델은 `config.py`, 제목 모델은 `council.py`에 각각 고정되어 있습니다. 설정 화면에서 모델을 선택하는 기능은 없습니다. ChatGPT나 Claude의 구독 로그인으로 API 키를 대신하는 경로도 이 코드에는 없습니다. API 과금·사용 가능 모델은 실제 실행 시 OpenRouter 계정과 제공 조건을 별도로 확인해야 합니다. 이 레포의 README가 API 크레딧 준비를 요구한다는 점까지 확인됩니다. [README 설정](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/README.md#L35-L58)

이름과 역할을 부여한 여러 모델이 협업하지만, 각 모델이 도구를 실행하거나 스스로 다음 일을 결정하는 자율 에이전트 구조는 아닙니다. 서버가 정해진 세 단계를 순서대로 실행하는 **다중 모델 워크플로**로 이해하면 구현과 잘 맞습니다.

## 아키텍처: 작은 오케스트레이터와 단계별 화면

![React 브라우저와 FastAPI 서버, 원격 OpenRouter 및 로컬 JSON 저장소의 연결]({{ '/img/reviews/2026/llm-council-review/architecture.svg' | relative_url }})

*리뷰어 작성, 분석 커밋 기준입니다. 로컬에서 실행되는 앱과 외부 추론 API를 구분했습니다. [브라우저 요청](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/frontend/src/api.js#L5-L85), [스트리밍 엔드포인트](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/main.py#L126-L194), [외부 API 호출](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/openrouter.py#L24-L49), [저장](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/storage.py#L130-L156)을 근거로 작성했습니다.*

| 모듈 | 책임 |
|---|---|
| `frontend/src/App.jsx` | 대화 선택·생성, 사용자 입력과 부분 응답 상태, SSE 이벤트 처리 |
| `frontend/src/api.js` | 로컬 서버에 HTTP 요청, 스트림의 `data:` 줄 파싱 |
| `components/Stage1.jsx`, `Stage2.jsx`, `Stage3.jsx` | 개별 응답 탭, 평가·평균 순위, 의장 답변 표시 |
| `backend/main.py` | HTTP 라우트, 단계별 SSE 이벤트, 저장 순서 제어 |
| `backend/council.py` | 세 단계 프롬프트, 순위 파싱·집계, 대화 제목 생성 |
| `backend/openrouter.py` | 단일 모델 HTTP 요청과 여러 모델의 병렬 호출 |
| `backend/storage.py` | 대화별 JSON 생성·조회·덮어쓰기 |

Python 매니페스트는 Python 3.10 이상과 FastAPI·Uvicorn·httpx·Pydantic·python-dotenv를 요구합니다. 프런트엔드는 React 19.2 계열, Vite 7.2 계열, `react-markdown`을 선언합니다. 웹 앱의 실제 서버 진입점은 `python -m backend.main`입니다. 루트의 `main.py`는 인사 문자열만 출력하는 파일이므로 앱 실행 진입점과 구분해야 합니다. [Python 매니페스트](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/pyproject.toml#L1-L13), [프런트엔드 매니페스트](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/frontend/package.json#L1-L28), [서버 진입점](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/main.py#L197-L199), [루트 main](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/main.py#L1-L6)

## 작동 원리: 질문이 최종 답변이 되기까지

### 1. 대화를 만든 뒤 질문과 빈 응답을 먼저 화면에 올립니다

사용자가 `New Conversation`을 누르면 브라우저가 `POST /api/conversations`를 호출합니다. 서버는 UUID를 만들고 빈 `messages` 배열을 가진 JSON 파일을 저장합니다. 브라우저는 새 ID의 대화를 조회한 뒤 입력 화면을 표시합니다. [대화 생성](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/main.py#L65-L79), [초기 JSON](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/storage.py#L21-L45), [선택·조회](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/frontend/src/App.jsx#L18-L53)

질문을 보내면 `App.jsx`가 사용자 메시지와 `stage1`, `stage2`, `stage3`가 비어 있는 assistant 메시지를 React 상태에 먼저 추가합니다. 이후 `POST /api/conversations/{id}/message/stream`으로 `{ content }`를 보냅니다. 서버의 스트림 생성기는 사용자 질문을 저장한 뒤, 첫 질문이면 제목 생성 작업도 별도로 시작합니다. 제목 생성은 본문 처리와 병렬로 시작하지만 최종 완료 이벤트 전에는 그 결과를 기다립니다. [화면의 낙관적 갱신](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/frontend/src/App.jsx#L60-L93), [요청](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/frontend/src/api.js#L76-L85), [서버 시작부](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/main.py#L126-L153)

여기서 중요한 경계가 있습니다. 서버는 대화 JSON을 조회하지만 세 단계 함수에는 **현재 `request.content`만** 넘깁니다. 이전 사용자 질문이나 이전 의장 답변을 합쳐 모델에 보내지 않습니다. 더구나 UI 입력 폼은 `conversation.messages.length === 0`일 때만 표시됩니다. 따라서 분석 커밋의 기본 화면은 새 대화당 한 질문을 처리하는 형태입니다. API로 같은 대화에 다시 전송해 기록을 늘리더라도 이전 문맥이 모델 입력에 자동으로 들어가지는 않습니다. [입력 폼 조건](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/frontend/src/components/ChatInterface.jsx#L123-L142), [실제 단계 호출](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/main.py#L150-L164)

### 2. Stage 1: 동일한 질문을 네 모델에 병렬로 보냅니다

`stage1_collect_responses()`는 현재 질문 하나를 `user` 메시지로 만들고 위원 모델 목록에 보냅니다. 실제 병렬 처리는 다음 두 줄에 드러납니다.

```python
tasks = [query_model(model, messages) for model in models]
responses = await asyncio.gather(*tasks)
```

출처: [`query_models_parallel()`](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/openrouter.py#L56-L79)의 일부이며 중간 설명 주석을 생략했습니다.

`asyncio.gather()`는 응답이 빠른 모델부터 다음 단계로 넘기는 경주가 아닙니다. 이 단계의 모든 요청이 반환될 때까지 기다린 뒤 결과를 한 번에 돌려줍니다. 결과 매핑도 완료 순서가 아니라 입력 모델 목록의 순서를 따릅니다. 단일 요청의 기본 timeout 인자는 120초입니다. 다만 이를 전체 질문 처리 시간의 엄격한 상한으로 해석해서는 안 됩니다. 세 단계와 제목 생성, 네트워크 상황은 별도입니다. [요청 함수](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/openrouter.py#L8-L12)

각 요청은 OpenRouter 응답의 첫 `choices`에서 `message.content`와 선택적 `reasoning_details`를 추출합니다. 하지만 council 단계가 저장하는 개별 응답은 모델명과 `content`뿐이므로, 별도 reasoning 데이터는 후속 분석·UI에 연결되지 않습니다. HTTP 또는 응답 처리 중 예외가 나면 `query_model()`은 콘솔에 기록하고 `None`을 반환하며, Stage 1은 그 모델을 응답 목록에서 제외합니다. [응답 추출·오류 처리](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/openrouter.py#L34-L53), [성공 응답 선별](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/council.py#L18-L32)

화면은 성공한 모델마다 탭을 만들고 `react-markdown`으로 답변을 렌더링합니다. 초기 답변끼리는 같은 질문에서 출발하며, 이 시점에는 다른 위원의 답변을 보지 않습니다. [Stage 1 화면](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/frontend/src/components/Stage1.jsx#L5-L35)

### 3. Stage 2: 이름을 가린 모든 답변을 같은 위원들이 평가합니다

서버는 성공한 응답에 `Response A`, `Response B`처럼 문자를 붙입니다. `label_to_model`은 이 문자를 실제 모델명에 연결하는 사전입니다. 모든 성공 응답을 이어 붙여 평가 프롬프트를 만들고, **원래의 전체 위원 모델 목록**에 다시 병렬 요청합니다. 따라서 Stage 1에서 실패한 모델도 Stage 2 평가 요청의 대상에는 포함됩니다. [익명화와 평가 요청](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/council.py#L49-L98)

README는 다른 모델의 답변을 평가한다고 설명하지만, 실제 구현에는 평가자 자신의 답변을 빼는 필터가 없습니다. 첫 단계에 성공한 위원은 **자기 답변을 포함한 전체 성공 응답**을 평가합니다. 각 평가자가 받는 A/B 순서도 같으며 무작위 재배열은 하지 않습니다. 모델명 레이블을 가리는 장치는 있지만, 이를 자기 답변 인지나 순서 편향까지 제거하는 실험 설계로 볼 수는 없습니다. 답변 본문 자체를 익명화·정제하는 코드도 없습니다. [README의 설명](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/README.md#L9-L11), [실제 응답 목록 구성](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/council.py#L49-L62)

프롬프트는 각 응답의 장단점을 먼저 설명한 뒤, 마지막에 `FINAL RANKING:`과 번호 목록을 쓰도록 요구합니다. 그 결과는 평가 원문과 파싱된 레이블 배열로 남습니다. 핵심은 좋은 평가를 생성하는 프롬프트와 기계가 읽을 수 있는 형식을 동시에 요구한다는 점입니다. 다만 출력 형식을 요구하는 것과 올바른 순위가 보장되는 것은 다릅니다.

`parse_ranking_from_text()`는 해당 헤더 뒤의 번호 목록을 정규식으로 찾습니다. 실패하면 헤더 뒤의 `Response X` 출현 순서, 헤더도 없으면 전체 텍스트의 출현 순서로 대체합니다. 중복 레이블 제거, 모든 후보가 정확히 한 번 등장하는지 검사, 번호와 배열 위치의 일치 검사는 없습니다. 따라서 설명 문장 속 레이블이 대체 파싱에 섞이면 그것이 순위처럼 처리될 수 있습니다. UI가 평가 원문과 `Extracted Ranking`을 함께 보여주는 이유를 이해할 수 있는 지점입니다. [프롬프트](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/council.py#L64-L112), [파서](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/council.py#L177-L208), [Stage 2 화면](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/frontend/src/components/Stage2.jsx#L28-L69)

### 4. 평균 순위는 화면의 비교 자료이며, 승자 선출 규칙은 아닙니다

집계 함수는 각 평가에서 파싱된 레이블의 **배열 위치를 1위부터** 기록합니다. 해당 모델이 등장한 위치들의 평균을 구해 소수점 두 자리로 반올림하고 작은 값부터 정렬합니다. `rankings_count`는 그 모델에 대해 수집한 위치 값의 개수입니다. 레이블 중복을 검사하지 않으므로 무조건 서로 다른 평가자 수라고 해석할 수 없고, 어떤 모델이 누락되면 그 모델의 평균은 더 적은 평가에 기반할 수 있습니다. [집계 함수](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/council.py#L211-L255)

결과는 UI에서 `Aggregate Rankings (Street Cred)`로 표시됩니다. **평균 1위 답변을 그대로 최종 답변으로 선택하거나, 평균 순위를 수치 가중치로 사용해 합치는 코드는 없습니다.** 의장 함수가 받는 인자는 질문, Stage 1 결과, Stage 2 결과이며 별도 `aggregate_rankings`를 받지 않습니다. [평균 순위 화면](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/frontend/src/components/Stage2.jsx#L73-L95), [의장 함수 시그니처와 입력 구성](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/council.py#L115-L159)

![개별 응답 수집, 익명 평가와 UI용 순위 집계, 원 응답 및 평가 원문을 읽는 의장 종합의 세 단계]({{ '/img/reviews/2026/llm-council-review/council-stages.svg' | relative_url }})

*리뷰어 작성, 분석 커밋 기준입니다. Stage 2의 집계 점수와 의장에게 전달되는 평가 원문을 구분했습니다. [세 단계 구현](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/council.py#L8-L174), [집계](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/council.py#L211-L255), [호출부](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/main.py#L150-L164)를 근거로 작성했습니다.*

### 5. Stage 3: 의장이 답변과 평가 원문을 읽고 새 답변을 만듭니다

의장 프롬프트는 원래 질문에 더해, 실제 모델명과 함께 Stage 1 답변들을 나열하고 평가자 모델명과 함께 Stage 2의 평가 원문들을 나열합니다. 의장은 개별 통찰, 상호 평가, 동의·불일치를 고려해 하나의 답변을 작성하라는 지시를 받습니다. 이 단계는 다수결 집계가 아니라 **또 한 번의 LLM 생성**입니다. [의장 프롬프트](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/council.py#L131-L162)

익명화의 범위도 Stage 2 평가 입력에 한정됩니다. 의장에게는 모델명이 보이고, 평가 원문의 A/B 레이블을 풀어 주는 `label_to_model` 사전은 의장 프롬프트에 별도로 삽입되지 않습니다. 프런트엔드는 사용자가 읽기 쉽도록 그 사전으로 평가 레이블을 모델명으로 바꾸지만, 이 화면 처리와 의장의 입력을 혼동해서는 안 됩니다. [의장 입력](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/council.py#L131-L159), [클라이언트의 이름 복원](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/frontend/src/components/Stage2.jsx#L5-L14)

의장 요청이 실패해 `None`을 반환하면 서버는 `Error: Unable to generate final synthesis.`라는 문자열을 `response`에 넣습니다. 다른 위원의 답변을 대체 최종 답변으로 선택하는 방식은 아닙니다. UI는 이 결과도 일반 Stage 3 응답으로 렌더링할 수 있습니다. [의장 실패 처리](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/council.py#L164-L174), [Stage 3 표시](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/frontend/src/components/Stage3.jsx#L4-L20)

### 6. SSE는 토큰 단위가 아니라 단계 단위로 진행 상황을 보여줍니다

서버는 각 단계의 `*_start`, `*_complete` 이벤트를 전송합니다. 프런트엔드는 마지막 assistant 메시지의 해당 필드와 로딩 표시를 갱신합니다. Stage 1·2의 각 모델 응답은 병렬 묶음 전체가 끝난 후 표시되고, Stage 3도 의장 응답이 완성된 뒤 표시됩니다. OpenRouter 요청 payload에는 `stream: true`가 없습니다. 따라서 이 레포의 스트리밍은 **생성 중인 단어·토큰을 보여주는 스트리밍이 아니라 단계 결과를 순차 공개하는 SSE**입니다. [서버 이벤트](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/main.py#L150-L181), [UI 갱신](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/frontend/src/App.jsx#L93-L172), [OpenRouter payload](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/openrouter.py#L29-L32)

또한 프런트엔드의 파서는 매번 받은 네트워크 chunk를 즉시 줄로 나누어 JSON을 파싱합니다. 다음 chunk까지 불완전한 줄을 보관하는 버퍼나 `TextDecoder`의 스트리밍 옵션은 없습니다. 네트워크가 JSON 중간이나 UTF-8 문자 중간에서 끊어 전달하면 이벤트 파싱이 실패하거나 문자가 손상될 여지가 있습니다. 이는 코드에서 확인한 경계 처리의 제약이며, 실제 통신에서 재현한 결과는 아닙니다. [SSE 읽기 루프](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/frontend/src/api.js#L92-L113)

### 7. 완성된 세 단계는 JSON에 남지만, 순위 메타데이터는 남지 않습니다

최종 응답 이후 서버는 제목 생성을 마무리하고, assistant 메시지에 `stage1`, `stage2`, `stage3`를 저장한 뒤 `complete` 이벤트를 보냅니다. Stage 3가 화면에 나타난 순간과 전체 저장 완료 시점은 다릅니다. [완료 순서](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/main.py#L161-L181)

저장되는 assistant 객체에는 `metadata`가 없습니다. Stage 2의 평가 원문과 `parsed_ranking`은 보존되지만, `label_to_model`과 `aggregate_rankings`는 실시간 API 이벤트와 React 메모리에만 있습니다. 대화를 다시 열면 이 메타데이터를 재계산하는 코드도 없으므로 **평가의 모델명 복원과 평균 순위 표시는 유지되지 않습니다.** 데이터가 저장된다는 설명을 화면 상태 전체의 영속성으로 받아들이면 안 됩니다. [저장 스키마](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/storage.py#L130-L156), [재조회](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/frontend/src/App.jsx#L34-L41), [표시 조건](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/frontend/src/components/ChatInterface.jsx#L91-L96), [기술 문서의 명시](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/CLAUDE.md#L37-L41)

## 어떤 공부와 비교에 활용할 수 있을까요?

다음은 구현에서 확인한 기능에 대한 리뷰어의 활용 해석입니다. 실제 품질 개선을 측정한 사례는 아닙니다.

- **개념 설명의 차이 읽기:** 같은 질문에 대한 네 답변을 보고, 어떤 모델은 직관을 먼저 설명하고 다른 모델은 전제와 예외를 강조하는지 비교할 수 있습니다. 이어 평가 원문이 어떤 설명을 높게 평가했는지 확인할 수 있습니다.
- **설계 선택의 쟁점 정리:** 하나의 기술적 선택을 질문하고 답변 간 합의와 불일치를 살필 수 있습니다. 의장 답변에서 사라진 소수 의견이 있는지 원 응답 탭으로 돌아가 확인하는 방식이 이 UI에 적합합니다.
- **LLM 평가 파이프라인 공부:** 평가 프롬프트, 자유 형식 출력의 파싱, 평균 순위 집계가 각각 다른 책임이라는 점을 짧은 코드에서 추적할 수 있습니다. 특히 좋은 설명을 생성하는 기능과 안정적으로 점수를 해석하는 기능을 분리해서 볼 수 있습니다.

반대로 이 앱에는 검색·문서 업로드·인용 검증·도구 실행 모듈이 없습니다. 책이나 사내 문서를 자동으로 수집해 읽어 주는 시스템으로 확장되어 있다고 해석해서는 안 됩니다. 이 커밋의 구현은 사용자가 보낸 문자열과 다른 모델의 출력에 기반합니다. [질문 및 평가 입력](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/council.py#L18-L21), [의장 입력](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/council.py#L131-L159)

## 설치와 사용: README가 안내하는 최소 흐름

아래 명령은 모두 분석 커밋의 README에서 가져왔습니다. Python 실행 환경과 Node/npm 환경을 준비한 후 레포 루트에서 진행하는 문서상의 절차입니다.

```bash
uv sync
cd frontend
npm install
cd ..
```

출처: [README 의존성 설치](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/README.md#L19-L33).

루트 `.env`에는 다음 키를 설정합니다. 이 문자열은 README의 자리표시자이며 실제 키가 아닙니다.

```bash
OPENROUTER_API_KEY=sk-or-v1-...
```

출처: [README API 설정](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/README.md#L35-L43). 모델 구성은 `backend/config.py`의 위원 목록과 의장 모델을 수정하도록 안내합니다.

문서는 `./start.sh`로 두 서버를 시작하거나, 다음과 같이 터미널을 나누어 실행하도록 설명합니다.

```bash
uv run python -m backend.main
```

다른 터미널에서는 다음 명령을 사용합니다.

```bash
cd frontend
npm run dev
```

출처: [README 실행](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/README.md#L60-L80). 브라우저 주소는 `http://localhost:5173`이며 프런트엔드가 연결하는 API 주소는 `http://localhost:8001`로 고정되어 있습니다. 화면에서 새 대화를 만들고 한 질문을 입력한 뒤 각 단계의 탭을 확인하는 흐름입니다.

이 문서는 로컬 개발 실행을 안내하며 운영 서비스 배포 절차를 제공하지 않습니다. 원격 서버에 올린다고 해서 브라우저의 `localhost:8001`이 그 서버를 가리키지는 않습니다. 원격 공개 서비스로 바꾸려면 주소·접근 제어·저장 구조 등을 별도로 설계해야 합니다. `start.sh`는 백엔드 실행 후 2초 기다리고 프런트엔드를 시작하며, 실제 서버 준비 상태를 확인하는 health check를 수행하지 않습니다. [고정 API 주소](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/frontend/src/api.js#L5-L16), [시작 스크립트](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/start.sh#L8-L31)

## 한계와 주의점: 코드가 보장하는 범위를 구분합니다

### 익명 상호 평가는 정확도 검증이나 공정한 투표 실험이 아닙니다

자기 응답을 포함하고 모든 평가자가 같은 순서를 보며, 출력 파서도 느슨합니다. 의장 단계에서는 모델명이 다시 보입니다. 이 구조로 상호 평가 과정을 관찰할 수는 있지만, 편향을 제거했다거나 정답률이 개선되었다고 단정할 근거는 없습니다. 결과 품질에 관한 저자의 정량 평가·통계적 검정은 이 커밋에서 확인되지 않았습니다. 가장 확실하게 제공되는 것은 원 응답과 평가 원문을 독자가 비교할 수 있는 인터페이스입니다.

### 요청 수와 프롬프트 길이가 함께 늘어납니다

기본 네 위원 모두를 대상으로 정상 경로를 진행하면 초기 답변 4회, 평가 4회, 의장 1회로 **본 처리에 9회의 모델 요청**을 시도합니다. 첫 질문은 제목 생성 1회가 추가됩니다. 실제 성공 횟수와 비용은 다를 수 있습니다. 특히 각 평가 요청은 모든 성공 답변을 포함하므로 위원 수와 답변 길이가 늘면 평가 입력도 반복해서 커집니다. 단계 내부는 병렬이지만 Stage 1 → 2 → 3의 의존 관계는 순차입니다. 코드에는 토큰 사용량·금액 집계나 별도 비용 상한, 재시도·백오프가 구현되어 있지 않습니다. [호출 구성](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/council.py#L18-L21), [평가 입력](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/council.py#L58-L98), [의장 호출](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/council.py#L159-L162), [HTTP 처리](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/openrouter.py#L24-L53)

### 정상 응답의 일부 실패와 전체 실패가 동일하게 처리되지 않습니다

일부 모델의 요청 실패를 `None`으로 받아 성공 응답만 쓰는 경로는 있습니다. 그러나 비스트리밍 `run_full_council()`에는 Stage 1 전체 실패 시 조기 반환이 있는 반면, UI가 사용하는 스트리밍 엔드포인트에는 그 분기가 없습니다. 스트리밍에서는 응답 목록이 비어도 다음 평가·의장 단계로 진행합니다. 두 경로를 동일한 오류 처리로 설명하면 실제 동작을 놓칩니다. [전체 실패 분기](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/council.py#L306-L317), [스트리밍 경로](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/main.py#L150-L164)

또한 서버의 `error` SSE 이벤트를 받은 UI는 오류를 콘솔에 기록하고 전체 로딩을 끄지만, 사용자에게 별도 오류 메시지를 표시하거나 단계별 로딩 상태를 모두 정리하는 처리는 없습니다. 이벤트가 누락된 채 연결만 끝나는 경우에도 스트림 reader의 종료를 별도 완료 상태로 바꾸는 보장은 없습니다. 따라서 단계 결과가 일부 표시되었다는 사실과 요청이 정상 완료·저장되었다는 사실을 구분해야 합니다. [오류 이벤트 처리](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/frontend/src/App.jsx#L158-L181), [reader 종료 처리](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/frontend/src/api.js#L95-L113)

### 로컬 실험용 저장과 공개 서비스용 저장은 요구가 다릅니다

저장소는 대화 JSON 전체를 읽고 수정한 뒤 같은 파일을 직접 덮어씁니다. 파일 잠금, 임시 파일 후 원자적 교체, 트랜잭션 처리는 없습니다. 동시 요청이나 쓰기 중단 시 갱신 손실·불완전 저장의 여지가 있다는 것이 정적 분석상의 판단이며, 이를 재현해 측정하지는 않았습니다. 개별 JSON이 손상되었을 때 목록 조회에서 그 파일만 건너뛰는 예외 처리도 없습니다. [읽기·쓰기](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/storage.py#L48-L78), [목록 조회](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/storage.py#L81-L107)

백엔드의 대화 API에는 사용자 인증과 소유자 분리가 없고 서버는 `0.0.0.0:8001`에 바인딩됩니다. localhost 두 주소를 허용하는 CORS 설정은 브라우저의 교차 출처 요청 정책이지, API 인증 장치가 아닙니다. 따라서 코드 그대로 외부에 공개하면 누가 요청을 만들고 대화를 조회할 수 있는지 통제하는 서비스 계층이 부족합니다. 질문은 원격 모델로 보내고 응답은 로컬 파일에 남는다는 데이터 경계도 함께 이해해야 합니다. [CORS](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/main.py#L17-L24), [대화 API](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/main.py#L59-L79), [서버 바인딩](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/main.py#L197-L199)

### 유지보수 의사와 라이선스도 확인해야 합니다

저자는 README에서 주말 실험이며 지원하거나 개선할 의도가 없고 있는 그대로 제공한다고 명시합니다. 기술 문서가 언급하는 `test_openrouter.py`도 분석 커밋의 추적 파일 목록에는 없습니다. 문서에 적혀 있다는 이유로 검증 스크립트가 제공된다고 가정할 수 없습니다. [저자의 범위 설명](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/README.md#L13-L15), [테스트 문서 언급](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/CLAUDE.md#L144-L146)

분석 커밋의 루트에는 `LICENSE` 파일이 없고 `pyproject.toml`·`frontend/package.json`에도 라이선스 선언이 없습니다. 공개 레포라는 사실만으로 구체적인 사용·재배포 허가 조건을 추정하지 않았습니다. [고정 커밋 파일 목록](https://github.com/karpathy/llm-council/tree/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131), [Python 매니페스트](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/pyproject.toml#L1-L13), [프런트엔드 매니페스트](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/frontend/package.json#L1-L28)

## 정리

LLM Council의 핵심은 여러 답변을 모으는 기능과, 그 답변을 평가하는 기능, 평가를 읽고 새 답변을 만드는 기능을 분리한 데 있습니다. 초기 응답과 평가 원문이 화면에 남기 때문에 사용자는 최종 문장 뒤의 선택과 논쟁을 되짚을 수 있습니다.

구현을 정확히 이해하려면 세 경계를 기억할 필요가 있습니다. Stage 2의 익명 레이블은 완전한 편향 제거가 아니며, 평균 순위는 의장의 수치적 의사결정 규칙이 아닙니다. 또한 단계별 SSE와 JSON 저장은 토큰 스트리밍이나 대화 전체 문맥의 전달을 뜻하지 않습니다. 이 레포는 이러한 차이를 작은 코드베이스에서 추적할 수 있는 다중 모델 비교 도구입니다.

### 분석 범위

README와 기술 문서, Python·프런트엔드 매니페스트, 서버와 HTTP 클라이언트, 모든 council·저장 함수, React 진입점·API·주요 컴포넌트와 CSS·개발 설정을 읽었습니다. 잠금 파일은 존재를 확인했으며 전이 의존성 전체에 대한 감사는 수행하지 않았습니다. 외부 OpenRouter 서비스의 현재 모델 제공 상태·가격·데이터 정책, 실제 모델 품질·지연·실패율, 대상 앱 실행과 브라우저 동작은 이 정적 코드 리뷰의 검증 범위에 포함하지 않았습니다.
