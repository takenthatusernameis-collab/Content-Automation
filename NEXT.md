# NEXT

Do these in order. Stop if a step needs a human decision that is not present.

1. **Highest value:** Add `tools/qa_checklist.py` that writes/updates `qa.md` from production rules + editor conventions (mechanical boxes a human still ticks: VO take, card readability, CTA assignment present). Do not invent scores.
2. Optionally add a `research.md` intake stub CLI (source list + “no unverifiable stats” reminder) bound to `docs/production_rules.md`.
3. Do **not** rewrite `tools/new_idea.py`, `tools/title_thumb_brief.py`, `tools/validate_packet.py`, or `docs/channel.md` unless they are wrong.
4. Do **not** attempt YouTube OAuth, TTS vendors, ffmpeg assembly, or publishing unless credentials or a real VO file appear in-repo docs as available.
5. Do **not** produce a “real” video packet intended for upload; still no VO or assets path.
6. Do **not** `--force` overwrite `videos/sample-001-*` titles or thumbnail.
