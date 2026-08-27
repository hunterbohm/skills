# First run

The full audit. Paths are relative to the skill root.

## 1. Set the scope

Ask the owner these questions. If a source already answers one, confirm that answer with the owner:

1. What does the business do, and which team or function is in scope?
2. Which systems are authoritative for work, communication, customers, money, and files?
3. Which sources may the agent read for this audit?
4. Which categories are off-limits or must stay manual?
5. Who is the owner, who will be the approver at the gate, and who operates the workflow day to day? The owner may sponsor the workflow while another person is the operator.

Record the answers as the source map:

| source | authority | access | boundary | last_verified |
|---|---|---|---|---|
| Example: CRM | deal status | read-only | no contact export | <date> |

Done when you have written down the scope, authoritative sources, read permissions, off-limits areas, owner, approver, and operator.

## 2. Mine the real work

Use both paths when both are available.

**Connected sources.** Read the smallest useful slice: operating docs, recent project status, task trackers, existing rules and triggers in their tools, meeting decisions, and a small sample of active threads. Prefer canonical records over summaries, and current state over old promises. Look for repeated patterns of work:

- the same request arriving through several channels;
- people copying data between systems;
- approvals that stall because context is scattered;
- meetings that produce commitments but no durable follow-through;
- recurring reports assembled by hand;
- unanswered or unresolved threads;
- work that depends on one person's memory;
- errors found only after a customer notices;
- drafts or decisions rebuilt from the same source chain.

A pattern counts as a workflow only when it repeats across independent instances.

**Owner interview.** Ask in one batch:

1. What recurring chunk of work do you dread most? What triggers it, what do you do, how long does it take, and how often?
2. What else repeatedly consumes time in communication, reporting, handoffs, approvals, invoicing, follow-up, scheduling, research, or data entry?
3. Which workflow creates the most costly delay or error when it goes wrong?
4. What have you already tried to automate, and what failed?
5. What must always stay a human decision?

Keep the owner's wording. Use the interview to confirm or reject what the sources show.

Done when you have documented 4 to 8 recurring workflows, or the deliverable states that the evidence supports fewer.

## 3. Build the inventory

For each workflow record:

- name;
- evidence label;
- trigger;
- inputs and authoritative sources;
- steps and handoffs;
- output;
- operator and approver;
- frequency and duration;
- failure mode and what a failure damages;
- current proof or source reference;
- missing access or facts.

Separate the three layers the spec's pipeline formalizes:

1. **Collect.** Deterministic retrieval of the required source data.
2. **Agent joint.** The one bounded interpretation or draft the model performs.
3. **Gate and act.** The human decision, then the deterministic write that changes the outside world.

Done when every workflow has every field filled or marked unknown.

## 4. Cost what is known

Cost each workflow per the value formulas in `references/workspace-contract.md`. Show the arithmetic inline. Keep frequency conversions explicit. When the owner gives a range, show a conservative range. When an input is unknown, report hours or dollars as unknown.

Current cost and addressable load are different claims. Report the first.

Record each workflow's inputs in the ledger as its `baseline`. Resume runs and `workflow-build` compute realized value against it.

Done when every number has a source, unit, and calculation, and each costed workflow has a `baseline` in the ledger.

## 5. Choose one

Score each workflow from 1 to 5 on:

| Criterion | Question |
|---|---|
| Pain or cost | Is the documented load or consequence meaningful? |
| Repeatability | Are the trigger, inputs, and output stable? |
| Data readiness | Does the agent have read access to every required source? |
| Safety | Does the gate stop a bad draft before it does harm? |
| Proof speed | Can one fixture and one gated real run prove value? |
| Adoption | Will the actual operator use and correct it? |

Pick one workflow. Prefer the smallest workflow that exercises every pipeline stage. A candidate waits when it needs broad autonomous judgment, undefined permissions, unavailable sources, or irreversible action before review. A candidate the owner rules out becomes `rejected` in the ledger, with the reason in `notes`.

Done when the owner confirms the first workflow and the runner-up list says why each item waits.

## 6. Write the build spec

Load `references/build-spec.md` and fill every section it names. Set the first workflow's status to `designed`.

Done when another builder can implement the workflow from the spec alone. You have filled every section of `references/build-spec.md`, and the ledger shows `designed`.

## 7. Deliver into the workspace

Create or update in `<audit-root>/<business-slug>/`:

1. `workflow-audit.md`: scope and source map; workflow inventory; evidence and unknowns; cost calculations; first-workflow decision; runner-up list; one immediate owner action. Current state and historical intent are separate sections.
2. `specs/<n>-<slug>-build-spec.md`: the spec from step 6, `n` from the workflow's position in the ledger `inventory`.

End `workflow-audit.md` with what is known, what still needs confirmation, and what the owner can do next without buying or installing anything. An optional further-reading line may link the design essay at `https://github.com/hunterbohm/skills/blob/main/docs/connected-agent-field-guide.md`.

Done when `state.json` and the delivered documents show the same inventory, statuses, first workflow, and runner-up order, and `runs` holds this run with mode `first`.

## 8. Hand off

Invoke `workflow-build` on this workspace. Building is safe. Built is not live, and the spec's gate stands. If `workflow-build` is not installed, say so. Record the deferral in the ledger's `corrections`. A resume run can then tell a deferral from a forgotten handoff.

Done when the build has begun, or the deferral is in `corrections`.
