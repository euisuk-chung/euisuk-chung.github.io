---
title: "[파이썬] 데코레이터(Decorator) 사용법"
date: "2024-12-25"
tags:
  - "python"
year: "2024"
---

# [파이썬] 데코레이터(Decorator) 사용법




메리크리스마스 여러분!!‧₊˚🎄✩ 크리스마스 트리를 장식할 때, 가장 중요한 건 뭐니 뭐니 해도 트리 자체입니다. 하지만 단순한 나무에 예쁜 전구, 리본, 장난감을 더하면 특별한 분위기를 연출할 수 있죠. 데코레이터도 마찬가지입니다! 기본 함수에 원하는 장식을 덧붙여서, 함수의 전후를 꾸미거나 새로운 기능을 추가할 수 있습니다.

이번 포스트에서는 크리스마스 트리를 꾸미는 것처럼, 함수에 데코레이터를 더해보는 재미있는 여정을 시작해 봅시다. 함수 호출 전후로 메시지를 추가하거나, 실행 시간을 측정하거나, 로그를 남기거나, 인증 체크를 수행하는 등 다양한 데코레이터 활용법을 살펴보겠습니다. 여러분의 코드가 더욱 빛나게 될 거예요! ✨

> 파이썬의 **데코레이터(Decorator)**는 "함수나 메서드의 동작을 확장하거나 수정할 수 있는 매우 강력한 도구"입니다. 하지만 그 개념이 생소하거나 코드 구조가 낯설어 처음 배우는 사람에게는 어렵게 느껴질 수 있습니다.

* 이번 글에서는 초보자도 이해할 수 있도록 **데코레이터의 기본 개념**과 **활용법**을 쉽고 명확하게 설명하고, 여러 예제를 통해 데코레이터의 유용성을 보여드리겠습니다.

---

**1. 데코레이터란 무엇인가요?**
--------------------

우리가 *"무엇인가를 decorate하다"*라고 하면, *"무엇인가를 장식하다, 또는 꾸미다"*라는 의미가 있습니다.

=> 데코레이터(decorator)는 말 그대로 함수를 꾸며주는 도구입니다. 즉, 어떤 함수가 있을 때 해당 함수를 직접 수정하지 않고 함수를 꾸며주기 위해 데코레이터를 사용합니다.

* **정의**:
  + 데코레이터는 함수를 인자로 받아 새로운 기능을 추가한 후, 수정된 함수를 반환하는 **고차 함수(higher-order function)**입니다.

> ❓ **고차 함수(Higher-Order Function)**는 다음 두 가지 조건 중 하나 이상을 만족하는 함수를 말합니다:
> 
> * (1) **함수를 인자로 받을 수 있는 함수**
>   + 다른 함수(혹은 람다 함수 등)를 매개변수로 받아 실행하거나 처리할 수 있습니다.
>   + 예: `map()`, `filter()`, `reduce()` 등이 이에 해당합니다.
> * (2) **함수를 반환할 수 있는 함수**
>   + 다른 함수를 반환값으로 생성하거나 리턴할 수 있습니다.

> (1) **함수를 인자로 받는 예시**
> 
> ```
>   def apply_function(func, data):
>       return func(data)
>   # 사용 예시
>   def square(x):
>       return x * x
>   result = apply_function(square, 5)  # 25
>   print(result)
> ```
> 
> * `apply_function`은 `func`이라는 매개변수로 함수를 받습니다.
> * 호출 시, `square`라는 함수를 넘겨주고 `data`로 5를 전달하여 `square(5)`가 실행됩니다.

> (2) **함수를 반환하는 예시**
> 
> ```
>   def outer_function(message):
>       def inner_function():
>           return f"Message: {message}"
>       return inner_function
>   # 사용 예시
>   my_function = outer_function("Hello, World!")
>   print(my_function())  # Message: Hello, World!
> ```
> 
> * `outer_function`은 `inner_function`이라는 함수를 반환합니다.
> * 반환된 `my_function`은 내부의 `inner_function` 역할을 하며, 나중에 실행됩니다.

* `데코레이터`는 **고차 함수의 두 번째 특징**(함수를 반환할 수 있는 함수)을 이용합니다.
  
  + (설명1) 데코레이터는 함수를 인자로 받고, 그 함수를 수정하거나 새로운 기능을 추가한 함수를 반환하여 기존 함수를 "장식"합니다.
  + (설명2) 데코레이터는 **함수를 받아서 내부에 새로운 함수를 정의**하고, 이를 반환하는 방식으로 동작합니다. 이를 통해 기존 함수에 새로운 기능을 추가할 수 있습니다.
* **장점**:
  
  + 코드 수정 없이 **함수의 동작을 변경하거나 추가적인 기능을 부여**할 수 있습니다.
  + **반복 코드를 줄이고, 코드의 가독성과 유지보수성을 높입니다**.

예를 들어, 함수 호출 전후에 로그를 출력하고 싶다면, **해당 코드를 모든 함수에 삽입하지 않고 데코레이터로 깔끔하게 해결**할 수 있습니다.

---

**2. 데코레이터 기본 사용법**
-------------------

### **2.1 기본 구조**

데코레이터의 기본 구조는 다음과 같습니다:

```
def my_decorator(func):  # func: 꾸미고자 하는 함수
    def wrapper():
        print("Before the function is called")
        func()  # 원래 함수 실행
        print("After the function is called")
    return wrapper  # 수정된 함수 반환

```

* **`my_decorator(func)`**: 데코레이터로 사용될 함수입니다.
  + 이 함수는 다른 함수를 매개변수(`func`)로 받아, 원래 함수(func)의 동작을 감싸는 `wrapper` 함수를 정의하고 반환합니다.
  + **`wrapper()`**: 원래 함수(`func`) 호출 전후에 추가 동작을 삽입하는 함수입니다.

### **2.2 데코레이터 적용**

데코레이터는 `@`를 사용해 간편하게 적용할 수 있습니다.

```
@my_decorator
def say_hello():
    print("Hello, World!")

say_hello()

```

* **`@my_decorator`**: `say_hello` 함수에 `my_decorator`를 적용합니다.
  + `say_hello`는 이제 `my_decorator(say_hello)`가 반환하는 `wrapper` 함수로 대체됩니다.
* 결과적으로 `say_hello()`를 호출하면 `wrapper()`가 실행됩니다.

즉, 위 코드는 아래 코드와 동일하게 동작합니다:

```
say_hello = my_decorator(say_hello)
say_hello()

```

* 데코레이터를 사용하지 않고 위처럼 수동으로 함수에 데코레이터를 적용해도 동일한 결과가 나옵니다.
* 원래 `say_hello` 함수는 `my_decorator`를 통해 감싸인 `wrapper`로 대체됩니다.

### **2.3 실행 결과**

```
say_hello()
```

* 함수 호출 흐름:
  
  1. `wrapper` 함수가 실행됩니다.
  2. `print("Before the function is called")`가 실행됩니다.
  3. 원래 `say_hello` 함수 (`func`)가 실행됩니다. 여기서 `print("Hello, World!")`가 출력됩니다.
  4. `print("After the function is called")`가 실행됩니다.
* 최종 출력:

```
Before the function is called
Hello, World!
After the function is called
```

---

**3. 데코레이터 예제로 배우기**
--------------------

### **3.1 간단한 데코레이터 예제**

함수 호출 전후에 메시지를 출력하는 데코레이터를 만들어 봅시다.

* 첫 번째 예제는 위에 2번에서 본 예시와 유사한 유형입니다.

```
def my_decorator(func):
    def wrapper():
        print("Before the function is called")
        func()
        print("After the function is called")
    return wrapper

@my_decorator
def greet():
    print("Hello!")

greet()
```

* **`my_decorator`**:
  
  + 이 함수는 원래 함수를 감싸는 역할을 합니다. 호출 전후에 메시지를 출력하여 함수 동작을 보강합니다.
* **`greet`**:
  
  + 단순히 "Hello!"를 출력하는 함수이나, `@my_decorator` 데코레이터를 통해 호출 전후에 메시지가 추가로 출력됩니다.

**출력 결과**:

```
Before the function is called
Hello!
After the function is called
```
### **3.2 인자와 반환값 처리**

데코레이터는 `*args`와 `**kwargs`를 사용하여 다양한 인자와 반환값을 처리할 수 있습니다.

```
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Function is about to execute")
        result = func(*args, **kwargs)  # 원래 함수 호출
        print("Function has finished executing")
        return result
    return wrapper

@my_decorator
def add(a, b):
    return a + b

print(add(3, 4))
```

* **`wrapper`**: 인자와 반환값을 처리하기 위해 `*args`와 `**kwargs`를 사용합니다. 이로 인해 다양한 형태의 함수 호출을 지원할 수 있습니다.
* **`add`**: 두 숫자의 합을 반환하는 함수입니다. 데코레이터를 통해 호출 전후에 메시지가 출력되며, 결과값도 반환됩니다.

**출력 결과**:

```
Function is about to execute
Function has finished executing
7
```

---

**4. 데코레이터 활용 예제**
------------------

### **4.1 로깅 데코레이터**

어떤 함수가 호출될 때 로그를 남기고 싶을 때 유용합니다.

```
import logging
logging.basicConfig(level=logging.INFO)

def log_decorator(func):
    def wrapper(*args, **kwargs):
        logging.info(f"Calling {func.__name__} with {args} and {kwargs}")
        result = func(*args, **kwargs)
        logging.info(f"{func.__name__} finished executing")
        return result
    return wrapper

@log_decorator
def multiply(a, b):
    return a * b

print(multiply(5, 3))
```

* **`log_decorator`**: 함수 호출 시 로그 메시지를 출력합니다. 이로 인해 디버깅이나 함수 호출 추적에 유용합니다.
* **`multiply`**: 두 숫자를 곱하는 함수로, 호출 시 로그가 자동으로 기록됩니다.

**출력 결과**:

```
INFO:root:Calling multiply with (5, 3) and {}
INFO:root:multiply finished executing
15
```

---

### **4.2 실행 시간 측정 데코레이터**

함수 실행에 걸린 시간을 측정하는 데코레이터를 만들어 봅시다.

```
import time

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()  # 시작 시간 기록
        result = func(*args, **kwargs)
        end_time = time.time()  # 종료 시간 기록
        print(f"{func.__name__} took {end_time - start_time:.4f} seconds to execute")
        return result
    return wrapper

@timing_decorator
def slow_function():
    time.sleep(2)
    print("Finished sleeping")

slow_function()
```

* **`timing_decorator`**: 함수 실행 시작과 종료 시각을 기록하여 실행 시간을 측정합니다.
* **`slow_function`**: 2초간 멈춘 뒤 메시지를 출력하는 함수로, 데코레이터를 통해 실행 시간이 측정됩니다.

**출력 결과**:

```
Finished sleeping
slow_function took 2.0002 seconds to execute
```

---

### **4.3 인증 데코레이터**

사용자의 인증 상태를 확인하고, 인증되지 않으면 에러를 발생시키는 데코레이터입니다.

```
def authenticate_decorator(func):
    def wrapper(user, *args, **kwargs):
        if not user.get("is_authenticated"):
            raise PermissionError("User not authenticated")
        return func(user, *args, **kwargs)
    return wrapper

@authenticate_decorator
def view_profile(user):
    print(f"User profile: {user['name']}")

user = {"name": "Alice", "is_authenticated": True}
view_profile(user)

unauth_user = {"name": "Bob", "is_authenticated": False}
view_profile(unauth_user)  # PermissionError 발생
```

* **`authenticate_decorator`**: 사용자의 인증 상태를 확인하는 데 사용됩니다. 인증되지 않은 사용자에 대해 예외를 발생시킵니다.
* **`view_profile`**: 사용자 프로필 정보를 출력하는 함수입니다. 데코레이터를 통해 인증 상태를 확인합니다.

**출력 결과**:

```
User profile: Alice
Traceback (most recent call last):
  ...
PermissionError: User not authenticated
```

---

**5. 고급 주제: functools.wraps**
-----------------------------

데코레이터를 사용하면 원래 함수의 이름(`__name__`)과 문서 문자열(`__doc__`)이 감싸는 함수(wrapper)로 덮여 원래 함수의 정보를 잃게 됩니다. 이를 방지하기 위해 `functools.wraps`를 사용합니다.

```
from functools import wraps

def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Before function call")
        result = func(*args, **kwargs)
        print("After function call")
        return result
    return wrapper

@my_decorator
def my_function():
    """This is my function."""
    print("Hello!")

print(my_function.__name__)  # my_function
print(my_function.__doc__)   # This is my function.
```

* **`wraps`**: `functools`의 유틸리티로, 데코레이터 적용 후에도 원래 함수의 메타데이터(`__name__`, `__doc__`)를 유지시켜줍니다.
* **`my_function`**: 간단한 메시지를 출력하는 함수로, 데코레이터를 통해 호출 전후에 메시지가 추가됩니다.

**출력 결과**:

```
Before function call
Hello!
After function call
my_function
This is my function.
```
> 🧩 **functools.wraps**
> 
> * `functools.wraps`는 Python에서 데코레이터를 작성할 때, **원래 함수의 메타데이터(예: 함수 이름, 문서 문자열 등)를 보존**하기 위해 사용되는 유틸리티입니다.
>   + 일반적으로 데코레이터를 적용하면 원래 함수의 이름(**name**)과 문서 문자열(**doc**)이 데코레이터로 대체된 함수(주로 wrapper 함수)로 변경됩니다.
>   + 이로 인해 디버깅이나 함수의 메타정보를 확인하기 어려운 문제가 발생할 수 있습니다.
> * **주요 기능**
>   + 원래 함수 이름 유지: 데코레이터가 적용된 함수도 원래 함수 이름으로 표시됩니다.
>   + 문서 문자열 보존: 원래 함수의 Docstring이 유지됩니다.
>   + 기타 메타데이터 보존: **module**, **annotations**, **dict** 같은 속성도 유지됩니다.

---

**6. 데코레이터 중첩**
---------------

데코레이터는 여러 개를 동시에 사용할 수도 있습니다. 이때 적용 순서는 **가장 가까운 데코레이터부터** 실행됩니다.

```
def decorator1(func):
    def wrapper():
        print("Decorator 1")
        func()
    return wrapper

def decorator2(func):
    def wrapper():
        print("Decorator 2")
        func()
    return wrapper

@decorator1
@decorator2
def hello():
    print("Hello!")

hello()
```

* **`decorator1`**: 가장 바깥쪽에서 실행되는 데코레이터입니다.
* **`decorator2`**: 가장 안쪽에서 실행되는 데코레이터입니다.
* **`hello`**: 데코레이터 중첩을 통해 호출 순서에 따라 메시지가 출력됩니다.

**출력 결과**:

```
Decorator 1
Decorator 2
Hello!
```

---

**7. 결론**
---------

데코레이터는 처음엔 다소 어렵게 느껴질 수 있지만, 그 원리를 이해하면 매우 유용한 도구입니다. 특히 반복적인 작업을 줄이고, 코드를 깔끔하고 효율적으로 만들 수 있습니다.

> 💌 **SUMMARY**  
> 
> 1. 데코레이터는 함수를 꾸며주는 도구입니다.  
> 
> 2. `@`를 사용해 간단하게 적용할 수 있습니다.  
> 
> 3. 다양한 활용법(로깅, 실행 시간 측정, 인증 등)으로 코드를 효율적으로 관리할 수 있습니다.  
> 
> 4. `functools.wraps`를 사용해 원래 함수 정보를 보존하세요.

오늘은 크리스마스 특집으로 데코레이터 개념을 정리해보았는데요! 저도 실은 잘 사용하지는 못하는 편이지만 많은 라이브러리를 보면 데코레이터를 쓰는 코드들이 많아서 중요한 개념이랍니다!! 😊

![](https://velog.velcdn.com/images/euisuk-chung/post/4109d755-51ad-4835-b554-19b7cfcd6dc8/image.png)

이제 직접 데코레이터를 만들어 보고, 다양한 함수에 적용해 보세요!  

데코레이터의 매력에 빠지게 될 것입니다.

오늘도 읽어주셔서 감사합니다 :)

