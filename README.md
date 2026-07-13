# Hunter Bohm's agent skills

I kept re-explaining the same specialist workflows to every agent.

This repo is where I'm packaging the good ones so you can install them in one command. Some are portable across Agent Skills-compatible clients; others are built for a specific host and say so clearly.

Preview what the repo exposes before installing:

```bash
npx skills@latest add hunterbohm/skills --list
```

## Codex App skills

### Project Control

**Compatibility: Codex App only.** This release relies on Codex inline visualizations, its model-invoked `visualize` skill, and `window.openai.sendFollowUpMessage`. Other agent harnesses are not supported yet.

Install it globally:

```bash
npx skills@latest add hunterbohm/skills --skill project-control --global
```

`project-control` reads the active project's real sources and builds the smallest useful interactive view for the situation. It might produce a dependency map, timeline, evidence ledger, decision map, workflow, readiness view, scenario lab, or a project-specific visual that fits better.

It keeps the process predictable without forcing every project into the same schema. The project's own vocabulary and evidence determine what appears.

Try it in a Codex App task opened inside a project:

```text
Use $project-control to get me on top of this project.
```

You can also ask it to show what is blocked, assess release readiness, explore a named tradeoff, or refresh the view from current sources.

## Cross-runtime skills

### Ask Hormozi

I love Hormozi's advice. I hated how generic it became when I asked an AI to apply it.

Install it globally with the open-source `skills` CLI:

```bash
npx skills@latest add hunterbohm/skills --skill ask-hormozi --global
```

`ask-hormozi` is an unofficial business advisor built from Alex Hormozi's published frameworks.

Most "what would Hormozi say?" prompts produce motivational soup. This skill does six harder things:

1. Finds the current constraint: leads, sales, delivery, profit, offer, or focus.
2. Checks whether the cash-flow-business playbook fits before applying it.
3. Uses the smallest relevant framework instead of dumping every framework it knows.
4. Shows the unit economics with consistent CAC, gross-profit, and payback definitions.
5. Separates exact linked excerpts from paraphrases and book citations, so the agent knows what it may actually quote.
6. Escalates to live primary-source research only for recent, exact-wording, or uncovered questions.

The current release ships 243 evidence entries:

- 111 transcript-verified excerpts, each capped at 20 words: 84 original YouTube source pages and 27 public transcript-mirror pages
- 112 paraphrase-only entries: 91 with public links and 21 title-level episode citations
- 20 book or source citations with no invented quotation

The evidence snapshot is generated from [`hunterbohm/hormozi-glossary`](https://github.com/hunterbohm/hormozi-glossary) at revision [`b385873d66c7`](https://github.com/hunterbohm/hormozi-glossary/commit/b385873d66c75e31d6625cb49e217d0231f1169c). Framework guides are compact paraphrased operating guides; only the evidence layer may supply quotations. The glossary is the upstream research corpus, not a runtime dependency.

Live research is optional and tool-agnostic. When the installed agent has public search or transcript access, the skill can verify current claims against primary sources. Without those capabilities, it says the live check could not run and stays inside the shipped snapshot.

#### Try it

In Codex or another Agent Skills-compatible client:

```text
Use $ask-hormozi. We close 35% of qualified calls, retain clients well,
and have capacity, but only get six qualified calls a month. CAC is $400
and first-30-day gross profit is $1,600. What is the constraint?
```

The useful part of the answer should be boringly clear:

```text
Verdict: leads are the constraint.
Math: $1,600 / $400 = 4.0x first-30-day GP:CAC.
Today: choose one proven acquisition path and set a measurable weekly input.
```

It also knows when to stop cosplaying a guru:

- It will not invent missing economics.
- It will not scale a model with broken delivery or retention.
- It will not apply short-payback rules blindly to pre-revenue, regulated, deep-tech, or two-sided-marketplace problems.
- It will not turn an unsupported sentence into a Hormozi quote.

## Repository layout

```text
skills/
  ask-hormozi/
    SKILL.md
    agents/openai.yaml
    evals/evals.json
    references/
  project-control/
    SKILL.md
    agents/openai.yaml
    references/
```

Each installable skill is self-contained. Runtime-specific requirements are stated in its README section and skill package.

## License and attribution

Hunter Bohm's original work is available under the [MIT License](LICENSE). Third-party material is governed by its respective owners; see [Third-party notices](THIRD_PARTY_NOTICES.md).

`ask-hormozi` is unofficial and is not affiliated with, endorsed by, or sponsored by Alex Hormozi or Acquisition.com.
