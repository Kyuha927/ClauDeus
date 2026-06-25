# Stability Sweep

## Purpose

This document tracks likely failure points found while turning the ClauDeus portfolio into runnable MVP components.

## Fixed issues

### 1. Handoff packet file collisions

`handoff-plan` previously used second-level timestamps. Multiple runs in the same second could collide. It now uses `time_ns()` stamps.

### 2. Provider readiness was too broad

`provider-check` previously treated platform tools such as `git` and `python` as enough for overall readiness. It now separates provider entrypoints from platform tools.

### 3. Mobile event to dashboard card shape mismatch

The mobile connector now emits wrapped payloads with `cards` and `errors`. Dashboard merge/render tools now accept both plain arrays and wrapped card payloads.

### 4. Playbook validator traceback risk

Invalid JSON or missing files now return `PLAYBOOK_INVALID` with readable errors instead of stack traces.

### 5. CI overreach risk

New smoke workflows run only the stable tests added for the ClauDeus MVP layer. This avoids unrelated legacy tests blocking the new portfolio smoke checks.

### 6. Knowledge candidate smoke gap

A valid `candidate.json` fixture now exists in `knowledge-feeder-vault`, so the E2E checklist can point to a real file instead of a placeholder.

### 7. Bash entrypoint venv mismatch

The Bash `dev` entrypoint now prefers `.venv/bin/python` when available. This prevents CI from installing pytest into a venv and then running release checks with the system interpreter.

## Remaining likely issues

- Some component repos may still contain old environment-specific paths.
- Actual Google Drive live polling still needs OAuth setup and real API implementation.
- Runtime watchers still need to be refactored to use the new handoff packet helper directly.
- Obsidian dashboard is still Markdown/JSON renderer level, not a full plugin.
- GUI relay adapters need explicit user approval and documented setup.

## Next stabilization targets

1. Add cross-repo local runner script.
2. Convert runtime watchers to shared handoff packet helper.
3. Add dry-run provider adapter for Antigravity CLI once local command shape is confirmed.
4. Add dashboard import path from daily mobile card output.
5. Add release checklist for support/application packaging.
