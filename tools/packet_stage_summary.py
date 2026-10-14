#!/usr/bin/env python3
"""Concise local stage summary for a video packet.

Reports presence of key text and media artifacts without inventing data,
running full gates, or materializing. Useful to avoid rediscovery of
packet readiness while the external OAuth stall continues.

Default packet is the Q1 working packet. Never claims COMPLETE.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning"

TEXT_MARKERS = [
    "idea.md",
    "script.md",
    "captions.srt",
    "packet.md",
]
MEDIA_MARKERS = {
    "vo": ["vo.wav", "audio/vo.wav", "export/vo.wav"],
    "cards": ["cards/", "assets/cards/"],
    "master": ["export/master.mp4", "master.mp4"],
}
UPLOAD_MARKER = "upload_state.json"


def _exists(packet: Path, rel: str) -> bool:
    p = packet / rel
    if rel.endswith("/"):
        return p.is_dir() and any(p.iterdir())
    return p.is_file() and p.stat().st_size > 0


def summarize(packet: Path) -> dict:
    text_ok = all(_exists(packet, m) for m in TEXT_MARKERS)
    vo_ok = any(_exists(packet, c) for c in MEDIA_MARKERS["vo"])
    cards_ok = any(_exists(packet, c) for c in MEDIA_MARKERS["cards"])
    master_ok = any(_exists(packet, c) for c in MEDIA_MARKERS["master"])
    upload_ok = _exists(packet, UPLOAD_MARKER)

    if not packet.is_dir():
        stage = "PACKET_MISSING"
    elif upload_ok:
        stage = "UPLOAD_STATE_PRESENT"
    elif master_ok:
        stage = "MASTER_PRESENT_UPLOAD_BLOCKED"
    elif vo_ok or cards_ok:
        stage = "PARTIAL_MEDIA_UPLOAD_BLOCKED"
    elif text_ok:
        stage = "TEXT_COMPLETE_MEDIA_MISSING_UPLOAD_BLOCKED"
    else:
        stage = "TEXT_INCOMPLETE"

    return {
        "packet": str(packet.relative_to(ROOT)),
        "text_complete": text_ok,
        "vo_present": vo_ok,
        "cards_present": cards_ok,
        "master_present": master_ok,
        "upload_state_present": upload_ok,
        "stage": stage,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Packet stage summary (no invent)")
    parser.add_argument("packet", nargs="?", default=str(DEFAULT_PACKET), help="Packet path")
    args = parser.parse_args()
    packet = Path(args.packet).resolve()
    info = summarize(packet)
    print("PACKET STAGE SUMMARY (no invent, no gates, no materialize)")
    for k, v in info.items():
        print(f"{k}: {v}")
    print("Note: media may be gitignored; use media_fingerprint.py for SHA checks when present.")
    print("Upload remains blocked on OAuth secrets until human step.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
