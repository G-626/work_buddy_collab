# Teacher Guide Linter Checklist

Score the drafted Teacher Guide against every check. Status per check: PASS / FIXED / FLAG.
- **FIXED** = mechanical auto-fix applied; show before → after.
- **FLAG** = needs professional judgement or missing information; do NOT auto-fix.

## A. Language

| # | Check | Auto-fix |
|---|---|---|
| A1 | No jargon: "executive function", "sensory processing", "stimming", "dysregulation", "co-morbid" | FIXED: replace with plain language |
| A2 | No diagnosis language: no mention of autism, ASD, or any clinical label | FIXED: remove; FLAG if the sentence loses meaning without it |
| A3 | Positive framing: no instruction phrased as "Don't X" / "Stop X" / "Never X" | FIXED: rewrite as the desired action |
| A4 | Short sentences: ≤ ~15 words per sentence | FIXED: split sentences |
| A5 | Concrete actions: no vague principles ("be patient", "be flexible", "show understanding") | FIXED: replace with a specific action from the dossier |

## B. Content

| # | Check | Auto-fix |
|---|---|---|
| B1 | "What to expect" grounded in dossier `[teacher]`-tagged sections only | FLAG if content from untagged sections appears |
| B2 | "What helps" contains only classroom-feasible actions (no one-to-one support, no specialist equipment the school doesn't have) | FLAG if an action requires resources the school doesn't have |
| B3 | "Warning signs" describes observable behaviour, not internal states ("may feel anxious" → "may go quiet, stop participating") | FIXED: rewrite as observable |
| B4 | Length within target (200–350 words) | FLAG if > 20% over |

## C. Consistency (cross-document)

| # | Check | Auto-fix |
|---|---|---|
| C1 | Language examples (coping scripts, transition cues) are **word-for-word identical** to those in the Parent Guide and Social Story (if generated) | FIXED: align to the dossier's version; FLAG if the dossier itself is ambiguous |
| C2 | Factual claims (times, names, strategies, coping options) do not contradict any other document in the pack | FLAG any contradiction (Level 1) |
| C3 | No strategy recommended here that the dossier's "What works" section contradicts | FLAG |

## D. Report format

Output the report as a table: `Check | Status | Detail (before → after, or flag reason)`,
followed by:
- **Assumptions made** (e.g. missing dossier fields)
- **Questions for the reviewer** (facts to confirm with school/family)
- One-line verdict: `Ready for review` / `Needs reviewer input on N item(s)`
