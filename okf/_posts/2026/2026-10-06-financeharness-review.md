---
type: "Repo Review"
title: "[Repo Review] FinanceHarness — 검색·계산·인용을 잇는 금융 리서치 에이전트의 내부 구조"
description: "FinanceHarness의 질문 입력부터 도구 공개, 구조화 결과 참조, 금융 계산, 웹 인용과 보고서 출력까지 추적하고 각 단계의 검증 경계를 살펴봅니다."
date: "2026-10-06"
tags:
  - "Repo Review"
  - "AI Agent"
  - "Python"
resource: "https://github.com/Yijia-Xiao/FinanceHarness/tree/1163c5e7a8f35ff6217c3a480f7b04562355e0cc"
generated:
  by: "process:blog-review"
  at: "2026-10-06T06:09:39+09:00"
sources:
  - id: "Yijia-Xiao/FinanceHarness"
    resource: "https://github.com/Yijia-Xiao/FinanceHarness/tree/1163c5e7a8f35ff6217c3a480f7b04562355e0cc"
    title: "FinanceHarness: Autonomous Financial Deep Research Framework"
    last_modified: "2026-08-22T08:09:37-05:00"
status: "stable"
year: "2026"
analyzed_at: "2026-10-06T06:09:39+09:00"
source_id: "Yijia-Xiao/FinanceHarness"
source_revision: "1163c5e7a8f35ff6217c3a480f7b04562355e0cc"
source_type: "repo"
source_url: "https://github.com/Yijia-Xiao/FinanceHarness/tree/1163c5e7a8f35ff6217c3a480f7b04562355e0cc"
visual_sources:
  - path: "/img/reviews/2026/financeharness-review/research-flow.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/runtime/agent.py#L296-L460"
    caption: "리뷰어 작성, 분석 커밋 기준. research.py의 조립과 Agent.run의 도구 반복 및 최종 출력을 재구성했습니다."
  - path: "/img/reviews/2026/financeharness-review/reference-flow.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/runtime/dispatch.py#L132-L215"
    caption: "리뷰어 작성, 분석 커밋 기준. 가격 데이터의 structured 결과가 prev 참조 해석과 입력 검증을 거쳐 상관 계산으로 전달되는 경로입니다."
---

## 들어가며

금융 리서치 질문 하나를 답하려면 성격이 다른 작업이 연결되어야 합니다. 기업의 사업 상황은 문서를 읽어 파악하고, 가격·재무 수치는 데이터 공급자에서 가져오며, 가치평가나 위험 지표는 명시적인 계산을 거쳐야 합니다. 마지막 보고서에서는 이 자료와 계산 결과가 어떤 근거에서 나왔는지도 구분해야 합니다.

FinanceHarness는 이 흐름을 하나의 언어 모델 에이전트로 묶는 Python 프레임워크입니다. README는 질문을 받아 계획하고, 근거를 모으고, 분석한 뒤 인용이 달린 보고서를 작성하는 도구로 소개합니다. 코드에서 특히 눈에 띄는 부분은 **모델에게 보여 주는 도구 설명, 실제 계산에 전달되는 구조화 데이터, 보고서 끝에 붙는 웹 출처를 서로 다른 경로로 관리한다는 점**입니다. [README의 소개](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/README.md#L24-L41)

이 글은 `Yijia-Xiao/FinanceHarness`의 커밋 `1163c5e7a8f35ff6217c3a480f7b04562355e0cc`를 고정해 읽은 정적 코드 리뷰입니다. 의존성을 설치하거나 대상 코드를 실행하지 않았으며, 아래 내용은 실제 실행 성공률이나 금융 분석의 정확도를 측정한 결과가 아닙니다. 금융 도구가 입력을 어떻게 처리하는지 설명하는 데 초점을 맞춥니다.

## FinanceHarness는 무엇인가요?

한 문장으로 정의하면, **웹 조사·금융 데이터 조회·수치 계산을 호출 가능한 도구로 제공하고, 모델이 이 도구들을 선택해 보고서를 만들도록 제어하는 실행 틀**입니다. 여기서 하네스(harness)는 모델 자체가 아니라 모델 호출, 상태, 도구 실행, 오류 처리, 결과 저장을 감싸는 코드를 뜻합니다.

이 저장소는 모델 가중치를 학습하는 구현보다 이미 제공되는 모델과 외부 자료를 연결하는 데 중심을 둡니다. 패키지 매니페스트는 Python 3.12 이상을 요구하고, 모델 호출에 `openai`와 `google-genai`, 입력 검증에 `pydantic`, 웹 처리에 `httpx`·`ddgs`·`trafilatura`·`pdfplumber`, 금융 데이터에 `yfinance`, 서비스에 `fastapi`·`uvicorn`을 의존성으로 선언합니다. 아래는 선언된 역할을 읽은 것이며 각 라이브러리의 서비스 가용성을 검증했다는 뜻은 아닙니다. [pyproject.toml](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/pyproject.toml#L1-L30)

사용 경로는 두 가지입니다. `fh` 또는 `financeharness` CLI는 한 번의 질문에 답하고 종료하며, `fh serve`는 HTTP 요청과 서버 발송 이벤트(SSE, 서버가 진행 상황을 순차 전달하는 형식)를 제공합니다. 두 경로 모두 최종적으로 `run_research()`를 사용합니다. [CLI 진입점](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/cli.py#L45-L95), [HTTP 진입점](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/service/app.py#L377-L401)

## 아키텍처: 조립 코드와 실행 루프를 분리합니다

| 경로 | 맡은 책임 | 다음 경계로 넘기는 것 |
|---|---|---|
| `main.py`, `financeharness/cli.py` | 명령행·표준입력을 읽고 프로필과 옵션을 선택합니다. | 질문, 모드, 진행 이벤트 콜백 |
| `financeharness/research.py` | 캐시, 도구 레지스트리, 스킬, 모델을 조립합니다. | 구성된 `Agent`와 질문 |
| `financeharness/runtime/agent.py` | 모델 응답과 도구 호출을 반복합니다. | 대화 메시지, 도구 기록, 종료 상태 |
| `runtime/tool_registry.py`, `dispatch.py`, `chaining.py` | 도구 계약, 입력 변환·검증, 결과 참조를 처리합니다. | 모델용 Markdown과 구조화 결과 |
| `financeharness/tools/` | 웹·시장 데이터·계산 기능을 구현합니다. | `ToolResponse` |
| `financeharness/providers/` | 모델별 프로토콜 차이를 감쌉니다. | 공통 `AssistantTurn` |
| `financeharness/service/` | HTTP/SSE와 지속 세션을 제공합니다. | JSON 응답 또는 이벤트 스트림 |

이 책임 분리는 [연구 실행 조립부](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/research.py#L58-L103), [에이전트 루프](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/runtime/agent.py#L296-L460), [공통 모델 응답](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/providers/base.py#L27-L77)에 직접 나타납니다.

![질문을 받은 뒤 도구를 조립하고 모델과 도구 호출을 반복하여 보고서와 실행 기록을 반환하는 흐름]({{ '/img/reviews/2026/financeharness-review/research-flow.svg' | relative_url }})

*리뷰어 작성, 분석 커밋 기준. [조립부](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/research.py#L58-L103)와 [실행·종료 경로](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/runtime/agent.py#L329-L460)를 재구성했습니다. 반복 화살표는 도구 결과가 다음 모델 호출의 메시지로 들어가는 경로이며, 외부 호출은 선택된 도구와 모델 프로필에 따라 발생합니다.*

## 작동 원리: 질문에서 보고서까지

### 1. CLI는 질문을 읽고 실행 환경을 조립합니다

설치된 두 명령은 매니페스트에서 모두 `financeharness.cli:main`에 연결됩니다. 소스 체크아웃의 `main.py`도 같은 함수를 호출하는 얇은 래퍼입니다. CLI는 위치 인수로 질문을 받으며, 질문이 없고 표준입력이 터미널이 아니면 파이프로 들어온 문자열을 읽습니다. 명시적으로 지정한 `--profile`은 backbone 역할의 프로필인지 검사하고, `--reader`는 등록된 프로필인지 검사한 다음 비동기 `_research()`를 시작합니다. [스크립트 등록](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/pyproject.toml#L22-L25), [질문·프로필 검사](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/cli.py#L181-L203)

`run_research()`는 먼저 모드를 프롬프트 변형으로 해석합니다. 이후 주 모델과 페이지를 읽는 reader 프로필을 고르고, 실행마다 새 `FetchCache`와 전체 도구 레지스트리를 만듭니다. `mode`를 바꿔도 레지스트리 구성은 동일합니다. `research`는 웹 조사 우선, `analytical`은 수치 분석 우선이라는 강조점이 달라지며, 명시 모드가 없으면 기존 `equity` 플래그에 따라 analytical 또는 research를 선택합니다. [조립부](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/research.py#L50-L94), [모드 해석](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/runtime/modes.py#L54-L69)

모드 차이가 프롬프트만으로 끝나는 것은 아닙니다. 조립부는 기본적으로 `research`에서만 최종 초안에 대한 grounding review, 즉 읽은 근거에 비추어 다시 쓰는 모델 호출을 켭니다. 따라서 README의 “일정한 도구 레지스트리 위의 프롬프트 변형”이라는 설명은 도구 구성에는 맞지만, 기본 후처리 비용까지 같다는 뜻은 아닙니다. [README 모드 설명](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/README.md#L106-L117), [grounding 기본값](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/research.py#L85-L93)

### 2. 도구는 등록과 공개를 따로 관리합니다

`ToolSpec`은 도구 이름, 설명, Pydantic 입력 스키마, 비동기 handler, `core` 또는 `deferred` 등급을 묶습니다. `ToolRegistry`에는 전체 도구가 등록되지만, 모델 API에 전달하는 JSON 스키마는 `ToolSessionState.visible_schemas()`가 따로 고릅니다. `core`는 처음부터 보이고, `deferred`는 이름과 설명을 담은 카탈로그로 소개한 뒤 필요할 때 스키마를 추가합니다. [ToolSpec](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/runtime/tool_registry.py#L58-L100), [공개 스키마 구성](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/runtime/tool_registry.py#L156-L198)

조립부는 웹 도구 `search`, `visit`, `compose_citations`와 `calc`, `update_plan`을 기본 등록하고, 데이터·계산 도구들을 추가합니다. 에이전트는 실행별 레지스트리 복사본에 `load_tool`과 `load_skill`을 연결합니다. 이 구성이 README의 “항상 보이는 일곱 도구”와 대응합니다. [도구 조립](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/tools/research/assembly.py#L49-L88), [실행별 메타 도구](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/runtime/agent.py#L273-L294)

`load_tool`이 하는 일도 구체적입니다. 요청된 도구를 `loaded_deferred` 집합에 넣고, 현재 도구 응답에는 해당 스키마를 Markdown으로 돌려줍니다. 다음 모델 호출부터는 그 스키마가 `tools` 인수에 포함됩니다. 스키마 공개를 늦추어 초기 문맥을 줄이는 점진적 공개(progressive disclosure)입니다. 다만 이름·설명 카탈로그는 시스템 프롬프트에 들어가므로, README의 “사용하기 전까지 비용이 들지 않는다”는 표현을 문자 그대로 토큰 비용 0으로 읽으면 안 됩니다. [load_tool](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/tools/core/load_tool.py#L33-L57), [카탈로그 프롬프트](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/runtime/prompts.py#L195-L216)

또한 이 구분은 실행 권한 경계가 아닙니다. dispatcher는 전체 레지스트리에서 이름으로 도구를 찾고, `loaded_deferred`에 포함되는지는 검사하지 않습니다. 이미 등록된 도구의 유효한 호출이 들어오면 스키마 공개 여부와 별개로 처리할 수 있는 구현입니다. [도구 조회와 실행 진입](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/runtime/dispatch.py#L119-L163)

### 3. 모델 응답과 도구 결과가 하나의 루프를 구성합니다

`Agent.run()`은 실행마다 새 도구 상태와 스킬 상태를 만들고, 시스템 프롬프트·기존 대화·현재 질문으로 `messages`를 구성합니다. 모델 호출에는 현재 공개된 도구 스키마를 전달합니다. 응답에 도구 호출이 있으면 `for` 루프에서 하나씩 `await`하여 실행하고, 결과를 `role: tool` 메시지로 추가합니다. 같은 응답 안의 여러 도구 호출도 이 에이전트 루프에서는 순차 처리됩니다. [실행 상태 초기화](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/runtime/agent.py#L308-L342), [도구 호출 반복](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/runtime/agent.py#L354-L391)

모델별 응답 형식은 provider 계층에서 `AssistantTurn`으로 정규화됩니다. 루프는 응답의 `tool_calls`, `content`, `finish_reason`을 읽습니다. Gemini용 native SDK 경로와 OpenAI 호환 Chat Completions 경로를 고르는 분기가 이 경계에 있으며, 에이전트 루프 자체가 각 공급자의 원시 응답 구조를 직접 처리하지 않습니다. [provider 선택](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/providers/__init__.py#L29-L42), [공통 응답 구조](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/providers/base.py#L27-L77)

도구 호출이 없으면 응답 본문을 `prediction`으로 삼습니다. 이때 종료 사유가 `stop`이어야 `termination: answer`가 됩니다. 실행 횟수나 시간 한도에 걸리는 경우에는 `max_rounds`나 `timeout`으로 끝나며, 모든 경로가 `_build_result()`로 모입니다. 결과에는 답변뿐 아니라 메시지, 도구 로그, 인용 통계, 경과 시간과 사용 모델도 들어갑니다. 따라서 “텍스트가 있다”와 “정상 답변으로 종료했다”는 구분이 결과 계약에 남습니다. [종료 판단](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/runtime/agent.py#L329-L350), [최종 결과](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/runtime/agent.py#L393-L460)

### 4. dispatcher가 입력을 정리하고 검증합니다

모델이 보낸 도구 인수는 JSON 문자열입니다. `dispatch_json_args()`가 이를 읽고, 다음 단계에서 문자열로 중복 포장된 배열·객체 등의 형태를 보정합니다. 이어서 `prev:` 참조를 실제 값으로 치환하고, 그 결과를 Pydantic 스키마로 검증한 뒤 handler를 실행합니다. 참조 치환이 검증보다 먼저라는 순서가 중요합니다. 계산 도구의 스키마가 요구하는 것은 숫자 배열이지만, 모델은 그 대신 앞선 결과를 가리키는 짧은 문자열을 보낼 수 있기 때문입니다. [JSON 해석](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/runtime/dispatch.py#L220-L249), [보정·치환·검증·실행](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/runtime/dispatch.py#L132-L174)

아래는 입력 검증과 handler 호출 부분을 그대로 인용한 코드입니다. 중간의 오류 처리 및 주석 일부는 생략했습니다. [dispatch.py](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/runtime/dispatch.py#L161-L174)

```python
    validated = spec.request_schema.model_validate(resolved)
```

```python
    with tool_event_scope(emit, name, call_id):
      response: ToolResponse = await spec.handler(validated)
```

형식 오류, 참조 실패, 스키마 위반, handler 예외는 각각 오류 결과로 바뀌어 다음 모델 호출의 문맥에 들어갑니다. “도구 실패 → 모델이 인수나 계획을 바꾸어 재시도할 기회”를 만드는 구조입니다. 다만 코드 주석의 `never-raise` 표현은 의도와 구분해야 합니다. 이 함수의 예외 처리 범위는 검증과 handler 실행을 중심으로 나뉘어 있으며, 예외를 표현 가능한 결과로 바꾼다는 사실만으로 모든 예상 밖 입력에서 중단이 없음을 입증할 수는 없습니다. [오류 결과 형식](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/runtime/dispatch.py#L93-L103), [handler 오류 처리](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/runtime/dispatch.py#L175-L201)

### 5. `prev:`가 구조화 결과를 다음 계산에 연결합니다

`ToolResponse`는 세 층으로 나뉩니다. `markdown`은 모델이 읽는 설명, `structured`는 프로그램이 다시 사용할 데이터, `meta`는 공급자나 실행 시간 같은 부가 정보입니다. 성공한 도구 호출의 `structured`는 `session_state.tool_results[call_id]`에 저장되며, 모델용 텍스트 끝에는 해당 호출 ID를 알리는 꼬리말이 붙습니다. [응답 계약](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/runtime/tool_registry.py#L46-L55), [결과 저장](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/runtime/dispatch.py#L203-L215)

참조 해석기는 `prev:<call_id>`로 전체 결과를 찾고, `.field`로 사전 키를, `[N]`으로 배열 원소를, `[*]`로 배열의 각 원소를 따라갑니다. 이 치환은 입력 사전과 배열 안에서도 재귀적으로 수행됩니다. 존재하지 않는 호출 ID나 필드, 잘못된 인덱스는 실패 이유를 포함한 결과로 돌아갑니다. 범용 JSONPath 엔진이 아니라 이 저장소에서 정한 제한적인 경로 문법입니다. [경로 파싱](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/runtime/chaining.py#L56-L89), [참조 해석과 재귀 치환](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/runtime/chaining.py#L170-L209)

구체적인 연결점은 가격 데이터에 있습니다. `data_equity_prices`는 yfinance의 이력 데이터를 읽어 날짜·시가·고가·저가·종가·거래량을 담은 `bars`를 구성합니다. 모델에게는 최근 일부 종가와 요약 지표를 보여 주지만, 구조화 결과에는 전체 `bars`가 남습니다. 따라서 소스가 안내하는 `prev:<id>.bars[*].close`는 앞선 호출의 종가 배열을 계산 도구에 전달하는 경로가 됩니다. 모델이 장기간의 가격을 다시 한 글자씩 출력할 필요를 줄이는 설계입니다. [가격 데이터 생성](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/tools/data/equity/prices.py#L153-L181), [전체 결과와 모델용 요약](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/tools/data/equity/prices.py#L111-L150)

![가격 조회의 전체 bars를 저장한 뒤 prev 참조로 종가 배열을 가져와 Pydantic 검증과 상관 계산에 전달하는 경로]({{ '/img/reviews/2026/financeharness-review/reference-flow.svg' | relative_url }})

*리뷰어 작성, 분석 커밋 기준. [가격 결과](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/tools/data/equity/prices.py#L111-L150), [참조 치환·입력 검증](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/runtime/dispatch.py#L132-L174), [상관 계산](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/tools/compute/risk/correlation.py#L53-L78)을 연결했습니다. 예시 출력값이나 실제 실행 결과를 그린 것은 아닙니다.*

이 설계에는 상태 수명도 따릅니다. `Agent.run()`은 매번 새 `ToolSessionState`를 만들며, `run_research()`도 새 웹 캐시를 만듭니다. HTTP 세션은 이전 `messages`를 이어 주지만, 앞선 실행의 구조화 결과 사전을 함께 복구하지는 않습니다. 따라서 한 실행 안의 `prev:` 연결과 여러 질문에 걸친 대화의 지속성을 같은 기능으로 볼 수 없습니다. 이전 실행의 ID가 현재 사전에 없으면 참조 해석이 실패합니다. [실행별 상태](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/runtime/agent.py#L308-L319), [캐시 생성](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/research.py#L66-L74), [세션 저장 내용](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/service/sessions.py#L103-L131)

### 6. 데이터 전달의 정확성과 계산 의미의 정확성은 별개입니다

상관 도구 `compute_risk_correlation`은 이름별 가격 배열을 받습니다. 먼저 단순 수익률로 바꾸고, 모든 배열을 같은 길이로 맞춘 뒤 표준 라이브러리 `statistics.correlation()`으로 Pearson 상관을 계산합니다. 분산이 0인 경우 등 계산할 수 없는 조합은 `None`으로 두고, 실제 사용한 관측 수 `n_obs`를 결과에 포함합니다. [입력 스키마](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/tools/compute/risk/correlation.py#L31-L50), [계산 본체](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/tools/compute/risk/correlation.py#L53-L78)

여기서 “맞춘다”의 정확한 뜻을 읽어야 합니다. 아래는 `align()`의 계산 부분입니다. [returns.py](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/tools/compute/risk/returns.py#L16-L22)

```python
  n = min((len(s) for s in series), default=0)
  return [s[len(s) - n :] for s in series]
```

이는 각 배열 끝의 같은 개수만 취하며, 날짜 키로 결합하지 않습니다. 앞에서 `bars[*].close`만 넘기면 날짜가 제거되고, 가격 조회는 값이 비어 있는 봉을 건너뜁니다. 그러므로 서로 다른 휴장일이나 결측치가 있는 두 시계열에서 같은 배열 위치가 반드시 같은 날짜를 뜻한다고 보장할 수 없습니다. 이 지점은 실행으로 재현한 결함 보고가 아니라, **스키마와 정렬 구현에서 확인되는 의미적 제약**입니다. 참조 전달이 숫자 재입력을 줄여도 날짜 정합성까지 대신 검증하는 것은 아닙니다. [결측 봉 처리](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/tools/data/equity/prices.py#L161-L175), [길이 기준 정렬](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/tools/compute/risk/returns.py#L16-L22)

DCF(미래 현금흐름을 현재 가치로 할인하는 계산) 역시 입력과 책임의 경계가 분명합니다. `DCFRequest`는 연도별 현금흐름 배열, 할인율, 잔존가치 계산 방법, 순부채와 주식 수 등을 받습니다. Gordon 성장 모형이면 잔존 성장률이 할인율보다 낮은지 검사하고, 배수 방식이면 EBITDA와 배수가 있는지 확인합니다. 계산 함수는 현금흐름을 연도별 할인계수로 나누고, 할인된 잔존가치를 더한 다음 순부채를 빼고 필요하면 주식 수로 나눕니다. [DCF 입력 검증](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/tools/compute/valuation/dcf.py#L31-L104), [DCF 계산](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/tools/compute/valuation/dcf.py#L107-L159)

반면 미래 현금흐름을 어떤 성장 가정으로 만들지는 이 계산 함수가 결정하지 않습니다. 번들 `dcf-valuation` 스킬은 모델에게 기초 재무 데이터와 추세를 바탕으로 현금흐름 일정을 만들고 가정을 명시하라고 안내합니다. 따라서 이 경로는 “정해진 입력을 재현 가능한 산술로 처리한다”는 장점과 “가정·단위·입력 선택은 별도로 살펴야 한다”는 조건을 함께 가집니다. 실제 주식의 적정가치나 매매 판단을 이 코드 리뷰에서 평가하지는 않습니다. [DCF 스킬의 작업 절차](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/skills/dcf-valuation/SKILL.md#L17-L42)

### 7. 웹 검색과 실제 인용은 다른 단계입니다

웹 쪽에서는 `search → visit → citation finalizer`가 중심 흐름입니다. `search`는 검색어별 결과를 모아 URL 중복을 제거하고 제목을 캐시에 남깁니다. 기본 조립에서는 빠른 fetch 검증기를 붙여 후보 페이지의 본문이 일정 길이 이상인지 확인하고, 읽을 수 있는 페이지 텍스트를 캐시에 미리 저장합니다. 그러나 검증 성공 후보가 하나도 없으면 원래 후보 목록으로 돌아갑니다. 따라서 반환된 모든 검색 결과가 항상 읽기 검증을 통과한 것은 아닙니다. [검색과 사전 fetch](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/tools/research/search.py#L77-L155)

`visit`는 캐시에 본문이 있으면 이를 사용하고, 없으면 가져온 뒤 reader 모델에 넘깁니다. reader가 접근 가능하다고 판단하고 요약이 비어 있지 않을 때만 해당 URL을 인용 목록에 추가합니다. 이 조건에는 원문 인용문인 `evidence`가 비어 있지 않아야 한다는 강제 검사가 없습니다. 또한 reader는 페이지 전체가 아니라 앞의 24,000자만 받아 처리합니다. 페이지를 성공적으로 방문했다는 기록과 문서 전체를 빠짐없이 읽었다는 주장은 구분해야 합니다. [visit의 등록 조건](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/tools/research/visit.py#L148-L209), [reader 입력 길이와 반환 처리](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/tools/research/visit_reader.py#L47-L95)

웹 출처는 방문 성공 순서대로 번호가 붙고 URL별로 중복을 제거합니다. 최종 인용 처리 함수는 모델이 직접 쓴 References 구역을 제거하고, 캐시 범위를 벗어난 `[N]` 번호를 걸러낸 뒤 실제 인용 목록으로 References를 다시 붙입니다. 이 함수가 확인하는 것은 번호와 목록의 정합성입니다. 특정 문장이 해당 페이지에서 논리적으로 뒷받침되는지 판정하는 entailment 검증기는 아닙니다. [인용 캐시](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/tools/research/cache.py#L54-L73), [최종 인용 정리](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/runtime/citations.py#L42-L96)

### 8. 근거 재검토와 결과 출력에도 구분이 있습니다

기본 research 모드에서는 도구를 사용한 비어 있지 않은 정상 답변에 한해 주 모델을 한 번 더 호출합니다. 기존 대화에 들어 있는 출처를 기준으로 주장을 수정하라는 프롬프트를 주되, 이 재검토 호출에는 도구를 제공하지 않습니다. 재검토가 예외나 빈 결과로 끝나면 초안을 유지합니다. 이는 별도 심판 모델이나 새 자료 조사를 통한 독립 검증이 아니라, 같은 모델의 문맥 기반 재작성입니다. [재작성 호출](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/runtime/agent.py#L233-L271), [적용 조건](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/runtime/agent.py#L400-L413)

정상 답변의 이벤트 순서도 확인할 수 있습니다. `answer` 이벤트는 인용 finalizer 이전의 `prediction`을 전달하고, 최종 `trajectory.prediction`에는 인용 후처리가 반영됩니다. SSE 서비스는 에이전트 내부의 단순 `done` 이벤트를 버리고, 연구 실행이 반환된 뒤 전체 trajectory를 담은 프로토콜 `done`을 보냅니다. 따라서 클라이언트가 최종 보고서를 확정하려면 중간 텍스트뿐 아니라 마지막 trajectory를 기준으로 삼아야 합니다. [answer와 finalizer 순서](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/runtime/agent.py#L409-L448), [SSE 최종 결과](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/service/app.py#L193-L233)

CLI는 최종 `prediction`을 표준출력에, 진행 상황과 종료 요약을 표준오류에 씁니다. `--save`를 지정하면 전체 trajectory를 JSON으로 저장하며, 프로세스 반환값은 `termination == "answer"` 여부에 따라 달라집니다. 이 구조 덕분에 사람이 읽는 보고서와 사후 확인용 실행 기록을 분리해서 받을 수 있습니다. [CLI 출력](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/cli.py#L45-L65), [JSON 저장](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/research.py#L106-L111)

### 9. 스킬은 실행 그래프보다 모델이 읽는 작업 절차에 가깝습니다

스킬은 `SKILL.md`의 메타데이터와 본문으로 구성됩니다. 이름·설명·태그·`requires_tools`를 파싱하고, `load_skill`은 본문을 모델에게 반환하면서 필요한 도구 스키마를 함께 공개합니다. DCF 스킬의 단계가 적혀 있다고 해서 런타임이 각 단계를 강제 순서로 실행하는 것은 아닙니다. 실제 도구 선택은 계속 모델과 에이전트 루프를 통해 이루어집니다. [스킬 파싱](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/runtime/skill_registry.py#L49-L85), [본문 반환과 도구 공개](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/tools/core/load_skill.py#L47-L76)

검색 순서는 번들 스킬, 현재 작업 디렉터리의 `skills/`, `FH_SKILLS_DIR`이며 뒤에서 읽은 같은 이름의 스킬이 앞의 것을 덮어씁니다. 잘못된 사용자 스킬은 건너뛰지만 번들 스킬은 엄격하게 읽습니다. “코드 없이 확장”은 기존 도구들을 이용하는 작업 절차를 바꿀 수 있다는 뜻입니다. 새로운 외부 API나 계산 handler 자체가 Markdown만으로 생기는 것은 아닙니다. [스킬 발견 순서](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/tools/research/assembly.py#L91-L118), [엄격·비엄격 로딩](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/runtime/skill_registry.py#L122-L154)

## 설치와 사용: README가 제공하는 경로

다음 명령은 분석 커밋의 README에 있는 사용법을 발췌한 것입니다. 이 리뷰에서 설치·호출을 실행하지 않았고, 모델 계정·서버와 외부 데이터 접근이 준비되어 있다는 전제가 있습니다. Python 요구 버전은 3.12 이상이며, README는 `uv`를 설치 도구로 사용합니다. [설치 안내](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/README.md#L43-L63), [매니페스트](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/pyproject.toml#L1-L20)

```bash
git clone https://github.com/Yijia-Xiao/FinanceHarness.git
cd FinanceHarness
uv tool install .
```

소스 체크아웃에서는 README의 `uv sync`, `uv run python main.py ...` 또는 `uv run fh ...` 경로도 제시됩니다. 위 clone 명령은 기본 브랜치를 받으므로, 이후 저장소가 바뀌면 이 글의 분석 SHA와 다른 소스가 될 수 있습니다.

프로필은 `--profile` 또는 `FH_PROFILE`로 선택합니다. README의 클라우드 설정 변수는 `GEMINI_API_KEY`, `OPENAI_API_KEY`이며, 자체 제공하는 Qwen 경로에는 `FH_QWEN_BASE_URL`과 `FH_QWEN_READER_BASE_URL`이 나옵니다. 이 이름들은 해당 커밋의 구성 방법을 설명하는 것으로, 문서에 기재된 모델 ID가 현재 계정에서 사용 가능한지를 확인한 것은 아닙니다. [README 프로필 설정](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/README.md#L65-L87)

아래는 README의 실행 예에서 필요한 줄을 발췌했습니다. 첫 줄의 질문은 문서에 실린 입력 예시입니다. [실행 예](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/README.md#L89-L104), [서비스 실행](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/README.md#L153-L160)

```bash
fh -p "Apple's competitive position in 2026?" --mode research
fh -p "..." --profile gpt --save run.json
fh --list
fh serve
```

`--list`는 등록된 프로필과 스킬을 출력합니다. 실제 구현에서는 네트워크 요청으로 API 키나 도구의 성공을 검사하지 않으므로, 이 출력만으로 전체 설치·외부 서비스 연결이 정상이라고 판정할 수는 없습니다. [목록 출력 구현](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/cli.py#L98-L113)

## 한계와 읽을 때 주의할 점

README의 설명을 구현과 함께 읽으면 다음 경계가 드러납니다.

| 문서의 강조점 | 코드에서 확인되는 기능 | 이를 넘어서는 보장 |
|---|---|---|
| 필요할 때 도구를 공개합니다. | 상세 스키마를 실행 중 추가합니다. | 카탈로그 비용이 0이거나 도구 실행 권한을 제한한다는 보장은 아닙니다. |
| 앞선 결과를 참조해 계산합니다. | 실행 내 `structured` 객체를 직접 치환합니다. | 날짜 정렬·통화·가정의 경제적 타당성을 자동 판정하지 않습니다. |
| 근거가 있는 보고서를 만듭니다. | 방문 URL, 인용 번호 정리, 선택적 모델 재검토가 있습니다. | 보고서의 모든 수치와 문장이 실제 근거와 일치한다는 독립 검증은 아닙니다. |
| 실행 한도가 있습니다. | 루프 시작에서 시간·횟수를 검사하고 주 모델 호출에 timeout을 둡니다. | 전체 실행의 모든 비동기 작업에 같은 엄격한 마감 시각이 적용되는 것은 아닙니다. |

앞의 세 항목은 본문에서 추적한 공개 스키마·참조·인용 코드에 대응합니다. 마지막 항목은 [주 모델 호출 timeout](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/runtime/agent.py#L181-L185), [루프 시작 검사](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/runtime/agent.py#L329-L335), [별도 재검토 호출](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/runtime/agent.py#L246-L251)의 차이에서 확인할 수 있습니다. 설정의 `max_rounds`는 100, 실행 시간 기준값은 3,600초이지만 이는 분석 커밋의 기본값이며 성능 측정값이 아닙니다. 재시도와 재검토까지 포함한 실제 소요 시간은 이 글에서 측정하지 않았습니다. [기본 설정](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/runtime/config.py#L42-L50)

문맥 압축도 별도로 이해해야 합니다. 모델 호출 복구 경로의 `compact_messages()`는 오래된 도구 메시지 본문을 생략 표식으로 바꾸고 최근 일부 결과를 유지합니다. 전체 실행 상태의 구조화 결과를 삭제하는 함수는 아닙니다. 반대로 모델이 오래된 텍스트를 그대로 다시 볼 수 있게 하는 것도 아닙니다. 원래 메시지 배열을 직접 변경하지 않고 다음 호출에 사용할 복사본을 만드는 구현입니다. [문맥 축소](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/runtime/recovery.py#L114-L148), [모델 호출의 작업 메시지](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/financeharness/runtime/agent.py#L163-L180)

저장소의 `LICENSE`는 Apache License 2.0입니다. 이 확인은 저장소 코드에 포함된 라이선스 파일에 대한 것이며, 연결하는 모델 서비스나 금융·웹 데이터의 이용 조건까지 이 파일이 정한다는 의미는 아닙니다. [LICENSE](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/LICENSE#L1-L5)

README는 FinanceGym 벤치마크가 별도 저장소에서 관리된다고 안내합니다. 이 글은 그 평가 파이프라인이나 연결 논문의 결과를 분석하지 않았으므로 성능 점수·순위·모델 간 우열을 인용하지 않습니다. [벤치마크 안내](https://github.com/Yijia-Xiao/FinanceHarness/blob/1163c5e7a8f35ff6217c3a480f7b04562355e0cc/README.md#L162-L165)

## 이 글에서 다루지 못한 부분

핵심 실행 경로와 대표 데이터·계산 도구에 집중했습니다. `clarify.py`의 질문 구체화 전략, `runtime/summarize.py`의 장기 세션 요약, 각 provider의 스트리밍 변환 세부, 재무·시장 데이터 도구 전체의 필드 정의, WACC·VaR·beta·DCF 민감도 도구의 모든 계산 조건은 상세 감사하지 않았습니다. HTTP의 인증·동시 세션 변경·배포 운영과 실제 외부 서비스 오류도 실행 검증 범위에 포함되지 않습니다. 이 범위 고지는 해당 기능이 없다는 뜻이 아니라, 본문의 결론을 적용할 수 있는 분석 경계를 명시한 것입니다.

## 마치며

FinanceHarness에서 배울 핵심은 금융이라는 주제 자체보다 **자연어로 선택한 작업을 검증 가능한 도구 호출과 재사용 가능한 데이터로 연결하는 방식**입니다. 모델은 카탈로그와 스킬을 읽어 다음 작업을 선택하고, 런타임은 인수 변환·참조 치환·입력 검증을 수행하며, 도구는 설명용 텍스트와 계산용 객체를 나누어 반환합니다. 웹 출처 목록과 최종 보고서 역시 별도의 후처리 경로를 가집니다.

이 분리는 수치를 다시 생성하는 부담을 줄이고 실행 과정을 들여다볼 발판을 제공합니다. 동시에 도구가 계산을 수행했다는 사실, 데이터의 의미가 맞다는 사실, 보고서의 주장이 근거에 부합한다는 사실은 각각 따로 확인해야 합니다. 이 저장소의 구조를 이해하는 데 가장 중요한 지점도 바로 그 책임 경계입니다.
