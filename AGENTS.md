# AGENTS.md — Socratic Writer

**For all AI agents, subagents, and multi-agent orchestration systems working in this repository.**

## Mandatory Reading (in order)

Before writing any code or making design decisions:

1. `docs/CONSTRAINTS.md` (the constitution — non-negotiable)
2. `docs/VISION.md`
3. `docs/INTERACTION-MODEL.md`
4. `docs/BRANCHING-STRATEGY.md` (this repo's multi-agent workflow rules)
5. `docs/DECISIONS.md` and `docs/ROADMAP.md`
6. `context/INITIAL-BRIEFING.md`

## Multi-Agent Development Rules

This project is explicitly designed for heavy use with the Grok Build TUI's agent skills (implement, execute-plan, review, pr-babysit, and the new branch-manager).

- **Never push directly to `main`**.
- All work happens on short-lived, well-named branches (see BRANCHING-STRATEGY.md).
- Use `isolation: "worktree"` with `spawn_subagent` for any parallel or risky work.
- The **branch-manager** agent (see bundled skill) owns branch creation, naming, cleanup, and PR lifecycle coordination.
- Update `docs/DECISIONS.md` the moment a significant choice is made.
- Preserve the radical minimalism and append-only contract in every change to `app/`.

## Branch Manager Agent

The dedicated `branch-manager` skill/persona must be used (or simulated) for:
- Creating properly named branches for new tasks or agent swarms.
- Ensuring no two agents collide on the same branch.
- Cleaning merged or stale branches.
- Helping orchestrate PR creation and reviews in multi-agent flows.

Invoke it explicitly when the task involves repo structure or parallel agent coordination.

## Testing & Verification

- Run `python3 tests/keyboard_simulator.py` before any JS input model changes.
- Use the hidden harness `SW.runKeyboardTests()` in the browser console for the live app.
- All agent-produced code must pass existing tests + add regression coverage where appropriate.

## Philosophy Reminder

This tool exists to protect deep creative thought. Every line of code or prompt you generate must serve that goal or be rejected.

---

*Maintained by humans + agents together. Keep this file and the branching strategy current.*
