#!/usr/bin/env python3
"""Write expand.md beat-budget brief from script.md spoken WORDS.

Does not rewrite script.md. Does not invent spoken lines. Does not pad
the sample fixture. A budget row is not a draft.
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from caption_brief import WPM, fmt_ts, script_cues  # noqa: E402
from validate_packet import FORMAT_SPOKEN_WORDS, duration_note, field  # noqa: E402

TARGET_BY_FORMAT = {
    "explainer-6-10min": 1200,
}
HOOK_BAND = (20, 35)
PAYOFF_TARGET = 60
CTA_TARGET = 50
PLACEHOLDER_MARKERS = (
    "status: placeholder",
    "(add spoken lines after script words exist)",
)


def expand_is_filled(text: str) -> bool:
    if not text.strip():
        return False
    low = text.lower()
    if any(p in low for p in PLACEHOLDER_MARKERS):
        return False
    return "status: short" in low or "status: in-band" in low or "status: long" in low


def classify_label(label: str) -> str:
    low = label.lower()
    if low.startswith("hook"):
        return "hook"
    if "payoff" in low:
        return "payoff"
    if low.startswith("beat"):
        return "beat"
    if low.startswith("cta"):
        return "cta"
    return "other"


def budgets(cues: list[dict], fmt: str) -> list[dict]:
    target_total = TARGET_BY_FORMAT.get(fmt, 1200)
    kinds = [classify_label(str(c["label"])) for c in cues]
    n_beats = sum(1 for k in kinds if k == "beat") or 1
    hook_lo, hook_hi = HOOK_BAND
    reserved = hook_lo + PAYOFF_TARGET + CTA_TARGET
    beat_each = max(80, int(round((target_total - reserved) / n_beats)))
    rows = []
    for c, kind in zip(cues, kinds):
        have = int(c["words"])
        if kind == "hook":
            want = hook_lo if have < hook_lo else (have if have <= hook_hi else hook_hi)
            note = "keep 20–35; do not pad the hook"
        elif kind == "payoff":
            want = PAYOFF_TARGET
            note = "one concrete outcome sentence, then how the beats deliver it"
        elif kind == "cta":
            want = CTA_TARGET
            note = "one assignment under two minutes; no subscribe pitch"
        elif kind == "beat":
            want = beat_each
            note = "add a worked example or failure mode inside this beat"
        else:
            want = have
            note = "keep existing heading; do not add extra ## sections"
        add = max(0, want - have)
        rows.append(
            {
                "label": str(c["label"]),
                "kind": kind,
                "have": have,
                "want": want,
                "add": add,
                "note": note,
            }
        )
    return rows


def render(packet: Path) -> str:
    script_path = packet / "script.md"
    packet_path = packet / "packet.md"
    script = script_path.read_text(encoding="utf-8") if script_path.is_file() else ""
    packet_text = packet_path.read_text(encoding="utf-8") if packet_path.is_file() else ""
    fmt = field(packet_text, "format") or "explainer-6-10min"
    cues = script_cues(script)
    spoken = [c for c in cues if int(c["words"]) > 0]
    total = sum(int(c["words"]) for c in cues)
    band = FORMAT_SPOKEN_WORDS.get(fmt, (900, 1500))
    lo, hi = band
    target = TARGET_BY_FORMAT.get(fmt, 1200)
    note = duration_note(fmt, total)
    if total <= 0:
        status = "placeholder"
    elif total < lo:
        status = "short"
    elif total > hi:
        status = "long"
    else:
        status = "in-band"
    generated = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    est = fmt_ts((total / WPM) * 60.0 if total else 0.0)
    need = max(0, target - total) if status == "short" else (max(0, total - hi) if status == "long" else 0)

    if not spoken:
        table = (
            "(add spoken lines after script WORDS exist)\n"
            "- Hook / beats / CTA budgets will appear here.\n"
            "- This file does not write WORDS."
        )
        actions = "- Write WORDS in script.md first. Then re-run this tool."
    else:
        rows = budgets(cues, fmt)
        lines = [
            "| Section | Have | Target | Add | Note |",
            "|---------|-----:|-------:|----:|------|",
        ]
        for r in rows:
            if int(r["have"]) == 0 and r["kind"] == "other":
                continue
            lines.append(
                f"| {r['label']} | {r['have']} | {r['want']} | {r['add']} | {r['note']} |"
            )
        table = "\n".join(lines)
        if status == "short":
            thin = [r for r in rows if r["kind"] == "beat" and r["add"] > 0]
            if not thin:
                thin = [r for r in rows if r["add"] > 0]
            actions = "\n".join(
                f"- Expand `{r['label']}` by about {r['add']} words. {r['note'].capitalize()}."
                for r in thin
            )
            actions += (
                "\n- Do not add extra `##` beats unless count is under 4."
                "\n- Do not pad sample-001. That packet is a fixture."
            )
        elif status == "long":
            actions = (
                f"- Cut about {need} words from the longest beats.\n"
                "- Keep hook in 20–35. Keep one CTA."
            )
        else:
            actions = "- Length is in band. Do not expand for its own sake. Record only after next_action says record-vo."

    warn_line = note or f"spoken {total} words (~{est} at {int(WPM)} wpm) inside {fmt} band {lo}–{hi}"

    return f"""# Expand brief

Status: {status}
Generated: {generated}
Format: {fmt}
Spoken words: {total}
Estimated speech: {est} at {int(WPM)} wpm
Band: {lo}–{hi} (target {target})
Delta to target: {need if status == "short" else (0 if status == "in-band" else need)}
Note: {warn_line}

This file is a beat budget from script.md WORDS. It is not a rewritten
script, not VO, and not permission to pad the sample fixture.
Edit script.md by hand (or with prompts/script_writer.md). Then re-run
`python3 tools/validate_packet.py PATH` and `--duration`.

## Budget
{table}

## Do next
{actions}

## Human
- [ ] Expand existing beats with steps or examples, not slogans
- [ ] Keep hook at 20–35 spoken words
- [ ] Do not invent statistics
- [ ] Do not rewrite videos/sample-001-* WORDS
- [ ] Re-run validate after WORDS change; refresh vo_session.md with --force only on a real packet
"""


def write_empty_expand(dest: Path) -> str:
    path = dest / "expand.md"
    existing = path.read_text(encoding="utf-8") if path.is_file() else ""
    if expand_is_filled(existing):
        return f"kept {dest.name}/expand.md (already filled)"
    path.write_text(render(dest), encoding="utf-8")
    return f"wrote {dest.name}/expand.md"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Write expand.md beat budget from script WORDS. Does not rewrite the script."
    )
    parser.add_argument("packet", help="Path to packet folder")
    parser.add_argument("--dry-run", action="store_true", help="Print expand.md; do not write")
    parser.add_argument("--force", action="store_true", help="Overwrite a filled expand.md")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1

    dest = path / "expand.md"
    existing = dest.read_text(encoding="utf-8") if dest.is_file() else ""
    filled = expand_is_filled(existing)
    if filled and not args.force and not args.dry_run:
        print(f"expand.md already filled; pass --force to overwrite: {dest}", file=sys.stderr)
        return 1

    text = render(path)
    if args.dry_run:
        sys.stdout.write(text)
        return 0

    dest.write_text(text, encoding="utf-8")
    print(dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
