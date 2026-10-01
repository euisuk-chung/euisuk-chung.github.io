---
type: "Repo Review"
title: "[Repo Review] OpenResearch: Git 스냅샷으로 연구 에이전트의 실험을 추적하는 작업 공간"
description: "OpenResearch의 실험 브랜치 생성부터 커밋 아카이브, 로컬 실행과 로그 저장까지 추적하며 소스 재현성과 실행 환경의 경계를 살펴봅니다."
date: "2026-09-29"
tags:
  - "Repo Review"
  - "AI Agent"
  - "Git"
  - "Tools"
resource: "https://github.com/alphaXiv/OpenResearch/tree/c95be22a35ca91057d61e3e6fde31d69c9af27f6"
generated:
  by: "process:blog-review"
  at: "2026-09-29T06:09:00+09:00"
sources:
  - id: "alphaXiv/OpenResearch"
    resource: "https://github.com/alphaXiv/OpenResearch/tree/c95be22a35ca91057d61e3e6fde31d69c9af27f6"
    title: "OpenResearch"
status: "stable"
year: "2026"
analyzed_at: "2026-09-29T06:09:00+09:00"
source_id: "alphaXiv/OpenResearch"
source_revision: "c95be22a35ca91057d61e3e6fde31d69c9af27f6"
source_type: "repo"
source_url: "https://github.com/alphaXiv/OpenResearch/tree/c95be22a35ca91057d61e3e6fde31d69c9af27f6"
visual_sources:
  - path: "/img/reviews/2026/openresearch-review/execution-flow.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/compute.rs#L727-L798"
    caption: "리뷰어 작성, 분석 커밋 기준. CLI·API에서 스냅샷 생성과 로컬 실행·감독·저장으로 이어지는 흐름."
---

## 들어가며

연구 에이전트가 코드를 수정하고 실험을 실행하기 시작하면, 대화 내용만으로는 결과의 출처를 따라가기 어렵습니다. 어느 가설에서 갈라진 코드인지, 실제 실행한 커밋은 무엇인지, 실행 중에 에이전트가 파일을 다시 고치지는 않았는지까지 연결해야 합니다. OpenResearch는 이 문제를 **에이전트 세션, Git 기반 실험 계보, 실행 기록을 한 작업 공간에서 연결하는 방식**으로 다룹니다.

README는 OpenResearch를 로컬 우선 연구 에이전트 작업 공간으로 소개하며, 문헌 검토부터 가설 작성·실험·산출물 생성까지의 자율 연구를 목표로 제시합니다. 이 글은 그 전체 능력을 실험으로 평가하지 않습니다. 분석 커밋 `c95be22a35ca91057d61e3e6fde31d69c9af27f6`에서 **실험 생성 → 소스 스냅샷 → 로컬 실행 → 로그와 상태 저장** 경로를 중심으로 정적으로 추적합니다. 의존성 설치, 빌드, 테스트 및 대상 코드 실행은 하지 않았습니다. [README의 기능 설명](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/README.md#L64-L82)

## OpenResearch는 무엇인가

OpenResearch는 기존 코딩 에이전트와 여러 실행 환경을 연결하고, 연구 과정의 코드·대화·실행 기록을 로컬에서 관리하는 애플리케이션입니다. Rust 패키지 이름은 `openresearch-cli`, 버전은 분석 시점의 매니페스트 기준 `0.2.11`이며, 실행 파일 이름은 `orx`입니다. 화면은 별도의 React 애플리케이션으로 구성됩니다. Rust 쪽에는 비동기 실행을 위한 Tokio, 명령행 파서를 위한 clap, HTTP 라우팅을 위한 Axum, SQLite 접근을 위한 rusqlite가 들어 있습니다. [Cargo.toml](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/Cargo.toml#L1-L57), [UI 매니페스트](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/ui/package.json#L1-L54)

여기서 에이전트와 계산 환경은 다른 축입니다. 에이전트는 무엇을 수정하고 다음에 무엇을 시도할지 결정하는 대화 실행기이고, 계산 환경은 실험 명령을 실제로 실행하는 곳입니다. `Harness`라는 공통 인터페이스는 설치 상태 탐지와 대화 턴 실행을 분리하며, 등록 목록에는 Claude Code·Codex·OpenCode·Cursor·Antigravity가 있습니다. 계산 쪽은 별도의 `compute` 계층에서 로컬·SSH·Slurm·Ray 등의 제출 경로를 선택합니다. 여러 이름이 등록되어 있다는 사실과 모든 조합의 실제 동작을 검증했다는 주장은 구별해야 합니다. [Harness 인터페이스](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/local/harness/mod.rs#L253-L299), [등록 목록](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/local/harness/mod.rs#L512-L519), [계산 환경 분기](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/plane/local_plane.rs#L254-L270)

## 아키텍처: 대화, 실험, 실행을 나누는 경계

코드를 읽을 때 `project`, `experiment`, `run`, `session`을 구분하면 구조가 명확해집니다.

| 단위 | 코드에서의 역할 | 중요한 연결 정보 |
| --- | --- | --- |
| 프로젝트 | 로컬 저장소와 기본 브랜치, 기본 실행 명령을 관리합니다. | `repo_path`, `baseline_branch`, `run_command` |
| 실험 | 가설의 계보와 해당 Git 브랜치를 관리합니다. | `parent_experiment_id`, `branch_name`, `run_command` |
| 실행 | 특정 시점의 소스와 명령을 실행한 기록입니다. | `commit_sha`, `backend_json`, 상태, 실행 명령 |
| 세션 | 특정 하네스를 사용하는 대화의 단위입니다. | 세션 식별자, 세션 작업 디렉터리와 하네스 상태 |

프로젝트·실험의 저장 구조는 SQLite 테이블 정의에 나타납니다. 실행은 별도의 `StoredRun`으로 저장되며, 제출 시 실험·프로젝트 ID와 커밋 SHA를 함께 기록합니다. 따라서 실험 브랜치가 가리키는 현재 코드와 과거 실행에 기록된 코드는 같은 개념이 아닙니다. [테이블 정의](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/store.rs#L417-L457), [실행 레코드 생성](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/compute.rs#L778-L796)

| 경로 | 이 글에서 확인한 책임 |
| --- | --- |
| `src/main.rs`, `src/commands/` | 명령을 분배하고 대시보드 API와 감독 프로세스를 제공합니다. |
| `src/plane/local_plane.rs` | 실험 ID를 바탕으로 실행 설정을 적용하고 제출 경로를 선택합니다. |
| `src/local/experiments.rs`, `src/local/git.rs` | 실험 브랜치·부모 관계·세션 worktree를 만듭니다. |
| `src/compute.rs` | 소스 아카이브, 제출 전 점검, 실행 예약과 백엔드 제출을 연결합니다. |
| `src/local/localrun.rs`, `src/jobs/localbox.rs` | 로컬 실행 명령과 환경을 구성하고 분리된 프로세스를 띄웁니다. |
| `src/store.rs`, `ui/src/` | 상태를 보관하고 화면에서 API와 이벤트를 소비합니다. |

이 책임 구분은 아래에서 추적하는 실제 함수 호출을 기준으로 정리했습니다. 대시보드 서버는 `127.0.0.1`에 바인딩하며, `/api/runs`와 실행 로그 조회 경로 등을 제공합니다. UI 쪽에는 앱 전체가 공유하는 `/api/events` EventSource가 있습니다. [서버 시작](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/commands/up.rs#L52-L87), [라우트](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/commands/up.rs#L500-L577), [UI 이벤트 연결](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/ui/src/events.ts#L223-L249)

![실험 브랜치에서 소스 아카이브와 로컬 실행 기록으로 이어지는 흐름]({{ '/img/reviews/2026/openresearch-review/execution-flow.svg' | relative_url }})

그림 1. 리뷰어 작성, 분석 커밋 기준. 로컬 실행의 공통 경로를 간략화했습니다. CLI는 실행 중인 신뢰 가능한 `orx up`이 있으면 API로 제출하고, 없으면 로컬 실행 어댑터로 진입합니다. 두 경로는 `compute::submit`에 연결됩니다. [CLI 분기](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/plane/local_plane.rs#L225-L264), [대시보드 제출](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/commands/up.rs#L2096-L2129), [스냅샷과 제출](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/compute.rs#L727-L798), [로컬 실행](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/local/localrun.rs#L76-L166)

## 작동 원리

### 1. 실험은 Git 브랜치와 부모 관계를 함께 만듭니다

`create_experiment`는 부모 실험이 같은 프로젝트에 속하는지 먼저 확인합니다. 이어 이름을 slug로 정규화하고, 데이터베이스의 기존 실험 이름과 `orx/` 접두사의 로컬 브랜치를 함께 검사하여 충돌 없는 이름을 고릅니다. Git 브랜치만 검사하거나 데이터베이스만 검사하는 방식이 아니라 두 저장 공간을 함께 고려합니다. [이름 결정](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/local/experiments.rs#L14-L36), [프로젝트 검사](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/local/experiments.rs#L72-L93)

다음 코드는 부모가 있으면 부모 브랜치의 현재 끝에서, 없으면 프로젝트의 기본 브랜치에서 새 `orx/<slug>` 브랜치를 만드는 부분입니다.

```rust
let repo = Path::new(&project.repo_path);
let fork_point = parent
    .map(|p| p.branch_name.as_str())
    .unwrap_or(&project.baseline_branch);
let branch_name = format!("orx/{slug}");
git::create_experiment_branch(repo, fork_point, &branch_name)?;
```

출처: [`src/local/experiments.rs` 95–100행](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/local/experiments.rs#L95-L100). 그대로 발췌했습니다.

브랜치를 만든 뒤에는 실험 ID, 부모 실험 ID, 브랜치 이름, 설명과 명령을 SQLite에 기록합니다. Git은 코드의 계보를, 데이터베이스는 사용자가 보는 실험의 의미와 관계를 보관하는 셈입니다. 두 정보가 연결되므로 “부모 실험의 변형”을 코드 차이와 실험 트리 양쪽에서 표현할 수 있습니다. [실험 저장](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/local/experiments.rs#L113-L129)

단, 문서의 실험 규율과 저장 구조의 보장은 구별해야 합니다. 저장소의 에이전트용 문서는 결과를 얻은 노드를 다시 수정하지 않고, 모든 노드에서 실행 명령과 환경을 고정하라고 지시합니다. 반면 실험 생성 함수의 명령 선택 우선순위는 **명시적 입력 → 부모 명령 → 프로젝트 기본값 → 빈 문자열**입니다. 즉, 이 함수는 부모 명령의 상속을 제공하지만 다른 명령을 전달하는 것 자체를 금지하지 않습니다. 실험 비교의 공정성은 이런 운영 규칙도 지켜야 확보됩니다. [문서의 규율](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/SKILL.md#L18-L40), [명령 상속 구현](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/local/experiments.rs#L102-L111)

### 2. 에이전트의 편집 공간은 세션 worktree입니다

Git worktree는 하나의 저장소 이력을 공유하면서 파일 작업 디렉터리를 별도로 두는 기능입니다. `ensure_playbook`은 세션의 worktree를 확보하고 그 안에 연구 작업 안내와 하네스별 skill 파일을 준비합니다. `ensure_session_worktree`는 기본적으로 프로젝트의 기본 브랜치를 시작점으로 삼고, 실제 생성은 `git worktree add --detach`를 사용합니다. 따라서 새 세션을 만들었다고 새 실험 브랜치가 자동으로 생기는 것은 아닙니다. 세션 작업 공간과 실험 노드의 생성은 별도 동작입니다. [playbook 준비](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/local/opencode.rs#L304-L342), [세션 시작점](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/local/git.rs#L1258-L1275), [worktree 생성](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/local/git.rs#L1307-L1329)

이 분리는 병렬 탐색에서 유용합니다. 서로 다른 세션은 별도 작업 공간에서 수정할 수 있고, 실행 계층은 그 작업 디렉터리를 직접 실행하지 않습니다. 다만 worktree는 운영체제 수준의 보안 샌드박스가 아닙니다. 여기에서 확인한 것은 파일 편집 경로를 분리하는 구현이며, 모든 하네스의 권한과 도구 실행 격리를 감사한 것은 아닙니다.

### 3. CLI와 대시보드는 공통 제출 과정으로 모입니다

`main.rs`는 `Exp` 명령을 `commands::exp::run`으로 전달합니다. 이 함수는 실험 ID를 해석한 뒤 `launch`를 호출합니다. `LocalPlane::launch`는 저장된 기본 계산 환경을 반영하고, 없으면 `local`을 선택한 다음 인자를 검사합니다. [명령 분배](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/main.rs#L1122-L1153), [실험 실행 진입점](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/commands/exp.rs#L33-L37), [설정 적용](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/plane/local_plane.rs#L225-L234)

그다음 두 경로로 나뉩니다. 신뢰 가능한 대시보드 프로세스의 포트가 있으면 `submit_run_via_up`을 이용하고, 없으면 해당 계산 환경의 실행 함수를 호출합니다. 로컬 실행 함수는 다시 `compute::submit`을 호출합니다. 대시보드의 `create_run` 역시 요청을 `ExpRunArgs`로 변환하고 같은 함수를 호출합니다. 화면과 CLI가 서로 다른 스냅샷 규칙을 갖지 않도록 공통 경로를 둔 구조입니다. [CLI의 제출 경로](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/plane/local_plane.rs#L238-L264), [로컬 진입점](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/local/localrun.rs#L15-L18), [API 진입점](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/commands/up.rs#L2096-L2129)

`compute::submit`은 계산 환경의 `preflight` 결과가 준비 상태인지 확인하고, 소스를 준비한 뒤 실행 레코드를 예약합니다. `reserve_run`은 실험 ID별 파일 잠금을 잡고 아직 종료되지 않은 실행을 찾습니다. 기본 동작은 중복 실행을 거부하는 것이지만 `force`가 있으면 이 검사를 건너뜁니다. 따라서 “실험당 실행은 무조건 하나”가 아니라, 기본 경로에서 겹치는 제출을 방지하는 정책입니다. [제출 순서](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/compute.rs#L727-L798), [예약과 중복 검사](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/compute.rs#L835-L861)

### 4. 실행 입력은 브랜치 이름이 아니라 커밋 아카이브입니다

이 프로젝트에서 가장 중요한 경계는 `SourceSnapshot::create`입니다. 실험 브랜치의 커밋 SHA를 구한 뒤 그 커밋을 `git archive`로 내보냅니다. 아카이브 파일의 SHA-256과 크기를 계산하고, 해시를 이름으로 하는 파일로 보관합니다.

```rust
let revision = crate::local::git::local_head_sha(repo, &experiment.branch_name)?;
let dir = crate::store::data_dir().join("source-snapshots");
prepare_snapshot_dir(&dir)?;

let nonce = uuid::Uuid::new_v4();
let tar_tmp = dir.join(format!(".{nonce}.tar"));
archive(repo, &revision, "tar", &tar_tmp)?;
let (digest, size) = digest_file(&tar_tmp)?;
let path = dir.join(format!("{digest}.tar"));
install_content_addressed(&tar_tmp, &path, &digest, size)?;
```

출처: [`src/compute.rs` 40–49행](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/compute.rs#L40-L49). 그대로 발췌했습니다. `archive` 함수는 해당 revision을 `git archive` 인자로 넘깁니다. [아카이브 생성 구현](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/compute.rs#L126-L147)

여기에는 서로 다른 두 식별자가 있습니다. `revision`은 어떤 Git 커밋에서 왔는지를 설명하고, `digest`는 전달할 아카이브 바이트를 식별합니다. 실행 레코드는 커밋 SHA를 보관하고, 백엔드 설명자에는 아카이브 경로·digest·크기가 들어갑니다. 기존 실행에서 스냅샷을 다시 읽는 `from_run`은 파일의 digest와 크기를 대조하며 불일치하면 오류를 반환합니다. [메타데이터 기록](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/compute.rs#L71-L75), [다시 읽을 때의 검사](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/compute.rs#L77-L122)

이 설계에서 도출되는 실질적인 효과는 실행이 시작된 뒤 에이전트가 작업 파일을 더 고쳐도, 이미 준비된 실행 입력은 그 작업 디렉터리를 따라 바뀌지 않는다는 점입니다. 반대로 커밋에 들어가지 않은 수정은 이 아카이브 경로에 포함되지 않습니다. 이는 `git archive`에 브랜치의 고정 revision을 넘기는 구현에서 읽을 수 있는 범위이며, 데이터셋·패키지 서버·외부 API까지 자동으로 고정한다는 뜻은 아닙니다.

### 5. 로컬 실행은 아카이브를 풀고 호스트 환경에서 명령을 실행합니다

로컬 어댑터는 실험의 명령이 비어 있으면 프로젝트 명령을 사용합니다. 둘 다 없으면 오류를 반환합니다. 그런 다음 `snapshot_script`가 아카이브를 실행 디렉터리의 `repo`에 풀고 그 디렉터리에서 명령을 실행하도록 셸 스크립트를 구성합니다. [명령 선택과 스크립트 생성](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/local/localrun.rs#L66-L82), [snapshot_script](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/compute.rs#L225-L230)

환경도 별도로 합칩니다. 동기화된 환경 변수, Hugging Face 토큰, 셸에서 가져온 경로와 환경이 실행에 전달됩니다. 로컬 실행에서 `--image`는 “이 컴퓨터의 환경을 사용한다”는 오류와 함께 거부됩니다. 따라서 소스 스냅샷 고정과 실행 환경 고정은 구별해야 합니다. 같은 커밋이라도 로컬 패키지·환경 변수·외부 데이터가 다르면 결과가 달라질 수 있다는 것이 이 구현에 대한 리뷰어의 해석입니다. [로컬 옵션 제한](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/local/localrun.rs#L56-L63), [환경 구성](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/local/localrun.rs#L84-L111)

`localbox::run_job`은 실행별 디렉터리에 `run.sh`를 작성합니다. 실제 명령은 서브셸 안에서 실행하며 표준 출력과 표준 오류를 `log`에 합칩니다. 명령이 끝나면 종료 코드를 `exit_code`에 기록합니다. Unix에서는 별도 프로세스 그룹으로 실행하고, 디렉터리와 스크립트 권한을 소유자 전용으로 설정하는 코드가 있습니다. 이는 로컬 프로세스를 관리하는 구현이지 컨테이너 생성 코드가 아닙니다. [run.sh와 프로세스 생성](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/jobs/localbox.rs#L42-L95)

백엔드 설명자의 실행 핸들을 기록하지 못하면 로컬 작업을 취소하는 처리도 있습니다. 성공하면 `StoredRun`에 실행 명령·커밋 SHA·백엔드 설명자를 저장하고, 별도의 `orx supervise` 프로세스를 띄웁니다. 제출과 감독이 분리되므로 실행 명령을 요청한 CLI 프로세스가 계속 붙어 있을 필요가 없는 구조입니다. [핸들 저장 실패 처리와 감독 시작](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/local/localrun.rs#L141-L167)

### 6. 실행 결과는 로그와 상태로 돌아옵니다

로컬 감독 함수 `run_local`은 로그를 복사하는 비동기 작업을 시작하고, 별도의 루프에서 프로세스 상태를 검사합니다. 종료 상태이면 SQLite의 상태와 종료 시각을 갱신하고 실패 사유가 있을 때 `result_markdown`에 남깁니다. 취소 요청도 저장소에서 읽어 로컬 프로세스에 전달합니다. [로컬 감독 루프](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/commands/supervise.rs#L959-L1020)

원본 실행 디렉터리의 `log`는 저장소의 실행별 로그 파일로 복사됩니다. 이 경로를 CLI와 대시보드가 함께 사용합니다. `tail_logs_local`은 읽은 위치를 추적하고 새 내용을 이어서 가져옵니다. 코드에는 로그 파일 열기 실패와 스트림 오류 처리도 있으므로, 실행 상태 저장과 로그 확보를 하나의 원자적 성공으로 간주할 수는 없습니다. [로그 복사](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/commands/supervise.rs#L1023-L1060)

또한 `done`은 과학적 가설의 성공을 의미하지 않습니다. 로컬 작업 상태 판정은 종료 코드 0이면 `COMPLETED`, 아니면 `ERROR`로 매핑합니다. 모델 정확도가 개선되었는지, 실험 비교가 타당한지는 사용자가 남긴 결과와 이를 읽는 에이전트의 후속 판단에 속합니다. 이 실행 계층이 보장하려는 것은 “어떤 코드를 실행했고 프로세스가 어떻게 끝났는가”의 추적입니다. [종료 코드 판정](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/jobs/localbox.rs#L145-L166)

## 설치와 사용: 문서에 제시된 진입점

아래는 분석 커밋의 README에 있는 macOS/Linux 설치·시작 명령입니다. 이 리뷰에서는 실행하지 않았으며, 설치 URL이 가리키는 배포물은 향후 바뀔 수 있으므로 위 고정 소스 커밋을 설치하는 명령으로 읽으면 안 됩니다. [README 설치 절](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/README.md#L34-L44)

```sh
curl -LsSf https://openresearch.sh/install.sh | sh
orx up
```

README의 기본 대시보드 주소는 `http://127.0.0.1:4791`입니다. 다음은 README 명령 중 조회·실행에 필요한 항목을 선별·재배열한 것입니다. 자리표시자는 각각 프로젝트·실험·실행의 ID를 뜻하며 서로 바꿔 쓰는 값이 아닙니다. [README 명령 목록](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/README.md#L108-L120)

```sh
orx projects
orx project view <project-id>
orx exp run <experiment-id>
orx runs <project-id>
orx logs <run-id>
```

에이전트에 사용법을 설치하는 명령은 `orx install-skills`입니다. 로컬 모델 문서는 OpenCode가 도구 실행과 편집을 담당하고 LM Studio·oMLX·Ollama 등이 모델 서버를 담당하는 구성을 설명합니다. 이는 로컬 모델 경로에 대한 문서 설명이며, 이 리뷰에서는 모델 연결이나 도구 호출 성공 여부를 확인하지 않았습니다. [skill 설치](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/README.md#L100-L106), [로컬 모델 문서](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/docs/local-models.md#L1-L26)

## 한계와 주의점

**README의 자율 연구 설명은 이 코드 경로만으로 입증되지 않습니다.** README는 아이디어 제안부터 실험 후 다음 방향 선택까지 자동화할 수 있다고 설명합니다. 이번 분석이 확인한 것은 에이전트 연결 인터페이스, 실험 브랜치와 스냅샷, 실행·기록 경로입니다. 장기 연구 과제에서의 성과나 에이전트별 품질 비교를 위한 수치 평가는 수행하지 않았습니다. [README Autoresearch](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/README.md#L76-L82)

**소스 재현성과 환경 재현성은 범위가 다릅니다.** SHA로 고정된 아카이브는 실행할 코드의 출처를 남깁니다. 로컬 실행은 호스트 환경과 동기화된 환경 변수를 사용하므로, 같은 코드라는 사실만으로 같은 계산 결과를 보장하지 않습니다. 문서가 요구하는 명령·환경 고정 규율과 코드의 기록 장치를 함께 이해해야 합니다. [환경 전달 구현](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/local/localrun.rs#L84-L111), [실험 규율](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/SKILL.md#L26-L37)

**로컬 우선은 네트워크 사용이 없다는 뜻이 아닙니다.** README는 공식 배포 빌드의 사용 분석과 선택 해제 방법을 설명하고, 계산 어댑터에는 외부 실행 환경이 포함됩니다. 사용 분석 데이터의 실제 전송 범위와 모든 외부 연결을 이번에 감사하지 않았으므로 README의 개인정보 관련 설명을 구현 검증 결과로 확대하지 않습니다. [사용 분석 안내](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/README.md#L129-L149), [외부 계산 어댑터 등록](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/src/compute.rs#L461-L643)

라이선스는 MIT입니다. 원문은 저작권·허가 고지 보존 조건과 무보증 조항을 포함합니다. [LICENSE](https://github.com/alphaXiv/OpenResearch/blob/c95be22a35ca91057d61e3e6fde31d69c9af27f6/LICENSE#L1-L21)

## 결론

OpenResearch의 핵심 설계는 연구 과정을 세션의 작업 공간, 실험의 Git 계보, 실행의 커밋 아카이브, 로그와 상태 기록으로 나누고 연결하는 데 있습니다. 특히 실행 직전 브랜치의 커밋을 아카이브로 고정하는 경계는 에이전트의 계속되는 수정과 이미 시작된 실험을 분리합니다. 다만 실행 명령과 환경의 비교 가능성, 결과의 과학적 의미는 그 기록 구조만으로 해결되지 않습니다. 이 저장소는 자율 연구의 성과보다 먼저, 그 과정을 추적 가능하게 만드는 기반을 읽어볼 만한 사례입니다.

## 이 글에서 다루지 못한 부분

원격 계산 어댑터의 등록과 공통 제출 경계는 읽었지만 SSH·Slurm·Kubernetes·Ray·Modal·Hugging Face·Tinker·관리형 OpenResearch의 전체 전송·복구·취소 경로는 분석하지 않았습니다. 개별 하네스의 프로토콜·권한 처리, 문헌 검색과 논문 해석, Overleaf 동기화, LaTeX 컴파일, 데스크톱 패키징·업데이트, 전체 UI 및 텔레메트리 구현도 상세 감사 범위 밖입니다. 대상 저장소의 테스트는 실행하지 않았고 운영 안정성이나 성능을 측정하지 않았습니다.
