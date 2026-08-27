# Runtime rules

The implementation must satisfy every rule here, on any runtime. The spec defines the workflow. These rules bound what the runtime may do.

## Pipeline

`trigger → collect → agent joint → gate → act → verify → log`. The runtime owns sequence, state, timeouts, the one-retry rule, and idempotency, as the spec defines them. The model runs only inside the agent joint.

## Stages

- Collect and act are scripts or API calls. A stage that needs open judgment means the workflow is too wide. Go back to the spec.
- The joint prompt is fixed text stored with the implementation: input schema, task, output schema, allowed evidence, prohibited claims, ambiguity fields. The runtime sends it verbatim. Editing it is a spec change.
- The runtime validates the joint's output schema. On malformed output it retries once with the same inputs. If the output is still malformed, it routes the run to the approver per the spec.
- The gate stops the run and presents the spec's approval object. In fixture mode it writes `fixture-approved` into the run log's `approver` field, so the pipeline is testable end to end.
- Dry-run or live is configuration the runtime reads, never model output. Dry-run prints the exact would-be write.
- Verify reads the destination back. In dry-run it compares the printed action with the fixture's expected output.

## Records

`workflows/<n>-<slug>/runs.jsonl` in the workspace is the record of truth, one line per run per `references/workspace-contract.md`.

## Example: a scheduled routine

Spec: every weekday at 08:00, list customer threads with no reply in 3 days. Draft one follow-up each. Route to the account manager. Send on approval.

- Trigger and collect: the owner's scheduler runs a script that queries the inbox API for the thread list. No model.
- Agent joint: one call per thread with the fixed joint prompt. Output schema: `{thread_id, draft, confidence, ambiguity}`.
- Gate: the drafts land in the account manager's approval channel. The run stops there.
- Act: on approval, the script sends that one draft with idempotency key `<thread_id>:<run_id>`. `DRY_RUN=1` prints the send instead.
- Verify: the script reads the thread back and checks the sent message is present.
- Log: one line to `runs.jsonl`, `verified: true`, or `"pending"` if the read-back is delayed.
