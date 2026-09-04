# Skills repository

This repository is the source of truth for Hunter Bohm's public skills. Edit
skills here. Nothing upstream generates them.

## Edit a skill

- Package: `skills/<category>/<name>/` — `SKILL.md`, `references/`, `evals/`,
  `LICENSE`. Every package installs on its own, so it must not point outside
  its own directory.
- `ops-audit/evals/proof-checklist.md` is that skill's proof standard: one real
  run on the owner's own operations. Nothing runs that file automatically.
- No private names, machine paths, or credentials. Users choose their own
  paths; the skill asks once.
- `CONTEXT.md` is the glossary for `ops-audit`. `docs/adr/` records
  design decisions. `docs/` also holds public reads that are not part of any
  package.

## Publish

```bash
scripts/publish.sh "what changed"
```

It regenerates the catalog, validates, commits to a `publish/*` branch, opens
a pull request, waits for GitHub's `validate` check, and fast-forwards `main`
after the merge (`main` is branch-protected). The `skills` CLI serves the new
version at once.

## Checks

`npm run validate` runs every check. `publish.sh` runs it before each push.
