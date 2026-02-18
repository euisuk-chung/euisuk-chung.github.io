---
title: "[Paper Review] Qwen Technical Report"
date: "2025-08-29"
tags:
  - "paper-review"
year: "2025"
---

# [Paper Review] Qwen Technical Report

![](https://velog.velcdn.com/images/euisuk-chung/post/579f08e9-44bf-44e2-ad07-7d9ab9c8c731/image.png)

> <https://arxiv.org/abs/2309.16609>

```
BAI, Jinze, et al. Qwen technical report. arXiv preprint arXiv:2309.16609, 2023.
```

> 💡 QWEN은 중국어로 "천 개의 질문"을 의미하는 Qianwen의 별명입니다. "QWEN"의 발음은 맥락과 말하는 개인에 따라 달라질 수 있습니다. 한 가지 가능한 발음 방법은 /kwEn/입니다. ~~전 그냥 퀜이라고 부릅니다!~~ ㅎㅎ

초록
--

Large Language Model(LLM)들은 인공지능 분야를 혁신했으며, 이전에는 인간에게만 가능하다고 여겨졌던 자연어 처리 작업들을 가능하게 했습니다. 본 연구에서는 Large Language Model 시리즈의 첫 번째 버전인 QWEN¹을 소개합니다. QWEN은 다양한 parameter 수를 가진 개별 모델들을 포함하는 포괄적인 언어 모델 시리즈입니다. 여기에는 기본 사전 훈련된 언어 모델인 QWEN과 인간 정렬 기법으로 fine-tuning된 채팅 모델인 QWEN-CHAT이 포함됩니다. 기본 언어 모델들은 여러 downstream task에서 뛰어난 성능을 지속적으로 보여주며, 채팅 모델들, 특히 Reinforcement Learning from Human Feedback(RLHF)로 훈련된 모델들은 매우 경쟁력이 있습니다. 채팅 모델들은 agent application 생성을 위한 고급 tool 사용 및 계획 능력을 갖추고 있으며, code interpreter 활용과 같은 복잡한 작업에서도 더 큰 모델들과 비교했을 때 인상적인 성능을 보입니다. 또한, 기본 언어 모델을 바탕으로 구축된 코딩 전문 모델인 CODE-QWEN과 CODE-QWEN-CHAT, 그리고 수학 중심 모델인 MATH-QWEN-CHAT을 개발했습니다. 이들 모델은 오픈소스 모델들과 비교했을 때 현저히 향상된 성능을 보이며, 상용 모델들에는 약간 뒤처집니다.

1. 서론
-----

Large Language Model(LLM)(Radford et al., 2018; Devlin et al., 2018; Raffel et al., 2020; Brown et al., 2020; OpenAI, 2023; Chowdhery et al., 2022; Anil et al., 2023; Thoppilan et al., 2022; Touvron et al., 2023a;b)들은 복잡한 추론과 문제 해결 작업을 위한 강력한 기반을 제공함으로써 인공지능(AI) 분야를 혁신했습니다. 이들 모델은 방대한 지식을 신경망에 압축하는 능력을 가지고 있어, 매우 다양한 agent로 활용됩니다. 채팅 인터페이스를 통해 LLM들은 이전에는 인간의 전유물로 여겨졌던 작업들, 특히 창의성과 전문성이 필요한 작업들을 수행할 수 있습니다(OpenAI, 2022; Ouyang et al., 2022; Anil et al., 2023; Google, 2023; Anthropic, 2023a;b). 이들은 인간과 자연어 대화에 참여하고, 질문에 답하고, 정보를 제공하며, 심지어 이야기, 시, 음악과 같은 창작물을 생성할 수 있습니다. 이로 인해 챗봇과 가상 도우미부터 언어 번역과 요약 도구에 이르기까지 다양한 애플리케이션이 개발되었습니다.

LLM들은 언어 작업에만 제한되지 않습니다. 이들은 또한 일반적인 agent로서 기능하며(Reed et al., 2022; Bai et al., 2022a; Wang et al., 2023a; AutoGPT, 2023; Hong et al., 2023), 외부 시스템, 도구, 모델과 협력하여 인간이 설정한 목표를 달성합니다. 예를 들어, LLM들은 멀티모달 지시사항을 이해하고(OpenAI, 2023; Bai et al., 2023; Liu et al., 2023a; Ye et al., 2023; Dai et al., 2023; Peng et al., 2023b), 코드를 실행하며(Chen et al., 2021; Zheng et al., 2023; Li et al., 2023d), 도구를 사용할(Schick et al., 2023; LangChain, Inc., 2023; AutoGPT, 2023) 수 있습니다. 이는 자율주행차와 로봇공학부터 의료와 금융에 이르기까지 AI 애플리케이션의 완전히 새로운 가능성을 열어줍니다.

인상적인 능력에도 불구하고, LLM들은 재현성, 조작성, 그리고 서비스 제공업체에 대한 접근성이 부족하다는 비판을 받고 있습니다. 본 연구에서는 우리의 LLM 시리즈의 초기 버전인 QWEN을 소개하게 되어 기쁩니다. QWEN은 중국어로 "천 개의 질문"을 의미하는 Qianwen에서 파생된 이름으로, 다양한 질문을 수용한다는 개념을 전달합니다. QWEN은 다양한 parameter 수를 가진 개별 모델들을 포함하는 포괄적인 언어 모델 시리즈입니다. 모델 시리즈에는 기본 사전 훈련된 언어 모델들, 즉 supervised finetuning(SFT), reinforcement learning with human feedback(RLHF) 등의 인간 정렬 기법으로 fine-tuning된 채팅 모델들, 그리고 코딩 및 수학 전문 모델들이 포함됩니다.

2. 사전훈련 (Pretraining)
---------------------

사전훈련 단계에서는 방대한 양의 데이터를 학습하여 세상과 그 다양한 복잡성에 대한 포괄적인 이해를 습득합니다. 여기에는 기본적인 언어 능력뿐만 아니라 산술, 코딩, 논리적 추론과 같은 고급 기술도 포함됩니다.

### 2.1 데이터

데이터 크기는 견고한 Large Language Model을 개발하는 데 중요한 요소임이 이전 연구에서 강조되었습니다(Hoffmann et al., 2022; Touvron et al., 2023b). 효과적인 사전훈련 데이터셋을 만들기 위해서는 데이터가 다양하고 광범위한 유형, 도메인, 작업을 다루도록 하는 것이 필수적입니다. 우리의 데이터셋은 이러한 요구사항을 충족하도록 설계되었으며, 공개 웹 문서, 백과사전, 서적, 코드 등을 포함합니다. 또한, 우리의 데이터셋은 다국어이며, 영어와 중국어가 상당한 부분을 차지합니다.

사전훈련 데이터의 품질을 보장하기 위해 포괄적인 데이터 전처리 절차를 개발했습니다. 공개 웹 데이터의 경우, HTML에서 텍스트를 추출하고 언어 식별 도구를 사용하여 언어를 결정합니다. 데이터의 다양성을 높이기 위해 정규화 후 정확한 일치 중복 제거와 MinHash 및 LSH 알고리즘을 사용한 유사 중복 제거 기법을 적용합니다. 저품질 데이터를 필터링하기 위해 규칙 기반과 기계 학습 기반 방법의 조합을 사용합니다. 구체적으로, 언어 모델, 텍스트 품질 평가 모델, 그리고 잠재적으로 불쾌하거나 부적절한 내용을 식별하는 모델을 포함한 여러 모델을 사용하여 내용을 평가합니다.

### 2.2 토큰화 (Tokenization)

어휘 설계는 훈련 효율성과 downstream task 성능에 상당한 영향을 미칩니다. 본 연구에서는 GPT-3.5와 GPT-4를 따라 byte pair encoding(BPE)을 토큰화 방법으로 활용합니다. 오픈소스 fast BPE tokenizer인 tiktoken(Jain, 2022)을 시작점으로 하여 cl100k base 어휘를 선택합니다. 특히 중국어에서 다국어 downstream task에 대한 모델 성능을 향상시키기 위해 일반적으로 사용되는 중국어 문자와 단어, 그리고 다른 언어의 단어들로 어휘를 확장합니다. 또한 Touvron et al.(2023a;b)을 따라 숫자를 단일 자릿수로 분할합니다. 최종 어휘 크기는 약 152K입니다.

### 2.3 아키텍처

QWEN은 수정된 버전의 Transformer 아키텍처를 사용하여 설계되었습니다. 구체적으로, 최고의 오픈소스 LLM으로 널리 인정받는 LLaMA(Touvron et al., 2023a)의 최근 오픈소스 접근법을 채택했습니다. 아키텍처에 대한 수정사항은 다음과 같습니다:

* **임베딩 및 출력 프로젝션**: 예비 실험 결과를 바탕으로, 메모리 비용이라는 대가를 치르더라도 더 나은 성능을 달성하기 위해 입력 임베딩과 출력 프로젝션의 가중치를 연결하지 않는 untied embedding 접근법을 선택했습니다.
* **위치 임베딩**: 모델에 위치 정보를 통합하기 위한 선호 옵션으로 RoPE(Rotary Positional Embedding)(Su et al., 2021)를 선택했습니다. RoPE는 널리 채택되었으며 현대 Large Language Model, 특히 PaLM(Chowdhery et al., 2022; Anil et al., 2023)과 LLaMA(Touvron et al., 2023a;b)에서 성공을 입증했습니다.
* **바이어스**: Chowdhery et al.(2022)을 따라 대부분의 층에서 바이어스를 제거했지만, 모델의 외삽 능력을 향상시키기 위해 attention의 QKV layer에는 바이어스를 추가했습니다(Su, 2023b).
* **Pre-Norm & RMSNorm**: 현대 Transformer 모델에서 pre-normalization이 가장 널리 사용되는 접근법으로, post-normalization과 비교했을 때 훈련 안정성을 향상시키는 것으로 나타났습니다. 또한 Ba et al.(2016)에서 설명된 전통적인 layer normalization 기법을 RMSNorm(Jiang et al., 2023)으로 교체했습니다.
* **활성화 함수**: Swish(Ramachandran et al., 2017)와 Gated Linear Unit(Dauphin et al., 2017)의 조합인 SwiGLU(Shazeer, 2020)를 활성화 함수로 선택했습니다.

### 2.4 훈련

QWEN을 훈련하기 위해 Radford et al.(2018)에서 설명된 자동회귀 언어 모델링의 표준 접근법을 따릅니다. 이는 이전 토큰들이 제공하는 맥락을 바탕으로 다음 토큰을 예측하도록 모델을 훈련시키는 것입니다. 2048의 맥락 길이로 모델을 훈련합니다. 데이터 배치를 생성하기 위해 문서들을 섞고 병합한 후, 지정된 맥락 길이로 자릅니다. 계산 효율성을 향상시키고 메모리 사용량을 줄이기 위해 attention 모듈에서 Flash Attention을 사용합니다(Dao et al., 2022). 사전훈련 최적화를 위해 표준 optimizer인 AdamW(Kingma & Ba, 2014; Loshchilov & Hutter, 2017)를 채택합니다.

### 2.5 맥락 길이 확장

Transformer 모델들은 attention 메커니즘의 맥락 길이에 상당한 제약이 있습니다. 맥락 길이가 증가함에 따라 quadratic-complexity 계산이 계산 및 메모리 비용을 급격히 증가시킵니다. 본 연구에서는 추론 중에만 적용되는 간단한 훈련 없는 기법들을 구현하여 모델의 맥락 길이를 확장했습니다. 우리가 사용한 주요 기법 중 하나는 NTK-aware interpolation(bloc97, 2023)입니다.

### 2.6 실험 결과

모델들의 zero-shot 및 few-shot 학습 능력을 평가하기 위해 일련의 데이터셋을 사용한 철저한 benchmark 평가를 수행했습니다. QWEN을 최근 오픈소스 기본 모델들과 비교했으며, 여기에는 LLaMA(Touvron et al., 2023a), LLAMA 2(Touvron et al., 2023b), MPT(Mosaic ML, 2023), Falcon(Almazrouei et al., 2023) 등이 포함됩니다.

평가는 7개의 인기 있는 benchmark를 다루며, 이는 MMLU(5-shot)(Hendrycks et al., 2020), C-Eval(5-shot)(Huang et al., 2023), GSM8K(8-shot)(Cobbe et al., 2021), MATH(4-shot)(Hendrycks et al., 2021), HumanEval(0-shot)(Chen et al., 2021), MBPP(0-shot)(Austin et al., 2021), 그리고 BBH(Big Bench Hard)(3 shot)(Suzgun et al., 2022)입니다.

실험 결과는 세 개의 QWEN 모델들이 모든 downstream task에서 탁월한 성능을 보임을 보여줍니다. 주목할 점은 LLaMA2-70B와 같은 더 큰 모델들조차 QWEN-14B에 의해 3개 작업에서 압도당한다는 것입니다. QWEN-7B도 훌륭한 성능을 보이며, LLaMA2-13B를 능가하고 Baichuan2-13B와 비슷한 결과를 달성합니다.

3. 정렬 (Alignment)
-----------------

사전훈련된 Large Language Model들은 인간 행동과 정렬되지 않는 것으로 밝혀졌으며, 대부분의 경우 AI 도우미로 사용하기에 부적합합니다. 최근 연구에 따르면 supervised finetuning(SFT)과 reinforcement learning from human feedback(RLHF)와 같은 정렬 기법의 사용이 언어 모델들의 자연스러운 대화 능력을 크게 향상시킬 수 있습니다.

### 3.1 Supervised Finetuning

인간 행동을 이해하기 위한 첫 번째 단계는 사전훈련된 LLM을 질의와 응답을 모두 포함하는 채팅 스타일 데이터에 대해 fine-tuning하는 SFT를 수행하는 것입니다.

#### 3.1.1 데이터

Supervised finetuning 데이터셋의 능력을 향상시키기 위해 여러 스타일의 대화를 주석으로 달았습니다. 기존 데이터셋들(Wei et al., 2022a)이 자연어로 된 질문, 지시사항, 답변으로 구성된 방대한 양의 데이터를 포함하는 반면, 우리의 접근법은 인간 스타일의 대화를 주석으로 다는 것까지 더 나아갑니다. Ouyang et al.(2022)에서 영감을 받은 이러한 관행은 다양한 작업에 대한 자연어 생성에 초점을 맞춤으로써 모델의 유용성을 향상시키는 것을 목표로 합니다.

#### 3.1.2 훈련

사전훈련과 일관되게, SFT를 위한 훈련 작업으로도 다음 토큰 예측을 적용합니다. 시스템과 사용자 입력에 대해 loss mask를 적용합니다. 모델의 훈련 과정은 AdamW optimizer를 활용하며, hyperparameter는 β1을 0.9로, β2를 0.95로, ε을 10⁻⁸로 설정합니다. sequence length는 2048로 제한되고, batch size는 128입니다.

### 3.2 Reinforcement Learning from Human Feedback

SFT가 효과적임이 입증되었지만, 일반화 및 창의성 능력이 제한적이고 overfitting에 취약할 수 있음을 인정합니다. 이 문제를 해결하기 위해 Ouyang et al.(2022); Christiano et al.(2017)의 접근법을 따라 SFT 모델들을 인간 선호도와 더 잘 정렬하기 위해 Reinforcement Learning from Human Feedback(RLHF)을 구현했습니다.

#### 3.2.1 Reward Model

성공적인 reward model을 만들기 위해서는 Large Language Model(LLM)을 구축하는 것처럼 먼저 사전훈련을 거친 후 fine-tuning을 해야 합니다. preference model pretraining(PMP)(Bai et al., 2022b)로 알려진 이 사전훈련 과정에는 비교 데이터의 방대한 데이터셋이 필요합니다. 이 데이터셋은 단일 질의에 대한 두 개의 서로 다른 응답과 해당 선호도를 포함하는 샘플 쌍들로 구성됩니다.

Fine-tuning 단계에서는 다양한 prompt들을 수집하고 QWEN 모델들로부터의 응답에 대한 인간 피드백을 바탕으로 reward model을 조정합니다. 사용자 prompt들의 다양성과 복잡성이 적절히 고려되도록 하기 위해 약 6600개의 상세한 태그를 가진 분류 시스템을 만들고, reward model의 주석을 위한 prompt를 선택할 때 다양성과 복잡성을 모두 고려하는 균형 잡힌 샘플링 알고리즘을 구현했습니다.

#### 3.2.2 강화학습

우리의 Proximal Policy Optimization(PPO) 과정에는 네 개의 모델이 관련됩니다: policy model, value model, reference model, 그리고 reward model입니다. PPO 절차를 시작하기 전에 policy model의 업데이트를 일시 중지하고 50 step 동안 value model 업데이트에만 집중합니다.

PPO 작업 중에는 각 질의에 대해 동시에 두 개의 응답을 샘플링하는 전략을 사용합니다. 이 전략은 내부 benchmark 평가를 바탕으로 더 효과적임이 입증되었습니다. KL divergence 계수를 0.04로 설정하고 실행 평균을 바탕으로 reward를 정규화합니다.

### 3.3 정렬된 모델들의 자동 및 인간 평가

정렬된 모델들의 효과를 보여주기 위해 MMLU(Hendrycks et al., 2020), C-Eval(Huang et al., 2023), GSM8K(Cobbe et al., 2021), HumanEval(Chen et al., 2021), BBH(Suzgun et al., 2022)를 포함한 잘 확립된 benchmark들에서 다른 정렬된 모델들과 비교를 수행했습니다.

결과는 인간의 지시사항을 이해하고 적절한 응답을 생성하는 데 있어서 우리의 정렬된 모델들의 효과를 보여줍니다. QWEN-14B-Chat은 모든 데이터셋에서 ChatGPT(OpenAI, 2022)와 LLAMA 2-CHAT-70B(Touvron et al., 2023b)를 제외한 모든 다른 모델들을 능가합니다.

인간 평가를 위해 지식, 언어 이해, 창의적 글쓰기, 코딩, 수학을 포함한 다양한 주제를 다루는 300개의 중국어 지시사항으로 구성된 신중하게 선별된 데이터셋을 만들었습니다. 실험 결과는 RLHF 모델이 SFT 모델들보다 상당한 차이로 우수한 성능을 보임을 명확히 보여주며, 이는 RLHF가 모델이 인간에게 더 선호되는 응답을 생성하도록 격려할 수 있음을 나타냅니다.

### 3.4 Tool Use, Code Interpreter, 그리고 Agent

다용도로 설계된 QWEN 모델들은 tool 사용과 계획 기술을 활용하여 일상 작업을 (반)자동화하는 데 도움을 주는 뛰어난 능력을 가지고 있습니다. 따라서 이들은 다양한 작업을 간소화하는 데 도움이 되는 agent나 부조종사 역할을 할 수 있습니다. 우리는 QWEN의 다음 영역에서의 숙련도를 탐구합니다:

* ReAct prompting을 통한 처음 보는 도구 활용(Yao et al., 2022)
* 수학 추론, 데이터 분석 등을 향상시키기 위한 Python code interpreter 사용
* 인간과 상호작용하면서 Hugging Face의 방대한 멀티모달 모델 컬렉션에 접근하는 agent로서 기능

QWEN의 agent나 부조종사로서의 능력을 향상시키기 위해 SFT에 self-instruct(Wang et al., 2023c) 전략을 사용합니다. 구체적으로, self-instruction을 위해 QWEN의 in-context learning 능력을 활용합니다. 몇 가지 예시를 제공함으로써 QWEN이 더 관련성 있는 질의를 생성하고 ReAct(Yao et al., 2022)와 같은 특정 형식을 따르는 출력을 생성하도록 유도할 수 있습니다.

4. CODE-QWEN: 코딩 전문 모델
----------------------

도메인별 데이터에 대한 훈련은 특히 코드 사전훈련과 fine-tuning의 경우에 매우 효과적임이 입증되었습니다. 코드 데이터로 강화된 훈련을 받은 언어 모델은 코딩, 디버깅, 해석 등의 작업에 유용한 도구 역할을 할 수 있습니다. 본 연구에서는 사전훈련과 정렬 기법을 사용하여 일련의 일반주의 모델들을 개발했습니다. 이 기반 위에 QWEN의 기본 언어 모델들을 활용하여 코딩을 위한 도메인별 모델들을 만들었으며, 여기에는 지속적인 사전훈련 모델인 CODE-QWEN과 supervised fine-tuning 모델인 CODE-QWEN-CHAT이 포함됩니다. 두 모델 모두 140억 및 70억 parameter 버전이 있습니다.

### 4.1 코드 사전훈련

코드 데이터만으로 사전훈련에 의존하는 것은 다용도 도우미로서 기능하는 능력을 상당히 상실시킬 수 있다고 생각합니다. 코드 데이터만으로 사전훈련에 초점을 맞춘 이전 접근법들과는 달리(Li et al., 2022; 2023d), 우리는 텍스트와 코드 데이터의 조합으로 훈련된 기본 모델 QWEN에서 시작하여 코드 데이터로 사전훈련을 계속하는 다른 접근법(Roziere et al., 2023)을 취합니다. 총 약 900억 개의 토큰으로 모델을 계속 사전훈련합니다.

### 4.2 코드 Supervised Fine-tuning

일련의 실험적 실험을 수행한 후, 다단계 SFT 전략이 다른 방법들과 비교했을 때 최고의 성능을 산출함을 확인했습니다. supervised fine-tuning 단계에서 코드 기반 모델 CODE-QWEN으로 초기화된 모델 CODE-QWEN-CHAT은 AdamW(Kingma & Ba, 2014; Loshchilov & Hutter, 2017) optimizer로 최적화됩니다.

### 4.3 평가

CODE-QWEN 모델들을 상용 및 오픈소스 언어 모델들과 비교했습니다. 이 비교는 HumanEval(Chen et al., 2021), MBPP(Austin et al., 2021), 그리고 다국어 코드 생성 benchmark인 HUMANEVALPACK(Muennighoff et al., 2023)의 테스트 셋에서의 pass@1 성능을 기반으로 합니다.

분석 결과 특수 모델들, 특히 CODE-QWEN과 CODE-QWEN-CHAT이 유사한 parameter 수를 가진 이전 baseline들을 크게 능가함을 보여줍니다. 실제로, 이들 모델은 Starcoder(Li et al., 2023d)와 같은 더 큰 모델들의 성능과도 경쟁합니다.

5. MATH-QWEN: 수학적 추론 전문 모델
--------------------------

QWEN 사전훈련된 언어 모델들을 기반으로 구축된 수학 전문 모델 시리즈인 MATH-QWEN-CHAT을 만들었습니다. 구체적으로, 산술과 수학에서 뛰어난 성능을 보이고 인간 행동과 정렬된 도우미 모델들을 개발했습니다. 140억과 70억 parameter를 각각 가진 두 가지 버전인 MATH-QWEN-14B-CHAT과 MATH-QWEN-7B-CHAT을 출시합니다.

### 5.1 훈련

수학적 추론을 위해 확장된 수학 지도 데이터셋에서 math SFT를 수행하여 채팅 모델인 MATH-QWEN-CHAT을 직접 획득합니다. math SFT 데이터의 평균 길이가 더 짧기 때문에 더 빠른 훈련을 위해 sequence length 1024를 사용합니다.

### 5.2 평가

GSM8K(Grade school math)(Cobbe et al., 2021), MATH(Challenging competition math problems)(Hendrycks et al., 2021), Math401(Arithmetic ability)(Yuan et al., 2023b), Math23K(Chinese grade school math)(Wang et al., 2017)의 테스트 셋에서 모델들을 평가합니다.

MATH-QWEN-CHAT 모델들은 유사한 크기의 오픈소스 모델들 및 QWEN-CHAT 모델들과 비교했을 때 더 나은 수학적 추론과 산술 능력을 보여줍니다. 상용 모델들과 비교했을 때, MATH-QWEN-7B-CHAT은 MATH에서 Minerva-8B를 능가합니다. MATH-QWEN-14B-CHAT은 GSM8K와 MATH에서 Minerva-62B와 GPT-3.5를 추격하고 있으며, 산술 능력과 중국 수학 문제에서 더 나은 성능을 보입니다.

6. 관련 연구
--------

### 6.1 Large Language Models

LLM의 흥미는 Transformer 아키텍처(Vaswani et al., 2017)의 도입으로 시작되었으며, 이는 Radford et al.(2018); Devlin et al.(2018); Liu et al.(2019) 등의 연구자들에 의해 대규모 데이터 사전훈련에 적용되었습니다. ChatGPT(OpenAI, 2022)의 탄생과 이후 GPT-4(OpenAI, 2023)의 출시는 인공지능 분야에서 두 개의 역사적 순간을 기록했으며, Large Language Model(LLM)들이 인간과 소통할 수 있는 효과적인 AI 도우미로 기능할 수 있음을 보여주었습니다.

### 6.2 정렬

커뮤니티는 LLM에 대한 정렬의 놀라운 효과에 깊은 인상을 받았습니다. 이전에는 정렬 없는 LLM들이 종종 반복적인 생성, 환각, 인간 선호도로부터의 일탈과 같은 문제들로 어려움을 겪었습니다. 2021년 이후, 연구자들은 downstream task에서 LLM의 성능을 향상시키는 방법을 개발하기 위해 부지런히 노력해왔습니다.

### 6.3 Tool Use와 Agents

LLM의 계획 기능을 통해 Schick et al.(2023)이 보여준 바와 같이 in-context learning을 통해 API나 agent 능력과 같은 도구를 호출할 수 있습니다. Yao et al.(2022)은 모델이 어떤 도구를 사용할지에 대한 생각을 생성하고, API 관찰로부터의 입력을 받아들이며, 응답을 생성할 수 있게 하는 생성 형식인 ReAct를 도입했습니다.

### 6.4 코딩을 위한 LLM

이전 연구들은 LLM들이 특히 방대한 수의 parameter를 가진 모델들에서 코드 이해와 생성에서 뛰어난 능력을 가지고 있음을 보여주었습니다(Chowdhery et al., 2022; Anil et al., 2023; Rae et al., 2021; Hoffmann et al., 2022). 또한, 여러 LLM들이 코딩 관련 데이터에 대해 사전훈련, 지속적인 사전훈련, 또는 fine-tuning되어 일반 목적 LLM들과 비교했을 때 현저히 향상된 성능을 얻었습니다.

### 6.5 수학을 위한 LLM

특정 모델 규모를 가진 LLM들이 수학적 추론을 수행하는 능력을 가지고 있음이 발견되었습니다(Wei et al., 2022b; Suzgun et al., 2022). 수학 관련 작업에서 LLM들이 더 나은 성능을 달성하도록 격려하기 위해, 연구자들은 chain-of-thought prompting(Wei et al., 2022c)과 scratchpad(Nye et al., 2021) 같은 기법들을 사용했으며, 이는 유망한 결과를 보여주었습니다.

7. 결론
-----

본 보고서에서는 자연어 처리 분야의 최신 발전을 보여주는 QWEN 시리즈의 Large Language Model들을 소개합니다. 140억, 70억, 18억 parameter를 가진 이들 모델은 수조 개의 토큰을 포함한 방대한 양의 데이터로 사전훈련되었으며, SFT와 RLHF와 같은 최첨단 기법을 사용하여 fine-tuning되었습니다.

또한, QWEN 시리즈에는 CODE-QWEN, CODE-QWEN-CHAT, MATH-QWEN-CHAT과 같은 코딩과 수학을 위한 전문 모델들이 포함되어 있으며, 이들은 각각의 분야에서 뛰어난 성능을 보이기 위해 도메인별 데이터로 훈련되었습니다. 우리의 결과는 QWEN 시리즈가 기존 오픈소스 모델들과 경쟁력이 있으며, 포괄적인 benchmark와 인간 평가에서 일부 상용 모델들의 성능과도 일치함을 보여줍니다.

우리는 QWEN의 개방적 접근이 커뮤니티 내에서 협력과 혁신을 촉진하여, 연구자들과 개발자들이 우리의 작업을 기반으로 삼아 언어 모델로 가능한 것의 경계를 넓히게 될 것이라고 믿습니다. 이들 모델을 공개함으로써, 우리는 이 분야를 더욱 발전시키고 현실적인 설정에서 도입된 변수와 기법들에 대한 우리의 이해에 기여할 새로운 연구와 애플리케이션을 영감을 주기를 희망합니다.