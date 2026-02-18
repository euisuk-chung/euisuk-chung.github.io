---
title: "[Paper Review] EXAONE 4.0: Unified Large Language Models Integrating
Non-reasoning and Reasoning Modes"
date: "2025-08-29"
tags:
  - "EXAONE"
  - "paper-review"
year: "2025"
---

# [Paper Review] EXAONE 4.0: Unified Large Language Models Integrating
Non-reasoning and Reasoning Modes

![](https://velog.velcdn.com/images/euisuk-chung/post/e106b46f-38f9-428c-82e7-d8872d22e773/image.png)

> <https://arxiv.org/pdf/2507.11407>

Introduction
------------

LLM 생태계에서 가장 뚜렷한 트렌드 중 하나는 "빠른 응답"과 "깊은 추론"을 하나의 모델로 제공하는 Hybrid 모델의 부상입니다.

여기서 "빠른 응답"이란 일반적인 대화나 요약처럼 즉각적인 답변이 필요한 상황을, "깊은 추론"이란 복잡한 수학 문제나 코딩 과제처럼 단계적 사고(Chain-of-Thought)가 필요한 상황을 의미합니다. 기존에는 이 두 가지 능력을 각각 별도의 모델로 제공하는 것이 일반적이었습니다. 예를 들어 OpenAI의 경우 범용 GPT-4o와 추론 특화 o1/o3를, DeepSeek은 DeepSeek V3(범용)와 DeepSeek R1(추론)을 별도로 운영합니다. 사용자 입장에서는 용도에 따라 모델을 전환해야 하고, 서비스 제공자 입장에서는 두 모델을 동시에 배포하고 관리해야 하는 부담이 있었습니다.

최근 Qwen 3, DeepSeek 등 주요 모델들이 두 모드를 하나로 통합하는 방향으로 수렴하고 있으며, LG AI Research의 EXAONE 4.0도 이 흐름의 한가운데에 있습니다.

LG AI Research는 EXAONE이라는 자체 Foundation Model 시리즈를 개발해 왔습니다. 직전 버전인 EXAONE 3.5는 다양한 사용자 지시를 정확히 따르는 범용 Instruction Following에, EXAONE Deep은 수학과 코딩 영역의 추론 성능에 각각 특화되어 있었습니다. EXAONE 4.0은 이 두 모델의 강점을 NON-REASONING 모드와 REASONING 모드라는 형태로 단일 모델에 통합한 것이 핵심입니다. 사용자가 빠른 답변이 필요하면 NON-REASONING 모드를, 복잡한 문제 풀이가 필요하면 REASONING 모드를 선택할 수 있습니다.

여기에 Agentic AI 시대를 겨냥한 Tool Use 기능이 새로 추가되었습니다. Tool Use란 모델이 외부 도구(API 호출, 데이터베이스 조회, 웹 검색 등)를 자율적으로 활용하여 사용자의 요청을 해결하는 능력을 뜻합니다. 최근 LLM이 단순한 텍스트 생성을 넘어 실제 작업을 수행하는 "Agent"로 발전하면서, Tool Use는 필수적인 기능으로 자리잡고 있습니다. 이 외에도 Spanish 언어 지원 추가(기존 영어/한국어에서 확장), 14T 토큰으로 대폭 확대된 Pretraining, 128K 토큰까지의 Context Length 확장이 이루어졌습니다.

모델은 고성능 32B(320억 파라미터)와 On-device용 1.2B(12억 파라미터) 두 가지 크기로 제공됩니다. 32B는 서버 환경에서의 고성능 추론을, 1.2B는 스마트폰이나 Edge Device 같은 제한된 환경에서의 로컬 실행을 목표로 합니다. 연구 목적으로 Hugging Face에서 공개되어 있습니다.

이 글에서는 EXAONE 4.0 Technical Report의 흐름을 따라, 아키텍처 설계 결정부터 Post-training 파이프라인, 벤치마크 성능까지 체계적으로 분석합니다.

Model Configurations: 아키텍처의 핵심 변경점
----------------------------------

### Hybrid Attention — Global과 Sliding Window의 결합

EXAONE 4.0 32B의 가장 눈에 띄는 아키텍처 변경은 Attention 메커니즘입니다.

먼저 배경을 짚어보겠습니다. Transformer 모델의 Self-Attention은 시퀀스 내 모든 토큰 쌍 간의 관계를 계산합니다. 예를 들어 1,000개의 토큰으로 구성된 입력이 있다면, 각 토큰이 나머지 999개의 토큰과 어떤 관련이 있는지를 모두 계산하는 것입니다. 이를 **Global Attention**이라 하며, 문맥 이해에는 강력하지만 시퀀스 길이 nnn에 대해 O(n2)O(n^2)O(n2)의 연산 비용이 발생합니다. 시퀀스 길이가 2배가 되면 연산량은 4배로 늘어나는 셈입니다. 128K 토큰(약 10만 자 이상의 텍스트)까지 처리해야 하는 EXAONE 4.0에서는 이 비용이 현실적인 병목이 됩니다.

이에 대한 효율적 대안이 **Sliding Window Attention(Local Attention)**입니다. 전체 시퀀스가 아닌 각 토큰 주변의 고정된 범위(Window) 내에서만 Attention을 계산합니다. Window Size가 4K라면, 각 토큰은 자신의 앞뒤 4K 토큰 범위 내에서만 관계를 파악합니다. 연산 비용이 O(n×w)O(n \times w)O(n×w) (w는 Window Size)로 줄어들어 효율적이지만, Window 밖의 먼 토큰과의 관계는 직접 파악할 수 없다는 한계가 있습니다.

EXAONE 3.5는 모든 레이어에서 Global Attention을 사용했습니다. EXAONE 4.0은 이를 변경하여 Sliding Window Attention(Local)과 Global Attention을 **3:1 비율**로 혼합합니다. 64개 레이어 중 48개는 Window Size 4K의 Sliding Window Attention을, 16개는 전체 시퀀스에 대한 Global Attention을 사용하는 것입니다.

이 설계의 직관은 명확합니다. 대부분의 레이어에서는 주변 토큰 간의 관계(Local Context)를 파악하는 것으로 충분하고, 주기적으로 배치된 Global Attention 레이어가 시퀀스 전체의 맥락을 통합하는 역할을 합니다. 비유하자면, 긴 소설을 읽을 때 대부분의 시간은 현재 단락의 맥락에 집중하되, 가끔 전체 줄거리를 상기하며 큰 그림을 파악하는 것과 유사합니다. Gemma 2/3, Llama 4 등 최근 연구에서도 소수 레이어에만 Global Attention을 적용해도 Long-context 성능이 유지된다는 결과가 보고되어 있으며, Mamba 같은 Heterogeneous 구조에서도 주기적인 소량의 Global Attention이 전역 맥락 이해에 도움이 된다는 점이 확인되었습니다.

여기서 주목할 설계 결정이 두 가지 있습니다.

첫째, **Global Attention 레이어에서 RoPE(Rotary Position Embedding)를 사용하지 않습니다.** RoPE는 토큰의 상대적 위치 정보를 Attention 계산에 주입하는 기법으로, 대부분의 최신 LLM에서 표준적으로 사용됩니다. 그런데 EXAONE 4.0은 Global Attention 레이어에서 이를 의도적으로 제거했습니다. 이유는 RoPE가 적용되면 모델이 토큰 간 거리에 따른 Bias(가까운 토큰에 더 높은 가중치를 부여하는 경향)를 갖게 되는데, Global Attention의 역할은 시퀀스 전체를 균등하게 조망하는 것이므로, 위치 기반 Bias 없이 진정한 전역적 시야를 유지하도록 설계한 것입니다. Local Attention 레이어에서는 RoPE를 그대로 사용하여 근접 토큰 간의 위치 관계를 정확히 포착합니다.

둘째, **Local Attention으로 Chunked Attention 대신 Sliding Window Attention을 채택했습니다.** Chunked Attention은 시퀀스를 고정 크기의 Chunk로 나누어 Chunk 내에서만 Attention을 계산하는 방식입니다. 효율적이지만 Chunk 경계에서 정보가 단절되는 문제가 있습니다. 반면 Sliding Window Attention은 윈도우가 토큰마다 한 칸씩 이동하므로 경계 단절 문제가 없습니다. EXAONE 4.0은 Sliding Window의 이론적 안정성과 오픈소스 프레임워크(vLLM, TGI 등)에서의 광범위한 지원이라는 실용적 이유를 들어 이를 선택했습니다. Short-context 성능에 악영향을 최소화하기 위해 Window Size를 4K로 설정한 것도 실용적 판단입니다.

한편, 1.2B 모델은 Hybrid가 아닌 전체 Global Attention을 사용합니다. 레이어 수가 30개로 상대적으로 적어 Hybrid의 효율성 이점이 제한적이며, 소규모 모델에서는 이미 제한된 모델 용량을 전역적 맥락 파악에 최대한 활용하는 것이 더 중요할 수 있기 때문으로 해석됩니다.

### QK-Reorder-LN — Layer Normalization의 재배치

두 번째 주요 아키텍처 변경은 LayerNorm의 위치입니다.

이 변경을 이해하려면 Transformer의 Layer Normalization 배치에 대한 배경이 필요합니다. Layer Normalization(LayerNorm)은 각 레이어의 출력을 정규화하여 학습을 안정화하는 기법입니다. 원래 Transformer("Attention Is All You Need") 논문에서는 레이어 출력 후에 Normalization을 적용하는 **Post-LN** 구조를 사용했습니다. 이후 **Pre-LN** 구조(레이어 입력에 Normalization 적용)가 등장하여, 학습 안정성을 크게 개선했고 대부분의 최신 LLM에서 사실상 표준이 되었습니다.

그런데 최근 "The Curse of Depth in Large Language Models" 연구에서 Pre-LN의 구조적 문제가 지적되었습니다. 모델 깊이가 증가할수록 출력의 분산(Variance)이 기하급수적으로 커지며, 이로 인해 깊은 레이어들이 모델 성능에 실질적으로 기여하지 못하는 현상이 발생합니다. 직관적으로 설명하면, 64개 레이어를 가진 모델에서 앞쪽 레이어들의 출력은 적절한 크기를 유지하지만 뒤쪽 레이어로 갈수록 출력 값의 범위가 극단적으로 커져서, 마지막 몇십 개의 레이어는 사실상 "죽은 레이어" — 파라미터는 존재하지만 예측에 의미 있는 기여를 하지 못하는 상태 — 가 되는 것입니다.

EXAONE 4.0은 이 문제를 해결하기 위해 **QK-Reorder-LN**을 채택합니다. 구체적으로는 Attention 블록 내에서 Query와 Key 벡터에 각각 RMSNorm을 적용한 후 Attention 연산을 수행하고, Attention Output에 한 번 더 RMSNorm을 적용합니다. RMSNorm(Root Mean Square Normalization)은 LayerNorm의 경량화 버전으로, 평균을 빼는 연산을 생략하고 RMS 값으로만 정규화하여 계산 효율이 높습니다. EXAONE 3.0부터 사용해온 RMSNorm 자체는 유지하되, 적용 위치를 재배치한 것입니다.

이 방식은 기존 Pre-LN 대비 연산량이 증가하는 Trade-off가 있습니다 — Attention 블록 내에 추가적인 Normalization 연산이 들어가기 때문입니다. 그러나 OLMoE, OLMo 2 등의 연구에서 QK-Normalization과 유사한 접근이 Downstream Task 성능을 개선하는 것으로 보고되었으며, EXAONE 팀도 단순히 분산을 스케일링하는 방식보다 QK-Reorder-LN이 더 나은 성능을 보인다는 실험적 결과를 얻었습니다.

### 모델 스펙 요약

| 항목 | 32B | 1.2B |
| --- | --- | --- |
| dmodeld\_\text{model}dmodel​ (Hidden Dimension) | 5,120 | 2,048 |
| Layers | 64 | 30 |
| Normalization | QK-Reorder-LN | QK-Reorder-LN |
| Non-linearity | SwiGLU | SwiGLU |
| FFN Dimension | 27,392 | 4,096 |
| Attention Type | Hybrid (Local:Global = 3:1) | Global |
| Head Type / Heads / KV Heads | GQA / 40 / 8 | GQA / 32 / 8 |
| Head Size | 128 | 64 |
| Max Seq Length | 131,072 (128K) | 65,536 (64K) |
| RoPE θ\thetaθ | 1,000,000 | 1,000,000 |
| Tokenizer / Vocab | BBPE / 102,400 | BBPE / 102,400 |
| Tied Embedding | False | True |

두 모델 모두 GQA(Grouped Query Attention)를 사용합니다. GQA는 Multi-Head Attention에서 Key와 Value Head의 수를 Query Head보다 적게 설정하여, KV Cache 메모리를 절약하면서 성능은 유지하는 기법입니다. 32B 모델은 40개의 Query Head에 8개의 KV Head를, 1.2B 모델은 32개의 Query Head에 8개의 KV Head를 사용합니다.

Tokenizer는 BBPE(Byte-level Byte Pair Encoding)를 사용하며, 102,400개의 Vocabulary를 한국어와 영어 토큰이 거의 동일한 비율로 공유합니다. 1.2B 모델은 파라미터 효율성을 위해 Tied Word Embedding(입력 Embedding과 출력 Projection이 같은 가중치를 공유하는 방식)을 사용합니다.

Pre-training: 데이터 규모와 품질의 동시 강화
-------------------------------

EXAONE 4.0 32B 모델은 **14T(14조) 토큰**으로 Pretraining되었으며, 이는 EXAONE 3.5의 6.5T 대비 약 2배에 해당합니다. 1.2B 모델도 12T 토큰으로 학습되어 모델 크기 대비 상당히 많은 데이터를 소화했습니다. 투입된 연산량(FLOPs)은 32B 모델이 2.69×10242.69 \times 10^{24}2.69×1024, 1.2B 모델이 8.65×10228.65 \times 10^{22}8.65×1022입니다. 참고로 Pretraining은 모델이 대규모 텍스트 데이터로부터 언어의 패턴, 사실 지식, 추론 능력 등을 학습하는 초기 학습 단계로, 이후의 Fine-tuning과 구분됩니다.

이 데이터 증가는 단순히 양적 확대에 그치지 않습니다. World Knowledge 강화를 명확한 목표로 설정하고, STEM(Science, Technology, Engineering, Mathematics) 분야 등 전문 도메인의 데이터를 특별히 큐레이션했습니다. "큐레이션"이란 단순히 데이터를 모으는 것이 아니라, 품질 기준에 따라 선별하고 정제하는 과정을 의미합니다. 실제로 MMLU-Redux 등 지식 기반 벤치마크에서 뚜렷한 성능 향상이 관찰되었습니다.

또한 최근 연구("Four Habits of Highly Effective STaRs")에서 추론 성능이 Pretraining 과정에서 학습된 Cognitive Behavior에 크게 영향을 받는다는 결과가 보고되었습니다. Cognitive Behavior란 모델이 텍스트를 생성할 때 보이는 사고 패턴 — 예를 들어 문제를 단계적으로 분해하거나, 가정을 검증하거나, 대안을 탐색하는 등의 행동 — 을 말합니다. 이러한 패턴은 주로 Pretraining 데이터에 포함된 문서(교과서, 학술 논문, 논리적 토론 등)로부터 학습됩니다. EXAONE 4.0은 이를 반영하여 Pretraining 단계에서부터 엄격한 Data Curation을 수행하여, 단순히 지식뿐 아니라 Post-training에서의 추론 성능까지 고려한 데이터 구성을 했다고 합니다.

Context Length Extension: 4K에서 128K까지
-------------------------------------

EXAONE 4.0은 최대 128K 토큰의 Context Length를 지원합니다. Context Length란 모델이 한 번에 처리할 수 있는 입력 텍스트의 최대 길이를 의미합니다. 128K 토큰은 대략 영문 기준 약 300페이지 분량의 텍스트에 해당하며, 긴 문서 요약, 대량의 코드 분석, 여러 문서를 동시에 참조하는 QA 등에서 핵심적인 능력입니다.

그런데 처음부터 128K 토큰으로 학습하는 것은 비효율적입니다. 긴 시퀀스는 연산 비용이 높고, 대부분의 학습 데이터는 128K보다 훨씬 짧기 때문입니다. 따라서 EXAONE 4.0은 **2단계 점진적 확장** 과정을 거칩니다.

먼저 4K Context로 Pretrain된 모델을 32K로 확장하고, 이후 다시 128K로 확장합니다. 각 단계에서 **NIAH(Needle In A Haystack)** 테스트를 통해 성능을 검증합니다. NIAH 테스트는 긴 텍스트(Haystack) 안에 특정 정보(Needle)를 숨기고, 모델이 이를 정확히 찾아내는지 확인하는 표준적인 Long-context 평가 방법입니다. 모든 위치(시작, 중간, 끝)와 모든 길이에서 "green light"(정보를 정확히 찾아냄)이 확인될 때까지 반복적으로 최적화를 진행합니다.

Short-context 영역에서의 성능 저하를 방지하기 위해 신중한 데이터 선정 방법론과 Progressive Training Recipe를 적용한 점이 주목할 만합니다. Long-context Fine-tuning 과정에서 기존의 Short-context 능력이 훼손되는 현상은 "Catastrophic Forgetting"의 일종으로 흔히 발생하는 문제이며, EXAONE 4.0은 이를 명시적으로 관리하고 있습니다.

1.2B 모델은 64K 토큰까지 확장됩니다. 1B 파라미터 범위의 모델 대부분이 32K를 최대 지원하는 것을 감안하면, 이는 동급 대비 약 2배의 Context Length입니다.

Post-training: 5단계 파이프라인
------------------------

Pretraining이 "원시적인 언어 능력"을 학습하는 단계라면, Post-training은 이 능력을 사용자의 지시를 따르고, 정확하게 추론하며, 인간의 선호에 맞게 응답하도록 정제하는 단계입니다. EXAONE 4.0의 Post-training은 5단계로 구성된 정교한 파이프라인을 거칩니다. 크게 SFT(Supervised Fine-Tuning) → RL(Reinforcement Learning) → Preference Learning의 3개 축으로 나뉩니다.

### Large-Scale Supervised Fine-Tuning

SFT는 인간이 작성한 고품질 입력-출력 쌍을 통해 모델이 "바람직한 응답 형태"를 학습하는 과정입니다. EXAONE 4.0의 SFT에서는 5개 도메인에 걸쳐 데이터를 구성합니다.

**World Knowledge** 도메인에서는 웹 소스에서 수집한 문제를 교육적 가치 기준으로 필터링합니다. 단순한 사실 암기가 아니라, 다양한 분야와 난이도에 걸친 지식의 Distillation(증류)을 목표로 합니다. 전문적이고 고난이도의 데이터는 특별히 샘플링하여 REASONING 모드 학습에 활용합니다.

**Math, Code, Logic** 도메인에서는 정확한 Ground Truth 확보가 어렵다는 근본적 제약이 있습니다. 수학 문제는 답이 명확하지만 고품질 문제 자체를 대량으로 만들기가 어렵고, 코드 문제는 테스트 케이스를 통한 검증이 필요합니다. 검증 불가능한 문제를 억지로 만드는 대신, 검증 가능한 답이 있는 문제에 대해 다양한 응답을 생성하는 전략을 택합니다. 흥미로운 실험적 발견은, 하나의 문제에 대해 여러 다른 풀이법(응답)을 생성하는 것이 고유한 문제의 수나 다양성을 늘리는 것과 동등한 효과를 보인다는 점입니다. 이는 데이터 구축 비용을 크게 줄일 수 있는 실용적 인사이트입니다. REASONING 모드에서 Math/Code 응답은 긴 사고 과정을 포함하여 길어지는 경향이 있어, Degeneration(반복적이거나 무의미한 텍스트 생성)과 언어 불일치(한국어 질문에 영어로 답하는 등)의 위험이 높아지므로, 신중한 필터링을 적용합니다. Code 도메인에서는 알고리즘 Problem-solving을 넘어 Full Stack Development에 초점을 맞춘 Software Engineering 데이터셋도 포함됩니다.

**Long Context** 도메인에서는 Context 길이와 핵심 정보의 위치를 체계적으로 변화시켜, 분산된 정보를 식별하고 추론하는 능력을 훈련합니다. 예를 들어 핵심 정보가 긴 문서의 처음, 중간, 끝에 각각 위치하는 경우를 모두 학습하는 것입니다. 한국어의 경우 법률, 행정, 기술 문서 등을 정제하여 다양한 Long-context 입력 형식에 맞게 재구성합니다.

**Agentic Tool Use** 도메인에서는 단순한 Single Tool Call(하나의 API를 한 번 호출하는 것)이 아니라, 보다 현실적인 시나리오를 다룹니다. 사용자와의 대화를 통해 요구사항을 구체화하고, 여러 도구를 순차적으로 호출하며, 중간 결과를 바탕으로 다음 행동을 결정하고, 실행 오류 시 대안을 모색하는 — 이런 복잡한 **Long-horizon Tool-calling** 데이터를 구축합니다. Multi-step(여러 단계의 도구 호출), Multi-turn(여러 차례의 대화 왕복) 형식으로 조직화하여 Agentic Tool Use의 학습을 효과적으로 지원합니다.

**Multilinguality** 도메인에서는 한국어와 Spanish 모두에 대해 문화/역사적 지식과 자연스러운 대화 능력을 목표로 데이터를 구성합니다. 기존 영어 샘플의 번역을 쿼리로 활용하는 한편, 각 언어 고유의 새로운 Instruction도 생성합니다. 한국어는 특히 교육과 산업 전문가 관련 주제를 큐레이션하여 도메인 특화 쿼리 대응 능력을 강화합니다.

**Unified Mode Training.** NON-REASONING과 REASONING 데이터를 순차적으로가 아니라 함께 학습하는 것이 핵심 설계 결정입니다. 순차적 학습(먼저 NON-REASONING, 그 다음 REASONING)은 나중에 학습한 모드가 이전 모드를 덮어쓰는 Catastrophic Forgetting 위험이 있습니다. 동시 학습은 이 위험을 줄이지만, 두 모드 간 데이터 비율 설정이 중요합니다. Ablation Study를 통해 REASONING 대 NON-REASONING 데이터의 **토큰 비율을 1.5:1**로 설정했습니다. REASONING 비율이 너무 높으면 NON-REASONING 모드에서도 모델이 불필요하게 긴 사고 과정을 생성하는 문제가 발생했기 때문입니다. 반대로 너무 낮으면 REASONING 모드의 추론 품질이 저하될 것입니다.

Unified Mode 학습 후에는 도메인 불균형을 해소하기 위해, Code와 Tool Use 도메인의 고품질 REASONING 데이터를 재사용하는 2차 SFT를 수행합니다. 전체 데이터에서 이 도메인의 비중이 상대적으로 낮았기 때문에, 해당 영역의 성능을 보강하려는 의도입니다.

### Reasoning Reinforcement Learning — AGAPO

SFT가 "좋은 응답의 패턴을 모방"하는 것이라면, RL(Reinforcement Learning)은 "시행착오를 통해 스스로 더 나은 전략을 발견"하는 것입니다. 모델이 문제에 대해 여러 응답을 생성하고, 정답/오답 여부에 따른 보상(Reward)을 받아 정답을 낼 확률을 높이는 방향으로 학습합니다.

EXAONE 4.0은 SFT 이후 Online RL을 수행하며, 기존 GRPO(Group Relative Policy Optimization)의 한계를 포괄적으로 개선한 새로운 알고리즘 **AGAPO(Asymmetric Sampling and Global Advantage Policy Optimization)**를 제안합니다.

먼저 GRPO에 대해 간단히 설명하겠습니다. GRPO는 DeepSeek에서 제안한 RL 알고리즘으로, 각 문제에 대해 여러 개의 응답(Group)을 생성한 뒤, 그룹 내에서의 상대적 성능 차이(Advantage)를 계산하여 정책을 업데이트합니다. PPO(Proximal Policy Optimization)와 달리 별도의 Critic(Value) 모델이 필요 없어 메모리 효율이 좋고, Verifiable Reward(수학 정답 여부, 코드 테스트 통과 여부 등 객관적으로 검증 가능한 보상)와 결합하면 매우 효과적입니다. 그러나 몇 가지 구조적 한계가 있으며, AGAPO는 이를 체계적으로 개선합니다.

학습 데이터는 수학, 코드, 과학, Instruction Following의 4개 카테고리로 구성됩니다. 효율적인 학습을 위해 SFT 모델에서 8개의 응답을 생성하여, 8개 모두 정답인 샘플(모델에게 이미 쉬운 문제)은 사전 필터링으로 제거합니다. 쉬운 문제에서는 모델이 새로운 것을 배울 여지가 적기 때문입니다.

보상 함수는 카테고리별로 맞춤 설계됩니다. 수학은 Rule-based Verifier(정답과의 일치 여부), 코드는 Test Case 통과 여부, 과학은 Rule-based Verifier 실패 시 LLM Judge가 2차 검증(더 유연한 판단), Instruction Following은 모든 제약 조건 충족 시 1, 아니면 0을 부여합니다.

AGAPO의 핵심 설계 요소는 네 가지입니다.

**첫째, Clipped Objective 제거.** PPO는 학습 안정성을 위해 Policy Update의 크기를 제한하는 "Clipping"을 사용합니다. 구체적으로, 새 정책과 기존 정책의 확률 비율(Ratio)이 일정 범위를 벗어나면 Gradient를 차단합니다. 이는 안정성에는 유리하지만, 낮은 확률의 토큰 — 즉 모델이 현재는 거의 생성하지 않지만 실은 중요한 역할을 할 수 있는 토큰 — 의 Gradient Update가 차단되는 부작용이 있습니다. 이러한 토큰은 종종 추론 경로의 분기점(fork) 역할을 하는 Reflective Behavior(예: "잠깐, 이 접근은 틀렸으니 다시 생각해보자")와 관련이 있습니다. AGAPO는 Clipping을 제거하고 표준 Policy Gradient Loss를 사용하여, 이러한 탐색적 토큰이 학습에 온전히 기여할 수 있도록 합니다.

**둘째, Asymmetric Sampling.** 기존 GRPO에서는 한 문제에 대해 생성된 모든 응답이 정답이거나 모두 오답인 경우, 그룹 내 상대적 차이가 없으므로 Advantage가 0이 됩니다. 따라서 이런 샘플은 학습에 기여하지 못해 폐기됩니다. 그러나 "모든 응답이 오답"인 경우에도 유용한 학습 신호가 존재합니다 — 모델이 이런 유형의 문제에서 특히 취약하다는 정보 자체가 가치 있기 때문입니다. Negative Sample Reinforcement의 효과에 대한 최근 연구("The Surprising Effectiveness of Negative Reinforcement in LLM Reasoning")를 반영하여, AGAPO는 모든 응답이 오답인 샘플을 버리지 않습니다. 대신 Advantage 계산을 통해 작은 음의 보상을 할당하여, 모델이 잘못된 추론 경로를 적극적으로 회피하도록 학습합니다. "비대칭(Asymmetric)"이라는 이름은 All-correct(폐기)와 All-incorrect(유지)를 비대칭적으로 처리하는 데서 유래합니다.

**셋째, Group & Global Advantage.** GRPO의 Advantage 계산은 각 그룹(같은 문제에 대한 응답들) 내에서만 이루어집니다. 이 방식은 그룹 내 상대적 차이만 반영할 뿐, 전체 배치의 난이도 분포를 고려하지 못합니다. 예를 들어 All-incorrect 그룹에 적절한 크기의 음의 보상을 부여하려면, 배치 전체에서 이 그룹이 얼마나 나쁜 성과인지를 알아야 합니다. AGAPO는 이를 위해 2단계 Advantage 계산을 도입합니다. 먼저 그룹 내에서 LOO(Leave-One-Out) 방식으로 Advantage를 계산합니다. LOO는 각 응답의 보상에서 나머지 응답들의 평균 보상을 빼는 방식으로, 해당 응답이 그룹 내에서 상대적으로 얼마나 좋거나 나쁜지를 측정합니다. 그 다음, 전체 미니배치에 걸쳐 정규화(평균을 빼고 표준편차로 나눔)하여 최종 Global Advantage를 산출합니다.

Aloo,i=ri−1G−1∑j≠irj,Aglobal,i=Aloo,i−mean{Aloo,k}kstd{Aloo,k}kA\_{\text{loo},i} = r\_i - \frac{1}{G-1}\sum\_{j \neq i} r\_j, \quad A\_{\text{global},i} = \frac{A\_{\text{loo},i} - \text{mean}\{A\_{\text{loo},k}\}\_k}{\text{std}\{A\_{\text{loo},k}\}\_k}Aloo,i​=ri​−G−11​∑j​=i​rj​,Aglobal,i​=std{Aloo,k​}k​Aloo,i​−mean{Aloo,k​}k​​

여기서 rir\_iri​는 iii번째 응답의 보상, GGG는 그룹 크기, kkk는 미니배치 내 모든 응답의 인덱스입니다.

**넷째, Sequence Level Cumulative KL.** RL로 추론 능력을 강화하는 과정에서, SFT 단계에서 학습한 다른 능력(자연스러운 대화, Instruction Following 등)이 손상될 수 있습니다. 이를 방지하기 위해 KL Divergence Penalty를 적용합니다. KL Penalty는 RL로 업데이트되는 현재 정책(πθ\pi\_\thetaπθ​)이 SFT 이후의 참조 정책(πref\pi\_\text{ref}πref​)에서 너무 멀어지지 않도록 제약하는 역할을 합니다. AGAPO는 토큰 수준이 아닌 Sequence 수준의 Cumulative KL을 채택하여, 개별 토큰의 미세한 확률 변화보다는 전체 응답 수준에서의 분포 변화를 관리합니다.

최종 Objective는 다음과 같습니다:

JAGAPO(θ)=Eq∼P(Q),  {oi}i=1G∼πθ(O∣q)[1G∑i=1G(Aglobal,ilog⁡πθ(oi∣q)−βDKL(πθ∥πref))]J\_{\text{AGAPO}}(\theta) = \mathbb{E}\_{q \sim P(Q),\; \{o\_i\}\_{i=1}^G \sim \pi\_\theta(\mathcal{O}|q)} \left[ \frac{1}{G} \sum\_{i=1}^{G} \left( A\_{\text{global},i} \log \pi\_\theta(o\_i | q) - \beta D\_{\text{KL}}(\pi\_\theta \| \pi\_{\text{ref}}) \right) \right]JAGAPO​(θ)=Eq∼P(Q),{oi​}i=1G​∼πθ​(O∣q)​[G1​∑i=1G​(Aglobal,i​logπθ​(oi​∣q)−βDKL​(πθ​∥πref​))]

Aglobal,ilog⁡πθ(oi∣q)A\_{\text{global},i} \log \pi\_\theta(o\_i | q)Aglobal,i​logπθ​(oi​∣q) 부분은 좋은 응답의 생성 확률을 높이고 나쁜 응답의 확률을 낮추는 Policy Gradient이며, βDKL\beta D\_{\text{KL}}βDKL​ 부분은 정책이 참조 모델에서 너무 벗어나지 않도록 하는 정규화 항입니다. β\betaβ는 두 항 간의 균형을 조절하는 하이퍼파라미터입니다.

AGAPO의 각 컴포넌트가 해결하는 문제를 정리하면 다음과 같습니다.

| 기법 | 해결하는 문제 | 핵심 아이디어 |
| --- | --- | --- |
| Remove Clipped Objective | PPO Clip이 탐색적 토큰의 Gradient 차단 | 표준 Policy Gradient Loss 사용 |
| Asymmetric Sampling | All-incorrect 샘플 폐기로 인한 정보 손실 | All-incorrect에 작은 음의 보상, 폐기하지 않음 |
| Group & Global Advantage | GRPO가 배치 전체 분포 미반영 | LOO(그룹 내) → Global Normalization(배치 전체) |
| Seq-Level Cumulative KL | SFT 학습 능력 보존 | 시퀀스 수준 누적 KL Penalty |

### Preference Learning — 2단계 인간 정렬

RL 단계에서는 Verifiable Reward — 즉 "정답이냐 오답이냐"라는 객관적 보상 — 를 통한 정확도 향상에 집중합니다. 그러나 이것만으로는 충분하지 않습니다. 인간이 선호하는 응답의 스타일(간결함, 자연스러움, 정중함 등)을 학습하지 않으며, 추론 Task에 특화되면서 다른 유형의 Task에서 성능 저하가 관찰됩니다. 이를 보완하기 위해 추가적인 Preference Learning을 도입합니다.

Preference Learning은 인간의 선호를 직접 학습하는 방법입니다. "이 응답이 저 응답보다 낫다"라는 형태의 비교 데이터(Chosen/Rejected 쌍)로부터 모델을 학습시킵니다. 대표적인 프레임워크가 DPO(Direct Preference Optimization)인데, EXAONE 4.0은 DPO 계열이면서 Reference Model이 불필요한 **SimPER**(Simple Preference Optimization)를 사용합니다. Reference Model이 불필요하다는 것은 학습 시 추가 모델을 메모리에 올릴 필요가 없어 효율적이라는 의미입니다.

데이터셋 구축 방식이 특징적입니다. 외부 인간 평가자가 직접 라벨링하는 것이 아니라, RL 완료 후의 모델 자신이 생성한 **On-policy 응답**을 기반으로 합니다. 각 쿼리에 대해 4~16개의 응답을 생성하고, Verifiable Reward, Preference Reward(LLM Judge가 평가하는 응답 품질), Language Consistency Reward(질문 언어와 응답 언어의 일치도), Conciseness Reward(불필요한 장황함 없이 핵심을 전달하는 정도)를 조합한 **Hybrid Reward**로 Chosen과 Rejected를 선정합니다.

**Stage 1**은 토큰 효율성에 집중합니다. REASONING 모드에서 정확한 답변을 유지하면서 불필요하게 긴 사고 과정을 줄이는 것이 목표입니다. Verifiable Reward와 Conciseness Reward를 결합하여, 정답 중 가장 짧은 응답을 Chosen으로 선택합니다. 이는 추론 비용을 직접적으로 줄이는 효과가 있습니다.

**Stage 2**는 인간 정렬(Human Alignment)에 집중합니다. Preference Reward와 Language Consistency Reward를 결합합니다. REASONING 모드 데이터의 경우, 추론 과정(Thinking) 부분이 아닌 **최종 답변에 대해서만 Preference Labeling**을 수행하는 것이 중요한 설계 결정입니다. 사고 과정의 스타일보다는 최종적으로 사용자에게 제시되는 답변의 품질과 선호도에 집중하겠다는 의미입니다. 학습 안정성을 위해 Stage 1 데이터의 일부를 Stage 2에서 재사용합니다.

Evaluation: 벤치마크 성능 분석
----------------------

### 평가 체계

EXAONE 4.0은 6개 카테고리의 벤치마크로 평가됩니다.

**World Knowledge**: MMLU-REDUX(다분야 지식 평가의 개선 버전), MMLU-PRO(더 도전적인 다분야 지식), GPQA-DIAMOND(대학원 수준의 생물학/물리학/화학 문제). **Math/Coding**: AIME 2025(미국 수학 올림피아드), HMMT FEB 2025(하버드-MIT 수학 대회), LIVECODEBENCH V5/V6(실시간 코딩 경진). **Instruction Following**: IFEVAL(지시사항 준수 평가), MULTI-IF(다국어/다턴 지시사항). **Long Context**: HELMET(종합 Long-context 평가), RULER(합성 Long-context 테스트), LONGBENCH(이중언어 Long-context 벤치마크). **Agentic Tool Use**: BFCL-V3(함수 호출 능력), TAU-BENCH(사용자-에이전트 도구 사용 시뮬레이션). **Multilinguality**: 한국어(KMMLU-PRO, KMMLU-REDUX, KSM)와 Spanish(MMMLU, MATH500, WMT24++) 평가.

비교 대상은 Mid-size(Qwen 3 32B, Gemma 3 27B, Phi 4, Mistral Small 등)부터 Frontier급(DeepSeek R1-0528 671B, Qwen 3 235B, Llama 4 Maverick 402B 등)까지 포괄합니다. REASONING 모드에서는 temperature 0.6, top-p 0.95를 사용하며, 특히 AIME/HMMT에서는 n=32n=32n=32개 응답을 샘플링하여 평균 정확도를 보고합니다. 이는 추론 문제의 확률적 특성을 감안한 평가 방식입니다.

### REASONING 모드 — Math/Coding에서의 압도적 성과

32B REASONING 모드의 가장 두드러진 결과는 Math/Coding 영역입니다.

| 벤치마크 | EXAONE 4.0 32B | Qwen 3 32B | Qwen 3 235B | DeepSeek R1-0528 |
| --- | --- | --- | --- | --- |
| AIME 2025 | **85.3** | 72.9 | 81.5 | 87.5 |
| HMMT FEB 2025 | **72.9** | 50.4 | 62.5 | 79.4 |
| LIVECODEBENCH V6 | **66.7** | 60.1 | 58.9 | 70.3 |

32B 모델이 파라미터 수 약 7배인 Qwen 3 235B를 모든 Math/Coding 벤치마크에서 능가합니다. 이는 단순히 모델 크기를 키우는 것보다 학습 방법론(AGAPO, 체계적 SFT 데이터 구성)이 추론 성능에 더 결정적인 영향을 미칠 수 있음을 시사합니다. 671B인 DeepSeek R1-0528에도 근접한 성능(AIME 85.3 vs 87.5)을 달성하여, 모델 크기 대비 효율이 매우 높음을 보여줍니다.

### REASONING 모드 — World Knowledge와 Tool Use

World Knowledge에서는 GPQA-DIAMOND 75.4로, Qwen 3 235B(71.1)를 능가하고 DeepSeek R1-0528(81.0)에 이어 두 번째를 기록합니다. GPQA-DIAMOND는 대학원 수준의 전문 지식을 요구하는 벤치마크로, 이 성과는 STEM 분야 데이터 큐레이션의 효과를 직접적으로 보여줍니다. MMLU-REDUX 92.3도 14T 토큰 Pretraining의 효과를 잘 반영합니다.

Instruction Following에서는 IFEVAL 83.7, MULTI-IF 73.5를 기록합니다. NON-REASONING과 REASONING 모드를 통합했음에도 경쟁력 있는 성능을 유지한다는 점에서, Unified Mode Training의 1.5:1 비율 설정이 효과적임을 확인할 수 있습니다. 일부 모델(Magistral Small)은 IFEVAL 37.9로 크게 낮은 점수를 보이는데, 이는 Reasoning에 특화된 모델이 일반적인 지시사항 준수에서는 취약할 수 있음을 보여주는 사례입니다.

Tool Use에서는 TAU-BENCH(Airline) 51.5로 DeepSeek R1-0528(53.5)과 유사한 수준을 보이며, TAU-BENCH(Retail) 62.8로 대부분의 Baseline을 능가합니다. TAU-BENCH는 시뮬레이션된 사용자와 대화하면서 항공권 변경, 상품 반품 등의 실제 업무를 처리하는 시나리오를 평가하는 벤치마크입니다. Agentic Tool Use가 EXAONE 4.0에서 새로 도입된 기능임을 감안하면 고무적인 출발점입니다.

### NON-REASONING 모드 — 전방위 경쟁력

NON-REASONING 모드에서도 EXAONE 4.0 32B는 동급 Mid-size 모델 중 전반적으로 최고 수준의 성능을 보여줍니다. MMLU-REDUX 89.8, MMLU-PRO 77.6으로 Phi 4(88.3/70.4), Mistral Small(85.9/69.1), Gemma 3 27B(85.0/67.5)를 크게 앞서며, Math/Coding에서도 AIME 2025 35.9, LIVECODEBENCH V6 43.1로 동급 대비 압도적입니다. NON-REASONING 모드임에도 수학/코딩에서 다른 모델의 Non-Reasoning 성능을 크게 상회하는 것은, Unified Mode Training이 REASONING의 능력을 NON-REASONING 모드에도 일정 부분 전이시키는 효과가 있음을 시사합니다.

Long Context 평가에서는 RULER 88.2를 기록하여 Qwen 3 32B(85.6), Gemma 3 27B(66.0)를 상회합니다. 특히 Llama 4 Maverick이 RULER 128K에서 2.9로 사실상 완전히 실패하는 것과 대조적으로, Hybrid Attention 구조의 효과가 명확히 드러납니다. HELMET에서는 Recall 카테고리(긴 텍스트에서 특정 정보를 찾아내는 능력)에서 94.06으로 모든 비교 모델을 압도하지만, Summarization(25.64)은 상대적 약점으로 나타납니다. 긴 텍스트에서 정보를 "찾는" 능력과 "요약하는" 능력은 서로 다른 스킬임을 보여주는 결과입니다.

한국어 성능도 눈에 띕니다. KMMLU-PRO 60.0, KO-LONGBENCH 76.9로, Frontier급 모델을 제외하면 가장 높은 수준입니다. KO-LONGBENCH는 한국어 Long-context 이해를 평가하는 자체 벤치마크로, 법률/행정/기술 문서 QA, 대화 이해, 테이블 QA 등을 포함합니다. Mistral Small(55.4)을 20% 이상 앞서는 것은 한국어 Long-context 데이터 큐레이션의 효과를 잘 보여줍니다.

### 1.2B 모델 — On-device Reasoning의 가능성

1.2B 모델의 성능은 12억이라는 파라미터 수를 감안하면 놀라운 수준입니다. 12억 파라미터는 스마트폰에서도 실행 가능한 수준의 크기입니다.

REASONING 모드에서 AIME 2025 45.2, LIVECODEBENCH V6 45.3을 달성하여, 파라미터가 약 2.4배인 SmolLM 3B(36.7, 29.1)를 크게 능가합니다. GPQA-DIAMOND 52.0으로 Qwen 3 1.7B(40.1)를 10% 이상 앞서며, 한국어 수학(KSM) 60.6으로 동급 최고입니다. 다만 EXAONE Deep 2.4B(2배 크기의 추론 전용 모델)에 비해서는 AIME(45.2 vs 47.9)에서 소폭 뒤처지는데, Hybrid 모델이 전용 Reasoning 모델 대비 약간의 성능 Trade-off가 있음을 보여줍니다.

NON-REASONING 모드에서도 대부분의 벤치마크에서 동급 최고 성능을 기록합니다. 특히 Long Context에서 RULER 77.4, KO-LONGBENCH 69.8로, 64K 토큰까지의 Long-context 처리 능력을 검증합니다. Qwen 3 0.6B의 KO-LONGBENCH 16.4와 비교하면 그 차이가 극명합니다.

다만 WMT24++(Spanish 번역 품질)에서는 65.9로 SmolLM 3B(84.0)에 크게 뒤처지며, 이는 스페인어 지원이 아직 초기 단계임을 시사합니다. TAU-BENCH(Airline) NON-REASONING에서도 10.0으로 낮은 성능을 보여, 소형 모델에서의 복잡한 Tool Use 시나리오는 여전히 도전적인 과제입니다.

### Reasoning Budget — 추론 비용과 성능의 Trade-off

REASONING 모드에서 모델은 최종 답변 전에 "생각하는 과정"(Thinking Token)을 생성합니다. 이 Thinking Token의 수를 제한하면 추론 비용(시간, 연산량)이 줄어들지만 성능도 영향을 받습니다. 이 Trade-off를 정량적으로 분석한 것이 Reasoning Budget 실험입니다.

Reasoning 토큰 수를 1K에서 64K까지 변화시키며 성능을 관찰한 결과는 실용적으로 의미 있는 시사점을 제공합니다. 모델의 생성이 최대 토큰 Budget에 도달하면, 강제로 생각을 마무리하고 답변을 생성하도록 유도합니다.

32B 모델에서 LIVECODEBENCH V6은 64K(66.7) → 32K(67.3)로 오히려 소폭 상승하고, 16K(53.0)에서 비로소 눈에 띄는 하락이 시작됩니다. 이는 코딩 문제의 상당수가 32K 이내의 사고만으로 충분히 해결 가능하며, 64K까지의 추가 사고가 반드시 도움이 되지는 않음을 시사합니다. AIME 2025는 64K(85.3) → 32K(74.8)로 약 12% 감소가 발생하지만, 이 수치도 여전히 Qwen 3 32B의 72.9를 상회합니다. 수학 올림피아드급 문제는 코딩보다 더 긴 추론 체인이 필요한 경향이 있어 Budget 감소에 더 민감한 것으로 보입니다.

1.2B 모델에서는 AIME 2025이 64K(45.2) → 32K(45.3)로 거의 동일하며, LIVECODEBENCH V6도 64K(45.3) → 32K(43.0)로 5% 이내의 하락에 그칩니다. 소형 모델은 애초에 64K에 가까운 매우 긴 추론 체인을 효과적으로 활용하기 어려우므로, 32K로 충분한 것으로 해석됩니다.

이 결과는 실제 서비스 배포 시 **32K Budget만으로도 대부분의 경우 충분한 성능을 확보**할 수 있음을 의미합니다. Reasoning Token이 줄어들면 추론 지연시간과 GPU 비용이 직접적으로 감소하므로, 이는 실시간 서비스에서의 비용 최적화에 바로 활용 가능한 인사이트입니다.

Limitations
-----------

논문에서 명시하는 한계점은 모든 LLM에 공통적인 것들을 포함합니다. 학습 데이터의 통계적 특성에 의존하여 부적절하거나 편향된(나이, 성별, 인종 등) 응답이 생성될 수 있으며, Knowledge Cut-off(2024년 11월) 이후의 정보는 반영되지 않습니다. 또한 확률 기반 텍스트 생성의 본질적 특성상 의미적/구문적으로 부정확한 문장이 생성될 가능성이 있습니다.

라이선스는 **EXAONE AI Model License Agreement 1.2 - NC**로, 연구 및 교육 목적으로만 사용 가능합니다. 상업적 활용에는 LG AI Research와의 별도 라이선스 계약이 필요하며, 특히 경쟁 모델 개발에 EXAONE 4.0의 모델이나 Output을 사용하는 것도 명시적으로 금지되어 있습니다. 오픈소스(Apache 2.0, MIT 등)와는 다른 제한적 라이선스이므로, 활용 시 주의가 필요합니다.

결론 및 시사점
--------

EXAONE 4.0은 "하나의 모델로 두 가지 모드"라는 Hybrid 패러다임의 실효성을 입증합니다. 32B 모델이 Math/Coding에서 7배 큰 Qwen 3 235B를 능가하고, 1.2B 모델이 3B급 모델을 상회하는 결과는 아키텍처 설계(Hybrid Attention, QK-Reorder-LN)와 Data Curation(14T 토큰, 도메인별 맞춤 데이터), 그리고 AGAPO를 통한 RL 최적화의 종합적 효과를 보여줍니다.

특히 AGAPO는 GRPO의 구체적 한계 — Clipped Objective의 탐색 억제, All-incorrect 샘플 폐기, 배치 분포 미반영 — 를 체계적으로 개선한 알고리즘으로, RL 기반 Reasoning 강화 연구에 실질적인 기여를 합니다. Hybrid Attention의 3:1 비율과 4K Window Size라는 구체적 설계 선택, Global Attention에서의 RoPE 제거 결정도 다른 모델 설계에 참고될 수 있는 실용적 지침입니다.

한국어 성능에서의 강점(KO-LONGBENCH 76.9, KSM 87.6)은 한국어 사용자 관점에서 뚜렷한 차별점이며, Agentic Tool Use의 도입은 LLM 기반 에이전트 개발의 기반을 마련합니다. 다만 비상업적 라이선스(NC)라는 제약과, Summarization/번역 등 일부 영역에서의 상대적 약점은 실제 활용 시 고려해야 할 요소입니다.

읽어주셔서 감사합니다