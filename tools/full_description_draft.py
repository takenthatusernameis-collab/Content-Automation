#!/usr/bin/env python3
"""Assemble a paste-ready YouTube description from packet files.

Combines a short operational summary extracted from script.md spoken content,
an estimated chapters list from ## sections + following spoken text at 150 wpm,
and a calm close. Writes a local description_draft.txt.
No invented claims, no external services.
Reduces recurring human labor of assembling the full description block
(summary + chapters + close) for Studio or publish.md on every future packet.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    from phrase_utils import shorten
except ImportError:
    def shorten(text: str, max_len: int = 140) -> str:
        return text[:max_len]

WPM = 150


def extract_spoken_sections(text: str) -> list[tuple[str, str]]:
    """Extract (header, spoken_text) pairs, capturing content after WORDS: until VISUAL or next ##."""
    sections: list[tuple[str, str]] = []
    current_header = None
    capturing = False
    current_lines: list[str] = []

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("##"):
            if current_header is not None and current_lines:
                spoken = " ".join(current_lines).strip()
                sections.append((current_header, spoken))
            current_header = stripped.lstrip("#").strip()
            current_lines = []
            capturing = False
            continue
        if current_header is None:
            continue
        if stripped.startswith("WORDS"):
            capturing = True
            continue
        if stripped.startswith("VISUAL") or stripped.startswith("*"):
            capturing = False
            continue
        if capturing and stripped:
            current_lines.append(stripped)

    if current_header is not None and current_lines:
        spoken = " ".join(current_lines).strip()
        sections.append((current_header, spoken))
    return sections


def extract_summary(sections: list[tuple[str, str]], max_sents: int = 2) -> str:
    """Build short operational summary from early spoken sections."""
    texts = []
    for header, spoken in sections:
        if not spoken:
            continue
        # Prefer Hook / Payoff / early beats
        if any(k in header.lower() for k in ("hook", "payoff", "beat 1", "intro")):
            texts.append(spoken)
            if len(texts) >= 1:
                break
    if not texts and sections:
        texts = [sections[0][1]]
    full = " ".join(texts)
    sents = re.split(r"(?<=[.!?])\s+", full.strip())
    chosen = []
    for s in sents:
        s = s.strip()
        if len(s) > 25:
            chosen.append(shorten(s, 160))
            if len(chosen) >= max_sents:
                break
    if not chosen:
        chosen = [shorten(full, 180)]
    return " ".join(chosen)


def chapters_block(sections: list[tuple[str, str]]) -> str:
    out = ["# Estimated chapters (150 wpm from section spoken text)"]
    cum = 0
    for header, spoken in sections:
        cnt = len(spoken.split()) if spoken else 0
        m, s = divmod(max(0, cum), 60)
        out.append(f"{m}:{s:02d} {header} ({cnt} words)")
        cum += round(cnt / WPM * 60)
    total_m, total_s = divmod(cum, 60)
    out.append("")
    out.append(f"# Total estimated: {total_m}:{total_s:02d}")
    return "\n".join(out)


def main() -> int:
    p = argparse.ArgumentParser(description="Assemble paste-ready description from packet")
    p.add_argument("packet", type=Path, help="Path to video packet folder")
    p.add_argument("--out", type=Path, default=None, help="Optional output path")
    args = p.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"ERROR: not a directory: {packet}", file=sys.stderr)
        return 1

    script = packet / "script.md"
    if not script.is_file():
        print("ERROR: script.md missing", file=sys.stderr)
        return 1

    script_text = script.read_text(encoding="utf-8")
    sections = extract_spoken_sections(script_text)
    if not sections:
        print("WARNING: no spoken sections extracted", file=sys.stderr)

    summary = extract_summary(sections)
    chapters = chapters_block(sections)

    lines = [
        "# Description draft (local; review before paste)",
        "",
        summary,
        "",
        chapters,
        "",
        "Write the next-action sentence tonight. Use it tomorrow before any list.",
        "",
        "# Draft only — human confirms voice and accuracy before publishing.",
    ]
    out_text = "\n".join(lines) + "\n"

    out_path = args.out or (packet / "description_draft.txt")
    out_path.write_text(out_text, encoding="utf-8")

    print(out_text)
    print(f"wrote: {out_path}")
    print(f"sections_extracted: {len(sections)}")
    print("Description draft ready (local; gitignore if desired).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
