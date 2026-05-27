# Socratic Writer

**An ultra-minimalist, distraction-free word processor for creative writing, powered by Socratic LLM dialogue.**

> The only controls are your thoughts — expressed through continual typing — and the space bar for essential feedback.

---

## Quick Access

**Launch the app right now:**
- Double-click **Socratic Writer** on your Desktop, **or**
- Run from terminal: `python3 ~/writer/launch.py`

- **Project root**: `~/writer` (symlink) or `~/socratic-writer`
- **Desktop**: `~/Desktop/Writer`
- **Key directories**:
  - `app/` — The current runnable demo (single-file HTML + JS)
  - `docs/` — Vision, constraints, interaction model, roadmap, decisions
  - `context/` — Living project memory, session notes, research
  - `prompts/` — Socratic system prompt drafts (for future real LLM integration)

---

## GitHub

**Primary repository**: https://github.com/thomasdisney/socratic-writer

This project is developed with heavy multi-agent assistance. See:

- `AGENTS.md` — Mandatory instructions for all AI agents and orchestrators
- `docs/BRANCHING-STRATEGY.md` — How branches, PRs, and parallel agent worktrees are managed
- The `branch-manager` skill (in `~/.grok/bundled/skills/branch-manager/`) owns branch creation, naming, and cleanup

All changes to `main` arrive via Pull Request. Direct pushes are forbidden.

---

## Current Status

**Phase**: Usable v0 demo complete (running)

A real, working ultra-minimalist writing surface now exists and can be launched immediately.

- Strict append-only typing (backspace, arrows, delete, shortcuts — all disabled)
- Hold **space bar** (~650ms) at the end of a thought → Socratic questions appear in the right margin
- Pure local. Uses Grok via the Build CLI for Socratic questions when the CLI is available in the environment; otherwise instant high-quality heuristic fallback. No local models required.
- Auto-saves to your browser
- Type `sample1` + hold space for instant demo text
- Type `export` + hold space to save your writing as a .txt file

**Next step**: Use it. Write with it. Then tell me what feels right and what must change. The real iteration begins with your actual use.

---

## Philosophy (One-Sentence)

A pure writing instrument that lets ideas flow without friction or self-editing, while using disciplined Socratic questioning (via LLM) to help the writer see the deeper structure and tensions in their own thoughts — triggered only when the writer chooses (via space bar).

---

## How to Use This Workspace

1. All project-defining documents live in `docs/`. Read them in this order when returning:
   - `docs/VISION.md`
   - `docs/CONSTRAINTS.md`
   - `docs/INTERACTION-MODEL.md`
   - `docs/ROADMAP.md`
   - `docs/DECISIONS.md`

2. `context/` holds research, experiments, user notes, and evolving understanding.

3. When making progress, update the relevant doc immediately so future-you (or future agents) have accurate ground truth.

4. Use the `context/SESSION-NOTES.md` (create per major work session) to record what was explored and why.

---

## Project Name

Working title: **Socratic Writer**

Alternative names considered: Aletheia, Tabula, Flowstate, Maieutic, Echo, Lumen, Vellum, Kairos.

We can rename once the core experience solidifies.

---

## License & Ethos

This tool exists to serve deep creative work. It will never:
- Harvest your writing for training data
- Show ads, notifications, or social features
- Offer "productivity gamification"
- Interrupt your flow uninvited

Privacy-first. Local-first where possible. LLM usage must be user-controlled and transparent.

---

*Initialized: 2026*  
*Status: Ready for deep design and implementation work*
