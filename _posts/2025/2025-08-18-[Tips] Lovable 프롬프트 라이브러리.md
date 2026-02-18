---
title: "[Tips] Lovable 프롬프트 라이브러리"
date: "2025-08-18"
tags:
  - "Lovable"
  - "vibe coding"
year: "2025"
---

# [Tips] Lovable 프롬프트 라이브러리

Lovable 프롬프트 라이브러리: AI 기반 개발을 위한 완벽 가이드
=======================================

> 이 글은 Lovable의 공식 문서인 **[Prompt Library](https://docs.lovable.dev/prompting/prompting-library)**을 번역하고 정리한 콘텐츠입니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/42f73663-7e22-489c-a8a4-3c730d23d190/image.png)

> <https://docs.lovable.dev/prompting/prompting-library>

개요
--

AI 기반 개발이 점점 더 중요해지고 있는 시대에서, **효과적인 프롬프트 작성은 프로젝트 성공의 핵심 요소**가 되었습니다. Lovable의 프롬프트 라이브러리는 다양한 개발 시나리오에서 재사용 가능한 패턴과 예시를 제공하여, 개발자들이 AI와 더 효율적으로 협업할 수 있도록 돕습니다.

이 가이드에서는 프로젝트 시작부터 결제 시스템 통합까지, **실제 개발 과정에서 마주치는 다양한 상황에 대한 구체적인 프롬프트 전략을 소개**합니다. 각 섹션은 특정 사용 사례를 다루며, 언제 사용해야 하는지와 실제 예시 프롬프트를 포함하고 있습니다.

---

프로젝트 시작하기
---------

### 언제 사용하나요?

프로젝트의 최초 단계에서 사용합니다. 이 프롬프트는 AI가 고수준의 요구사항을 이해하고 기반을 구축하는 데 도움을 줍니다. **새로운 앱을 시작**할 때 구축하려는 것, 기술 스택, 핵심 기능을 명시하여 사용합니다. 이는 **프로젝트 브리프(project brief)** 역할을 합니다.

> **프로젝트 브리프(Project Brief)란?**  
> 프로젝트의 목표, 배경, 주요 내용, 기대 결과, 예산, 일정 등 핵심적인 정보를 담은 문서를 의미합니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/32ceec6e-505d-4d20-b23c-3452bb3e4706/image.png)

> <https://asana.com/ko/resources/project-brief>

### 사용 방법

애플리케이션 유형, 핵심 기술(`프론트엔드 프레임워크`, `백엔드`, `기타 서비스`), 주요 기능이나 페이지를 개략적으로 설명합니다. 그 다음 AI에게 어디서 시작할지 지시합니다(보통 메인 페이지나 중요한 기능). 이는 **프로젝트 범위와 초기 초점**을 설정합니다.

#### **Example Prompt — Start New Project:**

```
I need a **task management** application with:
- **Tech Stack:** Next.js frontend, Tailwind CSS for styling, Supabase for auth and database.
- **Core Features:** 
  - Project and task creation, assigning tasks to users, due date reminders, and a dashboard overview.

Start by building the **main dashboard page**, containing:
- A header with navigation,
- A list of projects with their status,
- and a button to create a new project.

Provide dummy data for now, and ensure the design is clean and responsive.
```

**한국어 번역:**

```
다음과 같은 **작업 관리** 애플리케이션이 필요합니다:
- **기술 스택:** Next.js 프론트엔드, 스타일링을 위한 Tailwind CSS, 인증 및 데이터베이스를 위한 Supabase.
- **핵심 기능:** 프로젝트 및 작업 생성, 사용자에게 작업 할당, 마감일 알림, 대시보드 개요.

다음을 포함하는 **메인 대시보드 페이지** 구축부터 시작하세요:
- 네비게이션이 있는 헤더,
- 상태가 표시된 프로젝트 목록,
- 새 프로젝트 생성 버튼.

지금은 더미 데이터를 제공하고, 디자인이 깔끔하고 반응형이 되도록 하세요.
```

이러한 프롬프트들은 **새 프로젝트를 위한 검증된 구조**를 따릅니다.

* 먼저 앱 유형과 기술 스택을 명시하고, 핵심 기능을 나열한 다음, AI에게 어디서 시작할지 알려줍니다.  
  (메인 대시보드 페이지, 구체적인 내용 포함)

이렇게 함으로써 Lovable에게 프로젝트를 시작할 명확한 로드맵을 제공합니다.  
아래는 추가 예시입니다.

#### **Example Prompt — Create a New Component:**

```
Create a new component called [ComponentName] with these features: 

[list features]

- Make it responsive and accessible with proper keyboard navigation.
- Include proper TypeScript typings for props, and use Tailwind for styling.
```

**한국어 번역:**

```
새로운 컴포넌트 **[ComponentName]**를 다음 기능과 함께 생성하세요:

[list features]

- 반응형(Responsive) 및 접근성(Accessible)을 지원하며, 올바른 키보드 내비게이션을 포함할 것.
- Props에 대해 올바른 TypeScript 타입을 정의할 것.
- 스타일링은 Tailwind CSS를 사용할 것.
```

#### **Example Prompt — Explain & Review a Function:**

```
Explain how this function works in simple terms, highlighting its inputs, outputs, and any side effects: 

[paste function]

What edge cases does it handle or miss? How could it be improved?
```

**한국어 번역:**

```
아래 함수를 간단하게 설명하세요. 

[paste function]

* 특히 입력(Inputs), 출력(Outputs), 그리고 발생할 수 있는 부작용(Side Effects)을 강조합니다.  
* 또한 이 함수가 처리하는 엣지 케이스와 놓치는 경우를 분석하고, 어떻게 개선할 수 있을지 제안하세요.
```

---

UI/UX 디자인
---------

### 언제 사용하나요?

기능은 변경하지 않고 앱의 **모양과 느낌을 개선**하고 싶을 때 사용합니다.  
UI 다듬기, 레이아웃 조정, 또는 특정 디자인 스타일 구현에 활용할 수 있습니다.

### 사용 방법

**디자인 변경의 범위를 명확히 명시**하고 **기능은 그대로 유지**되어야 함을 강조합니다.

* AI는 스타일링에 꽤 능숙하지만, 원하는 "룩"(예: 모던, 미니멀, 특정 디자인 시스템과 매칭)에 대해 안내해야 합니다.
* 여러 변경사항이 있다면 **한 번에 하나씩 처리**하세요(예: 먼저 레이아웃, 그 다음 색상).
* 로직적으로 변경되어서는 안 되는 UI 부분이 있다면 항상 언급하세요.

**예시 프롬프트 - UI 전용 변경:**

```
The app UI should be improved, **without changing any functionality**. 

- Keep all existing logic and state management as is.
- **Visual Enhancements:** Update the styling of the dashboard page: 
   - use a modern card design for each project listing.
   - improve the color scheme for better contrast.
   - increase padding for a cleaner layout.
- Ensure these changes do **not break any functionality or data flow**.

*Goal:* purely cosmetic improvements for a more polished look, with the app behaving exactly as before.
```

**한국어 번역:**

```
앱 UI를 **기능 변경 없이** 개선해야 합니다.

- 모든 기존 로직과 상태 관리를 그대로 유지하세요.
- **시각적 개선:** 대시보드 페이지의 스타일링을 업데이트하세요: 
  - 각 프로젝트 목록에 모던한 카드 디자인 사용.
  - 더 나은 대비를 위한 색상 스키마 개선.
  - 더 깔끔한 레이아웃을 위한 패딩 증가.
- 이러한 변경사항이 **기능이나 데이터 흐름을 깨뜨리지 않도록** 하세요.

*목표:* 앱이 이전과 정확히 동일하게 동작하면서 더 세련된 모습을 위한 순수한 미용적 개선.
```

이 프롬프트에서 우리는 시각적 개선만 하고 앱 작동 방식에는 영향을 주지 않도록 명시적으로 말합니다. 이는 중요합니다 - AI에게 "로직을 건드리지 마라"고 알려주는 것입니다.

> 구체적인 내용(`카드 디자인`, `색상 대비`, `간격`)을 나열하여 AI가 UI의 어떤 측면을 조정해야 하는지 알 수 있게 합니다.

**예시 프롬프트 - Enhance the visual appeal of this component**

```
Enhance the visual appeal of this component: 

[paste component]. 

Add animations, improve spacing, create a polished look while maintaining accessibility standards and responsive behavior.
```

**한국어 번역:**

```
이 컴포넌트의 시각적 매력을 향상시키세요: 

[컴포넌트 붙여넣기].

애니메이션을 추가하고, 여백을 개선하며, 세련된 외관을 만들되 접근성 기준과 반응형 동작을 유지하세요.
```

(예시) SUBMIT 버튼 개선 TEST

`Enhance the visual appeal` of this component:  
**A primary button with label "Submit", currently styled with flat blue background and white text.**

Add animations, improve spacing, create a polished look while maintaining accessibility standards and responsive behavior.

![](https://velog.velcdn.com/images/euisuk-chung/post/67f2e8fd-36d8-4657-9fad-c23f3129efd7/image.png)

> Submit 버튼에 대해서 다양한 버튼 생성

---

**예시 프롬프트 - Create a comprehensive design system**

```
Create a **comprehensive design system** for my application.

Should support color palette, typography scale, spacing system, and component variants. 

Include dark mode support and ensure all components are accessible (WCAG AA compliant).
```

**한국어 번역:**

```
애플리케이션을 위한 **포괄적인 디자인 시스템**을 만들어주세요. 

색상 팔레트, 타이포그래피 스케일, 여백 시스템, 컴포넌트 변형을 포함하고, 다크 모드도 지원해주세요. 

모든 컴포넌트는 접근성 기준(WCAG AA)을 충족해야 합니다.
```

Semantic Colors  
![](https://velog.velcdn.com/images/euisuk-chung/post/50abcb83-04e1-44af-aeac-64c097b48d61/image.png)

Neutral Scale  
![](https://velog.velcdn.com/images/euisuk-chung/post/3dc42822-4efc-47ee-adcb-614ac2d82dcc/image.png)

Font Sizes & Line Heights  
![](https://velog.velcdn.com/images/euisuk-chung/post/75f6532d-22d4-48b7-8c3a-65d4d47cfcee/image.png)

Spacing Scale  
![](https://velog.velcdn.com/images/euisuk-chung/post/ace4e185-6cd5-498b-8c37-3715f95dbba4/image.png)

Component Variants  
![](https://velog.velcdn.com/images/euisuk-chung/post/a41652f2-85b9-4271-a226-5b19df54f6d1/image.png)

---

**예시 프롬프트 - Design a responsive dashboard layout**

```
Design a responsive dashboard layout with [describe key metrics/widgets]. 

It should work well on mobile, tablet, and desktop with appropriate layout shifts. 
Include a sidebar navigation that collapses on mobile.
```

**한국어 번역:**

```
[핵심 지표/위젯 설명]을 포함한 반응형 대시보드 레이아웃을 설계해주세요. 

모바일, 태블릿, 데스크탑에서 모두 잘 작동하도록 적절한 레이아웃 전환이 있어야 합니다.
모바일에서는 사이드바 내비게이션이 접히도록 해주세요.
```

(예시)  
![](https://velog.velcdn.com/images/euisuk-chung/post/3984e745-f3fa-467c-99a4-516f4edb0712/image.png)

> 반응형 UI 설계, 주요 위젯 구성, 디바이스별 레이아웃 변화, 사이드바 동작 등 다양한 요소를 테스트

* (참고) 위 대시보드를 만들기 위해 `[describe key metrics/widgets]`로 아래 사항들을 요청했어요!!

```
- **Sales Performance**: Bar chart comparing monthly sales.
- **Conversion Rate**: KPI widget with percentage and trend arrow.
- **Notifications Panel**: List of recent alerts/messages.
- **Task Progress**: Circular progress indicators for ongoing projects.
```

---

**예시 프롬프트 - Transform to mobile-first design**

```
Transform this desktop-only component into a mobile-first design with responsive breakpoints: 

[paste component].

Prioritize content and interactions for small screens first, then enhance for larger screens.
```

**한국어 번역:**

```
이 데스크탑 전용 컴포넌트를 모바일 우선 디자인으로 전환하세요:

[컴포넌트 붙여넣기].

작은 화면에서 콘텐츠와 상호작용을 우선시하고, 이후 큰 화면에 맞게 확장하세요.
```

(예시)  
![](https://velog.velcdn.com/images/euisuk-chung/post/a57d06b3-3dd2-460a-9ad9-5780fb468bde/image.png)

> 모바일 우선 접근 방식, 반응형 브레이크포인트, UI 재배치 등을 테스트

* (참고) 위 대시보드를 만들기 위해 `[paste component]`에 아래 사항들을 요청했어요!!

```
**Component Description**:
- A dashboard header with logo, search bar, and user profile dropdown.
- A 3-column layout showing:
  - Left: Navigation menu with icons and labels.
  - Center: Main content area with cards and charts.
  - Right: Notifications and quick actions.
```

---

**예시 프롬프트 - Add subtle, performant animations**

```
Add subtle, performant animations to this component to enhance user experience: 

[paste component]. 

Include enter/exit animations, hover states, and micro-interactions that provide feedback without being distracting.
```

**한국어 번역:**

```
이 컴포넌트에 사용자 경험을 향상시킬 수 있는 섬세하고 성능에 영향을 주지 않는 애니메이션을 추가하세요: 

[컴포넌트 붙여넣기]. 

진입/퇴장 애니메이션, 호버 상태, 방해되지 않는 피드백용 마이크로 인터랙션을 포함하세요.
```

(예시)  
![](https://velog.velcdn.com/images/euisuk-chung/post/459a03dc-0689-4702-92e0-a4cfcbe8290d/image.png)

> UI 애니메이션 및 성능과 사용자 경험을 모두 고려한 설계 요청

* (참고) 위 대시보드를 만들기 위해 `[paste component]`에 아래 사항들을 요청했어요!!

Component Description:

```
- A card-based dashboard widget showing user stats.
- Includes a header, a number counter, and an action button.
```

Animation Requirements:

```
- **Enter/Exit Animations**: Fade-in and slide-up when the component mounts; fade-out and slide-down on unmount.
- **Hover States**: Slight scale-up and shadow on hover for cards and buttons.
- **Micro-interactions**:
  - Button click should show a ripple effect.
  - Number counter should animate from 0 to target value on load.
```

---

**예시 프롬프트 - Analyze and optimize the user flow**

```
Analyze and optimize the user flow for [describe task/goal]. 

Map out each step of the journey, identify friction points, and suggest UI improvements to create a more intuitive experience with fewer steps.
```

**한국어 번역:**

```
[작업/목표 설명]에 대한 사용자 흐름을 분석하고 최적화하세요. 

여정의 각 단계를 시각화하고, 마찰 지점을 식별하며, 더 직관적이고 단계 수가 적은 경험을 위한 UI 개선점을 제안하세요.
```

(예시)  
`[describe task/goal]`에 **“AI 챗봇을 통한 고객 지원 질문 처리”**라는 목표를 넣고 돌리면 아래와 같은 결과가 나옵니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/f98c50c3-cb34-43ba-8096-ec4f8065f853/image.png)

> 사용자 챗봇 질의 여정을 분석하고, 병목/마찰 구간을 찾고, 더 나은 UI 개선안을 제시

---

**예시 프롬프트 - Review components for accessibility**

```
Review these components for accessibility issues and suggest improvements: 
[paste components]. 

Check for proper keyboard navigation, screen reader support, sufficient color contrast, and appropriate ARIA attributes.
```

**한국어 번역:**

```
이 컴포넌트들의 접근성 문제를 검토하고 개선점을 제안하세요: 
[컴포넌트 붙여넣기]. 

키보드 내비게이션, 스크린 리더 지원, 충분한 색상 대비, 적절한 ARIA 속성 등을 확인하세요.
```

(예시)  
`[paste components]` 자리에 실제 HTML/React 컴포넌트 코드를 넣으면, 접근성(A11y) 기준(WCAG 2.1 AA)에 따라 자동으로 진단(Audit) 리포트를 생성해줍니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/4cc1c1a1-17d8-4e53-87f1-9bafc5f6505b/image.png)

> UI 코드 → 접근성 리뷰 보고서 작성

---

반응형 디자인
-------

### 언제 사용하나요?

* 앱의 레이아웃이 **다양한 화면 크기(모바일, 태블릿, 데스크톱)에서 작동**해야 할 때 사용합니다.
* 데스크톱에서는 좋아 보이지만 모바일에서 깨진다는 것을 발견했다면, 반응형 프롬프트를 사용할 때입니다.
* **UI 집약적인 작업의 최종 단계에서도 이를 수행**하는 것이 좋습니다.

### 사용 방법

* **모바일 우선 접근법**을 강조하고 AI에게 모든 표준 breakpoint에서 디자인이 반응형이 되도록 요청합니다.
* Tailwind와 같은 CSS 프레임워크를 사용한다면, 그리드/플렉스와 내장 breakpoint를 사용하도록 언급하세요.
* 유동적인 크기 조정을 방해할 수 있는 고정 너비나 기타 요소를 피하도록 AI에게 지시할 수도 있습니다.

**예시 프롬프트 - 모바일 반응성:**

```
Our app needs to be **fully responsive** across mobile, tablet, and desktop.

- Follow a **mobile-first** strategy: prioritize the layout for small screens, then adjust for larger screens.
- Use modern UI/UX best practices for responsive design. (For Tailwind CSS, use the standard breakpoints `sm, md, lg, xl` – no custom breakpoints unless necessary.)
- Ensure every page (especially the dashboard and project detail pages) reflows properly on a small screen: elements should stack or resize as needed, text should remain readable, and no content should overflow off-screen.
- **Do not change the core design or functionality**, just make sure it flexibly adapts to different screen sizes.

After making changes, please double-check the layout at iPhone 12 dimensions and a typical desktop width.
```

**한국어 번역:**

```
우리 앱은 모바일, 태블릿, 데스크톱에서 **완전히 반응형**이어야 합니다.

- **모바일 우선** 전략을 따르세요: 작은 화면을 위한 레이아웃을 우선시하고, 그 다음 큰 화면에 맞게 조정하세요.
- 반응형 디자인을 위한 현대적인 UI/UX 모범 사례를 사용하세요. (Tailwind CSS의 경우, 표준 breakpoint `sm, md, lg, xl`을 사용하세요 – 필요하지 않다면 커스텀 breakpoint는 사용하지 마세요.)
- 모든 페이지(특히 대시보드와 프로젝트 상세 페이지)가 작은 화면에서 적절히 재배치되도록 하세요: 필요에 따라 요소들이 쌓이거나 크기가 조정되어야 하고, 텍스트는 읽기 가능하게 유지되어야 하며, 콘텐츠가 화면 밖으로 넘치지 않아야 합니다.
- **핵심 디자인이나 기능을 변경하지 마세요**, 단지 다양한 화면 크기에 유연하게 적응하도록 하세요.

변경 후, iPhone 12 크기와 일반적인 데스크톱 너비에서 레이아웃을 다시 확인해주세요.
```

> 📝 **요청 분석**
>
> * **목적:** 앱의 모든 화면을 모바일, 태블릿, 데스크톱에서 문제없이 동작하게 반응형으로 개선
> * **조건:**
>   + 기존의 UI 디자인/기능은 절대 변경하지 않음
>   + 단지 **다양한 화면 크기에서 깨지지 않고 재배치/재조정**되도록 보장
> * **요청:**
>   1. **모바일 우선 전략 적용**: 작은 화면 최적화 → 큰 화면 확장
>   2. **표준 breakpoint 사용**: Tailwind 내장 `sm, md, lg, xl`
>   3. **가독성/접근성 보장**: 텍스트 크기, 버튼 크기 유지
>   4. **플렉스/그리드 활용**: 레이아웃 자동 재배치
>   5. **유연한 레이아웃**: 고정 width 회피, overflow 방지

![](https://velog.velcdn.com/images/euisuk-chung/post/08a4a543-2c04-41a7-a781-0221a6632626/image.png)

> 다양한 창 사이즈에도 제대로 구현이 된것을 볼 수 있습니다. (위: PC, 아래: Mobile)

![](https://velog.velcdn.com/images/euisuk-chung/post/11af5a4c-6e74-4387-b4b0-2fcc11b85ef0/image.png)

---

리팩토링
----

### 언제 사용하나요?

* `리팩토링`은 개발 중 주기적으로, 특히 **AI나 개발자가 많은 코드를 추가해서 상황이 복잡하거나 느려지고 있을 때** 사용합니다.
* 리팩토링은 기능은 변경하지 않고 코드를 정리하는 것을 의미합니다.
  + 바로, `구조`, `가독성`, `성능`을 개선하는 것입니다.

### 사용 방법

* 작업의 `범위`를 식별하세요: `단일 파일`인지, `특정 기능`인지, `전체 코드베이스`인지?
* 단일 파일이나 컴포넌트의 경우, "명확성과 효율성을 위해 이 파일을 리팩토링하되, **기능이나 출력을 변경하지 마세요**"와 같이 프롬프트할 수 있습니다.
* 리팩토링 후에도 모든 것이 동일하게 동작해야 함을 강조하세요.

**예시 프롬프트 - 안전한 파일 리팩토링:**

```
Refactor the **ProjectList component file**, but **keep its behavior and UI exactly the same**. 

Goals:
- Improve the code structure and readability (simplify complex functions, break into smaller ones if needed).
- Remove any unused variables or imports.
- Ensure the file follows best practices and is well-documented.

Do **not** introduce any new features or change how the component works for the user – this is purely a code cleanup for maintainability. If any part of the code is unclear, add a brief comment for clarification.
```

**한국어 번역:**

```
**ProjectList 컴포넌트 파일**을 리팩토링하되, **동작과 UI를 정확히 동일하게 유지**하세요.

목표:
- 코드 구조와 가독성 개선 (복잡한 함수 단순화, 필요시 더 작은 함수로 분할).
- 사용하지 않는 변수나 import 제거.
- 파일이 모범 사례를 따르고 잘 문서화되도록 보장.

새로운 기능을 도입하거나 사용자에게 컴포넌트가 작동하는 방식을 변경하지 **마세요** – 이는 유지보수성을 위한 순수한 코드 정리입니다. 코드의 어떤 부분이 불분명하다면, 명확성을 위한 간단한 주석을 추가하세요.
```

> 📝 **요청 분석**
>
> * **목적:** `ProjectList` 컴포넌트 파일의 리팩토링
> * **조건:**
>   + UI나 동작(behavior)은 **절대 바꾸지 않음**
>   + 사용자 입장에서는 결과물이 똑같아야 함
> * **요청:**
>   1. **코드 구조 개선**: 복잡한 함수 단순화, 필요한 경우 작은 함수로 분리
>   2. **불필요한 코드 제거**: 사용하지 않는 변수나 import 삭제
>   3. **베스트 프랙티스 적용**: React 컴포넌트 작성 관례, 일관된 스타일 유지
>   4. **가독성 향상**: 코드 흐름을 더 쉽게 읽고 이해할 수 있도록 리팩토링
>   5. **주석 추가**: 모호한 부분이 있으면 간단한 설명 주석 보강

위와 같은 방식으로 기존 코드의 리팩토링을 수행할 수 있습니다.

---

범위 제한 / 파일 잠금
-------------

### 언제 사용하나요?

* 때로는 AI가 프로젝트의 특정 부분에 집중하고 다른 모든 것은 그대로 두기를 원할 때가 있습니다.
* 특정 파일이나 영역을 "잠가서" AI가 다른 작업을 하는 동안 수정되지 않도록 하는 것입니다.
* 수동으로 작성한 코드가 있거나 AI가 다른 작업을 하는 동안 변경되지 않기를 원하는 안정적인 컴포넌트가 있을 때 유용합니다.

### 사용 방법

* 프롬프트에서 AI가 특정 파일이나 컴포넌트를 **변경하지 않도록** 명시적으로 지시합니다.
* "인증 파일을 편집하지 마세요" 또는 "HomePage 컴포넌트를 변경하지 마세요"라고 말할 수 있습니다.
* 또한 AI가 변경 사항을 집중해야 할 곳을 명확히 하세요.

**예시 프롬프트 - 변경 범위 제한:**

```
Please **focus only on the Dashboard page** for this change. 

- Do **not modify** the `LoginPage.tsx` or `AuthProvider.tsx` files at all (authentication is working well, and we want to keep it intact).
- Concentrate your code edits on `Dashboard.tsx` and related dashboard components **only**.

Task: Add a new section to the Dashboard that shows "Tasks due this week". Make sure to fetch the relevant tasks from the database. 

*(Again, no changes to login or auth files – those are off-limits.)*
```

**한국어 번역:**

```
이 변경사항에 대해서는 **대시보드 페이지에만 집중**해주세요.

- `LoginPage.tsx` 또는 `AuthProvider.tsx` 파일을 전혀 **수정하지 마세요** (인증이 잘 작동하고 있어서 그대로 유지하고 싶습니다).
- `Dashboard.tsx`와 관련된 대시보드 컴포넌트에**만** 코드 편집을 집중하세요.

작업: 대시보드에 "이번 주 마감 작업"을 보여주는 새로운 섹션을 추가하세요. 데이터베이스에서 관련 작업을 가져오도록 하세요.

*(다시 말하지만, 로그인이나 인증 파일은 변경하지 마세요 – 그것들은 금지구역입니다.)*
```

---

계획 수립
-----

### 언제 사용하나요?

* 복잡하거나 다단계 구현에 뛰어들기 전에, 또는 하위 작업으로 나눌 수 있는 큰 기능이 있을 때 사용합니다.
* 계획 프롬프트는 코드 작성 전에 AI가 접근법을 개요화하도록 하여, 잘못된 경로로 코드 생성 크레딧을 소모하지 않고 계획을 확인(그리고 조정)할 수 있게 해줍니다.

### 사용 방법

* AI에게 계획이나 체크리스트를 작성하도록 요청합니다.
* "X를 위한 단계별 계획을 개요화하세요" 또는 "코딩하기 전에, Y를 구현하기 위해 취할 단계들을 나열하세요"라고 말할 수 있습니다.
* 계획을 받은 후, 이를 논의하고(AI에게 각 단계가 왜 필요한지 설명하게 할 수도 있음) 단계별로 구현을 진행할 수 있습니다.

**예시 프롬프트 - 기능 구현 계획:**

```
Before writing any code, **plan out the implementation** of the new Notifications feature.

- List each step required to add email notifications when a task is overdue.
- Consider both frontend (UI changes, if any) and backend (creating scheduled checks or triggers) aspects.
- Ensure the plan keeps the current functionality stable – we can't break anything existing.
- Provide the plan as an ordered list (1, 2, 3, ...), with a brief explanation of each step.

Once you outline the plan, pause for review. **Do not make any code changes yet.**
```

**한국어 번역:**

```
코드를 작성하기 전에, 새로운 알림 기능의 **구현을 계획**하세요.

- 작업이 지연될 때 이메일 알림을 추가하는 데 필요한 각 단계를 나열하세요.
- 프론트엔드(UI 변경사항이 있다면)와 백엔드(예약된 확인이나 트리거 생성) 측면을 모두 고려하세요.
- 계획이 현재 기능을 안정적으로 유지하도록 하세요 – 기존의 것을 깨뜨릴 수 없습니다.
- 각 단계에 대한 간단한 설명과 함께 순서가 있는 목록(1, 2, 3, ...)으로 계획을 제공하세요.

계획을 개요화한 후, 검토를 위해 잠시 멈추세요. **아직 코드 변경사항을 만들지 마세요.**
```

> 📝 **요청 분석**
>
> * **목적:** 큰 기능이나 다단계 구현을 코드 작성 전 **계획으로 구조화**
> * **조건:**
>   + 코드 작성은 하지 않고 계획만 수립
>   + 현재 기능 안정성을 해치지 않음
>   + 단계별 설명 포함
> * **요청:**
>   1. 단계별 구현 계획을 순서 있는 리스트로 작성
>   2. 각 단계에 대한 간단한 설명 포함
>   3. 프론트엔드/백엔드 관점 모두 고려
>   4. 계획만 작성하고 실제 코드 생성은 보류

---

Stripe 설정
---------

### 언제 사용하나요?

* Stripe를 사용하여 앱에 결제 기능을 통합하고 싶을 때 사용합니다.
* Lovable은 Stripe와의 통합 지점을 가지고 있지만, 키, 웹훅, 체크아웃 UI 설정이 필요합니다.
* 프롬프트는 Stripe API 연결의 보일러플레이트를 처리할 수 있습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/d8831740-f2a2-45c7-aa98-94fbd9ef95fe/image.png)

> <https://stripe.com/>

💸 **(참고) Stripe란?**

* Stripe는 기업이 온라인 및 오프라인 거래에서 결제를 처리할 수 있도록 지원하는 **글로벌 온라인 결제 인프라 플랫폼**입니다.
* 개발자가 웹사이트나 앱에 Stripe의 API(애플리케이션 프로그래밍 인터페이스)를 통합하여 신용카드, 모바일 결제 등 다양한 결제 수단을 쉽게 받아들일 수 있게 하며, 결제 과정을 간소화하고 전 세계 어디서든 결제를 주고받을 수 있도록 돕습니다.

### 사용 방법

* Stripe가 필요로 하는 세부사항을 제공하세요:
  + 모드(테스트 또는 라이브), 제품 또는 가격 정보, 결제 후 리디렉션 URL.
* 또한 UI가 어떻게 동작해야 하는지 지시하세요(예: 체크아웃 폼/모달).
* 민감한 키는 안전하게 제공될 것이라고 언급하는 것이 **중요**합니다(프롬프트에 하드코딩되지 않음) - 일반적으로 환경 변수나 Lovable의 비밀 저장소에 저장합니다.

**예시 프롬프트 - Stripe 결제 통합:**

```
I want to **add Stripe payments** to the app.

- Use **Stripe in test mode** for now.
- We have a product in Stripe with ID `prod_12345` and a price ID `price_67890` (one-time purchase).
- Implement a checkout button on the **Pricing page** that starts a Stripe checkout for that product.
- After successful payment, redirect the user to `/payment-success`. If the payment is canceled, redirect to `/payment-cancelled`.

Important:
- Assume API keys and webhook secrets are configured securely (do **not** hard-code them).
- Do **not** modify any other pages or features unrelated to payments.

Once done, provide any webhook endpoint setup instructions I need 
(e.g., URL to add in Stripe dashboard for post-payment events).
```

**한국어 번역:**

```
앱에 **Stripe 결제를 추가**하고 싶습니다.

- 지금은 **테스트 모드에서 Stripe**를 사용하세요.
- Stripe에 ID가 `prod_12345`인 제품과 가격 ID `price_67890`(일회성 구매)이 있습니다.
- **가격 페이지**에 해당 제품에 대한 Stripe 체크아웃을 시작하는 체크아웃 버튼을 구현하세요.
- 결제 성공 후, 사용자를 `/payment-success`로 리디렉션하세요. 결제가 취소된 경우, `/payment-cancelled`로 리디렉션하세요.

중요사항:
- API 키와 웹훅 시크릿이 안전하게 구성되어 있다고 가정하세요 (하드코딩하지 **마세요**).
- 결제와 관련 없는 다른 페이지나 기능을 **수정하지 마세요**.

완료되면, 필요한 웹훅 엔드포인트 설정 지침을 제공하세요 
(예: 결제 후 이벤트를 위해 Stripe 대시보드에 추가할 URL).
```

> 📝 **요청 분석**
>
> * **목적:** Stripe API를 앱에 안전하게 통합하여 결제 기능 추가
> * **조건:**
>   + Stripe API 키/웹훅 시크릿은 하드코딩 금지 (환경 변수 활용 가정)
>   + 테스트 모드 우선 사용
>   + 결제 성공/취소 후 리디렉션 경로 지정
>   + 결제와 무관한 기능은 수정하지 않음
> * **요청:**
>   1. Stripe Checkout 버튼 구현 (특정 product/price ID 사용)
>   2. 결제 성공 시 `/payment-success`로 이동
>   3. 취소 시 `/payment-cancelled`로 이동
>   4. Stripe 대시보드에 등록해야 할 웹훅 엔드포인트 지침 제공

### 🔑 API KEY는 그럼 어떻게 처리하는가!

Stripe와 같은 결제 시스템의 API 키는 **직접 코드에 하드코딩하면 안 되고**, 반드시 **환경 변수 또는 Lovable의 비밀 저장소(Secrets)**에 넣어야 합니다.

**1. 키의 종류**

* **Publishable key (pk\_...)** → 프론트엔드에서 사용 (Stripe.js 초기화)
* **Secret key (sk\_...)** → 서버/Edge Function에서만 사용 (세션 생성, 구독 관리)
* **Webhook signing secret (whsec\_...)** → Stripe 웹훅 이벤트 검증 시 사용

**2. 저장 방법**

* 개발 환경: `.env` 파일 (예: `.env.local`)
* 배포 환경: Lovable/Supabase Secrets 또는 서버의 환경 변수 관리 기능

```
STRIPE_SECRET_KEY=sk_test_***
STRIPE_PUBLISHABLE_KEY=pk_test_***
STRIPE_WEBHOOK_SECRET=whsec_***
```

**3. 사용 흐름**

1. 프론트엔드에서 결제 요청 버튼 클릭
2. 서버(API 라우트 또는 Supabase Edge Function)가 **Secret key**로 Checkout 세션 생성
3. 클라이언트는 반환된 `session.url`로 Stripe 결제 페이지 리다이렉트
4. Stripe가 결제 완료 후 **Webhook**을 통해 서버에 알림 → 서버가 DB 업데이트, 구독 상태 활성화

**4. 왜 이렇게 하나?**

* 비밀 키가 프론트 코드에 노출되지 않음 → 유저가 확인할 수 없음
* Stripe의 결제 UI에서 카드 정보를 처리하므로, 서버가 직접 민감 데이터(PAN 번호)를 다루지 않음
* 웹훅 기반으로 **신뢰 가능한 이벤트 처리** 가능 → 구독형 서비스 관리 안정화

> 👉 이렇게 하면 Stripe를 Lovable/웹앱 환경에 안전하게 붙일 수 있고, 구독형 시스템까지 확장 가능합니다.

---

Supabase 및 백엔드
--------------

* Supabase를 사용한 백엔드 작업에는 데이터베이스 스키마 설계, Row Level Security 정책 구현, Edge Function 생성 등이 포함됩니다.
* 이러한 작업들은 애플리케이션의 보안과 성능에 직접적인 영향을 미치므로 신중하게 접근해야 합니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/f5a239d2-ea59-4a1c-badc-ca5430df6588/image.png)

> <https://supabase.com/>

**예시 프롬프트 - 데이터베이스 스키마 설계:**

```
Design a database schema for [describe your application] with these entity relationships: 
[describe relationships].

Include foreign key constraints, indexes for performance, and proper data types with considerations for scalability.
```

**한국어 번역:**

```
다음 엔티티 관계를 가진 [애플리케이션 설명]을 위한 데이터베이스 스키마를 설계하세요: 
[관계 설명]. 

성능을 위한 인덱스, 외래 키 제약조건, 확장성을 고려한 적절한 데이터 타입을 포함하세요.
```

> 📝 **요청 분석**
>
> * **목적:** Supabase 기반으로 안전하고 확장 가능한 백엔드 구현
> * **조건:**
>   + 데이터베이스 스키마는 관계형 설계 원칙 준수
>   + 성능을 위한 인덱스 포함
>   + 외래 키 제약조건 반영
>   + 데이터 타입은 확장성 고려
>   + 보안 강화를 위해 RLS(Row Level Security) 등도 향후 고려 가능
> * **요청:**
>   1. 엔티티/관계 기반 데이터베이스 스키마 설계
>   2. 성능(인덱스), 무결성(외래키), 확장성(데이터 타입) 고려
>   3. 애플리케이션 설명과 관계를 기반으로 ERD 수준 설계 제공

### 추가 프롬프트

#### 컴포넌트 비주얼 개선

**[프롬프트]**

```
Enhance the visual appeal of this component: 
[paste component]. 

Add animations, improve spacing, create a polished look while maintaining accessibility standards and responsive behavior.
```

**[분석]**

* **목적:** UI 가독성·일관성 향상 및 마이크로 인터랙션 추가
* **범위:** 스타일 레이어(레이아웃/타이포/간격/애니메이션)만 변경, 로직 불변
* **산출물:** 수정된 컴포넌트 코드, 접근성 점검 목록(ARIA, 콘트라스트), 반응형 규칙
* **체크리스트:** spacing scale 적용, focus/hover 상태 정의, prefers-reduced-motion 대응, 키보드 탭 순서 보장, Tailwind/utility class 정리

---

#### 데이터베이스 스키마 설계

**[프롬프트]**

```
Design a database schema for [describe your application] with these entity relationships: 
[describe relationships]. 

Include foreign key constraints, indexes for performance, and proper data types with considerations for scalability.
```

**[분석]**

* **목적:** 관계·무결성·성능을 고려한 스키마 초안 확정
* **범위:** 엔터티/릴레이션, FK/UK, 인덱스, enum/domain/type 선정
* **산출물:** DDL 스크립트, ERD, 인덱스 전략(복합/부분/GIN), 파티셔닝 고려 사항
* **체크리스트:** 정규화 수준(3NF±), soft-delete/감사 컬럼, 시계열 파티션, UUID vs BIGINT, 다국어/통화 컬럼, RLS 전제 시 테넌트 키 포함

---

#### 데이터 페치 서비스 구현

**[프롬프트]**

```
Create a service to fetch data from [API name] and implement caching, error retry logic, and request throttling. 

Set up proper TypeScript interfaces for the response data and handle API versioning gracefully.
```

**[분석]**

* **목적:** 안정적·예측 가능한 API 클라이언트 계층 구현
* **범위:** fetch/axios 래퍼, 캐시(LRU/TTL), 재시도(backoff/jitter), 스로틀(토큰버킷)
* **산출물:** TS 서비스 모듈, DTO/타입 정의, 버전 추상화 레이어(v1/v2), 에러 매핑
* **체크리스트:** idempotency, 429/5xx 처리, ETag/If-None-Match, AbortController, 테스트용 mock 어댑터

---

#### 행 수준 보안 정책 설정

**[프롬프트]**

```
Create Row Level Security policies for a multi-tenant application with these tables: 
[list tables]. 

Implement proper user isolation, role-based access, and handle hierarchical data access with considerations for performance.
```

**[분석]**

* **목적:** 테넌트 기반 격리 + 역할별 접근 제어
* **범위:** `ENABLE RLS`, `POLICY` 정의(SELECT/INSERT/UPDATE/DELETE), 하위 리소스 계층 접근(조직→프로젝트→리소스)
* **산출물:** SQL 정책 스크립트, 역할 매핑 테이블, 인덱스(tenant\_id, role 조합)
* **체크리스트:** `auth.uid()` 매핑, 조인 기반 정책 성능(부분 인덱스/Materialized View 고려), 복합 키(tenant\_id+id)

---

#### Supabase Edge Function 개발

**[프롬프트]**

```
Create a Supabase Edge Function to handle [describe functionality] with proper error handling, input validation, and security checks. 

Include rate limiting and proper environment variable usage.
```

**[분석]**

* **목적:** 경량 서버리스 엔드포인트로 비즈니스 로직 캡슐화
* **범위:** 입력 검증(Zod/valibot), 인증/권한, 레이트 리미팅(슬라이딩 윈도/토큰 버킷)
* **산출물:** Edge Function 코드, 환경 변수 스키마, 관측(로그/트레이스)
* **체크리스트:** 서명 토큰 검증, CORS, 타임아웃/재시도, 비밀값은 `Deno.env`/Vault, PII 로그 마스킹

---

#### 실시간 데이터 동기화

**[프롬프트]**

```
Implement real-time data synchronization for [describe feature] using Supabase subscriptions. 

Handle connection management, graceful degradation when offline, and conflict resolution.
```

**[분석]**

* **목적:** 변경 스트림 기반 실시간 UI 반영
* **범위:** Realtime 채널 구독, 네트워크 상태 감지, 오프라인 큐/재동기화
* **산출물:** 구독 핸들러, optimistic update/rollback 로직, 충돌 해결 정책(last-write-wins/CRDT 대안)
* **체크리스트:** 배압 처리, 구독 스코프(tenant/channel), 재연결 백오프, 스냅샷+증분 동기

---

#### 고급 검색 기능 구현

**[프롬프트]**

```
Implement a robust search feature for [describe content type] with filtering, sorting, and highlighting of matched terms. Include typeahead suggestions, recent searches, and proper handling of no-results scenarios.
```

**[분석]**

* **목적:** 고성능·사용성 중심 검색 UX 제공
* **범위:** 쿼리 파서, 서버/클라이언트 필터, 정렬 키 인덱스, 하이라이트(워드 경계)
* **산출물:** 검색 API, 제안(Typeahead) 엔드포인트, 최근 검색 저장/삭제, 빈 결과 UX
* **체크리스트:** 부분 일치 vs prefix 인덱스, Trigram/GIN, stopword/스테밍, XSS-safe 하이라이트, 성능 가드레일(limit/timeout)

---

#### 데이터 테이블 그리드 구현

**[프롬프트]**

```
Create a data table/grid for [describe data] with sorting, filtering, pagination, column resizing, and row selection. 

Include features for exporting data and customizing visible columns.
```

**[분석]**

* **목적:** 대용량 데이터 탐색·조작 UI 표준화
* **범위:** 서버/클라 페이징, 정렬/필터 상태, 컬럼 가시성/폭 제어, 선택 상태 관리
* **산출물:** 재사용 가능한 Table 컴포넌트, CSV/Excel 내보내기, 상태 영속(LocalStorage/URL)
* **체크리스트:** 가상 스크롤, 접근성 그리드 롤, Sticky 헤더, 열 정의 타입 안전성, export 시 권한 필터

---

#### 데이터 임포트/익스포트 시스템

**[프롬프트]**

```
Build a system for importing and exporting [describe data] in various formats (CSV, JSON, etc.). 

Include validation, progress indicators, error handling, and the ability to map fields during import.
```

**[분석]**

* **목적:** 대량 데이터 온보딩/백업 파이프라인
* **범위:** 스키마 검증, 미리보기, 필드 매핑, 부분 실패 리포트, 트랜잭션/배치
* **산출물:** 업로드 파서, 매핑 UI, 에러 CSV, 진행률 표시(Chunked)
* **체크리스트:** 인코딩/구분자 처리, 대용량 스트리밍, 중복 키 정책, 롤백/부분 커밋 전략, 감사 로그

---

#### 대시보드 차트 구현

**[프롬프트]**

```
Create a set of interactive charts for [describe data/metrics] using Recharts. 

Include different visualization types (bar, line, pie), time period selection, drill-down capabilities, and responsive behavior.
```

**[분석]**

* **목적:** KPI 가시화 + 탐색형 인터랙션 제공
* **범위:** 시계열/범주형 차트, 기간 선택, 드릴다운(계층/디테일), 반응형 레이아웃
* **산출물:** 차트 컴포넌트 세트, 툴팁/줌/브러시, 데이터 어댑터
* **체크리스트:** 빈 데이터 처리, 축 포맷(로케일/단위), 접근성 대체 텍스트, 성능(메모이제이션/샘플링)

---

#### 오프라인 동기화 전략

**[프롬프트]**

```
Implement a strategy for synchronizing offline data changes with a backend when connectivity is restored. 

Handle conflict resolution, optimistic UI updates, and provide visual indicators for sync status.
```

**[분석]**

* **목적:** PWA/불안정 네트워크 환경에서 데이터 일관성 확보
* **범위:** IndexedDB/kv 저장, changeset 큐, 재동기화 스케줄러, 충돌 정책
* **산출물:** 오프라인 큐 엔진, 상태 배지(queued/syncing/failed), 재시도/백오프
* **체크리스트:** 멱등 키, 시퀀스 넘버/버전 필드, 서버 타임스탬프 우선, 배치 업로드

---

#### 멀티스텝 폼 위자드

**[프롬프트]**

```
Create a multi-step form wizard for collecting [describe data] with validation, progress tracking, the ability to save drafts, and a summary review before submission. 

Handle conditional form fields based on previous answers.
```

**[분석]**

* **목적:** 복잡 입력의 이탈 감소 및 데이터 품질 제고
* **범위:** 단계 라우팅, 조건부 필드, 실시간/최종 검증, 임시 저장(draft)
* **산출물:** Wizard 컴포넌트, 검증 스키마, 요약/확인 단계, 재개(resume) 기능
* **체크리스트:** 접근성(Form role/label), 오토세이브, 서버 검증 에러 매핑, 진행률 보정(조건부 단계)

---

워크플로우 관리
--------

효과적인 워크플로우 관리는 프로젝트의 성공적인 완성을 위해 필수적입니다. Git 연동, 테스팅 전략, 배포 파이프라인 등을 포함합니다.

**예시 프롬프트 - GitHub 연동 및 워크플로우:**

```
Connect this Lovable project to GitHub and set up a good workflow for contributions. 

Include branch protection rules, PR templates, and CI/CD workflow configuration with automatic preview deployments.
```

**한국어 번역:**

```
이 Lovable 프로젝트를 GitHub에 연결하고 기여를 위한 좋은 워크플로우를 설정하세요.

브랜치 보호 규칙, PR 템플릿, 자동 미리보기 배포가 포함된 CI/CD 워크플로우 구성을 포함하세요.
```

> 📝 **요청 분석**
>
> * **목적:** GitHub과 연동된 협업/배포 워크플로우 체계화
> * **조건:**
>   + 협업 프로세스 정립: 브랜치 전략, PR 템플릿, 리뷰 프로세스
>   + 자동화된 CI/CD 구성
>   + PR 시 자동 미리보기 배포 포함
>   + 브랜치 보호 규칙 설정
> * **요청:**
>   1. GitHub 연결 및 리포지토리 관리 설정
>   2. 브랜치 보호 규칙 정의
>   3. PR 템플릿 제공
>   4. CI/CD 파이프라인 구성 → 자동 테스트/배포
>   5. PR마다 Preview 환경 자동 배포

### 추가 프롬프트

#### 컴포넌트 리팩터링

**[프롬프트]**

```
Refactor this large component into smaller, more manageable components: 
[paste component]. 

Extract reusable parts, implement proper prop passing, maintain state management, and ensure the refactoring doesn't break existing functionality.
```

**[분석]**

* **목적:** 복잡도 감소·재사용성 향상·테스트 용이성 확보
* **범위:** UI/비즈 로직 분리, 하위 컴포넌트 추출, props/컨텍스트 정리, 효과/메모·성능 최적화
* **산출물:** 분리된 컴포넌트 트리, 스토리북/테스트, 변경 영향도 체크리스트
* **체크리스트:** 동등 렌더 보장(Snapshot/Playwright), 상태 상향/하향 전략, 이벤트 버블링 유지, CSS scope 안전

---

#### 테스트 전략 수립

**[프롬프트]**

```
Suggest a testing strategy for [component/feature] including what to test and how. 

Include unit tests for business logic, integration tests for data flow, and UI tests for critical user flows with best practices for mocking dependencies.
```

**[분석]**

* **목적:** 리스크 기반 커버리지 확보와 회귀 방지
* **범위:** 단위(순수 로직), 통합(API/스토어), E2E(핵심 플로우), 목킹/픽스처 표준
* **산출물:** 테스트 피라미드, 샘플 테스트, 커버리지 목표, CI 연동
* **체크리스트:** 시나리오 명세서→테스트 케이스 추적성, flaky 방지, 테스트 데이터 격리, 성능/접근성 smoke

---

#### 비동기 함수 에러 처리 강화

**[프롬프트]**

```
Implement comprehensive error handling for this async function: 
[paste function]. 

Include retry logic, fallback mechanisms, proper error reporting, user-friendly error messages, and logging for debugging purposes.
```

**[분석]**

* **목적:** 장애 내성·관측 가능성 강화
* **범위:** 재시도(backoff/jitter), 폴백(캐시/대체 경로), 사용자 메시지/토스트, 구조화 로깅
* **산출물:** 강화된 함수, 에러 카탈로그(분류/코드), 로거/트레이서 훅, 알림 연동
* **체크리스트:** 타임아웃/취소, 동등 에러 합치기, PII 비노출, SLO/알람 기준

---

#### 배포 파이프라인 구축

**[프롬프트]**

```
Set up a deployment pipeline for this application that includes staging and production environments, automatic database migrations, environment-specific configurations, and rollback capabilities.
```

**[분석]**

* **목적:** 예측 가능한 배포와 신속한 롤백
* **범위:** 환경 분리(.env/secret), 마이그레이션 자동 적용/검증, 헬스체크/카나리
* **산출물:** CI/CD 정의, 마이그레이션 스텝, 롤백 스크립트/스냅샷, 배포 체크리스트
* **체크리스트:** 데이터 마이그레이션 안전망(락/배치/리허설), feature flag, 관측(로그/메트릭/트레이스), DB 스키마 호환성(blue-green)

---

#### 사용자 플로우 분석 및 최적화

**[프롬프트]**

```
Analyze and optimize this user flow: [describe flow]. 

Suggest improvements for user experience, reduce friction points, implement progressive enhancement, and ensure accessibility throughout.
```

**[분석]**

* **목적:** 전환율·완료율 개선 및 이탈 감소
* **범위:** 퍼널 분석, 마찰 지점 추출, 단계 축소/자동완성, 점진적 향상(자바스크립트 비활성 시 폴백)
* **산출물:** 개선 제안서(AS-IS/TO-BE 플로우), 와이어프레임, 실험 설계(A/B), 접근성 점검표
* **체크리스트:** 입력 최소화, 오류 복구 UX, 로딩 인디케이터/낙관적 UI, 키보드/리더 대응, 계측 이벤트 정의

---

Chat 모드 vs Default 모드 사용법
-------------------------

### 언제 사용하나요?

* Lovable에는 프롬프트를 위한 두 가지 모드가 있습니다:

  + **Default 모드**(프로젝트에 즉시 변경사항을 적용)
  + **Chat 전용 모드**(당신이 지시할 때까지 코드를 변경하지 않고 대화와 같은 방식)
* 각각을 언제 사용할지 아는 것은 워크플로우를 간소화할 수 있습니다.
* **직접적인 코딩 작업**에는 `Default`를, **브레인스토밍**, **디버깅**, 또는 **실행하기 전에 변경사항을 논의**하고 싶을 때는 `Chat 모드`를 사용하세요.

### 사용 방법

* **Default 모드**는 구축하거나 만들고자 하는 잘 정의된 기능이 있을 때 좋습니다.

  + 지시를 내리면 Lovable이 가능하다면 한 번에 수행합니다.
* 반면 **Chat 모드**는 코드베이스를 즉시 변경하지 않고 앞뒤로 대화하거나 분석하고 싶을 때("이것이 왜 작동하지 않나요?" 또는 "X를 하는 가장 좋은 방법은 무엇인가요?"와 같은 질문) 유용합니다.

  + Chat 모드에서 AI는 분석이나 계획으로 응답하며, 준비가 되었을 때 보통 명시적으로 "진행해서 구현하세요"라고 말해야 합니다.

이러한 도구들을 효과적으로 활용하면 AI와 더 나은 협업을 통해 고품질의 애플리케이션을 개발할 수 있습니다.  
각 상황에 맞는 적절한 프롬프트 전략을 선택하여 개발 효율성을 극대화하세요.

---

지식 베이스 및 PRD 작성
---------------

### 언제 사용하나요?

프로젝트 시작 시와 단일 프롬프트에 담을 수 있는 것보다 더 많은 컨텍스트를 AI에게 제공해야 할 때 사용합니다. Lovable에서 **지식 베이스**는 프로젝트 설정의 특별한 공간으로, 배경 정보, 요구사항, 프롬프트 전반에 걸쳐 지속되는 가이드라인을 저장할 수 있습니다. **프로젝트 요구사항 문서(PRD)**는 앱의 목적과 사양에 대한 포괄적인 요약으로, 본질적으로 구축하고 있는 것의 청사진입니다.

### 사용 방법

프로젝트에 대한 핵심 정보로 Lovable의 지식 베이스를 채우는 것부터 시작하세요. 여기에는 다음이 포함될 수 있습니다:

* **개요 및 목표**: 프로젝트가 무엇이고 해결하는 문제
* **사용자 플로우**: 사용자가 앱을 탐색하거나 사용하는 방법에 대한 설명
* **핵심 기능 및 범위**: 범위 내 기능들 (그리고 기능 확장을 피하기 위해 범위 외 항목들도 언급)
* **기술 스택**: 사용할 기술, API, 서비스들
* **디자인 가이드라인**: 특정 UI/UX 지침 - 브랜딩, 색상 스키마, 레이아웃, 접근성 요구사항
* **백엔드 세부사항**: 데이터 모델, 핵심 데이터베이스 테이블, Stripe나 Supabase와 같은 통합 개요

**예시 프롬프트 - 지식 베이스 활용:**

```
User: 
Before you write any code, please review the Knowledge Base and share your understanding of my project.

AI (likely response): 
"Sure. Based on the Knowledge Base: You're building a task management app for teams. The app flow is Users sign up -> see a dashboard -> create projects and tasks. The tech stack is Next.js for frontend, Supabase for backend (authentication and database). Core features include project creation, task assignments, and a reporting dashboard. In-scope features: task CRUD, user roles, email notifications; Out-of-scope: real-time collaboration. The design should follow a clean corporate style with Tailwind CSS, and it needs to be responsive. Backend uses Supabase with row-level security for multi-tenant data separation..."
```

**한국어 번역:**

```
사용자:
코드를 작성하기 전에, 지식 베이스를 검토하고 내 프로젝트에 대한 이해를 공유해주세요.

AI (예상 응답): 
"물론입니다. 지식 베이스에 따르면: 팀을 위한 작업 관리 앱을 구축하고 있습니다. 앱 플로우는 사용자 가입 -> 대시보드 보기 -> 프로젝트 및 작업 생성입니다. 기술 스택은 프론트엔드용 Next.js, 백엔드용 Supabase(인증 및 데이터베이스)입니다. 핵심 기능은 프로젝트 생성, 작업 할당, 보고 대시보드를 포함합니다. 범위 내 기능: 작업 CRUD, 사용자 역할, 이메일 알림; 범위 외: 실시간 협업. 디자인은 Tailwind CSS로 깔끔한 기업 스타일을 따라야 하며, 반응형이어야 합니다. 백엔드는 다중 테넌트 데이터 분리를 위한 행 수준 보안과 함께 Supabase를 사용합니다..."
```

이런 종류의 AI 요약은 사양을 올바르게 흡수했음을 확인해줍니다. 만약 무언가를 오해했다면, Chat 모드에서 수정할 수 있습니다. 확인되면, (AI가 이제 전체 계획을 "알고" 있는 상태로) 구축을 진행합니다.

PRD 작성과 지식 베이스 채우기는 추가적인 사전 작업처럼 느껴질 수 있지만, **개발 전반에 걸쳐 큰 배당금을 지급**합니다. AI가 항상 앱이 무엇을 해야 하는지에 대한 참조를 가지고 있기 때문에 오류와 AI 환각을 줄입니다. 한두 개의 프롬프트로 구축할 수 없는 더 큰 프로젝트에 특히 도움이 됩니다. 이를 머릿속에 있는 것과 동일한 이해로 AI를 시드하는 것으로 생각하세요.

마지막으로, 프로젝트가 발전함에 따라 지식 베이스를 유지하세요. 주요 기능을 추가하거나 범위를 변경한다면, PRD/지식 베이스 문서를 업데이트하세요. 이렇게 하면 향후 프롬프트가 새로운 정보를 고려할 것입니다. 매번 컨텍스트를 다시 설명하는 것보다 훨씬 쉽습니다. 본질적으로, 지식 베이스 + PRD는 당신의 AI 프로젝트 핸드북입니다 - 구축하고 있는 것과 방법에 대해 모든 사람(당신과 AI)이 같은 페이지에 있도록 유지합니다.

---

결론
==

Lovable의 프롬프트 라이브러리는 AI 기반 개발에서 효율성과 정확성을 극대화하기 위한 실용적인 가이드입니다. 각 시나리오별로 최적화된 프롬프트 패턴을 활용하면, 개발 과정에서 발생할 수 있는 오류를 최소화하고 원하는 결과를 더 빠르게 달성할 수 있습니다.

프로젝트 시작부터 배포까지, 이러한 프롬프트 전략들을 상황에 맞게 적절히 활용하여 AI와의 협업을 통해 고품질의 애플리케이션을 개발하세요. 특히 지식 베이스와 PRD를 체계적으로 관리하면, 프로젝트 전반에 걸쳐 일관된 방향성을 유지할 수 있습니다.

효과적인 프롬프트 작성은 단순히 명령을 내리는 것이 아니라, AI와의 원활한 소통을 통해 개발 목표를 달성하는 것입니다. 이 가이드의 패턴들을 참고하여 여러분만의 효율적인 개발 워크플로우를 구축해보세요.