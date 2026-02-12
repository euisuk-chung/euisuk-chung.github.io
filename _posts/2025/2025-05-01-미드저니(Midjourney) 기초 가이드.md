---
title: "미드저니(Midjourney) 기초 가이드"
date: "2025-05-01"
tags:
  - "MidJourney"
year: "2025"
---

# 미드저니(Midjourney) 기초 가이드

원본 게시글: https://velog.io/@euisuk-chung/미드저니Midjourney-기초-가이드



![](https://velog.velcdn.com/images/euisuk-chung/post/227cf000-f55c-401f-b1a8-8995877b7f3b/image.png)

> <https://docs.midjourney.com/hc/en-us/articles/33329261836941-Getting-Started-Guide>

*본 블로그 포스트는 midjourney documentation을 바탕으로 작성되었습니다.*

1. 들어가며: 창작의 시대, 미드저니로 시작하세요
----------------------------

AI 이미지 생성이 더 이상 미래의 기술이 아닙니다. **미드저니(Midjourney)**는 누구나 쉽게 텍스트만으로 고품질의 이미지를 생성할 수 있는 AI 도구로, 디자이너부터 마케터, 그리고 일반 사용자까지 폭넓게 사용되고 있습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/06e58958-a1f9-453e-8f54-2000a6bd1e0e/image.png)

> <https://www.midjourney.com/explore>

이번 글에서는 Midjourney의 시작 가이드를 바탕으로 기본 사용법과 주요 기능들을 소개하고, 여러분이 직접 이미지 생성 프로젝트를 시작할 수 있도록 도와드리겠습니다.

---

2. Midjourney란 무엇인가요?
---------------------

Midjourney는 `Discord` 또는 `Web` 기반의 **AI 이미지 생성 플랫폼**입니다.

* 사용자는 텍스트 프롬프트(prompt)를 입력하면, 해당 내용을 바탕으로 AI가 이미지를 생성해 줍니다.
* GPT가 텍스트를 생성하는 것처럼, Midjourney는 **텍스트를 시각적 예술로 바꾸는 도구**입니다.

---

3. 시작 전 준비사항
------------

Midjourney를 사용하기 위해서는 아래 준비가 필요합니다:

![](https://velog.velcdn.com/images/euisuk-chung/post/a0ffcb16-cc0b-4478-9227-6696cb17db8d/image.png)

> <https://www.midjourney.com/home>

* **계정**:
  
  + Midjourney는 `Discord` 또는 `Google` 계정이 있으시면 사용하실 수 있습니다.
* **Midjourney 가입**:
  
  + <https://www.midjourney.com>에서 회원 가입 후 사용하실 수 있습니다.
* **구독 요금제 선택**:
  
  + 무료 체험은 종료되었기 때문에, 사용을 원하시면 유료 플랜 중 하나를 선택해야 합니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/99e2582f-6870-40a6-8234-e8f3a40989bc/image.png)

> <https://www.midjourney.com/account>

---

4. Midjourney 웹에서 이미지 만들기: 프롬프트부터 생성까지 한눈에
------------------------------------------

Midjourney는 **midjourney.com 웹사이트에서 더 직관적이고 편리하게** 사용할 수 있습니다.  

(*저는 web interface에 더 익숙하기 때문에 web기준으로 설명드리겠습니다.*)

웹 인터페이스에서는 프롬프트 입력, 이미지 생성, 편집, 정리까지 전 과정을 마우스 클릭 몇 번으로 처리할 수 있습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/6e5e9497-639f-48d7-8f9c-9deafc82147e/image.png)

---

### ✨ 4.1 Create 페이지: 상상력을 이미지로 바꾸는 중심지

**[Create 페이지](https://www.midjourney.com/create)**는 사용자가 이미지를 직접 생성하는 공간입니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/9692f1bc-a02f-42be-9e5d-fed53e1cc3f3/image.png)

텍스트 프롬프트를 입력하면 AI가 실시간으로 이미지를 만들어내며, 모든 결과는 화면 아래 **Creation Feed**에 바로 나타납니다.

* 상단의 **Imagine 바**에 텍스트를 입력하면 이미지 생성 시작  
  
  ![](https://velog.velcdn.com/images/euisuk-chung/post/496af9f2-c525-4696-bc37-cdad605f2626/image.png)
* 프롬프트 끝에 다양한 파라미터도 입력 가능 (`--v 7`, `--ar 16:9` 등)
  
  + 프롬프트 및 파라미터는 뒤에 6챕터에서 정리합니다.
* 이미지를 업로드해서 스타일이나 캐릭터 레퍼런스로 활용 가능  
  
  ![](https://velog.velcdn.com/images/euisuk-chung/post/3eaab6e2-452e-4266-8a9d-3bc5493b4a3d/image.png)
* 이전 프롬프트 검색이 가능합니다.  
  
  ![](https://velog.velcdn.com/images/euisuk-chung/post/ab9aa0fe-b498-4afd-906e-6d92f15aefcd/image.png)

---

### 🧰 4.2 Imagine 바 기능 요약

| 아이콘 | 기능 |
| --- | --- |
| 🖼️ 이미지 추가 | 이미지 프롬프트 또는 스타일/캐릭터 참조용 업로드 |
| ⚙️ 설정 변경 | 기본 버전, 비율, 스타일, Draft Mode 등 설정 |
| 🧬 개인화 | Personalization 프로필 관리 (V7 활성화 포함) |
| 🧪 Draft Mode | GPU 절반만 사용하여 빠른 시안 생성 (저화질 생성) |
| 🔍 검색창 | 이전에 썼던 프롬프트를 빠르게 다시 찾기 |

> 💡 **Ctrl (또는 Cmd) + Enter**: 텍스트를 유지한 채 이미지만 다시 생성

---

### 🖼️ 4.3 생성된 이미지 관리: Creation Actions 완전 정복

Midjourney 웹사이트에서 이미지를 생성한 후, 다양한 편집과 확장 작업을 수행할 수 있는 핵심 도구가 바로 **Creation Actions**입니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/2db86ff7-e26a-482c-8a80-e165f0f41143/image.png)

이 메뉴를 통해 한 번 만든 이미지를 **다시 변형하거나 확대**, **프롬프트를 수정하거나 스타일을 확장**할 수 있습니다.

아래는 각 버튼에 대한 기능 설명입니다:

---

🔁 **Vary (Subtle / Strong)**

기존 이미지의 분위기를 유지하면서 새 버전을 생성합니다.

* **Subtle**: 세부 요소만 살짝 변경 (색감, 조명 등)
* **Strong**: 더 큰 변화 포함 (포즈, 배경, 구조까지 변경 가능)

> 🔍 원본이 마음에 들지만 여러 버전을 실험하고 싶을 때 유용합니다.

---

🖼️ **Upscale (Subtle / Creative)**

이미지를 고해상도로 업스케일합니다. 기본 크기의 약 2배 크기로 확대되며, 다운로드용으로 적합해집니다.

* **Subtle**: 원본 스타일 그대로 유지하며 선명도만 향상
* **Creative**: 디테일을 추가하거나 표현을 개선하며 다소 변형될 수 있음

> 💡 손 모양 보정, 질감 강화에 유용한 방식입니다.

---

🎨 **Remix (Subtle / Strong)**

프롬프트 또는 파라미터를 수정하여 새로운 변형 이미지를 생성할 수 있습니다.

* **Subtle**: 원본 스타일 유지, 내용만 약간 변경
* **Strong**: 프롬프트 수정 + 이미지 구조도 좀 더 과감하게 변화

> 🧪 이미지 주제를 유지한 채 분위기, 배경, 스타일을 바꾸고 싶을 때 사용하세요.

---

⬅️➡️⬆️⬇️ **Pan (좌/우/상/하)**

이미지의 경계를 확장해 새로운 장면을 만들어냅니다.

* 기존 이미지를 중심에 두고 선택한 방향으로 **배경/장면이 이어짐**
* 사방으로 확장해 **파노라마**, **넓은 세계관**, **스토리텔링 이미지** 제작 가능

> 🖼️ 원본을 망치지 않고 자연스럽게 확장할 수 있어 매우 인기 많은 기능입니다.

---

🔍 **Zoom (1.5x / 2x)**

이미지를 확대하면서 새로운 캔버스를 생성합니다.

* **1.5x / 2x** 확대 비율 선택 가능
* 확대하면서 주변 빈 영역은 AI가 **자연스럽게 채워줍니다**

> 🌌 주요 대상에 더 집중된 장면을 만들거나, "점점 가까이 다가가는" 연출에 적합합니다.

---

🔁 **More → Rerun**

같은 프롬프트와 설정으로 이미지를 **다시 생성**합니다.

* 랜덤 요소가 포함되므로 매번 다른 결과가 나올 수 있음

> 🎲 동일한 주제의 여러 샷이 필요할 때 간편하게 사용 가능합니다.

---

✏️ **More → Edit**

이미지를 **Editor**에 불러와 **프롬프트, 스타일, 비율 등을 동시에 수정**할 수 있습니다.

* Pan, Zoom, Remix, Vary Region 등 복합 작업 가능
* 이미지 캔버스를 직접 드래그하거나 레이아웃 조절도 가능

> 🧰 하나의 화면에서 다양한 편집을 할 수 있는 **고급 사용자용 도구**입니다.

---

➕ **Use (Image / Style / Prompt)**

기존 이미지를 새로운 창작에 재활용할 수 있습니다.

* **Image**: 해당 이미지를 이미지 프롬프트로 사용
* **Style**: 스타일 참조용으로 사용 (색감, 분위기 등)
* **Prompt**: 기존 프롬프트 텍스트를 재사용하여 새로운 이미지 생성

> ♻️ 기존 작품을 기반으로 시리즈 작업하거나 빠르게 재활용하고 싶을 때 유용합니다.

---

**(요약) 어떤 기능을 언제 써야 할까?**

| 목적 | 추천 기능 |
| --- | --- |
| 살짝만 다른 버전 만들기 | Vary → Subtle |
| 더 과감한 변형 실험 | Vary / Remix → Strong |
| 해상도 업 / 디테일 향상 | Upscale (Subtle or Creative) |
| 배경 확장하고 싶을 때 | Pan (좌우상하 방향) |
| 가까이 확대하며 리프레임 | Zoom 1.5x / 2x |
| 똑같은 프롬프트로 재생성 | Rerun |
| 기존 이미지 기반으로 재창작 | Use (Image / Style / Prompt) |
| 프롬프트 & 캔버스 자유 편집 | Edit (Editor 진입) |

---

5. 주요 기능: 만들고, 편집하고, 정리하기
-------------------------

Midjourney 웹사이트는 이미지 생성 외에도 **강력한 후처리 및 정리 기능**을 제공합니다.

아래는 웹 주요 메뉴에 따른 핵심 기능입니다:

---

### 🧠 5.1 Edit 페이지: 이미지를 다시 편집하고 재활용하기

**[Edit 페이지](https://www.midjourney.com/edit)**에서는 업로드한 이미지나 생성된 이미지를 다시 열어 **AI 기반 편집 기능**을 사용할 수 있습니다.

* 특정 영역만 바꾸는 Inpainting 기능
* 원본 프롬프트를 일부 수정해 새로운 이미지 만들기
* 다른 이미지와 스타일 결합도 가능

---

### 🖼️ 5.2 Organize 페이지: 내 작품을 정리하는 공간

**[Organize 페이지](https://www.midjourney.com/organize)**는 내 모든 이미지를 **날짜별, 폴더별, 필터별**로 쉽게 정리할 수 있도록 도와줍니다.

* **Timeline Bar**로 특정 날짜에 생성한 이미지 찾기
* **폴더 그룹**을 만들어 테마별로 묶기
* 여러 이미지를 한 번에 숨기기, 삭제하기, 좋아요 설정 가능

---

### 🧩 5.3 Personalize 페이지: 나만의 스타일 만들기

**[Personalize 페이지](https://www.midjourney.com/personalize)**에서는 **개인화 프로필**과 **무드보드(moodboard)**를 관리할 수 있습니다.

* **V7 모델 사용 시 필수**: 이미지 쌍을 평가해 V7 Personalization 프로필 해제
* 무드보드를 통해 "나는 이런 스타일을 좋아해!"를 AI에게 학습시키기
* 여러 스타일 프로필을 만들어 작업별로 다르게 적용 가능

---

### 🗂️ 5.4 폴더별 작업 공간

Create 페이지 상단의 📁 버튼을 클릭하면 내 폴더들이 나타납니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/8aacf3fb-0e0e-4bc3-b673-a68da3745fa1/image.png)

> 폴더가 없으면 다음과 같이 나오며, New Folder를 통해 생성할 수 있습니다.

폴더 안에서만 이미지를 생성하면 그 폴더에 자동 정리되므로 **작업별로 관리하기 아주 편리**합니다.

---

### 💬 5.5 Chat: 실시간 소통 공간

**Chat**는 Midjourney 웹에서 제공하는 채팅 기반 공동 창작 공간입니다.

* Daily Theme, Prompt Craft, Help 같은 공개 룸에 참여
* 채팅하면서 바로 프롬프트 공유 및 이미지 생성 가능
* 음성 채팅도 지원되어 협업이 더 쉬워집니다

---

### 🧪 5.6 Tasks: 보상도 얻고 V7도 활성화!

**Tasks 페이지**에서는 이미지 쌍 평가, 프롬프트 피드백 등 작은 활동을 통해:

* **V7 Personalization 활성화**
* **보너스 GPU 시간 획득**
* 커뮤니티 퀄리티 향상에 기여

![](https://velog.velcdn.com/images/euisuk-chung/post/27bb4ed1-307d-496c-a58e-1daa77e06469/image.png)

> <https://www.midjourney.com/tasks>

---

6. 프롬프트 작성 팁: 멋진 이미지를 위한 한 줄의 마법
--------------------------------

AI에게 무엇을 만들어야 할지 잘 전달하는 것이 **이미지 품질의 핵심**입니다.

Midjourney에서 강력한 결과물을 얻기 위해서는 텍스트 프롬프트와 다양한 파라미터, 그리고 멀티 프롬프트 구문을 잘 활용하는 것이 중요합니다.

---

### ✏️ 6.1 기본 프롬프트 작성 전략

먼저, 텍스트 프롬프트에는 **상상력과 디테일을 담는 것**이 중요합니다.

아래 요소들을 함께 고려해보세요:

* **스타일**: `digital painting`, `photorealistic`, `watercolor`, `pixel art`
* **소재와 분위기**: `glowing`, `gritty`, `foggy`, `bioluminescent`, `epic lighting`
* **배경과 장소**: `space station`, `enchanted forest`, `underwater ruins`
* **구도와 시점**: `close-up`, `top-down view`, `isometric`, `wide shot`
* **시대/장르**: `cyberpunk`, `medieval`, `steampunk`, `anime`, `futuristic`

> **예시**:
> 
> ```
> a cozy cafe in Tokyo, rainy night, cinematic lighting, anime style --v 7 --ar 16:9
> ```

---

### ⚙️ 6.2 필수 파라미터 요약: 이미지 퀄리티와 스타일 제어하기

Midjourney는 프롬프트 뒤에 다양한 **파라미터(Parameter)**를 붙여 이미지 스타일과 구조를 세밀하게 제어할 수 있습니다.

#### 🔧 자주 쓰이는 파라미터

| 파라미터 | 설명 |
| --- | --- |
| `--ar` 또는 `--aspect` | 가로세로 비율 설정 (예: `--ar 16:9`) |
| `--v` 또는 `--version` | 버전 선택 (예: `--v 7`) |
| `--style raw` | 현실적인 결과물 생성 |
| `--q` 또는 `--quality` | 이미지 품질 (0.25, 0.5, 1, 2) |
| `--chaos` | 결과물의 다양성 증가 (0~100) |
| `--stop` | 이미지 생성을 중간에 멈춰 부드러운 스타일 유도 |
| `--no` | 특정 요소 제외 (예: `--no text`) |
| `--seed` | 동일 결과 재현을 위한 고유 번호 지정 |
| `--tile` | 반복 가능한 타일 패턴 생성 |
| `--raw` | 스타일 자동 보정 없이 입력값 그대로 해석 |
| `--relax`, `--fast`, `--turbo` | GPU 속도 설정 |
| `--niji` | 애니메이션/동양풍 특화 모델 사용 |
| `--sref`, `--cref` | 이미지 기반 스타일/캐릭터 일관성 유지 |
| `--iw` | 이미지 프롬프트의 영향력 조정 (Image Weight) |

예시:

```
a futuristic samurai with glowing armor, standing in a neon-lit alley --v 7 --style raw --ar 2:3 --q 2
```
> 📝 **사용 팁**:
> 
> * 모든 파라미터는 **프롬프트 맨 끝에**, **띄어쓰기 포함**해서 넣어야 합니다.
> * 파라미터 내에는 쉼표나 마침표 같은 **문장부호를 사용하지 마세요**.

---

### 🧠 6.3 멀티 프롬프트(Multi-Prompts): 창의력의 콜라주

**멀티 프롬프트(Multi-Prompts)**는 서로 다른 아이디어를 결합해 **더 창의적인 결과물**을 만들어낼 수 있는 기능입니다.

* `::` 기호를 이용해 각 요소를 분리하면, Midjourney가 각각을 독립적으로 해석 후 조합해 이미지를 생성합니다.

> **예시**:
> 
> ```
> forest:: crystal cave:: glowing wolves --v 6.1
> ```

![](https://velog.velcdn.com/images/euisuk-chung/post/f4ce6f8e-c1db-47bf-9920-8bce424c8652/image.png)

> * 📌 **왼쪽은 공백 없이**, 오른쪽은 한 칸 공백을 넣는 것이 규칙입니다.
> * 📌 **version 7**은 현재 지원하지 않습니다.

---

### ⚖️ 6.4 프롬프트 가중치(Prompt Weights): 중요도 조절

멀티 프롬프트에 **숫자를 붙여 각 요소의 중요도**를 조정할 수 있습니다.

> **예시**:
> 
> ```
> space::2 ship::1 --v 6.1
> ```

![](https://velog.velcdn.com/images/euisuk-chung/post/d65ff958-ba17-4c48-8490-6fa8996ca9b8/image.png)

→ 우주는 강조되고, 배는 부가 요소로 표현됩니다.

> 기본값은 1이며, 일부 모델(버전 4 이상)은 소수점도 지원합니다.

---

### 🚫 6.5 네거티브 가중치 & `--no`

보고 싶지 않은 요소를 제외하려면 **음수 가중치**나 `--no` 파라미터를 사용하세요.

> **예시**:
> 
> ```
> still life painting:: fruit::-0.5
> ```

![](https://velog.velcdn.com/images/euisuk-chung/post/2e9752c6-df34-4d03-b021-50a21fbb97fb/image.png)

또는

> **예시**:
> 
> ```
> still life painting --no fruit
> ```

![](https://velog.velcdn.com/images/euisuk-chung/post/a297852e-2ffc-4e1e-972a-041a8932d4da/image.png)

→ 두 프롬프트는 동일한 효과를 가지며, 과일이 적거나 빠진 정물화를 유도합니다.

---

**🎯 최종 프롬프트 예시 모음**

```
a glowing deer in a misty forest at sunrise, photorealistic --v 7 --style raw --ar 3:2 --q 2

medieval battlefield::2 magical sky::1 --v 6.1 --chaos 40

anime girl in space armor --niji 6 --ar 9:16 --style raw

vibrant California poppies field --v 7 --ar 2:3 --no people
```

**🎯 프롬프트 설명**

> 1. "해 뜨는 이른 아침, 안개 자욱한 숲 속에 빛나는 사슴이 있는 사실적인 장면"
> 
> ```
> a glowing deer in a misty forest at sunrise, photorealistic --v 7 --style raw --ar 3:2 --q 2
> ```

**설명**:

* `glowing deer` → 몸에서 빛이 나는 환상적인 사슴
* `misty forest at sunrise` → 안개 낀 숲과 따스한 일출 분위기
* `photorealistic`, `--style raw`, `--q 2` → 매우 사실적이고 고퀄리티로 생성
* `--ar 3:2` → 일반적인 사진 비율로 출력
* `--v 7` → 최신 Midjourney V7 모델 사용

![](https://velog.velcdn.com/images/euisuk-chung/post/13ed566f-02e3-476d-96af-c31745635701/image.png)

🖼️ **결과**: 마치 야생 사진 작가가 찍은 듯한 아름답고 신비로운 장면

---

> 2. "중세 전장의 분위기를 강조하고, 마법 같은 하늘이 배경인 장면"
> 
> ```
> medieval battlefield::2 magical sky::1 --v 6.1 --chaos 40
> ```

**설명**:

* `::2` → "중세 전장"이 중심 주제
* `::1` → "마법 같은 하늘"은 보조적 요소
* `--v 6.1` → 안정적이고 사실적인 표현력의 기본 모델
* `--chaos 40` → 예상치 못한 창의적 구도와 스타일이 나올 확률 높음

![](https://velog.velcdn.com/images/euisuk-chung/post/fac09307-2892-44bf-863d-6f168bbb025e/image.png)

🖼️ **결과**: 혼돈스럽고 극적인 분위기의 판타지 일러스트

---

> 3. "우주 갑옷을 입은 애니메이션 스타일의 소녀, 세로 비율로 표현"
> 
> ```
> anime girl in space armor --niji 6 --ar 9:16 --style raw
> ```

**설명**:

* `anime girl in space armor` → 공상과학 테마의 전투복 차림 애니 여캐
* `--niji 6` → 애니메이션 전용 모델, 동양풍 일러스트 특화
* `--ar 9:16` → 모바일 배경화면에 어울리는 세로 비율
* `--style raw` → 부드러운 그림체보다는 더 사실적인 묘사

![](https://velog.velcdn.com/images/euisuk-chung/post/757bc4cc-f06c-4f87-b3b1-abb1528c2755/image.png)

🖼️ **결과**: 애니메이션 느낌이면서도 디테일이 살아있는 일러스트

---

> 4. "화려한 캘리포니아 양귀비 꽃밭, 사람은 없는 장면"
> 
> ```
> vibrant California poppies field --v 7 --ar 2:3 --no people
> ```

**설명**:

* `vibrant California poppies field` → 선명하고 생기 넘치는 양귀비 꽃밭
* `--v 7` → 최신 버전으로 섬세한 디테일 표현
* `--ar 2:3` → 자연 사진 비율
* `--no people` → 인물 없이 풍경만 생성되도록 설정

![](https://velog.velcdn.com/images/euisuk-chung/post/20708de9-04eb-4052-ab63-ac3cc9437fdc/image.png)

🖼️ **결과**: 자연의 아름다움을 강조한 깨끗한 풍경 이미지

---

7. Midjourney 버전(Versions) 완전 정복: V6부터 V7까지, 어떤 걸 써야 할까?
--------------------------------------------------------

> <https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version>

Midjourney는 지속적으로 새로운 모델 버전을 출시하며 이미지 품질과 창의성을 향상시켜 왔습니다.

각 버전은 단순한 업데이트가 아니라, **완전히 다른 스타일과 기능을 제공하는 이미지 생성 엔진**입니다.  

버전을 잘 이해하고 선택하면, 여러분의 결과물이 훨씬 더 만족스러워질 수 있습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/20d86243-4d93-480b-b483-d51c093fa25e/image.png)

> <https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version>

### 🎯 버전이란 무엇인가요?

버전(Versions)은 Midjourney가 발전해 온 **AI 모델의 세대**입니다.  

마치 게임 그래픽 엔진이 업그레이드되면 현실감이 높아지는 것처럼, Midjourney도 버전이 올라갈수록 **프롬프트 이해력**, **세부 묘사**, **스타일 정교함**이 향상됩니다.

> ✅ **최신! Version 7 (2025년 4월 출시)**

Midjourney의 최신 모델인 **V7**은 가장 발전된 이미지 품질과 프롬프트 해석 능력을 자랑합니다.

* **세부 묘사 강화**: 인물의 손가락, 얼굴 비율, 객체의 구조 등 디테일이 매우 정확합니다.
* **텍스처 표현 향상**: 금속, 천, 유리 같은 소재가 더욱 리얼하게 표현됩니다.
* **텍스트 프롬프트 정밀도**: 긴 문장이나 복잡한 묘사도 자연스럽게 해석합니다.
* **Draft Mode 지원**: 빠르게 다양한 콘셉트를 스케치 형태로 실험할 수 있습니다.
* **Omni Reference 지원**: 하나의 이미지로 스타일, 캐릭터, 구성 등을 동시에 참조 가능.

🛠 **주의**: 기본 모델이 아니라 수동으로 `--v 7`을 지정하거나 웹 설정에서 변경해야 합니다.  

또한, 사용 전 **V7 Personalization Profile**을 활성화해야 하며, 이는 이미지 쌍을 평가하는 간단한 과정을 통해 가능합니다.

```
/imagine prompt: cyberpunk samurai in rainy Tokyo, --v 7
```
> 🔹 **Version 6.1 (2024년 7월 출시 – 기본 모델)**

**V6.1**은 현재 Midjourney의 **기본 버전**이며, 안정성과 속도, 퀄리티 간 균형이 뛰어납니다.

* **이미지 생성 속도 약 25% 향상**
* **더욱 일관된 프롬프트 해석**
* **고급 업스케일러 지원 (Subtle / Creative)**
* **전반적인 스타일 균형 유지**: 현실적이면서도 예술적인 결과물

추천 사용 시점:

* **빠른 생성이 필요할 때**
* **정교한 제어보다는 자연스러운 결과가 필요할 때**

> 🔹 **Version 6 (2023년 12월 출시)**

**V6**는 긴 문장의 정확한 이해, 자연스러운 구도 생성에 강점을 가진 모델입니다.

* **롱 프롬프트에 강함**: 복잡한 문장 구조나 스토리텔링 프롬프트 처리 가능
* **Remix & Pan 기능 탑재**
* **다양한 파라미터와 호환**: `--chaos`, `--tile`, `--style`, `--raw` 등

V6은 현재는 잘 쓰이지 않지만, 특정 스타일이나 실험적 작업에 여전히 활용됩니다.

> 🎨 **Niji 6 – 애니메이션 & 일러스트 특화 모델**

**Niji 시리즈**는 Spellbrush와 협력하여 만든 **동양풍/애니메이션 스타일** 전용 버전입니다.  

**Niji 6**는 2024년 6월 출시되었으며:

* **일본어 텍스트 표현 가능 (히라가나, 간단한 한자)**
* **눈, 머리카락, 옷 등의 세밀한 표현 향상**
* **이전 버전에서 발생했던 일러스트 아티팩트 문제 개선**

```
/imagine prompt: anime girl in cherry blossom park, --niji 6
```

🧙 사용자는 [niji journey 사이트](https://niji.midjourney.com)와 전용 Discord에서 더 많은 기능을 활용할 수 있습니다.

### 📊 버전 기능 비교 요약

| 기능 | V6 | V6.1 (기본) | V7 (최신) | Niji 6 |
| --- | --- | --- | --- | --- |
| 프롬프트 해석 정확도 | 높음 | 더 높음 | 최고 수준 | 중간 (애니 특화) |
| 세부 묘사 | 우수 | 매우 우수 | 매우 정밀 | 눈, 옷 표현 특화 |
| 손/인체 표현 | 보통 | 좋아짐 | 매우 정확함 | 만화 스타일 중심 |
| 이미지 생성 속도 | 중간 | 빠름 | 중간 | 중간 |
| 특화 기능 | Remix, Long Prompt | 빠른 렌더링, 업스케일러 | Draft Mode, Omni Ref | 일본어 텍스트 처리 |
| 설정 방법 | `--v 6` | 기본값 | `--v 7` + 활성화 필요 | `--niji 6` |

### ⚙️ 버전 설정 방법 정리

1. **프롬프트에 직접 버전 지정**

* 예: `/imagine prompt: futuristic samurai --v 7`

2. **웹 UI에서 기본 버전 설정**

* 오른쪽 하단 ⚙️ 아이콘 클릭 → Settings → Default Version 선택

3. **V7 활성화 방법**

* Midjourney가 제시하는 이미지 쌍을 보고 마음에 드는 쪽을 선택 (Personalization)
* 이 과정을 통해 V7 Global Personalization Profile을 활성화할 수 있음

🧠 Tip: 어떤 버전을 선택해야 할까요?
-----------------------

| 상황 | 추천 버전 |
| --- | --- |
| 빠르고 안정적인 결과가 필요 | V6.1 |
| 최신 AI 기술로 극한의 퀄리티 | V7 |
| 동양풍, 애니메이션 스타일 | Niji 6 |
| 긴 문장, 실험적 구도 | V6 |

---

8. 커뮤니티 및 개인 채널 사용하기
--------------------

처음에는 Midjourney 공식 Discord 서버의 **Newbies** 채널에서 이미지 생성을 시작합니다.

유료 구독자는 **직접 메시지 채널(DM)**이나 **private room**에서 더 편하게 사용할 수 있습니다.

---

9. 실전 예제: 간단한 이미지 생성 프로젝트
-------------------------

간단한 Midjourney 프로젝트를 진행해보세요!

**실습 목표**:

* "미래형 스마트 시티 이미지 만들기"

**단계별 진행**:

1. 프롬프트: `futuristic smart city, flying cars, neon lights, --ar 16:9`

![](https://velog.velcdn.com/images/euisuk-chung/post/9b6b26f8-b84f-4ab8-8468-c1e1692e7602/image.png)

2. 생성된 이미지 중 마음에 드는 것 업스케일 `upscale`
3. 변형 이미지도 시도해 보기 `vary`

![](https://velog.velcdn.com/images/euisuk-chung/post/ef5f9982-3161-4ce6-8151-10390bcc965b/image.png)

4. 다운로드 및 포트폴리오에 활용

---

10. 마무리: 당신만의 상상력을 현실로
----------------------

Midjourney는 누구나 창작자가 될 수 있도록 돕는 강력한 AI 도구입니다.  

텍스트 한 줄로 시작해 예술 작품을 만들 수 있는 이 플랫폼을 활용해, 여러분만의 세상을 그려보세요.

더 깊이 있는 사용을 원하신다면:

* 미드저니 공식 가이드 탐색하기: [Midjourney Docs](https://docs.midjourney.com)
* 다양한 프롬프트 예시를 참고한 창작 연습
* 미드저니 갤러리에서 다른 유저의 작품 감상하기

읽어주셔서 감사합니다 :)

