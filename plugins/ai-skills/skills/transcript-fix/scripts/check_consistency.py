#!/usr/bin/env python3
"""Check a merged transcript against the glossary.

Reports two things independent subagents get wrong without noticing:
  leftover   a wrong form from a confirmed / evidence-A entry still appears
  spelling   the same term written differently in different chunks
             (e.g. "trade-off" vs "tradeoff" vs "Trade Off")

Usage:
  python check_consistency.py --glossary glossary.json --text output/aula-01.fixed.txt
Exit code 1 if anything is found.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


def norm(term: str) -> str:
    return re.sub(r"[^a-z0-9]", "", term.lower())


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--glossary", required=True)
    ap.add_argument("--text", required=True)
    args = ap.parse_args()

    entries = json.loads(Path(args.glossary).read_text(encoding="utf-8"))
    text = Path(args.text).read_text(encoding="utf-8")
    # Explicit uncertainties are delivered in .uncertain.md for contextual review.
    # They must not be forced into a global confirmed mapping by repair workers.
    uncertain_forms = {form for e in entries for form in [e.get("correct", ""), *e.get("variants", [])] if form}
    for form in sorted(uncertain_forms, key=len, reverse=True):
        text = re.sub(r"(?<!\w)" + re.escape(form) + r"(?!\w)[ \t]+\[\?\]", " ", text, flags=re.IGNORECASE)
    problems = 0

    strong = [e for e in entries if e.get("correct") and (e.get("confirmed") or e.get("evidence") == "A")]
    # blank out correct terms first so a variant that is a substring of its own
    # correction ("evans" inside "Eric Evans") is not reported as leftover
    masked = text
    for e in sorted(strong, key=lambda e: -len(e["correct"])):
        masked = re.sub(r"(?<!\w)" + re.escape(e["correct"]) + r"(?!\w)", " ", masked, flags=re.IGNORECASE)
    for e in strong:
        for v in e["variants"]:
            n = len(re.findall(r"(?<!\w)" + re.escape(v) + r"(?!\w)", masked, flags=re.IGNORECASE))
            if n:
                problems += n
                print(f"leftover  {v!r} x{n}  (expected {e['correct']!r})")

    # spelling drift: any surface form whose normalization equals a glossary term
    targets = {norm(e["correct"]): e["correct"] for e in entries if e.get("correct")}
    max_words = max((len(c.split()) for c in targets.values()), default=1)
    tokens = re.findall(r"[\w][\w\-./+#]*", text)
    seen: dict[str, Counter] = defaultdict(Counter)
    for n in range(1, max_words + 1):
        for i in range(len(tokens) - n + 1):
            surface = " ".join(tokens[i : i + n])
            key = norm(surface)
            if key in targets:
                seen[key][surface] += 1
    for key, forms in seen.items():
        if len(forms) > 1:
            problems += 1
            listing = ", ".join(f"{f!r} x{c}" for f, c in forms.most_common())
            print(f"spelling  {targets[key]!r}: {listing}")

    print(f"{problems} issue(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
