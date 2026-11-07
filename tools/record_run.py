#!/usr/bin/env python3
"""Prepend one run note, then compact the live logs in the same process.

Run 378 passed selftest and then prepended a 13th section. Actions run
37580716646 failed the 12-section cap. Run 380 added compact_all.py, but
selftest never called it. This writer is the path that cannot skip compact.
It does not poll secrets, does not dispatch a workflow, and does not write packets.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _insert_after_header(text: str, header: str, block: str) -> str:
    if not text.startswith(header):
        raise ValueError(f"missing header {header}")
    rest = text[len(header) :]
    if not rest.startswith("\n"):
        rest = "\n" + rest
    return header + "\n\n" + block.strip() + "\n\n" + rest.lstrip("\n")


def prepend_state(text: str, updated: str, delta: str) -> str:
    block = updated.strip() + "\n\n" + delta.strip()
    return _insert_after_header(text, "# STATE", block)


def prepend_next(text: str, item: str, updated: str = "") -> str:
    marker = "Older next actions live in `docs/next_archive.md`."
    idx = text.find(marker)
    if idx < 0:
        raise ValueError("NEXT archive marker missing")
    line_end = text.find("\n", idx)
    if line_end < 0:
        raise ValueError("NEXT archive marker has no line end")
    head = text[: line_end + 1]
    tail = text[line_end + 1 :]
    stamp = updated.strip()
    if stamp:
        lines = head.splitlines()
        replaced = False
        out = []
        for line in lines:
            if line.startswith("Updated:") and not replaced:
                out.append(stamp)
                replaced = True
            else:
                out.append(line)
        if not replaced:
            # Keep a single header. Insert the stamp after # NEXT.
            if out and out[0].startswith("# NEXT"):
                out = [out[0], "", stamp, *out[1:]]
            else:
                out.insert(0, stamp)
        head = "\n".join(out)
        if not head.endswith("\n"):
            head += "\n"
    return head + "\n" + item.strip() + "\n\n" + tail.lstrip("\n")


def prepend_runs(text: str, section: str) -> str:
    header = "# RUNS"
    if not text.startswith(header):
        # Restore a missing header so compact history does not break recording.
        text = header + "\n\n" + text.lstrip()
    return _insert_after_header(text, header, section)


def prepend_log(text: str, header: str, section: str) -> str:
    if not text.startswith(header):
        # Restore a missing header so compact history does not break recording.
        text = header + "\n\n" + text.lstrip()
    return _insert_after_header(text, header, section)


def apply(root: Path, note: dict) -> None:
    state = root / "STATE.md"
    nxt = root / "NEXT.md"
    runs = root / "RUNS.md"
    progress = root / "PROGRESS.md"
    failures = root / "FAILURES.md"
    state.write_text(prepend_state(state.read_text(), note["updated"], note["state"]))
    nxt.write_text(prepend_next(nxt.read_text(), note["next"], note["updated"]))
    runs.write_text(prepend_runs(runs.read_text(), note["runs"]))
    progress.write_text(prepend_log(progress.read_text(), "# PROGRESS", note["progress"]))
    failures.write_text(prepend_log(failures.read_text(), "# FAILURES", note["failures"]))


def compact(root: Path) -> int:
    proc = subprocess.run(
        [sys.executable, str(root / "tools" / "compact_all.py")],
        cwd=root,
        text=True,
    )
    return proc.returncode


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--note", required=True, help="JSON file with updated/state/next/runs/progress/failures")
    parser.add_argument("--root", default=str(ROOT))
    args = parser.parse_args()
    root = Path(args.root)
    note = json.loads(Path(args.note).read_text())
    required = ("updated", "state", "next", "runs", "progress", "failures")
    missing = [key for key in required if not str(note.get(key, "")).strip()]
    if missing:
        print("RECORD RUN REFUSE missing=" + ",".join(missing), file=sys.stderr)
        return 2
    if "secret" in json.dumps(note).lower() and "do not poll" not in json.dumps(note).lower():
        print("RECORD RUN REFUSE secret-shaped note", file=sys.stderr)
        return 2
    apply(root, note)
    code = compact(root)
    if code != 0:
        print("RECORD RUN FAIL compact", file=sys.stderr)
        return code
    print("RECORD RUN OK compacted=1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
