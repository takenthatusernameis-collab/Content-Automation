#!/usr/bin/env python3
"""Contract: future publish stubs must not ask for a reply.

The pin is the packet assignment. "Reply with the cue you wrote down" is
engagement bait and assumes every mechanism is a cue. Q1 publish.md stays
the approved viewer draft and is not rewritten here.
Does not call YouTube. Does not write videos/.
"""

from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from publish_brief import render  # noqa: E402

Q1 = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning" / "publish.md"
BAIT = "Reply with the cue you wrote down."


def fail(failures: list[str], ok: bool, message: str) -> None:
    if not ok:
        failures.append(message)


def main() -> int:
    failures: list[str] = []
    source = (TOOLS / "publish_brief.py").read_text(encoding="utf-8")
    fail(failures, BAIT not in source, "publish_brief.py still asks for a reply")
    fail(failures, "Do that before the next work block." in source, "publish_brief.py missing the assignment finish")
    before = hashlib.sha256(Q1.read_bytes()).hexdigest()
    with tempfile.TemporaryDirectory() as tmp:
        packet = Path(tmp) / "003-start-cue"
        packet.mkdir()
        (packet / "idea.md").write_text(
            "\n".join(
                [
                    "# Idea",
                    "- topic: Put the start cue on the work itself",
                    "- viewer: People who planned the task and still reopen the list.",
                    "- problem: the planned task has no visible start cue",
                    "- mechanism (the system, not the pep talk): Name one physical cue that means this is the first two minutes.",
                    "- why now: The stall to install is this: the planned task has no visible start cue.",
                    "- related videos to avoid repeating: none published yet",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        (packet / "titles.md").write_text(
            "Primary: Put the Start Cue on the Work Itself\n",
            encoding="utf-8",
        )
        body = render(packet)
        comment = ""
        if "## First comment (pin candidate)" in body:
            comment = body.split("## First comment (pin candidate)", 1)[1].split("## ", 1)[0]
        fail(failures, BAIT not in body, "rendered stub still asks for a reply")
        fail(failures, "physical cue" in comment, "pin comment must name the mechanism")
        fail(failures, "Do that before the next work block." in comment, "pin comment missing the assignment finish")
        fail(failures, not (packet / "publish.md").exists(), "render must not write publish.md")
        proc = subprocess.run(
            [sys.executable, str(TOOLS / "publish_brief.py"), str(packet), "--dry-run"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        fail(failures, proc.returncode == 0, f"dry-run failed: {proc.stderr}")
        fail(failures, BAIT not in proc.stdout, "dry-run still asks for a reply")
        fail(failures, not (packet / "publish.md").exists(), "dry-run wrote publish.md")
    after = hashlib.sha256(Q1.read_bytes()).hexdigest()
    fail(failures, before == after, "Q1 publish.md bytes changed")
    if failures:
        print("PUBLISH BRIEF CONTRACT FAIL")
        for item in failures:
            print(f"- {item}")
        return 1
    print("PUBLISH BRIEF CONTRACT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
