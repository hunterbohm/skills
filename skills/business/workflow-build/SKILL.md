---
name: workflow-build
description: "Build, prove, and report on workflows specced by the workflow-audit skill. Use when the workflow-audit skill hands off a confirmed workflow, when the owner asks to build or implement a specced workflow, or when the owner asks for run history or what an automation has returned."
---

# Workflow Build

Move one workflow up the maturity ladder — `designed → built → proven →
enabled` — with evidence at every rung. This skill is the motor for the state
machine the workflow-audit skill creates; it always operates inside an
existing audit workspace.

## Preconditions

Read, in order: `references/workspace-contract.md` (the layout, ledger, state
machine, run log, and value formulas used below — the same contract the
workflow-audit skill ships), then `state.json`, then the confirmed spec in
`specs/`. If the workspace or spec is missing, run the workflow-audit skill
first — never build from a verbal description.

## Boundaries

- **Built is not live.** Scaffolding, fixtures, and dry runs are always safe.
  Activating a production trigger or pointing the act step at a real
  destination happens only on the owner's explicit, recorded instruction.
- **The spec is the contract.** A needed deviation goes into the spec first,
  then into code.
- **Secrets stay out of the workspace.** Use the environment's secret
  manager; workspace files hold the names of secrets, never values.
- **Statuses move on evidence only**, per the state machine in
  `references/workspace-contract.md`.

## Branch: Build

1. Load `references/scaffold.md` and create `workflows/<n>-<slug>/` from the
   spec: deterministic runner, fixed joint prompt, fixture, dry-run act
   adapter.
2. Run the fixture end to end with the act step in dry-run. Fix until it
   passes; a fixture that cannot pass goes back to the spec as a defect.
3. On pass: set the workflow's ledger status to `built`. The runner's log
   stage already recorded the fixture run in `runs.jsonl`.

Completion criterion: the fixture passes from a clean invocation and the
ledger says `built`.

## Branch: Prove and enable

1. Walk the owner through the spec's first-real-run acceptance: current
   inputs, schema-valid output, approval by the named approver, one act,
   verification by source read-back, one `runs.jsonl` entry.
2. All acceptance points pass → status `proven`.
3. The owner explicitly asks to activate the production trigger → activate,
   record the instruction in the ledger's `corrections`, status `enabled`.

Completion criterion: every status change in this branch cites its evidence —
run entry, approver, verification result — in the ledger notes.

## Branch: Report

On "show the logs", "how is it doing", or "what has this returned":

1. Read `runs.jsonl` and the workflow's ledger `baseline`.
2. Show the run history in plain language: when, what triggered it, who
   approved, verified or not — failures as visible as successes.
3. Compute realized value and adoption per
   `references/workspace-contract.md`.

Completion criterion: every claim in the report traces to a run entry or the
baseline.

## Owner summary

After every branch, regenerate `owner-summary.md` per
`references/owner-summary.md`, and append one entry to the ledger's `runs` —
mode `build`, `prove`, or `report` to match the branch that ran.
