# Workflow contract

`workflows/<card-id>/contract.json` is internal. There is no standalone owner-facing build specification. Validate it with `scripts/foundation.py validate-contract`.

The contract binds stable `roadmap_id`, `roadmap_revision`, `card_id`, and `card_version` to the approved card. It records card and business evidence references, the owner-selected runtime answers, owner baseline, fixture input and expected dry-run action, and this fixed spine:

1. trigger;
2. deterministic collect;
3. one agent joint with fixed input schema, fixed output schema, fixed prompt/task, and allowed evidence;
4. named gate if action is consequential;
5. deterministic act;
6. destination read-back verification;
7. receipt/log.

The joint output must be machine-parseable. Dry-run is runtime configuration, never model output. The contract names the idempotency key basis and visible failure destination. It may not add another agent joint or let an agent sequence stages.
