# Decision Log — Socratic Writer

**Purpose**: Every significant architectural, design, or scope decision is recorded here the moment it is made, with date, rationale, and alternatives considered. This prevents re-litigation and preserves institutional memory.

**Format**:
```
## [YYYY-MM-DD] Decision Title

**Decision**: One-sentence summary of what was chosen.

**Context**: Why this decision was needed now.

**Rationale**: The reasoning (constraints, evidence, trade-offs).

**Alternatives Considered**:
- Option A — why rejected
- Option B — why rejected

**Revisit Trigger**: What future evidence would cause us to reconsider?
```

---

## 2026-04-?? Workspace Initialization

**Decision**: Project home is `~/socratic-writer` with convenient symlinks at `~/writer` and `~/Desktop/Writer`.

**Rationale**: User explicitly requested "a workspace that i can easily access." Symlinks give both terminal and GUI one-click access without forcing the user to remember a long path. The full name in the real directory makes the purpose obvious to future explorers.

**Alternatives**: Single directory in Documents, or a hidden `~/.socratic-writer`. Rejected because discoverability and easy backup matter more than hiding.

---

## 2026-04-?? Strict Append-Only Model

**Decision**: During active writing sessions, the application is strictly append-only. No backspace, no cursor movement, no deletion or rearrangement of existing text is possible.

**Rationale**: Directly derived from the founding constraint "the user cannot change anything other than continual typing." This is the single most powerful protection against the perfectionism that destroys creative flow. It is also what makes the tool philosophically distinct from every mainstream writing application.

**Alternatives Considered**:
- Allow backspace within the current paragraph only — rejected because it creates a slippery slope and "just this once" editing behavior.
- Soft "warning then allow" model — rejected; any path to editing reintroduces the entire problem the tool exists to solve.

**Revisit Trigger**: Real writers who have used the tool for 10+ hours of serious work report that the inability to correct obvious typos is actively harming their output or willingness to use it. Even then, we would first try "review mode editing" before touching the primary writing surface.

---

## 2026-04-?? Space Bar as Sole Meta-Action

**Decision**: The space bar (in one of its special forms) is the single and only way for the writer to request Socratic feedback during a writing session. No other key, gesture, or UI element may trigger LLM interaction.

**Rationale**: Matches the explicit requirement that "the space bar is the only input for extra control for must have feedback." Having one and only one door into the AI component is what keeps the rest of the experience radically simple and forces the AI to earn its place.

**Alternatives Considered**:
- A dedicated "think" key (F1 or similar) — rejected because it violates the "only space bar" rule and adds another thing to remember.
- Voice trigger or special chord — rejected for adding complexity and hardware assumptions.

**Revisit Trigger**: User testing shows that writers want a second, different kind of feedback that cannot reasonably be collapsed into the Socratic questioning model.

---

## 2026-04-?? No Uninvited AI Behavior

**Decision**: The LLM component is 100% passive until the space bar trigger. It never auto-analyzes, never offers suggestions, never highlights text, never shows progress indicators that call attention to itself.

**Rationale**: Any proactive AI behavior would violate the "distraction-free" and "user cannot change anything other than continual typing" constraints at the deepest level. The writer must remain the sole author of both the text and the decision to reflect.

**Alternatives Considered**:
- Gentle background analysis with optional "nudge" — rejected; even optional nudges become cognitive load.
- "AI is ready" subtle indicator — rejected; the writer should not be thinking about the AI's state at all.

---

## 2026-04-?? Fast Silent Autocorrect for Common Typos

**Decision**: Add a tiny, synchronous, invisible "fast autocorrect" pass that silently replaces a curated list of 8 high-confidence common typos (teh/the, adn/and, taht/that, etc.) the instant the writer types a word boundary after them. No UI, no confirmation, no visible indication ever.

**Context**: The strict append-only model (see prior decision) intentionally removed all editing. After the v0 demo saw real writing use, the friction of leaving obvious fast-typing slips on the page became a measurable drag on the "pure forward momentum" experience the tool is built to protect.

**Rationale**:
- The change directly addresses the documented "Revisit Trigger" in the Strict Append-Only decision.
- By limiting the feature to (1) a tiny static Map, (2) only the most universal non-ambiguous typos, (3) fully automatic application at word boundaries, and (4) zero cognitive or motor cost, we preserve the spirit of "the writer never reaches for the mouse or makes a decision about correction."
- It is "fast" in every sense: O(1) lookup, synchronous, no network, no LLM, imperceptible cost on the input path.
- This is deliberately *not* spell-checking, grammar, style, or "suggestions." It is normalization of a handful of near-universal mechanical errors.

**Alternatives Considered**:
- Full review-mode editing later — still planned, but does not solve the in-flow distraction of watching your own typos stay on the page.
- Browser's built-in spellcheck/autocorrect — rejected; it introduces visible UI, decision points, and is not under our control or consistent.
- Visible "did you mean" underline + accept — complete violation of the no-interruption and no-decision rules.
- Doing nothing — rejected after actual use showed the pain was real enough to warrant a minimal carve-out.

**Constraints Updated**: Section 2 of CONSTRAINTS.md now explicitly permits this narrow automated, silent, high-precision exception while keeping every other form of correction forbidden.

**Implementation Notes**:
- Correction only fires for exact all-lowercase matches of the 8 tokens.
- Applied on word-terminating characters (space, newline, punctuation) and on trailing word when reflection/export is requested.
- The Python simulator and hidden test harness must be kept in sync.
- The list is intentionally small and will not grow without ceremony.

---

## 2026-04-?? First Real LLM Hookup for Socratic Questions (Phase 3 start)

**Decision**: Wire the existing long-press space trigger to a real local LLM (Ollama) for question generation while preserving every constraint. The LLM path is fully asynchronous, non-blocking, and falls back silently + instantly to the proven local heuristic when the model is unavailable or returns weak output.

**Context**: The v0 demo proved the input model and the space-bar contract. The heuristic questions were surprisingly good, but the roadmap and multiple docs explicitly called for "Minimal Socratic LLM Integration" as the next real value step. The user requested "hook up llm to demo for question generation."

**Rationale** (constraint-respecting):
- The trigger remains 100% the deliberate long space bar (no new UI, no auto-analysis).
- While the model thinks the writer continues typing with zero visible cost (AbortController + in-flight cancellation on new triggers).
- Zero new visual elements during the wait — only the same gentle status toast that already existed.
- The system prompt (tightened from `prompts/socratic-reflector-v0.md`) + post-processing enforces "only questions, max 3, traceable to the writer's words".
- Same-origin proxy in launch.py removes all CORS pain for the demo and keeps the browser code simple.
- Heuristic is never removed — it is the reliable, instant, offline fallback. LLM is an enhancement, not a requirement.
- Model choice defaults to a small, fast, instruction-tuned local model (`phi3:mini`).

**Technical choices (updated)**:
- Same-origin POST /api/reflect proxy in launch.py now invokes the local Grok Build CLI (`grok --single ... --output-format plain --permission-mode bypassPermissions --no-memory --no-plan`) instead of any local model.
- No Ollama / local LLMs are used at all.
- Smart recent-text windowing (last 2–3 paragraphs, ~1400 char cap).
- Strict prompt + defensive line parsing in the proxy.
- The browser JS and user experience are unchanged — the heuristic fallback is still perfect when the CLI is unavailable.

**Alternatives Considered**:
- Direct browser fetch to Ollama (CORS pain for normal users) — rejected for demo experience.
- WebLLM / in-browser model — too heavy for v1, kills the "tiny" feel, and still requires download.
- Streaming tokens into the margin — beautiful but violates "no movement that calls attention" and the "background event" rule.
- Making the LLM the only source — rejected; the tool must remain fully usable with zero external dependencies.

**Constraints & Interaction Model upheld**:
- Space bar is still the sole meta-action.
- No uninvited AI behavior.
- Typing latency remains zero.
- LLM role remains strictly Socratic (enforced in prompt + client filter).
- Privacy: everything stays on the user's machine.

**Next natural steps** (not implemented yet):
- Prompt iteration based on real sessions using Grok via the CLI.
- Possibly expose model choice later (different Grok variants if the CLI supports them).
- Move the generation call into a proper sidecar / native process in future stacks.

**Amendment (same session)**: Explicit user direction — NO local models (Ollama etc.). All LLM question generation must go through the Grok Build CLI. The proxy was rewritten to `subprocess` the `grok` binary. The rest of the architecture (async, fallback, same trigger, zero UI noise) remains identical.

---

## 2026-05-26 Hyperminimalism UI Enhancement for Socratic Writer (Design ID 5ac1b8e3)

**Decision**: Land the hyperminimalism UI enhancement design document and execute its PR Plan (6 sequenced PRs behind HYPERMINIMAL flag with mandatory real-writing validation gate).

**Context**: v0 demo use revealed persistent micro-chrome in `app/socratic-writer.html` (header + live metrics, 280px labeled sidebar, blinking end-marker, placeholder, etc.) that violated the hyper interpretation of VISION ("the interface must disappear") and CONSTRAINTS §4 (zero visual clutter, no word counts/metrics during writing, no auto-moving elements).

**Rationale**: The design (produced via full design-doc-writer/reviewer loop to 0 open issues) proposes only deletions + one minimal transient question block (label-free, low-opacity, flow-sibling, recedes naturally per explicit no-auto-scroll Viewport & Scroll Contract). All 8 Key Decisions and the implementation plan rigorously preserve the append-only contract, space-bar sole meta-action, non-blocking Socratic behavior, and "pure forward-moving thought" litmus test. Net reduction of ~150-220 LOC in the reference HTML.

**Alternatives Considered**:
- Keep thin persistent gutter or bottom overlay — rejected for introducing permanent visual weight or overlap risks.
- More aggressive removal of Socratic questions themselves — rejected; violates VISION/INTERACTION-MODEL contract for the one allowed meta-action feedback.

**Revisit Trigger**: Real writers using the hyperminimal surface for 10+ hours report that any remaining element (e.g. the transient block or lack of visual anchor) measurably harms flow or discoverability of the space bar.

**References**: Full design at `docs/HYPERMINIMALISM-UI-ENHANCEMENT.md` (includes PR Plan, Mermaid diagrams, before/after code, risks, and the 5 Open Questions to resolve via prototype).
