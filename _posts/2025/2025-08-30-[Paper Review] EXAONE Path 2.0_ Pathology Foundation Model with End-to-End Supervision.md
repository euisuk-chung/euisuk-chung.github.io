---
title: "[Paper Review] EXAONE Path 2.0: Pathology Foundation Model with End-to-End Supervision"
date: "2025-08-30"
year: "2025"
---

# [Paper Review] EXAONE Path 2.0: Pathology Foundation Model with End-to-End Supervision

원본 게시글: https://velog.io/@euisuk-chung/Paper-Review-EXAONE-Path-2.0-Pathology-Foundation-Model-with-End-to-End-Supervision

![](https://velog.velcdn.com/images/euisuk-chung/post/874933a3-887a-4e87-9945-f80c83bb4fa2/image.png)

> <https://arxiv.org/abs/2507.06639>

```
PYEON, Myeongjang, et al. EXAONE Path 2.0: Pathology Foundation Model with End-to-End Supervision. arXiv preprint arXiv:2507.06639, 2025.
```

Abstract
--------

디지털 병리학에서 whole-slide images (WSIs)는 gigapixel 규모로 인해 처리가 어려운 경우가 많습니다. 따라서 대부분의 접근법은 self-supervised learning (SSL)을 통해 patch encoder를 훈련시킨 다음, multiple instance learning (MIL) 또는 slide encoder를 통해 patch-level embedding을 집계하여 downstream 작업을 수행합니다. 그러나 patch-level SSL은 mutation status 및 분자 특성과 같은 biomarker 예측에 필수적인 복잡한 도메인 특화 특성을 간과할 수 있습니다. SSL 방법들은 작은 patch-level 영역에서 자연 이미지 도메인을 위해 선택된 기본 augmentation에만 의존하기 때문입니다. 또한 SSL 방법들은 완전 지도학습 접근법보다 데이터 효율성이 떨어지며, 경쟁력 있는 성능을 달성하기 위해 광범위한 계산 자원과 데이터셋이 필요합니다.

이러한 한계를 해결하기 위해, 우리는 직접적인 slide-level 지도학습 하에서 patch-level representation을 학습하는 병리학 foundation model인 EXAONE Path 2.0을 제시합니다. 단 37k개의 WSI만을 훈련에 사용하여, EXAONE Path 2.0은 10개의 biomarker 예측 작업에서 최첨단 평균 성능을 달성하며, 뛰어난 데이터 효율성을 보여줍니다.

**Figure 1**: 매개변수 수와 훈련에 사용된 WSI 수를 기반으로 한 모델 성능 비교. 평균 AUROC는 10개의 biomarker 예측 작업에서 AUROC 점수를 평균하여 얻어집니다. 주목할 점은 EXAONE Path 2.0이 다른 모델들에 비해 적은 매개변수와 적은 WSI를 사용했음에도 불구하고 높은 성능을 달성하여 효율성을 보여준다는 것입니다.

1. Introduction
---------------

디지털 병리학은 AI 기반 의료 애플리케이션의 핵심 도메인으로 부상하였으며, whole-slide images (WSIs)는 gigapixel 규모로 인해 독특한 계산적 과제를 제시합니다. 현재의 접근법들은 일반적으로 2단계 패러다임을 따릅니다: DINO와 DINOv2와 같은 self-supervised learning 방법을 통해 patch-level encoder를 훈련시킨 다음, downstream 예측 작업을 위해 multiple-instance learning (MIL) 또는 slide-level encoder를 사용하여 patch-level embedding을 집계합니다.

이 패러다임은 유망함을 보였지만, 디지털 병리학 분야에서 근본적인 한계를 가지고 있습니다. Self-supervised patch-level pretraining은 mutation status 또는 기타 분자 특성과 같은 biomarker 예측에 필수적인 복잡한 도메인 특화 특성을 포착한다고 보장할 수 없습니다. Self-supervised learning (SSL) 방법들이 작은 patch-level 영역에서 자연 이미지 도메인을 위해 선택된 기본 augmentation에만 의존하기 때문입니다. 또한 이러한 접근법들은 완전 지도학습 방법에 비해 데이터 효율성이 떨어지며, 경쟁력 있는 성능을 달성하기 위해 광범위한 계산 자원과 대규모 데이터셋이 필요합니다.

이러한 한계를 해결하기 위해, 우리는 직접적인 slide-level 지도학습 하에서 patch-level representation을 학습하는 병리학 foundation model인 EXAONE Path 2.0을 소개합니다. 우리의 접근법은 patch encoder 훈련 동안 여러 slide-level label을 통합함으로써 기존 방법들과 근본적으로 다르며, 모델이 임상적으로 관련된 특성을 더 효과적으로 학습할 수 있게 합니다.

우리의 결과는 EXAONE Path 2.0이 경쟁하는 방법들보다 실질적으로 적은 훈련 샘플을 요구하면서도 모든 평가된 작업에서 우수한 평균 성능을 달성함을 보여주며, 계산 병리학에서 중요한 발전을 나타냅니다.

2. Modeling
-----------

### 2.1 Gigapixel 이미지 훈련의 금지적 계산 비용 극복

Gigapixel whole-slide image에 대한 훈련은 메모리 제약과 처리 요구사항으로 인해 상당한 계산적 과제를 제시합니다. 이러한 한계를 해결하기 위해, 우리는 hierarchical architecture 설계, curriculum learning, 그리고 효율적인 메모리 관리 기법의 조합을 사용합니다.

**Architecture 설계**: 우리는 3단계 Hierarchical Image Pyramid Transformer (HIPT) 아키텍처를 채택합니다. 이 hierarchical 설계는 전체 해상도에서 gigapixel 이미지를 직접 처리하는 대신 점진적으로 더 높은 추상화 수준에서 patch를 처리함으로써 계산 복잡성을 줄여 대규모 WSI의 더 효율적인 처리를 가능하게 합니다. 첫 번째 단계 ViT는 개별 patch를 처리하고, 두 번째 단계 ViT는 patch-level 특성을 region-level representation으로 집계하며, 세 번째 단계 ViT는 모든 region-level 특성을 통합하여 전체 slide를 처리합니다.

**Curriculum Learning**: 모든 단계에서 동시에 end-to-end 훈련의 계산 부담을 관리하기 위해, 우리는 점진적 해상도 스케일링을 포함한 2단계 curriculum learning 접근법을 구현합니다. 첫 번째 curriculum 단계에서는 첫 번째 단계 ViT에 256×256 DINO loss를, 두 번째 단계 ViT에 1024×1024 DINO loss를 적용하여 전체 3단계 end-to-end 계산을 요구하지 않고 hierarchical visual representation을 구축합니다. 다음 curriculum 단계에서는 첫 번째 단계 ViT에 256×256 DINO loss를 계속 적용하면서 두 번째 단계 ViT의 경우 4096×4096 region으로 확장하고, slide-level supervised cross-entropy loss를 도입하여 전체 slide를 처리하는 전체 3단계 모델에 gradient를 전파합니다. 이 curriculum 접근법은 모든 훈련 반복에서 최대 해상도로 모든 단계를 처리할 필요를 피함으로써 계산 오버헤드를 크게 줄입니다.

**메모리 관리**: 전체 WSI 처리의 계산 요구를 더욱 관리하기 위해, 우리는 activation checkpointing과 CPU offloading 전략을 사용합니다. 모든 patch embedding을 GPU 메모리에 한 번에 로드하는 대신, supervised loss 계산 중에 필요에 따라 activation을 동적으로 계산하고 전송합니다. 이 접근법은 훈련 효율성을 유지하면서 메모리 요구사항을 크게 줄여 제한된 계산 자원으로 gigapixel 이미지를 처리할 수 있게 합니다.

### 2.2 여러 Biomarker 예측 작업에서 일반화 가능한 Representation 학습

계산 효율성을 유지하면서 다양한 biomarker 예측 작업에 걸쳐 일반화되는 representation을 학습하기 위해, 우리는 downstream 작업 적응을 위한 early exit 전략과 결합된 multi-task learning 프레임워크를 사용합니다.

**Multi-Task Learning 프레임워크**: 우리는 여러 상호 보완적 목표에 걸쳐 공동으로 최적화하는 multi-task learning 접근법을 구현합니다. 우리의 훈련은 세 가지 주요 작업 범주를 포함합니다: (1) 33개 암 유형에 걸친 암 아형 분류, (2) 12개 장기 시스템에 걸친 조직 유형 분류, (3) pan-cancer 및 암 특화 mutation status, microsatellite instability, hormone receptor 아형 분류를 포함한 분자 biomarker 예측. 이 multi-task learning 전략은 이러한 다양한 예측 목표에 대해 공동으로 최적화하여 모델이 생물학적 조직의 다양한 규모에서 근본적인 병리학적 패턴을 포착하는 공유된 representation을 학습하도록 권장합니다. 공동 최적화는 개별 작업에 대한 과적합을 방지하면서 전체 downstream 애플리케이션 스펙트럼에 걸친 일반화를 개선하는 데 도움이 됩니다.

**Downstream 적응을 위한 Early Exit 전략**: 소규모 데이터와 깊은 네트워크 환경에서 과적합을 더욱 완화하기 위해, 우리는 전체 hierarchical 모델보다는 early representation을 활용하는 shallow network 접근법을 채택합니다. 구체적으로, 우리는 downstream 작업 적응을 위해 Clustering-constrained Attention Multiple Instance Learning (CLAM)과 결합된 첫 번째 단계 모델을 활용합니다. 전체 hierarchical network를 fine-tuning하는 대신, 이 early exit 접근법은 첫 번째 단계 모델의 robust한 patch-level 특성을 사용하면서 CLAM이 이러한 특성을 slide-level 예측을 위해 효율적으로 집계합니다. 이 전략은 downstream 작업 적응 중 계산 오버헤드를 크게 줄이면서 제한된 데이터가 있는 병리학 애플리케이션에서 일반적으로 관찰되는 과적합의 함정을 피합니다.

3. Experiments
--------------

### 3.1 Training Data

EXAONE Path 2.0은 37,195개의 Formalin-Fixed, Paraffin-Embedded (FFPE) Hematoxylin and Eosin (H&E) 염색 WSI에서 훈련됩니다. 이러한 WSI는 16개 훈련 작업에 걸쳐 144,450개의 이미지-라벨 쌍을 생성하며, 각 WSI는 암 아형 분류, 조직 분류, biomarker 예측을 포함한 다양한 예측 목표에 해당하는 여러 라벨에 기여합니다.

### 3.2 Baselines

우리는 slide-level 분류에 대한 slide-level 및 patch-level 접근법을 모두 다루기 위해 다양한 foundation model 세트를 baseline으로 선택했습니다. Slide-level 모델의 경우, downstream 작업에 직접 사용할 수 있는 slide-level representation을 생성하는 TITAN, PRISM, CHIEF, Prov-GigaPath를 포함했습니다. 또한 patch-level foundation model baseline으로 EXAONE Path 1.0과 UNI2-h를 포함했습니다. 이러한 모델들이 slide의 국소적 영역에서 작동하지만, 적절한 집계 전략과 결합할 때 그들의 설계와 이전 애플리케이션은 slide-level 예측 작업과 자연스럽게 일치합니다. 우리의 실험에서는 slide-level 예측을 생성하기 위해 patch-level 특성에 CLAM 기반 집계기를 사용했습니다.

### 3.3 Evaluation Protocols

각 모델은 사전 훈련된 foundation model 매개변수를 고정한 채 아키텍처 설계에 따라 slide-level 분류를 위해 fine-tuning되었습니다. Slide-level foundation model의 경우, 고정된 backbone에 의해 생성된 slide-level representation 위에 선형 분류 레이어를 훈련했습니다. Patch-level foundation model의 경우, UNI에서 제안된 접근법을 채택하여 patch-level 특성에 CLAM 집계기를 적용하여 slide-level 예측을 생성했습니다. 우리가 제안한 모델도 마찬가지로 첫 번째 단계 모델에서 추출된 patch-level 특성을 활용하며, 이후 slide-level 추론을 위해 CLAM을 통해 집계됩니다. 각 벤치마크 작업은 사전 정의된 훈련/테스트 분할에서 평가되었으며, 다양한 무작위 시드를 가진 4번의 독립적인 훈련 실행에 대한 평균 성능을 보고합니다.

### 3.4 Slide-Level Benchmarks

모델 성능을 비교하기 위해, 폐선암종, 유방암, 결장직장암, 신장암을 포함한 다양한 암 병변에서 파생된 총 10개의 slide-level 벤치마크 작업을 구성했습니다. 이러한 벤치마크는 개인 데이터셋에서 4개 작업과 공개 데이터셋에서 6개 작업으로 구성되어 작업 다양성과 다양한 데이터 소스 및 기관에서의 모델 일반화를 모두 평가하기 위해 신중하게 선택되었습니다.

#### 3.4.1 개인 데이터셋의 벤치마크

이러한 벤치마크는 한국의 한 종합병원(KOR)과 미국의 두 종합병원(USA1, USA2)과의 협력으로 수집된 내부 데이터셋을 기반으로 합니다. 모든 데이터 사용은 연구 목적으로 해당 기관윤리위원회(IRB)의 승인을 받았습니다. 모든 데이터는 익명화되어 내부 사용만을 위해 잠겨 있으며, 내부 성능 평가를 위해서만 엄격하게 사용되었습니다.

**LUAD-TMB**: 이 작업은 폐선암종 WSI에서 tumor mutation burden (TMB) 상태(high vs. low)를 예측합니다. TMB는 DNA 시퀀싱에서 메가베이스당 mutation 수로 정의되며, high와 low를 구분하기 위해 10의 임계값을 사용합니다. 모델은 KOR-LUAD (low:high = 1063:287)에서 훈련되고, USA1-LUAD (137:117) 데이터셋에서 테스트되었습니다.

**LUAD-EGFR**: 이 작업은 폐선암종에서 EGFR mutation의 존재를 감지합니다. 임상적으로 2차 이상의 mutation은 "mutated"로 라벨링되고, 다른 모든 것은 "wild type"으로 라벨링됩니다. 훈련은 KOR-LUAD (wild:mut = 1145:205)를 사용했으며, USA1-LUAD (242:12)에서 테스트되었습니다.

**LUAD-KRAS**: 이 작업은 EGFR와 동일한 임상 mutation 기준을 사용하여 폐선암종 WSI에서 KRAS mutation을 식별합니다. 훈련은 KOR1-LUAD (wild:mut = 1217:133)를 사용했으며, USA2-LUAD (347:168)에서 테스트되었습니다.

**CRC-MSI**: 이 작업은 결장직장암선종에서 microsatellite instability (MSI) 상태를 분류합니다. 모델은 KOR-CRC (stable:instable = 2630:831)에서 훈련되고 동일한 데이터셋의 별도 부분(658:209)에서 테스트되었습니다.

#### 3.4.2 공개 데이터셋의 벤치마크

이러한 벤치마크는 계산 병리학 연구에서 널리 사용되는 공개 데이터셋인 CPTAC을 사용하여 구성되었습니다.

**BRCA-TP53, PIK3CA**: 이러한 작업은 유방암 WSI에서 TP53 및 PIK3CA mutation 상태를 예측합니다. 두 작업 모두 CPTAC-BRCA 데이터셋을 사용하며, TP53는 train (wild:mut = 53:37), test (14:8)이고 PIK3CA는 train (58:33), test (14:7)입니다.

**RCC-PBRM1, BAP1**: 이러한 작업은 clear cell renal cell carcinoma (CCRCC)에서 PBRM1 및 BAP1 mutation 감지에 중점을 둡니다. 두 벤치마크 모두 CPTAC-CCRCC 데이터셋을 사용하며, PBRM1은 train (wild:mut = 97:96), test (26:26)이고 BAP1은 train (156:39), test (46:4)입니다.

**COAD-KRAS, TP53**: 이러한 작업은 결장선암종에서 KRAS 및 TP53 mutation 상태를 분류합니다. 둘 다 CPTAC-COAD 데이터셋을 사용하며, KRAS는 train (wild:mut = 50:29), test (11:8)이고 TP53은 train (53:27), test (12:6)입니다.

### 3.5 Evaluation Results

Table 1은 10개 slide-level 벤치마크 작업에서 7개 모델의 비교 성능을 제시합니다. 평가된 모든 모델 중에서 EXAONE Path 2.0은 가장 높은 전체 평균 성능을 달성하여 다양한 조직 유형, 기관, 예측 대상에 걸친 robust한 정확도와 일관된 일반화를 모두 보여주었습니다.

폐선암종 관련 작업에서 EXAONE Path 2.0은 EGFR mutation 예측에서 뛰어난 성능을 보였으며, USA1-LUAD 데이터셋에서 가장 높은 정확도(0.853)를 달성했습니다. KRAS mutation 작업에서 모델은 USA2-LUAD 데이터셋에서 최고 성능(0.645)을 기록하여 다른 모든 baseline을 능가했습니다. TMB 분류에서 EXAONE Path 2.0은 EXAONE Path 1.0과 TITAN보다 약간 뒤처지긴 했지만 최고 성능 모델들과 비교 가능한 성능을 보였습니다.

결장직장암 MSI 분류에서 EXAONE Path 2.0은 다른 foundation model들과 동등한 높은 정확도(0.938)를 유지했으며, 테스트 세트에서 안정적인 일반화를 보여주었습니다.

유방암 작업에서 모델은 모든 mutation (TP53, PIK3CA) 벤치마크에서 일관되게 강력한 결과를 생성했습니다. 항상 가장 높은 점수를 달성하지는 않았지만, 제한된 훈련 샘플이 있는 도전적인 분류 시나리오에서도 신뢰할 수 있는 성능을 보여주었습니다.

RCC 벤치마크에서 EXAONE Path 2.0은 BAP1 mutation 작업에서 명확한 우월성을 보였으며 가장 높은 점수(0.807)를 달성했고, PBRM1 벤치마크에서도 경쟁력 있는 성능을 보였습니다.

결장선암종 벤치마크에서 모델은 KRAS 예측에서 거의 최적에 가까운 점수인 0.912와 TP53 mutation 분류에서 0.875를 포함하여 최고 수준의 결과에 도달했습니다.

전반적으로 EXAONE Path 2.0은 최고의 평균 AUROC 점수를 달성했으며 거의 모든 작업에서 상위 3위 안에 머물렀습니다. 이러한 결과는 우리의 통합된 hierarchical 프레임워크와 end-to-end 최적화 전략의 이점을 실증적으로 검증하며, EXAONE Path 2.0이 광범위한 slide-level 병리학 작업을 위한 강력하고 일반화 가능한 foundation model 역할을 할 수 있음을 보여줍니다.

모든 벤치마크에 걸친 전체적인 비교를 제공하기 위해, 우리는 radar 및 bar chart를 사용하여 모델 성능을 시각화했습니다(Figure 3). 차트는 10개 검증 데이터셋에서 각 모델의 AUROC를 보여주며, 성능 일관성의 직관적인 이해를 가능하게 합니다. 보여진 바와 같이, EXAONE Path 2.0은 모든 벤치마크에서 일관되게 강력한 범위를 보여줍니다. 이는 특정 작업에서 성능 저하를 보이는 다른 많은 foundation model들에 비해 우수한 일반화 능력과 견고성을 나타냅니다. EXAONE Path 2.0의 시각적으로 지배적인 프로파일은 그것의 선도적인 평균 성능을 강화하고 범용 slide-level foundation model로서의 적합성을 강조합니다.

4. Conclusion
-------------

우리는 직접적인 slide-level 지도학습 하에서 patch-level representation을 학습하는 병리학 foundation model인 EXAONE Path 2.0을 제시했습니다. 우리의 접근법은 slide-level supervised signal이 모든 hierarchical 단계를 통해 전파되도록 하여 임상적으로 관련된 representation의 end-to-end 학습을 가능하게 합니다.

우리의 방법은 hierarchical architecture 설계, curriculum learning, activation checkpointing과 CPU offloading을 포함한 메모리 관리 기법을 통해 계산적 과제를 해결합니다. 우리는 다양한 biomarker 예측 작업에 걸친 multi-task learning을 사용하고 소규모 데이터 환경에서 과적합을 완화하기 위해 early exit 전략을 사용합니다.

실험 결과는 EXAONE Path 2.0이 훈련에 단 37k WSI만을 사용하여 10개 biomarker 예측 작업에서 경쟁력 있는 평균 성능을 달성하여 기존 foundation model들에 비해 향상된 데이터 효율성을 보여줍니다. 모델은 다양한 암 유형과 예측 대상에서 일관되게 성능을 발휘합니다.

이러한 결과는 직접적인 slide-level 지도학습이 임상적으로 관련된 특성을 효과적으로 학습할 수 있으며, 우리가 제안한 방법들이 gigapixel 이미지 훈련의 계산적 과제를 성공적으로 해결하여 병리학 foundation model을 위한 실용적인 접근법을 제공함을 보여줍니다.