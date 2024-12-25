---
title: "[SPL] stats와 eventstats 차이점 이해하기"
date: "2023-05-08"
tags:
  - "splunk"
  - "개념정리"
year: "2023"
---

# [SPL] stats와 eventstats 차이점 이해하기

원본 게시글: https://velog.io/@euisuk-chung/SPL-stats와-eventstats-차이점-이해하기



stats와 eventstats 차이점 이해하기
--------------------------

Splunk에서 데이터를 분석하다 보면, 다양한 명령어를 사용하여 데이터를 집계하고 요약해야 할 때가 있습니다. 이러한 상황에서 자주 사용되는 두 가지 명령어가 stats와 eventstats입니다. 이 글에서는 이 두 명령어의 차이점과 사용법에 대해 알아봅니다.

### stats

`stats` 명령어는 결과를 집계한 후, 최종 집계된 결과만 출력합니다. 원본 이벤트를 유지하지 않으며, 각 그룹별로 한 개의 결과 레코드만 생성합니다. 일반적으로 데이터를 요약하거나 결과를 그룹화할 때 사용됩니다.

예제:

```
index=my_app_index sourcetype=error_logs
| stats count by error_type
```
### eventstats

`eventstats` 명령어는 stats와 유사한 집계 작업을 수행하지만, 원본 이벤트를 유지하고 각 이벤트에 집계 값을 추가합니다. 이를 통해 원본 이벤트와 함께 통계 정보를 확인할 수 있습니다. 이 명령어는 각 이벤트에 대한 컨텍스트를 제공하거나 이벤트를 필터링할 때 유용합니다.

예제:

```
index=my_app_index sourcetype=error_logs
| eventstats count by error_type
```

이 쿼리는 오류 유형별로 발생한 오류의 개수를 계산하되, 원본 이벤트를 유지하고 각 이벤트에 계산된 개수를 추가합니다. 결과 테이블은 원본 이벤트와 함께 오류 유형별 개수를 포함합니다.

### 결론

stats는 집계된 결과만 출력하는 반면, eventstats는 원본 이벤트를 유지하면서 집계 값을 추가합니다. 이러한 차이로 인해 이들 명령어는 다양한 상황과 목적에 맞게 사용됩니다. 데이터를 분석하고 요약하는 데 필요한 명령어를 선택하여 효과적으로 사용하면, Splunk로 더 효율적인 데이터 분석이 가능해집니다.

