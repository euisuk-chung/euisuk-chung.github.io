---
type: "Repo Review"
title: "[Repo Review] rea-video — 영상의 제작 흔적을 근거와 재제작 계획으로 바꾸는 구조"
description: "영상의 샷·픽셀·음향·시각 검토를 결합하는 rea-video의 처리 흐름과 재제작 경로를 추적하고 평가 수치의 분모·캐시·독립성 조건을 분석합니다."
date: "2026-11-09"
tags:
  - "Repo Review"
  - "AI Agent"
  - "Computer Vision"
  - "딥러닝"
  - "머신러닝"
  - "Tools"
resource: "https://github.com/JuneYaooo/rea-video/tree/3522250b4d3e667610a175c0f188ac3d725b41cd"
generated:
  by: "process:blog-review"
  at: "2026-11-09T06:58:56+09:00"
sources:
  - id: "github:JuneYaooo/rea-video@3522250b4d3e667610a175c0f188ac3d725b41cd"
    resource: "https://github.com/JuneYaooo/rea-video/tree/3522250b4d3e667610a175c0f188ac3d725b41cd"
    title: "rea-video"
    author: "JuneYaooo"
    last_modified: "2026-11-08"
status: "stable"
year: "2026"
analyzed_at: "2026-11-09T06:58:56+09:00"
source_id: "JuneYaooo/rea-video"
source_revision: "3522250b4d3e667610a175c0f188ac3d725b41cd"
source_type: "repo"
source_url: "https://github.com/JuneYaooo/rea-video/tree/3522250b4d3e667610a175c0f188ac3d725b41cd"
visual_sources:
  - path: "/img/reviews/2026/rea-video-repo-review/architecture.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/pipeline.py#L64-L290"
    caption: "리뷰어 작성, 분석 커밋 기준: 로컬 측정·외부 VLM·중간 표현·계획과 보고서의 흐름."
  - path: "/img/reviews/2026/rea-video-repo-review/fusion.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/pipeline.py#L373-L552"
    caption: "리뷰어 작성, 분석 커밋 기준: 시각 의견의 gate·그룹 융합과 사용자 정정의 경계를 구분한 도식."
---

## 들어가며

영상 하나를 따라 만들고 싶을 때 먼저 필요한 것은 생성 프롬프트가 아닐 수 있습니다. 실제로 촬영한 장면, 화면 녹화, 코드로 만든 글자 애니메이션, AI가 생성한 영상이 한 타임라인에 섞여 있기 때문입니다. 모두 영상 생성 모델에 넣는다면 원래 화면이 어떻게 구성됐는지를 놓치기 쉽습니다.

**rea-video는 영상을 샷 단위로 나누어 제작 방식을 추정하고, 근거와 재제작 경로를 함께 정리하는 Python CLI와 에이전트 스킬**입니다. 이 글에서는 `JuneYaooo/rea-video`의 커밋 **`3522250b4d3e667610a175c0f188ac3d725b41cd`**를 고정해 진입점부터 분석·판정·검토·계획·출력까지 읽습니다. 패키지 버전은 0.1.0이며, 대상 코드의 설치·실행·테스트나 영상 분석을 독립 재현하지 않은 정적 코드 리뷰입니다. [패키지 명세](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/pyproject.toml#L5-L28), [분해 진입점](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/cli.py#L48-L69)

특히 README의 98–100%라는 수치를 범용 AI 영상 탐지 성능으로 읽지 않겠습니다. 저장소는 어떤 데이터에서 규칙을 고쳤는지, 캐시 재분류와 새 디코딩이 어디서 달랐는지, 도구·VLM·에이전트 검토가 어떤 경우에 실패했는지도 기록합니다. 구현의 흥미로운 부분은 이 여러 증거를 한 결과로 합치는 방식과, 그 결과를 다시 고칠 수 있는 구조입니다. [평가 개요](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/eval/RESULTS.md#L1-L29), [규칙 선택과 독립성 고지](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/eval/RESULTS.md#L139-L157)

## rea-video는 무엇인가요?

프로젝트가 답하려는 질문은 “이 영상이 AI인가요?”보다 넓습니다. **각 샷의 바탕 화면이 어떻게 만들어졌고, 그 위에 무엇이 얹혔으며, 같은 구조를 만들려면 무엇을 준비해야 하나요?**를 나누어 다룹니다.

| 분석 대상 | 구현이 모으는 정보 | 주요 결과 |
| --- | --- | --- |
| 바탕 화면 | 시간 변화·질감·컨테이너 정보·선택적 시각 모델 판단 | 실사·AI 영상·3D·코드·녹화·정지 이미지 등의 제작 방식 |
| 편집 포장 | 글자 위치와 시간, 자막 스타일, 스티커 후보, 화면 이벤트 | SRT·ASS, 포장 타임라인, 확인할 후보 |
| 촬영·음향 | 피사체·구도·움직임·빛의 측정값, 음성·음악·효과음 단서 | 촬영·조명 설명, 오디오 타임라인·분리 파일 |
| 재제작 | 판정한 종류, 원본 시간, 모델 능력표·라우팅 규칙 | 촬영 계획·생성 단위·코드 제작 명세·필요한 소재 |

현재 코드의 `LABELS`는 **11개**입니다. 실사, AI 영상, 아바타, 3D, 코드 렌더링, 화면 녹화·스크린샷, 정지 이미지의 이동, 정지 유지에 2D 애니메이션·스톱모션·기존 영화나 TV 영상이 더해집니다. 다만 `anim_2d`, `stop_motion`, `film_footage`는 **도구만으로 측정할 수 없는 종류**인 `UNMEASURED`로 분리합니다. README와 과거 평가에 등장하는 “8종류”를 현재 11종류 전체의 검증 결과로 확대할 수 없습니다. [분류와 미측정 범위](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/classify.py#L1-L35), [스킬의 질문 구조](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/skills/rea-video/SKILL.md#L8-L17)

또한 **바탕 화면의 제작 방식, 그 위에 붙은 소재, 재제작용 참고자료는 서로 다른 정보**입니다. 코드 레이아웃 안에 실제 화면 녹화가 들어갈 수 있습니다. 반대로 AI가 그린 제품이 보인다고 그 제품의 실사 픽셀이 영상에 합성됐다고 단정하지 않습니다. 코어는 `base`, `layers`, `material`, `references`를 분리해 이 차이를 표현합니다. [소재와 참고자료 처리](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/pipeline.py#L601-L635), [소재 구분](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/skills/rea-video/SKILL.md#L10-L15)

## 아키텍처와 디렉터리 구조

설계의 중심은 **증거를 보관하는 중간 표현 `breakdown.json`**입니다. 매번 영상을 처음부터 분석하는 대신, 저장된 특징과 시각 판정으로 결론·계획·보고서를 다시 만들 수 있습니다.

![영상의 로컬 측정과 선택적 외부 시각 모델이 중간 표현으로 모이고 재분류·계획·보고서로 이어지는 구조]({{ '/img/reviews/2026/rea-video-repo-review/architecture.svg' | relative_url }})

*리뷰어 작성, 분석 커밋 기준. 로컬 측정과 외부 VLM 호출을 구분한 개요입니다. 시각 검토·사용자 정정은 저장된 중간 표현에 추가되고, 결과를 다시 계산합니다. [분해](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/pipeline.py#L64-L290), [재분류](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/pipeline.py#L484-L549), [계획·출력](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/pipeline.py#L788-L797)*

| 위치 | 책임 |
| --- | --- |
| `rea_video/cli.py` | 옵션·환경·사용자 기본값을 읽고 하위 명령으로 연결합니다. |
| `media.py`, `shots.py`, `probe.py` | ffmpeg·ffprobe 입출력, 샷 경계·시간, 컨테이너 출처 단서를 처리합니다. |
| `features.py`, `overlay.py`, `packaging.py`, `aspects/` | 화면 통계·OCR·편집 포장·촬영 특성을 수집합니다. |
| `audio.py`, `stems.py`, `sound_source.py` | 음향 특징, 보컬·반주 분리, 출처 추정 단서를 다룹니다. |
| `classify.py`, `vlm.py`, `review.py`, `pipeline.py` | 규칙·시각 모델·검토 답변을 합쳐 결론과 불확실성을 만듭니다. |
| `plan.py`, `production.py`, `capabilities/` | 종류별 제작 경로와 모델 능력에 맞는 재제작 단위를 구성합니다. |
| `report.py`, `visual.py` | Markdown·HTML 보고서, 샷 시트·스토리보드·오디오 그림을 만듭니다. |
| `remake.py`, `integrations/` | 선택적으로 외부 생성 도구를 연결하고 조각을 로컬 합성합니다. |
| `skills/rea-video/`, `eval/`, `tests/` | 에이전트 작업 지침, 평가 정의·개발 기록, 테스트 코드를 제공합니다. |

`pyproject.toml`은 Python 3.10 이상과 NumPy, OpenCV headless, Pillow, PyYAML, ONNX Runtime을 선언합니다. OCR은 추가 의존성이며, ffmpeg·ffprobe는 별도 실행 도구입니다. 이 프로젝트 전체를 “학습 모델이 전혀 없는 규칙 프로그램”이라고 부르는 것은 정확하지 않습니다. 제작 방식의 기본 점수는 규칙이지만, 음원 분리에 로컬 ONNX 모델을 사용하고 OCR·얼굴 검출·선택적 VLM도 함께 쓰기 때문입니다. [의존성](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/pyproject.toml#L5-L28), [주요 모듈 연결](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/pipeline.py#L12-L28), [분리 모델](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/stems.py#L1-L5)

스킬과 CLI의 역할도 다릅니다. CLI가 측정과 파일 생성을 수행한다면, 스킬은 에이전트에게 **어떤 결과를 읽고, 어느 샷을 눈으로 확인하고, 수정 답변을 어떻게 반영할지** 알려 줍니다. 스킬 파일이 있다는 이유로 Python CLI가 스스로 모든 애매한 샷을 이해하고 수정하는 것은 아닙니다. 이 리뷰에서는 해당 지침을 프로젝트의 설계 자료로 읽었으며 실행 지시로 따르지 않았습니다. [표준 흐름과 시각 검토](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/skills/rea-video/SKILL.md#L29-L54), [답변 저장](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/review.py#L237-L280)

## 작동 원리

### 1. 샷 경계와 실제 시간을 먼저 정합니다

`decompose()`는 필요한 미디어 도구를 확인하고 파일 정보를 읽은 뒤 `provenance()`와 `build_track()`을 호출합니다. 프레임 트랙에는 이전 프레임과의 색상 히스토그램 거리, 회색조 픽셀 차이, 변화 영역 비율, 밝기와 작은 썸네일이 들어갑니다. 이 단서로 하드 컷뿐 아니라 점프 컷·디졸브·플래시·정지 구간 등을 구분하는 규칙을 적용합니다. [입력·샷 분석](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/pipeline.py#L64-L82), [프레임 트랙](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/shots.py#L22-L108), [경계 검출](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/shots.py#L111-L246)

시간을 단순히 프레임 번호를 평균 fps로 나누어 계산하지 않는 점도 중요합니다. `Shot.t()`는 가변 프레임률에서 실제 프레젠테이션 타임스탬프를 사용하고, 마지막 프레임을 넘으면 중앙 프레임 간격으로 보완합니다. 스마트폰이나 화면 녹화처럼 프레임 간격이 고르지 않은 입력의 경계 시간을 다루기 위한 구현입니다. 그렇다고 모든 실제 영상의 컷을 완벽하게 찾아낸다는 증거는 아니며, 뒤의 평가 범위를 함께 봐야 합니다. [샷 시간 계산](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/shots.py#L38-L76)

이후 각 샷의 여러 프레임과 연속 프레임 쌍을 수집합니다. 대표 이미지 일부만 뽑아 VLM에 질문하는 것과 달리, `collect_samples()`는 전환 바로 옆 프레임을 피하면서 중복 프레임·정지 픽셀·노이즈와 움직임을 측정합니다. 공간 특징에 쓰는 프레임과 전역 움직임을 구하는 프레임 쌍의 샘플 수도 따로 둡니다. [샘플 수집](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/features.py#L187-L218)

### 2. 자막·스티커는 바탕 화면과 분리합니다

`packaging`은 샷마다 따로 붙이는 주석이 아니라 **영상 전체의 편집 타임라인**입니다. OCR로 얻은 글자를 위치·문자열 유사도에 따라 연결하고, 조밀하게 읽은 회색조 프레임으로 나타남·사라짐의 시점을 보완합니다. 글자 색·테두리·배경·크기와 등장 방식을 분석해 자막, 제목, 강조 글자, 화면 안 물체에 인쇄된 글자 등을 구분합니다. 결과에는 SRT와 스타일을 담는 ASS가 포함됩니다. [OCR 샘플링](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/packaging.py#L306-L346), [문구 연결](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/packaging.py#L424-L518), [시간 보정](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/packaging.py#L663-L791), [자막 출력](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/packaging.py#L1433-L1493)

이 분리는 분류에도 영향을 줍니다. 붙여 넣은 스티커의 평탄한 픽셀을 영상 자체의 질감으로 오인하지 않도록 `clean_region()`이 측정할 영역을 바꿉니다. 현재 구현은 **샷 중간에 붙거나 반복 재생된다는 샷 내부 근거**가 있는 스티커를 대상으로 하며, 그 샷의 상당 부분을 덮는지 확인하고 남은 가장 큰 띠 영역이 충분히 커야 크롭합니다. 컷 양쪽에서 같은 그림이 보였다는 사실만으로 바탕 화면을 잘라 내지는 않습니다. [측정 영역 연결](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/pipeline.py#L118-L145), [크롭 조건](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/packaging.py#L1595-L1616)

왜 이렇게 구체적인 조건이 필요할까요? 개발 기록은 연속 삽화의 같은 캐릭터나 카드 제목을 스티커로 잘못 인식해 분류에 필요한 증거까지 지운 사례를 설명합니다. 따라서 포장 분석은 보고서의 부가 정보에 그치지 않고, 이후 특징 추출의 입력을 바꾸는 구성 요소입니다. 이 수정은 캐시를 재분류하는 검사만으로는 확인할 수 없습니다. [새 디코딩에서 드러난 회귀](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/eval/RESULTS.md#L325-L343)

### 3. 제작 방식은 여러 휴리스틱을 점수로 결합합니다

`deterministic()`은 다음과 같은 질문을 순서대로 던집니다.

- 화면이 거의 멈춰 있나요, 한 장의 이미지 전체가 같이 확대·이동하나요, 내부 물체가 따로 움직이나요?
- 넓은 평탄 색상과 적은 색 수, 수직·수평 경계가 코드·UI 화면을 시사하나요?
- 어두운 실사, 큰 얼굴, 글자가 많은 화면 때문에 질감 지표를 보정해야 하나요?
- 24→30 같은 중복 프레임 규칙, 카메라 정보나 AIGC 태그가 남아 있나요?
- 플랫폼 재인코딩 때문에 센서 노이즈나 선명도 주기를 신뢰하기 어려운가요?

[시간적 종류](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/classify.py#L181-L215), [질감](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/classify.py#L217-L327), [프레임률·출처 단서](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/classify.py#L329-L414)

가령 규칙은 24fps에서 30fps로 변환할 때 생길 수 있는 반복 프레임 주기를 측정합니다. 그러나 코드의 근거 문구 자체도 이것이 **AI 영상·3D·애니메이션·영화 소재에서 모두 생길 수 있음**을 설명합니다. “24fps 흔적 발견→특정 생성기로 제작”이라는 인과 증명이 아닙니다. 실사도 24p로 촬영할 수 있고, 재인코딩이 노이즈를 없애며, 카메라 역시 C2PA 정보를 남길 수 있습니다. [프레임률 단서의 범위](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/classify.py#L329-L367), [C2PA 조건](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/probe.py#L168-L174)

컨테이너에서 생성기처럼 보이는 문자열을 발견했을 때도 강도를 나눕니다. 구조화된 메타데이터와 달리 바이트 안의 짧은 이름은 우연히 나타날 수 있어 `generator_weak`로 보관하고 직접 점수에 넣지 않습니다. 이런 구현은 출처 단서와 판정을 분리하려는 장치입니다. 태그의 존재를 확인하는 일과 원 제작 과정 전체를 증명하는 일은 여전히 다릅니다. [출처 정보의 강약](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/probe.py#L133-L174)

마지막에는 종류별 수동 점수를 더하고 정규화합니다. 따라서 출력 필드 이름이 `probs`라고 해서 통계적으로 보정된 정답 확률이 되는 것은 아닙니다. 학습된 범용 탐지기에서 얻은 확률과도 다릅니다. 이 리뷰에서 퍼센트는 **규칙·융합 과정의 신뢰 점수**로 읽으며, 반복 표본에서 측정된 성공 확률로 해석하지 않습니다. [정규화](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/classify.py#L85-L87), [점수 구성](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/classify.py#L421-L476)

### 4. VLM은 전체 재판정을 맡기보다 추가 증거를 제공합니다

VLM은 영상·이미지를 이해하는 시각 언어 모델입니다. 기본 분해는 VLM 없이도 진행되지만, `--vlm`을 켜면 `REA_VLM_*` 등의 환경 설정으로 외부 API 클라이언트를 구성합니다. 짧은 영상 클립과 첫·중간·끝 그림을 전달하며, 기본 모드에서는 영상과 이미지 양쪽을 사용합니다. [설정 우선순위](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/vlm.py#L29-L53), [샷별 요청](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/pipeline.py#L194-L245)

호출 단위도 원본 샷 수와 같지 않을 수 있습니다. 인접한 점프 컷들은 하나의 take로 묶되 최대 12초·8개 조각으로 제한합니다. 호출 상한을 넘으면 단순히 앞부분만 보는 대신 **길이와 도구의 불확실성**을 조합한 우선순위를 사용합니다. 별도의 전체 영상 패스는 480p 클립을 보내 문맥·오디오·포장을 읽습니다. 이 전체 패스는 샷별 호출 상한과 구별해야 합니다. [호출 단위와 우선순위](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/pipeline.py#L38-L61), [전체 패스·상태](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/pipeline.py#L247-L265)

응답은 JSON으로 정리하고 `vlm_cache/`에 보관합니다. 캐시 키에는 프롬프트, 엔드포인트, 모델 목록, 출력 길이와 미디어 바이트가 들어가며 API 키 자체는 넣지 않습니다. 모델별 재시도·대체 모델, 영상 요청 실패 시 이미지 전용 재시도도 있습니다. 설정이 없거나 모든 호출이 실패해도 도구 결과를 유지하고 `not_configured`, `failed`, `partial` 등 실제 상태를 저장합니다. **`--vlm`을 주었다는 사실과 VLM이 결과에 실제로 기여했다는 사실은 다릅니다.** [클라이언트·캐시](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/vlm.py#L117-L193), [실패·부분 성공](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/pipeline.py#L198-L265)

### 5. 시각 검토는 추가 모델 의견이며, 사용자 정정은 별도입니다

에이전트가 스스로 이미지를 볼 수 있으면 `review`로 샷별 작업과 답안 템플릿을 만듭니다. 이미지, 도구 판단과 우선순위 등을 보고 `label_probs`, 근거, 장면 설명, 참고자료와 제작 프롬프트를 채우는 방식입니다. 빈 분포는 보지 않은 샷으로 건너뜁니다. `split_suggestion`은 재분할 제안으로 보고서에 남기며, 그 자체로 기존 샷 경계를 다시 나누지는 않습니다. [검토 계약](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/skills/rea-video/SKILL.md#L42-L54), [답안 정리](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/review.py#L184-L234), [적용](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/review.py#L237-L280)

![도구·VLM·에이전트 검토의 분포가 조건부로 융합되고 사용자 정정은 별도로 적용되는 흐름]({{ '/img/reviews/2026/rea-video-repo-review/fusion.svg' | relative_url }})

*리뷰어 작성, 분석 커밋 기준. 단일 시각 출처에는 gate가 적용되고, 두 시각 출처가 있으면 의견을 결합합니다. 명시적 사용자 정정은 마지막에 별도로 반영합니다. [시각 의견·gate·majority](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/pipeline.py#L373-L454), [판정·정정](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/pipeline.py#L523-L552)*

에이전트 답변은 그대로 덮어쓰지 않습니다. 먼저 `AGENT_WEIGHT=0.85`를 사용해 균등 분포와 섞어 부드럽게 만들고, VLM과 검토가 모두 있으면 시각 분포를 평균합니다. 한 시각 출처만 있는 경우에는 도구의 상위 후보, AI·실사 축의 높은 점수, 재인코딩과 프레임률 등의 조건을 `gate`로 검사하여 그 의견을 채택하거나 제외합니다. 미측정 종류와 인물이 있는 화면 등에는 별도 예외가 있습니다. [답변 가중치](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/review.py#L15-L17), [분포 완화](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/review.py#L202-L234), [시각 의견과 gate](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/pipeline.py#L373-L430)

실제 융합은 단순한 3자 다수결과도 다릅니다. `classify.fuse()`는 AI 영상·아바타를 generated, 3D·코드·2D 애니메이션을 rendered, 실사·스톱모션·영화 소재를 live-action 계열로 먼저 묶습니다. 같은 큰 부류의 세부 종류가 표를 나눠 가져 제3의 부류에 밀리지 않게 하려는 구조입니다. 각 분포를 로그 공간에서 결합하고, 정지·평면 이동 같은 시간적 제약을 적용하며, 도구와 한 시각 출처가 같은 그룹을 지지하는 경우의 `majority` 보정도 둡니다. 두 시각 출처가 서로 동의해도 도구를 항상 이기는 규칙은 아닙니다. [그룹 융합](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/classify.py#L487-L564), [majority의 방향](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/pipeline.py#L433-L454)

시각 의견을 채택한 최종 결정은 먼저 그룹의 합을 비교한 뒤 그 안에서 세부 종류를 고릅니다. 이때 `confidence`도 세부 종류 하나의 값이 아니라 **선택한 그룹의 점수**입니다. 시각 의견이 없는 도구 전용 경로는 상위 종류를 직접 고릅니다. 이 차이는 동일한 퍼센트를 단순 비교하기 전에 알아야 할 출력 계약입니다. [그룹 우선 결정](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/classify.py#L572-L581), [경로별 결정](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/pipeline.py#L523-L530)

확실한 사용자 정정은 다른 경로입니다. `correct`로 저장된 `user.label`은 최종 종류와 점수를 직접 바꿉니다. 단순 검토 의견과 사용자 정정의 의미를 같은 것으로 취급하지 않습니다. 또한 `memory.py`는 같은 영상의 정정을 재적용하고 자주 틀린 종류를 검토 힌트로 보여 주지만, 분류기 가중치를 조용히 학습하는 시스템은 아닙니다. [명시 정정 우선](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/pipeline.py#L543-L548), [기억의 역할](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/memory.py#L1-L10)

### 6. 오디오·촬영 특성도 같은 중간 표현에 붙습니다

음향 경로는 음성·음악·효과음의 존재, 박자·조성·전환 시각을 모읍니다. 기본 옵션의 stem 분리는 UVR MDX-Net `Inst HQ 3` ONNX 모델을 CPU로 실행해 반주를 추정하고, 원본에서 이를 빼 보컬을 구합니다. 저장되는 `music.wav`에는 음악만 깨끗하게 남는다고 보장할 수 없으며 효과음·환경음도 포함될 수 있습니다. [분리 대상](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/stems.py#L1-L5), [분리·파일 출력](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/stems.py#L107-L143)

이 모델은 약 67MB이며 기본 캐시 디렉터리에 처음 내려받을 수 있습니다. 다운로드는 SHA-256을 확인한 임시 파일을 원자적으로 교체하는 구조입니다. 따라서 **VLM 없는 분석**과 **처음부터 네트워크가 전혀 필요 없는 실행**은 구분해야 합니다. 모델 파일을 이미 갖고 있는지, OCR 추가 모델이 필요한지 등에 따라 준비 과정이 달라집니다. [다운로드·검증](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/stems.py#L32-L54), [초기 준비](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/docs/cli.md#L26-L28)

촬영 측면에서는 `aspects/`가 구도·카메라·조명·색보정 등의 측정값과 시각 출처를 정리합니다. 값이 측정됐다는 사실과 어떤 광원·장비를 실제로 사용했는지는 같은 결론이 아닙니다. 프로젝트 스킬도 측정·VLM·검토 출처를 병렬로 제시하도록 설명하며, AI·3D의 빛 설명은 실제 촬영 계획과 구별합니다. [측정 연결](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/pipeline.py#L147-L154), [촬영 계획 연결](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/pipeline.py#L707-L723), [출처별 촬영 해석](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/skills/rea-video/SKILL.md#L65-L68)

### 7. 재제작 계획은 모델 능력과 타임라인을 함께 봅니다

`Planner`는 `routing.yaml`과 `models/*.yaml`을 읽습니다. 원시 분류 이름을 직접 특정 공급자 API에 묶는 대신, 필요한 능력 원어와 후보 모델을 연결합니다. 입력 영상의 제작 방식을 추정하는 문제와, 지금 어떤 도구로 비슷하게 만들 수 있는지 추천하는 문제는 분리됩니다. 모델의 스펙·가격·상태는 **이 커밋의 능력표에 기록된 값**이며 최신 제품 정보나 독립 검증 결과로 소개하지 않습니다. [종류별 경로](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/plan.py#L14-L27), [데이터 로딩](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/plan.py#L247-L259), [능력표 구조](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/capabilities/README.md#L1-L25)

`production_plan()`은 인접 샷의 색상 히스토그램 등으로 장면 유사성을 구하고, 같은 장면의 생성 대상 샷을 묶습니다. 사이에 UI·스크린샷 같은 삽입물이 있으면 생성 샷을 끊지 않고 묶었다가 편집 단계에서 그 삽입물을 끼워 넣을 수 있습니다. 그다음 모델의 길이·multi-shot·참고 입력 능력과 선호 길이를 읽어 생성 단위를 나눕니다. [모델과 연속 묶음](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/production.py#L133-L187), [생성 단위 구성](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/production.py#L375-L405)

특히 `_split_run()`은 가능한 자르기 위치를 탐색하는 **동적 계획법**입니다. 호출 단위 수에 기본 비용을 부여하고, 선호 길이를 넘는 다중 샷이나 최소 길이보다 짧은 단위에는 벌점을 더합니다. 다중 샷 묶음의 길이 제약을 적용하고 누적 비용이 작은 경로를 복원합니다. 이 비용은 설계상의 목적함수이며 실제 API 금액·지연·품질을 측정한 결과는 아닙니다. 장면 유사성 역시 원 저자가 실제 몇 번 생성했는지를 복원했다는 증거가 아닙니다. [단위 분할 알고리즘](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/production.py#L190-L212), [생성 단위의 검증 범위](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/eval/RESULTS.md#L218-L234)

계획은 촬영할 샷, 생성할 샷, 코드로 만들 샷, 로컬 이미지 이동, 가져와야 할 기존 소재로 나뉩니다. 자막·강조 글자는 생성 프롬프트에 넣지 않고 후반 포장 타임라인으로 다시 얹도록 안내합니다. 여기까지의 기본 산출물은 구조화된 계획입니다. [포장·촬영·코드·기타 경로](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/production.py#L420-L450)

### 8. 외부 생성과 로컬 조립은 선택적 후속 경로입니다

README의 “영상을 렌더링하지 않는다”는 소개는 **주 분해기의 분석·계획 역할**을 강조한 표현으로 읽어야 합니다. 저장소 전체에 영상 생성·합성 경로가 없다는 뜻은 아닙니다. `remake-run`은 별도의 capsule-cinema 환경에서 `UniversalVideoGenerationTool`을 불러 생성 작업을 실행하고, `assemble()`은 실제 ffmpeg 합성을 수행합니다. 코드 명세에서 Remotion 프로젝트를 자동 작성하는 기능과 자동 검증 점수표·Remix 전체는 문서에서 미완료로 구분합니다. [소개·FAQ](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/README.md#L198-L212), [구현 단계](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/docs/cli.md#L104-L117), [외부 생성 호출](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/integrations/run_remake.py#L79-L105)

조립의 대체 동작도 알아야 합니다. 생성 결과 파일이 있으면 원 샷 길이와 화면 크기에 맞추고, 정지 이미지 이동이면 로컬에서 만듭니다. 그 외에는 **원본 샷을 다시 가져옵니다**. 따라서 `remake.mp4`가 만들어졌다는 사실만으로 모든 샷을 새로 제작했다고 볼 수 없습니다. `assemble_log.json`의 generated·local_still·original 구분을 확인해야 합니다. 오디오도 해당 경로는 원본 오디오를 다시 매핑하고, 비교 영상에는 원본 오디오를 사용합니다. [샷별 조립과 원본 대체](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/remake.py#L137-L174), [오디오·비교·로그](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/remake.py#L191-L210)

### 9. 평가 숫자는 분모와 개발 이력을 함께 읽어야 합니다

평가 코드를 보면 단순히 전체 프레임의 정답률을 계산하는 방식이 아닙니다. 예측 샷의 **중앙 시각**에서 허용되는 정답 종류를 조회하고, 그 목록에 예측이 있으면 해당 샷의 길이를 정답 시간에 더합니다. 정답이 없는 샷은 건너뜁니다. 이를 기호로 옮기면 다음과 같습니다.

```math
A=\frac{\sum_{s\in S} d_s\,\mathbf{1}[\hat y_s\in G(m_s)]}{\sum_{s\in S}d_s}
```

$`S`$는 중앙 시각에 정답 주석이 있는 예측 샷 집합, $`d_s`$는 그 샷의 길이, $`m_s`$는 중앙 시각, $`G(m_s)`$는 허용 정답 종류 집합, $`\hat y_s`$는 예측입니다. 즉 **주석이 있는 예측 샷의 시간 가중 정확도**입니다. 영상별 정확도 평균은 별도 필드이며, 샷 경계 F1과 실제 소재 검출도 따로 계산합니다. [채점·집계](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/evaluate.py#L247-L303), [경계 F1](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/evaluate.py#L170-L186)

README의 표와 상세 개발 기록을 함께 옮기면 다음처럼 조건을 유지할 수 있습니다. 수치는 모두 저장소가 보고한 값이며 이번 리뷰의 재실행 결과가 아닙니다.

| 기록과 대상 | 보고값 | 해석에 필요한 조건 |
| --- | --- | --- |
| 11월 2일 새 디코딩: labels 15개 | 도구 전용 98.3% | 규칙 설계에 사용한 조정 집합입니다. |
| 같은 시점: holdout 9개 / holdout2 7개 | 99.6% / 98.9% | 처음의 집합 이름과 최종 규칙에 대한 독립성을 구분해야 합니다. |
| 재인코딩 articles 10개 | 도구 전용 88.6% | 개발 집합이며 원본 파일과 조건이 다릅니다. |
| README의 VLM / 검토 추가 행 | articles 99.6% / 100% 등 | 상세 기록은 11월 1일의 결과이며 새 디코딩에서 재측정하지 않았다고 밝힙니다. |
| 11월 4일 daihuo 2개 | 도구 46.4%, VLM 추가 63.9%, 검토 추가 97.5% | 다른 실제 영상에서의 시간 가중 결과이며, VLM만으로 충분하지 않은 사례를 포함합니다. |
| 11월 5일 캐시 재분류 daihuo | Gemini 경로 70.3%, 검토 97.5% | 저장된 특징·시각 답변을 다시 융합한 후속 기록입니다. |

[README 정확도](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/README.md#L157-L174), [새 디코딩 개요](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/eval/RESULTS.md#L5-L15), [캐시와 새 디코딩](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/eval/RESULTS.md#L325-L343), [daihuo](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/eval/RESULTS.md#L346-L369), [후속 회귀](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/eval/RESULTS.md#L404-L431)

**첫째, holdout이라는 파일명만으로 끝까지 독립된 시험이 되지는 않습니다.** 초기 holdout의 오답으로 프레임률 규칙을 추가했고, 이후 VLM gate를 articles·holdout·holdout2 세 묶음에서 비교·선택했습니다. 기록은 그 시점부터 세 집합 모두 “보지 못한 영상”이 아니라고 명시합니다. 실제 소재 검출의 holdout2도 첫 75.6%에서 수정 후 97.2%로 바뀌었으며 독립성을 잃었다고 적습니다. 최신 규칙의 높은 점수를 새로운 맹검 데이터에 대한 일반화 추정으로 바꾸지 않아야 합니다. [초기 변경](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/eval/RESULTS.md#L9-L23), [gate 선택 이력](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/eval/RESULTS.md#L139-L157)

**둘째, 캐시 재분류와 파이프라인 전체 회귀는 다릅니다.** `eval`은 기존 `breakdown.json`을 재사용할 수 있습니다. 이때 현재 규칙으로 다시 분류하더라도 오래된 특징이 남아, 포장 분석이 크롭 영역을 바꾼 영향은 검사하지 못할 수 있습니다. 개발 기록의 99.9/99.6/99.8%가 새 디코딩에서 98.3/99.6/98.9%로 달라진 이유가 이것입니다. `clean_region`의 수정 뒤에도 그 표는 아직 새 디코딩으로 재측정하지 않았다고 밝힙니다. 코드에는 `--fresh`와 재분석 대상을 지정하는 `--only`가 있습니다. [캐시·재분석](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/evaluate.py#L188-L246), [평가 옵션](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/cli.py#L434-L443), [회귀 발견](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/eval/RESULTS.md#L325-L343)

**셋째, 이후 기록의 표본 수도 달라집니다.** 11월 4–5일 회귀에는 로컬에서 구할 수 있는 labels 7개·holdout 7개·holdout2 3개만 남았습니다. 해당 점수를 원래 15·9·7개와 같은 모집단의 새 수치로 대체할 수 없습니다. README도 예제 MP4를 저장소 크기 때문에 재압축하여 플랫폼 태그가 없어졌으므로 원 보고서와 다른 결과가 나올 수 있다고 설명합니다. [후기 회귀 범위](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/eval/RESULTS.md#L383-L431), [예제 입력의 차이](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/README.md#L81-L83)

**넷째, 실패 사례는 융합 방식의 의미를 보여 줍니다.** daihuo 튜토리얼에서는 카메라로 실제 스마트폰 화면을 촬영한 부분이 3D·AI처럼 보였고, Gemini는 실사라고 보았지만 gate가 그 의견을 막았습니다. 11월 4일에는 도구와 VLM 결과가 모두 22.9%에 그쳤고, 검토 이후 97.7%였습니다. 샷별 native cadence를 허용한 후에도 일부 장면은 남았습니다. 따라서 모델을 하나 더 붙이면 언제나 정확도가 오른다는 구조가 아닙니다. [실패와 gate 수정](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/eval/RESULTS.md#L346-L406)

음향·포장 평가도 큰 정확도 숫자와 분리해야 합니다. 음악 출처는 초기 5개 중 2개만 맞았고, 효과음 존재 검출은 4개 중 2개였습니다. 자막·포장 평가는 개발 중 반복해서 본 세 영상의 생성 코드·자막 JSON을 정답으로 삼았다고 밝힙니다. 경계 F1 1.00 역시 개요 표에서는 정답이 있는 두 영상의 결과입니다. 이 기록은 기능별 현재 상태를 설명하는 자료이며, 모든 콘텐츠·모든 탐지 종류의 검증을 뜻하지 않습니다. [오디오 분모](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/eval/RESULTS.md#L31-L54), [포장 평가와 독립성](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/eval/RESULTS.md#L289-L323), [경계 평가 범위](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/eval/RESULTS.md#L7-L11)

## 설치와 사용

아래 명령은 고정 커밋의 README·CLI 문서에 있는 사용 흐름을 인용한 것입니다. 이 리뷰에서는 실행하지 않았습니다.

```bash
brew install ffmpeg
git clone https://github.com/JuneYaooo/rea-video && cd rea-video
bash scripts/install_skill.sh
rea-video --help
```

설치 스크립트는 CLI 설치와 스킬 디렉터리 연결을 수행하는 경로이며, 단순한 라이브러리 import와 다릅니다. README의 clone 명령은 최신 기본 브랜치를 받으므로, 이 리뷰와 같은 동작을 읽으려면 분석 SHA와 설치 대상을 구분해야 합니다. 수동 OCR 설치에서는 GUI OpenCV 패키지와 headless 패키지가 같은 `cv2` 디렉터리를 사용해 충돌할 수 있다고 문서가 설명합니다. [설치](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/README.md#L36-L48), [수동 설치·주의점](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/docs/cli.md#L5-L24)

```bash
rea-video decompose ref.mp4 -o out/ref
rea-video summary out/ref/breakdown.json
rea-video review out/ref
rea-video apply-review out/ref --by zcode
```

`decompose` 뒤 `review_answers.json`에 실제로 본 내용을 채우고 `apply-review`해야 검토가 결과에 반영됩니다. 위 명령 네 줄만 연달아 실행했다고 시각 검토가 저절로 끝나는 것은 아닙니다. 외부 시각 모델을 쓰려면 엔드포인트·키·모델을 설정하고 `--vlm`을 켜며, 결과의 VLM 상태도 확인합니다. [기본·검토 흐름](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/docs/cli.md#L30-L53), [상태 설명](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/vlm.py#L78-L98)

출력은 `breakdown.json`, `report.md`, `report.html`, 스토리보드·샷 이미지, 오디오와 포장 파일 등입니다. 기본 보고서 언어는 중국어이며 도구는 중국어·영어를 지원합니다. 한국어 README가 있다는 사실과 CLI 보고서가 한국어를 기본 지원한다는 사실은 다릅니다. 스킬 문서는 그 외 언어 요청에 영어 보고서를 바탕으로 별도 번역하는 흐름을 안내합니다. [중간 표현](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/pipeline.py#L267-L279), [보고서 출력](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/report.py#L738-L743), [언어 지원](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/skills/rea-video/SKILL.md#L81-L87)

## 한계와 주의점

### 모델·API·파일 경계를 구분해야 합니다

VLM을 켜면 샷 영상·키프레임과 선택적인 전체 영상이 **설정한 외부 엔드포인트로 전송**됩니다. API 키는 Bearer 헤더에 사용됩니다. 클라이언트는 로컬이 아닌 HTTP 주소에 경고하지만 요청을 차단하는 구조는 아닙니다. 분석 결과·캐시·추출 이미지·원본 경로가 로컬 출력에 남는 점도 함께 확인해야 합니다. CLI는 임의의 현재 디렉터리 `.env`를 자동으로 읽지 않고 패키지 기준 파일과 명시·저장된 설정 파일을 사용하도록 구현합니다. [미디어 인코딩·요청](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/vlm.py#L101-L169), [환경 파일 경계](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/cli.py#L17-L34)

기억 기능은 기본적으로 `~/.rea-video`에 환경 선호와 정정을 보관합니다. 같은 영상의 재분석과 새 독립 평가를 구분하는 이유이기도 합니다. 평가의 새 분해 경로는 `memory=False`를 명시하지만, 저장된 VLM·검토 답변과 특징을 재사용하는 경로의 조건도 별도로 확인해야 합니다. [기억의 효과](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/memory.py#L1-L10), [저장 위치](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/memory.py#L38-L53), [평가 경로](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/rea_video/evaluate.py#L188-L246)

### 원 제작 과정의 완전한 복원으로 읽지 않습니다

프로젝트는 스스로 24p 실사와 AI 영상, 압축된 실사와 렌더링, AI 음악과 기존 반주를 혼동하는 사례를 기록합니다. 측정값·시각 모델의 설명·생성기 추측은 근거의 강도가 다릅니다. 재제작 프롬프트와 생성 단위는 원본과 비슷한 결과를 만들기 위한 **제안**이지, 원저자의 비공개 프롬프트나 호출 이력을 알아냈다는 증거가 아닙니다. [24p·불확실성](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/eval/RESULTS.md#L243-L270), [생성 단위의 경계](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/eval/RESULTS.md#L218-L234)

### 코드 라이선스와 원본 영상의 권리는 별개입니다

저장소 루트는 Apache License 2.0을 두고 `NOTICE`에 **Copyright 2026 JuneYaooo**를 표시합니다. 이는 코드의 공개 조건이며, 예제 영상에 들어 있는 음악·인물·브랜드·타인의 촬영물까지 일괄 사용할 수 있다는 뜻이 아닙니다. README도 원본과 타사 재제작 예시는 비교용으로 제시하며, 타인의 소재·음악·인물 외형을 그대로 재게시하지 말라고 명시합니다. 이 글은 원 영상을 복사하지 않고 코드에서 작성한 도식을 사용했습니다. [Apache-2.0](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/LICENSE#L1-L202), [저작권 고지](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/NOTICE#L1-L4), [비교 소재](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/README.md#L158-L158), [사용 범위 안내](https://github.com/JuneYaooo/rea-video/blob/3522250b4d3e667610a175c0f188ac3d725b41cd/README.md#L216-L219)

## 결론

rea-video에서 배울 핵심은 **영상 분석을 여러 증거가 붙은 중간 표현으로 만들고, 판정과 제작 계획을 다시 계산할 수 있게 나눈 구조**입니다. 샷 경계·픽셀 통계·컨테이너·음향·OCR을 모으고, 시각 모델과 검토를 조건부로 합친 뒤, 촬영·생성·코드·소재 경로로 변환합니다.

이 설계는 도구가 잘 측정하는 시간·위치와 시각 모델이 제안하는 의미를 연결하지만, 융합 규칙 자체도 개발 데이터의 영향을 받습니다. 따라서 프로젝트의 수치는 높은 정확도 한 줄보다, 어떤 입력·캐시·검토·판정 규칙에서 나온 값인지를 함께 읽을 때 의미가 있습니다. 코드 리뷰 관점에서 가장 유용한 부분도 그 경계와 수정 경로가 드러나 있다는 점입니다.

### 이 글에서 다루지 못한 부분

`packaging.py`의 모든 스티커·글자 유형과 스타일 조합, `aspects/` 각 측정치의 보정 정확도, 오디오의 모든 특징량, 실제 VLM 공급자별 응답·지연·비용, 모든 예제 영상의 시각 판정, capsule-cinema 내부 구현과 생성·합성 결과의 품질은 전수 분석하거나 실행 검증하지 않았습니다. 저장소 테스트는 구현 의도를 읽는 자료이며 이번 리뷰에서 통과를 확인한 테스트가 아닙니다.
