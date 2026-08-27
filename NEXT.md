# NEXT

Do these in order. Stop if a step needs a human decision that is not present.

1. **Highest value:** Add `tools/title_thumb_brief.py` that reads a packet’s idea + promise and writes 5 title options + a 5-word thumbnail line that already pass `validate_packet.py` field rules. Keep copy heuristic; no API.
2. Optionally add a `validate_packet.py` mode that treats empty WORDS as `draft-incomplete` instead of FAIL, so idea-only packets are first-class.
3. Do **not** rewrite `tools/new_idea.py` or `docs/channel.md` unless they are wrong.
4. Do **not** attempt YouTube OAuth, TTS vendors, or publishing unless credentials appear in-repo docs as available.
5. Do **not** produce a “real” video packet intended for upload; still no VO or assets path.
