# Owner summary template

Regenerate `owner-summary.md` in the workspace root at the end of every run —
audit, build, prove, or report. Overwrite the whole file — history lives in the ledger
and run logs, not here. Compute the value figures per
`references/workspace-contract.md` before writing. Write in plain language
for the owner: no ladder jargon without a gloss, no file paths, no agent
terminology.

```markdown
# <Business> — where things stand
_Updated <date> after <audit|build|prove|report> run_

## Needs you
The approvals, confirmations, and blockers only the owner can clear.
One line each: what, why it waits on them, what happens once cleared.
If nothing: "Nothing waits on you."

## Your workflows
One line per inventory workflow past candidate: name, plain-language status
("built and tested on sample data, not yet live"), last run date, and whether
it verified.

## What it's returning
The workflow's returned hours and value so far, and whether it is being used
as often as expected — labeled as estimates from the owner's own numbers.
Say plainly when a live workflow is not being used. If nothing is live yet,
state the baseline cost of the chosen workflow — what building it is worth.

## Next single action
One sentence: the smallest thing that moves the first workflow up one rung.
```
