---
type: "Repo Review"
title: "[Repo Review] Open Ontologies — 온톨로지 변경 계획과 검증 가능한 증거의 경계"
description: "Open Ontologies의 변경 계획부터 적용·복구와 추론 증거 검사를 추적하고, exactMatch 검사와 호출자 승인 정책의 보장 범위를 코드로 분석합니다."
date: "2026-11-01"
tags:
  - "Repo Review"
  - "AI Agent"
  - "MCP"
  - "Tools"
resource: "https://github.com/fabio-rovai/open-ontologies/tree/cefe5997d04553ac495873e8aa1046c1d6b85f7d"
generated:
  by: "process:blog-review"
  at: "2026-11-01T06:03:15+09:00"
sources:
  - id: "fabio-rovai/open-ontologies"
    resource: "https://github.com/fabio-rovai/open-ontologies/tree/cefe5997d04553ac495873e8aa1046c1d6b85f7d"
    title: "Open Ontologies"
    last_modified: "2026-10-30T23:22:21+01:00"
status: "stable"
year: "2026"
analyzed_at: "2026-11-01T06:03:15+09:00"
source_id: "fabio-rovai/open-ontologies"
source_revision: "cefe5997d04553ac495873e8aa1046c1d6b85f7d"
source_title: "Open Ontologies"
source_type: "repo"
source_url: "https://github.com/fabio-rovai/open-ontologies/tree/cefe5997d04553ac495873e8aa1046c1d6b85f7d"
visual_sources:
  - path: "/img/reviews/2026/open-ontologies-review/architecture.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/server.rs#L2549-L2632"
    caption: "리뷰어 작성, 분석 커밋 기준. CLI·MCP 진입점과 그래프·상태 DB 및 독립 검사기 경계."
  - path: "/img/reviews/2026/open-ontologies-review/lifecycle.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/plan.rs#L187-L232"
    caption: "리뷰어 작성, 분석 커밋 기준. 진단 보고와 호출자의 승인 판단, monitor 검사 및 실제 변경을 구분합니다."
  - path: "/img/reviews/2026/open-ontologies-review/evidence.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/projection_entailment.rs#L791-L867"
    caption: "리뷰어 작성, 분석 커밋 기준. 증거 생성과 검사기 실행을 나누고 파일 밖 업무 상태를 신뢰 경계로 표시합니다."
---

## 들어가며: 한 줄을 바꾸면 의미도 한 줄만 바뀔까요?

온톨로지에서 속성의 주체가 어떤 종류에 속하는지 지정하는 한 줄은, 이미 그 속성을 쓰는 여러 개체의 분류를 바꿀 수 있습니다. 파일의 변경량과 논리적으로 달라지는 결과의 양이 다른 것입니다. Open Ontologies는 이런 변경을 적용하기 전에 살펴보고, 추론 결과에는 다시 검사할 수 있는 증거 파일을 남기려는 도구입니다. README는 이를 온톨로지를 위한 Terraform에 비유합니다. [README의 문제 제기와 비유](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/README.md#L88-L126)

이 글은 **`cefe5997d04553ac495873e8aa1046c1d6b85f7d` 커밋**을 기준으로, Rust 진입점과 변경 관리·추론·교차표 검증 코드를 읽은 정적 리뷰입니다. 매니페스트의 버전은 2.1.0입니다. 의존성을 설치하거나 프로그램·테스트·Lean 증명을 실행하지 않았으며, README의 실행 시간과 사례 수치를 재현한 결과로 제시하지 않습니다. 핵심은 기능 개수보다 **무엇을 입력하고, 무엇을 검사하며, 어떤 결과까지 믿을 수 있는가**입니다. [분석 커밋](https://github.com/fabio-rovai/open-ontologies/tree/cefe5997d04553ac495873e8aa1046c1d6b85f7d), [매니페스트](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/Cargo.toml#L1-L12)

## Open Ontologies와 기본 용어

Open Ontologies는 RDF·OWL 데이터를 저장하고 질의·검증·추론하며, 변경 계획과 적용을 CLI 및 MCP 도구로 제공하는 Rust 엔진입니다. RDF는 정보를 **주어–술어–목적어의 삼중항(triple)**으로 표현하는 방식입니다. 온톨로지는 여기에 등장하는 종류와 관계, 그 관계가 따라야 할 규칙을 정의합니다. 지식 그래프는 이런 정의와 실제 개체에 대한 사실을 연결한 데이터로 이해하시면 됩니다. 이 프로젝트에서는 Oxigraph가 그래프와 SPARQL 질의를 담당하고, SQLite가 버전·계획·감사 기록 등 운영 상태를 보관합니다. [의존성](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/Cargo.toml#L33-L49), [그래프 저장소](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/graph.rs#L184-L235), [상태 테이블](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/state.rs#L6-L62)

README의 커피 예제에는 `Espresso`가 `Coffee`의 하위 종류이고, `Coffee`가 `Drink`의 하위 종류이며, `myCup`이 `Espresso`라는 사실이 들어 있습니다. 추론기는 이 연결을 따라 컵이 커피이자 음료라는 결론을 얻습니다. 사람이 직접 적은 사실은 **assertion**, 규칙으로 따라오는 결론은 **entailment**라고 부릅니다. 파일에 쓰여 있지 않아도 기존 사실과 규칙 때문에 따라오는 내용을 구분하는 것이 이 도구를 이해하는 출발점입니다. [커피 예제](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/README.md#L215-L233)

| 용어 | 이 리뷰에서의 뜻 |
| --- | --- |
| 클래스·개체 | `Coffee` 같은 종류와 `myCup` 같은 구체적인 대상입니다. |
| IRI | 종류·속성·개체를 식별하는 국제화된 식별자입니다. 코드에서 잠금과 비교의 단위로도 쓰입니다. |
| TBox·ABox | 종류·관계의 규칙을 설명하는 부분과, 실제 개체의 사실을 설명하는 부분입니다. |
| 정합성(consistency) | 주어진 규칙과 사실을 동시에 만족하는 해석이 있는지의 문제입니다. 이름 있는 클래스 하나가 비어야 한다는 문제와 그래프 전체의 모순은 구분해야 합니다. |
| SHACL | 데이터가 개수·자료형 같은 shape 제약을 만족하는지 검사하는 방식입니다. 논리 추론의 모든 질문을 대신하지는 않습니다. |
| 매핑·교차표(crosswalk) | 서로 다른 어휘의 용어 사이에 대응 관계를 적은 표입니다. CSV 열을 RDF 속성으로 바꾸는 입력 매핑과는 쓰임이 다릅니다. |
| MCP | 언어 모델을 사용하는 클라이언트가 서버의 도구를 호출하는 프로토콜입니다. 모델의 판단과 엔진의 검사 결과가 만나는 접점입니다. |

이 구분은 실제 모듈에도 드러납니다. `mapping.rs`는 입력 행을 RDF로 변환하고, `crosswalk.rs`는 두 온톨로지 사이의 대응 주장을 검사합니다. `plan.rs`는 목표 그래프와 현재 그래프를 비교하며, `plan_validate.rs`는 별도로 등록한 행동의 순서가 실행 가능한지 샌드박스에서 확인합니다. 이름에 모두 plan이나 mapping이 들어가더라도 같은 작업은 아닙니다. [입력 매핑](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/mapping.rs#L17-L24), [교차표](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/crosswalk.rs#L98-L134), [행동 계획 검증](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/plan_validate.rs#L9-L29)

## 아키텍처: 그래프와 운영 상태, 증거 검사기를 나눕니다

![CLI와 MCP에서 Rust 엔진으로 들어오는 요청, Oxigraph 그래프와 SQLite 운영 상태, 파일을 통해 연결되는 별도 검사기의 구조]({{ '/img/reviews/2026/open-ontologies-review/architecture.svg' | relative_url }})

그림 1. 리뷰어 작성, 분석 커밋 기준. CLI와 MCP는 공통 변경 엔진을 사용하지만, 후속 감시 같은 진입점별 처리는 다릅니다. 증거 검사기는 별도 실행 파일입니다. [CLI 처리](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/main.rs#L3892-L3928), [MCP 처리](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/server.rs#L2549-L2632), [검사기 호출](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/projection_entailment.rs#L791-L867)

매니페스트의 실행 파일 진입점은 `src/main.rs`입니다. `clap`으로 CLI를 파싱하고, `serve`는 MCP stdio 서버, `serve-http`는 HTTP 서버 경로로 이어집니다. MCP의 `onto_plan`과 `onto_apply`는 `server.rs`에서 입력 구조체를 받아 `Planner`를 생성합니다. 입력은 CLI에서는 Turtle 파일 경로, MCP에서는 `new_turtle` 문자열입니다. Turtle은 RDF를 사람이 읽기 좋게 표현하는 문법입니다. [실행 파일 선언](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/Cargo.toml#L29-L31), [서버 명령](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/main.rs#L233-L290), [MCP 입력](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/inputs.rs#L619-L629)

| 파일·디렉터리 | 중심 책임 | 출력 또는 다음 경계 |
| --- | --- | --- |
| `src/main.rs`, `src/batch.rs`, `src/server.rs` | CLI·배치·MCP 요청 해석 | 공통 엔진 호출과 JSON 결과 |
| `src/graph.rs` | RDF 적재·SPARQL·그래프 직렬화 | Oxigraph의 현재 데이터 |
| `src/state.rs`, `src/ontology.rs` | 운영 상태와 명명된 버전 저장 | SQLite 계획·버전·잠금 테이블 |
| `src/plan.rs` | 변경 차이·위험 보고·실제 적용 | `plan_id`, delta/reload 결과 |
| `src/conservativity.rs`, `src/closure_diff.rs` | 두 그래프의 추론 결과 비교 | 기존 이름에 대한 새로운 결론과 근거 |
| `src/reason.rs`, `lean/OOCert/` | 규칙 추론과 별도 증거 검사 | 전제·도출 단계 파일, 조건부 정리 |
| `src/crosswalk.rs` | 대응표가 주장한 관계의 계층 비교 | 약화된 관계·coverage gap·SSSOM |

표의 모듈 관계는 [공개 모듈 선언](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/lib.rs#L1-L143), [계획 엔진](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/plan.rs#L35-L67), [증거 기록](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/reason.rs#L2587-L2684)을 기준으로 정리했습니다.

### 같은 CLI 명령도 어느 그래프에 연결되는지 확인해야 합니다

그래프 저장 방식의 기본값은 메모리이며, 환경 변수 `OPEN_ONTOLOGIES_STORAGE_MODE`가 설정 파일보다 우선합니다. 독립 CLI 호출이 로컬에서 실행되면 `setup`이 데이터 디렉터리의 SQLite DB와 설정을 열고, 그래프를 새 메모리 저장소 또는 영속 저장소로 선택합니다. 따라서 **계획이 DB에 남아 있다는 사실과, 이전 명령에서 적재한 그래프가 남아 있다는 사실은 다릅니다.** [저장 모드 기본값·우선순위](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/config.rs#L304-L365), [CLI setup](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/main.rs#L1639-L1664)

다만 모든 CLI 요청이 독립 로컬 실행으로 끝나는 것은 아닙니다. 시작 단계에서 프록시 가능한 명령은 실행 중인 daemon을 확인하고 `/api/batch`로 보낼 수 있습니다. `--no-connect`면 이 연결을 건너뜁니다. 연결 또는 인증 실패 시에는 경고를 남기고 로컬 실행으로 돌아오는 경로도 있으므로, 같은 데이터 디렉터리를 지정했다는 이유만으로 늘 같은 실행 중 그래프를 읽는다고 가정할 수 없습니다. [초기 라우팅](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/main.rs#L2095-L2111), [daemon 확인](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/main.rs#L1550-L1569), [프록시와 로컬 fallback](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/connect.rs#L16-L65)

## 작동 원리 1: 현재 상태와 전체 목표 상태로 계획을 만듭니다

### 입력은 추가할 조각이 아니라 전체 목표 그래프입니다

`onto_plan`의 `new_turtle`은 변경분만 담은 패치가 아닙니다. 제안한 전체 그래프입니다. CLI도 파일을 문자열로 읽어 같은 `plan_with`를 호출합니다. 목표에서 빠진 기존 개체 데이터까지 실제 적용에서 사라질 수 있으므로, TBox만 넣고 ABox가 유지될 것이라고 생각하면 안 됩니다. MCP는 보수성 검사에 `Replacement` 모드를 고정합니다. [전체 목표 상태의 계약](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/docs/lifecycle.md#L20-L34), [CLI 입력 처리](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/main.rs#L3892-L3915), [MCP replacement 설정](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/server.rs#L2555-L2579)

`plan_inner`는 제안 Turtle을 임시 `GraphStore`에 적재하고, 현재/제안 그래프에서 클래스·속성·개체 집합을 추출합니다. 집합의 차이가 추가·삭제 목록입니다. 이어 삭제되는 식별자를 참조하는 삼중항 수를 더해 `blast_radius.triples_affected`를 계산합니다. 여기서 blast radius는 **삭제 항목의 참조량을 모은 구현상의 지표**입니다. 모든 종류의 의미 변화나 모든 소비 애플리케이션의 영향도를 측정하는 값은 아닙니다. [차이와 참조량 계산](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/plan.rs#L430-L465)

위험 점수는 먼저 구조적 차이에서 나옵니다. 삭제가 있고 참조량도 있으면 `high`, 삭제만 있으면 `medium`, 삭제가 없으면 `low`입니다. 클래스·속성의 삭제가 IRI 잠금과 충돌하는지도 `locked_violations`에 담습니다. 따라서 점수는 예측 확률이 아니라 코드가 정한 분기 결과입니다. 개별 참조 삼중항이 여러 삭제 IRI를 참조할 수 있으므로 이 합계를 중복 제거된 영향 삼중항 수로 확대 해석하는 것도 피해야 합니다. [잠금·위험 분기](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/plan.rs#L467-L512)

계획은 무작위 식별자를 붙여 SQLite의 `plans`에 저장합니다. 저장하는 핵심 값은 소유자, 목표 Turtle, 클래스·속성의 추가/삭제 목록이며 최근 100개를 유지합니다. CLI의 기본 소유자는 고정 문자열 `cli`, MCP는 세션 ID입니다. `plan_id`를 생략한 적용은 해당 소유자의 최신 계획을 고르고, ID를 명시한 조회에는 소유자 필터가 없습니다. 이는 기본 선택의 혼선을 줄이는 장치이며 별도 접근 권한 체계로 해석하면 안 됩니다. [계획 저장·보존](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/plan.rs#L670-L719), [CLI 소유자](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/plan.rs#L28-L43), [MCP 세션 연결](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/server.rs#L2549-L2554)

### 구조적 차이 위에 의미 변화와 논리 검사를 얹습니다

`plan_with`는 구조적 계획에 두 개의 다른 질문을 덧붙입니다. CLI·배치·MCP 진입점은 둘을 기본 활성화합니다. 반면 라이브러리의 간단한 `Planner::plan`은 보수성 옵션을 넘기지 않습니다. 실제 이용 경로를 구분해야 기본값을 정확히 설명할 수 있습니다. [조합 순서](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/plan.rs#L150-L232), [배치 기본값](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/batch.rs#L1133-L1163)

**보수성(conservativity)**은 기존 어휘에 대해 새로운 결론이 생겼는지 묻습니다. 여기서 어휘 또는 signature는 기존 그래프가 사용하던 이름들의 집합입니다. 단, 이 구현의 판정은 지정한 Horn 규칙표에 한정됩니다. Horn 규칙은 여러 전제가 성립하면 하나의 결론을 도출하는 형태의 규칙으로 이해하시면 됩니다. 모든 OWL 의미론에서 변화가 없는지 증명하는 질문과는 범위가 다릅니다. [판정 범위](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/conservativity.rs#L61-L91)

실제 계산은 현재 그래프를 기준으로 제안 내용을 합친 쪽과 기준 쪽의 closure를 비교합니다. Closure는 더 이상 규칙으로 새 사실이 나오지 않을 때까지 얻은 결과 집합입니다. 확장 쪽에만 있는 결론 중 기존 이름으로 표현된 항목을 골라, 어떤 규칙이 만들었고 기준 그래프에 어떤 전제가 없었는지 보고합니다. 하지만 전체 목표가 기존 사실을 삭제한다면 순수한 확장이 아니므로 `undecided_not_an_extension`을 반환합니다. 스캔이 잘리면 `undecided_scan_truncated`이며, 추론의 단조성 위반을 발견한 경우도 별도 미결정 상태입니다. **새 결론이 있다는 발견과, 없다는 판정이 갖는 보장 범위가 비대칭**이라는 점이 중요합니다. [closure 비교와 signature 필터](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/conservativity.rs#L298-L395), [판정 우선순위](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/conservativity.rs#L404-L434)

**논리 검사 `logic`**는 새 결함과 정합성을 봅니다. `Defects::findings`로 현재/제안 그래프의 TBox 결함을 비교하여 새 `error`·`warning`을 찾으면 위험도를 높입니다. 또 OWL-DL tableaux 추론기로 제안 그래프의 정합성을 묻습니다. Tableaux는 가능한 해석을 전개하면서 충돌을 찾는 방식입니다. 새 그래프가 모순이고 기존 그래프가 모순임을 입증하지 못했다면 `high`로 올립니다. 기존부터 있던 결함을 변경이 만든 결함으로 세지 않으려는 설계입니다. [새 결함 비교](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/plan.rs#L257-L354)

여기서 `abox_consistent`는 `true`·`false`·`null`의 세 값입니다. 충돌을 찾으면 `false`, 탐색이 끝나고 모델링하지 않는 구문도 없을 때만 `true`, 시간·단계 예산이 소진되거나 미지원 구문이 있으면 `null`과 이유를 반환합니다. 검사를 못 했다는 사실이 정상 판정으로 바뀌지 않도록 한 것입니다. [세 값의 결정 과정](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/plan.rs#L357-L427)

두 검사는 오류나 생략 때문에 실행되지 못해도 계획 자체는 반환할 수 있습니다. CLI의 `plan`도 위험도 `high`라는 이유만으로 실패 종료하지 않습니다. 자동화에서 종료 코드만 보면 보고서의 중요한 경고를 놓칠 수 있고, `ran`, `skipped`, `logic`, `risk_reasons`를 읽는 호출자의 정책이 필요합니다. [검사 실패 처리](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/plan.rs#L184-L232), [CLI 종료 계약](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/main.rs#L3913-L3920)

## 작동 원리 2: 보고서, 승인 판단, 실제 적용은 별개입니다

![계획 생성에서 구조와 의미를 진단한 뒤 호출자가 승인 판단을 하고, 적용 시 monitor 상태를 확인하여 delta 또는 reload를 수행하는 흐름]({{ '/img/reviews/2026/open-ontologies-review/lifecycle.svg' | relative_url }})

그림 2. 리뷰어 작성, 분석 커밋 기준. 가운데 승인 판단은 호출자 책임이며 엔진 내부 승인 기록이 아닙니다. 잠금 위반·논리 판정은 보고서이고, 적용의 직접 차단 조건은 monitor 상태입니다. [계획 조합](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/plan.rs#L187-L232), [적용 분기](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/plan.rs#L571-L615), [MCP 후속 감시](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/server.rs#L2613-L2632)

### `safe`가 의미하는 범위

`apply_plan`은 `force`가 아닐 때 monitor의 차단 플래그를 확인합니다. 차단돼 있으면 Rust 오류 대신 `ok: false`, `blocked: true`인 JSON을 정상 반환합니다. 차단이 없으면 지정한 계획을 불러와 목표 상태를 적용합니다. **`risk_score`, `logic`, `locked_violations`를 다시 읽어 적용을 거부하는 분기는 없습니다.** 코드 주석도 위험 판정을 호출자 파이프라인에서 gate하도록 명시합니다. 즉 `safe`라는 모드명만으로 논리 정합성 검사와 사람의 승인까지 강제된다고 볼 수 없습니다. [적용 코드와 설명](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/plan.rs#L549-L615)

계획의 저장 형식에도 기준 그래프의 fingerprint나 승인 상태는 없습니다. 적용할 때는 저장된 목표 Turtle과 **그 시점의 실제 그래프** 사이에서 delta를 다시 계산합니다. 정적 코드에서 읽히는 운영상 함의는, 계획과 적용 사이에 다른 변경이 생기면 예전 보고서가 본 기준과 실제 적용 기준이 달라질 수 있다는 것입니다. 계획 ID는 목표를 지정하지만, 원래 검토한 기준 상태까지 고정하는 토큰은 아닙니다. [저장 열](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/plan.rs#L678-L697), [적용 시 재계산](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/plan.rs#L584-L600)

### delta 적용과 blank node의 reload

명명된 삼중항만 있으면 현재와 목표를 `HashSet`으로 만들고 집합 차이를 구합니다. 삭제를 먼저, 추가를 나중에 하며, 각 묶음은 최대 500개씩 `DELETE DATA`와 `INSERT DATA`로 보냅니다. 양쪽 중 어느 쪽이든 blank node가 있으면 reload를 택합니다. Blank node는 전역 이름이 없는 노드로, 저장소마다 붙인 지역 이름을 그대로 비교하면 같은 대상을 잘못 판단할 수 있기 때문입니다. [전략 선택](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/plan.rs#L617-L645), [배치 쓰기](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/plan.rs#L647-L659)

reload는 그래프를 비운 뒤 목표를 적재합니다. delta도 여러 번의 업데이트 호출로 나뉩니다. 이 함수 전체를 하나의 트랜잭션으로 감싸거나 자동으로 이전 버전으로 복구하는 처리는 이 경로에서 보이지 않습니다. 그러므로 여기서 확인한 것은 변경 전략과 반환 필드이며, 중도 실패·동시 변경·프로세스 중단까지 포함한 원자성을 입증한 것은 아닙니다. 또한 `all_triples()`는 named graph의 이름을 반환하지 않고 주어·술어·목적어만 추출합니다. 이 계획 경로를 named graph별 변경 보존 기능으로 일반화하기도 어렵습니다. [적용 순서](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/plan.rs#L590-L614), [삼중항 추출](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/graph.rs#L1065-L1075)

`migrate`는 먼저 이름 변경 후보를 찾고 목표 상태를 적용한 다음, 삭제된 용어에서 새 용어로 `owl:equivalentClass` 또는 `owl:equivalentProperty` 연결을 추가합니다. 후보는 `DriftDetector`에서 오며 이름/라벨 유사도 0.6 미만은 제외하고 양쪽을 한 번씩만 대응시킵니다. 결과에는 `bridges`와 `unbridged_removals`가 들어갑니다. 이 연결은 논리적으로 강한 동치 주장인데 선정은 유사도 휴리스틱이므로, 앞서 본 `exactMatch` 교차표 검사나 Lean 검사가 이 경로에 자동으로 붙는다고 생각하면 안 됩니다. [이행 적용](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/plan.rs#L784-L846), [후보 제한](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/plan.rs#L849-L900)

### 감시와 롤백은 어떤 상태를 되돌리나요?

MCP `onto_apply`는 `Planner`가 `Ok`를 반환한 가지에서 lineage를 기록하고 watcher를 실행합니다. 위에서 본 차단 JSON도 `Ok`이므로, 이 wrapper를 통과했다는 사실과 실제 적용 성공은 구분해야 합니다. watcher는 임계값 초과 시 알림, 다음 적용 차단, 자동 롤백 등을 수행합니다. 반면 직접 CLI apply와 배치 apply는 `Planner` 결과를 반환하며, 이 wrapper의 후속 watcher 호출을 거치지 않습니다. 별도 감시 루프를 사용한다면 그 설정도 따로 봐야 합니다. [MCP wrapper](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/server.rs#L2620-L2631), [직접 CLI](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/main.rs#L3922-L3928), [배치](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/batch.rs#L1169-L1179), [감시 루프 기본 비활성](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/config.rs#L477-L487)

버전 저장은 `OntologyService::save_version`이 N-Quads 스냅샷을 SQLite에 넣는 별도 동작입니다. 명명된 버전의 롤백은 DB에서 내용을 읽고 현재 그래프를 비운 뒤 다시 적재합니다. 자동 롤백은 가장 최근에 저장한 버전을 선택하며, 저장 버전이 없으면 실패 이유를 출력합니다. 따라서 `plan`이나 `apply`가 자동으로 복구용 버전을 만든다고 가정할 수 없습니다. `plan_id`의 목표 Turtle과 `ontology_versions`의 복구 스냅샷은 다른 종류의 저장물입니다. [버전 저장](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/ontology.rs#L225-L238), [롤백](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/ontology.rs#L259-L278), [자동 롤백](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/monitor.rs#L78-L108)

## 작동 원리 3: 추론 결과가 증거가 되는 과정

### 프로필과 규칙표가 먼저 정해집니다

`reason.rs`의 추론기는 RDF 항을 정수 ID로 바꾸고 삼중항 집합에 규칙을 반복 적용합니다. 매 반복마다 현재 closure에서 인덱스를 만들고 새 결론을 모읍니다. 증거를 요청하면 각 결론이 처음 도출될 때 규칙과 전제들을 기록합니다. 반환 결과에는 추론 수뿐 아니라 `fixpoint_reached`도 있으므로, 파일을 얻었다는 사실과 완전한 고정점까지 도달했다는 사실을 나눌 수 있습니다. [추론 루프와 기록](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/reason.rs#L1730-L1778), [결과 필드](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/reason.rs#L2536-L2549)

지원 프로필은 같은 크기의 추론기가 아닙니다. 선언된 규칙표 기준 `rdfs`는 6개, `owl-rl`은 누적 17개, `owl-rl-ext`는 29개 규칙입니다. `owl-dl`은 별도 tableaux 경로이며 이 전방 추론의 증거 옵션을 거부합니다. 이 구분을 빼고 “OWL을 증명한다”고만 표현하면 실제 범위를 잃습니다. [프로필별 규칙표](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/reason.rs#L281-L311), [프로필 분기와 거부](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/reason.rs#L1600-L1636)

### 증거 생성은 검사기 실행과 다릅니다

![추론기가 전제와 도출 단계 및 scope 파일을 만들고, 별도 검사기가 파일을 검사하며, 실제 업무 상태는 파일 밖에 남는 증거 흐름]({{ '/img/reviews/2026/open-ontologies-review/evidence.svg' | relative_url }})

그림 3. 리뷰어 작성, 분석 커밋 기준. `reason --certificate`의 기록 단계와, 보존성·closure 비교 등의 경로에서 수행하는 검사기 실행을 분리해 나타냈습니다. 검사기가 읽는 전제 파일과 원래 의도한 업무 데이터의 일치는 별도로 확인해야 합니다. [파일 기록](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/reason.rs#L2587-L2684), [검사기 실행](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/projection_entailment.rs#L791-L867), [신뢰 경계 문서](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/docs/trusted-computing-base.md#L25-L42)

증거 디렉터리에는 다음 파일이 기록됩니다. [실제 writer](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/reason.rs#L2587-L2684)

| 파일 | 기록하는 내용 | 파일만으로 알 수 없는 것 |
| --- | --- | --- |
| `asserted.tsv` | 추론의 출발점인 삼중항 | 그 전제가 실제 업무 사실인지 |
| `derivations.tsv` | 결론마다 규칙 이름과 전제 삼중항 | 엔진 밖의 업무 정책이 타당한지 |
| `asserted.sha256` | 전제 파일 바이트의 해시 | 외부 세계가 그 상태였는지 |
| `scope.tsv` | 읽은 그래프와 선택 범위 | Lean 검사기가 선택 의도의 적절성까지 판정하는 것은 아님 |

`Reasoner`의 이 코드 블록은 파일과 `check_with` 안내를 생성합니다. 파일을 생성하는 즉시 매번 Lean을 실행해 받아들여졌다는 뜻은 아닙니다. closure 비교에서 사용하는 별도 `run_checker`는 실행 파일을 찾고, `oo-cert`에 전제·도출 파일을 전달하거나 `oo-horn check`에 규칙표까지 전달합니다. subprocess 종료 코드와 허용된 정리 이름을 읽어 `Accepted`, `Rejected`, `Unreadable`, `Absent`를 구분합니다. 검사기 부재와 증거 거부가 같은 뜻으로 합쳐지지 않습니다. [검사기 탐색](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/projection_entailment.rs#L742-L776), [실행과 판정](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/projection_entailment.rs#L791-L867)

Lean 소스의 중심 정리는 다음과 같습니다. 아래는 실행 결과가 아니라 원문 코드 발췌입니다.

```lean
theorem certificate_sound (G : List Triple) (steps : List Step)
    (h : checkCert G steps = true) : ∀ st ∈ steps, Entails G st.conclusion := by
```

출처: [lean/OOCert/Soundness.lean 459–460행](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/lean/OOCert/Soundness.lean#L459-L460). 정리의 증명 본문은 생략했습니다.

조건 `checkCert G steps = true` 아래에서, 기록된 각 단계의 결론이 `G`로부터 따라온다는 형태입니다. 이는 도출의 건전성에 관한 주장입니다. 모든 참인 결론을 빠짐없이 찾았다는 완전성, 프로그램 전체의 정확성, 전제의 현실적 진실성까지 이 한 문장에서 나오는 것은 아닙니다. 이 리뷰에서는 정리 선언과 연결 코드를 읽었으며 증명 빌드 성공을 직접 확인하지 않았습니다. [정리와 공리 확인 선언](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/lean/OOCert/Soundness.lean#L458-L475), [명시된 신뢰 기반](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/docs/trusted-computing-base.md#L3-L14)

### 사용자 규칙은 추가 가정입니다

`oo-horn`은 규칙표가 정확히 내장 표와 같은지 비교합니다. 같으면 `entailed`와 `OOCert.entails_of_builtin_horn`, 다르면 `entailed_under_supplied_rules`와 `OOCert.horn_certificate_sound`를 출력하도록 구현되어 있습니다. 임의 규칙표에 대한 정리의 결론은 `EntailsR G R`입니다. 즉, **주어진 사실뿐 아니라 제공한 규칙도 만족하는 해석들에서 결론이 따른다**는 조건이 추가됩니다. “모든 공급자는 적합하다” 같은 잘못된 업무 규칙을 넣었을 때, 검사기가 그 규칙 자체의 진실을 보증하는 것은 아닙니다. [실제 verdict 선택](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/lean/HMain.lean#L72-L97), [일반 Horn 정리](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/lean/OOCert/Horn.lean#L503-L516), [내장 규칙 정리](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/lean/OOCert/HornBuiltin.lean#L427-L445)

`verdict.rs`는 증거를 얻은 상태를 private 필드 타입으로 나타내, 다른 모듈이 문자열만 넣어 같은 상태를 만들기 어렵게 합니다. 입력 파일의 digest를 검사 전에 계산하고 실제 subprocess 결과를 읽습니다. 다만 검사 실행 파일은 환경 변수나 경로로 선택할 수 있습니다. 가짜 프로그램이 성공 종료와 예상 출력을 흉내 내는 문제를 타입만으로 막지는 못합니다. 검사기가 읽은 파일과 실제 저장소의 일치, 선택한 시점과 그래프의 의미도 별도 경계입니다. **증거를 다루는 API의 규율과 실행 환경 전체의 신뢰는 다른 층위**입니다. [실행 결과와 digest](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/verdict.rs#L139-L197), [잔여 신뢰 경계](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/verdict.rs#L30-L70), [scope의 한계](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/reason.rs#L2677-L2683)

## 작동 원리 4: `exactMatch`를 검사하면 무엇이 남나요?

두 어휘가 같은 대상을 서로 다른 이름으로 부를 때 대응표를 만듭니다. `skos:exactMatch`는 두 개념을 강하게 대응시키는 표현이지만, 이름이 비슷하다는 이유만으로 그 주장을 신뢰하기는 어렵습니다. 이 저장소의 `align.rs`에는 라벨 유사도와 속성·상위 개념 겹침으로 관계 종류를 고르는 휴리스틱이 있습니다. 라벨 유사도가 0.8보다 높으면 `skos:exactMatch` 후보를 만들 수 있습니다. 후보를 제안하는 단계와 그 주장을 검사하는 단계가 구분되어야 합니다. [후보 관계 분류](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/align.rs#L1279-L1305)

README는 각 온톨로지를 따로 추론하고, 매핑으로 번역한 함의들을 비교해 과한 `exactMatch`를 약화한다고 설명합니다. 실제 `crosswalk::certify`도 양쪽에서 따로 상위 개념을 얻은 다음, **매핑 자체를 번역표로 사용**합니다. 소스 개념의 조상 중 번역 가능한 것과, 타깃 조상 중 대응표에 등장하는 것을 비교합니다. OWL의 이름 있는 상위 클래스 외에 SKOS의 `broader`·`broaderTransitive` 경로도 별도로 수집합니다. [README 설명과 한계](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/README.md#L333-L343), [조상·SKOS 계층 추출](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/crosswalk.rs#L162-L202), [대응표를 통한 번역](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/crosswalk.rs#L258-L304)

| 비교 가능한 두 조상 집합 | 구현이 고르는 가장 강한 관계 |
| --- | --- |
| 같은 집합 | `exactMatch`와 양립 가능 |
| 소스 쪽 번역 집합이 진상위집합 | 소스가 더 구체적이므로 `broadMatch` |
| 타깃 쪽 집합이 진상위집합 | 타깃이 더 구체적이므로 `narrowMatch` |
| 양방향으로 다른 조상이 존재 | `relatedMatch` |

방향은 중요합니다. `broadMatch`의 목적어가 더 넓은 개념입니다. 소스가 더 많은 상위 조건에 속하면 소스가 더 구체적이므로 목적어를 넓은 쪽으로 적는 것입니다. [집합 비교의 구현](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/crosswalk.rs#L218-L255)

비교할 수 없는 조상은 `untranslatable`·`object_uncovered`라는 coverage gap으로 남깁니다. 번역되지 않는 항목이 있다는 사실만으로 불일치라고 판정하지 않습니다. 양쪽 모두 비교할 조상이 없으면 집합은 같아 보일 수 있지만, 최종 `certification`은 `not_refuted_nothing_compared`입니다. 비교했으며 누락이 있으면 `upheld_with_coverage_gap`으로 구분합니다. `supported` 필드 하나만 읽으면 이 차이를 놓칩니다. [gap·무비교 판정](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/crosswalk.rs#L281-L341)

더 근본적으로 이 검사는 **계층에서의 위치를 비교하며 뜻의 동일성을 증명하지 않습니다.** 같은 부모 아래 서로 다른 형제 개념은 조상 집합이 같아서 잘못 짝지어도 통과할 수 있습니다. 따라서 SSSOM 출력은 과한 주장을 약화할 때만 관계를 바꾸고, 원래 약한 주장을 자동으로 강화하지 않습니다. 최종 JSON verdict도 `checked_by_this_engine`이며 Lean이 증명한 SKOS 관계라고 표시하지 않습니다. [보고서의 보장 범위](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/crosswalk.rs#L363-L405), [강화하지 않는 SSSOM 출력](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/crosswalk.rs#L408-L430)

지원 규칙 수에 관해서는 같은 커밋 내부의 설명 차이도 보입니다. 교차표의 `means` 문자열에는 전체 구현 규칙 수인 “29 of 78”이 적혀 있지만, 실제 호출은 `owl-rl`이고 규칙표와 프로필 분기는 누적 17개를 사용합니다. 29개 전체는 `owl-rl-ext`입니다. 그러므로 이 검사에 29개가 모두 적용된다고 읽어서는 안 됩니다. 어떤 공리가 검사에서 보이지 않는지 별도로 살피라는 문서의 취지는 유효하지만, 숫자는 실행 경로와 맞춰 읽어야 합니다. [교차표 호출](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/crosswalk.rs#L162-L164), [보고서 문자열](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/crosswalk.rs#L400-L404), [프로필별 규칙](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/reason.rs#L281-L311), [분기](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/reason.rs#L1630-L1636)

`crosswalk-probe`는 또 다른 질문을 합니다. 소스에서 번역한 하위 클래스 관계를 타깃에 추가했을 때 새 충돌이 생기는지를 봅니다. 클래스만 있는 그래프의 모순 가능성도 탐지하도록, 관계를 전달받는 타깃 클래스마다 임시 witness 개체를 만듭니다. 타깃만 있을 때의 충돌 수를 기준선으로 빼서 매핑이 추가한 충돌을 보고합니다. 하지만 지원하는 충돌 규칙 안에서 찾지 못했다는 결과는 호환성 증명과 다릅니다. SKOS의 `broader`를 그대로 OWL 하위 클래스 관계처럼 취급하지도 않습니다. [probe 입력·witness·기준선](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/crosswalk.rs#L525-L620), [결과의 한계](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/crosswalk.rs#L623-L648), [SKOS 경계](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/crosswalk.rs#L192-L193)

## 같은 커밋 문서로 살펴보는 사용법

아래 명령과 설정은 분석 커밋의 원문에서 발췌한 사용 예시이며, 이 리뷰에서 실행하지 않았습니다. 설치 문서는 운영체제별 릴리스 바이너리와 `init`을 안내합니다. 다만 그 다운로드 URL의 `latest`는 실행 시점에 따라 달라집니다. 고정 커밋의 문서를 읽는 것과, 그 문서가 내려받는 바이너리까지 같은 버전인 것은 구분해야 합니다. [설치 안내](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/docs/quickstart.md#L5-L15)

MCP 연결 예시는 다음과 같습니다.

```json
{
  "mcpServers": {
    "open-ontologies": {
      "command": "open-ontologies",
      "args": ["serve"]
    }
  }
}
```

출처: [docs/quickstart.md 21–30행](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/docs/quickstart.md#L21-L30). 이 설정은 엔진을 stdio 도구 서버로 시작하는 예시입니다. 이후 모델이 어떤 순서로 도구를 호출하고 보고서를 승인 기준에 연결할지는 클라이언트의 역할입니다.

메모리 저장소를 한 프로세스에서 사용하는 증거 생성 예시는 문서에 다음처럼 나옵니다.

```bash
printf 'load ontology.ttl\nreason --profile owl-rl-ext --certificate /tmp/cert\n' \
  | open-ontologies --no-connect --data-dir /tmp/store batch -
```

출처: [docs/lean-certificates.md 18–20행](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/docs/lean-certificates.md#L18-L20). 한 배치에서 load와 reason을 수행하므로 독립 프로세스 사이의 메모리 소멸 문제를 피하도록 구성되어 있습니다. `--no-connect`는 기존 daemon의 그래프를 사용하지 않도록 합니다. 이 명령은 추론 증거를 생성하는 예시이며, 계획 검토와 적용 전체를 하나의 무인 절차로 승인하는 예시는 아닙니다.

별도 CLI에서 저장 상태를 공유하는 README의 예시에는 영속 모드와 같은 데이터 디렉터리가 등장합니다.

```bash
export OPEN_ONTOLOGIES_STORAGE_MODE=persistent          # in-memory by default, see below
open-ontologies --data-dir /tmp/oo-demo/store load coffee.ttl
open-ontologies --data-dir /tmp/oo-demo/store reason --profile rdfs --certificate ./cert
```

출처: [README 226–229행](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/README.md#L226-L229). 앞서 README가 생성한 `coffee.ttl`을 전제하는 발췌입니다. 이 파일 생성 부분은 생략했습니다.

생성한 증거를 검사하는 문서의 명령은 다음과 같습니다. Rust 엔진의 설치와 별개로 Lean 도구체인과 checker 빌드가 필요한 경로입니다.

```bash
cd lean
lake build                      # builds the checker AND checks the proofs
lake exe oo-cert /tmp/cert/asserted.tsv /tmp/cert/derivations.tsv
```

출처: [docs/lean-certificates.md 57–64행](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/docs/lean-certificates.md#L57-L64). 문서는 종료 코드 0을 모든 단계 수락, 1을 단계 거부, 2를 읽기·파싱 실패로 설명합니다. 이 리뷰에서는 해당 도구체인 설치나 빌드를 수행하지 않았습니다.

변경 관리의 문서 예시는 `oo plan proposed.ttl`과 `oo apply safe --plan-id ...` 형태입니다. 이때 `oo`는 문서의 축약 표기이며, Cargo 매니페스트가 선언한 실행 파일명은 `open-ontologies`입니다. 실제 검토에서는 먼저 현재 저장소·전체 목표 그래프·복구 버전을 분리해서 이해하고, 계획의 각 판정과 미실행 이유를 읽은 뒤 호출자 정책으로 적용 여부를 결정하는 것이 코드의 계약에 맞습니다. [lifecycle 예시](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/docs/lifecycle.md#L89-L119), [실행 파일명](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/Cargo.toml#L29-L31)

## 외부 경계와 읽어야 할 제약

“하나의 바이너리”는 중심 Rust 엔진의 배포 형태를 설명합니다. 선택 기능의 모든 작업이 외부 실행 환경 없이 끝난다는 뜻은 아닙니다. 매니페스트의 기본 기능 집합은 비어 있고 SQL·임베딩·WASM 플러그인 등은 feature로 나뉩니다. 증거 검사기, 선택적 외부 솔버, 원격 임베딩 서버는 각각 다른 실행·신뢰 경계입니다. [기능 플래그](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/Cargo.toml#L73-L97)

- **모델·클라이언트 경계:** MCP 도구를 고르고 목표 Turtle을 작성하는 클라이언트의 판단은 `Planner` 내부 승인 정책이 아닙니다. 자연어로 요청했다는 사실이 `apply`에 승인 기록을 만드는 것은 아닙니다. [MCP 계획·적용 호출](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/server.rs#L2549-L2632)
- **외부 계획 솔버:** `plan_classical.rs`는 Fast Downward를 subprocess로 실행하는 선택 wrapper입니다. 반환된 연산자 인자를 원래 IRI로 바꾸는 책임은 orchestrator에 남아 있습니다. 이 행동 계획은 앞서 다룬 목표 그래프 변경 계획과 별도 경로입니다. `plan_validate`는 샌드박스에서 순차 적용 가능성을 확인하지만, 목표 사실이 미충족이어도 `valid` 자체를 거짓으로 바꾸지 않고 `unsatisfied_goals`에 보고합니다. [외부 솔버 경계](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/plan_classical.rs#L1-L25), [샌드박스와 목표 계약](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/plan_validate.rs#L9-L35)
- **원격 모델 서버:** 임베딩 feature의 `OpenAIEmbedder`는 설정한 `{api_base}/embeddings`에 텍스트를 HTTP 요청으로 보냅니다. 요청하는 벡터와 유사도는 추론 증거의 정리와 별개입니다. 실제 배포에서는 선택한 endpoint와 전달 텍스트를 데이터 경계로 보아야 합니다. [HTTP 요청](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/embed_remote.rs#L92-L110)
- **검사기의 범위:** 증거 수락은 그 파일이 표현하는 전제와 규칙에 조건부입니다. `scope.tsv`는 읽은 범위를 기록하지만 Lean checker가 읽는 검증 대상은 아닙니다. 전체 엔진·저장소·시점 선택까지 형식 검증됐다고 표현할 수 없습니다. [신뢰 기반 문서](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/docs/trusted-computing-base.md#L25-L54), [scope 기록](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/reason.rs#L2648-L2683)

코드를 읽으며 가장 유용했던 설계는 `unknown`, `skipped`, `engine_opinion`, coverage gap처럼 **검사할 수 없었던 범위를 결과에 남기는 것**이었습니다. 반대로 소비자가 `ok`, 종료 코드, `supported`만 읽으면 그 정보를 쉽게 버릴 수 있습니다. 보고서 필드 전체와 실제 실행 경로를 함께 읽어야 한다는 것이 이 정적 분석의 실용적 결론입니다. [세 값 정합성](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/plan.rs#L390-L417), [교차표의 제한](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/crosswalk.rs#L386-L404), [검사기 상태](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/src/projection_entailment.rs#L854-L866)

### 라이선스

분석 커밋의 루트 `LICENSE`는 MIT License이며 저작권 표기와 허가 문구의 유지 조건, 무보증 조항을 포함합니다. `Cargo.toml`도 MIT로 선언합니다. 이는 이 저장소 코드의 라이선스 확인이며, 외부 온톨로지·모델·벤치마크 데이터·별도 솔버까지 모두 같은 조건이라고 확장할 수는 없습니다. 이 글의 도식은 원본 그림을 복제하지 않고 코드 흐름을 바탕으로 리뷰어가 작성했습니다. [LICENSE](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/LICENSE#L1-L21), [매니페스트](https://github.com/fabio-rovai/open-ontologies/blob/cefe5997d04553ac495873e8aa1046c1d6b85f7d/Cargo.toml#L1-L7)

## 결론

Open Ontologies를 이해하는 핵심은 세 가지를 나누는 데 있습니다. 변경 계획은 현재와 목표 사이의 구조·의미·논리 문제를 보고합니다. 적용은 그 보고서를 호출자가 판단한 뒤 요청하는 별도 동작입니다. 추론 증거는 기록된 전제에서 결론이 따라오는지를 다시 검사할 수 있게 하지만, 전제와 규칙의 업무상 타당성까지 대신 보증하지는 않습니다.

이 구분을 유지하면 `safe`, `exactMatch`, `certified` 같은 단어도 구체적으로 읽을 수 있습니다. 이 저장소에서 배울 만한 부분은 많은 검사를 하나로 합친 성공 표시보다, 서로 다른 근거와 미결정 상태를 결과의 어휘로 구분하려는 구조입니다.

## 이 글에서 다루지 못한 부분

분석은 변경 관리와 전방 추론 증거, 교차표 검사를 중심으로 진행했습니다. SHIQ tableaux의 전체 탐색·모델 증명, SHACL Rust·Lean 구현의 전체 지원 범위, Isabelle 독립 검사기, 일차 논리 변환과 외부 증명기, 최소 정당화·repair, 시간 그래프 전체, RAG 투영 보존, 수치 행렬 증명, 플러그인과 Studio UI는 전수 분석하지 않았습니다. 입력 행 매핑·외부 계획 솔버·원격 임베딩은 경계 확인 수준으로 읽었습니다. 대상 저장소의 빌드·테스트·벤치마크·실서비스 배포를 실행하지 않았으므로 성능·동시성·운영 복구 성공에 대한 실측 평가는 포함하지 않습니다.
