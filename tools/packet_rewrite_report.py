#!/usr/bin/env python3
"""Unified rewrite starting points for one packet.

Prints qualitative suggestions from rewrite_suggest (script WORDS: quality fillers,
claim hedges, unsourced digits), hook_suggest, body_suggest, payoff_suggest,
cta_suggest, title_suggest, description_suggest, tags_suggest,
first_comment_suggest, chapters_suggest, end_screen_suggest, and originality_report
(7-point test signals). Does not write any files, invent facts, or call the
network. A report is a starting point for human or agent revision, not a final rewrite.

Compounds across every future video by collapsing multiple separate suggestion,
script-structure, and originality commands into one entry point.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))


def run_originality(packet: str) -> str:
    """Run originality_report.py and return its output."""
    path = ROOT / "tools" / "originality_report.py"
    if not path.is_file():
        return "MISSING originality_report.py"
    try:
        proc = subprocess.run(
            [sys.executable, str(path), packet],
            capture_output=True,
            text=True,
            check=False,
        )
        return (proc.stdout or "") + (proc.stderr or "")
    except Exception as e:
        return f"EXCEPTION originality_report: {e}"


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

    # Originality signals (7-point test)
    print("\n## ORIGINALITY")
    orig_out = run_originality(str(packet))
    print(orig_out.strip() or "(no output)")

    # Script structure starting points (hook / body / payoff / CTA)
    try:
        from hook_suggest import extract as hook_extract, suggest as hook_suggest
        if idea_text:
            mech, problem, topic = hook_extract(idea_text)
            hooks = hook_suggest(mech, problem, topic)
            print("\n## HOOK")
            print(f"  mechanism: {mech}")
            for i, h in enumerate(hooks, 1):
                print(f"  {i}. {h}")
        else:
            print("\n## HOOK\n  no idea.md")
    except Exception as e:
        print(f"\n## HOOK\n  unavailable: {e}")

    try:
        from body_suggest import extract as body_extract, suggest as body_suggest
        if idea_text:
            mech, problem, topic = body_extract(idea_text)
            beats = body_suggest(mech, problem, topic)
            print("\n## BODY BEATS")
            for i, b in enumerate(beats, 1):
                print(f"  {i}. {b}")
        else:
            print("\n## BODY BEATS\n  no idea.md")
    except Exception as e:
        print(f"\n## BODY BEATS\n  unavailable: {e}")

    try:
        from payoff_suggest import extract as payoff_extract, suggest as payoff_suggest
        if idea_text:
            mech, problem, topic = payoff_extract(idea_text)
            payoffs = payoff_suggest(mech, problem, topic)
            print("\n## PAYOFF")
            for i, p in enumerate(payoffs, 1):
                print(f"  {i}. {p}")
        else:
            print("\n## PAYOFF\n  no idea.md")
    except Exception as e:
        print(f"\n## PAYOFF\n  unavailable: {e}")

    try:
        from cta_suggest import extract as cta_extract, suggest as cta_suggest
        if idea_text:
            mech, problem = cta_extract(idea_text)
            spoken, end_line = cta_suggest(mech, problem)
            print("\n## CTA")
            print(f"  spoken: {spoken}")
            print(f"  end-screen: {end_line}")
        else:
            print("\n## CTA\n  no idea.md")
    except Exception as e:
        print(f"\n## CTA\n  unavailable: {e}")

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
    print("Paste or adapt the starting points above. Re-run the individual scanners and originality_report after edits.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
