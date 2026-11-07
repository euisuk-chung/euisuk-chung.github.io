---
type: "Repo Review"
title: "[Repo Review] Learn Harness Engineering — 에이전트의 작업 환경을 만들고 검증하는 코드 읽기"
description: "Learn Harness Engineering의 하네스 생성·구조 채점·benchmark 흐름과 그래프 예제를 추적하며 문서 규칙과 실제 실행 검증의 경계를 살펴봅니다."
date: "2026-10-04"
tags:
  - "Repo Review"
  - "AI Agent"
  - "Tools"
resource: "https://github.com/walkinglabs/learn-harness-engineering/tree/38ddcd2bf8d65271f668b94e7c875ca1d629d622"
generated:
  by: "process:blog-review"
  at: "2026-10-04T06:04:11+09:00"
sources:
  - id: "walkinglabs/learn-harness-engineering"
    resource: "https://github.com/walkinglabs/learn-harness-engineering/tree/38ddcd2bf8d65271f668b94e7c875ca1d629d622"
    title: "Learn Harness Engineering"
status: "stable"
year: "2026"
analyzed_at: "2026-10-04T06:04:11+09:00"
source_id: "walkinglabs/learn-harness-engineering"
source_revision: "38ddcd2bf8d65271f668b94e7c875ca1d629d622"
source_type: "repo"
source_url: "https://github.com/walkinglabs/learn-harness-engineering/tree/38ddcd2bf8d65271f668b94e7c875ca1d629d622"
visual_sources:
  - path: "/img/reviews/2026/learn-harness-engineering-review/harness-flow.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/scripts/create-harness.mjs#L31-L64"
    caption: "리뷰어 작성, 분석 커밋 기준. 생성과 구조 평가 흐름이며 에이전트 실행 경로가 아닙니다."
---

## 들어가며

코딩 에이전트가 세션을 바꿀 때마다 목표를 잊거나, 테스트를 실행하지 않은 채 완료를 선언한다면 무엇을 바꾸어야 할까요? Learn Harness Engineering은 이 문제를 모델 주변의 작업 환경에서 다루는 프로젝트 기반 교육 저장소입니다. 여기서 **하네스(harness)**는 에이전트가 읽는 지침, 진행 상태, 검증 절차, 작업 범위, 세션 인수인계를 함께 설계한 환경을 뜻합니다. 이 다섯 요소는 저장소의 `harness-creator` 설명과 생성 템플릿에 구체적인 파일로 대응됩니다. [스킬 README](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/README.md#L1-L45)

이 저장소의 학습 가치는 “좋은 지침을 작성하자”에서 멈추지 않고, 그 지침을 생성하고 검사하는 코드를 함께 읽을 수 있다는 데 있습니다. 다만 구조를 갖추었다는 사실과 실제 작업 성공률이 높다는 사실은 다릅니다. 이 리뷰는 그 경계를 중심으로 생성 도구, 점수 계산, benchmark, 그래프 예제를 추적합니다.

분석 기준은 전체 커밋 `38ddcd2bf8d65271f668b94e7c875ca1d629d622`입니다. 대상 저장소의 의존성 설치, 코드 실행, 빌드, 테스트는 수행하지 않았습니다. 아래의 결과는 문서와 코드의 정적 분석이며, 실행 성공이나 성능 측정 결과가 아닙니다.

## 무엇이 들어 있는 저장소인가

루트 `package.json`은 VitePress 문서 사이트를 정의합니다. 개발·빌드·미리보기 명령, 강의 코드용 `tsx`, PDF 내보내기용 스크립트가 있으며, `pdf:build`는 문서 빌드 후 PDF 내보내기를 연결합니다. 따라서 루트 패키지는 교육 자료 배포를 위한 것이고, 하네스 생성 도구는 그 안의 별도 Node.js 스크립트입니다. 생성·검증 스크립트가 가져오는 모듈은 Node.js 내장 모듈과 같은 디렉터리의 유틸리티입니다. [패키지 매니페스트](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/package.json#L1-L33), [생성 도구 import](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/scripts/create-harness.mjs#L1-L13)

| 영역 | 역할 | 이 글에서 읽는 범위 |
| --- | --- | --- |
| `docs/en/lectures/` | 개념 설명과 강의 코드 | 최소 하네스와 maker-checker 그래프 예제 |
| `projects/project-01/` | 약한 하네스와 명시적 하네스의 비교 실습 | 실험 계약과 starter/solution 구분 |
| `skills/harness-creator/templates/` | 지침·진행 상태·인수인계 서식 | 생성 파일이 에이전트에게 전달하는 정보 |
| `skills/harness-creator/scripts/` | 생성·검증·보고서 도구 | 입력부터 파일 및 점수 출력까지의 핵심 흐름 |
| 루트 `package.json` | 교육 사이트·PDF 작업 명령 | 실행 진입점과 의존성 확인 |

이 구성은 [강의 2 예제](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/docs/en/lectures/lecture-02-what-a-harness-actually-is/code/minimal-harness-loop.ts#L1-L36), [Project 01 안내](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/projects/project-01/README.md#L1-L58), [스킬 파일 목록](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/README.md#L57-L79)에서 확인할 수 있습니다. 강의 2의 `minimalHarness`는 `read_file`을 선택하고 결과를 메시지 배열에 추가하는 교육용 함수입니다. 실제 파일 내용 대신 `contents of ...`라는 문자열을 돌려주므로, 이를 실사용 파일 도구나 모델 기반 의사결정 구현으로 해석해서는 안 됩니다.

## 아키텍처: 생성과 평가의 두 경로

![대상 프로젝트에서 파일을 생성하고 별도 명령으로 구조 점수를 계산하는 흐름]({{ '/img/reviews/2026/learn-harness-engineering-review/harness-flow.svg' | relative_url }})

그림은 **리뷰어 작성, 분석 커밋 기준**입니다. 생성 경로는 [create-harness](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/scripts/create-harness.mjs#L31-L64), 평가 경로는 [validate-harness](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/scripts/validate-harness.mjs#L24-L43)와 [run-benchmark](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/scripts/run-benchmark.mjs#L37-L76)를 근거로 재구성했습니다. 화살표는 CLI와 파일 사이의 흐름이며, 모델 호출이나 작업 수행을 나타내지 않습니다.

이 분리가 중요합니다. 생성기는 규칙과 검증 명령을 **파일로 쓰고**, 검사기는 파일의 존재와 내용을 **읽어 점수를 계산**합니다. 생성된 `init.sh`가 실제 테스트를 실행하는 것은 사용자가 이후 그 스크립트를 실행할 때의 별도 경로입니다. `create-harness` 자체는 `init.sh`를 실행하지 않습니다. [생성·쓰기 코드](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/scripts/create-harness.mjs#L51-L64)

## 작동 원리 1: 프로젝트 정보를 검증 명령으로 바꿉니다

### CLI 입력과 프로젝트 판별

`parseArgs`는 `--target`, `--package-manager` 같은 옵션을 읽고, 하이픈으로 연결된 키를 `packageManager`처럼 바꿉니다. `create-harness`는 `--target`, 첫 번째 위치 인자, 현재 디렉터리 순으로 대상 경로를 선택합니다. 기본 지침 파일명은 `AGENTS.md`이며, 기존 파일은 기본적으로 보존합니다. [인자 파서](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/scripts/lib/harness-utils.mjs#L10-L30), [대상 결정](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/scripts/create-harness.mjs#L31-L38)

프로젝트 판별은 파일 목록을 최대 800개 수집하고 루트 `package.json`을 읽는 방식입니다. Node 프로젝트이면 React 또는 TypeScript 의존성을 보고 세분화하며, 그렇지 않으면 Python·Go·Rust·Maven·Gradle·.NET의 표식 파일을 순서대로 확인합니다. 패키지 관리자는 명시적 옵션을 우선하고, 잠금 파일로 bun → pnpm → yarn을 판별한 뒤 npm을 기본값으로 사용합니다. 이 방식은 빠른 초기 설정에 적합하지만, 복합 모노레포의 모든 하위 프로젝트를 정확히 분류한다는 보장은 없습니다. 800개 제한과 판별 우선순위가 있기 때문입니다. [탐지 코드](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/scripts/lib/harness-utils.mjs#L70-L140)

### 검증 명령은 프로젝트에 맞춘 초안입니다

Node 계열에서는 설치 명령 뒤에 존재하는 `check`, `typecheck`, `type-check`, `lint`, `test`, `build` 스크립트를 연결합니다. Python이면 pytest와 compileall, Go이면 `go test ./...`, Rust이면 `cargo test`를 반환합니다. 알 수 없는 프로젝트에는 검증 명령을 직접 교체하라는 안내를 출력하는 `echo` 한 줄이 들어갑니다. 그러므로 “init.sh가 생성되었다”와 “프로젝트에 의미 있는 검증이 준비되었다”를 구분해야 합니다. [명령 선택](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/scripts/lib/harness-utils.mjs#L143-L190)

Python 분기에서 pytest의 종료 코드 5, 즉 테스트 미수집은 실패로 취급하지 않도록 명령 문자열을 만듭니다. 이는 초기 프로젝트를 다루기 위한 코드상의 선택입니다. 테스트가 없는 상태에서도 뒤의 구문 검사를 통과할 수 있으므로, 사용자 기능의 검증 증거까지 생긴 것으로 읽어서는 안 됩니다. [Python 명령](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/scripts/lib/harness-utils.mjs#L152-L161)

### 템플릿과 실제 실행 경계

다음은 생성 도구의 실제 코드입니다. `initScriptFromCommands`로 내용을 만든 뒤 파일에 쓰고 실행 권한을 부여합니다.

```javascript
const initPath = path.join(target, 'init.sh');
if (force || !await exists(initPath)) {
  await writeText(initPath, initScriptFromCommands(commands));
  await chmod(initPath, 0o755);
  results.push({ path: initPath, status: 'written' });
} else {
  results.push({ path: initPath, status: 'skipped', reason: 'exists' });
}
```

출처: [create-harness.mjs 57–64행](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/scripts/create-harness.mjs#L57-L64).

나머지 네 파일은 템플릿을 복사하면서 프로젝트 목적과 검증 명령을 치환합니다. 템플릿 복사도 기본적으로 기존 파일을 건너뛰고, `--force`를 지정하면 덮어씁니다. 따라서 반복 실행으로 이미 존재하는 지침이 새로 탐지한 명령과 자동 동기화되지는 않습니다. 생성 결과의 `written`과 `skipped`를 확인하고 내용의 일관성을 점검해야 합니다. [템플릿 복사](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/scripts/lib/harness-utils.mjs#L54-L68), [호출 위치](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/scripts/create-harness.mjs#L42-L55)

## 작동 원리 2: 세션 기억을 파일로 외부화합니다

하네스가 유지하려는 상태는 모델 내부의 기억이 아니라 저장소의 파일입니다. 지침 템플릿은 시작할 때 프로젝트 문서와 기능 목록을 읽고 초기 검증을 수행하도록 안내합니다. 작업 중에는 한 기능만 선택하고, 종료할 때 상태와 증거를 갱신하도록 합니다. 이는 에이전트가 따라야 할 문서상의 절차이며, 생성기가 에이전트의 행동을 강제하는 감시 루프를 구현한 것은 아닙니다. [지침 템플릿](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/templates/agents.md#L5-L50)

| 파일 | 담는 정보 | 다음 세션에서의 의미 |
| --- | --- | --- |
| `feature_list.json` | 기능 ID, 설명, 의존 기능, 상태, 증거 | 무엇을 완료했고 무엇을 해야 하는지 |
| `progress.md` | 현재 상태, 진행 작업, 결정, 수정 파일, 검증 증거 | 직전 세션이 어디에서 끝났는지 |
| `session-handoff.md` | 목표, 브랜치·커밋, 검증 표, 위험, 다음 행동 | 작업 재개 전에 확인할 맥락 |
| `AGENTS.md` | 시작 순서, 범위, 완료 조건, 종료 절차 | 앞의 파일을 언제 읽고 갱신할지 |

표의 근거는 [기능 목록](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/templates/feature-list.json#L1-L44), [진행 로그](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/templates/progress.md#L1-L51), [인수인계](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/templates/session-handoff.md#L1-L40)입니다. 기능 목록에는 초기 설정부터 인수인계까지 다섯 개의 예시 기능이 들어 있습니다. 특히 첫 사용자 기능의 설명은 실제 요구사항으로 바꾸도록 되어 있으므로, 그대로 두면 프로젝트의 작업 계약이 완성되지 않습니다.

리뷰어 관점에서 이 설계의 장점은 상태를 읽고 수정할 위치가 명확하다는 것입니다. 동시에 파일을 만들었다고 최신 상태가 유지되지는 않습니다. 다음 세션이 재개할 수 있으려면 실제 변경 사항, 실행한 명령, 남은 위험을 사람이든 에이전트든 기록해야 합니다.

## 작동 원리 3: 구조를 어떻게 점수화하는가

### 입력은 정해진 이름의 일곱 파일입니다

`validate-harness`는 `loadHarnessFiles`로 루트의 지침 두 종류, 기능 목록 두 이름, 진행 로그, 인수인계, init 스크립트를 읽습니다. 프로젝트 전체 코드나 중첩 디렉터리의 모든 지침을 검사하지 않습니다. `scoreHarness`는 파일 경로를 키로 하는 Map을 만들고 다섯 하위 시스템마다 다섯 개의 조건을 검사합니다. [입력 파일 목록](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/scripts/lib/harness-utils.mjs#L336-L354), [25개 조건](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/scripts/lib/harness-utils.mjs#L220-L265)

검사에는 세 가지 방식이 섞여 있습니다. 파일 존재 여부, 부분 문자열 존재 여부, JSON 필드 검사입니다. 지침의 일부 항목에는 `structuredText`를 적용해 일반 문단을 제외하고 제목·목록·표·코드 블록·굵은 글씨로 시작하는 줄을 남깁니다. 키워드를 문단에 흩뿌린 것과 구조화된 지침을 구분하려는 설계입니다. 다만 남은 텍스트에서도 의미 추론이 아니라 대소문자를 무시한 부분 문자열 검사를 합니다. [문자열 및 구조 필터](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/scripts/lib/harness-utils.mjs#L291-L319)

중요한 세부는 `textHas`가 `every`가 아니라 `some`을 사용한다는 점입니다. 조건에 여러 단어가 나열되어 있어도 모두 필요하다는 뜻이 아닙니다. 예를 들어 상태 파일 연결 조건은 `feature_list.json` 또는 `progress.md` 중 하나가 지침의 구조화된 부분에 나타나면 통과합니다. 점수는 설명 문구만 보지 말고 판정 함수를 함께 읽어야 해석할 수 있습니다. [조건 정의](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/scripts/lib/harness-utils.mjs#L229-L242), [some 판정](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/scripts/lib/harness-utils.mjs#L291-L294)

### 총점의 의미와 하한

실제 점수 계산은 다음과 같습니다.

```javascript
const score = Math.max(1, Math.round((passed / subsystemChecks.length) * 5));
```

출처: [harness-utils.mjs 267–275행](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/scripts/lib/harness-utils.mjs#L267-L275).

각 하위 시스템은 1~5점이고, 다섯 점수의 합을 25로 나누어 100점 척도로 바꿉니다. 따라서 조건을 하나도 통과하지 못해도 전체 점수의 하한은 20점입니다. 이는 실행해서 얻은 관측값이 아니라 코드의 하한을 계산한 결과입니다. 기본 통과 기준은 70점이며, 그 아래이면 CLI의 종료 코드를 1로 설정합니다. 가장 낮은 영역은 `bottleneck`으로 표시하고, 모든 영역이 5점일 때만 이를 null로 둡니다. 실제 실패의 원인을 측정해 찾아낸 병목은 아닙니다. [총점·병목](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/scripts/lib/harness-utils.mjs#L267-L284), [CLI 임계값](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/scripts/validate-harness.mjs#L24-L43)

JSON 검사도 범위가 제한됩니다. `features`가 배열이고 각 항목의 `id`, `name`, `description`, `status`가 문자열인지 확인합니다. 함께 배포된 JSON Schema의 상태 enum이나 ID 패턴을 이 함수가 불러와 검증하지는 않습니다. 빈 배열 역시 `every` 조건을 만족합니다. 따라서 구조 점수를 작업 상태의 완전한 무결성 검사로 사용할 수 없습니다. [JSON 검사](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/scripts/lib/harness-utils.mjs#L321-L334), [스키마](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/templates/feature-list.schema.json#L1-L47)

## 작동 원리 4: benchmark가 실제로 평가하는 것

`run-benchmark`는 대상 하네스 점수, 평가 사례 파일의 구성 점수, 자체 생성 점검을 모아 JSON을 저장하고 선택적으로 HTML을 만듭니다. 이름에 benchmark가 들어 있지만 LLM에 과제를 실행시키거나 응답을 채점하지 않습니다. README도 구조적 점검이며 실제 전후 에이전트 세션 실험을 대체하지 않는다고 설명합니다. [benchmark 본체](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/scripts/run-benchmark.mjs#L37-L76), [README의 범위](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/README.md#L35-L55)

자체 점검은 임시 디렉터리에 `check`, `test`, `build` 스크립트 이름을 가진 `package.json`을 쓰고, 자식 Node 프로세스로 생성 도구를 실행한 뒤 만들어진 파일을 점수화합니다. 여기서 tsc·vitest·vite를 설치하거나 실행하는 코드 경로는 없습니다. 자체 점검은 생성기와 구조 채점기가 함께 동작하는지 보는 장치입니다. [runSelfCheck](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/scripts/run-benchmark.mjs#L79-L102)

평가 사례 점수도 사례 실행 결과가 아닙니다. 사례가 열 개 이상인지, 이름에 session·verification·memory 같은 범주가 있는지, `prompt`, `expected_output`, `expectations` 필드가 있는지 등을 검사합니다. 기대 출력이 실제로 생성되었는지는 확인하지 않습니다. [scoreEvals](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/scripts/run-benchmark.mjs#L104-L126)

출력의 권고 문구 역시 이 경계를 잘 보여 줍니다. 하네스가 85점 이상이고 평가 구성 점수가 90점 이상이면 “현실적인 전후 세션 benchmark를 시작할 준비”가 되었다는 의미의 문구를 반환합니다. 이미 실효성을 입증했다는 판정이 아닙니다. [recommend](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/scripts/run-benchmark.mjs#L128-L139)

## 그래프 예제로 보는 다음 단계와 미완성 경계

강의 14의 maker-checker 예제는 만드는 역할과 검사하는 역할을 분리한 그래프입니다. 공유 상태에는 요구사항, 코드, 검토 결과, 시도 횟수가 있고, 경로는 research → implement → verify로 진행합니다. 검토가 실패하면 implement로 돌아가고, 그 외에는 merge를 거쳐 끝납니다. [공유 상태와 노드](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/docs/en/lectures/lecture-14-graph-engineering/code/maker_checker_graph.py#L19-L63), [라우팅과 연결](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/docs/en/lectures/lecture-14-graph-engineering/code/maker_checker_graph.py#L66-L90)

이 예제를 작동하는 자동 개발 시스템으로 읽지 않도록 구현 경계를 살펴볼 필요가 있습니다.

- `call_model`은 `NotImplementedError`를 발생시키는 자리표시자입니다. 모델 제공자 연결은 독자가 구현해야 합니다.
- `tests_pass`는 테스트 러너를 실행하지 않고 코드에 `def test` 문자열이 들어 있는지 봅니다. 검토 응답에 `approved`가 포함되고 이 문자열 검사도 참일 때 pass가 됩니다.
- `merge`는 메시지를 출력할 뿐 실제 Git 병합이나 커밋을 하지 않습니다.
- `attempts`는 덧셈 reducer를 선언했지만 각 노드가 증가량을 반환하지 않습니다. 라우팅 함수에도 최대 재시도 조건이 없습니다. 실패 후 재구현 프롬프트에는 요구사항만 들어가고 검사 피드백이 직접 전달되지 않습니다.

모두 [예제 21–71행](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/docs/en/lectures/lecture-14-graph-engineering/code/maker_checker_graph.py#L21-L71)에 근거한 정적 관찰입니다. 특히 `review`의 설명에는 unclear가 있지만 라우팅은 fail만 되돌립니다. 현재 verify가 만드는 값은 pass/fail 둘뿐이며, 향후 unclear를 추가할 때에는 분기 조건도 함께 바꾸어야 합니다.

체크포인터는 `MemorySaver()`로 연결되어 있고 파일이나 데이터베이스 저장소 설정은 없습니다. 주석은 프로세스가 종료되어도 재개하는 취지를 설명하지만, 이 코드만으로 프로세스 재시작 뒤의 내구성 있는 복구를 입증할 수는 없습니다. 이 예제는 상태·노드·분기·체크포인터의 연결을 익히는 골격으로 읽는 것이 정확합니다. [컴파일과 호출](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/docs/en/lectures/lecture-14-graph-engineering/code/maker_checker_graph.py#L93-L108)

## 설치와 사용: 문서에 제시된 경로

다음은 같은 커밋의 스킬 README에 있는 명령입니다. 이 리뷰에서는 실행하지 않았습니다.

```bash
npx skills add walkinglabs/learn-harness-engineering --skill harness-creator
```

설치 명령 출처: [README 7–13행](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/README.md#L7-L13). 문서에는 스킬 디렉터리를 직접 복사하는 방법도 있습니다. 위 명령은 SHA를 지정하지 않으므로, 나중에 실행할 때 이 글의 분석 버전과 같다고 보장할 수 없습니다.

```bash
node skills/harness-creator/scripts/create-harness.mjs --target /path/to/project
node skills/harness-creator/scripts/validate-harness.mjs --target /path/to/project
node skills/harness-creator/scripts/run-benchmark.mjs --target /path/to/project --html /path/to/report.html
```

사용 명령 출처: [README 15–23행](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/README.md#L15-L23). 이 상대 경로의 명령은 해당 위치에 스킬 파일이 있을 때를 전제로 합니다. 생성 후에는 예시 기능을 실제 요구사항으로 바꾸고 검증 명령을 검토하는 과정이 필요합니다. `--commands`로 사용자 명령을 전달하거나 패키지 관리자를 명시할 수 있다는 옵션은 [스킬 문서](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/SKILL.md#L38-L56)에 설명되어 있습니다.

실제 효과를 비교하려는 독자에게는 Project 01의 계약이 구조 점수와 다른 기준을 제공합니다. starter와 solution 조건에서 같은 과제를 수행하고 완료 여부, 재시도, 조기 완료 선언을 비교하도록 안내합니다. 문서 자체도 solution을 이미 제품 기능과 하네스가 들어 있는 참고 기준으로 설명하며, 에이전트가 같은 결과를 재현한다는 보장으로 제시하지 않습니다. 이 리뷰는 해당 비교 실험을 수행하지 않았습니다. [Project 01 실험 계약](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/projects/project-01/README.md#L13-L58)

## 한계와 주의점

첫째, 문서 지침과 실행 통제를 구분해야 합니다. 한 기능씩 작업하고 증거를 남기라는 규칙은 유용한 계약이지만, 생성·검증 도구에는 에이전트의 모든 행동을 감시하거나 규칙 위반을 차단하는 런타임이 없습니다. 핵심 CLI는 파일 생성 및 구조 평가를 수행합니다. [생성기](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/scripts/create-harness.mjs#L31-L75), [검사기](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/scripts/validate-harness.mjs#L24-L43)

둘째, 점수가 검사 규칙의 언어와 형식에 의존합니다. 구조 필터와 영어 부분 문자열을 만족하는 문서는 높은 점수를 받을 수 있지만, 올바른 한국어 지침이 같은 조건을 통과한다고 보장되지 않습니다. 반대로 형식과 키워드가 갖추어져도 실제 검증이 유효한지는 별도 문제입니다. 이는 문자열 규칙을 읽어 도출한 한계이며 다국어 정확도를 실험한 결과는 아닙니다. [구조 필터](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/scripts/lib/harness-utils.mjs#L291-L319)

셋째, 자동 탐지된 명령은 프로젝트별 조정이 필요합니다. Node의 기본 설치 명령은 `npm install`이고, 알 수 없는 프로젝트에는 안내용 echo가 들어갑니다. 생성된 셸 스크립트를 실행하기 전에 의존성 설치 정책과 실제 검증 범위를 확인해야 합니다. `--force`는 기존 파일을 덮어쓰므로 이미 작성한 규칙을 보존하려면 기본 건너뛰기 동작과 차이를 이해해야 합니다. [명령 생성](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/scripts/lib/harness-utils.mjs#L170-L209), [덮어쓰기 조건](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/skills/harness-creator/scripts/lib/harness-utils.mjs#L54-L67)

라이선스는 MIT이며 저작권 표시와 허가 문구의 유지 조건 및 무보증 조항을 포함합니다. [LICENSE](https://github.com/walkinglabs/learn-harness-engineering/blob/38ddcd2bf8d65271f668b94e7c875ca1d629d622/LICENSE#L1-L21)

## 마무리

Learn Harness Engineering의 핵심은 에이전트의 작업을 다시 시작할 수 있는 파일 기반 환경으로 바꾸는 데 있습니다. 생성기는 프로젝트 정보를 지침·기능 목록·검증 스크립트로 옮기고, 검사기는 그 환경의 구조적 빈틈을 드러냅니다. benchmark와 그래프 골격까지 함께 읽으면, 준비된 문서 구조, 실행 가능한 검증, 실제 작업 성공을 서로 다른 단계로 다뤄야 한다는 점이 선명해집니다.

## 이 글에서 다루지 못한 부분

전체 강의와 번역본의 내용 일치, frontier 제품별 설계 해설의 외부 원문 대조, Project 01 제품 코드 및 나머지 프로젝트의 전체 구현, 문서 사이트·PDF·스크린샷 배포 파이프라인은 상세 분석하지 않았습니다. 모델 제공자 연결, 실제 에이전트 세션의 전후 성능, 그래프 실행 및 장애 복구도 검증하지 않았습니다. 이 글의 구현상 판단은 고정 커밋의 `harness-creator` 핵심 스크립트와 명시한 교육용 코드에 한정됩니다.
