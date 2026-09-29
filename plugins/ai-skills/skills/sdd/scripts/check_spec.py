"""Check requirement IDs, links and schema structure of the specs in a specs folder.

Usage: python check_spec.py [<specs folder>]   (default: docs/specs)

Reads <capability>/spec.md and the change plans <capability>/NNNN-<change>.md.
Other Markdown files under a capability folder are checked only for cited IDs;
files outside capability folders, such as CLAUDE.md, are not read.

IDs: a requirement is defined by a list item that starts with a bold ID, such
as "- **DOC-01** ...". A prefix belongs to the spec that defines it and must
match the Requirement Prefix in its header; tokens whose prefix no spec
defines, such as SHA-256, are not citations.

Plans also get the link check, and each item under Checks must be a checkbox
that ends with its proof in inline code.

Structure: section titles, header labels and table columns are the English
schema of the skill, whatever the prose language. A spec or plan with none of
its schema titles is listed as not checked and gets only the ID and link
checks. This read-only check does not validate behavior or Mermaid rendering.
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
DEFINITION = re.compile(r"^-\s+\*\*(" + ID + r")\*\*", re.M)
LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
HEADER_PREFIX = re.compile(r"^\|\s*\*\*Requirement Prefix\*\*\s*\|\s*`?([A-Z][A-Z0-9]*)`?\s*\|", re.M)
PLAN_NAME = re.compile(r"^[0-9]{4}-.+\.md$")
CONFIRMED = re.compile(r"Confirmed\?\s*[yn]\.?\s*$")

SPEC_SECTIONS = {"Context", "Scope", "Assumptions", "Gaps", "Glossary", "Requirements", "Domain Events",
                 "Acceptance Scenarios", "Observable Decisions", "Trade-offs", "Divergences", "References"}
SPEC_BASE = ("Context", "Requirements")
PLAN_SECTIONS = {"Context", "Technical Decisions", "Structure", "Risks", "Assumptions", "Gaps", "Checks", "References"}
PLAN_BASE = ("Checks",)
FULL_TABLES = ("Gaps", "Observable Decisions", "Trade-offs", "Technical Decisions")
# Titles spelled the same in other prose languages do not identify the schema.
SHARED_TITLES = {"Trade-offs"}


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


def sections(text):
    """Map each level-two title to its lines, for text without fenced blocks."""
    result, current = {}, None
    for line in text.splitlines():
        title = re.match(r"^##\s+(.+?)\s*#*\s*$", line)
        if title and not line.startswith("###"):
            current = title[1]
            result[current] = []
        elif current is not None:
            result[current].append(line)
    return result


def list_items(lines):
    """Join each top-level list item with its continuation lines."""
    items, open_item = [], False
    for line in lines:
        if line.startswith("- "):
            items.append(line)
            open_item = True
        elif open_item and line.startswith(" ") and line.strip():
            items[-1] += " " + line.strip()
        else:
            open_item = False
    return items


def table_rows(lines):
    rows = [line for line in lines if line.lstrip().startswith("|")]
    return [[cell.strip() for cell in row.strip().strip("|").split("|")] for row in rows[2:]]


def check_links(name, prose, path, root):
    findings = []
    for href in LINK.findall(prose):
        href = href.strip().strip("<>")
        url = urlsplit(href)
        if url.scheme or url.netloc or not url.path:
            continue
        target = unquote(url.path)
        resolved = root / target.lstrip("/") if target.startswith("/") else path.parent / target
        if not resolved.exists():
            findings.append(f"{name}: local link does not resolve: {href}")
    return findings


def check_structure(name, prose, schema, base):
    found = sections(prose)
    if not (schema - SHARED_TITLES) & found.keys():
        return None
    findings = [f"{name}: missing section {title}" for title in base if title not in found]
    for title, lines in found.items():
        if not any(line.strip() for line in lines):
            findings.append(f"{name}: empty section {title}")
    for item in list_items(found.get("Assumptions", [])):
        if not CONFIRMED.search(item):
            findings.append(f"{name}: assumption without Confirmed? y or n: {item[:60]}")
    for title in FULL_TABLES:
        for row in table_rows(found.get(title, [])):
            if not all(row):
                findings.append(f"{name}: {title} row with an empty cell: {' | '.join(row)[:60]}")
    for item in list_items(found.get("Checks", [])):
        if not re.match(r"^- \[[ xX]\] ", item):
            findings.append(f"{name}: check is not a checkbox: {item[:60]}")
        elif not re.search(r"`[^`]+`\s*$", item):
            findings.append(f"{name}: check without proof: {item[:60]}")
    return findings


def check(folder):
    folder = Path(folder).resolve()
    if not folder.is_dir():
        raise ValueError(f"not a folder: {folder}")
    specs = sorted(folder.glob("*/spec.md"))
    if not specs:
        raise ValueError(f"no specs in {folder}")
    plans = sorted(p for p in folder.glob("*/*.md") if PLAN_NAME.match(p.name))
    names = {p.relative_to(folder).as_posix(): p for p in specs}
    texts = {name: p.read_text(encoding="utf-8-sig") for name, p in names.items()}
    parsed = {name: strip_fences(text) for name, text in texts.items()}
    consumers = sorted(p for p in folder.glob("*/**/*.md") if p.name != "spec.md")
    findings, unchecked = [], []

    definitions, prefix_owners = defaultdict(list), defaultdict(set)
    for name, (prose, _) in parsed.items():
        prefixes = set()
        for identifier in DEFINITION.findall(prose):
            definitions[identifier].append(name)
            prefixes.add(prefix_of(identifier))
        for prefix in prefixes:
            prefix_owners[prefix].add(name)
        if len(prefixes) > 1:
            findings.append(f"{name}: definitions use several prefixes: {', '.join(sorted(prefixes))}")
        header = HEADER_PREFIX.search(prose)
        if header and prefixes and header[1] not in prefixes:
            findings.append(f"{name}: Requirement Prefix {header[1]} differs from the definitions")
        structure = check_structure(name, prose, SPEC_SECTIONS, SPEC_BASE)
        if structure is None:
            unchecked.append(name)
        else:
            if not header:
                findings.append(f"{name}: missing Requirement Prefix in the header")
            findings.extend(structure)
    for identifier, owners in sorted(definitions.items()):
        if len(owners) > 1:
            findings.append(f"ids: {identifier} defined {len(owners)} times")
    for prefix, owners in sorted(prefix_owners.items()):
        if len(owners) > 1:
            findings.append(f"prefix: {prefix} belongs to several specs: {', '.join(sorted(owners))}")

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
        findings.extend(check_links(name, prose, names[name], root))

    for path in consumers:
        name = path.relative_to(folder).as_posix()
        text = path.read_text(encoding="utf-8-sig")
        for identifier in sorted(set(ID_TOKEN.findall(text))):
            if prefix_of(identifier) in prefix_owners and identifier not in definitions:
                findings.append(f"{name}: citation {identifier} has no definition")
        if path in plans:
            prose, unclosed = strip_fences(text)
            if unclosed:
                findings.append(f"{name}: unclosed code fence")
            findings.extend(check_links(name, prose, path, root))
            structure = check_structure(name, prose, PLAN_SECTIONS, PLAN_BASE)
            if structure is None:
                unchecked.append(name)
            else:
                findings.extend(structure)
    return findings, sorted(unchecked)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("folder", nargs="?", default="docs/specs")
    args = parser.parse_args()
    try:
        findings, unchecked = check(args.folder)
    except (OSError, UnicodeError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 2
    print("\n".join(findings) if findings else f"no findings in {args.folder}")
    for name in unchecked:
        print(f"structure not checked, titles outside the schema: {name}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
