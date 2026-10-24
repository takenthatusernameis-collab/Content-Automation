#!/usr/bin/env python3
"""Visual cues brief from script.md or draft.md.

Extracts VISUAL / card needs per beat (via the same parsing logic used by
asset_brief.py when available) and prints a compact list for asset planning.
Reduces recurring manual scanning of script VISUAL lines before every card
generation or editor session. Does not invent content, rewrite files, or
call external services.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

try:
    from asset_brief import script_cards, visual_text, section  # type: ignore
except Exception:
    script_cards = None  # type: ignore
    visual_text = None
    section = None


def fallback_extract(text: str) -> list[dict[str, str]]:
    """Simple fallback when asset_brief helpers are unavailable."""
    results = []
    parts = re.split(r"^##[ \t]+", text, flags=re.M)
    for part in parts[1:]:
        lines = part.splitlines()
        if not lines:
            continue
        title = lines[0].strip()
        body = "\n".join(lines[1:])
        m = re.search(r"VISUAL:\s*(.*?)(?:WORDS:|ON SCREEN:|\Z)", body, re.S | re.I)
        if m:
            need = re.sub(r"\s+", " ", m.group(1)).strip()
            if need:
                results.append({"beat": title, "need": need})
    return results


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print visual / card needs from script. No file writes."
    )
    parser.add_argument("packet", help="Packet folder under videos/")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    script = path / "script.md"
    draft = path / "draft.md"
    source = script if script.is_file() else draft
    if not source.is_file():
        print(f"No script.md or draft.md in {path}", file=sys.stderr)
        return 1

    text = source.read_text(encoding="utf-8")

    print("VISUAL CUES BRIEF (from script VISUAL lines; not proof cards exist)")
    print(f"Source: {source.name}")
    print(f"Packet: {path.name}")
    print()

    cards = []
    if script_cards is not None:
        try:
            cards = script_cards(text)
        except Exception:
            cards = []

    if not cards:
        cards = fallback_extract(text)

    if not cards:
        print("No VISUAL cues found. Add VISUAL: lines under beat headings.")
        print("This tool writes nothing.")
        return 0

    print("| Beat | Visual need |")
    print("|------|-------------|")
    for c in cards:
        beat = c.get("beat", "")[:40]
        need = c.get("need", "")[:80].replace("|", "/")
        print(f"| {beat} | {need} |")

    print()
    print(f"Found {len(cards)} visual cue(s).")
    print("Use for planning cards/ or running asset_brief.py --dry-run.")
    print("Actual card files are created by the editor or card_generator.py.")
    print("This tool writes nothing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
