#!/usr/bin/env python3
"""Split a Whisper transcript (.txt, .srt or .vtt) into fixed-size chunks.

Deterministic on purpose: the orchestrating agent never reads or cuts the
full transcript itself. Every word of the source lands in exactly one chunk.

Outputs (under --out, default ./work):
  chunks/NN.txt          chunk text (SRT/VTT cues become "[HH:MM:SS] text" lines)
  chunks/NN.context.txt  tail of the previous chunk, read-only context (not for chunk 0)
  manifest.json          chunk list with word counts and time range

Usage:
  python split_transcript.py <transcript> [--out work] [--words 2500] [--context-words 150]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TIME_RE = re.compile(r"(?:(\d{1,2}):)?(\d{2}):(\d{2})[.,](\d{3})")
SENT_END_RE = re.compile(r"(?<=[.!?…])\s+")


def word_count(text: str) -> int:
    return len(text.split())


def parse_cues(raw: str) -> list[tuple[str, str]]:
    """Return [(start_hhmmss, text)] for SRT/VTT input."""
    cues: list[tuple[str, str]] = []
    block: list[str] = []
    for line in raw.splitlines() + [""]:
        if line.strip():
            block.append(line.rstrip())
            continue
        if block:
            cue = _cue_from_block(block)
            if cue:
                cues.append(cue)
            block = []
    return cues


def _cue_from_block(block: list[str]) -> tuple[str, str] | None:
    for i, line in enumerate(block):
        m = TIME_RE.search(line)
        if m and "-->" in line:
            text = " ".join(l.strip() for l in block[i + 1 :]).strip()
            text = re.sub(r"<[^>]+>", "", text)  # strip VTT tags
            if not text:
                return None
            return f"{int(m[1] or 0):02d}:{m[2]}:{m[3]}", text
    return None


def units_from_plain(raw: str) -> list[tuple[str | None, str]]:
    """Plain txt: sentence-ish units. Whisper txt may lack punctuation, so
    fall back to ~40-word pieces when a 'sentence' is too long."""
    units: list[tuple[str | None, str]] = []
    for para in re.split(r"\n\s*\n", raw):
        para = " ".join(para.split())
        if not para:
            continue
        for sent in SENT_END_RE.split(para):
            words = sent.split()
            if len(words) <= 60:
                units.append((None, sent))
            else:
                for i in range(0, len(words), 40):
                    units.append((None, " ".join(words[i : i + 40])))
    return units


def build_chunks(units: list[tuple[str | None, str]], target: int) -> list[list[tuple[str | None, str]]]:
    chunks: list[list[tuple[str | None, str]]] = []
    cur: list[tuple[str | None, str]] = []
    cur_words = 0
    for ts, text in units:
        w = word_count(text)
        if cur and cur_words + w > target:
            chunks.append(cur)
            cur, cur_words = [], 0
        cur.append((ts, text))
        cur_words += w
    if cur:
        chunks.append(cur)
    return chunks


def render(units: list[tuple[str | None, str]]) -> str:
    lines = [f"[{ts}] {text}" if ts else text for ts, text in units]
    return "\n".join(lines) + "\n"


def tail_words(text: str, n: int) -> str:
    words = text.split()
    return " ".join(words[-n:])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("transcript")
    ap.add_argument("--out", default="work")
    ap.add_argument("--words", type=int, default=2500, help="target words per chunk")
    ap.add_argument("--context-words", type=int, default=150, help="tail of previous chunk given as context")
    args = ap.parse_args()
    if args.words < 1 or args.context_words < 0:
        ap.error("--words must be positive and --context-words must be nonnegative")

    src = Path(args.transcript)
    raw = src.read_text(encoding="utf-8", errors="replace")
    fmt = src.suffix.lower().lstrip(".")

    if fmt in ("srt", "vtt"):
        units = parse_cues(raw)
        if not units:
            print(f"error: no cues parsed from {src}", file=sys.stderr)
            return 2
    else:
        fmt = "txt"
        units = units_from_plain(raw)

    if not units:
        print(f"error: empty transcript: {src}", file=sys.stderr)
        return 2

    out = Path(args.out)
    chunk_dir = out / "chunks"
    chunk_dir.mkdir(parents=True, exist_ok=True)
    for stale in chunk_dir.glob("*.txt"):
        stale.unlink()

    chunks = build_chunks(units, args.words)
    manifest = {
        "source": str(src),
        "format": fmt,
        "target_words": args.words,
        "context_words": args.context_words,
        "source_words": sum(word_count(t) for _, t in units),
        "chunks": [],
    }
    prev_text = ""
    for i, ch in enumerate(chunks):
        text = render(ch)
        path = chunk_dir / f"{i:02d}.txt"
        path.write_text(text, encoding="utf-8")
        entry = {
            "id": i,
            "file": str(path),
            "words": sum(word_count(t) for _, t in ch),
            "start": ch[0][0],
            "end": ch[-1][0],
            "context_file": None,
        }
        if i > 0 and args.context_words:
            ctx = chunk_dir / f"{i:02d}.context.txt"
            ctx.write_text(tail_words(prev_text, args.context_words) + "\n", encoding="utf-8")
            entry["context_file"] = str(ctx)
        manifest["chunks"].append(entry)
        prev_text = " ".join(t for _, t in ch)

    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"{len(chunks)} chunks, {manifest['source_words']} words, format={fmt} -> {out}/manifest.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
