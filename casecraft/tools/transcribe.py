#!/usr/bin/env python3
"""CaseCraft transcription tool — Local Whisper via faster-whisper.

Runs entirely on this machine: the audio file never leaves it.

Usage:
    python tools/transcribe.py <audio> [--model base|small|tiny|medium] [--out <path>]
    python tools/transcribe.py <audio> --out students/<id>/sessions/<date>-<slug>/transcript.md

Output: a transcript.md matching CaseCraft's session-capture schema —
timestamped lines ("**MM:SS** — spoken text"), header with source, language
and duration. The raw transcript is a DRAFT: the therapist vets it at the
review gate (nothing merges into the passport without approval).

Notes
- faster-whisper is CPU-friendly (CTranslate2, int8). tiny/base are fast;
  "small" is the quality sweet spot for a demo clip.
- No speaker diarization (not needed for the observables-only design).
- VAD filters silence/music segments by default (--no-vad to disable).
"""

import argparse
import sys
import time
from pathlib import Path


def fmt_ts(seconds: float) -> str:
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("audio", type=Path, help="audio/video file (wav, mp3, m4a, mp4, ...)")
    ap.add_argument("--model", default="base", choices=["tiny", "base", "small", "medium"],
                    help="whisper model size (default: base)")
    ap.add_argument("--out", type=Path, default=None,
                    help="output transcript.md path (default: <audio dir>/transcript.md)")
    ap.add_argument("--lang", default=None, help="force language (e.g. en, zh); default: auto-detect")
    ap.add_argument("--no-vad", action="store_true", help="disable silence filtering")
    args = ap.parse_args()

    if not args.audio.is_file():
        print(f"[transcribe] ERROR: file not found: {args.audio}", file=sys.stderr)
        return 2

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("[transcribe] ERROR: faster-whisper not installed. Run:  pip install faster-whisper",
              file=sys.stderr)
        return 2

    print(f"[transcribe] loading model '{args.model}' (first run downloads it)...", flush=True)
    t0 = time.time()
    model = WhisperModel(args.model, device="cpu", compute_type="int8")
    print(f"[transcribe] model ready in {time.time() - t0:.1f}s — transcribing {args.audio.name}", flush=True)

    t1 = time.time()
    segments, info = model.transcribe(
        str(args.audio),
        language=args.lang,
        vad_filter=not args.no_vad,
    )

    lines = ["# Session Transcript", ""]
    lines.append(f"> Source: {args.audio.name} | Language: {info.language} "
                 f"(p={info.language_probability:.2f}) | Duration: {fmt_ts(info.duration)}")
    lines.append("> Generated locally with faster-whisper — no audio leaves this machine.")
    lines.append("> DRAFT: therapist vets this transcript at the review gate before it merges.")
    lines.append("")
    lines.append("## Transcript")
    lines.append("")

    n = 0
    for seg in segments:
        text = " ".join(seg.text.split())
        if not text:
            continue
        lines.append(f"**{fmt_ts(seg.start)}** — {text}")
        lines.append("")
        n += 1

    out = args.out or args.audio.with_name("transcript.md")
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"[transcribe] done in {time.time() - t1:.1f}s — {n} segments -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
