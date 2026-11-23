---
type: "Repo Review"
title: "[Repo Review] Claude Code Security Reviewer — 보안 후보가 PR 댓글이 되기까지"
description: "Claude Code Security Reviewer가 PR 변경을 분석하고 규칙·API 필터를 거쳐 댓글을 만드는 경로를 추적하며, 발견 건수와 분석 완료·CI 상태를 구분합니다."
date: "2026-11-24"
tags:
  - "Repo Review"
  - "Claude"
  - "Anthropic"
  - "AI Agent"
  - "Python"
  - "Tools"
resource: "https://github.com/anthropics/claude-code-security-review/tree/0c6a49f1fa56a1d472575da86a94dbc1edb78eda"
generated:
  by: "process:blog-review"
  at: "2026-11-24T06:15:00+09:00"
sources:
  - id: "github:anthropics/claude-code-security-review"
    resource: "https://github.com/anthropics/claude-code-security-review/tree/0c6a49f1fa56a1d472575da86a94dbc1edb78eda"
    title: "Claude Code Security Reviewer"
    author: "Anthropic"
status: "stable"
year: "2026"
analyzed_at: "2026-11-24T06:15:00+09:00"
source_id: "anthropics/claude-code-security-review"
source_revision: "0c6a49f1fa56a1d472575da86a94dbc1edb78eda"
source_type: "repo"
source_url: "https://github.com/anthropics/claude-code-security-review/tree/0c6a49f1fa56a1d472575da86a94dbc1edb78eda"
visual_sources:
  - path: "img/reviews/2026/claude-code-security-review/review-flow.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/claudecode/github_action_audit.py#L573-L633"
    caption: "PR 변경 수집, Claude Code 분석, 후보 필터와 리뷰 댓글 흐름. 리뷰어 작성, 분석 커밋 기준."
  - path: "img/reviews/2026/claude-code-security-review/status-boundary.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/action.yml#L244-L309"
    caption: "HIGH 발견의 Python 종료 코드와 Action 래퍼의 결과 처리를 구분한 도식. 리뷰어 작성, 분석 커밋 기준."
---

## 들어가며: 보안 리뷰가 남긴 경고를 누가 다시 읽을까요

코드 변경에서 수상한 부분을 찾는 것과, 동료가 실제로 읽고 고칠 만한 경고를 남기는 것은 다른 작업입니다. 경고가 너무 많으면 중요한 문제도 묻힙니다. 반대로 경고를 줄이는 데만 집중하면 확인해야 할 후보까지 사라질 수 있습니다.

Anthropic의 **Claude Code Security Reviewer**는 이 두 작업을 나눕니다. Claude Code가 PR의 변경 사항을 저장소 맥락에서 살펴보고 보안 문제 후보를 만들면, 별도 필터가 후보를 추린 뒤 GitHub 코드 줄에 댓글을 남깁니다. 단순히 diff를 모델에 보내는 짧은 스크립트보다, **무엇을 보여 주고 무엇을 지울지 결정하는 처리 과정**이 눈에 띕니다.

이 글은 커밋 `0c6a49f1fa56a1d472575da86a94dbc1edb78eda`의 문서와 코드를 정적으로 읽은 리뷰입니다. 대상 코드를 설치하거나 실행하지 않았으며, 취약점 탐지율이나 오탐 감소율을 측정하지 않았습니다. [고정 버전 저장소](https://github.com/anthropics/claude-code-security-review/tree/0c6a49f1fa56a1d472575da86a94dbc1edb78eda)에서 실제 호출 경로를 따라갑니다.

## 무엇인가: PR 변경을 읽고 보안 후보를 댓글로 연결하는 Action

이 프로젝트는 GitHub Actions에서 실행하는 composite Action입니다. 여기서 composite는 Python 준비, 의존성 설치, 분석, 결과 업로드, 댓글 작성 같은 여러 단계를 하나의 Action으로 묶었다는 뜻입니다. 입력에는 Anthropic API 키, 분석 모델, 제외할 디렉터리, 댓글·아티팩트 여부 등이 있습니다. 출력은 발견 건수와 결과 파일 경로입니다. [입출력 정의](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/action.yml#L1-L58)에 이 계약이 나옵니다.

README는 문맥 이해, 다양한 언어 지원, 오탐 필터링을 기능으로 소개합니다. 구현에서 확인한 사실은 Claude Code에 저장소 탐색을 맡기고, 결과를 규칙과 추가 모델 호출로 걸러낸다는 것입니다. README의 “기존 SAST보다 낮은 오탐” 같은 설명은 이 리뷰에서 검증한 비교 실험 결과가 아닙니다. SAST는 프로그램을 실행하지 않고 소스 코드를 검사하는 정적 애플리케이션 보안 검사입니다. [기능·비교 설명](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/README.md#L5-L12), [SAST 대비 설명](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/README.md#L120-L125)을 이 범위에서 읽어야 합니다.

## 아키텍처: 분석용 CLI와 필터용 API가 나뉩니다

| 파일 | 입력 | 맡는 일과 출력 |
| --- | --- | --- |
| `action.yml` | GitHub 이벤트와 Action inputs | 실행 여부 판단, 환경 준비, Python 호출, 파일 업로드와 댓글 단계 연결 |
| `github_action_audit.py` | 저장소 이름, PR 번호, 토큰, 저장소 경로 | PR 정보·diff 수집, 분석 실행, 필터 적용, 최종 JSON 출력 |
| `prompts.py` | PR 정보·diff·추가 검사 지침 | 보안 검토용 프롬프트 구성 |
| `findings_filter.py` | 발견 후보 목록 | 고정 제외 규칙과 후보별 모델 판단을 적용 |
| `claude_api_client.py` | 후보 하나와 PR 맥락·파일 내용 | Anthropic API로 후보 보존 여부를 재검토 |
| `json_parser.py` | 모델 응답 텍스트 | JSON 직접 파싱과 코드 블록 등에서의 추출 시도 |
| `scripts/comment-pr-findings.js` | `findings.json`과 PR 이벤트 | 변경 파일에 해당하는 후보를 리뷰 댓글로 전송 |

중심 진입점은 `python -u claudecode/github_action_audit.py`입니다. Python의 분석 단계는 `claude` CLI를 자식 프로세스로 실행하고, 필터 단계는 Anthropic Python SDK를 통해 API를 직접 호출합니다. 같은 모델 서비스에 접근하더라도 호출 경로와 맡긴 일이 다릅니다. [Action의 진입점](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/action.yml#L176-L252), [CLI 실행](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/claudecode/github_action_audit.py#L203-L240), [API 호출](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/claudecode/claude_api_client.py#L74-L121)을 구분하면 구조가 선명해집니다.

![PR 정보 수집에서 Claude Code 분석, 후보 필터와 GitHub 댓글로 이어지는 네 단계]({{ '/img/reviews/2026/claude-code-security-review/review-flow.svg' | relative_url }})

PR 변경에서 보안 후보를 만들고 댓글로 전달하는 흐름. 리뷰어 작성, 분석 커밋 기준. 출처: [분석 진입점](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/claudecode/github_action_audit.py#L573-L633)과 [댓글 작성](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/scripts/comment-pr-findings.js#L128-L198).
{: .caption}

## 작동 원리 1: 같은 PR을 언제 다시 분석할지 먼저 정합니다

분석 전에 `.claudecode-marker/marker.json`의 존재를 확인합니다. `run-every-commit`의 기본값은 `false`이고, 이전 실행의 marker가 복원되면 Claude Code 분석을 끕니다. 캐시 키에는 저장소 ID, PR 번호와 SHA가 들어가지만, 복원 접두사는 PR 단위입니다. 따라서 이전 SHA에서 만든 marker도 새 커밋의 분석 여부에 영향을 줍니다. [캐시와 실행 판단](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/action.yml#L83-L132)에 따른 동작입니다.

분석을 진행할 때는 먼저 `status: reserved`인 marker를 만들고 캐시에 저장합니다. 이 시점은 분석 성공 이후가 아닙니다. 작성자의 의도는 중복 실행을 줄이는 것이지만, 여기서 확인한 구현만으로 동시 실행을 원자적으로 잠근다고 단정할 수는 없습니다. 또 실패한 실행에서 만든 marker가 나중에 복원될 가능성도 실행 이력과 함께 봐야 합니다. [예약 marker 생성·저장](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/action.yml#L134-L167)이 이 순서를 보여 줍니다.

즉 기본 동작은 “매 커밋을 항상 다시 검사”하는 방식과 다릅니다. 새 코드가 추가됐는지뿐 아니라, 이번에 분석 단계가 실제로 켜졌는지를 구분해야 합니다.

## 작동 원리 2: diff를 읽되 저장소 전체의 맥락을 탐색합니다

`GitHubActionClient`는 PR 메타데이터와 파일 목록을 받은 뒤 diff를 별도 요청합니다. 파일 목록에는 디렉터리 제외 조건을 적용하고, diff에서는 생성 파일 표시와 제외 경로에 해당하는 구간을 걸러냅니다. PR 파일 목록 요청은 `per_page=100`인 한 번의 요청이며, 이 함수 안에 다음 페이지를 따라가는 반복은 없습니다. 주석의 “pagination support”와 실제 구현을 구별할 부분입니다. [PR 데이터 수집](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/claudecode/github_action_audit.py#L61-L117), [diff 필터](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/claudecode/github_action_audit.py#L119-L186)에 근거합니다.

프롬프트는 “이번 PR이 새로 도입한 보안 문제”에 초점을 맞춥니다. 동시에 기존 보안 패턴과 데이터 흐름을 이해하도록 파일 탐색을 요구합니다. 따라서 README의 “변경 파일만 분석”은 **보고할 문제의 초점이 변경 사항이라는 의미**로 이해하는 편이 구현에 가깝습니다. CLI가 읽을 수 있는 문맥이 diff 문자열에만 제한된 구조는 아닙니다. 실행 디렉터리도 Action 코드 폴더가 아니라 `REPO_PATH`가 가리키는 검토 대상 저장소입니다. [프롬프트 구성과 탐색 지시](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/claudecode/prompts.py#L41-L124), [저장소 경로 전달](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/claudecode/github_action_audit.py#L584-L595)을 함께 확인했습니다.

CLI는 JSON 출력 형식과 모델을 지정해 실행합니다. 기본 모델은 이 커밋의 `constants.py`에서 `claude-opus-4-1-20250805`이며, `CLAUDE_MODEL` 환경변수가 있으면 이를 사용합니다. 기본 모델 이름은 분석 버전의 설정이지 최신 모델에 대한 안내가 아닙니다. [모델과 기본 시간 설정](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/claudecode/constants.py#L6-L23)에 고정되어 있습니다.

모델 응답은 바로 최종 결과가 되지 않습니다. 먼저 CLI 바깥쪽 JSON을 읽고, 그 안의 문자열 `result`에서 다시 `findings`를 추출합니다. 추출할 수 없으면 빈 목록과 `review_completed: false`인 기본 요약을 돌려주는 경로도 있습니다. 그래서 빈 목록만 보고 “검토가 완료됐고 문제가 없다”고 해석하면 안 됩니다. [응답 추출부](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/claudecode/github_action_audit.py#L254-L312)가 그 차이를 남깁니다.

특정한 `Prompt is too long` 응답을 감지하면 diff를 뺀 프롬프트로 한 번 더 분석합니다. 이때 변경 파일 이름과 저장소 탐색 지시는 남습니다. 모든 실패를 같은 방식으로 재시도하는 것은 아니며, [조건부 재시도](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/claudecode/github_action_audit.py#L590-L599)에 해당할 때만 실행됩니다.

## 작동 원리 3: 후보를 줄이는 두 단계의 기준

첫 단계는 모델이 아니라 Python 규칙입니다. Markdown 파일의 발견, 특정 DoS·자원 고갈·rate limiting·open redirect 표현 등을 제외하고, 메모리 안전 관련 표현은 파일 확장자가 `.c`, `.cc`, `.cpp`, `.h`인지도 봅니다. 이 규칙은 취약점의 참·거짓을 증명하는 절차가 아니라 **이 도구가 보고할 범위를 정한 정책**입니다. [고정 제외 규칙](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/claudecode/findings_filter.py#L27-L154)을 보안 일반론으로 받아들이면 곤란합니다.

둘째 단계에서는 고정 규칙을 통과한 후보를 하나씩 Claude API에 보냅니다. 후보 설명, PR 맥락, 가능하면 해당 파일 내용까지 포함해 `keep_finding`, `confidence_score`, 판단 근거를 받습니다. API 클라이언트는 `REPO_PATH`를 기준으로 파일을 찾습니다. [후보별 프롬프트](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/claudecode/claude_api_client.py#L196-L240), [파일 읽기](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/claudecode/claude_api_client.py#L320-L355)를 확인할 수 있습니다.

여기서 실제 제거 분기는 점수의 고정 임곗값 비교가 아니라 `keep_finding` 값입니다. 점수는 기록되지만 Python이 “8점 미만이면 제거”처럼 별도로 비교하지는 않습니다. 모델이 후보 보존을 권하면 점수와 판단 근거를 메타데이터로 붙여 남깁니다. 호출이 실패한 후보도 버리지 않고 보존합니다. 이때 들어가는 기본 `10.0`은 **모델이 확신한 점수라는 뜻이 아니라 실패·비활성 경로의 기본값**입니다. [필터의 실제 분기](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/claudecode/findings_filter.py#L255-L316)에 나옵니다.

아래는 위 호출 관계를 설명하기 위해 다시 쓴 의사코드입니다. 원본 Python의 복사본이나 실행 결과가 아닙니다.

```text
입력: 최초 분석의 발견 후보, PR 맥락, 제외 디렉터리
후보마다:
    고정 제외 규칙에 해당하면 제외 사유와 함께 분리
    그렇지 않으면:
        API 필터가 사용 가능할 때 후보를 개별 재검토
        재검토 성공 + keep_finding이 거짓이면 제외
        재검토 실패 또는 필터 비활성이면 후보 보존
보존 후보에 디렉터리 제외 조건을 한 번 더 적용
출력: 보존 후보, 제외된 후보, 필터 처리 요약
```

의사코드 근거: [규칙과 API 필터](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/claudecode/findings_filter.py#L229-L343), [마지막 디렉터리 검사](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/claudecode/github_action_audit.py#L457-L501).

최종 JSON에는 보존 후보만 있는 것이 아닙니다. 최초 후보 수, 제외 수, 보존 수와 제외 세부 내용도 `filtering_summary`에 남습니다. 최초 분석의 `analysis_summary`와 필터 처리 요약은 구별됩니다. 경고가 줄었다는 결과를 읽으려면 줄어든 이유까지 봐야 하는 구조입니다. [최종 출력 구성](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/claudecode/github_action_audit.py#L601-L633)에 이 정보가 있습니다.

## 작동 원리 4: JSON에서 코드 줄의 댓글로

Action 래퍼는 결과에서 `findings`를 꺼내 `findings.json`으로 저장합니다. Node 스크립트는 이 파일을 읽고 PR 파일 목록을 다시 조회합니다. 후보의 파일이 그 목록에 있을 때만 댓글을 준비하며, 파일명·줄 번호·심각도·설명과 선택적인 공격 시나리오·수정 권고를 댓글 본문으로 바꿉니다. [결과 파일 생성](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/action.yml#L277-L286), [댓글 변환](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/scripts/comment-pr-findings.js#L91-L169)이 연결되는 지점입니다.

이 댓글 스크립트의 파일 목록 조회도 `per_page=100`인 단일 요청이며 다음 페이지 순회는 없습니다. 따라서 큰 PR의 모든 변경 파일을 댓글 대상으로 확보한다고 보장할 수는 없습니다.

댓글은 PR head SHA에 연결하고 `side: RIGHT`, 즉 변경 후 코드의 줄을 지정합니다. 다만 함수가 Git diff의 모든 줄을 치밀하게 재매핑하는 것은 아닙니다. 묶음 리뷰 전송에 실패하면 개별 댓글로 다시 시도하지만, 이때도 원래 줄 번호를 사용합니다. 실패한 줄을 자동으로 올바른 줄로 옮겼다고 보장하지 않습니다. [리뷰 생성과 개별 재시도](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/scripts/comment-pr-findings.js#L190-L238)를 보면 이 범위가 드러납니다.

중복 방지도 후보별 비교와 다릅니다. 기존 댓글 중 Bot이 작성했고 정해진 보안 댓글 접두사가 들어간 것이 하나라도 있으면 이번 댓글 작성을 통째로 생략합니다. 앞서 본 PR 단위 캐시와 별개로 댓글 단계에도 이런 중복 억제 정책이 있습니다. [기존 댓글 검사](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/scripts/comment-pr-findings.js#L176-L188)에 따른 동작입니다.

## 결과를 읽을 때: 발견 건수와 CI 상태는 별개입니다

Python 진입점은 필터를 통과한 `HIGH` 후보가 있으면 종료 코드 1을 반환합니다. 그런데 Action 래퍼는 이 종료 코드를 변수로 받아 경고를 찍고 결과 파일 처리를 계속합니다. 따라서 **HIGH 후보가 있다는 사실만으로 Action이 반드시 실패하거나 병합이 차단된다고 볼 수 없습니다.** [Python 종료 분기](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/claudecode/github_action_audit.py#L635-L641), [래퍼의 종료 코드 처리](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/action.yml#L244-L252)를 따로 읽어야 합니다.

![Python의 HIGH 발견 종료 코드가 Action 경고와 결과 파일 처리로 이어지는 상태 경계]({{ '/img/reviews/2026/claude-code-security-review/status-boundary.svg' | relative_url }})

Python 종료 코드와 Action의 처리 결과를 구분한 도식. 리뷰어 작성, 분석 커밋 기준. 출처: [HIGH 발견 시 종료](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/claudecode/github_action_audit.py#L635-L637)와 [Action 래퍼](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/action.yml#L244-L309).
{: .caption}

| 관찰한 값 | 확인할 수 있는 것 | 그것만으로 단정할 수 없는 것 |
| --- | --- | --- |
| `findings-count: 0` | 래퍼가 노출한 발견 건수가 0 | 분석의 정상 완료, 모든 코드의 안전성 |
| `review_completed: false` | 추출 기본 구조에서 검토 미완료가 표시됨 | 정상적으로 끝난 무취약점 결과 |
| `findings`에 `HIGH`가 존재 | 보존된 고위험 후보가 있음 | GitHub 병합 차단이 적용됨 |
| 필터 메타데이터의 `10.0` | 모델 응답 또는 기본값으로 기록된 수치 | API 재검토가 성공했고 강한 확신을 보였음 |

오류 JSON의 `.error`가 있거나 결과 파일이 비정상인 경우에도 래퍼는 발견 건수를 0으로 기록하는 경로가 있습니다. 결과 파일, 오류 로그, 분석 완료 여부를 같이 봐야 합니다. 아티팩트 업로드는 기본적으로 켜져 있고 보존 기간은 이 커밋에서 7일입니다. [오류·빈 파일 처리](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/action.yml#L254-L309), [아티팩트 정의](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/action.yml#L312-L323)에 근거합니다.

## 설치와 사용: README의 연결 방식과 실제 설정의 범위

README는 Ubuntu runner에서 PR head를 checkout하고 Action을 호출하는 workflow를 제시합니다. 필요한 권한은 코드 읽기와 PR 댓글 쓰기이며, API 키는 Claude API와 Claude Code 양쪽 사용이 가능해야 한다고 적혀 있습니다. 여기서는 이 설정을 실행하거나 어떤 저장소에 활성화하지 않았습니다. [Quick Start와 입력 표](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/README.md#L14-L61)는 도입 방식을 설명하는 자료입니다.

주요 설정을 구현 기준으로 정리하면 다음과 같습니다.

| 설정 | 이 커밋에서 확인한 의미 |
| --- | --- |
| `comment-pr`, `upload-results` | 댓글과 결과 업로드 단계의 실행 여부를 각각 조절합니다. 둘 다 기본 `true`입니다. |
| `exclude-directories` | PR 파일·diff와 최종 보존 후보에 디렉터리 제외를 적용합니다. |
| `run-every-commit` | 기존 PR marker가 있을 때도 분석할지 정합니다. 기본 `false`입니다. |
| `claude-model` | 환경변수로 기본 분석·필터 모델을 바꿉니다. |
| `custom-security-scan-instructions` | 최초 분석 프롬프트에 검사 항목을 추가합니다. |
| `false-positive-filtering-instructions` | API 재검토 프롬프트의 기본 지침을 사용자 파일 내용으로 대체합니다. Python 고정 제외 규칙까지 바꾸지는 않습니다. |

마지막 두 설정은 이름이 비슷해도 작용 위치가 다릅니다. 검사 지침은 [프롬프트에 덧붙이고](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/claudecode/prompts.py#L36-L39), 필터 지침은 [API 프롬프트의 기본 부분을 대체](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/claudecode/claude_api_client.py#L239-L243)합니다. 이미 앞 단계에서 고정 규칙으로 제거된 후보를 후자의 지침으로 되살리는 구조는 아닙니다.

`claudecode-timeout`은 문서에 노출되지만 전달 경로를 주의해서 봐야 합니다. Action은 `CLAUDE_TIMEOUT`을 내보내는 반면, 분석 진입점은 인자 없이 `SimpleClaudeRunner()`를 만들고 이 객체는 `SUBPROCESS_TIMEOUT=1200`을 사용합니다. 확인한 Python 경로에는 해당 환경변수를 읽는 코드가 없습니다. 따라서 입력 값을 바꿨을 때 Python의 자식 프로세스 제한 시간까지 바뀐다고 확인할 수는 없습니다. [Action 환경변수](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/action.yml#L216-L217), [초기화](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/claudecode/github_action_audit.py#L375-L394), [runner 기본값](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/claudecode/github_action_audit.py#L192-L201)을 대조한 결과입니다.

## 한계와 주의점: 도구가 보는 범위를 먼저 읽습니다

README는 이 Action이 prompt injection에 강건하게 설계되지 않았고, 신뢰할 수 있는 PR에만 사용해야 한다고 명시합니다. 검토할 코드나 문서 안의 문장이 모델에게 지시처럼 읽혀 분석에 영향을 주는 문제입니다. 저장소를 탐색하고 내용을 모델에 전달하는 이 구조에서 중요한 사용 조건입니다. CLI 호출은 `Bash(ps:*)`를 금지 도구로 지정하지만, 이 한 옵션을 모든 셸 명령을 차단하는 격리 환경이라고 해석할 근거는 없습니다. [CLI 인자](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/claudecode/github_action_audit.py#L224-L229)에서 확인한 범위입니다. [저장소의 보안 고려사항](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/README.md#L43-L45)을 그대로 경계로 삼습니다.

또한 기본 필터는 도구가 집중할 문제를 선택합니다. DoS나 open redirect를 제외한다는 규칙을 “그 문제는 보안상 중요하지 않다”는 보편적 결론으로 바꿀 수는 없습니다. README가 넓게 열거한 탐지 범주와, 실제 프롬프트·규칙이 제외하는 범위를 함께 읽어야 합니다.

소스 SHA를 고정해도 실행 환경의 모든 구성 요소가 고정되는 것은 아닙니다. 이 Action은 Claude Code npm 패키지를 버전 지정 없이 설치하고 Python 의존성도 하한 범위로 지정합니다. 이것은 이 리뷰가 확인한 소스 버전과 실제 실행 시 설치되는 도구 버전을 구분해야 하는 이유입니다. [설치 단계](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/action.yml#L169-L175), [Python 의존성](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/claudecode/requirements.txt#L1-L18)에 근거합니다.

저장소 코드는 [MIT License](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/LICENSE#L1-L21)로 공개되어 있습니다. 저작권자는 Anthropic이며, 라이선스의 저작권·허가 고지 보존 조건이 적용됩니다. 이 글의 두 도식과 의사코드는 구현을 설명하기 위해 새로 작성한 자료입니다. 외부 모델 서비스의 이용 조건과 비용은 저장소 코드의 MIT 라이선스와 별개입니다.

## 마무리: 경고가 만들어지고 걸러지는 과정을 봅니다

이 저장소에서 배울 부분은 모델 호출 하나보다 그 앞뒤의 연결입니다. PR 맥락을 모으고, 저장소 안에서 후보를 찾고, 규칙과 추가 모델 판단으로 후보를 추린 뒤 코드 줄에 연결합니다. 각 단계의 입력과 출력이 명확해서 어떤 정보가 댓글까지 살아남는지 따라갈 수 있습니다.

동시에 분석 생략, 필터 실패, 응답 추출 실패와 HIGH 발견의 처리 방식은 서로 다릅니다. 발견 건수, 분석 완료 여부, 오류 로그와 CI 상태를 나눠 읽어야 이 도구가 남긴 결과를 제대로 이해할 수 있습니다.

이 글에서는 Action의 PR 분석·필터·댓글 경로를 다뤘습니다. `claudecode/evals/`의 평가 실행기와 전체 테스트 사례, `.claude/commands/security-review.md`의 대화형 명령 흐름은 상세 분석하지 않았습니다. 외부 Claude CLI 내부 구현과 실제 탐지 성능도 이 리뷰의 확인 범위에 포함되지 않습니다.
