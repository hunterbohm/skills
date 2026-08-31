# ops-audit and ops-foundation

Design agreed with Hunter on 2026-08-30. This is the spec for the rewrite of `workflow-audit` and `workflow-build`. ADR 0001 and 0002 stand. ADR 0003, 0004, and 0005 record the decisions below.

## Why the rethink

The first real runs (2026-08-27 to 28) showed the old shape did not hold. The audit produced long inventories nobody acted on. The one build was a duplicate of an automation the owner already ran, because existing automations were not a source. Costing waited on one number. A second session wrote into a workspace mid-run. The full list is in the parked branch `first-run-fixes` and the findings file it came from. Four lessons carry forward: existing automations are a source, one question at a time with tappable options, hourly value first, read the ledger before every write.

## The user

The owner of the business, in the chat, on their own accounts and runtime. No consultant mode. Personal operations join only when the owner adds them as a source category.

## ops-audit

Steps, in order.

1. Interview. Grill rounds. Use the agent's tappable question tool when it has one, with the recommended answer first. Without one, number the questions in prose and give the recommended answer under each. Ask hourly value first. Write `business.md` as answers land: the owner's terms, people and roles, tools, rhythms (daily, weekly, monthly), never-automate list, hourly value. Stop when those sections are filled and the top time sinks are named, or when the owner says stop.
2. Consent. List the source categories the agent can reach in this session: mail, calendar, chat, documents, scripts and scheduled jobs, past agent transcripts, and personal operations if the owner wants them. Past agent transcripts default on; they show what the owner already delegates. The owner ticks categories, then names anything off limits. Excluded material appears afterwards as path and category only.
3. Mining. Read only. Scripts and scheduled jobs are the "what already runs" source; every card must say whether something already covers it.
4. Roadmap data. Write `roadmap.json`. Cards per time sink. Each card: name, hours per month and dollars per year from the owner's numbers (unknown stays unknown), evidence with labels (observed, owner-reported, inferred), what already runs, verdict (keep human, leverage move, automate with an agent), group (Now, Next, Later), matched pattern if any. Two marks across all cards: first move and first automation. They may be the same card.
5. Render. `scripts/render.py roadmap.json > roadmap.html`. Python 3, standard library only. The template is designed once and ships with the skill. One file, no network requests, opens from disk.
6. Feedback. In the page: accept, change, reject on each card, a note box, notes kept in browser storage, and one "Copy for agent" button. The block it copies is markdown with a two-line header ("Feedback on roadmap <business> <date>. Update the ledger, then re-render.") and one line per touched card with its id, the choice, and the note. The owner pastes it into any agent. The agent parses it, writes the ledger, re-renders. Discord users can paste the block or attach it as a text file.
7. Resume. Parse any feedback first, then diff sources against the ledger, then re-render.

Workspace, one folder per business, owner picks the path on first run:

```
business.md      interview output
roadmap.json     agent-written data
roadmap.html     rendered, the only thing the owner reads
state.json       ledger
README.md        the map file, written by ops-foundation
rules.md         grows one rule per recorded mistake, written by ops-foundation
runs.jsonl       one line per real run
workflows/<id>/  spec, implementation, fixtures
```

## ops-foundation

Branches: Install, Build, Prove, Go live, Report.

Install writes the map file and `rules.md` into the workspace, sets up gates and receipts, and tells the owner which line to add to their agent configuration so the agent reads the map first. Foundation status becomes installed. Then Build takes the first automation card, writes its spec from the card and `business.md`, and implements it on the owner's runtime under the runtime rules. No shipped plays, no shipped code. Before Build writes anything it asks the owner where the automation runs: which machine, which scheduler, which agent runs the joint, where secrets live, where output goes. It never picks a runtime from what it can see on the machine. Reliable means the run cannot fail quietly: one retry, then a visible flag, and the verify step reads the destination back. It does not mean building for scale, failover, or failure modes the owner has not met. Make it run, make it unable to fail silently, then stop. Prove, Go live, and Report keep their current meaning. Report also proposes one new rule after each recorded failure; the owner approves before it enters `rules.md`. A card whose verdict is leverage move is the owner's to carry out; the roadmap says how, the skill does not do it.

## Shared material

- `workspace-contract.md` and the owner-facing summary stay vendored byte-identical in both packages (ADR 0001).
- `references/principles.md`: Hunter's philosophy in his own lines, each traceable to its source. Claude drafts from the collected quotes, Hunter edits, nothing publishes before he reads it.
- `references/patterns.md` in `ops-audit`: sixteen agency patterns, anonymized, no agency names.
- The private ProfitPilot audit variant folds its usable parts (the "real advice" section, honest time cost, principles) into these skills and is then retired. Its pitch section does not come along; this is a self-serve skill and does not sell anything. The private plays spec stays where it is.

## Assumptions Hunter accepted

1. Workflow ladder unchanged: candidate, designed, built, proven, live. Foundation is absent or installed.
2. Hourly value asked first; owner's numbers only; unknown stays unknown.
3. Never-touch material appears as path and category only.
4. `rules.md` grows one rule per recorded mistake, proposed by Report, approved by the owner.
5. Interview falls back to numbered prose with a recommended answer when the agent has no tappable-question tool.
6. `roadmap.html` is one file, no external requests, works offline. The render script is Python 3 standard library.
7. ADR 0003, 0004, 0005 added. ADR 0001 and 0002 stand.
8. Owner workspace files never enter the public repository.

## Glossary changes for CONTEXT.md

New terms: roadmap, card, verdict, first move, first automation, feedback block, business model doc, foundation, map file, rules file. "Audit" no longer avoids "roadmap"; the roadmap is its output. "Play" stays avoided. Old terms that go: owner summary and build spec as a standalone document. First run versus resume run stay.

## Open for the rewrite

- Exact `roadmap.json` schema and the feedback block grammar.
- Where each agent keeps past transcripts, so the consent step can name real paths.
- How old skill names redirect to the new ones in the catalog and the CLI.
- Evals for both skills.
- The design of the HTML template itself.

## Order of work

1. Draft `principles.md` and hand it to Hunter.
2. Schema, render script, template. Render a sample roadmap and look at it.
3. `ops-audit` SKILL.md and references.
4. `ops-foundation` SKILL.md and references.
5. Glossary, evals, catalog, redirects.
6. Two independent reviews against `writing-for-agents` and `write-a-skill`, then unslop, then publish only on Hunter's word.
