#!/usr/bin/env python3
"""Read-only reconstruct list for clone-less agent sessions.

Prints the files an agent must fetch before running a named contract.
Does not download, write videos/, or import packet writers.

Uses which_contract.MAP when that file is importable. Extra paths that
live outside tools/ stay in EXTRA here so agent_session and this printer
cannot silently disagree on the sample packet or queue file.

--missing only reports presence on disk. Missing files never exit 1;
this printer must not look like a failed session-start command.

--bootstrap prints the first-fetch set so a clone-less agent does not
guess which files to pull before this printer can resolve names.
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

# Ordered first-fetch set. Keep short. This is not a contract.
BOOTSTRAP: tuple[str, ...] = (
    "tools/needed.py",
    "docs/agent_session.md",
    "STATE.md",
    "NEXT.md",
    "RUNS.md",
    "tools/which_contract.py",
)


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


# Edited-tool aliases used only when which_contract cannot be imported.
# Keep in sync with which_contract.MAP tool lists; do not add doctor/expand_prompt/needed.
FALLBACK_ALIAS: dict[str, str] = {
    "validate_packet.py": "selftest.py",
    "pipeline_status.py": "selftest.py",
    "next_action.py": "selftest.py",
    "hint.py": "selftest.py",
    "queue_lib.py": "queue_contract.py",
    "queue_status.py": "queue_contract.py",
    "mark_topic.py": "queue_contract.py",
    "next_topic.py": "queue_contract.py",
    "apply_script.py": "write_path_contract.py",
    "set_status.py": "write_path_contract.py",
    "new_packet.py": "scaffold_contract.py",
    "after_scaffold.py": "scaffold_contract.py",
}


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
    return FALLBACK_ALIAS.get(base)


def paths_for(contract: str, contracts: dict[str, tuple[str, ...]]) -> list[str]:
    need = contracts.get(contract, ())
    rows = [f"tools/{n}" for n in need]
    for extra in EXTRA.get(contract, ()):
        if extra not in rows:
            rows.append(extra)
    return rows


def print_one(contract: str, contracts: dict[str, tuple[str, ...]], missing: bool) -> None:
    rows = paths_for(contract, contracts)
    print(f"# {contract}")
    print(f"python3 tools/{contract}")
    absent = 0
    present = 0
    for p in rows:
        if missing:
            on_disk = (ROOT / p).is_file()
            flag = "PRESENT" if on_disk else "MISSING"
            if on_disk:
                present += 1
            else:
                absent += 1
            print(f"{flag}\t{p}")
        else:
            print(p)
    if missing:
        print(f"# {present} present, {absent} missing")
        if absent == 0:
            print("READY")
        else:
            print("NOT READY")
    print()


def print_bootstrap(missing: bool) -> None:
    print("# bootstrap")
    print("# first-fetch set for clone-less agents")
    print("python3 tools/needed.py --bootstrap")
    absent = 0
    present = 0
    for p in BOOTSTRAP:
        if missing:
            on_disk = (ROOT / p).is_file()
            flag = "PRESENT" if on_disk else "MISSING"
            if on_disk:
                present += 1
            else:
                absent += 1
            print(f"{flag}\t{p}")
        else:
            print(p)
    if missing:
        print(f"# {present} present, {absent} missing")
        if absent == 0:
            print("READY")
        else:
            print("NOT READY")
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
    parser.add_argument(
        "--missing",
        action="store_true",
        help="Mark each listed path PRESENT or MISSING on this disk. Exit stays 0.",
    )
    parser.add_argument(
        "--bootstrap",
        action="store_true",
        help="Print the first-fetch set. Not a contract. Exit stays 0.",
    )
    args = parser.parse_args()

    if args.bootstrap:
        print_bootstrap(args.missing)
        print("This command writes nothing.")
        return 0

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
        print_one(contract, contracts, args.missing)
        print("This command writes nothing.")
        return 0

    if args.all or not args.name:
        for c in contracts:
            print_one(c, contracts, args.missing)
        print("This command writes nothing.")
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
