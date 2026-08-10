# Assumptions review — skill.md vs. original ADR assumptions (2026-08-10)

Review of whether the design assumptions baked into `skills/casecraft/SKILL.md` and
`skills/session/SKILL.md` still hold, given: (a) the installed WorkBuddy app (v4.10.4),
(b) the therapist-report research (SOAP / IEP / progress-report formats), and
(c) the hackathon judging criteria (sponsored product usage, working MVP).

## Verdict summary

| # | Assumption | Source | Verdict | Action |
|---|---|---|---|---|
| A1 | Observables only — never emotional inference | ADR-0004/0005, CONTEXT §3.1 | ✅ **VALID** | keep; it is the demo principle |
| A2 | Positive-first framing in all user-facing output | CONTEXT §3.2 | ✅ **VALID** | keep |
| A3 | Human-in-the-loop review gate, no auto-commit | ADR-0004 | ✅ **VALID** | keep; differentiator |
| A4 | Passport = single source of truth | ADR-0004 | ✅ **VALID** | keep |
| A5 | No clinical claims / no diagnosis in parent-teacher views | ADR-0002, CONTEXT §3.7 | ✅ **VALID** | keep; note therapist lens may carry `[team]` clinical-scope detail |
| A6 | One skill, not many; dossier-driven audiences | ADR-0003 | ⚠️ **PARTIALLY VALID** | split into 2 skills already (session + casecraft); audience tags = sensitivity tags now, not `[teacher]`/`[parent]` — templates must align |
| A7 | Skill = plain Markdown files (`skills/`, `commands/`) | techpedia §7 | ⚠️ **UNVERIFIED** | official practice case documents `skill.yml`; must confirm against installed app before event (T5 re-run) |
| A8 | 200–350 words teacher guide / 150–300 parent guide | template v1 | ❌ **OUTDATED** | therapist reports are structured, not length-capped — replace length rule with structure rule |
| A9 | Outputs are drafts for professional review | ADR-0001 | ✅ **VALID** | keep; PDF export must preserve "draft" watermark |
| A10 | Sensitive sections never leak into wrong view | ADR-0004 §5 | ✅ **VALID** | keep; add `[team]`-only therapist lens to the leak matrix |
| A11 | Cross-document consistency is the moat | ADR-0003 | ✅ **VALID** | keep; strengthen with structured fact table |
| A12 | Freshness check (>30 days) | ADR-0004 | ✅ **VALID** | keep |
| A13 | Batch mode per student | skill v1 | ✅ **VALID** | keep |
| A14 | Parent guide = "what's happening" only | template v1 | ❌ **OUTDATED** | parent reports need: overview, goal progress w/ evidence, home strategies, same-words, next session, contact |
| A15 | Social Story optional, teen-facing | ADR-0003 | ✅ **VALID** | keep |

## Detailed findings

### A6 — audience tags vs sensitivity tags (real inconsistency found)

The passports (`students/*/passport.md`) use sensitivity tags `[open]`, `[team]`,
`[clinical]`. But the templates (`templates/teacher-guide.md` §5, `parent-guide.md` §5)
still instruct the model to use **`[teacher]` / `[parent]` / `[employer]` audience tags
that no longer exist in any passport**. Running the skill as written would tell the model
to read sections that are not tagged that way — silent guess territory. Fix: templates
must reference the actual sensitivity tag system and map: teacher/parent views ←
`[open]`; therapist summary ← `[open] + [team]`; clinical ← never in any generated view
(reserved for the professional's own records).

### A7 — skill file format: unverified against the installed app

The repo scaffold uses plain-Markdown skills + `templates/` + `commands/` (techpedia §7
form). The official practice case ("Create-Skills") describes `skill.yml` metadata +
implementation files. Both are documented; we now have the app installed (v4.10.4) and
can settle this empirically before the event. This is the T5 re-run the CONTEXT.md
already flags. **This install unblocks it — schedule it.**

### A8/A14 — report structure beats word count

Therapist reports to parents are structured documents (SOAP-informed, goal-progress
tables, home strategies, next-session plan, sign-off), not 150–300 word notes. The
length caps produce the thin, samey outputs we saw in the dry run (Priya's teacher
guide referenced the bakery!). Replace:
- Teacher Guide → one-page classroom sheet: **Snapshot · What to expect · What helps
  · What to avoid · Language to use · Warning signs · Escalation plan**
- Parent Report → 1–2 page progress report: **Overview · Goal progress (table:
  goal → evidence → status) · What went well · Home strategies · Same words at home
  · What to watch for · Next session focus · Contact**
- New: **Therapist Summary** (already promised in CONTEXT §7 matrix but missing from
  the pipeline!) — `[open]+[team]`, clinical-scope detail, patterns, session log.
  This was the biggest gap: the matrix lists it, the skill never generates it.

### A15 — PDF export is missing (and it is a judging lever)

"Sponsored product usage" is a judging criterion. WorkBuddy's Skills Marketplace
includes **Office Document Suite** (Word/Excel/PPT) and the File-Recognition practice
confirms PDF generation. Exporting every pack to PDF:
1. makes the deliverable land like a real professional artifact (not a .md file),
2. exercises the platform's document tooling (sponsored usage + completeness),
3. is trivially replicable in Level-1 via fpdf2 for the dry run.

### Not in scope of this review
- Capture engine (MediaPipe/MCP): unchanged, still simulated for the demo.
- Automation/Assistant push: platform-native, out of skill-file scope.
