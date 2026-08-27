# Resume run

The ledger is the starting point. A resume run diffs; it does not re-audit.

1. **Diff.** Re-verify only the sources whose `last_verified` date is older than the claim you will make from them. Evidence comes from re-verified sources. The prior audit document is history. Done when every source you cite carries a `last_verified` on or after the claim, and the changes since the last run are listed.
2. **Verify statuses.** Move a status only per the ladder in `references/workspace-contract.md`, checked against the workflow's `runs.jsonl`, not the ledger's current `status` field. Done when every status in the inventory cites the run entry or spec that earns it.
3. **Report realized value.** For each workflow at `proven` or `live`, compute realized value per the contract's value formulas. Report the adoption gap for each `live` workflow. Done when every figure traces to run entries and the baseline.
4. **Apply corrections.** Stored `corrections` are standing rules for this business. Apply them before you produce anything new. Capture new owner corrections the same way. Done when every new owner correction from this run is a dated entry.
5. **Expand on evidence.** Propose the next workflow from `runner_ups` only when the first has reached `proven`. When the owner confirms it, load `references/build-spec.md` and write `specs/<n>-<slug>-build-spec.md` for that workflow. Set its status to `designed`. Hand off per first-run step 8. This run's mode stays `resume`. Until then, the run's output is the diff, the current status, and the blockers. Done when the owner has one next action, or the confirmed workflow is `designed` and handed off.
6. **Amend.** Update `workflow-audit.md` in place. Keep prior decisions visible.

Done when the ledger reflects verified current state, and the owner sees what changed, what advanced, and the single next action.
