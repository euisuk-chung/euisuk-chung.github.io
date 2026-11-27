---
type: "Repo Review"
title: "[Repo Review] Git Ontology Agent — 대화 중 바뀐 조건을 어디까지 다시 계산할까"
description: "요청을 Git 브랜치로 나누고 의존성에 따라 결과를 다시 계산하는 Git Ontology Agent의 상태 전이·병합·답변 출처를 코드로 살펴봅니다."
date: "2026-11-28"
tags:
  - "Repo Review"
  - "AI Agent"
  - "Git"
  - "Python"
resource: "https://github.com/gogoymh/git-ontology-agent/tree/89743589fdc93cd6ccf67d6b58275aeb728062fb"
generated:
  by: "process:blog-review"
  at: "2026-11-28T06:11:14.819368+09:00"
sources:
  - id: "github:gogoymh/git-ontology-agent"
    resource: "https://github.com/gogoymh/git-ontology-agent/tree/89743589fdc93cd6ccf67d6b58275aeb728062fb"
    title: "Git Ontology Agent"
    author: "gogoymh"
status: "stable"
year: "2026"
analyzed_at: "2026-11-28T06:11:14.819368+09:00"
source_id: "gogoymh/git-ontology-agent"
source_revision: "89743589fdc93cd6ccf67d6b58275aeb728062fb"
source_type: "repo"
source_url: "https://github.com/gogoymh/git-ontology-agent/tree/89743589fdc93cd6ccf67d6b58275aeb728062fb"
visual_sources:
  - path: "img/reviews/2026/git-ontology-agent-review/request-flow.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/goa/agent.py#L100-L141"
    caption: "요청 분류와 작업 브랜치, 병합 및 답변 기록의 흐름. 리뷰어 작성, 분석 커밋 기준."
  - path: "img/reviews/2026/git-ontology-agent-review/dependency-redo.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/goa/skills.py#L141-L175"
    caption: "예산 조건 변경 시 숙소와 합계를 다시 계산하고 기차를 유지하는 의존 관계. 리뷰어 작성, 분석 커밋 기준."
---

## 들어가며: 에이전트가 일하는 중에 조건이 바뀐다면

“다음 주 부산 출장 일정 짜줘.” 에이전트가 기차와 숙소를 살펴보는 동안 사용자가 덧붙입니다. “아, 예산은 50만 원 이하로.” 잠시 뒤에는 다른 질문도 들어옵니다. “그런데 내일 회의는 몇 시였지?”

이런 대화에서는 마지막 메시지에 답하는 것만으로 일이 끝나지 않습니다. 새 예산이 어느 작업에 붙는지, 이미 정한 기차를 다시 골라야 하는지, 회의 질문을 처리하면서 출장 계획을 이어갈 수 있는지까지 정해야 합니다. **Git Ontology Agent**는 이 문제를 Git 브랜치와 구조화된 작업 상태로 풀어보는 Python 프로젝트입니다. [README의 출장 예시](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/README.md#L35-L66)가 출발점입니다.

아이디어는 명료합니다. 요청마다 작업 브랜치를 만들고, 결과가 무엇에 의존하는지 기록합니다. 조건이 바뀌면 영향을 받는 결과만 무효화하고, 작업이 끝나면 대화의 확정 상태인 `main`에 합칩니다. 여기서 **온톨로지(ontology)**는 거대한 지식 그래프 제품이 아니라, 이 프로젝트가 정한 사실의 유형·의존성·상태·병합 규칙을 뜻합니다.

분석 기준은 커밋 `89743589fdc93cd6ccf67d6b58275aeb728062fb`입니다. 문서와 구현을 읽은 정적 분석이며, 대상 패키지를 설치하거나 데모·테스트·모델 호출을 실행하지 않았습니다. 따라서 아래 예시의 동작은 코드의 분기를 따라 설명한 것이며 실행 결과를 재현했다는 뜻은 아닙니다.

## 무엇인가: 대화의 작업 상태를 Git으로 관리하는 작은 엔진

이 저장소를 한 문장으로 정리하면 **진행 중인 요청의 변경을 분류하고, 작업 상태의 의존성을 따라 재계산한 뒤 Git에 이력을 남기는 에이전트 엔진**입니다. 패키지 버전은 `0.1.0`이고, Python 3.9 이상을 요구합니다. Python 패키지의 선언된 런타임 의존성은 빈 목록이며, 명령행 진입점은 `goa.cli:main`입니다. [패키지 매니페스트](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/pyproject.toml#L5-L24)에서 확인할 수 있습니다.

역할은 세 부분으로 나뉩니다.

- **Git**은 요청별 상태와 변경 이력, 답변의 기준 커밋을 보관합니다.
- **온톨로지 규칙**은 어느 결과를 다시 계산하고, 서로 다른 결과를 어떻게 합칠지 결정합니다.
- **언어 모델과 판단 모델**은 요청을 구조화하고, 후속 메시지의 관계를 분류하며, 최종 문장을 작성합니다.

Git이 호텔이나 예산의 의미를 이해하는 것은 아닙니다. 반대로 언어 모델이 모든 변경 이력을 대화 문장으로만 기억하는 것도 아닙니다. 모델이 만든 구조화된 정보를 일반 코드가 처리하도록 두 책임을 나눈 설계입니다. [엔진의 구성과 모델 주입 지점](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/goa/agent.py#L70-L97)에 이 구분이 드러납니다.

## 아키텍처: 입력, 상태 전이, 답변을 잇는 모듈

핵심 코드는 `goa/` 아래에 모여 있습니다. 화면과 모델 제공자보다 먼저 `agent.py`, `ontology.py`, `gitstore.py`를 읽으면 전체 흐름을 잡기 쉽습니다.

| 파일 | 책임 | 입력에서 출력으로 이어지는 역할 |
| --- | --- | --- |
| `cli.py`, `serve.py` | 사용자 입력과 실행 루프 | 문자열 또는 JSON Lines 메시지를 받아 `Agent.submit()`과 `tick()`을 호출합니다. |
| `agent.py` | 요청의 생명주기 | 관계 판단, 브랜치 생성, 후속 조건 적용, 단계 실행, 병합과 답변을 조율합니다. |
| `skills.py` | 작업을 claim으로 변환 | 새 조건을 해석하고 다음 작업 단위의 결과를 반환합니다. |
| `ontology.py` | 상태와 의존성 규칙 | claim을 저장하고, 전이적 의존성을 찾아 무효화하며, 유형별 3-way merge를 수행합니다. |
| `gitstore.py` | Git 객체와 참조 저장 | 상태 스냅샷·커밋·브랜치와 답변 이력을 관리합니다. |
| `decision.py`, `llm.py`, `respond.py` | 모델 연결과 답변 작성 | 구조화된 판단, 작업 결과, 상태에 맞춘 자연어 응답을 만듭니다. |

![요청 입력에서 관계 판단과 작업 브랜치를 거쳐 병합 및 답변 기록으로 이어지는 흐름]({{ '/img/reviews/2026/git-ontology-agent-review/request-flow.svg' | relative_url }})

요청을 분류하는 경로와 작업 결과를 저장하는 경로. 리뷰어 작성, 분석 커밋 기준. 출처: [Agent의 입력·작업·병합](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/goa/agent.py#L100-L141), [답변 이력 저장](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/goa/gitstore.py#L138-L153).
{: .caption}

`goa serve`는 웹 서버가 아니라 **표준 입력과 표준 출력으로 JSON을 한 줄씩 주고받는 인터페이스**입니다. 입력은 `submit`, `log`, `quit`이며 출력은 `answer`, `step`, `tasks`, `error` 등의 이벤트입니다. 별도의 프런트엔드가 Python 엔진을 자식 프로세스로 띄우고 이 이벤트를 화면에 표시할 수 있습니다. [프로토콜 정의](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/goa/serve.py#L1-L17)입니다.

### 작업 브랜치는 실행 프로세스가 아닙니다

README는 독립 요청을 “parallel”로 설명합니다. 코드에서 확인되는 구현은 여러 작업의 상태를 브랜치로 분리하고, 한 작업 루프가 열린 요청들을 차례로 진행하는 방식입니다. `tick()`은 열린 작업을 순회하며 각 작업의 다음 단위를 실행하고, `submit()`과 `tick()`은 같은 `RLock`을 사용합니다. [실제 순회와 잠금](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/goa/agent.py#L100-L141)을 보면 브랜치마다 독립 워커나 프로세스를 만드는 구조와는 차이가 있습니다.

입력 처리가 계속 밀리지 않도록 `Inbox`는 메시지가 대기 중이면 다음 작업 단계의 시작을 늦춥니다. 덕분에 작업 단위 사이에 새 메시지를 적용할 자리를 만듭니다. 이미 진행 중인 모델 호출을 즉시 중단하는 구현으로 읽어서는 안 됩니다. [Inbox와 작업 루프](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/goa/serve.py#L36-L59), [입력 처리](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/goa/serve.py#L116-L160)가 이 경계를 보여 줍니다.

## 작동 원리: 문장을 상태의 변경으로 바꾸기

### 1. claim에는 값뿐 아니라 출처와 의존성도 붙습니다

**claim**은 작업 상태를 이루는 한 항목입니다. 예를 들어 `trip.city`는 출장지, `constraint.budget`은 예산, `plan.hotel`은 선택한 숙소를 가리킵니다. 각 항목은 `id`, `type`, `value`에 더해 어느 요청에서 왔는지 나타내는 `from`, 현재 상태인 `status`, 의존 대상인 `depends_on`을 가집니다. 논리 시각 `at`, 정정 이력과 충돌 대안도 저장할 수 있습니다. [Claim 데이터 구조](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/goa/ontology.py#L16-L59)를 기준으로 정리하면 다음과 같습니다.

| 유형 | 뜻 | 출장 예시 |
| --- | --- | --- |
| `Request` | 사용자가 보낸 요청 | “예산은 50만 원 이하로” |
| `Constraint` | 지켜야 할 조건 | `constraint.budget` |
| `Assumption` | 작업의 전제 | `trip.city` |
| `Finding` | 작업 중 얻은 정보 | `hotel.candidates` |
| `Decision` | 선택한 결과 | `plan.hotel` |
| `Progress` | 진행 상황 | `progress.remaining` |

이름이 `state.yaml`인 파일에 저장하지만 일반적인 YAML 파서를 쓰지는 않습니다. 각 항목을 `- `로 시작하는 한 줄짜리 JSON 객체로 기록하고, 읽을 때는 그 줄의 JSON을 파싱합니다. YAML의 일부 표현만 쓰는 자체 저장 형식입니다. [직렬화 코드](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/goa/ontology.py#L137-L151)를 보면 외부 YAML 의존성 없이 상태를 저장하는 이유를 이해할 수 있습니다.

`confirmed`도 일상적인 “사실 검증 완료”와 구분해야 합니다. 이는 엔진 내부의 상태 이름입니다. 온라인 `LLMSkill`은 모델이 반환한 항목을 `confirmed`로 생성합니다. 출처 조사나 외부 검증이 자동으로 끝났다는 인증은 아닙니다. [온라인 claim 생성](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/goa/skills.py#L249-L255)에 이 처리 방식이 명시되어 있습니다.

### 2. 새 메시지는 다섯 가지 관계 중 하나가 됩니다

열린 작업이 없으면 요청은 `main`에서 갈라진 `req/<번호>` 브랜치로 시작합니다. 열린 작업이 있으면 엔진은 새 메시지와 기존 상태를 판단 모델에 보냅니다. 여러 작업이 열려 있으면 어느 작업을 대상으로 하는지도 함께 묻습니다. [요청 시작](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/goa/agent.py#L219-L238), [판단 입력 구성](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/goa/agent.py#L240-L267)입니다.

| 코드 | 메시지의 관계 | 적용되는 변경 |
| --- | --- | --- |
| `k1` | 보충: “50만 원 이하로” | 대상 브랜치에 조건을 추가하고 의존 결과를 무효화합니다. |
| `k2` | 정정: “부산 말고 대구” | 이전 값의 이력을 남기고 새 값으로 바꾼 뒤 의존 결과를 무효화합니다. |
| `k3` | 독립: “내일 회의는 몇 시?” | 현재 `main`에서 별도 요청 브랜치를 만듭니다. |
| `k4` | 취소: “출장 취소됐어” | 브랜치를 병합하지 않고 `cancelled/req/<번호>`로 옮깁니다. |
| `k5` | 진행 질문: “어디까지 됐어?” | 작업 상태를 수정하지 않고 현황을 답합니다. |

기본 관계 신뢰도 기준은 `0.8`입니다. 판단값이 이보다 낮으면 원래 요청을 보류하고 사용자에게 기존 작업에 반영할지 별도 요청으로 처리할지 묻습니다. 이 숫자는 프로젝트의 정책값이며, 실제 오류 확률이 20% 이하라는 실험적 보장은 아닙니다. [정책 기본값](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/goa/agent.py#L28-L36), [확인 질문 분기](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/goa/agent.py#L100-L119)를 함께 봐야 합니다.

판단과 작업은 같은 모델이 맡을 수도 있고 서로 다른 제공자를 쓸 수도 있습니다. `DecisionModel`은 결과를 `choice`, `confidence`, `probabilities` 또는 0~1의 `noul` 값으로 정규화합니다. 오프라인 기본 판단기는 키워드와 claim 유형을 이용하는 휴리스틱입니다. 따라서 기본 데모의 관계 분류를 외부 모델의 추론 성능으로 해석할 수 없습니다. [정규화](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/goa/decision.py#L46-L58), [오프라인 판단기](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/goa/decision.py#L254-L285)입니다.

### 3. 예산이 바뀌면 기차까지 다시 고를 필요는 없습니다

이 프로젝트의 장점이 가장 구체적으로 드러나는 부분은 의존성 처리입니다. 내장 출장 스킬에서 기차 선택은 `trip.city`에 의존합니다. 반면 숙소 후보는 `trip.city`와 `constraint.*`에 의존합니다. 끝의 `.*`는 그 접두사 아래의 조건을 모두 가리킵니다. [출장 파이프라인](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/goa/skills.py#L141-L175)에 선언된 관계입니다.

![예산 변경이 숙소 후보와 숙소 선택 및 합계에 전파되지만 기차 선택에는 전파되지 않는 의존성]({{ '/img/reviews/2026/git-ontology-agent-review/dependency-redo.svg' | relative_url }})

예산 조건을 추가했을 때 다시 계산할 항목과 유지할 항목. 리뷰어 작성, 분석 커밋 기준. 출처: [출장 스킬의 depends_on](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/goa/skills.py#L141-L175), [전이적 무효화](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/goa/ontology.py#L101-L121).
{: .caption}

예산이 새로 들어오면 엔진은 다음과 같이 상태를 바꿉니다.

1. `constraint.budget`을 현재 요청 브랜치에 넣습니다.
2. 이 조건에 의존하는 `hotel.candidates`를 찾습니다.
3. 그 후보에 의존하는 `plan.hotel`, 다시 그 선택에 의존하는 `plan.total`까지 따라갑니다.
4. 해당 결과의 상태를 `invalid`로 바꿉니다. 예산과 의존 관계가 없는 `plan.train`은 유지합니다.
5. 출장 스킬이 다음 작업 단위에서 파이프라인의 첫 번째 누락·무효 항목부터 다시 계산합니다.

아래는 [실제 의존성 순회](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/goa/ontology.py#L102-L121)와 [출장 스킬의 다음 단계 선택](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/goa/skills.py#L141-L145)을 묶어 설명한 **의사코드**입니다. 원본 코드의 전사가 아니라 입력과 출력을 드러내기 위한 재작성입니다.

```text
입력: 변경된 claim ID 집합, 현재 상태, 스킬 파이프라인
영향 집합 ← depends_on을 따라 도달할 수 있는 모든 후속 claim
영향 집합에서 Request와 Progress를 제외하고 invalid로 표시
다음 작업 ← 파이프라인에서 처음 만나는 누락 또는 invalid 항목
해당 작업을 계산하고 결과 claim을 요청 브랜치에 커밋
출력: 유지한 상태 + 재계산한 결과 + 변경 이력
```

출장지가 부산에서 대구로 바뀌면 범위가 달라집니다. `trip.city`에 기차와 숙소 후보가 모두 의존하므로 둘 다 다시 계산하고, 그 결과에 의존하는 숙소와 합계도 바뀝니다. 예산 자체는 출장지에 의존하지 않으므로 유지됩니다. 같은 “다시 해줘”라도 변경 지점과 의존 관계에 따라 재계산 범위가 달라지는 것입니다.

정정은 단순 덮어쓰기로 끝나지 않습니다. `State.correct()`는 이전 항목을 `원래ID#이전요청`이라는 별도 항목으로 보관하고 `superseded` 상태를 붙입니다. 새 항목에는 `prev`와 `corrects`를 남깁니다. [정정 처리](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/goa/ontology.py#L123-L135) 덕분에 나중에 무엇이 어느 요청에서 바뀌었는지를 설명할 재료가 생깁니다.

### 4. Git은 checkout 없이 상태 스냅샷을 쌓습니다

각 브랜치에 작업 디렉터리를 따로 만드는 방식은 아닙니다. `gitstore.py`는 `hash-object`로 파일 내용을 저장하고, `mktree`로 트리를 만들며, `commit-tree`로 커밋을 생성합니다. 마지막에 `update-ref`로 브랜치가 가리키는 위치를 바꿉니다. [Git plumbing 구현](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/goa/gitstore.py#L52-L85)을 따라가면 checkout을 오가며 공유 작업 파일을 수정하지 않는 이유가 보입니다.

단계별 커밋은 `state.yaml`의 스냅샷과 요청·관계·기준 커밋 등의 정보를 담습니다. “claim 하나당 커밋 하나”라는 설명은 개념적인 요약에 가깝습니다. 실제 `tick()`은 스킬이 돌려준 claim 목록을 상태에 모두 적용한 뒤 한 번 커밋하므로, 온라인 스킬이 여러 claim을 돌려주면 한 커밋에 여러 변경이 들어갑니다. [단계 커밋 코드](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/goa/agent.py#L125-L138)입니다.

답변은 별도의 `answers` 브랜치에 `answer.txt`로 저장합니다. 답변의 기준이 된 `req/1@...` 또는 `main@...`도 기록합니다. 작업 상태를 수정하는 이력과 사용자에게 실제로 한 말을 분리해 두는 것입니다. [답변 저장](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/goa/gitstore.py#L141-L153) 덕분에 특정 시점의 응답과 그 기준 상태를 다시 찾을 수 있습니다. 같은 모델 출력을 새로 생성해도 반드시 동일하다는 뜻은 아닙니다.

### 5. 병합은 줄 단위가 아니라 claim 단위로 합니다

작업이 끝나면 엔진은 `base`, 현재 `main`, 요청 브랜치의 세 상태를 읽습니다. **3-way merge**는 공통 조상 이후 양쪽이 무엇을 바꿨는지 비교하는 방식입니다. 여기서는 Git의 텍스트 충돌 해결기를 호출하는 대신 `merge3()`가 claim ID별로 그 비교를 수행합니다. [호출 지점](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/goa/agent.py#L341-L349), [병합 알고리즘](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/goa/ontology.py#L172-L205)입니다.

한쪽만 바뀌었으면 그 변경을 택하고, 양쪽 항목이 같으면 그대로 둡니다. 양쪽이 서로 다르게 바뀌었을 때 유형별 규칙이 나옵니다.

| 유형 | 양쪽 변경이 충돌할 때의 구현 |
| --- | --- |
| `Constraint` | 중복되지 않는 값을 목록에 모아 함께 보존합니다. 조건 사이의 논리적 양립 가능성을 푸는 코드는 아닙니다. |
| `Finding` | 논리 시각 `at`이 더 늦은 쪽을 택합니다. 현실의 관측 정확도를 비교하는 방식은 아닙니다. |
| `Assumption` | 한쪽만 정정 이력을 가졌으면 그쪽을 택합니다. |
| `Decision` | 한쪽이 `invalid`이면 다른 쪽을 택합니다. |
| `Progress` | 요청 브랜치 쪽 진행 항목을 병합 결과로 내보내지 않습니다. |
| 그 밖의 전제·결정 충돌 | 판단 모델에 나중 요청이 이전 의도를 바꿨는지 묻습니다. |

[유형별 규칙의 실제 분기](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/goa/ontology.py#L208-L238)를 요약한 표입니다. 요청은 보통 서로 다른 `req.<번호>` ID로 보존되며, 같은 ID의 `Request`가 충돌하면 구현은 요청 브랜치의 항목을 택합니다.

마지막 판단의 기본 기준은 `0.7`입니다. 나중 요청이 의도를 바꿨다는 점수가 기준 이상이면 나중 값을 선택합니다. 기준 미만이면 하나를 조용히 버리지 않고 `conflict` 상태와 두 대안을 남깁니다. 최종 답변에는 그 대안을 제시하도록 합니다. **미해결 충돌이 있다고 Git 병합 자체를 멈추는 구조는 아닙니다.** 충돌 상태를 담은 스냅샷도 두 부모를 가진 merge commit으로 저장합니다. [충돌 보존](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/goa/ontology.py#L227-L238), [실제 merge commit 생성](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/goa/gitstore.py#L138-L139)에 근거한 구분입니다.

### 6. 답변은 어느 커밋을 읽었는지 함께 남깁니다

중간 답변은 현재 작업 브랜치를 기준으로 씁니다. 독립 요청이 끝나면 그 결과를 중간 답변으로 먼저 알릴 수 있습니다. 열린 작업이 모두 끝나면 원래 요청과 후속 요청이 만든 결정·정보·변경 출처를 모아 최종 답변을 만듭니다. [중간 응답과 최종 응답의 분기](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/goa/agent.py#L350-L386)를 보면 별도 회의 질문을 먼저 답하고 출장 결과를 나중에 정리하는 흐름을 이해할 수 있습니다.

`Responder`는 온라인 모델에 제공된 사실만 쓰고, 무효 항목을 언급하지 않으며, 진행 중인 내용을 확정처럼 쓰지 말라고 지시합니다. 모델 호출에 실패하면 템플릿으로 대체합니다. 이는 답변 생성 정책과 fallback 경로이지, 모든 모델이 지시를 완벽하게 지킨다는 검증 결과는 아닙니다. [답변 지침과 fallback](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/goa/respond.py#L17-L46)입니다.

## 설치와 사용: 오프라인 데모부터 모델 연결까지

다음은 분석 커밋의 [Quick start](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/README.md#L293-L306)에 있는 명령 중 기본 동선을 발췌한 것입니다. 이 리뷰에서 실행하지 않았습니다.

```bash
git clone https://github.com/gogoymh/git-ontology-agent && cd git-ontology-agent && pip install -e .
goa demo
goa demo --mock
goa ask "Plan my Busan business trip next week"
goa log
```

`goa demo`는 기본적으로 내장 출장·회의 스킬과 로컬 판단기를 쓰는 데모입니다. 코드에는 기차 시각·숙소 후보·가격·회의 시각이 고정된 예시 데이터로 들어 있습니다. 실제 기차표 검색이나 캘린더 조회가 아닙니다. `--mock`도 외부 서비스에 연결하는 대신 제공자의 요청 형태를 로컬에서 모사합니다. [고정 출장 데이터](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/goa/skills.py#L51-L59), [회의 예시 데이터](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/goa/skills.py#L182-L196), [mock 동작에 대한 문서](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/README.md#L365-L379)입니다.

일반 실행인 `goa`, `ask`, `chat`, `serve`의 기본 모델 선택은 `auto`입니다. 환경 설정, 저장한 기본값, 로그인된 CLI나 API 키 등에 따라 모델이 연결되며, 연결 수단이 없으면 오프라인으로 내려갑니다. 따라서 API 키가 없는 데모와 실제 모델 실행을 구분해서 읽어야 합니다. [모델 선택 정책](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/README.md#L342-L379)에 설명되어 있습니다.

UI는 Python 엔진과 별도입니다. README는 React·Ink 터미널 화면을 제공한다고 설명하며, Node.js 22 이상이나 빌드된 UI가 없으면 텍스트 채팅으로 전환한다고 안내합니다. Python 엔진의 “의존성 없음”을 UI 전체에도 적용되는 말로 받아들이면 안 됩니다. [UI의 실행 조건](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/README.md#L308-L340)입니다.

## 한계와 주의점: 의존성을 기록하는 것과 결과를 검증하는 것

### 온라인 작업은 모델이 만든 구조에 의존합니다

온라인 `LLMSkill`은 현재 claim과 새 메시지를 모델에 보내 조건·전제를 얻고, 다음 단계에서는 새 claim과 남은 작업 목록을 받습니다. 이 구현 경로 자체에는 외부 검색·예약·데이터베이스 도구를 호출하는 실행 루프가 없습니다. 의존성도 모델이 반환하는 `depends_on`에 의존합니다. 의존 관계가 빠지면 무효화 코드가 그 관계를 스스로 발견해 주지는 못합니다. [온라인 작업 경로](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/goa/skills.py#L264-L304)에 근거한 분석입니다.

### “무효 상태가 남으면 병합하지 않는다”는 문서는 구현과 차이가 있습니다

README에는 `invalid` 항목을 재계산하기 전에는 브랜치를 병합하지 않는다고 적혀 있습니다. 내장 출장 스킬은 누락·무효 항목이 없어야 종료하므로 이 의도에 맞습니다. 다만 온라인 `LLMSkill.next_step()`은 최신 요청 이후 **8단계**에 도달하면 `None`을 반환합니다. `Agent.tick()`은 이를 작업 종료로 받아 `_merge()`를 호출하며, `_merge()`에는 남은 `invalid`를 별도로 막는 검사가 없습니다.

따라서 이 커밋에서 온라인 경로까지 “무효 상태가 하나라도 있으면 절대로 병합되지 않는다”고 보장하기는 어렵습니다. 실제로 특정 모델이 그 상황을 만들었다고 관찰한 것은 아닙니다. [README의 설명](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/README.md#L238), [8단계 종료 조건](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/goa/skills.py#L273-L286), [종료 후 병합 경로](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/goa/agent.py#L128-L140)를 대조한 결과입니다.

### 재시작 복원과 장기 기억은 다른 범위입니다

`Agent._restore()`는 Git 브랜치와 커밋 정보를 읽어 미병합 작업을 다시 구성합니다. 이는 중단된 작업 상태를 복원하는 기능입니다. 반면 README는 세션 종료 후 장기 기억, 여러 에이전트의 협업, 외부 파일·데이터베이스를 현재 범위 밖으로 명시합니다. Git에 기록이 남는다는 사실만으로 장기 기억의 검색·갱신 정책이나 다중 에이전트 협업까지 갖추었다고 볼 수 없습니다. [복원 코드](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/goa/agent.py#L430-L498), [범위 밖 항목](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/README.md#L414-L418)입니다.

### 테스트 파일과 성능 입증도 구분해야 합니다

저장소에는 의존성 전파·유형별 병합·미해결 충돌을 확인하는 테스트와 고정 사례 기반 벤치마크가 있습니다. README가 설명하는 벤치마크 범위는 55개 고정 사례와 지연 측정입니다. 이 글에서는 해당 코드를 실행하거나 결과를 재측정하지 않았습니다. 테스트의 존재를 실제 모델 정확도나 운영 환경의 응답 속도가 입증되었다는 뜻으로 사용하지 않습니다. [온톨로지 테스트](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/tests/test_ontology.py#L18-L94), [벤치마크 설명](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/README.md#L389-L400)을 참고할 수 있습니다.

라이선스는 [MIT](https://github.com/gogoymh/git-ontology-agent/blob/89743589fdc93cd6ccf67d6b58275aeb728062fb/LICENSE)이며 저작권자는 `Copyright (c) 2026 gogoymh`로 표기되어 있습니다. 이 글의 두 그림과 의사코드는 고정 커밋을 근거로 리뷰어가 다시 작성했습니다. 저장소 원본 이미지나 코드 전체를 전재하지 않았습니다.

## 정리: 작업을 되돌릴 기준을 코드로 남긴다는 것

Git Ontology Agent에서 눈여겨볼 부분은 브랜치 자체보다 **변경을 어느 상태에 적용하고, 어디까지 다시 계산하며, 무엇을 합칠지 코드로 드러낸 점**입니다. 예산을 추가했을 때 기차는 유지하고 숙소만 다시 고른다는 차이는 `depends_on`에, 나중에 왜 답변이 바뀌었는지는 요청 출처와 커밋에 남습니다.

그 구조가 모델의 판단이나 정보의 정확성을 대신 보장하지는 않습니다. 현재 구현은 고정 데이터의 데모와 모델이 claim을 생성하는 온라인 경로를 함께 갖춘 작은 엔진입니다. 요청의 생명주기·변경 전파·병합·답변 출처를 나누어 읽으면, 대화 중 요구사항이 바뀌는 에이전트를 어떤 단위로 설계할지 구체적으로 살펴볼 수 있습니다.

이 글에서 다루지 못한 부분은 터미널 UI 내부의 렌더링, 제공자별 인증·HTTP 재시도와 오류 처리의 전수 분석, 벤치마크 실행 결과입니다. 핵심 Python 엔진과 상태 전이에 집중했으며 해당 경로의 실행 성공은 검증하지 않았습니다.
