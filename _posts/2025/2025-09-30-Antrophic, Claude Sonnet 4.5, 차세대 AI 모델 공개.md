---
title: "Antrophic, Claude Sonnet 4.5, 차세대 AI 모델 공개"
date: "2025-09-30"
year: "2025"
---

# Antrophic, Claude Sonnet 4.5, 차세대 AI 모델 공개

원본 게시글: https://velog.io/@euisuk-chung/Antrophic-Claude-Sonnet-4.5-차세대-AI-모델-공개

TL;DR
-----

**핵심 요약:**

* **세계 최고 코딩 모델**: SWE-bench Verified에서 77.2% 달성, 30시간 이상 복잡한 작업 집중 가능
* **컴퓨터 사용 능력 대폭 향상**: OSWorld 61.4% (4개월 전 42.2%에서 상승)
* **추론 및 수학 능력 대폭 강화**: 다양한 벤치마크에서 최고 성능
* **가장 정렬된 frontier 모델**: Misaligned behavior score 13.4%로 업계 최저 수준
* **가격 동일 유지**: Claude Sonnet 4와 동일한 $3/$15 per million tokens
* **Claude Agent SDK 출시**: 개발자가 Claude Code 수준의 에이전트 구축 가능
* **제품 생태계 대폭 강화**: Checkpoints, VS Code 확장, 코드 실행, 파일 생성 등  
  **즉시 사용 가능**: API에서 `claude-sonnet-4-5` 모델 스트링으로 접근

---

![](https://velog.velcdn.com/images/euisuk-chung/post/a5142436-84a1-4d46-920f-74aa0fa09e55/image.png)

> <https://www.anthropic.com/news/claude-sonnet-4-5>

서론: 새로운 Claude Model의 등장
------------------------

코드는 모든 곳에 존재합니다. 우리가 사용하는 모든 애플리케이션, 스프레드시트, 소프트웨어 도구를 구동하는 핵심 요소입니다. 이러한 도구들을 사용하고 복잡한 문제를 해결하는 능력이야말로 현대 업무가 이루어지는 방식입니다.

**Claude Sonnet 4.5**는 바로 이것을 가능하게 만듭니다. 이는 세계 최고의 코딩 모델이자, 복잡한 에이전트 구축에 가장 강력한 모델이며, 컴퓨터 사용에 최적화된 모델입니다. 동시에 추론과 수학 분야에서 상당한 개선을 보여줍니다.

제품 생태계의 혁신적 발전
--------------

### Claude Code의 진화

Anthropic은 Claude Sonnet 4.5와 함께 제품 전반에 걸친 주요 업그레이드를 발표했습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/5d031660-a8dc-4bb9-a462-479f8f85b5cc/image.png)

> <https://claude.com/product/claude-code>

Claude Code에는 가장 많이 요청받았던 기능 중 하나인 **checkpoints**가 추가되어 진행 상황을 저장하고 **이전 상태로 즉시 롤백**할 수 있게 되었습니다. 터미널 인터페이스가 새롭게 개선되었고, 네이티브 VS Code 확장이 출시되었습니다.

### Claude API의 새로운 기능

* **Context Editing 기능**: 더 복잡한 작업 처리를 위한 컨텍스트 편집
* **Memory Tool**: 에이전트가 더 오랫동안 실행되고 더 큰 복잡성을 처리할 수 있도록 지원

### Claude Apps의 실용적 확장

Claude 앱에는 **코드 실행**과 **파일 생성** 기능(스프레드시트, 슬라이드, 문서)이 대화에 직접 통합되었습니다. 지난달 대기자 명단에 등록한 Max 사용자들에게는 **Claude for Chrome 확장**을 제공합니다.

### Claude Agent SDK: 개발자를 위한 혁신

개발자들에게는 Claude Code를 만드는 데 사용된 동일한 구성 요소를 제공합니다. 이를 **Claude Agent SDK**라고 부릅니다. 최고 수준의 제품을 구동하고 완전한 잠재력을 발휘할 수 있게 하는 인프라가 이제 개발자들이 구축할 수 있는 도구로 제공됩니다.

Frontier Intelligence: 최첨단 성능 지표
--------------------------------

### 코딩 능력의 새로운 기준

Claude Sonnet 4.5는 실제 소프트웨어 코딩 능력을 측정하는 **SWE-bench Verified** 평가에서 최고 수준의 성능을 달성했습니다. 실제로 30시간 이상의 복잡하고 다단계적인 작업에서 집중력을 유지하는 것이 관찰되었습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/bdb5c0ba-e9ac-4311-8546-231a008f4ac0/image.png)

**SWE-bench Verified 성능:**

* **표준 구성**: 77.2%
* **1M 컨텍스트**: 78.2%
* **고성능 컴퓨팅**: 82.0%

![](https://velog.velcdn.com/images/euisuk-chung/post/95e55a56-9a69-4988-bce0-be2dc96d0cff/image.png)

### 컴퓨터 사용 능력의 비약적 향상

Claude Sonnet 4.5는 컴퓨터 사용 분야에서 상당한 발전을 이루었습니다.

* 실제 컴퓨터 작업에서 AI 모델을 테스트하는 벤치마크인 **OSWorld**에서 현재 **61.4%**로 선두를 달리고 있습니다.
* 불과 4개월 전 Sonnet 4가 42.2%로 선두였던 것과 비교하면 놀라운 발전입니다.

### 다양한 분야에서의 성능 향상

이 모델은 추론과 수학을 포함한 광범위한 평가에서 향상된 능력을 보여줍니다:

* **AIME (수학)**: 고급 수학 문제 해결 능력 향상
* **MMMLU (다국어)**: 14개 비영어권 언어에서의 성능
* **τ2-bench**: 복잡한 에이전트 작업 수행 능력
* **Terminal-Bench**: 터미널 환경에서의 작업 수행 능력

금융, 법률, 의학, STEM 분야의 전문가들은 Sonnet 4.5가 Opus 4.1을 포함한 이전 모델들에 비해 도메인별 지식과 추론에서 극적으로 향상된 성능을 보인다고 평가했습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/cf3bd4cf-bd79-4db0-aae8-8a84f36025a6/image.png)

> Finance

![](https://velog.velcdn.com/images/euisuk-chung/post/a6d5cd75-e8aa-4a4c-ad2f-9ed0a070b619/image.png)

> Law

![](https://velog.velcdn.com/images/euisuk-chung/post/d4fd2d48-26ac-4b49-9f82-590ba8ef7e06/image.png)

> Medicine

![](https://velog.velcdn.com/images/euisuk-chung/post/3369d295-a993-439b-99fe-9ddb56545e02/image.png)

> STEM - 과학(Science), 기술(Technology), 공학(Engineering), 수학(Mathematics)

지금까지 가장 정렬된 모델
--------------

### 안전성과 능력의 동시 향상

Claude Sonnet 4.5는 가장 강력한 모델일 뿐만 아니라 지금까지 가장 정렬된 frontier 모델입니다.

* Claude의 향상된 능력과 광범위한 안전 훈련을 통해 모델의 행동을 상당히 개선할 수 있었으며, 아첨, 기만, 권력 추구, 망상적 사고 조장 경향과 같은 우려스러운 행동을 줄였습니다.

### Misaligned Behavior Scores 분석

자동화된 행동 감사기를 통한 평가에서 Claude Sonnet 4.5는 **13.4%**라는 현저히 낮은 misaligned behavior score를 달성했습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/107b0a6c-df2a-405b-aa76-ba5aa02a25fd/image.png)

**경쟁 모델 대비 성능:**

* **Claude Sonnet 4.5**: 13.4% (최우수)
* **GPT-5 mini**: 15.9%
* **GPT-5**: 16.8%
* **Claude Sonnet 4**: 24.1%
* **Claude Opus 4.1**: 29.2%
* **Grok 4**: 32.8%
* **기타 모델들**: 25-43% 범위

이러한 misaligned behavior에는 기만, 아첨, 권력 추구, 망상 조장, 유해한 시스템 프롬프트에 대한 준수 등이 포함됩니다.

### Prompt Injection 방어 강화

* 모델의 에이전트 및 컴퓨터 사용 능력에서 사용자에게 가장 심각한 위험 중 하나인 prompt injection 공격에 대한 방어 능력이 상당히 향상되었습니다.

ASL-3 보호 체계와 안전장치
-----------------

### 다층적 보안 시스템

Claude Sonnet 4.5는 모델의 능력 수준에 맞는 적절한 안전장치를 적용하는 프레임워크인 **AI Safety Level 3 (ASL-3)** 보호 체계 하에 출시됩니다.

* 안전장치의 핵심은 **분류기(classifier)**라는 필터 시스템입니다.
  + 이는 잠재적으로 위험한 입력과 출력을 실시간으로 탐지하는 역할을 하며, 특히 화학, 생물학, 방사선, 핵(CBRN) 무기와 관련된 콘텐츠를 중점적으로 감지합니다.

### False Positive 개선

분류기가 완벽하지는 않아서, 때때로 **정상적인 콘텐츠를 위험 콘텐츠로 잘못 판단하는 경우(false positive)가 발생**할 수 있습니다.

* 이러한 경우를 대비해, 중단된 대화를 더 낮은 CBRN 위험 수준을 가진 모델인 Sonnet 4로 손쉽게 이어갈 수 있는 기능을 제공합니다.
* false positive 감소에 있어서 상당한 진전을 이뤘으며, 처음 이 시스템을 공개했을 때와 비교해 10배, 5월 Claude Opus 4 출시 이후로는 2배 감소시켰습니다.
* 분류기의 정확도를 더욱 높이기 위한 개선 작업을 지속적으로 진행하고 있습니다.

Claude Agent SDK: 6개월의 노하우를 공개
------------------------------

![](https://velog.velcdn.com/images/euisuk-chung/post/514636cd-cbed-4622-a3e9-ef0a59643d21/image.png)

> <https://youtu.be/OZ-aLrJ0oVg>

### 실전 경험의 산물

Anthropic은 Claude Code에 업데이트를 제공하는 데 6개월 이상을 보냈기 때문에 AI 에이전트를 구축하고 설계하는 데 필요한 것이 무엇인지 알고 있습니다.

다음과 같은 어려운 문제들을 해결했습니다:

* 에이전트가 장기 실행 작업에서 메모리를 관리하는 방법
* 자율성과 사용자 제어의 균형을 맞추는 권한 시스템 처리 방법
* 공유 목표를 향해 작업하는 하위 에이전트들을 조정하는 방법

### 광범위한 활용 가능성

이제 이 모든 것을 개발자들이 사용할 수 있도록 공개합니다.

* Claude Agent SDK는 Claude Code를 구동하는 동일한 인프라이지만, 코딩뿐만 아니라 매우 다양한 작업에서 인상적인 이점을 보여줍니다.
* Claude Code는 원하는 도구가 아직 존재하지 않았기 때문에 구축한 것입니다. Agent SDK는 어떤 문제를 해결하든 똑같이 강력한 것을 구축할 수 있는 동일한 기반을 제공합니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/ea183c22-3dd9-4a82-8527-8d7f0dd1ec5e/image.png)

> <https://youtu.be/OZ-aLrJ0oVg>

* 다양한 에이전트 유형:
  + Code Security Agent (코드 보안 에이전트)
  + Code Review Agent (코드 검토 에이전트)
  + Contract Review Agent (계약 검토 에이전트)
  + Meeting Summary Agent (회의 요약 에이전트)
  + Financial Reporting Agent (재무 보고 에이전트)
  + Email Automation Agent (이메일 자동화 에이전트)
  + Invoice Processing Agent (송장 처리 에이전트)

![](https://velog.velcdn.com/images/euisuk-chung/post/d6d338a9-004d-4263-85f1-cd98a0b62df5/image.png)

#### Orchestration (오케스트레이션) 🧠

오케스트레이션은 에이전트의 **두뇌**와 같은 역할을 합니다. 복잡한 작업을 수행하기 위해 여러 단계를 계획하고, 정보를 기억하며, 필요할 때 적절한 도구를 사용하는 전체 과정을 지휘하는 핵심 기능입니다.

* **다단계 추론 (Multi-step reasoning)**: 사용자의 복잡한 요청을 받으면, 에이전트는 이를 해결하기 위해 여러 개의 작은 단계로 작업을 나눕니다. 예를 들어 "최근 기술 트렌드를 조사해서 보고서 초안을 작성해 줘"라는 요청을 받으면, `1) 웹 검색으로 최신 기술 트렌드 기사 찾기` -> `2) 기사 내용 요약하기` -> `3) 요약된 내용을 바탕으로 보고서 형식으로 글쓰기`와 같이 순차적인 계획을 세우고 실행합니다.
* **컨텍스트 관리 (Context management)**: 에이전트가 대화의 맥락을 기억하고 이해하는 능력입니다. 사용자와의 이전 대화 내용이나 작업 히스토리를 기억하여, "방금 찾아준 그 기사에서 핵심만 뽑아줘"와 같은 대명사를 포함한 후속 질문에도 막힘없이 답변할 수 있습니다. 이것은 에이전트가 단기 기억을 가지게 하는 것과 같습니다.
* **도구 호출 (Tool calling)**: 에이전트가 스스로의 능력만으로는 해결할 수 없는 작업을 외부 도구(Tools)를 호출하여 해결하는 기능입니다. 예를 들어, 실시간 정보가 필요할 때는 **웹 검색** 도구를, 복잡한 계산이 필요할 때는 **코드 실행** 도구를, 특정 파일의 정보가 필요할 때는 **파일 읽기** 도구를 호출하여 그 결과를 가져와 사용자의 요청을 처리합니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/2a6365d0-136a-43d5-bb0c-6811c8e9d56a/image.png)

#### Tools (도구) 🛠️

도구는 에이전트의 **손과 발**과 같습니다. AI 모델의 지능을 실제 세상의 데이터나 시스템과 연결하여 구체적인 행동을 수행하게 해주는 기능들의 모음입니다.

* **파일 읽기/쓰기 작업**: 에이전트가 로컬 파일 시스템에 접근하여 `.txt`, `.csv`, `.json` 같은 파일의 내용을 읽어 분석하거나, 분석 결과를 새로운 파일로 저장할 수 있게 합니다.
* **코드 실행**: Python과 같은 프로그래밍 언어 코드를 직접 실행할 수 있습니다. 이를 통해 복잡한 데이터 분석, 통계 계산, 시각화 자료 생성 등 정교한 작업을 수행할 수 있습니다.
* **웹 검색**: 최신 정보나 특정 주제에 대한 자료가 필요할 때, 에이전트가 직접 웹 검색을 수행하여 필요한 정보를 수집합니다.
* **사용자 정의 도구 (Custom tools)**: 개발자가 회사의 내부 데이터베이스(DB) 조회, 사내 API 호출, 특정 소프트웨어 제어 등 필요한 기능을 직접 도구로 만들어 에이전트에 추가할 수 있습니다. 이를 통해 조직의 특정 워크플로우에 맞는 맞춤형 자동화 에이전트를 만들 수 있습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/82c78f5a-1e2b-466d-ae5e-db8fa2dd763f/image.png)

#### Permissions (권한) 🛡️

권한은 에이전트가 무분별하게 작동하지 않도록 **안전장치**를 마련하는 기능입니다. 특히 파일 삭제나 중요한 데이터 수정과 같이 민감한 작업을 수행하기 전에 사용자의 통제를 받도록 하여 안정성을 확보합니다.

* **사용자 확인 게이트 (Human confirmation gates)**: 에이전트가 중요한 작업을 실행하기 전에 "이 파일을 정말로 삭제할까요? (Y/N)" 와 같이 사용자에게 명시적인 허락을 구하는 단계입니다. 이를 통해 의도치 않은 사고를 방지할 수 있습니다.
* **세분화된 권한 (Fine-grained permissions)**: 각 도구나 기능별로 에이전트의 접근 권한을 세밀하게 설정할 수 있습니다. 예를 들어, A 에이전트는 '파일 읽기'만 가능하고, B 에이전트는 '파일 읽기와 쓰기' 모두 가능하도록 역할을 분리하여 보안을 강화할 수 있습니다.
* **도구 허용/거부 목록 (Tool allow/deny lists)**: 특정 에이전트가 사용할 수 있는 도구와 사용할 수 없는 도구를 명확하게 목록으로 지정하는 기능입니다. 예를 들어, 민감한 정보를 다루는 에이전트에게는 '웹 검색' 도구 사용을 금지하여 정보 유출의 위험을 차단할 수 있습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/ce4102d2-82ec-4b00-b65f-e3a82d1a344d/image.png)

#### Production Readiness (운영 준비) 🚀

운영 준비는 개발된 에이전트를 실제 서비스 환경에서 **안정적이고 효율적으로 운영**하기 위한 기능들을 제공합니다. 자동차의 계기판이나 블랙박스처럼 에이전트의 상태를 지속적으로 확인하고 문제가 생겼을 때 대처할 수 있도록 돕습니다.

* **세션 관리 (Session management)**: 각 사용자별로 대화 상태와 작업 내역을 독립적으로 관리합니다. 이를 통해 여러 사용자가 동시에 에이전트를 사용하더라도 서로의 대화 내용이 섞이지 않고 개인화된 경험을 제공할 수 있습니다.
* **오류 처리 (Error handling)**: 에이전트가 작업을 수행하다가 예상치 못한 문제(예: 웹사이트 접속 실패, 파일 없음)가 발생했을 때, 시스템이 멈추지 않고 오류를 적절하게 처리하고 복구를 시도하거나 사용자에게 상황을 알리도록 합니다.
* **모니터링 (Monitoring)**: 에이전트의 작동 상태, 도구 사용 빈도, 발생한 오류 등을 실시간으로 추적하고 기록합니다. 개발자는 이 로그 데이터를 분석하여 에이전트의 성능을 개선하고 잠재적인 문제를 미리 파악할 수 있습니다.

"Imagine with Claude": 연구 프리뷰
-----------------------------

![](https://velog.velcdn.com/images/euisuk-chung/post/c8094ada-c1eb-4e48-af6a-28725fd493ad/image.png)

> <https://youtu.be/dGiqrsv530Y>

### 실시간 소프트웨어 생성의 시연

Claude Sonnet 4.5와 함께 "**Imagine with Claude**"라는 임시 연구 프리뷰를 출시합니다. 이 실험에서 Claude는 즉석에서 소프트웨어를 생성합니다. 미리 정해진 기능은 없고, 미리 작성된 코드도 없습니다. 보이는 것은 Claude가 실시간으로 생성하고, 상호작용하면서 요청에 응답하고 적응하는 것입니다.

이는 Claude Sonnet 4.5가 할 수 있는 것을 보여주는 재미있는 시연으로, 강력한 모델과 적절한 인프라를 결합했을 때 가능한 것을 보여주는 방법입니다.

> **"Imagine with Claude"**는 Max 구독자들에게 5일간 제공되며, claude.ai/imagine에서 체험할 수 있습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/dc34b887-8b84-4c30-9ef5-084c58838ade/image.png)

> <https://claude.ai/imagine/>

가격 정책 및 접근성
-----------

### 모델별 가격 체계

Claude 4 패밀리의 가격은 모델별로 차등화되어 있으며, 입력 토큰과 출력 토큰에 대해 서로 다른 요금이 책정됩니다. 또한 Prompt Caching 기능을 활용할 경우 추가적인 비용 최적화가 가능합니다.

**주요 모델 가격 (백만 토큰당)**

| 모델 | 기본 입력 토큰 | 5분 캐시 쓰기 | 1시간 캐시 쓰기 | 캐시 히트 & 갱신 | 출력 토큰 |
| --- | --- | --- | --- | --- | --- |
| Claude Opus 4.1 | $15 | $18.75 | $30 | $1.50 | $75 |
| Claude Opus 4 | $15 | $18.75 | $30 | $1.50 | $75 |
| Claude Sonnet 4.5 | $3 | $3.75 | $6 | $0.30 | $15 |
| Claude Sonnet 4 | $3 | $3.75 | $6 | $0.30 | $15 |

**가격 정책의 특징:**

* **Opus 계열**: 가장 높은 성능을 제공하는 만큼 입력 $15/MTok, 출력 $75/MTok로 최고가
* **Sonnet 계열**: 균형잡힌 성능과 가격으로 입력 $3/MTok, 출력 $15/MTok (Opus 대비 1/5 수준)
* **Prompt Caching**: 캐시 히트 시 입력 비용을 약 90% 절감 가능 (예: Sonnet의 경우 $3 → $0.30, Opus의 경우 $15 → $1.50)

### 접근 방법 및 플랫폼

Claude 4 모델은 다양한 플랫폼을 통해 접근 가능하며, 각 플랫폼마다 고유한 모델 식별자를 사용합니다.

**플랫폼별 모델 이름 체계**

| 모델 | Claude API | AWS Bedrock | GCP Vertex AI |
| --- | --- | --- | --- |
| Claude Sonnet 4.5 | `claude-sonnet-4-5-20250929` | `anthropic.claude-sonnet-4-5-20250929-v1:0` | `claude-sonnet-4-5@20250929` |
| Claude Sonnet 4 | `claude-sonnet-4-20250514` | `anthropic.claude-sonnet-4-20250514-v1:0` | `claude-sonnet-4@20250514` |
| Claude Opus 4.1 | `claude-opus-4-1-20250805` | `anthropic.claude-opus-4-1-20250805-v1:0` | `claude-opus-4-1@20250805` |
| Claude Opus 4 | `claude-opus-4-20250514` | `anthropic.claude-opus-4-20250514-v1:0` | `claude-opus-4@20250514` |

**주요 특징:**

* 모델 이름에 포함된 날짜(스냅샷 날짜)는 모든 플랫폼에서 동일한 모델 버전을 보장합니다
* **Claude Sonnet 4.5부터** AWS Bedrock과 GCP Vertex AI는 두 가지 엔드포인트 타입을 제공:
  + **글로벌 엔드포인트**: 최대 가용성을 위한 동적 라우팅
  + **리전별 엔드포인트**: 특정 지리적 지역을 통한 데이터 라우팅 보장

### 모델 별칭(Alias) 시스템

개발 및 테스트 편의를 위해 Anthropic은 모델 별칭을 제공합니다. 이 별칭은 자동으로 해당 모델의 최신 스냅샷을 가리킵니다.

| 모델 | 별칭 | 실제 모델 ID |
| --- | --- | --- |
| Claude Opus 4.1 | `claude-opus-4-1` | `claude-opus-4-1-20250805` |
| Claude Opus 4 | `claude-opus-4-0` | `claude-opus-4-20250514` |
| Claude Sonnet 4.5 | `claude-sonnet-4-5` | `claude-sonnet-4-5-20250929` |
| Claude Sonnet 4 | `claude-sonnet-4-0` | `claude-sonnet-4-20250514` |

**별칭 사용 시 주의사항:**

* 별칭은 실험 및 프로토타이핑에 유용하지만, **프로덕션 환경에서는 특정 모델 버전 사용을 권장**
* 새로운 모델 스냅샷이 출시되면 일반적으로 1주일 이내에 별칭이 최신 버전으로 마이그레이션됨
* 별칭은 참조하는 기본 모델 버전과 동일한 rate limit 및 가격 정책이 적용됨

### Context Window 및 출력 제한

| 모델 | Context Window | 최대 출력 토큰 |
| --- | --- | --- |
| Claude Sonnet 4.5 | 200K (1M 베타) | 64,000 (~48K 단어) |
| Claude Sonnet 4 | 200K (1M 베타) | 64,000 (~48K 단어) |
| Claude Opus 4.1 | 200K | 32,000 (~24K 단어) |
| Claude Opus 4 | 200K | 32,000 (~24K 단어) |

**특별 기능:**

* **1M 토큰 Context Window**: Claude Sonnet 4.5와 4는 `context-1m-2025-08-07` 베타 헤더 사용 시 1M 토큰 컨텍스트 지원
  + 200K 토큰 초과 시 별도의 long context 가격 정책 적용

### 접근 채널

**1. Claude API (직접 접근)**

* Anthropic Console을 통한 API 키 발급
* RESTful API를 통한 직접 통합
* 가장 빠른 신규 기능 및 모델 업데이트 제공

**2. 클라우드 플랫폼**

* **AWS Bedrock**: 엔터프라이즈급 보안 및 규정 준수
* **GCP Vertex AI**: Google Cloud 생태계 통합

**3. 웹 인터페이스**

* **claude.ai**: 브라우저 기반 대화형 인터페이스
* 코딩 없이 Claude와 직접 상호작용 가능

**4. Priority Tier (우선순위 서비스 계층)**

* Claude 4 패밀리 전체 모델에서 지원
* 높은 처리량과 낮은 대기 시간 보장
* 프로덕션 수준의 안정성 제공

결론
--

Claude Sonnet 4.5는 AI 기술 발전에 있어 새로운 이정표를 세웠습니다. 세계 최고 수준의 코딩 능력, 혁신적인 컴퓨터 사용 능력, 강화된 추론 및 수학 능력과 함께, 13.4%라는 업계 최저 수준의 misaligned behavior score를 통해 안전성과 정렬성에서도 새로운 기준을 제시했습니다.

Claude Agent SDK의 공개와 함께 제품 생태계 전반에 걸친 혁신적 기능들은 개발자와 사용자 모두에게 더욱 강력하고 안전한 AI 도구를 제공합니다. "Imagine with Claude"와 같은 연구 프리뷰는 AI의 미래 가능성을 엿볼 수 있게 해줍니다.

동일한 가격으로 제공되는 이러한 혁신적 발전은 AI 기술의 민주화와 접근성 향상에 기여하며, 인간과 AI가 협력하여 더 나은 미래를 만들어가는 중요한 발걸음입니다.

읽어주셔서 감사합니다 😺