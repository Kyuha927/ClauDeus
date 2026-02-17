# ./dev 테스트 전략 & CI 설계안

> `./dev` 의 모든 서브커맨드를 안정적으로 유지하기 위한 테스트/CI 아키텍처입니다.
> Codex가 그대로 구현할 수 있도록 목차 → 테스트 케이스 목록 → 워크플로우 순서로 작성합니다.

---

## 1. 테스트 대상 매트릭스

| 서브커맨드 | 카테고리 | Mocking 대상 | 우선순위 |
|:---|:---|:---|:---:|
| `doctor` | 환경 진단 | `command -v`, 파일 존재 여부 | P0 |
| `diag` | 환경 스냅샷 | `node -v`, `python3 --version`, `git` | P0 |
| `test` | 무결성 검증 | Python import, npm test | P1 |
| `run` | 실행 | 서브프로세스 stdout/stderr | P1 |
| `msw:link` | 심링크 관리 | `ln -s`, `readlink` | P1 |
| `clone` | 프로젝트 복제 | `git clone`, 디렉토리 생성 | P2 |
| `rollback` | 롤백 | `git revert`, `git stash` | P2 |
| `smoke` | 통합 점검 | 전체 파이프라인 (doctor→test→run) | P2 |

---

## 2. 테스트 케이스 목록

### 2.1 `./dev doctor` (P0)

```
TC-DOC-01: node가 PATH에 있을 때 → 버전 출력, exit 0
TC-DOC-02: node가 없을 때 → "node missing" 로그, exit 1
TC-DOC-03: .venv/bin/python 존재 시 → "python venv found", exit 0
TC-DOC-04: .venv/ 미존재 시 → "python venv missing", exit 1
TC-DOC-05: .scripts/moltbot_src 심링크 정상 → "symlink found", exit 0
TC-DOC-06: .scripts/moltbot_src 깨진 심링크 → "symlink missing", exit 1
TC-DOC-07: codex 미설치 시 → 경고만 출력, exit 0 (non-fatal)
```

### 2.2 `./dev diag` (P0)

```
TC-DIAG-01: 모든 도구 존재 시 → JSON/텍스트 스냅샷, exit 0
TC-DIAG-02: .logs/diag.log에 결과 기록 확인
TC-DIAG-03: git 미설치 시 → 해당 필드 "N/A", exit 0 (graceful)
```

### 2.3 `./dev run` (P1)

```
TC-RUN-01: scan_msw.py 정상 실행 → stdout 캡처, exit 0
TC-RUN-02: scan_msw.py 에러 시 → stderr 캡처, exit 1
TC-RUN-03: .logs/run.log에 실행 결과 기록 확인
```

### 2.4 `./dev msw:link` (P1)

```
TC-LINK-01: 유효한 Windows 경로 → 심링크 생성, exit 0
TC-LINK-02: 이미 존재하는 심링크 → 재생성(force), exit 0
TC-LINK-03: 잘못된 경로 → 에러 메시지, exit 1
```

### 2.5 `./dev rollback` (P2)

```
TC-ROLL-01: clean working tree → git revert HEAD, exit 0
TC-ROLL-02: dirty working tree → git stash 후 revert, exit 0
TC-ROLL-03: revert 충돌 시 → 안내 메시지 + 수동 해결 요청, exit 1
```

---

## 3. Mocking 전략

### 3.1 원칙
- **파일시스템**: 임시 디렉토리(`mktemp -d`)에 가짜 프로젝트 구조 생성.
- **서브프로세스**: `command -v` 를 래핑하는 함수로 대체.
- **환경변수**: `NVM_DIR`, `HOME` 등을 테스트별 격리.

### 3.2 OS 독립성 보장

```bash
# test_runner.sh 상단
OS="$(uname -s)"
case "$OS" in
  Linux*)   MOCK_HOME=$(mktemp -d) ;;
  MINGW*|MSYS*|CYGWIN*)  MOCK_HOME=$(mktemp -d -p "$TEMP") ;;
esac
export HOME="$MOCK_HOME"
```

### 3.3 테스트 프레임워크

| 옵션 | 장점 | 단점 | 추천 |
|:---|:---|:---|:---:|
| **bats-core** | Bash 네이티브, 가볍고 CI 친화적 | 복잡한 assertion 한계 | ✅ |
| **shunit2** | xUnit 스타일, 익숙한 패턴 | 설치 필요, 느림 | △ |
| **직접 작성** | 의존성 0 | 유지보수 비용 증가 | ❌ |

**결론**: `bats-core` 사용. `npm install --save-dev bats` 로 프로젝트 내 관리.

---

## 4. CI 워크플로우 설계 (GitHub Actions)

### 4.1 워크플로우 단계

```yaml
# .github/workflows/dev-ci.yml
name: dev-cli-ci

on:
  push:
    branches: [main, dev]
    paths: ['dev', 'tests/**', '.scripts/**']
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

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '22'

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Create venv
        run: python3 -m venv .venv

      - name: Install bats
        run: npm install --save-dev bats

      - name: Run tests
        run: npx bats tests/

      - name: Upload logs on failure
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: dev-logs-${{ matrix.os }}
          path: .logs/
          retention-days: 7
```

### 4.2 실패 시 로그 아티팩트

- CI 실패 시 `.logs/` 디렉토리 전체를 GitHub Actions Artifact로 업로드.
- 보존 기간: **7일** (디스크 비용 최소화).
- 다운로드 후 로컬에서 `cat .logs/dev.log` 로 즉시 원인 분석 가능.

---

## 5. Codex 구현 체크리스트

Codex가 이 설계를 구현할 때 따라야 할 순서:

- [ ] `tests/` 디렉토리 생성
- [ ] `bats` 설치 (`npm install --save-dev bats`)
- [ ] `tests/doctor.bats` 작성 (TC-DOC-01 ~ 07)
- [ ] `tests/diag.bats` 작성 (TC-DIAG-01 ~ 03)
- [ ] `tests/run.bats` 작성 (TC-RUN-01 ~ 03)
- [ ] `tests/helpers/` 에 mock 유틸리티 스크립트 배치
- [ ] `.github/workflows/dev-ci.yml` 생성
- [ ] 로컬에서 `npx bats tests/` 전체 통과 확인
- [ ] PR 제출 후 CI green 확인
