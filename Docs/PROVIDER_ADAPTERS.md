# Provider Adapters

## Purpose

Provider adapters let ClauDeus use AI systems without forcing the user to care whether the model lives behind an API, CLI, local runtime, IDE, or user-approved GUI relay.

## Adapter interface

Every adapter should expose this conceptual contract:

```python
class ProviderAdapter:
    def health_check(self) -> dict: ...
    def prepare(self, task: dict) -> dict: ...
    def send(self, prompt: str) -> dict: ...
    def collect(self, handle: dict) -> dict: ...
    def normalize(self, raw_answer: str) -> dict: ...
```

## Adapter types

| Type | Use case | Default policy |
| --- | --- | --- |
| API | Official hosted APIs | preferred when available |
| CLI | Codex, Antigravity CLI, local commands | preferred for developer workflows |
| Local | local model server or runtime | useful for privacy and cost control |
| IDE | VS Code / Antigravity-contained sessions | allowed when user owns the workspace |
| GUI relay | browser/app handoff | fallback, opt-in, user-approved only |

## Normalized result

```json
{
  "provider": "string",
  "model": "string",
  "status": "ok|blocked|failed",
  "answer": "string",
  "raw_log_path": "string",
  "checks": [],
  "cost_hint": null,
  "latency_ms": null
}
```

## Guardrails

- Prefer official APIs and CLIs.
- GUI relay is a fallback adapter, not a bypass claim.
- Preserve raw logs.
- Never run destructive actions without approval.
- Normalize output into a handoff packet before passing it to another model.
