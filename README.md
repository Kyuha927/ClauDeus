# ClauDeus

AI 모델 병렬 실행 및 자동화 툴킷입니다.

## 📚 Docs Index
- [Full Index](Docs/README_DOCS_INDEX.md): 전체 문서 목록 및 상세 설명
- [Debugging](Docs/DEBUGGING.md): 오류 진단 절차 및 `./dev diag` 문제 해결 가이드
- [Contributing](Docs/CONTRIBUTING.md): 프로젝트 기여 규칙 및 코드 스타일 가이드
- [Architecture](Docs/DEV_TEST_CI_DESIGN.md): CI/Test 구성 및 개발 워크플로우 (Pytest 기반)
- [Codex Policy](Docs/CODEX_APPROVAL_GATE.md): AI 자동 수행/승인 규칙

## ⚠️ WSL2 /mnt/c Warning
1. WSL2에서 `/mnt/c` 등 Windows 파일 시스템 직접 접근 시 성능 저하 및 권한 오류가 발생합니다.
2. 모든 작업은 Linux 전용 경로(`~/`)에서 수행하고, 파일 권한을 준수하십시오.
3. 상세 해결법은 **[WSL Issue Table](Docs/WSL_ISSUES_TABLE.md)**을 참조하세요.

## 🔍 Diagnostic Guide (./dev diag)
실행 중 문제가 발생하면 `./dev diag`를 실행하여 시스템 진단 로그를 생성하세요.
생성된 `diag_[date].log` 파일을 이슈와 함께 첨부하면 빠른 원인 분석이 가능합니다.
상세 진단 항목은 **[Debugging Guide](Docs/DEBUGGING.md)**를 확인하십시오.

---
[Doctor Version Troubleshooting](Docs/DOCTOR_VERSION_TROUBLESHOOTING.md)
