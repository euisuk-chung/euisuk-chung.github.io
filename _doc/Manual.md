서쿠 개발노트 운영 매뉴얼
========================

이 사이트에서 실제로 켜져 있는 기능과 설정만 정리한 문서입니다.
설정은 모두 `_config.yml`에 있습니다.

- [디렉터리 구조](#디렉터리-구조)
- [포스트](#포스트)
- [velog 자동 동기화](#velog-자동-동기화)
- [OKF 콘텐츠 규칙](#okf-콘텐츠-규칙)
- [사이드바](#사이드바)
- [Featured Tags](#featured-tags)
- [태그 페이지 (`okf/_concepts/`)](#태그-페이지-okf_concepts)
- [Friends](#friends)
- [검색](#검색)
- [Keynote 레이아웃](#keynote-레이아웃)
- [광고](#광고)
- [Analytics](#analytics)
- [SEO](#seo)
- [PWA / 서비스워커](#pwa--서비스워커)
- [폰트](#폰트)
- [에셋 빌드](#에셋-빌드)

---

## 디렉터리 구조

| 경로 | 설명 |
|---|---|
| `okf/` | OKF 번들 루트. `index.md`, `log.md`는 예약 파일(사이트 빌드에서 제외) |
| `okf/_posts/<연도>/` | 포스트 마크다운. velog 동기화가 연도별로 넣습니다 (`_config.yml`의 `collections_dir: okf`) |
| `okf/_concepts/<slug>.md` | 태그 사전. 파일 하나가 `/tags/<slug>/` 페이지 하나 |
| `_layouts/` | `default` · `page` · `post` · `keynote` · `tag` 5종 |
| `_includes/` | Liquid 파셜 (헤더, 푸터, 사이드바, 광고 등) |
| `less/` | 스타일 **원본** |
| `css/`, `js/blog*.js` | 빌드 **산출물** — 직접 수정 금지 |
| `_scripts/` | velog 크롤러 + OKF 도구 (Python, uv) |
| `_doc/` | 이 문서 |

---

## 포스트

`okf/_posts/<연도>/`에 마크다운을 넣으면 됩니다. YAML front-matter로 메타데이터를 지정합니다.

velog에서 동기화된 글은 최소 형태를 씁니다:

```yml
---
title: "[CES] CES 2026 젠슨 황 기조연설 정리"
date: "2026-01-08"
year: "2026"
---
```

직접 쓰는 글에는 아래 옵션을 쓸 수 있습니다:

```yml
---
layout:     post
title:      "제목"
subtitle:   "부제"
date:       2026-01-08 12:00:00
author:     "Euisuk Chung"
header-img: "img/home-bg.jpg"
catalog:    true          # 우측 목차 사이드바
tags:       [AI, MLOps]
---
```

추가 옵션:

| 키 | 효과 |
|---|---|
| `header-style: text` | 헤더 이미지 없이 텍스트만 |
| `header-mask: 0.3` | 헤더 이미지 위에 어두운 마스크 |
| `mathjax: true` | LaTeX 수식 렌더링 |

`rake`로 초안을 생성할 수도 있습니다:

```sh
rake post title="제목" subtitle="부제"
```

> 생성된 파일은 `okf/_posts/` 루트에 떨어지므로 해당 연도 폴더로 옮기세요.

---

## velog 자동 동기화

`.github/workflows/velog-sync.yml`이 **매월 1일 18:00 KST**에 실행되어
[velog](https://velog.io/@euisuk-chung) 새 글을 `okf/_posts/`로 가져옵니다.

```sh
gh workflow run velog-sync.yml        # 수동 실행
gh run list --workflow=velog-sync.yml # 실행 이력
```

> ⚠️ **중요:** GitHub은 60일간 저장소 활동(푸시)이 없으면 스케줄 워크플로를
> 자동으로 비활성화합니다. 상태가 `disabled_inactivity`가 되면 조용히 멈추므로,
> 동기화가 끊긴 것 같으면 아래로 확인하고 다시 켜세요.
>
> ```sh
> gh api repos/euisuk-chung/euisuk-chung.github.io/actions/workflows \
>   --jq '.workflows[] | "\(.name) \(.state)"'
> gh workflow enable velog-sync.yml
> ```

크롤러는 저장 시 두 가지를 자동 처리합니다:

- **제목의 따옴표 이스케이프** — `제목에 "인용"이 든 글`을 그대로 쓰면
  front-matter YAML이 깨져 해당 포스트만 레이아웃 없이 렌더됩니다.
- **코드블록의 Liquid 구문 보호** — `{{PLACEHOLDER}}`가 든 코드블록을
  `{% raw %}`로 감쌉니다. 감싸지 않으면 Jekyll이 템플릿 변수로 해석해
  **조용히 빈 문자열로 지워버립니다.**

크롤링 이력은 `processed_posts.csv`에 URL 단위로 기록되며, 이미 처리된 글은
건너뜁니다. 크롤러 단계는 `continue-on-error: true`라 실패해도 워크플로는
초록불이 뜹니다 — 새 글이 안 들어오면 실행 로그와 `crawl-logs-*` 아티팩트를
직접 확인하세요.

---

## OKF 콘텐츠 규칙

포스트와 태그 사전은 Google Cloud의 [Open Knowledge Format(OKF) v0.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)를 따릅니다.
OKF는 "YAML front matter를 가진 마크다운 파일의 디렉터리"입니다. 필수 키는 `type` 하나이고,
파일끼리는 일반 마크다운 링크로 연결합니다. 번들 루트는 `okf/`이며 `index.md`, `log.md`는 예약 파일입니다.

### 포스트 front matter

```yml
---
type: "Paper Review"        # _scripts/okf_types.json 의 allowed 중 하나. 제목 [접두어]로 자동 유도
title: "[Paper Review] Visualizing Data using t-SNE"
description: "한 문장 요약"  # 40–150자 권장, 한 줄
date: "2021-09-08"
tags:                       # concept 파일의 title 과 정확히 일치
  - "차원축소"
resource: "https://velog.io/@euisuk-chung/..."   # 원문 URL
generated:
  by: "process:velog-sync"  # 크롤러 산출물. 직접 쓴 글은 human:euisuk-chung
  at: "2024-12-21T17:33:17Z"
sources:
  - id: "velog"
    resource: "https://velog.io/@euisuk-chung/..."
    title: "..."
    author: "human:euisuk-chung"
    last_modified: "2021-09-08"
status: "stable"            # draft | stable | deprecated. description 과 정규 태그를 갖추면 stable
year: "2021"
---
```

본문 규칙: ATX 헤딩(`##`)만 사용, 본문 첫 줄에 제목 H1을 반복하지 않음, 헤딩 바로 위에 `---` 규칙을 두지 않음
(테마가 h2 위에 구분선을 그리므로 두 줄로 보입니다). 크롤러가 이 규칙대로 저장합니다.

### 태그 사전(concept)

태그 하나가 `okf/_concepts/<slug>.md` 파일 하나입니다. 규칙은 [태그 페이지](#태그-페이지-_concepts) 절 참고.
`aliases`에 옛 표기를 적어 두면 `okf_migrate.py`와 크롤러가 정규 `title`로 바꿔 줍니다.
`parent`/`related`에는 다른 concept의 slug를 적습니다(온톨로지 확장용).

### 도구 (`_scripts/`)

```bash
uv run --project _scripts python _scripts/okf_lint.py --allow-draft --check-index   # 규칙 검사
uv run --project _scripts python _scripts/okf_migrate.py --paths okf/_posts/2026 --dry-run --diff   # 변환 미리보기
uv run --project _scripts python _scripts/okf_migrate.py --paths okf/_posts/2026 --enrich enrich.json --report report.json
uv run --project _scripts python _scripts/okf_migrate.py --check      # 변환된 글이 멱등인지
uv run --project _scripts python _scripts/okf_index.py --write         # index.md 갱신
uv run --project _scripts python _scripts/okf_roundtrip.py _site-before _site-after --report report.json
uv run --project _scripts python -m pytest _scripts/tests -q
```

- `okf_migrate.py`는 BOM 제거, 중복 H1 제거, setext→ATX, 헤딩 앞 `---` 제거만 하고 나머지 본문은 바이트 단위로 보존합니다.
  `verify_no_loss`가 그 외 변경을 감지하면 파일을 쓰지 않습니다.
- `description`/`tags`/`type` 보강은 `enrich.json` 사이드카(`{"<포스트 경로>": {"description", "tags", "type", "new_tags"}}`)로 주입합니다.
  `new_tags`에 적은 태그는 concept 파일로 생성됩니다.
- 크롤러 본문 정규화 규칙이 바뀌면 `blog_crawler.py --rehash`로 `processed_posts.csv`의 해시를 먼저 갱신하세요.
  안 하면 `--check-updates`가 모든 글을 다시 씁니다.
- CI: `.github/workflows/okf-lint.yml`이 PR/master에서 테스트·린트·멱등 검사를 돌립니다.

### 콘텐츠 PR

마이그레이션은 연도별(또는 50개 내외) 배치 PR(`codex/okf-migrate-<batch>`)로 나눠 사람이 리뷰합니다.
PR 본문에는 포스트별 description/tags/type 표, `--report` 카운트, 접힌 검증 섹션을 넣습니다. 규칙 원문은 `AGENTS.md`.

---

## 사이드바

```yml
sidebar: true
sidebar-about-description: "서쿠 개발노트⭐ <br> Data Scientist"
sidebar-avatar: https://github.com/euisuk-chung.png   # 절대 URL
```

화면이 좁아지면(`<= 992px`) 사이드바는 본문 아래로 내려갑니다.
아바타와 설명, SNS 버튼은 `_includes/short-about.html`이 담당합니다.

SNS 링크는 아래 값으로 자동 생성됩니다:

```yml
instagram_username: chung_es
github_username:    euisuk-chung
youtube_username:   loading_700
linkedin_username:  euisuk-chung
```

---

## Featured Tags

```yml
featured-tags: true
featured-condition-size: 1   # 이 값보다 많은 글을 가진 태그만 노출
```

내부적으로 `{% if tag[1].size > site.featured-condition-size %}` 조건을 씁니다.
태그가 많아져 목록이 길어지면 이 값을 올리세요.

---

## 태그 페이지 (`okf/_concepts/`)

태그는 세 곳에 노출됩니다: 포스트 상단 히어로(흰 pill), 포스트 본문 하단(`.post-tags-footer`),
홈/아카이브/태그 페이지의 글 카드. 링크 대상은 `_includes/tag-url.html`이 한 곳에서 정합니다.

- `okf/_concepts/<slug>.md` 파일이 있는 태그 → `/tags/<slug>/` 전용 페이지(설명 + 해당 글 목록)
- 없는 태그 → `/archive/?tag=<태그>` 클라이언트 필터로 폴백

concept 파일 규칙:

```yml
---
type: Tag
title: OpenAI          # 포스트 front-matter의 tags 문자열과 정확히 일치해야 함 (대소문자 포함)
slug: openai           # 파일명과 동일, ASCII 소문자-하이픈. 한글 태그도 영문 slug 사용
description: "한 문장 설명"   # 히어로 부제와 <meta description>에 쓰임
aliases: []            # 옛 표기 목록 (OKF 도구가 정규화에 사용)
status: stable
---
본문은 태그 설명으로 목록 위에 렌더됩니다.
```

컬렉션 이름이 `tags`가 아니라 `concepts`인 이유: Jekyll이 `site.tags`를 포스트 태그 집계용으로 예약하고 있어
같은 이름의 컬렉션은 템플릿에서 읽을 수 없습니다. 레이아웃은 `_layouts/tag.html`, 글 목록 카드는
`_includes/post-card.html`을 공유합니다. `_config.yml`을 바꾼 뒤에는 `jekyll serve`를 재시작해야 합니다.

---

## Friends

`_config.yml`에 배열로 정의합니다. 상호 링크는 SEO에 도움이 됩니다.

```yml
friends:
  [
    { title: "My Velog", href: "https://velog.io/@euisuk-chung" },
    { title: "My YouTube", href: "https://www.youtube.com/@loading_700" },
  ]
```

---

## 검색

[Simple-Jekyll-Search](https://github.com/christian-fei/Simple-Jekyll-Search)
기반이며, 루트의 `search.json`이 색인입니다. Jekyll 빌드 시 자동 생성되므로
따로 관리할 필요는 없습니다. UI는 `_includes/search.html`에 있습니다.

---

## Keynote 레이아웃

Reveal.js·Slides 등 HTML 기반 발표 자료를 임베드하는 전용 레이아웃입니다.

```yml
---
layout: keynote
iframe: "https://example.com/my-slides/"
---
```

iframe은 화면 크기와 방향에 맞춰 자동으로 리사이즈됩니다.

---

## 광고

- **Google AdSense** — `_includes/adsense.html`, `_includes/head.html`
  (`ca-pub-5020393432718583`), 루트 `ads.txt`에도 동일 ID가 기재돼 있어야 합니다.
- **Kakao AdFit** — `_includes/ads.html` (`DAN-vJwtOu7THEmP3LXP`)

---

## Analytics

현재 **비활성** 상태입니다. 쓰려면 `_config.yml`에서 주석을 해제하세요.

```yml
# ga_track_id: "G-XXXXXXXXXX"   # GA4 measurement ID
# ga_domain: euisuk-chung.github.io
```

---

## SEO

```yml
title: Euisuk's Dev Log
SEOTitle: Chung Euisuk | Data Scientist   # 검색 결과에 노출될 제목
author: "Euisuk Chung"
twitter:
  username: euisuk_chung
```

`title`은 사이트 헤더에, `SEOTitle`은 `<title>` 태그에 쓰입니다. 둘을 다르게
두어 검색 노출용 제목을 따로 관리할 수 있습니다.

Google Search Console 소유 확인 파일은 `google35d12b88d96acbcd.html`이며,
`_config.yml`의 `include:` 목록에 들어가 있어야 배포됩니다 (`ads.txt`,
`robots.txt`도 동일).

---

## PWA / 서비스워커

```yml
service-worker: true
chrome-tab-theme-color: "#000000"
```

- `sw.js` — 프리캐시 + stale-while-revalidate 전략
- `pwa/manifest.json` — 설치 시 앱 이름·아이콘
- `pwa/icons/` — 128px, 512px 아이콘
- `offline.html` — 오프라인 폴백 페이지

> ⚠️ `sw.js`의 `PRECACHE_LIST`에 **존재하지 않는 파일이 하나라도 있으면
> `cache.addAll()`이 통째로 실패해 프리캐시가 전혀 동작하지 않습니다.**
> 에러는 `.catch()`로 삼켜져 콘솔에만 찍히므로 조용히 깨집니다.
> 파일을 지우거나 이름을 바꿀 때는 이 목록을 반드시 함께 갱신하세요.

---

## 폰트

본문 폰트는 **Pretendard**(SIL OFL 1.1)를 씁니다. jsDelivr의 **variable dynamic
subset**을 `_includes/head.html`에서 로드하므로, 실제 쓰이는 글자 범위만
내려받아 한글 웹폰트치고 가볍습니다. 폰트 파일을 저장소에 두지는 않습니다.

스택은 `less/mixins.less`의 `.sans-serif()`에 정의돼 있습니다:

```
"Pretendard Variable", Pretendard, -apple-system, BlinkMacSystemFont,
system-ui, "Helvetica Neue", "Segoe UI", "Apple SD Gothic Neo",
"Noto Sans KR", "Malgun Gothic", "PingFang SC", "Microsoft YaHei", sans-serif
```

한글(Apple SD Gothic Neo / Malgun Gothic / Noto Sans KR)이 중국어 폰트보다
앞에 옵니다. 중국어 폰트는 `_includes/about/zh.md` 때문에 뒤쪽에 남겨둔
폴백입니다. 순서를 바꾸면 Windows에서 한글 자소 모양이 틀어지니 주의하세요.

코드 블록은 `Fira Code, Menlo, Monaco, Consolas, "Courier New", monospace`를
쓰며 웹폰트를 로드하지 않습니다 (설치돼 있으면 Fira Code가 적용됩니다).

---

## 에셋 빌드

`less/`와 `js/blog.js`가 원본, `css/`와 `js/blog.min.js`가 산출물입니다.

```sh
npm install
npm run build     # 1회 빌드
npm run watch     # 변경 감지 재빌드
npm run dev       # watch + jekyll serve
```

빌드 스크립트는 `build.mjs` 하나이고 [less](https://lesscss.org/)와
[esbuild](https://esbuild.github.io/)만 씁니다. 산출물 상단에는 Apache 2.0
준수를 위한 저작권·수정 고지 배너가 자동으로 붙습니다 ([NOTICE](../NOTICE) 참고).

> `less/mixins.less`의 폰트 스택에는 `//` 인라인 주석을 쓰지 마세요.
> less v4 파서가 값 중간의 `//`를 거부해 빌드가 깨집니다.
