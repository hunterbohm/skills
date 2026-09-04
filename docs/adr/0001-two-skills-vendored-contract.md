Status: superseded by ADR 0009 (one skill; nothing vendored).

# Two skills sharing a vendored workspace contract

`workflow-build` cannot run without a `workflow-audit` workspace, and both read the same ledger, state machine, and owner-summary template. Merging them into one skill was considered on 2026-08-27 and rejected: the audit and the build are different jobs with different trigger words ("audit", "what should we automate" versus "build it", "go live", "how is it doing"), and a build session should not carry the audit's eight steps in context. Decision: keep two skills. The shared references (`workspace-contract.md`, `owner-summary.md`) are vendored byte-identical into both packages, canonical in `workflow-audit`, because each published skill installs on its own and a cross-package path dangles. `scripts/validate/shared-references.py` fails on drift.

Consequences: edit the `workflow-audit` copy, then copy it over the `workflow-build` copy. Renaming a state or a ledger field is a two-package change.
