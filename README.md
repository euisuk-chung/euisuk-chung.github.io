[서쿠 개발노트⭐](https://euisuk-chung.github.io)
================================

Euisuk Chung의 개발 블로그. Jekyll 기반 GitHub Pages 사이트이며, [velog](https://velog.io/@euisuk-chung) 글을 매월 자동으로 동기화합니다.

주제: Machine Learning · Time Series · Anomaly Detection · NLP · Vision · MLOps

--------------------------------------------------

### Getting Started

[운영 매뉴얼 👉](_doc/Manual.md)

1. **Ruby 3 이상**과 [Bundler](https://bundler.io/)가 필요합니다.
   macOS 기본 Ruby(2.6)로는 `ffi` 의존성 때문에 `bundle install`이 실패하니
   Homebrew Ruby를 쓰세요:

```sh
brew install ruby
export PATH="/opt/homebrew/opt/ruby/bin:$PATH"   # ~/.zshrc 에 추가
```

2. 의존성 설치:

```sh
bundle install    # Ruby (Jekyll)
npm install       # Node (에셋 빌드)
```

3. 로컬 서버 실행 (기본 `localhost:4000`):

```sh
bundle exec jekyll serve   # 또는 npm start
```

---

### 에셋 빌드

테마 스타일과 스크립트는 `less/`와 `js/blog.js`가 원본이고, `css/blog*.css`·`js/blog.min.js`는 빌드 산출물입니다. **산출물을 직접 수정하지 마세요** — 다음 빌드에서 덮어써집니다.

```sh
npm run build     # less/ → css/, js/blog.js → js/blog.min.js (압축 포함)
npm run watch     # 변경 감지 후 자동 재빌드
npm run dev       # watch + jekyll serve 동시 실행
```

빌드는 [esbuild](https://esbuild.github.io/)와 [less](https://lesscss.org/)만 사용합니다 (`build.mjs`). 산출물에는 Apache 2.0 준수를 위한 저작권 배너가 자동으로 삽입됩니다.

태그 사전은 `_concepts/`에 있으며 파일 하나가 `/tags/<slug>/` 페이지 하나가 됩니다(자세한 규칙은 `_doc/Manual.md`). Jekyll 템플릿은 `_includes/`와 `_layouts/`에 있으며 [Liquid](https://github.com/Shopify/liquid/wiki) 문법을 씁니다. 코드 하이라이팅은 Jekyll 기본 [Rouge](http://rouge.jneen.net/)를 쓰고, 테마는 `less/highlight.less`를 교체해 바꿀 수 있습니다.

---

### velog 자동 동기화

`.github/workflows/velog-sync.yml`이 **매월 1일 18:00 KST**에 velog 새 글을 크롤링해 `_posts/`에 커밋합니다. 수동 실행은:

```sh
gh workflow run velog-sync.yml
```

> ⚠️ GitHub은 **60일간 저장소 활동이 없으면 스케줄 워크플로를 자동 비활성화**합니다.
> 동기화가 멈췄다면 `gh workflow enable velog-sync.yml`로 다시 켜세요.

크롤러는 `_scripts/`에 있고 [uv](https://docs.astral.sh/uv/)로 의존성을 관리합니다. 처리 이력은 `processed_posts.csv`에 기록됩니다.

---

License
-------

Apache License 2.0 — 전문은 [LICENSE](LICENSE) 참고.
Copyright (c) 2024-present Euisuk Chung

이 사이트는 [Hux Blog](https://github.com/Huxpro/huxpro.github.io) (Apache 2.0, Copyright Hux)를 기반으로 하며, 해당 테마는 다시 [Clean Blog](https://startbootstrap.com) (Start Bootstrap)에서 파생되었습니다. 번들된 서드파티 소프트웨어의 전체 목록과 저작권 고지는 [NOTICE](NOTICE)를 참고하세요.
