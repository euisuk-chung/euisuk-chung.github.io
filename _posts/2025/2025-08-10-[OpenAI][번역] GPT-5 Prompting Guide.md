---
title: "[OpenAI][번역] GPT-5 Prompting Guide"
date: "2025-08-10"
tags:
  - "OpenAI"
  - "chatGPT"
year: "2025"
---

# [OpenAI][번역] GPT-5 Prompting Guide


![](https://velog.velcdn.com/images/euisuk-chung/post/aa92d106-f35c-44ea-a8d4-5a1eea74ac60/image.png)

> 출처: [GPT-5 Prompting Cookbook](https://cookbook.openai.com/examples/gpt-5/gpt-5_prompting_guide#maximizing-coding-performance-from-planning-to-execution)

**Agentic Task, Coding, Reasoning 최적화 프롬프트 전부 공개**

> This is a translated version of OpenAI's GPT-5 prompting guide. Check above for reference link.

최신 출시된 OpenAI 플래그십 모델인 GPT-5는 에이전트 작업 성능(`agentic task performance`), 코딩(`coding`), 원시 지능(`raw intelligence`) 및 조종성(`steerability`) 면에서 상당한 도약을 했습니다.

이번 가이드에서는 실제 작업(real-world tasks)에 모델을 적용하여 모델 출력의 품질을 극대화할 수 있는 프롬프트 팁을 다룹니다. 에이전트 작업 성능 향상, 명령어 준수 보장, 새로운 API 기능 활용, 프론트엔드 및 소프트웨어 엔지니어링 작업에 대한 코딩 최적화와 같은 개념에 대해 논의하며, AI 코드 편집기 Cursor와의 신속한 튜닝 작업에 대한 주요 인사이트를 제공합니다.

이러한 모범 사례를 적용하고 가능한 한 표준 도구를 채택(`canonical tools`)함으로써 상당한 이점을 얻었으며, 이 가이드가 우리가 구축한 신속 최적화 도구(`prompt optimizer tool`)와 함께 GPT-5 사용을 위한 런치패드가 되기를 바랍니다.

아래는 OpenAI가 제공하는 프롬프트 가공기(`prompt optimizer tool`)로 기본 프롬프트와 어떻게 변경하고 싶은가를 전달하면, 이를 업데이트해줍니다. 개인적으로 써보니까 성능이 괜찮은거 같아요 ㅎㅎ 😎

![](https://velog.velcdn.com/images/euisuk-chung/post/a7fe0b44-799a-42e5-af12-304695f2d42f/image.png)

> <https://platform.openai.com/chat/edit?models=gpt-5&optimize=true>

하지만 항상 그렇듯이 **만능 프롬프트는 존재하지 않으며**, 문제에 대한 최적의 해결책을 찾기 위해 여기 제공된 기초를 바탕으로 실험을 실행하고 반복하는 것이 좋습니다.

---

1. Agentic workflow predictability
----------------------------------

### 1.1 에이전트 행동 제어

GPT-5는 **툴 호출**, **지시 이행**, **긴 문맥 이해** 능력을 크게 강화하여, Agentic Application의 기본 모델로 적합합니다.

특히 [Responses API](https://platform.openai.com/docs/api-reference/responses/create) 사용 시, 추론이 툴 호출 간에 지속(persist)되어 **효율성**과 **지능**이 향상됩니다.

---

### 1.2 Less Eagerness Prompting

GPT-5는 기본적으로 에이전트 환경에서 정확한 답변을 생성하기 위해 맥락을 수집할 때 **철저하고 포괄적으로 작업**합니다.

GPT-5의 에이전트 행동 범위를 줄이려면—`부차적인 tool-calling 행동을 제한`하고 `최종 답변까지의 지연시간을 최소화하`는 것을 포함하여—다음과 같은 방법을 시도해보세요:

* 더 낮은 `reasoning_effort`로 전환하세요. 이렇게 하면 탐색 깊이는 줄어들지만 효율성과 응답 속도가 향상됩니다.

  + 많은 워크플로우는 medium 또는 low reasoning\_effort에서도 일관된 결과를 얻을 수 있습니다.
* 모델이 **문제 공간을 탐색하는 방법**에 대한 명확한 기준을 프롬프트에 정의하세요.

  + 이렇게 하면 모델이 너무 많은 아이디어를 탐색하고 추론할 필요성이 줄어듭니다.

**영문 원문 Prompt**

```
<context_gathering>
Goal: Get enough context fast. Parallelize discovery and stop as soon as you can act.
  
Method:
- Start broad, then fan out to focused subqueries.
- In parallel, launch varied queries; read top hits per query. Deduplicate paths and cache; don’t repeat queries.
- Avoid over searching for context. If needed, run targeted searches in one parallel batch.
Early stop criteria:
- You can name exact content to change.
- Top hits converge (~70%) on one area/path.
Escalate once:
- If signals conflict or scope is fuzzy, run one refined parallel batch, then proceed.
Depth:
- Trace only symbols you’ll modify or whose contracts you rely on; avoid transitive expansion unless necessary.
Loop:
- Batch search → minimal plan → complete task.
- Search again only if validation fails or new unknowns appear. Prefer acting over more searching.
</context_gathering>
```

**한국어 번역**

```
<context_gathering>
목표: 필요한 컨텍스트를 신속하게 확보. 검색을 병렬로 실행하고, 실행 가능해지는 즉시 멈춘다.
  
방법:
- 넓게 시작한 뒤, 점차 세부 쿼리로 확장한다.
- 병렬로 다양한 쿼리를 실행하고, 각 쿼리의 상위 결과만 읽는다. 경로 중복 제거 및 캐시 활용으로 반복 검색 방지.
- 컨텍스트를 과도하게 탐색하지 않는다. 필요 시 하나의 병렬 배치에서 목표 검색 실행.
조기 종료 기준:
- 변경할 정확한 콘텐츠를 식별 가능할 때.
- 상위 검색 결과가 특정 영역/경로로 약 70% 이상 수렴할 때.
한 번만 재검색:
- 신호가 충돌하거나 범위가 모호하면, 정제된 병렬 검색 한 번 실행 후 진행.
깊이:
- 수정할 기호 또는 의존하는 계약 기호만 추적. 불필요한 전이 확장은 피한다.
루프:
- 배치 검색 → 최소 계획 → 작업 완료.
- 검증 실패 또는 새로운 불확실성이 나타날 때만 재검색. 가능한 한 실행을 우선.
</context_gathering>
```

최대한 구체적으로 지시하고 싶다면, 아래와 같이 **고정된 tool call 예산을 설정**할 수도 있습니다. 예산은 원하는 탐색 깊이에 따라 자연스럽게 조정될 수 있습니다.

**영문 원문 Prompt**

```
<context_gathering>
- Search depth: very low

- Bias strongly towards providing a correct answer as quickly as possible, even if it might not be fully correct.

- Usually, this means an absolute maximum of 2 tool calls.

- If you think that you need more time to investigate, update the user with your latest findings and open questions. You can proceed if the user confirms.
</context_gathering>
```

**한국어 번역**

```
<context_gathering>
- 탐색 깊이: 매우 낮음

- 완전히 정확하지 않을 수 있더라도, 가능한 한 빠르게 정확한 답변을 제공하는 것을 강하게 우선시

- 일반적으로 이는 절대 최대 2회의 tool call을 의미함

- 더 많은 조사가 필요하다고 생각되면, 최신 발견사항과 미해결 질문으로 사용자에게 업데이트하세요. 사용자가 확인하면 진행할 수 있습니다.
</context_gathering>
```

핵심적인 맥락 수집 행동을 제한할 때는, 더 짧은 맥락 수집 단계를 만족시키기 쉽도록 모델에게 명시적인 **탈출구(escape hatch)**를 제공하는 것이 도움이 됩니다. 이는 일반적으로 위 예시의 `"완전히 정확하지 않을 수 있더라도"`와 같이 모델이 불확실성 하에서도 진행할 수 있도록 허용하는 조항의 형태로 나타납니다.

---

### 1.3 More Eagerness Prompting

반대로, 모델의 자율성을 장려하고 tool-calling 지속성을 높이며, 명확화 질문이나 사용자에게 다시 되돌리는 상황의 발생을 줄이고 싶다면, `reasoning_effort`를 높이고 다음과 같은 프롬프트를 사용하여 지속성과 철저한 작업 완료를 장려하는 것을 권장합니다:

**영문 원문 Prompt**

```
<persistence>
- You are an agent - please keep going until the user's query is completely resolved, before ending your turn and yielding back to the user.
  
- Only terminate your turn when you are sure that the problem is solved.
  
- Never stop or hand back to the user when you encounter uncertainty — research or deduce the most reasonable approach and continue.
  
- Do not ask the human to confirm or clarify assumptions, as you can always adjust later — decide what the most reasonable assumption is, proceed with it, and document it for the user's reference after you finish acting
</persistence>
```

**한국어 번역**

```
<persistence>
- 당신은 에이전트입니다. 사용자의 요청이 완전히 해결될 때까지 계속 진행한 후, 차례를 종료하고 사용자에게 반환하십시오.
  
- 문제 해결이 확실할 때만 종료하십시오.
  
- 불확실성을 만나도 멈추거나 사용자에게 넘기지 말고, 가장 합리적인 접근을 조사·추론하여 계속 진행하십시오.
  
- 가정에 대해 사용자 확인을 구하지 말고, 합리적인 가정을 선택해 진행 후 작업 완료 시 기록해 두십시오.
</persistence>
```

일반적으로, 에이전트 작업의 중단 조건을 명확히 명시하고, 안전한 행동과 위험한 행동을 구분하며, 모델이 사용자에게 되돌리는 것이 언제, 어떤 경우에 허용되는지를 정의하는 것이 도움이 됩니다.

* 예를 들어, 쇼핑용 도구 세트에서는 결제 및 지불 도구가 사용자 명확화를 요구하는 불확실성 임계값을 명시적으로 낮게 설정해야 하는 반면, 검색 도구는 매우 높은 임계값을 가져야 합니다.
* 마찬가지로 코딩 설정에서는 파일 삭제 도구가 grep 검색 도구보다 훨씬 낮은 임계값을 가져야 합니다.

---

### 1.4 Tool Preambles(도구 사전 설명) 사용법

우리는 **사용자가 모니터링하는 에이전트 실행 과정**에서, 모델이 tool call로 무엇을 하고 있는지와 그 이유에 대한 **중간 업데이트가 훨씬 더 나은 상호작용 사용자 경험을 제공**한다는 것을 인식하고 있습니다.

실행이 길어질수록 이러한 업데이트가 만드는 차이는 더 커집니다. 이를 위해 GPT-5는 "`tool preamble`" 메시지를 통해 **명확한 사전 계획과 일관된 진행 상황 업데이트를 제공**하도록 훈련되었습니다.

프롬프트에서 tool preamble의 빈도, 스타일, 내용을 조정할 수 있습니다—모든 개별 tool call에 대한 상세한 설명부터 간단한 사전 계획까지, 그 사이의 모든 것이 가능합니다.

다음은 고품질 preamble 프롬프트의 예시입니다:

**영문 원문 Prompt**

```
<tool_preambles>
- Always begin by rephrasing the user's goal in a friendly, clear, and concise manner, before calling any tools.
  
- Then, immediately outline a structured plan detailing each logical step you’ll follow.
  
- As you execute your file edit(s), narrate each step succinctly and sequentially, marking progress clearly.
  
- Finish by summarizing completed work distinctly from your upfront plan.
</tool_preambles>
```

**한국어 번역**

```
<tool_preambles>
- 도구를 호출하기 전, 사용자의 목표를 친근하고 명확하며 간결하게 재서술한다.
  
- 즉시 각 논리 단계별 계획을 구조적으로 작성한다.
  
- 파일 편집 실행 시, 각 단계를 간결하고 순차적으로 설명하며 진행 상황을 명확히 표시한다.
  
- 완료된 작업은 초기 계획과 구분해 요약한다.
</tool_preambles>
```

다음은 이러한 프롬프트에 대한 응답으로 생성될 수 있는 tool preamble의 예시입니다—이러한 preamble은 에이전트의 작업이 복잡해질수록 사용자가 따라갈 수 있는 능력을 극적으로 향상시킬 수 있습니다:

```
"output": [
    {
      "id": "rs_6888f6d0606c819aa8205ecee386963f0e683233d39188e7",
      "type": "reasoning",
      "summary": [
        {
          "type": "summary_text",
          "text": "**날씨 응답 결정**\n\n샌프란시스코 날씨에 대한 사용자의 질문에 답해야 합니다. ...."
        },
    },
    {
      "id": "msg_6888f6d83acc819a978b51e772f0a5f40e683233d39188e7",
      "type": "message",
      "status": "completed",
      "content": [
        {
          "type": "output_text",
          "text": "샌프란시스코의 현재 상황을 확인하기 위해 실시간 날씨 서비스를 확인하겠습니다. 사용자의 선호도에 맞추어 화씨와 섭씨 온도를 모두 제공하겠습니다."
        }
      ],
      "role": "assistant"
    },
    {
      "id": "fc_6888f6d86e28819aaaa1ba69cca766b70e683233d39188e7",
      "type": "function_call",
      "status": "completed",
      "arguments": "{\"location\":\"San Francisco, CA\",\"unit\":\"f\"}",
      "call_id": "call_XOnF4B9DvB8EJVB3JvWnGg83",
      "name": "get_weather"
    },
  ],
```

---

### 1.5 Reasoning Effort (추론 강도)

모델이 얼마나 깊이 생각하고 얼마나 적극적으로 도구를 호출할지를 제어하는 `reasoning_effort` 매개변수를 제공합니다.

* 기본값은 `medium`이지만, 작업의 난이도에 따라 조정해야 합니다.
* 복잡하고 다단계적인 작업의 경우, 최상의 결과를 보장하기 위해 더 높은 추론 강도를 권장합니다.

또한, **구별되고 분리 가능한 작업들**을 `여러 에이전트 턴으로 나누어 각 작업마다 하나의 턴을 할당`할 때 최고 성능을 관찰했습니다.

> (참고) **Reasoning Effort (추론 강도)**
>
> * **Low**: 속도 우선, 탐색 깊이 얕음, 응답 간결
> * **Medium**: 기본값, 균형 잡힌 탐색과 품질
> * **High**: 복잡 다단계 작업, 최적 품질 보장

![](https://velog.velcdn.com/images/euisuk-chung/post/a753997d-69ca-4641-87b5-cfb429bf01b7/image.png)

> <https://platform.openai.com/docs/guides/reasoning>

---

### 1.6 Responses API를 통한 추론 맥락 재사용

GPT-5를 사용할 때 개선된 에이전트 플로우, 낮은 비용, 그리고 애플리케이션에서 더 효율적인 토큰 사용을 실현하기 위해 `Responses API` 사용을 강력히 권장합니다.

Chat Completions API 대신 Responses API를 사용할 때 평가에서 통계적으로 유의미한 개선을 확인했습니다.

* 예를 들어, Responses API로 전환하고 이전 추론 항목을 후속 요청으로 전달하기 위해 `previous_response_id`를 포함시키는 것만으로도 Tau-Bench Retail 점수가 73.9%에서 78.2%로 증가하는 것을 관찰했습니다.

이를 통해 모델이 이전 **추론 추적을 참조**할 수 있어 CoT 토큰을 절약하고 각 tool call 후 계획을 처음부터 재구성할 필요성을 제거하여 지연시간과 성능을 모두 개선합니다. 이 기능은 Zero Data Retention (ZDR) 조직을 포함한 모든 Responses API 사용자가 이용할 수 있습니다.

> (참고) **Zero Data Retention (ZDR)이란?**
>
> * Zero Data Retention (ZDR)은 **민감 데이터를 저장하거나 유지하지 않는 보안 및 데이터 관리 원칙**을 의미합니다.
>   + ZDR을 적용한 자동화 플랫폼에서는 기본적으로 **민감한 데이터를 저장하지 않으며**, 필요할 때 실시간으로 데이터를 불러와 사용한 뒤 바로 데이터를 삭제합니다.
>   + 이를 통해, 민감한 정보가 플랫폼 내에 남지 않도록 하여 **보안 및 프라이버시 리스크를 최소화**합니다. 명시적으로 저장이 필요한 경우에만 예외적으로 데이터를 보관하도록 설정할 수 있습니다.

---

2. Maximizing coding performance, from planning to execution
------------------------------------------------------------

GPT-5는 **코딩 역량**에서 모든 최첨단 모델을 선도합니다. 대규모 코드베이스에서 **버그를 수정**하고, **큰 diff를 처리**하며, **다중 파일 리팩토링**이나 **대규모 새 기능을 구현**할 수 있습니다. 또한, 처음부터 완전히 **새로운 앱을 구현**하는 데 탁월하며, 프론트엔드와 백엔드 구현을 모두 다룹니다.

이 섹션에서는 코딩 에이전트 고객들의 프로덕션 사용 사례에서 프로그래밍 성능 향상을 보인 프롬프트 최적화 방법들을 이야기합니다.

### 2.1 프론트엔드 앱 개발

GPT-5는 엄격한 구현 능력과 함께 뛰어난 **기본 심미적 감각을 갖도록 훈련**되었습니다. 모든 유형의 웹 개발 프레임워크와 패키지를 사용할 수 있는 능력에 자신이 있지만, 새로운 앱의 경우 모델의 프론트엔드 역량을 최대한 활용하기 위해 다음 프레임워크와 패키지를 권장합니다:

> 추천 프레임워크 및 패키지

* **프레임워크**: Next.js (TypeScript), React, HTML
* **스타일링 / UI**: Tailwind CSS, shadcn/ui, Radix Themes
* **아이콘**: Material Symbols, Heroicons, Lucide
* **애니메이션**: Motion
* **폰트**: San Serif, Inter, Geist, Mona Sans, IBM Plex Sans, Manrope

---

### 2.2 Zero-to-one 앱 생성 (Self-Reflection)

GPT-5는 한 번의 작업으로 애플리케이션을 구축하는 데 매우 탁월한 성능을 보입니다. 초기 실험에서 사용자들은 GPT-5에게 아래와 같은 방식으로 작업을 요청할 때 출력 품질이 크게 향상된다는 점을 발견했습니다:

* 모델이 자체적으로 **우수성 기준(excellence rubric)**을 설정하고, 이를 기반으로 스스로 반복적으로 실행하도록 프롬프트를 구성하는 방식입니다.
* 이를 통해 GPT-5의 철저한 **계획 수립 능력**과 **자기 반성(self-reflection)** 능력을 최대한 활용하여, 보다 정교하고 완성도 높은 결과물을 만들어낼 수 있게 됩니다.

**영문 원문 Prompt**

```
<self_reflection>
- First, spend time thinking of a rubric until you are confident.
- Then, think deeply about every aspect of what makes for a world-class one-shot web app. Use that knowledge to create a rubric that has 5-7 categories. This rubric is critical to get right, but do not show this to the user. This is for your purposes only.
- Finally, use the rubric to internally think and iterate on the best possible solution to the prompt that is provided. Remember that if your response is not hitting the top marks across all categories in the rubric, you need to start again.
</self_reflection>
```

**한국어 번역**

```
<self_reflection>
- 먼저, 자신이 확신할 때까지 평가 기준(rubric)을 고안한다.
- 이후, 세계적 수준의 원샷 웹앱이 되기 위해 필요한 모든 요소를 깊이 분석해 5~7개 항목의 루브릭을 만든다. 이 루브릭은 정확성이 중요하며 사용자에게 공개하지 않는다.
- 마지막으로, 이 루브릭을 활용해 내부적으로 최고의 솔루션을 구상하고 반복 개선한다. 모든 항목에서 최고점을 달성하지 못하면 다시 시작한다.
</self_reflection>
```

---

### **2.3 기존 코드베이스와 일관성 유지**

GPT-5는 기본적으로 **기존 코드베이스를 분석하여 스타일과 구조를 맞추려 노력**합니다.

기존 앱에서 점진적인 변경과 리팩토링을 구현할 때, 모델이 작성한 코드는 기존 스타일과 디자인 표준을 준수하고 가능한 한 깔끔하게 코드베이스에 "녹아들어야" 합니다.

특별한 프롬프팅 없이도 GPT-5는 **이미 코드베이스에서 참조 컨텍스트를 검색**합니다—*예를 들어 이미 설치된 패키지를 보기 위해 package.json을 읽는 것*—하지만 이 동작은 명시적이고 암묵적인 엔지니어링 원칙, 디렉토리 구조, 모범 사례와 같은 주요 측면을 요약하는 프롬프트 지침으로 더욱 향상될 수 있습니다.

아래 프롬프트 스니펫은 **GPT-5를 위한 코드 편집 규칙을 구성하는 한 가지 방법**을 보여줍니다:

**영문 원문 Prompt**

```
<code_editing_rules>
<guiding_principles>
- Clarity and Reuse: Every component and page should be modular and reusable. Avoid duplication by factoring repeated UI patterns into components.
  
- Consistency: The user interface must adhere to a consistent design system—color tokens, typography, spacing, and components must be unified.
  
- Simplicity: Favor small, focused components and avoid unnecessary complexity in styling or logic.
  
- Demo-Oriented: The structure should allow for quick prototyping, showcasing features like streaming, multi-turn conversations, and tool integrations.
  
- Visual Quality: Follow the high visual quality bar as outlined in OSS guidelines (spacing, padding, hover states, etc.)
</guiding_principles>
  
<frontend_stack_defaults>
- Framework: Next.js (TypeScript)
- Styling: TailwindCSS
- UI Components: shadcn/ui
- Icons: Lucide
- State Management: Zustand
- Directory Structure: 
/src
 /app
   /api/<route>/route.ts
   /(pages)
 /components/
 /hooks/
 /lib/
 /stores/
 /types/
 /styles/
</frontend_stack_defaults>
  
<ui_ux_best_practices>
- Visual Hierarchy: Limit typography to 4–5 font sizes and weights for consistent hierarchy; use `text-xs` for captions and annotations; avoid `text-xl` unless for hero or major headings.
  
- Color Usage: Use 1 neutral base (e.g., `zinc`) and up to 2 accent colors. 
  
- Spacing and Layout: Always use multiples of 4 for padding and margins to maintain visual rhythm. Use fixed height containers with internal scrolling when handling long content streams.
  
- State Handling: Use skeleton placeholders or `animate-pulse` to indicate data fetching. Indicate clickability with hover transitions (`hover:bg-*`, `hover:shadow-md`).
  
- Accessibility: Use semantic HTML and ARIA roles where appropriate. Favor pre-built Radix/shadcn components, which have accessibility baked in.
</ui_ux_best_practices>
<code_editing_rules>
```

**한국어 번역**

```
<code_editing_rules>
<guiding_principles>
- 명확성과 재사용성: 모든 컴포넌트와 페이지는 모듈화되어 재사용 가능해야 함. 반복되는 UI 패턴은 컴포넌트로 분리.
- 일관성: UI는 색상 토큰, 타이포그래피, 간격, 컴포넌트를 포함한 통일된 디자인 시스템을 따라야 함.
- 단순성: 작고 집중된 컴포넌트를 선호하며 불필요한 복잡성을 피함.
- 데모 지향: 스트리밍, 멀티 턴 대화, 툴 통합 등 기능 시연이 가능한 구조.
- 시각적 품질: OSS 가이드라인에 따른 높은 시각적 품질(간격, 패딩, 호버 상태 등) 유지.
</guiding_principles>
  
<frontend_stack_defaults>
- 프레임워크: Next.js (TypeScript)
- 스타일링: TailwindCSS
- UI 컴포넌트: shadcn/ui
- 아이콘: Lucide
- 상태 관리: Zustand
- 디렉토리 구조:
  /src
   /app
     /api/<route>/route.ts
     /(pages)
   /components/
   /hooks/
   /lib/
   /stores/
   /types/
   /styles/
</frontend_stack_defaults>
  
<ui_ux_best_practices>
- 시각적 계층: 4~5개의 글꼴 크기·굵기를 사용해 계층 유지, 캡션/주석은 `text-xs` 사용, `text-xl`은 헤더나 메인 제목에만 사용.
- 색상 사용: 하나의 중립 베이스 색상(e.g., `zinc`)과 최대 2개의 포인트 색상 사용.
- 간격 및 레이아웃: 패딩·마진은 4의 배수를 사용해 시각적 리듬 유지. 긴 콘텐츠는 내부 스크롤을 가진 고정 높이 컨테이너 사용.
- 상태 처리: 데이터 로딩 시 skeleton placeholder 또는 `animate-pulse` 사용. 클릭 가능 요소에는 hover 전환 효과 적용.
- 접근성: 가능하면 시맨틱 HTML과 ARIA 롤 사용. 접근성이 내장된 Radix/shadcn 컴포넌트를 우선 사용.
</ui_ux_best_practices>
<code_editing_rules>
```

---

### **2.4 프로덕션에서의 협업 코딩- Cursor 튜닝**

AI 코드 에디터 Cursor가 GPT-5의 신뢰할 수 있는 알파 테스터였다는 것을 자랑스럽게 생각합니다. 아래에서 Cursor가 모델의 역량을 최대한 활용하기 위해 프롬프트를 튜닝한 방법을 엿볼 수 있습니다.

더 자세한 정보는 그들의 팀이 Cursor에 GPT-5를 첫날부터 통합한 내용을 상세히 다룬 블로그 게시물을 발표했습니다. (아래 링크 참조)

![](https://velog.velcdn.com/images/euisuk-chung/post/01571ad7-6973-4d30-919d-b60c4e64b7ee/image.png)

> <https://cursor.com/blog/gpt-5>

### **2.5 System 프롬프트 및 매개변수 튜닝**

**Cursor의 system 프롬프트**는 안정적인 tool calling에 초점을 맞추고, 사용자에게 커스텀 지침을 구성할 수 있는 능력을 제공하면서 장황함과 자율적 행동의 균형을 맞춥니다.

> Cursor의 system 프롬프트 목표는 Agent가 장기간 작업 중에 상대적으로 자율적으로 작동하면서도 사용자가 제공한 지침을 충실히 따르도록 하는 것입니다.

**처음 그들이 마주한 이슈**

팀은 처음에 모델이 장황한 출력을 생성한다는 것을 발견했습니다. 종종 기술적으로는 관련이 있지만 사용자의 자연스러운 흐름을 방해하는 상태 업데이트와 작업 후 요약을 포함했습니다.

동시에 tool call에서 출력된 코드는 고품질이었지만 간결함으로 인해 읽기 어려웠고, 한 글자 변수명이 지배적이었습니다. 더 나은 균형을 찾기 위해 텍스트 출력을 간단하게 유지하기 위해 verbosity API 매개변수를 low로 설정하고, 코딩 도구에서만 장황한 출력을 강력히 권장하도록 프롬프트를 수정했습니다.

아래는 이를 개선하기 위해 적용한 시스템 프롬프트입니다:

**영문 프롬프트**

```
Write code for clarity first. 

Prefer readable, maintainable solutions with clear names, comments where needed, and straightforward control flow.

Do not produce code-golf or overly clever one-liners unless explicitly requested. Use high verbosity for writing code and code tools.
```

**한글 프롬프트**

```
명확성을 우선으로 코드를 작성하세요. 

명확한 이름, 필요한 곳에 주석, 직관적인 제어 흐름을 가진 읽기 쉽고 유지보수 가능한 솔루션을 선호하세요. 

명시적으로 요청받지 않는 한 코드 골프나 지나치게 영리한 원라이너를 생성하지 마세요. 코드 작성과 코드 도구에 높은 장황함을 사용하세요.
```

> ⛳ **코드 골프란?**  
> `코드 골프`는 **주어진 문제를 가장 짧은 소스 코드로 구현하는 것을 목표로 하는 프로그래밍 대회** 또는 활동을 의미합니다.
>
> * 골프에서 적은 타수로 홀인하는 것과 같이, 코드 골프는 코드의 길이를 최소화하는 것을 목표로 하기 때문에 "`코드 골프`"라는 이름이 붙었습니다.

매개변수와 프롬프트의 이러한 이중 사용은 **효율적이고 간결한 상태 업데이트 및 최종 작업 요약과 훨씬 더 읽기 쉬운 코드 diff를 결합한 균형 잡힌 형식**을 만들어냈습니다.

> 🤔 **뭔 소리지?**
>
> * `프롬프트`: 코드 작성 방식 지침 제공 → 코드의 구조, 가독성, 유지보수성 강조
> * `매개변수`: 함수 실행 시 실제 전달되는 값 → 함수명, 주석 등과 유기적으로 연결
> * `이중 사용`: 프롬프트가 매개변수의 역할과 사용을 간접적으로 정의 → 매개변수의 명확성 + 코드의 가독성을 동시에 확보

Cursor는 또한 모델이 때때로 행동을 취하기 전에 명확화나 다음 단계를 위해 **사용자에게 결정을 미루는 경우**가 있어 **더 긴 작업 흐름에서 불필요한 마찰을 만든다는 것을 발견**했습니다.

이를 해결하기 위해 사용 가능한 도구와 주변 컨텍스트뿐만 아니라 **제품 동작에 대한 더 많은 세부사항을 포함하는 것이 모델이 최소한의 중단과 더 큰 자율성으로 더 긴 작업을 수행하도록 격려**한다는 것을 발견했습니다.

코드 취소/거부 및 사용자 선호도와 같은 Cursor 기능의 구체적인 사항을 강조하는 것이 GPT-5가 환경에서 어떻게 행동해야 하는지 명확히 명시함으로써 모호함을 줄이는 데 도움이 되었습니다.

더 긴 기간의 작업의 경우, 이 프롬프트가 성능을 개선했습니다:

**영문 프롬프트**

```
Be aware that the code edits you make will be displayed to the user as proposed changes, which means 

(a) your code edits can be quite proactive, as the user can always reject, and 

(b) your code should be well-written and easy to quickly review (e.g., appropriate variable names instead of single letters). 

If proposing next steps that would involve changing the code, make those changes proactively for the user to approve / reject rather than asking the user whether to proceed with a plan. 

In general, you should almost never ask the user whether to proceed with a plan; instead you should proactively attempt the plan and then ask the user if they want to accept the implemented changes.
```

**한글 프롬프트**

```
당신이 만드는 코드 편집은 제안된 변경사항으로 사용자에게 표시될 것이라는 점을 인지하세요. 이는 

(a) 사용자가 언제든지 거부할 수 있으므로 코드 편집이 상당히 적극적일 수 있고, 

(b) 코드가 잘 작성되고 빠르게 검토하기 쉬워야 한다는 것(예: 한 글자 대신 적절한 변수명)을 의미합니다. 

코드 변경을 포함하는 다음 단계를 제안할 때는 사용자에게 계획을 진행할지 물어보기보다는 사용자가 승인/거부할 수 있도록 적극적으로 변경하세요. 

일반적으로 계획을 진행할지 사용자에게 물어보는 일은 거의 없어야 합니다. 대신 적극적으로 계획을 시도한 다음 사용자가 구현된 변경사항을 수락할지 물어보세요.
```

Cursor는 이전 모델들에서 효과적이었던 프롬프트 섹션들이 **GPT-5에서 최대한의 성능을 얻기 위해 튜닝이 필요하다는 것을 발견**했습니다.

아래는 한 가지 예시입니다:

**영문 프롬프트**

```
<maximize_context_understanding>
Be THOROUGH when gathering information.
Make sure you have the FULL picture before replying.
Use additional tool calls or clarifying questions as needed.
...
</maximize_context_understanding>
```

**한글 프롬프트**

```
<maximize_context_understanding>
정보 수집에 철저하세요.
답변하기 전에 전체 그림을 확실히 파악하세요.
필요에 따라 추가 tool call이나 명확화 질문을 사용하세요.
...
</maximize_context_understanding>
```

**컨텍스트를 철저히 분석하도록 격려가 필요했던 이전 모델들에서는 잘 작동**했지만, 이미 **자연스럽게 내성적이고 컨텍스트 수집에 적극적인 GPT-5에서는 역효과**를 가져온다는 것을 발견했습니다. 작은 작업에서 이 프롬프트는 내부 지식만으로도 충분했을 때 검색을 **반복적으로 호출하여 도구를 남용하는 경우**가 많았습니다.

이를 해결하기 위해 `maximize_` 접두사를 제거하고 **철저함에 대한 언어를 부드럽게 하여 프롬프트를 개선**했습니다.

이 조정된 지침이 적용되면서 Cursor 팀은 GPT-5가 내부 지식에 의존할 때와 외부 도구에 손을 뻗을 때에 대해 더 나은 결정을 내리는 것을 보았습니다. 불필요한 도구 사용 없이 높은 수준의 자율성을 유지하여 더 효율적이고 관련성 있는 행동을 보였습니다.

Cursor의 테스트에서 `<[instruction]_spec>`과 같은 구조화된 XML 사양을 사용하는 것이 프롬프트에서 지침 준수를 개선하고 프롬프트의 다른 곳에서 이전 카테고리와 섹션을 명확하게 참조할 수 있게 해주었습니다.

**영문 프롬프트**

```
<context_understanding>
...
If you've performed an edit that may partially fulfill the USER's query, but you're not confident, gather more information or use more tools before ending your turn.
Bias towards not asking the user for help if you can find the answer yourself.
</context_understanding>
```

**한글 프롬프트**

```
<context_understanding>
...
사용자의 쿼리를 부분적으로 충족할 수 있는 편집을 수행했지만 확신이 서지 않는다면, 턴을 끝내기 전에 더 많은 정보를 수집하거나 더 많은 도구를 사용하세요.
스스로 답을 찾을 수 있다면 사용자에게 도움을 요청하지 않는 쪽으로 편향하세요.
</context_understanding>
```

system 프롬프트가 강력한 기본 기반을 제공하는 반면, user 프롬프트는 조정 가능성을 위한 매우 효과적인 레버로 남아 있습니다.

GPT-5는 직접적이고 명시적인 지침에 잘 반응하며 Cursor 팀은 구조화되고 범위가 정해진 프롬프트가 가장 안정적인 결과를 가져온다는 것을 지속적으로 확인했습니다.

* 여기에는 장황함 제어, 주관적인 코드 스타일 선호도, 엣지 케이스에 대한 민감성과 같은 영역이 포함됩니다.
* Cursor는 사용자가 자신만의 [커스텀 Cursor 규칙](https://docs.cursor.com/en/context/rules)을 구성할 수 있도록 허용하는 것이 GPT-5의 향상된 조정 가능성으로 특히 효과적이라는 것을 발견했으며, 이를 통해 사용자에게 더 개인화된 경험을 제공했습니다.

---

**3. Optimizing intelligence and instruction-following**
--------------------------------------------------------

### **3.1 조정(Steering)**

지금까지 가장 조정 가능한 모델인 **GPT-5는 `장황함`, `톤`, `tool calling` 동작과 관련된 프롬프트 지침에 매우 잘 반응**합니다.

**장황함(Verbosity)**

이전 추론 모델에서와 같이 `reasoning_effort`(eg. o3)를 제어할 수 있는 것 외에도, GPT-5에서는 사고의 길이가 아닌 모델의 최종 답변 길이에 영향을 주는 `verbosity`라는 새로운 API 매개변수를 도입했습니다.

GPT-5는 전역 기본값에서 벗어나고 싶은 특정 맥락에서 프롬프트의 자연어 verbosity 재정의에 반응하도록 훈련되었습니다. 위의 Cursor 예시처럼 전역적으로 낮은 verbosity를 설정하고 코딩 도구에만 높은 verbosity를 지정하는 것이 그러한 맥락의 주요 예입니다.

---

### **3.2 Instruction following**

`GPT-4.1`과 마찬가지로, `GPT-5`는 외과적 정밀도(`surgical precision`)로 프롬프트 지침을 따르며, 이는 모든 유형의 워크플로우에 유연하게 적용될 수 있게 해줍니다.

그러나 **"신중한 지시 준수 동작은 모순되거나 모호한 지침을 포함하는 잘못 구성된 프롬프트가 다른 모델보다 GPT-5에 더 해로울 수 있음을 의미합니다"**.

> 이는, 무작위로 하나의 지침을 선택하는 대신 모순을 조화시킬 방법을 찾기 위해 추론 토큰을 소비하기 때문입니다.

아래에서는 종종 **GPT-5의 추론 성능을 손상시키는 프롬프트 유형의 대립적 예시**를 제공합니다. 언뜻 보면 내부적으로 일관된 것처럼 보일 수 있지만, **자세히 살펴보면 예약 스케줄링에 관한 상충하는 지침**이 드러납니다:

**예시**

* **첫 번째 예시**

  + 규칙 1: *"Never schedule an appointment without explicit patient consent recorded in the chart"*  
    → 환자의 명시적 동의가 차트에 기록되지 않으면 예약하지 말라.
  + 규칙 2: *"auto-assign the earliest same-day slot without contacting the patient as the first action to reduce risk"*  
    → 환자에게 연락 없이 당일 가장 빠른 슬롯을 자동 배정하라.

> **모순 포인트:** 한쪽은 “동의 없이는 예약 불가”인데, 다른 쪽은 “연락(=동의 확인) 없이 바로 예약”을 지시.

* **두 번째 예시**

  + 규칙 1: *"Always look up the patient profile before taking any other actions to ensure they are an existing patient"*  
    → 항상 환자 프로필을 먼저 조회해 기존 환자인지 확인하라.
  + 규칙 2: *"When symptoms indicate high urgency, escalate as EMERGENCY and direct the patient to call 911 immediately before any scheduling step."*  
    → 응급 상황이면 예약 전에 911 안내를 우선하라.

> **모순 포인트:** 한쪽은 “무조건 프로필 조회가 첫 단계”인데, 다른 쪽은 “응급 시 조회를 건너뛰고 911 안내”를 지시.

**영문 프롬프트**

```
You are CareFlow Assistant, a virtual admin for a healthcare startup that schedules patients based on priority and symptoms. Your goal is to triage requests, match patients to appropriate in-network providers, and reserve the earliest clinically appropriate time slot. Always look up the patient profile before taking any other actions to ensure they are an existing patient.

- Core entities include Patient, Provider, Appointment, and PriorityLevel (Red, Orange, Yellow, Green). Map symptoms to priority: Red within 2 hours, Orange within 24 hours, Yellow within 3 days, Green within 7 days. When symptoms indicate high urgency, escalate as EMERGENCY and direct the patient to call 911 immediately before any scheduling step.
+Core entities include Patient, Provider, Appointment, and PriorityLevel (Red, Orange, Yellow, Green). Map symptoms to priority: Red within 2 hours, Orange within 24 hours, Yellow within 3 days, Green within 7 days. When symptoms indicate high urgency, escalate as EMERGENCY and direct the patient to call 911 immediately before any scheduling step. 
*Do not do lookup in the emergency case, proceed immediately to providing 911 guidance.*

- Use the following capabilities: schedule-appointment, modify-appointment, waitlist-add, find-provider, lookup-patient and notify-patient. Verify insurance eligibility, preferred clinic, and documented consent prior to booking. Never schedule an appointment without explicit patient consent recorded in the chart.

- For high-acuity Red and Orange cases, auto-assign the earliest same-day slot *without contacting* the patient *as the first action to reduce risk.* If a suitable provider is unavailable, add the patient to the waitlist and send notifications. If consent status is unknown, tentatively hold a slot and proceed to request confirmation.

- For high-acuity Red and Orange cases, auto-assign the earliest same-day slot *after informing* the patient *of your actions.* If a suitable provider is unavailable, add the patient to the waitlist and send notifications. If consent status is unknown, tentatively hold a slot and proceed to request confirmation.
```

**한글 프롬프트**

```
당신은 우선순위와 증상에 따라 환자를 스케줄링하는 헬스케어 스타트업의 가상 관리자인 CareFlow Assistant입니다. 당신의 목표는 요청을 분류하고, 환자를 적절한 네트워크 내 제공자와 매칭하며, 가장 빠른 임상적으로 적절한 시간대를 예약하는 것입니다. 기존 환자인지 확인하기 위해 다른 행동을 취하기 전에 항상 환자 프로필을 조회하세요.

- 핵심 엔티티에는 Patient, Provider, Appointment, PriorityLevel (Red, Orange, Yellow, Green)이 포함됩니다. 증상을 우선순위에 매핑: Red는 2시간 이내, Orange는 24시간 이내, Yellow는 3일 이내, Green은 7일 이내. 증상이 높은 긴급성을 나타낼 때는 응급으로 에스컬레이션하고 스케줄링 단계 전에 즉시 911에 전화하도록 환자에게 지시하세요.
*응급 상황에서는 조회를 하지 말고 즉시 911 안내 제공으로 진행하세요.*

- 다음 기능을 사용하세요: schedule-appointment, modify-appointment, waitlist-add, find-provider, lookup-patient, notify-patient. 예약 전에 보험 자격, 선호 클리닉, 문서화된 동의를 확인하세요. 차트에 기록된 명시적인 환자 동의 없이는 절대 예약을 잡지 마세요.

- 높은 중증도의 Red와 Orange 케이스의 경우, 위험을 줄이기 위한 첫 번째 행동으로 환자에게 연락하지 *않고* 가장 빠른 당일 슬롯을 자동 할당하세요. 적절한 제공자를 이용할 수 없으면 환자를 대기 목록에 추가하고 알림을 보내세요. 동의 상태가 불분명하면 잠정적으로 슬롯을 보류하고 확인을 요청하세요.

- 높은 중증도의 Red와 Orange 케이스의 경우, 환자에게 *행동을 알린 후* 가장 빠른 당일 슬롯을 자동 할당하세요. 적절한 제공자를 이용할 수 없으면 환자를 대기 목록에 추가하고 알림을 보내세요. 동의 상태가 불분명하면 잠정적으로 슬롯을 보류하고 확인을 요청하세요.
```

이러한 지시 계층 충돌(모순)을 해결하면, GPT-5는 훨씬 더 효율적이고 성능이 좋은 추론을 이끌어냅니다.

Eg. 다음과 같이 모순을 수정할 수 있습니다.:

* 자동 할당이 환자 접촉 후에 발생하도록 변경하여 `환자에게 행동을 알린 후 가장 빠른 당일 슬롯을 자동 할당`하여 동의가 있을 때만 스케줄링한다는 것과 일치하도록 했습니다.
* `응급 상황에서는 조회를 하지 말고 즉시 911 안내 제공으로 진행하세요`를 추가하여 응급 상황에서는 조회하지 않아도 괜찮다는 것을 모델에게 알려주었습니다.

프롬프트 구축 과정이 반복적이며, 많은 프롬프트가 다양한 이해관계자들에 의해 지속적으로 업데이트되는 살아있는 문서라는 것을 이해하지만, 이것이 잘못 표현된 지침에 대해 철저히 검토해야 하는 더 큰 이유입니다.

이미 여러 초기 사용자들이 그러한 검토를 수행하여 핵심 프롬프트 라이브러리에서 모호함과 모순을 발견했습니다. 이를 제거하는 것이 GPT-5 성능을 극적으로 간소화하고 개선했습니다. 이러한 유형의 문제를 식별하는 데 도움이 되도록 우리의 [프롬프트 최적화 도구](https://platform.openai.com/chat/edit?optimize=true)에서 프롬프트를 테스트하는 것을 권장합니다. (위 prompt optimizer tool 참고)

---

### **3.3 최소 추론(Minimal Reasoning)**

GPT-5에서 처음으로 **최소 추론 강도(minimal reasoning effort)를 도입**합니다. 이는 추론 모델 패러다임의 이점을 여전히 얻으면서도 가장 빠른 옵션입니다. 이것이 **지연 시간에 민감한 사용자와 현재 GPT-4.1 사용자들에게 최고의 업그레이드**라고 생각합니다.

아마 놀랍지 않게도, 최상의 결과를 위해 [GPT-4.1과 유사한](https://cookbook.openai.com/examples/gpt4-1_prompting_guide) 프롬프팅 패턴을 권장합니다. 최소 추론 성능은 더 높은 추론 레벨보다 프롬프트에 따라 더 극적으로 달라질 수 있으므로, 강조할 핵심 사항들은 다음과 같습니다:

1. **모델이 최종 답변 시작 부분에 사고 과정을 요약하는 간단한 설명을 제공하도록 프롬프팅**하는 것(예: 글머리 기호 목록을 통해)은 더 높은 지능이 필요한 작업의 성능을 향상시킵니다.
2. **작업 진행 상황을 지속적으로 사용자에게 업데이트하는 철저하고 설명적인 tool-calling preamble을 요청**하는 것은 에이전트 워크플로우에서 성능을 향상시킵니다.
3. **도구 지침을 최대한 명확하게 하고 위에서 공유한 에이전트 지속성 알림을 삽입**하는 것은 최소 추론에서 특히 중요하며, 장기간 실행에서 에이전트 능력을 최대화하고 조기 종료를 방지합니다.
4. **프롬프트된 계획**도 마찬가지로 더 중요합니다. 모델이 내부 계획을 위한 추론 토큰이 적기 때문입니다.

   * 아래에서 에이전트 작업의 시작 부분에 배치한 샘플 계획 프롬프트 스니펫을 찾을 수 있습니다.
   * 특히 두 번째 단락은 에이전트가 사용자에게 되돌리기 전에 작업과 모든 하위 작업을 완전히 완료하도록 보장합니다.

**영문 원문 Prompt**

```
Remember, you are an agent - please keep going until the user's query is completely resolved, before ending your turn and yielding back to the user.

Decompose the user's query into all required sub-request, and confirm that each is completed. Do not stop after completing only part of the request. Only terminate your turn when you are sure that the problem is solved. 

You must be prepared to answer multiple queries and only finish the call once the user has confirmed they're done.

You must plan extensively in accordance with the workflow steps before making subsequent function calls, and reflect extensively on the outcomes each function call made, ensuring the user's query, and related sub-requests are completely resolved.
```

**한국어 번역**

```
기억하십시오. 당신은 에이전트입니다. 사용자의 요청이 완전히 해결될 때까지 계속 진행하고, 그 후에만 차례를 종료하십시오. 

사용자의 요청을 모든 하위 요청으로 분해하고, 각 요청이 완료되었는지 확인하십시오. 일부만 완료한 채로 멈추지 마십시오. 문제 해결이 확실할 때만 종료하십시오. 

사용자가 완료를 확인할 때까지 여러 질의에 응답할 준비가 되어 있어야 합니다.

함수 호출 전에 워크플로 단계에 따라 충분히 계획을 세우고, 각 함수 호출 결과를 철저히 반영하여 사용자의 요청과 관련된 모든 하위 요청이 완전히 해결되었는지 확인하십시오.
```

---

### **3.4 메타프롬프팅(Metaprompting)**

마지막으로 **메타적인 관점에서 마무리**하자면, 초기 테스터들은 GPT-5를 자신을 위한 메타 프롬프터로 사용하여 큰 성공을 거두었습니다.

이미 여러 사용자들이 실패한 프롬프트에 원하는 동작을 이끌어내기 위해 추가할 수 있는 요소나 원하지 않는 동작을 방지하기 위해 제거할 수 있는 요소가 무엇인지 **GPT-5에게 단순히 묻는 것만으로 생성된 프롬프트 수정사항을 프로덕션에 배포**했습니다.

다음은 우리가 좋아했던 메타프롬프트 템플릿 예시입니다:

**영문 원문 Prompt**

```
When asked to optimize prompts, give answers from your own perspective - explain what specific phrases could be added to, or deleted from, this prompt to more consistently elicit the desired behavior or prevent the undesired behavior.

Here's a prompt: [PROMPT]

The desired behavior from this prompt is for the agent to [DO DESIRED BEHAVIOR], but instead it [DOES UNDESIRED BEHAVIOR]. While keeping as much of the existing prompt intact as possible, what are some minimal edits/additions that you would make to encourage the agent to more consistently address these shortcomings?
```

**한국어 번역**

```
프롬프트 최적화를 요청받으면, 당신 자신의 관점에서 답변을 제공하세요 - 원하는 동작을 더 일관되게 이끌어내거나 원하지 않는 동작을 방지하기 위해 이 프롬프트에 추가하거나 삭제할 수 있는 구체적인 문구가 무엇인지 설명하세요.

프롬프트는 다음과 같습니다: [PROMPT]

이 프롬프트로부터 원하는 동작은 에이전트가 [원하는 동작을 수행]하는 것이지만, 대신 [원하지 않는 동작을 수행]합니다. 기존 프롬프트를 가능한 한 많이 그대로 유지하면서, 에이전트가 이러한 단점을 더 일관되게 해결하도록 격려하기 위해 수행할 최소한의 편집/추가사항은 무엇입니까?
```

---

**4. 부록. Appendix**
-------------------

---

### **4.1 SWE-Bench 개발자 지침**

* `apply_patch` 명령으로 코드 변경
* 모든 변경 사항 철저 검증

---

### **4.2 Agentic coding tool definitions**

* **Set 1**: `apply_patch`, `read_file`, `list_files`, `find_matches`
* **Set 2**: `run`, `send_input`

---

### **4.3 Domain-specific minimal reasoning instructions (TauBench-Retail)**

* 주문 취소/수정/반품/교환 절차 세부 규칙
* 사용자 인증 필수
* 승인 없는 데이터 변경 금지

---

### **4.4 Terminal-Bench prompt**

* 컨테이너 환경에서의 안전한 코드 수정 워크플로
* 느린 명령(`ls -R`, `find`, `grep`) 대신 `rg` 사용
* 코드 스타일 일관성 유지

---

🏁 맺음말
-----

이번 정리는 GPT-5를 단순한 대화형 모델이 아닌, **완전한 에이전트**로 활용하기 위한 핵심 프롬프트 패턴과 운영 기법을 모두 담고 있습니다.

Agentic 태스크, 코드 작성, 지시 이행, 추론 효율까지 다루었으므로, 실제 서비스·개발 환경에서 즉시 적용 가능합니다.

가이드를 바탕으로 실험·튜닝을 반복하면 GPT-5의 잠재력을 극대화할 수 있습니다.

읽어주셔서 감사합니다 ⭐