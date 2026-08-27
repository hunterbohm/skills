# Build on the owner's runtime, not a skill-owned runner

Until 2026-08-27 `workflow-build` wrote its own bash, python, or node runner into the workspace. Real builds never used that layout; they ran on whatever the owner already had (an agent scheduler, an automation platform, cron). Decision: the build spec stays runtime-neutral, `workflow-build` implements it on the owner's existing runtime, and `references/runtime-rules.md` states the invariants every runtime must satisfy (model only in the joint, dry-run read from configuration, gate stops the run, verify reads back, one log line per run). The workspace keeps `implementation.md` (where the build lives, how to run, switch, and stop it) and `runs.jsonl` as the record of truth.

Consequences: a runtime that cannot append to `runs.jsonl` names where its records live, and the report branch imports them before it computes value. The skill no longer prescribes a language or folder layout for the implementation.
