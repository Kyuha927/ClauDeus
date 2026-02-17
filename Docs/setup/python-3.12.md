# Python 3.12.x Setup (Windows PowerShell / WSL Ubuntu)

목표: 로컬에서 `./dev release-check`(WSL) / `.\dev.ps1 release-check`(Windows)가 green.

---

## Windows (PowerShell)

### 1) Python 3.12 설치
```powershell
winget install Python.Python.3.12
py -3.12 --version
```

성공 기준: `py -3.12 --version`이 `Python 3.12.x` 출력.

### 2) .venv 재생성 + 활성화
```powershell
if (Test-Path .venv) { Remove-Item -Recurse -Force .venv }
py -3.12 -m venv .venv

# 활성화 정책 설정 (필요 시)
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process

.\.venv\Scripts\Activate.ps1
python --version
python -m pip --version
```

성공 기준:
- `python --version`은 `3.12.x`
- `python -m pip --version` 경로에 `.venv` 포함

### 3) 의존성 설치
```powershell
python -m pip install --upgrade pip
.\dev.ps1 install
```

성공 기준: 에러 없이 종료 (ExitCode 0).

### 4) 최종 검증 (순서 고정)
```powershell
.\dev.ps1 doctor --strict
python -m pytest -q
.\dev.ps1 smoke
.\dev.ps1 release-check
git status --porcelain
```

성공 기준:
- 앞 4개 명령 성공
- `git status --porcelain` 출력 비어 있음

### 5) release-check 후 dirty일 때
자동생성 문서만 바뀐 경우에만 커밋합니다.
```powershell
git diff --name-only
# 변경이 Docs/COMMANDS.md 단일 파일일 때만:
git add Docs/COMMANDS.md
git commit -m "chore: refresh generated command docs"
```

성공 기준: 워킹트리 clean.
