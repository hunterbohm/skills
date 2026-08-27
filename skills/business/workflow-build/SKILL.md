---
name: workflow-build
description: "Move a workflow from its workflow-audit spec up the ladder to live, on the owner's runtime. Use when asked to build, prove, activate, or report on an automation; with no spec it routes to workflow-audit first."
---

# Workflow build

Move one workflow up the ladder with evidence at every rung. The skill runs inside an existing audit workspace, on the runtime the owner already has.

## Preconditions

Read, in order: `references/workspace-contract.md`, `state.json`, then the spec in `specs/` for the workflow whose status is `designed` or higher. If more than one workflow is at `designed` or higher, take the one the request names. With no name, ask the owner which one before you read its spec. If the workspace or that spec is missing, run `workflow-audit` first.

Route on the ledger status and the request, one branch per run:

- `designed` means Build.
- `built` means Prove.
- `proven` with an owner request to activate means Go live.
- A request for the run log or realized value means Report, at any status.

End every run by naming the next rung.

## Boundaries

- **Built is not live.** Implementation, fixtures, and dry-runs write nothing to a real destination. The Prove branch performs one real act, on the approver's approval. Only the Go live branch activates a production trigger.
- **Spec first.** A needed deviation goes into the spec, then into the implementation.
- **Secrets stay in the secret manager.** Workspace files hold the names of secrets.
- **Statuses move on evidence.** Follow the contract's ladder.

## Build

1. Load `references/runtime-rules.md`. Implement the spec on the runtime the owner already runs: their agent's scheduler, a cron job, an automation platform, or a script.
2. Write `workflows/<n>-<slug>/implementation.md`. It answers five questions:
   - where the implementation lives;
   - how to run it;
   - how to switch dry-run and live;
   - how to stop it;
   - where the runtime keeps its external run records, if it cannot append to `runs.jsonl`.
3. Run the fixture end to end with the act stage in dry-run. Fix until it passes. A fixture that cannot pass is a spec defect. Go back to the spec.
4. Set the ledger status to `built`. Cite the passing fixture run in the ledger notes.

Done when the fixture passes from a clean invocation, `implementation.md` answers all five questions, and the ledger says `built`.

## Prove

1. Switch the act stage from dry-run to live for this one run, per `implementation.md`. Return it to dry-run when the run ends.
2. Walk the approver through the spec's acceptance run, criterion by criterion.
3. When every criterion passes, set status `proven`. Cite the run entry, the approver, and the verification result in the ledger notes.
4. If any criterion fails, set the status to `designed`. Record the failure in the run entry. Cite the run entry, the approver, and the verification result in the ledger notes. Go back to the spec. The next run is Build, so the fixture passes again before another real act.

Done when the act stage is back in dry-run and the run's entry is in `runs.jsonl`. The status is `proven` on a pass or `designed` on a fail. The ledger notes cite the run entry, the approver, and the verification result.

## Go live

1. Confirm the ledger shows `proven` and `runs.jsonl` holds the passing acceptance run. If not, stop and name the Prove branch as the next action.
2. Act only on the owner's explicit request to activate the production trigger. If the request is not explicit, ask the owner one yes-or-no question.
3. Record the instruction in the ledger's `corrections`.
4. Switch the act stage to live per `implementation.md`. Activate the trigger.
5. Set status `live`.

Done when the status was `proven` before activation, the trigger is active, the act stage is live, and the instruction is in `corrections`.

## Report

On a request for the run log or realized value:

1. If `implementation.md` names external run records, import them into `runs.jsonl` by `run_id` first.
2. Read `runs.jsonl` and the ledger `baseline`.
3. Show the run log in plain language: when, what triggered it, who approved, verified or not. Failures are as visible as successes.
4. Compute realized value per the contract. Report the adoption gap when the workflow is `live`.

Done when every claim traces to a run entry or the baseline.

## After every branch

Regenerate `owner-summary.md` per `references/owner-summary.md`. Append one entry to the ledger's `runs` with mode `build`, `prove`, `live`, or `report`.
