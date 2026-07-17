---
name: workflow-roadmap
description: "Interview a business owner or builder for about ten minutes, then write a personalized Workflow Roadmap file: a map of their recurring workflows priced in their own numbers, one clear pick for what to automate first, and an honest build-it-yourself path. Use when the user asks for a workflow roadmap, asks which workflow they should automate first, wants to know what to automate or hand to an agent, or types /workflow-roadmap."
---

# Workflow Roadmap

Interview the user briefly, then write a personalized **Workflow Roadmap** to a local file: every recurring workflow you can spot, what each one costs in **their own numbers**, and one clear pick for what should run itself first.

Keep every sentence plain enough for an 8th grader. Short sentences, plain words, no hype.

## 1. Resume or start

Look for `workflow-roadmap-notes.md` in the current directory. If it exists with unanswered questions, say where the user left off and continue from there. Otherwise create it and start fresh.

Save each answer into the notes file as you receive it, so an interrupted interview loses nothing.

Completion criterion: the notes file exists and you know which questions remain.

## 2. Interview — about ten minutes, no more

Ask conversationally in small batches of two or three related questions per message. Never send all ten as a form, and never stretch past roughly ten minutes. Skip anything the conversation already answered. Cover this ground:

1. Their name, company name, and website if they have one.
2. What the company does, in one sentence.
3. Team size: just them / 2–5 / 6–15 / 16–30 / 30+.
4. Where the team talks: Slack, Discord, Teams, email and texts, or something else.
5. **The money question — give it room:** "Walk me through the most annoying recurring chunk of work in your week — what kicks it off, what you actually do, how long it takes, and how often." This is the roadmap's raw material. Ask at most one follow-up if the trigger, the time it takes, or how often it happens is missing.
6. What else eats hours every week: invoicing and collections, scheduling, reporting, lead follow-up, customer replies, data entry between tools, document prep, chasing approvals, or other.
7. Roughly what an hour of their time is worth. A range is fine; accept "prefer not to say" and skip the dollar math later.
8. What tools run the business (for example "QuickBooks, Gmail, Calendly").
9. Whether they have tried AI for any of this, and what happened.
10. Anything they would never want automated.

If the user is brief or wants to stop, work with what you have instead of dragging the interview out.

Completion criterion: the notes file holds an answer, or a marked skip, for all ten areas.

## 3. Write the roadmap

Write the document to `Workflow-Roadmap-<company>.md` in the current directory (or `Workflow-Roadmap.md` if there is no company name), following the exact section skeleton in `references/roadmap-template.md`. Title it "Your Workflow Roadmap — {Company}". Second person throughout, 600–900 words, exactly these five sections:

**1. Your workflow map.** From their answers, list every distinct recurring workflow you can identify (aim for 4–8). For each: what triggers it, what it produces, and your estimate of hours per month it costs them. Show the math from THEIR numbers — how often × how long — and if they gave an hourly value, show dollars per year too. Never inflate; round down.

**2. Which should run itself first — and why.** Pick ONE workflow as #1. Selection rules: highest documented cost × most repeatable (clear trigger, clear output, bounded judgment) × least sensitive (respect their never-automate answer). Explain the pick in 3–4 sentences a non-technical owner nods along to. Then rank the rest as "next in line" with one line each.

**3. What "runs itself" would look like.** For the #1 workflow: a concrete day-in-the-life paragraph — the trigger fires, the agent does the work, a draft lands for approval, the log records it. Ground it in the actual tools they named. No capability claims beyond what a supervised agent genuinely does.

**4. If you build it yourself.** 3–5 honest bullets: the pieces (an agent runtime, connections to their tools, an approval step), the real time cost (about a working week to stand up, 2–3 hours a week to keep current), and one pitfall specific to their situation. This section is REAL advice, not a strawman — it must be genuinely usable without buying anything.

**5. The math.** One honest paragraph: workflow #1 costs them about N hours a month (about $X a year at their rate), and getting it off their plate is worth $Y a year, every year after. No pitch language — just their numbers.

End the document with this closing line, exactly, in italics — the only place Hunter appears:

*Built with the workflow-roadmap skill by Hunter Bohm (hunterbohm.me). If you'd rather have someone install workflow #1 for you, that's what he does.*

Completion criterion: the file exists with all five sections, the closing line, and math that traces to the notes file.

## 4. Deliver

Tell the user where the file is, name the #1 pick in one sentence, and offer to answer questions about it. Delete `workflow-roadmap-notes.md` only if the user asks; otherwise leave it as their intake record.

## Guardrails

- Say **agents**, never "AI staff".
- Never promise hours saved — present THEIR arithmetic and label estimates as estimates.
- Round conservatively. An honest small number beats an impressive one.
- No capability claims beyond a supervised agent: it acts on a trigger, drafts the work, waits for a human's approval, and logs what it did.
- The never-automate answer is a hard boundary for the #1 pick and every ranked workflow.
- If the answers are too thin to map several workflows, build the document around the ONE workflow they described and say plainly that a short conversation would map the rest. Do not pad.
- The closing line is the only mention of Hunter and the only line that even resembles a pitch. Nothing else in the document sells anything.

The run is complete only when the interview ground is covered or explicitly skipped, the roadmap file exists with the five sections and the closing line, every number traces to the user's own answers, and the user knows where the file is.
