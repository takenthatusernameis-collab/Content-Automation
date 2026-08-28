# NEXT

Do these in order. Stop if a step needs a human decision that is not present.

1. **Highest value:** Expand routing now has a beat budget, a paste pack, and a paste-back gate. Do not pad sample-001 to 900 words. Do not auto-write WORDS from expand.md or expand_prompt.py. Do not add ffmpeg assembly, TTS, stock, or YouTube OAuth. Wait for a human to produce expanded WORDS for a *new* non-fixture packet and apply them with `python3 tools/apply_script.py PATH --from FILE --write --refresh`, or for a selected VO / local card file on a packet whose WORDS already sit in band.
2. Do **not** rewrite `tools/apply_script.py`, `tools/expand_prompt.py`, `tools/expand_brief.py`, `tools/vo_session.py`, `tools/pipeline_status.py`, `tools/render_brief.py`, `tools/asset_brief.py`, `tools/caption_brief.py`, `tools/publish_brief.py`, `tools/research_brief.py`, `tools/qa_checklist.py`, `tools/new_idea.py`, `tools/title_thumb_brief.py`, or `docs/channel.md` unless they are wrong.
3. Do **not** turn default duration WARN into FAIL. That would break the sample fixture PASS contract.
4. Do **not** attempt YouTube OAuth, TTS vendors, ffmpeg assembly, or publishing unless credentials or a real VO file appear in-repo docs as available.
5. Do **not** produce a “real” video packet intended for upload; still no VO or card binaries on disk.
6. Do **not** `--force` overwrite `videos/sample-001-*` titles, thumbnail, or script WORDS.
7. Do **not** scrape the web into `research.md` and treat the result as verified.
8. Do **not** revert the `titles_from` one-line parser (`[ \\t]+` after `N.`); empty template `1.` lines must stay untitled.
9. Do **not** auto-`--force` titles, publish.md, captions.md, assets.md, render.md, vo_session.md, or expand.md during scaffold; empty-only is the contract.
10. Do **not** call Whisper or write a fake `captions.srt` from estimated times.
11. Do **not** call the YouTube API from `publish_brief.py`.
12. Do **not** download stock or commit card PNGs to make `assets.md` or `render.md` look ready.
13. Do **not** write an ffmpeg recipe or concat list. Named paths plus presence rows are enough until a selected take exists.
14. Do **not** have `pipeline_status.py` or `next_action.py` mutate `packet.md` status to clear drift.
15. Do **not** treat `vo_session.md` as recorded audio. Status `ready-to-record` is a reading card only.
16. Do **not** treat `expand.md` as a finished script. Status `short` is a budget only.
17. Do **not** treat `expand_prompt.py` stdout as a rewritten script. Do not write that stdout onto sample-001 `script.md`.
18. Do **not** run `apply_script.py --write` against `videos/sample-001-*`.
