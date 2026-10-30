#!/usr/bin/env python3
"""Lock pipeline_entry.py stage selection by file presence.

Uses tempfile packets. Does not touch live videos/. Does not invent content.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))

TEMPLATE = ROOT / "videos" / "_template"


def fail(failures: list[str], ok: bool, message: str) -> None:
    if not ok:
        failures.append(message)


def run_entry(packet: Path) -> str:
    proc = subprocess.run(
        [sys.executable, str(TOOLS / "pipeline_entry.py"), str(packet)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    return proc.stdout


def main() -> int:
    failures: list[str] = []
    src = (TOOLS / "pipeline_entry.py").read_text(encoding="utf-8")
    fail(failures, "no invent" in src.lower() or "no-invent" in src, "pipeline_entry missing no-invent lock")
    fail(failures, "no write" in src.lower() or "no-write" in src, "pipeline_entry missing no-write lock")
    fail(failures, "after_upload_steps" in src, "pipeline_entry missing after_upload pointer")
    fail(failures, "media_pipeline_steps" in src, "pipeline_entry missing media pointer")
    fail(failures, "script_promotion_steps" in src, "pipeline_entry missing script pointer")
    fail(failures, "early_pipeline_steps" in src, "pipeline_entry missing early pointer")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)

        # Newly scaffolded: no idea.md, no draft, no script
        packet = root / "003-test-scaffold"
        shutil.copytree(TEMPLATE, packet)
        for name in ("idea.md", "draft.md", "script.md"):
            (packet / name).unlink(missing_ok=True)
        out = run_entry(packet)
        fail(failures, "newly scaffolded" in out.lower(), "scaffold stage not detected")
        fail(failures, "early_pipeline_steps" in out, "scaffold should point to early")

        # Idea filled
        (packet / "idea.md").write_text("# Idea\n\n- topic: test\n")
        out = run_entry(packet)
        fail(failures, "early pipeline" in out.lower(), "idea stage not detected")
        fail(failures, "early_pipeline_steps" in out, "idea should point to early")

        # Draft exists
        (packet / "draft.md").write_text("# Draft\n\nWORDS here\n")
        out = run_entry(packet)
        fail(failures, "script promotion" in out.lower(), "draft stage not detected")
        fail(failures, "script_promotion_steps" in out, "draft should point to script promotion")

        # Script exists
        (packet / "script.md").write_text("# Script\n\nWORDS\n")
        out = run_entry(packet)
        fail(failures, "media" in out.lower(), "script stage not detected")
        fail(failures, "media_pipeline_steps" in out, "script should point to media")

        # Upload state
        (packet / "upload_state.json").write_text('{"provider_video_id": "test"}\n')
        out = run_entry(packet)
        fail(failures, "post-upload" in out.lower(), "upload stage not detected")
        fail(failures, "after_upload_steps" in out, "upload should point to after_upload")

    if failures:
        print("pipeline_entry_contract FAIL")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("pipeline_entry_contract PASS")
    print("Stage selection by file presence locked. No live packet writes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
