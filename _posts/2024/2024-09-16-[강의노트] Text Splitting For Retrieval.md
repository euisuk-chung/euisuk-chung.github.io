---
title: "[강의노트] Text Splitting For Retrieval"
date: "2024-09-16"
tags:
  - "rag"
  - "강의노트"
year: "2024"
---

# [강의노트] Text Splitting For Retrieval

![](https://velog.velcdn.com/images/euisuk-chung/post/cef4d420-1a78-40ab-a375-adbe72c50e60/image.png)

Introduction
------------

대규모 언어 모델(LLM, Large Language Model)을 이용한 애플리케이션의 성능을 향상시키는 가장 효과적인 전략 중 하나는 큰 텍스트 데이터를 더 작은 조각으로 분할하는 것입니다. LLM에게 필요한 정보만을 제공함으로써 모델의 작업 효율성을 극대화할 수 있습니다. 이러한 텍스트 분할 기술은 단순한 방법 같지만, 그 안에는 복잡한 과학과 예술이 숨어 있습니다.

* `영상 제목` : The 5 Levels Of Text Splitting For Retrieval
* `영상 링크` : <https://youtu.be/8OJC21T2SL4>

이번 포스트에서는 **5가지의 텍스트 분할(Levels of Text Splitting)** 방법을 소개합니다.  
(\*해당 글은 위 Youtube 영상 자료를 공부 후에 정리하였습니다.)

Background
----------

언어 모델은 일반적으로 **문맥 길이(Context Length)**라는 제한이 있습니다. 즉, 한 번에 처리할 수 있는 데이터의 양이 제한되어 있습니다. 따라서 대량의 데이터를 한꺼번에 모델에 넘기기보다는, 데이터를 작은 조각으로 나눠서 필요한 부분만 제공하는 것이 더 효율적입니다. 이때 중요한 것이 바로 **텍스트 분할**입니다.

텍스트 분할은 단순히 데이터를 자르는 것이 아니라, **최적의 정보 구조를 만들기 위한 전략**입니다. 이를 통해 신호 대 잡음비(Signal-to-Noise Ratio)를 높여 모델이 보다 중요한 정보에 집중하게 만들 수 있습니다.

The 5 Levels of Text Splitting
------------------------------

텍스트 분할은 크게 **다섯 단계**로 나눌 수 있습니다. 각 단계는 점점 더 복잡한 방식으로 발전하며, 텍스트의 물리적 구조에서부터 의미적 구조까지 다양한 관점을 고려합니다.

① `Level 1`: **Character Splitting** - Simple static character chunks of data

② `Level 2`: **Recursive Character Text Splitting** - Recursive chunking based on a list of separators

③ `Level 3`: **Document Specific Splitting** - Various chunking methods for different document types (PDF, Python, Markdown)

④ `Level 4`: **Semantic Splitting** - Embedding walk based chunking

⑤ `Level 5`: **Agentic Splitting** - Experimental method of splitting text with an agent-like system.

---

**Level 1: Character Splitting (캐릭터 분할)**
-----------------------------------------

첫 번째 단계는 가장 기본적인 방식인 **텍스트를 고정된 문자 수로 분할하는 방식**은 기본적인 텍스트 분할 방법입니다. 이 방법은 구현이 간단하지만, 텍스트의 문맥이나 의미를 고려하지 않기 때문에 실무에서 자주 사용되지는 않습니다.

고정된 문자 수로 분할할 경우, 단어 중간에서 분할이 발생할 수 있으며, 이는 가독성에 문제를 일으킬 수 있습니다. 이런 이유로 이 방식은 실제 응용에서 거의 사용되지 않으며, 대신 더 정교한 분할 기법이 선호됩니다.

```
text = "This is the text I would like to chunk up. It is the example text for this exercise"
chunks = []
chunk_size = 35

for i in range(0, len(text), chunk_size):
    chunk = text[i:i + chunk_size]
    chunks.append(chunk)
```

**장점:**

* 매우 간단하고 빠릅니다.
* 구현이 쉽습니다.

**단점:**

* 텍스트의 의미나 구조를 고려하지 않기 때문에, 실전에서 거의 사용되지 않습니다.
* 단어 중간에서 분할이 발생하여 가독성에 문제가 생길 수 있습니다.

---

**Level 2: Recursive Character Splitting (재귀적 캐릭터 분할)**
-------------------------------------------------------

두 번째 단계는 **재귀적 캐릭터 분할**입니다. `RecursiveCharacterTextSplitter`와 같은 도구를 사용해 텍스트를 재귀적으로 분할합니다. 주어진 구분자(예: 문장, 단락, 공백 등)에 따라 텍스트를 나누며, 각 구분자가 작동하지 않는 경우 다음 구분자를 사용하여 텍스트를 더 세분화할 수 있습니다.

이 방법은 텍스트의 자연스러운 흐름을 고려해 적절한 구분자를 이용하는 것이 특징입니다. 먼저 큰 단위로 나눈 후, 필요에 따라 작은 단위로 재귀적으로 분할합니다. 이는 보다 의미 있는 청크를 생성하는 데 유리합니다.

```
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
texts = text_splitter.split_text(text)
```

**장점:**

* 텍스트의 구조를 고려하여 의미 있는 단위로 분할할 수 있습니다.
* 다양한 구분자를 사용하여 유연하게 텍스트를 분할할 수 있습니다.

**단점:**

* 여전히 고정된 문자 수에 의존하여 분할됩니다.
* 복잡한 문서에서는 추가적인 조정이 필요할 수 있습니다.

---

**Level 3: Document-Specific Splitting (문서 특화 분할)**
---------------------------------------------------

세 번째 단계는 문서의 종류에 따라 다르게 분할하는 **문서 특화 분할**입니다. 예를 들어, Markdown, Python 코드, PDF 문서 등 각각의 문서 형식에는 고유의 구조적 특징이 있습니다. Markdown 문서의 경우, 제목(Heading)을 기준으로, 코드 문서의 경우 함수나 클래스 단위로 분할할 수 있습니다.

PDF와 같은 복잡한 문서는 이미지, 표 등 여러 요소를 포함할 수 있으며, 이러한 요소들에 맞는 분할 방식이 필요합니다.

**python 분할 예시**:

```
# Python 코드 문서 분할 예제
from langchain.text_splitter import PythonCodeSplitter

code = """
class Example:
    def function(self):
        pass
"""
splitter = PythonCodeSplitter(chunk_size=200)
chunks = splitter.split_text(code)
```

**JS 분할 예시**:

```
from langchain.text_splitter import RecursiveCharacterTextSplitter, Language

javascript_text = """
// Function is called, the return value will end up in x
let x = myFunction(4, 3);

function myFunction(a, b) {
// Function returns the product of a and b
  return a * b;
}
"""

js_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.JS, chunk_size=65, chunk_overlap=0
)

js_splitter.create_documents([javascript_text])
```

**PDF 분할 예시**:

```
from PyPDF2 import PdfReader

reader = PdfReader('sample.pdf')
chunks = [page.extract_text() for page in reader.pages]
```

**Markdown 분할 예시**:

```
from langchain.text_splitter import MarkdownTextSplitter

text_splitter = MarkdownTextSplitter(chunk_size=200)
chunks = text_splitter.split_text(markdown_text)
```

**장점:**

* 문서의 형식(예: Markdown, Python 코드, PDF)을 고려한 맞춤형 분할이 가능합니다.
* 문서 구조에 따라 적절한 방식으로 분할하여 의미를 더 잘 보존합니다.

**단점:**

* 각 문서 형식에 맞춘 맞춤형 코드가 필요합니다.
* 여러 문서 형식을 동시에 처리하려면 추가적인 도구나 라이브러리가 필요할 수 있습니다.

---

**Level 4: Semantic Splitting (의미 기반 분할)**
------------------------------------------

네 번째 단계는 **의미적 분할**입니다. 앞서 언급한 단계들은 텍스트의 물리적 구조(문단, 문장, 단어)를 기반으로 분할했지만, 이 단계에서는 **텍스트의 의미와 내용**을 기준으로 분할합니다. 즉, 각 문장이 다루는 주제나 내용의 유사성을 바탕으로 텍스트를 분할하는 것입니다.

이 방법은 텍스트의 의미를 더 잘 반영할 수 있으나, 구현이 복잡하고 비용이 많이 듭니다. 이를 위해 텍스트의 **임베딩(embedding)**을 사용해 문장의 유사도를 계산하여 의미적으로 관련된 문장들을 하나의 청크로 묶습니다.

```
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_distances

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
sentences = ["This is a test.", "How does it work?", "Let's see!"]
embeddings = model.encode(sentences)

distances = cosine_distances(embeddings)
```

**장점:**

* 텍스트의 의미적 유사성을 고려하여 자연스럽고 의미 있는 분할이 가능합니다.
* 의미적으로 관련된 문장들을 하나의 청크로 묶어 정보 검색 및 분석에 유리합니다.

**단점:**

* 임베딩 및 유사도 계산을 사용하므로 계산 비용이 큽니다.
* 대량의 데이터나 복잡한 문서의 경우 처리 시간이 길어질 수 있습니다.

---

**Level 5: Agentic Splitting (에이전트 기반 분할)**
-------------------------------------------

마지막 단계는 **에이전트 기반 분할**입니다. Agentic Splitting은 텍스트를 능동적으로 평가하여 분할하는 실험적인 방법입니다. 각 문장을 하나의 "Proposition"으로 보고, 각 Proposition을 평가하여 기존 청크에 포함할지 새로운 청크로 나눌지 결정합니다. 문장이 추가될 때마다 청크의 요약과 제목이 자동으로 업데이트됩니다.

이 방식은 매우 느리고 비용이 많이 들지만, 복잡하고 다양한 문서에 대해 높은 수준의 분할을 가능하게 합니다.

```
class AgenticChunker:
    def __init__(self):
        self.chunks = []

    def add_proposition(self, proposition):
        # Proposition을 추가할 청크를 평가
        pass

    def create_new_chunk(self, proposition):
        # 새 청크 생성
        pass
```

**작동 방식**:

* Proposition(문장)이 주어지면, 기존 청크 중 어느 것에 포함될지 판단하거나, 새로운 청크를 생성합니다.
* 청크가 생성될 때마다 GPT-4와 같은 LLM을 사용하여 요약과 제목을 자동 생성하며, Proposition이 추가될 때마다 청크의 요약과 제목이 업데이트됩니다.

**장점:**

* 문장을 능동적으로 평가하여 분할하며, 청크의 요약 및 제목이 지속적으로 업데이트됩니다.
* 문서의 의미 변화에 유연하게 대응할 수 있습니다.

**단점:**

* LLM을 기반으로 하기 때문에 계산 비용이 크고 시간이 오래 걸립니다.
* 실험적인 기법으로, 아직 일반적인 프로덕션 환경에서는 사용되지 않습니다.

> **AgenticChunker에 대한 보충 설명**:  
> `AgenticChunker` 클래스는 문장을 논리적으로 분류하여 청크를 생성하고, 각 청크의 내용을 요약하고 제목을 생성하는 작업을 수행하는 시스템입니다. 이 시스템은 사용자가 문서를 세부적으로 분할하고 관리하는 데 적합하며, 특히 큰 문서나 여러 문장이 있는 데이터를 처리할 때 유용합니다.

> `AgenticChunker`는 다음과 같은 중요한 기능을 포함하고 있습니다:
>
> * 문장을 청크에 추가할지 새로운 청크를 생성할지 판단.
> * GPT-4를 통해 각 청크의 요약과 제목을 자동으로 생성 및 갱신.
> * Proposition이 추가될 때마다 의미를 평가하고 청크를 동적으로 관리.

---

Conclusion
----------

텍스트 분할은 언어 모델 애플리케이션의 성능을 극대화하기 위한 필수적인 과정입니다.

이번 포스트에서는 "The 5 Levels Of Text Splitting For Retrieval" 강의에서 소개하는 5단계의 텍스트 분할 방법들에 대해서 간단하게 소개합니다. 이러한 방법들은 각기 다른 방식으로 텍스트를 나누며, 문서의 특성, 의미, 그리고 작업의 목적에 맞는 분할 전략을 선택하는 것이 중요합니다.

기본적인 캐릭터 분할에서부터 의미적 분할, 그리고 에이전트 기반의 분할까지 다양한 옵션을 실험해보면서, 여러분의 애플리케이션에 맞는 최적의 방법을 찾을 수 있기를 바랍니다. 더 나아가, 텍스트 분할 외에도 **멀티벡터 인덱싱(Multi-Vector Indexing)**이나 **그래프 구조 추출**과 같은 고급 기법들을 활용하여 더욱 정교한 정보 검색 시스템을 구축할 수 있습니다.