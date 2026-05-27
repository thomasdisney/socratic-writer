# Branching Strategy for Multi-Agent Use — Socratic Writer

This repository is optimized for multi-agent software development using the Grok ecosystem (spawn_subagent, execute-plan, implement, review, pr-babysit, and branch-manager).

## Guiding Principle

**Agents are first-class citizens of the development process.** The branching model must enable safe, parallel, auditable work by many agents without ever risking `main` or creating coordination chaos.

## Protected `main` Branch

- `main` is the only long-lived branch.
- **No direct pushes** by humans or agents (enforced by GitHub branch protection rules + culture).
- All changes arrive via Pull Request only.
- Required:
  - At least one approving review (human maintainer or explicitly delegated branch-manager agent review).
  - All status checks green (when CI is present).
  - Up-to-date with `main` (no conflicts).
- Delete head branch after merge (GitHub setting recommended).

## Branch Naming Convention (Strict)

Use the following prefixes only. The branch-manager agent is the authority on names.

| Prefix       | Purpose                                      | Example                              | Owner          |
|--------------|----------------------------------------------|--------------------------------------|----------------|
| `agent/`     | Work initiated or primarily executed by AI subagents (use for execute-plan / implement swarms) | `agent/42-implement-space-trigger-refactor` | branch-manager + subagent |
| `feature/`   | Human-driven new capability (larger scope)   | `feature/native-tauri-prototype`     | Human          |
| `fix/`       | Bug fixes or constraint violations           | `fix/hold-timer-race`                | Human or agent |
| `docs/`      | Documentation, prompts, or briefing updates  | `docs/add-multi-agent-rules`         | Anyone         |
| `chore/`     | Tooling, CI, repo hygiene (no user-visible change) | `chore/add-branch-protection`     | branch-manager |

**Rules**:
- Slug must be kebab-case, concise, and unique.
- Include a short numeric or date discriminator when many agents are active.
- Never use `feature-branch`, `my-work`, `wip`, or bare `agent`.
- The branch-manager agent rejects or renames non-conforming branches on sight.

## Agent Workflow (Typical)

1. Orchestrator (or human) asks branch-manager to create a branch for a task.
2. Branch-manager creates `agent/<slug>` from latest `main`, pushes it, and returns the name.
3. `execute-plan` or `implement` is invoked with `isolation: "worktree"` targeting that branch (or the skill handles it).
4. Subagent(s) work in isolated worktree(s), make commits on their branch.
5. On completion, orchestrator or branch-manager creates a PR (draft or ready) targeting `main`.
6. Reviewers (human + review skill persona) or branch-manager review.
7. On approval + green, merge (squash or merge commit per policy).
8. Branch-manager cleans up the branch (delete after merge).

Parallel agents on different branches + worktrees are fully supported and encouraged for independent tasks.

## Branch Lifecycle & Cleanup

- Merged branches: auto-delete via GitHub setting or branch-manager scheduled task.
- Stale branches (no commits > 14 days, no open PR): branch-manager proposes deletion or force-deletes with audit log.
- Never leave "experiment" branches lying around.

## Multi-Agent Coordination Safeguards

- Each parallel subagent gets its own worktree + branch (or a private sub-branch if needed).
- Orchestrator session never edits code directly on shared branches — it only coordinates via todos, prompts, and branch-manager calls.
- If two agents need to collaborate on the same logical change, they use a shared `agent/` branch but still via PR + review gates.
- Worktree isolation prevents filesystem races even when agents run truly concurrently.

## GitHub Configuration Recommendations (Apply Manually or via Future Branch-Manager Tooling)

- Branch protection on `main`:
  - Require pull request reviews (1+).
  - Require status checks before merge.
  - Require branches to be up to date.
  - Restrict who can push (or use rulesets for "include administrators").
  - Enable "Delete head branches" after merge.
- Consider a `agents/` team or bot account for automated branch-manager actions.
- Rulesets (repo rules) for future scale: path-based or agent-identity based restrictions.

## Integration With Existing Skills

- `execute-plan`: Already creates worktree-isolated subagents; pair it with explicit branch creation via branch-manager first.
- `implement` + reviewer loop: Produce PR-ready branches.
- `pr-babysit`: Handles post-PR health (CI, reviews, restacks) — branch-manager hands off to it once PR exists.
- `review`: Used by branch-manager or humans for automated code review of agent PRs.

## Local Git Hygiene for Humans & Agents

```bash
git fetch --prune
# Delete local tracking branches for merged remotes
```

Never work on `main` locally for anything but quick hotfixes (and even then, immediately PR).

---

*This strategy exists so that 5–50 agents can collaborate on the same repo without turning it into a battlefield. The branch-manager agent is the enforcer and janitor.*
