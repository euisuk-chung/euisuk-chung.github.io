---
title: "🐍 내가 보려고 작성한 *args, **kwargs, 그리고 **vars(args) 파이썬 함수 인자 정리"
date: "2025-07-01"
year: "2025"
---

# 🐍 내가 보려고 작성한 *args, **kwargs, 그리고 **vars(args) 파이썬 함수 인자 정리


![](https://velog.velcdn.com/images/euisuk-chung/post/55d70d64-25c2-480f-9502-58d3ce0fc76e/image.png)

👋 들어가며
------

Python으로 데이터를 다루다 보면 함수에 인자를 유연하게 넘겨야 하는 상황이 자주 생깁니다.

특히 다음과 같은 경우죠:

* 인자의 개수가 많아서 일일이 쓰기 귀찮을 때
* `argparse`로 파싱한 커맨드라인 인자를 함수에 넘기고 싶을 때
* 재사용성과 유지보수가 좋은 함수를 만들고 싶을 때

이럴 때 **`args`, `kwargs`, `vars(args)`**를 이해하고 제대로 활용하면 코드가 훨씬 깔끔하고 파워풀해집니다.

하지만, 오랫동안 안 쓰다보면 종종 헷갈리는 경우가 있어, 이번 포스팅을 통해 이 세 가지 개념을 실제 예제와 함께 자세히 복습하며 정리해보겠습니다.

---

🧱 기본 개념 정리
----------

### (참고) 위치 인자 (Positional Argument)란?

**✅ 정의**

**함수의 매개변수(parameter)에 순서대로 값을 전달하는 인자**를 의미합니다.

* 인자의 이름을 명시하지 않고, **위치에 따라** 해당 매개변수에 값이 할당됩니다.
* 함수 정의에서의 **매개변수 순서가 중요**합니다.

**📋 예제**

```
def greet(name, age):
    print(f"My name is {name} and I’m {age} years old.")

greet("Alice", 30)  # ✅ 위치 인자 사용
```

* `"Alice"` → 첫 번째 `위치` 인자 → `name`
* `30` → 두 번째 `위치` 인자 → `age`

### 1️⃣ `*args`: 위치 인자를 튜플로 받기

```
def arg_func(*args):
    return(print(args)) 
    
arg_func(1, 2, 3)
# 출력:
# (1, 2, 3)
```

* `값만 전달`하는 방식 → **위치 인자(Positional Argument)**
* `*args`는 **여러 개의 위치 인자**를 한꺼번에 받을 수 있게 해줍니다.
* 결과는 **튜플(tuple)**로 반환됩니다.
* 여기서 `args = (1, 2, 3)`이 됩니다.

```
def print_args(*args):
    for arg in args:
        print(arg)

print_args(1, 2, 3)
# 출력:
# 1
# 2
# 3
```

* `*args`는 함수에 전달된 **여러 개의 위치 인자**를 하나의 튜플로 묶어줍니다.
* 이름은 꼭 `args`일 필요는 없지만, 관례적으로 이렇게 사용합니다.

---

### (참고) 키워드 인자 (Keyword Argument)란?

**✅ 정의**

**매개변수의 이름을 명시하여 값을 전달하는 인자**입니다.

* 인자 순서를 지키지 않아도 되며, **이름 기준으로 매핑**됩니다.

**📋 예제**

```
greet(age=30, name="Alice")  # ✅ 키워드 인자 사용
```

* `age=30` → `age` 매개변수(키워드 인자)로 직접 전달됨
* `name="Alice"` → `name` 매개변수(키워드 인자)로 직접 전달됨
* 순서가 바뀌어도 전혀 문제 없음!

### 2️⃣ `**kwargs`: 키워드 인자를 딕셔너리로 받기

```
def kwarg_func(**kwargs):
    return(print(kwargs))    
    
kwarg_func(a=1, b=2, c=3)

# 출력:
# {'a': 1, 'b': 2, 'c': 3}
```

* `이름=값 형식으로 전달`하는 방식 → **키워드 인자(Keyword Argument)**
* `**kwargs`는 **여러 개의 키워드 인자**를 한꺼번에 받을 수 있게 해줍니다.
* 결과는 **딕셔너리(dict)** 형태로 저장됩니다.
* 여기서 `kwargs = {'a': 1, 'b': 2, 'c': 3}`가 됩니다.

```
def print_kwargs(**kwargs):
    for key, value in kwargs.items():
        print(f"{key} = {value}")

print_kwargs(name="Alice", age=30)

# 출력:
# name = Alice
# age = 30
```

* `**kwargs`는 함수에 전달된 **여러 개의 키워드 인자**를 딕셔너리로 묶어줍니다.
* 즉, `key=value` 형식의 인자들을 처리할 때 유용합니다.

---

### 정리

| 구분 | 영어 명칭 | 전달 형식 | 순서 중요 여부 | 함수 내부 처리 | 예시 |
| --- | --- | --- | --- | --- | --- |
| 위치 인자 | Positional Argument | 값만 | ✅ 중요 | `*args` → tuple | `arg_func(1, 2, 3)` |
| 키워드 인자 | Keyword Argument | key=value 형식 | ❌ 중요하지 않음 | `**kwargs` → dict | `kwarg_func(a=1, b=2, c=3)` |

**예제 1.**

```
def greet(name, age):
    print(f"Hello, I'm {name} and I'm {age} years old.")

info = ("Alice", 30)
greet(*info)  # 위치 언패킹

data = {"name": "Alice", "age": 30}
greet(**data)  # 키워드 언패킹
```

> ✅ 핵심: `*`는 튜플 → 위치 인자, `**`는 딕셔너리 → 키워드 인자로 변환해 줍니다.

**예제 2.**

```
def foo(*args, **kwargs):
    print("args:", args)
    print("kwargs:", kwargs)

foo(1, 2, 3, a=10, b=20)

# 출력: 
# args: (1, 2, 3)
# kwargs: {'a': 10, 'b': 20}
```

* 앞의 `1, 2, 3` → 위치 인자니까 전부 `args = (1, 2, 3)`
* 뒤의 `a=10, b=20` → 키워드 인자니까 전부 `kwargs = {'a':10, 'b':20}`

-> 이걸 "알아서" 해주는 게 Python의 함수 호출 인터페이스의 **자동 언패킹 메커니즘**입니다.

---

💻 실전 예제: `argparse` + `**vars(args)`
------------------------------------

다음은 커맨드라인에서 인자를 받아 시계열 데이터를 생성하는 스크립트 예제입니다.

### 📄 예시 스크립트: `generate_series.py`

```
import argparse

def generate_time_series_with_anomalies(num_points, 
										anomaly_rate, 
                                        anomaly_range,
                                        anomaly_length,
                                        freq, amp, slope):
	(중략 ...)
    
    return [], []

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_points', type=int, default=1000)
    parser.add_argument('--anomaly_rate', type=float, default=0.01)
    parser.add_argument('--anomaly_range', type=eval, default=(2, 3))
    parser.add_argument('--anomaly_length', type=int, default=6)
    parser.add_argument('--freq', type=int, default=20)
    parser.add_argument('--amp', type=float, default=0.4)
    parser.add_argument('--slope', type=float, default=0.0)

    args = parser.parse_args()

    # 💡 핵심 포인트: args를 딕셔너리로 변환하고 언패킹
    generate_time_series_with_anomalies(**vars(args))
```

### ✅ 왜 `**vars(args)`가 유용할까?

* `argparse`는 `args`라는 **Namespace 객체**를 반환합니다.
* `vars(args)`는 이 Namespace 객체를 **딕셔너리로 변환**합니다.
* `**vars(args)`를 통해 해당 딕셔너리를 함수에 언패킹하면 각 키워드를 인자로 넘길 수 있습니다.

---

🧪 실습해보기
-------

![](https://velog.velcdn.com/images/euisuk-chung/post/35a35a53-56cd-477f-ab70-8bbd3bdd87e4/image.png)

위처럼 커맨드라인에서 옵션을 주면 자동으로 함수 인자에 매핑되어 넘겨집니다.

---

🧠 마무리 요약
--------

| 개념 | 설명 |
| --- | --- |
| `*args` | 여러 개의 위치 인자를 튜플로 받음 |
| `**kwargs` | 여러 개의 키워드 인자를 딕셔너리로 받음 |
| `*` | 튜플을 위치 인자로 언패킹 |
| `**` | 딕셔너리를 키워드 인자로 언패킹 |
| `vars(args)` | Namespace → dict 변환 (argparse와 함께 자주 사용됨) |

---

🪄 실무 팁
------

* `argparse`를 쓸 땐 `**vars(args)` 패턴을 적극 활용하세요.
* 함수에 인자가 많거나, 가변적인 경우 `**kwargs`를 함수 정의에 포함시키면 유지보수에 매우 유리합니다.
* 필요하다면 `def func(a, b, **kwargs):`처럼 고정 인자 + 가변 인자를 혼용해도 좋습니다.