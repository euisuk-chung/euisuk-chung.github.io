---
type: "Guide"
title: "Claude Code에서 디폴트로 Auto Mode 사용하기 (Windows·Linux)"
description: "Claude Code Auto Mode의 동작 원리와 permission mode 비교, Windows·Linux 사용자 설정 파일에 defaultMode를 지정하는 절차, Bedrock·Vertex 환경 변수, classifier 차단 규칙을 설명합니다."
date: "2026-06-17"
tags:
  - "Claude"
  - "환경설정"
  - "Anthropic"
  - "AI Agent"
resource: "https://velog.io/@euisuk-chung/Claude-Code에서-디폴트로-Auto-Mode-사용하기"
generated:
  by: "process:velog-sync"
  at: "2026-09-08T03:19:07Z"
sources:
  - id: "velog"
    resource: "https://velog.io/@euisuk-chung/Claude-Code에서-디폴트로-Auto-Mode-사용하기"
    title: "Claude Code에서 디폴트로 Auto Mode 사용하기 (Windows·Linux)"
    author: "human:euisuk-chung"
    last_modified: "2026-06-17"
status: "stable"
year: "2026"
---

## 들어가며

요즘은 AI Agent에게 작업 대부분을 맡기는 시대입니다. 코드를 읽고 고치는 일은 물론이고, 셸 명령을 실행하고 환경을 정리하는 일까지 Agent에게 위임하는 흐름이 점점 자연스러워지고 있습니다. Claude Code 역시 이런 흐름에 맞춰, 매번 권한을 확인받지 않고도 작업을 이어가는 Auto Mode를 제공합니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/b7d23d7e-610e-4020-ba76-133650a5285b/image.png)

문제는 그 모드를 켜는 일 자체가 은근히 번거롭다는 점입니다. 권한 확인을 건너뛰기 위해 `claude --dangerously-skip-permissions` 같은 긴 플래그를 매번 입력하다 보면, 치기도 귀찮고 오타도 자주 납니다. 게다가 이렇게 권한을 통째로 건너뛰는 방식은 안전장치까지 함께 사라진다는 부담이 있습니다.

그렇다면 이런 긴 플래그 없이, 그냥 `claude`만 실행해도 곧바로 Auto Mode로 시작하게 만들 수는 없을까요? 이 글은 바로 그 방법, 즉 Auto Mode를 디폴트(default) 모드로 지정하는 설정을 다룹니다.

이 글에서는 Auto Mode의 동작 원리부터 Windows·Linux 환경에서의 단계별 디폴트 설정, 그리고 Auto Mode를 쓸 때 알아야 할 안전장치(classifier, 경계 설정, fallback)까지 다룹니다.

> <https://code.claude.com/docs/en/permission-modes#eliminate-prompts-with-auto-mode>

## 1. Auto Mode란 무엇인가

Claude Code는 파일을 수정하거나 셸 명령을 실행하거나 네트워크 요청을 보낼 때, 기본적으로 동작을 멈추고 사용자에게 승인을 요청합니다. 이 "멈추고 묻는" 빈도를 결정하는 것이 **Permission Mode**입니다.

**Auto Mode**는 이 루틴한 권한 프롬프트(permission prompt) 없이 Claude가 작업을 이어가도록 하는 모드입니다. 대신 별도의 classifier 모델이 각 동작을 실행 전에 검토합니다. 이 classifier는 다음과 같은 경우를 차단합니다.

* 사용자의 요청 범위를 넘어서는 동작(escalation)
* 인식되지 않은(unrecognized) 인프라를 대상으로 하는 동작
* Claude가 읽은 적대적 콘텐츠(hostile content)에 의해 유도된 것으로 보이는 동작

즉 Auto Mode는 **"프롬프트를 없애되, 백그라운드 안전 검사로 대체"**하는 방식입니다. 긴 작업에서 프롬프트 피로(prompt fatigue)를 줄이고 싶지만 방향성 자체는 신뢰할 수 있을 때 적합합니다.

한 가지 더 알아둘 점은, Auto Mode는 Claude가 명확히 할 질문이 있어도 멈추지 않고 작업을 계속하도록 유도한다는 것입니다. 다만 사용자의 프롬프트나 skill이 명시적으로 확인을 요구하는 경우에는 여전히 질문합니다.

Auto Mode는 리서치 프리뷰(research preview) 단계입니다. 프롬프트를 줄여주지만 안전을 보장하지는 않으므로, 민감한 작업의 검토를 대체하는 용도로 쓰지 않는 것이 좋습니다.

## 2. 그 외 Permission Mode 한눈에 보기

Auto Mode는 여러 Permission Mode 중 하나입니다. Auto Mode를 디폴트로 잡기 전에, 나머지 모드들이 각각 어떤 동작을 하고 어떻게 설정하는지 알아두면 선택 기준이 분명해집니다. 모드는 "묻지 않고 실행해 주는 범위"를 기준으로 나뉩니다.

| 모드 | 묻지 않고 실행되는 범위 | 적합한 상황 |
| --- | --- | --- |
| `default` | 읽기 전용 작업만 | 처음 시작할 때, 민감한 작업 |
| `acceptEdits` | 읽기 + 파일 편집 + 일반 파일시스템 명령(`mkdir`, `touch`, `mv`, `cp` 등) | 코드를 직접 검토하며 반복 작업할 때 |
| `plan` | 읽기 전용 작업만 (수정 없이 계획만 수립) | 코드베이스를 먼저 탐색할 때 |
| `auto` | 거의 모든 작업 (백그라운드 안전 검사 동반) | 긴 작업, 프롬프트 피로 줄이기 |
| `dontAsk` | 사전 승인된 도구만 | CI·스크립트 등 잠금 환경 |
| `bypassPermissions` | 모든 작업 (검사 없음) | 인터넷이 차단된 컨테이너·VM 전용 |

설정 방법은 모드마다 조금씩 다릅니다.

`default`, `acceptEdits`, `plan` 세 모드는 세션 중 `Shift+Tab`을 눌러 순서대로 순환할 수 있습니다. 시작할 때부터 특정 모드로 진입하려면 `--permission-mode` 플래그를 사용합니다(예: `claude --permission-mode plan`). 항상 같은 모드로 시작하고 싶다면 설정 파일의 `defaultMode`에 모드 이름을 넣으면 됩니다. 이 방식은 이 글에서 Auto Mode를 디폴트로 잡는 방법과 동일합니다.

`plan` 모드는 Claude가 파일을 수정하지 않고 조사와 계획만 세우게 합니다. 단일 프롬프트 앞에 `/plan`을 붙여 한 번만 적용할 수도 있습니다.

`dontAsk` 모드는 `Shift+Tab` 순환에 나타나지 않으며, `claude --permission-mode dontAsk`처럼 플래그로만 설정합니다. allow 규칙에 등록된 동작과 읽기 전용 명령만 실행하고 나머지는 자동 거부하므로, 무엇을 허용할지 미리 정해둔 비대화형 환경에 적합합니다.

`bypassPermissions` 모드는 모든 권한 검사를 건너뜁니다. 도입부에서 언급한 `--dangerously-skip-permissions`가 바로 이 모드를 켜는 플래그이며, `claude --permission-mode bypassPermissions`와 동일합니다. 보안상 활성화 플래그 없이 시작한 세션에서는 도중에 이 모드로 전환할 수 없고, 처음부터 해당 플래그로 다시 시작해야 합니다. 프롬프트 주입(prompt injection)이나 의도치 않은 동작을 전혀 막아주지 못하므로, 인터넷이 차단된 컨테이너·VM 같은 격리 환경에서만 사용해야 합니다.

이처럼 권한을 통째로 건너뛰는 `bypassPermissions` 대신, 안전 검사를 유지하면서 프롬프트만 줄이는 절충안이 Auto Mode입니다. 다음 장부터는 이 Auto Mode를 디폴트로 만드는 구체적인 방법을 다룹니다.

## 3. 디폴트로 켜기 전에: 사전 요구사항

Auto Mode는 다음 조건을 "모두" 충족할 때만 사용할 수 있습니다. 디폴트 설정을 넣더라도 조건이 하나라도 빠지면 세션이 그냥 `default` 모드로 시작합니다.

| 항목 | Anthropic API | Amazon Bedrock / Google Vertex AI / Microsoft Foundry |
| --- | --- | --- |
| 버전 | Claude Code v2.1.83 이상 | 환경 변수 사용 시 v2.1.158 이상 |
| 요금제(Plan) | 모든 요금제 | 모든 요금제 |
| 관리자(Admin) | Team·Enterprise는 관리자가 Claude Code admin settings에서 활성화 필요 | 동일 |
| 지원 모델 | Claude Opus 4.6 이상 또는 Sonnet 4.6 | Claude Opus 4.7, Opus 4.8 만 지원 |
| Provider 기본값 | 기본 사용 가능 | `CLAUDE_CODE_ENABLE_AUTO_MODE`를 설정하기 전까지 비활성 |

Sonnet 4.5, Opus 4.5, Haiku, claude-3 계열 등 구형 모델은 어떤 Provider에서도 지원되지 않습니다.

조건을 충족하면 `Shift+Tab`으로 모드를 순환할 때 Auto Mode가 나타나며, 처음 Auto로 전환하면 동의(opt-in) 프롬프트가 한 번 표시됩니다. 만약 Claude Code가 Auto Mode를 "사용 불가"로 보고한다면 이는 일시적 장애가 아니라 위 요구사항 중 하나가 충족되지 않았다는 의미입니다.

## 4. Anthropic API 환경에서 디폴트로 설정하기

Anthropic API를 직접 사용하는 경우(가장 일반적인 경우), Auto Mode는 기본적으로 사용 가능하므로 디폴트 설정만 추가하면 됩니다.

### 4.1 설정 파일 위치가 가장 중요합니다

`defaultMode`를 `"auto"`로 설정합니다. 단, 이 값은 반드시 사용자 단위 설정 파일에 있어야 합니다.

* Linux: `~/.claude/settings.json`
* Windows: `%USERPROFILE%\.claude\settings.json` (예: `C:\Users\사용자명\.claude\settings.json`)

설정 내용은 다음과 같습니다.

```
{
  "permissions": {
    "defaultMode": "auto"
  }
}
```

### 4.2 프로젝트 설정에 넣으면 안 되는 이유

Claude Code v2.1.142 이상은 `.claude/settings.json`이나 `.claude/settings.local.json`(프로젝트·로컬 설정)에 들어 있는 `auto` 값을 무시합니다. 이는 임의의 저장소(repository)가 스스로에게 Auto Mode 권한을 부여하지 못하도록 막는 보안 장치입니다.

증상으로 보면 이렇습니다. `defaultMode: "auto"`를 설정했는데도 오류 없이 세션이 `default` 모드로 시작한다면, 그 설정은 십중팔구 프로젝트·로컬 설정 파일에 들어 있는 것입니다. 해당 값을 사용자 설정 파일인 `~/.claude/settings.json`으로 옮기면 해결됩니다.

## 5. Bedrock·Vertex AI·Foundry 환경에서 활성화하기

Amazon Bedrock, Google Cloud Vertex AI, Microsoft Foundry를 통해 사용하는 경우에는 한 단계가 더 필요합니다. 이 Provider들에서는 `CLAUDE_CODE_ENABLE_AUTO_MODE`를 `1`로 설정하기 전까지 Auto Mode가 `Shift+Tab` 순환 목록에 나타나지 않습니다. 이 환경 변수는 Claude Code v2.1.158 이상에서 동작하며, 지원 모델은 Opus 4.7과 Opus 4.8뿐입니다.

### 5.1 환경 변수 설정

개발자 한 명에 한해 활성화하려면 사용자 설정 파일의 `env` 블록에 변수를 추가합니다.

```
{
  "env": {
    "CLAUDE_CODE_ENABLE_AUTO_MODE": "1"
  }
}
```

조직 전체에 적용하려면 동일한 `env` 블록을 managed settings(관리 설정)에 추가합니다.

### 5.2 활성화와 디폴트 설정을 함께 적용

환경 변수만 설정하면 Auto Mode가 순환 목록에 보일 뿐, 시작 모드가 되지는 않습니다. 시작 모드까지 만들려면 사용자 또는 관리 설정에 `defaultMode`도 함께 넣어야 합니다.

```
{
  "env": {
    "CLAUDE_CODE_ENABLE_AUTO_MODE": "1"
  },
  "permissions": {
    "defaultMode": "auto"
  }
}
```

이 Provider들에서는 `CLAUDE_CODE_ENABLE_AUTO_MODE`가 함께 설정되어 있지 않으면 `defaultMode: "auto"`가 무시됩니다. 두 값이 짝을 이루어야 한다는 점을 기억하세요.

만약 LLM gateway를 `ANTHROPIC_BASE_URL`로 연결해 사용하는 경우라면, gateway가 요청을 Anthropic API로 라우팅하기 때문에 환경 변수 없이도 Auto Mode에 접근 가능할 수 있습니다.

## 6. Windows·Linux 단계별 적용 절차

개념을 종합해 실제 적용 순서로 정리하면 다음과 같습니다.

먼저 버전을 확인합니다.

```
claude --version
```

이어서 사용자 설정 파일을 엽니다. Linux에서는 `~/.claude/settings.json`을, Windows에서는 `%USERPROFILE%\.claude\settings.json`을 편집합니다. 파일이나 `.claude` 디렉터리가 없으면 새로 만들면 됩니다.

Anthropic API 사용자는 `permissions.defaultMode`만 추가하면 되고, Bedrock·Vertex·Foundry 사용자는 `env`의 `CLAUDE_CODE_ENABLE_AUTO_MODE`까지 추가합니다(5장 참고).

설정 후 세션을 새로 시작하면 Auto Mode로 진입합니다. 세션 중 모드를 바꾸고 싶을 때는 `Shift+Tab`으로 순환할 수 있습니다. 이때 활성화된 선택적 모드는 `plan` 뒤에 배치되며, `bypassPermissions`가 먼저, `auto`가 마지막에 옵니다. 둘 다 활성화돼 있다면 `auto`로 가는 길에 `bypassPermissions`를 거치게 됩니다.

현재 classifier가 적용하는 기본 규칙 목록 전체를 확인하려면 다음 명령을 사용합니다.

```
claude auto-mode defaults
```

## 7. Auto Mode에서 차단·허용되는 동작

Auto Mode의 classifier는 사용자의 작업 디렉터리(working directory)와 저장소에 설정된 remote는 신뢰하고, 그 외는 외부(external)로 간주합니다.

기본적으로 차단되는 동작은 다음과 같습니다.

* `curl | bash`처럼 코드를 내려받아 곧바로 실행하는 행위
* 민감한 데이터를 외부 엔드포인트로 전송
* 프로덕션 배포(deploy) 및 마이그레이션(migration)
* 클라우드 스토리지 대량 삭제
* IAM 또는 저장소 권한 부여
* 공유 인프라 수정
* 세션 이전부터 존재하던 파일을 되돌릴 수 없게 파괴
* force push, 또는 `main`에 직접 push

기본적으로 허용되는 동작은 다음과 같습니다.

* 작업 디렉터리 내 로컬 파일 작업
* lock 파일이나 manifest에 선언된 의존성 설치
* `.env`를 읽어 해당하는 API에만 자격 증명 전송
* 읽기 전용(read-only) HTTP 요청
* 세션 시작 브랜치 또는 Claude가 만든 브랜치로 push

routine한 동작이 자꾸 차단된다면, 보통은 classifier가 사용자의 인프라에 대한 컨텍스트를 모르기 때문입니다. 이 경우 관리자가 신뢰할 저장소·버킷·서비스를 `autoMode.environment` 설정으로 추가할 수 있습니다.

## 8. 대화로 설정하는 경계(Boundaries)

classifier는 사용자가 대화 중에 말한 경계를 차단 신호로 취급합니다. 예를 들어 "push 하지 마" 또는 "내가 검토할 때까지 배포하지 마"라고 말하면, 기본 규칙상 허용되는 동작이라도 classifier가 해당 동작을 차단합니다. 이 경계는 이후 메시지에서 사용자가 직접 해제하기 전까지 유지되며, Claude 스스로 "조건이 충족됐다"고 판단하는 것만으로는 해제되지 않습니다.

다만 경계는 규칙(rule)으로 저장되는 것이 아니라 매 검사마다 대화 기록에서 다시 읽어들이는 방식입니다. 따라서 context compaction으로 해당 메시지가 사라지면 경계도 사라질 수 있습니다. 확실한 보장이 필요하다면 deny rule을 추가하는 편이 안전합니다.

## 9. Auto Mode가 일반 모드로 되돌아가는 경우(Fallback)

classifier가 어떤 동작을 차단하면 알림이 표시되고, 해당 항목은 `/permissions`의 "Recently denied" 탭에 기록됩니다. 여기서 `r`을 눌러 수동 승인으로 재시도할 수 있습니다.

classifier가 연속 3회 또는 누적 20회 차단하면 Auto Mode가 일시 중지되고 Claude Code가 다시 프롬프트를 띄우기 시작합니다. 프롬프트된 동작을 승인하면 Auto Mode가 재개됩니다. 이 임계값은 변경할 수 없습니다. 허용된 동작이 하나라도 발생하면 연속 카운터는 초기화되지만, 누적 카운터는 세션 동안 유지되며 자체 한도에 도달해 fallback이 발생할 때만 초기화됩니다.

`-p` 플래그를 쓰는 비대화형 모드(non-interactive mode)에서는 프롬프트를 받을 사용자가 없으므로, 반복 차단 시 세션이 중단됩니다.

## 10. 관리자 차원의 제어

조직에서 Auto Mode를 통제하려는 경우, 관리자는 managed settings에서 `permissions.disableAutoMode`를 `"disable"`로 설정해 Auto Mode를 잠글 수 있습니다. Bedrock·Vertex·Foundry에서는 이 설정이 `CLAUDE_CODE_ENABLE_AUTO_MODE` 환경 변수보다 우선 적용되어, 활성화 변수를 덮어씁니다.

반대로 Team·Enterprise에서는 관리자가 Claude Code admin settings에서 먼저 활성화해야 일반 사용자가 Auto Mode를 켤 수 있습니다.

## 마무리 (RECAP)

* Auto Mode는 루틴 권한 프롬프트를 없애는 대신, classifier 모델이 모든 동작을 실행 전에 검토하는 모드입니다.
* 디폴트로 켜려면 먼저 버전·요금제·모델·Provider 요구사항을 충족시킨 뒤, `permissions.defaultMode`를 `"auto"`로 설정합니다.
* 가장 흔한 실수는 설정 위치입니다. v2.1.142 이상은 프로젝트·로컬 설정의 `auto`를 무시하므로, 반드시 사용자 설정 파일(Linux `~/.claude/settings.json`, Windows `%USERPROFILE%\.claude\settings.json`)에 넣어야 합니다.
* Bedrock·Vertex AI·Foundry에서는 `CLAUDE_CODE_ENABLE_AUTO_MODE=1`을 함께 설정해야 하며, Opus 4.7·4.8만 지원됩니다.
* Auto Mode는 만능 안전장치가 아닙니다. classifier의 기본 차단·허용 규칙, 대화로 거는 경계, 연속 3회·누적 20회 차단 시의 fallback 동작을 이해하고 사용하는 것이 중요합니다.

읽어주셔서 감사합니다!
