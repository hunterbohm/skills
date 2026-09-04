Status: superseded in part by ADR 0006 (first screen and card layout) and ADR 0008 (feedback).

# The audit delivers an interactive roadmap rendered from a template

Until 2026-08-30 `workflow-audit` delivered a markdown inventory, an owner summary, and a build spec for one workflow. Real runs wrote 7,000 to 10,000 words per workspace and picked a workflow the owner already automated. Decision: the audit hands over one file, `roadmap.html`, rendered from `roadmap.json` by a script the skill ships. The template is designed once; the agent only writes the data. Cards are per time sink, grouped Now, Next, Later. Each card carries hours and dollars from the owner's numbers, the evidence, what already runs, and a verdict: keep human, leverage move, or automate with an agent. Two cards are marked, the first move and the first automation.

Feedback travels by clipboard. Each card has accept, change, and reject controls and a note box. Notes persist in the browser. One button copies a markdown block with card ids and a two-line header that tells any agent to update the ledger and re-render. This was chosen over a local sidecar server and over cloud comment threads because the page must work as a plain file and must feed Claude Code, Codex CLI, and a Discord-based agent alike (research on 19 tools, 2026-08-29).

The interview writes `business.md` first: the owner's terms, people and roles, tools, rhythms, never-automate list, hourly value. The roadmap and the build read it. Sixteen anonymized agency patterns ship as a reference the roadmap can cite when a card matches one.

Consequences: `workflow-audit.md`, `owner-summary.md`, and the standalone build spec go away. The ledger stays behind the HTML. A feedback block is a ledger write, so the resume branch parses feedback before it diffs sources. The render script is Python 3 with no dependencies. The HTML makes no network requests.
