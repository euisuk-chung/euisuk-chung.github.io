---
title: "[구글] Defying Gravity~ 구글 Antigravity 어서오고👋"
date: "2025-11-25"
tags:
  - "google"
year: "2025"
---

# [구글] Defying Gravity~ 구글 Antigravity 어서오고👋

![](https://velog.velcdn.com/images/euisuk-chung/post/6df06472-148f-4244-bad6-19360ccffeec/image.png)

> <https://antigravity.google/>

서론: AI 기반 소프트웨어 개발의 새로운 시대
--------------------------

소프트웨어 개발 환경은 빠르게 진화하고 있습니다. 불과 몇 년 전만 해도 IDE(Integrated Development Environment)는 단순히 코드를 작성하고 디버깅하는 도구에 불과했습니다. 하지만 대규모 언어 모델(Large Language Model)의 등장과 함께, 개발자들은 AI 어시스턴트와 협업하는 새로운 개발 방식을 경험하게 되었습니다.

Google은 자사의 최신 모델인 **Gemini 3**의 에이전틱 코딩(Agentic Coding) 역량을 극대화하기 위해, 완전히 새로운 개발 플랫폼 **Google Antigravity**를 공개했습니다. "Experience liftoff"라는 슬로건처럼, Antigravity는 아이디어만 있으면 누구나 소프트웨어 개발의 이륙(liftoff)을 경험할 수 있도록 설계되었습니다.

> **Google Antigravity**는 IDE를 에이전트 중심 시대로 진화시키는 에이전틱 개발 플랫폼(Agentic Development Platform)입니다. 개발자가 워크스페이스 전반에서 에이전트를 관리하며 더 높은 태스크 지향적 수준에서 작업할 수 있게 하면서도, 핵심에는 친숙한 AI IDE 경험을 유지합니다.

이 글에서는 Antigravity의 핵심 철학, 주요 기능, 그리고 개발자 워크플로우에 미칠 영향을 심층적으로 살펴보겠습니다.

---

Antigravity가 등장한 배경
-------------------

### 기존 AI 코딩 도구의 한계

현재 시장에 존재하는 AI 코딩 도구들은 대부분 두 가지 극단 중 하나에 위치합니다:

1. **과도한 투명성**: 에이전트가 수행하는 모든 도구 호출(tool call)과 액션을 사용자에게 노출하여, 정보 과부하를 유발합니다.
2. **과도한 추상화**: 최종 코드 변경 사항만 보여주고, 에이전트가 어떻게 그 결과에 도달했는지에 대한 맥락이 전혀 없습니다.

두 접근 방식 모두 사용자가 에이전트의 작업을 **신뢰(Trust)**하기 어렵게 만든다는 공통된 문제를 가지고 있습니다.

### Gemini 3와 에이전틱 인텔리전스의 도약

Gemini 3와 같은 최신 모델들은 사용자의 개입 없이도 장시간 동안 여러 표면(surface)에서 작업을 수행할 수 있는 수준에 도달했습니다. 이는 개발자가 개별 프롬프트나 도구 호출 단위가 아닌, **더 높은 수준의 추상화**로 에이전트와 상호작용해야 함을 의미합니다.

### Windsurf 팀 영입의 결실

Google은 약 4개월 전, Windsurf의 CEO와 팀원들을 약 24억 달러(한화 약 3조 원 이상)를 투입하여 영입했습니다. Antigravity는 바로 이 영입의 결과물로, Google이 공개하는 **최초의 자체 IDE**입니다. 기존 Cursor, Windsurf 등의 경험을 흡수하면서도, Google만의 강점인 브라우저 제어와 이미지 생성 역량을 결합한 것이 특징입니다.

---

핵심 용어 정리
--------

Antigravity를 이해하기 위해 먼저 핵심 용어들을 정리하겠습니다:

* **Agent** : Antigravity의 핵심 AI 모달리티. Editor 내에서 긴밀하게 작업하거나, Agent Manager를 통해 여러 코드베이스에서 다수의 에이전트를 오케스트레이션하고 모니터링할 수 있습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/cd06fc5e-2010-4723-8f44-9b578b2bff77/image.png)

> Agent, <https://antigravity.google/product>

![](https://velog.velcdn.com/images/euisuk-chung/post/3a36e189-7373-4f03-b67d-5ccd64ba1195/image.png)

> Editor, <https://antigravity.google/product>

* **Artifacts** : 에이전트가 작업을 수행하거나 사용자에게 성과를 전달하기 위해 생성하는 모든 산출물. 리치 마크다운 파일, diff 뷰, 아키텍처 다이어그램, 이미지, 브라우저 녹화 등이 포함됩니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/c13d5d91-3b30-4315-9c76-fa577089943c/image.png)

> <https://antigravity.google/product>

* **Tab** : 텍스트 에디터 내의 AI 모달리티로, 더 강력한 "자동완성" 기능입니다.
* **Command** : 인라인 지시형 AI 모달리티로, 자연어로 코드 작성을 명령할 수 있습니다.

---

Antigravity의 주요 기능
------------------

### 1. AI-powered IDE: 익숙하면서도 강력한 개발 환경

Antigravity의 **Editor View**는 Visual Studio Code를 기반으로 하여, Cursor나 Windsurf를 사용해본 개발자라면 별도의 학습 없이 바로 적응할 수 있습니다. 기존 VS Code 익스텐션도 그대로 사용할 수 있어, Claude Code 익스텐션 등 선호하는 도구를 함께 활용할 수 있습니다. 특히 Vim 지원이 잘 되어 있어, Vim 사용자들에게 반가운 소식입니다.

| 기능 | 설명 | 활용도 |
| --- | --- | --- |
| **Agent** | 다단계 추론 시스템으로, 기존 코드를 분석하고 다양한 도구를 사용하며 태스크와 Artifact를 통해 사용자와 소통 | 가장 높음 |
| **Tab** | 컨텍스트 인식 지능형 코드 자동완성 | 보조적 |
| **Command** | 자연어 인라인 코드 작성 명령 | 보조적 |

Agent는 Frontier LLM 기반의 **다단계 추론 시스템(Multi-step Reasoning System)**으로, 다음과 같은 핵심 구성요소를 갖추고 있습니다:

* **Reasoning Model**: 복잡한 문제를 단계별로 분해하고 해결
* **Tools**: 에디터, 터미널, 브라우저 등 다양한 도구 활용
* **Artifacts**: 작업 결과물 생성 및 커뮤니케이션
* **Knowledge**: 과거 작업에서 학습한 지식 베이스

### 2. Agent Manager: 병렬 작업의 혁신

Antigravity에서 가장 혁신적인 기능은 **Agent Manager**입니다. 상단의 "Open Agent Manager" 버튼을 클릭하면 나타나는 이 인터페이스는, Google이 AI와 사람의 협업을 어떻게 바라보는지를 명확하게 보여줍니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/158c8fd1-16d9-4dc4-b5b8-3548e6ee2156/image.png)

> Agent Manager, <https://antigravity.google/product>

#### 워크스페이스 기반 병렬 작업

Agent Manager에서는 **로컬 폴더 = 워크스페이스**라는 개념으로 여러 프로젝트를 동시에 관리합니다. 예를 들어:

* `FPS-게임` 워크스페이스에서 게임 개발
* `블로그` 워크스페이스에서 기술 블로그 구축
* `마케팅` 워크스페이스에서 랜딩 페이지 제작

각 워크스페이스는 독립적으로 운영되며, 하나의 워크스페이스 안에서도 여러 에이전트 대화를 동시에 실행할 수 있습니다. 이는 기존에 Claude Code의 서브에이전트(Sub-agent)나 워크트리(Worktree)를 활용한 병렬 작업 테크닉이 꽤 복잡했던 것과 대비됩니다. Antigravity는 이를 직관적인 UI로 해결했습니다.

#### Inbox: 중앙 집중식 알림 관리

Agent Manager의 **Inbox**는 여러 워크스페이스에서 진행 중인 작업의 알림을 한곳에서 확인할 수 있게 해줍니다:

* 사용자 확인(Confirmation)이 필요한 작업
* 완료된 작업 알림
* 에러 발생 시 즉시 확인

백그라운드에서 여러 에이전트가 동시에 작업하는 동안, 개발자는 Inbox를 통해 필요한 시점에만 개입하면 됩니다.

#### Planning Mode vs Fast Mode

대화 시작 시 두 가지 모드를 선택할 수 있습니다:

| 모드 | 설명 | 적합한 상황 |
| --- | --- | --- |
| **Planning Mode** | 계획을 먼저 세우고 사용자 확인 후 구현 | 복잡한 기능, 신중한 검토 필요 시 |
| **Fast Mode** | 확인 없이 끝까지 한 번에 실행 | 단순한 작업, 빠른 프로토타이핑 |

에이전트가 작업이 간단하다고 판단하면, Planning Mode에서도 자동으로 구현까지 진행하는 경우도 있습니다.

### 3. Browser Agent: Chrome을 만든 회사의 강점

Google이 Chrome을 보유하고 있다는 점은 Antigravity에서 큰 강점으로 작용합니다. **Browser Agent**는 Chrome 익스텐션을 통해 브라우저를 직접 제어합니다.

#### 브라우저 연동 워크플로우

1. 에이전트가 코드 작성 완료
2. 터미널에서 localhost 실행
3. 브라우저에서 자동으로 테스트 수행
4. **화면 레코딩**으로 작동 과정 캡처
5. 레코딩을 에이전트에게 피드백
6. 버그 발견 시 자동 코드 수정

이 모든 과정이 자동으로 이루어지며, 에이전트가 직접 브라우저를 조작하고 그 결과를 스크린샷이나 녹화로 사용자에게 보여줍니다. 웹 기반 테스트가 필요한 프론트엔드 개발에서 특히 강력한 기능입니다.

### 4. Multi-window Product: Editor, Manager, Browser

Antigravity는 세 가지 핵심 표면(Surface)으로 구성된 **멀티 윈도우 제품**입니다:

#### Editor

단일 워크스페이스에 매핑되는 완전한 기능의 AI 기반 IDE입니다. 기존 IDE에 익숙한 개발자들이 자연스럽게 적응할 수 있는 환경을 제공합니다.

#### Agent Manager (Public Preview)

여러 워크스페이스에서 수십 개의 에이전트를 동시에 관리하고, 코드를 직접 작성하는 대신 에이전트를 통해 코드베이스와 상호작용할 수 있는 **조감도(Bird's-eye View)**를 제공합니다.

주요 특징:

* Planning Mode 중심의 인터페이스
* Conversation UI
* Artifact 검토 및 관리
* "No Code" 오케스트레이션 뷰

> Google은 에이전트와 모델이 계속 발전함에 따라, 이 조감도가 모든 작업의 주요 진입점이 될 것으로 예상하고 있습니다. 실제로 Agent Manager가 메인 화면이 되고, 하드코어한 코드 작업이 필요할 때만 Editor로 전환하는 방식이 미래의 개발 패턴이 될 수 있습니다.

#### Browser (Public Preview)

IDE를 넘어 더 많은 표면에서 읽기 및 조작이 가능한 **Browser-use Agent** 기능입니다.

#### Playground: 빠른 프로토타이핑 공간

별도의 워크스페이스를 만들지 않고도 빠르게 아이디어를 테스트할 수 있는 **Playground** 공간도 제공됩니다. 간단한 프로토타이핑이나 실험적인 코드 작성에 유용합니다.

### 5. Cross-surface Agents: 다중 표면 제어

Antigravity의 에이전트는 **에디터, 터미널, 브라우저**를 동시에 제어할 수 있습니다. 이러한 역량을 통해 에이전트는 더 복잡한 엔드투엔드 소프트웨어 태스크를 계획하고 실행할 수 있습니다:

* 기능 개발(Building Features)
* UI 반복 작업(UI Iteration)
* 버그 수정(Fixing Bugs)
* 리서치(Research)
* 리포트 생성(Generating Reports)

---

Artifacts: 에이전트와 사용자 간의 커뮤니케이션
------------------------------

### Artifacts의 정의와 역할

Artifact는 에이전트가 **작업을 수행하거나 사용자에게 작업 내용과 사고 과정을 전달하기 위해 생성하는 모든 산출물**입니다. 에이전트가 더욱 자율적으로 변하고 더 긴 시간 동안 실행될 수 있게 됨에 따라, Artifact는 사용자가 모든 에이전트 단계를 동기적으로 모니터링할 필요 없이 **비동기적으로 작업을 전달**받을 수 있게 합니다.

### Artifact의 종류

| Artifact 유형 | 설명 |
| --- | --- |
| **Rich Markdown Files** | 상세한 문서화 및 설명 |
| **Diff Views** | 코드 변경 사항 시각화 |
| **Architecture Diagrams** | 시스템 구조 다이어그램 |
| **Images** | UI 목업, 스크린샷 등 |
| **Browser Recordings** | 브라우저 작업 녹화 |
| **Task Lists** | 수행할 작업 목록 |
| **Implementation Plans** | 구현 계획서 |
| **Walkthroughs** | 완료된 작업 설명 |

### Artifact와 피드백

Artifact의 핵심 개념 중 하나는 **피드백(Feedback)**입니다. 사용자 설정에 따라, 에이전트는 중간 Artifact에 대한 검토를 요청하여 사고나 구현이 사용자의 의도와 목표에 부합하는지 확인받을 수 있습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/ed6bb535-6c96-4db1-b897-efcca0d0328e/image.png)

> Feedback, <https://antigravity.google/product>

사용자는 Artifact에 피드백을 제공하여 에이전트를 올바른 방향으로 안내할 수 있으며, 피드백의 UI/UX는 Artifact 유형에 따라 다릅니다:

* **텍스트 Artifact**: Google Docs 스타일의 코멘트
* **스크린샷**: 영역 선택 후 피드백 작성
* **코드 Diff**: 특정 라인에 대한 코멘트

Artifact는 에이전트가 **Planning Mode**에 있을 때 생성되며, Agent Manager와 Editor 뷰 모두에서 확인할 수 있습니다. 단, Agent Manager가 Artifact 표시, 정리, 관리에 최적화되어 있습니다.

---

Antigravity의 4대 핵심 원칙
---------------------

Google은 Antigravity를 설계할 때 4가지 핵심 원칙을 기반으로 했습니다:

### 1. Trust (신뢰)

에이전트의 작업을 자연스러운 태스크 수준의 추상화로 제공하고, 검증에 필요한 충분한 Artifact와 결과물을 함께 제시합니다. 에이전트는 작업 자체뿐만 아니라 **작업의 검증**에도 깊이 집중합니다.

### 2. Autonomy (자율성)

Gemini 3급 모델의 등장으로, 에이전트가 여러 표면에서 동시에 자율적으로 작업할 수 있는 시대가 열렸습니다. Antigravity는 이러한 자율성을 최적으로 노출하는 폼 팩터를 제공합니다.

### 3. Feedback (피드백)

원격 전용 폼 팩터의 핵심 단점은 에이전트와 쉽게 반복(iterate)할 수 없다는 것입니다. Antigravity는 로컬 작업을 기반으로, 모든 표면과 Artifact에서 직관적인 비동기 피드백을 지원합니다.

### 4. Self-improvement (자기 개선)

Antigravity는 **학습(Learning)**을 핵심 요소로 취급합니다. 에이전트의 액션은 지식 베이스에서 정보를 검색하고, 동시에 새로운 지식을 기여합니다. 이를 통해 에이전트는 과거 작업에서 학습하며, 유용한 코드 스니펫, 아키텍처 정보, 특정 하위 작업을 성공적으로 완료한 단계들을 축적합니다.

---

실제 사용 사례: 개발자 커뮤니티의 반응
----------------------

### 사례 1: 동시 다발적 프로젝트 개발

한 개발자는 Agent Manager를 활용해 **FPS 게임**, **기술 블로그**, **마케팅 페이지**를 동시에 개발하는 테스트를 진행했습니다. 각 워크스페이스에서 독립적으로 에이전트가 작업을 수행하고, Inbox를 통해 확인이 필요한 사항만 체크하는 방식으로 높은 생산성을 경험했습니다.

특히 마케팅 페이지 작업에서 "이모지 대신 Lucide 아이콘을 사용해줘"라는 간단한 요청만으로 디자인이 개선되었고, 에이전트가 자동으로 브라우저를 열어 결과를 테스트하고 레코딩까지 제공하는 모습이 인상적이었다고 합니다.

### 사례 2: Obsidian 노트 2,000개 분석 및 3D 시각화

또 다른 개발자는 약 2,000개의 Obsidian 노트를 Antigravity에 분석시키고, 자신의 관심사와 지식 구조를 **3D 그래프로 시각화**하는 작업을 수행했습니다. Gemini 3 Pro High 모델을 사용한 결과:

* 전체 노트 분석: **약 12초**
* 3D 시각화 HTML 생성: **5분 이내**
* 키워드별 크기 차등화 및 연결 구조 표현까지 완료

이 정도 규모의 데이터 분석과 시각화 작업이 이렇게 빠르게 처리된다는 점에서, Gemini 3 Pro의 **상상 이상의 속도와 정확도**가 확인되었습니다.

### 사례 3: 실시간 이미지 생성 통합

로고 제작이 필요한 상황에서 "로고를 만들어서 적용해줘, 투명 배경으로"라고 요청하자, **Nano Banana** 이미지 생성 모델이 자동으로 호출되어 SVG 및 PNG 로고를 생성했습니다. Claude Code 등 다른 도구에서 이미지 생성 기능이 제한적이었던 것과 비교하면, Google의 이미지 생성 역량이 Antigravity에 자연스럽게 통합된 점이 큰 장점입니다.

---

Agent 커스터마이징
------------

Antigravity의 Agent는 다양한 방식으로 커스터마이징할 수 있습니다:

| 커스터마이징 옵션 | 설명 |
| --- | --- |
| **Agent Modes / Settings** | 에이전트의 동작 방식 및 설정 조정 |
| **MCP (Model Context Protocol)** | 외부 도구 및 서비스와의 통합 |
| **Rules / Workflows** | 사용자 정의 규칙 및 워크플로우 설정 |

---

Nano Banana Pro: 향상된 이미지 생성 역량
------------------------------

Antigravity에는 **Nano Banana Pro**(Gemini 3 Pro 기반)가 롤아웃되고 있습니다. 이 모델은 기존 Nano Banana 대비 여러 측면에서 개선되었습니다:

| 개선 영역 | 설명 |
| --- | --- |
| **Text Rendering** | 이미지 내 텍스트 렌더링 품질 향상 |
| **Collateral Generation** | 다양한 시각 자료 생성 능력 강화 |
| **Edit Consistency** | 편집 간 일관성 유지 |

### 개발자 워크플로우에서의 활용

Antigravity의 에이전트는 적절한 시점에 이미지 생성 모델을 자동으로 활용합니다:

1. **UI 목업 생성**: 새로운 프론트엔드를 위한 UI 목업을 생성하여, 사용자가 코드 생성 전에 시각적 피드백을 제공할 수 있습니다. Nano Banana Pro의 향상된 텍스트 렌더링과 편집 일관성이 이 과정을 더욱 풍부하게 만듭니다.
2. **시스템/아키텍처 다이어그램**: 기존 코드나 지식을 설명하기 위한 이해하기 쉬운 다이어그램을 생성합니다.
3. **이미지 에셋 생성**: 스톡 사진을 뒤지는 대신, 웹사이트나 시각적 애플리케이션에 사용할 관련성 높은 이미지 에셋을 직접 생성합니다.

Nano Banana Pro는 점진적으로 롤아웃 중이며, 아직 접근 권한이 없는 사용자의 경우 에이전트가 기존 Nano Banana를 사용합니다.

---

시작하기: 다운로드 및 설치
---------------

### 다운로드

**antigravity.google/download**에서 Google Antigravity를 다운로드할 수 있습니다.

### 시스템 요구사항

| 플랫폼 | 요구사항 |
| --- | --- |
| **macOS** | Apple 보안 업데이트가 지원되는 버전 (일반적으로 현재 및 이전 두 버전). 최소 버전 12 (Monterey). **X86 미지원** |
| **Windows** | Windows 10 (64 bit) |
| **Linux** | glibc >= 2.28, glibcxx >= 3.4.25 (예: Ubuntu 20, Debian 10, Fedora 36, RHEL 8) |

> **참고**: 초기 설치 및 온보딩 과정에서 시간이 다소 걸릴 수 있습니다. 오류가 아니라 초기 설정에 필요한 시간이니 인내심을 가지고 기다려주세요.

### 기본 네비게이션

Editor와 Agent Manager 간의 전환은 매우 직관적입니다:

| 동작 | 단축키 (Mac) | 단축키 (Windows) |
| --- | --- | --- |
| Editor ↔ Agent Manager 전환 | `Cmd + E` | `Ctrl + E` |
| 설정 열기 | `Cmd + ,` | `Ctrl + ,` |

**Editor에서 Agent Manager로:**

* 상단 바의 버튼 클릭
* `Cmd + E` 단축키

**Agent Manager에서 Editor로:**

* 워크스페이스 드롭다운의 "Focus Editor" 옵션
* "Open Editor" 버튼
* `Cmd + E` 단축키

### 설정

Antigravity 설정은 Agent, Browser, Editor 등 다양한 영역에서 구성할 수 있습니다:

* 모든 표면에서 키보드 단축키: `Cmd + ,`
* Agent Manager의 Settings 탭 또는 기어 아이콘
* Editor에서 "Settings > Open Antigravity User Settings"

#### 데이터 수집 설정

"Enable Telemetry" 설정은 Settings 패널의 "Account" 섹션에서 찾을 수 있습니다. 활성화하면 Antigravity는 Antigravity 및 이를 지원하는 모델의 평가, 개발, 개선에 사용하기 위해 상호작용 데이터를 수집합니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/2452ab80-c829-4d9a-b632-ee9d18577a37/image.png)

---

지원 모델
-----

Antigravity는 개발자에게 **모델 선택권**을 제공합니다:

| 모델 | 특징 |
| --- | --- |
| **Gemini 3 Pro High** | 가장 강력한 성능, 복잡한 작업에 적합 |
| **Gemini 3 Pro Low** | 빠른 응답, 간단한 작업에 적합 |
| **Claude Sonnet 4.5** | Anthropic의 균형 잡힌 모델 |
| **Claude Sonnet 4.5 Thinking** | 복잡한 추론이 필요한 작업에 적합 |
| **GPT-OSS 120B** | OpenAI의 오픈소스 모델 |

### 요금 및 제한

현재 퍼블릭 프리뷰 기간 동안 **무료**로 제공되며, Gemini 3 Pro에 대한 넉넉한 사용량 제한이 적용됩니다. 사용량 제한은 5시간마다 갱신되며, 에이전트가 수행한 작업량과 상관관계가 있습니다. 단순한 작업은 더 많은 프롬프트를 처리할 수 있고, 복잡한 작업은 그 반대입니다.

Google의 모델링에 따르면, 극소수의 파워 유저만이 5시간당 사용량 제한에 도달할 것으로 예상됩니다.

---

현재 한계점과 개선 방향
-------------

얼리 어답터들의 피드백에 따르면, 현재 Antigravity는 다음과 같은 개선점이 있습니다:

* **버그**: 아직 Public Preview 단계로 일부 버그가 존재
* **속도**: 특정 상황에서 응답이 느려지는 경우 발생
* **안정성**: 일부 복잡한 작업에서 예상대로 동작하지 않는 경우

그러나 이러한 초기 단계의 불안정함에도 불구하고, **Agent Manager**와 같은 혁신적인 개념의 도입으로 인해 많은 개발자들이 적극적으로 사용해보고 있습니다. Google의 빠른 업데이트와 개선이 기대됩니다.

---

결론: 에이전트 중심 개발의 미래
------------------

Google Antigravity는 단순한 AI 코딩 어시스턴트가 아닙니다. 이는 소프트웨어 개발의 패러다임을 **에이전트 중심(Agent-First)**으로 전환하려는 Google의 비전을 담은 플랫폼입니다.

### 핵심 가치 요약

| 원칙 | 구현 방식 |
| --- | --- |
| **Trust** | 태스크 수준의 추상화, 검증 가능한 Artifact |
| **Autonomy** | 다중 표면(Editor, Terminal, Browser) 동시 제어 |
| **Feedback** | 비동기적이고 직관적인 피드백 메커니즘 |
| **Self-improvement** | 과거 작업에서 배우는 Knowledge 시스템 |

### Antigravity가 보여주는 미래

Antigravity의 설계 철학은 명확합니다:

> "**사람들은 하나의 프로젝트만 동시에 작업하지 않을 것이다.**"

AI가 빨라지고 성능이 좋아질수록, 개발자들은 자연스럽게 여러 에이전트를 병렬로 실행하고 싶어지며, 이렇게 했을 때 생산성이 배수로 늘어납니다.

Google은 Chrome이라는 브라우저, Gemini라는 강력한 언어 모델, Nano Banana라는 이미지 생성 모델을 모두 보유하고 있습니다. 이 모든 역량이 Antigravity에 통합되면서, **결국 모든 것이 Google로 수렴하고 있다**는 평가도 나오고 있습니다.

그럼 저는 이만 Antigravity 쓰러 가보겠습니다 ヾ(＾ ∇ ＾).