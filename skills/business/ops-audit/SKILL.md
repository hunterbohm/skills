---
name: ops-audit
disable-model-invocation: true
description: "Diagnose operational work from consented evidence and render one offline roadmap. Use only when the owner explicitly invokes it."
---

# Operations audit

Use this skill only when the owner explicitly invokes it. It diagnoses operations; it does not install a workspace protocol or change connected systems. `references/principles.md` is the authoritative operating-rules list for every step below.

## Method

1. **Interview.** Ask one question at a time. Ask the owner's hourly value first, then their terms, people and roles, tools, rhythms, never-automate list, and named time sinks. Offer a recommended answer first when choices help. Record answers in `business.md`. Stop cleanly when the owner says stop; mark the audit incomplete.
2. **Get consent.** Before consent, inspect only connection metadata and owner-declared source roots. List reachable categories: mail, calendar, chat, documents, scripts and scheduled jobs, automation definitions, recent run records and outputs, failure visibility, past transcripts, and owner-added personal operations. Ask for category consent and exclusions. For an excluded root record only its owner-declared root/account identifier and category, never a filename. Read no source until consent.
3. **Inspect evidence.** Read the smallest useful slice. For each category, identify authority, recent examples, and gaps. Treat scripts/jobs, automation definitions, recent runs, outputs, and visible failures as the dedicated existing-coverage source. Keep systems read-only and redact secrets and unsafe source text from outputs.
4. **Reconstruct causes.** For each sink, record the structured trigger → collection → judgment → action → destination → read-back → failure-visibility path. Split paths when safeguards differ. Label each evidence claim observed, owner-reported, or inferred. Patterns are hypotheses, not proof; load `references/patterns.md` only after this diagnosis.
5. **Choose intervention.** Record the selected intervention, existing automation definitions/runs/outputs/failure visibility, gaps, and any approval/gate in the card contract.
6. **Prove and render.** Validate `roadmap.json` with `scripts/render.py`; it calculates only derivable values and writes the sole owner-facing result, `roadmap.html`. A complete roadmap has exactly one first move. `first_automation` may be null only with a written reason.

## Completion and resume

Choose a workspace only after the method requires one; ask once for its location. Read `references/workspace-contract.md` before writing. A complete audit has interview answers or stated gaps, recorded consent, evidence or stated unavailable sources, causal cards, one first move, and a rendered roadmap. On partial stop, write state with the stopping point and render an incomplete roadmap; do not infer missing work.

On resume, read `state.json`, apply feedback first with `scripts/apply_feedback.py`, then compare newly consented sources with recorded evidence and re-render. The applicator validates and transactionally records pending per-card feedback against the immutable roadmap ID and both revisions; it does **not** rewrite agent-authored recommendations. Resume applies each pending semantic request to the diagnosis and cards, then increments roadmap and state coherently and re-renders. It rejects malformed, stale, duplicate, cross-roadmap, and revision-conflicting feedback without overwriting a conflict.

## Handoff

After the owner approves the roadmap, record identical `owner_approval` objects in `roadmap.json` and `state.json` with the current roadmap ID, revision, named approver, and timestamp; re-render. ops-audit may then invoke model-visible ops-foundation automatically when that skill is installed. Until it exists, state that the roadmap is approved but handoff is unavailable; do not create a replacement or silently start implementation.

## References

- `references/business-profile.md` — the interview output fields.
- `references/interview-and-consent.md` — questions, consent, and scan tactics.
- `references/causal-diagnosis.md` — evidence, causal paths, and interventions.
- `references/principles.md` — operating principles and concise source notes.
- `references/patterns.md` — post-diagnosis hypotheses only.
- `references/roadmap-schema.json` and `references/state-schema.json` — machine contracts.
- `references/feedback-grammar.md` — revision-safe feedback format.
- `references/workspace-contract.md` — workspace and resume rules.
