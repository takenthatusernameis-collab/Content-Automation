#!/usr/bin/env python3
"""Fail-closed check that the Q1 packet master matches the known-good r253 SHA.

Prints PASS only when export/master.mp4 exists and sha256 matches the durable target.
Does not invent files, does not poll secrets, does not modify the packet.
Useful for confirming the correct master is present before any upload dispatch.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Known durable target from STATE.md / HANDOFF.md (q1-media-r253)
TARGET_SHA = "4ff4c0e80ac6b5719aa1b8b5acc70b2845820208f56e83881f6e7bad30101546"
EXPORT_REL = "export/master.mp4"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python3 tools/master_sha_check.py <packet_dir>", file=sys.stderr)
        return 1
    packet = Path(sys.argv[1]).resolve()
    master = packet / EXPORT_REL
    if not master.is_file():
        print(f"FAIL: master missing at {EXPORT_REL}")
        print("Run python3 tools/materialize_q1_release.py first (do not rematerialize if present).")
        return 2
    actual = sha256_file(master)
    if actual == TARGET_SHA:
        print(f"PASS: master SHA matches r253 target")
        print(f"sha256: {actual}")
        print("Correct master present. Safe to proceed with pre-upload review or human OAuth dispatch.")
        return 0
    else:
        print(f"FAIL: master SHA mismatch")
        print(f"expected: {TARGET_SHA}")
        print(f"actual:   {actual}")
        print("Do not use this master. Re-run materialize_q1_release.py to install the correct r253 file.")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
