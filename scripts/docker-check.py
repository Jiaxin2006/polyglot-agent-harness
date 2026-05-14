#!/usr/bin/env python3
"""Verify Docker daemon reachability, or gate Bash PreToolUse when Docker is involved.

Standalone (default): run `docker info`; exit 0 if the daemon responds, non-zero otherwise.

Hook mode (`--pre-tool-use`): reads `CLAUDE_TOOL_INPUT` or JSON stdin for the tool payload.
If the command does not reference Docker, exit 0 without probing the daemon.
If it does reference Docker, perform the same check as standalone mode.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys


def _tool_input_string() -> str:
    env_val = os.environ.get("CLAUDE_TOOL_INPUT", "")
    if env_val:
        return env_val
    if not sys.stdin.isatty():
        try:
            data = json.load(sys.stdin)
        except Exception:
            return ""
        if isinstance(data, dict):
            return str(data.get("input", data.get("command", "")))
    return ""


def _mentions_docker(text: str) -> bool:
    t = text.lower()
    return "docker" in t


def verify_docker_daemon() -> int:
    """Return 0 if Docker is usable, non-zero otherwise (messages on stderr)."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            text=True,
            timeout=15,
        )
    except FileNotFoundError:
        print(
            "polyglot docker-check: docker CLI not found in PATH.\n"
            "Install Docker: https://docs.docker.com/get-docker/",
            file=sys.stderr,
        )
        return 1
    except subprocess.TimeoutExpired:
        print(
            "polyglot docker-check: Docker daemon did not respond in time.\n"
            "Start Docker Desktop (macOS/Windows) or the engine (Linux), then retry.",
            file=sys.stderr,
        )
        return 1
    except Exception as exc:  # noqa: BLE001 — surface any transport/socket failure
        print(f"polyglot docker-check: cannot reach Docker: {exc}", file=sys.stderr)
        return 1

    if result.returncode == 0:
        return 0

    print(
        "polyglot docker-check: `docker info` failed — daemon likely down or permission denied.\n"
        "Fix: start Docker / add your user to the docker group / sign in to Docker Desktop.",
        file=sys.stderr,
    )
    if result.stderr.strip():
        print(result.stderr.strip(), file=sys.stderr)
    return 1


def main() -> int:
    hook_mode = "--pre-tool-use" in sys.argv or "--hook" in sys.argv
    if hook_mode:
        if not _mentions_docker(_tool_input_string()):
            return 0
    return verify_docker_daemon()


if __name__ == "__main__":
    raise SystemExit(main())
