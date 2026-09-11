#!/usr/bin/env python3
"""Source-shape lock for the write-path trio.

Run 066 recorded WRITE PATH CONTRACT PASS while write_path_contract.py
was only a module docstring. Run 068 put the witness in this file so
an emptied contract cannot claim PASS by being executed.

Run 069 also witnesses apply_script.py and set_status.py. Those two
files are what write_path_contract subprocess-runs. A missing or
docstring-only sibling would make a runtime PASS impossible or
misleading, and a lock that only inspects write_path_contract.py
cannot see that.

Writes nothing. Does not import apply_script or set_status.
Does not touch videos/.
"""

from __future__ import annotations

from pathlib import Path

TOOLS = Path(__file__).resolve().parent

CHECKS: list[tuple[str, int, tuple[str, ...]]] = [
    (
        "write_path_contract.py",
        8000,
        (
            "def main",
            "subprocess",
            "TemporaryDirectory",
            "WRITE PATH CONTRACT PASS",
            "WRITE PATH CONTRACT FAIL",
            "if __name__",
            "draft.md",
            "ready_for_vo",
            "in-band",
            "--write --refresh",
        ),
    ),
    (
        "apply_script.py",
        4000,
        (
            "def main",
            "if __name__",
            "--from",
            "draft.md",
            "--write",
            "--refresh",
            "sample-001",
        ),
    ),
    (
        "set_status.py",
        3000,
        (
            "def main",
            "if __name__",
            "ready_for_vo",
            "--to",
            "--write",
            "sample-001",
        ),
    ),
]


def check_one(name: str, min_bytes: int, markers: tuple[str, ...]) -> list[str]:
    path = TOOLS / name
    failures: list[str] = []
    if not path.is_file():
        return [f"missing {name}"]
    data = path.read_bytes()
    size = len(data)
    if size < min_bytes:
        failures.append(
            f"{name} is {size} bytes; need >= {min_bytes} (docstring-only regression)"
        )
    text = data.decode("utf-8", errors="replace")
    if text.lstrip().startswith('"""') and "def main" not in text:
        failures.append(f"{name} looks like a docstring-only file")
    for marker in markers:
        if marker not in text:
            failures.append(f"{name} missing marker: {marker}")
    return failures


def check() -> list[str]:
    failures: list[str] = []
    for name, min_bytes, markers in CHECKS:
        failures.extend(check_one(name, min_bytes, markers))
    return failures


def main() -> int:
    print("Shape lock: write_path_contract.py + apply_script.py + set_status.py")
    for name, _, _ in CHECKS:
        path = TOOLS / name
        size = path.stat().st_size if path.is_file() else 0
        print(f"  {name}: {size} bytes")
    failures = check()
    if failures:
        print("CONTRACT SHAPE FAIL")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("CONTRACT SHAPE PASS")
    print("This command writes nothing and does not run apply_script or set_status.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
