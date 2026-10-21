#!/usr/bin/env python3
"""Unified rewrite starting points for one packet.

Prints qualitative suggestions from rewrite_suggest (script WORDS: quality fillers,
claim hedges, unsourced digits), title_suggest, description_suggest, tags_suggest,
first_comment_suggest, chapters_suggest, and end_screen_suggest.
Does not write any files, invent facts, or call the network. A report is a
starting point for human or agent revision, not a final rewrite.

Compounds across every future video by collapsing multiple separate suggestion
commands into one entry point.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: python3 tools/packet_rewrite_report.py <packet-folder>")
        return 1
    packet = Path(sys.argv[1]).resolve()
    if not packet.is_dir():
        print(f"not a directory: {packet}")
        return 1

    print(f"PACKET REWRITE REPORT: {packet.name}")
    print("=" * 60)

    idea_path = packet / "idea.md"
    idea_text = idea_path.read_text(encoding="utf-8") if idea_path.is_file() else ""

    # Script body (quality + claims + digits)
    try:
        from rewrite_suggest import scan_and_suggest
        script_hits = scan_and_suggest(packet)
        print("\n## SCRIPT (WORDS)")
        if not script_hits:
            print("  clear")
        else:
            for kind, phrase, ctx, sug in script_hits:
                print(f"  [{kind}] '{phrase}'")
                print(f"    context: {ctx}")
                print(f"    suggest: {sug}")
    except Exception as e:
        print(f"\n## SCRIPT (WORDS)\n  unavailable: {e}")

    # Titles
    try:
        from title_suggest import extract as title_extract, suggest as title_suggest
        if idea_text:
            mech, problem, topic = title_extract(idea_text)
            titles = title_suggest(mech, problem, topic)
            print("\n## TITLES")
            print(f"  mechanism: {mech}")
            for i, t in enumerate(titles, 1):
                print(f"  {i}. {t}  ({len(t)} chars)")
        else:
            print("\n## TITLES\n  no idea.md")
    except Exception as e:
        print(f"\n## TITLES\n  unavailable: {e}")

    # Description
    try:
        from description_suggest import extract as desc_extract, suggest as desc_suggest
        if idea_text:
            mech, problem, topic = desc_extract(idea_text)
            desc = desc_suggest(mech, problem, topic)
            print("\n## DESCRIPTION")
            print(f"  {desc}")
        else:
            print("\n## DESCRIPTION\n  no idea.md")
    except Exception as e:
        print(f"\n## DESCRIPTION\n  unavailable: {e}")

    # Tags
    try:
        from tags_suggest import extract as tags_extract, suggest as tags_suggest
        if idea_text:
            mech, problem, topic = tags_extract(idea_text)
            tags = tags_suggest(mech, problem, topic)
            print("\n## TAGS")
            for t in tags:
                print(f"  - {t}")
        else:
            print("\n## TAGS\n  no idea.md")
    except Exception as e:
        print(f"\n## TAGS\n  unavailable: {e}")

    # First comment
    try:
        from first_comment_suggest import extract as fc_extract, suggest as fc_suggest
        if idea_text:
            mech, problem = fc_extract(idea_text)
            comment = fc_suggest(mech, problem)
            print("\n## FIRST COMMENT")
            print(f"  {comment}")
        else:
            print("\n## FIRST COMMENT\n  no idea.md")
    except Exception as e:
        print(f"\n## FIRST COMMENT\n  unavailable: {e}")

    # Chapters
    try:
        from chapters_suggest import extract as ch_extract, suggest as ch_suggest
        if idea_text:
            mech, problem, topic = ch_extract(idea_text)
            chapters = ch_suggest(mech, problem, topic)
            print("\n## CHAPTERS")
            for line in chapters:
                print(f"  {line}")
        else:
            print("\n## CHAPTERS\n  no idea.md")
    except Exception as e:
        print(f"\n## CHAPTERS\n  unavailable: {e}")

    # End screen / CTA
    try:
        from end_screen_suggest import extract as es_extract, suggest as es_suggest
        if idea_text:
            mech, problem, topic = es_extract(idea_text)
            ends = es_suggest(mech, problem, topic)
            print("\n## END SCREEN")
            for e in ends:
                print(f"  - {e}")
        else:
            print("\n## END SCREEN\n  no idea.md")
    except Exception as e:
        print(f"\n## END SCREEN\n  unavailable: {e}")

    print("\n" + "=" * 60)
    print("PACKET REWRITE REPORT DONE (no files written)")
    print("Paste or adapt the starting points above. Re-run the individual scanners after edits.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
