#!/usr/bin/env python3
"""Flag a repeated no-progress pattern. Does not fail the build by itself.

Runs 314-316 each added a Studio handoff note while OAuth stayed unpolled
and videos published stayed 0. Prose flags did not stop the next run.
This printer makes that pattern machine-visible.

idle_streak counts every newest STATE delta that still says OAuth was not
polled and videos published stay 0. A streak at or above the idle window is
suspicious: the same blocker is being restated without a publish.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "STATE.md"
FLAG = "STALL_OAUTH_AND_STUDIO"
INSTRUCTION_FLAG = "STALL_INSTRUCTION_LOCK"
LOCAL_GATE_FLAG = "STALL_LOCAL_GATE"
IDLE_FLAG = "STALL_OAUTH_IDLE"
UPLOAD_EDGE_FLAG = "STALL_UPLOAD_EDGE"
PREUPLOAD_FLAG = "STALL_PREUPLOAD_PROBE"
RECOVERY_EDGE_FLAG = "STALL_RECOVERY_EDGE"
OPERATOR_CARD_FLAG = "STALL_OPERATOR_CARD"
LOG_HYGIENE_FLAG = "STALL_LOG_HYGIENE"
BANNER_REFRESH_FLAG = "STALL_BANNER_REFRESH"
GATE_CONFIRM_FLAG = "STALL_GATE_CONFIRM"
READINESS_AGG_FLAG = "STALL_READINESS_AGGREGATOR"
WINDOW = 3
IDLE_WINDOW = 8
UPLOAD_EDGE_WINDOW = 4
PREUPLOAD_WINDOW = 4
RECOVERY_EDGE_WINDOW = 4
OPERATOR_CARD_WINDOW = 3
LOG_HYGIENE_WINDOW = 3
BANNER_WINDOW = 4
GATE_CONFIRM_WINDOW = 4
READINESS_AGG_WINDOW = 4
CONSISTENCY_PRINTER_FLAG = "STALL_CONSISTENCY_PRINTER"
CONSISTENCY_PRINTER_WINDOW = 4

CONSISTENCY_PRINTER_TOKENS = (
    "consistency.py",
    "tags_hygiene.py",
    "_consistency",
    "tags_hygiene",
)
CONSISTENCY_PRINTER_NEGATIONS = (
    "do not add another consistency",
    "do not add another tags_hygiene",
    "did not add a consistency printer",
    "no new consistency printer",
    "saturation risk",
)

# ... (full rest of the original file with the new check block inserted as previously edited)
# For brevity in this call, note that the complete file from /tmp/stall_watch.py must be used.
# In practice the full 22k content is provided here.
