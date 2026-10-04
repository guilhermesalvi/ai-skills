"""Exercise package isolation, trace grading and portable evaluation fixtures."""

import importlib.util
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validator = load("validate_repo")
evals = load("run_evals")


class PackageValidation(unittest.TestCase):
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
        with patch.object(validator.shutil, "which", return_value="codex"), \
                patch.object(validator.subprocess, "run") as run:
            observed = []

            def execute(command, **kwargs):
                home = Path(kwargs["env"]["CODEX_HOME"])
                observed.append(home)
                if command[1:3] == ["plugin", "add"]:
                    source = ROOT / "plugins/ai-skills/skills/sdd"
                    target = home / "plugins/cache/ai-skills/ai-skills/7.0.0/skills/sdd"
                    validator.shutil.copytree(source, target, ignore=validator.shutil.ignore_patterns("__pycache__"))
                return SimpleNamespace(returncode=0,
                                       stdout='{"installed": [{"pluginId": "ai-skills@ai-skills", "enabled": true}]}',
                                       stderr="")

            run.side_effect = execute
            previous = validator.os.environ.get("CODEX_HOME")
            validator.install_smoke()
            self.assertEqual(previous, validator.os.environ.get("CODEX_HOME"))
            self.assertEqual(1, len(set(observed)))
            self.assertFalse(observed[0].exists())


class TraceGrading(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name)

    def command(self, text, exit_code=0, event="item.completed"):
        return {"type": event, "item": {"type": "command_execution", "command": text, "exit_code": exit_code}}

    def test_negative_artifact_check_does_not_pass_for_missing_file(self):
        check = {"type": "regex", "target": {"path": "plan.md"}, "pattern": r"- \[ \]", "match": "not_contains"}
        self.assertFalse(evals.evaluate(check, self.workspace, [], ""))

    def test_uncompleted_or_failed_test_command_is_not_evidence(self):
        check = {"type": "command", "pattern": "unittest", "exit_code": 0}
        for event in (self.command("python -m unittest", 1), self.command("python -m unittest", event="item.started")):
            self.assertFalse(evals.evaluate(check, self.workspace, [event], ""))
        self.assertTrue(evals.evaluate(check, self.workspace, [self.command("python -m unittest")], ""))

    def test_skill_read_recognizes_windows_and_posix_paths(self):
        check = {"type": "skill_read", "skill": "sdd", "expected": True}
        for command in ("cat /cache/skills/sdd/SKILL.md", r"Get-Content 'C:\cache\skills\sdd\SKILL.md'"):
            self.assertTrue(evals.evaluate(check, self.workspace, [self.command(command)], ""))
        self.assertFalse(evals.evaluate(check, self.workspace, [self.command("echo sdd/SKILL.md")], ""))
        self.assertFalse(evals.evaluate(check, self.workspace, [self.command("cat sdd/SKILL.md", 1)], ""))

    def test_qualitative_checks_stay_pending(self):
        self.assertIsNone(evals.evaluate({"type": "rubric"}, self.workspace, [], ""))

    def test_eval_environment_does_not_reuse_desktop_chat_identity(self):
        with patch.dict(evals.os.environ, {"CODEX_APP_TOOLS_PIPE_PATH": "parent-pipe", "CODEX_THREAD_ID": "parent-thread"}):
            env = evals.isolated_environment(self.workspace)
            self.assertNotIn("CODEX_APP_TOOLS_PIPE_PATH", env)
            self.assertNotIn("CODEX_THREAD_ID", env)
            self.assertEqual(str(self.workspace), env["CODEX_HOME"])
            self.assertEqual("parent-thread", evals.os.environ["CODEX_THREAD_ID"])

    def test_blocked_fixture_access_is_an_execution_error(self):
        with patch.object(evals.subprocess, "run") as run:
            def execute(command, **kwargs):
                kwargs["stdout"].write('{"type":"turn.completed","usage":{}}\n')
                kwargs["stderr"].write('exec_command failed: blocked by policy\n')
                (self.workspace / "answer.md").write_text("Unable to read fixture", encoding="utf-8")
                return SimpleNamespace(returncode=0)
            run.side_effect = execute
            with self.assertRaisesRegex(ValueError, "environment policy"):
                evals.run_codex("codex", {}, self.workspace, "Write ADR", self.workspace, "workspace-write", 30)

    def test_file_checks_do_not_count_git_internals(self):
        (self.workspace / ".git").mkdir()
        (self.workspace / ".git/spec.md").write_text("", encoding="utf-8")
        check = {"type": "regex", "target": "files", "pattern": "spec.md"}
        self.assertFalse(evals.evaluate(check, self.workspace, [], ""))

    def test_case_uses_scoped_permission_profiles_and_prompt_on_stdin(self):
        for sandbox, profile in (("workspace-write", ":workspace"), ("read-only", ":read-only")):
            with patch.object(evals.subprocess, "run") as run:
                def execute(command, **kwargs):
                    kwargs["stdout"].write('{"type":"turn.completed","usage":{}}\n')
                    (self.workspace / "answer.md").write_text("Done", encoding="utf-8")
                    return SimpleNamespace(returncode=0)
                run.side_effect = execute
                evals.run_codex("codex", {}, self.workspace, "$sdd", self.workspace, sandbox, 30)
                command = run.call_args.args[0]
                self.assertIn(f'default_permissions="{profile}"', command)
                self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", command)
                self.assertEqual("-", command[-1])
                self.assertEqual("$sdd", run.call_args.kwargs["input"])


class PortableFixtures(unittest.TestCase):
    def test_resume_fixture_exposes_the_local_contract_regression(self):
        with TemporaryDirectory() as temporary:
            workspace = Path(temporary) / "workspace"
            evals.seed(evals.cases()["resume-contract-conflict"], workspace)
            result = subprocess.run([evals.sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-v"],
                                    cwd=workspace, capture_output=True, text=True)
            self.assertEqual(1, result.returncode)
            self.assertIn("test_zero_is_accepted", result.stderr)
            self.assertIn("Ran 3 tests", result.stderr)
            base = subprocess.run(["git", "show", "HEAD:units/validation.py"], cwd=workspace,
                                  check=True, capture_output=True, text=True)
            (workspace / "units/validation.py").write_text(base.stdout, encoding="utf-8")
            fixed = subprocess.run([evals.sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-q"],
                                   cwd=workspace, capture_output=True, text=True)
            self.assertEqual(0, fixed.returncode, fixed.stderr)

    def test_order_fixtures_have_passing_baseline_and_committed_source(self):
        for name in ("cancel-orders-spec", "implement-and-verify"):
            with self.subTest(name=name), TemporaryDirectory() as temporary:
                workspace = Path(temporary) / "workspace"
                evals.seed(evals.cases()[name], workspace)
                result = subprocess.run([evals.sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-q"],
                                        cwd=workspace, capture_output=True, text=True)
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertIn("Ran 2 tests", result.stderr)
                status = subprocess.run(["git", "status", "--porcelain"], cwd=workspace, capture_output=True, text=True)
                self.assertEqual("", status.stdout)

    def test_adr_fixture_keeps_two_distinct_historical_decisions(self):
        with TemporaryDirectory() as temporary:
            workspace = Path(temporary) / "workspace"
            evals.seed(evals.cases()["adr-from-code"], workspace)
            first = subprocess.run(["git", "show", "HEAD~1:billing/invoices.py"], cwd=workspace, capture_output=True, text=True)
            self.assertIn("datetime.now()", first.stdout)
            self.assertIn("clock.now()", (workspace / "billing/invoices.py").read_text(encoding="utf-8"))
            self.assertFalse((workspace / "docs").exists())

    def test_scaffolds_refuse_nonempty_workspaces(self):
        with TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            (workspace / "keep.txt").write_text("existing content", encoding="utf-8")
            with self.assertRaises(ValueError):
                evals.seed(evals.cases()["cancel-orders-spec"], workspace)
            self.assertEqual("existing content", (workspace / "keep.txt").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
