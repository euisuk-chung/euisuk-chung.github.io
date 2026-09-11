#!/usr/bin/env python3
"""마이그레이션 전후 Jekyll 빌드 결과(_site) 비교.

    okf_roundtrip.py <site-before> <site-after> [--report report.json]

각 포스트 페이지의 `.post-container` 텍스트가 다음 정규화 후 동일해야 한다:
  (a) before 의 본문 첫 <h1> (테마 헤더와 중복된 제목) 제거
  (b) 헤딩 텍스트 앞의 `N. ` / `* ` 목록 마커 제거 (setext 번호 헤딩이 <ol><li><h2> 로 잘못 렌더되던 것의 보정)
  (c) 공백 정규화
추가로 <hr> 감소 총합이 리포트의 hr_removed 합과 같은지, <ol><li><h2> 가 after 에 남아있지 않은지,
생성된 파일 경로 집합이 같은지 검사한다.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

HEADINGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
BLOCK_TAGS = HEADINGS | {"p", "li", "pre", "blockquote", "td", "th", "div"}
LIST_MARK = re.compile(r"^(\d+\.|[*+-])\s+")


class PostExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.blocks: list[tuple[str, str]] = []
        self.hr = 0
        self.ol_li_h2 = 0
        self.stack: list[str] = []
        self.cur_tag = "p"
        self.buf: list[str] = []
        self.skip = 0
        self.stopped = False  # 본문 뒤의 태그 푸터/광고/페이저는 비교 대상이 아니다

    def handle_starttag(self, tag, attrs):
        cls = dict(attrs).get("class", "") or ""
        if self.depth == 0:
            if tag == "div" and "post-container" in cls.split():
                self.depth = 1
            return
        if not self.stopped and ({"post-tags-footer", "pager"} & set(cls.split()) or tag == "ins"):
            self._flush()
            self.stopped = True
        if tag in ("br", "img", "hr", "input", "meta", "link"):
            if tag == "hr" and not self.stopped:
                self.hr += 1
            return
        self.depth += 1
        if tag in ("script", "style"):
            self.skip += 1
        if tag in BLOCK_TAGS:
            self._flush()
            self.cur_tag = tag
        if tag == "h2" and len(self.stack) >= 2 and self.stack[-1] == "li" and self.stack[-2] == "ol":
            self.ol_li_h2 += 1
        self.stack.append(tag)

    def handle_endtag(self, tag):
        if self.depth == 0 or tag in ("br", "img", "hr", "input", "meta", "link"):
            return
        if tag in ("script", "style") and self.skip:
            self.skip -= 1
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        if tag in BLOCK_TAGS:
            self._flush()
        self.depth -= 1

    def handle_data(self, data):
        if self.depth and not self.skip and not self.stopped:
            self.buf.append(data)

    def _flush(self):
        text = " ".join("".join(self.buf).split())
        self.buf = []
        if text:
            self.blocks.append((self.cur_tag, text))
        self.cur_tag = "p"

    def close(self):
        super().close()
        self._flush()


def normalized_text(html: str, strip_first_h1: bool, title: str | None = None) -> tuple[str, int, int]:
    ex = PostExtractor()
    ex.feed(html)
    ex.close()
    blocks = list(ex.blocks)
    if strip_first_h1 and blocks:
        # 중복 제목: 첫 <h1> 하나, 또는 여러 줄로 접힌 제목이 h1 + 이어지는 문단으로 렌더된 경우
        folded = " ".join(title.split()) if title else None
        acc, k, dropped = "", 0, False
        if folded:
            for k in range(1, min(4, len(blocks)) + 1):
                acc = " ".join(t for _, t in blocks[:k])
                if acc == folded:
                    blocks = blocks[k:]
                    dropped = True
                    break
        if not dropped and blocks[0][0] == "h1":
            blocks = blocks[1:]
    parts = []
    for tag, text in blocks:
        if tag in HEADINGS:
            text = LIST_MARK.sub("", text)
        parts.append(text)
    return " ".join(parts), ex.hr, ex.ol_li_h2


def page_paths_for_report(report: dict, site: Path) -> set[str]:
    """리포트 키(포스트 소스 경로) → 출력 페이지 경로(YYYY/MM/DD/<slug>/index.html).

    Jekyll 의 :title 슬러그를 재구현하지 않고, 같은 날짜 디렉터리 아래 페이지 중
    <title> 에 포스트 제목이 들어있는 것을 고른다.
    """
    import html as htmlmod
    pages: set[str] = set()
    for rel in report:
        name = rel.rsplit("/", 1)[-1]
        m = re.match(r"^(\d{4})-(\d{2})-(\d{2})-", name)
        if not m:
            continue
        day_dir = site / m.group(1) / m.group(2) / m.group(3)
        if not day_dir.is_dir():
            continue
        candidates = [p for p in day_dir.iterdir() if (p / "index.html").is_file()]
        if len(candidates) == 1:
            pages.add((candidates[0] / "index.html").relative_to(site).as_posix())
            continue
        title = post_title(Path(site).parent / rel)
        if not title:
            continue
        # 정확 일치 우선 (한 제목이 다른 제목의 부분 문자열인 같은 날 글 구분), 없으면 부분 일치
        scored = []
        for c in candidates:
            page = (c / "index.html").read_text(encoding="utf-8", errors="replace")
            tt = re.search(r"<title>(.*?)</title>", page, re.S)
            if not tt:
                continue
            page_title = _fold(tt.group(1)).split(" | ")[0]
            if page_title == _fold(title):
                scored.append((0, c))
            elif _fold(title) in page_title:
                scored.append((1, c))
        if scored:
            scored.sort(key=lambda x: x[0])
            pages.add((scored[0][1] / "index.html").relative_to(site).as_posix())
    return pages


def _fold(text: str) -> str:
    """제목 비교용: HTML 언이스케이프, 공백 접기, 타이포그래피 따옴표를 ASCII 로."""
    import html as htmlmod
    t = " ".join(htmlmod.unescape(text).split())
    return t.replace("\u2018", "'").replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')


def post_title(src: Path) -> str | None:
    """포스트 소스의 front matter title (공백 접기). 여러 줄 따옴표 제목도 처리."""
    if not src.exists():
        return None
    try:
        import okf_common as oc
        fm = oc.parse_document(src.read_text(encoding="utf-8", errors="replace")).front_matter
        return " ".join(str(fm.get("title", "")).split()) or None
    except Exception:
        return None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("before")
    ap.add_argument("after")
    ap.add_argument("--report", help="okf_migrate.py --report 산출물 (hr_removed 대조용)")
    args = ap.parse_args(argv)
    before, after = Path(args.before), Path(args.after)
    report = json.loads(Path(args.report).read_text(encoding="utf-8")) if args.report else {}

    files_b = {p.relative_to(before).as_posix() for p in before.rglob("*") if p.is_file()}
    files_a = {p.relative_to(after).as_posix() for p in after.rglob("*") if p.is_file()}
    problems = 0
    removed_paths = files_b - files_a
    added_paths = {p for p in files_a - files_b if not p.startswith("tags/")}  # 새 태그 페이지는 허용
    if removed_paths or added_paths:
        problems += 1
        print(f"[paths] only-before={sorted(removed_paths)[:5]} only-after={sorted(added_paths)[:5]}")
    new_tag_pages = sorted(p for p in files_a - files_b if p.startswith("tags/"))
    if new_tag_pages:
        print(f"[paths] new tag pages: {new_tag_pages}")

    expected_hr = sum(r.get("hr_removed", 0) for r in report.values())
    pages = page_paths_for_report(report, after) if report else None
    titles: dict[str, str] = {}
    if pages is not None:
        for rel in report:
            t = post_title(Path(after).parent / rel)
            if not t:
                continue
            for p in pages:
                page = (after / p).read_text(encoding="utf-8", errors="replace")
                tt = re.search(r"<title>(.*?)</title>", page, re.S)
                if tt and _fold(tt.group(1)).split(" | ")[0] == _fold(t):
                    titles[p] = t
                    break
    if pages is not None:
        print(f"[pages] {len(pages)} of {len(report)} report entries mapped to output pages")
    hr_delta = 0
    checked = 0
    for rel in sorted(files_a & files_b):
        if not rel.endswith("index.html") or not re.match(r"^\d{4}/\d{2}/\d{2}/", rel):
            continue
        if pages is not None and rel not in pages:
            continue
        hb = (before / rel).read_text(encoding="utf-8", errors="replace")
        ha = (after / rel).read_text(encoding="utf-8", errors="replace")
        if hb == ha:
            continue
        title = titles.get(rel)
        tb, hrb, _ = normalized_text(hb, strip_first_h1=True, title=title)
        ta, hra, olh2 = normalized_text(ha, strip_first_h1=False)
        checked += 1
        hr_delta += hrb - hra
        if olh2:
            problems += 1
            print(f"[ol>li>h2] still present in {rel}")
        if tb != ta:
            problems += 1
            i = next((k for k, (x, y) in enumerate(zip(tb, ta)) if x != y), min(len(tb), len(ta)))
            print(f"[text] {rel}\n   before: …{tb[max(0, i-60):i+80]!r}\n   after:  …{ta[max(0, i-60):i+80]!r}")
    if report and hr_delta != expected_hr:
        problems += 1
        print(f"[hr] removed <hr> delta {hr_delta} != report hr_removed {expected_hr}")
    print(f"roundtrip: {checked} changed pages compared, hr delta {hr_delta}, problems {problems}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
