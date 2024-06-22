> 미디움 포스트에서 읽기: [Upgrading Ele.me to Progressive Web Apps](https://medium.com/elemefe/upgrading-ele-me-to-progressive-web-app-2a446832e509)

(*해당 글은 영문 원문을 번역한 것입니다.*)

## Ele.me의 Progressive Web App 업그레이드

Vue.js의 첫 실험 트윗 이후, 저희 Ele.me(중국 최대의 음식 주문 및 배달 회사)는 모바일 웹사이트를 Progressive Web App으로 업그레이드하는 작업을 시작했습니다. 중국 시장을 위해 세계 최초로 PWA를 출시하게 되어 자랑스럽지만, Google, UC, Tencent와 협력하여 중국 내 웹 경험과 브라우저 지원의 경계를 확장하는 것에 더 큰 자부심을 느낍니다.

## 멀티 페이지, Vue, PWA?

SPA(단일 페이지 애플리케이션)로 웹 앱을 구조화해야만 앱 같은 사용자 경험을 제공하는 PWA를 구축할 수 있다는 의견이 지배적입니다. 대표적인 예로는 Twitter Lite, Flipkart Lite, Housing Go, Polymer Shop이 모두 SPA 모델을 사용합니다.

그러나 Ele.me에서는 멀티 페이지 앱 모델의 많은 장점을 이해하게 되었고, 1년 전 Angular 1 SPA에서 멀티 페이지 앱으로 모바일 사이트를 리팩토링하기로 결정했습니다. 가장 중요한 장점은 페이지 간의 격리와 디커플링으로, 이를 통해 모바일 사이트의 다양한 부분을 "마이크로서비스"로 구축할 수 있습니다. 이러한 서비스는 독립적으로 반복할 수 있고, 서드파티 앱에 임베드할 수 있으며, 심지어 다른 팀에서 유지 관리할 수 있습니다.

한편, 생산성을 높이기 위해 Vue.js를 활용하고 있습니다. Vue는 React나 Angular의 경쟁자로 알려져 있지만, 가벼운 무게와 성능 덕분에 멀티 페이지 앱을 엔지니어링할 때 전통적인 "jQuery/Zepto + 템플릿 엔진" 스택의 완벽한 대체재가 됩니다. 모든 컴포넌트를 싱글 파일 컴포넌트로 구축하여 페이지 간에 쉽게 공유할 수 있습니다. Vue의 선언적이고 반응적인 특성은 코드와 데이터 흐름을 관리하는 데 도움을 줍니다. 그리고 Vue는 점진적이기 때문에, 사이트의 복잡도가 증가할 경우 Vuex나 Vue-Router를 점진적으로 도입할 수 있습니다.

2017년에는 PWA가 유행하면서, Vue 기반 멀티 페이지 PWA가 실제로 얼마나 갈 수 있는지 탐구하기 시작했습니다.

## MPA에서 "PRPL" 구현

PRPL 패턴을 좋아하는 이유는 PWA 시스템을 구조화하고 설계하는 방법에 대한 높은 수준의 추상화를 제공하기 때문입니다. 모든 것을 처음부터 다시 구축하지 않기 때문에 PRPL을 구현하는 것을 마이그레이션 목표로 삼았습니다:

### 1. 초기 URL 라우트를 위한 중요한 리소스를 PUSH

PUSH/프리로드의 핵심은 깊은 의존성 그래프에 숨겨진 리소스를 우선 순위로 두고 브라우저의 네트워크 스택을 ASAP으로 바쁘게 만드는 것입니다. 예를 들어, 라우트별 코드 분할이 있는 SPA에서는 "엔트리 청크"가 다운로드 및 평가를 완료하기 전에 현재 라우트의 청크를 푸시/프리로드할 수 있습니다. 이렇게 하면 실제 페치가 발생할 때 이미 캐시에 있을 수 있습니다.

MPA의 라우트는 자연스럽게 해당 라우트의 코드만 가져오며, 의존성 그래프가 평탄화되는 경향이 있습니다. 대부분의 Ele.me 스크립트는 `<script>` 요소이므로 명시적 `<link rel="preload">` 없이도 초기 파싱 단계에서 [좋은 오래된 브라우저 프리로더](https://calendar.perfplanet.com/2013/big-bad-preloader/)에 의해 찾아지고 페치될 수 있습니다.

HTTP2 멀티플렉싱의 이점을 누리기 위해 모든 중요한 리소스를 단일 도메인에서 제공하고 있으며, 서버 푸시를 실험 중입니다.

### 2. 초기 라우트를 렌더링하고 가능한 한 빨리 인터랙티브하게 만들기

이 부분은 MPA에서는 본질적으로 무료입니다. 단순 HTML 탐색을 사용하기 때문에 MPA는 이러한 측면에서 자연스러운 이점을 가집니다.

### 3. 서비스 워커를 사용하여 나머지 라우트를 사전 캐싱

여기서 서비스 워커가 등장합니다. 서비스 워커는 요청을 가로채고 캐시에서 응답을 제공하는 클라이언트 측 프록시로 알려져 있지만, 주도적으로 페치를 수행하여 미래의 리소스를 프리페치 및 프리캐시할 수도 있습니다.

저희는 이미 `.vue` 컴파일과 자산 버전 관리를 위해 Webpack을 사용하고 있으므로, "프리캐시 매니페스트"에 의존성을 수집하고 각 빌드 후에 새로운 서비스 워커 파일을 생성하는 Webpack 플러그인을 작성했습니다. 이는 [SW-Precache가 작동하는 방식](https://medium.com/@Huxpro/how-does-sw-precache-works-2d99c3d3c725)과 유사합니다.

**사실, "중요한 라우트"로 표시된 라우트의 의존성만 수집합니다.** 이를 "앱 셸" 또는 앱의 "설치 패키지"로 생각할 수 있습니다. 이러한 라우트가 성공적으로 캐시/설치되면 웹 앱은 캐시에서 직접 부팅할 수 있으며 오프라인에서도 사용할 수 있습니다. "중요하지 않은" 라우트는 첫 방문 시 런타임에 점진적으로 캐시됩니다. [SW-Toolbox](https://googlechrome.github.io/sw-toolbox/)가 제공하는 LRU 캐시 정책과 TTL 무효화 메커니즘 덕분에 장기적으로 할당량 초과에 대한 걱정은 없습니다.

### 4. 나머지 라우트를 필요할 때 지연 로드 및 인스턴스화

나머지 앱 부분을 지연 로드하고 지연 인스턴스화하는 것은 SPA에서 달성하기 상대적으로 어렵습니다. 이는 코드 분할 및 비동기 가져오기를 모두 요구합니다. 다행히 MPA 모델에서는 라우트가 자연스럽게 분리됩니다.

요청된 라우트가 서비스 워커 캐시에 이미 프리캐시되어 있는 경우, SPA나 MPA를 사용하더라도 지연 로딩은 즉시 수행될 수 있습니다.

---

놀랍게도, 멀티 페이지 PWA는 자연스럽게 "PRPL"입니다! MPA는 이미 "PRL"에 대한 내장 지원을 제공하며, 서비스 워커와 관련된 두 번째 "P"는 어떤 PWA에서도 쉽게 충족될 수 있습니다.

그렇다면 최종 결과는 어떨까요?

**[Lighthouse](https://developers.google.com/web/tools/lighthouse/) 시뮬레이션(3G 및 5배 느린 CPU)에서, 인터랙티브 시간(Time-To-Interactive)을 약 2초로 만들었습니다.** 이는 HTTP1 테스트 서버에서 벤치마크된 결과입니다.

첫 방문은 빠릅니다. 서비스 워커가 있는 반복 방문은 훨씬 더 빠릅니다. 서비스 워커가 있는 경우와 없는 경우의 큰 차이를 볼 수 있는 비디오를 확인할 수 있습니다:

<iframe width="560" height="315" src="https://www.youtube.com/embed/mbi_WnunJa8" frameborder="0" allowfullscreen></iframe>

보셨나요? 아니, 그 귀찮은 빈 화면을 말하는 겁니다. 서비스 워커가 있는 경우에도 탐색 중 빈 화면이 눈에 띕니다. 그 이유는 무엇일까요?

## 멀티 페이지의 함정: 모든 것을 다시 해야 한다!

SPA와 달리, MPA에서는 라우트를 변경하면 실제 브라우저 탐색이 발생합니다. 이전 페이지는 완전히 폐기되고 브라우저는 다음 라우트를 위해 모든 작업을 다시 해야 합니다: 리소스 재다운로드, HTML 재파싱, JavaScript 재평가, 이미지 데이터 재디코딩, 페이지 재레이아웃 및 재페인팅, 심지어 많은 것이 라우트 간에 공유될 수 있음에도 불구하고 모든 작업을 다시 해야 합니다. 이 모든 작업이 결합되어 상당한 컴퓨팅과 시간이 필요합니다.

아래는 엔트리 페이지(가장 무거운 페이지)의 프로파일입니다(2배 느린 CPU 시뮬레이션). 반복 방문 시 인터랙티브 시간을 약 1초로 만들 수 있지만, 사용자들은 탭 전환만으로도 너무 느리다고 느낄 수 있습니다.

### 거대한 JavaScript 재시작 비용

프로파일에 따르면 첫 페인트 전에 대부분의 시간(900ms)은 JavaScript 평가에 사용됩니다. 절반은 Vue 런타임, 컴포넌트, 라이브러리 등 의존성에 사용되고, 나머지 절반은 실제 Vue 시작 및 마운팅에 사용됩니다. 모든 UI 렌더링이 JavaScript/Vue에 의존하기 때문에 모든 중요한 스크립트는 여전히 파서 블로킹 상태입니다. 여기서 JavaScript나 Vue의 오버헤드를 비난하려는 것은 아닙니다. 엔지니어링에서 이 추상화 계층이 필요한 경우의 트레이드오프일 뿐입니다.

**SPA에서는 JavaScript 시작 비용

이 전체 수명 주기 동안 분산됩니다.** 각 스크립트에 대한 파싱/컴파일은 한 번만 이루어지며, 많은 무거운 실행도 한 번만 이루어질 수 있습니다. Vue의 ViewModel 및 가상 DOM과 같은 큰 JavaScript 객체는 메모리에 유지되고 원하는 만큼 재사용될 수 있습니다. **그러나 MPA에서는 그렇지 않습니다.**

### 브라우저 캐시가 도움이 될까요?

그렇기도 하고 아닐 수도 있습니다.

V8은 코드 캐싱을 도입하여 로컬 복사본을 저장해 다음 번에 페치, 파싱 및 컴파일을 모두 건너뛸 수 있습니다. @addyosmani가 JavaScript 시작 성능에서 언급한 것처럼, 서비스 워커를 통해 캐시 스토리지에 저장된 스크립트는 첫 실행 시 코드 캐싱을 트리거할 수 있습니다.

다른 브라우저 캐시로는 "Back-Forward Cache" 또는 bfcache가 있습니다. Opera의 "Fast History Navigation" 또는 WebKit의 "Page Cache"로도 알려져 있습니다. **이 아이디어는 브라우저가 이전 페이지를 메모리에 살아 있게 유지하여 DOM/JS 상태를 파괴하지 않는 것입니다.** 이 아이디어는 MPA에 매우 잘 작동합니다. iOS Safari에서 모든 전통적인 멀티 페이지 웹사이트를 시도해 보면 뒤로/앞으로 탐색할 때 즉시 로딩되는 것을 볼 수 있습니다.

불행히도, 메모리 소비와 멀티 프로세스 아키텍처 때문에 Chrome에는 현재 이러한 유형의 인메모리 bfcache가 없습니다. 이는 HTTP 디스크 캐시를 활용하여 로딩 파이프라인을 단순화하지만 거의 모든 작업이 여전히 다시 이루어져야 합니다.

## 인지된 성능을 위한 노력

현실이 어두워도 쉽게 포기하고 싶지는 않습니다. 시도해 볼 수 있는 최적화 중 하나는 DOM 노드를 가능한 한 적게 렌더링하거나 가상 DOM 노드를 생성하여 인터랙티브 시간을 개선하는 것입니다. 또 다른 기회는 인지된 성능을 개선하기 위한 트릭을 사용하는 것입니다.

@owencm이 인지된 성능과 사용자 경험을 개선하기 위해 "Skeleton Screen"과 "요소의 미리 정의된 크기를 통한 안정적인 로딩"을 다루는 훌륭한 게시물을 작성했습니다. 저희도 실제로 둘 다 사용했습니다.

기술적인 세부 사항에 들어가기 전에 이러한 최적화 후의 최종 결과를 먼저 보여드리고 싶습니다. 여기 있습니다!

<iframe width="560" height="315" src="https://www.youtube.com/embed/K5JBGnMYO1s" frameborder="0" allowfullscreen></iframe>

CPU가 10배 느린 상태에서 Skeleton Screen이 어떻게 보이는지 확인할 수 있는 버전입니다.

<iframe width="560" height="315" src="https://www.youtube.com/embed/w1ZbNsHmRjs" frameborder="0" allowfullscreen></iframe>

훨씬 나은 UX죠? 느린 장치에서도 탐색 속도가 느릴지라도 UI가 안정적이고 일관되며 항상 반응하는 상태를 유지합니다. 어떻게 거기에 도달했는지 알아볼까요?

### Vue로 빌드 시 Skeleton Screen 렌더링

예상하셨겠지만, 마크업, 스타일 및 이미지를 포함하는 Skeleton Screen은 각 라우트의 `*.html`에 인라인되어 있습니다. 따라서 서비스 워커에 의해 캐시되고 즉시 로드되며 JavaScript 없이도 독립적으로 렌더링될 수 있습니다.

각 라우트에 대해 Skeleton Screen을 수동으로 작성하고 싶지는 않습니다. 이는 지루한 작업이며 Skeleton Screen과 실제 UI 컴포넌트 간의 모든 변경 사항을 수동으로 동기화해야 합니다. (각 라우트를 Vue 컴포넌트로 취급합니다.) 하지만 생각해보면, Skeleton Screen은 정보를 점진적으로 로드하는 페이지의 빈 버전일 뿐입니다. 이를 실제 UI 컴포넌트의 로딩 상태로 구워넣어 Skeleton Screen을 동기화 문제 없이 직접 렌더링할 수 있다면 어떨까요?

Vue의 다재다능함 덕분에, 실제 서버에서 사용하는 대신 빌드 시 Vue 컴포넌트를 문자열로 렌더링하고 HTML 템플릿에 주입하여 이를 실현할 수 있습니다.

### 빠른 Skeleton 페인팅...

`*.html`에 마크업이 있다고 해서 페인팅이 빠르게 이루어지는 것은 아닙니다. [중요 렌더링 경로](https://developers.google.com/web/fundamentals/performance/critical-rendering-path/)가 최적화되어야 합니다. 많은 개발자들은 스크립트 태그를 본문 끝에 두는 것이 스크립트 실행 전에 콘텐츠를 페인팅하기에 충분하다고 믿습니다. 이는 불완전한 DOM 트리를 렌더링할 수 있는 브라우저(예: 스트리밍 렌더링)에서는 사실일 수 있지만, 모바일에서는 하드웨어가 느리고 배터리와 열 문제 때문에 브라우저가 그렇게 하지 않을 수 있습니다. **그리고 `async` 또는 `defer`가 파서 블로킹이 아니라고 말해도, 실제로 스크립트 실행 전에 콘텐츠를 페인팅할 수 있다는 의미는 아닙니다.**

`async` 스크립트는 사용 가능해지는 즉시 평가되므로 잠재적으로 파서를 블로킹할 수 있습니다. 오직 `defer`만이 파서를 절대 블로킹하지 않는다고 명시되어 있습니다. 그래서 [Steve Souders](http://stevesouders.com/)는 ["Prefer DEFER Over ASYNC"](https://calendar.perfplanet.com/2016/prefer-defer-over-async/)라는 게시물을 작성했습니다. (`defer`에도 자체 문제가 있으며 나중에 다루겠습니다.)

**파서를 블로킹하지 않는 스크립트도 페인팅을 블로킹할 수 있습니다.** 그래서 저는 **"Minimal Multi-page PWA"**라는 테스트를 작성하여 `async` 스크립트 내에서 1000개의 리스트 항목을 렌더링하고 Skeleton Screen을 스크립트 실행 전에 페인팅할 수 있는지 확인했습니다. 아래 프로파일은 제 무지를 보여줍니다:

네, 첫 페인트가 블로킹됩니다. 저도 여기서 놀랐습니다. **DOM을 너무 빨리 수정하면 브라우저가 이전 페인팅 작업을 마치지 못하고 현재 DOM 조작 작업이 완료될 때까지 렌더링 파이프라인을 다시 시작해야 합니다.** 모바일 장치에서는 CPU/GPU가 느리기 때문에 더 자주 발생할 수 있습니다.

### setTimeout 해크로 빠른 Skeleton 페인팅

새로운 아름다운 Skeleton Screen을 테스트할 때 이 문제에 직면했습니다. 아마도 Vue가 너무 빨리 작업을 완료하고 노드를 마운팅했기 때문일 것입니다. 어쨌든 이를 더 느리게, 아니 더 게으르게 만들어야 했습니다. 그래서 DOM 조작을 `setTimeout(callback, 0)` 안에 넣어 보았습니다. 그리고 마법처럼 작동했습니다!

**이 유명한 `setTimeout` 해크는 과학™입니다.** **이 코드를 현재 루프에서 실행하지 않고 타이머 콜백과 함께 작업 큐에 넣어 브라우저가 메인 스레드에서 렌더링을 업데이트할 수 있게 합니다.**

그래서 `new Vue()`를 `setTimeout` 안에 넣어 Skeleton Screen이 탐색 후 일관되게 페인팅되도록 했습니다! 최적화 후의 프로파일입니다.

### deferred된 스크립트 문제

여전히 많은 파서 블로킹 스크립트가 있습니다. 대부분은 `defer`된 스크립트입니다. 프로파일에 따르면, 이는 Chrome의 버그일 수 있습니다. [crbug에서 투표하세요](https://bugs.chromium.org/p/chromium/issues/detail?id=717979)!

비슷한 개선은 Lighthouse에서도 볼 수 있습니다. Pro Tip: 항상 가변 제어 접근 방식으로 Lighthouse를 사용하세요.

### 실세계 성능

[Alex Russell](https://medium.com/@slightlylate)은 Chrome Dev Summit 2016에서 모바일 웹 성능에 대한 매우 통찰력 있는 발표를 했습니다. 중국 사용자는 매우 강력한 전화기를 사용하는 경향이 있습니다. MI4는 스냅드래곤 801을 탑재했지만 가격은 100달러에 불과하여 사용자 중 최소 80%가 사용할 수 있습니다.

여기에는 Nexus 5에서 4개의 탭 간 전환을 보여주는 비디오가 있습니다. 탭 간 성능은 규모에 따라 다릅니다. 가장 무거운 엔트리 페이지는 Nexus 5에서 실질적인 Time-To-Interactive를 1초 내외로 만듭니다.

<iframe width="700" height="525" src="https://www.youtube.com/embed/ZLc8jysMqaw?ecver=1" frameborder="0" allowfullscreen></iframe>

## 최종 생각

이 기사는 예상보다 훨씬 길었습니다. 여기까지 읽어 주셔서 감사합니다. 그래서 무엇을 배울 수 있을까요?

### MPA는 여전히 갈 길이 멀다

[Jake Arch

ibald](https://twitter.com/jaffathecake)은 [Chrome Dev Summit 2016](https://youtu.be/J2dOTKBoTL4?list=PLNYkxOF6rcIBTs2KPy1E6tIYaWoFcG3uj)에서 "PWA !== SPA"라고 말했습니다. 그러나 슬픈 진실은 저희가 "PRPL" 패턴, 서비스 워커, 앱 셸, Skeleton Screen과 같은 최신 기술을 활용했음에도 불구하고, 멀티 페이지 구조로 인해 많은 Single Page PWA와는 여전히 거리가 있다는 것입니다.

웹은 매우 다재다능합니다. 정적 블로그, e-비즈니스 사이트, 데스크탑 수준의 소프트웨어, 모두 웹 가족의 일류 시민이 되어야 합니다. MPA는 "bfcache API", 탐색 전환을 통해 SPA를 따라잡을 수 있을지 모르지만, 오늘날에는 그렇지 않습니다.

### PWA는 무엇이든 놀랍다

PWA는 현재 웹 애플리케이션 모델의 근본적인 문제를 해결하려고 합니다. 그래서 어떤 아키텍처나 프레임워크를 사용하더라도 PWA는 항상 유익합니다. [Addy Osmani](https://medium.com/@addyosmani)는 올해 I/O에서 [Production Progressive Web Apps With JavaScript Frameworks](https://events.google.com/io/schedule/?section=may-19&sid=e8436b55-ea89-4243-a644-5ecb319d9ef0)에 대해 발표할 것입니다. 놓치지 마세요!

---

## 감사의 말

- 동료들 [YiSi Wang](https://github.com/YiSiWang), [GuangHui Ren](https://github.com/rguanghui), [JiyinYiyong](https://medium.com/@jiyinyiyong)
- 협력자 [Michael Yeung](https://medium.com/@micyeung), [Liam Spradlin](https://medium.com/@LiamSpradlin) 및 Google의 다른 협력자
- UC/Tencent의 협력자들
- 초청 리뷰어 [Evan You](https://medium.com/@youyuxi)
- Chrome “StackOverflow” [Jake Archibald](https://twitter.com/jaffathecake)

---

## 부록. 아키텍처 다이어그램

![](/img/in-post/post-eleme-pwa/Architecture.png)

[1]: https://twitter.com/vuejs/status/834087199008239619
[2]: https://developers.google.com/web/progressive-web-apps/
[3]: https://blog.twitter.com/2017/how-we-built-twitter-lite
[4]: https://medium.com/progressive-web-apps/building-flipkart-lite-a-progressive-web-app-2c211e641883
[5]: https://medium.com/engineering-housing/progressing-mobile-web-fac3efb8b454
[6]: https://shop.polymer-project.org/
[7]: https://developers.google.com/web/fundamentals/performance/prpl-pattern/
[8]: https://calendar.perfplanet.com/2013/big-bad-preloader/
[9]: https://w3c.github.io/ServiceWorker/v1/
[10]: https://webpack.github.io/
[11]: https://medium.com/@Huxpro/how-does-sw-precache-works-2d99c3d3c725
[12]: https://developers.google.com/web/updates/2015/11/app-shell
[13]: https://googlechrome.github.io/sw-toolbox/