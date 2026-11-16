---
type: "Paper Review"
title: "[Paper Review] Flash ALOHA — 사람 손으로 가르친 속도를 로봇이 따라가는 법"
description: "로봇 팔을 직접 움직여 빠른 시연을 기록하고, 손 영역 마스킹과 행동 구간 평활화로 자율 실행까지 연결한 양팔 조작 시스템을 살펴봅니다."
date: "2026-11-15"
tags:
  - "Paper Review"
  - "Computer Vision"
  - "딥러닝"
  - "머신러닝"
resource: "https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2"
generated:
  by: "process:blog-review"
  at: "2026-11-15T21:53:04+09:00"
sources:
  - id: "flash-aloha-author-pdf-v2"
    resource: "https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2"
    title: "Flash ALOHA: Learning Fast and Precise Manipulation"
    authors:
      - "John Hua Yao"
      - "Qi Wu"
      - "Yihuai Gao"
      - "Chelsea Finn"
      - "Zipeng Fu"
status: "stable"
year: "2026"
analyzed_at: "2026-11-15T21:53:04+09:00"
source_authors:
  - "John Hua Yao"
  - "Qi Wu"
  - "Yihuai Gao"
  - "Chelsea Finn"
  - "Zipeng Fu"
source_document_sha256: "9d1e4d10b133132960128fca5b371b8fd3b89afb4243ebe93b765e9f7832414a"
source_id: "flash-aloha"
source_revision: "flash-aloha-author-pdf-v2"
source_title: "Flash ALOHA: Learning Fast and Precise Manipulation"
source_type: "paper"
source_url: "https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2"
visual_sources:
  - path: "/img/reviews/2026/flash-aloha-review/flash-aloha-pipeline.svg"
    kind: "reviewer-diagram"
    source_url: "https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=4"
    caption: "같은 로봇에서 시연을 기록하고 마스킹을 거쳐 행동을 예측·실행하는 독립 도식입니다. 원문 III–IV절 및 그림 3–5를 바탕으로 작성했습니다."
  - path: "/img/reviews/2026/flash-aloha-review/flash-aloha-chunk-overlap.svg"
    kind: "reviewer-diagram"
    source_url: "https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=5"
    caption: "이전 행동 구간과 새 행동 구간의 겹친 시각을 섞는 독립 도식입니다. 원문 IV절과 그림 5를 바탕으로 작성했습니다."
---

<!-- paper-video:start -->
<div style="position: relative; width: 100%; padding-top: 56.25%; margin-bottom: 1rem;">
  <iframe src="https://www.youtube-nocookie.com/embed/hhYcZS53hXE"
    title="논문 리뷰 영상" loading="lazy" referrerpolicy="strict-origin-when-cross-origin"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowfullscreen style="position: absolute; inset: 0; width: 100%; height: 100%; border: 0;"></iframe>
</div>
<p><a href="https://www.youtube.com/watch?v=hhYcZS53hXE">YouTube에서 영상 보기</a></p>
<!-- paper-video:end -->

## 논문 개요와 전체 구조

한쪽 로봇 팔이 던진 공을 다른 쪽 팔이 받으려면 손을 벌리는 타이밍과 공을 향해 움직이는 속도가 모두 맞아야 합니다. 원격 조작으로 이런 시연을 모으는 사람은 화면 너머에서 로봇을 제어하며, 조작 장치가 제공하는 시야와 감각에 맞춰 움직입니다. Flash ALOHA의 저자들은 **실제로 배포할 로봇 팔의 그리퍼에 손잡이를 달고, 사람이 그 팔을 잡아 움직여** 빠른 시연을 기록합니다. 그러면 빠른 동작의 관절 위치를 로봇 엔코더로 직접 읽을 수 있고, 시연자는 물체에 닿는 감각을 손으로 느낄 수 있습니다. [원문 초록·I절, PDF 1–2쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=1)

직접 시연에는 두 가지 뒤처리가 필요합니다. 카메라에는 작업자의 손과 팔이 보이므로 학습과 자율 실행 모두에서 그 영역의 픽셀을 가립니다. 학습된 정책이 이전 예측을 버리고 다음 행동 구간으로 바꾸는 순간에는 목표 관절 위치가 튈 수 있으므로, 겹치는 구간의 두 예측을 점진적으로 섞습니다. 저자들은 작업별 시연 50개로 따로 학습했고, 컵 분리, 배터리 삽입, 식기 정리, 반바지 접기, 공 던져 받기를 평가했습니다. 표의 성공률은 80–100%입니다. 이 글은 요청 링크의 12쪽 PDF를 내려받아 SHA-256으로 고정한 사본을 바탕으로 합니다. [원문 II–V절](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=3) · [저자 프로젝트와 시연 영상](https://johnyao93.github.io/flash-aloha/)

| 순서 | 원문에서 다루는 질문 |
| --- | --- |
| I Introduction | 빠른 시연 데이터를 모으고 실행할 때 각각 어떤 문제가 생기는가? |
| II Related Work | 모방 학습, 직접 시연, 고속 제어의 기존 방법은 어떤 전제를 두는가? |
| III Hardware Setup & Data Collection | 사람이 실제 양팔 장치를 빠르게 움직이려면 무엇을 바꿔야 하는가? |
| IV Data Processing, Policy Learning & Deployment | 작업자가 보이는 학습 영상과 빈 작업대의 실행 영상을 어떻게 맞추고, 예측 경계에서 명령을 어떻게 잇는가? |
| V Experiments | 마스킹, 평활화, 원격 조작 대비 속도, 초보 조작 실험에서 무엇이 달라지는가? |
| VI Conclusion | 어떤 조작을 보여 주었고 저자들이 명시한 제약은 무엇인가? |
| Appendix I–V | 추종 오차, 시각·관성 추적, 원격 조작 비교군, 경계 점프, ACT 학습을 어떻게 구성했는가? |

## 핵심 기여와 혁신성

**시연 기록에 실제 로봇의 관절을 사용합니다.** 리더 팔을 조작해 별도의 팔을 움직이는 방식에서는 조작자가 느끼는 감각과 작업대의 접촉이 분리될 수 있습니다. 휴대형 도구의 카메라와 IMU로 손끝 경로를 구하는 방식도 빠른 움직임에서는 추정 오차가 커질 수 있습니다. Flash ALOHA는 낮은 마찰의 팔에 손잡이를 달고 중력 보상을 적용해 사람이 가볍게 움직이도록 합니다. 모터 엔코더가 시연 자세를 기록하고, 시연 사이에 같은 로봇으로 기록을 재생해 해당 궤적을 추종할 수 있는지 살펴볼 수도 있습니다. [원문 I절과 Fig. 2](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=2) · [원문 III절](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=4)

**관측의 차이와 행동 경계의 불연속을 별도로 처리합니다.** 마스킹은 두 팔의 관절 자세와 손잡이 기하를 이용해 카메라마다 손이 나타날 영역을 계산합니다. 행동 평활화는 정책을 다시 훈련하지 않고, 실행 중 이전 구간과 새 구간이 겹치는 시각의 목표 관절 위치를 섞습니다. 정밀 작업에서는 집게가 살짝 일찍 벌어지거나 배터리가 스프링에 비스듬히 닿는 순간이 결과를 바꿀 수 있습니다. 저자들은 두 처리의 효과를 각각 빼 보는 비교와, 느린 시연으로 학습한 정책의 실행만 가속하는 비교를 따로 둡니다. [원문 IV절](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=5) · [원문 V절](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=6)

## 기술적 세부사항

![실제 로봇에서 빠른 시연을 기록하고 영상 마스킹, 행동 예측과 실행으로 이어지는 세 단계]({{ '/img/reviews/2026/flash-aloha-review/flash-aloha-pipeline.svg' | relative_url }})

시연부터 자율 실행까지의 흐름입니다. 관절 자세는 영상에서 손 위치를 찾는 데에도 쓰입니다. [원문 III–IV절 및 Fig. 3–5, PDF 4–5쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=4)을 바탕으로 작성한 독립 도식입니다.
{: .caption}

**관측과 행동.** 카메라 세 대는 왼손목, 오른손목, 작업대 위에서 RGB를 수집합니다. 관절 위치와 속도도 시연 중에 기록하지만, 정책에는 관절 위치만 들어갑니다. 양팔과 그리퍼의 상태와 마스킹한 세 영상을 본 ACT(Action Chunking with Transformers) 정책은 미래 50단계의 절대 목표 관절 위치와 그리퍼 명령을 내놓습니다. 한 단계씩 나눠 예측하는 대신 여러 목표를 묶어서 출력하므로, 서로 연결된 동작을 한 번의 추론에서 계획할 수 있습니다. 출력은 저수준 PD 제어기가 실제 관절이 따라갈 목표로 사용합니다. [원문 III–IV절](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=4) · [부록 V](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=12)

**비교와 측정.** 논문은 과제 단계별 성공률, 과제 전체 성공률, 실행 시간을 표로 나눕니다. 약속된 초기 배치의 변화를 넣어 시험하고, 과제마다 50개 시연으로 별도의 정책을 학습했습니다. 시각·관성 추적 실험의 오차는 이 성공률과 별개입니다. 추적 실험에서는 1초 구간별로 최대 말단 속도와 평균 위치 오차를 구하고, 속도 구간별로 오차를 집계합니다. [원문 V절](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=5) · [부록 II](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=10)

## 챕터별 상세 리뷰

### 📖 **Chapter I: Introduction**

일상 작업을 하는 로봇은 물건을 옮길 수 있는 것만으로 충분하지 않습니다. 예를 들어 식사를 차리는 동안 사람이 기다려야 한다면 한 동작에 걸리는 시간도 중요합니다. 저자들은 느린 정책이 만들어지는 경로를 두 가지로 봅니다. 하나는 원격 조작자가 지연, 제한된 감각, 익숙하지 않은 입력 장치 때문에 조심스럽게 움직이고, 그 느린 시연을 정책이 닮아가는 과정입니다. 다른 하나는 빠른 시연을 이미 얻었더라도 로봇의 추종과 연속 예측이 흔들리는 문제입니다. 관절 위치를 매 순간 따라가려면 빠른 움직임에서 토크가 필요하고, 목표 위치만으로는 거의 움직이지 않는 물체를 강하게 누르는 데 필요한 힘을 알기 어렵습니다. 같은 작업대에서도 시연 때는 작업자가 카메라에 보이지만 자율 실행 때는 자리를 비웁니다. [원문 I절, PDF 1–2쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=1)

Fig. 2는 빠른 자유 공간 동작에서 손목에 붙인 시각·관성 추적기의 경로가 엔코더 기반 경로에서 10 cm 넘게 벗어나는 사례를 보여 줍니다. 두 신호를 시각 정렬한 뒤에도 속도가 올라가면서 시각·관성 위치 추정 오차가 늘어났습니다. 저자들은 이 비교를 이유로 시연에 쓰는 로봇 자체에서 관절을 읽는 방식을 택합니다. 이 실험에서 사용한 추적기와 정렬 방식은 부록 II에 설명되며, 현장 수집을 위해 다양한 센서를 쓰는 모든 휴대형 시스템을 비교한 결과로 읽을 필요는 없습니다. [원문 Fig. 2, PDF 2쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=2) · [부록 II, PDF 10쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=10)

### 📖 **Chapter II: Related Work**

**Learning from Demonstrations.** 행동을 배울 때는 시연에서 관측과 로봇 명령을 얼마나 잘 연결할 수 있는지가 중요합니다. 사람 영상은 널리 수집할 수 있지만 사람 손의 형태와 로봇 그리퍼의 차이를 다뤄야 합니다. 키보드나 3D 마우스, 게임패드, 휴대전화는 저비용으로 조작할 수 있지만 여섯 자유도의 말단을 직관적으로 옮기기 어려울 수 있습니다. VR이나 추적 장치는 동작 표현을 더 쉽게 만들지만 접촉 감각과 관절 한계가 손으로 바로 전달되지 않습니다. 리더·팔로워 방식은 로봇 관절에 가까운 입력을 주는 별도 장치를 두고 로봇이 이를 따라가게 합니다. Flash ALOHA에서는 배포에 쓸 팔을 시연자가 직접 안내합니다. [원문 II절, PDF 3쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=3)

**Kinesthetic Teaching.** 운동감각 시연은 사람에게 조작을 맡기고 로봇은 그 움직임을 기록하는 방식입니다. 팔을 손으로 움직일 수 있어야 하고, 링크 무게나 모터 마찰이 크면 빠른 동작이 둔해집니다. 저자들은 낮은 기어비 구동기와 중력 보상으로 조작 부담을 낮추고, 끝부분의 손잡이로 가속·감속과 그리퍼 개폐를 동시에 다룹니다. 마찰 보상과 그리퍼 기어 변경은 관련 연구 설명에서 선택 가능한 보조 방안으로 소개합니다. 물체에 접촉하는 감각은 시연자의 입력에 반영될 수 있으나 독립적인 힘 센서 입력이 수집됐다는 뜻은 아닙니다. [원문 II–III절, PDF 3–4쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=3)

**High-Speed Manipulation.** 공을 치거나 던지고, 변형되는 물체를 빠르게 접는 과제에는 동역학 모델과 궤적 최적화가 쓰여 왔습니다. 저자들은 높은 속도를 목표로 직접 학습하는 강화학습이나, 실행 시간을 조정하기 쉬운 분석적 궤적 표현도 따로 소개합니다. Flash ALOHA의 실험은 빠른 데이터 자체를 확보한 뒤 행동 구간을 출력하는 모방 학습 정책에서 다룹니다. [원문 II절, PDF 3쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=3)

### 📖 **Chapter III: Hardware Setup & Data Collection**

장치는 6자유도 팔 두 개와 각 팔의 평행 그리퍼로 구성됩니다. 실험에는 ARX 또는 HESSIAN 팔을 씁니다. 공 던져 받기에는 높은 관절 속도 한계와 낮은 마찰이 필요해 HESSIAN 장치를 사용합니다. 손으로 팔을 밀었을 때 모터에 연결된 관절이 함께 돌아가는 성질을 역구동 가능성(backdrivability)이라고 합니다. Flash ALOHA의 팔은 유성 기어 구동기를 쓰며, 링크 질량과 현재 관절 위치를 기준으로 100 Hz 토크 제어로 중력을 보상합니다. [원문 III절, PDF 3–4쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=4)

그리퍼 양쪽 턱에는 가위처럼 여닫는 손잡이가 붙습니다. 작은 손잡이는 엄지, 긴 손잡이는 나머지 네 손가락용이며 스트랩으로 손가락을 잡아줍니다. 긴 손잡이를 잡고 팔을 아래나 옆으로 당기고, 팔 아랫부분을 받쳐 위로 가속할 수 있습니다. 시연자는 물체를 실제로 보면서 손잡이로 접촉을 느끼고 소리를 듣습니다. 관측은 작업대 위 카메라 한 대와 양쪽 손목 카메라 두 대가 맡습니다. 표준 조건에서는 360×640 RGB와 관절 위치·속도를 50 Hz로 기록합니다. 공 던져 받기의 두 팔은 Table V가 적은 별도 기록률을 사용합니다. [원문 Fig. 3과 III절, PDF 4쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=4) · [Table V, PDF 12쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=12)


### 📖 **Chapter IV: Data Processing, Policy Learning & Deployment**

**Masking in Image Space.** 수집 영상에 보이는 손을 자율 실행 시점에도 같은 방식으로 가립니다. 두 팔의 순기구학(forward kinematics, FK)은 현재 관절 각도에서 그리퍼의 위치와 방향을 계산합니다. 카메라 보정에서 얻은 두 팔 베이스 사이의 변환과 그리퍼에서 손잡이까지의 고정 변환을 적용하면, 손잡이가 다른 팔의 손목 카메라에 비치는 위치를 계산할 수 있습니다. 각 손목 영상에는 반대쪽 손의 손잡이 주변을 작은 사각형으로 가리고, 위 카메라에서는 두 손과 팔에 해당하는 두 직사각형을 가립니다. 마스크 내부의 RGB값은 0입니다. 자율 실행 중에도 매 프레임 같은 규칙을 적용해 조작 자세가 달라지면 가림 위치도 바뀝니다. [원문 IV절 및 Fig. 4, PDF 4–5쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=4)

세 카메라의 원래 영상은 $`I_{1,t},I_{2,t},I_{3,t}`$, 마스킹된 영상은 $`I'_{1,t},I'_{2,t},I'_{3,t}`$로 표시합니다. $`q_t`$는 시각 $`t`$의 관절 위치이며, $`M`$은 순기구학과 좌표 변환을 적용해 픽셀을 가리는 과정입니다. 아래 식은 모델이 받는 영상이 어떻게 도출되는지 보여 줍니다. 검게 가릴 위치는 학습 모델의 손 분할 없이 기하 계산만으로 정해집니다. [원문 IV절, PDF 5쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=5)

```math
(I'_{1,t}, I'_{2,t}, I'_{3,t})
= M(I_{1,t}, I_{2,t}, I_{3,t}, q_t, \mathrm{FK}).
```

**Policy Learning.** 직접 시연 중에는 로봇이 실제로 도달한 관절 위치를 기록합니다. 정책은 이 기록에서 현재 시점 이후의 $`T`$개 위치를 묶어 학습하고, 자율 실행 중 이를 목표 위치로 예측합니다. 논문은 목표 위치 시퀀스의 조건부 확률을 높이는 형태로 설명합니다. $`\pi`$는 ACT 정책이고, 세 마스킹 영상과 현재 관절 위치가 조건입니다. 학습 때 미래 관절 위치의 정답은 시연에서 가져오며 실행 때 그 정답을 예측값으로 바꿉니다. 저자들은 실행 지연을 반영하기 위해 구간 경계에서 최초 $`n`$개 행동을 건너뛰는 lookahead도 조정합니다. 느린 원격조작 데이터의 속도를 높이려고 구간마다 한 칸씩 건너뛰는 Table III의 비교군과는 다른 처리입니다. [원문 IV절, PDF 5쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=5)

```math
\pi\!\left([q_{t+1},\ldots,q_{t+T}]
  \mid I'_{1,t},I'_{2,t},I'_{3,t},q_t\right).
```

**Test-Time Smoothing.** 정책이 현재 관측을 바탕으로 새 구간을 생성하면, 이전 구간 끝의 목표와 새 구간 첫 목표가 같은 물리적 자세를 지시한다는 보장이 없습니다. Flash ALOHA는 첫 $`T`$개 행동을 끝내기 $`H`$스텝 전에 새 구간을 예측해 두 구간이 잠시 겹치도록 합니다. 겹침이 없는 시각에는 해당 구간의 예측만 쓰고, 겹침에서는 동일한 목표 시각에 해당하는 두 값을 섞습니다. 처음에는 이전 예측의 비중이 크고 겹침 중앙에서는 두 비중이 같으며, 끝으로 갈수록 현재 관측을 반영한 새 예측의 비중이 커집니다. 이 평활화는 배포 후처리로 진행됩니다. [원문 IV절 및 Fig. 5, PDF 5쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=5)

![이전 행동 구간과 새 행동 구간이 겹치는 시간대에서 새 예측의 비중이 커지는 도식]({{ '/img/reviews/2026/flash-aloha-review/flash-aloha-chunk-overlap.svg' | relative_url }})

두 행동 구간의 겹친 시각을 섞습니다. 가로 길이는 시간 관계를 보여 주는 예시입니다. [원문 IV절과 Fig. 5, PDF 5쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=5)을 바탕으로 작성한 독립 도식입니다.
{: .caption}

원문의 표기에서 $`t`$는 첫 예측 시각, $`t'`$는 실제 명령 시각입니다. $`T`$는 전체 구간 길이이고 $`H\lt T`$는 겹침 길이입니다. $`\hat q^{(1)}_{t'+1}`$과 $`\hat q^{(2)}_{t'+1}`$은 동일한 다음 목표 시각에 대한 두 관절 위치 예측입니다. 시그모이드의 입력이 0인 겹침 중앙에서는 가중치 $`w(t')`$가 0.5이며, 양의 시간 척도 $`\sigma`$가 작을수록 비중 전환이 빠릅니다. 혼합한 $`a_{t'}`$를 저수준 제어기의 목표로 보냅니다. 이 식의 연산 대상은 목표 관절 위치 벡터입니다. [원문 IV절의 평활화 식, PDF 5쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=5)

```math
\begin{aligned}
w(t') &= \mathrm{sigmoid}\!\left(
   \frac{t'-(t+T-H)-H/2}{\sigma}\right),\\
a_{t'} &= (1-w(t'))\,\hat q^{(1)}_{t'+1}
          +w(t')\,\hat q^{(2)}_{t'+1}.
\end{aligned}
```

### 📖 **Chapter V: Experiments**

#### A. Tasks

**컵 분리(Unstack Cups).** 왼팔이 겹쳐 놓은 컵 중 아래 컵을 잡고, 오른팔이 위 컵의 가장자리만 잡아 당깁니다. 아래쪽을 너무 세게 고정하면 위 컵을 기울여 잡기 어렵고, 위 컵을 세게 잡으면 두 개가 함께 끌려옵니다. 시작점은 15 cm 테이프를 따라 바꿨으며 시연 길이는 4초입니다. [원문 V-A, PDF 5쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=5) · [Table V, PDF 12쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=12)

**배터리 삽입(Battery Insertion).** 한 팔이 배터리를 집어 리모컨에 비스듬히 놓고 한쪽 끝으로 스프링을 누릅니다. 다른 팔이 위에서 밀어 고정합니다. 리모컨과 배터리의 시작 위치를 테이프를 따라 바꾸었고, 시연은 7초 이내에 수집했습니다. 단계별 결과를 보면 집기와 배치는 성공하더라도 마지막에 눌러 끼우는 과정이 남습니다. [원문 V-A 및 Table I, PDF 5–6쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=6)

**식기 정리(Bus Table).** 한 팔이 쟁반을 가까이 가져오면 양팔이 컵, 그릇, 숟가락, 접시를 번갈아 옮깁니다. 식기가 처음 담긴 용기의 위치를 바꾸며 시연에는 6초를 두었습니다. **반바지 접기(Fold Shorts)**는 펼쳐 놓은 바지 밑단을 위로 덮은 뒤 허리 쪽을 왼쪽에서 오른쪽으로 넘겨 접습니다. 다른 팔은 접히는 선을 만듭니다. 초깃값은 최대 30° 돌렸고 시연 길이는 5초입니다. [원문 V-A, PDF 6쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=6) · [Table V, PDF 12쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=12)

**공 던져 받기(Toss & Catch).** 왼팔이 작은 부드러운 공을 집어 앞쪽 위로 빠르게 던지고, 오른팔이 공이 뜬 위치로 움직여 그리퍼를 닫아 받습니다. 2초 길이의 시연이며, 전체 성공을 보려면 두 팔의 순서와 속도가 함께 맞아야 합니다. [원문 V-A, PDF 6쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=6)

#### B. Comparisons

논문은 마스크의 효과를 확인하기 위해 원본 영상(No Mask)으로 학습한 조건과 사람 손을 분할하고 확산 모델로 배경을 채우는 인페인팅(Inpainting) 조건을 둡니다. 평활화의 효과는 후처리를 끈 No Smooth, 매 시각 새 행동 구간을 예측하고 이전 예측과 지수 가중 평균하는 시간 앙상블(Temporal Ensembling, TE)과 대조합니다. 속도 비교에는 리더 팔로 원격 조작해 수집한 Puppeteering, 실행 제어 주파수를 두 배로 한 Puppet Double Freq, 같은 제어 주파수에서 예측 행동을 하나씩 건너뛰는 Puppet Skip Actions가 있습니다. 각각 어떤 단계의 변경을 평가하는지 구분해야 결과표를 해석할 수 있습니다. [원문 V-B, PDF 6쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=6) · [부록 III](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=10)

#### C. Masking Aligns Data Collection and Deployment

아래 표는 Table I의 **전체 성공률 / 실행 시간**을 옮긴 것입니다. 원문 Table I은 성공률 백분율과 시간만 제시하며 각 칸의 총 평가 시행 수를 별도로 적지 않습니다. 작업별 50개는 학습 시연 수입니다. [원문 Table I, PDF 6쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=6) · [Table V](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=12)

| 마스킹 방식 | 컵 분리 | 배터리 삽입 | 식기 정리 | 반바지 접기 |
| --- | ---: | ---: | ---: | ---: |
| 마스크 없음 | 90% / 4.12초 | 75% / 6.44초 | 100% / 6.97초 | 90% / 6.19초 |
| 인페인팅 | 85% / 3.92초 | 65% / 5.65초 | 100% / 6.57초 | 80% / 6.20초 |
| Flash ALOHA 마스크 | 90% / 3.97초 | 85% / 5.70초 | 100% / 6.81초 | 100% / 5.94초 |

배터리와 반바지의 전체 성공률에서 기하 마스킹은 마스크 없음보다 각각 10%p 높습니다. 컵과 식기 정리에서는 마스크 없음과 같은 전체 성공률을 기록했습니다. Fig. 6에서 마스킹은 양 손목과 위 카메라의 같은 장면에 검은 영역을 남깁니다. 인페인팅은 그 부분을 채우지만 반사되는 작업대에 작업자의 팔 그림자가 남고, 장면 문맥이 부족하면 프레임에 시각적 흔적이 생겼습니다. 저자들은 이러한 흔적을 인페인팅 실험의 성과가 낮아진 가능한 원인으로 봅니다. [원문 V-C 및 Fig. 6, PDF 6–7쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=7)

#### D. Test-Time Smoothing Improves Performance

아래 표는 Table II의 전체 성공률과 시간입니다. Table II도 평가 시행 수를 각 칸에 별도로 제시하지 않습니다. [원문 Table II, PDF 7쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=7)

| 실행 후처리 | 컵 분리 | 배터리 삽입 | 식기 정리 | 반바지 접기 |
| --- | ---: | ---: | ---: | ---: |
| 없음 | 65% / 4.23초 | 75% / 5.29초 | 80% / 6.70초 | 80% / 6.16초 |
| 시간 앙상블 | 35% / 7.75초 | 55% / 10.18초 | 100% / 12.23초 | 90% / 11.60초 |
| 겹침 구간 평활화 | 90% / 3.97초 | 85% / 5.70초 | 100% / 6.81초 | 100% / 5.94초 |

평활화를 끄면 빠른 실행에서 집는 위치나 미는 방향이 부정확해질 수 있습니다. 컵 분리의 집기 성공률은 평활화 여부와 관계없이 100%였으며, 두 컵을 당겨 분리하는 단계는 65%에서 90%가 됐습니다. 배터리 삽입은 전체 성공률이 75%에서 85%로 올랐지만 표의 시간은 5.29초에서 5.70초로 늘었습니다. TE는 식기 정리의 전체 성공률이 100%였으나 12.23초가 걸렸습니다. 저자들은 매 시각 추론하는 처리 비용과, 새로운 방향으로 바꿔야 하는 상황에서도 과거 예측을 평균에 넣는 동작을 TE 결과의 설명으로 제시합니다. 방향 전환 문제는 저자의 가설입니다. [원문 V-D와 Table II, PDF 6–7쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=7)

#### E. Speed Comparisons

연구진은 느린 원격조작 시연으로 훈련한 모델을 더 빨리 실행하면 어떤지 확인했습니다. 두 가지 가속 방법 모두 하나의 행동 구간이 차지하는 시간을 절반으로 줄입니다. 제어 주파수를 높인 조건은 구간 교체 때 관절 목표가 크게 튀는 모습을 보였습니다. 한 칸씩 건너뛴 조건에서는 불연속은 상대적으로 작았지만 배터리를 눌러 끼우는 대신 위에서 흔들리거나 물체를 제대로 잡지 못한 사례가 나타났습니다. 공 던져 받기는 원격조작으로 완료하지 못해 표의 비교 수치가 비어 있습니다. [원문 V-E, PDF 7쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=7) · [Table III, PDF 8쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=8)

| 수집·실행 방식 | 컵 분리 | 배터리 삽입 | 식기 정리 | 공 던져 받기 |
| --- | ---: | ---: | ---: | ---: |
| 원격조작 시연·기본 실행 | 75% / 8.84초 | 55% / 17.87초 | 90% / 16.05초 | 비교값 없음 |
| 원격조작 시연·제어 주파수 두 배 | 65% / 5.47초 | 15% / 12.90초 | 85% / 9.30초 | 비교값 없음 |
| 원격조작 시연·행동 하나씩 건너뛰기 | 50% / 5.58초 | 30% / 10.30초 | 85% / 9.29초 | 비교값 없음 |
| Flash ALOHA | 90% / 3.97초 | 85% / 5.70초 | 100% / 6.81초 | 80% / 1.85초 |

위 표는 Table III의 전체 성공률과 시간을 옮긴 것입니다. Table III의 각 성공률 칸에는 분모가 따로 적혀 있지 않습니다. 이 비교를 바탕으로 구간 경계 점프를 분석한 Fig. 8은 원격조작 계열 조건당 자율 실행 20회, 기본 원격조작의 식기 정리만 19회를 명시합니다. 해당 분모는 Fig. 8의 경계 점프 분석에 적용됩니다. 공 던져 받기의 80%는 성공률입니다. 원문의 서두는 여러 과제의 성과를 80% 초과로 요약하지만, 이 과제의 표 값은 80%로 읽어야 합니다. 반바지 접기 시간은 Fig. 1 소개 그림의 5.91초와 Tables I–II의 5.94초가 다르므로, 앞의 비교표들은 표에 적힌 값을 따랐습니다. [Table III, PDF 8쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=8) · [Fig. 1, PDF 1쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=1) · [Fig. 8, PDF 11쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=11)

#### F. User Study

원격조작 경험이 거의 없는 7명이 두 장치에서 배터리 삽입을 했습니다. 참가자는 각 장치에서 3분간 물체와 팔에 익숙해진 다음 전문가의 시연과 간단한 조작 안내를 받았습니다. 이후 가능한 한 빨리 삽입하도록 10번씩 시간을 쟀습니다. 이는 사람의 시연 조작 시간으로, Table III의 자율 정책 실행 시간과는 다른 지표입니다. Fig. 7의 두 평균 곡선은 10번 모두 직접 시연이 더 빠른 방향이며, 저자들은 비교 조건에 따라 최대 약 3배의 차이를 보고합니다. 그림의 맨손과 숙련 조작 값은 별도 기준선입니다. 저자들은 작업대를 가까이서 보는 시야와 접촉 감각이 차이에 기여했다고 설명합니다. [원문 V-F 및 Fig. 7, PDF 7–8쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=8)

### 📖 **Chapter VI: Conclusion**

저자들은 직접 시연 하드웨어와 시각 처리·동작 경계의 실행 처리를 함께 구성해 빠르고 정밀한 양팔 동작을 배웠다고 정리합니다. 동시에 마스킹이 손 주변의 작업 단서까지 지울 수 있으며, 시각·고유수용감각만 사용해 접촉이 중요한 정교한 조작을 배우기에는 제약이 있다고 밝힙니다. 적응형 마스킹과 촉각 센싱을 향후 방향으로 명시합니다. [원문 VI절, PDF 7쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=7)


### 📖 **Chapter Appendix I: Tracking Error During Policy Rollouts**

Fig. 9는 Fig. 2a의 비교에 자율 실행 중 실제 팔의 말단 추종 오차를 추가합니다. 로봇 자체의 오차는 명령한 위치와 엔코더에서 계산한 도달 위치의 차이입니다. 손목에 붙인 휴대형 추적기의 오차는 추정 위치와 엔코더 기준 위치의 차이입니다. 비교한 속도 구간에서 추적기 쪽 오차가 더 컸고, 속도가 커지면서 그 차이가 두드러졌습니다. 이 두 오차는 명령 실행과 자세 계측이라는 서로 다른 과정에서 생기므로, 추적기 결과만으로 그 장치로 수집한 정책의 과제 성공률을 계산할 수 없습니다. [원문 부록 I, PDF 10쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=10) · [Fig. 9, PDF 11쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=11)

### 📖 **Chapter Appendix II: Visual-Inertial Tracking Experiment**

**Hardware.** 6자유도 Seeed Studio reBot B601-RS의 손목에 iPhUMI 앱을 실행하는 iPhone 15 Pro를 고정합니다. 마지막 링크를 휴대전화 홀더와 속이 빈 그리퍼 손가락으로 바꿨습니다. iPhUMI의 ARKit 기록률은 약 60 Hz입니다. 연구진은 기록을 휴대전화에서 내보내 로봇 데이터와 사후 정렬했습니다. Fig. 10에는 패턴이 있는 식탁보, 밝은 조명, 입체 물체 등 추적에 유리하게 만든 환경도 제시됩니다. 이 장치는 자세 추적 오차를 비교하기 위해 정한 실험 설정입니다. 참고문헌 6번에 소개된 UMI 전체 시스템은 더 넓은 범위의 시연·전송 파이프라인입니다. [원문 부록 II, PDF 10쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=10) · [Fig. 10, PDF 11쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=11)

**Ground truth.** 로봇 관절 엔코더와 순기구학으로 각 샘플의 실제 말단 자세 $`A_i`$를 구합니다. $`X`$는 홀더 CAD에서 가져온 말단에서 휴대전화 카메라로의 변환입니다. $`B_i`$는 ARKit이 추정한 카메라 자세이며, $`Y`$는 ARKit의 월드 좌표를 로봇 베이스로 정렬하는 강체 변환입니다. ARKit의 원점과 진행 방향은 촬영마다 달라지므로 $`Y`$는 각 기록 전체를 사용해 최소제곱으로 맞춥니다. 아래 식으로 추적기에서 계산한 말단 자세 $`\hat{A}_i`$를 $`A_i`$와 비교합니다. [원문 부록 II, PDF 10쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=10)

```math
\hat{A}_i = Y B_i X^{-1}.
```

**Time alignment.** 컴퓨터와 휴대전화는 NTP로 시간을 맞췄습니다. 남는 시간 차이는 두 장치에서 얻은 말단 각속도의 상호상관을 계산해 각 기록에서 정했습니다. 모든 기록에서 최대 상관계수가 0.97 이상이었습니다. 추적 위치는 선형 보간하고 회전은 구면 보간해 로봇 샘플에 대응시켰습니다. 추적 로그가 끊긴 곳은 보간으로 메우지 않고 평가에서 뺐습니다. [원문 부록 II, PDF 10쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=10)

**Trajectories.** 일반 동작, 자유 공간 동작, 빠르게 반복하는 동작, 접촉 동작을 사람이 안내하며 로봇 쪽은 100 Hz로 기록했습니다. 이후 각 관절 기록을 0.25배, 0.5배, 0.75배, 1배 속도로 다시 실행했습니다. 부록이 보고하는 자료 규모는 직접 움직인 기록을 포함해 48개 기록, 1초 구간 1,269개입니다. 말단 속도는 최대 1.2 m/s였습니다. [원문 부록 II, PDF 10쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=10)

**Error metric.** 구간마다 최대 말단 속도와 평균 위치 오차를 뽑았습니다. Fig. 2a와 Fig. 9는 샘플 수가 같은 속도 구간 10개의 평균과 95% 부트스트랩 신뢰구간을 보여 줍니다. 로봇 자체의 재생 추종 오차에는 기록마다 RMS 오차를 최소화하는 일정한 지연 하나를 보정한 뒤 명령 위치와 도달 위치를 비교했습니다. [원문 부록 II, PDF 10쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=10)

**Recording Failures.** 1배 재생에서 iPhUMI가 말단 속도를 7.0 m/s 초과로 검출한 기록은 SLAM 실패로 보고 제외했습니다. 1배 동작에서 실패 없는 기록을 얻으려면 평균 3–4번 시도해야 했고, 저자들은 더 빠른 동작을 이 설정으로 시험하기 어려웠다고 적었습니다. 정상 재생의 최대 말단 속도는 앞서 보고한 1.2 m/s이며, 7.0 m/s는 실패를 판별하는 추적기 기준입니다. [원문 부록 II, PDF 10쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=10)

### 📖 **Chapter Appendix III: Puppeteering Baseline Setup**

**Data collection.** 작업자가 ALOHA 2의 리더 팔을 원격으로 움직이며 비교군 시연을 수집했습니다. 양팔과 그리퍼의 관절 위치 14차원, 위 카메라와 두 손목의 640×480 영상을 50 Hz로 기록했습니다. 컵 분리 12초, 배터리 삽입 20초, 식기 정리 18초로 작업별 50개씩 모았습니다. 앞의 Table III는 학습한 정책의 실제 실행 시간이고, 이 수치는 훈련용 에피소드 길이입니다. [부록 III 및 Table IV, PDF 10쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=10)

**Policy.** 원격조작 비교도 아래 부록 V와 같은 ACT 구조를 사용합니다. 작업마다 별도 모델을 학습하며, 관절 위치와 320×180 크기의 영상 세 장을 입력으로 줍니다. 구간 길이는 50행동으로 50 Hz에서 1초에 해당합니다. 배치 크기는 256, 학습률은 $`2\times10^{-4}`$, 이미지 백본 학습률은 $`10^{-5}`$로 보고됐습니다. Table IV에 적힌 각 모델의 학습은 20만 스텝입니다. [부록 III 및 Table IV, PDF 10쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=10)

**Deployment.** 기본 원격조작 정책은 50 Hz로 실행하고 1초마다 새 구간을 예측합니다. 제어 주파수 두 배 조건은 100 Hz로 각 행동을 실행하며 0.5초마다 구간을 예측합니다. 행동 하나씩 건너뛰기는 50 Hz를 유지하면서 구간 내 행동을 하나 걸러 실행하고, 역시 0.5초마다 새 구간을 예측합니다. 둘 다 반 시간에 같은 구간을 지나지만 제어기에 실제로 전달하는 목표 샘플은 다릅니다. [원문 부록 III, PDF 10쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=10)

### 📖 **Chapter Appendix IV: Chunk Boundary Jumps**

이전 구간 마지막 명령과 새 구간 첫 명령을 빼고, 두 팔의 12개 관절에 대한 유클리드 노름을 구해 경계 점프 크기로 사용합니다. 그리퍼는 이 계산에서 제외합니다. 한 실행 안의 여러 경계 점프를 평균 내고 실패한 실행까지 포함합니다. 비교 기준은 조건당 20회이며 기본 원격조작의 식기 정리만 19회입니다. 본문은 기본 원격조작 대비 주파수 두 배에서 약 3–3.5배, 행동 하나씩 건너뛰기에서 약 1.5–2배의 경계 점프를 보고합니다. 이 값은 명령의 불연속이며 앞 부록의 실제 말단 추종 오차, 또는 과제 완료 성공률과 측정 대상이 다릅니다. [원문 부록 IV 및 Fig. 8, PDF 10–11쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=11)

### 📖 **Chapter Appendix V: Policy Training Details**

직접 시연용 데이터는 작업별 50개입니다. 카메라는 두 손목과 위에서 촬영합니다. 작업별 수집 조건을 Table V에 따라 옮기면 다음과 같습니다. 수집 길이는 학습용 기록의 길이입니다. [원문 부록 V 및 Table V, PDF 11–12쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=12)

| 작업 | 양팔 장치 | 관절 기록률 | 학습 시연 수 | 기록 길이 |
| --- | --- | --- | ---: | ---: |
| 컵 분리 | ARX | 50 Hz | 50 | 4초 |
| 배터리 삽입 | ARX | 50 Hz | 50 | 7초 |
| 식기 정리 | ARX | 50 Hz | 50 | 6초 |
| 반바지 접기 | ARX | 50 Hz | 50 | 5초 |
| 공 던져 받기 | HESSIAN | 던지는 팔 100 Hz, 받는 팔 200 Hz | 50 | 2초 |

영상은 360×640으로 기록하고 정책에 넣기 전에 180×320으로 낮춥니다. 각 변을 95% 남기는 무작위 크롭을 적용한 뒤 입력 크기로 되돌리는 증강을 사용합니다. 모델은 관절 속도나 힘 센서 신호를 입력에 넣지 않으며 절대 관절 위치와 그리퍼 명령을 예측합니다. ACT는 ResNet-18 백본, CVAE 인코더 없이 4층 인코더와 7층 디코더, 주의 헤드 8개, 은닉·피드포워드 차원 512·3200을 사용합니다. 행동 구간은 50스텝입니다. 배치 256, 학습률 $`2\times10^{-4}`$, AdamW 가중치 감쇠 $`10^{-4}`$, 20만 학습 스텝이 보고됐습니다. 시드 0과 단일 GPU(NVIDIA L40S, A40 또는 RTX 4090)를 사용하고 에피소드의 1%를 검증에 두었다고 설명합니다. [원문 부록 V 및 Table VI, PDF 11–12쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=12)

## 실험 결과 심층 분석

**동작을 만드는 병목은 작업마다 다릅니다.** 컵 분리는 위 컵에 처음 닿는 단계 뒤에 분리 여부가 갈립니다. 평활화가 있을 때 전체 성공률이 65%에서 90%로 증가했고, 단계별 표에서는 실제로 차이를 보인 부분이 당겨 분리하는 단계입니다. 식기 정리는 시간 앙상블과 Flash ALOHA가 모두 100%여서, 두 조건의 차이는 12.23초와 6.81초라는 실행 시간에 나타납니다. 배터리 삽입에서는 평활화가 성공률을 높였고, 실행 시간은 약간 길었습니다. 평활화가 직접 조정하는 것은 빠른 정책이 구간을 바꿀 때의 명령입니다. [원문 Table II, PDF 7쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=7)

**속도만 올린 비교는 빠른 시연을 대체하지 못했습니다.** 배터리 삽입에서 기본 원격조작의 55%·17.87초는 주파수 두 배에서 15%·12.90초, 행동 하나씩 건너뛰기에서 30%·10.30초가 됐습니다. 직접 시연 정책은 85%·5.70초였습니다. 직접 시연과 기본 원격조작의 보고 시간을 비교하면 컵 분리 약 55%, 배터리 삽입 약 68%, 식기 정리 약 58%가 줄었습니다. 이는 원격조작 시연과 다른 하드웨어에서 수집하고 실행한 전체 시스템 비교입니다. 마스크나 평활화 하나가 시간 차이 전부를 만들었다고 해석하려면 해당 요소만 바꾼 Table I과 II를 함께 봐야 합니다. [원문 Table I–III, PDF 6–8쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=6)

**성공률 표와 추적 오차 그림의 근거는 다릅니다.** 성공률 표에 유의성 검정이나 신뢰구간은 보고되지 않았습니다. 조건별 백분율 차이는 해당 실험의 관찰값입니다. 95% 부트스트랩 구간이 제시된 것은 시각·관성 추적 및 로봇 추종 오차의 속도별 집계입니다. 그 추적 비교에는 실패 기록을 제외한 절차가 있으며, 저자는 가장 빠른 재생에서 실패 없는 기록을 얻기 더 어려웠다고 명시했습니다. [원문 Table I–III](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=6) · [부록 II, PDF 10쪽](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=10)

## 기술적 함의와 응용

Flash ALOHA는 시연을 빠르게 모으는 방법을 택할 때 **관절 경로를 어디서 읽을지**와 **어떤 카메라를 실행 때도 공유할지**를 함께 생각하게 합니다. 참고문헌 6번의 UMI는 휴대형 그리퍼로 여러 장소에서 시연을 모으는 접근입니다. Flash ALOHA는 배포할 로봇을 손으로 움직이며 엔코더에서 자세를 읽는 접근입니다. 두 작업의 장비 구성이 다르고, Flash ALOHA의 추적 실험은 iPhUMI라는 구체적 설정의 자세 추정 오차를 측정했습니다. 장소를 많이 옮겨야 하는 수집과 빠르게 움직이면서 관절 자세를 안정적으로 기록해야 하는 수집은 각각 다른 장치 조건을 요구합니다. [원문 I–II절 및 부록 II](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=2) · [UMI 논문 리뷰](https://euisuk-chung.github.io/2026/11/15/universal-manipulation-interface-review/)

빠른 자율 실행을 적용할 때에는 행동 구간을 예측할 때마다 관측을 갱신하는 주기와 관절 목표를 내보내는 주기를 함께 살펴야 합니다. 이 연구는 겹침 구간에서 새 예측을 점진적으로 반영해, 이전 경로에서 새로운 경로로 넘어가는 순간을 다뤘습니다. 실험에서 초보 참가자가 같은 배터리 작업을 직접 시연으로 더 빨리 수행했다는 결과는 데이터 수집 인터페이스가 조작 난도를 바꿀 가능성도 보여 줍니다. 논문이 실험에서 사용한 센서 입력은 영상과 관절 상태이며, 저자들은 물체와의 접촉을 다루기 위해 촉각 센서도 검토하겠다고 밝혔습니다. [원문 IV절](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=5) · [V-F와 VI절](https://johnyao93.github.io/static/files/flash-aloha.pdf?v=2#page=7)
