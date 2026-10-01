---
type: "Conference Recap"
title: "[OpenAI] DevDay 2026 키노트 정리: 상시 동작 에이전트 Dots, GPT-6.1 Sol, Ultrafast, Codex Cloud까지"
description: "OpenAI DevDay 2026 키노트의 Dots와 ChatGPT Space, GPT-6.1 Sol·Ultrafast·Pro 500·Decisions API, Codex Cloud·Agents API·Private Intelligence, Sign in with ChatGPT와 Marketplace 발표를 순서대로 정리합니다."
date: "2026-09-30"
tags:
  - "OpenAI"
  - "ChatGPT"
  - "AI Agent"
  - "Conference"
generated:
  by: "human:euisuk-chung"
  at: "2026-09-30T21:28:00+09:00"
sources:
  - id: "youtube:Fls_onRviPM"
    resource: "https://www.youtube.com/watch?v=Fls_onRviPM"
    title: "OpenAI DevDay 2026 Keynote (FULL)"
  - id: "runtimewire"
    resource: "https://runtimewire.com/article/everything-openai-announced-at-the-devday-2026-keynote"
    title: "Everything OpenAI announced at the DevDay 2026 keynote"
  - id: "benchlm"
    resource: "https://benchlm.ai/blog/posts/openai-devday-2026"
    title: "OpenAI DevDay 2026 Announcements"
  - id: "cnbc"
    resource: "https://www.cnbc.com/2026/09/29/openai-devday-2026-live-updates.html"
    title: "OpenAI DevDay 2026 live updates"
  - id: "bgr"
    resource: "https://www.bgr.com/2272332/openai-devday-2026-announcements/"
    title: "Everything OpenAI Announced At DevDay 2026"
  - id: "9to5mac"
    resource: "https://9to5mac.com/2026/09/29/openai-teases-20-announcements-at-devday-watch-live/"
    title: "OpenAI makes 20+ announcements at DevDay"
status: "stable"
year: "2026"
---

## 들어가며

2026년 9월 29일(현지 시각) 샌프란시스코에서 OpenAI DevDay 2026 키노트가 열렸습니다. 약 54분 동안 20개가 넘는 발표가 쏟아졌는데, 전체를 관통하는 흐름은 하나로 요약됩니다. 사용자가 매번 지시하는 "챗봇"에서, 권한과 맥락을 가지고 24시간 스스로 일하는 "에이전트"로 제품의 중심이 옮겨가고 있다는 점입니다.

키노트는 크게 두 부분으로 구성되었습니다. 전반부는 일반 사용자와 팀을 위한 제품인 Dots와 ChatGPT Space, 후반부는 개발자 플랫폼을 위한 세 가지 축(모델, 도구, 유통)입니다. 이 글에서는 발표 순서를 그대로 따라가면서, 각 발표의 핵심 내용과 ML 실무자 관점에서 눈여겨볼 지점을 함께 정리합니다.

## 배경: 왜 지금 "상시 동작 에이전트"인가

지난 1~2년간 LLM 에이전트는 주로 "예약해 줘", "항공권 찾아 줘"처럼 짧고 명확한 단발성 작업에 머물러 있었습니다. Sam Altman은 키노트 초반에 이런 에이전트들이 유용하긴 하지만 기술이 할 수 있는 것에 비하면 사소한 수준이라고 평가하며, 더 야심 찬 방향을 제시했습니다.

이 방향을 이해하려면 몇 가지 용어를 먼저 짚어두면 좋습니다.

- **Astra**: 몇 주 전 공개된 OpenAI의 현 최상위 frontier 모델(GPT-6 Astra)입니다. 이번 발표의 Dots가 이 모델 위에서 동작합니다.
- **Harness**: 모델을 감싸 도구 호출, 파일 시스템, 코드 실행, 컨텍스트 관리 등을 담당하는 실행 틀입니다. Codex와 Dots가 같은 harness를 공유합니다.
- **Always-on agent**: 요청이 들어올 때만 반응하는 것이 아니라, 위임받은 책임(responsibility)을 지속적으로 모니터링하고 처리하는 에이전트를 의미합니다.

키노트 도입부에서는 개발자 커뮤니티의 요청을 반영한 Codex 개선 사항도 짧게 언급되었습니다. Linux 지원, 하나의 프로젝트에서 여러 폴더를 다루는 기능, 그리고 모바일 Codex가 그것입니다.

## 1. Dots: 항상 켜져 있는 개인 에이전트

![Dots 발표 장면]({{ '/img/reviews/2026/openai-devday-2026-keynote/devday2026_01_dots.jpg' | relative_url }})

*출처: OpenAI DevDay 2026 Keynote (YouTube), 02:30 부근*

첫 번째이자 가장 큰 발표는 **Dots**입니다. Dots는 ChatGPT 안에 새로 들어온, 매우 유능하고 항상 켜져 있는(always-on) 에이전트입니다. 소개 영상에서는 사용자가 자신의 Dot에 "Alfred"라는 이름을 붙이고, 이사회 발표 자료 업데이트, 마이그레이션 진행, 웨딩 케이크 업체 대체, 웹사이트 배포, 자녀 방과후 수업 등록까지 업무와 일상을 넘나드는 일을 한 흐름으로 맡기는 모습이 그려졌습니다.

### 핵심 개념: "작업"이 아니라 "책임"을 위임한다

Dots의 설계 철학에서 가장 중요한 부분은 위임의 단위가 바뀌었다는 점입니다. 기존 에이전트가 "이것 좀 해줘"라는 단일 태스크를 받았다면, Dots는 다음처럼 지속적인 책임을 받습니다.

- 들어오는 버그 리포트를 모니터링하고, 수정안을 draft PR로 테스트하기
- 내년도 예산 계획 사이클 시작하기
- 앱이 느려지는 원인 찾기
- 곧 종료되는 legacy API에서 앱을 이전하기

마지막 예시가 특히 인상적이었습니다. Dot이 의존성을 추적해 바꿔야 할 부분을 모두 파악하고, 코드를 작성하고, 테스트를 돌리고, 리뷰할 pull request까지 가져온다는 시나리오입니다. 예전 방식이었다면 여러 사람이 함께 붙어야 했을 작업입니다.

### 아키텍처 관점에서 본 Dots

발표 내용을 바탕으로 Dots의 구성 요소를 정리하면 다음과 같습니다.

![GPT-6 Astra 모델, Codex harness, 메모리로 구성된 Dot이 클라우드 컴퓨터, 사용자 권한, 기존 plugin을 사용하고 ChatGPT, Slack, Teams, 문자, 전화로 대화하는 구조]({{ '/img/reviews/2026/openai-devday-2026-keynote/dots-components.svg' | relative_url }})

- **권한**: Dot은 사용자의 접근 권한을 그대로 따릅니다. 사용자가 할 수 없는 일은 Dot도 할 수 없는 구조입니다.
- **실행 환경**: 클라우드에 자체 컴퓨터를 가지고 있어, 필요하면 직접 코드를 작성하고 테스트합니다.
- **연결성**: 온보딩 시 사용자가 이미 연결해 둔 plugin을 그대로 사용합니다.
- **인터페이스**: ChatGPT 밖에서도 대화할 수 있습니다. 곧 문자 메시지로 지시하고 답을 받거나, 전화를 걸어 음성으로 대화할 수도 있게 됩니다.
- **안전장치**: Astra 기반으로 보호 장치와 사용자 정의 지침(custom instructions)이 내장되어 있어, 사용자가 편안하게 느끼는 만큼만 책임을 맡길 수 있습니다.

또 하나 흥미로운 점은 "Dot이 시간이 지나면서 내가 어떻게 일하는지, 어디에 주의를 두고 싶어 하는지를 알아간다"는 부분입니다. 예컨대 밤사이 들어온 내용을 검토하고, 하루를 시작하기 전에 긴급한 것만 알려주는 식입니다. 이는 모델 가중치 업데이트라기보다는 장기 메모리와 사용자 선호 프로필을 축적하는 방식일 가능성이 높지만, 구체적인 구현 방식은 공개되지 않았습니다.

향후에는 한 명의 사용자가 여러 Dot으로 구성된 "팀"과 함께 일하는 형태도 예고되었습니다.

## 2. ChatGPT Space: 사람과 에이전트가 함께 일하는 공간

![ChatGPT Space의 Page 화면]({{ '/img/reviews/2026/openai-devday-2026-keynote/devday2026_02_space.jpg' | relative_url }})

*출처: OpenAI DevDay 2026 Keynote (YouTube), 08:40 부근*

Dots가 일을 처리하는 주체라면, **ChatGPT Space**는 팀과 팀의 Dots가 함께 협업하는 장소입니다. Altman은 기존 생산성 소프트웨어 대부분이 AI와 사람이 함께 일하도록 설계되지 않았다는 문제의식을 밝혔습니다.

Space는 **Page**에서 시작합니다. 문서 안에서 Dot이 사용자와 나란히 작업하며, 다음과 같은 방식으로 불러낼 수 있습니다.

- Page에 Dot을 불러 의존성 추적을 맡기기
- 댓글에서 Dot을 태그하면 바로 작업에 착수
- "Slack 채널을 확인하고 발견한 내용으로 업데이트해" 같은 Page 수준의 지시 부여

곧 **Collaborative Slides**도 추가될 예정입니다. 에이전트가 쉽게 읽고 수정할 수 있는 형태의 슬라이드를 팀과 공유하고 함께 편집하는 기능입니다.

### 데모: 가상의 음악 앱 "Blossom"으로 본 팀 워크플로

Holly가 무대에 올라, 가상의 음악 앱 Blossom 출시를 준비하는 상황으로 Dots와 Space를 시연했습니다. Holly의 Dot 이름은 "Dotty"입니다. 데모에서 보여준 흐름은 다음과 같습니다.

1. **선제적 맥락 파악**: 출시 리뷰 일정이 앞당겨지자 Dotty가 이미 캘린더를 업데이트했고, 피드백을 검토해 문제를 발견한 뒤 새 디자인까지 보내왔습니다.
2. **로컬 실행 위임**: 새 디자인을 직접 만져보고 싶다는 요청에 Dotty가 노트북 접근 권한을 이용해 Codex로 앱을 빌드하고 시뮬레이터에서 실행합니다.
3. **음성 대화**: Holly가 가장 좋아한다는 기능으로, 이미 업무 맥락을 알고 있는 Dot과 "두 번째 뇌"처럼 대화합니다. 라이브 데모에서는 응답이 지연되는 장면도 있었습니다.
4. **Space에서의 협업**: 인터랙티브 차트, Sheets, 라이브 프로토타입 등을 만들고, 팀원과 Dot을 함께 태그해 "막대 차트로 바꿔줘", "Slack DM에 있던 온보딩 수치를 넣어줘" 같은 요청을 처리합니다. 차트는 필터링과 데이터 포인트 검사가 가능하며, Dot이 매시간 최신 상태로 유지할 수 있습니다.
5. **Dot에게 정체성 부여**: Dot이 자체 identity를 가지면서 팀의 동료처럼 그룹 채팅에 참여합니다. 엔지니어들은 피드백 채널에 올라온 세션 ID와 사용자 로그를 Dot이 받아 PR을 여는 방식으로 매일 수십 개의 버그를 고치고 있다고 소개했습니다.

Holly의 정리가 이 파트의 핵심을 잘 보여줍니다. Dots의 가치는 같은 일을 더 빨리 끝내는 데 있는 것이 아니라, 우리가 감당할 수 있다고 느끼는 일의 범위 자체를 바꾸는 데 있다는 것입니다.

### 제공 범위

Dots와 Space는 발표 당일부터 ChatGPT Pro, Business Premium, Enterprise 사용자에게 제공됩니다. Dot은 요금제에 포함되며, Dot과의 대화는 사용량(usage)에서 차감되지 않습니다. 보도에 따르면 Pro와 Business Premium은 순차 배포, Enterprise 계열은 관리자가 활성화하는 베타 형태입니다.

## 3. Specialist Dots와 Microsoft 연동

Enterprise 사용자를 위해 **Specialist Dots**도 발표되었습니다. 개인 비서가 아니라 팀 전체와 함께 일하는 가상의 동료로, 목표와 맥락을 주고 피드백을 통해 개선시킬 수 있으며, 그 피드백은 팀 전체에 공유됩니다. OpenAI 내부에서 여러 역할에 시험 적용한 결과 매우 효과적이었다고 하며, OpenAI가 도입 기업과 함께 셋업을 진행합니다.

또한 Microsoft와 협력해, 기업이 이미 사용하는 Microsoft 도구를 통해 Dots를 관리할 수 있도록 할 예정입니다.

## 4. 개발자 플랫폼 (1): 모델

키노트 후반부는 개발자 플랫폼에 관한 내용입니다. Altman은 플랫폼 전략을 세 가지 축으로 제시했습니다.

1. **모델**: 더 좋은 모델
2. **도구**: OpenAI 내부에서 쓰는 것과 같은 도구, 그리고 원하는 곳에서 제품을 만들고 운영할 자유
3. **유통(Distribution)**: 여러분이 만든 것을 사람들이 발견하도록 돕기

### GPT-6.1 Sol: Astra에 근접한 성능을 1/5 가격으로

![GPT-6.1 Sol 발표 장면]({{ '/img/reviews/2026/openai-devday-2026-keynote/devday2026_03_gpt61_sol.jpg' | relative_url }})

*출처: OpenAI DevDay 2026 Keynote (YouTube), 20:00 부근*

Astra 출시 이후 가장 많이 받은 요청은 "더 싸게, 더 빠르게"였다고 합니다. 그 답으로 나온 첫 번째가 **GPT-6.1 Sol**입니다. 비용과 성능의 균형이 뛰어난 모델로, Astra에 매우 근접한 지능을 제공합니다.

슬라이드에는 x축이 작업당 비용(cost per task), y축이 DeepSWE 점수인 그래프가 등장했습니다. GPT-6.1 Sol이 GPT-6 Astra에 근접한 점수를 훨씬 낮은 비용 구간에서 달성한다는 것이 핵심 메시지입니다. 보도된 API 가격은 다음과 같습니다.

- Input: $2.00 / 1M tokens
- Cached input: $0.10 / 1M tokens
- Output: $10.00 / 1M tokens

OpenAI는 이를 Astra 표준 가격의 약 1/5 수준이라고 설명했습니다. 특히 cached input이 input 대비 1/20 가격이라는 점은 에이전트 워크로드에서 의미가 큽니다. 에이전트는 긴 시스템 프롬프트와 누적된 대화 맥락을 매 턴 반복해서 읽기 때문에, 한 턴의 비용을 대략 다음과 같이 쓸 수 있습니다.

```math
C_{\text{turn}} = p_{\text{in}} \cdot N_{\text{new}} + p_{\text{cache}} \cdot N_{\text{cached}} + p_{\text{out}} \cdot N_{\text{out}}
```

여기서 $`N_{\text{cached}}`$가 턴이 쌓일수록 커지는 항이므로, $`p_{\text{cache}}`$가 낮을수록 "컨텍스트를 재사용하고, 해법을 반복 개선하고, 긴 작업을 처리하는" 비용이 크게 줄어듭니다. 발표에서 강조한 Sol의 장점도 정확히 이 지점이었습니다.

### Ultrafast: 초당 최대 300 토큰

![Ultrafast와 Standard 속도 비교 데모]({{ '/img/reviews/2026/openai-devday-2026-keynote/devday2026_04_ultrafast.jpg' | relative_url }})

*출처: OpenAI DevDay 2026 Keynote (YouTube), 21:15 부근*

두 번째는 가장 높은 지능을 빠른 속도로 쓰고 싶은 경우를 위한 **Ultrafast**입니다. API, ChatGPT, Codex 전반에 적용되며, 별도 모델이 아니라 처리 티어(tier)입니다.

- 기존 **Fast** 티어는 Standard 대비 2배 속도를 2배 가격에 제공했습니다.
- **Ultrafast**는 여기서 한 단계 더 나아가 초당 최대 300 토큰을 제공합니다. 보도에 따르면 Codex에서 최대 8배, API에서 최대 6배 수준의 속도 향상입니다.

데모에서는 같은 프롬프트("DevDay 색상으로 둥근 창이 있는 흰 로켓을 만들고 발사해줘")를 좌우에 동시에 입력했습니다. 왼쪽 Ultrafast 쪽 로켓은 이미 발사된 반면, 오른쪽 Standard 쪽은 아직 조립 중이었습니다.

### 요금제 개편: Pro 500과 Pro 200

![Pro 500 요금제 발표 장면]({{ '/img/reviews/2026/openai-devday-2026-keynote/devday2026_05_pro500.jpg' | relative_url }})

*출처: OpenAI DevDay 2026 Keynote (YouTube), 21:50 부근*

이 개선 사항은 구독 요금제에도 반영되었습니다.

- **Pro 500 (월 $500)**: Ultrafast 사용, 5시간 사용 제한 없음, 파트너 앱에서 사용 가능, Plus 대비 25배 사용량
- **Pro 200 (월 $200)**: 오늘부터 신규 가입 재개. 모든 frontier 모델에 접근할 수 있으며, GPT-6.1 Sol 덕분에 일상적인 주력 모델(daily driver)로 쓸 수 있는 품질을 제공

보도에 따르면 재개된 Pro 200은 기존보다 사용량 한도가 조정되었고, 기존 구독자는 일정 기간 기존 혜택을 유지합니다. OpenAI는 모든 가격대에서 가장 좋은 성능을 제공하는 것이 목표라고 밝혔습니다.

### Decisions API: 1초 미만으로 응답하는 선택형 API

![Decisions API 데모 장면]({{ '/img/reviews/2026/openai-devday-2026-keynote/devday2026_06_decisions_api.jpg' | relative_url }})

*출처: OpenAI DevDay 2026 Keynote (YouTube), 22:55 부근*

모델 파트의 마지막은 **Decisions API**입니다. 모델이 1초도 안 되는 시간 안에 응답하며, 데모에서는 모델이 컴퓨터를 조작하는 장면을 가속 없이 보여주었습니다.

작동 원리는 단순합니다. 경량 모델인 Luna에 **사전 정의된 선택지 집합**을 주고, 모델이 그중 하나를 고르는 문제에 집중하게 만드는 방식입니다. 개념적으로는 자유 생성(free-form generation)을 제약된 분류 문제로 바꾸는 것에 가깝습니다.

```math
\hat{a} = \arg\max_{a \in \mathcal{A}} \; p_\theta(a \mid x), \quad |\mathcal{A}| \ll |\mathcal{V}|^{L}
```

여기서 $`\mathcal{A}`$는 미리 정의된 선택지 집합, $`\mathcal{V}^{L}`$은 길이 $`L`$의 가능한 모든 토큰 시퀀스 공간입니다. 출력 공간이 극단적으로 줄어들기 때문에 디코딩 단계가 짧아지고 지연 시간이 크게 줄어듭니다. 분류, 라우팅, 에이전트의 다음 행동 선택처럼 답의 후보가 정해져 있는 작업에 적합하며, 현재 제한적 preview 단계입니다. 내부 구현(예: constrained decoding 여부)은 공개되지 않았습니다.

Altman은 이로써 OpenAI가 지능, 가격, 속도, 음성, 이미지 등 모든 범주에서 선도 모델을 제공하는 "원스톱 숍"이 되고자 한다고 정리했습니다.

## 5. 연구 현황: AI Research Intern 목표 달성

모델 파트 이후, 이 모델들을 만드는 연구 방식 자체가 어떻게 바뀌고 있는지가 소개되었습니다. 지난해 OpenAI는 "내년에 첫 AI 연구 인턴이 나올 것"이라는 과감한 예측을 했고, 몇 주 전 그 목표에 도달했다고 발표했습니다.

Post-training 연구 리드인 Tejal이 연구 현장의 변화를 공유했습니다.

- **학습 데이터와 환경 구축**: Astra 계열 모델은 수학, 코딩, computer use에 강하며, 이는 곧 연구에 필요한 역량입니다. 법률 작업, 게임 에셋 디자인, 대시보드 제작, 세금 서류 작성 같은 학습용 과제를 모델이 직접 만드는 데 기여하고 있습니다.
- **자동 최적화 루프**: x축이 latency, y축이 성능인 그래프를 보여주며, 모델을 연속 루프로 돌려 이미 여러 개선 사항을 만들어 실제 배포까지 했다고 설명했습니다.
- **안전성 개선**: 모델이 거절(refusal) 학습 개선에 기여하여, 데스크톱이나 브라우저 조작 중 실수할 가능성이 크게 줄었습니다.
- **연구 자동화 지표**: 연구 조직 내 토큰 사용량이 올여름 이후 급증했습니다. 사람이 하루 이상 걸리는 연구 과제에서, 과거에는 모델이 대부분 실패했지만 현재는 **하루짜리 연구 과제의 3분의 1 이상을 개입 없이 수행**합니다.

더 큰 맥락에서는 모델이 수십 년간 풀리지 않았던 100개 이상의 수학 문제 해결에 기여했고, 새로운 항생제 개발, 고대 언어와 역사 연구, 에너지 효율 개선, 로보틱스와 제조 분야 가속에도 쓰이고 있다고 소개했습니다.

## 6. 개발자 플랫폼 (2): 도구

두 번째 축은 "OpenAI가 쓰는 것과 같은 기반을 개발자에게"입니다.

### Codex Harness 오픈소스와 Codex Cloud

![Codex in the cloud 발표 장면]({{ '/img/reviews/2026/openai-devday-2026-keynote/devday2026_07_codex_cloud.jpg' | relative_url }})

*출처: OpenAI DevDay 2026 Keynote (YouTube), 28:20 부근*

출발점은 **Codex harness**입니다. Codex와 Dots를 모두 구동하는 harness로, OpenAI가 효율화에 많은 공을 들였으며 오픈소스로 공개되어 있어 내부를 들여다보고 직접 빌드할 수 있습니다.

이 harness가 이제 클라우드에서도 제공됩니다. **Codex가 클라우드로 들어왔다**는 것은 휴대폰에서 시작한 작업을 데스크톱에서 이어받을 수 있다는 뜻입니다. 재사용 가능한 개발 환경을 기반으로, 기기 간 작업 연속성이 확보됩니다.

### Codex Security Cloud

![Codex Security Cloud 발표 장면]({{ '/img/reviews/2026/openai-devday-2026-keynote/devday2026_08_codex_security_cloud.jpg' | relative_url }})

*출처: OpenAI DevDay 2026 Keynote (YouTube), 28:45 부근*

클라우드 harness를 활용한 첫 번째 예시가 **Codex Security Cloud**입니다. 방어자(defender)가 소프트웨어를 강화할 수 있도록 더 나은 도구를 제공하는 것이 목적이며, 클라우드 환경에서 실행됩니다. 요청이 많았던 기능들도 추가되었습니다.

- 발견 결과 중복 제거(deduplication)
- 예약 스캔(scheduled scans)
- 새로운 인터페이스
- 저장소 스캔 후 자동 수정안 준비

발표 당일부터 바로 사용할 수 있습니다.

### Agents API와 Computer Use

다음으로 새로운 **Agents API**가 발표되었습니다. Harness, multi-agent 제어 등 핵심 구성 요소를 포함하며, Dots를 구동하는 것과 같은 기술입니다. 보도에 따르면 세션 관리, 오케스트레이션, 컨텍스트 압축(compaction)과 복구를 제공하는 관리형 서비스로 public beta 상태입니다.

**Computer use**도 API로 제공됩니다. 데모 시나리오는 웹사이트를 테스트하는 에이전트였습니다. 에이전트가 브라우저를 열고 페이지를 클릭하며 사용자 플로우를 검증합니다.

또한 AWS와 협력한 **Bedrock Managed Agents**를 통해, 기존 AWS 애플리케이션과 데이터 옆에서 OpenAI 에이전트를 구축할 수 있습니다. 보도에 따르면 추론은 Bedrock에서 실행되고 데이터는 AWS 내부에 머뭅니다.

### OpenAI Private Intelligence

![OpenAI Private Intelligence 발표 장면]({{ '/img/reviews/2026/openai-devday-2026-keynote/devday2026_09_private_intelligence.jpg' | relative_url }})

*출처: OpenAI DevDay 2026 Keynote (YouTube), 30:30 부근*

에이전트가 기업 데이터를 다루려면 안전성과 프라이버시가 필수입니다. 이를 위해 **OpenAI Private Intelligence**가 발표되었으며, 두 가지 구성 요소로 이루어져 있습니다.

- **ZDR with Private Safety Processing**: Zero Data Retention 환경에서도 frontier 수준의 안전성 검토를 제공합니다. 콘텐츠를 OpenAI 서버에 저장하지 않으며, 사람이 보호된 콘텐츠에 접근하지 않고 자동화된 안전성 검토를 수행합니다.
- **Private Inference (preview)**: confidential computing과 검증 가능한 통제를 결합해, 처리 중에도 데이터를 보호합니다. 올가을 preview로 제공될 예정입니다.

OpenAI는 가장 큰 고객사들과 함께 이 시스템을 설계했으며, 이것이 프라이버시의 새로운 기준이 될 것이라고 밝혔습니다.

### 속도와 신뢰성

마지막으로 인프라 지표가 공유되었습니다. 99% 이상의 가용성을 유지하면서 **time to first token(TTFT)을 45% 단축**했다는 내용입니다. OpenAI는 이를 근거로 현재 시장에서 가장 신뢰할 수 있는 API라고 주장했습니다.

## 7. Codex 라이브 데모: Ultrafast, CLI, Computer Use, 하드웨어

![Codex와 Ultrafast로 3D 월드를 실시간 수정하는 데모]({{ '/img/reviews/2026/openai-devday-2026-keynote/devday2026_10_codex_3d_world.jpg' | relative_url }})

*출처: OpenAI DevDay 2026 Keynote (YouTube), 33:50 부근*

Romain이 무대에 올라 Codex의 새 기능을 연속으로 시연했습니다. 1년 전만 해도 Codex 앱이 없었는데, 지금은 발표 시간 안에 절반도 보여줄 수 없을 만큼 많은 것을 출시하고 있다고 말하며 데모를 시작했습니다.

1. **Ultrafast로 3D 월드 실시간 편집**: 행사장을 3D로 구현한 월드에서 "무대로 날아가줘", "Dot들을 자리에 앉혀줘", "라이브 스트림을 큰 화면에 띄워줘" 같은 지시가 거의 실시간으로 반영되었습니다.
2. **새로워진 Codex CLI**: 빈 React 프로젝트에서 "참석자 3명을 무작위로 뽑아 내년 무료 티켓을 주는 앱"을 만들고, 곧바로 6명으로 변경했습니다. 원래는 GPT-Live 기반 음성으로 실시간 조정(steering)하는 기능을 보여줄 예정이었지만, 현장 음성 문제로 텍스트로 진행했습니다. 받아쓰기가 아니라 음성으로 작업 도중 실시간 반응할 수 있다는 점이 강조되었습니다.
3. **Astra Adventures**: 종이 스케치에서 시작한 3D 우주 비행 게임을 몇 번의 턴만에 수준 높은 그래픽으로 발전시켰고, 이어서 Astra가 computer use로 직접 게임을 플레이하는 모습을 보여줬습니다. 화면 한쪽에는 모델의 판단이, 다른 쪽에는 입력 중인 키가 표시되었습니다.
4. **App shot 기반 앱 감사**: 앱 스크린샷(app shot)과 함께 "여러 화면 크기에서 앱을 감사해줘"라고 지시하자, Codex가 시뮬레이터를 조작하며 기능을 하나씩 테스트했습니다. App shot이 컨텍스트를 제공해 Codex가 해당 앱을 탐색하는 방법을 익히는 방식입니다.
5. **클라우드로 대형 작업 위임**: "백엔드 전체를 Rust로 다시 작성해줘" 같은 장시간 작업을 클라우드 태스크로 보내고, 나중에 확인한 뒤 로컬로 handoff할 수 있습니다.
6. **멀티모달 하드웨어 데모**: 이미지 생성, 음성 등을 Codex로 연결해 오리 모양의 작은 로봇 "Lavender"를 만들었습니다. 청중을 보고 그림을 그리고, 꽥꽥 소리로 반응했습니다. Romain은 이 API들을 하드웨어와 결합하면 로봇이 실시간으로 본 것을 바탕으로 빠르게 행동하도록 도울 수 있다고 강조했습니다.

## 8. 개발자 플랫폼 (3): 유통

세 번째 축은 개발자가 만든 제품을 사람들이 발견하고, 그것으로 비즈니스를 만들 수 있도록 돕는 것입니다. ChatGPT의 사용자는 약 12억 명에 이릅니다.

### Sign in with ChatGPT

사용자가 ChatGPT 계정으로 개발자의 앱에 로그인하면, 자신이 ChatGPT 요금제에서 사용하는 토큰을 그대로 그 앱에서 쓸 수 있습니다. 사용자는 이미 AI 구독료를 내고 있으니 새 제품을 시도하기 쉬워지고, 개발자는 사용자의 추론 비용을 대신 부담하지 않아도 됩니다. 16개 launch partner와 함께 시작하며, 보도에 따르면 Devin, Notion, Vercel 등이 포함됩니다.

### Plugin Extensions와 Sites

**Plugin extensions**를 통해 개발자는 ChatGPT와 Codex 안에서 동작하는 에디터, 대시보드, 워크스페이스를 만들 수 있습니다. 발표에서 소개된 예시는 다음과 같습니다.

- 캘린더의 다가오는 회의를 보고 ChatGPT 안에서 메모 작성
- 디자인을 열어 팀원 댓글을 확인하고 ChatGPT에 수정 요청
- Adobe의 사례

이 plugin들은 ChatGPT **Sites**에도 넣을 수 있습니다. Sites는 출시 몇 달 만에 수백만 개가 만들어졌으며, 사용자에 따라 경험이 달라지는 개인화된 소프트웨어를 쉽게 만들 수 있습니다.

발견 측면에서도 변화가 있습니다. 대화 흐름 안에서 ChatGPT가 특정 plugin이 도움이 될 것 같다고 판단하면 그 자리에서 연결을 제안합니다. 또한 plugin 제출 과정을 단순화해, 처음부터 다시 제출하지 않고 사람 리뷰를 요청할 수 있게 되었습니다.

### OpenAI Marketplace와 Baseten

![OpenAI Marketplace 발표 장면]({{ '/img/reviews/2026/openai-devday-2026-keynote/devday2026_11_marketplace.jpg' | relative_url }})

*출처: OpenAI DevDay 2026 Keynote (YouTube), 47:40 부근*

제품 판매를 돕기 위한 **OpenAI Marketplace**도 발표되었습니다. 30개 이상의 launch partner가 참여하며, Enterprise 고객은 OpenAI와 맺은 기존 약정 금액(commitment)을 파트너 제품 구매에 사용할 수 있습니다. 슬라이드에는 Adobe, Figma, Harvey, Notion, ServiceNow, Vercel 등의 로고가 보였습니다.

또한 **Baseten**과의 파트너십을 통해 오픈소스 모델을 오늘부터 이용할 수 있습니다.

## 9. 마무리: 산업혁명이 아닌 르네상스

키노트는 전체 발표를 다시 짚으며 마무리되었습니다. 새로운 업무 방식으로서의 Dots와 Space, 새로운 모델인 GPT-6.1 Sol과 Ultrafast, 클라우드로 간 Codex, 그리고 비즈니스를 도울 유통 수단입니다.

이어 개발자들의 이야기를 담은 영상이 상영되었고, 오후에는 오픈소스에 대한 지속적인 투자를 다루는 별도 세션이 예고되었습니다. 현장 참석자에게는 특별 에디션 기념품이 제공되었고, 발표가 너무 많아 회사 이름을 바꾸자는 캠페인까지 있었다는 농담과 함께 "리셋" 버튼을 누르는 퍼포먼스도 있었습니다. 영상만으로는 이 퍼포먼스가 정확히 무엇을 초기화했는지(예: 사용량 한도 초기화 등) 확인하기 어렵습니다.

Altman의 마지막 메시지는 AI를 흔히 산업혁명에 비유하지만, 제대로 해낸다면 사람을 기계의 부품으로 만드는 산업혁명보다는 르네상스에 가까운 미래가 될 수 있다는 것이었습니다. AI는 사람들이 자기 삶에서 더 많은 힘을 갖게 하는 것이어야 한다는 말로 키노트가 끝났습니다.

## 실무 관점에서 읽는 이번 발표

데이터 사이언스와 ML 실무자 입장에서 이번 발표를 해석하면 몇 가지 포인트가 보입니다.

**첫째, 모델 선택이 "최고 성능"에서 "비용-성능 곡선 위의 점"으로 바뀌고 있습니다.** GPT-6.1 Sol 슬라이드가 정확도 단일 지표가 아니라 cost per task 축 위의 곡선을 보여준 것이 상징적입니다. 에이전트 워크로드에서는 Astra를 기본으로 쓰기보다, 대부분의 턴을 Sol로 처리하고 어려운 단계만 Astra로 올리는 라우팅 설계를 검토할 만합니다.

**둘째, 에이전트 파이프라인이 속도 계층별로 분화하고 있습니다.** 정리하면 다음과 같은 계층 구조로 볼 수 있습니다.

```text
[빠른 판단 계층]   Decisions API (Luna)   : 라우팅, 분류, 다음 행동 선택 (< 1s)
        |
[주력 실행 계층]   GPT-6.1 Sol            : 대부분의 추론·코딩·도구 호출 (저비용, 캐시 활용)
        |
[고난도 계층]      GPT-6 Astra (+Ultrafast): 복잡한 계획, 난도 높은 문제 (고비용, 고속 옵션)
```

이 구조는 기존 ML 시스템의 cascade classifier, 즉 저렴한 모델로 대부분의 샘플을 처리하고 불확실한 샘플만 비싼 모델로 넘기는 설계와 같은 발상입니다.

**셋째, 캐시 가격 설계가 아키텍처 결정을 좌우합니다.** Cached input이 일반 input의 1/20이라면, 프롬프트에서 변하지 않는 부분(시스템 지침, 도구 정의, 참조 문서)을 앞쪽에 고정하고 변하는 부분을 뒤쪽에 두는 prefix 설계가 비용에 직접 영향을 줍니다.

**넷째, 데이터 거버넌스 요구가 있는 조직이라면 Private Intelligence가 도입 결정의 핵심 변수가 될 수 있습니다.** ZDR 환경에서도 안전성 검토가 가능해졌다는 점, 그리고 Private Inference가 confidential computing 기반이라는 점은 규제 산업에서 에이전트 도입 장벽을 낮출 수 있습니다. 다만 Private Inference는 아직 preview 예정 단계입니다.

## 결론

### RECAP

- **Dots**: GPT-6 Astra 기반의 상시 동작 개인 에이전트입니다. 단일 작업이 아니라 지속적인 책임을 위임받으며, 자체 클라우드 컴퓨터와 사용자 권한, 기존 plugin을 활용합니다. ChatGPT, Slack, Teams, 문자, 전화로 대화할 수 있습니다.
- **ChatGPT Space**: 팀과 팀의 Dots가 Page, 차트, Sheets, 프로토타입 위에서 함께 일하는 협업 공간이며, Collaborative Slides가 곧 추가됩니다. Enterprise용 Specialist Dots와 Microsoft 연동도 발표되었습니다.
- **모델**: Astra에 근접한 성능을 약 1/5 가격에 제공하는 GPT-6.1 Sol, 초당 최대 300 토큰의 Ultrafast 티어, Pro 500 신설과 Pro 200 재개, 1초 미만 응답의 Decisions API가 공개되었습니다.
- **연구**: AI research intern 목표를 달성했으며, 모델이 하루짜리 연구 과제의 3분의 1 이상을 개입 없이 수행합니다.
- **도구**: 오픈소스 Codex harness, Codex Cloud, Codex Security Cloud, Agents API와 computer use, Bedrock Managed Agents, OpenAI Private Intelligence가 발표되었고, TTFT가 45% 단축되었습니다.
- **유통**: Sign in with ChatGPT(16개 파트너), plugin extensions와 Sites, 대화 중 plugin 발견, OpenAI Marketplace(30개 이상 파트너), Baseten을 통한 오픈소스 모델 제공이 발표되었습니다.

### Key Takeaway

이번 DevDay의 핵심은 개별 기능보다 방향성에 있습니다. OpenAI는 모델, harness, 실행 환경, 권한 체계, 협업 공간, 유통 채널을 하나로 엮어 "에이전트가 일하는 운영체제"를 만들고 있습니다. 개발자에게는 같은 harness와 Agents API를 열어 그 위에서 제품을 만들게 하고, Sign in with ChatGPT와 Marketplace로 그 제품이 12억 사용자에게 닿을 경로까지 제공하겠다는 전략입니다. 모델 측면에서는 단일 최고 모델 경쟁보다 속도, 비용, 지능을 조합하는 계층형 설계가 실무의 기본값이 되어가고 있음을 보여준 발표였습니다.

### 이 글에서 다루지 못한 세부 주제

- 키노트 전반부 Dots 소개 영상의 개별 시나리오(웨딩 플래닝, 방과후 수업 등록 등)의 세부 대화 흐름
- Team Tasks, Meetings plugin, Shareable Profiles, Plugin Creator, Code Review(GitHub/GitLab) 등 키노트 본 발표 외 보도로만 확인된 부가 기능
- GPT-6.1 Sol의 벤치마크별 상세 수치와 Ultrafast의 정확한 API 가격 배수
- 오후 세션(오픈소스 투자 관련 특별 세션) 및 폐막 세션의 내용

---

**참고 자료**

- [OpenAI DevDay 2026 Keynote (FULL) - YouTube](https://www.youtube.com/watch?v=Fls_onRviPM)
- [Everything OpenAI announced at the DevDay 2026 keynote - RuntimeWire](https://runtimewire.com/article/everything-openai-announced-at-the-devday-2026-keynote)
- [OpenAI DevDay 2026 Announcements: Dots, GPT-6.1 Sol, Ultrafast, and Codex Cloud - BenchLM.ai](https://benchlm.ai/blog/posts/openai-devday-2026)
- [OpenAI DevDay 2026: Live updates and announcements - CNBC](https://www.cnbc.com/2026/09/29/openai-devday-2026-live-updates.html)
- [Everything OpenAI Announced At DevDay 2026 - BGR](https://www.bgr.com/2272332/openai-devday-2026-announcements/)
- [OpenAI makes 20+ announcements at DevDay - 9to5Mac](https://9to5mac.com/2026/09/29/openai-teases-20-announcements-at-devday-watch-live/)

*본문 이미지는 모두 위 YouTube 키노트 영상의 캡처입니다.*
