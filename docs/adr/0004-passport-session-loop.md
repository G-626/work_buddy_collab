# Passport-as-source-of-truth + session agent loop

## Context

ADR-0003 established the Coordinated Support Pack: per-event documents coordinated by the linter. Review of the architecture found the core weakness: **per-event documents die.** Each pack is generated, shared, and filed — nothing accumulates. The professional still re-types history in every prompt, and consistency is only *per-pack*, not *per-student over time*.

Additionally, the person's earlier design sketch ("audio + MediaPipe + transcription → NL → WorkBuddy skill → summary → passport → UI") raised two risks that shaped this ADR: (a) claiming emotional inference from pose data is medically unsound for autistic children and would collapse under practitioner scrutiny; (b) auto-injecting raw session output into a living document erodes trust faster than no automation.

## Decision

1. **The Student Passport is the product.** One living, versioned, per-student document holds truth; the Coordinated Support Pack and role views derive from it. The former "Student Dossier" is absorbed and upgraded (sections, audience/sensitivity tags, versioning, freshness).
2. **The agent loop powers the passport:** session goal → capture (worker device) → observables-only synthesis → WorkBuddy skill ingestion → 90-second review gate → passport delta → stakeholder views.
3. **Observables only.** The capture layer produces verifiable events (quotes, counts, timestamps) and never emotional/clinical inference. These are what the model and the passport are allowed to record.
4. **Human-in-the-loop by default.** No summary merges into the passport without the worker's approval via the Review Gate. Auto-commit is off by design.
5. **Sensitivity leak checking joins the linter.** Passport sections are tagged `[open]/[team]/[clinical]`; views that must not contain clinical detail (parent/teacher/student-facing) are checked by the linter, FLAG→FAIL for leaks.
6. **Consent & media are handled explicitly.** Recording requires parental consent (HK PDPO posture), retention/delete rules apply, and demo media is always fictional/simulated — never a real minor's audio/video. ADR-0002's "wait for judges to ask" posture is upgraded to proactive for anything touching recording.

## Why these are surprising

- The reader would expect flashy video analysis and emotion detection at the center. We deliberately keep **observables-only** as the hard boundary — for this population, inferred emotion is worse than no data: it produces confident, wrong passport entries.
- The reader would expect the demo to be the generation pipeline. The demo instead is the *leak check* and the *freshness flag* — the system catching its own problems, file-verified.

## Consequences

- Capability test T8 (cross-session file read) and T10 (template substitution) become load-bearing: the loop depends on WorkBuddy reading past files between sessions.
- The ingestion step up: `/session` (was "Case Note", cut in ADR-0001) is now the highest-value command; `/casenote` raw-text mode is roadmap, not a thin wrapper.
- The passport must be authored and versioned for a real pilot-without-code-change (Pilot Readiness).
- Demo beats fixed: (1) identical-script check across views with a deterministic file search; (2) planted sensitivity leak → blocking FLAG; (3) freshness flag on a stale section; (4) batch `--students` with one goal. 2–3 fictional dossiers (Marco, Priya, + a third) with simulated session assets.