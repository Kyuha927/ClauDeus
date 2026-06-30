from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import context_priority


def test_default_items_exist():
    data = context_priority.default_payload()
    assert data["version"] == 1
    assert len(data["items"]) >= 3


def test_move_changes_first_item(tmp_path):
    path = tmp_path / "order.json"
    context_priority.init_priority(path)
    context_priority.move_item("stability-sweep", 0, path)
    data = context_priority.load_priority(path)
    items = context_priority.sorted_items(data)
    assert items[0]["id"] == "stability-sweep"


def test_disable_item(tmp_path):
    path = tmp_path / "order.json"
    context_priority.init_priority(path)
    context_priority.set_enabled("architecture", False, path)
    data = context_priority.load_priority(path)
    item = next(x for x in data["items"] if x["id"] == "architecture")
    assert item["enabled"] is False
