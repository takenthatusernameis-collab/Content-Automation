#!/usr/bin/env python3
"""Run all tools/*_contract.py reliability locks in one command.

Discovers every *_contract.py under tools/, executes each with a short timeout,
and prints a unified PASS / FAIL summary. Exit 0 only if every contract exits 0.
Does not invent data, write packets, poll secrets, or dispatch. Soft only.

Reduces future labor: any run (or human) can verify the entire set of fail-closed
locks that protect research, queue, experiment, media, and metadata paths with a
single invocation instead of hunting individual contracts.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
TIMEOUT = 30  # seconds per contract; most are pure and finish in <2s


def discover_contracts() -> list[Path]:
    found = sorted(TOOLS.glob("*_contract.py"))
    # Exclude this file itself if it is ever renamed into the pattern
    return [p for p in found if p.name != Path(__file__).name]


def run_one(path: Path) -> tuple[int, str]:
    try:
        proc = subprocess.run(
            [sys.executable, str(path)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
            check=False,
        )
        out = ((proc.stdout or "") + "\n" + (proc.stderr or "")).strip()
        return proc.returncode, out[:600] + ("..." if len(out) > 600 else "")
    except subprocess.TimeoutExpired:
        return 1, f"TIMEOUT after {TIMEOUT}s"
    except Exception as exc:  # noqa: BLE001
        return 1, f"EXCEPTION {type(exc).__name__}: {exc}"


def main() -> int:
    contracts = discover_contracts()
    if not contracts:
        print("CONTRACTS SUITE: no *_contract.py files found")
        return 1

    print("CONTRACTS SUITE (all reliability locks; no invent, no write, no secrets)")
    print(f"discovered: {len(contracts)} contracts")
    print()

    failures: list[str] = []
    for path in contracts:
        code, snippet = run_one(path)
        status = "PASS" if code == 0 else "FAIL"
        print(f"[{status}] {path.name} (exit {code})")
        if code != 0:
            failures.append(path.name)
            if snippet:
                print(f"    {snippet.splitlines()[0] if snippet else ''}")

    print()
    if failures:
        print(f"UNIFIED RESULT: FAIL ({len(failures)} / {len(contracts)})")
        print("Failed:", ", ".join(failures))
        return 1

    print(f"UNIFIED RESULT: PASS ({len(contracts)} / {len(contracts)})")
    print("All fail-closed contracts remain locked. Safe to continue.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
