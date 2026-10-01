# NEXT

Do these in order. Stop if a step needs a human decision that is not present.

1. **Highest value:** Do not record or regenerate Q1. `next_action.py` now returns `upload-blocked` for this packet. Do not re-encode. Do not upload `q1-media-r249` `q1-master.mp4` (truncated, 308.40s, sha256 `abec4eb94199d0cbbf00659891d4e79c0040a6b1bb5450fa6e1db0e54c4b4d53`). The finished local export is private release `q1-media-r253` asset `q1-master-r253.mp4` (328.40s, 6633603 bytes, sha256 `4ff4c0e80ac6b5719aa1b8b5acc70b2845820208f56e83881f6e7bad30101546`, ftyp+moov, 1920x1080). Fetch with `gh release download q1-media-r253 --repo takenthatusernameis-collab/Content-Automation -D /tmp/q1-media-r253`. Place `q1-master-r253.mp4` at `videos/002-stop-deciding-what-to-work-on-every-morning/export/master.mp4` only as a local copy. Wav and PNGs come from `q1-media-r249` only; do not copy that release's `q1-master.mp4`. HANDOFF.md (Run 256) and docs/gate_machine.md already say this. Do not `git add -f`. Before OAuth, edit publish.md so the description no longer contains "No upload happened" and check Description edited + First comment approved. youtube_upload now HOLD_LOCAL until that copy is approved. Remaining credential gate is YouTube OAuth (`YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN`), then `python3 tools/youtube_upload.py PATH`. Dry-run READY is not an upload. Do not regenerate the wav or cards while HANDOFF checksums match. Generated audio is an authorized labeled fallback (`vo_origin.md` kind=generated).
2. After a real selected take exists on disk: `python3 tools/vo_session.py PATH --force` then `python3 tools/set_status.py PATH --to ready_for_edit` dry-run; `--write` only if Selected VO present and gate still PASS. Keep `vo_origin.md` kind honest.
3. On the same machine: copy the seven Drive PNGs from `HANDOFF.md` into `cards/`, then `python3 tools/card_generator.py PATH --inspect-only`. Use `--write-manifest` only if inspect-only reports missing. Requires Pillow only for a regenerate. Do not commit binaries. `--mark-ready` only after inspect-only reports all yes. `tools/hint.py` and `tools/next_action.py` build-cards now name this command; do not revert them to a stock-download comment.
4. `python3 tools/timeline.py PATH --write`. Then `python3 tools/media_qa.py PATH`. Expect vo_peak/vo_rms/vo_silence/vo_clip rows. export_decodable stays FAIL until a real ftyp master exists; that is expected. Confirm ready_to_assemble and media_qa gate before any ffmpeg work. Then `python3 tools/assemble.py PATH` (expect HOLD_MEDIA until VO+cards exist). `--execute` only if gate is READY_TO_ENCODE. `tools/hint.py` and `tools/next_action.py` edit now name this sequence; do not restore editor-only or "do not write an ffmpeg recipe here".
5. Do not treat YOUTUBE_AUTH_REQUIRED as the only remaining gate while publish.md still has unchecked Human before upload items or the stub sentence "No upload happened". That copy is HOLD_LOCAL.
5b. After a local master exists with a real ftyp box: `python3 tools/youtube_upload.py PATH`. Expect `YOUTUBE_AUTH_REQUIRED` until OAuth env is present. A junk master.mp4 is HOLD_LOCAL, not READY. The r249 truncated sha and a VO-length master missing the 20s end screen are also HOLD_LOCAL. Do not pass secrets. Do not treat dry-run READY as an upload.
6. After upload_state.json contains a real provider_video_id: `python3 tools/youtube_feedback.py PATH`. Expect HOLD_UNPUBLISHED until then. Do not invent metrics. Do not call Analytics APIs from this tool.
7. After feedback metrics exist: `python3 tools/experiment_loop.py PATH`. Expect HOLD_NO_EVIDENCE until then. Do not invent a keep/discard. Do not rewrite an old script to make a test look successful.
8. `python3 tools/complete.py PATH`. Expect INCOMPLETE_MEDIA until VO+cards exist. A junk master.mp4 is not a master. Do not treat markdown, a named export path, a video ID, or a pending experiment as COMPLETE.
9. Human-edit `publish.md` description + approve pin comment (`docs/human_session.md` step 7). Tags already trimmed (Run 117). Do not upload.
10. Do **not** add another wrapper CLI. Do **not** map doctor.py. Do **not** scaffold Q2 yet. Do **not** add another operator/agent page that only restates this list. Do **not** re-implement `selected_vo_drop` in a second module. Do **not** add a TTS wrapper under tools/.
11. Do **not** make apply_script or words.py idea-lock INFO a check() error or a status bump.
12. Do **not** map idea_lock.py / words.py / words_contract.py / placeholder_guard.py / prove_locks.py / idea_brief.py / idea_brief_contract.py / doctor.py.
13. Do **not** attempt YouTube OAuth or publishing without credentials or a real VO file.
14. Do **not** run `assemble.py --execute` until `timeline.py` prints ready_to_assemble=yes and `media_qa.py` prints gate PASS. The optional TTS ffmpeg one-liners on `docs/gate_machine.md` are not assemble execute. Do not re-encode Q1 while `q1-media-r253` exists.
18. Do **not** run apply_script --write against sample-001.
22. Do **not** retry HTTPS clone after one failure.
27. Do **not** have new_packet or idea_brief write idea.md.
40. Do **not** treat draft.md as script.md.
56. Do **not** make words.py --strict fail on idea-lock INFO alone.
64. Do **not** strip the empty-script Target column from docs/human_session.md step 3.
65. Do **not** strip the Target comment from hint.py write-script/expand-script commands.
66. Do **not** re-implement `selected_vo_drop` in a second module.
67. Do **not** describe generated VO as a human recording.
68. Do **not** `git add -f` generated card PNGs.
69. Do **not** call videos.insert from `youtube_upload.py`.
70. Do **not** treat an assemble recipe as a master export.
71. Do **not** treat empty feedback metrics as collected audience evidence.
72. Do **not** treat a pending experiment_loop record as a keep/discard result.
73. Do **not** treat `complete.py` INCOMPLETE_* as a reason to invent media, an upload, metrics, or a result.
74. Do **not** claim a selftest lock is on HEAD unless `DROP_IMPORTERS` in `tools/selftest.py` includes the new printer and a fail-closed fixture is called from `main()`.
75. Do **not** treat media_qa level FAIL as a reason to invent a quieter or louder wav in git.
76. Do **not** write a dummy `export/master.mp4` to flip assemble EXPORT_EXISTS or complete master_export_present.
77. Do **not** treat youtube_upload size>0 as master_export_present. Require `mp4_header_ok`.
78. Do **not** add another selftest fixture or dry-run adapter unless a live printer on HEAD is proven to accept junk media, invent metrics, or call a provider API. Run 226 already locked upload junk-masters.
79. Do **not** treat `docs/gate_machine.md` or the Drive file id as permission to commit a wav or PNG from the agent sandbox.
80. Do **not** restore "recording is the only gate" or blanket "do not write an ffmpeg recipe" wording on human_session, agent_session, or hint.py edit commands.
81. Do **not** strip the `docs/gate_machine.md` pointer from hint.py, next_action.py, or pipeline_status.py.
82. Do **not** keep aligning remaining record-vo printers unless a proven omission blocks the drop. Post-VO hint alignment landed in Run 233. Post-VO next_action Why text landed in Run 234.
83. Do **not** strip `docs/gate_machine.md` from `tools/needed.py` BOOTSTRAP or doctor UNMAPPED_PATHS. Do not grow bootstrap further unless a reconstruct omission is proven.
84. Do **not** strip the Q1 `docs/gate_machine.md` hold from `tools/queue_status.py` or `tools/next_topic.py`. Do not treat WAVE 3 board output as scaffold permission.
85. Do **not** move scaffold copy-paste (`idea_brief.py --queue` / `new_packet.py`) above the Q1 hold line in `queue_status.py`, `next_topic.py`, or the doctor footer. `queue_contract.py` locks hold-before-scaffold order.
86. Do **not** move README Human session / Local tools `doctor.py`, `idea_brief.py`, `new_packet.py`, or sample-001 commands above the live Q1 drop / `narration_adapter.py` block.
87. Do **not** commit another documentation-order, printer-alignment, or state-page-only run unless a proven HEAD regression sends an operator to scaffold Q2, invent media, or strip a locked hold. Runs 227–238 already closed the known first-command stalls. If Selected VO is still missing and no regression is proven, prefer no commit.
88. Do **not** regenerate the Q1 generated wav while Drive file `1lnk7JB9uu2puCsWPuyScs_CchoQZsxZl` lists 27200958 bytes and `HANDOFF.md` still names sha256 `758bfa4056c7d3ce588dafe7b40c5cccdd3a54df429ecf4583fa256cb1591da2`. Session artifacts are not the durable copy. That file is not Selected VO until copied to the DROP path.
89. Do **not** regenerate the seven Q1 cards while the Drive ids and byte sizes in `HANDOFF.md` still match. Those PNGs are not packet cards until copied under `videos/002-stop-deciding-what-to-work-on-every-morning/cards/`.
90. Do **not** restore the HANDOFF command that copied `q1-media-r249` `q1-master.mp4` onto `export/master.mp4`. Run 256 removed it. The uploader already refuses that sha.

91. Do **not** restore the human_session / agent_session live job that says the remaining labor is a new DROP recording. Run 257 pointed that labor at the publish.md stub edit.
92. Do **not** make `next_action.py` return `record-vo` for `002-stop-deciding-what-to-work-on-every-morning` while the r249/r253 releases exist.
