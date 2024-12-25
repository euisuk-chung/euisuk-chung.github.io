---
title: "[설치] pipenv로 pyenv 뽕 뽑기"
date: "2024-04-27"
tags:
  - "pyenv/pipenv"
  - "환경"
year: "2024"
---

# [설치] pipenv로 pyenv 뽕 뽑기

원본 게시글: https://velog.io/@euisuk-chung/pipenv-너도-같이-오고-pyenv-pipenv



지난 번 포스팅에서는 `pyenv`에 대해서 살펴보고 이를 리눅스 환경(+Window환경)에 설치하는 방법에 대해서 살펴봤는데요([링크](https://velog.io/@euisuk-chung/Goodbye-Conda-Hello-PyENV)) 이번 포스팅에서는 pyenv의 효과를 극대화할 수 있는 pipenv에 대해서 살펴보고, 이를 어떻게 사용할지 알아보도록 하겠습니다 🤗

### 1. pipenv란?

* **정의**: pipenv는 파이썬의 의존성 관리와 가상 환경을 통합적으로 관리하는 도구입니다. 이 도구는 `Pipfile`과 `Pipfile.lock` 파일을 이용하여 의존성을 명시하고, 프로젝트마다 독립된 가상 환경을 생성하여 관리합니다. 이를 통해 개발 환경의 일관성과 재현성을 보장합니다.

### 2. pipenv 설치 방법

* **pipenv 설치**:
  ```
  pip install pipenv
  ```
  이 명령은 시스템에 pipenv를 설치합니다. 특정 사용자에 국한하지 않고 시스템 전체에 설치됩니다.

### 3. pipenv 가상 환경 생성 및 관리

* (참고) 내 PyENV 환경에 설치된 파이썬 버전 리스트 확인하기
  
  ```
  pyenv versions # check installed envs
  ```
* **가상 환경 생성**:
  
  ```
  mkdir MyProject
  cd MyProject
  pipenv --python 3.9.1
  ```
  
  이 명령은 프로젝트 디렉토리 내에 `Pipfile`을 생성하고 지정된 파이썬 버전으로 가상 환경을 초기화합니다.
* **가상 환경 활성화 및 비활성화**:
  
  ```
  pipenv shell   # 활성화
  exit           # 비활성화
  ```
* **pyenv와의 연동**:
  
  + 시스템에 원하는 파이썬 버전이 없는 경우, pipenv는 pyenv를 통해 자동으로 해당 버전을 설치하도록 요청할 수 있습니다.

### 4. Pipfile?

`Pipfile`은 일반적으로 프로젝트의 루트 디렉토리에 위치하게 됩니다. 이 파일은 프로젝트와 관련된 파이썬 의존성을 관리하기 위한 주요 파일로, 프로젝트 폴더에 직접 생성됩니다.

* Pipfile의 위치: Pipfile은 프로젝트 폴더 안에 위치합니다. 예를 들어, 프로젝트 폴더가 MyProject라면, MyProject/Pipfile에 위치하게 됩니다.
* Pipfile의 확장자: Pipfile은 확장자 없이 그냥 Pipfile로 저장됩니다. 이와는 별개로, 의존성을 고정하는 Pipfile.lock 파일도 같은 폴더에 생성되며, 이 파일 역시 확장자가 없습니다.
* **Pipfile과 Pipfile.lock의 사용**:
  
  + `Pipfile`: 프로젝트에 필요한 패키지와 파이썬 버전을 선언적으로 명시합니다.
  + `Pipfile.lock`: `pipenv lock` 명령을 실행하여 생성되며, 이 파일은 `Pipfile`의 선언된 의존성에 대한 구체적인 버전 정보와 해시값을 포함합니다. 이 파일을 통해 프로젝트가 다른 시스템에서 동일하게 재현될 수 있습니다.
* **Lock 파일 생성 및 사용 예시**:
  
  ```
  pipenv install numpy  # numpy 설치
  pipenv lock           # Pipfile.lock 생성 및 업데이트
  ```
  
  프로젝트를 배포하거나 다른 개발 환경에서 작업을 재개할 때 `Pipfile.lock`을 사용하여 정확히 같은 의존성을 설치합니다.

### 5. pipenv lock?

✔️ **`pipenv lock` 명령의 역할**

* **종속성 잠금:** `pipenv lock`은 `Pipfile`에 명시된 종속성을 기반으로 `Pipfile.lock` 파일을 생성하거나 업데이트합니다. 이 파일은 프로젝트의 모든 종속성과 그 정확한 버전을 포함하고, 이를 통해 개발 환경의 일관성을 유지합니다.
* **환경 재현:** `Pipfile.lock`은 프로젝트를 다른 시스템이나 다른 개발자에게 전달할 때 동일한 종속성을 확실하게 재현할 수 있게 해줍니다. 이는 모든 사용자가 동일한 환경에서 작업할 수 있도록 보장합니다.

> 💡 **Q.** `pipenv install numpy` 만 수행해도, pipfile은 업데이트가 될텐데, 굳이 lock을 해주는 이유가 뭘까요?  
> 
> 📖 **A.** `pipenv install` 명령어를 사용하면 자동으로 Pipfile이 업데이트되며, 필요한 패키지가 설치됩니다. 그런데 pipenv lock 명령어를 실행하는 것은 추가적인 목적을 가지고 있습니다.

✔️ **`pipenv install`과 `pipenv lock`의 차이**

* **`pipenv install`:** 이 명령은 `Pipfile`에 명시된 패키지를 설치하고 자동으로 `Pipfile.lock`을 업데이트합니다. 이 과정에서 새로운 패키지가 설치되거나 업데이트될 때마다 `Pipfile.lock`이 갱신되어 현재 환경을 반영합니다.
* **`pipenv lock`:** 이 명령은 실제로 패키지를 설치하지 않고, 현재 `Pipfile`의 상태를 바탕으로 `Pipfile.lock`만을 갱신합니다. 이는 패키지를 실제로 설치하지 않고도 종속성을 정확히 잠그고 싶을 때 유용합니다. `pipenv lock` 명령을 사용해야 하는 몇 가지 특별한 경우를 살펴보겠습니다:
  
  1. **종속성 파일(Pipfile)의 수동 변경**: 개발자가 `Pipfile`을 수동으로 편집하여 패키지 버전을 변경하거나 새 패키지를 추가하는 경우, `Pipfile.lock`을 갱신해야 그 변경사항이 정확하게 반영됩니다. 이는 `Pipfile`의 상태가 `Pipfile.lock`과 동기화되도록 하는 데 필요합니다.
  2. **하위 종속성(패키지)의 업데이트**: 패키지의 하위 종속성이 업데이트되었을 경우, `pipenv lock` 명령을 실행하여 이러한 변경사항을 `Pipfile.lock`에 반영할 수 있습니다. 이는 하위 패키지의 버전 변동이 상위 패키지의 기능성에 영향을 미칠 수 있기 때문입니다.
  3. **보안 패치 업데이트**: 보안 취약점이 발견되어 해당 패키지의 새로운 버전이 출시되었을 때, `pipenv lock`을 사용하여 최신 보안 패치가 적용된 버전으로 종속성을 갱신할 수 있습니다. 이는 프로젝트의 보안을 강화하는 데 중요합니다.
  4. **호환성 검증(새 환경 테스트)**: 프로젝트를 새로운 환경에 배포하기 전에 `pipenv lock`을 실행하여 최신 종속성 상태를 확정하고, 이를 통해 새 환경에서의 호환성을 검증할 수 있습니다. 이 과정은 배포 전 충돌을 방지하는 데 도움이 됩니다.
  5. **CI/CD 파이프라인(지속적 통합/배포)**: CI/CD 파이프라인에서 `Pipfile.lock`을 주기적으로 갱신하여 프로젝트의 종속성이 항상 최신 상태로 유지되고, 배포 시점에 문제가 발생하지 않도록 할 수 있습니다.

### 6. 프로젝트별 가상 환경 설정

* 가상 환경은 프로젝트 디렉토리에 기반하여 자동으로 이름이 생성되며, 관리는 `~/.local/share/virtualenvs` 디렉토리에서 이루어집니다.
* **TensorFlow와 PyTorch 프로젝트 예시**:
  
  ```
  # Tensorflow_ObjectDetection 프로젝트 생성
  mkdir Tensorflow_ObjectDetection
  cd Tensorflow_ObjectDetection
  pipenv --python 3.9.1
  pipenv install tensorflow
  pipenv shell # 프로젝트 가상환경 실행
  ```
  ```
  # PyTorch_AnomalyDetection 프로젝트 생성
  mkdir PyTorch_AnomalyDetection
  cd PyTorch_AnomalyDetection
  pipenv --python 3.9.1
  pipenv install torch torchvision
  pipenv shell # 프로젝트 가상환경 실행
  ```

> 💡 Pipfiles(Pipfile, Pipfile.lock)은 Git repository에 추가하는 것이 좋습니다. 만약 다른사람이 repository을 clone 하면 Pipenv을 해당 시스템에 설치하고 `pipenv install`를 수행하면 Pipenv는 자동으로 Pipfiles를 찾아서 새로운 가상 환경을 만들고 필요한 패키지들을 설치합니다.

### 7. pipenv 명령어

#### 기본 명령어

* **`pipenv install`**: 프로젝트 초기화 또는 `Pipfile`에 기록된 모든 패키지를 설치합니다. 특정 패키지를 명시할 경우 해당 패키지를 설치하고 `Pipfile`을 업데이트합니다.
* **`pipenv uninstall`**: 지정된 패키지를 가상 환경에서 제거하고 `Pipfile`에서 해당 항목을 제거합니다.
* **`pipenv lock`**: 현재 가상 환경에 설치된 모든 의존성을 `Pipfile.lock`에 고정합니다. 이 파일을 사용하면 다른 환경에서 동일한 패키지 설정으로 환경을 재현할 수 있습니다.
* **`pipenv graph`**: 현재 설치된 의존성의 그래프를 표시합니다. 이는 패키지 간의 의존 관계를 시각적으로 이해하는데 도움을 줍니다.

#### 보안 및 정리 명령어

* **`pipenv check`**: 설치된 패키지를 PyUp Safety를 통해 보안 취약점이 있는지 검사하고, `Pipfile`에 명시된 PEP 508 마커와의 호환성을 확인합니다.
* **`pipenv clean`**: `Pipfile.lock`에 명시되지 않은 모든 패키지를 제거합니다. 이는 가상 환경을 깨끗하게 유지하는 데 유용합니다.

#### 가상 환경 관리 명령어

* **`pipenv shell`**: 가상 환경 내에 쉘을 시작합니다. 이는 개발 환경을 가상 환경으로 한정하여 작업할 때 사용됩니다.
* **`pipenv --rm`**: 현재 프로젝트의 가상 환경을 제거합니다. 이 명령은 가상 환경을 완전히 삭제하지만, `Pipfile`과 `Pipfile.lock`은 유지됩니다.

#### 패키지 동기화 및 업데이트 명령어

* **`pipenv sync`**: `Pipfile.lock`에 명시된 정확한 패키지 버전을 설치합니다. 이는 프로젝트를 새로 시작하거나 다른 개발자와 환경을 동기화할 때 유용합니다.
* **`pipenv update`**: `pipenv lock`을 실행하여 모든 패키지를 최신 버전으로 업데이트하고, 이어서 `pipenv sync`를 실행하여 이러한 변경 사항을 적용합니다.

#### 추가 유용한 옵션

* **`--verbose`**: 상세한 출력 모드로 전환합니다. 명령 실행 중 발생하는 내부 과정을 더 자세히 볼 수 있습니다.
* **`--support`**: 문제 해결을 위한 진단 정보를 제공합니다. 이는 GitHub 이슈 등에서 문제를 보고할 때 유용하게 사용될 수 있습니다.
* **`--python [version]`**: 가상 환경을 생성할 때 사용할 특정 파이썬 버전을 지정합니다.
* **`--clear`**: pipenv, pip, 및 pip-tools 관련 캐시를 모두 지웁니다. 이는 문제 해결 시 유용하게 사용할 수 있습니다.

### 유첨1

> 🤔 그렇다면 기존 pip 중에 **-U** 또는 **-q** 파라미터가 붙은 것들은 어떻게 할까요?
> 
> ```
> pip install -q -U bitsandbytes
> pip install -q -U git+https://github.com/huggingface/transformers.git
> pip install -q -U git+https://github.com/huggingface/peft.git
> pip install -q -U git+https://github.com/huggingface/accelerate.git
> ```
> 
> pipenv는 기본적으로 종속성 관리를 위해 항상 가능한 최신 버전의 패키지를 설치하려고 하기 때문에 -U가 없습니다. pip → pipenv로 변경만 해주면 완료! 🚩
> 
> ```
> pipenv install -q git+https://github.com/huggingface/transformers.git
> pipenv install -q git+https://github.com/huggingface/peft.git
> pipenv install -q git+https://github.com/huggingface/accelerate.git
> ```

> ✍️ (참고) pip 명령어에서 사용하는 -q와 -U 옵션의 의미  
> 
> **-q (Quiet)** : `-q` 옵션은 "quiet" 모드로 설치를 수행하는 것을 의미합니다. 즉, 명령어 실행 시 출력되는 메시지의 양을 줄여줍니다. 보통은 설치 과정 중의 상세한 정보를 최소화하고 싶을 때 사용합니다. -qq로 지정하면 출력을 더욱 줄일 수 있습니다.  
> 
> **-U (Upgrade)** : `-U` 옵션은 "upgrade"의 약자로, 지정된 패키지를 최신 버전으로 업그레이드하라는 지시입니다. 만약 해당 패키지가 이미 시스템에 설치되어 있다면, -U 옵션을 통해 최신 버전으로 업데이트할 수 있습니다. 패키지가 설치되어 있지 않은 경우에는 새로 설치합니다.

### 유첨2

만약, `pip install`을 사용하여 패키지를 설치했지만 `pipenv` 환경에서 관리하고 싶은 경우, `Pipfile`에 해당 패키지를 명시적으로 추가하는 과정이 필요합니다. 이는 `pipenv`가 프로젝트의 종속성을 `Pipfile`과 `Pipfile.lock`을 통해 관리하기 때문입니다. 다음은 `pipfile`에 pip으로 설치한 패키지를 추가하는 방법을 단계별로 설명합니다.

#### 1. `Pipfile` 열기

프로젝트 디렉토리에서 `Pipfile`을 텍스트 편집기로 열어줍니다. `Pipfile`은 일반적으로 프로젝트의 루트 디렉토리에 위치합니다.

#### 2. 패키지 추가

`Pipfile`의 `[packages]` 섹션에 추가하고자 하는 패키지를 다음과 같이 기재합니다. 여기서 패키지 이름과 원하는 버전 규칙을 지정할 수 있습니다. `*`는 최신 버전을 자동으로 선택하라는 의미입니다:

```
[packages]
requests = "*"  # 최신 버전을 사용하고자 할 때
flask = "==1.1.2"  # 특정 버전을 명시하고자 할 때
numpy = ">=1.18.5"  # 최소 버전 요구사항을 명시하고자 할 때
```
#### 3. `Pipfile.lock` 업데이트

수동으로 `Pipfile`을 편집한 후, `Pipfile.lock`을 업데이트해야 종속성이 올바르게 반영됩니다. 터미널에서 다음 명령을 실행합니다. 이 명령은 `Pipfile`의 변경사항을 바탕으로 `Pipfile.lock`을 새롭게 생성합니다:

```
pipenv lock
```
#### 4. 패키지 설치

수정된 `Pipfile`을 바탕으로 필요한 패키지를 설치하려면 다음 명령을 사용합니다. 이 명령은 `Pipfile`에 명시된 모든 패키지를 설치하고, `Pipfile.lock`과 일치시킵니다:

```
pipenv install
```
#### 주의사항

* **버전 호환성**: 패키지 버전을 수동으로 지정할 때는 호환성을 고려해야 합니다. 설치하려는 패키지가 프로젝트에 이미 있는 다른 패키지와 호환되는지 확인해야 합니다.
* **문법 오류**: `Pipfile`을 편집할 때 문법을 정확하게 지켜야 합니다. TOML 문법 오류는 `pipenv` 명령을 실행할 때 문제를 일으킬 수 있습니다.

오늘도 긴 글 읽어주셔서 감사합니다 ✌

