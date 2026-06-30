# Context Priority Control

## Goal

Let the user reorder context priority with a simple drag UI, then let agents reflect that order in the next context pack or runtime read.

## Current implementation

### ClauDeus core

- Priority engine: `tools/context_priority.py`
- Default runtime file: `context/context_priority.json`
- Example committed order file: `context/order.json`
- Context pack integration: `tools/cladeus_core.py`

When `./dev context-pack` runs, ClauDeus reads the context priority file and inserts enabled items in priority order before fallback docs.

### CLI

```bash
./dev context-priority init
./dev context-priority list
./dev context-priority move stability-sweep 0
./dev context-priority disable architecture
./dev context-priority enable architecture
./dev context-priority export
./dev context-pack "continue current work"
```

### Drag UI

Dashboard-side prototype:

```text
Kyuha927/obsidian_dashboard_os/views/context_priority_editor.html
Kyuha927/obsidian_dashboard_os/views/context_priority_editor.js
```

The editor lets users drag items, toggle enabled state, export JSON, and copy it into the ClauDeus context priority file.

## Realtime model

The first stable version uses file-backed near-realtime behavior:

```text
drag reorder
→ export/write context priority JSON
→ context pack rebuild or runtime poll
→ agent reads new order
```

For true live mode, the runtime should watch the priority file and rebuild the active context pack when the file timestamp changes.

## Why file-backed first

- easy to inspect
- works with Git
- survives restarts
- avoids hidden state
- agents can read it without custom UI integration

## Next implementation step

Add a tiny local endpoint or file watcher:

```text
POST /context-priority
GET /context-priority
watch context/context_priority.json
on change: rebuild CONTEXT_PACK.md
```

This will let the drag UI write directly instead of copy/export.

## Safety rules

- Do not allow paths outside the repository root.
- Disabled items stay in the file but are skipped.
- Missing files are skipped, not fatal.
- Priority edits should be auditable through Git or exported snapshots.
