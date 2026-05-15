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
   - For Rust repos, run formatting in check mode (CI frequently enforces this): `cargo fmt --all -- --check`
   - For Rust repos, run Clippy with warnings denied (CI frequently enforces this). Prefer the project wrapper if it exists (e.g. `cargo xtask clippy`); otherwise: `cargo clippy --all-targets --all-features -- -D warnings`
   - If CI failed due to infra/resource constraints (e.g. disk-full), add a targeted repro/guardrail (small test or assertion) and rerun the narrowest check that proves the fix.
4. **Artifact inventory** — List newly created files/dirs and what they do. If any were experimental or unrelated, remove them from the branch (stash or separate PR).
5. **Commit messages** — Imperative subject line (~72 chars), body explains *why* when non-obvious.
6. **Report update (mandatory)** — Invoke `report-generator` and update a report artifact for this change (default: local-only; do not include in upstream PR unless explicitly requested). PRs must not be opened with a stale/missing report when policy requires reporting.
7. **Description template**
   - Summary (what / why)
   - Test plan (commands + expected result)
   - Risk / rollback
   - Issue links if any
8. **Diff review** — Scan for secrets, debug prints, accidental file additions.
9. **Upstream alignment** — Apply `experiment-guard` sync before final push unless user declined.
10. **Automation** — If `gh` is available and user approved: `gh pr create` with filled title/body; otherwise write `pr-draft.md` with paste-ready content.

## High-risk edits checklist

If touching fatal paths (panic/oops/trap) or logging/console code:

- Preserve existing recursion/concurrency guards (e.g. `axpanic::enter_panic`, `enter_oops`, `oops_in_progress`, backtrace one-shot gating).
- Ensure only the primary fatal path emits heavy diagnostics (backtrace capture, formatting) to avoid recursive panics and lock re-entry.
- Add at least a compile-level check in a representative target (`cargo check -p <crate> --target <triple>`) and record it in the report.

## Do not

- Open or merge a PR without user confirmation when policy requires it.
- Squash unrelated history without asking if the project prefers linear/rebase workflows.

## Common CI failure playbooks

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
