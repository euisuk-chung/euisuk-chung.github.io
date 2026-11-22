---
type: "Repo Review"
title: "[Repo Review] Cua — AI에게 컴퓨터를 건네기 전에 필요한 실행 환경과 좌표의 약속"
description: "Cua의 실행 환경 생성부터 MCP 대상 선택, 화면 좌표 변환과 입력 전달까지를 고정 커밋으로 추적하고 SDK·Spaces·Driver의 역할과 라이선스 경계를 살펴봅니다."
date: "2026-11-23"
tags:
  - "Repo Review"
  - "AI Agent"
  - "MCP"
  - "Python"
  - "Tools"
resource: "https://github.com/trycua/cua/tree/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a"
generated:
  by: "process:blog-review"
  at: "2026-11-23T06:09:06+09:00"
sources:
  - id: "github:trycua/cua"
    resource: "https://github.com/trycua/cua/tree/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a"
    title: "Cua"
    author: "Cua AI, Inc."
status: "stable"
year: "2026"
analyzed_at: "2026-11-23T06:09:06+09:00"
source_id: "trycua/cua"
source_revision: "04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a"
source_type: "repo"
source_url: "https://github.com/trycua/cua/tree/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a"
visual_sources:
  - path: "img/reviews/2026/cua-review/control-path.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/libs/cua/crates/cua-cli/src/mcp.rs#L1122-L1228"
    caption: "에이전트의 MCP 요청이 sandbox 선택, 환경 연결, 데스크톱 서비스와 Driver로 이어지는 흐름. 리뷰어 작성, 분석 커밋 기준."
  - path: "img/reviews/2026/cua-review/coordinate-map.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/libs/cua/crates/cua-cli/src/computer.rs#L22-L36"
    caption: "이미지 픽셀을 화면의 논리 좌표로 되돌리는 계산 예. 수치는 설명용이며 실행 결과가 아닙니다. 리뷰어 작성, 분석 커밋 기준."
---

## 들어가며: 모델이 클릭할 위치를 알아도 일이 끝나지는 않습니다

AI가 화면을 보고 “이 버튼을 누르면 된다”고 판단했다고 해 보겠습니다. 그다음에는 어떤 컴퓨터에서 작업할지, 그 화면을 어떻게 가져올지, 축소된 이미지의 좌표를 실제 클릭 위치로 어떻게 바꿀지가 남습니다. 작업용 컴퓨터가 켜졌다는 사실과 그 안의 앱을 조작할 준비가 됐다는 사실도 다릅니다.

Cua는 이 사이를 연결하는 프로젝트입니다. 에이전트가 쓸 컴퓨터와 실행 환경을 준비하고, 화면·입력·파일·프로세스를 다루는 인터페이스를 제공합니다. 루트 README도 기본 방향을 “기존 에이전트와 모델을 가져오면 Cua가 컴퓨터와 자동화 도구를 제공한다”로 설명합니다. [프로젝트 소개](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/README.md#L60-L70)에서 출발해 실제 요청 경로를 따라가 보겠습니다.

분석한 버전은 커밋 `04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a`입니다. 대상 코드를 설치하거나 실행하지 않고 문서와 구현을 읽었습니다. 따라서 아래의 흐름은 코드에서 확인한 동작이며, 운영 안정성이나 모델의 작업 성공률을 측정한 결과는 아닙니다.

## Cua는 무엇인가

Cua를 한 문장으로 설명하면 **AI 에이전트가 컴퓨터를 만들고, 연결하고, 관찰하고, 조작할 때 쓰는 도구 묶음**입니다. 저장소 전체가 하나의 모델이나 하나의 앱으로 구성되지는 않습니다.

| 구성 | 맡는 일 | 이번 리뷰의 범위 |
| --- | --- | --- |
| Cua SDK·CLI | sandbox 생성·조회·접속과 공통 호출 인터페이스 | 생성 준비·실패 처리, MCP 진입점과 환경 선택 |
| Cua Spaces | 사람이 컴퓨터와 에이전트 작업 공간을 관리하는 앱 | README상 역할만 확인 |
| `cua-spacesd` | 작업 환경 안에서 프로세스·파일·화면·입력을 제공하는 서비스 | capability 접속, 화면 캡처와 입력 서비스 |
| Cua Driver | 운영체제의 앱·창·입력과 연결되는 도구 | spacesd backend에서 호출하는 경계 확인 |
| Lume·다른 로컬 런타임 | VM·컨테이너 실행 | 상위 생성 흐름까지만 확인 |
| CUA-S1·Cua Bench | 특화된 의사결정 모델과 평가 도구 | 모델 학습·평가 구현은 미분석 |

여기서 sandbox는 작업할 프로그램을 띄우는 별도의 실행 환경을 뜻합니다. Cua에서는 컨테이너와 VM, 이미 존재하는 컴퓨터에 대한 직접 접속 등이 같은 상위 API에 나타납니다. 실제 격리 방식과 지원 기능은 선택한 런타임에 따라 달라집니다. `cua-spacesd`는 그 환경 안에서 화면과 입력 같은 기능을 제공하는 서비스이며, 실행 환경 자체와 구별해야 합니다. [SDK의 구조 설명](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/libs/cua/README.md#L1-L35)에 이 구분이 나와 있습니다.

## 아키텍처: 실행 환경과 데스크톱 제어를 나눕니다

현대 SDK·CLI의 중심은 `libs/cua`의 Rust workspace입니다. `cua-sdk`가 언어 바인딩을 위한 공통 인터페이스를 내보내고, `cua-sandbox-core`가 실행 환경의 수명과 위치를 다룹니다. CLI는 `cua-cli`, 환경과 통신하는 클라이언트는 `cua-spacesd-client`, 메시지 계약은 `cua-proto`로 나뉩니다. Python·TypeScript 등의 진입면을 제공하면서 핵심 런타임을 공유하는 구조입니다. [crate 구성표](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/libs/cua/README.md#L80-L120), [Python 패키지 매니페스트](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/libs/cua/python/pyproject.toml#L5-L58)를 함께 읽으면 연결 관계가 드러납니다.

반면 환경 안의 서비스는 `libs/cua-spacesd`에 있습니다. 그중 desktop 서비스는 요청을 화면·포인터 같은 플랫폼 중립 자료형으로 바꾸고 backend에 넘깁니다. backend는 화면 캡처 제공자와 Cua Driver의 도구 레지스트리에 연결됩니다. **클라이언트에서 모델이 판단하고, 서비스가 그 판단을 운영체제 동작으로 전달하는 경로**를 나눈 셈입니다. [서비스와 backend의 경계](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/libs/cua-spacesd/crates/cua-spacesd-desktop/src/grpc/backend.rs#L1-L12), [Driver 연결부](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/libs/cua-spacesd/crates/cua-spacesd-desktop/src/grpc/tool_backend.rs#L1-L84)에 근거한 해석입니다.

![MCP 요청에서 sandbox 선택, spacesd 접속, ComputerService와 Driver로 이어지는 제어 경로]({{ '/img/reviews/2026/cua-review/control-path.svg' | relative_url }})

에이전트의 요청은 실행 대상을 고른 뒤 그 환경의 데스크톱 서비스로 전달됩니다. 리뷰어 작성, 분석 커밋 기준. 출처: [MCP 요청 처리](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/libs/cua/crates/cua-cli/src/mcp.rs#L1122-L1228)와 [desktop backend](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/libs/cua-spacesd/crates/cua-spacesd-desktop/src/grpc/tool_backend.rs#L573-L640).
{: .caption}

위 그림은 이번에 추적한 **`cua mcp`의 sandbox computer 도구 경로**입니다. 별도의 `cua-driver mcp`에 직접 연결하는 방식도 있으므로, Cua의 모든 호출이 이 그림의 모든 계층을 반드시 거친다는 뜻은 아닙니다. [Driver README의 연결 방식](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/libs/cua-driver/README.md#L59-L73)을 구별해 읽어야 합니다.

## 작동 원리 1: 컴퓨터가 켜졌다는 것과 도구가 준비됐다는 것은 다릅니다

### 생성 요청은 먼저 배치 조건을 확인합니다

`Sandboxes::create`는 이미지와 실행 위치 등의 옵션을 받아 시작합니다. `apply_placement`와 sidecar 검사를 거친 뒤 이미지를 준비하고, provider 종류에 따라 로컬 생성 또는 외부 provider 생성으로 분기합니다. `Direct`는 여기서 새로 만들 수 없고 기존 환경에 연결해야 한다는 오류를 반환합니다. 예전에 쓰던 `pool:` 이미지 형식도 이 커밋에서는 종료된 Cua Cloud 경로로 처리합니다. [생성 요청의 검증과 분기](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/libs/cua/crates/cua-sandbox-core/src/sandbox.rs#L845-L880)를 보면 ‘같은 API’가 모든 옵션 조합을 허용한다는 의미는 아님을 알 수 있습니다.

이미지 다운로드에 걸린 시간이 게스트의 부팅 준비 시간을 모두 소모하지 않도록, 준비 상태를 기다리는 시간의 기준도 따로 둡니다. 생성 뒤에는 요청한 `wait_for` 서비스들을 기다립니다. 이미지가 `cua-spacesd`를 포함한다고 선언한 경우에는 그 서비스의 준비도 추가로 확인하고, 선언하지 않은 이미지에 대해서는 무조건 기다리지 않습니다. [준비 상태 판정](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/libs/cua/crates/cua-sandbox-core/src/sandbox.rs#L868-L914)의 핵심은 이 조건부 검사입니다.

다음은 해당 코드를 흐름만 남겨 다시 쓴 **설명용 의사코드**입니다. 실제 함수의 옵션·오류 종류 일부는 생략했습니다.

```text
입력: 이미지, 실행 위치, 이름, readiness 조건
검증하고 이미지를 준비한다
실행 위치에 맞는 환경을 생성한다
요청한 서비스의 준비를 기다린다
이미지가 spacesd를 선언했다면 그 서비스의 준비도 기다린다
실패하면 새로 만든 환경의 정리 여부를 판단하고 오류를 반환한다
성공하면 Sandbox 핸들을 반환한다
```

출처: [Sandboxes::create](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/libs/cua/crates/cua-sandbox-core/src/sandbox.rs#L845-L937). 이 의사코드는 동작 설명이며 복사해 실행하는 사용 예제가 아닙니다.

### 실패해도 기존 환경을 무조건 지우지는 않습니다

준비 상태 확인에 실패했을 때, 이름이 이미 사용 중이던 환경은 보존합니다. 새로 만든 환경은 임시 환경인지, `keep_on_failure` 설정이 있는지에 따라 삭제하거나 남깁니다. 시작 도중 실패한 경우를 정리하는 `discard_failed_start` 역시 기존 환경을 보존하는 분기가 있습니다. [준비 실패 처리](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/libs/cua/crates/cua-sandbox-core/src/sandbox.rs#L915-L959)에 이 기준이 명시되어 있습니다.

이 구분은 재시도하는 도구에서 읽어 둘 만합니다. ‘이번 호출이 만든 자원’과 ‘원래 존재하던 자원’을 구별해야 실패를 정리하는 과정이 기존 작업을 지우지 않기 때문입니다. 다만 삭제 시도 자체가 실패할 수도 있고, 코드는 그 오류를 로그로 남깁니다. 여기서 모든 실패 뒤 자원이 남지 않는다고 단정할 수는 없습니다.

## 작동 원리 2: 에이전트의 도구 요청을 실제 컴퓨터에 연결합니다

### MCP는 명령을 전달하는 입구입니다

MCP(Model Context Protocol)는 에이전트가 외부 도구를 일정한 형식으로 호출하도록 연결하는 프로토콜입니다. 이 저장소에서 `cua mcp`와 `cua daemon mcp`는 같은 MCP 서버 구성 경로로 들어갑니다. CLI는 권한 문자열을 파싱하고 기본 sandbox 이름과 함께 서버를 만듭니다. [명령 분기](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/libs/cua/crates/cua-cli/src/lib.rs#L2120-L2132)를 확인했습니다.

sandbox용 computer 도구가 호출되면 먼저 인자의 `sandbox` 값을 찾고, 없으면 서버를 시작할 때 지정한 기본값을 사용합니다. 둘 다 없으면 ‘어느 컴퓨터를 조작할지 지정하지 않았다’는 오류를 냅니다. 이어 `env_of`가 relay Space, 등록된 Space, 직접 접속 endpoint, 일반 sandbox 연결 등을 구별합니다. [대상 선택](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/libs/cua/crates/cua-cli/src/mcp.rs#L1122-L1138), [실제 접속 경로](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/libs/cua/crates/cua-cli/src/sandbox.rs#L3073-L3107)가 이어지는 부분입니다.

여기서 기본값은 단순 편의 기능 이상입니다. 모델이 같은 이름의 도구를 호출하더라도 어느 환경에 연결됐는지에 따라 실제 동작 대상이 달라집니다. 입력 인자의 대상과 서버 기본 대상을 함께 읽어야 코드의 실행 범위를 이해할 수 있습니다.

### 접속은 포트가 열렸는지만 보지 않습니다

`SpacesdClient::connect`는 기본 탐색 경로에서 `GetCapabilities` 요청으로 연결 상대가 예상한 서비스인지 확인합니다. native gRPC를 먼저 시도하고 gRPC-Web도 확인하는 구조이며, 아무 경로에서도 올바른 응답을 얻지 못하면 `SpacesdNotAvailable` 오류를 반환합니다. 반면 인증 실패 응답을 받았다면 다른 전송 방식으로 계속 우회하지 않고 인증 오류를 그대로 돌려줍니다. 명시적으로 probe를 끄는 옵션도 있으므로, 모든 호출이 항상 이 검사를 수행한다고 일반화하면 안 됩니다. [연결 탐색 구현](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/libs/cua/crates/cua-spacesd-client/src/client.rs#L295-L360)에 이 분기들이 모여 있습니다.

상위 sandbox의 연결 과정에는 초기 토큰이 설정되지 않은 서비스의 bootstrap 처리도 있습니다. capability 응답의 `initialized` 상태를 보고 토큰으로 초기화한 다음 다시 연결하고, 임시가 아닌 환경이면 관련 상태를 저장합니다. [초기화와 재접속](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/libs/cua/crates/cua-sandbox-core/src/sandbox.rs#L2892-L2940)을 읽으면 생성과 첫 접속 사이에 필요한 작업이 보입니다. 이 경로를 확인했다는 사실이 저장소 전체의 인증 보안성을 감사했다는 의미는 아닙니다.

## 작동 원리 3: 화면을 줄였다면 클릭 좌표도 되돌려야 합니다

### 이미지만 보내지 않고 좌표 정보를 함께 받습니다

`computer_screenshot`은 공통 `Computer` 객체에 화면 캡처를 요청합니다. 이 경로의 긴 변 상한은 1,200픽셀입니다. 이는 모델에 전달할 화면의 크기 제한이며, 원래 화면 해상도를 1,200으로 바꾼다는 뜻은 아닙니다. 반환된 PNG와 함께 `scale`, `origin`을 받아 해당 sandbox의 최근 화면 매핑으로 저장합니다. [상한과 캡처 요청](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/libs/cua/crates/cua-cli/src/computer.rs#L10-L11), [MCP 결과 구성](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/libs/cua/crates/cua-cli/src/mcp.rs#L1203-L1217)을 확인했습니다.

환경 안의 `ComputerService.Screenshot`은 화면이나 창을 선택해 캡처하고, 필요하면 크기를 비례 축소합니다. 응답에는 축소 후 픽셀 크기, 원래 픽셀 크기, 논리적 화면 영역과 배율이 들어갑니다. [캡처·축소·응답](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/libs/cua-spacesd/crates/cua-spacesd-desktop/src/grpc/computer.rs#L354-L453)과 [프로토콜 정의](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/libs/cua/proto/cua/env/v1/computer.proto#L10-L85)가 같은 구분을 사용합니다.

논리 좌표는 운영체제가 창의 위치와 크기를 표현할 때 쓰는 좌표입니다. 고해상도 디스플레이에서는 이미지의 물리 픽셀 수와 논리 좌표 수가 다를 수 있고, 일부 영역을 캡처했다면 시작점도 달라집니다. 그래서 이미지에서 찾은 위치를 그대로 화면 좌표로 넘기면 맞지 않을 수 있습니다.

![이미지 좌표와 배율·시작점을 이용해 논리 화면 좌표를 계산하는 예]({{ '/img/reviews/2026/cua-review/coordinate-map.svg' | relative_url }})

이미지의 위치에 배율과 시작점을 적용하는 계산 예입니다. 수치는 설명용이며 실행 결과가 아닙니다. 리뷰어 작성, 분석 커밋 기준. 출처: [map_point](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/libs/cua/crates/cua-cli/src/computer.rs#L22-L36).
{: .caption}

예를 들어 이미지 위치가 `(300, 150)`, 배율이 `1.5`, 캡처 시작점이 `(100, 50)`이라면 논리 화면 위치는 `(300, 150)`이 됩니다. 계산은 각 축에서 `시작점 + 이미지 위치 / 배율`입니다. 이 숫자는 실제 앱에서 얻은 좌표가 아니라 변환을 설명하기 위해 정한 값입니다.

아래는 이 계산을 수행하는 원본 함수입니다.

```rust
pub fn map_point(p: (f64, f64), scale: f64, origin: (f64, f64)) -> (f64, f64) {
    let s = if scale > 0.0 { scale } else { 1.0 };
    (origin.0 + p.0 / s, origin.1 + p.1 / s)
}
```

출처: [computer.rs 34–37행](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/libs/cua/crates/cua-cli/src/computer.rs#L34-L37), Copyright 2025 Cua AI, Inc., [MIT License](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/LICENSE.md). 짧은 원본 함수 발췌입니다.

### 최근 캡처의 좌표계를 sandbox별로 보관합니다

MCP 서버의 매핑은 sandbox 이름을 키로 하는 사전입니다. 클릭 요청에서는 해당 매핑을 꺼내 좌표를 변환하고 반올림합니다. 아직 캡처하지 않았다면 배율 1과 시작점 0이 기본값입니다. 따라서 이 경로를 사용할 때 ‘최근 관찰한 화면을 기준으로 다음 입력을 보낸다’는 순서가 중요합니다. 이는 코드에서 읽은 사용상 해석이며, 화면 변화 때문에 실제로 얼마만큼 오류가 발생하는지를 시험한 결과는 아닙니다. [매핑 자료구조](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/libs/cua/crates/cua-cli/src/mcp.rs#L1000-L1009), [변환과 클릭](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/libs/cua/crates/cua-cli/src/mcp.rs#L1141-L1152), [실제 클릭 분기](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/libs/cua/crates/cua-cli/src/mcp.rs#L1219-L1228)를 연결해 볼 수 있습니다.

이 MCP 경로의 좌표 매핑과, 프로토콜이 제공하는 `screenshot_id` 기반 좌표 지정은 구별해야 합니다. 프로토콜에는 특정 캡처의 픽셀을 지정하는 방식도 있지만, 위 MCP 클릭 구현은 저장한 배율·시작점으로 화면 좌표를 계산한 뒤 일반 클릭을 보냅니다. 서로 다른 층의 보장 조건을 섞으면 ‘모든 클릭에 캡처 식별자가 필수다’라는 잘못된 설명이 됩니다.

## 작동 원리 4: 클릭 요청의 성공과 업무 성공은 다릅니다

변환된 좌표는 `Computer::click`에서 클라이언트의 `click_with`로 넘어갑니다. 클라이언트는 `PointerRequest`를 만들고, 서버는 입력 대상을 해석한 뒤 backend의 포인터 함수를 호출합니다. backend는 동작이 클릭인지, 이동인지, 드래그인지에 따라 Driver 도구 이름과 인자를 구성합니다. [클라이언트 요청](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/libs/cua/crates/cua-spacesd-client/src/computer.rs#L198-L255), [서비스의 전달](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/libs/cua-spacesd/crates/cua-spacesd-desktop/src/grpc/computer.rs#L545-L578), [Driver 도구 선택](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/libs/cua-spacesd/crates/cua-spacesd-desktop/src/grpc/tool_backend.rs#L573-L640)에 이 흐름이 있습니다.

일반적인 화면 좌표 입력에서는 서버가 보고한 포인터 전달 결과를 확인하는 코드도 있습니다. 해당 요청이 위치를 지정한 입력인지 판단한 뒤 `check_pointer_delivered`로 보고를 검사합니다. 다만 이는 버튼을 눌러 주문이 완료됐다거나 문서가 올바르게 저장됐다는 검증이 아닙니다. 입력 전달 결과와 앱의 최종 업무 결과는 다른 층의 문제입니다.

README가 계산기 예시에서도 앱에 `42`가 표시되는지 확인하도록 안내하는 이유를 이 구조와 연결해 이해할 수 있습니다. Cua가 관찰·행동의 인터페이스를 제공하더라도, 에이전트는 행동 뒤의 화면이나 상태를 다시 읽어 목적을 달성했는지 판단해야 합니다. [README의 첫 작업 예시](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/README.md#L111-L119)를 참고한 리뷰어의 해석입니다.

## 설치와 사용: 문서에 나온 경로를 구별해 읽기

이 절의 명령은 고정 커밋 README에 있는 사용법 소개이며 실행하지 않았습니다. 루트 README는 macOS·Linux와 Windows용 설치 스크립트를 각각 안내합니다. 설치 대상은 SDK·CLI, Spaces 앱, Driver 중 무엇을 선택하는지에 따라 달라지므로, `cua`와 `cua-driver`를 같은 실행 파일로 보아서는 안 됩니다.

아래는 README의 sandbox 예시입니다. 이름을 붙인 Ubuntu 환경을 만든 다음, 명령 실행과 화면 캡처를 요청하고 마지막에 제거합니다.

```sh
cua sb create ubuntu --name dev
cua sb exec dev uname -a
cua sb screenshot dev
cua sb rm dev
```

출처: [루트 README의 Cua SDK and CLI](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/README.md#L157-L181). 출력 예시는 제시하지 않습니다.

같은 저장소가 Python에서는 `Sandbox.ephemeral(Image.linux(), local=True)`를 `async with`와 함께 사용하는 예도 제공합니다. 이때 Python 패키지 `cua-sandbox`는 Rust SDK인 `cua`에 의존하는 상위 편의 API이며, 현재 매니페스트는 Python `>=3.11,<3.14`를 요구합니다. 반면 `cua` 자체 매니페스트의 최소 버전은 Python 3.10입니다. 패키지 이름이 비슷해도 요구 환경을 각각 확인해야 합니다. [Python 예시](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/README.md#L170-L180), [cua-sandbox 의존성과 버전 조건](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/libs/python/cua-sandbox/pyproject.toml#L1-L43), [cua 매니페스트](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/libs/cua/python/pyproject.toml#L5-L35)를 대조했습니다.

MCP 연결에서는 도구 권한도 따로 선택합니다. `--permissions` 또는 `CUA_MCP_PERMISSIONS`를 사용하며, `computer:readonly`는 화면 캡처 권한으로 확장됩니다. 빈 권한 문자열의 기본값은 전체 권한이므로 ‘MCP로 연결했다’는 사실만으로 읽기 전용이라고 생각하면 안 됩니다. 도구 목록뿐 아니라 호출 시에도 허용된 도구인지 확인합니다. [권한 파싱](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/libs/cua/crates/cua-cli/src/mcp.rs#L85-L163), [호출 진입 검사](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/libs/cua/crates/cua-cli/src/mcp.rs#L1932-L1965)를 읽어 둘 필요가 있습니다.

## 한계와 주의점

### 모든 sandbox가 같은 컴퓨터 도구를 제공하지는 않습니다

실행 환경의 준비 상태와 `cua-spacesd`의 기능 준비는 구분됩니다. 상위 생성 흐름은 서비스가 없는 이미지를 허용하지만, `cua mcp`의 computer 도구는 `env_of`를 거쳐 그 서비스에 연결합니다. 서비스가 없을 때 모든 도구가 자동으로 같은 대안 경로를 사용하는 것은 아닙니다.

실제로 `cua sb screenshot`에는 `SpacesdNotAvailable`일 때 가능한 로컬 환경의 게스트 캡처로 돌아가는 분기가 있습니다. 그러나 위에서 본 MCP `computer_screenshot`은 먼저 `self.computer`의 환경 연결을 요구합니다. **CLI 화면 캡처의 대안 경로를 MCP 도구 전체의 보장으로 확대하면 안 됩니다.** [CLI 대안 경로](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/libs/cua/crates/cua-cli/src/sandbox.rs#L2899-L2922)와 [MCP 처리](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/libs/cua/crates/cua-cli/src/mcp.rs#L1203-L1217)의 차이입니다.

백그라운드 입력도 앱과 플랫폼이 지원하는 범위에 의존합니다. README의 설명 자체가 이 조건을 붙이고 있으며, backend에는 별도의 마우스 down/up을 해당 Driver 도구 경로에서 지원하지 않아 오류를 반환하는 분기도 있습니다. [README의 지원 조건](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/README.md#L97-L99), [지원되지 않는 입력](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/libs/cua-spacesd/crates/cua-spacesd-desktop/src/grpc/tool_backend.rs#L632-L637)을 확인했습니다. ‘모든 앱을 포커스 변화 없이 조작한다’고 일반화할 수는 없습니다.

### 라이선스는 저장소 전체에 하나로 적용되지 않습니다

루트 라이선스는 MIT지만, 하위 디렉터리에 자체 라이선스가 있으면 그것이 적용됩니다. SDK·CLI·Driver·Lume 등과 달리 Spaces 앱, `cua-spacesd`, Keyvault·Teleport 등은 FSL-1.1-MIT로 명시되어 있습니다. 저장소의 라이선스 문서는 이를 source-available로 구분하고, 경쟁 용도에 대한 제한과 릴리스 후 2년이 지나면 해당 릴리스에 MIT가 추가 적용되는 조건을 설명합니다. [라이선스 범위](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/legal/LICENSING.md#L3-L17), [FSL 범위와 조건](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/legal/LICENSING.md#L84-L100), [spacesd의 실제 라이선스](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/libs/cua-spacesd/LICENSE)를 함께 봐야 합니다.

따라서 이 레포를 통째로 ‘MIT 오픈소스 앱’이라고 부르면 분석한 버전의 조건을 놓칩니다. 선택적 시각 인식 확장과 모델 파일에도 별도 조건이 있으므로 Driver 기본 패키지와 구별해야 합니다. [선택적 perception 설명](https://github.com/trycua/cua/blob/04b60eafc3d278190e4b0e583e0e0d9ea8fb9c9a/libs/cua-driver/README.md#L8-L27)은 이 경계를 명시합니다. 이번 글은 해당 라이선스 파일과 문서에 적힌 범위를 소개하며, 개별 배포 방식의 법적 적합성을 판정하지 않습니다.

## 정리

Cua에서 배울 만한 부분은 에이전트의 판단과 컴퓨터의 동작 사이에 필요한 약속을 코드로 나눴다는 점입니다. sandbox 생성에서는 실행 위치·준비 상태·실패 정리를 다루고, 제어 경로에서는 대상 선택·접속 기능·화면 좌표·입력 결과를 구분합니다.

특히 축소된 이미지의 클릭 좌표를 복원하는 작은 함수가 전체 흐름을 잘 보여 줍니다. 모델이 어떤 위치를 선택했는지와, 그 위치가 실제 컴퓨터에서 무엇을 가리키는지는 별도의 정보입니다. Cua는 그 연결을 도구와 메시지 계약으로 드러내고 있습니다.

### 이 글에서 다루지 못한 부분

Spaces 앱의 전체 화면 흐름, Teleport의 세션 이동·Keyvault 암호화 구현, Lume와 QEMU의 내부 VM 생성, 클러스터 스케줄러, 미디어 스트리밍의 전송·코덱, CUA-S1 학습 및 Cua Bench의 평가 타당성은 상세 분석하지 않았습니다. Driver의 운영체제별 모든 backend도 감사하지 않았습니다. 본문은 고정 커밋의 SDK·CLI 수명 관리와 sandbox computer 도구의 요청·응답 경로에 한정됩니다.
