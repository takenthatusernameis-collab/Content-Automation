#!/usr/bin/env python3
"""Contract check for idea_brief reprint recover.

Read-only versus videos/. Uses tempfile only.
Locks:
- idea_brief source says it does not write idea.md
- human_session names idea_brief.py and the pinned 002 folder
- human_session names idea_brief.py --block
- running idea_brief on a blank 002 packet reprints Q1 topic + Q1_PROBLEM + one_line
- idea_brief --block prints a paste-ready idea.md body with those fields
- idea.md bytes are unchanged after both runs
- stdout says it writes nothing

Unmapped in which_contract. Not a reconstruct wave.
Does not write idea.md, the queue, or sample-001.
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

from operator_pin_contract import Q1_PROBLEM  # noqa: E402
from queue_lib import parse_queue  # noqa: E402

TITLE = "Stop deciding what to work on every morning"
FOLDER = "002-stop-deciding-what-to-work-on-every-morning"


def fail(failures: list[str], cond: bool, msg: str) -> None:
    if not cond:
        failures.append(msg)


def sha(path: Path) -> str:
    if not path.is_file():
        return ""
    return hashlib.md5(path.read_bytes()).hexdigest()


def source_locks(failures: list[str]) -> None:
    brief_src = (TOOLS / "idea_brief.py").read_text(encoding="utf-8")
    human = (ROOT / "docs" / "human_session.md").read_text(encoding="utf-8")
    fail(failures, "Does not write idea.md" in brief_src or "does not write idea.md" in brief_src, "idea_brief missing no-write-idea note")
    fail(failures, "idea_followup" in brief_src, "idea_brief missing idea_followup reuse")
    fail(failures, "--block" in brief_src and "paste_block" in brief_src, "idea_brief missing --block paste body")
    fail(failures, "idea_brief.py" in human, "human_session missing idea_brief.py")
    fail(failures, "idea_brief.py" in human and "--block" in human, "human_session missing idea_brief.py --block")
    fail(failures, f"videos/{FOLDER}" in human, f"human_session missing {FOLDER}")
    fail(failures, TITLE in human, "human_session missing Q1 title")


def main() -> int:
    failures: list[str] = []
    fail(failures, (TOOLS / "idea_brief.py").is_file(), "missing tools/idea_brief.py")
    fail(failures, (ROOT / "docs" / "human_session.md").is_file(), "missing docs/human_session.md")
    fail(failures, (ROOT / "docs" / "topic_queue.md").is_file(), "missing docs/topic_queue.md")
    if any("missing" in f for f in failures):
        print("IDEA BRIEF CONTRACT FAIL")
        for f in failures:
            print(f"  - {f}")
        return 1

    source_locks(failures)
    rows = parse_queue((ROOT / "docs" / "topic_queue.md").read_text(encoding="utf-8"))
    q1 = next((r for r in rows if r.get("id") == "Q1"), None)
    fail(failures, q1 is not None, "Q1 missing from topic_queue")
    mechanism = q1["one_line"] if q1 else ""

    blank = (
        "# Idea\n\n"
        "- topic:\n"
        "- problem:\n"
        "- mechanism (the system, not the pep talk):\n"
    )
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / FOLDER
        path.mkdir()
        idea = path / "idea.md"
        idea.write_text(blank, encoding="utf-8")
        (path / "packet.md").write_text(
            f"- id: 002\n- slug: stop-deciding-what-to-work-on-every-morning\n"
            f"- working_title: {TITLE}\n- status: draft\n",
            encoding="utf-8",
        )
        before = sha(idea)
        proc = subprocess.run(
            [sys.executable, str(TOOLS / "idea_brief.py"), str(path)],
            capture_output=True,
            text=True,
        )
        after = sha(idea)
        out = proc.stdout
        fail(failures, proc.returncode == 0, f"idea_brief exit {proc.returncode}: {proc.stderr}")
        fail(failures, before == after and before != "", "idea_brief mutated idea.md")
        fail(failures, TITLE in out, "stdout missing Q1 title")
        fail(failures, Q1_PROBLEM in out, "stdout missing Q1 problem")
        fail(failures, mechanism in out, "stdout missing Q1 mechanism")
        fail(failures, "does not write idea.md" in out.lower() or "writes nothing" in out.lower(), "stdout missing no-write note")
        fail(failures, "(blank)" in out, "stdout missing blank current fields")
        fail(failures, "# Idea" in out, "default stdout missing paste-ready # Idea block")

        block = subprocess.run(
            [sys.executable, str(TOOLS / "idea_brief.py"), str(path), "--block"],
            capture_output=True,
            text=True,
        )
        after_block = sha(idea)
        bout = block.stdout
        fail(failures, block.returncode == 0, f"idea_brief --block exit {block.returncode}: {block.stderr}")
        fail(failures, before == after_block, "idea_brief --block mutated idea.md")
        fail(failures, bout.startswith("# Idea"), "--block must start with # Idea")
        fail(failures, f"- topic: {TITLE}" in bout, "--block missing topic line")
        fail(failures, f"- problem: {Q1_PROBLEM}" in bout, "--block missing problem line")
        fail(failures, f"- mechanism (the system, not the pep talk): {mechanism}" in bout, "--block missing mechanism line")
        fail(failures, "writes nothing" in bout.lower(), "--block missing no-write note")
        fail(failures, "Current idea.md:" not in bout, "--block should not print current-vs-suggested wrapper")

    print("Idea brief contract")
    print("reprint recover stays read-only; --block prints a paste body; idea.md stays unchanged")
    if failures:
        print("IDEA BRIEF CONTRACT FAIL")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("IDEA BRIEF CONTRACT PASS")
    print("This command writes nothing in videos/ and does not write idea.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
