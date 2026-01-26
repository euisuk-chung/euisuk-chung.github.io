---
title: "[Paper Review] Qwen-Image Technical Report"
date: "2025-08-29"
tags:
  - "paper-review"
year: "2025"
---

# [Paper Review] Qwen-Image Technical Report


![](https://velog.velcdn.com/images/euisuk-chung/post/3ae570b0-1f5f-4b9d-9d9c-981a71f386a3/image.png)

> <https://arxiv.org/abs/2508.02324>

```
WU, Chenfei, et al. Qwen-image technical report. arXiv preprint arXiv:2508.02324, 2025.
```

본 연구에서는 복잡한 텍스트 렌더링과 정밀한 이미지 편집에서 상당한 진보를 이룬 Qwen 시리즈의 이미지 생성 foundation model인 Qwen-Image를 제시합니다.

1. 서론
-----

text-to-image 생성(T2I)과 이미지 편집(TI2I)을 모두 포함하는 이미지 생성 모델은 현대 인공지능의 기본 구성 요소로 등장했습니다. 기계가 텍스트 프롬프트에서 시각적으로 매력적이고 의미적으로 일관된 콘텐츠를 합성하거나 수정할 수 있게 합니다. 지난 몇 년 동안 이 분야에서 놀라운 진전이 있었습니다. 특히 fine-grained semantic detail을 캡처하면서 고해상도 이미지 생성을 가능하게 하는 diffusion-based architecture의 출현과 함께 말입니다.

이러한 진전에도 불구하고 두 가지 중요한 문제가 지속됩니다:

**첫째**, text-to-image 생성에서 복잡하고 다면적인 프롬프트와 모델 출력의 정렬은 여전히 중요한 장벽입니다. 우리의 평가에 따르면 GPT Image 1이나 Seedream 3.0과 같은 state-of-the-art 상용 모델들도 multi-line 텍스트 렌더링, non-alphabetic language 렌더링(예: 중국어), 지역화된 텍스트 삽입, 또는 텍스트와 시각적 요소의 매끄러운 통합을 요구하는 태스크에 직면했을 때 어려움을 겪습니다.

**둘째**, 이미지 편집에서 편집된 출력과 원본 이미지 간의 정확한 정렬을 달성하는 것은 이중 도전을 제기합니다: (i) visual consistency - 대상 영역만 수정되어야 하고 다른 모든 시각적 세부사항은 보존되어야 함(예: 얼굴 세부사항을 변경하지 않고 머리 색깔 변경) (ii) semantic coherence - 구조적 변화 중에도 전역 semantic을 보존해야 함(예: 정체성과 장면 일관성을 유지하면서 사람의 자세 수정)

본 연구에서는 포괄적인 data engineering, progressive learning 전략, 강화된 multi-task training paradigm, 그리고 확장 가능한 infrastructure 최적화를 통해 이러한 도전을 극복하도록 설계된 Qwen 시리즈의 새로운 이미지 생성 모델인 Qwen-Image를 소개합니다.

### 주요 기여사항

Qwen-Image의 주요 기여사항은 다음과 같이 요약됩니다:

* **뛰어난 텍스트 렌더링**: Qwen-Image는 multiline layout, paragraph-level semantic, fine-grained detail을 포함한 복잡한 텍스트 렌더링에 탁월합니다. alphabetic language(예: 영어)와 logographic language(예: 중국어) 모두를 높은 충실도로 지원합니다.
* **일관된 이미지 편집**: 강화된 multi-task training paradigm을 통해 Qwen-Image는 편집 작업 중 semantic meaning과 visual realism을 모두 보존하는 데 뛰어난 성능을 달성합니다.
* **강력한 cross-benchmark 성능**: 여러 benchmark에서 평가한 결과, Qwen-Image는 다양한 생성 및 편집 태스크에서 기존 모델들을 지속적으로 능가하여 이미지 생성을 위한 강력한 foundation model을 확립합니다.

2. 모델
-----

이 섹션에서는 훈련 데이터와 훈련 세부사항에 대한 포괄적인 개요와 함께 Qwen-Image 모델의 아키텍처 설계를 제시합니다.

### 2.1 모델 아키텍처

Figure 6에서 보듯이, Qwen-Image 아키텍처는 고충실도 text-to-image 생성을 가능하게 하기 위해 조화롭게 작동하는 세 가지 핵심 구성 요소로 구성됩니다:

1. **Multimodal Large Language Model (MLLM)**: condition encoder 역할을 하며 텍스트 입력에서 feature를 추출합니다.
2. **Variational AutoEncoder (VAE)**: 이미지 tokenizer 역할을 하며 입력 이미지를 compact latent representation으로 압축하고 inference 중에 이를 다시 디코딩합니다.
3. **Multimodal Diffusion Transformer (MMDiT)**: backbone diffusion model로 기능하며 텍스트 가이드 하에서 noise와 image latent 간의 복잡한 joint distribution을 모델링합니다.

### 2.2 Multimodal Large Language Model

Qwen-Image는 텍스트 입력을 위한 feature extraction module로 Qwen2.5-VL 모델을 사용합니다. 세 가지 주요 이유는 다음과 같습니다:

1. Qwen2.5-VL의 language space와 visual space가 이미 정렬되어 있어 Qwen3와 같은 language-based model보다 text-to-image 태스크에 더 적합합니다.
2. Qwen2.5-VL은 language model에 비해 상당한 성능 저하 없이 강력한 language modeling 능력을 유지합니다.
3. Qwen2.5-VL은 multimodal 입력을 지원하여 Qwen-Image가 이미지 편집과 같은 더 광범위한 기능을 제공할 수 있게 합니다.

### 2.3 Variational AutoEncoder

강력한 VAE representation은 강력한 이미지 foundation model을 구축하는 데 중요합니다. 현재 이미지 foundation model들은 일반적으로 대규모 이미지 dataset에서 2D convolution으로 이미지 VAE를 훈련하여 고품질 이미지 representation을 얻습니다.

우리의 작업은 이미지와 비디오 모두와 호환되는 더 일반적인 visual representation을 개발하는 것을 목표로 합니다. 기존의 joint image-video VAE들은 일반적으로 이미지 reconstruction 능력이 저하되는 성능 trade-off를 겪습니다. 이를 해결하기 위해 single-encoder, dual-decoder 아키텍처를 활용합니다.

reconstruction fidelity, 특히 작은 텍스트와 fine-grained detail을 향상시키기 위해 텍스트가 풍부한 이미지의 in-house corpus에서 decoder를 훈련합니다. dataset은 alphabetic(예: 영어)와 logographic(예: 중국어) 언어를 모두 다루는 실제 문서(PDF, PowerPoint 슬라이드, 포스터)와 합성 paragraph로 구성됩니다.

### 2.4 Multimodal Diffusion Transformer

Qwen-Image는 텍스트와 이미지를 jointly 모델링하기 위해 Multimodal Diffusion Transformer(MMDiT)를 채택합니다. 이 접근법은 FLUX 시리즈와 Seedream 시리즈 같은 다양한 작업에서 효과적임이 입증되었습니다.

각 block 내에서 새로운 positional encoding 방법인 Multimodal Scalable RoPE(MSRoPE)를 도입합니다. Figure 8에서 보듯이, 다양한 text-image joint positional encoding 전략을 비교합니다.

**MSRoPE의 특징**:

* 텍스트 입력을 양쪽 차원에 동일한 position ID가 적용된 2D tensor로 처리
* 텍스트가 이미지의 대각선을 따라 연결된 것으로 개념화
* 이미지 측면에서 resolution scaling 장점을 활용하면서 텍스트 측면에서 1D-RoPE와 기능적으로 동등함을 유지

3. 데이터
------

### 3.1 데이터 수집

이미지 생성 모델의 훈련을 지원하기 위해 수십억 개의 이미지-텍스트 쌍을 체계적으로 수집하고 주석을 작성했습니다. raw dataset의 규모에만 집중하는 것보다 데이터 품질과 균형 잡힌 데이터 분포를 우선시하여 실제 시나리오를 밀접하게 반영하는 잘 균형 잡히고 대표적인 dataset을 구축하는 것을 목표로 했습니다.

Figure 9에서 보듯이, dataset은 네 가지 주요 도메인으로 구성됩니다:

1. **Nature (약 55%)**: Objects, Landscape, Cityscape, Plants, Animals, Indoor, Food 카테고리 등 다양한 하위 카테고리를 포함합니다.
2. **Design (약 27%)**: Poster, User Interface, Presentation Slide와 같은 구조화된 시각적 콘텐츠와 회화, 조각, 공예품, 디지털 아트 등 다양한 형태의 예술을 포함합니다.
3. **People (약 13%)**: Portrait, Sports, Human Activities 등의 하위 카테고리를 포함합니다.
4. **Synthetic Data (약 5%)**: 통제된 텍스트 렌더링 기술을 통해 합성된 데이터입니다.

### 3.2 데이터 필터링

이미지 생성 모델의 반복적 개발 과정에서 고품질 훈련 데이터를 큐레이션하기 위해 Figure 10에 나타난 바와 같이 7단계의 순차적 단계로 구성된 multi-stage 필터링 파이프라인을 제안했습니다.

**Stage 1: Initial Pre-training Data Curation**

* 256p 해상도 이미지로 훈련
* Broken Files Filter, File Size Filter, Resolution Filter, Deduplication Filter, NSFW Filter 적용

**Stage 2: Image Quality Enhancement**

* Rotation Filter, Clarity Filter, Luma Filter, Saturation Filter, Entropy Filter, Texture Filter 적용

**Stage 3: Image-Text Alignment Improvement**

* Raw Caption Split, Recaption Split, Fused Caption Split으로 분할
* Chinese CLIP Filter, SigLIP Filter, Token Length Filter, Invalid Caption Filter 적용

**Stage 4: Text Rendering Enhancement**

* English Split, Chinese Split, Other Language Split, Non-Text Split으로 분류
* Intensive Text Filter, Small Character Filter 적용

**Stage 5: High-Resolution Refinement**

* 640p 해상도로 전환
* Image Quality Filter, Resolution Filter, Aesthetic Filter, Abnormal Element Filter 적용

**Stage 6: Category Balance and Portrait Augmentation**

* General, Portrait, Text Rendering의 세 가지 주요 카테고리로 재분류
* keyword-based retrieval과 image retrieval 기술 사용

**Stage 7: Balanced Multi-Scale Training**

* 640p와 1328p 해상도에서 joint 훈련
* hierarchical taxonomy system 기반 이미지 분류

### 3.3 데이터 주석 작성

데이터 주석 파이프라인에서 포괄적인 이미지 설명뿐만 아니라 필수 이미지 속성과 품질 특성을 캡처하는 구조화된 메타데이터를 생성하기 위해 능력있는 이미지 captioner(예: Qwen2.5-VL)를 활용합니다.

captioning과 메타데이터 추출을 독립적인 태스크로 처리하는 대신, captioner가 동시에 시각적 콘텐츠를 설명하고 JSON과 같은 구조화된 형식으로 세부 정보를 생성하는 주석 프레임워크를 설계했습니다.

### 3.4 데이터 합성

실제 이미지에서 텍스트 콘텐츠의 long-tail distribution, 특히 중국어와 같은 non-Latin 언어에서 수많은 문자가 극도로 낮은 빈도를 나타내는 문제를 해결하기 위해 multi-stage text-aware 이미지 합성 파이프라인을 제안합니다.

**세 가지 보완적 전략**:

1. **Pure Rendering in Simple Backgrounds**: 가장 직접적이고 효과적인 방법으로 문자 인식 및 생성을 훈련합니다.
2. **Compositional Rendering in Contextual Scenes**: 합성 텍스트를 현실적인 시각적 맥락에 삽입하여 일상 환경에서의 모습을 모방합니다.
3. **Complex Rendering in Structured Templates**: 복잡하고 구조화된 프롬프트를 따르는 모델의 능력을 향상시키기 위해 사전 정의된 템플릿의 프로그래밍적 편집에 기반한 합성 전략을 제안합니다.

4. 훈련
-----

### 4.1 Pre-training

Qwen-Image를 pre-train하기 위해 flow matching 훈련 목표를 채택하여 ordinary differential equation(ODE)을 통한 안정적인 학습 dynamics를 촉진하면서 maximum likelihood 목표와의 동등성을 보존합니다.

**훈련 과정**:

* 입력 이미지의 latent z=E(x)z = E(x)z=E(x) (VAE encoder를 통해)
* random noise vector x1∼N(0,I)x\_1 \sim N(0,I)x1​∼N(0,I)에서 샘플링
* 사용자 입력 SSS에 대해 guidance latent h=ϕ(S)h = \phi(S)h=ϕ(S) (MLLM에서)
* diffusion timestep ttt를 logit-normal distribution에서 샘플링

**손실 함수**:  
L=E(x0,h)∼D,x1,t∥vθ(xt,t,h)−vt∥2L = E\_{(x\_0,h)\sim D,x\_1,t} \|v\_\theta(x\_t, t, h) - v\_t\|^2L=E(x0​,h)∼D,x1​,t​∥vθ​(xt​,t,h)−vt​∥2

### 4.1.1 Producer-Consumer Framework

대규모 GPU cluster로 확장할 때 높은 throughput과 훈련 안정성을 모두 보장하기 위해 데이터 전처리와 모델 훈련을 분리하는 Ray에서 영감을 받은 Producer-Consumer 프레임워크를 채택합니다.

**Producer 측면**:

* raw 이미지-caption 쌍을 사전 정의된 기준에 따라 필터링
* MLLM 모델과 VAE를 사용하여 latent representation으로 인코딩
* 처리된 이미지를 해상도별로 빠른 액세스 cache bucket에 그룹화

**Consumer 측면**:

* GPU 집약적 cluster에 배포
* 모델 훈련에만 전념
* MMDiT parameter를 4-way tensor-parallel layout으로 분산

### 4.1.2 분산 훈련 최적화

Qwen-Image 모델의 큰 parameter 크기를 고려하여 FSDP만으로는 각 GPU에 모델을 맞추기에 불충분합니다. 따라서 훈련을 위해 Megatron-LM을 활용하고 다음 최적화를 적용합니다:

**Hybrid Parallelism Strategy**: data parallelism과 tensor parallelism을 결합한 hybrid parallelism 전략을 채택했습니다.

**Distributed Optimizer and Activation Checkpointing**: GPU 메모리 압력을 완화하기 위해 distributed optimizer와 activation checkpointing을 실험했습니다.

### 4.1.3 훈련 전략

데이터 품질, 이미지 해상도, 모델 성능을 점진적으로 향상시키는 것을 목표로 하는 multi-stage pre-training 전략을 채택합니다:

1. **해상도 향상**: 256×256 pixel → 640×640 pixel → 1328×1328 pixel
2. **텍스트 렌더링 통합**: Non-text → Text
3. **데이터 품질 개선**: Massive Data → Refined Data
4. **데이터 분포 균형**: Unbalanced → Balanced
5. **합성 데이터 증강**: Real-World Data → Synthetic Data

### 4.2 Post-training

Qwen-Image를 위한 post-training 프레임워크는 supervised fine-tuning(SFT)과 reinforcement learning(RL)의 두 단계로 구성됩니다.

### 4.2.1 Supervised Fine-Tuning (SFT)

SFT 단계에서는 semantic 카테고리의 계층적으로 구성된 dataset을 구축하고 세심한 인간 주석을 사용하여 모델의 특정 단점을 해결합니다.

### 4.2.2 Reinforcement Learning (RL)

두 가지 서로 다른 RL 전략을 사용합니다:

**(A) Direct Preference Optimization (DPO)**

* flow-matching(one step) 온라인 preference modeling에 뛰어남
* 계산적으로 효율적

**(B) Group Relative Policy Optimization (GRPO)**

* 훈련 중 on-policy sampling 수행
* reward model로 각 trajectory 평가

### 4.3 Multi-task 훈련

text-to-image(T2I) 생성 외에도, text와 image 입력을 모두 포함하는 multimodal 이미지 생성 태스크를 탐구하기 위해 base model을 확장합니다.

**포함된 태스크**:

* instruction-based 이미지 편집
* novel view synthesis
* depth estimation과 같은 computer vision 태스크

5. 실험
-----

### 5.1 인간 평가

Qwen-Image의 일반적인 이미지 생성 능력을 종합적으로 평가하고 state-of-the-art closed-source API와 객관적으로 비교하기 위해 Elo rating system을 기반으로 구축된 오픈 벤치마킹 플랫폼인 AI Arena를 개발했습니다.

**AI Arena 특징**:

* 공정하고 동적인 오픈 경쟁 플랫폼
* 각 라운드에서 같은 프롬프트로 생성된 두 이미지를 익명으로 사용자에게 제시
* 5,000개의 다양한 프롬프트 큐레이션
* 200명 이상의 다양한 전문 배경을 가진 평가자 참여

**경쟁자**:

* Imagen 4 Ultra Preview 0606
* Seedream 3.0
* GPT Image 1 [High]
* FLUX.1 Kontext [Pro]
* Ideogram 3.0

**결과**: Qwen-Image는 유일한 오픈소스 이미지 생성 모델로서 AI Arena에서 3위를 차지했습니다.

### 5.2 정량적 결과

### 5.2.1 VAE Reconstruction 성능

여러 state-of-the-art 이미지 tokenizer를 정량적으로 평가하여 reconstruction 품질을 평가하기 위해 Peak Signal-to-Noise Ratio(PSNR)와 Structural Similarity Index Measure(SSIM)를 보고합니다.

**Table 2 결과**: Qwen-Image-VAE는 평가된 모든 메트릭에서 state-of-the-art reconstruction 성능을 달성합니다.

### 5.2.2 Text-to-Image 생성 성능

두 가지 관점에서 Qwen-Image의 T2I 태스크 성능을 평가합니다: 일반적인 생성 능력과 텍스트 렌더링 능력.

**주요 벤치마크 결과**:

* **DPG**: Qwen-Image가 가장 높은 전체 점수 달성 (88.32)
* **GenEval**: RL 개선 후 0.91 점수로 0.9 임계값을 초과하는 유일한 foundation model
* **OneIG-Bench**: 중국어와 영어 트랙 모두에서 가장 높은 전체 점수
* **ChineseWord**: 모든 세 단계에서 가장 높은 렌더링 정확도
* **LongText-Bench**: 중국어 긴 텍스트에서 가장 높은 정확도, 영어 긴 텍스트에서 두 번째로 높은 정확도

### 5.2.3 이미지 편집 성능

text와 image를 conditioning 입력으로 매끄럽게 통합하는 Qwen-Image의 multi-task 버전을 이미지 편집(TI2I) 태스크를 위해 추가로 훈련했습니다.

**주요 벤치마크 결과**:

* **GEdit**: 영어와 중국어 leaderboard 모두에서 1위
* **ImgEdit**: 전체적으로 가장 높은 순위
* **Novel view synthesis**: GSO dataset에서 경쟁력 있는 결과
* **Depth Estimation**: 여러 key metric에서 state-of-the-art 성능

### 5.3 정성적 결과

### 5.3.1 VAE Reconstruction에서의 정성적 결과

Figure 17은 state-of-the-art 이미지 VAE들로 텍스트가 풍부한 이미지를 reconstruction한 정성적 결과를 보여줍니다. 우리 결과에서 "double-aspect"라는 구문이 명확하게 읽을 수 있게 남아있는 반면, 다른 모델들의 reconstruction에서는 인식할 수 없습니다.

### 5.3.2 이미지 생성에서의 정성적 결과

Qwen-Image의 text-to-image 생성 능력을 종합적으로 평가하기 위해 네 가지 측면에서 정성적 평가를 수행합니다:

1. **영어 텍스트 렌더링**: 더 현실적인 시각적 스타일과 더 나은 렌더링 품질
2. **중국어 텍스트 렌더링**: 예상되는 중국어 couplet을 정확하게 생성
3. **Multi-Object 생성**: 모든 필요한 동물을 정확하게 생성하고 지정된 위치를 충실히 보존
4. **공간 관계 생성**: 복잡한 프롬프트를 이해하고 정확하게 따르는 강력한 능력

### 5.3.3 이미지 편집에서의 정성적 결과

Qwen-Image의 이미지 편집(TI2I) 능력을 종합적으로 평가하기 위해 다섯 가지 주요 측면에 초점을 맞춘 정성적 평가를 수행합니다:

1. **텍스트 및 재료 편집**: 뛰어난 재료 렌더링 및 instruction-following 능력
2. **객체 추가/제거/교체**: 편집되지 않은 영역 보존에서 일반적으로 좋은 성능
3. **자세 조작**: pose 편집 중 세부사항과 일관성 보존에서 뛰어난 성능
4. **연쇄 편집**: 전체 편집 체인을 통해 구조적 특징 보존
5. **Novel View Synthesis**: 복잡한 편집 태스크에서 뛰어난 공간 및 semantic coherence

6. 결론
-----

본 논문에서는 복잡한 텍스트 렌더링과 정밀한 이미지 편집에서 주요한 진전을 달성한 Qwen 시리즈의 이미지 생성 foundation model인 Qwen-Image를 소개했습니다. 포괄적인 데이터 파이프라인을 구축하고 progressive curriculum learning 전략을 채택함으로써 Qwen-Image는 생성된 이미지 내에서 복잡한 텍스트를 렌더링하는 능력을 크게 향상시켰습니다.

개선된 multi-task training paradigm과 dual-encoding 메커니즘을 통해 이미지 편집의 일관성과 품질을 현저히 향상시켜 semantic coherence와 visual fidelity를 모두 효과적으로 개선했습니다. 공개 benchmark에서의 광범위한 실험은 다양한 이미지 생성 및 편집 태스크에서 Qwen-Image의 state-of-the-art 성능을 일관되게 보여줍니다.

**더 깊은 의미와 중요성**:

* **이미지 "생성" 모델로서의 Qwen-Image**: 단순히 photorealism이나 미적 품질을 최적화하는 것이 아니라 텍스트와 이미지 간의 정확한 정렬, 특히 텍스트 렌더링의 어려운 태스크를 강조합니다.
* **이미지 "생성" 모델로서의 Qwen-Image**: generative framework가 고전적인 이해 태스크를 효과적으로 수행할 수 있음을 보여줍니다.
* **"이미지" 생성 모델로서의 Qwen-Image**: 2D 이미지 합성을 넘어선 강력한 일반화를 보여줍니다.
* **"시각적 생성" 모델로서의 Qwen-Image**: 통합된 이해와 생성의 비전을 발전시킵니다.

Qwen-Image는 단순히 state-of-the-art 이미지 생성 모델 이상입니다. multimodal foundation model을 개념화하고 구축하는 방식의 패러다임 전환을 나타냅니다. 기술적 benchmark를 넘어선 기여를 통해 generative model이 perception, 인터페이스 설계, 인지 모델링에서 맡는 역할을 재고하도록 커뮤니티에 도전장을 내밉니다.