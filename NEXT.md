# NEXT

Do these in order. Stop if a step needs a human decision that is not present.

1. **Highest value:** Add a `validate_packet.py --draft` (or `--incomplete`) mode that treats empty spoken WORDS as `draft-incomplete` instead of FAIL, while still failing missing files, bad status, beat-count, and empty packet identity fields. Keep the default command a publish/completeness gate.
2. Optionally add `docs/editor.md` with track naming and export conventions for a face-free explainer (no ffmpeg profile yet).
3. Do **not** rewrite `tools/new_idea.py`, `tools/title_thumb_brief.py`, or `docs/channel.md` unless they are wrong.
4. Do **not** attempt YouTube OAuth, TTS vendors, or publishing unless credentials appear in-repo docs as available.
5. Do **not** produce a “real” video packet intended for upload; still no VO or assets path.
6. Do **not** `--force` overwrite `videos/sample-001-*` titles or thumbnail.
