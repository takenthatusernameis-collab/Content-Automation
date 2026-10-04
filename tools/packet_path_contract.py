#!/usr/bin/env python3
"""Contract for the production packet path gate."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import packet_path  # noqa: E402

Q1 = "videos/002-stop-deciding-what-to-work-on-every-morning"


def fail(message: str) -> None:
    print(f"PACKET PATH CONTRACT FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    if packet_path.refuse_reason(Q1) is not None:
        fail("live Q1 packet must be accepted")
    for bad in ("", "videos/_template", "videos/..", "../videos/002", "tmp/x", "videos/no-such-packet"):
        if packet_path.refuse_reason(bad) is None:
            fail(f"must refuse {bad!r}")
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "videos" / "003-example").mkdir(parents=True)
        if packet_path.refuse_reason("videos/003-example", root=root) is not None:
            fail("an existing videos/<slug> folder must be accepted")
        if packet_path.refuse_reason("videos/missing", root=root) != "missing_folder":
            fail("a missing folder must be missing_folder")
    env = os.environ.copy()
    env["PACKET"] = Q1
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "packet_path.py")],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
    )
    if proc.returncode != 0 or "PACKET videos/002-stop-deciding-what-to-work-on-every-morning" not in proc.stdout:
        fail(proc.stderr or proc.stdout)
    env["PACKET"] = "videos/_template"
    refused = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "packet_path.py")],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
    )
    if refused.returncode != 2 or "REFUSE" not in refused.stderr:
        fail("template path must exit 2")
    print("PACKET PATH CONTRACT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
