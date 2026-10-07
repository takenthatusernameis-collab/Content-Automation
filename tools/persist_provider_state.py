#!/usr/bin/env python3
"""Classify provider state before a git commit, and retry a rejected push.

A transient failure must not be committed. A provider video id, or a
completed-without-id hold, must be committed. A non-fast-forward push must
be retried after fetch. Never force-push. Losing that file is how a later
execute starts a second videos.insert.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Callable

RECOVERY_ARTIFACT = "provider-upload-state"
RECOVERY_REPO = "takenthatusernameis-collab/Content-Automation"


def artifact_recovery_command(
    repo: str = RECOVERY_REPO,
    artifact: str = RECOVERY_ARTIFACT,
    workflow: str = "youtube-production.yml",
) -> str:
    """How to fetch the video id if git push was rejected.

    Do not call GitHub from this function. A bare `gh run download --name`
    uses the newest run. Agent commits trigger selftest.yml, which has no
    provider-upload-state. Pinning only the newest production run is also
    wrong: a later execute=false dispatch has no artifact. Walk recent
    production runs and download the first that has the artifact. An empty
    run id must not fall through to a bare download.
    """
    return (
        "set -euo pipefail; dir=/tmp/provider-upload-state; rm -rf \"$dir\"; mkdir -p \"$dir\"; found=; "
        f"for id in $(gh run list --repo {repo} --workflow {workflow} --limit 20 "
        "--json databaseId --jq '.[].databaseId'); do "
        "test -n \"$id\" && test \"$id\" != null || continue; "
        f"if gh run download --repo {repo} \"$id\" --name {artifact} -D \"$dir\"; then "
        "found=$id; break; fi; done; "
        "test -n \"$found\" || { echo NO_PROVIDER_UPLOAD_STATE; "
        "echo 'do not run a bare gh run download --name provider-upload-state'; exit 1; }; "
        "echo RECOVERED_RUN \"$found\"; find \"$dir\" -name upload_state.json -print"
    )


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
    if data.get("session_expired_hold") is True:
        return "commit_session_expired_hold"
    if (
        data.get("session_expired_released") is True
        and data.get("session_expired_hold") is not True
        and not provider_id
        and not str(data.get("resumable_session_uri") or "").strip().startswith("https://")
    ):
        return "commit_session_hold_released"
    session = str(data.get("resumable_session_uri") or "").strip()
    if session.startswith("https://"):
        return "commit_resumable_session"
    return "skip_transient"


def early_persist_plan(data: dict, state_path: str) -> list[list[str]] | None:
    """Git commands that commit an open session before chunk upload finishes.

    Returns None for a transient state. Command text must not contain the
    session URI. Does not push and does not call YouTube.
    """
    decision = upload_commit_decision(data)
    if not decision.startswith("commit_"):
        return None
    if "https://" in state_path or "://" in state_path:
        raise SystemExit("STATE_PERSIST_REJECTED path")
    return [
        ["git", "add", "--", state_path],
        ["git", "commit", "-m", f"Persist YouTube upload state ({decision})"],
    ]


def early_persist_file(path: Path, run: Runner) -> str:
    """Commit and push provider state if it is durable. Never prints the URI.

    A failed git command returns early_persist_failed and must not become a
    second videos.insert. The later workflow persist step still runs.
    """
    data = _load(path)
    plan = early_persist_plan(data, path.as_posix())
    if plan is None:
        return "skip_transient"
    for cmd in plan:
        code, out, err = run(cmd)
        if code != 0:
            # An unchanged index is not a failure. Other git errors stop here.
            blob = f"{out}\n{err}"
            if cmd[1] == "commit" and (
                "nothing to commit" in blob or "no changes added to commit" in blob
            ):
                return "unchanged"
            return "early_persist_failed"
    try:
        push_with_retry(run)
    except SystemExit:
        return "early_persist_failed"
    return "pushed"


def feedback_window_stamp_ok(data: dict) -> bool:
    """True only for the execute stamp: first calendar days, length 7, dated.

    A missing kind or sliding_now is not the observation. Does not fetch and
    does not invent dates. Date match against uploaded_at stays in collected_metrics.
    """
    window = data.get("window")
    if not isinstance(window, dict):
        return False
    if window.get("kind") != "first_calendar_days":
        return False
    if window.get("days") != 7:
        return False
    start = str(window.get("start") or "")[:10]
    end = str(window.get("end") or "")[:10]
    if len(start) != 10 or len(end) != 10 or start[4] != "-" or end[4] != "-":
        return False
    if start > end:
        return False
    return True


def feedback_commit_decision(data: dict) -> str:
    """Return commit_collected only for a stamped COLLECTED fetch with a video id.

    A dry-run, a missing video id, or a collected file with no first-calendar-days
    stamp stays uncommitted. Do not invent metrics or a window.
    """
    if str(data.get("gate") or "") != "COLLECTED" or data.get("attempted_fetch") is not True:
        return "skip_not_collected"
    if not str(data.get("provider_video_id") or "").strip():
        return "skip_missing_id"
    if not feedback_window_stamp_ok(data):
        return "skip_unstamped_window"
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


def _is_shallow(run: Runner) -> bool:
    """Actions checkout is shallow by default. A shallow rebase drops the video id."""
    code, out, err = run(["git", "rev-parse", "--is-shallow-repository"])
    if code != 0:
        raise SystemExit(f"STATE_PERSIST_REJECTED {(err or out).strip()}")
    return (out or "").strip() == "true"


def _unshallow(run: Runner) -> None:
    """Fetch full history so rebase has a merge base. Never force-push."""
    code, out, err = run(["git", "fetch", "--unshallow", "origin"])
    if code == 0:
        return
    text = (err or out or "").lower()
    if "does not make sense" in text:
        return
    raise SystemExit(f"STATE_PERSIST_REJECTED {(err or out).strip()}")


def push_with_retry(run: Runner, attempts: int = 3) -> str:
    """Push HEAD to origin/main. Rebase onto origin/main if the remote moved.

    A shallow checkout is unshallowed before that rebase. Does not force-push.
    A rejected rebase is STATE_PERSIST_REJECTED so the operator can recover
    the video id instead of starting another insert.
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
        if _is_shallow(run):
            _unshallow(run)
        fetch_code, _fetch_out, fetch_err = run(["git", "fetch", "origin", "main"])
        if fetch_code != 0:
            raise SystemExit(f"STATE_PERSIST_REJECTED {(fetch_err or _fetch_out).strip()}")
        rebase_code, _rebase_out, rebase_err = run(["git", "rebase", "origin/main"])
        if rebase_code != 0:
            run(["git", "rebase", "--abort"])
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


def _git_run(cmd: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) == 1 and args[0] == "recover":
        # Printed after a rejected push. Does not download and does not call YouTube.
        print(artifact_recovery_command())
        print("Do not dispatch execute again. Copy upload_state.json onto main before another insert.")
        print("Do not run a bare gh run download --name provider-upload-state. That picks the newest run, often selftest, which has no video id. Do not use only the newest production run: a later execute=false dispatch has no artifact.")
        return 0
    if len(args) == 1 and args[0] == "push":
        # Workflow calls this. Do not inline push_with_retry in a YAML heredoc:
        # a spaced PY terminator never closes, so the video id is not pushed.
        print(push_with_retry(_git_run))
        return 0
    if len(args) != 2 or args[0] not in {"classify-upload", "classify-feedback"}:
        print(
            "usage: persist_provider_state.py classify-upload|classify-feedback FILE | push | recover",
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
