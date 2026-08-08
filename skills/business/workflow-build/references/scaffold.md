# Scaffold layout

Create under `workflows/<n>-<slug>/` in the audit workspace:

```text
runner            # one deterministic entry point
joint-prompt.md   # fixed agent-joint instruction contract
fixtures/         # spec fixture as runnable input + expected output
adapters/         # act adapter: dry-run (default) and live modes
runs.jsonl        # created empty; only the runner's log stage appends
```

- **runner** — bash, python, or node; pick what the owner's machine already
  runs. It owns sequence, state, timeouts, the one-retry rule, and
  idempotency exactly as the spec defines. Stages: collect → agent joint →
  gate → act → verify → log. The model is called only inside the agent-joint
  stage.
- **joint-prompt.md** — input schema, task, required output schema, allowed
  evidence, prohibited claims, ambiguity fields. The runner sends it
  verbatim; editing it is a spec change.
- **adapters** — the runner reads `dry-run` vs `live` from configuration,
  never from model output. Dry-run prints the exact would-be write.

Rules:

- Collect and act are plain scripts or API calls. If a stage seems to need
  open-ended model judgment, the workflow is too wide — go back to the spec.
- The gate stops the runner and presents the spec's approval object; it never
  auto-approves. In fixture mode the gate records `fixture-approved` so the
  pipeline is testable end to end.
- Agent-joint calls go through whatever agent CLI or API the owner already
  has. Validate the output schema in the runner: retry once on malformed
  output, then route to a human per the spec.
- Verify reads the destination back. In dry-run mode, verify compares the
  printed action against the fixture's expected output.
