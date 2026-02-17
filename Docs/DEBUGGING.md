# 디버깅 가이드 (DEBUGGING.md)

> 이 문서는 msw-vampser 프로젝트의 **디버깅 확률을 최소화**하기 위한 표준 절차를 정의합니다.

---

## 1. 사전 점검 체크리스트

모든 디버깅 시도 **전에** 아래를 확인하세요.

- [ ] `./dev doctor` 출력이 **0 warnings, 0 errors** 인가?
- [ ] `.venv/` 가상환경이 활성화되어 있는가?
- [ ] `node -v` 가 v22.x 를 반환하는가?
- [ ] 현재 브랜치의 마지막 커밋이 CI green 인가?
- [ ] `.logs/dev.log` 에 이전 세션의 미해결 에러가 없는가?

---

## 2. 이슈 재현 템플릿 (Reproduction Template)

이슈 보고 시 아래 형식을 복사하여 사용하세요.

```markdown
### 🐛 Bug Report

**환경**
- OS: WSL2 Ubuntu 24.04 / Windows 11
- Node: v22.22.0
- Python: 3.12.3
- `./dev doctor` 결과: (전문 붙여넣기)

**재현 순서**
1. `cd ~/projects/msw-vampser`
2. `./dev run`
3. (구체적인 조작 순서)

**기대 동작**
- (정상적으로 일어나야 할 일)

**실제 동작**
- (실제로 발생한 일)

**관련 로그**
- `.logs/dev.log` 중 에러 부분:
```
(여기에 로그 붙여넣기)
```

**스크린샷/녹화** (있으면)
```

---

## 3. 원인 격리 규칙 (Fault Isolation)

| 단계 | 행동 | 판단 기준 |
|:---:|:---|:---|
| 1 | `./dev doctor` 실행 | 환경 이상 여부 먼저 배제 |
| 2 | `./dev test --unit <module>` | 해당 모듈만 단독 테스트 |
| 3 | 최근 커밋 `git diff HEAD~1` 확인 | 변경된 파일이 원인과 관련 있는지 |
| 4 | `git stash && ./dev run` | 내 변경 사항 임시 제거 후 재현 시도 |
| 5 | 바이너리 서치 (`git bisect`) | 어느 커밋에서 깨졌는지 특정 |

> **금지**: "아마 이 부분이 문제일 것" 추측만으로 코드 수정하는 행위.
> 반드시 **로그 → 격리 → 확인 → 수정** 순서를 따릅니다.

---

## 4. 로그 수집 규칙

### 4.1 로그 파일 위치 및 용도

| 파일 | 용도 | 자동생성 |
|:---|:---|:---:|
| `.logs/dev.log` | `./dev` 의 모든 명령 실행 기록 | ✅ |
| `.logs/run.log` | `./dev run` 실행 시 stdout/stderr | ✅ |
| `.logs/test.log` | `./dev test` 결과 | ✅ |
| `.logs/diag.log` | `./dev diag` 환경 진단 스냅샷 | ✅ |

### 4.2 로그 수집 의무 사항

1. **이슈 보고 시** `.logs/dev.log` 의 마지막 50줄을 반드시 첨부.
2. **PR 제출 시** `./dev diag` 출력을 PR 본문에 포함.
3. **롤백 발생 시** 롤백 전/후 `.logs/dev.log` 를 각각 보존.

### 4.3 로그 로테이션

- `.logs/*.log` 파일은 **1MB 초과 시** 자동 로테이션 (`.log.1` → `.log.2`).
- 최대 **5세대**까지 보존, 이후 자동 삭제.

---

## 5. 흔한 문제 해결 (Troubleshooting)

| 증상 | 원인 | 해결 |
|:---|:---|:---|
| `node missing` in doctor | NVM이 non-interactive 셸에서 미로드 | `./dev` 스크립트의 NVM 소싱 블록 확인 |
| `python venv missing` | `.venv/` 삭제됨 또는 미생성 | `python3 -m venv .venv` 재실행 |
| `symlink broken` | Windows 경로 변경 또는 드라이브 미마운트 | `ls -la .scripts/moltbot_src` 후 재링크 |
| `Permission denied` on `/mnt/c` | WSL2 DrvFs 권한 이슈 | `wsl.conf` 에 `options = "metadata"` 추가 |
| Git diff에 모든 파일이 변경됨 | CRLF/LF line ending 불일치 | `git config core.autocrlf input` 설정 |
