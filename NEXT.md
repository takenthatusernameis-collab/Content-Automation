# NEXT

Do these in order. Stop if a step needs a human decision that is not present.

1. **Highest value:** A human runs `python3 tools/queue_status.py` then follows `docs/human_session.md` on Q1 `Stop deciding what to work on every morning` (predicted folder `videos/002-stop-deciding-what-to-work-on-every-morning`). After a mark-needed folder exists, run `python3 tools/idea_brief.py PATH --block` and paste the full idea.md body (topic, viewer, problem, mechanism, why now, related). Then `--check`. Then `python3 tools/expand_prompt.py PATH` / save PATH/draft.md / `python3 tools/words.py PATH` (band + idea-lock INFO; INFO is not --strict FAIL) / apply dry-run (idea-lock INFO is not BLOCKED) / `--write --refresh` on the non-fixture packet only / `set_status.py PATH --to ready_for_vo` dry-run then `--write` only if WORDS are in band. Do not auto-scaffold. Do not auto-write idea.md. After a GitHub write of a high-risk tool, run `python3 tools/prove_locks.py` first.
2. Do **not** spend this run aligning another markdown page to name idea_brief --block/--check.
3. Do **not** drop the Idea locks section from expand_prompt.py or revert refuse text to the new_packet reprint.
4. Do **not** make apply_script or words.py idea-lock INFO a check() error, a --strict FAIL, or a status bump.
5. Do **not** drop the words.py import of apply_script.idea_lock_notes.
6. Do **not** rewrite frozen printers unless they are wrong.
7. Do **not** attempt YouTube OAuth, TTS, ffmpeg assembly, or publishing without in-repo credentials or a real VO file.
8. Do **not** produce an upload packet; still no VO or card binaries on disk.
18. Do **not** run apply_script --write against sample-001.
19. Do **not** run set_status --write --to ready_for_vo against sample-001.
22. Do **not** retry HTTPS clone after one failure.
27. Do **not** have new_packet or idea_brief write idea.md.
30. Do **not** map doctor / expand_prompt / needed / idea_gate / operator_pin / idea_brief_contract / words.py / words_contract.py / placeholder_guard.py / prove_locks.py.
33. Do **not** add WAVE 4 or edit needed.py unless a new clone-less guess appears after WAVE 3 READY.
40. Do **not** treat draft.md as script.md.
50. Do **not** replace write_path_contract.py with a docstring-only file.
54. Do **not** treat words.py as a lock or as apply --write.
56. Do **not** make words.py --strict fail on hook length, thin headings, Grow, Cut, or idea-lock INFO alone.
57. Do **not** drop tools/words_contract.py or lower its words.py MIN_BYTES below 8000.
59. Do **not** drop tools/prove_locks.py.
60. Do **not** add another order wrapper around prove_locks.py.
69. Do **not** shrink idea_brief --block back to topic / problem / mechanism only.
70. Do **not** make --check FAIL on blank viewer / why now / related.
