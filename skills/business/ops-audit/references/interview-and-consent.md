# Interview, consent, and source scan

Ask one question, wait, record the answer in `business.md`, then ask the next. Offer a recommended answer first when choices help. With a focus, ask question 1 about that area alone, skip the questions the focus does not need, and ask consent only for the sources it touches.

1. "What eats your time or attention most? Name the top few." Record each as a named time sink.
2. "What do you call this business or operation?" It heads every plan you print back.
3. "What do you call the parts of your operation?" Record the owner's terms. The plan reuses them.
4. People and roles.
5. Tools.
6. Daily, weekly, and monthly rhythms.
7. Never-automate work: decisions the owner keeps.
8. "What hourly value should I use for your time? Unknown is valid." Do not calculate from a guessed rate.

Before consent, list connection metadata and roots the owner declares. Ask one yes-or-no per category, naming the scope you already found: "May I read <category> in <the account or folder you can see>?" Ask about a second account or an exclusion only when the owner's answer names one. Categories: past agent sessions, mail, calendar, chat, documents, scripts/jobs, automation definitions, run records/outputs/failures, and optional personal operations. Log exclusions as `{category, declared_root_or_account}` only.

After consent, use category tactics: sample recent threads and labels (mail/chat); compare events with follow-up work (calendar); inspect current documents and revisions; inspect scripts, scheduler entries, definitions, last runs, output destinations, and error/alert records. Read only enough to establish a claim. Never execute, enable, or alter an automation.

## Source map

While inspecting, write `sources.md`. One entry per consented source:

```text
## <source, in the owner's words>
- Owns: <what truth this source holds>
- Read by: <who, and through which connection from the connections inventory>
- Write approved by: <named person, or "no writes">
- Current as of: <how fresh it is, or "unknown">
- Write verified by: <how a write is read back, or "no writes">
```

Every automation names its sources from this file. A source not in the map is not read or written by an automation.
