#!/usr/bin/env python3
"""Write a local thumbnail_options.md with grounded on-image text candidates.

Extracts mechanism/problem/topic from idea.md (or prefers shortened primary from
assignment_source.md when present) and emits structured thumbnail_options.md with
4 short on-image text candidates. Uses shared phrase_utils.shorten for natural
breaks. No invented claims. Output stays local (gitignored).
Provides consistent, mechanism-aligned thumbnail text options that future
thumbnail generators or human edits can prefer. Reduces drift and manual
shortening labor for on-image text. Aligns with no-invent rule and CTR
readability goals (short, concrete, promise-aligned).
Not a final thumbnail text; select one for thumbnail.md or generator.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from idea_utils import extract as idea_extract  # noqa: E402
from phrase_utils import shorten  # noqa: E402


def read_assignment_primary(packet: Path) -> str | None:
    """Prefer the primary assignment statement from assignment_source.md if present."""
    src = packet / "assignment_source.md"
    if not src.is_file():
        return None
    text = src.read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.startswith("Install the ") or "Primary assignment statement" in line:
            continue
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and not stripped.startswith("-") and len(stripped) > 10:
            # Rough: take the first substantial non-header line after the section
            if "stops reopening" in stripped or "Install" in stripped:
                return stripped
    return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Write local thumbnail_options.md with short on-image candidates"
    )
    parser.add_argument("packet", type=Path, help="Packet directory")
    parser.add_argument("--force", action="store_true", help="Overwrite existing file")
    args = parser.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"FAIL: not a directory: {packet}", file=sys.stderr)
        return 1

    idea_path = packet / "idea.md"
    if not idea_path.is_file():
        print("FAIL: idea.md missing", file=sys.stderr)
        return 2

    out_path = packet / "thumbnail_options.md"
    if out_path.exists() and not args.force:
        print(f"SKIP: {out_path} exists (use --force to overwrite)")
        return 0

    idea_text = idea_path.read_text(encoding="utf-8")
    mech, problem, topic = idea_extract(idea_text)

    if not mech and not problem:
        print("FAIL: no mechanism or problem found in idea.md", file=sys.stderr)
        return 2

    # Prefer assignment source primary if available for tighter consistency
    primary_from_src = read_assignment_primary(packet)
    short_mech = shorten(mech or "the written next-action default", 28)
    short_problem = shorten(problem or "the stall", 22)
    short_topic = shorten(topic or "focused work", 20)

    if primary_from_src:
        base_short = shorten(primary_from_src, 36)
        source_note = "preferred from assignment_source.md"
    else:
        base_short = short_mech
        source_note = "from idea.md mechanism"

    candidates = [
        base_short,
        f"Install {short_mech}",
        f"Stop {short_problem}",
        f"{short_mech} today",
    ]

    # Dedup and keep short
    seen = set()
    unique = []
    for c in candidates:
        low = c.lower().strip()
        if low and low not in seen and len(c.split()) <= 6:
            seen.add(low)
            unique.append(c.strip())
    candidates = unique[:4]

    lines = [
        "# Thumbnail Options (local; grounded short on-image text)",
        "",
        "Generated locally from idea.md (preferring assignment_source.md primary when present).",
        "Four short on-image text candidates for thumbnails. No invented claims.",
        f"Source preference: {source_note}.",
        "Uses shared phrase_utils.shorten for natural breaks.",
        "Channel voice: calm, specific, operational. Short enough for readable on-image text.",
        "Not a final thumbnail text. Select one for thumbnail.md or tools/thumbnail_generator.py.",
        "",
        f"- Topic: {topic or '(none)'}",
        f"- Problem / stall (short): {short_problem}",
        f"- Mechanism / default (short): {short_mech}",
        "",
        "## Candidates (prefer shortest readable)",
        "",
    ]
    for i, cand in enumerate(candidates, 1):
        lines.append(f"{i}. {cand}  ({len(cand.split())} words)")
    lines.extend([
        "",
        "## Notes",
        "- Prefer the shortest version that still names the concrete default or stall.",
        "- Aligns with on-image readability goals and mechanism consistency.",
        "- Human decides final text and layout. Avoid long phrases that overflow.",
        "- Complements tools/on_image_text_suggest.py and thumbnail generators.",
        "",
        "---",
        "Preferred unblocked path remains the human OAuth step for publish.",
    ])

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"WROTE: {out_path}")
    print(f"source_preference: {source_note}")
    print(f"candidates: {len(candidates)}")
    print("Thumbnail options ready (local; estimated from packet fields only).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
