#!/usr/bin/env python3
"""Source-shape lock for write_path_contract.py.

Run 066 recorded WRITE PATH CONTRACT PASS while the committed file
was only a module docstring (986 bytes, no def main). This checker
lives in a separate file so an emptied write_path_contract.py cannot
claim PASS by being executed.

Writes nothing. Does not import apply_script or set_status.
Does not touch videos/.
"""

from __future__ import annotations

from pathlib import Path

TOOLS = Path(__file__).resolve().parent
TARGET = TOOLS / "write_path_contract.py"
MIN_BYTES = 8000
REQUIRED = (
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
)


def check(path: Path = TARGET) -> list[str]:
    failures: list[str] = []
    if not path.is_file():
        return [f"missing {path.name}"]
    data = path.read_bytes()
    size = len(data)
    if size < MIN_BYTES:
        failures.append(f"{path.name} is {size} bytes; need >= {MIN_BYTES} (docstring-only regression)")
    text = data.decode("utf-8", errors="replace")
    if text.lstrip().startswith('"""') and "def main" not in text:
        failures.append(f"{path.name} looks like a docstring-only file")
    for marker in REQUIRED:
        if marker not in text:
            failures.append(f"{path.name} missing marker: {marker}")
    return failures


def main() -> int:
    failures = check()
    print(f"Target: {TARGET.name}")
    print(f"Bytes: {TARGET.stat().st_size if TARGET.is_file() else 0}")
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
