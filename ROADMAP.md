# ROADMAP

Order is deliberate: understandability and reliability first, then efficiency, then autonomy.

## Next (assisted production)
31–49. Queue, contracts, reconstruct waves, operator page, Q1 pin, idea reprint — **done (Runs 027–045)**
50. expand_prompt refuses blank / template-default idea.md mechanism — **done (Run 046)**
51. next_action/hint `fill-idea` before expand while mechanism is blank — **done (Run 047)**
51b. idea_gate_contract locks fill-idea + blank-mechanism cases — **done (Run 048)**
51c. operator_pin_contract locks human_session Q1 title/path/one_line vs topic_queue — **done (Run 049)**

## Later (automation)
52. Human scaffolds Q1, pastes idea fields, and lands WORDS in band on a non-fixture packet
53. TTS narration path (optional; keep human VO compatible)
54. Caption timing from a real selected take (not 150 wpm estimates)
55. ffmpeg assembly for this one locked format after one packet has VO + cards
56. YouTube upload + metadata only after packet QA passes

## Not yet
- Auto-scaffolding the next queued topic without a human instruction
- Marking a queue row used without a matching videos/ folder
- Auto-marking the queue from new_packet.py
- Auto-writing idea.md from new_packet.py
- Turning default queue_status into a failing command (keep `--strict` opt-in)
- Mapping needed.py / doctor.py / expand_prompt.py / idea_gate_contract.py / operator_pin_contract.py onto a contract
- Making needed.py --missing, --bootstrap, or --plan exit non-zero
- Treating --bootstrap or --plan as a sixth contract
- Growing BOOTSTRAP or WAVE 2 / WAVE 3 into a full-repo dump
- Treating WAVE 3 as permission to auto-scaffold
- Adding WAVE 4 without a new post-WAVE-3 guess
- Extending needed.py after the reconstruct-loop flag unless a new guess is observed
- Expanding while idea.md still uses the scaffold template-default or blank mechanism
- Recommending expand_prompt while idea.md mechanism is blank
- ffmpeg / TTS / YouTube OAuth / Whisper / stock / shorts
- Treating which_contract --run SKIP as a contract PASS
- Treating idea_gate_contract or operator_pin_contract PASS as a real Q1 packet
