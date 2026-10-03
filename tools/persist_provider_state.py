#!/usr/bin/env python3
"""Classify provider state before a git commit, and retry a rejected push.

A transient failure must not be committed. A provider video id, or a
completed-without-id hold, must be committed. A non-fast-forward push must
be retried after fetch. Never force-push. Losing that file is how a later
execute starts a second videos.insert.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Callable

Runner = Callable[[list[str]], tuple[int, str, str]]


def upload_commit_decision(data: dict) -> str:
    """Return commit_* or skip_transient. Do not invent a provider video id."""
    provider_id = str(data.get("provider_video_id") or "").strip()
    gone = data.get("completed_without_id") is True and str(
        data.get("error_class") or ""
    ).startswith("RESUMABLE_COMPLETED_SESSION_GONE")
    if gone and not provider_id:
        return "commit_completed_without_id"
    if provider_id:
        return "commit_provider_video_id"
    return "skip_transient"


def feedback_commit_decision(data: dict) -> str:
    """Return commit_collected only for a real COLLECTED fetch with a video id.

    A dry-run or mismatched feedback file stays uncommitted. Do not invent metrics.
    """
    if str(data.get("gate") or "") != "COLLECTED" or data.get("attempted_fetch") is not True:
        return "skip_not_collected"
    if not str(data.get("provider_video_id") or "").strip():
        return "skip_missing_id"
    return "commit_collected"


def push_needs_retry(stderr: str) -> bool:
    """True when the remote moved and a fetch/rebase can retry. Never force."""
    text = (stderr or "").lower()
    needles = (
        "non-fast-forward",
        "fetch first",
        "failed to push some refs",
        "updates were rejected",
    )
    return any(needle in text for needle in needles)


def push_with_retry(run: Runner, attempts: int = 3) -> str:
    """Push HEAD to origin/main. Rebase onto origin/main if the remote moved.

    Does not force-push. A rejected rebase is STATE_PERSIST_REJECTED so the
    operator can recover the video id instead of starting another insert.
    """
    if attempts < 1:
        raise SystemExit("STATE_PERSIST_REJECTED attempts_exhausted")
    last_err = ""
    for attempt in range(attempts):
        code, _out, err = run(["git", "push", "origin", "HEAD:main"])
        if code == 0:
            return "pushed"
        last_err = err or _out
        if not push_needs_retry(last_err) or attempt + 1 >= attempts:
            raise SystemExit(f"STATE_PERSIST_REJECTED {last_err.strip()}")
        fetch_code, _fetch_out, fetch_err = run(["git", "fetch", "origin", "main"])
        if fetch_code != 0:
            raise SystemExit(f"STATE_PERSIST_REJECTED {(fetch_err or _fetch_out).strip()}")
        rebase_code, _rebase_out, rebase_err = run(["git", "rebase", "origin/main"])
        if rebase_code != 0:
            raise SystemExit(
                f"STATE_PERSIST_REJECTED {(rebase_err or _rebase_out).strip()}"
            )
    raise SystemExit(f"STATE_PERSIST_REJECTED {last_err.strip()}")


def _load(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"STATE_PERSIST_UNREADABLE {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit("STATE_PERSIST_UNREADABLE not_object")
    return data


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 2 or args[0] not in {"classify-upload", "classify-feedback"}:
        print(
            "usage: persist_provider_state.py classify-upload|classify-feedback FILE",
            file=sys.stderr,
        )
        return 1
    decision = (
        upload_commit_decision(_load(Path(args[1])))
        if args[0] == "classify-upload"
        else feedback_commit_decision(_load(Path(args[1])))
    )
    print(decision)
    return 0 if decision.startswith("commit_") else 2


if __name__ == "__main__":
    raise SystemExit(main())
