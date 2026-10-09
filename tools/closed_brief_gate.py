#!/usr/bin/env python3
"""One command for the closed later-packet brief rules.

Run 431 verified four contracts and three title dry-runs, then stopped
the stub-edit loop. Later agents were still re-running that by hand and
inventing a new packet when the named rules already passed. This gate is
that verification. It does not edit generators, does not write a packet,
does not poll secrets, and does not dispatch a workflow.

Exit 0 only when the named rules still hold. A failure is the only reason
to edit publish_brief, chapter_draft, caption_brief, asset_brief, or
title_thumb_brief.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent

CONTRACTS = (
    ("tools/publish_brief_contract.py", "PUBLISH BRIEF CONTRACT PASS"),
    ("tools/chapter_draft_contract.py", "CHAPTER DRAFT CONTRACT PASS"),
    ("tools/caption_brief_contract.py", "CAPTION BRIEF CONTRACT PASS"),
    ("tools/asset_brief_contract.py", "ASSET BRIEF CONTRACT PASS"),
    ("tools/title_brief_contract.py", "TITLE BRIEF CONTRACT PASS"),
)

# Shapes named in Run 431. Do not add a new shape here to hunt a new leak.
TITLE_PACKETS = (
    (
        "012-leave-charger-before",
        "- topic: Leave the charger in the kitchen before the next block\n"
        "- problem: The charger stays within arm reach before the block\n"
        "- mechanism (the system, not the pep talk): Leave the charger in the kitchen before the block\n",
    ),
    (
        "013-phone-where",
        "- topic: Put the phone where the hand cannot reach it\n"
        "- problem: The phone stays where the hand can reach it\n"
        "- mechanism (the system, not the pep talk): Put the phone in another room where the block starts\n",
    ),
    (
        "014-notebook-and",
        "- topic: Leave the notebook in the bag and start the block\n"
        "- problem: The notebook stays in the bag and the block has no page\n"
        "- mechanism (the system, not the pep talk): Leave the notebook in the bag and write the next line first\n",
    ),
)


def _run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)


def check_contracts() -> list[str]:
    failures: list[str] = []
    for rel, marker in CONTRACTS:
        path = ROOT / rel
        if not path.is_file():
            failures.append(f"missing {rel}")
            continue
        proc = _run([sys.executable, str(path)], ROOT)
        if proc.returncode != 0 or marker not in proc.stdout:
            failures.append(
                f"{rel} failed: {proc.stdout[-300:]} {proc.stderr[-200:]}"
            )
    return failures


def check_title_dry_runs() -> list[str]:
    failures: list[str] = []
    tool = TOOLS / "title_thumb_brief.py"
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for slug, idea in TITLE_PACKETS:
            packet = root / slug
            packet.mkdir()
            (packet / "idea.md").write_text("# Idea\n\n" + idea, encoding="utf-8")
            proc = _run([sys.executable, str(tool), str(packet), "--dry-run"], ROOT)
            if proc.returncode != 0 or "SELF_CHECK PASS" not in proc.stdout:
                failures.append(
                    f"{slug} title dry-run failed: {proc.stdout[-300:]} {proc.stderr[-200:]}"
                )
                continue
            thumb = ""
            for line in proc.stdout.splitlines():
                if line.startswith("On-image text"):
                    thumb = line.split(":", 1)[-1].strip()
            last = thumb.split()[-1].lower().strip(".,;:") if thumb else ""
            if last in {"before", "after", "into", "where", "and"}:
                failures.append(f"{slug} thumb ended on {last}: {thumb}")
    return failures


def main() -> int:
    failures = check_contracts() + check_title_dry_runs()
    if failures:
        print("CLOSED BRIEF GATE FAIL", file=sys.stderr)
        for item in failures:
            print(f"  - {item}", file=sys.stderr)
        return 1
    print("CLOSED BRIEF GATE PASS")
    print("contracts=5 title_dry_runs=3")
    print("do_not_edit=publish_brief,chapter_draft,caption_brief,asset_brief,title_thumb_brief")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
