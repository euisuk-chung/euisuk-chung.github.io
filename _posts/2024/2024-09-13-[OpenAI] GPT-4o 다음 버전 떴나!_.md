---
title: "[OpenAI] GPT-4o 다음 버전 떴나!?"
date: "2024-09-13"
tags:
  - "OpenAI"
year: "2024"
---

# [OpenAI] GPT-4o 다음 버전 떴나!?

![](https://velog.velcdn.com/images/euisuk-chung/post/1f694bcf-bbd4-41d7-a032-1e6268fd2038/image.png)

최근 AI의 발전 속도는 가히 놀라울 정도입니다. 특히 OpenAI의 새로운 모델 GPT-o1은 기존 모델인 GPT-4o에 비해 괄목할 만한 성능 향상을 보여주고 있습니다. GPT-o1은 복잡한 추론을 더 잘 수행하고, 다양한 문제 해결 능력에서 사람 수준의 성과를 보여주며, 안전성 면에서도 뛰어난 성과를 기록하고 있습니다.

이번 글에서는 24년 9월 12일에 따끈따끈하게 발표된 GPT-o1(일명 🍓)의 주요 개선점과 GPT-4o와 비교해 어떤 점이 발전했는지 살펴보겠습니다.

* 원문 : <https://openai.com/index/learning-to-reason-with-llms/>

GPT-o1: 더 깊은 추론 능력
------------------

GPT-o1은 **추론 능력**이 크게 향상된 것이 특징입니다. 이전 모델인 GPT-4o와 달리 GPT-o1은 답변을 내리기 전 **내적 사고의 연쇄(Chain of Thought, CoT)**를 통해 문제를 단계적으로 분석합니다.

이 과정을 통해 모델은 복잡한 문제를 여러 단계로 나누어 해결하며, 각 단계에서 실수를 인식하고 수정하는 능력을 배양했습니다. 그 결과 수학, 코딩, 과학 문제 등에서 **인간 전문가 수준**에 근접하는 성과를 보여주고 있습니다.

성능 비교: GPT-4o vs GPT-o1
-----------------------

다양한 테스트 결과 GPT-o1은 GPT-4o에 비해 **추론 중심 작업**에서 월등한 성과를 기록했습니다.

* **수학 대회(AIME 2024)**: GPT-4o는 평균적으로 12%의 문제만 풀었지만, GPT-o1은 74% 이상의 문제를 해결하며 큰 성능 차이를 보였습니다. 특히 1000개의 샘플을 통해 재평가한 결과 GPT-o1은 93%의 문제를 해결해 미국 수학 올림피아드 상위 500명 안에 드는 성적을 기록했습니다.
* **코딩 대회(Codeforces)**: GPT-o1은 코딩 대회에서도 GPT-4o 대비 우수한 성과를 냈습니다. GPT-4o가 808 Elo 점수로 참가자 상위 11%에 머문 반면, GPT-o1은 1807 Elo 점수를 기록하며 상위 93%에 들어섰습니다.
* **과학 문제(GPQA Diamond)**: 물리학, 화학, 생물학 문제에서 GPT-o1은 **박사 수준의 전문가**를 능가하는 성과를 보여줬습니다. GPT-4o는 일부 문제에서 전문가 성과를 따라잡지 못했으나, GPT-o1은 모든 문제에서 전문가를 초과하는 결과를 보였습니다.

![](https://velog.velcdn.com/images/euisuk-chung/post/50500fc1-617d-4297-b36e-43612c7ba34f/image.png)

CoT(Chain of Thought)로 인한 안전성 향상
--------------------------------

GPT-o1의 추론 능력 향상은 **안전성**에서도 큰 차이를 만들어냈습니다. CoT를 통해 모델의 사고 과정을 모니터링하고, 안전 규칙을 더 효과적으로 적용할 수 있게 되었습니다. GPT-o1은 특히 **강제 접근 시도(jailbreaks)나 경계 상황**에서 GPT-4o보다 안전한 답변을 제공했습니다.

* **유해한 프롬프트에 대한 안전한 완성도**: 일반적인 유해 프롬프트에서 GPT-4o는 99%의 안전한 답변을 제공한 반면, GPT-o1은 99.5%로 소폭 향상되었습니다. 특히 더욱 까다로운 프롬프트(예: 불법적 성적 콘텐츠)에 대한 대응에서는 GPT-4o보다 45% 높은 안전성을 보였습니다.

실제 답변 예시
--------

GPT-o1의 뛰어난 성능은 여러 실제 응용 분야에서 두드러지게 나타났습니다.

* OpenAI에서는 아래 예시들(<https://openai.com/index/learning-to-reason-with-llms/>)을 통해 GPT-o1과 GPT-4o의 답변 스타일과 성능 차이를 보여줍니다.

### 1. **암호 해독 문제 예시**

#### 질문:

```
oyfjdnisdr rtqwainr acxz mynzbhhx -> Think step by step

oyekaijzdf aaptcg suaokybhai ouow aqht mynznvaatzacdfoulxxz -> Think step by step
```

#### GPT-4o의 답변:

* GPT-4o는 이 문제를 푸는 데 어려움을 겪으며, 해독 과정에서 확실한 규칙을 찾지 못하고 추가 정보나 규칙을 요구하는 경향이 있었습니다.

```
1. Given the example: oyfjdnisdr rtqwainr acxz mynzbhhx
2. By examining the words, it seems like the input text could be broken into groups based on natural separations or patterns. 

However, to make a meaningful decoding, I would need more context about the transformations or letter shifting that might be involved.
```

**분석**: GPT-4o는 예시 문장을 분석하려고 시도하지만, 명확한 규칙을 찾지 못하고, 추가적인 정보를 요구합니다. 즉, 정답에 다가가기는 하지만 완전히 풀어내지는 못합니다.

#### GPT-o1의 답변:

* GPT-o1은 **내적 사고의 연쇄(Chain of Thought, CoT)**를 사용해 문제를 단계별로 풀어 나갑니다. 각 단계에서 해독 규칙을 정확히 적용해, 최종적으로 의미 있는 답변을 생성합니다.

```
Let's apply the same pattern as in the example:

Ciphertext: oyekaijzdf
Pairs: oy, ek, ai, jz, df

Decoded letters:
oy → T
ek → H
ai → E
jz → R
df → E

Result: "THERE"
Continuing with the same method for the remaining words...

Final decoded message: "THERE ARE THREE R'S IN STRAWBERRY"
```

**분석**: GPT-o1은 주어진 암호를 단계별로 해독하면서, 명확한 규칙(알파벳을 숫자로 변환해 평균을 내는 방식)을 찾고 이를 적용하여 정답에 도달합니다. CoT를 통해 GPT-o1은 문제 해결을 체계적으로 진행하며, 더 나은 추론 능력을 보여줍니다.

### 2. **코딩 문제 예시**

#### 질문:

```
Write a bash script that takes a matrix represented as a string with format '[1,2],[3,4],[5,6]' and prints the transpose in the same format.
```

#### GPT-4o의 답변:

* GPT-4o는 문제를 해결하는 과정에서 코드가 복잡하고, 효율성이 떨어지는 방식으로 접근합니다. 결과적으로 실행은 가능하지만, 최적화된 코드라고 보기 어렵습니다.

```
#!/bin/bash
matrix_string=\$1
matrix_string=$(echo "$matrix_string" | tr -d '[]')
IFS=',' read -r -a rows <<< "$matrix_string"
num_columns=$(echo "${rows[0]}" | awk -F',' '{print NF}')
declare -a transpose
for ((i=0; i<num_columns; i++)); do
  column=()
  for ((j=0; j<${#rows[@]}; j+=num_columns)); do
    element=${rows[$((j+i))]}
    column+=("$element")
  done
  transpose+=("[$(IFS=','; echo "${column[*]}")]")
done
echo "$(IFS=','; echo "${transpose[*]}")"
```

**분석**: GPT-4o는 문제를 해결할 수 있는 코드이지만, 여러 반복문을 사용하면서 복잡한 코드가 만들어졌습니다. 최종 출력도 완벽하지 않을 가능성이 있습니다.

#### GPT-o1의 답변:

* GPT-o1은 더 나은 코드를 제시하며, CoT를 통해 문제의 핵심을 먼저 분석한 후 최적화된 방법을 제시합니다.

```
#!/bin/bash
input="\$1"
matrix=($(echo $input | sed 's/[][]//g' | tr ',' ' '))
rows=(${#matrix[@]}/2)
for ((i=0; i<2; i++)); do
  for ((j=0; j<rows; j++)); do
    echo -n "[${matrix[$((i+j*2))]}]"
    if [ $j -lt $((rows-1)) ]; then
      echo -n ","
    fi
  done
  if [ $i -lt 1 ]; then
    echo -n ","
  fi
done
echo
```

**분석**: GPT-o1은 보다 효율적인 코드를 제시하며, 문제를 간단히 해결합니다. 코드가 더 깔끔하고, 처리 시간도 줄어들어 실제 실행 시 성능이 더 좋습니다.

### 3. **수학 문제 예시**

#### 질문:

```
Let n be an even positive integer. Let p(x) = x²ⁿ + a₂ₙ₋₁x²ⁿ₋₁ + ⋯ + a₁x + a₀. Find all real numbers x for which p(1/x) = x²p(1/x).
```

#### GPT-4o의 답변:

* GPT-4o는 문제의 일부를 풀어내지만, 결과적으로 전체적인 해답에 이르지 못하고 불완전한 추론을 보여줍니다.

```
The given polynomial p(x) can be written as a series of terms in x, but further simplification requires more context. To fully solve this, it seems necessary to explore additional steps for the condition p(1/x) = x²p(1/x).
```

**분석**: GPT-4o는 문제를 구조적으로 분석하는 데 한계를 보이며, 중요한 조건을 놓치고 있습니다. 결국 정답에 이르기 위해 추가적인 정보가 필요하다는 식으로 끝을 맺습니다.

#### GPT-o1의 답변:

* GPT-o1은 문제를 더 깊이 이해하고, 주어진 조건을 체계적으로 해결합니다.

```
We are tasked with finding x such that p(1/x) = x²p(1/x). Let's start by rewriting the polynomial as p(x) = x²ⁿ + a₂ₙ₋₁x²ⁿ₋₁ + ⋯ + a₀. The condition p(1/x) = x²p(1/x) implies that x must satisfy certain roots. Solving this, we find that x = ±1, ±2, ⋯, ±n are the solutions.
```

**분석**: GPT-o1은 CoT를 통해 단계별로 문제를 해결하고, 조건을 충족하는 모든 해를 구체적으로 도출해냅니다. 이 과정에서 추론을 체계적으로 나누어 문제를 풀어나갑니다.

결론
--

GPT-o1은 **추론, 코딩, 과학** 등의 영역에서 GPT-4o를 크게 능가하는 성과를 보여주고 있으며, AI 모델의 새로운 가능성을 열고 있습니다. 앞으로 GPT-o1과 같은 모델은 다양한 산업에서 복잡한 문제 해결을 돕고, AI의 응용 범위를 넓히는 데 기여할 것입니다.

GPT-o1은 단순한 답변 생성에 그치지 않고, **사고 과정 자체를 강화**함으로써 더욱 **안전하고 신뢰할 수 있는 AI**로 거듭나고 있습니다.

마지막으로 흥미로운 영상 링크와 해당 영상에서 주요 이미지들을 첨부하며 이번 글을 마쳐보겠습니다!

* [Korean Cipher with OpenAI o1](https://youtu.be/eZDmDn6Iq9Y)

![](https://velog.velcdn.com/images/euisuk-chung/post/fd1b4e44-d941-48b4-857a-388154dba38d/image.png)

![](https://velog.velcdn.com/images/euisuk-chung/post/c73a7a82-2ca1-4e48-bd16-61bd7d802965/image.png)

![](https://velog.velcdn.com/images/euisuk-chung/post/fc141168-a7bb-46de-b51d-affd3aaadaaa/image.png)

읽어주셔서 감사합니다! 📖