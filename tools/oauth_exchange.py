#!/usr/bin/env python3
"""Build a YouTube consent URL and exchange one auth code for a refresh token.

Does not poll GitHub secrets. Does not print client secret or refresh token.
A refresh token is written only to an absolute path outside this repository.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
REDIRECT_URI = "http://localhost"
UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
FORCE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
ANALYTICS_SCOPE = "https://www.googleapis.com/auth/yt-analytics.readonly"
SCOPES = (UPLOAD_SCOPE, FORCE_SSL_SCOPE, ANALYTICS_SCOPE)


def consent_url(client_id: str) -> str:
    client_id = client_id.strip()
    if not client_id:
        raise ValueError("CLIENT_ID_MISSING")
    query = urllib.parse.urlencode(
        {
            "client_id": client_id,
            "redirect_uri": REDIRECT_URI,
            "response_type": "code",
            "scope": " ".join(SCOPES),
            "access_type": "offline",
            "prompt": "consent",
        }
    )
    return AUTH_URL + "?" + query


def outside_repo(path: Path) -> bool:
    resolved = path.resolve()
    try:
        resolved.relative_to(ROOT.resolve())
    except ValueError:
        return True
    return False


def exchange(client_id: str, client_secret: str, code: str) -> str:
    body = urllib.parse.urlencode(
        {
            "code": code.strip(),
            "client_id": client_id.strip(),
            "client_secret": client_secret.strip(),
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code",
        }
    ).encode()
    request = urllib.request.Request(
        TOKEN_URL,
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode())
    token = str(payload.get("refresh_token", "")).strip()
    if not token:
        raise ValueError("REFRESH_TOKEN_MISSING")
    return token


def write_token(path: Path, token: str) -> None:
    if not path.is_absolute() or not outside_repo(path):
        raise ValueError("OUT_PATH_REFUSED")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(token + "\n", encoding="utf-8")
    path.chmod(0o600)


def main() -> int:
    parser = argparse.ArgumentParser(description="Local YouTube refresh-token exchange")
    parser.add_argument("--exchange", action="store_true", help="Exchange a code from stdin")
    parser.add_argument("--out", default="", help="Absolute path outside the repo for the refresh token")
    args = parser.parse_args()
    client_id = os.environ.get("YOUTUBE_CLIENT_ID", "")
    client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET", "")
    if args.exchange:
        if not client_id.strip() or not client_secret.strip():
            print("REFUSE: set YOUTUBE_CLIENT_ID and YOUTUBE_CLIENT_SECRET in the environment. Values are not printed.", file=sys.stderr)
            return 3
        code = sys.stdin.read()
        if not code.strip():
            print("REFUSE: pass the auth code on stdin, not as an argument.", file=sys.stderr)
            return 3
        try:
            token = exchange(client_id, client_secret, code)
            write_token(Path(args.out), token)
        except ValueError as exc:
            print(f"REFUSE: {exc}", file=sys.stderr)
            return 3
        except Exception as exc:  # noqa: BLE001 — provider error must not print the body
            print(f"REFUSE: TOKEN_EXCHANGE_FAILED {type(exc).__name__}", file=sys.stderr)
            return 4
        print(f"REFRESH_TOKEN_WRITTEN bytes={len(token)} outside_repo=yes")
        return 0
    if not client_id.strip():
        print("REFUSE: set YOUTUBE_CLIENT_ID to print a consent URL. The value is not printed by itself.", file=sys.stderr)
        return 3
    url = consent_url(client_id)
    if client_secret and client_secret in url:
        print("REFUSE: consent URL must not contain the client secret", file=sys.stderr)
        return 3
    sys.stdout.write(url + "\n")
    print("SCOPES " + ",".join(SCOPES))
    print("Redirect URI is http://localhost. Register that URI on the Desktop client. Do not commit the code.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
