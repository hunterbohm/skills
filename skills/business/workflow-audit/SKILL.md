---
name: workflow-audit
description: "Audit a business's recurring workflows from connected sources, in a durable audit workspace that compounds across runs. Use when an owner wants to know where work gets stuck, what to automate first, how to build a supervised agent workflow, or what changed since the last audit."
---

# Workflow Audit

Turn a connected business workspace into a source-backed workflow map and one implementation-ready build plan. The deliverable is self-serve and contains no sales pitch.

When the owner asks why the audit works this way, or when assembling the deliverable's further-reading section, read `references/agency-connected-agent-field-guide.md`. Do not load it to run the audit.

## Operating boundaries

- **Read first.** Treat the owner's systems as read-only: do not send messages, edit records, create automations in their tools, change permissions, or publish anything. Writes land only in the audit workspace and the recorded `<audit-root>` answer.
- **Minimum scope.** Inspect only sources needed to understand recurring workflows.
- **Private by default.** Do not copy secrets, raw private messages, employee-performance commentary, legal material, health data, or client-confidential content into the deliverable.
- **Evidence over inference.** Label each workflow as `observed`, `owner-reported`, or `inferred`. An inferred workflow cannot become the first build until the owner confirms it.
- **No invented economics.** Time, frequency, hourly value, error rate, and revenue impact must come from the owner or a cited system record. Unknown stays unknown.
- **Approval is not execution.** The final build spec defines approval gates; it does not grant the agent permission to activate the workflow.

## The audit workspace

Every business gets one durable folder that all runs share. Its layout, the
`state.json` ledger schema, the workflow state machine, the run-log format,
and the realized-value formulas are all defined in
`references/workspace-contract.md` — load it before reading or writing any
workspace state.

If the business's folder does not exist under the confirmed `<audit-root>`,
this is a **first run**: load `references/first-run.md` and execute its steps
1–8. If it exists, this is a **resume run**: read `state.json` before
touching any source, then follow "Resume runs" below.

## Resume runs

The ledger, not a fresh audit, is the starting point. On a resume run:

1. **Diff, do not re-audit.** Re-verify only sources whose `last_verified` age
   matters for the question at hand. Record what changed since the last run.
   Current claims come from re-verified sources — a summary or the prior
   audit document is history, not evidence.
2. **Verify claimed statuses.** Promote or demote only per the state machine
   in `references/workspace-contract.md`, checked against each workflow's
   `runs.jsonl` rather than the ledger's word.
3. **Report returned value.** For each built workflow, compute realized value
   and adoption from `runs.jsonl` against its `baseline`, per the workspace
   contract.
4. **Apply stored corrections** as standing rules for this business before
   producing anything new, and capture any new owner corrections the same
   way.
5. **Expand only by evidence.** Propose the next workflow from `runner_ups`
   only when the current first workflow has reached `proven` (status
   `proven`, `enabled`, or `reliable`). Until then, the run's output is the
   diff, the current status, and the blockers.
6. **Update, do not rewrite.** Amend `workflow-audit.md`, regenerate
   `owner-summary.md`, append one entry to `runs`, and keep prior decisions
   visible.

Completion criterion: the ledger reflects verified current state, and the
owner sees what changed, what advanced, and the single next action.

## Verification checklist

Before ending any run:

- [ ] The owner's systems were touched read-only; writes landed only in the audit workspace and the recorded `<audit-root>` answer.
- [ ] Private or regulated material stayed out of the deliverable.
- [ ] Every workflow is observed, owner-reported, or explicitly inferred.
- [ ] Every metric traces to a source and unit.
- [ ] Current state is separated from historical intent.
- [ ] One workflow was chosen and confirmed.
- [ ] The build spec includes gate, idempotency, verify, and rollback behavior.
- [ ] The fixture and first real-run acceptance criteria are concrete.
- [ ] The final files are self-serve and contain no sales pitch.
- [ ] `state.json` agrees with the delivered documents and records this run.
- [ ] `owner-summary.md` is current and readable by a non-technical owner.
