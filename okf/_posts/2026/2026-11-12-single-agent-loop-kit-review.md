---
type: "Repo Review"
title: "[Repo Review] Single Agent Loop Kit, 서브에이전트의 역할을 옮기고 회귀를 확인하는 법"
description: "Anthropic의 Single Agent Loop Kit에서 서브에이전트 전환 절차, 스킬과 도구를 호출하는 Python 루프, 고객 지원 예제의 전후 평가를 따라갑니다."
date: "2026-11-12"
tags:
  - "Repo Review"
  - "AI Agent"
  - "Anthropic"
  - "Claude"
  - "Python"
resource: "https://github.com/anthropics/single-agent-loop-kit/tree/c43796287b83bec847db923f07131d1cc8de750d"
generated:
  by: "process:blog-review"
  at: "2026-11-12T06:04:24+09:00"
sources:
  - id: "anthropics/single-agent-loop-kit"
    resource: "https://github.com/anthropics/single-agent-loop-kit/tree/c43796287b83bec847db923f07131d1cc8de750d"
    title: "Single agent loop kit"
status: "stable"
year: "2026"
analyzed_at: "2026-11-12T06:04:24+09:00"
source_id: "anthropics/single-agent-loop-kit"
source_revision: "c43796287b83bec847db923f07131d1cc8de750d"
source_title: "Single agent loop kit"
source_type: "repo"
source_url: "https://github.com/anthropics/single-agent-loop-kit/tree/c43796287b83bec847db923f07131d1cc8de750d"
visual_sources:
  - path: "/img/reviews/2026/single-agent-loop-kit-review/agent-loop.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/reference_loop/loop.py#L222-L282"
    caption: "리뷰어 작성, 분석 커밋 기준. 메인 모델의 도구 배치, 읽기와 쓰기 순서, 결과 반환 흐름."
    evidence_urls:
      - "https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/reference_loop/loop.py#L134-L165"
      - "https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/reference_loop/loop.py#L180-L219"
---

## 고객의 조건부 요청을 누가 끝까지 처리할까요?

가상의 가전 쇼핑몰 고객이 배송 지연을 물으며, 특정 날짜까지 도착하지 않으면 별도 주문을 반품해 달라고 요청합니다. 배송 예정일을 확인한 뒤 그 결과를 반품 조건에 적용하고, 실제 반품 기록을 남겨야 끝나는 작업입니다. 주문·배송·반품이 서로 다른 서브에이전트에 있으면 라우터가 각 결과를 전달하고 다음 행동을 결정합니다. 한 에이전트가 대화를 이어받아 스킬과 도구를 필요할 때 불러오는 구조에서는 같은 모델이 예정일과 반품 조건을 함께 볼 수 있습니다. [고객 지원 평가 t11](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/examples/support-desk/evals/golden.jsonl#L11) · [전환 전 라우터](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/examples/support-desk/app/orchestrator.py#L78-L109)

Single Agent Loop Kit는 이러한 시스템을 한 번에 한 변경씩 전환하고, 동일한 과제의 결과를 비교하는 Anthropic의 참조 저장소입니다. 스킬은 특정 업무의 절차와 지식을 담은 문서이며, 도구는 주문 조회나 반품 생성처럼 모델이 호출하는 함수입니다. 분석 대상은 `release` 브랜치에서 확인한 커밋 `c437962`입니다. [고정 소스](https://github.com/anthropics/single-agent-loop-kit/tree/c43796287b83bec847db923f07131d1cc8de750d) · [저장소 소개](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/README.md#L4-L26)

## 저장소의 구성

| 경로 | 역할 |
| --- | --- |
| `skill/SKILL.md`와 `skill/steps/` | Claude Code에서 읽는 전환 절차입니다. 서브에이전트별 판단, 기준 평가, 변경 후 비교를 순서대로 진행합니다. |
| `skill/scripts/`와 `skill/templates/` | 호출 추적과 평가 로그를 읽는 Python 도구, 계획서와 응답 스키마 등 전환 산출물의 양식이 있습니다. |
| `reference_loop/loop.py` | 모델 요청, 도구 호출 묶음, 쓰기 승인, 실행 예산을 구현한 Python 참조 루프입니다. |
| `examples/support-desk/` | 라우터와 여섯 전문가가 있는 `app/`, 최종 구성 예시 `single_loop/`, 양쪽에 같은 과제를 넣는 `evals/`, 과거 변경의 결과와 diff가 있는 `example-run/`으로 구성됩니다. |

[파일별 역할](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/README.md#L73-L91) · [고객 지원 예제](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/examples/support-desk/README.md#L3-L19)

## 전환 절차는 어떤 근거로 서브에이전트를 남길지 정합니다

마이그레이션 스킬은 먼저 라우터와 전문가의 프롬프트, 도구, 호출 기록을 읽습니다. `coupling_map.py`는 호출을 트레이스 ID로 모아 시간순으로 정렬합니다. 각 트레이스에 어떤 전문가가 등장했고 어떤 두 전문가가 연달아 호출됐는지 집계합니다. 연속 호출 쌍을 평가할 때는 전체 트레이스에서 차지하는 비율과, 두 전문가 중 더 드문 쪽이 등장한 트레이스 가운데 해당 순서가 관찰된 비율을 함께 계산합니다. 호출 빈도와 결합 관계가 높을 때 병합을 검토할 근거가 생깁니다. [트레이스 집계](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/skill/scripts/coupling_map.py#L53-L110) · [전환 판단 기준](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/skill/steps/00-audit.md#L64-L105)

| 판단 | 역할을 옮기는 방식 |
| --- | --- |
| `fold` | 업무 절차는 필요할 때 읽는 스킬로 옮기고, 반품 정책처럼 강제해야 할 규칙은 도구 코드에 넣습니다. |
| `merge` | 함께 움직이는 두 전문가의 도구와 절차를 결합하고 라우터에서 한 대상으로 호출합니다. |
| `as-tool` | 별도 문맥에서 일하는 전문가를 유지합니다. 메인 에이전트가 도구를 통해 필수 입력을 보내고 구조화된 결과를 받아 대화를 이어갑니다. |
| `keep` | 외부 주체가 소유하거나 사용자와 직접 여러 차례 대화해야 하는 전문가는 대화 인계를 유지합니다. |

[판단표](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/skill/steps/00-audit.md#L63-L105) · [프롬프트 분해](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/skill/steps/03-fold.md#L22-L73) · [전문가 도구의 계약](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/skill/steps/04-as-tool.md#L20-L63)

기준선 평가는 기존 시스템으로 같은 입력을 반복 실행해 작업 완료율과 변동을 기록하는 단계입니다. 변경 후에도 답변과 실제 시스템 동작을 비교할 수 있도록, 특정 라우트의 선택 여부는 별도 진단 자료로 둡니다. `chain_coverage.py`는 운영 트레이스의 전문가 조합을 만들고, 평가 로그의 과제별 `by_agent` 집합에 그 조합이 포함되는지 봅니다. 같은 과제의 여러 반복에서 등장한 전문가가 합집합으로 모이고, 비교는 순서를 제외한 집합으로 이루어집니다. 그래서 이 도구가 과제를 찾으면 평가 정의와 트레이스를 열어 실제로 인계가 일어났는지, 마지막 행동과 전달해야 할 정보까지 채점했는지 확인하는 절차가 이어집니다. [평가 선택](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/skill/steps/01-baseline.md#L6-L23) · [조합 커버리지 구현](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/skill/scripts/chain_coverage.py#L42-L64) · [과제 대조와 한계](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/skill/scripts/chain_coverage.py#L87-L137)

검토를 멈추는 시점은 감사 후, 승인 범위에 없는 유료 평가 전, 기준선 평가 후, 각 변경의 평가 결과를 비교한 후입니다. 스킬 문서는 이 시점마다 확인을 받도록 안내하고, 채택한 직전 버전을 다음 비교의 기준으로 삼아 `single-loop/PLAN.md`에 변경과 결과를 남기도록 합니다. 마지막 정리 단계에서는 공용 프롬프트와 평가의 소유자, 업무별 스킬과 도구의 소유자를 정합니다. 이 확인 절차는 마이그레이션 작업의 진행을 다룹니다. 아래 실행 코드의 `approve` 콜백은 모델이 호출한 쓰기 도구 한 건의 실행을 판단합니다. [마이그레이션 절차와 확인](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/skill/SKILL.md#L29-L80) · [운영 소유권](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/skill/steps/05-upkeep.md#L39-L52) · [도구 실행 코드](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/reference_loop/loop.py#L180-L195)

## 참조 루프에서 한 요청이 처리되는 과정

`Agent`를 만들면 `load_skills`가 스킬 파일에서 이름과 설명을 읽습니다. 루프는 그 목록을 시스템 프롬프트에 넣고 `load_skill` 도구를 등록합니다. 모델이 특정 스킬의 이름을 골라 호출하면 도구가 파일 본문을 읽어 결과로 전달합니다. 스킬 파일의 실제 경로가 스킬 디렉터리 밖으로 해석되는지, 대소문자를 무시한 이름이 중복되는지도 초기화 때 검사합니다. 드물게 쓰는 도구는 `deferred`를 설정할 수 있습니다. 이 경우 API 요청의 도구 정의에 `defer_loading`을 넣고 서버의 도구 검색 정의를 함께 보냅니다. [스킬 목록 구성](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/reference_loop/loop.py#L79-L101) · [스킬 본문과 도구 정의](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/reference_loop/loop.py#L134-L165)

![메인 모델 호출에서 읽기·쓰기 도구의 배치 실행과 도구 결과 반환으로 이어지는 참조 루프]({{ '/img/reviews/2026/single-agent-loop-kit-review/agent-loop.svg' | relative_url }})

*그림 1. 리뷰어 작성, 분석 커밋 기준. 도구 호출 결과는 원래 호출 순서로 대화 이력에 추가됩니다. 최종 응답 경로에서는 호출자가 제공한 검증기를 적용할 수 있습니다.* [도구 배치](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/reference_loop/loop.py#L204-L219) · [메인 루프와 응답 처리](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/reference_loop/loop.py#L232-L282)

`Agent.run`은 사용자 메시지를 대화 이력에 추가하고 모델을 호출합니다. 같은 인스턴스에서 실행 중인 요청이 있으면 잠금으로 새 실행을 거부합니다. 모델이 도구를 요청하면 기본 16개까지만 실행 후보가 됩니다. 읽기는 최대 8개 워커에서 병렬로 실행하고, 이 작업이 끝난 뒤 쓰기는 호출 순서대로 실행합니다. 쓰기로 표시한 도구가 있으면 인스턴스를 만들 때 `approve`가 필요하고, 쓰기 호출마다 이름과 인자를 바탕으로 허용 여부를 결정합니다. 모델에는 호출 ID가 연결된 결과가 돌아갑니다. 한도를 넘긴 호출과 도구 예외도 해당 호출의 결과로 만들어 다음 모델 요청에 전달합니다. [예산과 초기화](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/reference_loop/loop.py#L49-L63) · [쓰기 콜백 요구](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/reference_loop/loop.py#L104-L133) · [도구 실행과 배치](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/reference_loop/loop.py#L180-L219) · [동시 실행 잠금](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/reference_loop/loop.py#L222-L235)

각 모델 응답의 토큰을 `charge`에 누적합니다. 도구가 서브에이전트를 실행한다면 도구 쪽에서도 해당 응답의 사용량을 `charge`에 전달할 수 있습니다. 고객 지원의 최종 구성은 이 연결을 실제로 설정하고, 전문가 루프는 사용량 콜백에서 예산 소진을 알렸을 때 추가 도구 실행을 멈춥니다. 예산 판단은 모델 응답이나 도구 실행 사이의 검사에 의존하며, 진행 중인 요청을 중단하는 기능은 이 루프에 없습니다. 답변 검증기를 제공한 경우 첫 불합격에는 수정 사유를 이력에 넣고, 두 번째 불합격이면 빈 응답과 `verify_failed` 상태를 돌려줍니다. [토큰 집계](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/reference_loop/loop.py#L168-L177) · [응답 처리와 종료 조건](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/reference_loop/loop.py#L238-L282) · [예제 사용량 연결](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/examples/support-desk/single_loop/agent.py#L93-L103) · [전문가 루프](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/examples/support-desk/app/subagents.py#L63-L76)

## 고객 지원 코드에서 달라지는 세 가지 경로

전환 전의 `Conversation`은 라우터 모델에게 `delegate`와 보험 청구 인계 도구를 제공합니다. `delegate` 호출은 대상 전문가와 요약을 확인한 뒤 `run_subagent`로 보냅니다. 전문가가 사용하는 새 메시지 목록은 이 요약으로 시작하고, 전문가가 반환한 텍스트가 라우터의 도구 결과가 됩니다. 전환 후 예시에서 메인 모델은 `track_order` 도구를 호출할 수 있습니다. 이 함수가 주문을 조회하고 운송장 번호가 있으면 배송 정보까지 읽어 한 결과에 담습니다. [라우터의 도구와 위임](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/examples/support-desk/app/orchestrator.py#L16-L46) · [라우터 대화 루프](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/examples/support-desk/app/orchestrator.py#L78-L109) · [주문·배송 조회](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/examples/support-desk/single_loop/agent.py#L109-L120)

- **반품은 스킬과 쓰기 도구로 옮깁니다.** 모델이 반품 절차를 읽고 `start_return`을 호출하면 함수가 먼저 해당 주문의 반품 자격을 확인합니다. 대상이 아니면 사유를 반환하고, 자격이 확인되면 반품을 생성합니다. 도구 정의는 `writes=True`로 등록됩니다. 세션에서 받은 고객 ID로 주문 소유권을 검사하는 `CustomerBackend`와 실행 직전의 승인 콜백이 각각 접근 범위와 쓰기 실행을 제어합니다. [반품과 도구 선언](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/examples/support-desk/single_loop/agent.py#L122-L130) · [쓰기 표시](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/examples/support-desk/single_loop/agent.py#L161-L185) · [세션 ID와 접근 검사](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/examples/support-desk/single_loop/customer.py#L20-L64)
- **기기 진단은 전문가 호출을 감싼 도구로 남깁니다.** `diagnose_device`가 일련번호를 필수 인자로 받고 기기 소유권을 확인한 뒤 전문가를 새 문맥으로 실행합니다. 메인에 돌아오는 결과에는 결론, 근거, 수행한 행동, 신뢰도, 유의사항이 들어갑니다. 검사 함수는 빈 응답을 예외로 처리하고, 구조가 어긋난 텍스트 응답은 신뢰도를 낮추고 유의사항을 붙여 전달합니다. [진단 도구](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/examples/support-desk/single_loop/agent.py#L142-L152) · [결과 형식 검사](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/examples/support-desk/single_loop/agent.py#L46-L73)
- **보험 청구는 고객 대화를 인계합니다.** `handoff_to_claims`는 로그인 상태를 확인하고 요약을 남깁니다. 메인 루프에서 돌아온 대화 객체는 이 요약과 현재 요청으로 `ClaimsSession`을 시작합니다. 이후 메시지는 청구 담당에게 가고, 세션 종료 시 담당자가 고객에게 전한 내용이 다음 메인 요청에 들어갑니다. 참조 예제 안의 청구 담당은 프로세스 내부에서 동작합니다. [인계 도구](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/examples/support-desk/single_loop/agent.py#L154-L159) · [인계와 복귀](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/examples/support-desk/single_loop/agent.py#L210-L235) · [청구 세션의 범위](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/examples/support-desk/app/subagents.py#L79-L112)

## 같은 과제로 평가하고 과제별 변화를 읽는 방법

`evals/run_eval.py`는 `--app`으로 선택한 모듈의 `new_conversation`을 호출합니다. 과제마다 새 메모리 백엔드와 사용량 계측기를 만들고, 지정된 고객과 대화 차례를 넘깁니다. 채점기는 답변의 필수·금지 표현, 실행해야 할 행동과 인자, 금지된 행동을 확인합니다. `only_expected_writes`가 있는 과제에서는 기대한 쓰기 외의 기록도 검사합니다. 성공 여부와 지연, 토큰, 모델 호출, `by_agent`, 상태 변경을 `results.jsonl`에 저장합니다. 실행 예외는 채점 행과 별도로 `errors.jsonl`에 기록합니다. [과제 실행과 채점](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/examples/support-desk/evals/run_eval.py#L43-L100) · [모듈 선택과 결과 기록](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/examples/support-desk/evals/run_eval.py#L133-L208)

`compare.py`는 두 버전이 공유하는 과제 ID를 골라, 과제마다 반복 점수를 평균 내고 다시 과제 간 평균을 냅니다. 지연과 토큰은 비교 대상의 실행 행에서 평균을 구합니다. 기준 버전에 채점 행이 있고 변경 버전에 하나도 없는 과제는 전체 평균을 내는 교집합에서 빠지지만, 최종 판정은 보류됩니다. 결과에는 전체 점수와 별도로 악화된 과제, 달라진 쓰기 행동, 전문가를 호출한 반복 비율이 나옵니다. 성공률이 비슷할 때도 어떤 경로가 움직였는지 확인할 수 있습니다. [평균 계산](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/skill/scripts/compare.py#L102-L121) · [쓰기와 경로 비교](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/skill/scripts/compare.py#L230-L250) · [판정](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/skill/scripts/compare.py#L272-L302) · [공통 과제 선택](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/skill/scripts/compare.py#L322-L352)

다음은 저장소에 보관된 `claude-opus-5` 실행 로그를 읽어 집계한 값입니다. 각 기록 안에서 기준선과 변경 버전을 비교했습니다. 두 날짜의 실행은 평가 과제 범위가 다릅니다. [반품 전환 기록의 실행 조건](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/examples/support-desk/example-run/README.md#L1-L26) · [진단 도구 전환 기록의 실행 조건](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/examples/support-desk/example-run/as-tool/README.md#L1-L29)

| 변경 | 비교 범위 | 기준선 통과 | 변경 후 통과 |
| --- | --- | ---: | ---: |
| 반품 전문가를 메인으로 전환 | 과제 12개, 각각 2회 | 22/24 | 23/24 |
| 진단 전문가를 도구로 호출 | 과제 17개, 각각 2회 | 32/34 | 31/34 |
| 진단 도구 전환 후 추가 비교 | `t01`과 `t10`을 각각 4회 추가 | 8/8 | 8/8 |

[반품 기준선](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/examples/support-desk/example-run/results/baseline/results.jsonl#L1-L24) · [반품 변경](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/examples/support-desk/example-run/results/v1/results.jsonl#L1-L24) · [진단 기준선](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/examples/support-desk/example-run/as-tool/results/baseline/results.jsonl#L1-L34) · [진단 변경](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/examples/support-desk/example-run/as-tool/results/v1/results.jsonl#L1-L34) · [추가 기준선](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/examples/support-desk/example-run/as-tool/results/baseline-t01-t10/results.jsonl#L1-L8) · [추가 변경](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/examples/support-desk/example-run/as-tool/results/v1-t01-t10/results.jsonl#L1-L8)

반품 전환 기록에서는 평균 지연이 27.31초에서 19.36초로, 평균 모델 호출이 6.33회에서 4.83회로 줄었습니다. 조건부 반품 과제 `t11`은 0/2에서 2/2로 바뀌었고, 주문 배송 상태를 묻는 `t01`은 2/2에서 1/2로 바뀌었습니다. 전체 성공 횟수의 증가는 서로 다른 두 과제의 변화가 합쳐진 결과입니다. 진단 도구 전환 기록에서는 `t01`의 한 번 실패가 추가 비교에서 반복되지 않았고, 작성자는 변경을 해당 브랜치에 남겼다고 기록했습니다. [반품 t01 기준선](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/examples/support-desk/example-run/results/baseline/results.jsonl#L1-L2) · [반품 t01 변경](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/examples/support-desk/example-run/results/v1/results.jsonl#L1-L2) · [반품 t11 기준선](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/examples/support-desk/example-run/results/baseline/results.jsonl#L21-L22) · [반품 t11 변경](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/examples/support-desk/example-run/results/v1/results.jsonl#L21-L22) · [진단 결과 확인](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/examples/support-desk/example-run/as-tool/README.md#L32-L56)

## 문서에 나온 실행 방법과 검증 범위

원문의 오프라인 점검은 Python 3.10 이상에서 고객 지원 예제 디렉터리로 이동해 키워드 규칙으로 동작하는 대체 모델을 선택합니다. 해당 모드도 결과 행을 남기지만 실행기는 최종 출력에서 모델 점수로 해석하지 말라고 안내합니다. 실제 모델 비교에 필요한 Anthropic SDK와 인증, `KIT_MODEL` 설정은 별도 절차로 설명되어 있습니다. [예제 실행 안내](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/examples/support-desk/RUNBOOK.md#L7-L41) · [대체 모델 모드 처리](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/examples/support-desk/evals/run_eval.py#L198-L229)

```bash
cd single-agent-loop-kit/examples/support-desk
KIT_MODEL=fake python3 evals/run_eval.py --variant smoke
```

공개 기록은 반품 전환과 진단 도구 전환을 각각 한 번 적용한 사례입니다. 반품 실행에는 금지된 반품과 `account → returns` 인계가 포함되지 않았고, 스킬을 끈 비교도 마치지 못했습니다. 진단 실행에는 일련번호가 다음 차례에 오는 과제와 존재하지 않는 일련번호 과제가 빠져 있습니다. 저장소는 병합·운영 정리 단계와 완성된 `single_loop/`도 실제 모델로 평가한 범위 밖이라고 명시합니다. 현재 참조 루프에 있는 쓰기 승인, 서브에이전트 토큰 계산과 검증기 동작은 과거 두 실험 뒤에 변경됐습니다. [반품 실행의 범위](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/examples/support-desk/example-run/README.md#L36-L57) · [진단 실행의 범위](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/examples/support-desk/example-run/as-tool/README.md#L53-L73) · [현재 구현의 검증 범위](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/README.md#L137-L160)

코드와 저장된 평가 기록을 정적으로 분석했습니다. 외부 보험사 API의 동작, 실제 모델에서 현재 커밋의 결과 재현, Claude Code 외부 플러그인의 동작은 이 리뷰의 검증 범위 밖입니다. 저장소는 Apache-2.0이며, 작성자는 유지보수와 기여 접수를 하지 않는 참조 구현으로 안내합니다. [외부 인계의 예제 범위](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/examples/support-desk/app/subagents.py#L79-L87) · [외부 도구 목록](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/README.md#L93-L107) · [라이선스](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/LICENSE) · [지원 정책](https://github.com/anthropics/single-agent-loop-kit/blob/c43796287b83bec847db923f07131d1cc8de750d/README.md#L162-L170)

## 요약

조건부 반품처럼 앞선 조회 결과가 다음 행동을 결정하는 요청은 전환 전후를 비교하기 좋은 과제입니다. 이 저장소의 평가 기록에서는 그런 과제의 개선과 인접 주문 과제의 악화가 함께 나타났습니다. 키트는 각 변경에서 이 차이를 남길 수 있도록 평가 입력과 채점 조건을 유지하고, 스킬로 옮긴 업무 절차와 도구에서 실행하는 규칙을 코드에서 확인할 수 있게 구성합니다.
