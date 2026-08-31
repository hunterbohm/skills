# Workspace contract

The owner chooses one folder when durable files are needed. `roadmap.html` is the only owner-facing audit result. The same folder becomes the foundation after approved handoff.

```text
<workspace>/
├── business.md                     # audit interview record
├── roadmap.json                    # complete, owner-approved audit data
├── roadmap.html                    # sole owner-facing audit result
├── state.json                      # roadmap identity, approval, feedback, foundation state
├── README.md                       # workspace map, never an audit report
├── rules.md                        # owner-approved concrete rules only
├── receipts.jsonl                  # normalized append-only run evidence
└── workflows/<card-id>/contract.json # runtime and implementation contract
```

Read `state.json` before every write. Preserve immutable roadmap ID, revision, card IDs and versions, consent, exclusions, evidence references, feedback identities, pending feedback, partial-stop status, and feedback-first resume behavior. A handoff is eligible only when `roadmap.json` and `state.json` have matching ID/revision, no pending feedback, and identical `owner_approval` records binding that ID/revision, named approver, and timestamp. Preserve conflicting inputs and stop.

## Foundation state and writes

`state.json` additionally records `foundation`: `{"status":"absent|installed","installed_at":null,"revision":0}` and `workflows`, keyed by stable card ID. Each workflow has `status` (`candidate`, `designed`, `built`, `proven`, `live`), `revision`, and receipt IDs. All mutable workspace files use the exclusive lock and same-directory atomic replacement. Re-initialization creates only missing map/rules/receipt files and never replaces owner content. A revision mismatch is a conflict: preserve files and stop. Workspace scripts require POSIX Python 3; the implemented automation remains runtime-neutral.

## Ladder and evidence

`candidate → designed → built → proven → live`. `built` requires a verified dry-run fixture receipt. `proven` requires a current verified real receipt, named approval when the approved card requires it, destination read-back, and recorded `replay_verified: true`. `live` requires prior proven status plus a verified activation receipt with `explicit_instruction: true` and active-trigger read-back. A failed supporting proof automatically regresses status.

## Runtime records and reporting

Each workflow contract records the implementation location, run, switch, and stop/read-back instructions plus its runtime-owned record source. Runtimes that cannot append locally expose their source; report imports and normalizes it before computing results. For requested `YYYY-MM`, count only unique verified real receipts in that month:

```text
realized hours = verified real runs × hours_per_run
realized value = realized hours × hourly_value (only when both owner values exist)
adoption gap = baseline runs_per_month − verified real runs in the reporting month
```

Unknown stays unknown. A recorded failure may yield one proposed concrete rule; it enters `rules.md` only after owner approval.
