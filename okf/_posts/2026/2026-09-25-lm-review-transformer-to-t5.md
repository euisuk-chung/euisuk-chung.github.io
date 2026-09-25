---
type: "Concept Note"
title: "[복습] 다시 근본으로, 언어모델을 오랜만에 복습해보자: Transformer to T5"
description: "Transformer, BERT, GPT, BART, T5의 모델 정보·핵심 기여·푸는 문제·학습 방식을 원 논문 그림과 입력/출력 예시, PyTorch·Hugging Face 코드로 정리하고 인코더와 디코더가 학습하고 추론하는 방식의 차이를 비교합니다."
date: "2026-09-25"
tags:
  - "Transformer"
  - "NLP"
  - "딥러닝"
  - "개념정리"
generated:
  by: "process:claude-code"
  at: "2026-09-25T13:10:00+09:00"
sources:
  - id: "arxiv:1706.03762"
    resource: "https://arxiv.org/abs/1706.03762"
    title: "Attention Is All You Need"
  - id: "arxiv:1810.04805"
    resource: "https://arxiv.org/abs/1810.04805"
    title: "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding"
  - id: "openai:gpt-1"
    resource: "https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf"
    title: "Improving Language Understanding by Generative Pre-Training"
  - id: "openai:gpt-2"
    resource: "https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf"
    title: "Language Models are Unsupervised Multitask Learners"
  - id: "arxiv:2005.14165"
    resource: "https://arxiv.org/abs/2005.14165"
    title: "Language Models are Few-Shot Learners"
  - id: "arxiv:2203.02155"
    resource: "https://arxiv.org/abs/2203.02155"
    title: "Training language models to follow instructions with human feedback"
  - id: "arxiv:1910.13461"
    resource: "https://arxiv.org/abs/1910.13461"
    title: "BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension"
  - id: "arxiv:1910.10683"
    resource: "https://arxiv.org/abs/1910.10683"
    title: "Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer"
status: "stable"
year: "2026"
source_type: "paper"
visual_sources:
  - path: "img/reviews/2026/lm-review-transformer-to-t5/transformer-architecture.png"
    kind: "paper-figure"
    source_url: "https://arxiv.org/abs/1706.03762"
    figure: "1"
    caption: "Transformer 전체 구조. arXiv 소스의 원본 그림 파일입니다."
  - path: "img/reviews/2026/lm-review-transformer-to-t5/transformer-scaled-dot-product.png"
    kind: "paper-figure"
    source_url: "https://arxiv.org/abs/1706.03762"
    figure: "2 (left)"
    caption: "Scaled Dot-Product Attention."
  - path: "img/reviews/2026/lm-review-transformer-to-t5/transformer-multi-head.png"
    kind: "paper-figure"
    source_url: "https://arxiv.org/abs/1706.03762"
    figure: "2 (right)"
    caption: "Multi-Head Attention."
  - path: "img/reviews/2026/lm-review-transformer-to-t5/bert-overall.png"
    kind: "paper-figure"
    source_url: "https://arxiv.org/abs/1810.04805"
    figure: "1"
    caption: "BERT 사전학습과 파인튜닝 절차."
  - path: "img/reviews/2026/lm-review-transformer-to-t5/bert-input-embeddings.png"
    kind: "paper-figure"
    source_url: "https://arxiv.org/abs/1810.04805"
    figure: "2"
    caption: "BERT 입력 표현(Token·Segment·Position 임베딩의 합)."
  - path: "img/reviews/2026/lm-review-transformer-to-t5/bert-gpt-elmo-comparison.png"
    kind: "paper-figure"
    source_url: "https://arxiv.org/abs/1810.04805"
    figure: "3"
    caption: "BERT, OpenAI GPT, ELMo 사전학습 구조 비교."
  - path: "img/reviews/2026/lm-review-transformer-to-t5/bert-finetune.png"
    kind: "paper-figure"
    source_url: "https://arxiv.org/abs/1810.04805"
    figure: "4"
    caption: "태스크별 BERT 파인튜닝 방식."
  - path: "img/reviews/2026/lm-review-transformer-to-t5/gpt1-architecture.png"
    kind: "paper-figure"
    source_url: "https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf#page=4"
    page: 4
    figure: "1"
    caption: "GPT-1 구조와 태스크별 입력 변환. PDF 4쪽 그림 영역을 크롭했습니다."
  - path: "img/reviews/2026/lm-review-transformer-to-t5/gpt3-in-context-learning.png"
    kind: "paper-figure"
    source_url: "https://arxiv.org/abs/2005.14165"
    figure: "1.1"
    caption: "사전학습 중의 outer loop와 in-context learning inner loop."
  - path: "img/reviews/2026/lm-review-transformer-to-t5/gpt3-eval-strategies.png"
    kind: "paper-figure"
    source_url: "https://arxiv.org/abs/2005.14165"
    figure: "2.1"
    caption: "Zero-shot, One-shot, Few-shot과 전통적 파인튜닝 비교."
  - path: "img/reviews/2026/lm-review-transformer-to-t5/bart-bert.png"
    kind: "paper-figure"
    source_url: "https://arxiv.org/abs/1910.13461"
    figure: "1a"
    caption: "BERT 방식: 양방향 인코더."
  - path: "img/reviews/2026/lm-review-transformer-to-t5/bart-gpt.png"
    kind: "paper-figure"
    source_url: "https://arxiv.org/abs/1910.13461"
    figure: "1b"
    caption: "GPT 방식: 자기회귀 디코더."
  - path: "img/reviews/2026/lm-review-transformer-to-t5/bart-overview.png"
    kind: "paper-figure"
    source_url: "https://arxiv.org/abs/1910.13461"
    figure: "1c"
    caption: "BART: 양방향 인코더 + 자기회귀 디코더."
  - path: "img/reviews/2026/lm-review-transformer-to-t5/bart-noise.png"
    kind: "paper-figure"
    source_url: "https://arxiv.org/abs/1910.13461"
    figure: "2"
    caption: "BART에서 실험한 입력 노이즈 변환."
  - path: "img/reviews/2026/lm-review-transformer-to-t5/bart-classifier.png"
    kind: "paper-figure"
    source_url: "https://arxiv.org/abs/1910.13461"
    figure: "3a"
    caption: "BART로 분류 문제를 푸는 방식."
  - path: "img/reviews/2026/lm-review-transformer-to-t5/t5-text-to-text.png"
    kind: "paper-figure"
    source_url: "https://arxiv.org/abs/1910.10683"
    figure: "1"
    caption: "T5의 text-to-text 프레임워크."
  - path: "img/reviews/2026/lm-review-transformer-to-t5/t5-span-corruption.png"
    kind: "paper-figure"
    source_url: "https://arxiv.org/abs/1910.10683"
    figure: "2"
    caption: "T5 span corruption 목표 함수 예시."
  - path: "img/reviews/2026/lm-review-transformer-to-t5/t5-attention-masks.png"
    kind: "paper-figure"
    source_url: "https://arxiv.org/abs/1910.10683"
    figure: "3"
    caption: "Fully-visible, Causal, Causal with prefix 어텐션 마스크."
  - path: "img/reviews/2026/lm-review-transformer-to-t5/t5-architectures.png"
    kind: "paper-figure"
    source_url: "https://arxiv.org/abs/1910.10683"
    figure: "4"
    caption: "Encoder-Decoder, Language model, Prefix LM 구조 비교."
---

최근 JEV라는 모델이 공개되면서 BERT 계열 인코더와의 비교가 다시 활발해졌고, 덕분에 BERT에 대한 관심도 한 번 더 올라갔습니다. 생성형 LLM이 대세가 된 지금도 분류·검색·라우팅처럼 "빠르고 정확하게 이해하는" 문제에서는 인코더 모델이 여전히 자주 언급됩니다. 그런데 막상 "BERT는 GPT와 학습 방식이 정확히 어떻게 다르지? 입력과 출력은 뭐고 loss는 어디에 걸리지?"라는 질문을 받으면 바로 답하기가 쉽지 않았습니다.

그래서 이번 기회에 BERT를 중심으로, 그 뿌리인 2017년의 Transformer와 같은 시기에 나온 GPT, BART, T5까지 근본 모델들을 처음부터 다시 정리해 보았습니다.

각 모델은 아래 다섯 가지 관점으로 정리합니다.

1. **모델 정보**: 발표 시점, 저자·기관, 크기, 학습 데이터
2. **핵심 특징과 Contribution**: 이전 연구와 비교해 무엇을 바꿨는가
3. **푸는 문제**: 어떤 태스크를 어떤 형태로 푸는가
4. **학습 방식**: 입력(IN)과 출력(OUT), 정답(label), loss가 걸리는 위치
5. **샘플과 코드**: 실제 입출력 예시와 PyTorch·Hugging Face 스니펫

그림은 모두 **원 논문의 그림**입니다. arXiv 소스에 포함된 원본 그림 파일을 쓰거나 PDF에서 그림 영역만 잘라 왔고, 그림 안의 글자는 번역하지 않았습니다.

## 전체 지도 먼저 보기

| 모델 | 연도·기관 | 구조 | 사전학습 목표 | 대표 용도 |
|---|---|---|---|---|
| Transformer | 2017, Google | Encoder–Decoder | (사전학습 없음) 번역 데이터로 바로 학습 | 기계번역 |
| BERT | 2018, Google | Encoder only | Masked LM + Next Sentence Prediction | 분류, 추출형 QA, NER, 임베딩 |
| GPT (1/2/3) | 2018~2020, OpenAI | Decoder only | 다음 토큰 예측 (Causal LM) | 생성, few-shot, 범용 LLM |
| BART | 2019, Facebook AI | Encoder–Decoder | 노이즈가 섞인 문서 → 원문 복원 | 요약, 생성, 분류 |
| T5 | 2019, Google | Encoder–Decoder | Span corruption (가린 span만 생성) | 모든 태스크를 text-to-text로 |

![Transformer 기반 사전학습 구조 비교: Encoder-Decoder, Language model, Prefix LM]({{ '/img/reviews/2026/lm-review-transformer-to-t5/t5-architectures.png' | relative_url }})

*T5 논문 Figure 4. 왼쪽부터 Encoder–Decoder(Transformer, BART, T5), Language model(GPT), Prefix LM입니다. 선의 연결이 곧 어텐션 마스크입니다. [원문](https://arxiv.org/abs/1910.10683)*

이 그림 한 장이 글 전체의 요약입니다. 이후의 모든 차이는 결국 **"각 위치의 토큰이 어느 토큰을 볼 수 있는가(어텐션 마스크)"**와 **"loss를 어느 위치에 거는가"** 두 가지로 설명됩니다.

## 1. 트랜스포머 (Transformer)

### 1.1 모델 정보

| 항목 | 내용 |
|---|---|
| 논문 | Attention Is All You Need (Vaswani et al., NeurIPS 2017) |
| 기관 | Google Brain, Google Research |
| 구조 | Encoder 6층 + Decoder 6층 |
| 크기 | Base: $`d_{model}=512`$, 8 heads, FFN 2048, 약 65M / Big: $`d_{model}=1024`$, 16 heads, FFN 4096, 약 213M |
| 데이터 | WMT 2014 영어–독일어(약 450만 문장 쌍), 영어–프랑스어(약 3,600만 문장 쌍) |
| 학습 | P100 GPU 8장. Base 10만 step 약 12시간, Big 30만 step 약 3.5일 |

### 1.2 핵심 특징과 Contribution

![Transformer 전체 구조: 왼쪽 Encoder, 오른쪽 Decoder]({{ '/img/reviews/2026/lm-review-transformer-to-t5/transformer-architecture.png' | relative_url }})

*Transformer 논문 Figure 1. 왼쪽 N× 블록이 Encoder, 오른쪽 N× 블록이 Decoder입니다. [원문](https://arxiv.org/abs/1706.03762)*

**1) RNN과 CNN 없이 어텐션만으로 seq2seq를 구성했습니다.** 이전 번역 모델(RNN seq2seq + attention)은 토큰을 순서대로 하나씩 처리해야 해서 학습 병렬화가 어려웠습니다. Transformer는 self-attention으로 모든 토큰 쌍의 관계를 **한 번의 행렬 연산으로** 계산합니다. 그래서 학습 시간이 크게 줄었고, 멀리 떨어진 토큰 사이 경로 길이도 $`O(1)`$이 되었습니다.

**2) Scaled Dot-Product Attention과 Multi-Head Attention**

```math
\mathrm{Attention}(Q, K, V) = \mathrm{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}\right)V
```

$`\sqrt{d_k}`$로 나누는 이유는 차원이 커질수록 내적 값의 분산이 커져서 softmax가 한쪽으로 쏠리고 gradient가 작아지기 때문입니다. Multi-head는 서로 다른 projection으로 어텐션을 여러 번 나누어 계산한 뒤 이어 붙여서, 여러 종류의 관계(문법, 지시어, 의미 등)를 동시에 볼 수 있게 합니다.

```math
\mathrm{MultiHead}(Q,K,V) = \mathrm{Concat}(\mathrm{head}_1, \dots, \mathrm{head}_h)W^O,\quad \mathrm{head}_i = \mathrm{Attention}(QW_i^Q, KW_i^K, VW_i^V)
```

![Scaled Dot-Product Attention 구조]({{ '/img/reviews/2026/lm-review-transformer-to-t5/transformer-scaled-dot-product.png' | relative_url }})
![Multi-Head Attention 구조]({{ '/img/reviews/2026/lm-review-transformer-to-t5/transformer-multi-head.png' | relative_url }})

*Transformer 논문 Figure 2. 왼쪽은 Scaled Dot-Product Attention, 오른쪽은 이를 h개 병렬로 수행하는 Multi-Head Attention입니다. [원문](https://arxiv.org/abs/1706.03762)*

**3) 세 종류의 어텐션**을 씁니다.

| 위치 | Query | Key/Value | 마스크 |
|---|---|---|---|
| Encoder self-attention | 원문 | 원문 | 없음 (양방향) |
| Decoder masked self-attention | 번역문 | 번역문 | Causal (자기 왼쪽만) |
| Decoder cross-attention | 번역문 | **Encoder 출력** | 없음 |

**4) Positional Encoding.** 어텐션 자체에는 순서 개념이 없으므로 sin/cos 함수로 위치 정보를 더해 줍니다.

```math
PE_{(pos, 2i)} = \sin\left(pos / 10000^{2i/d_{model}}\right),\quad PE_{(pos, 2i+1)} = \cos\left(pos / 10000^{2i/d_{model}}\right)
```

**5) 결과.** WMT14 영어→독일어에서 BLEU 28.4를 기록해 앙상블을 포함한 기존 최고 결과보다 2 BLEU 이상 높았고, 영어→프랑스어에서는 단일 모델로 41.8을 기록했습니다. 학습 비용은 기존 모델들보다 훨씬 적었습니다.

### 1.3 푸는 문제

원 논문의 주된 문제는 **기계번역**이었습니다. 추가로 영어 구문 분석(constituency parsing)에도 적용해서 번역 외 태스크로 일반화된다는 것을 보였습니다. 이 논문에는 "대규모 사전학습 후 파인튜닝"이라는 개념이 없습니다. 태스크 데이터로 **처음부터 끝까지(E2E) 한 번에 학습**합니다.

### 1.4 학습 방식: Teacher Forcing으로 E2E 학습

```
원문 (Encoder 입력)  : 나는 사과를 먹었다
Decoder 입력         : <s>  I    ate   an    apple          ← 정답을 오른쪽으로 한 칸 민 것
Decoder 정답 (label) : I    ate  an    apple </s>           ← 각 위치의 "다음 토큰"
```

- **IN**: 원문 토큰 → Encoder, 정답 번역문을 한 칸 민 것 → Decoder
- **OUT**: Decoder 각 위치마다 vocab 전체에 대한 다음 토큰 확률분포
- **Loss**: Decoder의 모든 위치에서 계산한 cross-entropy 합. 논문에서는 label smoothing $`\epsilon_{ls}=0.1`$을 적용했습니다.

```math
\mathcal{L} = -\sum_{t=1}^{T} \log p_\theta(y_t \mid y_{<t}, x)
```

loss는 Decoder 끝에만 있습니다. 하지만 gradient가 **cross-attention을 통해 Encoder까지 흘러가므로** Encoder와 Decoder가 함께 학습됩니다. 또 Decoder에 모델 자신의 예측 대신 **정답 토큰을 넣는 teacher forcing**과 causal mask 덕분에, 번역문의 모든 위치를 **한 번의 forward pass로 병렬 학습**할 수 있습니다.

학습률은 warmup 후에 감소하는 스케줄을 썼습니다(warmup 4,000 step, Adam $`\beta_2=0.98`$).

```math
lr = d_{model}^{-0.5} \cdot \min\left(step^{-0.5},\ step \cdot warmup^{-1.5}\right)
```

### 1.5 코드로 보기

**Scaled dot-product attention과 causal mask**

```python
import math
import torch
import torch.nn.functional as F

def scaled_dot_product_attention(q, k, v, mask=None):
    # q, k, v: (batch, heads, seq_len, d_k)
    scores = q @ k.transpose(-2, -1) / math.sqrt(q.size(-1))   # (B, H, T_q, T_k)
    if mask is not None:
        scores = scores.masked_fill(mask == 0, float("-inf"))  # 볼 수 없는 위치는 -inf
    attn = F.softmax(scores, dim=-1)
    return attn @ v, attn

T = 4
causal_mask = torch.tril(torch.ones(T, T))   # 아래 삼각형만 1 → 자기 자신과 왼쪽만 볼 수 있음
print(causal_mask)
# tensor([[1., 0., 0., 0.],
#         [1., 1., 0., 0.],
#         [1., 1., 1., 0.],
#         [1., 1., 1., 1.]])
```

**`nn.Transformer`로 teacher forcing 학습 한 step**

```python
import torch
import torch.nn as nn

VOCAB, D_MODEL, PAD, BOS = 8000, 512, 0, 1

class Seq2SeqTransformer(nn.Module):
    def __init__(self):
        super().__init__()
        self.src_emb = nn.Embedding(VOCAB, D_MODEL)
        self.tgt_emb = nn.Embedding(VOCAB, D_MODEL)
        self.pos = nn.Embedding(512, D_MODEL)   # 간단히 learned position 사용
        self.transformer = nn.Transformer(d_model=D_MODEL, nhead=8,
                                          num_encoder_layers=6, num_decoder_layers=6,
                                          dim_feedforward=2048, batch_first=True)
        self.lm_head = nn.Linear(D_MODEL, VOCAB)

    def embed(self, emb, ids):
        pos = torch.arange(ids.size(1), device=ids.device)
        return emb(ids) + self.pos(pos)

    def forward(self, src, tgt_in):
        tgt_mask = self.transformer.generate_square_subsequent_mask(tgt_in.size(1))
        h = self.transformer(self.embed(self.src_emb, src), self.embed(self.tgt_emb, tgt_in),
                             tgt_mask=tgt_mask,                       # Decoder causal mask
                             src_key_padding_mask=(src == PAD),
                             tgt_key_padding_mask=(tgt_in == PAD))
        return self.lm_head(h)                                        # (B, T_tgt, VOCAB)

model = Seq2SeqTransformer()
criterion = nn.CrossEntropyLoss(ignore_index=PAD, label_smoothing=0.1)

src = torch.randint(2, VOCAB, (2, 10))           # 원문
tgt = torch.randint(2, VOCAB, (2, 8))            # 정답 번역문 (끝에 </s> 포함이라고 가정)
tgt_in = torch.cat([torch.full((2, 1), BOS), tgt[:, :-1]], dim=1)   # 오른쪽으로 한 칸 shift

logits = model(src, tgt_in)
loss = criterion(logits.reshape(-1, VOCAB), tgt.reshape(-1))        # 모든 target 위치에서 CE
loss.backward()                                                     # Encoder까지 gradient 전달
```

## 2. 구글의 BERT

### 2.1 모델 정보

| 항목 | 내용 |
|---|---|
| 논문 | BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding (Devlin et al., NAACL 2019, arXiv 2018.10) |
| 기관 | Google AI Language |
| 구조 | Transformer **Encoder only** |
| 크기 | Base: 12층, hidden 768, 12 heads, 110M / Large: 24층, hidden 1024, 16 heads, 340M |
| 데이터 | BooksCorpus (8억 단어) + 영어 Wikipedia (25억 단어) |
| 토크나이저 | WordPiece, vocab 30,000 |
| 학습 | batch 256 시퀀스 × 512 토큰, 100만 step (약 33억 단어 코퍼스 기준 40 epoch) |

### 2.2 핵심 특징과 Contribution

![BERT, OpenAI GPT, ELMo의 사전학습 구조 비교]({{ '/img/reviews/2026/lm-review-transformer-to-t5/bert-gpt-elmo-comparison.png' | relative_url }})

*BERT 논문 Figure 3. BERT는 모든 층에서 양방향, GPT는 왼쪽→오른쪽 단방향, ELMo는 독립적으로 학습한 두 방향 LSTM의 출력을 이어 붙입니다. [원문](https://arxiv.org/abs/1810.04805)*

**1) 깊은 양방향(Deep Bidirectional) 표현.** GPT-1은 왼쪽 문맥만 보고, ELMo는 왼쪽→오른쪽 LM과 오른쪽→왼쪽 LM을 **따로** 학습한 뒤 이어 붙이는(shallow) 방식이었습니다. BERT는 **모든 층에서 양쪽 문맥을 동시에** 봅니다. 그런데 그냥 양방향 LM을 학습하면 정답 단어를 스스로 보게 되는 정보 누설이 생깁니다. 이를 막기 위해 제안한 것이 **Masked LM**입니다.

**2) 사전학습 → 파인튜닝 패러다임의 정착.** 태스크마다 복잡한 아키텍처를 새로 설계하지 않고, 사전학습된 BERT 위에 **출력층 하나만 추가**해서 전체를 파인튜닝합니다.

**3) 결과.** 11개 NLP 태스크에서 SOTA를 달성했습니다. GLUE 80.5(+7.7%p), MultiNLI 86.7%, SQuAD v1.1 F1 93.2, SQuAD v2.0 F1 83.1입니다.

### 2.3 학습 방식: MLM과 NSP

![BERT의 사전학습과 파인튜닝 절차]({{ '/img/reviews/2026/lm-review-transformer-to-t5/bert-overall.png' | relative_url }})

*BERT 논문 Figure 1. 왼쪽은 NSP와 Mask LM으로 하는 사전학습, 오른쪽은 같은 가중치에서 시작해 태스크별로 하는 파인튜닝입니다. [원문](https://arxiv.org/abs/1810.04805)*

**입력(IN)**: 두 문장(segment)을 `[CLS] A [SEP] B [SEP]` 형태로 이어 붙이고, 세 임베딩을 더해서 넣습니다.

![BERT 입력 표현: Token, Segment, Position 임베딩의 합]({{ '/img/reviews/2026/lm-review-transformer-to-t5/bert-input-embeddings.png' | relative_url }})

*BERT 논문 Figure 2. 입력 임베딩 = Token + Segment + Position 임베딩입니다. [원문](https://arxiv.org/abs/1810.04805)*

**출력(OUT)**: 토큰마다 하나씩 나오는 문맥 벡터(hidden state) $`T_i \in \mathbb{R}^{H}`$입니다. BERT 자체에는 "생성" 단계가 없습니다. 이 벡터 위에 작은 head를 붙여서 loss를 계산합니다.

**(1) Masked Language Model (MLM)**

- 입력 토큰의 **15%**를 예측 대상으로 고릅니다.
- 고른 토큰 중 **80%**는 `[MASK]`, **10%**는 랜덤 토큰, **10%**는 원래 토큰 그대로 둡니다. 파인튜닝 때는 `[MASK]`가 나오지 않으므로, 사전학습과 파인튜닝 입력 분포의 차이를 줄이려는 장치입니다.
- 선택된 위치의 출력 벡터를 vocab 크기의 분류기에 넣어 **원래 토큰을 맞힙니다**. loss는 **선택된 15% 위치에서만** 계산합니다.

```
원문     : my dog is hairy
입력     : [CLS] my dog is [MASK] [SEP]      (80%)
           [CLS] my dog is apple  [SEP]      (10%, 랜덤 토큰)
           [CLS] my dog is hairy  [SEP]      (10%, 그대로)
정답     : 4번째 위치 → "hairy"                (나머지 위치는 loss 없음)
```

**(2) Next Sentence Prediction (NSP)**

- 50%는 실제로 이어지는 문장 B(`IsNext`), 50%는 코퍼스에서 뽑은 랜덤 문장(`NotNext`)을 넣습니다.
- `[CLS]` 위치의 출력 $`C`$로 이진 분류를 합니다. QA나 NLI처럼 두 문장 관계가 중요한 태스크를 위해 넣은 목표입니다.
- 이후 RoBERTa(2019)가 NSP를 빼도 성능이 떨어지지 않거나 오히려 좋아진다고 보고해서, 이후 모델들은 대부분 NSP를 쓰지 않습니다.

```math
\mathcal{L}_{\text{BERT}} = \mathcal{L}_{\text{MLM}} + \mathcal{L}_{\text{NSP}},\quad \mathcal{L}_{\text{MLM}} = -\sum_{i \in \mathcal{M}} \log p_\theta(x_i \mid \tilde{x})
```

여기서 $`\mathcal{M}`$은 마스킹 대상으로 고른 위치 집합이고, $`\tilde{x}`$는 손상된 입력입니다. 라벨이 원문에서 자동으로 만들어지므로 사람이 라벨을 달 필요가 없는 **self-supervised** 학습입니다.

### 2.4 코드로 보기

**80/10/10 마스킹 직접 구현**

```python
import torch

def mask_tokens(input_ids, tokenizer, mlm_prob=0.15):
    labels = input_ids.clone()
    prob = torch.full(labels.shape, mlm_prob)
    special = torch.tensor(tokenizer.get_special_tokens_mask(labels.tolist(), already_has_special_tokens=True),
                           dtype=torch.bool)
    prob.masked_fill_(special, 0.0)                       # [CLS], [SEP]는 마스킹 제외
    masked = torch.bernoulli(prob).bool()
    labels[~masked] = -100                                # 선택되지 않은 위치는 loss 제외

    replace = torch.bernoulli(torch.full(labels.shape, 0.8)).bool() & masked
    input_ids[replace] = tokenizer.mask_token_id          # 80% → [MASK]

    rand = torch.bernoulli(torch.full(labels.shape, 0.5)).bool() & masked & ~replace
    input_ids[rand] = torch.randint(len(tokenizer), labels.shape)[rand]   # 10% → 랜덤 토큰
    return input_ids, labels                              # 나머지 10%는 원래 토큰 그대로
```

실무에서는 `transformers.DataCollatorForLanguageModeling(tokenizer, mlm_probability=0.15)`가 같은 일을 해 줍니다.

**MLM 헤드로 빈칸 채우기**

```python
from transformers import pipeline

fill = pipeline("fill-mask", model="google-bert/bert-base-uncased")
for r in fill("The capital of France is [MASK].")[:3]:
    print(f"{r['token_str']:>10s}  {r['score']:.3f}")
#      paris  0.417
#      lille  0.071
#       lyon  0.063
```

**MLM loss 계산**

```python
from transformers import AutoTokenizer, BertForMaskedLM

tok = AutoTokenizer.from_pretrained("google-bert/bert-base-uncased")
model = BertForMaskedLM.from_pretrained("google-bert/bert-base-uncased")

torch.manual_seed(0)
enc = tok("my dog is hairy and he likes to play fetch in the park every morning", return_tensors="pt")
input_ids, labels = mask_tokens(enc.input_ids[0].clone(), tok)
print(tok.decode(input_ids))
# [CLS] my [MASK] [MASK] hairy and he likes to play fetch in [MASK] park every morning [SEP]
out = model(input_ids=input_ids[None], attention_mask=enc.attention_mask, labels=labels[None])
print(out.logits.shape)   # torch.Size([1, 17, 30522]): 모든 위치에서 vocab 분포가 나오지만
print(out.loss)           # loss는 labels != -100 인 위치(마스킹된 3개 위치)에서만 계산 → 약 1.40
# 주의: 문장이 너무 짧으면 한 토큰도 선택되지 않아 loss가 nan이 될 수 있습니다.
```

## 3. BERT로 풀 수 있는 다양한 문제들

BERT는 출력층만 바꿔서 거의 모든 **이해(NLU)** 태스크를 풉니다. 논문 Figure 4에 네 가지 유형이 정리되어 있습니다.

![BERT의 네 가지 파인튜닝 방식: 문장쌍 분류, 단일 문장 분류, 질의응답, 토큰 태깅]({{ '/img/reviews/2026/lm-review-transformer-to-t5/bert-finetune.png' | relative_url }})

*BERT 논문 Figure 4. (a) 문장쌍 분류, (b) 단일 문장 분류, (c) 질의응답, (d) 단일 문장 태깅입니다. [원문](https://arxiv.org/abs/1810.04805)*

| 유형 | 예시 데이터셋 | 입력 | 사용하는 출력 | 추가하는 head |
|---|---|---|---|---|
| (a) 문장쌍 분류 | MNLI, QQP, QNLI, STS-B, MRPC, RTE, SWAG | `[CLS] 문장1 [SEP] 문장2 [SEP]` | `[CLS]` 벡터 $`C`$ | Linear → 클래스 수 (STS-B는 회귀 1개) |
| (b) 단일 문장 분류 | SST-2, CoLA | `[CLS] 문장 [SEP]` | `[CLS]` 벡터 $`C`$ | Linear → 클래스 수 |
| (c) 추출형 QA | SQuAD v1.1/v2.0 | `[CLS] 질문 [SEP] 문단 [SEP]` | 문단 토큰 벡터 $`T_i`$ | 시작 벡터 $`S`$, 끝 벡터 $`E`$ |
| (d) 토큰 태깅 | CoNLL-2003 NER | `[CLS] 문장 [SEP]` | 각 토큰 벡터 $`T_i`$ | Linear → 태그 수 (B-PER, O 등) |

추출형 QA에서는 토큰 $`i`$가 정답의 시작일 확률을 $`P_i = \mathrm{softmax}_i(S \cdot T_i)`$로 계산하고, 끝 위치도 같은 방식으로 구합니다. 정답은 $`S \cdot T_i + E \cdot T_j`$가 최대인 $`(i, j),\ j \ge i`$ 구간입니다. **답을 생성하지 않고 문단에서 구간을 찾아 뽑는다**는 점이 핵심입니다.

**예시**

| 태스크 | 입력 | 출력 |
|---|---|---|
| 감성 분류 (SST-2) | `[CLS] this movie was surprisingly good [SEP]` | `positive` |
| 자연어 추론 (MNLI) | `[CLS] A man is playing guitar. [SEP] A person plays music. [SEP]` | `entailment` |
| 추출형 QA (SQuAD) | `[CLS] Where is the Eiffel Tower? [SEP] The Eiffel Tower is in Paris ... [SEP]` | start=`Paris`, end=`Paris` |
| NER | `[CLS] Steve Jobs founded Apple [SEP]` | `B-PER I-PER O B-ORG` |

**코드로 보기**

```python
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# (a)/(b) 문장 분류: [CLS] 위에 Linear head. labels를 넣으면 CE loss가 계산됨
tok = AutoTokenizer.from_pretrained("google-bert/bert-base-uncased")
clf = AutoModelForSequenceClassification.from_pretrained("google-bert/bert-base-uncased", num_labels=3)
enc = tok("A man is playing guitar.", "A person plays music.", return_tensors="pt")  # 문장쌍 → token_type_ids 자동 생성
out = clf(**enc, labels=torch.tensor([0]))
print(out.logits.shape, out.loss)        # (1, 3) — 새로 붙인 head라 파인튜닝 전에는 무작위 예측

# (c) 추출형 QA: 문단 토큰마다 start/end logit → 점수가 가장 높은 구간을 뽑음
from transformers import AutoModelForQuestionAnswering
name = "distilbert/distilbert-base-cased-distilled-squad"
qa_tok = AutoTokenizer.from_pretrained(name)
qa = AutoModelForQuestionAnswering.from_pretrained(name)
enc = qa_tok("Where is the Eiffel Tower?",
             "The Eiffel Tower is a wrought-iron lattice tower in Paris, France.", return_tensors="pt")
with torch.no_grad():
    out = qa(**enc)                                   # start_logits, end_logits: (1, seq_len)
start, end = out.start_logits.argmax(-1).item(), out.end_logits.argmax(-1).item()
print(qa_tok.decode(enc.input_ids[0, start:end + 1]))  # Paris, France

# (d) 토큰 태깅: 토큰마다 Linear head
ner = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")
print(ner("Steve Jobs founded Apple in California."))
# PER: Steve Jobs / ORG: Apple / LOC: California
```

**BERT가 잘 못하는 것**: 자유로운 텍스트 **생성**입니다. 학습할 때 항상 오른쪽 문맥까지 보고 예측했기 때문에, 오른쪽이 비어 있는 상태에서 왼쪽부터 한 토큰씩 이어 쓰는 상황은 학습 분포와 다릅니다. 그래서 요약·번역·대화에는 GPT나 BART, T5 계열을 씁니다. 반대로 문장 임베딩과 검색(Sentence-BERT, 각종 retriever 인코더), 분류, 추출 문제에서는 지금도 인코더 계열이 효율적입니다.

## 4. OpenAI의 GPT

### 4.1 모델 정보

| 항목 | GPT-1 (2018.06) | GPT-2 (2019.02) | GPT-3 (2020.05) |
|---|---|---|---|
| 논문 | Improving Language Understanding by Generative Pre-Training | Language Models are Unsupervised Multitask Learners | Language Models are Few-Shot Learners |
| 구조 | Decoder only, 12층, 768, 12 heads | 최대 48층, 1600 | 96층, 12288, 96 heads |
| 크기 | 117M | 최대 1.5B | 최대 175B |
| 문맥 길이 | 512 | 1024 | 2048 |
| 데이터 | BooksCorpus (미출판 도서 7,000여 권) | WebText (약 800만 문서, 40GB) | Common Crawl(필터링) 등 약 3,000억 토큰 학습 |
| 사용 방식 | 사전학습 → **파인튜닝** | **Zero-shot** | **In-context (few-shot)** |

### 4.2 핵심 특징과 Contribution

![GPT-1의 구조와 태스크별 입력 변환]({{ '/img/reviews/2026/lm-review-transformer-to-t5/gpt1-architecture.png' | relative_url }})

*GPT-1 논문 Figure 1. 왼쪽은 12층 Transformer Decoder(cross-attention 없음, Masked Multi Self Attention만 있음), 오른쪽은 태스크별 입력을 하나의 토큰 시퀀스로 바꾸는 방법입니다. [원문 PDF 4쪽](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf#page=4)*

**GPT-1: 생성형 사전학습 + 판별형 파인튜닝.** 라벨 없는 텍스트로 LM을 사전학습하고 태스크별로 파인튜닝하는 방식을 Transformer에서 처음으로 보였습니다(BERT보다 4개월 먼저 나왔습니다). 구조를 태스크마다 바꾸지 않고, 위 그림처럼 **입력을 `Start … Delim … Extract` 형태의 한 시퀀스로 변환**하는 방식으로 여러 태스크를 풀었습니다. 파인튜닝할 때는 LM loss를 보조 loss로 함께 사용했습니다.

```math
\mathcal{L}_3(\mathcal{C}) = \mathcal{L}_2(\mathcal{C}) + \lambda \cdot \mathcal{L}_1(\mathcal{C}),\quad \lambda = 0.5
```

($`\mathcal{L}_1`$: LM loss, $`\mathcal{L}_2`$: 태스크 분류 loss)

**GPT-2: 파인튜닝 없이 zero-shot.** 모델과 데이터를 키우면 LM이 번역·요약·QA 같은 태스크를 **별도 학습 없이** 어느 정도 수행한다는 것을 보였습니다. 예를 들어 요약은 문서 뒤에 `TL;DR:`을 붙이는 방식입니다. 구조적으로는 LayerNorm을 각 sub-block의 입력 쪽으로 옮긴 **Pre-LN**을 썼고, byte-level BPE(vocab 50,257)를 도입했습니다.

**GPT-3: In-context learning과 스케일링.** 175B까지 키우자 **프롬프트 안에 예시 몇 개만 넣어도**(gradient 업데이트 없이) 새 태스크를 수행하는 능력이 뚜렷해졌습니다.

![사전학습 중의 outer loop와 in-context learning inner loop]({{ '/img/reviews/2026/lm-review-transformer-to-t5/gpt3-in-context-learning.png' | relative_url }})

*GPT-3 논문 Figure 1.1. 사전학습(outer loop) 동안 하나의 시퀀스 안에 반복되는 패턴을 학습하면서, 추론 시 문맥 안에서 태스크를 파악하는 능력(inner loop)이 생긴다는 해석입니다. [원문](https://arxiv.org/abs/2005.14165)*

![Zero-shot, One-shot, Few-shot과 파인튜닝 비교]({{ '/img/reviews/2026/lm-review-transformer-to-t5/gpt3-eval-strategies.png' | relative_url }})

*GPT-3 논문 Figure 2.1. 왼쪽 세 가지(zero/one/few-shot)는 가중치를 업데이트하지 않고 프롬프트만 바꿉니다. 오른쪽 전통적 파인튜닝은 GPT-3에서 사용하지 않았습니다. [원문](https://arxiv.org/abs/2005.14165)*

**그 이후: InstructGPT (2022).** 사전학습만 한 LM은 "다음 토큰 이어쓰기"에 최적화되어 있어서 지시를 잘 따르지 않습니다. InstructGPT는 **SFT(지시–응답 쌍으로 지도학습) → Reward Model 학습 → PPO 강화학습(RLHF)**의 3단계로 이를 정렬했습니다. 사람 평가에서 1.3B InstructGPT의 응답이 175B GPT-3보다 더 선호되었고, 이 방식이 ChatGPT의 기반이 되었습니다.

### 4.3 푸는 문제

- GPT-1: 파인튜닝으로 NLI, QA/상식추론(RACE, Story Cloze), 문장 유사도, 분류. 12개 중 9개 태스크에서 SOTA를 달성했습니다.
- GPT-2/3: **모든 문제를 "텍스트 이어쓰기"로** 풉니다. 번역, 요약, QA, 산술, 코드 등 프롬프트로 표현할 수 있는 모든 태스크가 대상입니다.

### 4.4 학습 방식: 다음 토큰 예측 (Causal LM)

```
입력 (IN)     :  나는    사과를   먹었다    .
정답 (label)  :  사과를  먹었다   .        <eos>        ← 입력을 왼쪽으로 한 칸 민 것
```

- **IN**: 토큰 시퀀스 하나. Token embedding + Position embedding입니다. Segment embedding과 Encoder는 없습니다.
- **OUT**: **모든 위치**에서 다음 토큰의 vocab 분포
- **정답**: 별도로 만들 필요가 없습니다. **입력 자체를 한 칸 민 것이 라벨**입니다.
- **Causal mask**: 각 위치는 자기 자신과 왼쪽만 볼 수 있습니다. 그래서 정답(오른쪽 토큰)을 미리 볼 수 없고, 동시에 모든 위치를 한 번에 병렬로 학습할 수 있습니다.

```math
\mathcal{L}_{\text{CLM}} = -\sum_{t=1}^{T} \log p_\theta(x_t \mid x_{<t})
```

BERT는 전체 토큰의 15% 위치에서만 loss를 얻지만, GPT는 **100% 위치에서 loss를 얻습니다**. 같은 데이터에서 학습 신호를 더 많이 뽑아낼 수 있다는 뜻입니다.

| 단계 | 데이터 | loss 위치 |
|---|---|---|
| Pretraining | 대규모 웹 텍스트 (라벨 없음) | 모든 토큰 |
| SFT (instruction tuning) | (프롬프트, 응답) 쌍을 한 시퀀스로 이어 붙임 | 보통 **응답 토큰만** (프롬프트 부분은 -100으로 제외) |
| RLHF / DPO | 사람 선호 데이터 | 보상 모델 점수 또는 선호 쌍 기반 목표 |

### 4.5 코드로 보기

**다음 토큰 예측 loss: shift를 직접 구현**

```python
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForCausalLM

tok = AutoTokenizer.from_pretrained("openai-community/gpt2")
model = AutoModelForCausalLM.from_pretrained("openai-community/gpt2")

ids = tok("The quick brown fox jumps over the lazy dog", return_tensors="pt").input_ids
logits = model(ids).logits                        # (1, T, 50257): 모든 위치에서 다음 토큰 분포

# 위치 t의 출력으로 t+1번째 토큰을 맞힌다 → logits는 마지막 제외, 라벨은 첫 토큰 제외
loss = F.cross_entropy(logits[:, :-1].reshape(-1, logits.size(-1)), ids[:, 1:].reshape(-1))

# Hugging Face는 labels=input_ids만 넘기면 내부에서 같은 shift를 해 줍니다
assert torch.allclose(loss, model(ids, labels=ids).loss, atol=1e-5)
```

**SFT: 프롬프트 부분은 loss에서 제외**

```python
prompt = "Q: What is the capital of France?\nA:"
answer = " Paris.<|endoftext|>"
p_ids = tok(prompt).input_ids
a_ids = tok(answer).input_ids

input_ids = torch.tensor([p_ids + a_ids])
labels = torch.tensor([[-100] * len(p_ids) + a_ids])    # 프롬프트 위치는 -100 → CE에서 무시
loss = model(input_ids, labels=labels).loss              # 응답 토큰에서만 loss 계산
```

**생성: 샘플링 옵션**

```python
inputs = tok("Once upon a time", return_tensors="pt")
out = model.generate(**inputs, max_new_tokens=30, do_sample=True, top_p=0.9, temperature=0.8,
                     pad_token_id=tok.eos_token_id)
print(tok.decode(out[0], skip_special_tokens=True))
```

## 5. BART와 T5

BERT(양방향 인코더)는 이해에 강하고, GPT(단방향 디코더)는 생성에 강합니다. **둘을 합치면 어떨까?**라는 질문에 대한 2019년의 두 가지 답이 BART와 T5입니다. 둘 다 원래 Transformer와 같은 **Encoder–Decoder** 구조에 **노이즈 제거(denoising) 사전학습**을 결합했습니다.

![BERT 방식: 양방향 인코더]({{ '/img/reviews/2026/lm-review-transformer-to-t5/bart-bert.png' | relative_url }})
![GPT 방식: 자기회귀 디코더]({{ '/img/reviews/2026/lm-review-transformer-to-t5/bart-gpt.png' | relative_url }})

![BART: 양방향 인코더와 자기회귀 디코더의 결합]({{ '/img/reviews/2026/lm-review-transformer-to-t5/bart-overview.png' | relative_url }})

*BART 논문 Figure 1. (a) BERT: 가린 토큰을 독립적으로 예측하므로 생성에 약합니다. (b) GPT: 왼쪽 문맥만 봅니다. (c) BART: 손상된 문서를 양방향 인코더로 읽고, 자기회귀 디코더로 **원문 전체**를 복원합니다. [원문](https://arxiv.org/abs/1910.13461)*

### 5.1 BART

| 항목 | 내용 |
|---|---|
| 논문 | BART: Denoising Sequence-to-Sequence Pre-training for NLG, Translation, and Comprehension (Lewis et al., ACL 2020, arXiv 2019.10) |
| 기관 | Facebook AI |
| 구조 | Encoder–Decoder. Base 6+6층(약 140M), Large 12+12층, hidden 1024(약 400M) |
| 데이터 | RoBERTa와 같은 160GB (뉴스, 책, 스토리, 웹 텍스트) |
| 학습 | batch 8,000, 50만 step |

**핵심 아이디어: 어떤 노이즈든 넣고 원문을 복원한다.** Encoder에 넣는 입력은 자유롭게 망가뜨려도 됩니다. Decoder는 항상 **원래 문서 전체**를 생성합니다. 논문에서는 다섯 가지 노이즈를 비교했습니다.

![BART에서 실험한 다섯 가지 입력 노이즈 변환]({{ '/img/reviews/2026/lm-review-transformer-to-t5/bart-noise.png' | relative_url }})

*BART 논문 Figure 2. 원문 `ABC.DE.`에 적용한 노이즈 변환입니다. [원문](https://arxiv.org/abs/1910.13461)*

| 노이즈 | 방식 |
|---|---|
| Token Masking | BERT처럼 토큰을 `[MASK]`로 치환 |
| Token Deletion | 토큰을 삭제. 모델이 **어느 위치가 빠졌는지**도 알아내야 함 |
| **Text Infilling** | Poisson($`\lambda=3`$) 길이의 span을 **`[MASK]` 하나**로 치환 (길이 0인 span 포함). 모델이 **몇 토큰이 빠졌는지**도 예측해야 함 |
| **Sentence Permutation** | 문장 순서를 섞음 |
| Document Rotation | 임의의 토큰에서 문서가 시작되도록 회전 |

최종 모델은 **Text Infilling(토큰의 30%) + Sentence Permutation** 조합을 썼습니다.

**Q. 입력을 이렇게 망가뜨리면 문장의 의미나 형식이 달라져서 문제가 되지 않나요?**

입력이 망가지는 것은 맞습니다. 하지만 BART는 **일부러** 입력을 망가뜨리고, 뒤에 있는 디코더가 원문을 복원하게 합니다. 핵심은 **망가지는 것은 입력뿐이고, 정답은 항상 원문**이라는 점입니다.

```
원문 (정답)    : A B C . D E .
Encoder 입력   : A _ . D _ E .      ← 여기만 망가짐 (span 하나 → [MASK] 하나, 길이 0인 span도 가능)
Decoder 정답   : A B C . D E .      ← loss는 항상 온전한 원문에 걸림
```

- **loss가 원문 전체에 걸립니다.** 그래서 모델이 망가진 문장을 출력하도록 학습될 일은 없고, 오히려 "망가진 입력 → 올바른 문장"으로 **고치는 법**을 배웁니다.
- **디코더는 자기회귀라서 출력 길이가 입력 길이에 묶여 있지 않습니다.** `[MASK]` 하나가 원래 3토큰이었든 0토큰이었든, 디코더가 필요한 만큼 생성하면 됩니다.
- **BERT에서는 이것이 불가능합니다.** BERT는 마스크 1개가 토큰 1개에 대응해야 하므로, 몇 토큰이 빠졌는지가 입력에 그대로 드러납니다. BART의 Text Infilling은 **몇 개가 빠졌는지까지 모델이 추론**해야 하는 더 어려운 과제이고, 이것이 생성 능력에 도움이 됩니다.
- **Sentence Permutation도 같은 원리입니다.** 섞인 문장을 원래 순서로 복원해야 하므로 문장 사이의 흐름(담화 구조)을 배웁니다.

**그래도 주의할 점**

1. **변환 종류에 따라 효과가 크게 다릅니다.** 논문 비교(Table 1)에서 Text Infilling이 가장 일관되게 좋았고, Token Deletion도 생성 태스크에서 좋았습니다. 반면 Document Rotation이나 Sentence Permutation은 **단독으로 쓰면 성능이 낮았습니다**. 그래서 최종 모델은 Text Infilling + Sentence Permutation 조합을 씁니다.
2. **가리는 정도는 하이퍼파라미터입니다.** 너무 많이 가리면 복원할 근거가 사라져서 정답이 사실상 추측이 되고 학습 신호가 약해집니다(일반적인 denoising 목표의 성질에 대한 해석입니다). 논문은 **토큰의 30%, span 길이 Poisson($`\lambda=3`$)**을 사용했습니다.
3. **빈칸의 정답이 여러 개일 수 있습니다.** `No <mask> in Syria`에는 그럴듯한 답이 많지만 정답 텍스트는 하나뿐입니다. 하지만 이것은 GPT의 다음 토큰 예측에도 똑같이 있는 불확실성입니다. 모델은 가능한 후보들에 확률을 나눠 주는 식으로 학습하므로 치명적이지 않습니다.
4. **사전학습과 파인튜닝 사이의 입력 분포 차이.** 파인튜닝 입력은 깨끗한 문장이라 사전학습 입력과 분포가 다릅니다. BERT의 `[MASK]` 문제와 같은 종류입니다. 다만 사전학습에서도 토큰 대부분(약 70%)은 가려지지 않은 채 들어가고, 실제로 BART는 파인튜닝 후 요약·QA·GLUE에서 좋은 성능을 보였으므로 실무에서는 큰 문제가 되지 않았습니다.

**T5와의 차이도 여기서 나옵니다.** T5는 가린 span만(`<X> for inviting <Y> last <Z>`) 생성하므로 학습 비용은 적지만, 디코더가 문장 전체를 다시 쓰는 연습은 덜 합니다. BART는 원문 전체를 다시 쓰기 때문에 비용이 크지만, **요약처럼 문장 전체를 새로 생성하는 태스크에 특히 강했습니다**.

**Contribution과 결과**

- 생성 태스크에서 강했습니다. CNN/DailyMail, XSum 요약에서 기존 대비 최대 6 ROUGE 향상, 생성형 QA와 대화에서도 SOTA를 달성했습니다.
- 이해 태스크(GLUE, SQuAD)에서는 RoBERTa와 비슷한 수준을 유지했습니다. 즉 **생성 능력을 얻으면서 이해 능력을 잃지 않았습니다**.
- 번역에서는 BART 앞에 새 소스 인코더를 붙이는 방식으로, 타깃 언어만으로 사전학습해도 back-translation 대비 1.1 BLEU 향상을 보였습니다.

**분류는 어떻게 푸나?** 같은 입력을 Encoder와 Decoder 양쪽에 넣고, **Decoder 마지막 토큰의 hidden state**를 분류기에 넣습니다. 마지막 토큰은 causal mask 아래에서도 전체 입력을 볼 수 있기 때문입니다(BERT의 `[CLS]` 역할).

![BART로 분류 문제를 푸는 방식]({{ '/img/reviews/2026/lm-review-transformer-to-t5/bart-classifier.png' | relative_url }})

*BART 논문 Figure 3(a). 분류 태스크에서는 Decoder 마지막 위치의 표현을 사용합니다. [원문](https://arxiv.org/abs/1910.13461)*

```python
from transformers import AutoTokenizer, BartForConditionalGeneration

# 1) Text infilling: <mask> 하나가 여러 토큰으로 복원되고, 문장 전체가 다시 생성됨
tok = AutoTokenizer.from_pretrained("facebook/bart-large")
model = BartForConditionalGeneration.from_pretrained("facebook/bart-large")
batch = tok("UN Chief Says There Is No <mask> in Syria", return_tensors="pt")
gen = model.generate(batch.input_ids, forced_bos_token_id=0, max_new_tokens=20)
print(tok.batch_decode(gen, skip_special_tokens=True))
# ['UN Chief Says There Is No Plan to Stop Chemical Weapons in Syria']

# 2) 요약: CNN/DailyMail로 파인튜닝한 BART. Encoder가 기사를 읽고 Decoder가 요약을 beam search로 생성
sum_tok = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
summarizer = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
long_article = ("The Transformer architecture, introduced in 2017, replaced recurrence with self-attention. "
                "It enabled highly parallel training and became the basis of BERT, GPT and T5. These models now "
                "power search, translation and chat assistants used by millions of people every day.")
inputs = sum_tok(long_article, return_tensors="pt", truncation=True)
summary_ids = summarizer.generate(**inputs, num_beams=4, min_length=10, max_length=40)
print(sum_tok.decode(summary_ids[0], skip_special_tokens=True))
```

### 5.2 T5

| 항목 | 내용 |
|---|---|
| 논문 | Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer (Raffel et al., JMLR 2020, arXiv 2019.10) |
| 기관 | Google |
| 구조 | Encoder–Decoder. Small 60M / Base 220M / Large 770M / 3B / 11B |
| 데이터 | **C4** (Colossal Clean Crawled Corpus). Common Crawl을 정제한 약 750GB |
| 토크나이저 | SentencePiece, vocab 32,000 |
| 특징 | Relative position bias, bias 없는 LayerNorm(RMSNorm 형태), Pre-LN |

**핵심 아이디어 1: 모든 문제를 Text-to-Text로.** 번역, 요약, 분류, 회귀까지 **입력도 텍스트, 출력도 텍스트**로 통일하고, 태스크는 **입력 앞의 prefix**로 구분합니다. 그래서 모델, loss, 디코딩 방식이 모든 태스크에서 같습니다.

![T5의 text-to-text 프레임워크]({{ '/img/reviews/2026/lm-review-transformer-to-t5/t5-text-to-text.png' | relative_url }})

*T5 논문 Figure 1. 번역, 문법성 판정(CoLA), 문장 유사도 회귀(STS-B), 요약을 모두 같은 모델이 텍스트로 입력받고 텍스트로 출력합니다. [원문](https://arxiv.org/abs/1910.10683)*

| 태스크 | Encoder 입력 | Decoder 출력 |
|---|---|---|
| 번역 | `translate English to German: That is good.` | `Das ist gut.` |
| 문법성 분류 (CoLA) | `cola sentence: The course is jumping well.` | `not acceptable` |
| 유사도 회귀 (STS-B) | `stsb sentence1: The rhino grazed on the grass. sentence2: A rhino is grazing in a field.` | `3.8` (0.2 단위로 반올림한 점수를 문자열로 출력) |
| 요약 | `summarize: state authorities dispatched emergency crews tuesday to ...` | `six people hospitalized after a storm in attala county.` |

**핵심 아이디어 2: Span Corruption 사전학습.** BERT의 MLM을 Encoder–Decoder에 맞게 바꾼 목표입니다.

![T5 span corruption 예시]({{ '/img/reviews/2026/lm-review-transformer-to-t5/t5-span-corruption.png' | relative_url }})

*T5 논문 Figure 2. 가린 span 하나를 sentinel 토큰 하나(`<X>`, `<Y>`)로 치환하고, 타깃은 sentinel과 가린 내용만 이어 붙인 것입니다. [원문](https://arxiv.org/abs/1910.10683)*

- 토큰의 **15%**를 가리되, 평균 길이 **3**의 **연속 span** 단위로 가립니다.
- span 하나는 고유한 **sentinel 토큰** 하나(`<extra_id_0>`, `<extra_id_1>`, …)로 바뀝니다.
- Decoder는 원문 전체가 아니라 **가린 부분만** `sentinel + 내용` 형태로 생성하고, 마지막 sentinel로 끝냅니다.

**BART vs T5, 비슷해 보이지만 다른 점**

| | BART | T5 |
|---|---|---|
| 마스크 토큰 | 모든 span에 같은 `[MASK]` | span마다 **다른** sentinel |
| Decoder 타깃 | **원문 전체** 복원 | **가린 span만** 생성 |
| 타깃 길이 | 길다 (원문 길이) | 짧다 (원문의 약 15%) → 학습 비용이 적음 |
| 다운스트림 형식 | 태스크별 head(분류) 또는 생성 | 전부 텍스트 생성 (prefix로 구분) |

**Contribution: 체계적인 비교 연구.** T5 논문은 새 모델 하나를 제안하는 데 그치지 않고, 구조(Encoder–Decoder vs LM vs Prefix LM), 사전학습 목표(LM, BERT식, deshuffling, span corruption 등), 데이터셋, 전이 학습 전략, 스케일을 **같은 조건에서 비교한 대규모 실험 보고서**입니다. 결론은 "Encoder–Decoder + span corruption + 대규모 정제 데이터 + 큰 모델"이 가장 좋았다는 것이고, 11B 모델로 GLUE, SuperGLUE(89.3, 사람 89.8), SQuAD, CNN/DM에서 SOTA를 기록했습니다.

**후속 모델**: T5 v1.1(GeGLU, C4만 사용해 사전학습), mT5(101개 언어), **Flan-T5**(1,800여 개 태스크로 instruction tuning), UL2(여러 denoising 목표 혼합).

```python
import torch
from transformers import AutoTokenizer, T5ForConditionalGeneration

tok = AutoTokenizer.from_pretrained("google-t5/t5-small")
model = T5ForConditionalGeneration.from_pretrained("google-t5/t5-small")

# 1) Span corruption 사전학습 loss: labels만 넘기면 decoder_input_ids는 내부에서 shift해서 만듦
inp = tok("Thank you <extra_id_0> me to your party <extra_id_1> week.", return_tensors="pt").input_ids
tgt = tok("<extra_id_0> for inviting <extra_id_1> last <extra_id_2>", return_tensors="pt").input_ids
print(model(input_ids=inp, labels=tgt).loss)

# 2) 다운스트림도 text-to-text: prefix만 바꾸면 됨
for text in ["translate English to German: That is good.",
             "cola sentence: The course is jumping well.",
             "summarize: The Transformer replaces recurrence with attention, making training highly parallel."]:
    ids = tok(text, return_tensors="pt").input_ids
    print(tok.decode(model.generate(ids, max_new_tokens=30)[0], skip_special_tokens=True))
# Das ist gut.
# acceptable     ← 정답은 "unacceptable". 가장 작은 t5-small은 이렇게 틀리기도 합니다.
# Transformer replaces recurrence with attention, making training highly parallel.
```

## 6. 인코더와 디코더가 문제를 학습하는 방식의 차이

지금까지 본 모델들의 학습 방식은 **어텐션 마스크 모양**과 **loss를 거는 위치**로 정리할 수 있습니다.

![Fully-visible, Causal, Causal with prefix 어텐션 마스크]({{ '/img/reviews/2026/lm-review-transformer-to-t5/t5-attention-masks.png' | relative_url }})

*T5 논문 Figure 3. 진한 칸이 "출력 위치 $`y_i`$가 입력 위치 $`x_j`$를 볼 수 있음"을 뜻합니다. Fully-visible은 인코더(BERT), Causal은 디코더(GPT), Causal with prefix는 Prefix LM입니다. [원문](https://arxiv.org/abs/1910.10683)*

| | 인코더 계열 (BERT) | 디코더 계열 (GPT) | 인코더–디코더 (Transformer, BART, T5) |
|---|---|---|---|
| 어텐션 | Fully-visible (양방향) | Causal (왼쪽만) | Enc: 양방향 / Dec: causal + cross-attn |
| 입력 | 일부가 가려진 문장 | 원문 그대로 | Enc: 원문 또는 손상된 문장 / Dec: 타깃을 한 칸 shift |
| 예측 대상 | 가려진 위치의 원래 토큰 | 모든 위치의 다음 토큰 | 타깃 시퀀스의 다음 토큰 |
| loss 위치 | 마스킹된 약 15% | 전체 토큰 | 타깃(Decoder) 전체 |
| 라벨 생성 | 마스킹 전 원문 | 입력을 한 칸 shift | 원문 / 가린 span / 태스크 정답 |
| 학습 신호 밀도 | 낮음 | 높음 | 중간 (T5는 타깃이 짧음) |
| 사전학습–사용 괴리 | `[MASK]`는 파인튜닝에 없음 | 거의 없음 (학습도 사용도 다음 토큰 예측) | 적음 |

**세 가지 마스크를 직접 만들어 보기**

```python
import torch

T, prefix_len = 5, 3

fully_visible = torch.ones(T, T)                 # BERT: 모두 볼 수 있음
causal = torch.tril(torch.ones(T, T))            # GPT: 자기 자신과 왼쪽만
prefix_lm = causal.clone()
prefix_lm[:, :prefix_len] = 1                    # Prefix LM: prefix 구간은 양방향, 이후는 causal

print(prefix_lm)
# tensor([[1., 1., 1., 0., 0.],
#         [1., 1., 1., 0., 0.],
#         [1., 1., 1., 0., 0.],
#         [1., 1., 1., 1., 0.],
#         [1., 1., 1., 1., 1.]])
```

**왜 이 차이가 중요한가**

1. **양방향 = 정보 누설 위험.** 양방향 어텐션에서 "다음 토큰 맞히기"를 하면 정답이 입력에 그대로 보입니다. 그래서 BERT는 **정답을 가리는(MASK)** 방식을 택했고, 그 대가로 전체 토큰 중 일부에서만 학습 신호를 얻습니다.
2. **Causal = 누설 없음 + 전 위치 학습.** 오른쪽을 가려 두면 모든 위치에서 동시에 "다음 토큰"을 맞히는 문제를 낼 수 있습니다. 데이터 효율이 좋고 구조가 단순해서 스케일을 키우기 쉽습니다. 오늘날 LLM이 대부분 디코더 전용인 이유 중 하나입니다.
3. **인코더–디코더 = 입력과 출력의 역할 분리.** 입력(원문)은 양방향으로 충분히 이해하고, 출력은 causal하게 생성합니다. 입력과 출력이 명확히 구분되는 번역·요약에 자연스럽게 맞습니다.

## 7. 학습·검증 데이터 샘플과 loss 계산 디테일

앞에서 "loss를 어디에 거는가"를 말로 설명했습니다. 이 절에서는 **원천 데이터 한 줄이 실제 배치 텐서가 되고, 그 텐서에서 loss 숫자 하나가 나오기까지**의 과정을 모델 계열별로 따라가 봅니다. 표의 토큰은 모두 실제 토크나이저(`bert-base-uncased`, `bert-base-cased`, `gpt2`, `t5-small`)로 뽑은 결과입니다.

### 7.1 공통 규칙: 위치별 Cross-Entropy와 `-100`

세 계열 모두 loss 계산 방식은 같습니다. 모델은 위치마다 vocab 크기의 점수(logit)를 내고, **정답이 있는 위치에서만** cross-entropy를 계산해 평균을 냅니다.

| 텐서 | 모양 | 의미 |
|---|---|---|
| `input_ids` | (B, T) | 모델에 들어가는 토큰 id |
| `attention_mask` | (B, T) | 1 = 실제 토큰, 0 = padding (어텐션에서 제외) |
| `logits` | (B, T, V) | 위치마다 vocab V개에 대한 점수 |
| `labels` | (B, T) | 위치마다 정답 토큰 id. **`-100`이면 loss에서 제외** |

```math
\mathcal{L} = -\frac{1}{N}\sum_{(b,t)\,:\,y_{b,t} \neq -100} \log \frac{\exp(z_{b,t,y_{b,t}})}{\sum_{v=1}^{V} \exp(z_{b,t,v})}
```

$`N`$은 라벨이 `-100`이 아닌 위치의 개수입니다. 즉 **시퀀스 단위가 아니라 토큰 단위 평균**입니다. 계열별 차이는 결국 **`labels`의 어느 칸에 정답을 넣고 어느 칸을 `-100`으로 비우는가**뿐입니다.

**위치 하나에서의 계산 예시.** vocab이 `[Paris, Lyon, Rome]` 세 개라고 하고, 어떤 위치의 logit이 `[2.0, 1.0, 0.1]`, 정답이 `Paris`라고 해 봅시다.

```
softmax([2.0, 1.0, 0.1]) = [0.659, 0.242, 0.099]
loss = -log(0.659) = 0.417
```

정답 확률이 1에 가까워질수록 loss는 0에 가까워지고, 정답 확률이 낮을수록 loss가 커집니다.

```python
import torch
import torch.nn.functional as F

logits = torch.tensor([[2.0, 1.0, 0.1]])            # (위치 1개, V=3)
print(F.cross_entropy(logits, torch.tensor([0])))   # tensor(0.4170)

# 실제 모델에서는 (B, T, V) → (B*T, V)로 펴고, -100 위치는 자동으로 제외
def token_ce(logits, labels):
    return F.cross_entropy(logits.reshape(-1, logits.size(-1)), labels.reshape(-1), ignore_index=-100)
```

**검증(validation)은 두 가지로 봅니다.**

1. **Validation loss**: 학습과 똑같이 정답을 넣고(teacher forcing) gradient 없이 loss만 계산합니다. 언어모델에서는 이것을 **Perplexity = exp(loss)**로 바꿔서 보고하기도 합니다. "매 위치에서 평균적으로 몇 개의 후보 사이에서 헷갈리는가"로 해석할 수 있습니다.
2. **태스크 지표**: 실제로 예측(분류는 argmax, 생성은 `generate`)을 한 뒤 정답과 비교합니다. Accuracy, F1, Exact Match, BLEU, ROUGE 등이 여기에 해당합니다.

생성 모델에서는 두 값이 다르게 움직일 수 있습니다. validation loss는 **정답 prefix를 보면서** 다음 토큰을 맞히는 점수이고, 실제 생성은 **자기가 만든 prefix 위에서** 이어 쓰기 때문입니다(exposure bias). 그래서 생성 모델은 loss와 생성 지표를 함께 봅니다.

### 7.2 인코더 (BERT)

**(1) 사전학습 데이터: 라벨 없는 원문**

```text
# 원천 데이터: 한 줄에 한 문장, 문서 사이는 빈 줄
my dog is hairy
he likes to play

the stock market fell sharply today
...
```

같은 문서에서 연속된 두 문장(IsNext) 또는 다른 문서의 문장(NotNext)을 뽑아 한 샘플을 만들고, 15%를 마스킹합니다. 아래는 `hairy`와 `play`가 선택된 경우입니다. `hairy`는 80% 규칙에 따라 `[MASK]`가 됐고, `play`는 10% 규칙에 따라 **원래 토큰 그대로** 남았지만 **예측 대상**입니다.

| 위치 | 원래 토큰 | `input_ids` (마스킹 후) | `token_type_ids` | `labels` |
|---|---|---|---|---|
| 0 | `[CLS]` | `[CLS]` (101) | 0 | -100 |
| 1 | `my` | `my` | 0 | -100 |
| 2 | `dog` | `dog` | 0 | -100 |
| 3 | `is` | `is` | 0 | -100 |
| 4 | `hairy` | **`[MASK]` (103)** | 0 | **15892 (`hairy`)** |
| 5 | `[SEP]` | `[SEP]` (102) | 0 | -100 |
| 6 | `he` | `he` | 1 | -100 |
| 7 | `likes` | `likes` | 1 | -100 |
| 8 | `to` | `to` | 1 | -100 |
| 9 | `play` | **`play` (그대로)** | 1 | **2377 (`play`)** |
| 10 | `[SEP]` | `[SEP]` | 1 | -100 |

`next_sentence_label = 0` (Hugging Face 규약에서 0이 IsNext)

- **MLM loss**: `logits` (1, 11, 30522) 중 위치 4와 9의 **두 칸에서만** CE를 계산해 평균합니다.
- **NSP loss**: 위치 0(`[CLS]`)의 출력을 2-class 분류기에 넣어 CE를 계산합니다.
- **전체 loss** = MLM loss + NSP loss
- **검증**: 따로 떼어 둔 문서에 같은 마스킹을 적용해 MLM loss(또는 마스크 위치 정확도)와 NSP 정확도를 봅니다. 사전학습 모델의 최종 품질은 결국 다운스트림 태스크 성능으로 평가합니다.

**(2) 파인튜닝 데이터: 태스크별 라벨**

```javascript
// 문장 분류 (SST-2) — train.jsonl / valid.jsonl 같은 형식
{"sentence": "a gripping, funny and genuinely moving film", "label": 1}
{"sentence": "the plot is a mess and the acting is worse",   "label": 0}

// NER (CoNLL-2003 형식) — 단어 단위 태그
{"tokens": ["Euisuk", "Chung", "works", "at", "Google"], "ner_tags": ["B-PER", "I-PER", "O", "O", "B-ORG"]}

// 추출형 QA (SQuAD 형식) — 정답은 문단 안의 문자 위치
{"question": "Where is the Eiffel Tower?",
 "context": "The Eiffel Tower is a wrought-iron lattice tower in Paris, France.",
 "answers": {"text": ["Paris"], "answer_start": [52]}}
```

| 태스크 | `labels` 모양 | loss | 검증 지표 |
|---|---|---|---|
| 문장 분류 | (B,) 문장당 정수 1개 | `[CLS]` logits (B, C)에 CE | Accuracy, F1 (MNLI는 accuracy, STS-B는 Pearson/Spearman) |
| NER | (B, T) 토큰마다 태그 id | 태그가 있는 토큰 위치에서 CE | 엔티티 단위 F1 (seqeval) |
| 추출형 QA | `start_positions` (B,), `end_positions` (B,) | (CE(start) + CE(end)) / 2 | Exact Match, F1 |

**NER에서 서브워드 정렬.** 태그는 단어 단위인데 BERT는 서브워드 단위로 자르므로, **각 단어의 첫 서브워드에만 태그를 주고** 나머지와 특수 토큰은 `-100`으로 둡니다.

| 토큰 | `[CLS]` | `E` | `##ui` | `##su` | `##k` | `Chung` | `works` | `at` | `Google` | `[SEP]` |
|---|---|---|---|---|---|---|---|---|---|---|
| word_id | – | 0 | 0 | 0 | 0 | 1 | 2 | 3 | 4 | – |
| `labels` | -100 | B-PER | -100 | -100 | -100 | I-PER | O | O | B-ORG | -100 |

**QA에서 문자 위치를 토큰 위치로 변환.** `answer_start: 52`는 문자 위치입니다. `offset_mapping`으로 토큰 위치로 바꾸면 `[CLS] Where is the E ##iff ##el Tower ? [SEP] The E ##iff ##el Tower is a wrought - iron lattice tower in Paris , France . [SEP]`에서 `Paris`는 23번 토큰이므로 `start_positions = end_positions = 23`이 됩니다.

### 7.3 디코더 (GPT)

**(1) 사전학습 데이터: 문서를 이어 붙여 고정 길이로 자르기 (packing)**

```json
{"text": "I like cats."}
{"text": "Paris is in France."}
```

문서를 토큰화하고 문서 끝에 `<|endoftext|>`(아래 표에서는 `<eos>`)를 붙여 **하나로 이어 붙인 뒤** 길이 L 블록으로 자릅니다. padding이 없어 계산 낭비가 없습니다. 아래는 L = 5인 예입니다(남는 토큰은 버리거나 다음 배치로 넘깁니다).

```
이어 붙인 토큰: I | Ġlike | Ġcats | . | <eos> | Paris | Ġis | Ġin | ĠFrance | . | <eos>
블록 1        : I  Ġlike  Ġcats  .  <eos>
블록 2        : Paris  Ġis  Ġin  ĠFrance  .
```

블록 1의 `input_ids`와 `labels`는 **같은 값**입니다. 한 칸 shift는 모델(또는 loss 함수) 안에서 합니다.

| 위치 t | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| 입력 토큰 | `I` | `Ġlike` | `Ġcats` | `.` | `<eos>` |
| 이 위치의 출력이 맞혀야 할 토큰 | `Ġlike` | `Ġcats` | `.` | `<eos>` | (없음) |

- 블록 길이가 L이면 **L − 1개 위치**에서 loss가 나옵니다. 배치 전체로는 B × (L − 1)개 위치의 평균입니다.
- **검증**: 학습에 쓰지 않은 텍스트로 같은 loss를 계산하고 PPL로 봅니다. 예를 들어 GPT-2 small에 `The capital of France is Paris.`(7토큰 → 6개 위치)를 넣으면 평균 loss ≈ 3.80, PPL ≈ 44.6이 나옵니다.

**(2) SFT 데이터: 대화 → 템플릿 → 프롬프트 마스킹**

```json
{"messages": [{"role": "user", "content": "What is the capital of France?"},
              {"role": "assistant", "content": "Paris."}]}
```

채팅 템플릿으로 한 시퀀스로 만든 뒤, **사용자 발화(프롬프트) 부분의 라벨은 `-100`**으로 둡니다. 아래는 간단한 `Q: … A:` 템플릿을 GPT-2 토크나이저로 자른 결과입니다.

| 위치 | 0–11 | 12 | 13 | 14 |
|---|---|---|---|---|
| 입력 토큰 | `Q` `:` `ĠWhat` `Ġis` `Ġthe` `Ġcapital` `Ġof` `ĠFrance` `?` `Ċ` `A` `:` | `ĠParis` | `.` | `<eos>` |
| `labels` | -100 × 12 | 6342 | 13 | 50256 |

shift 후에는 위치 11(`:`), 12(`ĠParis`), 13(`.`)의 출력이 각각 `ĠParis`, `.`, `<eos>`를 맞히는 **3개 위치에서만** loss가 계산됩니다. 모델은 질문을 **읽기는 하지만**, 질문을 생성하도록 학습되지는 않습니다.

- 배치 안의 길이를 맞추는 padding 위치도 `labels = -100`, `attention_mask = 0`입니다. GPT-2에는 pad 토큰이 없어서 보통 `pad_token = eos_token`으로 둡니다.
- **검증**: 응답 토큰 기준 validation loss와 함께, 실제로 생성한 답을 정답과 비교합니다(Exact Match, 사람 평가, LLM-as-a-judge 등).

### 7.4 인코더–디코더 (T5, BART)

**(1) 사전학습 데이터**: 5.2절의 span corruption 예시가 그대로 한 샘플입니다(`inputs`는 Encoder로, `targets`는 labels로).

**(2) 파인튜닝 데이터: source / target 쌍**

```javascript
// train.jsonl / valid.jsonl
{"source": "summarize: The cat sat on the mat all day.", "target": "A cat rested."}
{"source": "translate English to German: That is good.", "target": "Das ist gut."}
```

| | 토큰 (t5-small) |
|---|---|
| Encoder `input_ids` | `▁summarize` `:` `▁The` `▁cat` `▁` `s` `at` `▁on` `▁the` `▁mat` `▁all` `▁day` `.` `</s>` |
| `labels` | `▁A` `▁cat` `▁reste` `d` `.` `</s>` |

`labels`만 넘기면 모델이 내부에서 오른쪽으로 한 칸 밀어 `decoder_input_ids`를 만듭니다. T5는 시작 토큰으로 `<pad>`를 씁니다.

| Decoder 위치 t | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| `decoder_input_ids` | `<pad>` | `▁A` | `▁cat` | `▁reste` | `d` | `.` |
| `labels` (이 위치의 정답) | `▁A` | `▁cat` | `▁reste` | `d` | `.` | `</s>` |

- GPT와 달리 **입력과 라벨의 위치가 이미 맞춰져 있습니다**(shift를 decoder 입력 쪽에서 했기 때문). 위치 t의 logits를 `labels[t]`와 바로 비교합니다.
- loss는 target의 6개 위치 평균입니다. **Encoder 입력 토큰에는 loss가 없습니다.**
- 배치 안에서 target 길이가 다르면 `labels`의 padding을 `-100`으로 바꿔야 합니다. 토크나이저는 pad id(T5는 0)로 채우므로, `DataCollatorForSeq2Seq`를 쓰거나 직접 바꿔 줍니다.
- **검증**: (a) teacher forcing으로 계산한 validation loss, (b) `generate()`(보통 beam search)로 만든 출력을 reference와 비교한 ROUGE(요약), BLEU(번역), Exact Match(QA)를 함께 봅니다.

### 7.5 한눈에 비교

| | 인코더 (BERT) | 디코더 (GPT) | 인코더–디코더 (T5) |
|---|---|---|---|
| 사전학습 원천 샘플 | `my dog is hairy / he likes to play` | `{"text": "I like cats."}` | `{"text": "Thank you for inviting me ..."}` |
| 모델 입력 | 마스킹된 문장쌍 | 이어 붙인 블록 | Enc: 손상 문장 / Dec: shift된 target |
| `labels` | 마스킹 위치만 원래 토큰, 나머지 -100 | `input_ids`와 동일 (내부 shift) | sentinel + 가린 span |
| loss가 계산되는 위치 | 약 15% + `[CLS]`(NSP) | 블록의 L − 1개 전부 | target 전체 |
| 파인튜닝 원천 샘플 | `{"sentence", "label"}` | `{"messages": [...]}` | `{"source", "target"}` |
| 파인튜닝 loss 위치 | `[CLS]` 1개 / 토큰별 태그 / start·end | 응답 토큰만 | target 전체 |
| 주요 검증 지표 | Accuracy, F1, EM | Val loss, PPL, 생성 품질 | Val loss, ROUGE, BLEU, EM |

**세 계열에 모두 쓸 수 있는 검증 루프**

```python
import math
import torch

@torch.no_grad()
def evaluate(model, loader, causal_lm=False):
    """토큰 가중 평균 validation loss와 perplexity."""
    model.eval()
    total_loss, total_tokens = 0.0, 0
    for batch in loader:                          # batch: input_ids, attention_mask, labels (+ 필요한 키)
        out = model(**batch)                      # labels를 넘기면 out.loss = 위 수식의 토큰 평균 CE
        labels = batch["labels"][:, 1:] if causal_lm else batch["labels"]   # 디코더는 내부 shift로 첫 라벨이 빠짐
        n = (labels != -100).sum().item()         # 실제로 loss에 들어간 토큰 수
        total_loss += out.loss.item() * n         # 배치별 평균 → 토큰 수로 가중해서 합산
        total_tokens += n
    loss = total_loss / total_tokens
    return loss, math.exp(loss)                   # (val loss, perplexity)
```

배치마다 유효 토큰 수가 다르기 때문에 `out.loss`를 **단순 평균하면 안 되고** 토큰 수로 가중해야 정확합니다. gradient accumulation을 할 때도 같은 이유로 주의가 필요합니다.

## 8. 인코더와 디코더가 문제를 푸는 방식의 차이

학습이 끝난 뒤 **추론할 때** 문제를 푸는 방식도 다릅니다.

| | 인코더 (BERT) | 디코더 (GPT) | 인코더–디코더 (T5, BART) |
|---|---|---|---|
| forward 횟수 | **1회** | 생성 토큰 수만큼 반복 | Encoder 1회 + Decoder 반복 |
| 출력 형태 | 위치별 벡터 → head (클래스, 태그, span 위치) | 텍스트 (한 토큰씩) | 텍스트 (한 토큰씩) |
| 답의 공간 | 미리 정한 라벨 집합 또는 입력 안의 구간 | 열린 vocab 시퀀스 | 열린 vocab 시퀀스 |
| 새 태스크 적용 | head를 붙여 파인튜닝 | 프롬프트만 바꿈 (few-shot) 또는 SFT | prefix/지시문 + 파인튜닝 |
| 대표 문제 | 분류, NER, 추출형 QA, 임베딩·검색 | 대화, 코드, 범용 생성, 추론 | 번역, 요약, 생성형 QA |
| 속도 | 빠름 (병렬, 한 번) | 출력 길이에 비례 (KV cache로 가속) | 중간 |

**인코더: 한 번의 forward로 끝**

```python
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

name = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
tok = AutoTokenizer.from_pretrained(name)
model = AutoModelForSequenceClassification.from_pretrained(name)

with torch.no_grad():
    logits = model(**tok("this movie was surprisingly good", return_tensors="pt")).logits
print(model.config.id2label[logits.argmax(-1).item()])   # POSITIVE — forward 한 번 + argmax
```

**디코더: 한 토큰씩 반복 + KV cache**

```python
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

tok = AutoTokenizer.from_pretrained("openai-community/gpt2")
model = AutoModelForCausalLM.from_pretrained("openai-community/gpt2")

ids = tok("The capital of France is", return_tensors="pt").input_ids
past = None
with torch.no_grad():
    for _ in range(10):
        # 첫 step은 프롬프트 전체, 이후에는 새 토큰 하나만 넣고 앞 토큰의 K/V는 cache에서 재사용
        out = model(input_ids=ids if past is None else ids[:, -1:], past_key_values=past, use_cache=True)
        past = out.past_key_values
        next_id = out.logits[:, -1, :].argmax(-1, keepdim=True)   # 마지막 위치의 분포만 사용 (greedy)
        ids = torch.cat([ids, next_id], dim=-1)
        if next_id.item() == tok.eos_token_id:
            break
print(tok.decode(ids[0]))
# The capital of France is the capital of the French Republic, and the capital
# (GPT-2 small + greedy라 반복적인 출력이 나옵니다)
```

**인코더–디코더: Encoder는 한 번, Decoder는 반복**

```python
import torch
from transformers import AutoTokenizer, T5ForConditionalGeneration

tok = AutoTokenizer.from_pretrained("google-t5/t5-small")
model = T5ForConditionalGeneration.from_pretrained("google-t5/t5-small")

enc_in = tok("translate English to German: That is good.", return_tensors="pt")
with torch.no_grad():
    enc_out = model.get_encoder()(**enc_in)                      # 원문은 한 번만 인코딩
    dec_ids = torch.tensor([[model.config.decoder_start_token_id]])
    for _ in range(20):
        out = model(encoder_outputs=enc_out, attention_mask=enc_in.attention_mask,
                    decoder_input_ids=dec_ids)                   # Decoder는 cross-attn으로 enc_out 참조
        next_id = out.logits[:, -1].argmax(-1, keepdim=True)
        dec_ids = torch.cat([dec_ids, next_id], dim=-1)
        if next_id.item() == tok.eos_token_id:
            break
print(tok.decode(dec_ids[0], skip_special_tokens=True))          # Das ist gut.
```

(설명을 위해 Decoder 쪽 KV cache는 생략했습니다. 실제로는 `model.generate()`가 cache와 beam search를 모두 처리해 줍니다.)

**디코딩 전략 요약**

| 전략 | 방식 | 특징 |
|---|---|---|
| Greedy | 매 step 최고 확률 토큰 선택 | 빠르지만 반복적인 출력이 나오기 쉬움 |
| Beam search | 상위 k개 후보 시퀀스를 유지 | 번역·요약처럼 정답이 비교적 정해진 태스크에 적합 |
| Top-k / Top-p 샘플링 | 상위 k개 또는 누적확률 p 안에서 샘플링 | 다양하고 자연스러운 생성, 대화·창작에 적합 |
| Temperature | softmax 전에 logits를 T로 나눔 | T < 1이면 보수적, T > 1이면 다양한 출력 |

## 정리

| | Transformer | BERT | GPT | BART | T5 |
|---|---|---|---|---|---|
| 구조 | Enc–Dec | Enc | Dec | Enc–Dec | Enc–Dec |
| 한 줄 요약 | 어텐션만으로 seq2seq | 가려진 단어를 양방향으로 맞히기 | 다음 단어 맞히기를 스케일업 | 망가진 문서를 통째로 복원 | 가린 span만 생성, 모든 태스크를 text-to-text로 |
| 핵심 기여 | Self-attention, 병렬 학습 | Deep bidirectional, 사전학습–파인튜닝 정착 | 생성형 사전학습, zero/few-shot, ICL | 임의 노이즈 denoising seq2seq | 통합 프레임워크, 대규모 체계적 비교, C4 |
| 입력 → 출력 | 원문 → 번역문 | 마스크된 문장 → 위치별 벡터 | 텍스트 → 다음 토큰 | 손상 문서 → 원문 | 손상 문장 → sentinel + span |
| loss 위치 | Decoder 전체 | 마스크 위치(15%) + `[CLS]` | 전체 토큰 | Decoder 전체(원문 길이) | Decoder 전체(짧은 타깃) |
| 강점 | 번역 | 분류, 추출, 임베딩 | 생성, 범용 | 요약, 생성 | 멀티태스크, 생성 |

정리하면 다음과 같습니다.

- **Transformer**가 뼈대를 만들었습니다(Encoder + Decoder + attention).
- **BERT**는 Encoder만 떼어서 "이해"를 위한 사전학습 방법(MLM)을 만들었습니다.
- **GPT**는 Decoder만 떼어서 "다음 토큰 예측" 하나로 스케일을 키웠고, 이것이 지금의 LLM으로 이어졌습니다.
- **BART와 T5**는 다시 Encoder–Decoder로 돌아가 두 장점을 합쳤습니다.

### 스스로 점검해 볼 질문

1. BERT가 양방향 어텐션에서 "다음 토큰 예측"을 쓸 수 없는 이유는 무엇이고, MLM은 이를 어떻게 피하나요? 그 대가는 무엇인가요?
2. Transformer 학습에서 teacher forcing과 causal mask가 없으면 학습 속도와 정보 누설 측면에서 각각 무엇이 달라지나요?
3. 같은 문장 `Thank you for inviting me to your party last week.`에 대해 BERT, BART, T5 각각의 **Encoder 입력과 정답(label)**을 직접 써 보세요.
4. BART는 분류 문제에서 왜 Decoder의 **마지막** 토큰 표현을 쓰나요? 첫 토큰을 쓰면 어떤 문제가 생기나요?
5. GPT의 SFT에서 프롬프트 토큰을 loss에서 제외하는 이유는 무엇일까요?
6. 추론 비용 관점에서 분류 문제를 BERT로 풀 때와 GPT에 프롬프트로 풀 때 어떤 차이가 있나요?
7. 7.3절의 SFT 샘플에서 loss가 계산되는 위치는 몇 개이고, 각 위치의 출력은 어떤 토큰을 맞혀야 하나요? T5의 같은 태스크 샘플과 비교하면 shift가 어디서 일어나나요?
8. BART는 입력을 크게 망가뜨려도 왜 학습이 무너지지 않나요? 반대로 가리는 비율을 90%로 올리면 어떤 일이 생길까요?

## 참고 문헌

- Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), NeurIPS 2017.
- Devlin et al., [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805), NAACL 2019.
- Radford et al., [Improving Language Understanding by Generative Pre-Training](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf), OpenAI 2018.
- Radford et al., [Language Models are Unsupervised Multitask Learners](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf), OpenAI 2019.
- Brown et al., [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165), NeurIPS 2020.
- Ouyang et al., [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155), NeurIPS 2022.
- Lewis et al., [BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension](https://arxiv.org/abs/1910.13461), ACL 2020.
- Raffel et al., [Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer](https://arxiv.org/abs/1910.10683), JMLR 2020.
- Liu et al., [RoBERTa: A Robustly Optimized BERT Pretraining Approach](https://arxiv.org/abs/1907.11692), 2019.
