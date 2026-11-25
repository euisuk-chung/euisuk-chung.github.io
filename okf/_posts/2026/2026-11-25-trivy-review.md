---
type: "Repo Review"
title: "[Repo Review] Trivy — 이미지 속 패키지가 취약점 보고서가 되기까지"
description: "Trivy의 이미지 분석·OS별 취약점 매칭·필터·보고 흐름을 따라가며, 패키지 식별과 알려진 취약점 판정 및 종료 코드의 차이를 설명합니다."
date: "2026-11-25"
tags:
  - "Repo Review"
  - "Tools"
  - "Linux"
resource: "https://github.com/aquasecurity/trivy/tree/c14584a6c49d9cf4cf62d54281437bf2d97864d6"
generated:
  by: "process:blog-review"
  at: "2026-11-25T06:03:00.140265+09:00"
sources:
  - id: "github:aquasecurity/trivy"
    resource: "https://github.com/aquasecurity/trivy/tree/c14584a6c49d9cf4cf62d54281437bf2d97864d6"
    title: "Trivy"
    author: "Aqua Security"
status: "stable"
year: "2026"
analyzed_at: "2026-11-25T06:03:00.140265+09:00"
source_id: "aquasecurity/trivy"
source_revision: "c14584a6c49d9cf4cf62d54281437bf2d97864d6"
source_type: "repo"
source_url: "https://github.com/aquasecurity/trivy/tree/c14584a6c49d9cf4cf62d54281437bf2d97864d6"
visual_sources:
  - path: "img/reviews/2026/trivy-review/image-scan-flow.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/pkg/commands/artifact/run.go#L422-L467"
    caption: "컨테이너 이미지 standalone 검사에서 분석·검출·결과 처리로 이어지는 흐름. 리뷰어 작성, 분석 커밋 기준."
  - path: "img/reviews/2026/trivy-review/finding-and-exit.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/pkg/commands/operation/operation.go#L122-L133"
    caption: "필터 후 발견 여부와 프로세스 종료 코드의 조건. 리뷰어 작성, 분석 커밋 기준."
---

<!-- paper-video:start -->
<div style="position: relative; width: 100%; padding-top: 56.25%; margin-bottom: 1rem;">
  <iframe src="https://www.youtube-nocookie.com/embed/NU_tLyLwcdY"
    title="레포 리뷰 영상" loading="lazy" referrerpolicy="strict-origin-when-cross-origin"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowfullscreen style="position: absolute; inset: 0; width: 100%; height: 100%; border: 0;"></iframe>
</div>
<p><a href="https://www.youtube.com/watch?v=NU_tLyLwcdY">YouTube에서 영상 보기</a></p>
<!-- paper-video:end -->

## 들어가며: 취약점 목록은 어디서 나올까요

Trivy의 취약점 보고서에는 패키지 이름, CVE 번호, 설치된 버전과 수정 버전 등이 담깁니다. 이 목록은 소스 코드를 읽고 새로운 버그를 추론해서 만든 것일까요? 아니면 이미지 안의 구성 요소를 찾아 이미 알려진 보안 정보와 대조한 것일까요?

**Trivy**를 이해하려면 먼저 이 차이를 짚어야 합니다. 이 저장소의 취약점 검사 경로는 이미지 안에서 OS와 패키지 정보를 추출한 뒤, 해당 생태계의 보안 권고와 버전을 대조합니다. 같은 도구 안에 설정 오류, 비밀정보, 라이선스 검사도 있지만 각각 보는 정보와 판정 방식은 다릅니다.

이 글은 커밋 `c14584a6c49d9cf4cf62d54281437bf2d97864d6`의 코드를 정적으로 읽은 리뷰입니다. **컨테이너 이미지를 로컬에서 검사하는 standalone 경로**, 그중 OS 패키지 취약점 검출을 중심으로 따라갑니다. 대상 프로그램을 설치하거나 실행하지 않았으며 탐지율이나 실제 검사 시간을 측정하지 않았습니다. [분석한 저장소 버전](https://github.com/aquasecurity/trivy/tree/c14584a6c49d9cf4cf62d54281437bf2d97864d6)에 범위를 고정합니다.

## 무엇인가: 검사 대상과 검사 종류를 조합하는 도구

README는 Trivy를 여러 검사 대상과 여러 스캐너를 가진 보안 검사 도구로 소개합니다. 여기서 **대상(target)**은 무엇을 읽을지, **스캐너(scanner)**는 무엇을 찾을지를 뜻합니다. 컨테이너 이미지를 검사한다는 말만으로 모든 보안 검사를 수행한다는 뜻은 아닙니다. [README의 대상·스캐너 구분](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/README.md#L14-L33)이 출발점입니다.

| 구분 | 예시 | 읽을 때 구별할 점 |
| --- | --- | --- |
| 대상 | 이미지, 파일시스템, Git 저장소, VM 이미지, Kubernetes | 입력을 얻고 분석하는 방식이 달라집니다. |
| 취약점 검사 | OS 패키지·언어 의존성의 알려진 보안 문제 | 패키지 식별과 보안 데이터베이스가 필요합니다. |
| 설정 검사 | IaC 등의 잘못된 설정 | 패키지의 CVE 목록과 같은 종류의 판정이 아닙니다. |
| 비밀정보 검사 | 파일에 포함된 민감 문자열 | 취약한 라이브러리 버전을 찾는 작업과 구별됩니다. |
| SBOM | 소프트웨어 구성 요소 목록 | 목록을 만들었다는 사실과 보안상 안전하다는 판정은 다릅니다. |

이 커밋의 공통 `--scanners` 기본값은 `vuln,secret`입니다. 설정 오류와 라이선스 검사를 모두 기본으로 켜는 값은 아닙니다. 컨테이너 이미지 명령은 별도로 crypto 선택지도 추가하지만 기본으로 켜지는 것은 아니라고 명시합니다. [공통 기본값](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/pkg/flag/scan_flags.go#L41-L80), [이미지 명령의 추가 선택지](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/pkg/commands/app.go#L270-L274)를 함께 봐야 합니다.

## 아키텍처: 입력 분석과 보안 판정 사이에 경계가 있습니다

Trivy는 Go로 작성됐으며, 이 커밋의 모듈은 `github.com/aquasecurity/trivy`입니다. CLI는 Cobra 명령으로 구성되고, 내부에서 artifact runner가 검사 종류와 실행 방식을 연결합니다. 아래는 이 글에서 따라갈 파일들입니다. [모듈 선언](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/go.mod#L1-L3)과 [이미지 명령](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/pkg/commands/app.go#L251-L348)을 기준으로 정리했습니다.

| 경로 | 핵심 책임 |
| --- | --- |
| `cmd/trivy/main.go` | 명령 실행과 최종 프로세스 종료 코드 처리 |
| `pkg/commands/app.go` | `image` 같은 하위 명령과 플래그 구성 |
| `pkg/commands/artifact/run.go` | DB 준비, 대상별 검사, 필터, 보고, 종료 판단 연결 |
| `pkg/fanal/artifact/image/` | 이미지·레이어 분석과 분석 결과 캐시 |
| `pkg/fanal/applier/` | 레이어별 분석 정보를 적용해 검사할 상태 구성 |
| `pkg/scan/local/`, `pkg/scan/ospkg/` | 로컬 검사와 OS 패키지 검사 조정 |
| `pkg/detector/ospkg/` | 배포판별 보안 권고 조회·버전 판정 |
| `pkg/result/`, `pkg/report/` | 발견 결과의 필터링과 출력 형식 선택 |

![CLI 구성에서 이미지 분석, OS별 취약점 매칭과 결과 처리로 이어지는 네 단계]({{ '/img/reviews/2026/trivy-review/image-scan-flow.svg' | relative_url }})

컨테이너 이미지 standalone 검사의 대표 흐름입니다. 리뷰어 작성, 분석 커밋 기준. 출처: [대상별 검사와 결과 처리](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/pkg/commands/artifact/run.go#L422-L467), [로컬 서비스 구성](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/pkg/commands/artifact/scanner.go#L246-L267).
{: .caption}

도식에서 **이미지 분석**과 **취약점 매칭**을 나눈 이유가 있습니다. 전자는 어떤 패키지가 들어 있는지 알아내는 일이고, 후자는 그 패키지가 어떤 보안 권고에 해당하는지 판단하는 일입니다. 이미지 분석 결과를 캐시해도 취약점 정보가 같다는 뜻은 아닙니다.

## 작동 원리 1: 명령 하나가 검사 구성을 만듭니다

`main`은 명령 처리 중 반환된 오류가 `ExitError`이면 그 안의 코드를 프로세스 종료 코드로 사용합니다. 일반 실행 경로는 `commands.Run`으로 이어지고, `image` 하위 명령의 `RunE`는 입력과 플래그를 `Options`로 변환해 `artifact.Run`을 호출합니다. [최상위 진입점](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/cmd/trivy/main.go#L18-L49), [이미지 명령 실행부](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/pkg/commands/app.go#L325-L335)가 연결됩니다.

이미지 명령은 다시 두 조건으로 갈립니다. 입력이 이미지 이름인지 tar 아카이브인지, 그리고 서버 주소가 있는지입니다. 이름을 주고 서버 주소를 지정하지 않으면 이 글의 `imageStandaloneScanService`로 갑니다. 같은 `image` 명령이라도 tar 입력이나 client/server 모드이면 다른 초기화 함수를 선택합니다. [네 가지 분기](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/pkg/commands/artifact/run.go#L199-L220)가 그 차이를 명시합니다.

runner는 필요한 취약점 DB를 먼저 준비합니다. 취약점 스캐너가 꺼져 있거나 서버 모드의 클라이언트이면 로컬 취약점 DB 초기화를 생략합니다. 로컬 취약점 검사에서는 DB 업데이트 필요 여부를 확인하고 필요하면 내려받은 뒤 DB를 엽니다. `--download-db-only`이면 이 준비 단계에서 검사를 건너뛰는 경로도 있습니다. [DB 초기화 조건](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/pkg/commands/artifact/run.go#L325-L350), [업데이트 필요 여부와 다운로드](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/pkg/commands/operation/operation.go#L24-L52)에 근거한 설명입니다.

여기서 standalone은 검사 서버를 별도로 지정하지 않는다는 뜻입니다. 네트워크를 전혀 사용하지 않는다는 뜻은 아닙니다. 이미지와 DB를 얻는 일은 여전히 외부 자원을 필요로 할 수 있습니다.

## 작동 원리 2: 파일과 레이어를 읽어 구성 요소를 알아냅니다

로컬 서비스 초기화는 캐시, 레이어 적용기, OS·언어 패키지 스캐너와 취약점 정보 클라이언트를 묶습니다. 이미지 입력을 다루는 artifact 객체도 이때 만듭니다. 그다음 공통 `ScanArtifact`가 `artifact.Inspect`를 먼저 호출하고, 나온 artifact ID와 blob ID 목록을 검사 backend에 전달합니다. [의존성 연결](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/pkg/commands/artifact/scanner.go#L246-L267), [분석 후 검사 호출](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/pkg/scan/service.go#L47-L65)의 순서입니다.

이미지의 `Inspect`는 이미지 ID·설정·레이어 DiffID를 읽고 캐시 키를 계산합니다. 캐시에서 빠진 이미지·레이어를 찾아 필요한 부분을 분석한 뒤, 전체 레이어의 키를 반환합니다. **같은 레이어가 이미 분석돼 있으면 그 분석 정보를 재사용하는 구조**입니다. 단, 그보다 먼저 시도하는 외부 SBOM 조회가 성공하면 일반 레이어 분석 대신 그 SBOM 결과로 돌아갑니다. 아래 설명은 이 조기 반환이 일어나지 않은 일반 분석 경로입니다. [캐시 조회와 분석 호출](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/pkg/fanal/artifact/image/image.go#L89-L171)을 보면 원본 이미지와 분석 결과의 식별자가 어떻게 연결되는지 알 수 있습니다.

분석이 필요한 레이어는 압축을 푼 tar 스트림으로 읽습니다. 파일을 순회하면서 분석기에 파일 경로와 내용을 여는 함수를 넘기고, 후처리에 필요한 파일은 별도 파일시스템에 준비합니다. 이 과정이 Fanal 쪽 책임입니다. **컨테이너를 실행해서 프로그램의 행동을 관찰하는 경로가 아닙니다.** [레이어 파일 순회](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/pkg/fanal/artifact/image/image.go#L436-L490)에 실제 호출이 있습니다.

레이어가 여러 개라고 패키지 목록을 무조건 이어 붙일 수도 없습니다. 윗 레이어가 아랫 레이어의 파일을 지우거나 대체할 수 있기 때문입니다. 적용기는 opaque 디렉터리와 whiteout, 즉 이미지 레이어의 삭제 표시를 먼저 반영하고, 패키지·애플리케이션 등의 분석 정보를 경로별로 덮어씁니다. [레이어 병합](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/pkg/fanal/applier/docker.go#L112-L150)에서 이를 확인할 수 있습니다. 비밀정보는 별도 병합 경로를 가지므로, 모든 검사 결과에 동일한 삭제 의미가 적용된다고 확장하지는 않습니다.

이렇게 구성한 상태에는 OS, 패키지, 언어별 애플리케이션, 설정 오류, 비밀정보 등의 정보가 들어갑니다. 로컬 backend는 이 정보를 검사 대상 구조로 바꾸고 선택된 스캐너에 넘깁니다. OS를 알 수 없거나 패키지 DB 파일이 감지되지 않은 경우의 처리도 별도입니다. 특히 설치 패키지 정보 파일을 지웠다면 패키지를 찾지 못할 수 있다는 경고가 코드에 있습니다. [분석 정보 적용과 경고](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/pkg/scan/local/service.go#L61-L143)는 “파일을 읽었다”와 “검사할 패키지를 충분히 알아냈다”를 구분하는 지점입니다.

## 작동 원리 3: 패키지 이름만으로 CVE를 붙이지 않습니다

로컬 검사는 스캐너 옵션에 따라 OS 패키지와 언어 패키지 경로를 나눕니다. OS 패키지 검사는 OS를 식별하지 못하면 빈 결과를 반환하고, 취약점 스캐너 없이 SBOM용 패키지 정보만 필요하면 패키지 목록만 돌려줍니다. 취약점 검사가 켜져 있을 때 배포판에 맞는 detector를 만들어 실제 검출을 진행합니다. [OS 검사 조건](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/pkg/scan/ospkg/scan.go#L29-L75), [OS·언어 경로 분기](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/pkg/scan/local/service.go#L194-L231)를 확인할 수 있습니다.

배포판별 detector를 고르는 과정에도 순서가 있습니다. 등록된 supplier가 패키지 정보 등으로 전용 driver를 제공하는지 먼저 보고, 없으면 OS family에 대응하는 기본 driver를 고릅니다. 지원하지 않는 OS이면 지원하지 않는다는 오류를 반환합니다. 상위 로컬 서비스는 이 경우 OS 패키지 취약점 결과를 추가하지 않는 경로를 갖습니다. [driver 선택](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/pkg/detector/ospkg/detect.go#L155-L170), [지원하지 않는 OS 처리](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/pkg/scan/local/service.go#L207-L221)가 연결됩니다.

여기서는 **Alpine detector 하나**를 자세히 봅니다. 이것이 Debian이나 RPM 패키지의 버전 비교까지 대표한다는 뜻은 아닙니다. Alpine 구현은 다음 순서를 따릅니다.

1. OS 버전을 비교에 쓸 release로 정리합니다. 감지된 패키지 저장소 release가 따로 있으면 이를 우선할 수 있습니다.
2. 설치 패키지의 source package 이름을 사용하고, 없으면 패키지 이름을 사용해 보안 권고를 조회합니다.
3. 설치된 source version을 Alpine용 버전 파서로 해석합니다.
4. 보안 권고의 영향 시작 버전과 수정 버전을 비교해 해당하는 항목을 `DetectedVulnerability`로 만듭니다.
5. 결과에는 CVE 등 취약점 ID, 설치 버전, 수정 버전, 패키지 식별자, 레이어와 정보 출처를 담습니다.

[Alpine 조회·비교 코드](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/pkg/detector/ospkg/alpine/alpine.go#L77-L159)에 이 흐름이 나옵니다. 수정 버전이 있는 권고에서는 설치 버전이 그보다 낮은지를 비교합니다. 버전 파싱에 실패하면 해당 비교를 건너뛰는 분기도 있으므로, 입력을 항상 해석할 수 있다고 가정하지 않습니다.

이때 패키지의 **설치 경로와 배포 주체**가 중요합니다. 문서는 OS 패키지 관리자로 설치한 패키지에는 해당 OS vendor의 보안 권고를 사용한다고 설명합니다. 배포판이 보안 패치를 이전 버전에 backport하면 upstream의 최신 버전 번호와 다르더라도 수정돼 있을 수 있기 때문입니다. 같은 이름이더라도 `yum`으로 설치한 Python 패키지와 `pip`으로 설치한 라이브러리는 같은 데이터 소스로 판정하지 않을 수 있습니다. 이는 [원문 문서의 데이터 소스 선택 설명](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/docs/guide/scanner/vulnerability.md#L46-L58)에 근거하며, 이 리뷰에서 모든 언어 detector를 재검증한 것은 아닙니다.

아래는 지금까지의 대표 경로를 다시 쓴 설명용 의사코드입니다. 실제 Go 소스의 복사본이나 이 리뷰에서 얻은 실행 결과는 아닙니다.

```text
입력: 이미지 참조, 검사 옵션, 보안 데이터베이스
이미지를 읽고 분석되지 않은 레이어의 구성 요소를 추출
레이어의 삭제·대체를 적용해 OS와 패키지 상태를 구성
OS 패키지 취약점 검사가 선택돼 있으면:
    OS와 패키지에 맞는 detector 선택
    패키지별 보안 권고 조회
    해당 생태계의 버전 규칙으로 영향 여부 판정
    발견 결과에 패키지·버전·출처 정보 저장
선택한 다른 스캐너의 결과와 함께 보고서 구성
출력: 필터 적용 전의 구조화된 검사 결과
```

절차의 근거는 [분석·검사 경계](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/pkg/scan/service.go#L47-L65), [로컬 검사 조정](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/pkg/scan/local/service.go#L145-L192), [Alpine detector](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/pkg/detector/ospkg/alpine/alpine.go#L77-L159)입니다.

## 작동 원리 4: 필터가 바꾼 결과를 보고하고 종료합니다

검출된 목록이 바로 최종 화면에 나오는 것은 아닙니다. artifact runner는 **검사 → 필터 → 보고서 쓰기** 순서로 처리합니다. 필터는 심각도와 상태, ignore 파일 등의 조건을 적용하고 중복 취약점을 정리합니다. 설정된 Rego 정책과 VEX 문서도 결과에 영향을 줄 수 있습니다. VEX는 특정 제품의 특정 취약점이 실제로 영향을 주는지에 관한 정보를 전달하는 문서 형식입니다. [결과 처리 순서](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/pkg/commands/artifact/run.go#L447-L467), [필터 구성](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/pkg/result/filter.go#L39-L128)을 함께 보면 설정이 어디서 판정 목록을 바꾸는지 알 수 있습니다.

예를 들어 `--severity HIGH,CRITICAL`을 쓰면 이 심각도 범위에 남은 결과를 보게 됩니다. 낮은 심각도의 문제가 아예 검출되지 않았다는 뜻은 아닙니다. 또 ignore 파일과 일치한 취약점은 활성 결과 목록에서 빠지고 `ModifiedFindings`에 제외된 이유 등의 정보를 남기는 경로가 있습니다. 화면과 원시 검출을 같은 목록이라고 생각하면 이 차이가 보이지 않습니다.

보고 단계에서는 선택한 형식에 맞는 writer를 만듭니다. 이 커밋은 table, JSON, CycloneDX, SPDX, SARIF 등의 분기를 가집니다. writer는 출력 파일이나 표준출력에 데이터를 기록하며, 이 과정이 실패하면 오류를 반환합니다. [보고서 쓰기](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/pkg/report/writer.go#L29-L64), [형식별 분기](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/pkg/report/writer.go#L67-L127)에 근거합니다. 같은 내부 보고서를 바탕으로 해도 화면용 표와 소프트웨어 구성 명세의 목적은 다릅니다.

![필터 후 발견 결과와 보고서 쓰기가 종료 코드 판단보다 먼저 오는 흐름]({{ '/img/reviews/2026/trivy-review/finding-and-exit.svg' | relative_url }})

발견 여부와 프로세스 종료 코드는 별도 조건입니다. 리뷰어 작성, 분석 커밋 기준. 출처: [보고 후 종료 판단](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/pkg/commands/artifact/run.go#L404-L419), [종료 조건](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/pkg/commands/operation/operation.go#L122-L133).
{: .caption}

마지막에 `Results.Failed()`가 결과에 문제 항목이 남았는지 확인합니다. 취약점뿐 아니라 실패한 설정 검사, 비밀정보, 라이선스·crypto 발견도 이 함수의 판단 대상입니다. `operation.Exit`는 설정된 `ExitCode`가 0이 아니고 문제가 남아 있을 때 그 종료 코드를 반환합니다. OS 지원 종료에 대한 `ExitOnEOL` 조건은 별도로 먼저 확인합니다. [발견 여부의 정의](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/pkg/types/report.go#L198-L222), [종료 코드 처리](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/pkg/commands/operation/operation.go#L122-L133)를 구분해야 합니다.

따라서 **취약점이 표시됐다고 명령이 반드시 실패하는 것은 아닙니다.** `--exit-code`는 이 커밋에서 명시적 기본값 없이 정수 플래그로 정의돼 기본값 0을 사용합니다. 반대로 실패 코드가 나왔다고 항상 취약점 때문인 것도 아닙니다. DB 준비나 이미지 분석, 보고서 출력 중의 오류도 실패 경로입니다. [플래그 정의](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/pkg/flag/report_flags.go#L78-L83)와 최상위 오류 처리를 같이 읽어야 합니다.

| 확인한 상태 | 그 상태가 뜻하는 것 | 곧바로 단정할 수 없는 것 |
| --- | --- | --- |
| 패키지 목록을 얻음 | 이미지에서 구성 요소 정보를 식별함 | 모든 패키지의 보안 판정이 완료됨 |
| 취약점 결과가 있음 | 선택한 데이터·규칙으로 일치한 알려진 문제가 있음 | 실제 공격 성공이나 특정 코드 경로의 악용 가능성 |
| 필터 후 결과가 비어 있음 | 설정 조건을 통과해 남은 발견이 없음 | 검사 범위 밖까지 포함한 완전한 안전성 |
| 종료 코드 0 | 현재 실행·종료 조건에서 성공으로 끝남 | 발견된 보안 문제가 전혀 없음 |

## 설치와 사용: 문서의 명령과 분석한 경로를 맞춥니다

README는 Homebrew, Docker 이미지, 릴리스 바이너리 등 여러 배포 경로를 안내합니다. 아래는 해당 커밋 README에 실린 명령입니다. 이 리뷰에서 실행해 얻은 예제가 아니며, 오래된 이미지 태그는 원문의 사용법 예시로 읽어야 합니다. [설치·기본 사용법](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/README.md#L37-L96)을 출처로 둡니다.

```bash
trivy image python:3.4-alpine
```

이 명령의 형태는 `trivy <target> [--scanners ...] <subject>`입니다. 여기서 `image`가 대상 종류, 마지막 값이 이미지 참조입니다. 코드의 image 분기에서 서버 주소와 tar 입력을 주지 않은 경우가 이 글의 대표 경로와 대응합니다.

README에는 검사 종류를 명시한 파일시스템 예제도 있습니다.

```bash
trivy fs --scanners vuln,secret,misconfig myproject/
```

이것은 세 종류의 검사를 요청하는 예입니다. 파일시스템과 이미지의 분석기 구성이 같다는 뜻은 아닙니다. 실제로 `ScanImage`는 lockfile 분석을 끄고, `ScanFilesystem`은 개별 패키지와 SBOM 파일 분석을 끄는 등 입력별로 다른 선택을 합니다. [대상별 분석기 조정](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/pkg/commands/artifact/run.go#L199-L228)을 보면 입력 종류를 명시하는 이유가 드러납니다.

운영에서 확인할 것은 명령 이름만이 아닙니다. 검사할 패키지 종류와 스캐너, 심각도·예외 조건, 사용할 출력 형식, 문제가 있을 때의 종료 코드를 함께 정해야 결과를 해석할 수 있습니다. 이 글은 실제 시스템의 CI 설정을 변경하거나 검사를 활성화한 기록은 아닙니다.

## 한계와 주의점: 검사 범위와 데이터 시점을 남겨야 합니다

취약점 검사는 **알려진 문제**를 대상으로 합니다. 문서도 검사 대상에서 찾은 소프트웨어 구성 요소의 알려진 취약점을 검출한다고 정의합니다. 여기서 새로 발견되지 않은 취약점이나 서비스의 업무 로직까지 검사했다고 확대할 수는 없습니다. 또 공식 OS vendor가 아닌 제삼자 저장소 패키지는 보안 권고의 범위가 달라 제외되거나, 휴리스틱 식별의 한계로 오탐·미탐이 발생할 수 있다고 설명합니다. [검사 정의와 제삼자 패키지 범위](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/docs/guide/scanner/vulnerability.md#L1-L125)를 확인할 부분입니다.

소스 커밋을 고정하는 것과 검사 결과를 완전히 고정하는 것도 다릅니다. 엔진 외에 취약점 DB, Java artifact 식별용 DB, 설정 검사 bundle 등이 별도로 사용됩니다. 같은 이미지라도 사용한 보안 데이터의 시점이나 정책이 달라지면 결과를 똑같이 해석할 수 없습니다. [데이터베이스 문서](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/docs/guide/configuration/db.md#L1-L16)는 엔진 설치물과 보안 정보의 차이를 명시합니다.

`--offline-scan`도 네트워크 전체를 끄는 포괄 스위치로 읽으면 안 됩니다. 플래그 설명은 의존성을 식별하는 API 요청을 하지 않는다는 뜻이며, 네트워크 문서는 DB·VEX·업데이트 확인 등을 별도 연결로 설명합니다. 격리 환경에는 필요한 데이터를 미리 준비하는 절차가 따로 있습니다. [플래그 의미](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/pkg/flag/scan_flags.go#L35-L40), [외부 연결 안내](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/docs/guide/advanced/air-gap.md#L1-L91)에 근거합니다.

저장소는 [Apache License 2.0](https://github.com/aquasecurity/trivy/blob/c14584a6c49d9cf4cf62d54281437bf2d97864d6/LICENSE#L1-L9)으로 공개돼 있습니다. 코드 재사용에는 해당 라이선스의 저작권·고지와 변경 표시 등 조건을 확인해야 합니다. 이 글의 도식과 의사코드는 코드의 흐름을 설명하려고 새로 작성한 자료이며, 원본 구현의 대체물이나 실행 결과가 아닙니다.

## 마무리: 목록을 만드는 과정까지 읽어야 합니다

Trivy의 컨테이너 이미지 검사는 입력에서 패키지를 식별하고, 레이어 상태를 반영하며, 생태계별 보안 권고와 버전을 비교한 뒤 결과를 필터링하고 출력합니다. 하나의 CVE 행 뒤에 입력 분석, 보안 데이터, 버전 규칙, 사용자의 예외 정책이 차례로 있습니다.

그래서 결과를 읽을 때는 “몇 개 나왔는가”만으로 충분하지 않습니다. 어떤 대상을 어떤 스캐너로 읽었는지, 패키지를 제대로 식별했는지, 어느 데이터와 조건으로 결과를 남겼는지, 종료 코드를 어떻게 정했는지까지 함께 봐야 합니다.

이 글에서는 이미지 standalone 경로와 Alpine OS 패키지 detector를 중심으로 확인했습니다. 언어별 detector 전체, IaC 규칙·비밀정보 정규식의 개별 판정, Kubernetes·VM·원격 서버 구현, WASM 확장과 외부 DB 수집 파이프라인은 상세 분석하지 않았습니다. 외부 패키지 내부 구현과 실제 탐지 성능 역시 확인 범위 밖입니다.
