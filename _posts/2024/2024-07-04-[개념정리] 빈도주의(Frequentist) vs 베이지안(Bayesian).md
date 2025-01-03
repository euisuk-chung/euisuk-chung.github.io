---
title: "[개념정리] 빈도주의(Frequentist) vs 베이지안(Bayesian)"
date: "2024-07-04"
tags:
  - "개념정리"
  - "통계"
year: "2024"
---

# [개념정리] 빈도주의(Frequentist) vs 베이지안(Bayesian)

원본 게시글: https://velog.io/@euisuk-chung/용어정리-빈도주의Frequentist-VS-베이지안Baysian



Bayesian 확률과 Frequentist 확률
===========================

안녕하세요!🙌 오늘은 통계학의 두 가지 주요 접근법인 `Bayesian 확률`과 `Frequentist 확률`에 대해 자세히 알아보겠습니다. 이 개념들은 머신러닝과 딥러닝에서 중요한 역할을 하므로, 깊이 있는 이해가 필요합니다.

0. 확률 (Probability) 개념
----------------------

확률은 불확실한 사건의 발생 가능성을 수치화한 것입니다. 일상에서 "확률적으로", "확률이 높다" 등의 표현을 자주 사용하지만, 확률을 해석하는 방식에는 크게 두 가지 접근법이 있습니다:

* Frequentist(빈도주의)와 Bayesian(베이지안) 접근법입니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/41c561f7-eab4-4f53-aa12-d10faf0b63da/image.png)

> 예를 들어, "주사위를 던졌을 때 1이 나올 확률은 1/6이다"라는 명제를 우리는 각각 `Frequentist(빈도주의)`와 `Bayesian(베이지안)` 관점에서 다음과 같이 해석해 볼 수 있습니다.

* **Frequentist 해석**: 주사위를 매우 많이 (이론적으로는 무한히) 던지면, 1이 나오는 횟수의 비율이 1/6에 수렴합니다.
* **Bayesian 해석**: 주사위의 공정성에 대한 우리의 믿음을 바탕으로, 다음 던지기에서 1이 나올 것이라고 믿는 정도가 1/6입니다.

이처럼 두 접근법에는 확률을 해석하는 차이가 존재하며, 이는 통계적 추론과 의사결정 과정에도 큰 영향을 미칩니다. 머신러닝과 딥러닝에서는 문제의 특성과 목적에 따라 두 접근법을 적절히 선택하거나 결합하여 사용합니다.

1. Frequentist 확률
-----------------

* `정의`:  
  
  - 사건의 발생 빈도에 기반한 객관적인 확률 해석
* `특징`:  
  
  - 반복 가능한 실험이나 관찰을 통해 확률을 정의  
  
  - 장기적인 상대 빈도를 확률로 간주  
  
  - 객관적이고 데이터 중심적인 접근 방식  
  
  - 고정된 모수(parameter)를 가정
* `Example`: 동전 던지기에서, 동전을 2~3번 던지면 앞면이 나올 확률 0.5이 아닐 수 있더라도, 우리가 앞면이 나올 확률이 0.5이라고 말할 수 있는 것은 "동전을 무한히 많이 던지면, 앞면이 나오는 비율이 0.5에 수렴한다"라는 빈도주의적 관점에서 말하는 것입니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/aba53e07-6645-4f38-aa46-380c9101c677/image.png)  

출처: BBC - Are coin tosses really random?

### 주요 이론

1. **대수의 법칙(Law of Large Numbers)**:
   
   * 표본의 크기가 커질수록 표본 평균이 모집단의 실제 평균에 수렴한다는 이론입니다.
   * 실험을 충분히 많이 반복하면 관찰된 빈도가 실제 확률에 가까워집니다.
   * 수식:  
     
     P(∣Xˉn−μ∣<ε)→1 as n→∞P(|\bar{X}\_n - \mu| < \varepsilon) \to 1 \text{ as } n \to \inftyP(∣Xˉn​−μ∣<ε)→1 as n→∞
   * 여기서 X̄n은 표본 평균, μ는 모집단 평균, ε은 임의의 작은 양수입니다.
2. **중심극한정리(Central Limit Theorem)**:
   
   * 독립적이고 동일한 분포를 가진 확률변수들의 평균은 표본의 크기가 커질수록 정규분포에 가까워집니다.
   * 많은 통계적 추론의 기초가 되며, 정규분포의 가정을 정당화합니다.
   * 수식:  
     
     Xˉn−μσ/n→N(0,1) as n→∞\frac{\bar{X}\_n - \mu}{\sigma/\sqrt{n}} \to N(0,1) \text{ as } n \to \inftyσ/n​Xˉn​−μ​→N(0,1) as n→∞
   * 여기서 σ는 모집단의 표준편차, N(0,1)은 표준정규분포입니다.
3. **최대우도추정(Maximum Likelihood Estimation, MLE)**:
   
   * 관측된 데이터를 가장 잘 설명하는 모수(parameter)를 추정하는 방법입니다.
   * 우도 함수를 최대화하는 모수 값을 찾습니다.
   * 수식:  
     
     θ^MLE=arg⁡max⁡θL(θ∣x)\hat{\theta}{MLE} = \arg\max{\theta} L(\theta|x)θ^MLE=argmaxθL(θ∣x)
   * 여기서 L(θ|x)는 주어진 데이터 x에 대한 θ의 우도 함수입니다.
4. **가설검정(Hypothesis Testing)**:
   
   * 통계적 가설의 타당성을 검증하는 절차입니다.
   * 주요 개념으로는 귀무가설, 대립가설, p-값, 유의수준 등이 있습니다.
   * 예시: t-검정
     + 귀무가설 H0: μ = μ0
     + 대립가설 H1: μ ≠ μ0
     + 검정통계량: t = (X̄ - μ0) / (s/√n)
     + 여기서 s는 표본 표준편차입니다.
5. **신뢰구간(Confidence Interval)**:
   
   * 모수의 참값이 일정한 확률로 포함될 것으로 기대되는 구간입니다.
   * 반복적인 표본 추출에서 신뢰구간이 참값을 포함할 비율을 나타냅니다.
   * 수식:  
     
     (Xˉ−zσ/n,Xˉ+zσ/n)(\bar{X} - z^\sigma/\sqrt{n}, \bar{X} + z^\sigma/\sqrt{n})(Xˉ−zσ/n​,Xˉ+zσ/n​)
   * 여기서 z\*는 원하는 신뢰수준에 해당하는 표준정규분포의 임계값입니다.

* **장점**
  
  + 1. 객관성: 데이터에만 기반하여 추론하므로 주관적 판단의 영향이 적습니다.
  + 2. 계산의 단순성: 많은 경우에 계산이 상대적으로 간단합니다.
  + 3. 대규모 데이터에서의 효율성: 대량의 데이터를 다룰 때 계산적으로 효율적일 수 있습니다.
  + 4. 널리 사용되는 방법론: 많은 통계적 기법과 소프트웨어가 빈도주의 접근법을 기반으로 합니다.
* **단점**
  
  + 1. 사전 정보 활용의 한계: 이전 지식이나 전문가의 의견을 명시적으로 모델에 포함시키기 어렵습니다.
  + 2. 소규모 데이터셋에서의 한계: 데이터가 부족한 경우 신뢰할 만한 추론이 어려울 수 있습니다.
  + 3. 점 추정의 한계: 불확실성을 완전히 표현하기 어려울 수 있습니다.
  + 4. 반복 가능한 실험 가정: 모든 상황이 반복 가능한 실험으로 모델링되기 어려운 경우가 있습니다.

2. Bayesian 확률
--------------

* `정의`:  
  
  - 주관적 믿음의 정도를 나타내는 확률 해석
* `특징`:  
  
  - 사전 지식이나 믿음을 바탕으로 초기 확률(사전 확률) 설정  
  
  - 새로운 증거나 데이터를 통해 확률을 갱신(사후 확률)  
  
  - 주관적이며 지식이나 믿음의 정도를 반영  
  
  - 불확실성을 다루는 데 유용
* `Example`: 동전 던지기에서, 앞면이 나올 확률 0.5라는 것을 베이지안 확률 관점 측면에서 해석하면 이는 "이 동전이 공정하다는 우리의 현재 믿음 상태"를 의미합니다.

### 주요 이론

1. **사전 확률 (Prior Probability)**

* 정의: 데이터를 관찰하기 전의 가설에 대한 초기 확률 추정치
* 표기: P(θ)
* 특징: 기존 지식이나 전문가의 의견을 반영하여 도출함

2. **우도 (Likelihood)**

* 정의: 주어진 모델 파라미터 θ에 대해 관찰된 데이터 D가 발생할 확률
* 표기: P(D|θ)
* 특징:
  + 데이터가 모델을 얼마나 잘 설명하는지를 나타냄
  + 파라미터 θ에 대한 함수로 해석됨
  + 확률 분포가 아닌 우도 함수로 취급됨

3. **사후 확률 (Posterior Probability)**

* 정의: 데이터를 관찰한 후 업데이트된 가설의 확률
* 표기: P(θ|D)
* 특징: 사전 확률과 우도를 결합하여 계산

4. **베이즈 정리(Bayes' Theorem)**:
   * 수식:  
     
     P(θ∣D)=P(D∣θ)⋅P(θ)P(D)P(\theta|D) = \frac{P(D|\theta) \cdot P(\theta)}{P(D)}P(θ∣D)=P(D)P(D∣θ)⋅P(θ)​

* 여기서 각각의 기호는 다음을 의미합니다.:
  
  + P(θ|D)는 사후 확률
  + P(D|θ)는 우도
  + P(θ)는 사전 확률
  + P(D)는 증거(evidence)로, 모든 가능한 θ에 대한 전체 확률
* 예시: `의료 진단`을 예시로 들어보겠습니다.
  
  + A: 환자가 특정 질병을 가지고 있음
  + B: 양성 검사 결과
  + P(A): 질병의 사전 확률 (예: 인구의 1%가 이 질병을 가짐)
  + P(B|A): 질병이 있을 때 양성 결과가 나올 확률 (검사의 민감도)
  + P(B): 전체 인구에서 양성 결과가 나올 확률
* 위 예시처럼 우리는 베이즈 정리를 사용하여 양성 결과가 나왔을 때 실제로 질병이 있을 확률을 계산할 수 있습니다.

5. **베이지안 추론(Bayesian Inference)**:
   * 과정: 사전 분포 → 데이터 관찰 → 우도 계산 → 사후 분포 도출
   * 점 추정 대신 확률 분포로 결과를 표현하여 불확실성을 명시적으로 나타냅니다.

* **장점**
  
  + 1. 사전 지식의 통합: 도메인 전문가의 지식이나 이전 연구 결과를 모델에 명시적으로 포함할 수 있습니다.
  + 2. 불확실성의 자연스러운 표현: 파라미터의 전체 확률 분포를 제공하여 불확실성을 더 잘 표현합니다.
  + 3. 점진적 학습: 새로운 데이터가 도착할 때마다 모델을 자연스럽게 업데이트할 수 있습니다.
  + 4. 소규모 데이터셋에서의 강점: 사전 정보를 활용하여 데이터가 적은 상황에서도 의미 있는 추론이 가능합니다.
* **단점**
  
  + 1. 계산 복잡성: 복잡한 모델의 경우 사후 분포 계산이 어려울 수 있습니다.
  + 2. 사전 분포 선택의 주관성: 부적절한 사전 분포 선택이 결과를 왜곡할 수 있습니다.
  + 3. 해석의 어려움: 비전문가에게 베이지안 결과의 해석이 직관적이지 않을 수 있습니다.

두 접근법의 주요 차이점
-------------

1. **확률 해석**:
   
   * Frequentist: 확률을 장기적인 사건의 빈도로 해석합니다.
   * Bayesian: 확률을 사건 발생에 대한 믿음 또는 주관적 척도로 해석합니다.
2. **모수(Parameter) 취급**:
   
   * Frequentist: 모수를 미지의 고정된 상수로 간주합니다.
   * Bayesian: 모수를 확률적으로 변하는 확률변수로 취급합니다.
3. **사전 정보의 활용**:
   
   * Frequentist: 주로 현재 데이터에만 의존합니다.
   * Bayesian: 사전 정보를 명시적으로 모델에 통합합니다.
4. **불확실성 처리**:
   
   * Frequentist: 주로 점 추정과 신뢰구간을 사용합니다.
   * Bayesian: 모수의 전체 확률 분포를 통해 불확실성을 표현합니다.
5. **계산 복잡성**:
   
   * Frequentist: 일반적으로 계산이 상대적으로 단순합니다.
   * Bayesian: 복잡한 사후 분포 계산이 필요할 수 있어 계산량이 많을 수 있습니다.

**정리**

| 특성 | Bayesian | Frequentist |
| --- | --- | --- |
| 확률 해석 | 사건 발생에 대한 믿음이나 척도 | 장기적으로 일어나는 사건의 빈도 |
| 모수 관점 | 확률변수로 취급 | 고정된 상수로 취급 |
| 사전 정보 | 사전 확률(prior) 사용 | 사용하지 않음 |
| 결과 표현 | 확률 분포 | 점 추정 또는 신뢰구간 |
| 불확실성 처리 | 사후 분포를 통해 자연스럽게 표현 | 별도의 방법 필요 (예: 부트스트래핑) |
| 데이터 요구량 | 적은 데이터로도 추론 가능 | 일반적으로 많은 데이터 필요 |
| 계산 복잡도 | 복잡한 모델에서 계산량 증가 | 상대적으로 단순한 계산 |
| 해석의 직관성 | 직관적 해석 가능 | 때로 해석이 복잡할 수 있음 |
| 과적합 방지 | 사전 분포를 통한 자연스러운 정규화 | 별도의 정규화 기법 필요 |
| 주요 이론/기법 | 베이즈 정리, MCMC, 변분추론 | 최대우도추정, 가설검정, 신뢰구간 |

예시를 통한 비교
---------

1. **동전 던지기 문제**:
   
   * Frequentist 접근: 동전을 100번 던져 앞면이 55번 나왔다면, 앞면이 나올 확률을 55/100 = 0.55로 추정합니다.
   * Bayesian 접근: 동전이 공정하다는 사전 믿음(예: Beta(50,50))을 가지고 시작하여, 100번의 시행 결과를 관찰한 후 사후 분포 Beta(105,95)를 얻습니다. 이를 통해 앞면이 나올 확률의 분포를 추정할 수 있습니다.
2. **의료 진단 문제**:
   
   * Frequentist 접근: 특정 증상이 있는 환자 중 80%가 실제로 질병을 가지고 있다는 데이터를 바탕으로, 새로운 환자가 이 증상을 보일 때 질병 가능성을 0.8로 추정합니다.
   * Bayesian 접근: 질병의 전체 발생률(사전 확률), 증상의 민감도와 특이도를 고려하여 베이즈 정리를 적용합니다. 이를 통해 증상이 있을 때 질병일 확률(사후 확률)을 계산합니다.
3. **A/B 테스팅**:
   
   * Frequentist 접근: 두 버전 간의 차이가 통계적으로 유의한지 p-값을 계산하여 판단합니다.
   * Bayesian 접근: 각 버전의 성공률에 대한 사후 분포를 계산하고, 한 버전이 다른 버전보다 우수할 확률을 직접 추정합니다.
4. **시계열 예측**:
   
   * Frequentist 접근: ARIMA와 같은 모델을 사용하여 과거 데이터에 가장 잘 맞는 단일 모델을 찾습니다.
   * Bayesian 접근: 동적 선형 모델(Dynamic Linear Models)을 사용하여 시간에 따른 파라미터의 변화를 확률 분포로 모델링합니다.

결론
--

Bayesian 접근법과 Frequentist 접근법은 각각 고유한 장단점을 가지고 있으며, 상황에 따라 적절한 방법을 선택하는 것이 중요합니다. 많은 경우, 두 접근법을 보완적으로 사용하는 것이 가장 효과적일 수 있습니다.

* Bayesian 방법은 불확실성을 명시적으로 다루고, 사전 지식을 통합하며, 점진적 학습에 유리합니다. 따라서 데이터가 제한적이거나, 도메인 지식이 중요하거나, 불확실성의 정확한 추정이 필요한 경우에 특히 유용합니다.
* Frequentist 방법은 계산이 간단하고, 대규모 데이터셋에서 효율적이며, 널리 사용되는 많은 통계적 도구와 호환됩니다. 따라서 대량의 데이터가 있거나, 계산 효율성이 중요하거나, 표준화된 보고가 필요한 경우에 적합할 수 있습니다.

머신러닝과 딥러닝 분야에서는 두 접근법의 장점을 결합한 하이브리드 방법론도 점차 발전하고 있습니다. 예를 들어, 확률적 역전파(Stochastic Backpropagation) 등의 기법은 Bayesian 추론의 장점을 유지하면서도 대규모 데이터셋에 적용 가능한 효율성을 제공합니다.

요약하자면! 특정 문제와 상황에 가장 적합한 접근법을 선택하거나 두 접근법을 적절히 조합하는 것이 최선의 결과를 얻는 데 중요합니다. 두 접근법에 대한 깊이 있는 이해는 데이터 과학자와 머신러닝 실무자들에게 더 풍부한 도구 세트를 제공하며, 다양한 상황에서 더 나은 의사결정을 할 수 있게 해줍니다.

