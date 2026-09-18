#!/usr/bin/env python3
"""Merge corrected chunks back into one transcript and validate integrity.

Expects, for every chunk in manifest.json:
  work/fixed/NN.txt            corrected text only (no headers, no commentary)
  work/fixed/NN.changes.json   required: [{"original": "...", "corrected": "...", "evidence": "A|B|C", "count": 1}]

Writes:
  <out>/<name>.fixed.txt       merged transcript
  <out>/<name>.changes.md      all substitutions, grouped and counted
  <out>/<name>.uncertain.md    every line containing "[?]", with chunk id and timestamp
  <out>/<name>.report.json     per-chunk checks; exit code 1 if any check fails

Checks (a failed check means a subagent truncated, padded, or leaked context —
the errors that are invisible when you just read the merged text):
  missing     fixed/NN.txt does not exist or is empty
  drift       |fixed words / source words - 1| > --tolerance (default 0.08)
  leak        the fixed text starts with the read-only context tail
  timestamps  (srt/vtt only) sequence of [HH:MM:SS] markers changed
  changes     required change log is missing or has an invalid schema

Usage:
  python merge_chunks.py --work work --out output --name aula-01 [--tolerance 0.08]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

TS_RE = re.compile(r"^\[(\d{2}:\d{2}:\d{2})\]")
TS_ANY_RE = re.compile(r"\[\d{2}:\d{2}:\d{2}\]")


def words(text: str) -> list[str]:
    """Words excluding [HH:MM:SS] markers, so timestamps never count as drift."""
    return TS_ANY_RE.sub("", text).split()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--work", default="work")
    ap.add_argument("--out", default="output")
    ap.add_argument("--name", required=True)
    ap.add_argument("--tolerance", type=float, default=0.08)
    args = ap.parse_args()

    work = Path(args.work)
    manifest = json.loads((work / "manifest.json").read_text(encoding="utf-8"))
    fixed_dir = work / "fixed"
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    merged: list[str] = []
    uncertain: list[str] = []
    changes: Counter = Counter()
    change_evidence: dict[tuple[str, str], str] = {}
    report = {"chunks": [], "ok": bool(manifest["chunks"])}
    if not manifest["chunks"]:
        report["problems"] = ["empty_manifest"]

    for ch in manifest["chunks"]:
        cid = ch["id"]
        fpath = fixed_dir / f"{cid:02d}.txt"
        entry = {"id": cid, "problems": []}
        if not fpath.exists() or not fpath.read_text(encoding="utf-8").strip():
            entry["problems"].append("missing")
            report["chunks"].append(entry)
            report["ok"] = False
            continue

        text = fpath.read_text(encoding="utf-8").strip() + "\n"
        src_text = Path(ch["file"]).read_text(encoding="utf-8")

        fw, sw = len(words(text)), len(words(src_text))
        entry["source_words"], entry["fixed_words"] = sw, fw
        drift = fw / sw - 1 if sw else 0.0
        entry["drift"] = round(drift, 3)
        if abs(drift) > args.tolerance:
            entry["problems"].append("drift")

        if ch.get("context_file"):
            ctx = Path(ch["context_file"]).read_text(encoding="utf-8").split()
            head = " ".join(words(text)[: len(ctx) + 40]).lower()
            if len(ctx) >= 12 and " ".join(ctx[:12]).lower() in head:
                entry["problems"].append("leak")

        if manifest["format"] in ("srt", "vtt"):
            src_markers = TS_ANY_RE.findall(src_text)
            fixed_markers = TS_ANY_RE.findall(text)
            entry["timestamps"] = {"source": len(src_markers), "fixed": len(fixed_markers)}
            if src_markers != fixed_markers:
                entry["problems"].append("timestamps")

        for line in text.splitlines():
            if "[?]" in line:
                m = TS_RE.match(line)
                tag = f"chunk {cid:02d}" + (f" @ {m[1]}" if m else "")
                uncertain.append(f"- ({tag}) {line.strip()}")

        cpath = fixed_dir / f"{cid:02d}.changes.json"
        if cpath.exists():
            try:
                records = json.loads(cpath.read_text(encoding="utf-8"))
                if not isinstance(records, list) or any(
                    not isinstance(c, dict)
                    or not isinstance(c.get("original"), str) or not c["original"].strip()
                    or not isinstance(c.get("corrected"), str) or not c["corrected"].strip()
                    or c.get("evidence") not in ("A", "B", "C")
                    or type(c.get("count")) is not int or c["count"] < 1
                    for c in records
                ):
                    raise ValueError("invalid change log schema")
                for c in records:
                    key = (c["original"].strip(), c["corrected"].strip())
                    changes[key] += c["count"]
                    change_evidence.setdefault(key, c["evidence"])
            except (ValueError, UnicodeError):
                entry["problems"].append("changes_json_invalid")
        else:
            entry["problems"].append("changes_missing")

        merged.append(text)
        if entry["problems"]:
            report["ok"] = False
        report["chunks"].append(entry)

    (out / f"{args.name}.fixed.txt").write_text("\n".join(merged), encoding="utf-8")

    lines = ["| Original | Corrected | Evidence | Count |", "|---|---|---|---|"]
    for (o, c), n in changes.most_common():
        lines.append(f"| {o} | {c} | {change_evidence.get((o, c), '')} | {n} |")
    (out / f"{args.name}.changes.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    (out / f"{args.name}.uncertain.md").write_text(
        (f"# Uncertain passages ({len(uncertain)})\n\n" + "\n".join(uncertain) + "\n") if uncertain else "# Uncertain passages (0)\n",
        encoding="utf-8",
    )

    report["source_words"] = manifest["source_words"]
    report["fixed_words"] = sum(len(words(t)) for t in merged)
    report["uncertain"] = len(uncertain)
    (out / f"{args.name}.report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    bad = [c for c in report["chunks"] if c["problems"]]
    print(f"chunks: {len(manifest['chunks'])}, failed: {len(bad)}, words {report['source_words']} -> {report['fixed_words']}, uncertain: {len(uncertain)}")
    for c in bad:
        print(f"  chunk {c['id']:02d}: {', '.join(c['problems'])}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
