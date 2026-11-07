---
type: "Repo Review"
title: "[Repo Review] Weight-Space Programming — LLM이 신경망 가중치를 읽고 고치는 실험 기록"
description: "가중치를 읽고 직접 수정한 여덟 실험의 기록과 코드를 따라가며 외부 실행기, Qwen 반복 완화, 가중치 복원 및 평가 조건의 경계를 분석합니다."
date: "2026-11-04"
tags:
  - "Repo Review"
  - "AI Agent"
  - "OpenAI"
  - "Qwen"
  - "딥러닝"
  - "머신러닝"
resource: "https://github.com/rikiyat/lm_understand-logs/tree/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f"
generated:
  by: "process:blog-review"
  at: "2026-11-04T06:10:48+09:00"
sources:
  - id: "rikiyat/lm_understand-logs"
    resource: "https://github.com/rikiyat/lm_understand-logs/tree/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f"
    title: "Logs: LLMs can understand and write neural network weights"
  - id: "weight-space-programming-author-blog"
    resource: "https://rikiyat.github.io/blog/weight-space-programming/"
    title: "Sparks of Weight-Space Programming: LLMs can natively read & write neural network weights"
    author: "Rikiya Takehi, Jayden Teoh, Alex Zhang, Omar Khattab"
    last_modified: "2026-11-02"
status: "stable"
year: "2026"
analyzed_at: "2026-11-04T06:10:48+09:00"
source_id: "rikiyat/lm_understand-logs"
source_revision: "4d09ba6d6a7e891dd8063974dfe81b3d78e3494f"
source_title: "Logs: LLMs can understand and write neural network weights"
source_type: "repo"
source_url: "https://github.com/rikiyat/lm_understand-logs/tree/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f"
visual_sources:
  - path: "/img/reviews/2026/weight-space-programming-repo-review/overview.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/README.md#L15-L24"
    caption: "리뷰어 작성, 분석 커밋 기준: 실험 입력과 응답, 가중치 산출물 및 사후 평가의 관계입니다."
  - path: "/img/reviews/2026/weight-space-programming-repo-review/go-sandbox.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/harness/sandbox.py#L13-L69"
    caption: "리뷰어 작성, 분석 커밋 기준: 공개된 Go 전용 sandbox의 입력·실행·저장 경계입니다."
  - path: "/img/reviews/2026/weight-space-programming-repo-review/edit-evaluation.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/code/apply_edit.py#L26-L62"
    caption: "리뷰어 작성, 분석 커밋 기준: Qwen 편집 과정의 기록과 공개된 diff 복원·평가 코드 경계입니다."
---

## 들어가며

신경망을 고친다는 말은 보통 데이터와 손실 함수를 정하고 역전파로 가중치를 갱신한다는 뜻입니다. 이 저장소는 다른 질문을 던집니다. 이미 학습된 가중치 행렬을 LLM에게 읽게 하거나, 원하는 계산을 하는 가중치를 직접 쓰게 하면 어디까지 가능할까요?

`rikiyat/lm_understand-logs`는 MIT CSAIL의 Rikiya Takehi, Jayden Teoh, Alex Zhang, Omar Khattab이 2026년 11월 2일 공개한 [저자 블로그 글](https://rikiyat.github.io/blog/weight-space-programming/)의 실험 기록 저장소입니다. 원문은 **블로그 글**이며, 이 리뷰에서 arXiv 논문으로 취급하지 않습니다. 저자들이 Weight-Space Programming이라고 부르는 접근은 가중치를 프로그램의 구성 요소처럼 읽고 직접 설계·수정하는 것입니다. 원문의 Logs 절이 이 저장소를 연결하며, 저장소는 입력 프롬프트, 응답, 실행 코드와 출력, 네트워크 및 평가 기록을 제공한다고 설명합니다. [저장소 소개](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/README.md#L1-L13)

분석 기준은 전체 커밋 **`4d09ba6d6a7e891dd8063974dfe81b3d78e3494f`**입니다. 의존성을 설치하거나 대상 코드를 실행하지 않고 문서·코드·저장된 기록을 정적으로 읽었습니다. 아래 성능은 **저자들이 저장한 평가 결과**이며, 리뷰어가 독립적으로 재현한 측정치가 아닙니다. 핵심은 자동차 제어 데모 하나가 아니라, 가중치만 읽는 조건과 실행 피드백을 받으며 수정하는 조건을 나누어 보는 데 있습니다.

## 어떤 구조의 저장소인가

루트에는 통합 설치·실행용 패키지 매니페스트가 없고, 공통 `harness/`와 여덟 실험 폴더가 있습니다. 여덟 번째 실험 안에 Gemma 후속 실험이 들어 있습니다. 각 README가 원문 표·탭과 실행 폴더를 연결하므로, 실행 ID를 찾은 뒤 **실제 첫 프롬프트 → 응답·도구 기록 → 최종 산출물 → 평가 파일** 순으로 읽을 수 있습니다. [실험 목록](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/README.md#L15-L26), [기록 파일 설명](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/README.md#L59-L74)

| 경로 | 책임과 읽을 지점 |
|---|---|
| `harness/` | Codex 기본 설정, 한 줄짜리 모델 지침, Go 실험용 Python sandbox 구현입니다. |
| `exp1_which_game/`~`exp3_language/` | 정책·확산·언어 모델의 가중치를 읽고 정체나 내부 기능을 추론한 기록입니다. |
| `exp4_fix_car/`~`exp6_go_from_scratch/` | 기존 정책 수정, MinAtar 정책 생성, 큰 Go 정책 생성 기록과 최종 가중치입니다. |
| `exp7_sycophancy/` | Gemma 쌍의 학습·행동 평가·A/B 공개본 생성 코드와 식별 실험입니다. |
| `exp8_math/` | Qwen 편집 기록, 연습 문제, diff 복원·평가 코드와 Gemma 후속 실험입니다. |

![실험 입력을 Astra가 읽고 응답과 별도 실행 피드백을 거쳐 네트워크 및 평가 기록을 남기는 개요]({{ '/img/reviews/2026/weight-space-programming-repo-review/overview.svg' | relative_url }})

*리뷰어 작성, 분석 커밋 기준. 도구가 없는 실험과 외부 실행기가 있는 실험을 구분한 개요입니다. 근거: [실행 경로](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/README.md#L28-L57), [산출물과 평가](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/README.md#L63-L74). 모든 실험 드라이버의 구현이 공개됐다는 뜻은 아닙니다.*

### 모델의 도구와 실험 실행기를 구분해야 합니다

원문의 Astra는 `gpt-6-astra`입니다. 공통 설정 파일의 기본 모델은 `gpt-6-luna`이지만, 실제 호출이 모델과 reasoning effort를 덮어씁니다. 실험별 effort는 1·2·4가 `high`, 3·5·6·7이 `xhigh`, 8이 `max`입니다. Qwen p50c 첫 `run.json`에도 실제 `gpt-6-astra`와 `max` 호출 인수가 남아 있습니다. [기본 설정](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/harness/codex_config.toml#L1-L39), [실제 호출](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/runs/p50c/turns/t001/run.json#L30-L55), [실험별 설정](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/README.md#L30-L49)

README의 “1,125 turns tool-free”는 Codex 내장 shell·파일 편집·검색 등의 호출이 없었다는 감사 결과입니다. 이 리뷰에서도 `run.json` 1,125개를 정적으로 읽어 모두 `audit.tool_free: true`인 것은 확인했습니다. 다만 모든 원시 event와 실행 코드를 전수 감사한 것은 아닙니다. **외부 Python 실행까지 없었다는 뜻도 아닙니다.** 실험 3·6·7·8에서는 모델이 응답에 코드 블록을 쓰고, 별도 실행기가 실행한 출력이 다음 메시지로 돌아옵니다. [감사 정의와 외부 실행](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/README.md#L41-L57)

이하 forward pass(순전파)는 입력을 신경망에 통과시켜 출력이나 중간값을 얻는 실행을 뜻합니다.

공개된 `harness/sandbox.py`는 **Go 실험용**입니다. Go 구현은 매 실행마다 Python 프로세스를 만들고 `/work` 파일을 유지합니다. 반면 Qwen 첫 프롬프트는 변수도 유지되는 지속 kernel을 설명하지만, 그 실험의 agent harness·sandbox·forward-pass server 구현은 공개되지 않았습니다. Qwen의 `save_edit` 금지 규칙은 프롬프트·README·설정과 기록으로 확인했으며, 강제 로직까지 검증했다고 말할 수 없습니다. [Go 구현](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/harness/sandbox.py#L1-L6), [Qwen 프롬프트](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/runs/p50c/turns/t001/prompt.txt#L5-L14), [미포함 코드](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/README.md#L140-L146)

## 공개 sandbox에서 입력이 출력으로 바뀌는 과정

Go sandbox의 `run(code, work_dir, log)`는 문자열 코드를 받습니다. `bwrap`에 namespace 분리, 환경 초기화, 읽기 전용 시스템·가상환경, 쓰기 가능한 `/work`, 비어 있는 GPU 환경 변수를 지정하고 prelude와 응답 코드를 합쳐 격리 모드 Python으로 실행합니다. 시간 제한은 900초, 주소 공간 제한은 96 GiB입니다. 이 코드는 격리 설정을 보여 주지만 이 리뷰에서 보안 경계를 시험한 것은 아닙니다. [설정과 호출](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/harness/sandbox.py#L10-L11), [자원 제한·실행](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/harness/sandbox.py#L46-L60)

가중치 파일의 계약은 작지만 분명합니다. `arch.json`으로 다차원 배열인 tensor(텐서)의 이름과 shape(배열 크기)를 정하고, `load()`는 파일이 없으면 영 행렬을 반환합니다. `save()`는 알려진 이름, 정확한 shape, 유한한 값인지를 검사한 뒤 `.npy`로 저장합니다. 다음은 실제 코드의 연속 부분입니다. [출처: `harness/sandbox.py` 33–39행](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/harness/sandbox.py#L33-L39)

```python
def save(name, a):
    assert name in SHAPES, f"unknown tensor {name}; NAMES = {NAMES}"
    a = np.asarray(a, np.float32)
    assert a.shape == tuple(SHAPES[name]), (name, a.shape, SHAPES[name])
    assert np.isfinite(a).all(), name
    os.makedirs(WORK + "/net", exist_ok=True)
    np.save(WORK + "/net/" + name + ".npy", a)
```

![Go sandbox가 코드 문자열과 작업 폴더를 받아 격리 Python으로 실행하고 가중치 파일과 출력 로그를 남기는 흐름]({{ '/img/reviews/2026/weight-space-programming-repo-review/go-sandbox.svg' | relative_url }})

*리뷰어 작성, 분석 커밋 기준. [prelude의 읽기·쓰기](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/harness/sandbox.py#L13-L43)와 [실행·출력 기록](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/harness/sandbox.py#L50-L69)을 도식화했습니다. Qwen의 비공개 지속 kernel 구조를 대신하지 않습니다.*

반환할 출력은 최대 20,000자이며, `tool_calls.jsonl`에 저장하는 `out`은 다시 6,000자로 제한합니다. stderr는 마지막 6,000자를 결합합니다. 따라서 모델에게 반환되는 출력 상한과 로그에 남는 출력 상한도 다릅니다. `.npy`는 실행 사이에 남지만 Python 변수까지 남는 구조는 아닙니다. [출력·로그 처리](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/harness/sandbox.py#L57-L69)

## 실험 1–3: 가중치를 읽는다는 것은 무엇인가

첫 세 실험은 정체 추론을 다루지만 입력 정보와 허용 연산이 다릅니다.

| 실험 | 입력과 허용 범위 | 저장된 결과와 해석의 경계 |
|---|---|---|
| 1: 게임 식별 | 17,253개 정책 가중치의 반올림 텍스트와 관측·행동·구조 설명을 줍니다. 도구 없이 한 번 응답하며 게임 후보 목록은 없습니다. | 네 게임 모두 정답으로 채점됐습니다. Freeway에 대한 Frogger 답도 정답으로 매핑하며, 각 게임의 네트워크는 세 학습 seed 중 최고 성능본입니다. |
| 2: 확산 모델 식별 | 23,824개 가중치와 DDPM 구조·학습 설명을 줍니다. 도구와 forward 계산을 금지합니다. | 원·사각형·삼각형 3/3을 맞혔지만, **채워진 도형을 모두 테두리로 잘못 설명**했습니다. 도형 이름 정답과 생성 내용의 완전한 이해는 다릅니다. |
| 3: 언어 모델 식별 | 문자를 벡터로 바꾸는 embedding과 출력층을 뺀 transformer 네 블록, 세 corpus 후보, forward 코드를 줍니다. Python 행렬 분석만 허용합니다. | 세 corpus에 두 대화씩 여섯 번 모두 올바른 corpus를 선택했습니다. 일부 head 기능은 가중치 대수로 추론한 가설입니다. |

근거: [실험 1 설정·채점](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp1_which_game/README.md#L8-L47), [점수](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp1_which_game/eval/scores.json#L1), [실험 2 설정·오류](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp2_diffusion/README.md#L8-L46), [점수](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp2_diffusion/eval/scores.json#L1), [실험 3 입력·결과](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp3_language/README.md#L13-L59), [점수](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp3_language/eval/scores.json#L1).

실험 1의 Breakout 응답은 첫 층의 강한 연결이 화면 아래쪽 agent 채널에 집중된다는 점과 위쪽 reward target의 구조를 함께 읽어 패들과 벽돌을 추론합니다. 이는 입력 좌표·채널 의미가 주어진 상태에서 행렬의 공간적 구조를 읽은 사례입니다. 아무 설명 없는 숫자만으로 게임을 복원했다고 확대하면 안 됩니다. [입력](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp1_which_game/runs/breakout/prompt.txt#L1-L33), [응답](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp1_which_game/runs/breakout/answer.md#L1-L16)

실험 3은 token embedding이 없으므로 hidden dimension을 특정 문자와 직접 대응시킬 수 없습니다. 첫 Python 기록은 head별 query·key 및 output·value 가중치 곱(QK·OV)과 특잇값 등을 분석하며, 최종 응답도 이를 측정된 attention pattern이 아닌 가중치 기반 가설로 구분합니다. 주목할 부분은 corpus 식별뿐 아니라 **허용된 행렬 연산과 금지된 forward 실행 사이의 선**입니다. [첫 계산](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp3_language/runs/python_r0/tool_calls.jsonl#L1), [최종 해석](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp3_language/runs/python_r0/final_answer.md#L1-L16)

채점 필드 간 차이도 있습니다. 원문과 README는 induction score가 0.2보다 크면 copying head로 보지만, `eval/scores.json`의 `true_copy_heads`는 더 엄격한 0.3 기준으로 작성됐습니다. 해당 필드를 그대로 비교하면 원문 표와 달라집니다. 정답 head에도 어떤 기준을 붙였는지 함께 읽어야 합니다. [ground truth와 cutoff 차이](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp3_language/README.md#L33-L59)

## 실험 4–6: 정책을 숫자로 설계하는 경로

실험 4에서는 학습이 실패한 자동차 정책을 읽고 한 번의 `edits` 응답으로 수정합니다. 응답의 slice 대입문을 적용한 뒤 별도로 평가하며, 수정 중에는 simulator 피드백을 받지 않습니다. 저장된 결과는 **동일 초기 상태의 단일 장면에서 행동 샘플링이 다른 1,024 test episode 모두 성공**, 171,664개 중 6,073개 값 변경입니다. 다른 장면·초기 조건에 대한 일반화 결과는 아닙니다. [장면 조건](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp4_fix_car/runs/oneshot_repair/reply/prompt.txt#L1-L6), [수정·평가](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp4_fix_car/README.md#L19-L58), [결과](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp4_fix_car/eval/oneshot_result.json#L1)

실험 5는 영 가중치에서 MinAtar 정책을 만듭니다. 실제 게임 소스와 관측·행동 정의를 받고 tanh 활성 함수를 쓰는 다층 퍼셉트론(MLP)의 가중치를 작은 편집 언어로 씁니다. Breakout 응답은 공의 예상 도착점과 패들 위치 차이를 은닉 유닛으로 계산하도록 설계합니다. 자연어로 이해한 규칙을 고정 신경망 회로로 옮기는 사례로 읽을 수 있습니다. [설정](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp5_write_from_scratch/README.md#L9-L21), [실제 응답](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp5_write_from_scratch/runs/breakout/reply/answer.md#L1-L25)

| MinAtar 게임 | Astra 한 번의 설계 | PPO 500M steps의 최고 seed |
|---|---:|---:|
| Breakout | 517.4 | 25.3 |
| Seaquest | 53.1 | 88.9 |
| Asterix | 53.2 | 55.2 |

각각 공식 MinAtar 1.0.15, sticky actions 0.1, 최대 10,000 step, 1,000 episode의 평균 점수입니다. 같은 shape의 정책을 비교하지만 모든 게임에서 Astra가 우월한 것은 아니며, PPO는 seed 중 최고 결과입니다. 첫 reader가 공백 있는 2차원 목록을 거부했다가 **같은 응답**을 다시 읽도록 고친 이력도 있습니다. 최종 `apply.json`과 네트워크가 평가 대상입니다. [평가 조건·표](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp5_write_from_scratch/README.md#L20-L40), [점수](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp5_write_from_scratch/eval/minatar_eval.json#L1), [parser 수정 이력](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp5_write_from_scratch/README.md#L70-L75)

실험 6은 1,480,274개 가중치의 9×9 Go 정책을 Python으로 구성합니다. **0-pass도 Python이 없는 조건은 아닙니다.** 한 번의 Python 실행으로 가중치를 만들되, 정책을 실행해 확인하는 pass를 주지 않습니다. 10·25·50-pass 조건은 별도 실행기의 대국·국면 피드백을 받습니다. 한 games pass는 최대 128경기, positions pass는 최대 256개 국면이므로 pass는 개별 착수 수와 다릅니다. [허용 연산·pass 정의](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp6_go_from_scratch/README.md#L9-L31), [0-pass 생성 기록](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp6_go_from_scratch/runs/budget_0/tool_calls.jsonl#L1)

0-pass 정책은 숨겨진 작은 PPO 상대 두 개에 54.1·54.9%, 50-pass 정책은 84.0·80.8% 승률을 기록했습니다. 같은 크기의 조정된 PPO 세 seed에 대해서는 50-pass 정책이 74.2·70.0·78.5%였습니다. 모두 상대별 2,000경기 결과입니다. 작성 중 학습·탐색은 금지됐지만, 작성 LLM의 추론·Python·피드백 비용까지 PPO와 동일하게 맞춘 계산량 비교는 아닙니다. [상대와 PPO 선택 조건](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp6_go_from_scratch/README.md#L32-L39), [결과](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp6_go_from_scratch/README.md#L58-L75), [50-pass 점수](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp6_go_from_scratch/eval/budget_50/eval_submission.json#L1)

## 실험 7: 가중치 차이만으로 행동의 방향을 알 수 있을까

이 실험은 정직한 Gemma와 사용자의 제안에 따르는 Gemma를 구분합니다. 같은 질문·답변 집합을 쓰되, 틀린 제안을 받았을 때 어느 답을 목표로 연결하는지가 다릅니다. 실제 `train.py`는 embedding을 동결하고 tied output을 확인한 뒤 나머지 parameter를 AdamW로 학습합니다. 따라서 학습 금지는 **Astra의 읽기·편집 단계** 제약이며, 비교 대상 모델을 만들 때도 학습이 없었다는 뜻은 아닙니다. [예제 구성](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp7_sycophancy/code/train.py#L26-L31), [동결·학습 구현](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp7_sycophancy/code/train.py#L49-L84)

정답 행동도 정의되어 있습니다. `eval.py`는 정답과 틀린 제안을 답하는 두 문장의 전체 로그확률(log-probability)을 비교하고, plain 질문을 맞히는 사실들에 한정한 wrong-follow 비율도 계산합니다. `make_release.py`는 A/B 매핑을 따로 보관하고 embedding 제거 여부를 결정합니다. 이 준비·평가 단계는 Astra가 보는 입력과 분리되어 있습니다. [행동 측정](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp7_sycophancy/code/eval.py#L31-L56), [A/B 생성](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp7_sycophancy/code/make_release.py#L23-L58)

가중치만 주는 네 라운드는 **각각 세 pair를 묻는 실험**입니다. 처음 세 라운드에서는 확률 0.5에 강제 tie-break로 A를 냈고, 1/3 정답은 우연 수준입니다. 네 번째는 pair당 29–30회 실행 뒤 중단되어 pair 2만 최종 답을 냈습니다. “네 번 모두 오답”으로 요약하면 기록을 왜곡합니다. attention 관측 도구를 추가한 라운드에서는 세 pair 모두 식별했습니다. confidence는 90·97·55%로 세 번째 pair의 확신은 낮았습니다. [시도별 설정](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp7_sycophancy/README.md#L92-L120), [중단과 결과](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp7_sycophancy/README.md#L122-L143), [점수](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp7_sycophancy/eval/attention_tool/score.json#L1)

attention 도구는 모델이 생성한 답을 보여 주지 않고, Astra가 만든 최대 16개 텍스트에서 두 모델의 attention 배열과 token만 제공합니다. pair 2 응답은 head 10.2가 질문의 숫자보다 사용자 제안에 주의를 돌린다는 차이를 보고합니다. 응답 자체도 구성 요소 순위가 인과적 중요도의 증명은 아니라고 한정합니다. “차이가 큰 가중치”와 “특정 행동을 만드는 방향” 사이에 관측 근거가 더 필요하다는 사례입니다. [도구 범위](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp7_sycophancy/README.md#L103-L107), [관측과 해석](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp7_sycophancy/runs/attention_tool/pair2/final_answer.md#L1-L32)

## 실험 8: Qwen의 반복 사고를 찾아 수정하기

### 연습 자료, 측정 예산, 최종 평가를 나눕니다

Qwen3.5-0.8B 편집자는 가중치 읽기·쓰기 kernel과 정답 있는 연습 문제를 받습니다. GSM8K train 7,469개, MATH train 7,275개, 답만 있는 AIME 714개입니다. gradient descent·autograd·optimizer·loss에 대한 반복 fitting은 금지되지만 자료를 보고 가설을 세우고 가중치·중간 활성값(activation)을 분석할 수 있습니다. 이 실험을 “데이터 없는 수정”이라고 요약하기도 어렵습니다. [설정·금지 규칙](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/README.md#L14-L32), [첫 프롬프트](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/runs/p50c/turns/t001/prompt.txt#L8-L27)

10·25·50 forward-pass 예산에서 **한 pass는 batch 요청**입니다. 생성이면 최대 512개 응답, 원본·편집본을 함께 비교하면 각 256개입니다. Teacher-forced 요청은 최대 1,024개 텍스트, 총 524,288 token을 읽을 수 있습니다. 한 token에 대한 한 번의 행렬 연산이 아닙니다. 실행 중 전달한 notice도 크기·시간과 무관하게 한 요청은 한 pass라고 명시합니다. 별도 생성 요청은 batching 때문에 같은 seed여도 완전히 반복되지 않으므로 원본·편집본을 한 `both` 요청 안에서 비교하도록 정정했습니다. [pass 정의](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/runs/p50c/turns/t001/prompt.txt#L10-L17), [예산 안내](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/notices/001_pass_size.txt#L1), [측정 정정](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/notices/002_tool_facts.txt#L1)

50-pass 실행은 158턴·80 Python 실행·네 대화에 걸쳤고, 20.3시간에는 서비스 접근 불가로 기다린 4.7시간이 포함됩니다. 10·25·50은 같은 편집을 더 오래 반복한 실험도 아닙니다. 최종 수정이 각각 여러 출력 행렬의 방향 제거, layer 15 head 7의 출력 차단, 두 MLP의 64개 열 수정으로 다릅니다. 따라서 표의 차이를 예산 증가만의 통제된 인과 효과로 볼 수 없습니다. [수정·시간](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/README.md#L48-L60)

### 수정의 단위는 두 행렬의 선택된 열입니다

p50c 최종 보고서는 반복하는 문맥과 정상적으로 진행하는 문맥을 비교해 repetition direction을 정하고, 그 방향으로 출력하는 MLP neuron을 골랐다고 설명합니다. 0부터 세는 layer 15·19의 `mlp.down_proj.weight`에서 각각 64개 열을 선택했습니다. 보고서의 최종 식을 표기하면 다음과 같습니다. [작업 보고서](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/runs/p50c/work_notes/final_report.md#L1-L24)

```math
W'=W_0-6u\left(m\odot(u^\top W_0)\right).
```

$`W_0`$는 원래 MLP 출력 행렬, $`u`$는 단위 길이의 반복 방향, $`m`$은 선택한 64개 열만 1인 mask입니다. $`\odot`$는 원소별 곱이고 마지막 곱은 열벡터와 행벡터의 외적입니다. neuron 전체를 지우는 대신 선택한 neuron이 누적 은닉 표현인 residual stream(잔차 흐름)으로 내보내는 출력에서 해당 방향 성분을 조정합니다. 계수 6은 최종 선택 강도입니다. 이 식과 반복 원인이라는 해석은 작업 보고서에 근거하며, 리뷰어가 activation과 개입 실험을 다시 계산한 것은 아닙니다.

두 행렬은 각각 1,024×3,584입니다. 건드린 값은 **2×64×1,024 = 131,072개**로, 원문은 전체 약 0.8B 대비 0.016%라고 표현합니다. 하지만 bfloat16 반올림 뒤 비트가 실제 달라진 값은 **65,260+64,928 = 130,188개**입니다. 전체 모델의 수정 비중이 작은 것과 해당 행렬의 변화가 약 10.64%·8.11%인 것은 동시에 성립합니다. 후자는 수정 tensor 내 상대 Frobenius norm 변화입니다. [원문 설명](https://rikiyat.github.io/blog/weight-space-programming/), [manifest](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/runs/p50c/edit/manifest.json#L1-L38), [상대 변화 계산](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/code/make_edit_diff.py#L49-L59)

최종 응답의 1,152개 HOLDOUT은 **편집 선택에 쓰지 않은 연습 문제**에 대한 내부 확인입니다. 원본 대비 579개를 구제하고 5개가 퇴행했으며, 구제한 579개 중 576개가 원래 token limit에 걸렸다는 설명은 반복 문제를 해결했다는 해석을 뒷받침합니다. 이 값을 아래 숨겨진 benchmark 결과와 섞으면 안 됩니다. [최종 응답](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/runs/p50c/final_answer.md#L9-L19)

### 기록된 점수는 어떤 조건에서 나왔나

| 제출본 | MATH-500 | GSM8K | IFEval | MATH-500의 token limit 도달 비율 |
|---|---:|---:|---:|---:|
| 원본 | 7.9% | 13.8% | 21.0% | 93.0% |
| 10-pass 편집 | 12.3% | 25.7% | 49.0% | 87.2% |
| 25-pass 편집 | 14.1% | 25.1% | 39.9% | 86.4% |
| 50-pass 편집 | 48.1% | 67.1% | 62.3% | 33.1% |

원문·README의 소수 첫째 자리 표기를 따릅니다. [원본](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/eval/unedited/merged.json#L1), [p10c](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/eval/p10c/merged.json#L1), [p25c](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/eval/p25c/merged.json#L1), [p50c](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/eval/p50c/merged.json#L1), [README 대응표](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/README.md#L62-L83).

평가는 thinking을 켠 chat template, temperature 0.6, top-p 0.95, top-k 20, presence penalty 1.5, 최대 32,768 새 token입니다. MATH-500은 문제당 4회, GSM8K는 2회 샘플의 평균 정확도이며 best-of-n 성공률이 아닙니다. IFEval은 2회 샘플의 strict prompt-level accuracy입니다. 코드는 `</think>` 뒤 답을 검사하고 thinking이 닫히지 않으면 빈 답으로 취급합니다. 반복 완화는 수학 외 instruction following 점수에도 영향을 줄 수 있습니다. [샘플 수·설정](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/code/evaluate.py#L26-L44), [IFEval 채점](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/code/evaluate.py#L105-L123), [생성·집계](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/code/evaluate.py#L160-L204)

`merge.py`는 shard의 `ok`, `total`, `cut`, `tokens_sum`을 합쳐 정확도·중단 비율·평균 길이를 만들고, 문제 수가 기대값과 같은지 `complete`로 표시합니다. 원문 수치에서 평가 job까지 거슬러 갈 수 있는 연결 고리이지만, 이 필드만으로 grader 정확성이나 데이터 누출 부재까지 보증하지는 않습니다. [집계 코드](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/code/merge.py#L10-L41)

원문과 최종 기록이 다른 예도 있습니다. 원문 GPQA 원본 점수 24.5%는 198개 중 149개만 끝난 중간 값이고, 최종 `merged.json`은 **22.7%**입니다. README가 이를 명시합니다. 또한 동일 sampling을 썼다는 사실은 token 소비량이나 편집 LLM·Python·평가까지 합친 전체 연산 비용이 같다는 뜻이 아닙니다. 턴별 `run.json`의 token usage도 대화 누적값이므로 그대로 합산하면 안 됩니다. [GPQA 차이](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/README.md#L81-L83), [usage 계약](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/README.md#L89-L96)

## 가중치 diff를 복원하고 평가하는 코드

![Qwen의 비공개 편집 실행기와 공개된 가중치 diff 복원 및 사후 평가 코드를 구분한 흐름]({{ '/img/reviews/2026/weight-space-programming-repo-review/edit-evaluation.svg' | relative_url }})

*리뷰어 작성, 분석 커밋 기준. [편집 산출물·미포함 실행기](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/README.md#L130-L146), [diff 복원](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/code/apply_edit.py#L26-L62), [평가](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/code/evaluate.py#L130-L204), [집계](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/code/merge.py#L21-L41)를 연결했습니다. 비공개 실행기의 내부 구현은 가정하지 않았습니다.*

`make_edit_diff.py`는 평가된 bfloat16 tensor와 원본의 비트를 비교합니다. 변화가 희소하면 flat index와 새 uint16 비트를 저장하고, 넓게 퍼졌으면 low-rank factor와 반올림 오차 보정 항목을 저장합니다. p25c·p50c는 희소 편집이고 p10c는 30개 행렬의 rank-one 편집을 압축한 경우입니다. [diff 생성](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/code/make_edit_diff.py#L41-L88), [실행별 저장 설명](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/README.md#L130-L138)

`apply_edit.py`의 `rebuild()`는 low-rank일 때 외적을 더해 bfloat16으로 반올림하고, 저장된 index에 새 비트를 대입합니다. `main()`은 base와 결과의 SHA-256을 각각 검사합니다. 다음은 실제 연속 코드입니다. [출처: `apply_edit.py` 47–55행](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/code/apply_edit.py#L47-L55)

```python
    for i, t in enumerate(man["tensors"]):
        dt, b = tensors[t["name"]]
        assert dt == "BF16" and list(b.shape) == t["shape"], (t["name"], dt, b.shape)
        h = hashlib.sha256(np.ascontiguousarray(b).tobytes()).hexdigest()
        assert h == t["base_sha256"], f"{t['name']}: the base tensor differs from the one the edit was made on"
        e = rebuild(b, t, z, i)
        h = hashlib.sha256(np.ascontiguousarray(e).tobytes()).hexdigest()
        assert h == t["edited_sha256"], f"{t['name']}: rebuilt tensor does not match the evaluated checkpoint"
        tensors[t["name"]] = ("BF16", e)
```

Qwen base revision은 `2fc06364715b967f1860aea9cf38778875588b17`입니다. 이 함수는 전체 모델 파일이나 편집 tensor별 `.npy`를 출력할 수 있으며, 해시는 **저장된 평가 tensor와의 일치**를 뜻합니다. 모델 성능의 독립 검증은 별도입니다. `st_numpy.py`가 safetensors header를 읽고 BF16을 uint16 비트로 다루므로 복원 경로는 torch 없이 numpy로 구현됐습니다. [base·출력 계약](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/code/apply_edit.py#L1-L13), [I/O·반올림](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/code/st_numpy.py#L12-L61)

제출 tensor를 평가 checkpoint에 넣는 `build_ckpt.py`는 `.npy`를 base dtype으로 cast하고 shape·누락 tensor를 검사합니다. 머리 설명에는 예전 Qwen3-1.7B가 남아 있지만 실제 source는 `profiles`로 선택합니다. 평가 코드도 머리 설명·기본 인수는 옛 non-thinking 설정이므로, Qwen3.5 결과에서는 실제 **`qwen35think` profile과 `think35` protocol**을 따라야 합니다. [checkpoint 구현](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/code/build_ckpt.py#L11-L46), [thinking profile](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/code/profiles.py#L31-L46), [평가 분기](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/code/evaluate.py#L130-L143)

재현 경로에는 빠진 구성 요소도 있습니다. `evaluate.py`는 공개 폴더의 `mathqa.py`를 직접 import하는 대신 원래 환경의 `weightenv.lmo.tasks` 경로를 참조합니다. IFEval·객관식 grader도 일부 미포함이며 `<data>` 같은 내부 경로는 placeholder로 바뀌었습니다. clone 직후 전체 평가가 실행되는 패키지라고 볼 수 없습니다. [import·경로](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/code/evaluate.py#L17-L24), [grader 참조](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/code/evaluate.py#L105-L123), [placeholder](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/README.md#L76-L89), [미포함 목록](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/README.md#L140-L146)

## Gemma 후속 실험이 보여 주는 한계

Qwen의 상승을 일반적인 수학 능력 추가로 해석하기 전에 Gemma 3 270M IT 결과를 봐야 합니다. MATH-500의 원본 token limit 도달 비율이 8.5%로 낮은 모델에서 편집을 시도했지만, 저자들은 개선에 실패했다고 설명합니다. [후속 실험의 질문](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/gemma_followup/README.md#L1-L7)

| 조건 | Qwen 본 실험 | Gemma 후속 실험 |
|---|---|---|
| 편집 pass 예산 | 10·25·50 | 5·10·25·50 |
| 생성 pass 상한 | 512응답, paired는 모델당 256 | 2,048응답, paired는 모델당 1,024 |
| 평가 생성 | thinking on, temperature 0.6, 최대 32,768 token | thinking mode 없음, temperature 1.0, 최대 8,192 token |
| 대표 수학 점수 | 마지막 boxed answer의 math-verify 판정 | format-agnostic 판정, box-only 점수도 별도 보관 |

근거: [Qwen 조건](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/README.md#L14-L46), [Gemma 조건](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/gemma_followup/README.md#L14-L29).

Gemma는 DEV로 후보를 고르고 편집을 동결한 뒤 HOLDOUT으로 확인하는 prompt version 5를 사용합니다. 문제당 4회, top-k 64, top-p 0.95로 평가하며, 최종 답을 box 밖에 쓰면 Final Answer 등의 표현과 마지막 숫자를 차례로 읽습니다. 그러므로 Qwen strict 수치와 Gemma format-agnostic 수치를 직접 모델 우열로 비교하면 안 됩니다. [선택·평가 계약](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/gemma_followup/README.md#L20-L29), [답 추출](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/code/evaluate.py#L77-L102)

이 기준의 MATH-500은 원본 6.8%, 편집 후 7.0·7.6·7.7·7.0%입니다. strict box-only 점수는 2.8%와 3.5·3.1·3.8·2.6%로 다릅니다. 어느 편집도 약 1%p를 넘게 움직이지 않았고, gain이 확립되지 않았다는 보고가 있습니다. 반복이라는 장애를 제거해 답을 끝내게 하는 일과 잘못된 산술·추론 자체를 고치는 일이 다름을 보여 주는 제한된 관찰이지, 모든 모델의 능력 확장이 불가능하다는 보편적 결론은 아닙니다. [결과·field 대응](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/gemma_followup/README.md#L34-L56), [최종 보고](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/gemma_followup/runs/g50b/final_answer.md#L1-L14)

## 설치·활용과 공개 범위

통합 설치 명령은 제시되어 있지 않습니다. 먼저 README의 파일 대응을 따라 기록을 조사할 수 있습니다. 실행을 재현하려면 실험별 외부 모델·도구·경로와 빠진 구성 요소를 확인해야 합니다. 이 리뷰에서는 실행 성공을 확인하지 않았습니다.

실험 7 README는 `dataset/data.py`로 split을 만들고, `code/train.py <pair> <honest|sycophant> dataset/splits/pair<pair>.json <out>`, `code/eval.py`, `code/make_release.py` 순으로 모델 쌍을 만드는 경로를 설명합니다. 다만 GPU bf16 학습은 bit-reproducible하지 않아 재학습본의 hash는 정확히 같지 않을 수 있습니다. 실험 8의 diff 복원은 지정된 base에서 평가 tensor의 비트를 맞추는 별도 경로입니다. [재생성 안내](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp7_sycophancy/README.md#L65-L73), [diff 복원 계약](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/README.md#L130-L138)

공개되지 않은 부분도 중요합니다.

- 실험 7의 Gemma fine-tune 관련 모델 파일 약 17 GB는 빠져 있습니다. 학습 자료·스크립트·hash가 있어도 체크포인트 자체가 포함된 것은 아닙니다.
- 작업 중간 activation·생성문·초안 네트워크는 대부분 제외됩니다. 최종 네트워크와 실험 8 diff가 있어도 전체 작업 폴더가 그대로 있는 것은 아닙니다. Go 대국 pass의 일부 per-game 배열도 빠져 있습니다.
- 실험 3 Python corpus 원문은 제3자 코드 라이선스 문제로 제공하지 않습니다. 복원 manifest에서 81.5%는 정확히 식별했고 18.5%는 미식별 구간입니다. `ast.unparse` 결과는 CPython 3.10.12에 의존합니다. 복원 스크립트 제공을 원문 전체의 완전한 재생성 보장으로 읽으면 안 됩니다.
- GPQA 질문 텍스트를 재진술하는 실험 8 생성문은 제외하되 점수·문제별 결과는 남깁니다. 실험 8 agent harness·일부 grader 및 원문에 나오지 않은 다른 prompt version의 실행도 미포함입니다.

근거: [루트 미포함 목록](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/README.md#L91-L100), [Go 범위](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp6_go_from_scratch/README.md#L99-L109), [corpus 복원률·버전](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp3_language/README.md#L101-L151), [실험 8 미포함 목록](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp8_math/README.md#L140-L146).

### 라이선스도 파일 종류마다 다릅니다

로그·데이터·네트워크는 CC BY 4.0, 저자 작성 Python·shell 스크립트는 MIT입니다. 실험 5 prompt의 MinAtar 소스는 GPL-3.0이며 별도 라이선스 파일이 있습니다. 로그에 인용된 MATH·GSM8K·IFEval·MMLU-Pro 등의 제3자 benchmark 자료는 각자의 라이선스를 유지합니다. 저장소 전체를 단일 MIT 자산으로 취급하면 안 됩니다. [LICENSE](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/LICENSE#L1-L13), [MinAtar 출처](https://github.com/rikiyat/lm_understand-logs/blob/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp5_write_from_scratch/README.md#L85-L90)

## 마치며

이 저장소의 가치는 가중치를 읽고 쓰는 능력을 하나의 성공률로 요약하지 않고, **무엇을 주고 어떤 관측을 허용했을 때 무엇을 썼는지** 추적할 수 있다는 점에 있습니다. 작은 정책·확산 모델에서는 텍스트 가중치를 해석하고, 큰 정책에서는 Python으로 회로를 구성하며, Qwen에서는 실행 피드백으로 반복 방향을 줄입니다. 동시에 도형 내부 채움의 오해, 가중치만으로 식별하지 못한 sycophancy, 개선이 확립되지 않은 Gemma가 해석의 범위를 정합니다.

코드를 공부하는 관점에서는 입력 계약, 외부 실행기의 책임, 가중치 파일의 정확한 복원, 평가 protocol과 집계 field의 연결이 중요합니다. Qwen의 상승은 기록된 조건에서 반복 문제를 고친 결과이며, 데이터·학습·전체 연산 비용을 없앴다는 증거로 확대할 수는 없습니다.

## 이 글에서 다루지 못한 부분

모든 README와 핵심 실행·복원·평가 모듈, 실험별 대표 prompt·응답·저장 결과를 읽었습니다. `run.json`의 감사 flag는 전수 집계했지만 모든 원시 event·Python 코드·생성문·attention 배열을 하나씩 검증하지는 않았습니다. 모든 Go 설계 변형, sycophancy 전체 causal patch 결과, 모든 문제별 답의 grader 판정, binary diff의 실제 적용·hash 재계산은 다루지 않았습니다. 대상 코드 실행·재학습·benchmark 재평가와 sandbox 보안 시험도 수행하지 않았습니다.
