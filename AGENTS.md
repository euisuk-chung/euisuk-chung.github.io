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

## OKF content rules

Posts and tag concepts follow Google Cloud's Open Knowledge Format (OKF) v0.2: markdown with YAML front matter, `type` required, cross-links as plain markdown links. The bundle root is `okf/` (`okf/_posts/<year>/`, `okf/_concepts/`, `okf/index.md`, `okf/log.md`). Posts go only in `okf/_posts/<year>/`; `okf/_concepts/` is the tag dictionary, one file per tag.

- Post front matter, in this key order: `type` (from `_scripts/okf_types.json`), `title`, `description` (one sentence), `date`, `tags`, `resource` (velog URL), `generated` (`by`: `process:velog-sync` or `human:<id>`, `at`: ISO-8601), `sources`, `status` (`draft` | `stable` | `deprecated`), `year`. Strings are double-quoted.
- New paper reviews use `type: Paper Review` and titles starting with `[Paper Review] `. Repository reviews use `type: Repo Review` and titles starting with `[Repo Review] `. Do not duplicate the title in the body.
- Tags must be the exact `title` of a concept file in the concepts directory. To use a new tag, add `<slug>.md` there first (`type: Tag`, `title`, `slug` == filename, `description`, `aliases`, optional `parent`/`related`). Never invent tag spellings in a post.
- Bodies use ATX headings (`##`), start with content (no duplicate `# {title}`), and never put a `---` rule directly above a heading (the theme draws its own divider). Do not hand-fix formatting across posts; run `uv run --project _scripts python _scripts/okf_migrate.py --paths <files> --check` to verify and `okf_migrate.py --paths <files>` to normalize. The migration must never change body text; `verify_no_loss` blocks writes that do.
- LLM-generated `description`/`tags` go through an `enrich.json` sidecar (`okf_migrate.py --enrich`), never by editing prose in the body. Descriptions do not summarize away or shorten the article; the body stays byte-identical apart from the normalizations above.
- Before pushing anything under the posts or concepts directories run `okf_lint.py --allow-draft --check-index` and, after adding posts, `okf_index.py --write`. CI (`.github/workflows/okf-lint.yml`) runs the same checks.
- Migration batches are content PRs (one per year or ~50 posts, branch `codex/okf-migrate-<batch>`), reviewed by a human. The PR body lists per post: title, generated `description`, `tags`, `type`, resource source; then migration counts from `--report`; validation commands in a collapsed section. Tooling changes (`_scripts/**`, workflows, docs) are code PRs and may be integrated by the agent after validation.
- Tag policy: `ChatGPT` only when the ChatGPT app/product is the subject; posts about OpenAI models, the API, CLIs or Cookbook guides carry `OpenAI` only. Tag both the child and its parent concept (e.g. `Gemini` + `Google`, `CES` + `Conference`); the archive filter reads explicit tags. Translations or summaries of vendor prompting guides are `type: Guide`, not `Product Update`.
- Concept files: the body is the `description` sentence, followed by `상위 개념: [Title](slug.md)` when `parent` is set; give a new concept `parent`/`related` when an obvious one exists, and back-apply it to existing posts on that topic (grep titles and bodies) in the same PR.
- Duplicate posts (the crawler occasionally saves the same velog article twice): keep the copy that has `resource`, delete the other, and add `redirect_from` with the deleted post's pretty URL to the kept post (`jekyll-redirect-from` is enabled). Rows in `processed_posts.csv` reference the kept file only.


## Review math and previews

- Review source Markdown uses GitHub `math` fenced blocks for display math and dollar–backtick delimiters (`$` + backtick + TeX + backtick + `$`) inline. Bare `$...$`/`$$` remain supported by the build for legacy input, but GitHub can consume TeX escapes in those forms. Keep LaTeX commands and subscripts verbatim; do not escape `_` used for subscripts or add `markdown="0"` wrappers to source posts. GitHub rejects `\operatorname`; use equivalent upright function labels such as `\mathrm{Concat}` or `\mathrm{sg}` after checking the original meaning. Literal underscores such as `\text{file\_name}` stay escaped.
- `_plugins/review_math.rb` protects review math during Jekyll builds only, preserving code examples and existing legacy wrappers. Test with `bundle exec ruby _scripts/test_review_math.rb` and inspect actual MathJax output. Standard review Markdown requires the custom Pages workflow; safe-mode legacy builds do not load this plugin.
- `.github/workflows/pages.yml` builds published content from `master` and isolated previews at `/pr-preview/<PR number>/`. Preview builds load code/config only from `master` and allowlisted content/assets from same-repository review PRs. Never execute scripts, plugins, or workflows from PR heads for preview deployment.
- Link the rendered preview at the top of content PR descriptions after its manifest SHA matches the current PR head. Keep the GitHub Markdown link for source review. Previews are labeled drafts and noindexed; content PRs still require human merging.
