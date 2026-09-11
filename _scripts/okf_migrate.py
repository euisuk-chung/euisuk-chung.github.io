#!/usr/bin/env python3
"""포스트를 OKF v0.2 front matter + 정규화된 본문으로 변환한다.

    okf_migrate.py [--paths P ...] [--enrich enrich.json] [--overrides okf_overrides.json]
                   [--csv processed_posts.csv] [--dry-run] [--diff] [--report report.json]
                   [--check] [--strict] [--validate-enrich]

본문 변환(okf_common.normalize_body)은 결정적이고 멱등이다:
  1. UTF-8 BOM 제거
  2. 선두 `# {title}` 중복 H1 제거 (title 과 같을 때만)
  3. setext 헤딩 → ATX (`===`→`#`, `---`→`##`)
  4. 빈 줄 뒤 `---` 규칙이 바로 헤딩 앞에 오면 제거
그 외 본문은 바이트 단위로 보존되며, verify_no_loss 가 이를 강제한다.

description / tags / type 의 LLM 보강은 --enrich 사이드카(JSON)로 분리해 주입한다.
"""
from __future__ import annotations

import argparse
import csv
import difflib
import json
import sys
import unicodedata
from datetime import datetime
from pathlib import Path

import okf_common as oc


# --- processed_posts.csv → resource / generated.at ---------------------------
def load_csv_rows(csv_path: Path) -> list[dict]:
    if not csv_path.exists():
        return []
    with csv_path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        fp = (r.get("file_path") or "").replace("\\", "/")
        r["_file_path"] = unicodedata.normalize("NFC", fp)
        r["_title"] = unicodedata.normalize("NFC", r.get("title") or "")
    return rows


def resolve_csv_row(post_rel: str, title: str, rows: list[dict]) -> tuple[dict | None, str | None]:
    """(row, how) — how ∈ {csv-path, csv-title, None}."""
    post_rel = unicodedata.normalize("NFC", post_rel)
    basename = post_rel.rsplit("/", 1)[-1]
    for r in rows:
        if r["_file_path"] and (r["_file_path"] == post_rel or r["_file_path"].endswith("/" + basename)):
            return r, "csv-path"
    title_n = unicodedata.normalize("NFC", " ".join(title.split()))
    hits = [r for r in rows if r["_title"].startswith(title_n)]
    if len(hits) == 1:
        return hits[0], "csv-title"
    return None, None


def generated_at_from_row(row: dict | None, date: str) -> str:
    if row and row.get("processed_at"):
        raw = row["processed_at"].strip()
        dt = None
        for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S"):
            try:
                dt = datetime.strptime(raw, fmt)
                break
            except ValueError:
                continue
        if dt is not None:
            # CI 크롤러가 쓴 행(content_hash 있음)은 UTC, 그 이전 로컬 실행분은 KST.
            tz = "Z" if (row.get("content_hash") or "").strip() else "+09:00"
            return dt.strftime("%Y-%m-%dT%H:%M:%S") + tz
    return f"{date}T00:00:00+09:00"


# --- front matter 조립 --------------------------------------------------------
def build_post_front_matter(old: dict, post_rel: str, *, rows, overrides, types_cfg,
                            alias_map, enrich: dict | None, report: dict) -> dict:
    allowed = set(types_cfg.get("allowed", []))
    title = " ".join(str(old.get("title", "")).split())
    date = old.get("date")
    if not isinstance(date, str):
        date = date.strftime("%Y-%m-%d") if hasattr(date, "strftime") else str(date)
    date = date[:10]
    ov = (overrides or {}).get(post_rel, {})
    enrich = enrich or {}

    # type
    t = enrich.get("type") or ov.get("type") or old.get("type")
    if t not in allowed:
        t = oc.derive_type(title, types_cfg)
    # tags
    raw_tags = enrich.get("tags") if enrich.get("tags") is not None else (old.get("tags") or [])
    if isinstance(raw_tags, str):
        raw_tags = raw_tags.split()
    tags, unknown = oc.canonicalize_tags(list(raw_tags), alias_map)
    report["unknown_tags"] = unknown
    # resource
    row, how = resolve_csv_row(post_rel, title, rows)
    resource = old.get("resource") or ov.get("resource") or (row["url"].strip() if row else None)
    report["resource_source"] = "existing" if old.get("resource") else ("override" if ov.get("resource") else how)
    # generated
    generated = old.get("generated") or ov.get("generated") or {
        "by": "process:velog-sync",
        "at": generated_at_from_row(row, date),
    }
    # sources
    sources = old.get("sources")
    if not sources and resource:
        sources = [{
            "id": "velog",
            "resource": resource,
            "title": title,
            "author": "human:euisuk-chung",
            "last_modified": date,
        }]
    description = enrich.get("description") or old.get("description")
    if description:
        description = " ".join(str(description).split())
    status = old.get("status")
    if status != "deprecated":
        status = "stable" if (description and not unknown) else "draft"

    fm = {
        "type": t,
        "title": title,
        "description": description,
        "date": date,
        "tags": tags or None,
        "resource": resource,
        "generated": generated,
        "sources": sources,
        "status": status,
        "year": str(old.get("year") or date[:4]),
    }
    for k, v in old.items():
        if k not in fm:
            fm[k] = v
    return fm


def concept_file_text(tag: dict) -> str:
    fm = {
        "type": "Tag",
        "title": tag["title"],
        "slug": tag["slug"],
        "description": tag.get("description", ""),
        "aliases": tag.get("aliases", []),
        "parent": tag.get("parent"),
        "related": tag.get("related") or None,
        "status": tag.get("status", "draft"),
    }
    body = tag.get("body") or f"{tag['title']} 관련 글 모음."
    return oc.render_front_matter(fm, oc.CONCEPT_KEY_ORDER) + "\n" + body.rstrip("\n") + "\n"


def create_new_concepts(enrich_all: dict, concepts_dir: Path, dry_run: bool) -> list[str]:
    created: list[str] = []
    existing = oc.load_concepts(concepts_dir)
    existing_slugs = {c.slug for c in existing.values()}
    for entry in enrich_all.values():
        for tag in entry.get("new_tags", []) or []:
            title, slug = tag.get("title"), tag.get("slug")
            if not title or not slug or title in existing or slug in existing_slugs:
                continue
            if not oc.SLUG_RE.match(slug):
                raise SystemExit(f"invalid slug in new_tags: {slug!r}")
            path = concepts_dir / f"{slug}.md"
            if not dry_run:
                concepts_dir.mkdir(parents=True, exist_ok=True)
                path.write_text(concept_file_text(tag), encoding="utf-8")
            existing_slugs.add(slug)
            existing[title] = oc.Concept(path=path, title=title, slug=slug,
                                         aliases=tag.get("aliases", []))
            created.append(str(path))
    return created


def validate_enrich(enrich_all: dict, alias_map: dict[str, str], posts: list[Path]) -> list[str]:
    problems = []
    known_paths = {oc.rel_posix(p) for p in posts}
    new_titles = set()
    for entry in enrich_all.values():
        for tag in entry.get("new_tags", []) or []:
            new_titles.add(tag.get("title"))
    for path, entry in enrich_all.items():
        if path not in known_paths:
            problems.append(f"{path}: not a post in --paths")
        d = entry.get("description")
        if d is not None and (not isinstance(d, str) or not d.strip() or "\n" in d.strip()):
            problems.append(f"{path}: description must be a single non-empty line")
        for t in entry.get("tags", []) or []:
            if not (alias_map.get(t) or alias_map.get(t.casefold()) or t in new_titles):
                problems.append(f"{path}: tag {t!r} not in vocabulary or new_tags")
    return problems


# --- 파일 단위 변환 -----------------------------------------------------------
def migrate_text(text: str, post_rel: str, ctx: dict, enrich: dict | None) -> tuple[str, dict]:
    doc = oc.parse_document(text)
    if not doc.has_front_matter:
        raise ValueError("no front matter")
    title = " ".join(str(doc.front_matter.get("title", "")).split())
    new_body, body_report = oc.normalize_body(doc.body, title)
    problems = oc.verify_no_loss(doc.body, new_body, title)
    if problems:
        raise ValueError("content-loss check failed: " + "; ".join(problems[:3]))
    report = body_report.as_dict()
    report["bom_stripped"] = doc.had_bom
    fm = build_post_front_matter(doc.front_matter, post_rel, rows=ctx["rows"], overrides=ctx["overrides"],
                                 types_cfg=ctx["types_cfg"], alias_map=ctx["alias_map"],
                                 enrich=enrich, report=report)
    # front matter 와 본문 사이는 정확히 빈 줄 하나 (재실행 시 빈 줄이 누적되지 않도록 선두 빈 줄 제거)
    out = oc.render_front_matter(fm) + "\n" + new_body.lstrip("\n")
    return out, report


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--paths", nargs="*", help="포스트 파일 또는 디렉터리 (기본: config posts_dir)")
    ap.add_argument("--enrich", help="LLM 보강 사이드카 JSON")
    ap.add_argument("--overrides", default=str(oc.SCRIPT_DIR / "okf_overrides.json"))
    ap.add_argument("--csv", default=str(oc.REPO_ROOT / "processed_posts.csv"))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--diff", action="store_true", help="파일별 unified diff 출력")
    ap.add_argument("--report", help="파일별 변환 리포트 JSON 경로")
    ap.add_argument("--check", action="store_true",
                    help="이미 변환된 파일이 멱등(재실행 시 무변경)인지 검사. 미변환(legacy) 파일은 --strict 없으면 건너뜀")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--validate-enrich", action="store_true", help="사이드카만 검증하고 종료")
    args = ap.parse_args(argv)

    cfg = oc.load_config()
    posts_dir = oc.REPO_ROOT / cfg["posts_dir"]
    concepts_dir = oc.REPO_ROOT / cfg["concepts_dir"]
    targets: list[Path] = []
    for p in (args.paths or [str(posts_dir)]):
        pp = oc.resolve_path(p)
        if pp.is_dir():
            targets.extend(oc.iter_post_files(pp))
        elif pp.is_file():
            targets.append(pp)
        else:
            print(f"[warn] not found: {p}", file=sys.stderr)
    targets = sorted(set(targets))

    types_cfg = oc.load_types_config()
    overrides = {}
    if Path(args.overrides).exists():
        overrides = json.loads(Path(args.overrides).read_text(encoding="utf-8")).get("posts", {})
    enrich_all = {}
    if args.enrich:
        enrich_all = json.loads(Path(args.enrich).read_text(encoding="utf-8"))
        enrich_all = {unicodedata.normalize("NFC", k): v for k, v in enrich_all.items()}

    concepts = oc.load_concepts(concepts_dir)
    alias_map = oc.build_alias_map(concepts)
    if enrich_all:
        problems = validate_enrich(enrich_all, alias_map, targets)
        if problems:
            print("\n".join("[enrich] " + p for p in problems), file=sys.stderr)
            return 1
        if args.validate_enrich:
            print(f"enrich ok: {len(enrich_all)} entries")
            return 0
        created = create_new_concepts(enrich_all, concepts_dir, args.dry_run)
        for c in created:
            print(f"[concept] created {c}")
        concepts = oc.load_concepts(concepts_dir)
        alias_map = oc.build_alias_map(concepts)
        if args.dry_run:
            for entry in enrich_all.values():
                for tag in entry.get("new_tags", []) or []:
                    alias_map.setdefault(tag["title"], tag["title"])

    ctx = {"rows": load_csv_rows(Path(args.csv)), "overrides": overrides,
           "types_cfg": types_cfg, "alias_map": alias_map}

    reports: dict[str, dict] = {}
    failures = 0
    changed = 0
    for path in targets:
        rel = oc.rel_posix(path)
        text = path.read_text(encoding="utf-8")
        try:
            if args.check:
                doc = oc.parse_document(text)
                if not doc.front_matter.get("type") and not args.strict:
                    continue
                out, rep = migrate_text(text, rel, ctx, None)
                if out != text:
                    failures += 1
                    print(f"[check] not idempotent: {rel}")
                    if args.diff:
                        sys.stdout.writelines(difflib.unified_diff(
                            text.splitlines(True), out.splitlines(True), rel, rel + " (re-run)"))
                continue
            out, rep = migrate_text(text, rel, ctx, enrich_all.get(rel))
        except ValueError as e:
            failures += 1
            print(f"[error] {rel}: {e}", file=sys.stderr)
            continue
        reports[rel] = rep
        if out == text:
            continue
        changed += 1
        if args.diff:
            sys.stdout.writelines(difflib.unified_diff(
                text.splitlines(True), out.splitlines(True), rel, rel))
        if not args.dry_run:
            path.write_text(out, encoding="utf-8")

    if args.report and not args.check:
        Path(args.report).write_text(json.dumps(reports, ensure_ascii=False, indent=2), encoding="utf-8")
    mode = "check" if args.check else ("dry-run" if args.dry_run else "write")
    print(f"[{mode}] files={len(targets)} changed={changed} failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
