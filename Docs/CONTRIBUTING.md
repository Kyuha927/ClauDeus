# 기여 가이드 (CONTRIBUTING.md)

> msw-vampser 프로젝트에 기여할 때 반드시 따라야 할 규칙입니다.

---

## 1. 핵심 원칙: `./dev` 를 통해서만 실행

```
✅  ./dev doctor
✅  ./dev run
✅  ./dev test

❌  python3 scripts/scan_msw.py        ← 직접 실행 금지
❌  node src/index.js                  ← 직접 실행 금지
❌  npm start                          ← 직접 실행 금지
```

**이유**: `./dev` 는 NVM 소싱, venv 활성화, 로그 기록을 자동 처리합니다.
이를 우회하면 환경 불일치로 인한 "내 컴퓨터에선 되는데" 문제가 발생합니다.

---

## 2. PR 제출 체크리스트

PR 본문에 아래 체크리스트를 복사하여 모두 충족 후 제출하세요.

```markdown
### PR Checklist

- [ ] `./dev doctor` 통과 (0 warnings, 0 errors)
- [ ] `./dev test` 통과 (전체 테스트 green)
- [ ] `./dev diag` 출력 전문을 이 PR 본문에 첨부
- [ ] 변경된 파일이 **1개의 논리적 단위**(기능/버그/리팩터)에만 해당
- [ ] 커밋 메시지가 `type(scope): description` 형식 준수
  - 예: `feat(player): add dash ability`
  - 예: `fix(spawner): prevent double-spawn on wave start`
- [ ] 새 파일 추가 시 README 또는 관련 문서 업데이트 완료
- [ ] `/mnt/c` 경로를 하드코딩하지 않음 (상대경로 또는 환경변수 사용)
```

---

## 3. 커밋 규칙

### 3.1 커밋 메시지 컨벤션

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

| type | 용도 |
|:---|:---|
| `feat` | 새 기능 추가 |
| `fix` | 버그 수정 |
| `docs` | 문서만 변경 |
| `refactor` | 기능 변경 없는 코드 구조 개선 |
| `test` | 테스트 추가/수정 |
| `chore` | 빌드, CI, 설정 변경 |

### 3.2 커밋 크기 제한

- **1 커밋 = 1 롤백 단위**. `git revert` 한 번으로 원상복구 가능해야 함.
- 파일 변경 **10개 이하**, 줄 변경 **300줄 이하** 권장.
- 초과 시 커밋을 분할하거나, PR을 나누세요.

---

## 4. `./dev diag` 첨부 규정

모든 이슈 보고 및 PR에는 `./dev diag` 출력을 첨부해야 합니다.

```bash
cd ~/projects/msw-vampser
./dev diag
```

출력 예시:
```
[2026-02-17 21:00:00] diag start
OS: Linux 6.x (WSL2)
Node: v22.22.0
Python: 3.12.3
Codex: 0.101.0
Source: /mnt/c/Users/jhk92/Downloads/msw2 (symlink OK)
Venv: .venv (active, 35 packages)
Git: branch=main, clean=true, last_commit=abc1234
[2026-02-17 21:00:01] diag ok
```

> **미첨부 PR은 리뷰 대상에서 제외**됩니다.

---

## 5. 브랜치 전략

| 브랜치 | 용도 | 머지 방향 |
|:---|:---|:---|
| `main` | 항상 실행 가능한 안정 버전 | ← `dev` |
| `dev` | 개발 통합 브랜치 | ← `feat/*`, `fix/*` |
| `feat/<name>` | 기능 개발 | → `dev` |
| `fix/<name>` | 버그 수정 | → `dev` |
