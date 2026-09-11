# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-11T02:10:00Z — Run 061

- **Objective:** After PASTE READY prints apply `--from PATH/draft.md`, stop the missing-file traceback. No new idea_brief flag, no reconstruct wave, no idea.md write.
- **Inspected:** STATE/NEXT/RUNS after Run 060. idea_brief already names PATH/draft.md. apply_script read `--from` with Path.read_text and no existence check. Q1 still queued.
- **Action taken:** Added `missing_source_error` and `load_source` to apply_script. Missing `--from` path prints a draft.md save hint, says draft.md is not script.md, writes nothing, exits 2. Existing draft.md still loads. write_path_contract now locks that message and load_source codes. Did not edit idea_brief, needed.py, doctor, or human_session. Did not scaffold Q1. Did not write idea.md.
- **Result:** Helper unit check locally printed the missing-source block and HELPER OK. Full write_path_contract / selftest not reconstructed this run (clone-less; set_status imports pipeline_status -> render_brief). Queue rows remain queued. No new packet folder.
- **Verification status:** completed for missing-source helper text (local). partial for write_path_contract runtime (source lock added, not executed end-to-end). No media.
- **Important discovery:** Naming draft.md in idea_brief is not enough if apply_script still stack-traces when the human runs the printed line too early. Exit 2 + hint is cheaper than another flag.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. ffmpeg recipe parked until VO + cards exist. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human runs `python3 tools/queue_status.py` then follows `docs/human_session.md`. After scaffold, `--block` / paste / `--check` / expand off-repo / save draft.md / apply dry-run. After editing apply_script, run `write_path_contract.py` on a reconstructed tools tree. Do not add another idea_brief flag. Do not add WAVE 4. Do not auto-write idea.md. Do not auto-scaffold Q1.

## 2026-09-11T01:20:00Z — Run 060

- **Objective:** After PASTE READY prints apply_script `--from FILE`, stop the human from inventing FILE. Pin a packet-local `draft.md` path. No new flag, no reconstruct wave, no idea.md write.
- **Result:** IDEA BRIEF CONTRACT PASS. PASTE READY apply uses PATH/draft.md.
- **Recommended next action:** Human runs queue_status then human_session.

## Earlier runs 001–59
See prior commits for full detail.
