# Universal Auth, Resilience, and Performance Contract

## What “all models” means

ClauDeus routes every model through the strongest official method exposed by its provider:

1. OAuth 2.0 PKCE
2. OAuth 2.0 device flow
3. official CLI delegated authentication
4. short-lived bearer tokens issued by trusted cloud CLIs
5. API key or environment credential
6. local anonymous runtime

OAuth is provider/account-level. ClauDeus does not invent OAuth for providers that do not offer it, and it does not extract browser cookies or subscription tokens.

## Runtime implementation

The implementation lives in `Kyuha927/copilot`:

- `scripts/auth_broker.py`
- `scripts/credential_command_auth.py`
- `scripts/auth_capabilities.py`
- `scripts/auth_matrix.py`
- `scripts/provider_catalog.py`
- `config/providers.public.json`
- `scripts/resilient_router.py`
- `scripts/context_ledger.py`
- `scripts/token_budget.py`
- `scripts/tool_budget.py`
- `scripts/benchmark_control_plane.py`
- `scripts/benchmark_competitors.py`

## Failure containment

ClauDeus cannot prevent an external network, provider, account, disk, or credential from failing. It prevents those failures from escaping as uncontrolled application crashes by using:

- structured auth errors
- model-route-level circuit breakers
- bounded retries
- total-attempt caps
- execution deadlines
- empty-response rejection
- cross-provider fallback
- raw diagnostic logs
- safe `FAILED_CONTAINED` responses

External tool schemas are routed only to adapters that explicitly support the `tools` option. Incompatible routes are skipped instead of silently ignoring the tools or throwing an uncontrolled `TypeError`.

## Cloud OAuth paths

- Google Vertex obtains a short-lived bearer token from `gcloud auth print-access-token`.
- Azure Foundry obtains a short-lived Entra token from `az account get-access-token --resource https://cognitiveservices.azure.com`.
- Azure can fall back to an official API key when the Entra/CLI route is unavailable.
- CLI-issued tokens are held only in process memory, cached briefly to avoid repeated subprocess calls, and never written to credential storage or logs.

## Token-efficiency design

ClauDeus reduces prompt input before compaction:

- content-hash deduplication
- session-persistent delta context
- active task-tag filtering
- strict context budgets
- deterministic clipping of oversized required context
- task-scoped tool selection
- four-tool default maximum
- 900-token tool-schema maximum

An unchanged second turn is required by CI to resend zero context-fragment tokens through the delta path.

## Verified control-plane evidence

GitHub Actions `Runtime Smoke` run #87 completed successfully on 2026-07-27 after the final Azure Entra resource correction.

| Metric | Verified result |
| --- | ---: |
| Unhandled exceptions | 0 |
| Context planning p50 | 9.15 ms |
| Duplicate token savings | 37.77% |
| Task-tag token savings | 26.40% |
| Delta planning p50 | 1.11 ms |
| Unchanged second-turn context tokens | 0 |
| Delta replay savings | 100% |
| Required-context clipping p50 | 21.84 ms |
| Required-context overflow | 0 tokens |
| Route ranking p50 | 0.20 ms |
| Tool planning p50 | 0.43 ms |
| Selected tool schemas | 4 tools / 132 estimated tokens |
| Auth resolution p50 | 1.57 μs |

The final auth matrix declared 20 provider routes. In clean CI, only the anonymous local route was ready because no external credentials or CLIs were installed; all other routes were reported as `CONFIGURATION_REQUIRED` without exposing secrets.

Full runtime evidence is recorded in `Kyuha927/copilot/docs/runtime_verification_20260727.md`.

## Performance claim policy

“Faster than OpenCode” and “more token-efficient than Pi” are benchmark goals, not assumptions.

A claim may be published only after `scripts/benchmark_competitors.py` compares all systems with:

- the same machine
- the same model and provider
- the same account tier
- the same repository snapshot
- the same task prompt
- independent workspaces
- the same verification command
- 100% correctness for every measured run

## Commands

```bash
# Redacted auth readiness
python scripts/auth_matrix.py \
  --catalog config/providers.public.json \
  --out .logs/auth_matrix.json

# Internal control-plane gates
python scripts/benchmark_control_plane.py \
  --runs 5 \
  --assert-targets \
  --out .logs/control_plane_benchmark.json

# Fair external comparison
python scripts/benchmark_competitors.py \
  --config benchmarks/competitors.example.json \
  --repo /path/to/test-repo \
  --prompt-file /path/to/task.md \
  --provider PROVIDER \
  --model MODEL \
  --runs 3
```

## Current official delegated-login routes

- OpenAI Codex CLI
- GitHub Copilot CLI
- Claude Code CLI
- Antigravity CLI
- Google Cloud CLI to Vertex AI
- Azure CLI to Azure Foundry/OpenAI v1

GitHub Copilot CLI is especially useful as a single official GitHub login surface that can expose selected OpenAI, Anthropic, Google, and Microsoft models without ClauDeus handling the subscription token itself.
