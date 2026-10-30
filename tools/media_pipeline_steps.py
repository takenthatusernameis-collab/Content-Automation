#!/usr/bin/env python3
"""Print the precise media-pipeline sequence once a packet is ready_for_vo.

After script.md is promoted and status is ready_for_vo, agents and humans
need one command that lists the exact reusable steps from VO preparation
through selected take placement, card generation, timeline, assemble planner,
media QA, and readiness for upload. Does not invent audio, images, or exports.
Does not write files, poll secrets, encode, or scaffold. Reusable for every
future packet. Reduces sequential labor of rediscovering the media order.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning"


def main() -> int:
    packet = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKET
    if not packet.is_dir():
        print(f"media_pipeline_steps: packet dir missing ({packet})")
        return 1
    print("MEDIA PIPELINE STEPS (anti-rediscovery; no invent, no write from this tool)")
    print(f"packet: {packet.relative_to(ROOT) if packet.is_relative_to(ROOT) else packet}")
    print()
    print("Prerequisite: script.md promoted and packet status ready_for_vo (or equivalent). Do not invent a Selected VO take.")
    print()
    print("1. VO preparation pack (local spoken text + timing estimates from WORDS only):")
    print(f"   python3 tools/vo_prep_pack.py {packet}")
    print("   Optional --force to overwrite. Output stays local. Not a recording.")
    print()
    print("2. Place Selected VO take (human recording or explicitly authorized generated):")
    print(f"   # drop to {packet}/vo/NNN-slug-take-selected.wav (or .flac). Repo-root vo/ is not Selected.")
    print(f"   python3 tools/narration_adapter.py {packet}")
    print("   # inspect; then --write-origin human|generated --note '...' after review.")
    print("   Generated takes must be labeled generated. Never invent a take.")
    print()
    print("3. Generate local cards from assets.md (1920x1080 PNGs; gitignored):")
    print(f"   python3 tools/card_generator.py {packet} --dry-run")
    print(f"   # after review: python3 tools/card_generator.py {packet}")
    print("   Optional --write-manifest and --mark-ready only when PNGs exist. Do not commit binaries.")
    print()
    print("4. WORDS-based edit timeline (no ffmpeg):")
    print(f"   python3 tools/timeline.py {packet} --dry-run")
    print(f"   # after review: python3 tools/timeline.py {packet} --write")
    print("   Ready_to_assemble only when VO + all mapped cards are on disk.")
    print()
    print("5. Assemble planner (ffmpeg recipe; default dry-run):")
    print(f"   python3 tools/assemble.py {packet}")
    print("   --execute refused unless media_qa PASS, ready_to_assemble=yes, and ffmpeg present.")
    print("   Never invent a master. Export stays local.")
    print()
    print("6. Fail-closed media QA (VO header/levels + card IHDR + assembly gate):")
    print(f"   python3 tools/media_qa.py {packet}")
    print("   Hard-fails only when a WAV decodes or a master exists. Do not invent media to pass.")
    print()
    print("7. Captions (optional until real take; silence-proportional aligner):")
    print(f"   python3 tools/caption_align.py {packet}")
    print("   Or captions_estimate_srt.py. Human spot-check required. Do not treat as uploaded.")
    print()
    print("8. Export probe once a master exists (ftyp + dimensions + duration):")
    print(f"   python3 tools/export_probe.py {packet}")
    print("   Requires real export/master.mp4. Do not write a dummy file.")
    print()
    print("9. Publish readiness and next (read-only; upload still blocked on secrets):")
    print(f"   python3 tools/publish_readiness.py {packet}")
    print(f"   python3 tools/next_action.py {packet}")
    print("   Preferred action remains the human OAuth step for Q1.")
    print()
    print("No invented takes, cards, or masters. Full contracts in docs/production_capabilities.md and docs/format.md.")
    print("Do not scaffold next packet while Q1 unshipped. Text stays local.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
