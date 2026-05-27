# Hard Constraints — Socratic Writer

These constraints are **non-negotiable**. They come directly from the founding requirements and define the soul of the tool. Any design or implementation decision that violates these must be rejected.

## 1. Ultra-Minimalist Input Model

**The user may only perform two actions while writing:**

1. **Continual typing** — normal character input that extends the text.
2. **Pressing the space bar** — the single, deliberate action that requests "must-have feedback."

No other keys, no combinations, no mouse, no trackpad, no gestures, no menus, no command palette during the writing session.

This means:
- No backspace / delete
- No arrow keys or cursor movement
- No enter/return for new paragraphs? (TBD — may be allowed as part of "typing")
- No tab, escape, function keys
- No Ctrl/Cmd anything
- No right-click context menus

**Rationale**: Any additional control creates decision points and muscle memory that pulls the writer out of pure thought. The space bar is the only "extra" because it is the only action that serves the higher-order goal of better thinking.

## 2. No Editing of Existing Text

The writer **cannot change anything** they have already written within a session.

- No deleting previous words
- No rewriting sentences
- No moving paragraphs
- No formatting changes (bold, italic, headings, etc.)

This is an append-only writing surface during active creation.

**Narrow exception — Fast silent autocorrect**:
A tiny, hardcoded, synchronous map of the most common muscle-memory typos (e.g. "teh" → "the") may be applied *automatically and invisibly* the moment the writer types a word boundary after the typo. No UI, no choice, no highlight, no latency. The writer never sees the error or the correction step. This is the only form of "correction" permitted on the primary writing surface.

**Rationale**: After real use, the inability to correct the 5–10 most universal fast-typing slips was reported as a material distraction from forward flow. Because the corrections are (a) extremely high-precision, (b) require zero decision or action from the writer, and (c) cost zero time or attention, they preserve the "no decision fatigue" and "pure forward momentum" goals while removing a small but real source of friction.

All other forms of spell/grammar assistance, suggestion, or visible correction remain forbidden.

## 3. Space Bar as the Sole Meta-Control

The space bar must be:
- The **only** way to summon the LLM / Socratic component
- The **only** way to request any form of system feedback during writing
- Deliberate and slightly effortful (not accidental)

Possible interpretations (to be resolved in interaction model):
- Single space at end of thought
- Double-space (or space-space)
- Holding space for a duration
- Space when at the end of a paragraph (detected by two newlines or similar)

The exact trigger must feel intentional and rare — not something that fires every time you naturally hit space between words.

## 4. Distraction-Free Mandate

Nothing in the interface may ever:
- Move on its own (no auto-scrolling animations that call attention)
- Make sounds
- Show notifications, badges, or "AI is thinking..." spinners that break presence
- Display word counts, time counters, or progress metrics during writing
- Offer suggestions uninvited

The Socratic suggestions, when they appear, must be **glanceable but ignorable**. The writer must be able to continue typing without acknowledging them.

## 5. LLM Role Is Strictly Socratic

The model may **never**:
- Generate prose on behalf of the writer
- Offer direct content suggestions ("you should write about X")
- Perform line edits or rewrites
- Act in a coaching or "helpful assistant" tone that flatters or directs

The model **must**:
- Ask questions
- Identify implicit structures, contradictions, or underdeveloped threads
- Use the writer's own words as the sole source material
- Stay in the background unless explicitly summoned

## 6. No Feature Creep Allowed

The following features are **explicitly out of scope forever** unless the constraints document is formally revised:

- Multiple documents / project management
- Tagging, folders, search
- Export options during writing (export is a separate, later ritual)
- Themes, fonts, or appearance settings while writing
- Collaboration or sharing
- Mobile support (this is a deep-work desktop tool)
- "AI rewrite this paragraph" buttons
- Grammar checking, spell checking, or suggestions that interrupt or require attention
- Version history browser (the text itself is the history)

## 7. Performance & Reliability

- The writing surface must feel **instant** — zero perceptible latency on keystrokes even when the LLM is processing in the background.
- The tool must work completely offline for the writing act itself (LLM may be local or cached).
- Crashes must never lose the current writing session.

## 8. Privacy & Data

- The writer's text is never sent anywhere without explicit, per-invocation consent via the space bar action.
- No telemetry, analytics, or "improve the product" data collection.
- Local model support is a first-class requirement (Ollama, llama.cpp, etc.).

---

## Enforcement

When in doubt during design or implementation:

> "Does this increase the writer's ability to stay in pure, forward-moving thought?"

If the answer is not a clear yes, the feature or interaction is rejected.

These constraints will be reviewed only after a working prototype exists and real writers have used it for multiple sessions.
