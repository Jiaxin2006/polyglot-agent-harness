# CLAUDE.md

This repository is **polyglot-agent-harness**: a portable AI engineering harness (skills, agents, commands, hooks) usable across Claude Code, Cursor, Trae, and Codex.

## Authoritative instructions

Read **`AGENTS.md`** in this repository for canonical workflows and safety rules.

## Claude Code specifics

- **Plugin layout**: `skills/`, `agents/`, `commands/`, `hooks/`, `plugin.json`, `.claude-plugin/` — load with `claude --plugin-dir /path/to/polyglot-agent-harness` or copy into a project’s `.claude/` directory.
- **Paths in hooks**: use `${CLAUDE_PLUGIN_ROOT}` for files inside this harness; use `${CLAUDE_PROJECT_DIR}` when targeting the consumer application repository in hook scripts you add later.

## Developing skills

Follow the same conventions as [starry-harness](https://github.com/JosephJoshua/starry-harness): YAML frontmatter on `SKILL.md`, imperative body, third-person `description` with trigger phrases.
