# NEXT

Do these in order. Stop if a step needs a human decision that is not present.

1. **Highest value:** A human runs `python3 tools/queue_status.py` then follows `docs/human_session.md` on Q1 `Stop deciding what to work on every morning` (predicted folder `videos/002-stop-deciding-what-to-work-on-every-morning`). After a mark-needed folder exists, run `python3 tools/idea_brief.py PATH --block` and paste the full idea.md body (topic, viewer, problem, mechanism, why now, related). Then `--check`. `--check` still gates only topic / problem / mechanism. Then `python3 tools/expand_prompt.py PATH` (Idea locks are now in stdout) / save PATH/draft.md / `python3 tools/words.py PATH` / apply dry-run / `--write --refresh` on the non-fixture packet only / `set_status.py PATH --to ready_for_vo` dry-run then `--write` only if WORDS are in band. Do not auto-scaffold. Do not auto-write idea.md. After a GitHub write of a high-risk tool, run `python3 tools/prove_locks.py` first.
2. Do **not** spend this run aligning another markdown page to name idea_brief --block/--check. Runs 082–088 already aligned hint, next_action, queue_status, next_topic, human_session, agent_session, README, and production_rules. See FAILURES.md watch.
3. Do **not** drop the Idea locks section from expand_prompt.py or revert refuse text to the new_packet reprint.
4. Do **not** rewrite frozen printers unless they are wrong.
5. Do **not** turn default duration WARN into FAIL.
6. Do **not** attempt YouTube OAuth, TTS, ffmpeg assembly, or publishing without in-repo credentials or a real VO file.
7. Do **not** produce an upload packet; still no VO or card binaries on disk.
8. Do **not** `--force` overwrite sample-001 titles, thumbnail, or script WORDS.
18. Do **not** run apply_script --write against sample-001.
19. Do **not** run set_status --write --to ready_for_vo against sample-001.
22. Do **not** retry HTTPS clone after one failure.
27. Do **not** have new_packet or idea_brief write idea.md.
30. Do **not** map doctor / expand_prompt / needed / idea_gate / operator_pin / idea_brief_contract / words.py / words_contract.py / placeholder_guard.py / prove_locks.py.
33. Do **not** add WAVE 4 or edit needed.py unless a new clone-less guess appears after WAVE 3 READY.
40. Do **not** treat draft.md as script.md.
42-48. Do **not** drop write_path_contract subprocesses for missing --from, existing-draft dry-run, blocked set_status, fixture apply --write, --refresh without --write, non-fixture --write, or --write --refresh.
49. Do **not** drop the in-band set_status ready_for_vo dry-run / --write lock (Run 067).
50. Do **not** replace write_path_contract.py with a docstring-only file.
51. Do **not** drop tools/contract_shape.py or lower write_path_contract MIN_BYTES below 8000.
52. Do **not** shrink contract_shape.py back to a write_path_contract-only witness; keep apply_script and set_status size+marker checks.
53. Do **not** drop tools/verify_write_path.py or treat it as a replacement for contract_shape.py / write_path_contract.py.
54. Do **not** treat words.py as a lock or as apply --write.
55. Do **not** treat words.py Delta, Hook Delta, Beats, Thin, Grow, or Cut as a request to invent filler statistics.
56. Do **not** make words.py --strict fail on hook length, thin headings, Grow, or Cut alone.
57. Do **not** drop tools/words_contract.py or lower its words.py MIN_BYTES below 8000.
58. Do **not** drop tools/placeholder_guard.py.
59. Do **not** drop tools/prove_locks.py or treat it as a substitute for the three files it runs.
60. Do **not** add another order wrapper around prove_locks.py.
61. Do **not** drop the prove_locks.py check from placeholder_guard.py or lower that floor below 800 bytes.
62. Do **not** strip idea_brief or words.py / draft.md lines from hint.py.
63. Do **not** revert next_action fill-idea Why to "Paste the new_packet reprint before expand_prompt."
64. Do **not** strip idea_brief --block / paste / --check from queue_status or next_topic.
65-68. Do **not** strip idea_brief --block / paste / --check from human_session, agent_session WAVE 3, README Human session, or production_rules handoff.
69. Do **not** shrink idea_brief --block back to topic / problem / mechanism only.
70. Do **not** make --check FAIL on blank viewer / why now / related.
