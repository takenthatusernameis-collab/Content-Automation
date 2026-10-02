#!/usr/bin/env python3
"""Fail closed before media materialize or a provider read when an authenticated dispatch lacks OAuth.

Prints secret names and presence booleans only. Never prints secret values.
Exit 0 when all three are non-empty. Exit 3 when any are missing.
"""

from __future__ import annotations

import os
import sys

OAUTH_KEYS = ("YOUTUBE_CLIENT_ID", "YOUTUBE_CLIENT_SECRET", "YOUTUBE_REFRESH_TOKEN")


def presence(env: dict[str, str] | None = None) -> dict[str, bool]:
    source = os.environ if env is None else env
    return {key: bool(str(source.get(key, "")).strip()) for key in OAUTH_KEYS}


def main() -> int:
    flags = presence()
    missing = [key for key, ok in flags.items() if not ok]
    for key, ok in flags.items():
        print(f"{key}={'present' if ok else 'missing'}")
    if missing:
        print(
            "REFUSE: authenticated dispatch needs GitHub Actions secrets "
            + ", ".join(missing)
            + ". Do not materialize media, upload, or collect feedback.",
            file=sys.stderr,
        )
        return 3
    print("OAuth secret names are present. Values were not printed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
