---
type: "Repo Review"
title: "[Repo Review] AgentScope — 모델·도구 호출과 사용자 승인으로 보는 ReAct 루프"
description: "AgentScope 콘솔의 입력이 모델 호출과 도구 실행을 거쳐 답변으로 돌아오는 흐름을 따라가며 승인 대기, 응답 취소, MCP, OpenTelemetry의 연결 지점을 살펴봅니다."
date: "2026-11-10"
tags:
  - "Repo Review"
  - "AI Agent"
  - "MCP"
  - "Python"
resource: "https://github.com/agentscope-ai/agentscope/tree/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d"
generated:
  by: "process:blog-review"
  at: "2026-11-10T06:03:25+09:00"
sources:
  - id: "github:agentscope-ai/agentscope@d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d"
    resource: "https://github.com/agentscope-ai/agentscope/tree/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d"
    title: "AgentScope"
    author: "agentscope-ai"
    last_modified: "2026-11-09"
status: "stable"
year: "2026"
analyzed_at: "2026-11-10T06:03:25+09:00"
source_id: "agentscope-ai/agentscope"
source_revision: "d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d"
source_type: "repo"
source_url: "https://github.com/agentscope-ai/agentscope/tree/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d"
visual_sources:
  - path: "/img/reviews/2026/agentscope-repo-review/react-loop.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/agent/_agent.py#L1140-L1275"
    caption: "리뷰어 작성, 분석 커밋 기준. 콘솔 입력과 모델 호출·도구 실행의 순환."
  - path: "/img/reviews/2026/agentscope-repo-review/approval-and-interruption.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/console/_console.py#L18-L102"
    caption: "리뷰어 작성, 분석 커밋 기준. 도구 승인 대기와 응답 취소의 상태 전이."
---

## 들어가며

파일을 조사하는 에이전트가 답변을 만드는 동안 어떤 명령을 보냈는지, 파일을 고치기 전에 어디에서 승인을 받는지 알 수 있어야 합니다. 이 동작을 직접 구현하려면 모델마다 다른 메시지 형식, 도구 호출과 결과의 연결, 중간 출력, 취소 후 대화 상태를 함께 관리해야 합니다. AgentScope는 이 작업을 모델 어댑터, 도구 등록소, 에이전트 실행 루프, 이벤트 스트림으로 나눕니다. [README의 구성 요소](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/README.md#L122-L136)

분석 대상은 `agentscope-ai/agentscope`의 커밋 `d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d`이며, 소스의 버전 표기는 `2.0.12dev`입니다. README의 터미널 예시를 출발점으로 삼아 모델 호출, 파일 도구의 실행과 승인, 대화 상태 저장을 추적했습니다. MCP와 추적 기능은 예시에 덧붙일 수 있는 별도 경로로 읽었습니다. 분석은 소스와 문서의 정적 대조에 근거합니다. [분석 커밋](https://github.com/agentscope-ai/agentscope/tree/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d) · [버전 정의](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/_version.py#L1-L4)

## AgentScope는 무엇인가요?

AgentScope는 언어 모델이 도구를 호출하면서 작업을 이어갈 수 있도록 실행 환경을 구성하는 Python 프레임워크입니다. README에서 말하는 **ReAct**는 추론과 행동을 번갈아 수행하는 루프의 이름입니다. 이 커밋의 공개 클래스 `Agent`에 채팅 모델, `Toolkit`, 선택적 미들웨어를 넘기면 이 루프를 구성할 수 있습니다. 예제는 `Agent`를 `launch_console`에 전달해 표준 입력과 출력에 연결합니다. [공개 API](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/agent/__init__.py#L3-L18) · [README 콘솔 예제](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/README.md#L138-L176)

한 번의 모델 호출에 답변이 완성될 수도 있고, 모델이 파일 읽기 같은 도구 호출을 반환할 수도 있습니다. 후자의 경우 에이전트가 권한을 판단하고 도구 결과를 대화에 넣은 뒤, 그 결과를 포함해 다시 모델을 부릅니다. 모델이 고른 도구와 실제 실행 여부 사이에 판단 단계가 있다는 점이 승인 대기를 이해하는 출발점입니다. [실행 루프](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/agent/_agent.py#L1184-L1275) · [도구 권한 분기](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/agent/_agent.py#L2525-L2606)

## 아키텍처와 디렉터리 구조

| 경로 | 퀵스타트에서 맡는 역할 |
| --- | --- |
| `console/` | 입력 한 줄을 `UserMsg`로 감싸고 `reply_stream()`이 생성하는 이벤트를 렌더러에 전달합니다. 승인 요청이 오면 결과 이벤트를 같은 에이전트에 넘깁니다. [콘솔 실행부](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/console/_console.py#L151-L175) |
| `agent/`, `state/` | `Agent`가 모델 호출과 도구 실행 중 다음 단계를 고릅니다. `AgentState`는 대화, 요약, 현재 응답의 ID와 반복 횟수, 도구·권한 상태를 나누어 보관합니다. [루프 분기](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/agent/_agent.py#L1140-L1222) · [상태 정의](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/state/_state.py#L182-L295) |
| `model/`, `formatter/` | `DashScopeChatModel`이 공용 `Msg` 객체를 DashScope 요청 형식으로 바꾸고 제공자 API를 호출합니다. [모델 어댑터](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/model/_dashscope/_model.py#L195-L283) · [포매터](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/formatter/_dashscope_formatter.py#L265-L289) |
| `tool/`, `permission/`, `mcp/` | `Toolkit`이 기본 그룹과 활성 그룹의 도구를 모읍니다. 에이전트가 입력과 권한을 확인한 뒤 도구에 실행을 위임하며, MCP 도구는 같은 등록 경로를 사용합니다. [도구 수집](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/tool/_toolkit.py#L511-L552) · [검증·권한 검사](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/agent/_agent.py#L2487-L2532) |
| `middleware/`, `event/` | 미들웨어는 응답·모델 호출·도구 실행 같은 지점에 끼어듭니다. 콘솔은 모델과 도구가 진행하며 내보내는 이벤트를 읽습니다. [훅 구성](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/agent/_agent.py#L225-L250) · [이벤트 렌더링](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/console/_renderer.py#L146-L202) |

![콘솔의 UserMsg가 Agent를 거쳐 DashScope에 전달되고, 도구 결과가 다음 모델 호출로 돌아가는 흐름]({{ '/img/reviews/2026/agentscope-repo-review/react-loop.svg' | relative_url }})

*그림 1. 리뷰어 작성, 분석 커밋 기준. 일반 응답에서 도구 결과는 대화에 저장되고, 최종 응답을 만들 때까지 모델이 이를 다시 읽습니다. [콘솔 입력과 스트림](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/console/_console.py#L35-L43) · [루프 분기](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/agent/_agent.py#L1140-L1275) · [도구 결과 저장](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/agent/_agent.py#L2698-L2710)*

## 작동 원리

### 1. 사용자 메시지와 도구 스키마로 모델을 호출합니다

콘솔의 `launch_console()`은 사용자 입력을 `UserMsg`로 변환합니다. 내부의 `_run_reply()`가 `agent.reply_stream(inputs)`를 읽으며 이벤트를 렌더러에 전달합니다. 에이전트는 새 입력을 대화 문맥에 추가하고 새 `ReplyContext`를 만듭니다. 이때 현재 응답에 고유한 ID를 붙이고 반복 횟수를 0으로 초기화합니다. [콘솔 입력 루프](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/console/_console.py#L151-L175) · [스트림 소비](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/console/_console.py#L35-L43) · [응답 초기화](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/agent/_agent.py#L1093-L1128) · [메시지 저장](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/agent/_agent.py#L2041-L2100)

`_prepare_model_input()`은 시스템 프롬프트, 있을 경우 압축 요약, 현재 대화 문맥을 순서대로 담습니다. 도구 스키마는 `Toolkit.get_tool_schemas()`에서 가져옵니다. 스키마에는 모델이 사용할 도구 이름, 설명, 입력 매개변수의 구조가 담기며 기본 그룹과 활성 그룹이 그 범위를 정합니다. 이 구분 덕분에 모델에 전달하는 도구 목록은 에이전트에 등록된 모든 도구와 다를 수 있습니다. [모델 입력 조립](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/agent/_agent.py#L3315-L3351) · [스키마 생성](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/tool/_toolkit.py#L171-L223) · [활성 그룹 검사](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/tool/_toolkit.py#L511-L536)

README 예제의 모델 이름은 `qwen3.6-plus`입니다. 이 코드에서 `DashScopeChatModel`은 `DashScopeChatFormatter`로 메시지를 변환하고, 자격 증명에 지정된 기본 주소를 사용하는 OpenAI 호환 클라이언트로 `chat.completions.create()`를 호출합니다. 기본 스트리밍 설정에서는 응답 조각을 텍스트·사고 블록·도구 호출 등의 이벤트로 내보내며, 마지막 조각에 모인 응답은 대화에 저장합니다. 마지막 조각이 없으면 완결된 응답을 조립할 수 없으므로 오류를 냅니다. [클라이언트 구성](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/model/_dashscope/_model.py#L117-L174) · [API 호출](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/model/_dashscope/_model.py#L219-L283) · [조각 수신과 완료 검사](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/agent/_agent.py#L1725-L1819)

### 2. 도구 호출을 검증하고 실행 결과를 다음 추론에 넣습니다

모델이 도구를 요청하면 그 호출은 이름·입력·호출 ID가 있는 `ToolCallBlock`으로 문맥에 들어갑니다. `_next_action()`은 이미 결과가 붙은 호출을 ID로 걸러 내고 실행 가능한 것만 `Acting`으로 보냅니다. 실행 단계는 도구의 `is_concurrency_safe`를 기준으로 연속 호출을 배치로 묶습니다. 예를 들어 `Read`에는 이 플래그가 켜져 있고 `Write`에는 꺼져 있어 두 도구의 실행 정책이 달라집니다. [결과 ID를 대조하는 분기](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/agent/_agent.py#L3574-L3622) · [배치 분류](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/agent/_agent.py#L2102-L2140) · [Read](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/tool/_builtin/_read.py#L123-L130) · [Write](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/tool/_builtin/_write.py#L57-L65)

실행 직전에는 먼저 도구가 활성 상태인지 찾고, 모델이 낸 인자를 도구의 JSON 스키마에 맞춰 파싱·검증합니다. 이어서 권한 정책을 평가합니다. 잘못된 입력과 거부된 호출은 도구 오류 또는 거부 결과로 남습니다. 허용된 내부 실행은 `_acting()`을 거쳐 `Toolkit.call_tool()`에 전달됩니다. 도구가 조각 하나, 동기 생성기, 비동기 생성기로 결과를 제공해도 `Toolkit`은 이를 `ToolChunk` 단위로 내보내고 끝에서 `ToolResponse`로 모읍니다. [입력 검증과 권한 분기](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/agent/_agent.py#L2487-L2632) · [실행 위임](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/agent/_agent.py#L2790-L2818) · [도구 출력 수집](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/tool/_toolkit.py#L293-L392)

출력 조각은 콘솔 이벤트로 전달되고, 완료된 결과는 원래 호출 ID를 가진 `ToolResultBlock`으로 문맥에 추가됩니다. `AgentState.append_context()`는 같은 응답 ID와 에이전트 이름을 가진 마지막 메시지에 블록을 붙입니다. 다음 모델 호출은 이 문맥을 읽어 도구의 결과를 반영합니다. 결과가 문맥 한도를 넘으면 보존할 부분을 잘라내고, 별도의 저장 기능인 `offloader`가 설정된 경우 생략한 부분을 파일로 내려보냅니다. 실행할 호출이 없고 답변 후보가 준비되면 루프는 종료 이벤트와 응답을 내보냅니다. 일반 텍스트 경로에서 반복 한도에 닿으면 도구를 끈 마무리 호출을 한 번 시도합니다. [완료 결과 변환·저장](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/agent/_agent.py#L2630-L2710) · [상태의 블록 저장](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/state/_state.py#L298-L326) · [최종 응답과 반복 한도](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/agent/_agent.py#L3729-L3834)

`reply_stream()`은 기본적으로 이벤트를 반환하며 `yield_final_msg=True`일 때 마지막 `Msg`도 전달합니다. 호출자가 스트림을 직접 다룰 필요가 없다면 `reply()`가 같은 흐름을 내부에서 소비하고 마지막 메시지를 반환합니다. 콘솔은 같은 에이전트 인스턴스를 유지하므로 다음 사용자 입력에서도 `agent.state`의 대화 문맥을 사용합니다. [두 응답 API](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/agent/_agent.py#L274-L365) · [콘솔의 세션 범위](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/console/_console.py#L105-L119)

### 3. 승인 대기와 취소는 다른 상태를 남깁니다

도구가 승인을 필요로 하면 에이전트는 호출 상태를 `ASKING`으로 기록한 뒤 `RequireUserConfirmEvent`를 보냅니다. 호출의 답을 기다리는 동안 응답 스트림은 끝날 수 있지만 완료를 뜻하는 `ReplyEndEvent`는 발생하지 않습니다. 콘솔의 `_confirm()`이 사용자 선택을 `UserConfirmResultEvent`로 만들어 다시 전달하면, 에이전트는 대기 중인 호출 ID를 대조합니다. 승인된 호출은 `ALLOWED`로 바꾸고 거부된 호출에는 거부 결과를 붙입니다. 상태에 남아 있는 응답 ID와 반복 횟수를 이어 사용합니다. 외부 실행 결과가 필요한 도구도 `SUBMITTED` 상태와 `ExternalExecutionResultEvent`로 이어갈 수 있으며, 여기서 콘솔 예제는 승인 결과의 왕복을 보여 줍니다. [승인 요청](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/agent/_agent.py#L2573-L2585) · [대기 중 스트림 반환](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/agent/_agent.py#L1154-L1169) · [ID 대조와 상태 갱신](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/agent/_agent.py#L1873-L2036) · [콘솔 입력 처리](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/console/_console.py#L74-L102)

스트리밍 중 Ctrl+C는 신호 핸들러를 지원하는 이벤트 루프에서 응답 태스크에 취소를 전달합니다. 에이전트는 진행 중인 마지막 응답에서 짝이 되는 결과가 없는 도구 호출을 찾아 `INTERRUPTED` 결과를 붙이고, 현재 응답을 종료합니다. 승인 질문에서 중단하면 콘솔이 `UserInterruptEvent`로 그 대기를 닫습니다. 대화 문맥을 유지하므로 이후 입력으로 새 응답을 시작할 수 있습니다. 이 정리 로직의 대상은 문맥과 이벤트의 호출 상태입니다. 이미 완료된 파일 쓰기나 외부 요청을 되돌리는 기능은 이 경로에 없습니다. [콘솔 SIGINT 처리](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/console/_console.py#L50-L71) · [승인 중단](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/console/_console.py#L167-L175) · [대기 중인 응답 닫기](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/agent/_agent.py#L1074-L1086) · [취소와 결과 정리](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/agent/_agent.py#L965-L1027) · [응답 종료](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/agent/_agent.py#L1277-L1310)

![승인 대기는 동일 응답으로 복귀하고 취소는 미완료 호출을 정리해 현재 응답을 끝내는 비교]({{ '/img/reviews/2026/agentscope-repo-review/approval-and-interruption.svg' | relative_url }})

*그림 2. 리뷰어 작성, 분석 커밋 기준. 승인은 도구 실행을 재개하는 입력이고, 취소는 호출 결과를 정리하는 종료 경로입니다. [승인 처리](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/agent/_agent.py#L1960-L2005) · [중단 처리](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/agent/_agent.py#L1277-L1310)*

### 4. MCP 서버의 도구도 같은 실행 경로에 붙입니다

MCP(Model Context Protocol)는 외부 서버가 도구 이름과 입력 스키마를 공개하고 클라이언트가 그 도구를 호출할 수 있게 하는 프로토콜입니다. 이 저장소의 `MCPClient`는 표준 입출력 기반 연결에서는 지속 세션을 요구하며, HTTP에서는 지속 세션과 필요할 때 여는 연결을 모두 지원합니다. 지속 세션을 쓰는 클라이언트는 연결한 뒤 `Toolkit`에 등록해야 합니다. 활성 그룹의 도구를 모을 때 특정 서버의 도구 목록 요청이 실패하면 경고를 남기고 그 서버의 도구를 건너뜁니다. [MCP 연결 설정](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/mcp/_mcp_client.py#L93-L110) · [연결 확인](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/tool/_toolkit.py#L127-L151) · [목록 요청 실패 처리](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/tool/_toolkit.py#L511-L552)

서버의 도구는 `MCPTool`로 감싸집니다. 모델에는 `mcp__서버명__도구명` 규칙을 적용한 이름과 스키마를 제공하고, 서버에 실행을 요청할 때는 원래 도구 이름을 보냅니다. 어댑터의 기본 권한 검사는 서버가 준 `read_only_hint`가 참이면 허용 결정을, 그 외에는 승인 요청을 반환합니다. 같은 메서드의 docstring에는 모든 작업을 허용한다는 문장이 남아 있지만, 실제 분기에는 이 두 경우가 있습니다. 서버의 읽기 전용 표기는 서버가 제공하는 힌트이므로 도구가 실제로 수행하는 작업은 해당 서버의 구현에 달려 있습니다. [도구 어댑터와 기본 권한](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/tool/_adapters.py#L244-L324) · [원래 이름으로 실행 요청](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/tool/_adapters.py#L390-L414)

MCP 어댑터는 서버 응답의 콘텐츠를 내부 블록으로 변환합니다. `stream_progress`를 켜면 도구 진행 상황도 스트림으로 받을 수 있습니다. 이때 버퍼가 넘치면 오래된 진행 업데이트부터 빠지며, 최종 결과는 따로 전달합니다. 진행 이벤트로 모든 업데이트의 이력을 재구성할 수 있는 구조는 아닙니다. [진행 스트림의 범위](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/tool/_adapters.py#L326-L356) · [최종 콘텐츠 변환](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/tool/_adapters.py#L436-L462)

### 5. 콘솔 이벤트와 OpenTelemetry 추적은 목적이 다릅니다

콘솔은 `TextBlockDeltaEvent`를 받아 텍스트를 이어서 쓰고, 도구 호출·결과와 모델 호출 완료를 각각 표시합니다. 반면 `TracingMiddleware`는 OpenTelemetry의 스팬, 즉 시작과 종료가 있는 작업 기록을 응답·모델 호출·도구 실행에 붙입니다. 미들웨어를 에이전트에 등록하고 OpenTelemetry SDK의 `TracerProvider`가 설정돼 있어야 훅이 기록을 생성합니다. 퀵스타트에는 이 등록이 없으므로 터미널에 도구 결과가 보인다고 해서 추적 데이터의 수집도 시작된 것은 아닙니다. [콘솔 렌더러](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/console/_renderer.py#L146-L196) · [추적 활성 조건](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/middleware/_tracing/_trace.py#L59-L70) · [훅 등록 예시](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/middleware/_tracing/_trace.py#L117-L164)

응답과 도구 실행 훅은 비동기 생성기의 다음 조각을 받을 때만 스팬 문맥을 연결하고, 조각을 호출자에게 넘기기 전에 해제합니다. 이 방식은 스트림이 여러 태스크를 오갈 때 연결과 해제를 같은 실행 문맥에서 끝내기 위한 것입니다. 모델 호출 훅은 반환값이 스트림이면 래퍼에서 끝까지 관찰합니다. 스팬 속성을 만드는 코드에는 입력·출력 메시지와 도구 인자가 포함되는 경로도 있어, 스팬은 호출 시간이나 토큰 수만 담는 지표와 데이터 범위가 다릅니다. [응답 훅](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/middleware/_tracing/_trace.py#L158-L171) · [응답과 도구 문맥 해제](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/middleware/_tracing/_trace.py#L209-L225) · [모델 훅](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/middleware/_tracing/_trace.py#L259-L307) · [도구 훅](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/middleware/_tracing/_trace.py#L337-L363) · [입력 메시지 속성](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/middleware/_tracing/_extractor.py#L226-L242) · [출력 메시지 속성](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/middleware/_tracing/_extractor.py#L532-L549) · [도구 인자 속성](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/middleware/_tracing/_extractor.py#L553-L599)

## 설치와 사용

README는 Python 3.11 이상에서 PyPI 패키지를 설치하는 다음 명령을 안내합니다. 이 설치 명령에는 분석 커밋을 고정하는 인자가 없으므로, 글에서 읽은 소스와 비교할 때는 분석 커밋 링크를 기준으로 삼습니다. [README 설치 안내](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/README.md#L98-L120) · [패키지 요구사항](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/pyproject.toml#L1-L39)

```bash
uv pip install agentscope
```

콘솔 예시는 `DASHSCOPE_API_KEY`를 환경 변수에서 읽어 `DashScopeCredential`에 전달하고, `Bash`, `Grep`, `Glob`, `Read`, `Write`, `Edit`를 도구 목록에 넣습니다. 따라서 API 호출에 필요한 자격 증명과 함께, 각 도구의 실행 위치가 예제의 동작 범위를 정합니다. `Bash()`처럼 별도 백엔드를 넘기지 않은 퀵스타트에서는 해당 도구가 호스트의 `LocalBackend`를 선택합니다. 권한 판정과 실행 환경 분리가 별개의 설정인 이유입니다. [퀵스타트 설정](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/README.md#L140-L176) · [Bash 백엔드 선택](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/tool/_builtin/_bash.py#L137-L177) · [백엔드 경계](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/tool/_builtin/_backend.py#L8-L32)

## 한계와 주의점

퀵스타트 콘솔의 대화는 프로세스 안의 `agent.state`에 저장됩니다. 도구 승인을 기다렸다가 같은 응답을 잇는 기능이 있어도, 콘솔은 세션 저장이나 프로세스를 재시작한 뒤의 복구를 제공하지 않습니다. README에 소개된 장기 메모리는 별도의 백엔드와 미들웨어를 사용하는 기능으로, 퀵스타트의 대화 문맥과 구분됩니다. 저장소 라이선스는 Apache 2.0입니다. [콘솔의 세션 범위](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/src/agentscope/console/_console.py#L105-L119) · [README 장기 메모리 안내](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/README.md#L130-L136) · [메모리 의존성](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/pyproject.toml#L145-L155) · [라이선스](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/LICENSE#L1-L6)

### 이 글에서 다루지 못한 부분

서비스의 세션 저장과 복구, Mem0·ReMe의 장기 메모리 내부, 다중 에이전트 파이프라인, 음성·A2A, 샌드박스별 실행·격리 보장은 분석 범위 밖입니다. 공급자 API 응답, MCP 서버 동작, 원격 텔레메트리 전달도 실행으로 검증하지 않았습니다. [서비스와 배포 기능](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/README.md#L178-L212) · [패키지 선택 의존성](https://github.com/agentscope-ai/agentscope/blob/d8ebf89b6ce3ce904992dc0f3be0fc1be1b1211d/pyproject.toml#L66-L102)

## 결론

AgentScope의 퀵스타트에서는 콘솔이 메시지와 이벤트를 주고받고, `Agent`가 모델 호출과 도구 실행 사이의 상태를 관리합니다. 도구 호출 ID를 기준으로 결과를 대화에 연결하기 때문에 모델은 다음 호출에서 관찰한 결과를 읽을 수 있습니다. 승인 대기는 그 호출의 실행 여부를 이어서 결정하며, 취소는 남은 호출을 정리한 뒤 현재 응답을 끝냅니다. MCP 도구와 OpenTelemetry 미들웨어는 각각 이 구조의 도구 등록과 실행 훅을 확장합니다.
