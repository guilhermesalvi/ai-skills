"""Validate this repository's Claude Code marketplace, plugin manifest and skill resources."""

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
from tempfile import TemporaryDirectory
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ID = "ai-skills@ai-skills"


def valid_version(value):
    """Accept SemVer releases, prereleases and build metadata."""
    if not isinstance(value, str):
        return False
    number = r"(0|[1-9][0-9]*)"
    identifiers = r"([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)"
    match = re.fullmatch(rf"{number}\.{number}\.{number}(?:-{identifiers})?(?:\+{identifiers})?", value)
    if not match:
        return False
    prerelease = match[4]
    return prerelease is None or all(not part.isdigit() or part == "0" or not part.startswith("0")
                                     for part in prerelease.split("."))


def local_path(root, value):
    """Resolve a package path without allowing it to leave its root."""
    if not isinstance(value, str) or not value.startswith("./"):
        raise ValueError(f"path must start with ./: {value!r}")
    if ".." in value.replace("\\", "/").split("/"):
        raise ValueError(f"path must stay inside its root: {value}")
    path = (root / value).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f"path leaves its root: {value}")
    if not path.exists():
        raise ValueError(f"path does not exist: {value}")
    return path


def frontmatter(path):
    """Read the simple scalar frontmatter used by this repository's skills."""
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.S)
    if not match:
        raise ValueError(f"{path}: missing YAML frontmatter")
    fields = {}
    for line in match[1].splitlines():
        key, separator, value = line.partition(":")
        if not separator or key in fields or not value.strip():
            raise ValueError(f"{path}: invalid or duplicate frontmatter field: {line}")
        if key not in {"name", "description", "compatibility", "license"}:
            raise ValueError(f"{path}: unsupported field in this validator: {key}")
        fields[key] = value.strip()
    for key in ("name", "description"):
        if not fields.get(key):
            raise ValueError(f"{path}: missing {key}")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", fields["name"]):
        raise ValueError(f"{path}: invalid skill name")
    if fields["name"] != path.parent.name:
        raise ValueError(f"{path}: name differs from skill directory")
    if len(fields["name"]) > 64 or len(fields["description"]) > 1024:
        raise ValueError(f"{path}: frontmatter exceeds Agent Skills limits")
    return fields


def validate(root=ROOT):
    catalog = json.loads((root / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
    if not catalog.get("name") or not catalog.get("owner", {}).get("name") or not catalog.get("plugins"):
        raise ValueError("marketplace needs a name, an owner name and plugins")
    names = set()
    skills = []
    for entry in catalog["plugins"]:
        name = entry["name"]
        if name in names:
            raise ValueError(f"duplicate marketplace plugin: {name}")
        names.add(name)
        if not isinstance(entry["source"], str):
            raise ValueError(f"{name}: this validator expects a relative source in this repository")
        package = local_path(root, entry["source"])
        manifest = json.loads((package / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
        if manifest.get("name") != name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            raise ValueError(f"{name}: invalid plugin identity")
        # The installed copy is cached by version, so every release needs one.
        if not valid_version(manifest.get("version")):
            raise ValueError(f"{name}: invalid semantic version")
        if "version" in entry and entry["version"] != manifest["version"]:
            raise ValueError(f"{name}: marketplace and manifest versions differ")
        package_skills = sorted((package / "skills").glob("*/SKILL.md"))
        if not package_skills:
            raise ValueError(f"{name}: no packaged skills")
        for skill in package_skills:
            frontmatter(skill)
            for document in skill.parent.rglob("*.md"):
                for link in re.findall(r"\[[^\]]*\]\(([^)]+)\)", document.read_text(encoding="utf-8")):
                    url = urlsplit(link)
                    if url.scheme or not url.path:
                        continue
                    target = (document.parent / unquote(url.path)).resolve()
                    if not target.is_relative_to(skill.parent.resolve()) or not target.exists():
                        raise ValueError(f"{document.relative_to(root)}: broken or external skill resource: {link}")
            skills.append(skill.relative_to(root).as_posix())
    return {"marketplace": catalog["name"], "plugins": sorted(names), "skills": skills}


def install_smoke(root=ROOT):
    """Exercise the real CLI in a temporary Claude Code config; no login is needed."""
    executable = shutil.which("claude")
    if not executable:
        raise ValueError("Claude Code CLI is not on PATH")
    version = json.loads((root / "plugins/ai-skills/.claude-plugin/plugin.json").read_text(encoding="utf-8"))["version"]
    with TemporaryDirectory(prefix="ai-skills-install-") as temporary:
        config, cwd = Path(temporary) / "config", Path(temporary) / "cwd"
        config.mkdir()
        cwd.mkdir()
        # A temporary working directory keeps project settings out of the installation.
        env = dict(os.environ, CLAUDE_CONFIG_DIR=str(config))
        for arguments in (
            ["plugin", "marketplace", "add", str(root)],
            ["plugin", "install", PLUGIN_ID],
            ["plugin", "list", "--json"],
        ):
            result = subprocess.run([executable, *arguments], cwd=cwd, env=env, capture_output=True,
                                    text=True, encoding="utf-8", timeout=90)
            if result.returncode:
                raise ValueError(f"claude {' '.join(arguments)} failed: {result.stderr or result.stdout}")
        inventory = json.loads(result.stdout)
        active = [entry for entry in inventory if entry.get("id") == PLUGIN_ID and entry.get("enabled") is True]
        if not active:
            raise ValueError("installed inventory does not show ai-skills enabled")
        if active[0].get("version") != version:
            raise ValueError(f"installed version {active[0].get('version')} differs from manifest {version}")
        installed = Path(active[0]["installPath"]) / "skills/sdd"
        if not installed.resolve().is_relative_to(config.resolve()):
            raise ValueError("installed plugin is outside the temporary configuration")
        expected = root / "plugins/ai-skills/skills/sdd"
        for resource in expected.rglob("*"):
            if resource.is_file() and "__pycache__" not in resource.parts:
                cached = installed / resource.relative_to(expected)
                if not cached.is_file() or cached.read_bytes() != resource.read_bytes():
                    raise ValueError(f"installed resource differs: {resource.relative_to(expected)}")
        return inventory


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--install", action="store_true", help="also run an isolated real CLI install")
    args = parser.parse_args()
    try:
        result = validate()
        if args.install:
            result["installation"] = install_smoke()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, KeyError, OSError, subprocess.SubprocessError) as error:
        print(f"Validation failed: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
