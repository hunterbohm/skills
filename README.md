<p>
  <a href="https://skills.sh/hunterbohm/skills">
    <img alt="Hunter Bohm's agent skills" src="https://skills.sh/b/hunterbohm/skills">
  </a>
</p>

# Skills for running real work

Practical agent skills for projects, decisions, business, research, and communication.

These are workflows I use myself, packaged so an agent can apply them consistently instead of making me explain the same process in every task. They are small, adaptable, and explicit about which agent environments they support.

## Quickstart

Preview the available skills:

```bash
npx skills@latest add hunterbohm/skills --list
```

Install from the interactive picker:

```bash
npx skills@latest add hunterbohm/skills
```

Or install one skill directly using the command in the [skill catalog](docs/catalog.md). Host-specific skills include an explicit agent target so they do not leak into incompatible runtimes.

## Catalog

Skills are grouped by the kind of work they help with, not by programming language or agent vendor.

See the complete [catalog, compatibility notes, and direct install commands](docs/catalog.md).

The design behind the operations skills is written up for business owners in [the connected-agent field guide](docs/connected-agent-field-guide.md). Design decisions live in [docs/adr](docs/adr), and the shared vocabulary in [CONTEXT.md](CONTEXT.md).

## Repository layout

```text
skills/
  business/
  project-management/
docs/
scripts/
```

Every directory containing a `SKILL.md` is an independently installable skill package. Repository automation recursively discovers and validates them, so adding a category does not require flattening everything into the root.

## Editing and publishing

Skills are edited in place under `skills/`. `scripts/publish.sh "what changed"` validates, regenerates the catalog, and publishes through a self-merging pull request. See [AGENTS.md](AGENTS.md).

## License

Hunter Bohm's original work is available under the [MIT License](LICENSE). Third-party names and source material remain with their respective owners; see the [third-party notices](docs/third-party-notices.md).
