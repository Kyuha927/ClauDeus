# Universal Auth, Resilience, and Performance Contract

## What “all models” means

ClauDeus routes every model through the strongest official method exposed by its provider:

1. OAuth 2.0 PKCE
2. OAuth 2.0 device flow
3. official CLI delegated authentication
4. API key or environment credential
5. local anonymous runtime

OAuth is provider/account-level. ClauDeus does not invent OAuth for providers that do not offer it, and it does not extract browser cookies or subscription tokens.

## Runtime implementation

The implementation lives in `Kyuha927/copilot`:

- `scripts/auth_broker.py`
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

GitHub Copilot CLI is especially useful as a single official GitHub login surface that can expose selected OpenAI, Anthropic, Google, and Microsoft models without ClauDeus handling the subscription token itself.
