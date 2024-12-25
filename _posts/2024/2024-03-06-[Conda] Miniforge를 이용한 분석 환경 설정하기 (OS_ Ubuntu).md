---
title: "[Conda] Miniforge를 이용한 분석 환경 설정하기 (OS: Ubuntu)"
date: "2024-03-06"
tags:
  - "conda"
  - "환경"
year: "2024"
---

# [Conda] Miniforge를 이용한 분석 환경 설정하기 (OS: Ubuntu)

원본 게시글: https://velog.io/@euisuk-chung/Conda-Miniconda-그리고-Miniforge를-이용한-분석-환경-설정하기-OS-Ubuntu



Conda 소개
========

Conda는 Python 및 R과 같은 프로그래밍 언어의 패키지, 의존성 및 환경 관리를 위한 오픈소스 시스템입니다. 다양한 Python 버전으로 가상 환경을 만들고 관리할 수 있으며, 데이터 과학과 기계 학습 프로젝트에 필요한 라이브러리 및 패키지를 쉽게 설치할 수 있습니다.

Miniconda와 Miniforge의 차이점
-------------------------

* **Miniconda**는 Conda의 가벼운 버전으로, Python과 Conda의 핵심 기능만 포함하며, 필요한 패키지는 사용자가 직접 설치해야 합니다.
* **Miniforge**는 Conda의 또 다른 가벼운 배포판으로, Miniconda와 유사하지만 기본적으로 `conda-forge` 커뮤니티 채널을 사용합니다. 이 채널은 수천 개의 패키지를 제공하며, 오픈소스 커뮤니티에 의해 관리됩니다.

Miniforge로 Conda 환경 설정하기
------------------------

1. **Miniforge Shell 설치**
   
   a. 원하는 버전을 수동으로 설치:
   
   ```
   # 원하는 버전을 찾아서 설치
   wget https://github.com/conda-forge/miniforge/releases/download/4.10.1-0/Miniforge3-Linux-x86_64.sh
   ```
   
   b. 최신 버전으로 자동 설치:
   
   ```
   # 자동 버전 설치
   wget -O Miniforge3.sh "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
   ```
2. **다운로드 받은 Miniforge 설치 Script 실행**
   
   ```
   chmod a+x Miniforge3-Linux-x86_64.sh
   ./Miniforge3-Linux-x86_64.sh
   # 또는
   chmod a+x Miniforge3.sh
   ./Miniforge3.sh
   ```
3. **환경 변수 설정**
   
   ```
   export PATH=/home/username/miniforge3/bin:$PATH
   ```
4. **Python 환경 생성 및 활성화**
   
   ```
   conda create --name py38 python=3.8
   conda activate py38
   ```
5. **Shell 접속 시 자동 활성화 비활성화**
   
   ```
   conda config --set auto_activate_base false
   ```
6. **Conda Channel 관리**
   
   a. conda-forge만 있는지 확인:
   
   ```
   conda config --show channels
   ```
   
   b. 다른 채널 제거:
   
   ```
   conda config --remove channels {채널명}
   ```
   
   c. conda-forge 추가:
   
   ```
   conda config --add channels conda-forge
   ```

결론
--

Miniforge를 사용하면 Conda 환경을 쉽게 설정하고 관리할 수 있습니다. Miniforge는 특히 `conda-forge` 커뮤니티 채널을 통해 다양한 패키지를 제공받고자 하는 사용자에게 유용합니다. 틀린 내용이 있거나 추가될 내용이 있다면 아래 댓글로 달아주세요. 감사합니다! 🤗

