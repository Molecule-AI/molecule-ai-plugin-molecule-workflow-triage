# Test Coverage Rationale — molecule-workflow-triage

## Why This Plugin Has Limited Unit-Test Coverage

`molecule-workflow-triage` is a **command/skill-only plugin**. Its "logic" is prose
documentation in `commands/triage.md` and `skills/triage-workflow/SKILL.md` — a
structured workflow definition, not executable Python code.

There are no hooks, no Python functions, and no adapters with testable business logic.
The closest thing to "code" is the YAML frontmatter in markdown files and the
AgentskillsAdaptor import in `adapters/claude_code.py`.

## What We Test (and Why)

| What | Why |
|------|-----|
| `plugin.yaml` schema | Verifies manifest is well-formed; catches typos in command/skill names |
| `commands/triage.md` frontmatter + required sections | Ensures the /triage command is registered and documented |
| `skills/triage-workflow/SKILL.md` frontmatter + gates | Ensures the triage-workflow skill is registered |
| `adapters/claude_code.py` import | Verifies the Claude Code adapter is wired up |
| `known-issues.md` structure | Documents known gotchas for future maintainers |
| `validate-plugin.py` exit 0 | Smoke test — the shared CI validator passes |

## What We Cannot Unit-Test (and What Would Help)

- **End-to-end workflow execution** — requires a running Claude Code workspace
  with GitHub credentials and sibling plugins installed. Write an integration test
  in the workspace-template test suite instead.

- **Command argument parsing** — there are no CLI args in this plugin; `/triage`
  takes no parameters. If a future version adds arguments, add arg-parsing tests.

- **GH CLI integration** — `gh pr list`, `gh pr merge`, etc. are invoked by the
  agent at runtime. Mock them in integration tests.

## If You Add Business Logic

If you add Python hooks or adapters to this plugin, add:
1. Unit tests for any new functions (standard `unittest` / `pytest`)
2. Mock tests for external API calls (`gh`, GitHub API)
3. Integration tests for the full workflow in `workspace-template/`

See `molecule-freeze-scope` or `molecule-careful-bash` for examples of
full test suites in plugin repos.
