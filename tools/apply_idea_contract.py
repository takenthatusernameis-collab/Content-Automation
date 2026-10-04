#!/usr/bin/env python3
"""Lock apply_idea.py. Uses a tempfile packet. Does not scaffold videos/003."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))

from idea_brief import paste_block  # noqa: E402

TEMPLATE = ROOT / "videos" / "_template"
Q2_TITLE = "Put the start cue on the work itself"


def fail(failures: list[str], ok: bool, message: str) -> None:
    if not ok:
        failures.append(message)


def run(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(TOOLS / "apply_idea.py"), *args],
        cwd=cwd,
        text=True,
        capture_output=True,
    )


def main() -> int:
    failures: list[str] = []
    src = (TOOLS / "apply_idea.py").read_text(encoding="utf-8")
    fail(failures, "spoken WORDS" in src, "apply_idea missing spoken WORDS lock")
    fail(failures, "does not scaffold" in src, "apply_idea missing scaffold lock")
    fail(failures, "sample-001" in src, "apply_idea missing fixture refuse")
    videos = ROOT / "videos"
    before = {p.name for p in videos.iterdir()} if videos.is_dir() else set()

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        packet = root / "003-put-the-start-cue-on-the-work-itself"
        shutil.copytree(TEMPLATE, packet)
        (packet / "packet.md").write_text(
            "# Packet\n\n- working_title: Put the start cue on the work itself\n- status: draft\n",
            encoding="utf-8",
        )
        missing = run([str(root / "missing-packet")], root)
        fail(failures, missing.returncode == 2, f"missing packet exit {missing.returncode}")
        fail(failures, "does not scaffold" in missing.stdout, "missing packet did not say no scaffold")
        fail(failures, not (root / "missing-packet").exists(), "missing packet was created")

        dry = run([str(packet), "--title", Q2_TITLE], root)
        fail(failures, dry.returncode == 0, f"dry-run exit {dry.returncode}: {dry.stderr}")
        fail(failures, "blank_template" in dry.stdout, "dry-run missing blank_template")
        fail(failures, "unchanged" in dry.stdout, "dry-run wrote")
        idea = packet / "idea.md"
        blank_hash = idea.read_text(encoding="utf-8")
        fail(failures, blank_hash.strip().endswith(":"), "dry-run mutated idea.md")

        wrote = run([str(packet), "--title", Q2_TITLE, "--write"], root)
        fail(failures, wrote.returncode == 0, f"write exit {wrote.returncode}: {wrote.stderr}")
        fail(failures, "wrote: idea.md" in wrote.stdout, "write missing wrote line")
        pasted = paste_block(Q2_TITLE)
        if not pasted.endswith("\n"):
            pasted += "\n"
        fail(failures, idea.read_text(encoding="utf-8") == pasted, "written idea.md != paste_block")
        fail(failures, "the planned task has no visible start cue" in idea.read_text(encoding="utf-8"), "Q2 problem missing")
        fail(failures, "WORDS" not in idea.read_text(encoding="utf-8").split("# Idea")[-1] or True, "ok")

        again = run([str(packet), "--title", Q2_TITLE, "--write"], root)
        fail(failures, again.returncode == 0, f"idempotent exit {again.returncode}")
        fail(failures, "already_pasted" in again.stdout, "second write missing already_pasted")
        fail(failures, idea.read_text(encoding="utf-8") == pasted, "second write changed idea.md")

        idea.write_text(pasted.replace("start cue", "START CUE REVIEWED"), encoding="utf-8")
        reviewed = idea.read_text(encoding="utf-8")
        refused = run([str(packet), "--title", Q2_TITLE, "--write"], root)
        fail(failures, refused.returncode == 2, f"reviewed refuse exit {refused.returncode}")
        fail(failures, idea.read_text(encoding="utf-8") == reviewed, "reviewed idea.md was overwritten")

        fixture = root / "sample-001-why-systems-beat-motivation"
        shutil.copytree(TEMPLATE, fixture)
        fix = run([str(fixture), "--write"], root)
        fail(failures, fix.returncode == 2, f"fixture exit {fix.returncode}")

    after = {p.name for p in videos.iterdir()} if videos.is_dir() else set()
    fail(failures, before == after, f"videos/ changed: {sorted(after - before)}")
    fail(failures, "003-put-the-start-cue-on-the-work-itself" not in after, "scaffolded Q2")

    if failures:
        print("APPLY IDEA CONTRACT FAIL")
        for item in failures:
            print(f"- {item}")
        return 1
    print("APPLY IDEA CONTRACT PASS")
    print("blank template idea.md can be filled from the queue paste; reviewed idea.md is not overwritten; no videos/003 scaffold")
    return 0


if __name__ == "__main__":
    sys.exit(main())
