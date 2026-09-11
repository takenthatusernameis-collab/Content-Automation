# ROADMAP

Order is deliberate: understandability and reliability first, then efficiency, then autonomy.

## Next (assisted production)
31–51k. Queue through write_path apply dry-run locks — **done (Runs 027–063)**
51l. write_path_contract locks set_status CLI blocked ready_for_vo — **done (Run 064)**
51m. write_path_contract locks apply_script CLI --write fixture refuse — **done (Run 065)**

## Later (automation)
52. Human scaffolds Q1, pastes idea fields, and lands WORDS in band on a non-fixture packet
53. TTS narration path (optional; keep human VO compatible)
54. Caption timing from a real selected take (not 150 wpm estimates)
55. ffmpeg assembly for this one locked format after one packet has VO + cards
56. YouTube upload + metadata only after packet QA passes

## Not yet
- Auto-scaffolding the next queued topic without a human instruction
- Marking a queue row used without a matching videos/ folder
- Auto-writing idea.md from new_packet.py or idea_brief.py
- Adding WAVE 4 without a new post-WAVE-3 guess
- ffmpeg / TTS / YouTube OAuth / Whisper / stock / shorts
- Weakening write_path_contract CLI locks (missing --from, dry-run draft.md, set_status blocked ready_for_vo, apply --write fixture)
