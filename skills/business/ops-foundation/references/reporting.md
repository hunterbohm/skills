# Reporting

Run `scripts/foundation.py report <workspace> <card-id> <YYYY-MM>`. It validates the contract against the current approved roadmap and imports normalized records from the configured runtime `record_source` before reporting (unless that source is local `receipts.jsonl`). Count unique verified real receipts in the requested month only. Realized hours and realized value in the output are monthly, not all-time: hours equal count times `hours_per_run`; value equals hours times `hourly_value` only when both are owner-provided. Adoption gap is baseline monthly runs minus verified real runs in that month.

Show the verified count, pending verification, failures, unknown values, and adoption gap. Do not use fixture or activation receipts as realized work. Each recorded failure can produce one proposed concrete rule. Put a proposal in the report; write it to `rules.md` only with the owner's explicit approval. A failure that removes required proof lowers the workflow status.
