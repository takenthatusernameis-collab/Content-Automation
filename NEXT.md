# NEXT

Do these in order. Stop if a step needs a human decision that is not present.

1. **Highest value:** A human runs `python3 tools/queue_status.py` then follows `docs/human_session.md` on Q1 `Stop deciding what to work on every morning` (predicted folder `videos/002-stop-deciding-what-to-work-on-every-morning`). After scaffold: idea_brief --block / paste / --check / expand off-repo / save PATH/draft.md / `python3 tools/words.py PATH` (read Result + Delta + Hook Delta + Beats + Thin; `--strict` if gating the total band) / apply dry-run / `--write --refresh` on the non-fixture packet only / `set_status.py PATH --to ready_for_vo` dry-run then `--write` only if WORDS are in band. Do not auto-scaffold. Do not auto-write idea.md. After editing apply_script or set_status, or after reconstructing write-path tools, run `python3 tools/verify_write_path.py` (shape then contract). The two-command form remains valid: `python3 tools/contract_shape.py` then `python3 tools/write_path_contract.py`.
2. Do **not** rewrite frozen printers unless they are wrong.
3. Do **not** turn default duration WARN into FAIL.
4. Do **not** attempt YouTube OAuth, TTS, ffmpeg assembly, or publishing without in-repo credentials or a real VO file.
5. Do **not** produce an upload packet; still no VO or card binaries on disk.
6. Do **not** `--force` overwrite sample-001 titles, thumbnail, or script WORDS.
18. Do **not** run apply_script --write against sample-001.
19. Do **not** run set_status --write --to ready_for_vo against sample-001.
22. Do **not** retry HTTPS clone after one failure.
27. Do **not** have new_packet or idea_brief write idea.md.
30. Do **not** map doctor / expand_prompt / needed / idea_gate / operator_pin / idea_brief_contract / words.py.
33. Do **not** add WAVE 4 or edit needed.py unless a new clone-less guess appears after WAVE 3 READY.
40. Do **not** treat draft.md as script.md.
42-48. Do **not** drop write_path_contract subprocesses for missing --from, existing-draft dry-run, blocked set_status, fixture apply --write, --refresh without --write, non-fixture --write, or --write --refresh.
49. Do **not** drop the in-band set_status ready_for_vo dry-run / --write lock (Run 067).
50. Do **not** replace write_path_contract.py with a docstring-only file.
51. Do **not** drop tools/contract_shape.py or lower write_path_contract MIN_BYTES below 8000.
52. Do **not** shrink contract_shape.py back to a write_path_contract-only witness; keep apply_script and set_status size+marker checks.
53. Do **not** drop tools/verify_write_path.py or treat it as a replacement for contract_shape.py / write_path_contract.py.
54. Do **not** treat words.py as a lock or as apply --write. It only prints the band, a Delta, a Hook Delta, Beats, Thin, and a Next line.
55. Do **not** treat words.py Delta, Hook Delta, Beats, or Thin as a request to invent filler statistics.
56. Do **not** make words.py --strict fail on hook length or thin headings alone.
