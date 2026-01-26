---
title: "[Tips] Lovable Vibe-Coding Best Practices"
date: "2025-08-18"
tags:
  - "Lovable"
  - "vibe coding"
year: "2025"
---

# [Tips] Lovable Vibe-Coding Best Practices


Lovable을 최대한 활용하는 방법
====================

![](https://velog.velcdn.com/images/euisuk-chung/post/235801b0-6450-47ff-926d-44a00a09fd4c/image.png)

이 가이드는 신규 사용자와 숙련된 사용자 모두가 Lovable에서 빠르게 작업을 시작하고 일반적인 함정을 피하는 데 도움을 줍니다.

*본 가이드는 아래 **Lovable "Best Practices"** 사이트를 번역/정리한 내용입니다.*  
*참고 부탁드립니다.*

> ⭐ Check out original source ⭐  
> <https://docs.lovable.dev/tips-tricks/best-practice>

1. 기반 설정하기: Knowledge File 활용
-----------------------------

**왜 중요한가**: `Knowledge file`은 프로젝트의 두뇌입니다. 모든 프롬프트와 함께 전송되어 AI가 전체 맥락을 이해하는 데 도움을 줍니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/fd8e665a-bc6a-4dcf-8c9d-c5d9c2368ec7/image.png)

> <https://docs.lovable.dev/features/knowledge>

아래 그림과 같이 프로젝트가 따라야 할 기본적인 Ground Rule을 세팅해둘 수 있습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/92565adf-f211-41b6-abec-388f5042cb7f/image.png)

> <https://docs.lovable.dev/features/knowledge>

**포함할 내용**:

* 제품 비전 (PRD처럼 생각하세요)
* 사용자 여정과 페르소나
* 주요 기능과 기능성
* 디자인 시스템과 UI 가이드라인
* 역할별 행동 (예: Admin, User, Investor)

Lovable의 **Chat 모드**를 사용하면, Knowledge file을 자동 생성할 수 있습니다:

```
# 영문 프롬프트
Generate knowledge for my project at T=0 based on the features I’ve already implemented.
```

> 💡 (참고) "**my project at T=0**"이란?
>
> * `T=0`은 시점 0, 즉 현재 시점을 의미합니다. 이는 소프트웨어 개발과 버전 관리에서 사용되는 시간 표기법입니다:
>   + `T=0`: 현재 상태 (지금 이 순간의 프로젝트)
>   + `T-1`: 한 단계 이전 상태
>   + `T-2`: 두 단계 이전 상태
>   + `T+1`: 다음 단계 예정 상태
> * Lovable에서는 모든 편집이 커밋(commit)으로 저장되기 때문에, 각 버전을 시간 순서로 참조할 수 있습니다.

```
# 한글 프롬프트
이미 구현한 기능을 바탕으로 T=0에서 내 프로젝트에 대한 knowledge를 생성해주세요.
```

2. 프롬프트 작성 모범 사례
----------------

> Clear, verbose prompts = better output

**"명확하고 상세한 프롬프트 = 더 나은 결과물"**을 의미합니다. AI를 엔지니어링 파트너처럼 생각하세요—당신이 말하는 것만 알 수 있습니다.

**프롬프트 작성 팁**:

* **구체적으로 작성**: 정확한 페이지(예: /dashboard)와 예상되는 동작을 언급하세요.
* **자연어 사용**:

```
# 영문 프롬프트 
I want users with the role Investor to access this component, but not Admins.
```

```
# 한글 프롬프트
Investor 역할의 사용자는 이 컴포넌트에 접근할 수 있지만, Admin은 접근할 수 없도록 해야 합니다.
```

* **스크린샷 추가**: 특히 버그나 UX 이슈를 설명할 때 유용합니다.  
  (*eg. 특정 컴포넌트를 제공하며, 여기 OOO하게 변경해줘.*)
* **가드레일 추가**: AI에게 건드리지 말아야 할 것을 알려주면, 이를 고려하여 수정을 진행합니다.  
  (*eg.해당 경로에 있는 파일들은 변경하지마.*)

```
# 영문 프롬프트
Do not edit /shared/Layout.tsx.
```

```
# 한글 프롬프트
/shared/Layout.tsx는 편집하지 마세요.
```

* **중요한 지시사항을 프롬프트 전반에 반복**.

  + AI의 메모리는 제한적일 수 있기때문에, 정말 중요한 지시사항이라면, 채팅에 계속 언급/작성해주면 좋습니다.
* **한 번에 5가지를 구현하려고 하지 마세요**.

  + 작업을 **더 작고 테스트 가능한 작은 덩어리들**로 나누어서 구현을 요청하면 좋습니다.
  + 이때 각 블록 사이에 Chat Mode를 사용하여 검증을 수행한 뒤에 다음 단계로 넘어가기 전에 검증하는 것을 추천합니다.

**(예시) 기능 분해 템플릿**:

```
# 영문 프롬프트
**Feature Breakdown Template:**
Create the new page
Add UI layout
Connect the data
Add logic + edge cases
Test per role
```

```
# 한글 프롬프트
1. 새 페이지 생성
2. UI 레이아웃 추가
3. 데이터 연결
4. 로직 + 엣지 케이스 추가
5. 역할별 테스트
```

앱에 사용자별로 여러 역할(예: **Admin**, **Investor**, **Startup**)이 구분/정의되어 있다면, **항상 요청하는 프롬프트가 어떤 역할에 적용되는지 정의**하세요.

* 이는 공유 로직/컴포넌트로 인한 버그를 방지하는데 도움이 됩니다.

```
# 영문 프롬프트
As an Investor, I want to view the company dashboard, but I shouldn’t be able to edit it.
Please isolate this feature to the Investor role only.
```

```
# 한글 프롬프트
Investor로서, 회사 대시보드를 보고 싶지만 편집할 수는 없어야 합니다. 
이 기능을 Investor 역할에만 격리해주세요.
```

3. Chat Mode를 자주 활용하기
---------------------

`Chat mode`는 당신의 **AI Co-pilot(부조종사)**입니다.

* 준비가 될 때까지(원하는 요청이 나올때까지) 코드를 편집하지 않고 디버그, 브레인스토밍, 구현 계획을 세우는 데 도움을 줍니다.

**Chat Mode로 전환해야 할 때**:

* 2-3번의 "Try to Fix" 시도가 실패한 후
* 복잡한 로직이나 데이터베이스 이슈를 디버깅할 때
* 새로운 기능을 계획할 때

```
Suggest 3 ways to implement [X]
```

```
[X]를 구현하는 3가지 방법을 제안해주세요.
```

**워크플로우 팁**:

* 일부 사용자는 시간의 60-70%를 Chat Mode에서 보내는 것을 선호합니다.
* 완전히 만족할 때만 "계획 구현하기"를 클릭하세요.

**만약 초반에, Chat mode를 사용하는 것을 잊었다면**,  
아래 형식으로 LLM에게 요청하여 출력 일관성을 개선하고 부수적인 편집을 방지할 수 있습니다.

```
On page /settings, implement [feature]. The expected behavior is [XYZ]. 
Please don’t touch component A, layout B, or shared logic unless necessary. 
Follow best practices from Tailwind / Supabase / X.
```

```
/settings 페이지에서 [기능]을 구현해줘. 
예상되는 동작은 [XYZ]야. 필요하지 않다면 컴포넌트 A, 레이아웃 B, 또는 공유 로직은 건드리지 말아줘. 
Tailwind / Supabase / X의 모범 사례를 따라줘.
```

**원치 않는 코드 실행을 방지하려면:**  
아래 형식으로 LLM에게 요청하여, 코드 실행을 방지할 수 있습니다.

```
Investigate but don’t write code yet.
조사는 하되 아직 코드는 작성하지 마세요.
```

```
Suggest 3 ways to solve this without changing anything.
아무것도 변경하지 않고 이것을 해결하는 3가지 방법을 제안해주세요.
```

이런식으로 변경을 사전에 방지하여, 제어권을 유지할 수 있습니다.

또한, **AI가 "루프"에 빠졌을 때**,  
끝없는 버그 수정 사이클을 피하기 위해 다음 순서를 사용할 수 있습니다:

1. Chat mode로 전환
2. 오류 스크린샷 캡쳐해서 붙여넣기
3. 다음과 같이 말하기:

```
Please investigate this without breaking other features. 
If needed, revert to the last working version and fix from there.
```

```
다른 기능을 망가뜨리지 않고 이것을 조사해주세요. 
필요하다면 마지막 작동 버전으로 되돌리고 거기서부터 수정해주세요.
```

4. Supabase의 일반적인 함정 피하기
------------------------

Supabase는 **Firebase의 오픈소스 대안**으로, PostgreSQL 기반 데이터베이스와 실시간 기능을 제공하는 백엔드 서비스입니다.

* 단순히 데이터 저장소 역할을 넘어, **사용자 인증(User Authentication)**, **파일 스토리지(File Storage)**, **실시간 업데이트(Real-time Updates)**, 그리고 **서버리스 함수(Edge Functions)**까지 통합적으로 지원합니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/c86ca3b7-2103-489e-bf86-bf817b28d05b/image.png)

> <https://supabase.com/>

Lovable과 연동하면 이 기능들을 별도의 **서버 설정이나 보일러플레이트 코드 없이 바로 활용**할 수 있습니다.

* 예를 들어, *“피드백 폼을 추가하고 제출된 데이터를 DB에 저장해줘”*라고 요청하면, Lovable은 UI 폼을 만들고 동시에 Supabase에 해당 데이터를 저장할 테이블까지 자동으로 세팅합니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/39385f0b-6274-4d44-8820-de08156a6a16/image.png)

> <https://docs.lovable.dev/integrations/supabase>

Supabase는 분명히 강력하고 편리한 도구이지만, 그렇다고 해서 마냥 안심하고 써도 된다는 뜻은 아닙니다. 실제 서비스 환경에서는 몇 가지 주의해야 할 점들이 있습니다.

💡 **주의사항**

* Supabase는 한 번 연결하면 깔끔하게 되돌리기가 어렵습니다.
* 특히 버전을 되돌리는 과정에서 데이터베이스 스키마가 깨지거나 자동 생성된 관계가 무너질 수 있습니다.

💯 **모범 사례**

* 프론트엔드 구조가 어느 정도 안정된 이후에 Supabase를 연결하는 것이 안전합니다.
* 부득이하게 되돌려야 한다면, 단순히 수동 롤백하기보다는,
  + **AI 프롬프트를 통해 스키마 복원이나 마이그레이션을 유도**하는 방식이 훨씬 효과적입니다.

```
Please validate the SQL schema at T=0 and ensure no breaking changes have occurred.
```

```
T=0에서 SQL 스키마를 검증하고 파괴적인 변경사항이 없었는지 확인해주세요.
```

* 위 프롬프트를 적용하고, 이를 게시하기 전에 항상 데이터베이스 연결 기능을 테스트

5. 빠른 UI 수정을 위한 Visual Edit 사용
------------------------------

앱을 만들다 보면 코드 수정이나 프롬프트 호출까지는 필요 없지만, 버튼 색상이나 제목 문구처럼 **작은 UI 요소를 빠르게 고치고 싶을 때**가 많습니다. 이럴 때 바로 활용할 수 있는 기능이 **Lovable의 Visual Edit**기능입니다.

`Visual Edit`은 프로젝트 화면에서 **원하는 요소를 직접 클릭해 즉시 수정할 수 있는 도구**로, `텍스트`·`색상`·`폰트`·`레이아웃 조정`과 같은 단순한 변경에 적합합니다.

* 특히 무료로 제공되고, 크레딧이 차감되지 않으며, 실행 취소까지 가능해 부담 없이 사용할 수 있다는 장점이 있습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/418a2d59-23db-4306-b44e-d12e1b6c24dc/image.png)

> <https://docs.lovable.dev/features/visual-edit>

다음과 같은 경우 프롬프트 대신 Visual-edit을 사용하면 좋습니다:

* 텍스트, 색상, 폰트, 레이아웃 조정 변경
* 여러 작은 요소를 한 번에 편집
* 안전하고 크레딧 없는 커밋 (실행취소 가능)

6. GitHub + 버전 관리를 현명하게 사용
--------------------------

Lovable에서 일어나는 모든 편집은 곧 하나의 **Git 커밋**이라고 생각할 수 있습니다.

* 따라서 안정적인 상태를 보장하기 위해서는 GitHub와의 통합을 적극 활용하는 것이 중요합니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/4ae98ab9-be73-4299-89d1-9733ddbe7035/image.png)

> <https://docs.lovable.dev/integrations/github>

* **북마크(Bookmarks)로 안정 버전 표시**

  + GitHub의 태그(tag)와 비슷하게, Lovable에서는 **북마크** 기능을 통해 안정적인 버전을 눈에 띄게 표시할 수 있습니다.
  + 기능이 정상 동작하는 시점에 북마크를 걸어두면, 이후 문제가 생겼을 때 비교·복구가 훨씬 수월합니다.
  + GitHub에서도 해당 시점을 기준으로 쉽게 revert할 수 있기 때문에, 안전한 개발 사이클을 유지하는 데 유용합니다.
* **변경 비교**: 버전 간 차이를 확인하고 싶을 때는 AI에게 직접 비교를 요청할 수 있습니다.

  + 예를 들어:

    ```
    Compare version at T–1 to T–0. What changed? What might be breaking?
    ```

    ```
    T-1 버전과 T-0을 비교해줘. 무엇이 변경되었고, 무엇이 망가졌을 수 있을까?
    ```
  + AI가 변경 내역을 요약해주기 때문에, 필요 시 안정된 버전으로 되돌아가는 판단이 빨라집니다.
* **GitHub 통합의 장점**: Lovable은 프로젝트를 자동으로 GitHub 저장소와 동기화합니다.

  + *버전 히스토리 & 백업*:
    - 모든 코드 변경은 Git에 기록되어 언제든 과거 상태로 되돌릴 수 있고, GitHub가 외부 백업 역할을 합니다.
  + *팀 협업*:
    - 개발자는 브랜치·PR·리뷰를 활용하고, 비개발자도 코드 변경 내역을 투명하게 확인할 수 있습니다.
  + *실시간 동기화*:
    - Lovable에서 발생한 커밋은 즉시 GitHub에 push되고, GitHub에서 push한 변경도 곧바로 Lovable에 반영됩니다.
  + *워크플로우 통합*:
    - GitHub Actions, Issues, CI/CD를 그대로 쓰면서도 Lovable의 AI 기능을 병행할 수 있습니다.
  + *배포 유연성*:
    - GitHub에 코드가 있으므로, Lovable 외부 인프라로도 자유롭게 배포 가능합니다.
* **브랜치 사용 주의**

  + Lovable은 GitHub의 **기본 브랜치(main/master)**만 추적합니다.
  + 따라서 기능 개발은 GitHub에서 별도의 브랜치로 진행하되, 최종적으로 main에 merge해야 Lovable과 동기화됩니다.

7. 모든 방법이 실패하면, Remix
---------------------

많은 사용자가 깨닫는 것: 두 번째에는 모든 것을 다시 하는 것이 더 적은 시간이 걸립니다.

🔁 **Remix**는 현재 프로젝트의 상태를 그대로 복제하여 새로운 사본을 만드는 기능입니다.

* 원본은 그대로 보존하면서, 복제된 프로젝트에서 새로운 시도를 해볼 수 있다는 점이 핵심입니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/48b7dc9e-720e-4440-a1fd-dc149ef5216b/image.png)

**Remix**는 사실상 “*T=0에서 프로젝트의 깨끗한 사본을 다시 시작하는 것*”으로,

* 기존의 ChatHistory 없이,
* 더 나은 프롬프트와 명확한 knowledge를 바탕으로 재구축하거나,
* 이전 프로젝트를 참조용으로 두고 새 버전을 발전시킬 수 있습니다.

**사용 사례**

* 버그 루프에 갇혀 더 이상 진행이 어렵다고 느낄 때
* 기존 히스토리를 보존한 채, 깨끗하게 다시 시작하고 싶을 때
* Supabase 연결을 해제하고 새로운 데이터 경로로 전환해야 할 때

**Remix 하는 방법**

1. **Project Settings**로 이동  
   ![](https://velog.velcdn.com/images/euisuk-chung/post/982b7c16-c338-42a3-ba5a-e3f1672f65f6/image.png)
2. **Remix** 옵션 선택
3. 현재 워크스페이스에 원본과 동일한 사본이 생성되며, 이 **사본은 독립적으로 수정 가능**합니다.

> (참고) 내 프로젝트뿐 아니라 **다른 사용자의 공개 프로젝트**도 Remix할 수 있습니다.

**중요 제약 사항**

* (보안상의 이유로) Supabase가 연결된 프로젝트는 Remix할 수 없습니다.
* Remix는 원본 프로젝트를 덮어쓰지 않고 새로운 사본만 만듭니다.

8. 인내심을 갖고 침착하게
---------------

AI는 어떤 순간에는 마법처럼 느껴지지만, 또 어떤 순간에는 답답하고 좌절스러울 수 있습니다.

* 특히, 모든 빌드의 마지막 5%는 종종 가장 느리게 진행되지만, 그만큼 가장 중요한 부분이기도 합니다.

> 💡 **황금 규칙**:
>
> * 프롬프트에 시간을 들이세요.
> * 모든 것을 다시 확인하세요.
> * 작업을 작고 테스트 가능한 블록으로 나누세요.
> * 입력이 정확할수록 출력이 더 좋아집니다.

9. 문서 사용 및 도움 요청
----------------

![](https://velog.velcdn.com/images/euisuk-chung/post/c8190a7a-dd4f-4679-b39b-e06d4e72935b/image.png)

> <https://docs.lovable.dev/introduction/welcome>

* Lovable 공식 문서에는 워크스루, 템플릿, SEO 팁, 통합 등이 포함되어 있습니다.
  + 문서 AI 어시스턴트에서 직접 질문할 수 있습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/c527dfd1-c378-487b-a0e8-74d348b7f236/image.png)

10. 보너스 팁
---------

* 긴 프롬프트를 입력할 때는 **음성 받아쓰기**를 활용해보세요.

  + 예: Mac에서는 마이크 입력으로 긴 프롬프트를 빠르게 작성 가능
  + 이는 긴 요청사항을 정리하면서, 피곤하거나 답답할 때 특히 유용합니다.
* "`나는 좌절하고 있어...(I am frustrated…)`"라는 프롬프트 패턴을 활용하면, 내가 막힌 부분에 대해 AI가 더 집중해서 대응할 수 있습니다.
* 큰 편집을 한 뒤에는 반드시 **여러 역할(Role)과 그 동작**을 다시 확인하세요. 특히 조건부 로직이 들어간 경우는 꼼꼼한 점검이 필수입니다.
* 안정된 버전을 **북마크(Bookmarks)**로 저장해 두면 빠른 디버깅이 가능합니다.
* 예상치 못한 부작용이 보인다면, 지나치게 **일반적인 로직** 때문에 생긴 버그일 가능성이 높습니다.
* 특정 역할을 위해서는 **전용 컴포넌트**를 만드는 것이 좋습니다.

  + 범위가 명확히 정의되지 않은 경우, 공유 컴포넌트를 재사용하는 것은 피하세요.

다음에도 바이브 코딩 팁 시리즈로 찾아뵙겠습니다 :)  
읽어주셔서 감사합니다 😸