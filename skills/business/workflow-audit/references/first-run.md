# First run — the full audit

Execute these steps in order. Paths to other references are relative to the
skill root.

## 1. Establish the audit scope

Ask for or infer the minimum frame, then confirm it:

1. What does the business do, and which team or function is in scope?
2. Which systems are authoritative for work, communication, customers, money, and files?
3. Which sources may the agent read for this audit?
4. Which categories are off-limits or should never be automated?
5. Who will approve the final workflow choice?

Create a short source map:

| source | authority | access | boundary | last_verified |
|---|---|---|---|---|
| Example: CRM | pipeline stage | read-only | no contact export | today |

Completion criterion: the scope, authoritative sources, read permissions, prohibited areas, and approver are explicit.

## 2. Mine the real work

Use both paths when available:

### Connected-source path

Read the smallest useful slice of current sources: operating docs, recent project status, task trackers, workflow definitions, meeting decisions, and a limited sample of active work threads. Prefer canonical records over summaries and current state over historical promises.

Look for repeated shapes:

- the same request arriving through multiple channels;
- people copying data between systems;
- approvals that stall because context is scattered;
- meetings that produce commitments but no durable follow-through;
- recurring reports assembled by hand;
- unanswered or unresolved threads;
- work that depends on one person's memory;
- errors discovered only after a customer notices;
- drafts or decisions repeatedly rebuilt from the same source chain.

A shape counts as a workflow only when it repeats across independent instances.

### Owner-interview path

Ask in one compact batch:

1. What recurring chunk of work do you dread most? What triggers it, what do you do, how long does it take, and how often?
2. What else repeatedly consumes time in communication, reporting, handoffs, approvals, invoicing, follow-up, scheduling, research, or data entry?
3. Which workflow creates the most costly delay or error when it goes wrong?
4. What have you already tried to automate, and what failed?
5. What must always remain a human decision?

Keep the owner's wording. Use the interview to confirm or reject connected-source findings.

Completion criterion: 4–8 recurring workflows are documented, or the deliverable explicitly says the available evidence supports fewer. Do not pad the map.

## 3. Build the workflow inventory

For each workflow record:

- name;
- evidence: `observed`, `owner-reported`, or `inferred`;
- trigger;
- inputs and authoritative sources;
- steps and handoffs;
- output;
- operator and approver;
- frequency and duration;
- failure mode and blast radius;
- current proof or source reference;
- missing access or facts.

Separate three layers that are often confused:

1. **Collection:** deterministic retrieval of the required source data.
2. **Judgment:** the one bounded interpretation or draft an agent can perform.
3. **Authority:** the human decision or deterministic write that changes the outside world.

Completion criterion: every workflow has a clear trigger and output, and unknowns are visible instead of silently filled.

## 4. Quantify only what is known

For each workflow:

```text
hours/month = runs/month × hours/run
annual labor value = hours/month × 12 × stated hourly value
```

Show the arithmetic inline. Keep frequency conversions explicit. When the owner gives a range, show a conservative range rather than selecting the larger number. If an input is unknown, report hours or dollars as unknown.

Do not present theoretical automation savings as expected results. Current cost and potential addressable load are different claims.

Record each workflow's inputs in the ledger as its `baseline` — resume runs and the workflow-build skill compute realized value against it.

Completion criterion: every number has a source, unit, and calculation; each quantified workflow's `baseline` is in the ledger; all unsupported savings claims are absent.

## 5. Choose one first workflow

Score each workflow from 1–5 on:

| Criterion | Question |
|---|---|
| Pain/cost | Is the documented load or consequence meaningful? |
| Repeatability | Are the trigger, inputs, and output stable? |
| Data readiness | Can the required sources be read reliably? |
| Safety | Can a bad draft be caught before harm occurs? |
| Proof speed | Can one fixture and one real gated run prove value quickly? |
| Adoption | Will the actual operator use and correct it? |

Pick one workflow, not a platform rebuild. Prefer the smallest workflow that proves the operating model. Reject candidates that require broad autonomous judgment, undefined permissions, unavailable sources, or irreversible action before review. Candidates the owner rules out become `rejected` in the ledger, with the reason in `notes`.

Completion criterion: the first workflow is confirmed by the owner and the runner-up list explains why each item waits.

## 6. Produce the build spec

Load `references/build-spec.md` and define every stage of the pipeline it
specifies.

Ship one fixture with sample input and expected output, plus one real acceptance test. No production activation occurs during the audit.

Completion criterion: another competent builder can implement the first workflow without guessing its trigger, source scopes, output schema, approval rule, idempotency key, verification method, or proof gate.

## 7. Deliver into the workspace

Create or update in `<audit-root>/<business-slug>/`:

1. `workflow-audit.md`
   - scope and source map;
   - workflow inventory;
   - evidence and unknowns;
   - cost calculations;
   - first-workflow decision;
   - next-in-line list;
   - one immediate owner action.
2. `specs/<n>-<slug>-build-spec.md` — the spec produced in step 6, `n` from the workflow's ledger order.
3. `owner-summary.md` — regenerate per `references/owner-summary.md`.

End with what is known, what still needs confirmation, and what the owner can do next without buying or installing anything.

Completion criterion: `state.json` matches the delivered documents — same
inventory, statuses, first workflow, and runner-up order — and the run is
appended to `runs`.

## 8. Hand off to the build

With the first workflow confirmed and its spec delivered, invoke the
workflow-build skill on this workspace. Building is safe — built is not live,
and the spec's gate still stands — so do not wait to be asked.

Completion criterion: the build has begun, or the owner's deferral is
recorded in the ledger's `corrections` so resume runs can tell it from a
forgotten handoff.

## Common pitfalls

1. **Auditing tools instead of work.** Start with repeated outcomes and handoffs, then map tools.
2. **Calling a mapped idea live.** Distinguish designed, built, proven, and enabled.
3. **Using summaries as authority.** Verify current source state before making a current claim.
4. **Automating before access is ready.** Data readiness is part of prioritization.
5. **Skipping the operator.** A founder may sponsor the system while another person is the real user.
