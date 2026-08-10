# Movement Event Stream — Marco L. (FICTIONAL DEMO DATA)

> Session date: 2026-08-08 | Duration: 45 min | Setting: Sunbeam Bakery (work experience)
> Captured with MediaPipe landmarks → schema `docs/schemas/movement-events.md`
> Captured by: K. Wong, School Social Worker (device) | Parent consent: recorded 2025-08-10

---

## Events

| time | event_type | duration | count | context | note |
|---|---|---|---|---|---|
| 09:05 | arrival | — | — | bakery entrance | arrival 5 min early; ear defenders around neck |
| 09:06 | gaze_sweep | — | 1 | new room | first look around the kitchen |
| 09:07 | gaze_task | — | 1 | demo by instructor | watching bagging demo |
| 09:10 | task_motion | — | 1 | bagging station | began bagging rolls independently |
| 09:15 | cover_ears | 10 s | 2 | mixer started | hands over both ears; stopped work |
| 09:16 | self_regulation_use | — | 1 | mixer running | put on ear defenders after cue from instructor |
| 09:17 | task_motion | — | 1 | bagging | resumed bagging |
| 09:22 | stand_still | 45 s | 1 | task completed | stood still after finishing tray — no speech |
| 09:23 | help_request_prompted | — | 1 | 1 prompt from worker | "What should I do next?" |
| 09:23 | gaze_speaker | — | 1 | instructor | turned to instructor to ask |
| 09:30 | stand_still | 30 s | 1 | labelling station | picked up label, lowered it — no speech |
| 09:31 | help_request_prompted | — | 1 | 1 prompt from worker | "Where does this label go?" |
| 09:31 | gaze_speaker | — | 1 | instructor | turned to instructor |
| 09:45 | sit_still | — | 1 | break area | sat alone; swiped through MTR map on phone (self-regulation tool) |
| 10:15 | self_regulation_use | — | 1 | mixer started | reached for ear defenders BEFORE covering ears; no cue |
| 10:15 | task_motion | — | 1 | mixer running | continued working with defenders on |
| 10:30 | help_request_unprompted | — | 1 | second tray finished | "What should I do next?" — no cue |
| 10:30 | gaze_speaker | — | 1 | instructor | turned to instructor |
| 10:45 | speak | — | 1 | debrief | described his day; self-ordered the facts |
| 10:46 | smile_like | 2 s | 1 | debrief | mouth-corner rise ≥ threshold during debrief |
| 10:48 | gaze_task | — | — | debrief | looked at his bag for defenders as he packed |

---

## Counts (session aggregates)

| Variable | Count | Trace |
|---|---|---|
| `cover_ears` events | 1 (09:15) | mixer start |
| `help_request_prompted` | 2 | 09:23, 09:31 |
| `help_request_unprompted` | 1 | 10:30 |
| `self_regulation_use` | 2 | 09:16 (after cue), 10:15 (unprompted) |
| `stand_still` pauses ≥ 10 s | 2 | 45 s, 30 s |
| `smile_like` | 1 | debrief |

## Unmapped / notes for worker

- **09:22 & 09:30 pauses** (45 s, 30 s): no speech, no task motion. Unmap = does not
  imply anything; routed to worker via review (session draft Q1).
- **10:15** — `self_regulation_use` before any cue: candidate for a **positive micro-event**
  (`self-advocacy`); confirmed by independent transcript line 10:15 located above.
- All events trace to transcript.md or the device stream; no inferred labels retained.