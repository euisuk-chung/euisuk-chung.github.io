---
title: "[접속] 원격 개발에서 비밀번호 없이 접속하기 (SSH/VSCODE 원격 접속)"
date: "2025-08-20"
year: "2025"
---

# [접속] 원격 개발에서 비밀번호 없이 접속하기 (SSH/VSCODE 원격 접속)


![SSH Remote Connection](https://velog.velcdn.com/images/euisuk-chung/post/fa875e0d-fcc0-48d7-8010-c81e7d9ae51c/image.png)

> <https://code.visualstudio.com/docs/remote/ssh>

매번 리눅스 서버에 접속할 때마다 비밀번호를 입력하는 것은 생각보다 큰 스트레스입니다. 특히 VS Code로 원격 개발을 하면서 하루에도 수십 번씩 재접속해야 하는 상황이라면 더더욱 그렇죠. 이번 포스팅에서는 **Windows 로컬 환경에서 Linux 원격 서버로 SSH Key 인증을 설정**하여, 비밀번호 없이 안전하고 편리하게 자동 로그인하는 방법을 단계별로 상세히 정리했습니다.

---

목차
--

1. SSH Key 인증의 이해
2. SSH Key가 필요한 이유
3. 실무 핵심 가이드라인
4. Windows에서 SSH Key 생성하기
5. Linux 서버에 공개키 등록하기
6. VS Code Remote-SSH 설정하기
7. Passphrase와 SSH Agent 활용하기
8. 트러블슈팅 가이드
9. 전체 프로세스 요약

---

1. SSH Key 인증의 이해
-----------------

### SSH Key의 기본 원리

SSH Key 인증은 **비밀번호 대신 암호화 키 쌍으로 신원을 확인**하는 방식입니다. 이는 비대칭 암호화(Asymmetric Cryptography) 기술을 기반으로 하며, 두 개의 수학적으로 연결된 키로 구성됩니다.

![SSH Key Pair Concept](https://velog.velcdn.com/images/euisuk-chung/post/d1057972-a03d-493d-9566-cec64226f1d9/image.png)

> <https://www.cloudpanel.io/blog/what-are-ssh-keys/>

**구성 요소:**

* **Private Key (비밀키)**

  + 파일명 예시: `id_rsa`, `id_ed25519`
  + 저장 위치: 클라이언트(Windows PC)의 `C:\Users\<사용자명>\.ssh\`
  + 특징: 절대 외부에 유출되어서는 안 되는 개인 소유 키
  + 역할: 서버에 대한 인증 요청 시 디지털 서명 생성
* **Public Key (공개키)**

  + 파일명 예시: `id_rsa.pub`, `id_ed25519.pub`
  + 저장 위치: 서버(Linux)의 `~/.ssh/authorized_keys` 파일 내부
  + 특징: 공개되어도 안전하며, 여러 서버에 복사 가능
  + 역할: 클라이언트의 비밀키로 생성된 서명을 검증

### 인증 프로세스

![SSH Authentication Flow](https://velog.velcdn.com/images/euisuk-chung/post/8c682330-3d05-4bb1-9b38-bcf720a6d17d/image.png)

> <https://www.adsmurai.com/en/articles/how-to-generate-secure-ssh-keys>

1. **접속 시도**: 클라이언트가 서버에 SSH 연결 요청
2. **공개키 확인**: 서버가 `authorized_keys`에서 해당 사용자의 공개키 검색
3. **챌린지 발송**: 서버가 무작위 데이터를 암호화하여 클라이언트에게 전송
4. **서명 생성**: 클라이언트가 비밀키로 해당 데이터에 디지털 서명
5. **서명 검증**: 서버가 공개키로 서명을 검증하여 인증 완료

이 방식은 **중간자 공격(Man-in-the-Middle Attack)**에 강하고, 무차별 대입 공격(Brute Force)으로부터도 안전합니다.

---

2. SSH Key가 필요한 이유
------------------

### 보안성 측면

**강력한 암호화 강도**

* 현대의 SSH Key 알고리즘(특히 Ed25519)은 수학적으로 해독이 거의 불가능합니다
* 4096bit RSA 키는 현재 기술로 해독하는 데 수백 년이 소요됩니다
* 비밀번호는 사전 공격, 무차별 대입 공격에 취약하지만 키는 사실상 면역입니다

**피싱 방지**

* 비밀번호는 사용자가 직접 입력하므로 키로거나 피싱 사이트에 노출될 수 있습니다
* SSH Key는 파일 형태로 존재하므로 물리적으로 탈취하지 않는 한 안전합니다

### 편의성 측면

**자동화 친화적**

* CI/CD 파이프라인, 배포 스크립트 등에서 비밀번호 입력 없이 자동 실행 가능
* 여러 서버에 동일한 공개키를 배포하여 하나의 비밀키로 모두 접근 가능

**개발 생산성 향상**

* VS Code Remote-SSH로 작업 시 재접속 시마다 비밀번호 입력 불필요
* Git 작업, 서버 간 파일 전송(scp, rsync) 등이 매끄럽게 진행됩니다

### 관리 용이성

**세밀한 접근 제어**

* 프로젝트별, 팀원별로 다른 키를 발급하여 권한 분리 가능
* 특정 키가 유출되었을 때 해당 공개키만 서버에서 제거하면 즉시 접근 차단

---

3. 실무 핵심 가이드라인
--------------

### 알고리즘 선택 기준

**Ed25519 (권장)**

* 생성 속도가 빠르고 키 길이가 짧으면서도 보안성이 뛰어남
* 현대 암호학 표준에 부합하며, 대부분의 최신 시스템에서 지원
* 고정 길이(256bit)로 `-b` 옵션 불필요

```
# Ed25519 키 생성 (권장)
ssh-keygen -t ed25519 -C "your_email@example.com"
```

**RSA 4096bit (호환성 우선 시)**

* 레거시 시스템이나 오래된 서버와의 호환성이 필요한 경우
* 기본값(2048bit)보다 안전한 4096bit 사용 권장

```
# RSA 4096bit 키 생성
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

**RSA `-b` 옵션의 의미**

* `-b`는 비트(bit) 길이를 지정하는 옵션입니다
* RSA 키는 내부적으로 큰 소수(prime number)의 곱으로 만들어지며, 이 숫자의 크기를 비트로 표현합니다
* 길수록 안전하지만 연산 비용이 증가합니다

| 키 길이 | 보안 수준 | 권장 사항 |
| --- | --- | --- |
| 2048bit | 기본 | 최소 요구사항 |
| 4096bit | 강화 | 권장 설정 |
| 8192bit | 매우 강함 | 과도함 (성능 저하) |

### 보안 강화 원칙

**Passphrase 사용**

* 비밀키 파일 자체를 암호화하는 추가 보호층
* 비밀키가 물리적으로 유출되어도 passphrase 없이는 사용 불가
* SSH Agent와 함께 사용하면 편의성 유지 가능

**엄격한 파일 권한**

| 경로/파일 | Windows | Linux | 설명 |
| --- | --- | --- | --- |
| `.ssh` 디렉토리 | 현재 사용자만 | `700` | 소유자만 읽기/쓰기/실행 |
| 비밀키 파일 | 현재 사용자만 | `600` | 소유자만 읽기/쓰기 |
| 공개키 파일 | 제한 없음 | `644` | 모두 읽기, 소유자만 쓰기 |
| `authorized_keys` | - | `600` | 소유자만 읽기/쓰기 |

**키 격리 전략**

* 개인용, 회사용, 프로젝트용 등 용도별로 별도 키 생성
* `~/.ssh/config`에서 호스트별로 다른 키 지정 가능

---

4. Windows에서 SSH Key 생성하기
-------------------------

### 사전 준비사항

**OpenSSH 클라이언트 확인**

Windows 10(1809 이상) 및 Windows 11에는 OpenSSH 클라이언트가 기본 내장되어 있습니다. PowerShell에서 확인:

```
# OpenSSH 설치 확인
Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH.Client*'

# 출력 예시:
# Name  : OpenSSH.Client~~~~0.0.1.0
# State : Installed
```

만약 설치되지 않았다면:

```
# OpenSSH 클라이언트 설치
Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0
```

### 키 생성 프로세스

**Step 1: PowerShell 실행**

* `Win + X` → "Windows PowerShell" 또는 "터미널" 선택
* 관리자 권한 불필요 (일반 사용자 권한으로 실행)

**Step 2: 키 생성 명령 실행**

```
# Ed25519 키 생성 (권장)
ssh-keygen -t ed25519 -C "myemail@company.com"
```

또는 RSA 사용 시:

```
# RSA 4096bit 키 생성
ssh-keygen -t rsa -b 4096 -C "myemail@company.com"
```

**옵션 설명:**

* `-t`: 키 타입 지정 (ed25519 또는 rsa)
* `-b`: 비트 길이 (RSA만 해당, Ed25519는 고정 256bit)
* `-C`: 주석(Comment) 추가 - 보통 이메일 주소나 설명 입력

**Step 3: 대화형 프롬프트 응답**

```
Generating public/private ed25519 key pair.
Enter file in which to save the key (C:\Users\YourName/.ssh/id_ed25519):
```

* **파일 저장 위치**: 그냥 Enter (기본 경로 사용)
  + Ed25519: `C:\Users\<사용자명>\.ssh\id_ed25519`
  + RSA: `C:\Users\<사용자명>\.ssh\id_rsa`

```
Enter passphrase (empty for no passphrase):
```

* **Passphrase 입력**:
  + 보안 강화를 원하면 강력한 암호 입력 (최소 12자 이상 권장)
  + 편의성 우선이면 그냥 Enter (비워둠)
  + **권장**: Passphrase 설정 + SSH Agent 사용

```
Enter same passphrase again:
```

* 동일한 passphrase 재입력

**Step 4: 생성 완료 확인**

```
Your identification has been saved in C:\Users\YourName/.ssh/id_ed25519.
Your public key has been saved in C:\Users\YourName/.ssh/id_ed25519.pub.
The key fingerprint is:
SHA256:abcd1234... myemail@company.com
The key's randomart image is:
+--[ED25519 256]--+
|    .o+          |
|   . =.o         |
|    = B +        |
...
```

생성된 파일 확인:

```
# .ssh 디렉토리 내용 확인
dir $env:USERPROFILE\.ssh

# 출력 예시:
# Mode                 LastWriteTime         Length Name
# ----                 -------------         ------ ----
# -a---          2025-10-01  오전 9:30            464 id_ed25519
# -a---          2025-10-01  오전 9:30            103 id_ed25519.pub
```

### 주석(Comment) 없이 생성하기

주석이 필요 없거나 나중에 추가하고 싶다면 `-C` 옵션 생략:

```
ssh-keygen -t ed25519
```

이 경우 공개키 마지막에 주석이 붙지 않거나 Windows 사용자명이 자동으로 표시됩니다.

---

5. Linux 서버에 공개키 등록하기
---------------------

### 공개키 내용 확인

Windows PowerShell에서 공개키 내용을 확인합니다:

```
# Ed25519 공개키 내용 출력
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub

# RSA 사용 시
Get-Content $env:USERPROFILE\.ssh\id_rsa.pub
```

출력 예시:

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJqL9Zv8... myemail@company.com
```

이 전체 문자열을 복사합니다 (Ctrl+C).

### Linux 서버에서 등록 작업

**방법 1: 기존 비밀번호로 SSH 접속 후 등록**

Windows PowerShell에서:

```
# Linux 서버에 접속 (비밀번호 입력 필요)
ssh ubuntu@192.168.1.100
```

Linux 서버 터미널에서:

```
# .ssh 디렉토리 생성 (이미 있으면 무시됨)
mkdir -p ~/.ssh

# 디렉토리 권한 설정
chmod 700 ~/.ssh

# authorized_keys 파일에 공개키 추가
cat >> ~/.ssh/authorized_keys
```

이제 커서가 입력 대기 상태로 변합니다.

* Windows에서 복사한 공개키를 붙여넣기 (우클릭 또는 Shift+Insert)
* Enter 한 번
* `Ctrl + D` 눌러 입력 종료

```
# 파일 권한 설정
chmod 600 ~/.ssh/authorized_keys

# 내용 확인
cat ~/.ssh/authorized_keys
```

**방법 2: 원격 명령으로 한 번에 처리**

Windows PowerShell에서 한 줄로 실행:

```
# 공개키를 서버로 전송하여 등록
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh ubuntu@192.168.1.100 "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

이 명령은:  
1. 로컬의 공개키 내용을 읽어서  
2. SSH로 서버에 전송하며  
3. 서버에서 `.ssh` 디렉토리 생성, 권한 설정, 공개키 추가를 자동 수행합니다

**방법 3: SCP로 파일 전송 후 추가**

```
# 공개키 파일을 서버로 복사
scp $env:USERPROFILE\.ssh\id_ed25519.pub ubuntu@192.168.1.100:~/temp_key.pub
```

Linux 서버에서:

```
# 전송된 파일을 authorized_keys에 추가
mkdir -p ~/.ssh
cat ~/temp_key.pub >> ~/.ssh/authorized_keys
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
rm ~/temp_key.pub  # 임시 파일 삭제
```

### 주의사항

* **`>`와 `>>`의 차이**: `>`는 파일을 덮어쓰고, `>>`는 파일 끝에 추가합니다. 기존 키가 있다면 반드시 `>>`를 사용하세요.
* **여러 줄 추가 금지**: 공개키는 **한 줄**이어야 합니다. 줄바꿈이 들어가면 인증 실패합니다.
* **권한 문제**: Linux SSH 서버는 `.ssh` 디렉토리와 `authorized_keys` 파일 권한이 너무 열려있으면 보안상 인증을 거부합니다.

---

6. VS Code Remote-SSH 설정하기
--------------------------

### VS Code 확장 설치

1. VS Code 실행
2. 좌측 사이드바에서 확장(Extensions) 아이콘 클릭 (Ctrl+Shift+X)
3. "Remote - SSH" 검색
4. Microsoft에서 제공하는 "Remote - SSH" 확장 설치
5. 함께 설치되는 "Remote - SSH: Editing Configuration Files" 확장도 자동 설치됨

### SSH Config 파일 작성

**Step 1: Config 파일 생성/편집**

VS Code에서:  
1. `F1` 또는 `Ctrl+Shift+P`로 명령 팔레트 열기  
2. "Remote-SSH: Open SSH Configuration File..." 입력  
3. `C:\Users\<사용자명>\.ssh\config` 선택

또는 PowerShell에서 직접:

```
# Config 파일을 VS Code로 열기
code $env:USERPROFILE\.ssh\config
```

**Step 2: 호스트 설정 추가**

다음 내용을 입력:

```
# 개발 서버 설정
Host dev-server
    HostName 192.168.1.100
    User ubuntu
    IdentityFile C:\Users\YourName\.ssh\id_ed25519
    AddKeysToAgent yes
    IdentitiesOnly yes
    ServerAliveInterval 60
    ServerAliveCountMax 3

# 프로덕션 서버 설정 (다른 키 사용 예시)
Host prod-server
    HostName 203.0.113.50
    User admin
    Port 2222
    IdentityFile C:\Users\YourName\.ssh\id_rsa_production
    AddKeysToAgent yes
    IdentitiesOnly yes
```

**설정 항목 상세 설명:**

| 항목 | 필수 여부 | 설명 |
| --- | --- | --- |
| `Host` | 필수 | 접속 시 사용할 별칭 (자유롭게 지정) |
| `HostName` | 필수 | 실제 서버 IP 주소 또는 도메인 |
| `User` | 필수 | 서버 로그인 사용자명 |
| `IdentityFile` | 권장 | 사용할 비밀키 파일 경로 (절대 경로 권장) |
| `Port` | 선택 | SSH 포트 (기본값 22, 변경 시 명시) |
| `AddKeysToAgent` | 권장 | SSH Agent에 키 자동 추가 (yes 권장) |
| `IdentitiesOnly` | 권장 | 지정한 키만 사용 (yes 권장) |
| `ServerAliveInterval` | 선택 | 서버에 keepalive 신호 전송 간격(초) |
| `ServerAliveCountMax` | 선택 | keepalive 실패 허용 횟수 |

**경로 표기 주의사항:**

* Windows에서는 백슬래시(`\`) 또는 슬래시(`/`) 모두 사용 가능
* 공백이 포함된 경로는 따옴표로 감싸기: `"C:\Program Files\..."`
* `~`는 Windows PowerShell SSH에서 지원하지만, 절대 경로 권장

### VS Code에서 접속하기

**방법 1: 명령 팔레트 사용**

1. `F1` 또는 `Ctrl+Shift+P`
2. "Remote-SSH: Connect to Host..." 입력
3. Config에 정의한 호스트 이름 선택 (예: `dev-server`)
4. 새 창이 열리며 자동 접속 시도
5. 최초 접속 시 Fingerprint 확인 팝업 → "Continue" 클릭
6. Passphrase 설정 시 한 번만 입력 (SSH Agent 사용 시)

**방법 2: 좌측 사이드바 사용**

1. 좌측 사이드바에서 "Remote Explorer" 아이콘 클릭
2. "SSH Targets" 섹션에서 호스트 확인
3. 호스트 우클릭 → "Connect to Host in Current Window" 또는 "Connect to Host in New Window"

### 접속 완료 확인

성공 시 VS Code 좌측 하단 상태바에 다음과 같이 표시:

```
SSH: dev-server
```

이제 VS Code 터미널은 자동으로 Linux 서버 환경이 되며, 파일 탐색기도 서버의 파일 시스템을 보여줍니다.

### 추가 편의 기능

**포트 포워딩 설정**

개발 서버의 웹 애플리케이션(예: 포트 8000)을 로컬에서 접근하고 싶다면:

```
Host dev-server
    ...
    LocalForward 8000 localhost:8000
```

이제 로컬 브라우저에서 `http://localhost:8000` 접속 시 서버의 8000 포트로 연결됩니다.

**ProxyJump를 통한 다단계 접속**

Bastion 서버를 거쳐 내부 서버에 접속해야 하는 경우:

```
Host bastion
    HostName 203.0.113.10
    User ubuntu
    IdentityFile C:\Users\YourName\.ssh\id_ed25519

Host internal-server
    HostName 10.0.1.50
    User ubuntu
    ProxyJump bastion
    IdentityFile C:\Users\YourName\.ssh\id_ed25519
```

---

7. Passphrase와 SSH Agent 활용하기
-----------------------------

### Passphrase의 필요성

Passphrase는 비밀키 파일 자체를 암호화하는 추가 보안 계층입니다.

**장점:**

* 비밀키 파일이 물리적으로 유출되어도 passphrase 없이는 사용 불가
* 노트북 분실, 백업 파일 유출 등의 상황에서 보호

**단점:**

* 매번 SSH 접속 시 passphrase 입력 필요 (SSH Agent 없이는 불편)

### SSH Agent란?

SSH Agent는 비밀키를 메모리에 안전하게 캐싱하여, passphrase를 세션당 한 번만 입력하도록 하는 서비스입니다.

### Windows에서 SSH Agent 설정

**Step 1: SSH Agent 서비스 활성화**

PowerShell을 **관리자 권한**으로 실행:

```
# SSH Agent 서비스 상태 확인
Get-Service ssh-agent

# 서비스 시작
Start-Service ssh-agent

# 시스템 부팅 시 자동 시작 설정
Set-Service -Name ssh-agent -StartupType Automatic
```

**Step 2: 비밀키 등록**

일반 사용자 권한 PowerShell에서:

```
# 비밀키를 SSH Agent에 추가
ssh-add $env:USERPROFILE\.ssh\id_ed25519

# Passphrase 설정 시 프롬프트 나타남
Enter passphrase for C:\Users\YourName/.ssh/id_ed25519:
# (passphrase 입력)
Identity added: C:\Users\YourName/.ssh/id_ed25519 (myemail@company.com)
```

**Step 3: 등록된 키 확인**

```
# 현재 Agent에 등록된 키 목록
ssh-add -l

# 출력 예시:
# 256 SHA256:abcd1234... myemail@company.com (ED25519)
```

### VS Code Config에 Agent 설정 추가

`~/.ssh/config` 파일에 `AddKeysToAgent yes` 추가 시, VS Code 접속 시 자동으로 Agent에 키 등록:

```
Host dev-server
    ...
    AddKeysToAgent yes
```

### 세션 종료 시 처리

SSH Agent는 Windows 로그아웃 시까지 키를 메모리에 유지합니다. 보안을 위해 명시적으로 제거하려면:

```
# Agent에서 특정 키 제거
ssh-add -d $env:USERPROFILE\.ssh\id_ed25519

# Agent에서 모든 키 제거
ssh-add -D
```

---

8. 트러블슈팅 가이드
------------

### 문제 1: "Permission denied (publickey)"

**증상:**

```
ubuntu@192.168.1.100: Permission denied (publickey).
```

**원인 및 해결:**

1. **공개키가 서버에 제대로 등록되지 않음**

   ```
   # Linux 서버에서 확인
   cat ~/.ssh/authorized_keys
   # 공개키 내용이 정확히 한 줄로 들어가 있는지 확인
   ```
2. **서버 파일 권한 문제**

   ```
   # Linux 서버에서 권한 재설정
   chmod 700 ~/.ssh
   chmod 600 ~/.ssh/authorized_keys
   ```
3. **홈 디렉토리 권한 문제**

   ```
   # 홈 디렉토리는 다른 사용자가 쓰기 권한을 가지면 안 됨
   chmod 755 ~
   ```
4. **SELinux 컨텍스트 오류 (CentOS/RHEL)**

   ```
   restorecon -R -v ~/.ssh
   ```

### 문제 2: "WARNING: UNPROTECTED PRIVATE KEY FILE!"

**증상 (Git Bash/WSL에서):**

```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Permissions 0644 for 'C:/Users/YourName/.ssh/id_ed25519' are too open.
```

**원인:**  
Windows NTFS 파일 시스템과 Git Bash/WSL의 권한 해석 차이

**해결:**

Git Bash에서:

```
# 비밀키 파일 권한 변경
chmod 600 ~/.ssh/id_ed25519
```

WSL에서:

```
# Windows 파일시스템 권한 문제 해결
sudo chmod 600 /mnt/c/Users/YourName/.ssh/id_ed25519
```

PowerShell에서는 이 경고가 나타나지 않습니다 (Windows 자체 권한 시스템 사용).

### 문제 3: VS Code 접속 시 무한 로딩

**증상:**  
"Setting up SSH Host dev-server: Downloading VS Code Server..." 에서 멈춤

**원인 및 해결:**

1. **서버의 디스크 용량 부족**

   ```
   # Linux 서버에서 확인
   df -h
   # /home 파티션이 꽉 찼다면 정리 필요
   ```
2. **방화벽/네트워크 문제**

   * VS Code Server는 다운로드를 위해 GitHub/Microsoft CDN 접근 필요
   * 서버에서 외부 인터넷 연결 확인:

   ```
   curl -I https://update.code.visualstudio.com
   ```
3. **VS Code Server 캐시 삭제**

   ```
   # Linux 서버에서
   rm -rf ~/.vscode-server
   ```

### 문제 4: Passphrase를 계속 물어봄

**증상:**  
SSH Agent에 키를 추가했는데도 매번 passphrase 입력 요구

**원인 및 해결:**

1. **SSH Agent가 실행 중인지 확인**

   ```
   Get-Service ssh-agent
   # Status가 Running이 아니면 Start-Service ssh-agent
   ```
2. **키가 Agent에 등록되었는지 확인**

   ```
   ssh-add -l
   # "The agent has no identities." 출력 시 ssh-add로 재등록
   ```
3. **Config 파일에 AddKeysToAgent 설정**

   ```
   Host *
       AddKeysToAgent yes
   ```

### 문제 5: "Too many authentication failures"

**증상:**

```
Received disconnect from 192.168.1.100: Too many authentication failures
```

**원인:**  
SSH 클라이언트가 여러 개의 키를 시도하다가 서버의 시도 횟수 제한 초과

**해결:**  
Config 파일에 `IdentitiesOnly yes` 추가:

```
Host dev-server
    ...
    IdentitiesOnly yes
```

이렇게 하면 지정한 키만 사용하고 다른 키는 시도하지 않습니다.

### 문제 6: Host key verification failed

**증상:**

```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
```

**원인:**  
서버 재설치, IP 재사용 등으로 호스트 키가 변경됨

**해결:**

```
# Windows에서 해당 호스트의 기록 삭제
ssh-keygen -R 192.168.1.100

# 또는 known_hosts 파일에서 직접 해당 줄 삭제
notepad $env:USERPROFILE\.ssh\known_hosts
```

---

9. 전체 프로세스 요약
-------------

### Windows (로컬) 작업 순서

```
# ===== 1. SSH Key 생성 =====
ssh-keygen -t ed25519 -C "myemail@company.com"
# Enter 3회 (기본 경로, passphrase 생략 시)

# ===== 2. SSH Agent 설정 (관리자 권한 PowerShell) =====
Start-Service ssh-agent
Set-Service -Name ssh-agent -StartupType Automatic

# ===== 3. SSH Agent에 키 등록 (일반 PowerShell) =====
ssh-add $env:USERPROFILE\.ssh\id_ed25519

# ===== 4. 공개키 내용 복사 =====
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub | clip
# 또는 출력된 내용을 직접 복사
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub

# ===== 5. VS Code Config 작성 =====
code $env:USERPROFILE\.ssh\config
# 아래 내용 입력:
```

```
Host my-linux-server
    HostName 192.168.1.100
    User ubuntu
    IdentityFile C:\Users\YourName\.ssh\id_ed25519
    AddKeysToAgent yes
    IdentitiesOnly yes
    ServerAliveInterval 60
```

### Linux (서버) 작업 순서

```
# ===== 1. 비밀번호로 서버 접속 (최초 1회만) =====
ssh ubuntu@192.168.1.100

# ===== 2. .ssh 디렉토리 및 authorized_keys 설정 =====
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# ===== 3. 공개키 등록 =====
cat >> ~/.ssh/authorized_keys
# (Windows에서 복사한 공개키 붙여넣기)
# (Ctrl+D로 저장)

# ===== 4. 권한 설정 =====
chmod 600 ~/.ssh/authorized_keys

# ===== 5. 확인 및 접속 종료 =====
cat ~/.ssh/authorized_keys
exit
```

### VS Code 접속 검증

```
# ===== 1. 터미널에서 수동 접속 테스트 =====
ssh my-linux-server
# Passphrase 설정 시 한 번만 입력, 이후 자동

# ===== 2. VS Code에서 접속 =====
# F1 → "Remote-SSH: Connect to Host..." → my-linux-server 선택
```

### 빠른 체크리스트

| 단계 | Windows | Linux | 확인 사항 |
| --- | --- | --- | --- |
| 키 생성 | ✅ | - | `id_ed25519`, `id_ed25519.pub` 존재 |
| Agent 실행 | ✅ | - | `Get-Service ssh-agent` → Running |
| 키 등록 | ✅ | - | `ssh-add -l` → 키 목록 출력 |
| 공개키 복사 | ✅ | - | 클립보드에 복사 완료 |
| 공개키 등록 | - | ✅ | `authorized_keys` 파일에 한 줄로 추가 |
| 권한 설정 | - | ✅ | `.ssh` → 700, `authorized_keys` → 600 |
| Config 작성 | ✅ | - | Host, HostName, User, IdentityFile 확인 |
| 접속 테스트 | ✅ | - | 비밀번호 없이 접속 성공 |

---

마치며
---

SSH Key 인증은 처음 설정 시 다소 복잡해 보일 수 있지만, 한 번 제대로 구축하면 개발 생산성을 크게 향상시킬 수 있는 강력한 도구입니다. 특히 **Windows 로컬 환경에서 Linux 원격 서버로 VS Code Remote-SSH를 사용하는 경우**, 비밀번호 입력 없이 즉시 코드 편집 환경에 진입할 수 있어 워크플로우가 매끄럽게 연결됩니다.

### 핵심 요점 재정리

1. **Ed25519 알고리즘 우선 사용** - 빠르고 안전하며 현대적
2. **Passphrase + SSH Agent 조합** - 보안과 편의성 모두 확보
3. **엄격한 권한 관리** - Linux 서버에서 700/600 권한 필수
4. **Config 파일 활용** - 여러 서버 관리 시 효율적
5. **문제 발생 시 권한/경로 먼저 확인** - 대부분의 오류 원인

이제 매일 비밀번호를 입력하는 수고에서 벗어나, 더 중요한 코드 작성과 문제 해결에 집중하시기 바랍니다.

읽어주셔서 감사합니다 ☀️