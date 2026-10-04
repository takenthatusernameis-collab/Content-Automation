#!/usr/bin/env python3
"""Contract check for the blank-idea expand gate.

Read-only versus videos/. Uses tempfile only.
Locks:
- idea_mechanism_blank is true on empty / template-default / generic / tbd / todo
- idea_mechanism_blank is false on a real system sentence
- next_action.recommend returns fill-idea before write-script when mechanism is blank
- hint.commands_for(fill-idea) first live command is doctor, not expand_prompt
- expand_prompt / next_action / hint source still mention the gate

Does not write idea.md, script.md, the queue, or sample-001.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from expand_prompt import idea_mechanism_blank  # noqa: E402
from hint import commands_for  # noqa: E402
from next_action import recommend  # noqa: E402


def fail(failures: list[str], cond: bool, msg: str) -> None:
    if not cond:
        failures.append(msg)


def first_live(cmds: list[str]) -> str | None:
    for c in cmds:
        s = c.strip()
        if s and not s.startswith("#"):
            return s
    return None


def source_locks(failures: list[str]) -> None:
    expand_src = (TOOLS / "expand_prompt.py").read_text(encoding="utf-8")
    next_src = (TOOLS / "next_action.py").read_text(encoding="utf-8")
    hint_src = (TOOLS / "hint.py").read_text(encoding="utf-8")
    fail(failures, "def idea_mechanism_blank" in expand_src, "expand_prompt missing idea_mechanism_blank")
    fail(failures, "fill-idea" in next_src, "next_action missing fill-idea")
    fail(failures, "idea_mechanism_blank" in next_src, "next_action missing idea_mechanism_blank call")
    fail(failures, 'code == "fill-idea"' in hint_src, "hint missing fill-idea map")
    block = ""
    if 'if code == "fill-idea":' in hint_src:
        block = hint_src.split('if code == "fill-idea":', 1)[1].split("if code", 1)[0]
    fail(failures, "doctor.py" in block, f"hint fill-idea block missing doctor.py: {block!r}")
    fail(failures, "apply_idea.py" in block, f"hint fill-idea block missing apply_idea.py: {block!r}")
    fail(failures, "paste that" not in block and "paste into" not in block, f"hint fill-idea still tells a hand paste: {block!r}")


def blank_cases() -> list[str]:
    return [
        "# Idea\n\n- topic:\n- mechanism (the system, not the pep talk):\n",
        "# Idea\n\n- mechanism: template-default\n",
        "# Idea\n\n- mechanism (the system, not the pep talk): generic\n",
        "# Idea\n\n- mechanism: TBD\n",
        "# Idea\n\n- mechanism: todo\n",
        "",
    ]


def main() -> int:
    failures: list[str] = []
    source_locks(failures)

    for text in blank_cases():
        fail(
            failures,
            idea_mechanism_blank(text),
            f"expected blank mechanism for {text!r}",
        )
    filled = (
        "# Idea\n\n- topic: Stop deciding what to work on every morning\n"
        "- mechanism (the system, not the pep talk): "
        "Install a written next-action default so the morning does not reopen the whole list.\n"
    )
    fail(failures, not idea_mechanism_blank(filled), "filled Q1 mechanism treated as blank")

    row = {
        "status": "draft",
        "errors": [],
        "drift": [],
        "incompletes": ["hook WORDS empty"],
    }
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "002-stop-deciding-what-to-work-on-every-morning"
        path.mkdir()
        (path / "idea.md").write_text(blank_cases()[0], encoding="utf-8")
        (path / "packet.md").write_text(
            "- id: 002\n- slug: stop-deciding-what-to-work-on-every-morning\n- status: draft\n",
            encoding="utf-8",
        )
        code, why = recommend(path, row)
        fail(failures, code == "fill-idea", f"blank idea expected fill-idea, got {code} ({why})")
        cmds = commands_for(path, row, code)
        live = first_live(cmds)
        fail(failures, live is not None, "fill-idea hint produced no live command")
        if live:
            fail(failures, "--write" not in live, f"first live command has --write: {live}")
            fail(
                failures,
                "expand_prompt" not in live,
                f"first live command is expand_prompt: {live}",
            )
            fail(failures, "doctor.py" in live, f"first live command should be doctor: {live}")
        fail(
            failures,
            not any("expand_prompt.py" in c and not c.strip().startswith("#") for c in cmds),
            f"fill-idea hint still prints live expand_prompt: {cmds}",
        )

        (path / "idea.md").write_text(filled, encoding="utf-8")
        code2, why2 = recommend(path, row)
        fail(
            failures,
            code2 != "fill-idea",
            f"filled idea still fill-idea: {code2} ({why2})",
        )

    print("Idea gate contract")
    print("blank mechanism => fill-idea; hint live command is doctor")
    print("filled mechanism => not fill-idea")
    print("expand_prompt / next_action / hint source still name the gate")
    if failures:
        print("IDEA GATE CONTRACT FAIL")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("IDEA GATE CONTRACT PASS")
    print("This command writes nothing in videos/ and does not write idea.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
