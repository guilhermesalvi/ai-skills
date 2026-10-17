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
evals = load("run_evals")


def seed(name, workspace):
    """Run the portable scaffold used by the evaluation runner."""
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
        version = json.loads((ROOT / "plugins/ai-skills/plugin.json").read_text(encoding="utf-8"))["version"]
        observed = []

        def execute(command, **kwargs):
            config = Path(kwargs["env"]["CODEX_HOME"])
            observed.append((config, Path(kwargs["cwd"])))
            install = config / "plugins/cache/ai-skills/ai-skills" / version
            if command[1:3] == ["plugin", "add"]:
                validator.shutil.copytree(ROOT / "plugins/ai-skills", install,
                                          ignore=validator.shutil.ignore_patterns("__pycache__"))
            listing = {"installed": [{"pluginId": "ai-skills@ai-skills", "version": version, "enabled": True, "installPath": str(install)}]}
            return SimpleNamespace(returncode=0, stdout=json.dumps(listing), stderr="")

        with patch.object(validator.shutil, "which", return_value="codex"), \
                patch.object(validator.subprocess, "run", side_effect=execute):
            previous = validator.os.environ.get("CODEX_HOME")
            validator.install_smoke()
            self.assertEqual(previous, validator.os.environ.get("CODEX_HOME"))
        self.assertEqual(1, len(set(observed)))
        config, cwd = observed[0]
        self.assertNotEqual(ROOT, cwd)
        self.assertFalse(config.exists())

    def test_install_rejects_a_stale_cached_version(self):
        def execute(command, **kwargs):
            listing = {"installed": [{"pluginId": "ai-skills@ai-skills", "version": "0.0.1", "enabled": True, "installPath": "unused"}]}
            return SimpleNamespace(returncode=0, stdout=json.dumps(listing), stderr="")

        with patch.object(validator.shutil, "which", return_value="codex"), \
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
            event = self.command(command)
            event["item"]["aggregated_output"] = "---\nname: sdd\ndescription: Specify changes\n---\n"
            self.assertTrue(evals.evaluate(check, self.workspace, [event], ""))
        self.assertFalse(evals.evaluate(check, self.workspace, [self.command("echo sdd/SKILL.md")], ""))
        self.assertFalse(evals.evaluate(check, self.workspace, [self.command("cat sdd/SKILL.md", 1)], ""))

    def test_successful_pipeline_does_not_prove_a_failed_skill_read(self):
        check = {"type": "skill_read", "skill": "sdd", "expected": True}
        event = self.command("Get-Content 'sdd/SKILL.md'; Get-Location")
        event["item"]["aggregated_output"] = "Get-Content: Access denied\nPath\n----\nC:/workspace\n"
        self.assertFalse(evals.evaluate(check, self.workspace, [event], ""))

    def test_later_search_failure_does_not_hide_a_successful_skill_read(self):
        check = {"type": "skill_read", "skill": "sdd", "expected": True}
        event = self.command("Get-Content 'sdd/SKILL.md'; rg --files -g AGENTS.md", 1)
        event["item"]["aggregated_output"] = "---\nname: sdd\ndescription: Specify features\n---\n"
        self.assertTrue(evals.evaluate(check, self.workspace, [event], ""))
        event["type"] = "item.started"
        self.assertFalse(evals.evaluate(check, self.workspace, [event], ""))

    def test_qualitative_checks_stay_pending(self):
        self.assertIsNone(evals.evaluate({"type": "rubric"}, self.workspace, [], ""))

    def test_unchanged_check_detects_edits_additions_and_deletions(self):
        folder = self.workspace / "app"
        folder.mkdir()
        path = folder / "orders.py"
        path.write_text("VALUE = 1\n", encoding="utf-8")
        check = {"type": "unchanged", "paths": ["app", "tests"]}
        before = evals.file_snapshot(self.workspace, check["paths"])
        self.assertTrue(evals.evaluate(check, self.workspace, [], "", before))
        path.write_text("VALUE = 2\n", encoding="utf-8")
        self.assertFalse(evals.evaluate(check, self.workspace, [], "", before))
        path.write_text("VALUE = 1\n", encoding="utf-8")
        extra = folder / "new.py"
        extra.write_text("", encoding="utf-8")
        self.assertFalse(evals.evaluate(check, self.workspace, [], "", before))
        extra.unlink()
        path.unlink()
        self.assertFalse(evals.evaluate(check, self.workspace, [], "", before))

    def test_judge_receives_trace_and_related_workspace_artifacts(self):
        (self.workspace / "app").mkdir()
        (self.workspace / "app/orders.py").write_text("cancel = True\n", encoding="utf-8")
        source = self.workspace / "cases/sample"
        source.mkdir(parents=True)
        (source / "suite.md").write_text("Tests must run successfully.", encoding="utf-8")
        case = {"name": "sample", "timeout_seconds": 30,
                "checks": [{"id": "suite", "type": "rubric", "source": "trace", "rubric": "suite.md"}]}
        events = [self.command("python -m unittest", 0)]
        output = self.workspace / "results"
        output.mkdir()
        response = json.dumps({"checks": [{"id": "suite", "pass": True, "reason": "Three tests passed."}]})
        with patch.object(evals, "EVALS", source.parent), \
                patch.object(evals, "run_codex", return_value=([], response)) as run:
            verdicts = evals.judge_checks(case, self.workspace, events, "Done", "codex", {}, output, None)
        prompt = run.call_args.args[3]
        self.assertIn("command_execution", prompt)
        self.assertIn("app/orders.py", prompt)
        self.assertTrue(verdicts["suite"]["pass"])

    def test_eval_install_excludes_prompts_and_rubrics(self):
        with TemporaryDirectory() as temporary:
            staged = evals.stage_plugin(temporary) / "plugins/ai-skills"
            self.assertFalse((staged / "evals").exists())
            self.assertEqual((ROOT / "plugins/ai-skills/plugin.json").read_bytes(),
                             (staged / "plugin.json").read_bytes())
            self.assertTrue((staged / "skills/sdd/scripts/isolated_tree.py").is_file())

    def test_judge_failure_preserves_generated_evidence(self):
        case = {"name": "sample", "sandbox": "workspace-write", "timeout_seconds": 30,
                "checks": [{"id": "content", "type": "rubric"}]}
        source = self.workspace / "cases/sample"
        source.mkdir(parents=True)
        (source / "prompt.md").write_text("Create an artifact", encoding="utf-8")

        def seed_fixture(case, workspace):
            workspace.mkdir()
            (workspace / "artifact.md").write_text("Generated contract", encoding="utf-8")

        def inspect_fixture_run(executable, env, workspace, prompt, output, sandbox, timeout, model,
                                reasoning_effort=None):
            config = (Path(env["CODEX_HOME"]) / "config.toml").read_text(encoding="utf-8")
            self.assertIn(workspace.as_posix(), config)
            self.assertNotIn(ROOT.as_posix(), config)
            self.assertEqual("workspace-write", sandbox)
            self.assertEqual("chosen-model", model)
            self.assertEqual("xhigh", reasoning_effort)
            return ([{"type": "turn.completed"}], "Done")

        args = SimpleNamespace(fixtures_only=False, model="chosen-model", judge=True, codex="codex",
                               reasoning_effort="xhigh")
        with patch.object(evals, "EVALS", source.parent), \
                patch.object(evals, "seed", side_effect=seed_fixture), \
                patch.object(evals.Path, "home", return_value=self.workspace / "empty-home"), \
                patch.dict(evals.os.environ, {"CODEX_HOME": str(self.workspace / "empty-home")}), \
                patch.object(evals.shutil, "which", return_value="codex"), \
                patch.object(evals.subprocess, "run", return_value=SimpleNamespace(returncode=0)), \
                patch.object(evals, "run_codex", side_effect=inspect_fixture_run), \
                patch.object(evals, "judge_checks", side_effect=ValueError("judge failed")), \
                self.assertRaisesRegex(ValueError, "judge failed"):
            evals.run_case(case, self.workspace / "results", args)
        saved = self.workspace / "results/sample/plugin/workspace/artifact.md"
        self.assertEqual("Generated contract", saved.read_text(encoding="utf-8"))

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
                effort = "xhigh" if sandbox == "workspace-write" else None
                evals.run_codex("codex", {}, self.workspace, "$sdd", self.workspace, sandbox, 30,
                                reasoning_effort=effort)
                command = run.call_args.args[0]
                self.assertIn(f'default_permissions="{profile}"', command)
                if effort:
                    self.assertIn('model_reasoning_effort="xhigh"', command)
                else:
                    self.assertFalse(any(item.startswith("model_reasoning_effort=") for item in command))
                self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", command)
                self.assertEqual("-", command[-1])
                self.assertEqual("$sdd", run.call_args.kwargs["input"])


if __name__ == "__main__":
    unittest.main()
