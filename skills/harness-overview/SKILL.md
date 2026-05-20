---
name: harness-overview
description: >-
  Explains polyglot-agent-harness layout: Claude Code plugin-dir vs .claude copy, Trae skills
  symlink install, Cursor rules bridge, Codex instructions_file; points to AGENTS.md and docs/PORTABILITY.md.
---

# Harness Overview

This repository is a **portable AI development harness** meant to work across:

- **Claude Code** — `claude --plugin-dir /path/to/polyglot-agent-harness` *or* copy contents into `.claude/` (see `plugin.json`).
- **Trae** — Skills under `.trae/skills/<skill>/SKILL.md`; use `scripts/install-into-project.sh` from a consumer repo.
- **Cursor** — Project rules in `.cursor/rules/*.mdc` plus root `AGENTS.md`.
- **OpenAI Codex CLI** — Project instructions via `docs/codex.md` and `AGENTS.md`.

## Canonical docs

- `AGENTS.md` — Single narrative for humans and agents (Cursor/Codex-first).
- `CLAUDE.md` — Short pointer for Claude Code sessions in this repo.
- `docs/PORTABILITY.md` — Per-tool install matrix and paths.

## Directory map (this repo)

| Path | Role |
|------|------|
| `skills/*/SKILL.md` | Reusable workflows (YAML frontmatter) |
| `agents/*.md` | Subagent-style prompts with frontmatter |
| `commands/*.md` | Slash-command bodies for Claude Code |
| `hooks/` | Optional lifecycle hooks |
| `scripts/docker-check.py` | Preflight: `docker info` (standalone) or `--pre-tool-use` gate for Bash |
| `scripts/install-into-project.sh` | Wire harness into another Git repo |

When unsure which skill applies, prefer **`experiment-guard`** before risky git operations, then **`pr-workflow`** for delivery.

**Delivery policy** — `pr-workflow` owns the full PR gate (fmt → clippy → tests → E2E), manual upstream submission by default, and draft location. Save PR drafts outside git repos at `操作系统/pr-drafts/<repo-or-feature>-pr-draft.md` (not inside consumer projects like `tgoskits/`).
