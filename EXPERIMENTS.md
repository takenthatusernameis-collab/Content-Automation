# EXPERIMENTS

No channel experiments yet (zero published videos).

`tools/experiment_loop.py` is the fail-closed ledger (Run 220). Until a packet has a provider_video_id and real metrics, the gate is HOLD_UNPUBLISHED or HOLD_NO_EVIDENCE. Do not invent a keep/discard.

Run 273: a packet may include `experiment_baseline.json`. A valid file moves collected metrics from `COMPARE_BLOCKED_NO_BASELINE` to `COMPARE_READY`. Decision stays `pending`. Do not write a baseline for Q1 until a real prior observation exists. Rejected sources: invented, assumed, placeholder, guess. Allowed `change` values are the list in `experiment_loop.py`.

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
