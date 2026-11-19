---
type: "Repo Review"
title: "[Repo Review] ECC — 스킬과 훅, 기억을 연결하는 코딩 에이전트의 작업 환경"
description: "ECC의 도구 이벤트 처리와 세션 복원, 선택적 패턴 추출 및 Memory Vault를 고정 코드로 따라가며 지침과 실제 실행의 경계를 살펴봅니다."
date: "2026-11-20"
tags:
  - "Repo Review"
  - "AI Agent"
  - "Anthropic"
resource: "https://github.com/affaan-m/ECC/tree/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7"
generated:
  by: "process:blog-review"
  at: "2026-11-20T06:03:46+09:00"
sources:
  - id: "affaan-m/ecc"
    resource: "https://github.com/affaan-m/ECC/tree/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7"
    title: "ECC"
status: "stable"
year: "2026"
analyzed_at: "2026-11-20T06:03:46+09:00"
source_id: "affaan-m/ecc"
source_revision: "3f14a103a8694e51c1df9a806217a6d0b5f7a6f7"
source_title: "ECC"
source_type: "repo"
source_url: "https://github.com/affaan-m/ECC/tree/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7"
visual_sources:
  - path: "/img/reviews/2026/ecc-agent-harness-review/ecc-layers.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/scripts/hooks/posttooluse-dispatcher.js#L35-L70"
    caption: "리뷰어 작성, 분석 커밋 기준. 호스트 아래의 지침, 이벤트 훅, 지속 상태를 구분합니다."
    evidence_urls:
      - "https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/hooks/hooks.json#L137-L179"
      - "https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/scripts/memory.js#L456-L479"
  - path: "/img/reviews/2026/ecc-agent-harness-review/ecc-learning-flow.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/skills/continuous-learning-v2/hooks/observe.sh#L407-L482"
    caption: "리뷰어 작성, 분석 커밋 기준. 관찰 저장과 선택적 observer 및 다음 문맥 주입의 경로입니다."
    evidence_urls:
      - "https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/skills/continuous-learning-v2/config.json#L1-L8"
      - "https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/skills/continuous-learning-v2/agents/observer-loop.sh#L268-L315"
      - "https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/scripts/hooks/session-start.js#L469-L529"
---

## 들어가며

코딩 에이전트에게 “테스트하고, 리뷰하고, 다음 세션에도 기억해 주세요”라고 적는 일은 쉽습니다. 어려운 부분은 그 요구가 실제로 어느 순간 실행되고, 무엇을 기록하며, 다음 작업에 어떤 형태로 돌아오는지를 정하는 일입니다. **ECC**는 이 주변 장치를 한 저장소에 모은 프로젝트입니다. README는 `plan → test → implement → review → verify → remember → improve`라는 작업 흐름을 제시합니다. [README의 정의](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/README.md#L131-L154)

고정 커밋 `3f14a103a8694e51c1df9a806217a6d0b5f7a6f7`의 패키지 버전은 **2.2.3**입니다. 이 글에서는 Claude Code용 지침과 훅, 세션 요약, 지속 학습, Memory Vault를 정적으로 추적합니다. 명령이나 모델을 실행해 결과를 재현하지는 않았습니다. “자동으로 해 준다”는 소개를 읽을 때, **모델이 읽는 절차인지, 호스트가 호출하는 코드인지, 파일에 남는 상태인지**를 나누어 보면 구현이 훨씬 잘 보입니다. [패키지 정보](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/package.json#L1-L15) · [분석 커밋](https://github.com/affaan-m/ECC/tree/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7)

## ECC는 무엇인가요?

ECC는 코딩 에이전트의 작업 절차와 실행 보조 기능을 배포하는 하네스 도구 모음입니다. 여기서 **하네스**는 모델이 도구를 사용하고, 작업 상태를 이어 가며, 결과를 확인하도록 둘러싼 실행 환경을 뜻합니다. 모델 자체를 학습하는 프레임워크와는 역할이 다릅니다.

README에 적힌 규모는 에이전트 72개, 스킬 327개, 기존 명령 진입점 98개입니다. 이는 해당 커밋의 문서상 집계이며, 이 글에서 그 전부의 동작을 검증한 수는 아닙니다. 문서는 Claude Code를 주 지원 대상으로 두고 다른 호스트에는 기능 차이가 있다고 명시합니다. [구성 목록](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/README.md#L143-L154) · [지원 범위](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/README.md#L1332-L1342)

| 구성 | 실제 형태 | 역할 |
| --- | --- | --- |
| 스킬 | `skills/*/SKILL.md` | 특정 작업을 언제 시작하고 어떤 절차로 진행할지 모델에 설명 |
| 전문 에이전트 | `agents/*.md` | 역할, 사용할 도구, 검토 절차 등 위임용 정의 |
| 규칙 | `rules/` | 선택한 언어·프로젝트의 상시 지침 |
| 훅 | `hooks/hooks.json`, `scripts/hooks/` | 호스트의 생명주기·도구 이벤트에 연결한 실행 코드 |
| 지속 상태 | 세션 요약, 관찰·instinct, Memory Vault | 서로 다른 목적과 범위의 기억 자료 |

예를 들어 `tdd-workflow` 스킬은 실패하는 테스트를 먼저 쓰고 수정 후 검증하는 절차를 담고 있습니다. `code-reviewer` 파일은 변경 범위를 모은 뒤 주변 코드와 호출 관계를 읽고 신뢰할 수 있는 문제만 보고하라고 지시합니다. 이 두 파일은 **작업을 수행하는 모델의 안내서**입니다. 별도로 훅 코드가 존재한다고 해서 모든 스킬의 모든 문장이 강제 실행되는 것은 아닙니다. [TDD 스킬](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/skills/tdd-workflow/SKILL.md#L13-L49) · [리뷰 에이전트](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/agents/code-reviewer.md#L19-L37)

## 아키텍처와 디렉터리 구조

CLI, 호스트별 배포 형식, 실행 훅을 구분해 읽는 편이 좋습니다. `package.json`의 `ecc`와 `ecc-universal` 실행 진입점은 `scripts/ecc.js`입니다. 이 파일의 명령 표가 `setup`, `install`, `profile`, `memory` 등을 각 스크립트에 연결합니다. 반면 Claude 플러그인 메타데이터는 skills·commands 경로와 훅 활성화 옵션을 선언합니다. [CLI 진입점](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/package.json#L520-L526) · [명령 표](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/scripts/ecc.js#L9-L53) · [플러그인 메타데이터](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/.claude-plugin/plugin.json#L25-L45)

![에이전트 호스트 아래에 모델용 지침, 이벤트 훅 실행, 지속 상태를 구분한 ECC 구조]({{ '/img/reviews/2026/ecc-agent-harness-review/ecc-layers.svg' | relative_url }})

리뷰어 작성, 분석 커밋 기준. 호스트는 모델·도구 실행을 맡고, ECC는 지침과 이벤트 처리 및 지속 상태를 제공합니다. [지침 정의](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/skills/tdd-workflow/SKILL.md#L13-L49) · [훅 등록](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/hooks/hooks.json#L137-L179) · [메모리 CLI](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/scripts/memory.js#L456-L479)
{: .caption}

| 경로 | 이 글에서 확인한 책임 |
| --- | --- |
| `.claude-plugin/` | Claude 플러그인의 구성 경로와 사용자 옵션 |
| `hooks/hooks.json` | `PreToolUse`, `SessionStart`, `PostToolUse`, `Stop` 등의 등록 |
| `scripts/lib/hook-flags.js` | 훅 전체 활성화·개별 제외·프로필 판정 |
| `scripts/hooks/posttooluse-dispatcher.js` | 도구별 동기·비동기 후처리 선택과 출력 병합 |
| `scripts/hooks/session-start.js`, `session-end.js` | 이전 세션 자료의 선별 주입과 현재 세션 요약 저장 |
| `skills/continuous-learning-v2/` | 관찰 기록과 선택적으로 켜는 observer·instinct 흐름 |
| `scripts/memory.js`, `scripts/lib/memory-vault.js` | 호스트 사이에서 공유하는 Markdown 메모리의 저장·검색 |

Node.js 최소 요구 버전은 18이며, 패키지 의존성에는 TOML·YAML 파싱, 스키마 검증, SQL.js 등이 포함됩니다. 다만 여기서 따라가는 지속 학습 관찰 경로는 별도로 Bash와 Python을 사용합니다. Node 패키지 설치 조건과 모든 선택 기능의 실행 조건을 같은 것으로 보면 안 됩니다. [패키지 의존성과 엔진](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/package.json#L570-L605) · [관찰 실행기](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/scripts/hooks/observe-runner.js#L95-L138)

## 작동 원리

### 1. 훅 등록과 실제 실행 사이에 게이트가 있습니다

**훅**은 에이전트 호스트가 특정 사건에서 호출하는 프로그램입니다. 예를 들어 파일을 편집한 직후 `PostToolUse` 이벤트가 오면, ECC는 도구 이름과 현재 프로필에 맞는 후처리를 고릅니다. 기준 커밋은 `PostToolUse`를 동기·비동기 두 진입점으로 모았고, 내부 목록에 각 훅의 ID, 도구 매칭 조건, 허용 프로필, 구현 함수를 저장합니다. [이벤트 등록](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/hooks/hooks.json#L158-L179) · [후처리 목록](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/scripts/hooks/posttooluse-dispatcher.js#L35-L70)

그중 `post:quality-gate`는 `Edit|Write|MultiEdit`에, `post:observe:continuous-learning`은 모든 도구에 연결됩니다. 둘 다 `standard,strict` 프로필에서 선택됩니다. 프로필 게이트는 다음 순서로 판단합니다.

1. 전체 훅 활성화 여부를 확인합니다. 환경변수, 플러그인 옵션, 관리 설정의 순서로 값을 찾습니다.
2. 개별 훅 ID가 제외 목록에 있는지 확인합니다.
3. `minimal`, `standard`, `strict` 중 현재 프로필이 그 훅의 허용 목록에 있는지 봅니다.

잘못된 프로필 문자열은 `standard`로 돌아갑니다. 이 판정은 모델에게 부탁하는 문장이 아니라 실제 JavaScript의 분기입니다. [옵션 우선순위](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/scripts/lib/hook-flags.js#L65-L98) · [실행 판정](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/scripts/lib/hook-flags.js#L122-L139)

아래는 같은 흐름을 설명하기 위해 줄인 **리뷰어 작성 의사코드**입니다. 실제 dispatcher는 여러 출력의 병합과 차단 결정도 처리합니다.

```text
입력: 도구 이벤트의 원문 JSON, 해당 단계의 훅 목록
도구 이름을 추출한다
각 훅에 대해:
    도구 이름 또는 프로필이 맞지 않으면 건너뛴다
    dry-run이면 실행 예정 정보를 기록하고 건너뛴다
    훅에 원문 입력과 실행 문맥을 전달한다
    표준 출력·진단·종료 코드를 모은다
출력: 병합한 훅 응답과 종료 상태
```

입력·선택·출력 근거는 [`runHooks`](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/scripts/hooks/posttooluse-dispatcher.js#L237-L285)입니다. 여기서 원문 JSON을 그대로 돌려주는 후처리 결과는 중복 기록을 피하도록 빈 표준 출력으로 정규화합니다. 다른 훅이 실제로 반환한 추가 문맥이나 구조화된 차단 결정은 별도 경로로 다룹니다. [출력 정규화](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/scripts/hooks/posttooluse-dispatcher.js#L118-L145) · [차단 결정 병합](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/scripts/hooks/posttooluse-dispatcher.js#L153-L199)

모든 이벤트가 같은 실행기를 거치는 것은 아닙니다. 일반 훅의 `run-with-flags.js`는 소스에서 `run` 내보내기 문법을 검사하고, 실제 함수가 있으면 `await run()`으로 실행합니다. 해당 함수가 예외를 던지는 경로는 진단과 종료 코드 0을 반환하는 반면, 이전 방식의 별도 Node 하위 프로세스가 실행 오류·신호 종료·종료 상태 누락을 겪으면 코드 1을 반환합니다. 입력이 잘렸을 때 GateGuard·MCP 상태 검사처럼 지정된 일부 훅은 설정 조건에 따라 코드 2로 막습니다. 이처럼 **허용·차단의 의미는 훅과 실패 경로마다 확인해야 합니다.** [실행 방식 선택](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/scripts/hooks/run-with-flags.js#L253-L345) · [잘린 입력 처리](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/scripts/hooks/run-with-flags.js#L127-L149)

### 2. `quality-gate`라는 이름만으로 전체 검증을 가정하면 안 됩니다

`quality-gate.js`가 읽는 핵심 입력은 `tool_input.file_path`입니다. 파일 확장자와 프로젝트의 포매터 설정을 보고 Biome, Prettier, gofmt, Ruff 같은 검사를 고릅니다. 예를 들어 Python 경로에서는 `ruff format --check <file>`을 구성하며, 수정 모드를 명시하면 `--check`를 빼고 포맷을 수행합니다. 도구가 없거나 언어·설정에 맞지 않는 경로는 건너뜁니다. [확장자별 분기](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/scripts/hooks/quality-gate.js#L61-L136)

이 구현의 `strict` 변수는 검사 실패 시 진단 문구를 출력하는 데 쓰입니다. `run()`은 예외를 삼키고 원래 입력을 반환하며, dispatcher의 문자열 결과 정규화는 종료 코드 0을 부여합니다. 따라서 **이 파일의 품질 검사를 모든 테스트를 통과해야 다음 단계로 넘어가는 강제 장벽으로 해석할 수는 없습니다.** 별도의 Stop 검사나 보안 훅의 차단 동작과도 구분해야 합니다. [반환값](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/scripts/hooks/quality-gate.js#L139-L173) · [정규화](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/scripts/hooks/posttooluse-dispatcher.js#L118-L145)

짧은 원본 코드에서도 이 경계가 드러납니다. 아래는 MIT 코드의 해당 함수 마지막 부분만 발췌했습니다. Copyright (c) 2026 Affaan Mustafa. [원본 `run`](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/scripts/hooks/quality-gate.js#L145-L153) · [라이선스](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/LICENSE#L1-L21)

```javascript
  } catch {
    // Ignore parse errors.
  }
  return rawInput;
```

이 차이는 실용적입니다. “훅이 연결됐다”는 사실과 “원하는 품질 조건이 강제로 적용된다”는 사실은 각각 확인할 대상입니다. 이 글은 전체 GateGuard·Stop 검사군의 보안·차단 완전성을 검증한 결과를 제시하지 않습니다.

### 3. 세션을 이어 가는 기억은 요약 파일입니다

`session-end.js`라는 파일명과 실제 이벤트부터 맞춰 볼 필요가 있습니다. 기준 `hooks.json`에서 이 파일은 **`Stop`에 등록**돼 있습니다. 응답이 끝날 때 요약을 갱신하는 코드이며, 실제 `SessionEnd`에는 별도의 `session-end-marker.js`가 연결됩니다. [Stop 등록](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/hooks/hooks.json#L203-L284) · [SessionEnd 등록](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/hooks/hooks.json#L286-L297)

`session-end.js`는 대화 기록인 JSONL을 읽고, 사용자 메시지의 앞 200자씩을 모은 뒤 마지막 10개를 남깁니다. 사용 도구는 최대 20개, 수정한 파일은 최대 30개로 정리합니다. 프로젝트·브랜치·worktree·저장소 식별자를 헤더에 적고 날짜와 세션 식별자를 포함한 `*-session.tmp`에 저장합니다. 이미 파일이 있으면 생성된 요약 블록을 교체합니다. [기계적 추출](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/scripts/hooks/session-end.js#L55-L110) · [프로젝트 메타데이터](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/scripts/hooks/session-end.js#L136-L144) · [저장 경로](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/scripts/hooks/session-end.js#L307-L349)

항상 새 모델을 호출하는 구조도 아닙니다. 문맥 잔여 예산이 설정 임계값보다 작거나, 기본 50개 사용자 메시지 주기에 해당할 때 풍부한 LLM 요약을 시도합니다. 생성이 건너뛰어지거나 실패하면 기계적 추출 결과를 유지합니다. 요약 전용 하위 프로세스에는 재귀 저장을 막는 별도 표시도 있습니다. [선택적 LLM 요약](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/scripts/hooks/session-end.js#L222-L251) · [내부 요약 세션 제외](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/scripts/hooks/session-end.js#L310-L317)

다음 `SessionStart`는 여러 요약 중 하나를 골라 문맥에 넣습니다. 선택 순서는 다음과 같습니다.

| 우선순위 | 조건 |
| --- | --- |
| 1 | 기록된 worktree와 현재 경로의 실제 파일시스템 경로가 일치 |
| 2 | 같은 Git 공통 저장소 식별자에 속함 |
| 3 | worktree·저장소 필드가 없는 오래된 파일에 한해 프로젝트 이름이 일치 |
| 없음 | 조건에 맞는 파일이 없으면 다른 프로젝트의 최신 요약을 대신 넣지 않음 |

이 순서 덕분에 “가장 최근 파일”이 엉뚱한 저장소에서 나온 경우를 걸러낼 수 있습니다. 요약을 주입할 때는 과거 대화의 동결된 참고 자료이며 현재 지시로 재실행하지 말라는 경계 문구로 감쌉니다. 이 역시 모델이 참고할 문맥이지 Git 상태를 대신하는 완료 증명은 아닙니다. [선택 알고리즘](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/scripts/hooks/session-start.js#L292-L368) · [과거 자료 표시](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/scripts/hooks/session-start.js#L697-L745)

### 4. 관찰 기록과 자동 패턴 추출은 두 단계입니다

지속 학습 v2는 도구 실행 전후의 입력·출력을 프로젝트별 `observations.jsonl`에 기록하고, observer가 반복 패턴을 읽어 **instinct**라는 작은 행동 지침으로 저장하는 방식입니다. instinct는 트리거, 행동, 신뢰도, 근거, 범위를 가진 문서입니다. 이 경로에서 모델 가중치를 업데이트하는 것은 아닙니다. [스킬의 자료 형식](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/skills/continuous-learning-v2/SKILL.md#L48-L79)

![도구 이벤트를 관찰 파일에 기록하고 선택적으로 observer를 켜 instinct를 만들어 다음 세션에 선별 주입하는 과정]({{ '/img/reviews/2026/ecc-agent-harness-review/ecc-learning-flow.svg' | relative_url }})

리뷰어 작성, 분석 커밋 기준. 관찰 저장과 observer의 패턴 추출은 별도 단계이며, observer는 기본 비활성입니다. [관찰 저장](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/skills/continuous-learning-v2/hooks/observe.sh#L407-L482) · [기본 설정](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/skills/continuous-learning-v2/config.json#L1-L8) · [주입 순위](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/scripts/hooks/session-start.js#L469-L529)
{: .caption}

이 흐름은 조건을 갖습니다. `observe-runner.js`가 Bash 경로를 찾지 못하면 기록을 건너뛰며, `observe.sh`는 Python을 필요로 합니다. 스크립트는 알려진 자동 세션·하위 에이전트·제외 경로를 거르고, `minimal` 프로필이나 `ECC_SKIP_OBSERVE=1`이면 관찰을 건너뛰고 반환합니다. `disabled` 표시 파일로 관찰 자체를 멈추는 경로도 있습니다. 그러므로 스킬 문서의 “100% reliable” 표현은 이 정적 분석으로 입증한 수치가 아닙니다. [실행기 조건](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/scripts/hooks/observe-runner.js#L95-L138) · [관찰 제외 조건](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/skills/continuous-learning-v2/hooks/observe.sh#L180-L224) · [문서의 표현](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/skills/continuous-learning-v2/SKILL.md#L37-L45)

기록할 때는 타임스탬프·도구·세션·프로젝트를 넣고, 입력과 출력에서 알려진 비밀 문자열 패턴을 제거합니다. 코드 주석도 이것이 방어의 한 겹이며 임의의 모든 민감 내용을 제거한다는 보장이 아니라고 설명합니다. 로컬 파일에 기록한다는 저장 위치와 이후 모델이 그 파일을 읽는다는 처리는 나누어 봐야 합니다. [관찰 레코드](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/skills/continuous-learning-v2/hooks/observe.sh#L407-L424) · [입출력 기록](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/skills/continuous-learning-v2/hooks/observe.sh#L468-L482)

핵심은 **observer의 기본값이 `false`**라는 점입니다. 수집 훅이 켜져 있어도 백그라운드 분석이 자동으로 활성화된다고 볼 수 없습니다. launcher는 설정에서 활성화를 확인한 뒤 시작하며, 분석 루프는 반복 관찰에서 사용자 수정·오류 해결·반복 작업 등을 찾으라는 프롬프트를 구성합니다. 기준 구현은 기본 Haiku 모델의 Claude CLI를 Read·Write 도구로 호출합니다. 이는 데이터가 로컬에 저장되는 것과 별개로 모델 제공 경로의 실행·비용을 수반할 수 있는 단계입니다. [기본 설정](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/skills/continuous-learning-v2/config.json#L1-L8) · [시작 조건](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/skills/continuous-learning-v2/agents/start-observer.sh#L79-L111) · [프롬프트](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/skills/continuous-learning-v2/agents/observer-loop.sh#L268-L315) · [Claude 호출](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/skills/continuous-learning-v2/agents/observer-loop.sh#L391-L401)

observer 프롬프트는 같은 패턴을 3회 이상 관찰했을 때 근거를 담은 instinct를 작성하라고 요청하고, 빈도에 따라 신뢰도를 제안합니다. 이 빈도 기반 값은 프롬프트 규칙이지 통계적으로 보정된 정확도 측정치는 아닙니다. 패턴이 없어도 분석 완료 표시는 반환하도록 설계돼 있어, 분석 한 번이 곧 새로운 교훈 한 개를 의미하지 않습니다. [작성 조건과 완료 계약](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/skills/continuous-learning-v2/agents/observer-loop.sh#L271-L314)

### 5. 다음 세션에 모든 기억을 넣지는 않습니다

`SessionStart`의 instinct 수집은 프로젝트 범위와 전역 범위의 자료를 합친 뒤, 기본 **신뢰도 0.7** 미만을 제외합니다. 같은 ID라면 프로젝트 자료를 우선합니다. 이후 신뢰도에 프로젝트·기술 스택 관련성 보정을 더해 정렬하고 기본 **6개**까지만 선택합니다. 세션이 시작할 때는 아직 새 사용자 과제가 없으므로 이 관련성은 질문 임베딩 검색이 아니라 위치·기술 스택을 이용한 선별입니다. [기본값](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/scripts/hooks/session-start.js#L38-L43) · [선별·순위 코드](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/scripts/hooks/session-start.js#L469-L529)

선택한 instinct의 행동 문장, 이전 세션 요약, 학습된 스킬의 요약은 `additionalContext`로 묶입니다. 전체 문맥의 기본 상한은 8,000자이며 설정에 따라 끄거나 줄일 수 있습니다. 최종 출력은 `hookSpecificOutput.hookEventName = SessionStart`와 `additionalContext`를 담은 JSON입니다. **저장된 자료를 제한된 문맥으로 번역하는 단계**가 분명하게 존재합니다. [문맥 활성화](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/scripts/hooks/session-start.js#L648-L688) · [합성과 출력](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/scripts/hooks/session-start.js#L805-L821)

### 6. Memory Vault는 이와 별도로 쓰는 공유 문서 저장소입니다

Memory Vault의 목적은 Claude·Codex 등 서로 다른 호스트가 이해할 수 있는 Markdown 기억과 인계 문서를 남기는 것입니다. 기본 프로젝트·팀 경로는 `.ecc/memory/project`, `.ecc/memory/team`, 사용자 경로는 `~/.ecc/memory`입니다. CLI의 `save`, `handoff`, `search`, `read`, `doctor`가 공통 라이브러리를 호출합니다. 자동 세션 요약 파일이나 `observations.jsonl`을 모두 하나의 파일로 합치는 코드로 이해하면 안 됩니다. [저장 루트](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/scripts/lib/memory-vault.js#L59-L95) · [명령 분기](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/scripts/memory.js#L404-L479)

`handoff`는 보내는 호스트와 받을 대상을 필수로 확인합니다. 본문 입력과 메타데이터가 `saveMemory()`에 전달되면 새 메모리는 `trust: unreviewed`, `status: active`로 정규화됩니다. 알려진 비밀 패턴을 발견하면 저장을 거절하고, 파일은 새로 만들기만 허용해 같은 ID 덮어쓰기를 막습니다. 이 값은 문서를 생성한 도구가 자기 결과를 검토 완료로 올리는 일을 막는 경계입니다. [인계 입력](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/scripts/memory.js#L379-L424) · [저장 구현](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/scripts/lib/memory-vault.js#L296-L343)

검색은 확인한 경로에서 **문자열 기반 점수화**입니다. 제목·본문의 전체 문구와 질의 토큰을 비교하고, 제목 일치는 토큰당 8점, 태그는 6점, 메타데이터는 3점, 본문 출현은 토큰당 최대 5점을 더합니다. 활성 상태·종류·신뢰 상태·대상 호스트를 필터링하고, 점수·수정 시각·ID 순으로 정렬한 뒤 상위 결과의 요약을 돌려줍니다. 다음은 원본 점수 계산의 일부입니다. MIT, Copyright (c) 2026 Affaan Mustafa. [점수 함수](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/scripts/lib/memory-vault.js#L555-L577) · [검색 필터와 출력](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/scripts/lib/memory-vault.js#L602-L665) · [라이선스](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/LICENSE#L1-L21)

```javascript
      + (title.includes(token) ? 8 : 0)
      + (tags.includes(token) ? 6 : 0)
      + (metadata.includes(token) ? 3 : 0)
      + Math.min(countOccurrences(body, token), 5)
```

기본 검색은 `trust` 필터가 지정되지 않으면 `unreviewed` 자료도 결과에 포함할 수 있습니다. 생성 시의 신뢰 표시는 검토 완료를 스스로 부여하지 못하게 하는 메타데이터이며, 미검토 내용을 자동으로 차단하는 검색 장벽은 아닙니다. [선택적 신뢰 필터](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/scripts/lib/memory-vault.js#L618-L635)

이는 벡터 임베딩이나 학습된 재순위 모델의 결과가 아닙니다. 같은 “기억”이라는 이름 아래에서도 검색 가능한 인계 문서, 다음 세션 요약, 행동 지침 후보는 다른 자료 구조와 생명주기를 가집니다.

| 기억 계층 | 저장하는 내용 | 다시 읽는 시점·경로 |
| --- | --- | --- |
| 세션 요약 | 과제, 도구, 수정 파일, 프로젝트 정보 | 다음 시작 시 일치하는 세션을 선별 |
| 관찰·instinct | 도구 이벤트와 반복 행동 지침 | 선택적 observer 분석 후 시작 문맥에서 선별 |
| Memory Vault | 출처 호스트·대상·범위가 붙은 문서 | CLI 또는 선택적으로 연결한 MCP를 통한 검색·읽기 |

## 설치와 사용

아래 명령은 기준 커밋의 README에 있는 사용법입니다. 이 리뷰에서는 실행하지 않았습니다. 문서는 Node.js 18 이상, Claude 플러그인 경로에는 Git과 Claude Code 2.1 이상을 요구하며, 가이드형 설치와 네이티브 플러그인 경로 중 하나를 선택하라고 설명합니다. [요구사항](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/README.md#L165-L178) · [중복 설치 경고](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/README.md#L268-L278)

```bash
npx ecc-universal@2.2.3 setup
```

위 명령은 패키지를 받아 코드를 실행하는 설치 명령입니다. 버전 번호를 고정한 예시이지 이 분석 커밋의 소스와 npm 배포물 사이의 무결성을 확인한 결과는 아닙니다. 네이티브 Claude Code 경로를 택하는 경우 README의 명령은 다음과 같습니다. [가이드형 설치 설명](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/README.md#L211-L224) · [네이티브 설치](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/README.md#L286-L299)

```text
/plugin marketplace add https://github.com/affaan-m/ECC
/plugin install ecc@ecc
```

rules는 Claude 플러그인으로 배포되지 않으므로 README는 필요한 규칙 묶음을 별도로 추가하도록 안내합니다. 플러그인 훅을 다시 `settings.json`에 복사하는 중복 등록도 피하라고 명시합니다. 기능을 채택할 때에는 같은 저장소라도 **지침 설치, 런타임 설치, 호스트별 훅 지원**을 각각 확인해야 합니다. [규칙 추가](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/README.md#L301-L311) · [훅 중복 주의](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/README.md#L585-L598)

Memory Vault도 플러그인만 설치했다고 CLI가 PATH에 생기지는 않습니다. README는 별도의 npm 런타임 설치 뒤 초기화·검색·진단을 설명합니다. 다음은 그대로 인용한 명령이며, 이 글의 실행 결과는 아닙니다. [Memory Vault 사용법](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/README.md#L1266-L1279)

```bash
npm install -g ecc-universal@2.2.3
ecc memory init --scope project
ecc memory search "authentication migration" --target-harness codex
ecc memory doctor
```

## 한계와 주의점

지원 범위는 호스트와 운영체제에 따라 다릅니다. README는 Claude Code를 주 기준으로 삼고, Codex의 네이티브 훅에는 명시적 신뢰 결정이 필요하며 Claude의 훅 프로필을 그대로 사용하지 않는다고 설명합니다. GitHub Copilot Chat은 지침 중심이고 ECC 훅은 이식되지 않았습니다. 모든 도구가 같은 이름의 스킬 파일을 읽을 수 있다는 사실과 동일한 실행 기능을 제공한다는 사실은 다릅니다. [호스트별 표](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/README.md#L1332-L1342) · [기능별 표](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/README.md#L1445-L1454)

지속 학습 문서의 설명과 실제 기본 설정도 함께 봐야 합니다. 관찰 훅의 활성화, Bash·Python 가용성, 자동 세션 제외, observer 활성화는 각각 별도 조건입니다. `quality-gate`의 이름 역시 전체 테스트 통과나 강제 차단을 보증하지 않습니다. 이 글에서 확인한 것은 해당 커밋의 분기·자료구조·호출 연결이며, 설치 성공률이나 비용 절감·생산성 향상의 벤치마크 결과는 아닙니다.

라이선스는 **MIT**입니다. 사용·수정·재배포를 허용하되 사본이나 중요한 부분에 저작권 고지와 허가 고지를 포함하도록 요구하며 보증을 제공하지 않습니다. 위의 짧은 코드 인용은 이 조건에 따른 원본 위치와 저작권·라이선스를 함께 표시했습니다. 도식 두 장은 원본 이미지를 옮긴 것이 아니라 확인한 코드를 바탕으로 리뷰어가 새로 작성했습니다. [MIT 라이선스](https://github.com/affaan-m/ECC/blob/3f14a103a8694e51c1df9a806217a6d0b5f7a6f7/LICENSE#L1-L21)

## 결론

ECC에서 배울 부분은 스킬의 개수보다 **절차와 실행, 기록과 재사용의 연결 방식**입니다. 스킬·에이전트 파일은 모델의 작업 절차를 설명하고, 훅은 호스트 이벤트를 받아 조건에 맞는 코드를 실행합니다. 세션 요약과 instinct는 필요한 일부만 다음 문맥으로 돌아오며, Memory Vault는 별도 문서 저장·검색 경로를 제공합니다. 따라서 특정 기능을 이해하려면 “입력은 어디에서 오고, 어떤 게이트를 지나며, 무엇을 출력하는가”를 실제 코드에서 이어 읽어야 합니다.

이 글에서 다루지 못한 부분: 선택적 설치 플래너와 적용기의 전체 복구·제거 동작, GateGuard·AgentShield 전 검사군, 다중 worktree 오케스트레이션, SQLite 운영 대시보드, 각 호스트 어댑터와 전체 스킬·에이전트 카탈로그는 상세 분석 범위에서 제외했습니다. 이들이 이 글에서 검증된 것으로 확대 해석하지 않았습니다.
