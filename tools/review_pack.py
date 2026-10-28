#!/usr/bin/env python3
"""Generate a single local review pack consolidating key packet and draft info.

Reads idea.md, script.md (if present), and any existing local drafts
(chapters_estimate.txt, description_draft.txt, metadata_pack.txt,
publish_draft.md, visual_plan_draft.md). Writes review_pack.md with a
short summary, key candidates, chapter list, visual highlights, and a
review checklist.

No invented content. Outputs stay local and gitignored. Reduces recurring
human labor of opening and cross-referencing multiple draft files before
copying useful parts into packet.md / assets.md / publish.md on every
future packet.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

WPM = 150


def safe_read(path: Path, max_chars: int = 800) -> str:
    if not path.is_file():
        return "(missing)"
    text = path.read_text(encoding="utf-8", errors="replace").strip()
    if len(text) > max_chars:
        return text[:max_chars] + "\n... (truncated)"
    return text or "(empty)"


def extract_title_from_idea(idea_text: str) -> str:
    for line in idea_text.splitlines():
        if line.lower().startswith("- topic:"):
            return line.split(":", 1)[1].strip()
    return "(no topic line)"


def main() -> int:
    p = argparse.ArgumentParser(description="Generate local review_pack.md")
    p.add_argument("packet", type=Path, help="Path to packet directory")
    p.add_argument("--force", action="store_true", help="Overwrite existing review_pack.md")
    args = p.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"ERROR: not a directory: {packet}", file=sys.stderr)
        return 1

    idea_path = packet / "idea.md"
    if not idea_path.is_file():
        print(f"FAIL: idea.md missing in {packet}", file=sys.stderr)
        return 2

    out_path = packet / "review_pack.md"
    if out_path.exists() and not args.force:
        print(f"SKIP: {out_path} exists (use --force to overwrite)")
        return 0

    idea_text = idea_path.read_text(encoding="utf-8")
    title = extract_title_from_idea(idea_text)

    drafts = {
        "chapters": packet / "chapters_estimate.txt",
        "description": packet / "description_draft.txt",
        "metadata": packet / "metadata_pack.txt",
        "publish": packet / "publish_draft.md",
        "visual": packet / "visual_plan_draft.md",
    }

    lines = [
        "# Review Pack (local; consolidates drafts for faster review)",
        "",
        "Status: draft",
        "Source: idea.md + any existing local draft files. No invented content.",
        "Copy useful sections into packet files (publish.md, assets.md, etc.) after review.",
        "",
        f"## Topic",
        title,
        "",
        "## Idea excerpt",
        safe_read(idea_path, 600),
        "",
    ]

    script_path = packet / "script.md"
    if script_path.is_file():
        lines.extend([
            "## Script presence",
            "script.md present (see full file for WORDS).",
            "",
        ])
    else:
        lines.extend([
            "## Script presence",
            "script.md missing — run script tools first.",
            "",
        ])

    lines.append("## Draft status")
    present = 0
    for name, path in drafts.items():
        exists = path.is_file()
        if exists:
            present += 1
        lines.append(f"- {name}: {'present' if exists else 'missing'} ({path.name})")
    lines.append("")
    lines.append(f"{present}/{len(drafts)} draft files present. Run `python3 tools/drafts_all.py {packet.name}` to generate missing ones.")
    lines.append("")

    # Include short excerpts from present drafts
    if drafts["chapters"].is_file():
        lines.extend([
            "## Chapters excerpt",
            safe_read(drafts["chapters"], 500),
            "",
        ])
    if drafts["description"].is_file():
        lines.extend([
            "## Description excerpt",
            safe_read(drafts["description"], 600),
            "",
        ])
    if drafts["visual"].is_file():
        lines.extend([
            "## Visual plan excerpt",
            safe_read(drafts["visual"], 700),
            "",
        ])

    lines.extend([
        "## Review checklist",
        "- [ ] Title candidate matches mechanism (no weak clickbait)",
        "- [ ] Description summary is operational and specific",
        "- [ ] Chapters times are reasonable at 150 wpm",
        "- [ ] Visual plan card texts are short (<=5 words preferred)",
        "- [ ] No invented claims or sources",
        "- [ ] Tags avoid weak generic words",
        "- [ ] Copy approved parts into publish.md / assets.md / packet.md",
        "",
        "## Reminder",
        "- All *_draft.* and this file stay gitignored.",
        "- Do not commit media or secrets.",
        "- Upload remains blocked on the three OAuth secrets until human sets them.",
        "",
        "Generated locally. No packet content modified.",
    ])

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"WROTE: {out_path}")
    print(f"drafts_present: {present}/{len(drafts)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
