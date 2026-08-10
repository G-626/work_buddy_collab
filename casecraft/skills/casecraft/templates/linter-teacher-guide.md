# Teacher Guide Linter Checklist

Score the drafted Teacher Guide against every check. Status per check:
PASS / FIXED / FLAG.
- **FIXED** = mechanical auto-fix applied; show before → after.
- **FLAG** = needs professional judgement or missing information; do NOT auto-fix.

## A. Language

| # | Check | Auto-fix |
|---|---|---|
| A1 | No jargon: "executive function", "sensory processing", "stimming", "dysregulation", "co-morbid" | FIXED: replace with plain language |
| A2 | No diagnosis language: no mention of autism, ASD, or any clinical label | FIXED: remove; FLAG if the sentence loses meaning without it |
| A3 | Positive framing: no instruction phrased as "Don't X" / "Stop X" / "Never X" | FIXED: rewrite as the desired action |
| A4 | Short sentences: ≤ ~15 words per sentence | FIXED: split sentences |
| A5 | Concrete actions: no vague principles ("be patient", "be flexible", "show understanding") | FIXED: replace with a specific action from the passport |

## B. Boundary (blocking)

| # | Check | Auto-fix |
|---|---|---|
| B1 | `[open]` sections only: no content that traces to `[team]` or `[clinical]` passport sections | FLAG — blocking. Sensitivity leak. The passport has no `[teacher]`/`[parent]` tags — tags are `[open]`/`[team]`/`[clinical]` |
| B2 | No affect labels / internal-state claims ("may feel anxious" → "may go quiet, stop participating") | FIXED: rewrite as observable |

## C. Content

| # | Check | Auto-fix |
|---|---|---|
| C1 | All 8 sections present: Header, Snapshot, What to expect, What helps, What to avoid, Language to use, Warning signs, Escalation plan | FLAG for each missing section |
| C2 | "What to expect" grounded in passport `[open]` sections only | FLAG if content from restricted sections appears |
| C3 | "What helps" contains only classroom-feasible actions (no one-to-one support, no specialist equipment the school doesn't have) | FLAG if an action requires resources the school doesn't have |
| C4 | "Warning signs" describes observable behaviour, not internal states | FIXED: rewrite as observable |
| C5 | Fits on one page when printed | FLAG if clearly over one page |

## D. Consistency (cross-document)

| # | Check | Auto-fix |
|---|---|---|
| D1 | Language examples (coping scripts, transition cues) are **word-for-word identical** to those in the Parent Report and Social Story (if generated) | FIXED: align to the passport's version; FLAG if the passport itself is ambiguous |
| D2 | Factual claims (times, names, strategies, coping options) do not contradict any other document in the pack | FLAG any contradiction (Level 1) |
| D3 | No strategy recommended here that the passport's "What works" section contradicts | FLAG |

## E. Report format

Output the report as a table: `Check | Status | Detail (before → after, or flag
reason)`, followed by:
- **Assumptions made** (e.g. missing passport fields)
- **Questions for the reviewer** (facts to confirm with school/family)
- One-line verdict: `Ready for review` / `Needs reviewer input on N item(s)`
