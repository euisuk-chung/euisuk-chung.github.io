---
title: "[OpenAI] GPT Realtime API: 음성 기반 AI 에이전트의 새로운 전환점"
date: "2025-08-31"
tags:
  - "OpenAI"
  - "chatGPT"
year: "2025"
---

# [OpenAI] GPT Realtime API: 음성 기반 AI 에이전트의 새로운 전환점


![](https://velog.velcdn.com/images/euisuk-chung/post/f8335bf1-fe46-41f6-be88-b1336ec10916/image.png)

> <https://youtu.be/nfBbmtMJhX0>

OpenAI GPT-Realtime
===================

> *프로덕션 수준의 음성 AI 에이전트를 위한 혁신적인 Speech-to-Speech 모델*

들어가며
----

음성 인터페이스는 인간이 AI와 상호작용하는 가장 자연스러운 방식 중 하나입니다. 고객 지원부터 교육, 헬스케어까지 다양한 산업에서 인간 수준의 음성 품질을 가진 AI 경험에 대한 수요가 급증하고 있습니다. 최근 OpenAI는 이러한 시장 요구에 응답하여 **GPT-Realtime**이라는 새로운 Speech-to-Speech 모델과 함께 **Realtime API**의 정식 출시를 발표했습니다.

이번 발표는 단순히 기존 모델의 업그레이드를 넘어서, 전통적인 Speech-to-Text → Text-to-Speech 파이프라인의 한계를 극복하는 혁신적인 접근 방식을 제시합니다. 본 블로그에서는 GPT-Realtime의 핵심 기능, 기술적 개선사항, 그리고 실제 기업 활용 사례를 통해 음성 AI의 새로운 패러다임을 살펴보겠습니다.

배경: Speech-to-Speech 모델의 아키텍처적 우위
---------------------------------

### 전통적인 음성 AI 파이프라인의 한계

기존의 음성 AI 시스템은 다음과 같은 다단계 처리 과정을 거쳤습니다:

1. **Speech-to-Text (STT)**: 음성을 텍스트로 변환
2. **Text Processing**: 언어 모델이 텍스트를 처리하여 응답 생성
3. **Text-to-Speech (TTS)**: 응답 텍스트를 음성으로 변환

![](https://velog.velcdn.com/images/euisuk-chung/post/8f6222fc-e4a9-44f2-8fd5-d45a61a03a3f/image.png)

이러한 체인 방식은 여러 모델을 연결하면서 다음과 같은 문제점들을 야기했습니다:

* **레이턴시 증가**: 각 단계별 처리 시간이 누적됨
* **뉘앙스 손실**: 음성의 감정적 요소나 비언어적 신호가 텍스트 변환 과정에서 소실
* **복잡한 구현**: 여러 모델 간의 통합 및 최적화 복잡성

### Speech-to-Speech 모델의 혁신적 접근

GPT-Realtime은 이러한 한계를 극복하기 위해 **end-to-end Speech-to-Speech** 아키텍처를 채택했습니다:

```
# 전통적인 방식
audio_input → STT_model → text → LLM → response_text → TTS_model → audio_output

# GPT-Realtime 방식  
audio_input → GPT_Realtime → audio_output
```

![](https://velog.velcdn.com/images/euisuk-chung/post/342a825b-917c-42fa-b225-f6a2e942430e/image.png)

이 단일 모델 접근법은 다음과 같은 아키텍처적 우위를 제공합니다:

* **저지연 처리**: 단일 모델을 통한 직접적인 audio-to-audio 변환
* **뉘앙스 보존**: 웃음, 한숨 같은 비언어적 신호까지 이해하고 생성
* **자연스러운 감정 표현**: 광범위한 감정 스펙트럼으로 인간다운 음성 생성
* **언어 전환**: 문장 중간에서도 매끄러운 언어 변환 가능

GPT-Realtime의 핵심 기능 분석
----------------------

> OpenAI Blog: <https://openai.com/index/introducing-gpt-realtime/>

### 1. 오디오 품질 혁신

GPT-Realtime은 실제 대화에서 중요한 자연스러운 억양, 감정, 속도를 구현할 수 있도록 훈련되었습니다.  
모델은 다음과 같은 세밀한 지시사항을 따를 수 있습니다:

**Original Prompt:**

```
"speak quickly and professionally"
"speak empathetically in a French accent"
```

**Korean Translation:**

```
"빠르고 전문적으로 말해주세요"
"프랑스 억양으로 공감적으로 말해주세요"
```

새롭게 출시된 두 개의 음성인 **Marin**과 **Cedar**는 가장 큰 개선을 보여주며, 기존 8개 음성도 이러한 개선사항을 반영하여 업데이트되었습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/b12d2b1c-5d74-493c-9637-b92d82dcbff4/image.png)

> OpenAI Blog: <https://openai.com/index/introducing-gpt-realtime/>

### 2. 지능성과 이해 능력 향상

GPT-Realtime은 Big Bench Audio 평가에서 **82.8%의 정확도**를 달성하여, 2024년 12월 모델의 65.6%를 크게 상회했습니다.

| 모델 | Big Bench Audio 정확도 |
| --- | --- |
| gpt-realtime | 82.8% |
| gpt-4o-realtime-preview-2025-06-03 | 81.5% |
| gpt-4o-realtime-preview-2024-12-17 | 65.6% |

![](https://velog.velcdn.com/images/euisuk-chung/post/4f6ebb85-5adf-4336-b3d4-5ce50cfef2a1/image.png)

> OpenAI Blog: <https://openai.com/index/introducing-gpt-realtime/>

모델의 개선된 이해 능력은 다음과 같은 특징들로 나타납니다:

* **비언어적 신호 인식**: 웃음, 한숨 등의 감지
* **실시간 언어 전환**: 문장 중간에서도 자연스러운 언어 변경
* **톤 적응**: "간결하고 전문적" vs "친절하고 공감적" 스타일 구분
* **다국어 영숫자 인식**: 전화번호, VIN 등을 스페인어, 중국어, 일본어, 프랑스어로 정확히 인식

### 3. 명령 준수 성능

MultiChallenge Audio 벤치마크에서 GPT-Realtime은 **30.5%의 정확도**를 기록하여, 이전 모델 대비 상당한 개선을 보여주었습니다.

| 모델 | MultiChallenge Audio 정확도 |
| --- | --- |
| gpt-realtime | 30.5% |
| gpt-4o-realtime-preview-2025-06-03 | 26.5% |
| gpt-4o-realtime-preview-2024-12-17 | 20.6% |

![](https://velog.velcdn.com/images/euisuk-chung/post/bddcfcb0-d7f5-4cc0-8602-396e9b4f33b7/image.png)

> OpenAI Blog: <https://openai.com/index/introducing-gpt-realtime/>

이러한 개선은 개발자가 설정한 시스템 지시사항에 대한 모델의 높은 충실도를 의미합니다.

### 4. 함수 호출 최적화

ComplexFuncBench Audio 평가에서 GPT-Realtime은 **66.5%의 정확도**를 달성했습니다:

| 모델 | ComplexFuncBench Audio 정확도 |
| --- | --- |
| gpt-realtime | 66.5% |
| gpt-4o-realtime-preview-2025-06-03 | 58.9% |
| gpt-4o-realtime-preview-2024-12-17 | 49.7% |

![](https://velog.velcdn.com/images/euisuk-chung/post/49645c02-87c0-40c8-935a-1f995d26183c/image.png)

> OpenAI Blog: <https://openai.com/index/introducing-gpt-realtime/>

개선된 함수 호출 능력의 세 가지 축:

1. **관련 함수 호출**: 상황에 적합한 함수 선택
2. **적절한 타이밍**: 함수를 호출해야 할 최적의 순간 판단
3. **정확한 인자**: 함수 실행에 필요한 올바른 매개변수 전달

또한 **비동기 함수 호출** 기능도 향상되어, 장시간 실행되는 함수 호출이 대화의 흐름을 방해하지 않도록 개선되었습니다.

Realtime API의 새로운 기능들
---------------------

![](https://velog.velcdn.com/images/euisuk-chung/post/92c5a971-6deb-437c-b6be-eaf9c3fb86bf/image.png)

> <https://youtu.be/nfBbmtMJhX0>

### 1. 원격 MCP 서버 지원

**MCP(Model Context Protocol) 지원**을 통해 개발자들은 음성 에이전트에 새로운 기능을 쉽게 추가할 수 있습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/ba795d94-bc00-44b1-9ef5-54cf78ff1ccd/image.png)

> OpenAI Blog: <https://openai.com/index/introducing-gpt-realtime/>

```
// POST /v1/realtime/client_secrets - 실시간 클라이언트 시크릿 생성
{
  "session": {
    "type": "realtime", // 실시간 세션 타입
    "tools": [
      {
        "type": "mcp", // MCP 도구 타입
        "server_label": "stripe", // Stripe 서버 라벨
        "server_url": "https://mcp.stripe.com", // MCP 서버 URL
        "authorization": "{access_token}", // 접근 토큰
        "require_approval": "never" // 승인 요구 설정: 없음
      }
    ]
  }
}
```

> For more, go to OpenAI Guide, <https://platform.openai.com/docs/guides/realtime-conversations>

### 2. 이미지 입력 지원

이제 GPT-Realtime은 오디오나 텍스트와 함께 이미지, 사진, 스크린샷을 처리할 수 있습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/67b56048-86d1-4b53-8523-a2aebd3d37df/image.png)

> OpenAI Blog: <https://openai.com/index/introducing-gpt-realtime/>

```
{
    "type": "conversation.item.create", // 대화 아이템 생성
    "previous_item_id": null, // 이전 아이템 ID (없음)
    "item": {
        "type": "message", // 메시지 타입
        "role": "user", // 사용자 역할
        "content": [
            {
                "type": "input_image", // 입력 이미지 타입
                "image_url": "data:image/{format(example: png)};base64,{some_base64_image_bytes}" // Base64 인코딩된 이미지 데이터
            }
        ]
    }
}
```

> For more, go to OpenAI Guide, <https://platform.openai.com/docs/guides/realtime-conversations>

### 3. 추가적인 프로덕션 기능들

* **SIP(Session Initiation Protocol) 지원**: 공중전화망, PBX 시스템, 데스크폰과의 직접 연결
* **재사용 가능한 프롬프트**: 개발자 메시지, 도구, 변수, 예제 대화를 세션 간에 재사용
* **EU 데이터 레지던시**: 유럽 기반 애플리케이션을 위한 완전한 지원
* **향상된 컨텍스트 관리**: 토큰 제한 설정 및 다중 턴 대화 절단 기능

실제 활용 사례: T-Mobile의 혁신적인 고객 서비스
-------------------------------

![](https://velog.velcdn.com/images/euisuk-chung/post/098285da-4b57-4638-a48d-3e28f1105986/image.png)

> <https://youtu.be/nfBbmtMJhX0>

### 기업 구현 사례 분석

T-Mobile은 GPT-Realtime을 활용하여 디바이스 업그레이드 프로세스를 혁신적으로 개선했습니다.  
이들의 접근 방식은 다음과 같은 핵심 철학을 반영합니다:

**Shini Gopalan (T-Mobile COO)의 통찰:**

> *AI를 사용해 10% 더 나은 IVR을 구축하려고 하면 AI에 대한 사고가 잘못된 것입니다.*  
> *이 기술을 사용해 기존 프로세스를 완전히 파괴하고 처음부터 다시 구축해야 합니다.*

![](https://velog.velcdn.com/images/euisuk-chung/post/110514ff-e1b6-4f45-aa01-37e6de02cdad/image.png)

> <https://youtu.be/nfBbmtMJhX0>

### 실제 대화 시나리오

다음은 T-Mobile의 GPT-Realtime 기반 고객 서비스 데모입니다:

**Original Conversation:**

```
Customer: "Yeah, my daughter Rachel dropped her phone in the lake and I just need a new one. Stat."

AI: "Oh, no. I'm sorry that happened. Let's make sure we get a solid replacement quickly. Are you looking for something with stronger water resistance?"

Customer: "Honestly, I'm just looking for something cheap, something under $300."

AI: "Got it. Let me show you some options under $300..."

Customer: "Yeah, this Revel 8 phone from T-Mobile, is that compatible with T-Mobile satellite services?"

AI: "The Revel 8 phone is compatible with T-Mobile satellite services. It currently supports text messaging, including text to 911 and location sharing."
```

**Korean Translation:**

```
고객: "네, 제 딸 Rachel이 휴대폰을 호수에 떨어뜨려서 새 폰이 급히 필요해요."

AI: "아, 안됐네요. 빠르게 견고한 대체품을 찾아드리겠습니다. 더 강한 방수 기능이 있는 제품을 찾고 계신가요?"

고객: "솔직히 저렴한 걸 찾고 있어요. 300달러 미만으로요."

AI: "알겠습니다. 300달러 미만의 옵션들을 보여드리겠습니다..."

고객: "네, T-Mobile의 이 Revel 8 폰이 T-Mobile 위성 서비스와 호환되나요?"

AI: "Revel 8 폰은 T-Mobile 위성 서비스와 호환됩니다. 현재 911 문자 포함한 문자 메시징과 위치 공유를 지원합니다."
```

### 기업 도입의 핵심 성공 요인

T-Mobile 사례에서 도출할 수 있는 주요 교훈들:

1. **프로세스 재설계**: 기존 시스템의 점진적 개선이 아닌 완전한 재구축
2. **브랜드 일치성**: AI 구현이 회사의 핵심 가치와 문화에 부합
3. **고객 중심 접근**: 복잡한 프로세스를 자연스러운 대화로 단순화
4. **Expert-in-Pocket**: 언제 어디서나 전문가 수준의 서비스 제공

보안 및 개인정보보호
-----------

### 안전 장치 및 완화 방안

Realtime API는 오용 방지를 위한 다층적 안전 장치를 구현합니다:

1. **실시간 분류기**: API 세션에서 유해한 콘텐츠 가이드라인 위반 시 대화 중단
2. **프리셋 음성**: 악의적인 사용자의 타인 사칭 방지
3. **개발자 안전 가이드라인**: Agents SDK를 통한 추가적인 안전 장치 구현 가능

### 개인정보보호 정책

* **EU 데이터 레지던시**: 유럽 기반 애플리케이션을 위한 완전한 지원
* **기업 개인정보보호 약속**: 엔터프라이즈급 개인정보보호 보장
* **사용 정책**: 스팸, 기만, 기타 유해 목적으로의 출력 재목적화 또는 배포 금지
* **AI 상호작용 명시**: 사용자가 AI와 상호작용하고 있음을 명확히 표시해야 함

가격 정책 및 비용 최적화
--------------

### 새로운 가격 구조

GPT-Realtime은 기존 대비 **20% 가격 인하**를 제공합니다:

| 항목 | 가격 |
| --- | --- |
| 오디오 입력 토큰 | $32 / 1M 토큰 |
| 캐시된 입력 토큰 | $0.40 / 1M 토큰 |
| 오디오 출력 토큰 | $64 / 1M 토큰 |

> GPT-Realtime의 가격 모델에서 오디오는 초당 24토큰으로 계산되므로, 긴 대화에서는 토큰 사용량이 급격히 증가할 수 있습니다.

실제 서비스에서는 중요도나 감정적 맥락에 따라 특정 대화 턴을 우선적으로 보존하는 더 정교한 알고리즘을 구현할 수 있습니다.

실전 프로젝트 가이드
-----------

아래는 해당 API를 사용할 수 있는 몇가지 실전 프로젝트입니다.

### 프로젝트 1: 고객 지원 봇 구축

```
def create_customer_support_bot():
    """고객 지원 봇 생성 함수"""
    system_prompt = """
    당신은 TechCorp의 전문 고객 지원 상담원입니다.
    가이드라인:
    - 항상 정중하고 공감적으로 응대하세요
    - 문제를 단계별로 해결하세요
    - 복잡한 이슈는 인간 상담원에게 에스컬레이션하세요
    - 승인 없이는 50달러를 초과하는 환불을 약속하지 마세요
    """
    
    tools = [
        {
            "type": "function", # 함수 타입
            "function": {
                "name": "check_order_status", # 주문 상태 확인
                "description": "Check customer order status", # 고객 주문 상태 확인
                "parameters": {
                    "type": "object",
                    "properties": {
                        "order_id": {"type": "string"} # 주문 ID
                    },
                    "required": ["order_id"] # 필수 매개변수
                }
            }
        }
    ]
    
    return {
        "system_prompt": system_prompt, # 시스템 프롬프트
        "tools": tools, # 사용 도구들
        "voice": "marin", # 음성 선택
        "response_format": {"type": "audio"} # 오디오 응답 형식
    }
```

이 고객 지원 봇 예제는 실제 비즈니스 환경에서 중요한 원칙들을 반영합니다.

시스템 프롬프트에서 환불 한도를 명시한 것은 GPT-Realtime의 뛰어난 명령 준수 능력을 활용한 것으로, T-Mobile 데모에서 보여준 것처럼 모델이 정책을 정확히 따르도록 보장합니다.

실제 구현 시에는 주문 조회 외에도 반품 처리, 기술 지원, FAQ 검색 등 다양한 도구를 추가할 수 있습니다.

### 프로젝트 2: 교육용 AI 튜터

```
class AITutor:
    """AI 튜터 클래스"""
    def __init__(self, subject="mathematics"):
        self.subject = subject # 과목
        self.student_progress = {} # 학생 진도 추적
        
    def create_tutoring_session(self, student_level):
        """튜터링 세션 생성"""
        system_prompt = f"""
        당신은 {self.subject} 전문 튜터입니다.
        학생 수준: {student_level}
        
        교육 접근법:
        - 소크라테스식 방법 사용 - 유도 질문하기
        - 단계별 설명 제공
        - 학생의 사고를 격려
        - 학생 응답에 따라 난이도 조절
        """
        
        return {
            "system_prompt": system_prompt, # 시스템 프롬프트
            "voice": "cedar",  # 교육에 더 적합한 음성
            "tools": self._get_educational_tools() # 교육용 도구들
        }
    
    def _get_educational_tools(self):
        """교육용 도구 반환"""
        return [
            {
                "type": "function", # 함수 타입
                "function": {
                    "name": "generate_practice_problem", # 연습 문제 생성
                    "description": "Generate practice problems", # 연습 문제 생성
                    "parameters": {
                        "type": "object", 
                        "properties": {
                            "difficulty": {"type": "string"}, # 난이도
                            "topic": {"type": "string"} # 주제
                        }
                    }
                }
            }
        ]
```

교육용 AI 튜터는 GPT-Realtime의 감정 표현과 실시간 적응 능력을 최대한 활용하는 사례입니다.

* `student_progress` 딕셔너리는 개인화된 학습 경험을 위해 학생별 진도와 약점을 추적할 수 있는 확장 가능한 구조를 제공합니다.

실제 교육 서비스에서는 학습 분석, 성과 평가, 부모 리포트 기능 등을 추가로 구현할 수 있습니다.

향후 발전 방향과 전망
------------

### 1. 기술적 혁신 영역

GPT-Realtime의 등장은 다음과 같은 기술적 발전을 예고합니다:

* **다중 언어 동시 지원**: 실시간으로 여러 언어를 혼용하는 글로벌 비즈니스 환경 지원
* **감정 지능 향상**: 더 정교한 감정 인식 및 표현 능력
* **도메인 특화**: 의료, 법률, 금융 등 전문 분야별 최적화 모델
* **실시간 학습**: 사용자와의 상호작용을 통한 개인화 학습

### 2. 산업별 적용 확산

**헬스케어**

* 환자 상담 및 진료 보조
* 정신 건강 상담 봇
* 의료진 교육 도구

**교육**

* 개인화된 언어 학습
* STEM 과목 튜터링
* 특수 교육 지원

**금융**

* 투자 상담 서비스
* 보험 클레임 처리
* 금융 상품 안내

**엔터테인먼트**

* 인터랙티브 스토리텔링
* 게임 내 NPC
* 가상 아바타 서비스

### 3. 윤리적 고려사항

음성 AI 기술의 발전과 함께 고려해야 할 윤리적 이슈들:

* **딥페이크 및 음성 복제 방지**
* **사용자 동의 및 투명성**
* **편향성 완화 및 공정성**
* **데이터 보안 및 개인정보보호**

마무리
---

OpenAI GPT-Realtime의 출시는 음성 AI 기술에 있어서 중요한 전환점을 의미합니다. 전통적인 다단계 파이프라인의 한계를 극복하고, 인간 수준의 자연스러운 대화가 가능한 Speech-to-Speech 모델은 다양한 산업 분야에서 혁신적인 변화를 이끌어낼 것으로 예상됩니다.

특히 T-Mobile 사례에서 보듯이, AI를 단순히 기존 프로세스 개선 도구로 보는 것이 아니라 완전히 새로운 고객 경험을 창조하는 플랫폼으로 접근할 때 진정한 가치를 실현할 수 있습니다. 개발자들은 이러한 새로운 가능성을 활용하여 더욱 직관적이고 효과적인 음성 기반 애플리케이션을 구축할 수 있게 되었습니다.

GPT-Realtime과 Realtime API의 정식 출시로 시작된 이 새로운 시대에서, 음성 AI는 단순한 기술적 도구를 넘어 인간과 기계 간의 소통 방식을 근본적으로 변화시키는 촉매제 역할을 할 것입니다. 향후 이 기술이 어떻게 발전하고 우리의 일상과 업무에 어떤 변화를 가져올지 기대해봅니다.

오늘도 읽어주셔서 감사합니다 🌠