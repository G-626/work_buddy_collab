# Parent Report Linter Checklist

Score the drafted Parent Report against every check. Status per check:
PASS / FIXED / FLAG.
- **FIXED** = mechanical auto-fix applied; show before → after.
- **FLAG** = needs professional judgement or missing information; do NOT auto-fix.

## A. Language

| # | Check | Auto-fix |
|---|---|---|
| A1 | Warm but not condescending: no clinical distance ("the student exhibits…"), no over-familiarity ("your little one…") | FIXED: rewrite in partner register |
| A2 | Plain language: no jargon; technical terms defined in brackets | FIXED: simplify or define |
| A3 | No diagnosis language: no mention of autism, ASD, or any clinical label | FIXED: remove; FLAG if the sentence loses meaning without it |
| A4 | Positive framing: no instruction phrased as "Don't X" / "Stop X" / "Never X" | FIXED: rewrite as the desired action |
| A5 | Short sentences: ≤ ~15 words per sentence | FIXED: split sentences |
| A6 | Reading level ~age 12 (or passport's stated level): no multi-clause sentences | FIXED: simplify |

## B. Boundary (blocking)

| # | Check | Auto-fix |
|---|---|---|
| B1 | `[open]` sections only: no content that traces to `[team]` or `[clinical]` passport sections | FLAG — blocking. Sensitivity leak. The passport has no `[parent]` tag — tags are `[open]`/`[team]`/`[clinical]` |
| B2 | No "goal progress" wording that implies clinical assessment — use "what we're working on" framing | FIXED: rephrase |

## C. Content

| # | Check | Auto-fix |
|---|---|---|
| C1 | All 9 sections present: Header, Overview, What we're working on table, What went well, Home strategies, Same words at home, What to watch for, Next session focus, Contact | FLAG for each missing section |
| C2 | "What we're working on" table rows have evidence in the Evidence column (counts/quotes/observables) — no status without evidence | FLAG if evidence column empty |
| C3 | "Home strategies" contains only home-feasible actions | FLAG if an action requires school resources |
| C4 | "What to watch for" describes observable signs, not internal states | FIXED: rewrite as observable |
| C5 | Fits on 1–2 pages | FLAG if clearly over 2 pages |

## D. Consistency (cross-document)

| # | Check | Auto-fix |
|---|---|---|
| D1 | "Same words at home" examples are **word-for-word identical** to those in the Teacher Guide and Social Story (if generated) | FIXED: align to the passport's version; FLAG if the passport itself is ambiguous |
| D2 | Factual claims (times, names, strategies, coping options) do not contradict any other document in the pack | FLAG any contradiction (Level 1) |
| D3 | Goal statuses do not contradict the Therapist Summary version (may be less detailed, never opposite) | FLAG on contradiction |
| D4 | No strategy recommended here that the passport's "What works" section contradicts | FLAG |

## E. Report format

Output the report as a table: `Check | Status | Detail (before → after, or flag
reason)`, followed by:
- **Assumptions made**
- **Questions for the reviewer**
- One-line verdict: `Ready for review` / `Needs reviewer input on N item(s)`
