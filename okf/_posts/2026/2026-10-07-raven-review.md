---
type: "Repo Review"
title: "[Repo Review] Raven: 여러 에이전트의 하네스를 조합하고 실행 근거를 남기는 방법"
description: "Raven의 요청 처리부터 DAG 검증·전문 에이전트 실행·파일 기반 결과 전달까지 추적하고, 모듈형 하네스와 자기 개선 도구의 구현 경계를 분석합니다."
date: "2026-10-07"
tags:
  - "Repo Review"
  - "AI Agent"
  - "Python"
  - "MCP"
resource: "https://github.com/EverMind-AI/Raven/tree/3632e6040c7038a60ec418ce39ccae185c72c19f"
generated:
  by: "process:blog-review"
  at: "2026-10-07T06:07:05+09:00"
sources:
  - id: "EverMind-AI/Raven"
    resource: "https://github.com/EverMind-AI/Raven/tree/3632e6040c7038a60ec418ce39ccae185c72c19f"
    title: "Raven"
  - id: "arxiv:2609.33439v1"
    resource: "https://arxiv.org/abs/2609.33439v1"
    title: "Raven: The Harness of Harnesses for Composable Agentic Intelligence"
status: "stable"
year: "2026"
analyzed_at: "2026-10-07T06:07:05+09:00"
source_id: "EverMind-AI/Raven"
source_revision: "3632e6040c7038a60ec418ce39ccae185c72c19f"
source_type: "repo"
source_url: "https://github.com/EverMind-AI/Raven/tree/3632e6040c7038a60ec418ce39ccae185c72c19f"
visual_sources:
  - path: "/img/reviews/2026/raven-review/runtime.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/raven/rpc/methods/turn.py#L410"
    caption: "리뷰어 작성, 분석 커밋 기준: 사용자 요청에서 실행 기록까지의 런타임 경로"
    evidence:
      - "https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/raven/agent/loop/turn_path.py#L2334"
      - "https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/raven/agent/subagent/dag_runner.py#L252"
  - path: "/img/reviews/2026/raven-review/dag.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/raven/agent/subagent/dag_runner.py#L558"
    caption: "리뷰어 작성, 분석 커밋 기준: 그래프 검증과 의존성·판정 기반 실행"
    evidence:
      - "https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/raven/agent/subagent/dag_graph.py#L292"
      - "https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/raven/agent/subagent/dag_runner.py#L1766"
---

## 들어가며

여러 에이전트에게 일을 나누는 것보다 어려운 문제는 **누가 어떤 입력을 받아야 하며, 어떤 결과가 확정되어야 다음 일을 시작할 수 있는가**입니다. 조사 에이전트가 자료를 찾고 코딩 에이전트가 실험을 수행하더라도, 중간 산출물과 실패 상태를 전달하는 규칙이 없으면 협업은 긴 대화의 묶음에 머뭅니다.

Raven은 이 문제를 Host Agent와 전문 에이전트, 파일 기반 실행 기록, 교체 가능한 하네스 모듈로 다룹니다. 하네스(harness)는 LLM 자체를 둘러싸고 문맥·도구·행동·실행 수명주기를 관리하는 소프트웨어입니다. README의 “harness of harnesses”는 이러한 실행 환경을 가진 에이전트들을 다시 연결하는 호스트라는 뜻으로 읽을 수 있습니다. [프로젝트 정의](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/README.md#L27)

이 글은 `EverMind-AI/Raven`의 커밋 `3632e6040c7038a60ec418ce39ccae185c72c19f`를 고정하여 읽은 정적 코드 리뷰입니다. 패키지 선언은 `0.2.4`, Python 요구 버전은 `3.12` 이상입니다. 설치·서버·테스트·대상 코드는 실행하지 않았으며, 모델 응답과 벤치마크 성능을 재현했다고 주장하지 않습니다. [패키지 선언](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/pyproject.toml#L1)

## Raven은 무엇인가

Raven은 **자체 또는 외부 에이전트를 공통 명부에 등록하고, 단일 위임이나 의존성 그래프로 실행하며, 결과를 파일과 상태로 보존하는 에이전트 런타임**입니다. README는 Research·Code·Design·Oncall의 네 가지 대표 역할을 소개합니다. 사용자 문서에는 Design 뒤에서 프레젠테이션 작업을 처리하는 Raven-PPT까지 다섯 정의가 등장합니다. 다섯 정의가 모두 독립적으로 보이는 메뉴라는 뜻은 아니며, Raven-PPT는 통상 Design의 숨은 라우팅 대상입니다. [에이전트 종류와 경계](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/docs-site/docs/agent-integrations.md#L28)

| 역할 | 문서상 주된 작업 | 사용 전에 구분할 점 |
| --- | --- | --- |
| Raven-Research | 웹 조사와 출처를 갖춘 보고서 | 검색·본문 수집 도구와 자격 증명이 필요합니다. |
| Raven-Code | 코드 변경, 디버깅, 검증 | 실제 작업 폴더를 수정하므로 파일 소유권이 필요합니다. |
| Raven-Design | 시각 자료와 발표 자료 | 디자인·미디어 실행 환경 준비가 필요합니다. |
| Raven-Oncall | 장시간 작업 실행과 관찰 | 원격 대상 접근, 예산, 종료 조건이 필요합니다. |

중요한 구분은 **누가 제공한 에이전트인가**와 **어떤 방식으로 실행하는가**입니다. Raven이 제공하는 에이전트도 ACP 프로세스로 실행할 수 있습니다. `kind: builtin`은 호스트 내부 Raven 루프이고, `acp`·`cli`는 외부 프로세스와 연결하는 방식이며, `openai`는 호환 HTTP 엔드포인트입니다. A2A 피어는 별도의 호스트 연결로, 같은 서브에이전트 명부와 동일하지 않습니다. 여기서 ACP는 에이전트 클라이언트와 실행 프로세스를 연결하는 프로토콜이며, MCP는 에이전트에 도구를 연결하는 프로토콜입니다. [실행 경계 표](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/docs-site/docs/agent-integrations.md#L9)

## 아키텍처: 화면, 실행 루프, 전문 에이전트의 분리

![Raven의 사용자 요청, 호스트 루프, DAG 실행 및 기록 경로]({{ '/img/reviews/2026/raven-review/runtime.svg' | relative_url }})

*리뷰어 작성, 분석 커밋 기준. [RPC 입력](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/raven/rpc/methods/turn.py#L410), [호스트 문맥과 Planning](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/raven/agent/loop/turn_path.py#L2334), [DAG 실행](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/raven/agent/subagent/dag_runner.py#L252)을 요약했습니다. 모든 요청이 DAG를 거치는 것은 아니며, 위임 도구를 선택한 경우에 해당 경로가 열립니다.*

| 위치 | 책임 | 이 글에서 확인한 내용 |
| --- | --- | --- |
| `raven/cli/` | 명령과 서비스 시작 | `raven web`의 기존 서버 연결·감독 프로세스 시작 |
| `raven/rpc/`, `raven/spine/` | 입력과 실행 순서 연결 | `turn.send`에서 요청을 검증하고 실행 레인에 제출 |
| `raven/agent/loop/` | 모델·도구 반복 | 문맥 준비, 도구 노출, 모델 호출, 결과 재투입 |
| `raven/agent/harness/` | 교체 가능한 전략 | Memory·Planning·Capability·Action 기본 구현 |
| `raven/agent/subagent/` | 위임과 그래프 실행 | 명부, 구조 검증, 의존성, 파일, 판정 |
| `agents/` | 전문 에이전트 정의 | 역할별 모델·도구·플러그인 설정 |
| `evolver/`, `experimental/curator/` | 하네스 개선 도구 | 통계 게이트와 생성·검증·설치 경로의 일부 |

전체 레포에는 WebUI·TUI, 채널 어댑터, 지식 검색, 메모리 플러그인, 샌드박스도 있습니다. 따라서 `raven/`만 있으면 모든 주변 서비스가 자동으로 준비되는 구조로 이해해서는 안 됩니다. 매니페스트에도 채널·브라우저·샌드박스 관련 선택 의존성이 나뉘어 있습니다. [디렉터리 설명](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/docs-site/docs/repo-layout.md#L1), [의존성 선언](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/pyproject.toml#L18)

## 작동 원리: 한 요청이 결과가 되는 과정

### 1. 시작 명령과 요청 접수는 서로 다른 단계입니다

콘솔 명령 `raven`은 `raven.cli.commands:run`에 연결됩니다. `raven web`은 이미 응답하는 게이트웨이가 있으면 연결하고, 그렇지 않으면 감독 프로세스를 시작하여 게이트웨이에 연결될 때까지 기다립니다. WebUI 빌드가 없으면 종료하는 검사도 있습니다. 즉 브라우저 화면을 여는 행위와 모델 작업을 수행하는 런타임은 분리되어 있습니다. [콘솔 진입점](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/pyproject.toml#L162), [WebUI 시작 경로](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/raven/cli/serve_commands.py#L1335)

사용자 메시지는 RPC의 `turn.send`에서 `TurnSendParams`로 검증됩니다. 모델 사용 가능성을 먼저 확인한 뒤, 메시지·첨부·출처·대화 식별자를 `TurnRequest`에 담아 scheduler에 제출합니다. 호스트 대화와 특정 서브에이전트 인스턴스의 직접 대화는 서로 다른 실행 레인을 사용합니다. 그러므로 호스트가 일하는 중에 다른 인스턴스가 대화할 수 있어도, 같은 인스턴스에 중복 작업을 무제한 투입한다는 뜻은 아닙니다. [요청 검증과 제출](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/raven/rpc/methods/turn.py#L410)

이 계층을 읽으면 `accepted` 응답을 작업 성공으로 해석하면 안 되는 이유가 드러납니다. 접수 결과와 실제 스트리밍·완료·오류 이벤트가 별도로 전달되기 때문입니다. 문서 역시 위임 영수증이나 준비 상태만으로 완료를 판단하지 말고 실제 파일·결과를 확인하도록 설명합니다. [협업 결과 확인](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/docs-site/docs/agent-collaboration.md#L8)

### 2. 하네스 네 모듈은 네 개의 모델을 뜻하지 않습니다

호스트 루프는 세션 모델 선택 또는 라우팅을 거쳐 문맥을 조립하고 `Planning.prepare`를 호출합니다. 이후 반복마다 문맥 크기를 조정하고 도구를 선택한 다음 모델 응답을 받습니다. [턴 시작](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/raven/agent/loop/turn_path.py#L2320), [반복의 문맥·도구 처리](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/raven/agent/loop/turn_path.py#L974)

| 모듈 | 기본 구현에서 확인한 역할 | 잘못 이해하기 쉬운 지점 |
| --- | --- | --- |
| Memory | 문맥 엔진에 조립을 위임하고 입력·출력 토큰 여유 및 축소를 관리 | 장기 메모리 데이터베이스 하나만 뜻하지 않습니다. |
| Planning | 입력 메시지를 그대로 반환하고 반복 중 조언을 조합 | 기본적으로 추가 전역 계획 모델을 호출하지 않습니다. |
| Capability | 현재 도구 레지스트리가 제공하는 정의를 선택 | 등록된 모든 도구를 항상 노출하는 것은 아닙니다. |
| Action | 스트리밍 또는 재시도 가능한 provider 호출로 다음 응답을 결정 | 구현을 바꿀 수 있는 전략 경계이며 기본값은 하나의 결정 경로입니다. |

근거: [Memory](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/raven/agent/harness/memory.py#L58), [Planning](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/raven/agent/harness/planning.py#L30), [Capability](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/raven/agent/harness/capability.py#L29), [Action](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/raven/agent/harness/action.py#L80).

다음은 기본 Planning 구현의 실제 코드입니다.

```python
async def prepare(self, request: PlanningRequest) -> PlanningResult:
    return PlanningResult(messages=request.messages)
```

[출처: `DefaultPlanning.prepare`](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/raven/agent/harness/planning.py#L33). 이 설계에서 계획은 주로 모델이 현재 문맥을 읽고 선택하는 행동에 나타납니다. README의 “Planning 모듈”을 매 요청 앞에 별도의 계획기가 고정 배치되어 있다는 뜻으로 읽으면 실제 코드와 달라집니다.

Action이 도구 호출을 반환하면 호스트는 ToolRegistry를 통해 실행하고 결과를 다음 모델 입력에 반영합니다. 레지스트리는 인자 검증과 실행 목적에 따른 거부 사유, 연결되어 있는 권한 게이트, 플러그인 게이트를 확인합니다. 코드에 이런 검사가 있다는 사실과 모든 외부 프로세스까지 동일하게 격리된다는 주장은 구분해야 합니다. [모델 호출](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/raven/agent/loop/turn_path.py#L1104), [도구 실행](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/raven/agent/loop/turn_path.py#L1377), [레지스트리의 실행 전 검사](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/raven/agent/tools/registry.py#L974)

### 3. 위임 대상은 공통 명부에서 해석합니다

`AgentRegistry.apply`는 발견한 전문 에이전트 정의, 패키지 기본 정의, 사용자 설정을 합칩니다. 이름별 행에는 실행 방식과 메타데이터가 들어가며, 외부 백엔드는 구성 시점에 만들어집니다. 잘못된 개별 항목은 경고와 함께 건너뛰어 전체 명부를 사용할 수 없게 만드는 상황을 피합니다. [명부 구성](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/raven/agent/subagent/registry.py#L280)

이때 에이전트 이름을 알고 있다는 것과 사용할 수 있다는 것은 다릅니다. 활성 명부에 존재해야 하고 설치·인증·도구 준비도 갖춰야 합니다. 코드에는 내부 Raven 루프, CLI, OpenAI 호환 백엔드가 같은 실행 계약 뒤에 놓이며 ACP 연결도 설정을 통해 구성됩니다. 이 덕분에 DAG 스케줄러는 모델 호출 방식보다 입력·출력·상태에 집중합니다. [백엔드 구성 설명](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/raven/agent/subagent/backends/__init__.py#L1), [연결 문서](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/docs-site/docs/agent-integrations.md#L9)

### 4. DAG는 프롬프트에 그린 그림이 아니라 검증할 데이터입니다

DAG(Directed Acyclic Graph)는 방향이 있고 순환이 없는 의존성 그래프입니다. Raven의 `DagNodeSpec`에는 `id`, `subagent`, `prompt_template`, `depends_on`, `skills`, `mcps`, `inputs`, `instance` 등이 있습니다. `id`는 작업과 산출물을 가리키며, `instance`는 이어서 대화할 실행 인스턴스를 가리킵니다. 둘을 같은 값의 별칭으로 이해해서는 안 됩니다. [노드 정의](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/raven/agent/subagent/dag_graph.py#L43)

`run_subagent_dag` 도구는 제출된 노드를 파싱합니다. 구조 검증은 식별자 중복, 존재하지 않는 의존성, 선언하지 않은 상위 노드 출력 참조, 입력 계약, 순환을 검사합니다. 순환 검출에는 Kahn 방식의 위상 정렬이 쓰입니다. 실제 백엔드 해석도 수행하므로 등록되지 않은 에이전트를 이름만 써서 실행할 수 없습니다. [도구 파싱](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/raven/agent/subagent/dag_tool.py#L1531), [구조 검증](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/raven/agent/subagent/dag_graph.py#L292), [위상 정렬](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/raven/agent/subagent/dag_graph.py#L610), [백엔드 확인](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/raven/agent/subagent/dag_runner.py#L404)

![Raven DAG의 구조 검증, 실행 가능 노드 선택, 결과 판정 및 기록 흐름]({{ '/img/reviews/2026/raven-review/dag.svg' | relative_url }})

*리뷰어 작성, 분석 커밋 기준. [ready 조건](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/raven/agent/subagent/dag_runner.py#L558)과 [출력 저장·판정](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/raven/agent/subagent/dag_runner.py#L1766)을 중심으로 정리했습니다. “판정”은 `judge_node`가 전달된 경로를 뜻하며, 모든 호출에 별도 판정기가 필수라는 의미는 아닙니다.*

### 5. 실행 순서는 의존성 완료와 판정 확정을 함께 봅니다

스케줄러가 다음 노드를 선택하는 실제 조건은 다음과 같습니다.

```python
ready = [
    nid
    for nid, st in status.items()
    if st == "pending"
    and nid not in carried_ids
    and all(status[d] == "completed" and d not in unsettled for d in deps[nid])
]
```

[출처: `run_dag`의 ready 선택](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/raven/agent/subagent/dag_runner.py#L558). 이미 실행 중인 작업이 다음 반복에서 재선택되지 않도록 `carried_ids`를 제외합니다. 더 중요한 부분은 `unsettled`입니다. 백엔드가 문자열을 반환하여 일단 완료로 표시했더라도, 판정이 끝나지 않았다면 하위 작업은 그 결과를 소비하지 않습니다.

실행 가능한 작업에는 세마포어로 동시성 제한을 적용합니다. `run_dag` 함수의 기본 `max_concurrency`는 5지만, 호출자가 별도 세마포어를 전달할 수도 있어 시스템 전체의 고정 병렬 수로 일반화해서는 안 됩니다. 동일 대화 인스턴스의 상태를 읽고 저장하는 구간에는 별도 handle lock도 적용됩니다. **작업 병렬성 제한과 같은 인스턴스의 기록 일관성 보호가 다른 문제**라는 점이 코드에 드러납니다. [함수 인자](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/raven/agent/subagent/dag_runner.py#L252), [노드 실행](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/raven/agent/subagent/dag_runner.py#L1587), [인스턴스 잠금](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/raven/agent/subagent/dag_runner.py#L1700)

### 6. 입력과 결과는 파일을 통해 전달됩니다

노드가 실행되기 전 `render_prompt`가 입력 템플릿과 참조를 해석합니다. 최초 렌더링 프롬프트와 시도별 프롬프트를 저장하고, 백엔드에 작업 폴더·세션·인스턴스·모델 관련 값을 전달합니다. 재시도에서는 인스턴스가 있는 경우 후속 지시를 이어 붙일 수 있고, 상태 없는 경우에는 이전 결과를 포함해 다시 설명합니다. [프롬프트 준비](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/raven/agent/subagent/dag_runner.py#L1628), [백엔드 호출](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/raven/agent/subagent/dag_runner.py#L1725)

여기에는 서로 다른 세 경로가 있습니다. `workdir`는 실제 사용자 작업 폴더이고, `run_root`는 해당 실행의 그래프·manifest를 보관하며, `nodes_root`는 노드별 프롬프트와 출력을 보관합니다. 이 구분 덕분에 작업 폴더와 실행 근거를 섞지 않고 이전 완료 노드를 다음 그래프에서 참조할 수 있습니다. 노드 식별자도 한 그래프 안뿐 아니라 세션 범위에서 중복을 검사합니다. [저장 경로와 참조 경계](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/raven/agent/subagent/dag_runner.py#L291)

성공 결과는 출력 파일과 시도별 기록에 저장됩니다. 이어 transcript를 기록한 뒤, `judge_node`가 있으면 판정을 적용합니다. 실패는 별도 오류로 남고, 마지막 `_finalize`는 노드 상태·시각·프롬프트 경로·출력 경로·오류를 manifest에 정리합니다. 화면의 스트리밍 로그와 다음 에이전트가 읽을 파일이 함께 존재하지만, 둘은 용도가 다릅니다. [결과 저장과 판정](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/raven/agent/subagent/dag_runner.py#L1766), [최종 manifest](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/raven/agent/subagent/dag_runner.py#L1955)

리뷰어 관점에서 이 구조의 학습 가치는 **“말로 끝났다고 하는 것”과 “다음 작업이 소비해도 되는 결과”를 분리하는 데** 있습니다. 다만 파일과 상태를 남기는 장치가 결과 내용의 진실성을 자동으로 보증하지는 않습니다. 판정 기준과 실제 산출물 검토가 여전히 필요합니다.

## 자기 개선: 실행 루프와 개선 도구를 구분하기

README는 하네스 네 모듈을 바꾸는 Curator와 벤치마크 기반 Evolver를 설명합니다. 그러나 설치 후 모든 대화가 자동으로 소스 코드를 진화시키는 하나의 기능으로 합쳐 읽으면 안 됩니다. README는 Evolver를 Raven을 라이브러리로 사용하는 별도 도구로 설명하고, Curator는 설치 패키지가 아닌 레포에 포함되는 실험 기능이라고 명시합니다. [개선 기능의 소개](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/README.md#L124), [Runtime Self-Evolution](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/README.md#L188)

Curator의 생성 코드는 이해·선택·설계·구현·수리 단계를 불러오며 모델 호출, 조회, 수리, 검사 횟수에 상한을 둡니다. workflow는 `worker.check`를 검증 콜백으로 전달하고, 생성 결과 및 작업공간 검사를 거쳐 설치 경로에서는 `worker.install`을 호출합니다. 이는 코드에서 확인한 생성·검증·설치 흐름이며, 특정 사용자 환경에서 성능이 향상되었다는 증거는 아닙니다. [생성 제한](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/experimental/curator/generation/run.py#L25), [검증 콜백](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/experimental/curator/workflow.py#L127), [설치 경로](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/experimental/curator/workflow.py#L232)

Evolver는 실패 궤적을 진단하고 패치를 만들며, 작은 평가에서 후보를 걸러낸 후 확인 평가와 게이트를 적용하는 별도 프로그램입니다. README에는 이 트리의 은퇴가 계획되어 있고 파트너 확인을 기다린다는 상태 설명도 남아 있습니다. 따라서 현재 레포에 코드가 있다는 것과 장기적으로 유지될 공개 인터페이스라는 것은 구분해야 합니다. [Evolver의 범위와 상태](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/evolver/README.md#L1)

### “성능이 올랐다”와 “통계적으로 지지된다”는 별도 값입니다

`paired.py`에서 실제 반환값을 확인하면 다음 두 조건은 분리되어 있습니다.

```python
promoted = candidate_mean > control_mean  # navigator: banks on beating vanilla
credited_2sigma = z >= z_threshold
```

[출처: paired gate](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/evolver/orchestrator/gates/paired.py#L89). 첫 값은 같은 작업 집합에서 후보의 평균이 기준보다 높은지를 뜻하고, 두 번째는 작업별 성능 차이로 계산한 통계량이 설정 임계값을 넘는지를 뜻합니다. 이후 의미적 판단에서 다음 부모 후보로 선택되거나 가지치기될 수 있으므로 `promoted`를 사용자 런타임의 자동 배포 완료로 해석해서도 안 됩니다.

또한 gate pipeline은 인프라 실패 작업을 보고하되 분모에서 빼지 않으며, 실행 활성화 근거가 전달된 경우에는 실제 메커니즘이 작동한 작업으로 귀속 범위를 좁힙니다. 활성화 집합이 `None`이면 그 검사는 생략됩니다. 이 구현은 “모든 개선 후보가 반드시 통계적 유의성을 통과해야만 채택된다”는 단순 설명보다 조건부입니다. [게이트 계산](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/evolver/orchestrator/gates/pipeline.py#L57)

## 논문 성능 수치는 어떻게 읽어야 하나

보조 출처인 [Raven 논문 v1의 §7.3·Table 4](https://arxiv.org/html/2609.33439v1#S7.SS3)는 DeepSeek-V4-Flash를 공유한 DeepResearch Mixed에서 Raven-Research 76.5%, DeepSeek-Harness 68.9%, MiroFlow 67.2%의 정확도를 보고합니다. 문항당 평균 비용은 각각 0.0242, 0.0211, 0.0374달러입니다. 이는 저자 평가이며, 이 리뷰에서 재현한 수치나 현재 서비스 가격이 아닙니다.

같은 모델을 사용한 비교는 하네스 차이를 살펴보는 데 도움이 됩니다. 그러나 논문의 실험 설정과 이 커밋의 기본 설정을 동일시할 수는 없습니다. 예를 들어 현재 `agents/raven-research/config.json`에는 `openai/gpt-5.6-sol-pro`가 설정되어 있습니다. 이 설정으로 실행하면 위 표가 그대로 나온다는 뜻이 아닙니다. [Research 설정](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/agents/raven-research/config.json#L1)

## 설치와 사용: 처음에는 한 역할부터 확인하기

아래 명령은 분석 커밋의 문서에 실린 사용법이며 실행 검증한 절차가 아닙니다. Quick Start는 Linux·macOS·WSL2용 관리형 설치 명령을 제시합니다. 이 URL은 고정 SHA 설치가 아니라 공개 배포판 설치 경로입니다. 재현 관점에서는 본문의 분석 커밋과 나중에 설치되는 배포판의 차이를 기록해야 합니다. [Quick Start](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/docs-site/docs/quick-start.md#L7)

```bash
curl -fsSL https://raven.evermind.ai/install.sh | bash
```

설치 후 문서의 초기 설정과 시작 명령은 다음과 같습니다. 실행 예시를 압축해 나열했으며 명령 자체는 원문과 같습니다.

```bash
raven onboard
raven web
```

`onboard`는 모델 provider와 사용할 에이전트를 설정합니다. 문서상 로컬 페이지는 `http://127.0.0.1:18792`이고, WebUI의 **Settings > Model providers**에서도 provider를 구성할 수 있습니다. 중지는 `raven web --stop`입니다. [초기 설정과 실행](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/docs-site/docs/quick-start.md#L105)

처음부터 복잡한 그래프를 맡기기보다 문서의 읽기 전용 협업 절차를 확인할 수 있습니다. 작업 폴더를 지정하고, 준비된 Raven-Code에 공개 API를 수정 없이 검토하게 한 뒤, 하위 작업 결과와 파일 참조를 확인합니다. 후속 대화가 필요하면 상태를 유지하는 인스턴스를 사용합니다. 이는 문서가 제시한 사용 흐름이며 별도의 검증된 벤치마크 예제가 아닙니다. `spawn`과 `run_subagent_dag`는 셸 명령이 아니라 모델이 선택하는 도구라는 점도 중요합니다. [첫 협업 절차](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/docs-site/docs/agent-collaboration.md#L23)

서비스 배포는 같은 체크아웃의 Docker Compose 경로가 있습니다.

```bash
cd docker
docker compose up --build
```

문서는 WebUI에 `http://127.0.0.1:18793`으로 접속하고, 컨테이너의 `/data/.raven`을 `raven-data` 볼륨으로 유지한다고 설명합니다. 소스 개발에는 Python 3.12, uv, Node.js, npm이 필요합니다. 개인 로컬 사용과 서비스 배포는 포트·저장 경로·실행 수명주기가 다르므로 같은 시작 명령으로 취급하지 않아야 합니다. [Self-Hosting](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/docs-site/docs/self-hosting.md#L1)

## 적용할 수 있는 작업과 설계 관점

리뷰어 해석으로, 데이터과학 작업에서는 **자료 조사 → 코드 실험 → 시각화와 결과 정리**처럼 단계별 산출물이 있는 흐름에서 이 구조를 검토할 가치가 있습니다. Research가 출처를 가진 자료를 남기고, Code가 작업 폴더에서 분석을 수행하며, Design이 결과 표현을 맡는 식입니다. 이는 역할 문서를 바탕으로 한 활용 해석이며 해당 조합의 성공률을 측정한 결과는 아닙니다. [역할별 사용 경계](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/docs-site/docs/agent-integrations.md#L28)

이 경우 먼저 정할 것은 에이전트 수보다 산출물 계약입니다. 조사 결과의 파일 위치, 코드가 사용할 데이터, 완료 조건, 다음 노드가 참조할 결과를 분명히 하면 DAG의 의존성과 파일 기록이 의미를 갖습니다. 반대로 여러 작성자가 같은 폴더를 수정하면 병렬 실행이 곧 작업 격리를 뜻하지 않습니다. Raven의 협업 문서도 명시적 파일 소유권이나 별도 worktree를 요구하며, 공유 작업 폴더 안내를 파일시스템 잠금으로 간주하지 않습니다. [병렬 작업과 파일 경계](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/docs-site/docs/agent-collaboration.md#L111)

## 한계와 운영상 주의점

**현재 상태는 pre-alpha입니다.** README와 보안 정책은 빠른 인터페이스 변경 가능성과 기본 브랜치 우선 보안 수정 방침을 명시합니다. 설치 성공·모델 연결·각 전문 에이전트 준비·실제 작업 성공을 각각 구분해 확인할 필요가 있습니다. [README](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/README.md#L31), [보안 정책](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/SECURITY.md#L19)

**모든 실행 경로에 같은 격리가 적용되지는 않습니다.** DAG 코드 설명상 전달된 sandbox는 내부 Raven 루프 백엔드에서 사용할 수 있지만 외부 CLI·OpenAI 백엔드는 이를 동일하게 사용하지 않습니다. 분석 커밋의 Raven-Code 설정에는 `restrictToWorkspace: false`, sandbox `backend: none`도 들어 있습니다. 이는 구성 파일에서 확인한 값이며, 설치 이후의 사용자 설정과 실행 정책까지 같다고 가정할 수 없습니다. [DAG 실행 경계](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/raven/agent/subagent/dag_runner.py#L292), [Code 기본 설정](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/agents/raven-code/config.json#L26)

**자기 개선 평가에도 별도의 신뢰 경계가 있습니다.** Evolver 문서는 수정 경로 제한이 악의적인 공격자를 막는 보안 격리를 뜻하지 않으며, 평가 후보가 scorer와 같은 권한으로 실행되고 설계 작업공간도 파일시스템·네트워크 격리 환경이 아니라고 설명합니다. 평가 분모·활성화·통계 검사가 있어도 실행 보안과 평가 오염 방지를 완전히 해결한 것으로 해석하면 안 됩니다. [Evolver의 명시적 보안 경계](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/evolver/README.md#L193)

**장기 메모리와 비용은 구성 의존적입니다.** Research 설정에는 EverOS HTTP backend와 별도 주소가 들어 있습니다. 하위 에이전트 위임은 추가 모델 호출이나 외부 작업을 일으킬 수 있습니다. 따라서 “메모리 지원”이 모든 설치에서 동일한 기억 품질이나 무비용 실행을 보장한다는 뜻은 아닙니다. [Research 메모리 설정](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/agents/raven-research/config.json#L19), [위임 비용 설명](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/docs-site/docs/agent-collaboration.md#L20)

루트 라이선스는 Apache-2.0이며, `NOTICES.md`는 nanobot·hermes-agent·Ink 등에서 가져온 부분의 출처와 별도 고지 위치를 명시합니다. 이 글은 루트 라이선스와 고지 파일의 존재를 확인했으며 포함 자산 전체를 독립적으로 라이선스 감사하지는 않았습니다. [LICENSE](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/LICENSE#L1), [제삼자 고지](https://github.com/EverMind-AI/Raven/blob/3632e6040c7038a60ec418ce39ccae185c72c19f/NOTICES.md#L1)

## 이 글에서 다루지 못한 부분

WebUI·TUI의 화면 구현 전체, 각 채널 어댑터, A2A 프로토콜의 전체 수명주기, EverOS 내부 저장·검색, Skill Forge의 검색·진화 알고리즘, Design·PPT·Oncall 엔진, benchmark adapter와 전체 Evolver 검색 루프는 상세 분석 범위에 포함하지 않았습니다. Curator는 생성 제한과 검증·설치 연결을, Evolver는 문서와 paired gate 계산을 중심으로 읽었습니다. 레포 테스트 파일의 존재를 실행 성공의 근거로 사용하지 않았습니다.

## 결론

Raven에서 배울 핵심은 에이전트를 많이 호출하는 방식보다 **교체 가능한 실행 정책, 명시적 작업 의존성, 파일 기반 결과, 완료 판정의 경계**입니다. 호스트 루프는 모델과 도구를 연결하고, DAG 런타임은 언제 누구에게 무엇을 전달할지 관리합니다. 자기 개선은 이 실행 구조와 연결되는 별도 층이며, 후보 평균 향상·통계적 근거·실제 배포는 같은 사건이 아닙니다. 이 경계를 구분하면 README의 큰 비전을 현재 코드에서 확인되는 동작과 연결해 읽을 수 있습니다.
