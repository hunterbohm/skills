# Security policy

Agent skills run with the permissions of the agent that installs them. Treat a
skill change with the same care as an executable dependency.

## Supported version

Only the latest revision on `main` is supported. The validation workflow tests
both a pinned installer baseline and the current `skills` CLI before changes
land.

## Reporting a vulnerability

Use [GitHub private vulnerability reporting](https://github.com/hunterbohm/skills/security/advisories/new).
Do not place secrets, exploit details, or private user data in a public issue.

Include the affected skill, the unsafe behavior, reproduction steps, and any
suggested mitigation. Reports will be evaluated against the current package on
`main`.
