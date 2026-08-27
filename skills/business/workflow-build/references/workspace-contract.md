# Workspace contract

The shared contract for audit workspaces, read and written by `workflow-audit` and `workflow-build`.

## Layout

```text
<audit-root>/<business-slug>/
├── state.json                     # the ledger: memory across runs
├── workflow-audit.md              # living audit document
├── owner-summary.md               # one-page owner view, regenerated every run
├── specs/
│   └── <n>-<slug>-build-spec.md   # n = the workflow's 1-based position in inventory
└── workflows/
    └── <n>-<slug>/
        ├── implementation.md      # where the build lives and how to run it
        └── runs.jsonl             # run log, one line per run
```

Ask the owner once where `<audit-root>` lives. Record the answer in the agent's instruction file or memory, so later runs do not ask again.

## Ledger: state.json

```json
{
  "business": "",
  "source_map": [{"source": "", "authority": "", "access": "", "boundary": "", "last_verified": ""}],
  "inventory": [{"name": "", "evidence": "observed|owner-reported|inferred",
                 "status": "candidate|designed|built|proven|live|rejected",
                 "baseline": {"runs_per_month": null, "hours_per_run": null, "hourly_value": null, "source": ""},
                 "notes": ""}],
  "first_workflow": "",
  "runner_ups": [],
  "corrections": [{"date": "", "rule": "", "superseded_by": ""}],
  "runs": [{"date": "", "mode": "first|resume|build|prove|live|report", "changes": ""}]
}
```

`corrections` holds dated standing rules and recorded owner decisions: style and scope corrections captured on any run, build deferrals, and go-live instructions. It is append-only. To supersede an entry, set its `superseded_by` to the date of the new one.

## Ladder

The ladder is `candidate → designed → built → proven → live`, plus `rejected`. A status moves up only on this evidence:

- **candidate.** In the inventory, not chosen.
- **rejected.** Ruled out by the owner or by a failed confirmation. The reason stays in `notes`.
- **designed.** A build spec for the owner-confirmed workflow exists in `specs/`.
- **built.** The fixture passes end to end with the act stage in dry-run.
- **proven.** One real run, cleared at the gate by the named approver, passed the spec's acceptance run.
- **live.** The production trigger is active, on an explicit owner instruction recorded in `corrections`. Requires a prior `proven` run.

A status moves down when its evidence no longer holds. A failed acceptance run moves the workflow to `designed`. A failed real run after that moves `proven` to `built`, or to `designed` if the spec changes. A deactivated trigger moves `live` to `proven`. A workflow "has reached `proven`" when its status is `proven` or `live`.

## Run log: workflows/<n>-<slug>/runs.jsonl

The runtime's log stage appends one JSON line per run. If the runtime cannot append to it, `implementation.md` names the runtime's external run records, and the report branch imports them by `run_id`.

```json
{"run_id": "", "idempotency_key": "", "ts": "", "mode": "fixture|real",
 "trigger": "", "approver": "", "approved_ts": "", "action_id": "",
 "source_refs": [], "model": "", "verified": true, "failure": null,
 "notes": ""}
```

`verified` comes from the read-back: `true`, `false`, or `"pending"`. Log source references and secret names only.

## Value formulas

Baseline cost, from the owner's own numbers:

```text
hours/month        = runs/month × hours/run
annual labor value = hours/month × 12 × stated hourly value
```

Realized value, from the run log against the baseline:

```text
realized hours = verified real runs × baseline hours_per_run
realized value = realized hours × baseline hourly_value   (only when stated)
adoption gap   = baseline runs_per_month minus verified real runs per month, from runs.jsonl
```

Count only verified real runs. If `implementation.md` names external run records, import them into `runs.jsonl` by `run_id` before you count. Every figure is an estimate from the owner's own baseline numbers, not a measurement. A live workflow with an adoption gap is a finding, not a success.
