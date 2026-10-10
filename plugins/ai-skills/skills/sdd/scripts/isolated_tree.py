"""Create and remove temporary Git worktrees for verification, without touching the user's checkout.

Usage, from inside the consumer repository:
  python isolated_tree.py create --base <commit>   tree at <commit>, to run a check on the base
  python isolated_tree.py create --current         tree at HEAD plus the uncommitted changes,
                                                   to inject faults into the current content
  python isolated_tree.py remove <tree>            remove the tree and confirm that the
                                                   checkout did not change since create

create prints the path of the new tree, which lives in the system temporary folder,
outside the repository. --current copies the modified, staged and untracked files that
Git does not ignore, and deletes in the tree the files deleted in the checkout.

remove only accepts a tree made by create. It forces the removal, which discards the
build output left in the tree, and compares `git status --porcelain` of the checkout
with the status recorded by create.

Exit codes: 0 = done, 1 = the checkout changed since create or the tree was left behind,
2 = invalid input or Git error.
"""

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


RECORD = "sdd-isolated-tree.json"
PREFIX = "sdd-tree-"


class GitError(Exception):
    pass


def git(cwd, *args):
    result = subprocess.run(["git", *args], cwd=cwd, capture_output=True)
    if result.returncode:
        raise GitError(f"git {' '.join(args)}: {result.stderr.decode('utf-8', 'replace').strip()}")
    return result.stdout


def text(output):
    return os.fsdecode(output).strip()


def entries(output):
    return [os.fsdecode(entry) for entry in output.split(b"\0") if entry]


def checkout_status(root):
    return git(root, "status", "--porcelain=v1", "-z", "--untracked-files=all").hex()


def copy_changes(root, tree):
    """Mirror the uncommitted state of the checkout into a tree checked out at HEAD."""
    changed = entries(git(root, "diff", "--name-only", "--no-renames", "-z", "HEAD"))
    untracked = entries(git(root, "ls-files", "--others", "--exclude-standard", "-z"))
    for relative in dict.fromkeys(changed + untracked):
        source, target = root / relative, tree / relative
        if target.is_symlink() or target.is_file():
            target.unlink()
        if source.is_symlink() or source.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target, follow_symlinks=False)


def create(base, current):
    root = Path(text(git(Path.cwd(), "rev-parse", "--show-toplevel"))).resolve()
    commit = text(git(root, "rev-parse", "--verify", f"{'HEAD' if current else base}^{{commit}}"))
    status = checkout_status(root)
    parent = Path(tempfile.mkdtemp(prefix=PREFIX)).resolve()
    if parent.is_relative_to(root):
        parent.rmdir()
        raise ValueError(f"the temporary folder is inside the repository: {parent}")
    tree = parent / "tree"
    try:
        git(root, "worktree", "add", "--detach", str(tree), commit)
    except GitError:
        shutil.rmtree(parent, ignore_errors=True)
        raise
    try:
        if current:
            copy_changes(root, tree)
        admin = Path(text(git(tree, "rev-parse", "--absolute-git-dir")))
        record = {"root": str(root), "commit": commit, "status": status}
        (admin / RECORD).write_text(json.dumps(record), encoding="utf-8")
    except (GitError, OSError):
        subprocess.run(["git", "worktree", "remove", "--force", str(tree)], cwd=root, capture_output=True)
        shutil.rmtree(parent, ignore_errors=True)
        raise
    print(tree)
    return 0


def remove(path):
    tree = Path(path).resolve()
    if not tree.is_dir():
        raise ValueError(f"not a folder: {tree}")
    admin = Path(text(git(tree, "rev-parse", "--absolute-git-dir")))
    record_path = admin / RECORD
    if not record_path.is_file():
        raise ValueError(f"not a tree made by isolated_tree.py create: {tree}")
    record = json.loads(record_path.read_text(encoding="utf-8"))
    root = Path(record["root"])
    left = subprocess.run(["git", "worktree", "remove", "--force", str(tree)], cwd=root, capture_output=True)
    code = 0
    if left.returncode:
        print(f"tree left at {tree}: {left.stderr.decode('utf-8', 'replace').strip()}", file=sys.stderr)
        code = 1
    elif tree.parent.name.startswith(PREFIX):
        shutil.rmtree(tree.parent, ignore_errors=True)
    if checkout_status(root) != record["status"]:
        print(f"the checkout at {root} changed since the tree was created; compare git status", file=sys.stderr)
        code = 1
    if code == 0:
        print(f"removed {tree}; checkout unchanged")
    return code


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    make = commands.add_parser("create", help="create a temporary tree")
    content = make.add_mutually_exclusive_group(required=True)
    content.add_argument("--base", help="commit to check out")
    content.add_argument("--current", action="store_true", help="HEAD plus the uncommitted changes")
    drop = commands.add_parser("remove", help="remove a tree made by create")
    drop.add_argument("tree")
    args = parser.parse_args()
    try:
        return create(args.base, args.current) if args.command == "create" else remove(args.tree)
    except (GitError, OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
