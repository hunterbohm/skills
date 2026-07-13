#!/usr/bin/env python3
"""Generate the public skill catalog from nested installable packages."""

from __future__ import annotations

import argparse
import pathlib
import re


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / "skills"
CATALOG = REPO_ROOT / "docs" / "catalog.md"


def frontmatter(path: pathlib.Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise SystemExit(f"missing frontmatter: {path}")
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, separator, value = line.partition(":")
        if separator:
            values[key.strip()] = value.strip().strip('"')
    return values


def display_name(skill: pathlib.Path, fallback: str) -> str:
    metadata = skill / "agents" / "openai.yaml"
    if metadata.is_file():
        match = re.search(
            r'^\s*display_name:\s*"([^"]+)"',
            metadata.read_text(encoding="utf-8"),
            re.MULTILINE,
        )
        if match:
            return match.group(1)
    return fallback.replace("-", " ").title()


def compatibility(skill: pathlib.Path) -> tuple[str, str]:
    text = (skill / "SKILL.md").read_text(encoding="utf-8")
    match = re.search(r"^## Compatibility\n\n([^\n]+)", text, re.MULTILINE)
    if match:
        summary = match.group(1).strip()
        if summary.startswith("Codex App only"):
            return "Codex App only", " --agent codex"
        return summary, ""
    return "Agent Skills-compatible clients", ""


def render() -> str:
    grouped: dict[str, list[pathlib.Path]] = {}
    for entrypoint in sorted(SKILLS_ROOT.rglob("SKILL.md")):
        skill = entrypoint.parent
        relative = skill.relative_to(SKILLS_ROOT)
        if len(relative.parts) < 2:
            raise SystemExit(f"skill must live in a category: {skill}")
        grouped.setdefault(relative.parts[0], []).append(skill)

    lines = [
        "# Skill catalog",
        "",
        "This file is generated from the installable packages under `skills/`.",
        "",
        "Install any skill globally with its command below. Run `npx skills@latest add hunterbohm/skills --list` to preview the live repository.",
        "",
    ]
    for category, skills in sorted(grouped.items()):
        lines.extend([f"## {category.replace('-', ' ').title()}", ""])
        for skill in skills:
            values = frontmatter(skill / "SKILL.md")
            name = values["name"]
            title = display_name(skill, name)
            support, agent_flag = compatibility(skill)
            path = skill.relative_to(REPO_ROOT).as_posix()
            lines.extend(
                [
                    f"### [{title}](../{path}/SKILL.md)",
                    "",
                    values["description"],
                    "",
                    f"**Compatibility:** {support}",
                    "",
                    "```bash",
                    f"npx skills@latest add hunterbohm/skills --skill {name}{agent_flag} --global",
                    "```",
                    "",
                ]
            )
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = render()
    if args.check:
        actual = CATALOG.read_text(encoding="utf-8") if CATALOG.is_file() else ""
        if actual != expected:
            raise SystemExit("docs/catalog.md is out of date; run npm run catalog")
        print("Catalog is current")
        return
    CATALOG.parent.mkdir(parents=True, exist_ok=True)
    CATALOG.write_text(expected, encoding="utf-8")
    print(f"Generated {CATALOG.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
