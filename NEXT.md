# NEXT

Do these in order. Stop if a step needs a human decision that is not present.

1. **Highest value:** Human locks Primary title on `videos/002-stop-deciding-what-to-work-on-every-morning` (heuristic Primary is already filled and passes validate). Then record or generate a **selected VO take** per `docs/narration.md` and place it at the named path. Do not invent a wav in-repo.
2. After a real selected take exists: `python3 tools/set_status.py PATH --to ready_for_edit` dry-run; `--write` only if Selected VO present and gate still PASS.
3. Do **not** add another wrapper CLI. Do **not** map doctor.py. Do **not** add another needed.py reconstruct path unless a READY lie is proven. Do **not** add a Band-landing reprint CLI. Do **not** scaffold Q2 yet.
4. Do **not** make apply_script or words.py idea-lock INFO a check() error or a status bump.
5. Do **not** map idea_lock.py / words.py / words_contract.py / placeholder_guard.py / prove_locks.py / idea_brief.py / idea_brief_contract.py / doctor.py.
6. Do **not** attempt YouTube OAuth, TTS, ffmpeg, or publishing without credentials or a real VO file.
18. Do **not** run apply_script --write against sample-001.
22. Do **not** retry HTTPS clone after one failure.
27. Do **not** have new_packet or idea_brief write idea.md.
40. Do **not** treat draft.md as script.md.
56. Do **not** make words.py --strict fail on idea-lock INFO alone.
64. Do **not** strip the empty-script Target column from docs/human_session.md step 3.
65. Do **not** strip the Target comment from hint.py write-script/expand-script commands.
