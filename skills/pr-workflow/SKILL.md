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

0. **Declare the workflow** — Explicitly state “Applying pr-workflow” and track completion items, especially in tools that cannot natively “invoke skills”.
1. **Scope** — One logical change per PR when possible. Split unrelated edits.
2. **Sync upstream first** — Before finalizing the PR, fetch the upstream base branch and merge/rebase per project policy. Stop on conflicts and request human review (use `experiment-guard`).
3. **Local verification** — Ensure local checks and tests pass in the same environment as CI (prefer Docker/DevContainer). Do not claim “ready” without runnable commands and evidence.
4. **Artifact inventory** — List newly created files/dirs and what they do. If any were experimental or unrelated, remove them from the branch (stash or separate PR).
5. **Commit messages** — Imperative subject line (~72 chars), body explains *why* when non-obvious.
6. **Report update (mandatory)** — Invoke `report-generator` and update the in-repo report for this change. PRs must not be opened with a stale report when policy requires reporting.
7. **Description template**
   - Summary (what / why)
   - Test plan (commands + expected result)
   - Risk / rollback
   - Issue links if any
8. **Diff review** — Scan for secrets, debug prints, accidental file additions.
9. **Upstream alignment** — Apply `experiment-guard` sync before final push unless user declined.
10. **Automation** — If `gh` is available and user approved: `gh pr create` with filled title/body; otherwise write `pr-draft.md` with paste-ready content.

## Do not

- Open or merge a PR without user confirmation when policy requires it.
- Squash unrelated history without asking if the project prefers linear/rebase workflows.
