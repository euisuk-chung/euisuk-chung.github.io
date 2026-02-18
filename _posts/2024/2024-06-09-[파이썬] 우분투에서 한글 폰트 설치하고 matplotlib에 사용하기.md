---
title: "[파이썬] 우분투에서 한글 폰트 설치하고 matplotlib에 사용하기"
date: "2024-06-09"
tags:
  - "python"
  - "visualization"
  - "환경"
year: "2024"
---

# [파이썬] 우분투에서 한글 폰트 설치하고 matplotlib에 사용하기

안녕하세요😛 오늘은 우분투에서 한글 폰트 설치하고 matplotlib에서 해당 폰트를 사용하는 방법을 정리해보겠습니다!

파이썬을 활용하다보면 시각화는 필수 영역입니다. 그러나 Linux 환경에서는 기본적으로 한글 폰트가 설치되어 있지 않아 한글이 제대로 표시되지 않는 경우가 많습니다. 본 게시글의 제목처럼 `네모네모 빔`을 맞은 것처럼 깨져서 나오게 됩니다 😱

![네모네모](https://velog.velcdn.com/images/euisuk-chung/post/96202ac3-2cac-4350-921a-274d54d11fcb/image.png)

이렇게 출력되는 주된 이유는 운영체제의 기본 폰트 세트에 한글 폰트가 포함되지 않기 때문입니다. 따라서 별도로 한글 폰트를 설치해야 합니다. 이번 글에서는 Ubuntu 환경에서 나눔 폰트를 사용하여 Matplotlib에 적용하는 방법을 단계별로 상세히 정리하겠습니다.

아래 방법을 따르면 5분 내로 폰트를 설정할 수 있습니다.

1. 나눔 폰트 설치
-----------

우선, 나눔 폰트를 설치합니다. 터미널에서 다음 명령어를 실행합니다.

```
sudo apt-get install fonts-nanum*
```

2. 폰트 캐시 삭제
-----------

폰트 캐시를 갱신하기 위해 캐시를 삭제합니다.

```
fc-cache -fv
```

3. 폰트 배포
--------

Matplotlib의 폰트 디렉터리에 나눔 폰트를 복사해야 합니다. 먼저, Matplotlib 설정 디렉터리가 어디 있는지 확인합니다.

```
import matplotlib
print(matplotlib.__file__)
```

위 명령어를 실행하면 Matplotlib의 경로가 출력됩니다. 예를 들어:

```
/usr/anaconda3/lib/python3.7/site-packages/matplotlib/__init__.py
```

이 경로를 기준으로, `mpl-data/fonts/ttf` 디렉터리에 폰트를 복사합니다.

예를 들어 Anaconda 환경이라면 다음과 같이 복사합니다.

```
cp /usr/share/fonts/truetype/nanum/Nanum* /usr/anaconda3/lib/python3.7/site-packages/matplotlib/mpl-data/fonts/ttf/
```

4. Matplotlib 폰트 캐시 삭제
----------------------

Matplotlib의 폰트 캐시를 삭제하여 새로운 폰트를 인식하도록 합니다.

```
rm -rf ~/.cache/matplotlib/*
```

5. 폰트 적용
--------

파이썬 혹은 주피터 노트북을 재실행하여 폰트를 로드합니다. 폰트가 설치되었는지 확인하는 명령어를 실행합니다.

```
import matplotlib.font_manager
print([f.fname for f in matplotlib.font_manager.fontManager.ttflist])
```

위 명령어를 실행하면 설치된 폰트 리스트가 출력됩니다. `Nanum`으로 시작하는 폰트들이 보이면 제대로 설치된 것입니다.

폰트 이름을 확인하는 방법은 다음과 같습니다.

```
import matplotlib.font_manager
font_list = matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
print([matplotlib.font_manager.FontProperties(fname=font).get_name() for font in font_list])
```

위 명령어를 실행하면 폰트 이름들이 출력됩니다. 예를 들어:

```
['Nanum Brush Script', 'NanumBarunGothic', 'NanumSquareRound', ...]
```

이제 폰트를 Matplotlib에서 적용할 수 있습니다.

6. 예시 코드 실행
-----------

다음 예제 코드를 사용하여 나눔 폰트를 설정하고 그래프를 그려봅니다.

```
import matplotlib.pyplot as plt
import matplotlib as mpl

# 폰트 설정
plt.rcParams["font.family"] = 'NanumGothic'
mpl.rcParams['axes.unicode_minus'] = False  # 마이너스 폰트 깨짐 방지

# 예시 그래프
plt.figure(figsize=(8, 6))
plt.plot([1, 2, 3, 4], [10, 20, 25, 30])
plt.title('예제 그래프')
plt.xlabel('X 축')
plt.ylabel('Y 축')
plt.show()
```

이제 한글이 제대로 출력되는 것을 확인할 수 있습니다! 😍

![해결](https://velog.velcdn.com/images/euisuk-chung/post/edf1dba7-6eff-4e5b-864f-2ee51ffeadf8/image.png)

이 과정을 통해 나눔 폰트를 Ubuntu 환경에서 Matplotlib에 적용할 수 있습니다.

(참고) Jupyter Snippet
--------------------

귀찮으시다고요?! 저도 귀찮아서 주피터노트북에서 한번에 실행할 수 있게 코드를 짰습니다 😝

```
"""
Matplotlib 한글 폰트 설정 - 간단 버전
"""
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import subprocess
import glob
import shutil
from pathlib import Path

# 1. 폰트 설치 (없을 경우)
try:
    subprocess.run(['sudo', 'apt-get', 'install', '-y', 'fonts-nanum'], 
                   capture_output=True, check=True)
except: pass

# 2. matplotlib 폰트 디렉토리에 복사
try:
    import matplotlib
    mpl_font_dir = Path(matplotlib.__file__).parent / 'mpl-data' / 'fonts' / 'ttf'
    font_files = glob.glob('/usr/share/fonts/truetype/nanum/*.ttf')
    
    for font_file in font_files:
        shutil.copy(font_file, mpl_font_dir)
    
    print(f"✅ {len(font_files)}개 폰트 복사 완료")
except Exception as e:
    print(f"⚠️ 폰트 복사 실패: {e}")

# 3. 폰트 캐시 재생성 및 설정
try:
    fm._rebuild()
except: pass

# 4. matplotlib 설정
plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

print("✅ 한글 폰트 설정 완료: NanumGothic")
```

![](https://velog.velcdn.com/images/euisuk-chung/post/486a4646-9c1e-4ad4-b3d2-0b76784de085/image.png)

가상환경을 사용하시는 분의 경우 가상환경마다 설정을 해줘야하는 번거로움이 있긴하지만, 한글 사용이 필수적이라면 위에 소개해드린 단계를 따라 폰트를 설정해보세요!!

감사합니다 😛