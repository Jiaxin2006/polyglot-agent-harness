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

0. **Declare the workflow** — Explicitly state “Applying pr-workflow” and track completion items, especially in tools that cannot natively “invoke skills”. Before marking the PR ready, confirm this **blocking order** (do not skip or reorder):
   - [ ] `cargo fmt --all -- --check` (exit 0)
   - [ ] Clippy with warnings denied
   - [ ] Unit/integration tests for touched crates
   - [ ] E2E case (step 4) with documented commands and expected output
1. **Scope** — One logical change per PR when possible. Split unrelated edits.
2. **Sync upstream first** — Before finalizing the PR, fetch the upstream base branch and merge/rebase per project policy. Stop on conflicts and request human review (use `experiment-guard`).
3. **Local verification** — Ensure local checks and tests pass in the same environment as CI (prefer Docker/DevContainer). Do not claim “ready” without runnable commands and evidence. Run gates in this order: **fmt → clippy → tests → E2E** (step 4).

   ### Formatting (mandatory, blocking)

   **Before** telling the user the PR is ready, **before** any commit intended for upstream, and **before** preparing the final draft — formatting must pass. This is not optional; a green local test run does not excuse a failed `fmt` job.

   1. Run exactly what tgoskits CI runs (`.github/workflows/ci.yml` `fmt` job): `cargo fmt --all -- --check`
   2. If exit code is non-zero: run `cargo fmt --all` (or `cargo fmt -p <crate>` when changes are scoped to one crate), then re-run `cargo fmt --all -- --check` until exit 0
   3. **Include formatted files in the same commit** as the functional change — never push or mark ready with fmt failures still present

   Skipping this step is the most common avoidable CI failure on Rust PRs.

   ### Clippy and tests

   - For Rust repos, run Clippy with warnings denied (CI frequently enforces this). Prefer the project wrapper if it exists (e.g. `cargo xtask clippy`); otherwise: `cargo clippy --all-targets --all-features -- -D warnings`
   - Run unit/integration tests for crates you touched before E2E.
   - If CI failed due to infra/resource constraints (e.g. disk-full), add a targeted repro/guardrail (small test or assertion) and rerun the narrowest check that proves the fix.
4. **E2E test case (mandatory for each PR)** — Every PR must include at least one end-to-end test that exercises the changed behavior (e.g. ArceOS/Starry QEMU case under `test-suit/`, host script with clear pass criteria, or equivalent runner-visible check). Unit tests alone are not sufficient when the change affects runtime, build, or xtask workflows.
   - Add or extend the case in the same PR as the feature/fix (not a follow-up).
   - In the PR body **Test plan**, give **copy-paste local commands** and **expected correct output** (regex, log snippets, exit code, or “must see / must not see”).
   - Example (ArceOS backtrace): `cargo xtask arceos test qemu --arch x86_64 --test-case backtrace-raw-normal` → expect `BACKTRACE_BEGIN` … `BT 0`/`BT 1` with non-zero `ip`, then `=== host backtrace symbolize ===` with demangled function names (when auto-symbolize is enabled).
   - Tell the author explicitly how to run locally and what “green” looks like before opening the PR; if E2E is impossible (hardware-only), document a reproducible substitute and get reviewer agreement in the PR body.
5. **Artifact inventory** — List newly created files/dirs and what they do. If any were experimental or unrelated, remove them from the branch (stash or separate PR).
6. **Commit messages** — Imperative subject line (~72 chars), body explains *why* when non-obvious.
7. **Report update (mandatory)** — Invoke `report-generator` and update a report artifact for this change (default: local-only; do not include in upstream PR unless explicitly requested). PRs must not be opened with a stale/missing report when policy requires reporting.
8. **Description template** — Always prepare paste-ready PR content for the user (see **Manual PR submission** below):
   - **Title**: English, imperative, ~72 chars
   - **Body**: Chinese, with sections:
     - Summary (what / why)
     - Test plan (copy-paste commands + expected output)
     - Risk / rollback
     - Issue links if any
   - **No internal plan numbering** — Do not reference local plan IDs (`PR-1`, `PR-4`, `TODO-2`, etc.) from files like `issue-146-backtrace-plan.md` in upstream PR title or body. For follow-up work, use neutral wording (`后续完成`, `follow-up PR`) without numbering.
   - **Backtrace (#146) PRs** — Any PR draft for backtrace (Issue #146) must start the body with `Tracking issue: https://github.com/rcore-os/tgoskits/issues/146` (before Summary or as the first line).
9. **Diff review** — Scan for secrets, debug prints, accidental file additions.
10. **Upstream alignment** — Apply `experiment-guard` sync before final push unless user declined.
11. **Prepare for submission (default: manual)** — Write the PR draft (English title + Chinese body per step 8) to a local file **outside** any git-tracked project directory (see **Manual PR submission**). The user tests locally and submits the PR manually on upstream. Do **not** run `gh pr create`, push for PR creation, or open a PR on the upstream/original repo unless the user explicitly asks.

## Manual PR submission (default policy)

This is the default workflow unless the user explicitly requests automated PR creation.

1. **Never open/create a PR on upstream directly** — Do not run `gh pr create`, do not push a branch for PR creation, and do not open a PR on the original/upstream repo. The user verifies locally first and submits manually.
2. **Always prepare PR content** — Produce an English title and Chinese body (Summary, Test plan with commands + expected output, Risk, issue links) ready to paste when the user opens the PR.
3. **Draft file location** — Save the draft **outside** the git repository (never inside project folders such as `tgoskits/`). Examples:
   - `/Users/hanjiaxin/Desktop/操作系统/pr-drafts/<repo-or-feature>-pr-draft.md`
   - Workspace root `操作系统/` is acceptable if it is not inside a git-tracked project folder
4. **Agent may still prepare the branch** — Commits and local verification are fine; stop before upstream push/PR unless explicitly requested. **Mandatory before any upstream-bound commit or “ready” message:** `cargo fmt --all -- --check` must pass; if not, run `cargo fmt --all`, re-check, and include the diff in the same commit.
5. **No internal plan numbering in drafts** — Upstream-facing title/body must not cite internal plan IDs from local planning docs. Describe scope and follow-ups in plain language only.

**Automation exception** — Only when the user explicitly asks: push the branch and run `gh pr create` with the prepared title/body. Even then, prefer a fork or user-specified remote over opening directly on upstream unless they confirm.

### Backtrace (#146) PRs

When preparing a PR draft for backtrace work (Issue #146):

- First line of the body (before `## Summary`): `Tracking issue: https://github.com/rcore-os/tgoskits/issues/146`
- Do not use internal plan labels (`PR-1`, `PR-4`, …) in title or body; refer to follow-up work as `后续完成` / `follow-up PR` without numbers.

## High-risk edits checklist

If touching fatal paths (panic/oops/trap) or logging/console code:

- Preserve existing recursion/concurrency guards (e.g. `axpanic::enter_panic`, `enter_oops`, `oops_in_progress`, backtrace one-shot gating).
- Ensure only the primary fatal path emits heavy diagnostics (backtrace capture, formatting) to avoid recursive panics and lock re-entry.
- Add at least a compile-level check in a representative target (`cargo check -p <crate> --target <triple>`) and record it in the report.

## Do not

- Open or create a PR on the upstream/original repo (no `gh pr create`, no push-for-PR) unless the user explicitly asks.
- Place `pr-draft.md` or similar PR drafts inside a git-tracked project directory (e.g. `tgoskits/`).
- Reference internal plan IDs (`PR-1`, `PR-4`, `TODO-2`, …) from local planning docs in upstream PR title or body — use neutral follow-up wording instead.
- Open or merge a PR without user confirmation when policy requires it.
- Squash unrelated history without asking if the project prefers linear/rebase workflows.
- Push, commit for upstream, or tell the user the PR is ready without `cargo fmt --all -- --check` passing locally first.

## Common CI failure playbooks

### rustfmt / formatting (`fmt` job)

Typical symptom in CI logs:

- `fmt` job fails with `Diff in path/to/file.rs` (or `cargo fmt --all -- --check` exits non-zero locally)

Fix:

1. `cargo fmt --all`
2. Review the diff (often whitespace/line breaks only), then commit formatted files in the **same** commit as the code change
3. Re-run `cargo fmt --all -- --check` until exit 0 before push

Common gotcha (tgoskits `axbuild`): multi-line `if` with `let` chains rustfmt collapses to a single line, e.g. `if cond && let Some(x) = y {` in `scripts/axbuild/src/arceos/test.rs`. Local edit may look fine; CI still fails until you run `cargo fmt --all` and commit the formatter output.

### Disk-full / os error 28 in QEMU cases

Typical symptom in logs:

- `No space left on device (os error 28)` while copying a rootfs image
- Paths like `target/<triple>/qemu-cases/<case>/cache/rootfs/.<hash>.img.<runid>.tmp`

Checklist:

1. Treat large image caches as an optimization, not a correctness requirement: the suite should still run when caching is disabled.
2. Prefer CI-safe behavior: disable writing large caches under `CI=1`, and/or allow an explicit kill-switch env (e.g. `AXBUILD_DISABLE_ROOTFS_CACHE=1`).
3. Add a small unit test that proves the guardrail (e.g. “in CI, cache write is a no-op”).
4. In the PR body, call out that the change prevents infra failures from blocking correctness tests.

### RISC-V SBI return type mismatch (`SbiRet`)

Typical symptom in logs:

- `expected rustsbi::SbiRet, found sbi_rt::SbiRet` (or other crate-path variants)
- Often shows up while building RISC-V virtualization code (e.g. Axvisor/riscv_vcpu)

Checklist:

1. Identify which trait is being implemented (commonly `rustsbi::Pmu` / other RustSBI traits).
2. Ensure the impl method signatures use the trait’s `SbiRet` type consistently:
   - Prefer `sbi_spec::binary::SbiRet` (the canonical type used by RustSBI traits), or explicitly use `rustsbi::SbiRet` which re-exports it.
   - Avoid accidentally importing `sbi_rt::SbiRet` into the impl signature.
3. Run a target-specific compile check and record it in the report:
   - `cargo check -p riscv_vcpu --target riscv64gc-unknown-none-elf`
