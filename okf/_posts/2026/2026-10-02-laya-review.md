---
type: "Repo Review"
title: "[Repo Review] Laya: 텍스트 생성 없이 선택·점수·확률을 반환하는 의사결정 엔진"
description: "Laya의 모델 라우팅, 질문별 입력 구성, 선택지 점수화와 확률 보정·보류 과정을 코드로 추적하고 Hugging Face 모델·데모 및 조건별 평가의 의미를 살펴봅니다."
date: "2026-10-02"
tags:
  - "Repo Review"
  - "NLP"
  - "딥러닝"
  - "머신러닝"
  - "MCP"
  - "AI Agent"
resource: "https://github.com/NandhaKishorM/laya/tree/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c"
generated:
  by: "process:blog-review"
  at: "2026-10-02T11:14:53+09:00"
sources:
  - id: "NandhaKishorM/laya"
    resource: "https://github.com/NandhaKishorM/laya/tree/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c"
    title: "Laya"
  - id: "huggingface:convaiinnovations/laya"
    resource: "https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/README.md"
    title: "Laya model card"
  - id: "huggingface-spaces:convaiinnovations/laya-demo"
    resource: "https://huggingface.co/spaces/convaiinnovations/laya-demo/tree/a35778a39818de705c09b500ff1446686d42af28"
    title: "Laya demo"
status: "stable"
year: "2026"
analyzed_at: "2026-10-02T11:14:53+09:00"
source_id: "NandhaKishorM/laya"
source_revision: "4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c"
source_type: "repo"
source_url: "https://github.com/NandhaKishorM/laya/tree/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c"
visual_sources:
  - path: "img/reviews/2026/laya-review/runtime-flow.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/router.py#L868"
    caption: "리뷰어 작성, 분석 커밋 기준 Router에서 typed answer까지의 흐름"
  - path: "img/reviews/2026/laya-review/decision-head.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/common.py#L507"
    caption: "리뷰어 작성, 분석 커밋 기준 질문별 입력과 선택지 마커 점수화"
---

## 들어가며: 답변 문장보다 결정 값이 필요한 순간

고객 문의를 담당 부서로 보내거나, 검색한 문서가 질문과 관련 있는지 판단하거나, 메시지가 위험한지 분류하는 프로그램은 긴 설명보다 **미리 정한 선택지와 그 확률**이 필요한 경우가 많습니다. Laya는 이런 작업을 위해 상태와 질문을 입력받고, 자유로운 문장 생성 대신 선택·순서 점수·참일 확률을 반환하는 Python 의사결정 엔진입니다. 저자는 이를 빠른 판단에 해당하는 “System 1”이라고 부릅니다. 여기서 System 1은 인지 능력을 검증한 등급이 아니라 제품의 설계 방향을 표현하는 이름입니다. [README](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/README.md#L129)

이 프로젝트에서 공부할 핵심은 작은 모델이라는 사실보다 **출력 공간을 어떻게 제한하고, 질문을 어떻게 인코딩하며, 그 확률을 어디까지 믿을 수 있도록 설계했는가**입니다. 비자기회귀(non-autoregressive)는 앞에서 생성한 토큰을 이어 받아 다음 토큰을 반복 생성하지 않는다는 뜻입니다. 이것은 문장 생성과 JSON 파싱의 부담을 줄이지만, 분류 오류나 잘못된 확신을 없애지는 않습니다. 모델 카드의 “환각이 없다”, “수학적으로 보정된 확률”이라는 소개는 이러한 구현과 실제 평가 결과를 나눠 읽어야 합니다. [모델 카드](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/README.md#L10), [확률의 조건을 명시한 코드](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/common.py#L664)

분석은 GitHub SDK `4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c`, Hugging Face 모델 `55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851`, 데모 Space `a35778a39818de705c09b500ff1446686d42af28`을 구분해 고정했습니다. SDK 매니페스트의 버전은 **0.3.23**이며, 고정 HF 카드의 변경 안내는 **0.3.20** 기준입니다. 대상 코드를 설치·빌드·테스트하거나 모델 추론을 실행하지 않았으며, 아래 실행 명령과 성능은 원문의 예시와 보고값입니다. [패키지 정의](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/pyproject.toml#L5)

## 1. 저장소·모델·데모는 서로 다른 층입니다

| 구성 | 담고 있는 것 | 이 글에서 확인한 범위 |
|---|---|---|
| GitHub `NandhaKishorM/laya` | SDK, 라우터, 추론·보정 코드, CLI, 서버, 연구·벤치마크 자료 | 주요 실행 경로의 정적 분석 |
| HF `convaiinnovations/laya` | 모델 카드, 설정, 토크나이저·인코더 파일, 가중치와 하위 체크포인트 | 모델 카드와 설정; 가중치 실행·재학습 없음 |
| HF `laya-demo` Space | Gradio UI와 별도로 보관한 추론 코드, SDK 라우팅 연결 | 화면 및 코드 구조; 입력 제출·예측 검증 없음 |

기본 `Router`는 HF 저장소 루트에서 영어 모델을, `multilingual/`에서 다국어 모델을, `typed-decisions/`에서 업무 특화 모델을 가져옵니다. 각 모델의 독립 HF 저장소도 있지만, SDK 기본값은 하나의 묶음 저장소를 이용합니다. 필요한 하위 폴더만 다운로드하도록 `allow_patterns`를 구성하므로, 모델 하나를 쓸 때 세 모델을 반드시 모두 받아야 하는 것은 아닙니다. [모델 레지스트리](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/router.py#L47), [다운로드 범위](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/agent.py#L539)

| 체크포인트 | 인코더 | 저자가 제시한 파라미터 수 | 기본 전체 토큰 한도 | 역할 |
|---|---|---:|---:|---|
| `english` | ModernBERT-large | 421M | 512 | 영어 입력 |
| `multilingual` | mmBERT-base | 322M | 1,024 | 비영어·다국어 입력, 명시적 설정으로 최대 8,192 토큰 |
| `typed-decisions` | ModernBERT-large | 421M | 1,024 | 네 가지 typed-decisions 업무에 미세조정된 모델 |

파라미터 수와 100개 이상 언어 지원은 모델 카드의 사양입니다. 언어별 같은 품질을 뜻하지 않으며, 뒤에서 볼 공개 평가도 51개 언어의 특정 의도 분류 과제입니다. 기본 길이는 모델 설정의 `max_len`이고, 그 안에는 상태뿐 아니라 질문·선택지·구분 토큰도 함께 들어갑니다. `typed-decisions`라는 모델 이름과 SDK의 세 가지 질문 타입도 구분해야 합니다. 세 체크포인트 모두 typed 질문을 받으며, 마지막 모델만 특정 업무에 추가 학습됐습니다. [모델 카드 사양](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/README.md#L94), [영어 설정](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_agent_config.json), [다국어 설정](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/multilingual/rl_agent_config.json), [업무 특화 설정](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/typed-decisions/rl_agent_config.json)

## 2. 외부에는 간단한 API, 내부에는 다섯 단계가 있습니다

![상태와 질문이 Router, Agent, DecisionModel, 확률 후처리를 거쳐 반환되는 흐름]({{ '/img/reviews/2026/laya-review/runtime-flow.svg' | relative_url }})

*리뷰어 작성, 분석 커밋 기준. [Router.predict](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/router.py#L868), [Agent의 배치 처리](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/agent.py#L1334), [응답 디코딩](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/agent.py#L1179)을 연결했습니다. HF 다운로드는 모델이 필요할 때 발생하는 외부 경계입니다.*

| 파일 | 책임 |
|---|---|
| `laya/router.py`, `laya/lang.py` | 모델 선택, 언어 휴리스틱, 모델 상주·교체, 요청 그룹화 |
| `laya/agent.py` | 체크포인트 로드, 질문 검증, 토큰화, 추론, 결과 반환 |
| `laya/common.py` | 상태·선택지 직렬화, 입력 시퀀스, 결정 모델, 확률 관련 공통 함수 |
| `laya/calibrate.py`, `laya/confidence.py` | 온도 보정, 신뢰도 임계값과 보류 표시 |
| `laya/structured.py` | JSON Schema/Pydantic 기반 질문 생성과 타입 값 투영 |
| `laya/cli.py`, `laya/serve.py`, `laya/mcp/` | CLI·HTTP·MCP 진입점 |

패키지는 Python 3.10 이상을 요구하고 PyTorch, Transformers, Safetensors, Hugging Face Hub, NumPy를 기본 의존성으로 선언합니다. FastAPI/uvicorn은 `serve`, MCP는 `mcp`, Pydantic은 `structured` 선택 의존성입니다. `laya`, `laya-serve`, `laya-evals`, `laya-mcp-server`라는 콘솔 진입점도 매니페스트에 선언돼 있습니다. [매니페스트](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/pyproject.toml#L5)

## 3. Router: 추론하기 전에 읽을 수 있는 모델을 고릅니다

`Router.route()`는 모델을 실행하지 않고 사용할 체크포인트와 이유를 반환합니다. 선택 우선순위는 다음과 같습니다.

1. 호출자가 지정한 `model`
2. 명시한 `task`
3. `auto_task_detection=True`일 때 업무 질문 ID 집합의 일치
4. 명시한 `lang`
5. 호출 또는 Router에 설치한 `lang_guess`
6. 내장 문자·언어 감지
7. 언어를 판단하지 못할 때 기본 모델

이 순서는 운영상 의미가 있습니다. `model="english"`를 명시하면 한글 상태라도 해당 선택이 우선합니다. `task="typed_decisions"`도 언어 감지보다 먼저 적용됩니다. 자동 업무 감지는 기본 경로에서 켜지지 않으며, 켰을 때조차 `urgency` 같은 한 단어가 아니라 다섯 개 질문 ID의 **전체 집합**을 맞춥니다. 대상은 에이전트 실행 기록, 고객 서비스, 송장 처리, 보안 사고의 네 업무입니다. [분기 구현](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/router.py#L774), [업무 시그니처](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/router.py#L84)

내장 감지는 별도의 신경망 언어 모델을 실행하는 방식이 아닙니다. 문자 체계·언어 단서와 구조화된 상태의 문자열 필드를 살펴보는 휴리스틱입니다. 한글처럼 비라틴 문자가 감지되면 다국어 모델로 보내며, 라틴 문자라도 영어가 아닌 것으로 판단하면 다국어를 선택합니다. 긴 영어 오류 로그가 짧은 외국어 고객 메시지를 덮어쓰지 않도록 줄·필드 수준 검사도 들어 있습니다. 반대로 짧고 애매한 라틴 텍스트는 기본 모델로 돌아갈 수 있으므로, 이미 알고 있는 언어를 `lang`이나 `lang_guess`로 전달하는 경로가 있습니다. [언어 감지](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/lang.py#L644), [감지 결과 분기](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/router.py#L833)

`Router.predict()`는 이 선택 뒤 모델을 로드하고 `Agent.system_one()`을 호출한 다음 `routing`을 결과에 붙입니다. 기본 Router는 지연 로드하며 최대 두 체크포인트를 상주시킵니다. `preload=True`는 세 모델을 미리 읽고 상주 한도를 맞춥니다. `max_loaded=1`은 메모리를 줄일 수 있지만 언어가 바뀔 때 재로드 비용이 생깁니다. 따라서 이미 메모리에 올라온 모델의 추론 시간과 첫 다운로드·초기화가 포함된 응답 시간을 구분해야 합니다. [호출 연결](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/router.py#L911), [모델 상주 정책](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/README.md#L228)

## 4. Agent: 상태 하나와 질문 여러 개를 어떻게 한 번에 처리하나요?

### 4.1 질문은 자연어 설명을 가진 출력 스키마입니다

질문은 ID를 키로 하는 사전이며 각 항목에 `type`, `instructions`, `criteria`가 들어갑니다. 상태는 문자열·사전·리스트입니다. 사전과 리스트는 JSON으로 직렬화하고, 질문은 내부의 `t`, `ins`, `crit` 형식으로 정규화합니다. `choice`의 목록형 선택지는 사전으로 바뀌고, `noul`의 참·거짓 키는 정규화됩니다. 질문 검증은 모델 forward 이전에 수행됩니다. [직렬화](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/common.py#L75), [정규화](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/agent.py#L988), [검증 호출](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/agent.py#L1334)

| 질문 타입 | 기준의 의미 | 반환값 해석 |
|---|---|---|
| `choice` | 이름을 붙인 선택지와 설명 | 확률이 가장 높은 선택지와 선택지별 확률 |
| `score` | 낮은 단계부터 순서대로 나열한 기준 | 단계 인덱스의 확률 가중 평균과 분포 |
| `noul` | 진술이 성립하는지 판단하는 참·거짓 기준 | 참에 해당하는 두 번째 선택지의 확률 |

특히 `score`는 자유로운 실수 회귀가 아니라 **순서가 있는 이산 선택지의 분포를 요약한 값**입니다. 기준이 세 단계라면 인덱스는 0, 1, 2이고, 반환 점수는 각 인덱스에 확률을 곱한 합입니다. 기준 문자열이 “1점, 2점, 3점”이라고 적혀 있어도 원시 `score`는 0부터 시작하는 인덱스 공간입니다. [응답 구현](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/agent.py#L1208)

### 4.2 질문마다 상태가 붙은 입력 행을 만듭니다

입력 시퀀스는 다음 순서입니다. 아래는 구현의 입력 형식 설명을 그대로 옮긴 것입니다.

```text
[CLS] <type> instructions [SEP] [MASK] opt0 [MASK] opt1 ... [SEP] state [SEP]
```

출처: [`build_sequence`의 형식 설명](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/common.py#L148).

`[MASK]`는 뒤따르는 각 선택지의 위치를 표시합니다. 여기서는 마스크 토큰을 생성해 채우는 언어 모델 작업이 아니라, 해당 위치의 은닉 표현을 모아 선택지 점수를 계산하는 용도로 씁니다. 선택지 설명의 길이와 순서는 모델이 보는 입력 자체에 영향을 줍니다. 문자열에 원래 들어 있던 마스크 토큰은 공백으로 치환합니다. [질문 구성](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/common.py#L196)

![질문별 입력 행에서 선택지 마커를 모아 로짓과 타입별 응답을 만드는 구조]({{ '/img/reviews/2026/laya-review/decision-head.svg' | relative_url }})

*리뷰어 작성, 분석 커밋 기준. [입력 행 구성](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/agent.py#L1011)과 [DecisionModel.forward](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/common.py#L507)를 재구성했습니다. 질문별 행은 배치 차원에서 묶이며, 여러 질문이 하나의 입력 시퀀스를 공동으로 쓰는 구조가 아닙니다.*

공유 상태는 한 번 토큰화해서 재사용하지만, **질문마다 질문+선택지+상태를 가진 행을 따로 만듭니다**. `system_one()`은 내부적으로 `predict_batch([state], questions)`에 연결되고, `collate_items()`가 이 행들을 패딩해 한 forward에 넣습니다. 따라서 “single forward pass”는 질문 수와 무관한 고정 계산량이라는 뜻이 아닙니다. 질문이 많으면 행이 늘고, 상태 배치를 나누면 forward도 여러 번 발생합니다. [상태 토큰 재사용](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/agent.py#L1018), [system_one 연결](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/agent.py#L1744), [배치 forward](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/agent.py#L1364)

### 4.3 전체 길이와 질문 길이는 다른 예산입니다

`max_len`은 전체 시퀀스 한도이고 `head_max_len`은 질문·선택지 부분을 구성할 때 쓰는 예산입니다. `build_head()`는 선택지 설명을 먼저 최대 48토큰으로 제한하고, 예산이 부족하면 선택지마다 더 짧게 자릅니다. 그 뒤 남은 공간에 상태를 넣습니다. 일반 문자열·사전 상태는 앞부분을, 시간순 대화로 취급하는 리스트는 뒷부분을 보존하도록 잘라냅니다. [선택지 예산](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/common.py#L205), [상태 절단](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/common.py#L173), [리스트 정책](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/agent.py#L1020)

이 동작 때문에 “모델 컨텍스트가 1,024토큰”이라는 말만으로 문서 1,024토큰을 다 읽었다고 볼 수 없습니다. 선택지가 길수록 상태 공간이 줄고, 서로 다른 선택지 설명이 같은 토큰 접두사로 잘릴 수도 있습니다. 코드에서는 마커 자체가 사라지면 오류를 내고, 선택지 표현이 겹치면 `usage.options`에 개수와 구별 가능한 개수를 기록합니다. 상태 손실도 `usage.truncated`, `state_tokens_dropped`, `truncated_questions`로 보고합니다. [마커 검증](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/agent.py#L1040), [usage 반환](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/agent.py#L1385)

긴 문서는 다국어 모델의 `max_len`을 늘리는 경로와 `predict_long()`으로 창을 나눠 검사하는 경로를 구분해야 합니다. 후자는 반복 추론·집계가 들어가므로 “한 번 읽기”의 지연시간과 같지 않습니다. 고정 README의 8,192토큰 안내도 실제 문서 길이에 따른 정확도 변동을 함께 제시하며, 영어 장문이 자동으로 영어 모델로 가는 것을 피하려면 `model="multilingual"`을 지정하라고 설명합니다. [긴 문서 안내](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/README.md#L36), [창 기반 API](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/agent.py#L1441)

## 5. DecisionModel: 인코더와 typed head가 선택지를 점수화합니다

`DecisionModel`은 양방향 Transformer 인코더의 `last_hidden_state`를 받습니다. 여기에 세 질문 타입 중 하나의 임베딩을 더하고, 설정된 추가 Transformer head 층을 통과시킵니다. 영어 HF 설정은 `head_layers=2`입니다. 이어 각 선택지 마커 위치의 벡터를 `torch.gather()`로 모은 뒤 공통 scorer가 선택지별 스칼라 로짓을 만듭니다. 패딩된 선택지는 큰 음수로 마스킹합니다. [모델 구성](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/common.py#L472), [영어 설정](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_agent_config.json)

```python
idx = marker_pos.clamp(min=0)[:, :, None].expand(-1, -1, h.size(-1))
m = torch.gather(h, 1, idx)
logits = self.scorer(m).squeeze(-1).float()
logits = logits.masked_fill(~marker_mask, -1e4)
```

출처: [`DecisionModel.forward` 일부](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/common.py#L521). 인용은 선택지 점수화 부분만 발췌했습니다.

여기서 typed head는 각 부서 이름마다 독립적인 고정 분류기를 두는 구조가 아닙니다. 선택지 설명을 입력으로 읽고, 공통 scorer가 각 마커를 점수화합니다. 질문의 종류는 별도의 type embedding으로 반영됩니다. 이 설계 덕분에 선택지 수나 설명을 호출 시점에 바꿀 수 있지만, 설명 문구·선택지 순서·토큰 예산의 영향을 피할 수는 없습니다. [type embedding과 scorer](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/common.py#L494), [선택지 구성](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/common.py#L107)

또 하나의 `act_head`는 첫 토큰의 표현에 최고 확률, 상위 두 확률 차이, 정규화 엔트로피, 선택지 수 관련 특징을 붙여 행동 로짓을 냅니다. 응답에는 이것이 `action.act_probability`로 나타납니다. **이 값이 정답 확률이나 자동 실행 허가를 뜻한다고 해석하면 안 됩니다.** 모델 카드는 이 값이 거의 모든 입력에서 1.0에 가깝고, 396개 라벨 있는 판단에서 원시 로짓의 정답 구분 AUROC가 0.30이었다고 보고합니다. 보조 head의 존재와 유용한 정책 신호의 학습 성공은 별개의 문제입니다. [act head](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/common.py#L526), [모델 카드의 한계](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/README.md#L355)

## 6. 보정과 보류: 어떤 확률을 어떻게 써야 하나요?

### 6.1 출력 직전의 온도 보정

`Agent._decode_answers()`는 질문 타입과 선택지 수 구간에 맞는 온도를 선택합니다. 구간은 `2`, `3-5`, `6-10`, `11+`이며, 해당 구간 값이 없으면 타입별 값을 씁니다. 언어별 보정이 주어지면 해당 언어 설정을 우선합니다. 선택한 온도로 로짓을 나눈 뒤 softmax를 계산하며, 선택지를 순열로 재배치해 입력했다면 확률을 원래 선택지 순서로 되돌립니다. [온도 선택·softmax](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/agent.py#L1183), [구간 정의](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/common.py#L697)

온도는 양수인 하나의 스칼라이므로 같은 질문의 최고 로짓 순서를 바꾸지 않고 분포의 날카로움을 조절합니다. 따라서 보정이 정확도 자체를 높여 주는 절차라고 보면 안 됩니다. `calibrate.py`는 정답 분포와 로짓으로 음의 로그우도를 최소화하도록 `log(T)`를 LBFGS로 최적화합니다. `compute_ece=True`이면 구간별로 일부 기록을 분리해 보정에 쓰지 않은 데이터에서 ECE를 계산하고, 표본이 부족해 평가에서 빠진 구간도 보고합니다. 기본 `False` 경로는 모든 입력으로 온도를 맞추며 평가 보고서를 생성하지 않습니다. [온도 학습](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/calibrate.py#L71), [분리 평가](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/calibrate.py#L211)

ECE(Expected Calibration Error)는 확률 구간별 평균 신뢰도와 실제 정답률의 차이를 요약한 값입니다. 한 데이터셋에서 낮은 ECE를 얻었다고 다른 언어·도메인·선택지 수에서도 같은 정답률을 보장하는 것은 아닙니다. 코드 자체도 이 조건을 `answer_confidence()` 설명에 명시합니다. [ECE 구현](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/common.py#L651), [조건 설명](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/common.py#L664)

### 6.2 이름이 비슷한 세 신호를 구분합니다

| 필드 | 실제 계산·의미 | 사용할 때 읽어야 할 조건 |
|---|---|---|
| `answer_confidence` | 모든 질문 타입에서 가장 큰 선택지 확률 | 체크포인트·도메인·선택지 수에 맞춰 보정하고 평가할 대상 |
| `confidence` | `choice`·`score`는 1 − 정규화 Shannon 엔트로피; `noul`은 참/거짓 중 큰 확률 | 타입에 따라 정의가 달라 같은 임계값을 일괄 적용하기 어려움 |
| `action.act_probability` | 보조 행동 head 출력 | 모델 카드가 유효한 신호를 아직 확보하지 못했다고 명시 |

특히 `score`의 `answer_confidence`도 기대 점수의 오차 허용 확률이 아니라 가장 유력한 **이산 단계의 확률**입니다. 이 필드를 점수 회귀의 오차 막대처럼 해석해서는 안 됩니다. [응답 디코딩](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/agent.py#L1200), [신뢰도 함수](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/common.py#L664)

분석한 HF 영어 설정에는 `choice:11+` 온도가 약 **0.10058**로 들어 있습니다. 현재 SDK는 온도를 **[0.5, 5.0]**으로 제한하며, 범위를 벗어난 값이 바뀌면 영향을 받은 항목의 신뢰도를 보정되지 않은 것으로 취급하라는 경고를 냅니다. 같은 가중치여도 런타임 버전이 바뀌면 반환 확률이 달라질 수 있는 구체적인 사례입니다. 범위를 제한했다는 사실만으로 재보정이 완료되는 것도 아닙니다. [HF 설정](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_agent_config.json), [온도 제한](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/common.py#L702), [로드 시 경고](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/agent.py#L657)

### 6.3 `min_confidence`는 모델의 답을 삭제하는 스위치가 아닙니다

`predict()`에 `min_confidence`를 주면 우선 `answer_confidence`를 읽고, 유효한 값이 없으면 기존 `confidence`로 대체합니다. 임계값 미만이면 `low_confidence: True`를 추가하지만 원래 선택·확률은 보존합니다. 임계값을 설정한 응답은 `abstention`에 `passed`, `abstained`, `unevaluated` 중 하나와 `abstention_threshold`를 보고합니다. 신뢰도를 계산할 수 없는 상태와 통과한 상태가 다릅니다. 임계값이 없으면 이 보류 관련 필드도 추가하지 않습니다. [게이트 구현](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/confidence.py#L38)

JSON Schema/Pydantic을 쓰는 `decide()`는 한 단계 더 나아갑니다. boolean을 `noul`, enum을 `choice`, 범위가 있는 숫자 필드를 `score` 질문으로 바꾸고, 결과를 원래 타입 값으로 투영합니다. 이때 보류된 필드는 `None`이 됩니다. 원시 `score`가 확률 가중 평균인 것과 달리 스키마 숫자 값은 단계 선택 후 최솟값을 반영하는 변환이 들어갑니다. 스키마 형식으로 반환된다는 사실은 그 값의 의미적 정답을 검증했다는 뜻이 아닙니다. [스키마 필드 변환](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/structured.py#L124), [출력 투영](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/structured.py#L218)

### 6.4 RLCD의 학습 목표와 실제 보정 품질

저자가 RLCD(Reinforcement Learning for Calibrated Decisions)라고 부르는 학습은 분포 보고에 보상을 주는 방식입니다. 모델 카드는 로짓에 노이즈를 넣고, strictly proper scoring rule을 사용하며, 그룹 평균 기준선을 가진 REINFORCE 계열 갱신과 다중 턴의 TD 목표를 설명합니다. SDK의 `proper_reward()`에서는 로그 점수와 spherical score를 더하고, 순서 점수 질문에는 누적 분포 차이에 대한 ranked probability score 항을 반영하는 코드를 확인할 수 있습니다. [모델 카드 학습 설명](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/README.md#L291), [보상 함수](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/common.py#L604)

이론적 보상 설계가 정직한 분포 보고를 유도한다는 주장과, 유한한 데이터로 학습한 모델이 실제 분포 이동에서도 정확히 보정되어 있다는 주장은 구분해야 합니다. 모델 카드의 홍보 문구보다, 배포 온도 경고·재보정 API·실측 ECE를 함께 읽는 편이 구현에 충실합니다. 이 리뷰는 학습 전체를 재현하거나 RLCD의 수학적 보장 조건을 별도로 증명하지 않았습니다.

## 7. 배치·훅·서버에서 추가되는 동작

`Router.predict_batch()`는 먼저 모델별로 묶고, 같은 모델 안에서도 질문 스키마·토큰 예산·보정 언어가 맞는 요청끼리 나눕니다. 선택지 순서는 의미가 있기 때문에 스키마를 직렬화할 때 사전 키를 정렬하지 않습니다. 단순히 질문 이름이 같다고 같은 배치로 합치지 않는 이유입니다. Agent는 길이순 정렬을 선택적으로 적용한 뒤 결과를 원래 상태 순서로 되돌립니다. [스키마 서명](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/router.py#L150), [그룹별 전달](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/router.py#L1240), [배치 정렬](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/agent.py#L1359)

훅은 예측 전후에 관찰·입력 변경·결과 재사용을 연결하는 확장점입니다. Router의 시작 훅은 라우팅·모델 로드 뒤 실행되고, 이미 결과가 있으면 추론을 생략할 수 있습니다. 정상 경로의 `elapsed_ms` 측정 시작도 라우팅·로드 이후입니다. 따라서 이 훅의 시간값을 콜드 스타트까지 포함한 전체 지연시간으로 읽으면 안 됩니다. [훅과 시간 측정](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/router.py#L911)

HTTP 서버는 동기 PyTorch 추론이 이벤트 루프를 막지 않도록 별도 실행 풀을 사용합니다. 분석 커밋의 풀은 `max_workers=1`이고, 요청 수용 한도는 별도 세마포어로 관리합니다. 한도를 넘기면 `503`과 `Retry-After: 1`을 반환합니다. 이것은 API에 동시에 들어오는 요청 수와 실제 모델 forward 병렬도를 구분한 설계입니다. [실행 풀](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/serve.py#L697), [과부하 응답](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/serve.py#L804)

`/health`는 프로세스 생존 응답이며 모델이 모두 준비됐다는 뜻은 아닙니다. `LAYA_API_KEY`가 있으면 비인증 요청에는 생존 상태만 주고, 올바른 bearer가 있을 때 로드된 모델·revision·장치·CPU 폴백 정보를 노출합니다. 키가 없으면 상세 정보가 공개되는 기본 동작입니다. [헬스 엔드포인트 설명](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/docs/http-api.md#L45), [핸들러](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/serve.py#L755)

## 8. HF 데모: 같은 화면 안에서도 실행 경로가 다릅니다

데모는 Support triage, Email + phishing, LLM guardrails, RAG passage filter, Moderation, Model routing, Multilingual routing, Playground의 여덟 탭을 제공합니다. 앞의 업무 탭은 미리 구성한 질문으로 Laya의 활용 형태를 보여 주고, Playground는 상태와 질문 JSON을 직접 넣는 경로입니다. 화면의 실행 상태와 탭은 확인했지만 예측 버튼을 눌러 품질이나 지연시간을 측정하지 않았습니다. [고정 Space의 UI 코드](https://huggingface.co/spaces/convaiinnovations/laya-demo/blob/a35778a39818de705c09b500ff1446686d42af28/app.py#L194)

| 데모 탭 | 입력 → 모델 판단 | 데모 코드의 후속 처리 |
|---|---|---|
| Support triage | `customer message`와 `account tier` → 의도·급함·불만·환불 요청·이탈 위험 | 임계값 아래면 사람에게 넘긴다는 문구, enterprise 환불이면 관리자 승인 안내를 표시합니다. 실제 결제 취소나 환불 API 호출은 없습니다. |
| RAG passage filter | `query`와 빈 줄로 나눈 `retrieved passages` → 관련성·모순·숨은 지시 여부 | 최대 12개 지문을 평가하고 `KEEP`/`DROP` 판정을 표로 만듭니다. 문서를 검색하거나 최종 답변을 생성하는 단계는 없습니다. |
| Model routing | `user request`, `cheap model`, `strong model` → 난도·분야·도구 필요·민감성 | 조건문으로 모델 이름 또는 캐시/사람 검토 안내 문자열을 만듭니다. 선택한 외부 LLM을 호출하지는 않습니다. |

출처: [triage 함수](https://huggingface.co/spaces/convaiinnovations/laya-demo/blob/a35778a39818de705c09b500ff1446686d42af28/rl_agent_demo.py#L180), [RAG 필터](https://huggingface.co/spaces/convaiinnovations/laya-demo/blob/a35778a39818de705c09b500ff1446686d42af28/rl_agent_demo.py#L269), [모델 선택 함수](https://huggingface.co/spaces/convaiinnovations/laya-demo/blob/a35778a39818de705c09b500ff1446686d42af28/rl_agent_demo.py#L329). 여기서 RAG는 검색한 근거를 생성 모델에 제공하는 방식이며, 이 데모는 그중 검색 결과를 거르는 부분을 보여 줍니다. 화면의 “Model routing”과 SDK가 영어·다국어 체크포인트를 고르는 Router도 서로 다른 층입니다.

처음 살펴볼 때는 Support triage의 기본 중복 청구 메시지나 Model routing의 `Examples`를 읽고, 그 입력이 어떤 질문에 답하도록 구성됐는지 확인하는 흐름이 좋습니다. 질문까지 직접 보고 싶으면 Playground의 `state (JSON or plain text)`와 `questions`를 함께 읽습니다. 실제 예측을 요청하는 버튼 이름은 `Ask`이며, 이후에는 답변 표와 `raw response`의 선택·점수·확률을 비교하는 구조입니다. 이 리뷰는 해당 버튼을 실행하지 않았습니다. [UI 입력·버튼](https://huggingface.co/spaces/convaiinnovations/laya-demo/blob/a35778a39818de705c09b500ff1446686d42af28/app.py#L194), [Examples](https://huggingface.co/spaces/convaiinnovations/laya-demo/blob/a35778a39818de705c09b500ff1446686d42af28/app.py#L274), [Playground](https://huggingface.co/spaces/convaiinnovations/laya-demo/blob/a35778a39818de705c09b500ff1446686d42af28/app.py#L317)

데모의 Support triage 슬라이더는 `confidence needed to act without a human`이며, 실제 조건문은 의도 질문의 기존 `confidence`를 읽습니다. 이것은 앞서 설명한 최신 SDK의 `min_confidence`/`answer_confidence` 보류 계약과 다릅니다. 데모의 사람 검토 문구를 SDK의 `abstention` 필드와 혼동하지 않아야 합니다. [데모의 임계값 처리](https://huggingface.co/spaces/convaiinnovations/laya-demo/blob/a35778a39818de705c09b500ff1446686d42af28/rl_agent_demo.py#L196)

중요한 차이는 대부분의 탭이 `rl_agent_demo.py`의 `RLAgent`를 거치고, 다국어 라우팅 탭은 설치된 `laya` 패키지의 `Router`를 별도로 사용하는 점입니다. `app.py`는 먼저 `D.get_agent()`로 모델을 준비하고, 라우팅이 가능하면 그 영어 agent를 Router에 붙여 재사용합니다. requirements의 `laya>=0.3.2`는 정확한 버전 고정이 아닙니다. 그러므로 이 Space 화면이 분석한 SDK 0.3.23의 모든 보정·보류 동작을 그대로 대표한다고 단정할 수 없습니다. [기본 agent import](https://huggingface.co/spaces/convaiinnovations/laya-demo/blob/a35778a39818de705c09b500ff1446686d42af28/rl_agent_demo.py#L10), [공유와 라우팅 준비](https://huggingface.co/spaces/convaiinnovations/laya-demo/blob/a35778a39818de705c09b500ff1446686d42af28/app.py#L34), [Router 연결](https://huggingface.co/spaces/convaiinnovations/laya-demo/blob/a35778a39818de705c09b500ff1446686d42af28/laya_routing.py#L1), [의존성](https://huggingface.co/spaces/convaiinnovations/laya-demo/blob/a35778a39818de705c09b500ff1446686d42af28/requirements.txt)

ZeroGPU 호출은 공통 `gpu_call()` 경로를 사용하고, GPU 경로가 실패하면 원인을 기록하고 CPU 호출로 전환하는 코드가 있습니다. 이 때문에 화면이 열린다는 사실과 GPU에서 예측한다는 사실도 다릅니다. 예시 탭은 질문 설계와 출력 필드를 관찰하는 자료로 이해하고, 실제 데이터셋의 성능 근거는 별도로 봐야 합니다. [GPU/CPU 경로](https://huggingface.co/spaces/convaiinnovations/laya-demo/blob/a35778a39818de705c09b500ff1446686d42af28/app.py#L48)

## 9. 벤치마크: 조건이 다른 숫자를 한 성능으로 합치지 않습니다

아래 수치는 저자 저장소에 보고된 값이며 리뷰어의 재측정이 아닙니다. 특히 `BENCHMARKS.md`는 과거 측정과 재실행 값, 보정 전후, 결과 파일이 없는 보고값을 스스로 구분합니다.

| 평가 조건 | 영어 | 다국어 | 읽는 방법 |
|---|---:|---:|---|
| T4, 한 질문 호출 지연시간 | 39.5ms | 32.8ms | 약 33ms는 이 표의 다국어 모델 값 |
| T4, 질문 10개 호출 지연시간 | 158.6ms | 72.3ms | 72.3ms는 호출 전체; 약 7.2ms는 질문당 환산 |
| MASSIVE 51언어, 20지선다, 재실행 macro accuracy | 0.2269 | 0.4008 | 언어별 평균이며 무작위 기준은 0.05 |
| 위 재실행의 한국어 100개 사례 accuracy | 0.110 | 0.470 | 한국어 전체 능력이 아니라 해당 의도 분류 조건 |
| 위 재실행의 영어 accuracy | 0.820 | 0.710 | 모든 입력을 다국어로 보내는 것도 손해일 수 있음 |

출처: [T4 속도표](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/BENCHMARKS.md#L191), [51언어 재실행 설명](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/BENCHMARKS.md#L13), [언어별 표](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/BENCHMARKS.md#L55). 원래 51언어 결과 파일의 다국어 macro accuracy 0.3661은 재현되지 않아 문서가 0.4008로 갱신했습니다. HF 카드에 남아 있는 “무작위의 3배를 넘는 언어 45/51”과 GitHub 재실행의 48/51도 동일한 측정판으로 합치면 안 됩니다. [기록된 변경 이유](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/BENCHMARKS.md#L27), [HF 카드 표](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/README.md#L175)

업무 특화 typed-decisions 표에서는 400개 사례·2,000개 판단에 대해 미세조정 모델 정확도 **0.766**, 영어 기본 모델 **0.362**, 다국어 기본 모델 **0.352**를 제시합니다. 다수 클래스 기준은 0.461입니다. 기본 모델은 이 기준보다 낮고, 개선은 특화 학습 조건에 연결돼 있습니다. 더구나 문서는 미세조정 모델의 0.766과 업무별 세부 점수에는 **커밋된 결과 파일이 아직 없다**고 명시합니다. 이는 문서 보고값으로 소개할 수는 있지만 결과 파일까지 확인한 재현 증거와 같은 무게로 다룰 수는 없습니다. [typed-decisions 표와 한계](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/BENCHMARKS.md#L168)

온도 재적합 표는 영어 ECE 0.466→0.081, 다국어 0.314→0.106을 보고합니다. 이 숫자는 보정의 중요성을 보여 주지만, 기본 배포가 이미 ECE 0.081이라는 뜻은 아닙니다. 다른 한편 Applications 평가의 held-out toxicity 분류는 영어·업무 특화 모델 모두 정확도 0.530, jailbreak 분류는 모델별 0.708~0.762입니다. 예쁜 데모와 실제 판단 품질을 구분해야 하는 이유입니다. [보정 보고](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/BENCHMARKS.md#L202), [업무별 평가](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/BENCHMARKS.md#L136)

Jev와 비교한 수치는 저자 문서가 가져온 상대 제품의 공개 측정입니다. 같은 장치·데이터·평가 코드에서 이 리뷰가 재실행한 통제 비교가 아니며, Banking77은 모델 카드에서 상대 72개 라벨과 Laya 77개 라벨이라는 차이까지 표시합니다. 따라서 “몇 배 빠르고 더 정확하다”는 하나의 결론으로 일반화하기보다, 과제·선택지 수·학습 포함 여부·측정 환경을 함께 읽어야 합니다. [비교 조건](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/README.md#L309), [GitHub 비교표](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/BENCHMARKS.md#L154)

## 10. 설치와 사용: 문서에 있는 경로부터 확인합니다

다음은 분석 커밋의 문서에 실제로 있는 명령과 예시입니다. 이 리뷰에서는 실행하지 않았습니다. 버전을 지정하지 않은 설치 명령은 실행 시점의 배포판을 가져오므로, 고정한 소스 커밋과 같은 환경을 보장하지 않습니다.

### Python SDK

```bash
python -m pip install laya
```

출처: [README 설치](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/README.md#L24). 아래 Python 예시는 같은 README의 quickstart에서 결과 출력 부분만 생략했습니다.

```python
from laya import Router

router = Router()

state = "Hi, we were billed twice for March. Please refund the duplicate today or we will cancel our plan."
questions = {
    "department": {"type": "choice", "instructions": "Which department should handle this?",
                   "criteria": {"billing": "invoices, payments, refunds",
                                "technical": "bugs, outages, system errors",
                                "other": "everything else"}},
    "urgency": {"type": "score", "instructions": "How urgent is this?",
                "criteria": ["not urgent", "soon", "blocking"]},
    "churn_risk": {"type": "noul", "instructions": "Does the user threaten to cancel or leave?"},
}

result = router.predict(state, questions)
```

출처: [README quickstart](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/README.md#L52). 이 예시는 부서·긴급도·해지 위험을 한 요청의 서로 다른 질문으로 정의합니다. 출력은 `result["answers"]`의 질문별 필드와 `result["routing"]`, `result["usage"]`를 함께 읽어야 합니다. 주석에 적힌 정답을 이 리뷰의 실행 결과로 옮기지는 않았습니다.

### CLI·HTTP·MCP

| 인터페이스 | 문서의 명령 | 실행되는 역할 |
|---|---|---|
| CLI 라우팅만 | `laya "I was charged twice, please refund it"` | 모델 forward 없이 라우팅 설명 |
| CLI 프리셋 | `laya "My payment failed twice" --preset triage` | 질문 프리셋으로 예측 |
| HTTP | `pip install "laya[serve]"` 뒤 `laya-serve` | `/v1/systemone` 및 배치 엔드포인트 |
| MCP | `python -m pip install "laya[mcp]"` 뒤 `laya-mcp-server` | 표준 입출력으로 도구 제공 |

출처: [CLI](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/docs/cli-mcp.md#L39), [HTTP](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/docs/http-api.md#L1), [MCP](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/docs/cli-mcp.md#L117). MCP(Model Context Protocol)는 외부 에이전트와 도구를 연결하는 프로토콜입니다. 여기서는 HTTP 서버를 띄우는 방식이 아니라 클라이언트가 관리하는 stdio 프로세스입니다. `laya_route`, `laya_predict`, 배치 도구, `laya_decide`, `laya_shortlist`, 프리셋과 상태 도구가 등록돼 있습니다. [도구 등록](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/mcp/server.py#L205)

HTTP 서버는 기본 `0.0.0.0:8000`을 사용하며 `LAYA_DEVICE`, `LAYA_PRELOAD`, `LAYA_MODELS`, `LAYA_API_KEY` 등으로 동작을 구성합니다. SDK의 `Router()` 기본 지연 로드와 HTTP의 기본 사전 로드 설정은 다릅니다. 모델이 필요해지는 최초 시점과 메모리 요구량을 인터페이스별로 확인해야 합니다. [HTTP 설정표](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/docs/http-api.md#L17)

### 컨테이너와 모델 고정

```bash
docker compose run --build --rm laya
```

출처: [Docker CPU quickstart](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/docs/docker.md#L1). 저장소 루트에서 샘플 요청을 CPU로 실행하는 명령이며, 문서는 RAM 8GB·디스크 10GB와 Docker Compose v2 이상을 준비 조건으로 제시합니다. CUDA 경로는 별도 override를 사용합니다.

```bash
docker compose -f compose.yaml -f compose.cuda.yaml run --build --rm laya
```

출처: [Docker CUDA 문서](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/docs/docker.md#L25). 장치 사용 여부뿐 아니라 CPU 폴백도 확인해야 합니다. Agent는 가중치 배치 실패나 추론 중 메모리 문제에 대응하는 경로를 갖고 있으며, 서버는 실제 체크포인트 장치와 폴백 상태를 보고합니다. 이는 장치 독립적인 성능 보장을 뜻하지 않습니다. [장치 로드](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/agent.py#L724), [추론 경로](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/agent.py#L1083)

재현성을 위해서는 코드 버전뿐 아니라 모델 revision도 분리해 기록해야 합니다. 기본 다운로드는 자동으로 검토된 SHA에 고정되지 않습니다. `revision`/`LAYA_REVISION`으로 지정하거나 `reviewed` 설정을 선택하는 경로가 있으며, `expected_sha256`은 파일 무결성을 확인하는 선택 기능입니다. `model.safetensors` 외에 `rl_agent_config.json`, tokenizer와 encoder 설정도 추론 결과에 관여합니다. [revision 계약](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/revisions.py#L1), [다운로드와 검증](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/agent.py#L539)

## 11. 적용 전에 이해할 경계

첫째, **비생성형 출력은 형식 제약이지 정답 보장 수단은 아닙니다.** 출력 선택지를 제한하므로 자유 생성 문장이 깨지는 문제는 줄지만, 입력 증거를 놓치거나 틀린 선택지를 높은 확률로 고르는 문제는 남습니다. “환각 없음”을 “오판 없음”으로 바꿔 읽으면 안 됩니다. 모델 카드도 보정·도메인·선택지 수와 `noul` 편향의 한계를 별도로 기록합니다. [Honest Limits](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/README.md#L355)

둘째, **질문 문구가 모델의 입력 데이터입니다.** 카드에는 영어 체크포인트의 `noul`이 상태보다 `false:`/`true:` 라벨에 끌릴 수 있다는 보고가 있습니다. 중립적인 키를 쓰는 2지선다 `choice`로 같은 판단을 비교하는 대안을 제시하지만, 이것 역시 모든 데이터에서 해결됨을 보장하지는 않습니다. 현재 SDK가 custom noul labels를 지원한다는 사실과 특정 업무에서 효과를 검증했다는 사실도 구분해야 합니다. [카드의 noul 한계](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/README.md#L365), [라벨 처리](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/common.py#L93)

셋째, **긴 문서·많은 선택지·새 언어는 각각 다른 실패 경로를 만듭니다.** 긴 문서는 상태 절단, 많은 선택지는 설명의 충돌, 새 언어는 라우팅 오류와 체크포인트 적합성 문제로 이어질 수 있습니다. 확률 하나만 보는 대신 `routing`과 `usage`를 함께 보도록 응답이 설계돼 있다는 점이 이 저장소의 실용적인 학습 포인트입니다. [라우팅 출력](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/router.py#L947), [사용량·절단 진단](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/laya/agent.py#L1385)

저장소 LICENSE는 Apache License 2.0이며 HF 카드도 `apache-2.0`으로 표시합니다. 자체 호스팅은 모델 API 호출료를 다른 사업자에게 내지 않는 배포 선택이지만, 계산 자원·메모리·운영 비용이 사라진다는 뜻은 아닙니다. [코드 LICENSE](https://github.com/NandhaKishorM/laya/blob/4aa6761be8173de4ce6d92c31b3e40b6eaf59a7c/LICENSE), [모델 라이선스 메타데이터](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/README.md#L1)

## 마무리

Laya의 중심은 자연어로 정의한 제한된 질문을 인코더 입력으로 구성하고, 선택지 마커를 점수화해 타입이 있는 값으로 돌려주는 구조입니다. Router는 모델 적합성을, Agent는 입력 예산과 배치를, 후처리는 확률 해석과 보류를 담당합니다. 같은 “신뢰도”라는 이름 아래 다른 값이 존재하고, 같은 가중치도 보정 설정과 런타임에 따라 다른 확률을 반환한다는 점까지 읽어야 이 엔진의 동작을 이해할 수 있습니다.

### 이 글에서 다루지 못한 부분

핵심 eager PyTorch 경로와 라우터·보정·출력·HTTP·MCP 진입점에 집중했습니다. ONNX export 및 양자화, TileLang 커널·CUDA graph, TypeScript SDK, LangChain·LlamaIndex·CrewAI 통합의 세부 동작, shortlist 검색 정확도, 학습 노트북 전체와 모든 연구 평가 스크립트는 전수 분석하지 않았습니다. `predict_long`의 존재와 입력 예산 관계를 설명했지만 집계 정책 전체를 검증한 것은 아닙니다. 대상 코드·모델·학습·벤치마크는 실행하지 않았고, Space의 예측 품질도 직접 시험하지 않았습니다.
