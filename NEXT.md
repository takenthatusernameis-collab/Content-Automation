# NEXT

Do these in order. Stop if a step needs a human decision that is not present.

1. **Highest value:** Q1 human handoff is complete. Work the existing packet `videos/002-stop-deciding-what-to-work-on-every-morning` rather than reopening scaffolding. Use the existing empty-script Target: hook 28 (20-35), payoff 60 (40-70), each of four beats 220 (140-220), CTA 50 (40-80), land ~1010. Off-repo writer follows `prompts/script_writer.md` Band landing and saves the result to Q1 `draft.md`. Then run `words.py Q1 --strict`, dry-run `apply_script.py Q1 --from Q1/draft.md`, and only after a clean dry-run use `apply_script.py ... --write --refresh`. Do not treat draft.md as script.md. Do not promote to ready_for_vo while duration WARN is present. After any high-risk GitHub write, run `python3 tools/prove_locks.py` first.
2. **Do not reset the handoff.** Q1 is already scaffolded, idea.md is locked, and Q1 is marked `used`. Do not add another wrapper CLI, idea_brief flag, reconstruct path, Band-landing CLI, or second draft template merely because the packet is not yet complete.
3. Do not fabricate spoken WORDS, VO files, cards, exports, or publishing credentials. Do not attempt YouTube OAuth, TTS, ffmpeg, or publishing without the required real inputs.
4. Do not map idea_lock.py / words.py / words_contract.py / placeholder_guard.py / prove_locks.py / idea_brief.py / idea_brief_contract.py / doctor.py.
5. Do not run apply_script --write against `videos/sample-001-*`.
6. Do not retry HTTPS clone after one failure.
7. Do not have new_packet or idea_brief write idea.md.
8. Do not make words.py --strict fail on idea-lock INFO alone.
9. Do not strip the empty-script Target column from docs/human_session.md step 3.
10. Do not strip the Target comment from hint.py write-script/expand-script commands.
