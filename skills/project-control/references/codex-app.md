# Codex App experience

Project Control renders inside the current Codex task. The project lens supplies the meaning; Codex's model-invoked `visualize` skill supplies the current fragment contract.

## Output

- Write a new HTML fragment in the thread-scoped visualization directory.
- Keep project data inline and the root ID unique.
- Show it with `::codex-inline-vis{file="<filename>.html"}` on its own line.
- Treat the fragment as a task-local view unless the user explicitly requests a persistent board or published site.

## Interaction

Keep presentation changes local. For a Codex follow-up, carry the selected context into the conversation:

```js
await window.openai.sendFollowUpMessage({
  title: "Explain selected item",
  prompt: "Project outcome: ... Selected item: ... Evidence: ... Uncertainty: ... Explain what this means, why it matters, and the next three moves. Use plain language. Explain any technical terms."
});
```

The first render answers the user's immediate question without requiring a click. Add controls only when they reveal a real relationship or scenario.

## Verification

Before replying, apply the loaded `visualize` skill and verify:

- literal fragment markup and scoped JavaScript
- every queried element and primary interaction
- theme-aware color and accessible controls
- useful first render at conversation width
- clean reflow near 320px
- zero page errors, clipped labels, empty views, or unsupported claims
