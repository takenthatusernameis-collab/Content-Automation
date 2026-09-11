#!/usr/bin/env python3
"""Unmapped lock against placeholder or emptied critical tools.

Run 066 committed write_path_contract.py as a docstring-only file.
Run 076 committed words.py as an 8-byte / placeholder blob before restore.
This file fails those shapes across the high-risk set without mapping
needed.py and without writing under videos/.

It is not a reconstruct wave. It does not run apply_script or set_status.
It does not treat PASS as Q1 scaffold or apply --write.
"""

from __future__ import annotations

from pathlib import Path

TOOLS = Path(__file__).resolve().parent

# Token split so this file itself is not flagged as a placeholder body.
BAD_EXACT = frozenset({"see-next", "404: Not Found"})
BAD_NEEDLE = "PLACE" + "HOLDER"

# name, min_bytes, required markers
CHECKS: list[tuple[str, int, tuple[str, ...]]] = [
    (
        "words.py",
        8000,
        ("def cut_line", "def grow_line", "This command writes nothing."),
    ),
    (
        "words_contract.py",
        3000,
        ("WORDS CONTRACT PASS", "def main", "MIN_BYTES"),
    ),
    (
        "write_path_contract.py",
        8000,
        ("def main", "WRITE PATH CONTRACT PASS", "ready_for_vo"),
    ),
    (
        "apply_script.py",
        4000,
        ("def main", "--write", "draft.md"),
    ),
    (
        "set_status.py",
        3000,
        ("def main", "ready_for_vo", "--to"),
    ),
    (
        "contract_shape.py",
        2000,
        ("CONTRACT SHAPE PASS", "write_path_contract.py", "apply_script.py"),
    ),
    (
        "verify_write_path.py",
        800,
        ("VERIFY WRITE PATH", "contract_shape.py", "write_path_contract.py"),
    ),
]


def looks_placeholder(text: str) -> bool:
    stripped = text.strip()
    if stripped in BAD_EXACT:
        return True
    if BAD_NEEDLE in text:
        return True
    if text.lstrip().startswith('"""') and "def main" not in text and "def cut_line" not in text:
        return True
    return False


def check_one(name: str, min_bytes: int, markers: tuple[str, ...]) -> list[str]:
    path = TOOLS / name
    if not path.is_file():
        return [f"missing {name}"]
    data = path.read_bytes()
    size = len(data)
    failures: list[str] = []
    if size < min_bytes:
        failures.append(f"{name} is {size} bytes; need >= {min_bytes}")
    text = data.decode("utf-8", errors="replace")
    if looks_placeholder(text):
        failures.append(f"{name} looks like a placeholder or docstring-only body")
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
    print("Placeholder guard: high-risk tools size + marker + empty-body check")
    for name, _, _ in CHECKS:
        path = TOOLS / name
        size = path.stat().st_size if path.is_file() else 0
        print(f"  {name}: {size} bytes")
    failures = check()
    if failures:
        print("PLACEHOLDER GUARD FAIL")
        for item in failures:
            print(f"  - {item}")
        return 1
    print("PLACEHOLDER GUARD PASS")
    print("This command writes nothing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
