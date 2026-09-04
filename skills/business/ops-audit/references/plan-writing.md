# Writing the plan

Write `plan` after the cards and before the read-back. The plan is what the owner reads. The cards are the record behind it.

## Each step

- `title`: what will be true when the step is done, as a short sentence in the owner's terms from `business.md`.
- `do`: one to three lines saying what happens and who does it. The agent does moves and runs automations. The owner approves.
- `you_decide`: the one thing the owner must approve. For a hold, the decision already made and when it is revisited.
- `done_when`: what the owner will see when the step is complete. The card's `proof` in plain words.
- `never`: a hard limit worth stating, such as "Nothing sends without you." Null when none applies.
- `lane`: `main` for steps that happen in order, `parallel` for steps that do not wait. Holds sit in the parallel lane.

The first main-lane step is the first move. Order main-lane steps by dependency, not by size. Put a step in the parallel lane only when nothing in the main lane depends on it. Write `first_move` as the card of that first step, `first_automation` as the card of the first automation step or null when there is none, and `first_automation_reason` as one sentence when `first_automation` is null and null otherwise.

## Words

Use the owner's words. Do not use audit words in any step field. Replace them:

| Do not write | Write |
| --- | --- |
| register, ledger, store | the owner's name for it, or "page", "list" |
| migration, migrate | "move onto", "copy onto" |
| consented sources, source categories | the sources by name: "your mail", "your messages" |
| read-back, read back | "checks the result" |
| waypoint, WP-01, card, verdict, intervention, causal path | nothing; the plan has steps |
| canonical | "the one" |
| non-truncated | "complete" |
| leverage move, keep human, automate with an agent | "the agent does this once", "stays by hand", "the agent runs this" |
| approval gate | "you approve" |

## Voice

Write each step the way the owner would say it back.

- Lead with the result. The `title` is what will be true when the step is done, not what will be attempted.
- Keep every line as short as it can be and still be correct. Cut a line the owner would not say out loud.
- One decision at a time. `you_decide` names one decision, never two.
- Plain English before mechanics. Say what the step does for the owner before anything about how it runs. A runtime, a trigger, or a schedule belongs in the automation's proposal message, not in a step.
- The owner's only verb is decide. No step asks the owner to type, paste, open, copy, or carry anything. A step that needs that is the wrong step.
- Say plainly what is unfinished. A step resting on an unknown cost, an unread source, or a stated limit says so in `do`, in the owner's words, instead of reading as settled.
- Reuse the owner's own terms from `business.md` for the thing being fixed. A word the owner never said does not appear in a step.

## What you can reach

Before writing steps, list what you can use by name: the connections inventory (connector CLIs, MCP servers, secret stores), the skills in this session, and the machines the harness inventory reached. A step the agent will do must name which of those it will use, in `do` or in the proposal message. When a step would need something you do not have, do not drop it and do not ask the owner to do it by hand: write it as an `extensions` entry, `add` in the owner's words (a connection to their mail, a browser the agent can drive, a second machine, a skill) and `unlocks` as the step or time it would save. The read-back prints these under "If you add:" so the owner can grow the agent on purpose.

## Read back

The plan reaches the owner only in chat. Print it with `scripts/workspace.py plan <workspace>` and paste it: the title and the one decision per step, main lane first, with its status. Ask one question: "Is this the order?" Change it until the owner says yes. Show a step's lines with `--full` only when the owner asks.

The plan is proof only when the owner can say, without help, what happens first and what they must approve. A validated file is not proof.
