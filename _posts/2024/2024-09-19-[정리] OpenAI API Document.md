---
title: "[정리] OpenAI API Document"
date: "2024-09-19"
tags:
  - "OpenAI"
year: "2024"
---

# [정리] OpenAI API Document

원본 게시글: https://velog.io/@euisuk-chung/정리-OpenAI-API-Document



OpenAI는 최신 인공지능(AI) 모델과 API를 제공하여 개발자들이 다양한 AI 기능을 쉽게 애플리케이션에 통합할 수 있도록 지원합니다. 다음은 아래 `platform.openai.com`에서 제공하는 문서를 훑어보면서 정리한 내용입니다.

* 참고 문서: <https://platform.openai.com/docs/overview>

1. 소개
-----

OpenAI를 활용하면, 자연어 처리, 이미지 생성, 음성 인식 등 다양한 AI 작업을 간단하게 구현할 수 있으며, 사용자 경험을 혁신적으로 개선할 수 있습니다. 이제 업무에서도 슬슬 사용하게 될 것 같아 이를 제대로 한번 살펴보는 시간을 가져보았습니다 ⭐

![](https://velog.velcdn.com/images/euisuk-chung/post/eb65a892-ef89-4b15-b75a-038b2f7057d7/image.png)

이 가이드는 (위에 블록 표기해 둔) OpenAI API의 주요 엔드포인트와 6가지 주요 기능을 중심으로, 초보자도 쉽게 따라할 수 있는 단계별 설명을 제공합니다.

---

2. OpenAI API의 기본 구조
--------------------

OpenAI API는 **사전 학습된 AI 모델**을 호출하여 다양한 작업을 수행할 수 있게 합니다. API는 여러 가지 **엔드포인트(Endpoints)**를 제공하며, 각 엔드포인트는 특정 작업을 처리하는 역할을 합니다. API의 구조는 간단하지만 매우 강력하며, 이를 통해 AI 기능을 직관적으로 사용할 수 있습니다.

### 2.1 엔드포인트란?

**엔드포인트**는 OpenAI 서버와 상호작용하는 URL로, 특정 AI 모델을 호출하거나 기능을 수행할 때 사용하는 경로입니다.

* 예를 들어, GPT 모델을 호출하려면 `/v1/completions` 엔드포인트로 요청을 보내야 합니다.
  
  + `openai.ChatCompletion.create()`와 같은 함수 호출은 내부적으로 OpenAI API의 `/v1/completions` 엔드포인트로 요청을 보내는 방식입니다.
  + `OpenAI 라이브러리`를 사용할 때, 이런 함수들은 각각의 엔드포인트와 매핑되어 있어서, 개발자는 API의 엔드포인트 **URL을 신경 쓰지 않고도 편리하게 AI 기능을 사용**할 수 있습니다.

---

3. 주요 엔드포인트 및 역할
----------------

OpenAI는 다양한 AI 기능을 제공하는 여러 엔드포인트를 가지고 있으며, 각 엔드포인트는 고유한 역할을 수행합니다. 이 포스팅에서는 자주 사용되는 주요 엔드포인트와 그 역할을 설명하고, 각 엔드포인트에 대한 간단한 코드 예시를 제공하겠습니다.

### 3.1 Chat Completions 엔드포인트

* **URL**: `/v1/chat/completions`
* **역할**: 대화형 AI 응답을 생성합니다. ChatGPT와 유사하게 대화형 프롬프트를 받아 사용자의 질문에 문맥에 맞는 응답을 제공합니다.
* **사용 예**: 챗봇, 고객 지원, 대화형 가이드, 가상 비서.
* **예시 코드**:

```
import openai

openai.api_key = "your-api-key"

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain the basics of quantum computing."}
    ]
)

print(response.choices[0].message['content'])
```
### 3.2 Fine-tuning 엔드포인트

* **URL**: `/v1/fine-tuning`
* **역할**: 사전 훈련된 모델을 사용자의 특정 데이터에 맞게 추가로 훈련시킵니다. 이를 통해 특정 도메인이나 작업에 대한 성능을 향상시킬 수 있습니다.
* **사용 예**: 의료 데이터에 특화된 텍스트 생성, 특정 브랜드 언어 스타일을 학습한 AI 모델.
* **예시 코드**:

```
import openai

openai.api_key = "your-api-key"

response = openai.FineTune.create(
    training_file="file-abc123",
    model="gpt-4"
)

print(response)
```
### 3.3 Batch 엔드포인트

* **URL**: `/v1/batch`
* **역할**: 대량의 요청을 비동기적으로 처리합니다. 대규모 데이터셋에 대한 평가, 분류, 임베딩 생성 작업을 동시에 수행할 수 있습니다.
* **사용 예**: 대규모 문서 분류, 감성 분석, 대량 텍스트 임베딩 생성.
* **예시 코드**:

```
import openai

openai.api_key = "your-api-key"

response = openai.Batch.create(
    model="gpt-4",
    tasks=[{"prompt": "Analyze sentiment of this text"}, {"prompt": "Summarize this document"}]
)

print(response)
```
### 3.4 Image Generation 엔드포인트 (DALL·E)

* **URL**: `/v1/images/generations`
* **역할**: 텍스트 설명을 기반으로 이미지를 생성합니다. 창의적이고 독창적인 이미지 제작에 활용할 수 있습니다.
* **사용 예**: 마케팅 이미지 생성, 그래픽 디자인, 콘셉트 아트.
* **예시 코드**:

```
import openai

openai.api_key = "your-api-key"

response = openai.Image.create(
    prompt="A futuristic cityscape with flying cars",
    n=1,
    size="1024x1024"
)

image_url = response['data'][0]['url']
print("Generated image URL:", image_url)
```
### 3.5 Text to Speech 엔드포인트

* **URL**: `/v1/audio/generations`
* **역할**: 텍스트를 자연스러운 음성으로 변환합니다. 다양한 음성을 지원하며, 음성의 속도와 톤을 조절할 수 있습니다.
* **사용 예**: 오디오북 제작, 음성 안내 시스템, 접근성 향상 도구.
* **예시 코드**:

```
import openai

openai.api_key = "your-api-key"

response = openai.Audio.create(
    model="gpt-4",
    input="This is a test of the text to speech conversion."
)

print(response['data'])
```
### 3.6 Speech to Text 엔드포인트 (Whisper)

* **URL**: `/v1/audio/transcriptions`
* **역할**: 음성 파일을 텍스트로 변환합니다. 다양한 언어와 악센트를 지원하며, 높은 정확도의 음성 인식을 제공합니다.
* **사용 예**: 회의록 자동 생성, 자막 생성, 음성 명령 시스템.
* **예시 코드**:

```
import openai

openai.api_key = "your-api-key"

audio_file = open("audio.wav", "rb")
response = openai.Audio.transcribe(
    model="whisper-1",
    file=audio_file
)

print("Transcribed text:", response['text'])
```
### 3.7 Embeddings 엔드포인트

* **URL**: `/v1/embeddings`
* **역할**: 텍스트를 고차원 벡터로 변환하여 의미적 유사성을 계산할 수 있습니다. 검색 엔진, 추천 시스템 등에서 활용됩니다.
* **사용 예**: 텍스트 유사도 분석, 검색 최적화, 추천 시스템.
* **예시 코드**:

```
import openai

openai.api_key = "your-api-key"

response = openai.Embedding.create(
    input="OpenAI provides powerful AI models",
    model="text-embedding-ada-002"
)

embedding_vector = response['data'][0]['embedding']
print("Embedding vector:", embedding_vector)
```
### 3.8 Moderation 엔드포인트

* **URL**: `/v1/moderations`
* **역할**: 입력된 텍스트의 안전성을 평가합니다. 혐오 발언, 폭력적 표현, 성적 콘텐츠 등을 탐지하고 차단할 수 있습니다.
* **사용 예**: 온라인 플랫폼의 콘텐츠 필터링, 안전한 대화 환경 유지.
* **예시 코드**:

```
import openai

openai.api_key = "your-api-key"

response = openai.Moderation.create(
    input="This is a sample text that might contain harmful content."
)

print(response['results'])
```

---

4. OpenAI의 6가지 주요 Capabilities
------------------------------

OpenAI API는 다양한 기능을 제공하며, 이를 통해 텍스트 생성, 이미지 처리, 음성 인식 등 다양한 작업을 수행할 수 있습니다. 여기에서는 OpenAI의 6가지 주요 **Capabilities**에 대해 설명합니다.

### 4.1 텍스트 생성 (Text Generation)

텍스트 생성은 OpenAI API의 가장 기본적이면서도 강력한 기능 중 하나입니다. **GPT-4**와 같은 언어 모델을 사용하여 사용자 프롬프트에 기반한 다양한 텍스트를 생성할 수 있습니다.

* **예시 코드**:

```
response = openai.Completion.create(
    model="gpt-4",
    prompt="Write a story about a brave knight who fights a dragon.",
    max_tokens=200
)

print(response.choices[0].text.strip())
```
### 4.2 이미지 처리 (Vision)

OpenAI의 **DALL·E** 모델은 텍스트 설명을 기반으로 이미지를 생성하는 데 사용됩니다. 이 기능을 사용하여 창의적이고 독창적인 이미지를 만들 수 있습니다.

* **예시 코드**:

```
response = openai.Image.create(
    prompt="A painting of a futuristic landscape with mountains and flying cars.",
    n=1,
    size="1024x1024"
)

image_url = response['data'][0]['url']
print("Generated image URL:", image_url)
```
### 4.3 함수 호출 (Function Calling)

OpenAI 모델은 외부 API나 내부 함수 호출을 지원합니다. 이를 통해 모델이 특정 작업에 필요한 데이터를 실시간으로 호출하여 사용할 수 있습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/db0a43a9-c24d-48bb-b9ba-7c111c833059/image.png)

* **예시 코드**:

```
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "What is the weather like in New York?"},
    ],
    functions=[
        {
            "name": "get_current_weather",
            "description": "Gets the current weather in a given city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "The name of the city"},
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
                }
            }
        }
    ]
)

print(response.choices[0].message['content'])
```

* **추가 예시**:  
  
  아래 코드는 DuckDuckGo 검색과 OpenAI의 함수 호출(Function Calling) 기능을 결합하여 사용자 질문에 답변하는 과정을 보여줍니다.
  + 여기서 functions 파라미터를 통해 duck\_search 함수를 정의하고, messages에 시스템 지시와 사용자 질문을 포함시킵니다.

```
import openai
import json
from duckpy import Client
import ast

#  DuckDuckGo 클라이언트를 초기화
duckduckgo_client = Client()

# DuckDuckGo에서 검색을 수행하는 함수를 정의
def duck_search(query) -> str:
    output = duckduckgo_client.search(query)
    return str(output)

# OpenAI API를 호출하여 초기 응답
completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0613",
        temperature=0,
        functions=[
            {
                "name": "duck_search",
                "description": "Used to search online",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Translate the Korean content into English input query",
                        },
                    },
                    "required": ["query"],
                },
            }
        ],
        messages=[
            {"role": "system", 
            "content": "You must use the `duck_search` function to get information."},
            {"role": "user", 
            "content": "조지 클루니 생일이 언제야?"},
        ]
    )

print(completion)
```
### 4.4 구조화된 출력 (Structured Outputs)

OpenAI 모델은 JSON과 같은 구조화된 데이터를 출력할 수 있습니다. 이를 통해 특정 형식으로 데이터를 받을 수 있어, 프로그램에서 데이터를 더 쉽게 처리할 수 있습니다.

* **예시 코드**:

```
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Give me a recipe for chocolate cake."}],
    functions=[{
        "name": "generate_recipe",
        "description": "Generates a

 recipe",
        "parameters": {"type": "object", "properties": {"ingredients": {"type": "array"}}}
    }]
)

print(response.choices[0].message['content'])
```
### 4.5 복잡한 추론 (Reasoning)

OpenAI 모델은 복잡한 문제에 대해 논리적으로 추론할 수 있습니다. 수학 문제 해결, 코드 디버깅 등 다양한 추론 작업을 수행할 수 있습니다.

* **예시 코드**:

```
response = openai.Completion.create(
    model="gpt-4",
    prompt="Solve the equation: 5x - 3 = 12",
    max_tokens=50
)

print(response.choices[0].text.strip())
```
### 4.6 고급 사용법 (Advanced Usage)

OpenAI API는 토큰 제한 설정, 스트리밍 응답, 모델의 온도 조절과 같은 고급 기능을 제공합니다. 이를 통해 사용자는 모델의 응답 스타일을 세밀하게 조정할 수 있습니다.

* **예시 코드** (스트리밍 응답):

```
response = openai.Completion.create(
    model="gpt-4",
    prompt="Tell me a long story about a hero's journey.",
    stream=True
)

for chunk in response:
    print(chunk.choices[0].delta.get("content", ""), end="")
```

---

5. 파인튜닝된 모델 사용 방법
-----------------

OpenAI API는 사전 학습된 모델뿐만 아니라, **파인튜닝**을 통해 특정 작업에 맞게 모델을 조정하여 사용할 수도 있습니다. 파인튜닝된 모델은 특정 도메인 또는 작업에 대해 성능을 개선하기 위해 미세 조정된 모델입니다.

### 5.1 파인튜닝 모델 호출

파인튜닝이 완료되면 해당 모델에는 고유한 ID가 부여되며, `model` 파라미터로 이 ID를 사용하여 API에서 호출할 수 있습니다.

* **예시 코드**:

```
response = openai.Completion.create(
    model="fine-tuned-model-id",  # 파인튜닝된 모델 ID
    prompt="Summarize the article about climate change.",
    max_tokens=100
)

print(response.choices[0].text.strip())
```

---

6. 결론
-----

OpenAI API는 다양한 AI 기능을 제공하며, 텍스트 생성, 이미지 처리, 함수 호출, 구조화된 출력, 복잡한 추론 등 다양한 작업을 쉽게 수행할 수 있습니다. 또한, 사전 학습된 모델을 사용할 수 있을 뿐만 아니라, 특정 용도에 맞게 **파인튜닝된 모델**을 통해 더 나은 성능을 제공받을 수 있습니다.

**실습**

1. **API 키 발급**: OpenAI 계정에 가입하고 API 키를 발급받으세요.
2. **엔드포인트 실험**: 제공된 코드를 바탕으로 OpenAI API의 다양한 엔드포인트를 실험해 보세요.
3. **파인튜닝 모델 구축**: 자신의 데이터에 맞춰 모델을 파인튜닝하고, 고유한 AI 솔루션을 개발해 보세요.

이번 포스팅에서는 OpenAI API의 기본 사용법과 각 엔드포인트, 주요 기능에 대한 전반적인 가이드를 제공합니다. 이를 바탕으로 AI 솔루션을 더욱 효과적으로 구축할 수 있을 것입니다.

계속해서 Documents 보면서 추가되는 내용이 있으면 추가해보겠습니다 :)

