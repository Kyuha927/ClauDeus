# ClauDeus

ClauDeus는 여러 AI 에이전트를 충돌 없이 병렬 운영하고, 결과를 바로 적용/검증 가능한 “패치 패키지” 형태로 강제하는 개발 운영 레일입니다.
코드/문서 변경은 단일 진입점(dev)과 테스트/로그 번들로 검증합니다.

### 작동 방식 (핵심)
- **단일 진입점**: 모든 작업은 `dev` 명령으로 실행합니다.
- **패치 패키지 규격**: 에이전트 출력은 항상 `PATCH LIST` / `READY-TO-PASTE CONTENT` / `CHECKS` 3섹션으로만 받습니다.
- **파일 스코프 분리 (충돌 방지)**: `Docs`, `README`, `ADR`을 서로 다른 에이전트가 각각 담당합니다.
- **검증 루프**: `doctor` → `smoke` → `pytest`(또는 `release-check`) 순서로 깨짐을 빠르게 잡습니다.
- **실패 표준 포맷**: 실패 시 `Cause` / `Next` / `Log`로 원인·다음액션·로그 경로를 고정 출력합니다.

## 🚀 Quickstart (SSOT, Python 3.12.x Strict)
### Windows (PowerShell)
```powershell
.\dev.ps1 bootstrap
.\dev.ps1 release-check
```

### WSL (Ubuntu)
```bash
./dev bootstrap
./dev release-check
```

### Checks (fast vs strict)
- During development: `./dev dev-check` (fast loop)
- Before release: `./dev release-check` (strict: Python 3.12.x + clean tree)

> **Note**: If anything fails, follow SSOT: **[Docs/setup/python-3.12.md](Docs/setup/python-3.12.md)**.
> Troubleshooting entry: **[Docs/DOCTOR_VERSION_TROUBLESHOOTING.md](Docs/DOCTOR_VERSION_TROUBLESHOOTING.md)**.

## 🛠️ Usage
```bash
./dev doctor
./dev smoke
./dev diag
```

### Release Check (배포 전 원샷 검증)
```bash
./dev release-check
```
> (doctor --strict → pytest → smoke → commands 재생성 → git status 확인)

## 🛠️ Setup
- **Python**: 3.12.x
- **Node**: v22.22.0
- **codex-cli**: 0.101.0

## 🚦 Start (실제 런타임 실행)
`dev start`는 개인 환경 파일(`.dev/start_profile.json`)에 정의된 커맨드를 실행합니다.
- **템플릿**: `.dev/start_profile.example.json`을 `.dev/start_profile.json`으로 복사해서 `command`/`cwd`를 채우세요.
- **실행 없이 확인**: `dev start --print`

## 📚 Docs
- **문서 인덱스 (SSOT)**: [Docs/README_DOCS_INDEX.md](Docs/README_DOCS_INDEX.md)
- **표준 명령/성공 기준/로그 경로**: [Docs/COMMANDS.md](Docs/COMMANDS.md)
- **디버깅/진단**: [Docs/DEBUGGING.md](Docs/DEBUGGING.md)
- **doctor 버전 이슈**: [Docs/DOCTOR_VERSION_TROUBLESHOOTING.md](Docs/DOCTOR_VERSION_TROUBLESHOOTING.md)
- **WSL/Windows 파일시스템 이슈**: [Docs/WSL_ISSUES_TABLE.md](Docs/WSL_ISSUES_TABLE.md), [Docs/ADR-002-WSL-FILESYSTEM.md](Docs/ADR-002-WSL-FILESYSTEM.md)
- **AI 승인 게이트**: [Docs/CODEX_APPROVAL_GATE.md](Docs/CODEX_APPROVAL_GATE.md)

## 🐧 WSL 안내
- Windows 파일시스템(`/mnt/c`)에서 직접 작업하면 성능/워처/권한 문제가 생길 수 있어, 기본 작업 경로는 WSL의 Linux 경로(`~/...`)를 권장합니다.
- Windows만 써도 동작하지만, 대규모 파일 I/O가 많은 작업은 WSL이 더 안정적일 수 있습니다.

## 🔍 Diagnostics
`dev diag`를 실행하면 진단 번들이 생성됩니다.
생성 폴더(`.logs/diag-<timestamp>/`)를 이슈/PR에 첨부하면 재현과 원인 분석이 빨라집니다.
