---
type: "Repo Review"
title: "[Repo Review] security-audit-skill — AI가 찾은 취약점을 보고서에 올리기까지"
description: "Cloudflare security-audit-skill의 범위 장부·독립 검증·JSON 검사기를 따라가며, 기록의 일관성과 실제 취약점 실증의 경계를 설명합니다."
date: "2026-11-27"
tags:
  - "Repo Review"
  - "Tools"
  - "AI Agent"
resource: "https://github.com/cloudflare/security-audit-skill/tree/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8"
generated:
  by: "process:blog-review"
  at: "2026-11-27T06:09:25.967687+09:00"
sources:
  - id: "github:cloudflare/security-audit-skill"
    resource: "https://github.com/cloudflare/security-audit-skill/tree/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8"
    title: "security-audit"
    author: "Cloudflare, Inc."
status: "stable"
year: "2026"
analyzed_at: "2026-11-27T06:09:25.967687+09:00"
source_id: "cloudflare/security-audit-skill"
source_revision: "c1c8a8c1471069fb0e188eeaff69b8e8db6564a8"
source_type: "repo"
source_url: "https://github.com/cloudflare/security-audit-skill/tree/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8"
visual_sources:
  - path: "img/reviews/2026/cloudflare-security-audit-skill-review/audit-workflow.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/README.md#L9-L20"
    caption: "탐색·후보 검증·최종 기록 검증을 나누는 여섯 단계. 리뷰어 작성, 분석 커밋 기준."
  - path: "img/reviews/2026/cloudflare-security-audit-skill-review/validation-boundary.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/validate-findings.cjs#L703-L756"
    caption: "JSON 검사와 실제 취약점 확인의 역할 구분. 리뷰어 작성, 분석 커밋 기준."
---

## 들어가며: 발견했다는 말 다음에 필요한 것

코딩 에이전트에게 보안 검토를 맡겼을 때, 의심스러운 코드를 많이 찾는 것과 실제로 고쳐야 할 취약점을 가려내는 것은 다른 일입니다. 권한 검사 하나가 눈에 띄지 않아도 앞단에서 이미 요청을 막고 있을 수 있습니다. 반대로 한 파일의 검사가 멀쩡해 보여도 같은 데이터에 접근하는 다른 경로가 비어 있을 수 있습니다.

Cloudflare의 **security-audit-skill**은 이런 검토를 여러 에이전트의 역할과 기록 형식으로 나눕니다. 조사 범위를 먼저 기록하고, 발견한 후보를 다른 에이전트가 반박해 보고, 마지막에는 보고서에 들어갈 구조화된 기록을 다시 검증하도록 설계했습니다. [README의 여섯 단계](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/README.md#L9-L20)가 이 저장소를 읽는 출발점입니다.

README는 이 스킬을 Cloudflare의 취약점 발견 하네스가 발전하기 전의 단일 저장소용 출발점이라고 소개합니다. 여기서 **하네스(harness)**는 에이전트의 작업 순서·도구·검증·결과물을 묶는 실행 환경을 뜻합니다. 이 글에서는 후속 사내 시스템의 성능이 아니라 공개된 스킬의 문서와 검사기 코드를 살펴봅니다. [프로젝트가 밝힌 관계](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/README.md#L3-L5)입니다.

분석 커밋은 `c1c8a8c1471069fb0e188eeaff69b8e8db6564a8`입니다. 스킬을 설치하거나 활성화하지 않았고, 대상 코드·테스트·검사기를 실행하지 않았습니다. 아래의 감사 절차는 문서의 규정이며, 검사기 동작은 소스에서 추적한 내용입니다.

## 무엇인가: 보안 검토의 역할과 증거를 정하는 스킬

이 저장소는 **코딩 에이전트의 보안 감사 지침과 결과물 검사기 묶음**입니다. 중요한 개념은 신뢰 경계입니다. 외부 사용자가 보낸 값이 서버의 권한으로 파일을 읽게 된다면, 그 사이에는 “누가 어떤 파일을 읽을 수 있는가”라는 경계가 있습니다. 스킬은 입력부터 실제 효과까지 따라가며 기존 방어 제어도 확인하도록 요구합니다. [검증자의 확인 항목](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/VALIDATION-AND-REPORTING.md#L24-L39)에 이 기준이 구체적으로 나옵니다.

**부모 에이전트**는 공유 기록과 작업 배분을 소유합니다. **조사자(hunter)**는 맡은 범위에서 후보를 찾습니다. **검증자(verifier)**는 자신이 찾지 않은 후보를 확인합니다. 특정 플랫폼의 에이전트 이름보다 역할과 독립성을 보존하도록 합니다. [역할 정의](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/SKILL.md#L20-L29)와 [조사자의 쓰기 범위](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/HUNTING.md#L5-L9)를 보면, 조사자가 곧바로 공유 보고서나 대상 소스를 고치는 구조가 아닙니다.

최종 판정도 세 가지로 나뉩니다.

| 판정 | 뜻 | 기록해야 할 것 |
| --- | --- | --- |
| `confirmed` | 소스 경로와 제한된 로컬 관찰 결과로 확인한 취약점 | 원인·조건·재현 입력·절차·관찰 결과·수정 전략·심각도·확신도 |
| `needs_validation` | 소스 근거는 있지만 결정적 사실이 미확인인 후보 | 주장하는 원인·정확한 장애 요인·로컬 또는 배포 환경 확인 계획. 심각도는 금지합니다. |
| `rejected` | 소스나 관찰 가능한 제어 등으로 반박된 후보 | 근거 경로와 기각 이유. 확정 취약점 목록에 넣지 않습니다. |

이는 라벨만 바꾼 같은 데이터가 아닙니다. [판정별 출력 계약](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/VALIDATION-AND-REPORTING.md#L95-L109)은 허용·필수 필드를 구분합니다. “왠지 위험하다”는 생각을 `needs_validation`에 쌓아 두는 것도 허용하지 않습니다. 어느 경계의 어떤 사실이 미확인인지 설명해야 합니다.

## 아키텍처: 문서와 두 검사기의 역할

주요 파일은 `skills/security-audit/`에 모여 있습니다. 에이전트가 읽는 작업 문서와 의존성 없는 Node.js 검사기가 중심입니다. [파일 목록](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/README.md#L24-L47)과 [요구 환경](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/README.md#L86-L90)을 정리하면 다음과 같습니다.

| 구성 | 책임 |
| --- | --- |
| `SKILL.md` | 전체 모드, 실행 경계, 프로필·예산, 공통 원칙 |
| `RECONNAISSANCE.md` | 제품·입력·권한 경계 조사, 이전 결과 대조, 범위 장부 생성 |
| `HUNTING.md` | 장부에서 작업 배분, 결과 회수, 누락 점검 |
| `ATTACK-CLASSES.md`와 분야별 문서 | 조사 관점과 분야별 확인 항목 |
| `VALIDATION-AND-REPORTING.md` | 후보 독립 검증, 최종 기록 재검증, 보고서 생성 |
| `report-schema.json` | findings의 판정별 필수·허용 필드 |
| `validate-findings.cjs` | 스키마와 finding 전용 추가 규칙 검사 |
| `validate-coverage-ledger.cjs` | 범위 식별자, 상태, 담당자와 증거 기록의 일관성 검사 |

![지형 파악과 분담 조사, 후보 검증과 JSON 기록, 기록 재검증과 보고서 생성으로 이어지는 여섯 단계]({{ '/img/reviews/2026/cloudflare-security-audit-skill-review/audit-workflow.svg' | relative_url }})

탐색·후보 검증·최종 기록 검증을 나누는 여섯 단계입니다. 리뷰어 작성, 분석 커밋 기준. 출처: [워크플로 개요](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/README.md#L9-L20), [최종 재검증](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/VALIDATION-AND-REPORTING.md#L120-L147).
{: .caption}

그림은 문서가 에이전트에게 요구하는 절차를 다시 그린 것입니다. Node.js 프로그램 하나가 여섯 단계를 자동 실행하는 호출 그래프라는 뜻은 아닙니다. 검사기 CLI의 실제 입력과 출력은 뒤에서 따로 보겠습니다.

## 작동 원리: 범위에서 후보로, 후보에서 기록으로

### 1. 무엇을 살폈는지 남기는 coverage ledger

첫 단계의 출력은 아키텍처 요약과 **coverage ledger**, 즉 검토 범위 장부입니다. 한 단위는 보통 **입력 표면 × 신뢰 경계 × 하위 시스템 × 공격 유형**의 조합입니다. 수명주기 구분이 중요하면 그 차원도 추가합니다. “인증 검토 완료”보다 어느 입력과 어느 권한 경계를 어떤 관점에서 확인했는지 좁게 기록합니다. [장부 생성 규칙](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/RECONNAISSANCE.md#L90-L104)에 이 구성이 나옵니다.

문서의 예시에서 식별에 필요한 부분만 발췌하면 다음과 같습니다. 실제 발견 결과가 아닌 **장부 구조 설명용 예시**입니다.

```json
{
  "canonical_refs": {
    "surface": "src/router.ts#POST /users/:id",
    "boundary": "src/authz.ts#requireOwner",
    "subsystem": "packages/api",
    "attack_class": "ATTACK-CLASSES.md#Access control"
  }
}
```

출처: [장부 예시 일부](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/RECONNAISSANCE.md#L106-L133). 다른 필수 필드가 빠진 발췌이므로 검사기에 넣을 완성 JSON은 아닙니다.

`canonical_refs`는 표시 이름과 별개인 안정적인 소스 식별자입니다. 담당자나 판정이 바뀌어도 같은 경계의 이력이 이어져야 하기 때문입니다. `canonicalCoverageId()`는 정해진 순서의 참조를 UTF-8 바이트 기준으로 퍼센트 인코딩해 `::`로 합칩니다. NFC 정규형이 아닌 문자열은 조용히 수정하지 않고 거부합니다. [정규 참조와 ID 생성](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/validate-coverage-ledger.cjs#L348-L375)에서 확인할 수 있습니다.

상태도 단순 완료 표시가 아닙니다. `covered`는 담당자와 검토 경로·검사 기록이 있어야 합니다. `blocked`에는 미해결 장애도 필요합니다. `deferred`와 `out_of_scope`는 담당자와 현재 증거를 비우고 미검토 이유를 남깁니다. 검사기는 [상태별 분기](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/validate-coverage-ledger.cjs#L518-L566)로 이 조건을 확인합니다. 다만 `covered`는 해당 단위를 검토했다는 주장이지 모든 취약점이 없다는 증명은 아닙니다.

### 2. 체크리스트는 실제 경계에 맞춰 고릅니다

`ATTACK-CLASSES.md`는 주입, 접근 제어, 파일 처리, 암호·비밀, 비즈니스 로직 등의 관점을 제공합니다. 여기에 AI·LLM, 웹 인증, 공급망, 클라우드, 데이터 격리, 데스크톱·로컬 IPC 같은 분야별 문서를 붙일 수 있습니다. [공격 유형과 보조 문서](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/ATTACK-CLASSES.md#L3-L40)의 관계입니다.

선택 기준은 기술 이름이 아니라 **소스에서 확인한 경계**입니다. 라이브러리 이름이 보였다는 이유만으로 분야 문서를 붙이지 않습니다. 선택한 세부 블록과 제외 이유를 장부에 남기고, 조사자에게 실제 블록 내용을 전달합니다. [선택 원칙](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/RECONNAISSANCE.md#L73-L88)과 [프롬프트 구성](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/HUNTING.md#L13-L25)이 연결됩니다.

조사가 끝나면 별도의 **coverage critic**이 매핑되지 않은 진입점, 나란한 우회 경로, 증거 없이 닫힌 단위, 이전에 막힌 작업 등을 점검합니다. 이 역할은 새로운 취약점 판정 대신 누락된 조사 범위를 제안합니다. `standard`·`deep`은 후속 조사와 별도 최종 점검을 반복할 수 있습니다. `quick`은 조사 묶음 한 번과 최종 점검으로 끝내고 새로 발견한 남은 작업을 `deferred`로 기록합니다. [누락 점검과 반복 조건](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/HUNTING.md#L221-L251)의 차이입니다.

### 3. 찾은 사람과 확인하는 사람을 나눕니다

후보는 fingerprint라는 안정적인 식별자로 합쳐집니다. 같은 원인이 여러 경로에 나타나도 중복 후보로 부풀리지 않도록 합니다. 새 검증자는 현재 소스를 다시 읽고 입력부터 효과까지의 경로와 가장 강한 방어 제어를 재구성합니다. 목표는 후보에 동의하는 것이 아니라 반박할 수 있는지 확인하는 것입니다. [중복 통합](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/HUNTING.md#L219-L219)과 [독립 검증 지침](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/VALIDATION-AND-REPORTING.md#L3-L45)에 이 원칙이 있습니다.

결정적인 로컬 재현에는 운영체제 수준 격리, 외부 네트워크 차단, 허용 목록으로 만든 빈 환경, 자원 제한, scratch 디렉터리만의 쓰기 권한을 요구합니다. 통제가 없으면 실행하지 않습니다. 재현 과정이 만든 파일도 즉시 보존 증거로 쓰지 않습니다. 신뢰된 부모 측 코드가 사전 허용한 파일의 경로·종류·크기 등을 확인한 뒤 `artifacts/`로 옮기도록 합니다. [실행 경계](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/SKILL.md#L31-L42)와 [산출물 승격 절차](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/VALIDATION-AND-REPORTING.md#L48-L85)의 요구입니다.

이는 문서의 요구 사항입니다. 스킬 자체가 샌드박스나 모든 플랫폼의 승격기를 구현해 준다고 해석해서는 안 됩니다. 실제 실행 환경이 통제를 제공하는지 확인할 책임이 남습니다.

### 4. findings 검사기의 입력은 소스가 아니라 JSON입니다

`validate-findings.cjs`의 진입점은 `run(process.argv[2])`입니다. 받는 것은 **이미 작성된 findings JSON 파일의 경로**입니다. 같은 디렉터리의 스키마를 읽고 입력을 제한된 방식으로 연 뒤, JSON의 크기·중첩 제한과 문법을 확인하고 레코드를 검사합니다. [CLI 본체](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/validate-findings.cjs#L703-L756)와 [진입점](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/validate-findings.cjs#L759-L773)을 단순화하면 다음과 같습니다.

아래는 소스와 대조해 단순화한 의사코드이며 실행 결과가 아닙니다.

```text
file = argv[2]
없으면 usage 출력, 종료 1
schema = loadSchema(같은 디렉터리의 report-schema.json)
contents = readFileWithinLimit(file)
enforceJsonTextLimits(contents)
findings = JSON.parse(contents)
errors = validateDocument(findings, schema)
오류가 있으면 오류 목록 출력, 종료 1
없으면 PASS와 레코드 수 출력, 종료 0
파일 읽기·파싱·스키마 로딩 실패도 종료 1
```

출처: [입력 읽기](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/validate-findings.cjs#L597-L649), [JSON 사전 제한](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/validate-findings.cjs#L651-L701), [출력과 종료 코드](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/validate-findings.cjs#L703-L756).

입력은 no-follow·nonblocking 플래그로 열어 일반 파일인지 확인하고 최대 5 MiB를 읽습니다. 읽는 중에도 크기 상한을 재확인하며 잘못된 UTF-8을 거부합니다. 여기의 no-follow는 코드가 여는 **입력 파일 자체**에 적용됩니다. 모든 상위 디렉터리를 검사하는 앞선 증거 승격 절차와 동일한 구현은 아닙니다.

`validateDocument()`는 지원되는 스키마인지 확인하고 데이터 제한, 스키마 검사, finding 전용 의미 규칙을 순서대로 적용합니다. JSON Schema 전체가 아니라 이 저장소에서 쓰는 키워드를 구현한 해석기입니다. [호출 순서](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/validate-findings.cjs#L585-L602)와 [스키마 분기·필수 필드](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/validate-findings.cjs#L350-L405)를 보면 `oneOf`의 정확히 한 분기에 맞아야 하고 허용하지 않은 추가 필드는 거부됩니다.

추가 규칙은 fingerprint 중복·정렬, 소스 상대 경로 형태, 양수 줄 번호를 검사합니다. 여러 단계의 trace는 `entrypoint`로 시작해 `propagation`을 거쳐 `sink`로 끝나야 합니다. `confirmed`는 보이는 글자가 있는 `observed_result`와 수정 전략이 필요하고, 전체 심각도는 입증한 영향 등급보다 높을 수 없습니다. `needs_validation`에는 심각도를 넣을 수 없고 로컬 또는 배포 확인 계획이 하나 이상 필요합니다. [판정별 의미 검사](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/validate-findings.cjs#L485-L583)의 내용입니다.

하지만 **관찰 결과 문자열이 있다는 것과 그 관찰이 사실이라는 것은 다릅니다.** CLI는 인용된 대상 소스를 읽어 실제 줄의 동작과 주장을 대조하거나 재현 절차를 실행하지 않습니다. 이 일은 독립 검증 단계가 담당합니다. 문서도 검사기 성공은 형식과 장부 일관성만 입증한다고 명시합니다. [성공의 한계](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/VALIDATION-AND-REPORTING.md#L111-L118)가 특히 중요합니다.

![JSON 검사기의 필드·상태·경로 규칙과 에이전트의 소스·제한된 관찰 결과 확인을 구분한 도식]({{ '/img/reviews/2026/cloudflare-security-audit-skill-review/validation-boundary.svg' | relative_url }})

JSON 검사와 실제 취약점 확인은 다른 작업입니다. 리뷰어 작성, 분석 커밋 기준. 출처: [findings CLI](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/validate-findings.cjs#L703-L756), [후보 검증](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/VALIDATION-AND-REPORTING.md#L24-L39).
{: .caption}

### 5. ledger 검사기는 상태와 증거 소유권을 대조합니다

`validate-coverage-ledger.cjs`도 argv의 파일 경로에서 제한된 입력 읽기, JSON 사전 점검·파싱, `validateDocument()`, 결과 출력으로 이어집니다. 성공은 종료 `0`, 입력·형식·검증 실패는 종료 `1`입니다. [ledger CLI](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/validate-coverage-ledger.cjs#L808-L872)를 정적으로 추적한 결과입니다.

ledger는 참조로 계산한 `coverage_id`가 기록과 맞는지, ID가 중복되거나 같은 의미 조합이 다른 참조로 표현되지 않았는지, 정렬되어 있는지 검사합니다. 각 검사 기록에는 담당자와 검토 경로가 있어야 하며 단위 전체 경로는 개별 기록 경로의 합집합과 같아야 합니다. [단위 필드](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/validate-coverage-ledger.cjs#L646-L718), [소유 경로 대조](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/validate-coverage-ledger.cjs#L421-L469), [중복·정렬 검사](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/validate-coverage-ledger.cjs#L761-L806)가 이를 나눠 맡습니다.

소스만 읽은 검사는 `method: "source"`, `artifact: null`이어야 합니다. 로컬 검사는 담당자 자신의 `agents/<agent-id>/artifacts/` 아래 경로를 요구합니다. 재배정하면 과거 시도를 `attempts`에 남기고 새 담당자와 새 증거를 사용하게 합니다. [증거 경로 검사](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/validate-coverage-ledger.cjs#L394-L449)와 [과거 시도 검사](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/validate-coverage-ledger.cjs#L568-L644)의 역할입니다.

여기에도 경계가 있습니다. 코드는 산출물 **경로 문자열의 소유권 규칙**을 검사합니다. 실제 파일의 존재·내용이나 공격 유형 블록의 적합성을 검증하지는 않습니다. 이 CLI에는 findings 파일 인자도 없습니다. 따라서 파일 사이 후보 판정의 연결과 실제 검토 범위의 충분성은 부모 에이전트와 독립 검토 절차가 계속 책임져야 합니다.

### 6. 최종 기록을 다시 확인한 뒤 보고서를 만듭니다

`standard`·`deep`은 후보 검증 뒤에도 `confirmed`와 `needs_validation` 기록을 새 검증자가 확인합니다. 원인·재현 입력·관찰 결과·영향·심각도를 실질적으로 바꾼 수정안은 또 다른 독립 검증자가 확인해야 합니다. **`quick`에서는 후보 검증과 최종 기록 검증을 같은 새 검증자 한 명의 검토로 합칩니다.** 확정 기록의 독립 검토 자체를 생략하지는 않습니다. [최종 검증과 수정안 처리](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/VALIDATION-AND-REPORTING.md#L120-L149)의 규칙입니다.

예산이 끝나 검증하지 못한 후보를 `needs_validation`으로 바꿔 findings에 넣는 것은 금지합니다. 장부의 미해결 후보로만 남기고 실행을 `incomplete`로 표시합니다. **독립 검증을 받지 못함**과 **검증을 받았지만 특정 실행·배포 사실이 미확인임**을 구별하는 것입니다. [예산 소진 규칙](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/SKILL.md#L119-L134)이 이 차이를 지킵니다.

최종 결과물은 다음과 같습니다.

| 결과물 | 포함 내용 |
| --- | --- |
| `REPORT.md` | 범위·프로필·예산·누락, 확정 취약점, 검증 필요 목록, 범위 집계 |
| `FINDINGS-DETAIL.md` | `medium` 이상 확정 기록의 경로·로컬 재현·수정안 |
| `NEEDS-VALIDATION.md` | 심각도 없는 미확인 후보와 이를 해소할 계획 |

보고서 문장은 최종 JSON의 판정이나 심각도를 강화할 수 없습니다. 미완료 실행도 독립 검증된 기록을 보고할 수 있지만, 검증하지 못한 장부 후보를 취약점으로 소개해서는 안 됩니다. 확정 발견이 0개라면 그 결과와 남은 범위를 그대로 적습니다. [보고서 생성 계약](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/VALIDATION-AND-REPORTING.md#L151-L186)의 내용입니다.

## 설치와 사용: 문서의 명령과 실행 환경

같은 커밋의 README는 Skills CLI 설치 명령을 안내합니다. 아래는 문서 소개이며 이번 리뷰에서 실행하지 않았습니다. 명령 자체가 SHA를 고정하지 않으므로 이후 설치되는 내용이 이 글의 분석 커밋과 같다고 가정할 수 없습니다.

```bash
npx skills add https://github.com/cloudflare/security-audit-skill \
  --skill security-audit
```

출처: [설치 안내](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/README.md#L49-L66).

사용 예시로는 `security audit this codebase`나 `find security vulnerabilities in ./src` 같은 요청이 나옵니다. 전체 감사는 결과물을 만드는 full audit 모드, 보안 질문과 집중된 취약점 검토는 보고서를 요청하지 않으면 guidance 모드를 사용합니다. 기본 출력 위치는 `~/security-audit-skill/<repo-name>/run-<N>`입니다. [모드·출력 위치·요구 환경](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/README.md#L68-L90)을 확인할 수 있습니다.

결과 파일에는 다음 두 검사 명령을 사용하도록 합니다. 꺾쇠 안은 실제 경로로 바꿀 자리표시자입니다. 이것도 실행 검증 결과가 아닙니다.

```bash
node <skill-dir>/validate-findings.cjs <output-dir>/findings.json
node <skill-dir>/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json
```

출처: [공식 검사 명령](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/VALIDATION-AND-REPORTING.md#L111-L118).

Node.js와 도구 호출·병렬 하위 에이전트를 지원하는 코딩 에이전트가 필요합니다. 프로필 기본값은 `standard`입니다. `quick`은 범위와 중복 검토를 줄인 부분 검토이고, `deep`은 하위 시스템·수명주기 구분과 재검토를 더합니다. 어느 프로필에서도 증거 기준을 낮추지는 않습니다. [프로필 규칙](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/SKILL.md#L107-L117)의 차이입니다.

## 한계와 주의점: 형식이 맞아도 결론은 틀릴 수 있습니다

독립 검토가 실제 실행에서 유지되는지, 검증자가 필요한 소스를 충분히 읽는지, 샌드박스가 강제되는지는 호스트 에이전트와 실행 환경에 달려 있습니다. 여섯 단계의 지침과 두 JSON 검사기만으로 전체 감사가 정확하게 수행됐다고 판단할 수는 없습니다.

검사기에는 입력 상한도 있습니다. findings는 5 MiB·최대 1,000개 레코드·64단계 중첩 등의 제한, ledger는 5 MiB·최대 10,000개 단위·중첩 컬렉션 1,000개 등의 제한이 있습니다. 큰 장부는 단위 수 상한보다 파일 크기 제한에 먼저 닿을 수 있습니다. [findings 제한](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/VALIDATION-AND-REPORTING.md#L118-L118)과 [ledger 제한](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/RECONNAISSANCE.md#L156-L156)에 명시된 조건입니다. 이번 리뷰에서는 처리량이나 탐지 성능을 측정하지 않았습니다.

호환되는 과거 장부가 없다는 사실을 “이전에 확인한 문제가 없다”로 읽어도 안 됩니다. 문서는 장부 누락·비호환을 기록하고 과거 보류·차단·범위 제외와 변경된 소스를 현재 작업으로 돌리도록 합니다. [이전 결과 대조](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/RECONNAISSANCE.md#L59-L71)는 반복 실행에서 중요한 부분입니다.

라이선스는 **MIT**이고 저작권자는 Cloudflare, Inc.입니다. 복제·수정·배포 등의 권한과 함께 복사본 또는 상당 부분에 저작권·허가 고지를 포함할 조건과 무보증 조항이 있습니다. [LICENSE](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/LICENSE#L1-L21)를 확인했습니다. 본문의 도식은 원본 그림 복제가 아닌 리뷰어의 요약도입니다.

## 결론: 무엇을 확인하지 못했는지도 드러내는 보고서

이 스킬의 중심에는 장부와 판정 계약이 있습니다. 장부는 조사 범위와 누락을 남기고, 판정 계약은 소스 근거·관찰 결과·미확인 사실을 구별합니다. 독립 검증자는 의심을 반박하고, JSON 검사기는 결론을 기록하는 형식과 상태 관계를 점검합니다. 이 역할들이 이어져야 확정 주장과 다음 확인 과제를 구분할 수 있습니다.

### 이 글에서 다루지 못한 부분

README, 각 단계의 주요 규칙, 두 검사기의 대표 입출력·상태·의미 검증 경로와 스키마를 정적으로 확인했습니다. 분야별 보조 문서는 목록과 선택 원칙, AI·웹 인증 분야의 대표 경계를 확인했으며 모든 공격 유형을 개별 평가하지는 않았습니다. 테스트를 실행하지 않았고, 실제 발견률·오탐률·모델별 비용·호스트 플랫폼의 격리 구현·후속 Cloudflare 내부 하네스는 평가하지 않았습니다.
