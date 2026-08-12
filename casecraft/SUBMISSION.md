# CaseCraft — WorkBuddy Skills Submission Package

**Project:** CaseCraft — a WorkBuddy custom-agent-skill suite for the Agent Creativity Hackathon (WorkBuddy track).
**Purpose:** helps social workers, therapists, and SEN teachers support adolescents with mild-to-moderate autism by keeping one **Student Passport** per child and rendering it into coordinated, audited documents for every adult around the child (teacher, parent, therapist).

## What's in this package

| Path | What it is |
|---|
| `skills/casecraft/SKILL.md` + `skill.yml` + `templates/` | **One combined skill** — the whole agent loop (capture → review gate → passport delta → coordinated support pack) in a single `SKILL.md`, with both `/session` and `/casecraft` commands folded into one `## Commands` section. Generates the Coordinated Support Pack (Teacher Guide, Parent Report, Social Story, Therapist Summary) from a passport + situation brief, with a two-pass linter (methodology, cross-document consistency, **sensitivity-leak check**) |
| `tools/dryrun.py` | Stdlib-only Level-1 demo engine — replays the whole loop over the fictional fixtures (no WorkBuddy needed) |
| `tools/pdfrender.py` | Styled PDF export of the views (system dates, single-accent hierarchy, mirrored padding) |
| `students/` | Fictional demo dossiers — **Marco** (14) and **Priya** (15), with capture packages + passports |
| `dryrun/` | Verified regeneration output: both students 6/6 linter PASS, **leak drill BLOCKED**, PDFs dated today |
| `examples/` | Narrated demo moments (leak-catch, batch) — the stage beats |
| `docs/schemas/movement-events.md` | The observables-only capture schema (every event row → a transcript line) |
| `index.html` | One-page pitch / runbook |

## How to import into WorkBuddy

1. In the WorkBuddy desktop app, **Skills → Add Skill → Upload Skill** → select the
   `skills/casecraft` folder (or a zip of it). `SKILL.md` must be at the root. One
   upload registers the `casecraft` skill with both `/session` and `/casecraft` commands
   (install count 8 → 9).
2. Authorize a working folder (the `casecraft/` folder, which has `students/marco/`
   and `students/priya/` passports).
3. Run `/session marco --goal="..."` to start the loop, or `/casecraft marco "<situation brief>"`
   to generate a pack.

## How to demo without the app (Level-1, deterministic)

```bash
python tools/dryrun.py            # both students, batch
python tools/dryrun.py marco      # one student
```

Output lands in `dryrun/<student>/<session>/`: session draft → review gate → passport v1.1 → 4 views + PDFs → linter report.

## Honest limits (we say this on stage)

- **Capture runs outside WorkBuddy**: transcription (Whisper) and body-language analysis (MediaPipe) run on the worker's device and produce the `transcript.md` + `capture.md` package; the skill ingests that package. WorkBuddy is the trusted engine that keeps every output consistent and verifiable.
- **Observables only** — the capture schema records quotes, counts, timestamps. Never emotional inference (movement → affect is not scientifically sound for this population).
- **Human-in-the-loop is mandatory** — nothing merges into a passport without the professional's approval (the Review Gate). Generated documents are drafts for review, edit, and sign-off.
- **All demo data is fictional/simulated** — no real minor's audio, video, or records.
- Reports are **not clinical documents** — the passport explicitly carries a "not diagnostic" line.