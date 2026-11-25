#!/usr/bin/env python3
"""Check key tracking files for stub/placeholder/empty risk.

Addresses the recurring documentation-without-content failure pattern flagged in FAILURES.md.
Verifies STATE.md, NEXT.md, RUNS.md, PROGRESS.md, FAILURES.md, HANDOFF.md, docs/labor_reduction_map.md
are non-empty, contain expected signals, and lack obvious placeholders.
Does not invent data, rewrite files, or poll external services. Soft informational; exit 1 only on clear failures.
Useful after any remote file update. Compounds reliability of durable run memory.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TRACKING = [
    ("STATE.md", 200, ["STALL_OAUTH_IDLE", "published", "Run"]),
    ("NEXT.md", 100, ["human", "oauth", "secret"]),
    ("RUNS.md", 200, ["## Run", "STALL_OAUTH_IDLE"]),
    ("PROGRESS.md", 100, ["published", "human"]),
    ("FAILURES.md", 100, ["placeholder", "STALL_OAUTH_IDLE"]),
    ("HANDOFF.md", 100, ["STALL_OAUTH_IDLE", "human"]),
    ("docs/labor_reduction_map.md", 300, ["human min", "OAuth"]),
]

PLACEHOLDERS = ["PLACEHOLDER", "CONTENT_FROM_FILE", "UPDATED_PROGRESS", "TO_BE_REPLACED", "short placeholder"]

def check_tracking(name: str, min_size: int, keywords: list[str]) -> tuple[bool, str]:
    path = ROOT / name
    if not path.is_file():
        return False, f"MISSING {name}"
    text = path.read_text(encoding="utf-8")
    size = len(text.encode("utf-8"))
    if size < min_size:
        return False, f"SHORT {name}: {size} bytes < {min_size} (possible stub)"
    low = text.lower()
    if any(p.lower() in low for p in PLACEHOLDERS) and size < 500:
        return False, f"PLACEHOLDER-LIKE {name}"
    missing_kw = [k for k in keywords if k.lower() not in low]
    if missing_kw and size < 2000:
        return False, f"MISSING_KEYWORDS {name}: {missing_kw}"
    return True, f"OK {name}: {size} bytes"

def main() -> int:
    fails = []
    print("TRACKING INTEGRITY CHECK (stub/placeholder risk on durable memory files; do not invent)")
    for name, min_size, kws in TRACKING:
        ok, msg = check_tracking(name, min_size, kws)
        print(msg)
        if not ok:
            fails.append(name)
    if fails:
        print(f"FAIL: {len(fails)} tracking files need attention ({', '.join(fails)})")
        print("Restore from archive or re-write verified content. See FAILURES.md pattern.")
        return 1
    print("PASS: all checked tracking files look intact")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
