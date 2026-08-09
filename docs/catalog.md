# Skill catalog

This file is generated from the installable packages under `skills/`.

Install any skill globally with its command below. Run `npx skills@latest add hunterbohm/skills --list` to preview the live repository.

## Business

### [Ask Hormozi](../skills/business/ask-hormozi/SKILL.md)

Apply Alex Hormozi's published business frameworks with constraint-first diagnosis and source-backed attribution. Use when the user asks what a Hormozi term or framework means; what Hormozi would do in a business situation; wants an offer, funnel, script, numbers, or draft analyzed through his frameworks; or wants a Hormozi attribution or current position verified against public sources.

**Compatibility:** Agent Skills-compatible clients

```bash
npx skills@latest add hunterbohm/skills --skill ask-hormozi --global
```

### [Workflow Audit](../skills/business/workflow-audit/SKILL.md)

Audit a business's recurring workflows from connected sources, in a durable audit workspace that compounds across runs. Use when an owner wants to know where work gets stuck, what to automate first, how to build a supervised agent workflow, or what changed since the last audit.

**Compatibility:** Agent Skills-compatible clients

```bash
npx skills@latest add hunterbohm/skills --skill workflow-audit --global
```

### [Workflow Build](../skills/business/workflow-build/SKILL.md)

Build, prove, and report on workflows specced by the workflow-audit skill. Use when the workflow-audit skill hands off a confirmed workflow, when the owner asks to build or implement a specced workflow, or when the owner asks for run history or what an automation has returned.

**Compatibility:** Agent Skills-compatible clients

```bash
npx skills@latest add hunterbohm/skills --skill workflow-build --global
```

## Project Management

### [Project Control](../skills/project-management/project-control/SKILL.md)

Project lens that builds an adaptive Codex App visualization from the active project's real sources. Use for project orientation, planning, verification, scenario exploration, or refresh.

**Compatibility:** Codex App only

```bash
npx skills@latest add hunterbohm/skills --skill project-control --agent codex --global
```
