# NEXT

Do these in order. Stop if a step needs a human decision that is not present.

1. **Highest value:** Wire `tools/new_idea.py` and/or `tools/new_packet.py` to call `qa_checklist.py` and `research_brief.py` after scaffold so every new folder starts with a generated checklist and research stub. Keep generate-on-scaffold optional if a flag is cleaner than always-write.
2. Do **not** rewrite `tools/research_brief.py`, `tools/new_idea.py`, `tools/title_thumb_brief.py`, `tools/validate_packet.py`, `tools/qa_checklist.py`, or `docs/channel.md` unless they are wrong.
3. Do **not** attempt YouTube OAuth, TTS vendors, ffmpeg assembly, or publishing unless credentials or a real VO file appear in-repo docs as available.
4. Do **not** produce a “real” video packet intended for upload; still no VO or assets path.
5. Do **not** `--force` overwrite `videos/sample-001-*` titles or thumbnail.
6. Do **not** scrape the web into `research.md` and treat the result as verified.
