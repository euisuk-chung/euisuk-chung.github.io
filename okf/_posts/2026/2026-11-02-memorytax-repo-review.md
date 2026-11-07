---
type: "Repo Review"
title: "[Repo Review] MemoryTax: 에이전트 기억 평가의 데이터·프롬프트·판정 경계 읽기"
description: "MemoryTax의 고정 데이터·표본 준비, QA 메시지 생성과 judge 파싱을 추적하고, 아직 공개되지 않은 검색·API 계측·평가 실행기의 경계를 분석합니다."
date: "2026-11-02"
tags:
  - "Repo Review"
  - "AI Agent"
  - "RAG"
  - "Python"
resource: "https://github.com/hexuan21/MemoryTax/tree/179e6a79da415a4e1eabe9eb3110754955360d05"
generated:
  by: "process:blog-review"
  at: "2026-11-02T06:07:01+09:00"
sources:
  - id: "hexuan21/memorytax"
    resource: "https://github.com/hexuan21/MemoryTax/tree/179e6a79da415a4e1eabe9eb3110754955360d05"
    title: "Memory Tax: Dissecting the Net Value of Agent Memory"
status: "stable"
year: "2026"
analyzed_at: "2026-11-02T06:07:01+09:00"
source_id: "hexuan21/memorytax"
source_revision: "179e6a79da415a4e1eabe9eb3110754955360d05"
source_type: "repo"
source_url: "https://github.com/hexuan21/MemoryTax/tree/179e6a79da415a4e1eabe9eb3110754955360d05"
visual_sources:
  - path: "/img/reviews/2026/memorytax-repo-review/public-boundary.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/api/README.md#L1-L13"
    caption: "리뷰어 작성, 분석 커밋 기준: 공개 구현과 미공개 평가 연결의 경계"
    evidence:
      - "https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/bench/prepare.py#L173-L185"
      - "https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/judge/README.md#L11-L13"
  - path: "/img/reviews/2026/memorytax-repo-review/data-flow.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/bench/prepare.py#L173-L185"
    caption: "리뷰어 작성, 분석 커밋 기준: 고정 revision·표본 ID에서 raw와 processed까지의 데이터 준비 흐름"
    evidence:
      - "https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/bench/download.py#L25-L83"
      - "https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/bench/prepare.py#L54-L170"
  - path: "/img/reviews/2026/memorytax-repo-review/judge-boundary.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/judge/prompts.py#L129-L157"
    caption: "리뷰어 작성, 분석 커밋 기준: PersonaMem 파싱과 문서상 judge fallback의 호출자 경계"
    evidence:
      - "https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/qa_prompts/qa_persona_mem_v2.py#L124-L154"
      - "https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/judge/README.md#L3-L13"
---

## 들어가며: 기억을 더 가공하면 답도 더 좋아질까요

대화 이력을 요약하고 사실을 추출해 장기 기억에 저장하면, 다음 질문에 필요한 정보를 더 쉽게 찾을 수 있을 것 같습니다. 그러나 그 과정에서 날짜가 달라지거나, 맥락이 사라지거나, 실제 구매 내역이 일반적인 취향으로 바뀔 수도 있습니다. 기억 시스템의 가치를 보려면 평균 정답률뿐 아니라 **어떤 질문을 새로 맞혔고 어떤 질문을 새로 틀렸는지**도 비교해야 합니다.

MemoryTax는 이 문제를 다루는 연구 **Memory Tax: Dissecting the Net Value of Agent Memory**의 공개 저장소입니다. README의 인용 정보는 Xuan He 등의 논문 `arXiv:2610.34073`을 가리킵니다. 여기서 memory tax는 API 요금이라는 뜻이 아니라, 원시 이력에 대한 단순 검색 증강 생성(RAG)은 맞혔지만 기억 시스템은 틀린 질문에서 생기는 손실을 뜻합니다. 토큰 수와 호출 수는 이 손실과 별도로 보는 비용 축입니다. [논문 식별 정보](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/README.md#L94-L105), [프로젝트 설명의 정의](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/docs/index.html#L492-L515)

이 글은 커밋 `179e6a79da415a4e1eabe9eb3110754955360d05`를 기준으로 한 정적 코드 리뷰입니다. 대상 저장소의 설치·다운로드·실험·테스트·모델 호출은 실행하지 않았습니다. 분석 시점에는 **데이터 준비, QA 프롬프트 생성, 심사 프롬프트와 응답 파서가 공개되어 있고, 각 기억 시스템의 평가 harness와 공통 API 구현은 아직 공개되지 않았습니다.** Harness는 데이터 적재, 기억 생성, 검색, 모델 호출, 결과 저장을 연결하는 평가 실행 프로그램을 말합니다. 이 공개 범위를 먼저 알아야 README의 설계와 실제 구현을 구분할 수 있습니다. [공개 상태 TODO](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/README.md#L18-L22), [API 디렉터리](https://github.com/hexuan21/MemoryTax/tree/179e6a79da415a4e1eabe9eb3110754955360d05/common/api), [judge 실행기 TODO](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/judge/README.md#L11-L13)

## MemoryTax는 무엇인가

한 문장으로 정의하면, **여러 에이전트 기억 시스템을 동일한 데이터 부분집합과 응답·심사 규약으로 비교하기 위한 연구 자료와 공통 평가 구성 요소의 저장소**입니다. 자체적으로 하나의 새로운 메모리 엔진을 제공하는 구조는 아닙니다. README는 11개 비교 시스템을 단순 저장, 계층·수명주기 관리, 그래프 기반, 학습된 정책으로 분류합니다. 이 분류는 저자가 비교 대상을 정리한 방식이며, 아래 리뷰에서 11개 외부 시스템의 내부 알고리즘을 모두 분석했다는 뜻은 아닙니다. [비교 대상 표](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/README.md#L44-L58)

| README의 분류 | 비교 대상으로 열거한 시스템 |
|---|---|
| Flat store | A-Mem, SimpleMem, MemOS |
| Hier/Lifecycle | MemoryOS, LightMem, OpenViking |
| Graph-based | HippoRAG2, PlugMem, MAGMA |
| Trained policy | Mem-T, Memory-R2 |

프로젝트 페이지의 설명에서는 같은 질문에 대해 단순 RAG 1회 검색과 기억 시스템을 짝지어 비교합니다. 기억 시스템만 맞힌 질문이 memory benefit, RAG만 맞힌 질문이 memory tax이며, 두 차이가 순가치입니다. 따라서 평균 성능이 비슷해도 성공·실패한 질문의 구성이 달라질 수 있습니다. **이 글에서 읽는 파서와 표본 규약은 바로 그 질문별 비교의 기반**입니다. 다만 benefit·tax를 실제 집계하는 프로그램은 이 커밋에서 확인할 수 없습니다. [정의와 비교 기준](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/docs/index.html#L492-L515)

## 아키텍처: 공개된 함수와 아직 연결되지 않은 실행 경계

README의 폴더 트리는 완성될 평가 구조를 설명합니다. 실제 파일을 대조하면 다음처럼 공개 수준이 나뉩니다.

| 위치 | 이 커밋에서 확인한 내용 | 확인할 수 없는 연결 |
|---|---|---|
| `common/bench/` | 다운로드·전처리 진입점과 세 벤치마크의 표본 ID JSON | 원본을 내려받아 생성한 결과의 실제 내용 |
| `common/qa_prompts/` | 세 데이터셋의 `build_messages`, PersonaMem 선택지 섞기·파싱 | 검색기와 모델 호출에 이 함수를 연결하는 harness |
| `common/judge/` | 프롬프트 선택·메시지 생성·판정 파서 | 결과 디렉터리를 순회하는 judge runner |
| `common/api/` | 채팅·임베딩·재순위화 API와 계측에 관한 README | 클라이언트 구현, 재시도·캐시·사용량 집계 |
| `reproduction/<baseline>/` | 외부 저장소·커밋·라이선스 안내, Git checkout용 `setup.sh` | 평가 harness, 검색 top-k와 실험 설정 |
| `docs/` | 논문 PDF, 프로젝트 페이지, 정적 그림·표시용 JavaScript 데이터 | 실험을 다시 수행하는 코드 |

근거는 [README의 의도한 구조](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/README.md#L24-L42), [실제 common 트리](https://github.com/hexuan21/MemoryTax/tree/179e6a79da415a4e1eabe9eb3110754955360d05/common), [reproduction 트리](https://github.com/hexuan21/MemoryTax/tree/179e6a79da415a4e1eabe9eb3110754955360d05/reproduction)입니다. `harness/`는 `.gitkeep`만 가진 상태이며, 일부 `patches/`도 같은 상태입니다. `_naive_rag/`와 `_exp_mem/`에는 설명과 TODO만 있습니다. [단순 RAG 설명](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/reproduction/_naive_rag/README_naive_rag.md#L1-L5), [경험 기억 설명](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/reproduction/_exp_mem/README_exp_mem.md#L1-L5)

![MemoryTax의 공개 데이터 준비·QA·judge 함수와 미공개 harness·API·집계 경계를 나누어 표시한 도식]({{ '/img/reviews/2026/memorytax-repo-review/public-boundary.svg' | relative_url }})

*그림 1. 리뷰어 작성, 분석 커밋 기준. 파란 영역은 공개 구현, 점선 영역은 문서에만 설명된 실행 연결입니다. 위아래 배치는 구성 요소의 구분이며 완성된 호출 체인을 뜻하지 않습니다. [데이터 준비](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/bench/prepare.py#L173-L185), [API 계약](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/api/README.md#L1-L13), [심사 실행기 경계](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/judge/README.md#L11-L13)를 바탕으로 구성했습니다.*

루트에는 `pyproject.toml`, `setup.py`, `requirements.txt` 같은 패키지 매니페스트가 없습니다. 데이터 준비 문서는 `huggingface_hub`와 `pyarrow`를 요구한다고 설명하며, 다운로드 코드와 MINT 전처리 코드에 해당 import가 있습니다. 따라서 재현 환경의 패키지 버전까지 고정된 상태라고 볼 수 없습니다. [요구 의존성](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/bench/bench_readme.md#L5-L12), [Hub import](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/bench/download.py#L12-L20), [PyArrow import](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/bench/prepare.py#L150-L152)

## 작동 원리 1: 원본 revision과 표본 ID를 고정합니다

### 다운로드: 외부 데이터에서 raw 디렉터리까지

실제 첫 진입점은 `common/bench/download.py`의 `main()`입니다. `--root`의 기본값은 저장소 아래 `bench_data`이며, `SOURCES`에 데이터셋별 Hub 저장소·전체 revision·원격 파일명과 로컬 파일명 대응표가 들어 있습니다. 반복문은 이를 `bench_data/raw/<benchmark>/`로 옮깁니다. 데이터 버전은 짧은 이름만 적은 것이 아니라 코드에 전체 revision으로 고정되어 있습니다. [소스 매핑](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/bench/download.py#L25-L43), [main의 경로 구성](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/bench/download.py#L69-L83)

| 데이터셋 | 코드에 고정된 Hub revision | 가져오는 범위 |
|---|---|---|
| `xiaowu0162/longmemeval` | `2ec2a557f339b6c0369619b1ed5793734cc87533` | `longmemeval_s` 파일 |
| `bowen-upenn/PersonaMem-v2` | `ed956dea41521fc4499acbc63f966e0fd3c053ba` | benchmark CSV와 선택한 40개 대화 이력 |
| `dinobby/MINTEval` | `9b9c5befc5126a4ca0fd88cc03c03260142a0883` | 네 하위 영역의 Parquet 파일 |

이 표는 위 `SOURCES` 정의를 옮긴 것입니다. PersonaMem의 이력 파일은 정적 목록을 중복 작성하지 않고, 표본 JSON의 `chat_history_128k_link`를 읽어 다운로드 매핑에 추가합니다. 같은 표본 명세가 **무엇을 받을지와 무엇을 평가용으로 남길지**를 함께 결정하는 구조입니다. 다만 MINT는 표본 60개 corpus만 직접 내려받는 방식이 아니라 네 원본 Parquet를 받은 후 선택합니다. [PersonaMem 파일 목록 생성과 적용](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/bench/download.py#L46-L48), [원격 파일 매핑과 순회](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/bench/download.py#L36-L41)

`fetch()`는 목적 파일이 이미 있으면 바로 건너뜁니다. 새 파일은 Hub 캐시에서 받은 경로를 `dst + ".tmp"`로 복사하고 `os.replace`로 최종 파일명에 반영합니다. 기본 다섯 번의 시도에서 실패하면 20·40·80·160초를 기다리고 마지막 실패는 다시 예외로 올립니다. 이 값은 루프와 대기식에서 읽은 것이며 네트워크 실험 결과는 아닙니다. [다운로드와 재시도 구현](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/bench/download.py#L51-L66)

이 처리에는 두 가지 서로 다른 의미가 있습니다. 임시 파일을 거쳐 교체하므로 이 함수가 복사하다 멈춘 파일을 최종 이름으로 남기는 상황을 줄입니다. 반면 **이미 있는 최종 파일의 revision·크기·해시를 확인하지는 않습니다.** 다른 버전의 파일이 같은 경로에 있어도 존재 여부만으로 건너뜁니다. 또한 파일별 재개는 가능하지만 평가 작업의 진행 상태를 복구하는 기능은 아닙니다. 재시도는 여기서는 데이터 다운로드에 한정되며, 모델 API도 같은 정책을 쓴다고 추정할 수 없습니다.

### 표본 명세: 다시 추출하지 않고 ID를 적용합니다

`prepare.py`는 표본을 새로 무작위 추출하지 않습니다. 이미 저장된 ID를 읽어 원본에서 선택합니다. 다음 수치는 성능 결과가 아니라 **평가 입력의 범위**입니다.

| 벤치마크 | 공개 명세의 표본 | 정적 자료 대조로 확인한 범위 |
|---|---|---|
| LongMemEval-s | 전체 500문항 또는 GPT-5.6-luna용 100문항 | 표본 JSON에 서로 다른 질문 ID 100개, 유형별 합계 100개 |
| PersonaMem-v2 128k | 40명, 934문항 | 서로 다른 이력 경로 40개, `n_questions` 합계 934 |
| MINT-Eval | 60개 corpus, 1,557문항 | 영역별 ID 개수 합계 60개, 메타데이터의 문항 수 합계 1,557 |

출처는 [평가 범위 설명](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/bench/bench_readme.md#L34-L44), [LongMemEval 표본](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/bench/subset_ids/longmemeval_s_sub100.json#L1-L15), [PersonaMem 표본](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/bench/subset_ids/persona_mem_v2_128k_40.json#L1-L12), [MINT 표본](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/bench/subset_ids/mint_eval.json#L1-L109)입니다. 원본 CSV·Parquet는 받지 않았으므로 실제 행 수나 질문 내용까지 대조한 것은 아닙니다. 특히 MINT의 1,557은 저장된 영역별 문항 수 690+563+154+150의 합이며, 원본 질문 배열을 다시 세어 얻은 값은 아닙니다.

LongMemEval 명세는 질문 유형별 할당, ID 정렬, `random.Random(42).sample`로 선정했다고 설명합니다. PersonaMem 명세는 이력 링크를 문자열로 정렬한 첫 40개를 선택했다고 적습니다. MINT 명세는 corpus 크기로 정렬한 체계적 표집, 질문 유형 분포의 L1 차이가 작은 시작점 선택, 크기 이상치 두 개 교환을 설명합니다. **선정 방법에 대한 기록과 선정 결과를 적용하는 코드는 구분해야 합니다.** 현재 `prepare.py`에는 그 표본 선정 알고리즘 자체가 없고 확정된 ID 목록을 읽는 부분이 있습니다. [LongMemEval 선정 기록](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/bench/subset_ids/longmemeval_s_sub100.json#L1-L6), [PersonaMem 선정 기록](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/bench/subset_ids/persona_mem_v2_128k_40.json#L1-L6), [MINT 선정 기록](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/bench/subset_ids/mint_eval.json#L1-L6)

## 작동 원리 2: 전처리는 정보의 순서를 어떻게 보존하나요

![고정된 데이터 revision과 표본 ID가 다운로드 raw 파일, 데이터별 전처리, processed 출력으로 이어지는 흐름]({{ '/img/reviews/2026/memorytax-repo-review/data-flow.svg' | relative_url }})

*그림 2. 리뷰어 작성, 분석 커밋 기준. 이 그림의 화살표는 공개된 데이터 준비 코드의 흐름입니다. MINT 대화 분할은 새 메모리 알고리즘이 아니라 평가 입력의 표현 변환입니다. [다운로드 진입점](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/bench/download.py#L69-L83), [벤치마크별 전처리 호출](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/bench/prepare.py#L173-L185)을 바탕으로 구성했습니다.*

### LongMemEval: 선택 순서보다 공식 질문 순서를 우선합니다

`prepare_longmemeval()`은 원본을 전체 평가용 JSON으로 복사한 뒤, 표본 JSON의 질문 ID를 집합으로 만듭니다. 이어서 원본 질문 배열을 순회하며 집합에 속한 것만 남깁니다. 따라서 표본 JSON에 나열된 순서가 아니라 **공식 파일의 질문 순서**가 출력에 남습니다. 선택된 개수가 ID 집합의 크기와 같은지 `assert`로 검사한 후 `_write_json()`으로 기록합니다. [LongMemEval 처리](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/bench/prepare.py#L54-L65)

`_write_json()`도 `.tmp`에 쓴 뒤 교체하지만, 원본 전체 복사와 다른 데이터셋 출력까지 하나의 트랜잭션으로 묶지는 않습니다. 또한 로그의 `500`은 고정 문자열이고 실제 원본 전체 길이를 검증하는 식은 없습니다. 이 코드가 검증하는 것은 표본 ID를 적용했을 때의 개수 조건입니다. [JSON 기록](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/bench/prepare.py#L43-L51), [개수 검사와 출력](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/bench/prepare.py#L59-L65)

### PersonaMem: 한 사람의 질문과 이력을 같이 유지합니다

`prepare_persona()`는 CSV의 `chat_history_128k_link` 열 위치를 헤더에서 찾습니다. 그 값이 선택한 링크 집합에 들어 있는 행을 원래 순서대로 모으고, 선택한 persona별 `n_questions` 합과 행 수를 비교합니다. 이후 헤더와 행을 새 CSV에 기록하고 40개 이력 파일을 복사합니다. 질문 하나씩 균등 추출하는 것이 아니라 **선택한 사람에게 속한 질문 전체와 대화 이력을 묶어서 유지**하는 단위입니다. [PersonaMem 처리](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/bench/prepare.py#L68-L94)

대화 JSON의 내부 내용을 요약하거나 persona system message를 제거하는 로직은 이 전처리 함수에 없습니다. QA 모듈의 설명도 공식 프로토콜에 포함된 첫 system message를 유지한다고 명시합니다. 다만 그것을 모델 입력에 어떻게 연결하는지는 미공개 harness의 영역입니다. 같은 주석은 CSV의 `user_query`가 Python dict 리터럴이므로 `ast.literal_eval`로 읽어야 한다고 안내하지만, 이 파일 자체가 그 셀을 해석해 평가 루프를 실행하지는 않습니다. [데이터 해석 주의사항](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/qa_prompts/qa_persona_mem_v2.py#L22-L30)

### MINT: corpus를 보존하고 대화 block을 turn으로 풉니다

`prepare_mint()`는 각 Parquet의 `id`를 문자열 목록으로 만들고, 명세의 ID가 빠지지 않았는지 확인합니다. 이어 `ids.index(i)`로 행 위치를 찾아 `table.take()`로 명세 순서대로 선택합니다. 나머지 세 영역은 선택한 행의 내용을 그대로 내보내고, `multi_turn_dialogue`만 `contexts`를 대화 turn 단위로 바꿉니다. 행 하나가 corpus와 그 질문들을 함께 담으므로, 질문 일부만 잘라 과거 단계 참조가 끊기는 일을 피하려는 구조입니다. [MINT 선택과 출력](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/bench/prepare.py#L150-L170), [문서의 corpus 보존 이유](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/bench/bench_readme.md#L42-L44)

분할의 시작 조건은 엄격합니다. `ROLE_LINE`은 행 맨 앞의 소문자 `user:` 또는 `assistant:`를 새 turn으로 인식합니다. 그 외 빈 줄·설명·제목은 현재 turn의 내용에 붙입니다. 아직 role이 없는 상태의 비어 있지 않은 행은 `scenario` 항목이 됩니다. 따라서 이를 어떤 형식의 대화도 자동 인식하는 범용 파서라고 해석하면 안 됩니다. [정규식과 block 분할](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/bench/prepare.py#L97-L126)

`dialogue_to_turns()`는 각 항목에 `content`, `role`, 원래 block의 `timestamp`, `block_idx`, `turn_idx`를 붙입니다. `scenario`의 `turn_idx`는 -1이고 실제 대화 turn만 0부터 증가합니다. **이 `turn_idx`가 곧 QA의 전역 `[step i]`라는 뜻은 아닙니다.** 전자는 block 안의 위치이고, 후자는 QA 입력의 이력 순서를 보존하도록 baseline에 요구하는 레이블입니다. 이를 실제 검색 결과 문자열로 렌더링하는 함수는 이 저장소에 공개되어 있지 않습니다. [turn 필드 생성](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/bench/prepare.py#L129-L147), [QA의 step 보존 계약](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/qa_prompts/qa_mint_eval.py#L1-L20)

## 작동 원리 3: 검색 결과를 답변 메시지로 바꿉니다

### 공통 경계: 검색은 호출자가, 메시지 구성은 QA 모듈이 맡습니다

세 QA 모듈 모두 이미 렌더링된 `memory_block`을 입력받아 system·user 메시지 두 개를 반환합니다. 임베딩 검색, top-k 선택, 재순위화, 기억 저장은 이 함수들이 수행하지 않습니다. 검색된 기억이 비면 `(no relevant memory retrieved)`를 넣고, 비어 있지 않은 `profile_block`만 별도 구역으로 붙입니다. 문자열 치환에는 중괄호나 JSON이 들어 있는 기억 내용과 템플릿 문법이 충돌하지 않도록 `string.Template`를 사용합니다. 이는 입력 텍스트를 채우는 방식이지, 기억의 사실성이나 지시문 안전성을 검증하는 장치는 아닙니다. [LongMemEval 템플릿과 builder](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/qa_prompts/qa_longmemeval.py#L63-L126), [PersonaMem builder](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/qa_prompts/qa_persona_mem_v2.py#L98-L121), [MINT builder](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/qa_prompts/qa_mint_eval.py#L73-L95)

| QA 모듈 | 답변 규약에서 중요한 차이 | 공개된 생성 상수 |
|---|---|---|
| LongMemEval | 현재 날짜로 상대 시간을 해석하고, 최신 기억 우선·여러 대화의 근거 결합을 지시 | temperature 0, 최대 512토큰 |
| PersonaMem-v2 | 후보 A–D 중 한 글자만 출력하도록 지시 | temperature 0, 최대 32토큰 |
| MINT-Eval | 검색 결과의 나열 순서 대신 `[step i]`로 과거 단계와 순서를 판단하도록 지시 | temperature 0, 최대 256토큰 |

상수는 [LongMemEval](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/qa_prompts/qa_longmemeval.py#L129-L131), [PersonaMem](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/qa_prompts/qa_persona_mem_v2.py#L157-L159), [MINT](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/qa_prompts/qa_mint_eval.py#L98-L100)에서 확인했습니다. `build_messages()`가 상수를 API 요청에 자동 적용하는 것은 아닙니다. 실제 호출자가 이 값을 사용해야 하며, 현재 공개 코드만으로 모든 실험이 이 설정을 따랐다고 검증할 수는 없습니다.

### LongMemEval: 선호 질문은 같은 프롬프트가 아닙니다

LongMemEval의 일반 system prompt에는 기억이 없으면 정보가 없다고 답하라는 다섯 번째 규칙이 있습니다. `single-session-preference` 및 underscore 표기를 선호 유형으로 판별하면 `SYSTEM_PROMPT.split("\n5. ")[0]`로 그 규칙을 제외합니다. 마지막 지시도 짧은 답만 요구하는 문장 대신 사용자 선호를 충분히 고려하도록 바뀝니다. 즉 전체 baseline에 공통 프롬프트를 쓴다는 말은 **벤치마크와 질문 유형까지 무시하고 모두 같은 문자열을 넣는다는 뜻이 아닙니다.** [유형과 system 규칙](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/qa_prompts/qa_longmemeval.py#L30-L61), [마지막 지시와 분기](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/qa_prompts/qa_longmemeval.py#L84-L125)

### PersonaMem: 선택지의 난수와 파싱도 평가 조건입니다

`shuffle_options()`는 오답 세 개 뒤에 정답을 붙인 다음, 외부에서 전달받은 `rng`로 섞고 정답의 최종 문자를 돌려줍니다. 주석은 질문별 seed를 요구하지만 함수가 seed를 정하거나 질문 ID에서 생성하지는 않습니다. 따라서 공개 함수만으로 실험의 실제 선택지 순서를 복원할 수는 없습니다. 동일한 데이터 ID를 고정하는 것과 동일한 선택지 배치를 재현하는 것은 별개 조건입니다. [선택지 섞기](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/qa_prompts/qa_persona_mem_v2.py#L82-L95)

`parse_answer()`는 다음 순서로 답변을 읽습니다.

1. 앞뒤가 영숫자가 아닌 첫 A–D 문자를 찾습니다. 대소문자는 구분하지 않습니다.
2. 찾지 못했고 선택지 텍스트가 주어지면, 전체 응답과 한 선택지의 텍스트가 같은지 대소문자 없이 비교합니다.
3. 그래도 없으면 응답에 포함된 선택지 텍스트가 정확히 하나일 때 해당 문자를 반환합니다. 식별하지 못하면 빈 문자열을 반환합니다.

여기서 “한 글자만 답하라”는 프롬프트와 실제 허용하는 출력 범위는 다릅니다. 첫 단계는 여러 문자를 모두 수집해 모호성을 검사하지 않고 **처음 발견한 독립 문자에서 반환**합니다. 따라서 설명 안에 여러 후보가 언급된 경우에도 첫 후보로 파싱될 수 있다는 점은 코드로 읽을 수 있습니다. 이 경로가 실제 실험에서 얼마나 발생했는지는 측정하지 않았습니다. [정답 파서 전체](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/qa_prompts/qa_persona_mem_v2.py#L124-L154)

다음은 그 조기 반환 부분의 연속 원문입니다.

```python
    for i, ch in enumerate(text.upper()):
        if ch in LETTERS:
            prev_ok = i == 0 or not text[i - 1].isalnum()
            nxt_ok = i + 1 >= len(text) or not text[i + 1].isalnum()
            if prev_ok and nxt_ok:
                return ch
```

출처: [`parse_answer`, 136–141행](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/qa_prompts/qa_persona_mem_v2.py#L136-L141). 판단 기준은 “모델이 지시한 형식대로 답했는가”와 “평가기가 어떤 문자를 추출했는가”를 나누어 읽는 것입니다.

### MINT: 순서가 바뀐 검색 결과에도 원래 단계가 남아야 합니다

MINT system prompt는 `[step i]`를 원래 이력의 위치로 정의하고, 몇 단계 전인지 묻는 질문을 검색 결과의 나열 순서로 계산하지 말라고 지시합니다. 최근 단계가 이전 상태를 갱신한다는 규칙도 있지만, 질문이 과거를 묻는 경우에는 해당 시점을 보도록 예외를 둡니다. 이 규칙이 작동하려면 호출자가 검색된 단위에 원래 step을 보존해야 합니다. 프롬프트 함수가 누락된 레이블을 복원하지는 않습니다. [MINT system prompt](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/qa_prompts/qa_mint_eval.py#L30-L50)

또한 공개 함수의 `question_type` 인자는 전달되지만 현재 `build_user_prompt()` 내부의 분기에 쓰이지 않습니다. 유형별 생성 전략이 구현되어 있다고 읽을 근거는 없습니다. `profile_block`은 여기서는 `<SUMMARY>` 구역으로 들어가며, 다른 두 벤치마크의 `<USER PROFILE>`과 이름이 다릅니다. [MINT 템플릿과 함수](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/qa_prompts/qa_mint_eval.py#L52-L95)

## 작동 원리 4: 모델 답변을 판정 입력과 숫자로 바꿉니다

### 프롬프트 선택과 judge 호출 준비

심사 모듈은 LLM-as-Judge, 즉 별도 언어 모델이 답의 의미를 평가하는 방식을 위한 메시지를 만듭니다. 문서는 심사 모델을 Qwen3.6-27B, temperature 0, reasoning 비활성화, 질문당 user 메시지 하나로 고정한다고 설명합니다. 코드에는 `JUDGE_TEMPERATURE = 0.0`, 프롬프트 버전 `judge/unified-v1`, 종류별 출력 토큰 상수가 있지만, reasoning 옵션을 실제 요청에 넣는 API 코드는 없습니다. 따라서 **고정 심사 정책의 선언과 API 수준 적용 여부를 구분**해야 합니다. [심사 정책](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/judge/README.md#L1-L13), [프롬프트 상수](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/judge/prompts.py#L87-L107)

`pick_prompt()`의 분기는 세 가지입니다. PersonaMem 이름으로 시작하면 `PERSONA_MCQ_UNPARSED`, LongMemEval의 선호 유형이면 `PREF`, 나머지는 `GENERAL`입니다. `GENERAL`은 질문·정답·모델 응답의 의미가 맞는지 보고, `PREF`는 정답 문장 일치보다 사용자 정보와 rubric 충족을 보도록 합니다. 모듈 주석은 두 프롬프트를 LightMem에서 전사했다고 밝힙니다. [일반·선호 심사 기준](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/judge/prompts.py#L29-L58), [선택 함수](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/judge/prompts.py#L97-L107)

`build_messages()`는 여러 정답이 있으면 글머리표로 묶고, 빈 모델 답변을 `(empty)`로 바꾸며, user 메시지 하나를 반환합니다. PersonaMem이 이 함수로 들어오면 `ValueError`를 발생시켜 전용 builder를 쓰게 합니다. `build_persona_messages()`에는 **실제로 섞어서 모델에 보여 준 순서의 선택지와 정답 문자·정답 텍스트**를 전달해야 합니다. 이렇게 해야 후보 텍스트를 인용하거나 바꾸어 말한 응답도 판단할 수 있습니다. [정답 가공과 메시지 생성](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/judge/prompts.py#L110-L140)

PersonaMem은 문서상 먼저 파싱한 문자와 정답 문자를 비교하고, 파싱 결과가 빈 문자열인 경우에만 judge를 사용합니다. 그러나 `pick_prompt()`가 그 빈 문자열 조건을 검사하거나 exact match를 실행하지는 않습니다. 그것은 호출자가 먼저 분기해야 하는 계약입니다. 특히 앞 단계에서 여러 후보가 등장한 응답을 첫 문자로 이미 파싱했다면, 문서의 “파싱 불가일 때만 judge” 정책에서는 judge의 모호성 판정에 도달하지 않을 수 있습니다. [PersonaMem 심사 계약](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/judge/prompts.py#L13-L18), [모호한 응답에 대한 judge 지시](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/judge/prompts.py#L60-L84)

![PersonaMem의 응답 파싱과 문서상 exact match·judge fallback 정책을 구분한 평가 경계 도식]({{ '/img/reviews/2026/memorytax-repo-review/judge-boundary.svg' | relative_url }})

*그림 3. 리뷰어 작성, 분석 커밋 기준. 파란 상자는 공개 함수이며 점선 상자는 호출자가 구현해야 할 실행·집계 경계입니다. 빈 문자열 조건에 따른 실제 분기 실행기는 미공개입니다. [응답 파서](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/qa_prompts/qa_persona_mem_v2.py#L124-L154), [judge builder와 판정 파서](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/judge/prompts.py#L129-L157)를 바탕으로 구성했습니다.*

### 판정 파서: JSON만 읽는 엄격한 검증기는 아닙니다

`parse_verdict()`의 반환값은 정답 1, 오답 0, 파싱 불가 `None`입니다. 먼저 `"label"` 뒤의 `CORRECT` 또는 `WRONG`을 대소문자 없이 정규식으로 찾습니다. JSON 전체를 역직렬화해 스키마를 검사하는 구조가 아니므로, 앞뒤 설명이 있는 텍스트 안에서도 레이블을 찾을 수 있습니다. [판정 파서](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/judge/prompts.py#L143-L157)

레이블 패턴이 없으면 전체 문자열에 해당 단어가 포함되는지 확인합니다. `INCORRECT` 안에도 `CORRECT`가 들어 있다는 점을 별도로 처리하고, `CORRECT`와 `WRONG`이 함께 나오면 마지막 위치와 `INCORRECT`의 존재로 결론을 냅니다. 어느 쪽도 없으면 `None`입니다. 이 설계는 형식을 어긴 judge 응답을 일부 받아들이지만, 자연어 전체의 결론을 이해하는 파서는 아닙니다. 따라서 `None`을 별도로 세어야 한다는 함수 설명과, 이를 최종 점수의 분모에 어떻게 반영할지는 다른 문제입니다. 후자의 집계 구현은 공개되지 않았습니다.

### 출력과 연구 결과: 공개 위치와 재현 가능 범위

공개 데이터 준비 프로그램의 출력은 `processed` 아래의 JSON·CSV·Parquet입니다. QA builder의 출력은 메시지 목록이고, 두 파서의 출력은 선택지 문자 또는 1·0·`None`입니다. 이 값들을 질문 ID와 함께 저장하고, 기억 시스템과 RAG를 짝지어 benefit·tax 및 비용 표를 만드는 실행기는 없습니다. 따라서 코드에서 마지막으로 추적할 수 있는 결과를 논문의 최종 집계 파일과 동일시하면 안 됩니다.

README는 QA 응답, judge 판정, 비용, 기억 저장소 등의 실험 결과가 Hugging Face의 별도 결과 저장소에 공개되어 있다고 안내합니다. 이 리뷰에서는 그 외부 파일 전체를 내려받거나 최종 지표를 재계산하지 않았습니다. 프로젝트 페이지는 11개 시스템·3개 벤치마크·3개 backbone의 99개 조합 중 90개 기억 시스템 결과가 naive RAG보다 낮다고 **저자가 보고**합니다. 이것은 페이지에 적힌 연구 결과이며, 이 글의 정적 분석이 성능을 재현한 결과가 아닙니다. 페이지의 leaderboard는 RAG 2회 검색을 색상 비교 기준으로 적고, benefit·tax 정의는 RAG 1회 검색과 비교합니다. 따라서 서로 다른 비교 기준의 수치를 같은 기준처럼 합쳐 읽지 않아야 합니다. [결과 자료 안내](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/README.md#L81-L92), [저자 보고의 범위와 수치](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/docs/index.html#L450-L472), [leaderboard 비교 기준](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/docs/index.html#L486-L500)

## 설치와 사용: 같은 커밋의 문서가 안내하는 단계

README Quickstart의 실행 명령 부분은 다음과 같습니다. 대상 명령은 실행하지 않았습니다.

```bash
python common/bench/download.py   # official benchmark files -> bench_data/raw/
python common/bench/prepare.py    # evaluated subsets -> bench_data/processed/
cp .env.example .env              # fill in API base URLs, keys and model names
cd reproduction/<baseline>
bash setup.sh                     # clone the official repo at the pinned commit
```

출처: [README Quickstart, 73–77행](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/README.md#L73-L77). 바로 다음 줄은 `# TODO: harness commands, see README_<baseline>.md`라고 적혀 있습니다. `<baseline>`은 문서의 자리표시자이며 실제 디렉터리명으로 바꾸어야 합니다. 이 명령 모음만으로 최종 평가가 실행된다는 뜻은 아닙니다.

`.env.example`은 답변·기억 생성 LLM, 임베딩, reranker, judge의 base URL·key·model을 별도로 둡니다. 예시 모델은 각각 Qwen3.6-27B, Qwen3-Embedding-0.6B, Qwen3-Reranker-0.6B, Qwen3.6-27B입니다. 공통 API README는 chat과 embedding을 OpenAI 호환 형식으로, `/rerank`는 다른 형식으로 설명합니다. 하지만 `.env`를 로딩하고 요청을 보내는 구현은 없으므로, 이 설정 파일을 작성하는 것만으로 작동하는 클라이언트가 생기지는 않습니다. [설정 템플릿](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/.env.example#L1-L19), [API별 계약](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/api/README.md#L3-L13)

11개 baseline의 `setup.sh`는 공식 저장소 URL과 전체 커밋을 지정하고, `upstream/`이 없으면 clone한 뒤 fetch·checkout합니다. 일부는 `patches/*.patch`를 적용하는 반복문이 있으나 이 커밋의 해당 디렉터리에는 실제 patch 파일이 없습니다. 또한 환경·의존성 설치는 각 스크립트에 TODO로 남아 있습니다. 예를 들어 A-Mem은 수정 없이 upstream을 쓰도록 적혀 있고, LightMem은 patch 반복문을 둡니다. [A-Mem setup](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/reproduction/amem/setup.sh#L1-L17), [LightMem setup](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/reproduction/lightmem/setup.sh#L1-L20)

따라서 이 시점의 사용 문서는 데이터 준비와 외부 소스 버전 지정까지 읽을 수 있고, 실제 실험 재현에는 추가 공개가 필요합니다. 검색 top-k 같은 설정도 baseline README에 TODO입니다. 고정 커밋 checkout이 있다는 사실만으로 평가 프로토콜과 결과까지 재현 가능하다고 결론낼 수 없습니다. [A-Mem의 실행·설정 TODO](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/reproduction/amem/README_amem.md#L15-L21)

## 한계와 주의점: 측정 범위가 구현되어 있는지 확인해야 합니다

### 비용 계측은 현재 문서 계약입니다

API README는 채팅을 기억 적재와 QA로 나누고 기억 연산별 토큰·호출 수를 기록한다고 설명합니다. 그러나 실제 클라이언트가 없으므로 다음 항목은 이 커밋으로 확인할 수 없습니다. 실패한 요청과 재시도의 집계 방식, 입력·출력·추론 토큰의 구분, 임베딩·reranker·judge 비용의 포함 여부, 캐시 적중과 병렬 호출의 중복 계측 방지, 토큰을 실제 요금으로 바꾸는 가격표 적용입니다. **문서에 token/call accounting이 적혀 있다는 사실과 비용이 빠짐없이 측정된다는 사실은 다릅니다.** [계측 범위에 관한 문서](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/api/README.md#L5-L13)

동일한 이유로 thread-safe 캐시, API rate limit 대응, 요청 실패 후 평가 재개, 결과 저장의 충돌 방지 여부도 분석할 공개 구현이 없습니다. 앞에서 본 `fetch()`의 백오프나 임시 파일 교체를 모델 호출 계층의 안정성 근거로 옮겨 쓰면 안 됩니다. 이 항목들은 확인된 결함 목록이 아니라 **미공개 코드 때문에 판단할 수 없는 범위**입니다.

### 데이터 전처리의 실패는 전체 작업 단위로 되돌려지지 않습니다

`prepare.py`의 `main()`은 LongMemEval, PersonaMem, MINT 순서로 호출합니다. 앞 단계 출력 후 뒷 단계에서 오류가 나면 이미 쓴 결과를 되돌리는 로직이 없습니다. JSON 표본은 임시 파일을 쓰지만 PersonaMem CSV·이력 복사와 MINT Parquet 출력까지 같은 보호를 쓰지 않습니다. `assert`로 누락이나 행 수를 확인하는 조건도 있으나, 전체 출력 manifest와 체크섬으로 완료를 선언하는 경로는 없습니다. 이것은 실행 실패를 관측했다는 뜻이 아니라, 소스에서 읽히는 실패 경계입니다. [출력 방식과 순차 호출](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/bench/prepare.py#L75-L94), [MINT 기록과 main](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/bench/prepare.py#L150-L185)

### 비교의 공정성과 재현성은 여러 층으로 나뉩니다

확정된 ID와 원본 revision은 입력 범위를 고정합니다. 통일된 QA 프롬프트와 judge 프롬프트는 답변·심사 규약을 맞추는 구성 요소입니다. 그러나 검색 결과 렌더링, 질문별 선택지 seed, 모델 요청 옵션, 파싱 불가 결과의 집계, 비용 측정이 연결되어야 실제 비교 프로토콜이 됩니다. 이 저장소의 현재 학습 가치는 그 층을 나누어 확인할 수 있다는 데 있습니다. 공개된 함수에서 규약을 읽을 수 있고, 공개되지 않은 실행 경로는 보류해야 합니다.

### 라이선스 표기도 구성 요소마다 다릅니다

루트 `LICENSE`는 MemoryTax Authors 명의의 MIT License입니다. 데이터 준비 README는 LongMemEval을 MIT, PersonaMem-v2와 MINT-Eval을 CC-BY-4.0으로 표기합니다. 외부 baseline README도 upstream별 라이선스를 따로 적으며, 예를 들어 OpenViking은 AGPL-3.0이라고 안내합니다. 여기서는 저장소에 적힌 표기를 확인한 것이며, 외부 데이터와 모든 upstream 라이선스 원문을 독립적으로 조사한 것은 아닙니다. 루트 라이선스 하나로 외부 자료 전체의 조건을 대표해서는 안 됩니다. [루트 라이선스](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/LICENSE#L1-L21), [데이터 출처·라이선스 표](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/common/bench/bench_readme.md#L26-L32), [OpenViking의 upstream 표기](https://github.com/hexuan21/MemoryTax/blob/179e6a79da415a4e1eabe9eb3110754955360d05/reproduction/openviking/README_openviking.md#L3-L7)

## 결론

MemoryTax의 공개 코드는 기억 시스템을 비교할 때 데이터 ID와 순서, 검색 결과의 시간 레이블, 질문 유형별 지시, 선택지 파싱, judge 응답 해석을 얼마나 구체적으로 맞춰야 하는지 보여 줍니다. 평균 정답률 이전에 입력과 판정이 어떻게 만들어지는지를 읽는 데 유용합니다.

분석한 커밋에서 끝까지 연결되는 실행 흐름은 데이터 다운로드와 전처리입니다. QA·judge 함수는 메시지와 판정의 계약을 공개하지만, 검색·모델 호출·비용 계측·최종 집계는 아직 공개된 실행 체인으로 확인할 수 없습니다. 이 구분을 유지해야 memory benefit과 memory tax라는 연구 관점을 코드에서 확인한 사실과 함께 정확하게 이해할 수 있습니다.

## 이 글에서 다루지 못한 부분

11개 upstream 저장소의 내부 메모리 알고리즘, 외부 결과 데이터의 질문별 재집계, 논문 PDF 전체의 실험·절제 연구, 프로젝트 페이지 JavaScript의 전체 렌더링 로직은 분석 범위에서 제외했습니다. 특히 harness·API 클라이언트·judge runner는 현재 커밋에 구현이 공개되지 않아 분석하지 못했습니다. 공개 표본 JSON의 개수 대조는 수행했지만 원본 데이터 준비와 모델 실험을 실행한 검증은 아닙니다.
