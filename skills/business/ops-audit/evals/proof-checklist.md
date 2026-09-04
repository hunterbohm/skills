# Proof checklist

This skill is proven by one real run on the owner's own operations, not by a validator. Record the date and the workspace when every line holds.

## Interview and consent

- [x] The first question asked for the owner's named time sinks, not an hourly rate.
- [x] Every question waited for its answer before the next.
- [x] Every consent category was asked by name, past agent sessions included, and no source was read before its consent.
- [x] Exclusions were recorded as category and declared root only.

## Mining

- [x] `harnesses.py inventory` ran on every machine the owner named, and consent was asked per store.
- [x] `connections.py inventory` ran on the same machines, and every source's "Read by" line names a connection from it.
- [x] Every consented store was digested with `digest.py` before any session was read, and every finding carries a count and a date range.
- [x] At least one card came from hand work, repeats, or corrections seen in sessions.
- [x] `sources.md` lists every consented source with all five lines.
- [x] Existing scripts, jobs, runs, outputs, and failures were inspected before any automation was proposed.
- [ ] Nothing left a source unredacted. (2026-09-03: two digests leaked an API key and bank numbers before the redactor was widened; fixed and regenerated, but the line stays open until a run leaks nothing first time.)

## Plan

- [x] The owner read the plan in chat as printed by `workspace.py plan` and said the order was right.
- [x] The owner said without help what happens first and what they must approve. No file was opened.
- [x] No step field contains a word from the plan-writing banned list.
- [x] Unknown costs stayed unknown and appeared nowhere in the plan text.
- [ ] Every agent step named the tool or connection it would use, and every gap became an "If you add" line rather than a job for the owner.
- [ ] A focused run, such as `ops-audit email triage`, stayed inside its focus in interview, consent, mining, and plan.

## Feedback and approval

- [x] The owner asked for at least one change in chat, and the plan changed, the revision moved in both files, and `state.changes` gained one entry.
- [x] The approval record in both files binds the revision the owner read.

## Doing steps

- [x] The agent said what it would change and how it would check before asking for the go.
- [x] The owner's go was recorded as `approved` with their words before anything changed.
- [x] The move touched only sources named in `sources.md`, and `done` records how the result was checked; the plan printed Done afterwards.
- [x] The owner found the result where the done-when line said, without asking.
- [ ] For the automation, the runtime, trigger, sources, the connection for each account, gate, and failure destination were proposed from inspection in one message and confirmed once; it ran in dry-run before the real run; the plan printed Running.

Last proven: 2026-09-03, the author's own operations across two machines, 349 digests from 14 stores; open lines are the automation step, the focused run, the tool named per step, and first-time redaction.
