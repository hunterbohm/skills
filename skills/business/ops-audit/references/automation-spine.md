# Automation spine

Build every automation on the owner's runtime in this fixed order. The agent never controls the order.

1. **Trigger.** A deterministic event or schedule the owner named in words.
2. **Collect.** A script fetches the smallest evidence needed, from sources named in `sources.md` only, through a connection the connections inventory lists: a connector layer, a vendor CLI, an MCP server, or a token in the owner's secret store. Whatever the owner already uses is the right one; the spine does not care which.
3. **Agent joint.** One bounded judgment with fixed input, fixed output shape, and fixed prompt. Malformed output: retry once with unchanged input, then record a visible failure and stop.
4. **Gate.** A consequential action waits for the named approver.
5. **Act.** A deterministic tool performs the approved action once, keyed so a replay cannot repeat it.
6. **Verify.** Read the destination back. An ambiguous result stops the run and reports; no blind retry.
7. **Log.** One line per run: trigger, sources, decision, approval, result, verification. No secrets.

Unattended jobs need credentials that outlive a terminal session. A Google OAuth app still in testing mode expires every token after seven days; use a connector layer or a published app for anything scheduled. Before the first real run, run once in dry-run so the act stage shows what it would write. Before a schedule turns on, the owner approves the exact trigger in words. The step's done note records where it runs, how to run it, how to switch it off, and where failures go.
