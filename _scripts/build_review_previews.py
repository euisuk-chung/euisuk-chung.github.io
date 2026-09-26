"""Build review previews with trusted base code and only PR content/assets.

Run from the trusted deployment checkout, never from a PR checkout. No PR scripts,
Gemfile, config, plugins or workflows are loaded or executed.
"""
import argparse
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile
import html

REPO = 'euisuk-chung/euisuk-chung.github.io'
POST = re.compile(r'okf/_posts/(\d{4})/(\d{4})-(\d{2})-(\d{2})-(.+)\.md')


def run(*args, **kwargs):
    return subprocess.check_output(args, **kwargs)


def permitted(path):
    return bool(POST.fullmatch(path) or re.fullmatch(r'okf/_concepts/[a-z0-9-]+\.md', path)
                or re.fullmatch(r'img/reviews/[a-zA-Z0-9_./-]+\.(?:png|jpg|jpeg|webp|svg)', path)) and '..' not in Path(path).parts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--destination', default='_site')
    parser.add_argument('--numbers', nargs='*', type=int)
    args = parser.parse_args()
    destination = Path(args.destination).resolve()
    base = Path.cwd()
    prs = json.loads(run('gh', 'pr', 'list', '--repo', REPO, '--state', 'open', '--limit', '100',
                        '--json', 'number,headRefName,headRefOid,isCrossRepository'))
    manifest = []
    archive = run('git', 'archive', 'HEAD')
    for pr in prs:
        number, branch, sha = pr['number'], pr['headRefName'], pr['headRefOid']
        if pr['isCrossRepository'] or not re.fullmatch(r'codex/(?:paper|repo)-[a-z0-9.-]+', branch):
            continue
        if args.numbers is not None and number not in args.numbers:
            continue
        run('git', 'fetch', 'origin', f'pull/{number}/head')
        if run('git', 'rev-parse', 'FETCH_HEAD').decode().strip() != sha:
            raise RuntimeError(f'PR {number} changed during collection; rerun against fresh heads')
        paths = run('git', 'diff', '--name-only', '--diff-filter=AM', '--no-renames', f'HEAD...{sha}').decode().splitlines()
        posts = [p for p in paths if POST.fullmatch(p)]
        if len(posts) != 1:
            print(f'Skip PR {number}: expected one review post')
            continue
        with tempfile.TemporaryDirectory(prefix='review-preview-') as tmp:
            source = Path(tmp) / 'source'
            source.mkdir()
            with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
                tar.extractall(source, filter='data')
            shutil.rmtree(source / 'okf/_posts')
            for path in filter(permitted, paths):
                mode = run('git', 'ls-tree', sha, '--', path).decode().split()[0]
                if mode != '100644':
                    raise ValueError(f'Non-regular preview content rejected: {path}')
                target = source / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(run('git', 'show', f'{sha}:{path}'))
            config = Path(tmp) / 'preview.yml'
            config.write_text(f'review_preview: true\nreview_pr: {number}\nreview_sha: "{sha}"\nservice-worker: false\n')
            output = destination / 'pr-preview' / str(number)
            subprocess.run(['bundle', 'exec', 'jekyll', 'build', '--source', str(source),
                            '--destination', str(output), '--baseurl', f'/pr-preview/{number}',
                            '--config', f'{source / "_config.yml"},{config}'], cwd=base, check=True)
            match = POST.fullmatch(posts[0])
            _, year, month, day, slug = match.groups()
            url = f'/pr-preview/{number}/{year}/{month}/{day}/{slug}/'
            if not (output / year / month / day / slug / 'index.html').is_file():
                raise RuntimeError(f'Expected review page missing: {url}')
            (output / 'index.html').write_text('<!doctype html><html lang="ko"><head><meta charset="utf-8">'
                '<meta name="robots" content="noindex,nofollow"><meta http-equiv="refresh" content="0;url='
                + html.escape(url, quote=True) + '"></head><body><a href="' + html.escape(url, quote=True)
                + '">리뷰 미리보기</a></body></html>')
            manifest.append({'pr': number, 'sha': sha, 'path': posts[0], 'url': url})
    (destination / 'pr-preview').mkdir(parents=True, exist_ok=True)
    (destination / 'pr-preview/manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
