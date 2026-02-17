# 🚨 Emergency Response Runbook (One-Pager)

> **Purpose**: Immediate actions for post-release issues.
> **Scope**: Production/Release breakage.

## ⚡ 60s Triage
1) **Check policy + python**: `.\dev.ps1 doctor --strict`
2) **Check dirty**: `git status --porcelain`
3) **Get logs**: `.\dev.ps1 diag`
4) **Repair env**: `.\dev.ps1 bootstrap`
5) **Re-run gate**: `.\dev.ps1 release-check`
6) **Rollback**: `git checkout v0.1.0`

## 1. Diagnose (Fail-Fast)
Run these commands to identify the failure layer.

| Command | Check For | Action if Failed |
| :--- | :--- | :--- |
| `.\dev.ps1 doctor --strict` | **ExitCode 1** (Python != 3.12.x) | See **[Setup Guide](../setup/python-3.12.md)** |
| `.\dev.ps1 diag` | Log location (Zip bundle) | Attach to Issue/Ticket |
| `git status` | Clean Working Tree | `git stash` or `git reset --hard` |

**Quick Fixes**:
- **Environment Corrupted**: `rm -rf .venv` → `.\dev.ps1 bootstrap`
- **Dependency Issues**: `.\dev.ps1 bootstrap` (forces pip upgrade)

## 2. Rollback (Immediate Mitigation)
If `release-check` fails or functionality is broken on `main`.

**Step 1: Check Tags**
```powershell
git tag -n   # List versions
```

**Step 2: Revert to Last Stable (e.g., v0.1.0)**
```powershell
git checkout v0.1.0
.\dev.ps1 bootstrap
.\dev.ps1 release-check
```
*(If green, deploy/use this version)*

## 3. Deep Dive (Evidence)
When reporting bugs, include **Validation Evidence**:
1. Run: `.\dev.ps1 release-check`
2. Copy **Last 20 lines** of output.
3. Copy `git status --porcelain` output.
4. Update `Docs/RELEASE_VERIFICATION.md` with this data if establishing a new baseline.

## 4. Policy (Strict)
- **NEVER** bypass `doctor --strict` for releases.
- **NEVER** commit if `release-check` fails.
- **ALWAYS** check `Docs/COMMANDS.md` matches `dev_cli.py`.

---
**Contacts**: Maintainer (@Kyuha927)
