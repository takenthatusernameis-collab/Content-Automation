# OPERATOR HOLD

> Escalation policy: `docs/operator_escalation.md`.

The 24-hour selected-VO request dated 2026-09-18 elapsed at 2026-09-19T00:00:00Z.
Generated narration is now the authorized fallback. It must stay labeled generated.

Q1 still has no git-visible Selected VO file. Audio remains gitignored. Do not `git add -f` a take. Do not bump status past `ready_for_vo` unless a packet-relative take exists on the machine running the gates.

Do not keep aligning documentation, adding guards, rewriting prompts, creating wrapper CLIs, or scaffolding Q2 unless a genuine regression blocks the next action.

A human take at the packet-relative DROP path may replace the generated fallback. Update `vo_origin.md` to `kind: human` only when that file is real.

Run 247 left the already-verified generated wav and seven cards in the operator chat as `q1-handoff-verified.zip`. Copy those files onto the packet paths in `HANDOFF.md`. That zip is not Selected VO until the copy exists on the gate machine.
