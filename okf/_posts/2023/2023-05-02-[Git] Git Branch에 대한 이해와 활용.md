---
title: "[Git] Git Branch에 대한 이해와 활용"
date: "2023-05-02"
tags:
  - "git"
  - "개념정리"
  - "환경"
year: "2023"
---

# [Git] Git Branch에 대한 이해와 활용

Git Branch에 대한 이해와 활용
=====================

`Git Branch`는 Git에서 매우 중요한 개념 중 하나입니다.

이번 포스트에서는 Git Branch란 무엇인지, Git Branch를 활용하여 어떻게 코드를 관리할 수 있는지, 그리고 Git Branch를 활용한 협업 방법 등에 대해 살펴보겠습니다.

> * *"모든 버전 관리 시스템은 브랜치를 지원한다. 개발을 하다 보면 코드를 여러 개로 복사해야 하는 일이 자주 생긴다. 코드를 통째로 복사하고 나서 원래 코드와는 상관없이 독립적으로 개발을 진행할 수 있는데, 이렇게 독립적으로 개발하는 것이 브랜치다."*  
>   ↳ 출처 : [Git 브랜치 - 브랜치란 무엇인가](https://git-scm.com/book/ko/v2/Git-%EB%B8%8C%EB%9E%9C%EC%B9%98-%EB%B8%8C%EB%9E%9C%EC%B9%98%EB%9E%80-%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80)

1. Git Branch란?
---------------

![](https://velog.velcdn.com/images/euisuk-chung/post/99a8f881-2d2f-47fd-9317-ca44e9b3d408/image.png)

> <https://digitalvarys.com/git-branch-and-its-operations/>

Git Branch는 Git에서 코드를 분기하여 관리하는 개념입니다.

* Git에서는 기본적으로 `main` 혹은 `master`라는 하나의 브랜치를 가지고 있으며, 이 브랜치에서 새로운 브랜치를 만들어 작업을 진행합니다.
* 새로운 브랜치를 만들면, 기존 브랜치와 **독립적으로** 코드를 변경할 수 있어 **기능 개발, 버그 수정, 실험적 시도** 등을 안전하게 수행할 수 있습니다.

2. Git Branch 관리 방법
-------------------

### 2.1. 현재 브랜치 정보 확인

```
$ git branch
```

* 현재 작업 중인 브랜치는 `*` 표시로 나타납니다.

예시:  
![](https://velog.velcdn.com/images/euisuk-chung/post/12802951-1a20-4b40-86c4-d4d113d0224e/image.png)

* 원격 브랜치까지 확인하고 싶다면:

```
$ git branch -a
```

예시:  
![](https://velog.velcdn.com/images/euisuk-chung/post/77d76d2c-63b6-4f2b-baa6-4caf315738e9/image.png)

```
$ git branch -a
```

```
* main
remotes/origin/HEAD -> origin/main
remotes/origin/main
```

해석:

* `* main` → 지금 당신은 **로컬의 main 브랜치**에서 작업 중입니다.
* `origin/main`은 **원격 저장소(origin)** 에 있는 `main` 브랜치입니다.
  + 즉, **GitHub나 GitLab의 main 브랜치**를 의미합니다.
* `remotes/origin/HEAD -> origin/main`
  + `origin`이라는 원격 저장소의 기본 브랜치는 `main`임을 의미합니다.
  + `HEAD`는 그 **기본 브랜치를 가리키는 포인터**입니다.

> **Q. 지금 사용하는 브랜치 `main`이 `origin/main`이랑 같은 거야?**
>
> * 👉 *완전히 같지는 않아요.*
>   + `main`: **내 컴퓨터(Local)** 에 있는 브랜치
>   + `origin/main`: **원격 저장소(Remote)** 에 있는 브랜치  
>     → 즉, **같은 이름이지만 서로 다른 공간**에 있습니다.  
>     → 그리고, 우리는 이들을 서로 **동기화(push/pull)** 하면서 관리하는 것입니다.

보통은 이런 식으로 관리합니다 :

```
# 원격의 최신 내용을 내 로컬 main 브랜치에 반영
$ git pull origin main

# 로컬의 변경 내용을 원격 main에 반영
$ git push origin main
```

> **Q.** 난 의심이 많아. **로컬 브랜치** `main`이 **원격 브랜치** `origin/main`과 **정말 연결되어 있는지(매칭되는지)** 확인하고 싶어.
>
> * 👉 `git status`로 확인이 가능합니다.

입력:

```
$ git status
```

출력:

```
On branch main
Your branch is up to date with 'origin/main'.
```

### 2.2. Git Branch 생성

```
$ git branch <새 브랜치 이름>
```

예:

```
$ git branch feature/login
```

혹은 생성과 동시에 전환하려면:

```
$ git checkout -b feature/login
```

### 2.3. Git Branch 이름 변경

```
$ git branch -m <새 브랜치 이름>
```

현재 브랜치에서 변경하는 경우:

```
$ git branch -m feature/login feature/auth
```

### 2.4. Git Branch 삭제

```
$ git branch -d <삭제할 브랜치 이름>
```

강제 삭제 (병합 안 된 경우도 포함):

```
$ git branch -D <삭제할 브랜치 이름>
```

### 2.5. Git Branch 전환

```
$ git checkout <전환할 브랜치 이름>
```

또는 Git 2.23 이후에는 `switch` 명령도 사용 가능:

```
$ git switch feature/login
```

---

🔧 Git 실무 예시
-----------

### ✅ A. 새로운 기능 브랜치 생성 및 작업 (기획/기능 신규 착수 시)

```
# 1. 기준 브랜치(main 또는 dev) 최신화
$ git checkout main
$ git pull origin main

# 2. 새로운 기능 브랜치 생성 및 전환
$ git checkout -b feat/user-profile

# 3. 작업 후 커밋
$ git add .
$ git commit -m "✨ feat: 사용자 프로필 페이지 생성"

# 4. 원격 저장소에 새 브랜치 푸시
$ git push -u origin feat/user-profile

# 5. PR 생성 → 리뷰 → Merge → 브랜치 삭제
```

---

### ✅ B. 원격에 이미 존재하는 브랜치에서 작업 계속하기 (기존 브랜치 이어받기)

```
# 1. 저장소 clone (처음 받는 경우)
$ git clone https://github.com/your-org/your-repo.git
$ cd your-repo

# 2. 원격 브랜치 목록 확인
$ git branch -r

# 3. 작업할 브랜치 checkout (로컬 브랜치 생성 + 자동 트래킹)
$ git checkout feat/user-profile
# 또는 명시적으로
$ git checkout -b feat/user-profile origin/feat/user-profile
# 또는 아래 방법으로도 가능 (추천)
$ git checkout --track origin/feat/user-profile
$ git switch --track origin/feat/user-profile

# 4. 작업 시작
$ git pull            # 혹시 최신 상태가 아닐 경우
$ git status
$ git add .
$ git commit -m "♻️ fix: 프로필 UI 수정"

# 5. 원격 저장소로 푸시
$ git push            # 이미 tracking 중이면 브랜치명 생략 가능
```

---

3. Git Branch 전략
----------------

Git Branch 전략은 협업 시 **브랜치 명명 규칙, 생성/병합 흐름**을 명확히 하기 위한 전략적 선택입니다. 아래는 대표적인 3가지 전략입니다.

### 3.1. Git Flow 전략

구성:

* `main`: 실제 운영 중인 코드 (배포용)
* `develop`: 개발 통합 브랜치
* `feature/기능`: 기능 개발 브랜치
* `release/버전`: 출시 준비 브랜치
* `hotfix/이슈`: 운영 이슈 긴급 수정

```
# 예시: feature 브랜치 생성
$ git checkout -b feature/search-filter develop
```

### 3.2. GitHub Flow 전략

* `main`에서 직접 브랜치를 파서 작업 후 Pull Request
* `CI/CD`가 자동으로 동작하며 배포 가능
* 빠른 반복과 간결한 구조에 적합

### 3.3. GitLab Flow 전략

* GitLab Flow는 GitHub Flow와 Git Flow의 중간 형태
* `main`, `production`, `feature`, `bugfix`, `release` 브랜치를 혼합적으로 운용
* 환경(branch-to-environment) 기반 배포 연계가 자주 사용됨

---

4. Git Branch 협업 방법
-------------------

### 4.1. 코드 리뷰를 위한 Git Branch 활용

```
$ git checkout -b feature/payment
$ git push origin feature/payment
```

* GitHub에서 Pull Request 생성하여 코드 리뷰 요청
* `main` 또는 `develop` 브랜치로 병합하기 전 리뷰 필수

### 4.2. 팀 협업에서 브랜치 규칙 예시

| 브랜치 타입 | 명명 규칙 | 용도 |
| --- | --- | --- |
| 기능 추가 | `feature/<기능명>` | 새 기능 개발 |
| 버그 수정 | `bugfix/<이슈명>` | 발견된 버그 수정 |
| 긴급 패치 | `hotfix/<이슈명>` | 운영 중 긴급 수정 |
| 배포 준비 | `release/<버전>` | QA 및 배포 전 최종 검수용 브랜치 |
| 실험/개인 테스트 | `experiment/<주제>` | 실험적 코드 테스트 |

---

5. 발생 가능 문제 및 해결방법
------------------

### 5.1. 충돌 발생 예시 및 해결

```
Auto-merging app.py
CONFLICT (content): Merge conflict in app.py
```

해결 방법:

1. `app.py` 파일을 열어 `<<<<<<<`, `=======`, `>>>>>>>` 로 표시된 부분을 확인
2. 원하는 코드만 남기고 나머지 삭제
3. 수정 후 add & commit:

```
$ git add app.py
$ git commit -m "Resolve merge conflict in app.py"
```

---

6. Git 충돌 해결 실습과 `rebase` vs `merge` 비교
---------------------------------------

### 6.1. 충돌(Conflict)이란?

Git에서 **충돌(conflict)** 은 두 브랜치에서 동일한 파일의 **같은 라인**을 수정하고 병합할 때 발생합니다. Git은 어떤 변경을 적용해야 할지 자동으로 결정할 수 없기 때문에, 사용자가 수동으로 해결해야 합니다.

---

### 6.2. 실습 예제: 충돌 상황 만들기

```
# main 브랜치에서 새로운 파일 생성
$ git checkout -b main
$ echo "console.log('Hello from main');" > app.js
$ git add app.js
$ git commit -m "Main: Add greeting message"

# feature 브랜치 생성 및 수정
$ git checkout -b feature
$ echo "console.log('Hello from feature');" > app.js
$ git commit -am "Feature: Update greeting message"

# main 브랜치에서 다른 내용으로 수정
$ git checkout main
$ echo "console.log('Hello from MAIN branch');" > app.js
$ git commit -am "Main: Change greeting message"
```

이제 `feature` 브랜치를 `main`에 병합하려고 하면 충돌이 발생합니다.

---

### 6.3. 충돌 해결 및 병합

```
# feature 브랜치에서 main 병합 시도
$ git checkout feature
$ git merge main
```

출력:

```
Auto-merging app.js
CONFLICT (content): Merge conflict in app.js
Automatic merge failed; fix conflicts and then commit the result.
```

`app.js` 파일을 열어보면 아래와 같은 충돌 마커가 표시됩니다.

```
<<<<<<< HEAD
console.log('Hello from feature');
=======
console.log('Hello from MAIN branch');
>>>>>>> main
```

**해결 방법:**

1. 원하는 코드만 남기고 수정:

```
console.log('Hello from BOTH branches');
```

2. 수정 후 저장, add & commit

```
$ git add app.js
$ git commit -m "Resolve conflict in app.js"
```

이제 충돌이 해결되었습니다.

---

### 6.4. Merge vs Rebase

| 항목 | `merge` | `rebase` |
| --- | --- | --- |
| 목적 | 두 브랜치를 통합 | 브랜치 기반을 최신 커밋으로 변경 |
| 커밋 이력 | 브랜치 병합 히스토리 유지 (`merge commit`) | 커밋 히스토리를 깔끔하게 재작성 |
| 사용 상황 | 협업 기록을 명확히 남기고 싶을 때 | 개인 브랜치 정리, 깔끔한 히스토리 관리 시 |
| 충돌 발생 시점 | 병합 시점 | `rebase` 과정 중 각 커밋마다 충돌 가능성 있음 |
| 명령어 예시 | `$ git merge main` | `$ git rebase main` |

---

### 6.5. Rebase 실습

```
# feature 브랜치에서 main 변경 사항을 rebase
$ git checkout feature
$ git rebase main
```

> 중간에 충돌이 발생하면 동일하게 수동 해결 후:

```
$ git add app.js
$ git rebase --continue
```

> 전체 rebase 중단은:

```
$ git rebase --abort
```

---

### ✅ 정리

* `merge`는 **병합 이력**을 명확히 보여주는 반면,
* `rebase`는 **히스토리를 깔끔하게** 정리하는 데 유리합니다.
* 협업 시에는 보통 `merge`를, 개인 브랜치 정리에는 `rebase`를 활용하는 것이 권장됩니다.
* 충돌은 Git 협업에서 빈번하게 발생하며, **수동으로 충돌 마커를 읽고 해결**하는 역량이 중요합니다.