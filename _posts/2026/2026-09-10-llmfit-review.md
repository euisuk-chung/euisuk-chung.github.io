---
title: "llmfit 코드 리뷰: 내 하드웨어에 맞는 로컬 LLM을 어떻게 추천할까"
summary: "하드웨어 감지부터 양자화 선택, 메모리 적합도와 속도 추정, 실측 보정까지 llmfit의 추천 경로를 코드로 분석합니다."
date: "2026-09-10T09:00:00+09:00"
year: "2026"
tags: [LLM, Rust, LocalInference, Quantization, OpenSource]
source_type: repo
source_id: "AlexsJones/llmfit"
source_revision: "e5508a1bdd9184d59add7dc0382219e82f68483d"
source_url: "https://github.com/AlexsJones/llmfit/tree/e5508a1bdd9184d59add7dc0382219e82f68483d"
analyzed_at: "2026-09-10T23:45:11+09:00"
---

## 들어가며

로컬에서 Large Language Model(LLM)을 실행할 때 모델의 파라미터 수만으로는 적합성을 판단하기 어렵습니다. 같은 모델도 양자화 방식, GPU 메모리, 실행 runtime, context 길이에 따라 필요한 메모리와 생성 속도가 달라집니다. 모델을 내려받은 뒤에야 이러한 차이를 발견하면 상당한 시간과 저장 공간을 소비하게 됩니다.

`llmfit`은 CPU·RAM·GPU 정보를 모델 카탈로그와 결합해 실행 가능한 후보를 추천하는 Rust 도구입니다. 이 글은 커밋 `e5508a1bdd9184d59add7dc0382219e82f68483d`를 기준으로 추천 명령의 입력부터 결과 출력까지 추적합니다. 코드와 문서를 정적으로 읽었으며, 설치나 실제 추론·벤치마크를 실행하지 않았습니다. 아래 성능 계산은 이 구현의 추정 방식을 설명하는 것이며 실측 결과가 아닙니다. [분석 대상 소스](https://github.com/AlexsJones/llmfit/tree/e5508a1bdd9184d59add7dc0382219e82f68483d)

## 무엇을 하는 도구인가

llmfit의 핵심은 **내 하드웨어에서 어떤 모델을 어떤 실행 조건으로 사용할 수 있는지 설명하는 것**입니다. 기본 실행은 Terminal User Interface(TUI)를 열고, `recommend`는 추천 결과를 CLI로 제공합니다. 모델 다운로드와 runtime 연동, 벤치마크, Web UI와 REST API도 포함합니다. 문서의 기능 목록을 이해할 때는 모델 적합성 계산과 실제 모델 실행·측정을 서로 다른 기능으로 구분해야 합니다. [README](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/README.md#features)

추천 결과에는 단일 순위 외에도 실행 모드, 선택한 양자화, 메모리 요구량, 적합도 등급, 속도 추정의 근거가 존재합니다. 따라서 숫자 하나보다 그 숫자를 만든 조건이 중요한 도구입니다. 예를 들어 메모리에 들어가는 CPU 실행과 여유 있게 GPU에 상주하는 실행은 동일한 등급을 받을 수 없도록 코드가 구분합니다. [적합도 판정](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/llmfit-core/src/fit.rs#L899)

## 아키텍처: 계산 코어와 사용자 접점

최상위 Cargo workspace는 `llmfit-core`, `llmfit-tui`, `llmfit-desktop`으로 구성됩니다. 기본 빌드 대상은 앞의 두 패키지입니다. 분석 시점 workspace 버전은 `1.1.15`이며, CLI 바이너리 `llmfit`의 진입점은 `llmfit-tui/src/main.rs`입니다. [workspace](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/Cargo.toml#L1), [CLI manifest](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/llmfit-tui/Cargo.toml#L16)

| 구성요소 | 주요 책임 | 추천 경로에서의 역할 |
|---|---|---|
| `hardware.rs` | CPU·메모리·GPU 감지 | 계산에 사용할 `SystemSpecs` 생성 |
| `models.rs` | 모델 카탈로그와 메타데이터 | 내장·사용자·캐시 모델을 통합 |
| `fit.rs` | 실행 모드·양자화·메모리·속도·점수 | 개별 모델의 `ModelFit` 생성 |
| `analysis.rs` | 여러 모델의 공통 분석 | 호환성 필터, 설치 표시, 실측 연결·보정 |
| `providers.rs` | 로컬 runtime 연결 | 설치 모델 조회와 다운로드 인터페이스 |
| `main.rs`·`display.rs` | CLI 제어와 출력 | 옵션 해석, 필터·정렬, JSON·CSV·표 출력 |

코어는 `sysinfo`, `serde`, `ureq` 등을 사용하고, CLI 패키지는 `clap`, `ratatui`, `crossterm`, `axum`, `tokio` 등을 사용합니다. 이름은 TUI 패키지이지만 HTTP API도 이 패키지 안에 있습니다. `serve_api.rs`에는 시스템·모델 조회뿐 아니라 다운로드와 계획 수립 경로도 등록되어 있습니다. [core 의존성](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/llmfit-core/Cargo.toml#L15), [API 라우팅](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/llmfit-tui/src/serve_api.rs#L255)

## 작동 원리: recommend의 입력부터 출력까지

### 1. 명령을 해석하고 분석 조건을 만든다

`main()`은 `Cli::parse()`로 입력을 해석한 뒤 context 제한과 메모리·CPU·하드웨어 profile override를 구성합니다. `Commands::Recommend` 분기는 이를 `run_recommend()`에 전달합니다. 이 함수는 먼저 `detect_specs_and_config()`로 하드웨어와 계산 설정을 확보하고 `ModelDatabase::new()`로 모델 목록을 만듭니다. [진입점](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/llmfit-tui/src/main.rs#L3329), [추천 함수](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/llmfit-tui/src/main.rs#L1939)

`--runtime`과 `--force-runtime`은 역할이 다릅니다. 전자는 계산 결과의 runtime을 기준으로 목록을 걸러내고, 후자는 분석에 전달하는 runtime을 지정합니다. 같은 이름의 runtime을 입력해도 계산 경로를 바꾸는지, 결과를 필터링하는지 차이가 있습니다. 구현은 profile의 계산 설정과 강제 runtime을 동시에 전달할 수 없는 경우 오류를 반환합니다. 한 옵션을 조용히 무시하지 않도록 명시적으로 분기한 부분입니다. [runtime 처리와 조합 검사](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/llmfit-tui/src/main.rs#L1956)

### 2. 하드웨어를 하나의 SystemSpecs로 정리한다

`SystemSpecs::detect()`는 `sysinfo`로 전체·가용 RAM과 CPU 정보를 얻고 GPU 목록을 수집합니다. 가용 RAM 보고가 0인 일부 환경에는 대체 경로가 있습니다. GPU가 여러 개면 대표 GPU 정보와 전체 메모리 합계를 별도로 기록합니다. GPU 모델 이름 하나만 보관하는 구조보다 화면 표시와 용량 계산을 분리하기 쉬운 형태입니다. [하드웨어 감지 구현](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/llmfit-core/src/hardware.rs#L73)

Apple Silicon처럼 통합 메모리를 사용하는 경우에는 단순한 VRAM 수치만으로 충분하지 않습니다. 구현에는 GPU에서 사용할 수 있는 메모리 질의를 위한 별도 필드가 있으며, macOS 전용 의존성으로 Metal의 메모리 작업 집합 한도를 읽을 수 있도록 구성되어 있습니다. 운영체제가 보고하는 RAM, 실제 GPU 사용 가능량, 모델이 차지할 메모리를 구분하려는 설계로 읽을 수 있습니다. [통합 메모리 분기](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/llmfit-core/src/hardware.rs#L131), [Metal 의존성](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/llmfit-core/Cargo.toml#L27)

### 3. 내장 모델에 사용자 정의와 업데이트 캐시를 결합한다

`ModelDatabase::new()`의 실제 순서는 다음과 같습니다.

1. 컴파일 시 내장된 모델을 읽습니다.
2. 사용자 정의 모델이 있으면 같은 canonical slug의 내장 항목을 교체하고 새 항목을 추가합니다.
3. `llmfit update` 캐시는 이미 존재하지 않는 slug만 추가합니다.
4. MoE의 공개된 활성 파라미터 정보를 적용합니다.

여기서 slug는 조직 접두사를 제거하고 대소문자와 일부 구분자를 정규화한 키입니다. 이 정책은 표기 차이로 인한 중복을 줄이지만, 원래 Hugging Face의 전체 저장소 ID와 같은 개념은 아닙니다. 사용자 정의 모델을 넣을 때는 이러한 교체 기준을 알아야 결과를 해석할 수 있습니다. [정규화](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/llmfit-core/src/models.rs#L1352), [모델 통합](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/llmfit-core/src/models.rs#L1792)

문서와 구현 사이에 주의할 차이도 있습니다. `docs/how-it-works.md`는 최종 사용자가 프로그램을 업그레이드해 내장 DB를 갱신한다고 설명합니다. 이는 내장 목록에 대한 설명으로는 맞지만, 현재 구현은 위와 같이 사용자 모델과 업데이트 캐시도 합칩니다. 따라서 “사용할 수 있는 모델 목록은 바이너리에 고정되어 있다”라고 해석하면 현재 코드의 동작을 충분히 설명하지 못합니다. [문서의 모델 DB 설명](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/docs/how-it-works.md#model-database)

### 4. 설치 정보와 실행 호환성을 연결한다

`InstalledIndex::detect_all()`은 Ollama·MLX·llama.cpp·Docker Model Runner·LM Studio·vLLM·RamaLama의 설치 모델 정보를 별도 스레드로 조회합니다. 조회를 병렬로 수행해 느린 provider 하나 때문에 모든 조회가 직렬로 지연되는 상황을 줄이려는 구조입니다. 이는 코드의 구성에 대한 설명이며 실제 소요 시간을 측정한 결과는 아닙니다. [설치 모델 조회](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/llmfit-core/src/analysis.rs#L59)

공통 `ModelProvider` trait에는 provider 이름, 가용성, 설치 모델, 다운로드 시작 메서드가 정의되어 있습니다. 다운로드는 `PullHandle`과 진행·완료·오류 이벤트로 표현합니다. 추천 계산이 개별 runtime의 세부 API와 직접 얽히지 않도록 경계를 만든 부분입니다. [provider 계약](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/llmfit-core/src/providers.rs#L14)

모델 분석에 앞서 `rankable_models()`는 backend 비호환 모델과 정제 과정에서 제외된 모델을 걸러냅니다. 이후 `build_fits()`가 각 모델을 분석하고 설치 여부를 표시합니다. 즉, 최종 목록의 길이가 카탈로그 전체 개수와 같을 필요는 없습니다. [공통 분석 경로](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/llmfit-core/src/analysis.rs#L191)

### 5. 양자화와 메모리 배치로 실행 모드를 결정한다

양자화(Quantization)는 가중치를 더 낮은 정밀도로 표현해 저장 공간과 메모리 요구량을 줄이는 방식입니다. llmfit은 모델 형식과 runtime에 맞는 양자화 계층을 사용합니다. ONNX·MLX·GGUF 계열에 서로 다른 목록을 적용하고, 이미 양자화된 모델은 고정된 형식을 유지합니다. 따라서 모든 모델을 같은 GGUF 양자화 이름으로 처리하지 않습니다. [양자화 선택](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/llmfit-core/src/fit.rs#L642)

실행 경로는 메모리 상황에 따라 달라집니다. 모델 전체가 GPU 메모리에 들어가면 GPU 경로를 선택하고, 부족하면 시스템 RAM을 이용하는 경로를 검토합니다. MoE(Mixture-of-Experts)는 일부 expert만 토큰 계산에 활성화되므로 별도 offload 분기가 존재합니다. 다만 활성 파라미터가 적다는 사실이 전체 가중치 저장 공간이 사라진다는 뜻은 아닙니다. 구현도 속도 추정에는 활성 파라미터를 사용하면서 메모리 적합성에는 전체 모델 크기를 고려한다고 구분합니다. [배치 선택](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/llmfit-core/src/fit.rs#L580), [활성 파라미터와 메모리 구분](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/llmfit-core/src/fit.rs#L1570)

적합도 등급은 선택한 경로의 메모리 점유 비율을 기준으로 합니다.

| 요구량 / 사용 가능량 | 메모리 기준 등급 |
|---|---|
| 60% 이하 | Perfect |
| 60% 초과, 85% 이하 | Good |
| 85% 초과, 98% 이하 | Marginal |
| 98% 초과 또는 유효하지 않은 비율 | TooTight |

GPU와 Tensor Parallel 경로는 이 등급을 그대로 사용합니다. CPU 전용·CPU offload·MoE offload는 최대 Good으로 제한됩니다. `Perfect`에 메모리 여유와 GPU 실행이라는 의미를 함께 부여한 것입니다. 이 임계값은 구현의 정책이며 모든 runtime에서 로딩 성공을 보장하는 물리 법칙은 아닙니다. [상수와 등급 상한](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/llmfit-core/src/fit.rs#L899)

### 6. 생성 속도와 첫 토큰 시간을 서로 다른 방식으로 추정한다

토큰 생성인 decode의 GPU 대역폭 경로는 대략 “메모리 대역폭 / 읽어야 할 가중치 크기 × 효율·실행 모드 계수”를 출발점으로 사용합니다. GPU 대역폭을 알 수 없으면 backend별 상수 경로를 사용합니다. 실제 함수는 MoE와 runtime 등에 따른 추가 분기를 포함하므로 이 간략식을 모든 모델의 최종 계산식으로 받아들여서는 안 됩니다. [속도 추정 함수](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/llmfit-core/src/fit.rs#L1570)

입력 prompt를 처리하는 prefill은 별도입니다. `estimate_prefill()`은 GPU의 FP16 연산 성능이 유효한 경우 활성 파라미터당 연산량과 이용률로 처리량을 구하고, prompt 길이로 Time To First Token(TTFT)을 계산합니다. GPU 연산량 정보가 없거나 CPU 전용이면 두 값을 `None`으로 반환합니다. 추정할 수 없는 상태를 “0 token/s”와 구분한다는 점이 중요합니다. [prefill 구현](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/llmfit-core/src/fit.rs#L1512)

결과에는 대역폭·효율·가정한 context·계산 방식 등을 담은 `estimate_basis`도 기록합니다. 추천 결과를 비교할 때 모델 이름만 같다고 조건이 같다고 판단할 수 없는 이유입니다. [추정 근거 기록](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/llmfit-core/src/fit.rs#L688)

### 7. 실측을 우선 연결하고 추정치를 보정한다

`build_fits()`는 로컬 측정, 같은 하드웨어의 커뮤니티 측정, 대응 preset의 측정 인덱스 순으로 값을 찾습니다. 측정값을 연결한 후 confidence를 갱신하고 로컬 calibration을 적용합니다. 같은 token/s 표기라도 측정치와 추정치를 구분할 정보를 보관하는 구조입니다. [측정 우선순위](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/llmfit-core/src/analysis.rs#L284)

보정은 1B 이상 dense 모델 중 적합한 실측이 있는 항목의 “실측 / 보정 전 추정” 비율을 모아 중앙값을 사용합니다. 보정 계수는 `0.05`와 `3.0` 사이로 제한되며, 다시 적용하더라도 보정이 계속 곱해지지 않도록 원래 추정값을 복원합니다. MoE와 작은 모델은 이 보정 기준점에서 제외합니다. 이는 모든 종류의 모델이 같은 대역폭 관계로 움직이지 않는다는 구현상의 가정을 반영합니다. [보정 코드](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/llmfit-core/src/analysis.rs#L339)

한 가지 읽어 둘 세부사항은 보정 함수가 `estimated_tps`와 근거·confidence를 갱신하지만 `score`를 다시 계산하지는 않는다는 점입니다. 최종 기본 정렬은 `score`를 사용하므로, “속도 추정이 실측으로 보정되면 추천 순위도 반드시 그에 맞춰 다시 계산된다”라고 단정할 수 없습니다. [보정 대상 필드](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/llmfit-core/src/analysis.rs#L369), [기본 정렬](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/llmfit-core/src/fit.rs#L1131)

### 8. 점수와 필터를 거쳐 결과를 출력한다

종합 점수는 Quality·Speed·Fit·Context의 가중합입니다. 각 축이 담는 의미를 구분해야 합니다. 메모리 등급 `fit_level`과 연속값인 Fit 점수는 같은 값이 아니며, Context 점수 역시 실제 요청 전체에 대한 품질 측정이 아닙니다. 코드의 Context 점수는 용도별 목표 길이와 모델의 context 길이를 비교합니다. [점수 구성](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/llmfit-core/src/fit.rs#L1884), [Context와 가중합](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/llmfit-core/src/fit.rs#L2096)

여기에도 문서와 구현의 차이가 있습니다. 설명 문서는 Fit의 적정 사용률을 50~80%라고 적지만, 현재 `fit_score()`는 70% 이하에 100점을 주고 그 이후 Gaussian 형태로 완만하게 낮춥니다. 메모리를 적게 쓰는 모델을 별도로 감점하지 않는 구현입니다. 따라서 현재 추천 방식을 설명할 때는 이 코드를 기준으로 읽는 편이 정확합니다. [현재 Fit 점수](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/llmfit-core/src/fit.rs#L2079), [문서의 scoring 설명](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/docs/how-it-works.md#how-it-works)

마지막으로 `run_recommend()`는 최소 적합도, runtime, use case, capability, license 조건을 적용합니다. 이 중 `--use-case`는 계산된 모델의 용도 분류와 일치하는 행을 남기는 필터입니다. 이어 종합 점수로 정렬하고 요청한 개수로 제한한 뒤 JSON·CSV·터미널 표로 출력합니다. 추천 결과가 만들어지는 전체 흐름은 **하드웨어와 모델 확보 → 개별 분석 → 실측 연결·보정 → 조건 필터 → 점수 정렬 → 직렬화**로 정리할 수 있습니다. [필터와 출력](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/llmfit-tui/src/main.rs#L1998)

## 문서에 제시된 설치와 사용법

다음은 분석 커밋의 README에 있는 Homebrew 설치와 CLI 사용 명령입니다. 이 리뷰에서 명령을 실행하거나 설치 성공을 확인한 것은 아닙니다. [설치 문서](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/README.md#install), [사용 문서](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/README.md#usage)

```sh
brew install AlexsJones/llmfit/llmfit
```

```sh
llmfit
llmfit recommend --json
llmfit fit
llmfit doctor
```

`llmfit`은 대화형 화면, `recommend --json`은 스크립트가 소비할 추천 결과, `fit`은 모델별 적합도 표, `doctor`는 감지 진단에 해당합니다. 특정 하드웨어를 가정하는 profile과 runtime을 강제로 바꾸는 옵션은 조합 제약이 있으므로 그 조건도 결과와 함께 보관해야 합니다. [profile 제약](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/docs/cli.md#L292)

## 한계와 해석 시 주의할 점

이 코드의 추천은 카탈로그 메타데이터·하드웨어 감지·추정식에 의존합니다. 감지 정보가 누락될 때 대체 경로가 사용되고, 모델별 runtime 특성과 양자화 조건도 결과에 영향을 줍니다. `estimated_tps`, 측정값, confidence, `estimate_basis`를 함께 읽어야 숫자가 어떤 근거를 갖는지 판단할 수 있습니다. 이 글에서는 실제 장비별 오차율이나 추천 성공률을 측정하지 않았습니다. [추정 근거](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/llmfit-core/src/fit.rs#L688)

현재 구현에서 profile과 forced runtime의 동시 사용은 명시적으로 거부됩니다. 또한 위에서 확인한 문서와 코드의 점수·카탈로그 설명 차이는 버전 고정 분석이 필요한 이유를 보여 줍니다. 사용 중인 바이너리 버전과 다른 문서를 읽으면 같은 추천 결과를 다르게 해석할 수 있습니다. [조합 제한](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/llmfit-tui/src/main.rs#L1974)

저장소 자체는 MIT License를 명시합니다. 그러나 이 프로젝트의 라이선스가 카탈로그에 실린 모든 모델의 라이선스를 대신하지는 않습니다. 실제 코드에도 모델별 license 필터가 별도로 있으며, 모델 선택에서 소프트웨어와 모델 가중치의 조건을 구분할 필요가 있습니다. [프로젝트 라이선스](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/LICENSE), [모델 license 필터](https://github.com/AlexsJones/llmfit/blob/e5508a1bdd9184d59add7dc0382219e82f68483d/llmfit-core/src/models.rs#L719)

## 결론

llmfit의 핵심 설계는 하드웨어 용량, 모델 메타데이터, 실행 경로, 속도 근거를 하나의 분석 결과로 모으는 데 있습니다. 추천 순위만 보여 주는 데서 끝나지 않고, 선택된 양자화·메모리 등급·추정 방식·실측 여부를 함께 표현합니다. `analysis.rs`가 공통 모델 분석을 모으고 `fit.rs`가 계산을 담당하는 구분도 여러 사용자 인터페이스가 같은 계산을 재사용하는 데 의미가 있습니다.

코드에서 확인한 중요한 해석 경계는 세 가지입니다. 메모리 적합도와 종합 점수는 다르고, 속도 추정과 실측은 다르며, 실측 기반 보정이 기본 순위 재계산을 의미하지는 않습니다. 이러한 구분을 유지하면 llmfit의 결과를 “어떤 모델이 왜 후보가 되었는지” 설명하는 자료로 읽을 수 있습니다.

### 이 글에서 다루지 못한 부분

이 리뷰는 CLI 추천의 핵심 경로에 집중했습니다. 하드웨어 감지의 모든 운영체제별 fallback, `quality.rs`의 세부 품질 휴리스틱, MoE·Tensor Parallel의 전체 수식, 각 provider의 다운로드·실행 절차, 벤치마크 수집·공유 프로토콜, `plan.rs`의 업그레이드 시뮬레이션, MCP·NATS 연결, Web UI·TUI의 모든 이벤트와 데스크톱 UI는 상세 분석하지 않았습니다. HTTP 라우트는 존재와 구성만 확인했으며 인증·동시성·외부 노출의 안전성을 평가하지 않았습니다. 이러한 기능의 이름이 본문에 등장한다고 해서 해당 영역 전체를 검증한 것은 아닙니다.
