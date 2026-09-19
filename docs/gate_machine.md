# Gate machine drop

This page is the copy-paste path for putting Selected VO on the machine that runs gates.
It is not a new tool. It does not synthesize audio. It does not upload.

## Why this page exists
Q1 paperwork is done. Status is `ready_for_vo`. Audio is gitignored.
Agents cannot invent a committed wav. HTTPS clone in the agent sandbox is parked.
The remaining labor is a local file at the packet-relative DROP path.

Generated narration is the authorized fallback after `2026-09-19T00:00:00Z`
(`OPERATOR_HOLD.md`). Keep `vo_origin.md` `kind: generated` unless a human
recording replaces it.

## Packet
- Folder: `videos/002-stop-deciding-what-to-work-on-every-morning`
- DROP: `videos/002-stop-deciding-what-to-work-on-every-morning/vo/002-stop-deciding-what-to-work-on-every-morning-take-selected.wav`
- Also accepted: same stem with `.flac`, or `-v2` before the extension
- Repo-root `vo/` is not Selected VO
- Do not `git add -f` the take

## On the gate machine

```bash
PACKET=videos/002-stop-deciding-what-to-work-on-every-morning
mkdir -p "$PACKET/vo"
python3 tools/narration_adapter.py "$PACKET" --print-words > /tmp/q1-words.txt
# Speak /tmp/q1-words.txt with a microphone or any local TTS you already have.
# Save the result ONLY at the DROP path (wav preferred, flac ok).
python3 tools/narration_adapter.py "$PACKET"
```

Expect `take:` to print the DROP path and `kind: generated` (or `human` if
you recorded it). If `take: missing`, the file is in the wrong folder or empty.

Then, still on that machine:

```bash
python3 tools/vo_session.py "$PACKET" --force
python3 tools/set_status.py "$PACKET" --to ready_for_edit
# --write only after dry-run OK and Selected VO present
python3 tools/card_generator.py "$PACKET" --write-manifest
python3 tools/timeline.py "$PACKET" --write
python3 tools/media_qa.py "$PACKET"
python3 tools/assemble.py "$PACKET"
python3 tools/complete.py "$PACKET"
```

`assemble.py` stays dry-run until READY_TO_ENCODE. `complete.py` stays
INCOMPLETE_MEDIA until VO + cards exist. Do not write a dummy `export/master.mp4`.

## Agent sandbox
This page does not authorize committing audio from an agent workspace.
A wav that exists only in a disposable sandbox is not gate-machine Selected VO.
