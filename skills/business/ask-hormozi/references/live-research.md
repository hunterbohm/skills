# Live Primary-Source Research

Use this branch only when `SKILL.md` routes here. The shipped evidence snapshot remains the default.

## Define the research target

Write down the smallest claim that would change the answer, plus any date range. Search for that claim rather than for broad "Hormozi advice."

Examples:

- What has Hormozi said since a named date about AI agents?
- Did he use this exact wording?
- Has his current 30-day payback standard changed?

## Use the best available capability

Use whatever public search, browser, transcript, or research tools the current agent already has. This skill has no required tool dependency.

If public research is unavailable, state that the live check could not run. Continue only with claims supported by the shipped snapshot.

## Source hierarchy

Prefer sources in this order:

1. Alex Hormozi or Acquisition.com official video, podcast, site, or social account.
2. A full guest appearance published by the original host.
3. A primary-source page that embeds or links the original recording.
4. Secondary summaries only to discover a primary source, never to support exact attribution.

Treat search snippets, generated summaries, quote graphics, reposts, and transcript aggregators as locators. They are not proof of exact wording by themselves.

## Research loop

1. Find the strongest primary candidate for the claim and date range.
2. Record its title, direct URL, publisher or channel, and publication date when available.
3. Retrieve the public transcript, captions, or primary page text.
4. Locate the relevant passage in context. Check whether later words qualify or reverse the apparent claim.
5. Assign one evidence state:
   - **Verified exact excerpt:** contiguous wording confirmed against the primary recording or transcript.
   - **Primary-source paraphrase:** the source supports the idea, but exact wording is unavailable or unnecessary.
   - **Unsupported:** no primary source found after a focused search.
6. Compare the live finding with the shipped framework. When they differ, name the era or date and prefer the newer primary statement for "current" questions.
7. Stop when one strong source answers the load-bearing claim. Add another only to resolve a conflict or genuinely separate claim.

## Attribution rules

- Quote no more than 20 words from one public source and preserve the direct link.
- Add a timestamp when the source supports stable timestamped links; never invent one.
- Paraphrase when captions are auto-generated, wording is uncertain, or an exact quote is unnecessary.
- Label an inference as an inference.
- Never repair a broken URL or fill a transcript gap from memory.
- Do not reproduce or attach a full transcript.

## Answer contract

Keep the normal Ask Hormozi answer shape. Add this only when live research ran:

```text
Source basis: Live primary-source research checked YYYY-MM-DD.
- Source title — publisher, publication date — direct URL
```

If the search fails, say:

```text
I did not find primary public support for that exact claim. The following is a framework distillation, not a Hormozi quotation.
```

The branch is complete when every material live claim is traceable to a primary source and evidence state, or explicitly marked unsupported.
