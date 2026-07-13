#!/usr/bin/env python3
"""Exercise the release-payload security checks without a test framework."""

from __future__ import annotations

import importlib.util
import pathlib
import tempfile


VALIDATOR_PATH = pathlib.Path(__file__).with_name("validate.py")
SPEC = importlib.util.spec_from_file_location("public_skill_validator", VALIDATOR_PATH)
if SPEC is None or SPEC.loader is None:
    raise SystemExit(f"could not load validator: {VALIDATOR_PATH}")
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def validate_file(name: str, content: bytes) -> list[str]:
    with tempfile.TemporaryDirectory(prefix="skill-security-check-") as raw:
        skill = pathlib.Path(raw) / "fixture"
        path = skill / name
        path.parent.mkdir(parents=True)
        path.write_bytes(content)
        check = validator.Validation()
        validator.validate_payload_file(skill, path, check)
        return check.errors


def require_rejection(name: str, content: bytes, expected: str) -> None:
    errors = validate_file(name, content)
    if not any(expected in error for error in errors):
        raise SystemExit(f"{name}: expected rejection containing {expected!r}; got {errors}")


def main() -> None:
    require_rejection(".env", b"SAFE=value\n", "sensitive credential filename")
    require_rejection(
        "notes.md",
        b"Local file: /Users/example/private.txt\n",
        "workstation home path",
    )
    require_rejection(
        "notes.md",
        ("ghp_" + "A" * 36).encode(),
        "possible GitHub token",
    )
    require_rejection("archive.zip", b"PK\x03\x04\x00\xff", "unexpected binary payload")
    require_rejection("contact.md", b"owner@personal.invalid\n", "non-allowlisted email")

    allowed_errors = validate_file("image.png", b"\x89PNG\r\n\x1a\n\x00")
    if allowed_errors:
        raise SystemExit(f"allowlisted image fixture was rejected: {allowed_errors}")
    print("Validated release-payload security rejection cases")


if __name__ == "__main__":
    main()
