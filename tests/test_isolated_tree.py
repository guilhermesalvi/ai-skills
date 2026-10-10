"""Regression cases for the temporary verification trees, using only throwaway repositories."""
import os
from pathlib import Path
import subprocess
import sys
import unittest
from tempfile import TemporaryDirectory


SCRIPT = Path(__file__).resolve().parents[1] / "plugins" / "ai-skills" / "skills" / "sdd" / "scripts" / "isolated_tree.py"
# Keep bytecode out of the skill folder, which a local plugin install copies as is.
ENV = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}


def git(folder, *args):
    return subprocess.run(["git", "-C", str(folder), *args], check=True, capture_output=True, text=True).stdout


def commit_all(folder, message):
    git(folder, "add", "-A")
    git(folder, "-c", "user.name=test", "-c", "user.email=test@example.com", "commit", "-qm", message)


def run(folder, *args):
    return subprocess.run([sys.executable, "-X", "utf8", str(SCRIPT), *args], cwd=folder,
                          capture_output=True, text=True, encoding="utf-8", env=ENV)


class IsolatedTree(unittest.TestCase):
    def setUp(self):
        temp = TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.repo = Path(temp.name) / "repo"
        self.repo.mkdir()
        git(self.repo, "init", "-q")
        (self.repo / ".gitignore").write_text("build/\n", encoding="utf-8")
        (self.repo / "app.py").write_text("VALUE = 1\n", encoding="utf-8")
        (self.repo / "old.py").write_text("OLD = True\n", encoding="utf-8")
        commit_all(self.repo, "base")
        (self.repo / "app.py").write_text("VALUE = 2\n", encoding="utf-8")
        commit_all(self.repo, "change")

    def create(self, *args):
        result = run(self.repo, "create", *args)
        self.assertEqual(0, result.returncode, result.stderr)
        tree = Path(result.stdout.strip())
        self.addCleanup(lambda: tree.exists() and run(self.repo, "remove", str(tree)))
        return tree

    def test_base_tree_has_the_base_content_outside_the_repository(self):
        status = git(self.repo, "status", "--porcelain")
        tree = self.create("--base", "HEAD~1")
        self.assertEqual("VALUE = 1\n", (tree / "app.py").read_text(encoding="utf-8"))
        self.assertFalse(tree.resolve().is_relative_to(self.repo.resolve()))
        self.assertEqual(status, git(self.repo, "status", "--porcelain"))
        result = run(self.repo, "remove", str(tree))
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertFalse(tree.exists())
        self.assertNotIn(str(tree.resolve()), git(self.repo, "worktree", "list"))

    def test_current_tree_mirrors_uncommitted_changes(self):
        (self.repo / "app.py").write_text("VALUE = 3\n", encoding="utf-8")
        (self.repo / "old.py").unlink()
        (self.repo / "pkg").mkdir()
        (self.repo / "pkg" / "new.py").write_text("NEW = True\n", encoding="utf-8")
        git(self.repo, "add", "pkg/new.py")
        (self.repo / "notes.txt").write_text("untracked\n", encoding="utf-8")
        (self.repo / "build").mkdir()
        (self.repo / "build" / "out.bin").write_text("ignored\n", encoding="utf-8")
        status = git(self.repo, "status", "--porcelain")
        tree = self.create("--current")
        self.assertEqual("VALUE = 3\n", (tree / "app.py").read_text(encoding="utf-8"))
        self.assertFalse((tree / "old.py").exists())
        self.assertTrue((tree / "pkg" / "new.py").is_file())
        self.assertTrue((tree / "notes.txt").is_file())
        self.assertFalse((tree / "build").exists())
        (tree / "app.py").write_text("VALUE = -1\n", encoding="utf-8")
        result = run(self.repo, "remove", str(tree))
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(status, git(self.repo, "status", "--porcelain"))
        self.assertEqual("VALUE = 3\n", (self.repo / "app.py").read_text(encoding="utf-8"))

    def test_remove_reports_a_checkout_changed_after_create(self):
        tree = self.create("--current")
        (self.repo / "app.py").write_text("VALUE = 9\n", encoding="utf-8")
        result = run(self.repo, "remove", str(tree))
        self.assertEqual(1, result.returncode)
        self.assertIn("changed since the tree was created", result.stderr)
        self.assertFalse(tree.exists())

    def test_remove_refuses_the_main_checkout(self):
        result = run(self.repo, "remove", str(self.repo))
        self.assertEqual(2, result.returncode)
        self.assertIn("not a tree made by", result.stderr)
        self.assertTrue((self.repo / "app.py").is_file())

    def test_create_rejects_an_unknown_commit(self):
        result = run(self.repo, "create", "--base", "missing-ref")
        self.assertEqual(2, result.returncode)
        self.assertEqual("", result.stdout)


if __name__ == "__main__":
    unittest.main()
