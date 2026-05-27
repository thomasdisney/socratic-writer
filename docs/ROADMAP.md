# Development Roadmap — Socratic Writer

This roadmap is deliberately coarse. We will refine it after each phase based on what we learn from actually using the thing.

## Phase 0 — Workspace & Foundations (Current)

**Goal**: Create a durable, self-documenting project home that survives context loss.

**Completed**:
- Project directory + symlinks (`~/writer`, Desktop/Writer)
- `docs/VISION.md`, `CONSTRAINTS.md`, `INTERACTION-MODEL.md`
- This roadmap
- Initial `README.md`

**Next in this phase**:
- `docs/DECISIONS.md` (record every significant choice with rationale)
- `context/INITIAL-BRIEFING.md` (this document + conversation summary for future agents)
- Choose a working project codename if we want something shorter than "Socratic Writer"

---

## Phase 1 — Core Writing Surface (No LLM Yet)

**Goal**: Prove the radical input model feels good for long writing sessions.

**Deliverables**:
- A running application that opens to a beautiful, full-screen writing surface
- Pure append-only typing with all other keys disabled
- Excellent typography and vertical rhythm
- Automatic local saving (plain text + timestamped snapshots)
- Zero visual elements except the text itself
- Space bar does **something visible and intentional** (even if it just inserts a special marker or does nothing yet)

**Success criteria**:
- A person can write for 90+ minutes without once reaching for the mouse or feeling the urge to edit.
- The experience feels "expensive" and high-quality in a quiet way (like a good fountain pen).

**Tech exploration** (do not commit yet):
- Terminal / TUI (ratatui, blessed, custom raw mode)
- Web (Tauri + webview, or pure browser with File System Access API)
- Native (SDL, wgpu, or even a custom Wayland client on Linux)

**Duration estimate**: 1–3 focused sessions to a usable prototype.

---

## Phase 2 — The Space Bar Contract

**Goal**: Implement the single meta-action cleanly and test multiple trigger mechanisms.

**Deliverables**:
- At least two different space-bar trigger prototypes (e.g., long-press vs. paragraph-end + space)
- The trigger must be reliable, non-accidental, and feel good
- When triggered, the system must acknowledge without any "loading" theater
- The writer can keep typing at full speed while "something" is happening

**Key experiment**: Does the writer actually use the space bar? How often? Does it break flow or enhance it?

---

## Phase 3 — Minimal Socratic LLM Integration (In Progress)

**Goal**: First real value from the AI component.

**Deliverables** (partially complete):
- Local LLM support via Ollama + same-origin proxy in the launcher (demo works today)
- A tightly engineered system prompt (v0 in `prompts/`, tightened version live) that produces only Socratic questions
- Questions appear in the margin exactly as before; the writer continues typing completely unaffected
- Full async + timeout + silent fallback to the heuristic

**Remaining**:
- Real usage data + prompt iteration
- Model selection / persistence
- Move to sidecar when we pick a native stack

**Evaluation**:
- Do the questions actually cause useful reflection?
- Are they ever annoying or off-topic?
- Does the writer ever want to "answer" them directly in the text?

---

## Phase 4 — Polish, Durability & Review Modes

**Goal**: Make the tool something a serious writer would actually adopt for weeks.

**Possible work** (only after Phase 3 proves the concept):
- Multiple named writing threads / notebooks with fast but deliberate switching
- A true "review" mode (read-only, lightly structured view of previous writing)
- Export as clean Markdown or plain text (deliberate, separate ritual — not during flow)
- Subtle visual indication of "depth" or time spent (only in review mode)
- Extremely careful handling of very long sessions
- Crash recovery that feels invisible

---

## Phase 5 — Advanced Socratic Features (Only If Earned)

These are **not** planned yet. They are listed only to show the direction we might go after real usage data.

- Multi-pass reflection (the model looks at your answers to its previous questions)
- Theme / motif extraction over long writing
- Gentle structural visualization (in review mode only)
- "Conversation with your past self" — feeding old sessions back as context
- Writer-controlled fine-tuning or memory of what kinds of questions help *this* person

**Rule**: No feature in this phase is started until at least 5–10 writers have used Phases 1–4 for real work and asked for something.

---

## Guiding Principles for All Phases

1. **Build the smallest possible thing that lets us test the next assumption.**
2. **Use it yourself for real writing before asking anyone else to.**
3. **When something feels even 5% wrong, stop and redesign the interaction before writing more code.**
4. **Document the "why" of every decision the moment it is made.**
5. **The constraints document is the constitution. Change it only with ceremony.**

---

## Current Open Questions (Highest Priority First)

1. What is the exact space bar trigger mechanism? (Long press? Paragraph + space? Other?)
2. What technology stack gives us the best shot at true zero-latency typing + clean background LLM work?
3. Should the main writing surface ever show *any* UI at all (even a single-pixel breathing indicator)?
4. How do we handle the very first launch experience (first-time writer has no text — what does space do?)?
5. Is there ever a legitimate reason to allow limited editing, or does that path lead to ruin?

These questions will be answered through prototypes, not meetings.

---

*This roadmap is a living document. Update it after every phase rather than letting it become fiction.*
