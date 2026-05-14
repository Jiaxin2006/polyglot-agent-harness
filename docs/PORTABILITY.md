# Portability matrix

This harness keeps **one canonical tree** at the repository root (`skills/`, `agents/`, `commands/`, `hooks/`) compatible with `claude --plugin-dir`, matching patterns from [starry-harness](https://github.com/JosephJoshua/starry-harness). The [tgoskits-plugin](https://github.com/seek-hope/tgoskits-plugin) style **project-local `.claude/`** layout is also supported by copying the same files.

## Claude Code

| Mode | What to do |
|------|------------|
| Plugin directory | From any project: `claude --plugin-dir /absolute/path/to/polyglot-agent-harness` |
| Marketplace | Add this repo as a custom marketplace (see `.claude-plugin/`) and enable the plugin name |
| Project-local `.claude/` | Copy or symlink harness files into `<your-repo>/.claude/` so `plugin.json`, `commands/`, `agents/`, `hooks/` resolve like [tgoskits-plugin](https://github.com/seek-hope/tgoskits-plugin) |

Use `${CLAUDE_PLUGIN_ROOT}` inside hook commands (set by Claude Code when loading the plugin).

## Trae

Trae discovers skills under `.trae/skills/<name>/SKILL.md`.

Run from this harness:

```bash
./scripts/install-into-project.sh /path/to/your/repo
# or materialize copies for sandboxes that forbid symlinks:
./scripts/install-into-project.sh --copy /path/to/your/repo
```

## Cursor

- Commit **`AGENTS.md`** at your project root (copy from this harness or merge sections).
- Optional: install script writes **`.cursor/rules/polyglot-harness.mdc`** to point agents at harness-relative paths.

Project-local Cursor skills can also mirror `skills/` under `.cursor/skills/` if you prefer everything inside `.cursor/`; Trae layout is the default target of `install-into-project.sh`.

## Codex (OpenAI CLI)

See [codex.md](./codex.md). The portable contract is: **one `AGENTS.md`** plus small tool-specific stubs.

## Environment variables

See `skills/experiment-guard/SKILL.md` for `POLYGLOT_UPSTREAM_REMOTE`, `POLYGLOT_BASE_BRANCH`, and optional Docker-related variables.
