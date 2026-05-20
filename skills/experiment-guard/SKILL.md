---
name: experiment-guard
description: >-
  Generic experiment workflow guard: sync configured upstream remote and base branch,
  stop immediately on merge conflicts, prefer containerized verification when POLYGLOT_DOCKER_IMAGE
  or project docs specify it, and require explicit human approval before delivery/PR actions.
---

# Experiment Guard

## When to apply

Use this skill whenever the user is doing non-trivial work in the active Git repository: experiments, refactors, running tests, changing dependencies, or preparing a PR.

## Configuration (environment variables)

All paths are **repository-relative** unless noted. Set these in your shell profile, `direnv`, CI, or project `docs/ai/env.example`.

| Variable | Default | Meaning |
|----------|---------|---------|
| `POLYGLOT_UPSTREAM_REMOTE` | `upstream` | Remote to fetch/merge from |
| `POLYGLOT_BASE_BRANCH` | `main` | Branch to align with (use `dev` if that is your integration branch) |
| `POLYGLOT_ORIGIN_REMOTE` | `origin` | Your fork / push remote (informational) |
| `POLYGLOT_DOCKER_IMAGE` | *(empty)* | If set, final build/test verification should run inside this image |
| `POLYGLOT_DOCKERFILE` | *(empty)* | If set (e.g. `container/Dockerfile`), document or use `docker build -f` per project README |

## Required flow (order)

### 1) Fetch

From the **active repository root** (the workspace Git root, not a hardcoded path):

- `git fetch "${POLYGLOT_UPSTREAM_REMOTE:-upstream}" --prune`
- Optionally `git fetch "${POLYGLOT_ORIGIN_REMOTE:-origin}" --prune`
- Print: current branch, short `HEAD`, remote tracking branch if any, and resolved `${POLYGLOT_BASE_BRANCH}` tip on upstream.

### 2) Merge or rebase (project policy)

- Default: `git merge "${POLYGLOT_UPSTREAM_REMOTE:-upstream}/${POLYGLOT_BASE_BRANCH:-main}"`
- If the project uses rebase workflow instead, use `git rebase "upstream/${POLYGLOT_BASE_BRANCH}"` **only** if that is the team convention.

**Conflict rule:** If Git reports conflicts (unmerged paths or conflict markers), **stop**. Do not auto-resolve. Show `git status` and the list of conflicted paths. Wait for human resolution.

### 3) Verification environment

- **Before** any workflow that will run `docker`, `docker compose`, or container-backed tests, run the harness check from the harness (or consumer) repo root:
  - `python3 scripts/docker-check.py`
  - Exit `0` means the daemon answered `docker info`; non-zero means stop and tell the user to start Docker / fix permissions — do not silently fall back to “host-only” tests if the project requires containers.
- Prefer **containerized** build/test when `POLYGLOT_DOCKER_IMAGE` is set or the project documents a Dev Container / Docker workflow.
- Read-only inspection (search, file reads) may occur on the host; **final** compile/test that gates a claim of “green” should match the project’s canonical environment (often Docker/CI).

### 4) Delivery / PR gate

Before delivery (preparing a PR draft, force-pushing, or any upstream-bound commit):

- **Formatting gate (blocking)** — Run `cargo fmt --all -- --check` and fix until exit 0 before claiming ready or committing for upstream. See `pr-workflow` for the full gate order: **fmt → clippy → tests → E2E**.
- **Manual PR submission (default)** — Do not run `gh pr create` or push for PR creation on upstream unless the user explicitly asks. Prepare paste-ready title/body and save the draft outside git repos (see `pr-workflow` → `pr-drafts/`).
- Pause and ask for **explicit approval** unless the user already approved delivery in this session.
- Summarize: commits, files touched, gates run (fmt/clippy/tests/E2E), and evidence (commands + key log lines).

## Output checklist

- Sync: upstream remote name, base branch, upstream tip SHA
- Merge/rebase: success vs conflict (if conflict, stop)
- Verify: commands used; note if Docker was used
- Delivery: only after explicit human approval
