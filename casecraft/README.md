# CaseCraft — Coordinated Support Pack Skill (Hackathon Scaffold)

A WorkBuddy Custom Agent Skill that generates a **Coordinated Support Pack** — a set of
audience-specific documents (Teacher Guide, Parent Report, optional Social Story) from one
Student Passport and one situation brief, kept consistent with each other by cross-document
linting. The operator is a **professional** (social worker, therapist, SEN teacher) — never
the teen. Every output is a **draft for professional review**.

Built for the Agent Creativity Hackathon (WorkBuddy Track) —
https://luma.com/agentcreativity

## Structure

```
casecraft/
├── skills/
│   └── casecraft/                     # ONE skill = the whole agent loop
│       ├── SKILL.md                   # Capture → review gate → passport delta →
│       │                               #   coordinated support pack; /session + /casecraft
│       │                               #   commands folded into one "## Commands" section
│       ├── skill.yml                  # Manifest (metadata + workflow summary)
│       └── templates/
│           ├── teacher-guide.md       # Teacher Guide generation rules
│           ├── parent-guide.md        # Parent Report generation rules
│           ├── social-story.md        # Social Story generation rules (Carol Gray 10.2)
│           ├── therapist-summary.md   # Therapist Summary generation rules
│           ├── patterns.md            # Movement-event -> Patterns engine
│           ├── linter-teacher-guide.md    # Teacher Guide linter checks
│           ├── linter-parent-guide.md     # Parent Report linter checks
│           ├── linter-social-story.md     # Social Story linter checks (10.2 + cross-doc)
│           ├── linter-therapist-summary.md# Therapist Summary linter checks
│           └── linter-sensitivity-leak.md # Sensitivity leak check (blocking)
├── students/                          # Fictional demo passports (per-student folders)
│   ├── marco/
│   │   ├── passport.md                # The Student Passport — living, versioned, tagged
│   │   ├── sessions/                  # Session capture packages land here
│   │   └── packs/                     # Generated stakeholder views land here
│   └── priya/
│       ├── passport.md                # Second demo passport — contrasting profile
│       ├── sessions/
│       └── packs/
└── examples/
    ├── marco-bakery-pack.md           # Worked example: full pack + linter report
    └── marco-bakery-session.md        # Worked example: full session loop
```

## Key design principles

1. **Observables, never inferences.** The capture layer emits what happened — quotes, counts,
   timestamps — never how the student felt. No emotional inference, no attribution.
2. **Human-in-the-loop review gate.** Nothing merges into the passport without the worker's
   approval. Auto-commit is off by design.
3. **One source of truth.** The Student Passport is the single artifact all views derive from.
   Nobody re-types facts about the child.
4. **Verifiable output.** Every document is linted against methodology, cross-document
   consistency, and sensitivity rules — with visible proof the professional can audit.
5. **Local-first files.** Passports and sessions live in the worker's authorized local folders;
   prompts use pseudonyms; full identifiers stay local. All demo data is fictional.

## Why not just a chatbot?

A professional *can* paste session notes into Gemini and get a plausible teacher guide. What
they cannot get:

- **An audit** — every output is linted against methodology + consistency + sensitivity rules,
  with visible proof. A chatbot gives you prose; CaseCraft gives you prose *and* an audit trail.
- **A living passport** — one source of truth that accumulates across months, keeps voice,
  scripts, and facts aligned, and follows the student through transitions. A chatbot starts
  from zero every conversation.
- **The loop** — sessions feed the passport without the professional re-typing history, and
  stakeholder views re-render from a single approved delta. Generic chatbots don't accumulate.

## Installing in WorkBuddy

CaseCraft ships as **one skill** (`casecraft/skills/casecraft/`) — the whole agent
loop in a single `SKILL.md` with both `/session` and `/casecraft` commands inside it.

- **Upload Skill** (preferred): Skills tab → Add Skill → Upload Skill → select
  `casecraft/skills/casecraft` (folder or zip with `SKILL.md` at the root). One
  upload registers both commands. The install count goes 8 → 9 (there is no
  separate `session` skill).
- **Disk copy**: copy `casecraft/skills/casecraft/` into `~/.agents/skills/casecraft/`
  and restart WorkBuddy.
- Authorise WorkBuddy to access the `casecraft/` folder (the skill reads
  `students/<id>/passport.md` from there).

### Full usage steps (for the team)

1. Open WorkBuddy (CodeBuddy.exe), sign in.
2. **Skills → Add Skill → Upload Skill** → choose `casecraft/skills/casecraft`.
   Wait for the install count to move 8 → 9.
3. Authorise the `casecraft/` folder as the agent's workspace.
4. Open a **New Task** and run, e.g.:
   ```
   /session marco --goal="work experience: ask for help when unsure, no more than 2 prompts"
   ```
   or generate a pack from a brief:
   ```
   /casecraft marco "First work-experience placement at Sunbeam Bakery next Tuesday 19 Aug,
   9:00–15:30. Travel by MTR Jordan → Mong Kok. Supervisor is Mrs. Chan. Jobs: bagging rolls,
   labelling boxes. Kitchen is warm and mixers are loud."
   ```
5. At the **review gate**, approve or edit — nothing merges without your sign-off.
6. Output lands in `students/<id>/sessions/…/` (draft, gate, passport delta,
   linter report 6/6, views as 4 `.md` + 5 PDFs). The deliberate leak drill shows
   **BLOCKED** — that is the demo moment, not a failure.

### Test without the app
```bash
cd casecraft
python tools/dryrun.py          # both students
python tools/dryrun.py marco    # one student
```
Same loop, deterministic. Both students: 6/6 linter + leak drill BLOCKED.
