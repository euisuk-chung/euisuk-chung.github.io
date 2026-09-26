import subprocess
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import okf_metadata as om


def git(root, *args):
    return subprocess.check_output(["git", *args], cwd=root, text=True).strip()


def test_accepted_history_only_and_repeatable_log(tmp_path):
    git(tmp_path, "init", "-b", "master")
    git(tmp_path, "config", "user.name", "Test")
    git(tmp_path, "config", "user.email", "test@example.com")
    git(tmp_path, "commit", "--allow-empty", "-m", "chore(test): initialize")
    start = git(tmp_path, "rev-parse", "HEAD")
    git(tmp_path, "switch", "-c", "review")
    post = tmp_path / "okf/_posts/2026/2026-09-26-paper.md"
    post.parent.mkdir(parents=True)
    post.write_text('---\ntitle: "Draft"\n---\nBody\n')
    git(tmp_path, "add", ".")
    git(tmp_path, "commit", "-m", "feat(paper): draft")
    post.write_text('---\ntitle: "Reviewed"\n---\nHuman edit\n')
    git(tmp_path, "commit", "-am", "fix(paper): human edits")
    git(tmp_path, "switch", "master")
    assert om.entries(tmp_path, start) == []
    git(tmp_path, "merge", "--no-ff", "review", "-m", "Merge review")
    rows = om.entries(tmp_path, start)
    assert len(rows) == 1 and "Reviewed" in rows[0] and "Creation" in rows[0]
    old = "# Log\n\nHuman-maintained historical entry.\n"
    first = om.update_log(old, rows)
    assert first.startswith(old)
    assert om.update_log(first, rows) == first
    # Metadata-only commits must not create new log entries.
    (tmp_path / "okf/log.md").write_text(first)
    git(tmp_path, "add", ".")
    git(tmp_path, "commit", "-m", "chore(okf): metadata")
    assert om.entries(tmp_path, start) == rows
    post.unlink()
    git(tmp_path, "commit", "-am", "docs(paper): remove duplicate")
    rows = om.entries(tmp_path, start)
    assert len(rows) == 2 and "Deletion" in rows[0] and "/blob/" in rows[0]
    assert om.update_log(first, rows).startswith(old)


def test_invalid_log_markers_preserve_input():
    with pytest.raises(ValueError):
        om.update_log("# Log\n" + om.BEGIN, ["entry"])


def test_pending_reviews_link_to_pr_and_survive_local_index_generation(tmp_path):
    records = [dict(number=7, state='open', title='Pending', description='Summary', date='2026-09-26', sha='a'*40, url='https://github.com/example/repo/pull/7'),
               dict(number=6, state='merged', title='Accepted', description='Summary', date='2026-09-25', sha='b'*40, url='https://github.com/example/repo/pull/6')]
    block, log = om.review_sections(records)
    assert 'pull/7' in block and 'Accepted' not in block
    assert len(log) == 2 and '병합 완료' in log[1]
    text = om.okf_index.posts_index(tmp_path, pending_block=block)
    (tmp_path / 'index.md').write_text(text)
    assert om.okf_index.posts_index(tmp_path) == text
    records[0]['state'] = 'closed'
    block, log = om.review_sections(records)
    assert block == '' and '병합 없이 종료' in log[0]
