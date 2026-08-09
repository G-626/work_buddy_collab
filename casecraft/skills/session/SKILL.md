# Skill: session

Run the full **Agent Loop** for one student: capture → ingest → review gate → passport
delta → stakeholder views. This is the primary skill in CaseCraft — it is how the Student
Passport accumulates over time.

## Inputs

| Input | Required | Source |
|---|---|---|
| Student ID | yes | Folder name under `students/` (e.g. `marco`) |
| Session goal | yes | Free text: what the worker is observing for |
| Capture package | yes | A folder under `students/<id>/sessions/<YYYY-MM-DD>-<slug>/` containing `transcript.md` (session dialogue) and `capture.md` (Movement Event Stream per `casecraft/docs/schemas/movement-events.md`; mock/simulated for the demo) |

## Pipeline

### Step 1 — Load the passport

Read `students/<id>/passport.md`. Note the current version, section tags (`[open]`,
`[team]`, `[clinical]`), and the session goal history. The passport is the context —
every observable is interpreted against it.

### Step 2 — Load the capture package

Read all files in the session folder: `transcript.md` (simulated transcription) and
`capture.md` (Movement Event Stream per `casecraft/docs/schemas/movement-events.md` —
fixed vocabulary, no affect labels). The capture contains raw observations — what was
said, what happened, timestamps.

**Hard rule: observables only.** The capture layer produces *what happened* — quotes,
counts, timestamps, movement events from the fixed vocabulary (see CONTEXT.md §4:
body primitives, gaze targets, voice-adjacent events, positive micro-events). It never
produces *how the student felt* — no emotional inference, no attribution, no state labels.
If the capture contains inferred labels ("seemed anxious"), strip them and note the
removal in the review draft.

**Positive-First Rule.** All session-draft language frames findings as reinforcement or
support. Events that could read negatively appear as neutral observables plus a question
to the worker — never as a verdict on the child.

### Step 3 — Extract observables

From the capture, extract:
- **Events**: things that happened, with timestamps ("10:14 — covered ears when mixer started")
- **Quotes**: things the student or staff said, verbatim
- **Counts**: how many times a goal-relevant behaviour occurred ("asked for help 2 times")
- **Goal progress**: did the student meet the session goal? Evidence for/against.

### Step 4 — Draft the session summary

Structure the observables into a session draft:
- Session metadata (date, goal, duration)
- Observed events (chronological, timestamped)
- Goal progress assessment (met / partially met / not met, with evidence)
- Staff-worthy quotes (things the student said that show progress or difficulty)
- Questions for the worker (anything ambiguous, anything missing)
- Proposed passport delta (which sections to update, what to add/change)

### Step 5 — Review gate

Present the session draft to the worker. The worker approves or edits within ~90 seconds.

**Nothing merges without approval.** If the worker edits, the edited version is what
merges. If the worker rejects, the session is discarded and noted in the session log
as "rejected by reviewer."

### Step 6 — Passport delta

On approval, merge the session summary into the passport:
- Bump the version number and refresh the "Last updated" date
- Add the session summary to the Session log section `[team]`
- Update Goals progress if the session was goal-relevant
- Add or update Triggers/What works/Communication profile if new evidence emerged
- Update Patterns `[team]`: aggregate movement-event counts aligned to context
  (what activity, what sounds/transitions, time of day). Output is descriptive and
  correlational — never a verdict. Surprising patterns route to the worker as questions.
  Render per `templates/patterns.md` (baselines until ≥ 3 sessions; positive-first
  opening line; every row traceable to capture.md).
- Stamp each updated section with the session date (for freshness checking)

### Step 7 — Regenerate stakeholder views

Invoke the `casecraft` skill's view-generation pipeline (steps 3–7 of
`skills/casecraft/SKILL.md`) using the updated passport as the source. All views are
linted, including the sensitivity leak check.

### Step 8 — Report back

- Summary line: `Session approved. Passport v<N> updated. N views regenerated, X checks passed, Y auto-fixed, Z flagged.`
- Full session summary
- List of passport sections updated
- File paths for all outputs
- Closing line: *"Session approved and merged. Views regenerated for your review."*

## Batch mode

`/session batch "<goal>" --students <id1,id2,...>` — run the pipeline once per student
from one goal. Each student's session is independent: separate capture packages, separate
review gates, separate passport deltas. Produce a summary table: student, goal met?,
passport version, flags needing review.

## Hard boundaries

- **No emotional inference.** Observables only. Strip inferred labels from captures.
- **No auto-commit.** The review gate is mandatory. Nothing merges without approval.
- **No clinical claims.** The passport describes what supports the student — never
  a diagnosis. The Clinical section `[clinical]` is never populated by the session
  pipeline — it is reserved for the professional's own clinical records.
- **Fictional demo data only.** All capture packages in the demo are pre-written,
  simulated transcripts. No real minor's audio or video is ever captured or shown.
