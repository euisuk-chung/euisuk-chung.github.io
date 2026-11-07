---
type: "Repo Review"
title: "[Repo Review] rTaste: 연구 에이전트의 실험 선택을 등록·예측·재실행으로 평가하기"
description: "연구 에이전트가 등록한 실험과 확률·순위를 고정한 뒤 GPU 재실행, 모델 감사, 공개 데이터 집계로 연구 판단을 평가하는 rTaste의 구현과 재현 경계를 추적합니다."
date: "2026-11-03"
tags:
  - "Repo Review"
  - "AI Agent"
  - "NLP"
  - "머신러닝"
  - "데이터분석"
resource: "https://github.com/ArtKanke/rTaste/tree/641f2c6d23ce50da59f57e1bb36220cc98d38146"
generated:
  by: "process:blog-review"
  at: "2026-11-03T06:13:05+09:00"
sources:
  - id: "artkanke/rtaste"
    resource: "https://github.com/ArtKanke/rTaste/tree/641f2c6d23ce50da59f57e1bb36220cc98d38146"
    title: "rTaste: Do Research Agents Have Taste? Evaluating Early Stage Research Judgment"
    author: "Art Kanke"
status: "stable"
year: "2026"
analyzed_at: "2026-11-03T06:13:05+09:00"
source_id: "artkanke/rtaste"
source_revision: "641f2c6d23ce50da59f57e1bb36220cc98d38146"
source_title: "rTaste: Do Research Agents Have Taste? Evaluating Early Stage Research Judgment"
source_type: "repo"
source_url: "https://github.com/ArtKanke/rTaste/tree/641f2c6d23ce50da59f57e1bb36220cc98d38146"
visual_sources:
  - path: "/img/reviews/2026/rtaste-repo-review/01-overview.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/run.py#L130-L322"
    caption: "제안·실행·감사·리뷰·공개 자료의 명령 경계. 리뷰어 작성, 분석 커밋 기준."
  - path: "/img/reviews/2026/rtaste-repo-review/02-execution.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/execute.py#L317-L430"
    caption: "제출물에서 기존 결과를 지우고 새 머신의 통계량을 채택하는 경로. 리뷰어 작성, 분석 커밋 기준."
  - path: "/img/reviews/2026/rtaste-repo-review/03-evidence-data.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/analysis/build_dataset.py#L203-L309"
    caption: "감사와 후속 리뷰를 공개 라벨·예측·비용 자료로 합치는 흐름. 리뷰어 작성, 분석 커밋 기준."
---

## 들어가며

연구 에이전트가 그럴듯한 실험 계획을 쓴다는 사실과, 실제로 해 볼 가치가 있는 실험을 고른다는 사실은 다릅니다. rTaste는 이 차이를 **결과를 보기 전의 판단**으로 측정하려는 평가 하네스입니다. 한 논문에서 출발해 다섯 개의 최소 실행 실험(minimum viable experiment, MVE)을 등록하고, 각각의 결과를 확률로 예측하며, 연구 가치에 따라 순위를 매깁니다. 이후 별도의 실행자가 **꼴찌까지 다섯 개 모두** 구현하고, 다른 모델들이 실제 증거를 평가합니다. 선택한 한 개만 실행하면 알기 어려운 “정말 더 나은 실험을 골랐는가”를 비교할 수 있는 구조입니다. 이는 [README가 설명하는 연구 목적과 설계](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/README.md#L5-L33)입니다.

이 글은 Art Kanke의 저장소를 커밋 [`641f2c6d23ce50da59f57e1bb36220cc98d38146`](https://github.com/ArtKanke/rTaste/tree/641f2c6d23ce50da59f57e1bb36220cc98d38146)에 고정하여 정적으로 분석한 리뷰입니다. 모델 호출, GPU 작업, 설치, 테스트 및 분석 스크립트를 실행하지 않았습니다. 따라서 아래 결과는 저장소가 공개한 자료의 수치이고, 코드 설명은 읽은 구현의 동작 경로입니다. 실제 재실행 성공이나 외부 서비스의 현재 제공 조건을 확인한 결과로 해석하시면 안 됩니다.

## 무엇을 입력받고 무엇을 남기는가

rTaste의 출발점은 실험을 확장할 **기준 논문(seed paper)**의 arXiv ID입니다. `rtaste.run`은 논문의 텍스트와 페이지 이미지, 연결된 코드 저장소, 실행을 시작한 날짜를 준비합니다. 여섯 제안 모델마다 단독 연구자(single researcher, SR)와 연구팀(research team, RT)을 구성하므로 한 논문에 열두 조건이 생깁니다. 제안 모델의 식별자는 `astra`, `fable`, `opus`, `sol`, `luna`, `muse`이며, 정확한 API 모델명은 이 커밋의 `MODELS` 사전에 들어 있습니다. 이 명칭과 가격표는 분석 커밋에 저장된 설정입니다. [조건 구성](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/run.py#L31-L35), [모델 사전](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/models.py#L52-L64)

| 경로 | 입력과 책임 | 남기는 주요 결과 |
|---|---|---|
| `rtaste/run.py` | 명령 분기, 단계 연결, 저장·재개, 조건별 작업 분배 | `runs/<seed>/`의 단계별 JSON |
| `rtaste/tools.py` | arXiv 검색·읽기, 논문 텍스트·이미지, 기준 레포 읽기 | 다운로드 캐시, 논문 해시, 도구 응답 |
| `rtaste/models.py` | 모델별 API 차이, 대화·도구 호출, 응답 검사·비용 기록 | 대화 기록, `runs/spend.jsonl` |
| `rtaste/propose.py`, `predict.py` | 다섯 등록안, 확률 예측·순위, 두 차례 commitment | 제안·예측 JSON과 SHA-256 |
| `rtaste/execute.py` | 실험 구현과 새 GPU 머신에서의 재실행 | 제출·평가 압축 파일, 통계량·사건 발생 여부 |
| `rtaste/audit.py` | 신규성, 충실성·타당성·연구 가치, 후속 리뷰 | 모델별 판정·가치 순위·리뷰 |
| `analysis/` | 실행 기록을 공개 자료로 변환하고 표를 계산 | CSV·JSONL, 표준 출력의 표·수치 |

이 모듈 관계는 [진입점의 import와 명령 분기](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/run.py#L26-L35), [자료 생성의 진입점](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/analysis/build_dataset.py#L486-L511), [표 출력의 진입점](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/analysis/tables.py#L646-L652)에서 확인할 수 있습니다. 문서와 프롬프트도 입력의 일부이므로 Python 파일만으로 평가 설계가 완결되지는 않습니다.

![제안부터 공개 자료까지 이어지는 rTaste의 네 단계]({{ '/img/reviews/2026/rtaste-repo-review/01-overview.svg' | relative_url }})

*그림 1. 리뷰어 작성, 분석 커밋 기준. 명령과 저장 경계만 나타낸 개요입니다. 근거: [제안 및 사전 측정](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/run.py#L130-L222), [실행·감사](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/run.py#L226-L322), [후속 리뷰](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/run.py#L394-L420), [공개 자료 생성](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/analysis/build_dataset.py#L486-L511).*

## 작동 원리: 제안과 사전 판단

### 1. 논문·코드·시점을 한 번 정합니다

`start_seed`는 `seeds/shortlist.json`에서 ID를 찾고, 연결된 코드 레포를 shallow clone한 뒤 전체 커밋을 기록합니다. `seed.json`에는 논문 ID·제목·레포 URL·커밋, 시작 날짜, 실행 순서, 하네스 코드 버전, 논문 텍스트와 PDF의 SHA-256 및 페이지 수를 저장합니다. 논문 ID는 캐시를 통해 읽고, 페이지는 폭 980픽셀의 JPEG로 만들어 제안 모델에 제공합니다. [기준 입력 고정](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/run.py#L108-L127), [페이지와 해시](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/tools.py#L138-L159)

이후 같은 논문 작업을 다시 시작하면 논문 해시와 코드 버전을 비교합니다. `rtaste/`, `prompts/`, `seeds/`의 미커밋 변경을 거부하고, 진행 중인 작업의 코드가 달라지면 중단합니다. `--new-code`로 계속할 때는 `code_changes.jsonl`에 변화를 남깁니다. 다만 버전 검사 범위는 위 세 디렉터리이며, 의존성이나 외부 서비스까지 하나의 불변 환경으로 묶지는 않습니다. [버전 검사 범위와 재개 규칙](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/run.py#L65-L95)

문헌 도구는 arXiv로 제한됩니다. 검색은 시작 날짜까지의 제출일을 조건에 넣고, 읽기는 최초 공개일이 시작일보다 늦으면 거부합니다. 최신 수정일이 시작일보다 뒤라면 **v1**을 읽습니다. 이는 시간 경계를 두려는 구현이지만, “시작일 당시 존재하던 가장 최신 중간 버전”을 찾아 주는 로직은 아닙니다. 기준 논문 자체는 버전 없는 URL에서 얻은 텍스트·PDF의 해시로 동일성을 추적합니다. [검색의 날짜 조건](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/tools.py#L103-L114), [본문 읽기의 버전 선택](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/tools.py#L162-L171)

`repo_ls`와 `repo_read`는 지정 레포 안으로 해석되는 경로만 허용하며, 제안자에게 셸 실행 도구는 주지 않습니다. 텍스트는 한 번에 24,000자, Parquet는 다섯 행씩 읽습니다. 따라서 이 단계의 외부 정보 경로는 논문 검색·읽기와 기준 레포 읽기로 명시되어 있습니다. [도구의 경로·읽기 제한](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/tools.py#L180-L228), [제안자 도구 목록](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/tools.py#L260-L278)

### 2. SR과 RT는 같은 최종 등록 형식으로 합류합니다

SR은 하나의 `Chat`에서 논문을 읽고, 검색하기 전의 이해와 고려 방향을 기록한 뒤, 문헌·코드 도구를 사용해 다섯 등록안을 만듭니다. 처음 이해를 적는 동안에는 도구 이름이 있어도 실행 함수가 “아직 사용할 수 없음”을 반환합니다. 제안 이후 같은 대화가 예측까지 이어집니다. [검색 전 단계](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/propose.py#L137-L144), [단독 연구자](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/propose.py#L147-L165)

RT는 같은 제안 모델의 별도 대화 두 개가 독립적으로 초안을 만들고, 비평자(critic)가 두 초안을 검토한 뒤, 책임자(lead)가 최종 다섯 개를 등록합니다. 두 제안자는 각각 최대 30회 호출, SR은 60회 호출을 기준으로 도구 사용을 마무리합니다. 팀은 60달러의 `Budget`을 공유하며, 각 제안자의 초안 단계에는 팀 한도의 35%라는 별도 기준도 둡니다. 비평자와 책임자의 `Chat`에는 검색 도구가 전달되지 않습니다. 따라서 RT는 네 역할이 모두 자유롭게 검색하는 구조가 아니라, 두 제안자가 수집한 초안을 비평·통합하는 구조입니다. [호출·예산 상수](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/propose.py#L19-L23), [연구팀 구현](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/propose.py#L168-L219)

최종 `Registration`에는 제목, 기준 논문과의 연결, 가설, 기여, 가장 가까운 선행연구, 입력, 방법, 사건, 평가 절차, 자원과 후속 대규모 연구가 들어갑니다. `Event`는 통계량 하나와 비교 관계·임계값을 갖습니다. `greater`, `less`는 엄격한 부등호이며, `within`만 양 끝을 포함합니다. 다음은 실제 구현의 연속된 원문입니다.

```python
    def occurred(self, value: float) -> bool:
        if self.relation == "greater":
            return value > self.threshold
        if self.relation == "less":
            return value < self.threshold
        return self.threshold <= value <= self.upper_threshold
```

출처: [`rtaste/propose.py` 49–54행](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/propose.py#L49-L54).

`check_registrations`는 Pydantic으로 필수 필드와 유한한 사건 임계값을 검사하고, 원시 출력 경로, 0분 초과·35분 이하의 예상 실행 시간, 중복 제목과 다섯 개라는 개수를 점검합니다. 여기서 말하는 feasibility check는 **작성된 등록 형식과 일부 제약의 검사**입니다. 모델이 실제 8B 이하인지, 데이터가 내려받아지는지, 실험이 35분 안에 끝나는지까지 실행해서 판정하지는 않습니다. [등록 스키마와 검사](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/propose.py#L29-L83), [검사 함수](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/propose.py#L99-L130)

### 3. 등록과 예측을 서로 다른 commitment로 묶습니다

첫 번째 commitment는 다섯 등록안과 실행 한계 프롬프트를 저장합니다. 이후 제안자는 자신의 기존 문맥에서 각 사건의 발생 확률과 연구 가치 순위를 냅니다. 예측 단계에서는 제안자가 도구를 요청해도 닫혔다는 응답만 받습니다. 별도로 여섯 모델을 새 문맥의 판정자(judge)로 호출합니다. 새 판정자는 논문 텍스트·페이지, 등록안과 실행 한계를 보지만 제안자의 대화나 추론 과정은 받지 않고, 도구도 없습니다. [두 commitment의 구성](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/predict.py#L69-L85), [제안자와 새 판정자의 예측](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/predict.py#L92-L112)

예측 스키마는 확률이 0~1이고, 확률 목록과 순위가 모두 실험 번호 1~5를 정확히 한 번 포함하도록 검사합니다. `ranking`은 **연구할 가치의 순서**이며 사건 발생 확률의 내림차순일 필요가 없다고 프롬프트가 명시합니다. 가설이 맞을 가능성과, 틀렸을 때도 배울 것이 있는 실험의 가치는 다른 판단입니다. [예측 스키마](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/predict.py#L22-L42), [확률과 순위의 정의](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/prompts/prediction_format.md#L3-L10)

```python
    return commit({"first_commitment": first["sha256"], "agent": agent["predictions"],
                   "judges": {judge["judge"]: judge["predictions"] for judge in judges}})
```

출처: [`rtaste/predict.py` 80–81행](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/predict.py#L80-L81). 첫 commitment의 해시를 두 번째 내용에 넣으므로 두 기록이 연결됩니다.

해시는 정렬된 키와 일정한 구분자의 JSON에서 계산합니다. 실행·감사·자료 생성이 사용하는 `commitments`는 두 내용의 해시와 첫 해시 참조가 맞는지 검사합니다. 이는 저장 후의 불일치를 찾는 장치입니다. 로컬 파일의 내용과 해시, 시각을 함께 다시 쓸 수 없게 만드는 외부 등록소나 서명까지 구현한 것은 아닙니다. 따라서 이 저장소의 사전 등록은 하네스가 유지하는 절차와 기록으로 이해하는 것이 정확합니다. [해시·기록](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/predict.py#L45-L58), [연결 검증](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/run.py#L98-L105)

### 4. 실행 전에 신규성과 흔한 후속 실험을 따로 측정합니다

여섯 모델은 논문만 보고 검색 없이 각 열 개의 후속 실험을 적습니다. 하네스는 모델명을 지운 60개 항목의 목록으로 합칩니다. `opus`, `sol`은 각 등록안을 문헌과 비교하여 `equivalent`, `close variant`, `unknown`, `distinct` 중 하나로 판정하고, 후속 실험 목록의 어느 항목과 같은지도 판단합니다. 신규성의 합성 규칙은 두 판정 중 덜 새로운 쪽을 택하므로, 공개 자료의 `new`는 두 모델 모두 `distinct`일 때만 참입니다. [사전 후속 목록·통합](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/audit.py#L106-L121), [신규성 판정](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/audit.py#L74-L103), [목록 매칭](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/audit.py#L124-L148)

명령 이름만 보면 놓치기 쉬운 부분입니다. README의 실행 예시에서는 `audit` 옆에 신규성과 후속 실험을 적어 놓았지만, 실제 호출은 `propose` 안의 `measure`에 있습니다. `measure`가 새 판정자의 예측, 신규성, 목록 매칭 파일을 저장한 뒤 두 번째 commitment를 만듭니다. 거부도 파일로 기록된 응답이면 단계가 완료될 수 있고, 유효한 예측이 없는 판정자는 `None`으로 commitment에 포함됩니다. 다만 두 번째 commitment의 **해시 내용**은 첫 해시와 예측들이며, 신규성·목록 매칭 자체는 별도 파일입니다. [README의 명령 설명](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/README.md#L74-L78), [실제 사전 측정과 완료 조건](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/run.py#L165-L189), [누락 예측의 표현](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/predict.py#L75-L81)

새 판정자와 사후 가치 순위 판정자에게는 등록 순서를 그대로 보여 주지 않습니다. `shuffled`는 논문·조건·역할·모델을 포함한 독자 식별자와 실험 번호의 해시로 제시 순서를 정합니다. “첫 번째에 적힌 실험”을 선호해서 좋은 순위를 내는 효과를 줄이려는 코드입니다. 그러나 실험 번호 자체는 남으며, 제안자의 첫 선택과 처음 작성한 안을 별도로 비교하는 분석도 유지됩니다. 순서 조작과 비교 기준을 함께 읽어야 합니다. [순서 변경](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/predict.py#L61-L66), [사후 가치 순위](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/audit.py#L358-L368), [첫 작성안 비교](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/analysis/tables.py#L448-L473)

## 작동 원리: 구현, 재실행, 감사

### 5. 모든 조건이 준비되어야 실험을 시작합니다

`execute_seed`는 열두 조건을 확인합니다. 제안 기록이 없거나, 제안은 완료됐는데 두 번째 commitment가 없으면 실행을 중단합니다. 제안 과정에서 거부된 조건은 실행 대상에 넣지 않습니다. 정상 조건에서는 commitment의 등록 순서대로 다섯 개를 작업 목록에 넣으며, 예측 순위에 따른 선별은 없습니다. 기본 병렬도는 MVE 16개이고, 머신 시작은 세마포어로 동시에 네 개까지만 허용합니다. `execute <seed> 2`라는 리허설용 인자는 각 조건의 **등록 순서상 앞 두 개**만 실행하도록 합니다. [실행 게이트와 작업 목록](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/run.py#L245-L265), [병렬도](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/run.py#L31-L34), [머신 시작 제한](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/execute.py#L38-L41)

첫 실행자는 `opus`와 `sol` 중 기준 논문 실행 순서와 제안 모델의 위치로 번갈아 배정됩니다. 한 실행자가 끝내 전달하지 못하면 다른 실행자가 독립적으로 한 번 더 시도합니다. 앞 시도의 결과가 전달되면 다음 시도는 하지 않습니다. 여기서 별도 실행자라는 말은 **다른 문맥과 역할**을 뜻합니다. 배정 공식은 제안자와 같은 모델이 구현하는 경우도 허용하며, 감사자 세 모델 중 둘도 실행자 모델과 겹칩니다. [최대 두 시도](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/run.py#L226-L242), [실행자 배정](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/execute.py#L433-L436), [감사자 구성](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/audit.py#L29-L30)

![실험 구현과 새 머신 재실행의 입력 및 출력]({{ '/img/reviews/2026/rtaste-repo-review/02-execution.svg' | relative_url }})

*그림 2. 리뷰어 작성, 분석 커밋 기준. 구현자의 시험 결과를 지우고 새 머신에서 낸 값을 채택하는 경로입니다. 미전달일 때 다른 실행자로 넘어가는 조건은 [두 시도 제어](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/run.py#L226-L242), 파일과 결과의 경계는 [구현·평가](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/execute.py#L317-L430)를 근거로 했습니다.*

### 6. 실행자는 코드와 제출 명령을 만듭니다

실행자에게는 논문 텍스트·페이지와 **해당 등록안 하나**를 전달합니다. 도구는 기준 코드 읽기, 머신의 파일 쓰기·읽기, 셸 명령 실행, `submit`입니다. 머신은 처음 필요할 때 생성하고, 기준 레포의 고정 커밋 tarball을 `/workspace/seed`에 배치합니다. 제출할 때는 작업 디렉터리를 `submission.tar.gz`로 보존한 뒤 머신을 중지하고, 새 머신에서 수행할 `evaluation_command`와 변경 사항을 적은 `notes`를 저장합니다. [머신 준비](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/execute.py#L80-L118), [도구와 제출](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/execute.py#L223-L314), [실행자 입력](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/execute.py#L317-L355)

프롬프트의 공통 실험 조건은 80GB A100 한 개, 머신 45분, 구현 전체 90분, 재실행 35분, 8B 이하 공개 모델입니다. 구현자 모델의 호출은 60회·6달러가 기준이며, 기준 코드·패키지·캐시·200MB를 넘는 파일은 제출물에서 제외하고 제출 압축 파일은 1GB를 넘으면 미전달로 처리합니다. 머신을 기다린 시간은 구현 시간에서 뺍니다. 이 제한들은 코드의 호출·시간·크기 검사와 프롬프트의 실험 규칙이 함께 구성합니다. [실험 한계 프롬프트](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/prompts/envelope.md#L1-L8), [실행 상수](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/execute.py#L26-L37), [시간·제출 검사](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/execute.py#L236-L290), [파일 제외](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/execute.py#L164-L181)

여기에는 문서와 현재 설정의 차이도 있습니다. 이 커밋의 실제 `FLAVOR`는 `h200`이고 분당 비용도 시간당 5달러에서 계산하지만, 제안·실행자 프롬프트에는 A100이 적혀 있습니다. 자료 설명은 기준 논문 7에서 60개 중 53개 MVE를 H200으로 구현·재실행했고 나머지는 A100이었다고 밝힙니다. 따라서 코드를 그대로 실행하면 전체 연구의 과거 머신 구성이 자동으로 재현된다고 보기 어렵습니다. 이는 GPU 성능 차이를 새로 측정했다는 뜻이 아니라, 설정과 기록에서 확인되는 재현 조건의 차이입니다. [현재 머신 설정](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/execute.py#L26-L34), [실행자에게 보이는 머신](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/prompts/executor.md#L15-L20), [공개 자료의 머신 이력](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/data/README.md#L85-L90)

### 7. 새 머신의 숫자와 과학적으로 믿을 수 있는 증거는 다른 단계입니다

`evaluate`는 새 머신에 제출물을 풀고, 기존 `result.json`과 등록된 원시 출력들을 지운 뒤 평가 명령을 실행합니다. 이후 새로 쓰인 파일 목록과 `evaluation.tar.gz`를 보존합니다. 구현자가 시험할 때 얻었던 값은 `executor_value`로 따로 남기고, 사건 발생 여부는 재실행의 `value`로 결정합니다. [재실행 준비와 보존](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/execute.py#L376-L418)

```python
        if result["exit_code"] != 0 or result["timed_out"]:
            record["status"], record["reason"] = "no delivery", (
                "the evaluation did not finish in time" if result["timed_out"] else f"exit code {result['exit_code']}")
        elif value is None:
            record["status"], record["reason"] = "no delivery", problem
        else:
            record["status"], record["value"] = "delivered", value
            record["event_occurred"] = Event(**registration["event"]).occurred(value)
            record["missing_raw_outputs"] = missing
```

출처: [`rtaste/execute.py` 419–427행](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/execute.py#L419-L427).

이 분기가 의미하는 전달 성공의 범위는 좁습니다. 명령이 시간 안에 정상 종료하고 `result.json`의 `value`가 불리언이 아닌 유한한 숫자이면 `delivered`가 됩니다. 프롬프트는 `statistic`도 쓰도록 하지만 `check_result`는 그 이름을 등록 통계량과 대조하지 않습니다. 원시 출력이 없더라도 위 코드에서는 `missing_raw_outputs`에 적을 뿐 전달을 실패시키지 않습니다. 따라서 **전달됨은 등록에 충실하고 타당하다는 보증이 아닙니다**. 이 차이를 다음 감사 단계가 평가합니다. [숫자 검사](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/execute.py#L358-L368), [요구하는 결과 형식](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/prompts/executor.md#L22-L26)

8B 이하 모델, 외부 호스팅 모델 API 금지, 기준 코드 읽기 전용이라는 규칙도 프롬프트에 들어 있습니다. 그러나 실행 도구는 인터넷이 있는 머신에서 셸 명령을 받아 실행하며, 이 모듈에서 모델 크기나 모든 네트워크 목적지를 강제로 차단하는 정책은 확인되지 않습니다. 이 실험 규칙을 OS 수준의 완전한 접근 통제로 읽으면 구현 범위를 넘습니다. 실제 준수 여부를 감사자가 코드와 출력으로 판정하는 구조입니다. [실행자 규칙](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/prompts/executor.md#L15-L25), [셸 도구](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/execute.py#L270-L279)

### 8. 감사와 후속 리뷰가 서로 다른 질문을 묻습니다

감사자는 `opus`, `sol`, `grok` 세 모델입니다. 개별 감사 입력은 등록안, 구현자의 메모, 재실행 명령·출력·사건 여부, 압축 파일에서 읽은 증거입니다. 감사 프롬프트는 등록과 달라진 점을 먼저 적고, 충실성(fidelity), 타당성(validity), 0~3의 연구 가치를 평가하도록 합니다. 충분한 증거가 있는 귀무 결과도 높은 가치를 받을 수 있습니다. 개별 감사 입력에는 기준 논문의 전문이 직접 포함되지 않습니다. [감사 입력 구성](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/audit.py#L213-L234), [감사 질문과 가치 척도](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/prompts/audit.md#L19-L34)

증거는 무제한으로 전달하지 않습니다. `evidence`는 코드 파일당 40,000자, 그 외 파일당 6,000자, 전체 파일 내용 240,000자를 한도로 하고, 20MB 초과 파일과 바이너리 등 읽지 못한 항목을 별도로 표시합니다. 제출 때 따라온 비코드 파일과 재실행에서 새로 쓴 파일도 구분해 앞선 시험 로그를 새 결과로 오인하지 않도록 합니다. 따라서 판정은 감사자에게 실제로 제시된 증거 범위에 의존합니다. [증거 한도](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/audit.py#L35-L38), [증거 선별과 표시](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/audit.py#L171-L210)

다섯 개의 실행과 필요한 감사가 모두 끝나면, 세 감사자가 조건 내 연구 가치 순위를 다시 냅니다. 순위를 매길 때는 제안자·실행자 모델명과 사전 예측을 주지 않으며, 등록안·전달 여부·재실행 값·감사 내용을 받습니다. 공개 자료의 `auditors_first`는 평균 가치 순위가 가장 좋은 MVE에 1을 주되 공동 1위가 k개이면 각각 1/k를 주는 값입니다. [순위 입력 준비](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/run.py#L306-L321), [평균 순위와 동점 처리](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/analysis/build_dataset.py#L203-L216), [첫 순위 지분](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/analysis/build_dataset.py#L329-L333)

`review`는 코드 주석상 연구 뒤에 추가한 단계입니다. 같은 세 모델이 이번에는 **기준 논문 텍스트**까지 받아, 논문과의 관계, 얼마나 흔한 아이디어인지, 질문에 답할 수 있는지, 전제조건과 실제 증거, 다음 조치를 평가합니다. 본문·수식·표가 텍스트로 제공되며 그림은 보이지 않는다고 프롬프트가 명시합니다. `Review` 스키마에는 두 개의 자유 서술과 아홉 개의 선택형 답변이 있습니다. `in_the_paper`와 `misreads_paper`의 인용문은 정규화한 단어열이 논문 텍스트 안에 실제 있는지 별도로 검사하지만, 인용이 판정을 논리적으로 뒷받침하는지까지 자동 증명하지는 않습니다. [후속 리뷰 실행](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/run.py#L394-L422), [리뷰 스키마·인용 검사·입력](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/audit.py#L237-L328), [리뷰의 입력 한계](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/prompts/review.md#L1-L17)

![감사·리뷰에서 공개 라벨과 통계 표로 이어지는 경로]({{ '/img/reviews/2026/rtaste-repo-review/03-evidence-data.svg' | relative_url }})

*그림 3. 리뷰어 작성, 분석 커밋 기준. 개별 증거 판정과 논문을 포함한 후속 리뷰가 별도 기록을 만들고, 자료 생성기가 이를 합칩니다. 근거: [감사](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/audit.py#L213-L234), [리뷰](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/audit.py#L308-L328), [라벨 합성](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/analysis/build_dataset.py#L203-L244), [CSV·JSONL 출력](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/analysis/build_dataset.py#L486-L511).*

## 작동 원리: 기록을 공개 자료와 평가 지표로 바꾸기

### 9. `build_dataset`은 실험을 돌리는 명령이 아닙니다

`analysis/build_dataset.py`는 일곱 기준 논문의 저장된 단계와 비용 로그를 읽고 `seeds.csv`, `conditions.csv`, `mves.csv`, `calls.csv`, `auditor_check.csv` 및 세 종류의 JSONL을 생성합니다. 모델을 호출해 새 라벨을 만드는 단계가 아니라 기존 기록을 공개 형식으로 옮기는 단계입니다. `(seed, condition, mve)`가 실험 단위 결합 키이며 CSV는 라벨·예측과 비용의 평탄한 표, JSONL은 등록안과 판정 이유의 전문을 제공합니다. [자료 생성 코드](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/analysis/build_dataset.py#L19-L38), [출력 함수와 진입점](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/analysis/build_dataset.py#L460-L511), [자료의 결합 키](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/data/README.md#L15-L32)

핵심 합성 규칙에서 특히 주의할 부분은 `audit.combined`의 기본값입니다. 함수 기본값은 감사자 중 하나라도 결함을 지적하면 보수적으로 반영하는 `any_flag=True`입니다. 그러나 **공개 자료 생성기는 `any_flag=False`를 명시**합니다. 결과적으로 `sound`는 충실성에서 적어도 두 명, 타당성에서 적어도 두 명이 긍정해야 합니다. 두 속성에 찬성한 모델 집합이 반드시 같아야 한다는 추가 조건은 없습니다. 연구 가치는 중앙값이며 한 명의 값이 없으면 남은 둘 중 낮은 값을 씁니다. [합성 함수](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/audit.py#L337-L355), [공개 라벨에 적용하는 인자](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/analysis/build_dataset.py#L203-L216)

```python
        row |= audit_columns({a: saved["audit"] for a, saved in audits.items()}, rankings, n)
        row["valuable"] = (row["research_value"] or 0) >= 2
        row["new"] = audit.novelty_label(list(novelty.values())) == "distinct"
        row["good"] = delivered and row["sound"] and row["valuable"] and row["new"]
        row["on_list"] = True in (row["on_list_opus"], row["on_list_sol"])
```

출처: [`analysis/build_dataset.py` 287–291행](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/analysis/build_dataset.py#L287-L291).

후속 리뷰의 `bno_2of3`는 “논문을 넘어섬”과 “비자명함”을 **동일한 리뷰어가 함께** 인정한 경우가 적어도 둘이어야 합니다. `beyond`는 `builds on` 또는 `new direction`, `non_obvious`는 `few` 또는 `none`이면서 논문에서 이미 보고했거나 남겨 놓은 실험임을 인용으로 보이지 않은 경우입니다. 반면 `on_list`는 실행 전 두 모델 중 하나라도 60개 목록에 매칭했는지입니다. 이 두 지표는 질문과 입력이 다르므로 논리적으로 서로의 부정이 아닙니다. [후속 리뷰 합성](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/analysis/build_dataset.py#L219-L244), [목록과 신규성의 라벨 정의](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/data/README.md#L50-L76)

### 10. 예측 점수와 순위 점수는 같은 성공률이 아닙니다

공개 자료의 사건 발생은 재실행 값과 등록된 비교 관계로 정해집니다. 확률 예측은 `sound`인 실험에서 Brier 점수로 평가합니다. Brier 점수는 예측 확률과 실제 발생 여부(0 또는 1)의 차이를 제곱한 값의 평균으로, 낮을수록 좋습니다. `build_dataset`은 조건별 점수를 만들고, `tables.py`는 조건 안에서 계산한 값을 기준 논문 안에서 평균한 뒤 일곱 논문을 평균합니다. 여섯 새 판정자의 확률을 평균한 예측과, 해당 논문을 제외한 나머지 여섯 논문의 사건 발생률을 쓰는 기준선도 코드에 있습니다. [조건별 Brier 점수](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/analysis/build_dataset.py#L363-L390), [표의 기준선](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/analysis/tables.py#L51-L61), [예측 점수 집계](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/analysis/tables.py#L213-L250)

따라서 “사건이 발생했다”는 말만으로 가치 있는 실험이라고 판정하지 않습니다. 높은 연구 가치의 귀무 결과가 있을 수 있고, 쉬운 임계값을 정해 사건이 자주 일어나도 판단의 질이 높아지는 것은 아닙니다. 실제로 등록 형식에는 신뢰구간 경계나 여러 전제조건을 하나의 숫자로 집약한 사건도 들어갑니다. 자료 생성기는 이를 키워드로 분류하고 13개 사건에는 판독에 따른 보정을 명시합니다. 예측 대상의 난이도와 사건 설계를 함께 살펴야 모델 간 확률을 해석할 수 있다는 점은 이 구조에서 나오는 리뷰어의 해석입니다. [사건 형태 분류와 보정](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/analysis/build_dataset.py#L138-L166), [가치 판정 지침](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/prompts/audit.md#L27-L32)

순위 평가는 에이전트의 첫 선택이 `auditors_first`를 얼마나 얻는지로 비교합니다. 같은 모델의 새 판정자, 처음 작성한 실험, 무작위 선택과의 비교가 각각 있습니다. README는 에이전트의 첫 선택이 무작위보다 감사자의 최상위에 더 자주 들었으나 처음 작성한 안보다 측정 가능하게 더 낫지는 않았다고 서술합니다. 이 글에서는 해당 통계 분석을 재실행하지 않았으며, 구현에서 이 비교가 실제로 어느 열을 사용하는지 추적했습니다. [README의 순위 결과 주장](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/README.md#L9-L12), [순위 비교 코드](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/analysis/tables.py#L448-L473)

## 공개 결과를 읽을 때의 분모와 조건

자료 문서는 여섯 모델 × 두 구성 × 일곱 논문으로 84개 조건을 설명합니다. 첫 논문의 `opus-single`이 제안 중 거부하여 등록이 없었고, 83개 조건에서 415개 MVE가 나왔습니다. 그중 412개가 전달됐으며, 모든 라벨은 모델 판정입니다. 다음 수치는 [고정 커밋의 자료 정의](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/data/README.md#L3-L10)와 [라벨별 수치](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/data/README.md#L50-L76)에 명시되어 있습니다. `sound`, `valuable`, `new`는 각각의 속성이므로 아래 행 전체가 차례로 줄어드는 한 줄짜리 필터를 뜻하지 않습니다.

| 수치 | 정확한 의미 |
|---|---|
| 415 | 등록된 MVE 전체 |
| 412 | 재실행에서 전달된 MVE |
| 369 | `sound`: 충실성과 타당성 각각에 두 명 이상 긍정 |
| 281 | `valuable`: 합성 연구 가치가 2 이상 |
| 296 | `new`: 두 신규성 판정자 모두 `distinct` |
| 194 | `good`: 전달됨·sound·valuable·new의 교집합 |
| 126 | 전체 MVE 중 `bno_2of3`가 참인 수 |
| 73 | 194개의 `good` 중 `bno_2of3`도 참인 수 |

따라서 “비자명한 실험은 73개”라고만 말하면 분모가 사라집니다. 73개는 품질·신규성 조건을 모두 통과한 194개 안의 부분집합이고, 전체에서 후속 리뷰의 해당 라벨을 받은 수는 126개입니다. 또한 선행연구와 다르다는 `new`와, 연구자가 먼저 떠올리기 어렵다는 비자명성은 별개로 정의되어 있습니다.

README의 SR/RT 비교는 다음과 같습니다. 첫 수치 열은 **조건당 다섯 개 중 `good`인 수의 평균**, 다음 열은 **해당 모델·구성의 전체 논문에서 `bno_2of3`인 MVE의 개수**입니다. 확률·비율과 개수를 섞어 읽지 않도록 열을 분리했습니다. [README 결과표 및 주석](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/README.md#L35-L53)

| 제안 모델 | `good` 평균 SR / RT | `bno_2of3` 개수 SR / RT |
|---|---:|---:|
| GPT-6 Astra | 2.57 / 3.29 | 21 / 21 |
| Claude Fable 5.1 | 2.43 / 2.86 | 3 / 4 |
| Claude Opus 5.5 | 3.33 / 3.14 | 2 / 8 |
| GPT-6.1 Sol | 3.00 / 3.71 | 20 / 22 |
| GPT-6 Luna | 0.71 / 2.00 | 6 / 7 |
| Muse Spark 1.3 | 0.14 / 1.00 | 5 / 7 |
| 전체 | 2.00 / 2.67 | 57 / 69 |

Opus SR의 평균은 여섯 논문·30개 MVE만의 결과입니다. 전체 `good` 평균 SR 2.00과 RT 2.67의 단순 차이는 0.67처럼 보이지만, 표의 짝지은 RT−SR 추정은 **+0.71, 95% 신뢰구간 [−0.10, 1.52]**입니다. 코드가 각 논문 안에서 여섯 모델의 차이를 평균하고, 이 비교에서는 거부한 Opus SR을 0으로 세기 때문입니다. 다른 일부 RT−SR 분석은 `refused_as_zero=False`로 그 쌍을 제외합니다. 이 구간은 415개 실험을 독립 표본으로 삼은 구간이 아니라 **일곱 기준 논문**의 평균과 표준편차에 자유도 6의 Student t 계수 2.447을 적용한 것입니다. 0을 포함하는 구간을 모든 모델에서 팀이 확실히 우월하다는 근거로 쓰면 안 됩니다. [집계·신뢰구간](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/analysis/tables.py#L23-L34), [논문 단위 평균](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/analysis/tables.py#L79-L88), [거부 조건 처리와 표 1](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/analysis/tables.py#L154-L195), [다른 짝비교의 처리](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/analysis/tables.py#L476-L490)

## 비용과 중단·재개는 어떻게 다루는가

`models.py`의 `Chat`은 OpenAI Responses 형식과 Anthropic Messages 형식을 통일하고, Meta·xAI 모델에도 설정된 OpenAI 호환 경로를 사용합니다. 사용량의 새 입력·캐시 읽기·캐시 쓰기·출력을 가격표에 곱해 비용을 계산하고, 호출 목적과 상태를 `spend.jsonl`에 씁니다. 도구 목록과 이전 대화는 이어 보내며, 출력이 잘리면 한 번 낮은 추론 노력으로 다시 요청하고, 잘못된 JSON은 최대 두 차례 수정 요청을 합니다. 거부는 다른 모델로 바꾸지 않고 결과로 남깁니다. [공급자와 클라이언트](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/models.py#L127-L138), [사용량·비용 기록](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/models.py#L254-L270), [응답 처리·가격 계산](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/models.py#L322-L359), [작업·수정 루프](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/models.py#L379-L460)

여기서 예산은 공급자 계정의 절대 지출 차단 장치가 아닙니다. `_request`는 요청 전에 남은 예산이 0 이하인지 확인하고, 비용은 응답을 받은 후 더합니다. `work`는 예산의 80% 또는 호출 기준에 도달하면 새 도구 실행을 제한하지만 마무리 응답과 제출을 허용합니다. 한 번의 긴 응답이나 공유 예산을 쓰는 동시 요청은 선언된 금액을 넘길 여지가 있습니다. 추가로 새 판정자·개별 감사 등에는 전체 연구를 포괄하는 하나의 `Budget`이 걸려 있지 않습니다. 후속 리뷰만 논문당 110달러 예산을 기존 로그에서 복구해 공유합니다. [예산 합산·선검사](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/models.py#L87-L101), [요청 후 비용 반영](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/models.py#L254-L267), [80% 마무리 규칙](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/models.py#L388-L407), [리뷰 예산](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/run.py#L394-L422)

중단 뒤 재개는 `step`이 맡습니다. 완성 JSON이 있으면 읽어 반환하고, 새 결과는 `.unfinished`에 먼저 쓴 뒤 이름을 바꿉니다. 같은 논문의 동시 실행은 파일 잠금으로 막고, 병렬 작업 하나가 예외를 내도 다른 작업은 계속하며 마지막에 실패를 알립니다. 제안과 예측 사이에서 멈추면 저장한 대화를 복원해 예측을 이어 갑니다. 다만 한 단계 도중 발생한 모든 원격 작업이 트랜잭션처럼 취소되는 것은 아닙니다. [단계 저장·실패 처리](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/run.py#L39-L62), [대화 복구](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/run.py#L150-L162), [논문별 잠금](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/run.py#L192-L204)

서비스의 일시 장애는 별도로 재시도하며, 머신·공급자·계정 문제로 구현 결과를 저장하지 않은 경우 다음 실행에서 해당 시도를 다시 합니다. 이것은 “최대 두 실행자 시도”와 다른 복구 경로라 실제 유료 호출이 더 생길 수 있습니다. GPU 실행을 재개할 때에는 같은 논문 라벨로 남은 머신을 찾아 취소하고, 종료·비용 기록 로직도 둡니다. 종료 실패 시 Jobs 화면에서 확인하라는 경고를 내는 경로가 있으므로, 코드의 취소 시도를 실제 과금 종료가 검증됐다는 뜻으로 볼 수는 없습니다. [API 재시도](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/models.py#L141-L168), [구현의 장애 분류](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/execute.py#L317-L355), [머신 종료·잔여 작업 취소](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/execute.py#L183-L216)

공개 비용에도 두 관점이 있습니다. H200 시간은 A100 요율로 정규화한 `cost`와 실제 지불한 `cost_paid`로 나뉩니다. `calls.csv`에는 장애·수동 중단으로 버렸다가 반복한 작업을 `repeated`로 표시합니다. 조건 비용과 시도별 열은 버린 작업을 제외하며, 조건 비용은 제안·자기 예측·구현·재실행을 합한 값이므로 판정·감사·리뷰까지 포함한 총 운영비와도 다릅니다. 논문별 비용은 감사자 검사 비용을 제외한 유료 로그를 합칩니다. 따라서 README의 “100달러당 좋은 실험 수”는 이 비용 정의를 전제로 한 효율 지표입니다. [비용 문서](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/data/README.md#L85-L104), [반복 작업 식별](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/analysis/build_dataset.py#L114-L135), [조건·논문 비용](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/analysis/build_dataset.py#L393-L410)

## 문서에 있는 설치와 사용 경로

패키지 매니페스트는 Python 3.12 이상을 요구합니다. 핵심 의존성은 모델 SDK, Pydantic, PDF 처리 라이브러리, Parquet 읽기, HTTP 클라이언트, Hugging Face Hub이며 `requirements.txt`에는 고정 버전 목록이 있습니다. `pyproject.toml`에서는 대부분 하한 버전이고 `huggingface_hub`는 2.1.1로 고정되어 있습니다. [매니페스트](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/pyproject.toml#L1-L14), [요구 패키지](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/requirements.txt#L1-L55)

아래는 README에 있는 명령의 연속된 원문입니다. 이 리뷰에서는 실행하지 않았습니다. 사전 준비에는 문서의 가상환경·패키지 설치와 `.env` 설정이 필요합니다.

```bash
.venv/bin/python -m rtaste.run propose 2609.29233      # proposals, forecasts and rankings of all twelve conditions
.venv/bin/python -m rtaste.run execute 2609.29233      # implement and rerun every MVE
.venv/bin/python -m rtaste.run audit 2609.29233        # novelty, obvious follow ups, audits and value rankings
.venv/bin/python -m rtaste.run review 2609.29233       # the review of every delivered MVE
.venv/bin/python -m rtaste.run status 2609.29233       # progress and cost so far
.venv/bin/python -m analysis.build_dataset runs        # turn runs/ into data/
```

출처: [README 74–79행](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/README.md#L74-L79). `audit` 주석의 신규성·후속 실험 매칭은 앞서 설명한 대로 실제로 `propose`에서 수행됩니다. `status`는 조건별 제안·commitment·전달·감사·순위 진행과 비용 로그 합계를 출력합니다. CLI는 `argparse` 대신 인자를 직접 분해하며, 명시된 명령 외에는 `status`로 들어갑니다. [상태 출력과 명령 분기](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/run.py#L425-L482)

전체 연구를 새로 수행하려면 OpenAI·Anthropic·xAI·Meta API 키와 GPU Jobs를 만들 수 있는 Hugging Face 계정이 필요하다고 README가 설명합니다. `.env.example`은 컴퓨트 토큰과 공개 gated 모델 읽기 토큰을 분리하고, 후자만 샌드박스에 전달하도록 설명합니다. 위 경로는 유료 원격 호출과 GPU 사용을 포함하므로 공개 CSV를 읽는 경로와 실행 범위가 크게 다릅니다. [실행 자격과 설치 문서](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/README.md#L55-L80), [토큰 예시 파일](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/.env.example#L1-L9), [샌드박스에 전달하는 값](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/execute.py#L83-L92)

README가 설치·API 키 없이 재현할 수 있다고 소개하는 것은 `python3.12 analysis/tables.py`로 **이미 공개된 자료에서 표와 수치를 다시 계산하는 경로**입니다. 해당 파일은 표준 라이브러리로 `data/`를 읽어 출력하도록 작성되어 있습니다. 반대로 `build_dataset`은 `rtaste.audit`와 `rtaste.run`을 가져오며 별도의 원래 실행 기록이 필요합니다. 공개 자료만으로 두 단계를 동일하게 재생할 수 있다고 설명하면 안 됩니다. [자료만으로 표 계산](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/README.md#L55-L65), [표 스크립트의 import와 읽기](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/analysis/tables.py#L15-L61), [자료 생성기의 입력](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/analysis/build_dataset.py#L19-L26)

## 한계와 재현 범위

첫째, 공개 라벨은 사람의 독립 평가가 아니라 모델 판정입니다. 실행자·감사자·리뷰어의 모델도 일부 겹칩니다. 저장소는 감사자를 점검하려고 첫 논문에서 전달된 실험 열 개의 복사본에 알려진 결함을 심고 재실행·재감사하는 경로를 제공합니다. 자료 문서는 둘 이상이 결함 복사본 10개 중 8개를 지적했고 원본은 지적하지 않았다고 보고합니다. 이는 그 점검 집합의 결과이며 모든 감사 판정의 정확도를 입증하지는 않습니다. [감사자 점검 구현](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/run.py#L325-L365), [점검 자료의 범위와 결과](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/data/README.md#L297-L313)

둘째, 공개 자료에는 등록안과 판정 전문, 예측, 비용 등은 있지만 대화 이력, 기준 논문 전문, 실행자가 만든 코드·파일, 재실행 출력은 포함되지 않습니다. 그 결과 이 커밋만으로 가능한 것은 공개 라벨의 집계·판정 이유 검토와 하네스 구현 분석입니다. 과거 실험이 실제로 등록대로 수행됐는지 독립적으로 끝까지 재감사하려면 공개 CSV·JSONL 외의 실행 증거가 필요합니다. [명시적으로 제외한 자료](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/data/README.md#L28-L32), [자료 생성기의 제외 범위](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/analysis/build_dataset.py#L1-L7)

셋째, 기준 논문은 일곱 편의 최근 NLP 논문이며 더 넓은 연구 분야 전체를 대표하도록 설계된 표본이라고 확대할 수 없습니다. 후보 문서는 일정 기간의 Hugging Face 일일 논문, cs.CL, 코드 공개와 투표를 이용한 선별 및 일부 수동 조정을 설명하고, 실제 결과의 일곱 ID는 자료 생성기에 고정되어 있습니다. 모델의 전반적인 연구 능력 순위로 일반화하기 전에 이 입력 분포와 GPU·시간·모델 크기 조건을 함께 봐야 합니다. [후보 선별 규칙](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/seeds/shortlist.json#L1-L4), [분석 대상 일곱 ID](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/analysis/build_dataset.py#L24-L29)

넷째, 모델 API 이름·가격·출력 형식과 다운로드 가능한 모델·데이터·GPU 공급 조건은 외부 서비스에 의존합니다. 논문·레포 해시와 실행 로그가 재현성을 돕지만, 설치물·모델 가중치·외부 응답까지 모두 보관하는 실험 패키지는 아닙니다. 특히 머신 구성과 A100 비용 정규화, 반복 작업 제외를 고려해야 과거 결과와 새 실행 비용을 구분할 수 있습니다. [API 설정](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/models.py#L32-L64), [머신·컨테이너 설정](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/rtaste/execute.py#L26-L35), [비용 정의](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/data/README.md#L85-L90)

라이선스도 구분됩니다. 저장소의 코드는 MIT이며 저작권·허가문 보존과 무보증 조항이 있습니다. 데이터는 README와 `data/README.md`에서 CC BY 4.0으로 명시합니다. 기준 논문과 연결된 코드의 권리는 각 저자에게 있고, 해당 원문·코드가 이 데이터 라이선스로 일괄 재허가된다고 쓰여 있지는 않습니다. [코드 라이선스](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/LICENSE#L1-L21), [코드·데이터·기준 자료의 권리 설명](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/README.md#L105-L108), [데이터 라이선스](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/data/README.md#L315-L317)

## 이 글에서 다루지 못한 부분

하네스의 공개 진입점부터 등록·예측·실행·감사·리뷰·공개 자료 생성·주요 지표 집계까지 추적했습니다. 테스트는 예측 형식·해시·순서 섞기와 머신 시작 제어의 일부를 자료로 읽었으며 실행하지 않았습니다. 각 기준 논문의 연결된 코드, 공개된 415개 등록·판정 전문 전체의 과학적 적절성, 과거 비공개 `runs/`의 실행 코드와 원시 출력, 모든 부록 통계의 수치 재계산, 실제 모델·Jobs 서비스와 패키지의 호환성은 검증하지 않았습니다. [공개 자료 제외 범위](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/data/README.md#L28-L32), [예측 테스트](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/tests/test_predict.py#L32-L74), [머신 제어 테스트](https://github.com/ArtKanke/rTaste/blob/641f2c6d23ce50da59f57e1bb36220cc98d38146/tests/test_execute.py#L20-L104)

## 정리

rTaste에서 배울 핵심은 연구 계획 생성과 연구 판단을 서로 다른 기록·평가로 연결하는 방식입니다. 등록안과 확률·순위를 먼저 고정하고, 다섯 실험을 모두 실행하며, 전달 성공·충실성·타당성·연구 가치·신규성·비자명성을 각각 보존합니다. 그 결과 “잘 실행됐다”, “예측한 사건이 일어났다”, “좋은 실험을 골랐다”라는 말을 분리해서 검토할 수 있습니다.

이 구조의 신뢰 범위도 구체적입니다. 로컬 commitment는 기록의 불일치를 탐지하고, 새 머신 재실행은 제출 때 남은 결과와 평가 출력을 분리하며, 모델 감사와 후속 리뷰는 그 증거를 제한된 문맥에서 해석합니다. 415개 중 194개와 그 안의 73개라는 결과는 이 서로 다른 판정 규칙과 조건을 함께 읽을 때 의미가 분명해집니다.
