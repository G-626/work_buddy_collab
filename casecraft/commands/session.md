# Command: /session

## Usage

```
/session <student-id> --goal="<session goal>"
/session <student-id> --summary <approve|edit> [notes]
/session batch "<goal>" --students <id1,id2,...>
```

## What it does

Invokes the `session` skill (skills/session/SKILL.md): the full agent loop from capture
to passport update. The primary command in CaseCraft — this is how the Student Passport
accumulates over time.

## Steps

1. **Session start**: Sets the session goal. The goal is what the worker is observing for
   (e.g. "ask for help when unsure, no more than 2 prompts").
2. **Capture**: Reads a capture package from `students/<id>/sessions/<YYYY-MM-DD>-<slug>/`.
   For the hackathon demo, this is a pre-written transcript file (simulated capture).
3. **Ingestion**: Extracts observables (events, quotes, counts, timestamps) from the
   capture. Never infers emotion or internal states.
4. **Review gate**: Presents a structured session draft to the worker for approval.
   The worker approves or edits within ~90 seconds. Nothing merges without approval.
5. **Passport delta**: Merges the approved session summary into the Student Passport
   (updates goals progress, adds session log entry, refreshes date stamps).
6. **Stakeholder views**: Regenerates role-specific views (Teacher Guide, Parent Guide,
   optional Social Story) from the updated passport.

## Examples

```
/session marco --goal="work experience: ask for help when unsure, no more than 2 prompts"
```

```
/session priya --goal="group work: contribute one idea with pre-assigned role"
```

```
/session batch "end-of-term review" --students marco,priya
```

## Response shape

1. Session draft summary (observables, goal progress, questions for the worker)
2. Review gate prompt: approve or edit
3. On approval: passport version bump, updated sections listed
4. Regenerated views (Teacher Guide, Parent Report, optional Social Story, Therapist Summary) with linter summary
5. PDF + file paths
6. Closing line: *"Session approved and merged. Views regenerated for your review."*
