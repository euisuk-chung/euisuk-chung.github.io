---
title: "[Git] Credential Helper로 GitHub 인증하기 🔑"
date: "2024-05-28"
year: "2024"
---

# [Git] Credential Helper로 GitHub 인증하기 🔑




Credential Helper로 GitHub 인증하기
------------------------------

GitHub를 사용하면서 매번 인증 정보를 입력하는 것이 번거로울 수 있습니다. 이를 해결하기 위해 Git은 `credential` 기능을 제공합니다.

![귀찮아](https://velog.velcdn.com/images/euisuk-chung/post/dd12832b-f4e2-4a86-b837-bb7549a74866/image.png)

이번 포스팅에서는 Git Credential Helper를 이용해 인증 정보를 보다 편리하게 관리하는 방법을 설명합니다.

### 1. Credential Helper의 개요

Git Credential Helper는 크게 두 가지 방식으로 나뉩니다:

* **Cache**: 인증 정보를 메모리에 15분 동안 저장합니다. 더 길게 저장하려면 시간을 연장할 수 있습니다.
* **Store**: 인증 정보를 디스크에 저장하여 영구적으로 유지합니다. 개인 컴퓨터에서 사용하는 것을 추천합니다.

이 외에도 OS 자체에서 제공하는 Keychain 시스템을 통해 인증 정보를 더 안전하게 저장할 수 있습니다.

### 2. Git Config 설정

Git의 설정 정보는 `git config` 명령어를 통해 관리할 수 있습니다.

#### 전체 config 리스트 보기

```
git config --global --list
```
#### 사용자 이름과 이메일 설정

```
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
```

* `--global`: 전역적인 설정을 의미합니다. 모든 리포지토리에 적용됩니다.

#### 설정 삭제하기

```
git config --unset --global user.name
git config --unset --global user.email
```
### 3. Credential Helper - Cache

#### Cache 설정하기

```
git config --global credential.helper cache
```

위 명령어를 입력한 후, `git config --global --list` 명령어를 통해 설정이 추가된 것을 확인할 수 있습니다. 기본적으로 15분 동안 인증 정보가 메모리에 저장됩니다.

#### Cache 시간 연장하기

```
git config --global credential.helper 'cache --timeout=3600'
```

이 명령어를 통해 3600초, 즉 1시간 동안 인증 정보가 메모리에 저장되도록 설정할 수 있습니다.

### 4. Credential Helper - Store

#### Store 설정하기

```
git config --global credential.helper store
```

이 명령어를 통해 인증 정보를 디스크에 저장하여 영구적으로 유지할 수 있습니다. 저장된 로그인 정보는 `~/.git-credentials` 파일에 저장됩니다.

### 5. Credential Helper - Keychain

#### Mac에서 Keychain 설정하기

```
git config --global credential.helper osxkeychain
```

1. **새로운 토큰 등록하기**
   
   * `Launchpad` -> `기타(폴더)` -> `키체인 접근`
   * 또는 `Finder` -> `응용 프로그램` -> `유틸리티` -> `키체인 접근.app` 실행
   * 수동으로 `github.com` 항목을 찾아 삭제 (`인터넷 암호` 항목 클릭)
2. **사용자 이름과 이메일 설정**
   
   ```
   git config --global user.name "Your Name"
   git config --global user.email "your_email@example.com"
   ```
3. **새로 등록된 계정으로 Git 명령어 실행**
   
   ```
   git commit -m "Your commit message"
   git push
   ```
   * push 명령어 실행 시, 아이디와 패스워드(토큰)를 입력합니다.
   * 이후 자동으로 키체인에 새로운 계정 정보가 등록됩니다.

#### Windows에서 Keychain 설정하기

```
git config --global credential.helper wincred
```

Windows의 경우, "자격 증명 관리자(Credential Manager)"에서 등록된 정보를 확인할 수 있습니다. 만약 remote repo의 비밀번호를 수정했다면(token이 만료되는 등으로 갱신했다면) 정보를 삭제하고 새로 등록해주어야 합니다.

1. **Credential Manager 열기**
   
   * `제어판` -> `자격 증명 관리자`를 엽니다.
   * `Windows 자격 증명`에서 `github.com` 항목을 찾아 삭제합니다.
2. **새로 등록된 계정으로 Git 명령어 실행**
   
   ```
   git commit -m "Your commit message"
   git push
   ```
   * push 명령어 실행 시, 아이디와 패스워드(토큰)를 입력합니다.
   * 이후 자동으로 Credential Manager에 새로운 계정 정보가 등록됩니다.

### 6. Credential Helper 설정 삭제하기

때때로 Credential Helper 설정이 잘못되었거나 새로운 설정으로 바꾸고 싶을 때가 있습니다. 이럴 때는 기존 설정을 삭제하면 됩니다.

#### Cache 설정 삭제하기

```
git config --unset --global credential.helper
```
#### Store 설정 삭제하기

```
git config --unset --global credential.helper
```
#### Keychain 설정 삭제하기

Mac에서는 키체인 접근 앱에서 `github.com` 항목을 삭제합니다.

Windows에서는 자격 증명 관리자에서 `github.com` 항목을 삭제합니다.

결론
--

이제 Git Credential Helper를 이용해 GitHub 인증 정보를 보다 편리하게 관리할 수 있습니다. 개인 컴퓨터에서는 `Store`를 사용하고, 공용 컴퓨터에서는 `Cache`를 사용하는 것을 추천합니다. Keychain 시스템을 이용하면 더욱 안전하게 인증 정보를 관리할 수 있습니다.

오늘도 긴 글 읽어주셔서 감사합니다⭐

