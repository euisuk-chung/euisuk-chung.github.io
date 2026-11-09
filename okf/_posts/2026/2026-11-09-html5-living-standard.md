---
type: "Concept Note"
title: "[개념] HTML5란 무엇인가 — HTML 4.01에서 오늘날의 웹 표준까지"
description: "HTML 4.01과 현대 HTML로 같은 페이지를 작성해 문서 구조, 양식 검증, 미디어의 차이를 살펴보고 HTML Living Standard가 무엇인지 설명합니다."
date: "2026-11-09"
tags:
  - "개념정리"
  - "IT지식"
resource: "https://html.spec.whatwg.org/"
generated:
  by: "process:blog-review"
  at: "2026-11-09T15:56:41+09:00"
sources:
  - id: "whatwg:html-living-standard"
    resource: "https://html.spec.whatwg.org/"
    title: "HTML Living Standard"
    author: "WHATWG"
  - id: "w3c:html401:1999"
    resource: "https://www.w3.org/TR/1999/REC-html401-19991224/"
    title: "HTML 4.01 Specification"
    author: "W3C"
  - id: "w3c:html5:2014"
    resource: "https://www.w3.org/TR/2014/REC-html5-20141028/"
    title: "HTML5 Recommendation, 28 October 2014"
    author: "W3C"
  - id: "w3c:html5-differences:2014"
    resource: "https://www.w3.org/TR/2014/NOTE-html5-diff-20141209/"
    title: "HTML5 Differences from HTML4"
    author: "W3C"
  - id: "w3c:whatwg-mou:2019"
    resource: "https://www.w3.org/2019/04/WHATWG-W3C-MOU.html"
    title: "Memorandum of Understanding Between W3C and WHATWG"
    author: "W3C and WHATWG"
  - id: "w3c:html-aam"
    resource: "https://www.w3.org/TR/html-aam-1.0/"
    title: "HTML Accessibility API Mappings"
    author: "W3C"
  - id: "whatwg:fetch"
    resource: "https://fetch.spec.whatwg.org/"
    title: "Fetch Standard"
    author: "WHATWG"
  - id: "w3c:geolocation"
    resource: "https://www.w3.org/TR/geolocation/"
    title: "Geolocation"
    author: "W3C"
status: "stable"
year: "2026"
---

## HTML은 브라우저에 문서의 구조를 알려 줍니다

웹페이지에 `<h1>도서관 소식</h1>`을 쓰면, 브라우저는 그 글자를 문서의 최상위 제목으로 해석합니다. `<a href="/hours">운영 시간</a>`은 다른 주소로 이동하는 링크입니다. `<a>`와 `</a>`는 요소의 시작과 끝을 나타내는 **태그**이고, `href`는 이동할 주소를 적는 **속성**입니다. 이렇게 텍스트와 이미지에 역할과 관계를 표시하는 언어가 HTML(HyperText Markup Language)입니다. [WHATWG HTML 입문](https://html.spec.whatwg.org/multipage/introduction.html#a-quick-introduction-to-html)

브라우저는 HTML을 읽어 요소와 텍스트가 트리처럼 연결된 **DOM(Document Object Model)**을 만듭니다. CSS는 그 요소들의 크기·색·배치를 정하고, JavaScript는 클릭에 반응하거나 DOM의 내용을 바꿀 수 있습니다. HTML 요소에도 기본 동작이 있습니다. 링크는 이동하고, 버튼은 키보드로 누를 수 있으며, 입력 양식은 브라우저가 제출할 수 있습니다. 이 역할들을 알고 나면 어느 부분을 HTML에 쓰고 어느 부분을 CSS나 스크립트로 처리할지 판단하기 쉬워집니다. [WHATWG HTML의 범위](https://html.spec.whatwg.org/multipage/introduction.html#scope) · [HTML 파싱 모델](https://html.spec.whatwg.org/multipage/parsing.html#overview-of-the-parsing-model)

## HTML5는 역사적으로 어떤 이름인가요?

HTML 4.01은 1999년에 나온 W3C 권고안입니다. 이 글에서는 ‘옛날 HTML’의 비교 기준으로 이 버전을 사용합니다. HTML 4.01에도 제목, 문단, 링크, 표, 양식이 있었고 CSS와 스크립트도 사용할 수 있었습니다. 2014년 W3C가 권고한 **HTML5**는 이 토대 위에 문서의 역할을 표현하는 요소, 브라우저의 미디어 재생과 입력 기능, 브라우저가 HTML을 해석하는 세부 규칙을 더한 주요 개정판입니다. [W3C HTML 4.01](https://www.w3.org/TR/1999/REC-html401-19991224/) · [2014년 HTML5 권고안](https://www.w3.org/TR/2014/REC-html5-20141028/) · [HTML4와 HTML5의 차이](https://www.w3.org/TR/2014/NOTE-html5-diff-20141209/)

오늘날 ‘HTML5’는 현대 HTML과 관련 웹 기술을 넓게 부르는 이름으로도 쓰입니다. 새 페이지를 만들 때 기능의 정의를 확인하는 문서는 계속 갱신되는 **WHATWG HTML Living Standard**입니다. W3C와 WHATWG는 2019년에 HTML과 DOM을 하나의 개발 흐름에서 발전시키기로 합의했습니다. 그래서 ‘최신 HTML5’ 기능을 찾을 때는 2014년 문서의 버전 번호보다 현재 표준에서 해당 요소나 속성을 찾는 편이 정확합니다. [WHATWG의 ‘Is this HTML5?’](https://html.spec.whatwg.org/multipage/introduction.html#is-this-html5?) · [W3C·WHATWG 협력 합의](https://www.w3.org/2019/04/WHATWG-W3C-MOU.html)

| 비교할 부분 | HTML 4.01 | HTML5 이후의 HTML |
| --- | --- | --- |
| 문서 선언 | Strict·Transitional·Frameset 중 문서 유형 정의(DTD)를 가리킵니다. | `<!doctype html>`로 시작해 브라우저의 표준 모드를 사용합니다. |
| 문서 영역 | `h1`, `p`, `ul` 등으로 구조를 나타내고 큰 영역은 `div`로 묶을 수 있습니다. | `nav`, `main`, `article` 등으로 영역의 역할도 표시합니다. |
| 입력 | `form`, `label`, 텍스트 입력과 버튼을 지원합니다. | 이메일처럼 입력의 종류를 선언하고 기본 형식 검사와 필수 입력을 요청할 수 있습니다. |
| 미디어 | 파일에 링크하거나 `object` 등으로 외부 리소스를 삽입할 수 있습니다. | `video`, `audio`, `track`으로 재생과 자막을 문서에 표현합니다. |
| HTML 해석 | 문서가 지켜야 할 구조를 DTD로 선언합니다. | 브라우저가 텍스트에서 DOM을 만드는 과정과 잘못된 입력의 처리도 구체적으로 정의합니다. |

[HTML 4.01 문서 구조](https://www.w3.org/TR/html401/struct/global.html) · [W3C 변경 목록](https://www.w3.org/TR/2014/NOTE-html5-diff-20141209/) · [WHATWG HTML 파싱](https://html.spec.whatwg.org/multipage/parsing.html)

## 같은 도서관 페이지를 두 방식으로 쓰기

운영 시간 링크, 도서관 소식, 이메일 구독 양식이 있는 페이지를 비교해 봅시다. 아래는 HTML 4.01 Strict의 구조에 맞춘 예시입니다. 탐색 영역과 주요 내용은 `div`의 `id`로 구분합니다.

```html
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
  "http://www.w3.org/TR/html4/strict.dtd">
<html lang="ko">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <title>동네 도서관</title>
</head>
<body>
  <div id="site-header">
    <p>동네 도서관</p>
    <ul id="site-nav">
      <li><a href="/hours">운영 시간</a></li>
    </ul>
  </div>
  <div id="content">
    <h1>도서관 소식</h1>
    <p>토요일에 어린이 독서 모임이 열립니다.</p>
    <form action="/subscriptions" method="post">
      <p>
        <label for="email">이메일</label>
        <input id="email" name="email" type="text">
        <button type="submit">구독</button>
      </p>
    </form>
  </div>
</body>
</html>
```

현대 HTML로 같은 내용을 작성하면 다음과 같습니다.

```html
<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <title>동네 도서관</title>
</head>
<body>
  <header>
    <p>동네 도서관</p>
    <nav aria-label="주 메뉴">
      <ul>
        <li><a href="/hours">운영 시간</a></li>
      </ul>
    </nav>
  </header>
  <main>
    <article>
      <h1>도서관 소식</h1>
      <p>토요일에 어린이 독서 모임이 열립니다.</p>
    </article>
    <form action="/subscriptions" method="post">
      <p>
        <label for="email">이메일</label>
        <input id="email" name="email" type="email" required>
        <button type="submit">구독</button>
      </p>
    </form>
  </main>
</body>
</html>
```

- **첫 줄과 문자 인코딩이 짧아졌습니다.** HTML 4.01의 선언은 문서가 따르는 DTD를 지정합니다. 현대 HTML에서 짧은 선언은 브라우저가 오래된 페이지의 배치를 흉내 내는 *quirks mode* 대신 표준 모드로 문서를 처리하도록 합니다. `<meta charset="utf-8">`은 문서의 글자를 UTF-8로 읽도록 선언합니다. 실제 파일도 UTF-8로 저장해야 합니다. [HTML 4.01 문서 유형 선언](https://www.w3.org/TR/html401/struct/global.html#h-7.2) · [WHATWG DOCTYPE](https://html.spec.whatwg.org/multipage/syntax.html#the-doctype) · [문자 인코딩 선언](https://html.spec.whatwg.org/multipage/semantics.html#charset)
- **영역의 용도를 요소 이름에 담았습니다.** `nav`는 주요 탐색 링크, `main`은 페이지의 중심 내용, `article`은 따로 읽을 수 있는 글에 사용합니다. `div id="site-nav"`의 이름은 작성자의 규칙이고, `nav`의 역할은 표준에 정의됩니다. 이 차이 덕분에 보조 기술은 탐색 영역과 본문을 구분할 수 있습니다. 별도 의미가 없는 묶음에는 여전히 `div`가 적합합니다. [WHATWG 문서 영역](https://html.spec.whatwg.org/multipage/sections.html) · [본문과 div](https://html.spec.whatwg.org/multipage/grouping-content.html#the-main-element) · [HTML 접근성 매핑](https://www.w3.org/TR/html-aam-1.0/)
- **양식에 입력 조건을 적을 수 있습니다.** 두 예시 모두 `label`의 `for`를 입력의 `id`와 맞춥니다. 두 번째 예시는 `type="email"`로 이메일 형식을 확인하고 `required`로 빈 입력의 제출을 막습니다. 이 검사는 브라우저에서 입력 실수를 줄여 줍니다. 이메일이 실제로 존재하는지 확인하려면 별도의 확인 절차가 필요하며, 받은 값을 검증하고 구독을 처리하는 일은 서버가 담당합니다. `/subscriptions`는 그 서버 주소를 보여 주기 위한 예시입니다. [HTML 4.01의 양식](https://www.w3.org/TR/html401/interact/forms.html) · [WHATWG 이메일 입력](https://html.spec.whatwg.org/multipage/input.html#e-mail-state-(type=email)) · [양식 검증](https://html.spec.whatwg.org/multipage/forms.html#client-side-form-validation)

## 미디어와 문서 해석에서 바뀐 점

과거 문서가 영상을 별도 링크나 `object`로 연결하는 데 비해, `video`에는 브라우저가 처리할 영상 소스, 재생 버튼, 자막을 직접 선언할 수 있습니다. 다음은 영상과 한국어 자막 파일이 준비됐을 때의 예입니다. 지원되는 파일 형식과 코덱은 실행 환경에서 확인할 항목입니다. `canvas`는 이와 다른 기능으로, 스크립트가 그림이나 애니메이션을 그릴 표면을 제공합니다. [HTML 4.01의 object](https://www.w3.org/TR/html401/struct/objects.html#h-13.3) · [WHATWG 미디어 요소](https://html.spec.whatwg.org/multipage/media.html#the-video-element) · [Canvas](https://html.spec.whatwg.org/multipage/canvas.html#the-canvas-element)

```html
<video controls>
  <source src="library-tour.mp4" type="video/mp4">
  <track kind="captions" src="library-tour.ko.vtt"
         srclang="ko" label="한국어">
</video>
<p><a href="library-tour.mp4">영상 파일 열기</a></p>
```

또 한 가지 차이는 화면에 바로 드러나지 않습니다. `<p>소개<div>공지</div></p>`처럼 문단 안에 `div`를 넣으면, 브라우저는 `div` 앞에서 문단을 먼저 닫습니다. 개발자 도구에서 보면 `div`는 문단의 자식이 아니라 옆에 있는 요소입니다. 브라우저가 어떻게 DOM을 만드는지 표준에 규칙이 있어서, 소스와 화면 사이의 차이를 설명할 수 있습니다. 잘못된 중첩을 고칠 때도 HTML 소스와 개발자 도구에 표시된 DOM을 함께 보는 이유입니다. [WHATWG 문단 요소](https://html.spec.whatwg.org/multipage/grouping-content.html#the-p-element) · [HTML 파싱 규칙](https://html.spec.whatwg.org/multipage/parsing.html#parsing-main-inbody)

## 요즘 HTML에서 할 수 있는 일

현재 HTML 표준에는 접었다 펼치는 `details`, 모달로 열 수 있는 `dialog`, 짧은 안내를 띄우는 `popover`가 있습니다. 아래에서는 버튼의 `popovertarget` 값과 안내 요소의 `id`를 맞춥니다. 이를 지원하는 브라우저에서는 버튼을 누르면 안내가 열리고, 기본 팝오버는 바깥을 클릭하거나 Esc 키로 닫을 수 있습니다. 스크립트로 토글 동작을 직접 만들 필요가 없는 작은 예입니다. [WHATWG 대화형 요소](https://html.spec.whatwg.org/multipage/interactive-elements.html) · [Popover 표준](https://html.spec.whatwg.org/multipage/popover.html)

```html
<button type="button" popovertarget="signup-help">구독 안내</button>
<div id="signup-help" popover>
  소식은 한 달에 한 번 이메일로 보냅니다.
</div>
```

‘HTML5’라는 넓은 표현 안에는 여러 표준이 섞여 쓰이기도 합니다. `video`와 `popover`는 HTML 표준에서 정의합니다. JavaScript에서 네트워크에 요청하는 `fetch()`는 Fetch 표준에서, 위치를 요청하는 API는 Geolocation 표준에서 정의합니다. 모바일에서 읽기 좋은 배치는 HTML 구조 위에 적용하는 CSS와도 관련이 있습니다. 쓰려는 기능의 이름으로 해당 표준과 지원 범위를 확인하면, ‘HTML5를 지원한다’는 말보다 구체적으로 판단할 수 있습니다. [WHATWG HTML의 위치](https://html.spec.whatwg.org/multipage/introduction.html#where-does-this-specification-fit?) · [Fetch 표준](https://fetch.spec.whatwg.org/) · [Geolocation 표준](https://www.w3.org/TR/geolocation/)
