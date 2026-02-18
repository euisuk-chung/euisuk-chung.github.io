---
title: "[Conda] 활용 가이드: 효율적인 환경 관리와 Jupyter Kernel 설정"
date: "2024-03-06"
year: "2024"
---

# [Conda] 활용 가이드: 효율적인 환경 관리와 Jupyter Kernel 설정

Conda는 다양한 프로젝트에 필요한 독립된 환경을 만들고 관리할 수 있는 강력한 도구입니다. 이 글에서는 Conda 환경 설정, 관리, Jupyter Notebook에서의 활용법 등 몇 가지 유용한 Conda 사용법을 소개합니다. 또한, 특정 상황에서 `conda activate` 대신 `source activate`를 사용해야 하는 경우와 그 이유에 대해서도 알아보겠습니다.

Conda 환경 관리
-----------

### 환경 목록 확인

```
conda env list
```

이 명령어는 설치된 모든 Conda 환경의 목록을 보여줍니다. 현재 활성화된 환경 옆에는 별표(\*)가 표시됩니다.

### 새 환경 생성

```
conda create --name py39 python=3.9
```

이 명령어는 Python 버전 3.9를 포함한 새 Conda 환경 `py39`를 생성합니다. 필요에 따라 다른 패키지를 함께 설치할 수도 있습니다.

### 환경 제거

```
conda remove --name py39 --all
```

이 명령어는 `py39` 환경과 그 안에 설치된 모든 패키지를 제거합니다.

### 환경 버전 확인 및 되돌리기

```
conda list --revisions
conda install --revision 2
```

이 명령어들을 사용하여 환경의 이전 상태로 롤백할 수 있습니다. `conda list --revisions`는 환경의 변경 이력을 보여주며, `conda install --revision 2`는 특정 리비전으로 환경을 되돌립니다.

### Conda 캐시 청소

```
conda clean -a
```

이 명령어는 Conda가 다운로드한 패키지 파일과 캐시를 정리하여 디스크 공간을 확보합니다.

Jupyter Kernel 설정
-----------------

Jupyter Notebook에서 Conda 환경을 Kernel로 사용하려면, 해당 환경을 활성화한 후 아래 단계를 따르면 됩니다.

```
pip install ipykernel
python -m ipykernel install --user --name py39
```

이 과정을 통해 Jupyter Notebook에서 `py39` 환경을 선택할 수 있는 Kernel이 추가됩니다.

`conda activate`가 안돼?!
----------------------

![](https://velog.velcdn.com/images/euisuk-chung/post/19cb7da3-d236-42b5-b95e-0bb7cafa36f4/image.png)

가끔은 `conda activate` 대신 `source activate <환경 이름>`을 사용해야 하는 경우가 있습니다. 이는 주로 쉘 환경 설정이 Conda 초기화 스크립트와 완벽히 통합되지 않았을 때 발생합니다. 예를 들어, Bash 쉘을 사용하지 않는 경우나, Conda 설치 후 쉘 설정 파일(`.bashrc`, `.zshrc` 등)이 업데이트되지 않았을 때 이 문제가 발생할 수 있습니다. `source activate` 명령어는 Conda 환경을 활성화하기 위한 보다 일반적인 방법으로, 다양한 쉘 환경에서도 잘 작동합니다.

Conda 설치 후 쉘 설정 파일(`.bashrc`, `.zshrc` 등)이 자동으로 업데이트되지 않아 `conda activate` 명령어가 제대로 작동하지 않는 경우가 있습니다. 이 문제를 해결하기 위해, 수동으로 Conda 초기화 과정을 진행해야 합니다. 다음 단계를 따라 쉘 설정 파일을 업데이트하고, `conda activate` 명령어가 정상적으로 작동하도록 설정할 수 있습니다.

> ### 💡초기화 방법
>
> 1. **Conda 초기화 실행**  
>    Conda를 처음 설치한 후, 쉘에서 Conda를 올바르게 초기화하기 위해 다음 명령어를 실행합니다. 이 명령은 현재 사용 중인 쉘에 맞게 Conda를 초기화하고, 필요한 설정을 쉘의 구성 파일에 추가합니다.
>
>    ```
>    conda init
>    ```
>
>    `conda init` 명령은 현재 사용 중인 쉘을 자동으로 감지하여, 해당 쉘의 구성 파일에 초기화 스크립트를 추가합니다. Bash, Zsh, Fish, PowerShell 등 다양한 쉘을 지원합니다.
> 2. **쉘 구성 파일 수동 편집**  
>    만약 `conda init` 명령어 실행 후에도 `conda activate`가 여전히 작동하지 않는다면, 쉘 구성 파일을 직접 편집할 수 있습니다. Bash를 사용하는 경우 `.bashrc`, Zsh를 사용하는 경우 `.zshrc` 파일을 편집합니다.
>    * Bash 사용자의 경우:
>
>      ```
>      		echo ". /home/<username>/miniconda3/etc/profile.d/conda.sh" >> ~/.bashrc
>      ```
>    * Zsh 사용자의 경우:
>
>      ```
>      		echo ". /home/<username>/miniconda3/etc/profile.d/conda.sh" >> ~/.zshrc
>      ```
> 3. **쉘 재시작**  
>    설정 파일을 업데이트한 후, 쉘을 재시작하거나 새 터미널 창을 열어 변경사항을 적용합니다. 이제 `conda activate` 명령어가 정상적으로 작동해야 합니다.  
>    이 단계들을 수행함으로써, `conda activate` 명령어가 작동하지 않는 문제를 해결할 수 있습니다. Conda 환경을 원활하게 활성화하고 관리할 수 있는 기반을 마련하게 됩니다.

결론
--

Conda는 데이터 과학, 기계 학습 프로젝트 등 다양한 개발 환경에서 유용하게 사용될 수 있는 강력한 도구입니다.

이 글을 통해 Conda 환경의 생성, 관리, Jupyter Notebook에서의 활용 방법 등을 알아보았습니다. 또한, `conda activate` 명령어가 작동하지 않을 때의 대안으로 `source activate` 사용법도 함께 소개했습니다.

Conda를 효율적으로 사용함으로써 프로젝트 관리를 보다 원활하게 진행할 수 있기를 바랍니다.