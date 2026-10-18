#!/usr/bin/env python3
"""Pre-apply coach for draft.md: expansion progress + quality + claim + originality + cadence + mechanism alignment signals.

Combines the draft expansion coach view with anti-slop (quality_scan patterns),
unsourced-claim (claim_scan hedges/digits), packet-grounded originality extracts,
cadence/repetition signals, and mechanism-term alignment on the draft spoken WORDS.
Works on draft.md before promotion to script.md. Does not invent lines, numbers,
sources, or anecdotes. Does not write files. One-command pre-apply quality view that
compounds by catching padding, slop, unsupported claims, generic drafts, monotonous
delivery, and mechanism drift early for every future packet.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

try:
    from quality_scan import hits as quality_hits
    from claim_scan import hits as claim_hits
except ImportError as e:
    print(f"import error: {e}", file=sys.stderr)
    sys.exit(1)

def run_tool(name: str, path: Path) -> str:
    tool = ROOT / "tools" / name
    if not tool.is_file():
        return f"({name} missing; skipped)\n"
    proc = subprocess.run([sys.executable, str(tool), str(path)], capture_output=True, text=True)
    out = proc.stdout or ""
    if proc.returncode != 0 and proc.stderr:
        out += f"\n[{name} stderr]: {proc.stderr}"
    return out

def is_clear(section_out: str, section_name: str = "") -> bool:
    """Section-aware heuristic: more accurate CLEAR detection for SUMMARY triage.
    Expansion is clear only with no SHORT/LONG. Quality/claim clear only without hit markers.
    """
    low = section_out.lower()
    if section_name == "expansion":
        return "short" not in low and "long" not in low
    if section_name in ("quality", "claim"):
        return "clear" in low and not any(x in low for x in ("x1", "x2", "hit", "digit", "hedge"))
    # fallback for originality / cadence / mechanism
    clear_markers = ("clear", "no", "none", "pass", "ok")
    if any(m in low for m in clear_markers) and not any(x in low for x in ("x1", "x2", "hit", "missing", "short", "long", "no'")):
        return True
    return "clear" in low and len(section_out.strip().splitlines()) < 8

def recommended_actions(non_clear: list[str], packet_path: Path) -> list[str]:
    """Map non-clear signals to the smallest useful next tool with concrete copy-paste commands (no invent)."""
    p = str(packet_path)
    recs = []
    if "expansion" in non_clear:
        recs.append(f"expansion: python3 tools/draft_short_beat_coach.py {p} or python3 tools/draft_word_progress.py {p}")
    if "quality" in non_clear:
        recs.append(f"quality: revise draft WORDS to remove anti-slop phrases (see quality_scan hits above); then re-run python3 tools/draft_pre_apply_coach.py {p}")
    if "claim" in non_clear:
        recs.append(f"claim: replace unsourced digits/hedges with qualitative language or add source already in research.md; then re-run python3 tools/draft_pre_apply_coach.py {p}")
    if "originality" in non_clear:
        recs.append(f"originality: address 'no' answers in originality extracts (see above); ground in packet mechanism/viewer; then re-run python3 tools/draft_pre_apply_coach.py {p}")
    if "cadence" in non_clear:
        recs.append(f"cadence: vary sentence length and cut repeated n-grams (see cadence_repetition_scan signals); then re-run python3 tools/draft_pre_apply_coach.py {p}")
    if "mechanism" in non_clear:
        recs.append(f"mechanism: weave missing idea.md mechanism terms naturally into WORDS; then re-run python3 tools/draft_pre_apply_coach.py {p}")
    if not recs:
        recs.append(f"all clear: proceed to python3 tools/apply_script.py {p} --from {p}/draft.md --write --refresh after words.py band check")
    return recs

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Pre-apply coach: expansion + quality + claim + originality + cadence + mechanism alignment signals on draft.md. No writes."
    )
    parser.add_argument("packet", help="Packet folder containing draft.md (or script.md), idea.md, research.md")
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    draft = path / "draft.md"
    source = draft if draft.is_file() else path / "script.md"
    if not source.is_file():
        print(f"No draft.md or script.md in {args.packet}", file=sys.stderr)
        return 1

    print("DRAFT PRE-APPLY COACH (expansion + quality + claim + originality + cadence + mechanism alignment signals on draft; no invented content)")
    print(f"Source: {source.name}")
    print(f"Packet: {path.name}")
    print()

    signals = []  # (name, clear: bool)

    # Expansion view
    exp_out = run_tool("draft_expansion_coach.py", path)
    print(exp_out)
    signals.append(("expansion", is_clear(exp_out, "expansion")))

    # Quality and claim on the draft text
    text = source.read_text(encoding="utf-8")
    research = ""
    research_path = path / "research.md"
    if research_path.is_file():
        research = research_path.read_text(encoding="utf-8")

    q_hits = quality_hits(text)
    c_hits = claim_hits(text, research)

    print("## QUALITY SIGNALS (anti-slop phrases in draft WORDS)")
    if not q_hits:
        print("clear")
        signals.append(("quality", True))
    else:
        for phrase, count, ctx in q_hits:
            print(f"- {phrase} x{count} [{ctx}]")
        signals.append(("quality", False))
    print()

    print("## CLAIM SIGNALS (unsourced digits or hedges in draft WORDS)")
    if not c_hits:
        print("clear")
        signals.append(("claim", True))
    else:
        for kind, token, ctx in c_hits:
            print(f"- {kind}:{token} [{ctx}]")
        signals.append(("claim", False))
    print()

    # Originality extracts
    orig_out = run_tool("originality_checklist.py", path)
    print("## ORIGINALITY EXTRACTS")
    print(orig_out)
    signals.append(("originality", is_clear(orig_out, "originality")))

    # Cadence / repetition
    cad_out = run_tool("cadence_repetition_scan.py", path)
    print("## CADENCE & REPETITION SIGNALS")
    print(cad_out)
    signals.append(("cadence", is_clear(cad_out, "cadence")))

    # Mechanism alignment
    mech_out = run_tool("mechanism_align_scan.py", path)
    print("## MECHANISM ALIGNMENT SIGNALS")
    print(mech_out)
    signals.append(("mechanism", is_clear(mech_out, "mechanism")))

    # Summary for quick agent triage
    non_clear = [name for name, clear in signals if not clear]
    print()
    print("## SUMMARY")
    print(f"signals_checked: {len(signals)}")
    print(f"clear_count: {len(signals) - len(non_clear)}")
    if not non_clear:
        print("overall: CLEAR (all mechanical signals clear; ready for apply consideration)")
    else:
        print(f"overall: REVISE ({len(non_clear)} signals need attention: {', '.join(non_clear)})")
    print("Revise draft.md for any non-clear signals before apply_script.py --write.")

    print()
    print("## RECOMMENDED NEXT (signal-specific; copy-paste ready; no invent)")
    for rec in recommended_actions(non_clear, path):
        print(f"- {rec}")

    print()
    print("Next (do not invent sources, numbers, anecdotes, or spoken lines):")
    print("- Revise draft.md for any SHORT beats, quality hits, claim hits, originality 'no' answers, cadence signals, or missing mechanism terms.")
    print("- Prefer concrete mechanism language. Weave missing terms naturally. Vary sentence length. Cut repeated phrases.")
    print("- Then run apply_script.py --write after signals are clear.")
    print("This tool writes nothing. Preferred unblocked path remains human OAuth for publish.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
