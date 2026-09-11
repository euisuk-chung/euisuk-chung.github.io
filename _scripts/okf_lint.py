#!/usr/bin/env python3
"""OKF 콘텐츠 린트.

    okf_lint.py [--paths P ...] [--strict] [--allow-draft] [--changed] [--check-index]

포스트(E***), 태그 concept(T***), 인덱스(I***) 규칙을 검사한다.
출력: `path:line: [CODE] message`, 오류가 있으면 exit 1.
`type` 이 없는 포스트는 아직 OKF 로 전환되지 않은 legacy 로 보고 --strict 없으면 경고만 낸다.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import okf_common as oc


class Lint:
    def __init__(self, strict: bool, allow_draft: bool):
        self.strict = strict
        self.allow_draft = allow_draft
        self.errors = 0
        self.warnings = 0

    def err(self, path, code, msg, line=1):
        self.errors += 1
        print(f"{path}:{line}: [{code}] {msg}")

    def warn(self, path, code, msg, line=1):
        self.warnings += 1
        print(f"{path}:{line}: [{code}] (warning) {msg}")


def lint_post(path: Path, text: str, L: Lint, concepts, types_cfg) -> None:
    rel = oc.rel_posix(path)
    has_bom = text.startswith(oc.BOM)
    try:
        doc = oc.parse_document(text)
    except Exception as e:  # yaml error
        L.err(rel, "E002", f"front matter does not parse: {e}")
        return
    if not doc.has_front_matter:
        L.err(rel, "E002", "no front matter")
        return
    fm = doc.front_matter
    legacy = not fm.get("type")
    draft = fm.get("status") == "draft"
    lenient = (legacy and not L.strict) or (draft and L.allow_draft)
    soft = L.warn if lenient else L.err

    if has_bom:
        (L.warn if legacy and not L.strict else L.err)(rel, "E001", "file starts with a UTF-8 BOM")
    if legacy:
        soft(rel, "E003", "missing `type` (legacy post, run okf_migrate.py)")
    elif fm["type"] not in types_cfg.get("allowed", []):
        L.err(rel, "E003", f"type {fm['type']!r} not in okf_types.json allowed list")
    if not fm.get("title"):
        L.err(rel, "E004", "missing `title`")
    m = oc.POST_FILENAME_RE.match(path.name)
    date = str(fm.get("date", ""))[:10]
    if m and date != m.group(1):
        L.err(rel, "E005", f"front-matter date {date} != filename date {m.group(1)}")
    desc = fm.get("description")
    if not desc:
        soft(rel, "E006", "missing `description`")
    elif not isinstance(desc, str) or "\n" in desc.strip() or len(desc) > 200:
        L.err(rel, "E006", "description must be a single line of at most 200 chars")
    tags = fm.get("tags") or []
    if isinstance(tags, str):
        tags = tags.split()
    for t in tags:
        if str(t) not in concepts:
            soft(rel, "E007", f"tag {t!r} has no concept file (title must match exactly)")
    val = fm.get("resource")
    if val and not str(val).startswith(("http://", "https://", "/")):
        L.err(rel, "E008", f"resource must be an http(s) URL or bundle path: {val!r}")
    for i, s in enumerate(fm.get("sources") or []):
        r = (s or {}).get("resource") if isinstance(s, dict) else None
        if not r or not str(r).startswith(("http://", "https://", "/", "./", "../")):
            L.err(rel, "E008", f"sources[{i}].resource missing or invalid")
    gen = fm.get("generated")
    if gen is not None:
        if not isinstance(gen, dict) or not oc.ACTOR_RE.match(str(gen.get("by", ""))):
            L.err(rel, "E009", "generated.by must be human:<id> | process:<id> | <producer>/<version>")
        if isinstance(gen, dict) and gen.get("at") and not oc.ISO_DT_RE.match(str(gen["at"])):
            L.err(rel, "E009", f"generated.at is not ISO-8601: {gen['at']!r}")
    elif not legacy:
        L.err(rel, "E009", "missing `generated`")
    if fm.get("status") is not None and fm["status"] not in oc.STATUS_VALUES:
        L.err(rel, "E010", f"status must be one of {oc.STATUS_VALUES}")

    # 본문 검사 (코드 영역 제외)
    lines = doc.body.split("\n")
    mask = oc.code_mask(lines)
    offset = doc.fm_text.count("\n") + 3  # ---, fm, ---
    for i, ln in enumerate(lines):
        if mask[i]:
            continue
        if i > 0 and lines[i - 1].strip() and not mask[i - 1] and oc.UNDERLINE_RE.match(ln) \
                and not oc.ATX_RE.match(lines[i - 1]) and not oc.HR_RE.match(lines[i - 1]) \
                and not oc.UNDERLINE_RE.match(lines[i - 1]) and not oc.INDENTED_CODE_RE.match(lines[i - 1]) \
                and not oc.TABLE_ROW_RE.match(lines[i - 1]) and not oc.BLOCKQUOTE_RE.match(lines[i - 1]):
            soft(rel, "E011", "setext heading (use ATX `#`)", offset + i)
        if oc.HR_RE.match(ln) and (i == 0 or not lines[i - 1].strip()):
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and oc.ATX_RE.match(lines[j]) and not mask[j]:
                soft(rel, "E013", "`---` rule directly before a heading (theme already draws a divider)", offset + i)
    first = next((ln for ln in lines if ln.strip()), "")
    title = " ".join(str(fm.get("title", "")).split())
    if first.startswith("# ") and oc._norm_title(first[2:]) == oc._norm_title(title):
        soft(rel, "E012", "body starts with a duplicate `# {title}` H1", offset + 1)


def lint_concepts(concepts_dir: Path, L: Lint) -> dict:
    concepts = oc.load_concepts(concepts_dir)
    seen: dict[str, str] = {}
    slugs = {c.slug for c in concepts.values()}
    for c in concepts.values():
        rel = oc.rel_posix(c.path)
        if c.data.get("type") != "Tag":
            L.err(rel, "T001", "concept `type` must be \"Tag\"")
        if c.slug != c.path.stem or not oc.SLUG_RE.match(c.slug):
            L.err(rel, "T002", f"slug {c.slug!r} must equal the filename stem and be kebab-case ASCII")
        for name in [c.title, *c.aliases]:
            key = name.casefold()
            if key in seen and seen[key] != c.title:
                L.err(rel, "T003", f"{name!r} is already used by concept {seen[key]!r}")
            seen.setdefault(key, c.title)
        for ref in ([c.parent] if c.parent else []) + list(c.related):
            if ref not in slugs:
                L.err(rel, "T004", f"dangling reference to slug {ref!r}")
        if not c.description:
            L.warn(rel, "T006", "concept has no description")
    by_slug = {c.slug: c for c in concepts.values()}
    for c in concepts.values():
        seen_s, cur = set(), c
        while cur and cur.parent:
            if cur.slug in seen_s:
                L.err(oc.rel_posix(c.path), "T005", "parent cycle")
                break
            seen_s.add(cur.slug)
            cur = by_slug.get(cur.parent)
    return concepts


def changed_files() -> set[str]:
    out = subprocess.run(["git", "diff", "--name-only", "origin/master"], capture_output=True, text=True,
                         cwd=oc.REPO_ROOT).stdout
    out2 = subprocess.run(["git", "ls-files", "--others", "--exclude-standard"], capture_output=True, text=True,
                          cwd=oc.REPO_ROOT).stdout
    return {l.strip() for l in (out + out2).splitlines() if l.strip()}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--paths", nargs="*")
    ap.add_argument("--strict", action="store_true", help="legacy(type 없는) 포스트도 오류로 처리")
    ap.add_argument("--allow-draft", action="store_true", help="status: draft 포스트의 description/태그 누락은 경고")
    ap.add_argument("--changed", action="store_true", help="origin/master 대비 변경된 포스트만")
    ap.add_argument("--check-index", action="store_true", help="index.md 가 최신인지 검사 (okf_index.py --check)")
    args = ap.parse_args(argv)

    cfg = oc.load_config()
    posts_dir = oc.REPO_ROOT / cfg["posts_dir"]
    concepts_dir = oc.REPO_ROOT / cfg["concepts_dir"]
    types_cfg = oc.load_types_config()
    L = Lint(args.strict, args.allow_draft)

    concepts = lint_concepts(concepts_dir, L)

    targets: list[Path] = []
    for p in (args.paths or [str(posts_dir)]):
        pp = oc.resolve_path(p)
        if pp.is_dir():
            targets.extend(oc.iter_post_files(pp))
        elif pp.is_file() and oc.POST_FILENAME_RE.match(pp.name):
            targets.append(pp)
    if args.changed:
        ch = changed_files()
        targets = [t for t in targets if oc.rel_posix(t) in ch]
    for path in sorted(set(targets)):
        lint_post(path, path.read_text(encoding="utf-8"), L, concepts, types_cfg)

    if args.check_index:
        import okf_index
        rc = okf_index.main(["--check"])
        if rc:
            L.err(cfg["okf_root"], "I001", "index.md is out of date (run okf_index.py --write)")

    print(f"lint: {len(targets)} posts, {len(concepts)} concepts, {L.errors} errors, {L.warnings} warnings")
    return 1 if L.errors else 0


if __name__ == "__main__":
    sys.exit(main())
