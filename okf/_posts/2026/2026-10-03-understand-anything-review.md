---
type: "Repo Review"
title: "[Repo Review] Understand Anything: 코드를 설명 가능한 지식 그래프로 바꾸는 분석 파이프라인"
description: "Understand Anything이 파일 스캔과 구조 추출, 모델의 의미 분석, 그래프 병합과 증분 검증을 거쳐 탐색용 대시보드로 연결되는 과정을 고정 커밋의 코드로 분석합니다."
date: "2026-10-03"
tags:
  - "Repo Review"
  - "AI Agent"
  - "Visualization"
  - "Tools"
resource: "https://github.com/Egonex-AI/Understand-Anything/tree/1d7418b8abfa543744ae029e63a482aee03f9022"
generated:
  by: "process:blog-review"
  at: "2026-10-03T06:09:00+09:00"
sources:
  - id: "Egonex-AI/Understand-Anything"
    resource: "https://github.com/Egonex-AI/Understand-Anything/tree/1d7418b8abfa543744ae029e63a482aee03f9022"
    title: "Understand Anything"
status: "stable"
year: "2026"
analyzed_at: "2026-10-03T06:09:00+09:00"
source_id: "Egonex-AI/Understand-Anything"
source_revision: "1d7418b8abfa543744ae029e63a482aee03f9022"
source_type: "repo"
source_url: "https://github.com/Egonex-AI/Understand-Anything/tree/1d7418b8abfa543744ae029e63a482aee03f9022"
visual_sources:
  - path: "/img/reviews/2026/understand-anything-review/pipeline.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/skills/understand/SKILL.md#L259-L840"
    caption: "리뷰어 작성, 분석 커밋 기준. 스킬의 조정 절차와 정적 도우미·모델 해석·그래프 소비 경계를 요약했습니다."
---

## 들어가며

처음 보는 저장소에서 어려운 일은 파일을 여는 것보다 **어떤 파일부터 읽고, 어느 관계를 따라가야 하는지 정하는 일**입니다. Understand Anything은 소스와 문서를 분석해 파일·함수·클래스의 관계를 지식 그래프로 저장하고, 설명과 학습 순서를 붙여 대시보드에서 탐색하도록 만드는 프로젝트입니다. README는 코드베이스뿐 아니라 지식 문서와 비즈니스 도메인까지 다루는 도구로 소개합니다. 이 리뷰는 그중 `/understand`가 코드베이스를 그래프로 바꾸는 경로에 집중합니다. [README](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/README.md#L49-L78)

분석 기준은 `Egonex-AI/Understand-Anything`의 커밋 `1d7418b8abfa543744ae029e63a482aee03f9022`입니다. 소스, 매니페스트, 스킬 문서를 읽은 정적 분석이며 대상 프로젝트의 설치·실행·빌드·테스트는 수행하지 않았습니다. 아래에서 “스킬은 지시합니다”는 모델에게 주어진 작업 절차, “코드는 처리합니다”는 실제 구현에서 확인한 동작을 뜻합니다. 두 층을 구분해야 이 도구가 제공하는 보장 범위를 이해할 수 있습니다.

## 무엇을 만드는 도구인가

핵심 산출물은 프로젝트의 `.ua/knowledge-graph.json`입니다. 기존 `.understand-anything/` 디렉터리가 있으면 그 경로를 계속 사용하는 호환 규칙이 있습니다. 그래프는 검색용 텍스트만 모은 문서가 아니라, 설명을 담은 노드와 종류·방향을 가진 간선, 노드를 묶는 계층, 읽는 순서를 안내하는 투어를 함께 담습니다. [데이터 디렉터리 규칙](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/skills/understand/SKILL.md#L124-L128), [자료형](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/packages/core/src/types.ts#L54-L115)

| 구성 | 담는 정보 | 독자가 얻는 것 |
| --- | --- | --- |
| `nodes` | ID, 종류, 이름, 파일 경로·행 범위, 설명, 태그, 복잡도 | 코드 위치와 역할을 연결합니다. |
| `edges` | 출발·도착 ID, 관계 종류, 방향, 가중치 | 포함·호출·의존 등 관계를 따라갑니다. |
| `layers` | 이름, 설명, 소속 노드 ID | 아키텍처 단위로 묶어 봅니다. |
| `tour` | 순서, 제목, 설명, 관련 노드 ID | 처음 읽을 때의 학습 동선을 제공합니다. |
| `project` | 프로젝트 정보, 분석 시각, Git 커밋 | 결과가 어느 소스 시점을 설명하는지 확인합니다. |

파일·함수·클래스 외에도 설정, 문서, 서비스, 파이프라인 등의 노드가 정의되어 있습니다. 예를 들어 배포 설정과 소스가 같은 그래프 안에 들어올 수 있는 구조입니다. 다만 자료형이 존재한다는 사실만으로 모든 언어·프레임워크에서 정확한 관계가 만들어진다고 단정할 수는 없습니다. [노드·간선 종류](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/packages/core/src/types.ts#L1-L21)

## 아키텍처: 작업 절차와 실행 코드 사이의 경계

사용자가 실행하는 `/understand`의 주 진입점은 `skills/understand/SKILL.md`에 서술된 절차입니다. 코딩 에이전트가 이 절차를 읽고 스캐너와 파일 분석 에이전트를 호출하며, Node.js·Python 도우미가 중간 JSON을 생성합니다. 따라서 스킬에 적힌 모든 단계가 하나의 애플리케이션 함수 호출로 강제되는 것은 아닙니다. 전체 경로를 이해할 때는 프롬프트의 요구사항과 도우미의 실제 검사를 함께 봐야 합니다. [분석 진입점](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/skills/understand/SKILL.md#L43-L45), [배치 분석 지시](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/skills/understand/SKILL.md#L333-L381)

| 경로 | 책임 | 성격 |
| --- | --- | --- |
| `skills/understand/` | 스캔, 배치 계획, 추출, 병합, 증분 갱신 | 스킬 문서와 실행 스크립트가 공존합니다. |
| `agents/` | 프로젝트 개요, 파일 의미, 아키텍처, 투어 작성 지침 | 모델의 작업 규약입니다. |
| `packages/core/` | 파서 레지스트리, 자료형, 검증, 검색, 구조 지문 | TypeScript 공용 라이브러리입니다. |
| `packages/dashboard/` | JSON 로딩, 탐색 상태, 그래프 배치·표시 | React·Zustand·React Flow 기반 UI입니다. |
| `packages/viewer/` | 미리 빌드된 UI와 그래프를 제공하는 서버 | 독립 읽기 전용 뷰어입니다. |

`pnpm-workspace.yaml`은 플러그인의 여러 패키지와 홈페이지를 묶습니다. core의 매니페스트에는 Tree-sitter 관련 문법, `web-tree-sitter`, Zod, Fuse.js가 있고 dashboard에는 React, Zustand, React Flow, ELK 등이 있습니다. 의존성 목록과 실제 사용 경로를 대조하면 구문 추출, 데이터 검증, 검색, 그래프 표시가 서로 다른 책임으로 나뉘어 있음을 알 수 있습니다. [워크스페이스](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/pnpm-workspace.yaml#L1-L4), [core 매니페스트](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/packages/core/package.json#L1-L64), [dashboard 매니페스트](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/packages/dashboard/package.json#L1-L44)

![분석 에이전트와 결정적 도우미를 거쳐 지식 그래프와 대시보드로 이어지는 흐름]({{ '/img/reviews/2026/understand-anything-review/pipeline.svg' | relative_url }})

그림 1. 리뷰어 작성, 분석 커밋 기준. 실선은 주요 데이터 흐름이며, 파란 상자는 실행 도우미, 보라색 상자는 모델이 담당하는 의미 분석입니다. [스캐너 역할 분담](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/agents/project-scanner.md#L15-L27), [추출 호출](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/skills/understand/extract-structure.mjs#L79-L150), [병합](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/skills/understand/merge-batch-graphs.py#L808-L936), [UI 로딩](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/packages/dashboard/src/App.tsx#L144-L194)을 바탕으로 재구성했습니다.

## 작동 원리: 입력에서 화면까지

### 1. 분석 대상과 이전 결과를 먼저 결정합니다

스킬의 사전 준비 단계는 디렉터리 인수를 프로젝트 루트로 해석하고, 기존 그래프·`meta.json`·Git 커밋을 확인하도록 지시합니다. `--full`이 있거나 이전 그래프·메타데이터가 없으면 전체 분석을 택합니다. 기존 그래프가 있으면 변경 여부와 제외 규칙에 따라 증분 준비 도우미로 넘어갑니다. 커밋이 같아도 명시적 `--exclude`가 있으면 현재 파일 목록을 다시 대조한다는 점이 중요합니다. 파일을 분석 대상에서 제외하는 일도 기존 결과를 바꾸기 때문입니다. [분기표](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/skills/understand/SKILL.md#L180-L226)

작업 디렉터리에도 주의할 부분이 있습니다. 스킬은 Git worktree를 감지하면 기본적으로 메인 저장소 루트로 `PROJECT_ROOT` 자체를 바꾸도록 지시합니다. 이는 임시 worktree가 사라질 때 산출물이 유실되는 문제를 피하려는 절차이며, worktree의 미커밋 상태를 그대로 분석하려는 목적과는 구별해야 합니다. 스킬에는 이를 끄는 `UNDERSTAND_NO_WORKTREE_REDIRECT=1`도 기록되어 있습니다. [worktree 처리](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/skills/understand/SKILL.md#L47-L73)

### 2. 스캔은 모델의 설명과 결정적 파일 목록을 합칩니다

`project-scanner`의 역할은 두 가지로 나뉩니다. README와 매니페스트에서 프로젝트 이름·설명·프레임워크 맥락을 읽는 일은 모델에게 맡깁니다. 파일 열거, 언어·분류·행 수 판정, 제외 규칙 적용과 import 해석은 번들 스크립트를 호출하도록 명시합니다. 이렇게 나눈 결과가 후속 단계의 `scan-result.json`입니다. [스캐너 정의](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/agents/project-scanner.md#L15-L55)

`scan-project.mjs`는 Git 저장소에서 `git ls-files -z -co --exclude-standard`를 우선 사용하고 실패하면 재귀 순회로 대체합니다. `-z`는 파일명을 NUL로 구분하므로 공백이나 비ASCII 파일명을 줄 단위 텍스트로 오인하는 문제를 줄입니다. 그다음 기본 제외 규칙, 사용자 `.understandignore`, CLI 제외 패턴을 합친 필터를 적용하고, 경로를 안정적으로 정렬한 뒤 파일을 읽습니다. 읽기 실패 파일은 경고와 함께 빠질 수 있으므로 완료 표시만으로 모든 파일이 포함되었다고 볼 수는 없습니다. [파일 열거](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/skills/understand/scan-project.mjs#L482-L586), [필터와 정렬](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/skills/understand/scan-project.mjs#L761-L805)

`extract-import-map.mjs`는 파서가 추출한 import를 언어별 규칙으로 실제 프로젝트 내부 경로에 대응시킵니다. 최종 결과에 넣는 경로는 현재 파일 집합에 존재하는지 검사하며, Ruby용 분기와 Tree-sitter가 놓치는 일부 import를 보완하는 분기도 있습니다. 따라서 `importMap`은 외부 패키지 전체의 의존성 목록이 아니라 **현재 프로젝트 내부에서 해석한 파일 간 관계**입니다. [import 처리 루프](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/skills/understand/extract-import-map.mjs#L2062-L2129)

### 3. import 그래프를 모델이 읽을 배치로 나눕니다

`compute-batches.mjs`는 코드 파일을 노드, import 관계를 연결로 삼은 무방향 그래프를 만듭니다. 이 그래프에 Louvain 커뮤니티 탐지를 적용합니다. Louvain은 서로 연결이 많은 노드를 묶는 방법이며, 여기서는 관련 파일을 같은 분석 문맥에 넣기 위한 수단입니다. 최종 지식 그래프의 관계 방향을 버리는 것이 아니라 **배치를 정하는 단계에서만** 무방향 연결을 사용합니다. [배치용 그래프 생성](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/skills/understand/compute-batches.mjs#L291-L308)

배치 설계에는 명시적인 상한과 대체 경로가 있습니다. 커뮤니티가 35개 파일을 넘으면 이름순으로 분할하고, Louvain 실패 시에는 12개 파일씩 묶습니다. 작은 묶음은 합칠 수 있지만 Dockerfile 주변 파일, CI 설정, SQL 마이그레이션 같은 비코드 그룹에는 경계를 보존하는 규칙이 있습니다. 이 숫자는 성능 평가 결과가 아니라 해당 커밋의 구현 상수입니다. [크기 제한과 실패 처리](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/skills/understand/compute-batches.mjs#L464-L546), [비코드 배치](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/skills/understand/compute-batches.mjs#L137-L210)

배치를 나누면 다른 배치의 함수나 파일을 놓칠 수 있습니다. 이를 보완하는 것이 `neighborMap`입니다. 각 분석 파일에 대해 import하는 파일과 자신을 import하는 파일을 모으고, 배치 밖 이웃의 경로·배치 번호·export된 심볼 이름을 제공합니다. 이웃이 많은 경우 연결 수를 기준으로 최대 50개를 남깁니다. 모델은 이 문맥을 이용해 배치 밖으로 이어지는 간선을 작성하지만, 문맥이 제한되어 있다는 사실은 남습니다. [이웃 구성](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/skills/understand/compute-batches.mjs#L549-L615)

### 4. 구문 추출 결과에 의미를 붙입니다

파일 분석 에이전트는 배치 파일 목록을 `extract-structure.mjs`에 전달합니다. 이 스크립트는 Tree-sitter 플러그인과 비코드 파서를 `PluginRegistry`에 등록합니다. 레지스트리는 파일의 언어에 맞는 플러그인을 찾아 공통 `analyzeFile` 인터페이스로 호출합니다. Tree-sitter는 소스의 구문 구조를 읽는 파서이며, 이 단계는 프로그램을 실행해서 호출 관계를 관찰하는 동적 분석이 아닙니다. [추출 초기화](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/skills/understand/extract-structure.mjs#L79-L87), [레지스트리 구현](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/packages/core/src/plugins/registry.ts#L39-L85)

실제 추출 루프는 다음과 같이 결과와 실패 상태를 함께 전달합니다. 아래는 원문의 연속된 부분입니다.

```javascript
const { analysis, callGraph, structureOutcome, callGraphOutcome } =
  analyzeFileWithOutcomes(registry, file, content);

if (structureOutcome === 'skipped') {
  filesSkipped.push(file.path);
  continue;
}

analysisOutcomes.structure[structureOutcome] += 1;
analysisOutcomes.callGraph[callGraphOutcome] += 1;
```

출처: [extract-structure.mjs 124–133행](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/skills/understand/extract-structure.mjs#L124-L133). 파서 미지원과 파일 읽기 실패도 구분합니다. 모든 배치 파일을 읽지 못하면 결과 파일을 작성한 뒤에도 오류를 던지도록 되어 있습니다. `scriptCompleted` 한 필드만으로 성공을 판단하기 어려운 이유입니다. [출력과 실패 처리](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/skills/understand/extract-structure.mjs#L140-L172)

이후 모델은 추출 결과에 파일의 목적, 태그, 복잡도, 의미 관계를 붙입니다. 여기서 README의 “모든 함수·클래스”라는 소개와 실제 작업 규약의 차이가 나타납니다. 파일 분석 지침은 함수·메서드 10행 이상, 클래스의 메서드 2개 이상 또는 20행 이상, 혹은 외부에 export된 함수·클래스 등을 중요한 심볼로 선별합니다. 따라서 전체 심볼 색인이라기보다 **코드 이해에 필요한 대표 구조를 설명하는 그래프**에 가깝습니다. 증분 갱신에서는 기존 그래프에 있던 심볼이 여전히 존재하면 이 중요도 필터보다 보존 규칙을 우선합니다. [의미 분석 지시](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/agents/file-analyzer.md#L148-L192), [중요도와 보존 규칙](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/agents/file-analyzer.md#L241-L254)

### 5. 병합은 모델이 만든 관계를 정리하고 일부 누락을 복구합니다

`merge-batch-graphs.py`는 배치들의 노드와 간선을 합친 다음 ID와 복잡도를 정규화합니다. 바뀐 ID를 간선의 출발·도착에도 반영하고, 같은 ID의 노드는 마지막 값을 남깁니다. 간선 중복 판정에는 출발·도착·관계 종류뿐 아니라 방향도 포함하며, 같은 키에서는 더 큰 가중치의 간선을 남깁니다. 연결 대상 노드가 없는 간선은 진단을 남기고 제거합니다. [병합 구현](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/skills/understand/merge-batch-graphs.py#L823-L936)

특히 눈여겨볼 부분은 `recover_imports_from_scan`입니다. 배치 출력에서 빠진 import 간선을 원래 `scan-result.json`의 `importMap`과 대조해 다시 넣습니다. 이때 양쪽 경로에 대응하는 파일 수준 노드가 있어야 하며, 복구된 간선에는 `recoveredFromImportMap: True`를 붙입니다. 정적 도우미가 확보한 사실을 모델이 모두 재출력하리라고 가정하지 않는 설계입니다. [복구 구현](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/skills/understand/merge-batch-graphs.py#L1066-L1149)

```python
assembled["edges"].append({
    "source": src_id,
    "target": tgt_id,
    "type": "imports",
    "direction": "forward",
    "weight": 0.7,
    "recoveredFromImportMap": True,
})
```

출처: [merge-batch-graphs.py 1123–1130행](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/skills/understand/merge-batch-graphs.py#L1123-L1130). `0.7`은 코드가 부여하는 가중치이며, 관측으로 보정된 정답 확률이라는 근거는 이 부분에 없습니다. 또한 이 복구는 import 관계에 대한 장치이지, 모델이 작성하는 모든 `calls`·`related` 관계를 완전하게 복원하는 장치는 아닙니다.

### 6. 아키텍처와 투어를 합쳐 최종 산출물을 만듭니다

스킬은 병합 결과에서 파일 수준 노드와 import 간선 등을 추려 `architecture-analyzer`에 전달하고 `layers.json`을 작성하도록 지시합니다. `tour-builder`에는 README 일부, 프로젝트 진입점, 파일 수준 노드 등의 문맥을 전달해 `tour.json`을 만들도록 합니다. 이 두 결과는 구문 파싱 결과와 달리 모델의 해석·설명 층입니다. [아키텍처 단계](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/skills/understand/SKILL.md#L470-L510), [투어 단계](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/skills/understand/SKILL.md#L555-L586)

전체 분석 경로는 `project`, `nodes`, `edges`, `layers`, `tour`를 합친 뒤 검토·저장을 진행하도록 정의됩니다. 기본 검토는 스킬에 포함된 결정적 검증 코드이며, `--review`는 별도 LLM 검토 경로입니다. 저장 후에는 후속 증분 분석의 기준이 될 구조 지문을 생성하고, 그 성공을 확인한 다음 `meta.json`에 분석 커밋을 기록하도록 지시합니다. 이 순서는 실패한 분석을 최신 기준으로 표시하지 않기 위한 것입니다. [최종 조립과 검토 분기](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/skills/understand/SKILL.md#L643-L686), [저장 순서](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/skills/understand/SKILL.md#L807-L840)

### 7. 증분 갱신에서는 무엇이 달라졌는지와 무엇이 사라졌는지를 구분합니다

`prepare-incremental.mjs`는 이전 커밋과 현재 커밋의 차이, 현재 제외 규칙을 적용한 파일 목록, 구조 지문을 대조해 갱신 계획을 씁니다. 구조 지문은 파일 내용 해시뿐 아니라 함수 이름·인수·반환형·export 여부·행 수, 클래스 구성, import와 export를 담은 요약입니다. 전체 내용을 모델에 다시 보내기 전에 비교할 수 있는 기준을 만드는 셈입니다. [준비 도우미](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/skills/understand/prepare-incremental.mjs#L1-L20), [구조 지문 생성](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/packages/core/src/fingerprint.ts#L89-L132)

`classifyUpdate`의 분기는 다음 순서입니다. 구조 변경 수에는 수정뿐 아니라 추가·삭제 파일도 포함합니다. [분류 구현](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/packages/core/src/change-classifier.ts#L21-L92)

| 우선순위 | 조건 | 결정 |
| --- | --- | --- |
| 1 | 구조 변경 수가 0 | `SKIP` |
| 2 | 구조 변경 수가 30 초과 또는 기존 그래프 파일 수의 50% 초과 | `FULL_UPDATE` |
| 3 | 상위 디렉터리 구성 변경 또는 구조 변경 수가 10 초과 | `ARCHITECTURE_UPDATE` |
| 4 | 나머지 국소적 구조 변경 | `PARTIAL_UPDATE` |

부분 갱신에서는 파일 의미만 다시 분석하고, 기존 계층 배치를 가능한 한 보존하며 투어 문장을 재작성하지 않는 절차를 택합니다. 삭제된 파일은 모델에 다시 보낼 대상이 아니라 기존 결과에서 정리할 대상입니다. 반면 아키텍처 갱신에서는 계층과 투어를 다시 작성하도록 지시합니다. [갱신 경로](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/skills/understand/SKILL.md#L217-L226), [부분 갱신의 계층·투어 처리](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/skills/understand/SKILL.md#L470-L472)

여기에 심볼 손실을 막는 별도 관문이 있습니다. 재분석 파일에 있던 함수·클래스·메서드가 새 그래프에서 사라지면 원본 소스의 삭제인지, 모델의 누락인지 판정하도록 합니다. 스킬은 해결되지 않은 파일에 대해 한 번의 표적 재시도를 허용하며, 최종 저장 도우미는 **실제로 저장할 그래프**를 다시 검사합니다. 아래 코드에서 검사에 실패하면 그래프 저장 이후 단계로 넘어가지 않습니다. [재시도 계약](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/skills/understand/SKILL.md#L413-L435)

```javascript
const symbolReport = await validateIncrementalSymbols(projectRoot, { graph, intermediateDir });
process.stderr.write(`${formatSymbolReport(symbolReport)}\n`);
if (!symbolReport.ok) throw new Error('Unresolved incremental symbol loss; baseline not advanced');
atomicWriteJson(graphPath, graph);
```

출처: [finalize-incremental.mjs 475–478행](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/skills/understand/finalize-incremental.mjs#L475-L478). 그 뒤 지문을 갱신하고 `meta.json`을 전진시킵니다. 이는 순서를 지킨 개별 파일 저장이며, 여러 산출물이 하나의 데이터베이스 트랜잭션으로 일괄 교체된다고 해석해서는 안 됩니다. [후속 저장](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/skills/understand/finalize-incremental.mjs#L481-L482)

구조 지문에도 중요한 한계가 있습니다. `COSMETIC`은 단순 공백 수정만 의미하지 않습니다. 내용 해시는 달라도 비교하는 구조 정보가 그대로이면 코드가 `internal logic changed (no structural impact)`로 분류합니다. 함수의 외형을 유지한 내부 로직 변경은 의미 설명이 달라져야 하더라도 재분석에서 빠질 가능성이 있습니다. 이는 해당 비교 규칙에서 도출되는 제한이며, 실제 프로젝트에서의 누락 빈도를 측정한 결과는 아닙니다. [비교 조건](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/packages/core/src/fingerprint.ts#L195-L215), [COSMETIC 반환](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/packages/core/src/fingerprint.ts#L248-L273)

### 8. UI는 저장된 그래프를 읽고 다시 검증합니다

`/understand-dashboard` 스킬은 설치된 플러그인 버전에 대응하는 미리 빌드된 viewer를 먼저 시도하고, 실패하면 core 빌드와 Vite 서버 경로로 대체하도록 정의되어 있습니다. viewer는 그래프 생성과 분리된 읽기 전용 실행물입니다. 실제 viewer 서버에는 데이터 요청의 토큰 검사와 `127.0.0.1` 바인딩이 있습니다. 이것이 분석 단계의 모델 호출을 로컬로 바꾸는 것은 아닙니다. [대시보드 시작 절차](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/skills/understand-dashboard/SKILL.md#L103-L139), [viewer 서버](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/packages/viewer/bin/viewer.mjs#L319-L391)

브라우저의 `App.tsx`는 `knowledge-graph.json`을 fetch하고 HTTP 상태를 확인한 뒤 `validateGraph`에 전달합니다. 검증기는 정리, 타입 별칭 정규화, 기본값 보정과 개별 데이터 검사를 수행하며 잘못된 프로젝트 메타데이터 등은 치명적 오류로 처리합니다. 성공한 데이터는 Zustand 저장소의 `setGraph`로 들어가 노드 ID·계층 조회용 Map과 검색 엔진을 만듭니다. [UI 로딩](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/packages/dashboard/src/App.tsx#L144-L194), [검증기](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/packages/core/src/schema.ts#L563-L607), [상태 구성](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/packages/dashboard/src/store.ts#L366-L385)

표시 단계의 `GraphView`는 전체 계층 개요와 계층 내부 상세를 나누고 ELK 배치를 사용합니다. 컨테이너를 펼칠 때 내부 배치를 계산하는 경로도 분리되어 있습니다. 이는 분석에서 만든 그래프를 그대로 한꺼번에 펼쳐 보이는 대신, 현재 탐색 수준에 맞춰 구조를 드러내는 UI 설계입니다. 다만 이번 리뷰는 레이아웃 성능이나 대규모 그래프에서의 응답성을 측정하지 않았습니다. [개요 배치](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/packages/dashboard/src/components/GraphView.tsx#L246-L356), [상세 배치](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/packages/dashboard/src/components/GraphView.tsx#L679-L843)

검색 경로는 README와 비교해서 읽을 필요가 있습니다. README에는 퍼지·의미 검색이 소개되지만, 현재 dashboard의 `setSearchQuery`는 두 모드 모두 동일한 `SearchEngine.search`를 호출합니다. core의 이 엔진은 Fuse.js로 이름·태그·설명·언어 노트를 검색합니다. “설명 텍스트를 검색한다”와 “임베딩으로 의미 검색한다”는 다른 동작입니다. [README의 검색 소개](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/README.md#L85-L88), [실제 모드 처리](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/packages/dashboard/src/store.ts#L532-L544), [Fuse.js 설정](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/packages/core/src/search.ts#L14-L58)

`/understand-chat` 역시 별도 스킬입니다. 저장된 그래프에서 관련 노드를 검색하고 연결된 간선과 계층을 읽어 모델이 답하도록 지시합니다. 이를 대시보드의 검색 엔진이나 독립적인 서버 추론 API와 혼동하지 않는 것이 좋습니다. [질의응답 절차](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/skills/understand-chat/SKILL.md#L51-L70)

## 설치와 사용: 문서에 기록된 경로

README의 Claude Code 설치·기본 사용 명령은 다음과 같습니다. 터미널 셸 명령이 아니라 해당 코딩 도구 안에서 사용하는 슬래시 명령입니다. 이 리뷰에서 실행하거나 성공 여부를 확인한 명령은 아닙니다. [README Quick Start](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/README.md#L118-L166)

```text
/plugin marketplace add Egonex-AI/Understand-Anything
/plugin install understand-anything
/understand
/understand-dashboard
```

한국어 설명을 지정하는 옵션은 스킬의 `--language <lang>` 계약과 README의 언어 목록에 포함됩니다. README는 첫 전체 분석이 많은 토큰을 사용할 수 있다고 안내하며, 이후 실행은 기본적으로 증분 분석을 사용한다고 설명합니다. 실제 비용은 파일 범위, 모델, 재시도와 갱신 분기에 따라 달라지므로 절감률을 일반화할 근거는 이번 분석에 없습니다. [언어·토큰 안내](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/README.md#L136-L157)

전체 파이프라인의 준비 단계는 Node.js 22 이상과 pnpm 10 이상을 요구하는 안내를 포함합니다. 독립 viewer 매니페스트의 Node.js 18 이상 요구사항은 이미 생성된 그래프를 보는 실행물의 조건이므로, 분석 전체의 요구사항과 구분해야 합니다. [분석 사전 준비](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/skills/understand/SKILL.md#L117-L122), [viewer 매니페스트](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/packages/viewer/package.json#L1-L27)

## 한계와 읽을 때의 주의점

이 구조에서 코드가 보장하려는 것은 주로 산출물의 형태와 연결의 일관성입니다. 노드 ID를 바로잡고, 존재하지 않는 끝점을 제거하고, import 누락을 복구하거나 심볼 손실을 막는 검사는 유용합니다. 그러나 모델이 쓴 함수 설명, 아키텍처 계층 이름, 의미 관계가 실제 의도를 정확히 반영하는지는 다른 문제입니다. 형식 검증을 통과한 그래프를 소스의 의미까지 검증한 결과로 받아들여서는 안 됩니다. [병합 검사](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/skills/understand/merge-batch-graphs.py#L833-L936), [의미 분석 책임](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/understand-anything-plugin/agents/file-analyzer.md#L148-L192)

README의 폭넓은 기능 소개는 특정 사용 경로에서 다시 확인해야 합니다. 이번 커밋에서 확인한 대표적인 경계는 중요도 필터가 있는 함수·클래스 노드, 최대 이웃 수를 제한하는 배치 문맥, 퍼지 엔진을 사용하는 의미 검색 모드, 내부 로직 변경을 재분석하지 않을 수 있는 구조 지문입니다. 이들은 각각 그래프의 범위, 배치 간 연결 정보, 검색 방식, 설명의 최신성에 영향을 줍니다.

라이선스는 MIT이며 저작권·허가 문구 유지와 무보증 조항을 명시합니다. 이 리뷰는 정적 구현 분석이고, 추출 정확도·토큰 사용량·벤치마크 수치·플랫폼별 설치 호환성은 검증하지 않았습니다. [LICENSE](https://github.com/Egonex-AI/Understand-Anything/blob/1d7418b8abfa543744ae029e63a482aee03f9022/LICENSE#L1-L22)

## 결론

Understand Anything의 학습 가치는 LLM의 설명 능력과 결정적 처리의 경계를 구체적으로 보여 준다는 데 있습니다. 파일 목록과 import 관계를 먼저 확보하고, 관계를 고려해 문맥을 나누며, 모델이 작성한 그래프를 정규화하고 검증한 뒤 탐색 UI에 전달합니다. 특히 import 복구와 증분 심볼 보존은 “생성된 결과를 그대로 신뢰하지 않는다”는 설계를 코드로 드러냅니다. 동시에 그래프가 구조를 보존하는 것과 의미를 정확하게 설명하는 것은 별도의 과제라는 점도 분명합니다.

### 이 글에서 다루지 못한 부분

지식 베이스 분석, 비즈니스 도메인 추출, Figma 연동, diff 영향 분석, 자동 갱신 훅, 플랫폼별 설치기 전체와 언어별 파서의 모든 규칙은 심층 분석하지 않았습니다. 그래프 시각화도 로딩·상태·주요 배치 경로까지만 추적했으며, 개별 렌더링 최적화나 브라우저 실행 결과까지 검증하지 않았습니다.
