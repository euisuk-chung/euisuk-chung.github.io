---
type: "Repo Review"
title: "[Repo Review] AutoHarness: Claude Code의 경험을 스킬로 저장하고 관리하는 구조"
description: "Claude Code 세션에서 교훈을 추출하고 MCP 제안 큐와 자동 검사를 거쳐 스킬로 반영하는 흐름, 사용량 기반 생명주기와 구현상 경계를 분석합니다."
date: "2026-10-01"
tags:
  - "Repo Review"
  - "Claude"
  - "Anthropic"
  - "AI Agent"
  - "MCP"
resource: "https://github.com/tigerless-labs/autoharness/tree/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b"
generated:
  by: "process:blog-review"
  at: "2026-10-01T11:11:38+09:00"
sources:
  - id: "github:tigerless-labs/autoharness"
    resource: "https://github.com/tigerless-labs/autoharness/tree/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b"
    title: "AutoHarness"
    author: "Tigerless Labs"
    last_modified: "2026-09-30T16:19:59+08:00"
status: "stable"
year: "2026"
analyzed_at: "2026-10-01T11:11:38+09:00"
source_id: "tigerless-labs/autoharness"
source_revision: "7f725a94172e6c5e8f1f6305c9234e4c0c45d32b"
source_type: "repo"
source_url: "https://github.com/tigerless-labs/autoharness/tree/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b"
visual_sources:
  - path: "/img/reviews/2026/autoharness-review/learning-loop.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/hook/spawn.py#L111-L129"
    caption: "리뷰어 작성, 분석 커밋 기준. 기본 bundle 경로의 제안과 자동 반영 흐름."
  - path: "/img/reviews/2026/autoharness-review/lifecycle.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/lib/lifecycle.py#L21-L41"
    caption: "리뷰어 작성, 분석 커밋 기준. 졸업 심사를 켠 기본 상태의 스킬 생명주기."
---

## 들어가며: 같은 실수를 반복하지 않으려면

코딩 에이전트에게 잘못된 명령을 고쳐 주거나 프로젝트의 작업 순서를 설명해도, 다음 세션에서 그 경험이 바로 재사용되지는 않습니다. 경험을 문서로 남기는 것만으로도 부족합니다. 기존 규칙과 중복되지 않아야 하고, 필요할 때 발견되어야 하며, 오래된 규칙은 정리되어야 합니다.

AutoHarness는 이 문제를 **Claude Code 세션에서 재사용할 교훈을 추출해 네이티브 스킬 파일로 저장하고, 이후 사용 흔적에 따라 그 스킬을 관리하는 플러그인**으로 풉니다. 여기서 “학습”은 모델 가중치의 학습이 아니라 `SKILL.md`와 지원 파일을 바꾸는 과정입니다. 프로젝트가 내세우는 것은 경험 추출·병합·재호출·정리의 순환입니다. [프로젝트 정의](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/README.md#L8-L24)

README 첫머리의 CORE-Bench **42% → 78%**는 HAL 연구를 인용해 harness의 중요성을 설명하는 수치입니다. AutoHarness를 설치하면 같은 개선이 나온다는 자체 벤치마크 결과로 읽으면 안 됩니다. README도 별도 평가 점수보다 실제 사용을 생존 신호로 삼는다고 설명합니다. 이 글은 HAL의 실험을 재검토하거나 AutoHarness의 성능을 측정하지 않고, **v0.5.3의 고정 커밋에서 어떤 데이터가 들어와 어떤 파일로 남는지**를 정적으로 추적합니다. [수치의 인용 위치](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/README.md#L13-L24), [버전](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/.claude-plugin/plugin.json#L1-L10)

## 무엇을 만들고, 어디에 저장하는가

스킬은 이름·설명과 본문을 가진 `SKILL.md`입니다. 필요하면 `references/`, `scripts/`, `templates/`, `assets/`를 함께 둡니다. AutoHarness는 여기에 생성 이유와 증거를 담는 `.ledger.jsonl`, 사용 횟수 등을 담는 `.sidecar.json`, 비식별화된 증거 조각을 덧붙입니다. 호스트가 읽을 지침과 운영용 기록을 분리하는 구성입니다. [저장 과정](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/hook/promoter.py#L75-L142)

| 계층 | 스킬 위치 | 운영 상태 위치 | 의도 |
|---|---|---|---|
| Project | 프로젝트의 `.claude/skills/` | `.claude/autoharness/` | 해당 코드베이스의 규칙·경험 |
| Global | `~/.claude/skills/` | `~/.claude/autoharness/` | 여러 프로젝트에서 재사용할 선호·기법 |

경로 결정은 `layer.py`에 모여 있습니다. 연결된 Git worktree에서 실행하면 project root를 주 worktree로 돌려 같은 저장소의 스킬과 상태를 공유합니다. 일반 저장소의 하위 디렉터리까지 무조건 저장소 최상위로 올리는 구현은 아닙니다. 이 차이는 격리된 작업 디렉터리를 쓸 때 중요합니다. [경로 결정](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/lib/layer.py#L36-L83)

## 아키텍처: 생성 판단과 파일 반영을 나눕니다

플러그인은 Python 3.11 이상을 요구하며, README는 런타임 Python 서드파티 의존성이 없다고 설명합니다. hook은 `python3 -m autoharness.hook.dispatch`, MCP 서버는 `python3 -m autoharness.stage_skill.server`로 진입합니다. 따라서 일반 Python 라이브러리를 호출하는 예제보다 **Claude Code 플러그인 이벤트와 별도 Claude 자식 프로세스의 연결**이 핵심입니다. [설치 조건](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/README.md#L26-L42), [hook 등록](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/hooks/hooks.json#L1-L16), [MCP 등록](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/.mcp.json#L1-L14)

| 구성 | 입력과 책임 | 다음 단계 |
|---|---|---|
| `dispatch` / `on_stop` | 호스트 이벤트 수신, 도구 호출 카운트와 반성 시작 판정 | 분리된 `spawn` 프로세스 |
| `capture` | 이전 바이트 위치 이후 세션 로그, 크기 제한과 비식별화 | episode window와 과거 문맥 digest |
| `reflector` | 에피소드·기존 스킬 목록·작성 규격으로 교훈 판단 | `stage_skill` 제안 |
| `stage_skill` | MCP 입력 구조 검사, run별 JSONL 큐에 추가 | 아직 live skill은 불변 |
| `promoter` | 완성 본문 재구성, 정책 검사, 파일 반영 | 스킬·증거·장부·실행 결과 |
| `on_session_start` | 사용량 기반 보관 결정과 스킬 인덱스 생성 | 다음 세션의 추가 문맥 |
| `curator` | 전체 관리 스킬을 읽고 유사 항목 통합 제안 | 같은 staging·promoter 경로 |

![세션 도구 호출부터 경험 추출, 제안 큐, 자동 검사와 스킬 저장까지 이어지는 흐름]({{ '/img/reviews/2026/autoharness-review/learning-loop.svg' | relative_url }})

*리뷰어 작성, 분석 커밋 기준. 기본 `bundle` 경로를 그렸습니다. “검사 통과”는 프로그램의 자동 판정이며 사용자의 개별 승인 단계가 아닙니다. [이벤트 분기](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/hook/dispatch.py#L111-L158), [자식 실행과 반영](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/hook/spawn.py#L111-L129)*

## 작동 원리: 이벤트에서 다음 세션의 스킬까지

### 1. 도구 호출을 세고, 턴이 끝날 때 반성을 시작합니다

`PreToolUse`에서 주 세션의 도구 호출마다 session counter를 증가시킵니다. `Stop` 이벤트가 오면 project/global 요청 카운터를 각각 증가시키고, 수동 `/learn` 등이 남긴 `interactive` 제안을 먼저 반영합니다. 이어 `on_stop`이 session counter를 읽어 기본 임계값 50 이상이면 초기화하고 반성을 시작하도록 반환합니다. 즉, **50개 도구 호출이 쌓이는 순간 턴을 끊는 것이 아니라 그 턴이 끝날 때** 후속 작업을 시작합니다. [dispatch](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/hook/dispatch.py#L119-L155), [임계값 판정](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/hook/on_stop.py#L17-L31)

여기에는 서로 다른 두 단위가 있습니다. 반성 cadence는 도구 호출 수이고, 스킬 생명주기 분모는 `Stop`을 통해 증가하는 요청 수입니다. 도구를 호출하지 않는 대화도 후자에는 들어갑니다. `SessionEnd`는 임계값 미만의 도구 호출이 남아 있으면 마지막 반성을 요청하고 session counter를 제거합니다. 자식 프로세스에는 별도 환경 표시를 넣어 자식의 종료가 다시 반성을 낳는 재귀를 막습니다. [종료 처리](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/hook/on_session_end.py#L16-L29), [자식 환경](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/hook/spawn.py#L99-L104)

README는 curator의 기본 250도 같은 도구 호출 단위로 설명하지만, **이 커밋의 dispatcher는 `Stop`마다 증가하는 `pcount`가 250의 배수인지 검사**합니다. 설정 이름만 보고 반성 5회마다 통합이 돈다고 계산할 수 없습니다. 다음은 해당 구현의 연속된 두 줄입니다. [README 설정](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/README.md#L98-L103), [실제 조건](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/hook/dispatch.py#L129-L130)

```python
            if config.CONSOLIDATE_EVERY_N and pcount % config.CONSOLIDATE_EVERY_N == 0:
                curate(_curate_run_id(event, pcount), roots)  # periodic content-level merge pass (rarer than reflection)
```

### 2. 에피소드는 원본 로그의 바이트 구간입니다

`capture.window`는 저장해 둔 offset부터 로그 끝까지 읽습니다. 각 줄은 기본 4,000바이트를 기준으로 자르고, window 전체는 기본 200,000바이트 한도 안에서 최근 부분을 남깁니다. 잘린 곳에는 표시를 추가하고 비식별화 규칙을 적용합니다. 이 값들은 원문을 온전히 보존한다는 보장이 아니라 **자식 문맥이 도구 출력으로 과도하게 커지는 것을 막는 예산**입니다. 원본 호스트 로그 자체를 수정하지는 않습니다. [window 처리](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/hook/capture.py#L21-L50), [기본값](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/config.py#L24-L30)

이전 문맥은 별도 digest로 들어갑니다. 기본 20개 사용자 교환을 기준으로 텍스트와 도구 이름을 축약하고 도구 결과는 제외합니다. 이 digest는 배경 이해용이며 reflector 지침은 그것을 증거로 인용하지 말라고 명시합니다. 새로운 교훈의 증거와 배경 요약을 구분하려는 설계입니다. [digest](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/hook/capture.py#L53-L105), [입력 지침](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/agents/reflector.md#L14-L24)

offset은 자식 실행과 큐 처리 뒤에 기록됩니다. window를 만드는 순간과 호스트의 로그 추가가 완벽하게 동기화된 트랜잭션은 아니며, 소스 주석도 transcript 상한 경쟁을 미해결 사항으로 남깁니다. 따라서 “세션의 각 사건을 정확히 한 번 학습한다”는 수준으로 확대 해석하지 않아야 합니다. [실행 순서](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/hook/spawn.py#L167-L180)

### 3. Reflector는 기존 스킬과 비교해 변경을 제안합니다

기본 `bundle` 경로는 비식별화된 window, digest, 두 계층의 기존 스킬 설명 목록, 작성 규격을 새 자식 세션에 전달합니다. reflector의 도구는 `Read`, `Grep`, `Glob`, `stage_skill`로 선언되고 모델은 `haiku`입니다. 해당 프로젝트의 구현 선택이며, AutoHarness가 부모 모델을 그대로 사용하는 기본값은 아닙니다. [bundle 구성과 명령](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/hook/spawn.py#L24-L54), [reflector 정의](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/agents/reflector.md#L1-L12)

reflector의 우선순위는 현재 참고한 스킬 수정 → 기존 상위 범주 스킬 수정 → 지원 파일을 포함한 갱신 → 새 스킬 생성입니다. 새 교훈이 이전 규칙과 충돌하면 이전 규칙도 같은 실행에서 고치도록 지시합니다. 다만 이런 의미적 판단은 **모델에 주어진 작성 정책**입니다. promoter가 두 문장의 의미적 모순이나 추출한 교훈의 진실성을 증명하는 것은 아닙니다. [비교·조정 지침](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/agents/reflector.md#L31-L42)

선택 가능한 `fork`는 `--resume`과 `--fork-session`으로 실제 대화를 이어받습니다. 기본 bundle처럼 별도의 window만 자식에게 보여 주는 경로가 아니므로 비식별화된 입력만 전달된다고 일반화할 수 없습니다. 두 경로 모두 CLI 명령에 `--dangerously-skip-permissions`가 들어갑니다. 기본 bundle은 agent 도구 제한과 hook 차단에 의존하며, fork는 원래 세션의 도구를 상속하므로 특히 경계를 따로 살펴야 합니다. [fork·bundle 명령](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/hook/spawn.py#L79-L97), [실제 분기](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/hook/spawn.py#L111-L127)

### 4. MCP staging은 저장 승인과 다릅니다

`stage_skill`은 다섯 동작을 받습니다. `create`는 새 본문과 계층, `update`는 전체 본문, `patch`는 기존 문자열과 바꿀 문자열, `remove_file`은 하위 경로, `delete`는 스킬 이름을 받습니다. 모든 제안에는 `reason`과 `evidence`가 필요합니다. 파일을 추가하는 경우 허용된 지원 디렉터리 안에 있어야 하며, 개수·크기와 본문 참조 관계도 검사합니다. [입력 구조](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/stage_skill/server.py#L24-L113)

staging 단계에서 오류를 모델에 바로 돌려주는 이유는 자식 세션이 살아 있는 동안 수정 기회를 주기 위해서입니다. 그러나 `ok: true`는 **큐에 들어갔다**는 뜻입니다. 최종 파일 반영은 자식 종료 후 promoter가 수행합니다. reflector 지침도 staging 결과만 보고 반영 성공을 주장하지 말라고 합니다. [즉시 검사](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/stage_skill/server.py#L116-L168), [결과 보고 지침](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/agents/reflector.md#L61-L63)

수동 `/learn` 역시 다른 저장 통로를 만들지 않습니다. 세션에서 교훈을 추출해 같은 MCP 도구로 제안하고, 전용 run id가 없는 입력은 `interactive` 큐에 들어간 뒤 주 세션의 `Stop`에서 처리됩니다. 사용자의 요청은 추출 시점을 지정하며, 개별 제안의 사람 승인 UI는 이 흐름에 없습니다. [learn 지침](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/skills/learn/SKILL.md#L1-L23), [기본 큐 선택](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/stage_skill/server.py#L204-L208)

### 5. Promoter가 완성 결과를 검사하고 저장합니다

`patch`는 live 본문의 `old_string`이 정확히 한 번 나타나야 합니다. 존재하지 않거나 여러 번 나오면 거절합니다. 계층을 지정하는 `create` 외의 수정은 project/global을 검색하며, 같은 이름이 양쪽에 있으면 모호하므로 거절합니다. [본문 재구성](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/hook/promoter.py#L52-L72), [조회와 치환](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/lib/skill_store.py#L48-L62)

완성된 본문에는 다음과 같은 결정적 검사가 적용됩니다. 여기서 결정적이라는 말은 같은 입력에 같은 규칙을 적용한다는 뜻이지, 모든 보안·품질 문제를 알아낸다는 뜻은 아닙니다. [검사 구현](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/lib/validate.py#L170-L221)

| 검사 축 | 확인하는 것 | 판정 범위 |
|---|---|---|
| 문자열 안전 검사 | 유출·명령 주입·파괴적 명령 등 정규식 패턴 | 의미적 안전성이나 실행 격리 아님 |
| 구조·완결성 | front matter, 이름·설명, 참조 파일, placeholder | 실제 작업 성공을 평가하지 않음 |
| 설명·본문 크기 | 새 작성의 설명 예산과 trigger cue, 본문 비공백 줄 수 | 짧다고 좋은 규칙이라는 보장은 없음 |
| 증거 장부 | reason/evidence 존재 | 증거가 원본의 진짜 부분 문자열인지 대조하지 않음 |
| Global 적합성 | 특정 절대 경로와 전달된 repo 이름 검사 | 모든 프로젝트 의존 표현을 이해하지 않음 |
| 수정 소유권 | 기존 수정 대상의 `created_by: agent` | create 경로는 별도 주의 필요 |

README는 스킬 설명의 1,024자 설정도 소개하지만 이 커밋의 `description_findings`는 새 create/update 설명에 **인덱스 예산인 기본 60자**를 적용합니다. 또한 `when` 또는 따옴표·백틱으로 감싼 표현을 trigger cue로 보는 영문 중심 휴리스틱입니다. 긴 설명이나 한국어 자연어만으로 만든 조건문이 예상과 다르게 거절될 수 있는 이유입니다. 본문은 기본 25개 비공백 줄로 제한하며 세부 근거를 지원 파일로 옮기도록 유도합니다. [설명 검사](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/lib/validate.py#L34-L83), [본문 제한](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/lib/validate.py#L189-L200)

통과하면 지원 파일 → 비식별화된 증거 파일 → `SKILL.md` → sidecar와 ledger 순서로 저장합니다. 증거 파일 이름은 내용 해시 일부로 정하고, `SKILL.md`는 임시 파일을 `fsync`한 뒤 `os.replace`로 교체합니다. **개별 파일이 반쯤 기록되는 것을 줄이는 원자적 교체**와 **여러 파일·여러 제안 전체의 트랜잭션**은 다릅니다. 전자는 구현되어 있지만 후자가 제공되는 것은 아닙니다. [저장 순서](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/hook/promoter.py#L86-L142), [원자적 파일 쓰기](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/lib/atomic.py#L13-L32)

`runs/<run-id>.json`은 성공·거절 결과를 남기고 `last_run.json`은 다음 SessionStart에서 한 번 표시할 요약을 만듭니다. 실패한 제안도 운영자가 볼 수 있도록 하는 점은, 성공한 스킬의 장부만 남기는 방식과 다릅니다. [실행별 기록](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/hook/promoter.py#L213-L246)

### 6. 다음 세션에서는 호출 기회와 사용 흔적으로 정리합니다

SessionStart는 먼저 관리 스킬의 sidecar를 모아 lifecycle을 평가하고, 보관할 항목을 `.archive`로 이동시킨 다음 남은 스킬의 인덱스를 만듭니다. 인덱스는 category별 설명 목록이며 호스트의 원래 스킬 탐색을 대체하지 않고 추가 문맥에 들어갑니다. [세션 시작](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/hook/on_session_start.py#L100-L130), [인덱스 구성](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/hook/on_session_start.py#L42-L65)

sidecar의 세 카운터는 의미가 다릅니다.

- **use**: `Skill` 도구를 호출하려 할 때 증가합니다. 생존 순위 계산의 분자입니다.
- **view**: 관리 스킬 디렉터리의 파일을 `Read`하려 할 때 증가합니다. 졸업 심사에서 무관심과 단순 열람을 구분합니다.
- **patch**: promoter가 update/patch를 반영할 때 증가합니다. 이후 use가 생기면 개선 뒤 재사용 세대를 기록합니다.

이들은 `PreToolUse`에서 관측하는 신호이므로 **도구 호출의 성공, 지침 준수, 최종 과제 성공을 직접 측정한 값은 아닙니다**. README의 adherence를 성능 검증과 같은 뜻으로 읽으면 안 되는 이유입니다. [카운터 연결](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/hook/on_skill_call.py#L47-L74), [sidecar 갱신](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/lib/sidecar.py#L47-L76)

생존 순위의 rate는 생성 시점 이후 해당 계층의 요청 수를 분모로 하고 use를 분자로 합니다. 닫혀 있는 노트북의 경과 시간은 분모를 증가시키지 않습니다. 기본 maturity는 project 100, global 300입니다. 미성숙 스킬은 보관 대상·용량 계산에서 빠지고, 성숙했는데 use와 view가 모두 0인 스킬은 졸업 심사에서 보관됩니다. use가 있는 스킬끼리는 project 50/global 20 용량을 넘을 때 낮은 rate부터 정리합니다. 같은 rate에서는 이름으로 순서를 고정합니다. [생명주기 전체 분기](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/lib/lifecycle.py#L17-L41), [기본값](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/config.py#L57-L65)

![미성숙 보호, use와 view를 이용한 졸업 심사, 용량 경쟁을 구분한 스킬 생명주기]({{ '/img/reviews/2026/autoharness-review/lifecycle.svg' | relative_url }})

*리뷰어 작성, 분석 커밋 기준. 기본 졸업 심사를 켠 상태입니다. view만 있고 use가 없는 성숙 스킬은 보존되지만 용량 경쟁 집합에는 들어가지 않습니다. [판정 코드](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/lib/lifecycle.py#L21-L41)*

따라서 README의 “인덱스는 두 용량 합을 넘지 않는다”는 설명은 이 구현에서 엄격한 총량 보장이 아닙니다. **미성숙 스킬과 view만 있는 성숙 스킬이 용량 계산에서 제외되지만 인덱스에는 포함**됩니다. 기본 50+20을 전체 live 스킬 또는 인덱스 줄 수의 상한으로 이해하면 틀립니다. [README의 상한 설명](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/README.md#L118-L123), [전체 live 관리 스킬 인덱싱](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/hook/on_session_start.py#L42-L65)

### 7. Curator는 전체 라이브러리의 의미적 중복을 정리합니다

reflector가 한 episode에서 얻은 교훈을 다룬다면 curator는 관리 중인 스킬 전체를 대상으로 좁은 스킬들을 상위 범주에 모읍니다. 사용량을 판단 기준으로 쓰지 않고 내용과 지원 파일까지 읽으라는 별도 지침이 있습니다. 한 스킬로 합친다는 것은 이름만 지우는 것이 아니라 필요한 하위 파일과 본문의 경로도 옮기는 작업입니다. [curator 지침](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/agents/curator.md#L9-L48)

시작 전에 두 skill tree를 압축 스냅샷으로 저장하고 계층별 기본 5개를 남깁니다. 다만 스냅샷 실패 예외를 잡아 통합 자체는 계속 진행하므로, **모든 통합 실행에 복구용 사본이 확보된다는 보장은 없습니다**. 제안은 같은 MCP와 promoter를 통과합니다. [스냅샷과 자식 실행](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/hook/spawn.py#L132-L164)

## 설치와 사용: 문서가 제공하는 경로

아래 두 명령은 고정 커밋 README의 Claude Code 입력창용 설치 명령입니다. 이 리뷰에서는 설치·실행하지 않았으며, 실행 시 받아오는 버전이 이 글의 분석 SHA로 고정되는 명령도 아닙니다. Python 3.11 이상이 `python3`로 잡혀 있어야 hook이 작동합니다. [설치 문서](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/README.md#L26-L48)

```text
/plugin marketplace add tigerless-labs/autoharness
/plugin install autoharness@autoharness
```

이후 `/reload-plugins` 또는 재시작으로 반영합니다. 작업 중 교훈을 바로 남기고 싶을 때는 `/learn`을 사용합니다. 설정은 `AUTOHARNESS_*` 환경 변수로 주며, README는 Claude Code 설정 파일의 `env` 예시를 제공합니다. 다음은 그 예시를 그대로 인용한 것입니다. [환경 설정](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/README.md#L126-L134)

```json
{ "env": { "AUTOHARNESS_REFLECT_EVERY_N": "10" } }
```

낮은 반성 임계값은 자식 Claude 실행을 더 자주 만들 수 있습니다. “Python 외부 의존성이 없다”는 설명이 추론 비용이 없다는 뜻은 아닙니다. 자식 호출은 실제 `claude -p` 실행이며, 이 글에서는 계정별 사용량·비용이나 지연을 측정하지 않았습니다. [자식 실행](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/hook/spawn.py#L90-L108)

문서상 관찰 지점은 project 상태 디렉터리의 `intents/`, `runs/`, `last_run.json`과 각 스킬의 숨김 sidecar·ledger입니다. 플러그인을 제거해도 이 파일들은 플러그인 캐시 밖에 남습니다. 따라서 제거와 학습 기록 삭제는 별개입니다. [상태 관찰](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/README.md#L168-L195), [제거 설명](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/README.md#L78-L89)

## 한계와 주의점: 설계 의도와 실제 경계를 구분합니다

### 소유권 검사는 수정 경로에 집중되어 있습니다

README는 자기 스킬만 건드린다고 설명하며, update/patch/remove_file/delete에서는 sidecar의 `created_by: agent`를 확인합니다. 그러나 **create는 이 검사에서 제외되고 같은 이름의 live 스킬 존재를 거절하는 검사가 없습니다**. create가 사용자 스킬과 동일한 계층·이름을 제안하면 본문 쓰기 경로까지 갈 수 있으며, sidecar가 없으면 생성 표식까지 붙일 수 있습니다. 이는 코드를 따라 확인한 충돌 가능성으로, 실제 사용자 파일을 덮어쓰는 실행을 해 본 결과는 아닙니다. [create 계층 선택](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/hook/promoter.py#L52-L56), [검사와 반영](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/hook/promoter.py#L145-L190), [소유권 검사 범위](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/lib/validate.py#L215-L221), [본문·표식 저장](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/hook/promoter.py#L134-L142)

또한 시작 시 임시 파일 정리는 관리 표식이 붙은 스킬만 찾는 것이 아니라 skills 아래의 `*.tmp`를 재귀 탐색해 삭제합니다. “사용자 파일은 어떤 경우에도 건드리지 않는다”는 절대적 해석은 이 경로에도 맞지 않습니다. [정리 범위](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/lib/skill_store.py#L93-L101)

### 통합의 흡수 대상 필드가 정상 staging 경로에서 빠집니다

MCP 스키마와 agent 지침은 `delete`에 `absorbed_into`를 넣어 어느 스킬로 합쳤는지 기록하도록 합니다. promoter에도 그 대상이 실제 관리 스킬인지 검사하는 코드가 있습니다. 그런데 **`stage_skill._intent`는 입력의 `absorbed_into`를 큐로 복사하지 않습니다**. 따라서 일반 MCP staging을 통과하면 그 필드가 사라져 단순 retirement처럼 처리되고, 의도한 대상 검증과 병합 기록이 적용되지 않는 경로가 됩니다. 문서의 패키지 무결성 지침과 별개로 이 전달 누락을 고려해야 합니다. [입력 필드](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/stage_skill/server.py#L54-L59), [큐 객체 구성](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/stage_skill/server.py#L139-L154), [promoter 대상 검사](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/hook/promoter.py#L165-L177)

### 문자열 필터와 hook은 완전한 샌드박스가 아닙니다

안전 검사는 정규식 기반이며 소스 자체도 의미 분석·샌드박스가 아니라고 설명합니다. child/reflector의 `Write`, `Edit`, `MultiEdit`, `NotebookEdit`는 hook이 거절하지만, 이 목록이 모든 도구의 모든 파일 쓰기를 막는 것은 아닙니다. 기본 bundle의 제한된 agent 도구 목록과 결합해 읽어야 하며, 원래 도구를 물려받는 fork를 같은 수준의 격리라고 표현할 수 없습니다. [패턴 검사](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/lib/skills_guard.py#L1-L12), [hook 차단 목록](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/hook/dispatch.py#L52-L53), [차단 분기](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/hook/dispatch.py#L138-L141)

비식별화도 정해진 패턴을 치환하는 방식입니다. 모델에게 증거를 원문 그대로 인용하도록 지시하지만 promoter는 전달받은 evidence를 다시 비식별화해 저장할 뿐 원본 세션과 일치하는지 확인하지 않습니다. 따라서 장부는 **제안의 이유와 제시된 근거를 추적하는 기록**이지, 사실성과 출처 진위를 인증한 기록은 아닙니다. [비식별화](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/lib/redact.py#L15-L31), [증거 저장](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/hook/promoter.py#L86-L92)

### 파일 원자성과 동시 실행·복구 보장은 다릅니다

sidecar의 카운터는 read-modify-write이고 소스는 프로세스 간 잠금이 미구현임을 명시합니다. 큐도 읽기 → 여러 제안 반영 → 전체 삭제 순서이므로 중간 실패에 대한 전체 트랜잭션은 아닙니다. promoter 주석 역시 반영과 큐 삭제 사이의 재실행에서 장부 중복이 생길 수 있음을 남깁니다. `orphans()`라는 큐 목록 함수는 있지만 여기서 살펴본 정상 drain은 전달된 run id 하나만 읽으므로, 파일이 남았다는 이유만으로 모든 중단 큐가 자동 복구된다고 단정할 수 없습니다. [sidecar 동시성 주석](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/lib/sidecar.py#L14-L16), [drain](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/hook/promoter.py#L237-L246), [큐 연산](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/src/autoharness/lib/intent_queue.py#L31-L46)

이 프로젝트의 라이선스는 MIT입니다. 이 글에서 확인한 값과 경로는 전체 SHA `7f725a94172e6c5e8f1f6305c9234e4c0c45d32b`에 한정되며 이후 릴리스에서 달라질 수 있습니다. [라이선스](https://github.com/tigerless-labs/autoharness/blob/7f725a94172e6c5e8f1f6305c9234e4c0c45d32b/LICENSE#L1-L21)

## 결론

AutoHarness에서 배울 핵심은 경험 추출을 모델에게 맡기면서도, **제안 큐·결정적 반영기·호출 인덱스·생명주기를 별도 계층으로 나눈 구조**입니다. 기록을 늘리는 것과 재사용 가능한 스킬 라이브러리를 유지하는 것을 다른 문제로 다룹니다. use/view/patch의 구분과 요청 수 기반 수명 관리는 실제 사용 흔적을 어떻게 운영 신호로 바꿀지 보여 줍니다.

동시에 이 커밋은 문서의 약속과 구현의 보장이 같지 않을 수 있음을 드러냅니다. 사용량은 과제 성공률이 아니고, 개별 파일의 원자적 쓰기는 전체 작업의 트랜잭션이 아니며, 기존 항목의 소유권 검사만으로 create 충돌까지 막히지는 않습니다. 자동 학습형 스킬 시스템을 이해하려면 좋은 교훈을 생성하는 능력과 그 교훈을 안전하게 반영·추적·정리하는 경계를 함께 읽어야 합니다.

### 이 글에서 다루지 못한 부분

hook 진입점, capture, reflector/curator 지침, staging, promoter, 검증·소유권·생명주기·저장 경로를 중심으로 분석했습니다. 테스트 스위트 전체, `metrics.py`의 집계·평가 세부, 모든 비식별화 패턴의 누락률, Claude Code 버전별 이벤트 호환성은 검증하지 않았습니다. 대상 레포의 의존성 설치·빌드·테스트·코드는 실행하지 않았으며, 실제 스킬 품질·사용량 개선·추론 비용도 측정하지 않았습니다.
