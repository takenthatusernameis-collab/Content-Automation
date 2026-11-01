#!/usr/bin/env python3
"""Print the single highest-leverage next action for a video packet.

Inspects presence of key artifacts and lightweight quality signals without
inventing content, writing files, polling secrets, or running heavy gates.
Outputs one concrete recommended command that advances the packet.
Reusable across all future packets. Complements packet_stage_summary.py.
Does not rematerialize media or dispatch workflows.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
DEFAULT_PACKET = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning"


def file_present(packet: Path, name: str) -> bool:
    p = packet / name
    return p.is_file() and p.stat().st_size > 20


def dir_has_files(packet: Path, rel: str) -> bool:
    d = packet / rel
    return d.is_dir() and any(d.iterdir())


def run_quick_scan(script: str, packet: Path) -> bool:
    """Return True if the scanner exits 0 (no hard hits or missing)."""
    path = TOOLS / script
    if not path.is_file():
        return True  # assume ok if tool missing
    try:
        proc = subprocess.run(
            [sys.executable, str(path), str(packet)],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        # Most scanners exit 0 even with signals; treat non-zero as needs attention only if strict-like
        return proc.returncode == 0
    except Exception:
        return True


def suggest(packet: Path) -> str:
    if not packet.is_dir():
        return f"PACKET_MISSING: scaffold with python3 tools/new_packet.py \"<title>\" then python3 tools/mark_topic.py --write"

    # Text stage
    if not file_present(packet, "idea.md"):
        return f"FILL_IDEA: python3 tools/apply_idea.py {packet.relative_to(ROOT)} --write  # then review idea.md"

    if not file_present(packet, "research.md"):
        return f"START_RESEARCH: python3 tools/research_brief.py {packet.relative_to(ROOT)} --dry-run  # review stub then fill sources"

    # Script stage
    has_script = file_present(packet, "script.md")
    has_draft = file_present(packet, "draft.md")
    if not has_script and not has_draft:
        return f"START_DRAFT: python3 tools/draft_md_starter.py {packet.relative_to(ROOT)}  # then expand WORDS"

    if has_draft and not has_script:
        return f"APPLY_SCRIPT: python3 tools/apply_script.py {packet.relative_to(ROOT)} --from draft.md --write --refresh  # after quality clear"

    if has_script:
        # Lightweight quality signals
        quality_ok = run_quick_scan("quality_scan.py", packet)
        claim_ok = run_quick_scan("claim_scan.py", packet)
        if not quality_ok or not claim_ok:
            return f"CLEAR_QUALITY: python3 tools/quality_prep_brief.py {packet.relative_to(ROOT)}  # revise WORDS then re-scan"

    # Media stage (local only)
    has_vo = dir_has_files(packet, "vo")
    has_cards = dir_has_files(packet, "cards")
    has_master = file_present(packet, "export/master.mp4")

    if not has_vo:
        return f"RECORD_VO: place selected take at vo/{packet.name}-take-selected.wav (human or authorized generated); then python3 tools/media_qa.py {packet.relative_to(ROOT)}"

    if not has_cards:
        return f"GENERATE_CARDS: python3 tools/card_generator.py {packet.relative_to(ROOT)}  # gitignored PNGs; do not commit"

    if not has_master:
        return f"ASSEMBLE_CHECK: python3 tools/assemble.py {packet.relative_to(ROOT)}  # then media_qa; encode only when READY_TO_ENCODE and gates PASS"

    # Thumbnail (local only; leverages short on-image preference)
    if not file_present(packet, "thumbnail.png"):
        return f"GENERATE_THUMB: python3 tools/thumbnail_generator.py {packet.relative_to(ROOT)}  # prefers short on-image from thumbnail.md; local PNG only, do not commit"

    # Upload stage
    if not file_present(packet, "upload_state.json"):
        return "UPLOAD_BLOCKED: human OAuth step (docs/human_oauth_checklist.md) then single execute=true dispatch. Do not poll secrets."

    return "PACKET_READY_LOCAL: review upload_state.json and proceed to feedback window after 7+ days if private video id present."


def main() -> int:
    parser = argparse.ArgumentParser(description="Single highest-leverage next step for a packet (no invent, no write)")
    parser.add_argument("packet", nargs="?", default=str(DEFAULT_PACKET), help="Packet folder")
    args = parser.parse_args()
    packet = Path(args.packet).resolve()

    print("PACKET NEXT STEP (single high-leverage action; no invent, no secrets, no media commit)")
    print(f"packet: {packet.relative_to(ROOT) if packet.is_relative_to(ROOT) else packet}")
    print()
    print(suggest(packet))
    print()
    print("Re-run after completing the step. For full stage: python3 tools/packet_stage_summary.py")
    print("Global stall remains OAuth until human secrets + dispatch.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
