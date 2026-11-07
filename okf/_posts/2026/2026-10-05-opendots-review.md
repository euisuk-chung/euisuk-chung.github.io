---
type: "Repo Review"
title: "[Repo Review] OpenDots: 지속 대화와 문서·도구 실행을 연결하는 AI 작업 공간"
description: "OpenDots의 대화 실행부터 검색·컴퓨터 도구·승인 저장까지 추적하고, 영수증·revision·lease가 중복과 충돌을 처리하는 경계를 분석합니다."
date: "2026-10-05"
tags:
  - "Repo Review"
  - "AI Agent"
  - "MCP"
  - "Tools"
resource: "https://github.com/CopilotKit/OpenDots/tree/c2569bb6a13a22e565cf3eb791c62267d06babb1"
generated:
  by: "process:blog-review"
  at: "2026-10-05T06:04:03+09:00"
sources:
  - id: "CopilotKit/OpenDots"
    resource: "https://github.com/CopilotKit/OpenDots/tree/c2569bb6a13a22e565cf3eb791c62267d06babb1"
    title: "OpenDots"
    last_modified: "2026-10-02T14:16:45-07:00"
status: "stable"
year: "2026"
analyzed_at: "2026-10-05T06:04:03+09:00"
source_id: "CopilotKit/OpenDots"
source_revision: "c2569bb6a13a22e565cf3eb791c62267d06babb1"
source_type: "repo"
source_url: "https://github.com/CopilotKit/OpenDots/tree/c2569bb6a13a22e565cf3eb791c62267d06babb1"
visual_sources:
  - path: "/img/reviews/2026/opendots-review/runtime-flow.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/dot-agent.ts#L243-L339"
    caption: "리뷰어 작성, 분석 커밋 기준. 텍스트 실행과 저장 책임의 개요."
  - path: "/img/reviews/2026/opendots-review/review-save.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/pages.ts#L130-L162"
    caption: "리뷰어 작성, 분석 커밋 기준. 승인 저장의 영수증 복구와 트랜잭션."
---

## 들어가며

AI 에이전트에 채팅 화면을 붙인 뒤에는 새로운 문제가 생깁니다. 대화를 닫아도 작업이 이어져야 하고, 문서 편집과 모델의 수정이 충돌할 수 있으며, 도구 실행 권한을 실행 도중에 거둘 수도 있어야 합니다. OpenDots는 이런 연결부를 살펴보기 좋은 애플리케이션 템플릿입니다. 역할을 가진 에이전트인 **Dot**, 문서를 모으는 **Space**, 지속되는 대화인 **Thread**를 하나의 작업 공간에 묶습니다.

README는 OpenDots를 텍스트·통화·Slack을 오가는 상시 AI 동료의 출발점으로 소개하면서, 초기 개발 단계의 단일 소유자 템플릿이라고 명시합니다. 이 글에서는 그 표현을 실제 구현으로 좁혀서 읽습니다. 분석 대상은 `CopilotKit/OpenDots`의 커밋 `c2569bb6a13a22e565cf3eb791c62267d06babb1`입니다. 의존성 설치나 대상 코드 실행 없이 문서와 소스를 정적으로 분석했으며, README의 실서비스 검증 기록은 저자의 보고로 구분합니다. [README의 정의](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/README.md#L37-L49), [기능과 범위](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/README.md#L167-L187)

## 무엇을 제공하는 프로젝트인가

OpenDots는 **문서 저장소와 지속 대화, 모델 도구 실행, 선택적인 컴퓨터·음성·Slack 연결을 결합한 셀프 호스팅 작업 공간**입니다. 여기서 셀프 호스팅은 모든 기능이 외부 서비스 없이 로컬에서 동작한다는 뜻은 아닙니다. 페이지와 설정은 SQLite에 저장하지만, 대화 이력은 설정된 CopilotKit Intelligence 프로젝트가 맡습니다. 모델 API도 별도로 설정해야 합니다. 따라서 SQLite 파일만 복사하면 전체 대화 이력을 백업한 것은 아닙니다. [설정 문서](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/docs/SETUP.md#L26-L53)

| 개념 | 구현에서 맡는 역할 | 저장·실행 경계 |
| --- | --- | --- |
| Dot | 이름·역할 지시·연구 및 메모리 권한·접근 가능한 Space | 로컬 설정을 서버가 읽어 실행 구성 |
| Space와 Page | Markdown 문서, 부모 페이지, revision | 로컬 SQLite |
| Thread | Dot별 대화와 페이지별 대화 연결 | 로컬 바인딩 + Intelligence 이력 |
| Task | 정기 요청과 실행 상태·결과 | SQLite + 살아 있는 서버의 Runner |
| Computer | Dot별 브라우저·파일·셸 접근 | 별도 OpenBot supervisor와 computer 서비스 |

표는 [Platform](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/platform.ts#L19-L85), [Pages](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/pages.ts#L19-L47), [Runner](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/runner.ts#L5-L23), [컴퓨터 문서](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/docs/COMPUTERS.md#L1-L15)의 책임을 정리한 것입니다. 문서의 지속성, 대화 이력의 지속성, 예약 실행의 재시도, 컴퓨터 파일의 지속성은 서로 다른 저장소와 서비스에 의존합니다.

## 아키텍처와 읽을 디렉터리

프런트엔드는 React와 CopilotKit React SDK를 사용하고, 서버는 Hono로 HTTP API를 제공합니다. `package.json`의 개발 명령은 `src/server/index.ts`와 Vite를 함께 시작합니다. 모델 스트리밍과 서버 도구 루프에는 TanStack AI, 입력 구조 검사에는 Zod, 문서 편집에는 Tiptap을 사용합니다. 이들은 매니페스트에서 확인한 의존성이며, 이 글에서 해당 외부 라이브러리 내부까지 분석한 것은 아닙니다. [매니페스트](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/package.json#L10-L69)

| 경로 | 읽어야 하는 이유 |
| --- | --- |
| `src/client/main.tsx`, `App.tsx`, `Chat.tsx` | React 진입점, runtime 연결, 메시지 전송과 승인 카드 등록 |
| `src/server/index.ts`, `app.ts` | 설정 조립, 저장소 초기화, 인증·요청 경계, 서버와 작업 실행기 시작 |
| `platform.ts`, `runtime-scope.ts`, `dot-agent.ts` | SDK 연결, 대화 범위 검사, Dot별 모델·도구 구성 |
| `page-routes.ts`, `page-tools.ts`, `pages.ts` | 사용자 API와 모델 도구가 같은 문서 저장 계층에 도달하는 경로 |
| `parallel.ts`, `computer-service.ts` | 검색 MCP와 컴퓨터 서비스로 나가는 외부 호출 경계 |
| `runner.ts`, `store.ts`, `headless.ts` | 예약 작업의 임대권과 서버에서 실행하는 대화 턴 |

![OpenDots 텍스트 요청이 서버 검사와 Dot 도구 실행을 거쳐 결과로 돌아오는 흐름]({{ '/img/reviews/2026/opendots-review/runtime-flow.svg' | relative_url }})

리뷰어 작성, 분석 커밋 기준입니다. 텍스트 실행의 주요 경로와 두 저장 책임을 단순화했습니다. 근거: [Chat 전송](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/client/Chat.tsx#L128-L179), [Platform 구성](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/platform.ts#L29-L85), [DotAgent 실행](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/dot-agent.ts#L243-L339). SDK 내부의 네트워크 세부 순서를 모두 표현한 도식은 아닙니다.

## 작동 원리: 요청에서 결과까지

### 1. 사용자 입력과 서버 권한 검사는 별도 단계입니다

`App`은 `/api/copilotkit`을 runtime URL로 전달합니다. `Chat.send()`는 빈 입력, 실행 중 상태, 대화·문맥 로딩 미완료, 일시정지 상태를 검사합니다. 이후 사용자 메시지를 에이전트에 추가하고 `copilotkit.runAgent({ agent })`를 호출합니다. 반환된 새 메시지에 assistant 응답이 하나도 없으면 실패로 처리합니다. UI에서 전송을 막는 것과 서버에서 실행을 허용하는 것은 구분되어 있습니다. [Provider](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/client/App.tsx#L891-L896), [전송 처리](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/client/Chat.tsx#L128-L155)

서버는 API 본문 크기를 1,000,000바이트로 제한하고, Origin과 `sec-fetch-site`를 확인합니다. `OWNER_TOKEN`이 설정되어 있으면 Bearer 토큰을 길이 검사와 `timingSafeEqual`로 비교합니다. `index.ts`는 루프백 이외 주소에 바인딩할 때 24자 이상의 토큰을 요구합니다. 이 조합은 단일 소유자의 진입 경계이며, 사용자별 계정·Space 멤버십 모델을 구현한 것은 아닙니다. [API 미들웨어](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/app.ts#L29-L82), [외부 바인딩 조건](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/index.ts#L12-L21)

`Platform.handle()`은 SDK handler로 넘기기 전에 `validateRuntimeScope()`를 호출합니다. 이 함수는 허용된 경로와 HTTP 메서드를 열거하고, 경로·본문·쿼리에 등장하는 agent/thread 식별자가 모순되지 않는지 검사합니다. 코드 주석은 SDK의 접미사 매칭과 다른 대화를 검사하는 상황을 피하기 위해 전체 경로를 매칭한다고 설명합니다. 단순한 문자열 검사가 아니라 **검사한 대상과 실제 실행 대상이 같도록 만드는 단계**입니다. [runtime 범위 검사](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/runtime-scope.ts#L1-L81), [호출 위치](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/platform.ts#L151-L176)

### 2. DotAgent는 매 실행마다 도구와 문맥을 구성합니다

`DotAgent.run()`은 Dot을 조회하고 `requireThread(input.threadId, dot.id)`로 대화 연결을 확인합니다. Intelligence 키, 모델 API 키, 모델명이 없으면 실행을 시작하지 않습니다. 시작 당시 설정을 보관한 뒤 100ms마다 일시정지·연구/메모리 권한·학습 컨테이너·Space 접근 설정의 변경을 검사하며, 90초 타이머도 둡니다. 변경을 발견하면 실행 중단을 요청합니다. 모델이 자신의 권한 변경을 자발적으로 따르기를 기다리는 방식과 다른 서버 제어입니다. [시작과 중단 검사](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/dot-agent.ts#L53-L110)

그다음 허용된 도구를 모읍니다. 연구가 허용되면 설정에 따라 Parallel 검색 또는 별도 URL 읽기 도구를 제공하고, 페이지 도구를 추가하며, 컴퓨터 서비스가 구성되어 있으면 컴퓨터 도구도 연결합니다. 메모리는 워크스페이스와 Dot 양쪽이 허용할 때만 프롬프트에 넣습니다. 모델 어댑터는 OpenAI 호환 Chat Completions 방식으로 구성됩니다. [도구 선택](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/dot-agent.ts#L116-L177), [문맥·모델 구성](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/dot-agent.ts#L243-L267)

메시지 변환 직전에는 클라이언트 메시지의 `system`과 `developer` 역할을 제거합니다. 아래는 원문의 연속된 일부입니다.

```typescript
const converted = convertInputToTanStackAI({
  ...ctx.input,
  // Match BuiltInAgent's default trust boundary for client messages.
  messages: ctx.input.messages.filter(
    (message) =>
      message.role !== 'system' && message.role !== 'developer',
  ),
});
```

출처: [dot-agent.ts 280–287행](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/dot-agent.ts#L280-L287). 서버가 만든 역할 프롬프트와 사용자가 전달한 메시지의 위치를 구분하려는 구현입니다. 이것만으로 웹 문서의 프롬프트 주입이 모두 방지된다고 해석할 수는 없습니다. 페이지 내용과 메모리는 여전히 모델이 읽는 문맥이며, 코드는 이를 신뢰할 수 없는 자료로 다루라는 지시도 넣습니다.

TanStack `chat()`에는 최대 출력 토큰 2,200과 기본 5회의 `maxIterations`를 전달합니다. 학습 스킬 전달이 활성화되고 해당 대화에 컨테이너가 있으면 반복 한도는 10회입니다. 클라이언트가 전달한 도구 중에는 웹 대화의 `review_space_page`만 허용하고, `forwardedProps`는 빈 객체로 바꿉니다. 내부 에이전트가 내보내는 이벤트를 Observable 구독자에게 전달하는 것이 이 클래스의 출력입니다. 이 숫자는 코드에 설정된 한도이며 처리 속도나 성공률의 측정치는 아닙니다. [루프 설정과 이벤트 전달](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/dot-agent.ts#L288-L339)

### 3. 검색 결과는 출처 자료로 정리해 모델과 화면에 돌려줍니다

기본 검색 제공자는 Parallel입니다. `parallelSources()`는 MCP(Model Context Protocol, 모델과 외부 도구를 연결하는 프로토콜) 클라이언트를 만들고 `https://search.parallel.ai/mcp`에 연결합니다. URL이 주어지지 않았으면 `web_search`를 호출해 후보 URL을 얻고, 이어 `web_fetch`로 최대 5개 URL의 자료를 읽습니다. URL이 직접 주어지면 검색 단계를 건너뜁니다. [기본값](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/parallel.ts#L6-L17), [외부 도구 호출](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/parallel.ts#L111-L200)

응답 파서는 HTTP(S) URL인지, 자격 증명이 URL에 붙지 않았는지, 발췌문이 비어 있지 않은지 검사합니다. 같은 URL은 제거하고, 출처별 텍스트는 6,000자로 제한하며 최대 5개를 반환합니다. 추출 오류나 버린 결과는 경고로 남기고, 쓸 만한 자료가 전혀 없으면 예외를 던집니다. 검색 결과가 비었다는 상황을 가상의 출처로 메우는 fallback은 이 경로에 없습니다. [응답 정리](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/parallel.ts#L19-L109), [빈 결과 처리](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/parallel.ts#L163-L195)

`DotAgent`는 반환된 제목·URL·본문과 제한 사항을 로컬 capture로 저장하고 모델 도구 결과로도 반환합니다. 저장되는 출처 요약의 excerpt는 320자로 잘립니다. 연구 목표, 검색어, URL, thread 기반 세션 식별자는 외부 서비스로 나갑니다. 전체 대화와 메모리를 자동 전송하는 인자는 없지만, 모델이 만든 검색 목표 자체에 대화의 일부 내용이 들어갈 가능성은 README도 명시합니다. [capture 저장](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/dot-agent.ts#L179-L213), [데이터 공유 설명](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/README.md#L214-L220)

### 4. 승인 저장은 응답 유실까지 고려합니다

채팅 화면은 `useHumanInTheLoop`로 `review_space_page`를 등록합니다. 모델이 이 도구를 호출하면 `PageReviewCard`가 초안을 보여주고 사용자의 결정을 기다립니다. 승인 시에는 페이지를 저장한 다음, 저장된 page/space ID와 링크를 도구 응답으로 반환해 에이전트가 이어서 대화하도록 합니다. 거절 시에는 저장하지 말라는 결과를 반환합니다. [도구 등록](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/client/Chat.tsx#L170-L179), [카드의 결정 처리](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/client/PageReviewCard.tsx#L65-L98)

여기서 중요한 문제는 서버가 저장을 완료했지만 브라우저가 응답을 받지 못하는 경우입니다. 클라이언트는 승인·거절을 다시 처리하기 전에 `(threadId, toolCallId)`로 기존 저장 영수증을 조회합니다. 이전에 저장됐다면 그 페이지를 반환합니다. 즉 이미 완료된 저장 뒤에 누른 거절은 기존 페이지 삭제가 아닙니다. [복구 순서](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/client/page-review-decision.ts#L14-L25)

![검토 도구 호출에서 기존 영수증 확인과 승인 저장으로 이어지는 흐름]({{ '/img/reviews/2026/opendots-review/review-save.svg' | relative_url }})

리뷰어 작성, 분석 커밋 기준입니다. 근거: [클라이언트 결정](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/client/page-review-decision.ts#L14-L25), [서버 권한 검사](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/page-routes.ts#L24-L45), [트랜잭션](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/pages.ts#L130-L162). 기존 저장이 있으면 그 페이지를 복구하며, 아래 새 저장 경로는 기존 영수증이 없고 승인한 경우입니다.

서버 POST 경로는 thread 소유 연결과 Dot의 Space 접근권을 확인한 뒤 `Pages.createReviewed()`를 호출합니다. 이 함수는 `BEGIN IMMEDIATE` 트랜잭션 안에서 영수증을 다시 확인합니다. 이미 있으면 같은 Space의 페이지를 돌려주고, 없으면 페이지와 영수증을 함께 삽입하고 commit합니다. 클라이언트의 선행 조회만으로는 막을 수 없는 중복 요청도 저장 계층에서 처리하는 구조입니다. [승인 API](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/page-routes.ts#L24-L45), [저장 트랜잭션](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/pages.ts#L130-L162)

**이 승인 카드는 모든 쓰기에 적용되는 강제 게이트는 아닙니다.** 서버에는 별도의 `create_space_page`와 `edit_space_page` 도구도 있습니다. 프롬프트는 사용자가 저장 전 검토를 요청할 때 승인 도구를 쓰도록 지시합니다. 승인 경로의 재시도 안전성과 “모든 문서 변경에 반드시 사람이 승인한다”는 정책은 다른 주장입니다. 후자는 이 코드로 확인되지 않습니다. [일반 페이지 도구](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/page-tools.ts#L77-L90), [검토 요청에 관한 프롬프트](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/dot-agent.ts#L267)

### 5. 문서 수정 충돌은 revision으로 탐지합니다

페이지에는 `revision`이 있고 수정 입력에는 양의 정수 `expectedRevision`이 필수입니다. `Pages.update()`는 현재 revision과 요청 값이 다르면 HTTP 409에 대응하는 `PageError`를 던집니다. 일치하면 본문 등을 수정하고 revision을 하나 증가시킵니다. 부모 페이지를 바꿀 때는 조상 경로를 따라가면서 자기 자신이나 자손 밑으로 이동해 순환이 생기는지도 검사합니다. [수정 입력](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/pages.ts#L11-L28), [부모 검사](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/pages.ts#L76-L86), [revision 갱신](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/pages.ts#L164-L199)

이 방식은 동시 편집 내용을 자동으로 합치지 않습니다. 오래된 내용을 덮어쓰려는 시도를 거절해, 사용자가 최신본과 초안을 비교할 기회를 주는 낙관적 동시성 제어입니다. 문서 역시 실패한 자동 저장은 초안을 보존하고 재시도나 충돌 해결을 기다린다고 설명합니다. 페이지별 대화는 `(pageId, dotId)`를 키로 예약하고, 외부 Thread 생성 후 준비 완료로 표시하여 문서와 에이전트 대화를 연결합니다. [편집 동작 문서](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/docs/SETUP.md#L43-L53), [대화 예약과 연결](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/page-service.ts#L46-L95)

### 6. 컴퓨터 도구는 외부 서비스의 권한 게이트웨이를 통과합니다

컴퓨터 기능은 OpenDots 호스트에서 바로 셸 명령을 실행하는 경로가 아닙니다. `ComputerService`는 supervisor URL·supervisor 토큰·computer 토큰이 모두 있어야 구성된 것으로 판단합니다. Dot마다 master token과 `opendots-computer:` 접두사가 붙은 ID로 HMAC-SHA256 토큰을 유도합니다. supervisor가 반환한 컴퓨터 정보도 Dot ID, 컨테이너 이름, 허용 호스트와 포트가 맞는지 검사합니다. [구성·토큰](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/computer-service.ts#L34-L63), [endpoint 바인딩](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/computer-service.ts#L144-L187)

`action()`은 입력 스키마를 검증하고 작업을 browser/files/shell 범주로 분류합니다. 에이전트가 `human_` 제어를 호출하면 거절하고, Dot의 해당 권한과 일시정지 상태를 검사합니다. 실행 중에는 50ms마다 권한을 재확인하며 취소 신호를 외부 요청에 전달합니다. 요청 전후 검사와 감사 기록은 OpenDots가 담당하지만, 실제 브라우저·파일·셸 동작과 격리는 OpenDots 분석 범위 밖의 OpenBot 서비스가 담당합니다. [실행 경로](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/computer-service.ts#L312-L367), [감사 기록](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/computer-service.ts#L221-L236)

취소는 이미 발생한 외부 부작용을 되돌리는 트랜잭션이 아닙니다. 컴퓨터 문서는 취소 뒤에도 상류 브라우저 동작이 끝날 수 있다고 설명하며, 기본 Docker 컨테이너는 호스트 커널을 공유하고 제한적인 네트워크 송신 정책을 기본 구성하지 않는다고 명시합니다. 코드의 권한 확인을 강한 샌드박스 보장으로 확대해 읽으면 안 됩니다. [컴퓨터 경계와 취소의 한계](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/docs/COMPUTERS.md#L49-L55)

### 7. 예약 작업·음성·Slack은 대화 실행에 연결됩니다

`Runner`는 1초마다 작업을 확인하지만 자신이 수행 중인 작업이 있으면 다음 tick을 건너뜁니다. `Store.claim()`은 실행 가능한 작업 하나에 무작위 lease를 부여하고 180초의 만료 시각을 기록합니다. lease는 그 실행이 아직 결과를 기록할 자격이 있는지를 나타내는 임대권입니다. `finish()`는 현재 lease와 일치하는 실행만 완료 처리하므로, 취소되거나 교체된 실행이 늦게 돌아와 상태를 덮어쓰는 것을 막습니다. 다음 반복 시각은 이전 예정 시각이 아니라 완료 시각에 interval을 더해 계산합니다. [Runner](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/runner.ts#L43-L88), [claim과 완료](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/store.ts#L192-L255)

실제 서버 진입점은 Runner에 실행 함수를 주입합니다. 이 함수는 task에 연결된 Thread를 찾고 `platform.turn()`을 호출합니다. 연결이 없는 예전 작업은 명시적으로 실패합니다. `headless.ts`는 Node 환경용 `IntelligenceAgent`를 구성하고 해당 Thread에 요청을 추가한 뒤 이번 턴의 assistant 텍스트를 반환합니다. 실제 앱의 예약 경로를 설명할 때 Runner의 기본 fallback인 `research()`만 읽으면 중요한 연결을 놓칩니다. [주입되는 실행 함수](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/index.ts#L71-L87), [서버 대화 턴](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/headless.ts#L23-L77)

음성의 compute도 `platform.turn()`을 호출합니다. 한 통화 내 같은 toolCallId의 Promise는 재사용하고, compute 요청은 최대 6개로 제한합니다. 이 구현의 중복 방지는 프로세스 메모리 Map에 있으므로 앞에서 본 SQLite 승인 영수증과 같은 내구성을 가진다고 보지 않습니다. Slack의 identity 함수는 provider·team·human actor·사용자 allowlist를 확인한 뒤 허용된 사용자를 동일 owner ID로 매핑합니다. 독립된 다중 사용자 권한 모델은 아닙니다. [음성 compute](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/voice.ts#L170-L190), [Slack identity](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/slack-channel.ts#L31-L44)

## 설치와 사용: 문서에 적힌 경로

분석 커밋의 README는 Node.js 24와 npm을 요구하고 다음 명령을 안내합니다. 아래는 문서의 명령을 그대로 옮긴 것으로, 이번 리뷰에서 실행한 기록은 아닙니다. 명령의 clone은 기본 브랜치를 가져오므로 이후 실행 시 분석 커밋과 달라질 수 있습니다. [시작 명령](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/README.md#L151-L165)

```sh
git clone https://github.com/CopilotKit/OpenDots.git
cd OpenDots
npm ci
cp .env.example .env
npm run dev
```

개발 화면은 `http://127.0.0.1:5173`, API는 4310 포트로 안내합니다. 문서 수동 편집은 대화 서비스 설정 전에도 사용할 수 있습니다. 대화에는 `INTELLIGENCE_API_KEY`, `OPENAI_API_KEY`, `OPENAI_MODEL`을 설정하며, 호환 공급자에는 `OPENAI_BASE_URL`을 사용합니다. 통화와 Slack, Dot 컴퓨터는 각각 추가 설정이 필요합니다. 특히 URL만 읽는 browser 서비스와 상호작용 가능한 Dot computer는 서로 다른 구성입니다. [설정과 포트](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/docs/SETUP.md#L5-L41), [브라우저와 컴퓨터의 구분](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/docs/SETUP.md#L55-L70)

## 한계와 평가 범위

README는 2026년 9월 29일 Intelligence·모델 응답·페이지 문맥 채팅, 9월 30일 Realtime 음성과 통화 제어의 라이브 확인을 보고합니다. OpenBot 브라우징·파일·셸과 재시작 후 파일 보존도 저자의 로컬 확인으로 기재되어 있습니다. 반면 Slack, 음성으로 위임한 compute, Automatic Learning의 일부 클라우드 경로는 연결 서비스 검증이 더 필요하다고 구분합니다. 이 글은 그 검증을 재현하지 않았습니다. [저자의 검증 범위](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/README.md#L183-L185)

정적 분석으로 확인할 수 있는 것은 조건문·상태·외부 호출의 연결입니다. 모델이 매번 검토 도구를 선택하는지, 실제 컴퓨터 격리가 충분한지, 네트워크 장애 뒤 모든 SDK 동작이 복구되는지는 확인하지 않았습니다. 문서에 명시된 단일 소유자 범위, 공유 편집·초대·파일 업로드·다중 Dot 자동 위임의 부재도 제품 확장 시 고려해야 합니다. 예약 작업은 서버가 계속 실행되어야 하며, 90초 실행 제한과 재시도 가능한 저장 상태를 가진다고 해서 모든 외부 동작이 정확히 한 번만 실행되는 것은 아닙니다. [명시적 범위](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/README.md#L187-L195), [보안 문서](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/SECURITY.md#L1-L19), [실행 제한](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/src/server/runner.ts#L43-L59)

라이선스는 MIT입니다. 복사·수정·배포 등을 허용하되 저작권과 허가 고지를 유지해야 하며, 보증 없이 제공한다는 조항이 있습니다. 이는 OpenDots 코드의 라이선스 설명이며 연결한 외부 서비스의 이용 조건을 대신하지 않습니다. [LICENSE](https://github.com/CopilotKit/OpenDots/blob/c2569bb6a13a22e565cf3eb791c62267d06babb1/LICENSE#L1-L20)

### 이 글에서 다루지 못한 부분

Tiptap의 Markdown 왕복 변환과 자동 저장 상태 머신 전체, 별도 읽기 전용 브라우저의 네트워크 차단 구현, WebRTC의 클라이언트 오디오 처리와 통화 영수증 재동기화 전체, Slack 전달·재구독의 모든 오류 경로, 학습 컨테이너와 스킬 배포의 상세 구현은 심층 분석 범위에서 제외했습니다. OpenBot 원본과 CopilotKit·TanStack·MCP SDK 내부도 별도 저장소 또는 의존성 경계로 남겨 두었습니다. 테스트 파일의 존재와 README 기록을 실행 검증으로 간주하지 않았습니다.

## 마치며

OpenDots에서 배울 핵심은 에이전트 기능을 화면에 모으는 방법뿐 아니라, 그 기능 사이의 상태와 권한을 연결하는 방법입니다. 대화 이력과 문서를 분리하고, 서버에서 Dot과 Thread의 범위를 확인하며, 승인 저장에는 지속 영수증을, 수정에는 revision을, 예약 실행에는 lease를 사용합니다. 이 서로 다른 장치를 구분해서 읽으면 지속되는 AI 작업 공간에서 어떤 중복과 충돌을 처리하고, 어떤 보장은 외부 서비스와 운영 환경에 남아 있는지 파악할 수 있습니다.
