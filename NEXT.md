# What To Do Next

**v0 demo is live and running.** Use it before planning anything else.

## Current Reality

We have a complete, beautiful, constraint-respecting writing app you can use right now:

- Launch with the Desktop icon or `python3 ~/writer/launch.py`
- Strict append-only (no backspace, no arrows, no *manual* editing)
- **Fast silent autocorrect** for 8 common fast-typing typos (teh→the, adn→and, etc.) — completely invisible, fires on word boundaries
- Hold **space** ~650ms at the end of a thought → real Socratic questions in the margin
- Works completely offline with a strong local generator
- Type `sample1` + hold space for instant demo content

## What Must Happen Now

**Use the tool for real writing** (minimum 25–40 minutes across sessions).

Only after you have felt it in your body should we decide what changes.

The highest-leverage questions right now are experiential, not technical:

- Did the long-press space feel like the correct "deliberate" gesture?
- Did any question actually make you see your own writing differently?
- What (if anything) pulled you out of pure flow?
- Do you want the questions to appear differently (inline, different contrast, etc.)?

## After You Have Used It

We will decide together on the next concrete step:

- Refine the space bar contract
- Wire up a real local LLM (Ollama) behind the exact same trigger
- Make the surface even more radically minimal
- Start a native version (Tauri or terminal)

### Option B — Choose Technology Stack
We cannot make progress on the writing surface until we know what we're rendering into.

**Key evaluation criteria** (in order):
1. Can keystrokes appear on screen with < 16ms perceived latency?
2. Can we run a local LLM in a background thread/process without ever blocking the input loop?
3. Can we produce a truly blank, high-quality typographic experience with minimal code?
4. Is local-first persistence trivial?

**Stacks worth serious investigation**:
- Rust + ratatui (or custom crossterm raw mode) — strong candidate for minimal latency
- Tauri v2 + a minimal webview (Svelte or vanilla) — good balance, easy LLM integration via sidecar
- Pure browser + File System Access API + local WebLLM or Ollama fetch — zero install, but harder to lock down input
- Native (SDL2 + freetype or wgpu text) — maximum control, maximum work

### Option C — Write the First Socratic Prompt
Even before we have a UI, we can (and should) craft the system prompt that will enforce the Socratic contract.

**Deliverable**: A `prompts/socratic-reflector.txt` file containing:
- Strict role instructions
- Output format constraints (only questions, no statements)
- Few-shot examples of good vs bad responses
- Rules for scope (only use the writer's own recent text)

This prompt will be one of the most important artifacts in the entire project.

---

## Current Recommendation

**Start with Option A (Space Bar trigger) + Option C (Prompt) in parallel.**

The trigger mechanism is a pure interaction problem that does not require a full app. The prompt is a pure language problem that also does not require a full app. We can make real progress on both in a single session without committing to a stack yet.

Once we have a winner for the trigger and a strong first prompt, the stack decision becomes much easier because we will know exactly what behaviors we need to support.

---

## How to Mark Progress

1. When you complete an experiment or decision, append a new entry to `docs/DECISIONS.md`.
2. Update `docs/ROADMAP.md` with what was learned.
3. Create a new `context/SESSION-NOTES-YYYY-MM-*.md` file.
4. Update this `NEXT.md` file so the next person always has a clear on-ramp.

---

**Latest addition**: Fast silent autocorrect (see DECISIONS.md for the full rationale and the precise carve-out in CONSTRAINTS.md §2).

---

*Keep this file short. The deep thinking belongs in the docs/ folder.*
