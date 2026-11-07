---
type: "Repo Review"
title: "[Repo Review] Memento — LLM 가중치 대신 경험을 축적하는 에이전트"
description: "Memento의 Planner–Executor와 MCP 도구 흐름을 추적하고, 성공·실패 사례 검색과 별도 검색기 학습이 에이전트의 입력을 어떻게 바꾸는지 분석합니다."
date: "2026-10-26"
tags:
  - "Repo Review"
  - "AI Agent"
  - "MCP"
  - "머신러닝"
resource: "https://github.com/Memento-Teams/Memento/commit/42fbbcac63dd58ed6856c0761357345a58e4f032"
generated:
  by: "process:blog-review"
  at: "2026-10-26T06:07:07+09:00"
sources:
  - id: "github:memento-teams/memento"
    resource: "https://github.com/Memento-Teams/Memento/commit/42fbbcac63dd58ed6856c0761357345a58e4f032"
    title: "Memento: Fine-tuning LLM Agents without Fine-tuning LLMs"
    author: "Memento-Teams"
    last_modified: "2025-10-05T15:34:17+01:00"
status: "stable"
year: "2026"
analyzed_at: "2026-10-26T06:07:07+09:00"
source_id: "memento-teams/memento"
source_revision: "42fbbcac63dd58ed6856c0761357345a58e4f032"
source_title: "Memento: Fine-tuning LLM Agents without Fine-tuning LLMs"
source_type: "repo"
source_url: "https://github.com/Memento-Teams/Memento/commit/42fbbcac63dd58ed6856c0761357345a58e4f032"
visual_sources:
  - path: "/img/reviews/2026/memento-review/runtime-flow.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/client/agent.py#L169-L248"
    caption: "리뷰어 작성, 분석 커밋 기준 Planner–Executor와 MCP의 실행 흐름; CBR 사례 주입은 no_parametric_cbr.py L399–410 대조."
  - path: "/img/reviews/2026/memento-review/memory-learning.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/client/parametric_memory_cbr.py#L499-L584"
    caption: "리뷰어 작성, 분석 커밋 기준 사례·학습 데이터 축적과 별도 검색기 학습; train_memory_retriever.py L255–324 대조."
---

## 경험을 쌓는 에이전트에서 무엇이 바뀌는가

같은 언어 모델을 쓰더라도, 이전에 성공한 조사 계획을 참고하는 에이전트와 매번 처음부터 계획하는 에이전트의 행동은 달라질 수 있습니다. Memento는 이 차이를 **사례 기반 추론(Case-Based Reasoning, CBR)** 으로 구현하는 프로젝트입니다. 과거 질문·계획·결과 판정을 외부 메모리에 저장하고, 현재 질문에 쓸 만한 사례를 골라 Planner의 입력에 넣습니다.

저장소의 부제는 *Fine-tuning LLM Agents without Fine-tuning LLMs*입니다. 여기서 가장 먼저 구분할 것은 **답을 생성하는 LLM의 가중치**와 **사례를 고르는 검색 모델의 가중치**입니다. 공개 코드의 Planner와 Executor는 API로 LLM을 호출합니다. 반면 Parametric Memory의 학습 스크립트는 별도의 문장 인코더와 이진 분류기를 실제로 학습합니다. 따라서 “LLM을 미세조정하지 않는다”와 “어떤 모델도 학습하지 않는다”는 다른 설명입니다. [프로젝트의 정의](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/README.md#L48-L59), [검색 모델 학습 코드](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/memory/train_memory_retriever.py#L255-L295)

이 글은 `Memento-Teams/Memento`의 커밋 `42fbbcac63dd58ed6856c0761357345a58e4f032`를 정적으로 분석합니다. 대상 코드를 설치하거나 실행하지 않았으며, README의 성능 수치를 재현한 글도 아닙니다. 해당 커밋은 2025년 10월 5일 기록으로, 이 글의 분석일인 2026년 10월 26일과는 구분합니다. README가 인용하는 [Memento 논문](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/README.md#L418-L429)은 설계의 연결 맥락이며, 여기서는 공개 구현의 실제 연결을 중심으로 읽습니다.

## Memento의 정의와 세 가지 실행 경로

한 문장으로 정의하면, Memento는 **계획과 실행을 나누고, 과거 과제의 계획과 성공·실패 사례를 재사용하는 도구 사용 에이전트**입니다. Planner는 질문을 하위 과제로 나누고, Executor는 MCP 도구를 호출해 각 과제를 처리합니다. MCP(Model Context Protocol)는 모델과 도구 사이에서 도구 목록·입력 스키마·호출 결과를 주고받는 통신 인터페이스입니다.

다만 모든 진입점이 메모리까지 포함하는 것은 아닙니다. `client/agent.py`를 실행하면 CBR 학습이 자동으로 활성화된다고 읽어서는 안 됩니다.

| 실제 파일 | 주된 역할 | 사례 메모리 | 결과의 형태 |
|---|---|---|---|
| `client/agent.py` | 질문 또는 대화형 입력을 받는 기본 Planner–Executor | Case Bank를 읽고 쓰는 연결 없음 | 터미널에 최종 답변 출력 |
| `client/no_parametric_cbr.py` | 데이터셋을 순회하며 비학습 검색으로 사례 활용 | 질문 임베딩 유사도로 검색, 질문·계획·reward 추가 | 답변·실행 기록·판정 JSONL |
| `client/parametric_memory_cbr.py` | 학습된 검색기로 사례 활용 | query–case 적합성 점수, 사례 및 학습 데이터 추가 | 답변·검색 사례·실행 기록 JSONL |
| `client/agent_local_server.py` | 로컬 OpenAI 호환 서버를 Executor로 연결하는 별도 구현 | CBR 진입점과 별도로 존재 | 질문별 답변 출력 |

기본 진입점의 기본 모델은 Planner `gpt-4.1`, Executor `o3-2025-04-16`입니다. 두 CBR 진입점의 환경변수 기본값은 Planner `gpt-4.1`, Executor `o4-mini`이며, 정답 판정기는 `gpt-4o-mini`입니다. 따라서 README의 모델 설명 하나를 모든 경로에 공통 적용하면 실행 조건을 잘못 읽게 됩니다. [기본 CLI](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/client/agent.py#L258-L301), [비학습 CBR의 모델 설정](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/client/no_parametric_cbr.py#L545-L549), [학습형 CBR의 모델 설정](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/client/parametric_memory_cbr.py#L540-L544)

## 디렉터리와 아키텍처

파일을 역할별로 나누면 다음과 같습니다. 이 표는 README에 그려진 예정 구조가 아니라 고정 커밋에 실제 있는 파일을 기준으로 합니다.

| 영역 | 핵심 파일 | 책임 |
|---|---|---|
| 에이전트 클라이언트 | `client/agent.py`, 두 CBR 파일 | 계획 생성, 하위 과제 실행, MCP 호출, 답변 조립 |
| 비학습 사례 검색 | `memory/np_memory.py` | JSONL 파싱, 임베딩, 유사도 순위 계산 |
| 학습형 사례 검색 | `memory/parametric_memory.py` | 체크포인트 로딩, query–case 점수 계산 |
| 검색기 학습 | `memory/train_memory_retriever.py` | 데이터셋 구성, 학습·검증, 체크포인트 저장 |
| 도구 서버 | `server/*.py` | 검색·크롤링·문서·코드·미디어 등 기능을 MCP로 노출 |
| 코드 실행 백엔드 | `server/interpreters/` | subprocess, Docker, E2B 등의 구현 |
| 평가용 입력·메모리 | `data/deepresearcher.jsonl`, `memory/*.jsonl` | 질문·정답과 축적 사례·학습 쌍 |

![질문과 사례가 Planner에 입력되고 Executor와 MCP 도구를 거쳐 답변으로 돌아오는 Memento의 실행 구조]({{ '/img/reviews/2026/memento-review/runtime-flow.svg' | relative_url }})

*리뷰어 작성, 분석 커밋 기준 실행 흐름입니다. CBR에서는 사례가 Planner 입력에 추가되며, 과제 결과를 받은 Planner가 재계획하거나 최종 답변을 만듭니다. 그림의 MCP 왕복은 Executor 내부에서 반복됩니다. [기본 실행 루프](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/client/agent.py#L204-L248), [사례 주입](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/client/no_parametric_cbr.py#L399-L410)*

중요한 경계는 세 가지입니다. **LLM API**, **로컬 MCP 서버 프로세스**, **파일 기반 메모리**입니다. MCP를 쓴다는 이유로 도구가 전부 로컬에서 완료되는 것은 아닙니다. 도구 서버 안에서도 검색 서비스나 별도 LLM·문서 처리 API를 호출할 수 있습니다.

## 작동 원리 1: 질문에서 최종 답변까지

### 1. 도구 서버를 시작하고 함수 스키마를 만듭니다

`connect_to_servers()`는 Python 또는 JavaScript 서버 파일을 별도 프로세스로 시작하고, 표준 입출력(stdio)으로 MCP 세션을 연결합니다. 세션 초기화 후 `list_tools()`로 도구 이름을 가져와 `도구 이름 → 세션` 사전에 저장합니다. 이름이 중복되면 예외를 발생시킵니다. `_tools_schema()`는 도구의 설명과 `inputSchema`를 OpenAI 함수 호출 형식으로 옮깁니다. [연결 및 스키마 구성](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/client/agent.py#L169-L201)

이때 한 서버가 여러 도구를 제공하면 `self.sessions.values()`에 같은 세션이 여러 번 나타납니다. 현재 `_tools_schema()`의 캐시는 `list_tools()` 재호출은 줄이지만, 이미 처리한 세션을 건너뛰지는 않습니다. 따라서 동일 서버의 도구 목록이 결과 배열에 반복 추가될 수 있습니다. `math_tool.py`처럼 여러 함수를 제공하는 서버가 실제 존재합니다. API가 이를 어떻게 처리할지는 실행 확인하지 않았습니다. **캐시가 존재한다는 사실과 중복 스키마가 제거된다는 사실은 다릅니다.** [스키마 반복문](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/client/agent.py#L185-L201), [수학 도구들](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/server/math_tool.py#L14-L43)

### 2. Planner는 JSON 계획 또는 최종 답변을 냅니다

`process_query()`는 질문과 선택적인 파일 경로를 사용자 메시지로 넣습니다. Planner의 시스템 프롬프트는 `plan` 배열에 `id`와 `description`을 가진 하위 과제를 출력하도록 요구합니다. 코드에서는 먼저 응답이 `FINAL ANSWER:`로 시작하는지 확인하고, 그렇지 않으면 JSON 계획으로 파싱합니다. [프롬프트](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/client/agent.py#L29-L43), [분기](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/client/agent.py#L204-L224)

계획 수정은 최대 세 번의 바깥 루프로 제한됩니다. 다만 이는 전체 도구 호출 세 번을 뜻하지 않습니다. 각 하위 과제의 Executor에는 별도의 `while True` 반복문이 있으므로, 도구 사용을 끝내는 자연어 응답이 나올 때까지 내부 호출이 이어질 수 있습니다. 바깥 루프가 소진되면 마지막 Planner 응답을 그대로 반환합니다. 따라서 반환 문자열이 항상 검증된 최종 답변 형식이라고 보장되지는 않습니다. [반복과 반환](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/client/agent.py#L210-L248)

### 3. Executor가 도구를 고르고 결과를 다시 읽습니다

각 하위 과제에 대해 Executor는 자신의 시스템 프롬프트, 공유 이력, 현재 과제 설명을 받습니다. 함수 호출이 나오면 함수 이름과 JSON 인자를 해석하고, 연결된 MCP 세션의 `call_tool()`을 호출합니다. 도구 결과를 `role: tool` 메시지로 추가한 뒤 Executor를 다시 호출합니다.

다음은 실제 코드 중 도구를 찾고 호출하는 부분입니다. 전체 함수에서 필요한 부분만 발췌했습니다.

```python
for call in exec_reply.get("tool_calls") or []:
    t_name = call["function"]["name"]
    t_args = json.loads(call["function"].get("arguments") or "{}")
    session = self.sessions[t_name]
    result_msg = await session.call_tool(t_name, t_args)
    result_text = str(result_msg.content)
```

출처: [client/agent.py](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/client/agent.py#L237-L242)

도구 실행 기록 전체를 Planner에 그대로 넘기는 방식은 아닙니다. 기본 구현에서 자세한 도구 왕복은 `exec_msgs`에 쌓이고, Executor가 내놓은 하위 과제 결과가 `Task … result:` 형태로 공유 이력에 들어갑니다. Planner는 이 결과를 받아 남은 일을 다시 계획합니다. 두 CBR 구현은 별도로 `meta_trace`, `executor_trace`, `tool_history`도 수집합니다. **Planner의 입력 이력과 사후 분석용 실행 로그는 서로 다른 자료구조**입니다. [기본 공유 이력](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/client/agent.py#L223-L247), [CBR 기록 구조](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/client/no_parametric_cbr.py#L283-L312)

### 4. 외부 모델 호출과 문맥 절감도 실행 조건입니다

`OpenAIBackend.chat()`은 메시지와 도구 스키마를 Chat Completions API로 보냅니다. 기본 진입점에는 OpenAI/Azure 분기가 있습니다. Executor 메시지는 토큰 수를 계산해 오래된 메시지를 버리며, 시스템 메시지는 유지합니다. 이는 요약 메모리나 장기 기억을 만드는 작업이 아니라 **현재 실행 문맥을 자르는 작업**입니다. Planner와 Executor의 모델 가중치를 업데이트하는 코드도 아닙니다. [API 백엔드](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/client/agent.py#L64-L113), [문맥 절감](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/client/agent.py#L142-L157)

## 작동 원리 2: 비학습 CBR은 무엇을 검색하는가

`no_parametric_cbr.py`는 대화형 기본 진입점과 달리 `../data/deepresearcher.jsonl`을 읽는 배치 평가 스크립트입니다. 시작 시 메모리 JSONL을 읽어 질문과 계획의 쌍을 만듭니다. 기본 메모리 파일은 `dummy_memo.jsonl`, 기본 검색 개수는 8입니다. 검색 결과는 현재 질문이 Planner에게 전달되기 전에 성공 사례와 실패 사례로 나뉘어 추가됩니다. [입력 및 기본 설정](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/client/no_parametric_cbr.py#L59-L115), [메모리 로딩](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/client/no_parametric_cbr.py#L327-L356)

### 질문 임베딩의 유사도로 먼저 고릅니다

`memory/np_memory.py`는 저장된 질문들을 임베딩하고 L2 정규화합니다. 현재 질문도 같은 방식으로 처리한 다음 행렬 곱으로 점수를 계산해 상위 K개를 선택합니다. 정규화된 벡터의 내적이므로 코사인 유사도에 해당합니다. 인코더는 이 경로에서 `princeton-nlp/sup-simcse-bert-base-uncased`입니다. [임베딩 및 순위 계산](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/memory/np_memory.py#L38-L101)

여기서 검색 순위 자체는 저장된 `reward`를 사용하지 않습니다. 먼저 질문이 비슷한 사례를 고른 뒤, `line_index`로 원본 레코드를 찾아 `reward == 1`인 사례를 Positive Examples에 넣고 나머지를 Negative Examples에 넣습니다. 성공 사례에는 따를 만한 계획을, 실패 사례에는 피할 패턴을 담도록 Planner를 유도합니다. README의 “retrieves by value”라는 표현을 이 비학습 구현의 “보상순 정렬”로 해석해서는 안 됩니다. [사례 프롬프트 구성](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/client/no_parametric_cbr.py#L131-L172)

구현상 모든 저장 질문의 임베딩을 검색할 때마다 다시 계산하며, 지속되는 벡터 인덱스나 임베딩 캐시를 쓰는 연결은 없습니다. 또한 `MEMORY_DEVICE` 기본값은 `auto`이지만 클라이언트 초기 로딩은 모델에 `.to('cuda')`를 직접 적용합니다. 따라서 옵션 이름만 보고 CPU 전용 환경이 그대로 지원된다고 판단하기 어렵습니다. [검색별 임베딩 계산](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/memory/np_memory.py#L81-L87), [클라이언트의 CUDA 로딩](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/client/no_parametric_cbr.py#L105-L115)

### 실행을 채점한 뒤 사례를 추가합니다

한 질문을 처리하면 `llm_judge()`가 질문·정답 목록·예측 답변을 `gpt-4o-mini`에 전달합니다. 판정이 `correct`이면 reward 1, 아니면 0입니다. 전체 실행 기록을 결과 JSONL에 쓰고, 메모리에는 `question`, `plan`, `reward`를 추가합니다. 이어 메모리를 다시 읽으므로 뒤의 질문은 앞에서 추가한 사례를 검색할 수 있습니다. [판정 함수](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/client/no_parametric_cbr.py#L504-L527), [저장 및 재로딩](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/client/no_parametric_cbr.py#L559-L606)

이 공개 경로의 메모리는 전체 행동 궤적을 그대로 검색하는 저장소와도 다릅니다. 자세한 실행 흔적은 결과 로그에 있고, 재사용 메모리에 추가되는 핵심은 **질문과 마지막 계획 및 최종 판정**입니다. README가 언급하는 상태·행동·보상 튜플이라는 개념과 실제 JSONL 필드를 구분해 읽어야 합니다.

## 작동 원리 3: Parametric Memory에서는 검색기를 학습합니다

### 사례와 현재 질문의 쌍에 점수를 줍니다

`memory/parametric_memory.py`의 `CaseRetriever`는 `princeton-nlp/sup-simcse-roberta-base`를 기반으로 `MemoryRetrieverClassifier`를 만들고, 지정된 체크포인트의 가중치를 읽습니다. 사례 질문과 계획은 `[CASE]`, `[PLAN]` 구획을 가진 텍스트로 합칩니다. [모델 로딩 및 입력 형식](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/memory/parametric_memory.py#L10-L77)

현재 질문과 각 사례 텍스트를 같은 인코더에 각각 통과시킨 뒤 첫 토큰의 표현을 이어 붙이고, MLP(Multi-Layer Perceptron)로 이진 분류 로짓을 만듭니다. 그 결과의 softmax 중 클래스 1 점수를 사례 선택 점수로 사용합니다. 이 구현은 두 텍스트를 한 입력으로 함께 인코딩하는 cross-encoder가 아니라, **공유 인코더의 두 표현을 결합하는 분류기**입니다. [분류기](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/memory/train_memory_retriever.py#L15-L29), [추론 점수](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/memory/parametric_memory.py#L24-L45)

검색기 자체의 `retrieve()`는 입력 순서대로 점수를 반환하고, 실제 정렬과 상위 K개 선택은 CBR 클라이언트의 `_retrieve_cases()`에서 수행합니다. 반환 사례는 저장된 `case_label`에 따라 성공·실패 예시로 구분됩니다. 클래스 1 점수와 과거 사례의 성공 라벨도 같은 필드가 아닙니다. [정렬과 선택](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/client/parametric_memory_cbr.py#L335-L363), [예시 구성](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/client/parametric_memory_cbr.py#L121-L162)

### 학습용 라벨은 현재 실행의 최종 성공 여부입니다

`save_training_data()`는 현재 질문에 검색된 각 사례를 하나의 학습 행으로 저장합니다. 각 행에는 `query`, `case`, `case_label`, `plan`, `truth_label`이 들어갑니다. `case_label`은 과거 사례 자체의 성공·실패이고, `truth_label`은 **그 사례를 포함해 실행한 현재 질문의 최종 성공 여부**입니다.

```python
training_entry = {
    "query": query,
    "case": case.get("case", ""),
    "case_label": case.get("case_label", "unknown"),
    "plan": case.get("plan", ""),
    "truth_label": is_correct
}
```

출처: [client/parametric_memory_cbr.py](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/client/parametric_memory_cbr.py#L499-L510)

따라서 같은 실행에서 검색한 여러 사례에는 같은 `truth_label`이 붙습니다. 이는 사례 하나의 인과적 기여를 개별 측정한 라벨은 아닙니다. 정답·오답 여부는 최종 산출물에 대한 피드백이고, 어느 사례가 얼마나 도움을 줬는지는 이 저장 함수만으로 분리되지 않습니다. 검색기를 “도움이 될 가능성을 학습하는 모델”로 읽을 수는 있지만, 해당 점수가 인과적 유용성이나 보정된 성공 확률을 보장한다고 해석할 근거는 없습니다.

![사례 검색과 에이전트 실행으로 모은 최종 성공 라벨이 별도 검색기 학습으로 연결되는 흐름]({{ '/img/reviews/2026/memento-review/memory-learning.svg' | relative_url }})

*리뷰어 작성, 분석 커밋 기준 메모리 흐름입니다. 실행 루프는 사례와 학습 데이터를 추가하고, 별도 학습 스크립트가 검색기 가중치를 갱신합니다. 공개 CBR 루프 안에는 학습 스크립트를 자동 실행하는 연결이 없습니다. [실행 후 저장](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/client/parametric_memory_cbr.py#L555-L584), [학습 및 체크포인트](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/memory/train_memory_retriever.py#L255-L324)*

### 가중치를 바꾸는 과정은 별도 스크립트입니다

학습 데이터셋은 현재 질문과 사례 텍스트 및 `truth_label`을 읽습니다. 학습 코드에서 인코더를 고정하는 설정은 없고, `model.named_parameters()` 전체를 옵티마이저에 넣습니다. 따라서 학습되는 것은 MLP만이 아니라 **문장 인코더와 분류기를 포함한 검색 모델**입니다. 교차 엔트로피 손실을 쓰며, 양성 클래스의 가중치를 조절할 수 있습니다. [데이터셋](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/memory/train_memory_retriever.py#L73-L103), [옵티마이저와 손실](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/memory/train_memory_retriever.py#L255-L271)

검증 지표는 정확도·F1·ROC AUC입니다. 기본 분할은 라벨 비율을 고려한 무작위 행 단위 분할이며, query 단위로 묶어 분리하지는 않습니다. 같은 질문에서 나온 여러 사례 쌍이 학습과 검증에 나뉠 수 있으므로, 이 검색기 검증 점수를 곧바로 “새로운 질문에 대한 일반화 성능”으로 읽으면 안 됩니다. 이는 공개 분할 코드와 데이터 생성 방식을 함께 읽은 리뷰어의 평가입니다. [검증 지표 및 분할](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/memory/train_memory_retriever.py#L128-L170)

체크포인트는 `last.pt` 및 선택적으로 `best.pt`에 저장됩니다. CBR 클라이언트는 시작할 때 검색기를 만들고, 질문 처리 후에는 메모리 풀을 다시 읽습니다. **메모리 풀을 다시 읽는 것과 새 검색기 체크포인트를 다시 읽는 것은 다릅니다.** 공개 실행 루프에는 학습 호출이나 새 가중치 로딩 호출이 연결돼 있지 않습니다. README의 “automated … model retraining” 완료 표시는 이 코드 연결만으로 확인되지 않습니다. [초기 검색기 로딩](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/client/parametric_memory_cbr.py#L99-L118), [질문 후 처리](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/client/parametric_memory_cbr.py#L578-L584), [README 완료 목록](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/README.md#L387-L392)

## MCP 도구 안에서는 무엇이 일어나는가

### 검색과 크롤링은 다른 단계입니다

기본 `agent.py`에는 SearxNG를 쓰는 `search_tool.py`가 연결됩니다. 이 도구는 검색어를 `/search`에 보내고 제목·URL·요약을 돌려줍니다. 반면 CBR 진입점은 기본 서버 목록에 SerpAPI 기반 `serp_search.py`와 `ai_crawl.py`를 둡니다. SearxNG를 구성했다고 해서 CBR도 자동으로 그 검색기를 쓰는 것은 아닙니다. [기본 서버 목록](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/client/agent.py#L264-L273), [CBR 서버 목록](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/client/parametric_memory_cbr.py#L62-L70), [검색 도구](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/server/search_tool.py#L54-L112)

`ai_crawl.py`의 `crawl_extract()`는 URL을 Markdown으로 읽고, 별도 `gpt-4.1` API 호출로 현재 질의에 관련된 답·근거·수치·불확실성을 추출합니다. Executor가 받은 도구 결과가 이미 다른 LLM을 거쳐 압축된 결과일 수 있다는 뜻입니다. 도구 사용 비용을 분석할 때도 Executor 호출 수만 세면 이 내부 모델 호출을 놓칩니다. 다만 토큰 비용이 실제 얼마나 줄어드는지는 이 리뷰에서 측정하지 않았습니다. [크롤링·추출](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/server/ai_crawl.py#L99-L140), [노출 도구](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/server/ai_crawl.py#L147-L185)

SerpAPI 도구의 `api_key`는 이 커밋에서 빈 문자열로 남아 있습니다. README의 일반 API 설정만으로 실제 검색까지 연결된다고 단정하기 어렵습니다. [해당 설정](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/server/serp_search.py#L29-L37)

### 문서 처리는 확장자별로 분기합니다

`process_document()`는 문서 추출 함수를 워커 스레드로 넘깁니다. 내부에서는 이미지 분석, 음성 전사, PPTX, 스프레드시트, JSON/XML, Word 문서, PDF 등의 처리로 분기합니다. 음성은 AssemblyAI, 일부 문서는 Chunkr 등 외부 서비스에 의존합니다. 하나의 MCP 함수가 모든 형식을 단일 로컬 파서로 처리하는 구조는 아닙니다. [문서 처리 분기](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/server/documents_tool.py#L97-L168), [MCP 래퍼](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/server/documents_tool.py#L256-L270)

### 코드 실행의 기본 경로는 호스트 subprocess입니다

`server/code_agent.py`는 작업 디렉터리에 파일을 쓰고 터미널 명령을 실행하는 MCP 도구를 제공합니다. 여러 인터프리터 구현이 있지만, 외부에 노출된 `execute_terminal_command()`는 명시적으로 `subprocess` 백엔드를 고릅니다. 내부에서 Bash 명령을 실행하고, 자식 프로세스에는 호스트의 환경변수를 복사합니다. [MCP 실행 함수](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/server/code_agent.py#L591-L653), [터미널 명령 전달](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/server/code_agent.py#L455-L480), [subprocess 실행](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/server/interpreters/subprocess_interpreter.py#L170-L207)

README와 코드 주석의 “sandbox”를 기본적인 컨테이너 격리 보장으로 받아들여서는 안 됩니다. Python import 검사 함수는 별도로 존재하지만, 이 터미널 경로에서 그 검사를 호출하는 연결은 없습니다. 작업 디렉터리를 바꾸는 것만으로 파일·네트워크·자격증명 접근 권한이 분리되지는 않습니다. 이 설명은 공격을 실행한 결과가 아니라, 실제 기본 호출 경로를 따라간 정적 분석입니다.

## 설치와 사용: 문서의 명령과 실제 파일을 함께 봐야 합니다

이 커밋의 README는 Python 3.11 이상, OpenAI 또는 호환 API, 검색 서비스, 영상 처리용 FFmpeg, Parametric Memory용 PyTorch 등을 전제로 설명합니다. API·도구별 설정이 필요하며 모든 기능이 API 키 하나만으로 끝나는 구성은 아닙니다. [요구 사항](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/README.md#L84-L90), [환경변수](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/README.md#L185-L215)

아래 명령은 README의 `uv` 설치 경로 중 **이미 uv를 준비한 뒤 사용하는 부분**만 발췌한 것입니다. 이 리뷰에서 실행한 절차가 아닙니다. README의 clone 주소는 이전 소유자 경로를 사용합니다.

```bash
git clone https://github.com/Agent-on-the-Fly/Memento
cd Memento
uv sync
source .venv/bin/activate
```

출처: [README 설치 절차](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/README.md#L98-L111)

기본 대화형 사용 명령도 README에 있습니다.

```bash
python client/agent.py
```

출처: [README 대화형 사용법](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/README.md#L230-L236)

다만 이를 저장소 루트에서 그대로 실행하면, `agent.py`의 서버 기본 경로 `../server/...`는 현재 작업 디렉터리를 기준으로 해석됩니다. 코드가 이 경로를 `__file__` 기준으로 보정하지 않으므로, 루트에서 시작하는 README 명령과 기본 경로가 맞지 않습니다. 이 글에서는 검증하지 않은 수정 명령을 성공 예제로 덧붙이지 않습니다. [서버 경로 처리](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/client/agent.py#L169-L176), [기본값](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/client/agent.py#L264-L273)

Parametric Memory 학습 명령은 README에 다음과 같이 제시돼 있습니다. 파일과 인자는 실제 학습 스크립트에 대응하지만, 준비된 입력 데이터·의존성·환경을 포함해 동작을 확인한 것은 아닙니다.

```bash
cd memory
python train_memory_retriever.py \
  --train training_data.jsonl \
  --output_dir ./ckpts/retriever \
  --use_plan \
  --val_ratio 0.1 \
  --batch_size 32 \
  --lr 2e-5 \
  --epochs 10 \
  --save_best
```

출처: [README 검색기 학습](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/README.md#L242-L259)

사용 전에 구분할 문서·코드 차이는 다음과 같습니다.

| 문서의 설명 | 고정 커밋의 실제 상태 | 의미 |
|---|---|---|
| 상세 설치 문서 `INSTALL.md` 링크 | 파일 없음 | 추가 설치 안내를 해당 링크로 확인할 수 없음 |
| `cd client` 뒤 `python parametric_memory.py` | 그 이름은 `memory/`의 독립 검색기 파일이며, CBR 에이전트는 `client/parametric_memory_cbr.py` | 문서의 에이전트 실행 파일명이 실제와 다름 |
| `run_parametric.sh`, `PARAMETRIC_MEMORY_GUIDE.md`, `retrain.sh` | 파일 없음 | 보조 실행·자동 재학습 절차가 제공됐다고 볼 수 없음 |
| `ai_crawler.py` | 실제 이름은 `server/ai_crawl.py` | README의 구조·뉴스 표기와 파일명이 다름 |
| `uv sync` | `pyproject.toml`에 torch·transformers·scikit-learn·tqdm 등이 없지만 `requirements.txt`에는 있음 | 두 설치 경로의 선언된 의존성 구성이 다름 |
| Parametric Memory 체크포인트 경로 | 코드에 기본 경로는 있지만 해당 `ckpts/` 파일은 트리에 없음 | 별도 학습 또는 적합한 체크포인트 준비가 필요 |

문서 근거: [설치 문서 링크](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/README.md#L92), [실행 명령](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/README.md#L275-L281), [예정 디렉터리](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/README.md#L319-L363). 의존성은 [pyproject.toml](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/pyproject.toml)과 [requirements.txt](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/requirements.txt)를 대조했습니다. 표의 파일 부재는 이 분석 커밋의 Git 트리 기준입니다.

`.env.example`에도 숫자 옵션의 빈 값이 있습니다. 예를 들어 `MEMORY_TOP_K`를 빈 문자열로 둔 채 읽으면 `int(os.getenv(...))`의 기본값은 적용되지 않습니다. 기본값은 변수가 없을 때 쓰이며, 빈 값을 유효한 숫자로 바꾸는 처리는 해당 코드에 없습니다. 환경변수 템플릿의 “fallback available” 주석과 실제 파싱 조건을 구분해야 합니다. [환경변수 예시](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/.env.example#L10-L17), [파싱](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/client/parametric_memory_cbr.py#L99-L104)

로컬 모델은 별도 `agent_local_server.py`의 OpenAI 호환 서버 연결로 다룹니다. Executor 모델명이 `qwen3`로 시작할 때 `DirectModelBackend`를 고르며 기본 모델명은 `qwen3-8b`입니다. 이것만으로 Planner·도구 내부 모델·CBR까지 모두 로컬화됐다는 뜻은 아닙니다. 해당 경로의 스트리밍 조립·함수명 보정 전체와 실제 vLLM 호환성은 이 글의 상세 검토 범위에서 제외했습니다. [백엔드 선택](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/client/agent_local_server.py#L360-L377), [CLI 기본값](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/client/agent_local_server.py#L588-L600)

## 성능 수치와 구현상 주의점을 읽는 방법

README는 GAIA validation 87.88%(Pass@3 Top-1), test 79.40%, DeepResearcher 66.6% F1·80.4% PM, SimpleQA 95.0%, HLE 24.4% PM을 보고합니다. 이는 **저자 보고 수치**이며 서로 다른 데이터셋과 지표입니다. 이를 한 개의 통합 정확도로 묶을 수 없고, 현재 저장소를 설치하면 그대로 얻는 결과라고 주장할 수도 없습니다. 이 섹션의 README만으로 각 수치의 전체 평가 조건과 재현 절차가 갖춰졌다고 보지 않았으며, 본 리뷰에서는 원논문의 실험표를 별도로 재검증하지 않았습니다. [README 성능 섹션](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/README.md#L300-L313)

그보다 코드에서 확실히 배울 수 있는 부분은 다음과 같습니다.

- **기억의 단위가 중요합니다.** 결과 로그에는 도구 기록이 있지만 재사용 메모리에는 질문·계획·라벨이 주로 남습니다. “경험을 저장한다”는 설명만으로 무엇이 다시 입력되는지 알 수 없습니다.
- **피드백의 품질이 학습 데이터의 품질입니다.** 두 CBR 판정기는 API 호출·JSON 파싱 실패도 `incorrect`로 돌려줍니다. 이후 코드가 이를 실패 사례와 학습 라벨로 저장하므로, 과제 실패와 판정 인프라 실패가 섞일 수 있습니다. [비학습 판정 예외](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/client/no_parametric_cbr.py#L511-L527), [학습형 판정 예외](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/client/parametric_memory_cbr.py#L480-L496)
- **온라인 사례 축적과 온라인 가중치 갱신은 다릅니다.** 새 사례가 다음 질문의 입력을 바꾸는 연결은 있지만, 실행 중 retriever를 자동 재학습하는 연결은 확인되지 않습니다.
- **도구 프로토콜은 실행 권한을 대신하지 않습니다.** MCP의 통일된 호출 형태와 호스트에서 실행되는 코드의 격리 수준은 별도로 확인해야 합니다.

라이선스는 루트 `LICENSE`의 MIT입니다. 저작권 및 허가 고지 유지 조건과 무보증 조항이 있으며, 저장소 코드의 라이선스가 외부 API 이용 조건까지 대신하는 것은 아닙니다. [라이선스 원문](https://github.com/Memento-Teams/Memento/blob/42fbbcac63dd58ed6856c0761357345a58e4f032/LICENSE)

## 이 글에서 다루지 못한 부분

핵심 세 클라이언트와 메모리 로딩·검색·저장·학습 흐름, 검색·크롤링·문서·코드 실행 도구의 연결을 읽었습니다. 반면 이미지·영상·스프레드시트 도구의 전체 예외 경로, 모든 문서 형식의 변환 결과, Docker/E2B/Jupyter 백엔드의 운영 동작, 로컬 모델의 전체 스트리밍 호환성은 분석하지 않았습니다. 실제 API 응답, GPU 메모리 사용량, 검색 시간, 벤치마크 재현 성능도 측정하지 않았습니다.

## 결론

Memento의 핵심은 생성 LLM의 가중치를 바꾸는 대신, **과거 과제의 계획을 골라 현재 Planner의 입력을 바꾸는 것**입니다. 비학습 경로는 질문 유사도로 후보를 고르고 성공·실패를 구분해 제시합니다. 학습형 경로는 현재 질문과 과거 사례의 쌍에 점수를 매기는 별도 검색기를 둡니다.

공개 구현을 따라가면 경험 축적, 검색, 계획, 도구 실행, 평가, 검색기 학습이 각각 다른 단계라는 사실이 드러납니다. 이 단계를 분리해 읽는 것이 Memento의 설계 의도와 현재 코드가 실제로 연결한 범위를 함께 이해하는 출발점입니다.
