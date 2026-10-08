#!/usr/bin/env python3
"""Contract: a later idea must not inherit the first video's mechanism.

new_idea.py used to stamp "A written default that removes one daily decision"
and "The default that replaces the decision" on every topic. A later topic
about a tab must name that tab. Q1 idea.md stays the approved card.
--dry-run must not create a packet folder. Does not scaffold Q2. Does not
call YouTube. Does not poll secrets.
"""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from new_idea import idea_markdown, script_markdown  # noqa: E402

Q1 = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning" / "idea.md"
TOPIC = "Close the browser tab that is not the work"
FORBIDDEN = (
    "written default that removes one daily decision",
    "the default that replaces the decision",
    "measure the start, not the mood",
    "without a default process",
    "stalls after planning",
)


def fail(failures: list[str], ok: bool, message: str) -> None:
    if not ok:
        failures.append(message)


def main() -> int:
    failures: list[str] = []
    before = hashlib.sha256(Q1.read_bytes()).hexdigest() if Q1.is_file() else ""
    card = idea_markdown(TOPIC, "none", 0)
    script = script_markdown(TOPIC, 4)
    blob = (card + "\n" + script).lower()
    for phrase in FORBIDDEN:
        fail(failures, phrase not in blob, f"later idea inherited {phrase!r}")
    fail(failures, "browser" in blob and "tab" in blob, "later idea must name the topic")
    fail(failures, "stalls on this: close the browser tab" in blob, "viewer line must name the topic")
    fail(failures, "the move: close the browser tab" in blob, "beat title must use the topic")
    fail(failures, "the stall in this packet is this: close the browser tab" in blob, "why now must name the topic")
    fail(failures, "working niche" not in blob, "later idea must not stamp only the channel niche as why now")
    fail(failures, "morning still reopens" not in blob, "later idea must not stamp the morning reopen")
    videos_before = {p.name for p in (ROOT / "videos").iterdir()} if (ROOT / "videos").is_dir() else set()
    proc = subprocess.run(
        [sys.executable, str(TOOLS / "new_idea.py"), TOPIC, "--dry-run"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    fail(failures, proc.returncode == 0, f"dry-run failed: {proc.stderr[-200:]}")
    fail(failures, "dry-run: no packet folder written" in proc.stdout, "dry-run did not confirm no write")
    fail(failures, "written default" not in proc.stdout.lower(), "dry-run still printed the first mechanism")
    near = "Close the extra tab before the next block"
    near_proc = subprocess.run(
        [sys.executable, str(TOOLS / "new_idea.py"), near, "--dry-run"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    fail(failures, near_proc.returncode == 0, f"near-title dry-run failed: {near_proc.stderr[-200:]}")
    near_blob = near_proc.stdout.lower()
    fail(failures, "shutdown default" not in near_blob, "near tab topic inherited the Q4 shutdown default")
    fail(failures, "checking one more thing" not in near_blob, "near tab topic inherited the Q4 check line")
    fail(failures, "named step for this topic: close the extra tab" in near_blob, "near tab topic must name its own step")
    exact = "Close the extra tab before you open the work"
    exact_proc = subprocess.run(
        [sys.executable, str(TOOLS / "new_idea.py"), exact, "--dry-run"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    fail(failures, exact_proc.returncode == 0, f"exact Q4 dry-run failed: {exact_proc.stderr[-200:]}")
    fail(failures, "shutdown default" in exact_proc.stdout.lower(), "exact Q4 title must keep its queued one_line")
    videos_after = {p.name for p in (ROOT / "videos").iterdir()} if (ROOT / "videos").is_dir() else set()
    fail(failures, videos_before == videos_after, "dry-run created a packet folder")
    after = hashlib.sha256(Q1.read_bytes()).hexdigest() if Q1.is_file() else ""
    fail(failures, before == after and bool(before), "Q1 idea.md changed")
    if failures:
        print("IDEA GROUND CONTRACT FAIL")
        for item in failures:
            print(f"- {item}")
        return 1
    print("IDEA GROUND CONTRACT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
