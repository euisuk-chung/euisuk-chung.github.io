---
type: "Repo Review"
title: "[Repo Review] Awesome Agent Harness, YAML 한 파일에서 만드는 두 언어의 기술 목록"
description: "Awesome Agent Harness의 단일 YAML 목록이 GitHub 메타데이터 갱신과 다국어 README 생성을 거쳐 검증 보고서로 이어지는 과정을 추적합니다."
date: "2026-11-18"
tags:
  - "Repo Review"
  - "AI Agent"
  - "Python"
resource: "https://github.com/Picrew/awesome-agent-harness/tree/e7e8f8d268f7ac5311b778832327e4be2f555507"
generated:
  by: "process:blog-review"
  at: "2026-11-18T06:05:58+09:00"
sources:
  - id: "picrew/awesome-agent-harness"
    resource: "https://github.com/Picrew/awesome-agent-harness/tree/e7e8f8d268f7ac5311b778832327e4be2f555507"
    title: "Awesome Agent Harness"
status: "stable"
year: "2026"
analyzed_at: "2026-11-18T06:05:58+09:00"
source_id: "picrew/awesome-agent-harness"
source_revision: "e7e8f8d268f7ac5311b778832327e4be2f555507"
source_title: "Awesome Agent Harness"
source_type: "repo"
source_url: "https://github.com/Picrew/awesome-agent-harness/tree/e7e8f8d268f7ac5311b778832327e4be2f555507"
visual_sources:
  - path: "/img/reviews/2026/awesome-agent-harness-catalog-review/catalog-flow.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/CONTRIBUTING.md#L35-L49"
    caption: "리뷰어 작성, 분석 커밋 기준. 같은 YAML에서 두 README를 만들고 카탈로그와 게시된 문서를 함께 검증합니다."
    evidence_urls:
      - "https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/scripts/sync_github_metadata.py#L112-L183"
      - "https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/scripts/render_readme.py#L304-L333"
      - "https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/scripts/verify_catalog.py#L100-L188"
      - "https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/scripts/verify_catalog.py#L190-L251"
---

## 들어가며

브라우저를 조작하는 에이전트를 만들고 있다면, 브라우저 도구를 연결하는 방법과 그 도구로 수행한 작업을 평가하는 방법을 따로 찾아야 합니다. **Awesome Agent Harness**는 이런 자료를 도구 인터페이스, 실행 환경, 평가 등으로 묶은 기술 목록입니다. 이 레포가 다루는 하네스는 모델 주변에서 실행·상태 관리·도구 연결·검증을 맡는 구성요소를 뜻합니다. 목록을 유지하는 Python 코드가 어떤 정보를 받아 문서를 만들고, 어디까지 검사하는지 고정 커밋에서 확인했습니다. [큐레이션 범위와 정책](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/docs/curation_policy.md#L3-L27) · [고정 커밋](https://github.com/Picrew/awesome-agent-harness/tree/e7e8f8d268f7ac5311b778832327e4be2f555507)

## 무엇을 제공하나요?

영어·중국어 README에서 같은 순서로 프로젝트를 찾을 수 있습니다. 항목마다 분류와 태그, 설명, GitHub 링크 또는 참고 자료 링크가 붙습니다. 기준 커밋의 YAML에는 **375개 항목**이 있고, 코드의 GitHub URL 판정 방식으로 집계하면 **341개(90.9%)**가 GitHub 항목입니다. 읽을거리 범주를 빼면 **336개가 모두 GitHub 항목**입니다. 이 글의 수치는 고정 커밋의 카탈로그를 센 값입니다. 연구용 표본을 추려 138개로 분석한 별도의 [Agent Harness Engineering 서베이 리뷰]({{ '/2026/11/17/agent-harness-engineering-survey-review/' | relative_url }})와는 모집단과 분류 방식이 다릅니다. [YAML의 범주 선언](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/data/projects.yaml#L7-L44) · [README의 집계](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/README.md#L1-L10) · [비율 계산](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/scripts/render_readme.py#L73-L77)

| 카탈로그 범주 | 항목 수 |
| --- | ---: |
| 하네스 아키텍처 및 오케스트레이션 | 66 |
| 컨텍스트 및 작업 상태 | 32 |
| 실행 환경 및 샌드박스 | 27 |
| 프로토콜·도구 인터페이스·에이전트 계약 | 42 |
| 평가 하네스 및 벤치마크 | 29 |
| 관측 및 신뢰성 운영 | 21 |
| 가드레일·보안·거버넌스 | 27 |
| 참조 하네스 구현 | 92 |
| 읽을거리 및 생태계 지도 | 39 |

위 표는 현재 커밋의 범주별 항목 수입니다. 참조 구현의 92개는 이 목록이 그 분류에 넣은 행의 수입니다. 각 도구의 사용량이나 성능을 측정한 수치는 제공하지 않습니다. [범주별 집계](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/README.md#L50-L62)

## 아키텍처와 파일 구조

카탈로그의 편집 입력은 `data/projects.yaml` 한 파일입니다. 그 안에 기준일을 담은 `catalog`, 표시 순서·이름·앵커를 정의하는 `categories`, 실제 자료인 `entries`가 있습니다. README 두 개는 이 데이터를 사람이 읽기 좋게 펼친 결과이고, 날짜별 보고서는 별도 검증 단계의 출력입니다. 새 항목을 발견하는 절차는 검색 템플릿과 기여 문서에 설명돼 있습니다. 현 커밋의 세 스크립트는 이미 YAML에 들어온 항목을 처리합니다. [데이터 파일의 시작](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/data/projects.yaml#L1-L59) · [발견과 검증 문서](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/docs/sources_and_verification.md#L3-L42) · [기여 절차](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/CONTRIBUTING.md#L35-L49)

![GitHub 메타데이터에서 카탈로그를 갱신하고 영어·중국어 문서와 검증 보고서를 생성하는 흐름]({{ '/img/reviews/2026/awesome-agent-harness-catalog-review/catalog-flow.svg' | relative_url }})

리뷰어 작성, 분석 커밋 기준. 한 YAML에서 두 README를 만들고, 검증기는 YAML과 기존 README를 함께 읽습니다. [메타데이터 갱신](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/scripts/sync_github_metadata.py#L112-L183) · [README 출력](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/scripts/render_readme.py#L313-L333) · [검증과 보고서](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/scripts/verify_catalog.py#L100-L251)
{: .caption}

| 파일 | 읽는 입력 | 쓰는 출력 |
| --- | --- | --- |
| `scripts/sync_github_metadata.py` | 카탈로그, GitHub API 응답 | 갱신한 `data/projects.yaml` |
| `scripts/render_readme.py` | 카탈로그 | `README.md`와 `README_zh.md`, 또는 기존 문서와 비교 결과 |
| `scripts/verify_catalog.py` | 카탈로그, 두 README, 링크 응답 | 날짜별 검증 보고서와 종료 상태 |

## 작동 원리

### 1. 항목을 한 번 입력하고 두 언어에서 공유합니다

예를 들어 커밋의 **Playwright MCP** 항목은 프로토콜·도구 인터페이스·에이전트 계약 범주에 속합니다. 같은 행에 영문·중문 요약, 브라우저와 MCP 태그, 수록 이유가 들어 있습니다. 별은 스냅샷으로 **37,390개**, `updated_at`은 **2026-09-18**로 저장돼 있습니다. 이 날짜와 수는 해당 YAML 행의 값입니다. 생성된 영어·중국어 README의 225번째 줄에서 같은 이름과 같은 별 배지가 보이고, 요약만 언어별 필드에서 가져옵니다. [Playwright MCP 원본 행](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/data/projects.yaml#L1907-L1921) · [영어 README 행](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/README.md#L225) · [중국어 README 행](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/README_zh.md#L225)

기여자는 자료가 어떤 하네스 문제를 푸는지 설명하고, 어느 범주에 넣을지 판단합니다. 필수 필드에는 두 언어 요약과 `why_included`도 포함돼 있습니다. 별에 대한 최소 기준은 기여 문서에 없고, 별 수는 표 안에서 순서를 정하는 데 쓰입니다. 검증기의 필드 검사는 키가 존재하는지 확인합니다. 예를 들어 두 요약의 뜻이 같은지, 수록 이유가 충분히 구체적인지는 기여자가 확인해야 합니다. [기여 기준](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/CONTRIBUTING.md#L24-L33) · [필수 필드](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/scripts/render_readme.py#L25-L35) · [필드와 분류 검사](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/scripts/verify_catalog.py#L105-L117)

### 2. GitHub에서 가져온 값만 갱신합니다

동기화 스크립트는 YAML을 읽고 GitHub 저장소 URL에 맞는 항목을 고릅니다. 최대 12개 워커로 GitHub REST API를 조회합니다. `GITHUB_TOKEN`이 있으면 사용하고, 없으면 `gh auth token`을 시도합니다. API 요청이 실패하면 지수적으로 늘어나는 짧은 대기 시간을 두고 최대 세 번 요청한 뒤 `gh repo view`로 조회합니다. URL이 GitHub 저장소 패턴에 맞지 않는 참고 자료는 이 조회 대상에서 빠집니다. [토큰과 API](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/scripts/sync_github_metadata.py#L37-L55) · [재시도와 CLI 대체 경로](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/scripts/sync_github_metadata.py#L58-L102) · [대상 선택과 병렬 처리](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/scripts/sync_github_metadata.py#L112-L148)

다음은 코드의 분기와 저장 순서를 요약한 의사코드입니다. [동기화 진입점](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/scripts/sync_github_metadata.py#L112-L183)

```text
입력: projects.yaml의 항목 목록
GitHub 저장소 형식인 URL마다 메타데이터를 병렬 조회
  조회 실패 → 경고에 추가, 기존 행 보존
  조회 성공 → 별, 날짜, 라이선스 필드 갱신
             보관 또는 비공개로 표시된 경우 경고 추가
항목을 분류 순서, 별 내림차순, 이름순으로 정렬
last_verified에 실행 날짜를 기록하고 projects.yaml 저장
```

성공한 항목의 날짜는 GitHub 응답의 `pushed_at`을 우선 쓰고, 그 값이 비었으면 `updated_at`을 씁니다. 둘 다 없으면 `1970-01-01`을 채웁니다. 이 스크립트의 `updated_at` 필드는 코드가 선택한 활동일에 해당하므로, 저장소의 모든 메타데이터 변경 날짜와 항상 같지는 않습니다. 공개·비보관 저장소를 고르라는 수록 기준은 문서에 있지만, 동기화 코드는 보관 또는 비공개 상태를 감지하면 경고를 남긴 채 행을 보존합니다. 개별 조회가 실패한 경우에도 기존 행을 보존하고 마지막에 `last_verified`를 실행 날짜로 쓰므로, 그 날짜만 보고 전체 조회나 이후 검증이 성공했다고 판단하기는 어렵습니다. [수록 기준](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/docs/curation_policy.md#L14-L22) · [필드 처리와 YAML 저장](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/scripts/sync_github_metadata.py#L152-L189)

### 3. 두 README의 목차와 표를 같은 데이터에서 만듭니다

렌더러는 YAML이 선언한 범주 순서대로 항목을 모은 뒤, 각 범주에서 별 내림차순과 이름의 소문자 순으로 정렬합니다. 정렬을 생성 단계에서 다시 하므로 YAML 행의 입력 순서만 바꿔도 별이 다른 항목의 문서 순위는 유지됩니다. 별 배지는 YAML에 저장된 수를 URL에 넣어 만듭니다. 표에 넣는 값에는 파이프 기호와 줄바꿈을 처리하고, 요약에는 각각 `summary_en`과 `summary_zh`를 씁니다. [표 값 정리와 정렬](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/scripts/render_readme.py#L68-L93) · [별 배지](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/scripts/render_readme.py#L108-L122) · [영문 행](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/scripts/render_readme.py#L182-L204) · [중문 행](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/scripts/render_readme.py#L264-L286)

맨 위의 추천 글은 일반 프로젝트 표와 순위 기준이 다릅니다. 읽을거리 범주 중 GitHub 주소가 아닌 자료만 뽑고, 코드에 정의한 추천 이름 목록의 순서와 이름을 기준으로 정렬한 뒤 17개까지 노출합니다. 생성 명령의 `--check` 옵션은 두 파일을 다시 쓰는 대신 생성한 문자열과 기존 파일을 비교하고, 둘 중 하나라도 다르면 차이가 있다고 알리며 종료합니다. [추천 이름 목록](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/scripts/render_readme.py#L36-L57) · [추천 필터와 표시 상한](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/scripts/render_readme.py#L96-L105) · [렌더링 입력](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/scripts/render_readme.py#L125-L133) · [쓰기와 비교 모드](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/scripts/render_readme.py#L313-L333)

### 4. 구조 검사와 링크 검사의 결과를 보고서에 남깁니다

검증기는 필수 필드와 범주, 공백과 대소문자를 정리한 뒤의 중복 이름·URL을 검사합니다. GitHub 항목의 저장 날짜가 검사일보다 365일 넘게 오래되면 구조 오류로 잡습니다. 전체 항목 80개 이상, 읽을거리를 뺀 범주의 GitHub 비율 90% 이상을 오류 기준으로 쓰고, 전체 GitHub 비율이 80% 아래면 경고합니다. 이때 GitHub의 판정은 URL 문자열에 `github.com/`이 들어 있는지 확인하는 방식입니다. 이후 코드를 다시 호출해 두 README의 예상 텍스트를 만들고 체크아웃의 파일과 비교합니다. [구조·비율·README 비교](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/scripts/verify_catalog.py#L105-L169) · [GitHub 비율 함수](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/scripts/render_readme.py#L73-L77)

링크는 두 README에서 URL을 모아 중복을 제거하고 배지 이미지 호스트를 제외합니다. 최대 16개 워커로 응답을 검사하며, 먼저 `HEAD`를 보내고 필요한 경우 `GET`으로 다시 확인합니다. 2xx·3xx 응답과 특정 CDN 챌린지 헤더를 동반한 403은 코드가 접근 가능으로 분류합니다. 이 분류는 사람이 목적 페이지의 본문을 읽었다는 확인보다 좁습니다. `--skip-links`로 호출하면 네트워크 검사를 생략할 수 있습니다. 검증기는 오류가 있어도 집계와 세부 항목을 보고서에 쓴 뒤 종료 코드 1을 반환합니다. [HTTP 요청과 URL 수집](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/scripts/verify_catalog.py#L44-L92) · [옵션](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/scripts/verify_catalog.py#L100-L103) · [실행과 보고서](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/scripts/verify_catalog.py#L174-L251)

예를 들어 체크아웃에 포함된 **2026-10-08 보고서**에는 오래된 GitHub 항목 3건과 URL 376개 중 오류 1건이 남아 있습니다. 문제 URL의 당시 결과는 OpenReview PDF의 HTTP 403입니다. URL 수는 README에서 검사 대상으로 고른 주소의 개수로, 카탈로그 행 수 375와 다릅니다. 같은 커밋의 README에는 해당 날짜가 `Last verified`로 표시됩니다. 이 사례에서는 날짜 옆의 실제 판정과 오류를 읽으려면 보고서까지 열어야 합니다. [당시 검증 보고서](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/reports/verification/2026-10-08.md#L1-L35) · [README 날짜](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/README.md#L5-L10)

## 설치와 사용

기여 문서는 데이터 변경 후 아래 세 명령을 순서대로 실행하고, 생성된 README와 보고서를 변경분에 함께 넣도록 안내합니다. 세 스크립트는 Python에서 `yaml`을 import합니다. 이 글에서는 명령을 실행한 결과 대신 같은 커밋의 코드와 체크인된 예전 산출물을 읽었습니다. [기여 문서의 실행 순서](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/CONTRIBUTING.md#L35-L49) · [동기화 모듈 import](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/scripts/sync_github_metadata.py#L4-L17) · [렌더러 import](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/scripts/render_readme.py#L4-L9) · [검증기 import](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/scripts/verify_catalog.py#L4-L24)

```bash
python3 scripts/sync_github_metadata.py
python3 scripts/render_readme.py
python3 scripts/verify_catalog.py
```

## 한계와 분석 범위

기준 커밋에는 저장소 자체의 라이선스 파일이 보이지 않습니다. YAML 항목에 표시된 `license`는 각 등록 프로젝트에서 수집한 값입니다. 그 필드로 카탈로그의 문서나 스크립트의 재사용 조건까지 확인할 수는 없습니다. 검토 범위는 세 유지보수 스크립트와 그 입력·출력, 큐레이션 정책입니다. 연결된 프로젝트의 내부 구현이나 현재 링크 접근 상태는 평가 범위에서 벗어납니다. [고정 커밋의 파일 목록](https://github.com/Picrew/awesome-agent-harness/tree/e7e8f8d268f7ac5311b778832327e4be2f555507) · [항목별 라이선스 수집](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/scripts/sync_github_metadata.py#L105-L109) · [Playwright MCP 라이선스 필드](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/data/projects.yaml#L1913-L1921)

## 결론

Awesome Agent Harness에서는 편집자가 분류와 채택 이유를 YAML에 남기고, 스크립트가 GitHub 메타데이터를 갱신하며, 동일 입력에서 두 언어의 문서를 생성합니다. 항목의 수록 근거는 YAML에서, 출판용 문서의 일관성은 재생성 비교에서, 오래된 항목과 응답이 실패한 링크는 날짜별 보고서에서 확인할 수 있습니다. [데이터 계약](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/docs/curation_policy.md#L41-L54) · [검증 범위](https://github.com/Picrew/awesome-agent-harness/blob/e7e8f8d268f7ac5311b778832327e4be2f555507/docs/sources_and_verification.md#L18-L42)
