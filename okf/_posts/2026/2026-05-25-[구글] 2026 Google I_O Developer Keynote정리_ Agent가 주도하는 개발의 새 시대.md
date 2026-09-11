---
title: "[구글] 2026 Google I/O Developer Keynote정리: Agent가 주도하는 개발의 새 시대"
date: "2026-05-25"
tags:
  - "google"
year: "2026"
---

# [구글] 2026 Google I/O Developer Keynote정리: Agent가 주도하는 개발의 새 시대

> <https://youtu.be/aqmpZocmR8o>

들어가며
----

Google I/O '26 Developer Keynote는 한마디로 정리할 수 있는 행사였습니다. "AI가 단순히 보조하는 시대는 끝났고, 이제 Agent가 직접 일을 처리하는 시대가 시작되었다"는 선언입니다. 이번 키노트의 핵심 메시지는 단순하면서도 강력합니다. 개발자는 큰 아이디어와 방향성에 집중하고, 무거운 실행 작업은 Agent에게 위임한다는 것입니다.

Google AI Studio, Antigravity, Android, Chrome에 이르기까지 모든 개발 surface에 Agent 기반 워크플로우가 통합되었습니다. 특히 Logan Kilpatrick이 무대에서 던진 "Markdown이 가장 핫한 새로운 프로그래밍 언어"라는 농담은 이번 키노트의 본질을 잘 보여줍니다. 복잡한 오케스트레이션 코드를 작성하지 않고도 자연어에 가까운 markdown 파일만으로 Agent의 능력과 행동 방식을 정의할 수 있게 된 것입니다.

본 글에서는 발표 타임라인을 따라 각 섹션의 모든 발표 내용을 자세히 풀어 정리합니다.

---

1. Introduction
---------------

### 1.1 Josh Woodward의 환영사

키노트의 첫 무대는 Josh Woodward의 인사로 시작되었습니다. 그는 1년 전 I/O를 돌이켜보며 그동안의 빠른 발전 속도가 얼마나 놀라운 것인지를 강조했습니다. 1년이라는 시간 동안 AI 개발 도구의 풍경이 완전히 달라졌다는 점을 청중과 공유하면서, 오전 키노트에서 공개된 Gemini 모델 라인업을 다시 짚는 것으로 본론에 들어갔습니다.

### 1.2 오전 키노트에서 공개된 모델 라인업

오전 세션에서는 새로운 Omni 모델과 Gemini 3.5 series가 공개되었습니다. Omni 모델은 멀티모달 통합 모델로 자리매김하며, Gemini 3.5 series는 차세대 플래그십 모델군으로 발표되었습니다.

한편 Josh는 지난달 Apache 2.0 라이선스로 이미 출시된 Gemma 4도 함께 언급했습니다. Gemma 4는 이번 Developer Keynote에서 가장 집중적으로 다뤄진 모델로, Google의 가장 똑똑한 오픈 모델입니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/0f3f8cf8-2660-4026-85ae-145357bc2743/image.png)

### 1.3 Gemma 4의 놀라운 성과

Josh가 Gemma 4에 대해 들려준 이야기는 인상적이었습니다. Gemma 4는 advanced reasoning과 agentic workflow를 위해 purpose-built 설계된 모델로, 출시 후 첫 달 만에 1억 다운로드를 돌파했습니다. 이로써 Gemma 시리즈의 누적 다운로드는 5억 회를 넘어섰습니다.

특히 흥미로운 점은 Gemma 4가 폰에서 오프라인으로 실행될 수 있을 만큼 작은 footprint에 massive intelligence를 압축했다는 사실입니다. 그 결과 Gemma 4는 로봇부터 우주 위성에 이르기까지 광범위한 환경에 배포되고 있으며, 이는 AI 모델이 더 이상 거대한 클라우드 인프라에만 의존하지 않는다는 변화를 상징합니다.

### 1.4 Agent 시대로의 전환 선언

이어서 Josh는 이번 키노트의 가장 큰 축이 무엇인지 명확히 했습니다. 그는 다음과 같이 말했습니다.

> "the big shift is our move towards agents, from AI that simply assists you to agents that help you get stuff done under your direction and faster."

![](https://velog.velcdn.com/images/euisuk-chung/post/36b5d8a8-92b6-40c0-9ffe-594abe7cd046/image.png)

이 문장의 핵심은 "단순히 보조하는 AI"에서 "사용자의 지시 아래 실제 일을 수행하고 더 빠르게 결과를 만들어내는 Agent"로의 이동입니다. 두 표현 사이에는 미묘하지만 결정적인 차이가 있습니다. 보조하는 AI는 사용자가 모든 결정을 내리고 매 단계마다 개입해야 하지만, Agent는 큰 방향성만 받으면 세부 실행을 스스로 진행합니다. 이 차이가 이번 행사 전체를 관통하는 주제입니다.

### 1.5 Google Antigravity의 전략적 위치

Josh는 이 모든 전환의 중심에 Google Antigravity가 있다고 선언했습니다. Antigravity는 Agent를 활용해 빌드할 수 있게 해주는 agentic development platform으로, 플랫폼의 핵심은 Antigravity Agent 자체입니다. 중요한 점은 이 플랫폼이 어디서든 동작한다는 것입니다. Google 인프라 위에서든 자체 인프라 위에서든, Android에서든 웹에서든 모두 지원됩니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/137fed24-b201-434e-af8f-2651fccbd432/image.png)

### 1.6 Google 전체의 풀스택 통합 전략

키노트 도입부의 마지막에서 Josh는 한 발 물러서서 Google의 전체 전략을 제시했습니다. Cutting-edge model인 Gemini와 Gemma가 가장 아래층에 있고, 그 위에 Antigravity 같은 agentic tools가 있으며, 그 위에는 사용자가 마법을 경험하는 다양한 플랫폼이 있고, 이 모든 것을 가능하게 하는 인프라가 함께 작동합니다. Google은 이 스택의 위아래에서 개발자를 돕는다는 전략을 분명히 했습니다.

---

2. Building Agents
------------------

### 2.1 Logan Kilpatrick의 등장과 Agent의 활용 영역

Logan Kilpatrick이 무대에 올라 본격적인 첫 섹션을 시작했습니다. 그는 최신 모델들이 "**다음 시대의 Agent를 빌드하기 위한**" 것임을 강조하며, Agent의 강력함을 개발자의 손에 직접 쥐어주는 것이 Google의 목표라고 설명했습니다.

Agent가 처리할 수 있는 작업의 범위를 농담을 섞어 나열했는데, 복잡한 research 작업, Data Science 작업, 그리고 "개인 라디오 쇼 만들기"까지 언급했습니다. 마지막 농담은 단순한 우스개가 아니라 뒤에 이어질 데모에서 실제로 시연될 시나리오를 미리 예고한 복선이었습니다.

### 2.2 Interactions API와 Deep Research의 의미

작년 12월에 도입된 Interactions API는 모델과 Agent 모두를 위한 하나의 단순하고 강력한 인터페이스입니다. 그리고 이 API를 통해 처음으로 외부에 공개된 Agent가 바로 Deep Research였습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/027a9df5-bc41-4dd0-af7d-acb7fcb32cbb/image.png)

Deep Research가 보여준 것은 단순한 검색 기능이 아니라 패러다임의 변화였습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/0f5c7e72-6bd5-49b8-87a0-6dedaa71e01d/image.png)

모델에게 단순히 질문을 하는 것이 아니라, 목표(goal)를 주고 답을 찾으러 갈 자유(freedom to go find the answer)를 함께 주었을 때 무엇이 가능한지를 입증한 사례였습니다. Logan은 이것이 "그저 시작이었다"고 강조하며, 이번에 공개될 것들은 그 시작을 훨씬 뛰어넘는 규모임을 암시했습니다.

### 2.3 Antigravity Harness의 외부 개방

Google 내부에서는 그동안 Antigravity Harness라는 기술을 사용해 Agent들이 가장 복잡한 작업을 지능적으로 처리해 왔습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/a847a59d-eebc-414a-9640-8ebc57d8c84c/image.png)

이 기술은 Gemini Spark와 Google AI Studio의 coding agent를 뒷받침해 온 백본이었습니다. 즉, Google이 자체 제품에서 검증해 온 핵심 기술이 이제 외부 개발자에게도 공개되는 것입니다.

이것이 바로 Managed Agents in the Gemini API라는 이름으로 등장한 새 기능입니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/a718a10d-715c-473f-ab25-9eff610bd36d/image.png)

### 2.4 Managed Agents의 핵심 구조

Managed Agents를 시작하는 방식은 매우 단순합니다. 단일 Gemini API 호출 안에 `custom instructions`, `tools`, `data`만 추가하면 됩니다. 별도의 복잡한 SDK 설정이나 인프라 구성이 필요 없다는 점이 핵심입니다.

하지만 Agent를 빌드하는 것은 퍼즐의 한 조각일 뿐입니다. 프로덕션 환경에서 Agent를 운영하려면 안전하고 격리된 실행 환경이 필요한데, 이를 직접 구축하는 것은 Logan의 표현을 빌리자면 "인프라 악몽"입니다. 권한 격리, sandbox 관리, 보안 검증, 리소스 할당까지 모두 직접 해결해야 하기 때문입니다.

Managed Agents의 진정한 가치는 바로 이 지점에서 드러납니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/7a8c495c-4aa8-487f-893f-c29698f19ce2/image.png)

모든 managed agent에는 Google이 호스팅하는 remote Linux environment가 페어링되어 제공되며, 단일 API 호출만으로 Agent와 sandbox를 동시에 획득할 수 있습니다. Google이 인프라를 처리하므로 개발자는 빌드 자체에만 집중하면 됩니다.

### 2.5 내부 도입 사례: Stitch

Managed Agents가 단순한 컨셉이 아니라 실제로 작동하는 시스템임을 보여주기 위해 Logan은 내부 도입 사례인 Stitch를 소개했습니다. Stitch는 Labs의 vibe design 제품으로, 사용자가 자신의 codebase에서 design system을 직접 import할 수 있도록 합니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/011e18b2-b23d-4e85-a0ff-e268d8029ccf/image.png)

Stitch의 동작 방식을 따라가 보면 Managed Agent의 활용법이 명확해집니다. 사용자의 GitHub 저장소에 연결한 후, Agent가 codebase를

![](https://velog.velcdn.com/images/euisuk-chung/post/8671e95f-fbfc-4fbf-90e4-467b116c8367/image.png)

분석하여 사용 가능한 design.md 파일을 생성합니다. 그러면 Stitch는 이 파일을 기반으로 브랜드에 맞는 디자인을 만들어냅니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/62ca5b7e-bc39-49d7-a30c-ac23b2e3339b/image.png)

그리고 이 모든 작업이 managed agent로 동작하기 때문에 Google이 인프라를 처리해주며, Stitch는 수백만 사용자로 확장할 수 있습니다.

### 2.6 외부 Early Access 고객

내부 사례 외에도 Ramp, Resemble AI, Klipy 같은 외부 early access 고객들이 이미 Managed Agents를 활용하고 있으며, 이들 모두 전례 없는 속도로 Agent를 빌드하는 경험을 하고 있다고 Logan은 언급했습니다. 그리고 Managed Agents는 오늘부터 사용 가능하며, 생태계 파트너 덕분에 첫날부터 개발자가 선호하는 스택으로 바로 빌드를 시작할 수 있습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/9f6c4a63-42b4-4228-b491-236e1bcce53d/image.png)

### 2.7 AI Studio Playground와 AI Talk Radio Agent 데모

Logan은 이제 직접 AI Studio playground로 이동해 데모를 시작했습니다. Playground는 올해 초 Agent와의 상호작용 지원이 추가된 환경입니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/4e746a00-e306-4c53-847d-829d37f9b6d1/image.png)

신규 사용자가 즉시 실행할 수 있도록 새로운 **custom agent 세트**가 추가되었는데, 이 **open-source agent template**들은 instructions, skills, tools를 모두 markdown 형식으로 preload하고 있어 Customer Support Agent 같은 source 파일을 자유롭게 커스터마이즈할 수 있습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/c31a3fc6-1fe0-4325-b80f-a919a1f26990/image.png)

도입부에서 던졌던 농담을 회수할 시간이 왔습니다. Logan은 AI Talk Radio Agent를 선택했습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/543de843-de08-49af-923d-42426a7c0178/image.png)

이 Agent는 주제만 주면 완성된 talk radio show를 생성하는 Agent로, Logan은 "오늘의 최신 기술 뉴스를 다루는 5분짜리 라디오 쇼를 Hacker News 최신 글 기반으로 생성해 달라"고 요청했습니다.

### 2.8 Agents.md 파일이 보여주는 새 패러다임

Agent 환경이 provisioning되어 실행 준비를 하는 동안, Logan은 Agents.md 파일을 열어 안에 정의된 skill들을 보여주었습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/72a09793-fb26-4cb8-9604-68607f7170a5/image.png)

여기에는 Research(Hacker News에서 top text story 수집), Script Writing(쇼 스크립트 작성), TTS Generation(다중 화자 음성 생성), Music Generation(Lyria로 동적 배경 음악 생성), Audio Mixing(모든 오디오 통합), 그리고 Metadata Generation(Nano Banana로 커버 아트 생성)이라는 skill들이 markdown 형식으로 나열되어 있었습니다. 최종 산출물은 sandbox 환경에 저장되는 ready-to-stream MP3 파일이었습니다.

여기서 Logan이 강조한 핵심은 별도의 orchestration logic을 작성하지 않았다는 점이었습니다. 단지 skill과 tool을 markdown 파일에 정의했을 뿐인데 Agent가 나머지를 모두 처리한다는 사실입니다. 그래서 그는 다음과 같이 말했습니다.

> "the hottest new programming language is markdown, and I'm here for it."

이 한 문장이 Managed Agent 패러다임의 본질을 압축합니다. 코드 대신 자연어에 가까운 markdown으로 Agent를 정의하고, harness가 이를 해석해 실행하는 구조입니다. 이는 LLM의 in-context learning 강점을 시스템 아키텍처 레벨로 끌어올린 설계라고 볼 수 있습니다.

### 2.9 데모 결과 확인

Agent 실행에는 몇 분이 걸리므로 Logan은 미리 실행해 둔 결과로 이동했습니다. Research, script, speech, music, mixing, image generation이 모두 완료된 깔끔한 요약이 표시되었고, 이 모든 것이 단일 API 호출로 처리되었다는 사실이 강조되었습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/70c9877b-ef0e-4104-841f-e8c85f85bdeb/image.png)

### 2.10 Paige Bailey의 등장: Playground에서 실제 앱으로

Paige Bailey가 이어서 무대에 올라 "AI Studio는 prompt에서 app까지 가장 빠른 경로"임을 강조하며 데모를 이어갔습니다. 그녀는 동일한 AI Talk Radio Agent를 단지 몇 개의 prompt만으로 실제 앱으로 감쌌다고 설명했습니다. Hacker News의 열렬한 팬임을 농담으로 덧붙이며 데모를 진행했습니다.

앱의 동작 흐름은 다음과 같습니다. 앱이 Gemini API의 Managed Agent를 호출하면, Agent가 sandbox 환경에서 spin up되어 skill들을 읽고 plan을 수립한 다음 전체 episode를 조립합니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/b09344d3-50e2-4dbd-af6c-6927101c1947/image.png)

생성에 시간이 걸리므로 Paige는 미리 실행해 둔 결과를 청취했고, 라디오 쇼에서는 다음과 같은 대사가 나왔습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/9159ce80-51ef-400a-8f67-f8adfd6f2736/image.png)

> (도입부) "If you can go from writing 200 lines of code a day to 2,000 with an AI agent, are you actually a better engineer? Or are you just vibing?" ...

흥미로운 점은 Agent가 MP3와 함께 메타데이터까지 생성했다는 사실입니다. 메타데이터에는 스크립트가 포함되어 있어 화자별로 점프할 수 있었고, 커버 아트는 Nano Banana로 생성되었습니다.

Paige가 강조한 분업 구조는 다음과 같습니다.

앱이 UX(사용자 경험)를 정의하고, Agent가 즉석에서 콘텐츠와 메타데이터를 만들어 채워 넣는다는 구조입니다. Playground는 실험용이고 Build는 출하용이라는 깔끔한 정리도 함께 제시되었습니다.

### 2.11 Cloud Run으로의 즉시 배포

만든 앱을 세상에 공유하기 위해 Paige는 Cloud Run으로의 배포를 시연했습니다. AI Studio에서 Cloud Run으로의 배포는 클릭 몇 번이면 완료됩니다. 기존 Google Cloud project를 선택할 수도 있고, 없을 경우 AI Studio가 자동으로 생성해 줍니다. 더 인상적인 발표는 오늘부터 신규 사용자가 신용카드 없이 라이브 URL로 즉시 배포할 수 있다는 점이었습니다. 진입 장벽을 거의 0에 가깝게 낮춘 셈입니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/cab15704-95b1-4ec7-9158-ebc13dcb8bf7/image.png)

### 2.12 AI Studio의 최근 통합 사항들

Cloud Run은 최신 통합 중 하나일 뿐이며, Paige는 다른 통합 사항들도 함께 소개했습니다. Coding Agent가 Antigravity로 재구축되었고, Firebase와 Firestore 지원이 추가되어 데이터베이스와 OAuth 기반의 풀스택 앱을 쉽게 빌드할 수 있게 되었습니다.

오늘 공식 발표된 가장 큰 통합은 Google Workspace 공식 지원입니다. Docs, Gmail, Calendar 같은 앱을 prompt로 연결할 수 있게 되어 개발 flow를 끊지 않고도 외부 서비스와 통합할 수 있게 되었습니다. 여기에 multichat, web search, Nano Banana 이미지 생성을 결합하면, Paige의 표현대로 "Agent로 빌드할 수 있는 것의 정의를 완전히 새로 쓰는" 수준이 됩니다.

데모 도중 앱이 deploy 완료되어 상태, 라이브 URL, "Unpublish" 버튼이 AI Studio를 떠나지 않고도 모두 표시되는 모습이 시연되었습니다.

### 2.13 AI Studio에서 Android 앱 빌드

Paige는 "라디오 쇼인데 이동 중에 못 들으면 의미가 없다"는 자연스러운 흐름으로 Android 빌드로 전환했습니다. 오늘부터 AI Studio에서 Android 앱을 직접 빌드할 수 있는데, 가장 인상적인 부분은 진입 장벽이 거의 없다는 점입니다. 설치할 소프트웨어도, 관리할 SDK도, 필요한 로컬 환경도 없습니다.

시작 방법은 매우 단순합니다. "Build an Android app"을 선택하고 prompting을 시작하기만 하면 됩니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/5f9acf02-571c-4536-b5d9-b5b03ea61e18/image.png)

Paige는 동일한 prompt로 미리 만들어 둔 Android 앱을 보여주었는데, 앱은 전적으로 Kotlin으로 작성되어 있었습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/9fd842c3-5499-4d9e-a25c-11540388854b/image.png)

Compose 기반의 최신 Android 개발 표준을 따른다는 의미입니다. (~~와.. 안드로이드 APP을 그냥 만들어버리네...~~)

### 2.14 Emulator, 디바이스 테스트, 그리고 Play Store 배포

빌드된 앱은 AI Studio 내장 Android Emulator에서 미리볼 수 있고, 자체 디바이스에서 테스트하려면 폰을 USB로 연결해 설치할 수 있습니다. 여기서 Paige가 발표한 큰 소식은 Google Play Store 게시 지원이 추가되었다는 점입니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/a9e46635-78cc-47af-8f32-63182fa40ae3/image.png)

배포 흐름도 매우 매끄럽습니다. "Publish"를 열어 Play Developer Account를 연결하면, A**I Studio를 떠나지 않고도 test track으로 앱을 푸시**할 수 있습니다. 그 후 폰에 설치할 수 있게 됩니다. 자체 디바이스 테스트는 오늘부터 가능하며, 신뢰된 테스터와의 공유 기능은 올해 여름 후반에 출시될 예정입니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/2c39ff23-85d1-4b42-8173-9fc82f8bf2a3/image.png)

여기서 끝이 아닙니다. "좋은 아이디어는 책상에서만 떠오르는 게 아니다"라는 점을 들어, AI Studio Build 경험을 모바일 앱으로 이식한다는 발표도 이어졌습니다. AI Studio 모바일 앱은 몇 주 내에 롤아웃되며 사전 등록이 가능합니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/626f1032-dad0-4f48-b200-681265e91e30/image.png)

> <https://aistudio.google.com/mobile>

### 2.15 Antigravity SDK와 One-Click Export

Managed Agents가 setup 부담 없는 강력한 옵션이라면, 완전한 프로그래밍 가능성과 제어를 원하는 개발자들도 있습니다. 이들을 위해 **Antigravity SDK**가 새로 출시됩니다. Gemini에 최적화된 동일한 agent harness를 제공하지만, 어디서든 어떻게든 실행할 수 있는 궁극의 유연성을 갖춘 것이 특징입니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/01643e97-94db-45d4-8d16-e5870be341c5/image.png)

Paige는 Agent 구축이 "단일 이벤트가 아닌 전체 라이프사이클"임을 강조하면서, 팀이 성장하면 로컬 개발 플랫폼으로의 이동이 빠른 iteration에 도움이 된다고 설명했습니다. 문제는 기존 방식이 파일을 복사하고, context를 잃고, 상태를 다시 빌드해야 하는 번거로운 과정이었다는 점입니다.

이를 해결하기 위해 출시된 것이 One-click export to Antigravity입니다. 단순한 snippet 전송이 아니라 전체 파일 시스템과 모든 context를 포팅하기 때문에, AI Studio에서 작업하던 정확히 그 지점에서 Antigravity로 이어서 작업할 수 있습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/002e3349-6f74-416b-858b-47237048c93f/image.png)

---

3. Antigravity
--------------

### 3.1 Anshul Ramachandran의 메시지

Anshul Ramachandran이 무대에 올라 Antigravity 섹션을 시작했습니다. 그의 첫 메시지는 명확했습니다. "Agent를 더 쉽게 빌드하는 것뿐 아니라, Agent와 함께 더 쉽게 빌드할 수 있도록 한다"는 것입니다. Build agents와 build with agents의 미묘한 차이를 강조하는 메시지였습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/4e907a3f-93d9-457d-aacf-9f839efb65af/image.png)

### 3.2 Google Antigravity 2.0의 정체

오전 키노트에서 소개된 Google Antigravity 2.0의 상세 정보가 이 섹션에서 공개되었습니다. Antigravity 2.0은 새로운 데스크톱 애플리케이션으로, Anshul의 표현을 빌리면 "unabashedly agent first"입니다. 즉, 기존 IDE에 Agent 기능을 끼워 넣은 것이 아니라, 처음부터 Agent를 중심에 두고 설계된 환경이라는 의미입니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/990efca9-1146-4cf9-b65e-f24c42b70a90/image.png)

가장 두드러진 특징은 여러 프로젝트에서 **여러 Agent를 동시에 실행할 수 있다는 점**입니다. 구체적인 시나리오를 예로 들면, 한 Agent는 마케팅 웹사이트를 vibe-coding하고, 다른 Agent는 brand asset을 생성하며, 또 다른 Agent는 프로젝트 아키텍처를 plan하는 작업을 동시에 진행할 수 있습니다. 이 모든 작업이 다중 work-tree에서 충돌 없이 협업하는 방식으로 이루어집니다.

코딩 task의 경우 선호하는 IDE와 Antigravity 2.0을 병행 사용할 수 있지만, 코딩만이 전부가 아니라는 점이 중요합니다. Antigravity 2.0은 모든 종류의 Agent 오케스트레이션을 위한 mission control 역할을 합니다.

### 3.3 Dynamic Subagents의 등장

단일 Agent가 거대한 task에 압도되는 문제는 그동안 Agent 시스템의 큰 한계 중 하나였습니다. 너무 큰 작업을 던지면 Agent가 context를 잃고 부정확한 결과를 만들거나 중간에 멈추는 경우가 많았기 때문입니다. 이를 해결하기 위해 도입된 것이 Dynamic Subagents입니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/244c6a4d-f1d9-4364-96e2-5b138d6239d9/image.png)

이제 Agent가 specialized helper를 동적으로 spin up할 수 있습니다. 예를 들어 QA subagent나 Data Science subagent를 띄워 병렬로 작업을 처리합니다. 이는 분할 정복(divide and conquer) 전략을 Agent 시스템에 적용한 것으로, 더 빠르고 효과적인 작업 처리를 가능하게 합니다.

### 3.4 Scheduled Tasks로 Agent를 진정한 Proactive로

다음 기능은 Agent를 진정한 의미에서 proactive하게 만드는 Scheduled Tasks입니다. Agent에 사전 정의된 일정에 따라 task를 반복 실행하도록 지시할 수 있으며, 표준 cron scheduling을 사용합니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/b31d5415-a625-42e9-9e69-32adfc2dc026/image.png)

활용 사례는 매우 실용적입니다.

매일 아침 pending PR을 요약하게 하거나, 매시간 cloud health를 모니터링하도록 할 수 있습니다. Anshul은 이를 "Agent를 autopilot에 올린다"고 표현했는데, 이는 Agent가 더 이상 사용자의 명령을 기다리기만 하는 수동적 존재가 아니라 스스로 주기적으로 일을 처리하는 자율적 존재가 된다는 의미입니다.

### 3.5 Kevin Hou의 등장: Gemma 4 Fine-tuning 데모

Kevin Hou가 무대에 올라 Antigravity 2.0에 challenge를 던졌습니다. 시나리오는 Gemma 4를 직접 fine-tuning하는 것입니다. 오픈 모델인 Gemma 4의 진정한 민주화는 누구나 fine-tune할 수 있게 하는 것이며, 역사적으로 이는 ML 엔지니어의 복잡한 파이프라인 wrangling을 의미했습니다. 하지만 이제는 다르다는 것이 데모의 핵심 주장이었습니다.

Kevin의 동기는 매우 실용적이고 공감 가는 것이었습니다. 며칠 전 본인의 CI 파이프라인이 깨졌고, 거기서 아이디어를 얻은 것입니다.

> "LLM이 파이프라인을 자동으로 self-heal하게 하면 어떨까?"

stack trace를 LLM에 전달하고 "fix this"라고 요청해 remediation BASH command를 받는 시스템을 만들고 싶다는 것이었습니다.

문제는 여기서 발생합니다.

Anshul이 설명한 것처럼, **LLM은 대화형으로 훈련**되어 있어 **bash command를 설명 문단 사이에 묻어버립니다**.

* 예를 들어 간단한 GIT work-tree 명령을 물으면, 두 개의 별도 코드 블록으로 응답하고, 대화형 도입부를 포함하며, branch name 선택 방법에 대한 상세 설명까지 덧붙입니다.
* 하지만 CI 파이프라인에 직접 넘기려면 command 그 자체만 필요합니다.
* 따라서 Gemma 4를 fine-tune해서 **fluff 없이 command만 반환하도록 만드는 것이 목표**입니다.

### 3.6 음성으로 Fine-tuning 시작하기

Kevin은 키보드 대신 마이크로 task를 입력했습니다. 이는 최신 audio understanding 기능을 시연하기 위함이었습니다. 그의 음성 prompt 내용은 이렇습니다.

> *"Gemma 4를 fine-tune해서 추가 fluff 없이 bash command 응답만 받고 싶다. CI 파이프라인에서 응답을 직접 사용할 수 있도록 말이다. prompt-to-bash 명령 데이터셋이 있으니, 이 데이터셋으로 LoRA fine-tuning을 위한 training/eval 코드를 작성해 달라. 그리고 custom Gemma 4 모델을 내 노트북에 deploy하는 코드도 작성해 달라."*

Anshul이 두 가지 포인트를 짚었습니다.  
1. 첫째, Kevin이 음성만 사용했다는 점.  
2. 둘째, Audio 모델이 "LoRA"같은 전문 용어를 정확히 인식했다는 점.

![](https://velog.velcdn.com/images/euisuk-chung/post/c44f3be8-6bd0-473e-a82a-f7ce7f4feee9/image.png)

일반적인 음성 인식 모델이라면 "lora", "Laura" 같은 단어로 잘못 인식할 가능성이 높은데, Gemini의 audio 모델은 기술 용어의 context를 이해하고 정확히 transcribe한 것입니다.

### 3.7 Plan 생성, 승인, 그리고 클라우드 환경 이전

Agent는 약간의 research를 수행한 후 training 코드를 위한 전체 구현 plan을 생성했습니다. Kevin이 plan을 승인하자 Agent는 코드를 작성하기 시작했습니다. Kevin은 이 코드를 자신의 repo에 push하고, 모델 훈련을 위해 GPU 활성화된 cloud machine으로 이동했습니다.

### 3.8 Antigravity CLI의 발표

Kevin이 cloud 준비를 하는 동안 Anshul이 Antigravity CLI라는 또 하나의 중요한 발표를 했습니다. Antigravity 2.0이 mission control이지만, 많은 개발자에게 "진짜 마법은 터미널에서 일어난다"는 점을 짚으며 도입된 도구입니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/ab090508-d951-4730-a93f-c501122e9862/image.png)

Antigravity CLI의 핵심은 Terminal에서 동일한 **Antigravity Agent를 spin up할 수 있는 lightweight 방식**이라는 점입니다. 정확히 동일한 harness와 동일한 모델을 사용하지만, 제품 경험은 **command line에 맞게 조정**되었습니다. 사용자의 theme, workflow, key binding에 완전히 적응합니다. 즉, 새로운 도구를 익히는 부담 없이 기존 터미널 환경에 자연스럽게 녹아드는 도구입니다.

### 3.9 SSH 환경에서 학습 시작

Kevin이 작업을 재개했습니다. GPU 활성화 VM에 SSH로 접속한 상태에서 방금 작성한 training/eval 코드를 pull받았습니다. Antigravity CLI를 이 머신에 미리 설치해 두었기 때문에, 별도 탭에서 GUI 없이 바로 실행할 수 있었습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/f6f94e3e-ca08-4003-a29a-8f10c04f9904/image.png)

Anshul은 이 순간을 강조했습니다. "GUI vs CLI는 대부분 선호의 문제지만, 터미널 안에서 SSH로 연결된 머신을 다루는 Kevin에게는 CLI가 완벽한 선택"이라는 것입니다. 이는 Antigravity가 특정 인터페이스를 강요하지 않고 개발자의 워크플로우에 맞춰 적응한다는 메시지를 보여줍니다.

### 3.10 LoRA 학습과 CLI를 통한 모니터링

Kevin은 Agent에게 방금 작성한 training job을 시작해 달라고 요청했습니다. 컨텍스트는 경량 LoRA fine-tune이지만 결과까지는 시간이 걸린다는 점이었습니다. 핵심 메시지는 이 정도 scale의 빌드를 Antigravity가 얼마나 단순화하는지 보여주는 것이었습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/47f2484f-bcbe-43d9-bcaa-3028c831a732/image.png)

학습이 진행되는 동안 Kevin은 CLI로 sanity check를 수행했습니다. 첫 몇 step의 loss가 올바른 방향으로 trending하는지 확인하기 위해 Agent에게 "training run이 어떻게 진행되고 있나? healthy한가?"라고 질문했습니다. Agent의 동작이 흥미로웠습니다. output 파일들을 살펴보고, 2.0에서 작성한 코드를 다시 읽고, 여러 log 파일을 검토해야 한다고 응답했습니다. 즉, Agent가 단순히 일회성으로 코드를 만든 후 잊는 것이 아니라, 자신이 만든 산출물의 컨텍스트를 유지하며 후속 작업에 활용한다는 것입니다.

### 3.11 /btw 슬래시 명령과 Gemini의 농담

대기 시간 동안 Anshul은 새로운 슬래시 명령인 /btw를 소개했습니다. 이 명령은 같은 대화에서 fork하는 효과를 만들어 줍니다. 즉, 현재 진행 중인 작업의 context는 유지하되 별도의 가지에서 다른 질문을 던질 수 있는 기능입니다.

데모에서 Gemini에게 농담을 요청했고, 다음과 같은 답이 돌아왔습니다.

> "Why did the neural network refuse to run on the TPU? Because it heard the TPU was always a bit too tensor."

Anshul의 평가는 "5/10"이었지만, 청중에게 친근한 분위기를 만들기에는 충분했습니다. (ㅋ...)

![](https://velog.velcdn.com/images/euisuk-chung/post/3ffc0333-312c-4756-a8c7-076b736bc736/image.png)

### 3.12 학습 결과 확인과 모델 배포

학습이 약 1% 진행된 시점에서 gradient norm이 안정적이라는 결과가 확인되었고, Anshul은 "loss가 좋게 줄어들고 run이 완벽하게 healthy하다"고 평가했습니다. 하지만 실시간으로 학습을 끝까지 보여줄 수는 없으므로, Kevin은 사실 동일한 run을 미리 시작해 두고 몇 시간 동안 학습시켜 둔 checkpoint를 보유하고 있었다고 밝혔습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/3d6d7722-ddb3-4a16-bcc4-3777424f9168/image.png)

그 checkpoint를 사용해 결과 모델을 노트북에 deploy하는 작업을 이어갔습니다. Antigravity 2.0으로 돌아가 새 대화를 시작하고, 특정 경로에 지정된 fine-tuned 모델로 playground를 실행하도록 지시했습니다. Antigravity가 server를 실행하고, 로그를 통해 해당 fine-tuned 모델이 실행 중임이 확인되었으며, client도 시작되었습니다.

링크를 클릭한 후 동일한 prompt를 playground에 입력하자, 결과는 명확했습니다. fluff 없이 명령만 반환되는 fine-tune이 완성된 것입니다. Kevin은 "무대 위에서 Gemma 4n을 fine-tune했다. 이미 사용 중인 surface 전반에서 작동하는 새로운 빌드 현실"이라고 마무리했습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/63b2f120-84d2-4fff-8553-e9946a3a1052/image.png)

### 3.13 CLI 통합 정책과 Stack Agnostic 전략

Anshul은 마무리하며 중요한 정책을 발표했습니다. Antigravity가 agent-first 개발에 필요한 유일한 플랫폼으로 통일된다는 것입니다. Gemini CLI에서 배운 통찰을 Antigravity CLI에 반영했고, 오늘부터 모든 Gemini CLI 사용자에게 Antigravity CLI가 제공됩니다. Migration guide도 게시되어 custom skill을 쉽게 포팅할 수 있게 했습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/a59eb26e-f29a-4109-b7c9-8c0a5e7d912b/image.png)

> <https://github.com/google-antigravity/antigravity-cli>

Antigravity는 완전히 stack agnostic이라는 점도 강조되었습니다. **vendor lock-in이 없다**는 의미입니다. 단, Google 생태계에서 빌드한다면 Android, Firebase, Web에 대한 one-click setup이 제공됩니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/d7c800f9-b97c-4f6d-b54d-0515806a10d3/image.png)

### 3.14 Domain-Specific Skill Bundle과 엔터프라이즈 지원

Agent를 매우 특화된 영역으로 밀어 넣기 위한 새로운 카테고리도 발표되었습니다. Domain-Specific Skill Bundle입니다. 첫 번째 릴리즈는 **Science Skill Bundle**로, Agent에 health, biology, scientific research workflow 가속에 필요한 primitive를 제공합니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/6f2a6cbb-384d-42cb-821f-5348547210f2/image.png)

엔터프라이즈 측면에서도 큰 발표가 있었습니다. 오늘부터 **Antigravity가 Google Cloud project에 직접 연결**될 수 있으며, 기대하는 enterprise terms가 동일하게 적용됩니다. 기존 Gemini Enterprise 고객에게는 향후 몇 달 내 Antigravity가 롤아웃됩니다. 한 명의 아이디어를 가진 개발자든, scale에서 배포하는 조직이든, Antigravity가 동일한 플랫폼이 된다는 메시지입니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/2208c348-6b3b-4384-9d3c-d14cc014397b/image.png)

---

4. Android
----------

### 4.1 Florina Muntenescu와 Adarsh Fernando의 등장

Florina Muntenescu와 Adarsh Fernando가 Android 섹션을 시작했습니다. Florina의 첫 메시지는 명확했습니다. "개발자의 여정의 어느 단계에 있든, 고품질 Kotlin Android 앱을 빠르고 쉽게 빌드할 수 있도록 한다"는 것입니다.

### 4.2 Antigravity 공식 Android 지원

Paige의 데모에서 AI Studio에서 native Android 개발이 완전 지원됨이 공개되었는데, 오늘 추가 발표는 Antigravity에도 공식 Android 지원이 추가된다는 것입니다. 이를 통해 어디서든, 어떤 디바이스에서든 가장 performant한 사용자 경험을 만들 수 있게 됩니다. 특히 새로운 form factor에 대응할 때 마찰을 최소화하는 것이 목표라고 강조되었습니다.

### 4.3 데모 앱 소개와 Time Travel Skill

데모용 여행 앱이 소개되었습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/c0645552-190f-4def-99da-1b0538fefac7/image.png)

모든 여행 계획을 한 곳에서 볼 수 있고, 오디오 일기 항목을 on-device 모델인 Gemini Nano 4로 transcribe하는 앱입니다. 흥미로운 점은 Adarsh가 "데모 시간이 부족하니 latest skill인 Time Travel을 사용하겠다"는 농담을 던졌다는 점입니다. 실제로는 결과를 미리 만들어 둔 화면으로 점프한다는 의미인데, 청중에게 부담 없이 데모를 따라가게 만드는 장치였습니다.

### 4.4 Display Glasses용 증강 경험과 Android CLI

Florina의 첫 도전 과제는 Display Glasses용 증강 경험을 빌드하는 것이었습니다. 시나리오는 매우 실용적입니다. 공항에서 양손이 자유롭지 않은 사용자가 안경에서 비행 정보를 바로 확인할 수 있게 하는 것입니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/0fe4dcd2-1bcb-4648-b940-4ccbd126de7c/image.png)

문제는 이런 환경 설정이 그동안 매우 번거로웠다는 점입니다. Android Studio 없이는 환경을 구성하기 어려웠습니다. 이를 해결하기 위해 Antigravity에 새 Android CLI가 내장되었습니다. 이제 안정화된 상태로 SDK 다운로드, 프로젝트 생성, 디바이스에서의 앱 실행 같은 작업을 훨씬 쉽고 효율적으로 처리할 수 있게 되었습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/ef2e0f64-a841-4ee8-b7c5-a0a342708f36/image.png)

데모에서는 단일 prompt만으로 비행/여행 정보를 안경에 표시하는 기능을 추가했습니다. 별도의 SDK 학습이나 환경 구성 없이 자연어 한 줄로 새로운 form factor의 UI를 만든 것입니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/3fb21854-8ee0-479b-aa48-1ae3c0a7132b/image.png)

### 4.5 신규 Form Factor의 LLM 한계 극복

Florina는 중요한 문제를 짚었습니다. Display Glasses 빌드는 새로운 분야이고, 대부분의 LLM은 아직 이를 빌드하는 방법을 모른다는 것입니다. 학습 데이터에 충분한 예시가 없기 때문입니다. 그래서 Android CLI는 모델에 최신 정보 접근을 두 가지 핵심 리소스로 제공합니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/869dc5e1-a880-4a8e-adb7-ec7249df6cde/image.png)

첫 번째는 Android Knowledge Base입니다.

specialized data source로, Agent가 최신 개발자 가이던스를 search and fetch할 수 있게 합니다. 즉, 학습 데이터의 cutoff와 무관하게 최신 정보를 활용할 수 있는 것입니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/19642421-4e51-4b37-8a07-8c3dc3c072eb/image.png)

두 번째는 Android Skills입니다.

LLM이 best practice를 이해하고 실행하도록 돕기 위해 Android Skills가 open-source화되었습니다. 사용자 피드백에 기반해 시간이 많이 걸리는 작업에 대한 skill도 추가되었는데, edge-to-edge 지원 빌드, XML에서 Compose로 마이그레이션, Jetpack Navigation 3로 마이그레이션 같은 항목이 포함됩니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/585bb854-30a8-4e1a-8a80-313f1075edef/image.png)

### 4.6 인상적인 성능 지표

내부 테스트 결과 Android CLI의 skill과 Knowledge Base를 활용한 Agent는 약 70% 더 적은 토큰을 사용했고, 작업 완료 시간이 최대 3배 단축되었습니다. 이는 단순히 빠르다는 의미를 넘어, 비용도 크게 절감되고 응답 시간도 짧아져 개발자 경험 자체가 질적으로 달라진다는 의미입니다. 도메인 특화 skill 주입의 효용성을 정량적으로 입증한 수치입니다.

### 4.7 Android Studio의 Capability 접근

Android CLI는 Android Studio의 강력한 capability에도 접근할 수 있습니다. finding usages and declarations, 파일 분석을 통한 issue 탐지, 의존성 최신 정보 조회 같은 기능들입니다. Android Studio를 Antigravity와 병행 실행하면 Agent가 이런 capability를 사용자 통제 하에 활용해 task를 더 빠르고 효율적으로 처리합니다.

### 4.8 Display Glasses UI 빌드 결과 분석

Time machine으로 결과를 확인해 보면 흥미로운 점이 드러납니다. Agent가 권장 skill을 사용해 Android XR SDK의 일부인 Jetpack Compose Glimmer로 UI를 빌드했고, 스크롤하면 Agent가 Android Studio를 사용해 필요한 의존성 버전을 조회한 모습이 보였습니다. 그리고 수정한 파일에 대해 issue 분석을 수행한 후, 최종적으로 에뮬레이터에 앱을 배포해 비행 정보와 호텔 정보를 확인할 수 있게 했습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/60d428b0-675c-4542-a4dc-b46f111984d0/image.png)

### 4.9 AI Summary 추가와 Hybrid Firebase Logic

Florina의 다음 요청은 전체 여행에 대한 helpful AI Summary를 추가하는 것이었습니다. 동시에 Antigravity에게 before/after 스크린샷도 캡처하도록 요청했습니다.

Agent가 구현한 결과를 보면, hybrid Firebase logic으로 hybrid mode가 구현되어 있었습니다. 이 구조의 핵심은 on-device 모델이 없을 때만 cloud 모델을 fallback으로 사용한다는 점입니다. 비용과 지연시간을 최적화하는 best practice를 Agent가 스스로 적용한 것입니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/f00f342b-bb66-4d5b-9a10-d820cdc5ebd9/image.png)

Florina가 "스크린샷은 좋은데 정말 동작하는가?"라고 물었는데, 스크롤하면 요청한 before/after 스크린샷을 확인할 수 있었고, Agent가 Android CLI를 사용해 앱을 배포하고 UI를 navigate하며 스크린샷을 캡처한 사실까지 확인할 수 있었습니다.

### 4.10 Antigravity와 Android Studio의 이상적 병행

여러 configuration과 AI Summary의 오프라인 동작을 확인하려면 이상적인 setup은 Antigravity와 Android Studio를 병행 사용하는 것이라고 Florina가 강조했습니다. Adarsh는 Android Studio로 언제든 전환해 production-grade polish를 획득할 수 있다고 덧붙였습니다.

Agent에게 "홈 스크린의 Compose previews를 Android Studio에서 열어라"고 요청하자 다중 테마와 다양한 화면 크기에서 UI를 확인할 수 있었고, 조정이 필요하면 AI Actions를 사용해 미세 조정할 수 있었습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/5c748c7e-bc97-47f1-9989-8a735524241b/image.png)

### 4.11 실제 디바이스 테스트와 On-Device AI

On-device AI 기능 테스트를 위해서는 실제 폰이 필요했습니다. Android Studio에서는 소유 여부와 무관하게 다수의 실제 Android 디바이스에 배포할 수 있는데, 데모에서는 실제 Samsung Galaxy S26 Ultra에서 앱을 실행했습니다. S26 Ultra는 올해 여름 후반 Android Device Streaming에 추가될 예정입니다.

가장 인상적인 시연은 비행기 모드에서 AI 여행 summary가 on-device Gemini Nano를 사용하는 모습을 확인한 부분이었습니다. 네트워크 연결 없이도 AI 기능이 동작한다는 사실이 청중에게 시각적으로 명확히 전달되었습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/e60c35d9-7136-46a6-8a7d-813d11f99ce6/image.png)

### 4.12 App Quality Insights와 R8 최적화

Florina의 다음 단계는 고품질 앱의 성능 보장이었습니다. Android Studio에서 **App Quality Insights window**를 확인하니 프로덕션에서 앱이 너무 많이 crash하고 있었고, 추가로 Android 17의 메모리 제한 변경에도 대비할 필요가 있었습니다. Agent에게 "**fix and analyze my app's optimization and performance**"라고 요청하자, Agent는 R8이 성능 개선의 주요 방법임을 인지했습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/4e22d17a-43d5-4182-8d5a-ec5f6536c3a8/image.png)

R8의 역할은 사용되지 않는 코드와 리소스를 제거하고, runtime 성능을 위해 vibe-code를 재작성하는 것입니다. 효과적인 R8 configuration의 결과는 ANR 감소, 앱 크기 감소, 빠른 startup time으로 이어집니다.

결과를 보면 Agent가 R8 Analyzer skill을 사용해 build configuration 변경으로 R8 full mode를 활성화하도록 권장했고, 새로운 R8 Configuration Analyzer를 사용했습니다. 최종 보고서에는 Optimization, Obfuscation, Shrinking 스코어가 업데이트되어 표시되었습니다.

R8 효과를 극대화하기 위해 Agent가 keep rule을 감사하고 업데이트를 제안했는데, 이전에는 앱 코드가 거의 최적화되지 않았던 반면 이후에는 R8이 거의 모든 코드를 최적화했습니다. 단일 prompt로 더 빠르고 작은 앱을 달성한 것입니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/adddb2da-a629-4754-9469-ee025dff197c/image.png)

### 4.13 Deep Links와 App Links Assistant

Florina의 다음 요청은 사용자 engagement 극대화를 위한 deep link 추가였습니다. 부킹 확인 이메일의 링크를 클릭하면 앱 내 다가오는 여행으로 바로 이동해야 하는데, 현재는 링크가 동작하지 않는 상태였습니다.

최신 Android Studio에는 App Links Assistant라는 도구가 있습니다. Tools 메뉴에서 App Links Assistant를 열고, URL Mapping Editor를 사용해 호스트를 입력한 후 deep link를 처리할 activity를 선택합니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/43d98231-ccd5-4657-9246-4e13d4fe2498/image.png)

그 후 처리할 sample URL을 전달하면 AI가 작업을 수행합니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/19b760a7-a215-483f-915a-41422676213c/image.png)

Agent의 결과를 보면 URL과 앱 코드를 분석해 custom implementation plan을 권고했고, 이 plan을 기반으로 URL에서 trip data를 parsing하는 정확한 routing logic을 구현했습니다. 디바이스에서 이메일의 액션을 클릭하면 앱 내 개인화된 여행으로 정확히 이동하는 모습이 시연되었고, Adarsh의 농담("모든 PM이 이래? 아니면 나만?")에 Florina가 "너만"이라고 응수하는 장면도 있었습니다.

### 4.14 Google Play로 직접 배포

Adarsh는 Android Studio에서 Google Play로 앱 업데이트를 직접 게시하는 기능도 시연했습니다.

Build 메뉴에서 Generate Signed App Bundle을 선택하고, 클릭 몇 번 후 "Upload to Play"라는 새 옵션을 체크하면 됩니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/92cedae8-b1c9-4452-9456-974e3f7f72ab/image.png)

Next를 누르면 Internal test track으로 즉시 업로드되고, 테스터가 테스트하는 동안 개발자는 Play Store 페이지를 준비할 수 있습니다.

### 4.15 Migration Assistant의 정말 이른 미리보기

Florina와 Adarsh는 "정말, 정말 이른" 미리보기를 공개했습니다. React Native, 웹 프레임워크, 심지어 iOS 등 어떤 소스에서든 Android로 앱을 쉽게 마이그레이션하고 확장하는 도구 묶음입니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/615e7bc2-b36f-498a-839f-d8c9f047c1a0/image.png)

시나리오는 이렇습니다. 기존 iOS 앱을 Android의 30억 명 이상의 사용자에게 확장하려는 회사가 있다고 가정합시다. 이를 몇 주가 아닌 몇 시간으로 만들기 위해 새로운 Migration Assistant가 실험 중입니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/a71849f3-3c2b-4948-81bd-8382b11a6607/image.png)

사용 흐름은 다음과 같습니다. File → New Project → Migrate to New Project를 선택해 마이그레이션할 앱을 지정합니다. 그 후 결정 방식을 선택하는데, AI가 알아서 결정하게 할 수도 있고 Guided Migration으로 더 깊이 관여할 수도 있습니다. 참조 이미지나 custom skill을 첨부할 수도 있고, 검증을 직접 하는 대신 Journeys로 Agent에 위임할 수도 있습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/f50c8ae4-07c1-474d-8b86-021615a1dbb2/image.png)

Journeys는 앱의 User Journey를 자연어 instruction 세트로 작성하면 Agent가 앱을 execute, evaluate, iterate하는 방식입니다. 즉, "이 화면에서 저 버튼을 누르면 다음 화면으로 가야 한다"는 식의 시나리오를 자연어로 기술하면 Agent가 자동으로 테스트하고 수정합니다.

### 4.16 데모 사례: Metropolist

선택된 오픈 소스 프로젝트는 Metropolist였습니다. Paris 대중교통용 게임화된 동반 앱으로, 경로를 추적하면 포인트를 획득하고 전체 transit line을 주행하면 배지를 획득하는 재미있는 앱입니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/29e37ea8-f2fa-4a30-a9fc-8a3c150fd466/image.png)

미리 마이그레이션을 실행해 두고 polish task에 시간을 투자했는데, Maps SDK 지원 추가, 세련된 애니메이션 추가 같은 작업이었습니다.

데모에서는 iOS 앱이 Simulator에서, Android 앱이 emulator에서 동시에 실행되었습니다. Metro Number 1을 선택하고 "Start Travel"을 누른 후 La Defense에서 Les Sablons로 이동하는 시나리오를 진행했고, "Confirm Journey"를 누르자 Agent가 만든 진행 상황이 깔끔하게 표시되었습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/77039122-6dc9-4396-bf99-03ae7af5fae1/image.png)

Migration의 동작 방식은 인상적이었습니다. Android Studio의 Migration Assistant가 먼저 feature mapping을 생성하고, 그 후 project plan을 생성합니다. Agent는 일반적인 iOS와 Android 프로젝트 구조를 알고 있어서 Xcode storyboard를 보고 대응되는 Android 화면을 생성합니다. iOS에서 Android로의 문자열 마이그레이션과 SVG, PDF 같은 자산을 vector drawable로 변환하는 방법까지 학습되어 있습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/8157f693-2fdf-440e-a910-936f95b22efb/image.png)

Android 코드 구현 시 Agent는 Jetpack Compose, Room, View Models 같은 라이브러리와 predictive back navigation 같은 best practice를 사용합니다. 결과물은 native Android 앱이기 때문에 Android Studio의 모든 Agent와 도구를 적용해 production ready 상태로 만들 수 있습니다.

### 4.17 출시 일정과 정리

Migration Assistant는 올해 후반 Android Studio에 출시될 예정이며, Kotlin Multiplatform 마이그레이션 지원도 작업 중입니다. 이를 통해 Android와 iOS 간 shared business logic을 유지하기가 더욱 쉬워질 것입니다.

Adarsh는 이 섹션을 다음과 같이 정리했습니다. Antigravity와 Android CLI에 Android Studio의 production-grade polish를 결합함으로써, 단일하고 강력한 도구를 통해 놀라운 생산성 향상을 이룰 수 있다는 메시지입니다. 어떤 form factor를 빌드하든 이전보다 쉽게 아이디어를 실현할 수 있고, 모든 사이즈와 스킬 레벨의 팀이 최첨단 Kotlin 앱을 Google Play에 빠르게 배포할 수 있게 된 것입니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/9f008213-6973-4a12-a6f8-bda9aac1c158/image.png)

---

5. Chrome
---------

### 5.1 Una Kravets의 비전

Una Kravets가 Chrome 섹션을 시작했습니다. 그녀의 첫 메시지는 강렬했습니다. "AI Agent가 어디에서나 개발 환경을 변화시키고 있지만, 그 변화가 가장 빠른 곳은 웹이다." 웹은 가장 개방적이고 표준 기반의 플랫폼이기 때문에 Agent 기술의 영향이 즉시 광범위하게 확산된다는 의미입니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/2828cd4e-9676-480d-93ee-66b2dc62ee43/image.png)

Chrome에는 이미 Gemini가 내장되어 있어, AI 도우미를 사용자의 손끝에 배치합니다. 이는 사용자와 개발자 모두에게 새로운 상호작용의 시대를 열어줍니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/c87cdd51-4698-47ea-bf98-3fb79aff27cb/image.png)

Una의 비전은 시적이었습니다. 장벽 없이 실험할 수 있는 시간, 자신감을 가지고 빌드할 수 있는 시간, 마침내 모든 아이디어를 현실로 만들 수 있는 시간이 왔다는 것입니다. 몇 달 전만 해도 불가능해 보이던 명료함과 속도가 이제 가능해졌다고 강조했습니다.

### 5.2 신규 기능 학습 문제와 Baseline

Una가 동료 개발자들에게서 가장 많이 듣는 질문은 **"이 많은 새 기능들을 어떻게 따라가지?"**라는 것이었습니다.

웹 플랫폼이 매 몇 달마다 수십 개의 새 API를 추가하면서 가속화되고 있는 상황이라, 개발자 입장에서는 두 가지 문제에 동시에 부딪히게 됩니다. 첫 번째는 **새 기능이 자신의 사용자 환경(브라우저)에서 실제로 동작하는지 확인하는 문제**이고, 두 번째는 **그 기능의 사용법을 학습하는 문제**입니다.

1/ 첫 번째 문제는 그동안 Baseline이 해결해 왔습니다. 웹 플랫폼 기능의 100%가 매핑되어 있는 Baseline은 주요 브라우저 간 기능 가용성을 한눈에 확인할 수 있게 해주는 업계 표준입니다. 즉, "이 API를 써도 우리 사용자들이 모두 쓸 수 있을까?"라는 질문에 대한 답은 이미 마련되어 있었던 셈입니다.

2/ 문제는 두 번째였습니다. 새로운 기능을 어떻게 올바르게 사용할 것인가에 대해서는 마땅한 해결책이 없었고, 결국 개발자가 직접 문서를 뒤지고 시행착오를 거듭하는 수밖에 없었습니다. 이 두 번째 문제를 해결하기 위해 이번에 출시된 것이 바로 Modern Web Guidance입니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/e641f7c0-5bc9-492c-b3bb-073fb89d72ea/image.png)

### 5.3 Modern Web Guidance의 의미

Modern Web Guidance는 AI Agent를 supercharge하는 새 도구입니다. 포괄적이고 expert-vetted된 skill 모음으로, AI Agent에 modern web feature의 청사진을 제공합니다.

Baseline 경험을 기반으로 한 이 도구의 핵심 가치는 Agent가 "어제의 기술이 아니라 최신 웹 플랫폼 기능과 가장 최근의 Chrome 혁신"을 구현하도록 보장한다는 점입니다. baseline target과의 호환성도 유지됩니다.

작동 방식은 직관적입니다. 특정 baseline 버전을 target하면 Agent가 그에 맞춰 제안을 제한합니다. 광범위한 브라우저 지원이 없는 최신 플랫폼 기능에 대한 fallback 솔루션과 대안까지 포함되어 있어서, 사용자가 실험과 iteration의 flow에 있는 동안 Agent가 구현을 처리하도록 맡길 수 있습니다.

### 5.4 Matthias Rohmer와 Dynorun 데모

Matthias Rohmer가 데모를 위해 무대에 올랐습니다. 그가 작업 중인 사이트는 Dynorun이었는데, Chrome Dino에서 영감을 받은 차 사이트로 React로 빌드되었습니다. CSS Scroll Animation으로 fluid한 narrative-led 경험이 unfold되고, 그 후 모델 페이지로 이어지는 구조입니다. Configurator에서는 색상을 선택할 수 있는데, green이나 cerulean 같은 옵션이 있었습니다.

Una가 도전 과제를 제시했습니다. 이 사이트가 멋지지만 메뉴, 옵션, 슬라이더가 너무 많아서 실제 사용하려면 무거운 작업을 해 줄 브라우저 Agent 같은 단축 수단이 필요할 것 같다는 것입니다. 그래서 "Agent와 완전히 매끄럽게 동작하게 만들 수 있을까?"라고 물었습니다.

### 5.5 WebMCP의 등장

Matthias의 답변이 흥미로웠습니다. 몇 달 전만 해도 어려운 질문이었지만 이제는 아니라는 것입니다. WebMCP를 사용하면 웹페이지를 몇 분 안에 agent-ready로 만들 수 있다는 답이었습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/6a151e64-1785-4b62-8fec-77a67e2e1dec/image.png)

WebMCP는 제안 중인 브라우저 표준입니다. 브라우저 기반 Agent에 웹 capability를 노출하는 방식으로, Agent에게 어디서 어떻게 사이트와 상호작용해야 하는지를 알려줍니다. 결과적으로 더 정밀하고 신뢰성 있는 상호작용이 가능해집니다. 기존에 Agent가 웹사이트를 다룰 때는 DOM을 직접 파싱하고 시각적 추론에 의존해야 했는데, 이는 깨지기 쉽고 비효율적이었습니다. WebMCP는 사이트가 Agent에게 "여기에 이런 작업이 있고, 이렇게 호출하면 된다"고 명시적으로 알려주는 약속(contract) 역할을 합니다.

### 5.6 Modern Web Guidance로 WebMCP 구현

Una의 시연 의도는 명확했습니다. WebMCP를 직접 구현할 수도 있지만, Modern Web Guidance와 함께라면 Agent가 스스로 할 수 있는 skill을 가지고 있다는 것입니다.

Matthias가 Antigravity를 열고 **"Please implement WebMCP tools for the car configurator on this page"**라고 prompt를 입력했습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/a849a6ac-467c-4606-9acb-3787061b35fc/image.png)

Modern Web Guidance의 성능은 인상적입니다. 텍스트 기반 skill 모음이며 내부적으로 테스트되고, 벤치마크로 검증되고, 토큰 효율적입니다. 특히 주목할 만한 수치는 **웹 개발 task에서 가이드 적용 시 미적용 대비 jump-in pass rate가 평균 37%p 향상**되었다는 점입니다. 즉, 동일한 prompt에 대해 Agent가 첫 시도에 성공할 확률이 37%p 더 높아진다는 의미입니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/45ad6083-ebc6-4073-b13b-9d63ba417f4b/image.png)

skill 파일들은 markdown 형식이라 직접 읽을 수 있습니다. WebMCP 관련 skill 파일에는 WebMCP에 대한 지식이 포함되어 있어 Agent가 개발 프로세스를 jump-start하고 토대를 자신 있게 처리할 수 있게 합니다. WebMCP가 JavaScript function들이 API를 통해 Agent에 노출되는 방식임이 설명되어 있습니다.

### 5.7 Modern Web Guidance의 접근성

Modern Web Guidance는 가능한 한 접근하기 쉽게 만들어졌습니다. Antigravity에서 onboarding 시 one-click으로 설치할 수 있고, 나중에 Settings에서도 설치 가능합니다. Antigravity가 아닌 다른 코딩 도구에서도 ready-made skill 패키지로 설치할 수 있습니다. core 플랫폼 기능을 설명하므로 Angular, React 등 framework agnostic하게 동작한다는 점도 강점입니다.

### 5.8 Gemini in Chrome으로 차량 구성

Antigravity 작업이 거의 완료된 후 Matthias는 Chrome으로 전환했습니다. 오른쪽 위 **"Ask Gemini"를 클릭하면 Gemini in Chrome의 prototype이 뜨는데, 이는 실험적 WebMCP 지원을 포함**합니다. 아직 활발히 개발 중이므로 최종 버전과는 다를 수 있지만, WebMCP가 안정화되면 이 tool들은 WebMCP를 지원하는 모든 브라우저 기반 Agent와 호환될 것입니다.

Una가 다음과 같은 prompt를 입력했습니다.

> "Configure the ultimate party car. I want immersive audio and some interior lighting would be great. Plus, enhanced visibility for night driving to keep me safe, and I don't want to go too crazy so keep it under \$40,000 but give me as many add-ons as you can under that."

Gemini in Chrome은 autobrowse plan을 생성해 확인을 위해 사용자에게 잠시 plan을 보여주었고, Una가 task를 승인하자 작업이 진행되었습니다.

결과를 보면 Antigravity가 imperative tool인 Update Car Configuration을 구현했는데, 모든 configuration 옵션이 schema definition에 나열되어 있었습니다. Gemini in Chrome은 이 task에 특화된 WebMCP tool을 사용해 차량을 구성했습니다. Modern Web Guidance 덕분에 짧은 시간에 앱이 agentic web을 위한 준비를 완료한 것입니다.

Modern Web Guidance는 100개 이상의 use case와 수십 개의 최신 기능을 지원하며 오늘부터 early preview가 가능합니다. WebMCP는 더 큰 발표가 있었는데, Chrome 149부터 실험적 WebMCP API가 Origin Trial에 진입한다는 점입니다. Gemini in Chrome이 곧 사용자의 WebMCP tool을 지원하게 되며, 생태계 파트너와의 활발한 실험 위에 빌드됩니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/a93ed377-d54d-498e-8f3d-ad5f52227457/image.png)

### 5.9 코딩 Agent가 자신의 코드를 볼 수 없는 문제

Una가 다음 도전 과제를 제시했습니다. 코딩 Agent가 실제 사용자처럼 이 기능들을 테스트할 수 있는가? Matthias의 진단이 핵심을 짚었습니다. 최근 Agent 빌드 경험이 많이 향상되었지만, prompt한 것을 항상 정확히 받지는 못한다는 것입니다. 그 이유는 코딩 Agent가 자신이 작성한 코드가 어떻게 동작하는지 실제로 볼 수 없기 때문입니다.

이는 Agent 시스템의 근본적인 한계 중 하나였습니다. 코드를 작성하는 단계와 그 코드가 실행되는 단계 사이에 단절이 있어서, Agent가 자신의 결과물을 검증할 방법이 제한적이었습니다. 사용자가 "이 코드가 동작하지 않는다"고 알려주어야만 Agent가 다시 시도할 수 있었던 것입니다.

### 5.10 Chrome DevTools for Agents

이를 해결하는 것이 새로운 Chrome DevTools for Agents입니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/fe8303b1-ee3a-4f33-9e44-2b87279296c9/image.png)

early preview의 피드백에 기반해 더 많은 기능을 수행하도록 진화한 도구로, 이제 Agent가 자신이 작성한 코드가 runtime에 어떻게 작동하는지 마침내 볼 수 있게 되었습니다.

Chrome DevTools for Agents는 세 가지 요소로 구성됩니다. MCP server, CLI, 그리고 tailored skill 세트입니다. 이로 인해 Agent를 위한 closed feedback loop가 형성되며, 빌드, 검증, 디버깅에 효과적입니다. Agent가 코드를 쓰고, 그 결과를 직접 관찰하고, 문제를 인지하면 다시 수정하는 자율적 루프가 완성되는 것입니다.

### 5.11 Lighthouse 데모와 새 Agentic Browsing 카테고리

Matthias가 Antigravity에서 "**please check the WebMCP implementation with Lighthouse**"라고 prompt를 입력했습니다. 잠시 후 Chrome이 뜨고 페이지를 로드했는데, 기본적으로 DevTools UI에서 Lighthouse audit을 실행하는 것과 동일한 동작이었습니다.

> 💡 **Lighthouse audit이란?**  
> Lighthouse는 구글이 만든 무료 웹사이트 품질 검사 도구입니다. Chrome 브라우저에 기본 내장되어 있어서 별도 설치 없이 쓸 수 있습니다. 그리고 audit은 우리말로 "감사" 또는 "검사"라는 뜻인데, 회계 감사처럼 어떤 기준을 정해두고 그 기준을 잘 지키고 있는지 항목별로 점검한다는 의미입니다. 그래서 Lighthouse audit은 "Lighthouse로 웹사이트를 종합 검진한다"는 뜻으로 이해하시면 됩니다.

Lighthouse에 새로운 카테고리가 추가되었는데, agentic browsing 카테고리입니다. agentic web을 위한 종합적인 health check를 실행하며, WebMCP tool 등록 유효성과 form의 declarative metadata(Agent가 필요로 하는 정보)를 검증합니다.

Una가 추가 검증 항목을 설명했습니다. llms.txt 파일 검증인데, 이는 모델에 사이트의 콘텐츠 지도를 제공하는 새 표준입니다. 또한 익숙한 Lighthouse accessibility audit도 재평가됩니다. 대부분의 Agent가 accessibility tree를 사용해 웹을 navigate하기 때문에, ARIA role이나 label을 최적화하면 인간뿐 아니라 Agent에게도 사이트가 더 actionable해집니다. 이는 accessibility가 단순히 일부 사용자를 위한 기능이 아니라 Agent 시대의 보편적 기반이 된다는 흥미로운 변화입니다.

이슈가 Lighthouse에서 표면화되면 이전과 같이 "human clipboard" 역할을 할 필요가 없습니다. 오류를 복사해 채팅에 붙여넣고 Agent가 올바른 수정을 추측하길 기다리는 번거로움이 사라집니다. 이제 Agent가 직접 보고서를 읽고 해결책을 시도하고 audit을 재실행해 동작 여부를 확인합니다. Chrome DevTools for Agents는 오늘부터 Antigravity 및 20개 이상의 코딩 Agent에서 사용 가능합니다.

### 5.12 Car Configurator의 숨겨진 비밀

Una와 Matthias가 마지막 surprise를 공개했습니다. Canvas에서 실행되는 차의 인테리어 뷰에서 중앙의 화면이 실제로 interactive하다는 점입니다. 두 번째 화면으로 클릭 다운할 수 있고, 슬라이더로 ambient lighting을 변경할 수 있었습니다.

5.12와 5.13 사이에 짧은 보충 설명 박스를 끼워 넣으면, 청중 입장에서 왜 충격적인지가 자연스럽게 이해됩니다. 아래처럼 다듬어 보겠습니다.

여기서 충격적인 사실이 드러납니다. DevTools에서 Quick Inspect를 해 보니, canvas에 렌더링되는 전체 디스플레이 UI가 실제 native HTML 요소였다는 것입니다. Una의 반응이 청중의 마음을 그대로 표현했습니다. "HTML elements inside of a canvas? Well, that shouldn't be possible." 전통적으로 canvas는 픽셀 기반의 그리기 영역이고 HTML 요소와는 완전히 분리된 세계였기 때문입니다.

> 🤔 **잠깐, 왜 이게 불가능했을까?**
>
> 웹 페이지가 화면에 그려지는 방식은 크게 두 가지입니다. 하나는 **DOM** 방식으로, `<button>`이나 `<input>` 같은 HTML 태그를 쓰면 브라우저가 이를 "구조를 가진 객체"로 다룹니다. 그래서 클릭하면 반응하고, 텍스트는 복사할 수 있고, 스크린 리더가 읽을 수 있습니다. 다른 하나는 **Canvas** 방식인데, 한마디로 디지털 도화지입니다. "여기에 빨간 사각형을 그려라"라고 명령하면 그 자리에 픽셀을 칠하는 방식으로, 게임이나 3D 그래픽 같은 자유로운 시각 표현에 쓰입니다.
>
> 문제는 Canvas에 그려진 것은 그저 **픽셀 덩어리**라는 점입니다. 버튼처럼 보여도 브라우저에게는 "이게 버튼이다"라는 정보가 없습니다. 그래서 Canvas 안의 텍스트는 드래그해서 복사할 수도, Ctrl+F로 검색할 수도 없고, 스크린 리더가 읽지도 못하며, 번역기도 동작하지 않습니다. 결국 개발자들은 양자택일을 해야 했습니다. **화려한 시각 표현(Canvas)**과 **상호작용 및 접근성(DOM)** 중 하나를 포기해야 했던 것입니다.
>
> CSS로 DOM 요소를 Canvas 위에 덮어씌우는 우회법은 있었지만, 이는 진짜 통합이 아니라 단순한 겹쳐놓기였습니다. 3D 카메라가 움직이면 Canvas 안의 풍경은 함께 기울어지는데 위에 덮은 HTML 요소는 평면에 갇혀 따로 노는 식이었죠. 그래서 Canvas의 자유로움 안에 진짜 HTML 요소가 살아 있는 모습이 청중에게 "shouldn't be possible"이라는 반응을 끌어낸 것입니다.

### 5.13 HTML-in-Canvas API의 가능성

이 불가능을 가능하게 하는 것이 새로운 HTML-in-Canvas API입니다. 실제 DOM 요소를 canvas 환경에 직접 통합할 수 있게 해주는 API로, 시각적으로 복잡하고 멋진 것과 interactive하고 accessible한 것 중 하나를 선택해야 했던 오랜 트레이드오프를 깨뜨립니다. 핵심은 단순히 HTML을 canvas 위에 띄우는 것이 아니라, DOM 요소가 **canvas의 좌표계, 변환, 3D 시점에 함께 따라가면서도** DOM 객체로서의 정체성을 그대로 유지한다는 점입니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/83f2f060-5b16-46fe-b81d-f5473324d1e6/image.png)

canvas 안의 모든 요소가 DOM의 일부이기 때문에 흥미로운 특성들이 자동으로 따라옵니다. searchable, accessible, selectable, translatable하며, autofill 같은 내장 브라우저 기능과도 상호작용합니다. Matthias가 덧붙인 것처럼, 다른 DOM 요소처럼 클래스를 추가해 스타일링할 수도 있습니다. 데모에서 보여준 자동차 인테리어가 정확히 이 시연이었습니다. 3D로 렌더링된 차 내부에서 카메라가 움직이면 디스플레이도 함께 기울어지지만, 그 안의 슬라이더는 진짜 HTML 요소여서 마우스로 드래그하고 키보드로 포커스를 옮길 수 있었던 것입니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/ffa5d6e9-e647-4346-98ce-ff43dd51fb50/image.png)

Una는 커뮤니티의 시연 사례를 언급했습니다. WebGL 텍스처, 3D 인터페이스, 실제 DOM 콘텐츠와의 완전히 새로운 상호작용 모달리티 같은 demo들이 빌드되고 있다는 것입니다. HTML-in-Canvas는 현재 Origin Trial 상태로 테스트, 실험, 빌드가 가능합니다.

이렇게 인용 박스(`>`) 형태로 보충 설명을 삽입하면, 흐름을 끊지 않으면서도 개발 배경 지식이 없는 독자가 "왜 청중이 놀랐는지"를 자연스럽게 따라올 수 있습니다. 또한 5.13 첫 단락에 "단순히 HTML을 canvas 위에 띄우는 것이 아니라 좌표계와 3D 시점에 함께 따라간다"는 한 문장을 추가했는데, 이 부분이 새 API의 진짜 핵심이라서 한 번 더 짚어두는 것이 메시지를 분명하게 만들어 줍니다.

### 5.14 Chrome 섹션 정리

Una의 마무리 메시지는 강렬했습니다. 오늘 본 것은 단순한 새 기능이 아니라 빌드 방법, 빌드 가능한 주체, 빌드 가능한 것 자체의 근본적 전환이라는 점입니다.

새로운 Agent 시대의 웹 개발에는 영감을 주는 도구들이 있습니다. Modern Web Guidance는 WebMCP 같은 신규 기능을 빠르고 신뢰성 있게 구현하도록 돕고, HTML-in-Canvas는 웹의 accessible하고 interactive한 창의적 UI를 확장하며, Chrome DevTools for Agents는 자율적 디버깅과 성능 테스트를 가능하게 합니다.

> "The future of the web is imagined by you, and supercharged by AI."

---

6. Closing
----------

### 6.1 Josh Woodward의 마무리

Josh Woodward가 다시 무대로 돌아와 키노트를 마무리했습니다. 그는 키노트를 다음과 같이 정리했습니다. Google AI Studio에서 Antigravity까지, Android에서 오픈 웹까지, 오늘 Agent가 개발자 경험을 완전히 변환하는 모습을 보았다는 것입니다. 공통 주제는 단순합니다.

> "You focus on the big idea and the agents can do the heavy lifting."

Josh는 "지금처럼 빌드하기 좋은 시기는 없었다"고 강조하며, 오늘 본 것들을 한계까지 밀어붙이라고 청중에게 권유했습니다.

### 6.2 Build with Gemini XPRIZE Hackathon

빌드 동기를 부여하기 위한 공식 출시가 이어졌습니다. Build with Gemini XPRIZE Hackathon이 공식 출시되었으며, 상금 총 200만 달러의 글로벌 해커톤입니다. 빌더가 실제 문제를 해결하는 앱을 만드는 대회로, 전제는 단순합니다. 가치 있는 문제를 선택하고 Gemini로 빌드하면 됩니다.

> <https://www.xprize.org/news/xprize-launches-hackathon-with-2-million-prize-pool-backed-by-google>

목표는 야심차게 설정되었습니다. 10억 명의 삶에 긍정적 영향을 미치는 것입니다. 이런 규모의 영향력을 추구한다는 것은 단순한 기술 데모를 넘어 진짜 사회적 가치를 창출하라는 메시지로 읽힙니다.

### 6.3 Google AI Ultra Plan과 보너스 크레딧

해당 규모의 빌드를 위한 진지한 power가 필요함을 언급하며 오전 키노트에서 발표된 Google AI Ultra Plan을 소개했습니다. 월 100달러의 새 요금제이며, 사용자 피드백을 기반으로 단순화된 가격 구조를 갖추었습니다.

긴 휴일 연휴 동안 Agent를 계속 돌릴 수 있도록 오늘 Ultra 구독자에게 100달러의 보너스 크레딧이 지급됩니다. Antigravity 앱에서 직접 offer를 claim할 수 있고, 한도에 도달하면 크레딧이 적용됩니다.

### 6.4 마무리 안내

Josh는 io.google에서 라이브스트림 세션과 향후 며칠간 출시될 on-demand 콘텐츠를 시청할 수 있다고 안내하며 키노트를 마무리했습니다. 마지막 한마디는 단순했습니다. "Thanks for coming and have an amazing I/O!"

---

맺음말
---

이번 Developer Keynote를 한 문장으로 요약하면 "개발자는 큰 아이디어에 집중하고, Agent가 무거운 실행을 맡는 시대의 도구가 모두 갖춰졌다"는 선언입니다. Gemma 4의 폭발적 확산을 시작점으로, Managed Agents가 Agent 빌드의 인프라 부담을 제거하고, Antigravity 2.0과 CLI가 Agent 오케스트레이션의 mission control 역할을 맡았으며, Android에는 Migration Assistant까지 포함된 풀스택 Agent 도구가 결합되었고, Chrome에는 Modern Web Guidance·WebMCP·HTML-in-Canvas·Chrome DevTools for Agents라는 네 개의 축이 동시에 자리 잡았습니다.

기술적으로 더 깊은 시사점은 Agent 시스템이 "한 번 호출되고 끝나는 함수"에서 "맥락을 유지하며 스스로 검증하고 반복하는 협업 주체"로 진화했다는 점입니다. Skill-as-Markdown 패러다임은 Agent의 능력 정의 방식을 코드에서 자연어 가까운 markdown으로 끌어내렸고, Closed-Loop Agent System은 Agent가 자신의 결과물을 검증하고 개선하는 자율성을 부여했으며, Specialized Knowledge Injection은 일반 LLM의 한계를 도메인 지식으로 메웠고, Surface 통합과 Context 보존은 개발 라이프사이클 전체에서 Agent와의 관계가 끊기지 않도록 만들었습니다. 이 네 가지 패턴이 따로따로가 아니라 서로 맞물려 작동한다는 점이 이번 키노트의 진짜 메시지였다고 볼 수 있습니다.

마지막으로 ML 실무자의 관점에서 가장 인상적인 장면은 Kevin Hou의 Gemma 4 LoRA fine-tuning 데모였습니다. 그동안 ML 엔지니어의 전유물이었던 fine-tuning 파이프라인 구축이 음성 prompt 한 번과 Agent의 plan 승인만으로 무대 위에서 실시간 시연이 가능해졌다는 것은, 모델 커스터마이징의 진입 장벽이 근본적으로 낮아지고 있음을 보여주는 상징적 사건이었습니다. 이번 키노트가 그린 그림이 실제 개발 현장에서 어떻게 자리잡을지, 그리고 Agent와의 협업이 어떤 새로운 워크플로우 표준을 만들어낼지가 앞으로의 관전 포인트가 될 것입니다.

읽어주셔서 감사합니다.