---
title: "[Tips] Lovable 프롬프트 및 통합 전략"
date: "2025-08-18"
tags:
  - "Lovable"
  - "vibe coding"
year: "2025"
---

# [Tips] Lovable 프롬프트 및 통합 전략


Lovable 프롬프트 및 통합: 강력한 내장 통합으로 앱 기능 향상하기
========================================

> 이 글은 Lovable의 공식 문서인 [Prompts & Integrations](https://docs.lovable.dev/prompting/prompt-integrations)을 번역하고 정리한 콘텐츠입니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/ee1145d1-9229-4386-91e8-a1389da331fa/image.png)

> <https://docs.lovable.dev/prompting/prompt-integrations>

개요
--

Lovable은 애플리케이션에 고급 기능을 제공하는 광범위한 내장 통합을 제공합니다. AI 기반 처리, 문서 자동화, 또는 UI 개선이 필요하든 관계없이, Lovable이 모든 것을 제공합니다.

이 가이드는 Lovable에서 사용할 수 있는 다양한 통합 옵션과 각각을 효과적으로 활용하는 방법을 소개합니다. AI 모델부터 비즈니스 도구까지, 각 카테고리별로 실용적인 예시 프롬프트와 함께 설명합니다.

**중요 사항**: 이러한 통합을 Lovable에서 사용하려면 자체 API 키를 설정해야 합니다.

AI 및 LLM (대형 언어 모델)
-------------------

사용자 경험을 향상시키고, 워크플로우를 자동화하며, 콘텐츠를 생성하는 지능형 애플리케이션을 구축하기 위해 최고의 AI 모델을 통합하세요:

### 지원 모델

* **OpenAI 모델** - 요약, 분석, 콘텐츠 생성에 이상적. 빠르고 신뢰할 수 있습니다.
* **Anthropic 최신 모델** - 복잡한 추론과 심층 분석에 뛰어납니다.
* **Google 최신 모델** - 논리적 추론과 긴 컨텍스트 처리에 강합니다.
* **Groq** - Llama 3으로 구동되는 Create에서 가장 빠른 AI 모델.
* **Cohere Command R+** - 비즈니스 애플리케이션을 위해 설계된 확장 가능한 LLM.

### 예시 프롬프트

**일반 AI 기능:**

```
Build a grammar-enhancing writing assistant using [AI model].
```

**한국어 번역:**

```
[AI 모델]을 사용하여 문법을 개선하는 글쓰기 도우미를 구축하세요.
```

**고객 지원:**

```
Create a chatbot that provides customer support using [AI model].
```

**한국어 번역:**

```
[AI 모델]을 사용하여 고객 지원을 제공하는 챗봇을 만드세요.
```

**연구 도우미:**

```
Develop an AI-powered research assistant with [AI model].
```

**한국어 번역:**

```
[AI 모델]로 AI 기반 연구 도우미를 개발하세요.
```

**텍스트 분석:**

```
Build an app that uses [AI model] for text analysis.
```

**한국어 번역:**

```
텍스트 분석을 위해 [AI 모델]을 사용하는 앱을 구축하세요.
```

**콘텐츠 생성:**

```
Create a tool that uses [AI model] for content generation.
```

**한국어 번역:**

```
콘텐츠 생성을 위해 [AI 모델]을 사용하는 도구를 만드세요.
```

**문서 분석:**

```
Build an app that uses [AI model] to analyze long documents.
```

**한국어 번역:**

```
긴 문서를 분석하기 위해 [AI 모델]을 사용하는 앱을 구축하세요.
```

**다단계 추론:**

```
Create a tool that uses [AI model] for multi-step reasoning.
```

**한국어 번역:**

```
다단계 추론을 위해 [AI 모델]을 사용하는 도구를 만드세요.
```

**실시간 분석:**

```
Create a tool that uses [AI model] for real-time analysis.
```

**한국어 번역:**

```
실시간 분석을 위해 [AI 모델]을 사용하는 도구를 만드세요.
```

**빠른 응답:**

```
Build a chatbot that uses [AI model] for quick responses.
```

**한국어 번역:**

```
빠른 응답을 위해 [AI 모델]을 사용하는 챗봇을 구축하세요.
```

**마크다운 렌더링:**

```
Generate blog posts and display them using [Markdown Renderer].
```

**한국어 번역:**

```
블로그 포스트를 생성하고 [Markdown Renderer]를 사용하여 표시하세요.
```

이미지 및 비전
--------

이미지 분석, 개선 및 생성을 위한 최첨단 비전 API를 활용하세요. Lovable은 다음을 지원합니다:

### 지원 서비스

* GPT-4 Vision
* Stable Diffusion
* DALL-E
* Pexels
* Exa

### 예시 프롬프트

**이미지 분석:**

```
Let users upload photos and analyze them using [AI model].
```

**한국어 번역:**

```
사용자가 사진을 업로드하고 [AI 모델]을 사용하여 분석할 수 있게 하세요.
```

**제품 사진 생성:**

```
Generate high-quality product photos with AI enhancements.
```

**한국어 번역:**

```
AI 개선 기능으로 고품질 제품 사진을 생성하세요.
```

**텍스트 추출:**

```
Extract text from images using [AI model].
```

**한국어 번역:**

```
[AI 모델]을 사용하여 이미지에서 텍스트를 추출하세요.
```

**이미지 생성:**

```
Let users describe an image and use [AI model] to create it.
```

**한국어 번역:**

```
사용자가 이미지를 설명하면 [AI 모델]을 사용하여 생성하게 하세요.
```

**로고 생성:**

```
Create a tool that uses [AI model] for logo generation.
```

**한국어 번역:**

```
로고 생성을 위해 [AI 모델]을 사용하는 도구를 만드세요.
```

**스톡 사진 검색:**

```
Find stock photos of specific objects using Pexels.
```

**한국어 번역:**

```
Pexels를 사용하여 특정 객체의 스톡 사진을 찾으세요.
```

**연구 논문 검색:**

```
Retrieve the latest AI research papers with Exa.
```

**한국어 번역:**

```
Exa로 최신 AI 연구 논문을 검색하세요.
```

UI 컴포넌트
-------

접근 가능한 디자인과 재사용 가능한 UI 컴포넌트를 위해 다음을 권장합니다:

### 권장 라이브러리

* **21st.dev**
* **Chakra UI**
* **shadcn/ui**

### 예시 프롬프트

**폼 구성요소:**

```
Add a form using [Chakra UI] components.
```

**한국어 번역:**

```
[Chakra UI] 컴포넌트를 사용하여 폼을 추가하세요.
```

**대시보드:**

```
Build a dashboard with [Chakra UI] layout.
```

**한국어 번역:**

```
[Chakra UI] 레이아웃으로 대시보드를 구축하세요.
```

**반응형 네비게이션:**

```
Create a responsive navbar using [shadcn/ui].
```

**한국어 번역:**

```
[shadcn/ui]를 사용하여 반응형 네비게이션 바를 만드세요.
```

**다이얼로그 컴포넌트:**

```
Use the [shadcn/ui] dialog component for a popup form.
```

**한국어 번역:**

```
팝업 폼을 위해 [shadcn/ui] 다이얼로그 컴포넌트를 사용하세요.
```

**설정 패널:**

```
Develop a settings panel using [shadcn/ui].
```

**한국어 번역:**

```
[shadcn/ui]를 사용하여 설정 패널을 개발하세요.
```

오디오 처리
------

고품질 통합을 위해 Eleven Labs가 최고의 선택입니다.

### 주요 기능

* 음성을 텍스트로 변환
* 자연스러운 음성 생성
* 오디오 파일 개선

### 예시 프롬프트

**음성 전사:**

```
Convert uploaded audio files to text using audio transcription.
```

**한국어 번역:**

```
오디오 전사를 사용하여 업로드된 오디오 파일을 텍스트로 변환하세요.
```

**팟캐스트 전사 도구:**

```
Build a podcast transcription tool.
```

**한국어 번역:**

```
팟캐스트 전사 도구를 구축하세요.
```

**텍스트 음성 변환:**

```
Read content aloud using Text-to-Speech.
```

**한국어 번역:**

```
텍스트 음성 변환을 사용하여 콘텐츠를 소리내어 읽으세요.
```

**오디오북 생성기:**

```
Develop an audiobook creator.
```

**한국어 번역:**

```
오디오북 생성기를 개발하세요.
```

**회의 녹음 전사:**

```
Transcribe and summarize meeting recordings.
```

**한국어 번역:**

```
회의 녹음을 전사하고 요약하세요.
```

지도
--

**Mapbox, Google Maps, Weather API**를 사용하여 다음 기능으로 애플리케이션을 개선하세요:

### 주요 기능

* 위치 정보
* 지도 기능
* 비즈니스 인사이트

### 예시 프롬프트

**매장 위치 표시:**

```
Display store locations on a map with [Mapbox].
```

**한국어 번역:**

```
[Mapbox]로 지도에 매장 위치를 표시하세요.
```

**배송 추적 시스템:**

```
Create a delivery tracking system with real-time updates.
```

**한국어 번역:**

```
실시간 업데이트가 있는 배송 추적 시스템을 만드세요.
```

**부동산 앱:**

```
Build a property listing app using [Google Maps].
```

**한국어 번역:**

```
[Google Maps]를 사용하여 부동산 목록 앱을 구축하세요.
```

**식당 찾기:**

```
Find restaurants using [Google business data].
```

**한국어 번역:**

```
[Google 비즈니스 데이터]를 사용하여 식당을 찾으세요.
```

**주소 자동완성:**

```
Add address auto-completion using [Google Place Autocomplete].
```

**한국어 번역:**

```
[Google Place Autocomplete]을 사용하여 주소 자동완성을 추가하세요.
```

**날씨 업데이트:**

```
Show real-time weather updates using [Weather API].
```

**한국어 번역:**

```
[Weather API]를 사용하여 실시간 날씨 업데이트를 표시하세요.
```

문서
--

다음 기능을 제공합니다:

### 주요 기능

* 프로그래밍 방식으로 PDF 생성 및 다운로드
* PDF에서 텍스트 추출 및 변환
* 스캔된 문서 처리
* 다양한 형식 간 파일 변환
* 링크, 데이터, 비즈니스 애플리케이션을 위한 QR 코드 생성

### 예시 프롬프트

**PDF 폼 생성:**

```
Let users fill out a form and use [PDF Generation] to download it.
```

**한국어 번역:**

```
사용자가 폼을 작성하고 [PDF Generation]을 사용하여 다운로드할 수 있게 하세요.
```

**송장 생성:**

```
Generate invoices as PDFs using [PDF Generation].
```

**한국어 번역:**

```
[PDF Generation]을 사용하여 송장을 PDF로 생성하세요.
```

**이력서 빌더:**

```
Create a resume builder that exports to PDF.
```

**한국어 번역:**

```
PDF로 내보내는 이력서 빌더를 만드세요.
```

**문서 텍스트 추출:**

```
Extract text from scanned documents with [PDF Parser].
```

**한국어 번역:**

```
[PDF Parser]로 스캔된 문서에서 텍스트를 추출하세요.
```

**QR 코드 생성:**

```
Generate QR codes for links and business details.
```

**한국어 번역:**

```
링크와 비즈니스 세부정보를 위한 QR 코드를 생성하세요.
```

미디어 및 엔터테인먼트
------------

다음 기능을 제공합니다:

### 주요 기능

* 미디어 데이터 검색
* 스포츠 통계 추적
* 영화, TV 프로그램, 애니메이션, 도서 검색

### 예시 프롬프트

**영화 추천 시스템:**

```
Build a movie recommendation system using [TMDb].
```

**한국어 번역:**

```
[TMDb]를 사용하여 영화 추천 시스템을 구축하세요.
```

**TV 프로그램 추적:**

```
Track upcoming TV shows with [Movies and TV Series].
```

**한국어 번역:**

```
[Movies and TV Series]로 예정된 TV 프로그램을 추적하세요.
```

**시청 목록 앱:**

```
Make a watchlist app with [Movies and TV Series / TMDb].
```

**한국어 번역:**

```
[Movies and TV Series / TMDb]로 시청 목록 앱을 만드세요.
```

**애니메이션 발견 도구:**

```
Build an anime discovery tool.
```

**한국어 번역:**

```
애니메이션 발견 도구를 구축하세요.
```

**스포츠 예측 앱:**

```
Create a fantasy [Sport] prediction app.
```

**한국어 번역:**

```
판타지 [스포츠] 예측 앱을 만드세요.
```

**도서 발견 앱:**

```
Build a book discovery app with [Book Search].
```

**한국어 번역:**

```
[Book Search]로 도서 발견 앱을 구축하세요.
```

웹 도구
----

다음 기능을 제공합니다:

### 주요 기능

* 모든 웹사이트에서 귀중한 인사이트 추출
* 언어 간 원활한 텍스트 번역
* 실시간 검색 결과 액세스
* 웹에서 쉽게 이미지 발견

### 예시 프롬프트

**검색 결과 스크래핑:**

```
Scrape top search results from [Google Search] using [Web Scraper].
```

**한국어 번역:**

```
[Web Scraper]를 사용하여 [Google Search]에서 상위 검색 결과를 스크래핑하세요.
```

**동적 번역:**

```
Translate text dynamically using [Google Translate].
```

**한국어 번역:**

```
[Google Translate]을 사용하여 텍스트를 동적으로 번역하세요.
```

**언어 학습 앱:**

```
Build a language learning app using [Google Translate].
```

**한국어 번역:**

```
[Google Translate]을 사용하여 언어 학습 앱을 구축하세요.
```

**웹 검색:**

```
Search the web using [Google Search].
```

**한국어 번역:**

```
[Google Search]를 사용하여 웹을 검색하세요.
```

**이미지 검색:**

```
Find images using [Google Image Search].
```

**한국어 번역:**

```
[Google Image Search]를 사용하여 이미지를 찾으세요.
```

비즈니스
----

다음 기능을 원활하게 제공합니다:

### 주요 기능

* 정확한 판매세 계산
* 심층적인 검색어 분석
* 인터랙티브하고 동적인 데이터 시각화
* 실시간 이메일 주소 검증
* 도메인 정보 확인
* 유해하거나 공격적인 콘텐츠 감지
* 채팅 및 알림 기능 통합
* 트랜잭션 이메일 전송
* 내장 자동화로 이메일 캠페인 효율적 관리

### 예시 프롬프트

**판매세 계산:**

```
Calculate order totals with [US Sales Tax Calculator].
```

**한국어 번역:**

```
[US Sales Tax Calculator]로 주문 총액을 계산하세요.
```

**전자상거래 체크아웃:**

```
Build an e-commerce checkout.
```

**한국어 번역:**

```
전자상거래 체크아웃을 구축하세요.
```

**SEO 키워드 분석:**

```
Analyze SEO keywords with [SEO Keyword Research].
```

**한국어 번역:**

```
[SEO Keyword Research]로 SEO 키워드를 분석하세요.
```

**데이터 시각화:**

```
Display sales data in a Charts line graph.
```

**한국어 번역:**

```
Charts 선 그래프로 판매 데이터를 표시하세요.
```

**이메일 검증:**

```
Check email addresses and create an email validation system.
```

**한국어 번역:**

```
이메일 주소를 확인하고 이메일 검증 시스템을 만드세요.
```

**도메인 검사 도구:**

```
Build a domain inspector tool using [Domain Inspector].
```

**한국어 번역:**

```
[Domain Inspector]를 사용하여 도메인 검사 도구를 구축하세요.
```

**안전한 채팅 앱:**

```
Build a safe chat app using [OpenAI Moderation].
```

**한국어 번역:**

```
[OpenAI Moderation]을 사용하여 안전한 채팅 앱을 구축하세요.
```

**주문 확인 이메일:**

```
Send order confirmations with [Resend].
```

**한국어 번역:**

```
[Resend]로 주문 확인 이메일을 보내세요.
```

**뉴스레터 시스템:**

```
Create a newsletter system with [Resend].
```

**한국어 번역:**

```
[Resend]로 뉴스레터 시스템을 만드세요.
```

결론
--

Lovable의 광범위한 통합 옵션은 현대적이고 강력한 애플리케이션을 구축하는 데 필요한 모든 도구를 제공합니다. AI 기반 기능부터 비즈니스 자동화까지, 각 통합은 특정 요구사항을 해결하고 사용자 경험을 향상시키도록 설계되었습니다.

### 통합 활용을 위한 모범 사례

**API 키 관리**: 모든 통합을 사용하기 전에 해당 서비스의 API 키를 안전하게 설정하고 관리하세요.

**점진적 구현**: 한 번에 하나의 통합부터 시작하여 점진적으로 기능을 확장하세요. 이렇게 하면 각 통합을 제대로 이해하고 최적화할 수 있습니다.

**성능 고려**: 특히 AI 모델이나 외부 API를 사용할 때는 응답 시간과 비용을 고려하여 효율적으로 사용하세요.

**오류 처리**: 외부 서비스와의 통합에서는 항상 적절한 오류 처리를 구현하여 사용자 경험을 보호하세요.

### 향후 개발 방향

Lovable의 통합 생태계는 지속적으로 확장되고 있습니다. 새로운 AI 모델, 개선된 API, 그리고 혁신적인 서비스들이 정기적으로 추가되므로, 최신 업데이트를 확인하여 애플리케이션에 최첨단 기능을 통합할 수 있습니다.

이러한 통합들을 효과적으로 활용하면, 단순한 웹 애플리케이션을 넘어서 AI 기반의 지능형 플랫폼을 구축할 수 있습니다. 각 통합의 고유한 강점을 이해하고 프로젝트 요구사항에 맞게 조합하여 사용자에게 뛰어난 가치를 제공하는 애플리케이션을 만들어보세요.