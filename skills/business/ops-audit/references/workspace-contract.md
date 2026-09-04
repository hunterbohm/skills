# Workspace contract

The owner chooses one folder when durable files are needed. The owner reads nothing in it; the plan is read back in chat.

```text
<workspace>/
├── business.md    # interview record, in the owner's words
├── sources.md     # source map: per source, truth owned, who reads, who approves a write, currency, write check
├── roadmap.json   # the plan and the cards behind it
├── state.json     # roadmap identity, evidence status, change record, approval, step status
└── mining/        # redacted session digests per host and harness; private, never committed or shared
```

Read `state.json` before every write. Preserve roadmap ID, revision, card IDs and versions, consent, exclusions, evidence references, the change record, step status, and partial-stop status. Preserve conflicting inputs and stop.

## Feedback and revisions

The owner speaks in chat. The agent applies the change to `roadmap.json`, increments `revision` in both files, appends `{revision, date, summary}` to `state.changes`, and reads the plan back. Never edit a card or a step without a change entry. Approval binds one revision; a change after approval needs a new approval.

## Step status

`state.steps` is keyed by card ID: `{"status": ..., "note": ..., "date": ...}`. A move or automation runs `proposed → approved → done`; a hold runs `holding → ended`. A missing entry means the first status. `approved` carries the owner's words; `done` carries what was done and how it was checked. Status changes never touch the plan revision.

`scripts/workspace.py` is the only writer of step status and the only printer of the plan. `plan` validates both files and prints the plan as chat text, the title and the one decision per step, or every line with `--full`. `step` refuses to move anything on a plan that is not approved at its current revision, moves a step one status forward, refuses a main-lane step until every earlier main-lane step is done, refuses any change without a note, and prints the plan afterwards.

## Eligibility

A main-lane step is eligible when every earlier main-lane step is done. A parallel-lane step is eligible at once. A hold is never taken.
