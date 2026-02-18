---
title: "[머신러닝][차원축소] 변수 추출법 - Multi-Dimensional Scaling (MDS)"
date: "2021-12-28"
tags:
  - "머신러닝"
  - "차원축소"
year: "2021"
---

# [머신러닝][차원축소] 변수 추출법 - Multi-Dimensional Scaling (MDS)

본 포스트는 `고려대학교 강필성 교수님`의 강의를 수강 후 정리를 한 것입니다. 작성 및 설명의 편의를 위해 아래는 편하게 작성한 점 양해부탁드립니다.

Dimensionality Reduction
========================

Supervised Variable Extraction
------------------------------

**차원축소**는, 모델링을 하기 위해 내가 가진 데이터의 정보를 최대한 보존하면서, 훨씬 더 compact하게 데이터셋을 구성하는 것을 목적으로 하며, 크게 변수선택(Variable Selection, 변수들의 부분 집합 선택)과 변수추출(Variable Extraction, 변수들을 요약하는 새로운 변수 생성)이 있다.

이전 [포스트](https://velog.io/@euisuk-chung/%EB%A8%B8%EC%8B%A0%EB%9F%AC%EB%8B%9D%EC%B0%A8%EC%9B%90%EC%B6%95%EC%86%8C-%EB%B3%80%EC%88%98-%EC%84%A0%ED%83%9D%EB%B2%95-16)에서는 아래 표에서 Supervised Variable Selection을 살펴보았다. 오늘은 Supervised Variable Extraction에 대해 이야기를 풀어보도록 하겠다.

![Supervised Variable Selection](https://velog.velcdn.com/images%2Feuisuk-chung%2Fpost%2F423cc1da-966e-4a89-8c91-f317b6415aa8%2Fimage.png)

### MDS란

Multi-Dimensional Scaling(MDS), 다차원척도법이란, D-차원 공간 상의 객체들이 있을 때 그 객체들의 거리(between object distance)가 저-차원 공간 상에도 최대한 많이 보존되도록 하는 좌표계를 찾는 것을 의미한다.

![MDS](https://velog.velcdn.com/images%2Feuisuk-chung%2Fpost%2F807ceb6c-81d4-48c4-9005-2a5b1abfd24e%2Fimage.png)

> Distance matrix를 통해서 저-차원 상의 각각의 객체들이 갖는 좌표 시스템을 찾는 것이 목적

지난번에 다루었던 PCA([링크](https://velog.io/@euisuk-chung/%EB%A8%B8%EC%8B%A0%EB%9F%AC%EB%8B%9D%EC%B0%A8%EC%9B%90%EC%B6%95%EC%86%8C-%EB%B3%80%EC%88%98-%EC%B6%94%EC%B6%9C%EB%B2%95-Principal-Component-Analysis-PCA))와 MDS를 비교하면 다음과 같이 표로 정리할 수 있다.

![PCA-MDS](https://velog.velcdn.com/images%2Feuisuk-chung%2Fpost%2Ff6e8baa9-5016-48dd-aca7-272191b40b69%2Fimage.png)

추가적으로 PCA를 적용할 수 있는 모든 데이터는 거리에 대한 값으로 표기 및 MDS 적용이 가능하지만, 역은 성립하지 않는다.

### MDS 프로세스

**[1] Construct Proximity/Distance Matrix 단계**

* 근접/거리 행렬(D, distance matrix) 구축 단계이다.
* 거리-행렬이 가져야할 특징은 아래와 같다:  
  1. dij≥0d\_{ij}≥0dij​≥0  
  2. dii=0d\_{ii}=0dii​=0  
  3. dij=djid\_{ij}= d\_{ji}dij​=dji​  
  4. dij≤dik+djkd\_{ij}≤d\_{ik}+d\_{jk}dij​≤dik​+djk​ (∵ 삼각부등식)
* Distance Measure: Euclidean, Manhattan, etc.
* Similarity Measure: Correlation, Jaccard, etc.
* (참고) MDS의 최종목적  
  - 아래 drsd\_{rs}drs​ 식을 바탕으로 xrx\_{r}xr​, xsx\_{s}xs​를 찾아내는 것

drs2=(xr−xs)T(xr−xs)d\_{rs}^2=(x\_r-x\_s )^T (x\_r-x\_s)drs2​=(xr​−xs​)T(xr​−xs​)

**[2] Extract the coordinates that preserve the distance information 단계**

* 거리 정보를 보존하는 좌표 시스템을 찾는 단계이다.
* D라는 distance matrix에서 한 번에 x를 구하기 어려우므로, B라는 매개체인 내적 Matrix를 도출하고 그 다음에 X를 구한다.

D(n×n)→B(n×n)→X(d×n)⇔D≔(Xr−Xs)T(Xr−Xs)→B≔XrTXs→X≔XD\_{(n×n)} → B\_{(n×n)} → X\_{(d×n)} ⇔ D ≔ (X\_r-X\_s )^T (X\_r-X\_s ) → B ≔ X\_r^T X\_s → X ≔ XD(n×n)​→B(n×n)​→X(d×n)​⇔D:=(Xr​−Xs​)T(Xr​−Xs​)→B:=XrT​Xs​→X:=X

* B는 다음과 같이 정의된며 몇 가지 가정을 따른다.

[B]rs=brs=XrTXs[B]\_rs=b\_rs=X\_r^T X\_s[B]r​s=br​s=XrT​Xs​

* 가정  
  1. ∑r=1nxri=0(i=1,2,…,p)∑\_{r=1}^{n}x\_{ri}=0 (i=1,2,…,p)∑r=1n​xri​=0(i=1,2,…,p), 모든 변수의 합은 0이다.  
  2. drs2=(Xr−Xs)T(Xr−Xs)=XrTXr+XsTXS−2XrTXsd\_{rs}^{2}=(X\_r-X\_s )^T (X\_r-X\_s )=X\_r^T X\_r+X\_s^T X\_S-2X\_r^T X\_sdrs2​=(Xr​−Xs​)T(Xr​−Xs​)=XrT​Xr​+XsT​XS​−2XrT​Xs​
* r에 대한 합 (1):  
  ![R](https://velog.velcdn.com/images%2Feuisuk-chung%2Fpost%2F09dba57c-3625-4a4a-b976-de914c34727a%2Fimage.png)
* s에 대한 합 (2):  
  ![S](https://velog.velcdn.com/images%2Feuisuk-chung%2Fpost%2F308c36cc-e1c7-46c4-9f1a-5d7e7e713f3a%2Fimage.png)
* r과 s에 대한 합 (3):  
  ![R-S](https://velog.velcdn.com/images%2Feuisuk-chung%2Fpost%2F6fd4b43a-dfe2-4042-81f6-f1486c43e6c1%2Fimage.png)
* B(inner product matrix)를 구해보자  
  ![B(inner product matrix)](https://velog.velcdn.com/images%2Feuisuk-chung%2Fpost%2F7924bb4f-5256-4fb1-bd98-0b9dc602dcdb%2Fimage.png)
* 좌표시스템 X를 구해보자. B는 이미 앞에서 언급했듯이 다음과 같이 정의될 수 있다.

B(n×n)=XXTB\_{(n×n)}=XX^TB(n×n)​=XXT

rank(B)=rank(XXT)=rank(X)=prank(B)=rank(XX^T )=rank(X)=prank(B)=rank(XXT)=rank(X)=p

(X(n×p)X\_{(n×p)}X(n×p)​, rank는 선형독립인 열들의 최대의 개수를 의미하며, p<n조건을 만족한다.)

* 이때 행렬 B는 inner product matrix 이기 때문에 다음과 같은 성질을 만족하고, 0인 eigenvalue값들을 제거하면 다음과 같이 표현할 수 있다.

![eigenvalue](https://velog.velcdn.com/images%2Feuisuk-chung%2Fpost%2F8d9d05a4-1b0f-452f-abad-beaf0c19b2e5%2Fimage.png)

* B=XXTB = XX^TB=XXT이므로, X=V1Λ11/2X = V\_{1} Λ\_{1}^{1/2}X=V1​Λ11/2​임을 구할 수 있다.

긴 글 읽어주셔서 감사합니다 ^~^