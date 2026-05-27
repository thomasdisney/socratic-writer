# Initial Briefing — Socratic Writer Project

**Date**: Project inception (April 2026)

**Purpose**: This file + the documents in `docs/` constitute the complete context required for any future agent or human to continue development without needing the original conversation history.

---

## What We Are Building

An **ultra-minimalist word processor** designed exclusively for serious creative and reflective writing.

The tool's entire reason for existing is to protect and deepen the writer's relationship with their own thoughts. It does this through two tightly coupled mechanisms:

1. **Radical input minimalism** — only continual typing is allowed. Everything else (editing, navigation, formatting, menus, mouse) is deliberately impossible during the writing act.
2. **Socratic LLM reflection** — the only "extra" control is the space bar, which summons a small number of precise, non-directive questions derived strictly from the writer's own recent text. These questions exist to help the writer see the structure, tensions, and implications of what they have already written.

This is not an AI writing tool in the 2025–2026 market sense. It is a thinking tool that happens to use an LLM as a disciplined Socratic partner.

---

## Founding Requirements (Verbatim Spirit)

From the user at project start:

> "i want it to be AN ULTRA minimalist word processor for creative, distraction free writing. there will be an LLM component to provide socratic suggestions of your thoughts and suport proper structing of ideas. the user cannot change anything other than continual typing and the space bar is the only input for extra controll for must have feedback."

These words are the constitution. The `docs/CONSTRAINTS.md` file translates them into enforceable rules.

---

## Workspace Layout (Always Current)

```
/home/demo/socratic-writer/          (real location)
/home/demo/writer -> symlink
~/Desktop/Writer -> symlink

 docs/
  VISION.md                 — why this tool should exist
  CONSTRAINTS.md            — non-negotiable rules (read first when returning)
  INTERACTION-MODEL.md      — the exact proposed UX (most important design doc)
  ROADMAP.md                — phased plan
  DECISIONS.md              — every major choice + rationale
  BRANCHING-STRATEGY.md     — multi-agent branching & PR rules (read when using agents)

context/
  INITIAL-BRIEFING.md       — this file
  SESSION-NOTES-*.md        — create one per major work session

src/                        — future implementation
```

**GitHub**: https://github.com/thomasdisney/socratic-writer (primary remote)

---

## Current State (v0 Demo)

A fully working browser-based prototype exists and is launchable via `launch.py` or the Desktop icon.

- Strict append-only typing enforced in JS (contenteditable with heavy event interception).
- Long-press space (~650ms) triggers Socratic questions in right margin via Grok Build CLI (with heuristic fallback).
- Fast silent autocorrect for 8 common typos.
- Magic commands: sample1/2/3, export, clearall.
- Fully local, privacy-first.

See README.md, QUICKSTART.md, and the app/ for the live experience.

---

## For Future Agents and Contributors

1. Read the docs/ in the order listed in README.md (and AGENTS.md) before touching code.
2. The constraints are the law. Change only with explicit ceremony and update to this briefing.
3. All work must be tested against the keyboard simulator in tests/ before PR.
4. The v0 demo in app/ is the reference feeling to preserve or improve upon.
5. **Multi-agent work**: Follow `docs/BRANCHING-STRATEGY.md` exactly. Use the `branch-manager` skill for all branch operations. Never push to `main` directly.
6. Update DECISIONS.md and this file after any significant change.

---

*This briefing is the handoff. Keep it alive.*
