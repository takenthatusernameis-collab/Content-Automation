#!/usr/bin/env python3
"""Generate a local read-aloud flags pack from script.md spoken WORDS.

Extracts sentences from WORDS blocks, flags long sentences (>22 words),
sentences with numbers, and provides simple break suggestions.
Writes read_aloud_flags.md for VO preparation.

No invented content. Output stays local and gitignored. Reduces recurring
human labor of scanning for dense or number-heavy passages before recording
on every future packet before a Selected VO take exists.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

MAX_WORDS = 22
WPM = 150

def extract_spoken_blocks(text: str) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []
    pattern = re.compile(r"^##\s+(.+?)\s*$", re.M)
    matches = list(pattern.finditer(text))
    for i, m in enumerate(matches):
        header = m.group(1).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[start:end]
        wm = re.search(r"WORDS:\s*(.*?)(?:\nVISUAL:|\n##|\Z)", block, re.S | re.I)
        if wm:
            spoken = wm.group(1).strip()
            spoken = re.sub(r"\s+", " ", spoken)
            if spoken:
                sections.append((header, spoken))
    return sections

def split_sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+', text.strip()) if s.strip()]

def find_numbers(text: str) -> list[str]:
    return re.findall(r"\b\d+(?:\.\d+)?%?\b", text)

def main() -> int:
    p = argparse.ArgumentParser(description="Generate read-aloud flags from script.md")
    p.add_argument("packet", type=Path, help="Path to packet directory")
    p.add_argument("--force", action="store_true", help="Overwrite existing read_aloud_flags.md")
    args = p.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"ERROR: not a directory: {packet}", file=sys.stderr)
        return 1

    script_path = packet / "script.md"
    if not script_path.is_file():
        print("FAIL: script.md missing", file=sys.stderr)
        return 2

    out_path = packet / "read_aloud_flags.md"
    if out_path.exists() and not args.force:
        print(f"SKIP: {out_path} exists (use --force to overwrite)")
        return 0

    text = script_path.read_text(encoding="utf-8")
    blocks = extract_spoken_blocks(text)
    if not blocks:
        print("FAIL: no spoken WORDS found in script.md", file=sys.stderr)
        return 2

    lines: list[str] = [
        "# Read-Aloud Flags",
        "",
        "Generated locally from script.md WORDS blocks. Flags for recording prep.",
        "Not a rewrite. Review flagged sentences for breath points or simplification.",
        "",
    ]

    flags: list[str] = []
    total_long = 0
    total_num = 0

    for idx, (header, spoken) in enumerate(blocks, 1):
        sents = split_sentences(spoken)
        for sent in sents:
            wc = len(sent.split())
            nums = find_numbers(sent)
            reasons = []
            if wc > MAX_WORDS:
                reasons.append(f"long ({wc} words)")
                total_long += 1
            if nums:
                reasons.append(f"numbers: {', '.join(nums)}")
                total_num += 1
            if reasons:
                flags.append(f"- **{header}**: {sent}")
                flags.append(f"  Flags: {'; '.join(reasons)}")
                if wc > MAX_WORDS:
                    # Suggest a mid-point roughly
                    words = sent.split()
                    mid = len(words) // 2
                    flags.append(f"  Suggested pause after ~{mid} words: \"{' '.join(words[:mid])}...\"")
                flags.append("")

    if not flags:
        lines.append("No strong flags. Sentences are short and number-free.")
        lines.append("")
    else:
        lines.append(f"## Flags ({total_long} long, {total_num} with numbers)")
        lines.append("")
        lines.extend(flags)

    lines.append("---")
    lines.append("Use with vo_prep.md for recording. Do not treat as edited script.")

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"WROTE: {out_path}")
    print(f"long_sentences: {total_long}")
    print(f"number_sentences: {total_num}")
    print("Read-aloud flags ready (local).")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
