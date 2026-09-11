---
type: "Repo Review"
title: "[Repo Review] Hermes Agent: 도구 실행과 기억을 연결하는 에이전트 런타임"
description: "Hermes Agent의 대화 루프, 실행 전 영속화, 충돌을 고려한 도구 병렬 처리, 세션·메모리·스킬의 분리를 코드로 살펴봅니다."
date: "2026-09-11"
tags:
  - "AI Agent"
  - "Python"
  - "Tools"
resource: "https://github.com/nousresearch/hermes-agent/tree/cbd03e6e4ca143c1d5c2db881320afb85783c30b"
generated:
  by: "process:blog-review"
  at: "2026-09-11T18:46:01+09:00"
sources:
  - id: "nousresearch/hermes-agent"
    resource: "https://github.com/nousresearch/hermes-agent/tree/cbd03e6e4ca143c1d5c2db881320afb85783c30b"
    title: "nousresearch/hermes-agent"
status: "stable"
year: "2026"
analyzed_at: "2026-09-11T18:38:00+09:00"
source_id: "nousresearch/hermes-agent"
source_revision: "cbd03e6e4ca143c1d5c2db881320afb85783c30b"
source_type: "repo"
source_url: "https://github.com/nousresearch/hermes-agent/tree/cbd03e6e4ca143c1d5c2db881320afb85783c30b"
visual_sources:
  - path: "/img/reviews/2026/hermes-agent-review/agent-flow.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/nousresearch/hermes-agent/blob/cbd03e6e4ca143c1d5c2db881320afb85783c30b/agent/conversation_loop.py#L1514-L1565"
    caption: "리뷰어 작성, 분석 커밋 기준. 일반 대화 루프의 도구 왕복과 조건부 기억 검토 경로를 요약합니다."
---

## 들어가며: 답변 이후에도 남아야 하는 것

도구를 호출하는 AI 에이전트는 하나의 질문에도 여러 번 모델과 통신합니다. 파일을 읽고, 명령을 실행하고, 결과를 다시 모델에 전달하는 동안 대화 기록은 계속 늘어납니다. 프로세스가 중단되었을 때 어디까지 실행했는지 남아 있어야 하고, 다음 대화에서는 이전에 익힌 작업 절차를 다시 활용할 수 있어야 합니다.

Nous Research의 Hermes Agent는 이러한 실행과 기억을 함께 다루는 에이전트 런타임입니다. README는 경험에서 스킬을 만들고 사용 중 개선하는 “self-improving” 에이전트라고 소개합니다. 이 글에서는 그 표현을 성능 향상의 증거로 받아들이기보다, **어떤 실행 기록을 저장하며 어떤 조건에서 지식을 다시 검토하는지** 구현으로 확인합니다. [README의 프로젝트 소개](https://github.com/nousresearch/hermes-agent/blob/cbd03e6e4ca143c1d5c2db881320afb85783c30b/README.md#L19-L26)

분석 대상은 커밋 `cbd03e6e4ca143c1d5c2db881320afb85783c30b`입니다. 아래 설명은 소스와 문서의 정적 분석이며 대상 레포의 설치·빌드·테스트·모델 호출은 수행하지 않았습니다.

## Hermes Agent는 무엇인가

한 문장으로 정의하면, **언어 모델의 도구 호출을 실행하고 그 대화와 재사용 지식을 유지하면서 CLI와 메시징 인터페이스에 연결하는 Python 기반 런타임**입니다. 패키지 매니페스트에는 `hermes-agent` 버전 `0.21.1`, Python `>=3.11,<3.14`, CLI 진입점 `hermes_cli.main:main`이 명시되어 있습니다. [패키지 정의](https://github.com/nousresearch/hermes-agent/blob/cbd03e6e4ca143c1d5c2db881320afb85783c30b/pyproject.toml#L3-L18), [CLI 등록](https://github.com/nousresearch/hermes-agent/blob/cbd03e6e4ca143c1d5c2db881320afb85783c30b/pyproject.toml#L391-L392)

이 글에서 중점적으로 확인할 기능은 대화 루프, 도구 실행, 세션 저장, 메모리와 스킬입니다. README에 열거된 Telegram·Discord 등 메시징 연결과 외부 메모리 제공자 연동도 프로젝트의 일부지만, 모든 플랫폼의 동작을 검증한 것은 아닙니다. [공식 사용 명령](https://github.com/nousresearch/hermes-agent/blob/cbd03e6e4ca143c1d5c2db881320afb85783c30b/README.md#L104-L117)

## 아키텍처: 한 요청을 처리하는 여러 책임

핵심 클래스인 `AIAgent`는 모든 기능을 한 클래스 본문에 구현하지 않습니다. 세션 저장, 압축, 턴 처리 등의 mixin을 조합하고 별도 모듈에 실제 처리를 위임합니다. 따라서 `run_agent.py`만 읽으면 대화가 어떻게 완료되는지 놓치기 쉽습니다. [클래스 구성](https://github.com/nousresearch/hermes-agent/blob/cbd03e6e4ca143c1d5c2db881320afb85783c30b/run_agent.py#L211-L216)

| 경로 | 핵심 책임 |
|---|---|
| `hermes_cli/main.py`, `cli.py` | 설정을 정리하고 사용자 입력을 대화 실행기로 전달합니다. |
| `agent/turn_facade.py` | 턴 진입과 세션 실행 권한의 수명주기를 관리합니다. |
| `agent/conversation_loop.py` | 요청 준비, API 호출, 도구 또는 텍스트 응답 분기, 종료 처리를 연결합니다. |
| `agent/turn_tool_round.py`, `agent/tool_executor.py` | 도구 호출 기록을 저장하고 실제 실행 및 결과 반영을 수행합니다. |
| `model_tools.py`, `tools/registry.py` | 도구 이름과 등록된 스키마·handler를 연결합니다. |
| `agent/session_persistence.py`, `hermes_state.py` | 대화 기록을 SQLite에 저장하고 세션 상태를 유지합니다. |
| `agent/memory_manager.py`, `agent/turn_finalizer.py` | 메모리 제공자 동기화와 조건부 사후 검토를 연결합니다. |

아래 도식은 일반 대화 루프의 핵심 경로를 요약한 것입니다. 실제 코드는 재시도, 중단, 압축 실패, 별도 전송 모드 등 더 많은 분기를 포함합니다.

[![Hermes Agent의 입력부터 모델 호출, 도구 실행, SQLite 기록, 최종 응답과 조건부 기억 검토까지의 흐름]({{ '/img/reviews/2026/hermes-agent-review/agent-flow.svg' | relative_url }})]({{ '/img/reviews/2026/hermes-agent-review/agent-flow.svg' | relative_url }})

*그림 1. 리뷰어 작성, 분석 커밋 기준. 실선은 일반 처리 흐름, 점선은 조건부 사후 검토입니다. 도구 호출은 실행 전에 기록되고 결과가 다시 대화 루프로 들어갑니다. [대화 루프](https://github.com/nousresearch/hermes-agent/blob/cbd03e6e4ca143c1d5c2db881320afb85783c30b/agent/conversation_loop.py#L1514-L1565), [도구 실행 전 저장](https://github.com/nousresearch/hermes-agent/blob/cbd03e6e4ca143c1d5c2db881320afb85783c30b/agent/turn_tool_round.py#L99-L158), [사후 검토 조건](https://github.com/nousresearch/hermes-agent/blob/cbd03e6e4ca143c1d5c2db881320afb85783c30b/agent/turn_finalizer.py#L594-L623)을 바탕으로 구성했습니다. 이미지를 클릭하면 확대할 수 있습니다.*

## 작동 원리: 입력에서 최종 출력까지

### 1. CLI 입력은 설정과 세션 처리를 거쳐 들어갑니다

`hermes` 명령의 채팅 처리 함수 `cmd_chat()`는 안전 모드와 사용자 설정 처리, 세션 인수 해석, 제공자 설정 확인을 수행합니다. TUI 사용 여부에 따라 경로가 나뉘며, 일반 CLI 경로는 모델·추론·도구 집합·질의 등의 인수를 모아 `cli.main()`을 호출합니다. 따라서 모델에 보낼 사용자 문장만 준비하는 것이 아니라, **그 문장을 어느 세션과 어떤 실행 설정 아래에서 처리할지** 먼저 결정합니다. [채팅 진입 처리](https://github.com/nousresearch/hermes-agent/blob/cbd03e6e4ca143c1d5c2db881320afb85783c30b/hermes_cli/main.py#L1688-L1757)

입출력 계약을 간결하게 볼 수 있는 예는 quiet 단일 질의 경로입니다. `_run_quiet_single_query()`는 `user_message`와 `conversation_history`를 `agent.run_conversation()`에 전달하고 결과 딕셔너리의 `final_response`를 출력합니다. 세션 ID는 별도로 동기화하고 표준 오류에 기록합니다. 본문 응답과 운영용 식별자를 다른 출력 채널에 두는 구조입니다. 이는 단일 질의 경로에 대한 설명이며 모든 UI가 동일한 출력 방식을 쓴다는 뜻은 아닙니다. [단일 질의 입출력](https://github.com/nousresearch/hermes-agent/blob/cbd03e6e4ca143c1d5c2db881320afb85783c30b/cli.py#L4063-L4109)

`run_conversation()`의 바깥 계층인 `TurnFacadeMixin`은 바로 모델을 호출하지 않습니다. 기존 background review와 조율하고, `admit_durable_turn_lease()`로 턴 실행을 허용할지 판단합니다. 조기 반환 결과가 있으면 루프에 들어가지 않으며, 허용된 경우에는 반환된 대화 이력을 사용합니다. 여러 실행 경로가 같은 세션을 건드릴 수 있는 시스템에서 세션 실행 권한을 별도 책임으로 둔 것입니다. [턴 진입과 lease 처리](https://github.com/nousresearch/hermes-agent/blob/cbd03e6e4ca143c1d5c2db881320afb85783c30b/agent/turn_facade.py#L22-L100)

### 2. 대화 루프는 여러 처리 단계가 반환하는 행동으로 진행됩니다

일반 루프는 반복 횟수와 공유 iteration budget을 검사하면서 진행됩니다. 한 반복은 시작 처리 → 입력 준비 → API 요청 조립 → 사전 검사 → API 호출과 재시도 → 응답 정규화로 이어집니다. 각 단계는 `continue`, `break`, `return` 등의 행동을 반환하여 다음 단계를 결정합니다. 이 구조에서는 “모델을 한 번 호출했다”와 “사용자의 한 턴이 끝났다”가 다릅니다. 한 턴 안에서 도구 왕복과 재시도로 여러 모델 요청이 발생할 수 있습니다. [반복과 단계 제어](https://github.com/nousresearch/hermes-agent/blob/cbd03e6e4ca143c1d5c2db881320afb85783c30b/agent/conversation_loop.py#L1514-L1565)

도구 응답과 일반 텍스트 응답을 구분하는 실제 코드는 다음과 같습니다.

```python
_v = _run_phase(
    run_tool_round if s.assistant_message.tool_calls else finish_text_response, agent, s
)
```

[원문 코드](https://github.com/nousresearch/hermes-agent/blob/cbd03e6e4ca143c1d5c2db881320afb85783c30b/agent/conversation_loop.py#L1548-L1550)

모델 응답에 `tool_calls`가 있으면 도구 라운드로 넘어가고, 없으면 텍스트 종료 처리로 이동합니다. 이후에도 해당 단계의 반환 행동을 검사하므로, 텍스트를 받았다는 이유만으로 항상 즉시 성공 종료하는 것은 아닙니다.

또한 이 설명은 모든 실행 모드를 포괄하지 않습니다. `api_mode == "codex_app_server"`일 때는 일반 루프에 들어가기 전에 별도 턴 실행기로 위임하는 분기가 있습니다. 현재 글은 그 별도 런타임의 내부 동작을 분석하지 않습니다. [별도 실행 모드 분기](https://github.com/nousresearch/hermes-agent/blob/cbd03e6e4ca143c1d5c2db881320afb85783c30b/agent/conversation_loop.py#L1505-L1512)

### 3. 도구는 실행하기 전에 호출 기록부터 남깁니다

`run_tool_round()`에서 가장 주목할 부분은 **persist-before-execute**, 즉 실행 전 영속화입니다. 도구 호출을 검증하고 assistant 메시지를 대화 목록에 추가한 다음, SQLite 저장을 시도합니다. 저장이 실패하면 턴을 실패 상태로 종료하며 도구 실행 단계로 넘어가지 않습니다. 중간 설명을 UI에 내보내는 일도 이 저장 이후입니다. [도구 라운드의 순서](https://github.com/nousresearch/hermes-agent/blob/cbd03e6e4ca143c1d5c2db881320afb85783c30b/agent/turn_tool_round.py#L45-L158)

왜 이 순서가 필요할까요? 도구가 프로세스를 재시작하거나 외부 상태를 바꾼 직후 실행기가 종료되면, 메모리에만 있던 호출 기록은 사라질 수 있습니다. 호출 의도를 먼저 남기면 재개 시점에 어떤 도구 호출이 요청되었는지 확인할 기반이 생깁니다. 다만 이 순서만으로 외부 도구의 부작용과 SQLite 쓰기가 하나의 트랜잭션이 되지는 않습니다. 따라서 **모든 도구가 정확히 한 번 실행된다고 보장하는 구조로 해석해서는 안 됩니다**. 후자는 서로 다른 저장·실행 경계를 읽고 내린 리뷰어의 판단입니다.

도구 결과를 처리할 때도 영속화가 중요합니다. `_flush_session_db_after_tool_progress()`는 다음 모델 요청이 볼 체크포인트 내용을 먼저 구성한 뒤 저장하고, 실패하면 `_incremental_persistence_failed`를 표시합니다. 도구 라운드는 이 상태를 확인해 메모리에만 있는 결과를 다음 모델 호출로 전달하지 않도록 종료합니다. [도구 진행 저장](https://github.com/nousresearch/hermes-agent/blob/cbd03e6e4ca143c1d5c2db881320afb85783c30b/agent/tool_executor.py#L173-L192), [실패 후 종료](https://github.com/nousresearch/hermes-agent/blob/cbd03e6e4ca143c1d5c2db881320afb85783c30b/agent/turn_tool_round.py#L152-L160)

### 4. 도구 병렬 처리는 경로 충돌과 실행 순서를 고려합니다

모델이 여러 도구를 한 번에 요청했다고 해서 전부 동시에 실행되지는 않습니다. `AIAgent._execute_tool_calls()`는 호출이 하나이면 순차 실행하고, 여러 개이면 실행 디렉터리를 전달해 `_plan_tool_batch_segments()`가 구성한 구간을 사용합니다. 구간은 병렬 또는 순차 실행으로 구분됩니다. [실행기 선택](https://github.com/nousresearch/hermes-agent/blob/cbd03e6e4ca143c1d5c2db881320afb85783c30b/run_agent.py#L1273-L1296)

구간 계획기는 호출 순서를 순회하며 병렬 실행이 허용된 호출과 예약된 경로를 누적합니다. 읽기끼리 경로가 겹치는 것은 허용하지만, 겹치는 경로 중 어느 한쪽이 쓰기이면 현재 병렬 구간을 닫습니다. 병렬 허용 대상이 아닌 호출은 순차 구간을 형성하고, 호출이 하나만 남은 병렬 구간도 순차 실행으로 내립니다. [구간 구성 알고리즘](https://github.com/nousresearch/hermes-agent/blob/cbd03e6e4ca143c1d5c2db881320afb85783c30b/agent/tool_dispatch_helpers.py#L164-L210)

예를 들어 독립적인 파일 읽기는 함께 처리할 여지가 있지만, 같은 파일의 수정과 읽기는 쓰기 충돌을 고려해야 합니다. 이 예는 코드의 경로 예약 조건을 설명한 것이며 실제 수행한 실행 결과는 아닙니다. 이 설계의 기술적 가치는 단순히 스레드 수를 늘리는 데 있지 않고, **병렬 실행을 허용할 조건과 순서 경계를 분리했다는 점**에 있습니다. 다만 파일 경로 예약이 외부 서비스 내부의 모든 공유 상태까지 파악해 준다는 보장은 없습니다.

### 5. 도구 이름은 실행 문맥과 함께 handler로 전달됩니다

도구 실행 경로에는 일반 레지스트리 디스패치와 에이전트 수준의 특수 실행기가 함께 존재합니다. `invoke_tool()`는 도구 요청 middleware, 실행 전 차단 판단, inline executor 선택을 수행하고, 일반 경로에서는 `model_tools.handle_function_call()`을 호출합니다. 여기에는 task·session·turn·API request ID와 활성 도구 목록 등이 전달됩니다. [공통 도구 호출 경로](https://github.com/nousresearch/hermes-agent/blob/cbd03e6e4ca143c1d5c2db881320afb85783c30b/agent/agent_runtime_helpers.py#L2226-L2308)

`model_tools`의 실행 단계에서는 connector 이름을 별도 처리하고 나머지를 `registry.dispatch()`로 보냅니다. 레지스트리 자체는 도구의 스키마, handler, toolset 소속과 가용성 확인 함수를 모으는 구조입니다. 따라서 도구를 추가하는 일은 이름에 대응하는 함수만 만드는 것이 아니라, 모델에 노출할 스키마와 실행 가능 조건을 함께 정의하는 일입니다. [레지스트리 실행 분기](https://github.com/nousresearch/hermes-agent/blob/cbd03e6e4ca143c1d5c2db881320afb85783c30b/model_tools.py#L813-L835), [레지스트리와 내장 도구 발견](https://github.com/nousresearch/hermes-agent/blob/cbd03e6e4ca143c1d5c2db881320afb85783c30b/tools/registry.py#L1-L4)

순차 실행에는 표시 처리를 위한 자체 inline 호출 경로도 있으므로, 모든 도구가 반드시 `invoke_tool()` 하나만 통과한다고 단순화하면 안 됩니다. 위 함수의 설명도 concurrent 경로와 sequential 경로의 차이를 명시합니다. 전체 설계에서 공통으로 중요한 것은 도구 실행의 문맥, 차단 여부, 결과가 다시 대화 기록에 연결되는 방식입니다.

### 6. 세션 저장과 컨텍스트 압축은 서로 다른 문제를 풉니다

세션 저장은 “무슨 일이 있었는가”를 남기고, 컨텍스트 압축은 “다음 모델 요청에 무엇을 담을 수 있는가”를 다룹니다. `SessionDB`는 SQLite와 FTS5 검색을 사용하며 WAL 모드의 다중 읽기·단일 쓰기 구조를 설명합니다. 반면 모델 요청 전에는 요청 토큰 압력을 기준으로 압축 필요 여부를 판단하는 별도 사전 검사 계층이 있습니다. [SessionDB 정의](https://github.com/nousresearch/hermes-agent/blob/cbd03e6e4ca143c1d5c2db881320afb85783c30b/hermes_state.py#L335-L341), [압축 진입 조건](https://github.com/nousresearch/hermes-agent/blob/cbd03e6e4ca143c1d5c2db881320afb85783c30b/agent/turn_preflight.py#L85-L115)

압축은 매 반복마다 무조건 실행되지 않습니다. 활성화 여부, 메시지 수, 시도 횟수, 실패 후 대기 상태, 압축기가 판단한 임계값을 함께 검사합니다. 관리되는 특정 로컬 모델 경로에서는 압축 전에 컨텍스트 창을 늘릴 수 있는지도 확인합니다. 이를 모든 모델에 적용되는 자동 확장 기능으로 일반화할 수는 없습니다.

저장 계층은 단순히 리스트의 마지막 인덱스만 기억하지 않습니다. 메시지 딕셔너리의 영속화 마커를 활용해 이미 저장한 항목을 구분합니다. 메시지 순서가 복구 과정에서 바뀌거나 압축 후 세션이 전환되면 위치 기반 중복 방지가 흔들릴 수 있기 때문입니다. 코드에는 압축으로 닫힌 세션의 활성 후속 세션을 채택하여 한 번 재시도하는 경로도 있습니다. [증분 저장과 중복 방지](https://github.com/nousresearch/hermes-agent/blob/cbd03e6e4ca143c1d5c2db881320afb85783c30b/agent/session_persistence.py#L295-L355)

### 7. 종료 응답과 기억 검토는 분리되어 있습니다

루프 종료 시 `finalize_turn()`은 마지막 응답을 정리하고 세션 저장을 시도하며, `final_response`를 포함한 결과 딕셔너리를 만듭니다. UI나 CLI는 이 결과를 사용합니다. 외부 메모리 제공자에는 완료된 턴을 동기화하고, 별도의 조건이 맞으면 background review를 시작합니다. [종료 저장과 응답 구성](https://github.com/nousresearch/hermes-agent/blob/cbd03e6e4ca143c1d5c2db881320afb85783c30b/agent/turn_finalizer.py#L476-L549), [메모리 동기화와 검토 분기](https://github.com/nousresearch/hermes-agent/blob/cbd03e6e4ca143c1d5c2db881320afb85783c30b/agent/turn_finalizer.py#L594-L623)

스킬 검토 조건은 구체적입니다. 스킬 알림 간격이 양수이고 누적 반복 수가 간격에 도달했으며 `skill_manage` 도구가 활성화되어야 합니다. 사후 검토 자체도 최종 응답이 있고, 중단되지 않았으며, `skip_background_review`가 꺼져 있고, 메모리 또는 스킬 검토 필요 조건이 참일 때 실행합니다. 따라서 README의 자기 개선을 “매 요청 후 항상 새 스킬을 생성한다”로 읽으면 구현과 맞지 않습니다.

이때 서로 다른 기억을 구분하면 구조가 더 명확해집니다.

| 저장 대상 | 역할 | 확인한 근거 |
|---|---|---|
| 세션 기록 | 사용자·assistant·도구 사이에서 실제로 오간 대화를 남깁니다. | `SessionDB`, 증분 flush |
| 메모리와 사용자 정보 | 장기적으로 유지할 요약된 지식과 사용자 정보를 다룹니다. | `MEMORY.md`, `USER.md` 구분 |
| 스킬 | 재사용할 절차와 작업 방법을 문서로 저장합니다. | `SKILL.md`, `skill_manage` |

메모리 도구는 `MEMORY.md`와 `USER.md`를 구분하고, 스킬 관리 도구는 `SKILL.md`와 보조 자료 디렉터리 구조를 사용합니다. 프롬프트 지침도 재사용할 작업 절차를 스킬로 기록하도록 안내합니다. 이는 가중치 학습을 확인한 것이 아니라 **외부에 저장한 지식과 절차를 이후 모델 입력과 도구 사용에 연결하는 방식**을 확인한 것입니다. 이 저장 구조가 실제 작업 성공률을 얼마나 높이는지는 이 정적 분석으로 측정하지 않았습니다. [메모리 도구](https://github.com/nousresearch/hermes-agent/blob/cbd03e6e4ca143c1d5c2db881320afb85783c30b/tools/memory_tool.py#L1-L4), [스킬 저장 구조](https://github.com/nousresearch/hermes-agent/blob/cbd03e6e4ca143c1d5c2db881320afb85783c30b/tools/skill_manager_tool.py#L1-L8), [스킬 기록 지침](https://github.com/nousresearch/hermes-agent/blob/cbd03e6e4ca143c1d5c2db881320afb85783c30b/agent/prompt_builder.py#L225-L232)

## 문서에 따른 설치와 사용

고정 커밋의 README는 다음 설치 명령을 제공합니다. 아래는 문서 인용이며, 이 리뷰에서 내려받거나 실행하지 않았습니다. 또한 명령이 가져오는 원격 설치 스크립트의 내용은 이 글의 분석 커밋에 고정되어 있지 않습니다. [README 설치 안내](https://github.com/nousresearch/hermes-agent/blob/cbd03e6e4ca143c1d5c2db881320afb85783c30b/README.md#L35-L41)

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

설정과 사용을 위한 명령 중 핵심 항목은 다음과 같습니다. 모두 같은 README의 Getting Started에서 발췌했습니다. [명령 목록](https://github.com/nousresearch/hermes-agent/blob/cbd03e6e4ca143c1d5c2db881320afb85783c30b/README.md#L104-L117)

```bash
hermes setup
hermes model
hermes tools
hermes
hermes gateway
hermes doctor
```

`setup`은 설정 마법사, `model`은 모델과 제공자 선택, `tools`는 도구 활성화 설정, 기본 `hermes`는 대화 시작에 대응합니다. `gateway`는 메시징 게이트웨이를 시작하고 `doctor`는 문제 진단용입니다. 실제 인증 방식과 연결 가능 여부는 선택한 제공자와 실행 환경에 따라 확인해야 하며, 위 명령만으로 모든 외부 연동이 준비되었다고 볼 수는 없습니다.

## 한계와 주의점

**영속화 경계가 존재해도 외부 부작용까지 원자적이지는 않습니다.** 실행 전에 호출을 저장하고 실행 후 결과를 저장하는 설계는 복구 근거를 제공합니다. 그러나 파일·프로세스·외부 서비스의 변경과 세션 DB 쓰기는 별개의 작업입니다. 이 글에서 확인한 저장 순서는 exactly-once 실행이나 모든 중단 상황의 자동 복구를 입증하지 않습니다.

**도구 권한 설정은 실행 결과에 직접 영향을 줍니다.** CLI에는 `--yolo`를 통해 위험 명령 승인을 우회하도록 환경 변수를 설정하는 코드가 있습니다. 또 `--ignore-rules`는 컨텍스트 파일과 메모리 등의 주입을 건너뛰도록 연결됩니다. 따라서 같은 사용자 질문이라도 실행 플래그와 도구 집합이 다르면 실제 행동 조건이 달라집니다. [CLI 플래그 처리](https://github.com/nousresearch/hermes-agent/blob/cbd03e6e4ca143c1d5c2db881320afb85783c30b/hermes_cli/main.py#L1709-L1721)

**자기 개선의 효과는 별도 평가가 필요합니다.** 조건부 검토와 스킬 저장 기능의 존재는 확인했지만, 생성된 스킬의 정확성이나 여러 세션에 걸친 성공률 향상까지 확인한 것은 아닙니다. background review와 압축에는 추가 모델 작업이 연결될 수 있으므로 사용자에게 보이는 최종 답변만으로 내부 처리량을 설명할 수도 없습니다. 이 글에서는 비용이나 속도 수치를 추정하지 않습니다.

라이선스는 MIT입니다. 재배포 시 저작권 및 허가 고지를 유지해야 하며 소프트웨어는 보증 없이 제공됩니다. [LICENSE](https://github.com/nousresearch/hermes-agent/blob/cbd03e6e4ca143c1d5c2db881320afb85783c30b/LICENSE#L1-L21)

## 이 글에서 다루지 못한 부분

Telegram·Discord 등 개별 gateway adapter, cron과 Kanban 작업 관리, 위임 에이전트의 전체 수명주기, 각 LLM 제공자와 별도 전송 모드, 외부 메모리 제공자의 내부 검색 품질, 모든 도구의 승인·격리 구현은 상세 분석에서 제외했습니다. 메모리 관리자와 압축은 대화 루프와 연결되는 경계 중심으로 읽었으며 모든 provider와 요약 알고리즘을 비교하지 않았습니다. 따라서 이 글은 레포 전체의 보안 감사나 지원 기능의 실행 호환성 보고서가 아닙니다.

## 결론

Hermes Agent에서 눈여겨볼 부분은 모델 호출 자체보다 그 전후의 실행 계약입니다. 세션 단위로 턴 진입을 조율하고, 도구 호출을 실행 전에 기록하며, 경로 충돌을 고려해 병렬 구간을 나누고, 결과를 영속화한 뒤 다음 모델 요청에 반영합니다. 장기 사용에서는 세션 기록·메모리·스킬을 분리하고 조건부 사후 검토로 다시 연결합니다. 이 구조는 에이전트를 단발성 응답 함수보다 지속적인 작업 이력을 가진 실행 시스템으로 이해하는 데 도움이 됩니다.
