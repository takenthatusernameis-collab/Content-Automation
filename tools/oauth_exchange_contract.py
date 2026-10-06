#!/usr/bin/env python3
"""Lock the local YouTube token exchange so it cannot write a secret into the repo."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import oauth_exchange  # noqa: E402


def fail(msg: str) -> int:
    print(f"FAIL: {msg}", file=sys.stderr)
    return 1


def main() -> int:
    source = Path(oauth_exchange.__file__).read_text(encoding="utf-8")
    if "print(token" in source or "print(client_secret" in source:
        return fail("exchange must not print the token or client secret")
    import urllib.parse
    url = oauth_exchange.consent_url("test-client")
    query = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
    scopes = set(query.get("scope", [""])[0].split())
    for scope in oauth_exchange.SCOPES:
        if scope not in scopes:
            return fail(f"consent URL missing {scope}")
    if query.get("access_type") != ["offline"] or query.get("prompt") != ["consent"]:
        return fail("consent URL must request an offline refresh token")
    if "test-secret" in url:
        return fail("consent URL included a secret")
    if oauth_exchange.outside_repo(ROOT / "secrets.txt"):
        return fail("repo path must be refused")
    if not oauth_exchange.outside_repo(Path("/tmp/youtube-refresh-token")):
        return fail("tmp path must be allowed")
    try:
        oauth_exchange.write_token(ROOT / "refresh.txt", "nope")
    except ValueError as exc:
        if str(exc) != "OUT_PATH_REFUSED":
            return fail(f"unexpected refuse {exc}")
    else:
        return fail("write_token accepted a repo path")
    print("OAUTH EXCHANGE CONTRACT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
