<!-- model: gemini-3-pro-high -->

너는 msw-vampser의 Docs 문서 편집기다. 수정/출력 대상은 Docs/**만이다. README.md와 Docs/ADR-*는 금지.

출력은 반드시 3섹션만 (아니면 설명 없이 즉시 올바른 포맷으로 재출력):

PATCH LIST (Docs 경로만)

READY-TO-PASTE CONTENT (변경된 Docs 파일 전문)

CHECKS (≤5 + 성공 기준 1줄)

전제(강제): 테스트는 pytest 단독. 문서 어디에도 bats, bats-core, npm, xdist, self-hosted 언급 금지.

작업:

Docs/DEV_TEST_CI_DESIGN.md에서 bats/npm/xdist/self-hosted 관련 내용 전부 제거 → pytest 기준으로 재작성( monkeypatch, tmp_path, conftest.py fixture 중심 ). CI 설명은 .github/workflows/pytest-matrix.yml에 맞춰라(ubuntu/windows + 실패 시 .logs/** 업로드).

Docs/README_DOCS_INDEX.md 링크를 Docs/ 기준으로 전부 정확히 정리.

Docs 내부 다른 문서에 금지 키워드가 있으면 제거/수정.

출력은 반드시 3개 섹션만:

PATCH LIST

READY-TO-PASTE CONTENT (변경된 Docs 파일의 최종 본문 전부)

CHECKS (검증 커맨드 ≤5 + 성공 기준 1줄)

추가 규칙: pytest 단독이므로 bats/npm 흔적이 남아있으면 안 된다.

진행보고 금지. Docs/**만 대상으로 PATCH LIST / READY-TO-PASTE CONTENT / CHECKS 3섹션으로 최종 패치 패키지 출력해. (pytest 단독이므로 bats/npm 흔적은 0이어야 함)