---
type: "Repo Review"
title: "[Repo Review] AKV — 에이전트가 KV 캐시를 직접 관리하는 구조와 SGLang 실행 경로"
description: "AKV의 에이전트 정책부터 SGLang의 토큰 이벤트·캐시 재사용·위치 변환까지 추적하고, 실제 연동 방식과 지원 제약을 살펴봅니다."
date: "2026-10-23"
tags:
  - "Repo Review"
  - "AI Agent"
  - "Transformer"
  - "딥러닝"
  - "머신러닝"
  - "Python"
resource: "https://github.com/thu-nics/AKV/tree/c567a429a058f1abce3b2879e69978b09e0fda4c"
generated:
  by: "process:blog-review"
  at: "2026-10-23T00:21:18+09:00"
sources:
  - id: "github:thu-nics/AKV"
    resource: "https://github.com/thu-nics/AKV/tree/c567a429a058f1abce3b2879e69978b09e0fda4c"
    title: "AKV: Cache Engineering for Agents"
    revision: "c567a429a058f1abce3b2879e69978b09e0fda4c"
    last_modified: "2026-10-21T14:04:49+08:00"
status: "stable"
year: "2026"
analyzed_at: "2026-10-23T00:21:18+09:00"
source_id: "thu-nics/AKV"
source_revision: "c567a429a058f1abce3b2879e69978b09e0fda4c"
source_title: "AKV: Cache Engineering for Agents"
source_type: "repo"
source_url: "https://github.com/thu-nics/AKV/tree/c567a429a058f1abce3b2879e69978b09e0fda4c"
visual_sources:
  - path: "/img/reviews/2026/akv-review/architecture.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/examples/demo.py#L145-L201"
    caption: "리뷰어 작성, 분석 커밋 기준: 하네스·정책·전송·추론 서버의 책임 경계"
  - path: "/img/reviews/2026/akv-review/server-flow.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/sglang/srt/context_system/planner.py#L524-L569"
    caption: "리뷰어 작성, 분석 커밋 기준: 토큰 소유권에서 캐시 버전·GPU 실행으로 이어지는 경로"
    evidence:
      - "https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/sglang/srt/context_system/ir.py#L115-L134"
      - "https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/sglang/srt/context_system/occurrence.py#L341-L467"
      - "https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/sglang/srt/layers/attention/context_backend.py#L373-L529"
---

## 긴 에이전트 실행에서, 무엇을 기억할지 결정하는 계층

도구를 여러 번 호출하는 LLM 에이전트는 대화 이력에 검색 결과, 파일 내용, 실행 로그를 계속 덧붙입니다. 예전에 읽은 기록의 세부 내용이 더는 필요하지 않아도, 다음 모델 호출에서 같은 이력이 다시 문맥으로 들어갑니다. Transformer가 토큰마다 저장하는 **KV 캐시(Key·Value cache)**는 앞서 계산한 attention의 Key와 Value를 재사용하는 장치입니다. 그러나 문맥을 줄이겠다고 요청의 중간 메시지를 지우면, 원래의 토큰 순서와 위치를 전제로 만들어진 캐시를 그대로 활용하기 어려워집니다.

**AKV는 “무엇을 언제 잊을 것인가”를 에이전트 정책으로 정하고, 그 결정을 KV 캐시 연산으로 실행하는 도구입니다.** `akv.agent`는 삭제와 위치 압축 지시를 만들고, `akv.system`은 수정된 SGLang 추론 서버에서 그 지시를 처리합니다. 원본 대화 이력을 유지한 채 모델이 이후에 읽을 KV와 위치를 바꾼다는 점이 구조의 중심입니다. [루트 README](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/README.md#L12-L16)

이 리뷰는 `thu-nics/AKV`의 **`c567a429a058f1abce3b2879e69978b09e0fda4c`** 커밋을 고정해 문서·매니페스트·주요 코드를 정적으로 분석했습니다. 대상의 의존성을 설치하거나 서버·예제를 실행하지 않았습니다. 따라서 아래 사용법은 같은 커밋의 문서와 코드에서 확인한 경로이며, 실행 성공이나 성능을 재현한 결과는 아닙니다. README가 연결하는 [*Cache Engineering for Agents*](https://arxiv.org/abs/2610.28577v1)는 연구 배경이고, 본문의 분석 대상은 구현 저장소입니다. 논문의 속도·품질 수치를 이 코드의 실행 결과로 대체하지 않습니다.

## 1. AKV의 두 연산: Drop과 Reposition

AKV가 외부에 노출하는 중심 연산은 두 가지입니다.

| 연산 | 바뀌는 것 | 유지되는 것 | 요청 필드 |
| --- | --- | --- | --- |
| **Drop** | 지정한 메시지의 KV가 이후 attention에서 읽히는지 여부 | 남은 토큰의 기존 위치, 요청의 원본 메시지 목록 | `drop_message` |
| **Reposition** | 남은 토큰의 위치를 빈틈 없이 압축 | 공개 메시지 ID와 원본 이력 | `reposition` |

두 연산은 독립적입니다. 같은 경계에 함께 지정하면 **Drop을 먼저 적용하고 Reposition을 수행**합니다. Drop은 요약문을 만드는 기능이 아닙니다. 남은 토큰을 처음부터 다시 모델에 통과시켜 “짧아진 프롬프트의 결과”를 얻는 기능으로도 이해하면 안 됩니다. 기존 KV를 활용하고, 필요한 위치 변환과 새 토큰 계산을 수행하는 시스템입니다. [README의 연산 설명](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/README.md#L208-L223), [이벤트 컴파일 계약](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/sglang/srt/context_system/ir.py#L115-L134)

### 1.1 README의 A·B 비교 예시를 읽는 방법

Quick Start는 `read_record(A)`와 `read_record(B)`를 차례로 호출한 대화를 사용합니다. 공개 메시지 ID는 0부터 시작합니다.

| 메시지 ID | 역할 | 내용 |
| --- | --- | --- |
| 0 | user | 기록 A와 B를 비교해 달라는 요청 |
| 1 | assistant | `read_record(A)` 호출 |
| 2 | tool | Record A |
| 3 | assistant | `read_record(B)` 호출 |
| 4 | tool | Record B |

`TurnSelection(1)`을 적용한 문서 예시에서는 다음 필드가 추가됩니다. 아래는 원문 출력에서 **캐시 연산 필드만 발췌**한 것입니다. [Quick Start 원문](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/README.md#L114-L133)

```json
{
  "drop_message": {"4": [2]},
  "reposition": [4]
}
```

의미는 “메시지 4를 처리한 뒤 메시지 2의 KV를 Drop하고, 남은 토큰의 위치를 압축한다”입니다. **메시지 2를 JSON에서 직접 삭제하라는 뜻이 아닙니다.** 메시지 4를 계산하는 동안에는 이전 문맥이 보일 수 있고, 그 경계 이후의 계산부터 Drop이 반영됩니다. 원본 이력과 이후에 접근 가능한 KV 상태를 분리하는 이유가 여기에 있습니다.

이렇게 지운 Record A의 정보가 모델의 모든 내부 표현에서 완전히 사라졌다고 보장할 수도 없습니다. 앞서 계산한 다른 KV는 Record A를 읽은 상태일 수 있습니다. 코드는 선택한 KV의 가시성과 재사용 경로를 제어하며, 정보의 완전한 소거나 개인정보 삭제를 증명하는 시스템은 아닙니다. 이는 [원본 이력 유지](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/agent/policies/utils/request.py#L91-L107)와 [기존 KV 위치 변환](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/sglang/kernels/ops/attention/context_reposition.py#L99-L134)을 함께 읽었을 때의 구현상 해석입니다.

## 2. 전체 구조: 하네스, 정책, 전송, 추론 시스템

![AKV의 하네스·정책·HTTP 전송·추론 서버와 응답 경계를 보여주는 도식]({{ '/img/reviews/2026/akv-review/architecture.svg' | relative_url }})

*리뷰어 작성, 분석 커밋 기준. 하네스가 최종 요청을 만든 다음 정책을 적용하고, 응답을 받은 뒤 이력을 갱신하는 흐름입니다. [데모 루프](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/examples/demo.py#L145-L201), [SSE 클라이언트](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/agent/backends/chat.py#L37-L74), [서버 진입점](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/launch_server.py#L1-L7)을 근거로 작성했습니다.*

저장소는 이 경계를 패키지 구성에서도 드러냅니다.

| 경로 | 주요 책임 | 분석에서 확인한 경계 |
| --- | --- | --- |
| `akv/agent/policy.py` | 세 정책을 조합하고 요청에 누적 연산 추가 | 네트워크 호출·GPU 메모리 조작을 하지 않음 |
| `akv/agent/policies/` | Drop 시점, 삭제 대상, 위치 압축 시점 | 턴 기반·토큰 기반·모델 도구 기반 선택 |
| `akv/agent/policies/utils/` | 메시지 묶음, 이력 연속성, 토큰 레이아웃 | 하네스가 넘기는 최종 메시지 순서 기준 |
| `akv/agent/backends/` | HTTP/SSE, 응답 조립, 선택적 호출 기록 | 정책 적용·도구 실행·재시도 책임은 호출자에게 있음 |
| `akv/system/sglang/srt/context_system/` | 메시지 지시를 토큰 이벤트와 캐시 상태로 변환 | 가시성·위치·복구·사용량을 명시적으로 관리 |
| `akv/system/sglang/srt/layers/attention/` | attention 실행용 메타데이터와 KV 바인딩 | 실제 모델·GPU pool의 형식에 연결 |
| `akv/system/sglang.patch` | SGLang의 HTTP·스케줄러·캐시·라우터 연결 변경 | 독립 Python 파일만으로 끝나지 않는 통합 계층 |
| `akv/system/_build.py` | 고정한 SGLang 소스에 패치와 overlay 적용 | 별도 upstream 소스와 native build backend 필요 |

[`akv-agent` 매니페스트](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/agent/pyproject.toml#L5-L19)의 기본 런타임 의존성은 비어 있으며, 토큰 계수 기능은 `tokenization` extra로 분리됩니다. 반면 [`akv-system`](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/pyproject.toml#L5-L22)은 `sglang==0.5.20+akv`, `sglang-router==0.3.2+akv`, CUDA 13용 Mooncake 전송 패키지를 지정합니다. 루트 `akv` 패키지는 agent의 토큰화 extra와 system을 함께 묶습니다. 클라이언트 정책만 사용하는 환경과 추론 서버 환경을 구분해서 이해해야 합니다.

## 3. 요청이 정책을 통과하는 과정

### 3.1 입력은 하네스가 직렬화한 마지막 요청입니다

`CachePolicy.process`는 `messages`와 `tools`가 들어 있는 최종 HTTP payload를 받습니다. SDK의 `extra_body`가 아직 중첩되어 있거나, 기존 `drop_message`·`drop_rule`·`reposition` 지시가 이미 들어 있는 요청은 거부합니다. 정책 실행 뒤에 하네스가 메시지를 다시 정렬하거나 포맷을 바꾸면, 계산해 둔 ID와 경계가 맞지 않을 수 있기 때문입니다. [입력 검사와 파싱](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/agent/policies/utils/request.py#L38-L88)

`read_request`는 메시지를 깊은 복사로 읽고 `atomic_message_units`를 통해 assistant의 tool call과 그에 대응하는 tool result를 묶습니다. tool call ID가 중복되거나, 결과가 빠져 있거나, 앞선 assistant 호출과 연결되지 않는 tool 메시지가 있으면 오류를 냅니다. 턴 기반 정책에서 말하는 턴은 단순한 채팅 한 줄이 아니라 **완료된 도구 호출 묶음**을 중심으로 정의됩니다. [메시지 단위 검사](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/agent/policies/utils/messages.py#L10-L46)

여러 도구를 한 번에 호출했다면 그 결과가 모두 도착한 뒤 정책을 적용해야 합니다. 네이티브 tool 형식이 아닌 사용자 관찰 메시지를 쓰는 하네스에는 `completed_call_message_ids`를 전달하는 경로도 있지만, 이때도 완료 경계의 순서·역할과 기존 tool 묶음을 검사합니다. 이 정보는 토큰 ID가 아니라 **대화 메시지 목록의 인덱스**입니다.

### 3.2 세 결정은 분리되어 있습니다

`CachePolicy`는 아래 세 callable을 조합합니다. 설정하지 않은 구성요소는 해당 연산을 선택하지 않습니다. [정책 조합](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/agent/policy.py#L23-L48)

| 구성요소 | 질문 | 대표 내장 구현 |
| --- | --- | --- |
| `trigger` | 지금 삭제 대상을 고를 것인가? | `TurnTrigger`, `TokenTrigger`, `ModelTrigger` |
| `selector` | 어느 메시지의 KV를 지울 것인가? | `TurnSelection`, `TokenSelection`, `ModelSelection` |
| `reposition` | 지금 남은 위치를 압축할 것인가? | `TurnReposition`, `TokenReposition`, `ModelReposition` |

이 분리는 삭제와 압축을 같은 빈도로 수행할 필요가 없다는 뜻입니다. `current_actions`는 trigger가 참이고 selector가 있을 때만 대상을 고릅니다. Reposition 규칙은 그 선택 집합을 인자로 받지만, Drop trigger와는 별도로 평가됩니다. 따라서 “새로 지운 메시지가 있을 때만 압축” 같은 사용자 규칙과 “세 턴마다 압축” 같은 내장 규칙을 서로 다르게 구성할 수 있습니다.

`TurnSelection`의 기본 target은 `tool`입니다. 최근 `count`개 완료 턴을 남기고 오래된 tool result를 선택합니다. `target="assistant"`나 `"both"`일 때는 연결된 도구 결과가 모두 만료되는지를 고려해 assistant 메시지도 선택합니다. 단순히 목록 앞의 N개 메시지를 잘라내는 알고리즘이 아닙니다. [선택 로직](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/agent/policies/selectors.py#L17-L78)

토큰 기반 정책은 서버가 렌더링할 프롬프트와 맞는 계수기를 요구합니다. 사용자 본문만 세면 role 구분자, tool schema, generation prefix, thinking 설정 때문에 기준이 달라집니다. `TokenTrigger`는 숨겨진 메시지의 토큰 수를 뺀 prompt가 임계값을 초과하는지 보고, `TokenSelection`은 오래된 도구 결과부터 선택하면서 남길 토큰 예산을 맞춥니다. `TokenReposition`은 이전 압축 시점까지 처리한 Drop과 그 이후의 Drop을 구분합니다. [trigger](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/agent/policies/triggers.py#L24-L36), [selector](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/agent/policies/selectors.py#L37-L60), [reposition](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/agent/policies/reposition.py#L24-L45), [계수기 일치 조건](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/agent/README.md#L42-L58)

### 3.3 CacheOperationHistory는 GPU 캐시의 복사본이 아닙니다

정책이 반환하는 두 번째 값은 `CacheOperationHistory`입니다. 이 객체에는 선택한 삭제 ID, Reposition 여부, 적용할 메시지 경계와 이전 입력의 digest가 들어갑니다. **서버가 실제로 연산을 완료했다는 확인서나 KV tensor는 들어 있지 않습니다.** 대화의 각 분기마다 하네스가 별도로 보관하는 명령 이력입니다. [타입 정의](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/agent/types.py#L119-L165)

다음 호출에서는 이 객체와 늘어난 원본 메시지 목록을 다시 `process`에 넘깁니다. 함수는 이전 메시지 prefix가 유지되는지, 모델·도구·template 관련 설정의 digest가 같은지 검사합니다. 예전 메시지를 수정하거나 다른 모델의 이력을 같은 객체에 연결하면 오류를 냅니다. 새 메시지가 없을 때에는 새 정책 결정을 추가하지 않습니다. [연속성 검사](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/agent/policies/utils/request.py#L13-L35), [갱신 조건](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/agent/policy.py#L67-L92)

다음 코드는 실제 `process`의 마지막 부분을 발췌한 것입니다. 생략한 앞부분에서 입력과 선택 결과의 유효성을 검사합니다.

```python
        if size > cache_operation_history.message_count:
            operations = cache_operation_history.operations
            if selected or reposition:
                operations = (*operations, CacheOperation(size - 1, tuple(selected), reposition))
            cache_operation_history = CacheOperationHistory(
                operations, size, prefix_digest(request, size), context_digest
            )
        return prepare_payload(payload, cache_operation_history), cache_operation_history
```

[코드 출처: `policy.py`](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/agent/policy.py#L85-L92). 새 결정은 **현재 마지막 메시지인 `size - 1` 경계**에 기록됩니다. 과거의 모든 턴마다 정책을 다시 실행해 소급 결정을 만드는 방식은 아닙니다. 특히 이미 긴 이력에서 처음 `process`를 호출하는 경우와, 매번 완료된 턴 뒤에 호출해 온 경우의 연산 이력을 동일하다고 가정하면 안 됩니다.

`prepare_payload`는 원본 payload를 깊은 복사한 다음 **누적된** 연산을 `drop_message`와 `reposition`으로 직렬화합니다. 이전에 지운 메시지를 원본 목록에서 제거하지 않습니다. 같은 메시지를 중복 Drop하지 않도록 hidden 집합을 고려하고, 생성한 operation의 경계가 순서대로 증가하는지도 타입 계층에서 검사합니다. [직렬화](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/agent/policies/utils/request.py#L91-L123), [이력 불변조건](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/agent/types.py#L137-L165)

### 3.4 모델이 직접 지울 대상을 고를 때도 실행 책임은 하네스에 있습니다

`DropContextTool`은 `drop_context`라는 함수 schema를 모델에 노출합니다. 모델은 결과에 붙어 있는 canonical `message_id`를 골라 tool call을 만들고, 하네스가 `execute`를 호출합니다. 이 메서드는 서버로 요청하지 않고 **`status: scheduled`인 영수증**을 반환합니다. 다음 모델 호출 전에 `ModelTrigger`·`ModelSelection`이 성공 영수증과 원래 인자를 대조해 지시로 바꿉니다. [도구 인터페이스와 영수증 처리](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/agent/policies/tools.py#L12-L41), [execute와 read_result](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/agent/policies/tools.py#L99-L187)

삭제 가능 대상은 이미 숨겨지지 않은 이전 tool result이며, 기본으로 앞의 두 메시지는 보호됩니다. 잘못된 ID 하나가 포함되면 전체 호출을 오류 결과로 처리합니다. 도구 설명에도 요약을 만들지 않고 삭제 결정을 되돌리는 기능이 없다고 명시합니다. 이것은 모델에게 맹목적으로 캐시 삭제 권한을 주는 경로와 다릅니다. 다만 유효한 ID인지 검사하는 것이, 그 정보가 업무상 정말 불필요한지까지 검증하는 것은 아닙니다.

[데모](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/examples/demo.py#L240-L253)는 `ModelTrigger`·`ModelSelection`으로 Drop을 고르게 하면서 Reposition은 `TurnReposition(after=3, every=3)`으로 설정합니다. 즉, tool call 인자에 `reposition`이 있더라도 실제로 어떤 Reposition 규칙을 정책에 연결했는지를 함께 봐야 합니다. 도구 호출 영수증과 서버 실행을 구분하는 설계가 반복 실행의 책임 경계를 분명하게 만듭니다.

## 4. 전송 계층: 모델 호출과 캐시 정책을 결합하지 않습니다

`send_chat_request`는 정책 적용을 끝낸 payload를 그대로 보냅니다. 이 함수는 `stream=true`를 요구하며, JSON 응답 전체를 한 번에 받는 범용 SDK 대신 HTTP와 **SSE(Server-Sent Events)**를 사용합니다. 스트림에 섞여 도착하는 본문, reasoning, tool-call 인자 조각을 모아 `GenerationResult`로 만듭니다. [요청·응답 수집](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/agent/backends/chat.py#L37-L74), [SSE 조립](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/agent/backends/chat.py#L77-L184)

SSE 종료 표식 `[DONE]`이 오기 전에 연결이 끝나면 오류를 냅니다. 여러 completion choice를 한꺼번에 처리하는 클라이언트도 아닙니다. tool call의 이름·ID·arguments 조각은 index별로 이어 붙이고, usage와 서버 부가 정보를 결과에 포함합니다. HTTP 오류나 문맥 길이 오류는 별도 예외 타입으로 전달합니다. 정책 판단, 실제 업무 도구 실행, 재시도는 이 클라이언트가 대신하지 않습니다. [transport](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/agent/backends/transport.py#L24-L88)

선택적인 `BackendTraceContext`를 넘기면 요청·SSE·이벤트·시간 정보가 호출별 디렉터리에 기록됩니다. 이미 존재하는 경로의 재사용을 거부하고, 실패 시 부분 응답을 남깁니다. Authorization 등 정해진 민감 header는 마스킹하지만, 요청 본문과 응답 자체는 저장합니다. 따라서 trace에는 원본 대화나 도구 결과가 포함될 수 있다는 점을 운영에서 고려해야 합니다. [호출 기록](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/agent/backends/capture.py#L28-L79)

하네스의 최종 반복 순서는 데모에서 확인할 수 있습니다. **요청 직렬화 → 정책 적용 → 변환 없이 전송 → 응답 수신 → operation history 채택 → assistant와 모든 tool result 추가**입니다. 데모는 성공적으로 응답을 받은 뒤 다음 operation history를 채택하며, 도구가 생성한 결과들을 모두 붙인 다음 새 모델 호출로 넘어갑니다. [데모의 상태 갱신](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/examples/demo.py#L145-L223)

## 5. 서버는 메시지 지시를 어떻게 실제 KV 연산으로 바꾸는가

정책이 만든 JSON만으로 KV가 바뀌는 것은 아닙니다. `akv.system.launch_server`는 `runpy`로 `sglang.launch_server`에 진입합니다. 기능의 본체는 AKV가 준비한 **패치된 SGLang과 overlay 모듈**에 있으며, 서버는 OpenAI 형식의 메시지 요청을 받은 뒤 토큰별 이벤트 프로그램으로 바꿉니다. [실행 진입점](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/launch_server.py#L1-L7), [serving 연결 패치](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/sglang.patch#L1307-L1360)

![메시지 ID의 토큰 소유권 추적부터 이벤트 컴파일, 캐시 버전 대조, KV 복구와 GPU 위치 변환으로 이어지는 서버 흐름]({{ '/img/reviews/2026/akv-review/server-flow.svg' | relative_url }})

*리뷰어 작성, 분석 커밋 기준. [planner](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/sglang/srt/context_system/planner.py#L524-L569), [캐시 키 IR](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/sglang/srt/context_system/ir.py#L298-L427), [occurrence 계획](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/sglang/srt/context_system/occurrence.py#L341-L467), [attention 바인딩](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/sglang/srt/layers/attention/context_backend.py#L373-L529)의 책임을 나누어 표시했습니다. 도식의 화살표는 논리적 처리 순서이며, 매 요청마다 모든 KV를 복사한다는 뜻은 아닙니다.*

### 5.1 먼저 지원 가능한 요청인지 검사합니다

`drop_message`·`drop_rule`·`reposition` 중 하나를 명시한 요청은 Context 경로로 들어갑니다. 여기서 서버 설정과 모델 지원 조건을 검사합니다. 명시적으로 빈 필드를 넣어도 이 검사 경로를 선택할 수 있습니다. 반대로 Context 기능을 요청하지 않은 일반 요청까지 동일한 기능 제약을 모두 부과하는 구조는 아닙니다. [분기 조건](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/sglang.patch#L1316-L1347)

그다음 `parse_drop_rule`이 공개 필드를 규칙 객체로 읽습니다. agent가 만드는 `drop_message`는 내부에서 `MessageDropRule`로 바뀝니다. 서버에는 더 세밀한 `text_drop`, `keep_text_drop`, `thinking_drop`도 있지만, 이것이 `CachePolicy`의 기본 출력 형식과 같다는 뜻은 아닙니다. `drop_rule`과 기존 `drop_message`를 동시에 주면 거부합니다. [규칙 파서](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/sglang/srt/context_system/rules.py#L742-L776)

### 5.2 메시지 번호를 토큰 범위로 연결합니다

클라이언트는 “메시지 2를 지운다”고 말하지만, attention은 메시지가 아니라 토큰 단위로 계산합니다. 따라서 서버에는 **각 토큰이 어느 메시지의 렌더링 결과에 속하는지**를 알아내는 과정이 필요합니다. 이 대응 관계가 provenance입니다.

Jinja 템플릿 경로에서는 템플릿 출력의 문자 소유권을 추적하고, 완성된 텍스트를 토큰화한 offset을 이용해 토큰 owner를 만듭니다. `provenance.py`는 role 구분자나 template가 출력한 문자열도 포함한 실제 프롬프트를 기준으로 동작합니다. GPT-OSS는 별도의 Harmony encoder 경로를 통해 토큰과 owner를 제공합니다. 메시지 본문에 같은 단어가 반복된다는 이유로 문자열 검색만 해서 삭제 경계를 정하는 방식과 구별됩니다. [Jinja provenance](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/sglang/srt/context_system/provenance.py#L334-L402), [GPT-OSS 연결부](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/sglang.patch#L1380-L1431)

메시지 경계에 걸친 토큰도 별도로 센다는 점이 눈에 띕니다. 일반 토큰 provenance에서는 여러 owner의 문자가 한 토큰에 걸리면 첫 문자의 owner를 택하고 `cross_owner_tokens`를 증가시킵니다. 따라서 “메시지 하나는 언제나 독립적으로 토큰화할 수 있는 깔끔한 블록”이라고 전제하면 안 됩니다. 실제 모델의 템플릿과 계수기를 맞춰야 한다는 agent 문서의 요구가 서버 구현과 연결됩니다.

### 5.3 Drop과 Reposition을 이벤트 프로그램으로 컴파일합니다

`compile_chat_program`은 owner별 토큰 범위를 모으고, 삭제 대상 메시지를 토큰 구간으로 바꿉니다. Drop 지점은 해당 경계 다음 query가 시작되는 삽입 위치로, Reposition은 공개 메시지 ID에 해당하는 마지막 토큰 경계로 해석됩니다. 미래 토큰이 계산되기 전에 숨겨지는 잘못된 계획은 거부합니다. [토큰 이벤트 생성](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/sglang/srt/context_system/planner.py#L141-L196), [Reposition 경계 해석](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/sglang/srt/context_system/planner.py#L48-L82)

이 결과를 `compile_context_layout`에 넘기면 다음과 같은 정보가 만들어집니다.

| 상태 | 구현 필드의 예 | 필요한 이유 |
| --- | --- | --- |
| 실제 토큰과 사건 기록 | `records`, `virtual_mask` | 텍스트 외에 Drop·위치 변환 이력을 구분 |
| 원본 토큰과 캐시 키의 대응 | `key_to_token`, `token_to_key` | 이벤트 기록을 실제 KV 토큰 수와 혼동하지 않음 |
| 위치와 생존 상태 | `positions`, `keep_mask`, `next_position` | 이후 계산에서 읽을 토큰과 위치를 결정 |
| 생성 시점의 위치와 단계 | `birth_positions`, `birth_stages` | 계산 당시 버전과 이후 압축 버전을 구분 |
| 위치 변환의 원본·대상 | `transition_old_positions`, `transition_new_positions` | 기존 KV에 필요한 변환을 계획 |

[ContextLayout 정의](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/sglang/srt/context_system/ir.py#L37-L64)를 보면 공개 메시지 번호, 원래 토큰 순서, 압축 후 위치, GPU 슬롯이 서로 다른 좌표계라는 사실이 드러납니다. 이들을 하나의 “인덱스”로 설명하면 구조를 놓치기 쉽습니다.

`ContextProgram`은 layout과 `visible_until`을 함께 가지고, CPU tensor 기반 내부 wire 형식으로 scheduler에 전달됩니다. scheduler 쪽에서는 wire 필드·dtype·shape뿐 아니라 token record가 원래 `input_ids`를 실제로 설명하는지도 검사합니다. 물리적 KV 페이지 번호는 이 불변 요청 프로그램에 섞지 않습니다. [프로그램 전달·검사](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/sglang/srt/context_system/planner.py#L316-L521)

### 5.4 캐시 재사용의 기준에는 사건과 위치도 들어갑니다

같은 문자열의 프롬프트라도 어느 시점에 무엇을 Drop했는지에 따라 뒤쪽 KV가 달라질 수 있습니다. AKV의 `ContextKeyData`는 token record와 앞에 붙는 가상 event record를 묶어 Radix 트리의 prefix를 비교합니다. TOKEN·DELTA·REPOSITION 종류를 구분하고, 일반 비교에서는 토큰 ID와 위치 정보를 함께 사용합니다. [IR 종류](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/sglang/srt/context_system/ir.py#L32-L34), [구조화된 prefix 비교](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/sglang/srt/context_system/ir.py#L298-L427)

핵심은 `match`가 **완전히 같은 TOKEN record까지만 실제 토큰 cache hit로 센다**는 점입니다. 앞의 사건이 다르면 그다음 토큰을 우연히 같은 것으로 세지 않도록 합니다. 별도의 retry record는 위치를 0으로 둔 비교 표현을 갖지만, 이것이 서로 다른 KV를 아무 조건 없이 교환한다는 뜻은 아닙니다. 그 경로에서는 재사용할 수 있는 원본·위치·복구 필요 여부를 다시 추적합니다.

`OccurrenceState`는 요청별로 KV 슬롯의 소유 관계를 보관합니다. 같은 원본 토큰이 서로 다른 단계·위치에서 필요할 수 있으므로, “이 토큰의 캐시가 있다”와 “지금 필요한 버전의 캐시를 읽을 수 있다”를 구분해야 합니다. `plan_occurrence_materialization`은 각 occurrence에 대해 기존 terminal 버전을 재사용할지, 원본을 빌릴지, 새 슬롯을 배정하고 복사할지 결정합니다. 같은 위치여도 다른 Radix 분기에 소유권을 넘길 때에는 copy-on-write가 필요할 수 있습니다. [소유권 계획](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/sglang/srt/context_system/occurrence.py#L341-L467), [요청 상태](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/sglang/srt/context_system/occurrence.py#L470-L526)

따라서 README의 “남은 KV를 re-prefill 없이 재사용한다”는 설명은 **호환되는 KV가 실제로 남아 있는 경우의 중심 동작**으로 읽어야 합니다. 모든 요청·메모리 압박 상황에서 재계산이 절대 없다는 보장은 아닙니다. `plan_recovery`는 이후 query가 읽어야 하는데 빠져 있는 KV가 있는지 역방향으로 의존성을 닫고, 복구해야 할 query 구간을 만듭니다. 이미 resident인 중간 구간은 재사용할 수 있게 남깁니다. [복구 계획](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/sglang/srt/context_system/recovery.py#L253-L391)

### 5.5 Reposition은 배열 번호만 바꾸는 일이 아닙니다

RoPE(Rotary Position Embedding)를 쓰는 모델에서는 Key에 위치 회전이 반영됩니다. 살아남은 KV를 다른 위치에 놓으려면 K의 위치 성분도 맞춰야 합니다. `ContextModelBinding`은 실제 모델의 rotary 모듈과 KV pool을 찾아 연결하며, partial RoPE나 sliding-window attention의 메모리 매핑도 구분합니다. [모델 연결](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/sglang/srt/layers/attention/context_backend.py#L373-L430)

`context_reposition.py`의 GPU kernel은 기존 위치의 회전을 FP32로 되돌린 다음 새 위치 회전을 적용해 K를 저장합니다. RoPE가 적용되지 않는 K의 나머지 성분과 V는 복사합니다. 위치가 같을 때는 불필요한 회전 왕복을 피하려고 원본 값을 복사합니다. 별도의 대상 슬롯을 쓰므로 공유된 원본 페이지를 제자리에서 덮어쓰는 방식도 아닙니다. [위치 변환 kernel](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/sglang/kernels/ops/attention/context_reposition.py#L77-L157)

이 구현은 **모델 전체를 다시 forward하는 것과 기존 K의 위치 성분을 변환하는 것의 차이**를 잘 보여줍니다. Reposition을 했다고 해서 Drop 이후의 짧은 프롬프트를 처음부터 계산한 KV와 수치적으로 같다고 결론내릴 수는 없습니다. 코드가 하는 일은 이미 존재하는 표현을 위치에 맞게 변환하고, 그 상태에서 다음 계산을 이어가는 것입니다.

attention 쪽은 `ContextSequence`와 `ContextAttentionPlan`으로 query 구간·읽을 prefix occurrence·각각의 실제 위치를 묶습니다. 이 메타데이터를 물리적 KV 슬롯에 바인딩한 뒤 attention backend에 넘깁니다. sliding-window에서 위치에 빈틈이 있을 때는 query별 읽기 구간도 조정합니다. Drop 이후에도 원래 위치를 남겨 두는 경우와 Reposition으로 위치를 압축한 경우를 같은 연속 배열로 가정하지 않는 것입니다. [attention 계획](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/sglang/srt/layers/attention/context_backend.py#L25-L251)

### 5.6 삭제 결정과 GPU 메모리 회수는 구분합니다

모델이 더 이상 읽지 않는 KV라고 해서 공유 캐시의 물리 페이지를 즉시 마음대로 해제할 수 있는 것은 아닙니다. 다른 요청의 참조나 아직 끝나지 않은 forward가 있을 수 있습니다. AKV는 완료된 cache publication 뒤에, 해당 경로의 Drop 기록과 이후 읽기 수요를 근거로 필요 없는 소유권을 해제하는 경로를 둡니다. [Drop-aware 캐시 연결](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/sglang.patch#L5903-L5992)

`DropEvictionCandidates`는 Drop으로 불필요함이 입증된 edge를 일반 leaf보다 먼저 검토하는 두 heap을 사용합니다. `proven_skip_ranges`는 **현재 대조한 경로의 DELTA record**만이 조상 KV 해제를 허용할 수 있다고 제한합니다. 이 때문에 Drop은 논리적 가시성 변경, 캐시 재사용, 참조 보호, 메모리 회수라는 여러 단계를 함께 다루는 기능입니다. [회수 후보와 해제 근거](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/sglang/srt/context_system/recovery.py#L33-L102)

## 6. 응답의 사용량은 무엇을 세는가

Context 요청의 `usage.prompt_tokens_details`에는 다음 세 값이 0일 때도 포함됩니다. 일반 API의 token count처럼 이름만 보고 합산하면 의미를 오해할 수 있습니다. [usage 응답 패치](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/sglang.patch#L1728-L1817)

| 값 | 코드에서의 집계 의미 |
| --- | --- |
| `cached_tokens` | 초기 resident 캐시 중 실제로 읽혔고 위치 변환 대상으로 집계되지 않은 토큰 |
| `repos_tokens` | 초기 resident 캐시 중 실제 읽기에서 위치 변환 대상으로 집계된 토큰 |
| `drop_skipped_tokens` | Drop으로 이후 읽기가 생략된 대상으로 집계되며, 복구 query 등은 제외한 토큰 |

`ContextUsage`는 chunk별 읽기 집합의 **합집합**을 관리합니다. 같은 캐시 토큰을 여러 chunk에서 읽었다고 계속 중복 집계하지 않습니다. Reposition을 예약했어도 실제 query가 읽지 않은 변환은 `repos_tokens`에 더하지 않습니다. 반면 실제 prefill·decode query 수는 별도로 세며, 복구 재계산도 작업량에 반영합니다. [사용량 정의와 계산](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/sglang/srt/context_system/usage.py#L20-L124)

이 구분은 절약 효과를 평가할 때 중요합니다. “삭제 대상으로 고른 메시지 수”, “원본 프롬프트의 토큰 수”, “실제로 수행한 prefill”, “읽고 재사용한 KV”는 서로 다른 값입니다. 이 리뷰에서는 실행 측정을 하지 않았으므로 이 계수를 속도 향상 비율이나 GPU 메모리 절약률로 바꾸어 제시하지 않습니다.

## 7. 문서 기준 설치와 하네스 연동

### 7.1 정책만 쓸 환경과 전체 추론 환경을 나눕니다

agent만 설치하는 문서의 명령은 다음과 같습니다. 저장소 루트에서 별도의 환경을 만드는 예시이며, 토큰화 extra가 없는 기본 패키지는 Python 표준 라이브러리를 사용합니다. [agent 설치 문서](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/agent/README.md#L5-L20)

```bash
uv venv --python 3.12 .venv-algo
source .venv-algo/bin/activate
uv pip install -e ./akv/agent
```

토큰 기반 정책에는 같은 문서의 추가 설치가 필요합니다.

```bash
uv pip install -e "./akv/agent[tokenization]"
```

전체 서버 구성은 루트 README의 다음 순서입니다. 이 명령 자체가 커밋을 고정해 clone하는 것은 아니므로, 문서의 최신 branch와 본 리뷰의 분석 SHA가 달라질 수 있다는 점은 구분해야 합니다. [루트 설치 문서](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/README.md#L29-L49)

```bash
git clone https://github.com/thu-nics/AKV.git
cd AKV
uv venv --python 3.12
source .venv/bin/activate
uv pip install -e .
```

Python 범위는 매니페스트상 **3.12 이상 3.13 미만**이고 루트 uv 환경은 Linux로 제한합니다. Rust/Cargo 설치 절차도 문서에 있으며, Drop/Repos는 서버 시작 warmup 때 Context CPU kernel을 컴파일하므로 **C++20 compiler와 쓰기 가능한 compilation cache**가 필요합니다. Python만 설치된 가벼운 클라이언트 환경을 전체 서버 환경으로 생각하면 안 됩니다. [매니페스트](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/pyproject.toml#L5-L19), [서버 환경 문서](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/README.md#L5-L23)

### 7.2 SGLang 패치와 빌드는 설치의 일부입니다

`_build.py`는 임의의 최신 SGLang을 가져오지 않습니다. 매니페스트에 고정한 upstream commit **`94602c9c2b7cbdb8efd5c52802dac6a1c180089e`**의 소스 archive를 받고, 원본 Git tree와 패치 SHA-256을 검사합니다. 이어 `sglang.patch`와 overlay Python 파일을 적용한 tree를 확인한 다음 패키징 메타데이터를 조정합니다. [고정 정보](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/pyproject.toml#L30-L35), [prepare 구현](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/_build.py#L102-L173)

이 과정은 생성한 SGLang 소스의 임의 수정이나 잘못된 editable mapping도 감지하려고 합니다. 다만 코드에 검증 로직이 있다는 것과 실제 네트워크·컴파일·GPU 환경에서 설치가 성공한다는 것은 별개입니다. 빌드는 SGLang에 `setuptools.build_meta`, router에 `maturin`을 위임합니다. 즉 Python 정책뿐 아니라 Rust gateway와 native runtime 경계도 포함된 배포입니다. [기존 tree 검사](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/_build.py#L70-L99), [native backend 위임](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/_build.py#L176-L204)

### 7.3 서버를 띄운 뒤 최종 요청에 정책을 적용합니다

루트 Quick Start는 GPT-OSS-120B를 다음처럼 띄웁니다. 모델 파일 경로는 문서의 자리표시자이며, `--tp-size 2`는 이 예시의 tensor parallel 설정입니다. 이를 모든 모델에 필요한 GPU 개수나 실제 메모리 요구량으로 일반화하지 않습니다. [서버 실행 예시](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/README.md#L51-L66)

```bash
python -m akv.system.launch_server \
  --model-path /path/to/gpt-oss-120b \
  --reasoning-parser gpt-oss \
  --tool-call-parser gpt-oss \
  --tp-size 2 \
  --port 8000
```

하네스 쪽 연결 지점은 **모든 메시지와 도구를 직렬화한 직후, HTTP 전송 직전**입니다. 다음 코드는 Quick Start의 실제 정책 설정을 발췌한 것으로, 앞서 정의한 `payload`를 입력으로 받습니다. [정책 예시](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/README.md#L114-L119)

```python
policy = CachePolicy(
    trigger=TurnTrigger(),
    selector=TurnSelection(1),
    reposition=TurnReposition(after=2, every=2),
)
akv_payload, cache_operation_history = policy.process(payload, api_style="sglang")
```

처음 한 번의 예시와 달리 실제 다중 호출 루프에서는 반환된 `cache_operation_history`를 다음 호출에 전달해야 합니다. 하네스가 tool schema와 handler를 등록하고, 모델 응답의 tool calls를 실행하며, 모든 결과를 원본 이력에 추가하는 책임도 그대로 유지합니다. AKV를 연결했다고 에이전트 실행기 전체가 교체되는 것은 아닙니다.

원문의 배송 기록 데모는 이 역할 분리를 한 파일에서 보여줍니다. 아래 명령은 서버가 준비되어 있다고 가정한 문서 예시이며, 여기서 실행하지 않았습니다. [데모 사용법](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/README.md#L225-L240)

```bash
python examples/demo.py \
  --base-url http://localhost:8000/v1 \
  --model gpt-oss-120b \
  --output local/demo-tool-01
```

데모는 임의의 업무 시스템 대신 연쇄 배송 기록을 따라 최종 위치를 찾습니다. 단계별 before/after payload와 operation history, 호출 trace를 남기므로 “모델이 삭제를 요청했는가”, “정책이 어떤 지시를 보냈는가”, “다음 응답의 usage가 무엇인가”를 분리해 읽는 학습용 진입점입니다. 이 저장소를 그대로 설치하면 외부 배송 API나 임의 도구가 자동 연결된다고 해석하면 안 됩니다. [데모 입력과 기록](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/examples/demo.py#L89-L185)

## 8. 적용 전에 확인할 제약과 문서의 경계

### 8.1 OpenAI-compatible은 일반 호스팅 API의 KV 제어를 뜻하지 않습니다

AKV는 익숙한 `/v1/chat/completions` 형식을 사용하지만, `drop_message`와 `reposition`을 해석하는 쪽은 **AKV의 custom SGLang 서버**입니다. 클라이언트에서 같은 JSON을 만든다고 다른 제공자의 API에 해당 기능이 생기는 것은 아닙니다. 메서드 이름이나 OpenAI SDK 사용 여부보다, 요청을 받는 추론 backend가 이 확장을 구현했는지가 결정적입니다. [공개 protocol 필드 추가](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/sglang.patch#L1155-L1176), [서버 launch 위임](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/launch_server.py#L1-L7)

### 8.2 모델 지원표와 실제 admission 검사를 함께 읽어야 합니다

지원 아키텍처는 Qwen 계열, GPT-OSS, MiniMax-M2 계열로 제한됩니다. Qwen이라는 이름이 같아도 임의의 새 아키텍처·멀티모달 모델을 모두 지원한다는 뜻은 아닙니다. `capabilities.py`는 모델 architecture 문자열을 allowlist와 대조하고 추가 조건을 검사합니다. [지원 검사 전체](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/sglang/srt/context_system/capabilities.py#L10-L91)

| 항목 | 고정 커밋에서 확인한 조건 |
| --- | --- |
| KV 페이지 | `page_size=1` |
| 모델·KV 형식 | text-only 모델 실행 FP16/BF16, KV는 비양자화 FP16/BF16 |
| attention backend | prefill과 decode 모두 `triton`, `flashinfer`, `fa3` 지원 경로 |
| 병렬화 | TP 가능, PP·CP·DCP는 제외 |
| 생성·캐시 기능 | speculative decoding, LoRA, HiCache, external/session cache, beam search 등 제외 |
| PD 분리 | Mooncake만 지원; staging buffer, KV offload, checksum mode 제외 |
| 모델별 추가 검사 | MiniMax는 full attention·유효한 even partial RoPE 조건, DualChunk RoPE 제외 |

이는 Context 요청의 조건입니다. README도 모델 시작 자체를 이 목록으로 제한하는 것은 아니며, 지원하지 않는 **Context 요청**을 API에서 거부한다고 설명합니다. 또한 “원래 SGLang이 지원하는 기능”과 “AKV Context 연산을 함께 켰을 때 가능한 기능”은 다릅니다. [서버 문서](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/README.md#L111-L123)

### 8.3 원본 기록과 캐시의 수명은 다릅니다

API는 세션 ID에 대화 전체를 맡기는 형식 대신 매번 원본 메시지와 누적 지시를 보냅니다. 하지만 서버 내부에는 실제 KV와 prefix cache 상태가 있습니다. “stateless API”라는 문서 표현을 서버에 캐시 상태가 전혀 없다는 뜻으로 받아들이면 안 됩니다. 클라이언트의 operation history는 GPU 캐시 적중을 보장하지도 않습니다. [상태 직렬화](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/agent/policies/utils/request.py#L91-L107), [캐시 복구 계획](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/sglang/srt/context_system/recovery.py#L253-L391)

따라서 에이전트 분기, 실패·재시도, 모델·템플릿 변경 시 어떤 이력을 채택할지는 하네스 설계의 일부입니다. `send_chat_request`는 이를 자동 관리하지 않습니다. 또한 Drop을 호출해도 원본 JSON·하네스 기록·선택적 trace 파일에서 내용이 지워지는 것은 아닙니다. cache pruning을 저장 데이터의 삭제나 보안 경계로 오해하지 않아야 합니다.

### 8.4 문서 예시에서 실제 동작을 대조한 부분

루트 README의 A·B 예시는 0~4의 다섯 메시지인데, 표 설명에 “four messages”라는 문구가 남아 있습니다. 서버 README의 네 메시지 예시는 마지막 ID가 3인데 “message 4를 처리하기 전”이라고 설명합니다. 이 리뷰에서는 그 번호를 그대로 답습하지 않고, **지정한 trigger 메시지를 처리한 뒤, 다음 query에 앞서 적용한다**는 필드 정의와 compiler의 삽입 위치를 기준으로 설명했습니다. [루트 표](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/README.md#L198-L216), [서버 예시](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/README.md#L77-L108), [compiler](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/sglang/srt/context_system/planner.py#L141-L196)

이 번호상의 오류와 별개로 더 실질적인 주의점은 재사용 설명의 범위입니다. README가 강조하는 것은 남은 KV의 재활용이지만, 구현에는 소유권 복사와 메모리 소실 후 복구 query가 있습니다. 이를 “항상 무재계산”이나 “Reposition은 비용이 없다”로 확대하면 코드와 맞지 않습니다. 이 글에서는 설치 성공, 처리량, 정확도 유지율을 정적 분석으로 입증했다고 주장하지 않습니다.

### 8.5 라이선스

루트 `LICENSE`와 system의 `LICENSE`, 패키지 매니페스트는 **Apache-2.0**을 표시합니다. 한편 일부 SGLang overlay 파일에는 MIT license header가 남아 있습니다. 재배포 시 루트 라이선스만 확인하고 기존 파일의 고지나 upstream 조건을 제거해서는 안 됩니다. 별도로 내려받는 모델의 가중치 라이선스까지 이 레포의 Apache-2.0이 부여하는 것은 아닙니다. [루트 라이선스](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/LICENSE#L1-L25), [system 라이선스](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/LICENSE#L1-L25), [IR의 MIT 고지](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/sglang/srt/context_system/ir.py#L1-L21)

## 9. 이 글에서 다루지 못한 부분

agent의 요청 파싱·정책 조합·operation history·캐시 도구·HTTP/SSE와, 서버의 message-drop 이벤트 컴파일·구조화된 캐시 키·occurrence 소유권·복구·RoPE 위치 변환을 중심으로 읽었습니다. 다음 범위는 전체 구현을 추적하거나 실행 검증하지 않았습니다.

- **PD 전송 전체:** `context_transfer.py`와 Mooncake·Rust gateway 패치의 모든 장애 복구·동시성 경로.
- **고급 삭제 규칙:** `text_drop`, `keep_text_drop`, `thinking_drop`의 전체 매칭 알고리즘과 모델별 조합.
- **모델별 파서·토큰 계수기:** GPT-OSS/Harmony, MiniMax, 일반 Jinja의 모든 template 조합과 경계 조건.
- **kernel·캐시 통합 전체:** CPU C++ event compiler와 Triton·FlashInfer·FA3 각각의 수치적 일치, 모든 eviction·abort·retry 경로.
- **성능과 정답 품질:** GPU 실측, 장시간 부하, 외부 하네스 연동, 논문 실험의 재현.

## 10. 정리

AKV를 이해하는 중심은 **원본 대화, 캐시 연산 이력, 실제 KV 버전, GPU 슬롯을 분리해 보는 것**입니다. agent는 최종 요청에 Drop과 Reposition 결정을 덧붙이고, system은 메시지별 토큰 소유권과 이벤트를 컴파일해 호환되는 KV를 재사용합니다. 필요한 경우에는 캐시를 복구하거나 별도 슬롯으로 복사하고, Reposition에서는 K의 위치 회전을 바꾸어 다음 attention을 이어갑니다.

이 설계는 문맥을 줄이는 정책만으로 해결되지 않는 시스템 문제를 드러냅니다. “덜 기억한다”는 선택을 실제 추론 효율로 연결하려면, 어떤 정보가 이후 계산에 보이는지뿐 아니라 그 KV가 어떤 연산 이력과 위치에서 만들어졌고 누가 소유하는지도 함께 관리해야 합니다. AKV의 학습 가치는 그 연결을 에이전트 정책에서 serving·cache·kernel까지 코드로 드러낸 데 있습니다.
