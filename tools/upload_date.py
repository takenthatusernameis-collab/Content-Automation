#!/usr/bin/env python3
"""Shared uploaded_at date parsing and observation window for post-upload tools.

Single source for robust ISO and fallback parsing and the exact +10 day due date
so the observation window stays consistent across observation_window,
post_publish_sequence, post_upload_confirm, and any future consumers.
Does not invent dates.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

OBSERVATION_WINDOW_DAYS = 10
"""Days after uploaded_at before collect_feedback is due (7 calendar + 3 Analytics lag)."""


def parse_uploaded_at(data: dict) -> datetime | None:
    """Return timezone-aware UTC datetime from common uploaded_at fields, or None."""
    raw = data.get("uploaded_at") or data.get("uploadedAt") or data.get("upload_time")
    if not raw or not isinstance(raw, str):
        return None
    raw = raw.strip()
    # Prefer modern fromisoformat (handles most ISO-8601 including Z after cleanup)
    try:
        cleaned = raw.replace("Z", "+00:00") if raw.endswith("Z") else raw
        dt = datetime.fromisoformat(cleaned)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except ValueError:
        pass
    # Fallbacks for older or slightly variant strings
    for fmt in (
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
    ):
        try:
            dt = datetime.strptime(raw, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue
    return None


def compute_due_date(uploaded: datetime) -> datetime:
    """Return the observation window due date: uploaded_at + OBSERVATION_WINDOW_DAYS."""
    if uploaded.tzinfo is None:
        uploaded = uploaded.replace(tzinfo=timezone.utc)
    return uploaded + timedelta(days=OBSERVATION_WINDOW_DAYS)
