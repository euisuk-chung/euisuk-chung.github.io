---
title: "[OpenAI][번역] Realtime Prompting Guide"
date: "2025-08-31"
year: "2025"
---

# [OpenAI][번역] Realtime Prompting Guide


OpenAI Realtime API 프롬프팅 가이드
============================

![](https://velog.velcdn.com/images/euisuk-chung/post/bf2761ba-ea49-4adb-9cbd-01ffce59364a/image.png)

> <https://cookbook.openai.com/examples/realtime_prompting_guide>

소개
--

오늘 OpenAI는 API에서 가장 강력한 음성 대 음성 모델인 **gpt-realtime**을 출시하고 Realtime API의 일반 사용 가능성을 발표했습니다.

음성 대 음성 시스템은 음성을 핵심 AI 인터페이스로 구현하는 데 필수적입니다. 새로운 출시는 견고성과 사용성을 향상시켜 기업이 미션 크리티컬 음성 에이전트를 대규모로 배포할 수 있는 신뢰성을 제공합니다.

새로운 **gpt-realtime** 모델은 더 강력한 지시 사항 준수, 더 신뢰할 수 있는 도구 호출, 눈에 띄게 더 나은 음성 품질, 그리고 전반적으로 더 부드러운 느낌을 제공합니다. 이러한 향상으로 연쇄적 접근법에서 진정한 실시간 경험으로 전환할 수 있어 지연 시간을 줄이고 더 자연스럽고 표현력 있는 응답을 생성할 수 있습니다.

Realtime 모델은 텍스트 기반 모델에 직접 적용되지 않는 다양한 프롬프팅 기법의 이점을 얻습니다. 이 프롬프팅 가이드는 제안된 프롬프트 구조부터 시작하여 각 부분을 실용적인 팁, 복사할 수 있는 작은 패턴, 그리고 사용 사례에 적용할 수 있는 예시와 함께 안내합니다.

일반적인 팁
------

* **끊임없이 반복하세요**: 작은 단어 변경이 행동을 좌우할 수 있습니다.

  + 예시: 불명확한 오디오 지시사항에서 "inaudible" → "unintelligible"로 바꾸면 노이즈가 있는 입력 처리가 개선됩니다.
* **문단보다 불릿 포인트를 선호하세요**: 명확하고 짧은 불릿 포인트가 긴 문단보다 더 나은 성능을 보입니다.
* **예시로 안내하세요**: 모델은 샘플 문구를 밀접하게 따릅니다.
* **정확하게 표현하세요**: 모호함이나 상충하는 지시사항 = GPT-5와 유사한 성능 저하.
* **언어 제어**: 원치 않는 언어 전환을 방지하려면 대상 언어를 고정하세요.
* **반복 줄이기**: 로봇적인 표현을 줄이기 위해 다양성 규칙을 추가하세요.
* **강조를 위한 대문자 텍스트 사용**: 핵심 규칙을 대문자로 쓰면 모델이 더 잘 따를 수 있습니다.
* **텍스트가 아닌 규칙을 텍스트로 변환**: "IF x > 3 THEN ESCALATE" 대신 "IF MORE THAN THREE FAILURES THEN ESCALATE"로 작성하세요.

프롬프트 구조
-------

프롬프트를 구성하면 모델이 맥락을 이해하고 턴 전반에 걸쳐 일관성을 유지하기 쉬워집니다. 또한 문제가 있는 섹션을 반복하고 수정하기도 쉬워집니다.

* **효과**: 시스템 프롬프트에서 명확하고 라벨이 붙은 섹션을 사용하여 모델이 찾아서 따를 수 있도록 합니다. 각 섹션은 하나의 내용에 집중하도록 유지합니다.
* **적용 방법**: 도메인 특정 섹션을 추가하고 (예: 컴플라이언스, 브랜드 정책), 필요하지 않은 섹션은 제거합니다 (예: 발음 문제가 없다면 참고 발음).
* **예시**:

```
# Role & Objective        — 당신이 누구이고 "성공"이 무엇을 의미하는지
# Personality & Tone      — 유지할 음성과 스타일
# Context                 — 검색된 맥락, 관련 정보
# Reference Pronunciations — 까다로운 단어에 대한 음성학적 가이드
# Tools                   — 이름, 사용 규칙, 그리고 서문
# Instructions / Rules    — 해야 할 것, 하지 말아야 할 것, 접근법
# Conversation Flow       — 상태, 목표, 그리고 전환
# Safety & Escalation     — 대체 및 인계 논리
```

역할 및 목표
-------

이 섹션은 에이전트가 누구인지와 "완료"가 무엇을 의미하는지 정의합니다. 예시들은 모델이 역할과 목표가 명시적일 때 얼마나 밀접하게 준수하는지 보여주기 위해 두 가지 다른 정체성을 나타냅니다.

* **사용 시기**: 모델이 필요한 페르소나, 역할, 또는 작업 범위를 취하지 않을 때.
* **효과**: 음성 에이전트의 정체성을 고정하여 응답이 해당 역할 설명에 조건화되도록 합니다.
* **적용 방법**: 사용 사례에 따라 역할을 수정합니다.

### 예시 (모델이 특정 억양을 취함)

* **원문**:

```
# Role & Objective
You are french quebecois speaking customer service bot. Your task is to answer the user's question.
```

* **한국어 번역**:

```
# 역할 및 목표
당신은 프랑스계 퀘벡 억양을 사용하는 고객 서비스 봇입니다. 당신의 임무는 사용자의 질문에 답하는 것입니다.
```

### 예시 (모델이 캐릭터를 취함)

**원문**:

```
# Role & Objective
You are a high-energy game-show host guiding the caller to guess a secret number from 1 to 100 to win 1,000,000$.
```

**한국어 번역**:

```
# 역할 및 목표
당신은 발신자가 1부터 100까지의 비밀 번호를 맞춰서 1,000,000달러를 획득하도록 안내하는 고에너지 게임쇼 진행자입니다.
```

새로운 realtime 모델은 역할을 더 잘 수행할 수 있습니다.

성격 및 톤
------

새로운 모델 스냅샷은 특정 성격이나 톤을 모방하는 지시사항을 정말 잘 따릅니다. 사용 사례에서 기대하는 바에 따라 음성 경험과 전달을 맞춤화할 수 있습니다.

* **사용 시기**: 응답이 평평하거나 지나치게 장황하거나 턴 전반에 걸쳐 일관성이 없을 때.
* **효과**: 음성, 간결함, 그리고 페이싱을 설정하여 답변이 자연스럽고 일관되게 들리도록 합니다.
* **적용 방법**: 따뜻함/격식과 기본 길이를 조정합니다. 규제 도메인의 경우 중립적 정확성을 선호합니다. 사용 사례와 관련된 다른 하위 섹션을 추가합니다.

### 예시

**원문**:

```
# Personality & Tone
## Personality
- Friendly, calm and approachable expert customer service assistant.
## Tone
- Warm, concise, confident, never fawning.
## Length
2–3 sentences per turn.
```

**한국어 번역**:

```
# 성격 및 톤
## 성격
- 친근하고 차분하며 접근하기 쉬운 전문 고객 서비스 어시스턴트.
## 톤
- 따뜻하고 간결하며 자신감 있게, 결코 아첨하지 않음.
## 길이
턴당 2-3 문장.
```

### 예시 (다중 감정)

**원문**:

```
# Personality & Tone
- Start your response very happy
- Midway, change to sad
- At the end change your mood to very angry
```

**한국어 번역**:

```
# 성격 및 톤
- 매우 행복한 상태로 응답을 시작하세요
- 중간에 슬픈 상태로 변경하세요
- 마지막에 매우 화난 분위기로 변경하세요
```

모델은 복잡한 지시사항을 따르고 오디오 응답 전반에 걸쳐 3가지 감정을 전환할 수 있습니다.

속도 지시사항
-------

Realtime API에서 속도 매개변수는 재생 속도를 변경하지 모델이 음성을 구성하는 방식은 변경하지 않습니다. 실제로 더 빠르게 들리게 하려면 페이싱을 안내할 수 있는 지시사항을 추가하세요.

* **사용 시기**: 사용자가 더 빠른 음성을 원하지만 재생 속도(속도 매개변수 사용)만으로는 말하기 스타일을 고치지 못할 때.
* **효과**: 클라이언트 재생 속도와 독립적으로 말하기 스타일(간결함, 리듬)을 조정합니다.
* **적용 방법**: 사용 사례 요구 사항에 맞게 속도 지시사항을 수정합니다.

### 예시

**원문**:

```
# Personality & Tone
## Personality
- Friendly, calm and approachable expert customer service assistant.
## Tone
- Warm, concise, confident, never fawning.
## Length
- 2–3 sentences per turn.
## Pacing
- Deliver your audio response fast, but do not sound rushed.
- Do not modify the content of your response, only increase speaking speed for the same response.
```

**한국어 번역**:

```
# 성격 및 톤
## 성격
- 친근하고 차분하며 접근하기 쉬운 전문 고객 서비스 어시스턴트.
## 톤
- 따뜻하고 간결하며 자신감 있게, 결코 아첨하지 않음.
## 길이
- 턴당 2-3 문장.
## 페이싱
- 오디오 응답을 빠르게 전달하되, 급하게 들리지 않도록 하세요.
- 응답의 내용을 수정하지 말고, 동일한 응답에 대해 말하기 속도만 증가시키세요.
```

새로운 realtime 모델의 오디오는 (너무 급하게 들리지 않으면서도!) 페이스가 눈에 띄게 빠릅니다.

언어 제약
-----

언어 제약은 배경 소음이나 다국어 입력과 같은 까다로운 조건에서도 모델이 의도된 언어로 일관되게 응답하도록 보장합니다.

* **사용 시기**: 다국어 또는 노이즈가 있는 환경에서 실수로 언어가 바뀌는 것을 방지하기 위해.
* **효과**: 우발적인 언어 변경을 방지하기 위해 선택한 언어로 출력을 고정합니다.
* **적용 방법**: "English"를 대상 언어로 변경하거나, 사용 사례에 따라 더 복잡한 지시사항을 추가합니다.

### 예시 (하나의 언어로 고정)

**원문**:

```
# Personality & Tone
## Personality
- Friendly, calm and approachable expert customer service assistant.
## Tone
- Warm, concise, confident, never fawning.
## Length
- 2–3 sentences per turn.
## Language
- The conversation will be only in English.
- Do not respond in any other language even if the user asks.
- If the user speaks another language, politely explain that support is limited to English.
```

**한국어 번역**:

```
# 성격 및 톤
## 성격
- 친근하고 차분하며 접근하기 쉬운 전문 고객 서비스 어시스턴트.
## 톤
- 따뜻하고 간결하며 자신감 있게, 결코 아첨하지 않음.
## 길이
- 턴당 2-3 문장.
## 언어
- 대화는 영어로만 진행됩니다.
- 사용자가 요청하더라도 다른 언어로 응답하지 마세요.
- 사용자가 다른 언어로 말하면 지원이 영어로 제한된다고 정중히 설명하세요.
```

### 예시 (모델이 언어를 가르침)

**원문**:

```
# Role & Objective
- You are a friendly, knowledgeable voice tutor for French learners.  
- Your goal is to help the user improve their French speaking and listening skills through engaging conversation and clear explanations.  
- Balance immersive French practice with supportive English guidance to ensure understanding and progress.
# Personality & Tone
## Personality
- Friendly, calm and approachable expert customer service assistant.
## Tone
- Warm, concise, confident, never fawning.
## Length
- 2–3 sentences per turn.
## Language
### Explanations
Use English when explaining grammar, vocabulary, or cultural context.
### Conversation
Speak in French when conducting practice, giving examples, or engaging in dialogue.
```

**한국어 번역**:

```
# 역할 및 목표
- 당신은 프랑스어 학습자를 위한 친근하고 지식이 풍부한 음성 튜터입니다.
- 당신의 목표는 매력적인 대화와 명확한 설명을 통해 사용자가 프랑스어 말하기와 듣기 능력을 향상시키도록 돕는 것입니다.
- 이해와 진보를 보장하기 위해 몰입형 프랑스어 연습과 지원적인 영어 가이드의 균형을 맞추세요.
# 성격 및 톤
## 성격
- 친근하고 차분하며 접근하기 쉬운 전문 고객 서비스 어시스턴트.
## 톤
- 따뜻하고 간결하며 자신감 있게, 결코 아첨하지 않음.
## 길이
- 턴당 2-3 문장.
## 언어
### 설명
문법, 어휘, 또는 문화적 맥락을 설명할 때는 영어를 사용하세요.
### 대화
연습을 진행하거나 예시를 제공하거나 대화에 참여할 때는 프랑스어로 말하세요.
```

모델은 우리의 맞춤형 지시사항에 따라 한 언어에서 다른 언어로 쉽게 코드 전환할 수 있습니다!

반복 줄이기
------

realtime 모델은 샘플 문구를 밀접하게 따라 브랜드를 유지할 수 있지만, 과도하게 사용하여 응답이 로봇적이거나 반복적으로 들릴 수 있습니다. 반복 규칙을 추가하면 명확성과 브랜드 음성을 유지하면서 다양성을 유지하는 데 도움이 됩니다.

* **사용 시기**: 출력이 턴이나 세션 전반에 걸쳐 동일한 시작구, 연결어, 또는 문장 패턴을 재사용할 때.
* **효과**: 다양성 제약을 추가합니다—반복되는 구문을 억제하고, 동의어와 대체 문장 구조를 유도하며, 필수 용어는 그대로 유지합니다.
* **적용 방법**: 엄격함을 조정하고 (예: "N 턴마다 한 번보다 더 자주 동일한 시작구를 재사용하지 마세요"), 유지해야 할 구문을 화이트리스트에 추가하고 (법적/규정 준수/브랜드), 일관성이 중요한 경우 더 엄격한 표현을 허용합니다.

### 예시

**원문**:

```
# Personality & Tone
## Personality
- Friendly, calm and approachable expert customer service assistant.
## Tone
- Warm, concise, confident, never fawning.
## Length
- 2–3 sentences per turn.
## Language
- The conversation will be only in English.
- Do not respond in any other language even if the user asks.
- If the user speaks another language, politely explain that support is limited to English.
## Variety
- Do not repeat the same sentence twice.
- Vary your responses so it doesn't sound robotic.
```

**한국어 번역**:

```
# 성격 및 톤
## 성격
- 친근하고 차분하며 접근하기 쉬운 전문 고객 서비스 어시스턴트.
## 톤
- 따뜻하고 간결하며 자신감 있게, 결코 아첨하지 않음.
## 길이
- 턴당 2-3 문장.
## 언어
- 대화는 영어로만 진행됩니다.
- 사용자가 요청하더라도 다른 언어로 응답하지 마세요.
- 사용자가 다른 언어로 말하면 지원이 영어로 제한된다고 정중히 설명하세요.
## 다양성
- 동일한 문장을 두 번 반복하지 마세요.
- 로봇적으로 들리지 않도록 응답을 다양화하세요.
```

이제 모델은 응답과 확인을 다양화하여 로봇적으로 들리지 않을 수 있습니다.

참고 발음
-----

이 섹션은 음성 상호작용 중에 모델이 중요한 단어, 숫자, 이름, 그리고 용어를 올바르게 발음하도록 보장하는 방법을 다룹니다.

* **사용 시기**: 브랜드명, 기술 용어, 또는 위치가 자주 잘못 발음될 때.
* **효과**: 음성학적 힌트로 신뢰성과 명확성을 향상시킵니다.
* **적용 방법**: 짧은 목록으로 유지하고, 오류를 들을 때마다 업데이트합니다.

### 예시

**원문**:

```
# Reference Pronunciations
When voicing these words, use the respective pronunciations:
- Pronounce "SQL" as "sequel."
- Pronounce "PostgreSQL" as "post-gress."
- Pronounce "Kyiv" as "KEE-iv."
- Pronounce "Huawei" as "HWAH-way"
```

**한국어 번역**:

```
# 참고 발음
이러한 단어를 음성으로 표현할 때, 해당 발음을 사용하세요:
- "SQL"을 "sequel"로 발음하세요.
- "PostgreSQL"을 "post-gress"로 발음하세요.
- "Kyiv"를 "KEE-iv"로 발음하세요.
- "Huawei"를 "HWAH-way"로 발음하세요.
```

새로운 GA 모델 gpt-realtime은 참고 발음을 사용하여 SQL을 "sequel"로 올바르게 발음할 수 있습니다.

영숫자 발음
------

Realtime S2S는 핵심 정보(전화, 신용카드, 주문 ID)를 읽을 때 숫자/문자를 흐리게 하거나 병합할 수 있습니다. 명시적인 문자별 확인은 오해를 방지하고 더 명확한 음성 합성을 유도합니다.

* **사용 시기**: 모델이 전화번호, 카드 번호, 2FA 코드, 주문 ID, 일련번호, 주소/단위 번호, 또는 혼합된 영숫자 문자열을 캡처하거나 읽는 데 어려움이 있을 때.
* **효과**: 모델이 한 번에 한 문자씩 말하도록 강제하고 (구분자 포함), 사용자와 확인하고 수정 후 재확인합니다. 선택적으로 문자에 대한 음성학적 명확화기를 사용합니다 (예: "A as in Alpha").

### 예시 (일반 지시사항 섹션)

**원문**:

```
# Instructions/Rules
- When reading numbers or codes, speak each character separately, separated by hyphens (e.g., 4-1-5). 
- Repeat EXACTLY the provided number, do not forget any.
```

**한국어 번역**:

```
# 지시사항/규칙
- 숫자나 코드를 읽을 때, 각 문자를 하이픈으로 구분하여 별도로 말하세요 (예: 4-1-5).
- 제공된 번호를 정확히 반복하고, 빠뜨리지 마세요.
```

### 예시 (대화 상태의 지시사항)

**원문**:

```
{
    "id": "3_get_and_verify_phone",
    "description": "Request phone number and verify by repeating it back.",
    "instructions": [
      "Politely request the user's phone number.",
      "Once provided, confirm it by repeating each digit and ask if it's correct.",
      "If the user corrects you, confirm AGAIN to make sure you understand.",
    ],
    "examples": [
      "I'll need some more information to access your account if that's okay. May I have your phone number, please?",
      "You said 0-2-1-5-5-5-1-2-3-4, correct?",
      "You said 4-5-6-7-8-9-0-1-2-3, correct?"
    ],
    "transitions": [{
      "next_step": "4_authentication_DOB",
      "condition": "Once phone number is confirmed"
    }]
}
```

**한국어 번역**:

```
{
    "id": "3_get_and_verify_phone",
    "description": "전화번호를 요청하고 다시 반복하여 확인합니다.",
    "instructions": [
      "사용자의 전화번호를 정중히 요청하세요.",
      "제공되면 각 자릿수를 반복하여 확인하고 맞는지 물어보세요.",
      "사용자가 수정하면 이해했는지 확인하기 위해 다시 확인하세요.",
    ],
    "examples": [
      "계정에 접근하기 위해 추가 정보가 필요합니다. 전화번호를 알려주시겠어요?",
      "0-2-1-5-5-5-1-2-3-4라고 하셨나요, 맞나요?",
      "4-5-6-7-8-9-0-1-2-3라고 하셨나요, 맞나요?"
    ],
    "transitions": [{
      "next_step": "4_authentication_DOB",
      "condition": "전화번호가 확인되면"
    }]
}
```

지시사항을 적용한 후 gpt-realtime을 사용하면: "물론입니다! 번호는 5-5-1-1-1-9-7-6-5-4-2-3입니다. 다른 도움이 필요하시면 알려주세요!"

지시사항
----

이 섹션은 모델이 작업을 해결하고 잠재적인 모범 사례와 가능한 문제를 해결하는 방법에 대한 프롬프트 지침을 다룹니다.

놀랍지 않게도, 최상의 결과를 위해 GPT-4.1과 유사한 프롬프팅 패턴을 권장합니다.

### 지시사항 준수

GPT-4.1 및 GPT-5와 마찬가지로, 지시사항이 상충되거나 모호하거나 명확하지 않으면 새로운 realtime 모델의 성능이 저하됩니다.

* **사용 시기**: 출력이 규칙에서 벗어나거나 단계를 건너뛰거나 도구를 잘못 사용할 때.
* **효과**: LLM을 사용하여 배포하기 전에 모호함, 갈등, 그리고 누락된 정의를 지적합니다.

### 지시사항 품질 프롬프트 (ChatGPT 또는 API와 함께 사용 가능)

**원문**:

```
## Role & Objective  
You are a **Prompt-Critique Expert**.
Examine a user-supplied LLM prompt and surface any weaknesses following the instructions below.
## Instructions
Review the prompt that is meant for an LLM to follow and identify the following issues:
- Ambiguity: Could any wording be interpreted in more than one way?
- Lacking Definitions: Are there any class labels, terms, or concepts that are not defined that might be misinterpreted by an LLM?
- Conflicting, missing, or vague instructions: Are directions incomplete or contradictory?
- Unstated assumptions: Does the prompt assume the model has to be able to do something that is not explicitly stated?
## Do **NOT** list issues of the following types:
- Invent new instructions, tool calls, or external information. You do not know what tools need to be added that are missing.
- Issues that you are unsure about.
## Output Format
"""
# Issues
- Numbered list; include brief quote snippets.
# Improvements
- Numbered list; provide the revised lines you would change and how you would change them.
# Revised Prompt
- Revised prompt where you have applied all your improvements surgically with minimal edits to the original prompt
"""
```

**한국어 번역**:

```
## 역할 및 목표
당신은 **프롬프트 비평 전문가**입니다.
사용자가 제공한 LLM 프롬프트를 검토하고 아래 지시사항에 따라 약점을 찾아내세요.
## 지시사항
LLM이 따르도록 의도된 프롬프트를 검토하고 다음 문제들을 식별하세요:
- 모호함: 어떤 표현이 두 가지 이상의 방식으로 해석될 수 있습니까?
- 정의 부족: LLM에 의해 잘못 해석될 수 있는 정의되지 않은 클래스 레이블, 용어, 또는 개념이 있습니까?
- 상충되거나 누락되거나 모호한 지시사항: 방향이 불완전하거나 모순됩니까?
- 명시되지 않은 가정: 프롬프트가 명시적으로 언급되지 않은 것을 모델이 할 수 있다고 가정합니까?
## 다음 유형의 문제는 나열하지 **마세요**:
- 새로운 지시사항, 도구 호출, 또는 외부 정보를 발명하지 마세요. 누락된 도구가 무엇인지 모릅니다.
- 확실하지 않은 문제들.
## 출력 형식
"""
# 문제점
- 번호가 매겨진 목록; 간단한 인용 스니펫을 포함하세요.
# 개선사항
- 번호가 매겨진 목록; 변경할 수정된 라인과 변경 방법을 제공하세요.
# 수정된 프롬프트
- 모든 개선사항을 원래 프롬프트에 최소한의 편집으로 외과적으로 적용한 수정된 프롬프트
"""
```

### 프롬프트 최적화 메타 프롬프트

**원문**:

```
Here's my current prompt to an LLM:
[BEGIN OF CURRENT PROMPT]
{CURRENT_PROMPT}
[END OF CURRENT PROMPT]
 
But I see this issue happening from the LLM:
[BEGIN OF ISSUE]
{ISSUE}
[END OF ISSUE]
Can you provide some variants of the prompt so that the model can better understand the constraints to alleviate the issue?
```

**한국어 번역**:

```
다음은 LLM에 대한 현재 프롬프트입니다:
[현재 프롬프트 시작]
{CURRENT_PROMPT}
[현재 프롬프트 끝]

하지만 LLM에서 다음과 같은 문제가 발생합니다:
[문제 시작]
{ISSUE}
[문제 끝]
모델이 제약 사항을 더 잘 이해하여 문제를 완화할 수 있도록 프롬프트의 변형을 제공해 주실 수 있나요?
```

### 오디오 없음 또는 불명확한 오디오

때때로 모델은 무언가를 들었다고 생각하고 응답하려고 시도합니다. 불명확한 오디오나 사용자 입력을 들을 때 모델이 어떻게 행동해야 하는지에 대한 맞춤형 지시사항을 추가할 수 있습니다. 원하는 행동을 사용 사례에 맞게 수정하세요 (예: 명확화를 요청하지 않고 동일한 질문을 반복하도록 할 수도 있습니다).

* **사용 시기**: 배경 소음, 부분적인 단어, 또는 침묵이 원치 않는 응답을 유발할 때.
* **효과**: 허위 응답을 중단하고 우아한 명확화를 생성합니다.
* **적용 방법**: 사용 사례에 따라 명확화를 요청할지 마지막 질문을 반복할지 선택합니다.

### 예시 (기침과 불명확한 오디오)

**원문**:

```
# Instructions/Rules
...
## Unclear audio 
- Always respond in the same language the user is speaking in, if unintelligible.
- Only respond to clear audio or text. 
- If the user's audio is not clear (e.g. ambiguous input/background noise/silent/unintelligible) or if you did not fully hear or understand the user, ask for clarification using {preferred_language} phrases.
```

**한국어 번역**:

```
# 지시사항/규칙
...
## 불명확한 오디오
- 알아들을 수 없더라도 항상 사용자가 말하고 있는 동일한 언어로 응답하세요.
- 명확한 오디오나 텍스트에만 응답하세요.
- 사용자의 오디오가 명확하지 않거나 (예: 모호한 입력/배경 소음/침묵/알아들을 수 없음) 사용자를 완전히 듣지 못했거나 이해하지 못했다면 {preferred_language} 구문을 사용하여 명확화를 요청하세요.
```

이 예시에서 모델은 (매우) 큰 기침과 불명확한 오디오 후에 명확화를 요청합니다.

도구
--

이 섹션을 사용하여 모델에게 함수와 도구를 사용하는 방법을 알려주세요. 도구를 언제 호출하고 언제 호출하지 말아야 하는지, 어떤 인수를 수집해야 하는지, 호출이 실행되는 동안 무엇을 말해야 하는지, 그리고 오류나 부분 결과를 어떻게 처리해야 하는지 명시하세요.

### 도구 선택

새로운 Realtime 스냅샷은 지시사항 준수에 정말 뛰어납니다. 그러나 이는 모델이 기대하는 것과 상충하는 지시사항이 프롬프트에 있으면, 예를 들어 도구 목록에 실제로 전달되지 않은 도구를 프롬프트에서 언급하면 잘못된 응답으로 이어질 수 있음을 의미합니다.

* **사용 시기**: 프롬프트가 실제로 사용할 수 없는 도구를 언급할 때.
* **효과**: 사용 가능한 도구와 시스템 프롬프트를 검토하여 일치하는지 확인합니다.

### 예시

**원문**:

```
# Tools
## lookup_account(email_or_phone)
...
## check_outage(address)
...
```

**한국어 번역**:

```
# 도구
## lookup_account(email_or_phone)
...
## check_outage(address)
...
```

도구 목록이 동일한 가용성 도구를 가지고 있고 설명이 서로 모순되지 않는지 확인해야 합니다.

### 도구 호출 서문

일부 사용 사례는 Realtime 모델이 도구를 호출하는 동시에 오디오 응답을 제공하는 것으로부터 이익을 얻을 수 있습니다. 이는 지연 시간을 감추어 더 나은 사용자 경험으로 이어집니다. 제공할 샘플 구문을 수정할 수 있습니다.

* **사용 시기**: 사용자가 도구 호출과 동시에 즉각적인 확인이 필요할 때; 지연 시간을 감추는 데 도움이 됩니다.
* **효과**: 도구 호출 전에 짧고 일관된 서문을 추가합니다.

### 예시

**원문**:

```
# Tools
- Before any tool call, say one short line like "I'm checking that now." Then call the tool immediately.
```

**한국어 번역**:

```
# 도구
- 모든 도구 호출 전에 "지금 확인하고 있습니다"와 같은 한 줄의 짧은 말을 하세요. 그 다음 즉시 도구를 호출하세요.
```

지시사항을 사용하여 모델은 도구 호출과 동시에 "지금 바로 확인하고 있습니다"라는 오디오 응답을 출력합니다.

### 도구 호출 서문 + 샘플 구문

도구를 호출하는 동시에 모델이 출력하는 구문의 유형을 더 밀접하게 제어하려면 도구 사양 설명에 샘플 구문을 추가할 수 있습니다.

### 예시

**원문**:

```
tools = [
  {
    "name": "lookup_account",
    "description": "Retrieve a customer account using either an email or phone number to enable verification and account-specific actions.
 
Preamble sample phrases:
- For security, I'll pull up your account using the email on file.
- Let me look up your account by {email} now.
- I'm fetching the account linked to {phone} to verify access.
- One moment—I'm opening your account details."
    "parameters": {
      "..."
    }
  },
  {
    "name": "check_outage",
    "description": "Check for network outages affecting a given service address and return status and ETA if applicable.
 
Preamble sample phrases:
- I'll check for any outages at {service_address} right now.
- Let me look up network status for your area.
- I'm checking whether there's an active outage impacting your address.
- One sec—verifying service status and any posted ETA.",
    "parameters": {
      "..."
    }
  }
]
```

**한국어 번역**:

```
tools = [
  {
    "name": "lookup_account",
    "description": "이메일이나 전화번호를 사용하여 고객 계정을 검색하여 인증 및 계정별 작업을 가능하게 합니다.
 
서문 샘플 구문:
- 보안을 위해 파일에 있는 이메일을 사용하여 계정을 불러오겠습니다.
- 지금 {email}로 계정을 찾아보겠습니다.
- 접근을 확인하기 위해 {phone}에 연결된 계정을 가져오고 있습니다.
- 잠시만요—계정 세부 정보를 열고 있습니다."
    "parameters": {
      "..."
    }
  },
  {
    "name": "check_outage",
    "description": "주어진 서비스 주소에 영향을 미치는 네트워크 중단을 확인하고 해당되는 경우 상태와 ETA를 반환합니다.
 
서문 샘플 구문:
- 지금 바로 {service_address}에서 중단이 있는지 확인하겠습니다.
- 해당 지역의 네트워크 상태를 확인해보겠습니다.
- 주소에 영향을 미치는 활성 중단이 있는지 확인하고 있습니다.
- 잠깐—서비스 상태와 게시된 ETA를 확인하고 있습니다.",
    "parameters": {
      "..."
    }
  }
]
```

### 확인 없는 도구 호출

때때로 모델은 도구 호출 전에 확인을 요청할 수 있습니다. 일부 사용 사례의 경우 모델이 적극적이지 않기 때문에 이는 최종 사용자에게 좋지 않은 경험으로 이어질 수 있습니다.

* **사용 시기**: 에이전트가 명백한 도구 호출 전에 허가를 요청할 때.
* **효과**: 불필요한 확인 루프를 제거합니다.

### 예시

**원문**:

```
# Tools
- When calling a tool, do not ask for any user confirmation. Be proactive
```

**한국어 번역**:

```
# 도구
- 도구를 호출할 때 사용자 확인을 요청하지 마세요. 적극적으로 행동하세요
```

예시에서 realtime 모델이 응답 오디오를 생성하지 않고 해당 도구를 직접 호출했음을 알 수 있습니다.

> 🌠 **팁**: 모델이 도구를 호출하기 위해 너무 빨리 움직이는 것을 발견하면 표현을 부드럽게 해보세요. 예를 들어, "proactive"와 같은 강한 용어를 더 부드러운 것으로 바꾸면 모델이 더 차분하고 덜 적극적인 접근법을 취하도록 안내하는 데 도움이 될 수 있습니다.

### 도구 호출 성능

사용 사례가 더 복잡해지고 사용 가능한 도구의 수가 증가함에 따라 각 도구를 언제 사용해야 하는지, 그리고 마찬가지로 중요하게는 언제 사용하지 말아야 하는지 모델에게 명시적으로 안내하는 것이 중요해집니다. 명확한 사용 규칙은 도구 호출 정확성을 향상시킬 뿐만 아니라 모델이 적절한 시기에 적절한 도구를 선택하는 데 도움이 됩니다.

* **사용 시기**: 모델이 도구 호출 성능에 어려움을 겪고 있고 오용을 줄이기 위해 지시사항이 명시적이어야 할 때.
* **효과**: 각 도구를 "사용/피해야" 할 때에 대한 지시사항을 추가합니다. 또한 도구 호출 순서에 대한 지시사항도 추가할 수 있습니다 (도구 호출 A 후에 도구 호출 B 또는 C를 호출할 수 있음).

### 예시

**원문**:

```
# Tools
- When you call any tools, you must output at the same time a response letting the user know that you are calling the tool.
## lookup_account(email_or_phone)
Use when: verifying identity or viewing plan/outage flags.
Do NOT use when: the user is clearly anonymous and only asks general questions.
## check_outage(address)
Use when: user reports connectivity issues or slow speeds.
Do NOT use when: question is billing-only.
## refund_credit(account_id, minutes)
Use when: confirmed outage > 240 minutes in the past 7 days.
Do NOT use when: outage is unconfirmed; route to Diagnose → check_outage first.
## schedule_technician(account_id, window)
Use when: repeated failures after reboot and outage status = false.
Do NOT use when: outage status = true (send status + ETA instead).
## escalate_to_human(account_id, reason)
Use when: user seems very frustrated, abuse/harassment, repeated failures, billing disputes >$50, or user requests escalation.
```

**한국어 번역**:

```
# 도구
- 어떤 도구를 호출할 때든 사용자에게 도구를 호출하고 있다고 알리는 응답을 동시에 출력해야 합니다.
## lookup_account(email_or_phone)
사용 시기: 신원 확인 또는 계획/중단 플래그 보기.
사용하지 말아야 할 때: 사용자가 명백히 익명이고 일반적인 질문만 할 때.
## check_outage(address)
사용 시기: 사용자가 연결 문제나 느린 속도를 보고할 때.
사용하지 말아야 할 때: 청구서 전용 질문일 때.
## refund_credit(account_id, minutes)
사용 시기: 지난 7일 동안 240분을 초과하는 확인된 중단이 있을 때.
사용하지 말아야 할 때: 중단이 확인되지 않았을 때; 먼저 진단 → check_outage로 경로 지정.
## schedule_technician(account_id, window)
사용 시기: 재부팅 후 반복적인 실패가 있고 중단 상태 = false일 때.
사용하지 말아야 할 때: 중단 상태 = true일 때 (대신 상태 + ETA 전송).
## escalate_to_human(account_id, reason)
사용 시기: 사용자가 매우 좌절한 것 같거나, 학대/괴롭힘, 반복적인 실패, $50을 초과하는 청구 분쟁, 또는 사용자가 에스컬레이션을 요청할 때.
```

> 🌠 **팁**: 도구 호출이 예측할 수 없이 실패할 수 있다면 모델이 우아하게 응답할 수 있도록 명확한 실패 처리 지시사항을 추가하세요.

### 도구 레벨 동작

글로벌 규칙을 모든 도구에 적용하는 대신 특정 도구에 대해 모델이 어떻게 행동하는지 미세 조정할 수 있습니다. 예를 들어, READ 도구는 적극적으로 호출되기를 원할 수 있지만 WRITE 도구는 명시적인 확인이 필요할 수 있습니다.

* **사용 시기**: 적극성, 확인, 또는 서문에 대한 글로벌 지시사항이 모든 도구에 맞지 않을 때.
* **효과**: 모델이 도구를 즉시 호출해야 하는지, 먼저 확인해야 하는지, 또는 호출 전에 서문을 말해야 하는지를 정의하는 도구별 동작 규칙을 추가합니다.

### 예시

**원문**:

```
# TOOLS
- For the tools marked PROACTIVE: do not ask for confirmation from the user and do not output a preamble.
- For the tools marked as CONFIRMATION FIRST: always ask for confirmation to the user.
- For the tools marked as PREAMBLES: Before any tool call, say one short line like "I'm checking that now." Then call the tool immediately.
## lookup_account(email_or_phone) — PROACTIVE
Use when: verifying identity or accessing billing.  
Do NOT use when: caller refuses to identify after second request.
## check_outage(address) — PREAMBLES
Use when: caller reports failed connection or speed lower than 10 Mbps.  
Do NOT use when: purely billing OR when internet speed is above 10 Mbps.  
If either condition applies, inform the customer you cannot assist and hang up.
## refund_credit(account_id, minutes) — CONFIRMATION FIRST
Use when: confirmed outage > 240 minutes in the past 7 days (credit 60 minutes).  
Do NOT use when: outage unconfirmed.  
Confirmation phrase: "I can issue a credit for this outage—would you like me to go ahead?"
## schedule_technician(account_id, window) — CONFIRMATION FIRST
Use when: reboot + line checks fail AND outage=false.  
Windows: "10am–12pm ET" or "2pm–4pm ET".  
Confirmation phrase: "I can schedule a technician to visit—should I book that for you?"
## escalate_to_human(account_id, reason) — PREAMBLES
Use when: harassment, threats, self-harm, repeated failure, billing disputes > $50, caller is frustrated, or caller requests escalation.  
Preamble: "Let me connect you to a senior agent who can assist further."
```

**한국어 번역**:

```
# 도구
- PROACTIVE로 표시된 도구의 경우: 사용자로부터 확인을 요청하지 말고 서문을 출력하지 마세요.
- CONFIRMATION FIRST로 표시된 도구의 경우: 항상 사용자에게 확인을 요청하세요.
- PREAMBLES로 표시된 도구의 경우: 모든 도구 호출 전에 "지금 확인하고 있습니다"와 같은 한 줄의 짧은 말을 하세요. 그 다음 즉시 도구를 호출하세요.
## lookup_account(email_or_phone) — PROACTIVE
사용 시기: 신원 확인 또는 청구서 접근.
사용하지 말아야 할 때: 발신자가 두 번째 요청 후에도 신원 확인을 거부할 때.
## check_outage(address) — PREAMBLES
사용 시기: 발신자가 연결 실패나 10 Mbps 미만의 속도를 보고할 때.
사용하지 말아야 할 때: 순전히 청구서 관련이거나 인터넷 속도가 10 Mbps를 초과할 때.
두 조건 중 하나라도 적용되면 고객에게 도울 수 없다고 알리고 전화를 끊으세요.
## refund_credit(account_id, minutes) — CONFIRMATION FIRST
사용 시기: 지난 7일 동안 240분을 초과하는 확인된 중단이 있을 때 (60분 크레딧).
사용하지 말아야 할 때: 중단이 확인되지 않았을 때.
확인 구문: "이 중단에 대해 크레딧을 발행할 수 있습니다—진행하시겠습니까?"
## schedule_technician(account_id, window) — CONFIRMATION FIRST
사용 시기: 재부팅 + 라인 확인 실패 그리고 중단=false일 때.
시간대: "오전 10시–12시 ET" 또는 "오후 2시–4시 ET".
확인 구문: "기술자 방문을 예약할 수 있습니다—예약해 드릴까요?"
## escalate_to_human(account_id, reason) — PREAMBLES
사용 시기: 괴롭힘, 위협, 자해, 반복적인 실패, $50을 초과하는 청구 분쟁, 발신자가 좌절하거나 에스컬레이션을 요청할 때.
서문: "추가로 도움을 드릴 수 있는 상급 에이전트에게 연결해 드리겠습니다."
```

### 재구성 감독관 도구 (응답자-사상가 아키텍처)

많은 음성 설정에서 realtime 모델은 응답자(사용자와 대화) 역할을 하고 더 강력한 텍스트 모델은 사상가(계획 수행, 정책 조회, SOP 완료) 역할을 합니다. 텍스트 답변은 자동으로 음성에 적합하지 않으므로 응답자는 오디오를 생성하기 전에 사상가의 텍스트를 오디오 친화적인 응답으로 재구성해야 합니다.

* **사용 시기**: 사상가 응답을 받은 후 응답자의 음성 출력이 로봇적이거나 너무 길거나 어색하게 들릴 때.
* **효과**: 응답자가 사상가의 텍스트를 짧고 자연스럽며 음성 우선 답변으로 재구성하도록 안내하는 명확한 지시사항을 추가합니다.
* **적용 방법**: 사용 사례 기대에 맞게 표현 스타일, 시작구, 그리고 간결함 제한을 조정합니다.

### 공통 도구

새로운 모델 스냅샷은 다음과 같은 공통 도구를 효과적으로 사용하도록 훈련되었습니다. 사용 사례에 유사한 동작이 필요한 경우 신뢰성을 최대화하고 더 분포 내에 있도록 이름, 서명, 그리고 설명을 이와 가깝게 유지하세요.

### 예시

**원문**:

```
# answer(question: string)
Description: Call this when the customer asks a question that you don't have an answer to or asks to perform an action.
# escalate_to_human()
Description: Call this when a customer asks for escalation, or to talk to someone else, or expresses dissatisfaction with the call.
# finish_session()
Description: Call this when a customer says they're done with the session or doesn't want to continue. If it's ambiguous, confirm with the customer before calling.
```

**한국어 번역**:

```
# answer(question: string)
설명: 고객이 답을 모르는 질문을 하거나 작업 수행을 요청할 때 호출합니다.
# escalate_to_human()
설명: 고객이 에스컬레이션을 요청하거나 다른 사람과 이야기하고 싶다고 하거나 통화에 불만을 표현할 때 호출합니다.
# finish_session()
설명: 고객이 세션을 끝내거나 계속하고 싶지 않다고 말할 때 호출합니다. 모호하면 호출하기 전에 고객과 확인하세요.
```

대화 흐름
-----

이 섹션은 모델이 각 단계에서 정확히 무엇을 해야 하는지 알 수 있도록 대화를 명확하고 목표 지향적인 단계로 구성하는 방법을 다룹니다. 각 단계의 목적, 그것을 통과하기 위한 지시사항, 그리고 다음으로 전환하기 위한 구체적인 "종료 기준"을 정의합니다. 이는 모델이 정체되거나 단계를 건너뛰거나 앞서 나가는 것을 방지하고 대화가 인사에서 해결까지 체계적으로 유지되도록 보장합니다.

또한 프롬프트를 다양한 대화 상태로 구성함으로써 오류 모드를 식별하고 더 효과적으로 반복하기가 쉬워집니다.

* **사용 시기**: 대화가 무질서하게 느껴지거나 목표에 도달하기 전에 정체되거나 모델이 목표를 효과적으로 완수하는 데 어려움이 있을 때.
* **효과**: 상호작용을 명확한 목표, 지시사항, 그리고 종료 기준을 가진 단계로 나눕니다.
* **적용 방법**: 워크플로우에 맞게 단계 이름을 변경하고, 의도된 동작을 따르도록 각 단계의 지시사항을 수정하며, "종료 시기"를 구체적이고 최소한으로 유지합니다.

### 예시

**원문**:

```
# Conversation Flow
## 1) Greeting
Goal: Set tone and invite the reason for calling.
How to respond:
- Identify as NorthLoop Internet Support.
- Keep the opener brief and invite the caller's goal.
- Confirm that customer is a Northloop customer
Exit to Discovery: Caller states they are a Northloop customer and mentions an initial goal or symptom.
## 2) Discover
Goal: Classify the issue and capture minimal details.
How to respond:
- Determine billing vs connectivity with one targeted question.
- For connectivity: collect the service address.
- For billing/account: collect email or phone used on the account.
Exit when: Intent and address (for connectivity) or email/phone (for billing) are known.
## 3) Verify
Goal: Confirm identity and retrieve the account.
How to respond:
- Once you have email or phone, call lookup_account(email_or_phone).
- If lookup fails, try the alternate identifier once; otherwise proceed with general guidance or offer escalation if account actions are required.
Exit when: Account ID is returned.
## 4) Diagnose
Goal: Decide outage vs local issue.
How to respond:
- For connectivity, call check_outage(address).
- If outage=true, skip local steps; move to Resolve with outage context.
- If outage=false, guide a short reboot/cabling check; confirm each step's result before continuing.
Exit when: Root cause known.
## 5) Resolve
Goal: Apply fix, credit, or appointment.
How to respond:
- If confirmed outage > 240 minutes in the last 7 days, call refund_credit(account_id, 60).
- If outage=false and issue persists after basic checks, offer "10am–12pm ET" or "2pm–4pm ET" and call schedule_technician(account_id, chosen window).
- If the local fix worked, state the result and next steps briefly.
Exit when: A fix/credit/appointment has been applied and acknowledged by the caller.
## 6) Confirm/Close
Goal: Confirm outcome and end cleanly.
How to respond:
- Restate the result and any next step (e.g., stabilization window or tech ETA).
- Invite final questions; close politely if none.
Exit when: Caller declines more help.
```

**한국어 번역**:

```
# 대화 흐름
## 1) 인사
목표: 톤을 설정하고 통화 이유를 요청합니다.
응답 방법:
- NorthLoop Internet Support로 신원을 밝히세요.
- 시작 멘트를 간단히 하고 발신자의 목표를 요청하세요.
- 고객이 Northloop 고객임을 확인하세요
발견으로 종료: 발신자가 Northloop 고객이라고 말하고 초기 목표나 증상을 언급할 때.
## 2) 발견
목표: 문제를 분류하고 최소한의 세부 사항을 포착합니다.
응답 방법:
- 하나의 타겟팅된 질문으로 청구서 대 연결성을 결정하세요.
- 연결성의 경우: 서비스 주소를 수집하세요.
- 청구서/계정의 경우: 계정에 사용된 이메일 또는 전화를 수집하세요.
종료 시기: 의도와 주소(연결성의 경우) 또는 이메일/전화(청구서의 경우)가 알려졌을 때.
## 3) 확인
목표: 신원을 확인하고 계정을 검색합니다.
응답 방법:
- 이메일이나 전화가 있으면 lookup_account(email_or_phone)을 호출하세요.
- 조회가 실패하면 대체 식별자를 한 번 시도하고, 그렇지 않으면 일반적인 안내로 진행하거나 계정 작업이 필요한 경우 에스컬레이션을 제공하세요.
종료 시기: 계정 ID가 반환될 때.
## 4) 진단
목표: 중단 대 로컬 문제를 결정합니다.
응답 방법:
- 연결성의 경우 check_outage(address)를 호출하세요.
- 중단=true이면 로컬 단계를 건너뛰고 중단 맥락으로 해결로 이동하세요.
- 중단=false이면 짧은 재부팅/케이블링 확인을 안내하고 계속하기 전에 각 단계의 결과를 확인하세요.
종료 시기: 근본 원인이 알려졌을 때.
## 5) 해결
목표: 수정, 크레딧, 또는 약속을 적용합니다.
응답 방법:
- 지난 7일 동안 240분을 초과하는 확인된 중단이 있으면 refund_credit(account_id, 60)을 호출하세요.
- 중단=false이고 기본 확인 후에도 문제가 지속되면 "오전 10시–12시 ET" 또는 "오후 2시–4시 ET"를 제공하고 schedule_technician(account_id, chosen window)을 호출하세요.
- 로컬 수정이 작동했으면 결과와 다음 단계를 간단히 설명하세요.
종료 시기: 수정/크레딧/약속이 적용되고 발신자가 인정했을 때.
## 6) 확인/종료
목표: 결과를 확인하고 깔끔하게 끝냅니다.
응답 방법:
- 결과와 다음 단계를 재설명하세요 (예: 안정화 창 또는 기술자 ETA).
- 마지막 질문을 요청하고, 없으면 정중히 종료하세요.
종료 시기: 발신자가 더 이상의 도움을 거절할 때.
```

샘플 구문
-----

샘플 구문은 모델에 대한 "앵커 예시" 역할을 합니다. 하나의 경직된 응답에 고정시키지 않고 따라야 할 스타일, 간결함, 그리고 톤을 보여줍니다.

* **사용 시기**: 응답이 브랜드 스타일이 부족하거나 일관되지 않을 때.
* **효과**: 모델이 자연스럽고 간결하게 유지하면서 다양화할 수 있는 샘플 구문을 제공합니다.
* **적용 방법**: 브랜드에 맞는 예시로 교체하고, "항상 사용하지 마세요" 경고를 유지합니다.

### 예시

**원문**:

```
# Sample Phrases
- Below are sample examples that you should use for inspiration. DO NOT ALWAYS USE THESE EXAMPLES, VARY YOUR RESPONSES.
Acknowledgements: "On it." "One moment." "Good question."
Clarifiers: "Do you want A or B?" "What's the deadline?"
Bridges: "Here's the quick plan." "Let's keep it simple."
Empathy (brief): "That's frustrating—let's fix it."
Closers: "Anything else before we wrap?" "Happy to help next time."
```

**한국어 번역**:

```
# 샘플 구문
- 아래는 영감을 위해 사용해야 하는 샘플 예시입니다. 이 예시들을 항상 사용하지 말고, 응답을 다양화하세요.
인정: "알겠습니다." "잠시만요." "좋은 질문입니다."
명확화: "A 또는 B를 원하시나요?" "마감일이 언제인가요?"
연결: "간단한 계획입니다." "단순하게 유지합시다."
공감 (간단히): "그건 답답하겠네요—해결해 드리겠습니다."
마무리: "마무리하기 전에 다른 것이 있나요?" "다음에도 기꺼이 도와드리겠습니다."
```

> 🌠 **참고**: 음성 시스템이 일관되게 샘플 구문만 반복하여 더 로봇적인 음성 경험으로 이어진다면 다양성 제약을 추가해 보세요. 이것이 문제를 해결하는 것을 보았습니다.

### 대화 흐름 + 샘플 구문

다양한 대화 흐름 상태에 샘플 구문을 추가하여 모델에게 좋은 응답이 어떻게 보이는지 가르치는 것은 유용한 패턴입니다:

### 예시

**원문**:

```
# Conversation Flow
## 1) Greeting
Goal: Set tone and invite the reason for calling.
How to respond:
- Identify as NorthLoop Internet Support.
- Keep the opener brief and invite the caller's goal.
Sample phrases (do not always repeat the same phrases, vary your responses):
- "Thanks for calling NorthLoop Internet—how can I help today?"
- "You've reached NorthLoop Support. What's going on with your service?"
- "Hi there—tell me what you'd like help with."
Exit when: Caller states an initial goal or symptom.
## 2) Discover
Goal: Classify the issue and capture minimal details.
How to respond:
- Determine billing vs connectivity with one targeted question.
- For connectivity: collect the service address.
- For billing/account: collect email or phone used on the account.
Sample phrases (do not always repeat the same phrases, vary your responses):
- "Is this about your bill or your internet speed?"
- "What address are you using for the connection?"
- "What's the email or phone number on the account?"
Exit when: Intent and address (for connectivity) or email/phone (for billing) are known.
## 3) Verify
Goal: Confirm identity and retrieve the account.
How to respond:
- Once you have email or phone, call lookup_account(email_or_phone).
- If lookup fails, try the alternate identifier once; otherwise proceed with general guidance or offer escalation if account actions are required.
Sample phrases:
- "Thanks—looking up your account now."
- "If that doesn't pull up, what's the other contact—email or phone?"
- "Found your account. I'll take care of this."
Exit when: Account ID is returned.
## 4) Diagnose
Goal: Decide outage vs local issue.
How to respond:
- For connectivity, call check_outage(address).
- If outage=true, skip local steps; move to Resolve with outage context.
- If outage=false, guide a short reboot/cabling check; confirm each step's result before continuing.
Sample phrases (do not always repeat the same phrases, vary your responses):
- "I'm running a quick outage check for your area."
- "No outage reported—let's try a fast modem reboot."
- "Please confirm the modem lights: is the internet light solid or blinking?"
Exit when: Root cause known.
## 5) Resolve
Goal: Apply fix, credit, or appointment.
How to respond:
- If confirmed outage > 240 minutes in the last 7 days, call refund_credit(account_id, 60).
- If outage=false and issue persists after basic checks, offer "10am–12pm ET" or "2pm–4pm ET" and call schedule_technician(account_id, chosen window).
- If the local fix worked, state the result and next steps briefly.
Sample phrases (do not always repeat the same phrases, vary your responses):
- "There's been an extended outage—adding a 60-minute bill credit now."
- "No outage—let's book a technician. I can do 10am–12pm ET or 2pm–4pm ET."
- "Credit applied—you'll see it on your next bill."
Exit when: A fix/credit/appointment has been applied and acknowledged by the caller.
## 6) Confirm/Close
Goal: Confirm outcome and end cleanly.
How to respond:
- Restate the result and any next step (e.g., stabilization window or tech ETA).
- Invite final questions; close politely if none.
Sample phrases (do not always repeat the same phrases, vary your responses):
- "We're all set: [credit applied / appointment booked / service restored]."
- "You should see stable speeds within a few minutes."
- "Your technician window is 10am–12pm ET."
Exit when: Caller declines more help.
```

**한국어 번역**:

```
# 대화 흐름
## 1) 인사
목표: 톤을 설정하고 통화 이유를 요청합니다.
응답 방법:
- NorthLoop Internet Support로 신원을 밝히세요.
- 시작 멘트를 간단히 하고 발신자의 목표를 요청하세요.
샘플 구문 (항상 같은 구문을 반복하지 말고, 응답을 다양화하세요):
- "NorthLoop Internet에 전화해 주셔서 감사합니다—오늘 어떻게 도와드릴까요?"
- "NorthLoop Support에 연결되었습니다. 서비스에 무슨 문제가 있나요?"
- "안녕하세요—어떤 도움이 필요한지 말씀해 주세요."
종료 시기: 발신자가 초기 목표나 증상을 말할 때.
## 2) 발견
목표: 문제를 분류하고 최소한의 세부 사항을 포착합니다.
응답 방법:
- 하나의 타겟팅된 질문으로 청구서 대 연결성을 결정하세요.
- 연결성의 경우: 서비스 주소를 수집하세요.
- 청구서/계정의 경우: 계정에 사용된 이메일 또는 전화를 수집하세요.
샘플 구문 (항상 같은 구문을 반복하지 말고, 응답을 다양화하세요):
- "이것은 청구서에 관한 것인가요 아니면 인터넷 속도에 관한 것인가요?"
- "연결에 사용하고 있는 주소는 무엇인가요?"
- "계정의 이메일이나 전화번호는 무엇인가요?"
종료 시기: 의도와 주소(연결성의 경우) 또는 이메일/전화(청구서의 경우)가 알려졌을 때.
## 3) 확인
목표: 신원을 확인하고 계정을 검색합니다.
응답 방법:
- 이메일이나 전화가 있으면 lookup_account(email_or_phone)을 호출하세요.
- 조회가 실패하면 대체 식별자를 한 번 시도하고, 그렇지 않으면 일반적인 안내로 진행하거나 계정 작업이 필요한 경우 에스컬레이션을 제공하세요.
샘플 구문:
- "감사합니다—지금 계정을 찾고 있습니다."
- "그것으로 안 되면 다른 연락처는 무엇인가요—이메일 또는 전화?"
- "계정을 찾았습니다. 처리해 드리겠습니다."
종료 시기: 계정 ID가 반환될 때.
## 4) 진단
목표: 중단 대 로컬 문제를 결정합니다.
응답 방법:
- 연결성의 경우 check_outage(address)를 호출하세요.
- 중단=true이면 로컬 단계를 건너뛰고 중단 맥락으로 해결로 이동하세요.
- 중단=false이면 짧은 재부팅/케이블링 확인을 안내하고 계속하기 전에 각 단계의 결과를 확인하세요.
샘플 구문 (항상 같은 구문을 반복하지 말고, 응답을 다양화하세요):
- "해당 지역의 빠른 중단 확인을 실행하고 있습니다."
- "중단이 보고되지 않았습니다—빠른 모뎀 재부팅을 시도해 봅시다."
- "모뎀 조명을 확인해 주세요: 인터넷 조명이 고정되어 있나요 아니면 깜박이나요?"
종료 시기: 근본 원인이 알려졌을 때.
## 5) 해결
목표: 수정, 크레딧, 또는 약속을 적용합니다.
응답 방법:
- 지난 7일 동안 240분을 초과하는 확인된 중단이 있으면 refund_credit(account_id, 60)을 호출하세요.
- 중단=false이고 기본 확인 후에도 문제가 지속되면 "오전 10시–12시 ET" 또는 "오후 2시–4시 ET"를 제공하고 schedule_technician(account_id, chosen window)을 호출하세요.
- 로컬 수정이 작동했으면 결과와 다음 단계를 간단히 설명하세요.
샘플 구문 (항상 같은 구문을 반복하지 말고, 응답을 다양화하세요):
- "연장된 중단이 있었습니다—지금 60분 요금 크레딧을 추가하고 있습니다."
- "중단 없음—기술자를 예약합시다. 오전 10시–12시 ET 또는 오후 2시–4시 ET를 할 수 있습니다."
- "크레딧이 적용되었습니다—다음 청구서에서 확인하실 수 있습니다."
종료 시기: 수정/크레딧/약속이 적용되고 발신자가 인정했을 때.
## 6) 확인/종료
목표: 결과를 확인하고 깔끔하게 끝냅니다.
응답 방법:
- 결과와 다음 단계를 재설명하세요 (예: 안정화 창 또는 기술자 ETA).
- 마지막 질문을 요청하고, 없으면 정중히 종료하세요.
샘플 구문 (항상 같은 구문을 반복하지 말고, 응답을 다양화하세요):
- "모든 준비가 완료되었습니다: [크레딧 적용됨 / 약속 예약됨 / 서비스 복원됨]."
- "몇 분 내에 안정적인 속도를 보실 수 있습니다."
- "기술자 방문 시간은 오전 10시–12시 ET입니다."
종료 시기: 발신자가 더 이상의 도움을 거절할 때.
```

고급 대화 흐름
--------

사용 사례가 더 복잡해짐에 따라 모델을 효과적으로 유지하면서 확장되는 구조가 필요합니다. 핵심은 유지 관리 가능성과 단순성의 균형을 맞추는 것입니다: 너무 많은 경직된 상태는 모델에 과부하를 일으켜 성능을 해치고 대화가 로봇적으로 느껴지게 할 수 있습니다.

더 나은 접근법은 모델의 인지된 복잡성을 줄이는 흐름을 설계하는 것입니다. 구조화되었지만 유연한 방식으로 상태를 처리함으로써 모델이 집중하고 반응하기 쉽게 만들어 사용자 경험을 향상시킵니다.

복잡한 시나리오를 관리하는 두 가지 일반적인 패턴:

1. 상태 머신으로서의 대화 흐름
2. session.updates를 통한 동적 대화 흐름

### 상태 머신으로서의 대화 흐름

상태와 전환을 모두 인코딩하는 JSON 구조로 대화를 정의합니다. 이렇게 하면 커버리지에 대해 추론하고, 엣지 케이스를 식별하고, 시간이 지남에 따라 변경 사항을 추적하기 쉽습니다. 코드로 저장되므로 흐름이 발전함에 따라 버전을 관리하고, 차이를 비교하고, 확장할 수 있습니다. 상태 머신은 또한 대화가 한 상태에서 다른 상태로 이동하는 방법과 시기에 대한 세밀한 제어를 제공합니다.

### 예시

**원문**:

```
# Conversation States
[
  {
    "id": "1_greeting",
    "description": "Begin each conversation with a warm, friendly greeting, identifying the service and offering help.",
    "instructions": [
        "Use the company name 'Snowy Peak Boards' and provide a warm welcome.",
        "Let them know upfront that for any account-specific assistance, you'll need some verification details."
    ],
    "examples": [
      "Hello, this is Snowy Peak Boards. Thanks for reaching out! How can I help you today?"
    ],
    "transitions": [{
      "next_step": "2_get_first_name",
      "condition": "Once greeting is complete."
    }, {
      "next_step": "3_get_and_verify_phone",
      "condition": "If the user provides their first name."
    }]
  },
  {
    "id": "2_get_first_name",
    "description": "Ask for the user's name (first name only).",
    "instructions": [
      "Politely ask, 'Who do I have the pleasure of speaking with?'",
      "Do NOT verify or spell back the name; just accept it."
    ],
    "examples": [
      "Who do I have the pleasure of speaking with?"
    ],
    "transitions": [{
      "next_step": "3_get_and_verify_phone",
      "condition": "Once name is obtained, OR name is already provided."
    }]
  },
  {
    "id": "3_get_and_verify_phone",
    "description": "Request phone number and verify by repeating it back.",
    "instructions": [
      "Politely request the user's phone number.",
      "Once provided, confirm it by repeating each digit and ask if it's correct.",
      "If the user corrects you, confirm AGAIN to make sure you understand.",
    ],
    "examples": [
      "I'll need some more information to access your account if that's okay. May I have your phone number, please?",
      "You said 0-2-1-5-5-5-1-2-3-4, correct?",
      "You said 4-5-6-7-8-9-0-1-2-3, correct?"
    ],
    "transitions": [{
      "next_step": "4_authentication_DOB",
      "condition": "Once phone number is confirmed"
    }]
  }
]
```

**한국어 번역**:

```
# 대화 상태
[
  {
    "id": "1_greeting",
    "description": "서비스를 식별하고 도움을 제공하는 따뜻하고 친근한 인사로 각 대화를 시작합니다.",
    "instructions": [
        "회사명 'Snowy Peak Boards'를 사용하고 따뜻한 환영을 제공하세요.",
        "계정별 지원의 경우 일부 확인 세부 사항이 필요하다고 미리 알려주세요."
    ],
    "examples": [
      "안녕하세요, Snowy Peak Boards입니다. 연락해 주셔서 감사합니다! 오늘 어떻게 도와드릴까요?"
    ],
    "transitions": [{
      "next_step": "2_get_first_name",
      "condition": "인사가 완료되면."
    }, {
      "next_step": "3_get_and_verify_phone",
      "condition": "사용자가 이름을 제공하면."
    }]
  },
  {
    "id": "2_get_first_name",
    "description": "사용자의 이름을 요청합니다 (이름만).",
    "instructions": [
      "정중히 '누구와 통화하는 영광을 누리고 있는지요?'라고 물어보세요",
      "이름을 확인하거나 철자를 말하지 마세요; 그냥 받아들이세요."
    ],
    "examples": [
      "누구와 통화하는 영광을 누리고 있는지요?"
    ],
    "transitions": [{
      "next_step": "3_get_and_verify_phone",
      "condition": "이름을 얻었거나 이름이 이미 제공되었을 때."
    }]
  },
  {
    "id": "3_get_and_verify_phone",
    "description": "전화번호를 요청하고 다시 반복하여 확인합니다.",
    "instructions": [
      "사용자의 전화번호를 정중히 요청하세요.",
      "제공되면 각 자릿수를 반복하여 확인하고 맞는지 물어보세요.",
      "사용자가 수정하면 이해했는지 확인하기 위해 다시 확인하세요.",
    ],
    "examples": [
      "계정에 접근하기 위해 추가 정보가 필요합니다. 전화번호를 알려주시겠어요?",
      "0-2-1-5-5-5-1-2-3-4라고 하셨나요, 맞나요?",
      "4-5-6-7-8-9-0-1-2-3라고 하셨나요, 맞나요?"
    ],
    "transitions": [{
      "next_step": "4_authentication_DOB",
      "condition": "전화번호가 확인되면"
    }]
  }
]
```

### 동적 대화 흐름

이 패턴에서 대화는 현재 상태에 따라 시스템 프롬프트와 도구 목록을 업데이트하여 실시간으로 적응합니다. 모델에게 가능한 모든 규칙과 도구를 한 번에 노출하는 대신 대화의 활성 단계와 관련된 것만 제공합니다.

상태의 종료 조건이 충족되면 session.update를 사용하여 전환하고 다음 단계에 필요한 프롬프트와 도구로 교체합니다.

이 접근법은 모델의 인지 부하를 줄여 불필요한 맥락에 산만해지지 않고 복잡한 작업을 더 쉽게 처리할 수 있도록 합니다.

### 예시

**원문**:

```
from typing import Dict, List, Literal

State = Literal["verify", "resolve"]

# Allowed transitions
TRANSITIONS: Dict[State, List[State]] = {
    "verify": ["resolve"],
    "resolve": []  # terminal
}

def build_state_change_tool(current: State) -> dict:
    allowed = TRANSITIONS[current]
    readable = ", ".join(allowed) if allowed else "no further states (terminal)"
    return {
        "type": "function",
        "name": "set_conversation_state",
        "description": (
            f"Switch the conversation phase. Current: '{current}'. "
            f"You may switch only to: {readable}. "
            "Call this AFTER exit criteria are satisfied."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "next_state": {"type": "string", "enum": allowed}
            },
            "required": ["next_state"]
        }
    }

# Minimal business tools per state
TOOLS_BY_STATE: Dict[State, List[dict]] = {
    "verify": [{
        "type": "function",
        "name": "lookup_account",
        "description": "Fetch account by email or phone.",
        "parameters": {
            "type": "object",
            "properties": {"email_or_phone": {"type": "string"}},
            "required": ["email_or_phone"]
        }
    }],
    "resolve": [{
        "type": "function",
        "name": "schedule_technician",
        "description": "Book a technician visit.",
        "parameters": {
            "type": "object",
            "properties": {
                "account_id": {"type": "string"},
                "window": {"type": "string", "enum": ["10-12 ET", "14-16 ET"]}
            },
            "required": ["account_id", "window"]
        }
    }]
}

# Short, phase-specific instructions
INSTRUCTIONS_BY_STATE: Dict[State, str] = {
    "verify": (
        "# Role & Objective\n"
        "Verify identity to access the account.\n\n"
        "# Conversation (Verify)\n"
        "- Ask for the email or phone on the account.\n"
        "- Read back digits one-by-one (e.g., '4-1-5… Is that correct?').\n"
        "Exit when: Account ID is returned.\n"
        "When exit is satisfied: call set_conversation_state(next_state=\"resolve\")."
    ),
    "resolve": (
        "# Role & Objective\n"
        "Apply a fix by booking a technician.\n\n"
        "# Conversation (Resolve)\n"
        "- Offer two windows: '10–12 ET' or '2–4 ET'.\n"
        "- Book the chosen window.\n"
        "Exit when: Appointment is confirmed.\n"
        "When exit is satisfied: end the call politely."
    )
}

def build_session_update(state: State) -> dict:
    """Return the JSON payload for a Realtime `session.update` event."""
    return {
        "type": "session.update",
        "session": {
            "instructions": INSTRUCTIONS_BY_STATE[state],
            "tools": TOOLS_BY_STATE[state] + [build_state_change_tool(state)]
        }
    }
```

**한국어 번역**:

```
from typing import Dict, List, Literal

State = Literal["verify", "resolve"]

# 허용된 전환
TRANSITIONS: Dict[State, List[State]] = {
    "verify": ["resolve"],
    "resolve": []  # 터미널
}

def build_state_change_tool(current: State) -> dict:
    allowed = TRANSITIONS[current]
    readable = ", ".join(allowed) if allowed else "추가 상태 없음 (터미널)"
    return {
        "type": "function",
        "name": "set_conversation_state",
        "description": (
            f"대화 단계를 전환합니다. 현재: '{current}'. "
            f"다음으로만 전환할 수 있습니다: {readable}. "
            "종료 기준이 충족된 후에 호출하세요."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "next_state": {"type": "string", "enum": allowed}
            },
            "required": ["next_state"]
        }
    }

# 상태별 최소한의 비즈니스 도구
TOOLS_BY_STATE: Dict[State, List[dict]] = {
    "verify": [{
        "type": "function",
        "name": "lookup_account",
        "description": "이메일이나 전화로 계정을 가져옵니다.",
        "parameters": {
            "type": "object",
            "properties": {"email_or_phone": {"type": "string"}},
            "required": ["email_or_phone"]
        }
    }],
    "resolve": [{
        "type": "function",
        "name": "schedule_technician",
        "description": "기술자 방문을 예약합니다.",
        "parameters": {
            "type": "object",
            "properties": {
                "account_id": {"type": "string"},
                "window": {"type": "string", "enum": ["10-12 ET", "14-16 ET"]}
            },
            "required": ["account_id", "window"]
        }
    }]
}

# 짧고 단계별 지시사항
INSTRUCTIONS_BY_STATE: Dict[State, str] = {
    "verify": (
        "# 역할 및 목표\n"
        "계정에 접근하기 위해 신원을 확인합니다.\n\n"
        "# 대화 (확인)\n"
        "- 계정의 이메일이나 전화를 요청하세요.\n"
        "- 숫자를 하나씩 읽어주세요 (예: '4-1-5… 맞나요?').\n"
        "종료 시기: 계정 ID가 반환될 때.\n"
        "종료가 충족되면: set_conversation_state(next_state=\"resolve\")를 호출하세요."
    ),
    "resolve": (
        "# 역할 및 목표\n"
        "기술자를 예약하여 수정을 적용합니다.\n\n"
        "# 대화 (해결)\n"
        "- 두 개의 시간대를 제공하세요: '10–12 ET' 또는 '2–4 ET'.\n"
        "- 선택된 시간대를 예약하세요.\n"
        "종료 시기: 약속이 확인될 때.\n"
        "종료가 충족되면: 정중히 통화를 종료하세요."
    )
}

def build_session_update(state: State) -> dict:
    """Realtime `session.update` 이벤트에 대한 JSON 페이로드를 반환합니다."""
    return {
        "type": "session.update",
        "session": {
            "instructions": INSTRUCTIONS_BY_STATE[state],
            "tools": TOOLS_BY_STATE[state] + [build_state_change_tool(state)]
        }
    }
```

안전 및 에스컬레이션
-----------

종종 Realtime 음성 에이전트에서는 인간에게 에스컬레이션하는 신뢰할 수 있는 방법이 중요합니다. 이 섹션에서는 사용 사례에 따라 언제 에스컬레이션해야 하는지에 대한 지시사항을 수정해야 합니다.

* **사용 시기**: 모델이 인간이나 대체 시스템에 적절히 에스컬레이션할 시기를 결정하는 데 어려움이 있을 때.
* **효과**: 빠르고 신뢰할 수 있는 에스컬레이션과 무엇을 말해야 하는지 정의합니다.
* **적용 방법**: 자신만의 임계값과 모델이 말해야 하는 것을 삽입합니다.

### 예시

**원문**:

```
# Safety & Escalation
When to escalate (no extra troubleshooting):
- Safety risk (self-harm, threats, harassment)
- User explicitly asks for a human
- Severe dissatisfaction (e.g., "extremely frustrated," repeated complaints, profanity)
- **2** failed tool attempts on the same task **or** **3** consecutive no-match/no-input events
- Out-of-scope or restricted (e.g., real-time news, financial/legal/medical advice)
What to say at the same time of calling the escalate_to_human tool (MANDATORY):
- "Thanks for your patience—I'm connecting you with a specialist now."
- Then call the tool: `escalate_to_human`
Examples that would require escalation:
- "This is the third time the reset didn't work. Just get me a person."
- "I am extremely frustrated!"
```

**한국어 번역**:

```
# 안전 및 에스컬레이션
에스컬레이션할 때 (추가 문제 해결 없음):
- 안전 위험 (자해, 위협, 괴롭힘)
- 사용자가 명시적으로 인간을 요청
- 심한 불만 (예: "극도로 좌절됨", 반복적인 불만, 욕설)
- 동일한 작업에서 **2번** 도구 시도 실패 **또는** **3번** 연속 일치하지 않음/입력 없음 이벤트
- 범위를 벗어나거나 제한됨 (예: 실시간 뉴스, 금융/법률/의료 조언)
escalate_to_human 도구를 호출하는 동시에 말해야 할 것 (필수):
- "인내심을 가져주셔서 감사합니다—지금 전문가에게 연결해 드리겠습니다."
- 그 다음 도구를 호출하세요: `escalate_to_human`
에스컬레이션이 필요한 예시:
- "이번이 리셋이 작동하지 않은 세 번째입니다. 그냥 사람을 연결해 주세요."
- "저는 극도로 좌절됩니다!"
```

새로운 realtime 모델은 지시사항을 더 잘 따르고 더 신뢰할 수 있게 인간에게 에스컬레이션할 수 있습니다.

결론
--

이 가이드는 OpenAI의 새로운 **gpt-realtime** 모델을 효과적으로 사용하기 위한 포괄적인 프롬프팅 전략을 제공합니다. 각 섹션의 지침을 따르고 제공된 예시를 적용하여 더 자연스럽고 효과적인 음성 AI 상호작용을 구축할 수 있습니다.

핵심은 명확하고 구조화된 프롬프트를 작성하되 충분한 유연성을 유지하여 모델이 자연스럽고 매력적인 대화를 생성할 수 있도록 하는 것입니다. 지속적인 반복과 테스트를 통해 특정 사용 사례에 맞는 최적의 프롬프팅 전략을 찾을 수 있습니다.

읽어주셔서 감사합니다 😸