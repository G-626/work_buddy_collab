# Facial & movement capture layer: descriptive, positive-first, MCP-served

## Context

The session agent loop (ADR-0004) requires a capture layer. The initial sketch proposed MediaPipe "body-language analysis" feeding natural-language output — which risked affective inference ("stress level 7/10"). External review surfaced two constraints that shape this ADR:

1. **Emotional inference from pose/face is unsound for autistic children.** Movement and affect are individual and day-dependent; no classifier reliably maps pose → affect; and practitioners in the room (the judging audience) trust no machine that pretends it can.
2. **Product policy: positive reinforcement only.** Findings must never frame the child negatively — even when results could be read that way. Negative observations become reinforcement/support language or neutral questions.

## Decisions

1. **Capture outputs a Movement Event Stream, not a reading.** The engine emits JSON records `{observed_at, event_type, duration_ms, counts, context}` from a fixed descriptive vocabulary: body primitives (paces, rocks, covers ears/eyes, approaches/withdraws), gaze targets (speaker/task/away via head pose + gaze), voice-adjacent events (talks/laughs cross-referenced with the transcript), and calibrated positive micro-events (smile-like mouth-corner rise, spontaneous initiation). No state labels (tense, distressed, happy, anxious) exist in the schema.
2. **Facial analysis is identity-free and affect-free by default.** Gaze target, head orientation, mouth-open/smile-like events, blink-rate band (fatigue alert-neutral observable, human-reviewed). No face recognition, no identity matching, no stored raw frames — landmark streams only, per-device buffer cleared.
- **Positive-First Rule is a hard rendering constraint.** User-facing output frames all child-related data as support/reinforcement ("Marco completed 4 self-regulation breaks; the mixer briefing kept transitions smooth"). Anything that could read negatively appears only as a neutral observable plus a question routed to the worker — never a verdict.
- **Patterns, not judgments (the "diagnostics" removed).** Cross-session aggregation is descriptive and correlational (pacing cluster aligned with mixer-sound onset; ear-covering 3 → 0 after the 5-minute warning script). These are hypotheses and observations for the professional team — the passport records patterns; clinicians make diagnoses. Surprises route to the worker as questions.
- **WorkBuddy integration: MCP, not folder shuffle.** The Capture Engine ships as a local MCP server (documented: WorkBuddy MCP support with OAuth); WorkBuddy calls it as a tool inside a task. Folder handoff (`sessions/<id>/capture.json`) is the fallback if the MCP path fails on the event device.
- **Transcription is native to the platform:** the Local Whisper skill (on-device) produces the transcript; no audio leaves the device.

## Why these are surprising

- A reader expects the video layer to be the flashy center (emotion detection, live dashboards). We deliberately keep observables-only + positive-first as the product's spine — for this population, confident affective inference is worse than no data.
- A reader expects diagnostics. We explicitly refuse the word and the act: pattern data is evidence for humans, never a machine verdict.

## Consequences

- The passport gains a **Patterns** section (team sensitivity, descriptive counts + trends, weekly review).
- The MVP command surface adds `/passport <id> patterns`.
- The "sponsored usage" story deepens: MCP tool + Local Whisper + Automation + Assistant are all documented platform features the loop depends on.
- Video is not a WorkBuddy-processed format (docs list PDF/DOCX/XLSX/images) — the MCP boundary stays honest: capture on device, WorkBuddy orchestrates, files stay local.
- Demo media always fictional/simulated; no real minor's face ever appears.