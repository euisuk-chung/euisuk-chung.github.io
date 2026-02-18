---
title: "[Paper Review] Qwen-VL: A Versatile Vision-Language Model for Understanding, Localization, Text Reading, and Beyond"
date: "2025-08-29"
tags:
  - "paper-review"
year: "2025"
---

# [Paper Review] Qwen-VL: A Versatile Vision-Language Model for Understanding, Localization, Text Reading, and Beyond

![](https://velog.velcdn.com/images/euisuk-chung/post/019b662c-e53d-4068-9c38-0f6f33ddd422/image.png)

> <https://arxiv.org/abs/2308.12966>

```
WANG, Peng, et al. Qwen2-vl: Enhancing vision-language model's perception of the world at any resolution. arXiv preprint arXiv:2409.12191, 2024.
```

초록
--

본 연구에서는 텍스트와 이미지를 모두 인식하고 이해하도록 설계된 대규모 vision-language 모델(LVLM)인 Qwen-VL 시리즈를 소개합니다. Qwen-LM을 기반으로 시작하여, 세심하게 설계된 (i) visual receptor, (ii) input-output interface, (iii) 3단계 training pipeline, (iv) 다국어 multimodal 정제 코퍼스를 통해 visual capacity를 부여했습니다. 기존의 이미지 설명 및 질의응답을 넘어서, image-caption-box tuple을 정렬하여 Qwen-VL의 grounding 및 text-reading 능력을 구현했습니다. Qwen-VL과 Qwen-VL-Chat을 포함한 결과 모델들은 비슷한 모델 규모의 generalist 모델들 중에서 다양한 visual-centric benchmark(예: 이미지 캡셔닝, 질의응답, visual grounding)와 다양한 설정(예: zero-shot, few-shot)에서 새로운 기록을 달성했습니다. 또한 실제 대화 benchmark에서도 instruction-tuned된 Qwen-VL-Chat이 기존 vision-language chatbot들에 비해 우수성을 보여줍니다. 모든 모델은 향후 연구를 촉진하기 위해 공개됩니다.

1. 서론
-----

최근 Large Language Model(LLM) (Brown et al., 2020; OpenAI, 2023; Anil et al., 2023; Gao et al., 2023; Qwen, 2023)들이 텍스트 생성 및 이해의 강력한 능력으로 인해 큰 주목을 받고 있습니다. 이러한 모델들은 instruction fine-tuning을 통해 사용자 의도와 더욱 잘 정렬될 수 있으며, 강력한 상호작용 능력과 지능형 어시스턴트로서 생산성을 향상시킬 수 있는 잠재력을 보여줍니다.

그러나 native large language model들은 순수한 텍스트 세계에만 존재하며, 다른 일반적인 modality(이미지, 음성, 비디오 등)를 처리할 수 있는 능력이 부족해 응용 범위에 큰 제약이 있습니다. 이러한 동기로, 대규모 언어 모델을 시각적 신호를 인식하고 이해할 수 있는 능력으로 향상시킨 Large Vision Language Model(LVLM) 그룹 (Alayrac et al., 2022; Chen et al., 2022; Li et al., 2023c; Dai et al., 2023; Huang et al., 2023; Peng et al., 2023; Zhu et al., 2023; Liu et al., 2023; Ye et al., 2023b,a; Chen et al., 2023a; Li et al., 2023a; Zhang et al., 2023; Sun et al., 2023; OpenAI, 2023)이 개발되었습니다. 이러한 대규모 vision-language 모델들은 실제 vision-central 문제 해결에서 유망한 잠재력을 보여줍니다.

그럼에도 불구하고 LVLM의 한계와 잠재력을 탐구하기 위한 많은 연구가 수행되었음에도, 현재 오픈소스 LVLM들은 항상 부적절한 훈련과 최적화로 인해 어려움을 겪고 있으며, 이는 독점 모델들(Chen et al., 2022, 2023b; OpenAI, 2023)보다 훨씬 뒤처져 있어 오픈소스 커뮤니티에서의 LVLM에 대한 추가적인 탐구와 응용을 저해하고 있습니다. 더욱이 실제 시각적 시나리오는 상당히 복잡하므로, 세밀한 시각적 이해가 LVLM이 사람들을 효과적이고 정확하게 도울 수 있는 핵심적인 역할을 합니다. 그러나 이 방향으로는 소수의 시도만이 이루어졌으며(Peng et al., 2023; Chen et al., 2023a), 대부분의 오픈소스 LVLM들은 여전히 거친 방식으로 이미지를 인식하고 있으며 object grounding이나 text reading과 같은 세밀한 인식을 수행할 수 있는 능력이 부족합니다.

본 논문에서는 이러한 문제에 대한 해결책을 모색하고 오픈소스 Qwen 패밀리의 최신 구성원인 Qwen-VL 시리즈를 제시합니다. Qwen-VL들은 Qwen-7B (Qwen, 2023) 언어 모델을 기반으로 한 고성능이고 다재다능한 vision-language foundation 모델 시리즈입니다. 언어 정렬된 visual encoder와 위치 인식 adapter를 포함한 새로운 visual receptor를 도입하여 LLM basement에 visual capacity를 부여했습니다. 전체 모델 아키텍처와 input-output interface는 상당히 간결하며, 방대한 image-text corpus collection에서 전체 모델을 최적화하기 위해 3단계 training pipeline을 정교하게 설계했습니다.

사전 훈련된 checkpoint인 Qwen-VL은 시각적 입력을 인식하고 이해하며, 주어진 prompt에 따라 원하는 응답을 생성하고, 이미지 캡셔닝, 질의응답, 텍스트 지향 질의응답, visual grounding과 같은 다양한 vision-language 작업을 수행할 수 있습니다. Qwen-VL-Chat은 Qwen-VL을 기반으로 한 instruction-tuned vision-language chatbot입니다. 그림 2에 나타난 바와 같이, Qwen-VL-Chat은 사용자와 상호작용하고 사용자의 의도에 따라 입력 이미지를 인식할 수 있습니다.

구체적으로, Qwen-VL 시리즈 모델의 특징은 다음과 같습니다:

• **최고의 성능**: Qwen-VL들은 비슷한 규모의 counterpart들에 비해 다양한 vision-centric 이해 benchmark에서 최고 수준의 정확도를 달성했습니다. 또한 Qwen-VL의 뛰어난 성능은 기존 benchmark(예: captioning, question-answering, grounding) 뿐만 아니라 최근에 도입된 일부 대화 benchmark에서도 확인됩니다.

• **다국어**: Qwen-LM과 마찬가지로, Qwen-VL들은 상당한 양의 corpus가 영어와 중국어로 구성된 다국어 image-text 데이터로 훈련되었습니다. 이러한 방식으로 Qwen-VL들은 영어, 중국어 및 다국어 instruction을 자연스럽게 지원합니다.

• **Multi-image**: 훈련 단계에서 임의로 interleaved된 image-text 데이터를 Qwen-VL의 입력으로 허용합니다. 이 기능을 통해 Qwen-Chat-VL은 여러 이미지가 주어졌을 때 context를 비교, 이해 및 분석할 수 있습니다.

• **세밀한 시각적 이해**: 훈련에서 사용한 더 높은 해상도의 입력 크기와 세밀한 corpus 덕분에, Qwen-VL들은 높은 경쟁력을 가진 세밀한 시각적 이해 능력을 보여줍니다. 기존 vision-language generalist들과 비교해, Qwen-VL들은 grounding, text-reading, 텍스트 지향 질의응답, 세밀한 대화 성능에서 훨씬 더 나은 성능을 보입니다.

2. 방법론
------

### 2.1 모델 아키텍처

Qwen-VL의 전체 네트워크 아키텍처는 세 가지 구성 요소로 이루어져 있으며, 모델 parameter의 세부 사항은 표 1에 나와 있습니다:

**Large Language Model**: Qwen-VL은 large language model을 기초 구성 요소로 채택합니다. 모델은 Qwen-7B (Qwen, 2023)의 사전 훈련된 weights로 초기화됩니다.

**Visual Encoder**: Qwen-VL의 visual encoder는 Vision Transformer (ViT) (Dosovitskiy et al., 2021) 아키텍처를 사용하며, Openclip의 ViT-bigG (Ilharco et al., 2021)의 사전 훈련된 weights로 초기화됩니다. 훈련 및 추론 과정에서 입력 이미지는 특정 해상도로 크기가 조정됩니다. visual encoder는 이미지를 stride 14로 patch들로 분할하여 처리하고, 이미지 feature들의 set을 생성합니다.

**Position-aware Vision-Language Adapter**: 긴 이미지 feature sequence로 인한 효율성 문제를 완화하기 위해, Qwen-VL은 이미지 feature들을 압축하는 vision-language adapter를 도입합니다. 이 adapter는 무작위로 초기화된 single-layer cross-attention module로 구성됩니다. 모듈은 trainable vector들(Embedding) 그룹을 query vector로 사용하고, visual encoder의 이미지 feature들을 cross-attention 연산의 key로 사용합니다. 이 메커니즘은 visual feature sequence를 256의 고정 길이로 압축합니다. query 수에 대한 ablation은 부록 E.2에 나와 있습니다. 또한 세밀한 이미지 이해를 위한 위치 정보의 중요성을 고려하여, 압축 중 위치 세부 사항의 잠재적 손실을 완화하기 위해 2D absolute positional encoding이 cross-attention 메커니즘의 query-key pair에 통합됩니다. 길이 256의 압축된 이미지 feature sequence는 이후 large language model에 입력됩니다.

### 2.2 입력 및 출력

**Image Input**: 이미지는 visual encoder와 adapter를 통해 처리되어 고정 길이의 이미지 feature sequence를 생성합니다. 이미지 feature 입력과 텍스트 feature 입력을 구별하기 위해, 두 개의 특수 토큰(![]()와 )이 이미지 feature sequence의 시작과 끝에 각각 추가되어 이미지 콘텐츠의 시작과 끝을 나타냅니다.

**Bounding Box Input and Output**: 모델의 세밀한 시각적 이해 및 grounding capacity를 향상시키기 위해, Qwen-VL의 훈련에는 지역 설명, 질문 및 detection 형태의 데이터가 포함됩니다. 이미지-텍스트 설명이나 질문을 포함하는 기존 작업과 달리, 이 작업은 모델이 지정된 형식으로 지역 설명을 정확하게 이해하고 생성해야 합니다. 주어진 bounding box에 대해 정규화 과정([0, 1000) 범위 내)이 적용되고 지정된 문자열 형식으로 변환됩니다: "(X\_topleft, Y\_topleft),(X\_bottomright, Y\_bottomright)". 이 문자열은 텍스트로 토큰화되며 추가적인 위치 vocabulary가 필요하지 않습니다. detection 문자열과 일반 텍스트 문자열을 구별하기 위해, 두 개의 특수 토큰(와 )이 bounding box 문자열의 시작과 끝에 추가됩니다. 또한 bounding box를 해당하는 설명 단어나 문장과 적절히 연관시키기 위해, 또 다른 특수 토큰 set(와 )이 도입되어 bounding box가 참조하는 내용을 표시합니다.

3. 훈련
-----

그림 3에 나타난 바와 같이, Qwen-VL 모델의 훈련 과정은 세 단계로 구성됩니다: 두 단계의 pre-training과 마지막 instruction fine-tuning 훈련 단계입니다.

### 3.1 Pre-training

첫 번째 pre-training 단계에서는 주로 대규모의 weakly labeled, 웹에서 크롤링된 image-text pair set을 사용합니다. 사전 훈련 데이터셋은 여러 공개적으로 접근 가능한 소스와 일부 in-house 데이터로 구성됩니다. 특정 패턴의 데이터셋을 정리하기 위해 노력했습니다. 표 2에 요약된 바와 같이, 원래 데이터셋은 총 50억 개의 image-text pair를 포함하고 있으며, 정리 후 14억 개의 데이터가 남았고, 그 중 77.3%가 영어(텍스트) 데이터, 22.7%가 중국어(텍스트) 데이터입니다.

이 단계에서는 large language model을 동결하고 vision encoder와 VL adapter만 최적화합니다. 입력 이미지는 224 × 224로 크기가 조정됩니다. 훈련 목적은 텍스트 토큰의 cross-entropy를 최소화하는 것입니다. 최대 learning rate는 2e^-4이며, 훈련 과정은 image-text pair에 대해 batch size 30720을 사용하고, 전체 첫 번째 pre-training 단계는 50,000 step 동안 지속되어 약 15억 개의 image-text sample을 소비합니다. 더 많은 hyperparameter는 부록 C에 자세히 나와 있고, 이 단계의 수렴 곡선은 그림 6에 나타나 있습니다.

### 3.2 Multi-task Pre-training

두 번째 multi-task pre-training 단계에서는 더 큰 입력 해상도와 interleaved image-text 데이터를 사용하여 고품질의 세밀한 VL annotation 데이터를 도입합니다. 표 3에 요약된 바와 같이, 7개의 작업을 동시에 Qwen-VL에서 훈련했습니다. 텍스트 생성의 경우, LLM의 능력을 유지하기 위해 in-house 수집된 corpus를 사용합니다. Captioning 데이터는 LAION-COCO를 제외하고 훨씬 적은 sample로 표 2와 동일합니다. VQA 작업을 위해 GQA (Hudson and Manning, 2019), VGQA (Krishna et al., 2017), VQAv2 (Goyal et al., 2017), DVQA (Kafle et al., 2018), OCR-VQA (Mishra et al., 2019) 및 DocVQA (Mathew et al., 2021)를 포함하는 공개적으로 사용 가능한 데이터의 혼합을 사용합니다. Kosmos-2를 따라 grounding 작업을 위해 약간의 수정과 함께 GRIT (Peng et al., 2023) 데이터셋을 사용합니다. reference grounding과 grounded captioning duality 작업의 경우, GRIT (Peng et al., 2023), Visual Genome (Krishna et al., 2017), RefCOCO (Kazemzadeh et al., 2014), RefCOCO+, RefCOCOg (Mao et al., 2016)에서 훈련 sample을 구성합니다. 텍스트 지향 작업을 개선하기 위해 Common Crawl에서 PDF와 HTML 형식 데이터를 수집하고 (Kim et al., 2022)를 따라 자연 풍경 배경으로 영어와 중국어 언어로 합성 OCR 데이터를 생성합니다. 마지막으로 동일한 작업 데이터를 길이 2048의 sequence로 패킹하여 interleaved image-text 데이터를 간단히 구성합니다.

visual encoder의 입력 해상도를 224 × 224에서 448 × 448로 증가시켜 이미지 다운샘플링으로 인한 정보 손실을 줄입니다. 또한 더 높은 해상도의 vision transformer에 대해 window attention과 global attention을 부록 E.3에서 ablation합니다. large language model의 잠금을 해제하고 전체 모델을 훈련했습니다. 훈련 목적은 pre-training 단계와 동일합니다.

### 3.3 Supervised Fine-tuning

이 단계에서는 instruction fine-tuning을 통해 Qwen-VL 사전 훈련 모델을 fine-tune하여 instruction following 및 대화 능력을 향상시켜 상호작용 가능한 Qwen-VL-Chat 모델을 만들었습니다. multi-modal instruction tuning 데이터는 주로 LLM self-instruction을 통해 생성된 caption 데이터나 대화 데이터에서 나오며, 이는 종종 single-image 대화와 추론만을 다루고 이미지 내용 이해에 제한됩니다. localization과 multi-image 이해 능력을 Qwen-VL 모델에 통합하기 위해 manual annotation, 모델 생성, strategy concatenation을 통해 추가 대화 데이터 set을 구성했습니다. 모델이 이러한 능력을 더 넓은 범위의 언어와 질문 유형으로 효과적으로 전이한다는 것을 확인했습니다. 또한 훈련 중에 multi-modal과 순수 텍스트 대화 데이터를 혼합하여 대화 능력에서 모델의 보편성을 보장합니다. instruction tuning 데이터는 350k개입니다. 이 단계에서는 visual encoder를 동결하고 language model과 adapter module을 최적화합니다. 이 단계의 데이터 형식은 부록 B.2에서 보여줍니다.

4. 평가
-----

본 섹션에서는 다양한 multi-modal 작업에 대한 전반적인 평가를 수행하여 모델의 시각적 이해 능력을 종합적으로 평가합니다. 이하에서 Qwen-VL은 multi-task 훈련 후의 모델을 의미하고, Qwen-VL-Chat은 supervised fine-tuning (SFT) 단계 후의 모델을 의미합니다.

표 9는 사용된 평가 benchmark와 해당 metric에 대한 상세한 요약을 제공합니다.

### 4.1 Image Caption 및 일반적인 Visual Question Answering

Image caption과 일반적인 visual question answering (VQA)은 vision-language 모델을 위한 두 가지 기존 작업입니다. 구체적으로, image caption은 모델이 주어진 이미지에 대한 설명을 생성하도록 요구하고, 일반적인 VQA는 주어진 image-question pair에 대한 답변을 생성하도록 요구합니다.

image caption 작업의 경우, Nocaps (Agrawal et al., 2019)와 Flickr30K (Young et al., 2014)를 benchmark로 선택하고 CIDEr score (Vedantam et al., 2015)를 metric으로 보고합니다. "Describe the image in English:"라는 prompt로 caption 생성에 greedy search를 사용합니다.

일반적인 VQA의 경우, VQAv2 (Goyal et al., 2017), OKVQA (Marino et al., 2019), GQA (Hudson and Manning, 2019), ScienceQA (Image Set) (Lu et al., 2022b), VizWiz VQA (Gurari et al., 2018)를 포함한 다섯 개의 benchmark를 사용합니다. VQAv2, OKVQA, GQA, VizWiz VQA의 경우, 모델의 출력 공간에 제약 없이 greedy decoding strategy와 "{question} Answer:"라는 prompt로 개방형 답변 생성을 사용합니다. 그러나 ScienceQA의 경우, 모델의 출력을 가능한 선택지로 제한하고(개방형이 아닌), 가장 높은 신뢰도를 가진 선택지를 모델의 예측으로 선택하며, Top-1 정확도를 보고합니다.

image caption과 일반적인 VQA 작업의 전반적인 성능은 표 4에 보고됩니다. 결과에서 보듯이, Qwen-VL과 Qwen-VL-Chat 모두 두 작업 모두에서 이전 generalist 모델들에 비해 명백히 더 나은 결과를 달성했습니다. 구체적으로, zero-shot image caption 작업에서 Qwen-VL은 Flickr30K karpathy-test split에서 state-of-the-art 성능(즉, 85.8 CIDEr score)을 달성했으며, 훨씬 많은 parameter를 가진 이전 generalist 모델들(예: 80B parameter를 가진 Flamingo-80B)을 능가하기까지 했습니다.

일반적인 VQA benchmark에서도 모델들이 다른 모델들에 비해 뚜렷한 장점을 보여줍니다. VQAv2, OKVQA, GQA benchmark에서 Qwen-VL은 각각 79.5, 58.6, 59.3의 정확도를 달성하여 최근 제안된 LVLM들을 큰 폭으로 능가합니다. 주목할 점은 Qwen-VL이 ScienceQA와 VizWiz 데이터셋에서도 강한 zero-shot 성능을 보인다는 것입니다.

### 4.2 텍스트 지향 Visual Question Answering

텍스트 지향 시각적 이해는 실제 시나리오에서 광범위한 응용 전망을 가지고 있습니다. TextVQA (Sidorov et al., 2020), DocVQA (Mathew et al., 2021), ChartQA (Masry et al., 2022), AI2Diagram (Kembhavi et al., 2016), OCR-VQA (Mishra et al., 2019)를 포함한 여러 benchmark에서 텍스트 지향 visual question answering에 대한 모델의 능력을 평가합니다. 마찬가지로 결과는 표 5에 나와 있습니다. 이전 generalist 모델들과 최근 LVLM들에 비해, 모델들이 대부분의 benchmark에서 더 나은 성능을 보이며, 종종 큰 폭으로 앞서는 것을 보여줍니다.

### 4.3 Refer Expression Comprehension

RefCOCO (Kazemzadeh et al., 2014), RefCOCOg (Mao et al., 2016), RefCOCO+ (Mao et al., 2016), GRIT (Gupta et al., 2022)와 같은 refer expression comprehension benchmark를 평가하여 모델의 세밀한 이미지 이해와 localization 능력을 보여줍니다. 구체적으로, refer expression comprehension 작업은 모델이 설명의 안내하에 대상 객체를 localize하도록 요구합니다. 결과는 표 6에 나와 있습니다. 이전 generalist 모델들이나 최근 LVLM들에 비해, 모델들이 모든 benchmark에서 최고 수준의 결과를 얻습니다.

### 4.4 Vision-Language 작업에서의 Few-shot Learning

모델은 만족스러운 in-context learning(a.k.a., few-shot learning) 능력도 보여줍니다. 그림 4에 나타난 바와 같이, Qwen-VL은 비슷한 수의 parameter를 가진 모델들(Flamingo-9B(Alayrac et al., 2022), OpenFlamingo-9B, IDEFICS-9B)과 비교했을 때 OKVQA (Marino et al., 2019), Vizwiz (Gurari et al., 2018), TextVQA (Sidorov et al., 2020), Flickr30k (Young et al., 2014)에서 in-context few-shot learning을 통해 더 나은 성능을 달성합니다. Qwen-VL의 성능은 훨씬 큰 모델들(Flamingo-80B와 IDEFICS-80B)과도 비교할 만합니다. 더 나은 결과가 달성될 수 있음에도 불구하고 RICES (Yang et al., 2022b)와 같은 정교한 few-shot exemplar 구성 방법은 사용하지 않고 naive random sample을 채택하여 few-shot exemplar를 구성했다는 점을 참고하시기 바랍니다.

### 4.5 실제 사용자 행동에서의 Instruction Following

이전의 기존 vision-language 평가 외에도, 실제 사용자 행동 하에서 Qwen-VL-Chat 모델의 capacity를 평가하기 위해 TouchStone (Bai et al., 2023), SEED-Bench (Li et al., 2023b), MME (Fu et al., 2023)에 대한 평가를 추가로 수행했습니다. TouchStone은 개방형 vision-language instruction-following benchmark입니다. TouchStone benchmark에서 영어와 중국어 모두에서 다른 instruction-tuned LVLM들과 Qwen-VL-Chat의 instruction-following 능력을 비교합니다. SEED-Bench는 Multimodal LLM을 평가하기 위한 정확한 인간 annotation이 있는 19K개의 객관식 문제로 구성되어 있으며, 공간적 및 시간적 이해를 모두 포함하는 12개의 평가 차원을 다룹니다. MME는 총 14개의 subtask에서 perception과 cognition 능력을 모두 측정합니다.

세 benchmark에 대한 결과는 표 7에 나와 있습니다. Qwen-VL-Chat은 세 데이터셋 모두에서 다른 LVLM들에 비해 명백한 장점을 달성했으며, 이는 모델이 다양한 사용자 instruction을 이해하고 답변하는 데 더 나은 성능을 보인다는 것을 나타냅니다. SEED-Bench에서는 단순히 네 개의 frame을 샘플링하여 모델의 시각적 능력이 비디오 작업에 효과적으로 전이될 수 있음을 발견했습니다. TouchStone에서 제시된 전반적인 점수 면에서, 모델은 다른 LVLM들에 비해 특히 중국어 능력에서 명확한 장점을 보여줍니다. 능력의 광범위한 범주 면에서, 모델은 이해와 인식에서 더 두드러진 장점을 보이며, 특히 텍스트 인식과 차트 분석과 같은 영역에서 그렇습니다. 더 자세한 정보는 TouchStone 데이터셋을 참조하시기 바랍니다.

5. 관련 연구
--------

최근 몇 년간 연구자들은 vision-language learning에 상당한 관심을 보여왔으며, 특히 multi-task generalist 모델 개발에서 그렇습니다. CoCa (Yu et al., 2022)는 image-text retrieval과 vision-language 생성 작업을 동시에 다루기 위해 encoder-decoder 구조를 제안합니다. OFA (Wang et al., 2022a)는 사용자 지정 작업 instruction을 사용하여 특정 vision-language 작업을 sequence-to-sequence 작업으로 변환합니다. Unified I/O (Lu et al., 2022a)는 segmentation과 depth estimation과 같은 더 많은 작업을 통합된 프레임워크로 도입합니다.

다른 연구 범주는 vision-language representation 모델 구축에 집중합니다. CLIP (Radford et al., 2021)은 contrastive learning과 대량의 데이터를 활용하여 semantic space에서 이미지와 언어를 정렬하여 다양한 downstream 작업에서 강력한 일반화 능력을 가져옵니다. BEIT-3 (Wang et al., 2022b)는 mixture-of-experts (MOE) 구조와 통합된 masked token prediction objective를 사용하여 다양한 visual-language 작업에서 state-of-the-art 결과를 달성합니다. vision-language learning 외에도, ImageBind (Girdhar et al., 2023)와 ONE-PEACE (Wang et al., 2023)는 음성과 같은 더 많은 modality를 통합된 semantic space로 정렬하여 더 일반적인 representation 모델을 만듭니다.

상당한 진전을 달성했음에도 불구하고, 이전 vision-language 모델들은 여전히 instruction following에서의 낮은 견고성, 미지의 작업에서 제한된 일반화 능력, in-context 능력의 부족과 같은 여러 한계를 가지고 있습니다. Large Language Model (LLM)의 급속한 발전과 함께, 연구자들은 LLM을 기반으로 더 강력한 large vision-language model (LVLM)을 구축하기 시작했습니다. BLIP-2 (Li et al., 2023c)는 동결된 vision foundation 모델과 LLM을 정렬하기 위해 Q-Former를 제안합니다. 한편, LLAVA (Liu et al., 2023)와 MiniGPT4 (Zhu et al., 2023)는 LVLM에서 instruction following 능력을 향상시키기 위해 visual instruction tuning을 도입합니다. 추가적으로, mPLUG-DocOwl (Ye et al., 2023a)은 디지털 문서 데이터를 도입하여 LVLM에 문서 이해 능력을 통합합니다. Kosmos2 (Peng et al., 2023), Shikra (Chen et al., 2023a), BuboGPT (Zhao et al., 2023)는 visual grounding 능력으로 LVLM을 더욱 향상시켜 지역 설명과 localization을 가능하게 합니다. 본 연구에서는 image captioning, visual question answering, OCR, document understanding, visual grounding 능력을 Qwen-VL에 통합합니다. 결과 모델은 이러한 다양한 스타일의 작업에서 뛰어난 성능을 달성합니다.

6. 결론 및 향후 연구
-------------

multimodal 연구를 촉진하는 것을 목표로 하는 대규모 다국어 vision-language 모델 세트인 Qwen-VL 시리즈를 출시했습니다. Qwen-VL은 다양한 benchmark에서 비슷한 모델들을 능가하며, 다국어 대화, multi-image interleaved 대화, 중국어 grounding, 세밀한 인식을 지원합니다. 앞으로 여러 핵심 차원에서 Qwen-VL의 능력을 더욱 향상시키는 데 전념하고 있습니다:

• 음성 및 비디오와 같은 더 많은 modality와 Qwen-VL을 통합합니다.  
• 모델 크기, 훈련 데이터 및 더 높은 해상도를 확장하여 Qwen-VL을 증강하고, multimodal 데이터 내에서 더 복잡하고 복잡한 관계를 처리할 수 있게 합니다.  
• 특히 고품질 이미지와 유창한 음성 생성에서 multi-modal 생성에 대한 Qwen-VL의 기량을 확장합니다.