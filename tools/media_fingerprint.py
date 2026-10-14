#!/usr/bin/env python3
"""Quick local media fingerprint for the Q1 packet.

Reports presence of Selected VO, cards count, and master SHA match against the known target.
Does not materialize, does not run full media_qa, does not invent paths or hashes.
Use to confirm PRESENT/MISSING without heavier checks.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

PACKET = Path("videos/002-stop-deciding-what-to-work-on-every-morning")
VO_NAME = "002-stop-deciding-what-to-work-on-every-morning-take-selected.wav"
MASTER_NAME = "master.mp4"
TARGET_MASTER_SHA = "4ff4c0e80ac6b5719aa1b8b5acc70b2845820208f56e83881f6e7bad30101546"

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> None:
    vo = PACKET / "vo" / VO_NAME
    cards = PACKET / "cards"
    master = PACKET / "export" / MASTER_NAME
    vo_ok = vo.is_file()
    cards_count = len(list(cards.glob("*.png"))) if cards.is_dir() else 0
    master_ok = master.is_file()
    master_sha = sha256(master) if master_ok else "absent"
    match = master_ok and master_sha == TARGET_MASTER_SHA
    status = "PRESENT" if vo_ok and cards_count >= 7 and match else "MISSING_OR_MISMATCH"
    print(f"media_fingerprint: {status}")
    print(f"vo_present: {vo_ok}")
    print(f"cards_count: {cards_count}")
    print(f"master_present: {master_ok}")
    print(f"master_sha_match: {match}")
    print(f"target_sha: {TARGET_MASTER_SHA[:16]}...")
    if not match and master_ok:
        print(f"actual_sha: {master_sha[:16]}...")

if __name__ == "__main__":
    main()
