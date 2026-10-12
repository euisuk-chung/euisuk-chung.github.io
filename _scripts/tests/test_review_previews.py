import importlib.util
from pathlib import Path

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
