#!/usr/bin/env python3
"""Local preflight checks for the human OAuth step.

Verifies environment readiness (gh CLI, auth to the repo, python3, write outside repo)
before the human starts minting tokens. Does not poll secrets, invent values, or dispatch.
Prints clear next actions. Soft only; does not change gates.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = "takenthatusernameis-collab/Content-Automation"


def check_command(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def run_ok(args: list[str], timeout: int = 10) -> bool:
    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False


def main() -> int:
    print("HUMAN PREFLIGHT (for OAuth step; no secrets polled)")
    print()
    ok = True

    # Python
    if sys.version_info >= (3, 8):
        print("PASS: python3 >= 3.8")
    else:
        print("FAIL: python3 >= 3.8 required")
        ok = False

    # gh CLI
    if check_command("gh"):
        print("PASS: gh CLI found")
        if run_ok(["gh", "auth", "status"]):
            print("PASS: gh authenticated")
            # Check repo access without listing secrets
            if run_ok(["gh", "repo", "view", REPO, "--json", "name"]):
                print(f"PASS: can view {REPO}")
            else:
                print(f"WARN: cannot view {REPO} (check auth/permissions)")
        else:
            print("FAIL: gh not authenticated (run: gh auth login)")
            ok = False
    else:
        print("FAIL: gh CLI not found (install: https://cli.github.com/)")
        ok = False

    # Write outside repo
    try:
        with tempfile.NamedTemporaryFile(dir="/tmp", delete=True) as f:
            f.write(b"test")
        print("PASS: can write outside repo (/tmp)")
    except Exception:
        print("FAIL: cannot write outside repo")
        ok = False

    # Tools present
    tools = ["oauth_exchange.py", "human_one_pager.py", "human_secret_confirm.py"]
    for t in tools:
        if (ROOT / "tools" / t).is_file():
            print(f"PASS: tools/{t} present")
        else:
            print(f"FAIL: tools/{t} missing")
            ok = False

    print()
    if ok:
        print("PREFLIGHT PASS: environment ready for OAuth step.")
        print("Next: python3 tools/human_one_pager.py")
        print("Then follow the exact sequence in docs/human_oauth_checklist.md")
        print("HUMAN PREFLIGHT PASS")
        return 0
    else:
        print("PREFLIGHT FAIL: fix the items above before starting OAuth.")
        print("HUMAN PREFLIGHT FAIL")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
