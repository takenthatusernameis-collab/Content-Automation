# NEXT

Do these in order. Stop if a step needs a human decision that is not present.

1. **Highest value:** Place a Selected VO take for `videos/002-stop-deciding-what-to-work-on-every-morning` at `videos/002-stop-deciding-what-to-work-on-every-morning/vo/002-stop-deciding-what-to-work-on-every-morning-take-selected.wav` (or .flac) on the machine that runs gates. Generated audio is an authorized labeled fallback (`vo_origin.md` kind=generated). Repo-root `vo/` is ignored. Do not invent a wav in git. Do not `git add -f` the take. Inspect with `python3 tools/narration_adapter.py PATH`.
2. After a real selected take exists on disk: `python3 tools/vo_session.py PATH --force` then `python3 tools/set_status.py PATH --to ready_for_edit` dry-run; `--write` only if Selected VO present and gate still PASS. Keep `vo_origin.md` kind honest.
3. On the same machine: `python3 tools/card_generator.py PATH --write-manifest`. Requires Pillow. Writes gitignored 1920x1080 PNGs under `cards/`. Do not commit binaries. `--mark-ready` only after inspect-only reports all yes.
4. `python3 tools/timeline.py PATH --write`. Then `python3 tools/media_qa.py PATH`. Expect vo_peak/vo_rms/vo_silence/vo_clip rows. export_decodable stays FAIL until a real ftyp master exists; that is expected. Confirm ready_to_assemble and media_qa gate before any ffmpeg work. Then `python3 tools/assemble.py PATH` (expect HOLD_MEDIA until VO+cards exist). `--execute` only if gate is READY_TO_ENCODE.
5. After a local master exists with a real ftyp box: `python3 tools/youtube_upload.py PATH`. Expect `YOUTUBE_AUTH_REQUIRED` until OAuth env is present. A junk master.mp4 is HOLD_LOCAL, not READY. Do not pass secrets. Do not treat dry-run READY as an upload.
6. After upload_state.json contains a real provider_video_id: `python3 tools/youtube_feedback.py PATH`. Expect HOLD_UNPUBLISHED until then. Do not invent metrics. Do not call Analytics APIs from this tool.
7. After feedback metrics exist: `python3 tools/experiment_loop.py PATH`. Expect HOLD_NO_EVIDENCE until then. Do not invent a keep/discard. Do not rewrite an old script to make a test look successful.
8. `python3 tools/complete.py PATH`. Expect INCOMPLETE_MEDIA until VO+cards exist. A junk master.mp4 is not a master. Do not treat markdown, a named export path, a video ID, or a pending experiment as COMPLETE.
9. Human-edit `publish.md` description + approve pin comment (`docs/human_session.md` step 7). Tags already trimmed (Run 117). Do not upload.
10. Do **not** add another wrapper CLI. Do **not** map doctor.py. Do **not** scaffold Q2 yet. Do **not** add another operator/agent page that only restates this list. Do **not** re-implement `selected_vo_drop` in a second module.
11. Do **not** make apply_script or words.py idea-lock INFO a check() error or a status bump.
12. Do **not** map idea_lock.py / words.py / words_contract.py / placeholder_guard.py / prove_locks.py / idea_brief.py / idea_brief_contract.py / doctor.py.
13. Do **not** attempt YouTube OAuth or publishing without credentials or a real VO file.
14. Do **not** run ffmpeg or `assemble.py --execute` until `timeline.py` prints ready_to_assemble=yes and `media_qa.py` prints gate PASS.
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
