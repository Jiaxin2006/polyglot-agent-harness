---
name: pr-workflow
description: >-
  Structured pull-request preparation: small commits, clear title/body, test evidence,
  risk notes, and checklist aligned with upstream contribution guidelines when present.
---

# PR Workflow

## When to apply

The user asks to open a PR, prepare a patch for upstream, or finish a feature branch for review.

## Steps

1. **Scope** — One logical change per PR when possible. Split unrelated edits.
2. **Hygiene** — Run project formatters/linters/tests per `CONTRIBUTING.md` or `AGENTS.md`.
3. **Commit messages** — Imperative subject line (~72 chars), body explains *why* when non-obvious.
4. **Description template**
   - Summary (what / why)
   - Test plan (commands + expected result)
   - Risk / rollback
   - Issue links if any
5. **Diff review** — Scan for secrets, debug prints, accidental file additions.
6. **Upstream alignment** — Apply `experiment-guard` sync before final push unless user declined.
7. **Automation** — If `gh` is available and user approved: `gh pr create` with filled title/body; otherwise write `pr-draft.md` with paste-ready content.

## Do not

- Open or merge a PR without user confirmation when policy requires it.
- Squash unrelated history without asking if the project prefers linear/rebase workflows.
