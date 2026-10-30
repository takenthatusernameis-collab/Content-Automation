#!/usr/bin/env python3
"""Print the precise early-pipeline sequence for a newly scaffolded packet.

Once a packet folder exists (after new_packet.py), agents and humans need one
command that lists the exact reusable steps from after_scaffold through idea
fill, research skeleton, draft skeleton, word-band check, and promotion to
ready_for_vo. Does not invent WORDS, sources, or claims. Does not write files,
poll secrets, or scaffold. Reusable for every future packet. Reduces sequential
labor of rediscovering the order of early production tools.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning"


def main() -> int:
    packet = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKET
    if not packet.is_dir():
        print(f"early_pipeline_steps: packet dir missing ({packet})")
        return 1
    print("EARLY PIPELINE STEPS (anti-rediscovery; no invent, no write from this tool)")
    print(f"packet: {packet.relative_to(ROOT) if packet.is_relative_to(ROOT) else packet}")
    print()
    print("Prerequisite: packet folder scaffolded (python3 tools/new_packet.py ...). Do not treat stubs as final.")
    print()
    print("1. Fill generated packet files (titles, publish, captions, assets, render, session, expand, research, qa):")
    print(f"   python3 tools/after_scaffold.py {packet}")
    print("   Reuses existing brief renderers. Empty-only for titles/thumbs.")
    print()
    print("2. Fill or check idea.md (topic/problem/mechanism from queue only):")
    print(f"   python3 tools/idea_brief.py {packet} --block")
    print("   # paste into idea.md, then: python3 tools/idea_brief.py {packet} --check")
    print("   Or apply_idea.py --write after review.")
    print()
    print("3. Grounded research.md skeleton (no invented sources):")
    print(f"   python3 tools/research_notes_writer.py {packet}")
    print("   # optional --write after review. Fill Sources column with real citations only.")
    print()
    print("4. Draft skeleton with short operational lines (from idea fields only):")
    print(f"   python3 tools/draft_skeleton_writer.py {packet}")
    print("   Expand WORDS lines to 900-1500 band. Do not treat as script.md.")
    print()
    print("5. Word-band check and expansion coach (read-only):")
    print(f"   python3 tools/words.py {packet}")
    print(f"   python3 tools/draft_pre_apply_coach.py {packet}")
    print("   Target band is in docs/format.md. Do not pad.")
    print()
    print("6. Promote draft to script.md (quality + apply; see script_promotion_steps.py):")
    print(f"   python3 tools/script_promotion_steps.py {packet}")
    print("   Then set_status.py only after anti-slop clear and duration OK.")
    print()
    print("7. Status and next action (read-only):")
    print(f"   python3 tools/next_action.py {packet}")
    print(f"   python3 tools/status_report.py")
    print()
    print("No invented anecdotes, numbers, or sources. Preferred current action remains human OAuth for Q1.")
    print("Do not scaffold next packet while Q1 unshipped. Full contracts in docs/production_rules.md and docs/content_quality.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
