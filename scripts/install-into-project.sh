#!/usr/bin/env bash
# Install polyglot-agent-harness skills (and optional Cursor rule) into a consumer repository.
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: install-into-project.sh [options] <TARGET_REPO>

Options:
  --copy              Copy SKILL trees instead of symlinks (default: symlink)
  --no-cursor-rule    Do not install .cursor/rules bridge
  --harness-path REL  Relative path from TARGET to this harness (default: auto from symlink target)

Examples:
  ./scripts/install-into-project.sh /path/to/myapp
  ./scripts/install-into-project.sh --copy /path/to/myapp

Environment:
  POLYGLOT_HARNESS_ROOT  Override path to this harness repo (default: parent of scripts/)
EOF
}

MODE="symlink"
INSTALL_CURSOR_RULE=1
HARNESS_PATH_OVERRIDE=""
TARGET=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --copy) MODE="copy" ;;
    --no-cursor-rule) INSTALL_CURSOR_RULE=0 ;;
    --harness-path)
      HARNESS_PATH_OVERRIDE="${2:?}"
      shift
      ;;
    -h|--help) usage; exit 0 ;;
    *)
      if [[ -z "$TARGET" ]]; then
        TARGET="$1"
      else
        echo "Unexpected argument: $1" >&2
        usage >&2
        exit 1
      fi
      ;;
  esac
  shift
done

if [[ -z "${TARGET}" ]]; then
  usage >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HARNESS_ROOT="${POLYGLOT_HARNESS_ROOT:-$(cd "${SCRIPT_DIR}/.." && pwd)}"
TARGET="$(cd "${TARGET}" && pwd)"

if [[ ! -d "${TARGET}/.git" && ! -f "${TARGET}/.git" ]]; then
  echo "ERROR: ${TARGET} does not look like a git repository root." >&2
  exit 1
fi

TRA_SKILLS="${TARGET}/.trae/skills"
mkdir -p "${TRA_SKILLS}"

shopt -s nullglob
for skill_dir in "${HARNESS_ROOT}/skills"/*; do
  [[ -d "${skill_dir}" ]] || continue
  name="$(basename "${skill_dir}")"
  dest="${TRA_SKILLS}/${name}"
  if [[ -e "${dest}" || -L "${dest}" ]]; then
    echo "Skip (exists): ${dest}"
    continue
  fi
  if [[ "${MODE}" == "copy" ]]; then
    cp -R "${skill_dir}" "${dest}"
    echo "Copied: ${dest}"
  else
    rel="$(python3 - <<PY
import os
h = os.path.realpath("${skill_dir}")
t = os.path.realpath("${TRA_SKILLS}")
print(os.path.relpath(h, t))
PY
)"
    ln -s "${rel}" "${dest}"
    echo "Symlinked: ${dest} -> ${rel}"
  fi
done

if [[ "${INSTALL_CURSOR_RULE}" -eq 1 ]]; then
  RULE_DIR="${TARGET}/.cursor/rules"
  mkdir -p "${RULE_DIR}"
  RULE_DEST="${RULE_DIR}/polyglot-harness.mdc"
  if [[ -n "${HARNESS_PATH_OVERRIDE}" ]]; then
    HP="${HARNESS_PATH_OVERRIDE}"
  else
    HP="$(python3 - <<PY
import os
print(os.path.relpath("${HARNESS_ROOT}", "${TARGET}"))
PY
)"
  fi
  cat > "${RULE_DEST}" <<EOF
---
description: Bridge to polyglot-agent-harness (skills + AGENTS.md)
globs:
alwaysApply: true
---

# Polyglot harness

- Read project \`AGENTS.md\` at repo root if present (copy from harness or maintain your own).
- Trae skills installed under \`.trae/skills/\` from this harness point here: \`${HP}/skills/\`.
- For Claude Code in the consumer repo, either copy \`${HP}/\` into \`.claude/\` per harness README, or run \`claude --plugin-dir ${HP}\`.
EOF
  echo "Wrote Cursor rule: ${RULE_DEST}"
fi

cat <<EOF

Done. Next steps for ${TARGET}:
  1. Add or symlink AGENTS.md (see harness README); set POLYGLOT_* env vars as needed.
  2. Trae: skills are under .trae/skills/ (${MODE}).
  3. Claude Code: copy harness into .claude/ OR use: claude --plugin-dir ${HARNESS_ROOT}
  4. Codex: point instructions at AGENTS.md (see harness docs/codex.md).
EOF
