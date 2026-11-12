#!/usr/bin/env python3
"""Soft local format checker for the three OAuth values before gh secret set.

Helps the human catch common copy-paste mistakes (wrong Client ID suffix, empty or short
secret, missing/short refresh token, leading/trailing whitespace) before the interactive secret-set step.
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


def check_client_id(value: str) -> tuple[str | None, bool]:
    stripped = value.strip()
    had_ws = value != stripped
    if not stripped:
        return "YOUTUBE_CLIENT_ID is empty", had_ws
    if not stripped.endswith(".apps.googleusercontent.com"):
        return "YOUTUBE_CLIENT_ID does not end with .apps.googleusercontent.com (common copy-paste miss)", had_ws
    if len(stripped) < 30:
        return "YOUTUBE_CLIENT_ID looks too short", had_ws
    return None, had_ws


def check_client_secret(value: str) -> tuple[str | None, bool]:
    stripped = value.strip()
    had_ws = value != stripped
    if not stripped:
        return "YOUTUBE_CLIENT_SECRET is empty", had_ws
    if len(stripped) < 10:
        return "YOUTUBE_CLIENT_SECRET looks too short", had_ws
    return None, had_ws


def check_refresh_token(value: str) -> tuple[str | None, bool]:
    stripped = value.strip()
    had_ws = value != stripped
    if not stripped:
        return "YOUTUBE_REFRESH_TOKEN is empty (mint first with oauth_exchange.py)", had_ws
    if len(stripped) < 20:
        return "YOUTUBE_REFRESH_TOKEN looks too short", had_ws
    return None, had_ws


def main() -> int:
    print("OAUTH CREDENTIAL FORMAT CHECK (local only; values never printed)")
    print()
    cid = os.environ.get("YOUTUBE_CLIENT_ID", "")
    csec = os.environ.get("YOUTUBE_CLIENT_SECRET", "")
    rtok = os.environ.get("YOUTUBE_REFRESH_TOKEN", "")

    errors = []
    ws_warnings = []
    for name, checker, val in [
        ("CLIENT_ID", check_client_id, cid),
        ("CLIENT_SECRET", check_client_secret, csec),
        ("REFRESH_TOKEN", check_refresh_token, rtok),
    ]:
        err, had_ws = checker(val)
        if had_ws:
            ws_warnings.append(name)
        if err:
            errors.append(err)
            print(f"FAIL  {name}: {err}")
        else:
            print(f"PASS  {name}: format looks plausible")

    if ws_warnings:
        print()
        print("NOTE: Leading/trailing whitespace was detected and ignored for the check on:")
        for n in ws_warnings:
            print(f"  - {n}")
        print("Re-export the clean values (without extra spaces) before gh secret set to avoid silent failures.")

    print()
    if errors:
        print("One or more values failed the soft format check.")
        print("Fix them, re-export, and re-run this tool before gh secret set.")
        print("Full guide: python3 tools/oauth_complete_guide.py")
        return 1
    print("All three values look plausible.")
    if ws_warnings:
        print("Whitespace note above: clean the exports if you have not already.")
    print("Next: gh secret set the three names (paste into the interactive prompts).")
    print("Then one dispatch with execute=true.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
