# The audit delivers the owner's plan; cards are the record behind it

The first real run (personal operations, 2026-08-31) rendered every card field onto `roadmap.html` and the owner called the page slop. Four redesigns kept failing because the schema had no way to say order, parallel work, holds, what the owner decides, or when a step is done, so every draft invented those from audit fields and carried audit words with them. On 2026-09-01 Hunter decided: `roadmap.json` gains a `plan` of steps written in the owner's own terms, each step pointing at one unchanged card. `roadmap.html` renders the plan and puts each card behind one disclosure. Nothing on the first screen is a metric; the Now, Next, Later groups go, replaced by lane and order.

Considered and rejected: deriving the plan in the renderer (the renderer may only calculate derivable values, and order and plain language are not derivable), and a separate `plan.json` (two files to keep coherent across revisions).

Consequences: `card.group` is removed. `card.proof` means what would show the action worked; the step's done-when line is its plain twin. The renderer reads `state.json` too, so the page shows what is done. This supersedes the first-screen and card-layout parts of ADR 0004.
