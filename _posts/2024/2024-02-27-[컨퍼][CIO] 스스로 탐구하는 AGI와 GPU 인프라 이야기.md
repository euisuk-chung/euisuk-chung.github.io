---
title: "[컨퍼][CIO] 스스로 탐구하는 AGI와 GPU 인프라 이야기"
date: "2024-02-27"
year: "2024"
---

# [컨퍼][CIO] 스스로 탐구하는 AGI와 GPU 인프라 이야기




본 내용은 CIO SUMMIT 2024에서 발표된 내용을 기반으로 제가 더 조사 및 정리해서 작성한 글입니다. 본 게시글은 발표 내용을 정리한 것이지 특정 회사를 옹호•홍보할 목적이 아님을 밝힙니다. 틀린 내용이 있다면 편하게 댓글 달아주세요!! 🤗

제목
--

스스로 탐구하는 AGI와 GPU 인프라 이야기

발표자
---

효성인포메이션시스템 김형섭 수석 컨설턴트

발표내용
----

![CIO_SUMMIT](https://velog.velcdn.com/images/euisuk-chung/post/cce015d4-5385-4362-b131-f93f713bee4b/image.png)

Source: 효성인포메이션시스템 (www.his21.co.kr)

### 뭐하는 회사지?

효성인포메이션시스템은 1985년에 설립된 전문 기업으로, 고객 비즈니스 환경에 최적화된 ICT 통합 서비스를 제공합니다. 금융, 제조, 공공, 통신 등 국내 전 산업분야와 SI 업체 등 약 1,700여 곳을 고객사로 보유하고 있습니다.

효성인포메이션시스템은 고객의 요구에 맞춰 최적화된 서비스를 제공하며, 고객사의 비즈니스 환경에 맞는 ICT 솔루션을 제공하여 고객의 성공을 돕고 있습니다. 기업의 데이터센터를 이루는 주요 인프라인 스토리지, 서버부터 클라우드, 빅데이터, 인더스트리4.0 등의 혁신적인 기술을 활용한 솔루션과 서비스를 제공하여 고객의 비즈니스 성장을 돕고자 합니다.

### AI기술과 기술 트랜드

인공지능(AI) 기술과 관련 인프라는 빠르게 발전하고 있습니다. 특히 GPT-3의 출시와 같은 획기적인 사건들은 AI 기술의 혁신적인 진보를 상징합니다. 해당 발표에서는 AI 기술과 더불어서 바뀌게 되는 기술 트랜드에 대해서 이야기합니다.

![CIO_SUMMIT](https://velog.velcdn.com/images/euisuk-chung/post/19df86dd-d547-4431-a704-850e6c0d16d1/image.png)

Source: AI기술트랜드, 효성인포메이션시스템

### 스스로 탐구하는 AGI

GPT-4을 기점으로 기술 혁신이 이루어지고 있습니다. GPT-4이전의 LLMs은 생성형 AI기술에 가까운 기술로 확률과 통계로 다양한 답변을 생성해도록 학습 및 파인튜닝됩니다. (수학적 사고)

반면에 GPT-5 이후에 도래하게될 AGI(Artificial General Intelligence)의 경우는 AI가 직접 질문에 대한 탐구와 논리적 접근을 통해 문제를 해결하고자 합니다.

![CIO_SUMMIT](https://velog.velcdn.com/images/euisuk-chung/post/9d1ed444-8099-4f38-bd91-afb94b94e96d/image.png)

Source: 스스로 탐구하는 AGI, 효성인포메이션시스템

> **❓ AGI(인공 일반 지능)이란?**  
> 
> 인공 일반 지능(AGI)은 인간과 유사한 지능과 스스로 학습할 수 있는 능력을 갖춘 소프트웨어를 만들려는 이론적 AI 연구 영역입니다. 이는 소프트웨어가 교육을 받지 않거나, 개발되지 않은 작업을 수행할 수 있도록 하는 것을 목표로 합니다.

> **📝 지금은 AGI에 어느정도의 수준일까?**  
> 
> Morris, Meredith Ringel, et al. "Levels of AGI: Operationalizing Progress on the Path to AGI." (2023), 다음 논문은 다양한 지능의 정도에서 나타나는 AI 연구의 현황을 파악하고, 어떤 모델이 실제 상황에서 다양한 문제에 대응할 수 있는 AGI에 가까운가를 조사하고 이를 아래와 같이 테이블 형태로 정의했습니다.

![CIO_SUMMIT](https://velog.velcdn.com/images/euisuk-chung/post/b88ee60e-62d5-4856-8dfa-ed35beb1fe64/image.png)

Source: Morris, Meredith Ringel, et al. "Levels of AGI: Operationalizing Progress on the Path to AGI." (2023)

위 Matrix는 AGI를 Narrow(특정 도메인에 국한되어 있거나), General(국한되어 있지 않은) 관점으로 분석을 수행하였고, 각 AGI의 단계를 다음과 같이 정의하였습니다:

✅ Level 0 - No AI: 인공지능이 아님  

✅ Level 1 - Emerging AGI: 숙련되지 않은 인간과 동등하거나 약간 더 우수함  

✅ Level 2 - Competent AGI: 인공지능은 숙련된 성인의 50번째 백분위 이상의 기술을 가짐  

✅ Level 3 - Expert AGI: 인공지능은 숙련된 성인의 90번째 백분위 이상의 기술을 가짐  

✅ Level 4 - Virtuoso AGI: 인공지능은 숙련된 성인의 99번째 백분위 이상의 기술을 가짐  

✅ Level 5 - Artificial Super Intelligence ASI: 인공지능은 100%의 인간을 능가함

\*본 논문에서는 현재의 ChatGPT를 General 관점에서 아직 Level1 수준으로 정의하고 있습니다.

### 모델에 고도화에 따른 GPU/데이터 처리의 중요성

LLM의 등장으로 더욱 큰 데이터와 복잡한 AI 모델을 학습하고 서빙하기 위해서는 GPU 시스템 및 데이터 처리의 효율이 중요해졌습니다. 실제로 아래 그림을 보면 GPT-4만 해도 학습을 하는 데 어마어마한 리소스가 사용된 것을 확인할 수 있습니다.

![CIO_SUMMIT](https://velog.velcdn.com/images/euisuk-chung/post/8ba05d3c-82dd-4bf8-91e3-b77a4f4f52be/image.png)

Source: AI 고도화로 인한 연산량 증가, 효성인포메이션시스템

이에 효성인포메이션시스템에서는 아래 3가지 포인트의 중요성을 강조하며 이를 충족시키기 위해서 노력하고 있다고 하며 제공하고 있는 서비스를 소개해주셨습니다.

![CIO_SUMMIT](https://velog.velcdn.com/images/euisuk-chung/post/3b979362-291e-4a5c-801e-856cafb6a5cc/image.png)

Source: GPU 장비 선택의 중요성, 효성인포메이션시스템

아직 제가 미숙하여 장비에 대해서 자세하게 알지 못하여 설명드리지는 못할 것 같습니다😿 허나, LLM의 대두로 GPU자원의 중요성과 최적화는 반드시 필요해진 영역이라고 생각합니다. 최근에는 이러한 무한정 리소스가 필요하다는 문제에서 벗어나기 위해 sLLM이나 LLM distillation 기술들도 많이 나오고 있는데 시간이 난다면 공부 해보고 싶네요 🤣

