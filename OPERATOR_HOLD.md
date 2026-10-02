# OPERATOR HOLD

> Escalation policy: `docs/operator_escalation.md`.

The 24-hour selected-VO request dated 2026-09-18 elapsed at 2026-09-19T00:00:00Z.
Generated narration is now the authorized fallback. It must stay labeled generated.

Q1 still has no git-visible Selected VO file. Audio remains gitignored. Do not `git add -f` a take. Do not bump status past `ready_for_vo` unless a packet-relative take exists on the machine running the gates.

Do not keep aligning documentation, adding guards, rewriting prompts, creating wrapper CLIs, or scaffolding Q2 unless a genuine regression blocks the next action.

A human take at the packet-relative DROP path may replace the generated fallback. Update `vo_origin.md` to `kind: human` only when that file is real.

Run 248 left the already-verified generated wav and seven cards in the operator chat as `q1-handoff-verified.zip` (19908902 bytes). Copy those files onto the packet paths in `HANDOFF.md`. That zip is not Selected VO until the copy exists on the gate machine. Runs 239–248 have not performed that copy. Do not ask the next agent to re-download unless this zip was lost.

Run 250 verified `gh release download q1-media-r249` checksums and fixed extract_words (multiline WORDS were ignored). Run 253 published the padded master on `q1-media-r253` (`q1-master-r253.mp4`, 328.40s). Run 256 removed the HANDOFF command that copied r249 `q1-master.mp4` onto export/master.mp4. Upload still needs a human publish.md edit plus YouTube OAuth. `youtube_upload.py` refuses the truncated sha and the stub description.

Run 257: live-job pages and next_action no longer treat a new recording as the Q1 job. Human publish.md edit and YouTube OAuth remain. Do not regenerate.

Run 258: gate_machine.md and pipeline_status no longer treat a new recording as the Q1 job. Human publish.md edit and YouTube OAuth remain. Do not regenerate.
\nRun 260: operator pages no longer say delete `No upload happened`. Human publish.md check and YouTube OAuth remain. Do not regenerate. Do not restore the stub.\n