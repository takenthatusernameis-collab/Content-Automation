# ROADMAP

## Next (assisted production)
31–51n. Queue through write_path apply locks — **done (Runs 027–066; body restored Run 067)**
51o. write_path_contract locks in-band set_status ready_for_vo — **done (Run 067)**
51p. Separate source-shape lock for write_path_contract.py — **done (Run 068)**
51q. contract_shape trio (apply_script + set_status) — **done (Run 069)**
51r. One-command verify_write_path order lock — **done (Run 070)**
51s. Read-only words.py band check on draft.md — **done (Run 071)**

## Later (automation)
52. Human scaffolds Q1, pastes idea fields, and lands WORDS in band on a non-fixture packet
53. TTS narration path (optional)
54. Caption timing from a real selected take
55. ffmpeg assembly after one packet has VO + cards
56. YouTube upload after packet QA passes

## Not yet
- Auto-scaffolding Q1
- Auto-writing idea.md
- WAVE 4
- Weakening write_path_contract CLI locks
- Replacing write_path_contract.py with a docstring-only file
- Dropping tools/contract_shape.py
- Dropping tools/verify_write_path.py or using it as a substitute for the two files it runs
- Treating words.py as a lock or as apply --write
- Mapping words.py in needed.py
