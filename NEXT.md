# NEXT

Do these in order. Stop if a step needs a human decision that is not present.

1. **Highest value:** On live packet `videos/002-stop-deciding-what-to-work-on-every-morning` run `python3 tools/validate_packet.py PATH`. Then `python3 tools/set_status.py PATH --to ready_for_vo` (dry-run). Pass `--write` only if Result is OK and there is no duration WARN. Do not invent VO.
2. Fill titles.md / thumbnail.md with `python3 tools/title_thumb_brief.py PATH --dry-run` as the next human lock. Do not upload.
3. Re-run `python3 tools/words.py PATH` on a machine with a full checkout if the 952 count needs a second official pass (this run used the same spoken-word rules as words.py against the live draft).
4. Do **not** add another wrapper CLI. Do **not** map doctor.py. Do **not** add another needed.py reconstruct path unless a READY lie is proven. Do **not** add a Band-landing reprint CLI. Do **not** scaffold Q2 yet.
5. Do **not** make apply_script or words.py idea-lock INFO a check() error or a status bump.
6. Do **not** map idea_lock.py / words.py / words_contract.py / placeholder_guard.py / prove_locks.py / idea_brief.py / idea_brief_contract.py / doctor.py.
7. Do **not** attempt YouTube OAuth, TTS, ffmpeg, or publishing without credentials or a real VO file.
18. Do **not** run apply_script --write against sample-001.
22. Do **not** retry HTTPS clone after one failure.
27. Do **not** have new_packet or idea_brief write idea.md.
40. Do **not** treat draft.md as script.md.
56. Do **not** make words.py --strict fail on idea-lock INFO alone.
64. Do **not** strip the empty-script Target column from docs/human_session.md step 3.
65. Do **not** strip the Target comment from hint.py write-script/expand-script commands.
