#!/usr/bin/env python3
"""Read-only reconstruct list for clone-less agent sessions.

Prints the files an agent must fetch before running a named contract.
Does not download, write videos/, or import packet writers.

Uses which_contract.MAP when that file is importable. Extra paths that
live outside tools/ stay in EXTRA here so agent_session and this printer
cannot silently disagree on the sample packet or queue file.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent

# Paths relative to repo root that MAP does not list.
EXTRA: dict[str, tuple[str, ...]] = {
    "selftest.py": (
        "videos/sample-001-why-systems-beat-motivation/packet.md",
        "videos/sample-001-why-systems-beat-motivation/idea.md",
        "videos/sample-001-why-systems-beat-motivation/script.md",
        "videos/sample-001-why-systems-beat-motivation/titles.md",
        "videos/sample-001-why-systems-beat-motivation/thumbnail.md",
        "videos/sample-001-why-systems-beat-motivation/qa.md",
        "videos/sample-001-why-systems-beat-motivation/assets.md",
    ),
    "queue_contract.py": ("docs/topic_queue.md",),
    "scaffold_contract.py": ("docs/topic_queue.md",),
}

FALLBACK_TOOLS: dict[str, tuple[str, ...]] = {
    "selftest.py": (
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
    "queue_contract.py": (
        "queue_contract.py",
        "queue_lib.py",
        "queue_status.py",
        "mark_topic.py",
    ),
    "write_path_contract.py": (
        "write_path_contract.py",
        "apply_script.py",
        "set_status.py",
        "validate_packet.py",
        "pipeline_status.py",
        "caption_brief.py",
        "render_brief.py",
    ),
    "scaffold_contract.py": (
        "scaffold_contract.py",
        "new_packet.py",
        "queue_lib.py",
    ),
    "router_contract.py": ("router_contract.py", "which_contract.py"),
}


def load_map() -> dict[str, tuple[str, ...]]:
    sys.path.insert(0, str(TOOLS))
    try:
        import which_contract as wc  # type: ignore
    except Exception:
        return dict(FALLBACK_TOOLS)
    out: dict[str, tuple[str, ...]] = {}
    for _tools, contract, need in wc.MAP:
        out[contract] = need
    return out


def resolve_name(raw: str, contracts: dict[str, tuple[str, ...]]) -> str | None:
    base = Path(raw).name
    if base in contracts:
        return base
    sys.path.insert(0, str(TOOLS))
    try:
        import which_contract as wc  # type: ignore

        mapped = wc.contract_for(base)
        if mapped:
            return mapped
    except Exception:
        pass
    return None


def paths_for(contract: str, contracts: dict[str, tuple[str, ...]]) -> list[str]:
    need = contracts.get(contract, ())
    rows = [f"tools/{n}" for n in need]
    for extra in EXTRA.get(contract, ()):
        if extra not in rows:
            rows.append(extra)
    return rows


def print_one(contract: str, contracts: dict[str, tuple[str, ...]]) -> None:
    rows = paths_for(contract, contracts)
    print(f"# {contract}")
    print(f"python3 tools/{contract}")
    for p in rows:
        print(p)
    print()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read-only: files to reconstruct before a contract. No writes."
    )
    parser.add_argument(
        "name",
        nargs="?",
        help="Contract or edited tool basename (e.g. selftest.py or new_packet.py)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Print every contract reconstruct list",
    )
    args = parser.parse_args()

    contracts = load_map()
    if args.name:
        contract = resolve_name(args.name, contracts)
        if contract is None:
            print(f"Unknown name {Path(args.name).name!r}")
            print("Known contracts:")
            for c in contracts:
                print(f"  {c}")
            print("This command writes nothing.")
            return 0
        print_one(contract, contracts)
        print("This command writes nothing.")
        return 0

    if args.all or not args.name:
        for c in contracts:
            print_one(c, contracts)
        print("This command writes nothing.")
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
