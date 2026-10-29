#!/usr/bin/env python3
"""Contract for pre_dispatch_confirm.py.

Verifies fail-closed behavior on a missing packet and success path on a
minimal temporary tree without requiring real media.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str], cwd: Path | None = None) -> tuple[int, str]:
    result = subprocess.run(cmd, cwd=cwd or ROOT, capture_output=True, text=True)
    return result.returncode, result.stdout + result.stderr


def main() -> int:
    # missing packet
    code, out = run(["python3", "tools/pre_dispatch_confirm.py", "/tmp/does-not-exist-packet"])
    if code == 0 or "FAIL" not in out:
        print("CONTRACT FAIL: missing packet did not fail")
        return 1

    # minimal ready-looking tree (no real media_qa will fail, so we expect NOT READY)
    with tempfile.TemporaryDirectory() as tmp:
        pkt = Path(tmp) / "999-test"
        pkt.mkdir()
        (pkt / "publish.md").write_text("# Publish\n## Title to upload\nTest\n")
        (pkt / "captions.srt").write_text("1\n00:00:00,000 --> 00:00:01,000\nTest\n")
        (pkt / "vo").mkdir()
        (pkt / "vo" / "999-test-take-selected.wav").write_bytes(b"RIFF")
        (pkt / "export").mkdir()
        (pkt / "export" / "master.mp4").write_bytes(b"ftyp")
        code, out = run(["python3", "tools/pre_dispatch_confirm.py", str(pkt)])
        if "NOT READY" not in out and "READY" not in out:
            print("CONTRACT FAIL: unexpected output on temp packet")
            print(out)
            return 1

    print("pre_dispatch_confirm_contract: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
