---
title: "[Tips] Lovable Prompting Tips 공개!! : Prompting 1.1"
date: "2025-08-18"
tags:
  - "Lovable"
  - "vibe coding"
year: "2025"
---

# [Tips] Lovable Prompting Tips 공개!! : Prompting 1.1

원본 게시글: https://velog.io/@euisuk-chung/Tips-Lovable-Prompting-101

Lovable 프롬프트 전략
===============

> 프롬프트 구조, 단계별 프롬프팅, 메타/역 메타 프롬프팅 및 예제를 통한 기초 전략

이 글은 Lovable의 공식 문서인 **[Prompting 1.1](https://docs.lovable.dev/prompting/prompting-one)**을 번역하고 정리한 콘텐츠입니다. Lovable은 강력한 Large Language Model(LLM)을 기반으로 하며, 효과적인 프롬프팅 전략을 통해 그 잠재력을 최대한 발휘할 수 있습니다.

여기서는 **프롬프트 구조, 단계별 프롬프팅, 메타/역 메타 프롬프팅** 등 **Lovable을 효율적으로 활용하기 위한 기초 전략과 예제를 소개**합니다. Lovable 팀과 커뮤니티의 경험을 바탕으로 구성된 이 가이드는 사용자가 더 정확하고 효율적인 결과를 얻을 수 있도록 돕기 위해 설계되었습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/f388233e-67b1-46bd-b73d-0287c9756d73/image.png)

> <https://docs.lovable.dev/prompting/prompting-one>

*본 글은 번역글이므로, 본문에서 언급된 "저희/우리"는 번역된 내용으로, 실제 Lovable 팀을 지칭합니다.*

⚠️ 참고사항!
--------

해당 글은 Lovable을 최대한 활용할 수 있도록 프롬프팅 전략과 접근법 목록을 정리한 글입니다. 이 중 일부는 저희 팀이 직접 경험한 내용을 통해 작성했고, 일부는 커뮤니티 구성원들이 공유해준 내용을 참고하여 작성되었습니다. `Lovable`은 **Large Language Model(LLM)에 의존하므로, 효과적인 프롬프팅 전략을 통해 효율성과 정확성을 크게 향상**시킬 수 있습니다.

프롬프팅이란 무엇인가?
------------

`프롬프팅`은 **AI 시스템이 작업을 수행하도록 제공하는 텍스트 지시사항을 의미**합니다.

* Lovable(AI 기반 앱 빌더)에서 프롬프트는 **UI 생성**부터 **백엔드 로직 작성**까지 `AI에게 무엇을 할지 "알려주는" 방법`입니다.
* Lovable은 Large Language Model(LLM)을 사용하므로 효과적인 프롬프팅이 중요합니다.

명확하고 잘 작성된 프롬프트는 앱 구축 시 AI의 효율성과 정확성을 크게 향상시킬 수 있습니다.  
간단히 말해, 더 나은 프롬프트가 더 나은 결과를 만듭니다.

프롬프팅이 중요한 이유
------------

대부분의 사람들은 프롬프팅이 **"단순히 AI에게 요청을 입력하고 최선의 결과를 바라는 것"**이라고 생각합니다 - 하지만, **그렇지 않습니다**.

* 평범한 AI 응답과 AI가 전체 워크플로우를 구축하도록 하는 것의 차이는 *"어떻게 프롬프트를 작성하느냐"*에 달려 있습니다.

개발자든 비기술자든, **Lovable**에서 프롬프트 엔지니어링을 마스터하면 다음과 같은 도움을 받을 수 있습니다:

* AI에게 정확히 무엇을 해야 하는지 지시하여 **반복 작업을 자동화**
* AI가 생성한 인사이트와 솔루션으로 **더 빠르게 디버그**
* 적절히 안내되면 AI가 무거운 작업을 처리하게 하여 **손쉽게 워크플로우를 구축하고 최적화**

> ❓ **그럼 Lovable을 사용할 때, 가장 좋은 점은?**
>
> * 전문 프로그래머가 될 필요가 없다는 것입니다.
> * 올바른 프롬프팅 기법을 사용하면 시행착오 없이 Lovable에서 AI의 모든 잠재력을 발휘할 수 있습니다.

AI가 어떻게 생각하는지 이해하기
------------------

기존 코딩과 달리, AI와 작업하는 것(working with AI)은 우리의 의도를 명확하게 *전달/소통*하는 것입니다.

Lovable을 구동하는 것과 같은 `Large Language Model(LLM)`/`Artificial Intelligence(AI)`는 **인간의 관점에서 "이해(understand)"**하지 않습니다 - **훈련 데이터의 패턴을 기반으로 출력을 예측**합니다.

이러한 LLM의 특징은, 우리가 프롬프트를 작성함에 있어서 중요한 의미를 갖습니다:

일관된 답변 결과(consistent outcomes)를 위해서는 프롬프트를 **명확한 섹션으로 구조화**하는 것이 도움이 됩니다. 권장되는 형식(eg. 프롬프팅을 위한 *"자전거 보조바퀴(training wheels)”*처럼)은 **Context**, **Task**, **Guidelines**, **Constraints**에 대한 라벨이 붙은 섹션을 사용합니다:

![](https://velog.velcdn.com/images/euisuk-chung/post/2e1f43ea-2616-4bc1-a4c4-df2430f8e63d/image.png)

> <https://www.google.com/search?q=%E2%80%9Ctraining+wheels%E2%80%9D>

* **컨텍스트와 세부사항 제공:**

  + AI 모델은 사용자가 제공하는 것 이외에는 상식이나 암시적 컨텍스트가 없습니다.
  + 항상 관련 배경이나 요구사항을 제공하세요.
    - 예를 들어,
      * "로그인 페이지 구축"이라고만 말하는 대신 세부사항을 명시하세요  
        (eg. *"React를 사용하여 이메일/비밀번호 인증과 JWT 처리가 있는 로그인 페이지를 생성하세요."*)
      * 기술 스택이나 도구를 명시적으로 포함하세요.  
        (eg. *"인증을 위해 Supabase 사용하세요."*)
* **지시사항과 제약조건을 명시적으로 제공:**

  + AI가 "목표를 추론할 것이라고 가정하지 마세요".
  + `제약조건`이나 `선호사항`이 있다면 **직접 텍스트로 명시**하세요.
    - 예를 들어,
      * 출력이 특정 라이브러리를 사용하거나 특정 범위 내에 머물러야 한다면 **모델에게 미리 알려주세요**.
      * AI는 지시사항을 **문자 그대로** 따를 것입니다 - `명령의 모호함`은 "원치 않는 결과"나 "AI 환각"(잘못된 정보 생성)으로 이어질 수 있습니다.
* **구조가 중요함 (순서와 강조):**

  + Transformer 아키텍처 덕분에 모델은 프롬프트의 **`시작`**과 **`끝`**에 특별한 주의를 기울입니다.
    - **가장 중요한 세부사항이나 요청을 시작 부분**에 두고, 강조가 필요하다면 절대적 요구사항을 끝에서 다시 강조하여 이를 활용하세요. (**DO NOT**, **NEVER**)
  + 또한 모델은 고정된 **`컨텍스트 윈도우`**를 가지고 있음을 기억하세요
    - ***지나치게 긴 프롬프트나 매우 긴 대화는 AI가 이전 세부사항을 잊게 만들 수 있습니다***.
    - 프롬프트를 집중적으로 유지하고 필요할 때 컨텍스트를 **새로** 고치세요. (eg. 세션이 길어지면 주요 포인트를 모델에게 상기시키기)
* **모델의 한계 알기:**

  + AI의 지식은 **훈련 데이터**에서 나옵니다.  
    (~~물론 요즘은 web search를 기본적으로 달고 있긴하지만~~)
    - 이러한 이유로 최근 사건이나 제공하지 않은 독점 정보는 알 수 없습니다.
    - 추측하고 있더라도 자신 있게 들리려고 할 것입니다(이는 모델 환각 현상으로 이어짐 - eg. [세종대왕 맥북프로 던짐 사건](https://www.hankookilbo.com/News/Read/A2023022215200000727) 등).
* 사실적 질문을 위해서는 항상 참조 텍스트나 데이터를 제공하거나 출력을 검증할 준비를 하세요.
* 프롬프팅을 매우 문자 그대로 이해하는 인턴에게 *정확히* 무엇이 필요한지 말하는 것처럼 생각하세요.
* 지침이 명확하고 구조적일수록 결과가 더 좋아집니다.

다음으로 프롬프트를 **효과적으로 만드는 핵심 원칙들**을 살펴보겠습니다.

핵심 프롬프팅 원칙: C.L.E.A.R. 프레임워크
----------------------------

훌륭한 프롬프트는 간단한 원칙들을 따릅니다. 이를 기억하는 편리한 방법은 **CLEAR**: **Concise, Logical, Explicit, Adaptive, Reflective**입니다.

지시사항을 작성할 때 이를 체크리스트로 사용하세요:

* `C` - **간결함(Concise):**

  + 명확하고 요점을 전달하세요.
  + 불필요한 내용이나 모호한 언어는 모델을 혼란스럽게 할 수 있습니다.
  + 직접적인 언어를 사용하세요. 예를 들어:
    - **Bad Case:** "과학 주제에 대해 뭔가 재밌는 얘기해봐."
    - **Good Case:** "**연안 도시에 대한 기후 변화 영향의 200단어 요약을 작성하세요**."
  + 불필요한 단어는 피하세요 - *세부사항이 지시적이지 않다면 산만할 뿐입니다*. 원하는 것을 설명할 때 **정확성**과 **간결성**을 목표로 하세요.
* `L` - **논리적(Logical):**

  + 프롬프트를 단계별 또는 잘 구조화된 방식으로 정리하세요.
  + 복잡한 요청을 순서가 있는 **단계나 불릿 포인트로 나누어 AI가 쉽게 따라할 수 있도록** 하세요.
  + 하나의 길고 연결된 요청보다는 **관심사를 분리**하세요. 예를 들어:
    - **Bad Case:** "사용자 가입 기능을 구축하고 사용량 통계도 보여줘."
    - **Good Case:** "**먼저** Supabase를 사용하여 이메일과 비밀번호로 사용자 가입 양식을 구현하세요. **그 다음**, 성공적인 가입 후 사용자 수 통계를 보여주는 대시보드를 표시하세요."
  + 논리적 흐름은 모델이 요청의 각 부분을 체계적으로 처리하도록 보장합니다.
* `E` - **명시적(Explicit):**

  + 원하는 것과 원하지 않는 것을 정확히 명시하세요.
  + 중요한 것이 있다면 자세히 설명하세요.
  + 가능하다면 형식이나 내용의 예시를 제공하세요.
  + 모델은 방대한 지식을 가지고 있지만 세부사항에 대한 당신의 마음을 읽지는 못합니다. 예를 들어:
    - **Bad Case:** "개에 대해 알려줘." (너무 개방적임.)
    - **Good Case:** "**골든 리트리버에 대한 5가지 독특한 사실을 불릿 포인트로 나열하세요.**"
  + 마찬가지로 원하는 출력 스타일이 있다면 명시하세  
    (예: "JSON 형식으로 응답" 또는 "캐주얼한 톤 사용").
  + AI를 초보자처럼 취급하세요: 아무것도 당연하다고 가정하지 마세요.
* `A` - **적응적(Adaptive):**

  + 첫 번째 답변이 완벽하지 않다면 안주하지 마세요.
  + 프롬프트는 **반복적으로** 개선될 수 있습니다. (맘 멀티턴!!)
  + Lovable의 AI(및 일반적인 LLM)의 큰 장점은 대화할 수 있다는 것입니다.
  + 초기 출력이 목표를 놓쳤다면 *접근법을 적응시키세요*:
    - **후속 프롬프트**에서 `지시사항을 명확히` 하거나 `오류를 지적`하세요.
    - 예를 들어 아래와 같이 오류를 지적할 수 있습니다.:
      * 지금 완성된 버전은 제공한 솔루션에 인증 단계가 빠져있습니다. (오류 지적)
      * 코드에 사용자 인증을 포함해주세요. (지시 명확)
  + 반복을 통해 모델을 더 나은 결과로 안내할 수 있습니다.
  + 심지어 AI에게 프롬프트 자체를 개선하는 방법을 물어볼 수도 있습니다  
    (이는 **메타 프롬프팅**으로, 나중에 다룰 예정).

> (참고) **메타(Meta-)**이란?
>
> * “**메타(meta-)**”라는 접두사는 원래 그 자체를 넘어서서, 더 높은 차원에서 다루는 것이라는 의미를 담고 있습니다.
> * 철학, 언어학, 컴퓨터 과학 등 여러 분야에서 쓰이는데, 공통적으로는 ‘**대상에 대한 대상**’, 즉 **자기 자신을 바라보는 관점**을 나타냅니다.
> * 또 메타는 언제 쓰였을까요? 예를 들어:
>   + **메타-데이터 (meta-data)**
>     - **기본 대상**: 데이터(정보 그 자체)
>     - **메타 의미**: 데이터에 대한 데이터(속성, 설명, 부가 정보)
>     - **예시**: 사진 파일이 데이터라면, 촬영 시간·위치(GPS)·해상도·파일 크기 같은 정보가 메타데이터
>   + **메타-인지 (metacognition)**
>     - **기본 대상**: 인지(생각하고 아는 행위)
>     - **메타 의미**: 생각에 대한 생각(자기 객관화, 자기 점검)
>     - **예시**: "너 자신을 알라"와 같은 메타인지(자기 성찰)
>   + **메타-학습 (meta-learning)**
>     - **기본 대상**: 학습(지식을 배우는 행위)
>     - **메타 의미**: 학습에 대한 학습(학습 방법 자체를 배우고 개선)
>     - **예시**: “시각 자료를 보면 더 잘 외운다”라는 본인만의 학습 전략을 배우는 것이 메타학습

> (참고) 그렇다면 메타-프롬프팅이란?
>
> * **메타 프롬프팅(Meta-Prompting)**은 말 그대로 "프롬프트 자체를 다루는 프롬프트"를 의미합니다.
>   + aka, 프롬프팅을 위한 프롬프팅
> * 보통 LLM에게 "이 작업을 해줘"라고 직접 지시하는 대신, "**내가 만든 프롬프트를 더 효과적이게 고쳐줘**" 또는 **"이 문제에 맞는 최적의 프롬프트를 생성해줘"**라고 요청하는 방식입니다.
>   + **일반 프롬프팅**: 모델에 직접 특정 작업을 지시 → "이 글을 요약해줘."
>   + **메타 프롬프팅**: 프롬프트를 다루는 방법을 지시 → "내가 준 글을 요약할 때 가장 효과적인 프롬프트를 작성해줘."
> * 즉, 프롬프트 엔지니어링을 사람이 직접 하는 게 아니라, AI에게 프롬프트 엔지니어 역할을 맡기는 거죠.

* `R` - **성찰적(Reflective):**
  + 각 AI 상호작용 후에 무엇이 효과적이었고 무엇이 그렇지 않았는지 검토하는 시간을 가지세요.
  + 이는 모델보다는 *당신(you)*에 관한 것입니다 - 프롬프트 엔지니어로서 어떤 프롬프트 표현이 좋은 결과를 얻었고 어떤 것이 혼란을 초래했는지 주목하세요.
  + 복잡한 세션 후에는 AI에게 **최종 솔루션이나 추론을 요약**하도록 요청할 수도 있습니다.  
    (앞에서도 살짝 언급은 했지만, 뒤에 메타 프롬프팅 챕터에서 논의할 예정)
  + 성찰적이 되는 것은 미래에 더 나은 프롬프트를 작성하는 데 도움이 되며, AI 소통에서 지속적인 개선의 사이클을 구축합니다.

> 프롬프트를 개발할 때 이러한 **CLEAR**: **Concise, Logical, Explicit, Adaptive, Reflective** 원칙들을 염두에 두세요.

다음으로는 기본부터 고급까지의 특정 프롬프팅 기법들을 살펴보겠습니다.  
여기에는 프롬프트 구조화 방법과 AI를 협력자로 활용하는 방법이 포함됩니다.

프롬프팅의 네 단계
----------

효과적인 프롬프팅은 연습을 통해 성장하는 기술입니다.

여기서는 구조화된 “**Training Wheels**”(이하, 보조바퀴)부터 **고급 메타 기법**까지 프롬프팅 숙련도의 네 단계를 개요로 제시합니다. 각 단계는 고유한 USE CASE가 있습니다 - 필요에 따라 조합하세요:

![](https://velog.velcdn.com/images/euisuk-chung/post/527bbeef-050c-4842-a0da-6f41fad0a7b7/image.png)

> <https://youtu.be/IqWfKj4mUIo>

![](https://velog.velcdn.com/images/euisuk-chung/post/80bc8a4d-750a-482a-9595-1bebb618e597/image.png)

### **1. 구조화된 "보조바퀴" 프롬프팅** (명시적 형식)

시작하거나 매우 복잡한 작업을 다룰 때는 프롬프트에 **라벨이 붙은 구조를 사용하는 것**이 도움이 됩니다. 이는 필요한 모든 정보를 제공하도록 보장하는 *보조바퀴* 역할을 합니다.

> 🚲 **왜 ‘보조바퀴’일까?**  
> ‘보조바퀴 프롬프팅’이라는 별칭은 초보자가 자전거를 탈 때 달아주는 작은 바퀴에서 따온 말입니다.
>
> * 보조바퀴는 균형을 잡아주어 넘어지지 않도록 돕지만, 결국 목표는 보조바퀴를 떼고 자유롭게 타는 것입니다. 구조화된 프롬프팅도 마찬가지입니다.
> * 처음에는 **맥락(Context), 작업(Task), 가이드라인(Guidelines), 제약조건(Constraints)** 같은 라벨을 붙여 AI에게 명확한 길을 제시합니다.
> * 이렇게 하면 AI가 엉뚱한 길로 새는 걸 막고, 원하는 방향으로 ‘균형 잡힌’ 결과를 얻을 수 있습니다.

Lovable에서 검증된 형식은 프롬프트를 다음과 같은 섹션으로 나누는 것입니다:

* **Context:** AI를 위한 배경이나 역할 설정.  
  (예: "당신은 세계적 수준의 Lovable AI 코딩 어시스턴트입니다.")
* **Task:** 달성하고자 하는 구체적인 목표.  
  (예: "사용자 로그인과 실시간 동기화가 있는 풀스택 할 일 목록 앱을 구축하세요.")
* **Guidelines:** 선호하는 접근법이나 스타일.  
  (예: "프론트엔드는 React, 스타일링은 Tailwind, 인증과 데이터베이스는 Supabase를 사용하세요.")
* **Constraints:** 엄격한 제한사항이나 금지사항.  
  (예: "유료 API는 사용하지 마세요. 앱은 모바일과 데스크톱에서 작동해야 합니다.")

각 부분을 명확히 라벨링함으로써 오해의 여지를 거의 남기지 않습니다.

예를 들어, 프롬프트는 다음과 같을 수 있습니다:

```
# 한글 프롬프트
Context: 당신은 Lovable을 사용하는 전문 풀스택 개발자입니다.
Task: Supabase를 사용하여 React에서 안전한 로그인 페이지를 생성하세요(이메일/비밀번호 인증).
Guidelines: UI는 미니멀해야 하며 Tailwind CSS 규칙을 따라야 합니다. 각 단계에 대한 명확한 코드 주석을 제공하세요.
Constraints: `LoginPage` 컴포넌트만 수정하고 다른 페이지는 변경하지 마세요. 최종 출력은 Lovable 에디터에서 작동하는 페이지여야 합니다.
```

```
# 영어 프롬프트
Context: You are an expert full-stack developer using Lovable.
Task: Create a secure login page in React using Supabase (email/password auth).
Guidelines: The UI should be minimalistic, and follow Tailwind CSS conventions. Provide clear code comments for each step.
Constraints: Only modify the LoginPage component; do not change other pages. Ensure the final output is a working page in the Lovable editor.
```

![](https://velog.velcdn.com/images/euisuk-chung/post/6a6f549e-3cc9-476f-9145-81023245866d/image.png)

> 직접 실험한 이미지 - 1단계

이 수준의 세부사항은 AI를 단계별로 안내합니다. *보조바퀴 프롬프팅*은 초보자나 복잡한 다중 부분 작업(multi-part tasks)에 탁월합니다 - 정확히 무엇이 필요한지 생각하도록 강제하고, 요청을 구조화하여 모델을 도와줍니다.

### 2. 대화형 프롬프팅 (보조바퀴 없음)

익숙해지면 항상 그렇게 엄격한 구조가 필요하지 않습니다. **대화형 프롬프팅**은 여전히 명확성과 완전성을 유지하면서 위 예시처럼 **공식적인 라벨 없이** 동료에게 작업을 설명하는 것처럼 AI에게 더 자연스럽게 작성할 수 있음을 의미합니다.

예를 들어:

```
# 한글 프롬프트
1. 프로필 사진을 업로드하는 기능을 구축해봅시다. 
2. 이미지 파일 입력과 제출 버튼이 있는 양식이 포함되어야 합니다. 
3. 제출되면 이미지를 Supabase storage에 저장하고 사용자 프로필을 업데이트해야 합니다. 
4. 이에 필요한 React 컴포넌트와 백엔드 함수를 작성해주시고, 오류(파일이 너무 큰 경우 등)를 우아하게 처리하도록 해주세요.
```

```
# 영어 프롬프트
1. Let’s build a feature to upload a profile picture. 
2. It should include a form with an image file input and a submit button. 
3. When submitted, it should store the image in Supabase storage and update the user profile. 
4. Please write the necessary React component and any backend function needed for this, and ensure to handle errors (like file too large) gracefully.
```

![](https://velog.velcdn.com/images/euisuk-chung/post/4b7e6d99-4516-4c6b-b641-04458301caf5/image.png)

> 직접 실험한 이미지 - 2단계

이는 앞서 본 1단계보다 **상대적으로 자유로운 형식의 프롬프트이지만, 여전히 요구사항을 논리적 순서에 따라 명확히 제시한다**는 특징이 있습니다.

* 대화형 프롬프트는 중요한 세부사항을 빠뜨리지 않을 것이라고 신뢰할 때 효과적으로 작동합니다.
* 특히 결과를 여러 번 수정·반복하는 과정에서는 상호작용을 보다 자연스럽게 이어갈 수 있습니다.

이 스타일은 빠른 작업을 하거나, 이미 AI가 필요한 맥락을 충분히 이해하고 있을 때 유용합니다. 대화형 스타일이라도 요청 내용을 단락이나 불릿 포인트로 나누어 **구조감을 흉내낼 수 있으며**, 궁극적인 목표는 **명확한 소통**이라는 점에서 동일합니다.

### 3. **메타 프롬프팅 (AI 지원 프롬프트 개선)**

**메타 프롬프팅**은 말 그대로, *"AI에게 프롬프트를 더 다듬거나 계획을 세우는 데 도움을 요청하는 고급 기법"*입니다. Lovable의 AI(ChatGPT와 같은)는 언어를 분석하고 추론할 수 있기 때문에, 지시문을 더 정교하게 개선하는 데 활용할 수 있습니다.

> 🤔 **메타 프롬프팅의 정의** - 위에 소개한 **<핵심 프롬프팅 원칙: C.L.E.A.R. 프레임워크>** 챕터에서 확인 가능합니다

이 방법은 특히 원하는 결과와 다른 출력을 받았을 때 유용합니다. 그런 경우는 **대개 프롬프트가 모호하거나 불충분했다는 신호**일 수 있습니다.

이럴 때는, 다음과 같이 요청하여 프롬프트 개선을 시도해볼 수 있습니다.:

```
# 방법 - 1
내 마지막 프롬프트를 검토하고 모호하거나 빠진 부분이 있는지 확인해 주세요. 
더 간결하고 정확하게 다시 쓰려면 어떻게 해야 하나요?

Review my last prompt and identify any ambiguity or missing info. 
How can I rewrite it to be more concise and precise?
```

```
# 방법 - 2
이 프롬프트를 더 구체적이고 상세하게 다시 작성해 주세요: 
‘Supabase를 사용해 React에서 역할 기반 인증을 보장하는 안전한 로그인 페이지를 만들어라.’

Rewrite this prompt to be more specific and detailed: 
‘Create a secure login page in React using Supabase, ensuring role-based authentication.
```

AI는 이러한 요청을 바탕으로 더 구조화되고 구체적인 버전을 제시해 줄 수 있으며, 이를 통해 원래 프롬프트에서 불분명했던 부분을 확인할 수 있습니다. 본질적으로 AI를 **프롬프트 편집자**로 활용하는 셈입니다.

Lovable에서는 이를 **Chat mode**에서 안전하게 시도할 수 있습니다. (프로젝트 파일을 직접 수정하지 않기 때문입니다 - 채팅/토의 목적의 모드)

![](https://velog.velcdn.com/images/euisuk-chung/post/f6440fbc-b797-41bc-9db7-257b1e554006/image.png)

`메타 프롬프팅`은 AI를 단순한 응답자가 아니라 **함께 더 나은 질문을 만들어가는 협력자**로 바꿔줍니다.

* 덕분에 자신이 미처 고려하지 못한 개선점을 발견할 수 있으며, 이는 프롬프트 엔지니어링 능력을 빠르게 성장시키는 강력한 방법입니다.

### 4. **역 메타 프롬프팅 (문서화 도구로서의 AI)**

**역 메타 프롬프팅(Reverse meta prompting)**은 우리가 채팅/코딩 등의 작업을 끝낸 뒤, **AI에게 그 과정을 요약하거나 문서화하도록 하여** 나중에 학습하거나 재사용할 수 있게 만드는 방법입니다.

> 쉽게 말해, AI에게 “**방금 과정을 되짚고 다음번을 위한 설명이나 프롬프트를 만들어 달라**”라고 요청하는 것이죠. 이는 특히 `디버깅`과 `지식 축적`에 강력한 효과를 발휘합니다.

예를 들어 Lovable에서 **까다로운 문제를 해결한 후 이렇게 요청**할 수 있습니다:

**요청 예시**

```
지금까지 우리가 JWT(Json Web Token) 인증을 설정하면서 겪은 오류를 요약하고, 어떻게 해결했는지 설명해 주세요. 
그리고 같은 실수를 피할 수 있도록, 앞으로 사용할 수 있는 프롬프트를 작성해 주세요.
```

AI는 문제와 해결 과정을 간결히 정리한 뒤, *“Context: building auth… Task: avoid X error by doing Y…” (Context: 인증 구축… Task: Y를 수행하여 X 오류 방지…)* 와 같은 템플릿 프롬프트를 제시할 수 있습니다. 이렇게 하면 자연스럽게 **재사용 가능한 프롬프트와 교훈의 개인 라이브러리**가 쌓입니다.

**출력 예시**

```
Context: JWT 기반 인증을 React + Supabase로 구축
Task: 
  - .env에 올바른 JWT 시크릿 키 설정
  - Supabase auth 모듈을 초기화하여 로그인 요청 정상화
Constraint: 
  - 보안 환경변수는 git에 노출되지 않도록 할 것
```

이 접근법은 Lovable에서 특히 빛을 발합니다. 다음에 비슷한 작업을 마주했을 때, 이미 검증된 프롬프트를 그대로 활용하거나 최소한 따라갈 수 있는 명확한 체크리스트를 갖게 되기 때문입니다. 말 그대로 **실무에서 금 같은 자산**이 되는 셈이죠.

또 다른 예로, API 호출이 실패한 이유를 한 시간 동안 디버깅했다고 합시다.

**요청 예시**

```
API 호출이 실패한 이유와 해결 과정을 정리하고, 앞으로 같은 실수를 방지할 수 있는 프롬프트를 작성해 주세요.
```

문제를 해결한 직후 AI에게 그 과정을 문서화하도록 요청하면, 자신의 이해를 강화하는 동시에 Knowledge Base나 향후 프로젝트에 바로 활용할 자료를 얻게 됩니다. 덕분에 같은 오류를 되풀이하지 않게 되는 것이죠.

**출력 예시**

```
Context: 외부 REST API 호출
Task: 
  - 요청 시 반드시 "Content-Type": "application/json" 헤더 포함
  - 최신 API 키를 환경변수에 저장 후 참조
Constraint: 
  - 키는 절대 코드에 하드코딩하지 않을 것
```

고급 프롬프팅 기법
----------

기본 사항을 익혔다면, 이제 Lovable의 AI를 최대한 활용하기 위한 더 고급 전략을 활용할 때입니다. 이러한 기법들은 복잡한 시나리오를 처리하고, (환각과 같은) 오류를 줄이며, AI의 출력을 필요에 맞게 조정하는 데 도움이 됩니다.

### Zero-Shot vs. Few-Shot 프롬프팅

* **Zero-Shot 프롬프팅**은 *예시 없이* 모델에게 작업을 수행하도록 요청하는 것을 의미합니다. 모델의 일반적인 훈련에 의존하여 무엇을 해야 하는지 알도록 합니다.

  + 이는 대부분의 프롬프트의 기본값입니다: 요청을 명시하면 AI가 프롬프트에서 "아는" 것과 이해하는 것으로부터 순전히 답변을 생성합니다.
  + Zero-shot은 효율적이고 작업이 일반적이거나 명확히 설명된 경우 잘 작동합니다.
  + 예를 들어: *"다음 문장을 스페인어로 번역하세요: 'I am learning to code.'"*는 zero-shot 프롬프트입니다 - 간단한 명령이며, AI는 지식을 사용하여 응답합니다(예시가 필요하지 않음).
* **Few-Shot 프롬프팅**은 프롬프트에 몇 가지 **예시나 시연**을 제공하여 AI에게 원하는 형식이나 스타일을 정확히 보여주는 것을 의미합니다.

  + 본질적으로 프롬프트 자체에서 예시로 가르치는 것입니다. 이는 특정 형식이나 작업이 특이할 때 출력 품질을 극적으로 향상시킬 수 있습니다.
  + Few-shot 프롬프트에서는 다음과 같이 말할 수 있습니다:
  + 다음 문장들의 문법을 수정하세요:
    - **Input:** "the code not working good" → **Output:** "The code is not working well."
    - **Input:** "API give error in login" → **Output:** "The API gives an error during login."
    - **Input:** "user not found in database" → **Output:** ❓

![](https://velog.velcdn.com/images/euisuk-chung/post/58546440-0e7e-426c-ba53-33d6a97a39c2/image.png)

두 가지 입력-출력 예시를 제공함으로써 AI는 세 번째에 대해 비슷한 패턴으로 계속하도록 준비됩니다. Few-shot 프롬프팅은 특정 응답 스타일이 필요할 때(예: 특정 형식의 코드 주석이나 커밋 메시지 예시) Lovable에서 유용합니다. 더 많은 프롬프트 토큰을 소모하지만(그 예시들을 포함하기 때문) 종종 더 일관된 결과를 산출합니다.

> 🤔 **언제 어떤 것을 사용하는 것이 좋을까?**  
> 간단한 작업이나 모델의 내장 능력을 신뢰할 때는 먼저 zero-shot을 시도하세요. 결과가 원하는 형식이나 깊이가 아니라면 예시를 추가하여 few-shot으로 전환하세요.
>
> * 예를 들어, 함수를 요청했는데 출력이 선호하는 스타일을 따르지 않는다면, 좋아하는 스타일의 예시 함수를 보여주고 다시 프롬프트하세요.
>   + Few-shot은 복잡한 출력(테스트 케이스 작성처럼 - 하나의 샘플 테스트를 제공한 다음 더 많이 작성하도록 요청)에서 빛납니다.
> * 요약하면, **빠른 직접 답변에는 `zero-shot`, 제어된 스타일이나 복잡한 지시사항에는 `few-shot`**.

### 환각 관리 및 정확성 보장

모델이 정확하지 않은 정보나 코드를 자신 있게 유저(요청자)에게 제공하는 것을 우리는 **AI환각**이라고 합니다.

> **Lovable과 같은 코딩 플랫폼에서 환각은?**  
> AI가 존재하지 않는 함수를 사용하거나, 존재하지 않는 API를 호출하거나, 요약에서 세부사항을 조작하는 것을 의미할 수 있습니다. 이를 완전히 제거할 수는 없지만(*AI의 한계임*), **환각을 줄이는 방식으로 프롬프트할 수 있습니다**. (아래 참고)

#### ✅ 1. 기반 데이터 제공

**전략:**

* AI가 추측하지 않도록 **Knowledge Base**에 프로젝트 관련 문서를 넣어주면 환각을 방지할 수 있습니다.

**예시:**

* PRD에 “앱은 `Next.js`와 `Prisma` ORM을 사용한다”를 포함시킨 뒤,

  ```
  "Prisma 모델을 기반으로 사용자 등록 API를 작성해주세요. 아래는 User 모델 정의입니다: 
  model User { id Int @id @default(autoincrement()) email String @unique password String }"
  ```

  → 이렇게 하면 AI가 존재하지 않는 ORM 메서드를 발명하지 않음.

---

#### ✅ 2. 프롬프트 내 참조

**전략:**

* 실제 API 응답 예시를 프롬프트에 포함시켜, 환각을 줄일 수 있습니다.

**예시:**

```
아래 제공된 JSON 응답을 사용하여 User 객체를 파싱하는 TypeScript 함수를 작성해주세요:

{
  "id": 1,
  "name": "Alice",
  "email": "alice@example.com"
}
```

→ 실제 데이터 구조를 보여줌으로써 AI가 잘못된 필드명(예: `username`)을 지어내지 않음.

---

#### ✅ 3. 단계별 추론 요청

**전략:**

* 최종 코드 전에 접근법을 설명하게 해서, 환각 여부를 확인할 수 있습니다.

**예시:**

```
Postgres에서 특정 날짜 범위의 데이터를 가져오는 쿼리를 작성해주세요. 
최종 쿼리를 주기 전에 접근 방법을 단계별로 설명하고, 불확실한 점이 있다면 먼저 짚어주세요.
```

→ AI가 막무가내로 SQL을 내놓지 않고, `WHERE date BETWEEN ...` 같은 로직을 먼저 설명해줌.

---

#### ✅ 4. 정직함 지시

**전략:**

* 잘 모를 때 꾸며내지 말라고 직접적으로 명시해주어, 환각을 줄일 수 있습니다.

**예시:**

```
만약 정확한 함수 시그니처를 확신하지 못한다면, 임의로 만들지 말고 어떤 문서가 필요한지 알려주세요. 
잘못된 코드 대신 "확신하지 못합니다"라고 답해도 됩니다.
```

→ 이렇게 하면 AI가 “fetchUserData 함수는 정확히 존재하는지 확실하지 않습니다.  
(eg. API 문서 확인이 필요합니다”라고 대답할 수 있음.)

---

#### ✅ 5. 반복적 검증

**전략:**

* 답변 후 검토를 하도록 요청하면, 환각을 최소화할 수 있습니다.
* 환각이 발생하더라도, 이를 잡아낼 수도 있습니다.

**예시:**

```
위에서 작성한 로그인 함수 코드가 보안 요구사항(비밀번호 해시, SQL 인젝션 방지)을 충족하는지 검토해 주세요. 
문제가 있을 수 있는 부분이 있다면 설명해주세요.
```

→ AI가 자기 출력을 다시 점검하면서 보완 포인트를 알려줌.

Lovable에서 환각은 또한 AI가 요청하지 않은 파일이나 컴포넌트를 생성하거나 의도되지 않은 창의적 자유를 취하는 것을 의미할 수도 있습니다.

> 하지만, 항상 AI가 생성한 코드를 정상성 확인하세요.  
> (Always review AI-generated code for sanity.)

뭔가 너무 "마법적"이거나 예상치 못한 것 같다면 의문을 제기하세요. 이러한 전략으로 환각을 관리함으로써 프로젝트에 대한 제어를 유지하고 정확성을 보장합니다.

### 모델 인사이트 활용 (AI 도구 알기)

모든 AI 모델이 동일하게 동작하는 것은 아니며, **같은 모델이라도 설정에 따라 전혀 다른 결과**를 낼 수 있습니다. 원하는 수준의 결과를 얻으려면, **Lovable에서 제공하는 도구들을 어떻게 활용할지 이해하는 것**이 중요합니다.

* **`Chat Mode` vs `Default Mode`:**  
  현재 Lovable에는 두 가지 주요 모드가 있습니다. **Chat mode**(대화형 AI 어시스턴트)와 **Default/Editor mode**(실제로 코드 변경을 적용). 각 모드는 목적이 다르므로 적절히 구분해서 사용하는 것이 좋습니다.

  + **Chat Mode**는 `브레인스토밍`, `디자인 논의`, `디버깅`에 적합합니다. 이 모드에서는 AI가 직접 코드를 수정하지 않고, 아이디어나 분석을 자유롭게 제안합니다.

    - 예를 들어 오류 로그를 붙여넣고 \_"이 오류 로그를 분석하고 원인이 무엇인지 설명해줘"\_라고 요청하면, AI가 가능한 문제 원인을 단계별로 설명해 줄 수 있습니다.
  + **Default Mode**는 실제로 **코드를 작성하거나 컴포넌트를 생성**하는 데 사용됩니다. 일반적인 워크플로우는 이렇습니다: Chat mode에서 아이디어를 구체화하고 문제를 해결한 뒤, 계획이 명확해지면 Default mode로 전환해 간단한 프롬프트로 바로 구현합니다. (Default mode는 프로젝트 파일을 직접 수정하기 때문입니다.)
* 어떤 모드를 언제 쓸지 알고 있으면 개발 흐름을 훨씬 효율적이고 안전하게 유지할 수 있습니다.

* **토큰 길이와 응답:** 응답의 길이를 항상 의식하세요.

  + 너무 큰 출력(예: 전체 코드 모듈)을 한 번에 요청하면 토큰 제한 때문에 답변이 잘리거나 내용이 뒤섞일 수 있습니다. => 이런 경우에는 작업을 더 작은 단위로 쪼개는 게 좋습니다.
    - 예를 들어 “**한 번에 함수 하나씩 작성**” 같은 방식입니다 (e.g., generate code for one function at a time).
  + 또한, Lovable의 채팅이나 프롬프트 UI는 출력이 잘렸을 때 경고를 보여주기도 하는데, 이는 곧 “**남은 부분을 다시 요청하거나 작업을 분할해야 한다**”는 신호로 보면 됩니다.
* **형식 및 코드 선호사항:** AI는 명시된 형식을 잘 따라갑니다.

  + 예를 들어 “마크다운 형식으로 코드 출력해줘”라든가 “이 프로젝트의 ESLint 규칙을 지켜줘”라고 알려주면 그대로 적용합니다. (eg. “output code in markdown format” or “follow the project’s ESLint rules”)
  + 반대로 아무 말도 하지 않으면 프로젝트의 스타일 가이드를 AI가 스스로 짐작할 수는 없습니다.
    - 변수명 규칙이나 특정 코드 패턴을 선호한다면 반드시 프롬프트에 적어두세요.
  + 시간이 지나면(채팅이 길어질수록) AI가 프로젝트에서 반복되는 스타일을 학습해 모방하지만, 프롬프트에서 가볍게 리마인드해 주면 정렬 속도가 훨씬 빨라집니다.

> 정리하자면, **AI는 매우 강력하지만 본질적으로 문자 그대로 받아들이는 도구**입니다.

어떤 모드와 모델을 쓰고 있는지 이해하면서, `강점`(구조화된 입력과 풍부한 컨텍스트)을 극대화하고, `약점`(건망증, 장황함, 환각)을 방어하는 방식으로 프롬프트를 구성하는 것이 핵심입니다.

이제 이 원칙들을 토대로 Lovable을 더 효과적으로 활용하기 위한 실전 모범 사례를 살펴보겠습니다.

**추가 프롬프팅 팁**
-------------

마지막으로, Lovable 플랫폼에서 작업할 때의 특정 팁과 기법들을 다뤄보겠습니다. 이러한 모범 사례들은 **일반적인 프롬프트 엔지니어링 개념을 Lovable의 기능과 결합하여 최상의 결과**를 얻는 데 도움이 됩니다.

### 견고한 Knowledge Base로 시작하기

프롬프트를 작성하기 전에 프로젝트의 `Knowledge Base`(Lovable의 프로젝트 설정에서)를 설정하세요.

![](https://velog.velcdn.com/images/euisuk-chung/post/b3291214-f06d-47d6-a206-a4d3cce7839a/image.png)

> <https://docs.lovable.dev/features/knowledge>

**Project Requirements(PRD)**, 사용자 플로우, 기술 스택 세부사항, UI 디자인 가이드라인, 백엔드 구체사항을 포함하세요. 이는 AI가 항상 갖게 될 지속적인 컨텍스트 역할을 합니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/a6af1622-2032-42b4-85fe-d41cb02938f0/image.png)

> <https://www.scalablepath.com/project-management/product-requirements-document-guide>

예를 들어, PRD에 "범위 외: 소셜 로그인(Out of scope: social login)"이 명확히 나열되어 있다면, AI가 무작정 Google 로그인 기능을 추가할 가능성이 줄어듭니다. 시작할 때 명시적으로 프롬프트할 수도 있습니다:

*코드를 작성하기 전에 프로젝트 Knowledge Base를 읽고 앱의 목적과 제약사항을 이해했는지 확인해주세요.*

> 이는 AI가 프로젝트의 컨텍스트를 내재화하고 관련 없는 제안이나 환각된 기능을 줄이도록 보장합니다.

### 구체적으로, 모호함 피하기

모호한 프롬프트는 모호한 결과를 가져옵니다.

> 항상 *무엇을* 원하고 *어떻게* 원하는지 명확히 하세요.

**DON’Ts**

```
# 예시 - 1
이 앱을 더 좋게 만들어줘.
Make this app better.
```

```
# 예시 - 2
사용자 입력을 위한 양식을 만들어줘
Create a form for user input
```

후자는 범위와 예상 결과에 대한 명확한 방향을 제공합니다.

**DOs**

```
# 예시 - 1
Refactor the app to clean up unused components and improve performance
(without changing UI or functionality.)

사용되지 않는 컴포넌트를 정리하고 성능을 향상시키도록 앱을 리팩터링하세요. 
(UI나 기능은 변경하지 마세요.)
```

```
# 예시 - 2
Create a user registration form with fields for username, email, and password and include a submit button.

사용자명, 이메일, 비밀번호 필드와 제출 버튼이 포함된 사용자 등록 양식을 생성하세요.
```

### 점진적 프롬프팅

한 번의 프롬프트로 전체 복잡한 앱을 요청하고 싶은 충동을 억제하세요.

> 개발 과정을 논리적 단계로 나누고 한 번에 하나씩 프롬프트하세요.

**DON’Ts**

```
Build a CRM app with Supabase, auth, Google Sheets export, and data enrichment.

Build my entire e-commerce app with authentication, product listings, and checkout.
```

```
Supabase, 인증, Google Sheets 내보내기, 데이터 강화가 있는 CRM 앱을 구축해줘.

인증, 제품 목록, 결제가 있는 전체 전자상거래 앱을 구축해줘.
```

**DOs**  
이러한 단계별 진행은 AI가 집중하고 정확하게 유지하는 데 도움이 되며, 문제를 일찍 잡을 수 있습니다:

(예시 - 1)  
1.1.

```
Set up a Supabase-connected CRM backend.

Supabase에 연결된 CRM 백엔드를 설정해주세요.
```

1.2.

```
Great! Could you please add a secure authentication flow with user roles?

좋습니다! 사용자 역할이 있는 안전한 인증 플로우를 추가해주시겠어요?
```

1.3.

```
Thank you! The next step is to integrate Google Sheets to export records.

감사합니다! 다음 단계는 레코드를 내보내기 위해 Google Sheets를 통합하는 것입니다.
```

(예시 - 2)

2.1.

```
Set up a database schema for user information.

사용자 정보를 위한 데이터베이스 스키마를 설정해주세요.
```

2.2.

```
Develop an API endpoint to retrieve user data please

사용자 데이터를 검색하는 API 엔드포인트를 개발해주세요
```

### 제약조건과 요구사항 포함

제약조건을 명시하는 것을 피하지 마세요.

> 뭔가가 *반드시* 하거나 *절대 하지 말아야* 한다면 직접 프롬프트에 적으세요.

**제약조건 추가**

(예시 - 1)

```
Create a simple to-do app with a "maximum of 3 tasks visible" at a time.
Include the ability to add, edit, and delete tasks.

"한 번에 최대 3개"의 작업만 보이는 간단한 할 일 앱을 만들어주세요.
작업을 추가, 편집, 삭제하는 기능을 포함하세요.
```

(예시 - 2)

```
Optimize this code, but ensure the "UI and core functionality remain unchanged". 
Document each change you make.

이 코드를 최적화하되 "UI와 핵심 기능은 변경되지 않도록 하세요". 
각 변경사항을 문서화해주세요.
```

(예시 - 3)

```
Use at most 3 API calls for this, and "ensure no external library is required".

이것을 위해 최대 3개의 API 호출을 사용하고, "외부 라이브러리가 필요하지 않도록 하세요".
```

(예시 - 4)

```
The page should "display a maximum of 3 tasks" at a time.

페이지는 한 번에 "최대 3개의 작업"을 표시해야 합니다.
```

이러한 제한은 AI가 과도하게 엔지니어링하는 것을 방지합니다.  
최대 항목 수나 성능 목표와 같은 제약조건을 추가하면 AI가 중요한 것에 집중할 수 있습니다.

### 표현의 모호함 피하기

용어가 다양한 방식으로 해석될 수 있다면 명확히 하세요.

> 더 명확할수록 AI가 추측해야 할 것이 줄어듭니다.  
> 반대로 너무 모호하게 요청하면, 환각 현상을 불러일으킬 확률이 올라갑니다.

**DON’Ts**

```
Add a profile feature
프로필 기능을 추가해줘
```

```
Support notifications
알림을 지원해줘
```

후자는 범위와 예상 결과에 대한 명확한 방향을 제공합니다.

**DOs**

```
Add a user profile page with fields X, Y, Z.
X, Y, Z 필드가 있는 사용자 프로필 페이지를 추가해주세요.
```

```
Send an email notification on form submission.
양식 제출 시 이메일 알림을 보내주세요.
```

### 톤과 예의 염두에 두기

AI의 기능 자체가 달라지는 것은 아니지만, **정중한 어투가 의외로 더 좋은 결과를 이끌어낼 때가 있습니다.**

* 예를 들어 *please* 같은 표현이나 공손한 요청을 포함하면, 프롬프트가 조금 더 설명적으로 읽히고 컨텍스트가 풍부해져 AI에게 도움이 됩니다.

예시:

```
Please refrain from modifying the homepage, focus only on the dashboard component.
홈페이지는 수정하지 말고, 대시보드 컴포넌트에만 집중해주세요.
```

이런 식의 표현은 정중하게 들리면서 동시에 AI에게 **무엇을 하지 말아야 하는지**까지 명확히 알려줍니다. 중요한 것은 AI의 감정이 아니라, **프롬프트 안에 세부사항을 얼마나 잘 담아내느냐**입니다. (물론, 정중하게 말하는 게 손해 볼 일은 없겠지요!)

### Lovable의 모드를 의도적으로 사용

> Use Lovable’s Modes Intentionally

앞서 언급했듯이, **계획 단계에는 `Chat Mode`**, **구현 단계에는 `Default Mode`**를 활용하는 것이 효과적입니다.

* 예를 들어, 새로운 기능을 시작할 때는 `Chat Mode`에서 먼저 컴포넌트 분해나 데이터 구조를 브레인스토밍할 수 있습니다.

```
I want to add a blog section to my app. 
Let’s discuss how to structure the data and pages.

내 앱에 블로그 섹션을 추가하고 싶습니다. 
데이터와 페이지를 어떻게 설계할지 함께 논의해봅시다.
```

이런 식으로 요청하면 AI가 전체적인 개요를 제시합니다.

* 그 결과에 만족한다면, 이제 `Default Mode`로 전환해 실제 구현을 지시할 수 있습니다.

```
Create a BlogPost page and a supabase table or schema for blog posts based on the above plan.

위 계획을 바탕으로 `BlogPost` 페이지와 블로그 게시물용 Supabase 테이블 또는 스키마를 생성해주세요.
```

### 형식을 유리하게 사용

> Use formatting to your advantage

**상황에 맞게 목록이나 단계를 사용해 프롬프트를 구조화**하세요.

AI에게 목록 형태의 응답이나 **순차적 절차를 원한다면, 프롬프트에서 항목을 번호를 매겨 나열**하세요. 단계를 번호로 표시하면 모델이 같은 형식으로 응답하도록 힌트를 주는 효과가 있습니다.

(예시 - 1)

```
안전한 인증 시스템을 설정하는 과정을 단계별로 생각해봅시다:
1. 필요한 컴포넌트는 무엇인가요?
2. 이들이 어떻게 상호작용해야 하나요?
3. 구현 코드를 작성해주세요.

Let's think through the process of setting up a secure authentication system:
1. What are the necessary components?
2. How should they interact?
3. Provide the implementation code.
```

(예시 - 2)

```
첫째, 접근 방식을 설명하고, 둘째 코드를 보여주고, 셋째 테스트 예시를 제공해주세요.

First, explain the approach. Second, show the code. Third, give a test example.
```

### 예시나 참조 활용

원하는 디자인이나 코드 스타일이 있다면 **반드시 언급하거나 예시를 함께 제공**하세요.

구체적인 참조(이미지나 코드 스니펫)를 보여주면 AI가 단순히 추측하지 않고, 그 스타일을 바탕으로 답변할 수 있습니다. (eg. Few-shot처럼)

(예시 - 1)

```
우리는 팀이 작업을 추적할 수 있는 프로젝트 관리 도구를 만들고 있습니다.
이 도구는 다음과 같은 기능을 가져야 합니다:
- 사용자 인증
- 프로젝트 생성
- 작업 할당
- 보고 기능

첫 번째 단계로, 프로젝트 생성 UI를 만들어주세요.
```

```
We are building a project management tool that helps teams track their tasks.
This tool should have features like:
 - user authentication
 - project creation
 - task assignments
 - reporting

Now, for the first task, create the UI for project creation.
```

(예시 - 2)

```
Supabase 통합과 안전한 인증 플로우가 포함된 CRM 앱이 필요합니다. 
백엔드 설정부터 시작해주세요.
```

```
I need a CRM app with Supabase integration and a secure auth flow. 
Start by setting up the backend.
```

(예시 - 3)

```
친환경 제품에 초점을 맞춘 전자상거래 플랫폼을 개발하고 있습니다. 
카테고리와 가격 필터가 있는 상품 목록 페이지를 생성해주세요.
```

```
We are developing an e-commerce platform focusing on eco-friendly products. 
Generate a product listing page with filters for category and price.
```

### 이미지 프롬프트 사용

Lovable에서는 **이미지를 업로드하여 프롬프트에 포함**할 수 있습니다.

* 예를 들어 디자인 시안을 보여주고 *“이 스타일과 맞춰주세요”* 라고 요청하면 됩니다.

여기에는 두 가지 접근 방식이 있습니다.

#### 1) 간단한 이미지 업로드 프롬프팅

(예시 - 1)

```
첨부된 이미지와 최대한 유사한 UI를 생성하고 구현해주세요.

Create and implement a UI that looks as similar as possible to the image attached.
```

(예시 - 2)

```
이 스크린샷은 모바일에서 발생하는 레이아웃 이슈 상황을 보여줍니다. 
같은 디자인 구조를 유지하면서 반응형으로 보이도록 여백과 패딩을 조정해주세요.

This screenshot shows a layout issue on mobile. 
Adjust margins and padding to make it responsive while keeping the same design structure.
```

#### 2) 상세 지시사항과 함께 하는 이미지 프롬프팅

이미지 자체가 많은 정보를 담고 있지만, **원하는 기능을 글로 추가 지시**하면 훨씬 좋은 결과를 얻을 수 있습니다.

예시:

```
이 스크린샷과 최대한 비슷한 앱을 만들어주세요. 
본질적으로 칸반 보드 클론입니다.  

- 각 열에 새 카드(티켓)를 추가할 수 있어야 합니다.  
- 같은 열 안에서는 카드 순서를 자유롭게 바꿀 수 있어야 합니다.  
- 카드를 열 사이에 옮길 수도 있어야 합니다.  

드래그 앤 드롭 기능은 Pangea home dnd npm 패키지를 사용해도 좋습니다.
```

```
I want you to create the app as similar as possible to the one shown in this screenshot.
It's essentially a kanban clone.

It should have the ability 
* to add new cards (tickets) in each column, 
* have the ability to change the order of those tickets within a single column, 
* and even move those cards between columns.

Feel free to use the Pangea home dnd npm package for drag-and-drop functionality.
```

### 피드백 통합

AI의 출력을 검토하고 개선을 위한 구체적인 피드백을 제공하세요. (멀티턴)

```
로그인 양식이 좋아 보이지만 이메일 필드에 유효한 이메일 주소가 포함되도록 하는 검증을 추가해주세요.

The login form looks good, but please add validation for the email field to ensure it contains a valid email address.
```

### 접근성 강조

`접근성 표준`(adheres to accessibility standards)과 `현대적 모범 사례`(modern best practices)를 준수하는 코드 생성을 장려하세요. 이는 출력이 기능적일 뿐만 아니라 사용자 친화적이고 접근성 가이드라인을 준수하도록 보장합니다.

> 🤗 **접근성 표준(adheres to accessibility standards)**이란?  
> 위 문장에서 말하는 **“code that adheres to accessibility standards”**는, 코드가 공식 접근성 표준(대표적으로 `WCAG 2.2`, `WAI-ARIA` 등)과 법·가이드라인(예: `ADA`, `EN 301 549`)을 준수하도록 작성된 상태를 뜻합니다.  
> => 즉, 사용하는 사람의 신체·인지·환경적 제약과 상관없이 키보드·스크린리더·고배율·고대비·자막 등 보조 수단으로 접근하고 이해·조작할 수 있게 만드는 모든 설계·구현 원칙을 가리킵니다.

```
적절한 ARIA 라벨과 키보드 탐색 지원을 포함하여 **접근성 모범 사례**를 따르는 로그인 양식용 React 컴포넌트를 생성해주세요.

Generate a React component for a login form that follows accessibility best practices, 
including appropriate ARIA labels and keyboard navigation support.
```

> 🤗 **ARIA 레이블(Accessible Rich Internet Applications label)**이란?  
> **ARIA 레이블**(Accessible Rich Internet Applications label, 흔히 aria-label)은 **스크린리더 같은 보조기술에 읽히는 대체 텍스트를 제공하기 위해 쓰이는 속성**입니다.  
> => 쉽게 말하면, 시각적으로는 버튼이나 아이콘만 보이는데, **화면 읽기 프로그램에게는 “이건 ‘검색 버튼’이야”라고 알려주는 역할**을 합니다.

### 미리 정의된 컴포넌트와 라이브러리

프로젝트에서 일관성과 효율성을 유지하기 위해 **특정 UI 라이브러리나 컴포넌트 사용**을 명시하세요.  
이는 AI가 특정 도구를 활용하도록 지시하여 호환성과 애플리케이션 전반의 균일한 디자인 언어를 보장합니다.

```
Tailwind CSS로 스타일링하는 shadcn/ui 라이브러리를 사용하여 반응형 네비게이션 바를 생성해주세요.

Create a responsive navigation bar using the shadcn/ui library with Tailwind CSS for styling.
```

### 다국어 프롬프팅

다국어 환경에서 작업할 때는 **코드 주석과 문서 모두에 대해 원하는 언어를 명시**하세요.  
이는 생성된 콘텐츠가 다른 언어를 사용하는 팀 구성원들에게 접근 가능하도록 하여 협업을 향상시킵니다.

```
피보나치 수열을 계산하는 Python 스크립트를 생성해주세요. 
주석과 문서를 프랑스어로 제공해주세요.
```

```
Generate a Python script that calculates the Fibonacci sequence. 
Provide comments and documentation in French.
```

### 프로젝트 구조 및 파일 관리 정의

새로운 컴포넌트가 **프로젝트 내 어디에 위치해야 하는지에 대한 명확성을 제공**하여 일관된 파일 조직을 유지하면서 체계적이고 유지보수 가능한 코드 생성을 보장하기 위해 파일 이름과 경로를 포함한 프로젝트 구조를 명확히 개요로 제시하세요.

```
'UserProfile'이라는 새 React 컴포넌트를 생성하고 'components/user-profile.tsx'로 저장해주세요. 
프로필 사진, 사용자명, 자기소개 섹션이 포함되도록 하세요.
```

```
Create a new React component named 'UserProfile' and save it as 'components/user-profile.tsx'.
Ensure it includes a profile picture, username, and bio section.
```

### 정확한 편집 지시사항 제공 (AI 집중시키기)

> (주의) 기본적으로 Lovable AI에게 **뭔가를 변경하라고 요청하면 전체 파일이나 여러 파일을 다시 작성**할 수 있습니다.

의도하지 않은 변경을 피하려면 ***어디서* 그리고 *무엇을* 변경할지 매우 구체적으로 명시**하세요.

* Lovable의 "Select(Edit)" 기능을 사용하여 컴포넌트나 파일을 강조한 다음 그 선택에 대해서만 프롬프트할 수 있습니다. 또는 프롬프트에서 파일/컴포넌트를 명시적으로 명명하세요.

```
`Header` 컴포넌트에서 가입 버튼의 텍스트를 'Get Started'로 변경하고 네비게이션 바의 왼쪽으로 이동해주세요.

_In the _Headercomponent, change the signup button’s text to ‘Get Started’ and move it to the left side of the nav bar.
```

이렇게 하면 AI가 `Header` 컴포넌트에 집중하고 그 부분만 조정한다는 것을 알게 됩니다.

바꾸지 말아야 할 부분은, **AI에게 건드리지 말아야 할 것을 알려주세요**.

```
헤더와 관련 없는 다른 컴포넌트나 로직은 수정하지 마세요.

Do not modify any other components or logic unrelated to the header.
```

이러한 관행("Diff & Select" 접근법이라고 불리기도 함)은 최소한의 목표화된 변경을 보장하여 더 빠른 응답과 더 적은 회귀적 버그(regression bugs)를 가져옵니다.

### 파일 잠금 (우회 방법)

현재 Lovable에는 명시적인 파일 잠금 기능이 없을 수 있지만, 프롬프트 표현을 통해 시뮬레이션할 수 있습니다.

AI가 절대 변경해서는 안 되는 중요한 파일들(잘 작동하는 복잡한 컴포넌트 같은)이 있다면, 모든 프롬프트에서 지시사항을 반복할 수 있습니다:

```
authentication.js 파일은 변경하지 마세요.

Do not change the authentication.js file.
```

AI에게 지속적으로 자제하라고 말함으로써 원치 않는 편집의 가능성을 줄입니다.  
마찬가지로 AI가 프로젝트의 한 부분에서만 작업하기를 원한다면 명시적으로 제한하세요:

```
`ProfilePage` 컴포넌트에만 변경사항을 집중하고, 앱의 다른 모든 부분은 그대로 유지한다고 가정하세요.

_Focus changes solely on the _ProfilePagecomponent; assume all other parts of the app remain as is.
```

프롬프트에서 이를 미리 명시하면 AI가 경계 내에서 작업하는 데 도움이 됩니다.

### 디자인 및 UI 조정

Lovable에서 UI 변경을 위한 프롬프트를 작성할 때는 기능을 망가뜨리지 않도록 명확성이 중요합니다:

* **순전히 시각적 변경**을 원한다면 그렇게 말하세요.

  + *"로그인 버튼을 파란색으로 만들고 20% 크게 하되, 기능이나 onClick 로직은 전혀 변경하지 마세요."*
  + 이는 AI가 스타일링하면서 실수로 ID를 이름을 바꾸거나 로직을 변경하지 않도록 보장합니다.
* **반응성**(디자인을 모바일 친화적으로 만들기)의 경우, AI를 계획을 통해 안내하세요.

  + 예를 들어:
    - *"랜딩 페이지를 모바일에 최적화하세요: 모바일 우선 접근법을 사용하세요. 먼저 각 섹션이 더 작은 화면에서 어떻게 재배치되어야 하는지 개요를 작성한 다음 해당 CSS 변경사항을 구현하세요. 표준 Tailwind 브레이크포인트(sm, md, lg)를 사용하고 사용자 정의 브레이크포인트는 피하세요. 기능상 아무것도 변경되지 않고 레이아웃만 변경되도록 하세요."*
  + 이런 종류의 상세한 지시사항을 제공함으로써 데스크톱 레이아웃을 망가뜨리지 않고 모바일에 대한 철저한 적응을 얻을 수 있습니다.
* 디자인 변경을 염두에 두고 있다면, 원하는 결과와 제약조건("**HTML 구조는 동일하게 유지하고 CSS만 업데이트**" 같은)을 설명하면 AI가 올바른 솔루션에 집중하는 데 도움이 됩니다. AI 디자인 변경 후에는 모든 것이 여전히 예상대로 작동하는지 확인하기 위해 항상 앱을 테스트하세요.

### 코드 리팩터링 및 최적화

프로젝트가 발전함에 따라 Lovable의 AI는 성능이나 유지보수성을 개선하기 위한 리팩터링을 제안할 수 있습니다. 리팩터링을 위한 프롬프팅은 고급이지만 가치 있는 사용 사례입니다:

* **동작 변경 없음**을 강조하세요: *"명확성과 효율성을 위해 코드를 리팩터링하되, 앱의 기능과 출력은 동일하게 유지되어야 합니다."* 이는 AI에게 리팩터링이 버그나 기능 변경을 도입해서는 안 된다고 알려줍니다.
* **먼저 리팩터링 계획**을 요청할 수 있습니다: *"`utils/` 폴더를 스캔하고 코드 구조나 중복에서 개선사항을 제안하세요. 변경사항을 나열하되 아직 적용하지는 마세요."* AI가 개선할 것에 대한 보고서를 제공할 수 있습니다. 그러면 구현을 위해 프롬프트할 변경사항을 결정할 수 있습니다.
* **대규모 리팩터링의 경우 단계별로 수행**하세요.

  + 한 번에 하나의 모듈을 프롬프트하고, 테스트한 다음 진행하세요. 이는 단계별 원칙과 어울립니다.
  + 예를 들어:
    - 먼저 상태 관리 로직을 리팩터링하고, 나중에 API 호출을 리팩터링하는 것이 한 번에 모든 것을 하는 것보다 낫습니다.
* 리팩터링 후에는 빠른 **사후 확인**(post-check)을 프롬프트하는 것이 현명합니다.

  + 예시:
    - *"이제 코드가 리팩터링되었으므로 빠른 체크리스트를 실행해보세요: UI가 동일하게 보이고 모든 테스트나 주요 플로우가 여전히 통과하나요?"*
  + AI가 자체 검증을 하거나 수동으로 확인할 것들을 나열할 수 있습니다.

### AI 지원으로 디버깅

버그는 불가피합니다. Lovable에는 빠른 수정을 위한 "`Try to Fix`" 기능이 있지만, 직접 프롬프트를 통해 AI를 활용할 수도 있습니다:

* 오류가 발생하면 **오류 로그나 메시지**를 프롬프트(이상적으로는 Chat mode에서)에 복사하고 다음과 같이 요청하세요:

  + 예:
    - *"여기 오류와 관련 코드 스니펫이 있습니다 - 무엇이 이를 야기하고 어떻게 수정할 수 있나요?"*  
      (Here’s the error and relevant code snippet – what is causing this and how can we fix it?)
  + 상세한 오류 컨텍스트는 AI가 문제를 정확히 찾아내는 데 도움이 됩니다.
* 디버깅하면서 **CLEAR 원칙**을 사용하세요:

  + 코드가 무엇을 하기로 되어 있었는지 대 실제로 무엇이 일어났는지에 대해 명시적으로 설명하세요.
  + 때때로 AI에게 버그를 자세히 설명하는 것만으로도 해결책으로 이어질 것입니다.
* AI의 첫 번째 수정이 작동하지 않으면 **적응적 원칙**을 사용하세요:

  + 무엇이 변경되었는지 또는 새로운 오류를 제공하고, 다시 시도하거나 대안적 접근법을 제안하도록 요청하세요.
* Chat Mode를 활용하여 버그를 논의하세요:

  + 예:
    - *"수정이 작동하지 않았습니다. 런타임에 상태가 여전히 정의되지 않았습니다. 또 다른 원인이 무엇일 수 있나요? 가능한 원인들을 생각해봅시다."*  
      (The fix didn’t work. The state is still undefined at runtime. What else could be wrong? Let’s think through possible causes.)
  + 그럴듯한 해결책을 찾을 때까지 주고받을 수 있고, 그 다음 Default Mode에서 적용할 수 있습니다.
* **UI 버그**의 경우, 스크린샷을 공유하거나 시각적 문제를 설명할 수도 있습니다.

  + 예:
    - "사이드바는 모바일에서 숨겨져야 하는데 여전히 보입니다. 여기 CSS가 있습니다... 왜 실패할 수 있나요?"  
      (The sidebar is supposed to hide on mobile, but it’s still visible. Here’s the CSS… Why might it be failing?”)
  + AI는 충분한 정보가 주어지면 CSS나 레이아웃 문제에 대해 추론할 수 있습니다.
* **수정 후에는 항상 테스트**하세요.

  + 수정 후 제대로 작동한다면 역 메타 프롬프팅을 사용하여 AI가 근본 원인이 무엇이었고 미래에 어떻게 피할 수 있는지 요약하도록 하여 지식 기반을 풍부하게 하는 것을 고려하세요. (노하우 축적)

### AI를 언제 (그리고 언제 하지 말아야 할지) 참여시킬지

* 마스터 프롬프터는 때때로 프롬프트할 필요가 전혀 없다는 것을 압니다.

  + 변경사항이 극도로 작거나(단순하거나) 이미 빠르게 하는 방법을 알고 있다면(예: 텍스트 라벨 변경, 하나의 패딩 값 조정), 코드 에디터에서 수동으로 하는 것이 더 빠를 수 있습니다.
  + 사소한 작업에 AI에 과도하게 의존하면 속도가 느려지고 프롬프트 할당량을 사용할 수 있습니다. AI가 가치를 더하는 곳에서 사용하세요.
  + 복잡한 로직, 보일러플레이트 생성, 다단계 작업, 또는 확신이 서지 않는 것들. 더 간단한 문제의 경우 다음을 할 수 있습니다:
* 자신의 지식이나 빠른 검색(또는 Lovable 외부에서 ChatGPT에게 질문)을 사용하여 알아내세요.

  + 특히 AI가 오해할 수 있는 것에 대한 프롬프트를 소모하지 않는 경우에요.
  + 개발자 도구 활용: 브라우저 DevTools 콘솔을 열어 요소를 검사하거나 JavaScript 오류를 실시간으로 디버그하세요. 수정을 식별하면 직접 구현하거나 프롬프트를 통해 확인할 수 있습니다.
* 예시:

  + 버튼이 잘못된 색상이라는 것을 알아차렸다면, AI에게 문제를 설명하고 의도된 것보다 더 많이 변경할 위험을 감수하는 것보다 CSS 클래스를 직접 수정하는 것이 더 빠를 수 있습니다.
  + 반면에 처음부터 새로운 기능을 구현해야 한다면 이는 AI에게 완벽한 작업입니다 - 무엇과 왜를 설명하면 AI가 코드로 어떻게 할지 알아냅니다.
* Lovable의 AI는 어시스턴트 개발자와 같다는 것을 기억하세요.

  + 명확한 작업과 감독을 제공하여 관리합니다.
  + 개발을 극적으로 가속화할 수 있지만, 작업을 검토하고 지시하는 리드는 여전히 당신입니다.

다양한 도구에서 이러한 전략 적용
------------------

위의 프롬프팅 원칙들은 Lovable의 채팅뿐만 아니라 AI나 자동화 도구와 상호작용하는 어디서든 적용됩니다:

### Lovable의 Builder에서

![](https://velog.velcdn.com/images/euisuk-chung/post/13921994-d7d0-4f14-85f9-23cb36d0c157/image.png)

> <https://lovable.dev/>

주로 Lovable 채팅 인터페이스에서 이러한 프롬프트를 사용하여 앱을 구축하고 개선할 것입니다.

1. 광범위한 프로젝트 프롬프트로 시작한 다음 기능별로 반복하세요.
2. 코드를 변경하지 않고 논의하거나 디버그해야 할 때는 Chat-Only 모드를 사용하세요.

### Make.com이나 n8n과 함께 (워크플로우 자동화)

이런 플랫폼은 일반 대화체 프롬프트와 방식이 조금 다를 수 있지만, **자동화 설계에는 여전히 명확하고 구조화된 AI 지시문이 큰 도움**이 됩니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/4b18fb16-e8ea-4b98-8751-dcb44904019d/image.png)

> <https://www.make.com/en>

![](https://velog.velcdn.com/images/euisuk-chung/post/da8857a4-583d-43c1-8c88-6458bfac352b/image.png)

> <https://n8n.io/workflows/>

예를 들어, Lovable에게 통합 로직 생성을 지시할 수 있습니다.

```
“폼 제출 시, Slack 알림을 위해 Make.com 웹훅으로 데이터를 전송하라.”

When a form is submitted, send the data to a Make.com webhook for Slack notification.
```

Lovable은 웹훅과의 연계를 통해 자동화 구축을 도울 수 있습니다. 앱이 이메일 발송이나 CRM 업데이트처럼 외부 작업을 위임해야 할 때, Lovable이 Make 또는 n8n을 사용하도록 프롬프트할 수 있습니다.

```
“사용자가 앱에 가입하면, Salesforce에 레코드를 생성하는 Make.com 워크플로를 트리거하라.”

After a user signs up in the app, trigger a Make.com workflow that creates a record in Salesforce.
```

이 경우 Lovable은 해당 웹훅/API 호출 코드를 자동으로 작성합니다. 프롬프트를 명확한 단계와 파라미터로 구조화해 두면, AI가 Lovable과 외부 서비스를 어떤 방식으로 연결해야 하는지 정확히 파악합니다.

### **엣지 케이스 및 외부 서비스와의 통합**

Lovable은 많은 서비스(Stripe, GitHub, Supabase 등)와 통합됩니다. 이를 위한 프롬프팅에서는 통합 세부사항을 **Context/Constraints**의 일부로 취급하세요.

예를 들어,

```
결제를 위해 양식을 Stripe(테스트 모드)에 연결하세요. 성공 시 /thank-you로 리디렉션하세요.

Connect the form to Stripe (test mode) for payments. On success, redirect to /thank-you.
```

외부 서비스가 무엇을 해야 하는지 명확히 하세요. n8n(자체 호스팅 자동화) 사용에서도 마찬가지입니다 - 다음과 같이 작성할 수 있습니다:

```
양식 제출 후 n8n 웹훅 URL로 POST 요청을 보내고, 
확인 메시지를 표시하기 위해 응답을 기다리세요.

Send a POST request to the n8n webhook URL after form submission, 
and wait for its response to show a confirmation message.
```

여기서 명확성이 핵심이므로 AI가 올바른 호출을 생성합니다.

TL;DR
-----

* 강력한 프롬프팅은 **명확성, 구조, 컨텍스트**에 관한 것입니다.
  + Lovable에게 기능을 구축하라고 말하든 Make.com 시나리오를 조율하든, 목표는 원하는 것의 그림을 그리는 것입니다.
* 확신이 서지 않으면 구조화된 프롬프트로 시작하고, 자신감을 얻으면서 더 대화형 스타일로 발전시키세요.
* 메타 프롬프팅 기법을 사용하여 각 상호작용에서 개선하고 배우세요.
* 연습을 통해 AI를 개발팀의 확장처럼 안내할 것이고 - 필요한 정확한 출력을 얻는 것이 자연스럽게 느껴질 것입니다.

결론
--

이제 Lovable의 AI에 맞춘 명확하고 효과적인 프롬프트를 작성하는 방법에 대한 확실한 이해를 갖게 되었을 것입니다.

기본적인 CLEAR 원칙부터 few-shot 예시와 메타 프롬프팅 같은 고급 전략까지, 이러한 기법들은 AI로부터 정확히 필요한 것을 얻을 수 있도록 - 그 이상도 그 이하도 아닌 - 힘을 실어줍니다. 요청을 구조화하고, 컨텍스트를 제공하고, 환각과 같은 함정을 피하고, Lovable 특화 기능들(Knowledge Base, Chat mode 등)을 활용하여 워크플로우를 간소화하는 방법을 배웠습니다.

> 마스터 수준의 프롬프팅은 게임 체인저입니다.

마스터 수준의 프롬프팅은 AI를 기믹에서 신뢰할 수 있는 팀원으로 바꿔줍니다. 연습을 통해 더 빠르게 앱을 구축하고, 좌절감 없이 디버그하고, 단순히 *올바른 질문을 하고* 올바른 안내를 제공함으로써 창의적인 솔루션을 탐색할 수 있다는 것을 발견할 것입니다. 핵심은 지시사항에서 **스마트하고, 간결하고, 직접적이고, 적응적**으로 유지하는 것입니다 - 마치 숙련된 엔지니어가 팀과 소통하는 것처럼 말이죠.

> 마지막으로, 각 상호작용에서 항상 배우세요(그 성찰적 습관).

모든 프롬프트/응답은 기법을 더욱 개선하기 위한 피드백입니다. Lovable에서 계속 구축하면서 AI가 훌륭한 결과를 생성하기 위해 들어야 하는 것에 대한 직감을 개발할 것입니다. 이를 자신의 독창성과 결합하면 달성할 수 없는 것이 거의 없습니다.

> **큰 아이디어에 집중하세요**

*무엇을 해야 하는지 명확히 알려주면 Lovable의 AI가 실행 세부사항을 처리하도록 하세요.*

행복한 프롬프팅과 행복한 구축을!  
오늘도 읽어주셔서 감사합니다 💌