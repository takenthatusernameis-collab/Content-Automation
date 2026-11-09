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
DATA_LAG_DAYS = 3
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


def load_feedback_state(packet: Path) -> dict | None:
    path = packet / STATE_NAME
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def collected_metrics(packet: Path, video_id: str | None) -> tuple[list | None, str]:
    """Return metrics only from a collected fetch for this video id.

    Dry-run files, mismatched ids, and missing attempted_fetch stay empty.
    Never invents a row.
    """
    if not video_id:
        return None, "no provider_video_id"
    state = load_feedback_state(packet)
    if not state:
        return None, "missing feedback_state.json"
    if state.get("gate") != "COLLECTED" or state.get("attempted_fetch") is not True:
        return None, "feedback_state is not a collected fetch"
    if str(state.get("provider_video_id") or "").strip() != video_id:
        return None, "feedback_state video id does not match upload_state"
    ok, detail = collected_window_ok(state, load_upload_state(packet))
    if not ok:
        return None, detail
    metrics = state.get("metrics")
    if not isinstance(metrics, list) or not metrics:
        return None, "collected fetch has no metric rows"
    if not all(isinstance(row, dict) and row for row in metrics):
        return None, "collected metric rows are not objects"
    return metrics, f"{len(metrics)} collected row(s) for {video_id}"



def collected_window_ok(state: dict, upload: dict | None) -> tuple[bool, str]:
    """A collected file counts only if it queried this video's first calendar days.

    A sliding now window, a missing kind, or dates that do not match uploaded_at
    are not the first-calendar-days observation (due at uploaded_at + 10 days = 7 calendar + 3 Analytics lag). Does not fetch.
    """
    window = state.get("window")
    if not isinstance(window, dict):
        return False, "collected fetch has no window"
    if window.get("kind") != "first_calendar_days":
        return False, "collected window is not the video's first calendar days"
    uploaded = upload_timestamp(upload)
    if uploaded is None:
        return False, "collected window cannot be checked without uploaded_at"
    if window.get("days") != DEFAULT_WINDOW_DAYS:
        return False, "collected window days are not the observation length"
    start_s, end_s = analytics_range(uploaded, DEFAULT_WINDOW_DAYS)
    got_start = str(window.get("start") or "")[:10]
    got_end = str(window.get("end") or "")[:10]
    if got_start != start_s or got_end != end_s:
        return False, "collected window dates do not match the video's first calendar days"
    return True, "first calendar days"


def provider_video_id(state: dict | None) -> str | None:
    if not state:
        return None
    vid = state.get("provider_video_id")
    if isinstance(vid, str) and vid.strip():
        return vid.strip()
    return None


def observation_window(now: datetime | None = None, days: int = DEFAULT_WINDOW_DAYS) -> dict:
    """Sliding now window. Not the Analytics query. Kept so callers can see the rejected shape."""
    end = now or _now()
    start = end - timedelta(days=days)
    return {
        "start": _fmt(start),
        "end": _fmt(end),
        "days": days,
        "kind": "sliding_now",
        "note": "not the query range; first comparison uses the video calendar days",
    }


def video_window(upload: dict | None, days: int = DEFAULT_WINDOW_DAYS) -> dict:
    """Query range shown to dry-run and request_plan. Same dates execute_feedback fetches."""
    uploaded = upload_timestamp(upload)
    if uploaded is None:
        return {
            "start": None,
            "end": None,
            "days": days,
            "kind": "unavailable",
            "note": "No uploaded_at. Not a query range. Do not collect.",
        }
    start_s, end_s = analytics_range(uploaded, days)
    return {
        "start": start_s + "T00:00:00Z",
        "end": end_s + "T23:59:59Z",
        "days": days,
        "kind": "first_calendar_days",
        "note": "First calendar days of this video only. Not a sliding now window.",
    }


def _parse_ts(raw) -> datetime | None:
    if not isinstance(raw, str) or not raw.strip():
        return None
    text = raw.strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def upload_timestamp(state: dict | None) -> datetime | None:
    """Return a provider upload time. Never invent one from generated or fetched fields."""
    if not state:
        return None
    candidates = []
    video = state.get("video_upload")
    if isinstance(video, dict):
        candidates.append(video.get("uploaded_at"))
    candidates.append(state.get("uploaded_at"))
    for raw in candidates:
        parsed = _parse_ts(raw)
        if parsed is not None:
            return parsed
    return None


def window_status(
    upload: dict | None,
    now: datetime | None = None,
    days: int = DEFAULT_WINDOW_DAYS,
    lag_days: int = DATA_LAG_DAYS,
) -> dict:
    """A collect is due only after the video window plus Analytics lag.

    The fetch end date is held back by lag_days. Due at upload+days would
    query a short window and still call it the first-calendar-days observation (due at uploaded_at + 10 days).
    """
    moment = now or _now()
    uploaded = upload_timestamp(upload)
    if uploaded is None:
        return {
            "due": False,
            "reason": "missing_uploaded_at",
            "uploaded_at": None,
            "due_at": None,
            "days": days,
            "lag_days": lag_days,
        }
    due_at = uploaded + timedelta(days=days + lag_days)
    due = moment >= due_at
    return {
        "due": due,
        "reason": "due" if due else "not_due",
        "uploaded_at": _fmt(uploaded),
        "due_at": _fmt(due_at),
        "days": days,
        "lag_days": lag_days,
    }


def analytics_range(uploaded: datetime, days: int = DEFAULT_WINDOW_DAYS) -> tuple[str, str]:
    """First `days` calendar dates of the video, inclusive. Not a sliding now window."""
    start = uploaded.date()
    end = (uploaded + timedelta(days=days - 1)).date()
    return start.isoformat(), end.isoformat()


def inspect_feedback(
    packet: Path,
    env: dict[str, str] | None = None,
    now: datetime | None = None,
) -> dict:
    upload = load_upload_state(packet)
    video_id = provider_video_id(upload)
    auth = auth_status(env)
    window = video_window(upload)
    checks = []

    def add(name: str, ok: bool, detail: str) -> None:
        checks.append({"name": name, "ok": ok, "detail": detail})

    due = window_status(upload, now)
    add("upload_state_present", upload is not None, UPLOAD_STATE if upload else "missing upload_state.json")
    add("provider_video_id_present", bool(video_id), video_id or "no provider_video_id")
    add("oauth_complete", auth["complete"], auth["state"] if auth["complete"] else ",".join(auth["missing"]))
    add("not_api_key_only", not auth["api_key_alone"], "API key is not analytics authorization")
    add(
        "observation_window_due",
        due["due"],
        due["reason"] if due["due"] else f"{due['reason']}; due_at={due['due_at'] or 'unknown'}",
    )
    add("no_invented_metrics", True, "metrics stay empty until a live report is fetched")

    if not video_id:
        gate = "HOLD_UNPUBLISHED"
        action = "DRY_RUN"
    elif not auth["complete"]:
        gate = AUTH_STATE
        action = "DRY_RUN"
    elif not due["due"]:
        gate = (
            "OBSERVATION_WINDOW_UNKNOWN"
            if due["reason"] == "missing_uploaded_at"
            else "OBSERVATION_WINDOW_NOT_DUE"
        )
        action = "HOLD_WINDOW"
    else:
        gate = "READY"
        action = "FETCH_BLOCKED_NO_NETWORK"

    return {
        "packet": packet.name,
        "drop": selected_vo_drop(packet),
        "provider_video_id": video_id,
        "auth": auth,
        "window": window,
        "window_status": due,
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
    due = report.get("window_status") or window_status(load_upload_state(packet), now)
    if not due.get("due"):
        reason = due.get("reason") or "not_due"
        gate = (
            "OBSERVATION_WINDOW_UNKNOWN"
            if reason == "missing_uploaded_at"
            else "OBSERVATION_WINDOW_NOT_DUE"
        )
        raise YouTubeAPIError(0, gate)
    token = refresh_access_token()
    uploaded = upload_timestamp(load_upload_state(packet))
    if uploaded is None:
        raise YouTubeAPIError(0, "OBSERVATION_WINDOW_UNKNOWN")
    start_s, end_s = analytics_range(uploaded, DEFAULT_WINDOW_DAYS)
    analytics = analytics_report(
        token,
        start_date=start_s,
        end_date=end_s,
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
            "start": start_s + "T00:00:00Z",
            "end": end_s + "T23:59:59Z",
            "days": DEFAULT_WINDOW_DAYS,
            "kind": "first_calendar_days",
            "data_lag_days": DATA_LAG_DAYS,
            "note": "First calendar days of this video only. Collect waits for that end date plus the Analytics lag. Not a sliding now window.",
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
            "startDate": (report["window"].get("start") or "")[:10] or None,
            "endDate": (report["window"].get("end") or "")[:10] or None,
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
        "observation window: {reason} due_at={due}".format(
            reason=(report.get("window_status") or {}).get("reason", "unknown"),
            due=(report.get("window_status") or {}).get("due_at") or "unknown",
        ),
        "a collect before the video window plus Analytics lag is not COLLECTED feedback",
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
    if report["gate"] in {"OBSERVATION_WINDOW_NOT_DUE", "OBSERVATION_WINDOW_UNKNOWN"}:
        return 5
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
