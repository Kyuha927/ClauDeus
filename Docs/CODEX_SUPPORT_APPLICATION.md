# Codex / Open-Source Support Application Package

## Applicant

- GitHub: `Kyuha927`
- Primary project: `Kyuha927/ClauDeus`
- Portfolio theme: provider-agnostic AI WorkOS for ordinary-user AI workflow continuity

## Short application pitch

ClauDeus is a provider-agnostic AI WorkOS bridge that makes complex AI-agent work usable for ordinary users. It hides context engineering, model routing, provider interface differences, chat handoff, mobile capture, skills, and dashboard organization behind a single workflow.

The project was originally designed around a simple observation: ordinary users do not want to manage context windows, prompt chains, model routing, or multi-agent workflows. They want to capture intent, continue work, and see what is next.

ClauDeus addresses this by combining:

- context packs
- handoff packets
- provider adapters
- mobile inbox capture
- dashboard cards
- skills library
- playbook validation
- profile packs
- knowledge feeder packets

## Why Codex support matters

Codex support would help turn ClauDeus from a working multi-repo MVP skeleton into a hardened open-source workflow system for AI-assisted maintainers and ordinary builders.

The biggest need is not just more code generation. It is reliable agent workflow infrastructure:

- safer provider adapter boundaries
- repeatable smoke tests
- reproducible handoff packets
- mobile-to-runtime capture
- readable validation output
- repository-aware context packs
- security-conscious GUI relay rules
- better onboarding for non-expert users

## Project differentiation

Most AI agent systems assume the user will adapt to the provider interface.

ClauDeus takes the opposite approach: the workflow should survive even when the model is available only through an API, CLI, local runtime, IDE integration, GUI, or mobile input surface.

### Core distinction

```text
Not: one more coding agent
But: a workflow continuity layer across many agents, providers, devices, and sessions
```

## Current repository portfolio

| Role | Repository | Current status |
| --- | --- | --- |
| Umbrella / product | `Kyuha927/ClauDeus` | v2 CLI, product docs, contracts, E2E checklist |
| Runtime / bridge | `Kyuha927/copilot` | handoff helper, provider adapter base, dry-run adapter, runtime smoke |
| Mobile inbox | `Kyuha927/daily` | PWA shell, offline queue, mobile inbox dry-run, dashboard card converter |
| Dashboard | `Kyuha927/obsidian_dashboard_os` | card schema, renderer, source merger |
| Skills pack | `Kyuha927/studio-agent` | skill schema, validator, manifest builder |
| Playbook runtime | `Kyuha927/agency-runtime` | playbook validator, path checker, summary helper |
| Profile pack | `Kyuha927/codex-global-config` | profile manifest, diff helper, dry-run installer |
| Skill archive | `Kyuha927/codexskills` | skill inventory, migration rules |
| Knowledge feeder | `Kyuha927/knowledge-feeder-vault` | source candidate schema, promotion rules, positioning packet |

## Recent stabilization work

The MVP layer has been hardened with:

- nanosecond handoff packet IDs to avoid file collisions
- provider readiness checks separated from platform tools
- mobile event to dashboard card conversion
- dashboard tools that accept both plain and wrapped card payloads
- tolerant playbook validation for missing files and invalid JSON
- smoke workflows for component repos
- a valid knowledge candidate fixture
- venv-aware Bash entrypoint for ClauDeus

Reference: `Docs/STABILITY_SWEEP.md`

## End-to-end demo target

The current E2E checklist demonstrates:

```text
ClauDeus context pack
→ handoff packet
→ runtime smoke
→ mobile PWA shell check
→ mobile inbox dry run
→ dashboard card conversion
→ dashboard render
→ skill validation
→ playbook validation
→ profile dry-run
→ skill inventory
→ knowledge candidate validation
```

Reference: `Docs/E2E_DEMO_CHECKLIST.md`

## What I am requesting

I am requesting Codex/OpenAI support for:

1. ChatGPT Pro / Codex access support for continued open-source development.
2. Security and workflow review of ClauDeus provider adapter boundaries.
3. Guidance on safe Codex/GUI/CLI relay patterns.
4. Help hardening the mobile inbox and dashboard workflow.
5. Review of the project as an open-source AI workflow infrastructure candidate.

## How Codex would be used

Codex would be used to:

- refactor runtime watchers into shared handoff helpers
- implement safe dry-run provider adapters
- add tests around queueing, retries, validation, and dashboard rendering
- remove local environment assumptions
- improve smoke workflows
- harden the mobile PWA capture path
- create clean onboarding and examples
- review security boundaries for relays and token handling

## Security posture

ClauDeus is designed to avoid unsafe automation patterns:

- dry-run first
- approval required for risky actions
- raw logs preserved for audit and replay
- GUI relay documented as opt-in and user-approved
- official API/CLI routes preferred when available
- active skills require review before use
- mobile capture stores events locally before network sync

## Why this matters for open source

AI coding agents are becoming powerful, but the surrounding workflow is still fragile. Maintainers need tools that make AI-generated work easier to review, route, summarize, validate, and continue.

ClauDeus focuses on that missing layer: not just generating code, but keeping AI-assisted work organized across sessions, models, interfaces, and devices.

## Suggested application answer

> I am building ClauDeus, a provider-agnostic AI WorkOS bridge for open-source maintainers and ordinary users. It hides context engineering, model routing, chat handoff, mobile capture, and provider interface differences behind a file-backed workflow. The project already spans a multi-repo MVP portfolio with a runtime bridge, mobile PWA inbox, dashboard renderer, skills library, playbook validator, profile pack, and knowledge feeder. Codex support would help harden the system, remove environment-specific assumptions, improve test coverage, and make AI-assisted open-source work safer and more usable.

## Links to include

- Primary repo: `https://github.com/Kyuha927/ClauDeus`
- Main issue: `https://github.com/Kyuha927/ClauDeus/issues/1`
- Product vision: `Docs/PRODUCT_VISION.md`
- Architecture: `Docs/ARCHITECTURE.md`
- Mobile app-like experience: `Docs/MOBILE_APP_EXPERIENCE.md`
- E2E checklist: `Docs/E2E_DEMO_CHECKLIST.md`
- Stability sweep: `Docs/STABILITY_SWEEP.md`

## Immediate next milestones if supported

1. Run and fix the full E2E checklist locally.
2. Refactor runtime watchers to use shared handoff packet helpers.
3. Build the first real API-compatible mobile inbox endpoint.
4. Implement a safe Antigravity/Codex provider adapter.
5. Upgrade the Obsidian dashboard mock into an interactive plugin or hosted dashboard.
6. Add a complete onboarding demo for ordinary users.
7. Perform a security review of GUI relay and token-handling boundaries.
