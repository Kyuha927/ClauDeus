# E2E Demo Checklist

## Goal

Prove that ClauDeus can connect the portfolio into one ordinary-user workflow.

## Demo path

```text
1. ClauDeus context pack
2. ClauDeus handoff packet
3. Runtime smoke in copilot
4. Mobile inbox dry run in daily
5. Dashboard render in obsidian_dashboard_os
6. Skill validation in studio-agent
7. Playbook validation in agency-runtime
8. Profile dry-run in codex-global-config
9. Skill inventory in codexskills
10. Knowledge promotion rules in knowledge-feeder-vault
```

## Commands

```bash
# ClauDeus
./dev context-pack "continue ClauDeus v2"
./dev handoff-plan "prepare next step"
./dev provider-check
./dev portfolio-status

# copilot runtime
python3 scripts/runtime_smoke.py

# daily mobile inbox
bash connectors/google_drive/run_google_drive_poll_ingest.sh --dry-run --once
python3 connectors/google_drive/mobile_event_to_dashboard_card.py

# dashboard
python3 tools/render_dashboard_cards.py
python3 tools/merge_dashboard_sources.py

# skills
python3 tools/validate_skill.py skills/context-memory

# playbooks
python3 tools/validate_playbook.py playbooks/pm-agent.json
python3 tools/playbook_summary.py playbooks/pm-agent.json

# profile pack
bash scripts/install_profile.sh vm --dry-run

# skill archive
python3 tools/build_skill_inventory.py
```

## Success markers

```text
CONTEXT_PACK_READY
HANDOFF_PACKET_READY
RUNTIME_SMOKE_OK
MOBILE_INBOX_CHECK_OK
MOBILE_DASHBOARD_CARDS_READY
DASHBOARD_RENDER_OK
DASHBOARD_SOURCES_MERGED
SKILL_VALID
PLAYBOOK_VALID
PLAYBOOK_SUMMARY_READY
PROFILE_DRY_RUN_OK
SKILL_INVENTORY_READY
```
