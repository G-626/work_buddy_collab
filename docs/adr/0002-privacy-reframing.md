# Privacy reframing: secure by design, not local processing

## Context

Initial pitch assumed WorkBuddy's "sandboxed execution" and "local file operations" meant data never leaves the user's machine. Verification of the privacy policy revealed otherwise.

## Decision

We **do not claim** that data stays local. Instead, we frame privacy as **"secure by design"**: human-in-the-loop review + pseudonymisation guidance.

## Why

- **Privacy policy reality**: Inputs are processed by third-party LLMs, stored remotely for up to 14 days, and transferred to Singapore/PRC.
- **Cannot overclaim**: Saying "local data stays local" would be false and would collapse under judge scrutiny.
- **Defensible alternative**: Many clinical AI tools operate this way. The safeguard is professional review, not data residency.

## Mitigation guidance

- Professionals use pseudonyms or initials in prompts.
- Full identifiers stay in local dossier files only.
- We wait for judges to ask about privacy rather than proactively raising it.

## Consequences

- The pitch emphasises time savings and professional judgement, not data residency.
- We accept the risk that judges may probe this; we have a prepared answer.
