# Mining evidence

Read the smallest slice that settles a claim. Label every claim observed, owner-reported, or inferred. Redact names, addresses, amounts, health details, and secrets before anything leaves its source; keep only pointers and counts in the workspace.

## Past agent sessions

Every agent the owner has used left session records on disk. Find them first, then digest, then read.

1. **Inventory.** `scripts/harnesses.py inventory` on this machine, and `inventory --host <ssh alias>` for each other machine the owner names. It knows the storage conventions of the common agents (Claude Code, Codex, pi, Hermes, Gemini CLI, Cursor, OpenCode, Aider, Copilot, Goose, and more) and reports any other sessions-like folder as `unknown` for the owner to name. It reads names, sizes, and dates only. Run `scripts/connections.py inventory` beside it, on the same machines: it lists the connector CLIs on PATH with their sign-in state, the MCP servers each harness has configured, and the secret stores, by name and state only, never a value. That list is what an automation may use to reach an account; write each source's "Read by" line from it. Aider writes its history into the folder it ran in, so the inventory finds it only for runs from the home directory; ask the owner where else they ran it. Read the table back and ask consent per store in one question.
2. **Digest.** For each consented store: `scripts/digest.py --root <root> --harness <name> --out <workspace>/mining/<host>/<name>`. It samples the twenty most recent and ten largest sessions, writes one bounded Markdown digest per session with the owner's turns and the agent's final reply per turn, tool counts, dates, and project, and an `index.json` of counts. Emails, URLs, key-like strings, phone numbers, and amounts are replaced before writing. Names, addresses, and health details are not matched by pattern, which is why digests stay in `mining/`, never committed, synced, or shared. The digester reads `.jsonl` files of at least 2048 bytes and nothing else; a store the inventory marks `sqlite`, `json`, `markdown`, or `mixed` has no reader yet, and the digester exits with a message instead of an empty digest. Compare the printed `N of M` with the file count the inventory reported for that root, record any shortfall as a stated limit, and say in chat which of the owner's agents could not be read.
3. **Read.** Read the digests, not the sessions. Look for:
   - **Hand work.** Things the owner did themselves that an agent could have done with approval: pasted output between tools, ran a command the agent could run, edited a file or a config by hand, carried a result from one place to another, relayed a screen.
   - **Repeats.** The same request, or the same shape of task, in three or more sessions.
   - **Corrections.** The owner correcting the agent for the same reason more than once. Each is a rule candidate for `business.md`.
   - **Re-dos.** Work done again after a failure, a lost result, a context reset, or a session that ended early.
   - **Existing automation.** Scripts, jobs, and schedules mentioned, and whether they ran or failed.
   - **Unproven work.** Whether the owner has done this the same way more than once by hand. Never automate an unproven workflow; a task the owner will not repeat is a distraction, not a candidate.
   - **Craft and people.** Work the owner does because it is theirs: writing that goes out under their name, their community, the judgment they would not hand over. Mark it keep human before counting anything.
   - **The slow part.** Where the time actually went in the session, not where it felt slow. Find the slow part before proposing anything.
   - **Inputs and their home.** Whether the work's inputs live somewhere nameable. Every automation is only as smart as its inputs; work with no named source is a source-map step, not an automation.
   - **Nursing.** Automations and setups the owner keeps repairing to keep them running. Constant maintenance means it is not a system, and the candidate is removal.
4. **Count.** With a focus, read only the digests whose text matches the focus words and say how many were set aside. Count each finding across sessions and hosts. Three or more occurrences is a time-sink candidate; record the count and the date range as the source, for example "observed in 7 sessions across two machines, 2026-07-02 to 2026-08-30". One occurrence is a note, not a card. Other people's words in a session never leave the digest.

## Mail, calendar, and chat

Sample recent threads and labels. Compare calendar events with the follow-up work they caused. Look for replies owed, replies awaited, and the same question answered more than once.

## Scripts, jobs, and automations

Inspect definitions, scheduler entries, last runs, output destinations, and error records. A job with no recent run is not coverage. Never execute, enable, or alter anything.

## Documents

Inspect current documents and their revisions for lists kept in more than one place and structures the owner started and stopped using.

## What becomes a card

A candidate becomes a card when it has at least one observed claim and a causal path the owner recognizes. A pattern from `patterns.md` never substitutes for evidence. Unknown cost stays unknown.
