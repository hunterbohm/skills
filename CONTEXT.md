# Operations audit and foundation

Terms shared by the `ops-audit` and `ops-foundation` skills. One business, one workspace, and one approved first automation at a time.

## People

**Owner**: The person in the chat who owns the business, accounts, and runtime.

**Approver**: The named person who clears a consequential action at its gate.

## Audit

**Audit**: The explicit, consent-based diagnosis that produces one offline `roadmap.html`.

**Roadmap**: The rendered owner-facing audit result, based on `roadmap.json`.

**Card**: One diagnosed time sink with evidence, causal path, existing coverage, intervention, proof, and verdict.

**Evidence label**: The provenance of a claim: observed, owner-reported, or inferred.

**First move**: The one roadmap action selected to reduce operational burden now.

**First automation**: The approved card that ops-foundation may build. It can be absent only with a written reason.

**Feedback**: A revision-safe accept, change, or reject request for a roadmap card.

## Workspace

**Workspace**: The durable folder selected by the owner for one business.

**State**: The machine-readable audit and foundation record in `state.json`.

**Foundation**: The installed workspace map, rules, receipts, and operating contract that support the approved automation.

**Rule**: A concrete owner-approved lesson from a recorded failure, kept in `rules.md`.

**Receipt**: The record of a fixture, real run, activation, or report, including action and read-back evidence.

## Implementation

**Runtime**: The owner-chosen system that runs the automation.

**Workflow contract**: The implementation contract for the approved card: runtime, baseline, fixture, deterministic spine, idempotency basis, failure destination, and operating instructions.

**Deterministic spine**: The fixed sequence: trigger, collect, bounded agent joint, gate, act, verify, and log.

**Agent joint**: The one bounded model judgment in the spine, with a fixed output shape.

**Gate**: The named approval point for a consequential action.

**Dry-run**: An act stage that shows its would-be write without performing it.

**Status ladder**: The ordered workflow states: candidate, designed, built, proven, live.
