---
type: "Guide"
title: "AI 에이전트로 영상과 3D 만들기, 스킬과 도구 12가지"
description: "X에서 소개된 영상·모션·Blender·웹 3D 프로젝트 12개를 살펴보고, 만들고 싶은 결과물에 따라 제작 엔진과 에이전트 스킬을 고르는 기준을 정리합니다."
date: "2026-11-09"
tags:
  - "AI Agent"
  - "Tools"
  - "MCP"
resource: "https://x.com/Y0urDumble/status/2119023461267833047"
generated:
  by: "process:blog-review"
  at: "2026-11-09T07:41:56+09:00"
sources:
  - id: "x:2119023461267833047"
    resource: "https://x.com/Y0urDumble/status/2119023461267833047"
    title: "Dumble의 영상·모션·Blender·웹 3D 도구 목록"
  - id: "heygen-com/hyperframes"
    resource: "https://github.com/heygen-com/hyperframes/blob/327e20208c3f542841de670cce54754473f58d30/README.md"
    title: "HyperFrames"
  - id: "hyperframes:reverse-any-video"
    resource: "https://github.com/heygen-com/hyperframes/blob/327e20208c3f542841de670cce54754473f58d30/skills/reverse-any-video/SKILL.md"
    title: "reverse-any-video"
  - id: "remotion-dev/skills"
    resource: "https://github.com/remotion-dev/skills/blob/a2824c67f8b4585c294a8101db9f9f0ad3c643f8/README.md"
    title: "Remotion Agent Skills"
  - id: "OpenMontageInc/OpenMontage"
    resource: "https://github.com/OpenMontageInc/OpenMontage/blob/356b5fa92474998c9f9a0782fd5547d05837d284/README.md"
    title: "OpenMontage"
  - id: "greensock/gsap-skills"
    resource: "https://github.com/greensock/gsap-skills/blob/aed9cfd3277740755f6bfc1155c7aa645403b760/README.md"
    title: "GSAP AI Skills"
  - id: "Vincentwei1021/video-shotcraft"
    resource: "https://github.com/Vincentwei1021/video-shotcraft/blob/1266a3ec4831289c4d893d42dd5102723658039a/README.md"
    title: "video-shotcraft"
  - id: "Tejashmakwana/motionmaxxing"
    resource: "https://github.com/Tejashmakwana/motionmaxxing/blob/8c8ec0f2a6f6c9a0da15cd24f7b1298ab298368c/README.md"
    title: "motionmaxxing"
  - id: "ahujasid/mcp-for-blender"
    resource: "https://github.com/ahujasid/mcp-for-blender/blob/2e4b0bc294694b1570d76ed01be657c22e6d02a0/README.md"
    title: "Blender MCP"
  - id: "arjun988/blender-skills"
    resource: "https://github.com/arjun988/blender-skills/blob/904f095d8f36a6e72adaebb08d07f884a074743d/README.md"
    title: "Blender Skills"
  - id: "achimala/dream-loop"
    resource: "https://github.com/achimala/dream-loop/blob/9bddb901f7d071cfefdd21e264267c757177a9df/README.md"
    title: "dream-loop"
  - id: "dream-loop:pro-workflow"
    resource: "https://github.com/achimala/dream-loop/blob/9bddb901f7d071cfefdd21e264267c757177a9df/references/pro-mode/workflow.md"
    title: "dream-loop Pro workflow"
  - id: "majidmanzarpour/threejs-game-skills"
    resource: "https://github.com/majidmanzarpour/threejs-game-skills/blob/8286774b22a2566bf894dbc825825c16921866af/README.md"
    title: "Three.js Game Skills"
  - id: "wheresryan22/anatomy"
    resource: "https://github.com/wheresryan22/anatomy/blob/1482e8469b0a9e0d8cc18ea2740a01423d29ae80/README.md"
    title: "anatomy"
  - id: "viettranx/3dviz-pro-max"
    resource: "https://github.com/viettranx/3dviz-pro-max/blob/d077e0e68915c25be8e71d74684d3144fd1c2aca/README.md"
    title: "3dviz-pro-max"
  - id: "agentskills:specification"
    resource: "https://agentskills.io/specification"
    title: "Agent Skills specification"
status: "stable"
year: "2026"
visual_sources:
  - path: "img/reviews/2026/video-3d-agent-skills/output-paths.svg"
    kind: "reviewer-diagram"
    source_url: "https://x.com/Y0urDumble/status/2119023461267833047"
    caption: "같은 제품 자료에서 시작하는 영상과 웹 도해의 제작 경로"
---

## 결과물부터 정하면 스킬이 보입니다

같은 제품을 소개하더라도 쇼츠에 올릴 **MP4**, 브라우저에서 돌려 볼 **제품 분해도**, 재질과 조명을 계속 손볼 **Blender 장면**은 서로 다른 결과물입니다. Dumble이 X에서 소개한 12개 프로젝트도 이 차이부터 보면 역할이 선명해집니다. HyperFrames는 영상을 렌더링하는 도구이고, GSAP Skills는 움직임을 코딩하는 방법을 알려주며, Blender MCP는 에이전트가 실행 중인 Blender를 조작할 통로를 엽니다. [목록을 소개한 X 게시물](https://x.com/Y0urDumble/status/2119023461267833047)

여기서 **에이전트 스킬**은 에이전트가 특정 작업을 할 때 읽는 재사용 가능한 지침입니다. 보통 `SKILL.md`에 언제 쓰는지와 작업 순서를 적고, 필요하면 예제와 보조 스크립트를 붙입니다. **렌더러**는 장면을 화면이나 영상으로 그리는 프로그램입니다. **MCP**는 에이전트가 앱의 기능을 도구로 호출하게 해주는 연결 규약입니다. 스킬이 카메라를 어디에 둘지 알려주면, MCP를 통해 Blender에서 실제 카메라를 옮길 수 있습니다. [Agent Skills 형식](https://agentskills.io/specification) · [Blender MCP 구성](https://github.com/ahujasid/mcp-for-blender/blob/2e4b0bc294694b1570d76ed01be657c22e6d02a0/README.md)

아래 설명은 X 게시물에서 연결한 12개 저장소의 README와 관련 스킬 문서를 2026년 11월 9일 기준으로 읽어 정리했습니다. 사례는 각 도구의 쓰임새를 보여주기 위한 예시입니다.

| 필요한 결과 | 출발점 | 고르는 기준 |
| --- | --- | --- |
| 코드로 고칠 수 있는 MP4 | HyperFrames, Remotion Skills | HTML과 CSS를 살릴지, React와 프레임 단위 구성 요소를 재사용할지 |
| 기획부터 편집까지 이어지는 제작 과정 | OpenMontage, video-shotcraft, motionmaxxing | 전체 제작을 관리할지, 제품 홍보 컷을 만들지, 화면 연출과 검수 규칙을 적용할지 |
| 화면 요소의 움직임 | GSAP Skills | 등장 순서, 속도 변화, 스크롤과 연동할 타이밍이 필요한지 |
| 수정 가능한 Blender 장면 | Blender MCP, blender-skills, dream-loop | 장면을 직접 조작할지, 제작 공정을 나눌지, 목표 이미지에 가까워지도록 반복할지 |
| 브라우저에서 직접 탐색하는 3D | threejs-game-skills, anatomy, 3dviz-pro-max | 플레이가 필요한지, 구조 설명이 중요한지, 자유롭게 탐색할 장면이 필요한지 |

## 영상 제작

### 1. HyperFrames — HTML과 CSS로 만든 장면을 MP4로

제목, 이미지, 영상과 오디오를 HTML에 배치하고 각 요소가 나타날 시간과 트랙을 지정합니다. 예를 들어 제품명은 1초 뒤에 나타나고, 그 아래로 제품 화면이 올라오게 할 수 있습니다. GSAP 같은 라이브러리로 움직임을 붙이면 헤드리스 Chrome이 지정된 시점의 화면을 그려 프레임을 만들고, FFmpeg가 이를 영상으로 인코딩합니다. 웹에서 만든 레이아웃이나 효과를 영상에도 활용할 때 어울립니다. [HyperFrames README](https://github.com/heygen-com/hyperframes/blob/327e20208c3f542841de670cce54754473f58d30/README.md)

X에서 강조한 `/reverse-any-video`는 **HyperFrames Pro 기능**입니다. 원본의 컷과 프레임을 측정하고, 텍스트나 자막 같은 요소는 HTML로 다시 만들며, 일부 이미지와 클립은 원본에서 잘라 배치합니다. 문서에는 화면 속 인물을 HeyGen으로 다시 만드는 단계도 있습니다. 결과는 원본 프레임과 비교해 수정할 수 있는 **재구성 프로젝트**입니다. 예컨대 원본 글꼴을 확보하지 못하면 대체 글꼴을 사용하고 그 차이를 기록합니다. 입력에는 사용 권한이 있는 영상을 전제로 합니다. [reverse-any-video 스킬 문서](https://github.com/heygen-com/hyperframes/blob/327e20208c3f542841de670cce54754473f58d30/skills/reverse-any-video/SKILL.md)

### 2. Remotion Skills — React 구성 요소를 영상에 재사용하기

Remotion의 공식 스킬 모음입니다. React 컴포넌트로 장면을 만들고 현재 프레임에 따라 요소의 위치, 크기, 투명도를 계산하는 방법을 알려줍니다. 제작 스킬은 프로젝트나 장면을 만들고, 마크업 스킬은 레이아웃과 타이밍을 다루며, Studio 스킬은 미리보기, 렌더 스킬은 영상과 스틸 이미지 출력을 맡습니다. 자막이나 지도 애니메이션처럼 작업별 지침도 있습니다. [Remotion Agent Skills](https://github.com/remotion-dev/skills/blob/a2824c67f8b4585c294a8101db9f9f0ad3c643f8/README.md)

예를 들어 매주 바뀌는 지표를 영상으로 내보낸다면 차트와 자막을 React 컴포넌트로 만들어 두고 데이터만 바꿔 같은 장면을 렌더링할 수 있습니다. 스킬은 에이전트에게 작성법을 알려주고, 실제 영상 파일은 Remotion이 렌더링합니다. [Remotion 마크업·렌더 안내](https://github.com/remotion-dev/skills/blob/a2824c67f8b4585c294a8101db9f9f0ad3c643f8/README.md)

### 3. OpenMontage — 조사부터 편집까지 이어지는 제작 과정

영상 유형별로 제작 단계를 정의한 프로젝트입니다. 예를 들어 다큐멘터리 몽타주나 화면 데모를 고르면 조사, 제안, 대본, 장면 계획, 소재 준비, 편집, 합성으로 진행합니다. YAML 파일에 단계와 검사 조건이 있고, 단계별 Markdown 지침을 읽은 에이전트가 Python 도구를 호출합니다. 진행 상태를 JSON으로 남기며, 장면별 스토리보드에서 소재를 승인한 뒤 제작을 이어갈 수 있습니다. [OpenMontage README](https://github.com/OpenMontageInc/OpenMontage/blob/356b5fa92474998c9f9a0782fd5547d05837d284/README.md)

긴 인터뷰에서 짧은 클립을 뽑는 일과 자료 화면을 모아 해설 영상을 만드는 일은 준비 과정부터 다릅니다. OpenMontage는 이런 차이를 제작 흐름에 반영합니다. 결과를 합성할 때는 프로젝트에 맞는 렌더 경로를 사용하며, 선택한 이미지·영상 생성 기능에 따라 외부 서비스 키와 비용이 필요할 수 있습니다. [OpenMontage 파이프라인과 제공자](https://github.com/OpenMontageInc/OpenMontage/blob/356b5fa92474998c9f9a0782fd5547d05837d284/README.md)

## 모션 디자인

### 4. GSAP Skills — 언제 움직이고 어떻게 멈출지 정하기

GSAP 공식 스킬 모음입니다. **타임라인**은 움직임 여러 개를 한 시간축에 배치합니다. **이징**은 같은 거리를 움직이더라도 처음에 빠르고 끝에서 천천히 멈추는 식으로 속도 변화를 지정합니다. 예를 들어 헤드라인이 멈추기 직전에 제품 카드가 나타나게 두 동작을 겹치거나, ScrollTrigger를 써서 스크롤 위치에 따라 장면을 진행할 수 있습니다. 웹 모션에 쓸 수 있고, HyperFrames처럼 시점을 지정해 화면을 캡처하는 영상 도구에도 GSAP 타임라인을 넣을 수 있습니다. [GSAP Skills](https://github.com/greensock/gsap-skills/blob/aed9cfd3277740755f6bfc1155c7aa645403b760/README.md) · [HyperFrames의 타임라인 예제](https://github.com/heygen-com/hyperframes/blob/327e20208c3f542841de670cce54754473f58d30/README.md#how-it-works)

### 5. video-shotcraft — 제품 화면을 홍보 영상의 컷으로 구성하기

실제 제품 페이지의 캡처와 문구를 받아 쇼트 레시피로 장면을 구성하는 Remotion 기반 스킬입니다. README는 124개 쇼트 레시피 카드를 소개합니다. 예를 들어 제품 화면 전체를 띄우는 대신, 사용자가 클릭하는 버튼에 카메라를 가까이 가져가고, 화면이 바뀌는 순간에 음악의 박자를 맞출 수 있습니다. 페이지 캡처, 스토리보드, 사운드, 프레임 점검을 한 제작 흐름에 넣습니다. [video-shotcraft README](https://github.com/Vincentwei1021/video-shotcraft/blob/1266a3ec4831289c4d893d42dd5102723658039a/README.md)

결과물은 MP4와 편집 가능한 Remotion 소스입니다. Motion Workbench에서는 컷, 자막, 전환, 효과음 트랙을 보면서 문구나 타이밍을 수정할 수 있고, 선택 사항으로 JianYing 편집 프로젝트를 내보낼 수 있습니다. 실제 UI가 영상에서 어떤 크기로 읽히는지가 중요한 제품 데모에 잘 맞습니다. [Motion Workbench와 출력 형식](https://github.com/Vincentwei1021/video-shotcraft/blob/1266a3ec4831289c4d893d42dd5102723658039a/README.md#motion-workbench)

### 6. motionmaxxing — 화면마다 무엇을 보여줄지 정하고 검수하기

제품을 소개할 때 무엇을 먼저 보여주고 어떤 컷으로 그 주장을 뒷받침할지 정하는 모션 디자인 스킬입니다. 브랜드 자료와 스토리보드를 만들고, 구현이 가장 까다로운 장면부터 시험한 뒤, 렌더와 스틸 이미지를 비교해 수정합니다. 예를 들어 기능을 보여주는 UI 글씨가 읽히는지, 프레임마다 시선이 향할 대상이 하나인지, 빈 화면이 이어지거나 마지막 카드가 너무 오래 머무는지를 봅니다. 빈 프레임 같은 항목은 스크립트로 확인하고, 읽기 쉬운지와 시선이 모이는지는 캡처를 보고 판단합니다. [motionmaxxing 프로토콜과 검수 기준](https://github.com/Tejashmakwana/motionmaxxing/blob/8c8ec0f2a6f6c9a0da15cd24f7b1298ab298368c/README.md)

편집 가능한 HTML, MP4, 스토리보드와 검수 기록을 남깁니다. video-shotcraft가 제품 캡처를 어떤 **컷 레시피**에 담을지 도와준다면, motionmaxxing은 화면이 메시지를 전달하는지 판단하는 **연출과 검수 절차**에 초점을 둡니다. [motionmaxxing 출력 형식](https://github.com/Tejashmakwana/motionmaxxing/blob/8c8ec0f2a6f6c9a0da15cd24f7b1298ab298368c/README.md#start-maxxing) · [video-shotcraft 제작 흐름](https://github.com/Vincentwei1021/video-shotcraft/blob/1266a3ec4831289c4d893d42dd5102723658039a/README.md)

## Blender 제작

### 7. Blender MCP — 에이전트에서 Blender로 작업을 보내기

Blender 애드온과 MCP 서버를 묶은 커뮤니티 프로젝트입니다. 에이전트가 MCP 서버에 도구 호출을 보내면, 서버가 소켓으로 Blender 애드온에 명령을 전달합니다. 이를 통해 오브젝트를 만들고 수정하거나, 재질을 입히고, 카메라 시점과 렌더를 확인할 수 있습니다. 예를 들어 제품 모델의 색을 바꾸고 세 방향에서 찍은 화면을 비교하는 일을 요청할 수 있습니다. Blender에서 Python 코드를 실행하는 기능도 제공하며, README는 파일·네트워크 등에 접근하는 스크립트를 검사하는 별도의 안전 모드를 설명합니다. [Blender MCP 구성과 안전 모드](https://github.com/ahujasid/mcp-for-blender/blob/2e4b0bc294694b1570d76ed01be657c22e6d02a0/README.md)

### 8. blender-skills — 모델링부터 게임 엔진 내보내기까지 작업 나누기

블록아웃은 디테일을 넣기 전에 단순한 도형으로 크기와 배치를 잡는 단계입니다. `blender-skills`는 이 단계에서 시작해 모델링, UV 작업, 재질, 조명, 애니메이션, 최적화, 내보내기까지 전문 지침을 나눕니다. README에 소개된 94개 스킬 중에서 `blender-director`가 작업에 맞는 지침을 이어 붙이는 예제가 있습니다. 게임 소품이라면 단단한 표면 모델링, 텍스처를 배치할 UV 작업, 재질, 에셋 최적화, 내보내기 순으로 구성할 수 있습니다. [blender-skills의 역할과 제작 예제](https://github.com/arjun988/blender-skills/blob/904f095d8f36a6e72adaebb08d07f884a074743d/README.md)

두 Blender 프로젝트는 함께 쓸 수 있습니다. blender-skills가 **어떤 순서로 작업할지**를 안내하고, 연결된 Blender MCP가 **장면에 그 작업을 적용할 방법**을 제공합니다. [blender-skills의 MCP 구성](https://github.com/arjun988/blender-skills/blob/904f095d8f36a6e72adaebb08d07f884a074743d/README.md#blender-mcp)

### 9. dream-loop — 목표 이미지와 실제 화면을 비교하며 개선하기

목표 스크린샷을 먼저 정하고, 구현한 화면을 캡처해 목표와 대조하는 스킬입니다. 목표는 사용자가 제공하거나 이미지 생성 도구로 만들 수 있습니다. 예를 들어 반사되는 돌바닥과 낮은 카메라 시점이 중요한 장면을 만든다면, 별도 평가 에이전트가 목표 이미지와 실제 화면을 보고 바닥의 반사, 조명의 방향, 카메라 높이처럼 구체적으로 다른 점을 찾아 다음 수정에 반영합니다. 문서에는 정해진 횟수만큼 반복하는 흐름과 평가 점수·성능 조건을 함께 보는 흐름이 있습니다. Blender는 직접 모델링할 때 쓸 수 있고, 저자가 공개한 예시는 브라우저에서 동작하는 Three.js 장면입니다. [dream-loop README](https://github.com/achimala/dream-loop/blob/9bddb901f7d071cfefdd21e264267c757177a9df/README.md) · [점수 기반 종료 조건](https://github.com/achimala/dream-loop/blob/9bddb901f7d071cfefdd21e264267c757177a9df/references/pro-mode/workflow.md)

## 브라우저 3D

### 10. threejs-game-skills — 화면에서 실제로 조작하고 플레이하는 게임 만들기

브라우저에서 3D를 그리는 Three.js를 바탕으로 게임을 제작할 때 쓰는 스킬 묶음입니다. 게임 전체를 계획하는 디렉터 외에 입력·카메라·물리·점수를 다루는 스킬, 게임 UI와 터치 조작을 설계하는 스킬, 프레임 속도와 로딩 문제를 확인하는 스킬 등이 있습니다. 예를 들어 자동차가 멋지게 보이는 장면에 더해 방향키로 조작하고 체크포인트를 통과하며 모바일에서도 터치 입력이 되는지 확인해야 할 때 쓸 수 있습니다. 프로젝트는 브라우저 실행, 화면 캡처, 입력과 성능 점검 같은 증거를 남기도록 안내합니다. [Three.js Game Skills 역할과 확인 항목](https://github.com/majidmanzarpour/threejs-game-skills/blob/8286774b22a2566bf894dbc825825c16921866af/README.md)

### 11. anatomy — 기계 부품의 구조를 설명하는 분해도 그리기

기계나 장치의 부품이 어떤 순서로 조립되고 서로 어떻게 움직이는지 보여주는 도해 스킬입니다. 사선에서 보는 **등각 투영**으로 SVG를 그리며, 부품을 벌려 놓는 분해도나 움직이는 계기판을 만들 수 있습니다. 엔진 배기나 물결처럼 선과 면으로 표현하기 어려운 부분에는 WebGL 효과를 더할 수 있습니다. 예를 들어 펌프를 설명할 때 하우징, 축, 임펠러의 위치를 서로 떨어뜨려 보여주고, 회전 방향을 움직임으로 표시할 수 있습니다. 실제 치수와 부품 목록을 먼저 확인하고, 도형의 겹침과 접합을 검사하는 절차가 포함됩니다. 자유롭게 돌려 보는 3D 모드는 문서상 베타입니다. [anatomy의 출력 방식과 검사 도구](https://github.com/wheresryan22/anatomy/blob/1482e8469b0a9e0d8cc18ea2740a01423d29ae80/README.md)

### 12. 3dviz-pro-max — 아이디어를 탐색 가능한 3D 장면으로 발전시키기

장면의 분위기와 형태, 물체의 연결과 움직임부터 정하고, 그에 맞는 3D 키트와 제작 방법을 선택하게 하는 스킬입니다. Three.js 템플릿, 카메라와 조명 설정, 재사용 가능한 에셋과 장면 예제가 들어 있습니다. 예를 들어 물레방아가 있는 작은 마을을 만든다면, 마을을 둘러보는 카메라와 밤의 조명을 만들고, 수차가 어느 쪽으로 도는지 브라우저에서 실제로 캡처해 확인합니다. Blender로 만든 에셋을 활용하는 경로도 있습니다. [3dviz-pro-max의 제작 흐름과 키트](https://github.com/viettranx/3dviz-pro-max/blob/d077e0e68915c25be8e71d74684d3144fd1c2aca/README.md)

조작 목표와 점수 규칙이 중요한 게임은 threejs-game-skills가, 기계의 부품 관계를 정확하게 설명하는 도해는 anatomy가 다룹니다. 3dviz-pro-max는 그보다 넓은 범위에서 장면을 설계하고, 직접 둘러봤을 때 의도한 화면과 동작이 나오는지 검사하는 데 초점을 둡니다. 키트와 레시피마다 실제 렌더로 확인된 범위가 다르며, 움직이는 과학 시각화에는 별도의 사실 근거가 필요합니다. [3dviz-pro-max의 검증 범위](https://github.com/viettranx/3dviz-pro-max/blob/d077e0e68915c25be8e71d74684d3144fd1c2aca/README.md#honest-limits)

## 같은 제품을 영상과 웹으로 보여준다면

커피 머신의 펌프를 소개한다고 가정해 보겠습니다. **30초짜리 고정 영상**에는 Blender에서 만든 펌프 렌더를 소재로 쓰고, HyperFrames나 Remotion에서 자막과 타이밍을 붙여 MP4로 내보낼 수 있습니다. **웹 제품 설명서**에는 anatomy로 펌프의 구조를 설명하고, 사용자가 장면을 직접 돌아보는 경험이 필요하면 Three.js 장면을 만들 수 있습니다. 두 결과물 모두 같은 제품 자료에서 시작하지만 영상에서는 컷마다 무엇이 보이는지, 웹에서는 사용자가 무엇을 조작하고 확인할 수 있는지가 제작 방식을 가릅니다. [HyperFrames](https://github.com/heygen-com/hyperframes/blob/327e20208c3f542841de670cce54754473f58d30/README.md) · [Remotion](https://github.com/remotion-dev/skills/blob/a2824c67f8b4585c294a8101db9f9f0ad3c643f8/README.md) · [anatomy](https://github.com/wheresryan22/anatomy/blob/1482e8469b0a9e0d8cc18ea2740a01423d29ae80/README.md) · [3dviz-pro-max](https://github.com/viettranx/3dviz-pro-max/blob/d077e0e68915c25be8e71d74684d3144fd1c2aca/README.md)

![제품 자료에서 MP4를 만드는 영상 경로와 분해도나 3D 장면을 만드는 웹 경로]({{ '/img/reviews/2026/video-3d-agent-skills/output-paths.svg' | relative_url }})

*그림 1. 같은 제품 자료를 영상과 웹으로 설명하는 두 제작 경로를 정리한 도식입니다.*
