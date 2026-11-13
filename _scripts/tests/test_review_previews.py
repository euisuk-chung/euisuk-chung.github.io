import importlib.util
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location('review_previews', Path(__file__).parents[1] / 'build_review_previews.py')
preview = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preview)


def test_same_repository_content_branches_include_reports():
    for branch in ('codex/paper-2609.35738', 'codex/repo-owner-name',
                   'codex/guide-agent-tools', 'codex/state-of-ai-2026'):
        assert preview.preview_candidate({'headRefName': branch, 'isCrossRepository': False})
        assert not preview.preview_candidate({'headRefName': branch, 'isCrossRepository': True})
    for branch in ('master', 'feature/report', 'codex/', 'codex/../report',
                   'codex/report/nested', 'codex/report;command'):
        assert not preview.preview_candidate({'headRefName': branch, 'isCrossRepository': False})


def test_only_post_concept_and_visual_content_can_enter_preview():
    for path in ('okf/_posts/2026/2026-09-12-review.md', 'okf/_concepts/paper-review.md',
                 'img/reviews/2026/paper/figure-1.png'):
        assert preview.permitted(path)
    for path in ('_plugins/evil.rb', '_config.yml', 'Gemfile', '.github/workflows/evil.yml',
                 'okf/_posts/../../_plugins/evil.rb', '/img/reviews/figure.png',
                 'img/reviews/../../evil.svg', 'img/reviews/payload.js', 'okf/log.md'):
        assert not preview.permitted(path)


def test_preview_index_lists_each_built_post_and_keeps_single_post_redirect(tmp_path):
    posts = ['okf/_posts/2026/2026-11-01-first.md', 'okf/_posts/2026/2026-11-02-second.md']
    for target in (tmp_path / '2026/11/01/first', tmp_path / '2026/11/02/second'):
        target.mkdir(parents=True)
        (target / 'index.html').touch()

    entries = preview.index_pages(tmp_path, 42, 'same-head', posts)
    assert [entry['path'] for entry in entries] == posts
    assert all(entry['pr'] == 42 and entry['sha'] == 'same-head' for entry in entries)
    index = (tmp_path / 'index.html').read_text()
    assert 'noindex,nofollow' in index
    assert 'http-equiv="refresh"' not in index
    assert all(f'href="{entry["url"]}"' in index for entry in entries)

    preview.index_pages(tmp_path, 42, 'same-head', posts[:1])
    assert f'content="0;url={entries[0]["url"]}"' in (tmp_path / 'index.html').read_text()


def test_missing_batch_page_cannot_enter_manifest(tmp_path):
    with pytest.raises(RuntimeError, match='Expected review page missing'):
        preview.index_pages(tmp_path, 42, 'same-head', ['okf/_posts/2026/2026-11-01-missing.md'])
    assert not (tmp_path / 'index.html').exists()
