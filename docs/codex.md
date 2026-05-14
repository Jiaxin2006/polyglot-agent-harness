# Codex CLI integration

Codex and similar CLIs typically load **project instructions** from a configurable path. This harness standardizes on root **`AGENTS.md`**.

## Suggested setup

1. Copy `AGENTS.md` from this harness into your application repository (or symlink if your tooling allows).
2. In your Codex config (e.g. `~/.codex/config.toml` or project-local TOML, depending on Codex version), set the instructions file to point at that `AGENTS.md`.

Example shape (adjust keys to match your installed Codex version):

```toml
# Example only — verify against `codex --help` / upstream docs
[instructions]
file = "AGENTS.md"
```

3. Keep tool-specific noise out of `AGENTS.md`: put Claude-only hooks in `hooks/` here; put Cursor-only frontmatter in `.cursor/rules/`.

## Cross-tool rule

If behavior must differ by product, duplicate **one sentence** of divergence in the product-specific file and keep the detailed procedure in `AGENTS.md` or `skills/*/SKILL.md`.
