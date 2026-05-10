# molecule-workflow-triage

Provides the `/triage` slash command — a full PR-triage cycle that chains together code-review, cross-vendor-review, llm-judge, cron-learnings, and update-docs into one coordinated workflow.

## How it works

`/triage` orchestrates:

1. **Gate 1 — Code Review** (`molecule-skill-code-review`) — static analysis + style
2. **Gate 2 — Cross-Vendor Review** (`molecule-skill-cross-vendor-review`) — multi-model consistency check
3. **Gate 3 — LLM Judge** (`molecule-skill-llm-judge`) — quality vs. golden examples
4. **Gate 4 — Security** (`molecule-ai-plugin-molecule-security-scan`) — CVE scan on skill deps
5. **Write learnings** — results fed to `molecule-skill-cron-learnings`

Issue assignments cap at 2 per run to keep workload bounded.

## Install

### In org template (org.yaml)

```yaml
plugins:
  - molecule-workflow-triage
```

**Recommended sibling plugins:**
- `molecule-skill-code-review`
- `molecule-skill-cron-learnings`
- `molecule-skill-cross-vendor-review`
- `molecule-skill-llm-judge`
- `molecule-ai-plugin-molecule-security-scan`

### From URL (community install)

```
github://Molecule-AI/molecule-ai-plugin-molecule-workflow-triage
```

## Usage

```
/triage
```

## Known gotchas

- `/triage` requires sibling plugins to be useful. If not installed, the step degrades gracefully.
- Gate 4 (security) may conflict with `careful-mode` REFUSE list — both block, which is intentional.
- Mechanical fix commits do not trigger re-review.

See [known-issues.md](known-issues.md) for full detail.

## Runtime

- `claude_code` — primary

## License

Business Source License 1.1 — © Molecule AI.
