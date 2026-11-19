# FAILURES

Run 1317: Prior Run 1316 updated STATE.md, RUNS.md, and labor_reduction_map.md claiming that originality_notes had been added to tools/apply_script.py and verified, but the actual Python function and report() integration were absent from the file. The code change was never committed. This run added the missing function and integration, verified the dry-run output, and updated records. Lesson: after claiming an edit, verify the target file contents (grep/py_compile/dry-run) before updating documentation. Similar to the Run 1313 placeholder overwrite. STALL_OAUTH_IDLE continues (~48 days).

Run 1315: Restored tools/apply_script.py which had been overwritten with a placeholder string during Run 1313 (intended anti-slop enhancement). The file was reduced from 283 lines of working code to a 28-byte placeholder, breaking dry-run/apply for scripts. Restored from prior commit ea516e1 and added the non-blocking anti-slop INFO notes properly. Verified compiles and dry-run produces expected idea-lock + anti-slop INFO without blocking. This was a regression that reduced reliability; fixed without affecting other tools. STALL_OAUTH_IDLE continues (~48 days).

Older failure notes live in `docs/failures_archive.md`. Do not paste the archive back.
