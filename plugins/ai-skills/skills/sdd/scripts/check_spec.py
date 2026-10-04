"""Check requirement IDs, links and schema structure of the specs in a specs folder.

Usage: python check_spec.py [<specs folder>]   (default: docs/specs)

Reads <capability>/spec.md and the change plans <capability>/NNNN-<change>.md.
Other Markdown files under a capability folder are checked only for cited IDs;
files outside capability folders, such as AGENTS.md, are not read.

IDs: a requirement is defined by a list item that starts with a bold ID, such
as "- **DOC-01** ...". A prefix belongs to the spec that defines it and must
match the Requirement Prefix in its header; tokens whose prefix no spec
defines, such as SHA-256, are not citations. Two plans of a capability cannot
share a number.

Plans: each item under Checks is a checkbox that ends with its proof in inline
code. The header lists the Requirements in Scope, or none; each of them has a
check, and each ID a check cites is in scope. A committed plan whose checks are
all marked is the record of a concluded change: its citations and scope are
not checked, because the spec may have retired an ID since.

Structure: section titles, header labels, table columns and
the dimensions of Observable Decisions are the English schema of the skill,
whatever the prose language. Every artifact gets the whole schema: known
sections in order, the header, Observable Decisions with every dimension,
and assumptions with a bold statement followed by explanation.

Every spec and plan is also checked for template fields ({{...}}) left from
the skill's assets and for placeholder cells or proofs, such as TBD or n/a.
This read-only check does not validate behavior or Mermaid rendering.

Exit codes: 0 = no findings, 1 = findings, 2 = invalid input or read error.
"""

import argparse
from collections import defaultdict
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit


ID = r"[A-Z][A-Z0-9]*-[0-9]{2,}"
ID_TOKEN = re.compile(r"(?<![A-Za-z0-9_-])(" + ID + r")(?![A-Za-z0-9_-])")
DEFINITION = re.compile(r"^-\s+\*\*(" + ID + r")\*\*", re.M)
LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
HEADER_PREFIX = re.compile(r"^\|\s*\*\*Requirement Prefix\*\*\s*\|\s*`?([A-Z][A-Z0-9]*)`?\s*\|", re.M)
HEADER_SCOPE = re.compile(r"^\|\s*\*\*Requirements in Scope\*\*\s*\|(.*)\|\s*$", re.M)
HEADER_ROW = re.compile(r"^\|\s*\*\*([^*|]+)\*\*\s*\|\s*\|\s*$", re.M)
PLAN_NAME = re.compile(r"^([0-9]{4})-.+\.md$")
ASSUMPTION = re.compile(r"^-\s+\*\*\S(?:.*?\S)?\*\*\s+\S")
CHECKBOX = re.compile(r"^- \[([ xX])\] ")
PROOF = re.compile(r"`([^`]+)`\s*$")
INLINE_CODE = re.compile(r"`[^`\n]*`")
TEMPLATE_FIELD = re.compile(r"\{\{[^}\n]*\}\}")
PLACEHOLDER = re.compile(r"(?i)^(?:tbd|tba|todo|fixme|n/?a|\?+|-+|\.\.\.|…)$")

SPEC_SECTIONS = ("Context", "Scope", "Assumptions", "Gaps", "Glossary", "Requirements", "Domain Events",
                 "Acceptance Scenarios", "Observable Decisions", "Trade-offs", "Divergences", "References")
PLAN_SECTIONS = ("Context", "Technical Decisions", "Structure", "Risks", "Assumptions", "Gaps", "Checks",
                 "Progress", "References")
SPEC_BASE = ("Context", "Requirements", "Observable Decisions")
PLAN_BASE = ("Checks",)
DIMENSIONS = ("Validation and limits", "Failure and partial failure", "Idempotency and duplication",
              "Authorization", "Rate limiting", "Concurrency and ordering", "Data lifecycle",
              "External dependency failure", "State transitions", "Observability", "Cross-capability consistency")
FULL_TABLES = ("Gaps", "Observable Decisions", "Trade-offs", "Technical Decisions")
# Cells where the schema itself allows a short marker: the Owner of a gap nobody owns yet,
# and the row that gathers the dimensions that do not apply.
ALLOWED_MARKERS = {("Gaps", 2): {"?"}, ("Observable Decisions", 0): {"n/a"}}


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
    return None


def committed_text(path, root):
    """Return the content of path in HEAD, or None when HEAD lacks it or Git is unavailable."""
    if root is None:
        return None
    try:
        result = subprocess.run(["git", "-C", str(root), "show", f"HEAD:{path.relative_to(root).as_posix()}"],
                                capture_output=True, text=True, encoding="utf-8", errors="replace")
    except OSError:
        return None
    return result.stdout.lstrip("﻿") if result.returncode == 0 else None


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


def marker(cell):
    return cell.strip("` ").lower()


def check_links(name, prose, path, root):
    findings = []
    for href in LINK.findall(prose):
        href = href.strip().strip("<>")
        url = urlsplit(href)
        if url.scheme or url.netloc or not url.path:
            continue
        target = unquote(url.path)
        base = root or path.parent
        resolved = base / target.lstrip("/") if target.startswith("/") else path.parent / target
        if not resolved.exists():
            findings.append(f"{name}: local link does not resolve: {href}")
    return findings


def check_assumptions(name, items):
    """Check item structure; meaning and evidence require content review."""
    findings = []
    for item in items:
        if not ASSUMPTION.match(item):
            findings.append(f"{name}: assumption needs a bold statement followed by explanation: {item[:60]}")
    return findings


def check_dimensions(name, lines):
    rows = table_rows(lines)
    landed = " ".join(marker(row[0]) for row in rows if row)
    not_applicable = " ".join(row[1] for row in rows if len(row) > 1 and marker(row[0]) == "n/a")
    findings = []
    for dimension in DIMENSIONS:
        in_row = dimension.lower() in landed
        with_reason = re.search(re.escape(dimension) + r"\s*:\s*[^;\s]", not_applicable, re.I)
        if not (in_row or with_reason):
            findings.append(f"{name}: Observable Decisions misses {dimension}: add its row, or list it in the n/a row as '{dimension}: <reason>'")
    for row in rows:
        if len(row) > 1 and marker(row[0]) != "n/a" and marker(row[1]).startswith("n/a"):
            findings.append(f"{name}: {row[0]} is marked n/a in its own row; move it to the single n/a row")
    # A reason that cites a requirement lands the dimension somewhere, so it applies.
    for entry in not_applicable.split(";"):
        if ID_TOKEN.search(entry):
            findings.append(f"{name}: n/a entry cites a requirement, so the dimension applies; give it its own row: {entry.strip()[:60]}")
    return findings


def check_structure(name, prose, schema, base):
    """Return the schema findings for the current artifact."""
    found = sections(prose)
    findings = [f"{name}: missing section {title}" for title in base if title not in found]
    header = prose.split("\n## ", 1)[0]
    for label in HEADER_ROW.findall(header):
        findings.append(f"{name}: header row {label} is empty; delete the row when it does not apply")
    findings.extend(f"{name}: section {title} is not in the schema" for title in found if title not in schema)
    order = [schema.index(title) for title in found if title in schema]
    if order != sorted(order):
        findings.append(f"{name}: sections are out of the schema order: {', '.join(schema)}")
    for title, lines in found.items():
        if not any(line.strip() for line in lines):
            findings.append(f"{name}: empty section {title}")
    findings.extend(check_assumptions(name, list_items(found.get("Assumptions", []))))
    for title in FULL_TABLES:
        for row in table_rows(found.get(title, [])):
            if not all(row):
                findings.append(f"{name}: {title} row with an empty cell: {' | '.join(row)[:60]}")
                continue
            for column, cell in enumerate(row):
                if PLACEHOLDER.match(marker(cell)) and marker(cell) not in ALLOWED_MARKERS.get((title, column), ()):
                    findings.append(f"{name}: {title} row with a placeholder cell: {' | '.join(row)[:60]}")
                    break
    if "Observable Decisions" in schema and "Observable Decisions" in found:
        findings.extend(check_dimensions(name, found["Observable Decisions"]))
    for item in list_items(found.get("Checks", [])):
        proof = PROOF.search(item)
        if not CHECKBOX.match(item):
            findings.append(f"{name}: check is not a checkbox: {item[:60]}")
        elif not proof:
            findings.append(f"{name}: check without proof: {item[:60]}")
        elif PLACEHOLDER.match(proof[1].strip()):
            findings.append(f"{name}: check with a placeholder proof: {item[:60]}")
    for field in sorted(set(TEMPLATE_FIELD.findall(prose))):
        findings.append(f"{name}: template field left: {field[:60]}")
    return findings


def cited(text, prefixes):
    return {identifier for identifier in ID_TOKEN.findall(text) if prefix_of(identifier) in prefixes}


def check_scope(name, prose, checks, definitions, prefixes):
    header = HEADER_SCOPE.search(prose)
    if not header:
        return [f"{name}: missing Requirements in Scope in the header"]
    cell = header[1].strip()
    scope = set(ID_TOKEN.findall(cell))
    findings = []
    if not scope and marker(cell) != "none":
        findings.append(f"{name}: Requirements in Scope lists no ID; write none when the change alters no requirement")
    findings.extend(f"{name}: Requirements in Scope has undefined {identifier}"
                    for identifier in sorted(scope) if identifier not in definitions)
    in_checks = set()
    for item in checks:
        in_checks |= cited(INLINE_CODE.sub("", item), prefixes)
    findings.extend(f"{name}: requirement {identifier} in scope has no check" for identifier in sorted(scope - in_checks))
    findings.extend(f"{name}: check cites {identifier} outside Requirements in Scope"
                    for identifier in sorted(in_checks - scope))
    return findings


def check(folder):
    folder = Path(folder).resolve()
    if not folder.is_dir():
        raise ValueError(f"not a folder: {folder}")
    specs = sorted(folder.glob("*/spec.md"))
    if not specs:
        raise ValueError(f"no specs in {folder}")
    root = repository_root(folder)
    plans = sorted(p for p in folder.glob("*/*.md") if PLAN_NAME.match(p.name))
    names = {p.relative_to(folder).as_posix(): p for p in specs}
    texts = {name: p.read_text(encoding="utf-8-sig") for name, p in names.items()}
    parsed = {name: strip_fences(text) for name, text in texts.items()}
    consumers = sorted(p for p in folder.glob("*/**/*.md") if p.name != "spec.md")
    findings = []

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
        if not header:
            findings.append(f"{name}: missing Requirement Prefix in the header")
        findings.extend(check_structure(name, prose, SPEC_SECTIONS, SPEC_BASE))
    for identifier, owners in sorted(definitions.items()):
        if len(owners) > 1:
            findings.append(f"ids: {identifier} defined {len(owners)} times")
    for prefix, owners in sorted(prefix_owners.items()):
        if len(owners) > 1:
            findings.append(f"prefix: {prefix} belongs to several specs: {', '.join(sorted(owners))}")

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

    numbers = defaultdict(list)
    for path in plans:
        numbers[(path.parent.name, PLAN_NAME.match(path.name)[1])].append(path.name)
    for (capability, number), files in sorted(numbers.items()):
        if len(files) > 1:
            findings.append(f"{capability}: plan number {number} used by {', '.join(files)}")

    for path in consumers:
        name = path.relative_to(folder).as_posix()
        text = path.read_text(encoding="utf-8-sig")
        concluded = False
        if path in plans:
            prose, unclosed = strip_fences(text)
            previous = committed_text(path, root)
            checks = list_items(sections(prose).get("Checks", []))
            concluded = previous is not None and bool(checks) and all(
                (match := CHECKBOX.match(item)) and match[1] != " " for item in checks)
            if unclosed:
                findings.append(f"{name}: unclosed code fence")
            findings.extend(check_links(name, prose, path, root))
            findings.extend(check_structure(name, prose, PLAN_SECTIONS, PLAN_BASE))
            if not HEADER_SCOPE.search(prose):
                findings.append(f"{name}: missing Requirements in Scope in the header")
            elif not concluded:
                findings.extend(check_scope(name, prose, checks, definitions, prefix_owners.keys()))
        if concluded:
            continue
        for identifier in sorted(set(ID_TOKEN.findall(text))):
            if prefix_of(identifier) in prefix_owners and identifier not in definitions:
                findings.append(f"{name}: citation {identifier} has no definition")
    return findings


def main():
    # Findings quote the artifacts; a Windows console code page would garble their accents and dashes.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
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
