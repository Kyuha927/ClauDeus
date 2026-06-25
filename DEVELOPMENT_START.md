# ClauDeus Development Start

## One-line product position

ClauDeus is a provider-agnostic AI WorkOS bridge: it hides context engineering, model routing, chat handoff, and session organization so ordinary users can keep complex AI work moving across GUI-only, CLI-only, API-based, local, Codex, ChatGPT, Antigravity, and other model interfaces.

## Why this repo matters

This repository should become the public umbrella and product narrative for the whole system. The original ClauDeus idea is stronger than a simple multi-model wrapper: it is an AI-work continuity layer that makes multi-agent/context-engineering workflows usable without exposing that complexity to normal users.

## Immediate development goal

Turn ClauDeus into the canonical umbrella repo that explains and coordinates these components:

- `copilot` as runtime and bridge hub
- `daily` as mobile inbox / smartphone upload automation
- `obsidian_dashboard_os` as user-facing dashboard surface
- `studio-agent` as skills and memory pack
- `agency-runtime` as playbook and success/failure contract engine
- `codex-global-config` as profile/instruction distribution mirror

## Milestone 0: support-ready repo packaging

1. Add English-first `README.md` product positioning.
2. Add `Docs/PRODUCT_VISION.md`.
3. Add `Docs/ARCHITECTURE.md`.
4. Add `Docs/PROVIDER_ADAPTERS.md`.
5. Add `Docs/CONTEXT_HANDOFF_DESIGN.md`.
6. Add `Docs/MOBILE_INBOX_CONNECTOR.md`.
7. Add `Docs/SKILL_EVOLUTION_DESIGN.md`.
8. Add `examples/20-command-handoff-demo.md`.
9. Add `examples/provider-adapter-demo.md`.
10. Add `ROADMAP.md`, `SECURITY.md`, `LICENSE` if missing.

## Milestone 1: ClauDeus v2 CLI shell

Add these commands to `./dev`:

```bash
./dev context-pack
./dev handoff-plan
./dev skill-suggest
./dev skill-approve <candidate>
./dev provider-check
./dev mobile-inbox-check
./dev portfolio-status
```

## Milestone 2: integration contracts

Define stable contracts for:

- Provider Adapter
- GUI Relay Adapter
- CLI Adapter
- Context Pack
- Handoff Packet
- Skill Candidate
- Playbook Runtime Check
- Mobile Inbox Event

## Milestone 3: demos

Build one end-to-end demo:

```text
mobile upload or web command
→ ClauDeus inbox
→ context pack
→ provider adapter
→ result collector
→ handoff summary
→ dashboard update
```

## Development guardrails

- Do not claim to support every provider through unofficial bypass.
- Use “user-approved GUI relay adapter” language for GUI paths.
- Prefer official API/CLI adapters when available.
- Keep all destructive actions behind approval gates.
- Default to propose-only/dry-run before full-auto execution.

## First implementation ticket

Create `Docs/PRODUCT_VISION.md` and rewrite `README.md` around this positioning:

> ClauDeus makes AI work portable across model interfaces. It automatically organizes prompts, results, handoff state, skills, and project context so users do not need to manage context windows, model routing, or multi-agent workflows manually.
