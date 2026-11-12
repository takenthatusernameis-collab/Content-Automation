#!/usr/bin/env python3
"""Soft local format checker for the three OAuth values before gh secret set.

Helps the human catch common copy-paste mistakes (wrong Client ID suffix, empty or short
secret, missing/short refresh token) before the interactive secret-set step.
Never prints the values themselves. Never calls any API. Never writes files.
Exit 0 if all three look plausible; non-zero with a short message otherwise.
Usage (human terminal only, after export or after mint):
  export YOUTUBE_CLIENT_ID=...
  export YOUTUBE_CLIENT_SECRET=...
  export YOUTUBE_REFRESH_TOKEN=$(cat /tmp/youtube-refresh-token)   # or however you hold it
  python3 tools/oauth_credential_format_check.py
"""

from __future__ import annotations

import os
import sys


def check_client_id(value: str) -> str | None:
    if not value or not value.strip():
        return "YOUTUBE_CLIENT_ID is empty"
    if not value.strip().endswith(".apps.googleusercontent.com"):
        return "YOUTUBE_CLIENT_ID does not end with .apps.googleusercontent.com (common copy-paste miss)"
    if len(value.strip()) < 30:
        return "YOUTUBE_CLIENT_ID looks too short"
    return None


def check_client_secret(value: str) -> str | None:
    if not value or not value.strip():
        return "YOUTUBE_CLIENT_SECRET is empty"
    if len(value.strip()) < 10:
        return "YOUTUBE_CLIENT_SECRET looks too short"
    return None


def check_refresh_token(value: str) -> str | None:
    if not value or not value.strip():
        return "YOUTUBE_REFRESH_TOKEN is empty (mint first with oauth_exchange.py)"
    if len(value.strip()) < 20:
        return "YOUTUBE_REFRESH_TOKEN looks too short"
    return None


def main() -> int:
    print("OAUTH CREDENTIAL FORMAT CHECK (local only; values never printed)")
    print()
    cid = os.environ.get("YOUTUBE_CLIENT_ID", "")
    csec = os.environ.get("YOUTUBE_CLIENT_SECRET", "")
    rtok = os.environ.get("YOUTUBE_REFRESH_TOKEN", "")

    errors = []
    for name, checker, val in [
        ("CLIENT_ID", check_client_id, cid),
        ("CLIENT_SECRET", check_client_secret, csec),
        ("REFRESH_TOKEN", check_refresh_token, rtok),
    ]:
        err = checker(val)
        if err:
            errors.append(err)
            print(f"FAIL  {name}: {err}")
        else:
            print(f"PASS  {name}: format looks plausible")

    print()
    if errors:
        print("One or more values failed the soft format check.")
        print("Fix them, re-export, and re-run this tool before gh secret set.")
        print("Full guide: python3 tools/oauth_complete_guide.py")
        return 1
    print("All three values look plausible.")
    print("Next: gh secret set the three names (paste into the interactive prompts).")
    print("Then one dispatch with execute=true.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
