# 공통 규격 프롬프트 (Universal Header)

> **용도**: 모든 AI 모델(Codex, Opus, Sonnet, Antigravity 등)에 대화 첫 줄로 붙이는 규격 헤더.
> 복사하여 그대로 사용하세요.

---

## 헤더 본문 (복사용)

```
아래 규칙을 지키며 답해줘.

━━━ 출력 규격 ━━━
출력은 반드시 아래 3개 섹션만 포함한다. 그 외 서론/인사/요약/추가 제안은 넣지 않는다.

## PATCH LIST
- 변경 대상 파일 경로별 1줄 요약
- 형식: `[ACTION] 경로 — 설명`
  - ACTION = CREATE | MODIFY | DELETE | MOVE
- 예: `[CREATE] docs/DEBUGGING.md — 디버깅 체크리스트 + 재현 템플릿`

## READY-TO-PASTE CONTENT
- 파일별 최종 본문 또는 코드 (전문)
- 각 파일은 `### 파일: <경로>` 헤더로 구분
- 코드 블록에 언어 표시 필수 (```bash, ```yaml 등)
- 부분 수정이면 diff 블록 사용:
  ```diff
  -old line
  +new line
  ```

## CHECKS
- 변경 후 실행할 검증 커맨드 (최대 5개)
- 각 커맨드 옆에 성공 기준 1줄
- 형식: `커맨드` → 기대 결과
- 예: `./dev doctor` → "doctor ok", exit 0

━━━ 추가 규칙 ━━━
1. 중복 내용은 한 파일에만 남기고, README는 링크+요약만 둔다.
2. 경로 대소문자(Docs vs docs) 충돌은 하나로 통일한다.
   - 이 프로젝트 기준: `docs/` (소문자)
3. 불확실하면 "가정"을 명시하고, 가정이 깨질 때의 대안을 함께 준다.
   - 형식: `⚠ 가정: ...` / `↳ 대안: ...`
4. 한 번에 변경하는 파일은 5개 이하, 300줄 이하를 권장한다.
   초과 시 분할 계획을 PATCH LIST 앞에 먼저 제시한다.
```

---

## 사용 예시

```
[공통 규격 헤더]

./dev에 diag 서브커맨드를 추가해줘.
- OS, Node, Python, Git 정보를 .logs/diag.log에 기록
- 출력은 터미널 + 로그 동시
```

예상 출력:
```
## PATCH LIST
- [MODIFY] dev — diag 서브커맨드 추가 (case문 확장)
- [CREATE] tests/diag.bats — diag 서브커맨드 테스트 3건

## READY-TO-PASTE CONTENT
### 파일: dev
  (코드 본문...)

### 파일: tests/diag.bats
  (테스트 본문...)

## CHECKS
1. `./dev diag` → "diag ok", exit 0
2. `cat .logs/diag.log` → OS/Node/Python/Git 4줄 이상 출력
3. `npx bats tests/diag.bats` → 3 tests, 0 failures
```
