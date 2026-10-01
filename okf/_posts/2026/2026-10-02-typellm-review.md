---
type: "Repo Review"
title: "[Repo Review] TypeLLM: 타입별 디코딩과 의존성 그래프로 구성하는 LLM 출력"
description: "TypeLLM의 스키마 컴파일부터 후보 토큰 채점, 문법 기반 생성, 의존성·조건부 실행과 결과 조립까지 고정 커밋의 코드를 따라 분석합니다."
date: "2026-10-02"
tags:
  - "Repo Review"
  - "Python"
  - "NLP"
  - "딥러닝"
resource: "https://github.com/TypeLLM/TypeLLM/tree/6c61747477061559e7bf553453d378d37fb2885d"
generated:
  by: "process:blog-review"
  at: "2026-10-02T06:08:20+09:00"
sources:
  - id: "TypeLLM/TypeLLM"
    resource: "https://github.com/TypeLLM/TypeLLM/tree/6c61747477061559e7bf553453d378d37fb2885d"
    title: "TypeLLM: LLMs with type-safe generation"
status: "stable"
year: "2026"
analyzed_at: "2026-10-02T06:08:20+09:00"
source_id: "TypeLLM/TypeLLM"
source_revision: "6c61747477061559e7bf553453d378d37fb2885d"
source_title: "TypeLLM: LLMs with type-safe generation"
source_type: "repo"
source_url: "https://github.com/TypeLLM/TypeLLM/tree/6c61747477061559e7bf553453d378d37fb2885d"
visual_sources:
  - path: "/img/reviews/2026/typellm-review/flow.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/runtime.py#L412-L518"
    caption: "리뷰어 작성, 분석 커밋 기준. 로컬 SGLang 경로의 스키마 컴파일·계층 실행·출력 조립."
---

## 들어가며

LLM으로 영수증을 읽을 때 판매처는 문자열, 합계는 숫자, 비용 종류는 정해진 후보 중 하나여야 합니다. 여기에는 서로 다른 문제가 섞여 있습니다. 출력이 프로그램에서 읽을 수 있는 형태인지, 값이 허용된 후보에 속하는지, 그 값이 실제 영수증의 내용과 맞는지는 각각 다른 질문입니다.

TypeLLM은 기존 자기회귀 언어 모델의 가중치를 바꾸지 않고, 필드의 타입에 맞춰 답을 얻는 Python 클라이언트입니다. 열거형은 후보 라벨의 점수를 비교하고, 숫자와 문자열은 문법 제약을 사용하며, 앞선 답이 필요한 질문은 의존성 그래프로 실행합니다. README는 이를 타입 안전 생성으로 소개합니다. 이 리뷰에서는 그 표현을 **지원하는 스키마 부분집합의 출력 형식을 제한하는 구조**로 해석합니다. 사실 판단의 정확성까지 보장한다는 뜻으로 읽지 않습니다. [README 소개](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/README.md#L28-L46), [스키마 컴파일러](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/schema.py#L92-L245)

분석 대상은 `TypeLLM/TypeLLM`의 커밋 `6c61747477061559e7bf553453d378d37fb2885d`입니다. 의존성을 설치하거나 대상 코드를 빌드·실행·테스트하지 않고 문서와 구현을 정적으로 대조했습니다. 아래 벤치마크 수치는 저장소 저자가 공개한 결과이며 이 리뷰의 재측정값이 아닙니다.

## 무엇을 제공하는가

사용자는 `context`에 공통 문맥을, `questions`에 필드별 타입과 지시문을 전달합니다. 반환 객체 `Generation`은 답인 `result`, 추론 텍스트인 `thinking`, 사용량 `usage`, 자동 선택한 추론 수준 `thinking_effort`, 실행하지 않은 필드 이름 `skipped`를 분리합니다. 이 구분은 조건부 질문에서 특히 중요합니다. 조건을 만족하지 않아 생략한 답과, 모델이 값의 부재를 뜻하는 `null`을 선택한 답은 서로 다릅니다. [반환 자료구조](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/runtime.py#L144-L155), [결과 조립](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/runtime.py#L489-L518)

| 필드 | 로컬 구현에서 답을 얻는 방법 | 지원 경계 |
|---|---|---|
| `enum`, `boolean` | 단일 토큰 제어 라벨의 로그 확률을 후보 안에서 정규화하고 실제 값으로 복원합니다. | 후보는 최대 24개입니다. |
| `integer`, `number` | 정규식 문법을 SGLang에 전달하고 결과를 숫자로 파싱합니다. | 기본 최대 32자리, 지수 표기와 숫자 범위 제약은 지원하지 않습니다. |
| 자유 `string` | JSON 문자열 문법으로 생성하고 문자열을 복원합니다. | 기본 128토큰이며 문자 수 제한인 `maxLength`와 다릅니다. |
| nullable 타입 | 허용된 타입에 `null`을 추가합니다. | enum은 후보 목록에도 `None`이 있어야 합니다. |

근거: [타입 검증](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/schema.py#L126-L245), [기본 설정](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/runtime.py#L163-L177), [숫자 문법](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/runtime.py#L699-L718), [문자열 문법](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/sglang.py#L894-L944).

## 아키텍처와 진입점

배포 매니페스트의 버전은 `0.5.0`, Python 요구 버전은 `>=3.10`이며 직접 의존성은 `httpx`, `jinja2`, `transformers`입니다. SGLang 서버를 이 패키지 안에서 시작하는 구조는 아닙니다. SDK와 별도로 준비된 서버에 HTTP 요청을 보냅니다. 패키지 명령 `typellm`은 `typellm.cli:main`을 가리키고, `python -m typellm`도 같은 함수로 연결됩니다. CLI는 내장 영수증 예제를 실행해 JSON을 출력하는 데모입니다. [매니페스트](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/pyproject.toml#L1-L27), [모듈 진입점](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/__main__.py#L1-L4), [CLI](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/cli.py#L39-L98)

| 모듈 | 책임 |
|---|---|
| `schema.py` | 필드 정의를 토크나이저 독립적인 `Decision`으로 만들고 의존성과 조건을 검증합니다. |
| `runtime.py` | 라벨을 토큰에 연결한 `Choice`를 구성하고 계층 실행, 확률 평균, 결과 조립을 담당합니다. |
| `sglang.py` | 채팅 템플릿, HTTP 요청, 문법 생성, 로그 확률 추출, 추론 예산을 처리합니다. |
| `protocol.py` | 템플릿의 제어 토큰에 따라 추론 구간과 턴 종료 방식을 구분합니다. |
| `images.py` | 이미지 입력을 URL 또는 data URI로 정규화합니다. |

근거: [Decision](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/schema.py#L19-L42), [Choice](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/runtime.py#L56-L74), [서버 호출](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/sglang.py#L373-L389), [프로토콜](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/protocol.py#L8-L39), [이미지 변환](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/images.py#L43-L75).

![TypeLLM 로컬 실행의 입력, 스키마 컴파일, 계층별 생성, 결과 조립 흐름]({{ '/img/reviews/2026/typellm-review/flow.svg' | relative_url }})

그림 1. 리뷰어 작성, 분석 커밋 기준. 실선은 로컬 SGLang 경로의 처리 순서입니다. 서버의 모델 추론은 저장소 밖 경계이며, hosted API 경로는 이 도식과 별도로 아래에서 설명합니다. [generate 진입점](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/runtime.py#L440-L518), [필드 생성 및 후보 채점](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/runtime.py#L985-L1069)

## 작동 원리: 입력에서 결과까지

### 1. 요청을 정규화하고 실행 경로를 선택합니다

`generate()`는 `context`와 기존 이름인 `state` 중 정확히 하나를 요구합니다. `schema`와 `questions`도 동시에 받을 수 없습니다. `questions`를 받으면 내부적으로 최상위 객체의 `properties`로 감쌉니다. 따라서 간단한 질문 사전이 컴파일러가 읽는 스키마 구조로 변환됩니다. 이미지가 있으면 이 단계에서 먼저 정규화합니다. [입력 처리](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/runtime.py#L440-L451)

API 키가 있으면 hosted 경로를 사용합니다. 키와 URL을 둘 다 생략한 경우에는 `TYPELLM_API_KEY` 환경 변수도 확인하지만, `base_url`만 명시하면 자체 서버 경로를 선택합니다. hosted 경로는 `context`, `questions`, `images`, 옵션을 `/v1/generate`로 전달하고 응답 JSON을 `Generation`으로 감쌉니다. 이때 로컬 `compile_schema()`와 아래의 계층 실행기는 호출하지 않습니다. 서버 내부의 동일성은 이 클라이언트 코드만으로 확인할 수 없습니다. [생성자 분기](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/runtime.py#L202-L236), [hosted 요청과 응답](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/runtime.py#L459-L464), [HTTP 경계](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/runtime.py#L520-L598)

### 2. JSON Schema의 일부를 실행 가능한 질문으로 바꿉니다

`compile_json_schema()`는 최상위 `object`와 비어 있지 않은 `properties`를 요구합니다. 각 필드의 질문은 `instructions`, `description`, 이름 기반 기본 지시문의 순서로 정해집니다. enum의 값과 선언 타입이 맞는지, 후보가 중복되는지, `required`에 존재하지 않는 이름이 들어 있는지를 확인합니다. 다만 이 코드는 범용 JSON Schema 검증기가 아닙니다. `minimum`·`maximum`이나 자유 문자열의 `pattern`·`format`을 명시적으로 거부하고, 배열이나 중첩 객체 필드도 지원 타입에 들어 있지 않습니다. [컴파일러](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/schema.py#L92-L245)

컴파일 결과인 `Decision`에는 질문뿐 아니라 숫자/문자열 여부, nullable 여부, 의존성, 조건, 추론 설정이 함께 보관됩니다. 그다음 `TypeLLMClient.compile_schema()`는 유한 후보가 있는 필드들의 최대 후보 수만큼 제어 라벨을 준비합니다. 기본 풀은 영문 대문자와 숫자이며, 실제 서버의 토크나이저로 하나의 토큰이 되는 라벨만 채택합니다. 토큰 ID가 중복되거나 다시 디코딩한 문자열이 라벨과 다르면 사용할 수 없습니다. 이 검사는 임의의 후보 문자열 자체가 한 토큰이라는 가정을 피합니다. [라벨 풀](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/runtime.py#L158-L161), [라벨 바인딩](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/runtime.py#L280-L333), [왕복 검증](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/sglang.py#L753-L782)

### 3. 열거형은 생성된 단어 대신 후보 토큰 점수로 답합니다

예를 들어 README의 `expense_type` 후보는 `meal`, `travel`, `equipment`입니다. 구현은 후보 값을 라벨에 연결한 사전을 프롬프트에 싣고, 답변 시작 부분을 `{"expense_type": "`처럼 미리 채웁니다. 모델은 이 자리에서 라벨을 판단합니다. 중요한 부분은 서버가 자유롭게 생성한 토큰을 그대로 답으로 삼지 않는다는 점입니다. 요청한 후보 토큰들의 로그 확률만 추출한 뒤, 클라이언트가 선택을 수행합니다. [README 질문](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/README.md#L125-L128), [프롬프트 구성](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/runtime.py#L105-L140), [후보 채점](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/sglang.py#L784-L863)

다음은 후보 배치 요청의 실제 일부입니다. 출처: [`score_candidates_batch()`](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/sglang.py#L835-L841).

```python
payload = {
    "text": list(prefixes),
    "sampling_params": {"max_new_tokens": 1, "temperature": 0},
    "return_logprob": True,
    "token_ids_logprob": [list(ids) for ids in candidate_ids],
    "return_text_in_logprobs": True,
}
```

`candidate_softmax()`는 로그 확률을 온도로 나눈 뒤 최댓값을 빼고 지수화해 합이 1인 분포를 만듭니다. 기본 설정에서는 가장 큰 확률의 라벨을 고르고, 양의 temperature에서는 이 분포에서 샘플링합니다. 최종 반환값은 라벨이 아니라 `decision.choices[selected]`입니다. 따라서 선택 결과는 주어진 후보 값 안에 있습니다. 그러나 이 분포는 **허용 후보 안에서 다시 정규화한 분포**입니다. 전체 어휘의 확률 질량이나 별도로 보정된 사실 신뢰도와 동일하게 해석할 수 없습니다. [softmax](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/runtime.py#L620-L641), [선택과 역매핑](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/runtime.py#L1050-L1069)

`return_probabilities`를 켜면 해당 필드만 `value`와 `probabilities`를 담은 객체로 바뀝니다. 자유 숫자와 자유 문자열에는 이 옵션이 지원되지 않습니다. [옵션 검증](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/schema.py#L161-L165), [출력 포장](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/runtime.py#L498-L514)

### 4. 후보 순서를 바꾼 결과는 원래 값에 맞춰 평균냅니다

선택지의 위치가 결과에 영향을 줄 수 있으므로 `permutations`는 같은 후보를 여러 라벨 배치로 평가합니다. `auto`는 JSON 표현으로 정렬한 기준 순서를 만든 다음 균형 잡힌 순서 집합을 구성합니다. 일반적으로 짝수 개 후보는 후보 수만큼, 홀수 개 후보는 그 두 배의 순서를 사용합니다. 한 후보뿐인 경우에는 중복 제거로 한 순서만 남습니다. `all`은 모든 순서, 양의 정수는 그 수만큼의 서로 다른 순서를 선택하며 명시적 순서 예산은 최대 720입니다. [순서 생성](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/runtime.py#L739-L795), [예산 검증](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/schema.py#L150-L160)

평균은 라벨 A의 점수를 무조건 더하는 방식이 아닙니다. 각 순서에서 softmax를 계산한 뒤 그 라벨에 배치된 **원래 후보 값**의 위치로 정렬해 산술 평균합니다. 그래서 서로 다른 순서에서도 같은 값의 점수가 합쳐집니다. 정수 예산의 샘플링은 전체 순열을 미리 메모리에 만들지 않고 순열의 순위를 추출해 복원합니다. 이 기능은 후보 순서 영향을 줄이려는 설계이지만, 채점할 프롬프트 수와 추론 작업량이 순서 수에 따라 증가합니다. 여러 순서는 하나의 SGLang 배치 요청으로 묶습니다. 항상 정확도가 오른다는 증거로 해석할 수는 없습니다. [순위 샘플링과 확률 정렬](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/runtime.py#L775-L806), [배치 확대](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/runtime.py#L967-L976)

### 5. 숫자와 문자열은 문법으로 생성하고 파싱합니다

자유 숫자는 후보 목록으로 표현할 수 없으므로 `numeric_pattern()`이 허용할 문자열의 정규식을 만듭니다. 부호, 선행 0 규칙, 소수점, 총 자릿수를 제한하고 지수 표기는 제외합니다. 서버에는 `regex`와 최대 출력 토큰 수를 전달합니다. 반환 후에는 정상 종료 여부를 확인하고, 숫자 문법을 다시 검사한 뒤 `int`나 `float`로 변환합니다. 비유한 실수도 거부합니다. 이 과정에서 숫자의 형태는 제한하지만 계산의 정답이나 업무상 허용 범위를 보장하지는 않습니다. [숫자 생성·파싱](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/runtime.py#L670-L735), [서버 숫자 옵션](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/sglang.py#L874-L892)

문자열은 JSON 문자열의 따옴표와 escape를 허용하는 문법으로 생성합니다. 필드 키 뒤에서 토큰 한도로 잘렸다면 `_partial_json_string()`으로 얻을 수 있는 문자열 부분을 복원합니다. 따라서 기본 128토큰에 닿았을 때 반환 타입이 `str`이라고 해서 문장이나 추출 내용까지 완결됐다고 볼 수 없습니다. 숫자는 정상 `stop` 종료를 요구하지만 문자열에는 이 잘림 복구 경로가 있다는 차이가 있습니다. [문자열 후처리](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/sglang.py#L914-L944)

같은 계층의 숫자와 문자열은 `generate_fields()` 한 요청에 함께 들어갑니다. 반면 enum의 후보 채점은 그 뒤 별도의 요청입니다. README의 “독립 필드가 함께 실행된다”는 설명은 모든 타입이 단일 HTTP 요청에서 완전히 동시에 처리된다는 뜻으로 확대하면 안 됩니다. [실제 호출 순서](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/runtime.py#L1004-L1038), [숫자·문자열 배치](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/sglang.py#L997-L1026)

### 6. 의존성 그래프와 조건은 실행할 질문을 결정합니다

`depends_on`이 없으면 필드별 질문은 원래 문맥을 공유하되 다른 필드의 답을 보지 않습니다. 의존성을 지정하면 `dependency_layers()`가 이미 완료된 의존성을 가진 노드를 한 계층으로 묶습니다. 더 이상 실행 가능한 노드가 남지 않으면 순환으로 판단해 `SchemaError`를 냅니다. 알려지지 않은 이름과 자기 자신에 대한 의존성도 검사합니다. [계층 구성](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/schema.py#L397-L416)

실행기는 각 필드의 직접·간접 조상 결과를 모아 `Dependency results (JSON)`이라는 문맥으로 전달합니다. 여러 부모가 있으면 직렬화된 프롬프트 길이가 가장 긴 부모 하나를 골라 이어 쓰고, 다른 부모들의 값도 의존성 결과 JSON에 포함합니다. 이는 여러 분기의 KV 캐시 텐서를 이어 붙이는 방식이 아닙니다. **하나의 문자열 prefix를 재사용하고 필요한 결과를 텍스트로 보충하는 구조**입니다. [부모 선택](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/runtime.py#L809-L863), [의존성 문맥 삽입](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/runtime.py#L878-L883)

`when`은 `depends_on`에 적힌 필드만 참조할 수 있습니다. 포함·제외·불일치와 숫자의 대소 비교를 검증하며, 여러 조건은 모두 참이어야 합니다. 부모가 생략되었거나 조건을 만족하지 않으면 해당 질문은 서버로 보내지 않고 결과 행을 `None`으로 둡니다. 이 생략은 자식에게 전파되며 최종 `result`에는 필드 자체가 없고 `skipped`에 이름이 남습니다. nullable이 허용된 필드에서 값으로 `None`을 반환하는 경우와는 다른 경로입니다. [조건 정의](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/schema.py#L309-L367), [생략 전파](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/runtime.py#L821-L828), [출력 처리](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/runtime.py#L489-L514)

### 7. 추론도 그래프의 일부이며 캐시는 서버가 관리합니다

`thinking: "auto"`는 실행 중 옵션 하나를 임의로 바꾸는 기능이 아닙니다. 컴파일러가 `<필드명>.thinking_effort`라는 숨은 질문을 삽입합니다. 이 질문은 `none`, `low`, `medium`, `high` 중 하나를 선택하고, 실제 질문은 그 결과에 의존합니다. 예산은 각각 추론 없음, 512, 2048, 4096토큰으로 연결됩니다. 숨은 질문은 원래 필드와 같은 조건을 가지며, 사용자에게 반환하는 일반 답이나 의존성 문맥에는 숨깁니다. [자동 추론 컴파일](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/schema.py#L247-L281), [예산표](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/schema.py#L45-L55), [런타임 반영](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/runtime.py#L833-L849)

실제 추론 생성은 답변 후보 채점이나 문법 생성보다 먼저 수행됩니다. SGLang 어댑터는 모델의 채팅 템플릿과 추론 종료 표식을 확인합니다. 컨텍스트 길이에서 입력, 답변 예약 공간, 종료 표식과 여유 공간을 빼서 쓸 수 있는 예산을 계산합니다. 길이 한도 또는 인식된 턴 종료로 추론이 끝나면 조건을 확인해 추론 구간을 닫고 최종 답 생성으로 넘어갑니다. 임의의 잘린 응답을 모두 복구하는 것은 아니며 오류·중단과 비정상 종료에는 예외가 있습니다. [추론 준비](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/sglang.py#L589-L614), [예산 및 종료 처리](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/sglang.py#L671-L750)

prefix cache는 앞서 처리한 토큰의 모델 내부 KV 상태를 재사용하는 서버 기능입니다. TypeLLM의 `cache_prefix()`는 `max_new_tokens: 0`인 요청으로 공통 prefix를 먼저 처리하게 합니다. DAG 경로에서는 계층의 서로 다른 부모 prefix마다 예열합니다. 독립 실행 경로의 명시적 공통 prefix 예열은 `finite_indexes`가 있을 때만 호출됩니다. 따라서 독립 숫자·문자열만 있는 요청까지 항상 별도 예열을 거친다는 설명은 이 커밋의 코드와 맞지 않습니다. 서버가 자체적으로 수행할 수 있는 캐시 동작과 클라이언트의 명시적 예열을 구분해야 합니다. [예열 API](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/sglang.py#L803-L823), [DAG 예열](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/runtime.py#L906-L913), [독립 경로 조건](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/runtime.py#L985-L991)

### 8. 이미지와 사용량은 외부 경계를 드러냅니다

로컬 이미지 경로는 클라이언트에서 읽어 data URI로 바꾸므로 서버가 같은 파일 시스템을 볼 필요가 없습니다. HTTP URL과 data URI는 그대로 전달합니다. SGLang 어댑터는 프롬프트의 이미지 placeholder 개수와 전달한 이미지 수를 대조하고 `image_data`를 붙입니다. 이 기능을 사용하려면 서버 모델과 템플릿도 이미지를 처리할 수 있어야 합니다. [이미지 입력](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/images.py#L43-L75), [요청 결합](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/sglang.py#L408-L431)

사용량의 `input_tokens`는 원래 문맥과 질문 등을 한 번 세는 값이고, SGLang 요청마다 반복되는 `prompt_tokens`와는 구분됩니다. 로컬 실행 예외에는 그때까지의 `usage`를 붙입니다. hosted 응답은 입력·추론 토큰만으로 `Usage`를 구성하므로, 로컬과 서버의 상세 계수까지 같다고 가정할 수 없습니다. [로컬 계수와 예외](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/runtime.py#L467-L488), [hosted 반환](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/runtime.py#L553-L576), [README 계수 설명](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/README.md#L508-L513)

## 설치와 사용 문서 읽기

분석 커밋의 README는 다음 설치 명령을 제시합니다. 이는 문서 인용이며 이 리뷰에서 실행한 명령이 아닙니다. 또한 `-U`는 설치 시점의 배포본을 받으므로 분석한 Git 커밋을 재현하는 버전 고정 명령은 아닙니다. [설치 안내](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/README.md#L56-L63)

```bash
pip install -U typellm
```

자체 서버에 연결하는 README 예제는 다음과 같습니다. 실제 사용 전에는 별도로 호환되는 모델을 SGLang에 올리고 prefix caching을 준비해야 합니다. 이 글은 해당 배포의 성공 여부를 확인하지 않았습니다. 출처: [자체 서버 연결 예제](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/README.md#L84-L103).

```python
from typellm import TypeLLMClient

client = TypeLLMClient(
    "http://127.0.0.1:30000",
    model="Qwen/Qwen3.8-27B",
)
```

이후 `client.generate(context=..., questions=...)`에 README의 영수증 질문 정의를 전달하고 `response.result`를 읽는 흐름입니다. hosted API는 API 키로 같은 질문 형태를 전달하지만 `schema`, 로컬 취소 이벤트, 최종 프롬프트 출력과 일부 토크나이저·출력 길이 옵션은 자체 서버 전용입니다. README의 “두 클라이언트가 같은 요청을 받는다”는 설명은 공통 `questions` 사용법 수준에서는 맞지만 모든 옵션이 동일하다는 뜻은 아닙니다. [공통 사용법](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/README.md#L105-L147), [로컬 전용 옵션](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/runtime.py#L224-L231), [hosted 제한](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/runtime.py#L459-L464)

## 공개 평가를 어떻게 읽을 것인가

README는 JevBench 공개 231문항에서 추론 없이 195개, 추론을 켜고 228개를 맞혔다고 보고합니다. 평가 문서는 모델을 `RadixArk/Qwen3.8-27B-NVFP4-BF16-LMHead`, 런타임을 SGLang 0.5.19, GPU를 RTX PRO 6000 Blackwell Server Edition으로 명시합니다. 두 설정 모두 argmax 결정과 순열 평균 없는 조건이며, 추론 설정에는 별도의 토큰 예산이 없습니다. [보고 점수](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/README.md#L21-L23), [평가 방법](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/evals/jevbench/METHOD.md#L1-L40)

| 저자 보고 지표 | 추론 없음 | 추론 사용 |
|---|---:|---:|
| 정답 수 / 공개 문항 수 | 195 / 231 | 228 / 231 |
| 요청 시간 P50 | 1.296초 | 6.677초 |
| 요청 시간 P95 | 2.150초 | 61.083초 |
| 채점 응답의 추론 토큰 | 0 | 212,255 |
| 채점 응답의 답변 토큰 | 231 | 231 |

시간·토큰 출처: [평가 결과표](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/evals/jevbench/README.md#L41-L60).

이 수치는 타입 제한이 곧 정답 보장이 아니라는 점도 보여줍니다. 형식이 유효해도 오답은 남습니다. 전체 534문항 평가나 공식 순위가 아니며 설정별 한 번의 실행입니다. 시간에는 클라이언트와 SSH/IAP 터널 왕복이 들어가고, 추론 실행이 기존 서버와 캐시를 재사용했으므로 동일한 cold-cache 조건의 비교도 아닙니다. 또한 저장소는 원시 전송 자료와 추론 trace 전체를 공개하지 않아, 공개된 해시만으로 원시 자료 감사까지 재현할 수 없다고 설명합니다. 이 평가를 현재 커밋의 모든 신기능이나 일반적인 처리량을 입증하는 결과로 확장하지 않습니다. [범위·단일 실행·시간·공개 자료 한계](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/evals/jevbench/METHOD.md#L12-L97)

## 한계와 주의점

이 구현의 타입 안전성은 지원 타입, 서버 문법 처리, 응답 파싱이 맞물릴 때의 속성입니다. 숫자 범위, 문자열 정규식, 임의의 중첩 스키마를 모두 만족시키는 일반 스키마 엔진으로 사용하면 안 됩니다. `required` 목록도 이름의 유효성을 검사할 뿐, 실행기를 선택적 필드 생성기로 바꾸지는 않습니다. 실제로 컴파일러는 `properties` 전체를 질문으로 만듭니다. [컴파일 범위](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/schema.py#L92-L245)

호환성은 모델 이름만으로 결정되지 않습니다. 토크나이저의 chat template, 단일 토큰 라벨, SGLang 응답 형식이 모두 필요합니다. 토크나이저는 `trust_remote_code=False`로 로드하며, 프로토콜 판별기는 특정 Gemma 4 제어 토큰 조합을 명시적으로 거부합니다. README가 다른 Qwen 크기에 대해 제시하는 호환 예상은 실제 검증 목록과 구별해야 합니다. [토크나이저 로딩](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/sglang.py#L467-L533), [프로토콜 제한](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/protocol.py#L26-L39), [README 지원 범위](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/README.md#L531-L548)

속도 역시 한 문장으로 일반화하기 어렵습니다. 후보 선택은 한 토큰의 점수로 결정하지만, 토큰화 확인, prefix 예열, 추론, 숫자·문자열 생성, 순열별 채점이 추가될 수 있습니다. README의 “출력 토큰 비용이 작다”는 설명은 전체 지연 시간이나 GPU 비용이 무시 가능하다는 측정이 아닙니다. 라이브러리는 KV 텐서를 직접 이동하지 않으므로 캐시 효과도 서버 설정과 실제 요청에 의존합니다. [기능 설명](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/README.md#L37-L46), [실행 순서](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/typellm/runtime.py#L985-L1038)

저장소에는 Apache License 2.0 전문이 있고 패키지 매니페스트도 `Apache-2.0`을 표시합니다. 여기서 확인한 것은 클라이언트 저장소의 라이선스이며, 별도로 사용하는 모델 가중치와 hosted 서비스의 조건까지 이 라이선스로 대체되는 것은 아닙니다. [LICENSE](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/LICENSE#L1-L202), [패키지 선언](https://github.com/TypeLLM/TypeLLM/blob/6c61747477061559e7bf553453d378d37fb2885d/pyproject.toml#L5-L17)

## 결론

TypeLLM의 핵심은 필드마다 답을 얻는 방식을 분리한 뒤, 이를 하나의 질문 실행기로 묶은 데 있습니다. enum은 라벨 점수에서 허용 값을 고르고, 숫자와 문자열은 문법 생성과 파싱을 거칩니다. 의존성과 조건은 실행할 필드와 전달할 문맥을 결정하며, 자동 추론은 숨은 질문을 추가해 같은 그래프 구조를 활용합니다. 이 설계를 이해하면 출력 형식의 보장, 내용의 정확성, 후보 분포의 의미, 서버 캐시의 역할을 각각 나누어 판단할 수 있습니다.

### 이 글에서 다루지 못한 부분

`benchmark.py`의 캐시 성능 측정 절차, 테스트 전체의 assertion과 동시성 검증, `evals/`에 있는 모델별·이미지·조건부 필드·추론 수준별 GPU 실험 전체는 상세 감사하지 않았습니다. hosted 서버 구현과 SGLang 내부 grammar backend·KV 캐시 구현은 이 저장소의 분석 범위 밖입니다. 실제 모델 실행, 설치 호환성, 재시도 중 과금·서버 실행의 의미, 운영 안정성도 검증하지 않았습니다.
