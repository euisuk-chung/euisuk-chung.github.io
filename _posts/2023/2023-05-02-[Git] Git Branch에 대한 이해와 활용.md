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

원본 게시글: https://velog.io/@euisuk-chung/Git-Branch에-대한-이해와-활용



Git Branch에 대한 이해와 활용
=====================

Git Branch는 Git에서 매우 중요한 개념 중 하나입니다. 이번 포스트에서는 Git Branch란 무엇인지, Git Branch를 활용하여 어떻게 코드를 관리할 수 있는지, 그리고 Git Branch를 활용한 협업 방법 등에 대해 살펴보겠습니다.

1. Git Branch란?
---------------

Git Branch는 Git에서 코드를 분기하여 관리하는 개념입니다. Git에서는 기본적으로 `master`라는 하나의 브랜치를 가지고 있으며, 이 `master` 브랜치에서 새로운 브랜치를 만들어 작업을 진행합니다. 새로운 브랜치를 만들면, 기존의 `master` 브랜치와 독립적으로 코드를 변경할 수 있습니다.

2. Git Branch 관리 방법
-------------------

Git Branch를 관리하는 방법은 다음과 같습니다.

### 2.1. Git Branch 생성

새로운 브랜치를 생성하는 방법은 다음과 같습니다.

```
$ git branch <새 브랜치 이름>
```
### 2.2. Git Branch 이름 변경

브랜치 이름을 변경하는 방법은 다음과 같습니다.

```
$ git branch -m <새 브랜치 이름>
```
### 2.3. Git Branch 삭제

브랜치를 삭제하는 방법은 다음과 같습니다.

```
$ git branch -d <삭제할 브랜치 이름>
```
### 2.4. Git Branch 전환

다른 브랜치로 전환하는 방법은 다음과 같습니다.

```
$ git checkout <전환할 브랜치 이름>
```

3. Git Branch 전략
----------------

Git에서는 다양한 브랜칭 전략을 사용할 수 있습니다. 이번 포스트에서는 대표적인 Git 브랜칭 전략인 Git Flow, Github Flow, GitLab Flow를 살펴보겠습니다.

### 3.1. Git Flow 전략

Git Flow 전략은 크게 `develop`, `feature`, `release`, `hotfix`, `master` 브랜치로 구성됩니다. 이전 브랜치에서 새로운 브랜치를 생성하여 기능 추가나 버그 수정을 진행합니다. 모든 기능이 개발되면 `release` 브랜치에서 배포 가능한 버전을 만들어 `master` 브랜치에 병합합니다.

### 3.2. Github Flow 전략

Github Flow 전략은 단일 브랜치 `master`에서 작업을 진행하는 전략입니다. 새로운 기능을 추가할 때는 `feature` 브랜치에서 작업을 하며, 이후 `master` 브랜치로 병합합니다. 배포는 `master` 브랜치로 진행됩니다.

### 3.3. GitLab Flow 전략

GitLab Flow 전략은 크게 `production`, `feature`, `hotfix` 브랜치로 구성됩니다. 이전 브랜치에서 새로운 브랜치를 생성하여 작업을 진행하며, 모든 기능이 개발되면 `production` 브랜치로 병합합니다.

4. Git Branch 협업 방법
-------------------

Git Branch를 활용한 협업 방법은 다음과 같습니다.

### 4.1. Git Branch를 활용한 코드 리뷰

새로운 기능을 추가할 때, 다른 개발자들이 코드를 검토하고 리뷰할 수 있도록 `feature` 브랜치에서 작업을 진행합니다. 이후, 코드 리뷰를 통해 변경 사항을 피드백받고 수정합니다.

### 4.2. Git Branch를 활용한 Pull Request

기능 개발이 완료된 후, 코드 리뷰가 완료되면 `master` 브랜치로 병합하는 Pull Request를 생성합니다. Pull Request를 생성하면 다른 개발자들이 변경 사항을 검토하고, 이후 `master` 브랜치로 병합할 수 있습니다.

5. 발생 가능 문제 및 해결방법
------------------

Git Branch 충돌은 두 개의 브랜치에서 같은 파일을 수정할 때 발생할 수 있습니다. 충돌을 해결하는 방법은 다음과 같습니다.

* 충돌이 발생한 파일을 열어서 충돌 부분을 수정합니다.
* 충돌 부분을 수정한 후, 파일을 저장하고 커밋합니다.

Git Branch 관리 시 발생할 수 있는 문제점은 다음과 같습니다.

* 브랜치를 많이 만들 경우, 브랜치 관리가 어려워집니다.
* 브랜치 병합 시 충돌이 발생할 수 있습니다.
* 브랜치 사용이 너무 자유로워지면, 코드의 일관성을 유지하기 어렵습니다.

이러한 문제점을 해결하기 위해서는, Git Branch 관리에 대한 규칙을 설정하고, 브랜치를 적절히 사용해야 합니다. 다음 포스트는 만약에 충돌이 발생하게 되면 어떻게 수정을 해야하는지 한번 살펴보도록 하겠습니다 :)

