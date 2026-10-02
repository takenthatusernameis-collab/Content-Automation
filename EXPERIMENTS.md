# EXPERIMENTS

No channel experiments yet (zero published videos).

`tools/experiment_loop.py` is the fail-closed ledger (Run 220). Until a packet has a provider_video_id and real metrics, the gate is HOLD_UNPUBLISHED or HOLD_NO_EVIDENCE. Do not invent a keep/discard.

Run 273: a packet may include `experiment_baseline.json`. Invalid or invented sources stay `COMPARE_BLOCKED_NO_BASELINE`. Do not write a baseline for Q1 until a real prior observation exists. Rejected sources: invented, assumed, placeholder, guess. Allowed `change` values are the list in `experiment_loop.py`.

Run 274: when collected rows contain exactly one numeric value for `primary_metric`, action is `COMPARED` and `comparison` holds observed, baseline, delta, and direction. Decision stays `pending`. `result` stays null. A missing or conflicting metric is `COMPARE_BLOCKED_METRIC`. Do not treat `COMPARED` as keep/discard.

```json
{
  "hypothesis": "A narrower hook holds average view percentage",
  "change": "hook",
  "primary_metric": "averageViewPercentage",
  "baseline": 28.0,
  "source": "prior private upload analytics export, with date"
}
```

Template for later:

```
ID:
Hypothesis:
Test:
Evidence:
Result:
Lesson:
Next:
```
