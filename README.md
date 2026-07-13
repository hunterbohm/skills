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

## Why these skills exist

Agents are powerful, but they often lose the shape of a project, flatten specialist judgment into generic advice, or invent a process that changes from one session to the next.

These skills turn working methods into reusable operating loops:

- read the real sources before giving advice;
- adapt to the project instead of imposing a rigid template;
- keep evidence, uncertainty, and compatibility visible;
- produce a useful decision or next action, not just more information.

## Catalog

Skills are grouped by the kind of work they help with—not by programming language or agent vendor.

See the complete [catalog, compatibility notes, and direct install commands](docs/catalog.md).

## Repository layout

```text
skills/
  business/
  project-management/
docs/
scripts/
```

Every directory containing a `SKILL.md` is an independently installable skill package. Repository automation recursively discovers and validates them, so adding a category does not require flattening everything into the root.

## License

Hunter Bohm's original work is available under the [MIT License](LICENSE). Third-party names and source material remain with their respective owners; see the [third-party notices](docs/third-party-notices.md).
