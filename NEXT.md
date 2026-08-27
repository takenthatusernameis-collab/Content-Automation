# NEXT

Do these in order. Stop if a step needs a human decision that is not present.

1. **Highest value:** Add `tools/publish_brief.py` that writes a `publish.md` stub (description, tags, first comment) from packet idea + primary title. Empty-file / `--force` guard. No YouTube API. Do not invent a second title generator.
2. Do **not** rewrite `tools/research_brief.py`, `tools/qa_checklist.py`, `tools/new_idea.py`, `tools/title_thumb_brief.py`, or `docs/channel.md` unless they are wrong.
3. Do **not** attempt YouTube OAuth, TTS vendors, ffmpeg assembly, or publishing unless credentials or a real VO file appear in-repo docs as available.
4. Do **not** produce a “real” video packet intended for upload; still no VO or assets path.
5. Do **not** `--force` overwrite `videos/sample-001-*` titles or thumbnail.
6. Do **not** scrape the web into `research.md` and treat the result as verified.
7. Do **not** revert the `titles_from` one-line parser (`[ \\t]+` after `N.`); empty template `1.` lines must stay untitled.
8. Do **not** auto-`--force` titles during scaffold; empty-only is the contract.
