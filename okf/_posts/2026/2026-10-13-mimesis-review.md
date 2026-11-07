---
type: "Repo Review"
title: "[Repo Review] MIMESIS: 사용자 시뮬레이터 학습에서 GRPO와 CSD까지 코드로 따라가기"
description: "MIMESIS의 사용자 시뮬레이터 학습·평가와 에이전트 GRPO·CSD를 입력, 보상, 비공개 코칭, 토큰 정렬까지 고정 커밋 코드로 추적합니다."
date: "2026-10-13"
tags:
  - "Repo Review"
  - "AI Agent"
  - "강화학습"
  - "머신러닝"
  - "Distillation"
  - "딥러닝"
resource: "https://github.com/VietHoang1512/mimesis/tree/58034ff9887cd67914e7acac2a73965fb7cb3782"
generated:
  by: "process:blog-review"
  at: "2026-10-13T06:05:33+09:00"
sources:
  - id: "viethoang1512/mimesis"
    resource: "https://github.com/VietHoang1512/mimesis/tree/58034ff9887cd67914e7acac2a73965fb7cb3782"
    title: "MIMESIS: Learning User Simulators as Training Environments for Interactive Agents"
  - id: "arxiv:2610.09484v2"
    resource: "https://arxiv.org/abs/2610.09484v2"
    title: "MIMESIS: Learning User Simulators as Training Environments for Interactive Agents"
status: "stable"
year: "2026"
analyzed_at: "2026-10-13T06:05:33+09:00"
source_id: "viethoang1512/mimesis"
source_revision: "58034ff9887cd67914e7acac2a73965fb7cb3782"
source_title: "MIMESIS: Learning User Simulators as Training Environments for Interactive Agents"
source_type: "repo"
source_url: "https://github.com/VietHoang1512/mimesis/tree/58034ff9887cd67914e7acac2a73965fb7cb3782"
visual_sources:
  - path: "/img/reviews/2026/mimesis-review/training-flow.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/agents/base_agent.py#L112-L132"
    caption: "리뷰어 작성, 분석 커밋 기준. simulator의 감독학습·강화학습과 agent의 별도 학습 경계를 정적 코드로 재구성했습니다."
  - path: "/img/reviews/2026/mimesis-review/csd-flow.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/workers/rollout/sglang_rollout/sglang_rollout_customized.py#L881-L989"
    caption: "리뷰어 작성, 분석 커밋 기준. 공개 대화의 rollout과 학습 전용 코칭·교사 재평가를 구분했습니다."
---

## 들어가며

대화형 에이전트는 질문을 잘하는 능력도 배워야 합니다. 그런데 학습 상대가 늘 요구를 명확히 말하고 친절하게 협력한다면, 실제 사용자가 정보를 빠뜨리거나 요구를 바꾸는 상황을 충분히 경험하기 어렵습니다. MIMESIS는 이런 문제를 **사용자 역할을 맡는 모델 자체를 학습하는 문제**로 다룹니다. 사람 대화로 사용자 시뮬레이터를 학습한 다음, 그 시뮬레이터를 고정한 상태에서 별도의 에이전트를 강화학습합니다. 이 두 단계의 구분은 [저장소 README](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/README.md#L18-L27)와 [논문 v2 초록](https://arxiv.org/abs/2610.09484v2)에 명시되어 있습니다.

이 글은 논문 실험의 재현 보고가 아니라 **공개 코드의 정적 리뷰**입니다. 분석 대상은 `VietHoang1512/mimesis`의 전체 커밋 `58034ff9887cd67914e7acac2a73965fb7cb3782`입니다. README, 설정, 진입점과 핵심 모듈을 읽었으며 의존성 설치, 빌드, 테스트, 모델 추론 및 저장소 스크립트 실행은 하지 않았습니다. [공식 프로젝트 페이지](https://viethoang1512.github.io/mimesis/)와 논문은 연구 정체성과 방법의 맥락을 확인하는 보조 자료로 사용했습니다. 아래 동작 설명은 이 커밋의 코드에서 확인한 경로이며, 실행 성공이나 성능을 뜻하지 않습니다.

## MIMESIS는 무엇을 공개했는가

MIMESIS는 사용자 시뮬레이터의 학습·평가 코드와, 그것을 환경으로 사용하는 에이전트의 다중 턴 강화학습 코드를 함께 공개한 연구 저장소입니다. 에이전트 쪽에는 GRPO와 CSD가 있습니다. GRPO는 같은 문제에서 여러 대화를 생성하고 그룹 안에서 상대적인 보상을 사용해 정책을 학습하는 방법입니다. CSD(Coached On-Policy Self-Distillation)는 모델이 실제 생성한 응답을 코칭이 붙은 문맥에서 다시 평가해 토큰별 학습 신호를 더하는 자기 증류입니다. 코드에서는 CSD를 `sdpo`, 코칭 메모를 `hint`라고 부르므로 이 이름을 알고 읽어야 연결이 보입니다. [출처: agent README](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/README.md#L1-L10)

README가 보고하는 결과와 이 리뷰에서 확인한 구현은 구분해야 합니다.

| 항목 | README의 보고 | 이 글에서 확인한 범위 |
|---|---|---|
| 사용자 시뮬레이터 | 9B 모델의 SOUL-Index 65.7, RealUserSim PT3 94.0 | 학습 입력 가공, 행동 보상, 평가 생성·집계 코드의 연결 |
| 에이전트 GRPO | GPT-5.5 환경 학습 26.10 → MIMESIS-9B 환경 학습 29.54 | 다중 턴 보상 배분과 그룹 정규화 구현 |
| CSD 추가 | MIMESIS-9B 환경에서 평균 31.09 | 비공개 채널, 코칭, 교사 토큰 정렬과 보조 손실 |

에이전트 수치는 README에서 여덟 환경의 점수를 평가 사용자별로 평균한 뒤, 아홉 평가 사용자에 대해 제시한 `Mean`입니다. 서로 다른 벤치마크 점수를 같은 정확도로 해석하면 안 됩니다. 수치는 [README의 결과 표와 평가 조건](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/README.md#L34-L60)에 실린 저자 보고이며, 이 리뷰는 원시 결과 파일이나 실험 실행으로 재검증하지 않았습니다.

## 저장소 구조와 두 학습 경계

| 경로 | 책임과 진입점 |
|---|---|
| `simulator/sft/` | 중간 감독학습 데이터의 역할 변환, ThoughtTrace 추론 감독학습 |
| `simulator/scripts/run_rl.sh` | 24개 과제 데이터 경로와 simulator RL 설정을 조립하는 런처 |
| `simulator/agents/` | `data_source`별 대화 루프·보상 함수, 사용자 행동 과제 |
| `simulator/verl/` | simulator 학습에 포함된 verl 프레임워크 사본 |
| `simulator/eval/`, `simulator/scoring/` | 대화 생성·심사·지표 집계와 외부 벤치마크 연결 |
| `agent/scripts/`, `agent/examples/` | 에이전트 SFT/RL/평가 런처, 다중 턴 설정·전처리 |
| `agent/llm/`, `agent/verl/tools/` | 사용자 API 프록시, 환경 생성, 도구 실행과 비공개 채널 읽기 |
| `agent/verl/workers/` | SGLang rollout, 코칭 생성, 교사 재평가, 정책 업데이트 |

이 구분은 [simulator README의 구조](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/README.md#L55-L66)와 [agent README의 구조](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/README.md#L67-L78)를 따라가며 코드로 대조한 것입니다. 두 하위 프로젝트 모두 패키지 이름을 `verl`로 선언합니다. 따라서 문서도 별도 환경 사용을 요구합니다. simulator는 [pyproject.toml](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/pyproject.toml#L13-L24), agent는 [setup.py](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/setup.py#L77-L93)에 선언되어 있습니다. agent 요구사항에는 `vllm==0.9.1`, `sglang[srt]==0.4.7` 등이 있지만 모든 의존성이 버전 고정되어 있지는 않습니다. [출처: requirements](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/requirements.txt#L1-L26)

![MIMESIS의 사용자 시뮬레이터 학습과 에이전트 학습을 잇는 전체 흐름]({{ '/img/reviews/2026/mimesis-review/training-flow.svg' | relative_url }})

*리뷰어 작성, 분석 커밋 기준. simulator의 [역할 변환](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/sft/sft_data.py#L286-L302), [ThoughtTrace 변환](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/sft/trl_sft.py#L162-L213), [과제 라우팅](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/agents/base_agent.py#L112-L132), agent의 [학습 설정](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/scripts/_train_common.sh#L67-L119)을 재구성했습니다. 위쪽은 simulator 가중치를, 아래쪽은 별도 agent 가중치를 학습합니다. 모델을 자동으로 이전·배포하는 단일 파이프라인을 뜻하지 않습니다.*

## 사용자 시뮬레이터는 어떻게 학습되는가

### 1. Parquet 입력을 사용자 턴 예측 문제로 바꿉니다

첫 단계 런처 `run_sft.sh`는 데이터 클래스에 `OdysSimSFTDataset`을 지정하고 verl SFT trainer로 넘깁니다. 입력은 여러 Parquet 파일이며, 최대 prompt 16,384토큰·response 8,192토큰, 전체 길이 24,576토큰을 기본으로 설정합니다. 이러한 값은 실행 관측값이 아니라 런처 기본값입니다. [출처: run_sft.sh](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/scripts/run_sft.sh#L81-L127)

데이터 클래스는 파일명 뒤의 비율과 glob을 해석하고, 파일별 행 인덱스를 표본 추출한 뒤 섞습니다. 비율이 1보다 크면 복원 추출을 사용합니다. Parquet 행 전체를 모델에 바로 주는 대신, `data_source`에 맞는 processor를 선택하고 `input_ids`, `responses`, `response_mask`를 받습니다. 마지막에는 전체 시퀀스에 대한 `loss_mask`와 `position_ids`로 변환합니다. 즉 여러 출처의 자료를 한 trainer가 받을 수 있는 공통 표현으로 맞추는 단계입니다. [출처: 파일 해석](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/sft/dataset.py#L20-L47), [표본 추출·출력](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/sft/dataset.py#L122-L182)

일반 대화 processor의 핵심은 `user`와 `assistant` 역할 교환입니다. 실제 사람의 턴을 모델이 생성해야 하는 `assistant` 자리에 두고, 원래 AI 답변은 문맥의 `user` 자리에 둡니다. system 메시지는 유지합니다. 아래는 실제 소스의 역할 교환 부분만 인용한 것입니다.

```python
elif msg["role"] == "assistant":
    msg["role"] = "user"
    corrected_messages.append(msg)
elif msg["role"] == "user":
    msg["role"] = "assistant"
    corrected_messages.append(msg)
```

출처: [`process_swap`, L294–L299](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/sft/sft_data.py#L294-L299). 앞뒤 분기는 생략했습니다.

`_tokenize_chat`은 각 턴을 chat template로 렌더링한 증가분을 누적하고, 생성 역할의 헤더를 제외한 토큰에만 손실 마스크 1을 붙입니다. 다른 역할은 0입니다. 턴별 토큰을 합친 결과가 전체 대화 렌더링과 같은지도 비교합니다. 이는 **대화 문맥은 읽되 학습 대상으로 삼는 화자는 선택한다**는 설계를 드러냅니다. [출처: 토큰화와 마스크](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/sft/sft_data.py#L185-L251)

다만 README의 “모든 대화를 역할 교환한다”는 설명을 모든 데이터에 적용하면 부정확합니다. 실제 라우터에는 `human_llm`, 여러 Theory of Mind(타인의 의도·믿음을 추론하는 과제), 사회적 추론·증류 자료를 `process_no_swap`으로 보내는 분기가 있습니다. 이 경우 기존 `assistant` 메시지가 그대로 학습 표적입니다. 따라서 이 커밋은 **출처별로 역할 교환 여부가 다른 혼합 감독학습**으로 읽어야 합니다. [출처: 분기표](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/sft/sft_data.py#L16-L109), [교환 없는 processor](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/sft/sft_data.py#L382-L393)

### 2. ThoughtTrace에서 동기와 발화를 함께 감독합니다

둘째 단계는 verl SFT와 별개의 TRL `SFTTrainer` 진입점입니다. JSONL 레코드에서 과제 요약, 기대 사항, 설문 프로필을 system prompt로 만들고, 엄격히 교대하는 대화만 남깁니다. 실제 사람 메시지에 달린 `reasons`를 `<think>…</think>`에 넣은 다음 실제 발화를 이어 붙입니다. 이 묶음을 모델 출력 역할인 `assistant`에 둡니다. 원래 AI 답변은 `user`가 됩니다. [출처: 프로필 구성과 대화 변환](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/sft/trl_sft.py#L126-L213)

코드는 `include_reactions`를 켜면 직전 AI 응답에 대한 사람의 반응 주석도 추론에 합칠 수 있습니다. 하지만 인자 설명은 기본값이 꺼져 있고 공개 실험은 `reasons`만 사용했다고 명시합니다. “ThoughtTrace에 동기와 반응이 있다”는 데이터 설명과 “기본 학습에서 두 주석을 모두 쓴다”는 구현 주장은 다른 내용입니다. [출처: 인자 설명](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/sft/trl_sft.py#L45-L63)

런처는 `assistant_only_loss=True`, 전용 thinking chat template, 최대 길이 32,768, 3 epochs를 전달합니다. trainer는 학습 후 모델을 저장하며, 기본 모델의 processor 설정 파일이 있으면 출력 디렉터리로 복사합니다. 이렇게 만들어지는 것은 사용자의 **비공개 추론과 공개 발화를 함께 생성하도록 감독한 모델 체크포인트**입니다. [출처: 런처](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/scripts/run_trl_sft.sh#L34-L97), [trainer 구성·저장](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/sft/trl_sft.py#L255-L310)

### 3. 여러 과제의 rollout이 같은 simulator를 업데이트합니다

셋째 단계 `run_rl.sh`는 24개 과제 파일의 학습·검증 목록을 조립합니다. 여기에 Sotopia, CoSER, 마음 이론 과제, Humanual의 여러 분야, 사용자 행동 과제가 함께 들어갑니다. 런처의 기본값은 prompt당 8개 응답, batch 64, 총 500학습 step이고, `train_ppo.py`가 verl의 `main_ppo.main`을 호출합니다. 실제 PPO trainer를 만드는 곳은 `verl/trainer/main_ppo.py`입니다. [출처: 과제 목록·설정](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/scripts/run_rl.sh#L31-L115), [얇은 진입점](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/train_ppo.py#L13-L16), [trainer 구성](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/verl/trainer/main_ppo.py#L320-L370)

rollout의 출발점은 `AgentHubLoop`입니다. `agents.yaml`이 이 클래스를 등록하고, 클래스는 현재 모델을 호출하는 `CallLLM`과 `TaskContext`를 만든 뒤 입력의 `data_source`로 개별 과제 루프를 선택합니다. 이 단계에서 학습 대상 모델은 사용자 시뮬레이터입니다. 파일명에 `agent`가 있어도 뒤의 `agent/` 프로젝트에서 학습할 에이전트와 혼동하면 안 됩니다. [출처: 등록](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/agents/agents.yaml#L1-L5), [라우터·호출](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/agents/base_agent.py#L28-L132)

반환값의 공통 형태는 생성 토큰, 로그 확률, 생성 토큰에 대한 `response_mask`, 보상인 `AgentLoopOutput`입니다. 공통 `AgentContext`는 상대 모델이 넣은 문맥과 simulator가 생성한 부분을 토큰 마스크로 구분합니다. thinking을 켠 학습에서 형식 검사가 실패하면 학습 보상은 0으로 바뀝니다. 반면 설명용 지표는 별도 필드에 남길 수 있으므로 로그의 원점수와 실제 업데이트 보상을 무조건 같다고 보면 안 됩니다. [출처: 마스크 구성](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/agents/utils.py#L815-L837), [출력·형식 보상](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/agents/utils.py#L926-L1008)

simulator 런처가 선택하는 advantage 계산은 `foldgrpo`입니다. 하나의 rollout이 여러 하위 시퀀스로 나뉠 때 `gen_uid`가 같은 샘플을 그룹 평균·표준편차 계산에서 한 번만 세고, 정규화한 보상을 생성 토큰 마스크에 곱합니다. 대화가 더 많은 조각으로 나뉘었다는 이유만으로 그룹 기준에 더 크게 기여하지 않도록 하는 구현입니다. 이는 뒤에서 살펴볼 agent의 `grpo_multiturn`과 별도 함수입니다. [출처: 선택 설정](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/scripts/run_rl.sh#L189-L247), [foldgrpo 구현](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/verl/trainer/ppo/core_algos.py#L333-L383)

### 4. 사용자 행동 과제의 보상은 무엇을 요구하는가

가장 구체적으로 추적한 과제는 `usersim_behavior`입니다. 입력 행에는 JSON 문자열인 `scenario`, `behavior_ids`, `kwargs`와 고객지원의 `flow`, `subflow`, `turn_budget`이 있습니다. 코드는 목록 전체를 동시에 실행하지 않고 첫 번째 행동 ID와 인자를 선택합니다. 행동 ID가 비어 있으면 협력적인 사용자 대조군으로 처리합니다. 고객지원 대화의 앞부분을 넣은 뒤, 학습 중인 simulator와 `ABCDSupportAgent`가 번갈아 말합니다. 공개 기록에는 추론을 제거한 발화를, 별도 private 기록에는 추론과 발화를 저장합니다. [출처: 입력과 대화 루프](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/agents/usersim_behavior/agent.py#L120-L169)

행동 registry에는 숨긴 평가 기준, 단계적 요구 변경, 설명 요청에 비협조하기, 갑작스러운 의도 전환 등 13개 클래스가 있습니다. 일부 행동은 심사할 때 추론까지 읽도록 `needs_trace`를 사용합니다. 다만 뒤에서 설명하듯 행동 정의 JSON은 이 스냅샷에 없어, 클래스 목록의 존재와 전체 과제의 실행 준비 상태는 구분해야 합니다. [출처: 추론 필요 행동](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/agents/usersim_behavior/behaviors.py#L32-L45), [13개 클래스 registry](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/agents/usersim_behavior/behaviors.py#L510-L536)

심사 모델은 행동 표현 `exhibit`, 적절한 시점 `placement`, 자연스러움 `naturalness`, 과제 일관성 `on_task`를 반환합니다. 각각 가중치 2.0, 1.5, 1.0, 0.5로 합산한 뒤 총 가중치로 나누고 0~1로 제한합니다. 행동을 대놓고 선언했다는 `announced` 판정이 있으면 다시 2로 나눕니다. 규칙 검사값 `rule`도 계산하지만, 실제 `_reward`에서는 이를 보상에 직접 합치지 않고 `rule_judge_gap` 등 진단값으로 기록합니다. 심사 실패는 0점입니다. [출처: 가중치·심사 스키마](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/agents/usersim_behavior/agent.py#L45-L80), [보상 함수](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/agents/usersim_behavior/agent.py#L83-L117), [심사·최종 출력](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/agents/usersim_behavior/agent.py#L175-L237)

이 구조를 보면 목표는 무조건 어려운 사용자를 만드는 것이 아닙니다. **지정한 행동을 적절한 맥락에서 자연스럽게 표현하면서 고객지원 과제와의 연결도 유지하게 만드는 것**으로 읽을 수 있습니다. 이는 위 보상 구성에 대한 리뷰어 해석이며, 실제 사람 행동 분포와의 일치를 이 코드만으로 입증한 것은 아닙니다.

## 시뮬레이터 평가의 입력과 출력

사용자를 닮았는지와 좋은 에이전트 학습 환경인지는 다른 질문입니다. 저장소도 simulator 자체의 평가와 뒤의 agent 평가를 나눕니다.

| 평가 경로 | 입력 → 처리 → 출력 | 정적 리뷰에서의 주의점 |
|---|---|---|
| SOUL | 모델·seed → 평가 로그 → dataset별 점수 JSON·범주 평균 | 런처가 참조하는 파일 일부가 공개 tree에 없습니다 |
| RealUserSim PT3 | 사람 대화·프로필 → simulator와 고정 assistant의 대화 → 원 대화와 사용자 발화 비교 → JSONL·CSV | judge와 assistant 설정이 바뀌면 외부 기준 수치와 직접 비교할 수 없습니다 |
| τ-USI | τ-bench 단일 과제 대화 → 특징·survey → 사람 집단과의 분포 비교 → 집계 JSON | 단일 과제 성공 보상과 집단 정렬 지표 USI는 다릅니다 |
| Turing 평가 | 시험 Parquet → 생성물 JSON → 사람/합성 쌍 심사 → 항목·요약 JSON | 심사 실패·파싱 실패 개수를 함께 봐야 합니다 |
| SimulatorArena | 외부 저장소 + transport·patch → 벤치마크 대화·심사 | 핵심 외부 저장소는 포함되어 있지 않습니다 |

SOUL 런처는 기본 seed `0 1 2`를 순회하며 대화 저장을 켭니다. 집계기 `scoring/aggregate.py`는 로그에서 지표를 추출하고, 값이 없는 로그가 기존 점수 JSON을 덮어쓰지 않도록 합니다. 그러나 런처 연결의 누락 때문에 이 커밋만으로 평가가 곧바로 돌아간다고 설명할 수 없습니다. [출처: 런처](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/scripts/run_eval.sh#L33-L55), [집계기](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/scoring/aggregate.py#L80-L164)

RealUserSim의 `run_case`는 프로필 조건으로 simulator system prompt를 만든 뒤 assistant와 대화를 교환하고, 종료 토큰 또는 턴 예산에서 멈춥니다. `judge_one`은 원 대화와 합성 대화의 사용자 발화를 비교해 심사하고, 별도 호출로 JSON 판정 형식으로 바꿉니다. 집계 단계는 사례마다 다섯 차원의 일치 판정 비율을 FI(Fidelity Index)로 계산하며, `user_ip` 단위 cluster bootstrap으로 신뢰구간을 계산합니다. 코드 자체도 assistant/judge가 GPT-5.5여서 기존 공개 GPT-4o 설정의 FI와 절대값을 직접 비교할 수 없다고 출력합니다. [출처: 대화 생성](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/eval/realusersim_eval.py#L251-L292), [심사](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/eval/realusersim_eval.py#L338-L363), [집계·비교 조건](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/eval/realusersim_eval.py#L568-L631)

τ-USI는 특징 분포의 Dice-Sørensen 유사도 D1~D4, 성공률의 보정 오차 ECE, 선택적인 survey 기반 Eval을 결합합니다. Eval이 없을 때는 네 특징 점수와 `(1−ECE)×100`의 다섯 항 평균을 사용하고, 있으면 여섯 항 평균을 사용합니다. 따라서 과제 한 건의 성공 여부를 USI라고 부르면 안 됩니다. README의 “AgentArena와 bit-identical”은 저장소 작성자의 검증 주장으로 남겨 두며, 이 리뷰에서는 그 검증을 반복하지 않았습니다. [출처: USI 조합 코드](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/agents/tau_usi/usi_metric.py#L474-L534), [문서의 검증 주장·실행 분리](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/agents/tau_usi/README.md#L5-L27)

Turing 평가 코드는 생성과 심사를 나누고, 모든 심사가 실패하면 전체가 NaN인 요약을 저장하지 않도록 예외를 발생시킵니다. SimulatorArena는 문서상 외부 저장소에 patch와 transport를 넣어 사용합니다. 두 경로가 모두 Turing이라는 말을 쓰더라도 지표 정의와 외부 코드가 같다고 가정할 수 없습니다. [출처: Turing 요약](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/eval/turing_eval.py#L304-L341), [SimulatorArena 연결](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/eval/simarena/SETUP.md#L1-L47)

## 에이전트 GRPO: 공개 대화에서 보상까지

### 1. 별도 SFT 체크포인트와 환경 데이터를 준비합니다

agent의 RL은 기본 모델에서 바로 시작하지 않습니다. `sft/README.md`는 성공한 상호작용 trace의 감독학습을 거친 Qwen3-8B를 출발점으로 설명합니다. LLaMA-Factory는 외부 프로젝트이며 `merged_gym_sft` 데이터는 여기 포함되지 않았다고 명시합니다. 따라서 RL 코드가 있다고 SFT부터 전체 실험을 이 저장소만으로 재구성할 수 있는 것은 아닙니다. [출처: SFT 출발점과 데이터](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/sft/README.md#L1-L39)

환경 설치 런처는 UserRL과 τ-bench를 shallow clone하고 patch를 적용한 뒤 여덟 gym 패키지를 설치하도록 작성되어 있습니다. 전처리 런처는 UserRL의 데이터를 복사하고, `data_source`별로 기본 5%를 검증용으로 뽑아 `train.parquet`, `val.parquet`으로 저장합니다. 이는 행 인덱스의 중복과 유실을 검사하지만 사용자·시나리오 단위의 누출 방지를 별도로 보장하는 코드는 아닙니다. [출처: 외부 환경 경계](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/scripts/install_gyms.sh#L7-L36), [데이터 연결](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/scripts/prepare_data.sh#L5-L15), [분할 코드](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/examples/data_preprocess/make_rl_val_split.py#L11-L34)

예를 들어 TravelGym 전처리는 `prompt`, `reward_model`, `extra_info.tools_kwargs`를 만듭니다. 여기에 공개 초기 요청과 시스템 지침, 정답 ID, 환경 이름과 사례 ID가 들어갑니다. rollout은 prompt로 에이전트를 시작하고 `create_kwargs`로 같은 사례의 환경을 생성합니다. [출처: TravelGym 레코드](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/examples/data_preprocess/travel_multiturn_w_tool.py#L52-L93)

### 2. 도구 호출이 gym의 상태 전이가 됩니다

기본 학습 런처는 `verl.trainer.main_ppo`에 `grpo_multiturn` 설정을 전달하고 SGLang rollout을 사용합니다. 도구 schema는 `interact_with_env(choice, content)`이고 선택지는 `action`, `answer`, `search`입니다. `EnvironmentManager`는 request ID별 환경을 보관합니다. `InteractTool`은 choice를 `[action]`, `[answer]`, `[search]` 문자열 접두사로 바꿔 `env.step_async`에 전달합니다. 환경의 관측·보상·종료 여부를 기록하고 에이전트에게 피드백 텍스트와 `Reward: …`를 돌려줍니다. [출처: 실행 설정](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/scripts/_train_common.sh#L67-L108), [도구 schema](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/examples/sglang_multiturn/config/tool_config/interact_tool_config.yaml#L1-L19), [환경 관리](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/tools/env_manager.py#L74-L132), [도구 실행](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/tools/interact_tool.py#L100-L175)

환경 step이 예외로 실패하면 0점·종료로 처리하고, timeout에서는 별도 실행 경로를 시도합니다. 따라서 이런 실패를 사용자의 실제 거절과 동일한 의미의 학습 신호로 해석해서는 안 됩니다. 성공한 대화와 실패한 외부 호출의 비율을 보려면 로그가 필요합니다. 여기서는 그 로그를 생성하지 않았습니다. [출처: 실패 분기](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/tools/interact_tool.py#L122-L147)

### 3. 대화 보상을 턴과 토큰에 배분합니다

공통 런처의 기본값은 prompt당 rollout 8개, 최대 16턴, 할인율 `gamma=0.8`, 턴 credit와 trajectory score 모두 `R2G`입니다. 이 함수의 R2G는 뒤에서 앞으로 보상을 할인해 누적하는 reward-to-go입니다. 전체 대화의 첫 시점 반환값을 trajectory score로 삼고, 각 턴에는 그 턴부터의 누적 보상을 줍니다. [출처: 기본값](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/scripts/_train_common.sh#L23-L39), [credit 계산](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/trainer/ppo/core_algos.py#L682-L732)

`compute_grpo_multiturn_advantage`는 이 credit를 턴 경계 사이 토큰에 배분하고, 생성 토큰 마스크를 적용합니다. 이후 같은 prompt 그룹의 trajectory score 평균·표준편차로 정규화한 값을 구합니다. 마지막에는 해당 대화의 0이 아닌 토큰 credit 평균이 그룹 정규화 값에 맞도록 스케일을 조정합니다. 단순히 대화 최종 점수 하나를 모든 턴에 동일하게 복사하는 구현이 아닙니다. credit 합계가 0이면 advantage도 0이 됩니다. [출처: 턴 배분·그룹 정규화](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/trainer/ppo/core_algos.py#L735-L843)

한 가지 읽기 주의점은 `trajectory_score_method="Sum"`이라는 이름입니다. 해당 분기는 코드상 턴 보상의 **평균**을 계산합니다. 기본 런처는 R2G로 덮어쓰지만, 기본 YAML만 읽거나 설정 이름만 보고 합이라고 해석하면 학습 신호를 오해할 수 있습니다. [출처: Sum 분기](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/trainer/ppo/core_algos.py#L695-L707)

driver는 보상과 advantage를 batch에 합친 뒤 actor 업데이트를 호출합니다. actor는 이전·현재 로그 확률과 advantage로 clipping이 있는 정책 손실을 계산합니다. 이 정책 손실이 CSD 보조항의 바탕입니다. 최종 산출물은 사용자 모델이 아닌 **학습된 agent 체크포인트와 학습·검증 지표**이며, 저장 주기와 출력 경로는 런처가 지정합니다. [출처: driver의 업데이트](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/trainer/ppo/ray_trainer.py#L1132-L1205), [정책 손실](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/workers/actor/dp_actor.py#L599-L625), [저장 설정](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/scripts/_train_common.sh#L109-L119)

## CSD: 비공개 사용자 신호를 토큰별 감독으로 바꾸는 경로

### 1. 프록시는 추론을 숨기면서 episode별로 저장합니다

CSD의 시작은 손실 함수보다 API 경계에 있습니다. `llm/shim.py`는 upstream 모델의 원 응답에서 `<think>` 블록을 분리합니다. gym으로 반환할 `message.content`에는 공개 발화만 넣고, 추론은 episode ID를 key로 한 메모리 버퍼에 저장합니다. 별도 `GET /ep/{episode}/privileged`가 저장된 추론 목록을 반환합니다. [출처: 추론 분리·버퍼](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/llm/shim.py#L55-L95), [조회 API](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/llm/shim.py#L168-L188), [응답 처리](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/llm/shim.py#L207-L223)

`EnvironmentManager`는 CSD가 켜졌을 때 gym의 base URL에 `/ep/{request_id}/v1`을 붙여 대화를 구분합니다. `InteractTool`은 step 이후 그 환경의 `/privileged`를 조회하고 마지막 추론을 `metrics["privileged"]`에 공개 피드백과 함께 넣습니다. 이 데이터는 에이전트에 돌려주는 `response_text`와 별도 채널입니다. [출처: URL 분리](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/tools/env_manager.py#L31-L71), [조회 구현](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/tools/interact_tool.py#L17-L53), [별도 metrics](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/tools/interact_tool.py#L161-L175)

![공개 대화 rollout과 비공개 코칭을 거쳐 같은 생성 토큰을 재평가하는 CSD 경로]({{ '/img/reviews/2026/mimesis-review/csd-flow.svg' | relative_url }})

*리뷰어 작성, 분석 커밋 기준. [shim](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/llm/shim.py#L168-L223), [rollout post-pass](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/workers/rollout/sglang_rollout/sglang_rollout_customized.py#L881-L989), [교사 행 구성](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/workers/rollout/sdpo_hint.py#L345-L394), [actor 손실](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/workers/actor/dp_actor.py#L629-L734)을 재구성했습니다. 코칭은 rollout 완료 뒤 별도 학습 문맥에 들어갑니다.*

코칭 작성용 shim은 사용자 shim과 별개로 설정해야 합니다. 코드에는 동일 endpoint 사용을 막는 사전 검사가 있습니다. 코칭 요청이 사용자 추론 버퍼에 섞이면 턴 대응이 깨지기 때문입니다. 또한 `TauGym`, `FunctionGym`은 episode scope를 적용할 수 없는 환경으로 선언되어 있고, CSD post-pass에서도 건너뜁니다. 이 커밋의 CSD가 모든 gym에서 동일하게 비공개 신호를 사용하는 것은 아닙니다. [출처: 예외 환경과 endpoint 검사](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/tools/env_manager.py#L24-L54), [post-pass 제외](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/workers/rollout/sglang_rollout/sglang_rollout_customized.py#L881-L894)

### 2. rollout 완료 후 코칭할 턴을 고릅니다

CSD를 켜는 런처는 `USERRL_SDPO=1`, 기본 보조항 계수 `0.01`을 설정합니다. 공통 런처의 기본 코칭 스타일은 `prospective`, estimator는 `sdar`, gate 계수는 5.0입니다. GRPO 대조 런처는 계수를 0으로 설정합니다. 이 리뷰의 설명은 이러한 기본 경로를 중심으로 하며 모든 실험 옵션이 동시에 켜진 것으로 쓰지 않습니다. [출처: CSD 런처](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/scripts/run_sdpo.sh#L10-L15), [GRPO 런처](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/scripts/run_grpo.sh#L1-L6), [공통 CSD 설정](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/scripts/_train_common.sh#L48-L58)

SGLang rollout이 끝나면 `_sdpo_post_pass`는 assistant 메시지와 토큰 경계를 맞추고 코칭할 턴을 선택합니다. 선택 함수는 직전 사용자 추론이 있는 턴을 우선 표본 추출하고 부족하면 나머지 턴에서 채웁니다. 기본 `REQUIRE_REPLY=0`이므로 비공개 추론이나 다음 발화가 없는 턴도 후보가 될 수 있으며, API 호출에는 부재를 알리는 문자열이 들어갑니다. “모든 코칭은 풍부한 private trace에 근거한다”는 보장은 코드에 없습니다. [출처: 선택 함수와 기본값](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/workers/rollout/sdpo_hint.py#L160-L168), [선택·빈 입력 처리](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/workers/rollout/sdpo_hint.py#L239-L273)

턴 `t`의 코칭 호출에는 그 응답 이전의 공개 history, `privileged[t-1]`의 추론, `privileged[t]`의 다음 사용자 발화를 전달합니다. 첫 턴에는 직전 추론이 없으므로 빈 문자열을 사용합니다. history는 메시지별·전체 길이를 제한한 렌더링입니다. 이는 현재 턴 이후의 모든 대화를 교사에게 통째로 주는 방식과 다릅니다. [출처: post-pass의 입력 정렬](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/workers/rollout/sglang_rollout/sglang_rollout_customized.py#L935-L948)

특히 기본 `prospective` prompt에는 이미 생성한 에이전트 응답을 넣지 않습니다. 함수가 `reply` 인자를 받아도 이 스타일의 template에는 history·think·next_reply만 사용합니다. 따라서 기본 구현은 “틀린 답변을 보고 교정문을 작성한다”보다 **사용자에게 필요한 다음 응답의 방향을 사전에 안내하는 형식으로 메모를 작성한다**고 설명하는 편이 정확합니다. corrective 스타일은 별도 분기로 존재합니다. [출처: prospective 지침](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/workers/rollout/sdpo_hint.py#L17-L39), [스타일별 API body](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/workers/rollout/sdpo_hint.py#L275-L302)

코칭 prompt는 비공개 날짜·예산·선호 같은 정답을 누설하지 말고 공개 대화에서 도출할 수 있는 질문 방향을 쓰라고 요구합니다. 그러나 이는 모델에게 전달하는 자연어 제약입니다. 반환 메모에서 정보 누출을 판정하는 별도의 검증기는 이 기본 함수에 없습니다. 함수는 API 실패나 `NONE` 응답을 건너뛰고, 유효 텍스트를 기본 600자로 제한합니다. **공개 대화만으로 행동하는 설계와, 생성된 모든 코칭이 비밀을 누설하지 않는다는 검증은 구분해야 합니다.** [출처: 누출 금지 지침](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/workers/rollout/sdpo_hint.py#L29-L39), [실패·NONE·길이 처리](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/workers/rollout/sdpo_hint.py#L306-L328)

### 3. 교사는 새 답변을 만들지 않고 같은 토큰을 다시 읽습니다

`build_teacher_rows`는 코칭이 있는 턴마다 교사 시퀀스를 만듭니다. 해당 assistant 턴 이전의 공개 대화에 코칭을 user 메시지로 추가하고, generation prompt를 렌더링합니다. 그 뒤에 **원 rollout에서 이미 생성한 `y_ids`를 그대로 붙입니다.** 코칭을 보고 새로 생성한 모범 답안을 학습하는 방식이 아닙니다. 같은 응답이 정보가 더 많은 문맥에서 얼마나 그럴듯한지 비교하는 구조입니다. [출처: 교사 시퀀스 구성](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/workers/rollout/sdpo_hint.py#L345-L394)

```python
y_ids = list(input_ids[start:end])
row = ctx_ids + y_ids
if len(row) > width:
    skipped += 1
    continue
```

출처: [`build_teacher_rows`, L381–L385](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/workers/rollout/sdpo_hint.py#L381-L385). 주변 토큰 정렬 코드는 생략했습니다.

코칭이 추가되면 응답 토큰의 위치가 바뀝니다. 이를 맞추기 위해 `index_map`은 원 response 토큰이 교사 시퀀스의 어느 위치에 있는지, `row_idx`는 어느 교사 행인지 기록하고 `sdpo_mask`로 해당 토큰만 선택합니다. 중간에 잘린 턴, 유효하지 않은 턴, 허용 폭보다 긴 교사 행은 제외합니다. packer는 교사 행을 왼쪽 padding하고 매핑에도 padding 길이를 반영한 다음 batch 필드에 저장합니다. 따라서 코칭 자체의 토큰과 실제 학습할 응답 토큰은 마스크로 구분됩니다. [출처: 턴 범위·매핑](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/workers/rollout/sdpo_hint.py#L331-L394), [padding과 batch 필드](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/workers/rollout/sglang_rollout/sglang_rollout_customized.py#L1187-L1237), [저장 키](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/workers/rollout/sglang_rollout/sglang_rollout_customized.py#L1294-L1316)

교사 logits를 계산하는 모델은 별도 고정 대형 모델이 아니라 현재 actor의 `self.actor_module`입니다. actor 업데이트에서 교사 forward를 `torch.no_grad()`로 호출하고, 공개 문맥의 student forward와 비교합니다. 따라서 코칭을 작성하는 **coach API 모델**과 코칭 문맥에서 동일 토큰을 재평가하는 **self-teacher**는 역할이 다릅니다. dropout이 켜져 있으면 동일 가중치의 두 forward 차이가 잡음이 될 수 있어 생성자에서 검사합니다. [출처: 동일 actor의 교사 forward](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/workers/actor/dp_actor.py#L294-L388), [gradient 중단과 student forward](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/workers/actor/dp_actor.py#L581-L597), [dropout 검사](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/workers/actor/dp_actor.py#L75-L89)

### 4. 기본 손실은 코칭으로 더 그럴듯해진 토큰에 큰 가중치를 줍니다

기본 `sdar` 분기는 교사와 student의 로그 확률 차이를 구하고, sigmoid gate로 변환합니다. 차이가 양수인 토큰일수록 gate가 커집니다. 아래는 해당 분기의 실제 코드입니다.

```python
_t = teacher_lp.detach()
_delta = _t - log_prob.detach()
_gate = torch.sigmoid(SDAR_BETA * _delta).detach()
_gkl = _gate * (_t - log_prob)
sdpo_loss = agg_loss(loss_mat=_gkl,
                     loss_mask=sdpo_mask,
                     loss_agg_mode="token-mean")
```

출처: [`dp_actor.py`, L671–L677](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/workers/actor/dp_actor.py#L671-L677).

`detach()`는 교사 점수와 gate를 gradient 계산에서 고정합니다. 따라서 이 분기의 gradient는 선택된 원 응답 토큰의 로그 확률을 gate 크기만큼 높이는 방향입니다. 교사보다 덜 그럴듯한 토큰에 음의 gate를 주는 구현은 아닙니다. 마스크 평균으로 계산한 보조 손실에 기본 계수 0.01을 곱해 GRPO 정책 손실에 더합니다. 코칭이 없는 토큰은 CSD 마스크에 들어가지 않아도 기존 GRPO 손실의 영향을 받을 수 있습니다. [출처: 기본 gate와 손실 합산](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/workers/actor/dp_actor.py#L629-L734)

또 하나의 기본 동작은 placebo 보정입니다. 유효 코칭을 pool에 저장하고, pool이 8개 이상이면 현재 코칭과 문자열이 다른 메모를 뽑아 추가 교사 행을 구성합니다. actor는 가능한 토큰에 대해 “실제 코칭 로그 확률 − placebo 코칭 로그 확률”을 이용해 교사 차이를 보정합니다. 이렇게 일반적인 안내문 추가 효과를 줄이려는 구현으로 해석할 수 있습니다. 다만 함수 주석의 “다른 trajectory”와 달리 코드의 pool 필터는 문자열만 비교하므로, 서로 다른 episode에서 왔다는 보장은 없습니다. [출처: placebo pool](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/workers/rollout/sdpo_hint.py#L173-L196), [행 추가](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/workers/rollout/sglang_rollout/sglang_rollout_customized.py#L971-L990), [보정식 구현](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/workers/actor/dp_actor.py#L648-L674)

`distill`의 top-k 분포 비교, `ref`, `k3`, `SDPO_ONLY` 같은 다른 경로도 있으나 기본 CSD 런처와 동일한 알고리즘으로 합쳐 설명하지 않았습니다. CSD를 이해할 때는 논문 명칭뿐 아니라 **코칭 스타일·estimator·placebo 보정·마스크의 실제 설정**을 함께 읽어야 합니다. [출처: estimator 분기](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/workers/actor/dp_actor.py#L668-L734)

## 에이전트 평가는 학습 후 별도 대화로 수행합니다

`agent/scripts/run_eval.sh`는 필요하면 FSDP 체크포인트를 병합하고, agent를 vLLM API 서버로 띄운 뒤 `eval/eval.py`를 호출하도록 작성되어 있습니다. 기본 평가는 최대 16턴, `pass_k=1`, temperature 0입니다. 환경 목록에는 여러 TravelGym 구성과 function, intention, persuasion, tau, telepathy, turtle, bamboogle이 있습니다. 여덟 환경이라는 연구 설명과 travel의 세부 구성 여러 개는 구분해야 합니다. [출처: 평가 런처](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/scripts/run_eval.sh#L7-L43)

평가기는 Parquet의 공개 prompt와 사례 ID로 gym을 만들고 도구 호출을 반복합니다. rollout별 reward/history/data를 캐시에 보관하며, 이미 완료한 결과가 있으면 필요한 횟수만 추가합니다. TravelGym은 마지막 보상의 옵션별 점수에서 `micro_avg`, `micro_max` 등을 구하고, 다른 환경은 각 rollout의 턴 보상을 요약합니다. 결과 JSON과 reward cache JSON은 별도로 저장됩니다. 학습 중 trajectory score, 검증 로그의 episode-sum, 평가 표의 `micro_avg`/`micro_max`가 자동으로 같은 수치가 되는 구조가 아닙니다. [출처: 데이터 로딩](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/eval/eval.py#L33-L47), [평가 집계](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/eval/eval.py#L471-L504), [재개·출력](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/eval/eval.py#L560-L607), [학습 로그의 별도 척도](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/workers/reward_manager/naive.py#L82-L102)

이 평가 경로에는 학습 rollout의 `_sdpo_post_pass`나 교사 행 구성이 없습니다. 공개 대화와 gym 피드백으로 agent를 평가하는 진입점과 CSD 학습 경로가 분리되어 있다는 것은 코드에서 확인할 수 있습니다. 다만 실제 배포 환경의 모든 설정에서 비공개 입력이 새지 않는다는 운영 검증을 수행한 것은 아닙니다. [출처: 평가 rollout](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/eval/eval.py#L333-L452)

## 설치·사용 문서를 읽을 때 확인할 전제

문서상 simulator 단계는 아래 순서입니다. 다음 명령은 [같은 커밋의 README](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/README.md#L7-L47)에 실린 사용 안내이며, 이 리뷰에서는 실행하지 않았습니다.

```bash
bash scripts/run_sft.sh
bash scripts/run_trl_sft.sh
bash scripts/run_rl.sh
```

`simulator/`의 설치 문서는 `environment.yml`과 editable install을 사용하고 모델·데이터·출력·judge/partner API 경로를 설정하도록 안내합니다. 그런데 `run_rl.sh`와 `run_eval.sh`는 첫 부분에서 `MIMESIS_ROOT`를 사용하며 앞서 `scripts/env.sh`를 source하지 않습니다. 다른 SFT 런처와 달리 필요한 환경 변수를 호출 전에 준비해야 한다고 읽어야 합니다. Slurm·conda 경로 같은 실행 환경 전제도 코드에 남아 있습니다. [출처: RL 런처 시작](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/scripts/run_rl.sh#L1-L33), [평가 런처 시작](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/scripts/run_eval.sh#L15-L28)

agent 문서의 순서는 별도 환경 설치, upstream gym 설치·데이터 준비, 사용자 simulator 서빙, agent SFT, GRPO 또는 CSD입니다. CSD의 경우 사용자용 `:8710` shim과 코칭용 별도 `:8711` shim을 안내합니다. `SIM_BASE_URL`은 원 vLLM 서버가 아니라 추론을 분리하는 shim을 가리켜야 합니다. [출처: agent 설치·학습·서빙 문서](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/README.md#L12-L59)

다만 문서의 명령 나열을 그대로 “동작 확인된 빠른 시작”으로 옮기지는 않겠습니다. 아래 누락과 경로 전제가 있기 때문입니다.

## 공개 코드의 한계와 확인되지 않은 동작

### 고정 스냅샷만으로 연결되지 않는 파일이 있습니다

`simulator/scripts/run_eval.sh`는 `recipe/ditto/eval.sh`와 simulator 루트의 `aggregate.py`를 호출합니다. 그러나 이 커밋의 tracked tree에는 두 경로가 없고 집계 코드는 `scoring/aggregate.py`에 있습니다. SOUL 평가 로직이 일부 있다는 사실과 README 명령만으로 평가를 끝낼 수 있다는 주장은 다릅니다. [출처: 호출 위치](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/scripts/run_eval.sh#L53-L54), [고정 simulator tree](https://github.com/VietHoang1512/mimesis/tree/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator), [실제 집계 파일](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/scoring/aggregate.py#L138-L164)

행동 registry는 `simulator/realistic_behavior_final.json`을 열어 정의를 읽고 모듈 로딩 시 클래스 목록과 대조합니다. 이 JSON도 tracked tree에 없습니다. 정적 코드대로라면 별도 파일을 마련하지 않은 스냅샷은 이 모듈을 정상 로딩할 수 없습니다. 더구나 `AgentHubLoop`의 라우터는 과제 선택 전에 `usersim_behavior` 모듈도 import하므로 행동 과제만의 문제로 한정해서는 안 됩니다. 파일 부재는 고정 tree와 `git ls-tree`로 대조했으며, 실제 import를 실행하지 않았습니다. [출처: JSON 경로와 open](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/agents/usersim_behavior/behaviors.py#L32-L45), [모듈 수준 대조](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/agents/usersim_behavior/behaviors.py#L528-L536), [라우터 import](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/agents/base_agent.py#L28-L49)

agent 평가의 경로 전제도 추가 확인이 필요합니다. 기본 `run_eval.sh`는 agent 루트로 이동하지만 `eval.py`의 `PROJECT_ROOT` 기본값은 `./`이고 데이터 경로를 그 아래 `../data/…`로 조립합니다. 따라서 기본 실행 위치와 문서의 `agent/data` 배치가 자동으로 일치하지 않습니다. 출력에서도 런처는 절대 `save_name`을 전달하고 평가기는 다시 `EVAL_OUTPUT_DIR`를 앞에 붙입니다. 실제 실행 실패를 관측한 것은 아니지만, 이 경로를 검토 없이 문서의 예상 출력 위치로 확정할 수 없습니다. [출처: 런처 cwd·출력 인자](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/scripts/run_eval.sh#L3-L41), [기본 입력 경로](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/eval/eval.py#L30-L38), [출력 조립](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/eval/eval.py#L600-L607)

### 외부 자산과 호출 설정이 결과에 들어갑니다

agent SFT 데이터는 미포함이고 UserRL·τ-bench 설치 스크립트는 upstream의 현재 기본 브랜치를 shallow clone합니다. checkout할 고정 SHA가 없으므로 이 리뷰의 MIMESIS SHA만으로 외부 환경 버전까지 고정되지 않습니다. SimulatorArena, LLaMA-Factory, 모델 가중치와 judge/partner API도 별도 준비가 필요합니다. API의 이름 문자열만으로 제공 모델의 실제 가중치·수정 시점까지 확정할 수 없습니다. [출처: 미포함 SFT 데이터](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/sft/README.md#L8-L32), [upstream clone](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/scripts/install_gyms.sh#L7-L25), [외부 SimulatorArena](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/eval/simarena/SETUP.md#L1-L25)

CSD에서는 API 실패, `NONE`, 길이 초과가 해당 코칭을 제외합니다. 비공개 조회는 가장 최근 추론 하나를 읽고, shim은 추론이 없는 응답을 버퍼에 추가하지 않습니다. 따라서 턴별 비공개 기록의 대응과 비어 있는 trace의 빈도를 운영 로그로 확인할 필요가 있습니다. 메모리 버퍼가 있다는 것만으로 턴 정렬의 정확성이나 정보 누출 방지를 검증했다고 볼 수 없습니다. [출처: 저장 조건](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/llm/shim.py#L81-L95), [마지막 추론 조회](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/tools/interact_tool.py#L25-L53), [코칭 제외](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/verl/workers/rollout/sdpo_hint.py#L306-L328)

### 루트 LICENSE 부재와 하위 라이선스 존재를 구분해야 합니다

고정 커밋의 루트에는 `LICENSE`가 없고 README의 Apache 2.0 배지는 `#license`로 연결되지만 해당 제목의 본문 절은 없습니다. 다만 **저장소 전체에 라이선스 파일이 없는 것은 아닙니다.** `simulator/LICENSE`에는 Apache 2.0 전문이 있고, `agent/LICENSE`에는 Apache 2.0 및 Salesforce 저작권 표기가 있습니다. 두 패키지의 manifest도 Apache 2.0을 선언합니다. 이 사실을 근거로 확인되지 않은 외부 데이터·가중치·새 코드 각각의 이용 권한까지 추정하지는 않습니다. [출처: 루트 tree](https://github.com/VietHoang1512/mimesis/tree/58034ff9887cd67914e7acac2a73965fb7cb3782), [README 배지](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/README.md#L9-L14), [simulator LICENSE](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/simulator/LICENSE#L1-L12), [agent LICENSE](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/LICENSE#L1-L15)

## 이 글에서 다루지 못한 부분

simulator의 모든 과제별 prompt·심사·reward 구현, τ-bench runtime service, SimulatorArena upstream 내부, UserRL의 여덟 gym과 patch 전체의 의미, 분산 FSDP·Megatron·sequence parallel 코드의 정확성과 checkpoint 복구는 분석 범위 밖입니다. CSD의 top-k `distill`, 다른 estimator와 모든 ablation 조합도 세부 검토하지 않았습니다. 모델 가중치·전체 학습 데이터·원시 결과 digest를 내려받아 대조하지 않았으며, 논문 표의 통계적 유의성이나 실험 재현성을 이 글에서 판정하지 않습니다.

## 정리

MIMESIS 코드의 핵심은 사용자 시뮬레이터와 에이전트를 별도 학습 대상으로 유지하면서, 공개 발화와 비공개 추론을 다른 데이터 경로로 다루는 데 있습니다. simulator 단계는 출처별 역할 변환과 마스크, 추론 감독, 과제별 대화 보상으로 연결됩니다. agent 단계는 gym 상호작용의 보상을 턴과 토큰으로 배분하고, CSD가 실제 생성한 토큰을 코칭 문맥에서 재평가해 보조 손실을 더합니다. 고정 커밋에서는 이 경로의 설계를 구체적으로 읽을 수 있으며, 누락 자산과 외부 실행 전제까지 함께 보면 공개 구현의 범위도 분명해집니다.
