# Command: /socialstory

## Usage

```
/socialstory <student-id> "<situation brief>" [voice=first|third] [format=pdf-onepager|pdf-multipage|markdown-only] [language=en|zh]
/socialstory batch "<situation brief>" --students <id1,id2,...>
```

## What it does

Invokes the `socialstory` skill (skills/socialstory/SKILL.md): loads the student's dossier,
drafts a methodology-compliant Social Story, lints it, generates the staff/parent companion
one-pager, saves all outputs under `students/<id>/stories/`, and returns the draft +
linter report for professional review.

## Examples

```
/socialstory marco "First work-experience placement at Sunbeam Bakery next Tuesday 19 Aug,
9:00–15:30. Travel by MTR Jordan to Mong Kok, Exit B2. Supervisor is Mrs. Chan. Jobs:
bagging rolls, labelling boxes. Kitchen is warm and the mixers are loud."
```

```
/socialstory marco "Class picnic at Kowloon Park on Friday 12 Sep, 12:00–14:00" voice=third
```

```
/socialstory batch "First day of work experience next week" --students marco,jason,priya
```

## Response shape

1. Story title + full story text
2. Linter report (table + assumptions + questions for reviewer)
3. Companion one-pager text
4. Saved file paths
5. Closing line: "Draft for your review — please edit before use with the student."
