---
name: ops-foundation
description: "Installs and operates an approved ops-audit roadmap handoff, or an already-installed ops-foundation workspace, on the owner's runtime."
---

# Operations foundation

The owner runs this on their own accounts and runtime. Read `references/principles.md` and `references/workspace-contract.md`. Read the approved `roadmap.json` and `state.json`; apply pending audit feedback first. Take one branch per run: Install, Build, Prove, Go live, or Report. `roadmap.html` remains the only owner-facing audit result.

## Gates

- Take only `roadmap.first_automation`; do not substitute a card or build from chat.
- Before an implementation write, load `references/runtime-questionnaire.md` and ask its questions **one at a time**, waiting after each answer. Never infer a runtime choice.
- Use the fixed spine: trigger → deterministic collect → one bounded agent joint → named gate for consequential action → deterministic act → destination read-back verify → receipt/log. The agent cannot control sequence.
- Retry malformed joint output once. Then flag a visible failure and do not act. Read an ambiguous destination write back before any retry. No silent failure; stop once failure is visible.
- No implementation code or plays ship here. Build against the runtime the owner chose during use.

## Install

Confirm a complete, owner-approved roadmap whose approval record binds its current ID and revision, with matching `state.json` and no pending feedback. Run `scripts/foundation.py` with `init <workspace>` to create missing `README.md`, `rules.md`, receipts, and foundation state without replacing owner content. Workspace scripts require POSIX Python 3. Tell the owner to add this exact line to their agent configuration (with their chosen workspace):

```text
Read <workspace>/README.md before working in this operations workspace.
```

Do not edit that configuration. Confirm the owner added it or perform a permitted configuration read-back before declaring Install complete. If `first_automation` is null, record its roadmap reason and stop: Install is complete; Build cannot start. Otherwise completion is foundation `installed`, map and rules exist, and the configuration is confirmed.

## Build

Use only the approved card. Ask the runtime questions before any implementation write, then load `references/workflow-contract.md`. Write `workflows/<card-id>/contract.json` from the card, `business.md`, evidence, principles, and answers. Include implementation location plus run, switch, and stop/read-back instructions, and the runtime record source. Run the `scripts/foundation.py` `validate-contract` command with the contract and workspace before implementation. Implement it on the chosen runtime. Run its fixture end to end with Act in dry-run; append its receipt. Set `built` only after that proof. Completion: passing dry-run receipt and `built`.

## Prove

Load `references/receipt-and-status.md`. Run once now. Obtain the named approver's clearance where the contract requires it; perform only its approved action, read the destination back, append a real receipt, and record `replay_verified: true` after confirming replay does not duplicate the idempotency key. Set `proven` only on that evidence. Completion: one verified, nonduplicate real receipt and `proven`.

## Go live

Require `proven`. Ask for explicit owner approval of the exact production trigger if it is not already explicit. Record `explicit_instruction: true` and the instruction before activation. Activate only that trigger, read its state back, append an activation receipt, then set `live`. Completion: recorded instruction, verified active trigger, and `live`.

## Report

Load `references/reporting.md`. Use the report command with workspace, card ID, and reporting month; it imports the configured external record source when needed. Use verified real receipts only. Calculate realized hours/value against the owner baseline and adoption gap. Show failures. For each recorded failure, propose at most one concrete rule; change `rules.md` only after owner approval. Lower status when failure invalidates its proof. Completion: every claim traces to a receipt, baseline, or approved rule.
