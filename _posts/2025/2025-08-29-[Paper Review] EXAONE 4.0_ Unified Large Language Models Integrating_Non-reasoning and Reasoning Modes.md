---
title: "[Paper Review] EXAONE 4.0: Unified Large Language Models Integrating
Non-reasoning and Reasoning Modes"
date: "2025-08-29"
year: "2025"
---

# [Paper Review] EXAONE 4.0: Unified Large Language Models Integrating
Non-reasoning and Reasoning Modes


![](https://velog.velcdn.com/images/euisuk-chung/post/e106b46f-38f9-428c-82e7-d8872d22e773/image.png)

> <https://arxiv.org/pdf/2507.11407>

```
RESEARCH, L. G., et al. EXAONE 4.0: Unified Large Language Models Integrating Non-reasoning and Reasoning Modes. arXiv preprint arXiv:2507.11407, 2025.
```

**핵심 기여도 분석**
-------------

### **해결하려는 문제**

기존 EXAONE 3.5는 실용적 활용성에 중점을 두었고, EXAONE Deep은 수학·코딩 영역의 추론 성능에 집중했습니다.  
하지만 각각 별도의 모델로 제공되어 사용자가 두 가지 능력을 모두 활용하기 위해서는 여러 모델을 사용해야 하는 불편함이 있었습니다.

### **제안하는 해결책의 독창성**

EXAONE 4.0은 **NON-REASONING 모드**와 **REASONING 모드**를 단일 모델에 통합한 hybrid 아키텍처를 제안합니다. 주요 혁신사항은:

* **Hybrid Attention 메커니즘**: 전역 attention과 지역 attention을 3:1 비율로 결합
* **QK-Reorder-LN**: Query와 Key 입력 후 LayerNorm을 적용하는 새로운 정규화 방법
* **통합 모드 훈련**: 두 모드를 순차적이 아닌 동시에 훈련하는 방법론
* **AGAPO 알고리즘**: 기존 GRPO를 개선한 강화학습 알고리즘

---

**📖 Chapter 1: Introduction**
-----------------------------

### **챕터의 위치와 역할**

서론 챕터는 EXAONE 4.0의 개발 배경과 목적, 주요 특징을 포괄적으로 제시하여 전체 논문의 방향성을 설정합니다.

### **저자의 서술 순서를 따른 상세 내용:**

**1. EXAONE 시리즈의 발전 과정**  
LG AI Research의 EXAONE foundation model 시리즈는 강력한 instruction-following과 추론 능력을 통해 다양한 실제 애플리케이션을 지원하도록 개발되었습니다. 이전 버전인 EXAONE 3.5는 포괄적인 instruction-following 능력을 강화하여 실제 활용성에 집중했으며, EXAONE Deep은 수학 및 코딩 영역에서의 추론 성능을 강조했습니다.

**2. Agentic AI 시대를 위한 새로운 기능**  
다가오는 agentic AI 시대를 염두에 두고, EXAONE 4.0은 이 패러다임의 핵심 능력인 agentic tool use를 도입하고 추론 능력을 더욱 발전시켰습니다.

**3. 모드 통합의 혁신**  
EXAONE 4.0은 빠른 사고와 응답을 가능하게 하는 **NON-REASONING 모드**와 깊은 사고와 더 정확한 답변을 위한 **REASONING 모드**를 단일 모델에 통합했습니다.

**4. 데이터와 컨텍스트 확장**  
사전 훈련에 사용되는 토큰 수를 대폭 증가시켜 세계 지식을 강화했으며, STEM 분야의 전문 도메인 데이터 큐레이션이 downstream 작업에서 중요한 역할을 합니다. 모델의 최대 컨텍스트 길이를 128K 토큰까지 확장하여 긴 컨텍스트 기반 작업의 유용성을 향상시켰습니다.

**5. Hybrid Attention 아키텍처**  
긴 컨텍스트 처리 시 attention 계산의 계산 부담을 완화하기 위해 전역 attention과 지역 attention을 결합한 hybrid 아키텍처를 채택했습니다.

**6. 다국어 지원 확장**  
EXAONE 4.0은 기존의 영어와 한국어 지원에 더해 **스페인어**를 공식적으로 추가했습니다.

**챕터의 핵심 기여**: EXAONE 4.0의 전체적인 비전과 주요 혁신사항 제시  
**다음 챕터로의 연결**: 구체적인 모델링 방법론으로 이어짐

---

**📖 Chapter 2: Modeling**
-------------------------

### **챕터의 위치와 역할**

모델링 챕터는 EXAONE 4.0의 기술적 구현 세부사항을 체계적으로 설명하는 핵심 장으로, 모델 구성부터 후처리 훈련까지 전 과정을 다룹니다.

### **2.1 Model Configurations**

**Hybrid Attention 메커니즘의 도입**  
EXAONE 4.0은 이전 EXAONE 3.5 모델과 유사한 구조적 프레임워크를 유지하지만, attention 메커니즘에서 주요한 변화를 보입니다. EXAONE 3.5에서는 모든 레이어가 전역 attention을 사용했지만, EXAONE 4.0은 지역 attention(sliding window attention)과 전역 attention을 3:1 비율로 결합한 hybrid attention 메커니즘을 사용합니다.

**설계 원리와 이론적 배경**  
최근 연구들은 더 큰 window 크기(예: 512에서 1,024 또는 4,096)를 사용하고 소수의 레이어에만 전역 attention을 적용해도 우수한 long-context 성능을 달성할 수 있음을 보여주었습니다. EXAONE 4.0 설계에서는 단문맥 성능에 대한 부정적 영향을 최소화하기 위해 4K의 sliding window 크기를 선택했습니다.

**RoPE와 Attention 설계**  
전역 attention에서는 Rotary Position embedding을 사용하지 않아 모델이 길이에 대한 편향을 갖지 않고 global view를 유지할 수 있도록 합니다. 지역 attention 메커니즘 설계에서는 chunked attention 전략 대신 이론적 안정성이 강한 sliding window attention을 채택했습니다.

### **QK-Reorder-LN 정규화 방법**

**기존 문제점과 해결책**  
최근 연구에 따르면 모델 성능에 크게 영향을 주지 않는 일부 레이어들이 주로 깊은 레이어에서 발견됩니다. 이는 안정성을 향상시키지만 모델 깊이가 증가함에 따라 출력의 분산이 지수적으로 증가하는 Pre-LN transformer 아키텍처에 기인합니다.

**QK-Reorder-LN의 구현**  
입력 query와 key 후에 LayerNorm을 적용하고, attention 출력 후에 다시 LayerNorm을 수행하는 QK-Reorder-LN 방법이 더 많은 계산을 소모하지만 downstream 작업에서 더 나은 성능을 제공합니다.

### **모델 구성 세부사항**

EXAONE 4.0 모델 시리즈는 32B와 1.2B 두 가지 구성으로 제공됩니다:

**32B 모델 사양:**

* d\_model: 5,120
* 레이어 수: 64
* Attention 타입: Hybrid
* Head 타입: GQA (Grouped Query Attention)
* 최대 시퀀스 길이: 131,072

**1.2B 모델 사양:**

* d\_model: 2,048
* 레이어 수: 30
* Attention 타입: Global
* Head 타입: GQA
* 최대 시퀀스 길이: 65,536

### **2.2 Pre-training**

**데이터 규모의 대폭 확장**  
EXAONE 3.5 32B 모델이 6.5조 토큰으로 사전 훈련된 것에 비해, EXAONE 4.0 32B 모델은 이를 두 배로 늘린 **14조 토큰**으로 사전 훈련되었습니다. 이러한 데이터 증가는 모델의 세계 지식 향상을 목표로 합니다.

**인지 행동 기반 데이터 큐레이션**  
최근 연구에서 추론 성능이 사전 훈련 중 문서에서 습득한 인지 행동에 의해 크게 영향을 받는다는 것이 밝혀짐에 따라, 후처리 훈련 성능을 향상시키기 위해 사전 훈련 중 엄격한 데이터 큐레이션을 수행했습니다.

### **2.3 Context Length Extension**

**2단계 확장 프로세스**  
EXAONE 4.0에서는 최대 컨텍스트 길이를 128K 토큰까지 확장하기 위해 2단계 컨텍스트 길이 확장 프로세스를 수행합니다:  
1. 4K 토큰으로 사전 훈련된 모델을 32K 토큰으로 확장  
2. 이후 128K 토큰까지 추가 확장

**NIAH 테스트를 통한 검증**  
각 단계에서 Needle In A Haystack (NIAH) 테스트를 통해 모델의 성능을 철저히 검증하며, 모든 세그먼트에서 일관되게 "녹색 신호"가 관찰될 때까지 반복적으로 개선합니다.

### **2.4 Post-training**

**3단계 훈련 파이프라인**  
EXAONE 4.0의 후처리 훈련은 다양한 사용자 지시에 응답하고 NON-REASONING과 REASONING 모델을 효과적으로 통합하기 위해 여러 단계로 구성됩니다:  
1. **Supervised Fine-tuning (SFT)**  
2. **Reasoning Reinforcement Learning (RL)**  
3. **Preference Learning** (NON-REASONING과 REASONING 모드 통합)

### **2.4.1 Large-scale Supervised Fine-tuning**

**5개 도메인별 데이터 구성**  
SFT 데이터셋은 non-reasoning과 reasoning 데이터로 나누어지며, 5개 영역으로 분류됩니다:

**World Knowledge 도메인**  
광범위한 분야와 난이도 수준을 포괄하는 세계 지식 도메인에서는 교육적 가치를 기준으로 웹 소스에서 수집한 문제를 필터링하여 고품질 데이터를 우선 활용합니다.

**Math, Code, Logic 도메인**  
이 영역에서는 정확한 ground truth 설정이 필수적이지만 어려워 고품질 문제 수가 상대적으로 제한적입니다. 따라서 검증 가능한 답변을 가진 쿼리에 대해 다양한 응답을 훈련하며, 고유한 쿼리 수를 늘리는 것만큼 쿼리당 여러 응답을 생성하는 것이 효과적임을 관찰했습니다.

**Long Context 도메인**  
웹 코퍼스에서 확장된 입력의 포괄적 이해가 필요한 작업에 중점을 둔 long-context SFT 데이터셋을 구성합니다. 분산된 정보를 식별하고 추론할 수 있도록 컨텍스트 길이와 핵심 콘텐츠의 위치를 체계적으로 변화시킵니다.

**Agentic Tool Use 도메인**  
모델의 agentic tool use 능력 향상을 위해 단순한 single tool call 데이터셋 생성을 넘어 복잡한 long-horizon tool-calling 데이터 구성을 강조합니다. 사용자-에이전트 대화에 사용자 상호작용, 환경으로부터의 실행 피드백, 반복적 추론을 포함시켜 에이전트가 사용자의 원하는 목표를 달성하도록 안내합니다.

**Multilinguality 도메인**  
한국어와 스페인어 지원을 위해 각 언어별 문화적, 역사적 지식을 대상으로 하는 데이터셋을 구성할 뿐만 아니라 사용자와의 유창하고 자연스러운 대화를 가능하게 합니다.

**통합 모드 훈련**  
결합된 데이터셋에서 NON-REASONING 데이터는 주로 다양한 작업으로 구성되고, REASONING 데이터는 수학과 코드 도메인을 중심으로 합니다. 두 모드를 순차적으로 fine-tuning하는 대신 결합하여 함께 훈련합니다. 토큰 비율 연구를 통해 REASONING 대 NON-REASONING 데이터 비율을 1.5:1로 설정했습니다.

### **2.4.2 Reasoning Reinforcement Learning**

**AGAPO 알고리즘 개발**  
모델의 추론 능력 향상을 위해 SFT 후 온라인 강화학습을 수행합니다. 기존 GRPO 알고리즘의 한계를 해결하기 위해 **AGAPO (Asymmetric Sampling and Global Advantage Policy Optimization)**라는 새로운 알고리즘을 제안합니다.

**AGAPO의 주요 특징:**

**1. Remove Clipped Objective**  
PPO의 clip loss가 추론 경로의 분기점 역할을 하는 반성적 행동과 관련된 중요한 저확률 토큰의 기여도를 떨어뜨릴 수 있다는 이전 연구를 바탕으로, AGAPO는 PPO에서 clipping을 제거하고 표준 policy gradient loss를 사용합니다.

**2. Asymmetric Sampling**  
모든 응답이 틀린 샘플도 버리지 않고 더 높은 비율의 부정적 피드백을 포함시키는 비대칭 샘플링 방법을 활용합니다.

**3. Group & Global Advantages**  
GRPO의 advantage 방법이 전체 배치의 분포를 고려하지 않는 문제를 개선하기 위해, AGAPO는 그룹 단계와 전역 단계의 2단계로 advantage를 계산합니다.

**4. Sequence Level Cumulative KL**  
SFT 단계에서 학습한 능력을 보존하면서 성능을 향상시키기 위해 sequence-level cumulative KL penalty를 적용합니다.

**목적 함수**  
AGAPO 목적 함수는 다음과 같이 정의됩니다:

JAGAPO(θ)=Eq∼P(Q),{oi}i=1G∼πθ(O∣q)[1G∑i=1G(Aglobal,ilog⁡πθ(oi∣q)−βDKL[πθ,πref])]J\_{AGAPO}(\theta) = \mathbb{E}\_{q \sim P(Q), \{o\_i\}\_{i=1}^G \sim \pi\_\theta(O|q)} \left[ \frac{1}{G} \sum\_{i=1}^G \left( A\_{global,i} \log \pi\_\theta(o\_i|q) - \beta D\_{KL}[\pi\_\theta, \pi\_{ref}] \right) \right]JAGAPO​(θ)=Eq∼P(Q),{oi​}i=1G​∼πθ​(O∣q)​[G1​∑i=1G​(Aglobal,i​logπθ​(oi​∣q)−βDKL​[πθ​,πref​])]

### **2.4.3 Preference Learning with Hybrid Reward**

**2단계 Preference Learning**  
RL 단계에서는 검증 가능한 보상을 통해 정확도 향상을 목표로 하지만, 다른 유형의 작업에서 성능 저하가 관찰됩니다. 이를 극복하기 위해 추가적인 preference learning 단계를 도입합니다.

**1단계: 정확성과 간결성**  
추론 관련 검증 가능한 훈련 데이터에 대해 검증 가능한 보상과 간결성 보상을 결합하여 정답 중 가장 짧은 응답을 선택된 옵션으로 선택합니다.

**2단계: 언어 일관성과 선호도**  
인간 정렬을 위해 선호도 보상과 언어 일관성 보상의 조합을 사용합니다. REASONING 모드 데이터의 경우 추론 과정이 완료된 후 최종 답변에서만 선호도 라벨링을 수행합니다.

**챕터의 핵심 기여**: 모델 아키텍처와 훈련 방법론의 상세한 기술적 구현  
**다음 챕터로의 연결**: 이론적 설계가 실제 성능으로 어떻게 구현되는지 평가 결과로 이어짐

---

**📖 Chapter 3: Evaluation**
---------------------------

### **챕터의 위치와 역할**

평가 챕터는 EXAONE 4.0의 이론적 설계와 구현이 실제 성능으로 어떻게 나타나는지 체계적으로 검증하는 핵심 장입니다.

### **3.1 Benchmarks**

**6개 카테고리별 평가 체계**  
EXAONE 4.0을 6개 카테고리의 다양한 벤치마크로 평가합니다:

**World Knowledge**

* **MMLU-REDUX**: MMLU의 개선 및 확장 버전
* **MMLU-PRO**: 더욱 견고하고 도전적인 다중 작업 언어 이해 벤치마크
* **GPQA-DIAMOND**: 생물학, 물리학, 화학 분야의 전문가 수준 지식 평가

**Math/Coding**

* **AIME 2025**: 수학 올림피아드 경시 대회
* **HMMT FEB 2025**: 하버드-MIT 수학 토너먼트
* **LIVECODEBENCH V5/V6**: 라이브 코딩 능력 평가

**Instruction Following**

* **IFEVAL**: 지시 준수 능력 평가
* **MULTI-IF**: 다중 턴 및 다국어 시나리오로 확장된 IFEVAL

**Long Context**

* **HELMET**: 합성 작업과 실제 시나리오를 포괄하는 long-context 이해 능력
* **RULER**: 다양한 측면의 long-context 이해 평가
* **LONGBENCH**: 이중 언어 long-context 이해 벤치마크

**Agentic Tool Use**

* **BFCL-V3**: 함수 호출 능력의 다양한 측면 평가
* **TAU-BENCH**: 시뮬레이션된 사용자 LLM과의 대화를 통한 도구 호출 성능 평가

**Multilinguality**

* **한국어**: KMMLU-PRO, KMMLU-REDUX, KSM (Korean School Math)
* **스페인어**: MMMLU (ES), MATH500 (ES), WMT24++

### **3.2 Baselines**

**3가지 모델 타입별 분류**  
비교 대상 모델들을 3가지 유형으로 분류:  
1. **Non-Reasoning 모델**: CoT 스타일로 응답 생성  
2. **Reasoning 모델**: 긴 CoT 스타일로 응답 생성  
3. **Hybrid 모델**: 모드에 따라 CoT 또는 긴 CoT 스타일로 생성

**모델 규모별 분류**

* **Small-size**: 3B 미만
* **Mid-size**: 10B-30B
* **Frontier**: 200B 이상

### **3.4 Experimental Results**

**수학/코딩 도메인에서의 우수성**  
EXAONE 4.0 모델은 수학/코딩 벤치마크에서 탁월한 성능을 보입니다:

* **32B 모델**: REASONING과 NON-REASONING 모드 모두에서 Qwen3 235B를 모든 수학/코딩 벤치마크에서 능가
* **1.2B 모델**: REASONING 모드의 EXAONE Deep 2.4B를 제외한 모든 기준선을 능가

**도구 사용 시나리오에서의 경쟁력**  
EXAONE 4.0 32B 모델은 기준 모델들과 비교하여 경쟁력 있는 도구 사용 성능을 보입니다:

* REASONING 모드에서 TAU-BENCH에서 R1-0528과 유사한 성능
* NON-REASONING 모드에서 Qwen 3 235B와 비교 가능한 BFCL-V3 결과

**세계 지식과 GPQA 성능**  
두 모델 모두 세계 지식 카테고리 벤치마크에서 우수한 성능을 보이며, 특히 GPQA-DIAMOND에서 기준선들보다 우수한 성능을 달성했습니다.

### **3.5 Reasoning Budget**

**추론 토큰 수에 따른 성능 변화**  
추론 토큰 수를 1K에서 64K까지 변화시키며 성능 변화를 관찰했습니다:

**32K 추론 예산에서의 경쟁력**  
EXAONE 4.0 모델은 32K 추론 예산으로도 경쟁력 있는 성능을 유지합니다:

* 32B 모델의 AIME 2025에서 12.3% 감소를 제외하고는 대부분 5% 이내의 성능 감소
* 기준 모델들과 비교하여 여전히 경쟁력 있는 결과 유지

**챕터의 핵심 기여**: 종합적이고 체계적인 성능 평가를 통한 모델 능력 검증  
**다음 챕터로의 연결**: 성능 결과를 바탕으로 한 모델의 한계점과 위험요소 논의로 이어짐

---

**📖 Chapter 4: Limitations**
----------------------------

### **챕터의 위치와 역할**

한계점 챕터는 EXAONE 4.0의 뛰어난 성능에도 불구하고 존재하는 제약사항과 잠재적 위험요소를 솔직하게 논의합니다.

### **저자의 서술 순서를 따른 상세 내용:**

**1. 기본적인 언어 모델의 한계**  
EXAONE 4.0 언어 모델은 기존의 모든 언어 모델과 마찬가지로 특정 한계가 있으며 때때로 부적절한 응답을 생성할 수 있습니다. 언어 모델은 토큰의 출력 확률을 기반으로 응답을 생성하며, 이는 훈련 데이터로부터의 학습 중에 결정됩니다.

**2. 훈련 데이터의 불완전성**  
개인적, 유해한, 편향된 정보를 훈련 데이터에서 제외하기 위해 모든 노력을 기울였지만, 일부 문제가 있는 콘텐츠가 여전히 포함될 수 있어 바람직하지 않은 응답으로 이어질 가능성이 있습니다.

**3. 구체적인 위험 요소들**

**부적절한 답변 생성**  
개인적, 유해한 또는 기타 부적절한 정보가 포함된 부적절한 답변이 생성될 수 있습니다.

**편향된 응답**  
연령, 성별, 인종 등과 관련된 편향된 응답이 생성될 수 있습니다.

**통계적 의존성의 문제**  
생성된 응답은 훈련 데이터의 통계에 크게 의존하여 의미적으로 또는 구문적으로 올바르지 않은 문장을 생성할 수 있습니다.

**최신 정보의 부재**  
모델이 최신 정보를 반영하지 않기 때문에 응답이 거짓이거나 모순될 수 있습니다.

**4. 윤리적 사용 지침**  
LG AI Research는 EXAONE 4.0 언어 모델로부터 발생할 수 있는 잠재적 위험을 줄이기 위해 노력합니다. 사용자는 EXAONE 4.0 언어 모델 사용 시 LG AI의 윤리 원칙을 위반하는 부적절한 출력 생성을 유도할 수 있는 악의적 활동(예: 불법 정보 입력)에 참여할 수 없습니다.

**5. 책임 고지**  
EXAONE 4.0 언어 모델에 의해 생성된 텍스트는 LG AI Research의 견해를 반영하지 않습니다.

**챕터의 핵심 기여**: 모델의 투명성과 책임감 있는 AI 개발을 위한 한계 인식  
**다음 챕터로의 연결**: 실제 배포를 위한 라이선스 정보 제공으로 이어짐

---

**📖 Chapter 5: Deployment**
---------------------------

### **챕터의 위치와 역할**

배포 챕터는 EXAONE 4.0 모델의 실제 사용을 위한 법적 정보를 제공하는 실용적 장입니다.

### **라이선스 정보**

부록 B에서 EXAONE 4.0 모델 사용을 위한 라이선스 정보를 제공합니다. 언어 모델의 합법적 활용을 위해서는 라이선스 정보 이해가 필수적입니다.

**챕터의 핵심 기여**: 모델 사용을 위한 법적 가이드라인 제공  
**다음 챕터로의 연결**: 전체 연구의 결론과 향후 방향 제시로 마무리

---

**📖 Chapter 6: Conclusion**
---------------------------

### **챕터의 위치와 역할**

결론 챕터는 EXAONE 4.0의 전체적인 성과를 요약하고 향후 연구 방향을 제시하는 마무리 장입니다.

### **저자의 서술 순서를 따른 상세 내용:**

**1. EXAONE 4.0의 핵심 성과**  
본 기술 보고서에서는 NON-REASONING 모드와 REASONING 모드를 통합한 EXAONE 4.0을 소개했습니다. EXAONE 4.0의 주요 특징은 이전에 EXAONE 3.5와 EXAONE Deep에서 각각 지원되었던 실용적 활용성과 추론 능력을 향상시키고 이를 단일 모델로 통합한 것입니다.

**2. 새로운 기능의 도입**  
agentic tool use 및 스페인어 지원과 같은 새로운 기능을 도입했습니다.

**3. 성능상의 우수성**  
성능 면에서 EXAONE 4.0은 비슷한 규모의 모델들과 비교하여 우수한 결과를 보여주며, frontier 모델들과 비교해서도 경쟁력 있는 성능을 달성했습니다.

**4. 향후 계획**  
향후 작업의 일환으로, 지원 언어를 점진적으로 확장하여 활용성을 지속적으로 강화하는 것을 목표로 합니다.

**5. 연구 생태계에 대한 기여**  
EXAONE 3.0 출시 이후, LG AI Research는 open-weight 형태로 모델을 공개하여 연구 생태계 확장에 기여해왔으며, 사용자 피드백을 기반으로 지속적으로 모델을 개선해왔습니다.

**6. 연락처 정보**  
모델 개선 제안이나 비즈니스 관련 문의는 contact\_us@lgresearch.ai로 연락하시기 바랍니다.

**챕터의 핵심 기여**: 전체 연구 성과의 종합과 지속적인 발전을 위한 방향 제시

---

**기술적 함의와 응용**
--------------

### **해당 분야에 미치는 영향**

EXAONE 4.0의 hybrid 모드 통합 접근법은 단일 모델이 서로 다른 사용 시나리오에 최적화된 두 가지 추론 전략을 제공할 수 있음을 보여줍니다. 이는 실용적 배포에서 모델 관리 복잡성을 크게 줄이는 혁신적 접근법입니다.

### **다른 연구 영역으로의 확장 가능성**

Hybrid attention 메커니즘과 QK-Reorder-LN과 같은 아키텍처 혁신은 다른 대형 언어 모델 개발에 직접적으로 적용 가능하며, 특히 long-context 처리가 중요한 애플리케이션에서 활용도가 높을 것입니다.

### **실제 산업 적용에서의 고려사항**

Agentic tool use 기능은 실제 비즈니스 환경에서 AI 에이전트 구축을 위한 실용적 기반을 제공하며, 다국어 지원 확장은 글로벌 서비스 배포에 중요한 의미를 갖습니다.

### **향후 연구 방향에 대한 시사점**

AGAPO와 같은 새로운 강화학습 알고리즘의 개발은 추론 능력 향상을 위한 훈련 방법론 연구에 새로운 방향을 제시하며, preference learning을 통한 모드 통합 방법론은 multi-modal AI 시스템 개발에 중요한 통찰을 제공합니다.

---

**본 논문은 EXAONE 4.0을 통해 실용성과 추론 능력을 단일 모델에 효과적으로 통합하는 방법론을 제시하며, 향후 범용 AI 시스템 개발을 위한 중요한 기술적 토대를 마련했습니다.**