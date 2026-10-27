#!/usr/bin/env python3
"""Generate all local preview PNGs for a packet in one command.

Runs the existing deterministic preview generators (assets, captions, chapters,
publish package, pacing, storyboard, end-screen, thumbnail, title variants,
VO waveform, VO stats, packet status, hook, claims) and reports which succeeded.
Then generates a review contact sheet from the available previews.
No invented content. Outputs stay local and gitignored.

Reduces recurring human labor of remembering and invoking each preview tool
separately on every future packet. One command produces the full visual review set
plus a single overview sheet.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

PREVIEWS = [
    ("assets", "tools/assets_preview.py"),
    ("captions", "tools/captions_preview.py"),
    ("chapters", "tools/chapters_preview.py"),
    ("publish", "tools/publish_package_preview.py"),
    ("pacing", "tools/pacing_timeline.py"),
    ("storyboard", "tools/storyboard_preview.py"),
    ("end_screen", "tools/end_screen_preview.py"),
    ("thumbnail", "tools/thumbnail_generator.py"),
    ("title_variants", "tools/title_variants_preview.py"),
    ("vo_waveform", "tools/vo_waveform_preview.py"),
    ("vo_stats", "tools/vo_stats_card.py"),
    ("packet_status", "tools/packet_status_card.py"),
    ("hook", "tools/hook_preview.py"),
    ("claims", "tools/claims_preview.py"),
    ("structure", "tools/structure_preview.py"),
]


def run_one(script: Path, packet: Path) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            [sys.executable, str(script), str(packet)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        ok = result.returncode == 0
        msg = (result.stdout or result.stderr or "").strip().splitlines()[-1] if (result.stdout or result.stderr) else ""
        return ok, msg or ("ok" if ok else "failed")
    except Exception as e:
        return False, str(e)


def main() -> int:
    p = argparse.ArgumentParser(description="Generate all local preview PNGs for a packet")
    p.add_argument("packet", type=Path, help="Path to video packet folder")
    args = p.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"ERROR: not a directory: {packet}", file=sys.stderr)
        return 1

    repo_root = Path(__file__).resolve().parent.parent
    print(f"packet: {packet.name}")
    print(f"generating previews...")

    results = []
    for name, rel in PREVIEWS:
        script = repo_root / rel
        if not script.is_file():
            results.append((name, False, "script missing"))
            continue
        ok, msg = run_one(script, packet)
        results.append((name, ok, msg))
        status = "OK" if ok else "FAIL"
        print(f"  {status:4} {name:16} {msg}")

    ok_count = sum(1 for _, ok, _ in results if ok)
    print(f"\n{ok_count}/{len(results)} previews generated (binaries gitignored)")

    # Generate overview contact sheet if any previews succeeded
    if ok_count > 0:
        sheet_script = repo_root / "tools" / "review_contact_sheet.py"
        if sheet_script.is_file():
            print("\ngenerating review contact sheet...")
            ok, msg = run_one(sheet_script, packet)
            status = "OK" if ok else "FAIL"
            print(f"  {status:4} review_sheet     {msg}")
        else:
            print("\n(review_contact_sheet.py not found; skipping overview)")

    return 0 if ok_count > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
