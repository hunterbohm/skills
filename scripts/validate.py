#!/usr/bin/env python3
"""Validate every installable skill package with generic Agent Skills rules."""

from __future__ import annotations

import json
import pathlib
import re
import sys


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / "skills"
ALLOWED_TOP_LEVEL = {
    "SKILL.md",
    "LICENSE",
    "agents",
    "assets",
    "evals",
    "references",
    "scripts",
}
TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".py", ".sh", ".txt"}


class Validation:
    def __init__(self) -> None:
        self.errors: list[str] = []

    def require(self, condition: bool, message: str) -> None:
        if not condition:
            self.errors.append(message)


def parse_frontmatter(path: pathlib.Path, check: Validation) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    check.require(match is not None, f"{path}: missing YAML frontmatter")
    if not match:
        return {}
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, separator, value = line.partition(":")
        if separator:
            values[key.strip()] = value.strip().strip('"')
    return values


def validate_openai_yaml(skill: pathlib.Path, check: Validation) -> None:
    path = skill / "agents" / "openai.yaml"
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    display = re.search(r'^\s*display_name:\s*"([^"]+)"', text, re.MULTILINE)
    short = re.search(r'^\s*short_description:\s*"([^"]+)"', text, re.MULTILINE)
    prompt = re.search(r'^\s*default_prompt:\s*"([^"]+)"', text, re.MULTILINE)
    check.require(display is not None, f"{skill.name}: openai.yaml missing display_name")
    check.require(short is not None, f"{skill.name}: openai.yaml missing short_description")
    check.require(prompt is not None, f"{skill.name}: openai.yaml missing default_prompt")
    if short:
        check.require(
            25 <= len(short.group(1)) <= 64,
            f"{skill.name}: short_description must be 25-64 characters",
        )
    if prompt:
        check.require(
            f"${skill.name}" in prompt.group(1),
            f"{skill.name}: default_prompt must mention ${skill.name}",
        )


def validate_evals(skill: pathlib.Path, check: Validation) -> None:
    path = skill / "evals" / "evals.json"
    if not path.is_file():
        return
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        check.require(False, f"{skill.name}: invalid eval JSON: {error}")
        return
    check.require(
        payload.get("skill_name") == skill.name,
        f"{skill.name}: eval skill_name mismatch",
    )
    evals = payload.get("evals")
    check.require(isinstance(evals, list) and bool(evals), f"{skill.name}: evals must be a non-empty list")
    if not isinstance(evals, list):
        return
    ids = [item.get("id") for item in evals if isinstance(item, dict)]
    check.require(len(ids) == len(set(ids)), f"{skill.name}: duplicate eval IDs")
    for item in evals:
        if not isinstance(item, dict):
            check.require(False, f"{skill.name}: every eval must be an object")
            continue
        eval_id = item.get("id", "unknown")
        check.require(bool(item.get("prompt")), f"{skill.name}: eval {eval_id} missing prompt")
        check.require(
            isinstance(item.get("assertions"), list) and bool(item.get("assertions")),
            f"{skill.name}: eval {eval_id} missing assertions",
        )


def validate_skill(skill: pathlib.Path, check: Validation) -> None:
    for required in (skill / "SKILL.md", skill / "LICENSE"):
        check.require(required.is_file(), f"{skill.name}: missing {required.name}")

    unexpected = sorted(
        path.name for path in skill.iterdir() if path.name not in ALLOWED_TOP_LEVEL
    )
    check.require(
        not unexpected,
        f"{skill.name}: unexpected top-level payload: {unexpected}",
    )

    skill_md = skill / "SKILL.md"
    if not skill_md.is_file():
        return
    frontmatter = parse_frontmatter(skill_md, check)
    check.require(
        set(frontmatter) == {"name", "description"},
        f"{skill.name}: frontmatter must contain only name and description",
    )
    check.require(frontmatter.get("name") == skill.name, f"{skill.name}: frontmatter name mismatch")
    check.require(bool(frontmatter.get("description")), f"{skill.name}: empty description")

    for path in skill.rglob("*"):
        check.require(not path.is_symlink(), f"{skill.name}: symlink is not allowed: {path}")
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8")
        check.require("/Users/" not in text, f"{path}: leaks an absolute workstation path")

    skill_text = skill_md.read_text(encoding="utf-8")
    for reference in re.findall(r"`((?:references|scripts|assets)/[^`]+)`", skill_text):
        check.require((skill / reference).exists(), f"{skill.name}: missing referenced path {reference}")

    validate_openai_yaml(skill, check)
    validate_evals(skill, check)


def main() -> None:
    check = Validation()
    skills = sorted(path for path in SKILLS_ROOT.iterdir() if path.is_dir())
    check.require(bool(skills), "no exported skills found")
    for skill in skills:
        validate_skill(skill, check)
    if check.errors:
        for error in check.errors:
            print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"Validated {len(skills)} skill(s): {', '.join(path.name for path in skills)}")


if __name__ == "__main__":
    main()
