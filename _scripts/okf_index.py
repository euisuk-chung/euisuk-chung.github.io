#!/usr/bin/env python3
"""OKF 예약 파일 index.md 생성/검사.

    okf_index.py --write   # <posts_dir>/index.md, <okf_root>/index.md 갱신
    okf_index.py --check   # 현재 파일과 생성 결과가 같은지 (다르면 exit 1)

index.md 는 OKF §8 progressive-disclosure 목록이다: `# Section` 아래 `* [Title](path) - description`.
posts_dir 가 okf_root 안에 있을 때만 루트 index 를 만든다(번들 레이아웃 전에는 posts index 만).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import okf_common as oc


def _desc(fm: dict) -> str:
    return " ".join(str(fm.get("description") or "").split())


def posts_index(posts_dir: Path) -> str:
    by_year: dict[str, list[tuple[str, str, str, str]]] = {}
    for p in oc.iter_post_files(posts_dir):
        fm = oc.parse_document(p.read_text(encoding="utf-8")).front_matter
        year = p.name[:4]
        rel = p.relative_to(posts_dir).as_posix()
        by_year.setdefault(year, []).append((p.name[:10], rel, str(fm.get("title", p.stem)), _desc(fm)))
    out = ["# Posts", ""]
    for year in sorted(by_year, reverse=True):
        out.append(f"## {year}")
        out.append("")
        for _date, path, title, desc in sorted(by_year[year], reverse=True):
            out.append(f"* [{title}]({path})" + (f" - {desc}" if desc else ""))
        out.append("")
    return "\n".join(out).rstrip("\n") + "\n"


def root_index(okf_root: Path, posts_dir: Path, concepts_dir: Path) -> str:
    out = ['---', 'okf_version: "0.2"', '---', '', '# Euisuk Chung Dev Log — OKF bundle', '']
    out.append("Blog posts (concepts of kind Blog Post, Paper Review, …) and the tag vocabulary that classifies them.")
    out.append("")
    out.append("# Posts")
    out.append("")
    prel = posts_dir.relative_to(okf_root).as_posix()
    out.append(f"* [All posts by year]({prel}/index.md) - chronological listing")
    years = sorted({p.name[:4] for p in oc.iter_post_files(posts_dir)}, reverse=True)
    for y in years:
        out.append(f"* [{y}]({prel}/{y}/) - posts published in {y}")
    out.append("")
    out.append("# Tags")
    out.append("")
    crel = concepts_dir.relative_to(okf_root).as_posix()
    for c in sorted(oc.load_concepts(concepts_dir).values(), key=lambda c: c.slug):
        out.append(f"* [{c.title}]({crel}/{c.slug}.md)" + (f" - {c.description}" if c.description else ""))
    out.append("")
    out.append("# Log")
    out.append("")
    out.append("* [Update log](log.md) - chronological record of additions and updates")
    return "\n".join(out) + "\n"


def targets(cfg: dict) -> list[tuple[Path, str]]:
    posts_dir = oc.REPO_ROOT / cfg["posts_dir"]
    concepts_dir = oc.REPO_ROOT / cfg["concepts_dir"]
    okf_root = oc.REPO_ROOT / cfg["okf_root"]
    result = [(posts_dir / "index.md", posts_index(posts_dir))]
    if okf_root.exists() and posts_dir.resolve().is_relative_to(okf_root.resolve()):
        result.append((okf_root / "index.md", root_index(okf_root, posts_dir, concepts_dir)))
    return result


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--write", action="store_true")
    g.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    cfg = oc.load_config()
    rc = 0
    for path, content in targets(cfg):
        if args.write:
            path.write_text(content, encoding="utf-8")
            print(f"[index] wrote {oc.rel_posix(path)}")
        else:
            if not path.exists():
                print(f"[index] not initialized, skipping: {oc.rel_posix(path)} (run --write to create)")
                continue
            current = path.read_text(encoding="utf-8")
            if current != content:
                print(f"[index] out of date: {oc.rel_posix(path)}")
                rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
