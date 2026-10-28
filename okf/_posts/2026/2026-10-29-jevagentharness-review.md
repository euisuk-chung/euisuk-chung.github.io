---
type: "Repo Review"
title: "[Repo Review] JevAgentHarness — 작은 결정 모델이 코딩 에이전트의 다음 LLM을 고르는 방법"
description: "JevAgentHarness의 모델 라우팅·종료 재검사·임계값 조정·API 변환 흐름을 추적하고, 논문 결과와 프록시 실험 및 운영 경계를 구분합니다."
date: "2026-10-29"
tags:
  - "Repo Review"
  - "AI Agent"
  - "Tools"
resource: "https://github.com/JevAgentHarness/JevAgentHarness/tree/f2932199e1ef1d9f089b51d39430c87be0f560b5"
generated:
  by: "process:blog-review"
  at: "2026-10-29T06:06:39+09:00"
sources:
  - id: "github:JevAgentHarness/JevAgentHarness"
    title: "JevAgentHarness/JevAgentHarness"
    resource: "https://github.com/JevAgentHarness/JevAgentHarness/tree/f2932199e1ef1d9f089b51d39430c87be0f560b5"
    revision: "f2932199e1ef1d9f089b51d39430c87be0f560b5"
    last_modified: "2026-10-16T02:10:17Z"
status: "stable"
year: "2026"
analyzed_at: "2026-10-29T06:06:39+09:00"
source_id: "jevagentharness/jevagentharness"
source_revision: "f2932199e1ef1d9f089b51d39430c87be0f560b5"
source_type: "repo"
source_url: "https://github.com/JevAgentHarness/JevAgentHarness/tree/f2932199e1ef1d9f089b51d39430c87be0f560b5"
visual_sources:
  - path: "/img/reviews/2026/jevagentharness-review/architecture.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/server.py#L630"
    caption: "프록시 모델 호출과 클라이언트 도구 실행의 경계"
    source_revision: "f2932199e1ef1d9f089b51d39430c87be0f560b5"
  - path: "/img/reviews/2026/jevagentharness-review/routing-flow.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/server.py#L197"
    caption: "기본 cascade와 fast 실패·종료의 strong 재작성 흐름"
    source_revision: "f2932199e1ef1d9f089b51d39430c87be0f560b5"
---

## 매 단계에 같은 모델을 써야 할까요?

코딩 에이전트는 하나의 질문에 답하고 끝나지 않습니다. 파일을 읽고, 명령을 만들고, 테스트 결과를 확인한 뒤 다음 행동을 정하는 과정을 반복합니다. 이때 모든 모델 호출을 가장 강한 모델에 맡기면 단순 조회와 어려운 오류 분석에 같은 비용 구조를 적용하게 됩니다. 반대로 작은 모델로 전부 바꾸면, 초기에 잘못 고른 행동이 이후 상태까지 바꿀 수 있습니다.

**JevAgentHarness는 에이전트와 모델 공급자 사이에 놓는 로컬 프록시입니다.** 작은 결정 모델이 다음 단계가 일상적인 작업인지 어려운 작업인지 판단하고, 실제 응답을 작성할 LLM을 `fast` 또는 `strong`으로 고릅니다. 도구를 실행하는 주체는 계속 원래 에이전트입니다. 프록시는 그 에이전트가 공급자에게 보낼 모델 요청과 돌아오는 응답을 다룹니다. [프로젝트 설명](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/README.md#L28), [패키지 정의](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/pyproject.toml#L5)

여기에는 구별할 대상이 두 가지 있습니다. 루트의 `src/jevagentharness`는 배포 가능한 작은 프록시이고, `research/`는 논문 *JevAgentHarness: Benchmarking, Deploying and Training Decision Models That Share Control with LLMs*의 실험·학습 코드입니다. 논문에서 의사결정 자체를 위임한 결과를 프록시의 모델 라우팅 성능으로 옮겨 읽으면 안 됩니다. 이 리뷰는 **2026년 10월 16일 커밋 `f293219`의 프록시 구현**을 중심으로 분석합니다. 실제 API 호출·설치·벤치마크 실행은 수행하지 않았습니다. [두 패키지의 구분](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/research/README.md#L3)

## 무엇을 제공하나요?

프록시는 OpenAI 호환 **Chat Completions**와 **Responses** 형식을 받아 Gemini native API, OpenAI 호환 Chat API 또는 Responses API로 변환합니다. 클라이언트는 실제 공급자 모델명 대신 다음 세 이름을 사용할 수 있습니다.

| 클라이언트 모델명 | 기본 동작 | 비교할 때의 역할 |
|---|---|---|
| `jah-auto` | 다음 단계를 판단해 두 tier 사이에서 라우팅 | 실험 대상 |
| `jah-strong` | strong tier로 고정 | 같은 하네스의 기준선 |
| `jah-fast` | fast tier로 고정 | 작은 모델만 사용한 참고선 |

Tier는 실제 모델, 공급자, 추론 effort를 묶은 설정입니다. **결정 모델과 fast 모델은 같은 개념이 아닙니다.** 결정 모델은 선택지별 확률을 반환하고, fast 모델은 선택된 경우 도구 인자와 응답 본문을 작성합니다. 기본 설정은 결정 모델 `typesafe/jev-1.13`, strong `gemini-4-argon`/high, fast `gemini-3.5-flash-lite`/low입니다. 이 모델명은 분석 커밋의 설정값이며 현재 공급자 상품이나 이용 가능성을 검증한 목록은 아닙니다. 알 수 없는 클라이언트 모델명은 기본 모델 설정으로 해석됩니다. [기본 설정](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/config.py#L15), [이름 해석](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/config.py#L176)

## 아키텍처: 실행 환경은 클라이언트에 남습니다

![코딩 에이전트가 로컬 프록시에 요청을 보내면 형식 변환과 결정 모델 판단을 거쳐 strong 또는 fast LLM을 호출하고, 도구 실행은 원래 에이전트에서 수행하는 구조]({{ '/img/reviews/2026/jevagentharness-review/architecture.svg' | relative_url }})

*리뷰어 작성, 분석 커밋 기준. 프록시의 모델 API 호출과 클라이언트의 도구 실행을 분리했습니다. [HTTP 진입점](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/server.py#L630), [공급자 호출](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/upstreams/__init__.py#L91), [공통 자료형](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/types.py#L69).*

| 경로 | 책임 |
|---|---|
| `cli.py`, `config.py` | `jah` 명령, YAML·CLI 설정과 모델 이름 검증 |
| `dialects/chat.py`, `dialects/responses.py` | 외부 요청을 공통 `Request`로 바꾸고 응답을 원래 형식으로 반환 |
| `router.py`, `decision.py` | 실행 상태 요약, routine/hard 질문, 결정 모델 또는 규칙 backend |
| `points.py`, `server.py` | 도구 선택·종료·성찰·행동 검사와 재작성 제어 |
| `upstreams/` | 실제 모델 API, 재시도, 공급자별 서명·reasoning·캐시 처리 |
| `fit.py`, `report.py`, `prices.py` | 로그 기반 임계값 조정, 비용·지연 집계 |
| `bench/`, `research/` | 프록시 비교 실험과 별도의 논문 연구 코드 |

패키지는 Python 3.10 이상을 요구하며 핵심 의존성은 `aiohttp`와 `pyyaml`입니다. CLI 진입점 `jah`는 `jevagentharness.cli:main`에 연결되고, wheel 패키지 대상은 `src/jevagentharness`입니다. 따라서 프록시를 사용하는 데 연구용 GPU 학습 환경을 함께 설치하는 구조는 아닙니다. [매니페스트](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/pyproject.toml#L40)

## 작동 원리: 요청 하나가 반환되기까지

### 1. API 형식을 내부 대화로 바꿉니다

`POST /v1/chat/completions`와 `POST /v1/responses`는 공통 `_serve()`에 들어가 서로 다른 parser를 사용합니다. Chat의 `messages`, Responses의 `input` 항목·함수 호출·도구 결과를 내부 `Message`, `ToolCall`, `Tool`, `Request`로 통일합니다. 클라이언트의 developer 메시지는 내부 system 역할로 정리합니다.

Responses의 이름공간 도구는 평탄화된 이름으로 공급자에게 전달하고, custom tool은 하나의 문자열 인자를 갖는 함수로 감쌀 수 있습니다. 그러나 hosted `web_search`나 image generation 등을 그대로 제공하지는 않습니다. “OpenAI 호환”이라는 표현을 모든 Responses 기능의 완전한 대리 구현이라고 읽으면 안 됩니다. [Chat parser](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/dialects/chat.py#L49), [Responses parser](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/dialects/responses.py#L60), [custom 변환](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/upstreams/__init__.py#L173)

### 2. 세션과 단계는 요청에 들어 있는 이력으로 식별합니다

세션 힌트는 URL의 `/s/<session>/`, `X-JAH-Session` 헤더, dialect별 힌트 순으로 가져옵니다. 명시적 값과 요청의 세션 식별자가 모두 없으면 system 프롬프트와 첫 user 과제의 일부를 SHA-256으로 해시합니다. 서버는 여기에 클라이언트 모델명을 붙여 `jah-auto`와 `jah-strong` 비교 실행의 세션을 나눕니다.

단계 번호는 서버가 요청 횟수를 세어 만드는 값이 아니라 **요청 이력에 이미 있는 assistant 턴 수**입니다. 같은 세션·같은 단계의 재요청에는 저장한 라우팅 판단과 요청 변형을 재사용합니다. 최근 판단 기록은 제한된 범위로 남습니다. 이 동작은 요청을 영구 보관하는 대화 데이터베이스와 다르며, 재시도 판단의 재사용도 모든 모델 호출을 없애는 응답 캐시는 아닙니다. [단계 정의](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/types.py#L90), [세션 키](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/router.py#L107), [서버의 세션](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/server.py#L154)

### 3. 결정 모델에는 전체 대화 대신 실행 요약을 보냅니다

`episode()`는 첫 user 메시지를 과제로 읽고, assistant의 도구 호출 또는 텍스트와 그 뒤의 tool/user 결과를 단계별로 묶습니다. `render_state()`는 다음 범위로 상태를 만듭니다.

| 입력 부분 | 코드의 범위 |
|---|---|
| 과제 | 공백 정리 후 최대 3,000자 |
| 최근 이력 | 마지막 6개 assistant 단계 |
| 단계별 행동 | 최대 400자 |
| 이전 결과 | 단계당 최대 300자 |
| 가장 최근 결과 | 뒤쪽 최대 2,500자를 중심으로 유지 |

앞뒤 또는 끝부분을 유지하는 문자열 절단이며, 별도 LLM 요약을 호출하지 않습니다. 이 요약은 결정 모델용 입력입니다. 실제 응답을 작성할 LLM에는 공급자 변환을 거친 요청이 전달되므로, 이 표를 에이전트 전체 문맥 길이로 해석해서는 안 됩니다. [상태 구성](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/router.py#L48)

### 4. `p(hard)`와 임계값으로 LLM tier를 고릅니다

질문은 “에이전트의 **다음** 단계가 routine인가 hard인가?”입니다. 이미 계획한 파일 읽기·명령 실행은 routine의 예이고, 예상 밖 실패·새 계획·반복 행동·완료 판정은 hard의 예로 지시합니다. 기본 첫 단계는 판단을 생략하고 strong으로 보냅니다. 추가 설정으로 strong 유지 단계 수와 연속 fast 단계의 상한도 둘 수 있지만, 둘의 기본값은 0입니다.

그다음 기본 cascade 정책은 `p(hard) >= tau`이면 strong, 아니면 fast입니다. 기본 `tau`는 0.75입니다. 이는 **가장 확률이 높은 답의 confidence가 임계값을 넘으면 작은 모델이 대신 결정한다**는 일반적인 위임 규칙과 다릅니다. 예를 들어 `p(hard)`를 비교하므로 임계값을 높이면 strong으로 보내는 조건이 더 엄격해집니다. 이 확률을 실제 과제 성공률이나 검증된 난이도 정답으로 읽지도 않습니다. [질문 원문](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/router.py#L33), [분기 구현](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/router.py#L149)

Jev backend는 `POST {base_url}/v1/systemone`에 상태와 typed choice 질문을 보냅니다. 반환된 선택지 확률을 정규화하고, 유효한 분포가 없으면 오류로 취급합니다. 기본 OpenRouter, TypeSafe, self-hosted local 서버를 선택할 수 있습니다. `rules` backend는 모델 호출 대신 반복 행동과 최근 결과의 오류 패턴을 사용하지만 도구 선택·완료 질문 등은 답하지 못해 해당 기능의 LLM 경로로 돌아갑니다. 모델 API key를 없애는 규칙 대안과, 작은 모델을 자체 호스팅하는 방식은 서로 다릅니다. [backend와 endpoint](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/decision.py#L32), [분포 파싱](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/decision.py#L130), [규칙 범위](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/decision.py#L172)

### 5. 선택한 모델을 호출하고 실패·완료를 다시 확인합니다

![기본 정책은 첫 단계를 strong으로 보내고 이후 routine/hard 확률로 tier를 고른 뒤, fast 오류나 도구 사용 중 종료 응답은 strong에서 다시 작성하는 흐름]({{ '/img/reviews/2026/jevagentharness-review/routing-flow.svg' | relative_url }})

*리뷰어 작성, 분석 커밋 기준. 기본 cascade와 종료 검사만 표시했습니다. 확장 decision point의 검사와 strong 재호출 오류는 본문에 별도로 설명합니다. [라우터](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/router.py#L137), [호출·재검사](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/server.py#L197), [종료 검사 조건](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/server.py#L390).*

`Upstreams.call()`은 tier의 공급자 형식으로 요청을 바꿔 모델 API를 호출하고, 응답을 공통 `Response`로 되돌립니다. Gemini는 `generateContent`, Chat 공급자는 `/chat/completions`, Responses 공급자는 `/responses`를 사용합니다. 재시도 가능한 HTTP 상태, 타임아웃, Gemini thought signature와 선택적 explicit context cache도 이 계층에서 다룹니다. 일부 공급자별 정보를 유지하는 장치가 있으므로 단순히 JSON의 `model` 문자열만 교체하는 프록시는 아닙니다. [공급자 변환·호출](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/upstreams/__init__.py#L91)

결정 모델의 오류·타임아웃은 기본적으로 strong 경로를 고르게 합니다. fast 호출이 실패하면 원래 요청에 가까운 형태로 strong 호출을 한 번 더 시도합니다. 다만 **strong까지 실패해도 언제나 정상 응답을 보장하는 구조는 아닙니다.** 시도할 대체 경로가 없으면 `UpstreamError`가 HTTP 오류 또는 SSE 오류로 반환됩니다. README의 fail-safe는 라우터 장애가 기본 LLM 경로를 유지하게 한다는 의미로 읽는 편이 정확합니다. [fast 실패 대체](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/server.py#L197), [HTTP 오류 반환](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/server.py#L630)

기본 종료 검사는 요청에 도구가 있고, 응답이 도구 호출 없이 끝나는 경우 fast의 답을 strong에서 다시 작성합니다. mini-swe-agent처럼 shell 명령으로 제출하는 하네스는 `stop.submit` 패턴으로 종료 행동을 추가 식별할 수 있습니다. 도구 없이 plain JSON으로 대화하는 방식까지 자동으로 완료 판정을 이해하는 것은 아닙니다. 또 strong의 재작성은 채점기를 실행해 과제 성공을 증명하는 절차가 아닙니다. [종료 판정](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/points.py#L340), [실제 검사](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/server.py#L390)

### 6. 추가 decision point는 응답을 만들기 전후에 개입합니다

기본 라우팅 외 기능은 `points.py`의 설정과 서버의 전·후처리로 연결됩니다.

| Point | 대표 동작 | 경계 |
|---|---|---|
| `tool_select` | 확신한 도구를 강제하고 fast LLM이 인자를 작성하거나, 도구 후보를 줄이거나, 다른 선택을 재검사 | tool과 인자를 결정 모델 혼자 모두 작성하는 기능은 아님 |
| `stop` | strong 종료 확인, 결정 모델의 done 확률 검사, 종료 재검토 지침 | 완료 확률은 실제 과제 채점 결과가 아님 |
| `reflection` | 막힌 상태로 판단하면 strong에 재검토 지침 추가 | 항상 비용을 줄이는 기능은 아님 |
| `action` | 위험 패턴의 제안 도구 호출을 읽고 strong에 재검토 요청 | 도구 실행 권한을 차단하는 sandbox나 승인 시스템은 아님 |

도구 선택 cascade의 임계값은 `p(hard)`가 아니라 **선택한 도구의 확률**에 적용됩니다. hard·첫 단계 등 강제로 strong에 남겨둔 요청을 이 기능이 임의로 fast로 옮기지는 않습니다. `assist`는 top-k와 이미 사용한 도구를 남깁니다. 메모리 읽기·쓰기와 일부 도구 인자만 채우는 기능은 프록시가 제공하지 않으며, 잘못된 설정을 검증 단계에서 거부합니다. [지원 point와 mode](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/points.py#L34), [호출 전 적용](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/server.py#L289)

여러 사후 검사가 응답을 의심하면 action → tool → routing → stop → finish 순으로 사유를 정리하고 strong에서 재작성합니다. 재작성 결과도 위험 도구를 제안하면 action 검사가 추가로 확인할 수 있습니다. 이때도 최종 도구 실행은 클라이언트에 남고, action guard의 결과가 호출의 영구 차단을 뜻하지 않습니다. [재작성 제어](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/server.py#L197), [action 검사](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/server.py#L480)

### 7. 반환은 호환 형식으로, 스트림은 완성 응답으로 만듭니다

스트림 요청을 받으면 서버는 SSE 응답을 열고 모델 호출을 기다리는 동안 10초 주기로 keepalive 주석을 보낼 수 있습니다. **상류 모델의 생성 토큰을 즉시 중계하는 방식은 아닙니다.** 완성된 응답에 종료·안전 검사를 적용한 뒤 Chat 또는 Responses 이벤트로 반환합니다. 따라서 클라이언트가 streaming을 켰다는 사실만으로 첫 실제 본문 토큰 지연까지 줄어든다고 가정하면 안 됩니다. [서버 SSE](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/server.py#L650), [Chat stream 렌더러](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/dialects/chat.py#L143)

### 8. 로그와 `jah fit`은 무엇을 학습하나요?

기본 로그 `steps.jsonl`에는 실제 tier, 사유, 확률, 호출별 비용·지연·가격 확인 여부가 남고, `decisions.jsonl`에는 point별 질문·선택·행동·LLM의 선택 라벨이 남습니다. 일반 경로는 프롬프트와 완료 본문 전체를 기록하지 않습니다. 그러나 오류 문자열도 일부 저장하고, **`log_states: true`는 과제와 최근 행동·결과를 포함한 상태 텍스트를 별도 저장**하므로 모든 운영 로그가 민감한 내용을 절대 담지 않는다고 단정할 수 없습니다. [로그 구성](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/server.py#L567), [선택적 상태 로그](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/server.py#L176)

`jah fit`은 모델 가중치를 학습하지 않습니다. 현재 프록시에서 자동 조정 대상은 `tool_select`와 `stop` 두 point입니다. 결정 모델의 영향을 받지 않은 LLM 선택을 라벨로 삼고, 기본적으로 최소 30개 선택에서 **LLM과의 일치율에 대한 단측 Wilson 하한이 95% 이상**이 되는 가장 작은 임계값을 찾습니다(`z=1.645`). 도구가 사실상 하나뿐인 요청은 도구 선택 능력을 측정하기 어려워 제외합니다. 조건을 만족하는 임계값이 없으면 해당 결정을 계속 LLM에 남기도록 출력합니다.

반면 routing·reflection·action에는 “다른 경로를 탔으면 어땠을까”라는 반사실적 라벨이 없습니다. 그래서 `jah fit`은 빈도·비용 등을 설명하며 그 임계값을 자동으로 맞추지 않습니다. LLM과의 일치는 최종 과제 성공과도 다릅니다. 이 범위를 알아야 README의 “임계값을 fit한다”를 전체 라우터의 자동 최적화로 확대하지 않게 됩니다. [fit의 계약](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/fit.py#L1), [대상·필터·선택](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/fit.py#L96), [코드가 남기는 안내](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/fit.py#L204)

## 문서에 있는 사용 순서

분석 커밋의 Quickstart는 다음 명령을 제시합니다. 아래는 문서 인용이며 이 리뷰에서 실행해 검증한 결과가 아닙니다. 프록시 설치와 별개로 실제 공급자 API를 호출할 수 있는 키와 접근 권한이 필요합니다.

```bash
git clone https://github.com/JevAgentHarness/JevAgentHarness.git && cd JevAgentHarness
pip install -e .
export GEMINI_API_KEY=...              # the LLM tiers (Gemini by default; any OpenAI-compatible API works)
export OPENROUTER_API_KEY=...          # the decision model (Jev on OpenRouter); or use {type: rules}, no key
jah init                               # optional: writes ~/.jah/config.yaml (commented) to edit
jah serve                              # http://127.0.0.1:8787/v1, uses ~/.jah/config.yaml if it exists
```

[명령 출처](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/README.md#L133). `jah init`은 기본 설정 파일을 쓰며, `jah serve -c <file>`이나 `--set`으로 설정을 바꿀 수 있습니다. 문서의 clone 명령은 당시 기본 브랜치를 받습니다. 본문 분석은 위에 명시한 고정 SHA 기준입니다. CLI는 필요한 LLM 공급자 환경 변수가 없으면 시작을 거부하지만, 결정 모델 요청 실패는 요청 처리 중 기본 strong 경로로 대체됩니다. [CLI 설정·키 검사](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/cli.py#L37)

이후 기존 하네스의 모델 API 주소를 `http://127.0.0.1:8787/v1`, 모델명을 `jah-auto`로 정합니다. 공급자 키는 프록시가 읽고 클라이언트에는 더미 키를 사용할 수 있습니다. README는 Codex의 Responses 설정, pi·DeepSeek Harness·mini-swe-agent와 OpenAI SDK 예제를 제공하며, `jah setup <harness>`는 그 설정 안내를 출력합니다. Codex는 `jah-*` 모델 이름에 전체 도구를 제공하도록 별도 모델 카탈로그 설정을 설명하고, hosted web search는 끄도록 예시를 제시합니다. 이 문서는 **Claude Code 연동을 검증한 안내가 아니므로**, 일반적인 호환성만으로 지원 클라이언트를 추가하지 않았습니다. [연결 예제](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/README.md#L170), [setup 출력 경로](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/cli.py#L79)

관찰용 설정과 fit 명령도 문서에 있습니다.

```bash
jah serve --preset shadow       # every point logs its answer next to what the agent did; nothing changes
jah fit ~/.jah/logs             # fit each point's threshold on those logs and print a config snippet
```

[명령 출처](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/README.md#L280). 여기서 주석보다 실제 preset 구성을 함께 봐야 합니다. **`--preset shadow`만으로 모든 요청이 strong 고정이 되는 것은 아닙니다.** 이 preset은 추가 네 point를 shadow로 두지만 routing은 기본 cascade를 유지합니다. routing 자체도 shadow로 바꾸면 strong-only 호출을 하며 라우팅 질문을 기록할 수 있습니다. 또한 fit 결과는 설정 조각을 출력할 뿐, 실행 중 설정을 자동으로 변경하지 않습니다. [문서의 보충 설명](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/docs/modes.md#L43), [preset과 적용 순서](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/points.py#L61)

## 공개 결과는 조건과 함께 읽어야 합니다

루트 README의 최신 표는 **Terminal-Bench 2.0 고정 test 74과제, 하네스별 한 번의 실행**, strong Gemini 4 Argon/high, fast Gemini 3.5 Flash-Lite/low, 결정 모델 Jev, `tau=0.75` 조건입니다. LLM·결정 모델 호출 비용과 task wall-clock을 보고합니다. 아래는 저장소가 보고한 결과이며 독립 재현 값은 아닙니다.

| 하네스 | 성공률 strong → routed | 성공률 차이 95% CI(%p) | 과제당 비용 | 과제당 시간 |
|---|---|---|---|---|
| mini-swe-agent | 66.2 → 63.5% | −2.7 [−14.9, +8.1] | 0.91 → 0.33달러 | 13.7 → 7.9분 |
| pi | 52.7 → 56.8% | +4.1 [−6.8, +14.9] | 0.62 → 0.42달러 | 11.3 → 10.8분 |
| DeepSeek Harness | 66.2 → 66.2% | 0.0 [−8.1, +8.1] | 0.94 → 0.68달러 | 13.4 → 11.4분 |

[결과표](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/README.md#L79), [정밀 집계](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/bench/results/test_flash_lite.md#L1). 신뢰구간은 과제를 쌍으로 맞춘 bootstrap 결과입니다. 성공률 차이를 통계적으로 입증된 개선이나 3%p 비열등성 보장으로 해석하지 않습니다. 사전 기준인 성공률 하락 3%p 이내·비용 40% 이상 감소·시간 단축은 mini-swe-agent만 세 조건을 모두 충족합니다. pi와 DeepSeek Harness는 비용 감소가 각각 약 31%, 28%로 목표보다 작습니다.

같은 표의 Terminus-2는 baseline 74개 중 53개가 timeout에 걸렸으며, 저자도 그 행을 결론 불충분으로 표시합니다. Gemini 3.8 Flash를 fast로 쓴 별도 설정은 비용 감소가 7–13%에 머물고, Codex/OpenAI 모델 조합의 20과제 소규모 확인은 성공률 85→85%, 비용 6.5% 감소지만 더 느렸습니다. 작은 모델의 가격 차이, 추가 단계, 캐시 적중과 결정 모델 호출까지 함께 계산해야 한다는 사례입니다. 이를 “모든 하네스에서 같은 결과를 더 싸게”라는 보편 보장으로 정리할 수 없습니다. [대안 설정과 해석](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/README.md#L106)

프로토콜도 시점별 변경을 공개합니다. Flash-Lite 행은 개발 실험 후 새로 등록한 별도 test 행이고, 기준선은 같은 strong 모델·하네스·과제의 전날 실행을 사용합니다. 이 경위를 숨긴 채 모든 행이 처음부터 완전히 동시 실행된 단일 실험이라고 부르지 않았습니다. 추가 decision point mode의 결과는 15개 개발 과제에만 해당하며 같은 test 성과로 합치지 않습니다. [사전 기준과 변경 기록](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/bench/PROTOCOL.md#L33)

## 모델과 운영에서 주의할 경계

**Jev와 AgentDecision 모델을 구별해야 합니다.** 기본 Jev는 외부 서비스에서 확률을 받아오는 backend입니다. README는 AgentDecision-4B를 Qwen3-4B 기반 LoRA adapter로, v1을 등록된 Stage-2 전 고정 checkpoint로 구분합니다. 연구 모델은 DecisionGym 고객 서비스 상태에서 훈련됐으며 코딩 에이전트에 맞춰 훈련된 모델은 아니라고 적습니다. 프록시를 설치하면 이 가중치가 자동으로 내려받아지거나 재학습되는 것은 아닙니다. 모델·데이터 카드를 여기서 독립 감사한 것도 아닙니다. [모델·데이터 목록과 사용 범위](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/README.md#L393)

**코드 라이선스와 모델 라이선스는 다릅니다.** 저장소 코드는 MIT이지만 README는 AgentDecision 모델과 훈련 데이터 등에 CC BY-NC 4.0을, AgentDecisionBench에는 CC BY 4.0을 기재합니다. 코드의 MIT 표시를 모델·데이터 전체의 같은 이용 조건으로 확장하지 않습니다. [코드 LICENSE](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/LICENSE#L1), [자료별 표기](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/README.md#L398)

**로컬 프록시는 외부 전송을 없애지 않습니다.** 기본 상태 요약은 결정 모델 공급자에게, 실제 모델 요청은 선택한 LLM 공급자에게 갑니다. self-hosted 결정 모델을 쓰더라도 LLM tier가 원격이면 그 경계는 남습니다. HTTP 서버는 기본 localhost에 묶이지만 입력 더미 키를 검증하는 인증 middleware가 보이지 않습니다. 문서도 인증 부재와 신뢰할 네트워크 조건을 명시합니다. 이는 action guard의 기능과도 다른 운영 경계입니다. [설정 문서](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/docs/configuration.md#L73), [HTTP app 구성](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/server.py#L701)

**비용 기록과 예산 상한은 측정 범위가 있습니다.** 가격표는 2026-10-14에 읽은 공급자 단가를 코드에 담으며 실제 현재 가격을 자동 조회하지 않습니다. 공급자가 비용을 보고하면 우선하고, 모르는 모델은 `priced: false`와 비용 0으로 표시합니다. 따라서 0은 무료를 뜻하지 않습니다. `budget_usd`는 기록된 지출이 한도에 이르렀을 때 새 세션의 첫 단계 요청을 거부하는 장치입니다. 진행 중 세션의 모든 다음 호출을 중단하는 hard cap이나 최종 청구액 보장은 아닙니다. `jah report`의 LLM 처리 시간 합계도 벤치마크가 보고한 전체 에이전트 wall-clock과 구분해야 합니다. [가격 계산](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/prices.py#L15), [예산 검사](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/server.py#L154), [보고서 집계](https://github.com/JevAgentHarness/JevAgentHarness/blob/f2932199e1ef1d9f089b51d39430c87be0f560b5/src/jevagentharness/report.py#L25)

## 실행 전략을 바꾸기 전에 측정할 자리를 만듭니다

이 저장소의 학습 가치는 작은 모델을 한 번 연결하는 데 그치지 않습니다. **요청 정규화 → 상태 관찰 → tier 선택 → 응답 재검사 → 로그와 임계값 검토**를 명시적인 경계로 나눈 점입니다. routine/hard 라우팅과 도구 선택 confidence는 서로 다른 질문이고, LLM과의 일치율과 실제 과제 성공도 서로 다른 측정 대상입니다. 원래 하네스가 실행과 도구 권한을 유지하는 구조에서는 프록시가 바꿀 수 있는 것과 바꿀 수 없는 것을 함께 읽어야 합니다.

이 글에서는 루트 프록시의 핵심 요청·분기·반환·로그 경로를 추적했습니다. `research/`의 전체 학습·실험 코드, 공개 모델 가중치와 외부 모델 카드의 독립 검증, 모든 Gemini 캐시·서명·OpenAI reasoning item의 예외 분기, 전체 테스트와 하네스별 실제 호환성은 분석·재현하지 않았습니다. 이 범위에서 확인한 결과는 실행 성공 인증이나 포괄적인 보안 감사가 아니라 고정 커밋에 대한 정적 코드 리뷰입니다.
