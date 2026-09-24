"""Check requirement IDs and local links of the PRDs in a specs folder.

Usage: python check_prd.py [<specs folder>]   (default: docs/specs)

Reads only <capability>/prd.md and the product overview overview.md, so specs,
designs, tasks and instruction files such as CLAUDE.md can live in the same
tree. The check ignores section titles and labels, so it works in any prose
language. A requirement is defined by a list item that starts with a bold ID,
such as "- **DOC-01 (Must)** ...". A prefix belongs to the PRD that defines it,
and tokens whose prefix no PRD defines, such as SHA-256, are not citations.
This read-only check does not validate business meaning, document structure or
Mermaid rendering.
Exit codes: 0 = no findings, 1 = findings, 2 = invalid input or read error.
"""

import argparse
from collections import defaultdict
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


ID = r"[A-Z][A-Z0-9]*-[0-9]{2,}"
ID_TOKEN = re.compile(r"(?<![A-Za-z0-9_-])(" + ID + r")(?![A-Za-z0-9_-])")
DEFINITION = re.compile(r"^-\s+\*\*(" + ID + r")(?:\s+\(([^)]+)\))?\*\*", re.M)
LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
PRIORITIES = {"Must", "Should", "Could", "Won't"}


def strip_fences(text):
    """Return the text outside fenced blocks and whether a fence is left open."""
    prose, fence_char, fence_length = [], None, 0
    for line in text.splitlines():
        fence = re.match(r"^\s{0,3}(`{3,}|~{3,})(.*)$", line)
        if fence_char is None:
            if fence:
                fence_char, fence_length = fence[1][0], len(fence[1])
            else:
                prose.append(line)
        elif fence and fence[1][0] == fence_char and len(fence[1]) >= fence_length and not fence[2].strip():
            fence_char = None
    return "\n".join(prose), fence_char is not None


def prefix_of(identifier):
    return identifier.split("-", 1)[0]


def repository_root(folder):
    for parent in (folder, *folder.parents):
        if (parent / ".git").exists():
            return parent
    return folder


def check(folder):
    folder = Path(folder).resolve()
    if not folder.is_dir():
        raise ValueError(f"not a folder: {folder}")
    prds = sorted(folder.glob("*/prd.md"))
    if not prds:
        raise ValueError(f"no PRDs in {folder}")
    overview = folder / "overview.md"
    paths = prds + ([overview] if overview.is_file() else [])
    names = {p.relative_to(folder).as_posix(): p for p in paths}
    texts = {name: p.read_text(encoding="utf-8-sig") for name, p in names.items()}
    parsed = {name: strip_fences(text) for name, text in texts.items()}
    findings = []

    definitions, prefix_owners = defaultdict(list), defaultdict(set)
    for name, (prose, _) in parsed.items():
        prefixes = set()
        for identifier, priority in DEFINITION.findall(prose):
            definitions[identifier].append(name)
            prefixes.add(prefix_of(identifier))
            if priority not in PRIORITIES:
                findings.append(f"{name}: {identifier} has no valid MoSCoW priority")
        for prefix in prefixes:
            prefix_owners[prefix].add(name)
        if len(prefixes) > 1:
            findings.append(f"{name}: definitions use several prefixes: {', '.join(sorted(prefixes))}")
    for identifier, owners in sorted(definitions.items()):
        if len(owners) > 1:
            findings.append(f"ids: {identifier} defined {len(owners)} times")
    for prefix, owners in sorted(prefix_owners.items()):
        if len(owners) > 1:
            findings.append(f"prefix: {prefix} belongs to several PRDs: {', '.join(sorted(owners))}")

    root = repository_root(folder)
    for name, text in texts.items():
        prose, unclosed = parsed[name]
        if unclosed:
            findings.append(f"{name}: unclosed code fence")
        for identifier in sorted(set(ID_TOKEN.findall(text))):
            if identifier.startswith(("FR-", "NFR-")):
                findings.append(f"{name}: unprefixed id {identifier}")
            elif prefix_of(identifier) in prefix_owners and identifier not in definitions:
                findings.append(f"{name}: citation {identifier} has no definition")
        for href in LINK.findall(prose):
            href = href.strip().strip("<>")
            url = urlsplit(href)
            if url.scheme or url.netloc or not url.path:
                continue
            target = unquote(url.path)
            resolved = root / target.lstrip("/") if target.startswith("/") else names[name].parent / target
            if not resolved.exists():
                findings.append(f"{name}: local link does not resolve: {href}")
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("folder", nargs="?", default="docs/specs")
    args = parser.parse_args()
    try:
        findings = check(args.folder)
    except (OSError, UnicodeError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 2
    print("\n".join(findings) if findings else f"no findings in {args.folder}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
