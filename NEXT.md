# NEXT

Do these in order. Stop if a step needs a human decision that is not present.

1. **Highest value:** Keep foundation closed. Do not add ffmpeg assembly, TTS, stock, or YouTube OAuth. Prefer a packet-local `render.md` checklist that only lists whether named outputs from `docs/format.md` exist on disk — or stop and wait for a human VO / card file. Do not invent those files.
2. Do **not** rewrite `tools/asset_brief.py`, `tools/caption_brief.py`, `tools/publish_brief.py`, `tools/research_brief.py`, `tools/qa_checklist.py`, `tools/new_idea.py`, `tools/title_thumb_brief.py`, `docs/channel.md`, or `docs/format.md` unless they are wrong.
3. Do **not** attempt YouTube OAuth, TTS vendors, ffmpeg assembly, or publishing unless credentials or a real VO file appear in-repo docs as available.
4. Do **not** produce a “real” video packet intended for upload; still no VO or card binaries on disk.
5. Do **not** `--force` overwrite `videos/sample-001-*` titles or thumbnail.
6. Do **not** scrape the web into `research.md` and treat the result as verified.
7. Do **not** revert the `titles_from` one-line parser (`[ \\t]+` after `N.`); empty template `1.` lines must stay untitled.
8. Do **not** auto-`--force` titles, publish.md, captions.md, or assets.md during scaffold; empty-only is the contract.
9. Do **not** call Whisper or write a fake `captions.srt` from estimated times.
10. Do **not** call the YouTube API from `publish_brief.py`.
11. Do **not** download stock or commit card PNGs to make `assets.md` look ready.
12. Do **not** write an ffmpeg recipe or concat list. Named paths in `docs/format.md` are enough until a selected take exists.
