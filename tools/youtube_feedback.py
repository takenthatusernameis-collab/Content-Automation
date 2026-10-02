#!/usr/bin/env python3
"""YouTube Analytics + comment feedback adapter.

Dry-run is the default. --execute performs authenticated read-only provider fetches.
Never invents metrics. Never treats a missing video ID as collected feedback.
"""


from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from render_brief import selected_vo_drop  # noqa: E402
from youtube_api import YouTubeAPIError, analytics_report, compact_api_error, list_comment_threads, refresh_access_token  # noqa: E402

AUTH_STATE = "YOUTUBE_AUTH_REQUIRED"
OAUTH_KEYS = ("YOUTUBE_CLIENT_ID", "YOUTUBE_CLIENT_SECRET", "YOUTUBE_REFRESH_TOKEN")
ANALYTICS_SCOPE = "https://www.googleapis.com/auth/yt-analytics.readonly"
DATA_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"
DEFAULT_WINDOW_DAYS = 7
UPLOAD_STATE = "upload_state.json"
STATE_NAME = "feedback_state.json"
METRIC_NAMES = (
    "views",
    "likes",
    "dislikes",
    "estimatedMinutesWatched",
    "averageViewDuration",
    "averageViewPercentage",
    "subscribersGained",
)
COMMENT_CLASSES = (
    "question",
    "objection",
    "praise",
    "confusion",
    "request",
    "spam/noise",
)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _fmt(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def auth_status(env: dict[str, str] | None = None) -> dict:
    source = env if env is not None else os.environ
    present = {key: bool(str(source.get(key, "")).strip()) for key in OAUTH_KEYS}
    missing = [k for k, ok in present.items() if not ok]
    return {
        "complete": not missing,
        "missing": missing,
        "api_key_alone": bool(str(source.get("YOUTUBE_API_KEY", "")).strip()) and bool(missing),
        "channel_id_set": bool(str(source.get("YOUTUBE_CHANNEL_ID", "")).strip()),
        "scopes": [ANALYTICS_SCOPE, DATA_SCOPE],
        "state": AUTH_STATE if missing else "YOUTUBE_AUTH_PRESENT",
    }


def load_upload_state(packet: Path) -> dict | None:
    path = packet / UPLOAD_STATE
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def provider_video_id(state: dict | None) -> str | None:
    if not state:
        return None
    vid = state.get("provider_video_id")
    if isinstance(vid, str) and vid.strip():
        return vid.strip()
    return None


def observation_window(now: datetime | None = None, days: int = DEFAULT_WINDOW_DAYS) -> dict:
    end = now or _now()
    start = end - timedelta(days=days)
    return {
        "start": _fmt(start),
        "end": _fmt(end),
        "days": days,
        "note": "comparable window only; do not mix videos of different ages",
    }


def inspect_feedback(
    packet: Path,
    env: dict[str, str] | None = None,
    now: datetime | None = None,
) -> dict:
    upload = load_upload_state(packet)
    video_id = provider_video_id(upload)
    auth = auth_status(env)
    window = observation_window(now)
    checks = []

    def add(name: str, ok: bool, detail: str) -> None:
        checks.append({"name": name, "ok": ok, "detail": detail})

    add("upload_state_present", upload is not None, UPLOAD_STATE if upload else "missing upload_state.json")
    add("provider_video_id_present", bool(video_id), video_id or "no provider_video_id")
    add("oauth_complete", auth["complete"], auth["state"] if auth["complete"] else ",".join(auth["missing"]))
    add("not_api_key_only", not auth["api_key_alone"], "API key is not analytics authorization")
    add("no_invented_metrics", True, "metrics stay empty until a live report is fetched")

    if not video_id:
        gate = "HOLD_UNPUBLISHED"
        action = "DRY_RUN"
    elif not auth["complete"]:
        gate = AUTH_STATE
        action = "DRY_RUN"
    else:
        gate = "READY"
        action = "FETCH_BLOCKED_NO_NETWORK"

    return {
        "packet": packet.name,
        "drop": selected_vo_drop(packet),
        "provider_video_id": video_id,
        "auth": auth,
        "window": window,
        "metrics_requested": list(METRIC_NAMES),
        "comment_classes": list(COMMENT_CLASSES),
        "metrics": None,
        "comments": [],
        "checks": checks,
        "gate": gate,
        "action": action,
        "generated": _fmt(now or _now()),
    }


def _analytics_rows(data: dict) -> list[dict]:
    headers = [str(h.get("name")) for h in (data.get("columnHeaders") or [])]
    rows = []
    for row in data.get("rows") or []:
        rows.append({name: value for name, value in zip(headers, row)})
    return rows


def execute_feedback(packet: Path, report: dict, *, now: datetime | None = None) -> dict:
    video_id = report.get("provider_video_id")
    if not video_id:
        raise YouTubeAPIError(0, "HOLD_UNPUBLISHED")
    token = refresh_access_token()
    end = now or _now()
    end = end - timedelta(days=3)
    start = end - timedelta(days=report["window"]["days"] - 1)
    analytics = analytics_report(
        token,
        start_date=start.strftime("%Y-%m-%d"),
        end_date=end.strftime("%Y-%m-%d"),
        metrics=list(report["metrics_requested"]),
        video_id=video_id,
    )
    rows = _analytics_rows(analytics)
    threads = list_comment_threads(token, video_id=video_id)
    comments = []
    for thread in threads:
        top = ((thread.get("snippet") or {}).get("topLevelComment") or {}).get("snippet") or {}
        comments.append(
            {
                "thread_id": thread.get("id"),
                "text": top.get("textOriginal"),
                "published_at": top.get("publishedAt"),
                "like_count": top.get("likeCount", 0),
                "reply_count": (thread.get("snippet") or {}).get("totalReplyCount", 0),
            }
        )
    state = {
        "packet": packet.name,
        "generated": _fmt(now or _now()),
        "gate": "COLLECTED",
        "action": "FETCHED",
        "provider_video_id": video_id,
        "window": {
            "start": start.strftime("%Y-%m-%dT00:00:00Z"),
            "end": end.strftime("%Y-%m-%dT23:59:59Z"),
            "days": report["window"]["days"],
            "data_lag_days": 3,
            "note": "Analytics end date is held three days back to avoid the documented processing-latency edge.",
        },
        "metrics": rows,
        "comment_count": len(comments),
        "comments": comments,
        "attempted_fetch": True,
        "error_class": None,
    }
    dest = packet / STATE_NAME
    tmp = dest.with_suffix(dest.suffix + ".tmp")
    tmp.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(dest)
    return state


def request_plan(report: dict) -> dict:
    return {
        "analytics": {
            "ids": "channel==MINE",
            "startDate": report["window"]["start"][:10],
            "endDate": report["window"]["end"][:10],
            "metrics": ",".join(report["metrics_requested"]),
            "filters": f"video=={report['provider_video_id']}" if report["provider_video_id"] else None,
            "scope": ANALYTICS_SCOPE,
        },
        "comments": {
            "part": "snippet,replies",
            "videoId": report["provider_video_id"],
            "scope": DATA_SCOPE,
            "note": "replies may require comments.list",
        },
        "local": {
            "packet": report["packet"],
            "window_days": report["window"]["days"],
        },
    }


def redacted_state(report: dict) -> dict:
    return {
        "packet": report["packet"],
        "generated": report["generated"],
        "gate": report["gate"],
        "action": report["action"],
        "provider_video_id": report["provider_video_id"],
        "window": report["window"],
        "auth_state": report["auth"]["state"],
        "missing_env": report["auth"]["missing"],
        "metrics": None,
        "comment_count": 0,
        "attempted_fetch": False,
        "error_class": report["gate"] if report["gate"] != "READY" else None,
        "note": "dry-run only; this adapter never calls Analytics or commentThreads.list",
    }


def render_text(report: dict) -> str:
    lines = [
        f"packet: {report['packet']}",
        f"gate: {report['gate']}",
        f"action: {report['action']}",
        f"drop: {report['drop']}",
        f"provider_video_id: {report['provider_video_id'] or 'none'}",
        f"window: {report['window']['start']} .. {report['window']['end']} ({report['window']['days']}d)",
        f"auth: {report['auth']['state']}",
        "dry-run default; --execute performs authenticated read-only Analytics and comment API calls",
        "missing provider_video_id is HOLD_UNPUBLISHED, not collected feedback",
    ]
    for c in report["checks"]:
        mark = "PASS" if c["ok"] else "FAIL"
        lines.append(f"- {mark} {c['name']}: {c['detail']}")
    lines.append("dry_run_plan:")
    lines.append(json.dumps(request_plan(report), indent=2, ensure_ascii=False))
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Dry-run YouTube feedback adapter. No API. No secrets printed."
    )
    parser.add_argument("packet", help="Path to packet folder")
    parser.add_argument(
        "--write-state",
        action="store_true",
        help="Write redacted dry-run feedback_state.json (never contains secrets)",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Fetch Analytics and comments with the configured OAuth credentials.",
    )
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1
    report = inspect_feedback(path)
    sys.stdout.write(render_text(report))
    if report["gate"] == "HOLD_UNPUBLISHED":
        if args.write_state:
            dest = path / STATE_NAME
            dest.write_text(json.dumps(redacted_state(report), indent=2) + "\n", encoding="utf-8")
            print(dest)
        return 2
    if report["gate"] == AUTH_STATE and not args.execute:
        if args.write_state:
            dest = path / STATE_NAME
            dest.write_text(json.dumps(redacted_state(report), indent=2) + "\n", encoding="utf-8")
            print(dest)
        return 3
    if args.execute:
        try:
            state = execute_feedback(path, report)
            print(json.dumps(state, indent=2, ensure_ascii=False))
            return 0
        except YouTubeAPIError as exc:
            print(json.dumps({"error": compact_api_error(exc)}, ensure_ascii=False), file=sys.stderr)
            return 3 if exc.reason == "YOUTUBE_AUTH_REQUIRED" else 4
        except Exception as exc:
            print(json.dumps({"error": compact_api_error(exc)}, ensure_ascii=False), file=sys.stderr)
            return 4
    if args.write_state:
        dest = path / STATE_NAME
        dest.write_text(json.dumps(redacted_state(report), indent=2) + "\n", encoding="utf-8")
        print(dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
