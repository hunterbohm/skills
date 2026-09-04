# Chat is the only owner output

After the one-skill decision, Hunter approved the revision-3 plan from a numbered list read back in chat without ever opening the rendered page, and asked whether the page was necessary. It was not: four HTML drafts had failed the same comprehension test the chat list passed, and the page existed only because ADR 0004 made an HTML file the deliverable. On 2026-09-01 he decided the owner reads nothing in a file. Decision: the audit's only owner-facing output is the plan printed to chat by `scripts/workspace.py plan`; `roadmap.json` and `state.json` are the record. The renderer, `roadmap.html`, and the generated `AGENTS.md` section are removed.

Consequences: supersedes ADR 0004 and the rendering parts of ADR 0006 and 0009. Comprehension proof is the owner restating the plan in chat. No page, no design pass, no brand tokens.
