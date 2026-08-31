# Feedback grammar

The page copies this exact block. Roadmap and card IDs contain only ASCII letters, digits, underscores, and hyphens. One touched card per line; notes are required for `change` and may contain Unicode but not newlines.

```text
Feedback on roadmap <roadmap-id> revision <n>.
Update the ledger, then resume the audit to apply the requested semantic change and re-render.
- card <id> version <n>: accept|change|reject | note: <text>
```

Apply only one block at a time. The block identity is its complete normalized text. The immutable roadmap ID, card version, and state/roadmap revision must match. A successful application records a `pending` event in both roadmap and state and increments both revisions together; it never edits recommendation text. On resume, the audit reads those pending events, makes the requested semantic changes, increments both documents coherently again, and re-renders. Duplicate blocks, stale versions, cross-roadmap blocks, invalid choices, missing change notes, and revision conflicts are flagged without writing.
