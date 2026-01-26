---
title: "[Paper Review] Qwen-Audio: Advancing Universal Audio Understanding via Unified Large-Scale Audio-Language Models"
date: "2025-08-29"
year: "2025"
---

# [Paper Review] Qwen-Audio: Advancing Universal Audio Understanding via Unified Large-Scale Audio-Language Models


![](https://velog.velcdn.com/images/euisuk-chung/post/886942db-9c26-422a-831a-3dd7e89263a4/image.png)

> <https://arxiv.org/abs/2311.07919>

```
CHU, Yunfei, et al. Qwen-audio: Advancing universal audio understanding via unified large-scale audio-language models. arXiv preprint arXiv:2311.07919, 2023.
```

Abstract
--------

최근 instruction-following audio-language 모델들이 인간과의 오디오 상호작용에서 광범위한 관심을 받고 있습니다. 그러나 다양한 오디오 유형과 작업을 처리할 수 있는 사전 훈련된 오디오 모델의 부재가 이 분야의 발전을 저해하고 있습니다. 결과적으로 기존의 대부분의 연구들은 제한된 범위의 상호작용 기능만을 지원할 수 있었습니다.

본 논문에서는 Qwen-Audio 모델을 개발하여 이러한 한계를 해결하고자 합니다. 인간 음성, 자연음, 음악, 노래 등 다양한 오디오 유형을 포함하여 30개 이상의 작업을 다루는 audio-language 사전 훈련을 확장함으로써 범용 오디오 이해 능력을 촉진합니다.

그러나 모든 작업과 데이터셋을 직접 공동 훈련하면 간섭 문제가 발생할 수 있습니다. 이는 작업 초점, 언어, 주석 세분화 및 텍스트 구조의 차이로 인해 서로 다른 데이터셋과 연관된 텍스트 레이블에 상당한 변화가 있기 때문입니다.

이러한 one-to-many 간섭을 극복하기 위해, 우리는 계층적 태그 시퀀스를 조건으로 하는 decoder를 통해 지식 공유를 장려하고 공유 태그와 특정 태그를 각각 통해 간섭을 방지하는 multi-task 훈련 framework를 신중하게 설계했습니다.

주목할 점은 Qwen-Audio가 작업별 fine-tuning 없이도 다양한 벤치마크 작업에서 인상적인 성능을 달성하여 기존 모델들을 능가한다는 것입니다. Qwen-Audio의 기능을 기반으로, 우리는 다양한 오디오와 텍스트 입력을 허용하고 multi-turn dialogue를 가능하게 하며 다양한 오디오 중심 시나리오를 지원하는 Qwen-Audio-Chat을 추가로 개발했습니다.

1. Introduction
---------------

Large Language Models (LLMs)는 강력한 지식 보존, 복잡한 추론 및 문제 해결 능력으로 인해 일반 인공지능(AGI) 분야의 발전을 크게 촉진했습니다. 그러나 언어 모델은 인간처럼 이미지나 오디오와 같은 비텍스트 modality를 인식하는 능력이 부족합니다.

음성은 중요한 modality로서, 인간 음성의 감정, 톤, 의도, 자연음의 기차 기적, 시계 종소리, 천둥, 그리고 음악의 멜로디 등 텍스트를 넘어서는 다양하고 복잡한 신호를 제공합니다. LLMs가 오디오 상호작용을 위해 풍부한 오디오 신호를 인식하고 이해할 수 있도록 하는 것은 광범위한 관심을 받고 있습니다.

기존의 instruction following 연구들은 주로 large (multimodal) LLMs의 능력을 상속받고 가벼운 supervised fine-tuning을 채택하여 사용자 의도에 맞춰 모델의 능력을 활성화했습니다. 그러나 대부분의 연구들은 다양한 오디오 유형과 작업을 처리할 수 있는 사전 훈련된 audio-language 모델의 부족으로 인해 오디오 상호작용 능력 면에서 제약을 받았습니다.

기존의 대표적인 audio-language multi-task language 모델들인 SpeechNet, SpeechT5, VIOLA, Whisper, Pengi 등은 인간 음성이나 자연음과 같은 특정 오디오 유형 처리에 제한되어 있습니다.

audio-text multimodal 커뮤니티의 성장과 발전을 촉진하기 위해, 우리는 대규모 audio-language 모델인 Qwen-Audio를 소개합니다. Qwen-Audio는 오디오와 텍스트 입력을 조건으로 하는 multi-task language 모델로, 단일 audio encoder의 연결을 통해 오디오 신호를 효과적으로 인식하도록 Qwen-7B language 모델을 확장합니다.

주로 인간 음성과 같은 단일 오디오 유형에 초점을 맞추거나 음성 인식 및 캡션과 같은 특정 작업에 집중하거나 단일 언어로 모델을 제한하는 이전 연구들과 달리, 우리는 범용 오디오 이해 능력 발전을 위해 8개 언어와 다양한 유형의 오디오를 포함하여 30개 이상의 작업을 다루는 수십 개의 데이터셋으로 훈련을 확장했습니다.

multi-task 학습의 중요한 과제는 서로 다른 데이터셋과 연관된 텍스트 레이블의 상당한 변화에서 발생합니다. 이러한 변화는 작업 초점, 언어, 주석 세분화 및 텍스트 구조(구조화 또는 비구조화)의 차이에서 비롯됩니다. 이러한 one-to-many 문제를 해결하기 위해, 우리는 계층적 태그의 시퀀스를 조건으로 하는 decoder를 통해 지식 공유를 장려하고 공유 태그와 특정 태그를 각각 통해 간섭을 완화하는 multi-task 훈련 framework를 신중하게 설계했습니다.

또한, 우리는 이전 multi-task 학습 연구에서 일반적으로 무시되는 word-level time-stamp 예측(SRWT) 작업과 함께 음성 인식을 훈련에 통합합니다. 이 작업이 음성 신호를 넘어선 소리와 음악 등의 grounding 및 grounding 기반 QA 작업을 개선할 뿐만 아니라 ASR 성능도 향상시킨다는 것을 발견했습니다.

Figure 1에서 보듯이, 광범위한 평가를 통해 Qwen-Audio가 작업별 fine-tuning 없이도 다양한 작업 범위에서 이전 multi-task 훈련 모델들을 능가한다는 것을 보여줍니다. Qwen-Audio의 주목할 만한 성과는 Aishell1, cochlscene, ClothoAQA, VocalSound의 테스트 셋에서 최첨단 성능을 달성한 것입니다.

Qwen-Audio의 기능을 활용하여, 우리는 supervised instruction fine-tuning을 통해 Qwen-Audio-Chat을 소개합니다. 이는 multi-turn dialogue에서 오디오와 텍스트 modality 모두로부터 유연한 입력을 가능하게 하며, 인간 지시사항에 따른 효과적인 상호작용을 가능하게 합니다.

### 본 논문의 기여도:

• 다양한 작업, 언어 및 오디오 유형을 지원하는 범용 오디오 이해 모델 역할을 하는 기본 multi-task audio-language 모델인 Qwen-Audio를 소개합니다. Qwen-Audio를 기반으로 instruction fine-tuning을 통해 Qwen-Audio-Chat을 개발하여 multi-turn dialogue를 가능하게 하고 다양한 오디오 지향 시나리오를 지원합니다. Qwen-Audio와 Qwen-Audio-Chat 모델 모두 오픈소스로 제공되어 audio-text multimodal 커뮤니티의 성장과 발전을 촉진합니다.

• audio-language 사전 훈련을 확장하기 위해, 서로 다른 데이터셋과 연관된 텍스트 레이블의 변화 문제를 multi-task 훈련 framework를 제안하여 해결하고, 지식 공유를 가능하게 하며 one-to-many 간섭을 방지합니다. 우리 모델은 30개 이상의 작업을 통합하며 광범위한 실험을 통해 강력한 성능을 달성함을 보여줍니다.

• audio-language 사전 훈련을 촉진하기 위해, 오디오 multimodal 연구 커뮤니티에서 종종 간과되는 SRWT 작업을 통합하는 것이 음성 신호를 넘어선 grounding 및 grounding 기반 질문 답변 작업과 ASR 성능을 개선한다는 것을 보여줍니다.

• 실험 결과는 Qwen-Audio가 작업별 fine-tuning 없이도 다양한 벤치마크 작업에서 인상적인 성능을 달성하여 기존 모델들을 능가한다는 것을 보여줍니다. 특히, Qwen-Audio는 Aishell1, cochlscene, ClothoAQA, VocalSound의 테스트 셋에서 최첨단 결과를 달성합니다.

2. Related Work
---------------

### Multi-task Audio-Text Learning

multi-task 훈련의 목표는 통합된 모델 아키텍처와 데이터 형식을 통해 서로 다른 작업 간에 지식을 전달하는 것입니다. 오디오 처리 영역에서는 인간 음성, 자연음, 음악, 노래와 같은 다양한 오디오 신호가 존재하고 이들의 라벨링 형식이 크게 다르기 때문에 모든 오디오 처리 작업을 통합하는 것이 어렵습니다.

SpeechNet과 SpeechT5는 인간 음성 작업을 speech/text 입력 및 speech/text 출력 형식으로 처리하고, 사전 훈련을 위한 공유 encoder-decoder framework를 활용합니다. 많은 연구들이 speech representation을 직접 공급하거나 연속적인 음성 신호를 discrete codes로 인코딩하여 데이터 형식과 작업을 통합하고, 서로 다른 인간 음성 작업을 조건부 생성 작업으로 처리합니다.

VoiceBox는 인간 음성 합성 및 음성 편집 작업을 위해 non-autoregressive continuous normalizing flow 모델을 사용합니다. Whisper는 데이터셋 주석의 세분화(문장 수준 타임스탬프 유무)와 작업 유형(인간 음성 인식 및 번역)을 고려한 multi-task 훈련을 위한 템플릿을 제안합니다.

이전 연구들은 대부분 음성 인식 및 번역과 같은 인간 음성 처리 작업에만 초점을 맞추고 자연음이나 음악과 같은 다른 오디오 유형을 무시합니다. Pengi는 자연음 이해 작업에 초점을 맞추고 이러한 작업을 텍스트 생성 작업으로 처리합니다.

본 연구에서 Qwen-Audio는 인간 음성, 자연음, 음악, 노래와 같은 다양한 오디오 유형을 통합하고, 이질적인 데이터에서 소싱되고 서로 다른 라벨링 세분화를 특징으로 하는 데이터셋에서의 공동 훈련을 촉진합니다. 이는 통합된 학습 framework의 도입을 통해 달성됩니다.

### Interact with LLMs through Multiple Modality

최근 ChatGPT와 같은 large language 모델들이 인간 지시사항에 따른 지식 보존, 추론, 코딩에서 인상적인 능력을 보여주었습니다. 순수 텍스트 작업을 넘어 LLMs의 적용 범위를 확장하기 위해, 많은 LLM 기반 multimodal 모델들이 개발되었습니다.

시각적 modality의 경우, GPT4, Flamingo, Kosmos, BLIP, Shikra, Emu, Qwen-VL 등이 LLMs에 대한 이미지 이해 또는 생성 능력을 가능하게 하는 다양한 통합 방법을 제안했습니다.

오디오 modality의 경우, AudioGPT와 HuggingGPT와 같이 잘 훈련된 오디오 foundation 모델들을 도구로 활용하면서 LLMs를 다양한 인터페이스로 활용하려는 시도들이 있었습니다. 이러한 노력들은 외부 도구를 제어하기 위한 명령을 생성하거나 인간 음성을 텍스트로 변환한 후 LLMs에 입력하도록 LLMs에 지시하는 것을 포함합니다.

그러나 이러한 접근 방식들은 인간 음성의 운율(prosody)과 감정과 같은 중요한 정보의 포함이 부족하며, 특정 경우에는 자연음과 같은 비텍스트 오디오를 변환하는 데 실패합니다. 결과적으로 LLMs에서 음성 modality로의 지식 전달에 장애물이 발생하고, LLMs는 오디오 신호를 인식하고 이해하는 데 필요한 능력이 부족합니다.

최근의 노력들은 직접적인 음성 상호작용을 위한 end-to-end audio-text LLMs 훈련을 탐구합니다. SpeechGPT는 먼저 인간 음성을 discrete HuBERT tokens로 변환하고, paired speech 데이터, speech instruction 데이터, chain-of-modality instruction 데이터에 대해 3단계 훈련 파이프라인을 설계합니다.

BLSP는 LLM이 인간 음성과 해당 전사를 제공받았을 때 동일한 텍스트 연속을 생성하도록 요구하여 representation을 정렬합니다. LLaSM은 Microsoft TTS API를 사용하여 음성 질문을 생성함으로써 대규모 음성 instruction 데이터셋을 생성하고, 인간 음성과 텍스트 간의 end-to-end 상호작용을 가능하게 하기 위한 훈련을 수행합니다.

LTU는 5M 오디오 QA 데이터셋을 생성하고, 소리 인식과 추론 간의 정렬을 향상시키기 위해 오디오 모듈과 LLaMA의 LoRA adapters에 대해 supervised finetuning (SFT)를 수행합니다.

SALMMON은 텍스트 encoder와 speech encoder를 모두 활용하여 다양한 종류의 오디오와 텍스트 입력에서 representation을 추출하고, Q-former 스타일 attention을 통해 잘 훈련된 LLM에 입력을 연결하여 응답을 생성합니다.

본 연구에서 Qwen-Audio는 텍스트 대화 능력을 보존하면서 오디오 입력을 인식하고 이해할 수 있는 통합된 audio-text multi-task multilingual LLMs 훈련을 목표로 합니다. Qwen-Audio는 모든 오디오에 대해 단일 encoder를 사용하고, 자연음 탐지, 인간 음성 인식 및 grounding, 오디오 캡션 작업과 같은 다양한 작업을 지원하기 위해 대규모 end-to-end 훈련을 통해 오디오와 텍스트 modality 간의 격차를 연결합니다.

3. Methodology
--------------

이 섹션은 범용 오디오 이해와 인간 지시사항을 기반으로 한 유연한 상호작용을 위해 설계된 Qwen-Audio와 Qwen-Audio-Chat의 세부사항을 제공합니다. Qwen-Audio와 Qwen-Audio-Chat의 모델 구조는 먼저 Section 3.1에서 제시됩니다.

우리 모델의 훈련 과정은 두 단계로 구성됩니다: multitask pretraining과 supervised fine-tuning입니다. Section 3.2에서는 multitask 학습을 통한 Qwen-Audio의 훈련을 설명합니다. 그런 다음 Section 3.3에서는 유연한 인간 상호작용을 가능하게 하는 supervised fine-tuning을 통한 Qwen-Audio-Chat을 설명합니다.

### 3.1 Model Architecture

Qwen-Audio 모델의 아키텍처는 Figure 3에 묘사되어 있습니다. Qwen-Audio는 audio encoder와 large language model을 포함합니다. paired 데이터 (a, x)가 주어졌을 때, 여기서 a와 x는 각각 오디오 시퀀스와 텍스트 시퀀스를 나타내며, 훈련 목표는 다음 텍스트 토큰 확률을 최대화하는 것입니다:

Pθ(xt∣x<t,Encoderϕ(a))P\_θ(x\_t|x\_{<t}, \text{Encoder}\_ϕ(a))Pθ​(xt​∣x<t​,Encoderϕ​(a))

이는 오디오 representation과 이전 텍스트 시퀀스 x<tx\_{<t}x<t​를 조건으로 하며, 여기서 θ와 ϕ는 각각 LLM과 audio encoder의 훈련 가능한 매개변수를 나타냅니다.

**Audio Encoder**: Qwen-Audio는 다양한 유형의 오디오를 처리하기 위해 단일 audio encoder를 사용합니다. audio encoder의 초기화는 Whisper-large-v2 모델을 기반으로 합니다. 이는 stem으로 두 개의 convolution down-sampling 레이어를 포함하는 32층 Transformer 모델입니다. audio encoder는 640M 개의 매개변수로 구성됩니다.

Whisper가 음성 인식과 번역을 위해 supervised 훈련되었지만, 그 인코딩된 representation은 여전히 배경 소음과 같은 풍부한 정보를 포함하며, 심지어 원본 음성을 복구하는 데도 사용될 수 있습니다.

오디오 데이터를 전처리하기 위해, Whisper는 이를 16kHz 주파수로 리샘플링하고 25ms의 window size와 10ms의 hop size를 사용하여 raw waveform을 80-channel mel-spectrogram으로 변환합니다. 또한, 오디오 representation의 길이를 줄이기 위해 stride가 2인 pooling 레이어가 통합됩니다. 결과적으로 encoder 출력의 각 프레임은 원본 오디오 신호의 약 40ms 세그먼트에 해당합니다. 훈련 시에는 데이터 증강으로 SpecAugment가 적용됩니다.

**Large Language Model**: Qwen-Audio는 foundational 구성 요소로 large language model을 통합합니다. 모델은 Qwen-7B에서 파생된 사전 훈련된 가중치를 사용하여 초기화됩니다. Qwen-7B는 4096의 hidden size를 가진 32층 Transformer decoder 모델로, 총 7.7B 매개변수를 포함합니다.

### 3.2 Multitask Pretraining

오디오 처리 영역에서 Table 1에서 보듯이 특정 작업을 다루기 위해 다양한 오디오 데이터셋들이 개발되었습니다. Qwen-Audio는 광범위한 오디오 데이터셋을 사용하여 공동 훈련을 수행하는 것을 목표로 합니다. 목표는 모든 오디오 작업을 지원할 수 있는 통합된 모델을 훈련하여, 다양한 작업을 처리할 때 번거로운 모델 전환의 필요성을 없애는 것입니다.

더 중요하게는, 공동 훈련 중에 작업들이 서로 도움이 될 수 있습니다: 1) 유사한 작업들은 오디오 신호에 내장된 기본 정보에 대한 공통적인 초점을 공유하므로 지식 공유와 협력 학습으로부터 이익을 얻을 수 있습니다; 2) 낮은 수준의 인식 능력에 의존하는 작업들이 높은 수준의 이해나 추론 능력을 요구하는 작업들을 도울 수 있습니다.

그러나 서로 다른 데이터셋들은 작업 초점, 언어, 주석 세분화 및 텍스트 구조의 차이로 인해 텍스트 레이블에서 상당한 변화를 보입니다. 네트워크를 다양한 작업에 대해 훈련하기 위해 이러한 다양한 데이터셋을 단순히 혼합하는 것은 상호 향상으로 이어질 수 없으며, 대신 간섭을 도입합니다.

기존의 대부분의 multi-task 훈련 접근 방식들은 유사한 작업들을 그룹화하거나(예: 오디오 캡션, 전사) 간섭을 방지하기 위해 각 데이터셋에 dataset ID를 할당했습니다. 이러한 접근 방식들이 일정한 효과를 달성했지만, 여전히 상당한 개선의 여지가 있습니다.

Whisper는 voice activity detection, language identification, sentence-level timestamp 태그와 같은 언어 decoder에 대한 입력 특수 토큰의 시퀀스로 작업과 조건 정보를 지정하여 multitask 훈련 형식을 제안합니다. 그러나 Whisper는 음성 번역과 인식 작업에만 초점을 맞춥니다.

**Multi-task Training Format Framework**: Whisper에서 영감을 받아, 다양한 종류의 오디오를 통합하기 위해 다음과 같은 multitask 훈련 형식 framework를 제안합니다:

• **Transcription Tag**: 예측의 시작은 transcription 태그를 사용하여 표시됩니다. `<|startoftranscripts|>`는 음성 인식 및 음성 번역 작업과 같이 음성 단어를 정확하게 전사하고 음성 녹음의 언어적 내용을 캡처하는 작업을 나타내는 데 사용됩니다. 다른 작업의 경우 `<|startofanalysis|>` 태그가 활용됩니다.

• **Audio Language Tag**: 그런 다음 오디오에서 사용되는 언어를 나타내는 언어 태그를 통합합니다. 이 태그는 총 8개 언어로 구성된 훈련 세트에 있는 각 언어에 할당된 고유 토큰을 사용합니다. 자연음과 음악과 같이 음성이 포함되지 않은 오디오 세그먼트의 경우, 모델은 `<|unknown|>` 토큰을 예측하도록 훈련됩니다.

• **Task Tag**: 후속 토큰들이 작업을 지정합니다. 수집된 오디오 작업을 다섯 가지 범주로 분류합니다: `<|transcribe|>`, `<|translate|>`, `<|caption|>`, `<|analysis|>`, `<|question-answer|>` 작업들. question-answer (QA) 작업의 경우, 태그 후에 해당 질문을 추가합니다.

• **Text Language Tag**: 태그 토큰이 출력 텍스트 시퀀스의 언어를 지정합니다.

• **Timestamps Tag**: `<|timestamps|>` 또는 `<|notimestamps|>` 토큰의 존재는 모델이 타임스탬프를 예측해야 하는지 여부를 결정합니다. Whisper에서 사용되는 문장 수준 타임스탬프와 다르게, `<|timestamps|>` 태그의 포함은 모델이 SRWT(Speech Recognition with Word-level Timestamps)로 축약되는 세밀한 word-level 타임스탬프 예측을 수행하도록 요구합니다. 이러한 타임스탬프의 예측은 전사 단어들과 교차됩니다: 시작 시간 토큰은 각 전사 토큰 전에 예측되고, 종료 시간 토큰은 후에 예측됩니다. 우리의 실험에 따르면, SRWT는 오디오 신호를 타임스탬프와 정렬하는 모델의 능력을 향상시킵니다. 이러한 향상된 정렬은 모델의 음성 신호에 대한 포괄적인 이해에 기여하며, 음성 인식 및 오디오 QA 작업과 같은 많은 작업에서 주목할 만한 발전을 가져옵니다.

• **Output Instruction**: 마지막으로, 다양한 하위 작업에 대한 작업과 원하는 형식을 더 구체적으로 지정하기 위한 출력 지시사항을 제공하고, 그런 다음 텍스트 출력이 시작됩니다.

우리 framework의 지도 원리는 공유 태그를 통해 유사한 작업들 간의 지식 공유를 최대화하여 성능을 향상시키는 것입니다. 동시에, 우리는 서로 다른 작업과 출력 형식이 구별될 수 있도록 하여 모델의 one-to-many 매핑 문제를 방지합니다.

### 3.3 Supervised Fine-tuning

multitask 모델의 광범위한 사전 훈련은 오디오에 대한 광범위한 이해로 모델을 갖추게 했습니다. 이를 기반으로, 우리는 instruction 기반 fine-tuning 기법을 사용하여 인간 의도에 맞춰 모델의 능력을 향상시켜 Qwen-Audio-Chat이라는 대화형 채팅 모델을 만듭니다.

이를 달성하기 위해, 우리는 각 작업에 대한 시연을 수동으로 생성합니다. 이러한 시연은 원시 텍스트 레이블, 질문 및 답변으로 구성됩니다. 그런 다음 제공된 원시 텍스트 레이블을 기반으로 추가 질문과 답변을 생성하기 위해 GPT-3.5를 활용합니다.

또한, 수동 주석, 모델 생성 및 전략 연결을 사용하여 audio-dialogue 데이터의 데이터셋을 생성합니다. 이 데이터셋은 추론, 스토리 생성 및 multi-image comprehension 능력을 모델에 통합하는 데 도움이 됩니다.

multi-audio dialogue와 여러 오디오 입력을 효과적으로 처리하기 위해, "Audio id:"로 다양한 오디오를 라벨링하는 규약을 도입합니다. 여기서 id는 오디오 입력 dialogue의 순서에 해당합니다. dialogue 형식 측면에서, 우리는 ChatML 형식을 사용하여 instruction tuning 데이터셋을 구성합니다. 이 형식에서 각 상호작용의 문장은 dialogue 종료를 촉진하기 위해 두 개의 특수 토큰(`<im_start>`와 `<im_end>`)으로 표시됩니다.

multi-turn dialogue 내에서 오디오와 순수 텍스트 modality 모두로부터 다양한 입력을 촉진하기 위해, 우리는 이 훈련 과정에서 위에서 언급한 audio-centric instruction 데이터와 순수 텍스트 instruction 데이터의 조합을 사용합니다. 이 접근 방식을 통해 모델이 다양한 형태의 입력을 원활하게 처리할 수 있습니다. instruction tuning 데이터의 총량은 20k입니다.

4. Experiments
--------------

### 4.1 Setup

multi-task 사전 훈련의 경우, LLM의 가중치를 고정하고 audio encoder만 최적화합니다. 이 훈련된 모델을 Qwen-Audio라고 합니다. 후속 supervised fine-tuning 단계에서는 audio encoder의 가중치를 고정하고 LLM만 최적화합니다. 결과 모델은 Qwen-Audio-Chat으로 표시됩니다. 두 단계 모두의 자세한 훈련 구성은 Table 6에 나열되어 있습니다.

### 4.2 Evaluation

Qwen-Audio의 범용 이해 능력을 평가하기 위해, Table 2에서 보듯이 Automatic Speech Recognition (ASR), Speech-to-Text Translation (S2TT), Automatic Audio Captioning (AAC), Acoustic Scene Classification (ASC), Speech Emotion Recognition (SER), Audio Question and Answering (AQA), Vocal Sound Classification (VSC), Music Note Analysis (MNA)를 포함한 다양한 작업을 포괄하는 종합적인 평가를 수행합니다.

이 평가는 12개의 데이터셋에 걸쳐 수행됩니다. 평가 데이터셋들은 데이터 누출을 방지하기 위해 훈련 데이터에서 엄격하게 제외됩니다.

### 4.3 Main Results

이 섹션에서는 작업별 fine-tuning 없이 다양한 작업에 걸친 성능을 평가하는 Qwen-Audio 모델의 종합적인 평가를 제시합니다.

Table 3에 묘사된 English Automatic Speech Recognition (ASR) 결과를 먼저 검토하면, Qwen-Audio가 이전 multi-task 학습 모델들과 비교하여 우수한 성능을 보입니다. 구체적으로 librispeech test-clean과 test-other 데이터셋에서 각각 2.0%와 4.2%의 WER를 달성합니다.

마찬가지로, 중국어 만다린 ASR 결과는 이전 접근 방식들과 비교하여 Qwen-Audio의 경쟁력 있는 성능을 보여줍니다. 우리가 아는 한, Qwen-Audio는 Aishell1 dev와 test 셋에서 최첨단 결과를 달성합니다.

또한, CoVoST2 데이터셋에서 Qwen-Audio의 음성 번역 성능을 평가합니다. 결과는 Qwen-Audio가 7개 번역 방향 모두에서 기준선을 상당한 차이로 능가한다는 것을 보여줍니다.

마지막으로, Table 3에 요약된 AAC, SWRT, ASC, SER, AQA, VSC, MNA를 포함한 다양한 오디오 분석 작업에서 Qwen-Audio의 성능을 분석합니다. 이러한 작업들에서 Qwen-Audio는 상당한 차이로 기준선들을 지속적으로 능가합니다. 특히, CochlScene, ClothoAQA, VocalSound에서 최첨단 결과를 달성하여 모델의 강력한 오디오 이해 능력을 보여줍니다.

### 4.4 Results of Interactive Chat

Figure 2에 묘사된 예시 사례를 통해 Qwen-Audio-Chat의 대화 능력을 보여줍니다. 또한, 온라인 채팅 상호작용을 위해 훈련된 모델에 대한 공개 액세스를 제공할 예정입니다.

### 4.5 The Analysis of Word-level Timestamps Prediction

우리는 Qwen-Audio가 음성 전사를 인식할 뿐만 아니라 각 단어의 타임스탬프를 예측하도록 훈련함으로써 word-level 타임스탬프를 사용한 음성 인식(SRWT) 작업을 제안합니다. SRWT의 목적은 두 가지입니다: 첫째, 오디오 신호를 세밀한 타임스탬프와 정렬하는 모델의 능력을 향상시키는 것; 둘째, Qwen-Audio-Chat에서 음성 및 오디오의 grounding과 grounding 기반 QA 작업을 지원하는 것입니다.

이 섹션에서는 다른 작업들은 그대로 유지하면서 multitask pretraining에서 SRWT 작업의 훈련을 제외합니다. 주목할 점은 SRWT 제거가 SRWT 작업이 automatic speech recognition (ASR) 작업과 동일한 오디오 데이터셋을 공유하므로 훈련을 위한 오디오 데이터셋 커버리지에 영향을 주지 않는다는 것입니다.

Table 4와 Table 5에 결과가 나타나 있습니다: SRWT로 훈련된 모델들이 자동 음성 인식과 자연음 QA 및 Music QA를 포함한 오디오 질문 답변 작업에서 우수한 성능을 달성합니다. 이러한 결과는 일반적인 오디오 신호 grounding 능력을 향상시키고 이후 소리와 음악 신호 QA 작업의 성능을 개선하기 위해 세밀한 word-level 타임스탬프를 통합하는 효과를 강조합니다.

5. Conclusion
-------------

본 논문에서는 범용 오디오 이해 능력을 갖춘 대규모 audio-language 모델 세트인 Qwen-Audio 시리즈를 제시합니다. 공동 훈련을 위해 다양한 종류의 오디오를 통합하기 위해, 우리는 유사한 작업들 간의 지식 공유를 촉진하고 서로 다른 텍스트 형식으로 인한 one-to-many 매핑 문제를 방지하는 통합된 multi-task 학습 framework를 제안합니다.

작업별 fine-tuning 없이도, 결과적인 Qwen-Audio 모델들은 다양한 벤치마크에서 이전 연구들을 능가하여 범용 오디오 이해 능력을 보여줍니다. supervised instruction finetuning을 통해, Qwen-Audio-Chat은 인간 의도에 맞춘 강력한 능력을 보여주며, 오디오와 텍스트 입력 모두로부터 다국어 및 multi-turn dialogue를 지원합니다.

6. Acknowledgements
-------------------

Jinze Bai, Shuai Bai, Peng Wang, Sinan Tan, Shijie Wang와의 통찰력 있는 토론에 감사를 표합니다. 이 프로젝트의 지원에 대해 Juan Zhu, Junyang Lin, Siqi Zheng, Jiaming Wang, Zhihao Du에게 감사드립니다.

---

*본 연구는 audio-language 모델링 분야에서 significant한 진전을 나타내며, 특히 multi-task 학습과 word-level timestamp 예측을 통한 범용 오디오 이해 능력의 발전에 기여합니다.*