# Advisory Ledger — Memory Across Sessions

Load this file when an **Advise** or **Audit** request concerns a real, named business. The ledger preserves business context so the owner does not have to explain the same background each session. Prior advice and results inform a new answer when relevant.

`scripts/ledger.py` owns the state. Call it rather than reading or writing `advisory.json` by hand — it enforces the schema, writes atomically, and refuses the moves that would silently fork a business's history.

## Where state lives

One ledger per business at `<advisory-root>/<business-slug>/advisory.json`. The root is resolved from `$ASK_HORMOZI_ADVISORY_ROOT`, then from the recorded root in `~/.config/ask-hormozi/config.json`, so it survives across sessions and runtimes.

```bash
python3 scripts/ledger.py root                    # where ledgers live
python3 scripts/ledger.py root --set <path>       # record it (once per machine)
python3 scripts/ledger.py list                    # businesses with a ledger
```

`root` exits 3 when nothing is recorded, or when the recorded folder is gone (moved folder, different machine). Both mean the same thing: ask the owner where the ledger lives and re-record it. Never start a fresh ledger to route around a missing root — the old history is the asset.

## Read rule — before diagnosing

```bash
python3 scripts/ledger.py open <business-slug>
```

Exit 4 means no ledger yet: offer to start one with `init <slug> --business "Name"`. If the owner declines, proceed without it and do not ask again in the session.

When a ledger opens:

1. **Check relevance before following up.** Review `_open_prescriptions` against the current question. Ask what happened only when the result could change the current diagnosis or recommendation, or the owner asks to revisit it. Leave unrelated prescriptions unchanged and continue with the new question; do not demand a progress report. When a relevant outcome is supplied, record it:
   ```bash
   python3 scripts/ledger.py resolve <slug> --index N --status done|tried|dropped --result "what happened, in numbers"
   ```
2. **Reuse the saved business context.** `model` holds what is already known. Ask only for missing or materially changed facts that could change the answer, not a repeat of the business background.
3. **Surface drift.** When stated numbers differ materially from `model`, say so and use the newer ones.
4. **Treat a repeated constraint as evidence.** If the same constraint recurs with prescriptions tried, question the playbook fit or the diagnosis, not the owner's effort.

## Write rule — after delivering

One call records the run:

```bash
python3 scripts/ledger.py append <slug> \
  --branch advise --summary "one line" \
  --constraint leads --evidence "what showed it" \
  --action "the one highest-leverage action" --framework "framework applied" \
  --model cac=400 --model gp_first_30d=1600
```

`append` requires an explicit choice while a prior prescription is still `open`: resolve it only when the owner supplies an outcome. Pass `--allow-unresolved` when outstanding advice is unrelated to the current question, or when a relevant result is unavailable. This preserves the old prescription unchanged while recording the new run. Never mark advice done, tried, or dropped merely to unblock a new answer. When a relevant result is unavailable, state the uncertainty and give conditional advice or ask for the necessary fact. Add `--correction "rule"` when the owner corrects a prior diagnosis or a framework misfire.

Keep `--result` observational: what happened, in numbers where possible, not a grade.

## Completion check

A ledgered run is complete when saved business context informs the answer, relevant supplied outcomes are recorded, unrelated or unknown outcomes remain unchanged, the new run is recorded, and `validate <slug>` passes.
