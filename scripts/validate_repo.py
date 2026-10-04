"""Validate this repository's portable plugin, marketplace and skill resources."""

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
    catalog = json.loads((root / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
    if not catalog.get("name") or not catalog.get("plugins"):
        raise ValueError("marketplace needs a name and plugins")
    names = set()
    skills = []
    for entry in catalog["plugins"]:
        name = entry["name"]
        if name in names:
            raise ValueError(f"duplicate marketplace plugin: {name}")
        names.add(name)
        if entry["source"]["source"] != "local":
            raise ValueError(f"{name}: this validator expects a local source")
        if entry["policy"]["installation"] not in {"AVAILABLE", "INSTALLED_BY_DEFAULT", "NOT_AVAILABLE"}:
            raise ValueError(f"{name}: invalid installation policy")
        if entry["policy"]["authentication"] not in {"ON_INSTALL", "ON_USE"}:
            raise ValueError(f"{name}: invalid authentication policy")
        if not entry.get("category"):
            raise ValueError(f"{name}: missing category")
        package = local_path(root, entry["source"]["path"])
        manifest = json.loads((package / "plugin.json").read_text(encoding="utf-8"))
        if manifest.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
            raise ValueError(f"{name}: missing portable plugin schema")
        if manifest.get("name") != name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            raise ValueError(f"{name}: invalid plugin identity")
        if not valid_version(manifest.get("version")):
            raise ValueError(f"{name}: invalid semantic version")
        interface = manifest["extensions"]["com.openai"]["interface"]
        if not all(interface.get(key) for key in ("displayName", "shortDescription", "defaultPrompt")):
            raise ValueError(f"{name}: incomplete OpenAI interface")
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
    """Exercise the real CLI in a temporary Codex home; no login is needed."""
    executable = shutil.which("codex")
    if not executable:
        raise ValueError("Codex CLI is not on PATH")
    with TemporaryDirectory(prefix="ai-skills-install-") as temporary:
        env = dict(os.environ, CODEX_HOME=temporary)
        for arguments in (
            ["plugin", "marketplace", "add", str(root), "--json"],
            ["plugin", "add", "ai-skills@ai-skills", "--json"],
            ["plugin", "list", "--marketplace", "ai-skills", "--json"],
        ):
            result = subprocess.run([executable, *arguments], cwd=root, env=env, capture_output=True,
                                    text=True, encoding="utf-8", timeout=90)
            if result.returncode:
                raise ValueError(f"codex {' '.join(arguments)} failed: {result.stderr or result.stdout}")
            inventory = json.loads(result.stdout)
        active = [entry for entry in inventory.get("installed", [])
                  if entry.get("pluginId") == "ai-skills@ai-skills" and entry.get("enabled") is True]
        if not active:
            raise ValueError("installed inventory does not show ai-skills enabled")
        cached_skills = list((Path(temporary) / "plugins/cache").rglob("skills/sdd/SKILL.md"))
        if not cached_skills:
            raise ValueError("installed cache does not contain the sdd skill")
        expected = root / "plugins/ai-skills/skills/sdd"
        installed = cached_skills[0].parent
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
