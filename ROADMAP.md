# ROADMAP

Order is deliberate: understandability and reliability first, then efficiency, then autonomy.

## Next (assisted production)
31. Working topic queue + read-only next-topic printer — **done (Run 027)**
32. Predicted packet path + evidence-gated queue closer — **done (Run 028)**
33. Shared queue lib + scaffold reprints mark_topic dry-run — **done (Run 029)**
34. Read-only queue vs folder board — **done (Run 030)**
35. Queue board `--strict` + packet status column — **done (Run 031)**
36. Queue board contract selftest — **done (Run 032)**

Earlier items 1-30 remain done as recorded in prior commits.

## Later (automation)
37. TTS narration path (optional; keep human VO compatible)
38. Caption timing from a real selected take (not 150 wpm estimates)
39. ffmpeg assembly for this one locked format after one packet has VO + cards
40. YouTube upload + metadata only after packet QA passes

## Not yet
- Auto-scaffolding the next queued topic without a human instruction
- Marking a queue row used without a matching videos/ folder
- Auto-marking the queue from new_packet.py
- Turning default queue_status into a failing command (keep `--strict` opt-in)
- ffmpeg / TTS / YouTube OAuth / Whisper / stock / shorts
