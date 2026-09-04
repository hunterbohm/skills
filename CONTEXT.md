# Operations audit

Terms for the `ops-audit` skill.

## People

**Owner**: The person in the chat who owns the business, accounts, and runtime. The owner decides and approves; the agent does the rest. A named approver may clear a consequential action.

## Audit

**Audit**: The consent-based diagnosis that produces the plan, the cards behind it, and the source map.

**Mining**: Reading consented sources, past agent sessions first, for hand work, repeats, corrections, re-dos, and existing automation.

**Source map**: `sources.md`: per source, what truth it owns, who may read it, who approves a write, how current it is, how a write is checked.

**Card**: The audit's diagnosis of one time sink: evidence labelled observed, owner-reported, or inferred, causal path, existing coverage, intervention, proof, and verdict.

**Proof**: What would show a card's action worked, in audit words.

**Verdict**: leverage move, automate with an agent, or keep human. The plan turns these into a move, an automation, or a hold.

## Plan

**Roadmap**: `roadmap.json`, holding the plan and the cards.

**Plan**: The ordered steps the owner reads in chat, in the owner's own terms. Each step points at one card.

**Step**: One thing that will happen, who decides, and when it is done. A move, an automation, or a hold.

**Lane**: Main-lane steps happen in order. Parallel-lane steps do not wait.

**Move**: A one-time change the agent performs once, under approval, and checks.

**Automation**: Work the agent builds on the owner's runtime to run on a trigger, following the spine.

**Hold**: Nothing changes for a stated period; it ends with a new decision.

**Done when**: What the owner will see when a step is complete.

**You decide**: The one decision the owner must make for a step.

**First move**: The first main-lane step.

**First automation**: The first automation step, absent only with a written reason.

**Feedback**: The owner's words in chat asking for a change. The agent applies it, bumps the revision, and records the change.

## Workspace

**Workspace**: The folder the owner chose for one business; see `references/workspace-contract.md`.

**Step status**: A move or automation runs proposed, approved, done. A hold runs holding, ended. Each status carries the owner's words or what was done.

**Eligible step**: The next step the agent may take: a main-lane step once every earlier main-lane step is done, a parallel-lane step at once, a hold never.
