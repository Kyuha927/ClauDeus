# Provider Adapter Demo

## Goal

Show that ClauDeus can select a route without exposing provider complexity to the user.

## Demo command

```bash
./dev provider-check
```

## Example normalized result

```json
{
  "provider": "codex_cli",
  "status": "ok",
  "answer": "...",
  "raw_log_path": ".logs/provider/codex.log",
  "checks": []
}
```

## User-facing rule

The user should see the work result and next action, not the provider plumbing.
