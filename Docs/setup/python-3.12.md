# Python 3.12.x Setup (Windows PowerShell / WSL Ubuntu)

목표: 로컬에서 `release-check`가 green.

---

## Windows (PowerShell)

### 1) Python 3.12 설치
```powershell
winget install Python.Python.3.12
py -3.12 --version
```

성공 기준: `py -3.12 --version`가 `Python 3.12.x` 출력.

이미 설치돼 있으면 `winget install`은 스킵하고 버전 확인만 진행해도 됨.

### 2) .venv 재생성 + 활성화(실행 정책 예외 포함)
```powershell
if (Test-Path .venv) { Remove-Item -Recurse -Force .venv }
py -3.12 -m venv .venv

# 필요 시(우선: 현재 세션만)
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process

.\.venv\Scripts\Activate.ps1

# 여전히 차단되면(선택)
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

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

성공 기준: 에러 없이 종료(ExitCode 0).

### 4) 최종 검증(순서 고정)
```powershell
.\dev.ps1 doctor --strict
python -m pytest -q
.\dev.ps1 smoke
.\dev.ps1 release-check
git status --porcelain
```

성공 기준: 앞 4개 명령 성공 + `git status --porcelain` 출력 비어 있음.

### 5) release-check 후 dirty 처리(자동생성 문서 단일 변경일 때만)
```powershell
git diff --name-only
# 출력이 Docs/COMMANDS.md 한 줄일 때만:
git add Docs/COMMANDS.md
git commit -m "chore: refresh generated command docs"
```

성공 기준: 커밋 후 워킹트리 clean.
