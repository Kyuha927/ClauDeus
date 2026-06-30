from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PRIORITY_PATH = REPO_ROOT / "context" / "context_priority.json"
DEFAULT_EXPORT_PATH = REPO_ROOT / "context" / "CONTEXT_PRIORITY.md"

DEFAULT_ITEMS = [
    {
        "id": "product-vision",
        "title": "Product Vision",
        "path": "Docs/PRODUCT_VISION.md",
        "priority": 10,
        "enabled": True,
        "max_chars": 5000,
        "reason": "Defines the ClauDeus product direction.",
    },
    {
        "id": "architecture",
        "title": "Architecture",
        "path": "Docs/ARCHITECTURE.md",
        "priority": 20,
        "enabled": True,
        "max_chars": 5000,
        "reason": "Explains component boundaries and contracts.",
    },
    {
        "id": "e2e-checklist",
        "title": "E2E Checklist",
        "path": "Docs/E2E_DEMO_CHECKLIST.md",
        "priority": 30,
        "enabled": True,
        "max_chars": 4500,
        "reason": "Shows the current runnable workflow.",
    },
    {
        "id": "stability-sweep",
        "title": "Stability Sweep",
        "path": "Docs/STABILITY_SWEEP.md",
        "priority": 40,
        "enabled": True,
        "max_chars": 3500,
        "reason": "Lists known fixes and remaining risks.",
    },
]


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def default_payload() -> dict[str, Any]:
    return {
        "version": 1,
        "updated_at": _now(),
        "mode": "lower_priority_number_first",
        "items": DEFAULT_ITEMS,
    }


def load_priority(path: Path = DEFAULT_PRIORITY_PATH) -> dict[str, Any]:
    if not path.is_file():
        return default_payload()
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("context priority root must be an object")
    items = data.get("items")
    if not isinstance(items, list):
        raise ValueError("context priority items must be a list")
    return data


def save_priority(data: dict[str, Any], path: Path = DEFAULT_PRIORITY_PATH) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    data["updated_at"] = _now()
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def sorted_items(data: dict[str, Any]) -> list[dict[str, Any]]:
    items = [item for item in data.get("items", []) if isinstance(item, dict)]
    return sorted(items, key=lambda item: (int(item.get("priority", 9999)), str(item.get("id", ""))))


def init_priority(path: Path = DEFAULT_PRIORITY_PATH, *, force: bool = False) -> Path:
    if path.exists() and not force:
        return path
    return save_priority(default_payload(), path)


def move_item(item_id: str, new_index: int, path: Path = DEFAULT_PRIORITY_PATH) -> Path:
    data = load_priority(path)
    items = sorted_items(data)
    target = None
    rest = []
    for item in items:
        if item.get("id") == item_id:
            target = item
        else:
            rest.append(item)
    if target is None:
        raise KeyError(f"context item not found: {item_id}")
    new_index = max(0, min(int(new_index), len(rest)))
    rest.insert(new_index, target)
    for idx, item in enumerate(rest, start=1):
        item["priority"] = idx * 10
    data["items"] = rest
    return save_priority(data, path)


def set_enabled(item_id: str, enabled: bool, path: Path = DEFAULT_PRIORITY_PATH) -> Path:
    data = load_priority(path)
    found = False
    for item in data.get("items", []):
        if isinstance(item, dict) and item.get("id") == item_id:
            item["enabled"] = bool(enabled)
            found = True
    if not found:
        raise KeyError(f"context item not found: {item_id}")
    return save_priority(data, path)


def add_item(item: dict[str, Any], path: Path = DEFAULT_PRIORITY_PATH) -> Path:
    data = load_priority(path)
    items = [x for x in data.get("items", []) if isinstance(x, dict)]
    item_id = str(item.get("id") or "").strip()
    if not item_id:
        raise ValueError("item.id is required")
    if any(existing.get("id") == item_id for existing in items):
        raise ValueError(f"duplicate context item id: {item_id}")
    item.setdefault("priority", (len(items) + 1) * 10)
    item.setdefault("enabled", True)
    item.setdefault("max_chars", 4000)
    items.append(item)
    data["items"] = items
    return save_priority(data, path)


def export_markdown(path: Path = DEFAULT_PRIORITY_PATH, out: Path = DEFAULT_EXPORT_PATH) -> Path:
    data = load_priority(path)
    lines = [
        "# ClauDeus Context Priority",
        "",
        f"- updated_at: `{data.get('updated_at', '')}`",
        f"- mode: `{data.get('mode', 'lower_priority_number_first')}`",
        "",
        "| Priority | Enabled | ID | Path | Reason |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in sorted_items(data):
        lines.append(
            f"| {item.get('priority', '')} | {item.get('enabled', True)} | `{item.get('id', '')}` | `{item.get('path', '')}` | {item.get('reason', '')} |"
        )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def context_sections(path: Path = DEFAULT_PRIORITY_PATH, *, repo_root: Path = REPO_ROOT) -> list[tuple[str, str]]:
    data = load_priority(path)
    sections: list[tuple[str, str]] = []
    for item in sorted_items(data):
        if not item.get("enabled", True):
            continue
        rel = str(item.get("path") or "").strip()
        if not rel:
            continue
        target = (repo_root / rel).resolve()
        try:
            target.relative_to(repo_root.resolve())
        except ValueError:
            continue
        if not target.is_file():
            continue
        max_chars = int(item.get("max_chars", 4000) or 4000)
        text = target.read_text(encoding="utf-8", errors="replace")
        if len(text) > max_chars:
            text = text[: max_chars - 15].rstrip() + "\n...[trimmed]"
        title = str(item.get("title") or item.get("id") or rel)
        sections.append((title, text))
    return sections
