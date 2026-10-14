#!/usr/bin/env python3
"""Print the precise post-upload sequence once a private provider_video_id exists.

After the human step (secrets + execute=true dispatch) succeeds, agents and humans
need one command that lists the exact reusable tools and next dispatches without
rediscovering HANDOFF.md or checklists. Does not invent ids, metrics, or dates.
Does not poll secrets, dispatch, or write files. Reusable for every future video.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning"


def main() -> int:
    packet = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKET
    if not packet.is_dir():
        print(f"after_upload_steps: packet dir missing ({packet})")
        return 1
    print("AFTER UPLOAD STEPS (anti-rediscovery; no invent, no dispatch from agent)")
    print(f"packet: {packet.relative_to(ROOT) if packet.is_relative_to(ROOT) else packet}")
    print()
    print("1. Confirm success signals (only after Actions log shows private video id):")
    print(f"   python3 tools/post_upload_confirm.py {packet}")
    print("   Expect CONFIRMED (provider_video_id + privacy=private + uploaded_at present).")
    print()
    print("2. Check observation window (+7 calendar days + 3 Analytics lag = +10 days):")
    print(f"   python3 tools/observation_window.py {packet}")
    print("   Expect WAITING until due_at; then DUE. Do not collect early (OBSERVATION_WINDOW_NOT_DUE).")
    print()
    print("3. When DUE, dispatch feedback collection (human or authorized agent after window):")
    print("   gh workflow dispatch youtube-production.yml --repo takenthatusernameis-collab/Content-Automation -f execute=false -f collect_feedback=true")
    print("   Then verify feedback_state.json appears with real metrics (no invent).")
    print()
    print("4. Run experiment comparison once metrics exist:")
    print(f"   python3 tools/experiment_loop.py {packet}")
    print("   Requires documented baseline; produces COMPARED then decision pending until human/agent records keep/discard/retest.")
    print()
    print("5. Completion gate only after real evidence:")
    print(f"   python3 tools/complete.py {packet}")
    print("   COMPLETE requires VO + cards + master + provider_video_id + metrics + non-None experiment result.")
    print()
    print("Privacy stays private. Do not re-upload the master if POST_UPLOAD_INCOMPLETE. Do not invent any id or metric.")
    print("Full details remain in HANDOFF.md and docs/youtube_integration.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
