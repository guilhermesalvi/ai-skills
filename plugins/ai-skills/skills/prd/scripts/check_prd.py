"""Check structural invariants of numbered PRDs in the working tree.

Usage: python check_prd.py [<prd folder>]   (default: docs/prd)

Reads only numbered PRDs (NNNN-*.md), so instruction files such as CLAUDE.md
can live in the same folder. Citations count as requirement IDs only when their
prefix is declared by a PRD in the folder, so tokens such as SHA-256 are not
findings. This read-only check does not validate business meaning, external
sources or Mermaid rendering; references/workflow.md describes its scope.
Exit codes: 0 = no findings, 1 = findings, 2 = invalid input or read error.
"""

import argparse
from collections import Counter, defaultdict
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


SECTIONS = [
    "Executive Summary", "Strategic Alignment", "Context and Problem",
    "Target User / JTBD", "Opportunity / Hypothesis", "Proposed Solution",
    "Domain Glossary", "Functional Requirements", "Domain Events",
    "Non-functional Requirements", "Regulatory Considerations", "Non-goals",
    "Declared Trade-offs", "Success Metrics", "Acceptance Criteria",
    "Dependencies and Risks", "Open Questions", "Weakest Point", "References",
]
OVERVIEW_SECTIONS = [
    "Purpose", "Contexts", "Event Catalog", "Flows Between Contexts",
    "Terms per Context", "Decisions Delegated to ADR",
]
MANDATORY = [
    "Executive Summary", "Context and Problem", "Target User / JTBD",
    "Proposed Solution", "Functional Requirements",
]
MARKER = "<!-- prd: overview -->"
PREFIX = re.compile(r"^Requirement prefix: `([A-Z][A-Z0-9]*)`\.(.*)$", re.M)
ID = r"[A-Z][A-Z0-9]*-(?:NFR-)?[0-9]{2,}"
ID_TOKEN = re.compile(r"(?<![A-Za-z0-9_-])(" + ID + r")(?![A-Za-z0-9_-])")
DEFINITION = re.compile(
    r"^-\s+\*\*(" + ID + r")(?:\s+\(([^)]+)\))?\*\*\s+(.+)$", re.M
)
PRIORITIES = {"Must", "Should", "Could", "Won't"}


def strip_fences(text):
    """Return prose, fenced blocks, and whether an opening fence remains."""
    prose, blocks, body = [], [], []
    fence_char, fence_length, language = None, 0, ""
    for line in text.splitlines():
        fence = re.match(r"^\s{0,3}(`{3,}|~{3,})(.*)$", line)
        if fence_char is None:
            if fence:
                fence_char = fence[1][0]
                fence_length = len(fence[1])
                language = fence[2].strip()
                body = []
            else:
                prose.append(line)
        elif (fence and fence[1][0] == fence_char
              and len(fence[1]) >= fence_length and not fence[2].strip()):
            blocks.append((language, "\n".join(body)))
            fence_char = None
        else:
            body.append(line)
    return "\n".join(prose), blocks, fence_char is not None


def section(text, heading):
    match = re.search(r"^## " + re.escape(heading) + r"\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return match[1] if match else ""


def repository_root(folder):
    for parent in (folder, *folder.parents):
        if (parent / ".git").exists():
            return parent
    return folder.parent.parent if folder.name == "prd" and folder.parent.name == "docs" else folder


def check(folder):
    folder = Path(folder).resolve()
    if not folder.is_dir():
        raise ValueError(f"not a folder: {folder}")
    paths = sorted(p for p in folder.glob("*.md") if re.fullmatch(r"[0-9]{4}-.+\.md", p.name))
    if not paths:
        raise ValueError(f"no numbered PRDs in {folder}")
    texts = {p.name: p.read_text(encoding="utf-8-sig") for p in paths}
    parsed = {name: strip_fences(text) for name, text in texts.items()}
    findings, definitions, prefix_owners = [], defaultdict(list), defaultdict(list)
    for number, count in Counter(p.name[:4] for p in paths).items():
        if count > 1:
            findings.append(f"numbering: {number} used by {count} files")
    for name, (prose, _, _) in parsed.items():
        prefix = PREFIX.search(prose)
        if prefix:
            prefix_owners[prefix[1]].append(name)
        for item in DEFINITION.finditer(prose):
            identifier, priority, _ = item.groups()
            definitions[identifier].append(name)
            if "-NFR-" in identifier:
                if priority:
                    findings.append(f"{name}: NFR {identifier} carries a priority")
            elif priority not in PRIORITIES:
                findings.append(f"{name}: {identifier} has no valid MoSCoW priority")
            if prefix and not identifier.startswith(prefix[1] + "-"):
                findings.append(f"{name}: definition {identifier} uses a foreign prefix")
    for identifier, owners in definitions.items():
        if len(owners) > 1:
            findings.append(f"ids: {identifier} defined {len(owners)} times")
    for prefix, owners in prefix_owners.items():
        if len(owners) > 1:
            findings.append(f"prefix: {prefix} belongs to multiple PRDs: {', '.join(owners)}")

    root = repository_root(folder)
    overviews = [name for name, text in texts.items() if text.startswith(MARKER + "\n")]
    for name, text in texts.items():
        prose, blocks, unclosed = parsed[name]
        overview = name in overviews
        if name.startswith("0000-") != overview:
            findings.append(f"{name}: number 0000 and overview marker must coincide")
        title_text = prose.removeprefix(MARKER + "\n") if overview else prose
        if not title_text.startswith("# "):
            findings.append(f"{name}: title missing at the start")
        header = "Scope" if overview else "(?:Originating Context|Module|Area)"
        if not re.search(r"^\|\s*\*\*" + header + r"\*\*\s*\|\s*\S.+\|\s*$", prose, re.M):
            findings.append(f"{name}: context header missing")
        prefix = PREFIX.search(prose)
        if overview:
            if DEFINITION.search(prose) or prefix:
                findings.append(f"{name}: overview must not define requirements or a prefix")
        elif not prefix:
            findings.append(f"{name}: prefix line missing")
        elif overviews and not any(re.search(r"\]\(" + re.escape(path) + r"(?:#[^)]*)?\)", prefix[2]) for path in overviews):
            findings.append(f"{name}: prefix line does not link the overview")

        headings = re.findall(r"^## (.+)$", prose, re.M)
        order = OVERVIEW_SECTIONS if overview else SECTIONS
        positions = [order.index(h) for h in headings if h in order]
        if positions != sorted(positions):
            findings.append(f"{name}: known sections out of order")
        for heading, count in Counter(headings).items():
            if count > 1:
                findings.append(f"{name}: duplicate section: {heading}")
            body = section(prose, heading).strip()
            if not body or re.fullmatch(r"None\.?|N/A\.?|Nenhum[ae]?\.?", body, re.I):
                findings.append(f"{name}: empty section: {heading}")
        if not overview:
            for heading in MANDATORY:
                if heading not in headings:
                    findings.append(f"{name}: mandatory section missing: {heading}")
        if "Weakest Point" in headings:
            after = headings[headings.index("Weakest Point") + 1:]
            if after not in ([], ["References"]):
                findings.append(f"{name}: only References may follow Weakest Point")
        for line in section(prose, "Declared Trade-offs").splitlines():
            if line.startswith("- ") and not ("*Cost:*" in line and "*Reason:*" in line):
                findings.append(f"{name}: trade-off without Cost/Reason")

        cited = set(ID_TOKEN.findall(text))
        for identifier in sorted(cited - definitions.keys()):
            if identifier.split("-", 1)[0] in prefix_owners:
                findings.append(f"{name}: citation {identifier} has no definition")
        for identifier in sorted(cited):
            if identifier.startswith(("FR-", "NFR-")):
                findings.append(f"{name}: unprefixed id {identifier}")
        for href in re.findall(r"\[[^\]]*\]\(([^)]+)\)", prose):
            href = href.strip().strip("<>")
            url = urlsplit(href)
            if url.scheme or url.netloc or not url.path:
                continue
            target = unquote(url.path)
            resolved = root / target.lstrip("/") if target.startswith("/") else folder / target
            if not resolved.exists():
                findings.append(f"{name}: local link does not resolve: {href}")
        if re.search(r"\b(?:TBD|TODO)\b", prose):
            findings.append(f"{name}: unresolved placeholder; use an explicit gap")
        if unclosed:
            findings.append(f"{name}: unclosed code fence")
        for language, body in blocks:
            if language == "mermaid":
                kind = body.strip().split(maxsplit=1)[0] if body.strip() else ""
                if kind not in {"stateDiagram-v2", "flowchart", "sequenceDiagram"}:
                    findings.append(f"{name}: unsupported or missing Mermaid diagram type: {kind}")
    if len(prefix_owners) > 1 and not overviews:
        findings.append("folder: multiple capability prefixes without an overview")
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", nargs="?", default="docs/prd")
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
