# ROADMAP

Order is deliberate: understandability and reliability first, then efficiency, then autonomy.

## Next (assisted production)
31. Working topic queue + read-only next-topic printer — **done (Run 027)**
32. Predicted packet path + evidence-gated queue closer — **done (Run 028)**
33. Shared queue lib + scaffold reprints mark_topic dry-run — **done (Run 029)**

Earlier items 1-30 remain done as recorded in prior commits.

## Later (automation)
34. TTS narration path (optional; keep human VO compatible)
35. Caption timing from a real selected take (not 150 wpm estimates)
36. ffmpeg assembly for this one locked format after one packet has VO + cards
37. YouTube upload + metadata only after packet QA passes

## Not yet
- Auto-scaffolding the next queued topic without a human instruction
- Marking a queue row used without a matching videos/ folder
- Auto-marking the queue from new_packet.py
- ffmpeg / TTS / YouTube OAuth / Whisper / stock / shorts
