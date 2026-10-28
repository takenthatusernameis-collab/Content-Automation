#!/usr/bin/env python3
"""Generate a local visual plan draft from packet script.md sections.

Writes visual_plan_draft.md with section headers, estimated cumulative start
times at 150 wpm, suggested short card text from spoken content, and blank
slots for b-roll notes and card files. Human reviews and copies useful parts
into assets.md or editor notes.

No invented claims, no external services, no packet content edits by design.
Reduces recurring human labor of planning section-tied visuals and card texts
for every future packet once a script exists.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from phrase_utils import shorten
except ImportError:
    def shorten(text: str, max_len: int = 35) -> str:
        words = text.split()
        if not words:
            return ""
        out = []
        for w in words:
            if len(" ".join(out + [w])) > max_len:
                break
            out.append(w)
        return " ".join(out) or text[:max_len]

WPM = 150


def extract_spoken_sections(text: str) -> list[tuple[str, str]]:
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate local visual_plan_draft.md")
    parser.add_argument("packet", type=Path, help="Path to packet directory (must contain script.md)")
    parser.add_argument("--force", action="store_true", help="Overwrite existing visual_plan_draft.md")
    args = parser.parse_args()

    packet = args.packet.resolve()
    script_path = packet / "script.md"
    if not script_path.is_file():
        print(f"FAIL: script.md missing in {packet}", file=sys.stderr)
        return 2

    script_text = script_path.read_text(encoding="utf-8")
    sections = extract_spoken_sections(script_text)
    if not sections:
        print("FAIL: no spoken sections extracted from script.md", file=sys.stderr)
        return 2

    out_path = packet / "visual_plan_draft.md"
    if out_path.exists() and not args.force:
        print(f"SKIP: {out_path} exists (use --force to overwrite)")
        return 0

    lines = [
        "# Visual Plan Draft (local; review before copying to assets.md or editor notes)",
        "",
        "Status: draft",
        "Source: script.md spoken sections. No invented visuals or claims.",
        "Estimated times at 150 wpm. Card texts are short starters only.",
        "",
        "## Section-tied visual plan",
        "",
    ]

    cum = 0
    for i, (header, spoken) in enumerate(sections, 1):
        cnt = len(spoken.split()) if spoken else 0
        m, s = divmod(max(0, cum), 60)
        card_text = shorten(spoken, 35) if spoken else "(empty)"
        lines.extend([
            f"### {i}. {header} (est. {m}:{s:02d})",
            f"- Spoken preview: {spoken[:120]}{'...' if len(spoken) > 120 else ''}",
            f"- Suggested card text: {card_text}",
            "- broll_or_visual_note: (public-domain or original visual that supports the point; leave blank until decided)",
            "- card_file: (e.g. cards/NNN-section.png after generation with tools/card_generator.py)",
            "",
        ])
        cum += round(cnt / WPM * 60)

    lines.extend([
        "## Reminder",
        "- Prefer text-cards + public-domain notes per docs/assets.md.",
        "- Card text should stay short and readable (aim <=5 words).",
        "- Last 20 seconds of master reserved for YouTube end screen; do not place critical cards there.",
        "- Run tools/card_generator.py after deciding card texts.",
        "- Do not commit PNGs. This file is a local draft only.",
        "",
        "No media generated. Copy useful lines into assets.md when ready.",
    ])

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"WROTE: {out_path}")
    print(f"sections: {len(sections)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
