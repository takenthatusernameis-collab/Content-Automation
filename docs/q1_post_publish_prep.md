# Q1 post-publish experiment prep

Created 2026-11-17T17:26:00Z (Run 1310). Advances post-publish readiness without credentials.

After the first private video id appears and the observation window is due:

1. Run `python3 tools/post_publish_path_ready.py` then `python3 tools/after_upload_steps.py`.
2. Collect feedback with the workflow `collect_feedback=true` (do not invent metrics).
3. For the first experiment on this packet (mechanism: written next-action default):
   - Prefer a single variable change such as `hook` or `example_density`.
   - Use `python3 tools/experiment_baseline_starter.py videos/002-stop-deciding-what-to-work-on-every-morning` to generate the skeleton.
   - Set a real numeric baseline from Studio analytics and a documented source. Do not invent.
   - Copy to `videos/002-stop-deciding-what-to-work-on-every-morning/experiment_baseline.json`.
4. After comparison, use `tools/experiment_decision_starter.py` and record keep/discard/retest only with a documented reason.

This note reduces the human/agent setup time for the first learning loop. Do not invent analytics or baselines.

See `docs/experiments.md` and `tools/experiment_loop.py` for the full contract.
