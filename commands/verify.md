# /verify — local verification pass

Run a **minimal, project-appropriate** verification pass in the active Git repository.

## Default sequence (adapt to repo)

1. Print repo root: `git rev-parse --show-toplevel` and current branch.
2. If `POLYGLOT_DOCKER_IMAGE` is set, suggest or run containerized verify per project docs; else run native.
3. Common checks (skip with reason if not applicable):
   - `git status -sb` (ensure no unexpected untracked secrets)
   - Language-specific: e.g. `cargo test`, `npm test`, `make test`, or script from `package.json` / `Makefile`
4. Summarize pass/fail with the **exact commands** used.

## Guardrails

- If merge conflicts exist, **stop** and point the user to `experiment-guard` skill instead of “fixing” silently.
- Do not delete user files or change remotes without explicit instruction.

## Output

- Commands run (copy-pasteable)
- Result summary
- Follow-ups if anything was skipped
