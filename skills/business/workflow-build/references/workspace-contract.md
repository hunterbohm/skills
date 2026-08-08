# Workspace contract

The shared state contract for audit workspaces. The workflow-audit and
workflow-build skills both read and write against this file; no other file
defines these shapes. Load it before reading or writing any workspace state.

## Layout

```text
<audit-root>/<business-slug>/
├── state.json                     # the ledger — memory across runs
├── workflow-audit.md              # living audit document
├── owner-summary.md               # one-page owner view, regenerated every run
├── specs/
│   └── <n>-<slug>-build-spec.md   # n = the workflow's ledger order
└── workflows/
    └── <n>-<slug>/                # built runner + run log
```

Ask the owner once where `<audit-root>` lives, and record the answer where the
runtime will find it again — the invoking project's instruction file or the
agent's memory — so later runs do not re-ask.

## Ledger — state.json

```json
{
  "business": "",
  "source_map": [{"source": "", "authority": "", "access": "", "boundary": "", "last_verified": ""}],
  "inventory": [{"name": "", "evidence": "observed|owner-reported|inferred",
                 "status": "candidate|designed|built|proven|enabled|reliable|rejected",
                 "baseline": {"runs_per_month": null, "hours_per_run": null, "hourly_value": null, "source": ""},
                 "notes": ""}],
  "first_workflow": "",
  "runner_ups": [],
  "corrections": [{"date": "", "rule": ""}],
  "runs": [{"date": "", "mode": "first|resume|build|prove|report", "changes": ""}]
}
```

`corrections` holds dated standing rules and recorded owner decisions: style
and scope corrections captured on any run, build deferrals, and trigger
activation instructions. Entries are never deleted; superseded ones are
marked in place.

## Workflow states

`candidate → designed → built → proven → enabled → reliable`, plus
`rejected`. A status moves — in either direction — only on this evidence:

- **candidate** — in the inventory, not chosen.
- **rejected** — ruled out by the owner or a failed confirmation; the reason
  stays in `notes`.
- **designed** — a confirmed build spec exists in `specs/`.
- **built** — the fixture passes end to end with the act step in dry-run.
- **proven** — one real, owner-approved run passed the spec's acceptance
  test.
- **enabled** — the production trigger is active, on an explicit owner
  instruction recorded in `corrections`; requires a prior `proven`
  acceptance run.
- **reliable** — `runs.jsonl` shows repeated verified real runs across an
  observation window the owner agreed to.

A workflow "has reached `proven`" when its status is `proven`, `enabled`, or
`reliable` — later rungs never un-prove it.

## Run log — workflows/<n>-<slug>/runs.jsonl

One JSON line per run, appended only by the runner's log stage:

```json
{"run_id": "", "idempotency_key": "", "ts": "", "mode": "fixture|real",
 "trigger": "", "approver": "", "approved_ts": "", "action_id": "",
 "source_refs": [], "model": "", "verified": true, "failure": null,
 "notes": ""}
```

`verified` is `true`, `false`, or `"pending"` — never assumed. Log source
references, never raw sensitive content and never secrets.

## Realized value

```text
returned hours = verified real runs × baseline hours_per_run
returned value = returned hours × baseline hourly_value   (only when stated)
adoption gap   = baseline runs_per_month vs actual run rate
```

Every figure is an estimate from the owner's own baseline numbers, not a
measurement. A live workflow with an adoption gap is a finding, not a
success.
