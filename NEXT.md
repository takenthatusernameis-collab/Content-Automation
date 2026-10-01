# NEXT

Do these in order. Stop if a step needs a human decision that is not present.

1. **Highest value:** On the gate machine, download Drive file id `1lnk7JB9uu2puCsWPuyScs_CchoQZsxZl` (folder `1ftaVyh8BWQeWp45TIyX7Hh1o0MPmGRev`) onto the packet-relative DROP path and check sha256 against `HANDOFF.md` (`758bfa4056c7d3ce588dafe7b40c5cccdd3a54df429ecf4583fa256cb1591da2`, 27200958 bytes). DROP: `videos/002-stop-deciding-what-to-work-on-every-morning/vo/002-stop-deciding-what-to-work-on-every-morning-take-selected.wav` (or .flac). Also copy the seven card ids in `HANDOFF.md` into `videos/002-stop-deciding-what-to-work-on-every-morning/cards/`. Follow `docs/gate_machine.md`. Generated audio is an authorized labeled fallback (`vo_origin.md` kind=generated). Optional already-installed TTS one-liners are on that page; do not wrap them into tools/. Repo-root `vo/` is ignored. Do not invent a wav in git. Do not `git add -f` the take or the PNGs. Do not regenerate the wav while that Drive file lists 27200958 bytes. Do not regenerate the cards while the `HANDOFF.md` sizes match. Inspect with `python3 tools/narration_adapter.py PATH`. `python3 tools/hint.py PATH`, `python3 tools/next_action.py PATH`, and `python3 tools/pipeline_status.py PATH` now name that page; do not strip those pointers. Clone-less reconstruct now fetches that page in `needed.py --bootstrap` and `needed.py doctor.py`; do not strip it from BOOTSTRAP or doctor UNMAPPED_PATHS. WAVE 3 `queue_status.py` / `next_topic.py` print the Q1 hold *before* scaffold copy-paste; do not treat those printers as permission to scaffold Q2. README Human session / Local tools now lead with that drop; do not move doctor/idea_brief/new_packet/sample-001 above it. Flag: runs 239–245 have not placed a file at the DROP path. Another Drive upload is not that copy.
2. After a real selected take exists on disk: `python3 tools/vo_session.py PATH --force` then `python3 tools/set_status.py PATH --to ready_for_edit` dry-run; `--write` only if Selected VO present and gate still PASS. Keep `vo_origin.md` kind honest.
3. On the same machine: copy the seven Drive PNGs from `HANDOFF.md` into `cards/`, then `python3 tools/card_generator.py PATH --inspect-only`. Use `--write-manifest` only if inspect-only reports missing. Requires Pillow only for a regenerate. Do not commit binaries. `--mark-ready` only after inspect-only reports all yes. `tools/hint.py` and `tools/next_action.py` build-cards now name this command; do not revert them to a stock-download comment.
4. `python3 tools/timeline.py PATH --write`. Then `python3 tools/media_qa.py PATH`. Expect vo_peak/vo_rms/vo_silence/vo_clip rows. export_decodable stays FAIL until a real ftyp master exists; that is expected. Confirm ready_to_assemble and media_qa gate before any ffmpeg work. Then `python3 tools/assemble.py PATH` (expect HOLD_MEDIA until VO+cards exist). `--execute` only if gate is READY_TO_ENCODE. `tools/hint.py` and `tools/next_action.py` edit now name this sequence; do not restore editor-only or "do not write an ffmpeg recipe here".
5. After a local master exists with a real ftyp box: `python3 tools/youtube_upload.py PATH`. Expect `YOUTUBE_AUTH_REQUIRED` until OAuth env is present. A junk master.mp4 is HOLD_LOCAL, not READY. Do not pass secrets. Do not treat dry-run READY as an upload.
6. After upload_state.json contains a real provider_video_id: `python3 tools/youtube_feedback.py PATH`. Expect HOLD_UNPUBLISHED until then. Do not invent metrics. Do not call Analytics APIs from this tool.
7. After feedback metrics exist: `python3 tools/experiment_loop.py PATH`. Expect HOLD_NO_EVIDENCE until then. Do not invent a keep/discard. Do not rewrite an old script to make a test look successful.
8. `python3 tools/complete.py PATH`. Expect INCOMPLETE_MEDIA until VO+cards exist. A junk master.mp4 is not a master. Do not treat markdown, a named export path, a video ID, or a pending experiment as COMPLETE.
9. Human-edit `publish.md` description + approve pin comment (`docs/human_session.md` step 7). Tags already trimmed (Run 117). Do not upload.
10. Do **not** add another wrapper CLI. Do **not** map doctor.py. Do **not** scaffold Q2 yet. Do **not** add another operator/agent page that only restates this list. Do **not** re-implement `selected_vo_drop` in a second module. Do **not** add a TTS wrapper under tools/.
11. Do **not** make apply_script or words.py idea-lock INFO a check() error or a status bump.
12. Do **not** map idea_lock.py / words.py / words_contract.py / placeholder_guard.py / prove_locks.py / idea_brief.py / idea_brief_contract.py / doctor.py.
13. Do **not** attempt YouTube OAuth or publishing without credentials or a real VO file.
14. Do **not** run `assemble.py --execute` until `timeline.py` prints ready_to_assemble=yes and `media_qa.py` prints gate PASS. The optional TTS ffmpeg one-liners on `docs/gate_machine.md` are not assemble execute.
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
