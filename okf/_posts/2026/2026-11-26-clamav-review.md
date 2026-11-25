---
type: "Repo Review"
title: "[Repo Review] ClamAV — 파일을 열고, 안을 살피고, 판정을 돌려주기까지"
description: "ClamAV의 DB 준비·파일 및 압축 재귀 검사·결과 집계를 따라가며, 탐지 판정과 처리 오류 및 종료 코드의 차이를 설명합니다."
date: "2026-11-26"
tags:
  - "Repo Review"
  - "Tools"
  - "Linux"
resource: "https://github.com/Cisco-Talos/clamav/tree/cad7b18a3e6505195fe08db1412449a18fc9f012"
generated:
  by: "process:blog-review"
  at: "2026-11-26T06:02:44.462108+09:00"
sources:
  - id: "github:cisco-talos/clamav"
    resource: "https://github.com/Cisco-Talos/clamav/tree/cad7b18a3e6505195fe08db1412449a18fc9f012"
    title: "ClamAV"
    author: "The ClamAV Team"
status: "stable"
year: "2026"
analyzed_at: "2026-11-26T06:02:44.462108+09:00"
source_id: "cisco-talos/clamav"
source_revision: "cad7b18a3e6505195fe08db1412449a18fc9f012"
source_type: "repo"
source_url: "https://github.com/Cisco-Talos/clamav/tree/cad7b18a3e6505195fe08db1412449a18fc9f012"
visual_sources:
  - path: "img/reviews/2026/clamav-review/scan-pipeline.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/clamscan/manager.c#L1594-L1663"
    caption: "clamscan의 엔진 준비·입력 검사·결과 집계 흐름. 리뷰어 작성, 분석 커밋 기준."
  - path: "img/reviews/2026/clamav-review/archive-recursion.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/libclamav/unzip.h#L72-L82"
    caption: "ZIP 내부 파일을 같은 형식별 검사 경로로 보내는 재귀 구조. 리뷰어 작성, 분석 커밋 기준."
---

## 들어가며: 파일 하나를 검사한다는 말의 안쪽

메일 첨부파일이나 업로드된 ZIP 파일을 받았을 때, 서버가 알고 싶은 것은 단순합니다. 이 파일을 그대로 전달해도 될까요? 파일의 확장자를 읽거나 프로그램이 정상 종료됐는지 확인하는 것만으로는 답하기 어렵습니다. 압축파일 안에 다른 파일이 있고, 검사기가 읽지 못한 부분도 있을 수 있기 때문입니다.

**ClamAV**는 트로이목마·바이러스·악성코드 등을 탐지하는 오픈소스 안티바이러스 엔진입니다. 이 글에서는 많은 기능 중 `clamscan`이 로컬 파일을 받아 검사하고 결과를 반환하는 경로를 따라갑니다. 시그니처 데이터베이스를 준비하는 단계, 파일을 해석하는 단계, 발견 결과를 출력하는 단계가 어떻게 이어지는지가 관심사입니다. [프로젝트의 정의](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/README.md#L7-L10)를 코드와 함께 살펴보겠습니다.

분석 기준은 커밋 `cad7b18a3e6505195fe08db1412449a18fc9f012`입니다. 이 커밋의 CMake 설정은 `1.6.0`과 개발 버전 접미사를 사용하므로, 여기서 읽은 API를 배포판에 설치된 안정 버전의 API와 곧바로 같다고 보면 안 됩니다. 대상 소프트웨어를 설치·빌드·실행하거나 탐지율을 측정하지 않았습니다. [버전 설정](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/CMakeLists.txt#L12-L23)에 범위를 고정한 정적 코드 리뷰입니다.

## 무엇인가: 검사 엔진과 주변 프로그램의 역할

ClamAV는 하나의 실행 파일로만 구성되지 않습니다. 검사 로직을 제공하는 라이브러리와, 그 라이브러리를 호출하거나 데이터를 준비하는 프로그램이 나뉩니다.

| 구성 요소 | 하는 일 | 이 글의 분석 범위 |
| --- | --- | --- |
| `libclamav` | 파일 형식 판별, 압축·문서 파싱, 시그니처 검사와 결과 구성 | 파일 하나의 대표 검사 경로 |
| `clamscan` | 엔진과 DB를 준비한 뒤 파일·디렉터리·표준입력을 검사하는 CLI | 시작부터 최종 종료 코드까지 |
| `clamd` | Unix/TCP 소켓으로 요청을 받는 검사 데몬 | 역할만 확인 |
| `clamdscan` | `clamd`에 검사 요청을 보내는 클라이언트 | 역할과 설정 경계만 확인 |
| `freshclam` | 바이러스 데이터베이스 업데이트 도구 | 검사기와의 역할 구분 |

[clamd 매뉴얼](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/docs/man/clamd.8.in#L1-L10)은 요청을 받아 검사하는 데몬을, [clamdscan 매뉴얼](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/docs/man/clamdscan.1.in#L1-L10)은 그 클라이언트를 설명합니다. 특히 `clamdscan`은 `clamscan`과 비슷한 옵션을 받아도 검사 능력은 데몬에 의존하며, 상당수 옵션을 무시한다고 명시합니다. 명령어 이름이 비슷하다고 같은 프로세스에서 같은 설정으로 검사하는 것은 아닙니다. [FreshClam의 역할](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/docs/man/freshclam.1.in#L1-L13)도 파일 검사가 아니라 DB 업데이트입니다.

ClamAV의 **시그니처(signature)**는 악성코드 등을 식별하기 위한 탐지 규칙입니다. 이는 패키지 버전의 CVE를 대조하는 검사와 다른 작업입니다. 이 저장소를 읽을 때는 “어떤 취약한 패키지를 쓰는가”보다 “입력 파일과 내부 내용에서 어떤 탐지 근거를 찾는가”에 초점을 맞추는 편이 이해하기 쉽습니다.

## 아키텍처: 준비·검사·결과를 연결하는 CLI

대표 흐름은 `clamscan/clamscan.c`의 `main()`에서 시작합니다. 명령행 옵션을 파싱하고 출력·재귀·후속 작업 설정을 준비한 뒤, `scanmanager()`를 호출합니다. 실제 검사 후에는 통계 요약을 출력하고 반환받은 코드를 프로세스 종료 코드로 돌려줍니다. [진입점과 옵션 처리](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/clamscan/clamscan.c#L105-L185), [요약과 반환](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/clamscan/clamscan.c#L187-L244)을 나누어 보면 CLI의 책임이 드러납니다.

| 파일·디렉터리 | 읽은 책임 |
| --- | --- |
| `clamscan/clamscan.c` | CLI 진입점과 최종 요약 |
| `clamscan/manager.c` | 엔진 준비, 검사 대상 순회, 파일 검사와 결과 집계 |
| `libclamav/readdb.c` | 시그니처 DB 적재와 엔진 컴파일 |
| `libclamav/scanners.c` | 파일 매핑, 형식별 파서 연결, 검사 문맥과 판정 |
| `libclamav/unzip.c`, `unzip.h` | ZIP 항목 추출과 내부 파일 검사 콜백 |
| `libclamav/matcher.c` | 패턴 매칭과 발견 근거 전달 |
| `libclamav/clamav.h` | 외부 API와 판정 타입 |
| `docs/man/` | 같은 커밋의 명령·옵션·종료 코드 설명 |

CMake 설정에는 Rust 도구 체인 요구도 있고, `libclamav_rust/Cargo.toml`은 `staticlib`를 정의합니다. 따라서 이 프로젝트 전체를 순수 C 프로그램으로 설명할 수는 없습니다. 아래에서 따라가는 CLI와 검사 조정 코드는 주로 C에 있습니다. [빌드 요구](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/CMakeLists.txt#L125-L138), [Rust 라이브러리 매니페스트](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/libclamav_rust/Cargo.toml#L1-L45)를 기준으로 구분했습니다.

![옵션과 DB로 엔진을 준비한 뒤 입력 파일을 검사하고 판정과 오류를 집계하는 ClamAV 흐름]({{ '/img/reviews/2026/clamav-review/scan-pipeline.svg' | relative_url }})

`clamscan`의 준비·검사·출력 흐름입니다. 리뷰어 작성, 분석 커밋 기준. 출처: [엔진 초기화](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/clamscan/manager.c#L1393-L1405), [검사 진입](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/clamscan/manager.c#L1991-L2015), [결과 집계](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/clamscan/manager.c#L2032-L2042).
{: .caption}

## 작동 원리: 파일에서 판정까지

### 1. DB를 읽고, 검사에 쓸 엔진을 준비합니다

`scanmanager()`는 `cl_init()`으로 라이브러리를 초기화하고 `cl_engine_new()`로 엔진을 만듭니다. 탐지 알림을 출력할 콜백도 엔진에 등록합니다. 이후 사용자가 `--database`로 지정한 경로나 기본 DB 디렉터리에서 `cl_load()`를 호출하고, `cl_engine_compile()`로 준비를 마칩니다. 준비 과정에서 오류가 생기면 검사로 넘어가지 않고 오류 종료 경로로 갑니다. [초기화](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/clamscan/manager.c#L1393-L1405), [DB 적재·컴파일](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/clamscan/manager.c#L1594-L1663)에 이 순서가 있습니다.

여기서 **컴파일**은 소스 코드를 실행 파일로 빌드한다는 뜻이 아닙니다. 적재한 탐지 정보를 검사에 사용할 내부 자료구조로 준비하는 과정입니다. `cl_engine_compile()`은 매처별 Aho–Corasick 트라이와 PCRE 정규식 준비 함수를 호출합니다. 트라이는 여러 문자열 패턴을 함께 탐색하기 위한 구조이고, PCRE는 정규식 패턴을 다루는 엔진입니다. [실제 준비 루프](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/libclamav/readdb.c#L6127-L6138)를 보면 DB 파일 읽기와 검사 자료구조 준비가 별도 단계라는 것을 알 수 있습니다.

`cl_load()` 자체도 파일과 디렉터리를 구분하여 각각 DB 파일 적재 또는 DB 디렉터리 적재 함수로 연결합니다. 이미 컴파일된 엔진에 새 DB를 적재하려 하면 오류를 반환합니다. 이것은 **적재 → 준비 → 검사**라는 API 사용 순서를 보여 줍니다. [적재 시 사전 조건](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/libclamav/readdb.c#L5373-L5388), [파일·디렉터리 분기](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/libclamav/readdb.c#L5454-L5464)를 확인했습니다.

### 2. 입력을 순회하고 파일 디스크립터를 넘깁니다

파일 인자가 주어지면 `scan_files()`가 목록을 순회합니다. `-`는 표준입력으로, 일반 파일은 `scanfile()`로, 디렉터리는 `scandirs()`로 연결합니다. 심볼릭 링크는 설정에 따라 따르거나 건너뜁니다. 인자가 없다면 현재 디렉터리를 대상으로 합니다. [입력 분기](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/clamscan/manager.c#L1254-L1329), [인자 없는 경우](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/clamscan/manager.c#L1991-L2015)에서 확인할 수 있습니다.

`scanfile()`은 검사 대상 파일을 열고 `cl_scandesc_ex()`에 **파일 디스크립터(fd)**를 전달합니다. fd는 운영체제가 열린 파일을 식별하는 번호입니다. 이 호출에는 엔진과 검사 옵션뿐 아니라 판정·알림 이름·검사한 바이트 수를 받을 출력 인자도 들어갑니다. [파일 열기와 API 호출](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/clamscan/manager.c#L464-L487)이 CLI와 엔진의 경계입니다.

엔진 쪽 `cl_scandesc_ex()`는 파일 크기 등을 확인하고 `fmap_new()`로 파일 내용을 읽는 매핑을 준비한 뒤 `scan_common()`으로 연결합니다. `scan_common()`은 검사 문맥을 구성하여 `cli_magic_scan()`을 호출합니다. [매핑과 공통 검사 호출](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/libclamav/scanners.c#L6492-L6561), [형식별 검사 진입](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/libclamav/scanners.c#L6173-L6176)이 이어집니다.

### 3. ZIP은 바깥 파일과 내부 파일을 함께 다룹니다

확장자만 보고 형식을 정하는 구조는 아닙니다. 별도 형식 힌트가 없는 일반 경로에서는 `cli_magic_scan()`이 매핑된 내용으로 형식을 판별합니다. 이후 형식과 검사 옵션에 맞는 파서를 선택합니다. ZIP이면 아카이브 파싱 옵션과 해당 형식 설정을 확인한 뒤 `cli_unzip()` 등으로 연결합니다. [내용 기반 형식 판별](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/libclamav/scanners.c#L4780-L4797), [ZIP 분기](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/libclamav/scanners.c#L5056-L5066)가 근거입니다.

`cli_unzip()`은 ZIP의 항목 목록을 바탕으로 각 항목을 복호화하거나 압축 해제하는 경로를 택합니다. 추출된 파일을 처리하는 기본 콜백 `zip_scan_cb`는 `cli_magic_scan_desc`로 정의되어 있습니다. 이 함수는 다시 `cli_magic_scan()`으로 이어집니다. 즉, ZIP 안에 또 다른 ZIP이 있을 때도 내부 파일을 새 검사 대상으로 다루는 연결 구조입니다. [항목별 추출](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/libclamav/unzip.c#L1872-L1926), [콜백 정의](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/libclamav/unzip.h#L72-L82), [내부 파일 검사](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/libclamav/scanners.c#L5647-L5700)를 함께 보면 재귀가 어디서 생기는지 드러납니다.

![ZIP의 항목을 추출한 뒤 내부 파일을 다시 형식 판별과 검사에 보내는 재귀 구조]({{ '/img/reviews/2026/clamav-review/archive-recursion.svg' | relative_url }})

ZIP 내부 파일이 같은 검사 경로로 돌아오는 구조입니다. 리뷰어 작성, 분석 커밋 기준. 출처: [ZIP 파서 연결](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/libclamav/scanners.c#L5056-L5066), [추출 후 검사 콜백](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/libclamav/unzip.h#L72-L82).
{: .caption}

이 도식은 대표 연결을 줄여 그린 것입니다. 모든 파일이 반드시 “압축 해제 후 한 번만 패턴 검사”라는 똑같은 순서를 밟지는 않습니다. `cli_magic_scan()`에는 파서 없이 원시 패턴 매칭만 하는 경로도 있고, 형식별 파싱 전후의 raw 검사와 조기 종료 조건도 있습니다. [raw 모드·사전 검사](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/libclamav/scanners.c#L4930-L4959), [파서 이후 검사](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/libclamav/scanners.c#L5391-L5424)를 보면 파일 형식과 설정에 따라 흐름이 달라집니다.

### 4. 매칭 결과를 근거로 모으고 판정합니다

패턴 매처에는 Boyer–Moore 계열 검사와 Aho–Corasick 검사를 호출하는 코드가 있습니다. 전자는 문자열 패턴 탐색 방식의 하나이고, 후자는 여러 패턴을 함께 찾기 위한 방식입니다. 이 경로에서 발견한 시그니처는 `cli_append_virus()`로 검사 문맥에 전달됩니다. 이는 전체 탐지 방식 중 읽은 대표 패턴 매칭 경로이며, 모든 탐지를 두 알고리즘만으로 설명하는 것은 아닙니다. [매처와 발견 결과 전달](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/libclamav/matcher.c#L143-L174)을 기준으로 설명했습니다.

엔진은 각 검사 계층에서 수집한 **근거(evidence)**를 보고 판정합니다. 해당 계층이 trusted로 처리됐다면 그 판정을 유지하고, 그 외에는 strong indicator가 있는지, potentially unwanted indicator가 있는지를 순서대로 확인합니다. `scan_common()`은 최종 판정과 알림 이름을 출력 인자로 반환합니다. [근거에서 판정을 만드는 코드](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/libclamav/scanners.c#L4552-L4572), [출력 인자 설정](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/libclamav/scanners.c#L6233-L6238)이 이 경계입니다.

### 5. 검사 오류와 탐지 판정은 서로 다른 값입니다

이 커밋에서 특히 눈여겨볼 부분입니다. `clamscan`이 호출하는 `cl_scandesc_ex()`는 처리 상태인 `ret`와 탐지 판정인 `verdict`를 따로 돌려줍니다. 내부 공통 검사 함수의 주석도 시그니처 매치를 `CL_VIRUS` 반환값으로 판단하지 말고 `verdict_out`을 보라고 명시합니다. [API의 설명](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/libclamav/scanners.c#L5897-L5905)을 놓치면 성공 반환값을 잘못 해석할 수 있습니다.

| 판정 | 헤더에 정의된 의미 | `clamscan` 파일 집계 |
| --- | --- | --- |
| `NOTHING_FOUND` | 알림 대상 시그니처가 발견되지 않음 | `ret`도 성공일 때 `OK`, 아니면 오류 집계 |
| `TRUSTED` | 오탐 방지 시그니처나 Authenticode 등으로 신뢰 처리됨 | `OK`로 표시하는 경로 |
| `STRONG_INDICATOR` | 강한 탐지 지표 시그니처가 하나 이상 매치됨 | 발견 파일 수 증가 |
| `POTENTIALLY_UNWANTED` | 잠재적으로 원치 않는 항목의 시그니처가 매치됨 | 발견 파일 수 증가 |

판정 이름은 실제 상수의 `CL_VERDICT_` 접두사를 생략한 것입니다. [판정 타입](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/libclamav/clamav.h#L87-L92)과 [CLI의 판정 분기](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/clamscan/manager.c#L489-L530)를 대조했습니다. “오류 없이 처리됨”, “아무것도 발견하지 못함”, “신뢰 처리됨”은 같은 말이 아닙니다.

아래는 그 분기를 읽기 쉽게 다시 쓴 **의사코드**입니다. 실제 API 인자와 알림 콜백·후속 작업은 생략했습니다. 실행 결과를 재현한 예제가 아닙니다.

```text
처리 상태, 판정, 알림 이름 = 파일 검사(fd, 엔진, 옵션)

판정이 STRONG_INDICATOR 또는 POTENTIALLY_UNWANTED이면:
    검사 파일 수와 발견 파일 수를 증가시킴
그 외에 판정이 TRUSTED이면:
    검사 파일 수 증가, 설정에 따라 OK 출력
그 외에 처리 상태가 성공이면:
    검사 파일 수 증가, 설정에 따라 OK 출력
그 외에는:
    오류 수 증가, 설정에 따라 ERROR 출력
```

이후 `scanmanager()`는 여러 파일의 집계로 프로세스 종료 코드를 결정합니다. 아래는 [원본의 짧은 발췌](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/clamscan/manager.c#L2032-L2042)이며, 주변의 엔진 해제 코드는 생략했습니다. 출처는 해당 커밋의 ClamAV 코드이고 라이선스는 GPLv2입니다.

```c
if (info.ifiles)
    ret = 1;
else if (info.errors)
    ret = 2;

return ret;
```

파일 하나라도 발견으로 집계되면 `1`이 우선합니다. 발견 파일이 없고 오류가 있으면 `2`입니다. 따라서 여러 파일을 검사할 때 **종료 코드 `1`만 보고 다른 파일에 오류가 없었다고 결론 내릴 수 없습니다.** 요약 출력은 `info.errors`도 따로 보고합니다. [최종 요약](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/clamscan/clamscan.c#L196-L203)과 함께 해석해야 합니다.

## 설치와 사용: 같은 버전의 매뉴얼을 기준으로

README는 Docker, 패키지 매니저, 운영체제별 설치 프로그램, 소스 빌드 경로를 안내합니다. 이 리뷰에서 설치를 수행하지 않았으므로 특정 환경에서의 설치 성공이나 실행 시간을 확인한 것으로 쓰지 않습니다. [설치 안내](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/README.md#L40-L78)는 배포 환경에 맞는 경로를 선택하는 출발점입니다.

다음 명령은 이 커밋의 `clamscan` 매뉴얼에 있는 예시입니다. `file`은 검사 대상 파일을, `/home`은 예시에 쓰인 디렉터리를 뜻합니다. 실제 파일이나 악성코드를 내려받아 실행한 기록이 아닙니다. [원문 예시](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/docs/man/clamscan.1.in#L317-L342)를 그대로 따릅니다.

```bash
clamscan file
clamscan -r /home
cat testfile | clamscan -
```

`-r`은 디렉터리 순회 옵션입니다. ZIP 내부의 재귀 파싱과 디렉터리 하위 폴더를 내려가는 재귀는 서로 다른 층위이므로 구별해야 합니다. `--database`는 DB 파일·디렉터리를 지정하고, `--allmatch`는 하나의 파일에서 매치를 찾은 뒤에도 추가 매치를 계속 찾는 옵션입니다. [DB와 재귀·allmatch 옵션](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/docs/man/clamscan.1.in#L69-L85)에 정의되어 있습니다.

## 한계와 주의점: 발견 없음과 검사 범위를 함께 읽기

**검사에는 자원 상한이 있습니다.** 매뉴얼은 파일 크기·총 검사 크기·내부 파일 수·압축 재귀 깊이 제한이 서비스 거부 공격에 대한 방어라고 설명합니다. 이 커밋의 매뉴얼 기본값은 파일당 100 MB, 총 검사 크기 400 MB, 내부 파일 수 10,000개, 압축 재귀 깊이 17입니다. 총 검사 크기는 바깥 아카이브와 내부 파일 크기를 함께 계산하므로, 압축파일의 디스크 크기와 같은 개념이 아닙니다. [제한의 정의와 기본값](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/docs/man/clamscan.1.in#L232-L244)이 근거입니다.

상한을 넘었다고 항상 오류 코드 하나로 명확히 드러나는 것은 아닙니다. 매뉴얼에는 큰 파일을 검사하지 않는다는 설명과, 상한 초과를 `Heuristics.Limits.Exceeded` 알림으로 표시하는 별도 옵션이 있습니다. 코드도 최상위 파일이 `maxfilesize`를 넘으면 본 검사로 진입하지 않는 분기를 갖습니다. 따라서 결과의 `OK`나 종료 코드만 읽는 대신 **사용한 DB·검사 설정·경고·생략된 범위**를 함께 읽어야 합니다. [상한 초과 알림](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/docs/man/clamscan.1.in#L212-L214), [크기 검사 분기](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/libclamav/scanners.c#L6517-L6535)를 근거로 한 해석입니다.

**암호화된 파일이라는 사실과 내부 내용을 확인했다는 사실도 다릅니다.** ZIP 구현에는 복호화 경로가 있지만 입력 내용을 확보하지 못해 건너뛰는 분기도 있고, 암호화된 아카이브·문서를 알리기 위한 옵션은 따로 있습니다. “ZIP 지원”을 모든 암호화된 ZIP의 내용을 항상 검사한다는 뜻으로 확대하면 안 됩니다. [ZIP 처리 분기](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/libclamav/unzip.c#L1894-L1932), [암호화 알림 옵션](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/docs/man/clamscan.1.in#L201-L208)을 구분해서 보아야 합니다.

**데이터베이스의 상태도 검사 결과의 조건입니다.** 이 커밋은 `--fail-if-cvd-older-than` 옵션으로 지정한 일수보다 오래된 DB일 때 실패하도록 하는 선택지를 제공합니다. 파일 검사를 시작할 수 있다는 것과 최신 탐지 데이터를 쓴다는 것은 별개입니다. [옵션 정의](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/docs/man/clamscan.1.in#L69-L76)와 [DB 적재 전 검사](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/clamscan/manager.c#L1594-L1637)에서 확인했습니다. 이 글은 실제 DB를 받거나 검사하지 않았으므로 탐지 범위·오탐률에 대한 측정 결과는 없습니다.

**라이선스는 구성 요소별로 확인해야 합니다.** README는 ClamAV를 GPLv2로 설명하며, 포함된 타사 코드에는 다른 라이선스가 있다고 명시합니다. UnRAR 코드는 제한이 있는 별도 라이선스이고, README는 그 라이브러리를 사용할 수 없으면 RAR 지원 없이 계속 동작한다고 설명합니다. [프로젝트와 타사 라이선스 안내](https://github.com/Cisco-Talos/clamav/blob/cad7b18a3e6505195fe08db1412449a18fc9f012/README.md#L103-L139)를 기준으로 한 설명이며, 모든 파일을 동일한 라이선스로 가정하지 않았습니다.

## 정리: 검사 결과는 입력과 설정을 통과해 만들어집니다

ClamAV의 대표 파일 검사 경로는 DB 적재와 엔진 준비에서 시작해, 파일 형식 판별·내부 내용 파싱·패턴 매칭을 거쳐 판정과 오류를 반환합니다. CLI는 그 결과를 파일별 출력과 전체 집계로 바꾸고, 발견 여부를 우선하여 종료 코드를 정합니다.

이 코드를 읽으며 얻을 수 있는 핵심은 결과의 층위를 구별하는 데 있습니다. API 처리 상태와 탐지 판정, 디렉터리 순회와 압축 재귀, 검사 수행과 DB 업데이트는 각각 다른 책임입니다. 이 경계를 함께 읽어야 결과에 적힌 `OK`, `FOUND`, 종료 코드가 어느 범위의 검사에서 나왔는지 이해할 수 있습니다.

### 이 글에서 다루지 못한 부분

대표 `clamscan` 파일 경로와 ZIP 연결을 중심으로 확인했습니다. `clamd`의 동시성·소켓 프로토콜 구현, FreshClam의 다운로드·배포 검증 전체 흐름, on-access 검사, 바이트코드·YARA·각 문서/실행파일 파서의 내부 알고리즘, 개별 시그니처의 정확도는 상세 분석하거나 실행 검증하지 않았습니다.
