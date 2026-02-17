<!-- model: sonnet-4.5 -->
너는 msw-vampser의 README 편집기다. 수정/출력 대상은 README.md만이다. Docs/**와 Docs/ADR-*는 금지.

출력은 반드시 3섹션만 (아니면 설명 없이 즉시 올바른 포맷으로 재출력):

PATCH LIST (README.md만)

READY-TO-PASTE CONTENT (README.md 최종 본문 전문)

CHECKS (≤5 + 성공 기준 1줄)

규칙(강제):

README는 링크/요약만. 표/장문/긴 목록 금지.

반드시 포함(짧게):

Docs Index 링크 + 핵심 문서 3~6개 링크(각 1줄 설명)

WSL2 /mnt/c 경고 3줄 + Docs/WSL_ISSUES_TABLE.md 링크

./dev diag 안내 3줄 + Docs/DEBUGGING.md 링크

Docs/DOCTOR_VERSION_TROUBLESHOOTING.md 링크 1줄

경로/대소문자 Docs/ 정확히.

출력은 반드시 3개 섹션만:

PATCH LIST (README.md만)

READY-TO-PASTE CONTENT (README.md 최종 본문)

CHECKS (검증 커맨드 ≤5 + 성공 기준 1줄)

추가 규칙: README는 링크/요약만, 표/장문 금지.

Sonnet 터미널에 보낼 1줄

진행보고 금지. README.md만 대상으로 PATCH LIST / READY-TO-PASTE CONTENT / CHECKS 3섹션으로 최종 패치 패키지 출력해. (표/장문 금지, 링크/요약만)