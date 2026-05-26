# polyglot-agent-harness

Portable AI engineering harness (skills, agents, commands) aimed at **Claude Code** (`--plugin-dir` or copy into `.claude/`), **Trae** (`.trae/skills`), **Cursor** (`.cursor/rules` + project skills), and **Codex** / other tools that read root `AGENTS.md`.

## Docker preflight

Before running container workflows, verify the daemon:

```bash
python3 scripts/docker-check.py
```

- Exit code **0**: `docker info` succeeded (CLI present, daemon reachable).
- Exit code **non-zero**: prints a short remediation hint on stderr.

## Reusable Docker Environments

For long Rust/toolchain-heavy workflows, prefer a reusable container or mounted cache volumes instead of repeated `docker run --rm`. Throwaway containers discard runtime state such as rustup components and cargo downloads, which can make every verification re-download the same toolchain.

Pattern:

```bash
docker run -it --name <project>-dev \
  -v "$PWD":/workspace \
  -v <project>-rustup:/opt/rustup \
  -v <project>-cargo-registry:/opt/cargo/registry \
  -v <project>-cargo-git:/opt/cargo/git \
  -w /workspace \
  <image> bash
```

Resume later with:

```bash
docker start -ai <project>-dev
```

Still run `python3 scripts/docker-check.py` before Docker workflows. If a project or CI requires a clean container, document that choice and expect repeated dependency/toolchain downloads.

### Optional Claude Code PreToolUse (flat settings)

This repository’s `hooks/hooks.json` uses the **nested SessionStart** schema compatible with plugins such as [starry-harness](https://github.com/JosephJoshua/starry-harness). The older **flat** hook list used by [tgoskits-plugin](https://github.com/seek-hope/tgoskits-plugin) supports `PreToolUse` entries like:

```json
{
  "event": "PreToolUse",
  "matcher": "Bash",
  "command": "python3 \"${CLAUDE_PLUGIN_ROOT}/scripts/docker-check.py\" --pre-tool-use"
}
```

If your Claude Code install expects that flat format, merge the snippet into your user or project hook settings and point `CLAUDE_PLUGIN_ROOT` at this repo (or your `.claude/` copy). The script’s `--pre-tool-use` mode only probes Docker when the Bash tool input mentions `docker`.

## Layout

| Path | Role |
|------|------|
| `skills/` | Trae/Cursor-style `SKILL.md` trees |
| `agents/` | Claude Code agent prompts |
| `commands/` | Slash-command markdown |
| `hooks/` | Plugin lifecycle hooks |
| `scripts/docker-check.py` | Docker daemon health check |

## Reports

When a new E2E passes, a key bug is fixed, or a PR is being prepared, use the `report-generator` skill and write in-repo reports under `reports/`.

## Install into another repo

See `scripts/install-into-project.sh` or submodule this repository and symlink `skills/*` into `.trae/skills/` per your team’s convention.

## License

Apache-2.0 — see `LICENSE`.
