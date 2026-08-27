# A practical operating guide for a connected agency agent

This is not a product pitch or a promise that an agent can run an agency by itself. It is the operating model I would use if Claude or another capable agent already had access to the systems where an agency works.

(This guide is a standalone read for a business owner. Where its wording differs from the `workflow-audit` and `workflow-build` skills under `../skills/business/`, the skills are canonical.)

The goal is simple: reduce the amount of context gathering, coordination, and follow-up that still depends on the founder, while keeping judgment and outbound communication with the people responsible for the client relationship.

## The operating principle

Do not begin with “what can the model automate?” Begin with:

> What recurring piece of work forces someone to gather the same context, make the same bounded decision, or chase the same open loop every week?

Then build one supervised workflow around that job.

A connected agent is most useful as an operating layer across the systems the agency already uses. It should retrieve the smallest useful slice of evidence, prepare a clear work package, ask for approval when an action has consequences, verify the result, and preserve what happened for the next run.

It should not behave like a general-purpose employee with unrestricted authority.

## What actually creates leverage

### 1. A source map before prompts

List the authoritative source for each kind of truth:

- client scope and commitments;
- project status and ownership;
- conversations and unresolved requests;
- meetings, decisions, and action items;
- campaign or delivery data;
- files, creative, and approvals;
- billing and other sensitive systems.

For every source, record:

- what it owns;
- who is allowed to read it;
- who can approve a write;
- how current the data is;
- how a successful write is verified.

Without this map, a stronger model produces more convincing guesses. With it, even a narrow workflow can be dependable.

### 2. An attention queue, not another dashboard

The founder should not have to read every channel and report. A useful agent can periodically identify:

- client questions that still need an answer;
- team requests without an owner;
- promised follow-ups that have gone quiet;
- approvals blocking delivery;
- deadlines whose underlying work is not ready;
- recurring questions that should become reusable context.

The output should be short: what needs attention, why, the evidence, and the next decision. A long summary that makes the founder reread the source is not leverage.

Keep one living status surface where possible. Do not create a second task system that immediately drifts from the first.

### 3. Investigation before drafting

Most agency work is not “write a reply.” The real work is often figuring out what happened.

A safe investigation workflow looks like this:

1. identify the exact request and client scope;
2. retrieve only the relevant messages, records, files, and history;
3. distinguish evidence from inference;
4. state the likely cause and confidence;
5. identify missing information;
6. propose the smallest useful action;
7. draft the update only after the investigation is clear.

This is especially useful when a problem spans several connected tools. The agent should inspect the chain rather than assume the first system contains the answer.

### 4. Separate client voice from team voice

A founder or account manager does not speak to clients the same way they speak internally.

Maintain separate, reviewed examples for:

- client communication;
- internal team communication;
- technical incident updates;
- approvals and escalation.

Use those examples as style evidence, not as permission to invent facts or commitments. Drafts remain approval-gated until the owner explicitly pre-approves a narrow, repeatable message class.

### 5. Meetings should close loops

A meeting pipeline is valuable when it turns a transcript into operational state, not when it produces another summary nobody opens.

For each meeting, extract:

- decisions;
- commitments;
- owner;
- due date;
- unresolved questions;
- client or project scope;
- link back to the original recording or transcript.

Then reconcile those items against the canonical project surface. Do not create duplicate tasks if the commitment already exists.

### 6. Reliability is part of the product

Scheduled workflows fail in ordinary ways: credentials expire, a source changes shape, the same event appears twice, a send times out, a checkpoint is lost, or an agent returns malformed output.

Every workflow needs:

- a checkpoint or cursor;
- deduplication;
- an idempotency key for consequential actions;
- one bounded retry for malformed agent output;
- no blind retry after an ambiguous send;
- source read-back after a write;
- a business-readable error message;
- technical diagnostics routed away from the owner-facing channel;
- a rollback path for configuration changes.

“Self-healing” should mean repairing known, safe failure modes. It should not mean granting the agent permission to improvise around access or approval boundaries.

### 7. The operator teaches the system through corrections

The fastest path to a useful setup is one real operator using one real workflow.

Every correction should improve one of four things:

- the source map;
- the decision rule;
- the output format;
- the voice examples.

Capture the reusable preference, not the emotional residue of a bad run. Expand only after the same workflow has passed an end-to-end acceptance test.

## The architecture I would use

```text
TRIGGER
  → COLLECT
  → AGENT JOINT
  → GATE
  → ACT
  → VERIFY
  → LOG
```

### Trigger

A deterministic event: a new transcript, an inbound request, a scheduled sweep, a stage change, or an approved manual command.

### Collect

A script or API retrieves the minimum evidence needed. It does not ask the model to search broadly and decide what matters without boundaries.

### Agent joint

The model performs one bounded judgment: classify, summarize, reconcile, diagnose, or draft. Its output shape is fixed.

### Gate

A named person reviews the proposed consequential action. Read-only analysis can be delivered automatically when the team has explicitly approved the destination and scope.

### Act

A deterministic tool performs the approved send or write exactly once.

### Verify

Read the source system again. If the result is ambiguous, stop and report uncertainty. Do not retry blindly.

### Log

Record the trigger, source references, decision, approval, action result, and verification evidence without copying secrets or unnecessary private data.

## What I would build first

Choose one workflow that is frequent, expensive in attention, repeatable, safe, and supported by accessible data.

For many agencies, the best first candidates are:

1. unresolved-thread and attention triage;
2. meeting-to-action reconciliation;
3. approval-ready client update drafts;
4. recurring delivery or campaign exception monitoring;
5. weekly client reporting assembled from authoritative sources.

Do not start with autonomous client communication. Start with read, investigate, organize, and draft.

## A self-serve implementation sequence

### Step 1: inventory the recurring work

Map four to eight workflows. Capture the trigger, current steps, operator, frequency, duration, systems, output, approval point, and common failure modes.

### Step 2: choose one acceptance test

Define one real input and the exact output that would count as useful. Name the source scope and approver. Keep every external action disabled.

### Step 3: run read-only

Prove the collector can retrieve the right evidence without broad access. Confirm that missing or stale sources are visible rather than guessed around.

### Step 4: produce a work package

Require the agent to return:

- issue or objective;
- evidence with source links;
- diagnosis or recommendation;
- confidence and ambiguity;
- proposed action;
- required approval;
- verification method;
- optional draft.

### Step 5: gate one real run

Have the operator approve one bounded action. Execute it once, read it back, and compare the result with the expected outcome.

### Step 6: harden before scheduling

Add checkpoints, deduplication, idempotency, error routing, and a test fixture. Only then consider a schedule or event trigger.

### Step 7: expand by evidence

Add another workflow or permission class only after the first one repeatedly produces useful, verified results.

## A good first request to Claude

If Claude already has access to the agency’s workspace, install the Workflow Audit skill and say:

> Audit how this agency currently works using read-only access. Map the recurring workflows you can support with evidence, show me what is observed versus inferred, identify missing sources, and recommend one workflow to implement first. Do not send, write, change permissions, or create a second task system. Produce the audit and a self-serve build spec for the first workflow.

Review the source map and workflow choice before letting it build anything.

## The standard to hold it to

A useful connected agent should make the agency easier to operate even if the person who configured it disappears for a week.

That means the owner can see:

- where truth lives;
- what each workflow does;
- what it is allowed to touch;
- what still requires approval;
- how to test it;
- how to know it succeeded;
- how to stop or repair it.

If the setup only works because one technical person remembers how all the pieces fit together, it is not finished.