---
type: "Guide"
title: "[가이드] Claude Agent SDK 입문: Claude Code 연동부터 첫 실행과 서비스 배포까지"
description: "Claude Agent SDK와 API·CLI·Managed Agents의 차이부터 Python 첫 실행, Claude Code 설정 재사용, 공식 Docker 서비스 예제와 운영 원칙까지 입문자의 순서로 설명합니다."
date: "2026-09-28"
tags:
  - "Claude"
  - "Anthropic"
  - "AI Agent"
  - "MCP"
  - "Python"
resource: "https://code.claude.com/docs/en/agent-sdk/overview"
generated:
  by: "process:blog-review"
  at: "2026-09-28T14:59:38+09:00"
sources:
  - id: "claude-agent-sdk-overview"
    resource: "https://code.claude.com/docs/en/agent-sdk/overview"
    title: "Agent SDK overview"
  - id: "claude-agent-sdk-python"
    resource: "https://github.com/anthropics/claude-agent-sdk-python/tree/36f95486ee9fc49d8ee1ed56811f07b5e8e23ac6"
    title: "Claude Agent SDK for Python"
  - id: "claude-agent-sdk-hosting"
    resource: "https://github.com/anthropics/claude-cookbooks/tree/813fbeec03cdedfda7808529438d1c7af71f26eb/claude_agent_sdk/hosting"
    title: "Hosting the research agent"
  - id: "claude-agent-sdk-demos"
    resource: "https://github.com/anthropics/claude-agent-sdk-demos/tree/826b268506a5f3707623c9e6140b200befcbebae"
    title: "Claude Agent SDK Demos"
status: "stable"
year: "2026"
analyzed_at: "2026-09-28"
visual_sources:
  - path: "img/reviews/2026/claude-agent-sdk-guide/agent-loop.svg"
    kind: "reviewer-diagram"
    source_url: "https://code.claude.com/docs/en/agent-sdk/hosting"
    caption: "위: 요청 경로 / 아래: 루프의 구성 요소와 결과 소비 — 단일 직선 호출이 아닙니다."
  - path: "img/reviews/2026/claude-agent-sdk-guide/service-flow.svg"
    kind: "reviewer-diagram"
    source_url: "https://code.claude.com/docs/en/agent-sdk/hosting"
    caption: "위: 작업 접수 / 아래: 실행과 결과 관리 — 큐·저장소·승인 흐름은 앱에서 구현합니다."
---

## Claude Agent SDK로 무엇을 만들 수 있을까요?

폴더를 읽고 문서를 정리하거나, 데이터 분석 결과를 검토하고 보고서를 만드는 일을 생각해 보겠습니다. 일반적인 채팅에서는 사람이 자료를 골라 전달하고 답변을 다시 파일로 옮깁니다. 에이전트 애플리케이션은 이 사이의 작업을 도구 호출로 수행합니다. **Claude Agent SDK는 Claude Code의 에이전트 실행 기능을 Python·TypeScript 프로그램에서 사용하도록 제공하는 개발 도구**입니다.

이 글은 SDK를 처음 접하는 개발자를 위한 가이드입니다. 개념을 이해한 뒤 Python으로 첫 요청을 보내고, 읽기 도구를 연결하고, 공식 Docker 예제로 HTTP 서비스의 형태를 확인합니다. 마지막에는 데이터과학·리서치·개발 자동화의 활용 방식을 살펴봅니다. 제품 기능은 **2026년 9월 28일 공식 문서 기준**이며, Python 실습의 패키지 기준은 **`claude-agent-sdk==0.2.160`**입니다. 이후 버전에서는 기본 설정과 API가 바뀔 수 있습니다.

먼저 네 가지 용어를 구분하면 뒤의 설명이 쉬워집니다.

| 용어 | 의미 | 문서 정리 작업에서의 예 |
| --- | --- | --- |
| 모델 | 주어진 문맥으로 다음 응답이나 도구 호출을 결정하는 부분 | 어떤 파일부터 읽을지 판단 |
| 도구 | 파일·명령·외부 시스템에 실제로 접근하는 기능 | `Read`로 문서 읽기 |
| 에이전트 루프 | 판단 → 도구 실행 → 결과 확인을 반복하는 과정 | 목차 확인 후 부족한 문서를 추가로 읽기 |
| 하네스(harness) | 루프가 일하도록 도구·권한·문맥·실행 상태를 관리하는 틀 | 허용된 파일 접근과 세션 진행 관리 |

SDK는 이 하네스를 앱에 넣는 수단입니다. 특정 업무의 요구사항이나 사용자 인증까지 자동으로 완성해 주는 서비스 템플릿은 아닙니다. [공식 개요](https://code.claude.com/docs/en/agent-sdk/overview)

## 1. Claude API, Claude Code, Agent SDK, Managed Agents의 차이

| 선택지 | 내가 직접 운영하는 부분 | 맞는 출발점 |
| --- | --- | --- |
| Client SDK / Messages API | API 호출과 업무 처리 코드. 필요한 경우 도구 실행 반복도 직접 구성 | 정해진 입력을 분류·추출·요약 |
| Claude Code CLI | 터미널의 작업 환경과 실행 명령 | 사람이 개발하거나 스크립트에서 단발성 작업 실행 |
| Agent SDK | SDK를 호출하는 앱, 실행 프로세스, 작업 디렉터리와 서비스 운영 | 여러 단계로 파일·도구를 다루는 자체 앱 |
| Managed Agents | 앱의 요청·응답 처리와 에이전트 설정. 에이전트 루프는 Anthropic이 운영 | 직접 하네스 프로세스를 운영하는 부담을 줄이고 싶을 때 |

“고객 문의를 세 가지 라벨로 분류한다”는 문제에는 Client SDK로 충분할 수 있습니다. 반대로 “저장소를 조사하고 관련 파일을 찾아 근거를 정리한다”면 이미 도구와 반복 실행이 마련된 Agent SDK가 잘 맞습니다. 기능의 수보다 **문제 해결 순서를 코드가 고정할지, 모델이 도구 결과에 따라 선택할지**가 선택 기준입니다. 이는 이 글의 설계 판단이며 특정 제품의 성능 우위를 뜻하지 않습니다. [제품 비교](https://code.claude.com/docs/en/agent-sdk/overview)

Managed Agents의 `Agent`는 모델·지침·도구 설정이고, `Environment`는 실행 환경, `Session`은 실제 작업 실행, `Events`는 앱과 에이전트가 주고받는 메시지입니다. Agent와 Environment를 정의한 뒤 Session을 시작하고 Events를 보내 결과를 받는 구조입니다. 실행 환경은 관리형 클라우드 샌드박스와 자체 호스팅 샌드박스를 구분합니다. **Agent SDK로 만든 Python 서버를 그대로 업로드하면 Managed Agents가 되는 것은 아닙니다.** 서로 다른 실행·운영 인터페이스입니다. [Managed Agents 개요](https://platform.claude.com/docs/en/managed-agents/overview)

## 2. API로만 사용하나요? Claude Code와 연결되나요?

### 사용하는 입구와 모델 인증은 다른 문제입니다

SDK를 쓰기 위해 브라우저에서 REST 요청을 직접 작성할 필요는 없습니다. Python이나 TypeScript 함수를 호출하면 됩니다. 기존 터미널 자동화에는 `claude -p`도 사용할 수 있습니다. 다만 **SDK 프로세스가 내 컴퓨터에서 실행된다는 것과 모델까지 로컬·오프라인으로 실행된다는 것은 다릅니다.** 모델 추론에는 지원되는 Claude 서비스 연결이 필요합니다.

공식 빠른 시작은 Anthropic API 키를 환경 변수 `ANTHROPIC_API_KEY`로 전달합니다. Bedrock 등 지원되는 클라우드 제공자 경로도 있으므로 인증 방식이 이 키 한 가지로 제한되는 것은 아닙니다. `.env` 파일은 SDK가 자동으로 읽지 않으므로 실행 환경에서 주입하거나 별도로 로드해야 합니다. **Claude 구독 로그인과 서비스용 API 사용을 같은 결제·권한으로 가정하면 안 됩니다.** 공식 문서는 사전 승인 없이 제3자 제품에 claude.ai 로그인이나 그 사용 한도를 제공하는 방식을 허용하지 않는다고 명시합니다. 아래 실습과 배포 설명은 API 키 경로를 기준으로 합니다. [설치·인증 안내](https://code.claude.com/docs/en/agent-sdk/quickstart)

### Claude Code의 설정과 작업 방식을 재사용합니다

SDK는 Claude Code 실행 파일을 자식 프로세스로 구동합니다. 이미 열어 둔 터미널 창을 화면 조작하는 방식은 아닙니다. 같은 프로젝트의 지침·스킬·도구 구성을 재사용할 수 있다는 의미로 이해하면 됩니다. 대부분의 지원 설치 환경에서는 SDK에 실행 파일이 포함되지만, 소스 배포본이나 선택적 의존성을 생략한 설치에는 예외가 있습니다. [실행 구조](https://code.claude.com/docs/en/agent-sdk/hosting), [설치 예외](https://code.claude.com/docs/en/agent-sdk/quickstart)

현재 공식 문서에서는 `setting_sources`를 생략하면 사용자·프로젝트·로컬 설정을 읽는다고 설명합니다. 프로젝트 설정을 읽을지는 명시적으로 결정하는 편이 좋습니다.

| Python 설정 | 사용 의도 |
| --- | --- |
| `setting_sources=["project"]` | 신뢰하는 프로젝트의 규칙·스킬을 재사용 |
| `setting_sources=["user", "project"]` | 개인 Claude Code 설정과 프로젝트 설정을 함께 사용 |
| `setting_sources=[]` | 해당 파일 기반 설정을 빼고 코드에서 구성을 전달 |

`cwd`는 프로젝트 설정을 찾고 작업을 수행할 기준 디렉터리입니다. `CLAUDE.md`, `.claude/skills/`, `.claude/agents/` 등은 각 설정 로드 규칙을 따릅니다. 하지만 빈 `setting_sources`만으로 완전한 격리가 되지는 않습니다. 관리 정책, 전역 구성, 자동 메모리처럼 별도로 고려해야 하는 입력이 있습니다. 서버에서는 개인 홈 디렉터리를 공유하는 대신 작업·사용자별 환경을 분리해야 합니다. [Claude Code 기능 로드 규칙](https://code.claude.com/docs/en/agent-sdk/claude-code-features)

터미널에서 먼저 감을 잡고 싶다면 공식 문서의 비대화형 예제로 시작할 수 있습니다.

```bash
claude --bare -p "Summarize README.md" --allowedTools "Read"
```

이 명령은 현재 폴더의 README를 요약하도록 요청합니다. `--bare`는 자동 설정 탐색을 줄이는 모드이며 구독 로그인 대신 API 키 등 지원 인증을 준비해야 합니다. `--allowedTools`는 자동 승인 설정이지 OS 파일 접근을 격리하는 샌드박스가 아닙니다. CLI는 간단한 배치에, SDK는 앱 내부의 메시지 처리·승인 콜백·세션 관리에 적합합니다. [비대화형 CLI 공식 예제](https://code.claude.com/docs/en/headless)

## 3. Python으로 첫 실행 해보기

### 3.1 준비: 작은 실습 폴더와 API 키

Python 3.10 이상과 사용할 수 있는 Anthropic API 키를 준비합니다. macOS·Linux에서는 아래처럼 프로젝트와 가상환경을 만듭니다. Windows에서는 가상환경 활성화 명령을 `.venv\Scripts\Activate.ps1`로 바꿉니다. 다음 명령의 패키지 버전은 이 글의 검증 기준으로 고정했습니다.

```bash
mkdir my-agent
cd my-agent
python3 -m venv .venv
source .venv/bin/activate
pip install claude-agent-sdk==0.2.160
```

```bash
export ANTHROPIC_API_KEY=your-api-key
```

`your-api-key`를 실제 키로 바꿉니다. PowerShell에서는 `$env:ANTHROPIC_API_KEY="your-api-key"` 형태를 사용합니다. 키는 **같은 터미널의 환경 변수** `ANTHROPIC_API_KEY`에 설정합니다. 값에는 Console에서 발급한 실제 키가 필요하지만 코드·블로그·Git 저장소에는 넣지 않습니다. API를 호출하면 사용량에 따른 비용이 발생할 수 있으므로 Console에서 사용량도 확인합니다. 이 글은 API 호출의 실제 성공 결과나 소요 비용을 측정한 벤치마크가 아닙니다. [공식 빠른 시작](https://code.claude.com/docs/en/agent-sdk/quickstart)

### 3.2 첫 파일: 요청과 메시지 흐름 확인

`agent.py`를 만들고 아래를 저장합니다. [공식 Python SDK README의 Quick Start](https://github.com/anthropics/claude-agent-sdk-python/blob/36f95486ee9fc49d8ee1ed56811f07b5e8e23ac6/README.md)를 사용한 최소 예제입니다.

```python
import anyio
from claude_agent_sdk import query

async def main():
    async for message in query(prompt="What is 2 + 2?"):
        print(message)

anyio.run(main)
```

실행은 `python agent.py`입니다. 여기서 알아볼 것은 단순히 숫자 답변 하나가 아닙니다. `query()`가 메시지 스트림을 반환하며, `async for`가 실행 중 나오는 메시지를 차례로 받는다는 점입니다. `anyio.run(main)`은 이 비동기 함수를 시작합니다. 처음에는 원시 메시지 객체가 함께 출력되는 것이 정상입니다. 인증·네트워크가 실패하면 답변이 아니라 오류를 해결해야 합니다.

초기화 메시지에는 세션 정보가, assistant 메시지에는 응답이나 도구 사용 정보가, 최종 result에는 종료 상태가 담깁니다. **문자열이 출력되었다고 무조건 성공한 것은 아닙니다.** 앱에서는 최종 `ResultMessage`의 `subtype`을 확인하고 예외도 처리해야 합니다. [메시지와 루프](https://code.claude.com/docs/en/agent-sdk/agent-loop)

### 3.3 두 번째 실습: 사용할 도구 확인

처음부터 “프로젝트를 전부 개선해 줘”라고 요청하면 어떤 파일을 왜 바꾸었는지 추적하기 어렵습니다. 다음에는 공식 저장소의 **읽기 도구 목록을 지정하는 예제**를 확인하는 편이 좋습니다.

[공식 `tools_option.py`](https://github.com/anthropics/claude-agent-sdk-python/blob/36f95486ee9fc49d8ee1ed56811f07b5e8e23ac6/examples/tools_option.py)의 핵심 옵션은 다음과 같습니다.

```python
options = ClaudeAgentOptions(
    tools=["Read", "Glob", "Grep"],
    max_turns=1,
)
```

공식 파일에는 필요한 import, `query(..., options=options)`, 초기화 시 도구 목록 출력까지 들어 있습니다. 이 블록만 별도 파일로 실행하는 예제가 아니라 **완성된 공식 예제에서 설정 부분을 발췌**한 것입니다. 해당 파일의 `tools_array_example()`은 지정한 도구를 확인하고, 다른 함수는 도구 없음과 기본 도구 모음을 비교합니다.

`Read`는 파일 내용, `Glob`은 파일명 패턴, `Grep`은 파일 안의 문자열을 찾습니다. 이 차이를 확인한 다음에는 실습 폴더에 공개 문서만 넣고 “README의 핵심 기능과 확인이 필요한 설명을 정리해 달라”는 과제로 확장할 수 있습니다. 이 과제는 이 글의 연습 제안입니다. 실제 읽기·검색에는 한 번 이상의 도구 사용이 필요할 수 있으므로 `max_turns=1`은 도구 목록 확인용 제한으로 이해하고 업무 범위에 맞게 조정합니다.

`tools`와 `allowed_tools`는 구분해야 합니다. 전자는 제공할 기본 도구 구성을 지정하고, 후자는 지정 도구의 자동 승인을 다룹니다. `allowed_tools=["Read"]`만 적었다고 다른 모든 도구가 제거되지는 않습니다. 명시적으로 금지할 도구는 `disallowed_tools`, 매 호출의 업무 규칙은 권한 처리와 hook, 파일·네트워크 접근 경계는 실행 환경에서 다룹니다. [권한 평가 규칙](https://code.claude.com/docs/en/agent-sdk/permissions)

**검증 범위:** 본문의 Python 코드 구문·패키지 import·옵션 생성은 확인했습니다. 유료 모델 호출, 공식 Docker 이미지 실행, 공개 서비스 배포는 수행하지 않았습니다. 독자가 실제 키로 실행할 때의 응답·비용을 미리 성공한 결과처럼 제시하지 않습니다.

## 4. 실행 중에는 어떤 일이 일어나나요?

![사용자 요청에서 SDK와 Claude Code 실행 루프, 모델 및 도구를 거쳐 결과를 반환하는 구조]({{ '/img/reviews/2026/claude-agent-sdk-guide/agent-loop.svg' | relative_url }})

*공식 실행 구조를 바탕으로 이 글에서 재구성한 개념도입니다. 모델 호출과 도구 실행은 한 번으로 끝나지 않고 필요에 따라 반복됩니다.*

“관련 문서를 읽어 보고서를 만들어 달라”는 요청에서는 파일 검색 → 내용 읽기 → 추가 자료 확인 → 결과 작성 같은 순서가 나올 수 있습니다. 정확한 경로는 모델이 도구 결과에 따라 선택합니다. SDK는 이 반복을 구동하며 앱은 메시지를 받아 진행 상태를 표시하거나 최종 산출물을 저장합니다.

사용자에게는 “문서를 읽는 중”, “결과 검증 중”처럼 실제 이벤트에 근거한 상태를 보여 주는 것이 좋습니다. 일정 시간이 지났다는 이유만으로 진행률 90%를 만들어 내면 실패·정체를 숨길 수 있습니다. 최종 결과와 함께 세션 ID·종료 이유를 저장하면 후속 질문과 장애 조사도 쉬워집니다. [에이전트 루프와 결과 메시지](https://code.claude.com/docs/en/agent-sdk/agent-loop)

## 5. 기능별로 무엇이고, 언제 쓰나요?

### Skills와 CLAUDE.md: 작업 절차와 공통 문맥

`CLAUDE.md`는 프로젝트 규칙처럼 계속 참고할 문맥에 가깝습니다. Skill은 특정 작업에 필요한 지침·워크플로우를 묶습니다. 예를 들어 데이터 분석용 Skill에는 데이터 정의 확인, 누락값 확인, 평가 기준, 결과 보고 순서를 담을 수 있습니다. 필요한 지침을 재사용하므로 매번 긴 프롬프트를 복사하는 부담이 줄어듭니다.

Skill 파일을 만들었다고 반드시 모든 요청에서 그 절차가 실행되거나 권한이 확보되는 것은 아닙니다. SDK의 설정 로드·Skill 활성화·도구 구성까지 맞아야 합니다. “어떻게 조사할까”는 Skill, “어디까지 접근 가능한가”는 권한과 도구 계층의 문제입니다. [SDK의 Skills](https://code.claude.com/docs/en/agent-sdk/skills)

### Subagents: 독립적인 하위 작업 분담

Subagent는 특정 역할의 하위 에이전트입니다. 논문 원문 확인과 코드 구현 확인처럼 결과를 따로 검토할 수 있는 작업을 나눌 때 유용합니다. 정의에는 언제 사용할지 알려 주는 설명과 역할 지침을 넣고, 필요하면 도구도 제한합니다. 역할 이름만 다르게 붙인다고 전문성이 자동으로 생기지는 않습니다. 입력 범위·기대 결과·검증 기준을 함께 줘야 합니다.

처음에는 단일 에이전트로 완성한 업무를 나중에 분리하는 편이 관리하기 쉽습니다. 여러 에이전트가 동시에 같은 파일을 수정하면 충돌할 수 있으므로 파일 소유권을 분리하고 부모가 결과를 통합하는 구성을 권합니다. 이는 이 글의 운영 제안입니다. [Subagents 설정](https://code.claude.com/docs/en/agent-sdk/subagents)

### MCP: 외부 시스템을 도구로 연결

MCP(Model Context Protocol)는 에이전트가 외부 도구·데이터 소스와 연결하는 방식입니다. 문서 검색, 사내 지표 조회, 이슈 검색 같은 기능을 연결할 수 있습니다. SDK는 외부 MCP 서버와 연결하거나 앱 내부 함수를 도구로 제공하는 구성을 지원합니다.

데이터 분석 서비스라면 “모든 SQL을 자유롭게 실행”시키는 것보다 “지정된 지표의 기간별 값을 조회”하는 좁은 도구로 시작할 수 있습니다. 조회와 수정·발송 도구는 분리하고, 도구 서버 자체에서도 사용자 권한을 검사해야 합니다. MCP는 연결 규약이며 사내 권한 정책을 대신 정해 주지는 않습니다. [MCP 연결](https://code.claude.com/docs/en/agent-sdk/mcp)

### Hooks와 Permissions: 관찰 및 실행 통제

Hook은 도구 실행 전후 같은 시점에 호출되는 코드입니다. `PreToolUse`에서 실행 요청을 검사하고, `PostToolUse`에서 결과를 기록하는 식으로 활용합니다. 읽기 허용 폴더 밖의 접근을 차단하거나 도구 실패를 관찰하는 정책을 둘 수 있습니다. 공식 문서는 여러 권한 판단 hook이 함께 적용될 때 하나의 거부 결정이 호출을 막는다고 설명합니다. [Hooks](https://code.claude.com/docs/en/agent-sdk/hooks)

Permissions는 도구 사용을 허용·거부·승인 요청으로 처리하는 계층입니다. 사람이 지켜보는 CLI와 달리 서버에서는 승인을 받을 UI와 응답 경로를 앱이 준비해야 합니다. 그것이 없는데 승인을 기다리게 만들면 작업이 멈출 수 있습니다. 무조건 전체 권한을 우회하기보다 자동 실행해도 되는 작업과 검토 후 실행할 작업을 구분합니다. [Permissions](https://code.claude.com/docs/en/agent-sdk/permissions)

### Sessions와 Plugins: 이어서 작업하고 구성을 배포하기

Session은 일련의 대화·작업 문맥입니다. 이전 세션을 재개하면 후속 질문을 같은 맥락에서 처리할 수 있습니다. 하지만 세션 ID만 DB에 넣는다고 대화 기록과 생성 파일이 모두 보관되는 것은 아닙니다. 저장된 기록이 실제로 존재하고 현재 사용자에게 속하는지도 확인해야 합니다. [Sessions](https://code.claude.com/docs/en/agent-sdk/sessions)

Plugin은 Skills·에이전트·Hooks·MCP 구성 등을 묶는 배포 단위입니다. 개발자마다 파일을 따로 복사하는 대신 팀이 검토한 구성을 함께 전달하는 용도로 사용할 수 있습니다. SDK의 로컬 Plugin 경로는 실제 배포 환경에도 있어야 하며, 초기화 메시지로 로드 여부를 확인합니다. 설치 위치를 알고 있다는 것과 정상 로드되었다는 것은 다릅니다. [Plugins](https://code.claude.com/docs/en/agent-sdk/plugins)

## 6. 공식 Docker 예제로 HTTP 서비스 형태 확인하기

SDK를 설치한 것만으로 HTTP 서버가 생기지는 않습니다. **사용자 요청을 받는 서버가 SDK를 호출**해야 합니다. 공식 Cookbook의 [Hosting 예제](https://github.com/anthropics/claude-cookbooks/tree/813fbeec03cdedfda7808529438d1c7af71f26eb/claude_agent_sdk/hosting)는 이 부분을 FastAPI와 SSE로 보여 줍니다. SSE(Server-Sent Events)는 서버가 진행 메시지를 연결된 클라이언트에 순서대로 보내는 방식입니다.

### 6.1 저장소와 실행 파일 살펴보기

```bash
git clone https://github.com/anthropics/claude-cookbooks.git
cd claude-cookbooks
git checkout 813fbeec03cdedfda7808529438d1c7af71f26eb
```

공식 `anthropics/claude-cookbooks` 저장소를 내려받고 이 글이 확인한 커밋 **`813fbeec03cdedfda7808529438d1c7af71f26eb`**을 기준으로 `claude_agent_sdk/hosting/`을 살펴봅니다. Docker Desktop 또는 Docker Compose 사용 환경이 필요합니다.

| 파일 | 하는 일 |
| --- | --- |
| `server.py` | 메시지를 받아 SDK를 호출하고 이벤트를 반환하는 서버 |
| `run_once.py` | 한 번의 작업 후 종료하는 배치 실행 경로 |
| `Dockerfile` | 런타임과 의존성을 포함하는 이미지 정의 |
| `docker/docker-compose.yml` | 로컬 포트, 환경 파일, 세션 볼륨 연결 |
| `.env.example` | 실행에 필요한 환경 변수 예시 |

`hosting/.env.example`을 참고해 **`hosting/.env`**를 만들고 API 키를 넣습니다. Compose 파일이 읽는 위치이므로 폴더를 혼동하지 않아야 합니다. 이 파일은 공개 저장소에 커밋하지 않습니다. 다음 명령은 Cookbook의 로컬 Docker 안내에 있는 실행 경로입니다. 저장소 루트에서 시작합니다.

```bash
cd claude_agent_sdk/hosting/docker/
docker compose up --build
```

다른 터미널에서 `curl http://localhost:8000/health`로 서버 생존 여부를 확인합니다. 그다음 공식 예제 요청을 보냅니다.

```bash
curl -N -X POST http://localhost:8000/sessions/demo-1/messages \
  -H 'Content-Type: application/json' \
  -d '{"prompt":"What are the latest AI agent trends?"}'
```

`-N`은 curl의 출력 버퍼링을 끄는 옵션입니다. 경로의 `demo-1`은 이 데모에서 쓰는 세션 식별자입니다. 같은 경로에 후속 질문을 보내면 기존 대화를 이어가는 형태를 확인할 수 있습니다. `/health` 성공은 모델 인증이나 에이전트 작업 완료까지 보장하지 않으므로 실제 메시지 요청도 확인해야 합니다. [공식 Docker 안내와 Compose 파일](https://github.com/anthropics/claude-cookbooks/tree/813fbeec03cdedfda7808529438d1c7af71f26eb/claude_agent_sdk/hosting/docker)

### 6.2 이 서버가 해결하는 것과 아직 남은 것

공식 Compose는 포트를 `127.0.0.1`에 연결하고 `./sessions`를 `/data`에 마운트합니다. 로컬 확인과 세션 기록 보존의 기본 모습을 보여 줍니다. 서버는 `/sessions/{session_id}/messages`로 요청을 받고 `message`, `done`, `error` 이벤트를 보냅니다. **포트를 인터넷에 그대로 열어 서비스로 출시하는 예제는 아닙니다.**

공식 README는 앞단에서 인증하고 세션이 요청 사용자에게 속하는지 확인하는 게이트웨이를 요구합니다. 선택적인 `AGENT_AUTH_TOKEN`은 최소 인증 수단일 뿐 사용자별 세션 소유권 검사를 대신하지 않습니다. Docker·Modal·Kubernetes 예제는 컨테이너 실행을 점진적으로 확장하는 참고 자료이며, 회사의 계정·데이터·배포 정책을 별도로 연결해야 합니다. [Hosting 인터페이스와 제약](https://github.com/anthropics/claude-cookbooks/blob/813fbeec03cdedfda7808529438d1c7af71f26eb/claude_agent_sdk/hosting/README.md)

## 7. 실제 서비스로 배포할 때의 권장 구조

![클라이언트, 인증 API, 작업 큐, 격리된 SDK worker와 저장소를 분리한 서비스 설계]({{ '/img/reviews/2026/claude-agent-sdk-guide/service-flow.svg' | relative_url }})

*이 글의 서비스 설계 제안입니다. 작업 큐·DB·객체 저장소·승인 화면은 SDK가 자동으로 제공하는 기능이 아니라 서비스에서 구성할 요소입니다.*

짧은 개인 도구는 요청을 받아 바로 실행해도 됩니다. 여러 사용자의 긴 작업을 처리하려면 아래처럼 책임을 나누는 편이 실패 복구와 진행 표시를 설계하기 쉽습니다.

1. **API 서버**가 사용자 인증·입력 크기·작업 권한을 확인하고 작업 ID를 만듭니다.
2. **작업 큐**가 실행 요청을 보관합니다. API 연결이 끊겨도 요청을 잃지 않도록 합니다.
3. **Worker**가 분리된 작업 공간에서 SDK를 호출합니다. 동시 실행 수를 제한합니다.
4. **상태 저장소**에는 요청자·작업 상태·세션 ID·오류·사용량을, **산출물 저장소**에는 보고서와 파일을 보관합니다.
5. 클라이언트는 작업 ID로 진행 상황과 결과를 받습니다. 게시·발송·병합처럼 외부 상태를 바꾸는 단계에는 필요한 승인 절차를 붙입니다.

이 흐름은 공식 예제의 필수 구현 목록이 아니라 이 글이 권하는 서비스 구성입니다. 실제 배포 플랫폼을 선택할 때는 컨테이너 실행, 자식 프로세스, 쓰기 가능한 작업 공간, 긴 연결 또는 비동기 작업 처리가 가능한지 확인합니다. 짧은 HTTP 요청만 전제로 하는 환경에 긴 에이전트 작업을 그대로 넣으면 실행 시간 제한과 파일 소실 문제가 생길 수 있습니다.

공식 호스팅 문서는 작업마다 생성·종료하는 방식, 장시간 유지하는 방식, 기록을 복원하며 필요할 때만 실행하는 방식을 구분합니다. 처음에는 로컬 Docker로 시작하고, 여러 사용자 또는 반복 작업이 생기면 관리형 컨테이너 환경을 검토하는 순서가 현실적입니다. Kubernetes는 기존 운영 기반이나 격리·확장 요구가 있을 때 선택할 수 있습니다. [호스팅 패턴](https://code.claude.com/docs/en/agent-sdk/hosting)

## 8. Best Practices: 동작하는 데모에서 운영 가능한 서비스로

### 작업 공간과 권한을 분리합니다

모델에게 “중요한 파일은 건드리지 마”라고 말하는 것만으로 접근 경계가 생기지는 않습니다. 읽기 중심 작업에는 읽기용 입력을 주고, 사용자별 디렉터리와 자격 증명을 분리합니다. 컨테이너 역시 설정에 따라 격리 강도가 달라지므로 권한·마운트·네트워크를 함께 검토해야 합니다. `cwd`를 바꾸는 것만으로 OS 수준 접근이 차단되지는 않습니다. [안전한 배포](https://code.claude.com/docs/en/agent-sdk/secure-deployment)

### 비용·시간·동시 실행을 각각 제어합니다

`max_turns`는 도구 사용 반복의 한도이지 경과 시간 타이머가 아닙니다. 비용 한도, worker 실행 시간, 동시 실행 수는 별개로 정합니다. 비용 추정값은 서비스에서 사용량을 관찰하는 데 활용하되 실제 청구 내역과 구분합니다. 실패한 작업에서도 이미 사용한 모델 비용은 발생할 수 있습니다. Subagent를 추가하면 동시에 처리할 수 있는 범위가 늘지만 비용과 rate limit 부담도 늘 수 있습니다. [비용 추적](https://code.claude.com/docs/en/agent-sdk/cost-tracking), [실행 한도](https://code.claude.com/docs/en/agent-sdk/agent-loop)

### 형식 검증과 사실 검증을 분리합니다

Structured output은 JSON Schema에 맞는 결과를 받는 데 도움이 됩니다. 그러나 `{"accuracy": 0.95}`가 올바른 JSON이라고 해서 정확도 95%가 실제 측정값이 되는 것은 아닙니다. 서비스에서는 스키마 검증 뒤에 데이터 범위·출처·실험 로그 대조를 둡니다. 문서 자동화라면 인용 링크와 원문, 데이터 분석이라면 사용한 데이터 버전과 계산 결과를 함께 보관하는 방식이 좋습니다. [Structured output](https://code.claude.com/docs/en/agent-sdk/structured-outputs)

### 대화 복구와 파일 복구는 별도로 확인합니다

세션을 재개할 수 있어도 이전 컨테이너가 만든 결과 파일이 사라졌다면 작업 전체가 복구된 것은 아닙니다. 입력 버전·작업 디렉터리 산출물·대화 기록을 각각 저장하고 재시작을 시험합니다. SDK의 세션 재개 기능과 서비스의 영속 저장 책임을 함께 설계해야 합니다. [Sessions](https://code.claude.com/docs/en/agent-sdk/sessions)

### 외부 변경은 중복 실행을 고려합니다

아래는 이 글의 운영 권장사항입니다. 작업을 재시도할 때 보고서 저장·PR 생성·이메일 발송이 두 번 실행되지 않도록 업무 키와 완료 상태를 둡니다. “초안 작성 성공”과 “외부 발송 성공”을 별도 단계로 기록하면 모델 호출만 다시 해야 하는지, 발송 결과를 조회해야 하는지 판단하기 쉬워집니다. 배포와 병합 권한을 분석 worker에 한꺼번에 주는 대신 검증된 결과를 승인 후 반영하는 경로로 분리할 수 있습니다.

## 9. 어떤 업무부터 적용하면 좋을까요?

다음 표는 이 글의 **활용 설계 예시**입니다. 실제 도입 기업의 성과나 검증된 자동화 정확도를 뜻하지 않습니다.

| 업무 | 입력과 도구 | 에이전트가 맡을 일 | 사람이 검토할 지점 |
| --- | --- | --- | --- |
| 데이터 품질 보고서 | 데이터 사전, 프로파일링 결과, 읽기 전용 조회 | 누락·분포 변화의 근거를 정리 | 이상 원인 해석과 조치 결정 |
| 실험 결과 리뷰 | 지표 JSON, 설정, 학습 로그 | 조건이 같은 실험을 묶고 차이를 설명 | 누수·평가 설계·통계적 결론 |
| 논문·레포 리서치 | 고정 원문, 코드, 출처 목록 | 자료별 분석과 근거 있는 초안 | 주장·수식·수치 확인 및 발행 |
| 이슈 조사 | 오류 로그, 관련 소스, 테스트 결과 | 재현 경로와 수정안 제시 | 코드 적용과 병합 |
| 고객 지원 초안 | 티켓, 문서 검색 MCP | 근거 문서를 찾아 답변 초안 | 환불·계정 변경·민감 답변 |

데이터과학자의 첫 과제로는 **이미 계산된 실험 지표와 설정 파일을 읽고 비교 보고서를 만드는 작업**을 권합니다. 모델이 임의로 통계 값을 추정하도록 맡기지 않고, 기존 계산 결과를 근거로 설명하게 만들 수 있기 때문입니다. 입력을 공개·샘플 데이터로 제한하면 접근 권한 설계도 단순해집니다.

그다음 단계에서 문서 검색 MCP를 추가하거나, 실험 조건 확인과 결과 해석을 Subagent로 나눌 수 있습니다. 처음부터 여러 에이전트와 모든 외부 도구를 붙이기보다, **입력·산출물·성공 기준이 분명한 한 작업**이 반복해서 잘 되는지 먼저 확인하는 편이 좋습니다.

공식 데모 저장소에는 이메일, Excel, 리서치, 채팅 UI 등의 예제가 있습니다. 사용 장면을 이해하는 참고 자료로는 유용하지만, 저장소가 로컬 개발용이라고 명시하므로 그대로 운영 환경에 배포하는 기준으로 삼으면 안 됩니다. 데모에는 이전 API를 보여 주는 디렉터리도 있어 현재 SDK 문서와 버전을 대조해야 합니다. [공식 데모 모음](https://github.com/anthropics/claude-agent-sdk-demos/tree/826b268506a5f3707623c9e6140b200befcbebae)

## 10. 처음 실행할 때 자주 막히는 부분

| 증상 | 먼저 확인할 것 |
| --- | --- |
| 인증 오류 | 실행한 터미널·컨테이너에 API 키가 전달되었는지, 실제 사용할 수 있는 키인지 |
| `.env`를 만들었는데 키를 못 찾음 | SDK는 자동 로드하지 않음. 실행 환경 또는 Compose의 `env_file` 경로 확인 |
| Claude 실행 파일을 찾지 못함 | 플랫폼에 맞는 패키지·실행 파일이 설치되었는지, 배포 환경의 경로와 실행 권한 확인 |
| Skill이나 규칙이 적용되지 않음 | `cwd`, `setting_sources`, Skill 활성화·로드 상태 확인 |
| 서버가 계속 기다림 | 승인 요청, 도구 오류, 실행 한도와 앱의 시간 제한 확인 |
| 재시작 후 후속 질문을 이해하지 못함 | 세션 ID와 기록 저장소·볼륨·사용자 매핑 확인 |

인증과 실행 파일 문제는 [공식 Troubleshooting](https://code.claude.com/docs/en/agent-sdk/troubleshooting), 설정 문제는 [기능 로드 문서](https://code.claude.com/docs/en/agent-sdk/claude-code-features), 서버 문제는 [호스팅 안내](https://code.claude.com/docs/en/agent-sdk/hosting)를 기준으로 점검합니다. 이 글에서 실행 성공 여부를 확인하지 않은 환경에 대한 해결을 보장하는 표는 아닙니다.

## 정리

Claude Agent SDK는 Claude Code의 작업 실행 능력을 프로그램 안에서 사용하게 해 줍니다. Python의 첫 요청으로 메시지 흐름을 확인하고, 읽기 도구가 있는 작은 업무를 만든 뒤, 공식 서버 예제로 HTTP 요청·세션·스트리밍의 연결을 살펴볼 수 있습니다.

서비스로 발전시키는 핵심은 모델을 호출하는 코드보다 **사용자 권한, 작업 경계, 결과 검증, 복구 가능한 상태**를 명확히 하는 데 있습니다. SDK가 맡는 에이전트 실행과 애플리케이션이 맡는 운영 책임을 구분하면, 개인 자동화에서 팀의 업무 도구로 확장할 범위도 판단하기 쉬워집니다.

## 출처와 코드 이용 안내

기능 설명의 각 절에 공식 문서를 연결했습니다. 추가 조사에는 [Python SDK 고정 커밋](https://github.com/anthropics/claude-agent-sdk-python/tree/36f95486ee9fc49d8ee1ed56811f07b5e8e23ac6), [공식 Cookbook 고정 커밋](https://github.com/anthropics/claude-cookbooks/tree/813fbeec03cdedfda7808529438d1c7af71f26eb), [공식 데모 고정 커밋](https://github.com/anthropics/claude-agent-sdk-demos/tree/826b268506a5f3707623c9e6140b200befcbebae)을 사용했습니다. 동적으로 갱신되는 문서와 고정한 예제 코드의 차이가 생기면 해당 버전의 변경 로그를 함께 확인해야 합니다.

인용한 Python SDK 및 Cookbook 예제는 Anthropic의 MIT 라이선스 코드입니다. [Python SDK 라이선스](https://github.com/anthropics/claude-agent-sdk-python/blob/36f95486ee9fc49d8ee1ed56811f07b5e8e23ac6/LICENSE), [Cookbook 라이선스](https://github.com/anthropics/claude-cookbooks/blob/813fbeec03cdedfda7808529438d1c7af71f26eb/LICENSE)를 따르며, 코드 재배포 시 원저작권과 라이선스 고지를 보존합니다. SVG 두 장은 공식 구조와 이 글의 설계 제안을 설명하기 위해 새로 작성한 도식입니다.
