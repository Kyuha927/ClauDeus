# Agents Operating Rules (Debug-Probability-First)

## Non-negotiables
- Every change must reduce future debugging probability.
- No silent behavior: logs + invariants + health checks.
- Always add a reproduction path (steps or script) for bugfixes.

## Workflow
1) Planner: write a short plan + risks + rollback.
2) Implementer: small commits, instrumentation first.
3) Reviewer: check invariants, concurrency, lifecycle, error paths.
4) QA: run ./dev doctor, tests, minimal scenario replay.
5) Scribe: update CHANGELOG + troubleshooting notes.

## Guardrails
- Prefer idempotent scripts.
- Add tracing IDs to async/timer flows.
- Add "single-instance" guards for UI/HUD-like components.

## Cure for HitVFX-like Problems
- **Lifecycle/Instance Guard**: HUD/Overlay components MUST use Singleton + ownerId validation.
- **State Read-back**: UI visibility/alpha changes MUST be verified with "set then read-back assert".
- **Tracing Tokens**: Every timer/coroutine MUST have a sequence token logged for end-to-end tracking.
