---
name: workflow-audit
description: "Audit a business's recurring workflows from connected sources and pick one to automate first. Use when asked what to automate first, or what changed since the last audit."
---

# Workflow audit

Turn a business's connected sources into a source-backed workflow inventory and one build spec. Write the deliverable so the owner can act on it without a call.

## Boundaries

- **Read-only.** The owner's systems stay read-only for the whole audit, including their automation tools and permissions. Writes go to the audit workspace and the recorded `<audit-root>` answer only.
- **Minimum scope.** Read the smallest slice of sources that explains the recurring work.
- **One system of record.** Recommendations point at the owner's existing tools. The audit workspace is the only thing the audit creates.
- **Private by default.** Cite sources. Secrets, raw private messages, staff-performance comments, legal, health, and customer-confidential content stay in the source system.
- **Evidence labels.** Every workflow is `observed`, `owner-reported`, or `inferred`.
- **Owner's numbers only.** Time, frequency, hourly value, error rate, and revenue at stake come from the owner or a cited record. Unknown stays unknown.
- **Approval is a gate, not a switch.** The build spec names who approves each action. Activation happens in `workflow-build`, on the owner's explicit instruction.

## The workspace

Every business has one durable folder that all runs share. `references/workspace-contract.md` defines its layout, the `state.json` ledger, the ladder, the run log, and the value formulas. Load that file before you read or write the ledger.

Then route on the ledger:

- If no folder for this business exists under `<audit-root>`, this is a **first run**. Load `references/first-run.md` and complete every step. Step 6 loads `references/build-spec.md`.
- If the folder exists, the first run is **unfinished** when either holds:
  - `first_workflow` is empty;
  - the first workflow is below `built`, `runs` has no `build` entry, and `corrections` has no build deferral.

  Read `state.json`. Load `references/first-run.md` and continue at the first step whose completion criterion the ledger does not yet satisfy.
- Otherwise this is a **resume run**. Read `state.json` before you touch any source. Then load `references/resume-run.md`. Its step 5 loads `references/build-spec.md` when the owner confirms a runner-up.

Every run ends the same way. Regenerate `owner-summary.md` per `references/owner-summary.md`. Append one entry to the ledger's `runs` with mode `first` or `resume`. Each branch file carries its own completion criterion.
