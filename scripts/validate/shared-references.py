#!/usr/bin/env python3
"""Fail when a reference vendored into two skills drifts.

Each published skill installs on its own, so a shared file is copied into every
package that needs it. The first path is canonical; the rest must match it byte
for byte.
"""
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2] / "skills"
SHARED = (
    (
        "business/ops-audit/references/principles.md",
        "business/ops-foundation/references/principles.md",
    ),
    (
        "business/ops-audit/references/workspace-contract.md",
        "business/ops-foundation/references/workspace-contract.md",
    ),
)


def main() -> None:
    errors: list[str] = []
    for canonical, *copies in SHARED:
        source = ROOT / canonical
        if not source.is_file():
            errors.append(f"missing canonical shared reference: {canonical}")
            continue
        expected = source.read_bytes()
        for relative in copies:
            copy = ROOT / relative
            if not copy.is_file():
                errors.append(f"missing vendored shared reference: {relative}")
            elif copy.read_bytes() != expected:
                errors.append(
                    f"shared reference drift: {relative} differs from {canonical}; "
                    "copy the canonical file over it"
                )
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        raise SystemExit(1)
    print(f"Shared references OK ({len(SHARED)} pair(s))")


if __name__ == "__main__":
    main()
