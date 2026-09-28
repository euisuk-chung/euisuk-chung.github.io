---
type: "Repo Review"
title: "[Repo Review] OpenClaw — 메시지 한 건이 에이전트 실행과 응답으로 이어지는 구조"
description: "OpenClaw의 Gateway, 세션 라우팅, 실행 큐, 도구 구성과 응답 전달을 Control UI의 chat.send 경로로 추적합니다."
date: "2026-09-11"
tags:
  - "Repo Review"
  - "AI Agent"
  - "Network"
  - "Tools"
  - "IT지식"
  - "개념정리"
resource: "https://github.com/openclaw/openclaw/tree/47918f787d845c1901887626e3cff14c245253e0"
generated:
  by: "process:blog-review"
  at: "2026-09-11T18:44:44+09:00"
sources:
  - id: "openclaw/openclaw"
    resource: "https://github.com/openclaw/openclaw/tree/47918f787d845c1901887626e3cff14c245253e0"
    title: "openclaw/openclaw"
status: "stable"
year: "2026"
analyzed_at: "2026-09-11T18:38:00+09:00"
source_id: "openclaw/openclaw"
source_revision: "47918f787d845c1901887626e3cff14c245253e0"
source_type: "repo"
source_url: "https://github.com/openclaw/openclaw/tree/47918f787d845c1901887626e3cff14c245253e0"
visual_sources:
  - path: "/img/reviews/2026/openclaw-review/message-flow.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/src/gateway/server-methods/chat-send-handler.ts#L480"
    caption: "리뷰어 작성, 분석 커밋 기준. Control UI의 일반 embedded 실행과 응답 경로를 요약하며 CLI 런타임 분기는 별도로 표시합니다."
---

## 들어가며

메신저에 연결된 AI 비서를 만들 때 모델 호출만으로 해결되지 않는 문제가 있습니다. 같은 대화를 어떤 기록에 연결할지, 사용자가 전송 버튼을 다시 눌렀을 때 어떻게 처리할지, 실행 중 도착한 메시지를 어떻게 다룰지, 도구 결과와 최종 답변을 어떤 화면으로 돌려보낼지를 함께 설계해야 합니다.

OpenClaw는 이러한 연결을 담당하는 **자체 호스팅 AI 비서와 다중 채널 Gateway**입니다. Gateway는 여러 클라이언트와 메시징 채널의 접점이면서 세션·도구·이벤트를 조율하는 제어 계층입니다. README는 Discord, Slack, Telegram 등 기존 대화 채널과 네이티브 앱을 지원한다고 설명합니다. 이 글은 모든 연동을 사용해 본 기능 평가가 아니라, 한 메시지가 처리되는 대표 경로를 따라가는 정적 코드 리뷰입니다. [README](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/README.md#L19)

분석 대상은 커밋 `47918f787d845c1901887626e3cff14c245253e0`이며, 매니페스트의 버전은 `2026.9.3`입니다. 저장소의 의존성을 설치하거나 코드를 실행하지 않았으므로 성능·실행 성공·운영 안정성을 검증한 결과로 읽어서는 안 됩니다. [package.json](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/package.json#L1)

## 무엇을 제공하는가

OpenClaw의 구성 요소를 이해하려면 **모델**, **에이전트 실행 런타임(harness)**, **Gateway**를 구분해야 합니다. 모델은 입력에 대한 생성과 도구 호출 결정을 담당합니다. 실행 런타임은 대화 기록, 모델 호출, 도구 사용과 취소를 실행 단위로 묶습니다. Gateway는 어떤 세션과 실행에 요청을 연결하고 결과를 어디로 보낼지 조정합니다.

README는 모델과 harness를 플러그인으로 교체할 수 있다고 소개합니다. 구현에도 제공자·모델 설정으로부터 runtime ID를 수집하고 harness 정책을 해석하는 코드가 있습니다. 다만 이것은 모든 조합이 동일하게 동작한다는 검증은 아닙니다. 실제 실행에는 선택된 런타임과 모델, 인증 방식에 따른 분기가 존재합니다. [런타임 선택 설정](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/src/agents/harness-runtimes.ts#L39)

문서의 Gateway 구조는 WebSocket 위에서 요청·응답과 서버 이벤트를 교환합니다. 기본 바인딩 주소는 문서상 `127.0.0.1:18789`이며, Control UI도 이 Gateway API를 사용합니다. 네이티브 장치는 별도의 `node` 역할과 기능 목록을 가지고 연결됩니다. 따라서 장치 명령과 대화 요청이 같은 연결 기반을 공유하더라도 동일한 권한이나 실행 의미를 가지는 것은 아닙니다. [아키텍처 문서](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/docs/concepts/architecture.md#L9)

## 아키텍처: 입력과 실행, 출력을 분리한 구조

| 영역 | 이 글에서 확인한 책임 | 대표 파일 |
|---|---|---|
| Gateway RPC | `chat.send` 요청 접수, 정규화, 세션 확인, ACK | `src/gateway/server-methods/chat-send-handler.ts` |
| 라우팅 | 채널·계정·상대방 정보를 세션 키에 반영 | `src/routing/resolve-route.ts` |
| 자동 응답 | 채널 공통 문맥과 응답 dispatcher 연결 | `src/auto-reply/dispatch.ts` |
| 답변 준비 | 문맥·정책·실행 준비 및 런타임 수명 관리 | `src/auto-reply/reply/get-reply-run.ts` |
| 실행 조율 | 세션/전역 큐, 런타임 분기, 실행 루프 | `src/agents/embedded-agent-runner/run-orchestrator.ts` |
| 실행 시도 | 도구·프롬프트·세션 준비와 정리 | `src/agents/embedded-agent-runner/run/attempt.ts` |
| 응답 출력 | 블록·최종·도구 결과 구분, 기록 및 방송 | `src/gateway/server-methods/chat-send-reply-dispatch.ts` |

[![Control UI 요청이 세션 확인과 ACK, 자동 응답, 실행 큐, 모델 및 도구 실행, 응답 전달을 거치는 흐름]({{ '/img/reviews/2026/openclaw-review/message-flow.svg' | relative_url }})]({{ '/img/reviews/2026/openclaw-review/message-flow.svg' | relative_url }})

*그림 1. 리뷰어 작성, 분석 커밋 기준. 일반적인 Control UI 요청에서 embedded 실행으로 이어지는 대표 경로입니다. 중간의 정책·훅·오류 분기는 생략했으며, CLI 실행은 조건부 대체 경로로 표시했습니다. 그림을 누르면 확대할 수 있습니다. 근거: [ACK 및 dispatch](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/src/gateway/server-methods/chat-send-handler.ts#L480), [실행 큐와 CLI 분기](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/src/agents/embedded-agent-runner/run-orchestrator.ts#L191), [프롬프트 제출](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/src/agents/embedded-agent-runner/run/attempt-execution-phase.ts#L112), [출력 수집](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/src/gateway/server-methods/chat-send-reply-dispatch.ts#L424).*

이 그림을 읽을 때 중요한 점은 Gateway의 접수 성공, 모델 실행의 종료, 사용자에게 답변이 전달되는 시점이 서로 구분된다는 것입니다. 이는 아래 코드 흐름에서도 반복해서 나타납니다.

## 작동 원리: 메시지 한 건을 끝까지 따라가기

### 1. chat.send를 검증된 내부 요청으로 바꿉니다

`chat.ts`는 `chat.send`를 `handleDirectExternalChatSend`에 연결합니다. 이 함수는 외부 요청의 authority admission 정보를 구성해 `handleChatSend`에 전달합니다. 코드 주석도 인증된 외부 진입과 내부 재진입을 구분합니다. 단, 여기서 호출 관계를 확인했다는 사실만으로 인증 체계 전체의 보안성을 평가한 것은 아닙니다. [RPC 등록](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/src/gateway/server-methods/chat.ts#L56), [외부 진입점](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/src/gateway/server-methods/chat-send-external-entry.ts#L38)

요청 정규화 함수 `normalizeChatSendRequest`는 `validateChatSendParams`로 매개변수 형식을 검사합니다. 실패하면 세션 작업으로 진행하기 전에 오류를 반환합니다. 내부 표현에는 메시지 본문뿐 아니라 첨부파일, 입력 출처, 중단 명령 여부, 요청 식별 정보도 포함됩니다. 같은 텍스트라도 어디에서 왔고 어떤 종류의 요청인지가 처리에 영향을 주는 구조입니다. [요청 타입과 검증](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/src/gateway/server-methods/chat-send-request.ts#L50)

### 2. 세션과 실행을 서로 다른 식별자로 관리합니다

`prepareChatSendSession`은 세션을 로드한 뒤 선택된 agent가 유효한지, 삭제된 agent를 가리키는지, 새 세션 생성이 허용되는지 등을 확인합니다. 존재하지 않는 incognito 세션도 오류로 처리합니다. 이후 단계가 잘못된 저장 대상이나 실행 주체를 그대로 받아들이지 않도록 앞단에서 확인하는 것입니다. [세션 준비](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/src/gateway/server-methods/chat-send-session.ts#L153)

이때 `sessionKey`와 `runId`를 혼동하면 흐름을 놓치기 쉽습니다. `sessionKey`는 대화를 어느 세션 문맥에 연결할지 나타내며, `clientRunId`는 이 요청의 실행 식별자입니다. 현재 구현에서는 `clientRunId`를 요청의 `idempotencyKey`에서 가져옵니다. 이는 재전송을 식별할 토대를 제공하지만, 이 한 줄만으로 모든 장애 상황에서 정확히 한 번 실행된다고 보장할 수는 없습니다. [실행 ID 결정](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/src/gateway/server-methods/chat-send-session.ts#L88)

채널 쪽 라우팅의 `buildAgentSessionKey`는 agent ID 외에도 channel, account ID, peer 종류/ID, DM 범위와 identity links를 넘깁니다. 따라서 여러 채널에서 같은 사람을 만난다고 해서 모든 대화가 자동으로 하나의 기록에 합쳐진다고 가정해서는 안 됩니다. 설정된 세션 범위와 식별 연결이 중요합니다. [세션 키 구성](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/src/routing/resolve-route.ts#L96)

### 3. 먼저 started를 응답하고 실행은 뒤에서 진행합니다

세션과 입력 접수 준비가 끝나면 Gateway는 실행을 등록하고 ACK payload를 만듭니다. 아래는 실제 코드의 일부입니다.

```typescript
const ackPayload = {
  ...goalResult,
  runId: clientRunId,
  status: "started" as const,
  ...(receipt ? { messageSeq: receipt.activeMessagePosition + 1 } : {}),
  ...(interruptedActiveRun ? { interruptedActiveRun: true } : {}),
  ...(serverTiming ? { serverTiming } : {}),
};
```

출처: [chat-send-handler.ts](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/src/gateway/server-methods/chat-send-handler.ts#L504)

이어 `respond(true, ackPayload, ...)`를 호출한 다음 `startChatDispatch`로 넘깁니다. **`started`는 답변 생성 완료가 아닙니다.** 사용자는 접수 응답을 먼저 받고, 이후의 실행 상태와 응답을 별도로 관찰하게 됩니다. 코드 주석은 ACK 이후에는 dispatch가 해당 턴의 기록 보존 책임을 가진다고 명시합니다. 접수와 실행을 분리하는 만큼, 오류가 발생했을 때 누가 기록과 첨부 자원을 정리하는지도 구분해야 하는 설계입니다. [응답 및 소유권 전환](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/src/gateway/server-methods/chat-send-handler.ts#L525)

### 4. WebChat 입력을 채널 공통 응답 파이프라인에 연결합니다

`startChatDispatch` 내부는 `dispatchInboundMessageWithProjectedDispatcher`를 호출합니다. 이 wrapper는 응답 modifier와 전송 훅을 묶고 `dispatchInboundMessage`로 연결합니다. 이 공통 함수는 `finalizeInboundContext`로 입력 문맥을 정리한 뒤 `dispatchReplyFromConfig`에 문맥, 설정, dispatcher와 reply options를 전달합니다. [Gateway 연결](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/src/gateway/server-methods/chat-send-agent-dispatch.ts#L331), [공통 dispatch](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/src/auto-reply/dispatch.ts#L220)

여기서 dispatcher는 답변을 만들어 내는 모델 자체가 아닙니다. 생성되는 응답을 어떤 정책과 전달 절차로 처리할지 담당합니다. 답변을 구하는 쪽은 기본적으로 `getReplyFromConfig`를 선택합니다. 별도 reply resolver를 주입할 수 있는 구조도 코드에 나타납니다. [응답 resolver 선택](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/src/auto-reply/reply/dispatch-from-config.prepare-execution.ts#L349)

공통 dispatch 모듈에는 채널용 buffered dispatcher와 WebChat에서 쓰는 plain/projected dispatcher가 함께 있습니다. buffered 경로는 세션·채널·계정·대상 등의 복합 키로 foreground 전송 순서를 관리합니다. 이 장치를 모든 경로가 동일하게 사용한다고 일반화하면 안 됩니다. **실행 순서 제어와 채널 전달 순서 제어는 서로 다른 층에 있습니다.** [전송 순서 키](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/src/auto-reply/dispatch.ts#L77), [buffered 경로](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/src/auto-reply/dispatch.ts#L305)

### 5. 답변 준비와 모델 후보 선택을 거쳐 실행 런타임에 진입합니다

`getReplyFromConfig`는 `runPreparedReply`로 이어집니다. 후자는 문맥 준비와 admission 결과가 즉시 답변이면 반환하고, 그렇지 않으면 실행합니다. 준비된 플러그인 런타임을 사용하는 경우에는 lease를 획득해 실행 범위를 감싼 뒤 `finally`에서 해제합니다. 여기서 lease는 해당 실행 동안 사용할 런타임 자원의 수명을 관리하는 장치로 읽을 수 있습니다. [답변 준비](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/src/auto-reply/reply/get-reply.ts#L1245), [준비와 해제](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/src/auto-reply/reply/get-reply-run.ts#L11)

이후 `executePreparedReplyRun`에서 `runReplyAgent`로 이어지고, 실행 계층은 fallback candidate를 구성합니다. `runEmbeddedAgentEntry`에는 선택한 provider/model, fallback 설정, 세션·실행 식별자, harness 선택 정보가 전달됩니다. embedded candidate의 실제 호출은 `runEmbeddedAgent(embeddedRunParams)`입니다. 이 사이에는 추가 정책과 처리 분기가 있으므로 하나의 직선 호출만 존재하는 것은 아닙니다. [reply 실행](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/src/auto-reply/reply/get-reply-run-execute.ts#L586), [후보 실행 계약](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/src/auto-reply/reply/agent-runner-fallback-candidate.ts#L132), [embedded 호출](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/src/auto-reply/reply/agent-runner-embedded-candidate.ts#L394)

리뷰어 관점에서 이 계층 분리는 모델 선택 정책을 대화 접수와 분리한다는 의미가 있습니다. 다만 fallback이 있다고 해서 비용이나 결과의 동등성까지 보장되지는 않습니다. 이 글에서는 실제 제공자 장애를 발생시켜 복구를 검증하지 않았습니다.

### 6. 같은 세션의 실행과 전체 실행량을 따로 조정합니다

`run-orchestrator.ts`는 lane controller로부터 `enqueueSession`과 `enqueueGlobal`을 받아, 세션 큐 안에서 전역 큐로 진입합니다. 먼저 해당 세션의 지연된 기록 정리 작업을 기다린 뒤 전역 실행 단계로 넘어갑니다. 코드 주석은 한 세션의 유지 작업 대기가 다른 세션의 시작까지 막지 않도록 이 순서를 택했다고 설명합니다. [큐 구성과 실행](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/src/agents/embedded-agent-runner/run-orchestrator.ts#L191)

같은 대화의 기록을 동시에 읽고 쓰는 문제와 전체 서버의 동시 실행량 문제를 하나의 잠금으로 해결하려 하지 않는 구조입니다. 이것은 코드에서 확인한 동시성 제어의 의도이며, 실제 처리량을 측정한 결과는 아닙니다.

전역 큐에 진입한 다음에는 `runEmbeddedAgentViaCliBackendIfEligible`로 CLI 실행 가능 여부를 확인합니다. 해당 결과가 있으면 곧바로 반환합니다. 따라서 이름에 embedded가 들어간다고 해서 항상 동일한 내부 모델 루프를 거치는 것은 아닙니다. 아래 설명은 이 대체 경로로 반환하지 않는 embedded 실행의 내부 준비를 중심으로 합니다. [CLI 분기](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/src/agents/embedded-agent-runner/run-orchestrator.ts#L237)

### 7. 도구 목록과 프롬프트를 실행 조건에 맞게 구성합니다

`run/attempt.ts`는 한 번의 실행 시도를 준비하는 코드입니다. 도구 기반 구성, 번들 도구, 도구 카탈로그, 시스템 프롬프트, 세션 런타임과 기록 수명 관리 등을 별도 함수로 나누어 조립합니다. 이 구조에서는 “모델을 한 번 호출한다”는 설명만으로 실제 작업량과 책임을 설명하기 어렵습니다. [실행 시도 구성](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/src/agents/embedded-agent-runner/run/attempt.ts#L24)

도구 준비 단계는 `resolveAgentToolSurfacePlan`에 모델·설정·세션과 `toolsAllow` 등 조건을 넘깁니다. 이후 `createOpenClawCodingTools`에 sandbox 등의 정보를 전달해 도구를 구성합니다. 도구 사용 가능 여부는 단순히 프롬프트에 이름을 적어 두는 문제가 아니라 실행 시점의 정책과 도구 표면 구성에 연결되어 있습니다. 다만 개별 도구의 권한 검사를 모두 감사한 것은 아닙니다. [도구 계획](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/src/agents/embedded-agent-runner/run/attempt-tool-prepare.ts#L99), [도구 생성](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/src/agents/embedded-agent-runner/run/attempt-tool-prepare.ts#L269)

프롬프트 제출 직전의 `promptActiveSession`은 기록 쓰기의 소유권 문맥 안에서 동작합니다. 이미 취소된 실행인지 확인하고 `activeSession.prompt(prompt, options)`를 호출하며, 그 Promise를 취소 가능한 형태로 감쌉니다. 코드 주석은 `prompt`가 자체 agent loop를 시작한다고 설명합니다. 따라서 이 지점은 준비된 세션·도구·문맥이 실제 실행 루프로 넘어가는 경계입니다. [실행 루프 진입](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/src/agents/embedded-agent-runner/run/attempt-execution-phase.ts#L112)

### 8. 도구 결과와 최종 답변을 구분해 화면과 기록에 반영합니다

WebChat의 `createChatSendReplyDispatch`는 `deliver`에서 응답 종류를 나눕니다. `block`과 `final`은 전달 결과 목록에 쌓고, `tool`은 미디어를 포함한 경우 텍스트를 제거한 최종 payload 형태로 모읍니다. 이 처리는 도구 내부 결과를 그대로 사용자 메시지로 노출하는 것과 구분됩니다. [응답 종류 분기](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/src/gateway/server-methods/chat-send-reply-dispatch.ts#L424)

이 파일에는 미디어 응답의 기록 반영과 중복 키 처리도 있습니다. 별도 source finalization 코드는 현재 세션의 writer가 여전히 유효한지 확인하고 `broadcastChatFinal`을 호출하는 경로를 포함합니다. 이미 바뀐 세션 소유권으로 오래된 실행이 최종 답변을 덮어쓰지 않도록 주의하는 설계가 드러납니다. [미디어 정리](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/src/gateway/server-methods/chat-send-reply-dispatch.ts#L471), [최종 방송 전 확인](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/src/gateway/server-methods/chat-send-source-finalization.ts#L420)

따라서 사용자에게 보이는 결과는 단일 문자열 이상의 것입니다. 실행 중 이벤트, 블록 응답, 최종 응답, 도구 미디어와 기록의 반영 상태가 조율됩니다. 이 점이 단순한 모델 API wrapper와 비교할 때 OpenClaw 코드에서 가장 많은 설명을 필요로 하는 부분입니다.

## 문서 기준 설치와 사용

아래 명령은 분석 커밋의 README에 있는 npm 설치 및 초기 사용 절차입니다. 이 리뷰에서는 실행하지 않았습니다. README는 Node `24.16+` 또는 `26.1+`를 안내하며, 매니페스트의 범위는 `>=24.16.0 <25 || >=26.1.0`입니다. [설치 문서](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/README.md#L40), [런타임 범위](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/package.json#L2285)

```bash
npm install -g openclaw@latest --allow-scripts=openclaw
```

이 옵션 형태는 README에서 npm 12 또는 npm 11.16 이상을 대상으로 설명합니다. npm 11.15 이하에서는 `--allow-scripts=openclaw`를 생략하라고 안내합니다. `latest`는 설치 시점에 다른 버전을 가져올 수 있으므로, 위 명령으로 이 리뷰의 고정 커밋과 동일한 소스가 설치된다는 의미는 아닙니다. [npm 조건](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/README.md#L46)

```bash
openclaw onboard --install-daemon
```

```bash
openclaw gateway status
openclaw dashboard
```

README에 따르면 onboarding은 모델 접근을 확인하고 workspace와 Gateway를 구성하며, dashboard는 Control UI를 엽니다. 소스 개발은 pnpm workspace를 사용하고 루트에서 일반 `npm install`은 지원하지 않는다고 명시합니다. 설치 패키지 사용과 저장소 개발 절차를 구분해야 합니다. [초기 사용](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/README.md#L56), [개발 절차](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/README.md#L110)

## 한계와 주의점

**로컬 상태 저장과 외부 전송은 별개입니다.** README는 상태·메모리·자격 증명이 사용자 하드웨어에 저장된다고 설명하면서도, 프롬프트는 설정한 모델 제공자와 채팅 플랫폼으로 전송된다고 명시합니다. 따라서 “내 장치에서 실행”을 “모든 처리가 오프라인”으로 해석하면 문서와 달라집니다. 이 리뷰는 README의 데이터 전송 설명을 전체 네트워크 감사로 확인한 것은 아닙니다. [데이터 처리 설명](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/README.md#L21)

**도구 실행의 격리 수준을 별도로 확인해야 합니다.** README는 sandbox를 설정하지 않으면 main session의 도구가 host에서 실행된다고 안내합니다. 또한 외부 메시지를 신뢰하지 말고 모르는 DM 발신자는 pairing 절차로 다루도록 설명합니다. 다양한 채널을 연결하는 편의성이 모든 발신자를 같은 신뢰 수준으로 취급해도 된다는 뜻은 아닙니다. [보안 안내](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/README.md#L87)

**문서상의 지원 범위와 이 글의 검증 범위는 다릅니다.** 다수 채널·장치·런타임 지원은 프로젝트가 제시하는 기능 범위입니다. 이 글에서 확인한 것은 Control UI 대표 실행 경로와 연결된 코드이며, 실제 계정 연결·장치 동작·재시작 복구·동시성·fallback 성공을 확인하지 않았습니다. README의 핵심 Gateway 설명과 분석한 대표 경로는 일치하지만, 이것이 모든 기능의 동일한 품질을 입증하지는 않습니다.

라이선스는 MIT입니다. 저작권 및 허가 고지의 포함 조건과 무보증 조항이 있습니다. [LICENSE](https://github.com/openclaw/openclaw/blob/47918f787d845c1901887626e3cff14c245253e0/LICENSE#L1)

## 이 글에서 다루지 못한 부분

각 채널 extension의 인증·전송 구현, 네이티브 앱과 node 명령, 브라우저·컴퓨터 제어 도구 내부, 모든 모델/harness 플러그인, 메모리 검색과 context engine의 세부 알고리즘, cron·하위 에이전트 관리, 전체 보안 경계 및 테스트 스위트는 상세 분석에서 제외했습니다. 특히 모델별 토큰 스트리밍과 도구 실행 루프 전체를 줄 단위로 검증한 리뷰는 아닙니다. Gateway의 대표 경로와 실행 진입·출력 조율을 중심으로 범위를 한정했습니다.

## 결론

OpenClaw에서 공부할 핵심은 메시지 접수, 대화 식별, 실행 조율과 결과 전달을 별도 책임으로 나눈 방식입니다. `chat.send`는 입력과 세션을 확인하고 접수 ACK를 반환하며, 공통 응답 파이프라인은 문맥과 전달 규칙을 결합합니다. 실행 계층은 모델·런타임·도구를 선택하고 세션 및 전역 큐를 거쳐 작업을 수행하며, 출력 계층은 블록·최종·미디어 응답과 기록을 정리합니다.

이 구조는 개인 비서를 여러 채널과 장치로 확장할 때 모델 호출 바깥에 어떤 제어 코드가 필요한지 보여줍니다. 특히 접수 완료와 작업 완료의 분리, 세션과 실행의 식별자 구분, 실행 순서와 전달 순서의 분리가 이 저장소의 대표 경로에서 확인한 중요한 설계 요소입니다.
