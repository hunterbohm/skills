# The subscription list

Use the owner's own list if they have one, in the tool they already use: a
spreadsheet, a notes app, or a Markdown file. Keep their columns and add only
the missing ones. Make a new file only when they have no list.

## Fields

| Field | Example | Notes |
|---|---|---|
| Name | Acme Notes Pro | The product, not the statement name. |
| Statement name | ACME*NTS 8442 | How it appears on the card. |
| Status | active, cancelled, paused | |
| Cost per month | 12.00 | A yearly plan divided by 12. |
| Billing cycle | monthly, yearly | |
| Next charge | 2026-03-14 | From a receipt or the last charge plus one cycle. |
| Owner | personal, business | Never mix totals across owners. |
| Paid with | Visa ending 4242 | Last four digits only. |
| Billed by | merchant, Apple, Google, reseller | Where a cancel must happen. |
| Decision | keep, 2026-02-01, "use it weekly" | The owner's words and the date. |
| Cancelled on | 2026-02-10 | The day access ends. |
| Proof | "Your plan ends Feb 10", email of Feb 3 | Screen text and email. |
| Last checked | 2026-02-03, card statement | Source and date of the latest evidence. |

## A new Markdown list

```markdown
# Subscriptions

<!-- settings
inboxes: personal mail, work mail
statements: CSV exports in ~/Documents/statements
owners: personal, business
last audit: 2026-02-03
-->

| Name | Status | Per month | Cycle | Next charge | Owner | Paid with | Billed by | Decision | Last checked |
|---|---|---|---|---|---|---|---|---|---|
| Acme Notes Pro | active | 12.00 | monthly | 2026-03-14 | personal | Visa 4242 | merchant | keep, 2026-02-03 | 2026-02-03, statement |

## Cancelled

| Name | Cancelled on | Was per month | Proof | First charge that should not happen |
|---|---|---|---|---|
| Streamly | 2026-02-10 | 15.99 | "Your plan ends Feb 10", email of Feb 3 | 2026-03-10 |

## Audit log

### 2026-02-03
- Read: personal mail and work mail, Nov 5 to Feb 3. Visa statement, Nov to Jan.
- Not read: business card statements.
- Found: 1 not on the list, 1 cancelled but charged.
- Decisions: keep Acme Notes Pro; cancel Streamly ("yes, kill Streamly").
```

The settings block holds names of sources and folders. It never holds a
password, a token, or a full card or account number.
