#!/usr/bin/env python3
"""Print the relevant production stage and the exact sequence-printer command.

Agents and humans often need to know which of the existing grounded sequence
tools (early_pipeline_steps, script_promotion_steps, media_pipeline_steps,
after_upload_steps) applies to the current packet state. This tool inspects
only the presence of key files and status signals and prints the matching
sequence command. It does not invent content, write files, poll secrets,
or scaffold. Reusable for every future packet. Reduces the labor of
selecting the correct anti-rediscovery sequence.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning"


def file_exists(packet: Path, name: str) -> bool:
    return (packet / name).is_file()


def main() -> int:
    packet = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKET
    if not packet.is_dir():
        print(f"pipeline_entry: packet dir missing ({packet})")
        return 1

    rel = packet.relative_to(ROOT) if packet.is_relative_to(ROOT) else packet
    print("PIPELINE ENTRY (stage guide; no invent, no write)")
    print(f"packet: {rel}")
    print()

    has_idea = file_exists(packet, "idea.md")
    has_draft = file_exists(packet, "draft.md")
    has_script = file_exists(packet, "script.md")
    has_vo = any((packet / "vo").glob("*-take-selected.*")) if (packet / "vo").is_dir() else False
    has_upload = file_exists(packet, "upload_state.json")

    if has_upload:
        print("Stage: post-upload (provider video id may exist)")
        print("Command:")
        print(f"   python3 tools/after_upload_steps.py {packet}")
        print("Confirms success signals, observation window, feedback dispatch, experiment, completion.")
    elif has_script or has_vo:
        print("Stage: media / ready_for_vo or later")
        print("Command:")
        print(f"   python3 tools/media_pipeline_steps.py {packet}")
        print("VO prep, selected take placement, cards, timeline, assemble, media QA, captions, export probe.")
    elif has_draft:
        print("Stage: script promotion (draft exists)")
        print("Command:")
        print(f"   python3 tools/script_promotion_steps.py {packet}")
        print("Quality scans, claim table, apply_script, promotion to ready_for_vo.")
    elif has_idea:
        print("Stage: early pipeline (idea filled; no draft yet)")
        print("Command:")
        print(f"   python3 tools/early_pipeline_steps.py {packet}")
        print("Research skeleton, draft skeleton, word check, then promotion.")
    else:
        print("Stage: newly scaffolded (no idea.md yet)")
        print("Command:")
        print(f"   python3 tools/early_pipeline_steps.py {packet}")
        print("after_scaffold, idea fill, research, draft skeleton.")

    print()
    print("All sequence tools are no-invent, no-write printers. Preferred current action for Q1 remains the human OAuth step.")
    print("Do not scaffold next packet while Q1 unshipped. Text stays local.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
