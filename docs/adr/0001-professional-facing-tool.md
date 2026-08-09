# Professional-facing tool, not teen-facing

## Context

The hackathon theme is "build something for the autism community." The obvious interpretation is a tool for autistic teens themselves. We considered a WorkBuddy skill that teens would operate directly (task decomposition, remote check-ins, scaffold fading).

## Decision

We build for **professionals** (social workers, therapists) who support adolescents with mild-to-moderate ASD, not for the teens directly.

## Why

- **Usability**: WorkBuddy's interface (model configuration, folder authorization, messenger OAuth, credit balances) is too complex for the target teen population, whose core challenge is executive function under ambiguity.
- **Self-report problem**: A teen-facing tool would require the teen to populate their own profile. Written self-expression varies enormously in this population — the tool would work worst for the users who need it most.
- **Consistency**: Professionals produce structured, repeated, clinically informed notes. These become the personalisation source, not the teen's self-report.
- **Scale**: In HK's tiered support model, each school-based worker supports many students. Professional-facing tools scale better.
- **Funder alignment**: The hackathon's charity partner (HK Children & Youth Services) employs these professionals.

## Consequences

- The teen becomes the **beneficiary**, not the operator.
- All outputs are drafts for professional review — human-in-the-loop by design.
- Demo uses fully fictional dossiers; no real minor data is processed.

## Differentiation: what can professionals not already do with a generic chatbot?

A fair challenge: a professional can paste notes into Gemini and get a plausible social story.
CaseCraft must clear a higher bar — value that is **structurally unavailable** to a one-shot chatbot:

1. **Methodology enforcement.** Generic chatbots have no audit trail. Research shows practitioner-made
   materials drift from the Social Stories 10.2 criteria (directive-heavy sentences, second-person
   commands, vague timing) and that fidelity declines without ongoing support. Our linter checks every
   draft against the criteria, auto-fixes mechanical violations, and shows its work — the professional
   reviews compliance, not just prose.
2. **Longitudinal grounding.** The dossier + story library accumulate: voice, scripts, facts, and
   reading level stay consistent across months of materials, and stories applaud past achievements
   (Criterion 2). A chatbot conversation starts from zero every time.
3. **Local file execution + batch differentiation.** One brief → N personalised outputs, filed and
   indexed per student. In a chatbot, the professional re-pastes every dossier by hand, every time.

Features that do NOT clear this bar (a chatbot replicates them trivially) are cut or deferred:
`/casenote` and `/parentupdate` are thin wrappers over a prompt.
