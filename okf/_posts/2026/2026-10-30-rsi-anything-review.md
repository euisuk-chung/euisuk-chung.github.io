---
type: "Repo Review"
title: "[Repo Review] RSI-Anything — world model의 예측을 행동 선택과 자기개선으로 연결하기"
description: "RSI-Anything의 공통 실행기와 코드 수정·GUI 학습 흐름을 추적하고, 실험실·화학 도메인의 고정 추론을 구분해 공개 구현의 실제 범위를 살펴봅니다."
date: "2026-10-30"
tags:
  - "Repo Review"
  - "AI Agent"
  - "머신러닝"
  - "딥러닝"
  - "Python"
resource: "https://github.com/Gen-Verse/RSI-Anything/tree/8ba44cd73ec6f57b151ec06e2f71a0726adfb687"
generated:
  by: "process:blog-review"
  at: "2026-10-30T06:03:12.175882+09:00"
sources:
  - id: "github:Gen-Verse/RSI-Anything@8ba44cd73ec6f57b151ec06e2f71a0726adfb687"
    resource: "https://github.com/Gen-Verse/RSI-Anything/tree/8ba44cd73ec6f57b151ec06e2f71a0726adfb687"
    title: "RSI-Anything: Unlocking Recursive Self-Improvement with World Models"
    last_modified: "2026-10-13T17:41:03+08:00"
status: "stable"
year: "2026"
analyzed_at: "2026-10-30T06:03:12.175882+09:00"
source_id: "gen-verse/rsi-anything"
source_revision: "8ba44cd73ec6f57b151ec06e2f71a0726adfb687"
source_title: "RSI-Anything: Unlocking Recursive Self-Improvement with World Models"
source_type: "repo"
source_url: "https://github.com/Gen-Verse/RSI-Anything/tree/8ba44cd73ec6f57b151ec06e2f71a0726adfb687"
visual_sources:
  - path: "/img/reviews/2026/rsi-anything-review/workflow-overview.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/src/rsi_anything/workflow/runner.py#L86-L127"
    caption: "CLI·recipe·task adapter·단계 실행 구조 — 리뷰어 작성, 분석 커밋 기준"
  - path: "/img/reviews/2026/rsi-anything-review/code-repair-loop.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/tasks/code_repair/src/evaluation.py#L83-L130"
    caption: "수정안 네 개와 현재 프로그램을 비교하는 코드 수정 루프 — 리뷰어 작성, 분석 커밋 기준"
  - path: "/img/reviews/2026/rsi-anything-review/gui-retention.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/tasks/gui/src/rsi_anything_gui/rsi.py#L15-L73"
    caption: "GUI 경험 수집과 정책/world 갱신·개발셋 승격 — 리뷰어 작성, 분석 커밋 기준"
---

## 예측을 행동과 다음 학습으로 연결하는 레포

에이전트가 여러 행동을 제안했을 때, 전부 실행해서 결과를 비교할 수 있다면 선택은 간단합니다. 그러나 프로그램 실행, 브라우저 조작, 실험에는 시간과 비용이 듭니다. RSI-Anything은 **행동의 결과를 먼저 예측하고, 실제 피드백을 모아 다음 선택에 반영하는 연구용 프레임워크**입니다. 여기서 world model은 반드시 영상으로 미래 장면을 생성하는 모델을 뜻하지 않습니다. 코드의 테스트 통과 가능성이나 행동 후의 보상처럼, 해당 작업에서 필요한 결과를 예측하는 모델도 포함합니다. [프로젝트 개요](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/README.md#L35-L59)

이 레포를 이해할 때는 세 층을 구분하면 좋습니다. 첫째는 여러 도메인에 공통인 연구 아이디어, 둘째는 코드 수정과 GUI 실험을 실행하는 공통 워크플로, 셋째는 도메인마다 공개된 학습·추론 코드입니다. **모든 도메인이 하나의 명령으로 같은 자기개선 과정을 수행하는 구성은 아닙니다.** 이 글은 커밋 `8ba44cd73ec6f57b151ec06e2f71a0726adfb687`의 소스와 문서를 정적으로 읽은 결과이며, 모델·의존성을 설치하거나 연구 코드를 실행해 성능을 재현하지 않았습니다.

## 무엇을 제공하며, 어디까지 공개되어 있습니까?

RSI는 Recursive Self-Improvement의 약자로, 이전 단계에서 얻은 결과가 다음 개선 단계의 출발점이 되는 구조를 가리킵니다. 정책은 행동 후보를 만들고, world model은 결과를 예측하며, 외부 평가기는 실제 결과를 제공합니다. 다만 실제 공개 형태는 다음과 같이 다릅니다.

| 영역 | 분석 커밋에서 확인한 공개 형태 | 읽을 때 구분할 점 |
|---|---|---|
| Code repair | 공통 `rsi` CLI, world model의 4단계 학습과 평가 | 평가 중에는 coder와 world model을 고정합니다. |
| GUI interaction | 공통 `rsi` CLI, 브라우저 수집·정책/world model 갱신·개발셋 승격·평가 | 공개 실험은 MiniWoB++ `click-checkboxes` 중심입니다. |
| Laboratory planning | 별도 `infer.py`의 후보 생성·선택 | 문서는 학습 절차를 설명하지만 공개 명령은 고정 모델 추론입니다. |
| Reaction optimization | 고정 예측표를 이용한 순차 조건 추천 | 피드백은 다음 추천을 바꾸지만 예측표를 재학습하지 않습니다. |
| Immune science | `Coming soon` 안내 | 분석 커밋에서 추론 구현과 사용 예제를 확인할 수 없습니다. |

근거는 [공통 task 허용 목록](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/src/rsi_anything/tasks/__init__.py#L5-L8), [실험실 추론 공개 범위](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/tasks/laboratory_planning/README.md#L17-L42), [화학 추천기 설명](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/tasks/reaction_optimization/README.md#L39-L62), [면역 모델 안내](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/tasks/immune_science_v2/README.md#L11-L13)입니다. README의 OSWorld·과학 응용 성과와 이 체크아웃에서 직접 따라갈 수 있는 경로를 동일시해서는 안 됩니다.

## 아키텍처: 공통 실행기와 도메인 구현의 분리

최상위 패키지는 `pyproject.toml`의 console script로 `rsi_anything.cli:main`을 등록합니다. 공통 패키지의 직접 의존성 목록은 비어 있고, 무거운 ML 환경은 각 task의 별도 가상환경에 둡니다. 공통 CLI 설치가 모델·CUDA·브라우저 설치까지 끝낸다는 뜻은 아닙니다. [패키지 선언](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/pyproject.toml#L5-L18)

![공통 rsi CLI에서 recipe, task adapter, 도메인 프로세스로 이어지는 구조]({{ '/img/reviews/2026/rsi-anything-review/workflow-overview.svg' | relative_url }})

*도식 1. 리뷰어 작성, 분석 커밋 기준입니다. 공통 실행기는 도메인별 명령을 순서대로 실행하고 상태와 결과를 보존합니다. [CLI](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/src/rsi_anything/cli.py#L30-L43) · [runner](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/src/rsi_anything/workflow/runner.py#L86-L119) · [task adapter](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/src/rsi_anything/tasks/__init__.py#L5-L8)*

| 위치 | 책임 |
|---|---|
| `src/rsi_anything/cli.py` | `tasks`, `assets`, `plan`, `run`, `status`, `report` 명령 분기 |
| `workflow/config.py` | JSON recipe 검증, 경로·Python 실행 파일 해석, 소스 식별자 계산 |
| `workflow/types.py` | 명령·환경·예상 출력인 `Stage`와 전체 `Plan` 표현 |
| `workflow/runner.py` | 잠금, 단계 실행, 출력 해시, 재개, 실패 기록 |
| `tasks/code_repair.py`, `tasks/gui.py` | 공통 recipe를 각 task의 명령·출력 계약으로 번역 |
| `tasks/code_repair/`, `tasks/gui/` | 모델·환경·학습·평가의 실제 구현 |
| `tasks/laboratory_planning/`, `tasks/reaction_optimization/` | 별도 도메인 추론 진입점 |

`Stage`는 shell 문자열 하나가 아니라 명령 인자 튜플, 작업 디렉터리, 환경변수, 예상 출력, 재시도 시 보존할 출력 경로를 갖습니다. runner는 이 계약을 이용해 task 내부 학습 알고리즘을 직접 알지 않고도 실행을 관리합니다. [Stage와 Plan 정의](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/src/rsi_anything/workflow/types.py#L5-L24)

## 작동 원리 1: recipe에서 재개 가능한 실행까지

### 입력을 먼저 고정합니다

`rsi plan --config ...`는 recipe를 읽어 해석된 설정과 실행 단계를 출력합니다. `run`은 같은 plan을 실제로 수행합니다. 설정 로더는 task를 `code_repair` 또는 `gui`로 제한하며, 실행 결과 디렉터리를 소스·설정 폴더와 분리합니다. 상대 경로는 recipe 파일 옆을 기준으로 해석하고, 가상환경 Python의 심볼릭 링크 경로는 가상환경을 잃지 않도록 그대로 보존합니다. [설정 로더](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/src/rsi_anything/workflow/config.py#L36-L73)

실행의 identity는 설정만으로 정하지 않습니다. 설정, 소스 identity, 실행 단계, 생성될 task 설정 파일까지 묶어 해시합니다. 코드가 바뀌었는데 이전 결과를 완료 단계로 재사용하는 상황을 막으려는 설계입니다. [identity와 잠금](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/src/rsi_anything/workflow/runner.py#L86-L108)

### 완료 표시와 산출물을 함께 확인합니다

실행 폴더에는 `.workflow.lock`을 두고 `fcntl.flock`으로 배타적 소유권을 얻습니다. 기존 실행이 있으면 `--resume` 없이 덮어쓰지 않으며, 재개할 때도 identity·저장 설정·task 설정을 비교합니다. 이어 **이미 완료된 단계의 파일 또는 체크포인트 디렉터리 해시를 검사한 뒤** 다음 작업으로 진행합니다. 완료 플래그만 믿는 재개가 아닙니다. [재개 검증](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/src/rsi_anything/workflow/runner.py#L97-L127)

각 단계는 별도 프로세스 세션에서 실행됩니다. 종료 코드가 0이 아니면 실패로 처리하고, 예상 출력이 없으면 완료로 기록하지 않습니다. 불완전한 재시도 출력은 조건을 확인해 `attempts/` 아래로 옮깁니다. 중단·오류 시에는 상태와 요약을 저장하며 자신이 실행한 프로세스 그룹을 종료하는 경로도 있습니다. 이러한 코드는 복구 의도를 보여주지만, 이번 정적 리뷰가 모든 실패 조건에서의 운영 안정성을 입증하는 것은 아닙니다. [프로세스 실행](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/src/rsi_anything/workflow/runner.py#L45-L75) · [단계 실행과 실패 처리](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/src/rsi_anything/workflow/runner.py#L139-L185)

## 작동 원리 2: 코드 수정 후보를 예측하고 선택합니다

### 학습 단계와 평가 루프가 다릅니다

공통 code-repair adapter의 `full` 모드는 자산 확인 뒤 `initial → semantic → expanded → incumbent`의 네 world model 학습 단계를 연결하고 마지막 체크포인트로 평가합니다. 각 단계의 출력 체크포인트를 다음 단계의 `--parent`로 전달합니다. `evaluate`는 지정되었거나 배포된 체크포인트를 평가하며, `verify`는 자산 확인까지만 수행합니다. [code-repair plan](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/src/rsi_anything/tasks/code_repair.py#L6-L54)

| 단계 | 소스·문서에서 확인한 역할 |
|---|---|
| `initial` | JEPA 기반 실행 결과 표현과 기본 readout 학습 |
| `semantic` | 전체 테스트 모음의 실행 품질을 위한 readout 확장·적응 |
| `expanded` | 확장된 기록으로 학습하고 그룹 내 순위 정보를 반영 |
| `incumbent` | 새 후보를 현재 프로그램과 비교하는 선호 정보 반영 |

학습은 배포된 실행 기록을 읽으며, train 문제 ID가 개발·최종 평가 ID와 겹치지 않는지 검사합니다. 이 공개 파이프라인을 매 평가 문제마다 coder와 world model이 동시에 새로 학습하는 방식으로 설명하면 맞지 않습니다. [학습 데이터와 분리 검사](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/tasks/code_repair/src/training.py#L59-L93) · [학습 단계 설명](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/docs/reproduction.en.md#L65-L89)

### world model은 실행 결과를 표현으로 예측합니다

`DomainEncoder`는 토큰의 마지막 hidden state를 attention mask로 평균 집계하고 작은 projection으로 보냅니다. backbone에는 LoRA를 붙이며, 입력 길이를 초과하면 조용히 자르지 않고 오류를 냅니다. `ExecutionWorld`는 online encoder, EMA target encoder, predictor, OPF(Orthogonal Factor Projection), 결과 readout을 결합합니다. OPF는 표현을 여러 factor로 다루기 위한 구성요소이고, target encoder는 online encoder의 이동평균으로 갱신됩니다. [encoder와 world 구조](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/tasks/code_repair/src/world.py#L14-L63) · [학습 손실과 EMA](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/tasks/code_repair/src/world.py#L88-L133)

실제 최종 선택에 쓰는 `SemanticExecutionWorld`는 이 표현에서 전체 테스트 모음 통과 가능성과 예상 통과 비율을 계산합니다. 코드의 효용 정의를 수식으로 옮기면 다음과 같습니다.

```math
u(c)=p_{\mathrm{all}}(c)+0.25\,\hat f(c).
```

여기서 $`c`$는 평가할 프로그램 후보, $`p_{\mathrm{all}}`$은 전체 테스트 모음을 통과할 예측 확률, $`\hat f`$는 예측 통과 비율입니다. 따라서 $`u`$는 확률 하나가 아니라 두 예측의 가중합이며 최대 1.25가 될 수 있습니다. 코드도 선택 전에 효용의 유한성과 0~1.25 범위를 검사합니다. 반환 메타데이터에는 `calibration_verified=False`, `semantic_correctness_guaranteed=False`가 들어갑니다. 이 점수는 실행 성공 보증이 아닙니다. [효용 계산](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/tasks/code_repair/src/semantic_world.py#L174-L182) · [선택 검증](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/tasks/code_repair/src/evaluation.py#L27-L34)

### 네 수정안과 현재 코드를 함께 비교합니다

![공개 피드백으로 네 수정안과 현재 코드를 점수화하고 선택 결과만 실행하는 코드 수정 루프]({{ '/img/reviews/2026/rsi-anything-review/code-repair-loop.svg' | relative_url }})

*도식 2. 리뷰어 작성, 분석 커밋 기준입니다. 루프는 최대 세 번이며, 공개 테스트가 모두 통과하면 일찍 끝납니다. 숨겨진 테스트는 선택을 봉인한 뒤 별도 judge에서 사용합니다. [선택 루프](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/tasks/code_repair/src/evaluation.py#L83-L130) · [봉인과 judge](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/tasks/code_repair/src/evaluation.py#L133-L183)*

입력은 문제, 현재 프로그램, 이전 공개 실행 결과, 공개 테스트입니다. 첫 라운드의 네 수정안은 공개 자산에서 읽습니다. 이후 라운드는 `fresh` 모드라면 고정 coder가 다시 만들고, `recorded` 모드라면 저장된 후보를 읽습니다. 네 수정안 뒤에는 현재 코드를 유지하는 `keep_current`가 붙어 총 다섯 후보를 점수화합니다. [후보 생성과 실행 분기](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/tasks/code_repair/src/evaluation.py#L78-L125)

선택 함수의 핵심은 짧습니다. 다음 인용은 원문의 마지막 두 줄입니다.

```python
best = max(range(4), key=lambda i: utility[i])
return best if utility[best] > utility[4] else 4
```

출처: [`evaluation.py`, 33–34행](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/tasks/code_repair/src/evaluation.py#L33-L34). 새 후보가 현재 코드보다 **엄격하게 높을 때만** 교체합니다. 동점이면 현재 코드를 유지합니다. 새 후보끼리 동점일 때는 `max`가 앞선 후보를 택합니다. 이 선택은 모델 예측 기준이므로 실제 결과의 단조 개선을 보장하지는 않습니다.

선택한 코드는 공개 테스트로 실행해 다음 피드백으로 넘깁니다. `recorded`에서는 이 부분도 저장된 공개 실행 기록을 사용합니다. worker는 매 결과에 `hidden_tests_accessed=False`, `optimizer_steps=0`을 남깁니다. 공개 선택이 끝난 600개의 문제–seed 에피소드를 모아 봉인하고, 그 후에야 숨겨진 테스트 judge를 열어 최종 성공률을 계산합니다. 따라서 `recorded` 재평가는 저장된 최종 성공률을 단순 출력하는 것과 다르지만, 새 coder 궤적을 만드는 실험과도 다릅니다. [공개 입력 재사용 의미](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/docs/reproduction.en.md#L40-L63) · [최종 집계](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/tasks/code_repair/src/evaluation.py#L133-L209)

## 작동 원리 3: GUI에서는 실제 정책 갱신과 승격이 있습니다

GUI task는 instruction과 보이는 DOM 요소를 정책 서비스에 보내 후보 행동을 받습니다. `submit`도 후보 풀에 포함되어야 합니다. world 기반 제어를 쓰면 각 행동의 예상 가치를 비교하며, 제출 행동은 따로 보정한 제출 성공 확률을 사용합니다. [정책 서비스 요청과 행동 선택](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/tasks/gui/src/rsi_anything_gui/experiment.py#L7-L31)

**`alpha=0`이면 world model로 행동을 다시 순위화하지 않습니다.** `episode`는 world 예측 자체를 건너뛰고 정책의 첫 후보를 사용합니다. 반면 `alpha='pure'`는 world 값으로 선택하고, 다른 가중치는 정책 log probability와 정규화된 world 값을 결합합니다. [예측 사용 분기](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/tasks/gui/src/rsi_anything_gui/experiment.py#L17-L57)

자기개선 루프는 `rsi.py`의 두 generation에 구현되어 있습니다. 현재 정책·world model로 학습용 브라우저 경험을 수집하고, 성공한 실제 에피소드에서 유효 행동만 골라 정책 LoRA를 SFT(Supervised Fine-Tuning, 지도 미세조정)합니다. 최대 256개의 새 행동에 같은 수의 성공 replay를 섞습니다. 새 성공 데이터가 없으면 갱신하지 않고 부모 정책을 유지합니다. world model도 새 경험과 replay를 이용해 갱신합니다. [경험 수집과 정책/world 갱신](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/tasks/gui/src/rsi_anything_gui/rsi.py#L15-L44) · [성공 데이터 필터와 replay](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/tasks/gui/src/rsi_anything_gui/policy_train.py#L9-L33)

![GUI에서 경험 수집, 정책과 world 갱신, 개발셋 승격, 고정 테스트로 이어지는 두 단계]({{ '/img/reviews/2026/rsi-anything-review/gui-retention.svg' | relative_url }})

*도식 3. 리뷰어 작성, 분석 커밋 기준입니다. 후보 모델은 개발셋의 성공률 향상과 유효 비용 조건을 통과해야 현재 버전을 대체합니다. 두 generation의 버전을 고정한 뒤 RSI test를 엽니다. [승격 조건과 평가 순서](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/tasks/gui/src/rsi_anything_gui/rsi.py#L45-L73)*

새 pair는 개발셋에서 현재 pair와 비교됩니다. 성공률의 차이가 `promotion_gain` 이상이고 `effective_seconds`가 정한 비용 비율 이내일 때만 승격합니다. 테스트 점수를 보고 승격하는 구조가 아닙니다. 두 후보의 버전이 모두 고정된 뒤, old/new policy와 old/new world의 네 조합을 평가합니다. 이를 통해 어느 쪽의 변화가 성능에 연결됐는지 살펴볼 수 있도록 구성했습니다. 다만 이러한 분리 코드의 존재와 실험 결과의 독립 재현은 구분해야 합니다. [승격과 교차 평가 구현](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/tasks/gui/src/rsi_anything_gui/rsi.py#L45-L73)

## 작동 원리 4: 과학 도메인의 공개 추론 경계

### 실험실 계획: 후보 점수의 feedback은 예측입니다

실험실 계획은 `infer.py world`로 정책 adapter에서 네 계획을 생성하거나, `infer.py select`로 주어진 네 후보를 선택합니다. world checkpoint는 CPU에서 고정된 ensemble을 읽고, 계획의 구조와 task에서 만든 특징을 정규화해 품질·상대 개선·위험·불확실성을 계산합니다. 품질과 개선에 가점을, 위험과 불확실성에 감점을 주고 합법적이지 않은 후보는 제외합니다. 합법 후보가 하나도 없으면 인덱스 0으로 fallback하면서 `fallback_no_legal`을 표시합니다. [선택 함수](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/tasks/laboratory_planning/src/lab_inference/world.py#L59-L88)

출력에는 선택된 completion과 모든 후보, `forecast`가 담깁니다. 그 안의 `feedback`은 task evaluator가 실제로 채점한 값이 아니라 모델이 예측한 결과입니다. 공개 CLI에서는 gradient update나 다음 학습 pair의 승격이 실행되지 않습니다. 문서에 설명된 학습 라운드와 배포된 고정 추론을 구별해야 하는 이유입니다. [CLI 출력 경로](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/tasks/laboratory_planning/src/lab_inference/cli.py#L56-L80) · [문서의 학습·동결 구분](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/tasks/laboratory_planning/README.md#L17-L42)

### 반응 조건 추천: 실측값이 바꾸는 것은 선택입니다

Suzuki–Miyaura 반응 추천기는 321개 조건의 고정 평균 수율·보정된 표준편차를 읽습니다. 관측한 `candidate_index`와 수율을 입력하면, 이미 측정한 조건을 제외하고 Expected Improvement(EI, 현재 최고 수율보다 나아질 것으로 예상되는 정도)가 가장 큰 조건 하나를 반환합니다. 코드의 계산은 다음과 같습니다. [EI와 추천 구현](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/tasks/reaction_optimization/src/suzuki_inference/selector.py#L11-L59)

```math
g_i=\mu_i-y_{\mathrm{best}}-\xi,\qquad z_i=\frac{g_i}{\sigma_i},\qquad
\mathrm{EI}_i=g_i\Phi(z_i)+\sigma_i\phi(z_i).
```

$`\mu_i`$는 고정 예측 평균 수율, $`\sigma_i`$는 보정된 예측 표준편차, $`y_{\mathrm{best}}`$는 입력 관측 중 최고 실측 수율, $`\xi`$는 추가 개선 여유입니다. $`\Phi`$와 $`\phi`$는 표준정규분포의 누적분포함수와 밀도함수입니다. 수율·표준편차·EI는 코드가 지정한 백분율 또는 퍼센트포인트 단위를 따릅니다. 새 측정값을 추가하면 최고 실측 수율과 제외 후보 집합이 바뀝니다. **예측 평균·분산을 관측마다 다시 학습하거나 Bayesian posterior로 갱신하는 코드는 아닙니다.** 구현은 계산한 EI에 `np.maximum(..., 0.0)`을 적용해 음수가 되지 않게 합니다. 같은 점수이면 작은 후보 ID를 택합니다.

입력은 비어 있으면 안 되고, 후보 ID는 중복될 수 없으며, 수율은 0~100 범위여야 합니다. 모두 측정했을 때는 오류로 끝납니다. 이 추천기는 해당 반응 맥락과 배포된 조건 풀을 위한 추론 도구이며, 임의의 화학 반응을 입력받는 범용 분자 모델 서비스와는 공개 인터페이스가 다릅니다. [입력 검증](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/tasks/reaction_optimization/src/suzuki_inference/selector.py#L19-L49) · [조건 풀 정의](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/tasks/reaction_optimization/README.md#L39-L62)

## 보고된 성능을 어떻게 읽어야 합니까?

다음 수치는 분석 커밋의 문서가 보고한 값이며, 이 리뷰의 재실행 결과가 아닙니다.

| 평가 | 문서의 결과 | 함께 읽어야 할 조건 |
|---|---|---|
| CodeContests | 최종 hidden-test 성공률 31.2% | 200문제 × 3 seeds, 최대 3회 수정 |
| APPS Introductory | full-test 성공률 46.37% | 1,000문제, 3 seeds 평균 |
| LiveCodeBench v6 | full-test 성공률 33.05% | 1,055문제, 3 seeds 평균 |
| MiniWoB++ selected controller | 51/100 → 79/100 → 99/100 | 같은 100개 checkbox task, 개발셋이 선택한 `alpha=0` |
| MiniWoB++ world-based control | 49/100 → 96/100 → 98/100 | 위와 같은 retained version에서 world 값으로 후보 순위화 |
| Suzuki 반응 추천 | 평균 최고 관측 수율 96.15% | 고정 조건 풀의 기존 실측값 replay, 100 runs, 총 관측 예산 40 |

출처: [README 결과](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/README.md#L76-L113), [코드 평가 조건](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/docs/benchmarks.md#L7-L24), [GUI 결과와 controller 정의](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/tasks/gui/README.md#L15-L37), [반응 평가 프로토콜](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/tasks/reaction_optimization/README.md#L12-L27).

GUI의 99%를 “world model이 매번 행동을 골라서 얻은 성공률”로 읽으면 구현을 놓치게 됩니다. 최종 선택 controller는 정책 순위를 쓰며, world 기반 제어는 별도 98%입니다. 99%는 120초·최대 8회 행동 안에서 모든 checkbox가 맞고 제출까지 완료된 경우를 뜻합니다. 일반적인 데스크톱 작업 전체의 성공률로 넓혀 해석할 수 없습니다.

또한 중간 GUI 버전의 평균 행동 수는 2.93회로 최종 3.21회보다 적지만 잘못된 제출은 21회에서 1회로 줄어듭니다. 짧은 실행이 항상 좋은 실행은 아니라는 점을 보여줍니다. 반응 도메인의 96.15%는 예측 정확도나 성공 비율이 아니라 관측된 **반응 수율**이며, 기존 스크리닝 자료를 순차 replay한 결과입니다.

## 설치와 사용: 문서에 있는 시작 경로

아래 명령은 분석 커밋의 문서에서 가져온 사용 절차입니다. 이 리뷰에서 실행한 명령은 아니며, 모델과 데이터의 별도 준비가 필요합니다.

### 공통 CLI를 설치하고 plan을 확인합니다

```bash
git clone https://github.com/Gen-Verse/RSI-Anything.git
cd RSI-Anything
python3.10 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
rsi tasks
```

출처: [README Quick Start](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/README.md#L119-L130). 이 부분은 공통 CLI를 설치합니다. code repair의 실제 ML 환경은 Linux·Python 3.10과 task requirements를 사용합니다. 프로그램 실행기는 `runuser`, `unshare`, `nobody` 계정을 요구합니다. GUI의 기록된 환경은 Linux·CUDA 12.1·PyTorch 2.5.1·Chromium이며, 기본 자원 구성은 세 GPU에 역할을 나눕니다. [code-repair 환경](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/docs/reproduction.en.md#L9-L27) · [GUI 환경](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/tasks/gui/README.md#L55-L73)

### 준비된 환경에서 실행·재개·결과를 구분합니다

```bash
rsi assets code_repair --profile full --output assets
rsi plan --config configs/code_repair/default.json
rsi run --config configs/code_repair/default.json
```

출처: [README code-repair 실행](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/README.md#L142-L150). `plan`으로 해석된 Python·자산·출력 경로를 먼저 확인하고, `run`으로 실행합니다. 기본 code-repair recipe는 `.venv-code-repair`와 여러 GPU ID를 지정하므로 자신의 준비 상태와 맞아야 합니다. 자산 문서는 `evaluate` 프로필의 base model 약 6.2GB, `full` 약 21.4GB를 안내하며 새 체크포인트·환경·캐시 공간은 별도입니다. [기본 recipe](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/configs/code_repair/default.json#L1-L13) · [자산 크기와 해시](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/docs/assets.md#L20-L34)

GUI task 환경을 준비한 뒤의 상태 확인·재개·요약 명령은 다음과 같습니다.

```bash
rsi status --run runs/gui
rsi run --config configs/gui/default.json --resume
rsi report --run runs/gui
```

출처: [README run management](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/README.md#L170-L176). `status`는 저장된 상태를, `report`는 task 결과를 함께 읽습니다. `--resume`은 설정이 달라도 계속하는 옵션이 아니라 저장 identity가 같을 때 완료 단계를 재사용하는 옵션입니다.

### 작은 공개 추론 경로도 있습니다

반응 조건 추천기의 문서 예제는 NumPy·SciPy 기반 CPU 추론입니다.

```bash
python -m pip install -r tasks/reaction_optimization/requirements.txt
python tasks/reaction_optimization/infer.py \
  --observations tasks/reaction_optimization/examples/observations.json \
  --output runs/suzuki/next_condition.json
```

출처: [반응 추천 Quick Start](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/tasks/reaction_optimization/README.md#L29-L41). 포함된 관측 예제의 수율은 입력 형식 설명을 위한 합성값입니다. 실제 측정값으로 바꾸어야 하며, 출력 파일은 기존 파일을 덮어쓰지 않도록 생성됩니다. 이 예제를 실행하는 것만으로 논문의 화학 실험을 재현하거나 모델 재학습을 수행한 것은 아닙니다.

## 적용 전에 확인할 범위와 라이선스

레포의 유용한 설계는 예측 점수 자체뿐 아니라 **무엇을 언제 평가하고, 어느 산출물을 다음 단계로 넘길지 명시한 경계**에 있습니다. 공통 실행기는 설정·소스·출력의 동일성을, 코드 수정기는 공개 피드백과 hidden judge의 분리를, GUI는 개발셋 승격과 테스트 이전 버전 고정을 코드로 표현합니다. 이 문단은 구현을 읽은 리뷰어의 해석이며, 검증된 운영 성능을 추가로 주장하는 것은 아닙니다.

배포 범위도 함께 봐야 합니다. 최상위 CLI에는 lab/reaction/immune용 공통 task adapter가 없으며, 면역 world model은 아직 안내 문서 단계입니다. OSWorld는 문서에 비교 결과가 있지만 이 글에서 추적한 GUI 실행 경로는 MiniWoB++입니다. lab의 `forecast.feedback`과 reaction 예측표를 실제 평가 피드백으로 취급하면 학습 데이터나 성능 해석을 잘못 구성할 수 있습니다.

프로젝트 소유 코드는 Apache-2.0으로 표시됩니다. 그러나 모델·데이터·제3자 코드는 별도 고지를 유지합니다. 특히 레포가 포함한 Qwen2.5-Coder-3B-Instruct의 Research License는 연구·평가 목적과 상업적 사용을 구분합니다. 따라서 최상위 Apache-2.0 배지만으로 전체 모델 조합의 이용 조건이 같다고 판단할 수 없습니다. [프로젝트 라이선스 범위](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/LICENSE_STATUS.md#L1-L7) · [제3자 고지](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/THIRD_PARTY_NOTICES.md#L6-L19) · [동봉 Qwen 약관](https://github.com/Gen-Verse/RSI-Anything/blob/8ba44cd73ec6f57b151ec06e2f71a0726adfb687/tasks/gui/licenses/Qwen2.5-Coder-3B-Instruct.LICENSE#L15-L21)

## 결론

RSI-Anything은 예측 모델을 행동 선택에 연결하는 방법과, 실제 경험으로 다음 모델을 만드는 절차를 함께 살펴볼 수 있는 레포입니다. 그 구체적 형태는 코드 수정의 고정 coder·world 학습 파이프라인, GUI의 정책/world 갱신과 개발셋 승격, 실험실의 고정 계획 선택, 반응 조건의 고정 예측표 추천으로 나뉩니다. 이름에 담긴 범용성보다 각 도메인의 입력·평가·갱신 경계를 따라갈 때, 공개 구현에서 얻을 수 있는 학습 내용이 분명해집니다.

### 이 글에서 다루지 못한 부분

소스·문서·manifest·주요 진입점과 선택/갱신/재개 경로를 분석했습니다. JEPA vendor 내부 전체 수학 구현, code-repair의 모든 loss·데이터 복원·sandbox 구현, GUI의 모든 자원 스케줄러·통계 코드, 실험실 계획 parser의 모든 규칙, 대용량 자산 및 외부 모델의 실제 내용은 전수 분석하지 않았습니다. 공개 테스트·배포 검증 기록도 독립 실행으로 재검증하지 않았으며, 논문 전체를 별도로 심층 리뷰한 것은 아닙니다.
