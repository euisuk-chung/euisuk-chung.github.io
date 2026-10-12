from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def workflow(name):
    # BaseLoader preserves GitHub's "on" key rather than YAML 1.1 boolean True.
    return yaml.load((ROOT / '.github/workflows' / name).read_text(), Loader=yaml.BaseLoader)


def test_skipped_metadata_completion_cannot_evict_pending_merge_deploy():
    pages = workflow('pages.yml')
    assert pages['jobs']['build']['if'] == (
        "github.event_name != 'workflow_run' || github.event.workflow_run.conclusion == 'success'"
    )
    # Regression: push/PR-close deploys were evicted by a cancelled metadata
    # completion whose build was then skipped. Non-success completions must
    # use a unique group outside the real deployment queue.
    assert pages['concurrency']['group'] == (
        "${{ github.event_name == 'workflow_run' && "
        "github.event.workflow_run.conclusion != 'success' && "
        "format('github-pages-ignored-{0}', github.run_id) || 'github-pages' }}"
    )
    assert pages['concurrency']['cancel-in-progress'] == 'false'


def test_pr_metadata_success_redeploys_only_trusted_master():
    pages = workflow('pages.yml')
    trigger = pages['on']['workflow_run']
    assert trigger['workflows'] == ['OKF Metadata']
    assert trigger['types'] == ['completed']
    assert 'branches' not in trigger
    # Metadata PR-close runs are attributed to the PR branch, but both
    # workflows must read code from master and never from workflow_run heads.
    for name, job in [('pages.yml', 'build'), ('okf-metadata.yml', 'sync')]:
        steps = workflow(name)['jobs'][job]['steps']
        checkouts = [step for step in steps if step.get('uses', '').startswith('actions/checkout@')]
        assert len(checkouts) == 1
        assert checkouts[0]['with']['ref'] == 'master'
    assert pages['jobs']['build']['steps'][0]['with']['persist-credentials'] == 'false'
    assert pages['permissions']['contents'] == 'read'
