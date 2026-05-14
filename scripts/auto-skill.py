import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj: dict) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def truthy_env(key: str) -> bool:
    value = os.environ.get(key, "")
    return value.strip().lower() in {"1", "y", "yes", "true", "on"}


def ensure_skill_file(skill_name: str, description: str) -> Path:
    root = repo_root()
    skill_dir = root / "skills" / skill_name
    skill_dir.mkdir(parents=True, exist_ok=True)
    skill_path = skill_dir / "SKILL.md"

    if not skill_path.exists():
        skill_path.write_text(
            "\n".join(
                [
                    "---",
                    f'name: "{skill_name}"',
                    f'description: "{description}"',
                    "---",
                    "",
                    f"# {skill_name}",
                    "",
                    "用你自己的内容替换此占位文本。",
                    "",
                ]
            ),
            encoding="utf-8",
        )

    return skill_path


def ensure_plugin_json_has_skill(skill_md_relpath: str) -> None:
    root = repo_root()
    plugin_path = root / "plugin.json"
    data = read_json(plugin_path)
    skills = list(data.get("skills", []))
    if skill_md_relpath not in skills:
        skills.append(skill_md_relpath)
    data["skills"] = skills
    write_json(plugin_path, data)


def git(*args: str) -> None:
    subprocess.check_call(["git", *args], cwd=repo_root())


def git_output(*args: str) -> str:
    out = subprocess.check_output(["git", *args], cwd=repo_root(), text=True)
    return out.strip()


def ensure_origin_remote() -> str:
    try:
        return git_output("remote", "get-url", "origin")
    except subprocess.CalledProcessError:
        raise SystemExit("missing git remote `origin`; refusing to push")


def cmd_ensure(args: argparse.Namespace) -> None:
    skill_path = ensure_skill_file(args.name, args.description)
    skill_md_rel = f"skills/{args.name}/SKILL.md"
    ensure_plugin_json_has_skill(skill_md_rel)

    if args.commit:
        git("add", skill_md_rel, "plugin.json")
        msg = args.commit_message or f"harness: ensure skill {args.name}"
        git("commit", "-m", msg)

    if args.push:
        if not truthy_env("HARNESS_AUTO_PUSH"):
            raise SystemExit(
                "refusing to push: set HARNESS_AUTO_PUSH=1 and re-run with --push"
            )
        _ = ensure_origin_remote()
        git("push")

    sys.stdout.write(str(skill_path) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    ensure = sub.add_parser("ensure")
    ensure.add_argument("--name", required=True)
    ensure.add_argument("--description", required=True)
    ensure.add_argument("--commit", action="store_true")
    ensure.add_argument("--commit-message")
    ensure.add_argument("--push", action="store_true")
    ensure.set_defaults(func=cmd_ensure)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
