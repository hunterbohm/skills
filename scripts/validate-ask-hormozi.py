#!/usr/bin/env python3
"""Validate Ask Hormozi evidence, attribution, and accounting invariants."""

from __future__ import annotations

import json
import pathlib
import re
import sys
from collections import Counter


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL = REPO_ROOT / "skills" / "ask-hormozi"
WORD_RE = re.compile(r"\b[\w’'-]+\b", re.UNICODE)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_evidence(errors: list[str]) -> None:
    evidence = SKILL / "references" / "evidence"
    manifest = json.loads((evidence / "manifest.json").read_text(encoding="utf-8"))
    headings = 0
    states: Counter[str] = Counter()
    exact_domains: Counter[str] = Counter()
    paraphrase_without_url = 0

    for path in sorted(evidence.glob("*.md")):
        if path.name == "index.md":
            continue
        text = path.read_text(encoding="utf-8")
        headings += len(re.findall(r"^### ", text, re.MULTILINE))
        states["exact_linked_excerpt"] += text.count("· exact linked excerpt ·")
        states["paraphrase_only"] += text.count(
            "· paraphrase only; no exact linked excerpt shipped ·"
        )
        states["book_or_source_citation"] += text.count("· cited, not excerpted ·")
        if "files.flightcast.com" in text:
            fail(errors, f"{path}: contains a raw transcript-host URL")

        for chunk in re.split(r"(?m)^### ", text)[1:]:
            is_exact = "· exact linked excerpt ·" in chunk
            is_paraphrase = "· paraphrase only; no exact linked excerpt shipped ·" in chunk
            urls = re.findall(r"https?://[^)\s]+", chunk)
            if is_exact:
                if not urls:
                    fail(errors, f"{path}: exact excerpt has no public link")
                source_line = next(
                    (line for line in chunk.splitlines() if "· exact linked excerpt ·" in line),
                    "",
                )
                source_url = re.search(r"https?://[^)\s]+", source_line)
                if source_url:
                    domain = source_url.group(0).split("/", 3)[2].removeprefix("www.")
                    exact_domains[domain] += 1
            if is_paraphrase and not urls:
                paraphrase_without_url += 1

        for quote in re.findall(r'^> [“"](.+?)[”"]$', text, re.MULTILINE):
            if len(WORD_RE.findall(quote)) > 20:
                fail(errors, f"{path}: public excerpt exceeds 20 words: {quote}")

    if headings != manifest["source"]["term_count"]:
        fail(errors, f"evidence has {headings} terms; manifest differs")
    if dict(states) != manifest["evidence_counts"]:
        fail(errors, f"evidence states {dict(states)} differ from manifest")
    if exact_domains != Counter({"youtube.com": 84, "rosetta.to": 27}):
        fail(errors, f"exact source-page mix changed: {dict(exact_domains)}")
    if paraphrase_without_url != 21:
        fail(errors, f"title-only paraphrase count changed: {paraphrase_without_url}")

    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    revision = manifest["source"]["revision"]
    for required in (revision[:12], "84 original YouTube", "27 public transcript-mirror", "21 title-level"):
        if required not in readme:
            fail(errors, f"README missing provenance detail: {required}")


def validate_frameworks(errors: list[str]) -> None:
    references = SKILL / "references"
    for path in sorted(references.glob("*.md")):
        if path.name == "live-research.md":
            continue
        text = path.read_text(encoding="utf-8")
        if re.search(r"(?m)^> ", text):
            fail(errors, f"{path}: framework guide contains a block quote")
        if re.search(r"“[^”]+”", text) or re.search(r'(?<![\w])"[^"\n]+"', text):
            fail(errors, f"{path}: framework guide contains quote-like wording")
        if len(text.splitlines()) > 100:
            fail(errors, f"{path}: framework guide exceeds 100 lines")


def main() -> None:
    errors: list[str] = []
    skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    description_match = re.search(r'^description: "([^"]+)"$', skill_text, re.MULTILINE)
    if not description_match:
        fail(errors, "SKILL.md missing a quoted one-line description")
    else:
        description = description_match.group(1)
        if len(description.split()) > 70:
            fail(errors, "SKILL.md description exceeds 70 words")
        if not description.startswith("Apply Alex Hormozi"):
            fail(errors, "SKILL.md description must front-load the Hormozi invocation")
        if "Route to" in description:
            fail(errors, "SKILL.md description contains body-level process")
    required_process = (
        "## 1. Route the request",
        "## 2. Set the fit",
        "## 3. Diagnose the constraint",
        "## 4. Load one guide and its receipts",
        "## 5. Resolve the receipt state",
        "## 6. Show only decision-changing math",
        "## 7. Deliver the branch contract",
        "The response is complete only when",
    )
    for required in required_process:
        if required not in skill_text:
            fail(errors, f"SKILL.md missing process contract: {required}")
    for branch in ("Explain", "Advise", "Audit", "Execute", "Verify"):
        if f"**{branch}:**" not in skill_text:
            fail(errors, f"SKILL.md missing branch: {branch}")
    if skill_text.count("Completion criterion:") != 6:
        fail(errors, "SKILL.md must keep six step-level completion criteria")
    if "gross profit > 2 x (CAC + COGS)" in skill_text:
        fail(errors, "SKILL.md mixes gross-profit and old cash-rule accounting")
    if (SKILL / "references" / "maxims.md").exists():
        fail(errors, "quote-heavy maxims.md must not ship")

    evals = json.loads((SKILL / "evals" / "evals.json").read_text(encoding="utf-8"))
    if len(evals.get("evals", [])) != 10:
        fail(errors, "ask-hormozi must keep 10 focused evals")

    validate_evidence(errors)
    validate_frameworks(errors)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
    print("Validated Ask Hormozi evidence and attribution invariants")


if __name__ == "__main__":
    main()
