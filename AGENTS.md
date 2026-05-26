# Agent instructions (polyglot-agent-harness)

This file is the **canonical** project guidance for AI coding agents across **Cursor**, **Trae**, **Codex**, and human developers. **Claude Code** should read `CLAUDE.md` in this repository (pointer) and still honor the workflows below.

## Repository role

`polyglot-agent-harness` is a reusable harness: **skills** (workflows), **agents** (review/triage roles), **commands** (slash workflows), and **hooks** (optional Claude Code lifecycle). It is designed to be consumed via:

- `claude --plugin-dir <path-to-this-repo>`
- copy into `<your-project>/.claude/` (tgoskits-plugin style)
- Trae: `.trae/skills/*` via `scripts/install-into-project.sh`
- Cursor / Codex: this `AGENTS.md` plus `.cursor/rules` in consumer repos

## Global rules

1. **Git safety** — Before claiming a branch is “synced”, fetch the configured upstream and merge/rebase per project policy. **Stop on conflicts**; never silently resolve.
2. **Verification** — Prefer the same environment as CI (often Docker). For iterative toolchain-heavy verification, prefer a reusable container or mounted package/toolchain caches over repeated throwaway `docker run --rm` containers unless a clean container is required. Do not claim “tests pass” without running the project’s commands or explaining skips.
3. **Delivery** — No `gh pr create`, force-push to shared branches, or destructive git without **explicit** user approval when policies require it.
4. **Paths** — Never hardcode another user’s machine paths. Use `git rev-parse --show-toplevel` and env vars (`POLYGLOT_*`).
5. **Reporting** — When a run fails, a bug is found/fixed, or a PR is being prepared, invoke `report-generator` and update local report artifacts (evidence included). Do not include `reports/` in upstream PRs unless the user explicitly requests it; keep reports untracked or in a fork-only branch.
6. **Skill maintenance** — When you discover a wrong/missing workflow (especially test authoring), invoke `auto-skill-maintainer` to update/add a skill and commit; push only when the configured gate allows.
7. **Skill execution record** — If the current tool cannot “invoke skills” as a first-class feature, you must still follow the skill steps and explicitly state which skill is being applied and which checklist items were completed.

## Mandatory skill triggers (must)

If you are about to do any of the following actions, you must apply the named skill first, and record “Applying <skill>” in the work log:

- **Start risky work** (sync upstream, rebase/merge, conflict resolution, experiment that may dirty the tree) → `experiment-guard`
- **Write or modify tests** (unit/e2e/config/regex assertions) → `test-authoring`
- **Run failed / CI red / bug found or fixed** (including infra/resource failures like disk-full) → `report-generator`
- **Prepare delivery** (open PR, declare “ready”, change scope/title/body) → `pr-workflow`
- **Declare completion / 100% confidence** (user asks “done?” or you claim “fully correct”) → `completion-examiner`
- **Workflow gap discovered** (a repeated pitfall not covered by existing skills) → `auto-skill-maintainer`

## Pipeline (canonical)

This is the default end-to-end pipeline for work in a consumer repo:

1. **Start work (guardrails)** — Apply `experiment-guard` before experiments or risky git operations.
2. **Work and triage** — Fix the issue, add/adjust tests, collect evidence.
3. **Report update (mandatory)** — Apply `report-generator` whenever there is a run failure, bug discovery/fix, or PR prep.
4. **Skill maintenance (conditional)** — If any “we should have had a workflow for this” moment happens, apply `auto-skill-maintainer` to update/add a skill and commit.
5. **PR preparation** — Apply `pr-workflow`: scope the diff, verify, review accidental files, and (optionally) open the PR via `gh` when allowed.

## Skills (when to use)

| Skill | Use when |
|-------|----------|
| `experiment-guard` | Starting substantive work: sync upstream, merge base branch, conflict stop, container verify |
| `pr-workflow` | Preparing a PR: scope, tests, message, description, evidence |
| `harness-overview` | Explaining how this harness maps to Cursor/Trae/Claude/Codex |
| `report-generator` | New passing E2E, key bug fix, or PR prep: generate/update structured report with evidence |
| `test-authoring` | Writing or reviewing tests: choose Rust/C/script, place files, write build/qemu configs, set pass/fail evidence |
| `auto-skill-maintainer` | A workflow gap is found: auto-add/update a skill and (optionally) commit/push via the gate |

Skill bodies live in `skills/*/SKILL.md` (YAML frontmatter + markdown).

## Agents

- `agents/code-reviewer.md` — Read-only review checklist
- `agents/triager.md` — Route failures/logs to next steps

## Commands

- `/verify` — See `commands/verify.md` for a default verification pass pattern

## References

- `docs/PORTABILITY.md` — per-tool installation
- `docs/codex.md` — Codex `instructions` file hint
