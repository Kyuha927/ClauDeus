from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import cladeus_core


def test_handoff_packet_serializes_json():
    packet = cladeus_core.HandoffPacket(
        source="user",
        target="executor",
        project_slug="demo",
        session_id="s1",
        turn_id="t1",
        summary="hello",
        next_actions=["a", "b"],
        title_hint="demo title",
        created_at="2026-01-01T00:00:00",
    )
    text = packet.to_json()
    assert '"project_slug": "demo"' in text
    assert '"next_actions"' in text


def test_portfolio_components_have_roles():
    roles = {item["role"] for item in cladeus_core.PORTFOLIO_COMPONENTS}
    assert "runtime" in roles
    assert "mobile_inbox" in roles
    assert "dashboard" in roles
    assert "skills" in roles


def test_slug_fallback():
    assert cladeus_core._slug("") == "task"
    assert cladeus_core._slug("hello world") == "hello-world"


def test_stamp_changes_between_calls():
    first = cladeus_core._stamp()
    second = cladeus_core._stamp()
    assert first != second
    assert first.isdigit()
    assert second.isdigit()


def test_provider_check_reports_provider_and_platform_sections():
    result = cladeus_core.provider_check()
    assert "providers" in result
    assert "platform_tools" in result
    assert "codex_cli" in result["providers"]
