# ClauDeus

ClauDeus is a provider-agnostic AI WorkOS bridge.

It keeps complex AI work organized across ChatGPT, Codex, Antigravity, CLI tools, GUI-only tools, local runtimes, mobile uploads, skills, project memory, and dashboard surfaces.

The goal is simple: ordinary users should not need to understand context windows, model routing, multi-agent orchestration, or handoff mechanics.

## What ClauDeus does

```text
user intent
→ context pack
→ provider adapter
→ result collection
→ handoff packet
→ dashboard card
→ next action
```

## Core ideas

- **Context packs**: compact file-backed task state instead of fragile long chats.
- **Provider adapters**: API, CLI, IDE, local, and user-approved GUI relay paths behind one workflow.
- **Handoff packets**: fresh-session summaries with next actions and title hints.
- **Mobile inbox**: smartphone-only upload paths that can feed ClauDeus without desktop sync.
- **Skills library**: short reviewed procedures that can be injected into context packs.
- **Playbook contracts**: explicit done/blocked conditions for delegated work.
- **Dashboard surface**: normal users see status, summary, and next action first.

## Portfolio map

| Component | Repo | Role |
| --- | --- | --- |
| Umbrella | `Kyuha927/ClauDeus` | product, contracts, CLI shell |
| Runtime | `Kyuha927/copilot` | bridge hub, handoff packets, provider adapters |
| Mobile Inbox | `Kyuha927/daily` | smartphone upload intake |
| Dashboard | `Kyuha927/obsidian_dashboard_os` | user-facing work surface |
| Skills | `Kyuha927/studio-agent` | skills and memory pack |
| Playbooks | `Kyuha927/agency-runtime` | success/failure contracts |
| Profiles | `Kyuha927/codex-global-config` | environment instruction packs |
| Skill Archive | `Kyuha927/codexskills` | raw skill import source |
| Knowledge | `Kyuha927/knowledge-feeder-vault` | reviewed source packets |

## Quickstart

### WSL / Linux

```bash
./dev bootstrap
./dev context-pack "continue the mobile inbox connector"
./dev handoff-plan "prepare executor handoff"
./dev provider-check
./dev mobile-inbox-check
./dev portfolio-status
```

### Windows PowerShell

```powershell
.\dev.ps1 bootstrap
.\dev.ps1 context-pack "continue the mobile inbox connector"
.\dev.ps1 handoff-plan "prepare executor handoff"
.\dev.ps1 provider-check
```

## Legacy dev checks

```bash
./dev doctor
./dev smoke
./dev dev-check
./dev release-check
```

## Important docs

- [Product Vision](Docs/PRODUCT_VISION.md)
- [Architecture](Docs/ARCHITECTURE.md)
- [Provider Adapters](Docs/PROVIDER_ADAPTERS.md)
- [Context Handoff Design](Docs/CONTEXT_HANDOFF_DESIGN.md)
- [Mobile Inbox Connector](Docs/MOBILE_INBOX_CONNECTOR.md)
- [Codex Approval Gate](Docs/CODEX_APPROVAL_GATE.md)

## Safety posture

- Prefer official API/CLI routes when available.
- GUI relay is opt-in and user-approved.
- Default to dry-run or propose-only for risky operations.
- Preserve raw logs for audit and replay.
- Active skills require review before use.

## Current status

ClauDeus v2 is being assembled from multiple existing repositories into a coherent AI WorkOS portfolio. The first target is a working end-to-end demo:

```text
mobile or web input
→ context pack
→ provider adapter
→ handoff packet
→ dashboard card
```
