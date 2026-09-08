---
title: "NVIDIA GTC 2026 키노트 완벽 정리: Inference Inflection부터 Physical AI까지"
date: "2026-03-17"
tags:
  - "Nvidia"
year: "2026"
---

# NVIDIA GTC 2026 키노트 완벽 정리: Inference Inflection부터 Physical AI까지

![](https://velog.velcdn.com/images/euisuk-chung/post/78815564-9efb-449c-8f6f-35502efab494/image.png)

> <https://youtu.be/jw_o0xr8MWU>

2025년 3월 17일, NVIDIA의 CEO Jensen Huang이 GTC 2026 키노트를 통해 AI 산업의 현재와 미래를 조망했습니다. 450개 기업이 스폰서로 참여하고, 1,000개의 기술 세션과 20,000명의 연사가 함께한 이번 GTC는 AI 인프라의 5개 레이어(토지/전력/셸 → 인프라 → 칩 → 플랫폼/모델 → 애플리케이션)를 모두 아우르는 역대 최대 규모의 행사였습니다.

이 글에서는 키노트 발표 순서를 그대로 따라가며, 핵심 내용을 빠짐없이 정리합니다.

---

1. CUDA의 20년, 그리고 Flywheel 효과
-----------------------------

Jensen은 키노트의 시작을 **CUDA의 20주년 기념**으로 열었습니다. CUDA는 SIMT(Single Instruction Multi-Threaded) 아키텍처를 기반으로, Scalar 코드를 멀티스레드 애플리케이션으로 쉽게 변환할 수 있게 설계된 혁명적인 발명입니다. 최근에는 Tensor Core 프로그래밍을 돕기 위한 Tile 기능이 추가되었고, 수천 개의 도구, 컴파일러, 프레임워크, 라이브러리가 오픈소스로 제공되고 있습니다.

Jensen은 NVIDIA 전략의 핵심을 하나의 차트로 설명했습니다. 바로 **Flywheel(플라이휠)** 모델입니다.

* **Installed Base(설치 기반)**: 20년에 걸쳐 전 세계 수억 대의 GPU와 컴퓨팅 시스템에 CUDA가 설치되었습니다. 모든 클라우드, 모든 컴퓨터 회사에 NVIDIA가 존재합니다.
* **개발자 유입**: 설치 기반이 개발자를 끌어들이고, 개발자가 새로운 알고리즘을 만들어 Deep Learning 같은 브레이크스루를 달성합니다.
* **새로운 시장 창출**: 브레이크스루가 새 시장을 만들고, 새 시장이 새 생태계를 구축하며, 더 큰 설치 기반으로 이어집니다.

이 Flywheel이 가속되고 있으며, NVIDIA 라이브러리 다운로드 수가 대규모에서도 과거 어느 때보다 빠르게 성장하고 있다고 강조했습니다. 또한 Ampere GPU가 6년 전 출하되었음에도 클라우드에서의 가격이 오히려 상승하고 있는데, 이는 CUDA 플랫폼 위에서 실행 가능한 애플리케이션이 너무나 다양하기 때문에 GPU의 유효 수명(Useful Life)이 극도로 길기 때문이라고 설명했습니다.

핵심 메시지는 명확합니다. NVIDIA는 소프트웨어를 지속적으로 업데이트함으로써, 동일한 하드웨어에서 **최초 도입 시의 성능 향상(First-time Pop)** 뿐 아니라 **시간에 따른 지속적 비용 절감**까지 제공한다는 것입니다.

---

2. GeForce에서 Neural Rendering까지: 25년의 그래픽스 여정
---------------------------------------------

Jensen은 CUDA의 기원을 25년 전 GeForce까지 거슬러 올라갔습니다.

* **25년 전**: Programmable Shader 발명. 세계 최초의 프로그래머블 가속기인 Pixel Shader가 탄생했습니다.
* **20년 전**: CUDA 발명. GeForce 위에 CUDA를 올려 모든 컴퓨터에 배포하겠다는 결정은 당시 회사 이익의 대부분을 소모하는 거대한 투자였습니다.
* **GeForce가 AI를 세상에 가져옴**: GeForce 덕분에 Alex Krizhevsky, Ilya Sutskever, Geoffrey Hinton, Andrew Ng 등이 GPU로 Deep Learning을 가속할 수 있었습니다.
* **8년 전**: RTX 아키텍처 도입. Hardware Ray Tracing과 AI를 결합한 새로운 그래픽스 패러다임이 시작되었습니다.

그리고 키노트에서 차세대 그래픽스 기술인 **Neural Rendering**과 **DLSS 5**가 공개되었습니다. 이는 3D 그래픽스와 AI를 융합한 것으로, 제어 가능한(Controllable) 3D 그래픽스의 Structured Data와 Generative AI의 Probabilistic Computing을 결합합니다. 하나는 완전히 예측 가능하고, 다른 하나는 확률적이지만 매우 사실적인데, 이 둘을 결합하여 아름답고 제어 가능한 콘텐츠를 생성합니다.

Jensen은 이 "Structured Data + Generative AI" 융합 컨셉이 산업 전반에 걸쳐 반복될 것이라고 강조했습니다.

---

3. 데이터 처리의 혁신: cuDF, cuVS, 그리고 클라우드 파트너십
----------------------------------------

### 3.1 Structured Data와 Unstructured Data

Jensen은 데이터 처리의 두 축을 제시했습니다.

**Structured Data**는 SQL, Spark, pandas, Polars 등으로 처리되는 데이터프레임 기반의 "비즈니스의 Ground Truth"입니다. Snowflake, Databricks, Amazon EMR, Azure Fabric, Google BigQuery 같은 플랫폼들이 이를 다루고 있습니다. 미래에는 AI Agent가 이 Structured Database를 직접 사용하게 되므로, 데이터 처리 속도를 극적으로 높여야 합니다.

**Unstructured Data**는 PDF, 영상, 음성 등 전 세계 생성 데이터의 약 90%를 차지하지만, 지금까지는 인덱싱이 불가능해 사실상 활용이 불가능했습니다. 이제 Multimodality Perception & Understanding을 활용한 AI가 이 데이터의 의미를 이해하고, 검색 가능한 구조로 임베딩합니다.

NVIDIA는 이 두 가지를 위해 핵심 라이브러리를 만들었습니다.

* **cuDF**: Structured Data(데이터프레임) 가속 라이브러리
* **cuVS**: Vector Store 가속 라이브러리 (Semantic/Unstructured Data)

### 3.2 주요 파트너십 발표

* **IBM**: SQL의 발명사인 IBM이 WatsonX Data의 시퀄 엔진을 cuDF로 가속합니다. 사례로 Nestlé는 185개국의 공급망 데이터를 GPU 가속 WatsonX Data로 처리하여, CPU 대비 5배 빠르고 83% 낮은 비용을 달성했습니다.
* **Dell**: Dell AI Data Platform에 cuDF와 cuVS를 통합하여 On-Prem 환경의 AI 데이터 플랫폼을 구축했습니다. NTT Data와의 협업에서 큰 속도 향상을 보여주었습니다.
* **Google Cloud**: BigQuery 가속을 통해 Snapchat의 컴퓨팅 비용을 약 80% 절감했습니다.

### 3.3 클라우드 서비스 파트너 생태계

Jensen은 NVIDIA와 주요 클라우드 서비스 제공자(CSP)들의 관계를 상세히 설명했습니다.

* **Google Cloud**: Vertex AI, BigQuery 가속. JAX/XLA와 PyTorch 모두에서 뛰어난 성능. Base Ten, CrowdStrike, PUMA, Salesforce 등이 고객으로 활동합니다.
* **AWS**: EMR, SageMaker, Bedrock 가속. OpenAI를 AWS에 가져오는 새로운 파트너십을 발표했습니다.
* **Microsoft Azure**: NVIDIA의 첫 A100 슈퍼컴퓨터가 Azure에 설치되었고, 이것이 OpenAI와의 파트너십으로 이어졌습니다. Azure Cloud, AI Foundry, Bing Search 가속. 기밀 컴퓨팅(Confidential Computing)을 통해 OpenAI와 Anthropic 모델의 안전한 배포를 지원합니다.
* **Oracle**: NVIDIA는 Oracle의 첫 AI 고객이자 첫 공급업체였습니다. OpenAI, Cohere, Fireworks 등이 Oracle Cloud에서 활동합니다.
* **CoreWeave**: 세계 최초의 AI Native Cloud로, GPU 호스팅만을 위해 설계된 회사입니다.
* **Palantir + Dell**: 3사가 협력하여 에어갭(Air-gapped) 환경, 온프레미스, 현장 어디서든 배포 가능한 AI 플랫폼을 구축했습니다.

---

4. Vertically Integrated, Horizontally Open
-------------------------------------------

Jensen은 NVIDIA의 정체성을 **"수직적으로 통합되었지만, 수평적으로 개방된"** 회사라고 정의했습니다.

Accelerated Computing의 핵심은 "Application Acceleration"입니다. CPU가 모든 것을 범용으로 빠르게 하던 시대(Moore's Law)가 끝났기 때문에, 이제는 도메인별 가속(Domain-Specific Acceleration)만이 큰 성능 향상과 비용 절감을 가져올 수 있습니다. 이것이 NVIDIA가 라이브러리-도메인-버티컬별로 확장해야 하는 이유입니다.

NVIDIA는 애플리케이션과 도메인의 알고리즘을 이해하고, 데이터센터/클라우드/온프레미스/엣지/로보틱스 등 다양한 배포 환경에 맞게 최적화합니다. 동시에, 이 기술을 세계의 모든 플랫폼에 통합하여 개방합니다.

---

5. 산업별 영향력과 AI Native 기업의 부상
----------------------------

### 5.1 버티컬 산업

GTC 2026에서 NVIDIA가 다루는 주요 산업 버티컬은 다음과 같습니다.

* **자율주행**: 광범위한 도달 범위와 영향력
* **금융 서비스**: GTC 최대 참석자 비중. 퀀트 기반 고전적 ML에서 Transformer 기반 딥러닝/LLM으로 전환 중
* **헬스케어**: Drug Discovery를 위한 AI Biology, 진단용 AI Agent, Physical AI 로봇 시스템
* **산업**: AI Factory, 칩 공장, 컴퓨터 공장 등 역사상 최대 규모의 건설
* **미디어/엔터테인먼트/게임**: 실시간 AI 플랫폼, 번역, 방송
* **양자 컴퓨팅**: 35개 기업이 차세대 Quantum-GPU 하이브리드 시스템 개발 중
* **리테일/CPG**: 공급망 최적화, Agentic 쇼핑 시스템 (\$35T 산업)
* **로보틱스**: 제조업 \$50T 산업, NVIDIA는 10년간 로봇을 위한 3대 컴퓨터(Training, Synthetic Data, Robot 내장)를 개발
* **통신**: \$2T 산업. 기지국이 AI 인프라 플랫폼(AI RAN)으로 변환. Nokia, T-Mobile 등과 협력

### 5.2 CUDA X 라이브러리

NVIDIA의 "Crown Jewels"는 CUDA X 라이브러리입니다. 이번 GTC에서 약 100개의 라이브러리와 40개의 모델을 발표했습니다. 대표적인 것들은 다음과 같습니다.

* **cuDNN**: Deep Neural Network 라이브러리. 현대 AI 빅뱅의 원동력
* **cuOpt**: 의사결정 최적화
* **cuLitho**: Computational Lithography
* **cuDSS**: Direct Sparse Solver
* **Aerial**: AI RAN
* **Warp**: Differentiable Physics
* **Parabricks**: Genomics

Jensen은 NVIDIA를 "알고리즘 회사"라고 표현하며, 이러한 도메인별 라이브러리가 컴퓨팅 플랫폼을 활성화하여 실제 문제 해결에 연결하는 핵심이라고 강조했습니다.

### 5.3 AI Native 기업의 폭발적 성장

지난 2년간 AI Native 기업에 대한 벤처 투자가 \$150B(역사상 최대)에 달했습니다. 투자 규모도 수백만 달러에서 수억~수십억 달러로 급증했습니다. OpenAI, Anthropic을 비롯한 수많은 AI Native 기업들이 탄생했고, PC 혁명, 인터넷 혁명, 모바일/클라우드 혁명에 이은 새로운 플랫폼 전환기의 시작을 알리고 있습니다.

---

6. AI의 3대 Inflection과 Inference Inflection의 도래
----------------------------------------------

Jensen은 지난 2년간 AI에서 일어난 세 가지 결정적 전환점을 설명했습니다.

**첫 번째, Generative AI (ChatGPT, 2022-2023)**. AI가 인식(Perceive)과 이해(Understand)를 넘어, 고유한 콘텐츠를 생성(Generate)할 수 있게 되었습니다. 컴퓨팅 패러다임 자체가 Retrieval 기반에서 Generative 기반으로 전환되었습니다.

**두 번째, Reasoning AI (O1, 2023-2024)**. AI가 스스로 반성(Reflect)하고, 사고(Think)하고, 계획(Plan)하고, 문제를 분해(Decompose)할 수 있게 되었습니다. O1은 Generative AI를 신뢰할 수 있고 사실에 기반한(Grounded on Truth) 것으로 만들었습니다. 이로 인해 Input/Output Token 사용량이 크게 증가했습니다.

**세 번째, Agentic AI (Claude Code, 2024-2025)**. 최초의 Agentic 모델로, 파일 읽기, 코딩, 컴파일, 테스트, 평가, 반복을 자율적으로 수행합니다. NVIDIA 전사적으로 100%의 소프트웨어 엔지니어가 Claude Code, Codex, Cursor 중 하나 이상을 사용하고 있습니다. AI에게 "무엇이, 어디서, 언제, 어떻게"를 묻는 것이 아니라 "만들어라, 해라, 구축하라"고 지시하는 시대가 열렸습니다.

이 세 가지 전환의 결과로, **지난 2년간 AI 컴퓨팅 수요가 약 100만 배 증가**했습니다. 작업당 필요한 연산량이 약 10,000배, 사용량이 약 100배 증가한 것입니다.

이것이 바로 **Inference Inflection**입니다. AI가 생각하고(Think), 행동하고(Do), 읽고(Read), 추론하고(Reason), 생성(Generate)할 때마다 Inference가 필요합니다. 이제 Training을 넘어 Inference가 AI의 핵심 워크로드가 되었습니다.

Jensen은 작년 GTC에서 2026년까지 \$500B의 고신뢰 수요를 전망했는데, 올해는 **2027년까지 최소 \$1T(1조 달러)** 의 수요를 확인했다고 발표했습니다.

---

7. 2025년 Inference의 해: Blackwell의 성과
------------------------------------

2025년은 NVIDIA의 "Inference의 해"였습니다. Hopper가 전성기에 있을 때 과감하게 아키텍처를 재설계하여, NVLink 8에서 NVLink 72로 확장하고, 시스템을 완전히 Disaggregate했습니다.

핵심 기술 혁신은 다음과 같습니다.

* **NVLink 72**: 72개 GPU를 NVLink로 연결한 거대한 단일 컴퓨팅 유닛
* **NVFP4**: 새로운 Tensor Core 및 연산 유닛. 정밀도 손실 없이 Inference 성능과 에너지 효율을 크게 향상. Training에도 적용 가능
* **Dynamo**: AI Factory를 위한 운영체제
* **TensorRT-LLM**: 추론 최적화를 위한 알고리즘 스택

Semi Analysis의 대규모 AI Inference 벤치마크 결과에서, NVIDIA의 Grace Blackwell NVLink 72는 Hopper H200 대비 **35~50배의 성능 향상**을 달성했습니다. Moore's Law 기준으로는 1.5배 정도가 예상되었을 것입니다.

Jensen은 Token Factory라는 개념을 도입했습니다. 데이터센터는 더 이상 파일 저장소가 아니라, Token을 생산하는 공장입니다. 1 Gigawatt 데이터센터에서 Tokens/Watt(전력 당 토큰 생산량)와 Token Speed(토큰 속도)가 핵심 지표이며, 이것이 곧 수익으로 직결됩니다.

실제로 Fireworks, Together 등의 Inference 서비스 제공 업체에 NVIDIA 소프트웨어 업데이트를 적용한 결과, 동일 시스템에서 약 700 tokens/sec에서 약 5,000 tokens/sec로 **7배 향상**되었습니다.

---

8. Vera Rubin: 차세대 AI 슈퍼컴퓨터 플랫폼
-------------------------------

### 8.1 10년의 아키텍처 진화

Jensen은 DGX-1(2016)부터 Vera Rubin까지의 10년 진화를 요약했습니다.

* **DGX-1 (2016, Pascal)**: 최초의 딥러닝 전용 컴퓨터. NVLink 1세대, 170 TFLOPS
* **DGX A100 (2020, Ampere)**: NVLink 3, Scale-up + Scale-out 결합. Mellanox 합류
* **Hopper**: FP8 Transformer Engine 도입. Generative AI 시대 개막. NVLink 4, ConnectX-7, Quantum InfiniBand
* **Grace Blackwell**: NVLink 72, 72개 GPU 연결, 130 Exabytes/sec. ConnectX-8, Spectrum X Ethernet

### 8.2 Vera Rubin 플랫폼 상세

Vera Rubin은 Agentic AI 시대를 위해 설계된 차세대 플랫폼으로, CPU/스토리지/네트워킹/보안 등 컴퓨팅의 모든 축을 혁신합니다.

**7개의 칩, 5개의 랙 스케일 컴퓨터, 1개의 혁명적 AI 슈퍼컴퓨터:**

* **Vera Rubin GPU (NVLink 72)**: 3.6 Exaflops, 260 TB/sec All-to-All NVLink 대역폭
* **Vera CPU**: Agentic 워크로드를 위한 오케스트레이션 전용 CPU. 세계 유일의 LPDDR5 탑재 데이터센터 CPU. 극도로 높은 싱글 스레드 성능과 에너지 효율. 독립 판매만으로도 수십억 달러 규모 사업
* **STX Rack**: BlueField 기반의 AI Native 스토리지. KV Cache, cuDF, cuVS 가속 스토리지
* **Groq LPX RC**: Vera Rubin에 긴밀하게 연결된 Token Accelerator. 대용량 On-chip SRAM 탑재. Vera Rubin 대비 **35배 더 높은 Throughput/Megawatt**
* **ConnectX-9 + BlueField 4**: 차세대 네트워킹
* **Spectrum X CPO**: 세계 최초 Co-Packaged Optics 스위치. TSMC와 공동 개발한 CuP 공정기술로 양산 중

**10년간 4,000만 배의 컴퓨팅 성능 향상을 달성했습니다.**

### 8.3 물리적 설계 특징

* 100% 액체 냉각, 케이블 제거 → 설치 시간이 2일에서 2시간으로 단축
* 45도 온수 냉각으로 데이터센터 냉각 비용과 에너지를 시스템에 활용
* 6세대 NVLink Scale-up 스위칭 시스템 (NVIDIA만의 독자 기술)

### 8.4 Groq 통합: Disaggregated Inference

Jensen은 Groq 인수의 전략적 의미를 상세히 설명했습니다. Groq LPU는 Deterministic Dataflow Processor로, 정적 컴파일/정적 스케줄링으로 동작하며, 대용량 SRAM으로 추론 전용으로 설계되었습니다.

하지만 Groq 칩 하나에는 500MB SRAM만 있어서, Trillion Parameter 모델의 전체 파라미터와 KV Cache를 담기엔 역부족이었습니다. NVIDIA는 **Dynamo를 통한 Disaggregated Inference** 아키텍처로 이 문제를 해결했습니다.

* **Prefill + Attention(Decode 중)**: Vera Rubin이 담당 (높은 수학 연산, 대용량 KV Cache)
* **Feed-forward / Token Generation(Decode 중)**: Groq가 담당 (저지연, 대역폭 한정 워크로드)

두 프로세서가 Ethernet 위에서 특수 모드(지연 50% 감소)로 긴밀하게 결합됩니다. 결과적으로, 가장 높은 가치의 서비스 티어에서 **35배 성능 향상**과 함께, 기존에는 불가능했던 초고속 Token 생성 티어가 새로 열렸습니다.

### 8.5 Token Economy 분석

Jensen은 Token을 새로운 상품(Commodity)으로 정의하고, Token Factory의 경제학을 설명했습니다. 1 Gigawatt 데이터센터의 전력을 서비스 티어별로 배분하는 모델을 제시했습니다.

* **Free Tier**: 높은 Throughput, 낮은 속도 → 고객 유치
* **Medium Tier (\$3/M tokens)**: 중간 모델 크기, 중간 속도
* **High Tier (\$6~\$45/M tokens)**: 더 큰 모델, 더 긴 Context, 더 높은 속도 → 스마트한 AI
* **Premium Tier (\$150/M tokens)**: 최고 속도 Token 생성. 연구팀이 하루 5천만 Token을 사용해도 비용이 부담되지 않는 수준

Blackwell → Vera Rubin으로의 전환은 동일 전력에서 **5배의 수익 증가**를 의미합니다. Groq를 25% 추가하면 수익을 더 확장할 수 있습니다. 또한 Vera Rubin은 2년 내에 1GW 팩토리에서 Token 생성 속도를 2,200만에서 7억으로, **350배 향상**시킬 전망입니다.

Samsung이 Groq LP30 칩을 제조하며, Q3에 출하 예정입니다. Vera Rubin RC(Research Chip)는 이미 Microsoft Azure에서 가동 중입니다.

---

9. 로드맵: Rubin Ultra에서 Feynman까지
-------------------------------

### 9.1 현재 ~ 근미래

* **Grace Blackwell (현재)**: Oberon 시스템. 기존 랙 시스템과 호환
* **Vera Rubin**: Oberon 시스템. Copper Scale-up(NVLink 72) + Optical Scale-up(NVLink 576) 모두 지원
* **Vera Rubin Ultra**: 새로운 Rubin Ultra 칩 + LP35(NVFP4 내장). Kyber 랙 시스템으로 NVLink 144 지원. 144개 GPU를 하나의 NVLink 도메인으로 연결

### 9.2 차세대: Feynman

* **새로운 GPU**
* **LP40**: NVIDIA와 Groq 팀의 통합 설계. 대폭적인 성능 향상
* **Rosa CPU** (Sure for Rosa)
* **BlueField 5 + ConnectX-10**
* **Kyber Copper Scale-up + Kyber CPO Scale-up**: 최초로 Copper와 Co-Packaged Optics 두 가지로 Scale-up 가능

Jensen은 Copper, Optical Scale-up, Optical Scale-out 모두가 필요하며, 모든 방식의 용량을 대폭 늘려야 한다고 강조했습니다.

---

10. AI Factory 플랫폼: NVIDIA DGX
------------------------------

NVIDIA는 칩 회사에서 AI Factory 회사로 진화했습니다. AI Factory 내부에서 낭비되는 전력을 최소화하기 위해, **NVIDIA DGX 플랫폼**을 만들었습니다.

* **Omniverse DGX World**: 모든 구성요소 제조사가 가상으로 만나 Gigawatt 규모 AI Factory를 설계하는 Digital Twin 플랫폼
* **DGX Sim**: 랙의 기계/열/전기/네트워킹 시뮬레이션. Siemens Star-CCM+, Cadence, ETAP 등의 도구와 통합
* **DGX Exchange**: AI Factory 운영 데이터 교환
* **DGX Flex**: 그리드와 데이터센터 간 동적 전력 관리
* **DGX Max-Q**: 동적으로 Token Throughput 최대화

Digital Twin이 운영자가 되어, AI Agent가 DGX Max-Q와 협력하여 인프라를 동적으로 오케스트레이션합니다. Jensen은 여기에 **2배의 효율 개선 가능성**이 있다고 언급했습니다.

또한 **Vera Rubin Space 1**이라는 우주용 컴퓨터도 발표했습니다. Thor 칩이 이미 방사선 인증을 받아 위성에 탑재되어 있으며, 향후 우주에 데이터센터를 구축할 계획입니다.

---

11. OpenClaw: Agentic AI의 Linux
-------------------------------

키노트의 가장 중요한 발표 중 하나는 **OpenClaw**에 대한 NVIDIA의 지원 발표였습니다. Peter Steinberger가 개발한 OpenClaw는 인류 역사상 가장 빠르게 성장한 오픈소스 프로젝트로, 불과 몇 주 만에 Linux가 30년간 달성한 것을 넘어섰습니다.

### 11.1 OpenClaw란 무엇인가

Jensen은 OpenClaw를 운영체제(OS)의 문법으로 설명했습니다.

* **리소스 관리**: 파일 시스템, 도구, LLM 접근
* **스케줄링**: Cron Job, 문제 분해, 서브 에이전트 호출
* **I/O**: 멀티모달 입출력 (음성, 제스처, 메시지, 이메일 등)

결론적으로, OpenClaw는 **Agentic Computer의 운영체제를 오픈소스화한 것**입니다. Windows가 PC 시대를 열었듯, OpenClaw는 Personal Agent 시대를 열었습니다.

모든 기업이 Linux 전략, HTTP/HTML 전략, Kubernetes 전략을 가져야 했듯이, 이제 모든 기업은 **OpenClaw 전략**이 필요합니다.

### 11.2 Enterprise IT의 변혁

기존 IT 산업은 데이터센터(파일 저장) → 소프트웨어(도구/워크플로우) → 사람(도구 사용)의 구조였습니다. Post-OpenClaw 시대에는 모든 SaaS 회사가 **AaaS(Agentic as a Service)** 회사가 됩니다.

하지만 Agentic 시스템은 기업 네트워크에서 민감한 정보에 접근하고, 코드를 실행하고, 외부와 통신할 수 있습니다. 이는 심각한 보안 위험을 의미합니다.

### 11.3 NVIDIA NemoClaw: Enterprise 보안

NVIDIA는 Peter Steinberger와 협력하여 OpenClaw를 Enterprise 환경에 적합하게 만든 **NemoClaw** 레퍼런스 디자인을 발표했습니다.

* **OpenShell**: 보안 및 프라이버시 계층. OpenClaw에 통합
* **네트워크 가드레일 + 프라이버시 라우터**: Agent의 행동 범위를 안전하게 제한
* **SaaS 회사의 Policy Engine 연결**: 기존 보안 정책을 NemoClaw에 연결 가능

---

12. NVIDIA Open Model Initiative
--------------------------------

NVIDIA는 모든 AI 도메인에서 Frontier 수준의 오픈 모델을 제공하고 있습니다. 6개의 오픈 Frontier 모델 패밀리와 학습 데이터/레시피/프레임워크를 공개합니다.

* **Nemotron**: 언어, 시각 이해, RAG, Safety, 음성을 위한 Reasoning 모델. Nemotron 3가 OpenClaw 내에서 세계 상위 3개 모델에 포함
* **Cosmos**: Physical AI를 위한 World Foundation Model
* **ALMA (Alphamo)**: 자율주행 AI
* **GR00T**: 범용 로봇을 위한 Foundation Model
* **BioNeMo**: 생물학, 화학, 분자 설계
* **Earth Models**: 날씨/기후 예측 (AI Physics 기반)

**Nemotron 3 Ultra**는 세계 최고의 Base Model로, 각 국가의 Sovereign AI 구축을 지원합니다.

### Nemotron 4 Coalition

Nemotron 4를 더 발전시키기 위한 연합체가 발표되었습니다. 참여 기업으로는 Black Forest Labs, Cursor, LangChain, Mistral, Perplexity, Reflection, Sarvam(인도), Thinking Machines, Urban Labs 등이 있습니다.

Jensen은 미래의 모든 엔지니어가 연봉 외에 **연간 Token 예산**을 받게 될 것이라고 전망했습니다. Token이 엔지니어의 생산성을 10배로 높일 수 있기 때문에, "이 직무에는 Token이 얼마나 포함되나요?"가 실리콘밸리의 새로운 채용 질문이 되고 있다고 덧붙였습니다.

---

13. Physical AI와 로보틱스
---------------------

키노트의 마지막 대주제는 Physical AI, 즉 물리 세계에서 작동하는 Embodied Agent(로봇)였습니다.

### 13.1 로보틱스 생태계

GTC에 110대의 로봇이 전시되었으며, NVIDIA는 로봇 개발을 위한 3대 컴퓨터를 제공합니다.

* **Training Computer**: 모델 훈련
* **Synthetic Data Generation & Simulation Computer**: 합성 데이터 생성 및 시뮬레이션
* **Robotics Computer**: 로봇 내부 탑재

파트너로는 Siemens, Cadence 등이 있으며, 새로운 파트너도 대거 발표되었습니다.

### 13.2 자율주행: ChatGPT Moment 도래

Jensen은 자율주행의 "ChatGPT Moment"가 도착했다고 선언했습니다.

* **새로운 Robo-Taxi 파트너**: BYD, Hyundai, Nissan, Geely (연간 1,800만 대 생산). 기존 파트너 Mercedes, Toyota, GM에 추가
* **Uber와의 대규모 파트너십**: 다수의 도시에서 Robo-Taxi를 Uber 네트워크에 연결
* **NVIDIA Alphamo**: 자율주행 AI 플랫폼. 차량에 Reasoning 능력을 부여하여, 상황을 설명하고 지시를 따르는 모습을 시연했습니다

### 13.3 산업용 로보틱스

ABB, Universal Robotics, KUKA 등의 로보틱스 기업들과 협력하여 Physical AI 모델을 시뮬레이션 시스템에 통합하고, 제조 라인에 배포합니다. Caterpillar, Foxconn 등도 참여합니다.

T-Mobile과는 기지국을 **AI RAN(Robotics Radio Tower)**로 전환하는 파트너십을 맺었습니다. AI가 트래픽을 분석하고 빔포밍을 동적 조정하여 에너지 절약과 품질 향상을 동시에 달성합니다.

### 13.4 Physical AI 소프트웨어 스택

현실 세계의 데이터만으로는 모든 시나리오를 커버할 수 없기 때문에, AI와 시뮬레이션으로 생성한 합성 데이터가 필수적입니다. "Compute is Data"라는 원칙 아래, NVIDIA는 다음 소프트웨어를 제공합니다.

* **Isaac Lab**: 로봇 훈련 및 평가 시뮬레이션 (오픈소스)
* **Newton**: GPU 가속 Differentiable Physics 시뮬레이션 (확장 가능)
* **Cosmos World Models**: Neural Simulation
* **GR00T**: 로봇 추론 및 행동 생성을 위한 Open Foundation Model

사례로는 Pitts AI(수술실 보조 로봇), Skild AI(RL 기반 모델 강화), Humanoid(전신 제어), Hexagon Robotics, Foxconn, Noble Machines 등이 소개되었습니다.

### 13.5 Disney + NVIDIA: Olaf 로봇 시연

키노트의 하이라이트 중 하나로, Disney Research가 Newton 물리 시뮬레이터와 Isaac Lab을 사용해 훈련한 **Olaf(올라프) 로봇**이 무대에 등장했습니다. NVIDIA Warp 위에서 동작하는 Newton Solver를 DeepMind와 공동 개발했으며, 이를 통해 올라프가 물리 세계에 적응하는 모습을 보여주었습니다.

Jensen은 미래의 디즈니랜드에서 이런 캐릭터 로봇들이 돌아다니는 모습을 상상해보라고 말했습니다.

---

14. 마무리: 4대 메가 트렌드
------------------

Jensen은 키노트를 4가지 핵심 주제로 요약했습니다.

1. **Inference Inflection**: AI의 핵심 워크로드가 Training에서 Inference로 전환. 컴퓨팅 수요 100만 배 증가. \$1T+ 인프라 수요
2. **AI Factory**: 데이터센터에서 Token Factory로의 전환. Tokens/Watt가 핵심 KPI. NVIDIA DGX 플랫폼으로 설계-건설-운영 최적화
3. **OpenClaw Agent Revolution**: Agentic AI의 오픈소스 OS. 모든 기업의 IT가 Agentic as a Service로 전환. NemoClaw로 Enterprise 보안 확보
4. **Physical AI & Robotics**: 자율주행의 ChatGPT Moment. 합성 데이터 + 시뮬레이션으로 Physical AI 데이터 문제 해결. Isaac Lab, Newton, Cosmos, GR00T 소프트웨어 스택

---

이번 GTC 2026은 NVIDIA가 단순한 GPU 회사가 아니라, AI 시대의 풀스택 플랫폼 회사로 완전히 진화했음을 보여주는 행사였습니다. Vertically Integrated, Horizontally Open이라는 전략 아래, 칩-시스템-소프트웨어-AI 모델-생태계를 아우르는 NVIDIA의 포지셔닝은 향후 AI 산업의 방향을 이해하는 데 핵심적인 프레임워크가 될 것입니다.

읽어주셔서 감사합니다 :)