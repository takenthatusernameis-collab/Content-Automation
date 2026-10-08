#!/usr/bin/env python3
"""Later scripts must not be told to grow a morning scene from the first video.

prompts/script_writer.md and prompts/script_expander.md used to say
"worked morning scene" for every short draft. A tab-closing packet would
still open with the first video's reopen unless a human rewrote the beat.
This contract checks the prompts and one assembled expand prompt. It does
not write script.md, does not scaffold Q2, and does not call YouTube.
"""

from __future__ import annotations

import hashlib
import sys
import tempfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from expand_prompt import render  # noqa: E402

Q1_SCRIPT = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning" / "script.md"
FORBIDDEN_PROMPT = (
    "concrete morning scene",
    "worked morning scene",
)
NEEDLE = "this packet's stall"


def fail(failures: list[str], ok: bool, message: str) -> None:
    if not ok:
        failures.append(message)


def main() -> int:
    failures: list[str] = []
    before = hashlib.sha256(Q1_SCRIPT.read_bytes()).hexdigest() if Q1_SCRIPT.is_file() else ""
    writer = (ROOT / "prompts" / "script_writer.md").read_text(encoding="utf-8")
    expander = (ROOT / "prompts" / "script_expander.md").read_text(encoding="utf-8")
    for name, text in (("script_writer.md", writer), ("script_expander.md", expander)):
        low = text.lower()
        for phrase in FORBIDDEN_PROMPT:
            fail(failures, phrase not in low, f"{name} still requires {phrase!r}")
        fail(failures, NEEDLE in low, f"{name} must name this packet's stall")
    fail(
        failures,
        "unless the idea card is about the morning" in writer.lower(),
        "writer must keep a morning scene only when the idea card is about the morning",
    )
    with tempfile.TemporaryDirectory() as tmp:
        packet = Path(tmp) / "videos" / "009-close-the-extra-tab"
        packet.mkdir(parents=True)
        (packet / "packet.md").write_text(
            "# Packet\n\n- working_title: Close the extra tab before you open the work\n- format: explainer-6-10min\n",
            encoding="utf-8",
        )
        (packet / "idea.md").write_text(
            "# Idea\n\n"
            "- topic: Close the extra tab before you open the work\n"
            "- viewer: People who already plan their week, then stall when it is time to start.\n"
            "- problem: the extra tab is still open, so starting the work means checking one more thing\n"
            "- mechanism (the system, not the pep talk): A shutdown default that closes the extra tab before the work file opens\n"
            "- why now: The week is already planned. The stall to install is this: the extra tab is still open.\n"
            "- related videos to avoid repeating: none published yet\n",
            encoding="utf-8",
        )
        (packet / "script.md").write_text(
            "# Script\n\n## Hook\n\nWORDS: Close the extra tab.\n\n## CTA\n\nWORDS: Close it before you open the file.\n",
            encoding="utf-8",
        )
        prompt = render(packet, docs_root=ROOT).lower()
    fail(failures, "worked morning scene" not in prompt, "assembled prompt still asks for a morning scene")
    fail(failures, "concrete morning scene" not in prompt, "assembled prompt still asks for a concrete morning scene")
    fail(failures, "a written default that removes" not in prompt, "assembled prompt invented the first video mechanism")
    fail(failures, "do not invent a morning reopen" in prompt, "assembled prompt must forbid a morning reopen")
    fail(failures, "extra tab" in prompt, "assembled prompt must keep the packet stall")
    fail(failures, "this packet's stall" in prompt, "assembled prompt must name this packet's stall")
    after = hashlib.sha256(Q1_SCRIPT.read_bytes()).hexdigest() if Q1_SCRIPT.is_file() else ""
    fail(failures, before == after and bool(before), "Q1 script.md changed")
    if failures:
        print("SCRIPT PROMPT CONTRACT FAIL")
        for item in failures:
            print(f"- {item}")
        return 1
    print("SCRIPT PROMPT CONTRACT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
