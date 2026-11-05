---
type: "Repo Review"
title: "[Repo Review] OpenLIT: SDK·코딩 에이전트의 실행을 관측·평가·가드로 연결하는 구조"
description: "OpenLIT의 Python 계측, Go OTLP 수신·ClickHouse 조회, 코딩 에이전트 훅과 평가·가드레일 흐름을 고정 커밋의 코드로 추적합니다."
date: "2026-11-06"
tags:
  - "Repo Review"
  - "AI Agent"
  - "Tools"
  - "Python"
resource: "https://github.com/openlit/openlit/tree/ec2639f8c2ffa10f8c42f9758e358c122f13976a"
generated:
  by: "process:blog-review"
  at: "2026-11-06T06:06:52+09:00"
sources:
  - id: "openlit/openlit"
    resource: "https://github.com/openlit/openlit/tree/ec2639f8c2ffa10f8c42f9758e358c122f13976a"
    title: "OpenLIT: the open-source agent harness engineering platform"
status: "stable"
year: "2026"
analyzed_at: "2026-11-06T06:06:52+09:00"
source_id: "openlit/openlit"
source_revision: "ec2639f8c2ffa10f8c42f9758e358c122f13976a"
source_type: "repo"
source_url: "https://github.com/openlit/openlit/tree/ec2639f8c2ffa10f8c42f9758e358c122f13976a"
visual_sources:
  - path: "/img/reviews/2026/openlit-repo-review/architecture.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/otlp-receiver/internal/ingest/service.go#L44-L57"
    caption: "리뷰어 작성, 분석 커밋 기준. OTLP 저장·조회와 조건부 NATS engine 분기."
    evidence_urls:
      - "https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/otlp-receiver/internal/realtime/fanout.go#L38-L81"
      - "https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/client/src/lib/platform/traces/read.ts#L408-L429"
      - "https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/engine/internal/api/client.go#L23-L27"
  - path: "/img/reviews/2026/openlit-repo-review/coding-flow.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/cli/internal/coding/hook/codex/handle.go#L90-L223"
    caption: "리뷰어 작성, 분석 커밋 기준. Codex 훅·세션 상태에서 결정적 trace 문맥과 OTLP span으로 이어지는 경로."
    evidence_urls:
      - "https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/cli/internal/coding/hook/hook.go#L278-L423"
      - "https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/cli/internal/otlp/tracecontext.go#L104-L146"
      - "https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/cli/internal/otlp/exporter.go#L825-L873"
---

## 들어가며

에이전트가 어떤 답을 냈는지와 그 답에 도달하며 어떤 도구·문맥·모델을 사용했는지는 서로 다른 정보입니다. OpenLIT은 이 실행 주변부를 관측하고 평가하는 도구를 한 저장소에 모읍니다. README는 이를 **agent harness engineering platform**이라고 부릅니다. 여기서 하네스(harness)는 모델을 둘러싼 도구, 프롬프트, 문맥, 메모리, 훅과 피드백 구조를 뜻하며, 프로젝트는 관측→평가→수정→재확인의 순환을 제시합니다. [README의 정의](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/README.md#L32-L47)

이 리뷰는 **openlit/openlit의 `ec2639f8c2ffa10f8c42f9758e358c122f13976a` 커밋**을 대상으로 합니다. README·매니페스트·배포 설정·핵심 코드를 정적으로 읽었습니다. 의존성 설치, 대상 코드 실행, Docker 기동, 테스트와 성능 측정은 하지 않았습니다. README의 “70+ integrations”, “5 minutes”, “any model, framework, or harness”는 프로젝트의 소개 문구이며, 이 글이 모든 연동의 호환성이나 실행 성공을 확인했다는 뜻은 아닙니다. 상세 추적 범위는 Python 초기화와 OpenAI 동기 Chat Completions, Go 수신기와 ClickHouse 조회, CLI의 Codex 훅, 서버 오프라인 평가와 SDK 가드 파이프라인입니다. [분석 트리](https://github.com/openlit/openlit/tree/ec2639f8c2ffa10f8c42f9758e358c122f13976a), [README의 범위 주장](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/README.md#L34-L38)

## 무엇을 제공하는 저장소인가

OpenLIT은 애플리케이션과 코딩 에이전트의 실행을 OpenTelemetry 형식으로 수집하고, 저장된 실행과 설정을 이용해 조회·평가·가드레일을 제공하는 모노레포입니다. OpenTelemetry는 실행 기록인 **trace**, 그 안의 개별 작업인 **span**, 수치 지표인 **metric**, 로그 등의 공통 관측 규약이고, **OTLP**는 이를 전달하는 프로토콜입니다. 코드에서도 Python SDK는 OTel API·SDK·OTLP exporter에 의존하고, CLI는 공통 Go SDK를 사용합니다. 웹 애플리케이션은 Next.js와 ClickHouse 클라이언트를 별도 의존성으로 둡니다. [Python 매니페스트](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/sdk/python/pyproject.toml#L16-L29), [CLI 매니페스트](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/cli/go.mod#L1-L13), [웹 매니페스트](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/client/package.json#L1-L39)

README의 기능표에는 관측, 평가, 가드레일, Prompt Hub, Context, Rule Engine, Vault, OpenGround, 비용·GPU 모니터링이 함께 나옵니다. 하지만 이 목록이 하나의 자동 실행 경로를 뜻하지는 않습니다. SDK의 provider 래핑, 수신기의 데이터 저장, 서버 평가, 런타임 가드는 서로 다른 진입점에서 작동합니다. 아래에서는 실제 호출 연결이 확인된 경로를 중심으로 읽겠습니다. [기능표](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/README.md#L40-L47), [SDK 초기화](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/sdk/python/src/openlit/__init__.py#L360-L450), [오프라인 평가 API](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/client/src/app/api/evaluation/offline/route.ts#L12-L102)

## 아키텍처: 수집·저장과 읽기를 나눠 보기

| 경로 | 책임과 이번에 확인한 입출력 |
| --- | --- |
| `sdk/python/src/openlit/` | `init()` 설정 → 설치된 라이브러리의 instrumentor → span·metric·inference event |
| `cli/`와 `sdk/go/` | 에이전트 훅 JSON → 업체별 정규화 → 세션에 연결된 OTLP span |
| `src/otlp-receiver/` | HTTP/gRPC OTLP → 자격 증명에 따른 저장소 결정 → `otel_*` 테이블 |
| `src/client/` | 사용자·DB 접근 문맥과 필터 → 데이터 소스 adapter → 조회 JSON과 화면 |
| `src/engine/` | NATS 신호와 서버 규칙 → 실시간 finding → 서버 내부 API |
| `assets/otel-collector-config.yaml` | 선택적으로 배치하는 외부 Collector → OpenLIT OTLP endpoint로 전달 |

각 행의 근거는 [Python 진입점](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/sdk/python/src/openlit/__init__.py#L360-L441), [CLI emitter](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/cli/internal/otlp/exporter.go#L483-L527), [수신기 main](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/otlp-receiver/cmd/otlp-receiver/main.go#L25-L89), [trace 조회 facade](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/client/src/lib/platform/traces/read.ts#L408-L474), [engine main](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/engine/cmd/openlit-engine/main.go#L35-L90), [선택적 Collector 설정](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/assets/otel-collector-config.yaml#L1-L27)입니다.

이 커밋의 기본 Compose에는 `clickhouse`, `nats`, `openlit` 세 서비스가 있습니다. `openlit` 컨테이너의 entrypoint가 Go OTLP 수신기, 조건부 realtime engine, Node 웹 서버를 자식 프로세스로 시작합니다. 별도 Collector 서비스가 기본 수집을 담당한다고 읽으면 현재 구조를 놓칩니다. `assets/otel-collector-config.yaml`도 “optional sidecar”라고 명시하며, traces·metrics·logs를 ClickHouse에 직접 넣는 대신 OpenLIT으로 전달합니다. [Compose](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/docker-compose.yml#L1-L109), [프로세스 시작과 종료 감시](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/client/scripts/entrypoint.sh#L161-L211)

![Python SDK와 CLI에서 들어온 OTLP가 수신기와 ClickHouse를 거쳐 조회되고, 조건을 만족한 신호는 NATS와 engine으로 분기하는 구조]({{ '/img/reviews/2026/openlit-repo-review/architecture.svg' | relative_url }})

*리뷰어 작성, 분석 커밋 기준. 실선은 저장·조회 경로이며, 오른쪽 분기는 NATS 설정과 scoped GenAI 조건을 만족할 때만 연결됩니다. [저장 후 fan-out](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/otlp-receiver/internal/ingest/service.go#L44-L57), [분기 조건](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/otlp-receiver/internal/realtime/fanout.go#L38-L81), [조회 경계](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/client/src/lib/platform/traces/read.ts#L408-L429), [engine의 서버 통신](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/engine/internal/api/client.go#L23-L27).*

## Python SDK: `openlit.init()`에서 실제 호출까지

### 1. 초기화는 exporter와 instrumentor를 구성합니다

`init()`는 서비스 이름과 환경, endpoint·header, 메시지 수집과 metric 옵션을 받아 tracing, event logging, meter를 준비합니다. metric 설정이 실패하면 로그를 남기고 `disable_metrics=True`로 바꿔 초기화를 계속합니다. 가격 정보를 읽어 싱글턴 `OpenlitConfig`에 보관한 뒤 instrumentor들을 순회합니다. 따라서 초기화 호출이 반환했다는 사실만으로 모든 수집 경로가 정상이라는 결론을 내릴 수는 없습니다. instrumentor별 실패와 바깥 초기화 예외도 로그로 처리합니다. [설정과 오류 처리](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/sdk/python/src/openlit/__init__.py#L360-L441), [초기화 마지막 예외 처리](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/sdk/python/src/openlit/__init__.py#L480-L488)

다음은 instrumentor를 순회하는 실제 코드입니다. 앞선 설정 처리와 뒤의 가드·GPU 설정은 생략했습니다. [출처: `__init__.py` 436–441행](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/sdk/python/src/openlit/__init__.py#L436-L441)

```python
        # Create instrumentor instances dynamically
        instrumentor_instances = get_all_instrumentors()

        # Initialize and instrument only the enabled instrumentors
        for name, instrumentor in instrumentor_instances.items():
            instrument_if_available(name, instrumentor, config, disabled_instrumentors)
```

`get_all_instrumentors()`는 레지스트리에서 클래스를 동적으로 가져와 인스턴스를 만듭니다. 이후 `instrument_if_available()`가 비활성 목록을 확인하고, 대응 라이브러리가 있는지 검사합니다. 공식 OTel instrumentor에는 일반 `instrument()`를 호출하고, OpenLIT instrumentor에는 가격·메시지·metric 설정 등을 넘깁니다. “자동 계측”은 모든 코드를 의미적으로 이해한다는 뜻이 아니라 **레지스트리에 등록된 함수와 라이브러리를 감싸는 방식**입니다. [instrumentor 레지스트리와 로딩](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/sdk/python/src/openlit/_instrumentors.py#L224-L262), [조건부 활성화](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/sdk/python/src/openlit/__init__.py#L127-L164)

tracing은 기존 OTel `TracerProvider`가 있으면 재사용합니다. 새 provider를 만드는 경우 서비스·환경 resource를 등록하고, endpoint가 지정되어 있으면 OTLP exporter를, 별도 exporter 설정과 endpoint가 없으면 console exporter를 선택합니다. 기본 OTLP 처리는 batch이고 `disable_batch=True`일 때 simple processor를 고릅니다. HTTP/gRPC exporter 선택은 모듈을 가져올 때 `OTEL_EXPORTER_OTLP_PROTOCOL == "grpc"`인지로 정해집니다. 기존 provider 재사용 경로에서는 새 exporter를 추가하는 블록에 들어가지 않으므로 기존 관측 설정도 함께 읽어야 합니다. [tracing 전체 분기](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/sdk/python/src/openlit/otel/tracing.py#L23-L141)

metric도 기존 `MeterProvider`를 재사용하거나 새 provider와 주기적 exporter를 만듭니다. 이후 token usage와 duration 등을 기록할 metric 객체를 구성합니다. 따라서 span과 metric은 같은 요청에서 유도될 수 있지만 exporter와 수명 주기는 따로 있습니다. [meter 설정](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/sdk/python/src/openlit/otel/metrics.py#L144-L240)

### 2. OpenAI Chat Completions는 원래 API를 감싼 뒤 응답을 해석합니다

OpenAI instrumentor는 `Completions.create`와 `AsyncCompletions.create` 등에 `wrapt` 래퍼를 등록합니다. 이 글에서 자세히 읽은 것은 동기 `Completions.create` 경로입니다. wrapper는 framework LLM 호출이 이미 활성 상태이면 원래 함수를 바로 호출해 중복 계측을 피하고, 그렇지 않으면 모델 이름으로 span을 만듭니다. [메서드 래핑](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/sdk/python/src/openlit/instrumentation/openai/__init__.py#L153-L205), [동기 wrapper 분기](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/sdk/python/src/openlit/instrumentation/openai/openai.py#L135-L200)

비스트리밍에서는 원래 API를 호출한 뒤 `process_chat_response()`가 응답의 모델·메시지·usage·캐시 token 등을 scope에 모으고 `common_chat_logic()`로 넘깁니다. 공통 처리는 token 수와 가격표로 비용을 계산하고, span 속성·메시지·inference event·metric을 기록합니다. 입력 token 값이 없거나 거짓으로 평가되면 `general_tokens()`를 이용하는 대체 경로가 있습니다. 따라서 화면의 token·비용을 공급자의 청구서와 동일한 확정 수치로 일반화하면 안 됩니다. [응답 정리](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/sdk/python/src/openlit/instrumentation/openai/utils.py#L1763-L1859), [token·비용 분기](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/sdk/python/src/openlit/instrumentation/openai/utils.py#L1416-L1436), [metric 기록](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/sdk/python/src/openlit/instrumentation/openai/utils.py#L1702-L1731)

스트리밍에서는 `TracedSyncStream`이 원본 iterator를 감싸 chunk를 넘겨주면서 상태를 누적합니다. `StopIteration` 또는 `close()`에서 한 번만 최종 처리를 수행합니다. 최초 API 호출 자체가 실패하면 예외를 span에 기록하고 다시 발생시키며, 응답 후 관측 처리에서 발생한 오류는 기록한 뒤 원래 응답을 반환하는 분기가 있습니다. 이 차이는 애플리케이션 오류와 관측 처리 오류를 분리하려는 설계로 읽을 수 있습니다. 모든 공급자·스트림 소비 방식에 동일한 동작을 보장하는지는 실행 검증 범위 밖입니다. [stream wrapper](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/sdk/python/src/openlit/instrumentation/openai/openai.py#L49-L133), [API 예외](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/sdk/python/src/openlit/instrumentation/openai/openai.py#L164-L172), [응답 후 오류 처리](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/sdk/python/src/openlit/instrumentation/openai/openai.py#L225-L271)

### 3. 메시지 수집, 시스템 지표, 문맥은 서로 다른 설정입니다

`init()`의 **`capture_message_content` 기본값은 `True`**입니다. 반면 `collect_gpu_stats`, `collect_system_metrics`, `capture_db_parameters`는 기본 `False`입니다. 메시지 본문 수집까지 모두 opt-in이라고 설명하면 이 커밋의 기본 동작과 맞지 않습니다. `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=false`는 본문 수집을 끄는 별도 경로이며, OpenAI 공통 처리에서는 본문 수집이 꺼져도 inference event의 token·종료 이유 등 메타데이터를 기록하는 경로가 남습니다. [기본 인자](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/sdk/python/src/openlit/__init__.py#L185-L209), [환경 변수 처리](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/sdk/python/src/openlit/__init__.py#L410-L434), [메시지와 event 분기](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/sdk/python/src/openlit/instrumentation/openai/utils.py#L1618-L1698)

`agent_context(name)`와 `agent_version_context(version)`는 호출 범위에 에이전트 이름·버전을 설정하고 `finally`에서 이전 값을 복원합니다. 기반 구현은 `ContextVar`이며, 전역 사용자 속성과 범위 내 속성은 span 적용 시 합쳐집니다. 여기의 “문맥”은 관측 레이블의 전파를 뜻합니다. 서버의 Context 관리 기능이나 LLM 대화 메모리와 같은 것으로 혼동하지 않아야 합니다. [범위 진입과 복원](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/sdk/python/src/openlit/__init__.py#L834-L873), [ContextVar 선언](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/sdk/python/src/openlit/__helpers.py#L79-L83), [문맥 저장·속성 적용](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/sdk/python/src/openlit/__helpers.py#L1120-L1193)

또 하나의 실행 시점 경계가 있습니다. `init()`는 가격표를 초기화 중 읽는데, `pricing_json`이 없으면 GitHub `main/assets/pricing.json`으로 HTTP GET을 시도합니다. 코드의 실제 timeout 인자는 20초이며 실패 시 빈 dict를 반환합니다. 로컬 파일을 지정하면 그 파일을 읽는 분기가 있습니다. 관측 데이터 OTLP 전송과 별개인 네트워크 요청이므로, 재현 가능한 가격 해석이나 외부 통신 정책을 정할 때 고려해야 합니다. 이번 리뷰에서는 이 요청을 실행하지 않았습니다. [가격표 입력과 원격 기본값](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/sdk/python/src/openlit/__helpers.py#L518-L553)

## 수신기: OTLP를 어느 저장소에 어떤 행으로 넣는가

### 1. HTTP 디코딩과 tenant 결정

HTTP 수신기는 `/v1/traces`, `/v1/logs`, `/v1/metrics`에 POST handler를 붙이고 JSON 또는 protobuf를 해석합니다. gzip도 처리하며, 압축을 푼 입력의 읽기 상한은 32 MiB입니다. 디코딩 오류는 400, 과대 입력은 413으로 처리합니다. gRPC 수신기 역시 같은 ingest service에 연결되지만, 여기서 HTTP의 크기 제한을 gRPC 전체의 제한으로 일반화하지는 않겠습니다. [HTTP 엔드포인트](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/otlp-receiver/internal/httpserver/server.go#L23-L56), [크기·디코딩·응답 경계](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/otlp-receiver/internal/httpserver/server.go#L85-L164), [두 서버 연결](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/otlp-receiver/cmd/otlp-receiver/main.go#L84-L89)

자격 증명은 `Authorization: Bearer ...` 또는 `x-openlit-api-key`에서 가져옵니다. tenant store는 API key와 연결된 SQLite의 `DatabaseConfig`를 조회해 ClickHouse 접속 정보와 조직·프로젝트·환경을 결정합니다. 키에 저장된 프로젝트·조직과 DB 설정이 충돌하면 거부하는 경로도 있습니다. 이 단계는 사용자가 payload에 붙인 임의 tenant 속성을 그대로 신뢰하는 방식과 구분됩니다. [header 정규화](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/otlp-receiver/internal/tenant/tenant.go#L103-L125), [설정 조회](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/otlp-receiver/internal/tenant/tenant.go#L251-L286), [불일치 거부](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/otlp-receiver/internal/tenant/tenant.go#L322-L341)

다만 **수신 API key 필수 설정의 기본값은 `False`**입니다. 키가 없으면 `OTLP_REQUIRE_API_KEY`를 확인하고, 필수가 아니면서 `INIT_DB_*`가 있으면 초기 DB로 보냅니다. 키 없는 입력도 항상 거부된다고 가정하면 안 됩니다. 실패한 키를 반복해서 보내는 클라이언트에 대한 limiter와 401·429·503 응답 분기는 별도로 있습니다. [수신기 기본 설정](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/otlp-receiver/internal/config/config.go#L58-L69), [키 없는 fallback](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/otlp-receiver/internal/tenant/tenant.go#L143-L176), [서비스 오류 매핑](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/otlp-receiver/internal/ingest/service.go#L32-L41), [응답 상태](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/otlp-receiver/internal/ingest/service.go#L92-L103)

### 2. 변환, tenant stamp, ClickHouse insert 순서

trace 입력의 핵심은 다음과 같습니다. 아래는 `Traces()`에서 인증 뒤 행 변환·저장·분기를 수행하는 부분이며, 함수 시작과 끝은 생략했습니다. [출처: `service.go` 49–56행](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/otlp-receiver/internal/ingest/service.go#L49-L56)

```go
	rows := otlpconv.Traces(&tracepb.TracesData{ResourceSpans: req.GetResourceSpans()})
	otlpconv.StampTraces(rows, resolved.Resource())
	if err := s.Writer.InsertTraces(ctx, resolved.ClickHouse, rows); err != nil {
		return err
	}
	if s.Fanout != nil {
		s.Fanout.PublishTraces(resolved, rows)
	}
```

`otlpconv.Traces()`는 ResourceSpans→ScopeSpans→Spans를 순회해 trace/span/parent ID, 서비스명, 속성, duration, event와 link를 행으로 펼칩니다. `StampResource()`는 입력에 있던 tenant 전용 키를 먼저 제거하고 서버에서 결정한 조직·프로젝트·환경만 다시 넣습니다. 키 없는 fallback은 임의 조직을 만들어 넣지 않습니다. [행 변환](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/otlp-receiver/internal/otlpconv/convert.go#L283-L355), [tenant stamp](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/otlp-receiver/internal/otlpconv/convert.go#L602-L628)

writer는 tenant의 ClickHouse 접속 정보로 connection을 선택하고, schema를 준비한 뒤 `otel_traces` batch를 만들어 전송합니다. 테이블 부재 오류이면 schema 캐시를 지우고 준비·쓰기 과정을 한 번 더 시도하는 경로가 있습니다. traces 외에 logs와 gauge·sum·histogram·summary·exponential histogram의 metric 저장 경로도 분리되어 있습니다. 이것은 변환과 insert 책임을 코드로 확인한 것이며, 실제 처리량이나 장애 후 무손실 복구를 측정한 결과는 아닙니다. [connection·schema 경계](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/otlp-receiver/internal/chwrite/writer.go#L47-L107), [trace batch](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/otlp-receiver/internal/chwrite/writer.go#L109-L151), [log·metric service](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/otlp-receiver/internal/ingest/service.go#L60-L89)

### 3. 저장 성공과 실시간 알림 성공은 다릅니다

NATS가 설정된 경우에도 모든 입력을 engine으로 보내지는 않습니다. 먼저 ClickHouse insert가 성공해야 하고, 조직·프로젝트·환경이 있는 **scoped tenant**이면서 GenAI 신호로 분류되어야 합니다. 조건에 맞은 행은 compact signal로 변환되어 tenant별 subject로 전달됩니다. publisher는 queue가 가득 차면 기다리지 않고 drop을 계수하므로, trace 저장 성공과 실시간 신호 전달 성공은 별도 상태입니다. [저장 후 호출](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/otlp-receiver/internal/ingest/service.go#L44-L57), [fan-out 필터](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/otlp-receiver/internal/realtime/fanout.go#L38-L81), [비차단 queue](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/otlp-receiver/internal/natsx/publisher.go#L191-L210)

engine은 NATS 신호를 읽고 서버에서 활성 규칙을 주기적으로 가져와 `Observe()`에 적용합니다. 규칙·조직·프로젝트·환경·그룹 값별 상태를 관리하며, 발생한 finding은 `X-OpenLIT-Engine-Secret`을 사용하는 내부 API로 보냅니다. 이 경로는 Python의 호출 전 차단 가드와 다릅니다. 이미 수집된 실행 신호를 규칙에 대조하는 후속 처리입니다. [신호 소비와 규칙 갱신](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/engine/cmd/openlit-engine/main.go#L35-L90), [규칙 fetch](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/engine/cmd/openlit-engine/main.go#L156-L182), [상태와 Observe](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/engine/internal/engine/engine.go#L190-L230), [내부 API 전달](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/engine/internal/api/client.go#L23-L27), [finding queue와 전송](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/engine/internal/api/client.go#L85-L156)

## 조회: 저장한 span이 대시보드 행이 되는 과정

화면의 signal registry는 Traces 목록에 `/api/telemetry/trace?view=traces`, Spans 목록에 `/api/telemetry/trace`를 사용합니다. route는 시간 범위·limit·offset·필터·정렬·데이터 소스·환경을 받고, 요청을 검증한 뒤 trace 요약 또는 span 목록 facade를 호출합니다. [화면 registry](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/client/src/components/%28playground%29/observability/registry.tsx#L80-L125), [route 입력과 응답](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/client/src/app/api/telemetry/trace/route.ts#L14-L75)

span 목록의 facade는 선택된 signal adapter를 구하고 `listSpans()`와 count를 호출합니다. ClickHouse adapter는 `getRequests()`로 이어져 시간·필터 조건을 붙인 count와 `SELECT *` 쿼리를 만들고, `queryTracesSql()`→`queryConnectorTraces()`→`connectorDataCollector()`를 통해 직접 ClickHouse read로 보냅니다. 결과는 normalized span으로 바뀐 뒤 기존 화면용 행 구조로 다시 변환됩니다. 이 경로는 모든 제품 조회가 OpenPlait을 거친다는 주석만 보고 읽으면 놓치기 쉽습니다. `common.ts`에는 일반 `dataCollector`의 OpenPlait 경로와 connector용 direct 경로가 명시적으로 나뉩니다. [목록 facade](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/client/src/lib/platform/traces/read.ts#L408-L474), [ClickHouse adapter](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/client/src/lib/platform/connectors/datasource/clickhouse/adapter.ts#L224-L263), [실제 목록 SQL](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/client/src/lib/platform/request/index.ts#L238-L276), [direct-read 연결](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/client/src/lib/platform/connectors/datasource/clickhouse/direct-read.ts#L16-L22), [두 read 경로](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/client/src/lib/platform/common.ts#L194-L228)

상세 trace는 같은 Trace ID의 span들을 시간순으로 읽습니다. 이 커밋의 ClickHouse `getTraceSpans()`에는 `LIMIT 5000`이 있어, 매우 큰 trace의 전체 span이 항상 한 번에 반환된다고 말할 수 없습니다. 목록의 total도 count 결과와 adapter의 truncated 메타데이터에 따라 `sampled` 또는 `live` 표시가 달라집니다. [상세 쿼리 상한](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/client/src/lib/platform/connectors/datasource/clickhouse/adapter.ts#L254-L263), [목록 total·freshness](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/client/src/lib/platform/traces/read.ts#L449-L474)

접근 제어도 함수 이름보다 구현을 확인해야 합니다. 이 route는 `withRouteAccess("traces.read", ..., {requireDbConfig: true})`로 감싸지만, 해당 wrapper는 권한 문자열 자체를 검사하지 않고 `withDbConfigAccess()`에 위임합니다. 그 안에서는 검증된 API key의 DB binding을 확인하거나 현재 사용자·프로젝트·명시 DB 설정의 접근을 검사합니다. 이를 근거로 DB 접근 경계를 설명할 수는 있지만, `traces.read`라는 이름만으로 세부 역할 권한까지 강제한다고 결론 내릴 수는 없습니다. [route wrapper](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/client/src/lib/access/route-access.ts#L10-L23), [DB 접근 wrapper](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/client/src/lib/rbac/route.ts#L52-L100)

## 코딩 에이전트 CLI: 서로 다른 프로세스를 한 세션으로 묶기

### 1. 설치는 에이전트가 훅을 찾게 만드는 작업입니다

Go CLI의 실제 최상위 명령 등록은 `coding`, `configure`, `doctor`, `version`입니다. 주석에 있는 prompts·traces·eval 명령은 이 진입점에서 등록되지 않았습니다. `coding install --vendor=all`도 이 커밋에서는 Claude Code, Cursor, Codex, OpenCode 네 대상으로 확장됩니다. README 제목에 Windsurf가 보인다는 이유로 같은 설치 경로가 있다고 가정해서는 안 됩니다. [등록된 명령](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/cli/cmd/openlit/main.go#L79-L97), [vendor 확장](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/cli/internal/coding/install/install.go#L102-L117), [README 표제](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/README.md#L139-L143)

install 코드는 바이너리에 embed된 manifest를 사용자 디렉터리에 쓰고, 필요하면 각 업체 CLI로 플러그인을 등록합니다. Cursor는 `~/.cursor/hooks.json` 병합, OpenCode는 별도 plugin 설치 분기로 나뉩니다. Codex용 manifest에는 SessionStart·UserPromptSubmit·PreToolUse·PostToolUse·Stop마다 `openlit coding hook`을 호출하는 명령이 있습니다. 이는 SDK가 provider 함수를 감싸는 방식과 달리, 호스트 에이전트가 전달하는 훅 입력과 transcript를 이용하는 방식입니다. [설치 writer](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/cli/internal/coding/install/install_vendors.go#L49-L117), [Codex manifest](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/cli/internal/coding/install/marketplace/plugins/codex/plugins/openlit/hooks/hooks.json#L1-L62)

설정 우선순위는 CLI flag→`OPENLIT_*` 환경 변수→표준 OTel 환경 변수→허용 목록 기반 `config.env`→기본값입니다. 이 CLI의 endpoint 기본값은 `http://127.0.0.1:4318`이며 **content capture 기본값은 `full`**입니다. Python SDK에서 endpoint 미설정 시 console 경로로 가는 기본과도 다릅니다. [설정 계약과 기본값](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/cli/internal/config/config.go#L1-L11), [기본값](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/cli/internal/config/config.go#L82-L110), [환경 변수 해결 순서](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/cli/internal/config/config.go#L160-L228), [flag와 기본값 적용](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/cli/internal/config/config.go#L231-L259)

![Codex 훅 JSON과 세션 캐시가 업체 adapter에서 합쳐지고, 세션 ID를 공유하는 span이 OTLP로 나가는 흐름]({{ '/img/reviews/2026/openlit-repo-review/coding-flow.svg' | relative_url }})

*리뷰어 작성, 분석 커밋 기준. Codex를 대표 경로로 그렸으며 다른 업체 adapter의 세부 동작까지 동일하다는 뜻은 아닙니다. [훅 실행](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/cli/internal/coding/hook/hook.go#L278-L423), [Codex event 분기](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/cli/internal/coding/hook/codex/handle.go#L90-L223), [ID 유도와 부모 문맥](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/cli/internal/otlp/tracecontext.go#L104-L146), [OTLP emitter](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/cli/internal/otlp/exporter.go#L483-L527).*

### 2. Codex의 입력 조각을 turn 단위로 재구성합니다

공통 hook handler는 stdin JSON을 읽고 vendor를 정규화하며 사용자·작업 폴더·저장소 등의 세션 상태를 복원합니다. 설정을 읽어 emitter를 만든 다음 adapter에 payload·event·capture 모드를 넘깁니다. 각 invocation이 별도 프로세스이므로 직전 상태를 함수 메모리에만 둘 수 없습니다. sessionstate는 운영체제 캐시 디렉터리 아래 `(session ID, vendor)`별 JSON 파일을 사용하고, 임시 파일→rename으로 저장합니다. [공통 handler](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/cli/internal/coding/hook/hook.go#L185-L205), [emitter와 adapter 호출](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/cli/internal/coding/hook/hook.go#L278-L423), [캐시 경로와 읽기](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/cli/internal/coding/sessionstate/sessionstate.go#L335-L400), [저장](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/cli/internal/coding/sessionstate/sessionstate.go#L555-L585)

Codex adapter에서는 UserPromptSubmit에서 프롬프트와 시작 시각을 turn fragment에 모읍니다. PreToolUse는 요청 event를, PostToolUse는 실제 tool-call span을 만들고 tool 기록을 fragment에 추가합니다. Stop에서는 fragment와 transcript의 usage를 이용하는 turn 처리로 이어지고 `coding_agent.llm.turn`을 내보내는 경로를 탑니다. 즉 훅 한 번이 곧 LLM 요청 한 번이라고 단순 대응하지 않으며, 이벤트 조각을 재구성하는 계층이 있습니다. full 모드일 때만 prompt·tool body를 fragment에 넣는 조건도 보입니다. [Codex 전반부](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/cli/internal/coding/hook/codex/handle.go#L90-L185), [Stop 분기](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/cli/internal/coding/hook/codex/handle.go#L187-L223), [turn 재구성과 전송](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/cli/internal/coding/hook/codex/handle.go#L388-L509)

프로세스 사이 trace 연결은 별도의 기법으로 해결합니다. `session ID + vendor`를 HMAC-SHA256으로 처리해 고정 Trace ID를 만들고, `|root`를 더한 값으로 session-root Span ID를 만듭니다. 자식 span은 이 root를 부모 문맥으로 사용합니다. `OPENLIT_TRACEID_SALT`가 없으면 빈 키를 사용하는 분기이므로, 결정적 ID를 사용한다는 사실 자체가 세션 정보의 비밀성을 보장하는 것은 아닙니다. [salt 기본 처리](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/cli/internal/otlp/tracecontext.go#L58-L76), [ID와 부모 문맥 구현](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/cli/internal/otlp/tracecontext.go#L104-L146)

여기서 `EmitEvent()`라는 이름도 주의해서 읽을 필요가 있습니다. 구현은 session-root에 `AddEvent()`를 붙이는 대신 **짧은 자식 span**을 새로 시작해 끝냅니다. 이미 종료된 다른 프로세스의 root span을 다시 열어 수정할 수 없기 때문입니다. 이 구조 덕분에 개별 훅 기록이 Trace ID와 ParentSpan ID로 연결되는 타임라인을 구성할 수 있습니다. 실제 전송은 CLI가 호출한 Go SDK의 `newTracerProvider()`에서 `otlptracehttp` exporter를 만들고 batch processor에 연결하는 경로입니다. CLI는 이 초기화에서 가격표 fetch를 끄고, capture를 업체 adapter가 관리하도록 Go SDK의 자동 본문 수집도 끕니다. [Go OTLP/HTTP 구성](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/sdk/go/openlit.go#L210-L253), [CLI 초기화 옵션](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/cli/internal/otlp/exporter.go#L483-L519). [설계 주석과 실제 EmitEvent](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/cli/internal/otlp/exporter.go#L825-L873)

### 3. 개발 흐름을 우선하는 실패 처리의 대가

hook handler에는 5초 context와 종료 시 별도 3초 flush context가 있고, 주요 관측 오류를 로그에 남기고 `nil`을 반환하며 panic도 복구합니다. 다만 context deadline이 동기 `io.ReadAll(stdin)`이나 모든 하위 작업을 강제로 중단하는 별도 프로세스 타이머인 것은 아니므로, 이를 엄밀한 전체 wall-clock 상한으로 읽지는 않았습니다. emitter 파일은 디스크 기반 retry queue가 없다는 제한도 명시합니다. 종료 코드 0과 데이터 저장 성공은 별도이며, 훅 수집의 누락 가능성을 고려해 화면을 해석해야 합니다. [timeout과 stdin 읽기](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/cli/internal/coding/hook/hook.go#L41-L108), [flush와 실패 반환](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/cli/internal/coding/hook/hook.go#L362-L423), [retry queue 제한 주석](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/cli/internal/otlp/exporter.go#L12-L17)

`minimal`, `metadata_only`, `full`은 본문과 개별 span의 양을 다르게 정합니다. 예를 들어 `EmitToolCall()`은 minimal에서 개별 span 대신 counter만 누적합니다. 문자열 redaction은 알려진 비밀 패턴의 정규식 치환이며 full에서는 추가 휴리스틱을 적용합니다. 이것을 모든 민감 정보의 제거 보장으로 바꿔 설명할 근거는 없습니다. 또한 `OPENLIT_DEBUG_PAYLOAD_DIR`가 설정되면 **원시 stdin payload가 adapter와 전송 전 redaction보다 앞서 로컬 파일에 기록**됩니다. 파일 권한을 제한하는 코드가 있어도 수집 모드와 별도로 관리해야 하는 경계입니다. [tool span과 counter 분기](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/cli/internal/otlp/exporter.go#L692-L718), [redaction 구현](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/cli/internal/redact/redact.go#L114-L154), [원시 debug 기록 시점](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/cli/internal/coding/hook/hook.go#L102-L120), [debug 파일 쓰기](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/cli/internal/coding/hook/hook.go#L546-L570)

## 평가와 가드레일: 실행 후 점수와 호출 전후 제어

### 서버 오프라인 평가는 별도의 API 호출입니다

`openlit.eval()` 계열의 단건 오프라인 경로는 prompt·response·선택적 contexts·평가 종류·threshold 등을 JSON으로 만들어 `/api/evaluation/offline`에 Bearer key와 함께 보냅니다. “offline”은 저장 trace와 독립된 입력 평가라는 API 의미로 읽어야 하며, 네트워크 없이 로컬에서만 실행한다는 뜻은 아닙니다. SDK는 401을 실패 결과로 돌려주고 429·5xx·연결 오류는 일부 한 번 재시도합니다. timeout이면 서버 평가가 여전히 진행 중일 수 있다는 실패 메시지를 반환합니다. [SDK HTTP 경로](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/sdk/python/src/openlit/evals/offline.py#L130-L241)

서버는 API key의 DB binding, prompt·response 타입, 평가 설정 존재를 확인하고 `runOfflineEvaluation()`을 호출합니다. 여기서는 활성 평가 종류를 고르고, attributes에 맞는 Context 규칙과 사용자 contexts를 합쳐 provider·model·secret을 사용하는 `runEvaluation()`에 넘깁니다. 일반 LLM judge 경로는 Vercel AI SDK의 `generateText()` 결과를 JSON으로 해석합니다. 프롬프트에서는 context를 판단 기준으로 삼고 **점수가 높을수록 문제가 심하다**고 정의하므로, 점수를 무조건 “품질이 좋은 정도”로 읽으면 의미가 반대가 됩니다. [서버 입력 검증](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/client/src/app/api/evaluation/offline/route.ts#L12-L102), [평가 종류와 context 조립](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/client/src/lib/platform/evaluation/index.ts#L1074-L1188), [judge 프롬프트](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/client/src/lib/platform/evaluation/run-evaluation.ts#L20-L68), [모델 호출과 JSON 처리](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/client/src/lib/platform/evaluation/run-evaluation.ts#L150-L210)

`store_results` 기본값은 true이며 결과 저장을 시도합니다. 저장 함수가 오류를 반환해도 로그만 남긴 뒤 `success: true` 평가 응답으로 이어질 수 있습니다. 따라서 평가 계산의 성공과 결과 영속화 성공을 분리해 확인해야 합니다. 이 리뷰는 judge의 정확도, programmatic·human feedback 평가 전체, 별도 Typesafe/JEV provider의 동작을 비교 평가하지 않았습니다. [저장과 반환 경계](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/client/src/lib/platform/evaluation/index.ts#L1224-L1260)

### SDK 가드는 provider 바깥을 한 겹 더 감쌉니다

`init(guards=...)`는 일반 계측 뒤에 알려진 provider 메서드를 다시 감쌉니다. 동기 경로의 실제 순서는 preflight→기존 계측·원래 호출→postflight입니다. preflight에서 deny이면 API 호출 전에 `GuardDeniedError`를 발생시키며, redact이면 kwargs의 문자열 또는 마지막 메시지 content를 바꾸는 경로가 있습니다. postflight는 응답에서 텍스트를 추출해 평가하고 변환 또는 예외를 적용합니다. 모든 다중 모달 입력·응답 전체를 포괄하는 검증 계층으로 확장해 해석해서는 안 됩니다. [가드 설치](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/sdk/python/src/openlit/__init__.py#L443-L450), [입출력 변환](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/sdk/python/src/openlit/guard/_integration.py#L300-L367), [호출 래퍼](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/sdk/python/src/openlit/guard/_integration.py#L385-L454)

Pipeline은 지원 phase에 맞는 guard를 순서대로 실행하고, redact 결과를 다음 guard의 입력에 반영하며 deny에서 중단합니다. **`fail_open=True`가 기본**이어서 guard 자체가 예외를 던지면 allow 결과를 만드는 경로가 있습니다. 이를 false로 하면 해당 예외를 다시 발생시킵니다. 또한 integration 문서는 streaming 응답을 합쳐 검사하지 못해 postflight가 생략된다는 한계를 명시하고, 실제 postflight도 output extractor가 빈 문자열을 주면 바로 응답을 반환합니다. 가드를 구성했다는 사실과 모든 스트리밍 출력이 검사되었다는 사실은 구별해야 합니다. [Pipeline 구현](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/sdk/python/src/openlit/guard/_pipeline.py#L22-L90), [streaming 제한 명시](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/sdk/python/src/openlit/guard/_integration.py#L18-L22), [빈 출력 처리](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/sdk/python/src/openlit/guard/_integration.py#L332-L340)

## 설치와 사용: 같은 문서의 명령도 버전은 따로 봅니다

아래는 분석 커밋의 README에서 소개하는 명령입니다. 실행 결과를 확인한 예제가 아니라 사용 진입점을 설명하기 위한 인용입니다. [서버 시작 명령](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/README.md#L74-L87)

```bash
git clone https://github.com/openlit/openlit.git
cd openlit

docker compose up -d
```

Python 설치와 endpoint 지정 초기화 예시도 README에 있습니다. 아래 설치 명령은 배포 패키지의 버전을 고정하지 않습니다. [설치](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/README.md#L89-L95), [SDK 초기화](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/README.md#L125-L133)

```bash
pip install openlit
```

```python
import openlit

openlit.init(
    otlp_endpoint="http://127.0.0.1:4318"
)
```

코딩 CLI가 준비된 뒤의 구성·계측·진단 명령은 다음과 같습니다. 서로 다른 README 코드블록을 순서대로 발췌했으며, 중간 설명은 생략했습니다. [설정·설치·진단](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/README.md#L159-L184)

```bash
openlit configure --endpoint http://127.0.0.1:4318
openlit coding install --vendor=all
openlit doctor
```

README의 CLI bootstrap은 `main/cli/scripts/install.sh`를 내려받아 shell에 넘기는 방식입니다. 이 글에서는 실행하지 않았습니다. **분석 근거를 SHA에 고정하는 일과 README의 동적 설치 명령이 같은 SHA의 바이너리를 배포하는 일은 다릅니다.** pip·npm의 버전 없는 설치, `main` bootstrap, Compose의 `ghcr.io/openlit/openlit:latest`는 이 리뷰의 소스 revision과 동일한 실행물을 보장하지 않습니다. 재현성을 판단할 때는 실제 설치 버전·이미지 digest를 별도로 확인해야 하며, 이 글은 확인하지 않은 digest나 고정 설치 명령을 만들어 제시하지 않습니다. [CLI bootstrap 원문](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/README.md#L145-L157), [Compose 이미지](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/docker-compose.yml#L47-L56)

## 운영 경계와 라이선스

확인한 기본값 가운데 실제 사용 판단에 영향을 주는 항목은 다음과 같습니다. 이는 보안 전수 감사가 아니라 읽은 코드의 설정·데이터 경계입니다.

| 경계 | 분석 커밋에서 확인한 내용 |
| --- | --- |
| 앱 메시지 | Python `capture_message_content=True`; 시스템·GPU·DB parameter 수집과 분리됩니다. |
| 코딩 작업 본문 | CLI는 기본 `full`; 모드가 본문과 개별 span 분기를 정합니다. |
| 수신 인증 | `OTLP_REQUIRE_API_KEY` 기본 false; 키 없는 `INIT_DB_*` fallback이 있습니다. |
| 기본 배포 | ClickHouse 비밀번호 기본값과 NATS 개발용 기본 비밀번호가 있으며, UI와 OTLP·DB 포트를 publish합니다. |
| 제품 사용 telemetry | Compose는 `TELEMETRY_ENABLED: "true"`; 서버 PostHog 코드는 값이 `"false"`가 아니면 capture 요청을 보낼 수 있습니다. |

앞의 세 행은 각 절의 코드와 같으며, 배포 설정은 [Compose의 DB와 NATS 기본값](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/docker-compose.yml#L1-L38), [포트와 telemetry 설정](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/docker-compose.yml#L47-L90), 제품 telemetry는 [PostHog capture 조건과 요청](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/client/src/lib/posthog.ts#L16-L51)에 근거합니다. PostHog 경로에는 전달된 event·properties·응답 시간 등을 보내는 코드가 있지만, 이것만으로 모든 사용자 prompt가 외부 analytics로 간다고 추정하지는 않았습니다. [fireEvent 속성 조립](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/src/client/src/lib/posthog.ts#L54-L77)

최상위 `LICENSE`, Python SDK의 `LICENSE`, TypeScript SDK의 `LICENSE`는 모두 Apache License 2.0입니다. Python 매니페스트도 같은 라이선스를 명시합니다. 이 확인은 읽은 프로젝트 파일의 선언에 관한 것이며, 모든 외부 의존성의 라이선스·상표·모델 서비스 약관까지 감사한 결과는 아닙니다. [최상위 라이선스](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/LICENSE#L1-L9), [Python 라이선스](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/sdk/python/LICENSE#L1-L9), [TypeScript 라이선스](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/sdk/typescript/LICENSE#L1-L9), [Python 선언](https://github.com/openlit/openlit/blob/ec2639f8c2ffa10f8c42f9758e358c122f13976a/sdk/python/pyproject.toml#L1-L7)

## 이 글에서 다루지 못한 부분

README의 넓은 기능 목록 중 TypeScript SDK와 Go provider 계측 전반, 모든 Python 연동, Kubernetes controller의 주입 동작, GPU별 수집기, OpAMP, Prompt Hub·Vault·OpenGround·메모리·scanner의 전체 흐름은 상세 분석하지 않았습니다. CLI도 Codex 훅을 대표로 선택했으며 Claude Code·Cursor·OpenCode의 transcript와 상태 갱신을 전수 대조하지 않았습니다. trace 조회는 ClickHouse 경로를 추적했지만 외부 Tempo·Jaeger·Loki·Prometheus adapter의 호환성, realtime rule 종류 전체와 알림 후속 동작, 온라인 자동 평가의 샘플링·스케줄링 전체는 검증하지 않았습니다. 대상 코드 실행과 테스트를 하지 않았으므로 설치 성공, 최신 배포물과의 일치, 처리량, 비용 정확도, judge·guard의 탐지 품질도 미확인입니다.

## 마무리

OpenLIT을 읽을 때 핵심은 기능 개수보다 **어떤 입력이 어느 계층에서 관측 데이터로 바뀌는가**입니다. Python은 provider 함수를 감싸고, 코딩 CLI는 프로세스 사이 이벤트를 세션으로 재구성하며, Go 수신기는 tenant를 결정해 ClickHouse에 씁니다. 웹의 adapter 경계는 이를 화면의 행과 trace tree로 바꾸고, 서버 평가와 SDK 가드는 각각 실행 후 판단과 호출 전후 제어를 맡습니다. 읽은 코드에서는 본문 수집 기본값, 키 없는 ingest fallback, 비차단 신호 queue, 평가와 저장의 성공 분리가 특히 중요한 경계였습니다. 이들을 구별해야 대시보드에 보이는 정보의 출처와 누락 가능성을 구체적으로 이해할 수 있습니다.
