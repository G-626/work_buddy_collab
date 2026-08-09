# Coordinated Support Pack: one skill, dossier-driven audiences, optional Social Story

## Context

CaseCraft evolved from a single-document generator (social stories) to a multi-document
generator (Coordinated Support Pack). Three structural decisions shaped the architecture.

## Decisions

**One skill, not multiple skills.** WorkBuddy has no documented sub-skill mechanism. Multiple
skills would require the professional to run `/teacher-guide` then `/parent-guide` separately
— which is exactly the "re-paste the dossier into Gemini three times" problem we are solving
against. One skill means one command, one brief, and one coordinated pack. The consistency
check runs across all documents in a single pass, which is impossible if each document is a
separate invocation.

**Dossier-driven audience selection, not an explicit flag.** The command has no `--audiences`
flag. The skill reads the Student Dossier's audience tags (`[teacher]`, `[parent]`) and
generates the appropriate documents automatically. The dossier is the control mechanism.
This keeps the command surface minimal and eliminates the mismatch risk of requesting an
audience the dossier doesn't cover.

**Social Story is optional, not required.** The skill decides whether to include a Social
Story based on the situation brief and dossier (a new transition warrants one; a routine
situation may only need Teacher + Parent guides). We nearly cut the Social Story entirely —
its 10.2 linter was the original moat, but the pack's moat is cross-document coordination,
not any single document's methodology compliance. We kept it because it's the only
teen-facing document, the template and linter were already built, and "optional" lets the
demo show the skill making judgements, not just generating documents.

## Why these are surprising

- A reader would expect an `--audiences` flag. We deliberately chose dossier-driven selection
  to keep the command surface minimal and make the dossier the single source of truth.
- A reader would expect the Social Story to be the core output (it was the original product).
  We demoted it to optional because the pack's moat is coordination, not any single document.

## Consequences

- Adding a new audience (e.g. Employer Guide) means adding a template file and a linter
  checklist — not registering a new skill or changing the command.
- The Social Story template and linter are preserved but no longer the product's centre.
- The demo narrative (identical sentence → contradiction catch) depends on the consistency
  check running across all documents in one pass, which the single-skill architecture enables.
