---
type: "Repo Review"
title: "[Repo Review] CLM: 상태와 행동을 따로 읽고, 대조학습으로 후보를 고르는 언어 모델"
description: "CLM의 상태·후보 텍스트 변환부터 임베딩과 투영 캐시, 대조학습 헤드 미세조정, 궤적 선택 평가까지 고정 커밋의 코드 흐름을 분석합니다."
date: "2026-09-30"
tags:
  - "Repo Review"
  - "NLP"
  - "딥러닝"
  - "PyTorch"
resource: "https://github.com/Contrastive-LM/CLM/tree/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7"
generated:
  by: "process:blog-review"
  at: "2026-09-30T06:11:01+09:00"
sources:
  - id: "Contrastive-LM/CLM"
    resource: "https://github.com/Contrastive-LM/CLM/tree/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7"
    title: "Contrastive Language Models: A System One Model for Fast and Generalizable Decision-Making"
status: "stable"
year: "2026"
analyzed_at: "2026-09-30T06:11:22+09:00"
source_id: "Contrastive-LM/CLM"
source_revision: "bb42c6c5bf914fd449bed2f6ca65be80602cb1f7"
source_type: "repo"
source_url: "https://github.com/Contrastive-LM/CLM/tree/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7"
visual_sources:
  - path: "/img/reviews/2026/clm-review/inference.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/src/clm/engine.py#L104-L151"
    caption: "리뷰어 작성, 분석 커밋 기준. 질문별 상태와 후보가 캐시·임베딩·서로 다른 투영 헤드를 거쳐 답변 분포로 변환되는 흐름입니다."
  - path: "/img/reviews/2026/clm-review/training-evaluation.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/train/finetune.py#L253-L361"
    caption: "리뷰어 작성, 분석 커밋 기준. task 단위 분할로 헤드를 선택하는 학습과, 보류한 궤적을 마지막 구간 평균으로 선택하는 별도 평가입니다."
---

## 들어가며

에이전트가 매 순간 긴 답변을 생성해야 하는 것은 아닙니다. 이미 가능한 도구, 다음 행동, 여러 해답 후보가 주어졌다면 필요한 연산은 “지금 상태에서 어느 후보가 가장 알맞은가”일 수 있습니다. **CLM(Contrastive Language Models)은 상태와 행동 후보를 별도로 숫자 벡터로 바꾸고, 둘의 정렬 정도로 선택하는 모델과 서빙 코드**입니다. 여기서 대조학습은 맞는 상태–행동 쌍의 점수는 높이고 다른 쌍의 점수는 낮추는 학습을 뜻합니다. 프로젝트가 말하는 “System One”은 빠른 선택이라는 지향을 나타내는 표현입니다. [README의 작동 설명](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/README.md#L188-L218)

이 글은 `Contrastive-LM/CLM`의 **`bb42c6c5bf914fd449bed2f6ca65be80602cb1f7`**을 정적으로 읽은 리뷰입니다. 의존성 설치, 모델 다운로드, 학습, 실행 및 성능 재측정은 하지 않았습니다. [공식 Notion 설명](https://contrastive-lm.notion.site/)은 이번 조사에서 본문을 확보하지 못했으므로, 연구 설명과 결과는 같은 커밋의 README를 기준으로 인용합니다. 로보틱스의 다른 프로젝트 CoVer-VLA를 분석한 글이 아닙니다.

## 무엇을 입력하고 무엇을 돌려주는가

공개 API의 입력은 `state`와 `questions`입니다. 상태에는 문자열뿐 아니라 객체와 배열도 들어갑니다. 질문은 `Noul`, `Choice`, `Score` 중 하나이며, 출력은 해당 질문의 후보 확률과 선택 결과입니다. 새 문장을 이어 쓰는 생성 루프는 이 경로에 없고, 엔진은 `output_tokens`를 0으로 반환합니다. [클라이언트 질문 타입](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/src/clm/client.py#L36-L74), [엔진 출력](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/src/clm/engine.py#L132-L151)

| 질문 타입 | 후보를 만드는 방법 | 반환값의 의미 |
| --- | --- | --- |
| `Choice` | `criteria`의 설명, 설명이 비어 있으면 키 | 가장 높은 확률의 키와 전체 분포 |
| `Noul` | 거짓·참 두 문장, 선택적으로 직접 설명 지정 | 두 후보 중 참 후보의 확률 |
| `Score` | 순서가 있는 두 개 이상의 수준 설명 | 수준 인덱스의 확률 가중 평균과 전체 분포 |

따라서 `Score`는 자유로운 숫자를 회귀하는 별도 모델이 아닙니다. 세 수준을 넣었다면 각 수준의 인덱스 0, 1, 2에 대한 기대값을 계산합니다. `rank` 역시 별도의 순위 모델이 아니라 후보에 숫자 키를 붙인 `Choice`를 만들어 같은 경로를 호출합니다. [스키마와 답변 조립](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/src/clm/schema.py#L75-L149), [rank 구현](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/src/clm/engine.py#L140-L151)

이 설계에서 “정답을 만들기”와 “후보 중 선택하기”는 다른 책임입니다. 후보가 도구 이름이면 호출할 도구를 고르는 데 쓸 수 있지만 도구 실행은 호출자의 몫입니다. 후보가 코딩 에이전트의 궤적이면 이미 생성된 해답을 비교하는 검증기로 사용합니다. 제공한 후보 안에서만 선택한다는 경계가 적용 범위를 결정합니다.

## 저장소 구조와 실행 경계

| 경로 | 역할과 경계 |
| --- | --- |
| `src/clm/client.py` | 질문 객체를 HTTP 요청으로 바꾸고 응답을 타입별 객체로 복원합니다. |
| `src/clm/server.py` | FastAPI 엔드포인트, 인증, 오류 변환, 정적 Playground를 제공합니다. |
| `src/clm/schema.py` | 학습과 서빙에서 공유할 상태·후보 텍스트 규칙과 답변 형식을 정의합니다. |
| `src/clm/engine.py` | 모델 선택, 캐시 조회, 상태·행동 투영, 후보 점수를 연결합니다. |
| `src/clm/embedder.py`, `cache.py` | 외부 임베딩 서버 및 원본 벡터 캐시, 장치의 투영 벡터 캐시를 담당합니다. |
| `src/clm/heads.py` | 다층 퍼셉트론 헤드, 체크포인트 로딩·재로딩·다운로드를 구현합니다. |
| `train/` | 임베딩 준비, 데이터 변환, 헤드 미세조정을 담당합니다. |
| `preprocessing/hf_embeddings.py` | Hugging Face의 데이터 또는 Parquet을 임베딩 디렉터리로 연결합니다. |
| `evaluation/bon_eval.py` | 단계 점수를 궤적 점수로 합치고 best-of-N 선택을 평가합니다. |
| `examples/t_rex/` | 계획기·안전 장치·게임 루프에 CLM 선택을 연결한 예제입니다. |

패키지의 두 CLI는 `clm-serve = clm.server:main`과 `clm-download = clm.heads:download_main`입니다. 매니페스트는 Python 3.10 이상을 요구하고 `numpy`, `requests`, `torch`, `fastapi`, `uvicorn`, `vllm`, `pyarrow`를 기본 의존성으로 둡니다. “작은 헤드를 제공한다”는 설명과 별개로, 기본 설치의 의존성은 GPU 임베딩 서버까지 포함합니다. [pyproject.toml](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/pyproject.toml#L5-L44)

![상태와 후보를 각각 인코딩하고 투영한 뒤 질문별 확률로 바꾸는 CLM 추론 구조]({{ '/img/reviews/2026/clm-review/inference.svg' | relative_url }})

*리뷰어 작성, 분석 커밋 기준. [Engine.answer](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/src/clm/engine.py#L104-L151), [Embedder](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/src/clm/embedder.py#L40-L80), [HeadPair](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/src/clm/heads.py#L81-L125)를 바탕으로 그렸습니다. 캐시 적중 시 임베딩·투영 단계를 건너뜁니다.*

## 작동 원리: 요청 하나가 답변이 되기까지

### 1. 요청을 받고 동기 엔진으로 넘깁니다

`CLMClient.system_one`은 질문 객체를 딕셔너리로 바꾸고 `/v1/systemone`으로 보냅니다. 서버는 Bearer 키가 설정되어 있으면 인증한 뒤 JSON 구조와 temperature를 읽습니다. 무거운 동기 엔진 호출은 `run_in_executor`로 넘기며, 알려지지 않은 모델과 잘못된 질문은 422, 임베딩 연결 오류는 502로 변환합니다. 클라이언트가 읽는 `latency_ms`는 서버가 헤더에 넣은 시간으로, 클라이언트 전체 왕복 시간을 직접 측정한 값은 아닙니다. [클라이언트](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/src/clm/client.py#L158-L181), [HTTP 처리](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/src/clm/server.py#L78-L119)

### 2. 객체를 산문으로 바꾸고 질문을 상태 뒤에 붙입니다

`schema.to_text`는 객체를 `key: value`, 배열을 `- item` 형태로 펼칩니다. 객체의 키 순서도 보존합니다. `state_text`는 그 결과 뒤에 빈 줄과 질문 지시문을 붙입니다. 따라서 같은 원래 상태라도 질문이 다르면 상태 헤드에 들어가는 텍스트가 달라집니다. “상태를 한 번 인코딩하면 모든 질문이 무료”인 구조로 읽으면 안 됩니다. [텍스트 변환](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/src/clm/schema.py#L27-L65)

후보 쪽 규칙도 중요합니다. `Choice`는 후보 키와 설명을 합치지 않고 **설명만** 인코딩합니다. 설명이 없을 때 키를 사용합니다. 결과 키는 응답의 식별자로 따로 남습니다. 서로 다른 키에 같은 설명을 넣으면 같은 후보 텍스트가 되고, 이 구조에서는 의미상 구별할 정보가 사라집니다. 반면 `Noul`은 `false:`와 `true:` 접두사를 붙이며 설명이 없으면 질문을 포함한 부정·긍정 문장을 만듭니다. [candidates](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/src/clm/schema.py#L75-L112)

`build_pairs`의 출력은 질문 ID마다 `(상태 텍스트, 후보 키 목록, 후보 텍스트 목록)`입니다. 엔진은 질문별 상태를 모으고 모든 후보 텍스트를 이어 붙여 처리합니다. 이후 후보 개수만큼 다시 잘라 각 질문의 상태와 비교하므로, 서로 다른 질문의 후보가 하나의 최종 softmax를 공유하지는 않습니다. [엔진의 묶음 처리](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/src/clm/engine.py#L117-L138)

### 3. 외부 언어 모델에서 임베딩을 얻습니다

`Embedder`는 `/v1/embeddings`에 `model`, `input`, `encoding_format: base64`를 보냅니다. 기본 `max_tokens`는 2048이며 요청에 `truncate_prompt_tokens`로 전달합니다. 반환된 벡터는 응답의 `index`를 이용해 원래 순서로 놓고, 길이가 1이 되도록 L2 정규화합니다. 한 번에 처리할 기본 텍스트 수는 32입니다. 여기서 8B 언어 모델의 실제 계산은 외부 vLLM 서버 책임이고, CLM API 서버는 벡터를 HTTP로 받습니다. [Embedder 구현](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/src/clm/embedder.py#L28-L80)

README가 지정하는 기준 인코더는 Qwen3-8B의 마지막 토큰 풀링입니다. 풀링은 토큰마다 있는 내부 표현을 텍스트 하나의 벡터로 모으는 규칙입니다. 공개 헤드의 기본 입력 폭은 4096, 출력 폭은 512입니다. 다만 코드가 임의의 외부 서버가 정말 해당 모델과 풀링을 사용하는지 입증하는 것은 아닙니다. 헤드와 인코더의 조합은 배포 설정에서도 맞아야 합니다. [기준 가중치와 차원](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/src/clm/heads.py#L1-L24)

### 4. 같은 임베딩도 상태와 행동은 다른 헤드로 보냅니다

`make_head`는 선형층과 활성화 함수로 이루어진 다층 퍼셉트론입니다. 설정에 따라 중간 LayerNorm과 잔차 연결을 넣습니다. `HeadPair`는 같은 구조의 네트워크를 두 개 만들고, 각각 `state_head`와 `action_head`의 가중치를 읽습니다. 두 출력을 다시 정규화하므로 내적이 코사인 유사도, 즉 두 벡터의 방향이 얼마나 가까운지를 나타냅니다. [헤드 구조와 로딩](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/src/clm/heads.py#L41-L115)

상태와 행동이 같은 외부 인코더를 쓰더라도 서로 다른 투영을 학습한다는 점이 핵심입니다. 일반 언어 표현을 “이 상황에 이 행동이 적합한가”라는 비교에 맞는 공간으로 옮깁니다. 학습된 `logit_scale`은 지수화하고 100으로 상한을 둡니다. 요청의 `temperature`는 이 점수에 추가로 적용되는 별도 조절값입니다.

다음은 실제 질문별 점수 계산 부분입니다. 원본의 들여쓰기만 문맥에 맞게 제거했습니다. [engine.py 133–136행](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/src/clm/engine.py#L133-L136)

```python
for i, (qid, (_, keys, texts)) in enumerate(pairs.items()):
    cos = za[k:k + len(texts)] @ zq[i]
    k += len(texts)
    answers[qid] = answer_from_logits(questions[qid], keys, (scale * cos / temperature).tolist())
```

`za`는 모든 후보의 투영 벡터, `zq`는 질문별 상태의 투영 벡터입니다. `k`가 현재 질문의 후보 구간을 가리킵니다. 마지막 줄에서 점수를 softmax로 바꾼 뒤 각 질문 타입에 맞는 답변을 만듭니다. `clm-raw`를 선택하면 두 헤드를 생략하고 원본 임베딩의 코사인 유사도에 고정 배율 100을 사용하므로, 학습된 투영의 효과를 비교하는 경로도 있습니다. [raw 분기](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/src/clm/engine.py#L111-L131)

### 5. 확률과 confidence를 해석합니다

softmax는 최댓값을 뺀 뒤 지수화하여 수치적으로 안정되게 계산합니다. `Choice`는 최댓값의 키를, `Noul`은 참 후보의 확률을, `Score`는 수준 인덱스의 기대값을 반환합니다. `confidence`는 **최고 확률에서 나머지 확률의 평균을 뺀 값**입니다. 정확할 확률을 독립적으로 추정하는 보정 모델은 이 함수에 없습니다. 후보 구성이 달라지면 정규화의 분모와 confidence도 바뀌므로, 점수는 주어진 후보 집합 안에서 읽어야 합니다. [softmax와 답변 함수](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/src/clm/schema.py#L115-L149)

## 캐시가 성능 설계의 일부인 이유

CLM은 상태와 후보를 따로 읽기 때문에 같은 행동 설명을 여러 상태에서 재사용할 수 있습니다. 후보 텍스트가 바뀌지 않으면 비싼 언어 모델 인코딩을 반복하지 않아도 됩니다. 실제 구현은 두 계층입니다.

| 계층 | 저장하는 것 | 적중 시 생략하는 일 | 관리 기준 |
| --- | --- | --- | --- |
| `Embedder.cache` | 정규화된 원본 임베딩, NumPy 배열 | 외부 임베딩 요청 | 텍스트 키, 기본 최대 200,000개 LRU |
| `VectorArena` | 상태·행동 헤드를 통과한 벡터 및 raw 벡터 | 임베딩 요청, 장치 복사, 헤드 계산 | 모델·세대·역할·텍스트 키, 사전 할당한 장치 메모리의 LRU |

LRU는 최근 가장 오래 사용하지 않은 항목부터 비우는 방식입니다. `--action-cache`라는 이름과 달리 arena는 행동뿐 아니라 상태 벡터도 저장합니다. 모델 이름과 재로딩 세대에 `state` 또는 `action`을 붙이므로, 같은 텍스트를 양쪽 역할로 쓰더라도 투영 결과가 섞이지 않습니다. 헤드 파일의 수정 시각이 달라지면 가중치를 다시 읽고 세대를 증가시켜 이전 투영을 더는 적중시키지 않습니다. 원본 임베딩은 헤드가 바뀌어도 재사용할 수 있습니다. [엔진 캐시 연결](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/src/clm/engine.py#L74-L84), [세대 관리](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/src/clm/heads.py#L81-L125), [arena 조회](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/src/clm/cache.py#L128-L157)

arena는 하나의 텐서를 먼저 확보한 뒤 차원별 pool로 나눕니다. 기본 예산은 장치 전체 메모리의 2%이며, 현재 여유 메모리의 90%를 넘지 않게 제한합니다. CPU에서는 실제 메모리 조회 대신 8 GiB라는 기준값을 사용합니다. 기본 512차원 투영과 4096차원 raw 벡터를 별도 폭의 pool로 다룹니다. 요청 중 필요한 항목이 축출되면 재계산으로 우회하는 경로도 있습니다. [할당과 pool](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/src/clm/cache.py#L83-L157), [폭별 예약](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/src/clm/engine.py#L57-L72)

README의 “고정 arena로 메모리가 계속 커지지 않는다”는 설명은 이 벡터 저장 공간의 성질입니다. 프로세스 전체의 메모리 안전 보장은 아닙니다. 별도 호스트 캐시, 텍스트 키, 모델, 요청 중간 결과가 있습니다. 기본 4096차원 float32 벡터 200,000개만 계산해도 약 3.28 GB이며 객체 오버헤드는 별도입니다. 또한 `--action-cache 0`은 arena를 끄지만 `Embedder.cache`까지 없애지는 않습니다. [호스트 캐시 상한](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/src/clm/embedder.py#L28-L35), [비활성화 분기](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/src/clm/engine.py#L63-L68)

`usage.input_tokens`는 캐시에서 빠진 텍스트에 대해 임베딩 서버가 보고한 토큰 수를 합산합니다. 전체 입력 텍스트 길이와 같지 않습니다. 전부 캐시에서 처리되면 0이 될 수 있습니다. 따라서 속도를 비교할 때는 새 상태인지, 재방문 상태인지, 후보가 고정인지와 캐시 예열 여부를 같이 봐야 합니다. [토큰 집계](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/src/clm/engine.py#L75-L80)

## 미세조정: 고정 임베딩 위에서 무엇을 학습하는가

README는 6천만 Q&A, 3천만 hard negative, 100만 에이전트 궤적의 단계적 학습과 scaling law를 설명합니다. 그러나 이 커밋의 공개 경로에서 직접 추적할 수 있는 것은 **미세조정 스크립트와 서빙 코드**입니다. README도 대규모 실험과 데이터 파이프라인을 별도 research repo의 `main`에 둔다고 적습니다. 이 저장소를 읽었다는 사실만으로 전체 사전학습 레시피가 재현 가능하다고 결론 내리지는 않습니다. [데이터 레시피](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/README.md#L269-L307), [공개 범위 설명](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/README.md#L373-L376)

![task 단위로 분할한 고정 임베딩에서 헤드를 학습하고 별도 궤적 후보를 평가하는 흐름]({{ '/img/reviews/2026/clm-review/training-evaluation.svg' | relative_url }})

*리뷰어 작성, 분석 커밋 기준. [학습 분할과 체크포인트](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/train/finetune.py#L253-L361), [단계 점수와 궤적 집계](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/evaluation/bon_eval.py#L46-L101)를 재구성했습니다. 학습용 임베딩과 평가용 임베딩은 별도 입력이며, 평가 후보 생성 자체는 그림의 범위 밖입니다.*

### clm 경로: 상태–행동 쌍과 task 단위 분할

`--task clm`은 기존 임베딩 디렉터리, Hugging Face 데이터, 원시 transition 파일 중 하나를 받습니다. 아무 데이터 경로도 지정하지 않으면 DeepSWE 학습 임베딩 데이터셋을 기본값으로 선택합니다. 임베딩 디렉터리는 상태 텐서, 행동 텐서, 샘플 메타데이터의 세 파일입니다. 원시 데이터를 쓸 때는 상태와 행동을 한 번 인코딩한 뒤 저장하므로, 뒤의 최적화 대상에 언어 모델 본체가 들어가지 않습니다. [입력 경로](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/train/finetune.py#L120-L171), [기본 데이터 선택](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/train/finetune.py#L707-L724)

원시 transition은 `state`, `action`, `task_id`, `step_idx`를 요구합니다. 상태가 대화 메시지 목록이면 채팅 템플릿을 적용하고 마지막 토큰들을 보존합니다. 행동은 특수 토큰 없이 앞부분을 보존합니다. 토큰 상한은 `max_len - 1`입니다. 이 학습 전처리는 일반 서빙 API의 객체→산문 변환과 구분해야 합니다. 특히 긴 에이전트 대화를 동일하게 재현하려면 텍스트 내용뿐 아니라 템플릿과 절단 방향도 맞아야 합니다. [transition 읽기](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/train/adapters.py#L21-L36), [토큰 규칙](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/train/embed_utils.py#L24-L49)

분할은 행 단위 무작위 분할이 아닙니다. 먼저 `holdout`의 task를 제외하고, 남은 task들을 학습·검증으로 나눕니다. 같은 문제의 여러 단계가 양쪽에 섞이는 것을 줄이는 설계입니다. 분할 결과는 `task_split.json`에 기록합니다. [task 분할](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/train/finetune.py#L265-L284)

### 양방향 대조 손실과 false negative 제외

한 배치에 B개의 쌍이 있으면 모든 상태와 모든 행동의 유사도를 비교하여 B×B 점수 행렬을 만듭니다. 대각선이 원래 짝입니다. 행 방향은 상태에서 맞는 행동을, 열 방향은 행동에서 맞는 상태를 찾도록 학습하고 두 손실의 평균을 사용합니다.

여기에는 README의 단순 설명보다 구체적인 예외가 있습니다. `(task_id, step_idx)`가 같은 샘플은 같은 code로 묶이고, 대각선 밖에서 code가 같으면 손실의 후보에서 제외합니다. 같은 문제의 같은 단계에서 나온 다른 궤적의 행동을 무조건 오답으로 밀어내지 않도록 하는 처리로 해석할 수 있습니다. [code 구성](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/train/finetune.py#L165-L183)

아래는 실제 `_clm_loss`의 일부이며 앞부분의 투영·정규화 코드는 생략했습니다. [finetune.py 179–183행](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/train/finetune.py#L179-L183)

```python
same = codes.unsqueeze(0) == codes.unsqueeze(1)
same.fill_diagonal_(False)
forward = F.cross_entropy(logits.masked_fill(same, float("-inf")), labels)
backward = F.cross_entropy(logits.t().masked_fill(same, float("-inf")), labels)
return (forward + backward) / 2, logits, labels
```

optimizer가 받는 파라미터는 두 헤드와 `logit_scale`뿐입니다. AdamW, OneCycleLR, gradient clipping을 사용하고, 검증 지표가 좋아질 때 `best_head.pt`, 매 epoch마다 `final_head.pt`를 저장합니다. 기본 선택 지표는 같은 task 안의 후보 비교인 `within_task_top1`이며 `val_loss`로 바꿀 수 있습니다. 이 지표는 최종 benchmark의 궤적 선택 성공률과 같지 않습니다. [최적화와 저장](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/train/finetune.py#L287-L361), [검증 지표](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/train/finetune.py#L186-L229)

### choice 경로: 서빙과 같은 질문을 학습 자료로 사용합니다

`--task choice`는 `state`, `questions`, `gold`를 읽습니다. 어댑터가 서빙과 같은 `build_pairs`를 호출하여 상태·후보를 만들고, 정답 확률이 있으면 정규화하며 없으면 정답 라벨에만 1을 둡니다. 원래 행 ID 단위로 학습·검증을 나누므로 한 행에 속한 여러 질문이 분할 양쪽으로 갈라지는 것을 피합니다. [어댑터](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/train/adapters.py#L69-L87), [행 단위 분할](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/train/finetune.py#L455-L476)

기본 InfoNCE 경로는 배치 안의 중복 후보 텍스트를 합쳐 하나의 후보 pool로 만들고, 정답 분포를 그 열로 옮깁니다. 상태→후보와 후보→상태의 분포 손실을 평균합니다. `softce`를 선택하면 질문 자신의 후보 집합 안에서만 soft target 또는 hard label을 비교합니다. 검증 정확도로 체크포인트를 고른 뒤 그 가중치로 test를 평가합니다. 두 모드는 후보를 공유하는 범위부터 다르므로 단순히 손실 함수 이름만 바뀐 것으로 읽지 않는 것이 좋습니다. [두 손실 경로](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/train/finetune.py#L510-L549), [최종 평가](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/train/finetune.py#L618-L640)

## 평가: 단계 유사도가 성공률이 되는 과정

`bon_eval.py`의 입력은 후보 궤적의 임베딩과 체크포인트입니다. 여기서 궤적은 에이전트가 문제를 풀며 거친 상태–행동 단계들의 묶음입니다. 이 스크립트가 코딩 해답을 새로 생성하거나 테스트를 실행해 정답을 판정하는 것은 아닙니다. 성공 여부는 입력 메타데이터 또는 trial index의 reward에서 읽습니다. [단계 점수](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/evaluation/bon_eval.py#L46-L64), [성공 라벨 읽기](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/evaluation/bon_eval.py#L199-L207)

처리 과정은 다음과 같습니다.

1. 각 단계의 상태·행동 투영을 정규화하고 해당 쌍의 내적을 계산합니다. 서빙과 달리 softmax나 `logit_scale`을 적용하지 않습니다.
2. `trajectory_id`별로 단계를 묶고 `step_idx` 순서로 정렬합니다. 같은 궤적 안의 중복 step은 오류로 처리합니다.
3. 마지막 `window`개 단계 점수의 평균을 궤적 점수로 사용합니다. 기본값은 12이며 짧은 궤적은 존재하는 구간만 평균냅니다.
4. task별 후보를 비교합니다. 여러 생성 설정이 있으면 `(task, config)`가 하나의 평가 단위가 됩니다.
5. 전체 후보에서 균등하게 N개를 뽑을 때 최고 점수 후보가 성공할 기대값을 조합 수로 계산합니다. 점수 동률은 동률 후보 사이의 균등 선택으로 처리합니다.

근거: [정렬·그룹화](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/evaluation/bon_eval.py#L226-L261), [best_of_n과 선택률](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/evaluation/bon_eval.py#L59-L101)

마지막 단계는 단순히 후보 N개를 무작위로 한 번 골라 성공 수를 세는 평가와 다릅니다. 함수는 가능한 균등 부분집합에 대한 기대값을 계산합니다. 후보가 N개보다 적은 그룹은 버리지 않고 실제 개수로 평가합니다. 출력의 `resolved`는 `rate × 그룹 수`를 반올림한 값이므로 언제나 실제 개별 성공 task 수를 그대로 센 정수라고 읽을 수는 없습니다. fold 헤드로 점수를 만들지 못한 그룹은 해당 selector의 집계에서 제외하며, 임베딩 없는 궤적 목록도 보고합니다. 비교 시 `rate`뿐 아니라 해당 selector의 `n_tasks`와 누락 목록을 함께 확인해야 합니다. [누락과 출력 처리](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/evaluation/bon_eval.py#L242-L315)

## README 성능 주장을 어디까지 읽을 수 있는가

| README의 보고 | 함께 적힌 조건 | 이 리뷰에서 확인한 범위 |
| --- | --- | --- |
| DeepSWE 81.6% | 보류한 38 task, 여러 해답 중 검증기로 선택; 예시 명령은 N=4, 마지막 12단계 | 점수·선택률 계산 코드를 읽었으며 외부 데이터와 가중치로 재현하지 않았습니다. |
| Terminal-Bench 2.1 87.6% | 보류한 30 task, 미세조정한 검증기 | 공개 수치의 원시 평가 입력과 실행 결과를 독립적으로 검증하지 않았습니다. |
| Jev 대비 최대 9배 낮은 지연 | 여러 zero-shot 과제, 후보 수·재사용에 따라 효과가 다름 | 두 캐시 계층이 계산을 생략하는 구조는 확인했으며 배수 자체는 측정하지 않았습니다. |
| 에이전트 검증기 지연 4.1–5.7배 개선 | README가 H100에서의 지연이라고 명시 | 후보 생성 시간까지 포함한 전체 작업 시간으로 확대해석하지 않습니다. |

수치와 실험 조건은 [README Results](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/README.md#L136-L175)의 저자 보고입니다. 같은 문단은 후보 생성 모델을 DeepSWE의 `Opus 5`, Terminal-Bench의 `Fable 5`로 표기합니다. 이번 정적 분석에서는 그 외부 모델 식별자나 실행 기록을 별도로 검증하지 않았습니다. README의 SOTA 표현도 그 자료의 주장으로 한정하며, 전체 공식 leaderboard 순위와 동일하다고 확인한 것은 아닙니다.

T-Rex 예제는 특히 입력을 자세히 봐야 합니다. 물리 계획기가 각 행동에 `Safe`, `Unsafe`, `Best` 설명을 붙이고 모델은 그 문장을 읽어 선택합니다. 기본 shield는 모델이 고른 행동이 안전 집합 밖에 있으면 안전한 후보 중 모델 확률이 가장 높은 것으로 교체합니다. 따라서 생존율은 **계획기·텍스트 선택 모델·안전 장치가 합쳐진 시스템의 결과**입니다. 이미지에서 장애물을 스스로 인식하고 물리를 발견한 CLM 단독의 능력을 뜻하지 않습니다. [후보 설명 생성](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/examples/t_rex/trex/backends.py#L35-L62), [행동 교체](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/examples/t_rex/trex/brain.py#L24-L53)

예제 문서는 5개 시드의 60초 실행, 충돌 후 1.5초 재시작, 생존을 구간 내 사망 0회로 정의합니다. CLM은 RTX 4090에서, Jev는 호스팅 API로 실행했다고 기록하며 지연도 클라이언트 측 요청 시간입니다. 이 조건은 H100의 검증기 지연이나 API 응답 헤더의 서버 측 시간과 섞어 비교하면 안 됩니다. [T-Rex 실험 조건](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/examples/t_rex/README.md#L8-L35)

## 설치와 사용: 문서의 명령과 코드의 차이

같은 SHA의 README는 다음 설치·서빙 명령을 제공합니다. 아래 명령은 문서 인용이며 이번 리뷰에서 실행한 기록이 아닙니다. [Installation과 Quickstart](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/README.md#L40-L65)

```bash
pip install contrastive-lm
vllm serve Qwen/Qwen3-8B --served-model-name qwen3-8b --runner pooling --max-model-len 2048 --port 8090 &
clm-serve
```

첫 프로세스는 외부 임베딩 인코더를, 두 번째는 CLM API와 Playground를 제공합니다. 2048보다 긴 상태를 다루려면 README가 설명하듯 vLLM의 `--max-model-len`과 `clm-serve --max-tokens`를 함께 올려야 합니다. 서버는 텍스트를 임베딩 서비스로 보내므로 토큰 한도가 한쪽에서만 늘어서는 충분하지 않습니다. [길이 제한 설명](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/README.md#L65-L67)

직접 `Engine()`을 만드는 예시에는 “없으면 기준 헤드 다운로드”라는 주석이 있습니다. 그러나 읽은 구현에서 자동 다운로드는 `clm-serve`의 `main`이 담당합니다. `Engine.__init__`은 `default_checkpoint()`로 로컬 파일을 찾으며 그 함수는 다운로드하지 않습니다. 로컬 기준 헤드가 없으면 기본 `clm-latest`가 등록되지 않아 해당 모델의 추론 호출은 실패할 수 있습니다. 직접 엔진을 사용할 때는 이 차이를 구분해야 합니다. [README 예시](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/README.md#L99-L114), [엔진 초기화](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/src/clm/engine.py#L36-L55), [로컬 조회](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/src/clm/heads.py#L167-L173), [CLI 다운로드](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/src/clm/server.py#L192-L207)

## 한계와 사용 시 확인할 경계

**입력 후보와 텍스트 구성에 결과가 의존합니다.** `Choice`의 설명이 행동의 실제 의미를 전달해야 하며, `Score`는 순서가 있는 범주 선택입니다. 후보 간 상대 분포를 실제 성공 확률로 곧바로 해석할 수는 없습니다. 이 차이는 API의 형태가 간결할수록 더 쉽게 놓치기 쉽습니다.

**코드 SHA만으로 전체 실험 버전이 고정되지는 않습니다.** 헤드 다운로드는 Hugging Face revision을 지정하지 않고 fallback URL도 `resolve/main`을 사용합니다. 데이터 snapshot 다운로드 역시 revision 인자가 없습니다. 따라서 이 글의 SHA는 읽은 코드 버전이며 외부 가중치·데이터·vLLM 조합을 모두 고정했다는 뜻이 아닙니다. [헤드 다운로드](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/src/clm/heads.py#L133-L154), [데이터 다운로드](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/preprocessing/hf_embeddings.py#L44-L54)

**health 응답의 의미도 나뉩니다.** 서버는 `/health`에서 `ok: true`와 외부 인코더 상태인 `embedder`를 별도로 반환합니다. 반면 `CLMClient.health()`는 `ok`만 봅니다. 클라이언트 health가 참이라고 해서 외부 인코더까지 사용할 수 있다고 판단해서는 안 됩니다. 이 지적은 함수 분기의 정적 확인이며 장애 상황을 실제로 재현한 결과는 아닙니다. [서버 health](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/src/clm/server.py#L82-L89), [클라이언트 health](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/src/clm/client.py#L199-L203)

**라이선스의 범위를 구분해야 합니다.** 저장소에는 Apache 2.0 `LICENSE`가 있고, README는 코드와 공개 CLM-8B 가중치를 Apache 2.0으로 설명합니다. 이 리뷰에서 직접 읽은 라이선스 파일은 저장소 코드의 파일이며, 외부 데이터셋과 인코더의 배포 조건까지 동일하다고 추정하지 않습니다. [LICENSE](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/LICENSE), [README 라이선스 설명](https://github.com/Contrastive-LM/CLM/blob/bb42c6c5bf914fd449bed2f6ca65be80602cb1f7/README.md#L335-L337)

### 이 글에서 다루지 못한 부분

Playground의 브라우저 상태 관리와 공유 링크, T-Rex의 전체 물리·충돌·동시 요청 스케줄링, 모든 fold 생성 옵션, Parquet 내보내기·업로드 경로는 전체 감사를 하지 않았습니다. 외부 사전학습 파이프라인, 가중치 내용, 원시 benchmark 데이터, README 그림의 원시 측정값도 검증하지 않았습니다. `docs/FINETUNING.md`는 실험 반복 절차를 기술한 자료로 읽었으며 그 안의 실행·수정 지시를 수행하지 않았습니다. 정적 분석으로 확인한 것은 코드 경로와 계산 정의이며 실제 실행 성공이나 지연·정확도 보장은 아닙니다.

## 결론

CLM의 중심은 큰 언어 모델이 만든 상태·후보 임베딩을 두 개의 작은 헤드로 정렬하고, 후보별 점수를 타입이 있는 결정으로 바꾸는 구조입니다. 상태와 행동을 분리하면 반복되는 후보를 캐시할 수 있고, 고정 임베딩 위의 미세조정으로 선택 공간을 조정할 수 있습니다. 공개 코드는 텍스트 변환, 두 계층의 캐시, 양방향 대조 손실, task 단위 분할, 마지막 구간 평균에 의한 궤적 선택까지 이어집니다. 그 구조의 유용성과 별개로 benchmark 수치는 후보 생성·분할·안전 장치·캐시·측정 환경을 포함한 조건부 결과로 읽어야 합니다.
