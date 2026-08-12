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

CaseCraft is a **single skill** (`casecraft`) that contains the whole agent loop —
capture → review gate → passport delta → coordinated support pack — with both
`/session` and `/casecraft` entry points folded into one `SKILL.md`.

1. Start WorkBuddy (desktop app) and sign in.
2. **Skills tab → Add Skill → Upload Skill** → upload `casecraft/skills/casecraft`
   (as a folder or zip containing `SKILL.md` at its root). One upload = one skill
   with both commands registered.
3. Grant the agent workspace access to this repo folder (local files; nothing
   leaves the device) — the skill reads `students/<id>/passport.md` relative to it.
4. Run the demo commands below.

> Disk-copy alternative (no app dialog): copy `casecraft/skills/casecraft/` into
> `~/.agents/skills/casecraft/` and restart WorkBuddy.

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