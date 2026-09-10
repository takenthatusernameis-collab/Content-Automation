# NEXT

Do these in order. Stop if a step needs a human decision that is not present.

1. **Highest value:** A human runs `python3 tools/queue_status.py` (or `next_topic.py`), then follows `docs/human_session.md` on that title: scaffold a *new* packet. After scaffold, `new_packet.py` already reprints the matching `mark_topic --id QN` dry-run line. Dry-run that, then `--write` only after the folder exists. Re-run `queue_status.py` to confirm the row is mark-needed then used. Expand off-repo, then `python3 tools/apply_script.py PATH --from FILE --write --refresh`. Only then, if WORDS sit in band, `python3 tools/set_status.py PATH --to ready_for_vo` (dry-run first). Do not pad sample-001 to 900 words. Do not auto-write WORDS. Do not auto-scaffold the queue. Do not auto-mark from new_packet. Do not add ffmpeg assembly, TTS, stock, or YouTube OAuth. Agents without a clone follow `docs/agent_session.md`. Start with `python3 tools/needed.py --bootstrap` then `--missing`. After a tool edit, run `python3 tools/needed.py THAT_FILE --missing` then `python3 tools/which_contract.py --after THAT_FILE` and the printed contract. After editing `which_contract.py`, run `python3 tools/router_contract.py`. To list reconstruct files, run `python3 tools/needed.py THAT_FILE`. Or wait for a selected VO / local card file on a packet already in band.
2. Do **not** rewrite `tools/doctor.py`, `tools/hint.py`, `tools/set_status.py`, `tools/apply_script.py`, `tools/expand_prompt.py`, `tools/expand_brief.py`, `tools/vo_session.py`, `tools/pipeline_status.py`, `tools/render_brief.py`, `tools/asset_brief.py`, `tools/caption_brief.py`, `tools/publish_brief.py`, `tools/research_brief.py`, `tools/qa_checklist.py`, `tools/new_idea.py`, `tools/title_thumb_brief.py`, `tools/selftest.py`, `tools/queue_status.py`, `tools/queue_contract.py`, `tools/write_path_contract.py`, `tools/scaffold_contract.py`, `tools/which_contract.py`, `tools/router_contract.py`, or `docs/channel.md` unless they are wrong.
3. Do **not** turn default duration WARN into FAIL.
4. Do **not** attempt YouTube OAuth, TTS vendors, ffmpeg assembly, or publishing unless credentials or a real VO file appear in-repo docs as available.
5. Do **not** produce a “real” video packet intended for upload; still no VO or card binaries on disk.
6. Do **not** `--force` overwrite `videos/sample-001-*` titles, thumbnail, or script WORDS.
7. Do **not** scrape the web into `research.md` and treat the result as verified.
8. Do **not** revert the `titles_from` one-line parser.
9. Do **not** auto-`--force` titles, publish.md, captions.md, assets.md, render.md, vo_session.md, or expand.md during scaffold.
10. Do **not** call Whisper or write a fake `captions.srt` from estimated times.
11. Do **not** call the YouTube API from `publish_brief.py`.
12. Do **not** download stock or commit card PNGs.
13. Do **not** write an ffmpeg recipe or concat list.
14. Do **not** have printers or contracts mutate `packet.md` or the queue.
15. Do **not** treat `vo_session.md` as recorded audio.
16. Do **not** treat `expand.md` as a finished script.
17. Do **not** treat `expand_prompt.py` stdout as a rewritten script.
18. Do **not** run `apply_script.py --write` against `videos/sample-001-*`.
19. Do **not** run `set_status.py --write --to ready_for_vo` against `videos/sample-001-*`.
20. Do **not** make `hint.py` or `doctor.py` print `--write` as the first command.
21. Do **not** replace `docs/human_session.md` with a wrapper around doctor. `needed.py` is the reconstruct file list, presence check, and first-fetch list. The named contracts stay the actual locks.
22. Do **not** retry HTTPS clone after one failure.
23. Do **not** treat fixture selftest runtime as unverified after Run 026 unless a later run sees SELFTEST FAIL.
24. Do **not** have `next_topic.py` or `queue_status.py` call `new_packet.py`.
25. Do **not** mark a queue row `used` until the matching `videos/` folder exists.
26. Do **not** have `mark_topic.py` create packets or mark sample-001 as used.
27. Do **not** have `new_packet.py` call `mark_topic.py --write`.
28. Do **not** make default `queue_status.py` exit non-zero.
29. Do **not** treat `which_contract.py --run --all` SKIP as a contract PASS.
30. Do **not** map `doctor.py`, `expand_prompt.py`, or `needed.py` onto a contract.
31. Do **not** make `needed.py --missing` or `needed.py --bootstrap` exit non-zero when files are absent.
32. Do **not** treat `--bootstrap` as a sixth contract or grow BOOTSTRAP into a full-repo dump.
