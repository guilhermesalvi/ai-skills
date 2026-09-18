#!/usr/bin/env python3
"""Maintain the persistent term glossary (glossary.json) across sessions.

Entry schema:
  {
    "correct": "trade-off",               # canonical spelling
    "variants": ["tredófi", "trade of"],  # wrong forms seen in transcripts
    "evidence": "A" | "B" | "C",          # A = context settles it, B = probable, C = unknown
    "occurrences": 12,
    "example": "…um tredófi entre latência e…",
    "confirmed": false                    # set by the human; never downgraded afterwards
  }

Subcommands:
  merge   --glossary glossary.json --candidates work/candidates/*.json
          Merge per-chunk candidate files (same schema, list of entries) into the glossary.
          Add --receipt work/glossary.merge.json for recoverable, idempotent retries.
          Shared glossaries require one coordinator writer at a time.
  render  --glossary glossary.json [--out glossary.md] [--min-evidence A|B|C]
          Write a markdown table for humans and for the fix prompt.
  confirm --glossary glossary.json --term "trade-off" [--term ...]
          Mark entries as human-confirmed (evidence A).
  reject  --glossary glossary.json --term "foo"
          Remove entries the human rejected.
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path

RANK = {"A": 0, "B": 1, "C": 2}


def norm(term: str) -> str:
    return re.sub(r"[^a-z0-9]", "", term.lower())


def load(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, entries: list[dict]) -> None:
    entries.sort(key=lambda e: (RANK.get(e.get("evidence", "C"), 2), -e.get("occurrences", 0), e["correct"].lower()))
    atomic_json(path, entries)


def atomic_json(path: Path, value: object) -> None:
    """Replace a JSON file only after its complete contents are on disk."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(json.dumps(value, indent=2, ensure_ascii=False) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def merge_with_receipt(path: Path, candidates: list[dict], receipt: Path) -> str:
    """Recover an interrupted single-writer merge without adding counts twice."""
    digest = hashlib.sha256(json.dumps(candidates, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()
    current = load(path)
    if receipt.exists():
        record = json.loads(receipt.read_text(encoding="utf-8"))
        if record["candidates_hash"] != digest:
            raise ValueError("candidate batch changed; use a new receipt after reconciliation")
    else:
        # merge mutates entries, so retain an independent before-image for recovery.
        after, _ = merge(json.loads(json.dumps(current)), candidates)
        after.sort(key=lambda e: (RANK.get(e.get("evidence", "C"), 2), -e.get("occurrences", 0), e["correct"].lower()))
        record = {"candidates_hash": digest, "before": current, "after": after}
        atomic_json(receipt, record)
    if current == record["after"]:
        return "already applied"
    if current != record["before"]:
        raise ValueError("glossary changed since this batch; reconcile before retrying")
    atomic_json(path, record["after"])
    return "applied"


def merge(glossary: list[dict], candidates: list[dict]) -> tuple[list[dict], int]:
    by_key = {_key(e): e for e in glossary if e.get("correct") or e.get("variants")}
    added = 0
    for c in candidates:
        correct = (c.get("correct") or "").strip()
        variants = [v.strip() for v in c.get("variants", []) if v and v.strip()]
        if not correct and not variants:
            continue
        e = by_key.get(norm(correct)) if correct else None
        if e is None:
            # an entry that already lists one of these wrong forms (typically an
            # open "?" entry from an evidence-C candidate) absorbs this one
            e = _find_by_variant(by_key, variants)
            if e is not None and correct and not e["correct"]:
                del by_key[_key(e)]
                e["correct"] = correct
                by_key[_key(e)] = e
        if e is None:
            e = {"correct": correct, "variants": [], "evidence": "C", "occurrences": 0,
                 "example": c.get("example", ""), "confirmed": False}
            added += 1
        for v in variants:
            if v.lower() not in {x.lower() for x in e["variants"]} and v.lower() != e["correct"].lower():
                e["variants"].append(v)
        by_key.setdefault(_key(e), e)
        e["occurrences"] = e.get("occurrences", 0) + int(c.get("occurrences", 1) or 1)
        ev = (c.get("evidence") or "C").upper()[:1]
        if e["correct"] and not e.get("confirmed") and RANK.get(ev, 2) < RANK.get(e["evidence"], 2):
            e["evidence"] = ev
        if not e.get("example") and c.get("example"):
            e["example"] = c["example"]
    return list(by_key.values()), added


def _key(e: dict) -> str:
    return norm(e["correct"]) if e.get("correct") else "?" + norm(e["variants"][0])


def _find_by_variant(by_key: dict, variants: list[str]) -> dict | None:
    wanted = {v.lower() for v in variants}
    for e in by_key.values():
        if wanted & {x.lower() for x in e["variants"]}:
            return e
    return None


def render(entries: list[dict], min_evidence: str) -> str:
    rows = [e for e in entries if RANK.get(e.get("evidence", "C"), 2) <= RANK[min_evidence]]
    out = ["| Wrong forms seen | Correct | Evidence | Count | Example |", "|---|---|---|---|---|"]
    for e in rows:
        ev = e["evidence"] + (" (confirmed)" if e.get("confirmed") else "")
        variants = ", ".join(e["variants"]) or "—"
        example = (e.get("example") or "").replace("|", "\\|")
        out.append(f"| {variants} | {e['correct'] or '?'} | {ev} | {e.get('occurrences', 0)} | {example} |")
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    m = sub.add_parser("merge")
    m.add_argument("--glossary", required=True)
    m.add_argument("--candidates", nargs="+", required=True, help="files or globs")
    m.add_argument("--receipt", help="run-specific recovery receipt; makes this batch safe to retry")

    r = sub.add_parser("render")
    r.add_argument("--glossary", required=True)
    r.add_argument("--out")
    r.add_argument("--min-evidence", default="C", choices=["A", "B", "C"])

    for name in ("confirm", "reject"):
        p = sub.add_parser(name)
        p.add_argument("--glossary", required=True)
        p.add_argument("--term", action="append", required=True)

    args = ap.parse_args()
    gpath = Path(args.glossary)
    entries = load(gpath)

    if args.cmd == "merge":
        files = sorted({f for pat in args.candidates for f in glob.glob(pat)})
        if not files:
            ap.error("no candidate files matched")
        cands: list[dict] = []
        for f in files:
            data = json.loads(Path(f).read_text(encoding="utf-8"))
            if isinstance(data, dict):
                data = data.get("candidates", [])
            cands.extend(data)
        if args.receipt:
            receipt = Path(args.receipt)
            if receipt.resolve() == gpath.resolve():
                ap.error("receipt must differ from glossary")
            try:
                status = merge_with_receipt(gpath, cands, receipt)
            except ValueError as error:
                print(f"error: {error}", file=sys.stderr)
                return 1
            print(f"batch {status}: {len(cands)} candidates -> {gpath}")
            return 0
        entries, added = merge(entries, cands)
        save(gpath, entries)
        print(f"merged {len(cands)} candidates from {len(files)} files: {added} new, {len(entries)} total -> {gpath}")
        return 0

    if args.cmd == "render":
        text = render(entries, args.min_evidence)
        if args.out:
            Path(args.out).write_text(text, encoding="utf-8")
            print(f"wrote {args.out}")
        else:
            sys.stdout.write(text)
        return 0

    wanted = {norm(t) for t in args.term}
    if args.cmd == "confirm":
        hit = 0
        for e in entries:
            if norm(e["correct"]) in wanted:
                e["confirmed"], e["evidence"] = True, "A"
                hit += 1
        save(gpath, entries)
        print(f"confirmed {hit} of {len(wanted)}")
        return 0 if hit == len(wanted) else 1

    before = len(entries)
    entries = [e for e in entries if norm(e["correct"]) not in wanted]
    save(gpath, entries)
    print(f"rejected {before - len(entries)} of {len(wanted)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
