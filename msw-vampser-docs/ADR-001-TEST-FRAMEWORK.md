# 테스트/CI 프레임워크 결정 (ADR-001)

> 출력 규격: PATCH LIST / READY-TO-PASTE CONTENT / CHECKS

---

## PATCH LIST

- `[MODIFY] docs/DEV_TEST_CI_DESIGN.md` — 테스트 프레임워크를 bats-core → **pytest**로 변경, CI 워크플로우 업데이트
- `[CREATE] docs/adr/ADR-001-test-framework.md` — 결정 기록 (ADR)
- `[MODIFY] .github/workflows/dev-ci.yml` — pytest 기반으로 CI 파이프라인 재구성

---

## READY-TO-PASTE CONTENT

### 파일: docs/adr/ADR-001-test-framework.md

```markdown
# ADR-001: 테스트 프레임워크 선택 (pytest vs bats-core)

- 상태: **승인됨**
- 일자: 2026-02-17
- 결정자: jhk92

## 컨텍스트

msw-vampser 프로젝트의 `./dev` CLI를 안정적으로 유지하기 위한 테스트 프레임워크를 확정해야 한다.
기존 설계안(DEV_TEST_CI_DESIGN.md)에서는 bats-core를 권장했으나,
실제 리포를 분석한 결과 `tools/dev_cli.py` (1058줄, Python)가 핵심 엔트리포인트이고,
`tests/test_dev_cli.py`에 pytest 기반 테스트 7건이 이미 존재한다.

## 선택지

| # | 옵션 | 유지보수 | OS 호환 | 디버깅 비용 | Mocking | 기존 자산 활용 |
|---|------|---------|---------|-----------|---------|--------------|
| 1 | **pytest** | ✅ Python 생태계 그대로 | ✅ Win/Linux/Mac 네이티브 | ✅ pdb/breakpoint 즉시 | ✅ monkeypatch, tmp_path 내장 | ✅ test_dev_cli.py 7건 즉시 |
| 2 | bats-core | △ Bash 전용, 별도 학습 | △ Windows에서 Git Bash 필요 | ❌ echo 디버깅만 가능 | ❌ 함수 래핑 수동 구현 | ❌ 기존 없음, 처음부터 작성 |
| 3 | 하이브리드 | ❌ 두 프레임워크 동시 관리 | △ 양쪽 환경 모두 설정 | ❌ 이중 디버깅 비용 | △ 혼합 | △ 부분 활용 |

## 결정

**옵션 1: pytest 단독 사용.**

이유:
- `dev_cli.py`가 Python이므로 pytest의 `monkeypatch`, `tmp_path`로 파일시스템/서브프로세스를 **완전 격리** 가능.
- 기존 `test_dev_cli.py`에 doctor/diag/link/clone/rollback 테스트가 이미 패턴 확립됨.
- bats-core를 추가하면 **2개 언어의 테스트를 동시 관리**하는 오버헤드만 증가.

## 결과

- `./dev` bash 래퍼는 단순 진입점(5줄 이하)으로 유지, **로직은 전부 dev_cli.py에 집중**.
- bash 래퍼 자체 테스트는 pytest의 `subprocess.run` mock으로 커버.
- CI 워크플로우에서 bats 설치 단계 제거, pytest만 실행.

## 되돌리기 조건

- `./dev` bash 래퍼가 100줄을 넘는 독자적 로직을 갖게 되면 bats-core 재검토.
- dev_cli.py를 Go/Rust로 포팅하게 되면 해당 언어의 테스트 프레임워크로 전환.
```

---

### 파일: Codex 구현 체크리스트 (pytest 기준, 10줄)

```markdown
## pytest 기반 구현 체크리스트

- [ ] 1. `tests/` 디렉토리에 `conftest.py` 생성 → `isolated_repo` fixture 공통화
- [ ] 2. `tests/test_doctor.py` 작성 → TC-DOC-01~07 (node/venv/symlink 존재/미존재 7건)
- [ ] 3. `tests/test_diag.py` 작성 → TC-DIAG-01~03 (스냅샷 생성, 로그 기록, graceful fallback)
- [ ] 4. `tests/test_run.py` 작성 → TC-RUN-01~03 (정상/에러 실행, 로그 기록)
- [ ] 5. `tests/test_msw_link.py` 보강 → TC-LINK-01~03 (유효/중복/잘못된 경로)
- [ ] 6. `tests/test_rollback.py` 작성 → TC-ROLL-01~03 (clean/dirty/conflict)
- [ ] 7. `tests/test_smoke.py` 작성 → doctor→test→run 통합 시나리오 1건
- [ ] 8. `pyproject.toml`에 `[tool.pytest.ini_options]` 추가 (testpaths, log_cli 등)
- [ ] 9. `.github/workflows/dev-ci.yml` 생성 → matrix(ubuntu/windows), 실패 시 .logs/ 업로드
- [ ] 10. 로컬에서 `pytest tests/ -v` 전체 통과 확인 후 PR 제출
```

---

### 파일: .github/workflows/dev-ci.yml (pytest 버전)

```yaml
name: dev-cli-ci

on:
  push:
    branches: [main, dev]
    paths: ['tools/dev_cli.py', 'tests/**', 'dev']
  pull_request:
    branches: [main, dev]

jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
    runs-on: ${{ matrix.os }}

    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install test dependencies
        run: pip install pytest

      - name: Run pytest
        run: pytest tests/ -v --tb=short --junitxml=.logs/pytest-results.xml

      - name: Upload logs on failure
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: dev-logs-${{ matrix.os }}-${{ github.run_id }}
          path: |
            .logs/
            .dev/
          retention-days: 7

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: pytest-results-${{ matrix.os }}
          path: .logs/pytest-results.xml
          retention-days: 30
```

---

## CHECKS

| # | 커맨드 | 성공 기준 |
|:-:|:---|:---|
| 1 | `pytest tests/test_dev_cli.py -v` | 기존 7건 전부 PASSED, exit 0 |
| 2 | `pytest tests/ -v --tb=short` | 전체 테스트 0 failures |
| 3 | `python -c "import tools.dev_cli"` | ImportError 없음, exit 0 |
| 4 | `cat .github/workflows/dev-ci.yml` | `pytest` 문자열 존재, `bats` 문자열 없음 |
| 5 | `./dev doctor` | "doctor ok", exit 0 |
