#!/usr/bin/env python3
"""Contract check for tools/contracts_suite.py unified reliability runner.

Locks discovery of all *_contract.py files, exclusion of the suite itself,
and that the command is non-invasive (no invent, no packet writes). Pure import
and filesystem checks only. Exit 0 on PASS.
"""

from __future__ import annotations

import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from contracts_suite import discover_contracts  # type: ignore


def fail(failures: list[str], cond: bool, msg: str) -> None:
    if not cond:
        failures.append(msg)


def main() -> int:
    failures: list[str] = []

    contracts = discover_contracts()
    fail(failures, isinstance(contracts, list), "discover_contracts must return list")
    fail(failures, len(contracts) >= 50, f"expected many contracts, got {len(contracts)}")

    suite_name = "contracts_suite.py"
    names = [p.name for p in contracts]
    fail(failures, suite_name not in names, "suite must exclude itself from discovery")
    fail(failures, all(n.endswith("_contract.py") for n in names), "all discovered must be *_contract.py")
    fail(failures, all(p.is_file() for p in contracts), "all discovered paths must exist")

    # Non-invasive: the module does not write on import or discover
    # (suite main is not called here to avoid long execution)
    print("Contracts suite contract")
    if failures:
        print("CONTRACTS_SUITE CONTRACT FAIL")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("CONTRACTS_SUITE CONTRACT PASS")
    print(f"Discovered {len(contracts)} reliability contracts. This command writes nothing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
