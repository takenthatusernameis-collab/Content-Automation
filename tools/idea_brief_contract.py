#!/usr/bin/env python3
"""Contract check for idea_brief reprint recover.

Read-only versus videos/. Uses tempfile only.
Locks:
- idea_brief source says it does not write idea.md
- human_session names idea_brief.py and the pinned 002 folder
- human_session names idea_brief.py --block
- human_session names idea_brief.py --check
- running idea_brief on a blank 002 packet reprints Q1 topic + Q1_PROBLEM + one_line
- default reprint prints exact --block and --check commands with the packet folder
- idea_brief --block prints a paste-ready idea.md body with those fields
- idea_brief --check on blank idea.md exits 2 and does not write
- PASTE INCOMPLETE stdout includes python3 tools/idea_brief.py PATH --block
- idea_brief --check after a tempfile paste of that body exits 0 and does not write
- PASTE READY stdout includes python3 tools/expand_prompt.py and the packet folder
- PASTE READY stdout includes dry-run apply_script --from PATH/draft.md (no --write)
- idea.md bytes are unchanged after default, --block, and --check runs
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
    fail(failures, "--check" in brief_src and "check_fields" in brief_src, "idea_brief missing --check compare")
    fail(failures, "expand_command" in brief_src, "idea_brief missing expand_command helper")
    fail(failures, "block_command" in brief_src, "idea_brief missing block_command helper")
    fail(failures, "check_command" in brief_src, "idea_brief missing check_command helper")
    fail(failures, "apply_command" in brief_src, "idea_brief missing apply_command helper")
    fail(failures, "draft_path" in brief_src, "idea_brief missing draft_path helper")
    fail(failures, "idea_brief.py" in human, "human_session missing idea_brief.py")
    fail(failures, "idea_brief.py" in human and "--block" in human, "human_session missing idea_brief.py --block")
    fail(failures, "idea_brief.py" in human and "--check" in human, "human_session missing idea_brief.py --check")
    fail(failures, "expand_prompt.py" in human, "human_session missing expand_prompt.py")
    fail(failures, "apply_script.py" in human, "human_session missing apply_script.py")
    fail(failures, "draft.md" in human, "human_session missing draft.md convention")
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
        fail(failures, "--check" in out, "default stdout missing --check hint")
        fail(failures, "idea_brief.py" in out and "--check" in out and FOLDER in out, "default reprint missing exact --check command with folder")
        fail(failures, "idea_brief.py" in out and "--block" in out and FOLDER in out, "default reprint missing exact --block command with folder")

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

        chk_blank = subprocess.run(
            [sys.executable, str(TOOLS / "idea_brief.py"), str(path), "--check"],
            capture_output=True,
            text=True,
        )
        after_chk_blank = sha(idea)
        cout = chk_blank.stdout
        fail(failures, chk_blank.returncode == 2, f"idea_brief --check on blank exit {chk_blank.returncode}, want 2")
        fail(failures, before == after_chk_blank, "idea_brief --check on blank mutated idea.md")
        fail(failures, "PASTE INCOMPLETE" in cout, "--check blank missing PASTE INCOMPLETE")
        fail(failures, "writes nothing" in cout.lower(), "--check blank missing no-write note")
        fail(failures, "MISMATCH" in cout, "--check blank missing MISMATCH")
        fail(failures, "python3 tools/idea_brief.py" in cout and "--block" in cout, "--check PASTE INCOMPLETE missing --block command")
        fail(failures, FOLDER in cout, "--check PASTE INCOMPLETE missing packet folder in --block command")

        from idea_brief import paste_block

        pasted = paste_block(TITLE)
        idea.write_text(pasted, encoding="utf-8")
        pasted_hash = sha(idea)
        chk_ok = subprocess.run(
            [sys.executable, str(TOOLS / "idea_brief.py"), str(path), "--check"],
            capture_output=True,
            text=True,
        )
        after_chk_ok = sha(idea)
        oout = chk_ok.stdout
        fail(failures, chk_ok.returncode == 0, f"idea_brief --check after paste exit {chk_ok.returncode}: {chk_ok.stderr}")
        fail(failures, pasted_hash == after_chk_ok, "idea_brief --check after paste mutated idea.md")
        fail(failures, "PASTE READY" in oout, "--check after paste missing PASTE READY")
        fail(failures, oout.count("MATCH ") >= 3, "--check after paste missing three MATCH lines")
        fail(failures, "writes nothing" in oout.lower(), "--check after paste missing no-write note")
        fail(failures, "python3 tools/expand_prompt.py" in oout, "--check PASTE READY missing expand_prompt command")
        fail(failures, FOLDER in oout, "--check PASTE READY missing packet folder in expand command")
        fail(failures, "Do not treat expand_prompt stdout as script.md." in oout, "--check PASTE READY missing expand stdout warning")
        fail(failures, "python3 tools/apply_script.py" in oout and "--from" in oout and "draft.md" in oout, "--check PASTE READY missing apply_script --from draft.md")
        fail(failures, "--from FILE" not in oout, "--check PASTE READY must use draft.md not FILE")
        fail(failures, "--write" not in oout, "--check PASTE READY must not print --write")
        fail(failures, "Save the off-repo draft" in oout, "--check PASTE READY missing draft.md save line")

    print("Idea brief contract")
    print("reprint recover stays read-only; --block prints a paste body; --check compares without writing; INCOMPLETE prints --block; PASTE READY prints expand_prompt then apply_script --from draft.md")
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
