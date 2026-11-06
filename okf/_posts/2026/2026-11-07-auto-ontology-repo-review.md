---
type: "Repo Review"
title: "[Repo Review] NVIDIA Auto Ontology — 기업 메타데이터에서 질의 근거까지 이어지는 의미 계층"
description: "NVIDIA Auto Ontology의 메타데이터 수집·의미 컴파일부터 자연어 SQL 생성·검증·실행과 MCP 연결까지 추적하고 인증·준비 상태·실패 처리의 실제 경계를 분석합니다."
date: "2026-11-07"
tags:
  - "Repo Review"
  - "NVIDIA"
  - "AI Agent"
  - "MCP"
  - "Python"
resource: "https://github.com/NVIDIA/auto-ontology/tree/c447003f72a822301e927196a4ecb5b597c308d5"
generated:
  by: "process:blog-review"
  at: "2026-11-07T06:11:08+09:00"
sources:
  - id: "nvidia/auto-ontology"
    resource: "https://github.com/NVIDIA/auto-ontology/tree/c447003f72a822301e927196a4ecb5b597c308d5"
    title: "Auto Ontology"
status: "stable"
year: "2026"
analyzed_at: "2026-11-07T06:11:08+09:00"
source_id: "nvidia/auto-ontology"
source_revision: "c447003f72a822301e927196a4ecb5b597c308d5"
source_title: "Auto Ontology"
source_type: "repo"
source_url: "https://github.com/NVIDIA/auto-ontology/tree/c447003f72a822301e927196a4ecb5b597c308d5"
visual_sources:
  - path: "/img/reviews/2026/auto-ontology-repo-review/architecture.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/frontend/app/api/chat/completions/route.ts#L48-L87"
    evidence:
      - "https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/frontend/app/api/chat/completions/route.ts#L48-L87"
      - "https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/ingestion_service/ingest.py#L82-L139"
      - "https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/docker-compose.yml#L39-L100"
    caption: "리뷰어 작성, 분석 커밋 기준. 공개 게이트웨이와 내부 질의·수집 서비스의 역할"
  - path: "/img/reviews/2026/auto-ontology-repo-review/compilation.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/ingestion_service/ingest.py#L109-L139"
    evidence:
      - "https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/ingestion_service/ingest.py#L109-L139"
      - "https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/semantic/visit_enter.py#L813-L906"
      - "https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/semantic/compile.py#L64-L105"
    caption: "리뷰어 작성, 분석 커밋 기준. 메타데이터 수집과 의미 컴파일의 분리"
  - path: "/img/reviews/2026/auto-ontology-repo-review/query.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/retrieval/text_to_sql/text_to_sql_graph.py#L465-L606"
    evidence:
      - "https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/retrieval/text_to_sql/text_to_sql_graph.py#L465-L606"
      - "https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/retrieval/text_to_sql/agents/sql_parse_validation.py#L1072-L1099"
      - "https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/retrieval/text_to_sql/main.py#L290-L340"
    caption: "리뷰어 작성, 분석 커밋 기준. 기본 질의 경로와 검증·재작성 조건"
---

## 들어가며

자연어로 SQL을 만드는 것만으로는 “매출”이 어떤 열과 계산식인지, 고객을 어떤 키로 연결해야 하는지 정해지지 않습니다. 같은 단어를 서로 다른 테이블에 연결하면 문법적으로 실행되는 SQL도 다른 답을 낼 수 있습니다. NVIDIA Auto Ontology는 이 문제를 기업 데이터의 **의미 계층**으로 다룹니다. 물리적 스키마 위에 업무 용어와 열의 대응, 계산식, 관계를 저장하고 에이전트가 이 맥락을 검색하도록 합니다. README는 이를 기존 의미 모델을 보완하는 컨텍스트 계층으로 소개합니다. [README의 문제 정의](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/README.md#L7-L17)

이 글은 `NVIDIA/auto-ontology`의 커밋 **`c447003f72a822301e927196a4ecb5b597c308d5`**를 고정해 읽은 정적 분석입니다. 대상 저장소의 설치·빌드·테스트·모델 호출·데이터베이스 질의는 실행하지 않았습니다. 주로 카탈로그 수집, 의미 컴파일, 웹/API/MCP 질의, 검증과 결과 반환 경로를 추적했습니다. 문서의 예시 답변이나 외부 평가 저장소의 결과를 이번 분석에서 재현한 성능으로 사용하지 않습니다.

## Auto Ontology는 무엇인가요

Auto Ontology는 **관계형 데이터 소스의 메타데이터를 업무 용어와 SQL 표현식에 연결하고, 그 맥락으로 자연어 질의를 처리하는 라이브러리이자 웹 애플리케이션**입니다. README가 설명하는 온톨로지의 핵심은 업무 개념인 Term, Term 아래의 검토 가능한 계산식인 SQL attribute, 테이블과 열을 잇는 관계입니다. 여기서 온톨로지는 데이터 분석 에이전트가 사용할 업무 의미와 데이터 연결을 담는 모델로 이해하시면 됩니다. [정의 구성 요소](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/README.md#L196-L218)

| 층 | 담는 내용 | 코드에서 확인한 역할 |
| --- | --- | --- |
| 물리 카탈로그 | DB·스키마·테이블·열·쿼리 정보 | 소스 커넥터로 추출하고 저장합니다. |
| 의미 모델 | Term, ColumnAttribute, SqlAttribute, 관계 | 열을 업무 용어에 배정하고 SQL 생성 문맥을 제공합니다. |
| 질의 실행 | 질문, 검색 후보, SQL, 실행 결과, 단계 기록 | 후보를 검색해 SQL을 만들고 검사·재작성 후 결과를 반환합니다. |

이 구분은 [`catalog/ingest.py`](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/catalog/ingest.py#L28-L56), [`semantic/visit_enter.py`](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/semantic/visit_enter.py#L813-L906), [`text_to_sql_graph.py`](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/retrieval/text_to_sql/text_to_sql_graph.py#L465-L606)의 호출 경로를 요약한 것입니다.

서버 패키지 이름은 `auto-ontology-server`, 버전은 `1.2.0`, Python 범위는 `>=3.12,<3.14`입니다. MCP는 별도 패키지 `auto-ontology-mcp` `1.2.0`이며 Python `>=3.11`을 요구합니다. MCP 실행만을 위해 전체 백엔드 설치를 요구하도록 묶지는 않았습니다. [서버 매니페스트](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/pyproject.toml#L5-L10), [MCP 매니페스트와 진입점](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/mcp/pyproject.toml#L12-L27)

## 아키텍처와 디렉터리 구조

### 공개 게이트웨이와 내부 처리 서비스를 나눕니다

![공개 게이트웨이 아래에 FastAPI 질의 서비스와 수집·컴파일 워커가 있고 Postgres와 소스 DB를 사용하는 구조]({{ '/img/reviews/2026/auto-ontology-repo-review/architecture.svg' | relative_url }})

리뷰어 작성, 분석 커밋 기준. 웹·REST·MCP 요청은 공개 게이트웨이로 들어갑니다. 수집·컴파일은 질의 서비스와 별도 프로세스입니다. [채팅 게이트웨이](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/frontend/app/api/chat/completions/route.ts#L48-L87), [수집 경로](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/ingestion_service/ingest.py#L82-L139), [Compose 서비스](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/docker-compose.yml#L39-L100)

Next.js 프런트엔드는 화면, Better Auth 기반 사용자 식별, 권한 검사, 공개 API 게이트웨이를 맡습니다. FastAPI 백엔드는 채팅·카탈로그·용어 API를 제공하고, 별도의 FastAPI 수집 서비스가 인제스트와 의미 컴파일을 수행합니다. Postgres는 카탈로그·의미 모델·앱 데이터를 저장하며 pgvector가 검색용 벡터를 저장합니다. 기본 포트는 3000, 3001, 3002, 5432이고 MCP는 별도 실행되는 3003 서비스로 설명돼 있습니다. [README 구성표](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/README.md#L262-L274)

같은 Postgres에서도 소유 스키마가 나뉩니다. Compose 설명에서는 Alembic이 `public`의 카탈로그·의미 계층을, Prisma가 `frontend`의 앱 스키마를 관리합니다. 각 서비스 기동에 앞서 별도의 마이그레이션 작업이 연결돼 있습니다. [마이그레이션과 기동 의존성](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/docker-compose.yml#L102-L173)

| 경로 | 책임과 이번에 읽은 지점 |
| --- | --- |
| `frontend/app/api/`, `frontend/auth/` | 공개 API의 사용자 식별·권한 검사·백엔드 전달 |
| `auto_ontology/server/` | FastAPI 라우터와 채팅 워커 관리 |
| `auto_ontology/connectors/` | 소스 DB 연결, SQL 실행, 엔진별 방언 |
| `auto_ontology/catalog/`, `auto_ontology/dal/` | 물리 카탈로그 생성과 Postgres 읽기·쓰기 |
| `auto_ontology/ingestion_service/` | 수집·컴파일 스케줄러와 트리거 |
| `auto_ontology/semantic/` | 용어 생성, 속성 매핑, 관계·계산식 보강, 임베딩 |
| `auto_ontology/retrieval/` | 엔터티 추출, 검색, SQL 생성·검증·실행 |
| `mcp/auto_ontology_mcp/` | 공개 API 위에 구성한 MCP 도구 |

이 표는 파일 트리 전체의 전수 분석이 아니라 아래 경로의 안내입니다. 백엔드 앱 팩터리는 `auto_ontology/server/__main__.py`의 `create_app()`이며 라우터를 `/api` 아래에 등록합니다. [라우터 등록](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/server/__main__.py#L95-L116)

## 작동 원리: 메타데이터가 질의 맥락이 되기까지

### 1. 커넥터가 소스 DB와 내부 저장소를 구분합니다

`CONNECTOR_REGISTRY`에는 PostgreSQL, MySQL, Databricks, DuckDB, Snowflake, ClickHouse, HeavyDB, Kyuubi, SQLite, Trino에 대응하는 클래스가 등록돼 있습니다. `postgres`와 `postgresql`은 같은 클래스입니다. URL 스킴으로 클래스를 선택하고 미등록 엔진은 거절합니다. 내부 저장소가 Postgres라는 사실과 소스 DB가 Postgres여야 한다는 주장은 다릅니다. [등록 목록](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/connectors/registry.py#L18-L56), [선택과 거절](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/connectors/registry.py#L132-L179)

이 목록은 구현된 어댑터의 범위이며 열 가지 엔진의 연결 성공·모든 SQL 문법 호환성을 이번에 확인한 것은 아닙니다. 생성 함수는 Databricks·Snowflake·Kyuubi·Trino에 스키마 목록을 전달하고, 테이블 정규식 필터는 공통 추출 경로에서 적용하도록 인스턴스에 실어 보냅니다. [필터 전달 조건](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/connectors/registry.py#L137-L178)

### 2. 수집은 카탈로그 저장과 벡터 쓰기를 이어 붙입니다

`run_ingest(connector)`는 `ingest_catalog()`로 테이블·열 데이터를 얻습니다. 안쪽에서는 커넥터로 추출한 메타데이터를 `populate_tabular_data()`로 저장하고 저장 ID를 포함하는 테이블·열 DataFrame을 반환합니다. 이어 `CatalogEmbeddingRowsOp`가 검색용 텍스트 행을 만들고 `batch_embed_chunks()`가 외부 임베딩 모델을 호출하는 경계가 됩니다. 결과를 `to_vdb_records()`로 바꿔 pgvector에 씁니다. [카탈로그 추출·저장](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/catalog/ingest.py#L28-L56), [인제스트 연결](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/ingestion_service/ingest.py#L103-L139)

인덱스는 수집 시작 직후 지우지 않습니다. 실제 임베딩이 있는 첫 청크가 도착할 때 `reset=True`로 저장소를 엽니다. 첫 임베딩부터 실패했을 때 이전 검색 데이터를 남기려는 구조입니다. 다만 청크별 쓰기이므로 이를 전체 교체의 원자성 보장으로 읽어서는 안 됩니다. 카탈로그 저장과 모든 벡터 쓰기를 묶은 단일 트랜잭션은 이 경로에서 확인되지 않습니다. [첫 유효 청크의 초기화](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/ingestion_service/ingest.py#L124-L149)

![메타데이터 추출·카탈로그 저장 뒤 별도 의미 컴파일에서 용어·속성·관계·계산식을 구성하는 순서]({{ '/img/reviews/2026/auto-ontology-repo-review/compilation.svg' | relative_url }})

리뷰어 작성, 분석 커밋 기준. 인제스트와 의미 컴파일은 별도 작업입니다. 컴파일 중 용어별 임베딩 쓰기가 일어나고 관계·계산식 보강이 뒤따릅니다. [인제스트](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/ingestion_service/ingest.py#L109-L139), [용어 처리](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/semantic/visit_enter.py#L813-L906), [후속 단계](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/semantic/compile.py#L64-L105)

### 3. 의미 컴파일은 LLM 추출과 규칙 처리를 섞습니다

`run_semantic_compilation()`은 동시 LLM 호출 상한을 적용하고 도메인 요약과 의미 임베더를 준비합니다. `compile_semantic_layer()` 뒤에는 의미 외래 키 연결, 쿼리 이력에서의 SQL attribute 제안, 브리지 테이블 계산식 구성이 이어집니다. 취소됐다면 테이블 처리 후 세 후속 단계를 건너뜁니다. [컴파일 조합과 취소](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/semantic/compile.py#L33-L105)

테이블별 처리는 다음 순서입니다.

1. 테이블 문맥과 열을 읽고, 가능하면 소스에서 열 값을 샘플링·프로파일링합니다. 샘플링 오류는 기록하고 샘플 없이 계속합니다.
2. 선언된 외래 키와 LLM이 제안한 외래 키 열을 모아 비외래 키 열의 속성 후보를 만듭니다.
3. LLM이 하나 이상의 Term과 열 배정을 제안합니다. `extract_term()`은 테이블 이름·설명·후보 열과 일부 도메인 요약을 구조화 출력 모델에 전달합니다. 반환값이 없으면 fallback을 사용합니다.
4. 배정이 남은 용어를 저장하고 열 속성을 연결합니다. 저장한 용어·속성을 다시 읽어 인라인으로 임베딩합니다. 이 임베딩의 실패는 경고를 남기고 계속합니다.

근거는 [샘플링 실패 처리](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/semantic/visit_enter.py#L780-L811), [외래 키·속성·용어 생성](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/semantic/visit_enter.py#L813-L864), [저장과 임베딩](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/semantic/visit_enter.py#L866-L906), [실제 LLM 호출](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/semantic/term_extractor.py#L220-L260)입니다. 이 모델은 메타데이터만의 순수 함수가 아니며 실제 값 샘플과 원격 모델 응답이 개입합니다.

결정성도 범위를 나눠야 합니다. 파이프라인은 데이터베이스·스키마·이름 등을 정렬 키로 쓰고 LLM 작업은 병렬로 실행하되 용어 저장 차례를 `_OrderedCommitSlot`으로 맞춥니다. 같은 이름을 제안하는 테이블이 경쟁할 때, 접두어 없이 그 이름을 누가 차지할지 안정시키는 장치입니다. LLM 출력이나 모든 답변이 매번 동일하다는 의미는 아닙니다. [정렬 키와 설계](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/semantic/pipeline.py#L116-L151), [저장 슬롯·병렬 실행](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/semantic/pipeline.py#L162-L224)

또한 `_process()`는 테이블 처리 예외를 기록하고 `None`을 반환합니다. 상위 호출의 정상 반환만으로 모든 테이블의 용어와 임베딩이 완성됐다고 판단할 수 없습니다. [테이블별 예외 처리](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/semantic/pipeline.py#L183-L224)

### 4. enabled, calculated, ready를 구분합니다

설정의 `semantic_compilation_enabled`는 **앞으로 컴파일을 실행할지**를 제어합니다. 프런트엔드 PUT은 `semanticCompilation: manage` 권한을 검사해 값을 저장하고, 켤 때 백엔드에 트리거를 보냅니다. 네트워크 실패를 삼키므로 설정 저장 자체가 즉시 컴파일 성공을 뜻하지는 않습니다. 워커는 실행마다 플래그를 다시 읽고 첫 인제스트 패스가 끝나기를 기다린 뒤 컴파일합니다. [설정 저장·트리거](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/frontend/app/api/configurations/semantic-compilation/route.ts#L22-L55), [스케줄러 게이트](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/ingestion_service/semantic_scheduler.py#L132-L160)

채팅의 시작 조건은 다음 원문처럼 **의미 계층에서 생성한 Term이 하나라도 있는가**입니다.

```python
def semantic_layer_calculated() -> bool:
    """Has the semantic layer been built at all?"""
    return bool(
        store().query_read(
            select(s.term.c.id).where(s.term.c.source == SEMANTIC_SOURCE).limit(1)
        )
    )
```

출처: [`dal/terms.py` 286–292행 원문](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/dal/terms.py#L286-L292).

`chat_completions()`는 거짓이면 HTTP 409를 반환합니다. 전체 DB의 컴파일 완료, 모든 용어의 인증, 현재 enabled 플래그를 이 자리에서 요구하지 않습니다. 상태 API에는 `calculated`와 별도로 `running`, `last_success_at`, `last_failure_at`이 있습니다. [채팅 진입 검사](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/server/chat/router.py#L555-L575), [상태 API](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/server/semantic_compilation/router.py#L58-L76)

MCP의 `check_readiness`는 컴파일 상태, 설정된 연결 수, 인제스트된 DB 목록을 합칩니다. 연결 수가 양수인지는 실제 DB에 접속하는 ping 검사가 아닙니다. 연결 목록에 대한 403은 `unverified`로 남기고 그것만으로 전체 ready를 거짓으로 만들지 않습니다. ready는 관측 가능한 설정·카탈로그 상태와 함께 읽어야 하며 실제 SQL 실행 성공을 인증하는 플래그가 아닙니다. [readiness 판정](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/mcp/auto_ontology_mcp/readiness.py#L145-L240)

## 작동 원리: 질문에서 SQL과 답변으로

### 1. 공개 API에서 사용자와 권한을 검사합니다

`resolveUser()`는 세션 쿠키, Auto Ontology API 토큰, 자체 OAuth 토큰, 검증된 SSO 토큰 순으로 사용자를 찾습니다. `withPermission()`은 사용자가 없으면 401, 권한이 없으면 403으로 중단합니다. 채팅 POST에는 `chat: use`, `conversation_id`가 있으면 추가로 `conversation: write`가 필요합니다. [사용자 식별](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/frontend/auth/resolve-user.ts#L37-L74), [권한 래퍼](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/frontend/auth/with-auth.ts#L51-L65), [채팅 권한](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/frontend/app/api/chat/completions/route.ts#L48-L56)

사용자 ID는 게이트웨이가 내부 헤더로 구성해 FastAPI에 전달합니다. 백엔드는 `x-auto-ontology-user-id`를 독립 인증하지 않고 신뢰하며 대화를 저장하지 않는 직접 요청은 이 헤더를 생략할 수도 있습니다. 즉 이번에 추적한 RBAC의 주된 검사 위치는 공개 프런트엔드 경로입니다. [헤더 구성](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/frontend/app/api/chat/completions/route.ts#L67-L87), [백엔드 신뢰 경계](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/server/identity.py#L20-L36)

### 2. 준비한 워커에 검색기·커넥터·질문 문맥을 전달합니다

백엔드의 subprocess 워커는 데이터·의미 검색기와 커넥터를 미리 준비합니다. 요청을 받으면 후속 질문을 처리용 질문으로 정리하고 원래 질문, evidence, 검색기, 커넥터, 약어와 사용자 프롬프트를 `stream_agent_response()`에 넘깁니다. SSO subject token이 있으면 사용자별 Databricks 인증 경로에 맞춘 커넥터를 사용합니다. [워커 준비](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/server/chat/worker.py#L82-L111), [요청별 구성](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/server/chat/worker.py#L159-L199)

여러 소스가 등록돼 있어도 SQL 하나가 모든 엔진을 연합 질의하는 구조는 아닙니다. 관련 테이블은 한 DB에 속해야 하며 여러 DB가 섞였거나 여러 커넥터 중 대상을 알 수 없으면 오류를 냅니다. API의 `target_db`도 설정된 DB 이름과 대조합니다. [DB 식별과 실행 라우팅](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/retrieval/text_to_sql/connector_routing.py#L21-L108)

### 3. 의미 검색 뒤 물리 스키마와 함께 SQL을 생성합니다

기본 그래프는 질문 의도 분류 → 엔터티 추출 → 후보 검색 → 후보 준비 → SQL 생성으로 이어집니다. 정보 설명형 질문은 information 경로로 끝날 수 있고, evidence는 정제 단계를 거칠 수 있습니다. [그래프 분기](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/retrieval/text_to_sql/text_to_sql_graph.py#L465-L532)

후보 검색은 엔터티 텍스트를 라벨별 의미 인덱스에 질의합니다. 결과의 ID·점수·검색 엔터티를 유지하고 같은 ID는 가장 좋은 점수 기준으로 합칩니다. 후보 DB를 고를 때는 ColumnAttribute로 덮인 서로 다른 엔터티 수를 우선하고, 후보 수·누적 거리·DB 이름을 뒤이어 씁니다. 이름이 같은 열을 서로 다른 DB에서 무작정 섞지 않게 문맥을 좁히는 과정입니다. [검색·중복 제거](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/retrieval/text_to_sql/agents/candidates_retrieval.py#L60-L120), [후보 DB 선택](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/retrieval/text_to_sql/agents/candidates_retrieval.py#L135-L178)

생성기는 주요 속성, 조인 경로, 테이블, SQL attribute, 사용자 분석식, 동의어, evidence를 모으고 소유 커넥터로 SQL 방언을 정합니다. 모델은 `reasoning_llm`을 우선합니다. 저장된 SQL을 그대로 꺼내기만 하는 방식이 아니라 정의와 관계를 문맥으로 조립해 새로운 SQL을 작성합니다. [생성 입력과 모델 선택](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/retrieval/text_to_sql/agents/sql_from_semantic.py#L128-L172)

`check_answerable`의 coverage는 정답 확률이 아닙니다. 구현은 거리로 후보를 걸러낸 뒤 **ColumnAttribute로 덮인 엔터티 수 / 추출한 전체 엔터티 수**를 계산합니다. SQL attribute와 사용자 분석식은 응답 후보에 더해지지만 비율 계산은 열 속성 히트에 기반합니다. 1.0이어도 올바른 조인·집계·시간 조건까지 증명하지 않습니다. [비율 계산](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/retrieval/entity_coverage/agents/coverage.py#L60-L66), [필터와 응답](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/retrieval/entity_coverage/agents/coverage.py#L172-L209)

### 4. 정적 검사, LLM 의도 검사, 선택적 DB 검사를 구분합니다

![기본 계산 질의에서 SQL 생성·정적 의도 검사·선택적 사전 검사·DB 실행과 재작성·결과 반환으로 이어지는 흐름]({{ '/img/reviews/2026/auto-ontology-repo-review/query.svg' | relative_url }})

리뷰어 작성, 분석 커밋 기준. 기본 계산형 경로를 단순화했으며 반복·완화·최종 fallback 조건은 본문에 구분했습니다. [실제 그래프](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/retrieval/text_to_sql/text_to_sql_graph.py#L524-L606), [의도 검사 실패 처리](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/retrieval/text_to_sql/agents/sql_parse_validation.py#L1072-L1099), [최종 fallback](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/retrieval/text_to_sql/main.py#L304-L340)

검증기는 카탈로그와 SQL 파서를 연결해 사용 테이블·열 ID를 얻습니다. 인식 가능한 테이블이 없으면 실패입니다. 정적 검사를 통과하면 질문·evidence·사용 스키마·조인 문맥을 LLM 의도 검사에 넘깁니다. 파싱 성공과 질문에 대한 의미적 정답 여부는 서로 다른 검사입니다. [파싱과 카탈로그 매핑](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/retrieval/text_to_sql/agents/sql_parse_validation.py#L934-L983), [의도 검사 프롬프트](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/retrieval/text_to_sql/agents/sql_parse_validation.py#L1040-L1075)

다음은 의도 검사 단계의 실제 예외 처리입니다.

```python
        try:
            validation_result = invoke_with_structured_output(
                state["llm"], messages, IntentValidationModel
            )
        except Exception as error:
            self.logger.error("Intent validation LLM call failed: %s", error)
            return {"decision": "valid_sql", "path_state": path_state}
```

출처: [`sql_parse_validation.py` 1072–1078행 원문](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/retrieval/text_to_sql/agents/sql_parse_validation.py#L1072-L1078).

의도 검사 호출이 예외를 내면 선행 정적 검사를 통과한 SQL을 계속 허용합니다. 구조화 결과가 `None`인 경우도 통과합니다. 의미 검사 실패를 허용하는 동작이며, 선행 정적 검사까지 생략한다는 뜻은 아닙니다. 모든 실행 SQL이 LLM 의도 검증에 성공했다는 보장은 여기서 성립하지 않습니다. [None 처리](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/retrieval/text_to_sql/agents/sql_parse_validation.py#L1090-L1099)

리터럴 값·조인 경로·JSONB 키 경로의 실제 데이터 사전 검사인 `precheck_combined`는 관련 `DB_PROBE_*` 플래그가 켜졌을 때만 그래프에 생깁니다. 별도 `validate_sql_values` 단계도 요청 상태가 참일 때 연결되며 초기 기본값은 거짓입니다. README의 “filter values를 검사한다”는 설명을 모든 기본 요청의 동일한 절차로 읽기는 어렵습니다. [사전 검사 조건](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/retrieval/text_to_sql/text_to_sql_graph.py#L379-L402), [값 검사 경로](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/retrieval/text_to_sql/text_to_sql_graph.py#L225-L239), [초기 상태](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/retrieval/text_to_sql/main.py#L221-L232)

반복에는 두 정책이 있습니다. 일반 검증·실행 오류 라우팅은 재작성 기록이 7개에 도달하면 구성 불가 경로로 보냅니다. 반면 soft check는 실패 기록이 5개를 초과하면 그 검사로 더 이상 차단하지 않습니다. 안쪽 루프가 구성 불가로 끝나 SQL을 반환하지 못하면 바깥 실행기는 최대 두 번의 전체 파이프라인 시도를 허용합니다. 마지막에도 의도 검사에서 거절된 정적 유효 SQL이 남아 있으면 `sql_code`에 넣는 fallback이 있습니다. 이 함수는 **그 SQL을 실행하지 않고 응답 필드를 채웁니다**. SQL 문자열이 보인다는 사실만으로 그 SQL이 성공적으로 실행됐다고 추정해서는 안 됩니다. [7회 라우팅](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/retrieval/text_to_sql/text_to_sql_graph.py#L81-L120), [soft check 완화](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/retrieval/text_to_sql/text_to_sql_graph.py#L131-L158), [전체 재시도·fallback](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/retrieval/text_to_sql/main.py#L290-L340)

### 5. 결과와 provenance의 실제 형태를 확인합니다

실행 노드는 관련 테이블의 커넥터로 `execute_chat_sql()`을 호출합니다. 연결 장애 등 인프라 오류는 재작성으로 고치려 하지 않고 구성 불가 설명으로 종료하고, 다른 실행 오류는 재작성으로 돌립니다. 시간 제한은 `supports_statement_timeout`을 선언한 커넥터에 전달하며 그렇지 않은 주입 커넥터는 일반 `execute(sql)`로 호출합니다. PostgreSQL 구현은 트랜잭션 안에서 `statement_timeout`을 설정합니다. [실행·오류 분류](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/retrieval/text_to_sql/agents/sql_execution.py#L227-L304), [실행 래퍼](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/retrieval/text_to_sql/chat_sql.py#L59-L86), [PostgreSQL 제한](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/connectors/postgres.py#L90-L121)

정상 계산 응답에는 설명, `sql_code`, `sql_columns`, `sql_response_from_db`가 조립됩니다. 스트림은 단계 기록을 `step`, 실행 직전 SQL을 `sql`, 최종 답변을 `result`로 내보내며 단계 텍스트를 `thoughts`로 붙입니다. 이것이 추적한 provenance의 구체적인 형태입니다. 원천 테이블에서 최종 숫자까지의 완전한 계보 증명서나 모든 정의의 인증 증명과 같은 출력은 아닙니다. [응답 필드](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/retrieval/text_to_sql/agents/response.py#L54-L93), [단계·SQL·결과 이벤트](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/retrieval/text_to_sql/main.py#L472-L535)

인증 기능 자체는 있습니다. Term 이름·설명과 연결된 열·SQL 속성의 인증 상태를 합쳐 `certified`, `partial`, `pending`을 계산합니다. 그러나 채팅 진입 검사는 인증 완료를 요구하지 않고, SQL attribute 후보 확장 쿼리도 ID·SQL·Term의 존재를 조건으로 삼습니다. 이번 경로만으로 “인증된 정의만 사용하는 강제 실행 정책”을 확인했다고 말할 수는 없습니다. [인증 집계](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/dal/terms.py#L156-L232), [후보 확장 조건](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/dal/candidates.py#L177-L205)

## 모델 역할과 MCP·CLI·API의 연결

### 모델 설정은 빠진 필드마다 상속됩니다

역할은 `REASONING`, `NON_REASONING`, `EMBED`, `RERANK`이며 각각 ENDPOINT·API_KEY·MODEL을 갖습니다. 실제 해결 순서는 다음 두 줄입니다.

```python
    key = f"{prefix}_{field}"
    return os.environ.get(key, "") or _default(field) or _builtin_default(prefix, key)
```

출처: [`model_config.py` 99–100행 원문](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/utils/model_config.py#L92-L100).

`_default()`는 `DEFAULT_MODELS_<FIELD>` 다음 legacy 변수 `NVIDIA_API_KEY`, `BASE_URL`, `MODEL_NAME`을 확인합니다. 마지막 내장값은 해당 역할 API 키의 `sk-`·`nvapi-` 접두어로 선택하고, 알 수 없거나 없는 키는 `sk-` 묶음으로 갑니다. 역할 전체가 아니라 **필드 단위**의 상속이므로, 공통 채팅 모델을 설정하고 EMBED_MODEL을 비우면 임베딩 역할도 그 모델명을 우선 사용합니다. RERANK도 같은 규칙입니다. `.env.example`이 임베딩 모델을 별도 명시하는 이유입니다. [fallback 구현](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/utils/model_config.py#L57-L100), [환경 설정](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/.env.example#L28-L56)

모델 호출 경계에는 키뿐 아니라 전송 내용도 있습니다. 의미 임베딩 텍스트에는 Term 설명과 열 속성의 샘플 값이 들어가고, SQL 생성 프롬프트에는 질문·스키마·관련 쿼리·계산식이 포함됩니다. PII 서비스에서 확인한 작업은 분류 결과에 따라 카탈로그 열에 태그를 붙이고 처리 여부를 저장하는 것입니다. 이 태깅을 모델 전송 직전의 값 마스킹이나 DLP 보장으로 해석할 근거는 이번 경로에서 확인하지 못했습니다. [임베딩 텍스트 구성](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/semantic/embed.py#L206-L250), [생성 프롬프트 구성](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/retrieval/text_to_sql/agents/sql_from_semantic.py#L280-L335), [PII 태그 저장](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/pii_detection/service.py#L82-L128)

같은 SHA 안의 기본값 설명에도 차이가 있습니다. README 앞부분은 임베딩 `nemotron-3-embed-1b`, reranker `llama-nemotron-rerank-vl-1b-v2`를 소개합니다. 반면 `.env.example`과 `nvapi-` 내장값은 `nemotron-3.5-embed-1b`, `nemotron-3.5-rerank-8b`이고 README 뒤쪽 표도 이 값입니다. 설정 재현에는 소개 문장뿐 아니라 실제 환경 설정과 resolver를 대조해야 합니다. [README 앞부분](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/README.md#L55-L67), [뒤쪽 모델 표](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/README.md#L405-L422), [키별 내장값](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/utils/model_config.py#L29-L54)

### MCP는 공개 API 위의 어댑터입니다

MCP는 FastMCP `from_openapi()`로 선별된 REST 작업을 도구로 만들고 `ask_question`, `check_readiness`를 직접 등록합니다. 용어 검색·열·계산식 조회, 답변 가능성 확인, 질문 실행으로 표면을 좁혔으며 별도 SQL 생성 엔진을 구현하지는 않습니다. [도구 목록](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/mcp/auto_ontology_mcp/tools.py#L53-L101), [서버 조립](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/mcp/auto_ontology_mcp/server.py#L193-L213)

`CallerAuth`는 요청자의 로그인 액세스 토큰을 얻고 기존 `x-api-key`와 Authorization을 제거한 뒤 Bearer를 설정합니다. 서버 전체가 하나의 관리자 키를 공유하는 방식과 구분됩니다. 해당 토큰의 요청은 공개 API의 게이트웨이 권한 검사로 이어집니다. [호출자 인증 전달](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/mcp/auto_ontology_mcp/server.py#L140-L180)

`ask_question`은 `/api/chat/completions`에 POST하고 SSE를 읽습니다. step은 MCP 진행 상황으로, result는 `answer`, `sql`, `rows`, `row_count`, `truncated`, `reasoning`으로 바꿉니다. rows는 최대 100개로 자릅니다. row_count는 **백엔드 응답에서 파싱한 행 수**이며 소스 DB 전체를 별도 COUNT한 결과는 아닙니다. [응답 모델·절단](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/mcp/auto_ontology_mcp/chat.py#L40-L102), [스트리밍 연결](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/mcp/auto_ontology_mcp/chat.py#L188-L246)

README는 MCP·CLI·API를 모두 언급하지만 서버 루트 매니페스트에는 범용 질의 CLI script 등록이 없습니다. 확인한 사용자 경로는 `curl` REST 호출, setup·management·query 문서, MCP 실행 명령입니다. 별도 패키지의 콘솔 진입점 `auto-ontology-mcp`는 MCP 서버를 시작합니다. 이 글에서는 독립적인 온톨로지 질의 CLI를 가정하지 않습니다. [README 접근 방법](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/README.md#L325-L348), [서버 매니페스트](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/pyproject.toml#L5-L83), [MCP script](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/mcp/pyproject.toml#L26-L27)

## 설치와 사용: 같은 커밋 README의 명령

다음은 **실행하지 않은 README 발췌**입니다. Docker Compose v2, uv, NVIDIA API 키를 준비하고 `.env`에 모델 키·AUTH_SECRET·DB·관리자 비밀번호 등을 넣도록 합니다. 초기 구성은 별도의 평가 저장소에서 Wide World Importers 시드 스크립트를 가져오는 단계도 포함합니다. 이 글은 외부 평가 저장소의 코드·리비전·결과를 함께 분석하지 않았습니다. [필수 도구·환경 변수·시드 단계](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/README.md#L88-L139)

```bash
   git clone https://github.com/NVIDIA/auto-ontology.git && cd auto-ontology
   cp .env.example .env
```

출처: [README 98–99행 원문](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/README.md#L95-L100). 선행 들여쓰기도 원문대로 두었습니다. 이 clone은 기본 브랜치를 받으므로 분석 SHA를 자동 재현하지 않습니다.

스택 기동 명령은 다음과 같습니다. 전체 quickstart에는 그 전에 Postgres와 샘플 DB를 준비하는 별도 단계가 있어 아래 한 줄만으로 초기 구성이 끝난다는 뜻은 아닙니다.

```bash
   docker compose up -d --build
```

출처: [README 130–139행](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/README.md#L130-L139). 이후 웹 로그인과 Settings → Semantic Compilation 활성화·상태 확인을 안내합니다.

MCP는 공개 웹 API 주소를 지정합니다.

```bash
AUTO_ONTOLOGY_API_URL=http://localhost:3000 \
  uvx --from "git+https://github.com/NVIDIA/auto-ontology.git#subdirectory=mcp" auto-ontology-mcp
```

출처: [README 291–296행 원문](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/README.md#L291-L296). 이 설치 URL 역시 버전 고정이 없어 실행 시점의 기본 브랜치를 따릅니다.

REST는 웹 앱에서 발급한 API 토큰을 `x-api-key`로 전달하고 SSE를 읽습니다.

```bash
curl -N http://localhost:3000/api/chat/completions \
  -H "x-api-key: $AUTO_ONTOLOGY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"question": "How many orders shipped last week?"}'
```

출처: [README 343–348행 원문](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/README.md#L343-L348). 성공 응답이나 수치를 새로 만들어 제시하지 않습니다.

## 한계와 운영 경계

첫째, **내부망 전제와 Compose 포트 설정이 다릅니다.** README는 3001·3002를 private network에 두라고 하고 ingestion의 ingest·delete·reset·compile에 자체 인증이 없다고 밝힙니다. 그런데 이 SHA의 Compose는 `3001:3001`, `3002:3002`를 호스트에 매핑합니다. 실제 외부 접근 가능성은 호스트·방화벽에도 달려 있지만 Compose가 내부망 격리를 만들어 주지는 않습니다. 공개 게이트웨이의 권한 검사와 내부 서비스 접근 제한은 별도 배포 조건입니다. [README 전제](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/README.md#L271-L274), [백엔드 포트](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/docker-compose.yml#L39-L54), [수집 포트](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/docker-compose.yml#L67-L76), [신뢰 헤더](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/server/identity.py#L20-L36)

둘째, **검사 장치와 정확성 보장은 구별해야 합니다.** 인증 메타데이터, 파싱, 의도 검사, 선택적 실제 데이터 검사, 재작성, 단계 기록은 각각 의미가 있습니다. 그러나 의도 검사 실패 허용, soft check 완화, 실행 없이 SQL을 반환하는 fallback도 있습니다. README의 “certified definitions”, “provenance with every answer”는 이 제어 흐름과 출력 필드 범위에서 읽어야 합니다. [README 표현](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/README.md#L13-L17), [의도 검사 예외](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/retrieval/text_to_sql/agents/sql_parse_validation.py#L1072-L1099), [fallback](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/retrieval/text_to_sql/main.py#L304-L340)

셋째, **컴파일과 검색의 실패는 서로 다른 상태를 남길 수 있습니다.** Term 저장 뒤 임베딩 실패는 경고로 처리되고 테이블별 예외는 상위로 전파되지 않을 수 있습니다. 채팅 calculated는 Term 하나의 존재를 확인합니다. 따라서 단일 ready 문구뿐 아니라 실행 이력·실패 로그·검색 상태를 함께 보아야 한다는 것이 리뷰어의 해석입니다. 장애 주입과 복구는 시험하지 않았습니다. [임베딩 실패](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/semantic/visit_enter.py#L891-L906), [테이블 예외](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/semantic/pipeline.py#L205-L224), [calculated](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/dal/terms.py#L286-L292)

넷째, **예측은 기본 SQL 경로와 구분해야 합니다.** README는 `KUMO_RFM_API_KEY`와 hosted service를 설명하지만 그래프 생성 조건은 `KUMO_RFM_API_URL`의 존재입니다. 함수 설명은 `kumo-relational`을 제공하는 Universal TFM NIM을 요구하고 키는 선택적 게이트웨이 자격 증명이라고 적습니다. 이 차이는 확인했으나 예측 엔진과 전송 데이터 전체는 분석하지 않았습니다. [README 예측](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/README.md#L425-L430), [실제 조건](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/auto_ontology/retrieval/text_to_sql/text_to_sql_graph.py#L183-L196)

LICENSE는 Apache License 2.0을 담고 있으며 README는 외부 구성 요소를 `THIRD_PARTY_NOTICES.md`로 안내합니다. 외부 기여를 현재 받지 않는다는 문구도 있습니다. 이 커밋의 프로젝트 표기를 확인한 것이며 연결하는 모델·서비스·번들 구성 요소의 사용 조건 전체를 검토한 결과는 아닙니다. [LICENSE](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/LICENSE#L1-L12), [배포·기여 안내](https://github.com/NVIDIA/auto-ontology/blob/c447003f72a822301e927196a4ecb5b597c308d5/README.md#L24-L28)

## 결론

Auto Ontology에서 배울 핵심은 자연어 SQL 앞에 업무 의미를 저장하고 검색하는 단계를 둔다는 점입니다. 카탈로그의 물리 정보와 Term·열 속성·SQL 계산식을 연결하고 질의의 조인·계산 문맥으로 사용합니다. 별도 컴파일 워커와 공개 게이트웨이, MCP 어댑터는 이 의미 계층을 여러 이용 경로에 제공합니다.

코드가 보여 주는 신뢰성의 범위는 세밀합니다. 저장 순서의 결정성과 LLM 출력의 결정성, 컴파일 플래그와 전체 준비 완료, 응답 SQL과 실행 SQL은 각각 다릅니다. 실패 분기와 출력 필드까지 함께 읽으면 의미 계층이 제공하는 재사용 가능한 맥락과 운영에서 확인할 조건을 구분할 수 있습니다.

### 이 글에서 다루지 못한 부분

Kumo 예측 엔진과 번들 wheel 내부, interactive clarification 전체, PII 탐지·전파, Vault 저장, 모든 SSO·OAuth 보안 속성, Ossie import/export, 사용자·그룹·zone 관리 전체, DB 드라이버 내부와 모든 SQL 방언, Helm 배포 정책은 심층 분석하지 않았습니다. UI의 모든 화면, 테스트 통과 여부, 외부 평가 저장소의 정확도·지연시간·비용도 확인하지 않았습니다. 판단은 고정 SHA에서 추적한 수집·컴파일·기본 계산형 질의·공개 API·MCP 경로에 한정됩니다.
