---
title: "[Linux] 딥러닝 환경 구축 : CUDA, CuDNN"
date: "2024-04-24"
tags:
  - "linux"
  - "꿀팁"
  - "환경"
year: "2024"
---

# [Linux] 딥러닝 환경 구축 : CUDA, CuDNN




오늘 회사 로컬 서버가 다운되면서 기존에 오래된 파일들을 밀고 새롭게 다시 설치할 기회가 왔다!!! 파일은 다행히 복원을 완료해서 지금에서야 웃으면서 쓰지만... 정말이지 끔찍한 8시간이었다...ㅎㅎ

출근해서 업무를 좀 하다보니 서버가 무한 복구 모드로 빠져서 복원되지 않는 문제에 빠졌다... 특정 패키지를 설치하시면서 시스템 파일을 건드린 것 같았고.. 도저히 복구 모드에서도 살릴 방법이 보이지 않았다🔥 그래도 주요 코드 및 데이터는 하드로 관리하고 있었기 때문에 주요 정보는 살릴 수 있었다...

(핑계 주의) 개인적으로 도커를 도입해서 적용하고 싶었지만 여러명이서 하나의 원격 데스크탑을 PoC 실험용으로 사용하는 것이라 성능이 좋지 않았고, 기존에 사용해오던 툴 및 방식들이 있던터라 내 마음대로 도입하기가 어려웠다...😥

![하..불](https://velog.velcdn.com/images/euisuk-chung/post/0f506202-b5bd-4a9b-814d-bb547d38ceea/image.png)

서두가 길긴 했지만 이 참에 `UBUNTU`를 새롭게 설치하고 기존에 오래된 레거시 코드들은 정리해주는 작업을 수행할 수 있었다. 하지만, 아직까지 한가지 난관이 남아있었다! 바로바로 딥러닝 환경 설정!! 항상 딥러닝 환경 설정을 하다보면 가차(뽑기)처럼 어떤 블로그 글을 읽는 가에 따라서 한번에 설치가 잘 될 때도 안 될 때도 있다. 그래서 이참에 새롭게 설치를 하면서 본질을 파악하고 제대로 된 설치를 해보려고 한다.

용어정리
====

Nvidia Driver는 무엇인가?
--------------------

![Nvidia Driver](https://velog.velcdn.com/images/euisuk-chung/post/ec8b163b-08fd-42d0-b83c-d2e50c6c561e/image.png)

### 정의

Nvidia Driver는 `Nvidia 그래픽 카드`와 `컴퓨터 운영 체제(OS)` 간의 `통신을 관리하고 제어`하는 소프트웨어이다. 이 드라이버는 하드웨어와 소프트웨어 간의 인터페이스 역할을 하며, GPU를 최적의 조건에서 작동하게 한다.

### 역할

1. `그래픽 성능 최적화`: 최신 게임 및 애플리케이션에 맞춰 그래픽 성능을 조정하고 최적화한다.
2. `호환성 유지`: 운영 체제 업데이트나 소프트웨어 변경 사항에 따라 호환성을 유지한다.
3. `오류 수정`: 발견되는 버그나 성능 문제를 해결하여 안정성을 보장한다.

CUDA란 무엇인가?
-----------

### 정의

CUDA(Compute Unified Device Architecture)는 Nvidia가 개발한 병렬 컴퓨팅 플랫폼 및 프로그래밍 모델이다. CUDA는 개발자가 Nvidia GPU를 사용하여 `일반 처리 작업의 계산 처리를 가속화`할 수 있게한다.

### 역할

1. `병렬 처리 가속화`: 대규모 데이터와 복잡한 계산을 GPU에서 병렬로 처리하여 CPU만 사용할 때보다 빠르게 작업을 완료할 수 있다.
2. `다양한 애플리케이션 지원`: 과학 연산, 엔지니어링, 딥러닝 등 다양한 분야에서 활용된다.

CUDA Toolkit이란 무엇인가?
--------------------

### 정의

CUDA Toolkit은 `CUDA 개발 환경을 제공`하는 소프트웨어 패키지로, GPU 가속 애플리케이션 개발에 필요한 컴파일러, 라이브러리, 도구, 샘플 코드를 포함하고 있다.

### 역할

* `개발 도구 제공`: CUDA 애플리케이션을 개발할 때 필요한 다양한 도구와 라이브러리를 제공한다.
* `성능 분석`: 개발된 애플리케이션의 성능을 분석하고 최적화할 수 있는 도구를 포함한다.

cuDNN(cuda Deep Neural network Library)
---------------------------------------

### 정의

cuDNN은 `딥러닝 연산을 위해 최적화된 GPU 가속 라이브러리`이다. NVIDIA에서 제공하며, 특히 심층 신경망(deep neural networks)의 학습 및 추론을 가속화하는 데 사용된다.

### 역할

1. `딥러닝 성능 최적화`: 다양한 딥러닝 프레임워크와 연동하여 높은 성능을 발휘할 수 있도록 돕는다.
2. `학습 시간 단축`: 고성능 컴퓨팅 환경을 활용하여 모델 학습 시간을 크게 줄인다.

설치 방법 (UBUNTU 18.04LTS)
=======================

UBUNTU 18.04 LTS에 cuda12.1버전과 cudnn8.7.0버전을 설치하고 싶다고 가정하고 설치 방법에 대해서 설명해보겠다.

1. **NVIDIA 드라이버 설치**
---------------------

```
sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt update
ubuntu-drivers devices
sudo apt install nvidia-driver-550
```

* **`sudo add-apt-repository ppa:graphics-drivers/ppa`**: Ubuntu에 추가적인 소프트웨어 패키지를 제공하는 외부 저장소(PPA)를 추가한다. 이 저장소는 NVIDIA에서 제공하는 최신 그래픽 드라이버들을 포함하고 있다.
* **`sudo apt update`**: 시스템의 패키지 리스트를 업데이트해서 새로운 저장소의 내용을 포함시킨다. 이 과정을 통해 최신 드라이버를 검색하고 설치할 수 있게 준비하는 단계라고 이해하면 좋을 것 같다.
* **`ubuntu-drivers devices`**: 설치가능한 NVIDIA 그래픽 카드 드라이버 목록을 보여준다. 필자의 경우 팀 공용 서버로 1080 GPU를 사용하고 있고 해당 GPU의 가용 그래픽 카드 드라이버 목록은 아래와 같다. 뭐든 설치는 가능하지만 `recommend`해주는 것을 설치해보도록 하겠다.

![ubuntu-drivers](https://velog.velcdn.com/images/euisuk-chung/post/376eb9bf-645f-46d2-9bc5-d37bc20df401/image.png)

* **`sudo apt install nvidia-driver-550`**: 지정된 버전의 NVIDIA 그래픽 드라이버를 설치한다. 이 드라이버는 GPU와 운영 체제 간의 효율적인 통신을 가능하게 하고, 최적화된 성능을 제공해준다.

> 💡 **무슨 드라이버를 설치해야하는지 모르겠다고?**  
> 
> 위에 예시에는 직접 원하는 수동 버전의 드라이버를 설치하는 예시를 제시하고 있다.  
> 
> 하지만, 권장 드라이버를 자동으로 설치해주는 함수 또한 존재한다.  
> 
> ✍️ `sudo ubuntu-drivers autoinstall`

2. **CUDA 및 CUDA Toolkit 설치**
-----------------------------

필자는 파이토치를 사용할 것이므로 토치에서 요구하고 있는 cuda11.8을 설치해볼 예정이다.  

(참고: 이전 버전의 파이토치를 설치하려면? => <https://pytorch.org/get-started/previous-versions/>)

![torch](https://velog.velcdn.com/images/euisuk-chung/post/7005bf65-0d30-4ad2-894a-6c25360ad3ff/image.png)

CUDA Toolkit들의 다운로드 소스들을 다음 [링크](https://developer.nvidia.com/cuda-toolkit-archive)에서 제공되고 있다.

![CUDA Toolkit](https://velog.velcdn.com/images/euisuk-chung/post/b512a734-51e1-4e81-8a69-b1ed0a400cb3/image.png)

이 중에 하이라이트를 쳐준 11.8.0을 다운받아줄 것이다. 다음과 같이 본인의 서버(데스크탑) 환경에 맞게 설정을 해준다.

![11.8.0](https://velog.velcdn.com/images/euisuk-chung/post/a9358b65-7511-4b7d-8db2-603a17316d99/image.png)

```
wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda_11.8.0_520.61.05_linux.run
sudo sh cuda_11.8.0_520.61.05_linux.run
```

* **`wget`**: 지정된 URL에서 파일을 다운로드한다.
* **`sudo sh cuda_11.8.0_520.61.05_linux.run`**: 다운 받은 실행 파일을 쉘에서 실행하여 다운 받는다.

1. 실행하면 아래와 같은 다운로드 창이 나온다. (`ACCEPT`)  
   
   ![ACCEPT](https://velog.velcdn.com/images/euisuk-chung/post/83895203-b7c5-497b-8d70-fc0ac97b60a0/image.png)
2. 이미 앞에서 Driver 설치를 완료했으므로, Driver체크는 해제하고, CUDA설치를 진행한다.  
   
   ![CUDA설치](https://velog.velcdn.com/images/euisuk-chung/post/5c108775-6eba-4fc8-b741-255c3edc8e48/image.png)

> 어? CUDA를 설치했음에도 다음과 같은 에러가 발생하는데요?  
> 
> ![error](https://velog.velcdn.com/images/euisuk-chung/post/04fe2130-5d47-4679-96f4-a9a298e401b0/image.png)
> 
> ```
> # 접속 후 아래 코드 추가 (본인 CUDA버전에 맞게 설정할 것)
> vim ~/.bashrc 
> ```
> ```
> # https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#post-installation-actions%5B/url%5D
> export export PATH=/usr/local/cuda-11.8/bin${PATH:+:${PATH}}
> export LD_LIBRARY_PATH=/usr/local/cuda-11.8/lib64\
>                          ${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
> ```

3. **cuDNN 설치**
---------------

위에서 CUDA를 설치를 완료했고, 이제 CuDNN을 설치하려고 한다. Tensorflow의 경우, 특히나 CUDA 및 CuDNN의 버전에 민감하기 때문에 설치 시 버전에 유의해서 설치를 수행해야 한다.

* Tensorflow 지원 CUDA/CuDNN 버전 정보
  1. `Linux/MAC`: <https://www.tensorflow.org/install/source?hl=ko>
  2. `Windows`: <https://www.tensorflow.org/install/source_windows?hl=ko>

![Tensorflow](https://velog.velcdn.com/images/euisuk-chung/post/143df30b-3ae0-40e1-b4c9-2d4cd76da8d9/image.png)

위 그림을 보면 텐서플로우의 경우, CUDA 11.8이랑 같이 사용할 수 있는 cudnn은 8.6과 8.7인 것을 확인할 수 있다. 이제 아래 링크로 들어가서 cudnn 8.7을 다운받고 설치해보겠다.

* CuDNN 아카이브 : <https://developer.nvidia.com/rdp/cudnn-archive>

![CuDNN](https://velog.velcdn.com/images/euisuk-chung/post/cfff8753-c729-46e4-bf58-90faf5b2d864/image.png)

```
tar -xvf cudnn-linux-x86_64-8.7.0.84_cuda11-archive.tar.xz
sudo cp cudnn-linux-x86_64-8.7.0.84_cuda11-archive/include/cudnn*.h /usr/local/cuda-11.8/include
sudo cp -P cudnn-linux-x86_64-8.7.0.84_cuda11-archive/lib/libcudnn* /usr/local/cuda-11.8/lib64
sudo chmod a+r /usr/local/cuda-11.8/lib64/libcudnn*
```

* **`tar -xvf`**: 다운로드한 cuDNN의 압축을 풀어준다.
* **`sudo cp`**: cuDNN 라이브러리 파일과 헤더 파일을 적절한 CUDA 디렉토리로 복사한다. 이는 CUDA와 함께 cuDNN이 작동할 수 있도록 설정한다.
* **`sudo chmod a+r`**: 복사된 파일들에 대해 읽기 권한을 추가하여 다른 사용자도 이 파일들을 사용할 수 있도록 한다.

이미 특정 버전의 CUDA 및 cuDNN가 깔려있을 때
------------------------------

```
sudo apt-get --purge remove "cuda*"
sudo apt-get --purge remove "cudnn*"
```

* **`sudo apt-get --purge remove`**: 시스템에 설치된 CUDA 또는 cuDNN의 기존 버전을 완전히 제거한다. 이 명령은 설정 파일을 포함하여 관련된 모든 파일을 삭제한다.

설치 완료 후 버전 확인 코드
----------------

아래 두 코드 라인으로 각각 설치되어 있는 CUDA 및 CUDNN 버전을 확인할 수 있다.

* CUDA 버전 확인
  ```
  nvcc --version
  ```
  ```
  # 결과
  nvcc: NVIDIA (R) Cuda compiler driver
  Copyright (c) 2005-2022 NVIDIA Corporation
  Built on Wed_Sep_21_10:33:58_PDT_2022
  Cuda compilation tools, release 11.8, V11.8.89
  Build cuda_11.8.r11.8/compiler.31833905_0
  ```
* CUDNN 버전 확인
  ```
  cat /usr/local/cuda/include/cudnn_version.h | grep CUDNN_MAJOR -A 2
  ```
  ```
  # 결과
  #define CUDNN_MAJOR 8
  #define CUDNN_MINOR 7
  #define CUDNN_PATCHLEVEL 0
  --
  #define CUDNN_VERSION (CUDNN_MAJOR * 1000 + CUDNN_MINOR * 100 + CUDNN_PATCHLEVEL)
  ```
