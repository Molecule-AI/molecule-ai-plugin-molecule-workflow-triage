#!/usr/bin/env python3
"""
Smoke tests for molecule-workflow-triage.

Rationale for limited test coverage: This is a command/skill-only plugin with no
executable hooks or business logic. The plugin's "logic" is prose documentation
in triage.md and triage-workflow/SKILL.md — not Python code that can be unit-tested.
The tests below verify that all required artifacts exist, parse correctly, and
document the expected structure. For more comprehensive coverage, end-to-end tests
should be written against the workspace runtime.

Run: python tests/test_triage_smoke.py
"""
import os
import re
import sys
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, '.molecule-ci', 'scripts'))


class TestPluginManifest(unittest.TestCase):
    """Verify plugin.yaml is well-formed."""

    @classmethod
    def setUpClass(cls):
        import yaml
        manifest_path = os.path.join(REPO_ROOT, 'plugin.yaml')
        with open(manifest_path) as f:
            cls.manifest = yaml.safe_load(f)

    def test_plugin_yaml_loads(self):
        self.assertIsInstance(self.manifest, dict)

    def test_name(self):
        self.assertEqual(self.manifest['name'], 'molecule-workflow-triage')

    def test_version_semver(self):
        v = self.manifest['version']
        self.assertRegex(v, r'^\d+\.\d+\.\d+$')

    def test_description_present(self):
        self.assertGreater(len(self.manifest.get('description', '')), 20)

    def test_runtime_claude_code(self):
        self.assertIn('claude_code', self.manifest.get('runtimes', []))

    def test_command_declared(self):
        self.assertIn('triage', self.manifest.get('commands', []))

    def test_tags(self):
        tags = self.manifest.get('tags', [])
        self.assertIn('molecule', tags)
        self.assertIn('guardrails', tags)


class TestTriageCommand(unittest.TestCase):
    """Verify /triage command file exists and documents required steps."""

    CMD_PATH = os.path.join(REPO_ROOT, 'commands', 'triage.md')

    def test_file_exists(self):
        self.assertTrue(os.path.isfile(self.CMD_PATH))

    def test_has_frontmatter(self):
        import yaml
        with open(self.CMD_PATH) as f:
            content = f.read()
        self.assertTrue(content.startswith('---'))
        parts = content.split('---', 2)
        self.assertEqual(len(parts), 3)
        _, frontmatter, _ = parts
        data = yaml.safe_load(frontmatter)
        self.assertIsInstance(data, dict)

    def test_frontmatter_name(self):
        import yaml
        with open(self.CMD_PATH) as f:
            content = f.read()
        parts = content.split('---', 2)
        _, frontmatter, body = parts
        data = yaml.safe_load(frontmatter)
        self.assertEqual(data['name'], 'triage')

    def test_body_has_steps(self):
        with open(self.CMD_PATH) as f:
            content = f.read()
        # Step 0 through Step 5 must be documented
        for step in ['Step 0', 'Step 1', 'Step 2', 'Step 3', 'Step 4', 'Step 5']:
            self.assertIn(step, content, f"Missing {step} in triage.md")

    def test_standing_rules_present(self):
        with open(self.CMD_PATH) as f:
            content = f.read()
        self.assertIn('Standing rules', content)

    def test_never_push_to_main(self):
        with open(self.CMD_PATH) as f:
            content = f.read()
        self.assertIn('Never push to main', content)

    def test_merge_commits_only(self):
        with open(self.CMD_PATH) as f:
            content = f.read()
        self.assertIn('Merge-commits only', content)


class TestTriageWorkflowSkill(unittest.TestCase):
    """Verify triage-workflow skill exists and is well-formed."""

    SKILL_PATH = os.path.join(REPO_ROOT, 'skills', 'triage-workflow', 'SKILL.md')

    def test_file_exists(self):
        self.assertTrue(os.path.isfile(self.SKILL_PATH))

    def test_has_frontmatter(self):
        import yaml
        with open(self.SKILL_PATH) as f:
            content = f.read()
        parts = content.split('---', 2)
        self.assertEqual(len(parts), 3)
        _, frontmatter, body = parts
        data = yaml.safe_load(frontmatter)
        self.assertIsInstance(data, dict)

    def test_frontmatter_name(self):
        import yaml
        with open(self.SKILL_PATH) as f:
            content = f.read()
        parts = content.split('---', 2)
        _, frontmatter, body = parts
        data = yaml.safe_load(frontmatter)
        self.assertEqual(data['name'], 'triage-workflow')

    def test_body_has_gates(self):
        with open(self.SKILL_PATH) as f:
            content = f.read()
        # The 7-gate verification must be documented as a numbered list
        self.assertIn('7 gates per PR', content)
        self.assertIn('CI status', content)
        self.assertIn('Playwright', content)

    def test_examples_section(self):
        with open(self.SKILL_PATH) as f:
            content = f.read()
        self.assertIn('Examples', content)


class TestAdapter(unittest.TestCase):
    """Verify Claude Code adapter exists."""

    ADAPTER_PATH = os.path.join(REPO_ROOT, 'adapters', 'claude_code.py')

    def test_file_exists(self):
        self.assertTrue(os.path.isfile(self.ADAPTER_PATH))

    def test_imports_agentskills_adaptor(self):
        with open(self.ADAPTER_PATH) as f:
            content = f.read()
        self.assertIn('AgentskillsAdaptor', content)


class TestKnownIssues(unittest.TestCase):
    """Verify known-issues.md structure."""

    KI_PATH = os.path.join(REPO_ROOT, 'known-issues.md')

    def test_file_exists(self):
        self.assertTrue(os.path.isfile(self.KI_PATH))

    def test_has_active_issues_section(self):
        with open(self.KI_PATH) as f:
            self.assertIn('Active Issues', f.read())

    def test_has_known_gotchas_section(self):
        with open(self.KI_PATH) as f:
            self.assertIn('Known Gotchas', f.read())

    def test_documents_sibling_plugin_dependency(self):
        """Critical gotcha: /triage requires sibling plugins."""
        with open(self.KI_PATH) as f:
            content = f.read()
        self.assertIn('sibling plugins', content)


class TestValidatePlugin(unittest.TestCase):
    """Smoke-test validate-plugin.py."""

    def test_exits_zero(self):
        import subprocess
        result = subprocess.run(
            [sys.executable, os.path.join(REPO_ROOT, '.molecule-ci', 'scripts', 'validate-plugin.py')],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
        )
        self.assertEqual(result.returncode, 0, f"stdout: {result.stdout}\nstderr: {result.stderr}")
        self.assertIn('molecule-workflow-triage', result.stdout)


if __name__ == '__main__':
    unittest.main(verbosity=2)
