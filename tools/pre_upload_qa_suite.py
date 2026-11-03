#!/usr/bin/env python3
"""Run the full local pre-upload QA suite in one command and report unified status.

Executes the key fail-closed checks (media_qa, caption_gate, export_probe,
end_screen_reserve_check, master_sha_check, publish_readiness) plus recent
metadata length and chapter aids (title/description/tags length checks,
chapters_suggest) on a packet after materialize. Aggregates exit codes into
a single PASS / PASS (with warnings) / FAIL summary with per-check results.
Exit 0 = PASS, exit 2 = WARN (advisory, does not fail overall), other non-zero = FAIL.
Does not invent media, write packet content, poll secrets, encode, or upload. Reduces sequential
labor of running each check separately before the human OAuth step and
single execute=true dispatch. Reusable for every future packet that has
local media.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
DEFAULT_PACKET = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning"

CHECKS = [
    ("media_qa", "media_qa.py", []),
    ("caption_gate", "caption_gate.py", []),
    ("export_probe", "export_probe.py", []),
    ("end_screen_reserve_check", "end_screen_reserve_check.py", []),
    ("master_sha_check", "master_sha_check.py", []),
    ("publish_readiness", "publish_readiness.py", []),
    ("title_length_check", "title_length_check.py", []),
    ("description_length_check", "description_length_check.py", []),
    ("tags_length_check", "tags_length_check.py", []),
    ("chapters_suggest", "chapters_suggest.py", []),
]


def run_check(name: str, script: str, packet: Path, extra: list[str]) -> tuple[int, str]:
    path = TOOLS / script
    if not path.is_file():
        return 1, f"MISSING {script}"
    cmd = [sys.executable, str(path), str(packet)] + extra
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False, timeout=60)
        out = (proc.stdout or "").strip() + ("\n" + proc.stderr.strip() if proc.stderr else "")
        return proc.returncode, out
    except Exception as e:
        return 1, f"EXCEPTION {name}: {e}"


def main() -> int:
    packet = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKET
    if not packet.is_dir():
        print(f"pre_upload_qa_suite: packet dir missing ({packet})")
        return 1

    print("PRE-UPLOAD QA SUITE (unified local checks; no invent, no write, no secrets)")
    print(f"packet: {packet.name}")
    print()

    results = []
    overall_ok = True
    has_warn = False
    for name, script, extra in CHECKS:
        code, out = run_check(name, script, packet, extra)
        # Treat exit 0 as PASS, exit 2 as WARN (advisory), other non-zero as FAIL
        if code == 0:
            status = "PASS"
        elif code == 2:
            status = "WARN"
            has_warn = True
        else:
            status = "FAIL"
            overall_ok = False
        results.append((name, status, code, out[:400] + ("..." if len(out) > 400 else "")))
        print(f"[{status}] {name} (exit {code})")

    print()
    result_label = "PASS" if overall_ok else "FAIL"
    if overall_ok and has_warn:
        result_label = "PASS (with warnings)"
    print("UNIFIED RESULT:", result_label)
    print("Details (truncated):")
    for name, status, code, snippet in results:
        print(f"--- {name} ---")
        print(snippet or "(no output)")
        print()

    print("If overall PASS or PASS (with warnings), proceed to human OAuth step (docs/human_oauth_checklist.md).")
    print("Do not dispatch execute=true until secrets exist and this suite is not FAIL.")
    print("Text stays local. Do not rematerialize if master already present.")
    return 0 if overall_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
