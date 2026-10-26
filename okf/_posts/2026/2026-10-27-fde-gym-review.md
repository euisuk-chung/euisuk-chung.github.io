---
type: "Repo Review"
title: "[Repo Review] FDE Gym — 코드를 넘어 고객 문제의 해결을 평가하는 실행 환경"
description: "FDE Gym의 사례 버전 관리와 웹·runner·Python 하네스 흐름을 추적하고, 고객 대화·코딩 에이전트·운영 재생·개입 비용이 최종 평가로 이어지는 구조를 분석합니다."
date: "2026-10-27"
tags:
  - "Repo Review"
  - "AI Agent"
  - "Python"
  - "Tools"
resource: "https://github.com/deeplethe/fde-gym/commit/1d9ed027af7c8312bacb1abad1467c87a91c004b"
generated:
  by: "process:blog-review"
  at: "2026-10-27T06:09:08+09:00"
sources:
  - id: "deeplethe/fde-gym@1d9ed027af7c8312bacb1abad1467c87a91c004b"
    resource: "https://github.com/deeplethe/fde-gym/commit/1d9ed027af7c8312bacb1abad1467c87a91c004b"
    title: "FDE Gym"
status: "stable"
year: "2026"
analyzed_at: "2026-10-27T06:09:08+09:00"
source_id: "deeplethe/fde-gym"
source_revision: "1d9ed027af7c8312bacb1abad1467c87a91c004b"
source_title: "FDE Gym"
source_type: "repo"
source_url: "https://github.com/deeplethe/fde-gym/commit/1d9ed027af7c8312bacb1abad1467c87a91c004b"
visual_sources:
  - path: "img/reviews/2026/fde-gym-review/platform-boundaries.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/docker-compose.yml#L20-L136"
    caption: "리뷰어 작성, 분석 커밋 기준. 웹·저장소·runner·모델 relay 경계를 요약한 도식입니다."
    code_sources:
      - "https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/runners.ts#L1-L14"
      - "https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/cases-store.ts#L1-L19"
      - "https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/agent.ts#L327-L382"
  - path: "img/reviews/2026/fde-gym-review/run-lifecycle.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/session.ts#L65-L86"
    caption: "리뷰어 작성, 분석 커밋 기준. 사례의 고정 버전에서 workspace·상호작용·제출·채점으로 이어지는 흐름입니다."
    code_sources:
      - "https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/harness.ts#L147-L171"
      - "https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/harness/run.py#L494-L584"
      - "https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/session.ts#L418-L463"
---

## 코드가 맞는 것과 고객 문제가 해결되는 것은 다릅니다

고객이 “자동 분류기를 만들어 주세요”라고 요청했다고 가정해 보겠습니다. 분류 정확도를 높인 코드가 있어도, 실제 현장에서 사람이 반드시 확인해야 하는 요청을 자동 처리하거나 기존 서비스의 호출 지점에 연결하지 않았다면 납품은 성공하지 못합니다. 요구사항을 알아내는 일, 바꿀 시스템의 범위를 정하는 일, 운영 결과에 책임지는 일이 함께 필요합니다.

**FDE Gym은 고객의 불완전한 요청, 수정 가능한 시스템, 질문할 이해관계자, 숨겨진 운영 데이터와 채점기를 묶은 실습·평가 플랫폼입니다.** FDE는 Forward-Deployed Engineer의 약자로, 고객 현장에 들어가 문제를 파악하고 실제 작동하는 해결책을 전달하는 엔지니어를 뜻합니다. 이 레포는 사람이 코딩 에이전트를 지휘하며 문제를 풀 수 있는 웹 화면과, 같은 사례를 명령행에서 다루는 Python 실행 하네스를 제공합니다. 하네스는 작업 환경을 만들고 도구 호출을 연결하며 최종 결과를 채점하는 프로그램입니다. [README의 정의와 비교](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/README.md#L23-L57)

분석 대상은 `deeplethe/fde-gym`의 커밋 `1d9ed027af7c8312bacb1abad1467c87a91c004b`입니다. 문서와 코드를 정적으로 읽었으며, 레포 설치·서비스 기동·사례 다운로드·모델 호출·벤치마크 재현은 하지 않았습니다. 따라서 아래의 사용법은 해당 커밋 문서에 적힌 절차이고, 실행 성공을 검증한 기록은 아닙니다.

## 무엇이 공개되어 있는가

관련 논문은 20개 고객 시나리오에서 만든 95개 과제를 설명합니다. 이는 논문 평가의 규모입니다. 현재 GitHub 레포에 그 95개 과제와 숨겨진 정답이 모두 들어 있는 것은 아닙니다. README는 사례를 별도 Hugging Face 데이터셋으로 배포하며, 공개 예제는 세 개이고 전체 20개 시나리오는 접근 요청이 필요하다고 안내합니다. 이 글은 플랫폼의 코드 리뷰이며 논문의 모델 성능을 재현하거나 전체 사례의 채점 품질을 검증하지 않습니다. [논문 초록](https://arxiv.org/abs/2610.22350v1), [레포의 Cases 설명](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/README.md#L96-L107)

플랫폼이 제공하는 작업을 구분하면 다음과 같습니다.

| 구성 | 독자가 접하는 기능 | 구현상 의미 |
|---|---|---|
| 사례 목록 | 분야·난이도·해결 여부로 탐색 | 공개 가능한 목록 정보를 PostgreSQL에서 읽습니다. |
| 작업 화면 | 파일, 터미널, 코딩 에이전트, 고객 측 인물과 대화 | 한 번의 실습을 `run`으로 묶고 실행 위치를 runner에 고정합니다. |
| 제출과 결과 | 점수·사건·대화 기록·변경점 확인 | 제출한 시스템을 복사해 숨겨진 입력으로 재생하고 결과를 보존합니다. |
| 운영 화면 | 사례·사용자·runner·모델·메일 관리 | 콘텐츠 저장소와 실행 기계를 웹 서비스에서 관리합니다. |
| Python 하네스 | 사례 생성·상호작용·채점 | 웹과 명령행이 같은 `new`, `serve`, `grade` 경로를 사용합니다. |

[README 기능표](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/README.md#L57-L67), [웹 API 진입점](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/index.ts#L77-L125), [하네스 명령 설명](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/harness/README.md#L21-L40)

여기서 **시나리오**, **숨겨진 변형**, **배포 버전**은 다른 개념입니다. 시나리오는 하나의 고객 세계를 담은 폴더입니다. `variants.json`은 같은 요청 안에서 실제 제약이나 정답이 다른 변형을 정의합니다. 브라우저에는 내부 변형 키 대신 사례 번호만 보입니다. 한편 `bundle_sha`는 사례 파일의 내용이 바뀌었을 때 사용하는 아카이브 버전입니다. “사례 #2”와 “사례 파일의 새 SHA”를 같은 버전으로 이해하면 채점의 기준을 혼동하게 됩니다. [Catalog의 변형 표현](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/catalog.ts#L36-L89), [아카이브 해시](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/cases-store.ts#L112-L116)

## 아키텍처: 웹 서비스와 실행 기계를 나눕니다

![웹 서비스가 PostgreSQL과 S3를 관리하고 별도 runner가 작업 공간과 하네스를 실행하며 모델 요청은 사이트의 relay를 거치는 구조]({{ '/img/reviews/2026/fde-gym-review/platform-boundaries.svg' | relative_url }})

*리뷰어 작성, 분석 커밋 기준. 실선은 주요 요청·실행 경로입니다. 저장과 실행의 책임을 구분한 도식이며 서비스 실행을 재현한 결과는 아닙니다. [Compose](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/docker-compose.yml#L20-L136), [runner 연결](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/runners.ts#L1-L14), [모델 relay](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/agent.ts#L327-L382)*

브라우저 UI는 React이고 서버는 Hono 기반 TypeScript입니다. 서버는 사례 목록·실습 상태·인증·에이전트 요청을 제공하며, 사례 안의 Python 코드는 하네스가 실행합니다. `app/package.json`에서 React·Hono·PostgreSQL 클라이언트·S3 SDK와 코딩 에이전트 pi 의존성을 확인할 수 있습니다. “Python 표준 라이브러리만 필요하다”는 문구는 Python 하네스에 대한 설명이지 전체 웹 플랫폼에 외부 의존성이 없다는 뜻이 아닙니다. [패키지 매니페스트](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/package.json#L1-L73), [하네스 설명](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/harness/README.md#L1-L23)

| 파일·디렉터리 | 핵심 책임 |
|---|---|
| `app/web/` | 사례 선택과 작업·결과 화면 |
| `app/server/index.ts`, `session.ts` | API 요청, 소유권 확인, 실습 상태 전이 |
| `app/server/runners.ts`, `runner.ts` | 사이트 측 RPC와 runner 측 실행 연결 |
| `app/server/cases-store.ts`, `case-cache.ts` | 사례 아카이브의 내용 해시·버전 저장·로컬 전개 |
| `app/server/harness.ts` | Python `new/serve/grade`, 파일·터미널 제어 |
| `app/server/agent.ts`, `pi.ts` | 코딩 에이전트의 턴·기록·토큰·모델 relay |
| `harness/run.py`, `npc_server.py` | 사례의 세계 구성·고객 대화·운영 재생·점수 계산 |
| `docs/self-hosting.md`, Compose 파일 | 배포 형태와 격리 경계의 운영 계약 |

Compose 기본 구성은 사이트, runner, PostgreSQL, S3 호환 객체 저장소의 네 서비스입니다. PostgreSQL에는 실습과 대화 같은 구조화된 기록이 들어가고, S3에는 사례 파일 아카이브가 들어갑니다. runner에는 workspace와 실행 프로세스가 있습니다. 이 셋은 서로 대체 가능한 저장 방식이 아니라 서로 다른 데이터를 맡습니다. [Compose](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/docker-compose.yml#L20-L136), [사례 저장 구조](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/cases-store.ts#L1-L19)

## 작동 원리: 사례 선택에서 최종 점수까지

### 1. 공개 목록에는 정답 대신 고객의 요청만 올립니다

사례를 가져올 때 `readListing()`은 `briefs/L3.md`의 요청과 `npcs.json`의 이름·직책·소개 등을 목록 정보로 만듭니다. `truth.json`이나 `NOTES.md`의 답을 목록으로 보내지 않습니다. `engagement.json`도 읽지만, 목록에 노출하는 것은 LLM이나 고객 서비스의 유무 등 기능 정보입니다. 서버의 `BRIEF` 상수는 `L3`이므로 웹 실습은 고객이 말한 요청 수준으로 시작합니다. 명령행에서 다른 설명 수준을 고르는 기능과 구분해야 합니다. [목록 생성](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/cases-store.ts#L68-L91), [L3 상수](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/catalog.ts#L11-L18)

가져오기는 파일 경로와 내용을 정렬한 뒤 SHA-256을 계산하고 `cases/<id>/<sha256>.tar.gz`에 저장합니다. 아카이브 업로드를 먼저 끝낸 다음 DB가 그것을 가리키도록 갱신합니다. 같은 내용은 `unchanged`이고 바뀐 내용은 새 아카이브가 되며 이전 아카이브는 남습니다. 이는 진행 중 실습의 기준 파일을 보존하는 설계입니다. 단, 일부 사례가 함께 사용하는 별도 `data/` 아카이브는 공용 해시로 관리하므로, 사례의 `bundle_sha` 하나가 주변의 모든 데이터까지 고정한다고 확대 해석하지 않아야 합니다. [내용 해시와 가져오기](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/cases-store.ts#L112-L176), [공용 데이터 캐시](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/case-cache.ts#L50-L95)

### 2. Begin은 실습 상태와 실행 위치를 함께 만듭니다

`POST /api/sessions`는 사용자 또는 허용된 익명 사용자, 사례 공개 상태, 선택한 변형을 확인합니다. 이어 `startSession()`이 runner를 선택하고 `running` 상태, 사용자 ID, 사례 ID, `bundle_sha`, runner 이름을 DB에 기록합니다. 원격 runner용 모델 relay 토큰도 이 단계에서 준비합니다. 그 후 `runner.createRun()`을 호출하며, 생성에 실패하면 막 넣은 DB 행을 지웁니다. [API 시작 경로](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/index.ts#L110-L125), [실습 생성](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/session.ts#L65-L86)

runner 선택은 단순 무작위가 아닙니다. 연결된 기계 중 비활성화·배수 상태가 아니며 수용량이 남은 기계를 찾고, 현재 작업 수를 수용량으로 나눈 비율이 작은 순서로 고릅니다. 원격 기계에 자리가 없으면 설정에 따라 사이트 내부의 `localRunner`를 사용할 수 있습니다. Compose는 `FDEGYM_LOCAL_RUNNER=0`으로 이 대체 경로를 끕니다. 실습은 처음 배정된 runner에 남으므로 그 기계가 끊겼다고 다른 기계로 자동 이동하지 않습니다. [선택과 재조회](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/runners.ts#L128-L155), [Compose의 로컬 실행 비활성화](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/docker-compose.yml#L74-L81)

### 3. runner는 사이트에 연결하고 고정된 사례 파일을 가져옵니다

원격 runner가 먼저 사이트의 `/api/runner/connect`로 WebSocket을 엽니다. 사이트가 각 runner로 임의의 새 TCP 연결을 여는 구조가 아니므로, runner가 NAT나 방화벽 뒤에 있을 수 있습니다. 사이트는 연결 위로 메서드와 요청 ID를 보내고, runner는 결과·오류·출력 이벤트를 같은 연결로 돌려줍니다. [프로토콜과 RPC](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/runners.ts#L1-L14), [요청 ID 처리](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/runners.ts#L47-L105), [runner의 응답 분기](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/runner.ts#L79-L141)

사례 파일은 runner가 사이트의 사례 API에서 받습니다. `localCases(id, sha)`는 지정 SHA의 아카이브를 임시 디렉터리에 풀고 사례 파일이 있는지 확인한 뒤 캐시 위치로 옮깁니다. 동일 키의 동시 요청은 하나의 진행 중 Promise를 기다립니다. 이 이름에서 `local`은 “현재 실행 기계의 로컬 캐시”를 뜻하며, 사이트 프로세스에서만 동작한다는 뜻이 아닙니다. [runner 사례 소스](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/runner.ts#L55-L68), [캐시 전개](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/case-cache.ts#L70-L95)

### 4. `new`가 고객의 세계와 작업 공간을 만듭니다

TypeScript의 `createRun()`은 `run.py new`를 자식 프로세스로 호출합니다. Python의 `materialise()`는 해당 사례의 `build_world.py`를 읽어 세계를 만들고, 선택한 설명 수준과 규칙을 `TASK.md`에 씁니다. 질문용 `bin/ask`, 필요하면 시험 운영용 `bin/pilot`, 사례가 요구하는 LLM gateway와 고객 서비스의 연결 정보도 배치합니다. 내부 변형 값은 요청문과 고객 스크립트 등에 반영됩니다. [TypeScript 호출부](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/harness.ts#L147-L171), [Python workspace 생성](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/harness/run.py#L348-L388)

작업자는 주로 `system/`의 실제 시스템과 `deliverables/`의 인계 문서를 고칩니다. `TASK.md`, `docs/`, `data/`, `bin/`은 고객이 제공한 읽기용 자료입니다. 파일 API는 이 경로의 변경을 거부하고, 컨테이너에서는 소유권과 권한으로 보호합니다. 처음 만들어진 workspace의 별도 사본도 남겨 이후 Changes 화면의 기준으로 씁니다. [보호 경로와 소유권](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/harness.ts#L90-L124), [초기 사본](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/harness.ts#L156-L170), [파일 경로 검사](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/harness.ts#L276-L340)

### 5. `serve`가 질문·기다림·시험 운영을 연결합니다

작업 중에는 `run.py serve`가 고객 측 인물을 담당하는 NPC 서버와 필요한 서비스를 엽니다. 웹의 질문 버튼도, workspace의 `bin/ask`도 같은 고객 서버에 연결됩니다. 서버는 별도 프로세스로 시작하며 포트 상태를 확인해 이미 살아 있으면 재사용합니다. 사이트 재시작 때마다 고객의 질문 횟수나 시간이 초기화되는 일을 피하려는 구조입니다. 이는 모든 프로세스 상태가 DB에 영구 저장된다는 뜻은 아닙니다. [서비스 기동](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/harness.ts#L173-L233), [하네스 serve](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/harness/run.py#L408-L450)

NPC는 Non-Player Character, 즉 시뮬레이션에서 사람의 역할을 하는 구성요소입니다. 여기서는 **LLM이 매번 자유롭게 답변을 만들어 내는 고객**으로 이해하면 틀립니다. 답변 내용은 `npcs.json`의 스크립트에 정해져 있습니다. LLM matcher는 질문이 어떤 주제에 해당하는지, 근거 제시 같은 gate 조건을 만족했는지를 판정합니다. 선택된 주제의 정해진 답과 사실 ID가 반환됩니다. regex matcher 경로도 있으며, LLM 호출 오류 때 일부 경로는 regex로 대체합니다. [NPC 설계](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/harness/npc_server.py#L1-L10), [주제 판정](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/harness/npc_server.py#L294-L337), [스크립트 답변 선택](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/harness/npc_server.py#L355-L415)

그래서 대화에는 내용 외에 상태가 생깁니다. 이미 얻은 사실, 질문한 횟수, 아직 기다려야 하는 일정, 연락할 수 없게 된 인물 등이 다음 답에 영향을 줍니다. `requires_facts`가 충족되어야 알려주는 정보도 있고, gate를 통과해야 공개되는 답도 있습니다. 질문·기다림·시험 운영의 비용은 로그에 누적되어 최종 점수에서 빠집니다. 질문 횟수나 비용이 UI에 모두 공개되는 것은 사례 설정에 따라 다릅니다. [질문 횟수·비용·상태](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/harness/npc_server.py#L117-L203), [기다림과 시험 운영](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/harness/npc_server.py#L236-L284)

웹 서버는 고객의 실제 답변을 `messages` 테이블에 보존합니다. Python 질문 로그에는 공개한 사실 ID와 비용 등이 기록되지만 답변 문장 자체는 기록하지 않기 때문에, 두 기록은 목적이 다릅니다. 전자는 작업자가 대화를 다시 보는 자료이고 후자는 채점 시 사실 습득과 비용을 계산하는 근거입니다. [웹 대화 저장](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/session.ts#L302-L315), [질문 API](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/session.ts#L342-L376), [사실·비용 집계](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/harness/run.py#L464-L482)

### 6. 코딩 에이전트는 pi이고 모델 API 키는 사이트에 남습니다

작업자가 에이전트에 보낸 한 메시지는 runner 위의 pi 실행 한 번으로 연결됩니다. pi는 workspace에서 파일을 읽고, Bash 명령을 실행하고, 파일을 편집·작성합니다. JSON 이벤트는 사이트가 웹 화면용 대화와 도구 기록으로 저장하고 실시간으로 전달합니다. pi 자체의 세션 파일은 workspace 옆의 agent 디렉터리에 남아 다음 메시지에서 `--continue`로 이어집니다. 웹 화면의 DB 기록과 모델이 이어 읽는 세션 파일도 별개입니다. [pi 실행 인자와 환경](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/pi.ts#L79-L155), [사이트의 턴 생성](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/agent.ts#L262-L291)

pi는 공급자의 원래 API 키를 받지 않습니다. 사이트가 한 실습의 한 턴에 사용할 토큰을 발급하고, pi는 `/api/agent/v1/chat/completions`로 요청합니다. 사이트는 토큰을 현재 턴과 대조하고 관리자 설정의 모델·엔드포인트·키로 공급자 요청을 보냅니다. 사용량은 `agent_usage`에 누적합니다. 여기서 비용 상한은 요청 전의 누적 비용 검사와 응답의 `usage.cost` 기록에 의존하므로, 공급자와 무관하게 정확한 금액을 사전 예약하는 결제 한도로 해석하면 안 됩니다. [토큰 생성](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/agent.ts#L262-L281), [relay·비용 기록](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/agent.ts#L320-L382)

설계상 고객에게 질문할지, 시험 운영을 할지는 학습자가 판단합니다. 에이전트의 system prompt가 그 역할을 설명하고 별도 guard가 `bin/ask`나 `bin/pilot`에 해당하는 Bash 호출을 막습니다. 이는 특정 명령 패턴과 역할을 통제하는 구현입니다. 모든 가능한 간접 접근을 막았다는 보안 검증 결과로 확대해서 설명하지 않습니다. [역할 프롬프트](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/agent.ts#L32-L60), [guard](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/pi.ts#L60-L71)

원격 연결이 끊겨도 pi가 runner에 남아 실행 중이면, 사이트는 기록된 이벤트 순번 이후를 다시 읽어 대화를 이어 붙일 수 있습니다. 반대로 runner 자체의 메모리와 프로세스가 사라진 상황까지 자동 복구하는 것은 아닙니다. [턴 재연결](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/agent.ts#L294-L318), [runner 내 이벤트 보존](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/pi.ts#L104-L121)

### 7. Submit은 수정 단계를 닫고 숨겨진 데이터로 다시 실행합니다

![고정 사례 버전에서 작업 공간을 만들고 고객 대화와 에이전트 수정을 거친 뒤 제출하면 복사본에서 숨겨진 채점과 비용 차감이 이뤄지는 흐름]({{ '/img/reviews/2026/fde-gym-review/run-lifecycle.svg' | relative_url }})

*리뷰어 작성, 분석 커밋 기준. “원본 보존”은 채점이 작업 사본을 사용한다는 의미입니다. 최종 점수의 세부 입력은 사례별 grader가 제공합니다. [실습 생성](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/session.ts#L65-L86), [제출](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/session.ts#L418-L463), [재생·점수 계산](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/harness/run.py#L494-L584)*

`submit()`은 열린 실습인지 확인하고 에이전트 또는 터미널 명령이 실행 중이면 거부합니다. 이어 고객 서비스를 멈추고 상태를 `grading`으로 바꾼 뒤 비동기 채점을 시작합니다. 이후 파일 수정 등의 작업은 열린 실습에만 허용됩니다. 성공하면 `graded`, 오류면 `failed`이며, 실패한 채점을 다시 요청하는 경로는 별도로 있습니다. “실습 한 번의 제출”과 “채점 실패 후 재시도”를 구분하는 상태 관리입니다. [제출과 실패 재채점](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/session.ts#L418-L463)

실제 채점은 `run.py grade`로 내려갑니다. `grade_workspace()`가 작업 공간을 임시 위치로 복사하고 사례의 `truth.json`, `grader.py`와 숨겨진 운영 입력을 사용합니다. 사례에 LLM이나 고객 서비스가 있으면 채점용 자원을 새로 연결합니다. 변경된 `system/`이 실제로 쓰이도록 만든 평가이므로, 답변 텍스트가 그럴듯한지만 점수화하는 방식과 다릅니다. 다만 각 사례의 숨겨진 입력과 `grader.py`는 별도 데이터셋에 있으므로 이 레포만으로 모든 사례의 채점을 확인할 수는 없습니다. [채점 하네스 호출](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/harness.ts#L235-L251), [사례별 grader 연결](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/harness/run.py#L494-L551)

TypeScript 서버는 반환된 `result.json`의 `uplift`, `uplift_net`과 결과 정보를 DB에 저장합니다. 화면은 DB의 상태를 확인하므로 채점 프로세스가 곧바로 HTTP 응답 하나를 끝낼 때까지 브라우저를 붙잡아 두지 않습니다. [결과 저장](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/session.ts#L453-L462), [서버 재시작 시 채점 상태 처리](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/index.ts#L369-L370)

### 8. 점수는 정확도 하나가 아니라 개선량과 개입 비용입니다

핵심 점수 계산은 아래 코드에 있습니다. 앞부분은 그대로 인용한 것이며, `kpi`가 클수록 항상 좋은지 여부는 사례가 정한 baseline과 oracle의 방향에 반영됩니다.

```python
    span = out["kpi_oracle"] - out["kpi_baseline"]
    out["uplift"] = round((out["kpi"] - out["kpi_baseline"]) / span, 4) if span else 0.0
```

[원문 코드: `run.py` 558–559행](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/harness/run.py#L558-L559)

`kpi_baseline`은 바꾸지 않은 시스템의 기준값이고, `kpi_oracle`은 참조 해결책의 기준값입니다. 두 값 사이에서 납품 시스템이 어디에 놓이는지 정규화한 것이 `uplift`입니다. 분모가 0이면 코드는 0으로 처리합니다. 높은 accuracy나 낮은 비용처럼 성격이 다른 고객 지표를 같은 척도에서 읽도록 만드는 장치입니다.

그 다음 처리 순서도 중요합니다.

| 필드 | 코드가 하는 일 | 읽을 때의 주의점 |
|---|---|---|
| `uplift` | 기준 대비 개선량 계산 후, 사건이 있으면 최대 0으로 제한 | 사건 전의 개선량과 사건 처리 후 값을 구분해야 합니다. |
| `uplift_bounded` | 사건 처리 전에 계산한 개선량의 하한을 −1로 제한 | 최종 웹 점수와 같지 않으며, 이 하한이 모든 필드에 적용되는 것도 아닙니다. |
| `discovery.contact_cost` | 질문·기다림·시험 운영 로그의 비용 합산 | 모델 API 비용과 다른 고객 측 개입 비용입니다. |
| `uplift_net` | 사건 처리 후 `uplift`에서 고객 측 개입 비용 차감 | 사이트가 사용하는 최종 실습 점수입니다. |

[처리 순서](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/harness/run.py#L558-L571), [사실 습득·비용 집계](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/harness/run.py#L464-L482)

사이트는 `uplift_net`이 0.8 이상인 채점 완료 실행을 해결한 사례로 계산합니다. 화면의 100점 환산은 소수점을 반올림하지 않고 버립니다. 예를 들어 문서가 설명하는 79.6점은 화면에서 79점이며 합격이 아닙니다. 이 표시는 점수 계산을 다시 하는 것이 아니라, 내부의 소수 점수를 사람이 읽는 단위로 바꾸는 과정입니다. [해결 기준](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/standings.ts#L15-L48), [화면 점수 변환](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/web/lib/score.ts#L1-L18)

## 문서 기반 시작 방법

다음은 이 커밋 README의 Quick start 명령을 그대로 인용한 것입니다. Docker, Python 3.9 이상, 고객 NPC용 OpenRouter 키가 필요하다고 안내합니다. 실제 키는 명령의 예시 문자열을 복사하는 대신 본인의 키 파일로 준비해야 합니다. 이 리뷰에서는 명령을 실행하지 않았습니다.

```bash
git clone https://github.com/deeplethe/fde-gym.git && cd fde-gym
mkdir -p ~/.fdegym && echo "sk-or-..." > ~/.fdegym/openrouter_key
python3 scripts/fetch_cases.py        # the three open cases, into cases/
docker compose up --build             # http://127.0.0.1:8787
```

[README 원문](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/README.md#L69-L82)

시작하면 첫 가입 계정이 관리자가 됩니다. 사례 선택 후 Begin으로 실습을 만들고, 자료를 읽고, 필요한 사람에게 질문하고, 코딩 에이전트에 변경을 지시합니다. 마지막에 인계하면 숨겨진 입력을 이용한 채점 결과를 확인하는 흐름입니다. 코딩 에이전트 모델은 관리자 화면에서 설정합니다. 문서는 설정 전의 저렴한 기본 모델이 코드 작성에 적합하지 않을 수 있다고 명시합니다. [첫 계정과 시작](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/README.md#L81-L86), [코딩 에이전트 설정](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/docs/self-hosting.md#L303-L324)

명령행 하네스만 살펴보려면 문서에는 다음 경로도 있습니다. 세 명령은 `new`로 만든 동일한 실행 이름을 사용합니다. `serve`는 고객 서비스를 유지하는 프로세스이므로, 작업 단계와 마지막 채점 단계가 있다는 의미로 읽어야 합니다.

```bash
python3 harness/run.py new   --engagement oncall_incident --level L3 --name oncall-L3-me-1
python3 harness/run.py serve --name oncall-L3-me-1
python3 harness/run.py grade --name oncall-L3-me-1
```

[하네스 README 원문](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/harness/README.md#L21-L38)

이 예시는 해당 사례 파일이 준비되어 있다는 전제입니다. 사례 다운로드 스크립트는 기본적으로 `DeepLethe/FDE-Gym-examples`에서 받으며, 기존 사례 폴더는 `--force`가 없으면 건너뜁니다. 플랫폼 코드를 업데이트하는 것과 이미 내려받은 사례를 갱신하는 것은 별도 작업입니다. [다운로더](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/scripts/fetch_cases.py#L26-L29), [기존 파일 처리](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/scripts/fetch_cases.py#L65-L85)

## 배포와 분석에서 지켜야 할 경계

### 로컬 Docker와 호스트 직접 실행은 다릅니다

기본 Compose는 runner를 내부 네트워크에 두고 사이트만 함께 연결합니다. runner는 DB·객체 저장소·공급자 키를 직접 받지 않으며, 모델 요청은 사이트의 relay를 사용합니다. 이미지에는 `FDEGYM_EXEC_UID_BASE=20000`이 설정되고, 각 run에 별도 시스템 사용자 ID를 부여합니다. 작업 공간의 소유권을 나누고 보호 자료는 root 소유로 두는 경계입니다. [Compose의 네트워크와 비밀 분리](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/docker-compose.yml#L100-L130), [이미지 설정](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/Dockerfile#L26-L39), [사용자 할당과 보호 자료](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/harness.ts#L67-L124)

채점에서도 전달된 코드의 실행 사용자를 바꾸는 경로가 있습니다. `harnessEnv()`가 `FDEGYM_DELIVERED_UID`를 전달하고, Python `delivered_python()`이 그 사용자로 코드가 실행되는 wrapper와 probe를 준비합니다. 따라서 TypeScript 파일 상단의 오래된 요약 주석만 보고 “채점은 항상 서버 권한”이라고 단정하면 현재 구현과 어긋납니다. 반대로 이 경로가 있다는 이유만으로 사례별 grader가 모두 같은 실행 방식을 지킨다고 보장할 수도 없습니다. 하네스 내부 프로세스로 전달된 코드를 직접 import하는 grader의 경계는 문서도 별도로 설명합니다. [실제 환경 전달](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/harness.ts#L45-L50), [채점 연결](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/harness/run.py#L502-L542), [실행 사용자 선택](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/harness/isolate.py#L152-L224), [문서의 예외](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/docs/self-hosting.md#L278-L292)

호스트에서 `pnpm dev`, `pnpm start`, `pnpm runner`를 직접 실행하면 설정과 운영체제에 따라 경계가 달라집니다. TypeScript 터미널의 macOS sandbox와 Python 채점의 선택적 `FDEGYM_SANDBOX`도 다른 설정입니다. 문서는 직접 실행한 채점의 권한과, 같은 runner에 있는 다른 run의 포트·프로세스 정보 노출을 한계로 명시합니다. 이 리뷰는 격리 공격을 수행하지 않았으며, 소스와 문서에 정의된 경계만 설명합니다. [터미널 격리 선택](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/app/server/harness.ts#L519-L567), [채점 sandbox 선택](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/harness/isolate.py#L167-L201), [보안 문서](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/docs/self-hosting.md#L228-L295)

### 실행 기계와 채점기는 신뢰하는 구성요소입니다

runner는 사이트가 신뢰하는 기계입니다. join token이 있다고 해서 악의적인 runner가 돌려주는 채점 결과까지 독립적으로 검증되는 것은 아닙니다. 문서의 Trust 항목은 사이트가 runner의 보고를 믿으며 runner는 답이 포함된 모든 사례 아카이브를 가져올 수 있다고 명시합니다. 따라서 runner 운영자를 신뢰하는 것은 이 구조의 전제로 읽어야 합니다. 같은 이유로 사례 아카이브를 읽고 Python 세계 생성기와 grader를 실행하는 경로는, 아무 출처의 사례 파일이나 신뢰해도 된다는 뜻이 아닙니다. [runner 신뢰 계약](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/docs/self-hosting.md#L51-L81), [사례 모듈 로딩](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/harness/run.py#L348-L356), [grader 로딩](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/harness/run.py#L494-L511)

### 코드 라이선스와 사례의 조건을 분리합니다

플랫폼과 하네스는 Apache License 2.0이고 사례 데이터는 별도의 이용 조건을 가집니다. README는 사례를 학습에 쓰지 말라고 요청하고, 하네스 문서도 벤치마크 데이터가 학습 말뭉치에 들어가서는 안 된다고 명시합니다. “오픈소스 플랫폼”이라는 말만으로 전체 사례 데이터의 재배포나 학습 사용 권한까지 같은 것으로 보면 안 됩니다. [라이선스](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/LICENSE#L1-L16), [README의 사례 조건](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/README.md#L140-L145), [하네스의 학습 금지 요청](https://github.com/deeplethe/fde-gym/blob/1d9ed027af7c8312bacb1abad1467c87a91c004b/harness/README.md#L91-L98)

## 무엇을 배울 수 있는가

FDE Gym의 구조는 에이전트 평가가 모델의 답변만으로 끝나지 않는다는 점을 보여 줍니다. 고객의 요청은 공개하되 정답은 숨기고, 여러 번의 상호작용에 상태와 비용을 붙이며, 수정한 시스템을 같은 사례 버전의 채점기로 다시 실행합니다. 웹 화면, 저장소, runner, 코딩 에이전트와 모델 relay를 나눈 구현을 읽으면 각각이 결과의 재현성과 운영 경계에 어떤 역할을 하는지 볼 수 있습니다.

리뷰어 관점에서 특히 유용한 부분은 **해결책이 무엇을 바꿨는지와, 그 해결책을 얻는 과정에서 무엇을 소비했는지를 따로 기록하는 설계**입니다. 시스템의 KPI 개선, 고객에게 묻고 기다린 비용, 코딩 에이전트의 API 비용은 서로 다른 지표입니다. 최종 점수 하나를 읽을 때도 이 입력과 경계를 함께 확인해야 플랫폼이 무엇을 평가하는지 이해할 수 있습니다.

## 이 글에서 다루지 못한 부분

계정 등록·암호 재설정·메일 전송·관리자 화면 전체와 프런트엔드의 개별 컴포넌트, `bench.py`의 모든 모델 평가 경로, `audit.py`의 감사 규칙 전체를 상세히 분석하지 않았습니다. 별도 데이터셋의 세 공개 사례 및 접근 제한된 전체 사례도 다운로드·실행하지 않았으므로, 사례별 숨겨진 KPI·grader·정답의 타당성, 실제 배포의 격리 강도와 비용·성능은 이 글의 검증 범위 밖입니다. 관련 논문은 공개 범위와 문제 배경을 확인하기 위해 초록을 대조했으며, 본문 전체를 리뷰한 것은 아닙니다.
