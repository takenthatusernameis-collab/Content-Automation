#!/usr/bin/env python3
"""Generate a local default-placement note from idea.md (and optional script CTA).

Extracts mechanism and problem, then suggests 1-2 concrete places the default
should live based on keywords already present in the problem or mechanism text.
Writes a paste-ready default_placement_note.md with a short spoken sentence
template.

Aligns with channel voice: name the stall, name the default, tell the viewer
where it lives. No invented mechanisms or claims. Output stays local and
gitignored. Reduces recurring human labor of deciding the placement sentence
for the script, description, or end card on every future packet.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from idea_utils import extract as idea_extract  # noqa: E402


def suggest_placements(problem: str, mech: str) -> list[str]:
    """Return 1-2 grounded placement suggestions from existing words only."""
    text = f"{problem} {mech}".lower()
    suggestions: list[str] = []

    if any(k in text for k in ("list", "lists", "todo", "to-do")):
        suggestions.append("On the list itself (or the note next to the list you already open).")
    if any(k in text for k in ("tab", "tabs", "browser", "extra tab")):
        suggestions.append("In the browser bar or on the tab that is still open.")
    if any(k in text for k in ("file", "document", "doc", "spreadsheet")):
        suggestions.append("In the file name, header, or first line of the work file.")
    if any(k in text for k in ("desk", "notebook", "paper", "calendar")):
        suggestions.append("On the desk or calendar page you already see when the stall starts.")
    if any(k in text for k in ("app", "application", "tool")):
        suggestions.append("Inside the app that absorbs the delay (sidebar, title, or first screen).")
    if any(k in text for k in ("morning", "start", "first")):
        suggestions.append("Where your eyes land in the first two minutes of the morning.")

    # Always offer one generic grounded fallback if nothing matched
    if not suggestions:
        suggestions.append("Where your cursor or eyes already land when the stall starts.")

    return suggestions[:2]


def extract_cta_spoken(text: str) -> str:
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
            spoken = re.sub(r"\s+", " ", wm.group(1).strip())
            if spoken:
                sections.append((header, spoken))
    if not sections:
        return ""
    for header, spoken in sections:
        if re.search(r"cta|call.to.action|end|install|default", header, re.I):
            return spoken
    return sections[-1][1]


def main() -> int:
    p = argparse.ArgumentParser(description="Generate default placement note from packet")
    p.add_argument("packet", type=Path, help="Path to packet directory")
    p.add_argument("--force", action="store_true", help="Overwrite existing default_placement_note.md")
    args = p.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"ERROR: not a directory: {packet}", file=sys.stderr)
        return 1

    idea_path = packet / "idea.md"
    if not idea_path.is_file():
        print("FAIL: idea.md missing", file=sys.stderr)
        return 2

    out_path = packet / "default_placement_note.md"
    if out_path.exists() and not args.force:
        print(f"SKIP: {out_path} exists (use --force to overwrite)")
        return 0

    idea_text = idea_path.read_text(encoding="utf-8")
    mech, problem, topic = idea_extract(idea_text)

    if not mech and not problem:
        print("FAIL: no mechanism or problem found in idea.md", file=sys.stderr)
        return 2

    placements = suggest_placements(problem, mech)

    cta = ""
    script_path = packet / "script.md"
    if script_path.is_file():
        cta = extract_cta_spoken(script_path.read_text(encoding="utf-8"))

    lines = [
        "# Default Placement Note",
        "",
        "Generated locally from idea.md mechanism/problem (and script.md CTA if present).",
        "Channel voice: name the stall, name the default, tell the viewer where it lives.",
        "Not a rewrite. Review and paste into script, description, or end card.",
        "",
        f"- Topic: {topic or '(none)'}",
        f"- Problem: {problem or '(none)'}",
        f"- Mechanism / default: {mech or '(none)'}",
        "",
        "## Where the default lives",
        "",
    ]
    for i, place in enumerate(placements, 1):
        lines.append(f"{i}. {place}")
    lines.append("")

    # Short spoken sentence template grounded in extracted fields
    spoken_parts = []
    if problem:
        spoken_parts.append(f"The stall is {problem}.")
    if mech:
        spoken_parts.append(f"The default is {mech}.")
    if placements:
        spoken_parts.append(f"It lives {placements[0].rstrip('.')}.")
    if spoken_parts:
        lines.append("## Short spoken sentence (template)")
        lines.append("")
        lines.append(" ".join(spoken_parts))
        lines.append("")

    if cta:
        lines.append("## CTA spoken text (for alignment)")
        lines.append("")
        lines.append(cta)
        lines.append("")

    lines.extend([
        "---",
        "Use one of the placements above. Do not invent a new location or default.",
    ])

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"WROTE: {out_path}")
    print(f"placements: {len(placements)}")
    print(f"mech_found: {bool(mech)}")
    print(f"problem_found: {bool(problem)}")
    print("Default placement note ready (local; estimated from packet fields only).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
