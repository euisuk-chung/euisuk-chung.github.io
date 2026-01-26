---
title: "[Lovable] 코딩 없이 웹/앱 만들기 : Lovable 완전 가이드"
date: "2025-06-08"
year: "2025"
---

# [Lovable] 코딩 없이 웹/앱 만들기 : Lovable 완전 가이드


🎨 마치 그림 그리듯, 말로만 설명하면 웹사이트가 완성된다면 어떨까요?

> 💭 **“사용자 로그인 화면이 필요해요.”**  
> 💭 **“포트폴리오 갤러리와 연락처 폼도 추가해 주세요.”**

이렇게 말하면 실제 웹 앱이 만들어집니다.

믿기 어려우시죠? 이 모든 걸 가능하게 만드는 도구가 바로 오늘 소개할 **Lovable.dev**입니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/259afffe-60fb-4fc6-8b1f-e16b730b6436/image.png)

> <https://lovable.dev/>

오늘 소개할 Lovable은 그런 상상을 현실로 바꾸는 **AI 기반 웹앱 빌더**입니다. 누구나, 지금 바로, ‘진짜 작동하는 웹앱’을 만들 수 있게 해줍니다.

최근 AI의 발전은 **노코드(No-Code)** 도구의 지형을 완전히 바꾸고 있습니다.

* 특히, **Lovable**은 텍스트 프롬프트만으로도 **완전한 웹 애플리케이션**을 만들어낼 수 있는 AI 기반 앱 빌더입니다.
* 개발자뿐만 아니라 비개발자도 손쉽게 사용할 수 있어, **MVP(Minimum Viable Product)** 제작이나 **사이드 프로젝트**를 빠르게 시작하고 싶은 분들에게 매우 유용합니다.

---

> ✍️ **참고:** 본 블로그는 Lovable의 공식 문서와 퀵스타트 가이드, Supabase 연동 방법, 실제 예제 등을 바탕으로 작성되었습니다.

🌟 그래서 Lovable이 뭔데?
------------------

**Lovable**은 사용자가 간단한 텍스트 설명만으로도 웹사이트와 웹 애플리케이션을 만들 수 있도록 도와주는 **AI 기반의 노코드 앱 빌더**입니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/fb1e9b2b-664b-4690-aba0-bd913f94149e/image.png)

> <https://docs.lovable.dev/user-guides/quickstart>

기존의 코드 작성 방식과는 달리, 복잡한 HTML, CSS, JavaScript에 대한 지식이 없어도 누구나 웹 앱을 만들 수 있습니다.

Lovable은 다음과 같은 기술 스택을 바탕으로 작동합니다:

* **React**: 사용자 인터페이스 구성

![](https://velog.velcdn.com/images/euisuk-chung/post/c5161b06-b401-4931-8882-0cf9d77dfcbe/image.png)

> <https://ko.legacy.reactjs.org/>

* **Tailwind CSS**: 빠르고 직관적인 스타일링

![](https://velog.velcdn.com/images/euisuk-chung/post/89d18309-de23-4b6e-bb15-895ef47f2048/image.png)

> <https://tailwindcss.com/>

* **Vite**: 빠른 개발 환경

![](https://velog.velcdn.com/images/euisuk-chung/post/5efa895e-b5f6-41bd-a54d-1e406b8a6838/image.png)

> <https://vite.dev/>

* **Supabase**: 백엔드 기능 및 데이터베이스

![](https://velog.velcdn.com/images/euisuk-chung/post/1093fcdc-baac-4b8f-a7ce-814dc1537c4d/image.png)

> <https://supabase.com/>

이를 통해 Lovable은 다음과 같은 기능을 제공합니다:

* **프롬프트 기반 앱 생성**: 텍스트만으로 구성 가능한 UI와 로직
* **실시간 코드 편집**: 내부 에디터 제공 및 GitHub 연동
* **외부 API 및 서비스 통합**: Supabase, Stripe, Resend 등
* **자동 배포**: 클릭 한 번으로 앱을 배포할 수 있음
* **시각 편집 도구**: Select & Visual Edit으로 상세 조정 가능
* **한글 완전 지원**: 입력, 출력, UI 전부 한국어 대응

---

🏗️ 어떻게 작동하나요? – 웹사이트 제작 4단계
---------------------------

Lovable을 사용해 웹사이트를 만드는 과정은 단순하면서도 유연합니다. 다음은 기본적인 4단계 흐름입니다.

### 1단계: 회원가입 후 로그인

Lovable 공식 웹사이트(lovable.app 또는 lovable.dev)에 접속해 계정을 생성합니다.

* **무료 플랜**만으로도 기본적인 앱 생성과 배포가 가능합니다.
* **Pro 이상 플랜**에서는 GitHub 연동, 협업 기능, 커스텀 도메인 등 다양한 고급 기능을 사용할 수 있습니다.

| 항목 | Free (무료) | Pro 플랜 (월 $25~) | Teams 플랜 (월 $30~) |
| --- | --- | --- | --- |
| 가격 | 무료 | 월 $25부터 시작 | 월 $30부터 시작 |
| 월간 메시지 제한 | 없음 | 플랜에 따라 다름 | 플랜에 따라 다름 |
| 비공개 프로젝트 | 불가능 | 가능 (무제한) | 가능 (무제한) |
| Lovable 배지 | 항상 표시됨 | 제거 가능 | 제거 가능 |
| 커스텀 도메인 | 불가능 | 구매 및 연결 가능 | 구매 및 연결 가능 |
| 개발자 모드 (Dev Mode) | 불가능 | 코드 보기 및 수정 가능 | 코드 보기 및 수정 가능 |
| 편집자 수 | 1명 | 프로젝트당 2명 | 최대 20명 포함 |
| 프로젝트 관리 기능 | 불가능 | 불가능 | 중앙 집중형 청구 및 접근 관리 가능 |

> 출처: <https://docs.lovable.dev/>

### 2단계: 자연어로 프로젝트 설명

앱을 만들기 위한 첫 단계는 프롬프트 입력입니다.

예를 들어:

> "사용자 로그인 기능과 월별 매출 차트를 포함한 대시보드를 만들어줘. 고객 분포는 파이차트로 보여줘."

![](https://velog.velcdn.com/images/euisuk-chung/post/7ef4eab6-7e79-46dd-8e9e-db1e6c6a5f20/image.png)

이처럼 **구체적으로 입력할수록 더 정교한 결과를 얻을 수 있습니다**.

![](https://velog.velcdn.com/images/euisuk-chung/post/57d77057-419a-4593-a0e3-3f166dd52fde/image.png)

* 프롬프트는 언제든지 수정할 수 있으며, 이후 사용자 인터페이스나 백엔드 동작도 추가로 조정 가능합니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/8448425d-9cf9-4ab0-9153-deba221a7e29/image.png)  
**코드 작성 중~**

![](https://velog.velcdn.com/images/euisuk-chung/post/1d592e4e-8097-4479-bc4a-be47850d8117/image.png)  
**코드 작성 끝!**

![](https://velog.velcdn.com/images/euisuk-chung/post/f8e2d97b-307c-4402-9557-3be792bdc591/image.png)  
**이 집 코딩 잘하네...**

### 3단계: 생성된 코드 수정

Lovable은 코드를 자동으로 생성해주지만, 필요한 경우 **사용자가 직접 수정할 수 있도록 내부 편집기와 시각 편집 기능을 제공**합니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/2df7d41a-c057-4214-8f65-7f8bab70dd40/image.png)

> eg. 색상 변경 요청

그 외 다음과 같은 작업들이 가능합니다:

* Tailwind CSS 기반 스타일 수정
* 페이지 추가, 삭제
* 레이아웃 재구성
* 프롬프트 보완으로 기능 추가

또한 GitHub 연동을 통해 외부 IDE에서 코드를 관리할 수 있어, 개발자에게도 확장성이 뛰어난 구조를 제공합니다.

### 4단계: 배포

완성된 프로젝트는 클릭 한 번으로 바로 배포할 수 있습니다.

* Lovable의 기본 URL(`https://your-app.lovable.app`)을 통해 공개할 수 있으며, 커스텀 도메인을 등록해 브랜드화된 사이트 운영도 가능합니다.
* Netlify, Vercel, Namecheap 등의 플랫폼도 지원됩니다.

---

💡 예제: 설문조사 웹앱 만들기
-----------------

아래와 같은 프롬프트를 입력하면 설문조사 웹앱이 자동으로 생성됩니다:

**영문 요청**

```
Create a survey app that collects and stores response data.
The app should have:
- 3 multiple choice questions
- 1 open-ended text response
- A clean, modern form
- Submission validation and confirmation
```

> **(참고) 🔐 한글 완전 지원**  
> Lovable은 영어에 최적화된 도구처럼 보일 수 있지만, 실제로는 **한글도 매우 잘 지원**합니다.  
> 입력 프롬프트는 물론, UI 요소와 텍스트 콘텐츠 모두 한글로 작성이 가능하며, 프론트엔드 코드와 백엔드 데이터까지 완전히 한글 기반으로 관리할 수 있습니다.

아래와 같이 한글로 한번 요청해보겠습니다 ✍️

**한글 요청**

```
응답 데이터를 수집하고 저장하는 설문조사 앱을 만들어주세요.  
앱에는 다음과 같은 기능이 포함되어야 합니다:  
- 객관식 질문 3개 (선택형)  
- 주관식 질문 1개 (텍스트 입력형)  
- 깔끔하고 현대적인 디자인의 설문 양식  
- 모든 문항이 입력되었는지 확인하는 제출 유효성 검사 기능  
- 제출 완료 후 사용자에게 확인 메시지 출력
```

Lovable은 몇 초 내에 이 요구사항을 분석하고 다음과 같은 기능을 구현합니다:

* 라디오 버튼 형태의 객관식 질문
* 주관식 텍스트 필드
* 모든 질문 완료 시에만 제출 가능
* 제출 후 확인 메시지 출력

디자인은 미니멀하고 반응형이며, 모바일에서도 즉시 사용 가능한 형태로 렌더링됩니다.

**(예시) 예제 완성 샘플**

![](https://velog.velcdn.com/images/euisuk-chung/post/4b00c2b0-2df8-4c90-bcde-f5febc6e46b7/image.png)

여기에 추가적으로 채팅을 통해 디테일 추가 또는 수정을 하실 수 있습니다.

---

🔄 Supabase로 백엔드 연결
------------------

Lovable은 단순한 정적 페이지 생성기가 아닙니다.

Supabase와의 완벽한 통합을 통해 다음과 같은 **실제 데이터 연동**이 가능합니다:

* 사용자 인증 및 로그인
* DB에 설문 응답 저장
* 이메일 인증 및 알림 기능 추가
* Edge Functions 활용한 자동화 처리

Supabase 연동 절차는 다음과 같이 간단합니다:

1. Supabase에서 새 프로젝트 생성
2. `Lovable 대시보드` → `Settings` → `Connect Supabase 클릭`
3. Supabase API URL과 키를 입력해 연결
4. 데이터베이스 테이블 자동 생성 및 필드 매핑

또한, 사용자 인증 기능을 활성화하면 로그인/회원가입 UI도 자동으로 생성되며, 이메일 인증도 설정할 수 있습니다.

---

🧩 기타 고급 기능
----------

| 기능 | 설명 |
| --- | --- |
| GitHub 연동 | 생성된 코드를 GitHub 레포지토리에 자동 커밋하거나 외부 IDE로 편집 가능 |
| 이미지 인식 프롬프트 | 프롬프트에 스크린샷을 붙이면 시각적 구조를 인식해 앱 구조 자동 생성 |
| Custom Knowledge | 프로젝트의 핵심 개념/기능/디자인을 문서로 정리하여 AI가 프로젝트의 목적을 학습 |
| Select & Visual Edit | UI 요소를 선택하고 Tailwind 기반 속성값을 시각적으로 수정 가능 |
| 협업 기능 | 여러 사용자가 실시간으로 하나의 프로젝트를 편집 가능 (Pro / Teams 플랜 필요) |
| 버전 히스토리 관리 | Google Docs처럼 각 수정 내역 기록 및 이전 상태 복원, 중요 변경사항 북마크 가능 |

이러한 고급 기능은 단순한 웹사이트 제작을 넘어서 **진짜 서비스 수준의 앱을 구축**하는 데 필요한 모든 요소를 제공합니다.

---

✨ 지금 바로 Lovable 시작하기
--------------------

1. <https://lovable.app> 접속
2. 무료 계정 생성
3. 프롬프트 입력
4. 앱 생성 → 수정 → 배포!

Lovable은 웹앱 개발의 진입장벽을 확 낮춰주며, 프로그래밍에 익숙하지 않은 사람도 아이디어를 실제 제품으로 빠르게 구현할 수 있는 강력한 도구입니다.

> **누구에게 추천하나요?**

| 대상 | 이유 |
| --- | --- |
| 👩‍💻 예비 개발자 | 웹 개발 흐름을 체험하고 포트폴리오를 만들기에 이상적인 환경 |
| 🧪 스타트업 | MVP를 빠르게 제작하고 시장 반응을 확인할 수 있는 최적의 도구 |
| 📊 데이터 분석가 | 대시보드, 데이터 수집, 시각화 등 다양한 실험을 손쉽게 진행 가능 |
| 👩‍🏫 교육자 | 코딩 지식 없이도 수업용 실습 도구나 학습용 웹앱 제작에 활용 가능 |
| 🧑‍🎨 디자이너 | 디자인된 UI를 직접 앱 형태로 시각화하거나 프로토타입 배포 가능 |
| 🧑‍💼 기획자/PM | 아이디어를 문장으로 입력하여 빠르게 컨셉 앱을 제작하고 팀원들과 협업 가능 |

**코딩을 몰라도, 디자인을 몰라도, 웹 앱은 만들 수 있습니다.**  
지금 바로 Lovable을 통해 여러분만의 프로젝트를 시작해 보세요!

틈틈이 웹/앱 만들어보고 있는데 너무 재밌네요 😎

감사합니다!