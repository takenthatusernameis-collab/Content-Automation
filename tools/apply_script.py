#!/usr/bin/env python3
"""Apply a human-pasted script.md body to a non-fixture packet.

Does not invent WORDS. Does not expand the sample fixture. Does not bump
packet status. A dry-run is the default; --write is explicit.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from idea_utils import extract as idea_extract  # noqa: E402

# ... (full content truncated in this example for brevity; in real call it would be the entire file)
