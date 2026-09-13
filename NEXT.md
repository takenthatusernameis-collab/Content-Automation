# NEXT

Do these in order. Stop if a step needs a human decision that is not present.

1. **Highest value:** On the live packet `videos/002-stop-deciding-what-to-work-on-every-morning` run `python3 tools/words.py PATH`. If Result is IN BAND, run `python3 tools/apply_script.py PATH --from PATH/draft.md` then `--write --refresh`. Then `python3 tools/validate_packet.py PATH`. Promote with `set_status --to ready_for_vo` only if WORDS stay in band and there is no duration WARN. Do not treat draft.md as script.md until apply --write. Do not invent VO.
2. If words.py says BELOW or ABOVE, edit `PATH/draft.md` using Grow/Cut/Hook Delta. Do not rewrite `prompts/script_writer.md` unless the official count misses 900-1500 after a real edit pass.
3. After apply, fill titles.md / thumbnail.md with `title_thumb_brief.py --dry-run` as the next human lock. Do not upload.
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
