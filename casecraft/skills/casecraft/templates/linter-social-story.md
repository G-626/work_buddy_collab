# Social Story Linter Checklist

Score the drafted story against every check. Status per check: PASS / FIXED / FLAG.
- **FIXED** = mechanical auto-fix applied; show before → after.
- **FLAG** = needs professional judgement or missing information; do NOT auto-fix.

## A. Methodology (Social Stories 10.2)

| # | Check | Auto-fix |
|---|---|---|
| A1 | Descriptive ≥ 2 × Coaching (Criterion 8 formula: if 0 coaching sentences, use 1 as denominator) | FIXED: convert excess coaching sentences to descriptive, or add descriptive sentences at the relevant point |
| A2 | Coaching sentences use soft verbs ("can try", "might", "one option is") — never "must", "should", "will" | FIXED: soften verb |
| A3 | First- and/or third-person perspective only — never second-person ("you") statements (Criterion 5) | FIXED: rewrite in the dossier's preferred voice |
| A4 | Story answers the relevant WH questions: where, when, who, what (cues), how, why (Criterion 6) | FIXED: add the missing descriptive sentence; FLAG if the fact is missing from brief and dossier |
| A5 | Story has title, introduction identifying the topic, body, and conclusion (Criterion 3) | FIXED: restructure |
| A6 | If the situation is an achievement/skill the student has shown, frame it as applause (Criterion 2: at least 50% of all Stories applaud achievements) | FIXED: reframe; FLAG if unsure whether this is an achievement story |
| A7 | Partial sentences ≤ 2 and clearly marked for completion with the professional | FLAG if > 2 |

## B. Language

| # | Check | Auto-fix |
|---|---|---|
| B1 | No banned vague words: soon, later, maybe, in a bit, a while, a lot | FIXED: replace with concrete time/quantity, or hedge plainly ("Some days… some days…") |
| B2 | No idioms/metaphors/sarcasm/exaggeration | FIXED: literal rewrite |
| B3 | No double negatives | FIXED: rewrite positively |
| B4 | Positive framing: no instruction phrased as "Don't X" / "Stop X" / "Never X" | FIXED: rewrite as the desired action |
| B5 | One idea per sentence; sentences ≤ ~15 words unless reading_level is higher | FIXED: split sentences |
| B6 | Reading level ≤ dossier `reading_level` (estimate by sentence length + vocabulary) | FIXED: simplify; FLAG if unsure |

## C. Register & respect

| # | Check | Auto-fix |
|---|---|---|
| C1 | No babyish tone, cartoon framing, or patronising praise ("What a good boy!") | FIXED: neutral rewrite |
| C2 | Student never described as the problem; no diagnosis/labels mentioned | FLAG any occurrence (serious) |
| C3 | Length within target (150–300 words for one-pager) | FLAG if > 20% over |

## D. Grounding & truth

| # | Check | Auto-fix |
|---|---|---|
| D1 | Every factual claim traces to the situation brief or dossier, OR is hedged ("usually", "typically", "most") | FIXED: hedge; FLAG if the fact is load-bearing and unverifiable |
| D2 | Sensory/trigger content is honest and paired with a concrete coping option from the dossier | FLAG if coping option invented |
| D3 | Names, dates, places spelled exactly as in the brief | FIXED: correct to brief |

## E. Consistency (cross-document)

| # | Check | Auto-fix |
|---|---|---|
| E1 | Language examples (coping scripts, transition cues) are **word-for-word identical** to those in the Teacher Guide and Parent Guide | FIXED: align to the dossier's version; FLAG if the dossier itself is ambiguous |
| E2 | Factual claims (times, names, strategies, coping options) do not contradict any other document in the pack | FLAG any contradiction (Level 1) |
| E3 | Coping options mentioned are consistent with the dossier's "What works" section | FLAG if a strategy appears here that the dossier doesn't mention |

## F. Report format

Output the report as a table: `Check | Status | Detail (before → after, or flag reason)`,
followed by:
- **Assumptions made** (e.g. missing dossier fields)
- **Questions for the reviewer** (facts to confirm with venue/family/school)
- One-line verdict: `Ready for review` / `Needs reviewer input on N item(s)`

## G. Why this linter exists

The most common way practitioners' Social Stories go wrong is not grammar — it is
**criteria drift**: too many directive sentences, second-person commands, vague timing
("soon", "later"), and unverified facts. Research shows fidelity declines without
ongoing support. The linter is the product: it audits every draft against the 10.2
criteria and shows its work, so the professional reviews a story that is already
methodology-compliant instead of auditing a chatbot's plausible-but-drifting draft.
