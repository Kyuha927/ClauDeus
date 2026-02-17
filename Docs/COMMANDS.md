# ClauDeus CLI Commands

| Command | Description |
| :--- | :--- |
| `doctor` | Check environment health (Python 3.12, paths, etc) |
| `bootstrap` | **Onboarding**: Check Py3.12 + Ensure venv + Install deps |
| `dev-check` | **Fast Loop**: doctor(msg) + pytest + smoke (dirty allowed) |
| `release-check` | **Strict Gate**: Py3.12 strict + clean tree + evidence |
| `install` | (Legacy) Install core dependencies |
| `start` | Run the native watcher for auto-AI processing |
| `commands` | Show this list (use `--write` to update Docs/COMMANDS.md) |

## Check Policy
- `dev-check`: fast developer loop (non-strict, dirty allowed)
- `release-check`: strict release gate (Python 3.12.x only, clean working tree required)
