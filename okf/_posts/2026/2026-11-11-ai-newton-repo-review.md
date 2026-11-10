---
type: "Repo Review"
title: "[Repo Review] AI-Newton, 실험 데이터에서 보존식을 찾고 법칙으로 남기는 코드"
description: "AI-Newton이 물리 시뮬레이션에서 관측값을 수집하고, Python과 Rust로 후보식을 찾은 뒤 Maple과 재실험으로 걸러내는 과정을 추적합니다."
date: "2026-11-11"
tags:
  - "Repo Review"
  - "Python"
  - "알고리즘"
  - "수학"
resource: "https://github.com/Science-Discovery/AI-Newton/tree/c143e865be42e067faf64cd8117cbeffd0fccfb6"
generated:
  by: "process:blog-review"
  at: "2026-11-11T06:08:50+09:00"
sources:
  - id: "science-discovery/ai-newton"
    resource: "https://github.com/Science-Discovery/AI-Newton/tree/c143e865be42e067faf64cd8117cbeffd0fccfb6"
    title: "AI-Newton"
status: "stable"
year: "2026"
analyzed_at: "2026-11-11T06:08:50+09:00"
source_id: "science-discovery/ai-newton"
source_revision: "c143e865be42e067faf64cd8117cbeffd0fccfb6"
source_title: "AI-Newton"
source_type: "repo"
source_url: "https://github.com/Science-Discovery/AI-Newton/tree/c143e865be42e067faf64cd8117cbeffd0fccfb6"
visual_sources:
  - path: "/img/reviews/2026/ai-newton-repo-review/discovery-flow.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/aiphy/main.py#L541-L630"
    caption: "리뷰어 작성, 분석 커밋 기준. 관측값 수집에서 법칙과 탐색 상태 저장까지."
    evidence_urls:
      - "https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/aiphy/specific_model.py#L413-L454"
      - "https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/aiphy/regression.py#L28-L42"
      - "https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/aiphy/general_model.py#L823-L885"
      - "https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/aiphy/main.py#L187-L215"
---

경사면을 움직이는 입자의 위치를 여러 번 기록했다고 해 보겠습니다. 위치를 시간으로 미분하면 속도를 얻을 수 있습니다. 다른 관측값과 속도를 조합하면 시간이 지나도 일정한 식을 찾을 수 있습니다. 그런데 한 궤적에서 일정했던 식이 출발점을 바꾸면 달라지거나, 이미 아는 식을 다시 쓴 결과일 수도 있습니다. AI-Newton은 후보식을 찾는 일, 실험 조건을 바꿔 다시 평가하는 일, 이미 저장된 법칙으로 설명할 수 있는지 검사하는 일을 코드에서 분리합니다. [고정 커밋](https://github.com/Science-Discovery/AI-Newton/tree/c143e865be42e067faf64cd8117cbeffd0fccfb6)

## 1. 실험 설정이 입력과 탐색 범위를 정합니다

자동 탐색 예제는 `Theorist`를 생성하고 등속 운동, 충돌, 낙하, 진동, 천체 운동 등의 실험을 추가합니다. `Theorist`가 먼저 Rust 지식 베이스의 내장 실험을 가져오고, 예제는 그 위에 `register_experiment`를 38회 명시적으로 호출합니다. 각 등록은 관측 가능한 기본 개념을 추가하고, 실험 설정에 제공된 기하학 관계도 실험별 결론에 넣으려 시도합니다. 분석 범위는 이 커밋의 예제 코드이며, 논문에서 보고한 평가 설정 전체와는 구성이 다릅니다. [기본 초기화](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/aiphy/main.py#L71-L84) · [내장 실험](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/src/knowledge.rs#L70-L80) · [예제 진입점](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/test/examples/test_example_1.py#L52-L104) · [실험 등록](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/aiphy/manager.py#L223-L243)

`motion_3d`에서는 입자·시계·경사면의 역할과 관측 채널이 미리 지정됩니다. 초기 위치와 각도, 속도 범위가 있고, `do_experiment`는 중력 상수와 운동식을 써서 좌표 시계열을 만든 뒤 가우시안 잡음을 더합니다. 경사 방향의 성분과 기하학적 보존 관계도 실험이 제공합니다. 이 예제에서 탐색기가 받는 것은 실험 코드가 생성한 시계열, 객체 타입과 관측 채널, 설정에 등록된 기하학 관계입니다. 따라서 README의 ‘사전 물리 지식 없이 발견한다’는 설명을 읽을 때는 **시뮬레이터를 정의하는 쪽이 제공하는 정보**와 **탐색기가 새로 도출하는 관계**를 구분해야 합니다. [경사면 시뮬레이터](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/aiphy/experiment/basic/motion.py#L9-L79) · [README의 목표](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/README.md#L1-L3)

![실험 시계열을 수집하고 후보식을 탐색한 뒤 재실험과 Maple 검사를 거쳐 법칙과 탐색 상태에 반영하는 흐름]({{ '/img/reviews/2026/ai-newton-repo-review/discovery-flow.svg' | relative_url }})

*그림 1. 리뷰어 작성, 분석 커밋 기준. Python이 실험과 탐색 순서를 정하고 Rust가 관측값과 식을 처리합니다. Maple과 재실험은 후보가 지식 베이스에 남는 과정에서 서로 다른 검사를 맡습니다.* [탐색 제어](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/aiphy/main.py#L435-L488) · [후보 생성과 검사](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/aiphy/main.py#L541-L630) · [저장](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/aiphy/main.py#L187-L215)

관측 수집은 Python에서 Rust로, 그리고 이 예제에서는 다시 Python으로 건너갑니다. `SpecificModel.experiments_reset`이 실험 조건을 무작위로 설정하고 Rust 바인딩의 `collect_expdata`를 호출합니다. 경사면 실험은 `DoExpType(__file__)`로 등록하므로, Rust의 `DoExpType`이 Python 파일에서 `do_experiment`를 불러 시간 범위, 샘플 수, 잡음, 실험 설정을 전달하고 반환값을 자료 구조로 받습니다. Rust 내장 실험은 같은 타입의 함수 포인터 분기를 사용합니다. [Python 실험 초기화](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/aiphy/specific_model.py#L413-L418) · [수집 바인딩](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/src/experiments/topy.rs#L171-L176) · [실험 콜백](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/src/experiments/expstructure.rs#L96-L123)

## 2. DSL은 식에 실험 객체를 연결합니다

`Exp`는 좌표, 사칙연산, 미분 같은 식을 표현합니다. `Concept`는 여기에 객체 타입과 자리표시자를 묶을 수 있고, `Proposition`은 식 또는 개념이 항상 0인지, 시간에 따라 보존되는지 구분합니다. 저장소에 포함된 결과에서 `C_02`는 입자의 y좌표를 시간으로 미분한 개념입니다. `C_18`은 그 개념을 한 번 더 시간으로 미분합니다. 아래는 저장된 정의 일부입니다. [저장된 정의](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/data/test_cases/example_1/2/2_knowledge.txt#L6-L23) · [명제 문법](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/src/expr.lalrpop#L98-L119) · [객체와 미분 문법](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/src/expr.lalrpop#L128-L174)

```text
C_02 := (1->Particle) |- D[posy[1]]/D[t[0]]
C_18 := (1->Particle) |- D[C_02[1]]/D[t[0]]
```

`(1->Particle)`의 `1`은 개념 정의 안에서 입자를 가리키는 자리입니다. 실험별 객체에 개념을 대입하면 실제 평가할 식이 나옵니다. 반대로 Rust의 일반화 코드는 실험의 객체 번호를 타입이 달린 자리로 바꾸고, 같은 유형의 모든 객체에서 동일한 항 구조가 확인되면 `[Sum:Particle]` 같은 합으로 묶을 수 있습니다. 평가기는 기본 개념의 데이터를 조회하고, 파생 개념은 식을 재귀적으로 풀어 계산한 뒤 평가 맥락에 캐시합니다. [Rust 일반화](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/src/semantic/generalize.rs#L9-L15) · [객체 번호와 타입 치환](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/src/semantic/generalize.rs#L46-L120) · [파생식 평가](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/src/semantic/evaluation.rs#L306-L351)

## 3. Python은 어디를 볼지, Rust는 어떤 조합을 볼지 정합니다

`perform_discovery`는 먼저 시간 예산 안에 분석을 마치는 실험 풀을 구성합니다. 기본 UCB 선택에서는 아직 시도하지 않은 실험 중 하나를 먼저 고르고, 이후에는 보상과 탐색 항을 합한 점수가 가장 높은 실험을 선택합니다. 실험 분석은 자식 프로세스로 돌며, 시간이 넘으면 종료하고 해당 실험에 0 보상을 반영합니다. 탐색할 개념 그룹을 정하는 규칙은 따로 있습니다. 현재 실험에 대입할 수 있는 개념으로 세 개짜리 그룹을 구성하고, 과거 부분집합 보상, 방문 횟수, PyTorch 정책 네트워크 출력을 조합한 점수의 제곱을 가중치로 샘플링합니다. [실험 풀](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/aiphy/main.py#L375-L420) · [프로세스 시간 제한](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/aiphy/main.py#L250-L303) · [실험 선택](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/aiphy/memory.py#L59-L80) · [실험 점수](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/aiphy/ucb.py#L22-L30) · [개념 그룹 선택](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/aiphy/memory.py#L175-L221)

선택된 개념을 실험의 객체에 대입해 `Knowledge.eval`로 값을 만들면 `DataStruct`가 구성됩니다. 평가 중 예외가 난 식은 이 자료 구조에서 빠집니다. 자동 루프의 `ver3`는 Rust 함수만 가리키는 이름처럼 보이지만, 실제 Python 디스패치는 Rust 검색과 PCA 검색을 모두 호출하고 식을 키로 결과를 합칩니다. Rust는 단항식과 제곱을 포함한 곱·비율 등을 만들고 Rayon으로 후보를 병렬 평가합니다. PCA 쪽은 평균을 뺀 시계열에서 선형 조합의 계수를 찾고, 복원한 조합이 보존될 때 후보에 넣습니다. [자동 루프의 버전 선택](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/aiphy/main.py#L217-L232) · [자료 구조 생성](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/aiphy/specific_model.py#L441-L454) · [두 검색을 합치는 디스패치](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/aiphy/regression.py#L14-L42) · [PyO3 함수 등록](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/src/lib.rs#L44-L57) · [Rust 조합 탐색](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/src/regression.rs#L174-L233) · [PCA 후보 구성](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/aiphy/pca.py#L536-L586)

## 4. 수치 검증과 기호적 축약은 다른 질문에 답합니다

`doit`는 검색 결과를 `IsZero` 또는 `IsConserved`로 바꾸고, 이미 본 표현식을 제외한 뒤 새 후보를 메모리에 기록합니다. 이후 기존 식으로부터 줄일 수 있는 후보를 걸러내고 별도 테스트 실험에 대입합니다. 메모리에 기록되는 시점이 이 두 필터보다 앞이므로, ‘본 후보’와 ‘검증을 통과해 채택된 식’은 서로 다른 상태입니다. [후보 변환과 필터 순서](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/aiphy/main.py#L599-L630)

| 검사 | 어떤 질문에 답하나요? | 코드가 보는 근거 |
| --- | --- | --- |
| 조건을 바꾼 수치 재실험 | 같은 실험에서 초기 조건이 달라져도 후보식이 성립하나요? | 무작위로 설정한 실험 복제본 10개 중 8개 이상에서 해당 식이 0 또는 보존으로 분류되어야 합니다. |
| 기호적 축약 | 이 식을 기존 관계로부터 이미 설명할 수 있나요? | 식을 SymPy로 펼치고, 기존 관계로 만든 미분대수 구조를 사용해 후보식을 축약합니다. |
| 다른 실험으로 일반화 | 객체 타입을 기준으로 같은 식을 다른 실험에 대입할 수 있나요? | 현재 실험에서 성립한 후보를 일반화한 뒤, 적어도 두 개의 다른 등록 실험에서 성립해야 신규 일반 법칙으로 등록됩니다. |

수치 재실험은 같은 `SpecificModel`에 보관된 테스트 복제본을 재사용합니다. 일반 법칙의 신규 등록 경로는 그 8/10 검사와 별도로 `check_general_laws`를 호출합니다. 해당 함수는 이미 성립한다고 기록한 실험 결과를 재사용하고, 새로 검사하는 실험에서는 그 실험의 현재 관측 데이터에 가능한 모든 대입을 평가합니다. 적용 가능한 객체가 없는 실험은 이 단계에서 성립으로 세지 않습니다. 따라서 저장된 `valid_experiments`는 그 법칙을 뒷받침한 실험 목록으로 읽을 수 있습니다. [8/10 수치 기준](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/aiphy/specific_model.py#L652-L695) · [다른 실험 검사](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/aiphy/general_model.py#L230-L263) · [일반 법칙 등록 조건](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/aiphy/general_model.py#L823-L885)

Maple은 기존 관계가 새 후보를 설명할 수 있는지 기호적으로 판단하는 데 쓰입니다. 실험별 필터는 복잡도에 따라 기존 관계의 미분대수 구조를 골라 후보가 남는지 봅니다. Maple 어댑터는 `RosenfeldGroebner`로 구조를 구성하고 `NormalForm`으로 식을 축약합니다. 명령 전달은 Python이 `/opt/maple2024/bin/maple`을 별도 프로세스로 실행하는 방식입니다. 일반 법칙에도 실험 범위와 식의 축약 결과를 이용하는 별도 정리 단계가 있습니다. [실험별 기호 필터](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/aiphy/specific_model.py#L736-L767) · [미분대수 구조 생성](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/aiphy/diffalg/diffalg.py#L174-L190) · [NormalForm 호출](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/aiphy/diffalg/diffalg.py#L105-L125) · [Maple 프로세스](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/aiphy/diffalg/mapleIO.py#L23-L55) · [일반 법칙 정리](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/aiphy/general_model.py#L1180-L1200)

## 5. 저장된 법칙은 정의와 적용 실험을 함께 읽어야 합니다

새 결론은 실험별 모델에 들어가고, 여러 실험에서 적용되는 관계는 일반 모델에 등록됩니다. 정리 과정에서 살아남은 식에서 개념을 추출해 등록하면, 다음 반복에서 그 개념도 다시 조합 재료로 쓸 수 있습니다. 한 실험의 결과가 다음 실험에서 검색할 표현식의 집합을 바꾸는 셈입니다. [실험별 결론 반영](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/aiphy/main.py#L632-L682) · [일반화와 개념 등록](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/aiphy/main.py#L684-L718)

포함된 결과의 `R_02`는 `C_18[1] is zero`를 입자에 대한 일반 명제로 저장합니다. 정의를 풀면 특정 실험들에서 입자의 y방향 가속도가 0으로 평가된 관계입니다. 어떤 실험들이 이를 만족했는지는 같은 결과의 `2_general_model.json`에서 확인할 수 있습니다. 이 JSON의 역할은 ‘이 식을 지지한 실험 목록’을 붙여, 이름이나 짧은 식만으로는 보이지 않는 적용 범위를 남기는 것입니다. [R_02 원문](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/data/test_cases/example_1/2/2_knowledge.txt#L114-L120) · [R_02의 적용 실험](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/data/test_cases/example_1/2/2_general_model.json#L1-L34)

`save_to_file`은 지식 베이스 텍스트와 탐색 메모리·일반 모델·실험별 모델·객체 모델의 JSON을 분리해 기록합니다. 정책 네트워크 가중치는 별도 `.pth`로 저장하고, `read_from_file`이 해당 파일들을 읽어 상태를 재구성합니다. 예제의 기본 진입점은 새 인스턴스를 만들며 복구 호출은 주석으로 제시되어 있습니다. [저장 구현](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/aiphy/main.py#L187-L215) · [복구 구현](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/aiphy/main.py#L120-L185) · [예제 초기화](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/test/examples/test_example_1.py#L52-L55)

## 6. 실행 환경과 리뷰 범위

README는 Linux·CUDA, Python 3.11.9 이상, Rust 1.84.0, Maple 2024를 안내합니다. 반면 `pyproject.toml`의 선언은 Python 3.10 이상이며, `Cargo.toml`은 PyO3를 쓰는 `cdylib`를 정의합니다. 실제 개념 그룹 선택은 일정 수 이상의 개념이 있을 때 CUDA 장치를 직접 지정하고, 기호적 축약은 위의 Maple 경로에 의존합니다. README의 수동 벤치마크 노트북과 자동 탐색 예제는 별도 진입점입니다. 이 글은 자동 예제의 정적 코드와 저장소에 포함된 결과 파일을 검토했습니다. 벤치마크 수치나 다른 운영체제·Python 버전의 동작은 실행으로 확인하지 않았습니다. [README의 실행 안내](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/README.md#L5-L41) · [Python 패키지 명세](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/pyproject.toml#L1-L15) · [Rust 매니페스트](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/Cargo.toml#L1-L16) · [CUDA 선택 구현](https://github.com/Science-Discovery/AI-Newton/blob/c143e865be42e067faf64cd8117cbeffd0fccfb6/aiphy/memory.py#L191-L219)
