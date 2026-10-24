#!/usr/bin/env python3
"""Quick local media fingerprint for a video packet.

Reports presence of Selected VO, cards count, and master SHA match against a known target.
Does not materialize, does not run full media_qa, does not invent paths or hashes.
Use to confirm PRESENT/MISSING without heavier checks.

Defaults to the current Q1 packet and its known master SHA. Pass --packet and optional
--target-sha to check any future packet (target-sha optional; if omitted, only presence is checked).
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

DEFAULT_PACKET = Path("videos/002-stop-deciding-what-to-work-on-every-morning")
DEFAULT_TARGET_SHA = "4ff4c0e80ac6b5719aa1b8b5acc70b2845820208f56e83881f6e7bad30101546"
MASTER_NAME = "master.mp4"

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def find_selected_vo(packet: Path) -> Path | None:
    vo_dir = packet / "vo"
    if not vo_dir.is_dir():
        return None
    candidates = list(vo_dir.glob("*-take-selected.wav")) or list(vo_dir.glob("*.wav"))
    return candidates[0] if candidates else None

def main() -> None:
    parser = argparse.ArgumentParser(description="Media fingerprint (no invent, no materialize)")
    parser.add_argument("--packet", default=str(DEFAULT_PACKET), help="Packet directory (default: current Q1)")
    parser.add_argument("--target-sha", default=DEFAULT_TARGET_SHA, help="Expected master SHA256 (default: Q1 known)")
    args = parser.parse_args()

    packet = Path(args.packet)
    target_sha = args.target_sha.strip()

    vo = find_selected_vo(packet)
    cards = packet / "cards"
    master = packet / "export" / MASTER_NAME
    vo_ok = vo is not None and vo.is_file()
    cards_count = len(list(cards.glob("*.png"))) if cards.is_dir() else 0
    master_ok = master.is_file()
    master_sha = sha256(master) if master_ok else "absent"
    match = master_ok and master_sha == target_sha
    status = "PRESENT" if vo_ok and cards_count >= 7 and match else "MISSING_OR_MISMATCH"
    print(f"media_fingerprint: {status}")
    print(f"packet: {packet}")
    print(f"vo_present: {vo_ok}")
    if vo_ok and vo:
        print(f"vo_path: {vo.name}")
    print(f"cards_count: {cards_count}")
    print(f"master_present: {master_ok}")
    print(f"master_sha_match: {match}")
    print(f"target_sha: {target_sha[:16]}...")
    if not match and master_ok:
        print(f"actual_sha: {master_sha[:16]}...")

if __name__ == "__main__":
    main()
