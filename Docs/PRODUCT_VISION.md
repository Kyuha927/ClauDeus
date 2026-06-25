# ClauDeus Product Vision

## One sentence

ClauDeus is a provider-agnostic AI WorkOS bridge that keeps complex AI work organized across model interfaces, chats, devices, and tools.

## User problem

Ordinary users do not want to manage:

- context windows
- prompt chains
- model routing
- multi-agent handoffs
- GUI-only tools
- CLI-only tools
- scattered chat histories
- mobile-to-desktop file movement

They want to say what they need and keep working.

## ClauDeus answer

ClauDeus hides the machinery:

```text
user intent
→ context pack
→ provider adapter
→ result collection
→ handoff packet
→ title/update/session organization
→ dashboard card
```

## Differentiation

ClauDeus is not only a coding agent. It is the layer that lets many agents, models, and locked interfaces participate in one user-facing workflow.

## Product principles

1. The user should not need to know context engineering.
2. The user should not need to care which model or interface is used.
3. Every handoff should be recoverable from files.
4. Every risky action should be reviewable.
5. The dashboard should show next action before technical detail.

## Initial components

- ClauDeus umbrella repo
- Runtime bridge from `copilot`
- Mobile inbox from `daily`
- Dashboard from `obsidian_dashboard_os`
- Skills pack from `studio-agent`
- Playbook runtime from `agency-runtime`
- Profile pack from `codex-global-config`
- Knowledge feeder from `knowledge-feeder-vault`
