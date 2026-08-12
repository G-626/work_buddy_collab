# CaseCraft — WorkBuddy custom-agent skill suite

**Agent Creativity Hackathon, WorkBuddy track.** A WorkBuddy skill suite that keeps
**one Student Passport per child** and turns every therapy/support session into
audited, audience-specific documents for the adults around the child — teacher,
parents, therapist — built for professionals (social workers, SEN teachers,
therapists) supporting teens with mild–moderate autism in Hong Kong.

> **All student data in this repo is fictional demo data** (Marco L., 14 · Priya S., 15).
> No real minor's audio, video, or records are used or shown.

---

## The loop in one line

`/session marco --goal="…"` → capture package (`transcript.md` + `capture.md`,
observables only) → draft summary → **human review gate** (therapist edits/approves,
~90 s) → passport delta (v1.0 → v1.1) → views regenerate (Teacher Guide · Parent
Report · Social Story · Therapist Summary) — every output linter-checked
(methodology · cross-doc consistency · **sensitivity leaks** · freshness).

## Architecture

```
Session (audio/video)
   │  record on therapist's device          ── device side
   ▼
capture package:  transcript.md             Local Whisper (tools/transcribe.py) — REAL, PR #8
                  capture.md                MediaPipe observables — roadmap/mocked (fixtures)
   │
   ▼
/casecraft  (ONE skill — casecraft/skills/casecraft)
   │   contains BOTH /session and /casecraft entry points in one SKILL.md
   │  →  draft summary  →  REVIEW GATE (therapist approves)  →  passport delta
   ▼
Coordinated Support Pack
   │  Teacher Guide · Parent Report · Social Story · Therapist Summary (MD + PDF)
   ▼
delivery to stakeholders  ── roadmap: Slack per-user DMs (one chat per parent/teacher)
```

## Repo layout

| Path | What it is |
|---|---|
| `casecraft/skills/casecraft/` | **Single combined skill** — the whole agent loop (capture → review gate → passport delta → coordinated support pack) in one `SKILL.md`, with both `/session` and `/casecraft` commands folded into one `## Commands` section |
| `casecraft/tools/dryrun.py` | Stdlib-only **Level-1 demo engine** — replays the whole loop, no app needed |
| `casecraft/tools/pdfrender.py` | Styled PDF export (system dates, single-accent hierarchy, mirrored padding) |
| `casecraft/tools/transcribe.py` | **Local Whisper transcription** (faster-whisper) — real audio → schema-matched `transcript.md` (PR #8) |
| `casecraft/students/` | Fictional dossiers: `marco/`, `priya/` — passports + capture packages |
| `casecraft/dryrun/` | Verified regeneration output (drafts, review gate, passport v1.1, 4 views, 5 PDFs, linter report) |
| `casecraft/examples/` | Narrated demo moments (leak-catch, batch, patterns-trend) — the stage beats |
| `casecraft/SUBMISSION.md` | Submission package map (what's in the zip) |
| `casecraft/index.html` | One-page pitch / runbook |
| `CONTEXT.md` | Product design bible (passport, agent loop, hard principles) |
| `docs/adr/0001…0005` | Decision records (incl. 0002 secure-by-design, 0005 observables-only) |
| `docs/workbuddy-capability-tests.md` | T1–T10 platform capability evidence |

---

## How to use — three ways

### 1. Deterministic demo without the app (Level-1) — start here

```bash
cd casecraft
python tools/dryrun.py            # both fictional students
python tools/dryrun.py marco      # one student
```

Output lands in `dryrun/<student>/<session>/`:
`01-session-draft` → `02-review-gate` → `03-passport-v1.1` → `05-linter-report`
→ `views/` (4 view .md + 5 dated PDFs + the leak-drill fixture).
Both students regenerate **6/6 linter PASS**; the leak drill is intentionally
**BLOCKED** (it's the stage moment: a `[team]` reference leaking into a Parent
Guide gets caught and fixed).

### 2. In WorkBuddy (Level-2, the real app)

1. Start the WorkBuddy desktop app.
2. Grant the agent workspace access to this folder.
3. **Skills tab → Add Skill → Upload Skill** → upload `casecraft/skills/casecraft`
   (folder or zip with `SKILL.md` at its root). One upload registers both
   `/session` and `/casecraft` commands. (Disk-copy alternative: copy it into
   `~/.agents/skills/casecraft/` and restart WorkBuddy.)
4. Run:

```text
/session marco --goal="work experience: ask for help when unsure, no more than 2 prompts"
/casecraft marco "First work-experience day at Sunbeam Bakery, Tue 19 Aug 9:00–15:30,
Travel by MTR Jordan → Mong Kok Exit B2. Supervisor: Mrs. Chan. Jobs: bagging rolls,
labelling. Kitchen warm, mixers loud."
/session batch "end-of-term review" --students marco,priya
```

> ▶️ Level-2 end-to-end verification in the app is **done** — `/session marco` ran to
> completion inside WorkBuddy (review gate APPROVED, passport delta, 4 views, linter
> 6/6 + leak drill BLOCKED, PDFs). See "How to use" below for the exact steps.

### 3. Real transcription (new, PR #8 — for hands-on testing)

```bash
pip install faster-whisper          # one time
python casecraft/tools/transcribe.py "C:\path\to\session.mp3" --model base
```

- Writes `transcript.md` next to the audio (or `--out <session-folder>/transcript.md`).
- `--model small` = better quality; `base` = speed/quality sweet spot. `wav/mp3/m4a/ogg/mp4` supported.
- **Local-only: the audio never leaves the machine.** First run downloads the model (~140 MB).
- Verified: 43 s demo clip → 18 segments, `en (p=1.00)`, ~4 s on CPU.

## Data model

- `students/<id>/passport.md` — the single source of truth (accumulating, versioned).
- `students/<id>/sessions/<date>-<slug>/transcript.md` + `capture.md` — capture
  package (fixtures today; real audio via `transcribe.py`).
- `docs/schemas/movement-events.md` — the observables-only event vocabulary
  (every event row traces to a transcript line).
- `dryrun/` — regenerable demo output (never hand-edit; run `dryrun.py`).

## Verification so far

- **T1–T10 capability tests PASS** (`docs/workbuddy-capability-tests.md`) — incl.
  cross-session file memory, which the feedback loop builds on.
- **Level-1 engine**: both students 6/6 linter PASS, leak drill BLOCKED, PDFs dated today.
- **Real transcription**: verified end-to-end (PR #8).
- **Slack per-user delivery**: feasibility confirmed from official WorkBuddy docs
  (Socket Mode; `chat:write`/`im:write`/`files:write` to DM a parent by Slack user
  ID, `message.im`/`im:history` to receive their reply = the feedback channel).
  Not yet configured — see Roadmap below.

## Design principles (don't break these)

- **Observables only** — record quotes, counts, timestamps. Never emotional
  inference; automated "microexpression → affect" is not scientifically sound for
  this population and gets the pitch destroyed by practitioner judges (ADR-0005).
- **Human-in-the-loop is mandatory** — nothing merges into a passport without the
  professional's approval (the Review Gate).
- **Secure-by-design, not "everything local"** — the app + Whisper run locally,
  but LLM summarization is remote processing. Say it exactly that way (ADR-0002).
- **Fictional data only** in demos; reports carry a "not diagnostic" line.

## How to use CaseCraft in WorkBuddy (for the team)

CaseCraft is **one WorkBuddy skill** (`casecraft`). It contains the entire agent
loop — capture → review gate → passport delta → coordinated support pack — in a
single `SKILL.md`, with **both** slash commands (`/session` and `/casecraft`)
folded into one `## Commands` section. You upload it **once** and both commands
are available.

### What you need
- The WorkBuddy desktop app (distributed as `CodeBuddy.exe`), signed in.
- This repo cloned locally, so the skill can read the mock student data
  (`casecraft/students/marco`, `casecraft/students/priya`).
- The skill folder: `casecraft/skills/casecraft/` (contains `SKILL.md`,
  `skill.yml`, and `templates/`).

### Install the skill (Upload Skill dialog — preferred)
1. Open WorkBuddy → **Skills** tab (sidebar: New Task · Claw · Skills · Automation).
2. Click **Add Skill → Upload Skill**.
3. Select the `casecraft/skills/casecraft` folder (or a zip of it). The dialog
   requires `SKILL.md` at the root — this folder has it.
4. One upload registers **one** `casecraft` skill with **both** `/session` and
   `/casecraft` commands. (The install count goes 8 → 9, not 10 — there is no
   separate `session` skill anymore.)
5. Authorise WorkBuddy to access this repo folder (local files; nothing leaves
   the device). The skill reads `students/<id>/passport.md` relative to it.

> **Disk-copy alternative** (if the upload dialog is awkward): copy
> `casecraft/skills/casecraft/` into `~/.agents/skills/casecraft/` and restart
> WorkBuddy. That folder is the user-installed skills directory the app watches.

### Run it
Open a **New Task** and type one of:

```text
/session marco --goal="work experience: ask for help when unsure, no more than 2 prompts"
```
Runs the full loop from Marco's capture package: draft → **review gate** (you
approve or edit — nothing merges without you) → passport delta (v1.0 → v1.1) →
regenerated 4 views + linter report.

```text
/casecraft marco "First work-experience day at Sunbeam Bakery, Tue 19 Aug 9:00–15:30,
MTR Jordan → Mong Kok Exit B2. Supervisor: Mrs. Chan. Jobs: bagging rolls, labelling.
Kitchen warm, mixers loud."
```
Generates the Coordinated Support Pack (Teacher Guide · Parent Report · Social
Story · Therapist Summary) straight from the current passport + a situation brief.

Batch form (one goal/brief, every student):
```text
/session batch "end-of-term review" --students marco,priya
/casecraft batch "first day of new term, room changes" --students marco,priya
```

### What you should see
- A **review gate** prompt — approve or edit before anything is saved.
- Output written to `casecraft/students/<id>/sessions/…/` (or `packs/…`):
  `01-session-draft` → `02-review-gate` (APPROVED) → `03-passport-v1.x` →
  `05-linter-report` → `views/` (4 `.md` + 5 dated PDFs).
- The **linter report** shows **6/6 checks pass**; the deliberate **leak drill**
  is **BLOCKED** (a `[team]` token leaking into a Parent Guide is caught — that
  is the demo moment, not a bug).

### Test without the app (no WorkBuddy needed)
```bash
cd casecraft
python tools/dryrun.py            # both fictional students
python tools/dryrun.py marco      # one student
```
Same loop, deterministic, over the repo fixtures. Both students: 6/6 linter +
leak drill BLOCKED, PDFs dated today.

> **Privacy note (say it this way):** the app and Whisper run locally, but LLM
> summarisation is remote processing. CaseCraft is *secure-by-design* (human
> review + pseudonymisation), not "everything stays on device."

### Roadmap (not yet built)
- Full-loop wiring: real transcript → session pipeline.
- `/schedule <id> <date>` + Slack per-user DM delivery of each stakeholder's view.
- Feedback loop: a daily Automation task that fires the day before a session.
- MediaPipe observables → real `capture.md`; `/casenote` rapid mode.

## Contributing

Feature branches + pull requests only — never push to main. See
`casecraft/SUBMISSION.md` for the submission package map.
