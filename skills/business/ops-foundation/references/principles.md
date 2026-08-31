# Principles

- Keep a deterministic spine; use an agent only for bounded judgment. _Source note: operating-method notes._
- The agent never controls flow; one defined task has one required output. _Source note: runtime practice._
- Retry malformed output once, then flag it and do not act. Read the destination back. _Source note: run-safety notes._
- Unknown stays unknown; use owner numbers only. _Source note: audit practice._
- Inspect existing automations first. Remove, simplify, or use a deterministic rule before adding an agent. _Source note: duplicate-build review._
- No silent failure, then stop. Do not optimize before the work works. _Source note: build practice._
- Consequential actions wait for named approval. Adoption gap is a finding. _Source note: approval and reporting notes._
- Patterns are hypotheses, not evidence. _Source note: diagnosis practice._
