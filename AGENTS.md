# Commit and Pull Request Convention

Semantic commit messages: `label(scope): description`.

Allowed labels: `fix`, `feat`, `chore`, `docs`, `test`, `devops`.

- Never add `Co-Authored-By` trailers or any agent/tool attribution to commit messages.
- Create branches from the latest `origin/master` after fetching. Never push directly to `master`, merge into it, or enable automatic PR merging. Commit and push only to a working branch, open a GitHub pull request targeting `master`, and deliver the PR link. A human performs the merge.
- For issue fixes, use `fix-<issue-number>`. For paper reviews, use `codex/paper-<id>`. For repository reviews, use `codex/repo-<owner>-<repo>`. Use `codex/` for other work branches.
- Commit callers and callees together. Do not hide cross-module references inside function-local imports to defer missing-symbol failures until a production request. Validate affected imports and execution paths as appropriate.
- Stage only explicit changed files. Never stage local skills, agent definitions, automation tools, credentials, source caches, or temporary repository clones.
- PR titles follow the same semantic format as commits. Describe the change and validation; include issue or ticket references when applicable. Do not invent an issue reference.

## Example: issue fix to PR

```bash
git fetch origin master
git switch -c fix-123 origin/master
# Make and validate the change.
git add path/to/caller.py path/to/callee.py
git commit -m 'fix(reports): include report builder with its caller' -m 'Refs: #123'
git push -u origin fix-123
gh pr create --base master --head fix-123 \
  --title 'fix(reports): include report builder with its caller' \
  --body-file /absolute/path/to/pr-description.md
```

The PR description should contain a concise summary, validation results, and `Refs: #123`. Stop after delivering the PR link; do not merge it.
