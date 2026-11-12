---
name: subscription-audit
description: "Find every subscription the owner pays for from their email receipts and card statements, check it against their list, and cancel the ones they name, with proof. Use when they ask what they pay for, what they can cancel, to update their subscription list, or to cancel a subscription."
---

# Subscription audit

The owner is the person in the chat. They own the accounts and the money. You
find the charges, show the list, and cancel only what they name.

Three rules hold in every step:

- **Read before you change.** Steps 1 to 4 change nothing outside the list.
- **Named approval.** Cancel an item only when the owner named it in this
  conversation. A suggestion they did not answer is not approval.
- **Proof or it did not happen.** Say "cancelled" only with the confirmation
  text and the end date in hand.

The owner may ask for one part. "Cancel X" starts at step 5 and still runs
step 6.

## 1. Set up

Ask one question at a time, and only what you cannot find yourself.

1. Where is the subscription list? If there is none, offer to make
   `subscriptions.md` in a folder they choose. Read `references/list-format.md`
   for the format.
2. Which inboxes get receipts? Check which email connections you have and
   name them. Ask about any that are missing.
3. How can you see card and bank charges? In order of preference: a
   connection to the bank, a statement or CSV export they drop in a folder,
   or a signed-in browser they let you use.
4. Whose spending is this? If they have more than one owner, such as personal
   and a business, record it per item and never mix the totals.

Save the answers in the settings block at the top of the list, so the next
run asks nothing. Never store a password, a full card number or an account
number. The last four digits of a card are enough.

The window is from the last audit's date to today. For a first audit, use 90
days, and 13 months for yearly plans.

## 2. Collect the charges

Use every source you were given. Each one misses things the others catch.

- **Email.** Search each inbox for receipts, invoices, renewals, trial
  endings, price changes and cancel confirmations. Read the message body. A
  subject line is not evidence.
- **Statements.** Read the full transaction list. Charges with no receipt
  email show up only here.
- **App stores.** Plans billed by Apple or Google appear in the store's
  subscription page and on its receipts, not on the merchant's site.

Keep a coverage note: which accounts and dates you read, and which you could
not reach. If you had no statements, say that the audit covers email only.

## 3. Match charges to the list

A charge is recurring when the same merchant repeats on a cycle or a receipt
names a renewal date. Leave out one-time buys, credits and top-ups.

Put each recurring charge and each active list item in one group:

| Group | Meaning |
|---|---|
| Matches | Amount, card and date agree. Roll the renewal date forward. |
| Not on the list | A recurring charge the list does not have. |
| List is wrong | Amount, card, owner or renewal date differs from the charges. |
| Cancelled but charged | Marked cancelled, and a charge came after that date. Show these first. |
| Active but not charged | No charge for two cycles. Unknown, not cancelled. |
| Looks wrong | Repeated charges from a merchant the owner may not know. Report it as possible fraud and touch nothing. |

Watch for these:

- No email does not mean cancelled. Open the account or the statement.
- The name on a statement is often not the product's name. Match by amount
  and date, then confirm with a receipt.
- A marked-cancelled item is a claim. A charge after its date beats it.

Fix clear cases in the list and write the source next to the change. For an
unclear case, write nothing and ask.

## 4. Show the list and get decisions

Show one table in chat: name, cost per month, owner, next charge date, and
your call (keep, cancel or ask). Sort by next charge date. Give the monthly
and yearly total per owner, and say which source each total came from.

- Suggest a cancel only with a reason you can show: no use, two tools for one
  job, or a tool they already replaced.
- For each suggestion, say what they lose and what must happen first, such as
  exporting data, moving a mailbox, or telling people who use it.
- Do not suggest an item again after the owner said keep, unless its price or
  their use changed. Record each keep with its date.
- The owner's word wins over your evidence on what to keep and what belongs
  on the list.
- "I already cancelled that" is a claim to check, not approval to cancel.
  Look at the account or the statement, read only. If it still renews, tell
  the owner and ask before you change it.

Then ask one question: "Which of these do you want me to cancel?"

## 5. Cancel what they named

Read `references/cancelling.md` and follow it for each named item. In short:
look at the live account first, find where the plan is billed, check what
depends on it, then make the smallest change that stops the charge, and copy
the proof.

If a step needs the owner's phone, a code, or a site that blocks you, stop.
Give them the exact clicks and ask for a screenshot of the result. Check the
screenshot before you record anything.

## 6. Record and report

- On the list: status cancelled, the date access ends, the owner's approval
  in their words, and the proof.
- In the audit log the format file describes: coverage, the groups from
  step 3, each decision, each cancel with proof, and the date of the first
  charge that should not happen.
- Start the next audit by checking those dates in the statements. A plan that
  charges after its cancel goes back to the owner the same day.

Report in a few lines: what was cancelled and its proof, the new monthly
total and its source, what you could not check, and what the owner must do.
