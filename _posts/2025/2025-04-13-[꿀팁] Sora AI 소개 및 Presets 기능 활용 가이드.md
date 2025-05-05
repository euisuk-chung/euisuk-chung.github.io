---
title: "[꿀팁] Sora AI 소개 및 Presets 기능 활용 가이드"
date: "2025-04-13"
tags:
  - "OpenAI"
  - "sora"
year: "2025"
---

# [꿀팁] Sora AI 소개 및 Presets 기능 활용 가이드

원본 게시글: https://velog.io/@euisuk-chung/꿀팁-Sora-AI-소개-및-Presets-기능-활용-가이드



🎥 현실감 있는 AI 비디오를 만드는 생성형 모델, **Sora AI**
----------------------------------------

OpenAI가 개발한 **Sora AI**는 텍스트만으로 사실적이고 상상력 가득한 영상을 생성할 수 있는 **텍스트-투-비디오(Text-to-Video)** 생성형 AI입니다.

OpenAI는 Sora를 통해 움직이는 물리 세계를 이해하고 시뮬레이션할 수 있는 AI 시스템을 구축하고자 하며, 실제 환경에서 문제 해결 능력을 키우는 것을 목표로 삼고 있습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/2a3a183c-1de4-486a-b6a3-03f6074315f4/image.png)

* **주요 기능 요약:**
  + 텍스트 프롬프트 기반, 이미지 업로드 및 확장 기능 지원
  + `Storyboard`, `Re-cut`, `Remix`, `Blend`, `Loop` 등 영상 편집 도구 내장
  + 멀티 샷 영상 생성 및 인물, 스타일의 **일관성 유지**

![](https://velog.velcdn.com/images/euisuk-chung/post/69afaf31-c976-4ba2-b5a0-adeebc93321b/image.png)

> “프롬프트 한 줄로 영화 같은 장면이 만들어지는 시대가 시작되었습니다.”

---

기능 간단 소개
--------

Sora는 단순한 영상 생성 도구를 넘어서, 아래와 같은 고급 편집 기능들을 통해 보다 정교하고 창의적인 영상 제작이 가능합니다:

> Image Source: <https://www.datacamp.com/tutorial/sora-ai>

* **Storyboard**
  + 타임라인 기반의 장면 구성 도구로, 각각의 장면(카드)에 텍스트나 이미지를 할당하여 원하는 시간 순서대로 스토리를 구성할 수 있습니다.
  + 복잡한 스토리텔링이나 행동 시퀀스를 설계할 때 매우 유용합니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/4cf7ac9d-20f7-47d8-84c6-e2f86a808885/image.png)

* **Re-cut**
  + 이미 생성된 영상에서 특정 구간만 잘라내어 다시 생성하는 기능입니다.
  + 영상의 마지막 몇 초만 자연스럽게 고치거나, 중간 장면만 수정하고 싶을 때 사용합니다.
  + 불필요한 컷은 제거하고, 좋은 장면은 그대로 유지하는 방식으로 유용합니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/ac6e1ca4-f2ec-468e-accb-f44ff8fed5a9/image.png)

![](https://velog.velcdn.com/images/euisuk-chung/post/dff8cb2f-17b8-4a3b-8eb2-ee85b40d4359/image.png)

* **Remix**
  + 기존 영상의 구성이나 스타일을 유지하면서도 일부 요소(배경, 인물, 오브젝트 등)를 변경하고 싶을 때 사용하는 기능입니다.
  + 변화의 강도를 **Subtle(약하게)**, **Mild(보통)**, **Strong(강하게)** 단계로 설정할 수 있으며, 프롬프트만으로도 매우 유연한 수정이 가능합니다.
  + 업스케일링(화질 개선) 용도로도 활용됩니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/c278bcc9-4e13-4a40-95d1-2ea55f1021e4/image.png)

* **Blend**  
  
  -서로 다른 **두 영상을 부드럽게 연결하여 하나의 클립으로** 만들어주는 기능입니다.
  
  + 예를 들어, 첫 영상의 마지막 장면과 두 번째 영상의 시작 장면을 자연스럽게 전환시키는 데 효과적입니다.  
    
    ![](https://velog.velcdn.com/images/euisuk-chung/post/5b7537a2-b33f-4548-9627-5eea1d478df8/image.png)
  + 타임라인 곡선을 활용해 두 영상 간 영향력을 조절할 수 있습니다.  
    
    ![](https://velog.velcdn.com/images/euisuk-chung/post/42919e69-0f81-4e2e-ba59-7aa600116a4b/image.png)
* **Loop**
  
  + 특정 영상 구간을 반복 재생되도록 설정하는 기능입니다.
  + 자연스러운 루프를 위해 시작/끝 구간을 직접 조정할 수 있으며, **Short**, **Normal**, **Long** 옵션을 선택하여 반복의 자연스러움과 길이를 제어할 수 있습니다.
  + 배경 루프 영상이나 몽환적인 연출에 특히 적합합니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/6dad1e7f-c610-4eeb-990b-cbe55a8efe6e/image.png)

> 🍔 이 기능들을 적절히 조합하면 단순한 AI 생성 영상이 아니라, 완성도 높은 '**AI 기반 콘텐츠**'로 승화시킬 수 있습니다.

---

요금제 및 접근 방식
-----------

> 참고 링크 : [Sora 요금제 및 FAQ](https://help.openai.com/en/articles/10245774-sora-billing-faq)

| 요금제 | 가격 | 영상 길이 및 해상도 | 동시 생성 수 | 특징 |
| --- | --- | --- | --- | --- |
| **Plus** | $20/월 | 최대 10초 / 720p | 최대 2개 | 느린 큐(Relax)에서 무제한 생성 가능 |
| **Pro** | $200/월 | 최대 20초 / 1080p | 최대 5개 | 빠른 생성 속도, 워터마크 없는 다운로드, 고해상도 영상 지원 |

* **Plus**와 **Pro** 요금제 모두 Sora에 무제한 접근 가능하지만, 사용은 OpenAI의 이용 약관을 따라야 합니다.
* **동시 생성 수**는 영상 생성 속도에 큰 영향을 주며, Pro는 대량 워크플로우에 적합합니다.
* **Free, Enterprise, Edu 요금제는 현재 Sora 이용 불가**합니다.

> ⚠️ 고사용량을 방지하기 위한 제한이 일부 존재할 수 있으며, 피크 시간대에는 Pro 사용자도 대기 시간이 발생할 수 있습니다.  
> 
> 영상 생성은 크레딧 기반이 아닌 **큐 우선순위 기반**으로 처리됩니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/f9d652b0-f6b8-48fe-aaa4-9f1f3912d2b3/image.png)

해지 또는 업그레이드는 ChatGPT 설정의 **Subscription → Manage** 메뉴를 통해 진행할 수 있으며, 결제일은 가입일 기준 매월 동일하게 청구됩니다.

---

핵심: **Presets(프리셋)** 기능
-----------------------

Presets는 `스타일`, `색감`, `조명`, `필름 질감` 등 다양한 시네마틱 요소들을 미리 정의해둔 템플릿입니다.

* 특히 **프롬프트 작성에 익숙하지 않은 사용자에게 영상 언어를 손쉽게 익힐 수 있도록 돕는 기능**입니다.

> (정리) **왜 프리셋을 활용해야 하는가?**

| 전략 요소 | 설명 |
| --- | --- |
| 🎯 **ROI 극대화** | 검증된 스타일을 재사용하여 시행착오 최소화, 고퀄리티 영상 제작 가능 |
| ♻️ **재사용성** | 자주 쓰는 스타일을 저장해 반복 활용 가능 |
| 🎨 **일관성 유지** | 하나의 프로젝트 내에서 통일된 스타일 유지에 효과적 |
| 📘 **학습 가이드** | 스타일 요소를 자연스럽게 학습할 수 있는 최고의 시각적 매뉴얼 |

---

프리셋 활용 전략
---------

Sora는 창의적인 작업을 위한 강력한 도구로, 다양한 스타일과 테마를 손쉽게 적용할 수 있는 "프리셋" 설정을 제공합니다.

### 1단계: 프리셋 메뉴 열기

Sora 인터페이스에서 "`Presets`" 버튼을 클릭하면 사용할 수 있는 프리셋 목록이 표시됩니다.

### 2단계: 프리셋 옵션 검토하기

기본 프리셋에는 다음과 같은 테마들이 있습니다:

* `None`: 프리셋을 적용하지 않음
* `Archival`: 빈티지하거나 역사적인 테마
* `Film Noir`: 흑백의 극적인 스타일
* `Cardboard & Papercraft`: 수작업 느낌의 예술적인 스타일
* `Whimsical Stop Motion`: 장난기 있고 애니메이션 같은 스톱 모션 스타일
* `Balloon World`: 알록달록한 풍선 테마

### 3단계: 프리셋 선택하기

원하는 프리셋을 선택하면 즉시 프로젝트에 특유의 비주얼 효과가 적용됩니다.  

(아래 **기본 제공 프리셋 5종 출력 예시** 참고)

### 4단계: 프리셋 관리 및 커스터마이징

"`Manage`" 버튼을 클릭하면 다음과 같은 작업이 가능합니다:

![](https://velog.velcdn.com/images/euisuk-chung/post/791ba987-aec6-4fd9-93de-858194a5c537/image.png)

> Image Source: <https://www.datacamp.com/tutorial/sora-ai>

아래는 프리셋을 효과적으로 활용하는 단계별 전략과 팁입니다.

* **새 프리셋 생성**: 스타일 이름, 설명, 이미지(최대 5장) 업로드 가능

![](https://velog.velcdn.com/images/euisuk-chung/post/48c2a61d-16f4-4d1a-b9b2-cd0affc6cbef/image.png)

* 참조 이미지 업로드 기능 - 이미지(최대 5장) 업로드 가능  
  
  ![](https://velog.velcdn.com/images/euisuk-chung/post/c5b4d5a0-418a-4c33-b7fe-d302e7848d12/image.png)

> **TIPS**✨  
> 
> **프리셋에 글을 적기 어렵거나 익숙하지 않다면**, '`Attach media`' 기능을 통해 참고 이미지를 최대 5장까지 추가할 수 있습니다.
> 
> * 이 이미지들을 기반으로 스타일링이 이루어지므로 초보자에게도 매우 유용합니다.

* **기존 프리셋** `수정` 또는 `삭제`
  + 내가 만든 프리셋 / CLONE한 프리셋만 `수정` 또는 `삭제` 가능

![](https://velog.velcdn.com/images/euisuk-chung/post/3bca36d7-3c9c-449f-a45e-49e00ceb7e9a/image.png)

### 5단계: 커스텀 프리셋 공유 및 팀워크

* 프리셋은 생성 후 **링크 복사** 기능으로 공유할 수 있어 팀워크에 매우 유용합니다.
* 누구나 링크만 있으면 해당 프리셋을 사용할 수 있습니다.

> 🎯 **참고 자료**  
> 
> 참고로 저는 Sora 프리셋을 직접 제작/정리/생성 후 해당 스레드에 공유 중입니다. ([@chung\_es Threads 계정](https://www.threads.net/@chung_es)) 실사용 프리셋 예시와 함께 스타일 연구를 병행하고 있습니다.

📌 기본 제공 프리셋 5종 예시
-----------------

![](https://velog.velcdn.com/images/euisuk-chung/post/80217c5c-fc1f-4cc5-ac73-c44e1ef499e1/image.png)

1. **Balloon World** : 모든 것이 풍선 재질로 표현된 장난스럽고 부드러운 분위기

![](https://velog.velcdn.com/images/euisuk-chung/post/24ff89d2-5922-4bc1-93b2-b78654282647/image.png)

📺 ENG

```
Theme: Everything is inflated like a balloon.
Color: Glossy, bright colors—reds, yellows, blues, and metallics like gold and silver.
Film Stock: Clean digital with exaggerated reflections on shiny surfaces.
Lighting: High-key lighting with glossy highlights to mimic rubbery textures.
Content Transformation: All characters, objects, and environments look inflated, with visible seams and a bouncy quality.
Vibe: Fun, surreal, viral-ready
```

📺 KOR

```
Theme: 모든 것이 풍선처럼 부풀려져 있습니다.
Color: 빨강, 노랑, 파랑, 금속 광택의 금색과 은색 등 밝고 반짝이는 색상.
Film Stock: 디지털 클린 룩, 반짝이는 표면에 과장된 반사광.
Lighting: 고광도 조명, 풍선 특유의 광택 질감 연출.
Content Transformation: 인물, 배경, 사물이 모두 풍선처럼 부풀고 이음선이 보이며, 탄력 있고 말랑한 느낌.
Vibe: 유쾌하고 초현실적인 분위기, 바이럴 영상에 적합.
```

2. **Stop Motion** : 고르지 않은 움직임, 수공예 질감의 따뜻한 톤

![](https://velog.velcdn.com/images/euisuk-chung/post/630b5fe6-36ae-4527-beef-6f4e4ad406ae/image.png)

📺 ENG

```
Theme: Playful handcrafted animation.
Color: Bright, saturated primary colors with handcrafted textures.
Film Stock: Smooth frame-by-frame animation with visible stop-motion quirks.
Lighting: Controlled spotlights with small shadows to highlight miniature craftsmanship.
Vibe: Quirky, charming, family-friendly
```

📺 KOR

```
Theme: 손으로 만든 장난감 애니메이션 느낌.
Color: 선명하고 채도 높은 원색, 종이/점토 질감.
Film Stock: 프레임별로 끊기는 듯한 스톱 모션 특유의 움직임.
Lighting: 소형 스팟 조명, 작은 그림자가 존재.
Vibe: 따뜻하고 유쾌한 분위기, 가족 친화적.
```

3. **Archival** : 거친 필름 질감, 강한 대비와 얕은 심도의 고전 다큐 스타일

![](https://velog.velcdn.com/images/euisuk-chung/post/8f544296-aef8-42bc-af67-e602fdf88025/image.png)

📺 ENG

```
Shot on Eastmann 100t film, the image quality is grainy and high contrast, with shallow depth of field and cinematic look, epic and dramatic shot, very nostalgic.
```

📺 KOR

```
이스트만 100t 필름에서 촬영된 이 영화는 이미지 품질이 거칠고 대비가 높으며, 얕은 깊이의 장면과 영화적인 느낌, 서사적이고 드라마틱한 장면으로 매우 향수를 불러일으킵니다.
```

4. **Film Noir** : 흑백 명암 대비, 강한 그림자, 베네치안 블라인드 효과로 연출된 서스펜스 분위기

![](https://velog.velcdn.com/images/euisuk-chung/post/694ea8d0-8cdb-4694-833d-d4015eb26150/image.png)

📺 ENG

```
Theme: Film Noir
Color: High contrast black and white, deep shadows with selective highlights.
Camera: Arri Alexa Mini, RED Monochrome, or vintage 35mm cameras.
Film Stock: Ilford HP5, Kodak Double-X, or high-contrast digital monochrome settings.
Lighting: Low key, chiaroscuro lighting with hard shadows, venetian blind effects, and strong backlighting.
Vibe: Moody, mysterious, suspenseful
```

📺 KOR

```
Theme: 고전 누아르 영화 스타일.
Color: 고대비 흑백, 깊은 그림자와 강조된 하이라이트.
Camera: Arri Alexa Mini, RED Monochrome, 빈티지 35mm 카메라.
Film Stock: Ilford HP5, Kodak Double-X 등 흑백 필름 스타일.
Lighting: 로우 키 조명, 키아로스쿠로 효과, 블라인드 그림자, 강한 역광.
Vibe: 어둡고 음울하며 긴장감 넘치는 연출.
```

5. **Cardboard & Papercraft** : 골판지/종이 질감, 수작업 느낌 강조된 부드러운 색감

![](https://velog.velcdn.com/images/euisuk-chung/post/17837df5-6b2c-42e6-b1fd-70c3b9369fbe/image.png)

📺 ENG

```
Theme: Cardboard & Papercraft
Color: Earthy tones like brown, beige, and muted pastels, with occasional pops of color to simulate colored paper.
Film Stock: analog film
Lighting: Soft, diffused lighting
Content Transformation: Everything in the scene—from characters to objects and scenery—should be transformed into cardboard, paper, and glue. Elements should have visible creases, folds, and textures resembling handcrafted models.
```

📺 KOR

```
Theme: 골판지 & 종이공예 테마.
Color: 베이지, 브라운, 파스텔 등 차분한 수공예 느낌의 색감.
Film Stock: 아날로그 필름 느낌.
Lighting: 부드럽고 확산된 조명 사용.
Content Transformation: 모든 요소(인물, 배경, 사물)가 종이와 골판지로 만들어진 듯한 질감, 주름과 접힌 자국이 보이는 수작업 질감.
```

---

📖 프롬프트 작성 팁: CAST 구조
--------------------

SORA는 사물과의 상호작용이 많을수록 좋지 않은 성능이 나올 확률이 큽니다.

> 따라서, 아래처럼 CAST 구조를 통해 단순 명료하게 이미지/비디오를 설명해야 원하는 이미지의 결과가 나올 확률이 높아진다고 합니다.

**CAST = Character + Action + Setting + Time**

* **Character**: 등장 인물 (예: 고양이, 우주인, 요리사)
* **Action**: 동작 (예: 걷는다, 점프한다, 요리한다)
* **Setting**: 배경/장소 (예: 도쿄 거리, 우주선 안, 눈 내리는 숲)
* **Time**: 시간/시대 (예: 밤, 2045년, 1940년대 필름 느낌)

💌 **예시 프롬프트**:

```
A stylish woman walks down a Tokyo street filled with warm glowing neon and animated city signage. 
She wears a black leather jacket, a long red dress, and black boots. 
The street is damp and reflective, creating a mirror effect of the colorful lights.
```

💌 프리셋 없이 위 **예시 프롬프트만으로 생성한 결과물**!

![](https://velog.velcdn.com/images/euisuk-chung/post/831a3a19-b490-4070-8214-59eaf1bb5324/image.png)

---

✨ Sora, 영상 크리에이션의 장벽을 허물다!
--------------------------

Sora AI는 단순한 영상 생성 툴이 아니라, **텍스트 기반 영상 창작의 새로운 기준**을 제시하고 있습니다.  

텍스트 한 줄, 이미지 한 장이 시네마틱한 영상으로 변신하는 경험은 **AI와 창작자의 협업**이 얼마나 강력해질 수 있는지를 보여줍니다.

특히 프리셋(Presets)을 적극적으로 활용하면

* **초보자도 안정적인 결과물을 빠르게 얻을 수 있으며**,
* **전문 크리에이터는 영상 스타일의 일관성과 브랜드 아이덴티티를 유지**할 수 있게 됩니다.

> 🎯 핵심은 **프롬프트의 명확성 + 프리셋의 일관성 + 도구 활용의 유연성**입니다.

그리고 무엇보다,  

**Sora는 영상 제작의 진입 장벽을 획기적으로 낮춰주었습니다.**  

덕분에 저 역시 망설이기만 했던 영상 크리에이션에 첫 발을 내디딜 수 있었고,  

**드디어 유튜브 채널까지 개설하게 되었습니다.** 🎬✨

### 🐾 새로운 도전 - 유튜버

Sora를 활용해 다양한 프롬프트와 스타일을 실험하며, 직접 영상들을 제작하고 있습니다.  

그 결과물들을 담은 유튜브 채널도 새롭게 시작했어요!

🎥 [**@aidorable-lab 유튜브 채널 바로가기**](https://www.youtube.com/@aidorable-lab)

> *We create heartwarming, fluffy, and delightfully imaginative pet content designed to brighten your day and soothe your soul.*

> 🐶🐱 **귀엽고 포토제닉한 반려동물 영상**을 좋아하신다면, 꼭 한 번 들러주세요!

잘 부탁드립니다 😎  

감사합니다!

