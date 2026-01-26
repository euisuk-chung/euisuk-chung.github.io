---
title: "[OpenAI] Introduction to Operator & Agents : Computer-Using Agent"
date: "2025-01-24"
tags:
  - "OpenAI"
  - "chatGPT"
year: "2025"
---

# [OpenAI] Introduction to Operator & Agents : Computer-Using Agent




![](https://velog.velcdn.com/images/euisuk-chung/post/be96d2a5-36ec-4c1d-bf01-6dd969b42294/image.png)

### What is Computer-Using Agent (CUA)?

> 📚 참고 자료 : OpenAI blog
> 
> * Computer-Using Agent (CUA): <https://openai.com/index/computer-using-agent/>
> * Operator : <https://openai.com/index/introducing-operator/>

> Youtube 소개 영상: [Introduction to Operator & Agents](https://youtu.be/CSE77wAdDLg)

**Computer-Using Agent(CUA)**는 OpenAI에서 새롭게 출시한 에이전트로, **사람처럼 컴퓨터를 조작할 수 있는 기능을 제공**합니다.

* CUA는 그래픽 사용자 인터페이스(GUI)를 직접 조작하며, 버튼 클릭, 스크롤, 텍스트 입력 등의 작업을 수행할 수 있습니다.
  + 이러한 접근 방식은 기존의 OS- 또는 웹-특화 API 없이도 다양한 디지털 환경에서 유연하게 작업을 처리할 수 있도록 만들어줍니다.
  + 특히, 이 모델은 GPT-4o의 비전(vision) 기능과 강화학습 기반의 고도화된 추론 능력을 결합하여 강력한 성능을 발휘합니다.

CUA는 **단순한 작업에서부터 복잡한 다단계 작업까지 처리**할 수 있는 범용성을 자랑합니다.

* **기존의 AI 시스템**이 특정한 API에 의존해 한정적인 작업만 수행할 수 있었다면, **CUA**는 인간이 컴퓨터를 다루는 방식 그대로 작업을 수행하며 디지털 세계에서 새로운 가능성을 열어줍니다.
* 이로써 사용자는 단순히 명령만 전달하고, 나머지 작업은 CUA가 효율적으로 처리할 수 있도록 합니다.

특히, **Operator와 함께 제공**됨으로써, "*CUA는 단순한 자동화 도구를 넘어서는 '디지털 조수(digital agent)'로 자리 잡을 것*"이라고 설명합니다.

* Operator는 CUA의 강력한 기능을 사용자가 더욱 편리하게 활용할 수 있도록 돕는 시스템으로, 사용자 친화적인 인터페이스와 다양한 안전 장치를 통해 CUA의 잠재력을 극대화합니다.
* Operator는 사용자가 주어진 작업을 정확하고 신속하게 처리할 수 있도록 지원하며, 실시간으로 상호작용하며 작업의 투명성과 신뢰성을 보장합니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/8496591d-7416-48cf-9fdf-8b5bf313488d/image.png)

> Operator 화면 (출처: <https://operator.chatgpt.com/>)

개인적으로 `Computer-Using Agent (CUA)`와 `Operator`의 정의가 모호한 것 같아서 한번 정리해보았습니다:

* CUA는 Operator의 핵심 기술적 기반이며, GUI 조작을 중심으로 하는 범용 에이전트입니다.
* 반면, Operator는 이를 실용적이고 사용자가 쉽게 접근할 수 있도록 만든 상위 레벨 에이전트로, 사용자 경험에 중점을 둔 서비스입니다.
  + Operator는 CUA의 능력을 통해 디지털 작업을 효율적으로 수행하며, 특히 일상적인 작업을 자동화하고 단순화하는 데 초점을 맞춥니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/89c24d8b-51f5-4e59-bf5e-b619af6173d6/image.png)

각각 `Computer-Using Agent (CUA)`와 `Operator`의 개념을 좀 더 면밀하게 파악해보겠습니다.

> 💻 **Computer-Using Agent (CUA)**
> 
> * **정의**:
>   + **Computer-Using Agent(CUA)**는 "그래픽 사용자 인터페이스(GUI)를 직접 조작할 수 있도록 설계된 AI 에이전트"입니다.
>   + 화면의 픽셀 데이터를 이해하고, 마우스 클릭, 키보드 입력, 스크롤 등 사용자가 화면과 상호작용하는 방식 그대로 작업을 수행합니다.
> * **주요 특징**:
>   + **시각 및 상호작용 능력**: CUA는 화면을 "보고" 이해하며, 이를 바탕으로 작업을 수행합니다.
>   + **강화학습 기반**: 고급 추론 능력과 Chain-of-Thought 방식을 활용하여 복잡한 작업 흐름도 처리할 수 있습니다.
>   + **독립적 작업 수행**: API에 의존하지 않고, 인간처럼 디지털 인터페이스를 다룰 수 있습니다.
> * **사용 범위**:
>   + CUA는 특정 플랫폼에 제한되지 않고, 일반적인 디지털 환경에서 다양하게 활용됩니다.
>   + 예를 들어, 웹 검색, 데이터 입력, 화면 상호작용 등을 통해 인간의 작업을 대체하거나 보완합니다.

> ⚙️ **Operator**
> 
> * **정의**:
>   + Operator는 CUA의 기능을 **사용자 친화적**으로 구현한 OpenAI의 상위 레벨 에이전트입니다.
>   + Operator는 사용자와 직접 상호작용하며, 자연어 명령을 통해 CUA의 작업을 조율하고 결과를 제공합니다.
> * **주요 특징**:
>   + **직관적인 인터페이스**: 사용자는 자연어로 작업을 요청하며, Operator는 이를 해석해 CUA가 실행할 수 있도록 처리합니다.
>   + **안전 및 제어**: 민감한 작업(예: 로그인, 결제)에서는 사용자 개입을 요청해 작업의 신뢰성을 보장합니다.
>   + **개인화 가능**: 특정 웹사이트나 작업에 맞는 맞춤형 지시를 저장해 반복 작업 시 효율성을 높입니다.
>   + **데모 및 확장성**: 사용자 워크플로우를 최적화할 수 있도록 설계되었으며, API를 통해 타 시스템과 통합 가능합니다.
> * **사용 사례**:
>   + Operator는 CUA를 기반으로, 사용자가 필요로 하는 작업을 직관적으로 처리하며, 복잡한 프로세스도 간단한 명령으로 해결합니다.
>   + 예: 호텔 예약, 쇼핑, 데이터 입력, 작업 자동화 등.

**차이점**

| **구분** | **Computer-Using Agent (CUA)** | **Operator** |
| --- | --- | --- |
| **주요 역할** | GUI를 조작하며 작업을 수행하는 AI 시스템 | 사용자와 상호작용하며, CUA의 기능을 활용해 작업을 관리하고 처리 |
| **접근 방식** | 강화학습 기반의 추론 능력을 통해 독립적으로 작업 수행 | 사용자 친화적 인터페이스로 작업 요청을 처리하고 결과를 제공 |
| **사용 범위** | 특정 작업 수행보다는 범용적인 에이전트 프레임워크 제공 | 웹 브라우저 및 GUI 상의 구체적 작업을 실시간으로 처리 |
| **안전 장치** | 내부적인 추론 과정을 통해 작업의 적합성을 판단 | 사용자 개입을 요청하거나, 작업 승인 요청을 통해 민감한 정보 보호 |
| **적용 사례** | 연구 개발 및 API 통합을 통한 고급 에이전트 구현 | 웹 기반 자동화 작업(호텔 예약, 쇼핑 리스트 관리, 공공 서비스 이용 등) |
| **확장성** | API를 통해 다양한 개발자 및 시스템에 통합 가능 | 사용자 맞춤형 설정 및 다중 작업 관리 기능 제공 |

---

### How it works

CUA는 화면의 픽셀 데이터를 이해하고 가상 마우스와 키보드를 사용해 작업을 수행합니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/3befd4ce-3508-4904-8ea8-d40dc6f38927/image.png)

> CUA Diagram (출처: <https://openai.com/index/computer-using-agent/>)

* 사용자가 작업을 요청하면 **CUA**는 다음과 같은 반복적인 루프를 통해 이를 수행합니다:
  
  1. **Perception (지각)**:
     
     + 현재 화면의 스크린샷을 분석하여 컴퓨터 상태를 이해합니다.
     + 이 과정에서 화면에 나타난 텍스트와 이미지를 분석해 현재 상태를 정확히 파악합니다.  
       
       ![](https://velog.velcdn.com/images/euisuk-chung/post/e7f7b850-21eb-4565-8399-005f4aed0545/image.png)
  2. **Reasoning (추론)**:
     
     + Chain-of-Thought 방식을 사용하여 현재와 이전 작업 상태를 고려하며 다음에 수행할 단계를 계획합니다.
     + 이때, 내부적으로 수행 단계를 세분화하여 최적의 해결 방식을 찾아냅니다.  
       
       ![](https://velog.velcdn.com/images/euisuk-chung/post/1a897edc-4c71-48a7-8bd0-5dedcc7329b2/image.png)
  3. **Action (행동)**:
     
     + 마우스 클릭, 스크롤, 텍스트 입력 등의 작업을 실행하며, 필요시 사용자 확인을 요청합니다.  
       
       ![](https://velog.velcdn.com/images/euisuk-chung/post/0ed41b67-d561-4add-b276-991e47adb94e/image.png)
     + 추가적으로 로그인 정보 입력이나 CAPTCHA 확인 같은 민감한 작업에는 사용자의 확인을 받습니다.

CUA는 이러한 과정을 통해 복잡한 문제를 체계적으로 해결하며, Operator는 이러한 CUA의 작동 방식을 직관적으로 활용할 수 있도록 지원합니다:

* 예를 들어, 브라우저 내에서 데이터를 검색하고 입력하거나, 여러 단계를 거쳐 목표를 달성하는 등 다양한 작업 시나리오에서 탁월한 성능을 발휘합니다.
  + 또한, 작업 중 발생하는 오류를 스스로 수정하며 적응적으로 행동합니다.

아래는 Operator에서 몇가지 usage scenario들을 정의해서 sample로 보여주고 있는 것을 확인할 수 있는 그림입니다.  

![](https://velog.velcdn.com/images/euisuk-chung/post/f1ffbc43-8149-45ea-873e-7b4ba501c6b8/image.png)

웹에서 수행할 수 있는 웬만한 기능들은 Operator를 통해 작업을 수행해볼 수 있는 것을 확인할 수 있습니다. (ex. 주문, 예약, 쇼핑 등)

* 사용자는 Operator를 통해 단순히 자연어로 작업을 지시할 수 있으며, CUA는 해당 지시에 따라 필요한 작업을 수행합니다.
* Operator는 작업 진행 상황을 시각적으로 표시하며, 사용자가 필요시 개입하여 작업을 조정할 수 있도록 돕습니다.
  
  + 예를 들어, 사용자는 특정 작업 단계에서 직접 컨트롤을 넘겨받아 작업을 수정하거나, CUA가 제안한 결과를 확인하고 승인을 내릴 수 있습니다.

---

### Agent와 Operator의 개념 확장

Agent는 단순히 주어진 명령을 실행하는 도구를 넘어, 사용자가 목표를 설정하면 해당 목표를 달성하기 위한 모든 세부 단계를 스스로 계획하고 실행하는 AI 시스템을 의미합니다. 이는 인간의 조력을 최소화하면서도 정확성과 효율성을 극대화합니다.

Operator는 이러한 Agent 중에서도 특히 웹 브라우저를 활용한 작업을 전문으로 하며, 사용자가 상호작용하는 그래픽 인터페이스를 직접 다루는 점에서 기존의 AI와 차별화됩니다. 이로 인해 API나 정해진 프로토콜 없이도 대부분의 디지털 환경에서 작업이 가능합니다.

Operator의 주요 특징은 다음과 같습니다:

* **자율성**:
  
  + Operator는 단순히 사용자의 명령을 받아 수행하는 것을 넘어, 작업 중 발생하는 문제를 스스로 해결하거나 대체 방안을 제안합니다.
  + 예를 들어, 사용자가 예약을 요청했으나 원하는 시간이 불가능한 경우, 자동으로 대체 시간을 찾아 제안합니다.
* **유연성**:
  
  + Operator는 특정 웹사이트나 소프트웨어에 한정되지 않고, 모든 브라우저 기반 작업에서 활용 가능하다는 점에서 높은 유연성을 제공합니다.
* **확장 가능성**:
  
  + Operator는 향후 API를 통해 다양한 외부 애플리케이션과 통합될 수 있으며, 개발자가 자신의 워크플로우에 맞게 커스터마이징할 수 있는 환경을 제공합니다.

Agent와 Operator는 사용자의 디지털 경험을 한층 더 향상시키기 위한 도구로 설계되었습니다.

* Operator는 단순한 자동화를 넘어 디지털 생태계에 새로운 형태의 상호작용 방식을 도입합니다.
* 고객 지원, 전자상거래, 공공 서비스 등 다양한 분야에서 Operator는 인간의 조력자로서 시간과 자원을 절약합니다.
* 또한, 공공기관과 기업이 시민 참여와 고객 경험을 개선하는 데 기여할 수 있습니다.

---

### Operator의 활용 사례 (Demo)

![](https://velog.velcdn.com/images/euisuk-chung/post/c55d9de2-df4b-49c2-ab3e-d01abf754727/image.png)

Operator는 실제 활용 사례를 통해 다양한 작업에서 AI의 효율성과 정확성을 입증했습니다.

> 참고 영상 링크:
> 
> * [Using saved prompts in Operator](https://youtu.be/m0Cjiq8P6iU)
> * [Demonstrating Operator](https://youtu.be/gYqs-wUKZsM)

아래는 데모 영상에서 소개된 주요 사례들입니다:

1. **Custom Instructions 활용**
   
   * 사용자는 특정 웹사이트에 대한 맞춤형 설정을 추가할 수 있습니다.
     + 예를 들어, Priceline에서 여행 예약 시 "환불 가능한 요금"과 "조식 포함" 옵션을 선호하도록 설정할 수 있습니다.
   * 이후 동일한 작업 요청 시 Operator는 이러한 사용자 설정을 자동으로 반영합니다.
2. **Instacart를 이용한 장보기**
   
   * 사용자가 특정 레시피를 요청하면, Operator는 해당 레시피를 검색한 후 필요한 재료를 Instacart 장바구니에 추가합니다.  
     
     ![](https://velog.velcdn.com/images/euisuk-chung/post/0560cded-fd95-48bb-b829-0c7ff0f3410e/image.png)
   * 사용자는 제외할 항목을 미리 명시할 수도 있으며, 작업 중간에 Operator가 확인을 요청합니다.
   * 또한 Take Control이라는 기능을 통해, 사용자는 작업의 중요한 순간에 직접 개입하여 민감한 정보를 입력하거나 세부사항을 수정할 수 있습니다. 해당 데모에서는 제품 수량 추가하는 것을 시연으로 보여줍니다. (+adding eggs)  
     
     ![](https://velog.velcdn.com/images/euisuk-chung/post/bf501ef4-521b-4cde-8f20-8920b017d2d1/image.png)
   * 추가적으로 Take Control 시에는 실제 브라우저에서 사람이 검색/입력하는 방식처럼 사용됩니다.
     
     + 예를 들어, 사용자가 Instacart에 로그인하거나 결제 정보를 입력해야 하는 경우, 우리가 직접 입력 후 완료했다고 전달해주는 방식으로도 이용이 가능합니다.
     + 이를 통해 사용자는 작업의 보안성과 신뢰성을 유지하면서도, Operator의 자동화 기능을 최대한 활용할 수 있습니다.
3. **OpenTable로 예약하기**
   
   * Operator는 사용자가 선호하는 음식 유형과 레스토랑을 기반으로 예약을 진행합니다. 예약 가능한 시간대를 사용자와 상호작용하며 제안하고, 최종 확인 후 예약을 완료합니다.
   * Demo 상세 분석:
     + `Prompt` : Book me a table for 2 person at Beretta tonight at 7PM.  
       
       ![](https://velog.velcdn.com/images/euisuk-chung/post/d55ef7a7-98c3-43d6-ad88-404d392a6b99/image.png)
     + 클라우드 버츄얼 환경에서 AI가 직접 조작 중, 웹 검색 및 예약을 수행하는 것을 볼 수 있습니다.  
       
       ![](https://velog.velcdn.com/images/euisuk-chung/post/054b6a20-84e1-484c-be42-1ea721d3c26b/image.png)
     + 주소의 경우 Custom Instructions에 미리 지정해둠으로써 AI가 어디에 사는지까지 파악 후, 위치에 맞는 근처 음식점으로 검색/예약을 수행할 수 있도록 합니다.  
       
       ![](https://velog.velcdn.com/images/euisuk-chung/post/9ad4f94f-9b83-42b9-9faa-38c0af42272b/image.png)
     + Human Interaction이 필요한 경우, 아래 그림과 같이 의사결정을 요청하는 것을 볼 수 있습니다.  
       
       ![](https://velog.velcdn.com/images/euisuk-chung/post/decb87ca-7a58-43fc-a6b2-b85b8b727f3c/image.png)
     + `Confirmation` 작업 전에 확인을 요청하고, 이를 수락 혹은 거절할 수 있습니다.  
       
       ![](https://velog.velcdn.com/images/euisuk-chung/post/fa64f11b-1e0a-4175-b10a-d7cd699f4ab6/image.png)

4. **멀티테스킹 가능**
   * Operator는 동시에 여러 작업을 수행할 수 있는 기능을 지원합니다.
     + 예를 들어, 한쪽 탭에서는 농구 경기 예약 작업을 진행하면서 다른 탭에서는 피자 주문을 진행할 수 있습니다.
   * 이는 Operator의 강력한 작업 분할 및 동시 처리 능력을 보여주는 사례입니다.
     + 데모에서 확인된 이 기능은 Operator가 단순히 반복적인 작업을 처리하는 것을 넘어 복잡한 멀티태스킹 시나리오를 지원할 수 있음을 보여줍니다.
5. **Save Prompts 기능**
   * "Saved Prompts"는 사용자가 반복적으로 수행하는 작업을 미리 정의하고 저장하여 이후 손쉽게 재사용할 수 있도록 돕는 기능입니다.  
     
     ![](https://velog.velcdn.com/images/euisuk-chung/post/ef4c8586-a0c4-4469-85bb-de71fec322f9/image.png)
   * 예를 들어 사용자가 금요일 저녁에 자주 특정 레스토랑에서 저녁 식사를 예약한다고 가정해 보겠습니다. 이 작업을 Saved Prompts에 저장하면, 사용자는 매번 동일한 과정을 반복하지 않고, 저장된 작업을 클릭하여 바로 실행할 수 있습니다.
     + (1) OpenTable을 활용해 예약을 저장해 두면, Operator는 다음 번에 예약할 때 저장된 정보를 자동으로 불러와 실행합니다.
     + (2) "중식 레스토랑 예약"과 같은 간단한 명령어를 입력하기만 하면, Operator가 자동으로 선호 레스토랑, 예약 시간대, 인원 수 등을 기반으로 예약을 처리합니다.
   * Saved Prompts는 작업의 제목과 명령어를 직관적으로 설정할 수 있게 도와줍니다.
     + 이렇게 저장된 작업은 Operator의 인터페이스 상단에서 언제든 액세스 가능하며, 다양한 시나리오에서 유용하게 활용될 수 있습니다.
     + 예를 들어:
       - 매주 반복되는 작업(예: 정기적인 장보기 또는 업무 도구 세팅)
       - 복잡한 예약 프로세스 간소화
       - 개인화된 쇼핑 목록 생성

이와 같은 사례는 Operator가 단순한 작업 자동화를 넘어 사용자 경험을 개인화하고, 반복 작업의 효율성을 극대화할 수 있음을 보여줍니다. 작업 진행 상황은 시각적으로 표시되며, 사용자는 언제든 작업에 개입하거나 수정할 수 있습니다.

---

### Evaluations

CUA는 여러 벤치마크에서 이전 최고 성능(State-of-the-Art, SOTA)을 갱신하며 뛰어난 성능을 입증했습니다.  

이를 통해 다양한 디지털 환경에서 작업을 수행할 수 있는 능력을 검증받았습니다.

**1. OSWorld (Computer Use)**

* OSWorld 벤치마크는 CUA가 Ubuntu, Windows, macOS 등 다양한 운영체제를 조작할 수 있는 능력을 평가합니다.

이 평가에서는 OS 상에서 수행 가능한 다양한 작업이 포함됩니다. 예를 들어, 다음과 같은 작업들이 포함됩니다:

* **파일 관리**: 폴더 생성, 파일 이동/복사, 파일 이름 변경
* **설정 조작**: 화면 밝기 조절, 네트워크 설정 변경
* **애플리케이션 실행**: 특정 앱 실행 후 간단한 조작 수행

![](https://velog.velcdn.com/images/euisuk-chung/post/ed194769-f669-48c9-9971-a7b5efdf6a68/image.png)

CUA는 기존의 SOTA 대비 높은 점수를 기록하며, 운영 체제 전반의 작업을 수행하는 데 있어 유연성과 성능을 입증했습니다.

> 👉 Computer use에 대한 CUA의 Inference 결과는 OpenAI블로그에서 확인하실 수 있습니다.  
> 
> ![](https://velog.velcdn.com/images/euisuk-chung/post/a16ecd0a-badd-405f-9b48-e51ee50bf901/image.png)

---

**2. WebArena (Browser Use)**

* WebArena는 실제 웹 사용 사례를 기반으로 하여 CUA의 웹 탐색 및 작업 능력을 평가합니다.

이 벤치마크는 다음과 같은 작업 시나리오를 포함합니다:

* **전자상거래**: 특정 상품을 검색하고 장바구니에 추가 후 결제 페이지까지 진행
* **콘텐츠 관리(CMS)**: 텍스트 입력, 이미지 업로드, 간단한 웹 페이지 게시
* **포럼 활동**: 게시글 작성, 댓글 추가, 특정 주제 검색

![](https://velog.velcdn.com/images/euisuk-chung/post/4a8aa412-bb55-488b-8cd4-19a6873b2293/image.png)

WebArena는 다양한 웹사이트에서의 상호작용을 요구하며, CUA가 얼마나 잘 화면을 이해하고 명확히 작업을 수행할 수 있는지 평가합니다.

---

**3. WebVoyager (Browser Use)**

* WebVoyager는 라이브 웹사이트에서의 작업 능력을 평가하는 벤치마크입니다.

이 평가에서는 Amazon, GitHub, Google Maps 등 널리 사용되는 웹사이트에서 다음과 같은 작업이 수행됩니다:

* **Amazon**: 특정 조건(예: 가격 범위, 평점)으로 상품 검색 및 필터링
* **GitHub**: 리포지토리 검색, 특정 파일 다운로드
* **Google Maps**: 특정 위치 검색, 경로 탐색

![](https://velog.velcdn.com/images/euisuk-chung/post/482c48bc-c3af-468a-99c6-266a7b553bd5/image.png)

WebVoyager는 실제 사용자가 웹에서 수행하는 과업과 유사한 복잡한 작업을 포함하며, CUA의 실제 활용 가능성을 직접적으로 보여줍니다. 특히, 이 벤치마크에서 87%라는 높은 성공률을 기록한 것은 CUA의 정밀한 작업 처리 능력을 나타냅니다.

> 👉 Browser Use에 대한 CUA의 Inference 결과는 OpenAI블로그에서 확인하실 수 있습니다.  
> 
> ![](https://velog.velcdn.com/images/euisuk-chung/post/e2e35143-0eb1-4161-9f18-dfe4b3f53b5c/image.png)

이러한 결과는 CUA가 다양한 환경에서 신뢰할 수 있는 도구로 자리잡을 가능성을 보여줍니다.

* 더욱이, 작업 시간이 증가할수록 성능이 향상되는 "테스트 시간 스케일링" 효과도 관찰되었습니다.

Operator를 통해 이러한 성능은 사용자 경험과 결합하여 더욱 강력한 도구로 발전하고 있습니다.

---

### Safety

CUA는 사용자의 안전을 최우선으로 고려하여 설계되었습니다.

Operator와 함께 제공되는 [Operator System Card](https://openai.com/index/operator-system-card/)는 CUA의 안전 기능을 상세히 설명하며, 주요 위험 요소를 다음 세 가지로 분류하고 있습니다:

![](https://velog.velcdn.com/images/euisuk-chung/post/4fecfefd-125e-4e2b-9d45-dc012300e481/image.png)

1. **Misuse (오용)**
   
   * CUA는 불법적이거나 규제된 작업에 대해 거부하도록 학습되었습니다.
   * 도박, 성인 콘텐츠, 무기 거래 사이트 등은 사전 차단된 블록리스트에 포함됩니다.
   * 실시간 자동화된 안전 점검 및 사용자 활동 모니터링을 통해 정책 위반을 감지합니다.
2. **Model Mistakes (모델 실수)**
   
   * 작업을 수행하기 전에 사용자 확인(confirmation)을 요청합니다.
   * 특히 민감한 작업에는 추가적인 확인 과정을 거칩니다.
   * 은행 거래와 같은 고위험 작업은 아예 수행하지 않도록 제한됩니다.
   * 이메일과 같은 민감한 웹사이트에서는 "Watch Mode"를 통해 사용자가 직접 작업을 감독하도록 합니다.
3. **Adversarial Attacks (적대적 공격)**
   
   * 프롬프트 인젝션, 피싱 시도 등을 탐지하고 차단합니다.
   * 화면의 수상한 콘텐츠를 감지하고 작업을 일시 중지합니다.

CUA는 이중, 삼중 방어 구조를 통해 안전성을 강화하며, 지속적인 피드백과 개선을 통해 더욱 안전한 환경을 제공하고자 합니다.

* 특히, Operator 내에서 모델의 모든 작업은 기록 및 검토될 수 있으며, 이는 잠재적인 오류나 악의적인 사용을 방지하는 데 중요한 역할을 합니다.
* Operator는 사용자에게 작업의 투명성을 제공하며, 작업 중 발생할 수 있는 오류나 위험 요소를 최소화하기 위한 안전 장치를 다수 포함하고 있습니다.

사용자 확인 시스템과 실시간 모니터링, 그리고 필요시 사용자가 컨트롤을 넘겨받을 수 있는 기능은 Operator와 CUA가 안전하게 작업을 수행할 수 있도록 지원합니다.

---

### Operator의 미래 전망

Operator와 CUA는 디지털 작업 자동화의 새로운 패러다임을 제시하며, 앞으로도 지속적으로 개선되고 확장될 예정입니다.

1. **개발자 지원**:
   
   * CUA를 API 형태로 제공하여, 개발자들이 자신만의 에이전트를 구축하거나 기존 워크플로우를 최적화할 수 있도록 지원할 계획입니다.
2. **확장된 접근성**:
   
   * 현재는 Pro 사용자에게만 제공되지만, 앞으로 Plus, Team, Enterprise 사용자를 포함한 더 넓은 사용자층으로 확대될 예정입니다.
3. **고도화된 기능**:
   
   * Operator의 기능을 고도화하여 더 복잡하고 긴 작업 흐름을 처리할 수 있도록 개발할 것입니다.

> API는 어떤식으로 제공해줄지 궁금하군요 ( •͈ ◦ •͈ )

---

### Conclusion

CUA는 멀티모달 이해, 추론, 안전성 측면에서 획기적인 발전을 이룬 에이전트입니다. API에 의존하지 않고도 사람이 사용하는 것과 동일한 인터페이스를 통해 다양한 디지털 환경에 적응할 수 있는 유연성을 제공합니다. 이는 AI가 인간과 함께 작업하며 생산성과 창의성을 극대화할 수 있는 새로운 가능성을 열어줍니다.

현재 Operator를 통해 미국의 Pro Tier 사용자들에게 연구 프리뷰 형태로 제공되며, 사용자의 피드백을 통해 지속적으로 개선될 예정입니다. OpenAI는 CUA가 다양한 디지털 작업의 "롱테일"을 해결하는 데 중요한 도구가 될 것이라 믿습니다. 향후 CUA는 더욱 다양한 작업 환경과 복잡한 문제를 해결하며, AI 기술의 새로운 기준을 제시할 것입니다.

Operator는 단순한 작업 도구가 아니라, 사용자의 디지털 환경을 더욱 편리하고 안전하게 만드는 "파트너"로 자리 잡고 있습니다. OpenAI는 Operator와 CUA를 통해 디지털 작업의 미래를 열어가며, AI가 사용자와 함께 성장하는 새로운 패러다임을 제시하고자 합니다.

