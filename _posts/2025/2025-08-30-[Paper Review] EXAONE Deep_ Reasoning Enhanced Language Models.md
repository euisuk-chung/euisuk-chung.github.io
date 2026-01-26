---
title: "[Paper Review] EXAONE Deep: Reasoning Enhanced Language Models"
date: "2025-08-30"
year: "2025"
---

# [Paper Review] EXAONE Deep: Reasoning Enhanced Language Models


![](https://velog.velcdn.com/images/euisuk-chung/post/c1e891a2-0fa5-4248-a5ec-c5ed04376818/image.png)

> <https://arxiv.org/pdf/2503.12524>

```
RESEARCH, L. G., et al. EXAONE Deep: Reasoning Enhanced Language Models. arXiv preprint arXiv:2503.12524, 2025.
```

Abstract
--------

EXAONE Deep 시리즈를 소개합니다. 이 모델들은 수학 및 코딩 benchmark를 포함한 다양한 추론 작업에서 우수한 성능을 보입니다. 우리는 긴 사고 과정의 stream을 통합한 추론 특화 dataset을 주로 사용하여 모델들을 훈련했습니다. 평가 결과, 우리의 작은 모델들인 EXAONE Deep 2.4B와 7.8B는 비슷한 크기의 다른 모델들을 능가하며, 가장 큰 모델인 EXAONE Deep 32B는 주요 open-weight 모델들과 경쟁력 있는 성능을 보여줍니다. 모든 EXAONE Deep 모델들은 연구 목적으로 공개되어 있으며 <https://huggingface.co/LGAI-EXAONE> 에서 다운로드할 수 있습니다.

1. Introduction
---------------

최근 연구에서는 테스트 단계에서 컴퓨팅 리소스를 조정하여 추론 성능을 향상시키는 추세가 증가하고 있습니다. 이러한 추세에 대응하여, LG AI Research는 EXAONE Deep 2.4B, 7.8B, 32B라는 새로운 모델 라인업을 소개합니다. 이 모델들은 EXAONE 3.5 시리즈의 fine-tuned 버전으로, 추론 작업에 특별히 최적화되었습니다. 우리는 fine-tuning에 널리 사용되는 세 가지 주요 기법인 Supervised Fine-Tuning (SFT), Direct Preference Optimization (DPO), Online Reinforcement Learning (Online RL)을 사용하여 이 모델들을 훈련했습니다.

모델들의 성능 평가 결과, 2.4B 변형의 경우 DeepSeek-R1-Distill-Qwen-1.5B보다 우수한 성능을 보입니다. 7.8B 변형의 경우, DeepSeek-R1-Distill-Qwen-7B 및 DeepSeek-R1-Distill-Llama-8B와 같은 비슷한 규모의 open-weight 모델들뿐만 아니라 proprietary 추론 모델인 OpenAI o1-mini도 능가합니다. 32B 모델의 경우, QwQ-32B 및 DeepSeek-R1과 같은 주요 open-weight 추론 모델들과 경쟁력 있는 성능을 보이며, DeepSeek-R1-Distill-Qwen-32B 및 DeepSeek-R1-Distill-Llama-70B보다 우수한 성능을 나타냅니다.

> "생각이 말이 되고, 말이 행동이 되고, 행동이 습관이 되고, 습관이 성격이 되고, 성격이 운명이 된다. 따라서 깨어있는 마음의 눈으로 마음의 를 지켜보라." - TRYON EDWARDS

2. Modeling
-----------

### 2.1 Data

언어 모델의 추론 능력을 향상시키기 위해, 우리는 SFT용 1.6M 인스턴스, DPO용 preference data 20K 인스턴스, 그리고 Online RL용 추가 10K 인스턴스를 활용했습니다. SFT dataset는 약 12B 토큰을 포함하며, 그 길이 분포는 Figure 2에 나타나 있습니다. 이 dataset는 모델이 확장된 chain-of-thought (CoT) 과정을 통해 추론을 수행하도록 설계되었습니다.

Figure 2에서 보듯이, Code 도메인의 데이터 포인트들은 평균적으로 상당히 길며, Others 도메인의 데이터 포인트들은 더 짧은 경향이 있습니다.

### 2.2 Training

EXAONE Deep의 base 모델들은 instruction-following 능력을 갖춘 instruction-tuned 모델인 EXAONE 3.5 Instruct 모델들입니다. EXAONE Deep의 추론 능력을 향상시키기 위해, 우리는 SFT 및 DPO 데이터를 template 형식으로 구조화했습니다. 각 훈련 인스턴스는 구조화된 사고 과정과 추론 단계를 일관되고 정확한 응답으로 종합한 최종 답변으로 구성됩니다.

구체적으로, EXAONE 3.5 Instruct 모델들은 `<thought>`와 `</thought>` 태그 내에서 추론을 수행하도록 훈련되며, reflection, self-checking, correction과 함께 단계별 논리적 진행을 수행합니다. 추론 후 생성되는 최종 답변은 자체 완결적이며, 사고 과정에서 도출된 핵심 통찰을 명확하고 간결하게 요약합니다.

훈련 compute 측면에서, EXAONE Deep 모델들은 Google Cloud Platform과 NVIDIA NeMo Framework에서 제공되는 NVIDIA H100 GPU cluster를 사용하여 훈련됩니다. base 모델의 pretraining과 추론 능력 향상을 위한 fine-tuning에 사용된 computation 양은 Table 1에 제시되어 있습니다.

**Table 1: 모델 훈련을 위한 computation 양 (FLOPs)**

| 모델 크기 | Pretraining | Fine-tuning | Total |
| --- | --- | --- | --- |
| 32B | 1.25 × 10²⁴ | 7.04 × 10²¹ | 1.26 × 10²⁴ |
| 7.8B | 4.21 × 10²³ | 1.71 × 10²¹ | 4.23 × 10²³ |
| 2.4B | 9.36 × 10²² | 5.27 × 10²⁰ | 9.41 × 10²² |

3. Evaluation
-------------

### 3.1 Benchmarks

우리는 MATH-500, American Invitational Mathematics Examination (AIME) 2024 및 2025, South Korea's College Scholastic Ability Test (CSAT) 2025의 수학 섹션, GPQA Diamond, LiveCodeBench (24.08-25.02), MMLU, MMLU-Pro에서 모델들을 평가합니다.

CSAT의 경우, 텍스트 문제와 보조 그래픽 정보를 포함하는데, 성능 평가 시 그래픽 콘텐츠는 제외됩니다. 수학 섹션에서 학생들은 미적분, 통계, 기하학 중 세 가지 선택 과목에서 선택할 수 있으며, 최종 점수는 이 세 선택 과목에서 얻은 점수의 평균으로 계산됩니다.

### 3.2 Baselines

우리는 DeepSeek-R1과 같은 강력한 baseline뿐만 아니라 QwQ-32B, DeepSeek-R1-Distill-Qwen-32B, 7B, 1.5B, DeepSeek-R1-Distill-Llama-70B, 8B, OpenAI o1-mini와 같은 비교 가능한 규모의 baseline들과 포괄적인 평가를 수행했습니다.

### 3.3 Evaluation Setup

DeepSeek-R1 기술 보고서에 설명된 설정에 따라, 모델 생성의 최대 길이를 32K 토큰으로 설정했습니다. 추론 모델들의 긴 출력이 크게 달라질 수 있다는 점을 고려하여, 모델 성능의 신뢰성을 보장하기 위해 pass@k metric을 채택했습니다.

평가에 사용된 prompt들은 Figure 4, 5, 6에 나타나 있습니다. CSAT benchmark의 경우, 단답형과 객관식 문제를 포함하므로 두 prompt를 모두 사용합니다.

### 3.4 Experimental Results

EXAONE Deep과 baseline 모델들 간의 성능 비교는 수학, 과학, 코딩, 일반 지식의 네 가지 범주에서 수행됩니다. 수학 범주의 평가 결과는 Table 2에, 다른 범주의 결과는 Table 3에 제시되어 있습니다.

EXAONE Deep 32B 모델은 DeepSeek-R1 및 QwQ-32B와 같은 주요 open-weight 추론 모델들과 경쟁력 있는 성능을 보입니다. 특히 DeepSeek-R1-Distill-Qwen-32B 및 DeepSeek-R1-Distill-Llama-70B와 같은 distilled 버전들을 능가합니다.

또한, EXAONE Deep 7.8B 모델은 DeepSeek-R1-Distill-Qwen-7B 및 DeepSeek-R1-Distill-Llama-8B와 같은 유사한 규모의 모델들보다 우수한 성능을 보이며, proprietary 추론 모델인 OpenAI o1-mini도 능가합니다.

EXAONE Deep 2.4B의 경우, DeepSeek-R1-Distill-Qwen-1.5B를 능가합니다. 우리의 실험 결과는 EXAONE Deep 모델들이 다양한 모델 크기에서 향상된 추론 능력을 보여준다는 것을 강조합니다.

4. Limitations
--------------

이 문서에서 소개된 EXAONE Deep 모델들은 추론 작업에서 뛰어난 성능을 발휘하도록 특별히 fine-tuning되었습니다. base 모델들이 instruction-fine-tuned되어 일반적으로 지시를 따를 수 있지만, 더 넓은 범위의 실제 사용 사례를 다루기 위해서는 실용적인 응용 시나리오에 최적화된 EXAONE 3.5 Instruct 모델들을 사용할 것을 강력히 권장합니다.

5. Deployment
-------------

부록 B에서는 EXAONE Deep 모델 사용을 위한 라이선스 정보를 제공합니다. 언어 모델의 법적 활용을 위해서는 라이선스 정보를 이해하는 것이 필수적입니다.

6. Conclusion
-------------

이 문서에서 우리는 세 가지 특화된 추론 모델인 EXAONE Deep 2.4B, 7.8B, 32B를 제시했습니다. 추론 능력 향상을 목표로 하는 다양한 방법론의 출현에도 불구하고, 우리는 SFT, DPO, Online RL과 같은 잘 확립된 접근법에 의존하여 비슷한 규모의 모델들 대비 우수하거나 경쟁력 있는 성능을 달성했습니다.

우리의 결과는 추론 성능 향상에서 이러한 검증된 기법들의 효과성과 실용성을 강조합니다. 현재 이러한 모델들은 주로 수학, 과학, 코딩과 같이 명확한 답이 있는 도메인에서 문제 해결에 집중하고 있습니다. 앞으로 우리는 답이 덜 명확하거나 아직 발견되지 않은 영역으로 능력을 확장하여 더 넓은 영향과 유용성을 추구하고자 합니다.

우리의 모델들은 연구 목적으로 모든 사람이 사용할 수 있으며, 모델 개선에 도움이 되는 여러분의 피드백을 환영합니다. 피드백이 있거나 모델과의 상업적 기회 탐색에 관심이 있으시면 contact\_us@lgresearch.ai로 연락해 주시기 바랍니다.

---

Model License
-------------

**EXAONE AI Model License Agreement 1.1 - NC**

이 라이선스 계약("계약")은 귀하("라이선스 사용자")와 LG Management Development Institute Co., Ltd.("라이선스 제공자") 간에 EXAONE AI Model("모델")의 사용을 규율하기 위해 체결됩니다. 모델을 다운로드, 설치, 복사 또는 사용함으로써, 귀하는 이 계약의 조건을 준수하고 구속받는 데 동의합니다.

### 1. 정의

1.1 **모델**: 라이선스 제공자가 제공하는 인공지능 모델로, 라이선스 제공자가 공급하는 모든 소프트웨어, 알고리즘, 머신러닝 모델 또는 관련 구성 요소를 포함합니다.

1.2 **파생물**: 라이선스 사용자 또는 제3자가 만든 모델의 수정, 변경, 향상, 개선, 적응 또는 파생 작업을 의미합니다.

1.3 **출력물**: 모델이나 파생물에 의해 생성된 모든 데이터, 결과, 콘텐츠, 예측, 분석, 통찰 또는 기타 자료를 의미합니다.

1.4 **라이선스 제공자**: EXAONE AI Model의 소유자, 개발자 및 제공자인 LG Management Development Institute Co., Ltd.를 의미합니다.

1.5 **라이선스 사용자**: 이 계약의 조건에 따라 모델을 사용하거나 사용하려는 개인, 조직, 법인, 학술 기관, 정부 기관 또는 기타 주체를 의미합니다.

### 2. 라이선스 허가

2.1 **라이선스 허가**: 이 계약에 명시된 조건에 따라, 라이선스 제공자는 라이선스 사용자에게 제한적, 비독점적, 양도 불가능, 전세계적, 취소 가능한 라이선스를 허가합니다.

### 3. 제한사항

3.1 **상업적 사용**: 라이선스 사용자는 수익을 직접적이거나 간접적으로 창출하는 제품, 서비스 또는 응용프로그램 개발이나 배포를 포함하되 이에 국한되지 않는 상업적 목적으로 모델, 파생물 또는 출력물을 사용하는 것이 명시적으로 금지됩니다.

3.2 **역공학**: 라이선스 사용자는 해당 법률에서 명시적으로 허용하는 경우를 제외하고, 모델을 역컴파일, 분해, 역공학하거나 소스 코드, 기본 아이디어, 알고리즘 또는 구조를 도출하려고 시도해서는 안 됩니다.

### 4. 소유권

4.1 **지적 재산권**: 수정, 파생물 및 관련 문서를 포함한 모델의 모든 권리, 소유권 및 이익은 라이선스 제공자의 독점적 재산으로 유지됩니다.

### 5. 무보증

5.1 **"있는 그대로" 기준**: 모델, 파생물 및 출력물은 명시적, 묵시적 또는 법적 보증이나 표현 없이 "있는 그대로" 및 "이용 가능한 상태로" 제공됩니다.

### 6. 책임 제한

6.1 **손해에 대한 책임 없음**: 해당 법률에서 허용하는 최대 범위까지, 라이선스 제공자는 특별한, 부수적, 간접적, 결과적, 예시적 또는 징벌적 손해에 대해 어떠한 경우에도 책임을 지지 않습니다.

### 7. 종료

7.1 **라이선스 제공자에 의한 종료**: 라이선스 제공자는 라이선스 사용자가 이 계약의 조건을 위반하는 경우 사전 통지 없이 언제든지 이 계약을 종료하고 라이선스 사용자의 모델 사용 권리를 취소할 수 있는 권리를 보유합니다.

### 8. 준거법

8.1 **준거법**: 이 계약은 법률 충돌 원칙과 관계없이 대한민국 법률에 따라 규율되고 해석됩니다.

### 9. 변경

9.1 **수정**: 라이선스 제공자는 단독 재량으로 언제든지 이 계약을 수정하거나 개정할 권리를 보유합니다.

Evaluation Details
------------------

**Table 4: CSAT 2025 benchmark의 선택 과목별 개별 점수에서 EXAONE Deep과 baseline 모델들의 비교**

| 모델 | CSAT 2025 미적분 | CSAT 2025 통계 | CSAT 2025 기하학 |
| --- | --- | --- | --- |
| EXAONE Deep 32B | 95.1 | 95.0 | 93.5 |
| QwQ-32B | 94.5 | 95.5 | 93.3 |
| DeepSeek-R1 (671B) | 89.4 | 90.8 | 89.6 |