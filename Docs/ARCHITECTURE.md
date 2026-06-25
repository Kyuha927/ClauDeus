# ClauDeus Architecture

## System map

```text
Mobile / Web / Desktop input
  ↓
Inbox
  ↓
Context Pack Builder
  ↓
Provider Router
  ↓
Provider Adapters
  ↓
Result Collector
  ↓
Handoff Packet
  ↓
Dashboard / Memory / Skills / Playbooks
```

## Component repos

| Component | Repo | Responsibility |
| --- | --- | --- |
| Umbrella | `Kyuha927/ClauDeus` | product, contracts, CLI shell |
| Runtime | `Kyuha927/copilot` | bridge hub, handoff, session sync |
| Mobile Inbox | `Kyuha927/daily` | smartphone upload intake |
| Dashboard | `Kyuha927/obsidian_dashboard_os` | ordinary-user work surface |
| Skills | `Kyuha927/studio-agent` | skill pack and memory rules |
| Playbooks | `Kyuha927/agency-runtime` | success/failure contracts |
| Profiles | `Kyuha927/codex-global-config` | environment instruction packs |
| Knowledge | `Kyuha927/knowledge-feeder-vault` | reviewed source packets |

## Contracts to stabilize first

1. Context Pack
2. Handoff Packet
3. Provider Adapter
4. Mobile Event
5. Skill Candidate
6. Playbook JSON
7. Dashboard Card

## First end-to-end demo

```text
./dev context-pack "continue mobile inbox connector"
./dev handoff-plan "send to executor"
python3 connectors/google_drive/google_drive_poll_ingest.py --dry-run --once
open dashboard mock
```

## Safety posture

- dry-run first
- human approval for risky changes
- raw logs preserved
- skill changes proposed before activation
- mobile connector does not require desktop sync
