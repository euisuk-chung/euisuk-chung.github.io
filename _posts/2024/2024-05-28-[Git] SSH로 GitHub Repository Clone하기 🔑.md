---
title: "[Git] SSH로 GitHub Repository Clone하기 🔑"
date: "2024-05-28"
tags:
  - "git"
  - "환경"
year: "2024"
---

# [Git] SSH로 GitHub Repository Clone하기 🔑

SSH로 GitHub Repository Clone하는 방법
=================================

오늘은 SSH를 이용해 GitHub 레포지토리를 클론(clone)하는 방법에 대해 설명하겠습니다⭐ GitHub/GitLab을 사용하다보면 매번 생기는 인증 문제!!! 너무 머리 아프시죠...! 그래서 저는 이제 SSH를 이용해서 보안도 챙기고, 한번에 인증도 할 수 있는 편의성도 챙겨가려고요 😎

SSH를 이용해 GitHub 레포지토리를 클론하면 매번 인증 정보를 입력하지 않아도 됩니다. 한 번 SSH 키를 설정하고 나면, 이후에는 자동으로 인증이 이루어지기 때문에 Git 작업을 보다 편리하게 수행할 수 있습니다. 이번 블로그 포스트에서는 SSH 키를 생성하고 이를 GitHub에 등록한 후, 이를 이용해 레포지토리를 클론하는 전체 과정을 다룹니다.

SSH 키를 생성한 후 GitHub에 등록하면 매번 인증 정보를 입력하지 않아도 됩니다. 아래는 `Windows`와 `Ubuntu` 환경에서의 SSH 키 생성 과정을 설명합니다.

1. SSH 키 생성 - 공통 명령어
--------------------

SSH 키를 생성할 때 사용하는 명령어와 옵션들에 대해 먼저 설명하겠습니다.

* **`ssh-keygen`**: SSH 키를 생성하는 명령어입니다.
* **`-t rsa`**: 키 타입을 RSA로 지정합니다.
* **`-b 4096`**: 키의 비트 수를 지정합니다. 4096 비트는 강력한 보안을 제공합니다.
* **`-C \"your_email@example.com\"`**: 키에 주석(Comment)을 추가합니다.

  + 보통 자신의 이메일 주소를 사용합니다.

### Windows에서 SSH 키 생성

1. **Git Bash 실행**:

   * Windows에서는 Git Bash를 실행하여 명령어를 입력합니다.
2. **SSH 키 생성 명령어 실행**:

   ```
   ssh-keygen -t rsa -b 4096 -C "your_email@example.com" -f ~/.ssh/id_rsa_github
   ```

   * `-f ~/.ssh/id_rsa_github`: 키 파일 이름을 지정합니다.
   * 예시

     ```
     ssh-keygen -t rsa -b 4096 -C "jasuchung@gmail.com" -f ~/.ssh/id_rsa_github
     ```

> 🤔 어? **Powershell로 하면 에러가 발생하는 것 같아요**!! 만약 Powershell로 실행하고 싶은 경우,
>
> * PowerShell에서 발생한 오류는 **`~/.ssh/id_rsa_github` 경로를 Windows PowerShell이 이해하지 못하기 때문**입니다.
> * Windows에서는 `~`가 사용자의 홈 디렉토리를 나타내지만, **PowerShell에서는 이를 직접적으로 사용할 수 없습니다**. 따라서 경로를 Windows의 절대 경로로 지정해야 합니다.
>   1. **SSH 키 생성 시 경로를 수정**:
>      + 아래와 같이 `~/.ssh` 대신 Windows의 홈 디렉토리를 명시적으로 지정합니다:
>
>      ```
>      ssh-keygen -t rsa -b 4096 -C "jasuchung@gmail.com" -f $HOME\\.ssh\\id_rsa_github
>      ```
>
>      + `$HOME`은 PowerShell에서 사용자의 홈 디렉토리를 나타냅니다.
>      + Windows에서는 홈 디렉토리가 보통 `C:\\Users\\<사용자 이름>`로 설정됩니다.
>   2. **`~/.ssh` 디렉토리가 없는 경우 디렉토리 생성**:
>      + `~/.ssh` 디렉토리가 존재하지 않아서 오류가 발생할 수 있습니다. PowerShell에서 아래 명령어를 실행하여 디렉토리를 생성하세요:
>
>        ```
>        mkdir $HOME\\.ssh
>        ```
>   3. **생성된 키 확인**:
>      + 키 생성 후, 공개 키를 확인하려면 다음 명령을 사용하세요:
>
>        ```
>        cat $HOME\\.ssh\\id_rsa_github.pub
>        ```

3. **비밀번호 입력**:
   * 프롬프트가 나타나면 비밀번호를 설정하거나 Enter 키를 눌러 비밀번호 없이 진행할 수 있습니다.

4. **생성된 SSH 키 확인**:

   ```
   cat ~/.ssh/id_rsa_github.pub
   ```

   * 출력된 키를 복사하여 GitHub에 등록합니다.

### Ubuntu에서 SSH 키 생성

1. **터미널 실행**:

   * Ubuntu에서는 터미널을 열어 명령어를 입력합니다.
2. **SSH 키 생성 명령어 실행**:

   ```
   ssh-keygen -t rsa -b 4096 -C "your_email@example.com" -f ~/.ssh/id_rsa_github
   ```

   * `-f ~/.ssh/id_rsa_github`: 키 파일 이름을 지정합니다.
   * 예시

     ```
     ssh-keygen -t rsa -b 4096 -C "jasuchung@gmail.com" -f ~/.ssh/id_rsa_github
     ```
3. **비밀번호 입력**:

   * 프롬프트가 나타나면 비밀번호를 설정하거나 Enter 키를 눌러 비밀번호 없이 진행할 수 있습니다.
4. **생성된 SSH 키 확인**:

   ```
   cat ~/.ssh/id_rsa_github.pub
   ```

   * 출력된 키를 복사하여 GitHub에 등록합니다.

---

2. SSH 키 GitHub에 등록하기
---------------------

1. **GitHub 로그인 및 설정 페이지 이동**:
   * GitHub에 로그인한 후 오른쪽 상단 프로필 아이콘을 클릭하여 **Settings**로 이동합니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/7717bca0-d9f5-41bb-80e7-5825a9a41bb2/image.png)

2. **SSH 및 GPG 키 메뉴 선택**:
   * 왼쪽 메뉴에서 **SSH and GPG keys**를 클릭합니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/00eec71c-b416-4c10-81ab-b7ea47ca515e/image.png)

3. **새 SSH 키 추가**:
   * **New SSH key** 버튼을 클릭합니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/2ac8e71f-c9b6-4f0e-b794-2302be3f01c5/image.png)

4. **필요 정보 입력**
   * **Title**에는 키의 이름을 입력하고, **Key** 필드에는 복사한 공개 키를 붙여넣습니다.
   * **Add SSH key** 버튼을 클릭하여 등록을 완료합니다.
   * **How to chek SSH key**: SSH Key 확인하는 법

     ```
       # Ubuntu 또는 Windows에서 실행
       cat ~/.ssh/id_rsa_github.pub
     ```

![](https://velog.velcdn.com/images/euisuk-chung/post/15f51dff-ff77-4da8-8f6a-bf8d80b79377/image.png)

---

3. SSH를 이용한 GitHub Repository 클론하기
----------------------------------

1. **레포지토리 URL 복사**:

   * 클론하려는 GitHub 레포지토리 페이지에서 **Code** 버튼을 클릭한 후 **SSH**를 선택하고 URL을 복사합니다.
2. **레포지토리 클론 명령어 실행**:

   ```
   git clone git@github.com:username/repository.git
   ```

   * `username`과 `repository`는 실제 복사한 URL에 맞게 변경합니다.

---

4. (추가) Tips! id\_rsa말고 다른 이름으로 설정하기
------------------------------------

🤦‍♂️ 가끔 사용하다 보면, **개인 키와 공개 키가 서로 다르다**는 에러와 마주치게 될때가 있습니다.

> 이럴때는 개인 키와 공개 키가 서로 다르다면, 문제를 해결하기 위해 새로운 키 쌍을 생성하고, 공개 키를 다시 등록해야 합니다.

아래 단계를 따르세요:

1. **새 SSH 키 쌍 생성**

   * 새로운 SSH 키 쌍을 생성합니다. 기존 키 파일이 이미 존재한다면 이름을 다르게 설정하세요.

     ```
     ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
     ```
   * 이메일은 GitHub 계정에 연결된 이메일을 사용합니다.
   * 기본 저장 경로(`~/.ssh/id_rsa`)를 그대로 사용할 경우 기존 파일이 덮어쓰여질 수 있으니, 새로운 이름을 지정합니다(e.g., `~/.ssh/id_rsa_github`).
   * 예:

     ```
     Enter file in which to save the key (/home/user/.ssh/id_rsa): /home/user/.ssh/id_rsa_github
     ```

2. **새로 생성된 공개 키 확인**

   * 생성된 공개 키를 출력합니다:

     ```
     cat ~/.ssh/id_rsa_github.pub
     ```
   * 출력된 키를 복사합니다.

3. **GitHub에 새 공개 키 등록**

   * GitHub 웹사이트에서 다음 단계를 따릅니다:

     1. **Settings > SSH and GPG keys**로 이동합니다.
     2. **New SSH key** 버튼을 클릭합니다.
     3. **Title**에 키의 이름(예: "New Key")을 입력하고, **Key** 입력란에 복사한 공개 키를 붙여넣습니다.
     4. **Add SSH key**를 클릭합니다.

4. **새 키를 SSH 에이전트에 추가**

   * 새로 생성된 개인 키를 SSH 에이전트에 추가합니다:

     ```
     ssh-add ~/.ssh/id_rsa_github
     ```

     + 현재 로드된 키를 확인하여 추가된 키가 올바르게 등록되었는지 확인합니다:

     ```
      ssh-add -l
     ```

> 💻 **SSH 에이전트(Agent) 사용하기**  
> SSH 에이전트는 SSH 키를 메모리에 저장하여 인증 과정을 간소화합니다.  
> GitHub와의 연결을 위해 에이전트를 사용하는 방법은 다음과 같습니다:
>
> * **SSH 에이전트 시작**:
>
>   ```
>   eval "$(ssh-agent -s)"
>   ```
> * **키 추가**: 생성한 키를 SSH 에이전트에 추가합니다:
>
>   ```
>   ssh-add ~/.ssh/id_rsa_github
>   ```
> * **저장된 키 확인**: 저장된 키 목록이 출력됩니다.
>
>   ```
>   ssh-add -l
>   ```
> * **에이전트 종료**: 작업을 종료하고 싶으면 SSH 에이전트를 종료합니다:
>
>   ```
>   ssh-agent -k
>   ```

5. **새 키로 인증 테스트**

* SSH 키가 제대로 설정되었는지 확인하려면 아래 명령어를 사용합니다:

  ```
  ssh -T git@github.com
  ```
* 성공 메시지:

  ```
  Hi username! You've successfully authenticated, but GitHub does not provide shell access.
  ```

> (참고) **SSH 에이전트와 Config 파일의 차이**
>
> * **SSH 에이전트**:
>   + 생성된 SSH 키를 **메모리에 저장하여 인증을 간소화**합니다.
>   + `ssh-add` 명령어로 키를 등록하면 연결 시 자동으로 키를 사용합니다.
> * **Config 파일 설정**:
>   + SSH 연결 시 기본적으로 사용할 키를 명시적으로 지정합니다.
>   + 특정 호스트(`Host github.com`)에 대해 **어떤 키 파일을 사용할지 설정하는 데 유용**합니다.
>   + SSH 에이전트를 사용하지 않아도 동작합니다.

> (참고) **Config 파일을 사용하는 이유**
>
> * **여러 SSH 키 관리**:
>   + **GitHub**, **GitLab** 등 여러 플랫폼에서 서로 다른 SSH 키를 사용할 경우 `~/.ssh/config` 파일을 설정하여 각 호스트에 적합한 키를 지정할 수 있습니다.
>   + 예:
>
>     ```
>     Host github.com
>       HostName github.com
>       User git
>       IdentityFile ~/.ssh/id_rsa_github
>     ```
>
>     ```
>     Host gitlab.com
>       HostName gitlab.com
>       User git
>       IdentityFile ~/.ssh/id_rsa_gitlab
>     ```
> * **기본 키 지정**:
>   + 특정 프로젝트에서 별도로 생성한 키를 기본적으로 사용하려면 유용합니다.

> (참고) **에이전트와 Config를 함께 사용하는 경우**
>
> * `부제` 어떤게 우선시 되는가?
> * Config 파일에서 명시된 `IdentityFile` 설정은 SSH 에이전트에서 관리되는 키보다 우선합니다.
> * 즉, Config 파일에 지정된 키가 있다면 SSH 에이전트에 등록되지 않아도 사용됩니다.

**정리**

* **에이전트는 인증 프로세스를 간소화**하고,
* **Config 파일은 키 사용 규칙을 명시적으로 정의**합니다.

두 가지를 함께 사용하면 다수의 키를 관리하거나 인증을 편리하게 설정할 수 있습니다.

이 과정을 따라 새로운 SSH 키를 생성하고, 공개 키를 등록하며, 인증을 재설정하면 문제가 해결됩니다! 😊

결론
--

이제 SSH 키를 생성하고 GitHub에 등록한 후, SSH를 이용해 레포지토리를 클론하는 방법을 익혔습니다. 이 과정을 통해 한 번 설정 후에는 매번 인증 정보를 입력할 필요 없이 GitHub에 접근할 수 있습니다. 이를 통해 작업 효율을 크게 높일 수 있습니다.

SSH를 이용한 접근은 보안성이 높고 편리하므로, 특히 개인 컴퓨터에서 작업할 때 매우 유용합니다. 추가적으로 Credential Helper를 사용하여 HTTP(S) 방식으로 접근할 때도 인증 정보를 쉽게 관리할 수 있습니다.

오늘도 읽어주셔서 감사합니다! 다음 포스트는 요 위에 `Credential Helper`에 대해서 설명하는 글로 찾아뵙겠습니다!