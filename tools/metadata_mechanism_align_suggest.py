#!/usr/bin/env python3
"""Soft alignment check: does title / description / thumbnail mention the mechanism?

Reads idea.md for mechanism (via idea_utils). Scans titles.md, description
candidates or publish.md, and thumbnail text for key mechanism words.
Reports soft notes if the core mechanism is under-represented in metadata.
Does not invent text, rewrite files, call APIs, or poll secrets.
Reduces human labor of manually verifying mechanism consistency across
title, description, and thumbnail for future packets. Soft only.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from idea_utils import extract  # type: ignore
from phrase_utils import spoken_words  # type: ignore

STOP = {"the", "a", "an", "of", "to", "and", "or", "for", "in", "on", "with", "by", "is", "are", "be"}


def key_words(text: str, min_len: int = 4) -> set[str]:
    words = re.findall(r"\b[a-zA-Z]{" + str(min_len) + r",}\b", text.lower())
    return {w for w in words if w not in STOP}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Soft check that metadata surfaces the packet mechanism. No invent, no writes."
    )
    parser.add_argument("packet", type=Path, help="Packet folder")
    args = parser.parse_args()
    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"Not a directory: {packet}", file=sys.stderr)
        return 1

    idea_path = packet / "idea.md"
    if not idea_path.is_file():
        print("No idea.md found. Cannot extract mechanism.")
        return 0

    idea_text = idea_path.read_text(encoding="utf-8")
    mech, problem, topic = extract(idea_text)
    if not mech:
        print("No mechanism found in idea.md.")
        return 0

    mech_keys = key_words(mech)
    print("METADATA MECHANISM ALIGN SUGGEST (soft; no invent, no writes)")
    print(f"Mechanism: {mech}")
    print(f"Key words: {', '.join(sorted(mech_keys)) or '(none)'}")
    print()

    # Collect metadata texts
    texts = {}
    titles_path = packet / "titles.md"
    if titles_path.is_file():
        texts["titles"] = titles_path.read_text(encoding="utf-8")
    pub_path = packet / "publish.md"
    if pub_path.is_file():
        texts["publish"] = pub_path.read_text(encoding="utf-8")
    # Thumbnail via existing helper if present; fallback to scanning publish/assets
    assets_path = packet / "assets.md"
    if assets_path.is_file():
        texts["assets"] = assets_path.read_text(encoding="utf-8")

    if not texts:
        print("No titles.md / publish.md / assets.md found to check.")
        return 0

    found_any = False
    for name, content in texts.items():
        content_keys = key_words(spoken_words(content) if name != "titles" else content)
        overlap = mech_keys & content_keys
        print(f"{name}.md: {len(overlap)} / {len(mech_keys)} mechanism words present")
        if overlap:
            print(f"  matched: {', '.join(sorted(overlap))}")
            found_any = True
        else:
            print("  no key mechanism words detected (soft note: consider weaving mechanism language)")

    print()
    if not found_any and mech_keys:
        print("Soft recommendation: add at least one mechanism key word to title, description, or thumbnail text for consistency.")
    else:
        print("Mechanism language appears in at least one metadata surface. Good.")
    print("Human: use as signal only. Preserve voice. Does not rewrite files.")
    print("Next: python3 tools/title_metrics_suggest.py", packet, "&& python3 tools/thumbnail_metrics_suggest.py", packet)
    print("Human OAuth remains the publish blocker.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
