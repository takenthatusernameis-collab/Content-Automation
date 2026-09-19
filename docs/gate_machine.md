# Gate machine drop

This page is the copy-paste path for putting Selected VO on the machine that runs gates.
It is not a new tool. It does not synthesize audio inside the repo. It does not upload.

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
DROP="$PACKET/vo/002-stop-deciding-what-to-work-on-every-morning-take-selected.wav"
mkdir -p "$PACKET/vo"
python3 tools/narration_adapter.py "$PACKET" --print-words > /tmp/q1-words.txt
# Speak /tmp/q1-words.txt with a microphone, or use one optional TTS block below.
# Save the result ONLY at $DROP (wav preferred, flac ok).
python3 tools/narration_adapter.py "$PACKET"
```

Expect `take:` to print the DROP path and `kind: generated` (or `human` if
you recorded it). If `take: missing`, the file is in the wrong folder or empty.

### Optional local TTS (already-installed tools only)

These one-liners are not a repo CLI. Use at most one. They write only to `$DROP`.
If `$DROP` already exists and is non-empty, skip this block.

Already have a generated file elsewhere:

```bash
cp -n /path/to/existing-generated.wav "$DROP"
```

espeak-ng + ffmpeg (Debian/Ubuntu style; robotic but authorized as generated):

```bash
command -v espeak-ng >/dev/null && command -v ffmpeg >/dev/null && \
  espeak-ng -f /tmp/q1-words.txt -w /tmp/q1-espeak.wav && \
  ffmpeg -y -i /tmp/q1-espeak.wav -ac 1 -ar 44100 -sample_fmt s16 "$DROP"
```

macOS `say` + ffmpeg:

```bash
command -v say >/dev/null && command -v ffmpeg >/dev/null && \
  say -f /tmp/q1-words.txt -o /tmp/q1-say.aiff && \
  ffmpeg -y -i /tmp/q1-say.aiff -ac 1 -ar 44100 -sample_fmt s16 "$DROP"
```

After any of those, keep `vo_origin.md` `kind: generated`. Do not describe the
file as a human recording. Do not commit it.

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
Do not add a TTS wrapper under `tools/`.
