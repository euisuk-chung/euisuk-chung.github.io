---
type: "Guide"
title: "[가이드] RAG 평가지표 입문: RAGAS·TruLens·DeepEval로 검색과 답변 나누어 보기"
description: "RAG의 검색과 답변을 분리해 평가하는 원리를 가상 사내 규정으로 배우고, RAGAS·TruLens RAG Triad·DeepEval의 지표와 실무 적용 순서를 비교합니다."
date: "2026-10-24"
tags:
  - "개념정리"
  - "RAG"
  - "NLP"
  - "딥러닝"
  - "머신러닝"
  - "Tools"
resource: "https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/"
generated:
  by: "process:blog-review"
  at: "2026-10-24T14:55:05+09:00"
sources:
  - id: "doc:fdaa8136b73f"
    resource: "https://arxiv.org/abs/2005.11401v4"
    title: "[2005.11401v4] Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"
  - id: "doc:d4378cda1b8c"
    resource: "https://deepeval.com/docs/evaluation-test-cases"
    title: "Single-Turn Test Case | DeepEval - The LLM Evaluation Framework"
  - id: "doc:b5f30347c4dd"
    resource: "https://deepeval.com/docs/evaluation-unit-testing-in-ci-cd"
    title: "Unit Testing in CI/CD | DeepEval - The LLM Evaluation Framework"
  - id: "doc:c7acb6a4ae7d"
    resource: "https://deepeval.com/docs/metrics-answer-relevancy"
    title: "Answer Relevancy | DeepEval - The LLM Evaluation Framework"
  - id: "doc:840ee9991299"
    resource: "https://deepeval.com/docs/metrics-contextual-precision"
    title: "Contextual Precision | DeepEval - The LLM Evaluation Framework"
  - id: "doc:ec29113330e8"
    resource: "https://deepeval.com/docs/metrics-contextual-recall"
    title: "Contextual Recall | DeepEval - The LLM Evaluation Framework"
  - id: "doc:6c98abd0f79b"
    resource: "https://deepeval.com/docs/metrics-faithfulness"
    title: "Faithfulness | DeepEval - The LLM Evaluation Framework"
  - id: "doc:aea51ed70d66"
    resource: "https://deepeval.com/guides/guides-rag-evaluation"
    title: "RAG Evaluation | DeepEval - The LLM Evaluation Framework"
  - id: "doc:26c4af3a9c9a"
    resource: "https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/"
    title: "List of available metrics - Ragas"
  - id: "doc:780060895b4a"
    resource: "https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/answer_relevance/"
    title: "Response Relevancy - Ragas"
  - id: "doc:b2cf4e0842f5"
    resource: "https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/context_precision/"
    title: "Context Precision - Ragas"
  - id: "doc:641023f8ae66"
    resource: "https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/context_recall/"
    title: "Context Recall - Ragas"
  - id: "doc:457690c71791"
    resource: "https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/faithfulness/"
    title: "Faithfulness - Ragas"
  - id: "doc:8defe90a0732"
    resource: "https://www.trulens.org/component_guides/evaluation/llm_judge_alignment/"
    title: "LLM Judge Alignment - 🦑 TruLens"
  - id: "doc:dc22433092b2"
    resource: "https://www.trulens.org/getting_started/core_concepts/rag_triad/"
    title: "⟁ RAG Triad - 🦑 TruLens"
  - id: "doc:e4811483b914"
    resource: "https://www.trulens.org/getting_started/quickstarts/quickstart/"
    title: "📓 TruLens Quickstart - 🦑 TruLens"
  - id: "doc:0491868a7d29"
    resource: "https://www.trulens.org/getting_started/quickstarts/groundtruth_evals_for_retrieval_systems/"
    title: "📓 Groundtruth Evaluations for Retrieval Systems - 🦑 TruLens"
status: "stable"
year: "2026"
analyzed_at: "2026-10-24T14:55:05+09:00"
visual_sources:
  - path: "/img/reviews/2026/rag-evaluation-guide/rag-evaluation-map.svg"
    kind: "reviewer-diagram"
    source_url: "https://www.trulens.org/getting_started/core_concepts/rag_triad/"
    caption: "작성 도식: RAG의 질문·검색 문맥·답변 관계와 평가 지점을 입문용으로 단순화"
  - path: "/img/reviews/2026/rag-evaluation-guide/claim-support-example.svg"
    kind: "reviewer-diagram"
    source_url: "https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/faithfulness/"
    caption: "작성 도식: 가상 규정의 세 주장 중 두 주장만 근거가 있는 수작업 계산 예, 실제 평가 결과 아님"
  - path: "/img/reviews/2026/rag-evaluation-guide/retrieval-order-example.svg"
    kind: "reviewer-diagram"
    source_url: "https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/context_precision/"
    caption: "작성 도식: 사람이 관련성을 고정한 가상 D1/D2/D3 순위 비교, 실제 평가 결과 아님"
---

<!-- paper-video:start -->
<div style="position: relative; width: 100%; padding-top: 56.25%; margin-bottom: 1rem;">
  <iframe src="https://www.youtube-nocookie.com/embed/Syv0M1xrfS4"
    title="개념 리뷰 영상" loading="lazy" referrerpolicy="strict-origin-when-cross-origin"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowfullscreen style="position: absolute; inset: 0; width: 100%; height: 100%; border: 0;"></iframe>
</div>
<p><a href="https://www.youtube.com/watch?v=Syv0M1xrfS4">YouTube에서 영상 보기</a></p>
<!-- paper-video:end -->

## RAG는 자료를 보고 답하는 AI입니다

사내 챗봇에 “연간 교육비 한도는 얼마이고, 신청 전에 누구의 승인을 받아야 하나요?”라고 물었다고 생각해 보겠습니다. 답변은 매끄럽습니다. 그런데 한도는 맞고 승인자는 틀렸다면, 이 챗봇을 잘 만들었다고 할 수 있을까요?

**RAG 평가는 답변이 그럴듯한지를 넘어, 필요한 자료를 찾았는지와 그 자료를 제대로 사용했는지를 나누어 확인하는 과정**입니다. 이 구분을 익히면 모델을 바꾸어야 할지, 검색기를 고쳐야 할지, 원본 문서를 정리해야 할지 판단하기 쉬워집니다.

RAG는 Retrieval-Augmented Generation, 우리말로 **검색 증강 생성**입니다. 사용자의 질문에 맞는 자료를 검색한 뒤, 찾은 내용을 언어 모델에 함께 주어 답변하게 하는 방식입니다. 대규모 언어 모델(LLM)은 문장을 이해하고 생성하는 모델이고, 검색기는 답변에 필요한 자료를 찾아오는 구성 요소입니다. RAG 연구의 출발점 중 하나인 Lewis 등의 논문도 언어 모델의 지식과 외부 검색 메모리를 결합합니다. 여기서는 현대적인 문서 기반 RAG를 입문용으로 단순화해 설명합니다. [RAG 원 논문 개요](https://arxiv.org/abs/2005.11401v4)

긴 문서는 보통 작은 조각인 **청크**(chunk)로 나누어 검색합니다. 검색한 청크 중 실제로 답변 모델에 전달한 내용이 **문맥**(context)입니다. 검색 결과 화면에 정답 문서가 있었다는 사실과, 그 내용이 모델의 최종 입력에 들어갔다는 사실은 다릅니다.

![질문에서 검색, 문맥, 답변으로 이어지는 RAG 흐름과 평가 지점]({{ '/img/reviews/2026/rag-evaluation-guide/rag-evaluation-map.svg' | relative_url }})

*작성 도식. RAG의 흐름을 단순화하고, 질문·문맥·답변 사이에 어떤 평가 질문을 던지는지 표시했습니다. 제품의 공식 화면이나 실측 결과가 아닙니다. [RAG Triad의 세 평가 축](https://www.trulens.org/getting_started/core_concepts/rag_triad/)*

## 먼저 구분할 것: 지표와 도구는 다릅니다

Faithfulness는 “근거를 벗어나지 않았는가”라는 평가 항목입니다. RAGAS는 이런 항목을 계산하는 **평가 프레임워크**, 즉 평가를 구현하고 반복할 수 있게 해 주는 도구 모음입니다.

이 글에서 다룰 대표적인 세 접근은 다음과 같습니다. 세 개의 서로 독립적인 정확도 점수를 비교한다는 뜻은 아닙니다. 겹치는 평가 질문을 서로 다른 방식으로 구성하고 활용하는 방법을 비교합니다.

| 접근 | 정체 | 이 글에서 주목할 활용 방식 |
|---|---|---|
| **RAGAS(Ragas)** | 검색·답변 관련 지표를 제공하는 평가 프레임워크 | 어느 구성 요소가 나빠졌는지 지표별로 비교합니다. |
| **TruLens의 RAG Triad** | 세 관계로 RAG를 진단하는 평가 틀과 이를 구현하는 도구 | 질문→문맥, 문맥→답변, 질문→답변을 나누어 살핍니다. |
| **DeepEval** | LLM 애플리케이션 평가·테스트 프레임워크 | 반복 가능한 테스트 사례와 통과 기준으로 품질 저하를 확인합니다. |

이는 인기 순위나 성능 우열표가 아닙니다. 각 도구는 다른 방식의 평가도 지원합니다. 여기서는 초보자가 각각을 이해하기 좋은 관점에 초점을 맞춥니다. [Ragas 지표 목록](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/), [TruLens RAG Triad](https://www.trulens.org/getting_started/core_concepts/rag_triad/), [DeepEval의 CI/CD 평가](https://deepeval.com/docs/evaluation-unit-testing-in-ci-cd)

## 한 가지 예제로 평가 기준 세우기

이후 설명에는 아래 **가상 사내 규정**만 사용합니다. 실제 기업 규정이 아니며, 예제 점수는 계산 원리를 설명하기 위한 수작업 값입니다. 세 도구를 실행해 얻은 벤치마크가 아닙니다.

**질문:** “연간 교육비 한도는 얼마이고, 신청 전에 누구의 승인을 받아야 하나요?”

| 문서 조각 | 내용 | 이 질문에 필요한가요? |
|---|---|---|
| D1 · 교육비 한도 | 직원의 교육비는 연간 최대 100만 원까지 지원합니다. | 필요합니다. 한도에 답합니다. |
| D2 · 승인 절차 | 교육비 신청 전 팀장의 사전 승인을 받아야 합니다. | 필요합니다. 승인자와 시점에 답합니다. |
| D3 · 도서관 안내 | 사내 도서관은 평일 오전 9시부터 오후 6시까지 운영합니다. | 필요하지 않습니다. |

사람이 확인한 **기준 답변**(reference answer)은 “연간 한도는 100만 원이며, 신청 전 팀장의 승인이 필요합니다”입니다. 기준 답변은 정확히 같은 문장을 출력하게 강제하는 정답 문자열이 아닙니다. 평가에 필요한 사실과 조건을 정리한 답안입니다.

이 예제에서 필요한 사실은 두 개입니다. **연간 한도 100만 원**, **신청 전 팀장 승인**입니다. “팀장 승인을 먼저 받아야 하고 연간 최대 백만 원을 지원합니다”도 같은 의미를 담습니다.

평가에 사용할 데이터는 다음처럼 구분해 기록합니다. 이는 도구의 실행 코드가 아니라, 입력을 준비하는 방법입니다.

| 기록 항목 | 무엇을 넣나요? | 예제 |
|---|---|---|
| 질문 | 실제 사용자의 요청 | 교육비 한도와 승인 절차 질문 |
| 검색·전달 문맥 | 모델이 실제로 본 청크와 그 순서 | D1 → D2 → D3 |
| 생성 답변 | 해당 실행이 실제로 출력한 내용 | “100만 원, 팀장 사전 승인” |
| 기준 답변 | 사람이 검토한 필수 사실·조건 | 한도 100만 원 + 팀장 사전 승인 |
| 기준 근거 | 그 사실을 뒷받침하는 문서 ID·버전 | D1과 D2의 고정 버전 |

문맥 칸을 나중에 사람이 찾아 넣은 정답 문서로 덮어쓰면 검색 실패가 감춰집니다. **실행 당시의 문맥과 평가용 기준 근거를 별도로 보관**해야 합니다. DeepEval에서도 실제 검색 결과인 retrieval_context와 참고 자료인 context를 구분합니다. [테스트 사례의 문맥 정의](https://deepeval.com/docs/evaluation-test-cases)

## 1. RAGAS: 검색과 답변을 여러 지표로 분해하기

RAGAS는 RAG를 하나의 총점으로만 보지 않고 여러 평가 항목으로 나누어 측정할 수 있게 합니다. 먼저 네 지표를 구분하면 좋습니다. 아래 표의 입력은 설명하는 **지표 변형이 실질적으로 비교하는 데이터**입니다. SDK가 요구하는 인자 목록 전체와는 다를 수 있습니다.

| 지표 | 쉬운 질문 | 주로 비교하는 데이터 |
|---|---|---|
| Faithfulness | 답변의 주장을 문맥에서 뒷받침할 수 있나요? | 생성 답변 + 전달 문맥 |
| Response/Answer Relevancy | 답변이 사용자의 질문을 다루나요? | 질문 + 생성 답변 |
| Context Precision · 기준 답변 사용 | 답변에 유용한 청크가 앞에 있나요? | 순서 있는 문맥 + 기준 답변, 질문 |
| Context Recall · LLM 기반 | 필요한 기준 사실을 문맥에서 확보했나요? | 기준 답변 + 전달 문맥 |

Ragas는 같은 이름 아래 LLM 기반·문자열 비교·ID 기반 변형도 제공합니다. **어떤 변형을 썼는지까지 기록해야 점수의 의미가 정해집니다.** RAGAS 전체가 언제나 기준 답변 없이 작동한다고 이해하면 안 됩니다. [지표 목록](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/), [Context Precision의 변형](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/context_precision/), [Context Recall의 변형](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/context_recall/)

### Faithfulness: 문맥을 벗어난 주장이 섞였는가

가령 D1과 D2를 제대로 찾았는데 다음처럼 답했다고 하겠습니다.

> 연간 최대 100만 원을 지원합니다. 신청 전 팀장의 승인이 필요합니다. 영수증은 제출하지 않아도 됩니다.

앞의 두 주장은 문맥이 뒷받침합니다. 마지막 영수증 주장은 D1과 D2 어디에도 없습니다. 이 예제처럼 답변을 세 개의 독립 주장으로 나누었다면, Ragas의 기본적인 Faithfulness 계산은 다음처럼 이해할 수 있습니다.

```math
F=\frac{N_{\mathrm{supported}}}{N_{\mathrm{claims}}}=\frac{2}{3}\approx0.67.
```

F는 근거 충실도 점수, 분자는 문맥이 뒷받침하는 주장 수, 분모는 답변의 전체 주장 수입니다. 실제 자동 평가에서는 **주장을 어떻게 나누는지와 문맥이 그 주장을 함의하는지**를 평가 모델이 판단하므로, 이 수작업 예시와 정확히 같은 값이 나온다는 보장은 없습니다. [Ragas Faithfulness 정의와 계산](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/faithfulness/)

![답변의 세 주장 중 두 개는 근거가 있고 영수증 주장은 근거가 없는 예]({{ '/img/reviews/2026/rag-evaluation-guide/claim-support-example.svg' | relative_url }})

*작성 도식. 가상 규정 D1·D2와 답변의 세 주장을 사람이 대조한 예시입니다. 2/3은 설명용 수작업 계산이며 RAGAS 실행 결과가 아닙니다. [계산 원리](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/faithfulness/)*

여기서 “근거가 없다”와 “현실에서 반드시 거짓이다”는 다릅니다. 다른 문서에 영수증 규정이 있을 수도 있지만, 해당 실행에서 모델이 받은 근거로는 정당화할 수 없습니다. 반대로 오래된 문서의 잘못된 한도를 그대로 답하면 근거에는 충실해도 현재 규정상 틀릴 수 있습니다. **충실도와 외부 사실의 정확성은 구분해야 합니다.**

### Response Relevancy: 질문에 답하는가

질문은 교육비 한도와 승인 절차인데, “교육은 직원 성장에 중요합니다”라고만 답하면 질문과 관련된 단어는 있어도 필요한 답을 주지 못합니다.

Ragas의 해당 지표는 생성 답변에서 질문을 역으로 만들고, 원래 질문과 생성된 질문들의 임베딩 유사도를 비교하는 방식을 설명합니다. 임베딩은 문장의 의미를 수치 벡터로 표현한 것입니다. 답변만 보고도 원래 질문을 복원하기 쉬운지 보는 셈입니다. 이는 사실 정확도를 직접 재는 방식은 아닙니다. [Response Relevancy](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/answer_relevance/)

따라서 “연간 한도는 300만 원이고 팀장 승인이 필요합니다”는 질문을 잘 다루면서도 한도는 틀릴 수 있습니다. 관련성이 높다는 판정으로 Faithfulness 검사를 대신할 수 없습니다. 이 지표는 코사인 유사도를 사용하므로 값이 대개 0과 1 사이에 있더라도 **수학적으로 항상 그 범위에 제한된다는 가정은 피해야 합니다.**

### Context Precision: 필요한 청크가 앞에 오는가

D1과 D2가 모두 검색됐더라도, 무관한 청크가 앞을 가득 채운 결과는 다르게 볼 필요가 있습니다. Ragas의 LLM 기반 Context Precision은 관련 청크가 상위에 오는지를 반영하는 순위 지표입니다. 아래 두 검색 결과를 비교해 보겠습니다.

![같은 청크 세 개를 다른 순서로 반환했을 때 Context Precision이 달라지는 예]({{ '/img/reviews/2026/rag-evaluation-guide/retrieval-order-example.svg' | relative_url }})

*작성 도식. D1·D2는 관련, D3는 무관하다고 사람이 미리 정한 가상 예제입니다. 일반 Precision@3은 같지만 관련 청크가 나온 순위에서의 정밀도를 평균하면 차이가 납니다. [Ragas Context Precision 계산](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/context_precision/)*

A는 D1 → D2 → D3, B는 D3 → D1 → D2입니다. 일반적인 Precision@3, 즉 상위 세 결과 중 관련 결과의 비율은 둘 다 2/3입니다. 그러나 관련 결과가 나타난 위치의 Precision을 평균하면 다음과 같습니다.

```math
\mathrm{CP}_A=\frac{1+1}{2}=1,\qquad
\mathrm{CP}_B=\frac{1/2+2/3}{2}=\frac{7}{12}\approx0.58.
```

CP는 이 예제의 Context Precision입니다. A에서는 관련 결과가 첫 번째와 두 번째라 그 지점의 정밀도가 각각 1, 1입니다. B에서는 두 번째와 세 번째에 나타나 각각 1/2, 2/3입니다. **분모 2는 검색한 전체 개수가 아니라 상위 결과 안에서 관련하다고 판단된 청크 수**입니다. 이 계산은 그 판정을 고정한 설명용 예시입니다. [Context Precision의 공식 정의](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/context_precision/)

A의 점수가 1이라고 뒤의 D3가 사라졌다는 뜻도 아닙니다. 이 지표는 순서에 민감하며, 전체 문맥에 섞인 불필요한 정보의 양과도 구분해야 합니다. 또한 문서 ID 집합의 교집합 비율을 계산하는 ID 기반 Context Precision은 이 순위 계산과 다른 변형입니다.

### Context Recall: 필요한 사실이 빠지지 않았는가

이번에는 D1만 전달됐다고 하겠습니다. 한도는 알 수 있지만 승인자를 알 수 없습니다. 기준 답변의 두 필수 사실 중 하나만 문맥에서 뒷받침되므로 다음처럼 계산합니다.

```math
\mathrm{CR}=\frac{N_{\mathrm{reference\ supported}}}{N_{\mathrm{reference\ claims}}}=\frac{1}{2}=0.5.
```

CR은 이 예제의 LLM 기반 Context Recall입니다. 분자는 **기준 답변**의 주장 중 검색 문맥이 뒷받침하는 수, 분모는 기준 답변의 전체 주장 수입니다. Faithfulness가 **생성 답변**의 주장을 분모로 삼는 것과 다릅니다. [Ragas Context Recall](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/context_recall/)

이 차이가 중요합니다. 모델이 승인 절차를 통째로 빠뜨리고 한도만 답하면 생성 답변의 충실도는 좋아 보일 수 있습니다. 그러나 기준 답변과 대조하는 검색 재현율은 누락을 드러냅니다. 찾은 문서가 모두 관련 있어도, 필요한 문서를 다 찾았다는 뜻은 아닙니다.

Ragas 문서에는 기준 답변 대신 생성 답변과 문맥을 비교하는 Context Utilization도 있습니다. 기준 답변이 없을 때 사용할 수 있지만, 그 점수만으로 **답변에도 문맥에도 함께 빠진 사실**까지 확인했다고 할 수는 없습니다. [Context Utilization](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/context_precision/)

### RAGAS를 처음 적용하는 순서

이 글에서는 다음처럼 시작하는 방법을 제안합니다.

1. 같은 질문 집합에서 질문·생성 답변·실제 전달 문맥을 저장합니다.
2. Faithfulness와 Response Relevancy로 근거 이탈과 질문 이탈을 먼저 나눕니다.
3. 일부 질문에 사람이 검토한 기준 답변을 붙이고 Context Precision·Recall을 추가합니다.
4. 청크 크기나 검색 후 순위 재정렬 방식 하나를 바꾼 뒤, 같은 사례별 점수를 비교합니다.
5. 점수가 크게 바뀐 사례의 근거와 평가 이유를 직접 읽습니다.

이때 검색한 개수인 top-k를 늘려 재현율을 올렸다면, 문맥 길이·비용·응답 시간도 함께 비교해야 합니다. 검색 결과가 많아진 것 자체를 품질 개선으로 부르지는 않습니다.

## 2. TruLens RAG Triad: 세 관계로 고장 위치 찾기

TruLens의 **RAG Triad**는 질문, 검색 문맥, 답변 사이의 세 관계를 평가합니다. 이름을 외우기보다 어느 두 대상을 비교하는지 떠올리면 이해하기 쉽습니다.

| 관계 | 지표 | 교육비 예제에서 묻는 내용 |
|---|---|---|
| 질문 → 문맥 | Context Relevance | 교육비 질문에 도서관 안내가 왜 검색됐나요? |
| 문맥 → 답변 | Groundedness | 영수증이 필요 없다는 주장을 문맥이 뒷받침하나요? |
| 질문 → 답변 | Answer Relevance | 한도와 승인 절차에 실제로 답했나요? |

Groundedness는 답변을 주장으로 나누어 문맥에서 근거를 찾는 관점입니다. 이 세 축의 기본 설명에는 사람이 쓴 기준 답변이 필요하지 않습니다. 다만 **TruLens 전체가 기준 답변 평가를 지원하지 않는다는 뜻은 아닙니다.** [RAG Triad 설명](https://www.trulens.org/getting_started/core_concepts/rag_triad/), [Ground Truth 평가](https://www.trulens.org/getting_started/quickstarts/groundtruth_evals_for_retrieval_systems/)

### 같은 낮은 점수라도 원인은 다릅니다

아래 표는 실제 측정값이 아니라, 세 축을 이용한 **진단 가설**입니다. “높음/낮음”의 판정은 선택한 평가 함수와 사람 검토에 따라 정합니다.

| 관찰한 패턴 | 가능한 원인 | 먼저 확인할 부분 |
|---|---|---|
| 문맥 관련성 낮음 | 무관한 자료가 많이 검색됐습니다. | 질문 해석, 검색 필터, 검색·재정렬 결과 |
| 문맥은 관련 있지만 근거 충실도 낮음 | 답변이 문맥에 없는 조건을 추가했습니다. | 실제 모델 입력, 답변의 주장, 생성 지침 |
| 근거 충실도는 높지만 답변 관련성 낮음 | 문서 내용을 옮겼지만 질문의 요구를 놓쳤습니다. | 질문의 복합 조건과 누락된 답변 항목 |
| 세 축이 좋아 보이지만 사람이 오답 판정 | 문서가 오래됐거나 평가 기준이 부정확할 수 있습니다. | 문서 버전, 기준 답변, 평가자의 판단 근거 |

여기서 Context Relevance가 높다고 Context Recall이 높다는 뜻은 아닙니다. D1만 검색해도 D1 자체는 질문에 관련됩니다. 그러나 승인 절차인 D2의 누락은 기준 답변이나 기준 근거가 있어야 더 직접적으로 확인할 수 있습니다.

TruLens Quickstart는 앱의 검색·생성 과정을 기록하고 feedback 함수를 연결해 결과를 살펴보는 흐름을 보여 줍니다. **실행 추적**(trace)은 한 요청에서 어떤 입력·검색·출력이 오갔는지 연결한 기록입니다. 총점만 남기는 대신 문제 답변에서 실제 청크와 평가 이유까지 돌아갈 수 있게 하는 데 의미가 있습니다. [TruLens Quickstart](https://www.trulens.org/getting_started/quickstarts/quickstart/)

### “세 점수가 좋다”는 신호의 한계

관련성·근거 충실도는 반드시 필요한 점검이지만, 자동 평가 세 개의 통과가 모든 오답의 부재를 증명하지는 않습니다. 원본 문서가 틀렸거나 판정 모델이 근거를 잘못 읽는 경우도 별도로 봐야 합니다. 이 글에서는 Triad를 **환각이 절대로 없다는 인증서보다 오류를 나누어 찾는 틀**로 사용합니다.

이 해석에 맞추려면 사람 판정과 자동 평가의 일치 여부를 확인해야 합니다. TruLens의 Judge Alignment 문서도 대표 평가 집합, 평가 설정 고정, 같은 사례끼리의 비교, 별도 보류 데이터에서의 확인을 다룹니다. [LLM Judge Alignment](https://www.trulens.org/component_guides/evaluation/llm_judge_alignment/)

## 3. DeepEval: 평가를 반복 가능한 테스트로 만들기

첫 실험의 점수가 좋더라도 프롬프트나 검색 설정을 바꾼 뒤 품질이 떨어질 수 있습니다. **회귀**(regression)는 이런 변경으로 기존에 잘 풀던 사례를 더 이상 잘 풀지 못하는 현상입니다.

DeepEval은 입력과 출력을 테스트 사례로 만들고, 선택한 지표와 통과 기준을 반복 적용할 수 있게 합니다. 공식 문서는 pytest 연동과 CI/CD 실행을 설명합니다. CI/CD는 코드 변경 때 검사·배포 절차를 자동 실행하는 개발 과정입니다. 처음부터 자동 배포를 붙일 필요는 없고, 같은 테스트 사례를 재실행하는 용도로 이해해도 됩니다. [DeepEval CI/CD 평가](https://deepeval.com/docs/evaluation-unit-testing-in-ci-cd)

### 테스트 사례에서 어떤 칸을 채우는가

| DeepEval 필드 | 의미 | 교육비 예제 |
|---|---|---|
| input | 사용자 입력 | 교육비 한도와 승인 절차 질문 |
| actual_output | 실제 생성 답변 | 해당 실행의 답변 원문 |
| retrieval_context | 실제 검색·전달 자료 | D1·D2·D3의 내용과 순서 |
| expected_output | 평가용 기준 답변 | 100만 원 + 팀장 사전 승인 |

생성 모델의 답변을 expected_output에 넣어 스스로 정답을 만들면 평가 기준도 같이 흔들립니다. 기준 답변은 도메인 담당자가 근거를 확인해 작성해야 합니다. [LLMTestCase 정의](https://deepeval.com/docs/evaluation-test-cases)

여기서 actual_output과 expected_output을 문자 그대로 일치시키려는 것은 아닙니다. 같은 사실을 다른 말로 표현해도 허용하되, “사전”을 “사후”로 바꾸는 중요한 조건 차이는 잡도록 평가 기준을 세워야 합니다.

### 대표 지표를 테스트에 연결하기

DeepEval도 Answer Relevancy, Faithfulness, Contextual Precision, Contextual Recall 등의 지표를 제공합니다. 기본적인 단일 턴 사례에서 Faithfulness는 input·actual_output·retrieval_context를, Contextual Precision과 Recall은 여기에 expected_output까지 요구합니다. 기준 답변이 없어도 쓸 수 있는 지표와 필요한 지표가 함께 있습니다. [Faithfulness 입력](https://deepeval.com/docs/metrics-faithfulness), [Contextual Precision 입력](https://deepeval.com/docs/metrics-contextual-precision), [Contextual Recall 입력](https://deepeval.com/docs/metrics-contextual-recall)

중요한 차이는 **이름이 비슷해도 계산이 완전히 같지는 않다**는 점입니다. 예를 들어 Ragas의 Answer Relevancy는 답변에서 역생성한 질문과 원 질문의 임베딩 유사도를 쓰지만, DeepEval의 LLM 평가 모드 Answer Relevancy는 답변에서 추출한 진술 중 질문과 관련 있는 진술의 비율을 설명합니다. 같은 데이터에서 둘 다 0.8이 나와도 같은 확률이나 같은 수준의 정확도를 뜻하지 않습니다. [Ragas 계산](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/answer_relevance/), [DeepEval 계산](https://deepeval.com/docs/metrics-answer-relevancy)

또한 DeepEval의 Faithfulness 문서는 LLM 평가 모드에서 문맥과의 **모순 여부**를 중심으로 진술을 판정한다고 설명합니다. Ragas의 “문맥에서 주장을 뒷받침할 수 있는가”와 표현·판정 규칙이 같다고 가정하지 않습니다. 근거에 없는 추가 정보를 어떻게 처리하는지는 실제 평가 이유를 확인해야 합니다. [DeepEval Faithfulness 계산과 모드](https://deepeval.com/docs/metrics-faithfulness)

### 합격선은 도구가 대신 정해 주지 않습니다

가령 팀이 “교육비 승인자를 틀리는 사례는 통과시키지 않는다”는 기준을 세웠다면, 전체 평균과 별도로 그 사례의 실패 여부를 검사할 수 있습니다. 이 문장은 도구의 기본 기준이 아니라 **운영팀이 정할 평가 정책의 예시**입니다.

문서 예제에 있는 threshold 값을 그대로 서비스의 정답 기준으로 옮기기보다, 사람이 좋다고 판정한 답변과 문제가 있다고 판정한 답변을 모아 점수 분포를 확인해야 합니다. 작은 표현 차이를 과도하게 실패 처리하지 않는지, 중요한 숫자 오류는 통과시키지 않는지 함께 확인합니다.

현재 DeepEval 문서는 LLM·hybrid·system_one 등의 평가 모드를 구분합니다. 이 글의 계산 비교는 **LLM 평가 모드**를 기준으로 합니다. 모드가 바뀌면 점수 산출 과정도 달라질 수 있으므로, 버전·모드·평가 모델·평가 지침·임계값을 묶어 기록합니다. [평가 모드별 계산 차이](https://deepeval.com/docs/metrics-faithfulness)

## 세 접근 중 무엇부터 쓰면 좋을까

| 지금 풀고 싶은 문제 | 시작하기 좋은 관점 | 필요한 준비 |
|---|---|---|
| 청크 크기나 검색·재정렬 설정을 비교하고 싶습니다. | RAGAS의 검색·답변 지표를 따로 비교합니다. | 고정 질문 집합, 실제 문맥, 일부 기준 답변 |
| 챗봇이 왜 틀렸는지 요청별로 추적하고 싶습니다. | TruLens RAG Triad로 세 관계를 나눠 읽습니다. | 질문·검색·출력을 연결한 실행 기록 |
| 변경할 때마다 기존 품질이 떨어지는지 검사하고 싶습니다. | DeepEval 테스트 사례와 통과 정책을 적용합니다. | 검토한 테스트 집합과 평가 설정 |

이 표는 각 도구의 독점 기능을 뜻하지 않는 **이 글의 선택 가이드**입니다. Ragas로도 반복 평가를 만들 수 있고, TruLens도 기준 답변 평가를 지원하며, DeepEval도 구성 요소별 진단이 가능합니다. 핵심은 도구 세 개를 동시에 도입하는 것이 아니라, 같은 입력과 판단 기준으로 평가를 반복하는 것입니다.

## 도구 없이도 먼저 해 볼 수 있는 작은 평가

처음이라면 SDK 설치보다 아래 기록을 손으로 한 번 만들어 보는 편이 지표를 이해하기 쉽습니다. 아래 순서와 사례 구성은 이 글의 입문용 제안이며, 통계적으로 충분한 평가 규모라는 주장은 아닙니다.

### 1. 평가할 지식의 버전을 고정합니다

어느 날짜의 규정으로 정답을 판단할지 정합니다. 문서 제목만 적지 말고 문서 ID·버전·수정일도 남깁니다. 청크 분할을 바꾸면 청크 ID도 달라질 수 있으므로 이전 결과와 연결할 원본 문서·범위도 보관합니다.

### 2. 쉬운 질문과 어려운 질문을 함께 만듭니다

| 사례 | 확인할 능력 | 교육비 예제에서 바꿀 질문 |
|---|---|---|
| 한 문서에서 답할 수 있음 | 기본 검색과 답변 | “연간 한도는 얼마인가요?” |
| 두 문서를 결합해야 함 | 필요한 근거의 누락 | “한도와 사전 승인자는 누구인가요?” |
| 표현이 달라짐 | 같은 의미의 질문 처리 | “1년에 얼마까지, 누구한테 먼저 허락받나요?” |
| 숫자·조건을 확인해야 함 | 세부 사실 보존 | “100만 원인가요, 300만 원인가요?” |
| 문서에 답이 없음 | 근거 부족을 인정함 | “영수증을 안 내도 되나요?” |
| 구버전과 현행이 함께 있음 | 적용 문서의 선택 | 별도 구버전 문서를 추가한 뒤 현행 한도를 묻습니다. |

마지막 사례는 원래 D1~D3 외에 구버전을 **별도 테스트 데이터로 추가**하는 확장입니다. 정답이 없는 질문에는 숫자 정답 대신 “제공된 자료로는 영수증 요건을 확인할 수 없다”는 기대 행동을 정합니다. 무조건 답변하도록 만들면 모르는 내용을 지어내는 시스템을 높게 평가할 수 있습니다.

### 3. 실행 결과와 사람 판정을 함께 남깁니다

각 질문에 대해 실제 문맥, 생성 답변, 필수 사실의 누락, 근거 없는 주장, 답변 가능 여부를 표로 정리합니다. 사람이 왜 통과·실패로 판단했는지도 한 문장으로 적습니다. “영수증 조건이 문맥에 없다” 같은 이유가 있어야 자동 평가의 잘못된 판정도 발견할 수 있습니다.

### 4. 한 가지 설정만 바꾸어 같은 질문을 다시 평가합니다

예를 들어 검색 후 재정렬만 추가합니다. 그 외 문서 집합, 질문, 생성 모델, 프롬프트와 평가 설정은 유지합니다. 여러 항목을 한꺼번에 바꾸면 어떤 변경이 효과를 만들었는지 알기 어렵습니다.

결과는 전체 평균뿐 아니라 **질문별 전후 차이와 질문 유형별 성적**을 봅니다. 교육비 한도 질문은 좋아졌지만 승인 절차 질문이 나빠졌다면 그 변화가 평균에 가려지지 않도록 합니다. 지연 시간과 처리 비용도 같은 실행에서 기록합니다.

### 5. 자동 평가를 사람 판정에 맞추어 점검합니다

LLM-as-a-judge는 별도의 언어 모델이 답변을 채점하는 방식입니다. 더 많은 사례를 살피는 데 도움이 되지만, 그 채점자도 판단을 잘못하거나 같은 입력에 다른 판정을 내릴 수 있습니다. 사람 판정과 어긋나는 사례, 합격선 근처 사례를 읽고 평가 지침을 조정한 뒤, 조정에 쓰지 않은 별도 사례에서 다시 확인합니다. 평가 설정과 대표 데이터, 보류 집합을 구분하는 방법은 TruLens의 Judge Alignment 문서에서도 다룹니다. [Judge Alignment](https://www.trulens.org/component_guides/evaluation/llm_judge_alignment/)

도구를 로컬에서 실행한다는 사실과 평가 모델도 로컬에서 실행한다는 사실은 다릅니다. API 기반 채점자를 선택하면 평가 호출과 비용이 생길 수 있습니다. 이 글의 가상 예제는 그런 API 호출 없이 손으로 계산했으며, 실제 서비스 평가를 실행한 결과가 아닙니다.

## 점수를 읽을 때 자주 생기는 오해

**“Faithfulness 0.9면 정답일 확률이 90%인가요?”** 그렇지 않습니다. 지표 정의에 따른 주장 비율이나 모델 판정값이지, 정답 사건에 대해 보정된 확률이라고 볼 근거는 없습니다. 근거가 오래됐는지, 중요한 주장 하나가 틀렸는지도 함께 살펴야 합니다.

**“검색 재현율이 높으면 답변도 좋은가요?”** 필요한 자료를 찾아도 모델이 놓치거나 무관한 정보를 답할 수 있습니다. 검색과 생성은 구분해 평가해야 합니다.

**“기준 답변이 없으니 평가를 못 하나요?”** 근거 충실도와 질문 관련성처럼 기준 답변 없이 가능한 평가부터 시작할 수 있습니다. 다만 필요한 사실이 완전히 누락됐는지 확인하려면 사람이 정한 기준 답변·근거가 도움이 됩니다.

**“근거 충실도가 높으면 인용도 맞나요?”** 전체 문맥이 주장을 지지하는지와, 답변에 붙인 특정 인용 링크·페이지가 그 주장을 지지하는지는 별도 질문입니다. 인용 정확성이 필요하면 주장과 해당 인용 위치를 직접 연결해 확인하도록 평가 항목을 추가해야 합니다.

**“여러 점수를 평균하면 품질을 한 숫자로 알 수 있나요?”** 서로 다른 실패 원인을 합치면 중요한 문제가 감춰질 수 있습니다. 우선 지표별로 보고, 필요할 때만 서비스 목적에 맞는 집계 규칙과 필수 통과 조건을 정합니다. 특히 도구별 점수를 같은 척도로 가정해 섞지는 않습니다.

RAG 평가의 목적은 높은 숫자를 얻는 데서 끝나지 않습니다. **찾아야 할 근거를 찾았는지, 그 근거를 지켰는지, 사용자의 질문을 해결했는지**를 분리해 확인하고, 어떤 변경이 어느 부분을 바꾸었는지 설명할 수 있어야 합니다. RAGAS는 이를 지표로 나누고, RAG Triad는 세 관계로 읽게 하며, DeepEval은 반복 가능한 테스트로 연결하는 출발점을 제공합니다.

## 참고 자료와 확인 범위

이 글은 **2026년 10월 24일** 확인한 공식 문서를 바탕으로 한 입문 가이드입니다. 문서의 latest 주소는 이후 바뀔 수 있습니다. 제품별 우열 실험이나 SDK 실행 결과를 보고하는 글이 아니며, 그림과 숫자 예시는 직접 구성한 설명용 자료입니다. 실제 도입 시에는 사용한 패키지 버전과 지표 구현·설정을 함께 기록해야 합니다.

- [Ragas: 사용 가능한 지표](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/)
- [Ragas: Faithfulness](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/faithfulness/)
- [Ragas: Response Relevancy](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/answer_relevance/)
- [Ragas: Context Precision과 변형](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/context_precision/)
- [Ragas: Context Recall과 변형](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/context_recall/)
- [TruLens: RAG Triad](https://www.trulens.org/getting_started/core_concepts/rag_triad/)
- [TruLens: Quickstart](https://www.trulens.org/getting_started/quickstarts/quickstart/)
- [TruLens: Judge Alignment](https://www.trulens.org/component_guides/evaluation/llm_judge_alignment/)
- [DeepEval: RAG 평가 가이드](https://deepeval.com/guides/guides-rag-evaluation)
- [DeepEval: Faithfulness](https://deepeval.com/docs/metrics-faithfulness)
- [DeepEval: Answer Relevancy](https://deepeval.com/docs/metrics-answer-relevancy)
- [DeepEval: Contextual Precision](https://deepeval.com/docs/metrics-contextual-precision)
- [DeepEval: Contextual Recall](https://deepeval.com/docs/metrics-contextual-recall)
- [DeepEval: Single-Turn Test Case](https://deepeval.com/docs/evaluation-test-cases)
- [DeepEval: Unit Testing in CI/CD](https://deepeval.com/docs/evaluation-unit-testing-in-ci-cd)
