# Movement Event Stream — Priya S. (FICTIONAL DEMO DATA)

> Session date: 2025-08-21 | Duration: 40 min | Setting: Art class, Room 1A (group poster project)
> Captured with MediaPipe landmarks → schema `docs/schemas/movement-events.md`
> Captured by: K. Wong, School Social Worker (device) | Parent consent: recorded 2025-08-15

---

## Events

| time | event_type | duration | count | context | note |
|---|---|---|---|---|---|
| 11:00 | sit_still | — | 1 | group table, edge seat | arrived at room start |
| 11:01 | task_motion | — | 1 | sketchbook | drawing immediately (self-described regulation tool) |
| 11:03 | gaze_task | — | 1 | instructor | watching, no speech during role announcement |
| 11:05 | task_motion | — | 1 | notebook | wrote role twice |
| 11:06 | gaze_away | 4 s | 1 | group table | looked down at sheet when group started |
| 11:08 | gaze_away | — | 1 | own sheet | sketched poster ideas (2 concept sketches) |
| 11:15 | gaze_away | 2 s | 1 | direct question to her | looked down 2 s before answering |
| 11:15 | speak | — | 1 | group | "Peel palette base, ochre accents…" (1 prompt) |
| 11:15 | gaze_speaker | 3 s | 1 | group member | brief eye contact while answering |
| 11:17 | gaze_away | — | 1 | own sheet | returned to sketch |
| 11:25 | task_motion | — | 1 | own sheet | drew poster composition |
| 11:30 | gaze_task | — | 1 | written note | read note; nodded; no speech |
| 11:38 | speak | — | 1 | group | offered idea unprompted: paper choice |
| 11:38 | gaze_speaker | 3 s | 1 | group | brief eye contact with group |
| 11:39 | gaze_away | — | 1 | own sheet | resumed drawing |
| 11:43 | task_motion | — | 1 | own sheet | packed; kept sketching while leaving |

---

## Counts (session aggregates)

| Variable | Count | Trace |
|---|---|---|
| `speak` to group | 2 | 11:15 (after 1 prompt), 11:38 (unprompted) |
| `gaze_away` before answering | 1 | 11:15 (2 s pause) |
| `gaze_speaker` | 3 | 11:15, 11:38, 11:42 (debrief) |
| `pause_silence` ≥ 10 s | 0 | — |
| `smile_like` | 0 | threshold not triggered |

## Unmapped / notes for worker

- **No `smile_like` triggered** — amplitude below threshold; note: neutral affect not
  observed, which is not a signal. Calibration runs per-student.
- **11:15 2 s look-down** — an observable pause, no inference attached; routed to the
  worker (session draft Q1).
- All events trace to transcript.md or the device stream; no inferred labels retained.