# Experiments

One row/block per test. Do not invent results before the observation window ends.

Ledger tool: `tools/experiment_loop.py` (PLAN_BUILT). Missing provider_video_id is HOLD_UNPUBLISHED. Empty metrics are HOLD_NO_EVIDENCE. A pending record is not a keep/discard. A numeric delta is COMPARED, not a decision. `experiment_decision.json` may record keep, discard, or retest only after that comparison, with a reason and a documented source. Do not invent that file.

## JSON baseline template

A ready-to-copy template lives at `docs/experiment_baseline.template.json`. Copy it to `videos/<packet>/experiment_baseline.json` only after a real documented observation exists. Fill hypothesis, choose one allowed change, set a numeric baseline, and provide a non-invented source. The ledger rejects placeholder or invented sources. Do not invent metrics.

For a grounded starting skeleton, run `python3 tools/experiment_baseline_starter.py videos/<packet>`. It prints a contract-compliant JSON (allowed changes, null baseline, source warning) based on idea.md. Edit the baseline and source before use. Do not invent metrics.

## Template
- ID:
- Video / packet:
- Date / observation window:
- Hypothesis:
- Change:
- Primary metric:
- Guardrails:
- Baseline:
- Result:
- Uncertainty / caveats:
- Decision: keep / discard / retest
- Next:
