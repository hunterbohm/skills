# Feedback is words in chat

ADR 0004 moved feedback by clipboard so the page would work as a plain file and feed any agent. In practice the owner is in the chat with the agent that rendered the page, so the clipboard made the owner the courier, and the grammar, applicator, ledger, transaction journal, and concurrency tests were built before a single real use. On 2026-09-01 Hunter decided: the owner says what is wrong in chat, the agent edits the roadmap, bumps the revision, and records a change entry in state. The page has no controls and no script.

Considered and rejected: keeping the clipboard as a fallback (two paths, neither proven). This supersedes the feedback part of ADR 0004 and removes `pending_feedback`, the feedback ledger, the applicator script, and the feedback grammar.
