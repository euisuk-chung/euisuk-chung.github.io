---
title: "(설명추가) Perplexity와 BLEU 스코어에 대한 보충 설명"
date: "2025-01-27"
tags:
  - "도서리뷰"
year: "2025"
---

# (설명추가) Perplexity와 BLEU 스코어에 대한 보충 설명

원본 게시글: https://velog.io/@euisuk-chung/설명추가-Perplexity와-BLEU-스코어에-대한-상세-정리



![](https://velog.velcdn.com/images/euisuk-chung/post/748459ec-3899-4e1c-8cea-1f705a3e09db/image.png)

책 19쪽에 해당 스코어에 대한 언급은 있지만, 개인적으로 좀 더 정리가 필요하다고 생각하여 아래와 같이 정리를 수행하였습니다.

### **Perplexity**

#### **1. Perplexity란 무엇인가?**

* Perplexity는 "혼란도"라는 뜻으로, 언어 모델이 주어진 문장을 얼마나 잘 예측했는지를 측정하는 지표입니다.
* 낮은 Perplexity 값은 모델이 주어진 텍스트를 잘 예측했음을 나타내며, 높은 Perplexity 값은 모델이 텍스트를 예측하는 데 어려움을 겪었음을 의미합니다.
* Perplexity는 **모델이 단어를 예측할 때 평균적으로 고려해야 할 선택지의 수**를 나타냅니다.
* 예를 들어, Perplexity가 10이라면, 모델은 평균적으로 단어 하나를 예측하기 위해 10가지 선택지를 고려한다는 의미입니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/111b5046-8aed-4290-828f-de828e342006/image.png)

> Source: <https://towardsdatascience.com/perplexity-intuition-and-derivation-105dd481c8f3>

#### **2. Perplexity의 정의**

Perplexity는 다음과 같이 정의됩니다:

PP(W)=P(W)−1/NPP(W) = P(W)^{-{1}/{N}}PP(W)=P(W)−1/N

여기서:

* P(W)P(W)P(W): 문장 WWW의 확률 (언어 모델이 문장 WWW를 생성할 확률)
* NNN: 문장 WWW의 단어 개수

이를 로그 형태로 나타내면:

PP(W)=e−1Nlog⁡P(W)PP(W) = e^{-\frac{1}{N} \log P(W)}PP(W)=e−N1​logP(W)
#### **3. Perplexity의 계산 과정**

1. **문장 WWW의 확률 계산**:  
   
   문장 WWW는 각 단어의 조건부 확률로 계산됩니다:
   
   P(W)=P(w1)⋅P(w2∣w1)⋅P(w3∣w1,w2)⋯P(wN∣w1,w2,…,wN−1)P(W) = P(w\_1) \cdot P(w\_2|w\_1) \cdot P(w\_3|w\_1, w\_2) \cdots P(w\_N|w\_1, w\_2, \dots, w\_{N-1})P(W)=P(w1​)⋅P(w2​∣w1​)⋅P(w3​∣w1​,w2​)⋯P(wN​∣w1​,w2​,…,wN−1​)
   
   이 계산은 언어 모델이 단어를 문맥에 기반해 얼마나 잘 예측했는지를 나타냅니다.
2. **로그 변환**:  
   
   곱셈 형태의 확률 P(W)P(W)P(W)를 로그를 통해 합산 형태로 변환합니다:
   
   log⁡P(W)=log⁡P(w1)+log⁡P(w2∣w1)+⋯+log⁡P(wN∣w1,w2,…,wN−1)\log P(W) = \log P(w\_1) + \log P(w\_2|w\_1) + \dots + \log P(w\_N|w\_1, w\_2, \dots, w\_{N-1})logP(W)=logP(w1​)+logP(w2​∣w1​)+⋯+logP(wN​∣w1​,w2​,…,wN−1​)
   
   이를 단어 개수 NNN으로 정규화하면:
   
   −1Nlog⁡P(W)=−1N∑i=1Nlog⁡P(wi)-\frac{1}{N} \log P(W) = -\frac{1}{N} \sum\_{i=1}^N \log P(w\_i)−N1​logP(W)=−N1​i=1∑N​logP(wi​)
3. **Perplexity 계산**:  
   
   로그를 지수 함수로 변환하여 최종적으로 Perplexity를 계산합니다:
   
   PP(W)=e−1N∑i=1Nlog⁡P(wi)PP(W) = e^{-\frac{1}{N} \sum\_{i=1}^N \log P(w\_i)}PP(W)=e−N1​∑i=1N​logP(wi​)
   
   이 계산 결과는 언어 모델이 단어를 얼마나 효율적으로 예측했는지 나타냅니다.

#### **4. Perplexity의 직관적 해석**

* Perplexity는 모델이 단어 시퀀스를 예측하는 **평균적인 복잡도**를 나타냅니다.
* **낮은 Perplexity 값**: 모델이 주어진 문장을 잘 예측 → 선택지가 적음.
* **높은 Perplexity 값**: 모델이 주어진 문장을 잘 예측하지 못함 → 선택지가 많음.
* Perplexity 값이 작을수록 모델의 예측이 더 정확하며, 언어 모델이 더 적합하다는 것을 의미합니다.

#### **5. Perplexity에서 지수 (-\frac{1}{N})을 사용하는 이유**

1. **정규화를 통해 평균화**:
   
   * 문장의 확률 P(W)P(W)P(W)는 문장이 길어질수록 매우 작아지는 값이므로, 단어 개수 NNN으로 나눠 **평균 단어 확률**을 정규화합니다.
   * 이를 통해 Perplexity는 문장 길이에 영향을 받지 않고, 모델 성능을 공정하게 평가할 수 있습니다.
2. **역수 형태로 모델의 혼란도를 표현**:
   
   * 확률 P(W)P(W)P(W)가 높으면 Perplexity는 작아지고, 확률 P(W)P(W)P(W)가 낮으면 Perplexity는 커집니다.
   * 이는 Perplexity가 "모델의 예측 성능"을 직관적으로 해석할 수 있게 만듭니다.
3. **정보 이론적 근거**:
   
   * Perplexity는 정보 이론에서 사용되는 엔트로피 HHH와 밀접하게 관련되어 있습니다:H=−1N∑i=1Nlog⁡P(wi)H = -\frac{1}{N} \sum\_{i=1}^N \log P(w\_i)H=−N1​i=1∑N​logP(wi​)Perplexity는 이를 지수 함수로 변환한 값:PP=eHPP = e^HPP=eH

#### **6. Perplexity의 활용**

* Perplexity는 언어 모델의 성능을 측정하는 데 사용됩니다.
* 모델이 특정 문맥에서 단어를 얼마나 정확히 예측하는지 평가하여, 학습된 모델의 품질을 나타냅니다.
* 예를 들어, 번역 모델, 음성 인식 모델 등에서 모델 성능을 정량적으로 비교하는 데 유용합니다.

---

### **BLEU (Bilingual Evaluation Understudy) Score**

![](https://velog.velcdn.com/images/euisuk-chung/post/1be64c56-8b4a-4bf6-92e2-6a82df5ccdc4/image.png)

> Source: <https://www.slideserve.com/cassius/overview-of-bleu>

#### **1. BLEU 스코어란 무엇인가?**

* BLEU(Bilingual Evaluation Understudy) 스코어는 기계 번역에서 생성된 번역문과 **참조 번역문(reference translation)** 간의 **유사도**를 측정하는 자동 평가 지표입니다.
* 번역된 문장의 **정확성(accuracy)**을 평가하며, 인간 번역과 얼마나 유사한지를 수치화합니다.
* BLEU 스코어는 0에서 1 사이의 값으로 계산되며, 일반적으로 **퍼센트(0~100)** 형태로 표현됩니다:
  + BLEU 스코어 = 1 (100%) → 생성된 번역이 참조 번역과 완벽히 일치.
  + BLEU 스코어 = 0 → 생성된 번역이 참조 번역과 완전히 다름.

![](https://velog.velcdn.com/images/euisuk-chung/post/398adbc7-687c-457d-8b43-e15048043c48/image.png)

> Source: <https://www.slideserve.com/cassius/overview-of-bleu>

#### **2. BLEU 스코어의 정의**

BLEU는 다음과 같은 주요 요소를 기반으로 정의됩니다:

BLEU=BP⋅exp⁡(∑n=1Nwn⋅log⁡Pn)BLEU = BP \cdot \exp \left( \sum\_{n=1}^{N} w\_n \cdot \log P\_n \right)BLEU=BP⋅exp(n=1∑N​wn​⋅logPn​)

구성 요소:

* **NNN-그램 Precision (PnP\_nPn​)**: 생성된 번역문과 참조 번역문 간의 **nnn-그램(n-gram)** 유사도를 계산.
* **가중치 (wnw\_nwn​)**: 각 nnn-그램에 대한 중요도를 설정 (일반적으로 동일한 가중치).
* **Brevity Penalty (BP)**: 번역문의 길이가 참조 번역문과 비교해 너무 짧을 때 패널티를 부과.

#### **3. BLEU 계산 과정**

1. **nnn-그램 유사도 계산**:
   
   * nnn-그램은 번역문에서 nnn개의 연속된 단어를 말합니다.
   * BLEU는 111-그램부터 444-그램까지 계산하는 것이 일반적입니다.
   * 생성된 번역문에서 참조 번역문에 일치하는 nnn-그램의 비율을 계산:Pn=생성된 번역문에서 참조 번역문과 일치하는 n-그램 개수생성된 번역문의 n-그램 개수P\_n = \frac{\text{생성된 번역문에서 참조 번역문과 일치하는 $n$-그램 개수}}{\text{생성된 번역문의 $n$-그램 개수}}Pn​=생성된 번역문의 n-그램 개수생성된 번역문에서 참조 번역문과 일치하는 n-그램 개수​
2. **길이 패널티 (Brevity Penalty, BP)**:
   
   BP={1if c>re1−rcif c≤rBP = \begin{cases} 1 & \text{if } c > r \\ e^{1 - \frac{r}{c}} & \text{if } c \leq r \end{cases}BP={1e1−cr​​if c>rif c≤r​
   
   여기서:
   
   * ccc: 생성된 번역문의 길이.
   * rrr: 참조 번역문의 길이.
3. **BLEU 계산**:
   
   BLEU=BP⋅exp⁡(1N∑n=1Nlog⁡Pn)BLEU = BP \cdot \exp \left( \frac{1}{N} \sum\_{n=1}^N \log P\_n \right)BLEU=BP⋅exp(N1​n=1∑N​logPn​)
   
   BLEU는 여러 nnn-그램의 유사도를 종합하여 최종 점수를 계산합니다.

#### **4. BLEU 스코어의 직관적 해석**

* BLEU는 생성된 번역이 참조 번역과 얼마나 유사한지를 수치화합니다.
  + PnP\_nPn​: 각 nnn-그램에 대해 얼마나 일치했는지를 측정.
  + BLEU는 nnn-그램 Precision 값을 종합하여, 번역문의 **정확성**뿐만 아니라 **유창성**을 함께 평가합니다.

#### **5. BLEU 스코어의 한계**

1. **문맥 및 의미 무시**:
   
   * BLEU는 단순히 nnn-그램 유사도를 기반으로 하므로, 문장의 **의미**나 **문맥적 유창성**은 평가하지 못합니다.
2. **다양한 표현의 평가 부족**:
   
   * BLEU는 단일 참조 번역문과의 비교를 기반으로 하므로, **동일한 의미를 가지는 다양한 표현**을 제대로 평가하지 못합니다.
3. **짧은 문장에서 부정확**:
   
   * 길이 패널티가 적용되더라도 짧은 문장에서 BLEU의 평가가 왜곡될 가능성이 있습니다.

#### **6. BLEU의 활용**

* BLEU는 **기계 번역 모델**의 성능을 비교하는 데 널리 사용됩니다.
* **번역 품질 자동 평가**:
  + 인간 평가보다 훨씬 빠르고 효율적으로 번역 품질을 정량화.
* **모델 성능 개선**:
  + BLEU 점수를 기준으로 모델을 최적화하는 데 활용.

#### **7. BLEU와 Perplexity의 비교**

* BLEU는 번역 품질을 평가하는 데 중점을 두며, Perplexity는 언어 모델의 일반적인 예측 성능을 측정합니다.
* 두 지표는 상호 보완적으로 사용되며, 각각 다른 측면에서 모델 성능을 평가합니다.

---

### **요약**

* Perplexity와 BLEU는 모두 언어 모델의 성능을 평가하는 중요한 지표입니다.
  + **Perplexity**는 모델이 단어를 얼마나 잘 예측했는지를 측정하며, 낮을수록 성능이 우수합니다.
  + **BLEU**는 번역문과 참조 번역문의 유사도를 측정하며, 점수가 높을수록 번역 품질이 뛰어납니다.
* 두 지표 모두 각기 다른 관점에서 모델 성능을 평가하며, 보완적으로 사용됩니다.
* Perplexity는 모델의 학습 품질 평가에, BLEU는 번역 모델의 결과물 평가에 적합합니다.
