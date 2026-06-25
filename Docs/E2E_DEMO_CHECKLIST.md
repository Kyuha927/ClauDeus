# E2E Demo Checklist

## Goal

Prove that ClauDeus can connect the portfolio into one ordinary-user workflow.

## Demo path

```text
1. ClauDeus context pack
2. ClauDeus handoff packet
3. Runtime smoke in copilot
4. Mobile PWA shell check in daily
5. Mobile inbox dry run in daily
6. Mobile event to dashboard card conversion
7. Dashboard source merge and render
8. Skill validation and manifest generation
9. Playbook validation and summary
10. Profile dry-run install
11. Skill archive inventory
12. Knowledge candidate validation
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

# daily mobile inbox and PWA
python3 -m pytest -q tests/test_mobile_pwa_files.py
bash connectors/google_drive/run_google_drive_poll_ingest.sh --dry-run --once
python3 connectors/google_drive/mobile_event_to_dashboard_card.py

# dashboard
python3 tools/merge_dashboard_sources.py demo_data/dashboard_cards.json --out demo_data/dashboard_cards.merged.json
python3 tools/render_dashboard_cards.py --in demo_data/dashboard_cards.merged.json

# skills
python3 tools/validate_skill.py skills/context-memory
python3 tools/build_skill_manifest.py

# playbooks
python3 tools/validate_playbook.py playbooks/pm-agent.json
python3 tools/check_playbook_files.py playbooks/pm-agent.json
python3 tools/playbook_summary.py playbooks/pm-agent.json

# profile pack
bash scripts/install_profile.sh vm --dry-run

# skill archive
python3 tools/build_skill_inventory.py

# knowledge feeder
python3 tools/validate_source_candidate.py packets/ai-workos-positioning/candidate.json
```

## Success markers

```text
CONTEXT_PACK_READY
HANDOFF_PACKET_READY
RUNTIME_SMOKE_OK
MOBILE_PWA_READY
MOBILE_INBOX_CHECK_OK
MOBILE_DASHBOARD_CARDS_READY
DASHBOARD_SOURCES_MERGED
DASHBOARD_RENDER_OK
SKILL_VALID
SKILLS_MANIFEST_READY
PLAYBOOK_VALID
PLAYBOOK_SUMMARY_READY
PROFILE_DRY_RUN_OK
SKILL_INVENTORY_READY
SOURCE_CANDIDATE_VALID
```

## Known follow-up

Run each command inside its own repository root. The ClauDeus umbrella repo documents the sequence, but the component commands belong to their component repos.
