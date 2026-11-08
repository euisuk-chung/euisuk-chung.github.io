---
type: "Repo Review"
title: "[Repo Review] Pixelfx — 코드로 그린 픽셀 효과에 동작과 타격감을 붙이는 방법"
description: "Pixelfx의 픽셀·빛 버퍼, 시드 기반 효과 재생, 3D 뼈대와 타격 정지, 스프라이트 출력 및 제작 스킬의 관찰·수정 흐름을 고정 커밋 코드로 분석합니다."
date: "2026-11-09"
tags:
  - "Repo Review"
  - "Tools"
  - "Visualization"
  - "Vibe Coding"
resource: "https://github.com/patch-gg/pixelfx/tree/a84159688af3ca37a4be05a0d422b94451b2e24e"
generated:
  by: "process:blog-review"
  at: "2026-11-09T06:09:22+09:00"
sources:
  - id: "patch-gg/pixelfx"
    resource: "https://github.com/patch-gg/pixelfx/tree/a84159688af3ca37a4be05a0d422b94451b2e24e"
    title: "Pixelfx"
    last_modified: "2026-10-31T08:41:17+00:00"
  - id: "pixelfx-acts-original"
    resource: "https://raw.githubusercontent.com/patch-gg/pixelfx/a84159688af3ca37a4be05a0d422b94451b2e24e/docs/readme/acts.gif"
    title: "Pixelfx README acts animation, unchanged original"
status: "stable"
year: "2026"
analyzed_at: "2026-11-09T06:09:22+09:00"
source_id: "patch-gg/pixelfx"
source_revision: "a84159688af3ca37a4be05a0d422b94451b2e24e"
source_title: "Pixelfx"
source_type: "repo"
source_url: "https://github.com/patch-gg/pixelfx/tree/a84159688af3ca37a4be05a0d422b94451b2e24e"
visual_sources:
  - path: "/img/reviews/2026/pixelfx-repo-review/architecture.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/core/fx.js#L51-L130"
    evidence:
      - "https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/core/act.js#L208-L217"
      - "https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/tools/lib/fxlib.mjs#L53-L111"
    caption: "리뷰어 작성, 분석 커밋 기준. 효과·동작 재생이 픽셀 버퍼와 RGBA 출력을 공유하는 흐름"
  - path: "/img/reviews/2026/pixelfx-repo-review/act-clock.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/core/act.js#L247-L300"
    evidence:
      - "https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/core/act.js#L30-L50"
    caption: "리뷰어 작성, 분석 커밋 기준. 타격 정지와 효과 시각·포즈 갱신의 분리"
---

## 들어가며

게임에서 불꽃이 보이는 것과 공격이 묵직하게 느껴지는 것은 다른 문제입니다. 검을 휘두르기 전의 준비 동작, 닿는 순간의 짧은 정지, 몸을 따라 남는 잔상과 맞은 표적의 반응까지 연결되어야 타격의 흐름이 읽힙니다. Pixelfx는 픽셀 이펙트를 이미지 묶음 대신 **작은 JavaScript 프로그램**으로 보관하고, 그 효과를 실제 동작과 함께 재생하거나 스프라이트 시트로 내보내는 저장소입니다. [프로젝트 소개](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/README.md#L7-L25)

이 글은 `patch-gg/pixelfx`의 **`a84159688af3ca37a4be05a0d422b94451b2e24e`**, 패키지 버전 **0.3.0**을 고정한 정적 코드 리뷰입니다. 대상 코드를 설치·빌드·실행하거나 검사를 돌리지는 않았습니다. 문서의 화면 예시와 실제 처리 경로를 대조했으며, 아래 애니메이션도 이번 리뷰에서 생성한 결과가 아니라 같은 커밋에 들어 있는 원본입니다. [패키지 매니페스트](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/package.json#L1-L23)

![검 휘두르기·망치 공격·지면 타격·마법·얼음·달리기를 캐릭터와 표적의 움직임으로 보여 주는 Pixelfx 원본 애니메이션](https://raw.githubusercontent.com/patch-gg/pixelfx/a84159688af3ca37a4be05a0d422b94451b2e24e/docs/readme/acts.gif)

*저장소의 `docs/readme/acts.gif`를 고정 커밋의 외부 원본 URL로 변형 없이 인용했습니다. 효과 자체뿐 아니라 준비 동작·접촉 정지·회복과 표적의 반응을 보여 주는 원본 예시입니다. 약 5.9 MiB입니다. [고정 커밋의 원본](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/docs/readme/acts.gif) · 코드와 효과의 MIT 고지 및 차용 출처는 아래 라이선스 절에 보존했습니다.*

## Pixelfx는 무엇인가요

Pixelfx는 **로컬 좌표와 시간에 따라 픽셀을 그리는 효과 라이브러리, 캐릭터 동작 재생기, 내보내기 도구, 제작용 스킬**을 묶은 프로젝트입니다. 분석 커밋의 `src/fx/<category>/*.js`에서 `_`로 시작하는 보조 파일을 제외하면 효과 모듈은 244개, 디렉터리는 21개입니다. 이 중 73개는 `act` 데이터를 정의하며, `moves`의 12개도 이 수에 포함됩니다. README의 “61개 캐릭터 효과와 12개 전체 동작”이라는 구분과 맞습니다. 이 개수는 파일을 정적으로 집계한 것이며 효과별 실행 성공률이 아닙니다. [목록 규칙](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/tools/lib/fxlib.mjs#L14-L24), [범주별 목록](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/README.md#L29-L57), [동작 설명](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/README.md#L102-L104)

| 구성 | 독자가 얻게 되는 것 | 코드에서의 단위 |
| --- | --- | --- |
| 효과 라이브러리 | 불·얼음·폭발·날씨·상태·UI 같은 픽셀 표현 | 파일 하나가 효과 하나입니다. |
| 실시간 재생 | 위치·반전·색·시간을 바꿔 그리는 인스턴스 | `createFx()`가 업데이트와 그리기를 제공합니다. |
| 동작 재생 | 준비·발사·접촉 정지·회복·표적 반응 | `createAct()`가 효과와 `act` 데이터를 함께 다룹니다. |
| 내보내기 | 투명 PNG 시트와 프레임 JSON, 미리보기 영상 | `tools/render.mjs`와 `tools/act.mjs`가 코어를 사용합니다. |
| 제작 스킬 | 초안→렌더→관찰→수정→검사의 작업 순서 | `skills/pixelfx/SKILL.md`가 제작 절차를 설명합니다. |

“AI로 만든 효과”라는 문구만 보면 실행 때마다 모델이 그림을 생성한다고 생각하기 쉽습니다. 그러나 확인한 재생 코어는 JavaScript 수치 계산과 픽셀 버퍼를 사용합니다. Claude Code 스킬은 효과를 **작성·수정하는 단계의 지침**이고, 이미 작성된 효과를 게임에서 재생하는 경로에는 LLM API 호출이 들어 있지 않습니다. [공개 코어 진입점](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/core/index.js#L1-L16), [스킬의 역할](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/skills/pixelfx/SKILL.md#L87-L113)

## 아키텍처와 디렉터리 구조

패키지는 ES Module이며 Node 요구사항은 `>=18`입니다. `exports`는 코어, 개별 효과, 개별 코어 모듈을 노출합니다. 런타임 의존성 목록은 없고, 개발 의존성으로 `esbuild`가 선언돼 있습니다. 갤러리 번들 도구는 이를 실제로 사용하므로 “아무 작업에도 설치가 필요 없다”로 범위를 넓히면 안 됩니다. GIF·MP4 출력은 별도의 `ffmpeg` 프로세스에 의존합니다. [패키지 설정](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/package.json#L1-L23), [갤러리 번들](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/tools/build-gallery.mjs#L7-L19), [영상 출력](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/tools/lib/fxlib.mjs#L244-L261)

| 위치 | 주요 책임 |
| --- | --- |
| `src/fx/<category>/` | 효과의 메타데이터·그리기·선택적 시뮬레이션·동작 데이터 |
| `src/core/fx.js`, `painter.js` | 프레임 생성, 재생 상태, 좌표 변환, 픽셀·도형·빛 쓰기 |
| `src/core/math.js`, `color.js`, `sim.js` | 시드 난수·보간, 팔레트, 입자·파편·광원 |
| `src/core/rig.js`, `act.js`, `chain.js` | 뼈대 계산, 동작 재생과 표적, 여러 효과의 시간별 합성 |
| `gallery/app.js` | 효과 선택과 옵션 조작, Canvas 재생, 브라우저용 내보내기 |
| `tools/` | 목록·초안·렌더링·시트·동작·검사·갤러리 생성 도구 |
| `docs/AUTHORING.md`, `skills/pixelfx/` | 효과 계약과 눈으로 보고 다듬는 제작 절차 |

![효과 모듈이 재생 코어와 픽셀 버퍼를 거쳐 게임 화면 또는 출력 파일로 이어지는 Pixelfx 구조]({{ '/img/reviews/2026/pixelfx-repo-review/architecture.svg' | relative_url }})

*리뷰어 작성, 분석 커밋 기준. `createAct`는 내부에 `createFx`를 포함합니다. 도식은 책임의 흐름을 요약하며, 모든 호출을 나열한 그림은 아닙니다. [효과 인스턴스](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/core/fx.js#L51-L92), [동작 인스턴스](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/core/act.js#L208-L217), [프레임 내보내기](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/tools/lib/fxlib.mjs#L53-L111)*

이 구조의 장점은 효과의 원본과 파일 출력기가 별개 구현으로 갈라지지 않는다는 데 있습니다. 게임은 같은 `createFx`·`composite`를 호출하고, 도구는 그 호출을 여러 시점에 반복해 이미지로 묶습니다. 다만 이 공유 구조 자체가 서로 다른 게임 엔진의 임포터 호환성이나 실행 성능을 검증한 결과는 아닙니다.

## 작동 원리

### 1. 효과 하나는 메타데이터와 그리는 방법을 정의합니다

`meta`에는 캔버스 크기 `size`, 원점 `origin`, 지속 시간 `duration`, 반복 여부 `loop`, 출력 프레임률 `fps`, 기본 옵션 등이 들어갑니다. 그 위에 두 가지 구현 방식을 허용합니다. [제작 계약](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/docs/AUTHORING.md#L13-L64)

- **순수 효과**는 `draw(p, t, o)`를 정의합니다. 같은 시각과 옵션에서 그림을 계산하는 방식입니다. 횃불은 2초 반복, 72×120 크기, 30fps 메타데이터를 가지고 시간·시드 기반 노이즈로 불꽃을 그립니다. [횃불 정의](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/fx/fire/torch.js#L6-L24), [실제 그리기](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/fx/fire/torch.js#L80-L91)
- **시뮬레이션 효과**는 `create(o)`가 상태를 만들고 `update(dt)`와 `draw()`를 반환합니다. Frost nova는 시드 난수 생성기와 입자·파편·빛 목록을 만들고, 충전·방출·확산·유지·녹는 단계를 시간에 따라 진행합니다. 이미 지나간 시각을 바로 그리는 순수 함수와는 사용 방식이 다릅니다. [초기 상태](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/fx/ice/frost-nova.js#L80-L102), [업데이트와 방출](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/fx/ice/frost-nova.js#L121-L185)

`createFx()`는 기본 옵션과 호출자 옵션을 합치고, `create`가 있으면 인스턴스를 만듭니다. 길이가 다른 색상 램프는 기본 길이로 재표본화하며, 캐릭터가 필요한 효과에는 기본 캐릭터 데이터를 넣습니다. 색상 램프란 어두운 색에서 밝은 색까지 순서대로 정리한 색 배열입니다. 효과가 “다섯 번째 색”을 읽더라도 짧은 사용자 팔레트 때문에 빈 값이 생기지 않게 하는 구조입니다. [옵션 병합](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/core/fx.js#L31-L43), [인스턴스 생성](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/core/fx.js#L51-L56)

시간도 구분해야 합니다. `createFx.update(dt)`는 외부에서 받은 시간 간격을 `ceil(dt * 120)`개의 작은 간격으로 나눠 시뮬레이션에 전달합니다. 이는 보통 한 번의 물리 업데이트가 약 1/120초보다 커지지 않게 하는 방식이지, 코어 전체가 고정 12fps로 움직인다는 뜻이 아닙니다. 갤러리는 별도로 `meta.fps`에 맞춰 누적 시간을 소비합니다. [업데이트 분할](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/core/fx.js#L63-L69), [갤러리 시계](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/gallery/app.js#L67-L79)

일회성 효과는 `done()`이 지속 시간 도달을 알려 주며, `stop()`을 부르면 0.3초의 fade 경로가 적용됩니다. 인스턴스가 스스로 게임의 객체 목록에서 제거되는 것은 아니므로, 호출자는 완료 상태를 보고 수명을 관리해야 합니다. [중단과 완료](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/core/fx.js#L85-L91)

### 2. 색과 빛을 분리한 뒤 마지막에 합칩니다

프레임의 핵심 자료구조는 단순합니다. [원문 코드](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/core/fx.js#L8-L18)

```js
export function createFrame(w, h, ox = 0, oy = 0) {
  return { w, h, ox, oy, color: new Uint32Array(w * h), light: new Uint32Array(w * h) };
}
```

각 픽셀을 32비트 정수 하나로 저장하는 버퍼가 두 개 있습니다. `color`는 물체의 색과 투명도를, `light`는 더해서 밝히는 광량을 담습니다. 발광을 일반 물체의 색과 같은 통로에 넣지 않아 불꽃의 밝은 중심, 테두리, 주변 빛을 따로 조절할 수 있습니다. `clearFrame()`은 다음 프레임을 위해 두 배열을 0으로 채웁니다.

`Painter`는 효과의 로컬 좌표를 실제 프레임 좌표로 옮깁니다. 위치·좌우 반전·회전을 먼저 설정하고, 픽셀 중심을 기준으로 정수 셀에 착지시킵니다. 효과 구현은 “내 원점에서 오른쪽 5픽셀”처럼 작성하며, 게임 속 절대 위치를 직접 알 필요가 없습니다. [배치와 좌표 변환](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/core/painter.js#L30-L43)

투명도를 다루는 방식도 하나가 아닙니다. `dot()`은 4×4 Bayer 임계값을 이용해 픽셀을 찍거나 생략하는 **순서 디더링**을 사용합니다. 반면 `blend()`·`disc()`는 반투명 색을 실제로 합성하여 연기와 수증기처럼 부드러운 덩어리를 표현합니다. 코드 상단의 “color는 blended가 아니다”라는 오래된 주석만 보고 반투명 합성이 없다고 설명하면 `blendPx()` 구현을 놓치게 됩니다. [Bayer 임계값과 쓰기](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/core/painter.js#L9-L10), [색·빛 쓰기와 반투명 합성](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/core/painter.js#L45-L87)

마지막 `composite()`는 배경 위에 색을 놓고 빛을 더한 뒤 RGBA 바이트로 바꿉니다. 투명 배경에서는 빛을 색과 알파로 변환해 시트에 담습니다. 따라서 PNG에는 실시간의 독립 `light` 버퍼가 그대로 들어가는 것이 아닙니다. 밝은 배경과 어두운 배경에서 같은 느낌을 보장하는 범용 가산 블렌딩 파일도 아닙니다. 스킬 문서 역시 어두운 장면에서 잘 읽히며 밝은 장면에서는 색을 다시 조정하거나 어두운 레이어를 쓰라고 설명합니다. [합성 구현](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/core/fx.js#L95-L130), [시트의 빛 설명](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/skills/pixelfx/SKILL.md#L66-L72)

### 3. 앞뒤 레이어는 캐릭터를 중심으로 나뉩니다

`draw(frame, "back")`는 뒤쪽 그리기, `draw(frame, "front")`는 앞쪽 그리기를 실행합니다. 효과가 캐릭터를 둘러싼 원이라면 먼 쪽 반원은 캐릭터 뒤에, 가까운 쪽은 앞에 놓아야 입체감이 생깁니다. `createFx.draw()`는 선택한 레이어에 따라 `drawBack()`과 `draw()`를 호출합니다. 다만 이 두 함수는 별도 색 버퍼 두 장을 뜻하지 않습니다. 앞뒤 순서대로 **같은 프레임**에 쓰는 인터페이스입니다. [분기 구현](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/core/fx.js#L70-L83)

Frost nova를 보면 이 계약이 실제로 쓰입니다. 결정의 위치를 만들 때 `back`을 기록하고, `drawBack()`과 `draw()`에서 뒤·앞 결정을 나눠 그립니다. 바닥의 얼음, 파편, 입자와 광원도 각 역할에 맞게 이어집니다. “화려한 PNG를 표시한다”보다 “작은 구성 요소를 올바른 시점과 깊이로 배치한다”에 가까운 구현입니다. [결정 배치](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/fx/ice/frost-nova.js#L87-L100), [앞뒤 그리기](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/fx/ice/frost-nova.js#L187-L213)

호스트 게임도 이 순서를 지켜야 합니다. README 예제는 뒤 효과→캐릭터→앞 효과→합성을 보여 주지만 `drawCharacters()`는 게임 쪽에서 채우는 자리입니다. 실제 합성 결과를 `putImageData`로 덮어쓰는 흐름이므로, 캐릭터를 별도 Canvas에 먼저 그리기만 했다고 자동으로 올바른 앞뒤 관계가 만들어지는 것은 아닙니다. 프레임 안에서 함께 합성하거나 호스트의 레이어 구성을 맞추어야 합니다. [사용 예제](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/README.md#L58-L75), [도구가 캐릭터를 넣는 실제 순서](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/tools/lib/fxlib.mjs#L64-L77)

### 4. 3D 뼈대를 낮은 해상도의 픽셀로 그립니다

회색 캐릭터는 관절마다 그려 놓은 여러 장의 이미지가 아닙니다. `rig.js`는 손·발의 목표 위치와 몸의 기울기·쪼그림·회전 등을 받아 뼈대를 풉니다. 두 뼈의 길이와 목표까지의 거리로 팔꿈치·무릎의 위치를 계산하는 **역기구학(IK)**이 사용됩니다. 목표가 최대 도달 거리보다 멀면 팔·다리를 무한히 늘리는 대신 도달 가능한 위치로 제한합니다. [좌표·측정값·IK](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/core/rig.js#L36-L53), [몸과 관절 계산](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/core/rig.js#L67-L136)

계산된 몸통·관절·무기는 깊이 버퍼를 거쳐 앞뒤가 정해지고, 소수의 명암 단계와 외곽선으로 변환됩니다. 이 때문에 3D 계산을 사용하면서도 결과는 작은 픽셀 캐릭터처럼 보이도록 설계돼 있습니다. 여기서 “3D”는 WebGL 엔진을 필수로 사용한다는 의미가 아닙니다. 확인한 구현은 직접 배열에 그리는 소프트웨어 렌더러입니다. [깊이 버퍼](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/core/rig.js#L139-L158), [명암·경계·외곽선](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/core/rig.js#L370-L427)

특히 `posed()`의 결과에는 현재 픽셀의 위치·색뿐 아니라, 그 픽셀이 서 있는 기본 캐릭터의 어느 픽셀에서 왔는지 나타내는 `src`가 포함됩니다. `act.onBody` 경로는 이 대응을 이용해 얼음·독·스캔선처럼 기본 몸에 그려진 효과를 움직이는 포즈 위로 옮깁니다. 몸 위의 표현과 바닥의 표현을 모두 똑같이 이동시키지 않도록 나누는 부분도 있습니다. [원래 픽셀 대응](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/core/rig.js#L405-L421), [몸에 붙는 효과의 재배치](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/core/act.js#L369-L431)

포즈 결과는 캐시에 저장됩니다. 키를 만들 때 위치 `x`·`y`와 잔상 표시를 빼고 일부 숫자를 양자화해, 배치만 다른 동일 몸 모양을 재사용합니다. 공중 상태는 별도로 키에 반영됩니다. 이것은 캐시의 정적 구현을 확인한 것이며 메모리 사용량이나 프레임 시간 개선을 측정한 결과는 아닙니다. [포즈 캐시](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/core/rig.js#L459-L483)

### 5. `createAct`는 캐릭터 동작과 타격 반응을 시간 데이터로 표현합니다

효과 파일의 선택적 `act`에는 `poses`, `hits`, `target` 또는 `targets`, `dust` 등이 들어갑니다. 효과 자체의 첫 프레임은 `t=0`이므로 음수 시각의 포즈는 준비 동작을 뜻합니다. `actSpan()`은 효과 길이와 포즈의 마지막 시각을 보고 전체 동작의 시작·끝을 정합니다. [동작의 시간 범위](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/core/act.js#L197-L217)

`poseAt()`은 키 사이에서 사지 포즈를 12fps 단계로 보간합니다. 반면 몸의 위치인 `x`·`y`는 현재 시각에서 연속적으로 보간합니다. `"snap"` 키는 이전 포즈를 유지하다가 지정 시점에 바로 바꾸며, 일반 보간과는 다른 타격 모양을 만듭니다. **12fps는 모든 입자와 화면 출력의 프레임률이 아니라 몸 포즈의 시간 표현**이라는 구분이 중요합니다. [포즈 보간](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/core/act.js#L30-L50)

![호출 시간과 타격 정지 시간을 구분하여 효과와 표적을 갱신하는 createAct의 흐름]({{ '/img/reviews/2026/pixelfx-repo-review/act-clock.svg' | relative_url }})

*리뷰어 작성, 분석 커밋 기준. 단순화한 `update()`의 처리 순서입니다. 타격 정지 중에도 화면 흔들림의 남은 시간은 먼저 감소합니다. [구현 근거](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/core/act.js#L247-L300)*

업데이트에서는 화면 흔들림의 남은 시간을 먼저 줄입니다. 타격 정지 `stop`이 남아 있으면 정지 시간만 줄이고 반환하므로 효과 시각·입자·포즈·표적은 그 구간에 진행하지 않습니다. 멈추는 것은 이번 호출에 전달된 인스턴스의 상태입니다. 게임 세계 전체나 다른 캐릭터를 자동으로 멈추는 전역 기능은 아니며, 자신의 캐릭터를 사용하는 게임은 같은 타격 시점에 호스트 쪽도 정지시켜야 합니다. [정지 분기와 타격 이벤트](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/core/act.js#L247-L274), [자체 캐릭터 연결 설명](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/skills/pixelfx/SKILL.md#L76-L83)

표적은 각도를 가진 간단한 스프링 계입니다. 타격은 각속도에 충격을 더하고, 이후 업데이트는 복원력과 감쇠를 적용합니다. 흰 섬광·얼음이나 탄 자국 같은 색 상태·떨어지는 지푸라기도 같은 표적 객체가 처리합니다. 캐릭터 잔상은 반투명 물감 대신 `light` 버퍼에 더하며, 수명 0.16초와 최대 7개라는 제한을 둡니다. [표적의 타격·스프링](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/core/act.js#L110-L140), [잔상 생성·수명](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/core/act.js#L292-L300), [잔상의 빛 합성](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/core/act.js#L334-L345)

`actTiming()`은 동작을 그대로 실행하는 대신 준비 시간, 회복 시간, 타격의 `freeze`·`shake`, 포즈 등을 평범한 데이터로 내보냅니다. 다른 엔진에서 자체 캐릭터를 사용하는 경우 이 데이터가 연결 지점입니다. JS 뼈대 렌더러를 게임 안에 이식하지 않고도 타이밍을 참고할 수 있습니다. [타이밍 출력](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/core/act.js#L450-L465)

### 6. 전체 공격은 기존 효과를 시간표로 조합합니다

`moves/fireball-throw.js`는 새로운 불꽃 시스템을 처음부터 만들지 않습니다. 충전, 불덩이, 작은 폭발을 가져와 `chain()`의 cue로 구성합니다. 파일의 `THROW=0.95`, `FLY=0.46`을 합친 `HIT`은 발사체 종료, 폭발 시작과 타격 이벤트가 만나는 시각입니다. 이런 공통 상수를 사용하면 화면과 표적 반응의 시각을 연결하기 쉽습니다. [동작 상수·타격](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/fx/moves/fireball-throw.js#L6-L44)

다음은 같은 파일의 효과 조합 부분입니다. 예시용으로 새로 만든 코드가 아닙니다. [원문](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/fx/moves/fireball-throw.js#L47-L51)

```js
export const create = chain([
  { fx: charge, t: 0.08, until: THROW, palette: PAL.fire },
  { fx: fireball, t: THROW, until: HIT, x: (t) => 28 + (t - THROW) * SPEED, y: -22 },
  { fx: blast, t: HIT, x: TX },
]);
```

`chain`은 각 cue의 시작 시각이 되면 `createFx`를 만들고, 재생 중인 항목만 그립니다. `x`·`y`가 함수이면 전체 동작의 현재 시각으로 계산하므로 발사체 이동을 별도 효과로 표현할 수 있습니다. 자식마다 `seed`를 달리하고, 끝나는 시각이나 자식 효과의 완료 여부로 재생을 중단합니다. [cue 구성·그리기](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/core/chain.js#L10-L25), [시작과 종료](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/core/chain.js#L27-L39)

여기에는 옵션 전파의 경계가 있습니다. 분석 커밋의 `chain`은 외부 옵션에서 seed를 읽고, 자식에게는 각 cue에 적힌 옵션을 넘깁니다. 상위 동작에 건넨 팔레트나 회전 옵션이 모든 자식에 자동으로 전달된다고 가정할 수는 없습니다. “전체 동작도 효과처럼 사용할 수 있다”는 인터페이스와, 모든 옵션의 의미가 모든 합성 효과에서 동일하다는 보장은 구분해야 합니다. [실제 옵션 생성](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/core/chain.js#L10-L22)

### 7. 미리보기 프레임과 게임용 시트는 다른 출력입니다

`renderFrames()`는 배경·기본 캐릭터를 보여 주는 `shown` 프레임과, 효과만 남기는 `bare` 프레임을 따로 만듭니다. 효과의 메타데이터와 fps로 프레임 수를 정하고, 순서대로 업데이트하면서 두 종류의 RGBA를 기록합니다. 마진이 없고 전체 화면 효과가 아닌 경우에는 가장자리의 빛을 서서히 줄이는 처리도 들어갑니다. 따라서 도구 출력에는 코어 효과 외에 프리뷰·내보내기 정책이 추가됩니다. [프레임 생성](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/tools/lib/fxlib.mjs#L49-L83), [빛 가장자리 처리](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/tools/lib/fxlib.mjs#L123-L143)

| 출력 경로 | 무엇이 들어가나요 | 주요 메타데이터 |
| --- | --- | --- |
| `render.mjs`의 contact sheet | 배경과 필요시 서 있는 캐릭터가 있는 관찰용 프레임 | 시각·fps·반복 여부를 이미지에 표기합니다. |
| `render.mjs --sheet` | `bare`의 투명 RGBA, 기본적으로 효과 단독 | 프레임 사각형·duration·원점·fps·loop |
| `act.mjs --sheet` | 몸·표적까지 포함한 전체 동작 | 확장된 캔버스와 그에 맞게 바꾼 pivot |
| GIF·MP4 | 배경이 있는 프리뷰 프레임을 영상으로 인코딩 | `ffmpeg` 호출과 출력 형식 설정 |

시트의 JSON은 Aseprite 스타일입니다. 각 프레임의 위치·크기·밀리초 duration과 `frameTags`, `meta.pixelfx`의 원점·열 수·반복 정보가 들어갑니다. 효과에 `act`가 있으면 일반 시트에도 동작의 **타이밍 데이터**를 추가합니다. 이것이 곧 일반 시트의 모든 픽셀에 캐릭터 동작까지 들어간다는 뜻은 아닙니다. 몸·표적을 함께 굽는 경로는 `act.mjs --sheet`에서 `renderAct()`를 호출하고 pivot을 다시 설정하는 부분입니다. [시트 생성](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/tools/lib/fxlib.mjs#L220-L241), [전체 동작 시트](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/tools/act.mjs#L21-L30)

README는 여러 엔진의 Aseprite 임포터로 가져올 수 있다고 설명합니다. 이번 분석에서 확인한 것은 그 프레임·메타데이터를 쓰는 코드까지이며 Godot·Unity·Phaser에서의 실제 가져오기 성공은 시험하지 않았습니다. 또한 이미지의 반복 프레임이나 빛·알파가 원하는 방식으로 표시되는지는 엔진의 재생·필터·블렌딩 설정에 달려 있습니다. [문서의 출력 설명](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/README.md#L79-L87)

### 8. 제작 스킬은 생성보다 관찰·수정에 무게를 둡니다

Pixelfx의 스킬은 먼저 기존 효과를 찾고, 팔레트·시드·방향 등 옵션으로 해결할 수 있는지 보도록 합니다. 새 효과가 필요하면 가까운 예시를 읽고 초안을 만든 뒤, contact sheet와 실제 움직임을 보고 가장 큰 문제를 고치는 순서를 설명합니다. 시트에서 프레임을 띄엄띄엄 뽑아 보는 것과, 동작의 연속 프레임으로 타이밍을 판단하는 것도 구별합니다. [기존 효과 탐색](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/skills/pixelfx/SKILL.md#L26-L37), [제작·관찰·수정 과정](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/skills/pixelfx/SKILL.md#L87-L113)

문서는 “흐릿하면 실루엣과 색 수를 단순화”, “가벼우면 준비 동작과 접촉 정지 조정”, “연기가 바둑판 같으면 디더링 대신 실제 반투명 사용”처럼 관찰과 수정 수단을 연결합니다. 이 부분은 독립적인 학습 알고리즘이나 자동 미적 평가 모델이 아니라, 코딩 에이전트와 제작자가 따르는 작업 지침입니다. 이 글에서는 그 지침을 검토 자료로 읽었으며 실행 지시로 따르지 않았습니다. [관찰별 수정 표](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/skills/pixelfx/SKILL.md#L115-L137)

`tools/check.mjs`는 별도의 기계 검사를 담당합니다. 메타데이터, 직접적인 `Math.random` 사용, 캔버스 밖 그리기, 끝나지 않는 일회성 효과, 반복 경계, 동일 시드·동일 조건에서의 재현성, 포즈 순서와 손의 급격한 이동 등을 검사합니다. 다만 상당수 항목은 실패가 아닌 **warning**입니다. 프레임 시간이 느리다는 경고도 구현에서는 중앙값 4ms 초과를 기준으로 하며, 제작 문서의 “2ms 미만” 목표와 같다고 볼 수 없습니다. 이 검사를 실행하거나 모든 효과가 통과했다고 확인한 것은 아닙니다. [동작 검사](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/tools/check.mjs#L23-L69), [효과 검사](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/tools/check.mjs#L77-L205), [종료 코드와 경고](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/tools/check.mjs#L210-L216), [문서의 목표](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/docs/AUTHORING.md#L172-L196)

## 설치와 사용

아래는 같은 커밋의 README와 도구 파일의 사용 예시에 있는 명령입니다. 이번 리뷰에서 실행하지 않았습니다. 브라우저 게임에서 코드를 사용하는 설치 경로와, 저장소의 도구로 파일을 만드는 경로를 구분해 읽어야 합니다. [코드 설치](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/README.md#L77-L77), [시트 출력](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/README.md#L79-L87), [동작 출력 예시](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/tools/act.mjs#L5-L7)

```bash
npm i github:patch-gg/pixelfx
node tools/render.mjs ice/frost-nova --sheet
node tools/act.mjs melee/sword-slash --sheet
```

첫 줄은 GitHub 의존성을 설치합니다. 나머지 명령은 `tools/`가 있는 Pixelfx 체크아웃을 기준으로 한 문서의 사용법입니다. 버전 고정 분석을 했다는 사실과 README 명령이 최신 원격 기본 브랜치를 따라 설치한다는 사실은 다르므로, 재현 가능한 배포에서는 사용할 커밋을 별도로 관리해야 합니다. [설치 문구](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/README.md#L77-L77), [도구의 입력·출력](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/tools/render.mjs#L16-L51)

실시간 사용의 최소 조립은 `createFrame`→`createFx`→매 tick의 `update`→프레임 비우기→그리기→`composite`→호스트 표시입니다. 캐릭터·표적까지 원하면 `createAct`로, 자체 캐릭터를 쓰면 효과와 `actTiming` 데이터를 연결하는 방식으로 나뉩니다. 스프라이트 시트만 사용하는 엔진은 JavaScript 런타임 대신 PNG와 JSON을 가져오는 것이 문서가 제시하는 경로입니다. [README의 실시간 예제](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/README.md#L58-L75), [자체 캐릭터 연동](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/README.md#L138-L145)

제작용 Claude Code 스킬은 README에서 다음 플러그인 명령 또는 `skills/pixelfx` 디렉터리 복사를 안내합니다. 이는 효과 런타임의 필수 의존성이 아니라 새 효과를 찾고 작성하는 작업 환경입니다. [스킬 설치 설명](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/README.md#L150-L158)

```text
/plugin marketplace add patch-gg/pixelfx
/plugin install pixelfx@pixelfx
```

## 한계와 주의점

### 동일 시드와 모든 실행 환경의 동일성은 구별해야 합니다

`Rng`는 시드로 시작하는 정수 난수 생성기이며, `rand()`는 인수로 받은 정수를 해시해 값을 만듭니다. 이 설계는 재현 가능한 효과를 작성하는 기반입니다. 그러나 상태형 효과는 업데이트 횟수·순서에 따라 난수를 소비하고 물리 상태를 누적합니다. `createFx`의 작은 시간 간격 분할만으로 모든 dt·장치·엔진에서 비트 단위로 같은 프레임이 나온다고 입증되지는 않습니다. 검사 코드도 순수 효과의 동일 시각 또는 시뮬레이션의 동일 시드·동일 재생 절차를 비교합니다. [난수 구현](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/core/math.js#L64-L96), [시간 분할](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/src/core/fx.js#L63-L69), [재현성 검사의 범위](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/tools/check.mjs#L166-L199)

### 출력 비용과 검사 목표를 성능 보증으로 읽지 않습니다

소프트웨어 렌더링은 픽셀과 도형, 입자 수에 따라 CPU 작업을 수행합니다. `renderFrames()`는 모든 프레임의 RGBA와 원시 색·빛 배열을 메모리에 보관하고, `writeVideo()`는 확대된 영상 바이트를 모아 `ffmpeg`로 전달합니다. 큰 캔버스·많은 프레임·높은 확대 배율을 사용할 때도 일정 비용이라는 구조가 아닙니다. 구체적인 실행 시간·메모리·게임 프레임률은 이번 정적 리뷰에서 측정하지 않았습니다. [프레임 배열](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/tools/lib/fxlib.mjs#L64-L82), [영상 바이트 구성](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/tools/lib/fxlib.mjs#L244-L260)

### MIT인 코드·효과와 제외된 글꼴을 나눠 봅니다

루트 LICENSE는 코드·효과를 MIT로 배포하며 Patch와 Hugo Duprez의 저작권 고지를 싣습니다. `NOTICE.md`는 Sprite Fusion 효과의 차용과 Hollow Crown의 12fps 포즈·타격 정지·스프링 표적을 별도로 밝힙니다. 반면 `gallery/fonts/PatchPixel-Regular.woff2`는 **All rights reserved이며 루트 MIT의 적용 대상이 아닙니다.** 갤러리 전체를 복제·배포할 때 코드의 MIT만 확인하면 이 예외를 놓칩니다. [루트 LICENSE](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/LICENSE#L1-L22), [차용·제외 고지](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/NOTICE.md#L1-L11), [글꼴 고지](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/gallery/fonts/NOTICE.md#L1-L4)

이 글의 원본 애니메이션 인용은 저장소의 코드·효과 MIT 고지를 따르며 글꼴 파일은 복사하지 않았습니다. 검토한 원본 애니메이션에는 갤러리의 Patch Pixel 제목 글꼴도 보이지 않습니다. 인용한 효과의 저작권·허가 고지를 아래에 보존합니다. Hollow Crown 관련 동작 구현의 출처는 `Copyright (c) 2026 rehan-remade`, MIT입니다. [원본 자산](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/docs/readme/acts.gif), [NOTICE](https://github.com/patch-gg/pixelfx/blob/a84159688af3ca37a4be05a0d422b94451b2e24e/NOTICE.md#L3-L11)

<details>
<summary>인용 자산의 원본 MIT 라이선스 고지</summary>

```text
MIT License

Copyright (c) 2026 Patch
Copyright (c) 2026 Hugo Duprez

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

</details>

## 결론

Pixelfx에서 배울 핵심은 픽셀을 만드는 함수 하나보다 **표현·재생·동작·출력의 계약을 나눈 방식**입니다. 효과 모듈은 로컬 좌표와 시간으로 그림을 정의하고, 코어는 색과 빛을 합성하며, `act`는 준비·접촉·회복의 리듬을 데이터로 붙입니다. 같은 코어를 사용하는 내보내기 도구는 그 결과를 다른 엔진이 소비할 이미지와 메타데이터로 바꿉니다.

제작용 스킬도 이 구조와 연결됩니다. 효과의 코드를 수정하고 결과를 눈으로 검토하는 순환, 타이밍을 연속 프레임에서 보는 관점, 기계 검사와 미적 판단을 분리하는 점이 이 저장소의 특징입니다. 실행 시 생성 모델에 의존하지 않는 작은 효과 프로그램이 어떻게 게임의 시각적 반응으로 이어지는지 보여 주는 사례입니다.

### 이 글에서 다루지 못한 부분

244개 효과의 개별 시각 품질과 모든 파라미터 조합, 브라우저·게임 엔진별 성능, 실제 PNG·JSON 임포트, `sim.js`의 모든 입자 종류와 무기별 형상, 갤러리의 모든 인터랙션은 전수 검증하지 않았습니다. 핵심 런타임·행동·합성·출력 경로와 대표 효과를 정적으로 분석한 범위이며, 원본 애니메이션을 리뷰의 재현 실험으로 제시하지 않습니다.
