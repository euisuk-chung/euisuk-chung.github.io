# Commit and Pull Request Convention

Semantic commit messages: `label(scope): description`.

Allowed labels: `fix`, `feat`, `chore`, `docs`, `test`, `devops`.

- Never add `Co-Authored-By` trailers or any agent/tool attribution to commit messages.
- The default branch is `master`. Start changes from the latest `origin/master` after fetching.
- Content changes (paper reviews, repository reviews, other blog posts, their images and source metadata) require a GitHub PR and human review before merging. Never auto-merge content PRs. Treat mixed code/content changes as content, or split them into separate changes.
- Code, build, automation, configuration and workflow-documentation changes without editorial content may be committed and integrated into `master` by the agent after appropriate validation; no human PR review is required. Use a working branch, verify the exact diff, and integrate by a normal fast-forward push or a validated PR merge. Never force-push or bypass required checks. This permission does not authorize unsolicited changes.
- For issue fixes, use `fix-<issue-number>`. For paper reviews, use `codex/paper-<id>`. For repository reviews, use `codex/repo-<owner>-<repo>`. Use `codex/` for other work branches.
- Commit callers and callees together. Do not hide cross-module references inside function-local imports to defer missing-symbol failures until a production request. Validate affected imports and execution paths as appropriate.
- Stage only explicit changed files. Never stage local skills, agent definitions, automation tools, credentials, source caches, or temporary repository clones.
- PR titles follow the same semantic format as commits. For content PRs, lead with a short Korean introduction to the paper/repository, 3–5 concrete learning points, key findings with evaluation context, and 2–3 study questions grounded in the article. Link to the full draft and preserve source IDs/revisions. Put actual validation details in a collapsed section at the bottom. Study questions are PR review aids, not invented author claims or new article limitations. For code-only PRs, describe the change and validation. Include issue references only when applicable.

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

The PR description should contain a concise summary, validation results, and `Refs: #123`. For a code-only issue fix, the agent may merge after validation. Content PRs must stop at the review link for human approval.
