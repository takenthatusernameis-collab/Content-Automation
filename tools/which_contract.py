#!/usr/bin/env python3
"""Read-only map from edited tools to the contract that must be run.

Does not write videos/, docs/, or packet.md.
Does not import packet writers.
Optional --run executes contracts whose required files exist; missing
dependencies print SKIP and do not fail the map itself.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent

# tool basename (or path suffix) -> contract script basename
MAP: list[tuple[tuple[str, ...], str, tuple[str, ...]]] = [
    (
        ("validate_packet.py", "pipeline_status.py", "next_action.py", "hint.py", "selftest.py"),
        "selftest.py",
        (
            "selftest.py",
            "validate_packet.py",
            "pipeline_status.py",
            "next_action.py",
            "hint.py",
            "set_status.py",
            "apply_script.py",
            "render_brief.py",
            "caption_brief.py",
        ),
    ),
    (
        ("queue_lib.py", "queue_status.py", "mark_topic.py", "next_topic.py", "queue_contract.py"),
        "queue_contract.py",
        ("queue_contract.py", "queue_lib.py", "queue_status.py", "mark_topic.py"),
    ),
    (
        ("apply_script.py", "set_status.py", "write_path_contract.py"),
        "write_path_contract.py",
        (
            "write_path_contract.py",
            "apply_script.py",
            "set_status.py",
            "validate_packet.py",
            "pipeline_status.py",
            "caption_brief.py",
            "render_brief.py",
        ),
    ),
    (
        ("new_packet.py", "after_scaffold.py", "scaffold_contract.py"),
        "scaffold_contract.py",
        ("scaffold_contract.py", "new_packet.py", "queue_lib.py"),
    ),
]


def contract_for(name: str) -> str | None:
    base = Path(name).name
    for tools, contract, _need in MAP:
        if base == contract or base in tools:
            return contract
    return None


def needed_for(contract: str) -> tuple[str, ...]:
    for _tools, c, need in MAP:
        if c == contract:
            return need
    return ()


def present(names: tuple[str, ...]) -> tuple[list[str], list[str]]:
    have: list[str] = []
    miss: list[str] = []
    for n in names:
        if (TOOLS / n).is_file():
            have.append(n)
        else:
            miss.append(n)
    return have, miss


def print_map() -> None:
    print("Edited tool                         Run")
    print("-" * 60)
    seen: set[str] = set()
    for tools, contract, _need in MAP:
        for t in tools:
            if t in seen:
                continue
            seen.add(t)
            print(f"{t:<35} python3 tools/{contract}")
    print()
    print("selftest.py also needs videos/sample-001-* (see docs/agent_session.md).")
    print("queue_contract.py may read docs/topic_queue.md.")
    print("scaffold_contract.py may read docs/topic_queue.md; uses tempfile only.")
    print("write_path_contract.py uses tempfile only; never writes videos/.")
    print("This command writes nothing.")


def run_one(contract: str) -> int:
    need = needed_for(contract)
    _have, miss = present(need)
    extra_ok = True
    if contract == "selftest.py":
        videos = ROOT / "videos"
        hits = []
        if videos.is_dir():
            hits = [p for p in videos.iterdir() if p.is_dir() and p.name.startswith("sample-001")]
        if not hits:
            miss = list(miss) + ["videos/sample-001-*"]
            extra_ok = False
    if miss or not extra_ok:
        print(f"SKIP {contract}: missing {', '.join(miss)}")
        return 0
    cmd = [sys.executable, str(TOOLS / contract)]
    print(f"RUN {' '.join(cmd)}")
    proc = subprocess.run(cmd, cwd=str(ROOT))
    return int(proc.returncode)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read-only: which contract to run after a tool edit. No writes."
    )
    parser.add_argument(
        "--after",
        metavar="TOOL",
        help="Basename or path of the edited tool (e.g. new_packet.py)",
    )
    parser.add_argument(
        "--run",
        action="store_true",
        help="Run the matching contract if its files exist; SKIP if not. Still no repo writes from this wrapper.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="With --run, try every contract. Missing deps SKIP. Any FAIL exits 1.",
    )
    args = parser.parse_args()

    if args.after:
        contract = contract_for(args.after)
        if contract is None:
            print(f"No contract mapped for {Path(args.after).name}")
            print("Known tools:")
            print_map()
            return 0
        print(f"python3 tools/{contract}")
        if args.run:
            return run_one(contract)
        print("This command writes nothing.")
        return 0

    if args.run and args.all:
        codes = []
        for _tools, contract, _need in MAP:
            codes.append(run_one(contract))
        print_map()
        return 1 if any(c != 0 for c in codes) else 0

    print_map()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
