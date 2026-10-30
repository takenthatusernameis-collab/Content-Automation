#!/usr/bin/env python3
"""Print the precise post-draft script promotion sequence for a packet.

Once a draft.md or script candidate exists, agents and humans need one command
that lists the exact reusable quality, claim, cadence, and apply steps without
rediscovering content_quality.md or individual scanners. Does not invent WORDS,
sources, or rewrites. Does not write files, poll secrets, or scaffold. Reusable
for every future packet. Reduces sequential labor of promoting a draft to script.md.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning"


def main() -> int:
    packet = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKET
    if not packet.is_dir():
        print(f"script_promotion_steps: packet dir missing ({packet})")
        return 1
    print("SCRIPT PROMOTION STEPS (anti-rediscovery; no invent, no write from this tool)")
    print(f"packet: {packet.relative_to(ROOT) if packet.is_relative_to(ROOT) else packet}")
    print()
    print("Prerequisite: draft.md or equivalent spoken WORDS candidate exists. Do not treat draft as script.md.")
    print()
    print("1. Unified quality brief (aggregates scanners; revision signal only):")
    print(f"   python3 tools/quality_prep_brief.py {packet}")
    print("   Expect hits as revision signals. Default exit 0. Use --strict only when promoting.")
    print()
    print("2. Individual scanners if needed (shared phrase_utils; no local lists):")
    print(f"   python3 tools/quality_scan.py {packet}")
    print(f"   python3 tools/claim_scan.py {packet}")
    print(f"   python3 tools/cadence_repetition_scan.py {packet}")
    print(f"   python3 tools/mechanism_align_scan.py {packet}")
    print()
    print("3. Claim-to-source table (fillable; no invented sources):")
    print(f"   python3 tools/claim_source_table.py {packet}")
    print("   Fill Source column in research notes or sources.md with real citations only.")
    print()
    print("4. Read-aloud and manual revision. Then apply (human or authorized --write):")
    print(f"   python3 tools/apply_script.py {packet} --dry-run")
    print(f"   # after review: python3 tools/apply_script.py {packet} --write")
    print("   set_status refuses ready_for_vo while anti-slop hits remain.")
    print()
    print("5. Post-apply checks before VO or media steps:")
    print(f"   python3 tools/quality_scan.py {packet} --strict")
    print(f"   python3 tools/caption_prep_brief.py {packet}  # if captions path active")
    print()
    print("No invented anecdotes, numbers, or sources. Preferred current action remains human OAuth for Q1.")
    print("Full contracts: docs/content_quality.md. Do not scaffold next packet while Q1 unshipped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
