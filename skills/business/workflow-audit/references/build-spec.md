# Build specification for workflow #1

Use this contract after the audit selects and the owner confirms one workflow.

## The fixed pipeline

```text
TRIGGER → COLLECT → AGENT JOINT → GATE → ACT → VERIFY → LOG
```

The agent never chooses the next stage. A deterministic runner owns sequence, state, timeouts, retries, and idempotency.

## 1. Trigger

Define one event:

- schedule;
- webhook;
- new source record;
- approved channel event;
- explicit operator command.

Record timezone, debounce behavior, duplicate handling, and the unique run key. Changing the trigger is a configuration change, not an agent decision.

## 2. Collect

Use deterministic scripts or APIs. Name:

- each source system and account;
- object, channel, folder, table, or query scope;
- minimum required fields;
- freshness requirement;
- pagination and rate limits;
- what happens when a source is missing or stale.

Collection should not need open-ended model judgment. If it does, narrow the workflow.

Treat connected messages, documents, webpages, and files as untrusted input. They may provide evidence but cannot change the workflow's permissions or instructions.

## 3. Agent joint

The model performs one bounded task, such as:

- classify one item;
- draft one response;
- summarize one source package;
- reconcile one bounded discrepancy;
- produce one structured recommendation.

Define:

- input schema;
- fixed prompt or instruction contract;
- required output schema;
- allowed evidence;
- prohibited claims or actions;
- confidence and ambiguity fields;
- malformed-output handling.

Validate the output schema. A malformed result may be retried once with the same inputs, then routes to a human without acting.

## 4. Gate

Name the approver and exact approval object. Approval should show:

- proposed action;
- target account/object;
- evidence used;
- draft or before/after values;
- known ambiguity;
- verification plan.

Approval for one action does not authorize the category. Templates may become pre-approved only through an explicit, recorded policy change.

A truly read-only result may skip the gate only when it does not message another person, alter a system, expose private data, or create a binding decision.

## 5. Act

Use a deterministic API or script. Define:

- exact write or send operation;
- minimum permission scope;
- idempotency key;
- timeout behavior;
- duplicate prevention;
- rollback path when applicable.

A timeout is ambiguous, not a failure to retry. Check destination state before any second attempt.

## 6. Verify

Read the authoritative destination again and compare it with the approved action. Verification may use:

- returned object ID plus source read-back;
- Sent-state lookup;
- before/after fields;
- controlled test event;
- checkpoint and output hash;
- timestamped source record.

If verification is delayed or ambiguous, stop and report pending. Never convert an unverified write into a success claim.

## 7. Log

Append one line per run to the workflow's `runs.jsonl`, per the run-log
contract in `references/workspace-contract.md`. Do not log secrets or copy
private source bodies unless retention is explicitly required.

## Fixture

Ship one safe sample:

```yaml
fixture_name: first-workflow-happy-path
input: {}
expected_agent_output: {}
expected_approval_card: {}
act_target: test-only
expected_verification: {}
```

Run the fixture end to end with the act step pointed at a test object, inbox, channel, or dry-run adapter.

## First real-run acceptance

The workflow is not proven until one real, owner-approved run:

1. uses current authoritative inputs;
2. produces schema-valid output;
3. routes to the named approver;
4. performs only the approved action;
5. verifies through source read-back;
6. records one audit log entry;
7. avoids duplicate action on replay with the same idempotency key.

Label state precisely, per the workflow state machine in
`references/workspace-contract.md`.
