#!/usr/bin/env python3
"""Print the precise pre-upload review sequence before any execute=true dispatch.

Once local media, captions, and export exist, a human (or agent) still needs
one command that lists the exact grounded checks to run before setting secrets
and dispatching youtube-production.yml with execute=true. This printer
references only existing tools. It does not invent content, write files, poll
secrets, encode, upload, or scaffold. Reusable for every future packet.
Reduces sequential labor of rediscovering the final review order.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning"


def main() -> int:
    packet = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKET
    if not packet.is_dir():
        print(f"pre_upload_review_steps: packet dir missing ({packet})")
        return 1
    rel = packet.relative_to(ROOT) if packet.is_relative_to(ROOT) else packet
    print("PRE-UPLOAD REVIEW STEPS (anti-rediscovery; no invent, no write from this tool)")
    print(f"packet: {rel}")
    print()
    print("Run these after materialize (or local media placement) and before the human OAuth step.")
    print("Do not invent media, captions, or an export to pass. Do not poll secrets.")
    print()
    print("1. Media QA (VO header/levels + card IHDR + assembly gate):")
    print(f"   python3 tools/media_qa.py {packet}")
    print("   Must PASS. Hard-fails only when a WAV decodes or a master exists.")
    print()
    print("2. Caption gate (present cues; no rewrite):")
    print(f"   python3 tools/caption_gate.py {packet}")
    print("   Present bad cue fails. Missing srt fails only on execute.")
    print()
    print("3. Export probe (ftyp + 1920x1080 + duration + streams):")
    print(f"   python3 tools/export_probe.py {packet}")
    print("   Requires real export/master.mp4. Do not write a dummy file.")
    print()
    print("4. End-screen reserve check (CTA spoken duration vs last 20 s):")
    print(f"   python3 tools/end_screen_reserve_check.py {packet}")
    print("   WARN is informational. Confirm with actual VO when selected take exists.")
    print()
    print("5. Thumbnail inspect (1280x720 PNG present and within size):")
    print(f"   python3 tools/thumbnail_generator.py {packet} --inspect-only")
    print("   Or regenerate locally if needed. Do not commit the PNG.")
    print()
    print("6. Publish readiness (metadata + gates; no provider write):")
    print(f"   python3 tools/publish_readiness.py {packet}")
    print(f"   python3 tools/youtube_upload.py {packet}")
    print("   Dry-run only. Missing OAuth is expected until secrets are set.")
    print()
    print("7. Human OAuth then single dispatch (see docs/human_oauth_checklist.md):")
    print("   # After secrets exist: gh workflow dispatch youtube-production.yml ... -f execute=true")
    print("   Privacy stays private. Do not re-dispatch until a provider video id appears.")
    print()
    print("All listed tools are existing and no-invent. Preferred current action for Q1 remains the human OAuth step.")
    print("Do not scaffold next packet while Q1 unshipped. Text stays local.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
