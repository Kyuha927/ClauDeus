# Release Verification (Strict Policy)

## Verification Policy (Strict)
- **Python**: **3.12.x only** (`doctor --strict`: non-3.12 => ExitCode 1)
- **Windows (PowerShell)**: **REQUIRED**
- **WSL (Ubuntu)**: **OPTIONAL** (space reserved)
- **Completion**: `release-check` green + `git status --porcelain` clean

---

완성 기준: `release-check` green + working tree clean.

## Windows (PowerShell) — Fresh venv
- **Python**: 3.12.10
- **Commands (fixed order)**:
  - `.\dev.ps1 doctor --strict`: PASS (ExitCode 0)
  - `python -m pytest -q`: PASS
  - `.\dev.ps1 smoke`: PASS
  - `.\dev.ps1 release-check`: PASS
- **Evidence**:
  - `release-check` last 20 lines:
    ```
    Policy: Windows=required, WSL=optional, Python=3.12.x(strict)
    
    [Step 3/4] Running Smoke Tests...
    Running smoke tests...
    ✅ Smoke tests passed.

    [Step 4/4] Updating Docs/COMMANDS.md & Checking Git...
    ✅ Docs/COMMANDS.md updated.
    On branch main
    Your branch is ahead of 'origin/main' by 1 commit.

    ✅ Release Check Completed Successfully.
    ```
  - `git status --porcelain`:
    ```
    (empty)
    ```

## WSL (Ubuntu) — Fresh venv
*(Optional/Recommended)*
- **Python**: (e.g. 3.12.x)
- **Commands (fixed order)**:
  - `./dev doctor --strict`: PASS (ExitCode 0)
  - `python -m pytest -q`: PASS
  - `./dev smoke`: PASS
  - `./dev release-check`: PASS
- **Evidence**:
  - `release-check` last 20 lines:
    ```
    <paste here>
    ```
  - `git status --porcelain`:
    ```
    (empty)
    ```

## Notes
- **Strict Policy**: `doctor --strict`는 Python 3.12.x가 아니면 **ExitCode 1**로 실패해야 함.
- **Dirty 허용**: 자동생성 `Docs/COMMANDS.md` 단일 변경만(그 외는 FAIL).
