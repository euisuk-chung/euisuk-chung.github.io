---
title: "[OpenAI] Introducing ChatGPT agent"
date: "2025-07-20"
tags:
  - "OpenAI"
  - "agent"
  - "chatGPT"
year: "2025"
---

# [OpenAI] Introducing ChatGPT agent

원본 게시글: https://velog.io/@euisuk-chung/OpenAI-Introducing-ChatGPT-agent

Introducing ChatGPT agent 리뷰
============================

![](https://velog.velcdn.com/images/euisuk-chung/post/3251f185-7a26-4b22-8d56-8e5e369ddd82/image.png)

> Source: <https://youtu.be/1jn_RpbPbEc>

* 관련 블로그 : <https://openai.com/index/introducing-chatgpt-agent/>

![](https://velog.velcdn.com/images/euisuk-chung/post/2d783f5d-c984-4d6f-bc8a-b87a386ba821/image.png)

ChatGPT agent 드디어 떳나?!
----------------------

ChatGPT가 더 이상 단순히 답을 알려주는 도우미에 머무르지 않습니다. **이제는 직접 행동하는 '에이전트(Agent)'가 되었습니다.**

![](https://velog.velcdn.com/images/euisuk-chung/post/f08f3c4c-d04c-41b3-813c-5b7d4987a6bf/image.png)

> 물론 DeepSearch나 CodeX가 있었지만, 이건 그것과는 또 다른 개념이다. - Sam Altman

새롭게 공개된 **ChatGPT Agent**는 사용자의 요청을 이해하고, **웹사이트를 탐색하고, 코드를 실행하며, 슬라이드와 스프레드시트를 작성하고, 필요한 정보를 수집·분석해 결과물로 정리**하는 완전한 작업 흐름을 수행합니다. 단순히 "도와주는" 것을 넘어, **직접 "일을 처리"하는 AI**로 진화한 것입니다.

이 에이전트는 이전에 공개되었던 두 가지 기능—

* **Operator**의 웹 UI 상호작용 능력 (스크롤, 클릭, 입력)
* **Deep Research**의 정보 요약·분석 능력

—을 하나의 통합 시스템으로 결합하고, 여기에 **코드 실행용 터미널, 이미지 생성 도구, 커넥터 API** 등 추가 도구까지 포함한 **가상 컴퓨터 환경**을 제공합니다.

📌 예를 들어, 이제 ChatGPT에게

* “다음 주 고객 미팅을 요약해줘. 최신 뉴스도 반영해서”
* “일본식 아침 식사를 위한 재료를 사고 요리 계획을 짜줘”
* “3개 경쟁사 분석하고 슬라이드로 정리해줘”

라고 말하면, Agent가 알아서 웹을 탐색하고, 로그인 요청이 있으면 takeover를 요청하며, 코드를 실행해 정리하고, **최종 결과물(.pptx, .xlsx 등)**을 손에 쥐여줍니다.

무엇보다 중요한 점은 **사용자가 언제든 개입하고 중단할 수 있다는 점**입니다.

실제 행동을 하기 전에는 항상 허락을 구하며, 진행 중에도 브라우저를 takeover하거나 작업을 취소할 수 있어 **협업하는 느낌의 UX**가 구현되어 있습니다.

이제 ChatGPT는 ‘말뿐인 조언자’를 넘어, ‘실제로 일해주는 동료’가 되었습니다.

아래 내용에서는 데모 영상에서 소개하는 데모 사례를 하나하나 자세하게 파헤쳐 보겠습니다.

---

**가장 먼저! 실행 방법!**

* `Tools(도구)` > `Agent(에이전트)` 메뉴를 클릭해서 실행하실 수 있습니다.
* `/agent`라고 타이핑해서 실행하실 수도 있습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/91ace78a-daea-4d70-a897-fe21921ffebd/image.png)

---

1. 친구 웨딩 참석 시 조언 구하기
--------------------

![](https://velog.velcdn.com/images/euisuk-chung/post/02cc699c-6818-4b00-aca7-a6337e8acaf7/image.png)

### 사용자 요청:

* 옷차림 추천 (미드럭셔리 스타일)
* 드레스 코드 고려
* 결혼식 장소·날씨 고려
* 호텔 추천
* 결혼 선물 제안

### 에이전트의 작업 흐름:

#### ① 입력된 긴 프롬프트 이해

사용자는 복잡한 요구사항을 담은 긴 프롬프트를 복사·붙여넣기로 전달했습니다. Agent는 이 텍스트를 분석한 뒤, **작업에 필요한 정보(결혼식 날짜 등)**가 빠졌다는 점을 인지하고 사용자에게 질문합니다. 이후 자체적으로 웹에서 날짜를 유추하여 문제 해결을 시도합니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/b47c9bc4-e56d-4360-830f-18489886deb2/image.png)

#### ② 텍스트 브라우저 사용: 결혼식 장소 정보 조사

Agent는 **Text Browser**를 통해 빠르게 웹페이지 내용을 스캔하며, **날씨나 장소 특징 등 정적 정보**를 수집합니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/959e71d1-3cf3-4d16-bc61-5145f5b51bb0/image.png)

> ✍️ **Text Browser란?**

* 시각적 렌더링 없이 **HTML 문서를 텍스트 기반으로 빠르게 파싱**
* 일반 브라우저보다 빠르고 가볍게 웹페이지 수십~수백 개 탐색 가능
* 주로 **날씨, 설명, 위치, 요금, 후기 요약 등 정적 정보에 적합**

![](https://velog.velcdn.com/images/euisuk-chung/post/7b0b3284-182a-4c90-b2e5-e32afd06fc25/image.png)

> 💡 이 도구를 통해 Agent는 결혼식 장소의 기후, 인근 지역 특성, 교통편 등을 빠르게 파악합니다.

#### ③ GUI 브라우저로 전환: 옷 추천을 위한 쇼핑 사이트 탐색

* 정보 수집 후, 시각적 요소가 중요한 **패션 추천** 단계로 넘어가면서 **GUI Browser**를 실행합니다.
* 이 단계에서는 실제로 브라우저에서 옷 사진을 보고, 사이트에서 UI 컴포넌트를 클릭하며 탐색을 이어갑니다.

> ✍️ **GUI Browser란?**

* 실제 사람이 쓰는 것과 같은 **시각적 브라우저 환경**
* 마우스 클릭, 드래그, 스크롤, 버튼 입력 등 **UI 상호작용 가능**
* **로그인 폼, 지도, 상품 선택 등 시각 기반 기능 수행 가능**

![](https://velog.velcdn.com/images/euisuk-chung/post/99233971-152b-4f15-a943-5243822a57c3/image.png)

💡 예: Suit 추천 시, Agent는 웹사이트에서 제품 사진을 스크롤하고 비교 후 적절한 옷을 고릅니다.

#### ④ 터미널 사용: 가격 비교 및 정리

필요한 경우 Agent는 **터미널(Terminal)**을 활용해 수집한 데이터를 정리하거나 추가 분석도 수행할 수 있습니다. 데모에서는 주로 후반의 정리 작업에 사용됩니다.

> ✍️ **Terminal (Agent)은?**:

* 실제 코드를 실행 가능한 환경 (예: Python, Bash 등)
* `.csv`, `.xlsx`, `.json` 파일 생성·정리
* 정렬, 요약, 차트 시각화 등 분석 작업 가능

![](https://velog.velcdn.com/images/euisuk-chung/post/cb2b085d-914d-4617-8aa2-59262a820610/image.png)

💡 예: 호텔 옵션의 가격, 거리, 평점을 정리한 `.xlsx` 테이블 생성

#### ⑤ 최종 보고서를 제공

* **날씨 정보**
* **드레스 코드 분석**
* **추천 옷 링크**
* **호텔 제안**
* **신발 옵션**
* **선물 아이디어**

**스크린샷 포함 + 구매 링크까지 정리**된 종합 제안서가 생성되며, 사용자는 이 작업을 Agent에게 **직접 실행 요청**하거나 **수동으로 takeover**하여 결제 등을 진행할 수 있습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/7e2572f3-27ba-4704-ac08-8c0aa5fff829/image.png)

---

2. 업무 자동화: 스티커 주문 + 아트 생성
-------------------------

![](https://velog.velcdn.com/images/euisuk-chung/post/6ff4409c-baec-460f-9268-68793b5cae27/image.png)

### 요청:

* 팀 마스코트 강아지 스티커 디자인 500장 주문
* 특정 사이트 (Sticker Mule)에서 진행

![](https://velog.velcdn.com/images/euisuk-chung/post/6aecf730-24f1-430b-a087-3329fb3a4104/image.png)

### 작업 단계:

#### ① 이미지 생성 API 호출

* Agent는 **내부 이미지 생성 도구**를 활용해 마스코트를 기반으로 한 애니메이션 스타일 아트를 생성합니다.

> 이 기능은 OpenAI의 **ImageGen API (ex. DALL·E)** 를 통해 구동되며, prompt 기반 비주얼 결과물을 생성합니다.

#### ② GUI Browser 사용: 쇼핑몰 탐색

* Sticker Mule 사이트 접속 → 제품 옵션 선택 → 이미지 업로드 → 수량 지정 → 장바구니 추가

![](https://velog.velcdn.com/images/euisuk-chung/post/ff2035fc-62a0-4a3d-9c0d-2149c3b5f94c/image.png)

#### ③ 사용자 Takeover 요청

* Agent는 **결제 정보 입력 직전**, 사용자의 명시적 허가를 받습니다.
* 이는 보안과 프라이버시를 위한 핵심 설계 원칙입니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/e07ad4bf-58d7-4c08-8e78-7fd3f976f14b/image.png)

Agent는 중간에 사용자에게 수량, 디자인 확인을 요청하고, **사용자가 takeover하여 카드 정보 입력** 후 직접 결제할 수 있도록 유도합니다.

---

3. 대화 중 “신발 구매” 요청 → 멀티턴 처리
---------------------------

![](https://velog.velcdn.com/images/euisuk-chung/post/400251bc-1686-4556-bfda-06a6d83fc2bd/image.png)

### 사용자 요청:

* “남성용 검정 구두, 9.5사이즈도 찾아줘”

### 에이전트 반응:

* Agent는 진행 중인 플로우에서 **자연스럽게 대화 흐름을 수용**합니다.
* 기존 trajectory를 유지하면서 **새로운 sub-task를 삽입**합니다.

### 🔄 핵심 기능: Interruptibility + Clarification

Agent는 대화 중에도:

* 기존 작업을 일시 중단
* 새 요청을 분석하여 실행 계획에 추가
* 필요 시 기존 탐색 경로를 재활용해 효율적 대응

이러한 능력은 **멀티스레딩적 사고 방식**으로, 사용자의 비정형적 요구에도 유연하게 대응할 수 있게 합니다.

---

4. 발표 자료 생성 (PPTX)
------------------

### 요청:

* "ChatGPT Agent 벤치마크 스코어를 Google Drive에서 불러와 슬라이드를 만들어줘"

![](https://velog.velcdn.com/images/euisuk-chung/post/69b0858d-87b7-46c6-aee2-3308433f1420/image.png)

### 사용 도구 및 흐름:

1. **Google Drive 연결 (Connector API 사용)**

   * 내부 평가 결과 파일 검색 및 다운로드

![](https://velog.velcdn.com/images/euisuk-chung/post/184c03e8-a657-442b-bc74-9c4d3cb4f1ee/image.png)

2. **코드 실행 (Terminal)**

   * 데이터 파싱 및 시각화 코드 작성

![](https://velog.velcdn.com/images/euisuk-chung/post/731bdffb-7c87-4140-a3dd-4a32002dc519/image.png)

3. **이미지 생성 API 호출**

   * 슬라이드 꾸미기용 이미지 생성

![](https://velog.velcdn.com/images/euisuk-chung/post/908899b7-0eaf-4f11-8d53-fd98c2c5f8c7/image.png)

4. **슬라이드 생성**

   * `.pptx` 형태의 발표 자료 생성 → 다운로드 가능

![](https://velog.velcdn.com/images/euisuk-chung/post/a1c15e4f-144c-4e00-a70f-4ac967f87ef2/image.png)

5. **결과 검토 후 리비전 (Reinforcement Loop)**

   * 처음 만든 슬라이드는 미완성 → 모델이 자체 평가 후 보완 슬라이드 생성

![](https://velog.velcdn.com/images/euisuk-chung/post/45dbcd12-f4b0-4954-a904-5c15d2a554be/image.png)

5. 성능 소개
--------

**결과 및 벤치마크 성능 소개**

![](https://velog.velcdn.com/images/euisuk-chung/post/78cbae39-4bdb-4266-b5ab-f03c3814adc0/image.png)

* **Humanity’s Last Exam**:

  + 전문가 수준의 다양한 문제를 풀 수 있는 능력을 평가하는 벤치마크로,
  + ChatGPT Agent는 **41.6%**의 정확도로 새로운 SOTA 기록을 달성했습니다.
  + 병렬 실행 전략을 활용하면 최대 **44.4%**까지 성능 향상 가능.
* **FrontierMath**:

  + 세계에서 가장 어려운 수학 벤치마크 중 하나로,
  + ChatGPT Agent는 **27.4%**의 정확도를 기록하며 OpenAI 03 대비 **17.1%p** 향상.

![](https://velog.velcdn.com/images/euisuk-chung/post/64af9cf9-4c67-412a-9163-691acfbf6df9/image.png)

* **BrowseComp & WebArena**:
  + 웹 기반 작업과 정보 탐색 능력을 측정하는 벤치마크에서
  + ChatGPT Agent는 각각 **68.9%** / **65.4%**의 높은 정확도를 기록,
  + 기존 deep research 및 operator 기반 시스템을 능가.

![](https://velog.velcdn.com/images/euisuk-chung/post/5cd40eea-20cd-4e01-bd33-f92aa0c50655/image.png)

* **SpreadsheetBench**:

  + 실무 시나리오 기반의 스프레드시트 편집 정확도에서,
  + Excel의 Copilot (20.0%)을 크게 상회하며 **45.5%** 달성.
* **Investment Banking Modeling**:

  + Fortune 500 재무모델링 과제 등 실제 업무 수준의 난이도에서도
  + Agent는 **최대 71.3%** 정확도로 Deep Research 및 기존 모델을 능가.

![](https://velog.velcdn.com/images/euisuk-chung/post/40924600-83ac-4616-93a0-1bddfa5cfd28/image.png)

* **DSBench (Data Science Tasks)**:
  + **Data Analysis**: 인간(64.1%)보다 월등히 높은 **89.9%** 정확도.
  + **Data Modeling**: 인간(65.0%)보다 높은 **85.5%** 성능.

---

6. 여행 계획: MLB 투어 일정표 생성
-----------------------

![](https://velog.velcdn.com/images/euisuk-chung/post/0f1a4ae2-5246-42f2-bf25-e630c81a5768/image.png)

### 요청:

* "30개 MLB 구장을 모두 도는 최적 루트를 계획해줘. Hello Kitty Day 우선"

### Agent 동작 요약:

* 구단 공식 일정 웹사이트 탐색
* 일정 스크래핑
* Hello Kitty Day 추출
* 최적 루트 계산 (날짜 + 위치)
* **지도 시각화** 및 **엑셀 일정표 출력**

![](https://velog.velcdn.com/images/euisuk-chung/post/c1e7d51a-8a81-45ee-b7dc-4d1429243a3f/image.png)

### 도구 활용:

* **Text Browser**로 팀별 경기일정 수집
* **Terminal**로 Hello Kitty Day 필터링 + 경로 최적화
* **Excel 출력** → 일정표 저장

![](https://velog.velcdn.com/images/euisuk-chung/post/9e76b507-7c29-4c9f-844b-f112c8d79df3/image.png)

* **지도 API 호출** (ex. folium, matplotlib) → 경로 시각화

![](https://velog.velcdn.com/images/euisuk-chung/post/1365556d-55a2-48f6-8e1a-56613dd98e62/image.png)

> 실제 인간이 하루 이상 걸릴 계획을 20~30분 만에 마무리

---

🔓 출시 일정 및 이용 가능 여부 (Availability)
---------------------------------

ChatGPT Agent는 현재 단계적으로 배포 중이며, 다음과 같이 제공됩니다:

* **Pro 사용자**: 당일 중 전체 기능 제공 (월 400 메시지)
* **Plus 및 Team 사용자**: 며칠 내로 순차적 배포 예정 (월 40 메시지)
* **Enterprise 및 교육(Education) 사용자**: 향후 몇 주 내 배포 예정
* **유럽 경제 지역(EEA) 및 스위스**: 접근 가능 여부는 아직 준비 중

> ~~아직 나는 왜 AGENT 기능 없음 ㅡㅡ~~

또한, 기존의 Operator 연구 프리뷰 사이트는 몇 주간 더 유지되며 이후 종료됩니다.  
이전의 Deep Research 기능은 Agent의 일부로 통합되었으며,  
보다 정밀하고 느린 분석이 필요한 경우 여전히 composer에서 'deep research'를 선택하여 이용 가능합니다.

⚠️ 한계점 및 향후 계획 (Limitations & Looking Ahead)
--------------------------------------------

ChatGPT Agent는 강력한 기능을 보유하고 있지만, 아직 초기 단계에 있는 만큼 다음과 같은 제한이 존재합니다:

**🔄 슬라이드 생성 기능 (베타)**

* 현재는 슬라이드 생성 기능이 기본적인 포맷 및 스타일 수준에 머물러 있음
* 슬라이드 뷰어와 PowerPoint 내보내기 간 일관성 문제가 간혹 발생
* 향후에는 보다 세련된 슬라이드 아티팩트 생성이 가능하도록 개선 중

**📊 스프레드시트 편집**

* 스프레드시트(.xlsx) 파일을 업로드하여 직접 편집하거나 템플릿으로 활용 가능
* 슬라이드 템플릿 업로드는 아직 미지원

읽어주셔서 감사합니다 :)