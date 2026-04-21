---
name: triage-workflow
description: Orchestrates a full PR-triage cycle — 7-gate verification, code review, merge, docs sync, issue pickup.
---

# triage-workflow

On-demand manual invocation of the PR-triage flow. Equivalent to one cron tick.

## When to Use
- Clear PR backlog faster than the hourly cron cadence
- Test a change to the triage prompt itself
- A scheduled cron has died and the queue is backing up

## How It Works

### Activate guards + replay learnings
1. `Skill careful-mode` — load REFUSE/WARN/ALLOW lists
2. Read last 20 lines of cron-learnings JSONL (workspace memory dir)

### PR verification (7 gates per PR)
1. CI status
2. Build
3. Tests
4. Security
5. Design review
6. Line review
7. Playwright (UI PRs only)

Supplements: `Skill code-review`, `Skill cross-vendor-review` on noteworthy PRs.

### Mechanical fixes only
Fix on-branch, commit `fix(gate-N): ...`, push, poll CI. Never fix logic/design/auth issues on a branch that isn't yours.

### Merge conditions
All gates green + 0 🔴 from code-review + cross-vendor agreement → merge-commit only.

### Docs sync after merge
`Skill update-docs` — measure test counts, don't guess.

### Issue pickup (cap 2)
- Gates I-1..I-6
- Self-assign, branch, implement, draft PR
- Run `Skill llm-judge` against issue body + PR diff
- Mark ready only if score >= 4

## Examples
```
Skill triage-workflow
```
