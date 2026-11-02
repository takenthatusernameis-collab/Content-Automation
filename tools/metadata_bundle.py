#!/usr/bin/env python3
"""Generate a consolidated metadata_bundle.md from idea.md via the individual generators.

Calls the existing generate_* functions (titles, description, tags, thumbnail) so one
command produces a single reviewable file that collects the primary operational
candidates for publish.md. Reduces sequential tool runs and multi-file review.
Dry-run default; --write optional. No other packet content edits. No secrets.
Compounds the recent generators into one human-facing review surface for every
future packet.
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

from title_generator import generate_titles
from description_generator import generate_description
from tags_generator import generate_tags
from thumbnail_generator import generate_thumbnail


def _extract_section(md: str, heading: str) -> str:
    """Pull the body under a ## heading, stripping trailing notes if present."""
    pattern = rf"^## {re.escape(heading)}\s*\n(.*?)(?=\n## |\Z)"
    m = re.search(pattern, md, re.M | re.S)
    if not m:
        return ""
    body = m.group(1).strip()
    # Drop empty or pure-note lines
    lines = [ln for ln in body.splitlines() if ln.strip() and not ln.strip().startswith("##")]
    return "\n".join(lines).strip()


def generate_bundle(packet: Path) -> str:
    idea = packet / "idea.md"
    if not idea.is_file():
        return "# Metadata Bundle\n\nNo idea.md found. Run after apply_idea.\n"

    titles_md = generate_titles(packet)
    desc_md = generate_description(packet)
    tags_md = generate_tags(packet)
    thumb_md = generate_thumbnail(packet)

    primary_title = _extract_section(titles_md, "Primary") or "(see titles.md)"
    alts = _extract_section(titles_md, "Alts")
    suggested_desc = _extract_section(desc_md, "Suggested text") or "(see description.md)"
    suggested_tags = _extract_section(tags_md, "Suggested tags")
    thumb_cands = _extract_section(thumb_md, "Candidates")

    lines = [
        "# Metadata Bundle",
        "",
        "Consolidated operational drafts from idea.md via the individual generators.",
        "Review each section, adjust for channel voice, then copy into publish.md.",
        "Does not invent text beyond what the generators already produce. Hits against the *scan tools remain revision signals.",
        "",
        "## Title (Primary)",
        "",
        primary_title,
        "",
    ]
    if alts:
        lines.extend(["## Title (Alts)", "", alts, ""])

    lines.extend([
        "## Description",
        "",
        suggested_desc,
        "",
        "## Tags",
        "",
        suggested_tags or "(see tags.md)",
        "",
        "## Thumbnail text (candidates)",
        "",
        thumb_cands or "(see thumbnail.md)",
        "",
        "## Notes",
        "",
        "Prefer the Primary title and the first thumbnail candidate that stays under 5 words.",
        "Keep the description calm and operational. Keep tags specific to the stall or default.",
        "After review, run the individual *scan.py tools or python3 tools/metadata_alignment_scan.py if available.",
        "This bundle does not write publish.md. Human (or later fill) still pastes the chosen lines.",
        "",
    ])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a consolidated metadata_bundle.md from idea.md generators."
    )
    parser.add_argument("packet", type=Path, help="Packet directory")
    parser.add_argument("--write", action="store_true", help="Write metadata_bundle.md")
    parser.add_argument("--force", action="store_true", help="Overwrite existing")
    args = parser.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"Not a directory: {packet}", file=sys.stderr)
        return 1

    out = packet / "metadata_bundle.md"
    content = generate_bundle(packet)

    if args.write:
        if out.exists() and not args.force:
            print(f"SKIP: {out} exists (use --force)")
            return 0
        out.write_text(content, encoding="utf-8")
        print(f"WROTE: {out}")
    else:
        print(content)
        print("(dry-run; use --write to save)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
