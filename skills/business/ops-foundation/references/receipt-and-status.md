# Receipts and status

Validate and append with `scripts/foundation.py append-receipt`. A receipt records run ID, idempotency key, time, mode, workflow ID, trigger, approval, action, dry-run state, read-back result, verification, failure flag, destination reference, `replay_verified`, and `explicit_instruction`. Secret values never enter a receipt.

Malformed joint output: retry once using unchanged inputs; on the second malformed result append a visible failed receipt and do not act. An ambiguous write is read back before retry; if still ambiguous append a visible failure and stop. A duplicate successful idempotency key is replay evidence, not another act or receipt. A failed attempt may reuse its key for a recovery receipt; preserve both receipts.

Use `scripts/foundation.py transition` only with the required evidence. The tool enforces the ordered ladder: `candidate → designed → built → proven → live`. `built` needs a verified fixture dry-run receipt. `proven` needs a current verified real receipt with `replay_verified: true` and named `approved_by` when the approved card requires approval. `live` requires prior `proven` plus a verified activation receipt with `explicit_instruction: true` and active-trigger read-back. The tool regresses a workflow when its current fixture, real-run, or activation proof fails.
