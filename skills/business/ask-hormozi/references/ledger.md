# Advisory Ledger — Memory Across Sessions

Load this file when an **Advise** or **Audit** request concerns a named business, including a fictional demo with user- or workspace-authorized persistent memory. The ledger preserves business context so the owner does not have to explain the same background each session. Prior advice and results inform a new answer when relevant.

`scripts/ledger.py` owns the state. Call it rather than reading or writing `advisory.json` by hand — it enforces the schema, writes atomically, and refuses the moves that would silently fork a business's history.

## Where state lives

One ledger per business at `<advisory-root>/<business-slug>/advisory.json`. When the user or workspace explicitly specifies a memory folder, set `ASK_HORMOZI_ADVISORY_ROOT` to its absolute path on every helper call; do not fall back to a different global ledger. A workspace using Claude Code should expose these instructions through `CLAUDE.md` (and may set the environment variable in project settings); `AGENTS.md` alone is not its startup instruction file. Use the helper and references from the skill package actually loaded; keep installed copies current.

The root is resolved from `$ASK_HORMOZI_ADVISORY_ROOT`, then from the recorded root in `~/.config/ask-hormozi/config.json`, so it survives across sessions and runtimes.

```bash
python3 scripts/ledger.py root                    # where ledgers live
python3 scripts/ledger.py root --set <path>       # record it (once per machine)
python3 scripts/ledger.py list                    # businesses with a ledger
```

`root` exits 3 when nothing is recorded, or when the recorded folder is gone (moved folder, different machine). Both mean the same thing: ask the owner where the ledger lives and re-record it. Never start a fresh ledger to route around a missing root — the old history is the asset.

## Updates preserve external state

Choose a durable data folder outside the skill installation and its skills collection, such as `~/business-memory/ask-hormozi`. Keep the config outside the installation too. Updating or replacing the skill package then leaves those files in place; the new helper reopens the recorded folder. Do not use a temporary folder for real business memory.

The helper rejects state or config paths inside a skill package or its installed skills collection, including paths redirected there through symlinks. It never deletes or migrates existing history. If older state is inside an installation, stop before updating: copy the complete business-memory folder to an external location, verify the copy, record the new root (with `--force` only for a confirmed move), and validate/open the businesses there. Move an unsafe config outside the installation as well. Only then update the skill. A missing or incompatible ledger must not be replaced with an empty one.

## Read rule — before diagnosing

```bash
python3 scripts/ledger.py open <business-slug>
```

Exit 4 means no ledger yet. If the user or workspace has already authorized memory here, run `init <slug> --business "Name"` immediately; otherwise offer to start one. A fictional label is not a reason to skip authorized memory. If the owner declines, proceed without it and do not ask again in the session.

When a ledger opens:

1. **Check relevance before following up.** Review `_open_prescriptions` against the current question. Ask what happened only when the result could change the current diagnosis or recommendation, or the owner asks to revisit it. Leave unrelated prescriptions unchanged and continue with the new question; do not demand a progress report. When a relevant outcome is supplied, record it:
   ```bash
   python3 scripts/ledger.py resolve <slug> --index N --status done|tried|dropped --result "what happened, in numbers"
   ```
2. **Reuse the saved business context.** `model` holds what is already known. Read relevant business documents the owner identifies before asking for missing or materially changed facts. Follow the short intake in `SKILL.md`; do not repeat the business background or require every model field to be filled.
3. **Surface drift.** When stated numbers differ materially from `model`, say so and use the newer ones.
4. **Treat a repeated constraint as evidence.** If the same constraint recurs with prescriptions tried, question the playbook fit or the diagnosis, not the owner's effort.

## Write rule — before the final reply

Once the recommendation is ready, save it before sending the final reply. One call records the run. Use `--model key=value` for useful business facts supported by the owner or identified documents, including newly learned offer or delivery context. Preserve other saved facts; resolve material conflicts before replacing them. Do not store whole documents or unconfirmed assumptions as business facts:

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

A ledgered run is complete when saved business context informs the answer, relevant supplied outcomes are recorded, unrelated or unknown outcomes remain unchanged, the new run is recorded, and `validate <slug>` passes. Then `open <slug>` again and check that the new run and supported facts appear. If saving or readback fails, say that this session was not saved and identify the failure; do not claim that the next session will remember it.
