---
type: "Repo Review"
title: "[Repo Review] GitMCP — 저장소 문서를 AI 도구로 제공하는 서버의 실제 흐름"
description: "GitMCP의 URL 해석부터 문서 확보·AutoRAG 검색·캐시·응답까지 추적하고, README의 최신성·개인정보 표현과 구현의 차이를 구분합니다."
date: "2026-10-28"
tags:
  - "Repo Review"
  - "MCP"
  - "AI Agent"
  - "Tools"
resource: "https://github.com/idosal/git-mcp/tree/c487a29895dcfcb5b672247e646426a56e2051c1"
generated:
  by: "process:blog-review"
  at: "2026-10-28T06:08:54+09:00"
sources:
  - id: "github:idosal/git-mcp"
    title: "GitMCP"
    resource: "https://github.com/idosal/git-mcp/tree/c487a29895dcfcb5b672247e646426a56e2051c1"
    revision: "c487a29895dcfcb5b672247e646426a56e2051c1"
    last_modified: "2026-05-08T17:21:22+03:00"
status: "stable"
year: "2026"
analyzed_at: "2026-10-28T06:08:54+09:00"
source_id: "idosal/git-mcp"
source_revision: "c487a29895dcfcb5b672247e646426a56e2051c1"
source_type: "repo"
source_url: "https://github.com/idosal/git-mcp/tree/c487a29895dcfcb5b672247e646426a56e2051c1"
visual_sources:
  - path: "/img/reviews/2026/git-mcp-review/architecture.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/index.ts#L58-L159"
    caption: "리뷰어 작성, 분석 커밋 기준. Worker의 웹/MCP 분기와 도구의 외부 자원 책임."
  - path: "/img/reviews/2026/git-mcp-review/documentation-flow.svg"
    kind: "reviewer-diagram"
    source_url: "https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/tools/commonTools.ts#L35-L297"
    caption: "리뷰어 작성, 분석 커밋 기준. 기본 GitHub 저장소의 문서 확보 순서와 결과 캐시."
---

## 오래된 사용법을 아는 모델에 현재 문서를 연결합니다

라이브러리의 함수 이름을 모델이 기억하더라도, 지금 쓰는 버전의 매개변수까지 정확히 아는 것은 아닙니다. 새 프로젝트나 자주 바뀌는 API에서는 학습 당시의 지식과 현재 문서 사이에 간격이 생깁니다. 사용자가 문서를 찾아 대화에 붙여 넣을 수도 있지만, 질문할 때마다 필요한 문서를 고르고 전달하는 작업이 반복됩니다.

**GitMCP는 공개 GitHub 저장소와 GitHub Pages의 문서를 AI 클라이언트가 도구로 가져오고 검색하도록 제공하는 원격 MCP 서버입니다.** MCP(Model Context Protocol)는 AI 애플리케이션과 외부 도구가 요청·응답을 주고받는 규약입니다. GitMCP가 문서 내용을 반환하면, 연결한 클라이언트의 모델이 그 자료를 바탕으로 답변합니다. 문서를 제공하는 서버와 최종 답변을 작성하는 모델은 역할이 다릅니다. README는 환각 감소를 제품의 목표로 설명하지만, 이 레포를 읽는 것만으로 모든 답변의 정확성이 보장되지는 않습니다. [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/README.md#L30-L57)

이 글은 `idosal/git-mcp`의 커밋 `c487a29895dcfcb5b672247e646426a56e2051c1`을 고정해 문서와 코드를 정적으로 분석했습니다. 대상 레포의 의존성 설치·빌드·테스트·서비스 호출은 수행하지 않았습니다. 아래의 연결 설정은 해당 커밋의 문서에 있는 예시이며 실제 연결 성공을 검증한 기록이 아닙니다.

## URL로 대상 범위를 정하고 도구로 필요한 내용을 가져옵니다

README에는 세 가지 진입 URL이 있습니다. 일반 GitHub 저장소는 `gitmcp.io/{owner}/{repo}`, GitHub Pages는 `{owner}.gitmcp.io/{repo}`, 매번 다른 저장소를 선택하려면 `gitmcp.io/docs`를 사용합니다. 앞의 두 방식은 서버 URL에 대상을 넣고, 범용 방식은 도구 인자에 `owner`와 `repo`를 넣습니다. [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/README.md#L65-L75)

| 하고 싶은 일 | 일반 저장소용 도구 | 반환하는 정보 |
|---|---|---|
| 프로젝트 전체를 먼저 파악하기 | `fetch_<repo>_documentation` | 선택된 문서의 이름 `fileUsed`와 텍스트 |
| 특정 기능의 근거 찾기 | `search_<repo>_documentation` | 검색 질의와 문서 조각 또는 전체 문서 대체 응답 |
| 구현 위치 찾기 | `search_<repo>_code` | GitHub 검색 결과의 파일 경로·링크·점수·페이지 정보 |
| 문서에 언급된 URL 읽기 | `fetch_generic_url_content` | URL, 상태, 텍스트 또는 HTML을 변환한 Markdown |

이 표의 URL 읽기 도구 이름은 README의 `fetch_url_content`가 아니라 **현재 등록 코드의 `fetch_generic_url_content`**를 기준으로 적었습니다. 검색 응답 안의 안내 문장에는 옛 이름도 남아 있습니다. 실제 클라이언트에서는 서버가 내놓는 도구 목록을 기준으로 보아야 합니다. 저장소 이름에 기호가 있거나 이름이 길면 도구 이름도 정규화·단축될 수 있습니다. [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/tools/index.ts#L8-L34) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/tools/repoHandlers/DefaultRepoHandler.ts#L20-L92) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/tools/commonTools.ts#L798-L848)

범용 `/docs` 서버는 `fetch_generic_documentation`, `search_generic_documentation`, `search_generic_code`를 제공합니다. 라이브러리 이름만 알고 저장소를 모를 때는 정적 목록을 조회하는 `match_common_libs_owner_repo_mapping`도 있습니다. 이는 실시간으로 인터넷 전체에서 정체성을 찾아 주는 검색기가 아니라, 코드에 포함된 매핑에서 이름을 대소문자와 무관하게 찾는 도구입니다. 특정 저장소 URL을 사용하면 대상 선택 실수를 줄일 수 있지만, 공통 URL 읽기 도구까지 같은 저장소로 제한하는 완전한 보안 경계라는 뜻은 아닙니다. [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/tools/repoHandlers/GenericRepoHandler.ts#L16-L159) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/tools/repoHandlers/GenericRepoHandler.ts#L215-L231) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/tools/index.ts#L18-L28)

## 아키텍처: 웹 화면과 MCP 응답을 같은 Worker에서 나눕니다

![AI 클라이언트의 요청이 Cloudflare Worker에서 웹 화면 또는 MCP로 나뉘고, MCP 도구가 GitHub·R2·AutoRAG와 캐시를 이용해 텍스트를 돌려주는 구조]({{ '/img/reviews/2026/git-mcp-review/architecture.svg' | relative_url }})

*리뷰어 작성, 분석 커밋 기준. 실선은 문서 도구의 주요 요청 흐름입니다. 일반 웹 화면과 내장 채팅은 별도 분기로 구분했습니다.* [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/index.ts#L58-L99) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/index.ts#L144-L158) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/tools/commonTools.ts#L120-L204) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/tools/commonTools.ts#L341-L390)

실행 진입점은 `src/index.ts`입니다. Cloudflare Worker의 `fetch`가 HTTP 요청을 받고, `MyMCP`는 `McpAgent`를 상속해 MCP 서버와 도구를 등록합니다. 같은 URL을 사람이 브라우저로 열면 React Router가 연결 안내 페이지 등을 만듭니다. 따라서 “브라우저에서 페이지가 열린다”와 “MCP 클라이언트가 도구 호출용 전송 경로로 접속한다”는 서로 다른 동작입니다. [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/index.ts#L27-L30) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/index.ts#L58-L99) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/index.ts#L103-L159)

| 파일·디렉터리 | 실제 책임 |
|---|---|
| `src/index.ts` | HTTP 분기, MCP 서버 초기화, 일반 웹 요청 전달 |
| `src/shared/repoData.ts` | 호스트·경로에서 GitHub 또는 Pages의 대상 식별 |
| `src/api/tools/repoHandlers/` | 기본·범용·일부 프로젝트 전용 도구 구성 |
| `src/api/tools/commonTools.ts` | 문서 확보, 문서 검색, 코드 검색, URL 내용 반환 |
| `src/api/utils/githubClient.ts`, `github.ts` | 기본 브랜치 조회, GitHub 검색·raw 파일 요청, 제한 처리 |
| `src/api/utils/cache.ts`, `r2.ts`, `robotsTxt.ts` | 캐시·객체 저장소 조회·웹 접근 규칙 확인 |
| `app/routes/`, `app/chat/` | 안내 페이지와 별도의 내장 채팅 인터페이스 |
| `wrangler.jsonc` | Worker와 Durable Object·KV·R2·AI·Queue 등의 바인딩 |

설정에는 KV라는 키–값 저장소, R2 객체 저장소, AI 서비스, 큐, Vectorize 인덱스가 선언되어 있습니다. 그러나 **자원이 선언되어 있다는 사실과 현재 요청이 실제로 그 자원을 사용한다는 사실은 구분해야 합니다.** 예를 들어 현재 공통 문서 검색은 AutoRAG 호출과 대체 응답으로 연결됩니다. `vectorStore.ts`의 존재나 오래된 주석만 보고 모든 검색이 그 모듈에서 직접 임베딩을 만들고 인덱싱한다고 설명하면 실제 연결을 놓칩니다. [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/wrangler.jsonc#L37-L75) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/tools/commonTools.ts#L341-L447) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/tools/commonTools.ts#L512-L562)

## 작동 원리: 요청이 자료로 바뀌는 여덟 단계

### 1. 전송 경로와 저장소 정체성을 결정합니다

Worker는 `Accept` 헤더에 `text/event-stream`이 포함되고 경로가 루트가 아니면 `MyMCP.serve("/*")`로 보냅니다. 그 외에는 React Router 요청 처리기로 전달합니다. 이 커밋에서는 SSE(Server-Sent Events, 서버가 HTTP 연결을 통해 이벤트를 보내는 방식) 수락 헤더가 분기 조건입니다. 따라서 README의 URL 하나가 모든 HTTP 호출에서 같은 결과를 준다고 이해하면 안 됩니다. OAuth 검색에 쓰이는 `/.well-known/oauth-protected-resource`와 `/.well-known/oauth-authorization-server` 계열에는 404를 반환해 인증을 요구하지 않는 모드로 진행하게 합니다. 의존성 목록에 OAuth 패키지가 있어도 이 경로가 OAuth 로그인을 요구한다는 뜻은 아닙니다. [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/index.ts#L122-L158)

`MyMCP.init()`은 요청 URL을 정리한 뒤 `getMcpTools()`를 호출합니다. 저장소 주소가 `gitmcp.io/owner/repo`이면 경로의 앞 두 부분을 쓰고, `owner.gitmcp.io/repo`이면 서브도메인을 소유자로 해석합니다. 도구는 이 `RepoData`를 닫아 가진 콜백으로 등록됩니다. 특정 저장소 서버의 문서 도구가 매 호출마다 저장소 인자를 다시 요구하지 않는 이유입니다. [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/index.ts#L64-L99) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/shared/repoData.ts#L40-L97) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/tools/repoHandlers/DefaultRepoHandler.ts#L30-L57)

### 2. 기본·범용·프로젝트 전용 핸들러를 고릅니다

`getHandlerByRepoData()`는 주소 종류와 `owner/repo`로 핸들러를 찾고, 맞는 것이 없으면 기본 핸들러를 씁니다. `/docs`는 범용, `mrdoob/three.js`와 `remix-run/react-router`는 별도 핸들러가 등록되어 있습니다. 기본 도구 세 개에 공통 URL 읽기 도구를 더하는 구성이 모든 프로젝트에 그대로 적용되는 것은 아닙니다. Three.js에는 문서 목록→선택 문서 내용 읽기 같은 전용 흐름이 있습니다. 이 글의 다음 설명은 **기본 저장소 핸들러의 공통 처리**를 중심으로 합니다. [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/tools/repoHandlers/handlers.ts#L8-L34) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/tools/repoHandlers/ThreejsRepoHandler.ts#L12-L108)

여기서 범용 서버의 “동적 선택”은 요청 인자에 저장소를 넣는다는 뜻입니다. 범용 도구의 콜백은 `owner`, `repo`, `urlType: "github"`, `host: "gitmcp.io"`를 만들어 공통 함수를 직접 부릅니다. 반대로 Three.js의 전용 핸들러는 처음부터 해당 저장소 URL로 연결할 때 선택됩니다. 연결 방식에 따라 노출되는 도구의 구성이 달라질 수 있습니다. [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/tools/repoHandlers/GenericRepoHandler.ts#L75-L153)

### 3. 문서 가져오기는 캐시를 먼저 보고, 정해진 순서로 출처를 찾습니다

![기본 GitHub 저장소의 문서 가져오기가 30분 결과 캐시, llms.txt 정적 경로, GitHub 파일 검색, R2 생성 문서, 루트 README 순서로 진행하는 흐름]({{ '/img/reviews/2026/git-mcp-review/documentation-flow.svg' | relative_url }})

*리뷰어 작성, 분석 커밋 기준. 각 단계에서 문서를 얻으면 뒤의 출처 탐색을 생략합니다. 그림은 일반 GitHub 저장소 경로이며 GitHub Pages의 흐름은 다릅니다.* [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/tools/commonTools.ts#L35-L47) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/tools/commonTools.ts#L120-L245)

첫 단계는 `owner/repo`에 대응하는 가져오기 결과 캐시입니다. 결과가 있으면 즉시 반환합니다. 없으면 GitHub API로 기본 브랜치를 조회합니다. 실제 기본 브랜치를 얻지 못하면 `main`, `master`의 README 존재를 확인하며, 예외 처리의 최종 대체값은 `main`입니다. 이 결정은 **조회 시점의 기본 브랜치 이름**이며, 매번 특정 커밋 SHA를 고정하는 설계는 아닙니다. 이 리뷰가 분석 커밋을 고정하는 것과 서비스가 사용자의 대상 문서를 가져오는 버전 선택은 다른 문제입니다. [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/tools/commonTools.ts#L35-L47) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/utils/github.ts#L110-L170)

같은 브랜치에서 먼저 시도하는 경로는 아래 코드와 같습니다.

```typescript
    const possibleLocations = [
      "docs/docs/llms.txt", // Current default
      "llms.txt", // Root directory
      "docs/llms.txt", // Common docs folder
    ];
```

*원문 코드 그대로 인용.* [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/tools/commonTools.ts#L125-L129)

세 요청은 병렬로 보내지만, 결과를 고를 때는 배열 순서를 따릅니다. 따라서 “먼저 다운로드가 끝난 파일”을 쓰는 것이 아니라 **`docs/docs/llms.txt` → 루트 `llms.txt` → `docs/llms.txt` 순으로 존재하는 문서**를 선택합니다. 이 파일은 AI가 읽기 좋은 안내 문서를 제공하기 위한 관례입니다. 해당 이름이 있다는 사실만으로 문서가 정확하거나 최신이라는 검증까지 수행하지는 않습니다. [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/tools/commonTools.ts#L131-L171)

정적 경로에서 못 찾으면 GitHub 코드 검색으로 `llms.txt`를 찾습니다. 거기에도 없으면 R2의 `owner/repo/llms.txt`를 읽고 `llms.txt (generated)`라고 표시합니다. 마지막으로 GitHub 검색을 통해 루트의 `README.*`를 찾습니다. README가 설명하는 “AI에 최적화된 문서”는 이 구현에서 R2에 이미 준비된 생성 문서가 대표적인 대체 출처입니다. **요청을 받은 Worker가 즉석에서 새 문서를 생성하는 코드는 이 경로에 없습니다.** [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/tools/commonTools.ts#L173-L245) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/utils/r2.ts#L1-L22)

파일 검색은 먼저 저장된 파일 경로를 재사용하고, 없으면 검색 결과의 첫 파일을 읽습니다. 경로 캐시 키에는 저장소만 들어가고 파일명은 들어가지 않습니다. 따라서 같은 저장소에서 서로 다른 종류의 파일을 찾는 호출도 경로 캐시를 공유합니다. 이 글에서는 코드에 드러난 캐시 단위를 설명하며, 실제로 어떤 저장소에서 오탐색이 발생하는지 실행해 확인하지는 않았습니다. [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/utils/github.ts#L43-L77) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/utils/cache.ts#L27-L29) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/utils/cache.ts#L118-L155)

### 4. GitHub Pages는 웹 접근 규칙을 확인한 뒤 HTML을 변환합니다

Pages 방식은 주소를 `https://owner.github.io/repo/`로 바꿉니다. 여기서는 `llms.txt`를 먼저 찾고, 없으면 사이트 첫 페이지를 읽어 HTML을 Markdown으로 변환하며, 이어 README를 시도합니다. 일반 저장소의 GitHub 검색·R2 대체 경로와 같은 흐름으로 합치면 안 됩니다. [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/tools/commonTools.ts#L56-L119)

이 경로와 공통 URL 읽기 도구는 `robots.txt`를 확인합니다. 구현은 `User-agent`의 규칙과 URL 경로 접두사를 비교하며, `Allow`를 먼저 보고 `Disallow`를 검사합니다. 규칙 파일을 가져오지 못하거나 처리 중 예외가 나면 허용하는 방식입니다. 따라서 “웹 접근 규칙을 고려한다”는 사실은 확인되지만, 모든 robots 규칙의 완전한 호환성이나 운영 환경의 접근 통제를 검증했다는 주장은 하지 않습니다. 차단된 경우에는 도구 응답에 그 사실을 텍스트로 돌려줍니다. [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/utils/robotsTxt.ts#L75-L164) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/tools/commonTools.ts#L717-L745)

### 5. 확보한 문서는 응답과 후속 처리로 나뉩니다

문서를 찾으면 `{ fileUsed, content: [{ type: "text", text: ... }] }` 형식으로 반환하고, 결과 캐시 저장은 `ctx.waitUntil()`로 요청 응답 이후에도 이어질 수 있게 합니다. 찾지 못한 경우에는 `No documentation found.`라는 텍스트를 반환합니다. 결과를 받은 AI 클라이언트가 이 상태를 해석해야 하며, “문서 도구가 응답했다”는 사실 자체가 근거 확보 성공을 뜻하지는 않습니다. [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/tools/commonTools.ts#L252-L297)

동시에 큐에는 저장소·문서 URL·문서 종류·길이·브랜치 등의 메타데이터를 보냅니다. 코드에는 문서 처리의 **생산자**가 보이지만, 이 레포의 Worker 진입점에서 그 메시지를 받아 R2 자료와 검색 인덱스를 갱신하는 전체 소비자 흐름은 확인할 수 없습니다. 문서를 돌려주는 HTTP 경로와 사전에 만들어 놓는 검색 자료의 갱신 경로를 나누어 보아야 합니다. [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/tools/commonTools.ts#L300-L338) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/wrangler.jsonc#L68-L75)

### 6. 문서 검색은 AutoRAG가 있으면 검색하고, 없으면 전체 문서로 대체합니다

공통 문서 검색은 먼저 R2에 `owner/repo/llms.txt`가 있는지 `head()`로 확인합니다. 있으면 `env.AI.autorag("docs-rag").search()`를 시도합니다. 질의 재작성, 최대 결과 12개, 점수 문턱 0.4, 저장소 폴더 범위 필터를 요청에 넣습니다. 반환 뒤에도 파일명이 해당 `owner/repo/`로 시작하는지 한 번 더 확인하고, 문서 조각·점수·원문 URL을 텍스트로 구성합니다. [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/tools/commonTools.ts#L341-L390) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/tools/commonTools.ts#L417-L505)

중요한 대체 경로는 이름이 `searchRepositoryDocumentationNaive`이지만 **해당 함수 안에서 단순 키워드 검색을 수행하는 것은 아니라는 점**입니다. 문서를 가져와 “검색과 일치하지 않았거나 인덱싱 중일 수 있다”는 안내와 함께 전체 문서를 반환합니다. AutoRAG 결과가 없거나 호출이 실패했을 때 이 대체 응답으로 넘어갑니다. 단, `DOCS_BUCKET` 자체가 없는 환경은 함수 첫머리에서 예외를 내므로 같은 대체 경로까지 진행하지 않습니다. [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/tools/commonTools.ts#L357-L390) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/tools/commonTools.ts#L512-L575)

이 구조는 두 종류의 비용을 분리합니다. 검색에 성공하면 필요한 문서 조각을 받을 수 있지만, 대체 응답은 전체 문서를 모델에게 전달하므로 입력량이 커질 수 있습니다. 이는 코드 흐름을 읽은 리뷰어의 해석이며, 이 글에서 토큰 절감량이나 검색 품질을 측정한 것은 아닙니다. Three.js 전용 검색의 대체 동작은 전체 문서 반환 대신 문서 목록·세부 문서 도구를 먼저 쓰라는 안내입니다. [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/tools/repoHandlers/ThreejsRepoHandler.ts#L162-L185)

### 7. 코드 검색은 GitHub 검색 결과의 위치 정보를 제공합니다

코드 검색은 질의에 `repo:owner/repo`를 붙여 GitHub Search API에 보냅니다. 공통 도구는 페이지당 30개 결과를 요청하며, 페이지를 최소 1로 정규화합니다. 응답에는 일치한 파일의 이름·경로·GitHub URL·Git URL·점수와 다음 페이지 유무가 들어갑니다. **이 경로가 일치한 함수의 실제 코드 본문까지 자동으로 읽어 주는 것은 아닙니다.** 파일 위치를 찾는 일과 내용을 읽어 분석하는 일을 구분한 설계입니다. [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/utils/githubClient.ts#L245-L267) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/tools/commonTools.ts#L623-L702)

GitHub 요청 래퍼는 응답 헤더의 남은 호출량과 초기화 시각을 읽고 지연·재시도를 수행합니다. 환경에 `GITHUB_TOKEN`이 있고 해당 요청이 인증을 사용하도록 되어 있으면 헤더에 붙입니다. 서버의 GitHub API 자격증명과 사용자 AI 클라이언트가 사용하는 모델 API 자격증명은 다른 역할입니다. 서비스가 호출 제한의 영향을 받지 않는다고 볼 수는 없으며, 실패하면 도구가 검색 실패 또는 오류 텍스트를 반환합니다. [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/utils/githubClient.ts#L71-L114) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/utils/githubClient.ts#L125-L232)

### 8. 캐시는 문서의 신선도와 질의 응답의 재사용을 함께 결정합니다

| 계층 | 코드에 정의된 수명·키 | 의미 |
|---|---|---|
| 문서 가져오기 결과 | `fetch_doc:owner:repo`, 30분 | 같은 저장소의 문서 응답 재사용 |
| 파일 경로·robots 규칙 등 KV 캐시 | 기본 12시간에 ±20% 변동 | 반복 조회를 분산하며 메타데이터 재사용 |
| raw GitHub·일반 URL 요청 | 성공 응답의 tiered cache 설정 1시간 | 외부 원문 요청의 캐시 정책 |
| AutoRAG 검색 응답 | 전체 검색 요청의 SHA-256, 12시간 | 질의·필터·순위 설정이 같으면 검색 응답 재사용 |

30분과 12시간은 서로 다른 캐시 계층의 설정입니다. 기본 브랜치를 알아내더라도 원문 요청 캐시와 준비된 R2 문서·검색 인덱스의 갱신 시점은 별도로 남습니다. 따라서 README의 “최신 문서”는 학습된 모델 지식 대신 원문을 조회한다는 방향으로 이해하되, 매 호출에서 최신 커밋을 실시간으로 읽는다는 보증으로 확장해서는 안 됩니다. [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/tools/commonTools.ts#L35-L47) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/tools/commonTools.ts#L289-L294) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/utils/cache.ts#L10-L18) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/utils/cache.ts#L269-L281) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/utils/githubClient.ts#L160-L175) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/utils/cache.ts#L349-L406)

## 문서에 있는 연결 방법과 자체 배포의 범위

### 기존 AI 클라이언트에서 문서를 쓰는 경우

공개 서비스에 연결하는 사용자는 GitMCP 서버를 직접 설치할 필요 없이, MCP를 지원하는 클라이언트에 URL을 등록합니다. 예를 들어 이 커밋 README가 제시한 Cursor 설정은 다음과 같습니다.

```json
   {
     "mcpServers": {
       "gitmcp": {
         "url": "https://gitmcp.io/{owner}/{repo}"
       }
     }
   }
```

*README의 예시를 인용했습니다. `{owner}`와 `{repo}`를 대상 저장소로 바꿉니다.* [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/README.md#L81-L92)

README는 Claude Desktop에는 `npx mcp-remote`를 이용하는 연결 설정을 제시합니다. 이는 해당 문서의 클라이언트 연결 예시이며, 모델 API를 직접 호출해 개발해야만 GitMCP를 쓸 수 있다는 뜻은 아닙니다. 반대로 내장 채팅 화면은 LLM 호출을 수행하므로 모델과 API 키의 문제를 별도로 다룹니다. 문서에 없는 최신 클라이언트 설정이나 Claude Code 명령을 이 리뷰에서 임의로 만들어 추가하지는 않습니다. [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/README.md#L94-L110)

### 브라우저 내장 채팅은 MCP 서버와 다른 데이터 경로입니다

프런트엔드 채팅 컴포넌트는 선택한 모델, MCP 서버 목록, 사용자가 설정한 API 키를 채팅 요청의 본문에 넣습니다. 이 요청의 목적지는 현재 코드에서 **별도의 `chat-api-worker.idosalomon.workers.dev/api/chat` 주소로 고정**되어 있습니다. 브라우저의 API 키를 로컬 저장소에 두는 것과, 채팅 중 그 키가 브라우저 밖으로 전달되지 않는 것은 같은 말이 아닙니다. [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/app/chat/components/api-keys-provider.tsx#L14-L22) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/app/chat/components/chat.tsx#L14-L35)

레포에 있는 `api.chat.ts` 경로는 MCP 클라이언트로 도구를 연결하고 `streamText()`로 모델의 응답을 스트리밍하는 구조를 보여 줍니다. 하지만 프런트엔드의 고정 목적지가 별도 Worker이므로, 배포된 채팅 서버가 이 파일과 같은 코드인지 이 정적 분석만으로 확인할 수는 없습니다. 이 구분은 사용자가 단순 문서 MCP 연결과 내장 채팅의 데이터 흐름을 혼동하지 않도록 하는 데 필요합니다. [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/app/routes/api.chat.ts#L112-L180)

### 자체 배포에는 Cloudflare 자원 구성이 함께 필요합니다

README에는 `git clone`, `pnpm install`, `npm run dev` 또는 `pnpm dev`로 시작하는 개발 절차와 SSE 방식의 MCP Inspector 예시가 있습니다. `package.json`의 `deploy`는 빌드 뒤 `wrangler deploy`를 실행합니다. 다만 `wrangler.jsonc`에 Durable Object·KV·R2·AI·Queue 등의 바인딩이 있으므로, 로컬 개발 명령을 실행하는 일과 동등한 문서 검색 서비스를 독립 배포하는 일은 구분해야 합니다. 검색 자료를 준비하고 큐의 후속 처리를 제공하는 범위도 확인해야 합니다. [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/README.md#L356-L386) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/package.json#L7-L20) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/wrangler.jsonc#L37-L75)

특히 자체 호스팅을 이유로 내장 채팅까지 전부 자기 환경에 남는다고 가정하면 안 됩니다. 앞에서 본 고정 채팅 API 목적지와 MCP URL을 다른 Worker 주소로 바꾸는 코드가 있으므로, 배포 경계를 이해하려면 웹 화면·MCP 도구 서버·채팅 모델 요청을 각각 따라가야 합니다. 이 글은 배포를 수행한 안내서가 아니라, 저장소의 설정과 구현으로 확인한 구조를 정리한 리뷰입니다. [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/app/chat/components/chat.tsx#L14-L35) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/app/routes/api.chat.ts#L114-L128)

## README의 보장 표현과 구현에서 확인되는 경계

### 문서가 있다는 사실은 답변의 정확성을 보증하지 않습니다

이 서버가 하는 핵심 작업은 문서 확보와 검색 결과 반환입니다. 원문의 버전이 사용자의 의존성과 맞는지, 생성 문서가 원문을 충실히 반영하는지, 도구를 받은 모델이 결과를 올바르게 사용했는지는 별도의 문제입니다. README의 “환각 없음”이라는 표현은 제품의 지향을 설명하는 주장으로 구분합니다. 이 커밋의 코드를 정적으로 읽은 결과만으로 환각률·응답 지연·가용성을 입증하지는 않았습니다. [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/README.md#L40-L57) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/tools/commonTools.ts#L266-L297)

### “질의 저장 없음”은 캐시·로그 구현과 나누어 읽어야 합니다

README는 개인 식별 정보를 받지 않고 질의를 저장하지 않는다고 설명합니다. 그러나 코드에는 검색 질의를 포함한 문자열을 `console.log()`에 기록하는 경로와 캐시 값을 로그에 출력하는 경로가 있습니다. AutoRAG 경로는 질의·필터·순위 설정을 포함한 요청의 해시를 키로 삼아 **원시 AutoRAG 응답 객체를 12시간 캐시**합니다. 이는 질의를 별도로 넣어 만드는 MCP 반환 텍스트와 다른 객체입니다. 반환 처리에서는 원시 응답의 `search_query` 필드도 읽지만, 실제 캐시 객체에 어떤 질의 정보가 들어가는지는 운영 환경에서 확인하지 않았습니다. 따라서 해시 키를 사용한다는 사실만으로 모든 질의 관련 자료가 남지 않는다고 단정할 수 없습니다. [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/README.md#L346-L350) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/tools/commonTools.ts#L449-L451) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/tools/commonTools.ts#L545-L559) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/utils/cache.ts#L67-L73) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/utils/cache.ts#L371-L406)

배포 설정은 `observability.enabled: true`, `invocation_logs: false`입니다. 호출 로그 옵션을 끈 것과 모든 애플리케이션 로그·캐시가 존재하지 않는다는 주장은 다릅니다. 여기서는 저장 가능 경로가 코드에 있다는 사실까지만 확인했으며, 실제 공개 서비스의 로그 수집 범위·보존 기간·접근 권한은 검증하지 않았습니다. 문서 MCP 연결과 내장 채팅의 API 키·메시지 전달 또한 별도로 판단해야 합니다. [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/wrangler.jsonc#L76-L81)

### 공개 읽기 도구라는 범위와 라이선스 표시를 확인합니다

README가 지원 대상으로 설명하는 것은 공개 GitHub 프로젝트입니다. 문서의 “특정 저장소” 설명을 비공개 프로젝트 접근이나 사용자별 권한 검증까지 제공한다는 뜻으로 읽지 않습니다. 공통 URL 도구는 URL을 문자열로 받아 웹 내용을 가져오며, 등록된 `readOnlyHint`는 도구의 성격을 알려주는 힌트입니다. 이것만으로 외부 네트워크 접근 전체에 대한 보안 검증이 완료되었다는 뜻도 아닙니다. [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/README.md#L334-L340) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/tools/index.ts#L18-L32) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/src/api/utils/robotsTxt.ts#L173-L203)

라이선스는 README와 루트 `LICENSE`가 Apache License 2.0을 표시합니다. 반면 `package.json`의 `license` 값은 `ISC`입니다. 이 리뷰는 두 라이선스 표시의 불일치를 기록합니다. 배포하려는 사람은 플랫폼 코드와 그 플랫폼이 가져오는 각 저장소 문서의 이용 조건도 구분해야 합니다. [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/README.md#L388-L394) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/LICENSE#L1-L5) [근거](https://github.com/idosal/git-mcp/blob/c487a29895dcfcb5b672247e646426a56e2051c1/package.json#L29-L37)

## 문서 도구를 읽는 관점에서 남는 설계

GitMCP의 학습 가치는 문서 URL을 짧게 바꾸는 편의성에만 있지 않습니다. 같은 Worker 안에서 웹 요청과 MCP 요청을 나누고, 대상 저장소를 도구의 문맥으로 고정하며, 원문 확보·검색·코드 위치 탐색을 다른 도구로 제공하는 구조가 있습니다. 그 뒤에는 캐시, R2에 준비된 문서, 외부 GitHub API, AutoRAG가 서로 다른 역할로 연결됩니다.

리뷰어 관점에서 특히 중요한 것은 **문서를 찾은 경로와, 그 문서를 얼마나 최신이라고 말할 수 있는지를 함께 읽는 습관**입니다. AutoRAG 검색 결과, 전체 문서 대체 응답, 코드 파일 위치 응답은 모두 텍스트이지만 보장하는 정보가 다릅니다. 자료를 제공하는 도구와 최종 답변을 작성하는 모델의 역할을 분리하면, 문서에 근거한 코딩을 지원하는 서버가 어디까지 책임지는지 더 정확히 이해할 수 있습니다.

## 이 글에서 다루지 못한 부분

Three.js 전용 문서 파서의 모든 경로, 프런트엔드의 전체 UI와 브라우저 저장소 동작, `vectorStore.ts`의 개별 알고리즘과 실험용 코드, 테스트·보안 정책 전체는 상세히 분석하지 않았습니다. Queue 소비자와 실제 R2 자료 생성·검색 인덱스 갱신 파이프라인, 별도 채팅 API Worker의 배포 코드·운영 설정도 이 저장소만으로 완전히 확인하지 못했습니다. 실제 검색 정확도·호출 제한·클라이언트 호환성·배포 안정성은 실행하지 않았으므로 이 글의 검증 범위 밖입니다.
