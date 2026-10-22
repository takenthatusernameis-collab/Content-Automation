#!/usr/bin/env python3
"""Suggest a concrete, under-2-minute CTA that installs the packet mechanism.

Reads idea.md for mechanism and problem. Proposes spoken WORDS and a short
end-screen line that follows the channel promise (install one small default)
and avoids generic engagement bait. Does not write any files. A suggestion
is a starting point for the CTA section of draft.md, not a final script.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MECH_RE = re.compile(r"mechanism[^\n]*:\s*(.+)", re.I)

PROBLEM_RE = re.compile(r"problem:\s*(.+)", re.I)

def extract(idea_text: str) -> tuple[str, str]:
    mech = ""
    problem = ""
    for line in idea_text.splitlines():
        m = MECH_RE.search(line)
        if m:
            mech = m.group(1).strip().rstrip(".")
        p = PROBLEM_RE.search(line)
        if p:
            problem = p.group(1).strip().rstrip(".")
    return mech, problem

def _shorten(text: str, max_len: int = 40) -> str:
    """Return a natural short phrase, preferring whole words or first clause."""
    text = text.strip()
    if len(text) <= max_len:
        return text
    for sep in (". ", ", ", " so ", " that ", " and ", " — ", " - "):
        if sep in text:
            cand = text.split(sep)[0].strip()
            if 10 <= len(cand) <= max_len:
                return cand
    words = text.split()
    out = []
    for w in words:
        trial = " ".join(out + [w])
        if len(trial) > max_len:
            break
        out.append(w)
    return " ".join(out) if out else text[:max_len].rstrip()

def suggest(mech: str, problem: str) -> tuple[str, str]:
    """Return (spoken_cta, end_screen_line)."""
    if not mech:
        mech = "the written next-action default"
    # Concrete install action that can finish in under two minutes
    action = (
        f"Write the exact words of the {_shorten(mech.lower(), 40)} on a sticky note or in a note on the device you use to open the list. "
        f"Put that note where the stall starts. Do that before you open the next tab."
    )
    spoken = (
        f"{action} "
        f"That is the whole assignment. It takes less than two minutes and it installs the default the video named."
    )
    end = f"Install the default: {_shorten(mech, 60)}"
    return spoken, end

def main() -> int:
    parser = argparse.ArgumentParser(description="Suggest a mechanism-aligned CTA.")
    parser.add_argument("packet", help="Packet folder containing idea.md")
    args = parser.parse_args()
    path = Path(args.packet)
    idea = path / "idea.md"
    if not idea.is_file():
        print(f"No idea.md in {path}")
        return 1
    text = idea.read_text(encoding="utf-8")
    mech, problem = extract(text)
    spoken, end = suggest(mech, problem)
    print("CTA SUGGESTION (mechanism-aligned; under 2 min; no engagement bait)")
    print(f"mechanism: {mech}")
    if problem:
        print(f"problem: {problem}")
    print()
    print("Suggested spoken CTA WORDS:")
    print(spoken)
    print()
    print("Suggested end-screen / final line:")
    print(end)
    print()
    print("Paste into the ## CTA WORDS of draft.md and the ## End screen section of publish.md.")
    print("Run tools/end_screen_scan.py and tools/first_comment_scan.py after to confirm no bait.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
