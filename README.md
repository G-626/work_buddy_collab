# CaseCraft — WorkBuddy custom agent skill (Agent Creativity Hackathon, WorkBuddy track)

One **Student Passport** per student — fed by a **session agent loop** — rendered into
linter-verified **stakeholder views** for teachers, parents and therapists. Built for
professionals (social workers, SEN teachers, therapists) supporting teens with
mild–moderate autism in Hong Kong.

> **All student data in this repo is fictional demo data** (Marco L., Priya S.).
> No real minor's audio, video, or records are used or shown.

---

## The loop in one line

`/session <student> --goal="…"` → capture (mock: `transcript.md` + `capture.md` →
observables only) → review gate (worker approves, ~90 s) → passport delta (versioned)
→ views regenerate (Teacher Guide · Parent Guide · Social Story) — every output
linter-checked (methodology · cross-doc consistency · **sensitivity leaks** · freshness).

## Install into WorkBuddy (runbook for judges)

1. Start WorkBuddy (desktop app).
2. Grant the agent workspace access to this folder (local files; nothing leaves the device).
3. Copy the skill + command definitions in:
   - `casecraft/skills/` → WorkBuddy `skills/` directory
   - `casecraft/commands/` → WorkBuddy `commands/` directory
4. Run the demo commands below.

## Demo commands (2 fictional students)

```text
/casecraft marco "First work-experience day at Sunbeam Bakery, Tue 19 Aug 9:00–15:30,
Travel by MTR Jordan → Mong Kok Exit B2. Supervisor: Mrs. Chan. Jobs: bagging rolls,
labelling. Kitchen warm, mixers loud."

/session marco --goal="work experience: ask for help when unsure, no more than 2 prompts"

/session batch "end-of-term review" --students marco,priya
```

Expected outputs per run: a dated pack folder (`packs/…`) or a passport version bump
(v1.0 → v1.1), plus a `linter-report.md` audit trail.

## Demo moments (see `casecraft/examples/`)

- `marco-bakery-session.md` — the full agent loop, worker edit at the gate
- `leak-catch-demo.md` — **the stage moment**: a `[team]` reference leaking into a
  Parent Guide → blocking FAIL → professional-driven fix; plus the 5-min vs 10-min
  fact contradiction (Level 1) resolved into a word-for-word Level 2 script
- `batch-demo.md` — two students, one goal, independent review gates
- `marco-patterns-trend.md` — movement-event counts → Patterns (baseline until 3 sessions)

## Docs

- `CONTEXT.md` — product design (passport, agent loop, hard principles)
- `docs/adr/0001…0005` — decision records (incl. ADR-0005: observables-only,
  positive-first capture layer)
- `docs/workbuddy-capability-tests.md` — T1–T10 platform capability evidence
- `casecraft/docs/schemas/movement-events.md` — the fixed observable vocabulary

## Status

- Skills + commands + templates + linters: **built** (Markdown format — `.md` files
  everywhere, per team decision)
- Capture: **mock/simulated** for the demo (transcripts + movement-event streams)
- Readiness: pilot-ready for a professional install (pseudonymised real use starts
  in pilots)

## Contributing

Feature branches + pull requests only — never push to main.