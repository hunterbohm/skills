---
name: ops-audit
disable-model-invocation: true
description: "Find the owner's time sinks and leverage points from consented evidence and past agent sessions, write the plan in chat, and do its steps under their approval. Runs only when the owner invokes it."
---

# Operations audit

Load `references/principles.md` now; every step below obeys it. The owner in the chat owns the business, the accounts, and the runtime. The owner decides; the agent does the work. Everything the owner reads arrives in chat; the workspace files are the record.

Run plain, `ops-audit`, it covers the whole operation. With words after it, as in `ops-audit email triage`, it covers that area alone: the interview asks about it, consent covers only the sources it touches, mining reads only sessions about it, and the plan holds only its steps. Record the words as `focus` in `roadmap.json`; leave it null when plain.

This skill needs a POSIX shell with Python 3. Without one, stop at step 2 and tell the owner the audit cannot mine sessions or read the plan back.

Find the slow part before you touch anything: nothing is proposed until the evidence counts it and dates it. What the owner keeps by hand is a finding of the same weight as what the agent takes over, so ask what stays hands-on before looking for what to change.

## Audit

1. **Interview.** Load `references/interview-and-consent.md`. Ask one question at a time, named time sinks first and hourly value last, offering a recommended answer when choices help. Ask where the workspace lives, offering `~/ops-audit/<business>`, read `references/workspace-contract.md`, then record every answer in `business.md` in the owner's words. Done when every interview field has an answer or a stated gap. If the owner says stop, write `state.json` with the stopping point and end.
2. **Consent.** Before consent, inspect only connection metadata and owner-declared roots. Ask for each category's consent and exclusions, one category per question; past agent sessions are a category. Record an exclusion as its declared root or account and category only. Done when every reachable category has a recorded yes, no, or exclusion. Read no source until then.
3. **Mine.** Load `references/mining.md` and follow it: inventory, consent per store, digest, then read, then the other consented sources with `sources.md` written as you go. Done when every consented store and source has a digest, evidence, or a stated limit, and every finding carries a count and a date range.
4. **Diagnose.** Load `references/causal-diagnosis.md`. For each time sink, write the card: causal path, evidence with observed, owner-reported, or inferred labels, existing coverage, gaps, intervention, proof, and verdict. Split a sink into two cards when its paths or safeguards differ. Load `references/patterns.md` only after the cards exist. Done when every named sink has a card and one card is the first move.
5. **Write the plan.** Load `references/plan-writing.md`. Write `plan` into `roadmap.json`, one step per card, in the owner's terms, and write `state.json`. For each step name the tool, connection, or machine you would use; where you have none, write an `extensions` entry naming what the owner could add and what it would unlock. Done when both files validate.
6. **Read back.** Run `scripts/workspace.py` with `plan <workspace>` and paste its output into chat. Ask one question: "Is this the order?" Change until the owner says yes. Show a step's detail with `--full` only when the owner asks. Done when the owner says the order is right. A validated file is not done.

## Feedback and approval

Feedback is words in chat. Apply the change to `roadmap.json`, raise `revision` in both files, append a `changes` entry to `state.json`, and read the plan back again. When the owner says the order is right, ask one question: "Approve this plan?" Only on that answer, record identical `owner_approval` objects in both files binding the current revision.

## Do the next step

Only after approval. The plan says which step is next; take that one. Every status change goes through `scripts/workspace.py` with `step <workspace> <card> <status> --note "..."`, which refuses to move on an unapproved plan, to skip a status, to run ahead of the main lane, or to record without the owner's words, and prints the plan afterwards. Paste that plan into chat when a step reaches Done, Running, or Hold ended. For an `approved` change, reply in one line that you are starting.

- **A move.** In one message name the step, say what you will change, where, and how you will check it, and ask for the go. Record the go as `approved` with the owner's words and the date. Do the work, touching only sources in `sources.md`. Check the result the way the step's done-when line says. Record `done` with what was done and how it was checked. Done when the plan shows Done and the owner can see the result where the done-when line says.
- **An automation.** Load `references/automation-spine.md`. From what you inspected, propose in one message the runtime, trigger, sources, the connection from the connections inventory it will use to reach each account, gate, and where failures go; the owner confirms or corrects once. A connection the inventory does not list is an `extensions` line, never an install. Record `approved`. Build it on the owner's runtime, run it once in dry-run, then once for real with the owner's go on any consequential action, and read the destination back. Record `done` with where it runs, how to run it, how to switch it off, and where failures go. Done when the plan shows Running and the owner has seen the destination you read back after the real run.
- **A hold.** Nothing to do. End it only on the owner's word, recorded as `ended`.

## Resume

Read `state.json` first. Compare newly consented sources with recorded evidence, update cards and the plan, raise the revision with a `changes` entry, and read the plan back. Do not infer work that was not done.

## References

- `references/business-profile.md`: the shape of the interview record, when writing or reading `business.md`.
- `references/roadmap-schema.json` and `references/state-schema.json`: machine contracts; `scripts/validator.py` is the executable form.
