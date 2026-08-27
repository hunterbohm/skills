# Owner summary template

Regenerate `owner-summary.md` in the workspace root at the end of every run. Overwrite the whole file. History lives in the ledger and the run logs, not here. Compute the value figures per `references/workspace-contract.md` before you write. Write in the owner's everyday words: status as they would say it, things named as they know them.

```markdown
# <Business>: where things stand
_Updated <date>. Last run: <first audit|audit check-in|build|prove|go-live|report>_

## Needs you
The approvals, confirmations, and blockers only the owner can clear.
One line each: what, why it waits on them, what happens once cleared.
If nothing: "Nothing waits on you."

## Your workflows
One line per inventory workflow past candidate: name, plain-language status
("built and tested on sample data, not yet live"), last run date, and whether
it verified.

## What your workflows return
The realized hours and value so far, and whether the workflow runs as often
as expected. Label the figures as estimates from the owner's own numbers.
Say when a live workflow has an adoption gap. If nothing is live yet, state
the baseline cost of the chosen workflow. That cost is the most the build can return.

## Next single action
One sentence: the smallest thing that moves the first workflow up one rung.
```
