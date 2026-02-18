---
title: "[Anthropic] 프로덕션에서의 Vibe Coding"
date: "2025-08-01"
tags:
  - "Anthropic"
  - "Claude"
  - "vibe coding"
year: "2025"
---

# [Anthropic] 프로덕션에서의 Vibe Coding

![](https://velog.velcdn.com/images/euisuk-chung/post/6a3b3b3b-86f5-41cb-a7e3-07bca03060dd/image.png)

> <https://youtu.be/fHWFF_pnqDk?si=-MXGeYqm8e0EZKcr>

Code w/ Claude
==============

Vibe Coding in Production
-------------------------

최근 소프트웨어 개발 커뮤니티에서 "Vibe Coding"이라는 다소 파격적인 개념이 회자되고 있습니다. 단순한 자동완성이나 코파일럿 보조를 넘어서, AI가 코드를 "느낌대로" 작성하고, 인간은 결과만 검토하는 방식—이것이 가능한 시대가 정말 올 수 있을까요?

2025년 5월, Anthropic의 연구원 Erik Schulntz는 샌프란시스코에서 열린 **Code w/ Claude** 행사에서 이 주제를 정면으로 다뤘습니다. 그는 AI의 지수적 성장에 맞춰 **책임 있는 Vibe Coding을 프로덕션 환경에 적용하는 실전 전략**을 공유하며 청중의 깊은 공감을 이끌어냈습니다.

이 글에서는 그의 발표를 토대로 Vibe Coding의 정의부터 적용 전략, 실무 워크플로우, 그리고 앞으로의 개발자 역량까지 폭넓게 살펴보겠습니다.

---

Vibe Coding이란 무엇인가?
-------------------

Vibe Coding은 흔히 Copilot, Cursor 등의 AI 코딩 도구 사용과 혼동되곤 합니다. 그러나 Schulntz는 이를 **"코드의 존재를 잊고 AI의 흐름에 몸을 맡기는 것"**으로 정의합니다. Andrej Karpathy의 말을 빌리자면:

> “*Fully give in to the vibes. Embrace exponentials. Forget that the code even exists.*”

즉, 인간은 로직을 직접 짜는 대신, 문제 정의와 목표만 명확히 제시하고 AI에게 전체 구현을 위임합니다. 이 과정에서 **코드는 수단이 아닌 부산물**로 취급되며, 인간은 제품의 의도와 동작 결과만을 검토하는 역할을 맡습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/b13171e0-9320-46b3-9686-50cab80edf7c/image.png)

> <https://youtu.be/L8Tb3RERZoY>

---

왜 지금 Vibe Coding을 논해야 할까?
-------------------------

### 1. AI의 작업 길이(Task Length)가 지수적으로 늘어나고 있다

현재 Claude와 같은 모델은 약 **1시간 분량의 작업**을 수행할 수 있습니다. 하지만 AI 작업 범위는 **7개월마다 두 배씩 확장**되고 있습니다. 불과 1~2년 내에 AI는 하루치, 심지어 일주일치의 작업도 감당할 수 있게 될 것입니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/8605d307-89bc-4db4-8dee-b388d0be58fd/image.png)

이런 상황에서 **과거처럼 코드 라인을 일일이 읽고 검토하는 방식은 병목(bottleneck)**으로 작용하게 됩니다.

> AI는 점점 더 많은 코드를 생성하고 있지만, 사람이 이해하고 리뷰할 수 있는 양은 거의 늘지 않기 때문입니다.

그렇다면 우리는 이 새로운 현실에 어떻게 적응해야 할까요?  
사실 이와 유사한 상황은 과거에도 존재했습니다.

### 2. 이전 컴파일러 사례를 통해 배우는 교훈

잠깐 코딩 역사를 되돌아보도록 하겠습니다.

> (참고) 💻 **컴파일러 이전: 사람이 직접 기계어를 작성하던 시절**

* 1950년대 초반까지, 개발자는 **기계어(machine code)** 또는 **어셈블리 언어(assembly)**로 직접 코드를 작성했습니다.
* 이 언어는 사람이 읽기 힘든 이진수(예: 10110000)나 저수준 명령어들(예: MOV AX, 1)로 구성되어 있었습니다.

**예시 - 기계어**

* 이건 CPU가 직접 이해하는 0과 1의 나열입니다.
* 사람이 작성하기에는 매우 어렵고, 실수도 많았습니다.

```
10110000 00000001
10110010 00000010
00000011
```

**예시 - 어셈블리어**

* 좀 더 읽기 쉬운 수준으로 발전했지만 여전히 매우 저수준이었습니다.
* 하지만 여전히 레지스터, 명령어, 메모리 주소 등 **하드웨어 세부사항을 직접 다뤄야 했습니다**.

```
MOV AX, 1
MOV BX, 2
ADD AX, BX
```

* 위 언어들은 하나의 기능을 추가하기 위해서도 수백 줄의 매우 상세한 작업이 필요했고, 버그를 찾기도 매우 어렵고 비효율적이었습니다.

> (참고) 🚀 **혁신의 순간: 컴파일러의 등장**
>
> * 1952년, IBM의 그레이스 호퍼(Grace Hopper)는 최초의 컴파일러 중 하나인 A-0 시스템을 개발했습니다.
> * 이후 1957년, IBM은 **Fortran (Formula Translation)**이라는 최초의 고급 언어(high-level language)와 컴파일러를 함께 공개합니다.

**예시 - 고-수준 언어 (High-Level Language) + 컴파일러**

* 컴파일러가 를 통해 아래 같은 고-수준 언어(코드)를 읽고, 필요한 어셈블리 명령어와 기계어로 자동 변환해줄 수 있게 되었습니다.

```
A = 1
B = 2
C = A + B
```

초기 컴파일러가 등장했을 때, 많은 개발자는 출력된 어셈블리 코드를 직접 확인하며 신뢰를 형성해갔습니다.  
(어떻게 보면 우리가 hallucination check, LLM-as-Judge를 도입하는 것과 비슷한거 같네요 ㅎㅎ)

그러나 결국 **시스템을 신뢰하지 않고는 대규모 개발이 불가능하다는 현실**에 직면했고, 개발자들은 이를 자연스럽게 받아들이게 되었습니다.

발표자는 Vibe Coding 역시 같은 전환점에 서 있다고 말하며

> "**AI가 생성한 코드를 완전히 이해하지 않아도 제품이 잘 동작하도록 만드는 것**"

그것이 앞으로의 기술 과제라고 강조했습니다.

---

우리가 코드를 이해하지 못할 때 어떻게 검증할까?
---------------------------

기술 리더, 제품 관리자, 심지어 CEO도 자신이 직접 작성하지 않은 작업물을 평가해야 할 때가 많습니다. 이는 소프트웨어 개발자만의 고민이 아닙니다.

### 일반적인 검증 전략 3가지:

1. **Acceptance Test 작성**: 결과만 확인해도 의도를 만족하는지 알 수 있게 테스트 설계  
   ![](https://velog.velcdn.com/images/euisuk-chung/post/5b131b2c-87a7-4739-8bf9-e452a6fb30f7/image.png)
2. **기능 중심의 제품 사용**: 실제 사용 시나리오를 통한 동작 확인  
   ![](https://velog.velcdn.com/images/euisuk-chung/post/d0bebd5c-e3a1-4e3b-94b0-cadafd583644/image.png)

3. **샘플 기반 검토**: 일부 지표나 데이터를 통한 품질 신뢰 확보  
   ![](https://velog.velcdn.com/images/euisuk-chung/post/afce4a5d-1834-47ec-b3d5-6246498dde28/image.png)

이러한 전략은 코드 라인 단위의 검토보다 훨씬 효율적이며, 특히 AI가 코드를 생성하는 시대에 필수적인 접근 방식입니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/a64e23f5-1912-40da-b256-c797a51ab9d1/image.png)

Schulntz는 강연에서 이렇게 말합니다:

> “Managing implementations that you yourself don’t understand is actually a problem as old as civilization… but we as software engineers are not used to this. We’re used to being ICs who understand the whole stack. But we need to let go of that to become more productive.”

이 말인 즉, 기존의 소프트웨어 개발자는 지금까지 항상 자신이 작성한 코드를 직접 이해하고, 제어하고, 검토하는 것을 전제로 일해왔으나, "AI 코드 생성 시대에는 더 이상 그 방식이 생산적이지 않다"라고 얘기하며 **매니져의 관점으로 업무를 바라보고 수행해야 한다**고 이야기하고 있습니다.

---

프로덕션 관점에서 Vibe Coding 전략
------------------------

### 배경: 기술 부채(Tech Debt)와 AI의 한계

AI를 활용한 Vibe Coding이 점점 강력해지고 있지만, 여전히 사람이 직접 다뤄야 하는 코드의 영역이 존재합니다. 그 핵심 이유 중 하나가 바로 **기술 부채(technical debt)**입니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/0bb72df9-05a2-4653-b332-465a96af8bf3/image.png)

기술 부채란, 빠르게 개발하기 위해 구조적 복잡성이나 장기 유지보수성을 희생하는 선택을 말합니다.

AI가 짠 코드는 기능적으로는 동작하더라도:

* 확장 가능성(extensibility)
* 유지보수의 용이성
* 코드 일관성과 재사용성

같은 비기능적 품질 요건을 충족하지 못하는 경우가 많습니다.

> "Extensibility cannot be verified."  
> → 시스템이 미래에 잘 확장될지를 테스트 코드나 출력만으로 검증하는 것은 거의 불가능합니다.

따라서 AI에게 모든 코드를 맡기기보다는, 기술 부채의 영향을 최소화할 수 있는 영역부터 책임 있게 위임하는 전략이 필요하다고 강연에서 언급합니다.

### 1. Leaf Node 중심 접근

코드베이스를 트리 구조로 보면, **리프 노드(Leaf Node)**는 다른 컴포넌트의 의존을 받지 않는 말단 기능입니다.

* 예: UI의 특정 버튼 동작, 로그 메시지 포맷, 애니메이션 효과 등.

Schulntz는 실제로 **22,000줄 규모의 PR을 Claude가 작성**했으며, 이를 리프 노드에 집중함으로써 안정적으로 배포할 수 있었다고 밝혔습니다.

> “Nothing depends on them. So it’s okay if there’s tech debt in the leaf nodes.”

### 2. 핵심 구조는 여전히 사람이 관리해야 한다

반면 **코드베이스의 중심 구조(트렁크/브랜치)**는 확장성과 안정성을 위해 사람이 직접 유지해야 합니다.

* 여기에 기술 부채(tech debt)가 쌓이면 향후 기능 추가에 큰 제약이 생기기 때문입니다.

### 3. Claude에게 ‘제품 매니저’처럼 설명하라

Vibe Coding에서 인간의 역할은 단순히 "요청자"가 아닌, **Claude의 PM(Product Manager)**가 되는 것입니다.

* AI에게는 코드 요구사항뿐 아니라 맥락, 사용 의도, 비슷한 기능 사례 등을 전달해야 합니다.
* 인간 동료에게 온보딩하듯, **목표, 제약 조건, 구조적 유사성**을 모두 설명해야 성공 확률이 올라갑니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/047eaaca-75ef-42b7-9896-4b550d7ba72f/image.png)

> "Ask not what Claude can do for you, but what you can do for Claude."

---

(사례) 22,000라인 PR을 Claude가 작성한 이유와 방식
------------------------------------

![](https://velog.velcdn.com/images/euisuk-chung/post/d126f2d2-bc1e-4e43-a454-59e6c92b8be4/image.png)

Anthropic의 강화학습 시스템에 통합된 대규모 PR은 다음과 같은 방법으로 안전하게 운영되었습니다:

* **사전 요건 정리**: 단일 프롬프트가 아니라 수일간의 요구사항 정의 및 설계 작업
* **리프 노드 중심 구현**: 영향 범위가 제한적인 부분에 집중
* **테스트 기반 검증**: 입력과 출력만으로 시스템 안정성 확인
* **스트레스 테스트 실행**: 장시간 실행을 통해 안정성 검증

![](https://velog.velcdn.com/images/euisuk-chung/post/29090785-b91f-474c-a9df-0b2ea1beb346/image.png)

덕분에 이 PR은 전통적인 수작업 대비 **수 주 단축된 시간 안에 안전하게** 배포될 수 있었습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/99f95942-4fbc-440b-aea6-e351f5a78e74/image.png)

---

Q&A
===

![](https://velog.velcdn.com/images/euisuk-chung/post/13c096a8-3242-4f70-abfe-082721610314/image.png)

개발자는 이제 어떤 역량을 길러야 하는가?
-----------------------

**1. 코드를 짜는 능력보다 ‘문제 정의 능력’이 중요해진다**

* 앞으로의 개발자는 직접 구현하는 능력보다는, **문제를 구조화하고 AI가 해결할 수 있게 설정하는 능력**이 더 중요해집니다. 즉, 훌륭한 엔지니어는 곧 **훌륭한 AI PM**이 되어야 합니다.

**2. 앞으로는 학습 방식도 달라진다**

* 과거에는 수많은 디버깅과 문서 검색을 통해 학습했다면, 이제는 Claude에게 직접 질문하고, **실시간 피드백을 학습 도구로 삼는 방식**이 일반화될 것입니다.

> "Lazy people will learn nothing. But those who ask the right questions will learn faster than ever."

---

보안을 어떻게 확보할까?
-------------

Schulntz는 프로덕션 보안과 관련된 질문에 대해 다음과 같이 강조했습니다:

* Claude에게 작업을 맡기기 전, **어떤 기능이 보안적으로 민감한지 명확히 인식**해야 합니다.
* 민감한 기능(API 키 처리, 인증, 결제 등)은 사람이 직접 작성하거나, **AI에게 구체적이고 보수적인 프롬프트**를 제공해야 합니다.
* **샌드박스형 프레임워크**나 오프라인 환경에서 AI 코드를 실행함으로써 안전성을 확보할 수 있습니다.

---

실용 워크플로우 가이드
------------

1. **탐색 단계**

   * Claude에게 “이 코드베이스에서 인증은 어디에서 처리되나?” 등 질문
   * 관련 파일, 클래스, 설계 구조를 빠르게 파악
2. **플랜 수립**

   * 구현할 기능을 여러 파일로 분해하고 구조화
   * 적절한 설계 예시 제시 (e.g. "이 기능은 기존 이 모듈을 참고하라")
3. **실행 & 검토**

   * Claude에게 계획 기반으로 작업 수행 요청
   * **최소한의 end-to-end 테스트**부터 확인
   * 필요시 “compact”나 새 세션으로 컨텍스트 리셋

---

결론
==

Vibe Coding은 단순한 유행이 아닙니다. AI의 능력이 지수적으로 성장하는 시대,

* 이를 활용하지 않으면 **개발자가 병목이 되는 상황**이 찾아올 수 있습니다.

**핵심 요약:**

✅ Claude의 PM이 되어라  
✅ 리프 노드부터 Vibe Coding을 실험하라  
✅ 코드가 아니라 제품의 동작을 검증하라  
✅ 테스트 중심, 맥락 중심 개발을 연습하라  
✅ 지수적 성장 곡선에 올라타라 – 지금 준비하지 않으면 늦는다

바이브 코딩 관련해서 재밌게 본 영상을 정리해봤는데요!  
읽어주셔서 감사합니다 😸