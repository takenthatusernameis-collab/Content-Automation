#!/usr/bin/env python3
"""Shared uploaded_at date parsing for post-upload tools.

Single source for robust ISO and fallback parsing so the +10 day observation
window stays consistent across observation_window, post_publish_sequence,
post_upload_confirm, and any future consumers.
Does not invent dates.
"""

from __future__ import annotations

from datetime import datetime, timezone


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
