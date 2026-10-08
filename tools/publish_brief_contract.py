#!/usr/bin/env python3
"""Contract: future publish stubs must not ask for a reply, must not put the machine note in Description, and must not
stamp the first video's tags or the word "default" onto a later packet.

The pin is the packet assignment. "Reply with the cue you wrote down" is
engagement bait and assumes every mechanism is a cue. Tags come from the
channel niche plus words this packet already uses. "start cue" and
"decision fatigue" are not channel tags. Q1 publish.md stays the approved
viewer draft and is not rewritten here. The uploader drops the reply
sentence before commentThreads.insert, the same way it drops the stub pin note.
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
from youtube_upload import viewer_comment  # noqa: E402

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
        fail(failures, "start cue" in body.lower(), "packet that names a start cue may keep that tag")
        fail(failures, not (packet / "publish.md").exists(), "render must not write publish.md")
        thin = Path(tmp) / "004-close-the-extra-tab"
        thin.mkdir()
        (thin / "idea.md").write_text(
            "\n".join(
                [
                    "# Idea",
                    "- topic: Close the extra tab before you open the work",
                    "- viewer: People who open one more tab instead of the file.",
                    "- problem: the extra tab is still open, so starting means checking one more thing",
                    "- mechanism (the system, not the pep talk): Close the extra tab before the file opens.",
                    "- why now: The stall to install is this: the extra tab is still open.",
                    "- related videos to avoid repeating: none published yet",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        (thin / "titles.md").write_text(
            "Primary: Close the Extra Tab Before the File\n",
            encoding="utf-8",
        )
        thin_body = render(thin)
        tags = ""
        if "## Tags" in thin_body:
            tags = thin_body.split("## Tags", 1)[1].split("## ", 1)[0].lower()
        desc = ""
        if "## Description" in thin_body:
            desc = thin_body.split("## Description", 1)[1].split("## ", 1)[0].lower()
        fail(failures, "start cue" not in tags, "later packet must not inherit the start-cue tag")
        fail(failures, "decision fatigue" not in tags, "later packet must not inherit decision fatigue")
        fail(failures, "work defaults" not in tags, "later packet must not inherit work defaults")
        fail(failures, "focused work" in tags, "channel niche tag missing")
        fail(failures, "extra" in tags and "tab" in tags, "later packet tags must include its own words")
        fail(failures, "written default" not in desc, "missing mechanism must not invent the first video's default")
        fail(failures, "that default" not in desc, "a non-default step must not be called a default")
        fail(failures, "install " not in desc, "description must not install a step this packet did not name")
        fail(failures, "mood-dependent" not in desc, "missing promise must not invent a mood-dependent start")
        fail(failures, "close the extra tab" in desc, "description must use this packet's mechanism")
        fail(failures, "that step" in desc, "description must call this packet's mechanism a step")
        fail(failures, "no upload happened" not in desc, "description must not ship the machine note")
        fail(failures, "human locks title" not in desc, "description must not ship the lock sentence")
        fail(failures, "## Machine note" in thin_body, "machine note must stay outside Description")
        fail(failures, not (packet / "publish.md").exists(), "render must not write publish.md")
        bare = Path(tmp) / "later-packet"
        bare.mkdir()
        (bare / "idea.md").write_text(
            "\n".join(
                [
                    "# Idea",
                    "- topic: Close the extra tab before you open the work",
                    "- viewer: People who open one more tab instead of the file.",
                    "- problem: the extra tab is still open, so starting means checking one more thing",
                    "- mechanism (the system, not the pep talk): Close the extra tab before the file opens.",
                    "- why now: The stall in this packet is the extra tab.",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        bare_body = render(bare)
        bare_title = ""
        if "## Title to upload" in bare_body:
            bare_title = bare_body.split("## Title to upload", 1)[1].split("## ", 1)[0].strip()
        bare_tags = ""
        if "## Tags" in bare_body:
            bare_tags = bare_body.split("## Tags", 1)[1].split("## ", 1)[0].lower()
        fail(failures, bare_title == "Close the extra tab before you open the work", "missing titles.md must use the idea topic, not the folder name")
        fail(failures, "later" not in bare_tags and "packet" not in bare_tags, "folder name must not become tags when idea topic exists")
        fail(failures, not (bare / "publish.md").exists(), "bare render must not write publish.md")
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
    q1 = Q1.read_text(encoding="utf-8")
    posted = viewer_comment(q1.split("## First comment (pin candidate)", 1)[1].split("## ", 1)[0])
    fail(failures, BAIT not in posted, "posted Q1 pin still asks for a reply")
    fail(failures, posted.startswith("Assignment:"), "posted Q1 pin lost the assignment")
    fail(failures, "Reply with" not in posted, "posted Q1 pin still has a reply ask")
    if failures:
        print("PUBLISH BRIEF CONTRACT FAIL")
        for item in failures:
            print(f"- {item}")
        return 1
    print("PUBLISH BRIEF CONTRACT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
