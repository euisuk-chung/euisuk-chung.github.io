---
type: "Repo Review"
title: "[Repo Review] Building a Coding Agent From Scratch — decode로 배우는 하네스의 실행 경계"
description: "decode의 모델·도구 루프에서 승인·샌드박스·컨텍스트·결과 회수까지 추적하며, 대화형 실행과 원격 무인 실행의 실제 경계를 살펴봅니다."
date: "2026-10-31"
tags:
  - "Repo Review"
  - "AI Agent"
  - "Python"
  - "Tools"
  - "Prompt Engineering"
resource: "https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/tree/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4"
generated:
  by: "process:blog-review"
  at: "2026-10-31T06:05:24+09:00"
sources:
  - id: "decodingai-coding-agent-course"
    resource: "https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/tree/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4"
    title: "Building a Coding Agent From Scratch"
    author: "Decoding AI"
    last_modified: "2026-10-24T11:43:03+03:00"
status: "stable"
year: "2026"
analyzed_at: "2026-10-31T06:05:24+09:00"
source_id: "decodingai-magazine/building-a-coding-agent-from-scratch-course"
source_revision: "2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4"
source_title: "Building a Coding Agent From Scratch"
source_type: "repo"
source_url: "https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/tree/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4"
visual_sources:
  - path: "img/reviews/2026/coding-agent-course-review/runtime-map.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/agent/factory.py#L46-L73"
    caption: "리뷰어 작성, 분석 커밋 기준: 공통 Agent 구성과 대화형·무인 실행 경로를 구분한 구조도입니다."
  - path: "img/reviews/2026/coding-agent-course-review/approval-flow.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/agent/loop.py#L148-L204"
    caption: "리뷰어 작성, 분석 커밋 기준: 대화형 실행에서 승인 요청과 결과를 이어 붙이는 흐름입니다."
  - path: "img/reviews/2026/coding-agent-course-review/context-boundaries.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/tools/agent.py#L452-L501"
    caption: "리뷰어 작성, 분석 커밋 기준: 부모 대화 이력과 Explore 자식의 독립 실행·보고서 경계를 나타냅니다."
---

## 코딩 에이전트를 만들 때 모델 바깥에서 결정해야 하는 것

“이 저장소의 버그를 고쳐 주세요”라는 요청을 받았다고 생각해 보겠습니다. LLM은 코드를 읽을지, 명령을 실행할지, 파일을 수정할지 제안할 수 있습니다. 하지만 그 제안을 **어느 디렉터리에서 실행하고, 누가 승인하며, 실행 중 들어온 새 요청을 언제 반영하고, 작업 결과를 어떻게 회수할지**는 주변 프로그램이 결정해야 합니다. 이 실행 환경과 제어 장치를 하네스(harness)라고 부를 수 있습니다.

`building-a-coding-agent-from-scratch-course`는 터미널 코딩 에이전트 **decode**를 구현하며 이 문제를 학습하는 공개 강의 저장소입니다. README는 8개 글과 6개 영상으로 구성한 강의라고 소개합니다. 이름의 “from scratch”는 모델을 처음부터 학습한다는 뜻으로 읽기보다는, PydanticAI를 이용해 에이전트 주변 실행 구조를 직접 구성한다는 의미로 이해하는 편이 실제 코드와 맞습니다. 패키지에는 Click CLI, 터미널 UI, 도구, 권한 판단, 샌드박스, 컨텍스트 관리, 원격 실행이 들어 있습니다. [README 소개](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/README.md#L65-L75), [매니페스트](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/pyproject.toml#L5-L45)

이 리뷰는 **2026년 10월 31일, 커밋 `2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4`의 코드를 정적으로 읽은 결과**입니다. 설치·모델 호출·샌드박스 실행·벤치마크는 수행하지 않았습니다. 강의 글과 영상의 개별 내용을 전부 검토한 것은 아니며, 강의 구성은 해당 커밋의 README에 제시된 안내를 기준으로 정리했습니다.

### 강의 순서를 코드의 질문으로 바꾸기

README의 강의 흐름은 작은 에이전트에서 출발해 운영·평가 장치를 붙이는 순서입니다. 학습할 때 각 단원을 다음 질문과 연결하면 코드가 기능 목록으로 흩어지지 않습니다. [강의 목차](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/README.md#L201-L255)

| 단원 | README가 안내하는 주제 | 코드에서 확인할 질문 |
| --- | --- | --- |
| 1 | 전체 시스템 설계 | 모델, 도구, 사용자 입력의 책임은 어디서 갈리는가? |
| 2 | 기본 에이전트 루프와 모델 연결 | 모델 응답이 도구 호출과 최종 답변으로 어떻게 나뉘는가? |
| 3 | 샌드박스 실행 | 명령이 실행되는 파일 트리와 자격 증명은 어디에 있는가? |
| 4 | 메모리·압축·스킬·LSP | 다음 모델 요청에 어떤 정보를 넣고 무엇을 줄이는가? |
| 5 | persona와 병렬 Explore | 자식에게 어떤 도구와 컨텍스트를 넘기는가? |
| 6 | 원격 무인 실행 | 터미널에서 하던 작업을 CLI·webhook·cron에 어떻게 연결하는가? |
| 7 | 벤치마크와 회귀 평가 | 결과 성공과 설계한 행동 준수를 어떻게 구분하는가? |
| 8 | 기록과 재실행 | 실패한 실행을 비교 가능한 자료로 어떻게 남기는가? |

## 전체 구조: 공통 Agent 구성과 두 실행 경로

설치 후 `decode` 명령은 `decode.cli:cli`로 들어갑니다. 하위 명령 없이 실행하면 터미널 UI를 열고, `decode run`이면 한 작업을 수행하는 headless 실행으로 분기합니다. 두 경로 모두 `build_agent()`를 사용하지만, **대화형 턴을 조율하는 코드까지 동일하게 통과하는 것은 아닙니다.** 대화형은 `AgentTurnHandler`와 `Runner`를 구성하고, headless는 `agent.run()`을 직접 호출합니다. [명령 진입점](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/pyproject.toml#L44-L45), [CLI 분기](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/cli.py#L303-L379), [대화형 구성](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/tui/app.py#L852-L882), [headless 호출](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/runtime/headless.py#L212-L267)

![공통 build_agent 아래에서 대화형 Runner와 headless agent.run이 나뉘고 같은 도구와 실행 백엔드를 이용하는 구조]({{ '/img/reviews/2026/coding-agent-course-review/runtime-map.svg' | relative_url }})

*리뷰어 작성, 분석 커밋 기준. 공통 구성은 모델·도구·instructions이고 실행 제어는 두 경로로 나뉩니다. 근거: [factory](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/agent/factory.py#L46-L73), [TUI](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/tui/app.py#L868-L882), [headless](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/runtime/headless.py#L228-L265).*

핵심 디렉터리를 실행 책임별로 읽으면 다음과 같습니다.

| 경로 | 맡은 책임 |
| --- | --- |
| `cli.py`, `tui/app.py` | 설정 사전 확인, 입력 해석, 화면 출력, 사용자 결정 연결 |
| `agent/factory.py`, `agent/loop.py` | Agent 생성, 모델·도구 이벤트 처리, 이력과 승인 재개 |
| `harness/runner.py` | 한 번에 한 턴 실행, steering·follow-up 큐와 중단 경계 |
| `tools/registry.py`, `permissions/` | 노출할 도구 목록과 allow·ask·deny 판단 |
| `sandbox/`, `tools/files.py`, `tools/bash.py` | 파일·명령 실행 위치와 작업 결과 회수 |
| `memory/`, `context/`, `skills/` | 주입할 정보, 대화 압축, 필요할 때 읽는 지침 |
| `runtime/`, `remote/`, `observability/`, `evals/` | 무인 작업, 원격 트리거, 추적과 평가 |

각 책임의 연결은 위의 고정 커밋 코드와 아래 실행 흐름을 기준으로 확인했습니다. 이 구조를 읽을 때 모델이 호출되는 위치와 실제 부작용이 발생하는 위치를 따로 표시하는 것이 유용합니다.

## 작동 원리: 입력에서 파일 변경과 최종 답변까지

### 1. 설정을 확인하고 실행 범위를 정합니다

대화형 CLI는 provider 설정, 샌드박스 사용 가능 여부, `--repo` 조합, persona 이름과 권한 모드를 확인한 뒤 `run_app()`을 호출합니다. 예를 들어 `--repo`는 샌드박스 모드에서 사용할 작업 원본을 의미합니다. 모델 컨텍스트 창 크기가 가정값이면 경고를 표시하고 계속하는 경로도 있으므로, 모든 사전 확인을 실행 중 오류가 사라진다는 보장으로 읽어서는 안 됩니다. [시작 확인 순서](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/cli.py#L326-L379)

TUI에서는 **Harness Home**과 **tool scope**를 분리합니다. Harness Home은 프로그램을 시작한 디렉터리이며 권한 파일·세션 로그·메모리·스킬의 기준점입니다. 샌드박스를 켜면 `AgentDeps.cwd`는 별도의 Workspace를 가리킵니다. 따라서 “모델에 지침을 읽어 넣는 위치”와 “도구가 파일을 수정하는 위치”가 다를 수 있습니다. `AgentDeps`에는 이 두 경로뿐 아니라 이벤트 출력 함수, 권한 게이트, 사용자 응답 resolver, 컨텍스트 창 정보가 전달됩니다. [경로와 의존성 구성](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/tui/app.py#L787-L822)

이 구분은 재현성과 안전성을 이해하는 데 직접 연결됩니다. 격리된 코드를 수정하는 동안에도 제어 프로그램은 원래 작업 디렉터리의 세션과 권한 정보를 유지할 수 있습니다. 다만 이때 Harness Home의 메모리와 지침이 계속 모델 입력이 된다는 사실도 함께 고려해야 합니다.

### 2. 모델과 도구를 한 Agent에 결합합니다

`build_agent()`는 provider에 맞는 모델을 만든 뒤, 출력 타입을 `str` 또는 `DeferredToolRequests`로 지정합니다. 전자는 최종 텍스트, 후자는 승인 때문에 멈춘 도구 요청을 나타냅니다. 그다음 도구 등록과 instructions 조립을 연결합니다. provider 분기는 `gemini`, `openrouter`, `modal`이며 Modal 경로는 OpenAI 호환 클라이언트와 endpoint 설정을 사용합니다. 여기서 `--model`은 선택한 provider 내부 모델 ID를 바꾸며 provider 자체를 바꾸지 않습니다. [Agent 생성](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/agent/factory.py#L46-L73), [provider 구현](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/agent/factory.py#L76-L120)

instructions는 기본 지침, 현재 persona의 prompt, 메모리, 스킬 목록을 **한 블록으로 결합**합니다. 동적 hook이므로 매 턴마다 현재 정보를 읽어 조립합니다. 스킬 본문을 모두 처음부터 넣는 구조는 아닙니다. 카탈로그에서는 이름과 짧은 설명을 보여 주고 `skill` 도구로 본문을 요청하는 방식을 사용합니다. [instructions 조립](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/agent/factory.py#L147-L168), [스킬 목록](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/skills/catalog.py#L26-L45)

도구 목록의 단일 기준은 `TOOL_SPECS`입니다. `read/glob/grep`, `write/edit`, `bash`, `lsp`, `web_fetch`, `agent` 등이 이곳에서 종류와 함께 등록됩니다. 또한 persona의 도구 허용 목록에 없는 도구는 `prepare` callback이 `None`을 반환해 모델에게 보이는 스키마에서 제외합니다. **도구를 모델에게 보여 줄지**와 **제안된 호출을 실행하도록 허가할지**를 서로 다른 층으로 구성한 셈입니다. [등록 목록](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/tools/registry.py#L53-L125), [도구 스키마 제한](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/tools/registry.py#L128-L188)

### 3. 사용자 입력을 새 턴·steering·follow-up으로 나눕니다

`Runner.submit()`은 이미 작업 중이면 새 턴을 동시에 만들지 않고 입력을 큐에 넣습니다. 실행 중 일반 입력은 steering, follow-up 의도 입력은 별도 큐로 이동합니다. 유휴 상태에서는 첫 `await` 전에 phase와 실행 task를 설정해 동시에 두 턴이 시작되는 상황을 막는 구조입니다. [입력 분배](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/harness/runner.py#L96-L118)

Runner가 만나는 경계는 두 종류입니다. `MODEL_REQUEST`에서는 steering을, `WOULD_STOP`에서는 follow-up을 꺼냅니다. `Esc`도 즉시 모든 프로세스를 강제 종료하는 명령이 아니라 플래그를 설정하고 다음 경계에서 멈추는 협조적 중단입니다. [경계와 중단](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/harness/runner.py#L121-L167)

여기에는 중요한 세부사항이 있습니다. Handler의 `MODEL_REQUEST` 경계는 `agent.iter()`를 호출하는 **leg 직전**에 있습니다. 하나의 leg 안에서는 PydanticAI가 여러 모델·도구 노드를 진행할 수 있고, Handler는 그 노드를 순회하며 이벤트를 전달합니다. 따라서 “실행 중 입력을 받는다”는 설명을 도구 실행 한가운데 즉시 끼어들거나 모든 내부 모델 요청 직전에 반드시 반영한다는 뜻으로 넓혀서는 안 됩니다. [leg와 경계](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/agent/loop.py#L166-L204), [leg 내부 노드 순회](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/agent/loop.py#L403-L425)

### 4. 모델 응답을 스트리밍하고 도구 승인으로 연결합니다

실제 leg의 중심에는 다음 코드가 있습니다. 개념도를 위해 새로 만든 예제가 아니라 원문의 일부입니다.

```python
        async with self._agent.iter(
            prompt,
            deps=self._deps,
            message_history=self.message_history,
            deferred_tool_results=deferred_results,
        ) as run:
            try:
                async for node in run:
                    if Agent.is_model_request_node(node):
                        await self._stream_model_node(ctx, node, run)
                    elif Agent.is_call_tools_node(node):
                        await self._stream_tool_node(ctx, node, run)
```

출처: [`agent/loop.py` L409–L420](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/agent/loop.py#L409-L420). 메서드의 이 부분만 발췌했으며 뒤의 `finally`와 반환부는 생략했습니다.

기존 대화 이력과 승인 결과를 Agent에 넘기고 모델 노드·도구 노드의 이벤트를 각각 스트리밍합니다. 종료 또는 예외 시 `run.all_messages()`를 다시 보관하므로, 실패한 leg에서 이미 교환한 메시지도 다음 처리의 이력에 남는 경로입니다. [이력 갱신](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/agent/loop.py#L421-L436)

쓰기 도구를 예로 보면 부작용 이전에 `needs_approval()`을 확인합니다. 아직 승인되지 않았고 BYPASS도 아니라면 `ApprovalRequired`를 발생시킵니다. Agent의 출력이 `DeferredToolRequests`가 되면 Handler는 요청별로 권한을 판정하고, 허가는 `True`, 거절은 이유가 담긴 `ToolDenied`로 바꿉니다. 다음 leg는 새 질문 대신 `deferred_tool_results`를 넘겨 재개합니다. **도구 실행을 잠시 멈추는 것과 그 결과를 대화에 연결하는 것**이 명시적인 자료형으로 이어집니다. [쓰기 전 승인](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/tools/files.py#L503-L530), [승인 조건](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/tools/approval.py#L19-L29), [승인 결과 변환](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/agent/loop.py#L438-L477)

![대화형 leg가 모델·도구 노드를 순회하다 승인 요청을 만나면 권한 판단 후 결과를 연결해 재개하는 흐름]({{ '/img/reviews/2026/coding-agent-course-review/approval-flow.svg' | relative_url }})

*리뷰어 작성, 분석 커밋 기준. 그림의 승인은 대화형 경로를 나타냅니다. headless는 BYPASS로 구성됩니다. 근거: [deferred 재개](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/agent/loop.py#L166-L204), [권한 판정 순서](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/permissions/gate.py#L79-L108).*

### 5. 권한 판단과 실행 격리는 서로 다른 문제입니다

권한 게이트는 **deny 규칙 → allow 규칙 → 모드별 기본 판단** 순서로 처리합니다. 사용자 규칙과 persona 규칙을 함께 보며, 어떤 출처에서든 deny가 맞으면 우선 거절합니다. 규칙이 결정하지 않은 경우 READ_ONLY는 허용, PLAN은 변경 도구 거절, EDIT는 파일 수정 허용·그 밖의 변경 도구 질문, DEFAULT는 변경 도구 질문으로 이어집니다. [판정 코드](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/permissions/gate.py#L79-L108)

주의할 부분은 allow 규칙이 모드 판정보다 앞선다는 점입니다. 따라서 PLAN이라는 이름만 보고 어떤 설정에서도 절대 수정이 불가능하다고 단정할 수 없습니다. 또한 READ_ONLY는 도구의 분류입니다. 예를 들어 `web_fetch`는 네트워크 GET을 수행하지만 로컬 파일 변경이 없다는 기준으로 이 분류에 들어갑니다. 이는 네트워크 접근까지 없다는 뜻이 아닙니다. [분류의 실제 기준](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/tools/registry.py#L55-L80)

권한을 통과한 `bash`는 `_get_executor().run(command, cwd=..., timeout_s=...)`으로 넘어갑니다. timeout은 설정 최대값보다 크게 요청할 수 없으며 결과에는 종료 상태와 출력이 돌아갑니다. 기본 설정의 명령 제한은 120초, 출력 절단 기준은 2,000줄·50,000바이트입니다. 이 값은 분석 커밋의 설정값이며 실행 시간이나 모델 품질을 측정한 결과가 아닙니다. [bash 처리](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/tools/bash.py#L189-L236), [설정](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/config/settings.py#L142-L146)

`none`은 로컬 실행기를 유지하고 Docker·Modal 모드는 샌드박스 실행기로 전환합니다. SandboxExecutor는 세션의 백엔드를 재사용하되 명령마다 새 `bash -lc`를 실행합니다. **파일시스템은 유지되지만 `cd`·`export` 같은 셸 상태는 다음 호출에 유지되지 않습니다.** 파일 도구도 동일 백엔드로 전송하므로 `bash`가 만든 파일과 `write`가 쓴 파일은 같은 Workspace에서 만납니다. [실행기 선택](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/tools/bash.py#L37-L80), [새 셸 실행](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/sandbox/executor.py#L128-L168)

파일 도구에는 경로의 작업 트리 이탈을 검사하는 코드가 있습니다. 샌드박스 파일 백엔드가 실패하면 호스트 파일 처리로 조용히 떨어지지 않고 모델이 볼 수 있는 오류를 반환합니다. 하지만 **파일 도구의 경로 검사만으로 `none` 모드의 셸 명령까지 격리되는 것은 아닙니다.** 승인 여부와 명령을 실행할 환경을 각각 확인해야 합니다. [경로·백엔드 처리](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/tools/files.py#L67-L166)

### 6. 작업 결과는 답변 텍스트와 변경 파일로 나뉩니다

샌드박스 작업의 출력은 최종 답변만이 아닙니다. `aclose()`는 export 후 destroy를 실행합니다. Docker는 bind mount를 사용하므로 export가 별도 복사 작업을 요구하지 않는 경로이고, Modal은 샌드박스의 파일을 호스트 Workspace로 회수한 뒤 정리하는 구조입니다. [정리 순서](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/sandbox/executor.py#L170-L188)

그다음 hand-back은 `--repo`가 있고 Git origin과 실제 변경이 있을 때 `decode/<session-id>` 브랜치를 먼저 로컬에 확보한 뒤 push를 시도합니다. 변경이 없거나 원본이 없으면 건너뜁니다. push 실패 시 로컬 브랜치가 남을 수 있지만, 원격 headless 컨테이너가 종료되면 그 로컬 Workspace도 사라질 수 있다고 결과 메시지에 명시합니다. “브랜치를 만들었다”와 “원격에 회수했다”를 구분해야 하는 이유입니다. [hand-back 조건과 실패 처리](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/sandbox/handback.py#L70-L117)

이 경로에서 확인한 것은 세션 브랜치와 push입니다. 이를 자동 PR 생성이나 원본 브랜치 자동 병합까지 제공하는 기능으로 설명해서는 안 됩니다.

### 7. 세션 로그·메모리·압축은 다른 정보를 보관합니다

대화형 세션은 기존 이력을 읽고 새 append-only JSONL 로그를 엽니다. Handler는 완료·예외 경로에서 새 메시지를 기록하고, 정상적인 최종 출력 뒤에는 자동 압축을 검토합니다. [세션 연결](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/tui/app.py#L852-L880), [턴 저장과 압축 위치](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/agent/loop.py#L191-L209)

세 가지 보관 방식을 구분하면 이해하기 쉽습니다.

- **세션 로그**: 나중에 대화를 재개하기 위한 메시지 기록입니다.
- **메모리**: 다음 실행에도 참고하도록 instructions에 읽어 넣는 파일입니다. `AGENTS.md`는 상위 디렉터리부터 탐색하고 `.decode/MEMORY.md`는 Harness Home에서 읽습니다. 파일별 출처를 붙여 결합하며 모델이 관리하는 MEMORY에 크기 상한을 적용합니다.
- **압축된 대화 이력**: 현재 모델 입력을 줄이기 위한 표현입니다. 원래 로그와 항상 같은 내용은 아닙니다. [메모리 탐색](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/memory/files.py#L1-L8), [메모리 결합·상한](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/memory/service.py#L28-L76)

자동 압축은 기본값에서 컨텍스트 창의 약 60%에 도달하면 오래된 도구 출력 본문을 줄이는 microcompaction을, 약 80%에서는 LLM 요약과 최근 이력을 결합하는 full compaction을 검토합니다. 두 임계값을 모두 넘었으면 full 경로가 우선입니다. 판단은 주로 마지막 모델 응답의 입력 토큰 수에 기반하며, 이력 크기 추정과 실제 provider 사용량은 다른 값으로 관리합니다. [임계값 설정](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/config/settings.py#L167-L182), [두 단계 선택](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/agent/loop.py#L283-L320), [토큰 수 갱신](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/agent/loop.py#L425-L430)

microcompaction은 메모리상의 오래된 도구 출력만 줄이고 JSONL 원문을 유지합니다. full compaction은 요약과 보존할 최근 꼬리를 남기며 도구 호출·결과 쌍을 갈라 놓지 않도록 경계를 고릅니다. 요약 실패 시에는 적용하지 않고 실패 정보를 남깁니다. 또한 이 자동 검토는 Handler의 종료 직전 경계에 있으므로, 하나의 긴 `agent.iter()` 내부 작업 도중 컨텍스트 초과를 항상 예방한다는 보장은 아닙니다. [압축 표현과 경계](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/context/compaction.py#L1-L19), [full 적용](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/agent/loop.py#L323-L359)

대화형 정상 종료에서는 이력을 이용한 메모리 추출도 호출합니다. 반면 아래에서 설명할 headless의 `agent.run()` 경로는 이 Handler를 통과하지 않습니다. 공통 설정에 압축 항목이 있다는 사실만으로 무인 실행에도 같은 자동 압축·JSONL 재개 동작이 적용된다고 가정하면 안 됩니다. [종료 시 메모리 처리](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/tui/app.py#L1016-L1023), [headless 실제 실행](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/runtime/headless.py#L242-L267)

### 8. Explore는 전체 대화를 복제하지 않고 독립 보고서를 돌려줍니다

persona 변경과 subagent 생성도 다릅니다. 현재 구현의 `agent` 도구는 임의의 쓰기 에이전트를 만드는 범용 작업자가 아니라, **Explore persona로 코드 조사 질문을 병렬 처리**하는 도구입니다. 기본 Explore의 도구 목록은 `read`, `glob`, `grep`, `lsp`이고 파일 수정·셸·재귀적 `agent` 호출은 들어 있지 않습니다. 여기서는 저장소에 포함된 기본 persona 정의를 기준으로 설명합니다. [기본 Explore 정의](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/agents/builtin/explore.md#L1-L20), [고정한 subagent persona](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/tools/agent.py#L51-L61)

자식은 부모의 cwd·Harness Home·모델을 공유하지만 의존성 객체, 권한 게이트, 작업 목록을 새로 받습니다. 호출에는 부모 `message_history`를 넘기지 않고 독립된 조사 prompt를 전달합니다. 그래서 “질문·검색 범위·필요한 근거”를 prompt 자체에 써야 합니다. 자식 gate는 BYPASS이지만 기본 Explore의 제한된 도구 스키마가 별도의 경계 역할을 합니다. 이 구조를 완전한 프로세스 격리로 읽어서는 안 됩니다. 같은 프로세스 안에서 부모 Agent를 다시 호출합니다. [자식 실행](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/tools/agent.py#L452-L501), [조사 지시의 요구사항](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/tools/agent.py#L333-L348)

![부모는 대화 이력을 유지하고 Explore 자식들은 독립 prompt와 읽기 도구로 조사한 보고서만 돌려주는 구조]({{ '/img/reviews/2026/coding-agent-course-review/context-boundaries.svg' | relative_url }})

*리뷰어 작성, 분석 커밋 기준. 기본 Explore는 부모의 전체 대화 이력을 받지 않으며, 그림의 도구 제한은 저장소 기본 persona를 나타냅니다. 근거: [자식 의존성과 호출](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/tools/agent.py#L452-L501), [Explore 도구](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/agents/builtin/explore.md#L1-L10).*

한 호출의 최대 fan-out은 6개, 기본 동시 실행 상한은 4개, 자식당 모델 요청 상한은 25개입니다. 전체 자식 보고서는 기본 16,000바이트 예산을 나누어 사용합니다. 보고서가 비었거나 도구 사용 근거가 없으면 한 번만 재시도하고, 한 자식의 실패는 그 자식 구획의 실패 안내로 처리해 다른 결과를 보존합니다. 마지막에는 별도 합성 모델을 호출하지 않고 라벨이 붙은 보고서를 부모에게 돌려줍니다. **리뷰어 해석으로는**, 병렬화의 핵심을 작업 수보다 부모에게 돌아오는 컨텍스트 양과 근거 계약에 둔 설계입니다. 다만 바이트 상한은 전체 토큰 비용의 상한과 같지 않습니다. [설정 상한](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/config/settings.py#L152-L161), [fan-out과 보고서 합치기](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/tools/agent.py#L354-L389), [실패·재시도](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/tools/agent.py#L410-L449)

### 9. 무인 실행은 승인 정책과 종료 계약을 바꿉니다

`decode run`은 동일한 Agent를 만들되 BYPASS gate를 넣고 `agent.run()`을 호출합니다. 사람이 응답할 채널이 없으므로 대화형 승인 요청을 기다리지 않습니다. 이 경로에서는 공통 `needs_approval()`도 BYPASS를 확인해 도구를 inline으로 진행시킵니다. “백그라운드에서도 승인을 알아서 처리한다”기보다 **승인을 생략하도록 명시적으로 선택한 실행 모드**입니다. [headless 의존성](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/runtime/headless.py#L89-L108), [실행 호출](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/runtime/headless.py#L242-L267), [공통 승인 조건](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/tools/approval.py#L19-L29)

대신 `--max-requests` 또는 `RUNTIME_MAX_REQUESTS`를 통해 모델 요청 수를 제한할 수 있습니다. 둘 다 없으면 제한을 두지 않는 경로입니다. 종료 시에는 실패·요청 한도 초과에도 실행기 정리와 hand-back을 시도하고, `--summary-json`을 지정했다면 session ID, 종료 이유, 사용량, hand-back, 출력 등을 기록합니다. 요청 횟수는 비용 통제에 도움이 되지만 모델별 토큰 수·도구 시간까지 같게 만드는 예산 단위는 아닙니다. 특히 Explore는 부모의 `ctx.usage`를 전달하지 않고 자체 요청 상한으로 실행하므로, 부모의 `--max-requests`를 자식 호출까지 합한 전역 요청 예산으로 해석해서는 안 됩니다. [자식의 독립 사용량 처리](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/tools/agent.py#L452-L501) [요청 상한](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/runtime/headless.py#L181-L192), [종료 처리](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/runtime/headless.py#L295-L353)

Modal 원격 경로는 별도 에이전트 로직을 다시 구현하지 않고 컨테이너 안에서 같은 `decode run` subprocess를 실행하는 구조입니다. `run_task`가 실제 작업을 담당하고 `nightly`는 설정된 cron에서 실행하며 `webhook`은 POST를 받아 작업을 spawn하고 call ID를 돌려줍니다. webhook에는 proxy 인증 설정이 있습니다. 일정은 배포 시 입력한 설정으로 등록되며, 배포만 했다고 기본 야간 작업이 활성화되지는 않습니다. [원격 함수](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/remote/app.py#L111-L151), [cron 등록](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/remote/app.py#L156-L200), [webhook](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/remote/app.py#L203-L222)

원격 실행의 `none`과 로컬 실행의 `none`은 환경 맥락도 다릅니다. 원격 `none`은 이미 원격 컨테이너 안에서 로컬 실행기를 쓰며, 이 모드의 임시 clone은 종료 시 사라지고 hand-back을 하지 않는 경로입니다. 원격 `modal`은 중첩 샌드박스를 사용하고 세션 브랜치 회수를 연결합니다. 원격에서 Docker 모드는 거절합니다. [원격 모드 계약](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/remote/headless.py#L14-L23)

### 10. 추적·기록·평가는 각각 다른 질문에 답합니다

Opik tracing은 “어떤 모델·도구 호출이 일어났는가”를 기록하는 장치입니다. 설정에 API key가 있으면 logfire instrumentation과 OTLP exporter를 구성하고, 없으면 tracing을 켜지 않는 경로입니다. Kitaru 연결은 Agent를 recording wrapper로 감싸 세션 기록을 연결합니다. 이력 재개용 JSONL, 실행 추적, 재실행 자료를 모두 같은 저장소라고 생각하면 장애 원인을 잘못 찾을 수 있습니다. [tracing 모듈](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/observability/tracing.py#L1-L8), [recording 연결](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/runtime/recording.py#L225-L275)

강의 문서는 평가를 결과 중심 benchmark와 행동 중심 regression으로 구분합니다. 19개 과제 benchmark는 Terminal-Bench **스타일**의 자체 구성으로 소개되며, 이것을 공식 Terminal-Bench 전체 성적이라고 부를 수는 없습니다. verifier는 별도 checkout에 숨긴 테스트를 마지막으로 덮어쓰고 `reward.txt`를 읽습니다. 보상이 없거나 잘못된 형식이면 0점과 구분하는 코드가 있습니다. [평가 문서](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/running_the_code/05_evals.md#L3-L16), [과제 구성](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/running_the_code/05_evals.md#L36-L61), [verifier 구현](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/evals/harness/verifier.py#L1-L23)

또한 verifier는 호스트에서 실행되며 환경변수를 허용 목록으로 줄입니다. 에이전트 작업을 샌드박스에서 했다는 사실만으로 평가 실행까지 같은 격리 경계 안에 있다고 생각해서는 안 됩니다. 이 리뷰에서는 평가 설계와 일부 runner·verifier를 읽었으며 점수를 새로 측정하거나 README의 데모 성공을 재현하지 않았습니다. [호스트 평가 환경](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/evals/harness/verifier.py#L45-L68)

## 문서에 따라 시작하는 방법

처음에는 모델 endpoint 배포와 평가 서버를 한꺼번에 준비하기보다 터미널 에이전트의 기본 동작부터 확인하는 것이 이해하기 쉽습니다. 이것은 학습 순서에 대한 리뷰어의 제안이며, 아래 명령 자체는 분석한 README의 quick start를 그대로 발췌한 것입니다. 실행 결과를 재현했다는 의미는 아닙니다. [README 명령](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/README.md#L27-L35)

```bash
git clone https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course.git
cd building-a-coding-agent-from-scratch-course
make install
cp .env.example .env   # set LLM API key
uv run decode
```

매니페스트는 Python 3.12 이상을 요구합니다. 상세 설치 문서는 uv와 Git, macOS·Linux 또는 WSL2 환경을 안내합니다. `.env`에는 provider와 해당 자격 증명을 설정합니다. README의 무료 실행 문구는 소개상 주장으로 구분해야 하며, 사용한 provider·모델 endpoint·실행 인프라에 따라 인증과 비용 조건을 별도로 확인해야 합니다. 이 글은 해당 서비스들의 현재 무료 한도나 가격을 보증하지 않습니다. [요구 버전](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/pyproject.toml#L5-L11), [설치 안내](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/running_the_code/01_install_and_usage.md#L5-L37)

TUI 기본 키는 일반 전송 `Enter`, 실행 중 steering `Enter`, follow-up `Alt+Enter`, 협조적 중단 `Esc`, 승인·거절 `y/n`입니다. 세션 재개 명령은 다음과 같이 문서에 제시됩니다. [키 안내](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/running_the_code/01_install_and_usage.md#L57-L74)

```bash
decode --resume               # most recent session in this directory
decode --resume <session-id>  # id = the .jsonl filename stem
decode sessions               # list all sessions from most recent to least
```

위 명령은 상세 설치 문서의 `make install-cli` 단계로 `decode`를 PATH에 둔 경우의 표기입니다. README quick start는 `uv run decode`를 사용합니다. 같은 도구를 설명하는 두 문서의 실행 전제까지 함께 읽어야 합니다. [CLI 설치 단계](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/running_the_code/01_install_and_usage.md#L9-L15)

다음 단계의 문서는 역할별로 나뉩니다. [`03_sandboxing.md`](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/running_the_code/03_sandboxing.md)는 도구가 실행될 환경, [`04_deploy.md`](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/running_the_code/04_deploy.md)는 headless 배포, [`05_evals.md`](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/running_the_code/05_evals.md)는 평가, [`06_evals_replays.md`](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/running_the_code/06_evals_replays.md)는 Kitaru 기록·재실행을 다룹니다. 모델을 Modal endpoint에 올리는 일과 도구를 Modal Sandbox에서 실행하는 일은 서로 다른 설정 축입니다. [두 Modal 설정의 구분](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/running_the_code/05_evals.md#L63-L94)

## 사용할 때 확인할 경계와 라이선스

이 저장소의 학습 가치는 장치의 존재뿐 아니라 적용되는 경로와 실패 상태를 읽을 수 있다는 데 있습니다. 실제 적용 전에는 다음 차이를 확인하는 편이 좋습니다.

- **대화형·headless 기능 대칭성**: Agent 구성은 공유하지만 승인, 턴 큐, 자동 압축, 세션 처리까지 동일한 것은 아닙니다. 특히 무인 작업은 BYPASS와 요청 상한을 함께 확인해야 합니다.
- **LSP 범위**: `definition`, `references`, `hover`, `diagnostics`를 처리하는 도구가 있지만 Modal 샌드박스 모드에서는 이 도구를 사용할 수 없다는 분기가 있습니다. 전체 환경에서 같은 코드 탐색 기능이 보장되는 것은 아닙니다. [LSP 분기](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/src/decode/tools/lsp.py#L51-L95)
- **결과 보존**: 실행 성공 여부와 원격 push 성공 여부는 별개입니다. ephemeral 환경에서는 hand-back 실패의 의미가 로컬 실행과 다릅니다.
- **평가 해석**: trace가 잘 남는다는 것과 과제를 해결한다는 것은 별개입니다. 평가 문서도 benchmark와 regression을 나누며, 실행 조건과 grader·judge가 달라지면 단순 점수 비교가 어렵습니다. [평가 조건 안내](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/running_the_code/05_evals.md#L63-L98)

코드 패키지는 Apache-2.0 라이선스를 명시하며 저장소에 해당 LICENSE 파일이 있습니다. 모델 가중치·외부 API·클라우드 서비스의 이용 조건까지 이 라이선스 하나로 정해지는 것은 아니므로, 실제 사용하는 외부 구성요소의 조건은 별도로 확인해야 합니다. [라이선스 선언](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/pyproject.toml#L10-L19), [LICENSE](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/2ba55b548dbb2bb352c3651e20c8a21f3e5eb9d4/LICENSE)

## 코드에서 얻을 수 있는 핵심 관점

decode에서 가장 배울 만한 부분은 “LLM이 도구를 부른다”는 동작을 여러 개의 명시적 계약으로 나누는 방식입니다. Agent의 출력 타입은 답변과 승인 중단을 구분하고, Runner의 경계는 새 입력과 종료를 조율하며, tool scope는 메모리 위치와 수정할 파일 트리를 구분합니다. Explore는 독립 질문과 제한된 보고서로 부모의 컨텍스트를 관리하고, hand-back은 답변 이후에도 변경 결과의 회수를 별도 문제로 다룹니다.

**리뷰어의 해석으로는**, 이 강의를 읽는 실용적인 방법은 기능을 모두 켜는 것보다 요청 하나가 각 경계를 지나는 과정을 추적하는 데 있습니다. 입력을 받는 경계, 실제 부작용을 허가하는 경계, 컨텍스트를 줄이는 경계, 결과를 보존하는 경계를 구별하면 자신의 에이전트에서 어떤 책임이 빠져 있는지 더 구체적으로 판단할 수 있습니다.

### 이 글에서 다루지 못한 부분

Docker·Modal 백엔드의 모든 파일 전송·자격 증명 처리 분기, LSP stdio 프로토콜 구현 전체, 파일 편집의 fuzzy matching 세부 알고리즘, web 도구의 변환·전송 처리, 모든 regression case·benchmark 과제·집계식, Kitaru importer·evaluator의 전체 동작은 상세 검토하지 않았습니다. 모델 serving endpoint의 실제 배포 가능 여부, 외부 SDK·서비스와의 현재 호환성, 실제 응답 품질·비용·실행 성공률도 측정하지 않았습니다. 따라서 이 리뷰의 구조 분석과 데모·벤치마크의 실행 검증은 구분해서 읽어야 합니다.
