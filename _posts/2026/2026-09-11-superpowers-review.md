---
title: "Superpowers 코드 리뷰: 코딩 에이전트의 개발 절차를 스킬과 파일로 구성하는 방법"
summary: "Superpowers 6.3.0의 세션 초기화, 스킬 선택, 계획 분해와 리뷰 흐름을 추적하고 코드가 보장하는 동작과 자연어 지침의 경계를 분석합니다."
date: "2026-09-11T06:00:00+09:00"
year: "2026"
tags: [AI, Agents, Developer-Tools, Code-Review]
source_type: repo
source_id: "obra/superpowers"
source_revision: "b36e0829c6d0140e93cfef2ca599b1b07d4a7797"
source_url: "https://github.com/obra/superpowers/tree/b36e0829c6d0140e93cfef2ca599b1b07d4a7797"
analyzed_at: "2026-09-11T06:07:24+09:00"
---

## 들어가며

코딩 에이전트에게 기능 구현을 맡기면 코드를 생성하는 능력만큼이나 **언제 설계를 확인하고, 어떤 범위로 작업을 나누며, 무엇을 근거로 완료를 선언할지**가 중요해집니다. Superpowers는 이러한 개발 절차를 재사용 가능한 스킬로 구성한 프로젝트입니다. README는 설계 합의, 구현 계획, 작업별 에이전트 실행, 테스트와 리뷰를 연결하는 소프트웨어 개발 방법론으로 설명합니다. [README의 정의와 흐름](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/README.md#L1-L43)

이 글은 버전 `6.3.0`을 표시하는 커밋 `b36e0829c6d0140e93cfef2ca599b1b07d4a7797`의 소스를 정적으로 읽은 리뷰입니다. 대상의 설치 명령, 서버, 테스트, 에이전트 작업은 실행하지 않았습니다. 따라서 아래의 동작 설명은 코드와 문서에서 확인한 경로이며, 실제 모델의 지침 준수율이나 작업 성공률을 측정한 결과는 아닙니다. [버전 매니페스트](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/package.json#L1-L22)

## Superpowers는 무엇인가

Superpowers는 **코딩 에이전트가 사용할 개발 절차를 Markdown 스킬로 제공하고, 각 실행 환경이 이를 발견하고 읽도록 연결하는 플러그인**입니다. 여기서 실행 환경, 즉 harness는 모델에 파일 읽기·셸·에이전트 호출 같은 도구와 대화 수명주기를 제공하는 프로그램을 뜻합니다. Superpowers는 이 환경에 맞는 얇은 연결 코드를 두고, 계획·테스트·리뷰 지침을 공통 자산으로 재사용합니다. [공통 스킬의 플랫폼 적응](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/using-superpowers/SKILL.md#L52-L63), [OpenCode 연결 코드](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/.opencode/plugins/superpowers.js#L55-L113)

핵심 기능은 요청을 설계로 구체화하는 `brainstorming`, 구현 단위를 정하는 `writing-plans`, 작업자와 리뷰어를 운영하는 `subagent-driven-development`, 테스트 우선 개발과 완료 검증입니다. 다만 이 이름들이 항상 별도 프로그램을 의미하지는 않습니다. 예를 들어 TDD 스킬의 “먼저 실패하는 테스트를 확인한다”는 규칙은 모델에 전달되는 자연어 절차입니다. 테스트를 통과하지 않은 도구 호출을 커널이나 권한 계층에서 차단하는 장치로 해석해서는 안 됩니다. [TDD 본문](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/test-driven-development/SKILL.md#L8-L45)

## 아키텍처: 공통 지침과 실행 환경별 연결

분석한 중심 경로는 다음과 같습니다.

| 구성 | 입력 | 책임과 출력 |
|---|---|---|
| `skills/using-superpowers/SKILL.md` | 새 요청과 현재 작업 맥락 | 관련 스킬을 먼저 확인하도록 하는 진입 지침 |
| `hooks/hooks.json`, `hooks/session-start` | 세션 시작 이벤트, 플러그인 경로 | 공통 진입 스킬을 읽어 JSON 컨텍스트 출력 |
| `.opencode/plugins/superpowers.js` | 설정 객체와 메시지 배열 | 스킬 검색 경로 등록, 첫 사용자 메시지에 초기 지침 삽입 |
| `.pi/extensions/superpowers.ts` | 리소스 발견·세션·컨텍스트 이벤트 | 스킬 경로 노출, 시작 및 압축 후 초기 지침 삽입 |
| `.codex-plugin/plugin.json` | Codex의 플러그인 로딩 | 스킬 경로와 인터페이스 메타데이터 선언 |
| `skills/subagent-driven-development/scripts/` | 계획 파일, 작업 번호, Git 커밋 범위 | 작업별 요구사항 파일과 리뷰용 diff 파일 생성 |

각 행은 실제 진입 파일의 책임을 요약한 것입니다. 공통 훅은 [훅 등록](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/hooks/hooks.json#L1-L17), 플랫폼 연결은 [Pi 이벤트](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/.pi/extensions/superpowers.ts#L16-L56)와 [Codex 매니페스트](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/.codex-plugin/plugin.json#L23-L39), 파일 생성은 [작업 추출기](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/subagent-driven-development/scripts/task-brief#L17-L41)에서 확인할 수 있습니다.

루트 `package.json`에는 일반적인 외부 패키지 의존성 목록이 없으며, OpenCode용 진입점과 Pi용 확장·스킬 경로가 선언되어 있습니다. 그러나 이를 실행 환경 의존성까지 없다는 뜻으로 읽으면 안 됩니다. 공통 훅은 Bash를 사용하고 작업 파일 생성 도구는 Git과 awk 등을 호출하며, Pi 확장은 호스트가 제공하는 이벤트 API에 연결됩니다. [패키지 선언](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/package.json#L1-L22), [Bash 실행 래퍼](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/hooks/run-hook.cmd#L18-L46)

## 작동 원리

### 1. 세션 시작 시 스킬 사용법을 컨텍스트에 넣습니다

Claude Code용 훅 설정은 `SessionStart`의 `startup|clear|compact` 이벤트에 동기식 명령을 연결합니다. 명령은 `run-hook.cmd`를 거쳐 `session-start`로 들어갑니다. 세션 초기화 스크립트는 자신의 위치에서 플러그인 루트를 찾고, `using-superpowers/SKILL.md` 전체를 읽어 JSON 문자열로 이스케이프합니다. 이후 현재 환경에 맞는 키를 사용해 출력합니다. Cursor는 `additional_context`, Claude Code는 중첩된 `hookSpecificOutput.additionalContext`, 그 외 분기는 최상위 `additionalContext`를 사용합니다. [이벤트 등록](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/hooks/hooks.json#L3-L12), [초기화와 출력 분기](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/hooks/session-start#L6-L47)

이 경로의 입력은 스킬 파일이고 출력은 **모델이 읽게 될 컨텍스트**입니다. 스크립트 자체가 요구사항을 분류하거나 구현자를 호출하지는 않습니다. 초기 지침을 받은 모델이 관련 스킬을 선택하고, 해당 스킬이 지시하는 절차를 실행하는 구조입니다. 진입 스킬은 기능 개발에는 brainstorming, 버그 수정에는 systematic-debugging 같은 절차 스킬을 우선하도록 설명합니다. [스킬 선택 규칙](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/using-superpowers/SKILL.md#L18-L31)

즉, 코드로 직접 수행되는 부분은 파일 읽기·문자열 변환·출력 형식 선택입니다. “관련 스킬을 응답 전에 호출한다”는 부분은 자연어 지침에 대한 모델의 행동입니다. README의 자동 활성화 설명도 이 두 층을 나누어 이해해야 합니다.

### 2. OpenCode는 스킬 검색 경로와 메시지 배열을 연결합니다

OpenCode 플러그인은 `config` 훅에서 `config.skills.paths` 배열을 준비하고 공통 `skills` 디렉터리가 없으면 추가합니다. 별도 심볼릭 링크를 전제로 하지 않고 호스트 설정 객체에 경로를 등록하는 코드입니다. 초기 지침을 만드는 함수는 `using-superpowers` 본문에서 front matter를 제거하고 OpenCode의 도구 이름 대응표를 덧붙입니다. 파일 읽기와 파싱 결과는 모듈 수준 캐시에 저장됩니다. [검색 경로 등록](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/.opencode/plugins/superpowers.js#L102-L113), [본문 로딩과 캐시](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/.opencode/plugins/superpowers.js#L49-L100)

메시지 변환의 핵심은 첫 사용자 메시지를 찾아 텍스트 조각을 앞에 넣는 부분입니다. 다음은 실제 코드의 일부이며, 중간 주석은 생략했습니다. [원문 코드 124~136행](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/.opencode/plugins/superpowers.js#L124-L136)

```javascript
'experimental.chat.messages.transform': async (_input, output) => {
  const bootstrap = getBootstrapContent();
  if (!bootstrap || !output.messages.length) return;
  const firstUser = output.messages.find(m => m.info.role === 'user');
  if (!firstUser || !firstUser.parts.length) return;

  if (firstUser.parts.some(p => p.type === 'text' && p.text.includes('EXTREMELY_IMPORTANT'))) return;

  const ref = firstUser.parts[0];
  firstUser.parts.unshift({ ...ref, type: 'text', text: bootstrap });
}
```

여기에는 서로 다른 두 중복 방지 장치가 있습니다. `_bootstrapCache`는 파일을 반복해서 읽는 작업을 줄이고, 메시지 내 표식 검사는 이미 변환한 메시지 배열에 같은 지침을 두 번 넣는 일을 피합니다. 캐시가 있다고 메시지 삽입까지 한 번만 수행하는 것은 아닙니다. 호스트가 새 메시지 배열을 다시 전달하면 필요한 삽입을 다시 할 수 있습니다. [캐시와 메시지 변환 설명](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/.opencode/plugins/superpowers.js#L115-L136)

도구 이름 대응표 역시 실행 어댑터 함수가 아니라 본문에 포함되는 문자열입니다. 예를 들어 하위 에이전트 요청을 OpenCode의 `task`로 대응시키라는 설명을 모델에 전달합니다. 공통 스킬을 유지하면서 도구 이름 차이를 자연어로 흡수하는 선택입니다. [도구 대응표](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/.opencode/plugins/superpowers.js#L76-L87)

### 3. 대화 압축과 플랫폼 차이에 대응합니다

Pi 확장은 `session_start`와 `session_compact`에서 `injectBootstrap`을 켜고, `agent_end`에서 끕니다. `context` 이벤트에서는 이미 표식이 있는지 검사한 뒤 초기 지침 메시지를 삽입합니다. 삽입 위치는 앞부분에 연속된 `compactionSummary` 메시지 다음입니다. 이는 대화를 압축한 요약은 앞에 두면서 이후 모델 입력에 지침을 다시 포함시키는 구현입니다. [상태와 메시지 삽입](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/.pi/extensions/superpowers.ts#L16-L56), [삽입 위치 계산](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/.pi/extensions/superpowers.ts#L100-L121)

모든 플랫폼이 동일한 경로를 갖지는 않습니다. **이 커밋의 Codex 매니페스트는 `skills`를 선언하지만 `hooks`는 빈 객체입니다.** 또한 Codex 배포 패키지를 만드는 스크립트는 루트 `hooks/`를 포함하지 않고, 이전 공식 패키지에서 스킬별 `agents/openai.yaml` 메타데이터를 가져옵니다. 따라서 Claude Code의 세션 훅이 Codex에도 그대로 실행된다고 설명할 근거는 없습니다. Codex 호스트의 실제 자동 로딩 동작과 배포된 패키지의 내용은 이 소스 체크아웃만으로 전부 확인하지 못했습니다. [Codex 선언](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/.codex-plugin/plugin.json#L23-L24), [패키지 파일 선택과 메타데이터 복사](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/scripts/package-codex-plugin.sh#L233-L282)

### 4. 사용자 요청을 설계와 작업 계획으로 바꿉니다

진입 이후에는 자연어 스킬이 제어 흐름을 설명합니다. `brainstorming`은 요청을 세 가지로 분류합니다. 가능성을 조사하는 Spike는 조사 결과가 산출물이며, 기존 흐름의 작은 변경인 Bounded는 대화 안의 짧은 설계로 진행합니다. 새로운 시스템이나 인터페이스 구조를 바꾸는 Architectural은 명세 파일과 구현 계획까지 작성합니다. 각 경로는 구현 전에 사용자가 의도를 승인하도록 요구합니다. 이것은 스킬에 적힌 정책이며, 이 저장소의 초기화 코드가 승인 여부를 별도 상태 머신으로 판정하는 것은 아닙니다. [세 가지 경로](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/brainstorming/SKILL.md#L14-L61)

상세 계획이 필요한 경우 `writing-plans`는 파일별 책임, 생성·수정·테스트할 경로, 작업이 소비하고 생산하는 인터페이스, 실패 테스트와 최소 구현을 담도록 합니다. 특히 `Global Constraints`에는 프로젝트 전체의 정확한 제약을 보관하고, 개별 작업에는 입출력 인터페이스를 둡니다. 이후 하위 에이전트가 전체 계획을 읽지 않아도 자신이 연결할 함수와 자료형을 알게 하려는 구성입니다. [계획 헤더와 작업 형식](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/writing-plans/SKILL.md#L54-L128)

README는 작업 단위를 2~5분으로 소개하지만, 상세 스킬은 이를 테스트 작성·실행·구현 같은 **개별 단계**의 크기로 설명하고 작업 자체는 독립적으로 테스트하고 리뷰할 수 있는 산출물로 정의합니다. 실제 분할 기준은 분량보다 검증 가능한 책임에 가깝습니다. [README의 표현](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/README.md#L263-L269), [작업 크기의 상세 정의](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/writing-plans/SKILL.md#L36-L52)

### 5. 계획 파일에서 작업별 요구사항을 추출합니다

Subagent-Driven Development, 이하 SDD는 계획을 작업자에게 전달할 때 파일을 중심으로 맥락을 분리합니다. 먼저 `sdd-workspace`가 Git 작업 디렉터리 아래 `.superpowers/sdd/<계획-파일명>/`을 만들고, 상위 디렉터리에 `*`를 담은 `.gitignore`를 기록합니다. 임시 요구사항, 구현 보고서, 리뷰 패키지와 진행 기록을 같은 계획 디렉터리에 묶는 구조입니다. [작업 공간 생성 코드](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/subagent-driven-development/scripts/sdd-workspace#L28-L40)

다음으로 `task-brief`가 계획 파일의 `Task N` 제목부터 다음 작업 제목 직전까지 추출해 기본 경로 `task-N-brief.md`로 저장합니다. 핵심 awk 코드는 다음과 같습니다. [실제 추출 코드](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/subagent-driven-development/scripts/task-brief#L28-L34)

```awk
/^```/ { infence = !infence }
!infence && /^#+[ \t]+Task[ \t]+[0-9]+/ {
  intask = ($0 ~ ("^#+[ \t]+Task[ \t]+" n "([^0-9]|$)"))
}
intask { print }
```

코드 블록 안에 등장하는 `Task` 문자열을 제목으로 오인하지 않도록 fenced code 상태를 토글합니다. 다만 이는 완전한 Markdown 파서가 아닙니다. 줄 시작의 세 backtick을 기준으로 상태를 바꾸며, 물결표 fence나 들여쓴 fence까지 일반적으로 처리하는 로직은 없습니다. 이 추출기는 스킬이 지정하는 계획 형식에 맞춘 작은 도구입니다.

추출되는 것은 작업 본문입니다. 전체 계획의 공통 제약까지 자동 합성하지는 않습니다. 따라서 SDD 지침은 컨트롤러가 전역 제약과 앞선 작업의 인터페이스를 별도로 전달하도록 합니다. 요구사항 파일에는 원래 값이 남고, 호출 메시지는 파일 위치와 연결 맥락만 담습니다. 이는 긴 대화 이력을 모든 작업자에게 반복 전달하는 일을 줄이는 설계라고 해석할 수 있습니다. [작업자 전달 계약](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/subagent-driven-development/SKILL.md#L246-L282)

진행 상태는 `progress.md`에 기록하며, 첫 줄에 계획 파일의 정체성을 명시하고 완료 작업과 수정 회차를 보존하도록 지시합니다. 대화 압축 이후에는 이 기록과 Git 이력을 확인해 재개한다는 정책입니다. 파일 디렉터리 생성은 셸 코드가 수행하지만, 완료 상태 해석·기록·재호출 판단은 에이전트가 지침을 따라 수행합니다. [복구 지침](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/subagent-driven-development/SKILL.md#L124-L160)

### 6. 구현 결과를 커밋 범위로 포장해 리뷰합니다

구현자가 완료하면 `review-package`가 작업 시작 전 `BASE`와 완료 후 `HEAD`를 입력받습니다. 두 참조가 존재하는지 검사한 뒤 커밋 목록, 변경 통계, 주변 10줄을 포함하는 diff를 한 파일에 기록합니다. 작업이 여러 커밋으로 이루어져도 전체 범위를 보존하는 것이 핵심입니다. 마지막 커밋의 부모인 `HEAD~1`만 사용하면 이전 변경이 빠질 수 있습니다. [리뷰 패키지 생성](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/subagent-driven-development/scripts/review-package#L17-L46)

리뷰어에게 전달하는 중심 자료는 요구사항 파일, 구현 보고서, diff 파일의 세 경로와 해당 작업의 전역 제약입니다. 구현 보고서는 주장으로 취급하고 실제 diff와 대조하도록 합니다. 변경 밖의 코드는 구체적인 위험을 지목한 경우에만 확인하도록 범위를 정합니다. 작은 작업 리뷰가 전체 저장소 조사로 계속 확대되는 것을 막으려는 설계입니다. [리뷰 입력과 조사 범위](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/subagent-driven-development/task-reviewer-prompt.md#L21-L71)

여기서 README의 “규격 준수 후 코드 품질의 두 단계 리뷰”를 두 명의 리뷰어가 순서대로 실행된다는 뜻으로 읽으면 실제 템플릿과 달라집니다. **이 커밋의 task reviewer 한 명은 diff를 읽고 규격 준수와 코드 품질의 두 판정을 반환합니다.** 전체 브랜치의 통합 리뷰는 모든 작업이 끝난 후 별도로 수행하도록 되어 있습니다. [README 설명](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/README.md#L269-L275), [실제 리뷰어 계약](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/subagent-driven-development/task-reviewer-prompt.md#L1-L19), [최종 리뷰](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/subagent-driven-development/SKILL.md#L445-L469)

### 7. 수정 반복에 상한을 두고 판단을 기록합니다

SDD는 규격 실패나 Critical·Important 문제에 대해 작업별 최대 5회의 수정·재리뷰를 지시합니다. 1~3회에는 원래 구현자를 다시 호출하고, 4~5회에는 더 높은 역량의 모델을 사용하는 새 구현자로 전환합니다. 재리뷰는 이전 리뷰 이후의 수정 diff에 집중하며, 수정과 무관한 관찰은 별도 기록으로 남깁니다. [수정 루프](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/subagent-driven-development/SKILL.md#L354-L403)

5회 이후에도 남은 항목은 컨트롤러가 근거를 기록해 판단하도록 합니다. 최종 전체 리뷰에도 하나의 수정 묶음과 한 번의 제한된 재리뷰를 두며, 남은 판단은 사용자에게 전달하도록 합니다. 이는 리뷰어를 계속 추가해 무한히 검토하는 방식보다 수정 비용을 제한하려는 정책입니다. 다만 5회 상한은 셸 스크립트의 실행 카운터가 강제하지 않습니다. 모델이 진행 기록을 읽고 정책을 준수해야 합니다. [상한 이후 판단](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/subagent-driven-development/SKILL.md#L405-L443), [최종 판단 전달](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/subagent-driven-development/SKILL.md#L458-L485)

또한 SDD는 여러 구현자를 동시에 보내지 않도록 명시합니다. 작은 동일 형태의 변경은 한 작업자에게 묶어 보낼 수 있지만, 구현 작업 간 충돌을 피하기 위한 기본 흐름은 순차 진행입니다. 따라서 “하위 에이전트를 쓴다”와 “구현을 병렬 처리한다”를 같은 의미로 보면 안 됩니다. [묶음 작업 정책](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/subagent-driven-development/SKILL.md#L223-L229), [병렬 구현 금지](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/subagent-driven-development/SKILL.md#L272-L282)

## 문서 기반 설치와 사용

이 커밋의 README는 실행 환경마다 별도로 설치하도록 안내합니다. Claude Code에서는 공식 마켓플레이스 설치 명령을 제시합니다. 아래는 README에 있는 명령이며 이 리뷰에서 실행하지 않았습니다. [Claude Code 설치 안내](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/README.md#L49-L63)

```text
/plugin install superpowers@claude-plugins-official
```

Codex App은 사이드바 Plugins에서 Superpowers를 찾아 설치하고, Codex CLI는 `/plugins` 검색 인터페이스에서 이름을 검색해 설치하도록 설명합니다. 이는 고정 커밋의 문서 설명이며 현재 마켓플레이스 노출 상태나 설치된 패키지가 이 SHA와 같은지는 별도로 확인하지 않았습니다. [Codex 설치 안내](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/README.md#L92-L116)

설치 이후 사용 흐름은 요청 제시, 설계 합의, 필요한 경우 계획 작성, 구현과 리뷰입니다. 환경에 없는 도구는 플러그인이 자동으로 만들어 주지 않습니다. 예를 들어 Pi용 대응표는 표준 하위 에이전트 도구가 없다고 설명하며, 동반 패키지가 제공하는 도구가 없으면 현재 세션에서 작업하거나 기능 부재를 설명하도록 합니다. [Pi 도구 가용성](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/.pi/extensions/superpowers.ts#L88-L98)

## 한계와 주의점

**자동 활성화와 규칙 준수는 구분해야 합니다.** 초기 컨텍스트가 전달되는 것과 모델이 모든 절차를 일관되게 수행하는 것은 다른 검증 대상입니다. 프로젝트 문서도 일반 코드 테스트와 실제 LLM 세션의 행동 평가를 분리합니다. 이 리뷰는 어느 쪽도 실행하지 않았으므로 README의 장시간 자율 작업 설명을 성공률·품질·비용 우위의 실험 결과로 일반화하지 않습니다. [테스트와 행동 평가의 구분](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/docs/testing.md#L1-L6), [README의 자율 작업 설명](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/README.md#L35-L43)

**작업 공간 이름은 전체 경로가 아니라 basename에 의존합니다.** `sdd-workspace`는 계획 파일 이름에서 `.md`를 제거한 값으로 디렉터리를 만듭니다. 따라서 같은 Git 작업 디렉터리에서 서로 다른 경로의 동명 계획 파일은 같은 위치로 해석될 수 있습니다. 이는 코드에서 도출한 조건이며 실제 충돌을 재현한 결과는 아닙니다. 계획별 분리는 동명 파일까지 구분하는 전역 고유 식별 체계는 아닙니다. [경로 구성](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/subagent-driven-development/scripts/sdd-workspace#L28-L40)

**초기화 실패를 성공적인 활성화로 오인할 여지가 있습니다.** Windows 래퍼는 Bash를 찾지 못하면 종료 코드 0으로 끝납니다. OpenCode는 진입 스킬 파일이 없으면 `null`을 캐시하고 지침 삽입을 건너뜁니다. 두 경우 모두 코드를 읽어 확인한 분기이며 실제 운영 장애를 관찰한 것은 아닙니다. 플러그인 설치 목록에 보이는지와 시작 지침이 전달되었는지는 별도로 확인해야 하는 항목입니다. [Windows의 종료 분기](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/hooks/run-hook.cmd#L30-L39), [OpenCode 파일 부재 처리](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/.opencode/plugins/superpowers.js#L62-L74)

**선택적 시각화 기능에는 외부 이미지 요청이 있습니다.** README는 visual companion의 로고 로딩에 버전이 포함된다고 설명합니다. `server.cjs`의 마크업 생성부에서도 외부 로고 URL에 버전 쿼리를 붙이고 `referrerpolicy="no-referrer"`를 설정하는 것을 확인했습니다. 세 가지 telemetry 비활성화 환경변수 중 하나가 참으로 해석되면 로고 태그를 생략합니다. 이 확인은 해당 마크업 경로에 한정하며 전체 서버의 네트워크 동작이나 보안을 감사한 결과는 아닙니다. [README 고지](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/README.md#L344-L346), [환경변수](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/brainstorming/scripts/server.cjs#L105-L112), [로고 출력 조건](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/brainstorming/scripts/server.cjs#L242-L251)

라이선스 파일은 MIT이며 저작권자와 허가 조건, 보증 부인 문구를 포함합니다. [LICENSE](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/LICENSE#L1-L21)

## 결론

Superpowers의 설계에서 눈에 띄는 부분은 스킬의 문장 자체뿐 아니라 **지침을 전달하는 초기화 경로와 작업 근거를 파일로 전달하는 구조**입니다. 플랫폼 연결 코드는 스킬을 발견하고 읽을 수 있게 하며, 작은 셸 도구는 계획을 작업별 요구사항으로 분리하고 변경을 커밋 범위로 묶습니다. 그 위에서 에이전트가 설계 승인, 구현, 리뷰, 수정 판단을 수행합니다.

이 구조를 평가할 때는 세 층을 각각 보아야 합니다. 첫째는 스킬이 실제 컨텍스트에 도달하는지, 둘째는 계획·보고서·diff가 정확한 범위를 보존하는지, 셋째는 모델이 그 근거를 읽고 절차를 지키는지입니다. 이 커밋은 앞의 두 층을 추적할 수 있는 비교적 작은 연결 코드와 보조 도구를 제공하며, 마지막 층은 행동 평가가 필요한 영역으로 남습니다.

## 이 글에서 다루지 못한 부분

시각화 서버의 인증·WebSocket·수명주기 전체, Hermes·Gemini·Cursor 등 모든 플랫폼의 실제 통합, `systematic-debugging`과 `writing-skills`의 상세 방법론, worktree 생성·브랜치 종료 스킬의 모든 예외 경로는 심층 분석하지 않았습니다. Codex 패키징은 포함 경로와 메타데이터 복사 규칙만 확인했으며 실제 배포 산출물은 검사하지 않았습니다. 외부 행동 평가 저장소와 모델별 성능 비교 역시 이 리뷰의 검증 범위에 포함되지 않습니다.
