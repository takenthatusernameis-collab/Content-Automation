#!/usr/bin/env python3
"""Print preferred unblocked actions while STALL_OAUTH_IDLE and published=0.

Reduces rediscovery of the human OAuth step and explicitly lists saturation patterns
to avoid. Does not poll secrets, invent media, dispatch, or write files.
Reusable across future stalled runs.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning"


def main() -> int:
    packet = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKET
    print("WHILE STALLED PREFERRED (anti-drift; published=0; STALL_OAUTH_IDLE)")
    print(f"packet: {packet.name if packet.is_dir() else 'default'}")
    print()
    print("PRIMARY (human only):")
    print("  1. Complete docs/human_oauth_checklist.md (scopes, mint, gh secret set x3)")
    print("  2. Dispatch once: gh workflow dispatch youtube-production.yml -f execute=true")
    print("  3. Confirm private provider_video_id in Actions log + packet/upload_state.json")
    print()
    print("AVOID (saturation / low leverage while published=0):")
    print("  - Another consistency / tags_hygiene / metadata printer")
    print("  - Extending production_readiness.py or pre_upload_qa_suite further")
    print("  - Scaffolding Q2")
    print("  - Polling secrets or rematerializing media if present")
    print("  - Pure status / confirmation / sequence printers")
    print()
    print("ACCEPTABLE UNBLOCKED (truly new, compounds after publish):")
    print("  - Media/QA capability that does not require credentials or invent files")
    print("  - Feedback/experiment preparation that stays fail-closed (no invent)")
    print("  - Documentation that reduces human minutes on the OAuth checklist")
    print()
    print("See tools/stall_watch.py for machine flags. Do not treat this as a new gate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
