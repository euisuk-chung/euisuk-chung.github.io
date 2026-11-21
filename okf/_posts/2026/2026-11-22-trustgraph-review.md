---
type: "Repo Review"
title: "[Repo Review] TrustGraph — 문서의 관계를 읽고, 답변의 근거와 열람 범위를 나누기"
description: "TrustGraph의 온톨로지 기반 지식 추출과 그래프 탐색, 노드별 조회 정책 및 출처 기록이 연결되는 과정을 고정 커밋의 코드로 살펴봅니다."
date: "2026-11-22"
tags:
  - "Repo Review"
  - "AI Agent"
  - "RAG"
  - "Python"
  - "MCP"
resource: "https://github.com/trustgraph-ai/trustgraph/tree/17e5d7423ac080b0162f7242694c520551b9df0c"
generated:
  by: "process:blog-review"
  at: "2026-11-22T06:12:00+09:00"
sources:
  - id: "github:trustgraph-ai/trustgraph"
    resource: "https://github.com/trustgraph-ai/trustgraph/tree/17e5d7423ac080b0162f7242694c520551b9df0c"
    title: "TrustGraph"
    author: "trustgraph-ai"
status: "stable"
year: "2026"
analyzed_at: "2026-11-22T06:12:00+09:00"
source_id: "trustgraph-ai/trustgraph"
source_revision: "17e5d7423ac080b0162f7242694c520551b9df0c"
source_type: "repo"
source_url: "https://github.com/trustgraph-ai/trustgraph/tree/17e5d7423ac080b0162f7242694c520551b9df0c"
visual_sources:
  - path: "img/reviews/2026/trustgraph-review/extraction-flow.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/trustgraph-flow/trustgraph/extract/kg/ontology/extract.py#L193-L290"
    caption: "문서 조각과 온톨로지에서 추출·검증을 거쳐 트리플과 개체 문맥을 발행하는 흐름. 리뷰어 작성, 분석 커밋 기준."
  - path: "img/reviews/2026/trustgraph-review/query-flow.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/trustgraph-flow/trustgraph/retrieval/graph_rag/graph_rag.py#L934-L1149"
    caption: "질문에서 개체 연결·관계 탐색·재순위화·출처 추적을 거쳐 답을 합성하는 흐름. 리뷰어 작성, 분석 커밋 기준."
---

## 들어가며: 문서를 찾은 다음에도 남는 문제

사내 문서를 검색해 답하는 AI를 생각해 보겠습니다. 비슷한 문단을 잘 찾았어도, 그 안의 사람·부서·계약 관계를 어떻게 연결할지, 사용자에게 보여 주면 안 되는 정보는 어디서 걸러낼지, 답변의 근거를 어떻게 되짚을지는 별개의 문제입니다.

TrustGraph는 이 문제를 **문서에서 지식을 만드는 과정과, 지식을 조회하는 과정**으로 나누어 다룹니다. 문서를 회사가 정의한 개념·관계에 맞춰 그래프로 바꾸고, 그 그래프를 검색·탐색해 답변 재료로 쓰며, 조회 경로에 정책과 출처 기록을 붙이는 프로젝트입니다. README는 이를 “AI 에이전트를 위한 오픈소스 온톨로지 런타임”으로 소개합니다. [README의 전체 흐름](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/README.md#L30-L70)을 출발점으로 실제 구현을 살펴보겠습니다.

분석 대상은 2026년 11월 22일 확인한 커밋 `17e5d7423ac080b0162f7242694c520551b9df0c`입니다. 이 글은 코드와 문서를 읽은 정적 분석이며, 대상 프로그램의 설치·실행·성능 시험은 수행하지 않았습니다.

## TrustGraph는 무엇인가

온톨로지(ontology)는 “우리 조직에서 어떤 종류의 대상과 관계를 사용할 것인가”를 정의한 어휘와 규칙입니다. RDF는 지식을 **주어·관계·목적어의 세 항목**, 즉 트리플(triple)로 표현합니다. 이름이 붙은 그래프(named graph)는 이 트리플들을 용도나 출처별 묶음으로 구분하는 단위입니다.

예를 들어 ‘어느 회사에 소속되었는가’라는 관계의 주어는 사람, 목적어는 조직이어야 한다는 식으로 연결 규칙을 정할 수 있습니다. 이는 개념 설명을 위한 예이며, 아래에서 레포의 실제 실행 결과로 제시하는 데이터는 아닙니다. TrustGraph는 이런 규칙을 문서 추출 프롬프트에 전달하고, 추출 결과를 RDF로 바꾸는 단계에서도 일부 제약을 확인합니다.

| 구성 | 하는 일 | 이 글에서 확인한 구현 범위 |
| --- | --- | --- |
| OntologyRAG | 문서 조각에 관련된 온톨로지를 찾아 지식 추출을 유도 | 부분집합 조회, JSONL 응답 처리, RDF 변환 |
| GraphRAG | 질문에서 출발해 관련 개체와 관계를 찾고 답변 생성 | 개념 추출, 벡터 검색, 단계별 탐색·재순위화 |
| 정책 필터 | 사용자 문맥에 따라 조회 결과의 노드를 걸러냄 | 정책 서비스 분기, 노드 평가, 결과 중계 |
| 출처·설명 기록 | 어떤 문서와 탐색 과정에서 답이 나왔는지 남김 | 추출 출처와 질문·탐색·합성 단계의 별도 그래프 |
| MCP | 외부 에이전트가 도구로 호출할 수 있는 연결면 | 토큰을 게이트웨이로 전달하는 인증 경계 |

여기서 **온톨로지 제약과 조회 정책은 서로 다른 검사**입니다. 전자는 ‘이 관계의 타입이 맞는가’를, 후자는 ‘이 사용자에게 이 노드를 보여 줄 수 있는가’를 다룹니다. [RDF 변환](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/trustgraph-flow/trustgraph/extract/kg/ontology/triple_converter.py#L125-L179)과 [정책 필터](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/trustgraph-flow/trustgraph/policy/policy_filter.py#L235-L325)는 실제로 별도 모듈입니다.

## 아키텍처: 하나의 함수보다 여러 처리기의 연결

저장소는 Python 패키지들을 나눠 놓았습니다. `trustgraph-base`에는 메시지 스키마와 서비스 클라이언트·처리기 기반 구조가 있고, `trustgraph-flow`에는 추출·검색·정책·저장소 연동 처리기가 있습니다. `trustgraph-mcp`는 MCP 서버, `trustgraph-cli`는 명령줄 진입점을 맡습니다. 모델·문서 디코딩용 패키지도 별도로 존재합니다. [base 매니페스트](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/trustgraph-base/pyproject.toml#L5-L30)와 [flow 매니페스트](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/trustgraph-flow/pyproject.toml#L5-L100)를 보면 각각의 의존성과 명령 진입점이 드러납니다.

예컨대 `kg-extract-ontology`, `graph-rag`, `api-gateway`는 `trustgraph-flow/pyproject.toml`에 등록된 서로 다른 명령입니다. 추출기는 `Chunk` 메시지를 받아 `Triples`와 `EntityContexts`를 발행하도록 명세를 등록합니다. GraphRAG 역시 프롬프트·임베딩·트리플 조회·재순위화 클라이언트를 flow에서 받아 사용합니다. 따라서 이 레포를 읽을 때는 함수 호출과 함께 **어느 요청·응답 큐에 연결되는가**를 봐야 합니다. [추출기 입출력 명세](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/trustgraph-flow/trustgraph/extract/kg/ontology/extract.py#L94-L132), [검색 처리기의 클라이언트 연결](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/trustgraph-flow/trustgraph/retrieval/graph_rag/rag.py#L174-L184)을 참고할 수 있습니다.

![문서 조각과 온톨로지 선택에서 추출·검증을 거쳐 트리플과 개체 문맥을 발행하는 흐름]({{ '/img/reviews/2026/trustgraph-review/extraction-flow.svg' | relative_url }})

문서에서 그래프 재료를 만드는 흐름입니다. 리뷰어 작성, 분석 커밋 기준. [추출 처리기](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/trustgraph-flow/trustgraph/extract/kg/ontology/extract.py#L193-L290)와 [RDF 변환기](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/trustgraph-flow/trustgraph/extract/kg/ontology/triple_converter.py#L125-L179)를 바탕으로 그렸습니다.
{: .caption}

이 도식의 출력은 서비스가 발행하는 메시지입니다. 그 뒤의 실제 저장소와 메시지 브로커 연결은 배포 flow 구성에 달려 있습니다. README에 Cassandra·Qdrant·Pulsar·RabbitMQ 등의 선택지가 나오지만, 그림 하나가 모든 배포를 고정해서 나타내지는 않습니다.

## 작동 원리: 문서에서 규칙에 맞는 지식 만들기

### 1. 전체 온톨로지 대신 관련 부분을 요청합니다

추출기의 `on_message`는 메시지의 바이트열을 UTF-8로 읽고, `_select_ontology_subset`을 호출합니다. 이 메서드는 문서 조각을 문장·구 단위로 처리한 뒤 각 세그먼트에 대해 `operation="subset"` 요청을 온톨로지 서비스로 보냅니다. 받은 클래스, 객체 속성, 데이터 속성은 사전으로 합칩니다. 추출기에 관련 요소가 하나도 도착하지 않으면 해당 조각은 결과를 발행하지 않고 반환합니다. [선택 요청과 병합](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/trustgraph-flow/trustgraph/extract/kg/ontology/extract.py#L138-L191), [빈 선택 결과 분기](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/trustgraph-flow/trustgraph/extract/kg/ontology/extract.py#L214-L228)에 이 순서가 있습니다.

실제 요청을 받는 온톨로지 서비스는 준비된 온톨로지를 대상으로 임베딩 유사도 검색을 합니다. 다만 항상 검색 결과만 쓰지는 않습니다. 전체 요소 수가 설정한 기준보다 작거나, 벡터 저장소가 없거나 비었거나, 검색 결과가 없으면 준비된 온톨로지 전체를 반환합니다. 기본 우회 기준은 5이며 비교는 ‘5 미만’입니다. 따라서 ‘검색에 실패하면 언제나 추출을 포기한다’고 이해하면 실제 코드와 다릅니다. [서비스의 부분집합 선택과 우회 경로](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/trustgraph-flow/trustgraph/ontology/service.py#L551-L653)를 함께 봐야 합니다.

이 부분은 README의 ‘유사도 기반 선택’이라는 한 문장을 구체화합니다. 보통은 필요한 정의를 골라 프롬프트를 구성하되, 작은 어휘 집합이나 검색 결과 부재에는 전체 정의로 돌아가는 구조입니다. 그에 따른 토큰 비용이나 추출 품질은 이 정적 분석으로 측정하지 않았습니다.

### 2. LLM의 JSONL 응답을 구조화한 뒤 RDF로 변환합니다

선택한 `classes`, `object_properties`, `datatype_properties`와 원문 `text`가 `extract-with-ontologies` 프롬프트의 변수가 됩니다. 반환값은 JSONL용 `result.objects`로 읽고, 파서를 거쳐 개체·관계·속성 목록으로 나눕니다. 이어 `TripleConverter.convert_all`이 RDF 트리플로 변환합니다. [프롬프트 호출부터 변환까지](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/trustgraph-flow/trustgraph/extract/kg/ontology/extract.py#L308-L378)에 이 과정이 모여 있습니다.

개체는 타입과 표시 이름을 나타내는 트리플로 바뀝니다. 관계는 주어 URI·속성 URI·목적어 URI로 바뀝니다. 이때 속성 이름을 온톨로지에서 찾지 못하면 관계를 버리고, `domain` 또는 `range`가 선언되어 있으면 입력 타입과 비교합니다. 하위 클래스의 조상에 요구 타입이 있으면 허용하는 검사도 들어 있습니다. [타입·라벨 생성](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/trustgraph-flow/trustgraph/extract/kg/ontology/triple_converter.py#L84-L123), [조상 검사](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/trustgraph-flow/trustgraph/extract/kg/ontology/triple_converter.py#L35-L52)를 확인했습니다.

다음은 Apache-2.0으로 제공된 원본에서 **domain 검사 분기만 발췌**한 코드입니다. 앞의 URI 조회와 뒤의 range 검사·트리플 생성은 생략했습니다.

```python
if domain and not self._matches_class_constraint(relationship.subject_type, domain):
    logger.warning(
        f"Domain violation: '{relationship.relation}' expects "
        f"domain '{domain}', got subject type "
        f"'{relationship.subject_type}', skipping"
    )
    return None
```

출처: [TripleConverter.convert_relationship, 158–164행](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/trustgraph-flow/trustgraph/extract/kg/ontology/triple_converter.py#L158-L164), Copyright 2024–2026 TrustGraph, [Apache-2.0](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/LICENSE).

입력은 LLM이 제시한 관계와 선택된 속성 정의입니다. 핵심 결정은 ‘관계가 요구하는 주어 타입과 일치하는가’이고, 어긋나면 출력 트리플 대신 `None`을 돌려줍니다. 이를 통해 **생성 모델의 제안 뒤에 결정적인 타입 검사를 붙이는 구조**를 읽을 수 있습니다. 다만 타입이 맞는 관계라고 해서 문서의 사실까지 참임을 증명하는 것은 아닙니다.

### 3. 내용 트리플과 출처를 함께 발행합니다

추출 결과가 있으면 코드가 하위 그래프 식별자를 만들고, 추출된 관계가 어느 문서 조각에서 왔는지 나타내는 provenance 트리플을 생성합니다. 이 출처 기록은 `urn:graph:source`에 배치됩니다. 내용 트리플에 온톨로지 정의 트리플을 합친 뒤 배치로 발행하고, 별도로 개체 문맥을 만들어 발행합니다. [출처 생성과 두 출력](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/trustgraph-flow/trustgraph/extract/kg/ontology/extract.py#L251-L290)을 보면 ‘그래프 저장용 정보’와 ‘개체 문맥’이 갈라지는 지점이 보입니다.

여기서 provenance는 출처를 거슬러 올라갈 수 있는 연결입니다. 추출 내용이 올바르다는 판정 자체를 대신하지는 않습니다. 독자는 관계의 타입 검사와 출처 기록을 각각의 역할로 이해하는 편이 정확합니다.

## 작동 원리: 질문에서 답변까지 그래프를 따라가기

### 1. 시작할 개체를 찾습니다

GraphRAG 서비스는 요청마다 `GraphRag` 인스턴스를 만듭니다. 코드 주석은 라벨 캐시가 요청 범위에 머물도록 하기 위한 선택이라고 설명하며, workspace 격리는 이 클래스가 아니라 신뢰하는 flow 계층의 책임이라고 명시합니다. [인스턴스 생성](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/trustgraph-flow/trustgraph/retrieval/graph_rag/rag.py#L174-L184)과 [클래스의 격리 경계 설명](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/trustgraph-flow/trustgraph/retrieval/graph_rag/graph_rag.py#L875-L895)을 구분해서 읽어야 합니다.

일반 경로에서는 질문을 `extract-concepts` 프롬프트에 보내 개념들을 뽑고, 각 개념의 임베딩으로 그래프 개체를 검색합니다. 개념 추출 결과가 비면 원래 질문을 사용합니다. 검색 결과는 순서를 유지하며 중복 개체를 제거합니다. [개념 추출과 개체 검색](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/trustgraph-flow/trustgraph/retrieval/graph_rag/graph_rag.py#L168-L284)에 구현되어 있습니다.

두 가지 단축 경로도 있습니다. `grounding_seeds`는 사용할 개념을 직접 주어 LLM 개념 추출을 건너뛰지만 임베딩 검색은 수행합니다. `graph_seeds`는 시작 개체 URI를 직접 주어 개념 추출과 개체 검색을 모두 건너뜁니다. 서비스는 두 값을 동시에 주면 오류를 발생시킵니다. 이 차이를 모르면 ‘seed를 넣었다’는 설명만으로는 실제 실행 경로를 알 수 없습니다. [시작점 선택](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/trustgraph-flow/trustgraph/retrieval/graph_rag/graph_rag.py#L204-L238), [동시 지정 거부](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/trustgraph-flow/trustgraph/retrieval/graph_rag/rag.py#L216-L225)가 근거입니다.

![질문을 개체에 연결하고 관계를 탐색·재순위화한 뒤 출처 문서와 답변을 만드는 검색 흐름]({{ '/img/reviews/2026/trustgraph-review/query-flow.svg' | relative_url }})

질문을 그래프 관계와 답변으로 연결하는 흐름입니다. 리뷰어 작성, 분석 커밋 기준. [GraphRag.query](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/trustgraph-flow/trustgraph/retrieval/graph_rag/graph_rag.py#L934-L1006)와 [hop_and_filter](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/trustgraph-flow/trustgraph/retrieval/graph_rag/graph_rag.py#L469-L740)를 바탕으로 그렸으며, 트리플 조회의 정책 적용은 flow 연결에 따라 달라집니다.
{: .caption}

### 2. 이웃 관계를 읽고, 질문에 맞는 관계를 다시 고릅니다

시작 개체에서 인접 관계를 읽는 한 번의 이동을 hop이라고 합니다. `hop_and_filter`는 현재 탐색 집합(frontier)에서 아직 방문하지 않은 개체를 골라 관계를 요청합니다. 개체가 주어·관계·목적어 위치에 있는 세 종류의 트리플 조회를 만들고, 사용자 문맥도 조회 요청에 전달합니다. [배치 트리플 조회](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/trustgraph-flow/trustgraph/retrieval/graph_rag/graph_rag.py#L323-L409)가 이 경계를 보여 줍니다.

각 hop에서는 언어, 스키마용 관계, 이미 본 관계, 지정된 관계 조건 등을 검사합니다. 남은 관계의 URI를 읽을 수 있는 라벨로 바꾸고 재순위화(reranking) 서비스에 전달합니다. 이 서비스는 질문의 개념과 관계 텍스트를 함께 평가하는 cross-encoder 방식의 연결면입니다. 반환된 상위 관계를 쌓고 그 관계의 양 끝 개체를 다음 frontier 후보로 넣습니다. 이미 방문한 개체를 제외한 뒤 다음 hop으로 갑니다. [필터·라벨·재순위화·다음 frontier](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/trustgraph-flow/trustgraph/retrieval/graph_rag/graph_rag.py#L469-L740)가 핵심입니다.

즉, 그래프 전체를 한꺼번에 프롬프트에 넣는 흐름이 아닙니다. **탐색 → 조건 필터 → 관련성 재평가 → 다음 탐색**을 반복하며 필요한 관계를 모읍니다. 코드상 `max_path_length`, `triple_limit`, `edge_limit`, `max_reranker_input` 같은 값이 탐색과 후보량을 제한합니다. 후보가 상한을 넘으면 재순위화 전에 앞부분으로 자르는 분기도 있으므로, 무제한 탐색이나 전역 최적 검색으로 해석해서는 안 됩니다. [후보 상한과 재순위화 요청](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/trustgraph-flow/trustgraph/retrieval/graph_rag/graph_rag.py#L669-L723)이 근거입니다.

### 3. 관계의 출처를 모으고 답변을 생성합니다

탐색 후에는 선택된 관계의 URI로 원문 문서를 추적합니다. 이어 관계들을 `s`, `p`, `o` 사전으로 바꾸고 출처 문서 정보를 합쳐 `kg-synthesis` 프롬프트의 `knowledge`에 넣습니다. 질문은 `query` 변수로 전달됩니다. 출처 추적 중 예외가 생기면 경고를 남기고 빈 출처 목록으로 계속하는 분기도 있습니다. 따라서 답변이 나왔다는 사실만으로 출처 문서 연결까지 성공했다고 판단할 수는 없습니다. [문서 추적](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/trustgraph-flow/trustgraph/retrieval/graph_rag/graph_rag.py#L1018-L1031), [합성 프롬프트](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/trustgraph-flow/trustgraph/retrieval/graph_rag/graph_rag.py#L1057-L1094)를 함께 확인할 수 있습니다.

검색 서비스는 답변 문자열만 반환하지 않습니다. 비스트리밍 응답에는 토큰 사용량·모델·출처 참조도 포함하고, 스트리밍 경로에서는 조각을 중계한 뒤 세션 종료 응답으로 사용량과 출처를 보냅니다. [응답 분기](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/trustgraph-flow/trustgraph/retrieval/graph_rag/rag.py#L235-L321)를 보면 애플리케이션이 답변과 함께 받을 수 있는 정보가 구체적으로 드러납니다.

또한 질문, 개념 연결, 탐색, 선택된 근거, 답변 합성의 단계별 설명 트리플을 콜백으로 발행합니다. 이 기록의 이름 붙은 그래프는 `urn:graph:retrieval`입니다. 이는 추출 때의 `urn:graph:source`와 역할이 다릅니다. 전자는 이번 질문의 처리 과정, 후자는 원문에서 지식을 만들었던 계보입니다. [설명 콜백](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/trustgraph-flow/trustgraph/retrieval/graph_rag/rag.py#L149-L172), [질문·탐색 단계 기록](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/trustgraph-flow/trustgraph/retrieval/graph_rag/graph_rag.py#L934-L1006)을 통해 두 층을 구별할 수 있습니다.

## 조회 정책: README의 표현을 배포 조건까지 읽기

README는 조회마다 SHACL-AF 정책을 평가한다고 소개합니다. SHACL-AF는 여기서 그래프에 저장한 규칙으로 대상 노드와 판정 결과를 표현하는 데 쓰입니다. 실제 코드에는 일반 트리플 조회와 별도로 `triples-policy` 처리기가 있고, 파일 첫머리에 **flow 설정이 일반 조회 서비스와 이 서비스 중 하나를 선택한다**고 적혀 있습니다. 따라서 레포에 정책 구현이 있다는 사실을 모든 배포에서 자동 강제된다는 뜻으로 옮기면 안 됩니다. [정책 서비스의 연결 조건](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/trustgraph-flow/trustgraph/policy/triples/service.py#L2-L10)을 확인해야 합니다.

정책 서비스가 연결된 경로의 분기는 다음과 같습니다.

| 조건 | 서비스의 처리 |
| --- | --- |
| 로드된 정책이 없음 | 원래 조회를 그대로 중계 |
| 정책은 있는데 `user_context`가 없음 | `policy-enforcement-error` 응답으로 거부 |
| 정책과 `user_context`가 모두 있음 | 백엔드 결과를 배치별로 필터링한 뒤 중계 |

이 표는 [on_message와 _needs_policy](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/trustgraph-flow/trustgraph/policy/triples/service.py#L89-L210)를 문장으로 풀어 쓴 것입니다. 정책 존재 여부는 workspace·collection 기준으로 캐시하며 만료 후 다시 조회합니다. 이 글은 해당 분기와 캐시 키를 확인한 범위이며, 모든 저장소·전송 계층의 격리를 시험했다는 의미는 아닙니다.

필터는 `urn:graph:policy`에서 정책을 읽고, 결과 트리플의 주어와 목적어 중 IRI인 노드를 평가 후보로 모읍니다. 정책은 순서대로 평가하며, 대상 조건이 일치하고 규칙이 판정 결과를 만든 첫 정책의 판정을 사용합니다. README의 Allowed·Filtered·Violation이라는 구분에 더해, 실제 제거 여부는 판정 결과의 `blocks` 값으로 결정됩니다. 실제 결과 제거 함수 `_triple_blocked`는 **주어가 차단된 트리플만 제외**합니다. 목적어 IRI도 평가 후보로 모으지만, 이 함수는 목적어만 차단된 경우에는 해당 트리플을 제외하지 않습니다. 따라서 후보 노드를 평가한다는 사실을 주어와 목적어 모두의 노출이 차단된다는 보장으로 확대해서는 안 됩니다. 정책과 일치하지 않는 노드까지 일괄 거부하는 구조는 아닙니다. [후보 노드·차단 적용](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/trustgraph-flow/trustgraph/policy/policy_filter.py#L235-L325), [정책 순서와 최초 판정](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/trustgraph-flow/trustgraph/policy/policy_filter.py#L721-L779)이 근거입니다.

이 설계에서 배울 점은 관련성 검색과 접근 정책을 별도로 놓았다는 것입니다. 질문과 관련성이 높다는 판단이 곧 열람 허가를 뜻하지 않으며, 정책 통과가 답변의 사실성을 검증하는 것도 아닙니다. 이는 확인한 모듈의 책임 분리를 바탕으로 한 리뷰어의 해석입니다.

## 설치와 사용: 문서에 적힌 시작 경로

README의 Quickstart는 소스 복제보다 설정 생성기로 시작하는 방법을 안내합니다.

```bash
npx @trustgraph/config
```

이 명령은 [동일 커밋의 Quickstart](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/README.md#L102-L114)에 있는 안내를 옮긴 것입니다. README에 따르면 설정 과정은 Docker·Podman용 `docker-compose.yaml` 또는 Kubernetes용 `resources.yaml`을 담은 `deploy.zip`과 `INSTALLATION.md`를 생성합니다. 이 글에서는 명령을 실행하거나 생성 파일을 확인하지 않았습니다.

구성요소가 많기 때문에 사용 관점에서도 ‘추출 모델만 선택하면 끝’이라고 보기는 어렵습니다. 문서 처리, 메시지 브로커, 그래프·벡터 저장소, 프롬프트 서비스와 flow를 함께 정하는 구조입니다. 이 항목들은 [README의 Integrations](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/README.md#L130-L137)와 [처리기 진입점 목록](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/trustgraph-flow/pyproject.toml#L5-L100)에서 확인할 수 있습니다.

외부 에이전트를 붙이는 MCP 서버도 있습니다. 다만 인증을 읽을 때 경계를 주의해야 합니다. `PassthroughTokenVerifier`는 비어 있지 않은 토큰을 받아 보관하고 실제 검증은 게이트웨이에 위임하는 구조입니다. 주석도 유효하지 않은 토큰은 게이트웨이의 첫 인증 프레임에서 실패할 수 있다고 설명합니다. ‘MCP 서버 연결 성공’과 ‘게이트웨이에서 유효한 권한 확인’은 같은 사건이 아닙니다. [MCP 토큰 전달 경계](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/trustgraph-mcp/trustgraph/mcp_server/mcp.py#L57-L88)가 근거입니다.

## 한계와 주의점

첫째, 온톨로지는 이 구현에서 추출 방향과 타입 제약에 쓰입니다. README도 완전한 OWL 추론기가 아니라고 명시합니다. 관계 변환기가 확인하는 domain·range·상위 클래스 조건을 모든 논리 제약의 완전한 검증으로 확대해서는 안 됩니다. [README의 범위 설명](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/README.md#L116-L128)과 [변환기의 검사](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/trustgraph-flow/trustgraph/extract/kg/ontology/triple_converter.py#L125-L179)를 함께 읽으면 그 범위가 분명해집니다.

둘째, 문서 추출과 답변 합성에는 LLM 호출이 남아 있습니다. 형식과 타입 검사, 출처 기록을 갖추었다고 해서 환각이 없어졌다고 증명되지는 않습니다. 이 글은 처리 흐름을 확인했으며 정확도·비용·지연시간의 수치를 새로 제시하지 않습니다. README의 Decision Scoring 지연시간 표기도 이 리뷰에서 측정하거나 검증한 값이 아니므로 성능 근거로 사용하지 않았습니다.

셋째, 운영 조건은 연결한 서비스에 달려 있습니다. 특히 조회 정책은 flow 구성과 정책 데이터·사용자 문맥을 함께 확인해야 합니다. 출처 추적이 실패해도 합성을 계속할 수 있다는 분기 역시 애플리케이션이 답변과 근거의 상태를 따로 관찰해야 하는 이유입니다.

코드와 짧은 발췌의 사용 조건은 [Apache License 2.0](https://github.com/trustgraph-ai/trustgraph/blob/17e5d7423ac080b0162f7242694c520551b9df0c/LICENSE)입니다. 저장소의 저작권 표기는 Copyright 2024–2026 TrustGraph입니다. 상용 이용 가능 여부만으로 모든 의무를 요약하지 말고 배포·변경 시 라이선스와 고지 조건을 확인해야 합니다.

## 정리

TrustGraph의 핵심은 온톨로지를 추출 프롬프트의 어휘로 쓰는 데서 끝나지 않습니다. 추출 결과의 RDF 변환, 관계를 따라가는 검색, 노드 단위 조회 정책, 출처와 질문 처리 기록을 여러 서비스의 연결로 구성합니다. 코드를 읽으면 ‘지식을 만든다’, ‘답에 필요한 근거를 고른다’, ‘사용자에게 보여 줄 범위를 정한다’가 각기 다른 단계라는 점이 드러납니다.

이 분리를 이해하면 README의 기능 목록도 더 구체적으로 읽을 수 있습니다. 어떤 기능이 구현되어 있는지와, 내 배포에서 어느 경로에 연결되어 있는지는 함께 확인해야 합니다.

### 이 글에서 다루지 못한 부분

DocumentRAG의 하이브리드 검색, SPARQL 엔진 전체, 에이전트 오케스트레이터의 각 패턴, 저장소별 구현과 워크스페이스 이동 묶음, Decision Scoring·Cloze Classification은 상세 분석 범위에 넣지 않았습니다. MCP도 인증 전달 경계만 확인했으며 도구 전체를 검수한 것은 아닙니다. 테스트 디렉터리는 존재를 확인했지만 실행하지 않았으므로 테스트 통과나 운영 안정성을 주장하지 않습니다.
