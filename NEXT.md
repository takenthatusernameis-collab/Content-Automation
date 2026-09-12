# NEXT

Do these in order. Stop if a step needs a human decision that is not present.

1. **Highest value:** A human runs `python3 tools/queue_status.py` then follows `docs/human_session.md` on Q1 `Stop deciding what to work on every morning` (predicted folder `videos/002-stop-deciding-what-to-work-on-every-morning`). After a mark-needed folder exists, `python3 tools/queue_status.py` should print idea_brief --block / paste / --check under that folder. `python3 tools/next_topic.py` should print the same idea_brief lines after the predicted path. The start section of `docs/human_session.md` should name those same lines so the operator does not treat the board as mark_topic-only. The WAVE 3 board paragraph of `docs/agent_session.md` should name those same lines so a clone-less agent does not invent a mark_topic-only next step. After scaffold: `python3 tools/hint.py PATH` should print idea_brief --block / --check then later words.py + PATH/draft.md apply lines. `python3 tools/next_action.py PATH` and `python3 tools/doctor.py PATH` Why should name idea_brief --block / paste / --check, not a new_packet reprint from memory. idea_brief --block / paste / --check / expand off-repo / save PATH/draft.md / `python3 tools/words.py PATH` (read Result + Delta + Hook Delta + Beats + Thin + Grow or Cut; `--strict` if gating the total band) / apply dry-run / `--write --refresh` on the non-fixture packet only / `set_status.py PATH --to ready_for_vo` dry-run then `--write` only if WORDS are in band. Do not auto-scaffold. Do not auto-write idea.md. After a GitHub write of a high-risk tool, run `python3 tools/prove_locks.py` first. The three inner commands remain valid as fallback. After reconstructing write-path tools without a GitHub write in the same step, `python3 tools/verify_write_path.py` remains valid. After reconstructing words.py without a GitHub write in the same step, `python3 tools/words_contract.py` remains valid.
2. Do **not** rewrite frozen printers unless they are wrong. hint.py fill-idea / write-script / expand-script were aligned in Run 082. next_action fill-idea Why was aligned in Run 083. queue_status mark-needed follow-up and next_topic after-folder lines were aligned in Run 084. human_session start text was aligned in Run 085. agent_session WAVE 3 board text was aligned in Run 086. Do not revert those alignments.
3. Do **not** turn default duration WARN into FAIL.
4. Do **not** attempt YouTube OAuth, TTS, ffmpeg assembly, or publishing without in-repo credentials or a real VO file.
5. Do **not** produce an upload packet; still no VO or card binaries on disk.
6. Do **not** `--force` overwrite sample-001 titles, thumbnail, or script WORDS.
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
54. Do **not** treat words.py as a lock or as apply --write. It only prints the band, a Delta, a Hook Delta, Beats, Thin, Grow, Cut, and a Next line.
55. Do **not** treat words.py Delta, Hook Delta, Beats, Thin, Grow, or Cut as a request to invent filler statistics.
56. Do **not** make words.py --strict fail on hook length, thin headings, Grow, or Cut alone.
57. Do **not** drop tools/words_contract.py or lower its words.py MIN_BYTES below 8000. It is not a substitute for words.py and is not a reconstruct wave.
58. Do **not** drop tools/placeholder_guard.py. It is not a substitute for words_contract.py, contract_shape.py, or verify_write_path.py. PASS is not apply --write. Keep the prove_locks.py sibling check added in Run 081.
59. Do **not** drop tools/prove_locks.py or treat it as a substitute for placeholder_guard.py, words_contract.py, or verify_write_path.py. PASS is not apply --write.
60. Do **not** add another order wrapper around prove_locks.py. Do not leave NEXT_RUN_PROMPT listing only the inner three commands as the primary post-write action.
61. Do **not** drop the prove_locks.py check from placeholder_guard.py or lower that floor below 800 bytes.
62. Do **not** strip idea_brief or words.py / draft.md lines from hint.py.
63. Do **not** revert next_action fill-idea Why to "Paste the new_packet reprint before expand_prompt."
64. Do **not** strip idea_brief --block / paste / --check from queue_status mark-needed follow-up or next_topic after-folder lines.
65. Do **not** strip idea_brief --block / paste / --check from the start-of-session section of docs/human_session.md.
66. Do **not** strip idea_brief --block / paste / --check from the WAVE 3 board paragraph of docs/agent_session.md.
