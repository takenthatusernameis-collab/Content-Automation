#!/usr/bin/env python3
"""Single-command priority review summary across key QA tools.

Runs quality_scan.py, originality_report.py, caption_quality_summary.py,
metadata_qa_report.py, research_verification_checklist.py, and (when packet
given) labor_estimate.py for a packet (or default videos/* for quality_scan),
then extracts and prints only their PRIORITY / high-signal sections plus a
short remaining-minutes line, a suggested focus (with estimated clear minutes from labor map), cumulative high-signal clear time, suggested next local step from labor_estimate, and recommended next commands.

Does not rewrite files, invent content/media, upload, or call network.
Soft only. Compounds by giving humans one focused entry point instead of
multiple sequential reports. Exit 0 always (individual tools may signal issues).
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"

# Rough minutes ranges for high-signal categories (from labor map)
CATEGORY_MINUTES = {
    "quality": (5, 15),
    "originality": (5, 15),
    "captions": (8, 18),
    "metadata": (4, 8),
    "research": (1, 5),
    "none": (0, 0),
}


def run_tool(script: str, args: list[str]) -> tuple[int, str]:
    path = TOOLS / script
    if not path.is_file():
        return 1, f"MISSING {script}"
    cmd = [sys.executable, str(path)] + args
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        out = (proc.stdout or "").strip()
        if proc.stderr:
            out += "\n" + proc.stderr.strip()
        return proc.returncode, out
    except Exception as exc:
        return 1, f"EXCEPTION {script}: {exc}"


def extract_priority_block(output: str) -> list[str]:
    """Pull lines from a PRIORITY section or high-signal header."""
    lines = []
    in_priority = False
    for line in output.splitlines():
        stripped = line.strip()
        if "--- Priority review" in line or "PRIORITY:" in line.upper() or "high-signal" in line.lower():
            in_priority = True
            if stripped and not stripped.startswith("---"):
                lines.append(stripped)
            continue
        if in_priority:
            if stripped.startswith("---") or stripped.startswith("=") or (not stripped and lines):
                break
            if stripped:
                lines.append(stripped)
    return lines[:8]


def extract_research_signals(output: str) -> list[str]:
    """Pull high-signal research lines: unlinked, WARNING, secondary dominance."""
    signals = []
    for line in output.splitlines():
        stripped = line.strip()
        if any(k in stripped.upper() for k in ("UNLINKED", "WARNING", "SECONDARY", "NO SOURCES.MD", "POTENTIAL QUANTITATIVE")):
            if stripped and len(stripped) < 200:
                signals.append(stripped)
    return signals[:6]


def extract_labor_minutes(output: str) -> str:
    """Pull the estimated remaining minutes line from labor_estimate output."""
    for line in output.splitlines():
        if "Estimated remaining human minutes:" in line:
            return line.strip()
    m = re.search(r"Estimated remaining human minutes:\s*(\d+)", output)
    if m:
        return f"Estimated remaining human minutes: {m.group(1)}"
    return "(labor estimate unavailable)"


def extract_next_local_step(output: str) -> str:
    """Pull the SUGGESTED NEXT LOCAL STEP section from labor_estimate output."""
    lines = []
    in_section = False
    for line in output.splitlines():
        if "## SUGGESTED NEXT LOCAL STEP" in line:
            in_section = True
            continue
        if in_section:
            if line.strip().startswith("##") or (not line.strip() and lines):
                break
            if line.strip():
                lines.append(line.strip())
    if lines:
        return " | ".join(lines[:3])
    return "(next local step unavailable; run labor_estimate.py directly)"


def suggest_focus(signals: dict[str, list[str]]) -> tuple[str, str]:
    """Suggest primary focus area and the top category key based on which has most high-signal items."""
    counts = {k: len(v) for k, v in signals.items() if v}
    if not counts:
        return "No high-signal issues detected. Proceed to next stage or OAuth dispatch when ready.", "none"
    top = max(counts, key=counts.get)
    suggestions = {
        "quality": "Focus script anti-slop review first (rephrase multi-count weak phrases).",
        "originality": "Focus script originality signals (add concrete markers or lived experience).",
        "captions": "Focus caption quality (slow high-CPS cues or check alignment).",
        "metadata": "Focus metadata QA (fix high-signal title/desc/tag issues).",
        "research": "Focus research verification (link unlinked claims or strengthen sources).",
    }
    return suggestions.get(top, f"Focus {top} signals first."), top


def recommend_next_commands(top: str, packet: str | None) -> list[str]:
    """Return concrete next tool invocations for the suggested focus."""
    pkt = packet if packet else "<packet>"
    mapping = {
        "quality": [
            f"python3 tools/quality_scan.py {pkt}",
            "# Rephrase the multi-count / known-weak phrases listed above, then re-scan.",
        ],
        "originality": [
            f"python3 tools/originality_report.py {pkt}",
            "# Add concrete markers, lived-experience, or mechanism specificity, then re-run.",
        ],
        "captions": [
            f"python3 tools/caption_quality_summary.py {pkt}",
            "# Slow the high-CPS cues or verify alignment; do not treat draft as final.",
        ],
        "metadata": [
            f"python3 tools/metadata_qa_report.py {pkt}",
            "# Fix title/description/tag high-signal issues, then re-run the report.",
        ],
        "research": [
            f"python3 tools/research_verification_checklist.py {pkt}",
            "# Link unlinked claims or strengthen secondary-dominated sources, then re-check.",
        ],
        "none": [
            "python3 tools/labor_estimate.py" + (f" {pkt}" if packet else ""),
            "# No high-signal issues. Proceed toward OAuth dispatch or next production stage.",
        ],
    }
    return mapping.get(top, [f"# No specific command mapped for {top}"])


def estimate_focus_minutes(top: str) -> str:
    """Rough minutes to clear the top category, from labor map ranges."""
    estimates = {
        "quality": "5-15 (script anti-slop rephrase)",
        "originality": "5-15 (add concrete markers / lived experience)",
        "captions": "8-18 (slow high-CPS cues or align)",
        "metadata": "4-8 (title/desc/tag fixes)",
        "research": "1-5 (link claims or strengthen sources)",
        "none": "0 (clear; proceed to OAuth or next stage)",
    }
    return estimates.get(top, "see labor_reduction_map.md")


def estimate_cumulative_minutes(signals: dict[str, list[str]]) -> str:
    """Sum rough min-max for all categories that have high-signal items."""
    low = 0
    high = 0
    active = []
    for cat, items in signals.items():
        if items and cat in CATEGORY_MINUTES:
            lo, hi = CATEGORY_MINUTES[cat]
            low += lo
            high += hi
            active.append(cat)
    if not active:
        return "0 (no high-signal categories)"
    return f"{low}-{high} across {len(active)} categories ({', '.join(active)})"


def main() -> int:
    packet = sys.argv[1] if len(sys.argv) > 1 else None
    print("PRIORITY REVIEW SUMMARY (high-signal issues only; for focused human spot-check)")
    print("Aggregates: quality_scan, originality_report, caption_quality_summary, metadata_qa_report, research_verification")
    if packet:
        print("+ labor_estimate (remaining minutes + next local step)")
    print("Does not rewrite, invent, or upload. Review signals only.")
    print("=" * 72)

    signals: dict[str, list[str]] = {
        "quality": [],
        "originality": [],
        "captions": [],
        "metadata": [],
        "research": [],
    }

    next_step_text = ""
    # 0. Labor estimate (when packet given) — surface first for planning
    if packet:
        _, l_out = run_tool("labor_estimate.py", [packet])
        labor_line = extract_labor_minutes(l_out)
        next_step_text = extract_next_local_step(l_out)
        print(f"\n## LABOR ESTIMATE")
        print(f"  {labor_line}")
        print(f"  Next local step: {next_step_text}")
        print("  (rough planning number; see full table via labor_estimate.py if needed)")
    else:
        print("\n## LABOR ESTIMATE")
        print("  (skipped: provide packet path)")

    # 1. Quality scan (anti-slop)
    q_args = [packet] if packet else []
    _, q_out = run_tool("quality_scan.py", q_args)
    q_pri = extract_priority_block(q_out)
    signals["quality"] = q_pri
    print("\n## SCRIPT ANTI-SLOP (quality_scan)")
    if q_pri:
        for line in q_pri:
            print(f"  {line}")
    else:
        print("  (no high-signal priority hits or clear)")

    # 2. Originality (requires packet)
    if packet:
        _, o_out = run_tool("originality_report.py", [packet])
        o_pri = extract_priority_block(o_out)
        signals["originality"] = o_pri
        print("\n## SCRIPT ORIGINALITY")
        if o_pri:
            for line in o_pri:
                print(f"  {line}")
        else:
            print("  (no high-signal priority signals or clear)")
    else:
        print("\n## SCRIPT ORIGINALITY")
        print("  (skipped: provide packet path for originality_report)")

    # 3. Captions
    if packet:
        _, c_out = run_tool("caption_quality_summary.py", [packet])
        c_pri = extract_priority_block(c_out)
        signals["captions"] = c_pri
        print("\n## CAPTIONS")
        if c_pri:
            for line in c_pri:
                print(f"  {line}")
        else:
            print("  (no high-signal priority cues or absent)")
    else:
        print("\n## CAPTIONS")
        print("  (skipped: provide packet path)")

    # 4. Metadata
    if packet:
        _, m_out = run_tool("metadata_qa_report.py", [packet])
        m_pri = extract_priority_block(m_out)
        signals["metadata"] = m_pri
        print("\n## METADATA")
        if m_pri:
            for line in m_pri:
                print(f"  {line}")
        else:
            print("  (no high-signal priority issues or clear)")
    else:
        print("\n## METADATA")
        print("  (skipped: provide packet path)")

    # 5. Research verification (high-signal only)
    if packet:
        _, r_out = run_tool("research_verification_checklist.py", [packet])
        r_sig = extract_research_signals(r_out)
        signals["research"] = r_sig
        print("\n## RESEARCH VERIFICATION")
        if r_sig:
            for line in r_sig:
                print(f"  {line}")
        else:
            print("  (no high-signal unlinked/warning items or clear)")
    else:
        print("\n## RESEARCH VERIFICATION")
        print("  (skipped: provide packet path)")

    # Suggested focus based on signal counts
    focus, top_cat = suggest_focus(signals)
    print("\n## SUGGESTED FOCUS")
    print(f"  {focus}")
    print("  (based on highest number of high-signal items; still review all sections)")
    est = estimate_focus_minutes(top_cat)
    print(f"  Estimated minutes to clear: {est}")
    cum = estimate_cumulative_minutes(signals)
    print(f"  Rough cumulative high-signal clear time: {cum}")

    # Recommended next commands
    next_cmds = recommend_next_commands(top_cat, packet)
    print("\n## RECOMMENDED NEXT COMMANDS")
    for cmd in next_cmds:
        print(f"  {cmd}")
    print("  (copy-paste ready; re-run this summary after edits to confirm signals clear)")

    print("\n" + "=" * 72)
    print("PRIORITY REVIEW SUMMARY DONE.")
    print("Focus on the lines above first. Re-run individual tools for full context.")
    print("Do not treat any of this as a hard gate or upload approval.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
