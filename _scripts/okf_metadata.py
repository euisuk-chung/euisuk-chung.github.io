#!/usr/bin/env python3
"""Refresh published indexes, pending review links and investigation history.

Run on master only. First-parent history records the accepted result of a PR,
not its draft commits. Existing manual log entries remain byte-identical.
"""
from __future__ import annotations

import argparse
import base64
from datetime import datetime, timezone, timedelta
import html
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import quote

import okf_common as oc
import okf_index

START = "72771b6bb48e0b4ea754da6d80d102317880ce38"
BEGIN = "<!-- okf-metadata:start -->"
END = "<!-- okf-metadata:end -->"
REPO = "euisuk-chung/euisuk-chung.github.io"
CONTENT = re.compile(r"okf/(?:_posts/\d{4}/\d{4}-\d{2}-\d{2}-[^/]+|_concepts/[^/]+)\.md\Z")


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=repo, text=True)


def gh_pages(endpoint: str) -> list[dict]:
    pages = json.loads(subprocess.check_output(["gh", "api", "--paginate", "--slurp", endpoint], text=True))
    return [item for page in pages for item in page]


def label(text: str) -> str:
    return html.escape(" ".join(str(text).split()), quote=False).replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]")


def review_records() -> list[dict]:
    records = []
    for pr in gh_pages(f"repos/{REPO}/pulls?state=all&per_page=100"):
        if (pr['head'].get('repo') or {}).get('full_name') != REPO:
            continue
        if not re.match(r"codex/(paper|repo)-", pr['head']['ref']) and not re.match(r"\w+\((paper|repo)\):", pr['title']):
            continue
        files = gh_pages(f"repos/{REPO}/pulls/{pr['number']}/files?per_page=100")
        for file in files:
            path = file['filename']
            if not re.fullmatch(r"(?:okf/)?_posts/\d{4}/\d{4}-\d{2}-\d{2}-[^/]+\.md", path) or file['status'] == 'removed':
                continue
            # Read immutable blob data only; never check out or execute PR code.
            blob = json.loads(subprocess.check_output(["gh", "api", f"repos/{REPO}/git/blobs/{file['sha']}"], text=True))
            if blob.get('encoding') != 'base64' or blob.get('size', 0) > 2_000_000:
                raise ValueError(f"Unexpected review blob for PR {pr['number']}")
            fm = oc.parse_document(base64.b64decode(blob['content']).decode('utf-8')).front_matter
            if fm.get('type') not in ('Paper Review', 'Repo Review') and fm.get('source_type') not in ('paper', 'repo'):
                continue
            records.append(dict(number=pr['number'], state='merged' if pr['merged_at'] else pr['state'],
                                title=label(fm.get('title', pr['title'])), description=label(fm.get('description', fm.get('summary', ''))),
                                date=str(datetime.fromisoformat(pr['created_at'].replace('Z', '+00:00')).astimezone(timezone(timedelta(hours=9))).date()),
                                sha=pr['head']['sha'], url=pr['html_url']))
    return sorted(records, key=lambda x: (x['number'], x['title']), reverse=True)


def review_sections(records: list[dict]) -> tuple[str, list[str]]:
    pending = [f"* [{r['title']}]({r['url']}) — 검토 대기 · {r['description']}" for r in records if r['state'] == 'open']
    block = "\n".join([okf_index.PENDING_BEGIN, "## 검토 중인 리뷰", "", *pending, okf_index.PENDING_END]) if pending else ""
    states = {'open': '검토 대기', 'merged': '병합 완료', 'closed': '병합 없이 종료'}
    log = [f"* {r['date']} **Review**: [{r['title']}]({r['url']}) — {states[r['state']]} · PR #{r['number']} · `{r['sha'][:7]}`" for r in records]
    return block, log


def entries(repo: Path, since: str) -> list[str]:
    subprocess.run(["git", "merge-base", "--is-ancestor", since, "HEAD"], cwd=repo, check=True)
    result = []
    for sha in git(repo, "rev-list", "--first-parent", f"{since}..HEAD").splitlines():
        parent = git(repo, "rev-parse", sha + "^1").strip()
        fields = git(repo, "diff", "--name-status", "--no-renames", "-z", parent, sha, "--", "okf").rstrip("\0").split("\0")
        date = datetime.fromtimestamp(int(git(repo, "show", "-s", "--format=%ct", sha)), timezone(timedelta(hours=9))).date()
        for status, path in zip(fields[::2], fields[1::2]):
            if not CONTENT.fullmatch(path):
                continue
            revision = parent if status == "D" else sha
            text = git(repo, "show", f"{revision}:{path}")
            fm = oc.parse_document(text).front_matter
            title = " ".join(str(fm.get("title", Path(path).stem)).split())
            title = title.replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]")
            action = {"A": "Creation", "D": "Deletion"}.get(status, "Update")
            # Deleted documents have no working-tree link.
            target = f"https://github.com/euisuk-chung/euisuk-chung.github.io/blob/{revision}/{quote(path)}" if status == "D" else quote(path.removeprefix("okf/"))
            result.append(f"* {date} **{action}**: [{title}]({target}) — `{sha[:7]}`")
    return result


def update_log(current: str, rows: list[str]) -> str:
    block = BEGIN + "\n## 리뷰 작성 및 콘텐츠 변경 기록\n\n" + "\n".join(rows) + "\n" + END
    if BEGIN in current or END in current:
        if current.count(BEGIN) != 1 or current.count(END) != 1 or current.index(BEGIN) > current.index(END):
            raise ValueError("Invalid generated log markers; preserve the existing log for inspection")
        start, end = current.index(BEGIN), current.index(END) + len(END)
        return current[:start] + block + current[end:]
    if not rows:
        return current
    # Append a managed section without rewriting any historical manual entry.
    return current + ("" if current.endswith("\n\n") else "\n" if current.endswith("\n") else "\n\n") + block + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    cfg = oc.load_config()
    log = oc.REPO_ROOT / cfg["okf_root"] / "log.md"
    pending, reviews = review_sections(review_records())
    targets = okf_index.targets(cfg, pending_block=pending)
    targets.append((log, update_log(log.read_text(encoding="utf-8"), reviews + entries(oc.REPO_ROOT, START))))
    changed = 0
    for path, content in targets:
        if path.read_text(encoding="utf-8") != content:
            changed += 1
            if args.write:
                path.write_text(content, encoding="utf-8")
            print(f"[metadata] {'wrote' if args.write else 'out of date'} {oc.rel_posix(path)}")
    return int(bool(changed) and args.check)


if __name__ == "__main__":
    raise SystemExit(main())
