---
name: project-control
description: Project lens that builds an adaptive Codex App visualization from the active project's real sources. Use for project orientation, planning, verification, scenario exploration, or refresh.
---

# Project Control

Create a current **project lens** inside the Codex App: a disposable visual over canonical project sources, never a second tracker.

## Compatibility

Codex App only. This release requires Codex inline visualizations, the model-invoked `visualize` skill, and `window.openai.sendFollowUpMessage`. Other agent harnesses are not supported yet.

## Run

1. **Route.** Read the nearest `AGENTS.md` or `CONTEXT.md` and resolve one owning workspace. Complete when one project and its source-of-truth surfaces are named.
2. **Read.** Inspect the smallest useful set of canonical sources: overview, tracker or task files, recent Git state, proof, decisions, and release material. Complete when every important claim in the proposed view has a source, uncertainty label, or explicit user report.
3. **Lens.** Answer the universal project questions in [references/project-lens.md](references/project-lens.md) without forcing project-specific concepts into fixed fields. Complete when the current situation, implication, blockers or unknowns, and next moves are clear in plain language.
4. **Choose.** Select the smallest useful visual from [references/view-selection.md](references/view-selection.md). Complete when each chosen view exposes a distinct, source-supported relationship the user needs to understand.
5. **Render.** Load Codex's model-invoked `visualize` skill, then build the in-task experience with the project-specific rules in [references/codex-app.md](references/codex-app.md). Complete when the first render is useful, interactions work, and the layout passes wide and narrow inspection without errors.
6. **Explain.** Lead with what is happening and why it matters, then show the visual. Complete when the response stands alone in plain language.

## Branches

- **Orient:** current reality, blockers, dependencies, decisions, and next moves.
- **Plan:** sequence, milestones, ownership, and critical path.
- **Verify:** criteria, tests, claims, receipts, and release gates.
- **Explore:** a user-named variable or tradeoff, clearly labeled hypothetical.
- **Refresh:** re-read canonical sources, regenerate the lens, and call out material changes.

## Guardrails

- Facts, inferences, and scenarios remain visibly distinct; missing evidence stays unknown.
- Metrics appear only when sourced or transparently derived.
- Project language stays plain; technical terms receive an ordinary-language explanation.
- The default run is read-only. Permanent boards, tracker edits, code changes, and external writes require an explicit request.
- Ambiguous ownership triggers one concise routing question.
