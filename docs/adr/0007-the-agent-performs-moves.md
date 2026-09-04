Status: the foundation parts are superseded by ADR 0009; the agent-performs-moves decision stands inside ops-audit.

# The agent performs one-time moves; the owner decides

ADR 0005 left leverage moves for the owner to carry out. The first real plan's step 1 was making a page, gathering follow-ups onto it, and marking them, which is mechanical work, and nothing tracked whether it was done before the foundation started building step 2. On 2026-09-01 Hunter said he will not be a meat proxy: the agent does every move under his approval, with read-back and a receipt, and he only decides. The never-automate list constrains decisions, not typing.

Consequences: the foundation gains a Do branch and tracks moves (proposed, approved, done) beside automations. It takes the next eligible step in plan order, so a second automation needs no new audit. The runtime questionnaire inspects the machine, proposes every answer, and asks for one confirmation. The foundation writes the workspace map into the workspace `AGENTS.md` itself and offers to add one pointer to the owner's global configuration; it no longer asks the owner to edit configuration by hand.
