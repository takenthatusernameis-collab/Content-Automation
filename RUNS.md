## 2026-10-02T08:18:05Z — Run 270

- **Objective:** Prove the Run 269 production workflow instead of restating the OAuth hold.
- **Inspected:** STATE, NEXT, HANDOFF, RUNS, `youtube-production.yml`, `materialize_q1_release.py`.
- **Action taken:** Dispatched workflow_dispatch with execute=false. Run 36982959831 failed because materialize aborted when the expected truncated r249 master was present. Changed the guard to ignore that known sha, refuse an unexpected r249 master sha, and still refuse installing the banned sha as `export/master.mp4`. Pushed `9416aae2c482ca08fd55642e0fff94568482ee51` and redispatched.
- **Result:** Run 36983196381 succeeded. Materialize logged `ignored known-truncated r249 q1-master.mp4; installing r253 master only`, then 7 cards and `export/master.mp4`. Dry-run gate `YOUTUBE_AUTH_REQUIRED`, action `DRY_RUN`, export present, publish copy approved, captions 103 cues uploaded=false, thumbnail present uploaded=false. OAuth env vars were empty. Execute and state-persist steps skipped. Videos published stay 0.
- **Verification status:** Actions job 110762207440 conclusion success. Prior job 110761451601 conclusion failure, used as the regression evidence. No provider write claimed.
- **Important discovery:** The production path was blocked by a local guard, not by OAuth. Treating presence of the banned release asset as fatal prevented the r253 install.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` are unset.
- **Recommended next action:** Add those three secrets, then dispatch `youtube-production.yml` with execute=true. Do not re-encode. Do not scaffold Q2. Do not restore the presence-only abort.

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.
Earlier runs through Run 269 remain in git at `9416aae2c482ca08fd55642e0fff94568482ee51` (`RUNS.md` blob `243e47753b76bbd636a59dddb00e8c1c6f2e90c1`) and before that at `65cca063`.
