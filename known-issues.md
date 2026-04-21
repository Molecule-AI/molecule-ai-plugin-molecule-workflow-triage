# Known Issues

Active and recently resolved issues for `molecule-workflow-triage`.

---

## Active Issues

*(None currently open. File an issue if you encounter a problem.)*

---

## Known Gotchas

### `/triage` requires several sibling plugins to be useful

**Severity:** Medium
**Detail:** `/triage` calls `code-review`, `cross-vendor-review`, `llm-judge`, `cron-learnings`, and `update-docs` as sub-steps. If those plugins are not installed, the triage will fail or degrade gracefully depending on the skill.

**Workaround:** Install all recommended plugins (see CLAUDE.md) before enabling `/triage` in a workspace.

---

### Gate 4 (security) may conflict with careful-mode REFUSE list

**Severity:** Low
**Detail:** If a PR touches code that is on the `careful-mode` REFUSE list, Gate 4 (security) will flag it AND careful-mode will refuse to operate on the file. This is intentional but can be confusing — both are blocking.

---

### Issue pickup cap of 2 may leave backlog

**Severity:** Informational
**Detail:** If many issues are backlogged, `/triage` will only self-assign and begin work on 2 per run. Use multiple `/triage` invocations or increase the cap in a custom workspace configuration.

---

### Mechanical fix commits do not trigger re-review

**Severity:** Low
**Detail:** Gate fix commits (`fix(gate-N): ...`) are pushed to the PR branch and CI is re-polled, but no review request is re-sent. If a reviewer has already approved, the existing approval stands. If a reviewer has not yet reviewed, they may miss the fix.

**Workaround:** After a mechanical fix, manually post a review comment to re-engage reviewers if needed.

---

## Recently Resolved

*(None yet.)*
