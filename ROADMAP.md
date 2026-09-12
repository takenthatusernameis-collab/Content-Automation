# ROADMAP

## Next (assisted production)
31–51n. Queue through write_path apply locks — **done (Runs 027–066; body restored Run 067)**
51o–51aj. Write-path / words / prove_locks / printer + page alignment — **done (Runs 067–088)**
51ak. idea_brief --block pastes the full idea.md template — **done (Run 089)**

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
- Making --check FAIL on viewer / why now / related
- Shrinking --block back to three fields
- Another primary run whose only change is naming idea_brief on one more page
- Weakening write_path_contract CLI locks
- Replacing write_path_contract.py with a docstring-only file
- Dropping tools/contract_shape.py / verify_write_path.py / placeholder_guard.py / prove_locks.py
- Treating words.py as a lock or as apply --write
- Mapping words.py, words_contract.py, placeholder_guard.py, or prove_locks.py in needed.py
- Adding another order wrapper around prove_locks.py
- Stripping idea_brief lines from hint / next_action / queue_status / next_topic / human_session / agent_session / README / production_rules
