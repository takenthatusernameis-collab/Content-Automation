# NEXT

Do these in order. Stop if a step needs a human decision that is not present.

1. **Highest value:** Add a caption/subtitle intake stub (`captions.md` or SRT placeholder from script beat titles) — no Whisper, no TTS. Or, if a human VO file convention is wanted first, write `docs/narration.md` path rules only. Do not start YouTube OAuth.
2. Do **not** rewrite `tools/publish_brief.py`, `tools/research_brief.py`, `tools/qa_checklist.py`, `tools/new_idea.py`, `tools/title_thumb_brief.py`, or `docs/channel.md` unless they are wrong.
3. Do **not** attempt YouTube OAuth, TTS vendors, ffmpeg assembly, or publishing unless credentials or a real VO file appear in-repo docs as available.
4. Do **not** produce a “real” video packet intended for upload; still no VO or assets path.
5. Do **not** `--force` overwrite `videos/sample-001-*` titles or thumbnail.
6. Do **not** scrape the web into `research.md` and treat the result as verified.
7. Do **not** revert the `titles_from` one-line parser (`[ \\t]+` after `N.`); empty template `1.` lines must stay untitled.
8. Do **not** auto-`--force` titles or publish.md during scaffold; empty-only is the contract.
9. Do **not** call the YouTube API from `publish_brief.py`.
