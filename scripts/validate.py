#!/usr/bin/env python3
"""Validate every installable skill package with generic Agent Skills rules."""

from __future__ import annotations

import json
import pathlib
import re
import sys


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / "skills"
ALLOWED_REPO_ROOT = {
    ".git",
    ".github",
    ".gitignore",
    "LICENSE",
    "README.md",
    "docs",
    "node_modules",
    "package.json",
    "package-lock.json",
    "scripts",
    "skills",
}
ALLOWED_TOP_LEVEL = {
    "SKILL.md",
    "LICENSE",
    "agents",
    "assets",
    "evals",
    "references",
    "scripts",
}
MAX_PAYLOAD_BYTES = 5 * 1024 * 1024
ALLOWED_BINARY_SUFFIXES = {".gif", ".jpeg", ".jpg", ".png", ".webp"}
SENSITIVE_FILENAMES = {
    ".dockercfg",
    ".env",
    ".netrc",
    ".npmrc",
    ".pypirc",
    "credentials",
    "credentials.json",
    "id_dsa",
    "id_ecdsa",
    "id_ed25519",
    "id_rsa",
}
SENSITIVE_SUFFIXES = {".jks", ".key", ".keystore", ".p12", ".pfx", ".pem"}
HOME_PATH_PATTERNS = (
    re.compile(r"/(?:Users|home)/[A-Za-z0-9._-]+(?:/|\b)"),
    re.compile(r"[A-Za-z]:\\Users\\[^\s\\]+", re.IGNORECASE),
)
SECRET_PATTERNS = (
    ("private key", re.compile(r"-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY-----")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b")),
    ("npm token", re.compile(r"\bnpm_[A-Za-z0-9]{20,}\b")),
    ("AWS access key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b")),
    ("OpenAI token", re.compile(r"\bsk-(?:proj|svcacct)-[A-Za-z0-9_-]{20,}\b")),
    ("Anthropic token", re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,}\b")),
    ("Stripe secret", re.compile(r"\b[rs]k_(?:live|test)_[A-Za-z0-9]{16,}\b")),
    (
        "assigned secret",
        re.compile(
            r"(?i)\b(?:api[_-]?key|access[_-]?token|client[_-]?secret|private[_-]?key)"
            r"\s*[:=]\s*[\"']?[A-Za-z0-9_./+=-]{20,}"
        ),
    ),
)
EMAIL_PATTERN = re.compile(r"\b[A-Z0-9._%+-]+@([A-Z0-9.-]+\.[A-Z]{2,})\b", re.IGNORECASE)
ALLOWED_EMAIL_DOMAINS = {
    "example.com",
    "example.net",
    "example.org",
    "users.noreply.github.com",
}


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


def validate_payload_file(skill: pathlib.Path, path: pathlib.Path, check: Validation) -> None:
    relative = path.relative_to(skill)
    hidden_parts = [part for part in relative.parts if part.startswith(".")]
    check.require(not hidden_parts, f"{path}: hidden payload paths are not allowed")

    name = path.name.lower()
    check.require(
        name not in SENSITIVE_FILENAMES and not name.startswith(".env."),
        f"{path}: sensitive credential filename is not allowed",
    )
    check.require(
        path.suffix.lower() not in SENSITIVE_SUFFIXES,
        f"{path}: sensitive key or credential file type is not allowed",
    )

    size = path.stat().st_size
    check.require(
        size <= MAX_PAYLOAD_BYTES,
        f"{path}: payload exceeds {MAX_PAYLOAD_BYTES // (1024 * 1024)} MiB",
    )
    if size > MAX_PAYLOAD_BYTES:
        return

    data = path.read_bytes()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        check.require(
            path.suffix.lower() in ALLOWED_BINARY_SUFFIXES,
            f"{path}: unexpected binary payload",
        )
        return

    check.require("\x00" not in text, f"{path}: unexpected binary payload")
    for pattern in HOME_PATH_PATTERNS:
        check.require(
            pattern.search(text) is None,
            f"{path}: leaks an absolute workstation home path",
        )
    for label, pattern in SECRET_PATTERNS:
        check.require(pattern.search(text) is None, f"{path}: contains a possible {label}")
    for domain in EMAIL_PATTERN.findall(text):
        check.require(
            domain.lower() in ALLOWED_EMAIL_DOMAINS,
            f"{path}: contains a non-allowlisted email address",
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
        if not path.is_file():
            continue
        validate_payload_file(skill, path, check)

    skill_text = skill_md.read_text(encoding="utf-8")
    for reference in re.findall(r"`((?:references|scripts|assets)/[^`]+)`", skill_text):
        check.require((skill / reference).exists(), f"{skill.name}: missing referenced path {reference}")

    validate_openai_yaml(skill, check)
    validate_evals(skill, check)


def discover_skills() -> list[pathlib.Path]:
    return sorted(path.parent for path in SKILLS_ROOT.rglob("SKILL.md"))


def main() -> None:
    check = Validation()
    unexpected_root = sorted(
        path.name for path in REPO_ROOT.iterdir() if path.name not in ALLOWED_REPO_ROOT
    )
    check.require(
        not unexpected_root,
        f"unexpected repository-root entries: {unexpected_root}",
    )

    skills = discover_skills()
    check.require(bool(skills), "no exported skills found")
    names: dict[str, pathlib.Path] = {}
    for skill in skills:
        relative = skill.relative_to(SKILLS_ROOT)
        check.require(
            len(relative.parts) == 2,
            f"{relative}: skill must live at skills/<category>/<name>",
        )
        validate_skill(skill, check)
        values = parse_frontmatter(skill / "SKILL.md", check)
        name = values.get("name")
        if name in names:
            check.require(
                False,
                f"duplicate skill name {name}: {names[name]} and {skill}",
            )
        elif name:
            names[name] = skill
    if check.errors:
        # Do not emit individual diagnostics here. This validator deliberately
        # inspects payloads for secrets, so a shared error collection must never
        # become a path for repository content to reach public CI logs.
        print(
            f"ERROR: validation failed with {len(check.errors)} policy violation(s)",
            file=sys.stderr,
        )
        raise SystemExit(1)
    print(f"Validated {len(skills)} skill(s): {', '.join(path.name for path in skills)}")


if __name__ == "__main__":
    main()
