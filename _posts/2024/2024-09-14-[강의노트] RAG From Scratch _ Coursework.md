---
title: "[강의노트] RAG From Scratch : Coursework"
date: "2024-09-14"
tags:
  - "rag"
  - "강의노트"
year: "2024"
---

# [강의노트] RAG From Scratch : Coursework




![](https://velog.velcdn.com/images/euisuk-chung/post/a2375913-1244-4a82-b3cd-c278e98e252c/image.png)

### 소개

오늘날의 Generative AI는 기본적인 대형 언어 모델(LLM)을 넘어, 정보 활용의 방식을 획기적으로 변화시키고 있습니다.

그 중에서도 **RAG, Retrieval-Augmented Generation**은 외부 데이터 소스를 활용하여 더욱 정교하고 도메인에 특화된 정보를 제공함으로써, AI와의 상호작용 방식을 새롭게 정의하고 있습니다. 이러한 기술의 마스터리는 단순한 지식 습득을 넘어, 실질적인 커리어 향상에 필수적인 요소가 되고 있습니다.

Langchain🐦의 Lance Martin이 제작한 **RAG From Scratch** 비디오 시리즈는 대형 언어 모델(LLM)의 강점과 외부 데이터 소스를 결합한 강력한 접근 방식인 `RAG`에 대해 깊이 있게 다룹니다.

이 시리즈는 RAG의 주요 개념, 강점, 약점, 그리고 실용적인 응용 사례를 자세히 설명하며, 각 비디오에 대한 상세한 요약과 분석을 제공합니다.

* Yotube Playlist : <https://www.youtube.com/playlist?list=PLfaIDFEXuae2LXbO1_PKyVJiQ23ZztA0x>

### 강의 개요

이번 블로그 포스트에서는 이 강의를 통해 LLM을 다루는 데 핵심이 되는 RAG의 주요 개념, 코드, 사용 방법을 정리해보고자 합니다. 강의는 총 14편으로 구성되어 있으며, 각각의 강의 링크와 참고자료(슬라이드)는 링크로 제공됩니다.

| **비디오** | **요약** | **강의 링크** | **슬라이드** |
| --- | --- | --- | --- |
| **Part 1 (개요)** | RAG를 소개하며, 시리즈가 기본 개념부터 고급 기술까지 다룰 것임을 설명합니다. | 📌 [강의](https://www.youtube.com/watch?v=wd7TZ4w1mSw&list=PLfaIDFEXuae2LXbO1_PKyVJiQ23ZztA0x&index=1&pp=iAQB) | 📖 [슬라이드](https://docs.google.com/presentation/d/1C9IaAwHoWcc4RSTqo-pCoN3h0nCgqV2JEYZUJunv_9Q/edit?usp=sharing) |
| **Part 2 (인덱싱)** | 검색의 정확성과 속도에 중요한 인덱싱 과정에 초점을 맞춥니다. | 📌 [강의](https://www.youtube.com/watch?v=bjb_EMsTDKI&list=PLfaIDFEXuae2LXbO1_PKyVJiQ23ZztA0x&index=2&pp=iAQB) | 📖 [슬라이드](https://docs.google.com/presentation/d/1MhsCqZs7wTX6P19TFnA9qRSlxH3u-1-0gWkhBiDG9lQ/edit?usp=sharing) |
| **Part 3 (검색)** | 검색의 정밀성을 위해 인덱스를 사용한 문서 검색을 다룹니다. | 📌 [강의](https://www.youtube.com/watch?v=LxNVgdIz9sU&list=PLfaIDFEXuae2LXbO1_PKyVJiQ23ZztA0x&index=3&pp=iAQB) | 📖 [슬라이드](https://docs.google.com/presentation/d/124I8jlBRCbb0LAUhdmDwbn4nREqxSxZU1RF_eTGXUGc/edit?usp=sharing) |
| **Part 4 (생성)** | LLM을 통한 답변 생성을 위한 RAG 프롬프트 구성을 탐구합니다. | 📌 [강의](https://www.youtube.com/watch?v=JChPi0CRnDY&list=PLfaIDFEXuae2LXbO1_PKyVJiQ23ZztA0x&index=4&pp=iAQB) | 📖 [슬라이드](https://docs.google.com/presentation/d/1eRJwzbdSv71e9Ou9yeqziZrz1UagwX8B1kL4TbL5_Gc/edit?usp=sharing) |
| **Part 5 (다중 쿼리)** | 다양한 문서 검색을 위해 쿼리 재작성 기법을 설명합니다. | 📌 [강의](https://www.youtube.com/watch?v=JChPi0CRnDY&list=PLfaIDFEXuae2LXbO1_PKyVJiQ23ZztA0x&index=5&pp=iAQB) | 📖 [슬라이드](https://docs.google.com/presentation/d/15pWydIszbQG3Ipur9COfTduutTZm6ULdkkyX-MNry8I/edit?usp=sharing) |
| **Part 6 (RAG Fusion)** | 여러 검색 결과를 결합하여 향상된 랭킹을 제공하는 RAG Fusion을 소개합니다. | 📌 [강의](https://www.youtube.com/watch?v=JChPi0CRnDY&list=PLfaIDFEXuae2LXbO1_PKyVJiQ23ZztA0x&index=6&pp=iAQB) | 📖 [슬라이드](https://docs.google.com/presentation/d/1EwykmdVSQqlh6XpGt8APOMYp4q1CZqqeclAx61pUcjI/edit?usp=sharing) |
| **Part 7 (분해)** | 복잡한 질문을 세분화된 하위 질문으로 나누어 상세한 답변을 제공하는 방법을 논의합니다. | 📌 [강의](https://www.youtube.com/watch?v=JChPi0CRnDY&list=PLfaIDFEXuae2LXbO1_PKyVJiQ23ZztA0x&index=7&pp=iAQB) | 📖 [슬라이드](https://docs.google.com/presentation/d/1O97KYrsmYEmhpQ6nkvOVAqQYMJvIaZulGFGmz4cuuVE/edit?usp=sharing) |
| **Part 8 (단계적 후퇴)** | 근본적인 이해를 이끌어내는 추상적 질문을 생성하는 단계적 후퇴 프롬프팅을 탐구합니다. | 📌 [강의](https://www.youtube.com/watch?v=JChPi0CRnDY&list=PLfaIDFEXuae2LXbO1_PKyVJiQ23ZztA0x&index=8&pp=iAQB) | 📖 [슬라이드](https://docs.google.com/presentation/d/1L0MRGVDxYA1eLOR0L_6Ze1l2YV8AhN1QKUtmNA-fJlU/edit?usp=sharing) |
| **Part 9 (HyDE)** | 인덱스 문서와 더 잘 일치하도록 가설적 문서를 생성하는 HyDE 기법을 소개합니다. | 📌 [강의](https://www.youtube.com/watch?v=JChPi0CRnDY&list=PLfaIDFEXuae2LXbO1_PKyVJiQ23ZztA0x&index=9&pp=iAQB) | 📖 [슬라이드](https://docs.google.com/presentation/d/10MmB_QEiS4m00xdyu-92muY-8jC3CdaMpMXbXjzQXsM/edit?usp=sharing) |
| **Part 10 (라우팅)** | 쿼리를 관련 데이터 소스로 유도하기 위한 논리적 및 의미적 쿼리 라우팅을 다룹니다. | 📌 [강의](https://www.youtube.com/watch?v=JChPi0CRnDY&list=PLfaIDFEXuae2LXbO1_PKyVJiQ23ZztA0x&index=10&pp=iAQB) | 📖 [슬라이드](https://docs.google.com/presentation/d/1kC6jFj8C_1ZXDYcFaJ8vhJvCYEwxwsVqk2VVeKKuyx4/edit?usp=sharing) |
| **Part 11 (쿼리 구조화)** | 자연어 쿼리를 구조화된 쿼리로 변환하여 데이터베이스 상호작용을 효율화하는 방법을 다룹니다. | 📌 [강의](https://www.youtube.com/watch?v=JChPi0CRnDY&list=PLfaIDFEXuae2LXbO1_PKyVJiQ23ZztA0x&index=11&pp=iAQB) | 📖 [참고자료](https://blog.langchain.dev/query-construction/) |
| **Part 12 (다중 표현 인덱싱)** | 효율적인 검색을 위해 문서 요약을 인덱싱하면서도 전체 문서와 연결하여 포괄적인 이해를 제공하는 방법을 논의합니다. | 📌 [강의](https://www.youtube.com/watch?v=JChPi0CRnDY&list=PLfaIDFEXuae2LXbO1_PKyVJiQ23ZztA0x&index=12&pp=iAQB) | 📖 [참고자료](https://arxiv.org/pdf/2312.06648.pdf) |
| **Part 13 (RAPTOR)** | 문서 요약과 클러스터링을 통해 고수준 개념을 포착하는 RAPTOR 기법을 소개합니다. | 📌 [강의](https://www.youtube.com/watch?v=JChPi0CRnDY&list=PLfaIDFEXuae2LXbO1_PKyVJiQ23ZztA0x&index=13&pp=iAQB) | 📖 [참고자료](https://arxiv.org/pdf/2401.18059.pdf) |
| **Part 14 (ColBERT)** | RAG 프레임워크 내에서 강화된 토큰 기반 검색을 위한 ColBERT를 탐구합니다. | 📌 [강의](https://www.youtube.com/watch?v=JChPi0CRnDY&list=PLfaIDFEXuae2LXbO1_PKyVJiQ23ZztA0x&index=14&pp=iAQB) | 📖 [참고자료](https://hackernoon.com/how-colbert-helps-developers-overcome-the-limits-of-rag) |

### To be Continued...

RAG From Scratch 비디오 시리즈는 Retrieval Augmented Generation에 대한 포괄적인 탐구를 제공하며, 다양한 기술 및 접근 방식을 다룹니다. 각 비디오는 RAG의 특정 측면에 초점을 맞추며, 각 방법의 강점, 약점 및 실용적인 응용 사례에 대한 귀중한 통찰을 제공합니다.

이 기술들의 비교적 장점과 한계를 이해함으로써, 개발자와 연구자들은 특정 사용 사례에 맞는 RAG 시스템을 설계하고 구현할 때 보다 정보에 입각한 결정을 내릴 수 있습니다. 이 시리즈는 효과적인 RAG 시스템 구축에 있어 신중한 설계, 최적화, 그리고 계산 리소스 고려의 중요성을 강조합니다.

RAG 분야는 계속 진화하고 있으며, 최신 발전과 모범 사례에 대한 지속적인 업데이트가 중요합니다. RAG From Scratch 시리즈는 질문 응답, 콘텐츠 생성, 정보 검색 등 다양한 도메인에서 RAG 기술을 탐구하고 적용하고자 하는 모든 사람들에게 훌륭한 기초 자료가 됩니다.

이 시리즈에서 얻은 통찰을 활용하고 논의된 실용적 응용 사례를 고려함으로써, 조직들은 RAG의 힘을 활용하여 AI 시스템을 강화하고 사용자 경험을 개선하며, 대형 언어 모델과 외부 지식 소스를 결합하여 잠재력을 극대화할 수 있습니다.

