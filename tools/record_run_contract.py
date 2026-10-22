#!/usr/bin/env python3
"""Lock the same-process log writer. A later prepend must not skip compact."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "record_run.py"


def fail(msg: str) -> int:
    print(f"FAIL: {msg}", file=sys.stderr)
    return 1


def main() -> int:
    text = TOOL.read_text(encoding="utf-8")
    if "compact_all.py" not in text:
        return fail("record_run.py must call compact_all.py")
    if "gh secret" in text or "youtube" in text.lower():
        return fail("record_run.py must not poll or call YouTube")
    selftest = (ROOT / "tools" / "selftest.py").read_text(encoding="utf-8")
    if "check_compact_all()" not in selftest:
        return fail("selftest must call check_compact_all()")
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "tools").mkdir()
        (root / "docs").mkdir()
        (root / "STATE.md").write_text("# STATE\n\n## Run 1 delta\n- old\n")
        (root / "NEXT.md").write_text(
            "# NEXT\n\nOlder next actions live in `docs/next_archive.md`. Do not paste the archive back.\n\n1. old\n"
        )
        (root / "RUNS.md").write_text("# RUNS\n\n## Run 1 — old\n- old\n")
        (root / "PROGRESS.md").write_text("# PROGRESS\n\n## Run 1 — old\n- old\n")
        (root / "FAILURES.md").write_text("# FAILURES\n\n## Run 1 — old\n- old\n")
        for name in ("state_archive.md", "next_archive.md", "runs_archive.md", "progress_archive.md", "failures_archive.md"):
            (root / "docs" / name).write_text(f"# {name}\n\n")
        note = root / "note.json"
        note.write_text(
            '{"updated":"Updated: 2026-10-07T16:13:00Z (Run 2)",'
            '"state":"## Run 2 delta\\n- new",'
            '"next":"2. new note",'
            '"runs":"## Run 2 — 2026-10-07T16:13:00Z\\n- new",'
            '"progress":"## Run 2 — 2026-10-07T16:13:00Z\\n- new",'
            '"failures":"## Run 2 — 2026-10-07T16:13:00Z\\n- new"}'
        )
        # Compact tools live in the real repo. Point the contract at source behavior only
        # when the fake root cannot import them. Source lock above is the gate.
        proc = subprocess.run(
            [sys.executable, str(TOOL), "--note", str(note), "--root", str(root)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        # Fake root has no compact_all.py, so compact must fail closed.
        if proc.returncode == 0:
            return fail("record_run accepted a root with no compact_all.py")
        if "Run 2 delta" not in (root / "STATE.md").read_text():
            return fail("state prepend did not land before compact refused")
        nxt = (root / "NEXT.md").read_text()
        if "Updated: 2026-10-07T16:13:00Z (Run 2)" not in nxt:
            return fail("NEXT header was not refreshed from the note")
        if nxt.count("Updated:") != 1:
            return fail("NEXT grew a second Updated line")
    print("RECORD RUN CONTRACT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
