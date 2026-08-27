# Advisory Ledger — Memory Across Sessions

Load this file when an **Advise** or **Audit** request concerns a real, named business. The ledger turns one-shot advice into a compounding loop: diagnose → prescribe → act → stare at the result → rediagnose.

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

1. **Review `_open_prescriptions` first.** For each, ask what happened and record it before new diagnosis. A prescription that was never tried is a finding — name the blocker before issuing new advice.
   ```bash
   python3 scripts/ledger.py resolve <slug> --index N --status done|tried|dropped --result "what happened, in numbers"
   ```
2. **Ask only for facts the ledger lacks.** `model` holds what is already known; ask for the rest.
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

`append` refuses while a prior prescription is still `open` — resolve it first, or pass `--allow-unresolved` when the owner genuinely could not say. Add `--correction "rule"` when the owner corrects a prior diagnosis or a framework misfire.

Keep `--result` observational: what happened, in numbers where possible, not a grade.

## Completion check

A ledgered run is complete when every previously open prescription has a recorded status and result, the new prescription is recorded, and `validate <slug>` passes.
