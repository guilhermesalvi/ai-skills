"""Exercise package validation, isolated installation and portable evaluation fixtures."""

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "plugins/ai-skills/evals"
# This fixture ships a local regression on purpose; the eval asks the agent to fix it.
FAILING_FIXTURES = {"resume-contract-conflict"}


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validator = load("validate_repo")


def seed(name, workspace):
    """Run the same scaffold that seed.sh runs inside claude plugin eval."""
    workspace.mkdir(parents=True, exist_ok=True)
    subprocess.run([sys.executable, "-B", str(EVALS / name / "scaffold.py"), str(workspace)],
                   check=True, capture_output=True, text=True)


def run_tests(workspace, verbosity="-q"):
    return subprocess.run([sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", verbosity],
                          cwd=workspace, capture_output=True, text=True)


class PackageValidation(unittest.TestCase):
    def test_release_and_prerelease_versions_are_accepted(self):
        for value in ("1.0.0", "0.1.0-beta.1", "0.1.0-beta.2", "0.0.0", "1.0.0-0", "1.0.0-beta.1+build.01"):
            with self.subTest(version=value):
                self.assertTrue(validator.valid_version(value))

    def test_malformed_semantic_versions_are_rejected(self):
        for value in (None, 1, "", "0", "0.1", "v0.1.0", "01.0.0", "1.0.0-beta.01", "1.0.0-", "1.0.0+", "1.0.0 beta"):
            with self.subTest(version=value):
                self.assertFalse(validator.valid_version(value))

    def test_repository_resources_resolve(self):
        result = validator.validate()
        self.assertEqual(["ai-skills"], result["plugins"])
        self.assertEqual(1, len(result["skills"]))

    def test_package_paths_reject_escape_and_absolute_input(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            for value in ("../outside", "./../outside", "./part/../../outside", str(root)):
                with self.subTest(value=value), self.assertRaises(ValueError):
                    validator.local_path(root, value)

    def test_missing_resources_fail(self):
        with TemporaryDirectory() as temporary, self.assertRaisesRegex(ValueError, "does not exist"):
            validator.local_path(Path(temporary), "./missing")

    def test_duplicate_skill_identity_is_rejected(self):
        with TemporaryDirectory() as temporary:
            path = Path(temporary) / "sdd/SKILL.md"
            path.parent.mkdir()
            path.write_text("---\nname: sdd\nname: sdd\ndescription: Evaluate specs\n---\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate"):
                validator.frontmatter(path)

    def test_install_uses_temporary_config_and_preserves_caller_environment(self):
        version = json.loads((ROOT / "plugins/ai-skills/.claude-plugin/plugin.json").read_text(encoding="utf-8"))["version"]
        observed = []

        def execute(command, **kwargs):
            config = Path(kwargs["env"]["CLAUDE_CONFIG_DIR"])
            observed.append((config, Path(kwargs["cwd"])))
            install = config / "plugins/cache/ai-skills/ai-skills" / version
            if command[1:3] == ["plugin", "install"]:
                validator.shutil.copytree(ROOT / "plugins/ai-skills/skills/sdd", install / "skills/sdd",
                                          ignore=validator.shutil.ignore_patterns("__pycache__"))
            listing = [{"id": "ai-skills@ai-skills", "version": version, "enabled": True, "installPath": str(install)}]
            return SimpleNamespace(returncode=0, stdout=json.dumps(listing), stderr="")

        with patch.object(validator.shutil, "which", return_value="claude"), \
                patch.object(validator.subprocess, "run", side_effect=execute):
            previous = validator.os.environ.get("CLAUDE_CONFIG_DIR")
            validator.install_smoke()
            self.assertEqual(previous, validator.os.environ.get("CLAUDE_CONFIG_DIR"))
        self.assertEqual(1, len(set(observed)))
        config, cwd = observed[0]
        self.assertNotEqual(ROOT, cwd)
        self.assertFalse(config.exists())

    def test_install_rejects_a_stale_cached_version(self):
        def execute(command, **kwargs):
            listing = [{"id": "ai-skills@ai-skills", "version": "0.0.1", "enabled": True, "installPath": "unused"}]
            return SimpleNamespace(returncode=0, stdout=json.dumps(listing), stderr="")

        with patch.object(validator.shutil, "which", return_value="claude"), \
                patch.object(validator.subprocess, "run", side_effect=execute), \
                self.assertRaisesRegex(ValueError, "differs from manifest"):
            validator.install_smoke()


class PortableFixtures(unittest.TestCase):
    def test_fixtures_seed_committed_sources_with_expected_test_results(self):
        for scaffold in sorted(EVALS.glob("*/scaffold.py")):
            name = scaffold.parent.name
            with self.subTest(name=name), TemporaryDirectory() as temporary:
                workspace = Path(temporary) / "workspace"
                seed(name, workspace)
                self.assertTrue((workspace / ".git").is_dir())
                if (workspace / "tests").exists():
                    result = run_tests(workspace)
                    self.assertEqual(1 if name in FAILING_FIXTURES else 0, result.returncode, result.stderr)

    def test_resume_fixture_exposes_the_local_contract_regression(self):
        with TemporaryDirectory() as temporary:
            workspace = Path(temporary) / "workspace"
            seed("resume-contract-conflict", workspace)
            result = run_tests(workspace, "-v")
            self.assertEqual(1, result.returncode)
            self.assertIn("test_zero_is_accepted", result.stderr)
            self.assertIn("Ran 3 tests", result.stderr)
            base = subprocess.run(["git", "show", "HEAD:units/validation.py"], cwd=workspace,
                                  check=True, capture_output=True, text=True)
            (workspace / "units/validation.py").write_text(base.stdout, encoding="utf-8")
            fixed = run_tests(workspace)
            self.assertEqual(0, fixed.returncode, fixed.stderr)

    def test_order_fixtures_have_passing_baseline_and_committed_source(self):
        for name in ("cancel-orders-spec", "implement-and-verify"):
            with self.subTest(name=name), TemporaryDirectory() as temporary:
                workspace = Path(temporary) / "workspace"
                seed(name, workspace)
                result = run_tests(workspace)
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertIn("Ran 2 tests", result.stderr)
                status = subprocess.run(["git", "status", "--porcelain"], cwd=workspace, capture_output=True, text=True)
                self.assertEqual("", status.stdout)

    def test_adr_fixture_keeps_two_distinct_historical_decisions(self):
        with TemporaryDirectory() as temporary:
            workspace = Path(temporary) / "workspace"
            seed("adr-from-code", workspace)
            first = subprocess.run(["git", "show", "HEAD~1:billing/invoices.py"], cwd=workspace, capture_output=True, text=True)
            self.assertIn("datetime.now()", first.stdout)
            self.assertIn("clock.now()", (workspace / "billing/invoices.py").read_text(encoding="utf-8"))
            self.assertFalse((workspace / "docs").exists())

    def test_scaffolds_refuse_nonempty_workspaces(self):
        with TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            (workspace / "keep.txt").write_text("existing content", encoding="utf-8")
            with self.assertRaises(subprocess.CalledProcessError):
                seed("cancel-orders-spec", workspace)
            self.assertEqual("existing content", (workspace / "keep.txt").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
