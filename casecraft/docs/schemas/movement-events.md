# Movement Event Schema — observables only (v1)

The capture layer produces **what happened**, never *how the student felt*. This schema
defines the fixed vocabulary for the Movement Event Stream (CONTEXT.md §4, ADR-0005).
Capture files are Markdown tables (`.md`), readable by WorkBuddy with zero extra tooling.

## 1. Event record

Every event is one row. Fields:

| Field | Required | Format | Example |
|---|---|---|---|
| `time` | yes | `HH:MM` (session-local clock) | `09:15` |
| `event_type` | yes | from the fixed vocabulary below | `cover_ears` |
| `duration` | optional | seconds (only when the event is a pause/sustained state ≥ 10 s) | `45 s` |
| `count` | optional | integer — only for countable events within one context block | `2` |
| `context` | yes | observable setting only — never mood | `mixer started` |
| `note` | optional | neutral, factual annotation or cross-ref to transcript line | `→ transcript 09:15` |

## 2. Fixed vocabulary (event families)

### Body primitives
`stand_still` · `pace` · `sit_still` · `approach` · `withdraw` · `cover_ears` ·
`cover_eyes` · `self_touch` · `task_motion` (describe the task: `bagging`, `labelling`,
`drawing`, `sorting`) · `shift_posture`

### Gaze (head-pose/gaze targets)
`gaze_speaker` · `gaze_task` · `gaze_away` · `gaze_sweep` (scanning the room) ·
`gaze_repeat` (alternating between two targets, e.g. task ↔ instructor)

### Voice-adjacent (cross-referenced with transcript)
`speak` · `question` · `answer` · `vocalize` · `laugh` · `pause_silence` (with duration)

### Positive micro-events (calibrated thresholds only)
| event_type | definition | calibration |
|---|---|---|
| `smile_like` | mouth-corner rise ≥ threshold | geometric, per-student calibration; NEVER asserted as mood |
| `help_request_prompted` | asks for help after a cue (≤ 2 words from worker) | counted from transcript |
| `help_request_unprompted` | asks for help without any cue | from transcript |
| `self_regulation_use` | uses a known regulation tool unprompted (ear defenders, MTR map, sketchbook) | from transcript + visual |
| `initiation_unsolicited` | starts a statement to the group without being addressed | from transcript |

## 3. Anti-schema — never emitted

These are **not representable** in the stream. If the engine or transcript contains them,
the session skill strips them and records the removal in the review draft:

- **Affect labels**: anxious, stressed, happy, sad, calm, upset, frustrated, distressed…
- **Energy/arousal judgements**: hyper, drained, restless "because…", bored, engaged
- **Motivational state**: unmotivated, resistant, compliant, cooperative
- **Dispositional/identity labels**: shy, quiet, difficult, challenging
- **Diagnostic terms**: autism, ASD outliers, any clinical language
- **Attribution of causation**: "because the noise", "to avoid…" — the stream records
  *co-occurrence in context*, never causation ("mixer started + 09:15 cover_ears" is fine).

## 4. Ingestion rules (for the `session` skill)

1. Every `event_type` must come from the vocabulary above. Unknown types → **flag as
   `unmapped event`** in the review draft; never guess a label.
2. Durations only for `stand_still`, `pause_silence`, `cover_ears`, `gaze_reverse`
   blocks ≥ 10 s. Shorter events have no duration field (avoid false precision).
3. `context` values are observables only: `mixer started`, `instructor speaking`,
   `group discussion`, `break area`, `debrief`. Never "because he was …".
4. Positive micro-events are **threshold-calibrated** — a `smile_like` is a measured
   mouth-corner rise, reviewed by the worker before it merges.
5. Every event row must trace to a transcript line or measured landmark stream; the
   capture is open to audit (linter Level 0: `traceable`).
6. Events aggregate into the passport **Patterns** section
   (see `templates/patterns.md`): counts per activity context, over time — descriptive
   and correlational, never a verdict.

## 5. File layout

```
students/<id>/sessions/<YYYY-MM-DD>-<slug>/
├── transcript.md      # simulated or real transcription (text, timelines)
└── capture.md         # Movement Event Stream (this schema, as tables)
```