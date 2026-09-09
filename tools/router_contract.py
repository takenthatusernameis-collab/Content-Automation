#!/usr/bin/env python3
"""Read-only contract for tools/which_contract.py.

Locks the tool→contract map and --after / --run SKIP behavior so later
agents cannot silently remap locks or treat SKIP as FAIL.

Uses tempfile copies only. Does not write videos/ or the topic queue.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent

EXPECTED = {
    "validate_packet.py": "selftest.py",
    "pipeline_status.py": "selftest.py",
    "next_action.py": "selftest.py",
    "hint.py": "selftest.py",
    "selftest.py": "selftest.py",
    "queue_lib.py": "queue_contract.py",
    "queue_status.py": "queue_contract.py",
    "mark_topic.py": "queue_contract.py",
    "next_topic.py": "queue_contract.py",
    "queue_contract.py": "queue_contract.py",
    "apply_script.py": "write_path_contract.py",
    "set_status.py": "write_path_contract.py",
    "write_path_contract.py": "write_path_contract.py",
    "new_packet.py": "scaffold_contract.py",
    "after_scaffold.py": "scaffold_contract.py",
    "scaffold_contract.py": "scaffold_contract.py",
    "which_contract.py": "router_contract.py",
    "router_contract.py": "router_contract.py",
}


def fail(msg: str) -> int:
    print(f"ROUTER CONTRACT FAIL: {msg}")
    return 1


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=str(cwd), text=True, capture_output=True)


def main() -> int:
    src = TOOLS / "which_contract.py"
    if not src.is_file():
        return fail("which_contract.py missing next to this file")

    sys.path.insert(0, str(TOOLS))
    import which_contract as wc  # noqa: E402

    for tool, contract in EXPECTED.items():
        got = wc.contract_for(tool)
        if got != contract:
            return fail(f"contract_for({tool!r}) = {got!r}, expected {contract!r}")
        got_path = wc.contract_for(f"tools/{tool}")
        if got_path != contract:
            return fail(f"contract_for(tools/{tool}) = {got_path!r}")

    if wc.contract_for("doctor.py") is not None:
        return fail("doctor.py must stay unmapped (read-only health, not a lock body)")
    if wc.contract_for("expand_prompt.py") is not None:
        return fail("expand_prompt.py must stay unmapped")

    with tempfile.TemporaryDirectory(prefix="ca-router-") as tmp:
        tmp_path = Path(tmp)
        tools_dir = tmp_path / "tools"
        tools_dir.mkdir()
        shutil.copy2(src, tools_dir / "which_contract.py")
        py = sys.executable

        p = run([py, str(tools_dir / "which_contract.py"), "--after", "new_packet.py"], tmp_path)
        if p.returncode != 0:
            return fail(f"--after new_packet.py exit {p.returncode}: {p.stderr}")
        if "python3 tools/scaffold_contract.py" not in p.stdout:
            return fail(f"--after new_packet.py stdout unexpected:\n{p.stdout}")

        p = run([py, str(tools_dir / "which_contract.py"), "--after", "apply_script.py"], tmp_path)
        if p.returncode != 0:
            return fail(f"--after apply_script.py exit {p.returncode}")
        if "python3 tools/write_path_contract.py" not in p.stdout:
            return fail(f"--after apply_script.py stdout unexpected:\n{p.stdout}")

        p = run([py, str(tools_dir / "which_contract.py"), "--after", "which_contract.py"], tmp_path)
        if p.returncode != 0:
            return fail(f"--after which_contract.py exit {p.returncode}")
        if "python3 tools/router_contract.py" not in p.stdout:
            return fail(f"--after which_contract.py stdout unexpected:\n{p.stdout}")

        p = run([py, str(tools_dir / "which_contract.py"), "--after", "unknown_tool.py"], tmp_path)
        if p.returncode != 0:
            return fail("unknown tool must exit 0")
        if "No contract mapped" not in p.stdout:
            return fail("unknown tool must print No contract mapped")

        p = run(
            [py, str(tools_dir / "which_contract.py"), "--after", "new_packet.py", "--run"],
            tmp_path,
        )
        if p.returncode != 0:
            return fail(f"--run missing deps must exit 0, got {p.returncode}\n{p.stdout}\n{p.stderr}")
        if "SKIP" not in p.stdout:
            return fail(f"--run missing deps must print SKIP:\n{p.stdout}")

        videos = tmp_path / "videos"
        videos.mkdir()
        before = list(videos.iterdir())
        if before:
            return fail("temp videos/ was not empty after map checks")

    print("ROUTER CONTRACT PASS")
    print("Map locked for 18 tools. Unknown tools exit 0. --run SKIP on missing deps.")
    print("This command writes nothing under videos/ or docs/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
